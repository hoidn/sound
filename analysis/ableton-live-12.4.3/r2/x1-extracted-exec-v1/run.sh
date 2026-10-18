#!/bin/sh
# X1 extracted-execution pilot. Regenerates every file listed in manifest.json.
# Requires: gcc, gdb, objdump, python3; the x86_64 slice at XEXEC_SLICE (default in tools/xexec/xexec.py).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
python3 -I -B run_pilot.py | tee summary.txt
python3 -I -B make_manifest.py
