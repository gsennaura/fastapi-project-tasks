.PHONY: help setup up down restart logs test clean migrate format lint dev health

.DEFAULT_GOAL := help

DOCKER_COMPOSE = docker compose
APP_CONTAINER = fastapi-app
DB_CONTAINER = fastapi-postgres

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Build images and prepare environment
	@echo "Setting up development environment..."
	$(DOCKER_COMPOSE) build --no-cache
	@echo "Environment prepared. Use 'make up' to start services."

up: ## Start services and run migrations
	@echo "Starting services..."
	$(DOCKER_COMPOSE) up -d
	@$(MAKE) wait-healthy
	@$(MAKE) migrate
	@$(MAKE) health
	@echo "Services running at http://localhost:8000"

down: ## Stop services
	$(DOCKER_COMPOSE) down

restart: ## Restart services
	@$(MAKE) down
	@$(MAKE) up

dev: ## Start with development tools (includes pgadmin)
	$(DOCKER_COMPOSE) --profile dev up -d
	@$(MAKE) wait-healthy
	@$(MAKE) migrate
	@echo "Development environment running (includes PgAdmin at :5050)"

logs: ## Show app logs
	$(DOCKER_COMPOSE) logs -f $(APP_CONTAINER)

logs-db: ## Show db logs
	$(DOCKER_COMPOSE) logs -f $(DB_CONTAINER)

logs-all: ## Show all logs
	$(DOCKER_COMPOSE) logs -f

health: ## Check if API is running
	@echo "Checking API health..."
	@curl -sf http://localhost:8000/health > /dev/null && echo "API is healthy" || echo "API is not responding"

wait-healthy: ## Wait for services to start
	@echo "Waiting for services to be healthy..."
	@timeout 60 bash -c 'until $(DOCKER_COMPOSE) ps | grep -q "(healthy)"; do sleep 2; done' || (echo "Services failed to become healthy" && exit 1)

migrate: ## Run migrations
	@echo "Running database migrations..."
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) alembic upgrade head

migration: ## Create migration (use: make migration MESSAGE="description")
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) alembic revision --autogenerate -m "$(MESSAGE)"

rollback: ## Rollback migration
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) alembic downgrade -1

test: ## Run all tests
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) pytest tests/test_simple.py tests/test_integration_simple.py tests/test_main.py tests/unit/ -v

test-unit: ## Run unit tests only
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) pytest tests/unit/ -v

test-integration: ## Run integration tests only
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) pytest tests/test_simple.py tests/test_integration_simple.py tests/test_main.py -v

test-coverage: ## Run tests with coverage
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) pytest --cov=app --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) pytest --tb=short -q --disable-warnings -x

format: ## Format code with Black
	@echo "🎨 Formatting code..."
	@which black > /dev/null || (echo "❌ Black not installed. Run: pip install black" && exit 1)
	black app/ tests/

lint: ## Run all linting checks
	@echo "🔍 Running linting checks..."
	@which black > /dev/null || (echo "❌ Black not installed. Run: pip install black ruff mypy" && exit 1)
	black --check app/ tests/
	ruff check app/ tests/
	mypy app/ --ignore-missing-imports

security: ## Run security checks
	@echo "🔒 Running security checks..."
	@which bandit > /dev/null || (echo "❌ Security tools not installed. Run: pip install bandit safety" && exit 1)
	bandit -r app/ -f json
	safety check

install-dev: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	@echo "✅ Development tools installed!"
	@echo "💡 Now you can use: make format, make lint, make security"

security: ## Security scan
	$(DOCKER_COMPOSE) exec $(APP_CONTAINER) bandit -r app/

clean: ## Remove containers and volumes
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f

clean-all: ## Remove everything
	$(DOCKER_COMPOSE) down -v --remove-orphans --rmi all
	docker system prune -af

status: ## Show status
	$(DOCKER_COMPOSE) ps

first-run: ## First-time setup
	@echo "First-time setup for new developers..."
	@$(MAKE) setup
	@$(MAKE) up
	@echo "Project is ready! Open http://localhost:8000/docs"
