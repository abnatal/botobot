FROM python:3
LABEL maintainer="abnatal@gmail.com"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/
COPY ./ /app/

COPY docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/docker-entrypoint.sh"]
