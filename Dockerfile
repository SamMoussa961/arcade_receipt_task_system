FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-cache

COPY . /app

RUN mkdir -p /app/data

CMD ["/app/.venv/bin/uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
