"""Re-hash every file listed in an evidence-run manifest. Usage: python3 -I evidence_hashes.py MANIFEST [...]"""
import hashlib, json, sys
from pathlib import Path

for m in map(Path, sys.argv[1:]):
    doc = json.loads(m.read_text())
    files = doc["files"]
    rows = files.items() if isinstance(files, dict) else [(f.get("path"), f) for f in files]
    bad, n = [], 0
    for path, f in rows:
        want = f if isinstance(f, str) else f.get("sha256")
        p = m.parent / path
        n += 1
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != want:
            bad.append(path)
    print(m.parent.name, "listed", n, "mismatches", bad)
