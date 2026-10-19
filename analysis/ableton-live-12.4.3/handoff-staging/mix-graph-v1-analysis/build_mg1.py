"""Stage the mix-graph-v1 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from any directory:
  python3 -I -B build_mg1.py build          # fixtures/, signals, cases.json, draft manifest.json (files[] empty)
  python3 -I -B build_mg1.py seal           # manifest files[], author-validation.json, traceability.json
  python3 -I -B build_mg1.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Inputs (read-only): SPEC-MIX-GRAPH r1 (wiki/specs/mix-graph.md) as narrowed in
wiki/specs/mix-graph-handoff-plan.md; the X results of r2/t14-mix-v1/results/mix.json (computation cases)
and r2/x2-mixer-v1/results/mixer.json (pan-law and fader gains used by the render cases); the T11-MIN
building blocks of r2/t11-structure-v1/make_fixture.py; the structure checker of that packet
(schema_check.py, fixture_audit.py) with the shipped schema 12.0_12402.txt.

Fixtures are built from the T11-MIN rules (make_fixture.py's element builders); no shipped file is read
into them. The two input signals are generated from integer formulas. Expected values of the
computation cases are copied from the X result files at build time; expected render coefficients are
composed from the X gains. seal cross-checks every case with model_*(), an independent restatement of
the released clauses (it shares the evidence and is not an oracle), runs the T11 structure checks on
every fixture, re-hashes the evidence, and scans the payload. README.md, AGENTS.md and spec.md are
hand-written.
"""
import hashlib, json, math, re, struct, sys, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "mix-graph-v1"
EVID = ROOT / "analysis/ableton-live-12.4.3"
T11 = EVID / "r2/t11-structure-v1"
T14 = EVID / "r2/t14-mix-v1"
X2M = EVID / "r2/x2-mixer-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
SCHEMA_SHA = "b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299"
X86_SHA = "1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0"
ARM_SHA = "3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
R = "REQ-MIX-GRAPH-"
sys.path.insert(0, str(T11))
import make_fixture as MF  # noqa: E402  (T11-MIN element builders)
import schema_check  # noqa: E402
import fixture_audit  # noqa: E402

PROV_X = "extracted execution: the original x86_64 code computed these values on these inputs; not an observed run of the application"
PROV_XS = ("extracted execution of the point and segment computations; the choice of segment is static-derived; "
           "not an observed run of the application")
PROV_S = "static-derived; not observed reference output"
PROV_R = ("composed render (spec conformance): composed from the rules of this contract and extracted-execution gains; "
          "not measured; no render of the original application exists")
CMP_C = "each listed number within the case tolerance (absolute); integers, Booleans and labels exact"
CMP_R = ("for every frame n of the input signals and both channels c, |y_c[n] - sum of coefficient x input[n]| <= "
         "tolerance_factor x X, where y is the main output and X the largest magnitude of any input sample of the case")
MIN, VMAX, FLOOR = "0.0003162277571", "1.99526238", 0.0003199999919
FRAMES, RATE, SPB = 64, 44100, 22050.0


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ---- input signals (generated; 16-bit PCM, two channels, 44,100 Hz) ----
def sig_a(n):
    return 1024 * ((n % 32) - 16), 2048 * abs((n % 16) - 8) - 8192


def sig_b(n):
    return (12000 if n % 8 < 4 else -12000), 512 * ((5 * n) % 64 - 32)


SIGNALS = {"A": ("fixtures/signals/x-a.wav", sig_a), "B": ("fixtures/signals/x-b.wav", sig_b)}


def write_wav(path, fn):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<hh", *fn(n)) for n in range(FRAMES)))


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (2, 2, RATE)
        raw = w.readframes(w.getnframes())
    pairs = struct.iter_unpack("<hh", raw)
    return [(a / 32768, b / 32768) for a, b in pairs]


# ---- fixtures: T11-MIN rules, two audio tracks A and B, one return R, no clips, no devices ----
def template():
    ids = MF.Ids()
    scenes = 2
    a_mix, _ = MF.mixer(ids, [(0, "true")])
    b_mix, _ = MF.mixer(ids, [(0, "true")])
    r_mix, _ = MF.mixer(ids, [(0, "false")])
    main_mix, main_t = MF.mixer(ids, [], main=True)
    pre_mix, _ = MF.mixer(ids, [])
    seq = lambda: MF.el("MainSequencer", None, MF.slots(None, scenes))  # noqa: E731
    tracks = MF.el("Tracks", None,
                   MF.track("AudioTrack", 1, "A", "A", 3, a_mix, [], seq(), [], scenes),
                   MF.track("AudioTrack", 2, "B", "B", 4, b_mix, [], seq(), [], scenes),
                   MF.track("ReturnTrack", 3, "R", "R", 55, r_mix, [], None, []))
    main = MF.el("MainTrack", None, MF.name("", "Main"), MF.v("Color", 69),
                 MF.el("AutomationEnvelopes", None, MF.el("Envelopes", None,
                       MF.envelope(0, main_t["TimeSignature"], [MF.el("EnumEvent", {"Id": "0", "Time": MF.L, "Value": "201"})]),
                       MF.envelope(1, main_t["Tempo"], [MF.el("FloatEvent", {"Id": "0", "Time": MF.L, "Value": "120"})]))),
                 MF.el("DeviceChain", None, MF.routing("AudioOutputRouting", "AudioOut/External/S0"), main_mix,
                       MF.el("DeviceChain", None, MF.el("Devices"))))
    prehear = MF.el("PreHearTrack", None, MF.el("DeviceChain", None, pre_mix))
    scene_els = [MF.el("Scene", {"Id": str(i)}, MF.follow_action(), MF.v("Name", f"Scene {i + 1}"), MF.v("Color", -1),
                       MF.v("Tempo", 120), MF.v("IsTempoEnabled", "false"), MF.v("TimeSignatureId", 201),
                       MF.v("IsTimeSignatureEnabled", "false")) for i in range(scenes)]
    liveset = MF.el("LiveSet", None, MF.v("NextPointeeId", ids.n + 1), tracks, main, prehear,
                    MF.el("SendsPre", None, MF.el("SendPreBool", {"Id": "0", "Value": "false"})),
                    MF.el("Scenes", None, *scene_els),
                    MF.el("Transport", None, MF.v("LoopOn", "false"), MF.v("LoopStart", 0), MF.v("LoopLength", 8),
                          MF.v("CurrentTime", 0)),
                    MF.v("GlobalQuantisation", 4), MF.v("AutoQuantisation", 0), MF.v("CrossfadeCurve", 2))
    return MF.el("Ableton", {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1"}, liveset)


def kid(node, tag):
    hits = [k for k in node[2] if k[0] == tag]
    assert len(hits) == 1, (node[0], tag, len(hits))
    return hits[0]


def track_node(root, key):
    ls = kid(root, "LiveSet")
    if key == "M":
        return kid(ls, "MainTrack")
    tid = {"A": "1", "B": "2", "R": "3"}[key]
    return [t for t in kid(ls, "Tracks")[2] if t[1].get("Id") == tid][0]


PATHS = {"Volume": ("Volume", "Manual"), "Pan": ("Pan", "Manual"), "SplitStereoPanL": ("SplitStereoPanL", "Manual"),
         "SplitStereoPanR": ("SplitStereoPanR", "Manual"), "Speaker": ("Speaker", "Manual"), "PanMode": ("PanMode",),
         "SoloSink": ("SoloSink",), "CrossFadeState": ("CrossFadeState", "Manual"),
         "Send": ("Sends", "TrackSendHolder", "Send", "Manual"), "EnabledByUser": ("Sends", "TrackSendHolder", "EnabledByUser")}


def doc(changes=None):
    """Template XML bytes with {(track key, value name): text} changes applied."""
    root = template()
    for (key, name), text in (changes or {}).items():
        node = kid(kid(track_node(root, key), "DeviceChain"), "Mixer")
        for tag in PATHS[name]:
            node = kid(node, tag)
        assert "Value" in node[1]
        node[1]["Value"] = text
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    MF.render(root, 0, lines)
    return ("\n".join(lines) + "\n").encode("utf-8")


# ---- expected values from the X result files ----
MIX = json.loads((T14 / "results/mix.json").read_text())
MIXER = json.loads((X2M / "results/mixer.json").read_text())
SENDS = {c["case"]: c for c in MIX["sends"]}
PAN = {(p["w"], p["pan"], p.get("splitL"), p.get("splitR"), p["vol"]): p["gains_LL_LR_RL_RR"] for p in MIXER["pan_law"]}
ROUND = {(r["curve"], r["stored_gain"]): r["gain_back_x"] for r in MIXER["fader"]["roundtrip_Q019"]}
CATS = ["unaffected", "soloed", "following", "muted", "indirectly-muted", "return-solo-muted", "cue"]


def send_eval(name):
    c = SENDS[name]
    i = c["in"]
    assert i[8] == 1.0 and i[9:13] == [1.0, 0.0, 0.0, 1.0], name  # outside any group: group switch on, identity
    return {"arguments": {"gain": i[3], "send_gate": i[0], "active": i[1], "post": i[2], "pan_matrix": i[4:8]},
            "expected": {"matrix": c["out_LL_LR_RL_RR"]}}


def computation_cases():
    sw = MIX["solo"]["switch_word"]
    gates = [{"arguments": {"solo_category": CATS[r["solo_type"]], "track_switch": bool(r["speaker"])},
              "expected": {"main_gate": r["MainOn"], "send_gate": r["SendsOn"]}} for r in sw if r["solo_type"] <= 6]
    ramps = MIX["ramp_interpolator"]
    vp = MIX["volume_panner"]
    auto = MIX["automation"]
    e9 = auto["E9_polyline"]
    seg = lambda st: {"matrix_target": [o["target"] for o in st["outputs"]], "length": st["outputs"][0]["length"]}  # noqa: E731
    assert all(o["length"] == st["outputs"][0]["length"] for st in vp for o in st["outputs"])
    L = -63072000
    return [
        ("MG-001", ["005"], "Send matrix, post-fader", "send-matrix", [send_eval("post, defaults for 8..12")], 1e-6, PROV_X),
        ("MG-002", ["005"], "Send matrix, pre-fader: no pan law and no volume", "send-matrix",
         [send_eval("pre, defaults for 8..12")], 1e-6, PROV_X),
        ("MG-003", ["005"], "Send matrix halfway through a pre/post fade", "send-matrix",
         [send_eval("IsPost 0.5 (mid-ramp)")], 1e-6, PROV_X),
        ("MG-004", ["005", "007"], "Send matrix with the send gate off; with the send inactive; with send gain 0",
         "send-matrix", [send_eval("SendsOn 0"), send_eval("not connected"), send_eval("send level 0")], 1e-6, PROV_X),
        ("MG-005", ["004", "005"], "Send gain 1 with the pan-law matrix of pan -0.5 at volume gain 0.5, post-fader, then pre-fader",
         "send-matrix", [send_eval("post, send 1, pan-law matrix of pan -0.5 vol 0.5"), send_eval("pre, send 1, same matrix")],
         1e-6, PROV_X),
        ("MG-006", ["004"], "Main matrix with the main gate 1, 0 and 0.5", "main-matrix",
         [{"arguments": {"main_gate": s["MainOn"], "pan_matrix": s["matrix_in"]}, "expected": {"matrix": s["out"]}}
          for s in MIX["main_switch"]], 1e-6, PROV_X),
        ("MG-007", ["007", "008"], "Main and send gates for each solo category with the track switch on and off", "gates",
         gates, 0, PROV_X),
        ("MG-009", ["010"], "Switch fade length with default settings", "fade-length",
         [{"arguments": {}, "expected": {"samples": MIX["solo"]["track_fade_time"]["samples"]}}], 0, PROV_X),
        ("MG-010", ["009"], "Gain ramp from 0 to 1 over 4 samples, advanced one sample at a time", "ramp-advance",
         [{"arguments": {"start": 0.0, "target": 1.0, "length": 4, "advances": 5},
           "expected": {"values": [s["value"] for s in ramps[0]["states"]]}}], 1e-6, PROV_X),
        ("MG-011", ["009"], "A ramp whose per-sample step is below 1e-12 takes its target at once; a value below 1e-12 counts as 0",
         "ramp-start",
         [{"arguments": {"start": 0.0, "target": f32(1e-9), "length": 10000}, "expected": {"value": ramps[2]["state"]["value"]}},
          {"arguments": {"start": 0.0, "target": f32(5e-13), "length": 0}, "expected": {"value": ramps[3]["GetRamp_target"]}}],
         1e-15, PROV_X),
        ("MG-012", ["004", "009"], "Pan-law matrix ramps while a volume ramp and a shorter pan ramp overlap", "pan-ramp",
         [{"arguments": {"initial": {"split_amount": 0.0, "pan": 0.0, "split_l": -1.0, "split_r": 1.0, "volume_gain": 1.0},
                         "changes": [{"sample": 0, "input": "volume_gain", "target": 0.5, "length": 100},
                                     {"sample": 20, "input": "pan", "target": -1.0, "length": 50}]},
           "expected": {"after_changes": [seg(vp[1]), seg(vp[2])]}}], 1e-6, PROV_X),
        ("MG-031", ["013"], "The 15 interior points of a curved segment", "polyline",
         [{"arguments": {"start": [0.0, -1.0], "end": [4.0, 1.0], "controls": [0.5, 0.0, 0.5, 0.0]},
           "expected": {"points": [list(p) for p in e9["points"][1:16]]}}], 1e-6, PROV_X),
        ("MG-032v", ["013"], "Playback value on a curved segment at envelope times 1, 2 and 3", "playback-value",
         [{"arguments": {"events": [[L, -1.0], [0.0, -1.0, [0.5, 0.0, 0.5, 0.0]], [4.0, 1.0]], "samples_per_beat": SPB,
                         "times": [1.0, 2.0, 3.0]}, "expected": {"values": [p["value"] for p in e9["played"]]}}], 1e-6, PROV_XS),
        ("MG-033v", ["013"], "Playback value of the ramp from a leading event whose value differs, at envelope time 0",
         "playback-value",
         [{"arguments": {"events": [[L, 1.0], [4.0, 0.0]], "samples_per_beat": SPB, "times": [0.0]},
           "expected": {"values": [auto["E13_t0"]["played_from_minus_1e7"]["value"]]}}], 1e-12, PROV_XS),
        ("MG-034v", ["013"], "Playback value on a linear segment at envelope times 5, 6 and 7", "playback-value",
         [{"arguments": {"events": [[L, 0.0], [4.0, 0.0], [8.0, 1.0]], "samples_per_beat": SPB, "times": [5.0, 6.0, 7.0]},
           "expected": {"values": [p["value"] for p in auto["E1_linear"]]}}], 1e-6, PROV_XS),
        ("NEW-DISCRETE", ["013"], "Bool and Enum envelopes take the value of the last point at or before the time; at two points with one time the later applies",
         "discrete-value",
         [{"arguments": {"events": [[L, True], [4.0, False], [8.0, True]], "times": [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]},
           "expected": {"values": [True, True, False, False, True, True]}},
          {"arguments": {"events": [[L, 0], [4.0, 1], [4.0, 2], [8.0, 0]], "times": [2.0, 4.0, 6.0, 8.0]},
           "expected": {"values": [0, 2, 2, 0]}}], 0, PROV_S),
        ("NEW-RAMPLEN", ["014"], "Ramp length of an automated value for four segments and a stopped transport",
         "ramp-length",
         [{"arguments": {"step": 0.002, "segment": s, "samples_per_beat": SPB, "transport": t}, "expected": {"length": n}}
          for s, t, n in (([4.0, 0.0, 8.0, 1.0], "playing", 200), ([0.0, 0.0, 64.0, 1.0], "playing", 2822),
                          ([0.0, 0.0, 1000.0, 0.25], "playing", 65536), ([0.0, 0.5, 4.0, 0.5], "playing", 0),
                          ([4.0, 0.0, 8.0, 1.0], "stopped", 0))], 0, PROV_S),
    ]


def coeffs(**k):
    """main L and R as {input channel: coefficient}; missing entries are 0."""
    return {"L": {c: v for c, v in k.items() if c.endswith("_L")}, "R": {c: v for c, v in k.items() if c.endswith("_R")}}


def render_cases():
    vmax = ROUND[("volume", f32(float(VMAX)))]
    m6 = ROUND[("volume", f32(0.5011872053))]
    pan_m1 = PAN[(0.0, -1.0, -1.0, 1.0, 1.0)]
    split0 = PAN[(1.0, 0.0, 0.0, 0.0, 1.0)]
    assert PAN[(0.0, 0.0, -1.0, 1.0, 1.0)] == [1.0, 0.0, 0.0, 1.0]  # Stereo, centre: identity
    one = coeffs(A_L=1.0, A_R=1.0)
    nil = coeffs()
    S = "0.5011872053"
    return [
        ("NEW-BASE", ["001", "002", "003", "005", "006", "011"], "Template: track A at 0 dB, every send at its minimum",
         {}, ["A"], one),
        ("MG-029a", ["003", "006", "011"], "Track A volume at the stored maximum 1.99526238 (+6 dB)", {("A", "Volume"): VMAX}, ["A"],
         coeffs(A_L=vmax, A_R=vmax)),
        ("MG-029b", ["003", "006", "011"], "Track A volume at the stored minimum 0.0003162277571: silent", {("A", "Volume"): MIN},
         ["A"], nil),
        ("NEW-FLOOR-BELOW", ["003", "011"], "Track A volume 0.000319, below the silence limit: silent", {("A", "Volume"): "0.000319"},
         ["A"], nil),
        ("NEW-FLOOR-ABOVE", ["003", "011"], "Track A volume 0.00033, above the silence limit: audible", {("A", "Volume"): "0.00033"},
         ["A"], coeffs(A_L=f32(0.00033), A_R=f32(0.00033))),
        ("MG-030m", ["003", "006", "011"], "Main track volume 0.5011872053 (-6 dB)", {("M", "Volume"): S}, ["A"],
         coeffs(A_L=m6, A_R=m6)),
        ("MG-022m", ["004", "011"], "Track A pan -1 in Stereo mode", {("A", "Pan"): "-1"}, ["A"],
         coeffs(A_L=pan_m1[0], A_R=pan_m1[3])),
        ("NEW-SPLIT", ["004", "011"], "Track A in Split Stereo mode with both split pans at 0", {("A", "PanMode"): "1",
         ("A", "SplitStereoPanL"): "0", ("A", "SplitStereoPanR"): "0"}, ["A"],
         {"L": {"A_L": split0[0], "A_R": split0[2]}, "R": {"A_L": split0[1], "A_R": split0[3]}}),
        ("NEW-SUM", ["002", "003", "006", "011"], "Tracks A and B both reach the main track; B at volume 0.5011872053",
         {("B", "Volume"): S}, ["A", "B"], coeffs(A_L=1.0, A_R=1.0, B_L=m6, B_R=m6)),
        ("MG-023", ["005", "007", "011"], "Track A switched off with its send at 0.5011872053: nothing reaches the main track",
         {("A", "Send"): S, ("A", "Speaker"): "false"}, ["A"], nil),
        ("NEW-RETURN-OFF", ["005", "006", "007", "011"], "Return R switched off while track A sends 0.5011872053 to it: only A's main output remains",
         {("A", "Send"): S, ("R", "Speaker"): "false"}, ["A"], one),
    ]


def cid(n):
    return f"MIX-GRAPH-{n:03d}"


def all_cases():
    out = []
    for src, reqs, purpose, comp, evals, tol, prov in computation_cases():
        out.append({"src": src, "case": {
            "kind": "computation", "purpose": purpose, "requirements": [R + r for r in reqs], "input": None,
            "action": "compute", "computation": comp, "evaluations": evals, "tolerance": tol,
            "expectation_provenance": prov, "reference_execution": "not-run", "candidate_execution": "not-run",
            "comparator": CMP_C}})
    for src, reqs, purpose, changes, sigs, main in render_cases():
        out.append({"src": src, "changes": changes, "case": {
            "kind": "render", "purpose": purpose, "requirements": [R + r for r in reqs], "input": None,
            "action": "render",
            "render": {"sample_rate": RATE, "frames": FRAMES, "transport": "playing from beat 0",
                       "signals": {k: SIGNALS[k][0] for k in sigs}},
            "expected": {"main": {ch: {k.replace("_", "."): v for k, v in d.items()} for ch, d in main.items()}},
            "tolerance_factor": 1e-5, "expectation_provenance": PROV_R, "reference_execution": "not-run",
            "candidate_execution": "not-run", "comparator": CMP_R}})
    for n, c in enumerate(out, 1):
        c["case"] = {"id": cid(n), **c["case"]}
        if c["case"]["kind"] == "render":
            c["case"]["input"] = f"fixtures/{cid(n)}.xml"
    return out


# ---- packaging ----
def sha(b):
    return hashlib.sha256(b).hexdigest()


UNRELEASED = [R + "012", R + "015", R + "016"]


def manifest_meta(n_cases):
    return {
        "schema": "handoff-manifest-v1", "release_id": "mix-graph-v1", "release_status": "candidate-unreviewed",
        "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-MIX-GRAPH", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-AUDIO", "FEAT-AUTOMATION"],
        "partial_requirement_scopes": {
            R + "001": "One mixer stage per audio, MIDI and return track and the main track; source, devices in order, mixer stage; one main and one send output per return; send k and the k-th SendPreBool belong to the k-th return in list order; tracks output to the main track; render output is the main track's main output",
            R + "002": "Main output M_main x and send outputs M_k x per sample; no other gain between device chain and mixer stage; return and main inputs are sums",
            R + "003": "Crossfade assignment None and no automation: volume gain equals the stored gain from 0.0003162277571 to 1.99526238, zero at or below 0.0003199999919; main track the same",
            R + "004": "Main matrix is the main gate times the pan-law matrix; the pan law; split amount is the stored PanMode code and ramps over the fade length",
            R + "005": "Send matrix g e a (q P + (1 - q) I) for a track outside any group; pre and post consequences; q from SendPreBool; a send at its stored minimum contributes nothing; send output to the k-th return",
            R + "006": "Destination inputs are per-sample sums; send sums in binary64 then binary32; main outputs binary32; return mixer shapes its output; main has no sends and its main output is the render output",
            R + "007": "With no track soloed, track switch off sets both gates to 0, on sets them to 1; changes ramp over the fade length",
            R + "008": "Main and send gates for each solo category and the track switch; no soloed track when no mixer stores SoloSink true; category assignment not released",
            R + "009": "Per-sample gains; ramp rules (linear, immediate below 1e-12 per sample, binary32 step); main entries move from the first sample, send entries one sample later; pan-law entries ramp to the value at the end of the shortest input ramp; values below 1e-12 count as 0",
            R + "010": "Fade length 75 samples at every sample rate for the gates, the post amount and the split amount; unchanged values give no ramp after the start",
            R + "011": "Render convention: a render starts from the settled state of the opened set (project convention, not original behavior)",
            R + "013": "Playback value of an envelope as a computation: point list with the first time at -10,000,000 beats, 16-piece curved segments, lookup at envelope time with the later of two equal times, segment value in samples, hold, Bool and Enum without interpolation; envelope time, drive and units not released",
            R + "014": "Ramp length of an automated value: max(200, min(65536, trunc(q / |slope|))) while playing, none for a flat segment or a stopped transport; last ramp shortened, new segment at each point; q is one thousandth of the range under the assumed default settings (0.002 for pan); only q / |slope| below 2^31",
        },
        "unreleased_requirements": UNRELEASED,
        "compatibility_dimensions": {
            "audio": "render cases: composed expectations (spec conformance, not measured compatibility); computation cases: extracted execution and static-derived values; reference execution not-run and no render of the original exists",
            "timing": "per-sample ramp and fade lengths as computations; real-time scheduling and latency excluded",
            "behavior": "solo category assignment, automation drive, editing and manual changes excluded",
            "project-files": "mixer values are read from the fixtures as stated; file reading itself is not graded",
            "file-format-written": "excluded",
            "ui-text": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "group tracks and tracks inside a group; audio, MIDI or return tracks whose output is not AudioOut/Main; input monitoring; a non-zero TrackDelay; frozen tracks",
                "racks; devices that report latency; in render cases any device or clip",
                "more than 12 return tracks; send holders or SendPreBool items not exactly one per return track; render sets with other than one return track",
                "crossfade assignment A or B (CrossFadeState other than 1) on any track; a main track with its track switch off",
                "any mixer storing SoloSink true; solo of the main or cue track",
                "a send stored above its minimum 0.0003162277571 whose output can reach the main track (its track's send gate on and the return playing); sends with EnabledByUser false above their minimum",
                "stored volumes outside 0.0003162277571 to 1.99526238, sends outside 0.0003162277571 to 1, pans and split pans outside -1 to 1, PanMode other than 0 and 1",
                "automation envelopes that drive a mixer or device parameter during a render case; clip envelopes",
                "ramp-length inputs whose step divided by the absolute slope is 2^31 or more",
            ],
            "behavior": [
                "which envelope drives a parameter and when, the mapping from song position to envelope time, and automated against manual values (REQ-MIX-GRAPH-012, 016)",
                "the units of automated values, including volume and send automation (REQ-MIX-GRAPH-015)",
                "the send gain of sends stored above their minimum; which sends are active",
                "which solo category a track is in when a Live Set stores a solo; the cue output",
                "the crossfade factor and the ramp of a crossfade-assignment change",
                "clip playback, instruments and device processing",
                "recording, editing, undo, manual changes during a render, automation override and re-enable",
                "real-time scheduling, latency, the audio-device stage after the main track, and what the original does in the first samples after a set is opened",
                "a non-default fade-length setting; the order of the main-bus sum",
            ],
        },
        "fixture_origin": "independently authored minimal Live Set documents built for this release on the project's minimal-set rules, and two generated 16-bit test signals; no shipped file content, audio or program code",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": n_cases,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    fx = STAGE / "fixtures"
    (fx / "signals").mkdir(parents=True, exist_ok=True)
    for old in [*fx.glob("*.xml"), *(fx / "signals").glob("*")]:
        old.unlink()
    for rel, fn in SIGNALS.values():
        write_wav(STAGE / rel, fn)
    cases = []
    for c in all_cases():
        if c["case"]["kind"] == "render":
            (STAGE / c["case"]["input"]).write_bytes(doc(c["changes"]))
        cases.append(c["case"])
    doc_ = {"schema": "mix-graph-cases-v1", "target": TARGET,
            "scope": "mix-graph-v1 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
            "fixture_origin": "Independently authored minimal Live Set documents and generated test signals; no shipped file copied or excerpted",
            "oracle_status": "Computation cases: extracted execution or static-derived; render cases: composed (spec conformance, not measured); neither reference nor candidate executed",
            "representation": {
                "computation": "computation name, evaluations of arguments -> expected result (see spec.md)",
                "render": "fixture Live Set, input signals placed at the named tracks' mixer-stage inputs, expected main output as coefficients of the input channels",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(len(cases)), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- cross-check model: an independent restatement of the released clauses ----
class Excluded(Exception):
    pass


def model_pan(w, p, sl, sr, v):
    th = lambda u: (u + 1) * math.pi / 4  # noqa: E731
    ll = v * (w * math.cos(th(sl)) + (1 - w) * max(1e-5, math.sqrt(2) * math.cos(th(p))))
    lr = v * w * math.sin(th(sl))
    rl = v * w * math.cos(th(sr))
    rr = v * (w * math.sin(th(sr)) + (1 - w) * max(1e-5, math.sqrt(2) * math.sin(th(p))))
    return [f32(x) for x in (ll, lr, rl, rr)]


def model_points(t0, v0, t1, v1, c):
    dt, dv = t1 - t0, v1 - v0
    px = (t0, t0 + c[0] * dt, t0 + c[2] * dt, t1)
    py = (v0, v0 + c[1] * dv, v0 + c[3] * dv, v1)
    out = []
    for i in range(1, 16):
        s = i / 16
        b = ((1 - s) ** 3, 3 * (1 - s) ** 2 * s, 3 * (1 - s) * s * s, s ** 3)
        out.append([sum(bi * x for bi, x in zip(b, px)), f32(sum(bi * y for bi, y in zip(b, py)))])
    return out


def model_point_list(events):
    pts = []
    for i, e in enumerate(events):
        t = -1e7 if i == 0 else float(e[0])
        pts.append((t, f32(float(e[1]))))
        if len(e) > 2 and any(x != 0.5 for x in e[2]) and i + 1 < len(events):
            pts += [tuple(p) for p in model_points(t, f32(float(e[1])), float(events[i + 1][0]), f32(float(events[i + 1][1])), e[2])]
    return pts


def grid(t):
    return math.copysign(math.floor(abs(t) * 3843840 + 0.5) / 3843840, t)


def model_playback(events, spb, t):
    pts = model_point_list(events)
    t = grid(t)
    k = max(i for i, p in enumerate(pts) if p[0] <= t)
    if k + 1 >= len(pts):
        return pts[k][1]
    (ta, va), (tb, vb) = pts[k], pts[k + 1]
    if va == vb:
        return va
    slope = f32(vb - va) / ((tb - ta) * spb)
    val = va + max(0.0, (t - ta) * spb) * slope
    return min(max(val, min(va, vb)), max(va, vb))


def model_discrete(events, t):
    times = [-1e7] + [float(e[0]) for e in events[1:]]
    return events[max(i for i, x in enumerate(times) if x <= grid(t))][1]


def model_ramp_length(step, seg, spb, transport):
    ta, va, tb, vb = seg
    slope = f32(f32(vb) - f32(va)) / ((tb - ta) * spb)
    if slope == 0 or transport != "playing":
        return 0
    r = step / abs(slope)
    if r >= 2 ** 31:
        raise Excluded("step / |slope| >= 2^31")
    return max(200, min(65536, math.trunc(r)))


def model_ramp(start, target, n, advances):
    d = f32((target - start) / n)
    vals, cur = [], start
    for k in range(1, advances + 1):
        cur = target if k >= n else f32(cur + d)
        vals.append(cur)
    return vals


def model_ramp_start(start, target, n):
    if abs(target) < 1e-12:
        return 0.0
    if n == 0 or abs((target - start) / n) < 1e-12:
        return target
    return start


CAT_GATES = {"unaffected": ("s", "s"), "following": ("s", "s"), "cue": ("s", "s"), "soloed": (1, 1), "muted": (0, 0),
             "indirectly-muted": ("s", 0), "return-solo-muted": (0, "s")}


def model_computation(comp, a):
    if comp == "send-matrix":
        p, q = a["pan_matrix"], a["post"]
        k = a["gain"] * a["send_gate"] * a["active"]
        return {"matrix": [k * (q * p[i] + (1 - q) * (1.0 if i in (0, 3) else 0.0)) for i in range(4)]}
    if comp == "main-matrix":
        return {"matrix": [a["main_gate"] * x for x in a["pan_matrix"]]}
    if comp == "gates":
        s = int(a["track_switch"])
        m, e = CAT_GATES[a["solo_category"]]
        return {"main_gate": s if m == "s" else m, "send_gate": s if e == "s" else e}
    if comp == "fade-length":
        return {"samples": 75}
    if comp == "ramp-advance":
        return {"values": model_ramp(a["start"], a["target"], a["length"], a["advances"])}
    if comp == "ramp-start":
        return {"value": model_ramp_start(a["start"], a["target"], a["length"])}
    if comp == "pan-ramp":
        cur = dict(a["initial"])
        ramps = {}  # input -> (start sample, start value, target, length)
        out = []
        names = ("split_amount", "pan", "split_l", "split_r", "volume_gain")
        for ch in a["changes"]:
            now = ch["sample"]
            for k, (s0, v0, tg, n) in list(ramps.items()):  # advance running ramps to now
                cur[k] = v0 + (tg - v0) * min(1.0, (now - s0) / n)
            ramps = {k: r for k, r in ramps.items() if r[0] + r[3] > now}
            ramps[ch["input"]] = (now, cur[ch["input"]], ch["target"], ch["length"])
            end = min(r[0] + r[3] for r in ramps.values())
            at = {k: (ramps[k][1] + (ramps[k][2] - ramps[k][1]) * (end - ramps[k][0]) / ramps[k][3]) if k in ramps else cur[k]
                  for k in names}
            out.append({"matrix_target": model_pan(at["split_amount"], at["pan"], at["split_l"], at["split_r"], at["volume_gain"]),
                        "length": end - now})
        return {"after_changes": out}
    if comp == "polyline":
        return {"points": model_points(*a["start"], *a["end"], a["controls"])}
    if comp == "playback-value":
        return {"values": [model_playback(a["events"], a["samples_per_beat"], t) for t in a["times"]]}
    if comp == "discrete-value":
        return {"values": [model_discrete(a["events"], t) for t in a["times"]]}
    if comp == "ramp-length":
        return {"length": model_ramp_length(a["step"], a["segment"], a["samples_per_beat"], a["transport"])}
    raise KeyError(comp)


def close(a, b, tol):
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str):
        return a == b
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    return abs(a - b) <= tol


def judge_computation(c):
    errs = []
    for i, ev in enumerate(c["evaluations"]):
        try:
            got = model_computation(c["computation"], ev["arguments"])
        except Excluded as e:
            errs.append(f"evaluation {i}: excluded input: {e}")
            continue
        if not close(ev["expected"], got, max(c["tolerance"], 0)):
            errs.append(f"evaluation {i}: model {got} vs expected {ev['expected']}")
    return errs


def mixer_values(root):
    """Read the T1 mixer values the render model needs; raise Excluded outside the released preconditions."""
    ls = root.find("LiveSet")
    tracks = list(ls.find("Tracks"))
    if [t.tag for t in tracks].count("ReturnTrack") != 1 or len(list(ls.find("SendsPre"))) != 1:
        raise Excluded("render sets have exactly one return and one SendPreBool")
    if any(e.get("Value") == "true" for e in root.iter("SoloSink")):
        raise Excluded("SoloSink true")
    out = {}
    for t in tracks + [ls.find("MainTrack")]:
        key = {"1": "A", "2": "B", "3": "R"}.get(t.get("Id"), "M") if t.tag != "MainTrack" else "M"
        dc, mx = t.find("DeviceChain"), t.find("DeviceChain/Mixer")
        if t.tag != "MainTrack":
            if dc.find("AudioOutputRouting/Target").get("Value") != "AudioOut/Main":
                raise Excluded("output not AudioOut/Main")
            if t.find("TrackGroupId").get("Value") != "-1":
                raise Excluded("grouped")
            if list(t.find("AutomationEnvelopes/Envelopes")):
                raise Excluded("track automation")
        if list(dc.find("DeviceChain/Devices")):
            raise Excluded("devices")
        if any(True for _ in t.iter("AudioClip")) or any(True for _ in t.iter("MidiClip")):
            raise Excluded("clips")
        val = lambda p: mx.find(p).get("Value")  # noqa: E731
        if val("CrossFadeState/Manual") != "1":
            raise Excluded("crossfade assignment A or B")
        g = f32(float(val("Volume/Manual")))
        if not f32(float(MIN)) <= g <= f32(float(VMAX)):
            raise Excluded("volume out of range")
        pans = [f32(float(val(p + "/Manual"))) for p in ("Pan", "SplitStereoPanL", "SplitStereoPanR")]
        if any(not -1 <= p <= 1 for p in pans):
            raise Excluded("pan out of range")
        mode = val("PanMode")
        if mode not in ("0", "1"):
            raise Excluded("pan mode")
        spk = val("Speaker/Manual")
        if key == "M" and spk != "true":
            raise Excluded("main track switch off")
        holders = mx.findall("Sends/TrackSendHolder")
        sends = []
        for h in holders:
            s = f32(float(h.find("Send/Manual").get("Value")))
            if not f32(float(MIN)) <= s <= 1.0:
                raise Excluded("send out of range")
            sends.append((s, h.find("EnabledByUser").get("Value") == "true"))
        out[key] = {"v": 0.0 if g <= FLOOR else g, "pan": pans[0], "sl": pans[1], "sr": pans[2], "w": float(mode),
                    "on": 1.0 if spk == "true" else 0.0, "sends": sends}
    mm = ls.find("MainTrack/DeviceChain/Mixer")
    allowed = {mm.find(p + "/AutomationTarget").get("Id") for p in ("Tempo", "TimeSignature")}
    if any(e.find("EnvelopeTarget/PointeeId").get("Value") not in allowed
           for e in ls.find("MainTrack/AutomationEnvelopes/Envelopes")):
        raise Excluded("main automation other than tempo and time signature")
    return out


def model_render(xml_bytes, sig_keys):
    """Coefficients of the main output in the input channels, from the released rules (2 x 2 per input track)."""
    import xml.etree.ElementTree as ET
    mv = mixer_values(ET.fromstring(xml_bytes))
    P = {k: model_pan(t["w"], t["pan"], t["sl"], t["sr"], t["v"]) for k, t in mv.items()}
    zero = [[0.0, 0.0], [0.0, 0.0]]

    def mat(p):  # rows = output channel (L, R), columns = input channel (L, R)
        return [[p[0], p[2]], [p[1], p[3]]]

    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    def add(a, b):
        return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]

    def scale(s, a):
        return [[s * x for x in row] for row in a]

    to_main = {}
    return_in = {}
    for k in ("A", "B"):
        t = mv[k]
        x = [[1.0, 0.0], [0.0, 1.0]] if k in sig_keys else None  # coefficient of x_k in x_k
        if x is None:
            continue
        to_main[k] = scale(t["on"], mul(mat(P[k]), x))
        s, enabled = t["sends"][0]
        if s == f32(float(MIN)) or t["on"] == 0.0:
            continue  # g = 0 at the stored minimum, or the send gate is off: no send contribution
        return_in[k] = None  # unknown send gain or activity (not released)
    r = mv["R"]
    if any(v is None for v in return_in.values()) and r["on"] != 0.0:
        raise Excluded("a send above its minimum reaches a playing return")
    if r["sends"][0][0] != f32(float(MIN)) and r["on"] != 0.0:
        raise Excluded("return send above its minimum")
    total = {}
    for k, m in to_main.items():
        total[k] = mul(mat(P["M"]), m)  # the return contributes nothing in every released render
    return {ch: {f"{k}.{c}": total[k][row][col] for k in total for col, c in enumerate("LR")}
            for row, ch in enumerate("LR")}


def judge_render(c, xml_bytes):
    errs = []
    keys = list(c["render"]["signals"])
    try:
        got = model_render(xml_bytes, keys)
    except Excluded as e:
        return [f"excluded input: {e}"]
    exp = c["expected"]["main"]
    for ch in "LR":
        for name in {*got[ch], *exp[ch]}:
            if abs(got[ch].get(name, 0.0) - exp[ch].get(name, 0.0)) > 1e-7:
                errs.append(f"{ch} {name}: model {got[ch].get(name, 0.0)} vs expected {exp[ch].get(name, 0.0)}")
    # the comparator itself, on the shipped signals: expected and model outputs agree within the tolerance
    sig = {k: read_wav(STAGE / c["render"]["signals"][k]) for k in keys}
    xmax = max(abs(v) for s in sig.values() for fr in s for v in fr)
    for n in range(c["render"]["frames"]):
        for ci, ch in enumerate("LR"):
            y = sum(got[ch].get(f"{k}.{c2}", 0.0) * sig[k][n][j] for k in keys for j, c2 in enumerate("LR"))
            e = sum(exp[ch].get(f"{k}.{c2}", 0.0) * sig[k][n][j] for k in keys for j, c2 in enumerate("LR"))
            if abs(y - e) > c["tolerance_factor"] * xmax:
                errs.append(f"frame {n} {ch}")
    return errs


# ---- traceability (analyst-only; never shipped) ----
SPEC = "wiki/specs/mix-graph.md (SPEC-MIX-GRAPH r1)"
EV = {
    "x-sends": "analysis/ableton-live-12.4.3/r2/t14-mix-v1/results/mix.json sends[] (Live x86 0x101b40d30 = engine TSendVolumes::Calc 0x171a20; raw/runs.jsonl); notes-q019.txt 3d-3e",
    "x-switch": "t14 results/mix.json main_switch[] (0x101b40cf0 TVolumeSwitch::Calc)",
    "x-solo": "t14 results/mix.json solo.switch_word (0x101b3fdc0, 0x101b3ff50) and solo.split (0x101b401c0); notes-solo.txt",
    "x-fade": "t14 results/mix.json solo.track_fade_time (0x101b0ee70 after 0x101b0ecb0: 75)",
    "x-ramp": "t14 results/mix.json ramp_interpolator[] (0x101b2b970, 0x101b2bae0, 0x101b2ba30)",
    "x-panner": "t14 results/mix.json volume_panner[] (setters 0x101b243f0, 0x101b244a0; recompute 0x101b27860)",
    "x-bezier": "t14 results/mix.json automation.E9_polyline.points (0x1011f1610; point emission 0x102520a60, s=(i+1)/16, pc + constants)",
    "x-segment": "t14 results/mix.json automation.E9_polyline.played, E13_t0, E1_linear (0x101b1f400; subss then divsd read in x86-disasm.txt)",
    "s-pointlist": "notes-automation.txt 1a (0x102823cb0; first time := -1e7 at 0x102823d84 from 0x105dae938, objdump)",
    "s-lookup": "notes-automation.txt 1b (engine 0x141110, 0x140310 pc; grid 0x15bdfe0); Bool/Enum mode 1",
    "s-ramplen": "notes-automation.txt 2 (engine 0x16a240 pc; Live x86 0x101b39550 objdump re-read 2026-10-18: cvttsd2si %xmm0,%eax 32-bit, cmovl 0x10000, cmovg MinSeg; 0x101b1f3d0: slope 0 -> 1.7976931348623155e308 sentinel -> no ramp); defaults hook 0x10282b410 (N 1000, MinSeg 200, no smoothing) objdump",
    "s-graph": "notes-mix.txt (track-out unit builder 0x102866450 pc; OTrackOutProcessor ports); SendsPre mask 0x1027bde00 pc",
    "s-perSample": "notes-mix.txt; per-sample functions 0x101b4d870 (main: add then multiply) and 0x101b4c400 (send: multiply then add), objdump",
    "s-summing": "send accumulation addsd 0x101b4c400; main outputs float32 0x101b4d870 (objdump)",
    "s-volume": "notes-q019.txt 1a-1c, 2a-2c, 5 (manual value sent as position; engine curve 1 and floor 0x39a7c5ac); x2-mixer-v1 results/mixer.json fader.roundtrip_Q019 (exact at -70, -6, 0, +6 dB)",
    "x-panlaw": "analysis/ableton-live-12.4.3/r2/x2-mixer-v1/results/mixer.json pan_law[] (TVolumePanner::Calc 0x101b719e0, glibc cos)",
    "s-panmode": "notes-mix.txt PanMode -> ramp node -> pan-mode amount (pc)",
    "s-sendspre": "SendsPre -> SendIsPost<k> (notes-mix.txt; 0x1027bde00 12-bit mask, pc)",
    "s-sendmin": "notes-q019.txt 3a (send ToEngine = send-curve position, pc; converter kind 0 objdump 0x102788389); x2-mixer-v1 fader.gain_to_position send 0.0003162277571 -> 0.0 (X); under A4 floor(curve0(0)) = 0, without A4 the port receives position 0",
    "s-mute": "notes-solo.txt; switch word X with solo type 0",
    "s-nosolo": "SPEC-MIX-GRAPH A2: a loaded SoloSink true acts as pressing Solo (untraced); with every SoloSink false no Solo is pressed under either reading",
    "d-template": "analysis/ableton-live-12.4.3/r2/t11-structure-v1/make_fixture.py (T11-MIN builders); schema_check.py, fixture_audit.py",
    "adr-0004": "wiki/decisions/adr-0004-target-scope-t1.md render conventions (settled start)",
}
TRACE = {
    "MG-001": ("MG-001", ["x-sends"], "as written"),
    "MG-002": ("MG-002", ["x-sends"], "as written"),
    "MG-003": ("MG-003", ["x-sends"], "as written"),
    "MG-004": ("MG-004", ["x-sends"], "as written; three evaluations"),
    "MG-005": ("MG-005", ["x-sends"], "as written; two evaluations"),
    "MG-006": ("MG-006", ["x-switch"], "as written; three evaluations"),
    "MG-007": ("MG-007", ["x-solo"], "narrowed: solo types 0-6 only (type 7 is not a category); the cue column dropped; types given as category names"),
    "MG-009": ("MG-009", ["x-fade"], "as written"),
    "MG-010": ("MG-010", ["x-ramp"], "as written"),
    "MG-011": ("MG-011", ["x-ramp"], "as written; two evaluations"),
    "MG-012": ("MG-012", ["x-panner", "x-panlaw"], "as written"),
    "MG-031": ("MG-031", ["x-bezier"], "as written"),
    "MG-032v": ("MG-032 value part", ["x-bezier", "x-segment", "s-pointlist", "s-lookup"], "re-authored as a computation: the claim that M's arrangement envelope drives M's pan (A8) is dropped; times are envelope times"),
    "MG-033v": ("MG-033 value part", ["x-segment", "s-pointlist", "s-lookup"], "re-authored as a computation (A8 dropped)"),
    "MG-034v": ("MG-034 value part", ["x-segment", "s-pointlist", "s-lookup"], "re-authored as a computation (A8 dropped)"),
    "NEW-DISCRETE": ("new (REQ-013 Bool/Enum and step clauses had no case)", ["s-lookup", "s-pointlist"], "static-derived"),
    "NEW-RAMPLEN": ("new (REQ-014 had no case without A3/A8)", ["s-ramplen"], "static-derived; A6 and the pan step stated in the contract"),
    "NEW-BASE": ("new (REQ-001/002/006 had no case without A4/A7)", ["s-graph", "s-perSample", "s-summing", "s-sendmin", "x-panlaw", "d-template", "adr-0004"], "composed"),
    "MG-029a": ("MG-029 narrowed", ["s-volume", "x-panlaw", "s-sendmin", "adr-0004"], "stored 2 replaced by the in-range maximum 1.99526238: opening out-of-range values is U (SPEC-MIXER-VALUES r4 REQ-015)"),
    "MG-029b": ("MG-029 narrowed", ["s-volume", "s-sendmin", "adr-0004"], "stored 0 and -1 replaced by the in-range minimum 0.0003162277571 (same reason)"),
    "NEW-FLOOR-BELOW": ("new (floor inside the stored domain)", ["s-volume", "s-sendmin", "adr-0004"], "composed"),
    "NEW-FLOOR-ABOVE": ("new (floor inside the stored domain)", ["s-volume", "x-panlaw", "s-sendmin", "adr-0004"], "composed; gain within the comparator of 0.00033"),
    "MG-030m": ("MG-030 without the send", ["s-volume", "x-panlaw", "s-sendmin", "adr-0004"], "A's send kept at its minimum so A4/A7 are not needed"),
    "MG-022m": ("MG-022 without the send", ["x-panlaw", "s-sendmin", "adr-0004"], "A's send kept at its minimum"),
    "NEW-SPLIT": ("new (REQ-004 split amount)", ["x-panlaw", "s-panmode", "s-sendmin", "adr-0004"], "composed"),
    "NEW-SUM": ("new (REQ-006 main sum)", ["s-summing", "s-volume", "x-panlaw", "s-sendmin", "adr-0004"], "composed"),
    "MG-023": ("MG-023", ["x-solo", "x-sends", "s-mute", "s-nosolo", "adr-0004"], "as written; the expectation does not depend on A4 or A7 (send gate 0 zeroes every send entry, MG-004)"),
    "NEW-RETURN-OFF": ("new (REQ-007 on a return)", ["x-solo", "s-mute", "s-nosolo", "s-sendmin", "adr-0004"], "composed; independent of A4 and A7 because the return's gates are 0"),
}
NOT_RELEASED = {
    "MG-008": "grades three internal predicates with no released observable; its reading 'speaker ignored for type 4' contradicts REQ-008's X table (type 4: main gate = s)",
    "MG-020, MG-021, MG-022, MG-030": "send above its minimum reaching a playing return: A4 (Q-023, Q-019 condition) and A7 (send-active derivation, Q-023 item); MG-022 and MG-030 re-authored without the send",
    "MG-024, MG-025, MG-026, MG-027": "solo loaded from the set: A2 (Q-023)",
    "MG-028": "crossfade assignment A: A5 (Q-023); also A4 and A7",
    "MG-029 (stored 2, 0, -1)": "out-of-range stored volume: opening is U in SPEC-MIXER-VALUES r4 REQ-015; re-authored in range",
    "MG-032, MG-033, MG-034 (render form)": "M's arrangement envelope driving M's pan rests on A8 (Q-023); value parts re-authored as computations",
    "MG-035": "A3, A6 and A8 (volume automation units and drive)",
    "MG-036": "A7 and A8 (Speaker envelope on R with A's send above minimum)",
    "MG-037": "A8 (session launch stops arrangement automation)",
    "MG-038 to MG-041": "U cases",
}
CLAUSES = {
    "001": "S clauses kept; >12 returns, holder gaps and count mismatch excluded (U)",
    "002": "S, as written",
    "003": "assign None, manual volume, in-range stored gain; A5 (A/B) and A3 (automated) parts excluded; consequences for out-of-range stored values excluded (opening U)",
    "004": "X matrix and pan law (restated from SPEC-MIXER-VALUES r4 REQ-013); S split amount",
    "005": "X matrix and consequences; S SendsPre mapping; S-cond (A4) gain clause narrowed to the exact stored minimum; A7 and U a_k excluded",
    "006": "S clauses; summation order U excluded (tolerance)",
    "007": "X and S, as written",
    "008": "X gate table kept (types 0-6 as categories); S (A2) category assignment excluded except: no SoloSink true -> no soloed track; U excluded",
    "009": "S and X, as written; volume-curve evaluation narrowed to the volume gain",
    "010": "X 75 samples; S scope; crossfade-assign ramp excluded with A/B assignments; automation ramps -> REQ-014; developer option U excluded",
    "011": "Proposed (A1) adopted as the ADR 0004 render convention; automation part dropped",
    "012": "not released: S (A8) and U",
    "013": "S and X kept as a computation on envelope time; automation offset (untraced) and drive (REQ-012) excluded; comparison with REQ-AUTOMATION-ENVELOPES-010 is analyst-side only",
    "014": "S (A6) kept with A6 and the pan step stated; volume/send example (A3/A4) excluded; r >= 2^31 excluded (finding F3)",
    "015": "not released: S-cond (A3)",
    "016": "not released: its observable is the drive state of REQ-012",
}

# ---- checks ----
DENY = [r"analysis/", r"wiki/", r"raw/", r"\.\./", r"0x[0-9a-fA-F]{4,}", r"FUN_", r"disassembl", r"decompil",
        r"pseudocode", r"Ghidra", r"vtable", r"dossier", r"corpus", r"\bPRB-", r"\bQ-0", r"\bMG-0", r"\bMV-0",
        r"\bAEN-", r"\bLSS-", r"\bA[1-8]\b", r"\bE(?:1|9|13)\b", r"\bB0\b", r"T11", r"\bt1[1-4]\b", r"x2-", r"T1\.",
        r"MainOn", r"SendsOn", r"SendIsPost", r"PanModeAmount", r"GroupOn", r"mpActive", r"TSend", r"TVolume", r"ORamp",
        r"OSolo", r"OTrack", r"OFloat", r"OAuto", r"OAsync", r"OCross", r"OConvert", r"SetRamp", r"GetRamp",
        r"Extrapolat", r"\bSIs", r"STrackFade", r"NAudio", r"AConvert", r"ALevel", r"SControl", r"SAudio", r"cvtt",
        r"Timeable", r"Remoteable", r"TrackDevice", r"\bmp[A-Z]", r"\bslot\b", r"[Ee]ngine", r"harness", r"xexec",
        r"objdump", r"Python", r"derivation", r"traceab", r"Recording Audio", r"/home/", r"/var/", r"/tmp/",
        r"Live\.arm64", r"ev_[0-9a-f]", r"\+0x", r"glibc", r"\bpc\b", r"✓", r"Prehear", r"PreHear(?!Track)"]
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


def text_of(p):
    return p.read_text() if p.suffix != ".wav" else ""


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
    refs = [c["input"] for c in cases if c["input"]] + [p for c in cases if c["kind"] == "render"
                                                        for p in c["render"]["signals"].values()]
    missing_inputs = sorted({r for r in refs if not (d / r).is_file()})
    deny = {str(p.relative_to(d)): h for p in [*files, d / "manifest.json"] if (h := deny_hits(text_of(p), p.name))}
    symlinks = [str(p.relative_to(d)) for p in d.rglob("*") if p.is_symlink()]
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "symlinks": symlinks,
            "markdown_links": {k: len(v) for k, v in link_rows.items()}, "unresolved_links": bad_links,
            "missing_case_inputs": missing_inputs, "deny_list_hits": deny,
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def evidence_identity():
    out = {}
    for run in ("r2/t14-mix-v1", "r2/x2-mixer-v1", "r2/t11-structure-v1"):
        m = json.loads((EVID / run / "manifest.json").read_text())
        files = m["files"]
        bad = [p for p, h in files.items() if not (EVID / run / p).is_file()
               or sha((EVID / run / p).read_bytes()) != (h["sha256"] if isinstance(h, dict) else h)]
        out[run] = {"manifest_sha256": sha((EVID / run / "manifest.json").read_bytes()), "files": len(files),
                    "mismatches": bad}
    t14 = json.loads((T14 / "manifest.json").read_text())["slices"]
    x86 = Path(t14["live_x86_64"]["path"])
    out["live_x86_64_sha256_matches"] = x86.is_file() and sha(x86.read_bytes()) == X86_SHA == t14["live_x86_64"]["sha256"]
    arm = EVID / "derived/Live.arm64"
    out["live_arm64_sha256_matches"] = arm.is_file() and sha(arm.read_bytes()) == ARM_SHA
    out["schema_sha256_matches"] = sha(SCHEMA.read_bytes()) == SCHEMA_SHA
    return out


def structure_checks(cases):
    """T11 structure rules on every fixture: no schema deviation, no traced refusal, no unknown shape."""
    sch = schema_check.load_schema(str(SCHEMA))
    fixture_audit.LIVESET_ORDER[:] = list(sch["LiveSet"])
    import xml.etree.ElementTree as ET
    out = {}
    for c in cases:
        if c["kind"] != "render":
            continue
        root = ET.fromstring((STAGE / c["input"]).read_bytes())
        dev, r = fixture_audit.measure(sch, root)
        out[c["id"]] = {"schema_deviations": dev, "refusals": fixture_audit.refusals(r, dev),
                        "unknown_shapes": fixture_audit.unknowns(r), "pointees": r["pointees"],
                        "next_pointee_id": r["next_pointee_id"], "max_pointee_id": r["max_pointee_id"]}
    return out


def perturb(x):
    """Alter the first number or Boolean leaf of x in place; return True when one was altered."""
    items = list(x.items()) if isinstance(x, dict) else list(enumerate(x))
    for k, v in items:
        if isinstance(v, bool):
            x[k] = not v
            return True
        if isinstance(v, (int, float)):
            x[k] = v + (1 if isinstance(v, int) else 0.01)
            return True
        if isinstance(v, (dict, list)) and perturb(v):
            return True
    return False


def mutation_probe(cases):
    """Each case with one expected number altered must be caught by the cross-check."""
    missed = []
    for c in cases:
        c2 = json.loads(json.dumps(c))
        if c2["kind"] == "computation":
            assert perturb(c2["evaluations"][0]["expected"])
            if not judge_computation(c2):
                missed.append(c2["id"])
        else:
            m = c2["expected"]["main"]["L"]
            m["A.L"] = m.get("A.L", 0.0) + 0.01
            if not judge_render(c2, (STAGE / c2["input"]).read_bytes()):
                missed.append(c2["id"])
    planted = deny_hits("see analysis/x and 0x101b40d30 via MG-020 under A4 with SendsOn in the engine", "spec.md")
    return {"mutated_cases": len(cases), "missed": missed, "planted_deny_terms_flagged": len(planted)}


def excluded_probes():
    probes = {"SoloSink true on A": {("A", "SoloSink"): "true"},
              "crossfade assignment A": {("A", "CrossFadeState"): "0"},
              "volume 2": {("A", "Volume"): "2"}, "volume 0": {("A", "Volume"): "0"},
              "send 0.5 reaching a playing return": {("A", "Send"): "0.5"},
              "return send 0.5": {("R", "Send"): "0.5"},
              "pan mode 2": {("A", "PanMode"): "2"}, "main switch off": {("M", "Speaker"): "false"},
              "send 0.000318 (between minimum and floor)": {("A", "Send"): "0.000318"}}
    out = {}
    for name, ch in probes.items():
        try:
            model_render(doc(ch), ["A"])
            out[name] = False
        except Excluded:
            out[name] = True
    try:
        model_ramp_length(0.002, [0.0, 0.0, 100.0, 1e-7], SPB, "playing")
        out["ramp length step/|slope| >= 2^31"] = False
    except Excluded:
        out["ramp length step/|slope| >= 2^31"] = True
    return out


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    srcs = [c["src"] for c in all_cases()]
    problems, fixtures, seen = {}, {}, {}
    base = doc().decode().split("\n")
    for c in cases:
        if c["kind"] == "computation":
            errs = judge_computation(c)
        else:
            raw = (STAGE / c["input"]).read_bytes()
            errs = judge_render(c, raw)
            if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n"):
                errs.append("not ASCII/LF/final newline")
            if raw in seen:
                errs.append(f"same bytes as {seen[raw]}")
            seen[raw] = c["id"]
            changed = [ln.strip() for ln, b in zip(raw.decode().split("\n"), base) if ln != b]
            fixtures[c["id"]] = {"bytes": len(raw), "lines": raw.count(b"\n"), "lines_changed_from_template": changed}
        if errs:
            problems[c["id"]] = errs
    struct_ = structure_checks(cases)
    bad_struct = {k: v for k, v in struct_.items() if v["schema_deviations"] or v["refusals"] or v["unknown_shapes"]}
    signals = {}
    for k, (rel, fn) in SIGNALS.items():
        data = read_wav(STAGE / rel)
        signals[rel] = {"frames": len(data), "bytes": (STAGE / rel).stat().st_size,
                        "matches_formula": data == [(a / 32768, b / 32768) for a, b in map(fn, range(FRAMES))],
                        "max_abs": max(abs(v) for fr in data for v in fr)}
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "mix-graph-v1 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases),
              "kinds": {k: sum(c["kind"] == k for c in cases) for k in ("computation", "render")},
              "case_problems": problems, "excluded_input_probes_rejected": excluded_probes(),
              "mutation_probe": mutation_probe(cases), "evidence_identity": evidence_identity(),
              "structure_checks": {"schema": str(SCHEMA.name), "fixtures": len(struct_), "failing": bad_struct,
                                   "detail": struct_},
              "signals": signals, "fixtures": fixtures, **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model restates the "
                        "same evidence and is not an oracle; the render model is static (coefficients), as the cases are."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    trace = {"schema": "mix-graph-traceability-v1", "spec": SPEC, "evidence": EV, "clauses": CLAUSES,
             "cases": {}, "draft_cases_not_released": NOT_RELEASED,
             "assumptions_relied_on": {"A1": "settled for T1 as the ADR 0004 render convention (REQ-011); every render case",
                                       "A6": "stated in the contract (REQ-014)",
                                       "pan step 0.002": "inferred from the pan range -1..1; stated in the contract",
                                       "arm64 equivalence": "fma-scan.txt; stated in the contract"},
             "assumptions_not_relied_on": ["A2", "A3", "A4 (except: a send at the exact stored minimum gives 0 with or without it)",
                                           "A5", "A7", "A8"]}
    for c, src in zip(cases, srcs):
        s, ev, note = TRACE[src]
        assert all(e in EV for e in ev), src
        trace["cases"][c["id"]] = {"source": s, "evidence": ev, "change": note}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "kinds", "case_problems", "excluded_input_probes_rejected",
                                             "mutation_probe", "evidence_identity", "payload_files",
                                             "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
                                             "missing_case_inputs", "deny_list_hits", "manifest_sha256")}, indent=1))
    print("structure failing:", bad_struct, "signals:", signals)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
