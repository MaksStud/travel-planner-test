FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update; \
    apt-get install -y gettext;

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
