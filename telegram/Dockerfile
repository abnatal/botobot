FROM python:3-slim
LABEL maintainer="abnatal@gmail.com"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY ./botobot_telegram/telegram_cli.py .
COPY settings.toml .

RUN useradd -m botobot
RUN chown -R botobot .

USER botobot
CMD [ "python", "./telegram_cli.py" ]
