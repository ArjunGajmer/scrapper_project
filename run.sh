#!/bin/bash

echo "Running Daemon"
python schedular.py &

echo "Starting FastAPI server..."
uvicorn app.main:app --reload &

echo "Starting Celery worker..."
celery -A app.celery_app worker --loglevel=info &

wait
