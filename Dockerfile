FROM python:3.8-slim

WORKDIR /app
COPY . /app

ARG VERSION
ENV APP_VERSION=$VERSION

RUN apt-get update && apt-get install -y gcc vim postgresql-client

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
