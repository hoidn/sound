#!/bin/sh
# X2 extracted execution of Live 12.4.3 mixer value functions (ADR 0003, evidence label X).
# Regenerates results/mixer.json, raw/runs.jsonl, x86-disasm.txt, fma-scan.txt and manifest.json.
# Requires: gcc, objdump, python3; the x86_64 slice at XEXEC_SLICE (default below).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
: "${XEXEC_SLICE:=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64}"
export XEXEC_SLICE
python3 -I -B run_mixer.py
python3 -I -B fp_scan.py ../../derived/Live.arm64 "$XEXEC_SLICE" fma-scan.txt \
  0x101ac2bf8:0x101aec640 0x101ac3498:0x101aecbd0 0x101ac353c:0x101aecc90 \
  0x101b3b95c:0x101b719e0 0x101aede40:0x101b198c0 \
  0x101aee8b8:0x101b1a470 0x101aee9c0:0x101b1a550 0x101aeeac0:0x101b1a630 \
  0x101aeeb98:0x101b1a6f0 0x101aeec78:0x101b1a7b0 0x101aeed4c:0x101b1a880 0x101aeedb8:0x101b1a8e0
python3 -I -B make_evidence.py
