"""Stage the midi-config-v3 release candidate (analyst side; not reviewed, not released).

Run with CPython 3.11 and -I (the S4 host interpreter 3.11.13 was used):
  python3.11 -I build_v3.py build          # fixtures/, cases.json, manifest.json (files[] empty) in ../midi-config-v3/
  python3.11 -I build_v3.py seal           # manifest files[], author-validation.json, traceability.json, spec diff
  python3.11 -I build_v3.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Inputs (read only): the released midi-config-v2 package, carried unchanged (109 case records and fixture
bytes); the SPEC-MIDI-USER-MAPPING r3 MT table; the N7 packet (acceptance-cases.json, native-constants.json,
scripts/derive_cases.py) and the v2 interpretation cross-check model. New value-case expectations are computed
by model_values(), an exact-rational restatement of the released value clauses in spec.md. The seal step
compares them with the spec table, the N7 float32 model (under every takeover choice for `any` cases) and the
N7 case file, re-checks the decode tables over all 128 data values, and checks fixtures, hashes, links and a
sanitization deny-list. None of these is an oracle: all share the same static evidence.
README.md, AGENTS.md and spec.md in the stage directory are hand-written.
"""
import configparser, difflib, hashlib, importlib.util, io, json, re, sys
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True  # imported analyst modules live in other directories; write nothing there
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "midi-config-v3"
V2 = ROOT / "handoff/midi-config-v2"
V2A = HERE.parent / "midi-config-v2-analysis"
N7 = ROOT / "analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1"
SPEC = ROOT / "wiki/specs/midi-user-mapping.md"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS"
V2_MANIFEST_SHA = "889b52fa3b7f19c1bd085f26db39e0f62f00cbf7dc85be050e32207f012eb4d7"
PROV = "static-derived; not observed reference output"
COMPARATOR = ("exact assignment set over all fields; order immaterial; device_parameter_banks exact; "
              "values: parameter value after each message, in order, within 1e-6 absolute")
TOL = 1e-6

# ---- value cases: (number, spec case, purpose, control, map mode, takeover, parameter, messages) ----
CONT = {"kind": "continuous", "stepped": False, "min": 0, "max": 1, "initial_value": 0.5}
STEP = {"kind": "continuous", "stepped": True, "min": 0, "max": 3, "initial_value": 1}
NUM = 20  # every value case assigns controller number 20 on channel 0; 14-bit LSB is 52


def on(*data):
    return [(NUM, v) for v in data]


VALUE = [
    (110, "MT-01", "Absolute under takeover none: data values 0, 64 and 127 set v/127 of the range",
     "Encoder1", "Absolute", "none", CONT, on(0x00, 0x40, 0x7F)),
    (111, "MT-02", "Absolute14Bit under takeover none: MSB then LSB completes one pair",
     "Encoder1", "Absolute14Bit", "none", CONT, [(NUM, 0x64), (NUM + 32, 0x32)]),
    (112, "MT-03", "Absolute14Bit under takeover none: LSB then MSB completes one pair",
     "Encoder1", "Absolute14Bit", "none", CONT, [(NUM + 32, 0x32), (NUM, 0x64)]),
    (113, "MT-04", "Absolute14Bit under takeover none: a newer MSB replaces the held one; a lone LSB after the pair changes nothing",
     "Encoder1", "Absolute14Bit", "none", CONT, [(NUM, 0x10), (NUM, 0x64), (NUM + 32, 0x32), (NUM + 32, 0x00)]),
    (114, "MT-05", "Absolute14Bit under takeover none: full scale, then zero",
     "Encoder1", "Absolute14Bit", "none", CONT, [(NUM, 0x7F), (NUM + 32, 0x7F), (NUM, 0x00), (NUM + 32, 0x00)]),
    (115, "MT-06", "LinearSignedBit: signed steps of (max - min)/256 per message",
     "Encoder1", "LinearSignedBit", "any", CONT, on(0x01, 0x41, 0x40, 0x7F)),
    (116, "MT-07", "LinearSignedBit2: signed steps of (max - min)/256 per message",
     "Encoder1", "LinearSignedBit2", "any", CONT, on(0x01, 0x41, 0x40)),
    (117, "MT-08", "LinearTwoCompliment: signed steps of (max - min)/256 per message",
     "Encoder1", "LinearTwoCompliment", "any", CONT, on(0x01, 0x7F, 0x41, 0x40)),
    (118, "MT-09", "LinearBinaryOffset: signed steps; data value 64 decodes to 0",
     "Encoder1", "LinearBinaryOffset", "any", CONT, on(0x41, 0x3F, 0x40, 0x00)),
    (119, "MT-10", "AccelSignedBit: accelerated steps; magnitude 10 gives 20 and data value 0 gives +20",
     "Encoder1", "AccelSignedBit", "any", CONT, on(0x01, 0x07, 0x09, 0x0A, 0x41, 0x49, 0x00)),
    (120, "MT-11", "AccelSignedBit2: accelerated steps; data value 0 gives -50",
     "Encoder1", "AccelSignedBit2", "any", CONT, on(0x01, 0x41, 0x07, 0x47, 0x00)),
    (121, "MT-12", "AccelTwoCompliment: accelerated steps; data values 65 and 0 count up by 50",
     "Encoder1", "AccelTwoCompliment", "any", CONT, on(0x01, 0x7F, 0x08, 0x41, 0x42, 0x00)),
    (122, "MT-13", "AccelBinaryOffset: accelerated steps; data value 64 gives +50",
     "Encoder1", "AccelBinaryOffset", "any", CONT, on(0x41, 0x3F, 0x46, 0x39, 0x40)),
    (123, "MT-14", "LinearBinaryOffset: relative steps are clamped at max and at min",
     "Encoder1", "LinearBinaryOffset", "any", CONT, on(0x7F, 0x7F, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00)),
    (124, "MT-15", "Stepped parameter, Absolute under takeover none: nearest integer of the scaled value",
     "Encoder1", "Absolute", "none", STEP, on(0x15, 0x16, 0x3F, 0x40, 0x7F)),
    (125, "MT-16", "Stepped parameter, LinearSignedBit: one unit per message by the sign of the step, clamped at min",
     "Encoder1", "LinearSignedBit", "any", STEP, on(0x05, 0x01, 0x41, 0x46, 0x46, 0x46)),
    (126, "MT-22", "Crossfader Absolute values apply directly under every takeover choice",
     "CrossfaderSlider", "Absolute", "any", CONT, on(0x0A, 0x64)),
    (127, "MT-23", "A relative value applies directly on the first message under every takeover choice",
     "Encoder1", "LinearSignedBit", "any", CONT, on(0x01)),
]
EXCLUDED_SPEC_CASES = {  # spec r3 S-cond rows: condition unresolved (no probe run), no expectation released
    "MT-17": "S-cond: on/off parameter thresholds (PRB-N7-04)",
    "MT-18": "S-cond: on/off parameter, relative (PRB-N7-04)",
    "MT-19": "S-cond: Pick-Up arithmetic and label (PRB-N7-03)",
    "MT-20": "S-cond: Value Scaling arithmetic and label (PRB-N7-03)",
    "MT-21": "S-cond: Pick-Up first message without a previous value (PRB-N7-03)",
}
# ---- analyst traceability (never shipped); locators are in the N7 packet unless stated ----
EV = "analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/"
EVIDENCE = {
    "v2": "handoff/midi-config-v2/ (manifest sha256 " + V2_MANIFEST_SHA + ", REVIEW.md); per-case sources in "
          "analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2-analysis/traceability.json",
    "E10": EV + "results/n7-0004 0x103b4d744 (wrapper forwards channel, CC, mode, avoid, sensitivity unchanged); "
           "results/n7-0001 0x102593258 (validation 0x1025931ac; mode 5 -> 0x1026094e0 called at 0x10259338c with x0-x4 "
           "only; other modes: CC receiver, init 0x101b7f32c stores avoid at +0x44); results/n7-0004 0x101b69248 -> "
           "results/n7-0002 0x101b65b68 (per-input prior table, -129 fill) -> results/n7-0004 0x101b7842c (every handler "
           "on the (channel, CC) list). S4 listings: _Framework/ControlSurface _install_mapping L735-743; "
           "InputControlElement L191, L197; _Generic/GenericScript L216 (crossfader set_needs_takeover(False))",
    "E11": EV + "results/n7-0002 0x1026094e0 (keys (ch, n, 5) -> type 5 and (ch, n+32, 5) -> type 6; receiver flag "
           "`mov w3,#0x0` at 0x102609548), 0x101b8028c MSB store, 0x101b802bc LSB store, 0x101b7fcc0 combine "
           "((MSB<<7|LSB)/129.0, constant 0x10584a8b4; MapMode 0, sensitivity 1.0; all four slots reset)",
    "E12": EV + "results/n7-0002 0x101b76bf0 value function (absolute t = v/127, divisor 127.0; relative (hi-lo)/256*d*s or "
           "+-1 when quantized; clamp; frinta at 0x101b76cd4; step negated and t = (127-v)/127 when Max < Min); "
           "results/n7-0001 0x101b7b96c decoder; results/n7-0003 0x101b842cc table init; out/native-constants.json",
    "E13": EV + "results/n7-0003 0x1026fa5c8, 0x1026fa684 (Type 1 ATimeableFloat, 2 Bool, 3 Enum, 0 other; Min/Max; "
           "Quantized); results/n7-0001 0x101b7fde4 apply (Type 2 branch; otherwise value function, then takeover only "
           "for MapMode 0/5, Type 1 and prior != FLT_MAX); results/n7-0002 0x101b7f894 CC receiver (prior := FLT_MAX "
           "when avoid and Zoom 1.0; quantized relative accumulator +-s, fires at |acc| >= 1)",
    "E14": EV + "results/n7-0001 0x101b7c508 takeover (mode 0 returns clamp(new)), 0x101b7c344 Pick-Up; results/n7-0003 "
           "0x101b83750 preference setter; out/corpus-excerpts.jsonl 0x1022df424 UI entry order (decompiler only)",
}
INFERRED = {
    "I1": "Takeover index 0 is the preference choice labelled None: UI entries are declared in the order no takeover, "
          "pick-up, value scaling (0x1022df424, decompiler only) and index 1 posts the pick-up notification. Stated in "
          "the contract as an assumption with a comparison obligation.",
    "I2": "The handler registry 0x101b84798/0x10260535c is the MidiMap handler lookup, and dispatch entry +0x30 holds "
          "the installed map mode (spec r3 E10 inference).",
    "I3": "The parameter setter 0x101b0d328 (untraced) stores the value without further processing. The contract makes "
          "this a precondition and excludes parameters that change a value after it is set.",
    "I4": "Messages are applied in arrival order, once each; the queued-command path taken when 0x1011c0ee8(0x100500) "
          "is nonzero has unknown timing. The contract applies messages one at a time and excludes back-to-back "
          "ordering, coalescing and deferral.",
    "I5": "Layer wiring from control to component setter, assumed for every target association since spec revision 1.",
}
CLAUSES = {  # released or narrowed clause -> evidence labels and inferences
    "midi-config-v2 clauses of REQ-002, 003, 005 (labels), 006 to 013, carried unchanged": (["v2"], []),
    "value: continuous controls act on their channel and number; Absolute14Bit also on n + 32": (["E10", "E11"], ["I2", "I5"]),
    "value: each message applied once, no smoothing": (["E12", "E13"], ["I3", "I4"]),
    "value: target parameter min, max, current value, stepped, four kinds": (["E13"], []),
    "value: min below max precondition (reversed ranges excluded; finding F2)": (["E12"], []),
    "value: Absolute": (["E12", "E13"], []),
    "value: stepped rounding to nearest, halves away from zero": (["E12"], []),
    "value: Absolute14Bit pairing, replacement, lone half, 16383 scale": (["E11", "E12"], []),
    "value: relative decode table and A, B": (["E12"], []),
    "value: relative application, not stepped and stepped": (["E12", "E13"], []),
    "takeover: choice none applies every value": (["E14"], ["I1"]),
    "takeover: relative values exempt": (["E13"], []),
    "takeover: enumerated and other kinds exempt": (["E13"], []),
    "takeover: crossfader Absolute values exempt (REQ-010)": (["E10", "E13"], []),
    "exclusion: crossfader Absolute14Bit under choices other than none (finding F1)": (["E10", "E11"], []),
    "exclusion: on/off parameters (spec S-cond, PRB-N7-04)": (["E13"], []),
    "exclusion: Pick-Up, Value Scaling, their labels and the default (spec S-cond, PRB-N7-03)": (["E14"], []),
    "exclusion: timing, ordering, coalescing, deferral (PRB-N7-05)": (["E13"], ["I4"]),
    "exclusion: number n + 32 shared with another assignment; several assignments on one address": (["E10", "E11"], ["I2"]),
}
CASE_EVIDENCE = {"MT-01": "AN", "MT-02": "PN", "MT-03": "PN", "MT-04": "PN", "MT-05": "PN", "MT-15": "AN",
                 **{f"MT-{k:02d}": "R" for k in (6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 23)}, "MT-22": "X"}
CASE_EVIDENCE_KINDS = {
    "AN": (["E10", "E12", "E13", "E14"], ["I1", "I2", "I3", "I4"]),
    "PN": (["E10", "E11", "E12", "E13", "E14"], ["I1", "I2", "I3", "I4"]),
    "R": (["E10", "E12", "E13"], ["I2", "I3", "I4"]),
    "X": (["E10", "E12", "E13"], ["I2", "I3", "I4"]),
}
ASSIGN = {
    "Encoder1": {"section": "DeviceControls", "control": "Encoder1", "target": "device-parameter:1", "banks": 1},
    "CrossfaderSlider": {"section": "MixerControls", "control": "CrossfaderSlider", "target": "crossfader", "banks": None},
}

# ---- exact restatement of the released value clauses (spec.md "Value transforms") ----
A_TAB, B_TAB = [1, 2, 3, 4, 5, 8, 10, 20, 50], [1, 2, 3, 4, 5, 8, 20, 50]


def a(k):
    return A_TAB[k - 1] if 1 <= k <= 9 else 20


def b(k):
    return B_TAB[k - 1] if 1 <= k <= 8 else 50


DECODE = {
    "LinearSignedBit": lambda v: v if v <= 64 else -(v - 64),
    "LinearSignedBit2": lambda v: -v if v <= 64 else v - 64,
    "LinearTwoCompliment": lambda v: v if v <= 64 else v - 128,
    "LinearBinaryOffset": lambda v: v - 64,
    "AccelSignedBit": lambda v: a(v) if v <= 64 else -a(v - 64),
    "AccelSignedBit2": lambda v: -b(v) if v <= 64 else b(v - 64),
    "AccelTwoCompliment": lambda v: b(v) if v <= 65 else -b(128 - v),
    "AccelBinaryOffset": lambda v: b(v - 64) if v >= 64 else -b(64 - v),
}


class NoExpectation(Exception):
    pass


def nearest(x):  # halves away from zero
    n = int(abs(x) + Fraction(1, 2))
    return Fraction(n if x >= 0 else -n)


def model_values(control, mode, takeover, p, msgs, n=NUM):
    if p["kind"] == "on/off":
        raise NoExpectation("on/off parameter")
    lo, hi, cur = (Fraction(str(p[k])) for k in ("min", "max", "initial_value"))
    if not lo < hi or not lo <= cur <= hi:
        raise NoExpectation("range precondition")
    if p["stepped"] and any(x.denominator != 1 for x in (lo, hi, cur)):
        raise NoExpectation("stepped parameter with non-integer bound or value")
    if mode == "Absolute14Bit" and n > 95:
        mode = "Absolute"  # label rule
    exempt = (mode in DECODE or p["kind"] in ("enumerated", "other")
              or (control == "CrossfaderSlider" and mode == "Absolute"))
    if takeover != "none" and not exempt:
        raise NoExpectation("takeover choice other than none on a value subject to takeover")
    fit = (lambda x: nearest(x)) if p["stepped"] else (lambda x: x)
    held, out = {}, []
    for num, v in msgs:
        if mode == "Absolute14Bit" and num in (n, n + 32):
            held["msb" if num == n else "lsb"] = v
            if len(held) == 2:
                cur = fit(lo + (hi - lo) * Fraction(128 * held["msb"] + held["lsb"], 16383))
                held = {}
        elif num == n and mode == "Absolute":
            cur = fit(lo + (hi - lo) * Fraction(v, 127))
        elif num == n:
            d = DECODE[mode](v)
            step = (1 if d > 0 else -1) if p["stepped"] else (hi - lo) * Fraction(d, 256)
            cur = min(max(cur + step, lo), hi)
        out.append(cur)
    return out


def fixture(control, mode):
    dev = f"Encoder1: {NUM}\nEncoderMapMode: {mode}\n" if control == "Encoder1" else ""
    mix = f"CrossfaderSlider: {NUM}\nCrossfaderMapMode: {mode}\n" if control == "CrossfaderSlider" else ""
    return (f"[Globals]\nGlobalChannel: 0\n\n[DeviceControls]\n{dev}\n[MixerControls]\n{mix}\n"
            "[TransportControls]\n").encode("ascii")


def cid(n):
    return f"MIDI-CONFIG-{n:03d}"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(rel, data):
    p = STAGE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def value_case(n, mt, purpose, control, mode, takeover, p, msgs):
    meta = ASSIGN[control]
    vals = [round(float(x), 9) for x in model_values(control, mode, takeover, p, msgs)]
    assignment = {"section": meta["section"], "control": control, "target": meta["target"],
                  "message_type": "control-change", "number": NUM, "channel": 0, "map_mode": mode}
    return {
        "id": cid(n), "purpose": purpose, "origin": "new in midi-config-v3",
        "requirements": ["REQ-MIDI-USER-005"] + (["REQ-MIDI-USER-010"] if control == "CrossfaderSlider" else []),
        "input": f"fixtures/{cid(n)}/UserConfiguration.txt",
        "stimulus": {"takeover": takeover, "parameter": {"target": meta["target"], **p},
                     "messages": ["B0 %02X %02X" % m for m in msgs]},
        "expected": {"assignments": [assignment], "device_parameter_banks": meta["banks"], "values": vals},
        "expectation_provenance": PROV, "reference_execution": "not-run", "candidate_execution": "not-run",
        "comparator": COMPARATOR,
    }


def manifest_meta(case_count):
    v2 = json.loads((V2 / "manifest.json").read_text())
    ex = v2["exclusions"]
    behavior = [x for x in ex["behavior"] if x != "numeric transforms, 14-bit pairing, relative arithmetic, pickup and takeover"]
    assert len(behavior) == len(ex["behavior"]) - 1
    scopes = dict(v2["partial_requirement_scopes"])
    scopes["REQ-MIDI-USER-005"] = (scopes["REQ-MIDI-USER-005"] + "; value transforms of Absolute, Absolute14Bit and the "
                                   "eight relative modes for continuous, enumerated and other parameters; takeover "
                                   "choice none and the values exempt from takeover")
    scopes["REQ-MIDI-USER-010"] = (scopes["REQ-MIDI-USER-010"] + "; their values follow the REQ-MIDI-USER-005 transforms; "
                                   "crossfader Absolute values exempt from takeover")
    return {
        "schema": "handoff-manifest-v1", "release_id": "midi-config-v3", "release_status": "candidate-unreviewed",
        "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-MIDI-USER-MAPPING", "parent_revision": 3, "release_revision": 3},
        "feature_ids": ["FEAT-MIDI-USER-MAPPING"],
        "partial_requirement_scopes": scopes,
        "unreleased_requirements": v2["unreleased_requirements"],
        "compatibility_dimensions": {
            **v2["compatibility_dimensions"],
            "parameter-values": "static-derived values for continuous controls in value cases; reference execution not-run",
            "behavior": "runtime routing and effects not-run; effects other than the released value transforms excluded",
        },
        "exclusions": {
            "inputs_without_expectation": ex["inputs_without_expectation"] + [
                "on/off target parameters, in every map mode",
                "a target parameter reporting a minimum equal to or above its maximum; a stepped parameter with a non-integer minimum, maximum or current value; a current value outside the range; a parameter that changes a value after it is set",
                "under a takeover choice other than none: Absolute and Absolute14Bit values for a continuous parameter, except Absolute values of the crossfader (crossfader Absolute14Bit values included)",
                "an enabled assignment on number n + 32 and the channel of an Absolute14Bit control with number n",
                "other MIDI input during a value case, including running status",
            ],
            "behavior": behavior + [
                "Pick-Up and Value Scaling takeover, the labels of the takeover choices other than none, and the default choice",
                "values of on/off parameters",
                "when a value is applied; ordering, coalescing and deferral of messages sent back to back; latency",
                "displayed values and any change a parameter makes to a value after it is set",
                "which application parameter a target is, and its kind, range and stepping",
            ],
        },
        "stated_assumptions": [
            "The takeover choice called none, under which takeover never acts, is the choice labelled None in the preferences; inferred from the order of the choices, not observed. Cases MIDI-CONFIG-110 to 114 and 124 depend on it.",
        ],
        "fixture_origin": "independently authored ASCII configuration inputs, expected logical assignments, MIDI byte sequences, parameter descriptions and expected values",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": "midi-config-v2",
        "supersession": {
            "relationship": "strict superset on publication; midi-config-v2 stays immutable and valid for its narrower scope",
            "superseded_manifest_sha256": V2_MANIFEST_SHA,
            "restated_cases": "MIDI-CONFIG-001 to 109: case records and fixture bytes identical to midi-config-v2",
            "changes": [
                "REQ-MIDI-USER-005 gains value transforms: Absolute, Absolute14Bit pairing, the eight relative decode tables and step rules, stepped rounding, takeover choice none and the takeover exemptions",
                "REQ-MIDI-USER-010 gains master, cue and crossfader values and the crossfader Absolute takeover exemption",
                "the general value-transform exclusion of midi-config-v2 is narrowed to the listed value exclusions",
                "case representation gains stimulus (takeover, parameter, messages) and expected.values for value cases",
                "cases MIDI-CONFIG-110 to 127 added (18 value cases)",
                "no midi-config-v2 clause, case or fixture changed; nothing in midi-config-v2 is contradicted",
            ],
        },
        "entrypoint": "README.md", "case_count": case_count,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    v2 = json.loads((V2 / "cases.json").read_text())
    cases = []
    for c in v2["cases"]:
        write(c["input"], (V2 / c["input"]).read_bytes())
        cases.append(c)
    for row in VALUE:
        n, _, _, control, mode = row[:5]
        write(f"fixtures/{cid(n)}/UserConfiguration.txt", fixture(control, mode))
        cases.append(value_case(*row))
    rep = dict(v2["representation"])
    rep.update({
        "stimulus": "value cases only: takeover (none, or any = every takeover choice); parameter (target, kind, stepped, "
                    "min, max, initial_value); messages (three-byte Control Change messages in hexadecimal, applied in order)",
        "values": "value cases only: expected.values, the target parameter value after each message, exact results rounded "
                  "to nine decimals, compared within 1e-6 absolute",
    })
    doc = {"schema": "midi-config-cases-v3", "target": TARGET,
           "scope": "midi-config-v3 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
           "fixture_origin": "Independently authored minimal ASCII inputs and MIDI byte sequences; no shipped file copied",
           "oracle_status": v2["oracle_status"], "representation": rep, "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(len(cases)), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- checks ----
DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"\+0x", r"FUN_", r"\.pyc", r"bytecode", r"disassembl",
        r"decompil", r"pseudocode", r"Ghidra", r"dossier", r"corpus", r"vtable", r"offset", r"\bL\d{2,}", r"Python",
        r"configparser", r"GenericScript", r"_UserScript", r"_Framework", r"_Generic", r"create_instance", r"parse_int",
        r"parse_map_mode", r"getint", r"getboolean", r"c_instance", r"MidiMap", r"RemoteMapper", r"ATimeable",
        r"TControllerMapMode", r"OChangeController", r"PriorCValue", r"CValue", r"FLT_MAX", r"frinta", r"fmadd",
        r"float32", r"129\.0", r"-129", r"avoid_takeover", r"needs_takeover", r"set_needs", r"sensitivity", r"[Zz]oom",
        r"relative_smooth", r"quantiz", r"thread", r"handler", r"registry", r"dispatch", r"receiver", r"\benum\b",
        r"ButtonMatrix", r"EncoderElement", r"ChannelStrip", r"Component\b", r"\bS4-", r"\bMT-\d", r"\bN7", r"\bE1[0-4]\b",
        r"\bI[1-6]\b", r"PRB-", r"\bQ-0", r"S-cond", r"derivation", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/",
        r"ev_[0-9a-f]", r"sha256\s*[0-9a-f]{64}"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as the released packages


def payload(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md_path, root):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md_path.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md_path.parent / path).resolve() if path else md_path
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
    missing = [c["input"] for c in cases if not (d / c["input"]).is_file()]
    deny = {}
    for p in [*files, d / "manifest.json"]:
        hits = sorted({m for pat in DENY for m in re.findall(pat, p.read_text())} - ALLOWED_HITS.get(p.name, set()))
        if hits:
            deny[str(p.relative_to(d))] = hits
    symlinks = [str(p.relative_to(d)) for p in d.rglob("*") if p.is_symlink()]
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "manifest_case_count": man["case_count"],
            "cases": len(cases), "hash_or_size_mismatches": mismatches, "inventory_differences": inventory,
            "symlinks": symlinks, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad_links, "missing_case_inputs": missing, "deny_list_hits": deny,
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def spec_mt_table():
    rows = {}
    for line in SPEC.read_text().splitlines():
        m = re.match(r"\|\s*(MT-\d\d)\s*\|\s*(S|S-cond)\s*\|.*\|\s*([^|]+?)\s*\|\s*$", line)
        if m:
            rows[m[1]] = (m[2], m[3])
    assert len(rows) == 23, len(rows)
    return rows


def check_values(cases):
    """Compare value-case expectations with the spec table, the N7 case file and the N7 float32 model."""
    dc = load("n7_derive_cases", N7 / "scripts/derive_cases.py")
    n7 = {c["id"]: c for c in json.loads((N7 / "out/acceptance-cases.json").read_text())["cases"]}
    table = spec_mt_table()
    by_id = {c["id"]: c for c in cases}
    problems, included = {}, set()
    choices = {"none": [dc.NONE], "any": [dc.NONE, dc.PICKUP, dc.SCALING]}
    for n, mt, _, control, mode, takeover, p, msgs in VALUE:
        c, errs = by_id[cid(n)], []
        got = c["expected"]["values"]
        included.add(mt)
        label, spec_vals = table[mt]
        if label != "S":
            errs.append(f"spec label {label}")
        spec_nums = [float(t) for t in spec_vals.split(",")]
        if len(spec_nums) != len(got) or any(abs(x - y) > TOL for x, y in zip(spec_nums, got)):
            errs.append(f"spec table {spec_nums} != {got}")
        n7v = n7[mt]["expected_after_each_message"]
        if n7[mt]["input"] != c["stimulus"]["messages"] or n7[mt]["map_mode"] != mode:
            errs.append("N7 case input or mode differs")
        if any(abs(x - y) > TOL for x, y in zip(n7v, got)) or len(n7v) != len(got):
            errs.append(f"N7 case file {n7v} != {got}")
        for tm in choices[takeover]:
            m = dc.Mapping(mode, lo=p["min"], hi=p["max"], quant=p["stepped"], value=p["initial_value"],
                           avoid=control == "CrossfaderSlider", tm=tm)
            mv = dc.run(m, NUM, msgs)
            if any(abs(x - y) > TOL for x, y in zip(mv, got)) or len(mv) != len(got):
                errs.append(f"N7 model under takeover choice {tm}: {mv} != {got}")
        if len(got) != len(msgs) or any(not re.fullmatch(r"B0 (14|34) [0-7][0-9A-F]", s) for s in c["stimulus"]["messages"]):
            errs.append("message format")
        if errs:
            problems[c["id"]] = errs
    excluded = {k for k, (lab, _) in table.items() if lab == "S-cond"}
    # the payload's decode table and A, B lists must equal the spec's and the restatement's
    row = re.compile(r"\s*\| `(?:Linear|Accel)\w+` \|")
    wiki_rows = [x.strip() for x in SPEC.read_text().splitlines() if row.match(x)]
    text = (STAGE / "spec.md").read_text()
    pay_rows = [x.strip() for x in text.splitlines() if row.match(x)]
    lists = {k: [int(x) for x in re.search(k + r"\(\*k\*\) is ([\d, ]+?),? for", text)[1].split(", ")] for k in "AB"}
    if wiki_rows != pay_rows or len(pay_rows) != 8 or lists != {"A": A_TAB, "B": B_TAB}:
        problems["spec.md"] = ["decode table or A/B lists differ from the parent spec or the restatement"]
    selection = {"spec_S_rows_released": sorted(included), "spec_S_cond_rows_excluded": sorted(excluded),
                 "selection_matches_spec_labels": included == {k for k, (lab, _) in table.items() if lab == "S"}
                 and excluded == set(EXCLUDED_SPEC_CASES)}
    # decode tables: restatement vs N7 model over all data values; A/B vs image constants
    consts = json.loads((N7 / "out/native-constants.json").read_text())
    table_diffs = [(m, v) for m in DECODE for v in range(128) if dc.decode(float(v), dc.MODE[m]) != DECODE[m](v)]
    tables_ok = (consts["table_B_0x10584a580_modes_2_3_4"] == B_TAB
                 and consts["table_A_0x10584a5a0_mode_1_first8"] + [consts["table_A_ninth_element_stored_by_0x101b842cc"]] == A_TAB)
    # the restatement refuses excluded inputs
    probes = {}
    for name, args in {
        "on/off parameter": ("Encoder1", "Absolute", "none", {**CONT, "kind": "on/off"}, on(0x40)),
        "min above max": ("Encoder1", "Absolute", "none", {**CONT, "min": 1, "max": 0}, on(0x40)),
        "stepped, non-integer value": ("Encoder1", "LinearSignedBit", "any", {**STEP, "initial_value": 1.5}, on(0x01)),
        "Absolute, continuous, takeover any": ("Encoder1", "Absolute", "any", CONT, on(0x40)),
        "crossfader Absolute14Bit, takeover any": ("CrossfaderSlider", "Absolute14Bit", "any", CONT, [(NUM, 1), (NUM + 32, 1)]),
    }.items():
        try:
            model_values(*args)
            probes[name] = "EXPECTATION GIVEN (wrong)"
        except NoExpectation as e:
            probes[name] = f"no expectation: {e}"
    # finding F1: in the N7 model the 14-bit path ignores the crossfader opt-out, so Pick-Up holds the first pair
    f1 = {mode: dc.run(dc.Mapping(mode, avoid=True, tm=dc.PICKUP), NUM, msgs) for mode, msgs in
          (("Absolute", [(NUM, 0x20)]), ("Absolute14Bit", [(NUM, 0x20), (NUM + 32, 0x00)]))}
    return problems, selection, {"decode_differences": table_diffs, "tables_match_image_constants": tables_ok,
                                 "excluded_input_probes": probes,
                                 "crossfader_pickup_in_N7_model_from_0.5": f1}


def n7_identity():
    man = json.loads((N7 / "manifest.json").read_text())
    bad = [k for k, v in man["files"].items() if not (N7 / k).is_file() or sha((N7 / k).read_bytes()) != v["sha256"]]
    return {"n7_manifest_sha256": sha((N7 / "manifest.json").read_bytes()), "n7_target": man["target"],
            "n7_files_listed": len(man["files"]), "n7_file_mismatches": bad}


def seal():
    cm = load("v2_crosscheck_model", V2A / "crosscheck_model.py")
    doc = json.loads((STAGE / "cases.json").read_text())
    cases = doc["cases"]
    v2 = json.loads((V2 / "cases.json").read_text())["cases"]
    carry = {"v2_case_records_identical": cases[:len(v2)] == v2,
             "v2_fixture_bytes_identical": all((STAGE / c["input"]).read_bytes() == (V2 / c["input"]).read_bytes() for c in v2),
             "v2_representation_fields_kept": all(doc["representation"][k] == v for k, v in
                                                  json.loads((V2 / "cases.json").read_text())["representation"].items())}
    problems = {}
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        errs = []
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n") or re.search(rb"[\x00-\x09\x0b-\x1f\x7f]", raw):
            errs.append("fixture not ASCII/LF/newline-terminated or has control characters")
        configparser.ConfigParser().read_file(io.StringIO(raw.decode("ascii")))  # must not raise
        if cm.canon(cm.interpret(raw.decode("ascii"))) != cm.canon(c["expected"]):
            errs.append("v2 interpretation cross-check disagrees")
        addrs = [(x["message_type"], x["number"], x["channel"]) for x in c["expected"]["assignments"]]
        if len(set(addrs)) != len(addrs):
            errs.append("duplicate MIDI address")
        if errs:
            problems[c["id"]] = errs
    vproblems, selection, tables = check_values(cases[len(v2):])
    for k, v in vproblems.items():
        problems.setdefault(k, []).extend(v)
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    # v2 -> v3 text changes for review: every removed v2 line is listed
    diffs, removed = [], {}
    for name in ("README.md", "AGENTS.md", "spec.md"):
        old, new = (V2 / name).read_text().splitlines(), (STAGE / name).read_text().splitlines()
        diffs += difflib.unified_diff(old, new, f"midi-config-v2/{name}", f"midi-config-v3/{name}", lineterm="")
        removed[name] = sum(1 for line in difflib.ndiff(old, new) if line.startswith("- "))
    (HERE / "v2-to-v3-text.diff").write_text("\n".join(diffs) + "\n")
    report = {"schema": "author-validation-v1", "package": "midi-config-v3 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "carried_from_v2": carry, "value_selection": selection, "value_tables": tables,
              "v2_lines_changed_or_removed": removed, "evidence_identity": n7_identity(), "text_diff": "v2-to-v3-text.diff", **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed. The restatement, the spec "
                        "table, the N7 case file and the N7 float32 model share the same static evidence; none is an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    trace = {"schema": "midi-config-v3-traceability", "status": "analyst-only; never part of the payload",
             "parent_spec": "SPEC-MIDI-USER-MAPPING revision 3 (wiki/specs/midi-user-mapping.md)",
             "plan": "wiki/specs/midi-config-v3-handoff-plan.md", "supersedes": "midi-config-v2",
             "evidence_identity": n7_identity(), "evidence": EVIDENCE, "inferred": INFERRED,
             "clauses": {k: {"evidence": e, "inferred": i} for k, (e, i) in CLAUSES.items()},
             "cases": {c["id"]: {"source": f"midi-config-v2 {c['id']} (record and fixture unchanged)", "evidence": ["v2"]}
                       for c in v2},
             "excluded_spec_cases": EXCLUDED_SPEC_CASES}
    for n, mt, _, control, mode, takeover, _, _ in VALUE:
        e, i = CASE_EVIDENCE_KINDS[CASE_EVIDENCE[mt]]
        trace["cases"][cid(n)] = {"source": f"SPEC-MIDI-USER-MAPPING r3 {mt} (label S)", "evidence": e, "inferred": i,
                                  "takeover": takeover}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "carried_from_v2", "value_selection",
                                             "payload_files", "hash_or_size_mismatches", "inventory_differences",
                                             "unresolved_links", "missing_case_inputs", "deny_list_hits",
                                             "manifest_sha256")}, indent=1))
    print(json.dumps(tables, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
