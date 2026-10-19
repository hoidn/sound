#!/bin/sh
# X2 notes and launch (extracted execution). Regenerates every file listed in manifest.json.
# Requires: gcc, gdb, objdump, python3; the x86_64 slice at XEXEC_SLICE (default in tools/xexec/xexec.py).
# Builds the loader copy xexec_x2.c to /var/tmp/sound-analysis/xexec-x2-notes-launch/xexec (outside the tree).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
python3 -I -B run_x2.py | tee summary.txt
python3 -I -B make_manifest.py
