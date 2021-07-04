FROM python:3.9-slim-buster

WORKDIR /bert

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y libpq-dev build-essential
RUN pip install --upgrade pip

# Flake8 test
RUN pip install flake8
COPY . .
RUN flake8 --ignore=E501,E402,F401 .

# install dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# copy project
COPY . .
