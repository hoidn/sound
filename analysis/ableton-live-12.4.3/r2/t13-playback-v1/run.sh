#!/bin/sh
# T1.3 playback core (packet t13-playback-v1): regenerate every retained output, area by area, then the manifest.
# Requires gcc, gdb, objdump, python3 (numpy for audio/), the corpora under /var/tmp/sound-analysis, the Live x86_64
# and Engine slices, analysis/ableton-live-12.4.3/derived/Live.arm64 and the app bundle (read-only).
# Each area builds its own loader outside the tree: /var/tmp/sound-analysis/xexec-t13-<area>/xexec.
# Raw outputs contain heap addresses (ASLR), so a rerun changes raw/*.jsonl hashes but not the results files.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
: "${T13_CACHE:=${TMPDIR:-/tmp}}"; export T13_CACHE
(cd transport && python3 -I -B run_transport.py > results/summary-run_transport.txt \
  && python3 -I -B sweep.py > results/summary-sweep.txt && sh retain.sh)
sh launch/run.sh
(cd .. && python3 -I -B t13-playback-v1/midi/run_x.py && python3 -I -B t13-playback-v1/midi/run_builder.py \
  && python3 -I -B t13-playback-v1/midi/cases.py > t13-playback-v1/midi/results/cases.json)
sh audio/run.sh
sh stop/run.sh
python3 -I -B end/run_end.py > /dev/null
python3 -I -B plus_one_check.py > /dev/null
python3 -I -B make_manifest.py
