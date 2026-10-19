#!/bin/sh
# Regenerate the Tension evidence (about 3 minutes). Needs gcc, python3 with numpy and scipy, objdump,
# and the app bundle at /home/ollie/Ableton Live 12 Suite.app. The loader is built to
# /var/tmp/sound-analysis/t12-tension/xdev (XDEV_BIN overrides).
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
python3 -I -B tension.py
python3 -I -B fit.py
python3 -I -B run_tension.py
python3 -I -B analyze_tension.py > results/analyze.txt 2> /dev/null
python3 -I -B checks_tension.py > results/checks.txt 2> /dev/null
python3 -I -B sensitivity.py > results/sensitivity.txt 2> /dev/null
python3 -I -B fma_scan.py "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Tension.bundle/Contents/MacOS/Tension" > results/fma_scan.txt
python3 -I -B make_manifest.py
