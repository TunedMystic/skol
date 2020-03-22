#!/usr/bin/env bash

set -ev

BIN_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Migrate the database
export DSN="$DATABASE_DSN?sslmode=disable"
dbmate -env DSN wait
dbmate -env DSN --migrations-dir=/usr/src/sql/migrations migrate
