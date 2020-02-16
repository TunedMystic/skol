#!/usr/bin/env bash

GR='\033[0;32m'  # Green
NC='\033[0m'     # No color

ARGS=("$@")


# -------------------------------------------------------------------
# Main entrypoint
# -------------------------------------------------------------------

case ${ARGS[0]} in
    db)
        docker run -d -p 5432:5432 --name db postgres:11-alpine
        ;;
    start)
        uvicorn markette.app:app --reload
        ;;
    test)
        ENV=test pytest tests
        ;;
esac
