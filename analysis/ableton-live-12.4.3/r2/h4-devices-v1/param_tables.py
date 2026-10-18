"""H4 static: recover the bundle-side parameter index tables of the five non-Softube bundles from C1 pseudocode.

Usage: python3 -I param_tables.py <helpers root> <out dir>
For each bundle the 'ParamLink' entries (28-byte records: module, module parameter, initialized, virtual, kind,
min, max, last value) are filled by setter functions that reference the string 'ParamLink: re-initializing ...'.
Analog/Tension/Collision/Electric: each setter's kind is read from its own pseudocode ('+ 0xc) = <kind>', virtual if
it writes '+ 9) = 1'); the table builder is the caller with the most setter calls, parsed call by call.
Corpus: the table is inlined at instance offset 0xe0078 (stride 0x1c); fields are read from the assignments.
Kinds (from TassmanSynthWrapper::SetParameter, see the research page): 0 clamp [0,1]; 1 clamp [min,max] then
rescale to 0..127; 2 clamp [min,max] passed through; 3 clamp >= 0 and truncate to int (max recorded as stored).
Writes out/param_tables.json and compares the multiset of non-[0,1] ranges with the XML modal ranges in params.json.
This parses decompiler text: it is a static derivation, and every recovered row keeps its source line.
Depends on: Python stdlib; /var/tmp/sound-analysis/helpers/<slug>/corpus/{decomp/chunks,indexes}.
"""
import collections, glob, json, os, re, struct, sys

SLUGS = {"Analog": "UltraAnalog", "Tension": "StringStudio", "Collision": "Collision", "Electric": "LoungeLizard",
         "Corpus": "Corpus"}
BASE = 0xE0078


def f32(tok):
    tok = tok.strip()
    if tok.startswith("0x"):
        return struct.unpack("<f", struct.pack("<I", int(tok, 16) & 0xFFFFFFFF))[0]
    return float(tok)


def code_of(root, slug):
    out = {}
    for f in sorted(glob.glob(f"{root}/{slug}/corpus/decomp/chunks/chunk-*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            out[r["entry"]] = r
    return out


def setters(root, slug):
    for line in open(f"{root}/{slug}/corpus/indexes/strings.jsonl"):
        r = json.loads(line)
        if r["value"].startswith("ParamLink: re-initializing"):
            return sorted({x["function"] for x in r["refs"] if x["function"]})
    raise SystemExit(f"{slug}: ParamLink string not found")


def split_args(s):
    depth, cur, out = 0, "", []
    for ch in s:
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
            continue
        depth += ch in "(["
        depth -= ch in ")]"
        cur += ch
    return out + [cur.strip()]


def aas(root, slug):
    code = code_of(root, slug)
    kinds = {}
    for s in setters(root, slug):
        c = code[s]["code"]
        k = re.findall(r"\+ 0xc\) = (\d)", c)
        sig = re.search(r"\w+ FUN_\w+\(([^)]*)\)", c).group(1)
        kinds[s] = {"name": code[s]["name"], "kind": int(k[-1]), "virtual": "+ 9) = 1" in c,
                    "float_args": sig.count("float")}
    calls = collections.Counter()
    for line in open(f"{root}/{slug}/corpus/indexes/calls.jsonl"):
        r = json.loads(line)
        if r["callee"] in kinds:
            calls[r["caller"]] += 1
    builder = calls.most_common(1)[0][0]
    rows, virt = [], set()
    for ln in code[builder]["code"].splitlines():
        m = re.search(r"(FUN_[0-9a-f]+)\((.*)\);", ln)
        if m:
            entry = "0x" + m.group(1)[4:].lstrip("0")
            k = kinds.get(entry)
            if k is None and entry in code:  # one-level wrapper around a setter (e.g. Tension 0x13b80)
                inner = ["0x" + x.lstrip("0") for x in re.findall(r"FUN_([0-9a-f]+)\(", code[entry]["code"])]
                hit = [kinds[x] for x in inner if x in kinds]
                if hit:
                    k = dict(hit[0], name=code[entry]["name"], virtual=hit[0]["virtual"] or "+ 9) = 1" in code[entry]["code"])
            if k is None:
                continue
            a = split_args(m.group(2))
            p = a.index("param_1")
            floats, idx = a[:p], int(a[p + 1], 0)
            if k["kind"] == 3:            # (table, index, [module, param,] max)
                lo, hi = 0.0, float(int(a[-1], 0))
            elif k["kind"] == 0:          # (table, index, module, param)
                lo, hi = 0.0, 1.0
            elif len(floats) == 2:        # (min, max, table, index, ...)
                lo, hi = f32(floats[0]), f32(floats[1])
            else:                         # decompiler dropped an argument; keep the line, no range
                lo, hi = None, None
            rows.append({"index": idx, "kind": k["kind"], "min": lo, "max": hi, "virtual": k["virtual"],
                         "setter": entry, "line": ln.strip()})
        v = re.search(r"\+ 0xe0060\) \+ (0x[0-9a-f]+)\) = 1;", ln)
        if v:
            virt.add((int(v.group(1), 16) - 9) // 0x1C)
    for r in rows:
        r["virtual"] = r["virtual"] or r["index"] in virt
    return {"setters": kinds, "builder": builder, "builder_name": code[builder]["name"], "rows": rows}


def corpus(root, slug):
    code = code_of(root, slug)
    s = setters(root, slug)
    c = code[s[0]]["code"]
    fields = collections.defaultdict(dict)
    for off, val in re.findall(r"\(param_1 \+ (0xe0[0-9a-f]+)\) = ([^;]+);", c):
        o = int(off, 16) - BASE
        if o < 0:
            continue
        idx, field = divmod(o, 0x1C)
        fields[idx][field] = val.strip()
    rows = []
    for idx in sorted(fields):
        f = fields[idx]
        if f.get(8) != "1":
            continue
        kind = int(f.get(0xC, "0"), 0)
        hi = f32(f[0x14]) if 0x14 in f else None
        lo = f32(f[0x10]) if 0x10 in f else 0.0
        rows.append({"index": idx, "kind": kind, "min": lo, "max": hi, "virtual": f.get(9) == "1",
                     "fields": {hex(k): v for k, v in sorted(f.items())}})
    return {"setters": {x: code[x]["name"] for x in s}, "builder": s[0], "rows": rows}


def main(root, outdir):
    P = json.load(open(os.path.join(outdir, "params.json")))
    res = {}
    for slug, dev in SLUGS.items():
        t = corpus(root, slug) if slug == "Corpus" else aas(root, slug)
        idx = [r["index"] for r in t["rows"]]
        t["summary"] = {"entries": len(t["rows"]), "distinct_indices": len(set(idx)),
                        "index_range": [min(idx), max(idx)], "by_kind": dict(collections.Counter(r["kind"] for r in t["rows"])),
                        "virtual": sum(r["virtual"] for r in t["rows"]), "xml_params": len(P[dev]["params"])}
        def norm(lo, hi):
            return f"{lo:g}..{hi:g}"
        bundle_ranges = collections.Counter(norm(r["min"], r["max"]) for r in t["rows"]
                                            if r["max"] is not None and r["min"] is not None and (r["min"], r["max"]) != (0.0, 1.0))
        t["summary"]["unparsed_range"] = sum(r["min"] is None or r["max"] is None for r in t["rows"])
        xml_ranges = collections.Counter()
        for path, a in P[dev]["params"].items():
            rng = a.get("MidiControllerRange.pair")
            if rng and a["declared_class"]["top"][0][0] != "TimeableBool":
                lo, hi = (float(x) for x in rng["top"][0][0].split(".."))
                if (lo, hi) != (0.0, 1.0):
                    xml_ranges[norm(lo, hi)] += 1
        t["range_comparison"] = {"bundle_non_unit": dict(sorted(bundle_ranges.items())),
                                 "xml_non_unit": dict(sorted(xml_ranges.items())),
                                 "only_bundle": dict(sorted((bundle_ranges - xml_ranges).items())),
                                 "only_xml": dict(sorted((xml_ranges - bundle_ranges).items()))}
        res[slug] = {"xml_element": dev, **t}
    json.dump(res, open(os.path.join(outdir, "param_tables.json"), "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
