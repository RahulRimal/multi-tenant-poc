FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY .env.dev .env
COPY . .

RUN chmod +x web-entrypoint.sh
RUN chmod +x celery-entrypoint.sh

