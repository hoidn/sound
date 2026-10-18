"""H2 browser index: write manifest.json (SHA-256 of every script and output; pin inputs).

Usage: python3 -I make_manifest.py <evidence dir> <helper dir> <App-Resources dir> <Live.arm64>
"""
import hashlib, json, os, platform, sys


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


ev, helper, app, live = sys.argv[1:5]
files = sorted(os.path.relpath(os.path.join(d, f), ev) for d, _, fs in os.walk(ev) for f in fs if f != "manifest.json")
idx = json.load(open(os.path.join(helper, "corpus/indexes/manifest.json")))
manifest = {
    "id": "H2-INDEX-V1", "created": "2026-10-17", "python": platform.python_version(), "host": platform.platform(),
    "command": "bash run.sh",
    "inputs": {
        "helper_slice": json.load(open(os.path.join(helper, "slice.json"))),
        "helper_summary": json.load(open(os.path.join(helper, "summary.json"))),
        "c1_run_json_sha256": sha(os.path.join(helper, "corpus/decomp/run.json")),
        "c1_coverage_json_sha256": sha(os.path.join(helper, "corpus/decomp/coverage.json")),
        "c2_index_files": idx["files"],
        "filerefmap_db": {"path": os.path.join(app, "Database/filerefmap.db"), "sha256": sha(os.path.join(app, "Database/filerefmap.db"))},
        "live_arm64": {"path": live, "size": os.path.getsize(live), "sha256": sha(live)},
        "ghidra_project": os.path.join(helper, "project") + " (opened read-only once for typeinfo references; no outputs retained)",
    },
    "outputs": {f: {"size": os.path.getsize(os.path.join(ev, f)), "sha256": sha(os.path.join(ev, f))} for f in files},
}
json.dump(manifest, open(os.path.join(ev, "manifest.json"), "w"), indent=1)
