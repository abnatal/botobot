from flask import jsonify
from flask_restful import Resource
from botobot_core.decorators import token_required
from botobot_core.models import Message

class StaticTextResource(Resource):
    """ Provides static texts previously stored on database """

    @token_required
    def post(self, topic):
        message = Message.get('statictext.%s' % topic) or Message.get('statictext.topic_not_found')
        return jsonify({ 'messages' : [message.fulltext], 'quit': True })
