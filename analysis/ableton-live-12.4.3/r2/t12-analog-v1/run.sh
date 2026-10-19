#!/bin/sh
# Regenerate the Analog evidence (about 10 minutes on 8 workers). Needs gcc, python3 with numpy and scipy,
# objdump, the app bundle at /home/ollie/Ableton Live 12 Suite.app and, for static_map.py, the read-only
# helper corpus /var/tmp/sound-analysis/helpers/Analog. The loader is built to
# /var/tmp/sound-analysis/t12-analog/xdev (XDEV_BIN overrides); AN_WORKERS sets the parallel renders.
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python3 -I -c "import sys; sys.path.insert(0, '.'); import xdevpy; xdevpy.build()"
python3 -I fit.py
python3 -I static_map.py
python3 -I measure.py > results/measure.txt
python3 -I cases.py > results/cases.txt
python3 -I fma_scan.py "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Analog.bundle/Contents/MacOS/Analog" > results/fma_scan.txt
python3 -I make_manifest.py
