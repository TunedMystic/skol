#!/usr/bin/env bash

GR='\033[0;32m'  # Green
NC='\033[0m'     # No color

ARGS=("$@")


# -------------------------------------------------------------------
# Main entrypoint
# -------------------------------------------------------------------

case ${ARGS[0]} in
    build)
        docker-compose build markette
        ;;
    build-test)
        docker-compose build markette-test
        ;;
    start)
        docker-compose up -d markette && \
        docker-compose logs -f markette
        ;;
    remove)
        docker container rm -fv markette db
        ;;
    lint)
        docker-compose run --rm markette-test sh -c "./bin/lint" && \
        docker container rm -fv db-test
        ;;
    test)
        docker-compose run --rm markette-test && \
        docker container rm -fv db-test
        ;;
esac
