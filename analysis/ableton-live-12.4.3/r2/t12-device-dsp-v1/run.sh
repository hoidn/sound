#!/bin/sh
# Regenerate the T1.2 feasibility evidence (about 3 minutes). Needs gcc, python3 with numpy and
# scipy, node, objdump, and the app bundle at /home/ollie/Ableton Live 12 Suite.app.
# The loader is built to /var/tmp/sound-analysis/t12-xdev/xdev (XDEV_BIN overrides).
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
python3 -I model.py
python3 -I fit.py
python3 -I run_corpus.py
python3 -I analyze_corpus.py > results/analyze_corpus.txt
python3 -I run_analog.py > results/run_analog.txt
python3 -I libm_sensitivity.py > results/libm_sensitivity.txt
python3 -I probe_others.py > /dev/null
D="/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac"
{ echo "== Corpus"; python3 -I fma_scan.py "$D/Corpus.bundle/Contents/MacOS/Corpus" 0x1f3f8 0x23670 0x1dfec 0x271cc 0x26a5c 0x27040 0x1d1b4 0x2764c
  echo "== Analog"; python3 -I fma_scan.py "$D/Analog.bundle/Contents/MacOS/Analog"; } > results/fma_scan.txt
python3 -I make_manifest.py
