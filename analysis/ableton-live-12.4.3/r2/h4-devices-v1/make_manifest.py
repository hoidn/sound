"""H4 static: write manifest.json (SHA-256 of every script and output; pinned inputs and commands).

Usage: python3 -I make_manifest.py <evidence dir> <App-Resources dir> <Live.arm64> <helpers root>
"""
import hashlib, json, os, platform, sys


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


ev, res, img, helpers = sys.argv[1:5]
files = sorted(os.path.relpath(os.path.join(d, f), ev) for d, _, fs in os.walk(ev) for f in fs
               if f != "manifest.json" and "__pycache__" not in d)
slugs = ["Amplifier", "Cabinet", "Analog", "Tension", "Collision", "Electric", "Corpus"]
corpus = {}
for s in slugs:
    c = json.load(open(os.path.join(helpers, s, "corpus/decomp/coverage.json")))
    m = os.path.join(helpers, s, "corpus/indexes/manifest.json")
    corpus[s] = {"slice": json.load(open(os.path.join(helpers, s, "slice.json"))),
                 "summary": json.load(open(os.path.join(helpers, s, "summary.json"))),
                 "coverage": {k: c[k] for k in ("eligible", "attempted", "successful", "counts", "run_sha256")},
                 "indexes_manifest_sha256": sha(m)}
manifest = {
    "id": "H4-DEVICES-V1", "created": "2026-10-17", "python": platform.python_version(), "host": platform.platform(),
    "commands": [
        "python3 -I bundles.py <App-Resources>/Devices/Mac out",
        "python3 -I schema_devices.py <App-Resources>/Schema out",
        "python3 -I presets.py <App-Resources> out",
        "python3 -I tables.py out",
        "python3 -I param_tables.py /var/tmp/sound-analysis/helpers out",
        "python3 -I entry_points.py /var/tmp/sound-analysis/helpers out",
        "python3 -I live_strings.py analysis/ableton-live-12.4.3/derived/Live.arm64 out",
        "python3 -I corpus_labels.py <App-Resources> analysis/ableton-live-12.4.3/derived/Live.arm64 out",
        "python3 -I checks.py out <App-Resources>/Devices/Mac",
        "python3 -I make_manifest.py . <App-Resources> <Live.arm64> /var/tmp/sound-analysis/helpers",
    ],
    "inputs": {
        "app_resources": res,
        "info_plist": {"path": os.path.join(os.path.dirname(res.rstrip("/")), "Info.plist"),
                       "sha256": sha(os.path.join(os.path.dirname(res.rstrip("/")), "Info.plist"))},
        "live_arm64": {"path": img, "size": os.path.getsize(img), "sha256": sha(img)},
        "scanned_documents": {"digest_list": "out/inputs.jsonl", "sha256": sha(os.path.join(ev, "out/inputs.jsonl"))},
        "helper_corpora": corpus,
        "ghidra": "12.1.4 (C1 R2BulkDecompile / C2 R2ExportIndexes outputs, read only)",
    },
    "outputs": {f: {"size": os.path.getsize(os.path.join(ev, f)), "sha256": sha(os.path.join(ev, f))} for f in files},
}
json.dump(manifest, open(os.path.join(ev, "manifest.json"), "w"), indent=1)
