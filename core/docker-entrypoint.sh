#!/bin/bash
cd /app
export FLASK_APP=./botobot_core/app.py
export ENV_FOR_DYNACONF=production

echo "Creating database..."
flask create-db

echo "Starting server...."
gunicorn botobot_core.wsgi:application --bind 0.0.0.0:5000
