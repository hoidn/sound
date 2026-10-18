#!/bin/sh
# Regenerate S5 static outputs, the registry-order check and the manifest.
# Read-only on the bundle, the Live slice and the C1/C2 corpus. results/ (query-server output)
# and corpus-excerpts.jsonl are kept as captured; they are hashed, not regenerated.
set -eu
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
H=$(cd "$(dirname "$0")" && pwd)
python3 -I "$H/s5_static.py" "$B" "$H/static-survey.json" "$H/inputs-documents.tsv" "$H/clip-records.tsv"
python3 -I "$H/check_registry_order.py" "$H/corpus-excerpts.jsonl" "$B/App-Resources/Schema/12.0_12402.txt" \
  > "$H/registry-order-check.txt"
python3 -I - "$H" <<'PY'
import hashlib, json, os, platform, sys
h = sys.argv[1]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
files = sorted(os.path.relpath(os.path.join(d, f), h) for d, _, fs in os.walk(h) for f in fs
               if f != "manifest.json" and not f.startswith("."))
m = {
    "id": "S5-CLIP-LAUNCH-V1", "packet": "S5 clip launch settings and launch quantization",
    "target": "Ableton Live 12 Suite 12.4.3 arm64",
    "binary": {"path": "../../derived/Live.arm64", "sha256": sha(os.path.join(h, "../../derived/Live.arm64"))},
    "host": platform.platform(), "python": sys.version.split()[0], "command": "sh run.sh",
    "query_rounds": {"s5-0001": 8, "s5-0002": 8, "s5-0003": 8, "s5-0004": 8},
    "files": {f: {"sha256": sha(os.path.join(h, f)), "bytes": os.path.getsize(os.path.join(h, f))} for f in files},
}
json.dump(m, open(os.path.join(h, "manifest.json"), "w"), indent=1)
PY
