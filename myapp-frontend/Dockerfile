FROM python:3.12-slim AS builder
RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y install gcc
RUN mkdir /app
COPY pyproject.toml /app/

RUN cd /app && poetry install --no-interaction --no-ansi --no-root --without dev

###

FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="My App: REST API"
LABEL org.opencontainers.image.source https://github.com/yinchi/k8s-db-test
LABEL org.opencontainers.image.authors "Yin-Chi Chan <ycc39@cam.ac.uk>"

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=builder /app .
COPY /myapp_frontend ./myapp_frontend

ENV DEBUG_DASH=0
CMD python -m myapp_frontend.main