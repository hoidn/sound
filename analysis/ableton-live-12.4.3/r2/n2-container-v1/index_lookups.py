"""Extract the C2 index rows N2 relied on (direct callers and string referrers).

Usage: python3 -I index_lookups.py <indexes-dir> > index-lookups.jsonl
"""
import json, pathlib, sys

CALLEES = {"0x101485c50", "0x101485240", "0x10146c0d4", "0x10146c258", "0x10148389c", "0x1018536d4",
           "0x1002e6e00", "0x101528c84", "0x101488ec0", "0x10148229c", "0x101529024", "0x101515628",
           "0x101515c1c", "0x101514954", "0x10147f9b4", "0x1018ed778", "0x102971090"}
STRINGS = {"MajorVersion", "MinorVersion", "SchemaChangeCount", "Revision", "Creator", "Ableton ",
           "Ableton Live ", '<?xml version="1.0" encoding="UTF-8"?>'}
idx = pathlib.Path(sys.argv[1])
with (idx / "calls.jsonl").open() as f:
    for line in f:
        if any(f'"callee":"{c}"' in line for c in CALLEES):
            r = json.loads(line)
            print(json.dumps({"index": "calls", "callee": r["callee"], "caller": r["caller"], "site": r["site"], "kind": r["kind"]}))
with (idx / "strings.jsonl").open() as f:
    for line in f:
        r = json.loads(line)
        if r["value"] in STRINGS:
            print(json.dumps({"index": "strings", "address": r["address"], "value": r["value"],
                              "functions": sorted({x["function"] or "data" for x in r["refs"]})}))
