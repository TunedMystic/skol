#!/usr/bin/env bash

set -ev

BIN_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


# Migrate the database
sleep 2
migo --dsn $DATABASE_DSN migrate


# Set uvicorn args based on the environment.
UVICORN_ARGS='--reload --reload-dir=/usr/src/app'

if [ "$ENV" = "prod" ]; then
    UVICORN_ARGS='--workers 2'
fi

# Run the application
uvicorn --host 0.0.0.0 --port 8000 $UVICORN_ARGS app.main:app
