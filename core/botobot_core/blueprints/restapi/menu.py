import requests
from flask import jsonify
from flask_restful import reqparse, abort, Resource
from botobot_core.decorators import token_required
from botobot_core.models import ChatContext, Message, Api

class MenuResource(Resource):
    """ The main menu resource. Gets user input and relays it to other APIs. """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('client', type=str, required=True, help="Invalid request.")
        self.parser.add_argument('version', type=str, required=True, help="Invalid request.")
        self.parser.add_argument('chat_id', type=str, required=True, help="Invalid request.")
        self.parser.add_argument('message', type=str)
        self.parser.add_argument('cmd', type=str)
        self.args = self.context = self.current_api = None

    @token_required
    def post(self):
        """ Entry point: all requests pass here and get a reply or are fowarded to another APIs.
        """
        self.args = self.parser.parse_args()
        self.context = self.get_context(self.args['chat_id'], self.args['client'])

        # A /start command (telegram) was received or previous context does not exist.
        if self.args.get('cmd') == 'start' or (not self.context):
            self.context = self.create_context(self.args['chat_id'], self.args['client'], self.args['version'])
            return self.handle_start()

        # Context exists. Check the message.
        if self.args.get('message'):
            if not self.context.current_api:
                return self.handle_message(self.args.get('message'))
            else:
                return self.forward_message(api=self.context.current_api, message=self.args.get('message'))

        # Wrong request.
        abort(404)

    def handle_start(self):
        """ The very first message when a chat starts. """
        hello = Message.get('general.hello')
        options = ['*%d.* %s' % (i + 1, api.label) for i, api in enumerate(Api.get_all_visible())]
        return jsonify({ 'messages' : [hello.fulltext, "\n".join(options)] })

    def handle_message(self, message):
        """ Chat already started. Handles the user input. """
        try:
            option = int(message.strip())
        except ValueError:
            return jsonify({ 'messages' : [Message.get('general.wrong_option').fulltext] })

        apis = Api.get_all_visible()
        if option >= 1 and option <= len(apis):
            return self.redirect_context(option)

        return jsonify({ 'messages' : [Message.get('general.wrong_option').fulltext] })

    def redirect_context(self, option):
        """ Redirect the context to another API.
            Occurs when user selects a valid option from the main menu.
        """
        self.set_current_api(Api.get_all_visible()[option - 1])
        return self.forward_message(self.context.current_api, message=None)

    def forward_message(self, api, message):
        """ Forwards the message received to the current API.
        """
        req = requests.Session().post(api.url, json = self.make_json_body(message), headers = self.make_headers())

        # Check for errors.
        if req.status_code >= 300:
            self.set_current_api(None)
            return jsonify({ 'messages' : [Message.get('general.request_error').fulltext] })

        # Handle the API response.
        response = req.json()
        messages = response.get('messages') or []
        if response.get('quit'):
            messages.append(Message.get('general.see_you').fulltext)
            self.destroy_current_context()
        return jsonify({ 'messages' : messages })

    def create_context(self, chat_id, client, version):
        return ContextManager.create_context(chat_id=chat_id, client=client, version=version)

    def destroy_current_context(self):
        ContextManager.destroy_context(self.context)

    def get_context(self, chat_id, client):
        return ContextManager.get_context(chat_id=chat_id, client=client)

    def set_current_api(self, api):
        self.context.current_api = api
        ContextManager.save_context(self.context)

    def make_headers(self):
        return { 'Content-Type': 'application/json' } #, 'Authorization': f'JWT {self.auth_token}' }

    def make_json_body(self, message):
        return {'message' : message, 'chat_id' : self.args.get('chat_id'), 'client' : self.args.get('client'), 'version' : self.args.get('version')}

class ContextManager():
    @staticmethod
    def get_context(chat_id, client):
        return ChatContext.get(chat_id=chat_id, client=client)

    @staticmethod
    def create_context(chat_id, client, version):
        ctx = ChatContext(
            chat_id = chat_id,
            client = client,
            version = version,
            current_api = None)
        ctx.save()
        return ctx

    @staticmethod
    def save_context(context):
        context.save()

    @staticmethod
    def destroy_context(context):
        context.delete()
