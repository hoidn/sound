#!/bin/sh
# Regenerate H1 plugin-scanner static evidence. Read-only on the bundle, the helper
# slice, its C1 corpus and C2 indexes; never opens the Ghidra project.
set -eu
H=$(cd "$(dirname "$0")" && pwd)
D=/var/tmp/sound-analysis/helpers/Ableton_Plugin_Scanner
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
S=$D/Ableton_Plugin_Scanner.arm64
python3 -I "$H/h1_extract.py" "$D" "$B" "$H"
python3 -I "$H/macho_vtables.py" "$S" 0x100b6cf28 0x100b442c8 0x100b44748 0x100b43b10 0x100b43b78 0x100b43ab8 \
  0x100b709d8 0x100b444d8 0x100b44558 0x100b443e8 0x100b46480 > "$H/vtables.json"
python3 -I "$H/string_refs.py" "$D/corpus/indexes/strings.jsonl" "$H/keys.txt" > "$H/string-refs.tsv"
python3 -I - "$H" "$D" <<'PY'
import hashlib, json, os, platform, sys
h, d = sys.argv[1], sys.argv[2]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
files = {}
for root, _, names in os.walk(h):
    for n in sorted(names):
        p = os.path.join(root, n)
        r = os.path.relpath(p, h)
        if r != "manifest.json":
            files[r] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
cov = json.load(open(f"{d}/corpus/decomp/coverage.json"))
m = {
    "id": "H1-PLUGIN-SCANNER-V1", "packet": "H1 plugin discovery (FEAT-HOSTING), static",
    "target": "Ableton Live 12 Suite 12.4.3", "host": platform.platform(),
    "python": sys.version.split()[0], "command": "sh run.sh",
    "helper": {"slice": json.load(open(f"{d}/slice.json")), "summary": json.load(open(f"{d}/summary.json")),
               "corpus_run_sha256": cov["run_sha256"], "corpus_counts": cov["counts"],
               "corpus_timed_out": cov["timed_out"],
               "indexes_manifest_sha256": sha(f"{d}/corpus/indexes/manifest.json")},
    "files": dict(sorted(files.items())),
}
json.dump(m, open(f"{h}/manifest.json", "w"), indent=1)
PY
