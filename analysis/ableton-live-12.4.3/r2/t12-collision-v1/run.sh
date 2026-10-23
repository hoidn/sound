#!/bin/sh
# Regenerate the Collision evidence (about 3 minutes). Needs gcc, python3 with numpy and scipy, objdump,
# gst-launch-1.0 with the Ogg and Vorbis plug-ins, and the app bundle at /home/ollie/Ableton Live 12 Suite.app.
# The loader is built to /var/tmp/sound-analysis/t12-collision/xdev (XDEV_BIN overrides); scratch renders
# go to /var/tmp/sound-analysis/t12-collision/.
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
rm -f results/collision.json
python3 -I fit.py
python3 -I run_collision.py
python3 -I run_noise.py
python3 -I libm_sensitivity.py
python3 -I previews.py
python3 -I fma_scan.py "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Collision.bundle/Contents/MacOS/Collision" \
  0x2809c 0x38edc 0x2faa0 0x13ba0 > results/fma_scan.txt
python3 -I make_manifest.py
