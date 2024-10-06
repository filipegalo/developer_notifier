#! /usr/bin/env bash

export PYTHONPATH=$(pwd)

# Let the DB start
python app/pre_start.py

# Run migrations
alembic upgrade head

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000