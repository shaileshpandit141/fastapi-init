#!/usr/bin/env bash
set -e

# Load env vars
export $(grep -v '^#' .env | xargs)

APP="main:app"
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8000}

echo "Starting FastAPI Init app"
echo "Reload enabled"

exec uv run uvicorn "$APP" \
  --host "$HOST" \
  --port "$PORT" \
  --reload \
