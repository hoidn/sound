#!/bin/sh
# X2 transport-state extracted execution. Regenerates every file listed in manifest.json except the scripts.
# Requires: gcc, gdb, objdump, python3; the x86_64 slice (XEXEC_SLICE) and the corpora under /var/tmp/sound-analysis.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
python3 -I -B run_x2.py
python3 -I -B make_manifest.py
