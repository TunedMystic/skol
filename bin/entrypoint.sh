#!/usr/bin/env bash

uvicorn markette.app:app --host 0.0.0.0 --port 8000 --reload
