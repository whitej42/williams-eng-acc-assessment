FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app/api

ENV PYTHONPATH=/app

## Development Stage ##
FROM base AS development

# Copy requirements and install
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir psycopg2==2.9.10

# Copy application code into /app/api so the 'api' package exists
COPY api/ /app/api
RUN chown -R appuser:appuser /app

USER appuser

# Expose application port
EXPOSE 8000

# Run application in development
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

## Production Stage ##
FROM base AS production

# Copy requirements and install
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into /app/api so the 'api' package exists
COPY api/ /app/api
RUN chown -R appuser:appuser /app

USER appuser

# Expose application port
EXPOSE 8000

# Run application in production
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]