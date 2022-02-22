FROM python:3
LABEL maintainer="abnatal@gmail.com"

# Install OS packages.
RUN apt-get -qq update
RUN apt-get install --yes apache2 apache2-dev locales

# Copy the app.
WORKDIR /app
RUN chown www-data:www-data /app
COPY --chown=www-data:www-data ./ /app/

# Install Python packages.
RUN pip install --no-cache-dir -r requirements.txt

# Create the database.
ENV FLASK_APP=/app/botobot_api/app.py
RUN flask create-db

# Run.
EXPOSE 5000
CMD [ "mod_wsgi-express", "start-server", "/app/botobot_api/wsgi.py", "--user", "www-data", "--group", "www-data", "--host", "0.0.0.0", "--port", "5000", "--log-to-terminal" ]
