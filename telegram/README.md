# 🐬 BotoBot Telegram Client
Interface between the BotoBot API and the Telegram API.

Check the live demo at https://t.me/BotoBotDemo_bot

## Prerequisites
You need to register a new bot at https://t.me/BotFather

Check the documentation at https://core.telegram.org/bots#6-botfather or watch a <a href='https://www.youtube.com/results?search_query=botfather'>tutorial video on youtube</a>.

## Project structure
```
Project
├── telegram_cli
│   ├── telegram_cli.py: Python application.
|   ├── settings.toml: Configuration file
|   ├── requirements.txt: Modules dependecies.
```

## Dependencies
This project project depends on [BotoBot API](https://github.com/abnatal/botobot/tree/main/api).

It was tested with Python 3.10.

## How to run
### Configuration
Edit the __settings.toml__ and provide the following parameters:
```
TELEGRAM_TOKEN = '9999999999:ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BOTOBOT_API_WEBHOOK = 'http://botobot_api:5000/'
```
The __TELEGRAM_TOKEN__ parameter is the access token of your telegram bot.

The __BOTOBOT_API_WEBHOOK__ is the URL of the BotoBot API. Please notice that it points to the __botobot_api__ host, which is the default configuration for our docker-compose setup. If you want to run it as a standalone app, change this address (usually "http://127.0.0.1:5000/" for development environments).

### Install python dependencies
```
python -m pip install -r requirements.txt
```

### Run
```
python telegram_cli\telegram_cli.py
```
Application running, you can talk to your bot.

### Docker
To run it as a docker container, check the [README.md](https://github.com/abnatal/botobot/tree/main/README.md) file in the parent directory.
