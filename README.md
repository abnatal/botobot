# 🐬 BotoBot
BotoBot is an easy to configure menu-based chatbot for Whatsapp / Telegram.

It's composed by three python applications:
- API
- Telegram Client
- WhatsApp Client

You can see the live demo at https://t.me/BotoBotDemo_bot

## Prerequisites
### For telegram
You have to register a new bot at https://t.me/BotFather

Check the documentation at https://core.telegram.org/bots#6-botfather or watch a <a href='https://www.youtube.com/results?search_query=botfather' target='_blank'>tutorial video on youtube</a>.

### For WhatsApp
You need to setup an account with a Facebook Business Solution Providers (BSP) for Whatsapp. Currently, this project supports <a href='https://gupshup.io' target='_blank'>Gupshup</a> and <a href='https://www.positus.com.br'>Positus</a>.

## Project structure
<img src="https://abnatal.com/github/botobot_diagram.jpg"></img>
```
Project
├── api
|   ├── botobot_api: Flask application to handle the user input and execute services APIs.
|
├── telegram
│   ├── telegram_cli: Python application to interface with Telegram API.
|
├── whatsapp
│   ├── whatsapp_cli: Flask application to interface with the Facebook BSP.
|
├── requirements.txt: List of modules dependecies.
```

## How to build and run
Check the README.md files inside each project folder (api, telegram, whatsapp) for instructions.

The WhatsApp Client  (./whatsapp) and Telegram Client (./telegram) depend on the API project (./api).

## Technologies used
- Python
- Flask RESTful
- SQLAlchemy

## Future tasks

- [ ] Admin Interface
