"""Separate reviewer's check of the bundled-device-parameters-v1 candidate (handoff review; analyst side).

Run: python3 -I review_check.py [payload_dir]   (default: the staging payload). Writes review-check.json here.
Independent of the author's build_bdp.py, cases.py, crosscheck_model.py and trace.py (none is imported).
Reads, read only: the payload (spec.md, cases.json, fixtures/), every shipped .adv/.adg/.als/.alc under the
application resources recorded in the H4 run manifest, and the N5/N6 conversion tables (retained queries).
Checks: (1) tables vs shipped documents, (2) whole-number marks vs N5/N6 converters, (3) draft-error fields,
(4) every fixture's form and the deviations from the tables, (5) every expectation by the reviewer's own
reading of the contract rules, (6) fixture originality against shipped presets, (7) deny-list hygiene.
"""
import collections, gzip, json, os, re, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PAY = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[1] / "bundled-device-parameters-v1"
R2 = ROOT / "analysis/ableton-live-12.4.3/r2"
APP = Path(json.loads((R2 / "h4-devices-v1/manifest.json").read_text())["inputs"]["app_resources"])
DEV = ["Amp", "Cabinet", "UltraAnalog", "StringStudio", "Collision", "LoungeLizard", "Corpus"]
POSITION = {"Corpus": ["ExcitationX", "ListeningXL", "ListeningXR"],
            "Collision": [f"Resonator{i}/{p}" for i in (1, 2) for p in ("HitX", "ListeningXL", "ListeningXR")]}
# Label lists as the reviewer read them in the device constructors (decompiled corpus, 2026-10-18); enum lists
# are index-ordered. For the Bool switch the two-text converter returns its FIRST text for a nonzero value and
# parses the first text to 1.0 (convention confirmed at 20 other call sites, e.g. "On","Off"; "Inverted","Normal").
CTOR_LABELS = {"Amp": {"AmpType": ["Clean", "Boost", "Blues", "Rock", "Lead", "Heavy", "Bass"]},
               "Cabinet": {"CabinetType": ["1x12", "2x12", "4x12", "4x10", "4x10 Bass"],
                           "MicrophonePosition": ["Near On-Axis", "Near Off-Axis", "Far"],
                           "MicrophoneTypeSwitch": {True: "Dynamic", False: "Condenser"}},
               "LoungeLizard": {"PickupModel": ["R", "W"]},
               "Corpus": {"ResonanceType": ["Beam", "Marimba", "String", "Membrane", "Plate", "Pipe", "Tube"],
                          "ResonatorQuality": ["Eco", "Low", "Med", "High"], "MidiMode": ["Last", "Low"]}}
SHAPE = {"Float": ["LomId", "Manual", "MidiControllerRange", "AutomationTarget", "ModulationTarget"],
         "Enum": ["LomId", "Manual", "AutomationTarget", "MidiControllerRange"],
         "Bool": ["LomId", "Manual", "AutomationTarget", "MidiCCOnOffThresholds"]}


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def num(t):
    return float(t)


# ---------- payload contract ----------
def parse_spec(text):
    names = dict(re.findall(r"^\| (\w+) \| `(\w+)` \|$", text.split("### REQ-BUNDLED-DEVICE-PARAMETERS-001")[1]
                            .split("\n### ")[0], re.M))
    tab = text.split("\n## Parameter tables")[1].split("\n## ")[0]
    tables = {}
    for el, body in re.findall(r"^### \w+ \(`(\w+)`\)\n(.*?)(?=^### |\Z)", tab, re.M | re.S):
        rows = []
        for p, k, d, n in re.findall(r"^\| `([^`]+)` \| ([\w ]+?) \| (.+?) \| ?(.*?) ?\|$", body, re.M):
            r = {"path": p, "kind": k, "note": n.strip()}
            if k in ("Float", "Enum"):
                lo, hi = d.split("..")
                r.update(lo=lo, hi=hi)
            elif k != "Bool":
                r["value"] = d.strip('`"')
            rows.append(r)
        tables[el] = rows
    r14 = text.split("### REQ-BUNDLED-DEVICE-PARAMETERS-014")[1].split("\n## ")[0]
    labels = {}
    for name, path, rest in re.findall(r"^- (\w+) `([^`]+)`(?: \([^)]*\))?: (.+)\.$", r14, re.M):
        labels.setdefault(names[name], {})[path] = rest.split(", ")
    return names, tables, labels


# ---------- shipped documents ----------
def shipped_docs():
    for dp, _, fs in os.walk(APP):
        for f in fs:
            if f.endswith((".adv", ".adg", ".als", ".alc")):
                p = Path(dp) / f
                raw = p.read_bytes()
                yield p, gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def flatten(node, pre=""):
    """-> [(path, kind, info)] of a device element's content; kind Float/Enum/Bool/plain/empty."""
    out = []
    for c in node:
        p = pre + c.tag
        tags = [k.tag for k in c]
        if "Manual" in tags and "AutomationTarget" in tags:
            kind = "Float" if "ModulationTarget" in tags else "Bool" if "MidiCCOnOffThresholds" in tags else "Enum"
            rng = c.find("MidiCCOnOffThresholds" if kind == "Bool" else "MidiControllerRange")
            out.append((p, kind, {"tags": tags, "manual": c.find("Manual").get("Value"),
                                  "range": (rng.find("Min").get("Value"), rng.find("Max").get("Value")),
                                  "mapped": "KeyMidi" in tags, "lomid": c.find("LomId").get("Value"),
                                  "targets": [(t.get("Id"), [(x.tag, x.get("Value")) for x in t])
                                              for t in c if t.tag.endswith("Target")]}))
        elif not len(c):
            out.append((p, "plain" if set(c.attrib) == {"Value"} else "empty", {"value": c.get("Value")}))
        else:
            if c.attrib:
                out.append((p, "group-with-attributes", dict(c.attrib)))
            out += flatten(c, p + "/")
    return out


def check_shipped(tables):
    occ = collections.defaultdict(list)  # el -> [(ext, doc, element)]
    adv_root_ok, n_docs, n_with = [], 0, 0
    for p, raw in shipped_docs():
        n_docs += 1
        if not any(f"<{el}>".encode() in raw or f"<{el} ".encode() in raw for el in DEV):
            continue
        root = ET.fromstring(raw)  # every document holding a device parses; a failure would stop the check
        n_with += 1
        for el in DEV:
            for e in root.iter(el):
                occ[el].append((p.suffix, str(p.relative_to(APP)), e))
        if p.suffix == ".adv" and len(root) and root[0].tag in DEV:
            adv_root_ok.append(len(root) == 1)
    shared = set.intersection(*({c.tag for _, _, e in occ[el] for c in e} for el in DEV))
    res = {"documents_scanned": n_docs, "documents_with_devices": n_with, "occurrences": {el: len(v) for el, v in occ.items()},
           "adv_with_device_root_child": len(adv_root_ok), "adv_device_is_only_child": all(adv_root_ok),
           "shared_member_names": len(shared), "per_device": {}}
    for el in DEV:
        rows = tables[el]
        want = [(r["path"], r["kind"] if r["kind"] in SHAPE else "plain") for r in rows]
        d = {"adv": 0, "order_mismatch": [], "shared_not_prefix": 0, "shape_or_form": [], "adv_range_ne_domain": 0,
             "modal_unmapped_range_ne_domain": [], "plain_values_seen": {}, "bool_text_other": 0,
             "manual_outside_domain_adv": 0, "whole_marked_fractional_text": 0}
        modal = collections.defaultdict(collections.Counter)
        for ext, doc, e in occ[el]:
            kids = [c.tag for c in e]
            k = 0
            while k < len(kids) and kids[k] in shared:
                k += 1
            if any(t in shared for t in kids[k:]):
                d["shared_not_prefix"] += 1
            body = ET.Element(el)
            body.extend(list(e)[k:])
            flat = flatten(body)
            got = [(p, kind) for p, kind, _ in flat]
            if ext == ".adv":
                d["adv"] += 1
                if got != want:
                    d["order_mismatch"].append(doc)
            for p, kind, info in flat:
                r = next((x for x in rows if x["path"] == p), None)
                if r is None:
                    continue
                if kind == "plain":
                    d["plain_values_seen"].setdefault(p, collections.Counter())[f"{ext}:{info['value']}"] += 1
                    continue
                if kind not in SHAPE:
                    continue
                if not info["mapped"]:
                    modal[p][info["range"]] += 1
                if ext == ".adv":
                    if info["tags"] != SHAPE[kind] or info["lomid"] != "0" or any(
                            t != ("0", [("LockEnvelope", "0")]) for t in info["targets"]):
                        d["shape_or_form"].append(f"{doc}:{p}")
                    dom = ("64", "127") if kind == "Bool" else (r["lo"], r["hi"])
                    if kind == "Bool":
                        d["adv_range_ne_domain"] += info["range"] != dom
                    else:
                        d["adv_range_ne_domain"] += (num(info["range"][0]), num(info["range"][1])) != (num(r["lo"]), num(r["hi"]))
                    if kind == "Bool":
                        d["bool_text_other"] += info["manual"] not in ("true", "false")
                    else:
                        v = num(info["manual"])
                        d["manual_outside_domain_adv"] += not num(r["lo"]) <= v <= num(r["hi"])
                        d["whole_marked_fractional_text"] += r["note"] == "whole numbers" and not re.fullmatch(r"-?\d+", info["manual"])
        for r in rows:
            if r["kind"] in ("Float", "Enum"):
                top = modal[r["path"]].most_common(1)[0][0]
                if (num(top[0]), num(top[1])) != (num(r["lo"]), num(r["hi"])):
                    d["modal_unmapped_range_ne_domain"].append((r["path"], top))
            if "value" in r:
                adv_vals = {k.split(":", 1)[1] for k in d["plain_values_seen"].get(r["path"], {}) if k.startswith(".adv:")}
                if adv_vals != {r["value"]}:
                    d.setdefault("plain_adv_values_ne_table", []).append((r["path"], sorted(adv_vals)))
        d["plain_values_seen"] = {p: dict(c) for p, c in d["plain_values_seen"].items() if len(c) > 1}
        d["order_mismatch"] = d["order_mismatch"][:5]
        d["shape_or_form"] = d["shape_or_form"][:5]
        res["per_device"][el] = d
    # draft-error fields: names claimed stored in the draft that no document stores
    claim = {"Collision": ["PitchBendRangeRelativePosition", "SyncRateRelative"]}
    res["draft_claimed_fields_found"] = {n: sum(1 for _, _, e in occ["Collision"] for x in e.iter() if x.tag == n)
                                         for n in claim["Collision"]}
    res["corpus_sidechain"] = collections.Counter(
        (p, info.get("value")) for _, _, e in occ["Corpus"] for p, kind, info in flatten(e) if p.startswith("SideChain/"))
    res["corpus_sidechain"] = {f"{p} = {v!r}": n for (p, v), n in res["corpus_sidechain"].items()}
    return res, occ


def whole_from_converters():
    out = set()
    for row in (R2 / "n5-device-mapping-v1/out/conversions.tsv").read_text().splitlines()[1:]:
        c = row.split("\t")
        if c[3] in ("legacyint", "quantizing"):
            out.add((c[0], c[2]))
    for row in (R2 / "n6-device-tables-v1/out/conversions.tsv").read_text().splitlines()[1:]:
        c = row.split("\t")
        if c[3] == "TimeableFloat" and re.match(r"(legacyint|quantizing)\(", c[5]):
            out.add((c[0], c[2]))
    return out


# ---------- the reviewer's restatement of the released reading rules ----------
class NoExp(Exception):
    pass


FLOAT_PREFIX = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?")


def read_float(t):
    s = t.lstrip(" ")
    b = s[1:] if s[:1] in "+-" else s
    if (t and t[0] in "\t\n\r\f\v") or re.match(r"(?i)(0x|inf|nan)", b) or t == "Invalid" or t.startswith("#"):
        raise NoExp(t)
    m = FLOAT_PREFIX.match(s)
    if not m:
        return "refused"
    return f32(float(m.group(0)))


def read_enum(t):
    if re.fullmatch(r" *\+?[0-9]+", t) and len(t) <= 63:
        return int(t.strip(" +"))
    if re.fullmatch(r"[0-9]+ +", t):
        return int(t)
    if t.strip(" ") == "" or not t.isascii():
        return "refused"
    s = t.lstrip(" ")
    r = s[1:] if s.startswith("+") else s
    if r == "" or (s.startswith("+") and r.startswith("-")):
        return "refused"
    core = r.rstrip(" ")
    core = core[1:] if core.startswith("-") else core
    if any(c not in "0123456789" for c in core):
        return "refused"
    if not t.endswith(" ") and len(t) > 63:
        return "refused"
    raise NoExp(t)


def read_bool(t):
    return {"true": True, "1": True, "false": False, "0": False}.get(t, "refused")


def review_read(raw, rows):
    """-> ('refused', None, deviations) or ('opens', values, deviations); NoExp if the contract gives none."""
    dev_notes = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return "refused", None, [f"not well-formed: {e}"]
    assert root.tag == "Ableton" and dict(root.attrib) == {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                                          "SchemaChangeCount": "1"} and len(root) == 1
    dev = root[0]
    paths = {r["path"]: r for r in rows}
    groups = {"/".join(p.split("/")[:i]) for p in paths for i in range(1, p.count("/") + 1)}
    vals, refused = {}, []

    def walk(node, pre):
        expect = []
        for r in rows:
            if r["path"].startswith(pre):
                h = r["path"][len(pre):].split("/")[0]
                if h not in expect:
                    expect.append(h)
        seen = []
        for c in node:
            p = pre + c.tag
            if c.tag == "Foo":
                dev_notes.append(f"unknown Foo under {pre or 'device'} at child {list(node).index(c)}"
                                 + (f" with content {[k.tag for k in c]}" if len(c) else ""))
                continue
            if c.tag not in expect:
                raise NoExp(f"unlisted {p}")
            if c.tag in seen:
                dev_notes.append(f"duplicate {p}")
                if p in groups or paths[p]["kind"] in SHAPE:
                    refused.append(p)
                    continue
                raise NoExp(f"duplicate plain {p}")
            seen.append(c.tag)
            if p in groups:
                assert not c.attrib
                walk(c, p + "/")
            elif paths[p]["kind"] in SHAPE:
                r = paths[p]
                kids = [k for k in c if k.tag != "Foo"]
                if len(kids) < len(list(c)):
                    dev_notes.append(f"unknown Foo inside parameter {p} holding {[x.tag for k in c if k.tag == 'Foo' for x in k]}")
                tags = [k.tag for k in kids]
                if tags.count("Manual") == 2:
                    dev_notes.append(f"two Manual in {p}")
                    refused.append(p)
                    continue
                assert tags == SHAPE[r["kind"]] and not c.attrib, p
                lohi = ("64", "127") if r["kind"] == "Bool" else (r["lo"], r["hi"])
                rng = kids[-1] if r["kind"] != "Float" else kids[2]
                assert [(x.tag, x.attrib) for x in rng] == [("Min", {"Value": lohi[0]}), ("Max", {"Value": lohi[1]})], p
                assert kids[0].attrib == {"Value": "0"}
                for t in kids:
                    if t.tag.endswith("Target"):
                        assert t.attrib == {"Id": "0"} and [(x.tag, x.attrib) for x in t] == [("LockEnvelope", {"Value": "0"})]
                t = kids[1].get("Value")
                v = {"Float": read_float, "Enum": read_enum, "Bool": read_bool}[r["kind"]](t)
                if v == "refused":
                    dev_notes.append(f"{p} Manual {t!r} refused")
                    refused.append(p)
                    continue
                if r["kind"] != "Bool" and not num(r["lo"]) <= v <= num(r["hi"]):
                    raise NoExp(f"out of domain {p}")
                if r["note"] == "whole numbers" and v != int(v):
                    raise NoExp(f"fractional {p}")
                vals[p] = v
            else:
                assert dict(c.attrib) == {"Value": paths[p]["value"]} and not len(c), p
        if seen != expect:
            raise NoExp(f"order under {pre}")

    walk(dev, "")
    if len(refused) > 1:
        raise NoExp("more than one rule broken")
    return ("refused", None, dev_notes) if refused else ("opens", vals, dev_notes)


def text_form(raw):
    t = raw.decode("ascii")
    lines = t.split("\n")
    ok = t.endswith("\n") and "\r" not in t and "\t" not in t and lines[0] == '<?xml version="1.0" encoding="UTF-8"?>'
    ind = all(re.match(r"^( {2})*<", l) for l in lines[1:-1])
    return ok and ind


def check_cases(tables, labels_spec):
    cases = json.loads((PAY / "cases.json").read_text())["cases"]
    out, digests = {}, collections.Counter()
    base = {}
    for c in cases:
        raw = (PAY / c["input"]).read_bytes()
        digests[raw] += 1
        rows = tables[c["device"]]
        res = {"purpose": c["purpose"], "text_form_ok": text_form(raw)}
        try:
            outcome, vals, notes = review_read(raw, rows)
        except NoExp as e:
            res["NO_EXPECTATION_IN_REVIEW_READING"] = str(e)
            out[c["id"]] = res
            continue
        res["deviations"] = notes
        exp = c["expected"]
        errs = [] if outcome == exp["outcome"] else [f"outcome {outcome}"]
        if outcome == "opens":
            for k, v in exp.get("state", {}).items():
                if type(vals.get(k)) is not type(v) or vals.get(k) != v:
                    errs.append(f"state {k} reviewer {vals.get(k)!r} expected {v!r}")
            for k, v in exp.get("labels", {}).items():
                lab = labels_spec.get(c["device"], {}).get(k)
                mine = lab[int(vals[k])] if lab else None
                if mine != v:
                    errs.append(f"label {k} contract {mine!r} expected {v!r}")
                ctor = CTOR_LABELS[c["device"]][k]
                if (ctor[vals[k]] if isinstance(ctor, dict) else ctor[int(vals[k])]) != v:
                    errs.append(f"label {k} differs from the constructor reading: {ctor[vals[k]] if isinstance(ctor, dict) else ctor[int(vals[k])]!r}")
            pos = [k for k in exp.get("state", {}) if k in POSITION.get(c["device"], [])]
            if pos:
                res["position_keys_graded"] = pos
            res["state_keys"] = len(exp.get("state", {}))
            res["values_read"] = len(vals)
            if c["purpose"].startswith("Complete"):
                base[c["id"]] = (c["device"], vals)
        res["errors"] = errs
        out[c["id"]] = res
    return cases, out, sum(n > 1 for n in digests.values()), base


def originality(base, occ):
    """Max share of equal parameter values between a complete-device fixture and any shipped .adv of that device."""
    out = {}
    for cid, (el, vals) in base.items():
        best = (0.0, None)
        for ext, doc, e in occ[el]:
            if ext != ".adv":
                continue
            k = 0
            flat = {p: info for p, kind, info in flatten(e) if kind in SHAPE}
            same = sum(1 for p, v in vals.items() if p in flat and (
                (flat[p]["manual"] == "true") == v if isinstance(v, bool) else num(flat[p]["manual"]) == v))
            share = same / len(vals)
            if share > best[0]:
                best = (round(share, 3), doc.rsplit("/", 1)[-1])
        out[cid] = best[0]
    return out


DENY = [r"0x[0-9a-fA-F]{4,}", r"FUN_|DAT_|LAB_|PTR_", r"\bA[A-Z][a-z]+[A-Z]\w*", r"Timeable|Remoteable|SNew",
        r"[Dd]ecompil|[Dd]isassembl|[Pp]seudocode|Ghidra|vtable|dossier|typeinfo", r"\bP4-|PRB-|\bQ-0|\bN[1-9]\b|\bH4\b",
        r"analysis/|wiki/|raw/|handoff-staging|/home/|/var/|/tmp/", r"\.adv\b.*Core|Core Library|Defaults/",
        r"[Cc]onstructor|[Cc]onverter|[Ss]etParameter|[Bb]undle|Softube|engine index", r"\bA[1-3]\b|\bI[1-6]\b|\bF[1-8]\b|BDP-",
        r"[Ss]chema"]


def hygiene():
    hits = {}
    for p in sorted(PAY.rglob("*")):
        if p.is_file():
            t = p.read_text()
            h = sorted({m.group(0) for pat in DENY for m in re.finditer(pat, t)})
            if h:
                hits[str(p.relative_to(PAY))] = h
    vals = collections.Counter()
    for p in sorted((PAY / "fixtures").glob("*.xml")):
        vals.update(re.findall(r'(?:Value|Id|\w+Version|SchemaChangeCount)="([^"]*)"', p.read_text()))
    words = sorted(v for v in vals if re.search(r"[A-Za-z]", v))
    return hits, words


def main():
    spec = (PAY / "spec.md").read_text()
    names, tables, labels_spec = parse_spec(spec)
    report = {"payload": str(PAY), "app_resources": str(APP),
              "table_counts": {el: (sum(r["kind"] in SHAPE for r in t), sum(r["kind"] not in SHAPE for r in t))
                               for el, t in tables.items()}}
    shipped, occ = check_shipped(tables)
    report["shipped"] = shipped
    conv = whole_from_converters()
    marked = {(el, r["path"]) for el, t in tables.items() for r in t if r["note"] == "whole numbers"}
    report["whole_numbers"] = {"marked": len(marked), "converter_set_stored": len(conv & {(el, r["path"])
                               for el, t in tables.items() for r in t}),
                               "marked_not_in_converters": sorted(marked - conv),
                               "converter_stored_not_marked": sorted((conv & {(el, r["path"]) for el, t in tables.items()
                                                                         for r in t}) - marked)}
    report["labels_contract_vs_constructor"] = {
        f"{el}/{p}": ("same" if (CTOR_LABELS[el][p] == l if isinstance(CTOR_LABELS[el][p], list)
                                 else [CTOR_LABELS[el][p][False], CTOR_LABELS[el][p][True]] == l) else
                      f"DIFFERS: contract {l}, constructor false/true {CTOR_LABELS[el][p]}")
        for el, d in labels_spec.items() for p, l in d.items()}
    cases, res, dups, base = check_cases(tables, labels_spec)
    report["cases"] = res
    report["duplicate_fixtures"] = dups
    report["case_errors"] = {k: v["errors"] for k, v in res.items() if v.get("errors")}
    report["cases_without_review_expectation"] = [k for k, v in res.items() if "NO_EXPECTATION_IN_REVIEW_READING" in v]
    report["position_keys_graded"] = {k: v["position_keys_graded"] for k, v in res.items() if "position_keys_graded" in v}
    report["originality_max_equal_share"] = originality(base, occ)
    report["hygiene_hits"], report["fixture_text_values"] = hygiene()
    (HERE / "review-check.json").write_text(json.dumps(report, indent=1, default=str) + "\n")
    summary = {k: report[k] for k in ("table_counts", "whole_numbers", "labels_contract_vs_constructor", "duplicate_fixtures",
                                      "case_errors", "cases_without_review_expectation", "position_keys_graded",
                                      "originality_max_equal_share", "hygiene_hits", "fixture_text_values")}
    summary["shipped"] = {k: v for k, v in shipped.items() if k != "per_device"}
    summary["shipped_per_device"] = {el: {k: v for k, v in d.items() if v not in (0, [], {})}
                                     for el, d in shipped["per_device"].items()}
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
