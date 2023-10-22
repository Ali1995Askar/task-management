# pull official base image
FROM python:3.8-slim-buster

# set work directory
WORKDIR /usr/src/code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/code/
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/code

