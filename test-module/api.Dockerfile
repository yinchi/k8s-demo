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

COPY /test-module/pyproject.toml /test-module/README.md /app/test-module/
RUN cd /app/test-module && poetry install --no-interaction --no-ansi --no-root --without dev --without frontend

###

FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="My App: Test module API"
LABEL org.opencontainers.image.source https://github.com/yinchi/k8s-db-test
LABEL org.opencontainers.image.authors "Yin-Chi Chan <ycc39@cam.ac.uk>"

ENV PATH="/app/test-module/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install curl

COPY --from=builder /app/ /app
COPY --exclude=*.venv* /test-module /app/test-module

WORKDIR /app/test-module/test_module
CMD fastapi run --host 0.0.0.0  --workers 1 ./api.py --root-path=/test-module/api