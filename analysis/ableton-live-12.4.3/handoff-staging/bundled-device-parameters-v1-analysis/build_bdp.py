"""Stage the bundled-device-parameters-v1 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3.13 and -I from any directory:
  python3 -I build_bdp.py build          # spec tables, fixtures/, cases.json, manifest.json (files[] empty)
  python3 -I build_bdp.py seal           # evidence re-check, cross-check, manifest files[], validation, trace
  python3 -I build_bdp.py verify <dir>   # hashes, inventory, links, deny list of an exported copy

Inputs (read only): the H4, N5 and N6 run outputs named in EVIDENCE, and for the seal-time re-check the
shipped device presets of the 12.4.3 bundle. No shipped byte is copied into the payload: fixtures are written
from the parameter tables with values computed here. README.md, AGENTS.md and the prose of spec.md are
hand-written; build replaces only the body of its "## Parameter tables" section.
Dependencies: cases.py (case table), crosscheck_model.py (independent reader of the payload), trace.py.
"""
import hashlib, json, re, struct, sys
from pathlib import Path

sys.dont_write_bytecode = True  # leave no __pycache__ next to the analyst files

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "bundled-device-parameters-v1"
R2 = ROOT / "analysis/ableton-live-12.4.3/r2"
H4, N5, N6 = R2 / "h4-devices-v1/out", R2 / "n5-device-mapping-v1/out", R2 / "n6-device-tables-v1/out"
EVIDENCE = {  # path -> SHA-256 recorded in the run manifests
    H4 / "schema_devices.json": "063925312adf93a1aca808897dbb06823a54337f095a2d23754aed3085c04fa2",
    H4 / "param_table.tsv": "51610b71146369215ea48006c2c9243fc9811fd4316f905d5b71acfb666141c7",
    H4 / "fields.json": "ef354a03aa4304073a1f836b677e23aec5b32d921caa928cedce6fdbd75af95f",
    N5 / "conversions.tsv": "4faec668bfd8f86fc14c6c29a4651c92d99284d83d53e1a506e28b2445448cbe",
    N6 / "conversions.tsv": "3fd82068ee78c017beb340583c41b5f99deca1fab7903fce76fb1ccc4bf2626c",
    N6 / "loader_slots.txt": "b0242aa24478eb095105394e45ec98a36d93ab6b7888963fc1b42746ff4e21b2",
    N6 / "nonparam_fields.tsv": "4d590e1b1bb60af7d0573ae92a08d9625fe4041cdc36f347f0cbcaa5eee6c1e7",
    ROOT / "analysis/ableton-live-12.4.3/derived/Live.arm64": "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad",
}
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
DEVICES = [("Amp", "Amp"), ("Cabinet", "Cabinet"), ("Analog", "UltraAnalog"), ("Tension", "StringStudio"),
           ("Collision", "Collision"), ("Electric", "LoungeLizard"), ("Corpus", "Corpus")]
KIND = {"TimeableFloat": "Float", "TimeableEnum": "Enum", "TimeableBool": "Bool",
        "RemoteableInt": "Plain integer", "RemoteableString": "Plain text", "RemoteableBool": "Plain Boolean"}
LABELS = {  # released subset of REQ-014 (N5 conversions.tsv labels; constructor string order re-read 2026-10-18)
    "Amp": {"AmpType": ["Clean", "Boost", "Blues", "Rock", "Lead", "Heavy", "Bass"]},
    "Cabinet": {"CabinetType": ["1x12", "2x12", "4x12", "4x10", "4x10 Bass"],
                "MicrophonePosition": ["Near On-Axis", "Near Off-Axis", "Far"]},
    # review 2026-10-18: MicrophoneTypeSwitch labels excluded (draft order false/true reversed by the review's reading)
    "LoungeLizard": {"PickupModel": ["R", "W"]},
    "Corpus": {"ResonanceType": ["Beam", "Marimba", "String", "Membrane", "Plate", "Pipe", "Tube"],
               "ResonatorQuality": ["Eco", "Low", "Med", "High"], "MidiMode": ["Last", "Low"]},
}
ROOT_ATTRS = [("MajorVersion", "5"), ("MinorVersion", "12.0_12402"), ("SchemaChangeCount", "1")]
# review 2026-10-18: REQ-015 position parameters keep their table rows; their values are never graded
POSITION = {("Corpus", p) for p in ("ExcitationX", "ListeningXL", "ListeningXR")} | \
           {("Collision", f"Resonator{i}/{p}") for i in (1, 2) for p in ("HitX", "ListeningXL", "ListeningXR")}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def fnum(x):
    """Plain decimal text of an exactly representable number: integers without a fraction."""
    return str(int(x)) if float(x) == int(x) else repr(float(x))


# ---- tables from the evidence ----
def load_tables():
    """-> {element: [member dict]} in document order. Member: path, kind, lo, hi, whole, value (plain fields)."""
    cur = json.loads((H4 / "schema_devices.json").read_text())["current"]
    rng = {}
    for row in (H4 / "param_table.tsv").read_text().splitlines()[1:]:
        c = row.split("\t")
        rng[(c[0], c[1])] = (c[2], c[8])
    whole = set()
    for row in (N5 / "conversions.tsv").read_text().splitlines()[1:]:
        c = row.split("\t")
        if c[3] in ("legacyint", "quantizing"):
            whole.add((c[0], c[2]))
    for row in (N6 / "conversions.tsv").read_text().splitlines()[1:]:
        c = row.split("\t")
        if c[3] == "TimeableFloat" and re.match(r"(legacyint|quantizing)\(", c[5]) and "not stored" not in c[4]:
            whole.add((c[0], c[2]))
    fields = json.loads((H4 / "fields.json").read_text())
    tables = {}
    for _, el in DEVICES:
        rows = []
        for path, cls in cur[el]:
            m = {"path": path, "kind": KIND[cls]}
            if cls.startswith("Timeable"):
                pcls, r = rng[(el, path)]
                assert pcls == cls, (el, path)
                if m["kind"] != "Bool":
                    lo, hi = (float(v) for v in re.fullmatch(r"(-?[\d.]+)\.\.(-?[\d.]+)", r).groups())
                    m.update(lo=lo, hi=hi)
                m["whole"] = (el, path) in whole
            else:
                m["value"] = fields[el][path]["top"][0][0]  # modal shipped value (D)
            rows.append(m)
        tables[el] = rows
    n_whole = sum(m.get("whole", False) for rows in tables.values() for m in rows)
    assert n_whole == 28, n_whole
    return tables


def params(rows):
    return [m for m in rows if m["kind"] in ("Float", "Enum", "Bool")]


# ---- payload tables (spliced into spec.md) ----
def table_md(tables):
    out = ["The tables list every member of each device element in document order. Kinds and domains are",
           "defined in REQ-BUNDLED-DEVICE-PARAMETERS-003 and REQ-BUNDLED-DEVICE-PARAMETERS-006. In the note column,",
           "\"whole numbers\" marks the parameters of REQ-BUNDLED-DEVICE-PARAMETERS-007 and \"labels\" the",
           "parameters of REQ-BUNDLED-DEVICE-PARAMETERS-014. \"position\" marks the parameters of",
           "REQ-BUNDLED-DEVICE-PARAMETERS-015, whose values have no expectation in this release.",
           "For a plain field the third column gives the `Value` text that documents of this format version",
           "store and that the fixtures use.", ""]
    for name, el in DEVICES:
        rows = tables[el]
        out += [f"### {name} (`{el}`)", "",
                f"{len(params(rows))} parameters" + (f" and {len(rows) - len(params(rows))} plain fields." if
                                                     len(rows) > len(params(rows)) else "."), "",
                "| Path below the device element | Kind | Domain or stored value | Note |", "| --- | --- | --- | --- |"]
        for m in rows:
            if m["kind"] == "Float" or m["kind"] == "Enum":
                dom = f"{fnum(m['lo'])}..{fnum(m['hi'])}"
            elif m["kind"] == "Bool":
                dom = "false, true"
            else:
                dom = f"`\"{m['value']}\"`"
            note = "whole numbers" if m.get("whole") else "labels" if m["path"] in LABELS.get(el, {}) else \
                "position" if (el, m["path"]) in POSITION else ""
            out.append(f"| `{m['path']}` | {m['kind']} | {dom} | {note} |")
        out.append("")
    return "\n".join(out)


def splice_tables(tables):
    p = STAGE / "spec.md"
    text = p.read_text()
    head, sep, rest = text.partition("## Parameter tables\n")
    assert sep, "spec.md lacks the Parameter tables heading"
    nxt = rest.index("\n## ")
    p.write_text(head + sep + "\n" + table_md(tables) + rest[nxt:])


# ---- fixtures ----
class N:
    def __init__(self, tag, attrs=(), kids=None, group=False):
        self.tag, self.attrs, self.kids, self.group = tag, list(attrs), kids if kids is not None else [], group

    def lines(self, d=0):
        ind = "  " * d
        a = "".join(f' {k}="{v.replace("&", "&amp;").replace("<", "&lt;").replace(chr(34), "&quot;")}"'
                    for k, v in self.attrs)
        if not self.kids:
            return [f"{ind}<{self.tag}{a} />"]
        return [f"{ind}<{self.tag}{a}>"] + [x for k in self.kids for x in k.lines(d + 1)] + [f"{ind}</{self.tag}>"]

    def clone(self):
        return N(self.tag, self.attrs, [k.clone() for k in self.kids], self.group)


def V(tag, value):
    return N(tag, [("Value", value)])


def target(tag):
    return N(tag, [("Id", "0")], [V("LockEnvelope", "0")])


def param_node(tag, m, text):
    lo_hi = lambda t: N(t, kids=[V("Min", fnum(m["lo"])), V("Max", fnum(m["hi"]))])
    if m["kind"] == "Float":
        kids = [V("LomId", "0"), V("Manual", text), lo_hi("MidiControllerRange"), target("AutomationTarget"),
                target("ModulationTarget")]
    elif m["kind"] == "Enum":
        kids = [V("LomId", "0"), V("Manual", text), target("AutomationTarget"), lo_hi("MidiControllerRange")]
    else:
        kids = [V("LomId", "0"), V("Manual", text), target("AutomationTarget"),
                N("MidiCCOnOffThresholds", kids=[V("Min", "64"), V("Max", "127")])]
    return N(tag, kids=kids)


def device_tree(el, rows, texts):
    root = N(el)
    for m in rows:
        *groups, leaf = m["path"].split("/")
        parent = root
        for g in groups:
            nxt = next((k for k in parent.kids if k.tag == g and k.group), None)
            if nxt is None:
                nxt = N(g, group=True)
                parent.kids.append(nxt)
            parent = nxt
        parent.kids.append(param_node(leaf, m, texts[m["path"]]) if "value" not in m else V(leaf, m["value"]))
    return root


def find(node, path):
    for part in path.split("/"):
        node = next(k for k in node.kids if k.tag == part)
    return node


def document(dev_node):
    a = "".join(f' {k}="{v}"' for k, v in ROOT_ATTRS)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', f"<Ableton{a}>"] + dev_node.lines(1) + ["</Ableton>"]
    return ("\n".join(lines) + "\n").encode("ascii")


# ---- values ----
def value_of(m, mode, i):
    """Numeric value of a parameter in a mid, min or max fixture (exactly representable in binary32)."""
    if m["kind"] == "Bool":
        return {"min": False, "max": True}.get(mode, i % 2 == 0)
    lo, hi = m["lo"], m["hi"]
    if mode in ("min", "max"):
        v = lo if mode == "min" else hi
    elif m["kind"] == "Enum":
        v = (int(hi) + 1) // 2
    else:
        v = lo + ((hi - lo) // 4 if m["whole"] else (hi - lo) / 4)
    if m["kind"] == "Enum":
        return int(v)
    assert f32(v) == v
    return float(v)


def text_of(v):
    return ("true" if v else "false") if isinstance(v, bool) else fnum(v)


def base_values(rows, mode):
    """Bool parameters alternate true, false, ... in table order in the mid fixture."""
    bools = [m["path"] for m in params(rows) if m["kind"] == "Bool"]
    return {m["path"]: value_of(m, mode, bools.index(m["path"]) if m["kind"] == "Bool" else 0) for m in params(rows)}


def state_json(v):
    return v if isinstance(v, (bool, int)) else f32(v)


# ---- build ----
def build():
    sys.path.insert(0, str(HERE))
    import cases as C
    tables = load_tables()
    splice_tables(tables)
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    for old in (STAGE / "fixtures").glob("*.xml"):
        old.unlink()
    out = []
    for c in C.cases(tables, sys.modules[__name__]):
        el, rows = c["device"], tables[c["device"]]
        vals = base_values(rows, c["base"])
        vals.update(c.get("values", {}))
        texts = {p: text_of(v) for p, v in vals.items()}
        texts.update(c.get("texts", {}))
        tree = device_tree(el, rows, texts)
        for edit in c.get("edits", []):
            edit(tree)
        rel = f"fixtures/{c['id']}.xml"
        (STAGE / rel).write_bytes(document(tree))
        exp = {"outcome": c["outcome"]}
        if c["outcome"] == "opens":
            keys = [k for k in c.get("state_keys") or [m["path"] for m in params(rows)] if (el, k) not in POSITION]
            exp["state"] = {k: (c["state"][k] if k in c.get("state", {}) else state_json(vals[k])) for k in keys}
            if c.get("labels"):
                exp["labels"] = c["labels"]
        comparator = "outcome exact" + ("; listed state keys exact" if "state" in exp else "") + \
                     ("; listed labels exact text" if "labels" in exp else "")
        out.append({"id": c["id"], "kind": c["kind"], "purpose": c["purpose"],
                    "requirements": [f"REQ-BUNDLED-DEVICE-PARAMETERS-{r}" for r in c["reqs"]],
                    "device": el, "input": rel, "action": "open", "expected": exp,
                    "expectation_provenance": c["prov"], "reference_execution": "not-run",
                    "candidate_execution": "not-run", "comparator": comparator})
    doc = {"schema": "bundled-device-parameters-cases-v1", "target": TARGET,
           "scope": "bundled-device-parameters-v1 partial requirement clauses only (see spec.md)",
           "status": "released-reviewed",
           "fixture_origin": "Independently authored device presets written from the parameter tables; no shipped file copied or excerpted",
           "oracle_status": "Documented and static-derived expectations; neither reference nor candidate executed",
           "representation": {
               "paths": "below the device element; groups joined by /",
               "action": "open: open the device preset in a fresh state",
               "outcome": "opens or refused",
               "state": "parameter values read when the preset opens; only listed keys are judged. Float: JSON number equal to the binary32 value; Enum: integer; Bool: true or false",
               "labels": "text the user interface shows for the listed parameter's value; exact",
               "note": "project comparison representation, not an API of the original application or a required design"},
           "cases": out}
    (STAGE / "cases.json").write_text(json.dumps(doc, indent=1, ensure_ascii=True) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(C.manifest_meta(len(out), TARGET), indent=1) + "\n")
    print(len(out), "cases staged")


# ---- checks ----
DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"FUN_", r"DAT_", r"disassembl", r"decompil",
        r"pseudocode", r"Ghidra", r"vtable", r"dossier", r"\bcorpus", r"constructor", r"\bloader", r"post-load",
        r"convert", r"registr", r"\bslot", r"descriptor", r"Timeable", r"Remoteable", r"\bA(?:Amp|Cabinet|UltraAnalog|StringStudio|Collision|LoungeLizard|Corpus)\b",
        r"SNewCompound", r"[Ss]chema (?:order|file|field|class)", r"Schema/", r"\bbundles?\b", r"Softube", r"Tassman",
        r"ToggleDummy", r"IsChain2", r"DummyPerNote", r"GetPlugInfo", r"SetParameter", r"legacyint", r"quantiz",
        r"Core Library", r"Defaults/", r"App-Resources", r"Contents/", r"Pipe Resonator", r"Clean\.adv",
        r"\b[HNSD]\d\b", r"\bP4-", r"PRB-", r"\bQ-0\d", r"\bA[1-3]\b", r"\bI\d\b", r"\bBDP-\d", r"\bF[1-7]\b",
        r"ev_[0-9a-f]", r"derivation", r"traceab", r"handoff-staging", r"Live\.arm64", r"/home/", r"/var/",
        r"/tmp/", r"[Pp]ython", r"[Ee]xpat", r"strto", r"from_chars", r"\+0x", r"build_bdp", r"crosscheck",
        r"\bmodal\b", r"1,064|3,634|37,794|13,618|114,570"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}


def payload(d):
    return sorted(p for p in Path(d).rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md, root):
    out = []
    for t in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        if re.match(r"[a-z]+:", t):
            out.append((t, "external URL not allowed"))
            continue
        path, _, anchor = t.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = dest.is_file() and root.resolve() in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((t, "ok" if ok else "UNRESOLVED"))
    return out


def verify(d):
    d = Path(d)
    man = json.loads((d / "manifest.json").read_text())
    files = payload(d)
    mism = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
            or sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inv = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    link_rows = {str(p.relative_to(d)): links(p, d) for p in d.glob("*.md")}
    bad = {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    missing = [c["input"] for c in cases if not (d / c["input"]).is_file()]
    deny = {}
    for p in [*files, d / "manifest.json"]:
        text = p.read_text()
        hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mism,
            "inventory_differences": inv, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad, "missing_case_inputs": missing, "deny_list_hits": deny,
            "symlinks": [str(p) for p in d.rglob("*") if p.is_symlink()]}


def seal():
    sys.path.insert(0, str(HERE))
    import crosscheck_model as X, trace as T
    ident = {str(p.relative_to(ROOT)): {"sha256": sha(p.read_bytes()), "recorded": h,
                                        "match": sha(p.read_bytes()) == h}
             for p, h in EVIDENCE.items()}
    assert all(v["match"] for v in ident.values()), ident
    recheck = T.recheck_shipped(load_tables())
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    model = X.Model(STAGE / "spec.md")
    problems, fixtures = {}, {}
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        errs = X.compare(model, raw, c["expected"])
        if not raw.isascii() or b"\r" in raw or b"\t" in raw or not raw.endswith(b"\n"):
            errs.append("not ASCII with LF endings, no tabs and a final newline")
        if errs:
            problems[c["id"]] = errs
        fixtures[c["id"]] = {"bytes": len(raw), "lines": raw.count(b"\n"), "sha256": sha(raw)}
    dup_inputs = len({f["sha256"] for f in fixtures.values()}) != len(fixtures)
    for doc in ("README.md", "spec.md"):
        if f"{len(cases)} cases" not in (STAGE / doc).read_text() or f"All {len(cases)} fixtures" not in \
                (STAGE / "spec.md").read_text():
            problems[doc] = [f"case count {len(cases)} not stated"]
    probes = X.self_test(model, STAGE, cases)
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "bundled-device-parameters-v1 (staged candidate)",
              "python": sys.version.split()[0], "evidence_identity": ident, "shipped_recheck": recheck,
              "spec_page_crosscheck": T.spec_page_diff(load_tables()), "cases": len(cases),
              "case_problems": problems, "duplicate_inputs": dup_inputs, "model_probes": probes,
              "fixtures": fixtures, **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model reads the "
                        "payload's own tables and restates the same static evidence; it is not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    tr = T.traceability(cases)
    (HERE / "traceability.json").write_text(json.dumps(tr, indent=1) + "\n")
    keys = ("cases", "case_problems", "duplicate_inputs", "payload_files", "hash_or_size_mismatches",
            "inventory_differences", "unresolved_links", "missing_case_inputs", "deny_list_hits", "manifest_sha256")
    print(json.dumps({k: report[k] for k in keys}, indent=1))
    print(json.dumps({"probes_failed": [p for p in probes if not p["ok"]],
                      "recheck_failures": recheck.get("failures"),
                      "spec_page_differences": len(report["spec_page_crosscheck"])}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
