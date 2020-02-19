APP=markette
APP_TEST=markette-test

.PHONY: help build build-test clean lint remove start test
.SILENT: clean

help: ## This help
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-15s\033[0m %s\n", $$1, $$2}'

build: clean  ## Build the images
	docker-compose build ${APP}

build-test: clean  ## Build the images for testing
	docker-compose build ${APP_TEST}

clean:  ## Remove cached files and dirs from workspace
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.DS_Store" -delete

	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf htmlcov

	@echo "Cleaned workspace"

lint:  ## Run linting
	docker-compose run --rm ${APP_TEST} sh -c 'flake8 && isort --recursive --check-only --diff ${APP}'

remove:  ## Remove the containers
	docker container rm -fv ${APP} db || echo "Containers are removed"

start:  ## Start the containers
	docker-compose up -d ${APP}
	docker-compose logs -f ${APP} || echo "Exited container logs"

test:  ## Run tests
	docker-compose run --rm ${APP_TEST}
