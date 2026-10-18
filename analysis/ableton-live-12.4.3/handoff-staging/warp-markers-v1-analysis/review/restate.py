"""Reviewer's independent restatement of warp-markers-v1 (analyst side; not payload). Written without the
author's model. Usage: python3 -I restate.py <package dir>

Opening follows the contract's clauses. Calls are evaluated twice: (a) by the contract's clauses with exact
rational tempo, and (b) by the procedure the static evidence shows for the add (scan by SecTime, as-given
beat checks, the add's own floating-point grid rounding, inclusive beat bounds nb.beat + (bpm/60)*ds) and for
the remove/move lookup (same rounding, exact beat match). Both must equal each expectation. Each call case also
reports its distance from a rounding tie (grid steps), from a tempo limit (BPM) and from a neighbour's SecTime."""
import json, math, re, sys
import xml.etree.ElementTree as ET
from fractions import Fraction as Fr
from pathlib import Path

D = Path(sys.argv[1])
N = 3843840
STEP = 2.6015651015651016e-07
CLIP = "LiveSet/Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip"
SWP = ("LiveSet/Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/SampleParts/"
       "MultiSamplePart/SampleWarpProperties")
DEF = {"GranularityTones": 30, "GranularityTexture": 65, "FluctuationTexture": 25, "TransientResolution": 6,
       "TransientLoopMode": 2, "ComplexProFormants": 100, "ComplexProEnvelope": 128}
NUM = re.compile(r"[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?")


class Refused(Exception):
    pass


def number(text):  # REQ-002 clause 2/3
    t = text.lstrip(" ")
    m = NUM.match(t)
    if not m:
        raise Refused
    return float(m.group(0))


def open_doc(path):
    root = ET.parse(path).getroot()
    assert root.tag == "Ableton" and root[0].tag == "LiveSet"
    h = root.find(CLIP)
    key = "AudioClip"
    if h is None:
        h, key = root.find(SWP), "SampleWarpProperties"
    st = dict(DEF) if key == "AudioClip" else {}
    for el in h:
        if el.tag == "WarpMarkers":
            st["WarpMarkers"] = [[number(m.get("SecTime")), number(m.get("BeatTime"))] for m in el]
        elif el.tag == "IsWarped":
            st["IsWarped"] = {"true": True, "false": False}[el.get("Value")]
        elif el.get("Value") is not None and el.tag != "TransientEnvelope":
            st[el.tag] = int(el.get("Value"))
    return key, st


def q_exact(b):  # nearest grid point, halves away from zero
    x = abs(Fr(b)) * N
    n = math.floor(x + Fr(1, 2))
    return float(Fr(n if b >= 0 else -n, N)), float(abs(x - math.floor(x) - Fr(1, 2)))


def q_fp(b):  # the add's and the lookup's own arithmetic
    s = 1.0 if b >= 0 else -1.0
    return s * (math.floor(abs(b + s * STEP * 0.5) * 3843840.0) / 3843840.0)


def add_contract(st, p, b, length):
    ms = st["WarpMarkers"]
    if not st["IsWarped"]:
        return {"outcome": "refused", "refusal_reason": "not-warped"}, {}
    if not (0 <= p <= length):
        return {"outcome": "refused", "refusal_reason": "sample-time-out-of-range"}, {}
    vis = ms[:-1]
    i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
    left, right = ms[i - 1], (ms[i] if i < len(vis) else None)
    assert i > 0, "p below first marker is excluded"
    if b < left[1]:
        return {"outcome": "refused", "refusal_reason": "beat-below-left-neighbour"}, {}
    if right and b > right[1]:
        return {"outcome": "refused", "refusal_reason": "beat-above-right-neighbour"}, {}
    qb, tie = q_exact(b)
    info = {"tie_distance_steps": tie, "tempo_limit_distance_bpm": [], "neighbour_distance_s": []}
    for nb in [left] + ([right] if right else []):
        t = (Fr(qb) - Fr(nb[1])) / (Fr(p) - Fr(nb[0])) * 60
        info["tempo_limit_distance_bpm"].append(float(min(abs(t - 5), abs(t - 999))))
        info["neighbour_distance_s"].append(abs(p - nb[0]))
        if not 5 <= t <= 999:
            return {"outcome": "refused", "refusal_reason": "segment-tempo-out-of-range"}, info
    return {"outcome": "accepted"}, info


def add_evidence(st, p, b, length):  # procedure as the evidence shows it
    ms = st["WarpMarkers"]
    if not st["IsWarped"]:
        return {"outcome": "refused", "refusal_reason": "not-warped"}
    if p < 0 or p > length:
        return {"outcome": "refused", "refusal_reason": "sample-time-out-of-range"}
    prev_beat, left, right = 0.0, None, None
    for k, m in enumerate(ms):
        shadow = k == len(ms) - 1
        if p < m[0] or shadow:
            if k != 0 and b < prev_beat:
                return {"outcome": "refused", "refusal_reason": "beat-below-left-neighbour"}
            if not shadow and m[1] < b:
                return {"outcome": "refused", "refusal_reason": "beat-above-right-neighbour"}
            left = ms[k - 1] if k != 0 else None
            right = None if shadow else m
            break
        prev_beat = m[1]
    qb = q_fp(b)
    for nb in [x for x in (left, right) if x is not None]:
        ds = p - nb[0]
        a, c = (999.0 / 60.0) * ds + nb[1], (5.0 / 60.0) * ds + nb[1]
        lo, hi = (c, a) if c < a else (a, c)
        if lo > qb or hi < qb:
            return {"outcome": "refused", "refusal_reason": "segment-tempo-out-of-range"}
    return {"outcome": "accepted"}


def lookup(st, call, rounding):
    ms = st["WarpMarkers"]
    qb = rounding(call["beat"])
    if isinstance(qb, tuple):
        qb = qb[0]
    hit = None
    for k, (_, beat) in enumerate(ms):
        if beat == qb:
            hit = k
            break
        if beat > qb:
            break
    if hit is None:
        return {"outcome": "refused", "refusal_reason": "no-such-marker"}
    if hit == len(ms) - 1:
        return {"outcome": "refused", "refusal_reason": "shadow-marker"}
    return {"outcome": "accepted"} if call["function"] == "remove_warp_marker" else {"no-expectation": "move"}


def evaluate(c, length=3.0):
    try:
        key, st = open_doc(D / c["input"])
    except Refused:
        return {"outcome": "refused"}, {"outcome": "refused"}, {}
    call = c.get("call")
    if not call:
        want = c["expected"].get("state", {}).get(key, {})
        got = {"outcome": "opens", "state": {key: {k: st[k] for k in want}}}
        return got, got, {}
    f = call["function"]
    if f in ("sample_to_beat_time", "beat_to_sample_time"):
        r = {"outcome": "refused", "refusal_reason": "not-warped"} if not st["IsWarped"] else {"no-expectation": "value"}
        return r, r, {}
    if f == "add_warp_marker":
        a, info = add_contract(st, call["sample_time_seconds"], call["beat"], length)
        return a, add_evidence(st, call["sample_time_seconds"], call["beat"], length), info
    qb, tie = q_exact(call["beat"])
    return lookup(st, call, q_exact), lookup(st, call, q_fp), {"tie_distance_steps": tie}


cases = json.loads((D / "cases.json").read_text())["cases"]
bad = 0
for c in cases:
    a, b, info = evaluate(c)
    ok = json.dumps(a, sort_keys=True) == json.dumps(c["expected"], sort_keys=True) == json.dumps(b, sort_keys=True)
    bad += not ok
    print(c["id"], "agree" if ok else f"DIFFER contract={a} evidence={b} expected={c['expected']}",
          json.dumps(info) if info else "")
print("cases", len(cases), "disagreements", bad)
