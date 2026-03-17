FROM python:3.10-slim AS base

# --- Environment setup ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# --- Install dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

# --- Source code ---
COPY src/ /app/src/

# --- Standard entrypoint ---
CMD ["python", "-m", "src.coordinator"]
