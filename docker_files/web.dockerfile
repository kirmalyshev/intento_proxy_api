FROM python:3.7.9-slim
MAINTAINER Kirill Malyshev "kirill.malyshe@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN pip install pip -U
RUN pip install -r requirements.txt

ENV HOME_DIR=/intento_api_proxy
RUN rm -rf $HOME_DIR
RUN mkdir $HOME_DIR
COPY . $HOME_DIR
WORKDIR $HOME_DIR