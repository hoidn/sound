"""Reviewer's checks of the automation-envelopes-v2 candidate (analyst side, never shipped; output is data).

usage: TMPDIR=<scratch> python3 -I -B review_checks.py > review-checks.json
Read-only on the payload, handoff/automation-envelopes-v1 and r2/t11-structure-v1. Independent of the author's
build_v2.py and of the v1 cross-check model: the contract is restated here from spec.md alone.

Checks: (1) inventory and SHA-256 of every payload file against manifest.json; (2) the superseded release's
manifest digest and file hashes; (3) carried records equal v1's and carried fixtures equal v1's files with
whole lines inserted only; (4) the T1.1 checkers (fixture_audit.py by its own command line on a copy holding only
this release, schema_check.py on every fixture); (5) the reviewer's restatement of the contract against all
expectations; (6) isolation: each refused fixture with only its tested defect repaired opens under the
restatement and passes the T1.1 checker; (7) links and case inputs resolve in a copy; (8) a wide sanitization
scan and a scan for wording that implies evaluated or playback values.
"""
import hashlib, json, math, os, re, shutil, struct, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PKG = HERE.parents[1] / "automation-envelopes-v2"
V1 = ROOT / "handoff/automation-envelopes-v1"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
SCHEMA = "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt"
V1_DIGEST = "793c1d7d5432de529c21c628e7fa6c46eecb1fa9128a4da9db1d1dfc34378302"  # handoff/index.md catalog value
L = -63072000.0
sha = lambda b: hashlib.sha256(b).hexdigest()


class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


# ---- the contract, restated from spec.md ----
NUM = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?")


def read_double(t):  # REQ-012 rule 1
    s = t.lstrip(" ")
    if re.match(r"[+-]?(0[xX]|inf|nan)", s, re.I) or s.startswith("#") or t == "Invalid" or t[:1] in "\t\r\n":
        raise NoExpectation(f"excluded text {t!r}")
    m = NUM.match(s)
    if not m:
        raise Refused(f"number text {t!r}")
    return float(m.group(0))


def read_value(kind, t):
    if kind == "FloatEvent":  # rule 2
        x = struct.unpack("<f", struct.pack("<f", read_double(t)))[0]
        if not -1e6 < x < 1e6:
            raise NoExpectation("value range")
        return x
    if kind == "BoolEvent":  # rule 3
        if t in ("true", "1"):
            return True
        if t in ("false", "0"):
            return False
        raise Refused(f"bool text {t!r}")
    # EnumEvent, rule 4 (excluded spellings first)
    if re.fullmatch(r" +\d+ +| *\+\d+ +|.*-.*", t) or (len(t) > 63 and t.endswith(" ")):
        raise NoExpectation(f"excluded integer text {t!r}")
    if t.isascii() and (re.fullmatch(r" *\+?\d+", t) or re.fullmatch(r"\d+ +", t)) and (t.endswith(" ") or len(t) <= 63):
        return int(t.strip().lstrip("+"))
    raise Refused(f"integer text {t!r}")


def fmt(x, p):  # REQ-012 rule 7
    if x == 0 and math.copysign(1, x) > 0:
        return "0"
    if x == 0:
        raise NoExpectation("negative zero on save")
    lam = math.log10(abs(x))
    k = math.ceil(lam) if lam >= 0 else math.floor(lam)
    if abs(lam - round(lam)) < 1e-9 and Decimal(abs(x)) != Decimal(10) ** round(lam):
        raise NoExpectation("next to a power of ten")
    d = max(0, p - k)
    s = format(Decimal(x).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_EVEN), "f")
    return s.rstrip("0").rstrip(".") if "." in s else s


def K(c1, c2):  # REQ-009
    return 0 <= c1 <= 1 and 0 <= c2 <= 1 and (c1 <= c2 or c1 * c1 + c2 * c2 - c1 * c2 - c1 <= -1e-6)


CTRL = ("CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y")


def restate(data, action, discard="approved"):
    """Outcome and saved envelopes under the contract; NoExpectation outside its scope.
    discard: "approved" (REQ-007 clause 5 as approved), "none" (the automation-envelopes-v1 reading) or
    "clip-at-most-one" (a clip envelope with no event also discarded: the reading the disassembly rules out)."""
    root = ET.fromstring(data)
    ls = root.find("LiveSet")
    targets = {}
    for name in ("Speaker", "Pan", "CrossFadeState"):
        targets[ls.find(f"Tracks/AudioTrack/DeviceChain/Mixer/{name}/AutomationTarget").get("Id")] = name
    clip_target = ls.find("Tracks/MidiTrack/DeviceChain/MainSequencer/MidiControllers/ControllerTargets.6").get("Id")
    kind_of = {"Speaker": "BoolEvent", "Pan": "FloatEvent", "CrossFadeState": "EnumEvent", "ctl6": "FloatEvent"}
    envs = []
    for e in ls.findall("Tracks/AudioTrack/AutomationEnvelopes/Envelopes/AutomationEnvelope"):
        envs.append(("track", targets[e.find("EnvelopeTarget/PointeeId").get("Value")], e))
    for e in ls.findall("Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip/Envelopes/Envelopes/ClipEnvelope"):
        assert e.find("EnvelopeTarget/PointeeId").get("Value") == clip_target
        envs.append(("clip", "ctl6", e))
    if len({t for _, t, _ in envs}) != len(envs):
        raise NoExpectation("two envelopes on one target")
    tl = ls.find("Tracks/MidiTrack/DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events")
    if tl is not None and len(tl):
        raise NoExpectation("non-empty arrangement clip timeline")
    parsed = []
    for where, tgt, e in envs:  # reading: text rules refuse first (rule 5)
        evs = []
        for ev in e.find("Automation/Events"):
            if ev.tag != kind_of[tgt]:
                raise NoExpectation("event kind")
            t = read_double(ev.get("Time"))
            v = read_value(ev.tag, ev.get("Value"))
            c = [read_double(ev.get(n)) if ev.get(n) is not None else 0.5 for n in CTRL]
            evs.append((ev.tag, t, v, c, ev))
        if any(b[1] < a[1] for a, b in zip(evs, evs[1:])) or (evs and not L <= evs[0][1] < 1e6):
            raise NoExpectation("time order or range")
        parsed.append((where, tgt, evs))
    kept = []
    for where, tgt, evs in parsed:  # REQ-007 clause 5 (as approved): discard before the checks
        clip_cut = len(evs) == 1 if discard == "approved" else len(evs) <= 1
        if discard != "none" and ((where == "track" and len(evs) < 2) or (where == "clip" and clip_cut)):
            continue
        kept.append((where, tgt, evs))
    for where, tgt, evs in kept:  # REQ-007 clauses 1 and 2
        if not evs:
            raise Refused(f"empty {where} envelope")
        if evs[0][1] not in (L, 0.0):
            raise Refused(f"first event time {evs[0][1]}")
    if action == "open":
        return {"outcome": "opens"}
    saved = []
    for where, tgt, evs in kept:
        if where != "track":
            continue
        out = []
        for i, (tag, t, v, c, ev) in enumerate(evs):
            a = {"Time": fmt(t, 17)}
            a["Value"] = fmt(float(v), 9) if tag == "FloatEvent" else ("true" if v is True else "false") if tag == "BoolEvent" else str(v)
            if c != [0.5] * 4:
                nxt = evs[i + 1] if i + 1 < len(evs) else None
                if i == 0 or nxt is None or nxt[1] <= t or nxt[2] == v or not (K(c[0], c[2]) and K(c[1], c[3])):
                    raise NoExpectation("curve controls outside REQ-008 clause 4 or K")
                for n, x in zip(CTRL, c):
                    if x != 0.5:
                        a[n] = fmt(x, 17)
            out.append({"element": tag, "attributes": a})
        if evs and evs[0][2] != evs[1][2]:
            raise NoExpectation("leading value differs from the next")
        saved.append({"target": tgt, "events": out})
    return {"outcome": "opens", "saved": {"envelopes": saved}}


def outcome(data, action, discard="approved"):
    try:
        return restate(data, action, discard)
    except Refused as e:
        return {"outcome": "refused", "reason": str(e)}


def same(got, exp):
    if got["outcome"] != exp["outcome"]:
        return False
    if "saved" not in exp:
        return True
    g = {x["target"]: x["events"] for x in got["saved"]["envelopes"]}
    return all(g.get(x["target"]) == x["events"] for x in exp["saved"]["envelopes"])


# ---- T1.1 checkers ----
def t11_cli(cases):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(PKG, Path(tmp) / "automation-envelopes-v2")
        out = Path(tmp) / "audit.json"
        r = subprocess.run([sys.executable, "-I", "-B", str(T11 / "fixture_audit.py"), SCHEMA, tmp, str(out)],
                           capture_output=True, text=True, check=True)
        audit = json.loads(out.read_text())
    files = sorted(str(p) for p in (PKG / "fixtures").glob("*.xml"))
    sc = [json.loads(x) for x in subprocess.run([sys.executable, "-I", "-B", str(T11 / "schema_check.py"), SCHEMA, *files],
                                                capture_output=True, text=True, check=True).stdout.splitlines()]
    rel = audit["releases"][0]
    per = {}
    for e in rel["fixtures"]:
        per[e["fixture"]] = {"kind": e["kind"], "refusals": e.get("refusals"), "unknown_shapes": e.get("unknown_shapes"),
                             "effects": sorted({c.get("effect") for c in e["cases"]})}
    for x in sc:
        per[os.path.relpath(x["doc"], PKG)]["schema_deviations"] = x.get("deviations")
        per[os.path.relpath(x["doc"], PKG)]["structure_rules"] = x.get("rules")
    return {"stdout": r.stdout.strip(), "totals": audit["totals"], "summary": rel.get("summary"), "fixtures": per}


def t11_one(data):
    """T1.1 checker on one document held in memory (fixture_audit.measure/refusals/unknowns, unchanged)."""
    sys.path.insert(0, str(T11))
    import fixture_audit as fa
    from schema_check import load_schema
    if not fa.LIVESET_ORDER:
        t11_one.schema = load_schema(SCHEMA)
        fa.LIVESET_ORDER.extend(t11_one.schema["LiveSet"])
    dev, r = fa.measure(t11_one.schema, ET.fromstring(data))
    return {"refusals": fa.refusals(r, dev), "unknown_shapes": fa.unknowns(r), "schema_deviations": dev}


# reviewer's own controls: (case, old text, new text) repairing only the defect under test
CONTROLS = {
    "AUTOMATION-ENVELOPES-008": [('Time="-63071999"', 'Time="-63072000"')],
    "AUTOMATION-ENVELOPES-012": [("<Events />", '<Events>\n<FloatEvent Id="0" Time="-63072000" Value="0" />\n'
                                  '<FloatEvent Id="1" Time="0" Value="0" />\n</Events>')],
    "AUTOMATION-ENVELOPES-013": [('Value="abc"', 'Value="0"')],
    "AUTOMATION-ENVELOPES-014": [('Value="TRUE"', 'Value="true"')],
    "AUTOMATION-ENVELOPES-015": [('Value="2.0"', 'Value="2"')],
    "AUTOMATION-ENVELOPES-030": [('Id="0" Time="4"', 'Id="0" Time="-63072000"')],
    "AUTOMATION-ENVELOPES-031": [('Id="0" Time="4"', 'Id="0" Time="-63072000"')],
}

DENY = [r"0x[0-9a-fA-F]{5,}", r"FUN_", r"\bA[A-Z][a-z]+[A-Z]\w*", r"\bT[A-Z][a-z]+[A-Z]\w*", r"[Pp]urg", r"dangling",
        r"\bwalk\b", r"post-?load", r"vtable", r"pseudo", r"decompil", r"disassembl", r"Ghidra", r"\bslot \+", r"\+0x",
        r"analysis/", r"raw/", r"wiki/", r"\.\./", r"\bSF-\d", r"\bI[0-9]\b", r"\bQ-0", r"\bT1[0-9.]", r"\bAEN-",
        r"\bs6-", r"\bn1-", r"arm64 corpus", r"\bLSong|\bASong", r"\bflag\b", r"SPEC-(?!AUTOMATION-ENVELOPES)",
        r"REQ-(?!AUTOMATION-ENVELOPES)", r"\bcorpus", r"\bexcerpt", r"\bP\b reading", r"recovered", r"\bLive\.arm64"]
VALUE_WORDS = [r"evaluat", r"playback", r"\bplays?\b", r"\b[EP]\(t\)", r"interpolat", r"\bramp", r"value at",
               r"value an envelope", r"supplies", r"between equal", r"applied", r"render", r"\baudio\b"]


def scan(patterns):
    hits = []
    for p in sorted(PKG.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".json"):
            for n, line in enumerate(p.read_text().splitlines(), 1):
                for rx in patterns:
                    for m in re.finditer(rx, line):
                        hits.append(f"{p.relative_to(PKG)}:{n}: {m.group(0)!r}")
    return hits


def links_and_inputs(cases):
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "pkg"
        shutil.copytree(PKG, cp)
        for md in cp.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
                path, _, frag = target.partition("#")
                if re.match(r"[a-z]+:", path):
                    bad.append(f"{md.name}: external {target}")
                    continue
                f = (md.parent / path) if path else md
                if not f.resolve().is_relative_to(cp.resolve()) or not f.is_file():
                    bad.append(f"{md.name}: {target}")
                elif frag and f.suffix == ".md":
                    anchors = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                               for h in re.findall(r"^#+ (.*)$", f.read_text(), re.M)}
                    if frag not in anchors:
                        bad.append(f"{md.name}: anchor {target}")
        for c in cases:
            if not (cp / c["input"]).is_file():
                bad.append(f"missing input {c['input']}")
    return bad


def main():
    out = {}
    man = json.loads((PKG / "manifest.json").read_text())
    listed = {f["path"]: f for f in man["files"]}
    on_disk = {str(p.relative_to(PKG)) for p in PKG.rglob("*") if p.is_file()} - {"manifest.json"}
    out["inventory_differences"] = sorted(on_disk ^ set(listed))
    out["hash_or_size_mismatches"] = [k for k, f in listed.items() if (PKG / k).is_file() and
                                      (sha((PKG / k).read_bytes()) != f["sha256"] or (PKG / k).stat().st_size != f["bytes"])]
    out["manifest_sha256"] = sha((PKG / "manifest.json").read_bytes())
    v1m = json.loads((V1 / "manifest.json").read_text())
    out["v1_manifest_digest_matches_catalog"] = sha((V1 / "manifest.json").read_bytes()) == V1_DIGEST == man["supersession"]["superseded_manifest_sha256"]
    out["v1_file_mismatches"] = [f["path"] for f in v1m["files"] if sha((V1 / f["path"]).read_bytes()) != f["sha256"]]
    cases = json.loads((PKG / "cases.json").read_text())["cases"]
    v1c = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
    carried, new = [], []
    for c in cases:
        (carried if c["id"] in v1c else new).append(c["id"])
    out["carried"], out["new"], out["not_carried"] = carried, new, sorted(set(v1c) - {c["id"] for c in cases})
    import difflib
    sup = {}
    for cid in carried:
        a = (V1 / f"fixtures/{cid}.xml").read_text().split("\n")
        b = (PKG / f"fixtures/{cid}.xml").read_text().split("\n")
        ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != "equal"]
        sup[cid] = {"record_equal": next(c for c in cases if c["id"] == cid) == v1c[cid],
                    "only_insertions": all(o[0] == "insert" for o in ops), "inserted_lines": sum(o[4] - o[3] for o in ops)}
    out["carried_checks"] = sup
    out["t11_checker"] = t11_cli(cases)
    res, iso = {}, {}
    for c in cases:
        data = (PKG / c["input"]).read_bytes()
        try:
            got = outcome(data, c["action"])
            res[c["id"]] = {"agrees": same(got, c["expected"]), "reason": got.get("reason")}
        except NoExpectation as e:
            res[c["id"]] = {"agrees": False, "reason": f"no expectation: {e}"}
        if c["expected"]["outcome"] == "refused":
            ctrl = data.decode()
            for old, new_ in CONTROLS[c["id"]]:
                assert ctrl.count(old) == 1, (c["id"], old)
                ctrl = ctrl.replace(old, new_)
            iso[c["id"]] = {"control": outcome(ctrl.encode(), "open")["outcome"], "t11": t11_one(ctrl.encode())}
    out["restatement"] = res
    dep = {}
    for mode in ("none", "clip-at-most-one"):
        dep[mode] = [c["id"] for c in cases if outcome((PKG / c["input"]).read_bytes(), c["action"], mode)["outcome"]
                     != c["expected"]["outcome"]]
    out["cases_whose_outcome_changes_under_other_readings"] = dep
    sys.path.insert(0, str(T11))
    import fixture_audit as fa
    dropped = {}
    for cid in ("AUTOMATION-ENVELOPES-003", "AUTOMATION-ENVELOPES-004", "AUTOMATION-ENVELOPES-011"):
        root = ET.fromstring((V1 / f"fixtures/{cid}.xml").read_bytes())
        _, _, fixed = fa.repairs(root)  # T1.1's own minimal and recommended additions
        data = ET.tostring(fixed)
        dropped[cid] = {"v1_expected": v1c[cid]["expected"]["outcome"], "t11_after_additions": t11_one(data),
                        "approved_reading": outcome(data, "open")["outcome"], "v1_reading": outcome(data, "open", "none")}
    out["v1_dropped_cases_with_corrected_structure"] = dropped
    out["isolation_controls"] = iso
    out["fixtures_ascii_lf_final_newline"] = all(p.read_bytes().isascii() and b"\r" not in p.read_bytes() and
                                                 p.read_bytes().endswith(b"\n") for p in (PKG / "fixtures").glob("*.xml"))
    out["distinct_fixtures"] = len({sha(p.read_bytes()) for p in (PKG / "fixtures").glob("*.xml")})
    out["unresolved_links_or_inputs"] = links_and_inputs(cases)
    r2 = ROOT / "analysis/ableton-live-12.4.3/r2"
    ident = {}
    for name, path, want in [("Live.arm64", ROOT / "analysis/ableton-live-12.4.3/derived/Live.arm64",
                              "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad"),
                             ("Live_x86_64", Path("/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64"),
                              "1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0"),
                             ("schema 12.0_12402", Path(SCHEMA), "b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299")]:
        ident[name] = sha(path.read_bytes()) == want
    for pk in ("s6-automation-v1", "t11-structure-v1"):
        files = json.loads((r2 / pk / "manifest.json").read_text())["files"]
        ident[pk] = {"files": len(files), "mismatches": [k for k, f in files.items()
                     if not (r2 / pk / k).is_file() or sha((r2 / pk / k).read_bytes()) != f["sha256"]]}
    for c in ("corpus", "corpus-x86"):
        ident[c + " indexes executable_sha256"] = json.loads(Path(f"/var/tmp/sound-analysis/{c}/indexes/manifest.json").read_text())["executable_sha256"]
    out["evidence_identity"] = ident
    out["sanitization_hits"] = scan(DENY)
    out["value_wording_hits"] = scan(VALUE_WORDS)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
