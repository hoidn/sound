#!/bin/sh
# X2 MIDI: extracted execution of the x86_64 MIDI-mapping chain. Regenerates every file listed in manifest.json.
# Requires: gcc, gdb, objdump, python3; the x86_64 slice at XEXEC_SLICE (default in tools/xexec/xexec.py).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
python3 -I -B run_x2.py | tee summary.txt
python3 -I -B static_e15.py
python3 -I -B make_manifest.py
