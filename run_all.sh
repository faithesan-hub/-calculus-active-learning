#!/usr/bin/env bash
# Runs the whole project from raw data to paper. Add --final after author verification.
set -euo pipefail
cd "$(dirname "$0")"
python3 code/01_fetch.py
python3 code/02_build.py
python3 code/03_analysis.py > /dev/null
python3 code/04_figures.py "$@"
python3 code/05_manuscript.py "$@"
python3 code/06_docs.py "$@"
