#!/usr/bin/env bash

# Run the application with uvicorn.
if [ "$ENV" = "dev" ]; then
    uvicorn --host 0.0.0.0 --port 8000 --reload --reload-dir=/app/markette markette.app:app
else
    uvicorn --host 0.0.0.0 --port 8000 --workers 2 markette.app:app
fi
