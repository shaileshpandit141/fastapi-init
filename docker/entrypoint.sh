#!/bin/bash
set -e

if [ "$SERVICE" = "api" ]; then
  exec uv run uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4
fi

if [ "$SERVICE" = "worker" ]; then
  exec uv run celery -A celery_app:celery worker \
    --loglevel=info \
    --concurrency=4
fi
