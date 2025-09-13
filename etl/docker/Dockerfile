FROM python:3.12-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY etl/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL pipeline code
COPY etl/ ./etl/

# Set working directory to ETL folder
WORKDIR /app/etl

# Create data directories if they don't exist
RUN mkdir -p ../data/raw ../data/final

# Make the pipeline executable
RUN chmod +x duckdb_pipeline.py

# Default command to run the pipeline
CMD ["python", "duckdb_pipeline.py"]