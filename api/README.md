# 🐬 BotoBot API
The core module of BotoBot. It's a Flask RESTful application that provides:
- An entry point (webhook) to receive messages from clients (eg. Telegram / Whatsapp);
- Services APIs (one endpoint for each option on the menu);
- Route messages between Clients and APIs.

This projects contains three sample services (Stock Prices, Weather and Static Texts).

New services must be implemented here, as new API resources.

## Project structure
```
Project
├── botobot_api
│   ├── blueprints: REST API resources
|   ├── ext: Extensions (configuration, database, commands and resources)
|   ├── tests: Pytest tests
|   ├── app.py: Flask application
|   ├── requirements.txt: Modules dependecies.
```

## Dependencies
This project was tested with Python 3.10.

## How to run

### Install python dependencies
```
python -m pip install -r requirements.txt
```

### Configuration
This application can run out of the box for debugging purposes. However, it's strongly recommended that you edit the __settings.toml__ and change the __SECRET_KEY__ parameter.

If you want to use a DBMS other than SQLite, please provide the connection string in the __SQLALCHEMY_DATABASE_URI__ parameter.

### Run
It's necessary to create the database before the first execution.

In the application directory, run:
```
flask create-db
```
To run the application:
```
flask run
```

### Docker Container
To run it as a docker container, use the __Dockerfile__ provided.

## Add new services to the bot
- Implement the new resource in the __blueprints\restapi__ directory;
- Add the corresponding record to __Api__ table (take a look in other records as an example);
- Edit the __RESTAPI_RESOURCES__ section in __settings.toml__ (include you new class).

# TODO
- [ ] Admin Interface