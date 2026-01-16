#!/usr/bin/env bash
set -e

echo "Enforcing static invariants"
ruff check .

echo "Enforcing type invariants"
mypy backend--ignore-missing-imports

echo "Enforcing behavioral invariants"
pytest -v

echo "All invariants preserved"
