#!/usr/bin/env bash
set -e

export $(grep -v '^#' .env | xargs)

CELERY_APP="celery_app:celery"
LOG_LEVEL="DEBUG"
QUEUE=${CELERY_QUEUE:-default}

echo "Starting Celery Worker"
echo "Queue: $QUEUE"

exec uv run celery -A "$CELERY_APP" worker \
  --loglevel="$LOG_LEVEL" \
  --queues="$QUEUE" \
  --concurrency=1 \
  --pool=solo
