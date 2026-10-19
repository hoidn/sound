"""Stage the midi-note-storage-v2 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from anywhere:
  python3 -I build_v2.py build          # fixtures/, cases.json, draft manifest.json, traceability.json, text diff
  python3 -I build_v2.py seal           # manifest files[] + checks -> author-validation.json
  python3 -I build_v2.py verify <dir>   # the same checks against an exported copy (no manifest rewrite)

Inputs, all read only:
- handoff/midi-note-storage-v1: the 67 carried case records and fixtures;
- the v1 analysis modules mns_cases (fragments, edits, carrier, gzip form), mns_model (cross-check model)
  and mns_trace (v1 traceability), imported unchanged;
- t11-structure-v1: schema_check.py, fixture_audit.py and released-fixture-audit.json (the Live Set
  structure checker and the minimal addition per released fixture), with the shipped schema 12.0_12402;
- x2-notes-launch-v1 and x2-transport-v1 results (extracted execution, label X).

Structure outputs kept beside this script (regenerate from this directory; S = the schema path below):
  python3 -I -B ../../r2/t11-structure-v1/schema_check.py "$S" ../midi-note-storage-v2/fixtures/*.als > t11-schema-check.jsonl
      (then strip the leading path to .../handoff-staging/)
  python3 -I -B ../../r2/t11-structure-v1/fixture_audit.py "$S" <dir holding a copy of midi-note-storage-v2> t11-fixture-audit.json

Each v2 fixture is the v1 fixture text with the two T11-MIN additions the audit lists for it: one empty
freeze slot after the MIDI track's MainSequencer (required: REQ-LIVE-SET-STRUCTURE-006) and one scene
after Tracks (removes REQ-006's slot-against-scene unknown). Nothing else changes. MNS-012, which the audit
cannot parse, gets the same additions. spec.md, README.md and AGENTS.md are hand-written. model() is the
v1 cross-check model with the v2 negative-zero clauses; it restates the same evidence and is not an oracle.
"""
import copy, difflib, json, math, re, shutil, struct, sys, zlib
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True  # keep the v1 analysis and T11 directories free of caches
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "midi-note-storage-v2"
V1 = ROOT / "handoff/midi-note-storage-v1"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
XN = ROOT / "analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1"
XT = ROOT / "analysis/ableton-live-12.4.3/r2/x2-transport-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
sys.path[:0] = [str(HERE.parent / "midi-note-storage-v1-analysis"), str(T11)]
import mns_cases as mc  # noqa: E402
import mns_model as mm  # noqa: E402
import mns_trace as mt  # noqa: E402
import fixture_audit as fa  # noqa: E402  (imports schema_check)
import build_mns as b1  # noqa: E402  (links, DENY, sha; not run)

R = mc.R
PROV_X = "extracted execution (x86_64 slice, glibc substitutions); arm64 equivalence inferred"
H = mc.H  # "0.000000260156510156510156"

# ---- the two T11-MIN additions (released-fixture-audit.json, minimal and recommended addition) ----
FREEZE = ['<FreezeSequencer>', '\t<ClipSlotList>', '\t\t<ClipSlot Id="0">', '\t\t\t<ClipSlot>', '\t\t\t\t<Value />',
          '\t\t\t</ClipSlot>', '\t\t\t<HasStop Value="true" />', '\t\t</ClipSlot>', '\t</ClipSlotList>',
          '</FreezeSequencer>']
SCENES = ['<Scenes>', '\t<Scene Id="0">', '\t\t<Name Value="" />', '\t\t<Color Value="-1" />', '\t\t<Tempo Value="120" />',
          '\t\t<IsTempoEnabled Value="false" />', '\t\t<TimeSignatureId Value="201" />',
          '\t\t<IsTimeSignatureEnabled Value="false" />', '\t</Scene>', '</Scenes>']
AFTER_MAIN, AFTER_TRACKS = "\t" * 5 + "</MainSequencer>", "\t\t</Tracks>"


def add_structure(text):
    """v1 carrier text -> v2 carrier text: insert the freeze slot and the scene, nothing else."""
    lines = text.split("\n")
    i = lines.index(AFTER_MAIN) + 1
    lines[i:i] = ["\t" * 5 + x for x in FREEZE]
    j = lines.index(AFTER_TRACKS) + 1
    lines[j:j] = ["\t\t" + x for x in SCENES]
    return "\n".join(lines)


def strip_structure(text):
    lines = text.split("\n")
    i = lines.index(AFTER_MAIN) + 1
    j = lines.index(AFTER_TRACKS) + 1
    assert lines[i:i + len(FREEZE)] == ["\t" * 5 + x for x in FREEZE] and lines[j:j + len(SCENES)] == ["\t\t" + x for x in SCENES]
    del lines[i:i + len(FREEZE)]
    j = lines.index(AFTER_TRACKS) + 1
    del lines[j:j + len(SCENES)]
    return "\n".join(lines)


def document(frag):
    return add_structure(mc.document(frag).decode("utf-8")).encode("utf-8")


def unzip(raw):
    return zlib.decompress(raw, 31).decode("utf-8")


# ---- new cases (X): id, kind, requirement suffixes, purpose, fragment, expected saved notes ----
NEW = {
    "MNS-023": ("boundary", ["006", "016"], "Time -0.0000001 on n1 rounds to negative zero and is saved as -0",
                mc.F(mc.f0, mc.n(1, Time="-0.0000001")), mc.X(mc.s0, {1: {"Time": "-0"}})),
    "MNS-072": ("boundary", ["006", "016"], "Time 0.00000013007825507825505 on n1, one binary64 step below the binary64 "
                "value of half a grid unit, is stored as one grid unit", mc.F(mc.f0, mc.n(1, Time="0.00000013007825507825505")),
                mc.X(mc.s0, {1: {"Time": H}})),
    "MNS-073": ("boundary", ["002", "004", "005", "016"], "OffVelocity -0 on n1 and Probability -0 on n2 are kept as "
                "negative zero and saved as -0", mc.F(mc.f0, mc.n(1, OffVelocity="-0"), mc.n(2, Probability="-0")),
                mc.X(mc.s0, {1: {"OffVelocity": "-0"}, 2: {"Probability": "-0"}})),
    "MNS-074": ("boundary", ["002", "005", "006", "016"], "Velocity -0 on n1 becomes 1; Duration -0 on n2 and Time -0 on "
                "n3 are stored as positive zero", mc.F(mc.f0, mc.n(1, Velocity="-0"), mc.n(2, Duration="-0"),
                                                       mc.n(3, Time="-0")),
                mc.X(mc.s0, {1: {"Velocity": "1"}, 2: {"Duration": "0"}, 3: {"Time": "0"}})),
    "MNS-075": ("boundary", ["002", "005", "016"], "Velocity 127.00001 and 0.99999994, one binary32 step outside the "
                "limits, become 127 and 1", mc.F(mc.f0, mc.n(1, Velocity="127.00001"), mc.n(2, Velocity="0.99999994")),
                mc.X(mc.s0, {1: {"Velocity": "127"}, 2: {"Velocity": "1"}})),
}
V1_IDS = [c[0] for c in mc.CASES]
ORDER_IDS = sorted(V1_IDS + list(NEW))
FRAG = {c[0]: c[4] for c in mc.CASES} | {k: v[3] for k, v in NEW.items()}

# X evidence per case: (note, attribute, text, kind, X record). Record "note:<label>:<field>" names a vector of
# x2-notes-launch-v1 results/notes.json, "event:<input>" an event vector; field vel/veldev/offvel/prob is the
# copied binary32 value, time/dur the held binary64 value. The saved text is looked up in writer_texts.
X_EVIDENCE = {
    "MNS-023": [(1, "Time", "-0.0000001", "double", "note:MNS-023 n1:time")],
    "MNS-072": [(1, "Time", "0.00000013007825507825505", "double", "note:tie k=0 -1ulp:time")],
    "MNS-073": [(1, "OffVelocity", "-0", "float", "note:offvel -0:offvel"),
                (2, "Probability", "-0", "float", "note:prob -0:prob")],
    "MNS-074": [(1, "Velocity", "-0", "float", "note:vel -0:vel"), (2, "Duration", "-0", "double", "note:dur -0:dur"),
                (3, "Time", "-0", "double", "note:time -0:time")],
    "MNS-075": [(1, "Velocity", "127.00001", "float", "note:vel above 127:vel"),
                (2, "Velocity", "0.99999994", "float", "note:vel below 1:vel")],
}
# Carried cases whose limits, grid or writer the same X run also computed; their records stay unchanged.
X_CORROBORATES = {
    "MNS-014": [(1, "Velocity", "0", "float", "note:MNS-014 n1:vel"), (2, "Velocity", "300", "float", "note:MNS-014 n2:vel"),
                (3, "Velocity", "0.5", "float", "note:MNS-014 n3:vel")],
    "MNS-015": [(1, "OffVelocity", "-5", "float", "note:MNS-015 n1:offvel"),
                (2, "OffVelocity", "200", "float", "note:MNS-015 n2:offvel")],
    "MNS-016": [(1, "Probability", "1.5", "float", "note:MNS-016 n1:prob"),
                (2, "Probability", "-1", "float", "note:MNS-016 n2:prob")],
    "MNS-017": [(1, "Duration", "-2", "double", "note:MNS-017 n1:dur"),
                (2, "Duration", "Invalid", "double", "note:MNS-017 n2:dur")],
    "MNS-018": [(1, "Time", "-3", "double", "note:MNS-018 n1:time"),
                (1, "VelocityDeviation", "-500", "float", "note:MNS-018 n1:veldev")],
    "MNS-019": [(1, "Velocity", "80.578949", "float", "note:MNS-019 n1:vel"),
                (2, "Velocity", "33.3", "float", "note:MNS-019 n2:vel")],
    "MNS-020": [(1, "Time", "0.123456789", "double", "note:MNS-020 n1:time"),
                (1, "Duration", "0.3333333333", "double", "note:MNS-020 n1:dur")],
    "MNS-021": [(1, "Time", "-0.0000002", "double", "note:MNS-021 n1:time")],
    "MNS-022": [(1, "Time", "0.00000013", "double", "note:MNS-022 n1:time"),
                (3, "Duration", "0.000000131", "double", "note:MNS-022 n3:dur")],
    "MNS-025": [(2, "Time", "20", "double", "note:MNS-025:time"), (3, "Duration", "0", "double", "note:MNS-025:dur")],
    "MNS-067": [(3, "Time", " 0.5abc", "double", "note:MNS-067 n3:time")],
    "MNS-069": [("e1", "TimeOffset", "0.123456789", "double", "event:0.123456789")],
}
OMIT = {"Probability": 1.0, "VelocityDeviation": 0.0}  # REQ-004: value written only when it differs


# ---- cross-check model: mns_model with the v2 negative-zero clauses (not an oracle) ----
V1_FN = {k: getattr(mm, k) for k in ("number", "grid", "fmt", "read_note", "read_event")}


def neg0(v):
    return v == 0 and math.copysign(1, v) < 0


def number(text, single=False, invalid_ok=False):
    """v1 REQ-002 clause 3 reading; -0 now reads as negative zero (v1 excluded it)."""
    if text == "Invalid":
        if invalid_ok:
            return mm.DMAX
        raise mm.Excluded("Invalid outside Duration and TimeOffset")
    rest = text.lstrip(" ").lstrip("+-").lower()
    if text.startswith("#") or rest.startswith(("0x", "inf", "nan")) or re.match(r" *[^\S ]", text):
        raise mm.Excluded(f"number form {text!r}")
    m = re.match(r" *([+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)", text)
    if not m:
        raise mm.Refused(f"no numeric prefix {text!r}")
    v = mm.f32(float(m.group(1))) if single else float(m.group(1))
    if not abs(v) < 1e6:
        raise mm.Excluded(f"value {text!r} out of scope")
    return v


def grid(x):
    """REQ-006 formula; -0 gives +0, a value rounding to zero from below gives -0."""
    if x == mm.DMAX:
        return x
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * mm.H * 0.5) * 3843840.0) / 3843840.0)


def fmt(x, p):
    if x == 0:
        return "-0" if neg0(x) else "0"
    return V1_FN["fmt"](x, p)


def read_note(el):
    if "VelocityDeviation" in el.attrib and neg0(number(el.get("VelocityDeviation"), True)):
        raise mm.Excluded("VelocityDeviation -0")
    return V1_FN["read_note"](el)


def read_event(x):
    for a in ("Value", *mm.CURVES):
        if a in x.attrib and neg0(number(x.get(a), a == "Value")):
            raise mm.Excluded(f"{a} -0")
    return V1_FN["read_event"](x)


def model(raw):
    patch = {"number": number, "grid": grid, "fmt": fmt, "read_note": read_note, "read_event": read_event}
    for k, f in patch.items():
        setattr(mm, k, f)
    try:
        return mm.model(raw)
    finally:
        for k, f in V1_FN.items():
            setattr(mm, k, f)


# ---- X evidence lookup and check ----
def x_results():
    notes = json.loads((XN / "results/notes.json").read_text())
    parse = json.loads((XT / "results/parse.json").read_text())
    vec = {"note:" + v["label"]: v for v in notes["notes"]}
    vec |= {"event:" + repr(v["input_time_offset"]["v"]): v for v in notes["events"]}
    writes = {(w["kind"], w["value"]["bits"]): w["text"] for w in notes["writer_texts"]}
    texts = {(r["kind"], r["text"]): r for r in parse["number_and_bool"]}
    return vec, writes, texts


def dbits(v):
    return "0x" + struct.pack(">d", v).hex()


def x_value(vec, ref):
    kind, label, *field = ref.split(":")
    v = vec[kind + ":" + label]
    if kind == "event":
        return v["input_time_offset"]["v"], v["held_time_offset"]
    i, f = v["input"], field[0]
    if f in ("time", "dur"):
        return i[f]["v"], v["held_time" if f == "time" else "held_duration"]
    k = ["vel", "veldev", "offvel", "prob"].index(f)
    return i[f]["v"], v["copied_vel_veldev_offvel_prob"][k]


def saved_attr(case, note, attr):
    s = case["expected"]["saved_notes"]
    if note == "e1":
        return s["event_lists"][0]["events"][0].get(attr)
    kt, idx = {1: (0, 0), 2: (0, 1), 3: (1, 0)}[note]
    return s["key_tracks"][kt]["notes"][idx].get(attr)


def x_check(case, entries, x):
    """Compare a case's expectation with the X results it cites; returns a list of problems."""
    vec, writes, texts = x
    errs = []
    for note, attr, text, kind, ref in entries:
        read = mm.DMAX if text == "Invalid" else float(re.match(r" *([+-]?[0-9.]+)", text).group(1))
        read = mm.f32(read) if kind == "float" else read
        xin, held = x_value(vec, ref)
        if dbits(xin) != dbits(read):
            errs.append(f"{attr} {text!r}: X input {xin!r} is not the text's value {read!r}")
        if text == "-0":  # the reading of -0 itself: x2-transport-v1 parse.json, same text conversion
            r = texts.get((kind, "-0"))
            if not r or r["bits"] != ("8000000000000000" if kind == "double" else "80000000"):
                errs.append(f"{kind} '-0' did not read as negative zero")
        hv = struct.unpack(">f" if "bits32" in held else ">d", bytes.fromhex(held.get("bits32", held.get("bits"))[2:]))[0]
        exp = saved_attr(case, note, attr)
        if exp is None:
            if attr not in OMIT or hv != OMIT[attr]:
                errs.append(f"{attr}: omitted in the case, X value {hv!r}")
            continue
        got = writes.get((kind, dbits(hv)))
        if got != exp:
            errs.append(f"{attr} {text!r}: X held {hv!r} written {got!r}, case {exp!r}")
    return errs


# ---- T11 structure checks ----
def tree_form(e):
    return (e.tag, dict(e.attrib), [tree_form(c) for c in e])


def structure_report(pkg, cases):
    schema = fa.load_schema(str(SCHEMA))
    if not fa.LIVESET_ORDER:
        fa.LIVESET_ORDER.extend(schema["LiveSet"])
    audit = {e["fixture"]: e for r in json.loads((T11 / "released-fixture-audit.json").read_text())["releases"]
             if r["release"] == "midi-note-storage-v1" for e in r["fixtures"]}
    out = {"schema": str(SCHEMA.name), "refused_or_unknown": {}, "schema_deviations": {},
           "differs_from_audit_repair": [], "audit_additions_not_used": [], "unparseable": {}}
    want_add = {fa.ET.tostring(fa.ET.fromstring("".join(x.strip() for x in FREEZE))),
                fa.ET.tostring(fa.ET.fromstring("".join(x.strip() for x in SCENES)))}
    for c in cases:
        cid, txt = c["id"], unzip((pkg / c["input"]).read_bytes())
        try:
            root = ET.fromstring(txt)
        except ET.ParseError as e:
            out["unparseable"][cid] = str(e)
            continue
        dev, r = fa.measure(schema, root)
        bad = fa.refusals(r, dev) + fa.unknowns(r)
        if bad:
            out["refused_or_unknown"][cid] = bad
        if dev:
            out["schema_deviations"][cid] = dev
        e = audit.get(c["input"])
        if e:  # carried fixture: v2 tree equals the audit's repaired copy of the released v1 fixture
            adds = {fa.ET.tostring(fa.ET.fromstring(a["xml"])) for a in e["minimal_addition"] + e["recommended_addition"]}
            if adds != want_add:
                out["audit_additions_not_used"].append(cid)
            v1root = ET.fromstring(unzip((V1 / c["input"]).read_bytes()))
            if tree_form(fa.repairs(v1root)[2]) != tree_form(root):
                out["differs_from_audit_repair"].append(cid)
    # MNS-012 (repeated attribute, not parseable): without the repeat it is the MNS-001 fixture, which opens.
    t12 = unzip((pkg / "fixtures/MNS-012.als").read_bytes())
    out["MNS-012_without_repeated_attribute_equals_MNS-001"] = (
        t12.replace(' Velocity="85" Velocity="85"', ' Velocity="85"', 1) == unzip((pkg / "fixtures/MNS-001.als").read_bytes()))
    return out


# ---- packaging ----
sha = b1.sha
REVIEW_PENDING = {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None}


def manifest_meta(n_cases):
    v1m = json.loads((V1 / "manifest.json").read_text())
    scopes = dict(v1m["partial_requirement_scopes"])
    scopes.update({
        R + "002": scopes[R + "002"] + "; -0 reads as negative zero (expectations only in Time, Duration, Velocity, "
                                       "OffVelocity and Probability)",
        R + "005": "Velocity, OffVelocity, Probability and Duration limits on opening, exact at the binary32 bounds; "
                   "negative zero: Velocity -0 becomes 1, OffVelocity and Probability -0 kept, Duration -0 kept by the "
                   "limits; Time, VelocityDeviation and NoteId not limited",
        R + "006": "Rounding of Time, Duration and TimeOffset to multiples of 1/3,843,840 by the stated binary64 "
                   "formula, half away from zero, including next to halfway points; -0 stored as +0; a value rounding "
                   "to zero from below stored as -0",
        R + "016": "Saved number text with 17 or 9 significant-digit rule, positive zero 0 and negative zero -0, plain "
                   "integers, IsEnabled false",
    })
    excl = copy.deepcopy(v1m["exclusions"])
    inputs = excl["inputs_without_expectation"]
    k = next(i for i, s in enumerate(inputs) if s.startswith("NaN, infinite"))
    inputs[k] = ("NaN, infinite, # and hexadecimal number text, inf and nan words, leading whitespace other than "
                 "U+0020; Invalid outside Duration and TimeOffset; magnitudes of 1,000,000 or more other than Invalid; "
                 "negative zero read in VelocityDeviation, an event's Value or a curve control; saved values whose "
                 "log10 is within 1e-12 of an integer without being an exact power of ten")
    excl["parent_cases_not_released"] = [c for c in excl["parent_cases_not_released"] if c != "MNS-023"]
    return {
        "schema": "handoff-manifest-v1", "release_id": "midi-note-storage-v2",
        "release_status": "staged candidate; not reviewed; not released", "release_date": None,
        "target": v1m["target"],
        "specification": {"id": "SPEC-MIDI-NOTE-STORAGE", "parent_revision": 3, "release_revision": 3},
        "feature_ids": v1m["feature_ids"],
        "partial_requirement_scopes": scopes,
        "unreleased_requirements": v1m["unreleased_requirements"],
        "compatibility_dimensions": {
            "project-files": "static-derived and extracted-execution expectations for the clip notes element read and "
                             "written; reference execution not-run",
            **{k: v for k, v in v1m["compatibility_dimensions"].items() if k != "project-files"}},
        "expectation_provenance_labels": {
            mc.PROV: "derived from evidence reviewed before sanitization",
            PROV_X: "the original program's x86_64 build computed the judged values on a Linux x86_64 host, with glibc "
                    "in place of the macOS system libraries: the value limits and time-grid rounding applied to the "
                    "value of the case's text, the reading of the text -0, and the saved text of the resulting value; "
                    "locating the notes, reading other text, opening and saving remain static-derived",
        },
        "stated_assumptions": [
            "Opening a set and saving it without other changes changes the notes only as the release states; a "
            "refusal raised while the notes are read stops the reading of the document (as in midi-note-storage-v1).",
            "Decimal number text is read and written with exact, correctly rounded conversions; exact decimal ties on "
            "save round to even (as in midi-note-storage-v1). No case lies on a tie.",
            "The macOS arm64 build computes these limits, roundings, readings and texts as the x86_64 build does. All "
            "cases with the extracted-execution label depend on it.",
            "The reference's decimal reading of -0 gives negative zero, as the glibc run did. MNS-073 depends on "
            "it; the results of MNS-074 are the same for either zero.",
            "The reference's number text on save keeps the sign of negative zero, as the glibc run did. MNS-023 and "
            "MNS-073 depend on it.",
        ],
        "exclusions": excl,
        "fixture_origin": "independently authored gzip Live Sets from a carrier written for this release: one MIDI "
                          "track with one session slot holding the case's clip and one empty freeze slot, and one "
                          "scene; no shipped file content or program code",
        "approved_public_sources": [],
        "review": REVIEW_PENDING,
        "supersedes": "midi-note-storage-v1",
        "supersession": {
            "relationship": "superset in effect: every midi-note-storage-v1 clause and case is carried with the same "
                            "expectation; midi-note-storage-v1 stays immutable, but its fixtures lack Live Set "
                            "structure that opening requires and must not be used",
            "superseded_manifest_sha256": sha((V1 / "manifest.json").read_bytes()),
            "restated_cases": "the 67 midi-note-storage-v1 case records, unchanged; each fixture is the "
                              "midi-note-storage-v1 fixture with one empty freeze slot and one scene added",
            "changes": [
                "fixtures: all 67 rebuilt; each gains, and only gains, a FreezeSequencer whose ClipSlotList holds one "
                "empty slot, after the MIDI track's MainSequencer, and a Scenes list with one scene after Tracks; MNS-012 gets the "
                "same additions, so its only defect is the repeated attribute",
                "REQ-002: -0 reads as negative zero; MNS-073 and MNS-074",
                "REQ-005: limits exact at the binary32 bounds; negative zero for each limited value; MNS-074, MNS-075",
                "REQ-006: the stated formula governs next to halfway points; -0 stored as +0; a value rounding to "
                "zero from below stored as -0; MNS-023, MNS-072, MNS-074",
                "REQ-016: negative zero written -0; MNS-023, MNS-073",
                "exclusion of negative zero narrowed to VelocityDeviation, event Value and curve controls; MNS-023 "
                "released",
                "provenance label extracted execution added for the five new cases, with the stated assumptions it "
                "rests on; carried records keep the static-derived label",
            ],
        },
        "entrypoint": "README.md", "case_count": n_cases,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def traceability(cases):
    xr = "analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/results/notes.json"
    v1t = json.loads((HERE.parent / "midi-note-storage-v1-analysis/traceability.json").read_text())
    out = {"schema": "midi-note-storage-v2-traceability-v1", "spec": "SPEC-MIDI-NOTE-STORAGE r3",
           "carried_static_evidence": {
               "traceability": "analysis/ableton-live-12.4.3/handoff-staging/midi-note-storage-v1-analysis/traceability.json",
               "plan": "wiki/specs/midi-note-storage-handoff-plan.md#evidence-traceability",
               "review": "handoff/midi-note-storage-v1/REVIEW.md"},
           "x_evidence": {
               "notes": "analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/manifest.json (results/notes.json, "
                        "addresses.json, slice-compare.txt, summary.txt)",
               "minus_zero_reading": "analysis/ableton-live-12.4.3/r2/x2-transport-v1/results/parse.json "
                                     "number_and_bool[text='-0'] (x86 0x10151b630 = arm64 0x10152bfb8, the same text "
                                     "conversion as REQ-002's, n1-0006)",
               "research": "wiki/research/midi-note-storage.md#extracted-execution-results-x2-2026-10-18",
               "functions": "limits x86 0x102a2a7f0 (arm64 0x1028e2c80); note grid 0x102a2a9b0 (0x1028e2e24); event "
                            "grid 0x1026ede60 (0x1025c7a0c); writers P=17 0x10142b980, P=9 0x10142b6c0 (X1)",
               "substitutions": "limits and grid call no import; writers use glibc 2.39 log10 and vsnprintf (C locale); "
                                "the -0 reading uses glibc strtod",
               "arm64": "slice-compare.txt: limits, sign and grid sequences equal for every input class (no FMA effect)",
           },
           "structure_evidence": {
               "spec": "wiki/specs/live-set-structure.md REQ-006, REQ-018 (r1)",
               "audit": "analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json release "
                        "midi-note-storage-v1: 66 fixtures refused by REQ-006 (freeze slot count), minimal addition "
                        "one empty freeze slot; recommended addition one scene (REQ-006 U, Q-022); MNS-012 not "
                        "parseable",
               "checker": "analysis/ableton-live-12.4.3/r2/t11-structure-v1/schema_check.py and fixture_audit.py "
                          "(measure, refusals, unknowns, repairs), imported unchanged",
               "track_group_default": "TrackGroupId is absent in every fixture (as in v1). Corpus pseudocode, not "
                                      "re-read in disassembly: the track initializer FUN_102705a50 "
                                      "(chunk-01903.jsonl offset 78507, code SHA-256 3c23d9df…6d53d97) sets the "
                                      "remoteable at track+0x400 to 0xffffffff with TrackGroupIdNotifier; the getter "
                                      "0x102709884 (chunk-01904.jsonl offset 57284, 32390593…483a06388) tests "
                                      "+0x400 != -1. Absent reads as -1, not grouped; the audit finds no refusal",
           },
           "cases": {}}
    for c in cases:
        cid = c["id"]
        e = {"requirements": c["requirements"], "provenance": c["expectation_provenance"],
             "fixture": "v1 fixture text plus the freeze slot and the scene" if cid in V1_IDS
             else "v1 carrier form (mns_cases.document) plus the freeze slot and the scene"}
        if cid in NEW:
            e["source"] = f"SPEC-MIDI-NOTE-STORAGE r3 {cid}"
            e["x_evidence"] = [f"{xr} {ref} (n{n} {a} text {t!r}, {k}); saved text: {xr} writer_texts[{k}, held value]"
                               + (f"; reading of '-0': analysis/ableton-live-12.4.3/r2/x2-transport-v1/results/"
                                  f"parse.json number_and_bool[{k}, '-0']" if t == "-0" else "")
                               for n, a, t, k, ref in X_EVIDENCE[cid]]
            e["static_steps"] = ("locating the notes, reading decimal text other than -0 (REQ-002 clause 3), opening "
                                 "and saving (as midi-note-storage-v1, evidence keys attrs, omit, fmt, gate)")
        else:
            e["v1"] = v1t["cases"][cid]
            if cid in X_CORROBORATES:
                e["x_corroboration"] = [f"{xr} {ref} (n{n} {a} text {t!r}, {k})" for n, a, t, k, ref in X_CORROBORATES[cid]]
        out["cases"][cid] = e
    return out


def text_diff():
    out = []
    for name in ("README.md", "AGENTS.md", "spec.md"):
        a = (V1 / name).read_text().splitlines(keepends=True)
        b = (STAGE / name).read_text().splitlines(keepends=True)
        out += difflib.unified_diff(a, b, f"midi-note-storage-v1/{name}", f"midi-note-storage-v2/{name}")
    return "".join(out)


def build():
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures").mkdir(parents=True)
    v1doc = json.loads((V1 / "cases.json").read_text())
    v1cases = {c["id"]: c for c in v1doc["cases"]}
    cases = []
    for cid in ORDER_IDS:
        rel = f"fixtures/{cid}.als"
        (STAGE / rel).write_bytes(mc.gz(document(FRAG[cid])))
        if cid in v1cases:
            cases.append(v1cases[cid])
        else:
            kind, reqs, purpose, _, saved = NEW[cid]
            cases.append({"id": cid, "kind": kind, "purpose": purpose, "requirements": [R + r for r in reqs],
                          "input": rel, "action": mc.OS, "expected": {"outcome": mc.LOADS, "saved_notes": saved},
                          "expectation_provenance": PROV_X, "reference_execution": "not-run",
                          "candidate_execution": "not-run", "comparator": mc.COMPARATOR[mc.OS]})
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": v1doc["schema"], "target": v1doc["target"],
        "scope": "midi-note-storage-v2 partial requirement clauses only (see spec.md)",
        "status": "staged candidate; not reviewed; not released",
        "fixture_origin": "Independently authored gzip Live Sets; no shipped file copied or excerpted",
        "oracle_status": "Static-derived and extracted-execution expectations (label per case); neither the reference "
                         "application nor a candidate executed",
        "representation": v1doc["representation"],
        "cases": cases}, indent=1, ensure_ascii=False) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(len(cases)), indent=1) + "\n")
    (HERE / "traceability.json").write_text(json.dumps(traceability(cases), indent=1, ensure_ascii=False) + "\n")
    (HERE / "v1-to-v2-text.diff").write_text(text_diff())
    print(len(cases), "cases staged")


ALLOWED = [PROV_X, "x86_64 build", "x86_64 host", "macOS arm64 build", "glibc in place of the macOS system libraries",
           "the glibc run",  # wording of the provenance label, its definition and the stated assumptions
           "not an executable harness for the original application"]  # carried v1 sentence
DENY = b1.DENY + [r"xexec", r"\bX[12]\b", r"x[12]-", r"from_chars", r"vsnprintf", r"strtod", r"log10\(", r"[Ss]etValue",
                  r"\bgdb\b", r"harness", r"\bstubs?\b", r"\btrap", r"\bslice", r"glibc", r"x86", r"0x[0-9a-f]{6,}",
                  r"cvtsd2ss|fcvt|frint|roundsd|fmadd|minss", r"\bREVIEW\.md\b", r"T11", r"T1\.1", r"\bLSS-", r"LIVE-SET",
                  r"audit", r"validation walk", r"pointee", r"\bQ-02\d", r"make_fixture", r"schema_check", r"\bA[4-7]\b"]


def mutations(cases, x):
    """Mutated expectations: each must be caught by the model, and new cases also by the X check."""
    def first(c):
        return c["expected"]["saved_notes"]["key_tracks"][0]["notes"][0]
    muts = {
        "MNS-028 next id 4": ("MNS-028", lambda c: c["expected"]["saved_notes"].__setitem__("note_id_next", "4")),
        "MNS-003 VelocityDeviation dropped": ("MNS-003", lambda c: first(c).pop("VelocityDeviation")),
        "MNS-004 attribute order reversed": ("MNS-004", lambda c: c["expected"]["saved_notes"]["key_tracks"][0]["notes"]
                                             .__setitem__(0, dict(reversed(list(first(c).items()))))),
        "MNS-020 Time unrounded": ("MNS-020", lambda c: first(c).__setitem__("Time", "0.123456789")),
        "MNS-049b events reversed": ("MNS-049b", lambda c: c["expected"]["saved_notes"]["event_lists"][0]["events"]
                                     .reverse()),
        "MNS-046 outcome loads": ("MNS-046", lambda c: c["expected"].__setitem__("outcome", "loads")),
        "MNS-023 Time 0": ("MNS-023", lambda c: first(c).__setitem__("Time", "0")),
        "MNS-072 Time 0 (exact rounding)": ("MNS-072", lambda c: first(c).__setitem__("Time", "0")),
        "MNS-073 OffVelocity 0": ("MNS-073", lambda c: first(c).__setitem__("OffVelocity", "0")),
        "MNS-074 Velocity -0": ("MNS-074", lambda c: first(c).__setitem__("Velocity", "-0")),
        "MNS-075 Velocity 127.000008": ("MNS-075", lambda c: first(c).__setitem__("Velocity", "127.000008")),
    }
    by_id = {c["id"]: c for c in cases}
    out = {}
    for name, (cid, mutate) in muts.items():
        c = copy.deepcopy(by_id[cid])
        mutate(c)
        hit_model = bool(mm.judge(c, model((STAGE / c["input"]).read_bytes())))
        hit_x = bool(x_check(c, X_EVIDENCE[cid], x)) if cid in X_EVIDENCE else None
        out[name] = "detected" if hit_model and hit_x is not False else f"MISSED (model {hit_model}, X {hit_x})"
    return out


PROBES = {k: v for k, v in mc.PROBES.items() if k != "Time -0.0000001 (negative zero)"} | {
    "VelocityDeviation -0": mc.F(mc.f0, mc.n(1, VelocityDeviation="-0")),
    "event Value -0": mc.F(mc.f1, mc.e(1, Value="-0")),
    "curve control -0": mc.F(mc.f1, mc.e(1, CurveControl1X="-0")),
    "event TimeOffset -0 (at offset 0)": mc.F(mc.f1, mc.e(1, TimeOffset="-0")),
    "Time 1000000": mc.F(mc.f0, mc.n(2, Time="1000000")),
}


def probe_report():
    out = {}
    for name, frag in PROBES.items():
        got = model(mc.gz(document(frag)))
        ok = got[0] == "no-expectation" or (got[0] == "loads" and got[1] is None)
        out[name] = ("no expectation" if got[0] == "no-expectation" else "loads; saved notes undetermined") if ok \
            else f"UNEXPECTED {got[0]}"
    return out


def check(pkg, rewrite):
    pkg = pkg.resolve()
    doc_ = json.loads((pkg / "cases.json").read_text())
    x = x_results()
    v1cases = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
    problems, x_problems, form = {}, {}, []
    for c in doc_["cases"]:
        raw = (pkg / c["input"]).read_bytes()
        errs = mm.judge(c, model(raw))
        if errs:
            problems[c["id"]] = errs
        d = zlib.decompressobj(31)
        txt = d.decompress(raw)
        if raw[:10] != mc.GZ_HEADER or not d.eof or d.unused_data or b"\r" in txt or not txt.endswith(b"\n"):
            form.append(c["id"])
        if c["id"] in X_EVIDENCE and (xe := x_check(c, X_EVIDENCE[c["id"]], x)):
            x_problems[c["id"]] = xe
    carry = {"records_changed": [], "fixture_text_not_v1_plus_additions": [], "new_fixture_not_v1_form": []}
    for c in doc_["cases"]:
        stripped = strip_structure(unzip((pkg / c["input"]).read_bytes()))
        if c["id"] in v1cases:
            if c != v1cases[c["id"]]:
                carry["records_changed"].append(c["id"])
            if stripped != unzip((V1 / c["input"]).read_bytes()):
                carry["fixture_text_not_v1_plus_additions"].append(c["id"])
        elif stripped != mc.document(FRAG[c["id"]]).decode("utf-8"):
            carry["new_fixture_not_v1_form"].append(c["id"])
    corroboration = {cid: x_check(next(c for c in doc_["cases"] if c["id"] == cid), ev, x) or "agrees"
                     for cid, ev in X_CORROBORATES.items()}
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                             for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}

    def scan(p):
        t = re.sub(r"\s+", " ", re.sub(r"\b[0-9a-f]{64}\b", "", b1.text_of(p)))  # digests are not text
        for a in ALLOWED:
            t = t.replace(a, "")
        return sorted({m for pat in DENY for m in re.findall(pat, t)} - b1.ALLOWED_HITS.get(p.name, set()))
    return {
        "cases": len(doc_["cases"]), "manifest_case_count": manifest["case_count"],
        "outcomes": {o: sum(c["expected"]["outcome"] == o for c in doc_["cases"]) for o in ("loads", "refused")},
        "actions": {a: sum(c["action"] == a for c in doc_["cases"]) for a in ("open", "open-save")},
        "provenance_counts": {k: sum(c["expectation_provenance"] == k for c in doc_["cases"])
                              for k in sorted({c["expectation_provenance"] for c in doc_["cases"]})},
        "case_problems": problems, "x_evidence_problems": x_problems,
        "x_corroboration_of_carried_cases": corroboration,
        "carried_cases": sum(c["id"] in v1cases for c in doc_["cases"]), "carry": carry,
        "fixture_form_problems": form,
        "distinct_inputs": len({(pkg / c["input"]).read_bytes() for c in doc_["cases"]}),
        "structure": structure_report(pkg, doc_["cases"]),
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(b1.links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in b1.links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in b1.links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in doc_["cases"] if not (pkg / c["input"]).is_file()],
        "deny_list_hits": {str(p.relative_to(pkg)): h for p in [*files, pkg / "manifest.json"] if (h := scan(p))},
        "limits": "Checks authored consistency, the Live Set structure rules of the T11 checker and agreement with the "
                  "retained extracted-execution results only: neither the reference application nor a candidate was "
                  "executed; the cross-check model restates the same evidence and is not an oracle.",
    }


def selfcheck():
    assert fmt(-0.0, 17) == "-0" and fmt(0.0, 9) == "0" and fmt(127.0, 9) == "127"
    assert grid(-0.0) == 0 and not neg0(grid(-0.0)) and neg0(grid(-1e-07))
    assert dbits(grid(float("0.00000013007825507825505"))) == dbits(1 / 3843840)
    assert add_structure(strip_structure(document(mc.f0()).decode())) == document(mc.f0()).decode()


if __name__ == "__main__":
    selfcheck()
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        rep = check(STAGE, rewrite=True)
        rep = {"schema": "author-validation-v1", "package": "midi-note-storage-v2 (staged candidate)",
               "python": sys.version.split()[0], "zlib": zlib.ZLIB_RUNTIME_VERSION, **rep,
               "excluded_input_probes": probe_report(), "mutated_expectations": mutations(
                   json.loads((STAGE / "cases.json").read_text())["cases"], x_results())}
        (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
        print(json.dumps({k: v for k, v in rep.items() if k not in ("x_corroboration_of_carried_cases",)},
                         indent=1, ensure_ascii=False))
    elif cmd == "verify":
        print(json.dumps(check(Path(sys.argv[2]), rewrite=False), indent=1, ensure_ascii=False))
