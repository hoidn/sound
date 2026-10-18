"""Copy pseudocode rows for given function entries out of the C1 bulk corpus.

Usage: python3 -I corpus_get.py <chunks-dir> <out-dir> 0x<entry>...
Reads chunk-*.jsonl rows (fields entry, state, code, code_sha256); writes <out-dir>/<entry>.c
and prints entry, state and code_sha256. A missing entry prints "absent" (corpus may be partial).
"""
import json, pathlib, sys

chunks, out, wanted = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), set(sys.argv[3:])
found = {}
for path in sorted(chunks.glob("chunk-*.jsonl")):
    with path.open() as f:
        for line in f:
            if not any(w in line[:40] for w in wanted):
                continue
            row = json.loads(line)
            if row["entry"] in wanted:
                found[row["entry"]] = (path.name, row)
    if len(found) == len(wanted):
        break
for entry in sorted(wanted):
    if entry not in found:
        print(entry, "absent")
        continue
    name, row = found[entry]
    (out / f"{entry}.c").write_text(row["code"] or "")
    print(entry, name, row["state"], row["code_sha256"])
