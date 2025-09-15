# Colours
GREEN=\033[0;32m
YELLOW = \033[1;33m
NC=\033[0m

.DEFAULT_GOAL := help

help:	## Show this help.
	@echo "╔═══════════════════════════════════════════╗"
	@echo "║             Williams Race API             ║"
	@echo "╚═══════════════════════════════════════════╝"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf " $(YELLOW)%-15s $(NC)%s\n", $$1, $$2}'

# Local run commands
run_local:  ## Run FastAPI Locally
	uvicorn api.main:app --reload

run_local_alt: # Run on alternative port to Docker
	uvicorn api.main:app --reload --port 8080

# Data Commands
run_pipeline: ## Run DuckDB ETL Pipeline Script
	cd etl && python3 duckdb_pipeline.py

# Docker commands
up: ## Run docker compose
	docker compose -f docker/docker-compose.yml up -d
	@echo "$(GREEN)Services started$(NC)"

down: ## Stop docker compose
	docker compose -f docker/docker-compose.yml down
	@echo "$(GREEN)Services stopped!$(NC)"

build: ## Build docker compose
	docker compose -f docker/docker-compose.yml build
	@echo "$(GREEN)Docker compose built$(NC)"

build_no_cache: ## Build docker compose without cache
	docker compose -f docker/docker-compose.yml build --no-cache
	@echo "$(GREEN)Docker compose built without cache$(NC)"

build_api: ## Build api docker image
	docker build -f api/docker/Dockerfile -t williams-eng-acc-api .
	@echo "$(GREEN)API docker image built!$(NC)"

build_etl: ## Build etl docker image
	docker build -f etl/docker/Dockerfile -t williams-eng-acc-etl .	
	@echo "$(GREEN)ETL docker image built$(NC)"

restart_etl: ## Rerun ETL process inside Docker
	docker compose -f docker/docker-compose.yml restart etl

# Logs
logs: ## View docker compose logs
	docker compose -f docker/docker-compose.yml logs -f

logs_api: ## View api logs
	docker compose -f docker/docker-compose.yml logs api

logs_etl: ## View etl logs
	docker compose -f docker/docker-compose.yml logs etl

logs_postgres: ## View postgres logs
	docker compose -f docker/docker-compose.yml logs postgres
