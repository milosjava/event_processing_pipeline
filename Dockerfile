FROM python:3.12.0b3-slim as base

FROM base as poetry

WORKDIR /tmp
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install --disable-pip-version-check --requirement=requirements.txt && \
    rm requirements.txt

COPY poetry.lock pyproject.toml ./
RUN poetry export --output=requirements.txt && \
    poetry export --dev --output=requirements-dev.txt

FROM base as dev

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/tmp \
    python3 -m pip install --disable-pip-version-check --requirement=/tmp/requirements.txt

FROM base as final

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/tmp \
    python3 -m pip install --disable-pip-version-check --requirement=/tmp/requirements-dev.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=event_collector_server.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]