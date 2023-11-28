FROM python:3.11-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

