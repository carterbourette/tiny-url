FROM python:3.8.3-alpine3.11 AS base

RUN apk add --upgrade \
    tzdata \
    && rm -rf /var/cache/apk/*

ENV TZ America/Toronto

# 
FROM base as builder

RUN mkdir /install

WORKDIR /install

RUN pip install pipenv

COPY Pipfile ./

RUN apk add \
    git \
    g++ \
    libffi-dev \
    libxml2 \
    unixodbc-dev \
    gcc \
    openssl-dev \
    && rm -rf /var/cache/apk/*

RUN pipenv install --system --skip-lock

#
#
FROM builder as dev

WORKDIR /usr/src/app

ENTRYPOINT [ "gunicorn" ] 
CMD ["--reload", "-w", "2", "--threads", "4", "--access-logfile", "-", "--worker-class", "gthread", "-b", "0.0.0.0:8000", "tinyurl.main" ]

#
#
FROM dev as prod

WORKDIR /usr/src/app
COPY tinyurl ./tinyurl

EXPOSE 8000

ENTRYPOINT [ "gunicorn" ] 
CMD ["-w", "2", "--threads", "4", "--access-logfile", "-", "--worker-class", "gthread", "-b", "0.0.0.0:8000", "tinyurl.main" ]