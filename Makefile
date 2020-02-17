.PHONY: help build build-test clean lint remove start test
.SILENT: clean

help: ## This help
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Build the images
	docker-compose build markette

build-test:  ## Build the images for testing
	docker-compose build markette-test

clean:  ## Remove cached files and dirs from workspace
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.DS_Store" -delete

	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf htmlcov

lint:  ## Run linting
	docker-compose run --rm markette-test sh -c 'flake8 && isort --recursive --check-only --diff markette'
	docker container rm -fv db-test

remove:  ## Remove the containers
	docker container rm -fv markette db

start:  ## Start the containers
	docker-compose up -d markette
	docker-compose logs -f markette

test:  ## Run tests
	docker-compose run --rm markette-test
	docker container rm -fv db-test
