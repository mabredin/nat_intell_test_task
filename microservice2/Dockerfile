FROM python:3.10-slim as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y curl git
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=$PATH:/etc/poetry/bin

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true
RUN poetry install --only main

FROM python:3.10-slim as app
WORKDIR /app
ENV PYTHONPATH=$PYTHONPATH:/app/src PATH=/app/.venv/bin:$PATH
COPY --from=builder /app/.venv .venv
COPY ./src ./src

CMD ["uvicorn", "main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
