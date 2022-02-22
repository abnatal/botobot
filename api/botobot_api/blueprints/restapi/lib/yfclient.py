import yfinance as yf
from botobot_api.models import Message

class YahooFinanceClient():
    """ Gets data from Yahoo! Finance. """

    @staticmethod
    def get_formatted_stock_info(ticker):
        stock = yf.Ticker(ticker.strip())
        if stock.info.get('currentPrice') is not None:
            return Message.get('stocks.result_template').fulltext.format(**stock.info)
        else:
            return Message.get('stocks.no_data_found').fulltext.format(ticker=ticker.strip().upper())
