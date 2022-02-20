from flask import jsonify
from flask_restful import Resource
from botobot_api.decorators import token_required
from botobot_api.models import Message

class StaticTextResource(Resource):
    """ Provides static text previously stored on database """

    @token_required
    def post(self, topic):
        message = Message.get('statictext.%s' % topic) or Message.get('statictext.topic_not_found')
        return jsonify({ 'messages' : [message.fulltext], 'quit': True })
