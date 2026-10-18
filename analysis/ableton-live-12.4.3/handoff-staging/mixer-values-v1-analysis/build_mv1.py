"""Stage the mixer-values-v1 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from any directory:
  python3 -I build_mv1.py build          # fixtures/, cases.json, draft manifest.json (files[] empty)
  python3 -I build_mv1.py seal           # manifest files[], author-validation.json, traceability.json
  python3 -I build_mv1.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Fixtures are written here from one template authored for this release; no shipped file is read.
Expected values, texts and names in CASES are hand-authored from SPEC-MIXER-VALUES r1 (narrowed; see
wiki/specs/mixer-values-handoff-plan.md). seal cross-checks them with model(), an independent restatement
of the released clauses that also checks every input stays clear of the excluded boundaries. It shares
the same static evidence and is not an oracle. README.md, AGENTS.md and spec.md are hand-written.
"""
import hashlib, json, math, re, struct, sys
import xml.etree.ElementTree as ET
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "mixer-values-v1"
EVID = ROOT / "analysis/ableton-live-12.4.3"
IMAGE_SHA = "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
PROV = "static-derived; not observed reference output"
R = "REQ-MIXER-VALUES-"
MIN, VMAX = "0.0003162277571", "1.99526238"

# mixer key -> (path below LiveSet, track element attributes, send holder EnabledByUser or None for no sends)
MIXERS = {
    "audio": ("Tracks/AudioTrack", ' Id="11"', "true"),
    "midi": ("Tracks/MidiTrack", ' Id="12"', "true"),
    "return": ("Tracks/ReturnTrack", ' Id="13"', "false"),
    "main": ("MainTrack", "", None),
    "cue": ("PreHearTrack", "", None),
}
MANUAL = ["Speaker", "Pan", "SplitStereoPanL", "SplitStereoPanR", "Volume", "CrossFadeState"]
BASE = {"Send": MIN, "Speaker": "true", "SoloSink": "false", "PanMode": "0", "Pan": "0", "SplitStereoPanL": "-1",
        "SplitStereoPanR": "1", "Volume": "1", "CrossFadeState": "1", "CrossFade": "0"}


def doc(changes=None):
    """Template document with {(mixer, element): text} or {("set", "CrossfadeCurve"): text} changes."""
    ch = changes or {}
    v = lambda m, k: ch.get((m, k), BASE[k])
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<Ableton MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1">', "  <LiveSet>", "    <Tracks>"]
    for m, (path, attrs, enabled) in MIXERS.items():
        tag = path.split("/")[-1]
        d = 6 if path.startswith("Tracks/") else 4
        p = " " * d
        out += [f"{p}<{tag}{attrs}>", f"{p}  <DeviceChain>", f"{p}    <Mixer>"]
        q = p + "      "
        if enabled is None:
            out.append(f"{q}<Sends />")
        else:
            out += [f"{q}<Sends>", f'{q}  <TrackSendHolder Id="0">', f"{q}    <Send>",
                    f'{q}      <Manual Value="{v(m, "Send")}" />', f"{q}    </Send>",
                    f'{q}    <EnabledByUser Value="{enabled}" />', f"{q}  </TrackSendHolder>", f"{q}</Sends>"]
        for k in ["Speaker", "SoloSink", "PanMode", "Pan", "SplitStereoPanL", "SplitStereoPanR", "Volume",
                  "CrossFadeState"] + (["CrossFade"] if m == "main" else []):
            if k in ("SoloSink", "PanMode"):
                out.append(f'{q}<{k} Value="{v(m, k)}" />')
            else:
                out += [f"{q}<{k}>", f'{q}  <Manual Value="{v(m, k)}" />', f"{q}</{k}>"]
        out += [f"{p}    </Mixer>", f"{p}  </DeviceChain>", f"{p}</{tag}>"]
        if m == "return":
            out.append("    </Tracks>")
    out += [f'    <CrossfadeCurve Value="{ch.get(("set", "CrossfadeCurve"), "2")}" />', "  </LiveSet>", "</Ableton>", ""]
    return "\n".join(out).encode("ascii")


def V(value, text=None, name=None):
    e = {"value": value}
    if text is not None:
        e["text"] = text
    if name is not None:
        e["name"] = name
    return e


STRIP = {"Volume": V(1.0, "0.0 dB"), "Pan": V(0.0, "C"), "SplitStereoPanL": V(-1.0, "50L"),
         "SplitStereoPanR": V(1.0, "50R"), "PanMode": V(0, name="Stereo"), "Speaker": V(True, "On"),
         "CrossFadeState": V(1, name="None")}
SENDMIN = V(0.0003162277571391314, "-inf dB")
BASE_EXPECT = {
    **{f"audio/{k}": e for k, e in STRIP.items()}, "audio/Send": SENDMIN,
    **{f"midi/{k}": e for k, e in STRIP.items()}, "midi/Send": SENDMIN,
    **{f"return/{k}": e for k, e in STRIP.items()},
    "main/Volume": V(1.0, "0.0 dB"), "main/Pan": V(0.0, "C"), "main/CrossFade": V(0.0),
    "cue/Volume": V(1.0, "0.0 dB"),
    "set/CrossfadeCurve": V(2, name="Constant Power"),
}
BASE_COUNTS = {"audio": 1, "midi": 1, "main": 0, "cue": 0}
CURVES = ["Dipped", "Intermediate", "Constant Power", "Slow Fade", "Slow Cut", "Fast Cut", "Transition"]

# (n, kind, requirement suffixes, purpose, changes, expected values, expected send counts)
CASES = [
    (1, "positive", ["001", "002", "003", "004", "006", "007", "008", "009"],
     "Template document: every value at its template text", {}, BASE_EXPECT, BASE_COUNTS),
    (2, "positive", ["002", "006"], "Audio volume 0.5011872053 (-6 dB)",
     {("audio", "Volume"): "0.5011872053"}, {"audio/Volume": V(0.5011872053146362, "-6.0 dB")}, None),
    (3, "positive", ["001", "002", "006"], "Main volume 0.7367056608, three decimals",
     {("main", "Volume"): "0.7367056608"}, {"main/Volume": V(0.7367056608200073, "-2.654 dB")}, None),
    (4, "positive", ["006"], "Audio volume 0.5, three decimals",
     {("audio", "Volume"): "0.5"}, {"audio/Volume": V(0.5, "-6.021 dB")}, None),
    (5, "positive", ["006"], "Audio volume 0.25, three decimals above 10 dB magnitude",
     {("audio", "Volume"): "0.25"}, {"audio/Volume": V(0.25, "-12.041 dB")}, None),
    (6, "boundary", ["002", "006"], "Audio volume at the top of its range (+6 dB)",
     {("audio", "Volume"): VMAX}, {"audio/Volume": V(1.9952623844146729, "6.0 dB")}, None),
    (7, "boundary", ["002", "006"], "Audio volume at the bottom of its range (-70 dB)",
     {("audio", "Volume"): MIN}, {"audio/Volume": V(0.0003162277571391314, "-inf dB")}, None),
    (8, "boundary", ["006"], "Audio volume 0.99999: rounds to zero decibels, no minus sign",
     {("audio", "Volume"): "0.99999"}, {"audio/Volume": V(0.9999899864196777, "0.0 dB")}, None),
    (9, "boundary", ["006"], "Audio volume 0.0003311311302 (-69.6 dB), above the -inf limit",
     {("audio", "Volume"): "0.0003311311302"}, {"audio/Volume": V(0.0003311311302240938, "-69.6 dB")}, None),
    (10, "boundary", ["006"], "Audio volume 0.0003235936455 (-69.8 dB), at or below the -inf limit",
     {("audio", "Volume"): "0.0003235936455"}, {"audio/Volume": V(0.00032359364558942616, "-inf dB")}, None),
    (11, "positive", ["006"], "Audio volume 0.30725: trailing zero removed, two decimals remain",
     {("audio", "Volume"): "0.30725"}, {"audio/Volume": V(0.3072499930858612, "-10.25 dB")}, None),
    (12, "positive", ["001", "006"], "MIDI track volume 0.03548133373 (-29 dB)",
     {("midi", "Volume"): "0.03548133373"}, {"midi/Volume": V(0.03548133373260498, "-29.0 dB")}, None),
    (13, "positive", ["001", "006"], "Return track volume 1.5, positive with three decimals",
     {("return", "Volume"): "1.5"}, {"return/Volume": V(1.5, "3.522 dB")}, None),
    (14, "boundary", ["001", "002", "006"], "Cue volume at the top of its range (+6 dB)",
     {("cue", "Volume"): VMAX}, {"cue/Volume": V(1.9952623844146729, "6.0 dB")}, None),
    (15, "positive", ["003", "006"], "Audio send 0.1 (-20 dB)",
     {("audio", "Send"): "0.1"}, {"audio/Send": V(0.10000000149011612, "-20.0 dB")}, None),
    (16, "boundary", ["003", "006"], "Audio send at the top of its range (0 dB)",
     {("audio", "Send"): "1"}, {"audio/Send": V(1.0, "0.0 dB")}, None),
    (17, "boundary", ["001", "003", "006"], "MIDI track send 0.0003311311302 (-69.6 dB), above the -inf limit",
     {("midi", "Send"): "0.0003311311302"}, {"midi/Send": V(0.0003311311302240938, "-69.6 dB")}, None),
    (18, "positive", ["004", "007"], "Audio pan -0.6", {("audio", "Pan"): "-0.6"},
     {"audio/Pan": V(-0.6000000238418579, "30L")}, None),
    (19, "boundary", ["007"], "Audio pan 0.004999999888, inside the centre band",
     {("audio", "Pan"): "0.004999999888"}, {"audio/Pan": V(0.004999999888241291, "C")}, None),
    (20, "boundary", ["007"], "Audio pan 0.01, at the edge of the centre band",
     {("audio", "Pan"): "0.01"}, {"audio/Pan": V(0.009999999776482582, "C")}, None),
    (21, "boundary", ["007"], "Audio pan 0.0101, just right of the centre band",
     {("audio", "Pan"): "0.0101"}, {"audio/Pan": V(0.010099999606609344, "1R")}, None),
    (22, "boundary", ["007"], "Audio pan -0.0101, just left of the centre band",
     {("audio", "Pan"): "-0.0101"}, {"audio/Pan": V(-0.010099999606609344, "1L")}, None),
    (23, "boundary", ["004", "007"], "Audio pan 1 (hard right)", {("audio", "Pan"): "1"},
     {"audio/Pan": V(1.0, "50R")}, None),
    (24, "boundary", ["004", "007"], "Audio pan -1 (hard left)", {("audio", "Pan"): "-1"},
     {"audio/Pan": V(-1.0, "50L")}, None),
    (25, "boundary", ["007"], "Audio pan 0.33: the stored binary32 value, not the decimal, is rounded",
     {("audio", "Pan"): "0.33"}, {"audio/Pan": V(0.33000001311302185, "17R")}, None),
    (26, "positive", ["001", "007"], "Main pan 0.2", {("main", "Pan"): "0.2"},
     {"main/Pan": V(0.20000000298023224, "10R")}, None),
    (27, "positive", ["004", "007"], "Audio pan mode 1 with split pans -0.5 and 0.5",
     {("audio", "PanMode"): "1", ("audio", "SplitStereoPanL"): "-0.5", ("audio", "SplitStereoPanR"): "0.5"},
     {"audio/PanMode": V(1, name="Split Stereo"), "audio/SplitStereoPanL": V(-0.5, "25L"),
      "audio/SplitStereoPanR": V(0.5, "25R")}, None),
    (28, "positive", ["009"], "Audio crossfade assignment code 0", {("audio", "CrossFadeState"): "0"},
     {"audio/CrossFadeState": V(0, name="A")}, None),
    (29, "positive", ["009"], "Audio crossfade assignment code 2", {("audio", "CrossFadeState"): "2"},
     {"audio/CrossFadeState": V(2, name="B")}, None),
    (30, "positive", ["008"], "Audio track switch false", {("audio", "Speaker"): "false"},
     {"audio/Speaker": V(False, "Off")}, None),
] + [
    (31 + i, "boundary" if c in (0, 6) else "positive", ["009"], f"Crossfade curve code {c}",
     {("set", "CrossfadeCurve"): str(c)}, {"set/CrossfadeCurve": V(c, name=CURVES[c])}, None)
    for i, c in enumerate((0, 1, 3, 4, 5, 6))
] + [
    (37, "positive", ["001", "009"], "Main crossfader -0.25", {("main", "CrossFade"): "-0.25"},
     {"main/CrossFade": V(-0.25)}, None),
]
COMPARATOR = ("outcome exact; each listed value exact (binary32 compared after exact widening; Booleans and codes "
              "exact); text and name exact strings; send counts exact; unlisted values not judged")


# ---- independent cross-check model of the released clauses (not an oracle) ----
class Excluded(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def f32_step(x, k):
    b = struct.unpack("<I", struct.pack("<f", x))[0]
    return struct.unpack("<f", struct.pack("<I", b + (k if x > 0 else -k)))[0]


DOMAIN = {"Volume": (f32(float(MIN)), f32(float(VMAX))), "Send": (f32(float(MIN)), 1.0), "Pan": (-1.0, 1.0),
          "SplitStereoPanL": (-1.0, 1.0), "SplitStereoPanR": (-1.0, 1.0), "CrossFade": (-1.0, 1.0)}
CODES = {"PanMode": ["Stereo", "Split Stereo"], "CrossFadeState": ["A", "None", "B"], "CrossfadeCurve": CURVES}


def read_number(text, key):
    if not re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", text):
        raise Excluded(f"number form {text!r}")
    exact = Fraction(text)
    v = f32(float(text))  # nearest binary64, then nearest binary32
    if exact != 0:  # single rounding must agree and the text must not lie within 1% of a step of a halfway point
        for n in (f32_step(v, -1), f32_step(v, 1)):
            mid = (Fraction(v) + Fraction(n)) / 2
            if abs(exact - Fraction(v)) >= abs(exact - Fraction(n)) or \
                    abs(exact - mid) < abs(Fraction(n) - Fraction(v)) / 100:
                raise Excluded(f"rounding of {text!r}")
    a, b = DOMAIN[key]
    if not a <= v <= b:
        raise Excluded(f"{key} {text!r} outside its range")
    return v


def db_text(g):
    getcontext().prec = 40
    exact_db = Decimal(g).log10() * 20
    milli = exact_db * 1000
    if abs(exact_db - Decimal("-69.7")) < Decimal("0.00005") or \
            abs(milli - milli.to_integral_value(rounding="ROUND_FLOOR") - Decimal("0.5")) < Decimal("0.05"):
        raise Excluded(f"gain {g!r} within 0.00005 dB of a text boundary")
    texts = set()
    l0 = f32(math.log10(g))
    # tolerate the platform logarithm differing by up to two binary32 steps (log10 of 1 is exact)
    for l in ([l0] if l0 == 0 else [f32_step(l0, k) for k in range(-2, 3)]):
        db = f32(l * 20.0)
        if db <= -70.0 + 0.3:
            texts.add("-inf dB")
        elif round(abs(db) * 1000) == 0:
            texts.add("0.0 dB")
        else:
            s = ("%.3f" % db).rstrip("0")
            texts.add((s + "0" if s.endswith(".") else s) + " dB")
    if len(texts) != 1:
        raise Excluded(f"unstable text for {g!r}: {texts}")
    return texts.pop()


def pan_text(p):
    if -0.01 <= p <= 0.01:
        return "C"
    q = abs(p) * 50
    assert Fraction(q) == abs(Fraction(p)) * 50  # exact for binary32 inputs
    if q - math.floor(q) == 0.5:
        raise Excluded(f"pan tie {p!r}")
    return "%d%s" % (math.floor(q + 0.5), "L" if p < 0 else "R")


def entry(key, el_text):
    if key in CODES:
        if not re.fullmatch(r"[0-9]+", el_text) or int(el_text) >= len(CODES[key]):
            raise Excluded(f"{key} code {el_text!r}")
        return V(int(el_text), name=CODES[key][int(el_text)])
    if key == "Speaker":
        if el_text not in ("true", "false"):
            raise Excluded(f"Boolean {el_text!r}")
        return V(el_text == "true", "On" if el_text == "true" else "Off")
    v = read_number(el_text, key)
    if key in ("Volume", "Send"):
        return V(v, db_text(v))
    return V(v) if key == "CrossFade" else V(v, pan_text(v))


def model(xml_bytes):
    """Return (outcome, values, send counts); raise Excluded for inputs without an expectation."""
    root = ET.fromstring(xml_bytes)
    assert root.tag == "Ableton" and root.attrib == {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                                      "SchemaChangeCount": "1"}
    ls = root.find("LiveSet")
    if len(ls.findall("Tracks/ReturnTrack")) != 1:
        raise Excluded("return track count")
    values, counts = {}, {}
    for m, (path, _, enabled) in MIXERS.items():
        mx = ls.findall(path + "/DeviceChain/Mixer")
        assert len(mx) == 1, path
        mx = mx[0]
        holders = mx.findall("Sends/TrackSendHolder")
        if len(holders) != (0 if enabled is None else 1) or [h.get("Id") for h in holders] not in ([], ["0"]):
            raise Excluded(f"{m} send holders")
        for h in holders:
            if h.find("EnabledByUser").get("Value") != enabled:
                raise Excluded(f"{m} EnabledByUser")
        if mx.find("SoloSink").get("Value") != "false":
            raise Excluded(f"{m} SoloSink")
        if any(c.tag.endswith("KeyMidi") for c in mx.iter()):
            raise Excluded("KeyMidi")
        counts[m] = len(holders)
        for k in MANUAL + (["CrossFade"] if m == "main" else []):
            els = mx.findall(k + "/Manual")
            assert len(els) == 1, (m, k)
            values[f"{m}/{k}"] = entry(k, els[0].get("Value"))
        values[f"{m}/PanMode"] = entry("PanMode", mx.find("PanMode").get("Value"))
        if holders:
            values[f"{m}/Send"] = entry("Send", holders[0].find("Send/Manual").get("Value"))
    values["set/CrossfadeCurve"] = entry("CrossfadeCurve", ls.find("CrossfadeCurve").get("Value"))
    return "opens", values, counts


def judge(expected, outcome, values, counts):
    errs = [] if outcome == expected["outcome"] else [f"outcome {outcome}"]
    for k, e in expected["values"].items():
        got = values.get(k)
        if got is None or any(got.get(f) != e[f] or type(got.get(f)) is not type(e[f]) for f in e):
            errs.append(f"{k}: model {got} != expected {e}")
    for k, n in expected.get("send_counts", {}).items():
        if counts.get(k) != n:
            errs.append(f"send count {k}")
    return errs


# ---- packaging ----
def sha(b):
    return hashlib.sha256(b).hexdigest()


def cid(n):
    return f"MIXER-VALUES-{n:03d}"


def manifest_meta():
    return {
        "schema": "handoff-manifest-v1", "release_id": "mixer-values-v1", "release_status": "candidate-unreviewed",
        "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-MIXER-VALUES", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-AUDIO", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {
            R + "001": "Mixer location per track type and the value elements read; same rules for every track type; homonymous elements elsewhere are different values",
            R + "002": "Volume is a binary32 linear gain; expectations from 0.0003162277571 to 1.99526238 only",
            R + "003": "One send per return track on audio, MIDI, group and return mixers, none on main and cue; send is a binary32 linear gain from 0.0003162277571 to 1; documents with one return track only",
            R + "004": "Pan and split pans are binary32 values from -1 to 1; pan mode codes 0 Stereo and 1 Split Stereo",
            R + "006": "Volume and send value text: binary32 decibels, -inf dB at or below -69.7, otherwise three decimals with trailing zeros removed to one, unit dB; inputs near text boundaries excluded",
            R + "007": "Pan value text: C within +-0.01, otherwise 50 times the magnitude rounded, with L or R; exact halfway values excluded",
            R + "008": "Track switch Boolean with text On and Off; SoloSink meaning not released",
            R + "009": "Crossfade assignment codes A, None, B; crossfader location and range; crossfade curve codes 0 to 6 and their names; curve shapes not released",
        },
        "unreleased_requirements": [R + n for n in ("005", "010", "011", "012", "013", "014", "015")],
        "compatibility_dimensions": {
            "project-files": "static-derived expectations for values read from documents; reference execution not-run",
            "ui-text": "static-derived value texts and code names; the place that shows them is not specified; reference execution not-run",
            "file-format-written": "excluded (REQ-MIXER-VALUES-010)",
            "audio": "excluded (REQ-MIXER-VALUES-011 to 014)",
            "behavior": "editing, fader positions and controller mapping excluded (REQ-MIXER-VALUES-005)",
            "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "number text other than an optional minus sign, digits and an optional point with digits, for example exponents, a plus sign, spaces, empty text, inf, nan, hexadecimal or # forms; a missing Value attribute",
                "Boolean text other than true and false; code text other than unsigned decimal digits",
                "volumes outside 0.0003162277571 to 1.99526238, sends outside 0.0003162277571 to 1, pans, split pans and crossfader outside -1 to 1, pan mode other than 0 and 1, crossfade assignment other than 0 to 2, crossfade curve other than 0 to 6",
                "volumes and sends whose exact decibel value lies within 0.00005 dB of -69.7, of +-0.0005, or of a number halfway between two consecutive multiples of 0.001",
                "pan and split pan values -0.75, -0.25, 0.25 and 0.75",
                "documents with no return track or more than one; send holders not equal to one per return track; holder Id other than 0; EnabledByUser other than true on audio, MIDI and group holders and false on the return track's own holder; SoloSink other than false",
                "missing, duplicated or unknown mixer value elements; value elements in another order; a track without a mixer; any KeyMidi child in a mixer",
                "automation, clip envelopes, modulation or MIDI and key mappings that target a mixer value",
                "other envelopes, format versions, compressed containers and document kinds; host locales whose decimal separator is not '.'",
            ],
            "behavior": [
                "what is written on save (REQ-MIXER-VALUES-010)",
                "effect of volume, sends, pan, pan mode, track switch, crossfader and crossfade assignment on audio, the silence limit, ramps and curve shapes (REQ-MIXER-VALUES-011 to 014)",
                "out-of-range and alternative stored values (REQ-MIXER-VALUES-015)",
                "fader positions, the position-to-gain curves and controller mappings (REQ-MIXER-VALUES-005)",
                "which part of the user interface shows which text, and any other form of the same value, such as digits without the unit or without -inf",
                "editing after opening, including text entry, keys, mouse, remote control and MIDI; creating tracks and the values of new mixers and send holders; undo",
                "the meaning of EnabledByUser and SoloSink; the return mixer's own send; whether the cue volume is the preview level; crossfader value text",
            ],
        },
        "fixture_origin": "independently authored minimal XML documents from one template; no shipped file content or program code",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    for old in (STAGE / "fixtures").glob("*"):
        old.unlink()
    cases = []
    for n, kind, reqs, purpose, changes, values, counts in CASES:
        rel = f"fixtures/{cid(n)}.xml"
        (STAGE / rel).write_bytes(doc(changes))
        expected = {"outcome": "opens", "values": values}
        if counts:
            expected["send_counts"] = counts
        cases.append({"id": cid(n), "kind": kind, "purpose": purpose, "requirements": [R + r for r in reqs],
                      "input": rel, "action": "open", "expected": expected, "expectation_provenance": PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run", "comparator": COMPARATOR})
    doc_ = {"schema": "mixer-values-cases-v1", "target": TARGET,
            "scope": "mixer-values-v1 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
            "fixture_origin": "Independently authored minimal XML documents; no shipped file copied or excerpted",
            "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
            "representation": {
                "mixers": "audio, midi, return, main, cue (see spec.md); set for the Live Set itself",
                "values": "<mixer>/<element> -> value (binary32 number, Boolean or integer code) and text or name",
                "send_counts": "mixer -> number of sends",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- traceability (analyst-only; never shipped) ----
S9 = "analysis/ableton-live-12.4.3/r2/s9-mixer-v1/"
D8 = "analysis/ableton-live-12.4.3/r2/d8-mixer-v1/"
E = {
    "doc-form": S9 + "static-survey.json documents.tracks (1,340 mixers in 376 documents; children in schema order; "
                "no KeyMidi), returns_per_doc (sends minus returns = 0 for 588 mixers; main and cue none); schema "
                "12.0_12402.txt TrackDevice, MainTrackDevice, TrackSendHolder, LiveSet lines 3802-3844",
    "ctor": S9 + "results/s9-0001/functions/0x10271b660 (volume 0x1026f0bcc(0,1,1) at 0x10271be44-0x10271be68; "
            "Speaker 0x1026ec1cc with formatter 0x10143b884 at .c lines 284-287; CrossFadeState entries A/None/B "
            "0x1026ef060 at 0x10271bf38; dB formatter 0x1023e06fc(3,1,1,1) at 0x10271c138-0x10271c16c)",
    "pan-ctor": S9 + "results/s9-0001/functions/0x10271c734 (PanMode entries Stereo/Split Stereo via 0x101567ad8, "
                "index 0; Pan, Left, Right (-1,1,0/-1/1); pan text singleton 0x101439ec4)",
    "send-ctor": S9 + "results/s9-0002/functions/0x102658f54 (.c lines 72-96: own 0x1023e06fc(3,1,1,1) guard, "
                 "0x1026f0b58(0,1,curve(0)); control 0x1026605c8 mode 0)",
    "ranges": S9 + "image-reads.txt read_mem 0x10588302c/0x105883044 (mode 0 0x39a5cb5f-0x3f800000, mode 1 "
              "0x39a5cb5f-0x3fff64c2); results/s9-0002/functions/0x10255d93c",
    "gain-db": S9 + "results/s9-0002/functions/0x102183bf4 disassembly 0x102183c04-0x102183c3c (fcvt s0,d0; "
               "log10f; fmul 20.0f; fcvt d0,s0; g <= 0 -> -140.0); 0x102183abc (floor -70.0)",
    "db-text": S9 + "results/s9-0001/functions/0x101437334 (floor+0.3 -> -inf; decimals; ' dB'); 0x101431c6c "
               "disassembly 0x101431ca8-0x101431d38 (frinta(10^max*v)==0 -> 0.0; '%*.*f' via 0x1011bfe14; strip to "
               "min decimals); image-reads.txt vtable 0x106670140 (+0x28 0x101437334, +0x40 0x1014374b4 second "
               "form), 0x106774f60 (+0x28 0x102183bf4)",
    "pan-text": S9 + "results/s9-0002/functions/0x10143a290 (+-0.01 double compares, x+-50 double, C/L/R); " + D8
                + "results/d8-0002/functions/0x101431c60 (max = min = 0 decimals); image-reads.txt vtable 0x106670828 "
                "(+0x28 0x10143a290)",
    "speaker-text": S9 + "corpus-excerpts.jsonl records 0x10143b884 (singleton with vtable 0x106670bc8) and "
                    "0x10143ba28 ('Off' when value == 0.0 else 'On'); image-reads.txt vtable 0x106670bc8 (+0x28 "
                    "0x10143ba28)",
    "enum": S9 + "results/s9-0004/functions/0x101567ad8 (enum init stores index and entry list); " + D8
            + "results/d8-0002/functions/0x1026ef0dc (index passed to 0x101567bfc)",
    "curve-names": S9 + "corpus-excerpts.jsonl record 0x102672204 (seven names Dipped ... Transition); "
                   "results/s9-0003/functions/0x101aed36c (seven crossfade tables, same order); C1 corpus 0x102672448 "
                   "(set constructor: 0x101567bfc(member 0x3e, 2, name list); not retained, corpus identity in "
                   + S9 + "corpus-decomp-run.json); CrossfadeCurve in the 376 shipped LiveSet documents of "
                   + S9 + "inputs-documents.tsv: 2 in 375, 6 in 1 (counted while staging, 2026-10-18)",
    "c-locale": "wiki/specs/transport-state-handoff-plan.md#evidence-traceability review additions: 0x1011bfe14 is "
                "the C-locale vsnprintf_l; the display print 0x101431c6c calls it at 0x101431cdc",
    "reading": "wiki/research/transport-state-native.md#writer-number-format (N1 loader and writer); " + S9
               + "notes.md negative results ('by the N1 loader rule a direct store ... not re-traced for these "
               "classes'); results/s9-0001/functions/0x1026f0bcc (s2 -> Manual)",
}
I = {
    "I1": "Mixer value text is read by the generic loader: plain decimal -> nearest binary64 -> nearest binary32, "
          "Booleans true/false, codes decimal. Not re-traced for TimeableFloat, TimeableBool, TimeableEnum or "
          "RemoteableEnum; tempo (TimeableSongTempo) is a different class, so the transport-state-v1 check does not "
          "carry over by identity. Fixture numbers are chosen so single and double rounding agree.",
    "I2": "The value text of an enumerated value is its entry name (PanMode, CrossFadeState, CrossfadeCurve); the "
          "enum text routine is not traced.",
    "I3": "LiveSet/CrossfadeCurve is the set enum the set constructor initialises with the seven names and index 2 "
          "(corpus 0x102672448); member-to-element binding untraced; consistent with 375/376 shipped sets storing 2.",
    "I4": "The platform log10f is within one binary32 step of the correctly rounded result; the 0.00005 dB margin "
          "and the two-step tolerance in model() cover it.",
    "I5": "Split pans use the pan text converter: 0x10271c734 pseudocode passes singleton 0x101439ec4 for Pan and "
          "both splits; the confirmed branch is Pan's.",
    "I6": "The primary text slot (+0x28: unit and -inf) is the value text a user sees in at least one place; the "
          "second slot (+0x40) form is excluded; covered by the comparison obligation.",
}
CLAUSES = {
    R + "001 location and elements": (["doc-form", "ctor", "pan-ctor"], ["I1"]),
    R + "001 same rules for every track type": (["ctor", "pan-ctor", "send-ctor"], []),
    R + "002 volume binary32 gain and range": (["ctor", "ranges"], ["I1"]),
    R + "003 one send per return; main and cue none": (["doc-form"], []),
    R + "003 send binary32 gain and range": (["send-ctor", "ranges"], ["I1"]),
    R + "004 pan and split range; pan mode codes": (["pan-ctor", "enum"], ["I1", "I2"]),
    R + "006 volume and send text": (["gain-db", "db-text", "ctor", "send-ctor", "c-locale"], ["I4", "I6"]),
    R + "007 pan text": (["pan-text", "pan-ctor", "c-locale"], ["I5", "I6"]),
    R + "008 track switch text": (["ctor", "speaker-text"], ["I1", "I6"]),
    R + "009 crossfade assignment codes": (["ctor", "enum"], ["I1", "I2"]),
    R + "009 crossfader location and range": (["doc-form"], ["I1"]),
    R + "009 crossfade curve codes and names": (["curve-names", "enum"], ["I1", "I2", "I3"]),
}
TRACE = {
    1: "MV-001 (narrowed: EnabledByUser meaning and the return track's own send dropped; MIDI track added)",
    2: "MV-002", 3: "MV-003", 4: "MV-004 first value", 5: "MV-004 second value", 6: "MV-005", 7: "MV-006",
    8: "MV-007", 9: "MV-008", 10: "MV-009",
    11: "new: REQ-006 trailing-zero clause with two remaining decimals",
    12: "new: REQ-001 same rules on a MIDI track (value occurs in shipped APC40 Demo.als)",
    13: "new: REQ-001 same rules on a return track, positive three decimals",
    14: "new: REQ-001 same rules on the cue track (value occurs in 3 shipped cue mixers)",
    15: "MV-010", 16: "MV-011", 17: "new: REQ-006 -inf limit applied to a send",
    18: "MV-012", 19: "MV-013 first value", 20: "MV-013 second value", 21: "MV-014 first value",
    22: "MV-014 second value", 23: "MV-015 first value", 24: "MV-015 second value",
    25: "new: research correction 2026-10-17 (float32 0.33 -> 17R)", 26: "new: REQ-001 same pan rule on the main track",
    27: "MV-016", 28: "MV-017 first value", 29: "MV-017 second value", 30: "MV-018",
    31: "new: REQ-009 curve code 0", 32: "new: REQ-009 curve code 1", 33: "new: REQ-009 curve code 3",
    34: "new: REQ-009 curve code 4", 35: "MV-019", 36: "new: REQ-009 curve code 6",
    37: "new: REQ-009 crossfader location and range",
}
CASE_EVIDENCE = {
    "Volume": ["ctor", "ranges", "gain-db", "db-text"], "Send": ["send-ctor", "ranges", "gain-db", "db-text"],
    "Pan": ["pan-ctor", "pan-text"], "SplitStereoPanL": ["pan-ctor", "pan-text"],
    "SplitStereoPanR": ["pan-ctor", "pan-text"], "PanMode": ["pan-ctor", "enum"], "Speaker": ["ctor", "speaker-text"],
    "CrossFadeState": ["ctor", "enum"], "CrossFade": ["doc-form"], "CrossfadeCurve": ["curve-names", "enum"],
}
CASE_LINKS = {"Volume": ["I1", "I4", "I6"], "Send": ["I1", "I4", "I6"], "Pan": ["I1", "I6"],
              "SplitStereoPanL": ["I1", "I5", "I6"], "SplitStereoPanR": ["I1", "I5", "I6"], "PanMode": ["I1", "I2"],
              "Speaker": ["I1", "I6"], "CrossFadeState": ["I1", "I2"], "CrossFade": ["I1"],
              "CrossfadeCurve": ["I1", "I2", "I3"]}
# draft cases not carried, with reasons (plan page holds the same table)
NOT_RELEASED = {
    "MV-020, MV-021, MV-022": "REQ-010: the graded output is what a 12.4.3 save writes, the U part (PRB-S9-07)",
    "MV-023, MV-024, MV-025, MV-026": "REQ-005: fader positions not observable in scope; last-ulp platform values",
    "MV-027": "track creation is an edit; new-mixer defaults and their save text (PRB-S9-07)",
    "MV-028, MV-040 to MV-045": "U cases",
    "MV-029 to MV-039": "audio renders needing measurement; MV-029 to 034 also conditional on Q-019",
}

# ---- checks ----
DENY = [r"analysis/", r"wiki/", r"raw/", r"\.\./", r"0x[0-9a-fA-F]{4,}", r"FUN_", r"disassembl", r"decompil",
        r"pseudocode", r"Ghidra", r"vtable", r"dossier", r"corpus", r"\bPRB-", r"\bQ-0", r"\bMV-0", r"\bMX-",
        r"\bS9\b", r"\bD8\b", r"\bN1\b", r"\bI[1-9]\b", r"Timeable", r"Remoteable", r"TrackDevice", r"\bmp[A-Z]",
        r"LSong", r"ATrack", r"log10f", r"exp10", r"printf", r"frinta", r"%\.?\*", r"\bslot", r"singleton",
        r"Track Volume", r"Track Panning", r"Speaker On", r"X-Fade", r"Solo-Cue", r"Recording Audio",
        r"Sample Reference", r"APC40", r"12\.4d1", r"12\.1d1", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/",
        r"ev_[0-9a-f]", r"derive_curves", r"static-survey", r"traceab", r"\bB0\b", r"derivation", r"Python",
        r"Unexpected node", r"\+0x"]
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


def deny_hits(text, name):
    hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
    return [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(name, ()))]


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
    deny = {str(p.relative_to(d)): h for p in [*files, d / "manifest.json"] if (h := deny_hits(p.read_text(), p.name))}
    symlinks = [str(p.relative_to(d)) for p in d.rglob("*") if p.is_symlink()]
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "symlinks": symlinks,
            "markdown_links": {k: len(v) for k, v in link_rows.items()}, "unresolved_links": bad_links,
            "missing_case_inputs": missing_inputs, "deny_list_hits": deny,
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def evidence_identity():
    out = {"image_sha256_matches": sha((EVID / "derived/Live.arm64").read_bytes()) == IMAGE_SHA}
    for run in ("r2/s9-mixer-v1", "r2/d8-mixer-v1"):
        m = json.loads((EVID / run / "manifest.json").read_text())
        files = m["files"]
        bad = [p for p, h in files.items() if sha((EVID / run / p).read_bytes()) != (h["sha256"] if isinstance(h, dict) else h)]
        out[run] = {"manifest_sha256": sha((EVID / run / "manifest.json").read_bytes()), "files": len(files),
                    "mismatches": bad}
    out["s9_binary_sha256_matches"] = json.loads((EVID / "r2/s9-mixer-v1/manifest.json").read_text())["binary"]["sha256"] == IMAGE_SHA
    return out


def mutation_probe(cases):
    """Each case with one expected entry altered must be caught by the cross-check."""
    missed = []
    for c in cases:
        exp = json.loads(json.dumps(c["expected"]))
        k = next(iter(exp["values"]))
        e = exp["values"][k]
        if "text" in e:
            e["text"] += "x"
        elif "name" in e:
            e["name"] += "x"
        else:
            e["value"] = e["value"] + 1 if not isinstance(e["value"], bool) else not e["value"]
        if not judge(exp, *model((STAGE / c["input"]).read_bytes())):
            missed.append(c["id"])
    planted = deny_hits("see analysis/x and 0x10143a290 via PRB-S9-04 in a vtable", "spec.md")
    return {"mutated_cases": len(cases), "missed": missed, "planted_deny_terms_flagged": len(planted)}


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    problems, fixtures = {}, {}
    seen = {}
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        try:
            errs = judge(c["expected"], *model(raw))
        except Excluded as e:
            errs = [f"input has no expectation: {e}"]
        if not raw.isascii() or b"\r" in raw or b"\t" in raw or not raw.endswith(b"\n"):
            errs.append("not ASCII/LF/no-tab/final newline")
        if raw in seen:
            errs.append(f"same bytes as {seen[raw]}")
        seen[raw] = c["id"]
        changed = [ln for ln, base_ln in zip(raw.decode().split("\n"), doc().decode().split("\n")) if ln != base_ln]
        if errs:
            problems[c["id"]] = errs
        fixtures[c["id"]] = {"bytes": len(raw), "lines": raw.count(b"\n"), "lines_changed_from_template": changed}
    # excluded inputs must be rejected by the model
    probes = {"pan 0.25": {("audio", "Pan"): "0.25"}, "volume 2": {("audio", "Volume"): "2"},
              "volume 0.0001": {("audio", "Volume"): "0.0001"}, "send 1.0000001": {("audio", "Send"): "1.0000001"},
              "volume exponent": {("audio", "Volume"): "1e0"}, "volume -69.7 dB": {("audio", "Volume"): "0.00032734069"},
              "pan mode 2": {("audio", "PanMode"): "2"}, "curve 7": {("set", "CrossfadeCurve"): "7"},
              "speaker 1": {("audio", "Speaker"): "1"}, "dB tie -6.0625": {("audio", "Volume"): str(f32(10 ** (-6.0625 / 20)))}}
    rejected = {}
    for name, ch in probes.items():
        try:
            model(doc(ch))
            rejected[name] = False
        except Excluded:
            rejected[name] = True
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "mixer-values-v1 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "excluded_input_probes_rejected": rejected, "mutation_probe": mutation_probe(cases),
              "evidence_identity": evidence_identity(), "fixtures": fixtures, **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model restates the "
                        "same static evidence and is not an oracle; libm differences are emulated as +-2 binary32 steps."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    trace = {"schema": "mixer-values-traceability-v1", "spec": "SPEC-MIXER-VALUES r1", "evidence": E,
             "inferred_links": I,
             "clauses": {k: {"evidence": ev, "inferred": inf} for k, (ev, inf) in CLAUSES.items()},
             "cases": {}, "draft_cases_not_released": NOT_RELEASED}
    for c in cases:
        n = int(c["id"][-3:])
        els = sorted({k.split("/")[1] for k in c["expected"]["values"]})
        trace["cases"][c["id"]] = {
            "source": TRACE[n],
            "evidence": sorted({e for el in els for e in CASE_EVIDENCE[el]} | ({"doc-form"} if "send_counts" in c["expected"] else set())),
            "inferred": sorted({i for el in els for i in CASE_LINKS[el]})}
    assert set(trace["cases"]) == {c["id"] for c in cases} and set(E) >= {e for v in CLAUSES.values() for e in v[0]}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "excluded_input_probes_rejected",
                                             "mutation_probe", "evidence_identity", "payload_files",
                                             "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
                                             "missing_case_inputs", "deny_list_hits", "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
