# The name of the executable. Defaults to the current directory name.
# https://stackoverflow.com/a/1371283
PROJECT_NAME=$(shell echo $${PWD\#\#*/})
bold=\033[1m
normal=\033[0m

.PHONY: help build build-test start remove lint test

help:
	@echo 'Makefile for ${PROJECT_NAME}      '
	@echo '                                  '
	@echo 'Usage:                            '
	@echo "  ${bold}build${normal}        Build the images"
	@echo "  ${bold}build-test${normal}   Build the images for testing"
	@echo "  ${bold}start${normal}        Start the containers"
	@echo "  ${bold}remove${normal}       Remove the containers"
	@echo "  ${bold}lint${normal}         Run linting"
	@echo "  ${bold}test${normal}         Run tests"

build:
	@echo 'Building images'
	docker-compose build markette

build-test:
	@echo 'Building images for testing'
	docker-compose build markette-test

start:
	@echo 'Starting containers'
	docker-compose up -d markette
	docker-compose logs -f markette

remove:
	@echo 'Removing containers'
	docker container rm -fv markette db

lint:
	@echo 'Running linting'
	docker-compose run --rm markette-test sh -c 'flake8 && isort --recursive --check-only --diff markette'
	docker container rm -fv db-test

test:
	@echo 'Running tests'
	docker-compose run --rm markette-test
	docker container rm -fv db-test

clean:
	@echo 'Cleaning workspace'
	;