#!/bin/sh
# T1.3 audio (unwarped audio clip playback): regenerate results/, raw/runs.jsonl, summary.txt and the shipped-clip scan.
# Requires gcc, gdb, objdump, python3 with numpy; the Live x86_64 slice (XEXEC_SLICE, default in xexec.py) and the app bundle.
# Builds xexec_t13.c (tools/xexec/xexec.c plus "poke") to /var/tmp/sound-analysis/xexec-t13-audio/xexec.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
python3 -I -B run_x.py > summary.txt
A="/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources"
find "$A" \( -name '*.als' -o -name '*.alc' \) -print0 | sort -z | xargs -0 python3 -I -B unwarped_clips.py > shipped-unwarped-clips.jsonl 2> scan-skipped.txt
