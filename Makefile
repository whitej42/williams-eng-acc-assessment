.DEFAULT_GOAL := help

help:
	@echo "Williams Enginering Acceleration API"


run: # Run FastAPI locally
	python -m uvicorn api.main:app --reload


# Data Commands
run_pipeline: # Run DuckDB ETL Pipeline
	cd etl && python duckdb_pipeline.py

db_flush: