from datetime import datetime
import random, requests
from botobot_api.models import Message

class SevenTimerClient():
    """ Client for the 7timer.info API. """

    def __init__(self):
        self.service_url = 'https://www.7timer.info/bin/api.pl'
        self.sample_cities = [{ 'city' : 'Belรฉm', 'lon': -48.501, 'lat': -1.456, 'country': '๐ง๐ท' }, { 'city': 'Portel', 'lon': -50.817, 'lat': -1.937, 'country': '๐ง๐ท' }, { 'city': 'Buenos Aires', 'lon': -58.382, 'lat': -34.604, 'country': '๐ฆ๐ท' }, { 'city': 'La Paz', 'lon': -68.119, 'lat': -16.49, 'country': '๐ง๐ด' }, { 'city': 'Caracas', 'lon': -66.904, 'lat': 10.481, 'country': '๐จ๐ด' }, { 'city': 'Santiago', 'lon': -70.669, 'lat': -33.449, 'country': '๐จ๐ฑ' }, { 'city': 'San Francisco', 'lon': -122.419, 'lat': 37.775, 'country': '๐บ๐ธ' }, { 'city': 'Chicago', 'lon': -87.63, 'lat': 41.878, 'country': '๐บ๐ธ' }, { 'city': 'London', 'lon': -0.128, 'lat': 51.507, 'country': '๐ด๓ ง๓ ข๓ ฅ๓ ฎ๓ ง๓ ฟ' }, { 'city': 'Amsterdan', 'lon': 4.904, 'lat': 52.368, 'country': '๐ณ๐ฑ' }, { 'city': 'Berlin', 'lon': 13.405, 'lat': 52.52, 'country': '๐ฉ๐ช' }, { 'city': 'Paris', 'lon': 2.352, 'lat': 48.857, 'country': '๐ซ๐ท' }, { 'city': 'Brussels', 'lon': 4.357, 'lat': 50.848, 'country': '๐ง๐ช' }, { 'city': 'Dublin', 'lon': -6.26, 'lat': 53.35, 'country': '๐ฎ๐ช' }, { 'city': 'Tokyo', 'lon': 139.769, 'lat': 35.68, 'country': '๐ฏ๐ต' }, { 'city': 'Bangkok', 'lon': 100.502, 'lat': 13.756, 'country': '๐น๐ญ' }, { 'city': 'Singapore', 'lon': 103.82, 'lat': 1.352, 'country': '๐ธ๐ฌ' }, { 'city': 'Beijing', 'lon': 116.407, 'lat': 39.904, 'country': '๐จ๐ณ' }, { 'city': 'Kuala Lumpur', 'lon': 101.687, 'lat': 3.139, 'country': '๐ฒ๐พ' }, { 'city': 'Johannesburg', 'lon': 28.047, 'lat': -26.204, 'country': '๐ฟ๐ฆ' }, { 'city': 'Cairo', 'lon': 31.236, 'lat': 30.044, 'country': '๐ช๐ฌ' }, { 'city': 'Yaoundรฉ', 'lon': 11.502, 'lat': 3.848, 'country': '๐จ๐ฒ' }, { 'city': 'Camberra', 'lon': 149.13, 'lat': -35.281, 'country': '๐ฆ๐บ' }] 

    def get_weather_info(self, longitude, latitude):
        """ Fetch weather data from 7timer.info. """
        req = requests.get(self.service_url, params={'lon': longitude, 'lat': latitude, 'product':'civillight', 'output':'json' })
        return req.json() if req.status_code < 300 else None

    def get_formatted_weather_info(self, city, days):
        """ Returns a markdown formatted text containing the city's weather information. """
        info = self.get_weather_info(longitude=city['lon'], latitude=city['lat'])
        if not info:
            return Message.get('weather.error_fetch').fulltext

        template = Message.get('weather.temperature_template').fulltext
        return '\n'.join(template.format(date=datetime.strptime(str(info['dataseries'][i]['date']), '%Y%M%d').strftime('%d/%M/%Y'),
                                         min=info['dataseries'][i]['temp2m']['min'],
                                         max=info['dataseries'][i]['temp2m']['max']) for i in range(days))

    def pick_random_city(self):
        """ Just pick up a random city from the 'sample_cities' list. """
        return self.sample_cities[random.randrange(len(self.sample_cities))]
