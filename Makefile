APP=skol
APP_TEST=skol-test

.PHONY: help
help:  ## This help
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: clean source.tar.gz  ## Build the images
	docker-compose build ${APP}
	$(MAKE) clean

.PHONY: build-test
build-test: clean source.tar.gz  ## Build the images for testing
	docker-compose build ${APP_TEST}
	$(MAKE) clean

.PHONY: clean
clean:  ## Remove cached files and dirs from workspace
	@echo "Cleaning workspace"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.DS_Store" -delete
	@rm -f .coverage coverage.xml
	@rm -rf .pytest_cache
	@rm -rf htmlcov
	@rm -f source.tar.gz

.PHONY: lint
lint:  ## Run linting
	docker-compose run --rm ${APP_TEST} sh -c 'flake8 && isort --recursive --check-only --diff app'

.PHONY: remove
remove:  ## Remove the containers
	docker container rm -fv ${APP} db || echo "Containers are removed"

source.tar.gz:  # Add project source to a tarball
	tar -cvzf source.tar.gz app bin sql tests setup.cfg

.PHONY: start
start:  ## Start the containers
	docker-compose up -d ${APP}
	docker-compose logs -f ${APP} || echo "Exited container logs"

.PHONY: test
test:  ## Run tests
	docker-compose run --rm ${APP_TEST} sh -c 'pytest -rx --cov-report xml --cov=app tests'
