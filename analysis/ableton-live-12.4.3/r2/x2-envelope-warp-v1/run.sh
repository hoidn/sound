#!/bin/sh
# X2 extracted-execution: envelope evaluation and warp mapping. Regenerates results/, raw/, imports.txt.
# Requires gcc, gdb, objdump, python3; the x86_64 slice (tools/xexec/xexec.py SLICE). The X2 loader copy
# (xexec2.c) is built to $X2_BIN (default /var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
export X2_BIN="${X2_BIN:-/var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2}"
python3 -I -B run_x2.py > summary.txt
python3 -I -B check_rules.py >> summary.txt
python3 -I -B make_manifest.py
