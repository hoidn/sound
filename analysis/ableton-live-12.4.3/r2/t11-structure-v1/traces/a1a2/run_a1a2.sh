#!/bin/sh
# Static trace of A1 (open path to the post-load checks) and A2 (freeze slots during reading).
# Read-only on the corpora and images. Output: corpus excerpts, vtable owners, reachability, x86 disassembly.
set -eu
H=$(cd "$(dirname "$0")" && pwd)
R="$H/../../.."
B="$R/../derived/Live.arm64"
cd "$H"
export N1_CACHE="${N1_CACHE:-$(mktemp -d)/arm64-map.pickle}"
python3 -I "$R/s9-mixer-v1/corpus_lookup.py" excerpt corpus-excerpts.jsonl \
  0x101486fe4 0x101487198 0x101484108 0x101478258 0x10151e0d8 0x1015192c0 0x1015192b8 0x101546518 0x101547ef4 \
  0x10146c258 0x1018536d4 0x1002e6e00 0x1011c709c 0x10184e56c 0x101854f54 0x10184df98 0x1018517cc 0x10185139c \
  0x101852600 0x1025cb2b8 0x1027de958 0x1025cb248 0x1027df560 0x10291f76c 0x1027e3118 0x1027df670 0x10291f948 \
  0x10265e1d8 0x10265d22c 0x1025cde68 0x1025cdeb8 0x1025cdf38 0x10268dfc8 0x10267af54 0x1025776b4 0x10257770c \
  0x1023bfed4 0x101535944 0x101856bc8 > /dev/null
X86_CACHE="$(dirname "$N1_CACHE")/x86-map.pickle" python3 -I corpus_lookup_x86.py excerpt corpus-excerpts-x86.jsonl \
  0x10147e150 0x10147b550 0x10146e9f0 0x10150cb10 0x1015084b0 0x10186d760 0x10035eec0 0x101868370 0x10186edc0 \
  0x101867dc0 0x1026f1720 > /dev/null
python3 -I "$H/../tracks/vtable_owner.py" "$B" 0x1002e6e00 0x1018536d4 0x101854f54 0x101852600 0x1025cb2b8 \
  0x1027de958 0x1025cb248 0x1025cde68 0x1025cdeb8 0x1025cdf38 0x1027df670 0x10291f948 > vtable-owners.txt
for v in 0x10680fe20 0x106829160; do for o in 0xd0 0x100; do
  python3 -I "$H/../tracks/read_ptrs.py" "$B" "$(python3 -c "print(hex($v + $o))")" 1; done; done > chain-vtable-slots.txt
{
  for r in 0x1002e6e00 0x1018536d4; do echo "== root $r"; python3 -I reach.py /var/tmp/sound-analysis/corpus 6 $r \
    0x10148389c 0x101484108 0x101486fe4 0x10146c0d4 0x10146c258 0x101535944; done
  for r in 0x102695f78 0x1025cb2b8 0x1027de958 0x1023c6d80 0x1014674b4 0x101486fe4 0x101487310; do echo "== root $r"
    python3 -I reach.py /var/tmp/sound-analysis/corpus 5 $r 0x10265d22c 0x10265e1d8 0x1025cde68 0x1025cdf38 \
      0x10268dfc8 0x10267d264 0x10267bfc0 --grep '\+ 0x2e8\)\)\('; done
} > reach.txt
python3 -I dis_x86.py /var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64 \
  "0x10147e150:0x10147e2e0:load step; arm64 0x101486fe4" "0x1015084b0:0x1015084c0:context +0x2c read" \
  "0x10147e2e0:0x10147e3a0:walk; arm64 0x101487198" "0x10150cb10:0x10150cb84:context constructor; arm64 0x10151e0d8" \
  > x86-load-sequence.txt
