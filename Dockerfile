FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN "curl -LsSf https://astral.sh/uv/install.sh | sh"
RUN "uv sync"
CMD ["uv", "run" "manage.py", "runserver", "0.0.0.0:8000"]
