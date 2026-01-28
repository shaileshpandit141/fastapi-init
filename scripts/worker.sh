#!/usr/bin/env bash

exec uv run celery -A celery_app:celery worker -l info
