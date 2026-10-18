#!/bin/sh
# Regenerate S1 static evidence. Read-only on the bundle and Live.arm64.
set -eu
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
H=$(cd "$(dirname "$0")" && pwd)
BIN="$H/../../derived/Live.arm64"
python3 -I "$H/s1_schema.py" "$B/App-Resources/Schema" "$H/schema-survey.json"
python3 -I "$H/s1_documents.py" "$B" "$B/App-Resources/Schema" "$H/documents-survey.json" "$H/inputs-documents.tsv"
python3 -I "$H/s1_anchors.py" "$BIN" "$B/App-Resources/Schema/12.0_12402.txt" "$H/anchors-live-arm64.json"
python3 -I - "$H" "$B" <<'PY'
import hashlib, json, os, platform, subprocess, sys
h, b = sys.argv[1], sys.argv[2]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
schema = json.load(open(f"{h}/schema-survey.json"))
docs = json.load(open(f"{h}/documents-survey.json"))
anch = json.load(open(f"{h}/anchors-live-arm64.json"))
schema_list = "".join(f"{v['sha256']}  {v['file']}\n" for v in schema["versions"])
default = docs["liveset_records"][[r["path"] for r in docs["liveset_records"]].index(
    "App-Resources/Builtin/Templates/DefaultLiveSet.als")]
prior = {  # hashes recorded in wiki/research/native-transport-study.md
    "Schema/12.0_12402.txt": ["b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299",
                              schema["versions"][-1]["sha256"]],
    "DefaultLiveSet.als compressed": ["aeec3f07599da0a61cc86fd9ddeb78a5ce61fe473f676d50c1ae3e281c289a1f", default["sha256"]],
    "DefaultLiveSet.als decoded": ["6ccfa96df1e7a7fbdcd48fc40641ace19bd5e798acc23117c45fda64a78d4783", default["decoded_sha256"]],
    "Live.arm64": ["3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad", anch["sha256"]],
}
out = sorted(f for f in os.listdir(h) if f != "manifest.json" and os.path.isfile(f"{h}/{f}"))
m = {
    "id": "S1-STATIC-V1", "packet": "S1 transport-state fields, static half",
    "target": "Ableton Live 12 Suite 12.4.3", "bundle": b, "host": platform.platform(),
    "python": sys.version.split()[0],
    "cxxfilt": subprocess.run(["c++filt", "--version"], capture_output=True, text=True).stdout.splitlines()[0],
    "command": "sh run.sh",
    "inputs": {
        "schema_files": {"count": schema["files_parsed"], "appledouble_skipped": schema["appledouble_skipped"],
                         "digest_list_sha256": hashlib.sha256(schema_list.encode()).hexdigest(),
                         "digest_list_location": "schema-survey.json versions[].sha256"},
        "documents": {"count": docs["files"], "appledouble_skipped": docs["appledouble_skipped"],
                      "digest_list": "inputs-documents.tsv"},
        "binary": {"path": "../../derived/Live.arm64", "sha256": anch["sha256"], "bytes": anch["bytes"]},
    },
    "prior_hash_checks": {k: {"recorded": r, "recomputed": c, "match": r == c} for k, (r, c) in prior.items()},
    "outputs": {f: {"sha256": sha(f"{h}/{f}"), "bytes": os.path.getsize(f"{h}/{f}")} for f in out},
}
json.dump(m, open(f"{h}/manifest.json", "w"), indent=1)
assert all(v["match"] for v in m["prior_hash_checks"].values()), m["prior_hash_checks"]
PY
