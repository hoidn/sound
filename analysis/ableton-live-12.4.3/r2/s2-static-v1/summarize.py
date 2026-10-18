"""S2 static: per-extension distributions over documents.jsonl.

Usage: python3 -I summarize.py <out dir>   (reads <out>/documents.jsonl, writes <out>/summary.json)
Schema .txt rows are summarized separately by schema_inventory.py and excluded here.
"""
import json, os, statistics, sys
from collections import Counter


def dist(values):
    return dict(Counter(values).most_common())


def summarize(rows):
    by_ext = {}
    for r in rows:
        if r["ext"] == "txt":
            continue
        by_ext.setdefault(r["ext"], []).append(r)
    out = {}
    for ext, rs in sorted(by_ext.items()):
        g = [r["gzip"] for r in rs if "gzip" in r]
        x = [r["xml"] for r in rs if "xml" in r]
        ab = [v for v in x if v["root"] == "Ableton"]
        attrs = [dict(v["root_attrs"]) for v in ab]
        sizes = [r["payload_size"] for r in rs if "payload_size" in r]
        s = {
            "files": len(rs),
            "by_top_dir": dist(r["top"] for r in rs),
            "container": dist(r["container"] for r in rs),
            "magic8_non_gzip_non_xml": dist(r["magic16"][:16] for r in rs if r["container"] not in ("gzip", "xml-like")),
            "errors": [r["path"] for r in rs if "error" in r],
        }
        if g:
            s["gzip"] = {
                "cm": dist(h["cm"] for h in g), "flags": dist("|".join(h["flags"]) or "(none)" for h in g),
                "reserved_bits_set": sum(1 for h in g if h["reserved_bits"]),
                "mtime_zero": sum(1 for h in g if h["mtime"] == 0),
                "mtime_min_max_nonzero": [min((h["mtime"] for h in g if h["mtime"]), default=None),
                                          max((h["mtime"] for h in g if h["mtime"]), default=None)],
                "xfl": dist(h["xfl"] for h in g), "os": dist(h["os"] for h in g),
                "fname_present": sum(1 for h in g if "fname" in h),
                "fname_values_sample": sorted({h["fname"] for h in g if "fname" in h})[:10],
                "header_len": dist(h["header_len"] for h in g),
                "trailing_bytes_nonzero": sum(1 for h in g if h["trailing_bytes"]),
            }
        if x:
            s["xml"] = {
                "decl": dist(v["decl"] for v in x), "bom": sum(v["bom"] for v in x),
                "crlf": sum(v["crlf"] for v in x), "ends_with_newline": sum(v["ends_with_newline"] for v in x),
                "well_formed": sum(v["well_formed"] for v in x),
                "parse_errors": [(r["path"], r["xml"]["parse_error"]) for r in rs if "xml" in r and not r["xml"]["well_formed"]],
                "root": dist(v["root"] for v in x),
                "root_line": dist(v.get("root_line") for v in x),
                "root_attr_order": dist(",".join(a for a, _ in v["root_attrs"]) for v in ab),
                "MajorVersion": dist(a.get("MajorVersion") for a in attrs),
                "MinorVersion": dict(sorted(Counter(a.get("MinorVersion") for a in attrs).items(), key=lambda kv: str(kv[0]))),
                "SchemaChangeCount": dist(a.get("SchemaChangeCount") for a in attrs),
                "Creator": dist(a.get("Creator") for a in attrs),
                "Revision_distinct": len({a.get("Revision") for a in attrs if "Revision" in a}),
                "Revision_absent": sum(1 for a in attrs if "Revision" not in a),
                "Revision_empty": sum(1 for a in attrs if a.get("Revision") == ""),
                "Revision_forms": dist(("40hex" if len(v) == 40 and all(c in "0123456789abcdef" for c in v) else repr(v)[:24])
                                       for a in attrs if "Revision" in a for v in [a["Revision"]]),
                "first_child": dist(v["first_child"] for v in x),
                "payload_size_min_median_max": [min(sizes), int(statistics.median(sizes)), max(sizes)] if sizes else None,
            }
        out[ext] = s
    return out


if __name__ == "__main__":
    d = sys.argv[1]
    rows = [json.loads(l) for l in open(os.path.join(d, "documents.jsonl"))]
    json.dump(summarize(rows), open(os.path.join(d, "summary.json"), "w"), indent=1)
