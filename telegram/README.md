# 🐬 BotoBot Telegram Client
Interface between the BotoBot Core API and the Telegram API.

Check the live demo at https://t.me/BotoBotDemo_bot

## Prerequisites
You need to register a new bot at https://t.me/BotFather

Check the documentation at https://core.telegram.org/bots#6-botfather or watch a <a href='https://www.youtube.com/results?search_query=botfather'>tutorial video on youtube</a>.

## Project structure
```
Project
├── botobot_telegram
│   ├── telegram_cli.py: Python application.
|   ├── settings.toml: Configuration file
|   ├── requirements.txt: Modules dependecies.
```

## Dependencies
This project project depends on [BotoBot Core](https://github.com/abnatal/botobot/tree/main/core).

Tested with Python 3.10.

## How to run
### Configuration
Edit the __settings.toml__ and provide the following parameters:
```
TELEGRAM_TOKEN = '9999999999:ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BOTOBOT_CORE_WEBHOOK = 'http://botobot_core:5000/'
```
The __TELEGRAM_TOKEN__ parameter is the access token of your telegram bot.

The __BOTOBOT_CORE_WEBHOOK__ is the URL of the BotoBot Core Webhook. Please note that it points to the __botobot_core__ host, which is the default configuration for our docker-compose setup. If you want to run it as a standalone app, change this address (usually http://127.0.0.1:5000/ for development environments).

### Install python dependencies
```
python -m pip install -r requirements.txt
```

### Run
```
python botobot_telegram\telegram_cli.py
```
Application running, you can talk to your bot.

### Docker
To run it as a docker container, check the [README.md](https://github.com/abnatal/botobot/tree/main/README.md) file in the parent directory.
