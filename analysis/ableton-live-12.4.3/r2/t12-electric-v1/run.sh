#!/bin/sh
# Regenerate the SPEC-DEVICE-ELECTRIC evidence (about one minute on 8 cores). Needs gcc, objdump,
# python3 with numpy and scipy, and the app bundle at /home/ollie/Ableton Live 12 Suite.app.
# The loader is built to /var/tmp/sound-analysis/t12-electric/xdev (XDEV_BIN overrides); scratch
# renders go to /var/tmp/sound-analysis/t12-electric/.
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python3 -I fit.py
python3 -I measure.py
python3 -I run_cases.py > results/run_cases.txt
python3 -I probes_events.py > results/probes_events.txt
python3 -I probes_params.py > results/probes_params.txt
python3 -I fma_scan.py "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Electric.bundle/Contents/MacOS/Electric" > results/fma_scan.txt
python3 -I make_manifest.py
