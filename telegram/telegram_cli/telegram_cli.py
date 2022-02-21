from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ParseMode, error
import os, sys, requests, logging

class BotoBotTelegramClient:
    ERROR_MESSAGE = 'Sorry, an error occurred while processing your request. Please, try again later.'
    ERROR_TELEGRAM_UNAUTHORIZED = 'Authorization error! Check the "TELEGRAM_TOKEN" variable.'

    def __init__(self):
        self.load_config()
        self.req_headers = { 'Content-Type': 'application/json' }

    def load_config(self):
        self.config = {}
        for p in ['TELEGRAM_TOKEN', 'BOTOBOT_WEBHOOK']:
            self.config[p] = os.environ.get(p)
            if self.config[p] is None:
                raise Exception('ERROR: variable not found: {}.'.format(p))

    def start(self, update, context):
        json_data = {'chat_id' : update.effective_chat.id, 'cmd' : 'start', 'client':'telegram', 'version':'1.0'}
        try:
            req = requests.Session().post(self.config['BOTOBOT_WEBHOOK'], json = json_data, headers = self.req_headers)
            if req.status_code >= 300:
                raise Exception(f'HTTP ERROR {req.status_code}! Content: {req.text}')

            response = req.json()
            for message in response['messages']:
                context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.ERROR_MESSAGE, parse_mode=ParseMode.MARKDOWN)
            raise

    def on_message(self, update, context):
        message = update.message.text.strip()
        json_data = {'chat_id' : update.effective_chat.id, 'message' : message, 'client':'telegram', 'version':'1.0'}
        try:
            req = requests.Session().post(self.config['BOTOBOT_WEBHOOK'], json = json_data, headers = self.req_headers)
            if req.status_code >= 300:
                raise Exception(f'HTTP ERROR {req.status_code} na requisição! Content: {req.text}')

            response = req.json()
            for message in response.get('messages'):
                logging.debug(f'message={message}')
                context.bot.send_message(chat_id=update.effective_chat.id, text=message[:4095], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.ERROR_MESSAGE, parse_mode=ParseMode.MARKDOWN)
            raise

    def main(self):
        updater = Updater(token=self.config['TELEGRAM_TOKEN'], use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.on_message))
        try:
            updater.start_polling()
            updater.idle()
        except error.Unauthorized:
            logging.exception(self.ERROR_TELEGRAM_UNAUTHORIZED)
            raise

if __name__ == '__main__':
    logging.basicConfig(filename='telegram_cli.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s %(name)s] %(levelname)s: %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info("Starting telegram client...")

    BotoBotTelegramClient().main()
