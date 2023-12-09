# docker build -t transia/cloudbuild-app .
FROM python:3.10.6-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y build-essential

WORKDIR /app

# Copy the pyproject.toml and poetry.lock (if exists) files into the container
COPY pyproject.toml poetry.lock* /app/

# Install Poetry in the container
RUN pip install --no-cache-dir poetry

# Configure Poetry to not create a virtual environment inside the Docker container
RUN poetry config virtualenvs.create false

# Install the project dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

COPY . /app

ARG API_ENV
ENV API_ENV=$API_ENV
ARG API_HOST
ENV API_HOST=$API_HOST
ARG API_PORT
ENV API_PORT=$API_PORT
ARG XRPL_WSS_ENDPOINT
ENV XRPL_WSS_ENDPOINT=$XRPL_WSS_ENDPOINT
ARG XAHAU_WSS_ENDPOINT
ENV XAHAU_WSS_ENDPOINT=$XAHAU_WSS_ENDPOINT

EXPOSE $API_PORT

CMD exec gunicorn --bind :$API_PORT --workers 4 server:app --timeout 3600
