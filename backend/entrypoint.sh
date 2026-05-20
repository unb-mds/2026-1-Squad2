#!/bin/sh
set -e

echo "[entrypoint] Aplicando migrations..."
alembic upgrade head

echo "[entrypoint] Iniciando servidor..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload