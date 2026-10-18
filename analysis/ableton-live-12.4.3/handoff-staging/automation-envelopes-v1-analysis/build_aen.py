"""Stage the automation-envelopes-v1 release (analyst side). Narrowed by the 2026-10-18 handoff review (REVIEW.md).

Run with CPython 3.13 and -I, from any directory:
  python3 -I build_aen.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3 -I build_aen.py seal           # manifest files[], author-validation.json, traceability.json
  python3 -I build_aen.py verify <dir>   # hashes, inventory, links, case inputs, deny list of a copy

Fixtures are written here from one template authored for this release; no shipped file is read.
Expected results in CASES are hand-authored static derivations from SPEC-AUTOMATION-ENVELOPES r1.
The seal step cross-checks every expectation against crosscheck_model.model(), an independent
restatement of the released clauses (load checks, event text, saved text, envelope value at t). It shares the same
static evidence and is not an oracle. README.md, AGENTS.md and spec.md are hand-written.
"""
import hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # -I leaves the script directory off sys.path; the siblings are our own modules
sys.dont_write_bytecode = True
from crosscheck_model import B, CC, F, N, OPENS, REFUSED, NoExpectation, model, mutate, same  # noqa: E402
from trace_aen import EV, INF, NOT_RELEASED, TRACE  # noqa: E402

ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "automation-envelopes-v1"
S6 = ROOT / "analysis/ableton-live-12.4.3/r2/s6-automation-v1"
IMAGE = ROOT / "analysis/ableton-live-12.4.3/derived/Live.arm64"
IMAGE_SHA = "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
PROV = "static-derived; not observed reference output"
PROV_V = "static-derived envelope value at the stated times; not observed reference output and not rendered output"
L = "-63072000"
TID = {"Speaker": "21", "Pan": "22", "CrossFadeState": "23", "ControllerTargets.6": "31"}


# ---- fixture authoring ----
def events(cls, pairs, ids=None, curves=None):
    """pairs: (Time text, Value text); None omits the attribute. curves: {index: {name: text}}."""
    out = []
    for i, (t, v) in enumerate(pairs):
        attrs = [("Id", str(ids[i] if ids else i))]
        attrs += [] if t is None else [("Time", t)]
        attrs += [] if v is None else [("Value", v)]
        attrs += list((curves or {}).get(i, {}).items())
        out.append(f"<{cls} " + " ".join(f'{k}="{x}"' for k, x in attrs) + " />")
    return out


def envelope(tag, eid, target, evs):
    lines = [f'<{tag} Id="{eid}">', "\t<EnvelopeTarget>", f'\t\t<PointeeId Value="{TID[target]}" />',
             "\t</EnvelopeTarget>", "\t<Automation>"]
    lines += ["\t\t<Events>", *("\t\t\t" + e for e in evs), "\t\t</Events>"] if evs else ["\t\t<Events />"]
    lines += ["\t\t<AutomationTransformViewState>", '\t\t\t<IsTransformPending Value="false" />',
              "\t\t\t<TimeAndValueTransforms />", "\t\t</AutomationTransformViewState>", "\t</Automation>"]
    if tag == "ClipEnvelope":
        lines += ["\t<LoopSlot>", "\t\t<Value />", "\t</LoopSlot>", "\t<ScrollerTimePreserver>",
                  '\t\t<LeftTime Value="0" />', '\t\t<RightTime Value="0" />', "\t</ScrollerTimePreserver>"]
    return lines + [f"</{tag}>"]


def track_env(target, evs, eid=0):
    return envelope("AutomationEnvelope", eid, target, evs)


def clip_env(evs):
    return envelope("ClipEnvelope", 0, "ControllerTargets.6", evs)


def _list(lines, depth):
    t = "\t" * depth
    if not lines:
        return [t + "<Envelopes />"]
    return [t + "<Envelopes>", *(t + "\t" + x for x in lines), t + "</Envelopes>"]


def doc(track=(), clip=()):
    """The template: one audio track (envelope list, mixer Speaker, Pan, CrossFadeState) and one MIDI
    track with a session MIDI clip (clip envelope list) and the MIDI controller target 6."""
    track = [x for e in track for x in e]
    clip = [x for e in clip for x in e]
    def target(name, before):
        return [f"<{name}>", *before, f'\t<AutomationTarget Id="{TID[name]}">', '\t\t<LockEnvelope Value="0" />',
                "\t</AutomationTarget>", f"</{name}>"]
    mixer = (target("Speaker", ['\t<Manual Value="true" />'])
             + target("Pan", ['\t<Manual Value="0" />', "\t<MidiControllerRange>", '\t\t<Min Value="-1" />',
                              '\t\t<Max Value="1" />', "\t</MidiControllerRange>"])
             + target("CrossFadeState", ['\t<Manual Value="1" />']))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Ableton MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1">',
        "\t<LiveSet>",
        '\t\t<NextPointeeId Value="40" />',
        "\t\t<Tracks>",
        '\t\t\t<AudioTrack Id="1">',
        "\t\t\t\t<AutomationEnvelopes>", *_list(track, 5), "\t\t\t\t</AutomationEnvelopes>",
        "\t\t\t\t<DeviceChain>", "\t\t\t\t\t<Mixer>", *("\t\t\t\t\t\t" + x for x in mixer), "\t\t\t\t\t</Mixer>",
        "\t\t\t\t</DeviceChain>",
        "\t\t\t</AudioTrack>",
        '\t\t\t<MidiTrack Id="2">',
        "\t\t\t\t<DeviceChain>", "\t\t\t\t\t<MainSequencer>", "\t\t\t\t\t\t<ClipSlotList>",
        '\t\t\t\t\t\t\t<ClipSlot Id="0">', "\t\t\t\t\t\t\t\t<ClipSlot>", "\t\t\t\t\t\t\t\t\t<Value>",
        '\t\t\t\t\t\t\t\t\t\t<MidiClip Id="0" Time="0">',
        "\t\t\t\t\t\t\t\t\t\t\t<Envelopes>", *_list(clip, 12), "\t\t\t\t\t\t\t\t\t\t\t</Envelopes>",
        "\t\t\t\t\t\t\t\t\t\t</MidiClip>", "\t\t\t\t\t\t\t\t\t</Value>", "\t\t\t\t\t\t\t\t</ClipSlot>",
        "\t\t\t\t\t\t\t</ClipSlot>", "\t\t\t\t\t\t</ClipSlotList>",
        "\t\t\t\t\t\t<MidiControllers>", f'\t\t\t\t\t\t\t<ControllerTargets.6 Id="{TID["ControllerTargets.6"]}">',
        '\t\t\t\t\t\t\t\t<LockEnvelope Value="0" />', "\t\t\t\t\t\t\t</ControllerTargets.6>",
        "\t\t\t\t\t\t</MidiControllers>",
        "\t\t\t\t\t</MainSequencer>", "\t\t\t\t</DeviceChain>",
        "\t\t\t</MidiTrack>",
        "\t\t</Tracks>",
        "\t</LiveSet>",
        "</Ableton>",
    ]
    return ("\n".join(lines) + "\n").encode("ascii")


E1 = [(L, "0"), ("4", "0"), ("8", "1")]
E8 = [(L, "1"), ("4", "1"), ("4", "-1"), ("8", "-1")]
E9P = [(L, "-1"), ("0", "-1"), ("4", "1")]
C9 = {1: {"CurveControl1X": "0.5", "CurveControl1Y": "0", "CurveControl2X": "0.5", "CurveControl2Y": "0"}}
C11 = {1: {"CurveControl1X": "0.8", "CurveControl1Y": "0", "CurveControl2X": "0.2", "CurveControl2Y": "1"}}
E14 = [(L, "true"), ("4", "false"), ("8", "true")]
E15 = [(L, "1"), ("4", "0"), ("8", "2")]
# Review: release case 021 keeps the leading value equal to the next value, so its saved text does not depend
# on whether a save keeps a differing leading value; envelopes are listed against target order (REQ-002).
E14S = [(L, "false"), ("4", "false"), ("8", "true")]
E15S = [(L, "0"), ("4", "0"), ("8", "2")]


def saved(target, cls, rows):
    """rows: dict of attribute text per event (Id excluded)."""
    return {"target": target, "events": [{"element": cls, "attributes": r} for r in rows]}


def tv(t, v):
    return {"Time": t, "Value": v}


def vals(target, pairs):
    return [{"target": target, "time": t, "value": v} for t, v in pairs]


# (number, purpose, requirement suffixes, fixture bytes, action, expected)
CASES = [
    (1, "Pan envelope with three events at the lower bound, 4 and 8; open, then save", ["001", "002", "003", "012"],
     doc([track_env("Pan", events(F, E1))]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [saved("Pan", F, [tv(L, "0"), tv("4", "0"), tv("8", "1")])]}}),
    (2, "Pan envelope with a single event at the lower bound", ["005", "007"],
     doc([track_env("Pan", events(F, [(L, "0.5")]))]), "open", {"outcome": OPENS}),
    (3, "Pan envelope whose only event is at 4", ["007"],
     doc([track_env("Pan", events(F, [("4", "0")]))]), "open", {"outcome": REFUSED}),
    (4, "Pan envelope with an empty event list", ["007"],
     doc([track_env("Pan", [])]), "open", {"outcome": REFUSED}),
    (5, "Pan envelope whose first event is at 0", ["007"],
     doc([track_env("Pan", events(F, [("0", "0"), ("4", "1")]))]), "open", {"outcome": OPENS}),
    (6, 'Pan envelope whose first event Time is written "-0"', ["007", "012"],
     doc([track_env("Pan", events(F, [("-0", "0"), ("4", "1")]))]), "open", {"outcome": OPENS}),
    (7, 'Pan envelope whose first event Time is written "-6.3072e7", the lower bound in exponent form', ["007", "012"],
     doc([track_env("Pan", events(F, [("-6.3072e7", "0"), ("4", "1")]))]), "open", {"outcome": OPENS}),
    (8, "Pan envelope whose first event is at -63071999, one beat after the lower bound", ["007"],
     doc([track_env("Pan", events(F, [("-63071999", "0"), ("4", "1")]))]), "open", {"outcome": REFUSED}),
    (9, "Pan envelope with a later event at the negative time -10", ["006", "007"],
     doc([track_env("Pan", events(F, [(L, "0"), ("-10", "0.5"), ("4", "1")]))]), "open", {"outcome": OPENS}),
    (10, "Clip envelope on MIDI controller target 6 with events at the lower bound and 0", ["001", "002", "007"],
     doc(clip=[clip_env(events(F, [(L, "127"), ("0", "127")]))]), "open", {"outcome": OPENS}),
    (11, "Clip envelope whose only event is at 4", ["007"],
     doc(clip=[clip_env(events(F, [("4", "127")]))]), "open", {"outcome": REFUSED}),
    (12, "Clip envelope with an empty event list", ["007"],
     doc(clip=[clip_env([])]), "open", {"outcome": REFUSED}),
    (13, 'FloatEvent Value "abc"', ["012"],
     doc([track_env("Pan", events(F, [(L, "0"), ("4", "abc")]))]), "open", {"outcome": REFUSED}),
    (14, 'BoolEvent Value "TRUE" on a Speaker envelope', ["003", "012"],
     doc([track_env("Speaker", events(B, [(L, "true"), ("4", "TRUE")]))]), "open", {"outcome": REFUSED}),
    (15, 'EnumEvent Value "2.0" on a CrossFadeState envelope', ["003", "012"],
     doc([track_env("CrossFadeState", events(N, [(L, "1"), ("4", "2.0")]))]), "open", {"outcome": REFUSED}),
    (16, "Pan events with Value 0.3 and a second Time of 0.3; open, then save", ["012"],
     doc([track_env("Pan", events(F, [(L, "0.3"), ("0.3", "0.3")]))]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [saved("Pan", F, [tv(L, "0.3000000119"),
                                                              tv("0.299999999999999989", "0.3000000119")])]}}),
    (17, "Curve controls 0.5, 0, 0.5, 0 on the event at 0; open, then save", ["008", "009"],
     doc([track_env("Pan", events(F, E9P, curves=C9))]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [saved("Pan", F, [
         tv(L, "-1"), {"Time": "0", "Value": "-1", "CurveControl1Y": "0", "CurveControl2Y": "0"}, tv("4", "1")])]}}),
    (18, "Curve controls 0.8, 0, 0.2, 1 on the event at 0; open, then save", ["008", "009", "012"],
     doc([track_env("Pan", events(F, E9P, curves=C11))]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [saved("Pan", F, [
         tv(L, "-1"), {"Time": "0", "Value": "-1", "CurveControl1X": "0.800000000000000044", "CurveControl1Y": "0",
                       "CurveControl2X": "0.200000000000000011", "CurveControl2Y": "1"}, tv("4", "1")])]}}),
    (19, "Only CurveControl1Y 0 and CurveControl2Y 0 present on the event at 0; open, then save", ["008", "009"],
     doc([track_env("Pan", events(F, E9P, curves={1: {"CurveControl1Y": "0", "CurveControl2Y": "0"}}))]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [saved("Pan", F, [
         tv(L, "-1"), {"Time": "0", "Value": "-1", "CurveControl1Y": "0", "CurveControl2Y": "0"}, tv("4", "1")])]}}),
    (20, "All four curve controls 0.5 on the event at 0; open, then save", ["008", "009"],
     doc([track_env("Pan", events(F, E9P, curves={1: {k: "0.5" for k in CC}}))]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [saved("Pan", F, [tv(L, "-1"), tv("0", "-1"), tv("4", "1")])]}}),
    (21, "CrossFadeState envelope listed before the Speaker envelope; open, then save", ["002", "003", "012"],
     doc([track_env("CrossFadeState", events(N, E15S), 0), track_env("Speaker", events(B, E14S), 1)]), "open-save",
     {"outcome": OPENS, "saved": {"envelopes": [
         saved("CrossFadeState", N, [tv(L, "0"), tv("4", "0"), tv("8", "2")]),
         saved("Speaker", B, [tv(L, "false"), tv("4", "false"), tv("8", "true")])]}}),
]

COMPARATOR = {
    "open": "outcome exact",
    "open-save": "outcome exact; per listed target: one saved envelope naming it, events in order, attribute text exact, Id not compared",
}

DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"FUN_", r"\bA(?:Float|Bool|Enum)Event\b",
        r"\bA(?:List)?Automation\w*", r"AClipEnvelope", r"APtr", r"mpObject", r"\bT(?:Float|Discrete)\w*Interpolator",
        r"Timeable\w*", r"SNewCompound", r"mCurve", r"mValue", r"mTime", r"\bslot\s*\+", r"vtable", r"registr",
        r"constructor", r"\bloader\b", r"post-load", r"converter", r"bisection", r"Ghidra", r"decompil", r"pseudocode",
        r"disassembl", r"dossier", r"corpus", r"Invalid Pointee", r"has no events", r"invalid time", r"DocumentCorrupt",
        r"not at 0\.0", r"strtod", r"printf", r"[Ee]xpat", r"Python", r"PRB-", r"\bQ-0\d", r"\bAEN-", r"\bE\d{1,2}\b",
        r"\bA[12]\b", r"\bI[1-6]\b", r"\bS[1-9]\b", r"\bN[12]\b", r"derivation", r"traceab", r"Recording Audio",
        r"Quick Start", r"Chuck Sutton", r"Patience", r"Core Library", r"\bB[012]\b", r"12\.4d1", r"12\.1d1",
        r"Live\.arm64", r"/home/", r"/var/", r"/tmp/", r"\bev_[0-9a-f]", r"build_aen", r"\+0x"]
ALLOWED_HITS = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cid(n):
    return f"AUTOMATION-ENVELOPES-{n:03d}"


def req(suffixes):
    return [f"REQ-AUTOMATION-ENVELOPES-{s}" for s in suffixes]


SCOPES = {
    "REQ-AUTOMATION-ENVELOPES-001": "Track envelopes in a track's AutomationEnvelopes/Envelopes, clip envelopes in a clip's Envelopes/Envelopes; AutomationEnvelope and ClipEnvelope shape with EnvelopeTarget/PointeeId and Automation/Events; empty transform state",
    "REQ-AUTOMATION-ENVELOPES-002": "PointeeId names the Id of the target element; binding by Id, not by list position (judged through the saved envelope of each target); fixture target relations only",
    "REQ-AUTOMATION-ENVELOPES-003": "FloatEvent, BoolEvent and EnumEvent by target kind; Id, Time (binary64) and Value (binary32, Boolean, integer) in the parameter's stored units",
    "REQ-AUTOMATION-ENVELOPES-005": "A list whose only event is at the lower bound is accepted",
    "REQ-AUTOMATION-ENVELOPES-006": "Document order with non-decreasing times; at most two events at one time; a later event may have a negative time",
    "REQ-AUTOMATION-ENVELOPES-007": "Empty event list refused; first event time other than the lower bound or 0 refused (binary64 comparison, -0 counts as 0); later times not checked; track and clip envelopes",
    "REQ-AUTOMATION-ENVELOPES-008": "Curve control attribute names; a missing control reads as 0.5; four 0.5 controls mean no curve; on save each control equal to 0.5 is omitted and the others written as binary64 text",
    "REQ-AUTOMATION-ENVELOPES-009": "Controls in [0, 1] whose pairs meet the stated monotonicity condition are kept on open",
    "REQ-AUTOMATION-ENVELOPES-012": "Event text on open (Time and controls as decimal binary64, Float Value then binary32, Bool tokens, integer rule; refusal of rejected text) and on save (17 and 9 significant-digit rule, true or false, decimal integers)",
}
EXCL_INPUTS = [
    "a PointeeId that names no element, or an element other than the release's target relations, including another track's parameter; two envelopes naming one target; repeated target Ids; target Ids not below NextPointeeId; LockEnvelope other than 0",
    "events in time disorder; three or more events at one time; repeated or missing event Ids; an event without Time or Value; an event element that does not match its target's value kind",
    "stored transforms: a pending transform or a non-empty TimeAndValueTransforms",
    "values outside the ranges of REQ-AUTOMATION-ENVELOPES-003; event times below L, at or above 1,000,000, or not finite",
    "curve controls outside [0, 1] or not satisfying K, and controls on the first or last event, on an event followed by one at the same time, or on an event whose next event has the same value",
    "Time, curve control or FloatEvent Value text that, after leading spaces and an optional sign, starts with 0x or 0X, or with inf or nan in any letter case; the text Invalid; text starting with #; leading whitespace other than U+0020",
    "EnumEvent Value text with spaces both before and after the digits, with + and trailing spaces, or with a - sign, and such text longer than 63 characters that ends in a space",
    "the main track's tempo and time-signature envelopes; envelopes of other tracks, devices, modulation targets and other MIDI controller targets; audio clip envelopes",
    "elements outside AutomationEnvelope and ClipEnvelope that use the same Events shape, such as the timelines of arrangement clips",
    "any other format version, root attribute or compressed container",
    "documents that break more than one rule of this release",
]
EXCL_BEHAVIOR = [
    "the value an envelope supplies to its parameter at any time, for Float, Bool and Enum envelopes, track and clip envelopes alike (REQ-AUTOMATION-ENVELOPES-010 and 011), including at event times, after the last event and between equal values, and whether event Ids affect it (REQ-AUTOMATION-ENVELOPES-004)",
    "whether opening replaces controls that do not satisfy K by 0.5",
    "whether a save keeps or renumbers event and target Ids, the saved transform state, saved negative zero, whether a save writes envelopes that hold a single event, and whether a save keeps a leading event whose value differs from the next event's value",
    "editing, override, recording and undo (REQ-AUTOMATION-ENVELOPES-013)",
    "texts, dialogs and logging of a refusal, and the state after it",
    "audio rendering, smoothing, scheduling and timing",
]


REVIEW = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVE-01 high: every value case (022 to 029) rested on an untraced per-target conversion; withdrawn; REQ-010, 011 and 004 unreleased; REQ-005 and 006 narrowed",
        "RVE-02 low: case 021 saved a leading value that differs from the next value; fixture aligned so the expectation does not depend on that untraced save rule; envelopes listed against target order",
        "RVE-03 info: saved PointeeId judged only against the saved target Id; no case assumes a save keeps Ids",
        "RVE-04 info: no shipped set and no dangling, unsorted, Id-less, Time-less, Value-less or duplicate-Id input; checked per fixture",
        "RVE-05 info: stated assumptions (open reaches the envelope checks, Bool and Enum text rules, save keeps the binding) accepted",
        "RVE-06 info: evidence identity re-checked; all hashes matched",
        "RVE-07 editorial: payload status set to reviewed release; review record added; inventory re-hashed",
    ],
    "disposition": "Approved with listed narrowing (RVE-01, RVE-02), only for the explicit partial clauses; expectations static-derived; reference and candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}


def manifest_meta():
    return {
        "schema": "handoff-manifest-v1", "release_id": "automation-envelopes-v1", "release_status": "released",
        "release_date": "2026-10-18", "target": TARGET,
        "specification": {"id": "SPEC-AUTOMATION-ENVELOPES", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-AUTOMATION", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": SCOPES,
        "unreleased_requirements": ["REQ-AUTOMATION-ENVELOPES-004", "REQ-AUTOMATION-ENVELOPES-010",
                                    "REQ-AUTOMATION-ENVELOPES-011", "REQ-AUTOMATION-ENVELOPES-013"],
        "compatibility_dimensions": {
            "envelope-storage-and-load-checks": "static-derived expectations; reference execution not-run",
            "file-format-written": "saved event text only, static-derived; reference execution not-run",
            "envelope-value-at-time": "excluded (REQ-AUTOMATION-ENVELOPES-010 and 011 unreleased)",
            "editing-and-ui": "excluded (REQ-AUTOMATION-ENVELOPES-013)",
            "audio": "excluded", "timing": "excluded",
        },
        "exclusions": {"inputs_without_expectation": EXCL_INPUTS, "behavior": EXCL_BEHAVIOR},
        "fixture_origin": "independently authored minimal Live Set XML documents from one template; no shipped file content, schema content or program code",
        "approved_public_sources": [],
        "review": REVIEW,
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    cases = []
    for n, purpose, reqs, data, action, expected in CASES:
        rel = f"fixtures/{cid(n)}.xml"
        (STAGE / rel).write_bytes(data)
        cases.append({"id": cid(n), "purpose": purpose, "requirements": req(reqs), "input": rel, "action": action,
                      "expected": expected,
                      "expectation_provenance": PROV_V if action == "open-evaluate" else PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run",
                      "comparator": COMPARATOR[action]})
    doc_ = {"schema": "automation-envelopes-cases-v1", "target": TARGET,
            "scope": "automation-envelopes-v1 partial requirement clauses only (see spec.md)",
            "status": "released-reviewed",
            "fixture_origin": "Independently authored minimal documents; no shipped file copied",
            "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
            "representation": {
                "action": "open or open-save",
                "outcome": "opens or refused",
                "saved": "open-save only: per listed target, the saved envelope's events in order with exact attribute text other than Id",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1, ensure_ascii=True) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- checks ----
def payload(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md_path, root):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md_path.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md_path.parent / path).resolve() if path else md_path.resolve()
        ok = dest.is_file() and root.resolve() in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((target, "ok" if ok else "UNRESOLVED"))
    return out


def verify(d):
    d = Path(d)
    man = json.loads((d / "manifest.json").read_text())
    files = payload(d)
    mismatches = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
                  or sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inventory = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    link_rows = {str(p.relative_to(d)): links(p, d) for p in d.glob("*.md")}
    bad_links = {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    missing_inputs = [c["input"] for c in cases if not (d / c["input"]).is_file()]
    deny = {}
    for p in [*files, d / "manifest.json"]:
        text = p.read_text()
        hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "manifest_case_count": man["case_count"],
            "hash_or_size_mismatches": mismatches, "inventory_differences": inventory,
            "symlinks": [str(p) for p in d.rglob("*") if p.is_symlink()],
            "markdown_links": {k: len(v) for k, v in link_rows.items()}, "unresolved_links": bad_links,
            "missing_case_inputs": missing_inputs, "deny_list_hits": deny}


def evidence_identity():
    man = json.loads((S6 / "manifest.json").read_text())
    bad = [p for p, f in man["files"].items() if sha((S6 / p).read_bytes()) != f["sha256"]]
    return {"s6_manifest_files": len(man["files"]), "s6_mismatches": bad,
            "image_sha256_matches": sha(IMAGE.read_bytes()) == IMAGE_SHA == man["binary"]["sha256"]}


def probes():
    """Excluded inputs must give no expectation in the model (or the stated refusal)."""
    pan = lambda pairs, **kw: doc([track_env("Pan", events(F, pairs, **kw))])
    rows = [
        ("dangling PointeeId", doc([envelope("AutomationEnvelope", 0, "Pan", events(F, E1))]).replace(b'PointeeId Value="22"', b'PointeeId Value="39"'), "open", None),
        ("events in time disorder", pan([(L, "0"), ("8", "-0.5"), ("4", "0.5")]), "open", None),
        ("duplicate event Ids", pan([(L, "0"), ("4", "0.5")], ids=[0, 0]), "open", None),
        ("event without Time", pan([(L, "0"), (None, "0.5")]), "open", None),
        ("event without Value", pan([(L, "0"), ("4", None)]), "open", None),
        ("three events at one time", pan([(L, "0"), ("4", "0"), ("4", "1"), ("4", "0")]), "open", None),
        ("value out of range", pan([(L, "0"), ("4", "2")]), "open", None),
        ("hexadecimal time", pan([(L, "0"), ("0x4", "1")]), "open", None),
        ("integer with a minus sign", doc([track_env("CrossFadeState", events(N, [(L, "1"), ("4", "-1")]))]), "open", None),
        ("controls not satisfying K", pan(E9P, curves={1: {"CurveControl1X": "0.2", "CurveControl1Y": "1.5", "CurveControl2X": "0.8", "CurveControl2Y": "-0.5"}}), "open", None),
        ("interior linear value", pan(E1), "open-evaluate", {"outcome": OPENS, "values": vals("Pan", [(6, 0.5)])}),
        ("value at a step", pan(E8), "open-evaluate", {"outcome": OPENS, "values": vals("Pan", [(4, 1)])}),
        ("Bool value at an event time", doc([track_env("Speaker", events(B, E14))]), "open-evaluate", {"outcome": OPENS, "values": vals("Speaker", [(4, False)])}),
        ("time before a first event at 0", pan([("0", "0"), ("4", "1")]), "open-evaluate", {"outcome": OPENS, "values": vals("Pan", [(-1, 0)])}),
        ("interior curved value", pan(E9P, curves=C9), "open-evaluate", {"outcome": OPENS, "values": vals("Pan", [(2, -0.75)])}),
    ]
    out = {}
    for name, data, action, exp in rows:
        try:
            out[name] = model(data, action, exp or {"outcome": OPENS})["outcome"] + " (expectation produced)"
        except NoExpectation as e:
            out[name] = f"no expectation: {e}"
    return out


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    problems, fixtures, mutants = {}, {}, 0
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        errs = []
        got = None
        try:
            got = model(raw, c["action"], c["expected"])
        except NoExpectation as e:
            errs.append(f"model: no expectation ({e})")
        if got is not None and not same(got, c["expected"]):
            errs.append(f"model {got} != expected")
        try:
            if got is not None and same(model(raw, c["action"], mutate(c["expected"])), mutate(c["expected"])):
                errs.append("mutated expectation not detected")
            else:
                mutants += 1
        except NoExpectation:
            mutants += 1
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n"):
            errs.append("not ASCII with LF endings")
        if errs:
            problems[c["id"]] = errs
        fixtures[c["id"]] = {"bytes": len(raw), "lines": raw.count(b"\n"), "sha256": sha(raw)}
    by_hash = {}
    for k, v in fixtures.items():
        by_hash.setdefault(v["sha256"], []).append(k)
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "automation-envelopes-v1 (reviewed staging copy)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "mutated_expectations_detected": f"{mutants}/{len(cases)}",
              "identical_fixture_inputs": [v for v in by_hash.values() if len(v) > 1],
              "excluded_input_probes": probes(), "fixtures": fixtures, "evidence_identity": evidence_identity(),
              **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model restates the "
                        "same static evidence and is not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    trace = {"schema": "automation-envelopes-traceability-v1", "spec": "SPEC-AUTOMATION-ENVELOPES r1",
             "evidence": EV, "inferred_links": INF, "spec_cases_not_released": NOT_RELEASED,
             "cases": {cid(n): {"source": src, "requirements": req(next(c[2] for c in CASES if c[0] == n)),
                                "evidence": ev, "inferred": inf} for n, (src, ev, inf) in TRACE.items()}}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "mutated_expectations_detected", "excluded_input_probes",
                                             "identical_fixture_inputs", "evidence_identity", "payload_files",
                                             "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
                                             "missing_case_inputs", "deny_list_hits", "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
