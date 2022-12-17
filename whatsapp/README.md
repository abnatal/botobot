# 🐬 BotoBot WhatsApp Client
Interface between the BotoBot Core and the WhatsApp API.

Check the telegram live demo at https://t.me/BotoBotDemo_bot

## Prerequisites
You need to setup an account with a Facebook Business Solution Provider (BSP) for Whatsapp. Currently, this project supports [Gupshup](https://gupshup.io) and [Positus](https://www.positus.com.br).

## Project structure
```
Project
├── botobot_whatsapp
│   ├── blueprints: REST API resources (webhooks)
|   ├── ext: Extensions (configuration, database, commands)
|   ├── tests: Pytest tests
|   ├── app.py: Flask application
|   ├── requirements.txt: Modules dependecies.
```

## Dependencies
This project project depends on [BotoBot Core](https://github.com/abnatal/botobot/tree/main/core).

It was tested with Python 3.10.

## Configuration
Edit the __settings.toml__ and provide the following parameters:

### General
```
SECRET_KEY = "some_random_key"
WEBHOOK_TOKEN = 'please_change_this_to_a_random_string'
BOTOBOT_CORE_WEBHOOK = 'http://botobot_core:5000/'
```
The __SECRET_KEY__ is the Flask secret key. Please provide a random string.

The __WEBHOOK_TOKEN__ is a random string to be configured with your BSP (Gupshup or Positus)

The __BOTOBOT_CORE_WEBHOOK__ is the URL of the BotoBot Core Webhook. Please note that it points to the __botobot_core__ host, which is the default configuration for our docker-compose setup. If you want to run it as a standalone app, change this address (usually http://127.0.0.1:5000/ for development environments).

### Gupshup
```
GUPSHUP_WHATSAPP_PHONE = '999999999999'
GUPSHUP_APPNAME = 'your_appname_at_gupshup'
GUPSHUP_API_KEY = 'your_key_at_gupshup'
```
The __GUPSHUP_WHATSAPP_PHONE__ is your company phone configured at Gupshup. If your app isn't in production, GupShup provides you a proxy phone number.

The __GUPSHUP_APPNAME__ is your app name at Gupshup.

The __GUPSHUP_API_KEY__ is your api key at Gupshup.

### Positus

## How to run

### Install python dependencies
```
python -m pip install -r requirements.txt
```

### Run
It's mandatory to create the database before the first execution.

In the application directory, run:
```
flask create-db
```
To run the application:
```
flask run
```

### Docker
To run it as a docker container, check the [README.md](https://github.com/abnatal/botobot/tree/main/README.md) file in the parent directory.
