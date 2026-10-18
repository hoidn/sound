"""Analyst-only evidence for bundled-device-parameters-v1: traceability, shipped re-check, draft cross-check.

recheck_shipped(tables): re-reads (read only) every shipped .adv that holds one of the seven devices and checks
the documented facts the payload states: placement, member order, fixture form, plain field values, domains.
spec_page_diff(tables): compares the payload tables with the draft spec page tables (classes, domains, steps).
traceability(cases): case -> draft source, evidence keys and inferred links; clause -> evidence.
"""
import gzip, itertools, json, re
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
H4 = ROOT / "analysis/ableton-live-12.4.3/r2/h4-devices-v1"
SPEC_PAGE = ROOT / "wiki/specs/bundled-device-parameters.md"
SHAPE = {"Float": ["LomId", "Manual", "MidiControllerRange", "AutomationTarget", "ModulationTarget"],
         "Enum": ["LomId", "Manual", "AutomationTarget", "MidiControllerRange"],
         "Bool": ["LomId", "Manual", "AutomationTarget", "MidiCCOnOffThresholds"]}


def fnum(x):
    return str(int(x)) if float(x) == int(x) else repr(float(x))


def recheck_shipped(tables):
    app = Path(json.loads((H4 / "manifest.json").read_text())["inputs"]["app_resources"])
    if not app.is_dir():
        return {"status": "not run: application resources absent"}
    occ = [json.loads(l) for l in (H4 / "out/occurrences.jsonl").read_text().splitlines()]
    docs = sorted({o["doc"] for o in occ if o["ext"] == ".adv" and o["device"] in tables})
    base = {n for n, _ in json.loads((H4 / "out/schema_devices.json").read_text())["device_base_prefix"]}
    n = {"documents": len(docs), "parameters": 0, "range_differs_from_domain": 0, "fractional_whole": 0,
         "manual_outside_domain": 0}
    failures = []
    for d in docs:
        root = ET.fromstring(gzip.open(app / d).read())
        dev = root[0]
        if len(root) != 1 or dev.tag not in tables:
            failures.append(f"{d}: root children")
            continue
        rows = {m["path"]: m for m in tables[dev.tag]}
        order = []

        def walk(node, pre):
            for c in node:
                p = pre + c.tag
                if p in rows:
                    order.append(p)
                    yield p, c
                elif not pre and c.tag in base:
                    continue
                elif not len(c):
                    failures.append(f"{d}: unlisted element {p}")
                else:
                    if c.attrib:
                        failures.append(f"{d}: group {p} has attributes")
                    yield from walk(c, p + "/")
        for p, c in list(walk(dev, "")):
            m = rows[p]
            if "value" in m:
                if dict(c.attrib) != {"Value": m["value"]} or len(c):
                    failures.append(f"{d}: plain {p} = {c.attrib}")
                continue
            n["parameters"] += 1
            kids = list(c)
            if [k.tag for k in kids] != SHAPE[m["kind"]] or c.attrib:
                failures.append(f"{d}: shape {p}")
                continue
            if kids[0].attrib != {"Value": "0"} or any(k.tag.endswith("Target") and (k.attrib != {"Id": "0"} or
               [(x.tag, x.attrib) for x in k] != [("LockEnvelope", {"Value": "0"})]) for k in kids):
                failures.append(f"{d}: LomId or target form {p}")
            rng = next(k for k in kids if k.tag.startswith("Midi"))
            want = ["64", "127"] if m["kind"] == "Bool" else [fnum(m["lo"]), fnum(m["hi"])]
            if [x.get("Value") for x in rng] != want:
                n["range_differs_from_domain"] += 1
            t = kids[1].get("Value")
            if m["kind"] == "Bool":
                if t not in ("true", "false"):
                    failures.append(f"{d}: Bool text {p} {t!r}")
            else:
                v = float(t)
                n["manual_outside_domain"] += not m["lo"] <= v <= m["hi"]
                n["fractional_whole"] += bool(m.get("whole")) and v != int(v)
        if order != [m["path"] for m in tables[dev.tag]]:
            failures.append(f"{d}: member set or order differs")
    return {"status": "run", "app_resources": str(app), "counts": n, "failures": failures,
            "note": "range_differs_from_domain counts unmapped occurrences with a narrower stored range (draft REQ-006 U part); "
                    "these documents are not fixtures"}


def spec_page_diff(tables):
    """Rows of the draft spec page tables that disagree with the payload tables (class, domain, whole steps)."""
    text = SPEC_PAGE.read_text().split("## Parameter tables", 1)[1].split("\n## Timing", 1)[0]
    page = {}
    for el, body in re.findall(r"^### \w+ \(`(\w+)`\)\n(.*?)(?=^### |\Z)", text, re.M | re.S):
        for path, kind, dom in re.findall(r"^\| `([^`]+)` \| (\w+) \| ([^|]+?) \|", body, re.M):
            parts = [p.split(",") for p in re.findall(r"\{([^}]*)\}", path)]
            for combo in itertools.product(*parts) if parts else [()]:
                it = iter(combo)
                page[(el, re.sub(r"\{[^}]*\}", lambda _: next(it), path))] = (kind, dom.strip())
    diffs = []
    for el, rows in tables.items():
        mine = {}
        for m in rows:
            if m["kind"] in SHAPE:
                dom = "true/false" if m["kind"] == "Bool" else f"{fnum(m['lo'])}..{fnum(m['hi'])}"
                mine[(el, m["path"])] = (m["kind"], dom + (", integer steps" if m.get("whole") else ""))
        for k in sorted(set(mine) | {k for k in page if k[0] == el}):
            if mine.get(k) != page.get(k):
                diffs.append({"device": el, "path": k[1], "payload": mine.get(k), "draft_page": page.get(k)})
    return diffs


EV = {
    "names": "H4 out/occurrences.jsonl (device element per occurrence, ext, devices_depth); out/scan.json; out/live_strings.json",
    "placement": "H4 out/occurrences.jsonl (.adv rows); seal-time recheck: each shipped .adv with one of the seven devices has it as the root's only child",
    "members": "H4 out/schema_devices.json current[element] for 12.0_12402 (paths, classes, order); out/params.json distinct_param_path_sets = 1; recheck of order in all shipped .adv",
    "shape": "H4 out/param_table.tsv classes; recheck of child order, LomId 0, target Id 0, LockEnvelope 0 and thresholds 64/127 in shipped .adv",
    "domains": "H4 out/param_table.tsv range column (modal unmapped MidiControllerRange); out/checks.txt 'no Manual value outside the modal unmapped range'; N6 conversions_nested.py; N5 constructor arguments",
    "whole": "N5 out/conversions.tsv class legacyint or quantizing; N6 out/conversions.tsv user_converter legacyint(...) or quantizing(...); H4 param_table.tsv kinds int",
    "float_text": "N1 n1-0006 0x10152bfb8 float branch (Invalid by length 7, '#' by length 9, else strtod with a no-consumption throw, then (float)); N6 out/loader_slots.txt; transport-state-v1 REQ-004/005",
    "enum_text": "N1 n1-0006 0x1002fd908 integer text rule; converter 0x1002fda78 confirmed by the transport-state-v1 reviewer; the TimeSignature Manual is the Manual class of every Enum parameter (N1, ATimeableEnum)",
    "bool_text": "N1 n1-0006 0x10152bfb8 bool branch; 0x10152bf4c length and memcmp",
    "parse_typed": "N1 transport-state-native native reading steps 1-3: 0x1015299e0 looks up child names among the class fields (0x10152ac0c); attribute text converted by base type at parse time",
    "dup": "N1 n1-0007 add slot 0x101472624 'Class {} already has member {}' with corrupt-document key 0x10148229c",
    "unknown": "N1 0x1015299e0: unknown child of a compound skipped with its subtree; 'Unexpected node' record 0x101453aac built, not thrown; transport-state-v1 REVIEW (TS-016 ruling, RV1-06)",
    "loader": "N6 out/loader_slots.txt (ATimeableFloat/Enum/Bool and every device and group class: 0x101487310 at +0x140); Amp re-read 2026-10-18: SNewCompound<AAmp> 0x1030b42e8 -> FUN_1030b4934 stores vtable 0x1068bff78; +0x140 = 0x101487310, +0xd0 = 0x1023a3b14 (N6 extract_nested.Image, Live.arm64 3a99ceea...)",
    "post_load": "device post-load 0x1023a3b14 (corpus: calls 0x10248857c; resets +0x1cc from INT_MIN to 0); group post-load 0x101486fa8; Timeable post-load 0x1026fc4cc, no range test (N6 page)",
    "plain": "H4 out/fields.json modal values; N6 out/nonparam_fields.tsv constructor values; recheck of plain values in shipped .adv",
    "labels": "N5 out/conversions.tsv labels; corpus string order re-read 2026-10-18 in FUN_1030b4934 (Amp), FUN_1030c9c90 (Cabinet), FUN_1030e9578 (Electric), FUN_1030e277c (Corpus)",
    "ids": "H4 out/params.json AutomationTarget.IdIsZero.adv; H4 page target counts; recheck",
    "refusal": "N1: read errors throw with corrupt-document key 0x10148229c; preset open command and catch untraced (I1)",
}
INFERRED = {
    "I1": "A read error anywhere in a device preset stops the preset from opening (preset open command and catch site untraced; same reader as Live Sets, whose catch als-container-v1 RVA-01 confirmed)",
    "I2": "The root-position device element is created through its class by name and read by the generic member reader; with every member present the untraced create path (Q-006, draft A1) cannot change a value read",
    "I3": "No device-level post-load step changes a value read (device post-load 0x1023a3b14 traced one level)",
    "I4": "The REQ-014 label lists are the texts the user interface shows (draft A3); Corpus LfoType, LfoSync and LfoStereoMode, which carry a second name list in the same constructor, are excluded",
    "I5": "Absence of the members shared by all devices does not change a judged outcome; the comparison obligation inserts them for the reference",
    "I6": "No class involved registers a member named Foo",
}
CLAUSES = {
    "001": ["names", "placement"], "002": ["members", "dup", "parse_typed"], "003": ["shape", "ids"],
    "004": ["float_text", "enum_text", "bool_text", "parse_typed", "refusal"], "006": ["domains", "loader", "post_load"],
    "007": ["whole"], "011": ["unknown", "plain", "parse_typed"], "012": ["ids"], "014": ["labels"],
}


def traceability(cases):
    import cases as C, build_bdp as B
    internal = {c["id"]: c for c in C.cases(B.load_tables(), B)}
    out = {}
    for c in cases:
        reqs = [r[-3:] for r in c["requirements"]]
        ev = sorted({k for r in reqs for k in CLAUSES[r]})
        inf = ["I5"] + (["I1"] if c["expected"]["outcome"] == "refused" else ["I2", "I3"])
        inf += ["I4"] if "014" in reqs else []
        inf += ["I6"] if "011" in reqs and "Foo" in c["purpose"] else []
        out[c["id"]] = {"source": internal[c["id"]]["src"], "evidence": ev, "inferred": sorted(inf)}
    return {"schema": "bundled-device-parameters-traceability-v1", "spec": "SPEC-BUNDLED-DEVICE-PARAMETERS r1",
            "evidence": EV, "inferred_links": INFERRED, "clauses": CLAUSES, "cases": out,
            "draft_cases_not_released": {
                "BDP-002, 003, 031, 032": "save output (REQ-005 and P4-H4-01)",
                "BDP-014, 015, 016, 017": "out-of-range handling (REQ-010, P4-H4-02, PRB-N1-06)",
                "BDP-018 to 027": "defaults when absent (REQ-008; create path A1 open in Q-006)",
                "BDP-028": "fractional whole-number value (REQ-007 S(A1) and U parts)",
                "BDP-033": "target Id rule on save (REQ-012 U, P4-H4-01)",
                "BDP-034": "new-instance defaults (REQ-009, P4-H4-03, P4-N5-03)",
                "BDP-037": "position meaning (REQ-015, P4-N5-01, P4-N6-01)"}}
