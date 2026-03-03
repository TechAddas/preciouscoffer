#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PY="$ROOT_DIR/pc_venv/bin/python"
FIXTURE_PATH="$ROOT_DIR/backups/sqlite_to_postgres.json"

if [[ ! -x "$VENV_PY" ]]; then
  echo "Python not found at $VENV_PY"
  exit 1
fi

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "DATABASE_URL is not set."
  echo "Example: export DATABASE_URL='postgresql://user:pass@host:5432/dbname'"
  exit 1
fi

if [[ ! -f "$FIXTURE_PATH" ]]; then
  echo "Fixture not found at $FIXTURE_PATH"
  echo "Generate it with:"
  echo "$VENV_PY manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes --output backups/sqlite_to_postgres.json"
  exit 1
fi

echo "Running migrations on PostgreSQL..."
"$VENV_PY" "$ROOT_DIR/manage.py" migrate

echo "Loading fixture into PostgreSQL..."
"$VENV_PY" "$ROOT_DIR/manage.py" loaddata "$FIXTURE_PATH"

echo "Done. PostgreSQL now has your migrated data."
