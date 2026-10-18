"""S2 static: Schema/ directory inventory and document-version cross-check.

Usage: python3 -I schema_inventory.py <Schema dir> <out dir>
Reads <out>/documents.jsonl (from doc_inventory.py); writes <out>/schemas.json.
"""
import hashlib, json, os, re, sys
import xml.parsers.expat
from collections import Counter

NAME_RE = re.compile(r"^(\d+)\.(\d+)_(\d+)\.txt$")


def schema_row(path):
    raw = open(path, "rb").read()
    st = {"depth": 0, "root": None, "root_attrs": None, "classes": 0, "fields": 0}
    px = xml.parsers.expat.ParserCreate()
    px.ordered_attributes = True

    def start(name, attrs):
        if st["depth"] == 0:
            st["root"], st["root_attrs"] = name, [[attrs[i], attrs[i + 1]] for i in range(0, len(attrs), 2)]
        elif st["depth"] == 1:
            st["classes"] += 1
        elif st["depth"] == 2:
            st["fields"] += 1
        st["depth"] += 1

    def end(name):
        st["depth"] -= 1

    px.StartElementHandler, px.EndElementHandler = start, end
    px.Parse(raw, True)  # fail fast: a malformed shipped schema is a finding to surface, not skip
    decl = raw.split(b"\n", 1)[0].decode("latin-1")
    del st["depth"]
    return {"size": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "decl": decl, **st}


def version_key(stem):
    m = NAME_RE.match(stem + ".txt")
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def main(schema_dir, out):
    names = sorted(n for n in os.listdir(schema_dir) if not n.startswith("._"))
    bad = [n for n in names if not NAME_RE.match(n)]
    rows = {}
    for n in names:
        r = schema_row(os.path.join(schema_dir, n))
        a = dict(r["root_attrs"])
        suffix = int(NAME_RE.match(n).group(3))
        r["translator_attr"] = "TranslatorNumber" if "TranslatorNumber" in a else ("TranslatorCount" if "TranslatorCount" in a else None)
        r["translator_matches_suffix"] = r["translator_attr"] is not None and int(a[r["translator_attr"]]) == suffix
        rows[n[:-4]] = r
    order = sorted(rows, key=version_key)
    suffixes = [version_key(s)[2] for s in order]
    by_sha = {}
    for s in order:
        by_sha.setdefault(rows[s]["sha256"], []).append(s)
    docs = [json.loads(l) for l in open(os.path.join(out, "documents.jsonl"))]
    used = Counter()
    for d in docs:
        x = d.get("xml") or {}
        if x.get("root") == "Ableton":
            a = dict(x["root_attrs"])
            used[(a.get("MinorVersion"), a.get("MajorVersion"), a.get("SchemaChangeCount"), d["ext"])] += 1
    cross = []
    for (minor, major, scc, ext), n in sorted(used.items(), key=lambda kv: str(kv[0])):
        s = rows.get(minor)
        sa = dict(s["root_attrs"]) if s else {}
        cross.append({"MinorVersion": minor, "ext": ext, "documents": n, "doc_MajorVersion": major,
                      "doc_SchemaChangeCount": scc, "schema_file": f"{minor}.txt" if s else None,
                      "schema_Version": sa.get("Version"), "schema_ChangeCount": sa.get("ChangeCount"),
                      "major_eq_schema_version": (major == sa.get("Version")) if s else None,
                      "scc_eq_schema_changecount": (scc == sa.get("ChangeCount")) if s and scc is not None else None})
    result = {
        "schema_dir": schema_dir, "files": len(names), "nonconforming_names": bad,
        "name_pattern": NAME_RE.pattern,
        "prefix_distribution": dict(Counter(s.split("_")[0] for s in order)),
        "oldest": order[0], "newest_by_version_key": order[-1],
        "suffix_monotonic_in_version_order": all(a < b for a, b in zip(suffixes, suffixes[1:])),
        "suffix_non_increasing_steps": [(order[i], order[i + 1]) for i in range(len(order) - 1) if suffixes[i] >= suffixes[i + 1]],
        "root_names": dict(Counter(r["root"] for r in rows.values())),
        "root_attr_orders": dict(Counter(",".join(k for k, _ in r["root_attrs"]) for r in rows.values())),
        "schema_Version_by_prefix": {p: dict(Counter(dict(rows[s]["root_attrs"]).get("Version") for s in order if s.startswith(p + "_")))
                                     for p in dict.fromkeys(s.split("_")[0] for s in order)},
        "translator_attr_matches_suffix_all": all(r["translator_matches_suffix"] for r in rows.values()),
        "translator_attr_switch": [s for i, s in enumerate(order) if i and rows[s]["translator_attr"] != rows[order[i - 1]]["translator_attr"]],
        "changecount_first_present": next((s for s in order if "ChangeCount" in dict(rows[s]["root_attrs"])), None),
        "document_versions_crosscheck": cross,
        "document_minor_versions_without_schema": sorted({c["MinorVersion"] for c in cross if c["schema_file"] is None}),
        "version_attr_switch": [s for i, s in enumerate(order) if i and dict(rows[s]["root_attrs"])["Version"] != dict(rows[order[i - 1]]["root_attrs"])["Version"]],
        "identical_content_groups": [g for g in by_sha.values() if len(g) > 1],
        "suffix_ranges": {p: {"min": min(v), "max": max(v), "count": len(v),
                              "gaps": [[a, b] for a, b in zip(v, v[1:]) if b - a > 1]}
                          for p in dict.fromkeys(s.split("_")[0] for s in order)
                          for v in [[version_key(s)[2] for s in order if s.startswith(p + "_")]]},
        "schemas": {s: rows[s] for s in order},
    }
    json.dump(result, open(os.path.join(out, "schemas.json"), "w"), indent=1)


if __name__ == "__main__":
    assert version_key("11.0_402") < version_key("11.0_11201") < version_key("12.0_12000")
    main(sys.argv[1], sys.argv[2])
