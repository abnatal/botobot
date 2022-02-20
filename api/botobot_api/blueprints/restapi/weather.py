from flask import jsonify
from flask_restful import Resource
from botobot_api.decorators import token_required
from botobot_api.models import Message
from botobot_api.blueprints.restapi.lib.seventimerclient import SevenTimerClient

class WeatherResource(Resource):
    """ Provides weather data. Powered by 7timer.info API. """

    @token_required
    def post(self):
        stc = SevenTimerClient()

        # There is an intro message and one message for each city.
        messages = [Message.get('weather.intro').fulltext]
        for city in [stc.pick_random_city(), stc.pick_random_city()]:
            city['weather_info'] = stc.get_formatted_weather_info(city=city, days=2)
            messages.append(Message.get('weather.result_template').fulltext.format(**city))

        return jsonify({ 'messages' : messages, 'quit': True })