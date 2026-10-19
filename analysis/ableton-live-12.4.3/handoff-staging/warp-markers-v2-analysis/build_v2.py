"""Stage the warp-markers-v2 candidate (analyst side): fixtures, cases and the draft manifest.

Run with CPython 3.13 and -I from any directory:
  python3 -I build_v2.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3 -I check_v2.py seal           # structure checks, model, X agreement, carry, manifest files[], reports
  python3 -I check_v2.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Every XML fixture is the base Live Set T11-MIN, made by the T1.1 generator make_fixture.py (imported
unchanged; its hash is checked against its run manifest), with the base clip's warp state set to the
warp-markers-v1 template and its sample reference pointed at the generated WAV, plus the one change
the case states. Cases 001-038 are copied verbatim from the released warp-markers-v1 cases.json;
039-064 are hand-authored here. README.md, AGENTS.md and spec.md are hand-written.
Inputs: make_fixture.py, handoff/warp-markers-v1/cases.json. Outputs: the stage directory only.
"""
import copy, io, json, os, sys, wave
from pathlib import Path

sys.dont_write_bytecode = True  # never write caches into the analysis directories
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "warp-markers-v2"
sys.path.insert(0, str(HERE))
from v2_meta import PROV_S, PROV_X, PROV_XS, T11, V1, manifest_meta, sha  # noqa: E402

T11DIR = ROOT / T11
_t11 = json.loads((T11DIR / "manifest.json").read_text())["files"]
assert sha((T11DIR / "make_fixture.py").read_bytes()) == _t11["make_fixture.py"]["sha256"], "make_fixture.py changed"
sys.path.insert(0, str(T11DIR))
import make_fixture as mf  # noqa: E402

TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
WAV_RATE, WAV_FRAMES = 8000, 24000  # 3.0 s; the warp-markers-v1 WAV, byte for byte
SAMPLE = "fixtures/sample.wav"
CLIP_PATH = ["LiveSet", "Tracks", "AudioTrack", "DeviceChain", "MainSequencer", "ClipSlotList", "ClipSlot",
             "ClipSlot", "Value", "AudioClip"]
CLIP_FIELDS = [("IsWarped", "true"), ("WarpMode", "4"), ("GranularityTones", "40"), ("GranularityTexture", "100"),
               ("FluctuationTexture", "50"), ("TransientResolution", "4"), ("TransientLoopMode", "1"),
               ("TransientEnvelope", "100"), ("ComplexProFormants", "75"), ("ComplexProEnvelope", "64")]
SEVEN = ("GranularityTones", "GranularityTexture", "FluctuationTexture", "TransientResolution",
         "TransientLoopMode", "ComplexProFormants", "ComplexProEnvelope")
M1 = [("10", "0", "0"), ("11", "1", "2"), ("12", "2", "3"), ("13", "2.015625", "3.03125")]
LATER = [("10", "0.5", "1"), *M1[1:]]                         # first marker later (draft list M2)
TWO = [("10", "0", "0"), ("11", "0.0112275449101796407", "0.03125")]  # two markers, 167 BPM (draft list M0)
SIXTEENTH = [*M1[:3], ("13", "2.03125", "3.0625")]            # shadow 1/16 beat after the last visible marker


def wav():
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(WAV_RATE), w.writeframes(b"\0\0" * WAV_FRAMES)
    return buf.getvalue()


WAV = wav()


def kid(node, tag):
    return next(k for k in node[2] if k[0] == tag)


def at(node, tags):
    for t in tags:
        node = kid(node, t)
    return node


def setv(node, tag, value):
    kid(node, tag)[1]["Value"] = str(value)


def markers(ms):
    return [mf.el("WarpMarker", {"Id": i, "SecTime": s, "BeatTime": b}) for i, s, b in ms]


def base_tree():
    """T11-MIN with its clip warped as the v1 template and its sample reference pointed at sample.wav."""
    root = mf.build(WAV)  # FileRef size and CRC are computed from these bytes by the generator
    clip = at(root, CLIP_PATH)
    sref = kid(clip, "SampleRef")
    fref = kid(sref, "FileRef")
    setv(fref, "RelativePath", "sample.wav")
    setv(fref, "Path", "/Fixtures/sample.wav")
    setv(sref, "DefaultDuration", WAV_FRAMES)
    setv(sref, "DefaultSampleRate", WAV_RATE)
    setv(clip, "IsWarped", "true")
    setv(clip, "WarpMode", "4")
    i = next(n for n, k in enumerate(clip[2]) if k[0] == "WarpMode")
    clip[2][i + 1:i + 1] = [mf.v(t, x) for t, x in CLIP_FIELDS[2:]]
    kid(clip, "WarpMarkers")[2][:] = markers(M1)
    # review RVW2-01 (device placement is open, Q-022): both device lists emptied, as the live-set-structure-v1
    # review did for T11-MIN; their targets 67 and 68 go with them, so NextPointeeId is 67 (largest target Id 66)
    for track in ("MidiTrack", "AudioTrack"):
        at(root, ["LiveSet", "Tracks", track, "DeviceChain", "DeviceChain", "Devices"])[2][:] = []
    setv(kid(root, "LiveSet"), "NextPointeeId", 67)
    return root


def clip_fx(put=None, drop=(), novalue=(), ms=None):
    def change(root):
        clip = at(root, CLIP_PATH)
        for t, x in (put or {}).items():
            setv(clip, t, x)
        clip[2][:] = [k for k in clip[2] if k[0] not in drop]
        for k in clip[2]:
            if k[0] in novalue:
                k[1].clear()
        if ms is not None:
            kid(clip, "WarpMarkers")[2][:] = markers(ms)
    return change


def second(attr, text):  # the three-marker list with one attribute of its second marker replaced
    i, s, b = M1[1]
    return [M1[0], (i, text, b) if attr == "SecTime" else (i, s, text), *M1[2:]]


def render(root):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    mf.render(root, 0, lines)
    return ("\n".join(lines) + "\n").encode("ascii")


def fixture(change=None):
    root = copy.deepcopy(BASE)
    if change:
        change(root)
    return render(root)


BASE = base_tree()
FIXTURES = {
    "base.xml": fixture(), "not-warped.xml": fixture(clip_fx({"IsWarped": "false"})),
    "sectime-exponent.xml": fixture(clip_fx(ms=second("SecTime", "1.0e0"))),
    "sectime-leading-space.xml": fixture(clip_fx(ms=second("SecTime", " 1"))),
    "beattime-off-grid.xml": fixture(clip_fx(ms=second("BeatTime", "2.0000001"))),
    "beattime-trailing-text.xml": fixture(clip_fx(ms=second("BeatTime", "2junk"))),
    "sectime-no-number.xml": fixture(clip_fx(ms=second("SecTime", "abc"))),
    "beattime-empty.xml": fixture(clip_fx(ms=second("BeatTime", ""))),
    "settings-absent.xml": fixture(clip_fx(drop=SEVEN)), "settings-no-value.xml": fixture(clip_fx(novalue=SEVEN)),
    "transient-resolution-0.xml": fixture(clip_fx({"TransientResolution": "0"})),
    "transient-loop-mode-0.xml": fixture(clip_fx({"TransientLoopMode": "0"})),
    **{f"warp-mode-{c}.xml": fixture(clip_fx({"WarpMode": str(c)})) for c in (0, 1, 2, 3, 6)},
    "first-marker-later.xml": fixture(clip_fx(ms=LATER)),
    "two-markers.xml": fixture(clip_fx(ms=TWO)),
    "shadow-sixteenth.xml": fixture(clip_fx(ms=SIXTEENTH)),
    "sample.wav": WAV,
}

# ---- new cases (hand-authored expectations; see traceability.json) ----
B, UW, LT, TW, SX = "base.xml", "not-warped.xml", "first-marker-later.xml", "two-markers.xml", "shadow-sixteenth.xml"
TEMPO, NOM = "segment-tempo-out-of-range", "no-such-marker"


def s2b(t):
    return {"function": "sample_to_beat_time", "sample_frames": t}


def b2s(b):
    return {"function": "beat_to_sample_time", "beat": b}


def add(p, q):
    return {"function": "add_warp_marker", "sample_time_seconds": p, "beat": q}


def rm(q, d=None):
    if d is None:
        return {"function": "remove_warp_marker", "beat": q}
    return {"function": "move_warp_marker", "beat": q, "distance": d}


def val(v):
    return {"outcome": "accepted", "value": v}


ACC = {"outcome": "accepted"}


def no(reason):
    return {"outcome": "refused", "refusal_reason": reason}


C8, C78, C15, C1516 = ["003", "008"], ["003", "007", "008"], ["015"], ["015", "016"]
# (number, kind, purpose, requirement suffixes, fixture, call or None for open, expected, provenance)
NEW = [
    (39, "boundary", "sample_to_beat_time(-4000): -0.5 s, before the first marker, so the first segment is extended",
     C8, B, s2b(-4000), val(-1.0), PROV_X),
    (40, "positive", "sample_to_beat_time(4000): 0.5 s, inside the first segment", C8, B, s2b(4000), val(1.0), PROV_X),
    (41, "positive", "sample_to_beat_time(8000): 1 s, at the second marker", C8, B, s2b(8000), val(2.0), PROV_X),
    (42, "positive", "sample_to_beat_time(12000): 1.5 s, inside the second segment", C8, B, s2b(12000), val(2.5),
     PROV_X),
    (43, "boundary", "sample_to_beat_time(16000): 2 s, at the last visible marker", C78, B, s2b(16000), val(3.0),
     PROV_X),
    (44, "boundary", "sample_to_beat_time(20000): 2.5 s, past the last visible marker, so the segment to the shadow "
     "marker is extended", C78, B, s2b(20000), val(4.0), PROV_X),
    (45, "boundary", "sample_to_beat_time(400000): 50 s, beyond the sample and every marker; the result is not "
     "limited", C78, B, s2b(400000), val(99.0), PROV_X),
    (46, "boundary", "sample_to_beat_time(0) with the first marker at 0.5 s and beat 1: before the first marker",
     C8, LT, s2b(0), val(0.0), PROV_X),
    (47, "boundary", "sample_to_beat_time(2000) with the first marker at 0.5 s and beat 1: 0.25 s, before the first "
     "marker", C8, LT, s2b(2000), val(0.5), PROV_X),
    (48, "positive", "beat_to_sample_time(0.5): inside the first segment", C8, B, b2s(0.5), val(2000.0), PROV_X),
    (49, "positive", "beat_to_sample_time(2.5): inside the second segment", C8, B, b2s(2.5), val(12000.0), PROV_X),
    (50, "boundary", "beat_to_sample_time(4): past the last visible marker, so the segment to the shadow marker is "
     "extended", C78, B, b2s(4), val(20000.0), PROV_X),
    (51, "boundary", "sample_to_beat_time(8000) on a list of two markers, the second 1/32 beat after the first at "
     "167 BPM: the only segment is the shadow segment", C78, TW, s2b(8000), val(2.783333333333333), PROV_XS),
    (52, "boundary", "Add at 1.5 s, beat 2.0416666666666665: equal to the lower beat bound toward the left "
     "neighbour (about 5 BPM)", C1516, B, add(1.5, 2.0416666666666665), ACC, PROV_X),
    (53, "boundary", "Add at 1.5 s, beat 2.0416664065101564: one grid step below that lower bound", C1516, B,
     add(1.5, 2.0416664065101564), no(TEMPO), PROV_XS),
    (54, "boundary", "Add at 2.5 s, beat 11.325: equal to the upper beat bound toward the left neighbour (about "
     "999 BPM); the next marker is the shadow marker, so there is no right bound", C1516, B, add(2.5, 11.325), ACC,
     PROV_XS),
    (55, "boundary", "Add at 2.5 s, beat 11.325000260156509: one grid step above that upper bound", C1516, B,
     add(2.5, 11.325000260156509), no(TEMPO), PROV_XS),
    (56, "boundary", "Remove beat 2.0000001300782553, the binary64 value nearest to the point halfway between beat 2 "
     "and the next grid point: it rounds up, and no marker has the result", C1516, B, rm(2.0000001300782553),
     no(NOM), PROV_X),
    (57, "boundary", "Remove beat 2.000000130078255, one binary64 step below the halfway point: grid rounding still "
     "rounds it up, and no marker has the result", C1516, B, rm(2.000000130078255), no(NOM), PROV_X),
    (58, "boundary", "Remove beat 2.0000001300782544, two binary64 steps below the halfway point: grid rounding "
     "gives 2, the second marker's beat", C1516, B, rm(2.0000001300782544), ACC, PROV_XS),
    (59, "boundary", "Add at 1 s, beat 2: the sample time equals the left neighbour's, both bounds toward it are its "
     "beat 2, and the beat equals it", C1516, B, add(1, 2), ACC, PROV_XS),
    (60, "boundary", "Add at 1 s, beat 2.5: the sample time equals the left neighbour's, so only beat 2 is within "
     "the bounds", C1516, B, add(1, 2.5), no(TEMPO), PROV_XS),
    (61, "boundary", "Add at 0.25 s, beat -1 with the first marker at 0.5 s: there is no left neighbour, so there is "
     "no left beat check and no left bound; tempo to the right neighbour 480 BPM", C15, LT, add(0.25, -1), ACC,
     PROV_S),
    (62, "negative", "Move beat 2.001, distance 1, on a clip that is not warped: refused because no marker matches, "
     "not because the clip is not warped", C1516, UW, rm(2.001, 1), no(NOM), PROV_S),
    (63, "boundary", "Remove beat 0 on a list of two markers: the first marker matches and is not the shadow marker",
     ["007", "015"], TW, rm(0), ACC, PROV_S),
    (64, "positive", "Shadow marker 1/16 beat after the last visible marker (3.0625 beats, 2.03125 s): held as "
     "stored", ["002", "003", "007"], SX, None,
     {"outcome": "opens", "state": {"AudioClip": {"WarpMarkers": [[0.0, 0.0], [1.0, 2.0], [2.0, 3.0],
                                                                  [2.03125, 3.0625]]}}}, PROV_S),
]


def cid(n):
    return f"WARP-MARKERS-{n:03d}"


def comparator(call, exp):
    if "value" in exp:
        unit = "1e-9 beat" if call["function"] == "sample_to_beat_time" else "1e-6 sample frame"
        return f"outcome exact; value within {unit}"
    if call:
        return "outcome exact; refusal_reason exact" if exp["outcome"] == "refused" else "outcome exact"
    return "outcome exact" if exp["outcome"] == "refused" else \
        "outcome exact; listed state keys exact (binary64 numbers; marker lists as whole ordered lists)"


def case_json(n, kind, purpose, reqs, fx, call, exp, prov):
    c = {"id": cid(n), "kind": kind, "purpose": purpose, "requirements": [f"REQ-WARP-MARKERS-{r}" for r in reqs],
         "input": f"fixtures/{fx}", "sample": SAMPLE, "action": "open-call" if call else "open"}
    if call:
        c["call"] = call
    return {**c, "expected": exp, "expectation_provenance": prov, "reference_execution": "not-run",
            "candidate_execution": "not-run", "comparator": comparator(call, exp)}


def v1_cases():
    return json.loads((ROOT / V1 / "cases.json").read_text())["cases"]


EXCLUSIONS = {
    "inputs_without_expectation": [
        "SecTime or BeatTime text starting, after spaces and a sign, with 0x, inf or nan; the text Invalid; text starting with #; leading whitespace other than U+0020; a missing SecTime or BeatTime; values outside -1,000,000 to 1,000,000",
        "marker Id values that are missing, repeated or not decimal integers; content inside WarpMarker; children of WarpMarkers other than WarpMarker",
        "audio clip marker lists with fewer than two markers or not strictly increasing in both positions",
        "code and setting text other than plain decimal digits; codes outside their lists; settings outside their ranges or not integers; IsWarped other than true or false; a missing IsWarped or WarpMode; a TransientEnvelope value other than 100 (every fixture carries 100; the held value is not judged)",
        "children of AudioClip other than those the fixtures carry, other child orders, repeated children",
        "any change to the fixtures' context: the document outside the clip's warp children and marker list, including the clip's sample reference, and the WAV file; any device in a device list (every device list of the fixtures is empty), including a Sampler or Simpler and its sample parts",
        "scripting arguments that are not finite or have magnitude 1,000,000 or more; a move on a list of fewer than three markers; a call that breaks more than one rule, except an add_warp_marker call, which the first failing check of REQ-015 clauses 1 to 5 decides",
        "any other envelope, format version, compressed container or document kind",
    ],
    "behavior": [
        "everything written on save (REQ-002, 003, 004, 007, 010 save clauses)",
        "an empty marker list, in an audio clip or a sample part (REQ-004); one-marker, out-of-order and equal-position lists (REQ-005); missing or Invalid positions (REQ-006)",
        "the value used, shown and saved for codes and settings outside their ranges (REQ-014); the TransientEnvelope range and default",
        "conversion results after any edit of the clip; conversions on clips that are not audio clips",
        "playback (REQ-009): which sample position plays at a given beat, whether a clip that is not warped uses its warp markers, arrangement clips; the audio output of every warp mode",
        "the default WarpMode of an audio clip and the default warp mode preference",
        "Sampler and Simpler sample parts: where they store warp state (REQ-001 clause 2), their marker lists (REQ-004), codes, settings and defaults; any device in a device list",
        "where and when the application creates or re-places the shadow marker, and the values it gives it; the marker list after an accepted add or remove; move limits and accepted moves; the scripting warp_mode setter; non-audio clips",
        "display of markers, codes, labels and settings; interactive edits, auto-warp, recording and undo",
        "any change the application makes by itself after reading the document, such as automatic warping or sample analysis; whether the original makes one on opening is not established",
        "the structure rules that decide whether a Live Set opens; how a document refers to and finds its sample",
        "refusal presentation and the state after a refusal; error text of scripting calls",
        "progress, cancellation and timing",
    ],
}
CHANGES = [
    "fixtures: every XML document rebuilt as a complete Live Set (the base set of spec.md, whose device lists are empty) with the warp-markers-v1 change of its case; 17 of the 18 v1 documents are refused by the target build's open-time structure check (a track with clip slots but no freeze slots); fixture names kept; the WAV is byte-identical",
    "case WARP-MARKERS-018 withdrawn, with REQ-001 clause 2 and REQ-004: its document needs a Simpler in a track's device list, and whether the target build accepts a device there is not established; simpler-empty-markers.xml removed",
    "cases 007 and 008 now isolate the number-text refusal: their v1 documents were also refused for their structure",
    "REQ-015 clause 5: the 5 to 999 BPM tempo rule replaced by the binary64 beat bounds per neighbour (same outcome within warp-markers-v1's scope); the bands near the limits and near a neighbour's sample time withdrawn; cases 052 to 055, 059 and 060",
    "REQ-016: grid rounding stated as its binary64 operation sequence (same outcome within warp-markers-v1's scope); the band near a rounding tie withdrawn; cases 056 to 058",
    "REQ-008: conversion values of sample_to_beat_time and beat_to_sample_time released for a call right after opening; cases 039 to 051 on two new documents",
    "REQ-007: the shadow segment extends the conversions; a shadow spacing other than 1/32 beat is kept on opening; case 064 on a new document",
    "REQ-015: an add below the first marker's sample time has no left neighbour (case 061); move, like remove, has no warped check (case 062); a remove on a list of two markers is accepted (case 063)",
    "REQ-009 stays unreleased, as in warp-markers-v1: no case of this release can observe playback",
    "provenance labels extracted execution and computed by extracted-execution rules added; stated assumptions extended to the sample rate, the marker list a conversion uses and the arm64 build; the carried records unchanged",
    "exclusions: conversion values, the add below the first marker, a remove on fewer than three markers and the three uncertainty bands no longer excluded; the fixtures' context, the structure rules, sample resolution, device lists and Sampler and Simpler sample parts newly excluded",
]


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    for name, data in FIXTURES.items():
        p = STAGE / "fixtures" / name
        p.write_bytes(data)
        if name.endswith(".wav"):
            os.utime(p, (mf.LASTMOD, mf.LASTMOD))  # the clip's LastModDate, as the generator does
    # review RVW2-01: WARP-MARKERS-018 (a Simpler sample part) is withdrawn; its ID stays unused
    cases = [c for c in v1_cases() if c["id"] != cid(18)] + [case_json(*c) for c in NEW]
    assert [c["id"] for c in cases] == [cid(n) for n in range(1, 65) if n != 18]
    doc = {"schema": "warp-markers-cases-v2", "target": TARGET,
           "scope": "warp-markers-v2 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
           "fixture_origin": "Independently authored complete Live Set documents built from one base set, and one generated silent WAV; no shipped file copied",
           "oracle_status": "Static-derived and extracted-execution expectations, labelled per case; neither the reference application nor a candidate executed",
           "representation": {
               "paths": "relative to /Ableton/LiveSet; the clip is the only AudioClip",
               "state": "values held after opening, by element name; WarpMarkers as [SecTime, BeatTime] pairs in list order",
               "call": "one scripting call after opening; arguments are binary64",
               "value": "accepted conversion calls only: the number returned",
               "refusal_reason": "open-call refused only; see spec.md",
               "note": "project comparison representation, not an API of the original application or a required design"},
           "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc, indent=1, ensure_ascii=True) + "\n")
    man = manifest_meta(len(cases), TARGET, EXCLUSIONS, CHANGES)
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    print(len(cases), "cases,", len(FIXTURES), "fixtures staged")


if __name__ == "__main__":
    {"build": build}[sys.argv[1]]()
