#!/bin/sh
# Reviewer's static check of the envelope removal on open (finding RA2-01). Read-only on the corpora and images.
# Output in removal/: corpus excerpts with line SHA-256 (arm64, x86_64), x86_64 disassembly, image reads.
set -eu
H=$(cd "$(dirname "$0")" && pwd)
R2="$H/../../../r2"
A="$H/../../../derived/Live.arm64"
X=/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64
L="$R2/t14-mix-v1/corpus_lookup.py"; D="$R2/t11-structure-v1/traces/a1a2/dis_x86.py"
T="$R2/t11-structure-v1/traces/tracks"
C="${TMPDIR:-/tmp}/ra2-cache"; mkdir -p "$C" "$H/removal"; cd "$H/removal"
CORPUS=/var/tmp/sound-analysis/corpus LOOKUP_CACHE="$C/arm64.pickle" python3 -I "$L" excerpt excerpts-arm64.jsonl \
  0x102695f78 0x101849958 0x10185138c 0x1018499a4 0x102711584 0x10275a1dc 0x1025cde14 0x10270c118 0x10265e0c8 \
  0x102456e98 0x1024559b8 0x102406378 0x1024dd434 0x1024dd41c 0x101482798 0x1024dd3a8 0x1014827f8 0x1025619e0 \
  0x1025654e8 0x1026fc4c4 0x102485d28
CORPUS=/var/tmp/sound-analysis/corpus-x86 LOOKUP_CACHE="$C/x86.pickle" python3 -I "$L" excerpt excerpts-x86.jsonl \
  0x1027c1640 0x102843e40 0x1025765e0 0x1025752e0 0x102523310 0x102601720 0x1026016f0 0x10281afa0 0x102687f00 \
  0x10268b7d0 0x10282e7c0 0x10186b240 0x101863860 0x1018638b0
python3 -I "$D" "$X" "0x1027c1964:0x1027c1993:song post-load per-track loop: gate byte +0x3a0, then track removal" \
  "0x10186b240:0x10186b24c:gate getter" "0x101863a37:0x101863a47:application constructor stores 1 at +0x3a0" \
  "0x102843e40:0x102843eb4:per track: clip removal per clip, then track-envelope removal" \
  "0x102523350:0x1025233c0:track-envelope removal test" "0x102601720:0x102601776:relation test" \
  "0x1026016f0:0x1026016fe:target +0x1e8 -> +0x1e0" "0x10281afa0:0x10281afaa:target +0x1e0 (owner)" \
  "0x10282e7c0:0x10282e7c8:TimeableFloat/Bool/Enum +0x338" "0x102687f00:0x102687f36:AListAutomation +0x2b8 (count >= 2)" \
  "0x10268b7d0:0x10268b82f:AListAutomation +0x398 full-range branch" "0x10155dd50:0x10155dd5e:list size" \
  "0x10257533e:0x1025753da:clip-envelope removal test" > x86-disasm.txt
{
  echo "== range constants"; python3 -I "$H/img_read.py" "$A" dbl 0x1055d9680 2
  for v in 0x105b3eb10 0x105b9e6f0 0x105b42d18; do python3 -I "$H/img_read.py" "$X" dbl $v 2; done
  echo "== slot owners"; python3 -I "$T/vtable_owner.py" "$A" 0x1025619e0 0x1025654e8; python3 -I "$T/vtable_owner.py" "$X" 0x102687f00
  echo "== x86 AListAutomation vtable 0x106d15a60 +0x398, +0x1e8"; python3 -I "$T/read_ptrs.py" "$X" 0x106d15df8 1
  python3 -I "$T/read_ptrs.py" "$X" 0x106d15c48 1
  echo "== arm64 vtables (offset-to-top 0 rows are primary)"
  python3 -I "$H/rtti_vtable.py" "$A" 0x1d8,0x1e0,0x1e8,0x338 AFloatAutomationTarget ABoolAutomationTarget \
    AEnumAutomationTarget ATimeableFloat ATimeableBool ATimeableEnum AUserFloatModulationTarget
  echo "== x86 vtables"
  python3 -I "$H/rtti_vtable.py" "$X" 0x1d8,0x1e0,0x1e8,0x338 AFloatAutomationTarget ABoolAutomationTarget \
    AEnumAutomationTarget ATimeableFloat ATimeableBool ATimeableEnum
} > image-reads.txt
python3 -I - "$H/removal/excerpts-arm64.jsonl" > gate-writers-arm64.txt <<'PY'
import json, re, sys, glob
# every arm64 function whose pseudocode stores a byte or halfword at +0x350 and uses the application getter or
# global, or lies in the application's address range; rescans the whole corpus
for f in sorted(glob.glob('/var/tmp/sound-analysis/corpus/decomp/chunks/*.jsonl')):
    for line in open(f):
        if '0x350) =' not in line: continue
        r = json.loads(line); c = r['code'] or ''; a = int(r['entry'], 16)
        hits = [l.strip() for l in c.split('\n') if re.search(r'\*\((undefined1|undefined2|char|bool|byte)\s*\*\)\(\w+ \+ 0x350\) =', l)]
        if hits and ('DAT_106f54e20' in c or 'FUN_101849958' in c or 0x101840000 <= a < 0x101860000):
            print(r['entry'], hits)
PY
