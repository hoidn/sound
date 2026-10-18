"""Dump defined strings of Ableton_Index.arm64 in an address range, with referencing functions.

Usage: python3 -I strings_region.py <strings.jsonl> <start-hex> <end-hex> <out.tsv>
Input: C2 strings.jsonl (wiki/research/r2-corpus-tooling.md). Output: TSV address, value (repr,
truncated to 400 chars), referencing function entries (direct, or 'via' one data hop).
"""
import json, sys

def referrers(rec):
    out = set()
    for ref in rec.get("refs", []):
        if ref.get("function"):
            out.add(ref["function"])
        for via in ref.get("via", []):
            if via.get("function"):
                out.add("via:" + via["function"])
    return sorted(out)

src, start, end, dst = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16), sys.argv[4]
with open(src) as f, open(dst, "w") as o:
    for line in f:
        r = json.loads(line)
        if start <= int(r["address"], 16) < end:
            o.write(f"{r['address']}\t{repr(r['value'])[:400]}\t{' '.join(referrers(r))}\n")
