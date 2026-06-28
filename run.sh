#!/usr/bin/env bash
# Linux/macOS equivalent of run.ps1 — runs the full pipeline from data generation to dashboard output
set -euo pipefail
PYTHON="${PYTHON:-python}"
"$PYTHON" python/generate_data.py
"$PYTHON" python/run_pipeline.py
"$PYTHON" -m unittest discover -s tests -v
"$PYTHON" dbt/load_seeds.py
DBT="$(dirname "$PYTHON")/dbt"
if [ ! -x "$DBT" ]; then DBT="dbt"; fi
"$DBT" build --project-dir dbt --profiles-dir dbt --no-partial-parse
echo 'Built docs/index.html and artifacts/Baltic_Commerce_Analysis.xlsx'
