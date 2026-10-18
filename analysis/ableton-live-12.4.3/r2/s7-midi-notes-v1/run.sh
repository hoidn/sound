#!/bin/sh
# Regenerate the S7 static outputs (read-only on the bundle). Usage: sh run.sh [bundle Contents dir]
set -e
B="${1:-/home/ollie/Ableton Live 12 Suite.app/Contents}"
cd "$(dirname "$0")"
python3 -I s7_static.py "$B" static-survey.json inputs-documents.tsv
