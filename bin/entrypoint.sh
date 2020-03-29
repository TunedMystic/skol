#!/usr/bin/env bash

set -ev

BIN_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


# Migrate the database
migo --dsn $DATABASE_DSN wait
migo --dsn $DATABASE_DSN --dir sql/migrations migrate


# Set uvicorn args based on the environment.
UVICORN_ARGS='--reload --reload-dir=/usr/src/app'

if [ "$ENV" = "prod" ]; then
    UVICORN_ARGS='--workers 2'
fi

# Run the application
uvicorn --host 0.0.0.0 --port 8000 --no-access-log $UVICORN_ARGS app.main:app
