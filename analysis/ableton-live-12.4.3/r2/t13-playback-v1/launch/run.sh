#!/bin/sh
# T1.3 fork B (launch timing): regenerate the X run of the launch pre-delay and the derived launch-sample table.
# Requires gcc, python3 and the x86_64 Live slice (tools/xexec/xexec.py default path or XEXEC_SLICE).
# Builds xexec_t13.c to /var/tmp/sound-analysis/xexec-t13-launch/xexec (outside the tree).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
python3 -I -B run_launch.py > run_launch.txt
python3 -I -B samples.py > samples.txt
