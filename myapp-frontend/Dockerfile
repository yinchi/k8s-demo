# syntax=docker/dockerfile:1.7-labs

# CONTEXT: ..

FROM python:3.12-slim AS builder
RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install gcc

RUN mkdir -p /app/myapp-models /app/myapp-frontend

COPY /myapp-models /app/myapp-models

COPY /myapp-frontend/pyproject.toml /myapp-frontend/README.md /app/myapp-frontend/
RUN cd /app/myapp-frontend && poetry install --no-interaction --no-ansi --no-root --without dev

###

FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="My App: REST API"
LABEL org.opencontainers.image.source https://github.com/yinchi/k8s-db-test
LABEL org.opencontainers.image.authors "Yin-Chi Chan <ycc39@cam.ac.uk>"

ENV PATH="/app/myapp-frontend/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY --from=builder /app/ /app
COPY --exclude=*.venv* /myapp-frontend/ /app/myapp-frontend

WORKDIR /app/myapp-frontend
CMD python -m myapp_frontend.main