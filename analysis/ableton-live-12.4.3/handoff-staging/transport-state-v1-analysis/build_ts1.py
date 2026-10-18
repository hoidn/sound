"""Stage the transport-state-v1 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from anywhere:
  python3 -I build_ts1.py build          # fixtures/, cases.json, draft manifest.json in ../transport-state-v1/
  python3 -I build_ts1.py seal           # manifest files[] + checks -> author-validation.json
  python3 -I build_ts1.py verify <dir>   # same checks against an exported copy (no manifest rewrite)

spec.md, README.md and AGENTS.md are hand-written. Expected outputs below are the hand-derived
static expectations from SPEC-TRANSPORT-STATE r1 (narrowed; see wiki/specs/transport-state-handoff-plan.md).
The model() functions are an independent re-reading of the released clauses used only to
cross-check those expectations; it shares the static evidence and is not an oracle.
"""
import hashlib, json, math, re, shutil, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / "transport-state-v1"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS"
PROV = "static-derived; not observed reference output"
R = "REQ-TRANSPORT-STATE-"
ORDER = ["PhaseNudgeTempo", "LoopOn", "LoopStart", "LoopLength", "LoopIsSongStart", "CurrentTime", "PunchIn",
         "PunchOut", "MetronomeTickDuration"] + [n + "KeyMidi" for n in (
         "DrawButton Follow PhaseNudgeUp PhaseNudgeDown TapTempo LoopOn Start Stop Record SessionRecord "
         "PrepareSceneForNewRecording ArrangementOverdub AutomationArm BackToArrangement ReEnableAutomation "
         "PunshIn PunshOut MetronomOn MidiPrelisten TriggerCapture FollowActionEnabled IsTempoFollowerInControl "
         "ResyncExternalHardware").split()] + ["DrawMode"]
BASE = [("PhaseNudgeTempo", "10"), ("LoopOn", "false"), ("LoopStart", "8"), ("LoopLength", "16"),
        ("LoopIsSongStart", "false"), ("CurrentTime", "0"), ("PunchIn", "false"), ("PunchOut", "false"),
        ("MetronomeTickDuration", "0"), ("DrawMode", "false")]
TEMPO, TSIG = "MainTrack/DeviceChain/Mixer/Tempo/Manual", "MainTrack/DeviceChain/Mixer/TimeSignature/Manual"


def doc(transport=None, tempo='<Manual Value="120" />', tsig='<Manual Value="201" />'):
    lines = transport or [f'<{n} Value="{v}" />' for n, v in BASE]
    t = "\n".join("      " + x for x in lines)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<Ableton MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1">\n  <LiveSet>\n'
            f'    <Transport>\n{t}\n    </Transport>\n    <MainTrack>\n      <DeviceChain>\n        <Mixer>\n'
            f'          <Tempo>\n            {tempo}\n          </Tempo>\n'
            f'          <TimeSignature>\n            {tsig}\n          </TimeSignature>\n'
            f'        </Mixer>\n      </DeviceChain>\n    </MainTrack>\n  </LiveSet>\n</Ableton>\n')


def edit(name, value=None, drop=(), extra=None, dup=None):
    out = []
    for n, v in BASE:
        if n in drop:
            continue
        out.append(f'<{n} />' if (n == name and value is None) else f'<{n} Value="{value if n == name else v}" />')
        if dup and n == dup[0]:
            out.append(f'<{n} Value="{dup[1]}" />')
    return out + ([extra] if extra else [])


# id, kind, requirements, purpose, fixture text, action, expected
CASES = [
    ("TS-001", "positive", ["003", "002", "011"], "Loop switch text true opens loop on and saves as true",
     doc(edit("LoopOn", "true")), "open-save",
     {"outcome": "opens", "state": {"loop_on": True}, "saved": {"values": {"Transport/LoopOn": "true"}}}),
    ("TS-002", "positive", ["003"], "Loop switch text 1 opens loop on", doc(edit("LoopOn", "1")), "open",
     {"outcome": "opens", "state": {"loop_on": True}}),
    ("TS-003", "positive", ["003"], "Loop switch text 0 opens loop off", doc(edit("LoopOn", "0")), "open",
     {"outcome": "opens", "state": {"loop_on": False}}),
    ("TS-004", "negative", ["003"], "Loop switch text TRUE is refused (case-sensitive)",
     doc(edit("LoopOn", "TRUE")), "open", {"outcome": "refused"}),
    ("TS-005", "negative", ["003"], "Empty loop switch text is refused", doc(edit("LoopOn", "")), "open",
     {"outcome": "refused"}),
    ("TS-006", "boundary", ["004", "011"], "Loop start text after the numeric prefix is ignored",
     doc(edit("LoopStart", "4.5abc")), "open-save",
     {"outcome": "opens", "state": {"loop_start": 4.5}, "saved": {"values": {"Transport/LoopStart": "4.5"}}}),
    ("TS-007", "negative", ["004"], "Loop length text without a numeric prefix is refused",
     doc(edit("LoopLength", "abc")), "open", {"outcome": "refused"}),
    ("TS-008", "positive", ["005", "011"], "Tempo text is held as binary32 and saved with nine-digit precision",
     doc(tempo='<Manual Value="93.3333333" />'), "open-save",
     {"outcome": "opens", "state": {"tempo": 93.33333587646484}, "saved": {"values": {TEMPO: "93.3333359"}}}),
    ("TS-009", "negative", ["006"], "Time-signature code text with a fraction is refused",
     doc(tsig='<Manual Value="201.0" />'), "open", {"outcome": "refused"}),
    ("TS-011", "missing", ["007"], "Missing LoopStart element reads as 8", doc(edit(None, drop=("LoopStart",))),
     "open", {"outcome": "opens", "state": {"loop_start": 8.0}}),
    ("TS-012", "missing", ["007"], "LoopLength element without Value reads as 16", doc(edit("LoopLength")),
     "open", {"outcome": "opens", "state": {"loop_length": 16.0}}),
    ("TS-013", "missing", ["007"], "Missing CurrentTime and LoopOn elements read as 0 and off",
     doc(edit(None, drop=("CurrentTime", "LoopOn"))), "open",
     {"outcome": "opens", "state": {"current_time": 0.0, "loop_on": False}}),
    ("TS-014", "missing", ["007"], "Tempo Manual without Value reads as 120", doc(tempo="<Manual />"), "open",
     {"outcome": "opens", "state": {"tempo": 120.0}}),
    ("TS-015", "negative", ["008"], "Two LoopOn elements in Transport are refused",
     doc(edit(None, dup=("LoopOn", "true"))), "open", {"outcome": "refused"}),
    ("TS-016", "boundary", ["008"], "Unknown Transport child is skipped and not saved",
     doc(edit(None, extra='<Foo Value="1" />')), "open-save",
     {"outcome": "opens", "saved": {"absent": ["Transport/Foo"]}}),
    ("TS-020", "save", ["011"], "Tempo 121.2 is saved as 121.199997", doc(tempo='<Manual Value="121.2" />'),
     "open-save", {"outcome": "opens", "saved": {"values": {TEMPO: "121.199997"}}}),
    ("TS-021", "save", ["011"], "Loop start 0.3 is saved with seventeen-digit precision",
     doc(edit("LoopStart", "0.3")), "open-save",
     {"outcome": "opens", "saved": {"values": {"Transport/LoopStart": "0.299999999999999989"}}}),
    ("TS-022", "save", ["002", "011"], "Unchanged values round-trip and Transport children keep their order",
     doc(), "open-save",
     {"outcome": "opens", "saved": {"transport_order": True, "values": {
         "Transport/LoopOn": "false", "Transport/LoopStart": "8", "Transport/LoopLength": "16",
         "Transport/CurrentTime": "0"}}}),
]
COMPARATOR = {
    "open": "outcome exact; listed state keys exact (binary64 equality)",
    "open-save": "outcome exact; listed state keys exact; saved document compared as parsed XML for listed "
                 "values (exact Value text, single empty element), absent paths and Transport order only",
}


# ---- independent cross-check model of the released clauses (not an oracle) ----
class Refused(Exception):
    pass


class Excluded(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def read_number(text, single):
    rest = text.lstrip(" ").lstrip("+-").lower()
    if text == "Invalid" or text.startswith("#") or rest.startswith(("0x", "inf", "nan")) or re.match(r"^ *[^\S ]", text):
        raise Excluded(text)
    m = re.match(r"^ *([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)", text)
    if not m:
        raise Refused(text)
    return f32(float(m.group(1))) if single else float(m.group(1))


def read_bool(text):
    if text in ("true", "1"):
        return True
    if text in ("false", "0"):
        return False
    raise Refused(text)


def read_int(text):
    if re.fullmatch(r" +\+?\d+ +|\+\d+ +", text) or "-" in text:
        raise Excluded(text)
    if not text.isascii() or not text.strip(" "):
        raise Refused(text)
    body = text.strip(" ")
    body = body[1:] if body.startswith("+") else body
    if not re.fullmatch(r"\d{1,63}", body):
        raise Refused(text)
    return int(body)


def fmt(x, p):
    if x == 0:
        assert math.copysign(1, x) > 0
        return "0"
    lg = math.log10(abs(x))
    k = math.floor(lg) if lg < 0 else math.ceil(lg)
    s = "%.*f" % (max(0, p - k), x)
    return s.rstrip("0").rstrip(".") if "." in s else s


def children(parent, name):
    return [] if parent is None else [c for c in parent if c.tag == name]


def model(xml_text):
    """Return (outcome, state, saved_xml_root or None)."""
    try:
        live = ET.fromstring(xml_text).find("LiveSet")
    except ET.ParseError:
        return "refused", None, None
    tr = live.find("Transport")
    mixer = live.find("MainTrack/DeviceChain/Mixer")
    state = {"loop_on": False, "loop_start": 8.0, "loop_length": 16.0, "current_time": 0.0, "tempo": 120.0}
    try:
        for name in ORDER:
            if len(children(tr, name)) > 1 and not name.endswith("KeyMidi"):
                raise Refused("duplicate " + name)
        for sect in ("Tempo", "TimeSignature"):
            if len(children(mixer.find(sect), "Manual")) > 1:
                raise Refused("duplicate Manual")
        for name, key, reader in (("LoopOn", "loop_on", read_bool),
                                  ("LoopStart", "loop_start", lambda t: read_number(t, False)),
                                  ("LoopLength", "loop_length", lambda t: read_number(t, False)),
                                  ("CurrentTime", "current_time", lambda t: read_number(t, False))):
            el = tr.find(name)
            if el is not None and el.get("Value") is not None:
                state[key] = reader(el.get("Value"))
        tm = mixer.find("Tempo/Manual")
        if tm is not None and tm.get("Value") is not None:
            state["tempo"] = read_number(tm.get("Value"), True)
        code = read_int(mixer.find("TimeSignature/Manual").get("Value"))
    except Refused:
        return "refused", None, None
    assert 0 <= state["loop_start"] < 1e6 and 1 <= state["loop_length"] < 1e6 and 0 <= state["current_time"] < 1e6
    assert 20 <= state["tempo"] <= 999 and 0 <= code <= 494
    out = {"LoopOn": "true" if state["loop_on"] else "false", "LoopStart": fmt(state["loop_start"], 17),
           "LoopLength": fmt(state["loop_length"], 17), "CurrentTime": fmt(state["current_time"], 17)}
    present = {c.tag: c.get("Value") for c in tr if c.tag in ORDER}
    root = ET.Element("Ableton")
    t = ET.SubElement(ET.SubElement(root, "LiveSet"), "Transport")
    for name in ORDER:
        if name in out or name in present:
            ET.SubElement(t, name, Value=out.get(name, present.get(name)))
    mx = ET.SubElement(ET.SubElement(ET.SubElement(root.find("LiveSet"), "MainTrack"), "DeviceChain"), "Mixer")
    ET.SubElement(ET.SubElement(mx, "Tempo"), "Manual", Value=fmt(state["tempo"], 9))
    ET.SubElement(ET.SubElement(mx, "TimeSignature"), "Manual", Value=str(code))
    return "opens", state, root


def judge(expected, outcome, state, saved):
    errs = []
    if outcome != expected["outcome"]:
        return [f"outcome {outcome}"]
    for k, v in expected.get("state", {}).items():
        if state[k] != v:
            errs.append(f"state {k}={state[k]!r}")
    sv = expected.get("saved", {})
    live = saved.find("LiveSet") if saved is not None else None
    for path, text in sv.get("values", {}).items():
        els = live.findall(path)
        if len(els) != 1 or list(els[0]) or set(els[0].attrib) != {"Value"} or els[0].get("Value") != text:
            errs.append(f"saved {path}")
    for path in sv.get("absent", []):
        if live.findall(path):
            errs.append(f"present {path}")
    if sv.get("transport_order"):
        names = [c.tag for c in live.find("Transport") if c.tag in ORDER]
        if names != sorted(names, key=ORDER.index) or any(names.count(n) != 1 for n in
                                                           ("LoopOn", "LoopStart", "LoopLength", "CurrentTime")):
            errs.append("transport order")
    return errs


# ---- packaging ----
def sha(b):
    return hashlib.sha256(b).hexdigest()


def manifest_skeleton():
    return {
        "schema": "handoff-manifest-v1",
        "release_id": "transport-state-v1",
        "release_status": "staged candidate; not reviewed; not released",
        "release_date": None,
        "target": TARGET,
        "specification": {"id": "SPEC-TRANSPORT-STATE", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-TRANSPORT", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {
            R + "001": "Locations and value types of the six values; homonymous elements elsewhere are different values. Units unreleased",
            R + "002": "Empty single-Value element shape for the four Transport values and both Manual elements; the four always written once; relative order of the 33 known Transport children",
            R + "003": "Exact Boolean tokens true/1/false/0; all other text refused",
            R + "004": "Decimal-prefix reading with leading spaces skipped and trailing text ignored; nearest binary64; no prefix refused",
            R + "005": "Tempo read as REQ-004 then rounded to nearest binary32",
            R + "006": "Accepted and refused integer spellings listed in spec.md only",
            R + "007": "Missing element or Value for the four Transport values and tempo Manual reads off/8/16/0/120",
            R + "008": "Duplicate known non-KeyMidi Transport children or Manual refused; unknown Transport child skipped and not saved",
            R + "010": "Code meaning (n-1)+99*log2(d) only; no acceptance case",
            R + "011": "Boolean and integer text; fixed-precision decimal text with P=17 or 9 for in-range finite nonzero values; positive zero",
        },
        "unreleased_requirements": [R + "009", R + "012"],
        "compatibility_dimensions": {
            "project-files": "static-derived expectations for the listed document values; reference execution not-run",
            "behavior": "effective transport state after opening excluded",
            "audio": "excluded", "ui": "excluded", "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "number text starting (after spaces and sign) with 0x, inf or nan; Invalid; text starting with #; leading whitespace other than U+0020",
                "values outside the spec.md ranges; non-finite, largest finite and negative-zero values; saved values whose log10 is within 1e-12 of a non-exact integer",
                "time-signature text with spaces on both sides, or + with trailing spaces; any - sign",
                "missing TimeSignature/Manual or its value; missing Transport, Tempo, TimeSignature, Mixer, DeviceChain or MainTrack",
                "unknown attributes; repeated unknown children; any *KeyMidi child in the input; LoopIsSongStart other than false",
                "automation events or scene values that disagree with Manual",
                "other envelopes, format versions, compressed containers and document kinds",
            ],
            "behavior": [
                "effective tempo and time signature after opening; whether a code other than 201 takes effect",
                "editing after opening (UI, remote control, MIDI)",
                "whether automation or other known Transport children are written; byte layout of saved documents",
                "playback, timing, Link and external sync; undo",
                "refusal text, presentation and state after refusal",
            ],
            "parent_cases_not_released": ["TS-010", "TS-017", "TS-018", "TS-019", "TS-023"],
        },
        "fixture_origin": "independently authored minimal XML documents and expected logical results",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None,
                   "record": None},
        "supersedes": None,
        "entrypoint": "README.md",
        "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures").mkdir(parents=True)
    cases = []
    for cid, kind, reqs, purpose, text, action, expected in CASES:
        rel = f"fixtures/{cid}.xml"
        (STAGE / rel).write_text(text)
        cases.append({"id": cid, "kind": kind, "purpose": purpose, "requirements": [R + r for r in reqs],
                      "input": rel, "action": action, "expected": expected, "expectation_provenance": PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run",
                      "comparator": COMPARATOR[action]})
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": "transport-state-cases-v1", "target": TARGET,
        "scope": "transport-state-v1 partial requirement clauses only (see spec.md)",
        "status": "staged candidate; not reviewed; not released",
        "fixture_origin": "Independently authored minimal XML documents; no shipped file copied or excerpted",
        "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
        "representation": {
            "paths": "relative to /Ableton/LiveSet",
            "state": "loop_on Boolean; loop_start, loop_length, current_time binary64; tempo binary32 compared after exact widening",
            "saved": "values: path -> exact Value text; absent: paths; transport_order: REQ-002 order",
            "note": "project comparison representation, not an API of the original application or a required design"},
        "cases": cases}, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_skeleton(), indent=1) + "\n")
    print(len(cases), "cases staged")


DENY = [r"0x1[0-9a-f]{5,}", r"FUN_", r"\bA(Transport|Loop|Current|Timeable|Remoteable|MainTrack|Song)\w*",
        r"SNewCompound", r"[Ss]et[Vv]alue|[Gg]et[Vv]alue", r"strtod", r"[Ee]xpat", r"vtable", r"registr",
        r"constructor", r"loader", r"post-load", r"\bslot", r"descriptor", r"Ghidra", r"decompil", r"pseudocode",
        r"disassembl", r"dossier", r"corpus", r"\bn[12]-0", r"s1-static", r"PRB-", r"\bQ-0\d", r"analysis/",
        r"wiki/", r"\.\./", r"/home/", r"/var/", r"/tmp/", r"derivation", r"traceab", r"Recording Audio",
        r"Core Library", r"\bB0\b", r"%\.\*", r"printf", r"arm64", r"Python", r"\bev_[0-9a-f]", r"\bS[1-5]\b",
        r"\bN[1-5]\b", r"build_ts1"]


def links(pkg, md):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = not re.match(r"[a-z]+:", target) and dest.is_file() and pkg in dest.parents
        if ok and anchor:
            ok = anchor in {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                            for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
        out.append((target, ok))
    return out


def check(pkg, rewrite):
    pkg = pkg.resolve()
    doc_ = json.loads((pkg / "cases.json").read_text())
    problems = {}
    for c in doc_["cases"]:
        raw = (pkg / c["input"]).read_bytes()
        errs = [] if raw.isascii() and b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n") else ["format"]
        try:
            outcome, state, saved = model(raw.decode("ascii"))
            errs += judge(c["expected"], outcome, state, saved)
        except Excluded as e:
            errs.append(f"fixture hits an exclusion: {e}")
        if c["expected"]["outcome"] != "refused":
            ET.fromstring(raw)  # positive fixtures must be well-formed
        if errs:
            problems[c["id"]] = errs
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()),
                              "bytes": p.stat().st_size} for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}
    report = {
        "cases": len(doc_["cases"]), "manifest_case_count": manifest["case_count"], "case_problems": problems,
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in doc_["cases"] if not (pkg / c["input"]).is_file()],
        "deny_list_hits": {str(p.relative_to(pkg)): hits for p in [*files, pkg / "manifest.json"]
                           if (hits := sorted({m for pat in DENY for m in re.findall(pat, p.read_text())}))},
        "limits": "Checks authored consistency only: no reference or candidate executed; the cross-check model is an "
                  "independent re-reading of the same static evidence, not an oracle.",
    }
    return report


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        rep = check(STAGE, rewrite=True)
        rep = {"schema": "author-validation-v1", "package": "transport-state-v1 (staged candidate)",
               "python": sys.version.split()[0], **rep}
        (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1) + "\n")
        print(json.dumps(rep, indent=1))
    elif cmd == "verify":
        print(json.dumps(check(Path(sys.argv[2]), rewrite=False), indent=1))
