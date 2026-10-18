"""Inventory application SQL strings in Ableton_Index.arm64 (C2 strings.jsonl).

Usage: python3 -I sql_inventory.py <strings.jsonl> <out.jsonl> <summary.json>
Selects defined strings that start (after whitespace) with an SQL verb, excluding the embedded
SQLite library's own format strings (those containing printf-style %Q/%q/%w/%s/%z or sqlite_ names).
Each output line: address, value, referencing functions. The summary lists table names created
anywhere, columns of every CREATE TABLE statement seen, and counts.
"""
import json, re, sys

VERB = re.compile(r"^\s*(CREATE|ALTER|DROP|INSERT|SELECT|UPDATE|DELETE|WITH|PRAGMA|REPLACE|ANALYZE|VACUUM|BEGIN|COMMIT|ATTACH)\b", re.I)
LIBRARY = re.compile(r"%[QqwszT]|sqlite_|\bx\(|fts3|fts4aux|fts5|json_each|zipfile|dbstat")
CREATE = re.compile(r"CREATE\s+(TEMPORARY\s+)?(VIRTUAL\s+)?TABLE\s+(IF NOT EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:USING\s+\w+\s*)?\((.*?)\)\s*;", re.I | re.S)

def referrers(rec):
    out = set()
    for ref in rec.get("refs", []):
        if ref.get("function"):
            out.add(ref["function"])
        for via in ref.get("via", []):
            if via.get("function"):
                out.add("via:" + via["function"])
    return sorted(out)

def columns(body):
    cols = []
    for part in re.split(r",(?![^()]*\))", body):
        tok = part.strip().split()
        if tok and tok[0].upper() not in ("UNIQUE", "PRIMARY", "FOREIGN", "CHECK", "CONSTRAINT"):
            cols.append(tok[0])
    return cols

src, out_path, summary_path = sys.argv[1:4]
rows, tables = [], {}
for line in open(src):
    r = json.loads(line)
    v = r["value"]
    if not VERB.match(v) or LIBRARY.search(v) or len(v) < 8:
        continue
    rows.append({"address": r["address"], "value": v, "functions": referrers(r)})
    for m in CREATE.finditer(v if v.rstrip().endswith(";") else v + ";"):
        name = m.group(4)
        tables.setdefault(name, []).append({"address": r["address"], "columns": columns(m.group(5))})
with open(out_path, "w") as o:
    for row in rows:
        o.write(json.dumps(row, ensure_ascii=False) + "\n")
summary = {
    "sql_strings": len(rows),
    "referenced": sum(1 for r in rows if r["functions"]),
    "tables": {k: v for k, v in sorted(tables.items())},
}
json.dump(summary, open(summary_path, "w"), indent=1, sort_keys=True)
print(json.dumps({"sql_strings": summary["sql_strings"], "referenced": summary["referenced"], "tables": sorted(tables)}))
