#!/bin/bash
cd /app
export FLASK_APP=./botobot_whatsapp/app.py
export ENV_FOR_DYNACONF=production

echo "Creating database..."
flask create-db

echo "Starting server...."
gunicorn botobot_whatsapp.wsgi:application --timeout 240 --workers 3 --bind 0.0.0.0:8500
