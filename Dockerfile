FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev

COPY . /app/


EXPOSE 8000

WORKDIR /app/lowen_derape

CMD uv run python manage.py migrate && \
    uv run gunicorn lowen_derape.wsgi:application --bind 0.0.0.0:8000 --workers 3
