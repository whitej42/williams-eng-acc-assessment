.DEFAULT_GOAL := help

help:
	@echo "Williams Enginering Acceleration API"

# Run Commands
run: # Run FastAPI locally
	uvicorn api.main:app --reload

up: # Run docker compose
	docker compose -f docker/docker-compose.yml up -d

down: # Stop docker compose
	docker compose -f docker/docker-compose.yml down

build: # Build docker compose
	docker compose -f docker/docker-compose.yml build

build_no_cache: # Build docker compose without cache
	docker compose -f docker/docker-compose.yml build --no-cache

build_api: # Build api docker image
	docker build -f api/docker/Dockerfile -t williams-eng-acc-api .

build_etl: # Build etl docker image
	docker build -f etl/docker/Dockerfile -t williams-eng-acc-etl .

# Data Commands
run_pipeline: # Run DuckDB ETL Pipeline
	cd etl && python duckdb_pipeline.py