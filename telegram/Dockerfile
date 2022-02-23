FROM python:3-slim
LABEL maintainer="abnatal@gmail.com"

WORKDIR /usr/src/app

RUN useradd -m botobot

COPY ./botobot_telegram/telegram_cli.py .
COPY requirements.txt .
COPY settings.toml .
RUN chown -R botobot .

USER botobot

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./telegram_cli.py" ]
