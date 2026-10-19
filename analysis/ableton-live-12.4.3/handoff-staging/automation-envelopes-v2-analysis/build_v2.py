"""Stage the automation-envelopes-v2 candidate (analyst side, never shipped).

Run with CPython 3.13 and -I -B, from any directory (set TMPDIR to a scratch folder for the audit copy):
  python3 -I -B build_v2.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3 -I -B build_v2.py seal           # checks, manifest files[], author-validation.json, traceability.json,
                                           # t11-fixture-audit.json, t11-schema-check.jsonl
  python3 -I -B build_v2.py verify <dir>   # hashes, inventory, links, case inputs, deny list of a copy

Inputs (read only):
  - automation-envelopes-v1-analysis/build_aen.py and crosscheck_model.py: the v1 template, event lists, case
    expectations and cross-check model, imported unchanged;
  - handoff/automation-envelopes-v1/: the released v1 case records and fixtures (carried records must match);
  - r2/t11-structure-v1/: released-fixture-audit.json (the additions each v1 fixture needs), schema_check.py and
    fixture_audit.py (the structural checker), with the shipped schema 12.0_12402.
Every v2 fixture is a v1-form document (the v1 template plus the case's envelopes) with the T11 additions
inserted as whole lines: one empty session slot and one empty freeze slot on the audio track, one empty freeze
slot on the MIDI track, and one scene. No line of the v1-form document changes. seal() proves that for every
carried case the fixture equals t11(v1 released fixture), and that every fixture passes the T11 checker with no
refusal, no unknown shape and no schema deviation.
"""
import copy, difflib, hashlib, json, math, os, re, shutil, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from decimal import Decimal, localcontext
from pathlib import Path

sys.dont_write_bytecode = True  # never write a cache into the v1 or T11 directories
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "automation-envelopes-v2"
V1A = HERE.parent / "automation-envelopes-v1-analysis"
V1R = ROOT / "handoff/automation-envelopes-v1"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
S6 = ROOT / "analysis/ableton-live-12.4.3/r2/s6-automation-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
CORPUS = Path("/var/tmp/sound-analysis/corpus/decomp/chunks")
sys.path[:0] = [str(HERE), str(V1A), str(T11)]
import build_aen as v1  # noqa: E402  (template, event lists, CASES, verify, links)
import crosscheck_model as cm  # noqa: E402
import fixture_audit as fa  # noqa: E402
from schema_check import load_schema  # noqa: E402

L, F, B, N = v1.L, cm.F, cm.B, cm.N
OPENS, REFUSED = cm.OPENS, cm.REFUSED
PROV = v1.PROV
V1_MANIFEST_SHA = "793c1d7d5432de529c21c628e7fa6c46eecb1fa9128a4da9db1d1dfc34378302"

# ---- T11 additions, in the v1 fixtures' tab-indented form (fixture_audit FREEZE_SLOT and SCENE) ----
def _slots(tag, d):
    t = "\t" * d
    return [f"{t}<{tag}>", f"{t}\t<ClipSlotList>", f'{t}\t\t<ClipSlot Id="0">', f"{t}\t\t\t<ClipSlot>",
            f"{t}\t\t\t\t<Value />", f"{t}\t\t\t</ClipSlot>", f'{t}\t\t\t<HasStop Value="true" />',
            f"{t}\t\t</ClipSlot>", f"{t}\t</ClipSlotList>", f"{t}</{tag}>"]


SCENES = ["\t\t<Scenes>", '\t\t\t<Scene Id="0">', '\t\t\t\t<Name Value="" />', '\t\t\t\t<Color Value="-1" />',
          '\t\t\t\t<Tempo Value="120" />', '\t\t\t\t<IsTempoEnabled Value="false" />',
          '\t\t\t\t<TimeSignatureId Value="201" />', '\t\t\t\t<IsTimeSignatureEnabled Value="false" />',
          "\t\t\t</Scene>", "\t\t</Scenes>"]
# anchor line -> block inserted directly after it (the anchors are unique in every v1-form document)
ADDITIONS = [
    ("\t\t\t\t\t</Mixer>", _slots("MainSequencer", 5) + _slots("FreezeSequencer", 5),
     "audio track: MainSequencer and FreezeSequencer, one empty clip slot each, after Mixer"),
    ("\t\t\t\t\t</MainSequencer>", _slots("FreezeSequencer", 5),
     "MIDI track: FreezeSequencer with one empty clip slot, after MainSequencer"),
    ("\t\t</Tracks>", SCENES, "LiveSet: Scenes with one scene, after Tracks"),
]
TIMELINE = ["\t\t\t\t\t\t<ClipTimeable>", "\t\t\t\t\t\t\t<ArrangerAutomation>", "\t\t\t\t\t\t\t\t<Events />",
            "\t\t\t\t\t\t\t\t<AutomationTransformViewState>", '\t\t\t\t\t\t\t\t\t<IsTransformPending Value="false" />',
            "\t\t\t\t\t\t\t\t\t<TimeAndValueTransforms />", "\t\t\t\t\t\t\t\t</AutomationTransformViewState>",
            "\t\t\t\t\t\t\t</ArrangerAutomation>", "\t\t\t\t\t\t</ClipTimeable>"]


def insert_after(data, pairs):
    """Insert whole lines after unique anchor lines; assert that removing them gives the input back."""
    lines = data.decode("ascii").split("\n")
    at = []
    for anchor, block in pairs:
        idx = [i for i, x in enumerate(lines) if x == anchor]
        assert len(idx) == 1, (anchor, idx)
        at.append((idx[0], block))
    out, added = [], set()
    pos = dict(at)
    for i, x in enumerate(lines):
        out.append(x)
        for y in pos.get(i, []):
            added.add(len(out))
            out.append(y)
    assert [x for i, x in enumerate(out) if i not in added] == lines
    return "\n".join(out).encode("ascii")


def t11(data):
    return insert_after(data, [(a, b) for a, b, _ in ADDITIONS])


def with_timeline(data):  # the MIDI track's MainSequencer: ClipSlotList, ClipTimeable, MidiControllers
    return insert_after(data, [("\t\t\t\t\t\t</ClipSlotList>", TIMELINE)])


# ---- cases ----
V1_CASES = {c[0]: c for c in v1.CASES}
CARRIED = [1, 2, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
NOT_CARRIED = {
    3: "track envelope whose only event is at 4, expected refused",
    4: "track envelope with an empty event list, expected refused",
    11: "clip envelope whose only event is at 4, expected refused",
}
pan = lambda pairs: v1.doc([v1.track_env("Pan", v1.events(F, pairs))])
clip = lambda pairs: v1.doc(clip=[v1.clip_env(v1.events(F, pairs))])
NEW = [
    (30, "Pan envelope with two events, the first at 4", ["007"], pan([("4", "0"), ("8", "1")]), "open",
     {"outcome": REFUSED}),
    (31, "Clip envelope on MIDI controller target 6 with two events, the first at 4", ["007"],
     clip([("4", "127"), ("8", "127")]), "open", {"outcome": REFUSED}),
    (32, "The clip envelope of case 010, and an empty event list in the MIDI track's arrangement clip timeline",
     ["001", "007"], with_timeline(V1_CASES[10][3]), "open", {"outcome": OPENS}),
]
# Isolation controls: each refused fixture with only the tested defect repaired (must open, structure unchanged)
CONTROLS = {
    8: pan([(L, "0"), ("4", "1")]),
    12: V1_CASES[10][3],
    13: pan([(L, "0"), ("4", "0.5")]),
    14: v1.doc([v1.track_env("Speaker", v1.events(B, [(L, "true"), ("4", "false")]))]),
    15: v1.doc([v1.track_env("CrossFadeState", v1.events(N, [(L, "1"), ("4", "2")]))]),
    30: pan([(L, "0"), ("8", "1")]),
    31: clip([(L, "127"), ("8", "127")]),
}


def all_cases():
    """(number, purpose, requirement suffixes, v1-form bytes, action, expected, origin)."""
    rows = [(*V1_CASES[n], "carried") for n in CARRIED]
    rows += [(*c, "new") for c in NEW]
    return [(n, p, r, t11(d), a, e, o) for n, p, r, d, a, e, o in rows]


COMPARATOR = v1.COMPARATOR
SCOPES = {
    "REQ-AUTOMATION-ENVELOPES-001": "Track envelopes in a track's AutomationEnvelopes/Envelopes, clip envelopes in a clip's Envelopes/Envelopes; AutomationEnvelope and ClipEnvelope shape with EnvelopeTarget/PointeeId and Automation/Events; empty transform state; the MIDI track's arrangement clip timeline (MainSequencer/ClipTimeable/ArrangerAutomation) has the same Events shape and is not an envelope",
    "REQ-AUTOMATION-ENVELOPES-002": v1.SCOPES["REQ-AUTOMATION-ENVELOPES-002"],
    "REQ-AUTOMATION-ENVELOPES-003": v1.SCOPES["REQ-AUTOMATION-ENVELOPES-003"],
    "REQ-AUTOMATION-ENVELOPES-005": "A document whose track envelope holds a single event, at the lower bound, opens; whether that envelope is kept is not specified",
    "REQ-AUTOMATION-ENVELOPES-006": v1.SCOPES["REQ-AUTOMATION-ENVELOPES-006"],
    "REQ-AUTOMATION-ENVELOPES-007": "Empty event list of a clip envelope refused; for track and clip envelopes with at least two events, first event time other than the lower bound or 0 refused (binary64 comparison, -0 counts as 0); later times not checked; an empty arrangement clip timeline of the MIDI track does not cause a refusal (stated assumption). No expectation for a track envelope with fewer than two events other than one event at the lower bound, or for a clip envelope with exactly one event",
    "REQ-AUTOMATION-ENVELOPES-008": v1.SCOPES["REQ-AUTOMATION-ENVELOPES-008"],
    "REQ-AUTOMATION-ENVELOPES-009": v1.SCOPES["REQ-AUTOMATION-ENVELOPES-009"],
    "REQ-AUTOMATION-ENVELOPES-012": "Event text on open (Time and controls as decimal binary64, Float Value then binary32, Bool tokens, integer rule; refusal of rejected text) and on save (17 and 9 significant digits with k taken from the binary64 base-10 logarithm, true or false, decimal integers)",
}
EXCL_INPUTS = [
    v1.EXCL_INPUTS[0], v1.EXCL_INPUTS[1], v1.EXCL_INPUTS[2], v1.EXCL_INPUTS[3], v1.EXCL_INPUTS[4],
    v1.EXCL_INPUTS[5], v1.EXCL_INPUTS[6],
    "a track envelope with no event, or with one event at a time other than L; a clip envelope with exactly one event",
    "saved binary64 values (Time, curve controls) whose log10 is not an integer but lies between 1/4 and 3/4 of a binary64 gap from one",
    v1.EXCL_INPUTS[7],
    "elements outside AutomationEnvelope and ClipEnvelope that use the same Events shape, other than an empty Events list in the MIDI track's arrangement clip timeline: a non-empty timeline, and the timelines of audio tracks, samples and take lanes",
    "Live Set structure other than the fixtures' (see spec.md): other tracks, devices, scenes, clips and clip slots, main and cue tracks, sends and returns",
    v1.EXCL_INPUTS[9], v1.EXCL_INPUTS[10],
]
EXCL_BEHAVIOR = [
    "the value an envelope supplies to its parameter at any time, for Float, Bool and Enum envelopes, track and clip envelopes alike (REQ-AUTOMATION-ENVELOPES-010 and 011), including at event times, after the last event and between equal values, and whether event Ids affect it (REQ-AUTOMATION-ENVELOPES-004): no externally observable reading of the value computed from the stored events has been established, and the value applied while the transport plays rests on conditions not yet established for a document that has just been opened",
    "whether opening keeps an envelope with fewer than two events",
    v1.EXCL_BEHAVIOR[1],
    v1.EXCL_BEHAVIOR[2],
    v1.EXCL_BEHAVIOR[3], v1.EXCL_BEHAVIOR[4], v1.EXCL_BEHAVIOR[5],
]
ASSUMPTIONS = [
    "BoolEvent and EnumEvent values are read and written with the Boolean and integer text rules of REQ-AUTOMATION-ENVELOPES-012 (the format declares them Boolean and integer). Cases 014, 015 and 021 depend on it.",
    "A save keeps each envelope bound to its target. Every open-save case (001, 016 to 021) depends on it.",
    "No step that runs when a document is opened refuses an empty Events list in the MIDI track's arrangement clip timeline. Case 032 depends on it.",
    "Where its last bit decides k on save (REQ-AUTOMATION-ENVELOPES-012 step 1), the reference's binary64 base-10 logarithm errs by less than 3/4 of a binary64 gap, outside the excluded band. No case lies next to a power of ten, so no case depends on it.",
]
FIXTURE_CHANGES = {
    "carried": "Each carried fixture is the automation-envelopes-v1 file of the same name with 40 lines inserted and no line changed, removed or reordered",
    "insertions": [desc + f" ({len(block)} lines)" for _, block, desc in ADDITIONS],
    "new": "fixtures/AUTOMATION-ENVELOPES-030.xml to 032.xml use the same template and insertions; 032 also has the 9-line arrangement clip timeline in the MIDI track's MainSequencer, between ClipSlotList and MidiControllers",
    "not_carried": [f"fixtures/{v1.cid(n)}.xml" for n in NOT_CARRIED],
}
CHANGES = [
    "Fixtures: every fixture gains one empty session and one empty freeze clip slot on the audio track, one empty freeze clip slot on the MIDI track and one scene (40 lines). A Live Set whose audio or MIDI track has a different number of session and freeze clip slots is not opened, and every automation-envelopes-v1 fixture had a session clip slot on its MIDI track and no freeze sequencer; the session slot and scene make each track hold one slot per scene. No v1 line changes",
    "Not carried: cases 003, 004 and 011. Each expected a refusal for an envelope with fewer than two events (a track envelope whose only event is at 4, a track envelope with no event, a clip envelope whose only event is at 4). Whether opening keeps such an envelope is not established, so the refusal does not follow; these inputs now have no expectation. automation-envelopes-v1's REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 are narrowed accordingly",
    "New cases 030 and 031 test the first-event time check with two events (track and clip envelope). IDs 022 to 029 were withdrawn before automation-envelopes-v1 was released and are not reused",
    "New clause and case 032: an empty Events list in the MIDI track's arrangement clip timeline does not make the document refused (stated assumption); the exclusion of that element is narrowed",
    "REQ-AUTOMATION-ENVELOPES-012 save step 1 corrected: k comes from the binary64 base-10 logarithm, as in transport-state-v2; values in the band where its last bit is not established are excluded. No v1 case is affected",
    "Assumption removed: opening a Live Set applies the checks of REQ-AUTOMATION-ENVELOPES-007 is now static-derived",
    "REQ-AUTOMATION-ENVELOPES-005 restated: the document opens; whether the one-event envelope is kept is excluded",
    "Unchanged: every other clause, the 18 carried case records and every expectation; the value an envelope supplies at a time stays unreleased (REQ-AUTOMATION-ENVELOPES-010 and 011), with the reason stated",
]
REVIEW = {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None}


def manifest_meta(n_cases):
    return {
        "schema": "handoff-manifest-v1", "release_id": "automation-envelopes-v2",
        "release_status": "staged candidate; not reviewed; not released", "release_date": None, "target": v1.TARGET,
        "specification": {"id": "SPEC-AUTOMATION-ENVELOPES", "parent_revision": 4, "release_revision": 4},
        "feature_ids": ["FEAT-AUTOMATION", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": SCOPES,
        "unreleased_requirements": ["REQ-AUTOMATION-ENVELOPES-004", "REQ-AUTOMATION-ENVELOPES-010",
                                    "REQ-AUTOMATION-ENVELOPES-011", "REQ-AUTOMATION-ENVELOPES-013"],
        "compatibility_dimensions": {
            "envelope-storage-and-load-checks": "static-derived expectations; reference execution not-run",
            "file-format-written": "saved event text only, static-derived; reference execution not-run",
            "envelope-value-at-time": "excluded (REQ-AUTOMATION-ENVELOPES-010 and 011 unreleased; reason in spec.md)",
            "editing-and-ui": "excluded (REQ-AUTOMATION-ENVELOPES-013)",
            "audio": "excluded", "timing": "excluded",
        },
        "expectation_provenance_labels": {PROV: "derived from evidence reviewed before sanitization; no case is an observation of the original application"},
        "stated_assumptions": ASSUMPTIONS,
        "exclusions": {"inputs_without_expectation": EXCL_INPUTS, "behavior": EXCL_BEHAVIOR},
        "fixture_origin": "independently authored minimal Live Set XML documents from one template; no shipped file content, schema content or program code",
        "approved_public_sources": [],
        "review": REVIEW,
        "supersedes": "automation-envelopes-v1",
        "supersession": {
            "relationship": "corrective and narrowing: automation-envelopes-v1 stays immutable, but its fixtures must not be used to judge that a document opens, and its cases 003, 004 and 011 and its REQ-AUTOMATION-ENVELOPES-007 clauses 1 and 2 for envelopes with fewer than two events must not be relied on",
            "superseded_manifest_sha256": V1_MANIFEST_SHA,
            "restated_cases": "AUTOMATION-ENVELOPES-001, 002, 005 to 010 and 012 to 021: case records identical to automation-envelopes-v1; fixtures changed as in fixture_changes",
            "not_carried": [v1.cid(n) for n in NOT_CARRIED],
            "new_cases": [v1.cid(c[0]) for c in NEW],
            "changes": CHANGES,
            "fixture_changes": FIXTURE_CHANGES,
        },
        "entrypoint": "README.md", "case_count": n_cases,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    fx = STAGE / "fixtures"
    if fx.exists():
        shutil.rmtree(fx)
    fx.mkdir(parents=True)
    cases = []
    for n, purpose, reqs, data, action, expected, origin in all_cases():
        rel = f"fixtures/{v1.cid(n)}.xml"
        (STAGE / rel).write_bytes(data)
        cases.append({"id": v1.cid(n), "purpose": purpose, "requirements": v1.req(reqs), "input": rel,
                      "action": action, "expected": expected, "expectation_provenance": PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run",
                      "comparator": COMPARATOR[action]})
    doc_ = {"schema": "automation-envelopes-cases-v1", "target": v1.TARGET,
            "scope": "automation-envelopes-v2 partial requirement clauses only (see spec.md)",
            "status": "staged candidate; not reviewed",
            "fixture_origin": "Independently authored minimal documents; no shipped file copied",
            "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
            "representation": {
                "action": "open or open-save",
                "outcome": "opens or refused",
                "saved": "open-save only: per listed target, the saved envelope's events in order with exact attribute text other than Id",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1, ensure_ascii=True) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(len(cases)), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- cross-check model: v1 model plus the v2 narrowing and the corrected save step 1 ----
def fmt_v2(x, p):
    """REQ-012 save rule with k from the binary64 logarithm L (correctly rounded here); band without expectation."""
    if x == 0:
        if math.copysign(1, x) < 0:
            raise cm.NoExpectation("negative zero on save")
        return "0"
    with localcontext() as ctx:
        ctx.prec = 60
        lg = Decimal(abs(x)).log10()
    n = int(lg.to_integral_value())
    if lg != n and abs(lg - n) < Decimal("1e-9"):
        gap = Decimal(math.nextafter(float(n), math.inf if lg > n else -math.inf)) - n
        if Decimal("0.25") <= abs((lg - n) / gap) <= Decimal("0.75"):
            raise cm.NoExpectation("log10 in the band without expectation")
    lb = float(lg)  # nearest binary64 to log10|x|
    k = math.ceil(lb) if lb >= 0 else math.floor(lb)
    s = format(Decimal(x), f".{max(0, p - k)}f")
    return s.rstrip("0").rstrip(".") if "." in s else s


cm.fmt = fmt_v2  # save_text() looks fmt up in its module


def model(data, action, expected):
    root = ET.fromstring(data)
    for env in root.iter():
        if env.tag not in ("AutomationEnvelope", "ClipEnvelope"):
            continue
        evs = list(env.find("Automation/Events"))
        if env.tag == "AutomationEnvelope" and len(evs) < 2 and not (
                len(evs) == 1 and cm.read_double(evs[0].get("Time", "")) == cm.LOW):
            raise cm.NoExpectation("track envelope with fewer than two events")
        if env.tag == "ClipEnvelope" and len(evs) == 1:
            raise cm.NoExpectation("clip envelope with exactly one event")
    return cm.model(data, action, expected)


# ---- T11 structure checks ----
_SCHEMA = None


def structure(data):
    """T11 checker on one document: (traced refusals, unknown shapes, schema deviations)."""
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = load_schema(str(SCHEMA))
        fa.LIVESET_ORDER[:] = list(_SCHEMA["LiveSet"])
    root = ET.fromstring(data)
    dev, r = fa.measure(_SCHEMA, root)
    return fa.refusals(r, dev), fa.unknowns(r), dev


def run_t11_cli():
    """Run the T11 checkers' own command lines on a copy of the staging tree (read-only on T11)."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(STAGE, Path(tmp) / "automation-envelopes-v2")
        out = Path(tmp) / "audit.json"
        r = subprocess.run([sys.executable, "-I", "-B", str(T11 / "fixture_audit.py"), str(SCHEMA), tmp, str(out)],
                           capture_output=True, text=True, check=True)
        audit = json.loads(out.read_text())
    files = sorted(str(p) for p in (STAGE / "fixtures").glob("*.xml"))
    sc = subprocess.run([sys.executable, "-I", "-B", str(T11 / "schema_check.py"), str(SCHEMA), *files],
                        capture_output=True, text=True, check=True).stdout
    rows = [json.loads(x) for x in sc.splitlines()]
    for x in rows:
        x["doc"] = os.path.relpath(x["doc"], STAGE)
    (HERE / "t11-schema-check.jsonl").write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows))
    rel = audit["releases"][0]
    audit["note"] = "fixture_audit.py run by build_v2.py seal on a temporary copy of the staging directory"
    (HERE / "t11-fixture-audit.json").write_text(json.dumps(audit, indent=1) + "\n")
    return {"fixture_audit_totals": audit["totals"], "fixture_audit_summary": rel["summary"],
            "fixture_audit_stdout": r.stdout.strip(),
            "schema_check_deviations": {x["doc"]: x["deviations"] for x in rows if x.get("deviations") or "error" in x}}


# ---- evidence identity ----
def evidence_identity():
    out = v1.evidence_identity()
    t = json.loads((T11 / "manifest.json").read_text())
    out["t11_manifest_files"] = len(t["files"])
    out["t11_mismatches"] = [p for p, f in t["files"].items()
                             if not (T11 / p).is_file() or v1.sha((T11 / p).read_bytes()) != f["sha256"]]
    bad = []
    for line in (HERE / "purge-excerpts.jsonl").read_text().splitlines():
        r = json.loads(line)
        with open(CORPUS / r["chunk"], "rb") as fh:
            fh.seek(r["offset"])
            raw = fh.readline().rstrip(b"\n")
        if hashlib.sha256(raw).hexdigest() != r["line_sha256"]:
            bad.append(r["record"]["entry"])
    out["purge_excerpts_checked_against_corpus"] = sum(1 for _ in (HERE / "purge-excerpts.jsonl").open())
    out["purge_excerpt_mismatches"] = bad
    return out


def probes():
    """Excluded inputs must give no expectation in the model; the save-rule example must reproduce."""
    p = lambda pairs, **kw: t11(v1.doc([v1.track_env("Pan", v1.events(F, pairs, **kw))]))
    rows = [
        ("dangling PointeeId", t11(v1.doc([v1.track_env("Pan", v1.events(F, v1.E1))])).replace(b'PointeeId Value="22"', b'PointeeId Value="39"'), "open"),
        ("track envelope with an empty list", t11(v1.doc([v1.track_env("Pan", [])])), "open"),
        ("track envelope with one event at 4", p([("4", "0")]), "open"),
        ("clip envelope with one event at the lower bound", t11(clip([(L, "127")])), "open"),
        ("events in time disorder", p([(L, "0"), ("8", "-0.5"), ("4", "0.5")]), "open"),
        ("duplicate event Ids", p([(L, "0"), ("4", "0.5")], ids=[0, 0]), "open"),
        ("event without Time", p([(L, "0"), (None, "0.5")]), "open"),
        ("event without Value", p([(L, "0"), ("4", None)]), "open"),
        ("three events at one time", p([(L, "0"), ("4", "0"), ("4", "1"), ("4", "0")]), "open"),
        ("value out of range", p([(L, "0"), ("4", "2")]), "open"),
        ("hexadecimal time", p([(L, "0"), ("0x4", "1")]), "open"),
        ("controls not satisfying K", p(v1.E9P, curves={1: {"CurveControl1X": "0.2", "CurveControl1Y": "1.5", "CurveControl2X": "0.8", "CurveControl2Y": "-0.5"}}), "open"),
    ]
    out = {}
    for name, data, action in rows:
        try:
            out[name] = model(data, action, {"outcome": OPENS})["outcome"] + " (expectation produced)"
        except cm.NoExpectation as e:
            out[name] = f"no expectation: {e}"
    near = {"Time 1000.0000000000001": fmt_v2(1000.0000000000001, 17),
            "Time 0.000001": fmt_v2(0.000001, 17)}
    out["save step 1 examples (transport-state-v2 wording)"] = near
    assert near == {"Time 1000.0000000000001": "1000.00000000000011", "Time 0.000001": "0.00000099999999999999995"}
    return out


def v1_records():
    return {c["id"]: c for c in json.loads((V1R / "cases.json").read_text())["cases"]}


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    v1rec = v1_records()
    built = {v1.cid(n): (d, o) for n, _, _, d, _, _, o in all_cases()}
    problems, fixtures, mutants, isolation = {}, {}, 0, {}
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        errs = []
        got = None
        try:
            got = model(raw, c["action"], c["expected"])
        except cm.NoExpectation as e:
            errs.append(f"model: no expectation ({e})")
        if got is not None and not cm.same(got, c["expected"]):
            errs.append(f"model {got} != expected")
        try:
            m = cm.mutate(c["expected"])
            if got is not None and cm.same(model(raw, c["action"], m), m):
                errs.append("mutated expectation not detected")
            else:
                mutants += 1
        except cm.NoExpectation:
            mutants += 1
        ref, unk, dev = structure(raw)
        if ref or unk or dev:
            errs.append(f"T11: refusals {ref}, unknown shapes {unk}, schema deviations {dev}")
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n"):
            errs.append("not ASCII with LF endings")
        if raw != built[c["id"]][0]:
            errs.append("fixture differs from the build")
        if built[c["id"]][1] == "carried":
            v1raw = (V1R / c["input"]).read_bytes()
            if raw != t11(v1raw):
                errs.append("not equal to the v1 released fixture with the T11 insertions")
            if c != v1rec[c["id"]]:
                errs.append("case record differs from automation-envelopes-v1")
        if errs:
            problems[c["id"]] = errs
        fixtures[c["id"]] = {"bytes": len(raw), "lines": raw.count(b"\n"), "sha256": v1.sha(raw)}
    for n, base in CONTROLS.items():
        ctrl = t11(base)
        case = (STAGE / f"fixtures/{v1.cid(n)}.xml").read_bytes()
        ref, unk, dev = structure(ctrl)
        out = model(ctrl, "open", {"outcome": OPENS})["outcome"]
        ops = difflib.SequenceMatcher(None, case.split(b"\n"), ctrl.split(b"\n"), autojunk=False).get_opcodes()
        diff = {"case_lines_replaced": sum(i2 - i1 for t, i1, i2, _, _ in ops if t != "equal"),
                "control_lines": sum(j2 - j1 for t, _, _, j1, j2 in ops if t != "equal")}
        isolation[v1.cid(n)] = {"control_outcome": out, "control_t11": [ref, unk, dev], "differing_lines": diff}
        if out != OPENS or ref or unk or dev:
            problems.setdefault(v1.cid(n), []).append(f"isolation control failed: {isolation[v1.cid(n)]}")
    by_hash = {}
    for k, v in fixtures.items():
        by_hash.setdefault(v["sha256"], []).append(k)
    t11_cli = run_t11_cli()
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": v1.sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in v1.payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "automation-envelopes-v2 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "mutated_expectations_detected": f"{mutants}/{len(cases)}",
              "refusal_isolation_controls": isolation,
              "identical_fixture_inputs": [v for v in by_hash.values() if len(v) > 1],
              "excluded_input_probes": probes(), "t11_checker": t11_cli, "fixtures": fixtures,
              "evidence_identity": evidence_identity(), **verify(STAGE),
              "limits": "Checks authored consistency and the T11 structure rules as implemented by its checker: no "
                        "reference or candidate executed; the model restates the same static evidence and is not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    diff = []
    for name in ("README.md", "AGENTS.md", "spec.md"):
        diff += difflib.unified_diff((V1R / name).read_text().splitlines(True), (STAGE / name).read_text().splitlines(True),
                                     f"automation-envelopes-v1/{name}", f"automation-envelopes-v2/{name}")
    (HERE / "v1-to-v2-text.diff").write_text("".join(diff))
    from trace_v2 import trace
    tr = trace([c["id"] for c in cases])
    (HERE / "traceability.json").write_text(json.dumps(tr, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "mutated_expectations_detected",
                                             "refusal_isolation_controls", "identical_fixture_inputs",
                                             "excluded_input_probes", "t11_checker", "evidence_identity",
                                             "payload_files", "hash_or_size_mismatches", "inventory_differences",
                                             "unresolved_links", "missing_case_inputs", "deny_list_hits",
                                             "manifest_sha256")}, indent=1))


DENY = [r"(?<!Clip)Timeable\w*" if x == r"Timeable\w*" else x for x in v1.DENY] + [r"T11", r"make_fixture", r"fixture_audit", r"schema_check", r"\baudit", r"\bwalk\b", r"[Pp]urg",
                  r"half-dangling", r"evaluator", r"point list", r"\b[EP]\(t\)", r"\bLSS-", r"\bMG-", r"\bRVE-",
                  r"SPEC-(?!AUTOMATION-ENVELOPES)", r"REQ-(?!AUTOMATION-ENVELOPES)", r"\bglibc", r"slot \+",
                  r"\bI[7-9]\b", r"\bF[1-9]\b", r"\bQ-\d", r"mode [01]", r"build_v2", r"trace_v2"]


def verify(d):
    v1.DENY[:] = DENY  # v1.verify reads its module's DENY
    return v1.verify(d)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
