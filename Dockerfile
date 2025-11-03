# Base image
FROM python:3.12-slim
# Environment
ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set workdir
WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN uv sync

# Copy project
COPY . /app/

# Collect static files (optional)
RUN uv run python manage.py collectstatic --noinput || true
RUN uv run python manage.py migrate

# Expose port
EXPOSE 8000
WORKDIR /app/lowen_derape
# Start Gunicorn via uv
CMD ["uv", "run", "gunicorn", "lowen_derape.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
