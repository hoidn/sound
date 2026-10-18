"""Print C1 pseudocode records for given function entries of Ableton_Index.arm64.

Usage: python3 -I code_of.py <chunks-dir> <out-dir|-> 0x<entry>...
Writes <out-dir>/<entry>.c (pseudocode, prefixed by a comment with name/state/warnings), or prints
to stdout when out-dir is '-'. Input format: wiki/research/r2-corpus-tooling.md (C1 records).
"""
import json, pathlib, sys

chunks, out, wanted = pathlib.Path(sys.argv[1]), sys.argv[2], {int(a, 16) for a in sys.argv[3:]}
found = set()
for path in sorted(chunks.glob("chunk-*.jsonl")):
    for line in path.open():
        r = json.loads(line)
        if int(r["entry"], 16) in wanted:
            text = f"// {r['entry']} {r['name']} state={r['state']} body_bytes={r['body_bytes']} warnings={len(r['warnings'])} chunk={path.name}\n{r['code'] or ''}"
            found.add(int(r["entry"], 16))
            if out == "-":
                print(text)
            else:
                pathlib.Path(out, r["entry"] + ".c").write_text(text)
missing = wanted - found
if missing:
    sys.exit("not found: " + " ".join(hex(a) for a in sorted(missing)))
