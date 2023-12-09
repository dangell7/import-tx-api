# docker build -t transia/cloudbuild-app .
FROM python:3.10.6-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y build-essential

COPY ./deps/*.whl ./
RUN pip install *.whl && rm -rf *.whl

COPY ./*.whl ./
RUN pip install *.whl && rm -rf *.whl

ARG API_ENV
ENV API_ENV=$API_ENV
ARG API_PORT
ENV API_PORT=$API_PORT

EXPOSE $API_PORT

CMD exec gunicorn --bind :$API_PORT --workers 4 server:app --timeout 3600
