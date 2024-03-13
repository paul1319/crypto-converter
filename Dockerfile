FROM python:3.10 AS base

RUN apt-get update && apt-get upgrade -y

# Poetry
ENV POETRY_VERSION=1.8 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME=/opt/poetry

RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install install poetry==${POETRY_VERSION}
RUN ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry

# Packages
COPY ./poetry.lock ./pyproject.toml /usr/src/app/
WORKDIR /usr/src/app/
RUN poetry install --no-dev --no-root --no-interaction

# Run
FROM base AS prod
COPY . /usr/src/app/

FROM base AS dev
RUN poetry install --no-root --no-interaction
COPY . /usr/src/app/

