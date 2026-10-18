#!/bin/sh
# Regenerate S9 evidence. Read-only on the bundle, Live.arm64 and the C1/C2 corpus. Nothing is executed from the bundle.
set -eu
H=$(cd "$(dirname "$0")" && pwd)
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
BIN="$H/../../derived/Live.arm64"
cd "$H"
export N1_CACHE="${N1_CACHE:-$(mktemp -d)/entry-map.pickle}"
python3 -I s9_static.py "$B" static-survey.json inputs-documents.tsv
python3 -I derive_curves.py > curves.txt
{
  for v in 0x1067d0108 0x1066807e0 0x106670828 0x106670bc8 0x106774f60 0x106670140; do
    echo "== read_ptrs $v 12"; python3 -I read_ptrs.py "$BIN" $v 12; done
  for a in "0x1058486a8 i 7" "0x1058486c4 i 7" "0x10588302c f 6" "0x105883044 f 6" "0x105bb3a43 B 7"; do
    echo "== read_mem $a"; python3 -I read_mem.py "$BIN" $a; done
} > image-reads.txt
python3 -I corpus_lookup.py excerpt corpus-excerpts.jsonl $(grep -v '^#' corpus-entries.txt)
python3 -I - "$H" <<'PY'
import hashlib, json, os, sys
h = sys.argv[1]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
files = {}
for d, _, fs in os.walk(h):
    for f in sorted(fs):
        p = os.path.join(d, f); r = os.path.relpath(p, h)
        if r == 'manifest.json' or f.startswith('.'): continue
        files[r] = {'sha256': sha(p), 'bytes': os.path.getsize(p)}
m = json.load(open(os.path.join(h, 'manifest-head.json')))
m['files'] = dict(sorted(files.items()))
json.dump(m, open(os.path.join(h, 'manifest.json'), 'w'), indent=1)
PY
