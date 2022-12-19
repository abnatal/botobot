# 🐬 BotoBot
BotoBot is an easy to configure menu-based chatbot for Whatsapp / Telegram.

It's composed by three python applications:
- BotoBot Core
- Telegram Client
- WhatsApp Client

Check the live demo at https://t.me/BotoBotDemo_bot

## Prerequisites
### For Telegram
You have to register a new bot at https://t.me/BotFather

Check the documentation at https://core.telegram.org/bots#6-botfather or watch a <a href='https://www.youtube.com/results?search_query=botfather' target='_blank'>tutorial video on youtube</a>.

### For WhatsApp
You need to setup an account with a Facebook Business Solution Provider (BSP) for Whatsapp. Currently, this project supports <a href='https://gupshup.io' target='_blank'>Gupshup</a> and <a href='https://www.positus.com.br'>Positus</a>.

## Project structure
<img src="https://abnatal.com/github/botobot_diagram.jpg"></img>
```
Project
├── core
|   ├── botobot_core: Flask application to handle the user input and call services APIs.
|
├── telegram
│   ├── botobot_telegram: Python application to interface with Telegram API.
|
├── whatsapp
│   ├── botobot_whatsapp: Flask application to interface with the Facebook BSP.
|
├── requirements.txt: List of modules dependecies.
```

## How to Build and Run
### Docker
Use the __docker-compose.yml__ provided.
```
# First, configure each application by editing its "settings.toml" file..
# Instructions about configuration are presented at the README.md files inside each project folder.
cd core
cp settings.toml.sample settings.toml
vi settings.toml

cd ../telegram
cp settings.toml.sample settings.toml
vi settings.toml

cd ../whatsapp
cp settings.toml.sample settings.toml
vi settings.toml

# Run with docker-compose:
cd ..
docker-compose up -d --build
```

### Running as standalone apps
Please check the README.md files inside each project folder (core, telegram, whatsapp) for instructions.

The WhatsApp and Telegram clients depend on the BotoBot Core project.

## Technologies used
- Python
- Flask RESTful
- SQLAlchemy

## Future tasks

- [ ] Admin Interface

## Why "boto"?
Boto is the <a href='https://marinemammalscience.org/facts/inia-geoffrensis'>amazon river dolphin</a>. One of their strongest skills is communication.
