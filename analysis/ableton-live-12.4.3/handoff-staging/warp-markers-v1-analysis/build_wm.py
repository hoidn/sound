"""Stage the warp-markers-v1 release (analyst side). Reviewed 2026-10-18; review edits are marked "review:".

Run with CPython 3.11 and -I from any directory:
  python3.11 -I build_wm.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3.11 -I build_wm.py seal           # manifest files[], author-validation.json, traceability.json
  python3.11 -I build_wm.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Fixtures are authored here: minimal decoded Live Set documents from one template, and one generated
silent WAV. No shipped file is read for the payload. Expected results are the hand-authored static
derivations in CASES. seal cross-checks them against model(), an independent restatement of the
released clauses (it shares the static evidence and is not an oracle), runs a mutation self-check
and re-hashes the evidence. README.md, AGENTS.md and spec.md in the stage directory are hand-written.
"""
import hashlib, io, json, math, re, sys, wave
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # -I omits the script directory; wm_meta.py holds the analyst tables
sys.dont_write_bytecode = True
from wm_meta import ALLOWED_HITS, CLAUSES, DENY, E, I, TRACE, evidence_identity, manifest_meta  # noqa: E402
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "warp-markers-v1"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
PROV = "static-derived; not observed reference output"
ENVELOPE = '<Ableton MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1">'
CLIP_PATH = ["Tracks", 'AudioTrack Id="0"', "DeviceChain", "MainSequencer", "ClipSlotList", 'ClipSlot Id="0"',
             "ClipSlot", "Value", 'AudioClip Id="0" Time="0"']
SIMPLER_PATH = ["Tracks", 'MidiTrack Id="0"', "DeviceChain", "DeviceChain", "Devices", 'OriginalSimpler Id="0"',
                "Player", "MultiSampleMap", "SampleParts", 'MultiSamplePart Id="0"', "SampleWarpProperties"]
CLIP_FIELDS = [("IsWarped", "true"), ("WarpMode", "4"), ("GranularityTones", "40"), ("GranularityTexture", "100"),
               ("FluctuationTexture", "50"), ("TransientResolution", "4"), ("TransientLoopMode", "1"),
               ("TransientEnvelope", "100"), ("ComplexProFormants", "75"), ("ComplexProEnvelope", "64")]
SIMPLER_FIELDS = [("WarpMode", "0"), ("GranularityTones", "30"), ("GranularityTexture", "65"),
                  ("FluctuationTexture", "25"), ("ComplexProFormants", "100"), ("ComplexProEnvelope", "128"),
                  ("TransientResolution", "6"), ("TransientLoopMode", "2"), ("TransientEnvelope", "100"),
                  ("IsWarped", "false")]
SEVEN = ("GranularityTones", "GranularityTexture", "FluctuationTexture", "TransientResolution",
         "TransientLoopMode", "ComplexProFormants", "ComplexProEnvelope")
M1 = [("10", "0", "0"), ("11", "1", "2"), ("12", "2", "3"), ("13", "2.015625", "3.03125")]
SAMPLE = "fixtures/sample.wav"
WAV_RATE, WAV_FRAMES = 8000, 24000  # 3.0 s


def nest(path, inner):
    lines, depth = ['<?xml version="1.0" encoding="UTF-8"?>', ENVELOPE, "  <LiveSet>"], 2
    for p in path:
        lines.append("  " * depth + f"<{p}>")
        depth += 1
    lines += ["  " * depth + line for line in inner]
    for p in reversed(path):
        depth -= 1
        lines.append("  " * depth + f"</{p.split()[0]}>")
    return ("\n".join(lines + ["  </LiveSet>", "</Ableton>"]) + "\n").encode("ascii")


def markers_xml(ms):
    if not ms:
        return ["<WarpMarkers />"]
    return ["<WarpMarkers>"] + [f'  <WarpMarker Id="{i}" SecTime="{s}" BeatTime="{b}" />' for i, s, b in ms] \
        + ["</WarpMarkers>"]


def clip(put=None, drop=(), novalue=(), markers=M1):
    inner = [f"<{k} />" if k in novalue else f'<{k} Value="{(put or {}).get(k, v)}" />'
             for k, v in CLIP_FIELDS if k not in drop]
    return nest(CLIP_PATH, inner + markers_xml(markers))


def second(attr, text):  # list M1 with one attribute of its second marker replaced
    i, s, b = M1[1]
    return [M1[0], (i, text, b) if attr == "SecTime" else (i, s, text), *M1[2:]]


def wav():
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(WAV_RATE), w.writeframes(b"\0\0" * WAV_FRAMES)
    return buf.getvalue()


FIXTURES = {
    "base.xml": clip(), "not-warped.xml": clip({"IsWarped": "false"}),
    "sectime-exponent.xml": clip(markers=second("SecTime", "1.0e0")),
    "sectime-leading-space.xml": clip(markers=second("SecTime", " 1")),
    "beattime-off-grid.xml": clip(markers=second("BeatTime", "2.0000001")),
    "beattime-trailing-text.xml": clip(markers=second("BeatTime", "2junk")),
    "sectime-no-number.xml": clip(markers=second("SecTime", "abc")),
    "beattime-empty.xml": clip(markers=second("BeatTime", "")),
    "settings-absent.xml": clip(drop=SEVEN), "settings-no-value.xml": clip(novalue=SEVEN),
    "transient-resolution-0.xml": clip({"TransientResolution": "0"}),
    "transient-loop-mode-0.xml": clip({"TransientLoopMode": "0"}),
    **{f"warp-mode-{c}.xml": clip({"WarpMode": str(c)}) for c in (0, 1, 2, 3, 6)},
    "simpler-empty-markers.xml": nest(SIMPLER_PATH, markers_xml([]) + [f'<{k} Value="{v}" />' for k, v in SIMPLER_FIELDS]),
    "sample.wav": wav(),
}

# ---- hand-authored expectations (static derivations; see traceability) ----
M1S = [[0.0, 0.0], [1.0, 2.0], [2.0, 3.0], [2.015625, 3.03125]]
BASE = {"IsWarped": True, "WarpMode": 4, "GranularityTones": 40, "GranularityTexture": 100, "FluctuationTexture": 50,
        "TransientResolution": 4, "TransientLoopMode": 1, "ComplexProFormants": 75, "ComplexProEnvelope": 64,
        "WarpMarkers": M1S}
DEFAULTS = {"GranularityTones": 30, "GranularityTexture": 65, "FluctuationTexture": 25, "TransientResolution": 6,
            "TransientLoopMode": 2, "ComplexProFormants": 100, "ComplexProEnvelope": 128}
OPENS, REF, ACC = "opens", {"outcome": "refused"}, {"outcome": "accepted"}


def st(**clip_state):
    return {"outcome": OPENS, "state": {"AudioClip": clip_state}}


def no(reason):
    return {"outcome": "refused", "refusal_reason": reason}


def add(p, q):
    return {"function": "add_warp_marker", "sample_time_seconds": p, "beat": q}


def rm(q, d=None):  # remove_warp_marker(q), or move_warp_marker(q, d) when d is given
    if d is None:
        return {"function": "remove_warp_marker", "beat": q}
    return {"function": "move_warp_marker", "beat": q, "distance": d}


B, UW = "base.xml", "not-warped.xml"
NW, OOR, BL, BR, TEMPO, NOM, SH = ("not-warped", "sample-time-out-of-range", "beat-below-left-neighbour",
                                   "beat-above-right-neighbour", "segment-tempo-out-of-range", "no-such-marker",
                                   "shadow-marker")
# (number, kind, purpose, requirement suffixes, fixture, call or None for open, expected)
CASES = [
    (1, "positive", "Warped audio clip with three visible markers, a shadow marker, Complex mode and non-default settings",
     ["001", "002", "003", "011", "012", "013"], B, None, st(**BASE)),
    (2, "positive", "IsWarped false", ["001", "003"], UW, None, st(IsWarped=False, WarpMarkers=M1S)),
    (3, "boundary", 'Second marker SecTime "1.0e0"', ["002"], "sectime-exponent.xml", None, st(WarpMarkers=M1S)),
    (4, "boundary", 'Second marker SecTime " 1" (leading space)', ["002"], "sectime-leading-space.xml", None,
     st(WarpMarkers=M1S)),
    (5, "positive", 'Second marker BeatTime "2.0000001", which is not on the beat grid', ["002", "016"],
     "beattime-off-grid.xml", None, st(WarpMarkers=[M1S[0], [1.0, 2.0000001], *M1S[2:]])),
    (6, "boundary", 'Second marker BeatTime "2junk" (text after the number)', ["002"], "beattime-trailing-text.xml",
     None, st(WarpMarkers=M1S)),
    (7, "negative", 'Second marker SecTime "abc"', ["002"], "sectime-no-number.xml", None, REF),
    (8, "negative", 'Second marker BeatTime "" (empty)', ["002"], "beattime-empty.xml", None, REF),
    (9, "missing", "Seven setting elements absent; TransientEnvelope kept", ["010", "012", "013"],
     "settings-absent.xml", None, st(**DEFAULTS)),
    (10, "missing", "Seven setting elements present without a Value attribute", ["010", "012", "013"],
     "settings-no-value.xml", None, st(**DEFAULTS)),
    (11, "positive", "TransientResolution 0", ["012"], "transient-resolution-0.xml", None,
     st(TransientResolution=0)),
    (12, "positive", "TransientLoopMode 0", ["012"], "transient-loop-mode-0.xml", None, st(TransientLoopMode=0)),
    (13, "positive", "WarpMode 0 (Beats)", ["011"], "warp-mode-0.xml", None, st(WarpMode=0)),
    (14, "positive", "WarpMode 1 (Tones)", ["011"], "warp-mode-1.xml", None, st(WarpMode=1)),
    (15, "positive", "WarpMode 2 (Texture)", ["011"], "warp-mode-2.xml", None, st(WarpMode=2)),
    (16, "positive", "WarpMode 3 (Re-Pitch)", ["011"], "warp-mode-3.xml", None, st(WarpMode=3)),
    (17, "positive", "WarpMode 6 (Complex Pro)", ["011"], "warp-mode-6.xml", None, st(WarpMode=6)),
    (18, "positive", "Simpler sample part with an empty marker list", ["001", "004"], "simpler-empty-markers.xml",
     None, {"outcome": OPENS, "state": {"SampleWarpProperties": {"WarpMarkers": []}}}),
    (19, "negative", "sample_to_beat_time on a clip that is not warped", ["008"], UW,
     {"function": "sample_to_beat_time", "sample_frames": 0}, no(NW)),
    (20, "negative", "beat_to_sample_time on a clip that is not warped", ["008"], UW,
     {"function": "beat_to_sample_time", "beat": 0}, no(NW)),
    (21, "negative", "Add at 0.5 s, beat 1 on a clip that is not warped", ["015"], UW, add(0.5, 1), no(NW)),
    (22, "positive", "Add at 0.5 s, beat 1 (segment tempi 120 and 120 BPM)", ["015"], B, add(0.5, 1), ACC),
    (23, "negative", "Add at -0.1 s, beat 0 (before the sample start)", ["015"], B, add(-0.1, 0), no(OOR)),
    (24, "negative", "Add at 900,000 s, beat 100 (after the sample end)", ["015"], B, add(900000, 100), no(OOR)),  # review: RVW-04
    (25, "negative", "Add at 1.5 s, beat 1.9 (below the left neighbour's beat 2)", ["015"], B, add(1.5, 1.9), no(BL)),
    (26, "boundary", "Add at 1.5 s, beat 1.999999999: below the left neighbour's beat as given, equal to it after "
     "grid rounding", ["015", "016"], B, add(1.5, 1.999999999), no(BL)),
    (27, "negative", "Add at 1.5 s, beat 3.5 (above the right neighbour's beat 3)", ["015"], B, add(1.5, 3.5), no(BR)),
    (28, "negative", "Add at 1.5 s, beat 2.01 (tempo to the left neighbour about 1.2 BPM)", ["015", "016"], B,
     add(1.5, 2.01), no(TEMPO)),
    (29, "negative", "Add at 0.5 s, beat 1.99 (tempo to the right neighbour about 1.2 BPM)", ["015", "016"], B,
     add(0.5, 1.99), no(TEMPO)),
    (30, "negative", "Add at 0.001 s, beat 1 (tempo to the left neighbour 60,000 BPM)", ["015"], B, add(0.001, 1),
     no(TEMPO)),
    (31, "positive", "Add at 1.5 s, beat 2.5 (segment tempi 60 and 60 BPM)", ["015"], B, add(1.5, 2.5), ACC),
    (32, "boundary", "Add at 2.5 s, beat 4: after the last visible marker, so only the left limit applies (120 BPM)",
     ["007", "015"], B, add(2.5, 4), ACC),
    (33, "negative", "Remove the shadow marker (beat 3.03125)", ["007", "015"], B, rm(3.03125), no(SH)),
    (34, "negative", "Move the shadow marker (beat 3.03125, distance 1)", ["007", "015"], B, rm(3.03125, 1), no(SH)),
    (35, "boundary", "Remove beat 2.0000001, which grid rounding maps to the second marker's beat 2", ["015", "016"], B,
     rm(2.0000001), ACC),
    (36, "negative", "Remove beat 2.001, which matches no marker after grid rounding", ["015", "016"], B, rm(2.001),
     no(NOM)),
    (37, "negative", "Move beat 2.001, distance 1: no marker matches", ["015", "016"], B, rm(2.001, 1), no(NOM)),
    (38, "positive", "Remove beat 2 on a clip that is not warped", ["015"], UW, rm(2), ACC),
]


def cid(n):
    return f"WARP-MARKERS-{n:03d}"


def comparator(call, exp):
    if call:
        return "outcome exact; refusal_reason exact" if exp["outcome"] == "refused" else "outcome exact"
    return "outcome exact" if exp["outcome"] == "refused" else \
        "outcome exact; listed state keys exact (binary64 numbers; marker lists as whole ordered lists)"


def case_json(n, kind, purpose, reqs, fx, call, exp):
    c = {"id": cid(n), "kind": kind, "purpose": purpose, "requirements": [f"REQ-WARP-MARKERS-{r}" for r in reqs],
         "input": f"fixtures/{fx}", "sample": SAMPLE, "action": "open-call" if call else "open"}
    if call:
        c["call"] = call
    return {**c, "expected": exp, "expectation_provenance": PROV, "reference_execution": "not-run",
            "candidate_execution": "not-run", "comparator": comparator(call, exp)}


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    for name, data in FIXTURES.items():
        (STAGE / "fixtures" / name).write_bytes(data)
    cases = [case_json(*c) for c in CASES]
    doc = {"schema": "warp-markers-cases-v1", "target": TARGET,
           "scope": "warp-markers-v1 partial requirement clauses only (see spec.md)", "status": "released-reviewed",
           "fixture_origin": "Independently authored minimal documents and one generated silent WAV; no shipped file copied",
           "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
           "representation": {
               "paths": "relative to /Ableton/LiveSet; one AudioClip or one SampleWarpProperties per fixture",
               "state": "values held after opening, by element name; WarpMarkers as [SecTime, BeatTime] pairs in list order",
               "call": "one scripting call after opening; arguments are binary64",
               "refusal_reason": "open-call refused only; see spec.md",
               "note": "project comparison representation, not an API of the original application or a required design"},
           "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc, indent=1, ensure_ascii=True) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(len(cases), TARGET), indent=1) + "\n")
    print(len(cases), "cases,", len(FIXTURES), "fixtures staged")


# ---- cross-check model: the released clauses restated ----
class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


PREFIX = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
INIT = {"GranularityTones": 30, "GranularityTexture": 65, "FluctuationTexture": 25, "TransientResolution": 6,
        "TransientLoopMode": 2, "ComplexProFormants": 100, "ComplexProEnvelope": 128}
RANGES = {"GranularityTones": (12, 100), "GranularityTexture": (2, 263), "FluctuationTexture": (0, 100),
          "ComplexProFormants": (0, 100), "ComplexProEnvelope": (8, 256), "WarpMode": {0, 1, 2, 3, 4, 6},
          "TransientResolution": set(range(7)), "TransientLoopMode": {0, 1, 2}}


def position(text):
    t = text.lstrip(" ")
    if re.match(r"[+-]?(0[xX]|inf|nan|#|Invalid)", t, re.I) or t[:1] in ("\t", "\n", "\r"):
        raise NoExpectation(f"number form {text!r}")
    m = PREFIX.match(t)
    if not m:
        raise Refused()
    v = float(m.group(0))
    if abs(v) > 1e6:
        raise NoExpectation("position outside scope limit")
    return v


def value(tag, text):
    if tag == "IsWarped":
        return {"true": True, "false": False}[text]
    if not re.fullmatch(r"0|[1-9][0-9]*", text):
        raise NoExpectation(f"setting text {text!r}")
    v, r = int(text), RANGES.get(tag)
    if r is not None and (v not in r if isinstance(r, set) else not r[0] <= v <= r[1]):
        raise NoExpectation(f"{tag} outside its codes or range")
    return v


def load(data):
    ls = ET.fromstring(data).find("LiveSet")
    clip_el = ls.find("Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip")
    swp = ls.find("Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/SampleParts/"
                  "MultiSamplePart/SampleWarpProperties")
    holder, key = (clip_el, "AudioClip") if clip_el is not None else (swp, "SampleWarpProperties")
    state = dict(INIT)
    for el in holder:
        if el.tag == "WarpMarkers":
            state["WarpMarkers"] = [[position(m.attrib["SecTime"]), position(m.attrib["BeatTime"])] for m in el]
        elif el.tag != "TransientEnvelope" and "Value" in el.attrib:
            state[el.tag] = value(el.tag, el.attrib["Value"])
    ms = state["WarpMarkers"]
    if key == "AudioClip" and (len(ms) < 2 or any(a[0] >= b[0] or a[1] >= b[1] for a, b in zip(ms, ms[1:]))):
        raise NoExpectation("audio clip list not well formed")
    return key, state


def grid(b):  # nearest multiple of 1/3843840, halves away from zero, exact arithmetic
    x = Fraction(b) * 3843840
    n = math.floor(abs(x) + Fraction(1, 2))
    if abs(abs(x) - math.floor(abs(x)) - Fraction(1, 2)) < Fraction(1, 10 ** 3):  # review: RVW-03 band
        raise NoExpectation("beat near a rounding tie")
    return float(Fraction(n if x >= 0 else -n, 3843840))


def lookup_model(ms, call):
    if len(ms) < 3:
        raise NoExpectation("remove on fewer than three markers")
    q = grid(call["beat"])
    hit = next((i for i, (_, b) in enumerate(ms) if b == q), None)
    if hit is None:
        return no(NOM)
    if hit == len(ms) - 1:
        return no(SH)
    if call["function"] == "move_warp_marker":
        raise NoExpectation("accepted move")
    return ACC


def add_model(warped, ms, p, b, length):
    if not warped:
        return no(NW)
    if not 0 <= p <= length:
        return no(OOR)
    vis = ms[:-1]
    if p < vis[0][0]:
        raise NoExpectation("add before the first marker")
    i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
    left, right = ms[i - 1], (vis[i] if i < len(vis) else None)
    if b < left[1]:
        return no(BL)
    if right and b > right[1]:
        return no(BR)
    qb = grid(b)
    for nb in [left] + ([right] if right else []):
        if abs(Fraction(p) - Fraction(nb[0])) < Fraction(5, 10 ** 4):  # review: RVW-03 band
            raise NoExpectation("add near a neighbour's sample time")
        tempo = (qb - nb[1]) / (p - nb[0]) * 60
        if min(abs(tempo - 5), abs(tempo - 999)) < 1e-3:  # review: RVW-03 band
            raise NoExpectation("tempo at a limit")
        if not 5 <= tempo <= 999:
            return no(TEMPO)
    return ACC


def call_model(state, call, length=WAV_FRAMES / WAV_RATE):
    f = call["function"]
    if f in ("sample_to_beat_time", "beat_to_sample_time"):
        if not state["IsWarped"]:
            return no(NW)
        raise NoExpectation("conversion value")
    if f in ("remove_warp_marker", "move_warp_marker"):
        return lookup_model(state["WarpMarkers"], call)
    return add_model(state["IsWarped"], state["WarpMarkers"], call["sample_time_seconds"], call["beat"], length)


def model(case):
    try:
        key, state = load((STAGE / case["input"]).read_bytes())
    except Refused:
        return REF
    if "call" in case:
        return call_model(state, case["call"])
    want = case["expected"].get("state", {})
    return {"outcome": OPENS, "state": {k: {f: state[f] for f in v} for k, v in want.items() if k == key}}


def agrees(got, exp):  # JSON text equality keeps true/1 and 1/1.0 distinct
    return json.dumps(got, sort_keys=True) == json.dumps(exp, sort_keys=True)


def mutate(exp):
    m = json.loads(json.dumps(exp))
    if "state" in m:
        k = next(iter(m["state"]))
        f = next(iter(m["state"][k]))
        v = m["state"][k][f]
        m["state"][k][f] = (not v) if isinstance(v, bool) else (v + [[9.0, 9.0]] if isinstance(v, list) else v + 1)
    elif m["outcome"] == "refused" and "refusal_reason" in m:
        m["refusal_reason"] = OOR if m["refusal_reason"] != OOR else NW
    else:
        m = {"outcome": OPENS, "state": {}} if m["outcome"] == "refused" else no(NOM)
    return m


# ---- checks ----
def sha(b):
    return hashlib.sha256(b).hexdigest()


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
        ok_ = dest.is_file() and root.resolve() in dest.parents
        if ok_ and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok_ = anchor in slugs
        out.append((target, "ok" if ok_ else "UNRESOLVED"))
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
    missing = sorted({x for c in cases for x in (c["input"], c["sample"]) if not (d / x).is_file()})
    deny = {}
    for p in [*files, d / "manifest.json"]:
        if p.suffix == ".wav":
            continue
        text = p.read_text()
        hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad_links, "missing_case_inputs": missing, "deny_list_hits": deny,
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def fixture_report():
    rep = {}
    for name in FIXTURES:
        raw = (STAGE / "fixtures" / name).read_bytes()
        if name.endswith(".wav"):
            with wave.open(str(STAGE / "fixtures" / name)) as w:
                rep[name] = {"bytes": len(raw), "channels": w.getnchannels(), "sample_width": w.getsampwidth(),
                             "rate": w.getframerate(), "frames": w.getnframes(), "all_zero": set(raw[44:]) == {0}}
            continue
        root = ET.fromstring(raw)
        rep[name] = {"bytes": len(raw), "ascii": raw.isascii(), "lf_only": b"\r" not in raw, "tabs": b"\t" in raw,
                     "final_newline": raw.endswith(b"\n"), "root_attrs": root.attrib,
                     "holders": [e.tag for e in root.iter() if e.tag in ("AudioClip", "SampleWarpProperties")]}
    return rep


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    problems, undetected = {}, []
    for c in cases:
        try:
            got = model(c)
        except NoExpectation as e:
            got = {"no-expectation": str(e)}
        if not agrees(got, c["expected"]):
            problems[c["id"]] = f"model {got} != expected {c['expected']}"
        elif agrees(got, mutate(c["expected"])):
            undetected.append(c["id"])
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "warp-markers-v1 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "mutations_undetected": undetected, "fixtures": fixture_report(), "evidence_identity": evidence_identity(ROOT),
              **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model restates the "
                        "released clauses from the same static evidence and is not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    trace = {"schema": "warp-markers-traceability-v1", "spec": "SPEC-WARP-MARKERS r1", "evidence": E,
             "inferred_links": I,
             "clauses": {k: {"clause": c, "support": s, "evidence": ev, "inferred": inf}
                         for k, (c, s, ev, inf) in CLAUSES.items()},
             "cases": {cid(n): {"source": s, "evidence": ev, "inferred": inf} for n, (s, ev, inf) in TRACE.items()}}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    used = [x for row in [*trace["cases"].values(), *trace["clauses"].values()] for x in row["evidence"]]
    links_used = [x for row in [*trace["cases"].values(), *trace["clauses"].values()] for x in row["inferred"]]
    assert set(used) <= set(E) and set(links_used) <= set(I), (set(used) - set(E), set(links_used) - set(I))
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "mutations_undetected", "payload_files",
                                             "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
                                             "missing_case_inputs", "deny_list_hits", "manifest_sha256",
                                             "evidence_identity")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
