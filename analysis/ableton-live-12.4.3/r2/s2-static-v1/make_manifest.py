"""S2 static: write manifest.json (hash every script and output; pin inputs).

Usage: python3 -I make_manifest.py <evidence dir> <App-Resources dir> <Live.arm64>
"""
import hashlib, json, os, platform, sys


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


ev, res, img = sys.argv[1:4]
files = sorted(os.path.relpath(os.path.join(d, f), ev) for d, _, fs in os.walk(ev) for f in fs if f != "manifest.json")
inputs = [json.loads(l) for l in open(os.path.join(ev, "out/inputs.jsonl"))]
plist = os.path.join(os.path.dirname(res.rstrip("/")), "Info.plist")
manifest = {
    "id": "S2-STATIC-V1", "created": "2026-10-17", "python": platform.python_version(), "host": platform.platform(),
    "commands": [
        "python3 -I doc_inventory.py <App-Resources> out",
        "python3 -I summarize.py out",
        "python3 -I schema_inventory.py <App-Resources>/Schema out",
        "python3 -I binary_headers.py out <the 8 files listed in out/binary_headers.json>",
        "python3 -I strings_query.py <Live.arm64> out",
        "python3 -I make_manifest.py . <App-Resources> <Live.arm64>",
    ],
    "inputs": {
        "app_resources": res,
        "info_plist": {"path": plist, "sha256": sha(plist)},
        "live_arm64": {"path": img, "size": os.path.getsize(img), "sha256": sha(img)},
        "parsed_documents": {"digest_list": "out/inputs.jsonl", "count": len(inputs),
                             "digest_list_sha256": sha(os.path.join(ev, "out/inputs.jsonl"))},
    },
    "outputs": {f: {"size": os.path.getsize(os.path.join(ev, f)), "sha256": sha(os.path.join(ev, f))} for f in files},
}
json.dump(manifest, open(os.path.join(ev, "manifest.json"), "w"), indent=1)
