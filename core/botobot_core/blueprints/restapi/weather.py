from flask import jsonify
from flask_restful import Resource
from botobot_core.decorators import token_required
from botobot_core.models import Message
from botobot_core.blueprints.restapi.lib.seventimerclient import SevenTimerClient

class WeatherResource(Resource):
    """ Provides weather data. Powered by 7timer.info API. """

    @token_required
    def post(self):
        """ Response is an intro message plus wheater info about two random cities. """

        stc = SevenTimerClient()
        messages = [Message.get('weather.intro').fulltext]
        for city in [stc.pick_random_city(), stc.pick_random_city()]:
            city['weather_info'] = stc.get_formatted_weather_info(city=city, days=2)
            messages.append(Message.get('weather.result_template').fulltext.format(**city))

        return jsonify({ 'messages' : messages, 'quit': True })