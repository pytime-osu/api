# BUILD DEPENDENCIES
ARG DISCOVERY_API_KEY
ARG DISCOVERY_SERVICE_URL
ARG DISCOVERY_COLLECTION_ID
ARG DISCOVERY_ENVIRONMENT_ID
ARG TWITCH_CLIENT_ID
ARG TWITCH_CLIENT_SECRET

FROM python:3.8-alpine as builder
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN set -ex \
    && apk update \
    && apk add --no-cache postgresql-libs linux-headers \
    && apk add --no-cache gcc musl-dev build-base python3-dev postgresql-dev  \
    && pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# copy project
COPY . /usr/src/app/

# FINAL IMAGE

# pull official base image
FROM python:3.8-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create env variables for application
ENV DISCOVERY_API_KEY=$DISCOVERY_API_KEY
ENV DISCOVERY_SERVICE_URL=$DISCOVERY_SERVICE_URL
ENV DISCOVERY_COLLECTION_ID=$DISCOVERY_COLLECTION_ID
ENV DISCOVERY_ENVIRONMENT_ID=$DISCOVERY_ENVIRONMENT_ID
ENV TWITCH_CLIENT_ID=$TWITCH_CLIENT_ID
ENV TWITCH_CLIENT_SECRET=$TWITCH_CLIENT_SECRET

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

EXPOSE 8000
CMD gunicorn pytime_api.wsgi:application --workers 2 --bind 0.0.0.0:8000