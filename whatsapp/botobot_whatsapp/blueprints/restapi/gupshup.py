import requests, logging, threading, urllib, time, datetime
from flask import request, abort, current_app as app
from flask_restful import reqparse, Resource
from botobot_whatsapp.models import GupshupMessage

ERROR_MESSAGE = 'Sorry, an error occurred while processing your request. Please, try again later.'

class WhatsappGupShupWebhook(Resource):
    """ Webhook for gupshup API callback.
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app', required=True)
        self.parser.add_argument('version', required=True)
        self.parser.add_argument('type', required=True)
        self.parser.add_argument('timestamp', type=int)
        self.parser.add_argument('payload', type=dict)
        self.parser.add_argument('token', location='args')

        # Config headers used in requests.
        self.gupshup_headers = { 'Content-Type': 'application/x-www-form-urlencoded', 'apikey': app.config.GUPSHUP_API_KEY, 'Cache-Control' : 'no-cache', 'cache-control': 'no-cache' }
        self.botobot_core_headers = { 'Content-Type': 'application/json' }

    def post(self):
        """ Process the message received from gupshup.
        """
        self.args = self.parser.parse_args()
        if not self.validate_args(self.args):
            abort(404)

        # Get the request type.
        req_type, req_payload = self.args.get('type'), self.args.get('payload')

        # Save the payload data received.
        self.save_data_from_payload(req_type, req_payload)

        # Process the message in a separate thread, so it won't delay the response for this request.
        if req_type == 'message' and req_payload:
            threading.Thread(target=self.api_response, args=[app._get_current_object()]).start()

        # Inform gupshup that the message was received (204-Empty Response).
        return ('', 204)

    def api_response(self, app):
        """ Exchange messages between botobot API and Gupshup API.
        """
        # Because it's in a thread, we need to push application context.
        app.app_context().push()
        payload = self.args.get('payload')

        # Check if message and source are valid.
        message, sender = self.get_message_data_from_payload(payload)
        if message is None and sender is None:
            return

        self.relay_message(sender, message)
    
    def relay_message(self, sender, message):
        """ Send the message received from gupshup to botobot API, then send the response back to gupshup.
        """
        json_data = {'chat_id' : sender, 'message' : message, 'client' : 'whatsapp', 'version' : '1.0'}
        try:
            # Make a request to Botobot CORE.
            req = requests.Session().post(app.config.BOTOBOT_CORE_WEBHOOK, json = json_data, headers = self.botobot_core_headers)
            if req.status_code >= 300:
                raise Exception(f'HTTP ERROR {req.status_code}! Content: {req.text}')

            # Send the response to Gupshup API.
            response = req.json()
            for i, message in enumerate(response.get('messages')):
                gup_response = self.send_message(chat_id=sender, text=message)

                # Wait for the gupshup confirmation of message enqueued, sent, delivered or read, 
                # before send the next one. Otherwise, messages can reach the user in a random order.
                if i < len(response.get('messages')) - 1:
                    self.wait_message_enqueue(gup_response.get('messageId'))
        except:
            self.send_message(chat_id=sender, text=ERROR_MESSAGE)
            raise

    def wait_message_enqueue(self, message_id, timeout = 60, sleep_time = 0.25):
        """ Wait until gupshup confirms that the message was sent to WhatsApp queue.
            There is an default timeout of 60 seconds.
        """
        seconds = 0
        while seconds < timeout:
            msg = GupshupMessage.get_message_enqueued(message_id)
            if msg and msg.message_event_type == 'failed':
                raise Exception(f'GUPSHUP ERROR! message_id={message_id}, message_event_type={msg.message_event_type}')
            if msg and msg.message_event_type in ['enqueued', 'sent', 'delivered','read']:
                break
            time.sleep(sleep_time)
            seconds += sleep_time

    def send_message(self, chat_id, text):
        """ Send a message to gupshup endpoint.
        """
        payload = { 'source' : app.config.GUPSHUP_WHATSAPP_PHONE, 'destination' : chat_id, 'message' : {'type' : 'text', 'text' : text }, 'src.name' : app.config.GUPSHUP_APPNAME, 'channel' : 'whatsapp', 'disablePreview' : 'true'}
        gup_message = GupshupMessage(payload = payload, type = 'text', destination = chat_id, outbound = True, dt = datetime.datetime.now())
        gup_message.save()

        # Send the request.
        req = requests.Session().post(app.config.GUPSHUP_ENDPOINT_URL, data = urllib.parse.urlencode(payload), headers = self.gupshup_headers)
        json_data = req.json()

        # Update the record to the database.
        gup_message.response_code = req.status_code
        gup_message.message_id = json_data['messageId'] if json_data else None
        gup_message.save()
        return json_data

    def validate_args(self, args):
        """ Validates the token and the app name.
        """
        if args.get('token') != app.config.WEBHOOK_TOKEN:
            logging.warn(f"Incorrect token: {args.get('token')}")
            return False

        if args.get('app') != app.config.GUPSHUP_APPNAME:
            logging.warn(f"Incorrect app name! Expected: {app.config.GUPSHUP_APPNAME}, received: {args.get('app')}.")
            return False
        return True

    def get_message_data_from_payload(self, payload):
        """ Returns the message and the sender contained on the payload.
        """
        message = payload.get('payload').get('text')
        if not message or message.strip() == '':
            logging.warn('Empty message received!')
            message = None

        sender = payload.get('source') or payload.get('sender').get('phone') if payload.get('sender') else None
        if not sender:
            logging.warn('Sender not found in the payload!')
            sender = None

        return message, sender

    def save_data_from_payload(self, type, payload):
        """ Extract data from the request payload according to request type and saves it to the database.
        """
        if not payload:
            return

        whatsapp_id = message_id = message_event_type = destination = sender_phone = sender_name = None
        if type == 'message':
            whatsapp_id = payload.get('id')
            sender_phone = payload.get('sender').get('phone') if payload.get('sender') else None
            sender_name = payload.get('sender').get('name') if payload.get('sender') else None
        if type == 'message-event':
            message_id = payload.get('id')
            message_event_type = payload.get('type')
            destination = payload.get('destination')
            whatsapp_id = payload.get('payload').get('whatsappMessageId') if payload.get('payload') else None
        if type == 'user-event':
            sender_phone = payload.get('phone')

        # Save it.
        GupshupMessage(payload = request.get_json(), type = type, message_id = message_id, message_event_type = message_event_type, whatsapp_id = whatsapp_id, destination = destination, sender_phone = sender_phone, sender_name = sender_name, outbound = False, dt = datetime.datetime.now()).save()
