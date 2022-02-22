from botobot_api.ext.database import db
from botobot_api.models import Message, Api

def create_db():
    """ Creates the database and required records. """
    db.create_all()
    data = [
        Message(key='general.hello', fulltext='Hello, my name is Boto! 🐬\nHow can I help you?'),
        Message(key='general.wrong_option', fulltext='Sorry, invalid choice!\nPlease, pick one of the numbers below:'),
        Message(key='general.request_error', fulltext='Sorry, something went wrong...\nTry again later.'),
        Message(key='general.bye', fulltext='Bye!'),
        Message(key='general.see_you', fulltext='If you need anything else, please just send me a *"hi"*. 👋'),
        Message(key='statictext.instructions', fulltext='This is the Botobot demo. 🐬\n\n\It contains three sample services: stock prices, weather and static texts (Instructions / About).\n\nPlease notice that you may experience a slight delay in the stock prices and weather services because they rely on external APIs.'),
        Message(key='statictext.about', fulltext='This project is under the GNU General Public License v3.0.\n\nCheck the source code at https://github.com/abnatal/botobot\n\nFeel free to contact me on abnatal@gmail.com'),
        Message(key='statictext.topic_not_found', fulltext='Topic not found!'),
        Message(key='stocks.inform_ticker', fulltext='Please, inform a stock ticker or *quit* to quit.\n\n(e.g. *AAPL*, *AMZN*, *KO*, *MSFT*, *PETR4.SA*, etc.)'),
        Message(key='stocks.inform_another_ticker', fulltext='You may inform another ticker or *quit* to quit.'),
        Message(key='stocks.no_data_found', fulltext='No data found for ticker *{ticker}!*'),
        Message(key='stocks.result_template', fulltext = '*{longName}*\n*🖥️ Sector:* {sector}\n*🌎 Country:* {country}\n*📈 Price:* {currentPrice:.2f} {currency}\n'),
        Message(key='weather.intro', fulltext='*Sample API: Weather (7timer.info)*\n\nCheck the temperature for two *random cities* for the next two days:\n'),
        Message(key='weather.result_template', fulltext = '{country} *{city}*\n{weather_info}'),
        Message(key='weather.temperature_template', fulltext = '{date}: *{min}ºC*  ~  *{max}ºC*'),
        Message(key='weather.error_fetch', fulltext='Error fetching data!'),
        Api(name='instructions', label='Instructions', url='http://127.0.0.1:5000/statictext/instructions', position=1),
        Api(name='stocks', label='Sample API: Stock Prices', url='http://127.0.0.1:5000/stocks', position=2),
        Api(name='weather', label='Sample API: Weather', url='http://127.0.0.1:5000/weather', position=3),
        Api(name='about', label='About', url='http://127.0.0.1:5000/statictext/about', position=4),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return

def drop_db():
    """ Drops the entire database """
    db.drop_all()

def init_app(app):
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))
