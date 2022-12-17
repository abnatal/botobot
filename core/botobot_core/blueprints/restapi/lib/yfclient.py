import yfinance as yf
from botobot_core.models import Message

class YahooFinanceClient():
    """ Gets stock data from Yahoo! Finance. """

    @staticmethod
    def get_formatted_stock_info(ticker):
        stock = yf.Ticker(ticker.strip())
        if stock.info.get('currentPrice'):
            return Message.get('stocks.result_template').fulltext.format(**stock.info)

        return Message.get('stocks.no_data_found').fulltext.format(ticker=ticker.strip().upper())
