#!/bin/sh
# T1.4 mix graph evidence: extracted execution of Live 12.4.3 track-output functions (ADR 0003,
# label X), the engine-to-Live function matches, the arm64 fused-multiply-add scan, and the manifest.
# Regenerates results/mix.json, raw/runs.jsonl, match-engine.txt, fma-scan.txt, x86-disasm.txt and
# manifest.json. Requires gcc, objdump, python3; the x86_64 Live slice at XEXEC_SLICE (default below).
# The static notes (notes-*.txt) and corpus excerpts (excerpts-*.jsonl) are inputs, not regenerated.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here"
: "${XEXEC_SLICE:=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64}"
export XEXEC_SLICE
python3 -I -B run_mix.py
python3 -I -B match_engine.py 0x171a20 304 0x1719e0 64 0x15c620 96 0x15c6e0 80 0x15c730 64 0x15c790 48 \
  0x1550a0 176 0x155150 176 0x158510 272 0x1a26d0 384 0x11ab30 32 0x170ab0 240 0x170c40 160 0x170eb0 192 \
  0x1500b0 160 > match-engine.txt
python3 -I -B fp_scan.py ../../derived/Live.arm64 "$XEXEC_SLICE" fma-scan.txt \
  0x101b10efc:0x101b40d30 0x101b3b720:0x101b71780 0x101b3b8f0:0x101b71950 0x101aff3a0:0x101b2b970 \
  0x101aff494:0x101b2ba80 0x101afb494:0x101b27860 0x101b18bb4:0x101b497f0 > /dev/null
python3 -I -B make_evidence.py
