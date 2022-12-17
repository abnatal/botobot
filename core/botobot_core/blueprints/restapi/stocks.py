from flask import jsonify
from flask_restful import Resource, reqparse
from botobot_core.decorators import token_required
from botobot_core.models import Message
from botobot_core.blueprints.restapi.lib.yfclient import YahooFinanceClient

class StocksResource(Resource):
    """ Provides prices of stocks. Powered by Yahoo! Finance. """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('message', type=str)

    @token_required
    def post(self):
        self.args = self.parser.parse_args()
        if not self.args.get('message'):
            return self.handle_start()
        else:
            return self.handle_message(self.args.get('message'))

    def handle_start(self):
        """ Ask user to enter the ticker code """
        return jsonify({ 'messages' : [Message.get('stocks.inform_ticker').fulltext], 'quit': False })

    def handle_message(self, message):
        """ Query the ticker code or quit """
        message = message.lower().strip()
        if message == 'quit':
            return jsonify({ 'messages' : [Message.get('general.bye').fulltext], 'quit': True })
        else:
            return jsonify({ 'messages' : [YahooFinanceClient.get_formatted_stock_info(ticker=message), Message.get('stocks.inform_another_ticker').fulltext], 'quit': False })
