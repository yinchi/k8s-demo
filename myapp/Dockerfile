FROM python:3.12-slim as builder
RUN pip install poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt dist-upgrade -y && apt install -y gcc

WORKDIR /app
COPY pyproject.toml .
RUN poetry install --no-interaction --no-ansi --no-root --without dev

######

FROM python:3.12-slim as runtime

LABEL org.opencontainers.image.title="My App"
LABEL org.opencontainers.image.description="\
Demo app for testing Kubernetes deployment. The app contains \
a database service installed via Helm, and a webapp container \
containing both a FastAPI backend and a Plotly Dash frontend."
# LABEL org.opencontainers.image.source https://github.com/yinchi/k8s-db-test/
LABEL org.opencontainers.image.authors="Yin-Chi Chan <ycc39@cam.ac.uk>"

RUN apt update && apt dist-upgrade -y && apt install -y net-tools iputils-ping

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=builder /app/ ./
COPY .env .env.secret .
COPY myapp/ ./myapp/

CMD uvicorn myapp.main:app --host "0.0.0.0" --port 80 --workers 1
