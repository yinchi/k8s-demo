# syntax=docker/dockerfile:1.7-labs

# CONTEXT: ..
FROM python:3.12-slim AS builder
RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install gcc

COPY /frontend-common /app/frontend-common

COPY /frontend-main/pyproject.toml /frontend-main/README.md /app/frontend-main/
RUN cd /app/frontend-main && poetry install --no-interaction --no-ansi --no-root --without dev

###

FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="My App: Frontend main page"
LABEL org.opencontainers.image.source https://github.com/yinchi/k8s-db-test
LABEL org.opencontainers.image.authors "Yin-Chi Chan <ycc39@cam.ac.uk>"

ENV PATH="/app/frontend-main/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8050

COPY --from=builder /app/ /app
COPY --exclude=*.venv* /frontend-main /app/frontend-main

WORKDIR /app/frontend-main/frontend_main
CMD gunicorn -w 1 -b 0.0.0.0:8050 main:server