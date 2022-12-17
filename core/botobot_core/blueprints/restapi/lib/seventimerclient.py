from datetime import datetime
import random, requests
from botobot_core.models import Message

class SevenTimerClient():
    """ DEMO: client for the 7timer.info API. """

    def __init__(self):
        self.service_url = 'https://www.7timer.info/bin/api.pl'
        self.sample_cities = [{ 'city' : 'Belém', 'lon': -48.501, 'lat': -1.456, 'country': '🇧🇷' },
                              { 'city': 'Portel', 'lon': -50.817, 'lat': -1.937, 'country': '🇧🇷' },
                              { 'city': 'Buenos Aires', 'lon': -58.382, 'lat': -34.604, 'country': '🇦🇷' },
                              { 'city': 'La Paz', 'lon': -68.119, 'lat': -16.49, 'country': '🇧🇴' },
                              { 'city': 'Caracas', 'lon': -66.904, 'lat': 10.481, 'country': '🇨🇴' },
                              { 'city': 'Santiago', 'lon': -70.669, 'lat': -33.449, 'country': '🇨🇱' },
                              { 'city': 'San Francisco', 'lon': -122.419, 'lat': 37.775, 'country': '🇺🇸' },
                              { 'city': 'Chicago', 'lon': -87.63, 'lat': 41.878, 'country': '🇺🇸' },
                              { 'city': 'London', 'lon': -0.128, 'lat': 51.507, 'country': '🏴󠁧󠁢󠁥󠁮󠁧󠁿' },
                              { 'city': 'Amsterdan', 'lon': 4.904, 'lat': 52.368, 'country': '🇳🇱' },
                              { 'city': 'Berlin', 'lon': 13.405, 'lat': 52.52, 'country': '🇩🇪' },
                              { 'city': 'Paris', 'lon': 2.352, 'lat': 48.857, 'country': '🇫🇷' },
                              { 'city': 'Brussels', 'lon': 4.357, 'lat': 50.848, 'country': '🇧🇪' },
                              { 'city': 'Dublin', 'lon': -6.26, 'lat': 53.35, 'country': '🇮🇪' },
                              { 'city': 'Tokyo', 'lon': 139.769, 'lat': 35.68, 'country': '🇯🇵' },
                              { 'city': 'Bangkok', 'lon': 100.502, 'lat': 13.756, 'country': '🇹🇭' },
                              { 'city': 'Singapore', 'lon': 103.82, 'lat': 1.352, 'country': '🇸🇬' },
                              { 'city': 'Beijing', 'lon': 116.407, 'lat': 39.904, 'country': '🇨🇳' },
                              { 'city': 'Kuala Lumpur', 'lon': 101.687, 'lat': 3.139, 'country': '🇲🇾' },
                              { 'city': 'Johannesburg', 'lon': 28.047, 'lat': -26.204, 'country': '🇿🇦' },
                              { 'city': 'Cairo', 'lon': 31.236, 'lat': 30.044, 'country': '🇪🇬' },
                              { 'city': 'Yaoundé', 'lon': 11.502, 'lat': 3.848, 'country': '🇨🇲' },
                              { 'city': 'Camberra', 'lon': 149.13, 'lat': -35.281, 'country': '🇦🇺' }] 

    def get_weather_info(self, longitude, latitude):
        """ Fetch weather data from 7timer.info. """
        req = requests.get(self.service_url, params={'lon': longitude,
                                                     'lat': latitude,
                                                     'product':'civillight',
                                                     'output':'json' })
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
        """ Picks up a random city from the 'sample_cities' list. """
        return self.sample_cities[random.randrange(len(self.sample_cities))]
