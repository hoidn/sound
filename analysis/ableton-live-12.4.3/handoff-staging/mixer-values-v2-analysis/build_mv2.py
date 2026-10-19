"""Stage the mixer-values-v2 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from any directory:
  python3 -I build_mv2.py build          # fixtures/, cases.json, draft manifest.json (files[] empty)
  python3 -I build_mv2.py seal           # structure checks, cross-checks, manifest files[], author-validation.json,
                                         # traceability.json
  python3 -I build_mv2.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Inputs (read-only): the released mixer-values-v1 package (carried case records), the mixer-values-v1 build script
(case edits, cross-check model, packaging helpers; imported unchanged), the T1.1 generator make_fixture.py
(T11-MIN rules; imported unchanged) and checkers, and the X2 mixer results (expected values of the new cases).
Fixtures are written from one template set: T11-MIN without the content other specs own. No shipped file is read.
README.md, AGENTS.md and spec.md are hand-written.
"""
import json, sys

sys.dont_write_bytecode = True  # imports below live in other analysts' directories; leave no caches there
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "mixer-values-v2"
EVID = ROOT / "analysis/ableton-live-12.4.3"
T11 = EVID / "r2/t11-structure-v1"
X2 = EVID / "r2/x2-mixer-v1"
V1PKG = ROOT / "handoff/mixer-values-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
sys.path[:0] = [str(HERE), str(T11), str(HERE.parent / "mixer-values-v1-analysis")]  # -I omits the script dir
import make_fixture as mf  # noqa: E402  T11-MIN generator (SPEC-LIVE-SET-STRUCTURE REQ-018), unchanged
import build_mv1 as v1  # noqa: E402  v1 case edits, model(), judge(), verify(), unchanged

R = "REQ-MIXER-VALUES-"
XLABEL = "extracted execution (x86_64 slice, glibc substitutions); arm64 equivalence inferred"
V1_MANIFEST_SHA = "5f6b8401b9324d0cf3d60da47d190e61b93e1935f96995128021f29c9f39cd60"
TRACK = {"audio": "AudioTrack", "midi": "MidiTrack", "return": "ReturnTrack", "main": "MainTrack", "cue": "PreHearTrack"}
f32 = v1.f32


# ---- fixtures: the template set and the per-case edits of mixer-values-v1 ----
def template():
    """T11-MIN (make_fixture.build) without clips (so no sample file), devices and the MIDI track's volume envelope.
    Ids, names, colours, routing, slots, scenes, SendsPre, transport and the main track's tempo and time-signature
    envelopes are T11-MIN's; pointee Ids run 1 to 66 in T11-MIN's order, so NextPointeeId is 67."""
    ids, scenes = mf.Ids(), 2
    m_mix, _ = mf.mixer(ids, [(0, "true")])
    a_mix, _ = mf.mixer(ids, [(0, "true")])
    r_mix, _ = mf.mixer(ids, [(0, "false")])
    main_mix, main_t = mf.mixer(ids, [], main=True)
    pre_mix, _ = mf.mixer(ids, [])
    seq = lambda: mf.el("MainSequencer", None, mf.slots(None, scenes))
    tracks = mf.el("Tracks", None,
                   mf.track("MidiTrack", 1, "Lead", "Lead", 15, m_mix, [], seq(), [], scenes),
                   mf.track("AudioTrack", 2, "", "2-Audio", 3, a_mix, [], seq(), [], scenes),
                   mf.track("ReturnTrack", 3, "", "A-Return", 55, r_mix, [], None, []))
    main = mf.el("MainTrack", None, mf.name("", "Main"), mf.v("Color", 69),
                 mf.el("AutomationEnvelopes", None, mf.el("Envelopes", None,
                       mf.envelope(0, main_t["TimeSignature"], [mf.el("EnumEvent", {"Id": "0", "Time": mf.L, "Value": "201"})]),
                       mf.envelope(1, main_t["Tempo"], [mf.el("FloatEvent", {"Id": "0", "Time": mf.L, "Value": "120"})]))),
                 mf.el("DeviceChain", None, mf.routing("AudioOutputRouting", "AudioOut/External/S0"), main_mix,
                       mf.el("DeviceChain", None, mf.el("Devices"))))
    prehear = mf.el("PreHearTrack", None, mf.el("DeviceChain", None, pre_mix))
    scene_els = [mf.el("Scene", {"Id": str(i)}, mf.follow_action(), mf.v("Name", f"Scene {i + 1}"), mf.v("Color", -1),
                       mf.v("Tempo", 120), mf.v("IsTempoEnabled", "false"), mf.v("TimeSignatureId", 201),
                       mf.v("IsTimeSignatureEnabled", "false")) for i in range(scenes)]
    liveset = mf.el("LiveSet", None, mf.v("NextPointeeId", ids.n + 1), tracks, main, prehear,
                    mf.el("SendsPre", None, mf.el("SendPreBool", {"Id": "0", "Value": "false"})),
                    mf.el("Scenes", None, *scene_els),
                    mf.el("Transport", None, mf.v("LoopOn", "false"), mf.v("LoopStart", 0), mf.v("LoopLength", 8),
                          mf.v("CurrentTime", 0)),
                    mf.v("GlobalQuantisation", 4), mf.v("AutoQuantisation", 0), mf.v("CrossfadeCurve", 2))
    return mf.el("Ableton", {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1"}, liveset)


def child(node, tag):
    return next(k for k in node[2] if k[0] == tag)


def doc(changes=None):
    """The template set with {(mixer, element): text} or {("set", "CrossfadeCurve"): text} changes (v1 keys)."""
    root = template()
    ls = root[2][0]
    for (m, k), text in (changes or {}).items():
        if m == "set":
            child(ls, k)[1]["Value"] = text
            continue
        t = child(child(ls, "Tracks"), TRACK[m]) if m in ("audio", "midi", "return") else child(ls, TRACK[m])
        mx = child(child(t, "DeviceChain"), "Mixer")
        node = (child(child(child(child(mx, "Sends"), "TrackSendHolder"), "Send"), "Manual") if k == "Send"
                else child(mx, k) if k in ("SoloSink", "PanMode") else child(child(mx, k), "Manual"))
        node[1]["Value"] = text
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    mf.render(root, 0, lines)
    return ("\n".join(lines) + "\n").encode("ascii")


# ---- computed cases (new): inputs chosen here, expected values from the X2 run ----
def x2():
    return json.loads((X2 / "results/mixer.json").read_text())


CURVE_NAMES = v1.CURVES  # code order: Dipped ... Transition
XF_POSITIONS = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0]  # multiples of 1/64 only (the X run also has +-0.95)
GAIN_TEXT = {0.0003162277571391314: "-70 dB", 0.5011872053146362: "-6 dB", 1.0: "0 dB", 1.9952623844146729: "+6 dB"}
G2P_TEXT = {("volume", 0.5): "0.5 (-6.021 dB), between two curve points", ("volume", 0.001): "0.001 (-60 dB), near the bottom",
            ("volume", 2.0): "2, above the top point", ("volume", 1.0): "1 (0 dB), a curve point",
            ("volume", 0.1995263397693634): "the curve point at position 0.5 (-14 dB)",
            ("send", 0.1000000014901161): "0.1 (-20 dB), just below a curve point", ("send", 1.0): "1 (0 dB), the top point",
            ("send", 0.0003162277571391314): "the bottom point (-70 dB)"}


def computed_cases():
    x = x2()
    out = []  # (kind of function, requirement, purpose, compute fields, expected, comparator, X locator)
    for r in x["fader"]["position_to_gain"]:
        p = f32(r["position"])
        out.append(("position-to-gain", "005", f"{r['curve'].capitalize()} curve, position to gain: position {r['position']:g}",
                    {"curve": r["curve"], "position": p}, {"gain": r["gain_x"]}, "step",
                    f"fader.position_to_gain {r['curve']} {r['position']}"))
    for r in x["fader"]["gain_to_position"]:
        g = f32(r["gain"])
        out.append(("gain-to-position", "005", f"{r['curve'].capitalize()} curve, gain to position: gain {G2P_TEXT[r['curve'], r['gain']]}",
                    {"curve": r["curve"], "gain": g}, {"position": r["position_x"]}, "1e-6",
                    f"fader.gain_to_position {r['curve']} {r['gain']}"))
    seen = set()
    for r in x["fader"]["roundtrip_Q019"]:
        if (r["curve"], r["stored_gain"]) in seen:
            continue
        seen.add((r["curve"], r["stored_gain"]))
        assert r["exact_roundtrip"] and r["gain_back_x"] == r["stored_gain"]
        out.append(("round-trip", "005",
                    f"{r['curve'].capitalize()} curve, round trip: the {GAIN_TEXT[r['stored_gain']]} curve point returns exactly",
                    {"curve": r["curve"], "gain": r["stored_gain"]}, {"gain": r["gain_back_x"]}, "exact",
                    f"fader.roundtrip_Q019 {r['curve']} {r['stored_gain']}"))
    for r in x["pan_law"]:
        sl, sr = r.get("splitL", -1.0), r.get("splitR", 1.0)
        w, v = r["w"], r["vol"]
        what = (f"pan {r['pan']:g}" if w == 0 else f"split pans {sl:g} and {sr:g}") + (", v = 0" if v == 0 else "")
        out.append(("pan-law", "013", f"Pan-law gains, w = {w:g}: {what}",
                    {"w": w, "pan": r["pan"], "split_left": sl, "split_right": sr, "v": v},
                    {"gains": dict(zip(["L->L", "L->R", "R->L", "R->R"], r["gains_LL_LR_RL_RR"]))}, "step-or-1e-12",
                    f"pan_law w={w} pan={r['pan']} splits={sl},{sr} vol={v}"))
    for code, row in enumerate(x["crossfade"]):
        lv = {l["x"]: l["level_x"] for l in row["levels"]}
        out.append(("crossfade-level", "014", f"Crossfade curve code {code} ({CURVE_NAMES[code]}): levels at seven positions",
                    {"curve": code, "positions": XF_POSITIONS},
                    {"levels": [{"position": p, "level": lv[p]} for p in XF_POSITIONS]}, "step-or-1e-12",
                    f"crossfade {row['curve']} (code {code})"))
    return out


COMPARATORS = {
    "step": "gain: the expected binary32 value or one of its two binary32 neighbours",
    "1e-6": "position: within 1e-6 of the expected value",
    "exact": "gain: exactly the expected binary32 value, which equals the input gain",
    "step-or-1e-12": ("each listed gain or level: the expected binary32 value, one of its two binary32 neighbours, "
                      "or within 1e-12 of it"),
}


# ---- packaging ----
def cid(n):
    return f"MIXER-VALUES-{n:03d}"


def v1_records():
    return json.loads((V1PKG / "cases.json").read_text())["cases"]


def new_records():
    recs = []
    for n, (fn, req, purpose, fields, expected, comp, _) in enumerate(computed_cases(), start=38):
        recs.append({"id": cid(n), "kind": "computation", "purpose": purpose, "requirements": [R + req],
                     "input": None, "action": "compute", "compute": {"function": fn, **fields}, "expected": expected,
                     "expectation_provenance": XLABEL, "reference_execution": "not-run", "candidate_execution": "not-run",
                     "comparator": COMPARATORS[comp]})
    return recs


def edits_text(changes):
    return "; ".join(f"{m} {k}{'' if k in ('SoloSink', 'PanMode') or m == 'set' else '/Manual'} {t}"
                     for (m, k), t in changes.items()) or "none (the template set)"


BASE_CHANGES = [
    "every fixture is rebuilt from a new template set; each case's edits are the mixer-values-v1 edits, unchanged",
    "track order MIDI, audio, return (was audio, MIDI, return); track Ids 1, 2 and 3 (were 11, 12 and 13)",
    "each track gains Name (MIDI: Lead/Lead; audio: empty/2-Audio; return: empty/A-Return; main: empty/Main), Color, "
    "AutomationEnvelopes with an empty list (main: one-event tempo and time-signature envelopes), TrackGroupId -1 "
    "(not on main) and AudioOutputRouting (AudioOut/Main; main: AudioOut/External/S0)",
    "MIDI and audio tracks gain a session clip list (MainSequencer) and a FreezeSequencer list with two empty clip "
    "slots each; MIDI, audio, return and main tracks gain an empty device list (DeviceChain/DeviceChain/Devices)",
    "each mixer gains On (true) as its first child; each value element with a Manual child gains an AutomationTarget "
    "with an Id, all but Speaker a MidiControllerRange (volume 0.0003162277571 to 1.99526238, sends 0.0003162277571 "
    "to 1, pans and crossfader -1 to 1, crossfade assignment 0 to 2) and all but Speaker and CrossFadeState a "
    "ModulationTarget; the main mixer gains Tempo (120) and TimeSignature (201) before CrossFade",
    "LiveSet gains NextPointeeId 67 (pointee Ids 1 to 66), SendsPre with one SendPreBool Id 0 false, two scenes, "
    "Transport (loop off, start 0, length 8, position 0), GlobalQuantisation 4 and AutoQuantisation 0",
    "indentation is one tab per level (was two spaces); XML declaration, envelope attributes, ASCII text, LF line "
    "endings and the final newline unchanged; mixer value texts unchanged",
]
CHANGES = [
    "fixtures: all 37 rebuilt as complete Live Sets from the template set (fixture_changes); case records "
    "MIXER-VALUES-001 to 037 unchanged; no expectation changed",
    "preconditions: the statement that set content absent from a fixture cannot change a judged outcome is withdrawn; "
    "every fixture holds the template set's structure, and documents with another structure have no expectation",
    "REQ-MIXER-VALUES-005 released in part: both fader curves and both conversions as computed values at the listed "
    "inputs, and the exact round trip for seven curve points; cases 038 to 064",
    "REQ-MIXER-VALUES-013 released in part: pan-law gains as computed values for w and v of 0 or 1 at the listed "
    "inputs; cases 065 to 073",
    "REQ-MIXER-VALUES-014 released in part: levels of the seven crossfade curves at seven positions as computed "
    "values; cases 074 to 080; REQ-MIXER-VALUES-009 now points to it for the curve levels",
    "REQ-MIXER-VALUES-008: the On/Off rule is also supported by extracted execution; cases 001 and 030 keep their "
    "records and the static-derived label",
    "provenance: the extracted-execution label is new and carried by every new case; its definition names what ran "
    "and what did not; stated assumptions added for it",
    "representation: action compute with function, inputs and per-function comparators; open cases unchanged",
    "comparison obligation: each fixture is the set itself; computed cases have no observation channel in the "
    "original application",
    "exclusions: REQ-005, 013 and 014 move from unreleased to partial and their remainders are listed; added: "
    "documents whose structure differs from the template set, computed inputs other than those listed, the meaning of "
    "SendPreBool, where and when the audio path applies the computed gains, whether a set with another structure opens",
]


def manifest_meta(fixture_changes):
    m = json.loads((V1PKG / "manifest.json").read_text())  # released v1 wording, reviewer corrections included
    m.update({"release_date": None, "files": [], "review": {"status": "pending", "reviewers": [], "date": None,
                                                           "findings": [], "disposition": None, "record": None}})
    s = m["partial_requirement_scopes"]
    s[R + "005"] = ("Volume and send fader curves (101 points each) and the position-to-gain and gain-to-position "
                    "conversions as computed values at the listed inputs only; exact round trip at the seven listed "
                    "curve points only; no fader, control or audio binding")
    s[R + "008"] = "Track switch Boolean with text On and Off (static-derived; also extracted execution); SoloSink meaning not released"
    s[R + "009"] = s[R + "009"].replace("curve shapes not released", "curve levels only as released in REQ-MIXER-VALUES-014")
    s[R + "013"] = ("Pan-law gain matrix as computed values for w and v each 0 or 1 at the listed inputs only; which w "
                    "and v the audio path supplies, ramps and application to audio not released")
    s[R + "014"] = ("Levels of the seven crossfade curves at positions -1, -0.5, -0.25, 0, 0.25, 0.5 and 1 as computed "
                    "values; the crossfader-to-position mapping, assignment, application to audio and ramps not released")
    m["partial_requirement_scopes"] = dict(sorted(s.items()))
    m.update({
        "release_id": "mixer-values-v2", "release_status": "staged candidate; not reviewed; not released",
        "specification": {"id": "SPEC-MIXER-VALUES", "parent_revision": 4, "release_revision": 4},
        "unreleased_requirements": [R + n for n in ("010", "011", "012", "015")],
        "fixture_origin": ("independently authored complete minimal Live Sets from one template set; no shipped file "
                           "content or program code; computed cases have no fixture"),
        "supersedes": "mixer-values-v1", "case_count": 80,
    })
    m["compatibility_dimensions"].update({
        "computed-values": ("extracted-execution fader-curve conversions, pan-law gains and crossfade curve levels at the "
                            "listed inputs; no observation channel in the original application; reference execution not-run"),
        "audio": "excluded (REQ-MIXER-VALUES-011 and 012; application of the computed gains of 005, 013 and 014)",
        "behavior": "editing, fader positions shown and controller mapping excluded",
    })
    m["expectation_provenance_labels"] = {
        v1.PROV: "derived from evidence reviewed before sanitization",
        XLABEL: ("the original program's x86_64 code that computes the value ran on the case's inputs, on a Linux x86_64 "
                 "host with glibc in place of the macOS system libraries (base-10 exponential and cosine); nothing that "
                 "supplies these inputs from a document, a control or the audio path ran, and nothing that applies "
                 "the results to audio"),
    }
    m["stated_assumptions"] = [
        "Static-derived (carried): a mixer number written as plain decimal text is read as the nearest binary32 number; "
        "a code's name is its list entry; some display shows the value texts, computed from the value as read; the "
        "base-10 logarithm may differ in the last binary32 digit, so inputs near a text boundary have no expectation.",
        "The macOS arm64 build computes these values as the x86_64 build does, within each case's comparison. Its fused "
        "multiply-adds can change the last binary32 digit of the Dipped and Intermediate levels, of the pan-law gains "
        "(through binary64 intermediate results only) and of the three curve points next to the bottom of each fader "
        "curve; the comparisons cover these, and MIXER-VALUES-051, which uses one of those points, moves by less than "
        "1e-8 for a one-step change. All extracted-execution cases depend on it.",
        "The reference's base-10 exponential and cosine are within one binary32 step of glibc's at these inputs; the "
        "comparisons allow one step.",
        "The round-trip cases (MIXER-VALUES-058 to 064) compare exactly. They assume that the reference's base-10 "
        "exponential gives each of the curve points involved as the binary32 value nearest to the exact result, as the "
        "glibc run did; each exact result lies at least 0.16 of a binary32 step from a rounding midpoint, so an "
        "exponential that errs by less than 0.66 of a step gives the same points.",
    ]
    ex = m["exclusions"]
    ex["inputs_without_expectation"] = [e for e in ex["inputs_without_expectation"] if not e.startswith("other envelopes")] + [
        "documents whose structure differs from the template set other than in the mixer value texts the cases change, "
        "including another number of tracks, scenes, clip slots, send holders or SendsPre items, a SendPreBool other "
        "than false, and added clips, devices or envelopes",
        "computed inputs other than those listed in the cases: other positions, gains, pan-law inputs (including w or v "
        "other than 0 and 1) and crossfade positions; round trips of gains other than the seven listed",
        "other envelopes, format versions, compressed containers and document kinds; host locales whose decimal "
        "separator is not '.'",
    ]
    ex["behavior"] = [
        "what is written on save (REQ-MIXER-VALUES-010)",
        "the gains the audio path computes from stored values and where and when it applies them: the volume and send "
        "gain and silence limit (REQ-MIXER-VALUES-011, 012), which w and v feed the pan law, the crossfade factor of "
        "an assigned track, ramps and rendered audio",
        "out-of-range and alternative stored values (REQ-MIXER-VALUES-015)",
        "fader positions shown, and the mapping of controllers and faders to the conversions of REQ-MIXER-VALUES-005",
        "which crossfader end favours A or B, crossfade levels at other positions",
        "which part of the user interface shows which text, and any other form of the same value, such as digits "
        "without the unit or without -inf",
        "editing after opening, including text entry, keys, mouse, remote control and MIDI; creating tracks and the "
        "values of new mixers and send holders; undo",
        "the meaning of EnabledByUser, SoloSink and SendPreBool; the return mixer's own send; whether the cue volume is "
        "the preview level; crossfader value text",
        "whether a set with another structure opens; the rules that decide it",
    ]
    m["supersession"] = {
        "relationship": ("replaces mixer-values-v1: every mixer-values-v1 clause and case record is carried with the same "
                         "expectations, and its fixtures are replaced by complete sets; mixer-values-v1 stays "
                         "immutable, but its fixtures lack set content whose absence has an unknown effect on opening"),
        "superseded_manifest_sha256": V1_MANIFEST_SHA,
        "restated_cases": "MIXER-VALUES-001 to 037: case records identical to mixer-values-v1; fixture files rebuilt",
        "changes": CHANGES, "fixture_changes": fixture_changes,
    }
    m["files"] = m.pop("files")  # keep the inventory last
    return m


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    for old in (STAGE / "fixtures").glob("*"):
        old.unlink()
    carried = v1_records()
    assert [c["id"] for c in carried] == [cid(c[0]) for c in v1.CASES]
    per_fixture = {}
    for rec, (n, _, _, _, changes, _, _) in zip(carried, v1.CASES):
        (STAGE / rec["input"]).write_bytes(doc(changes))
        per_fixture[rec["input"]] = {"mixer_values_v1_sha256": v1.sha((V1PKG / rec["input"]).read_bytes()),
                                     "case_edits": edits_text(changes)}
    cases = carried + new_records()
    head = json.loads((V1PKG / "cases.json").read_text())
    head.update({"scope": "mixer-values-v2 partial requirement clauses only (see spec.md)",
                 "status": "staged candidate; not reviewed; not released",
                 "fixture_origin": ("Independently authored complete minimal Live Sets from one template set; no "
                                    "shipped file copied or excerpted; computed cases have no fixture"),
                 "oracle_status": ("Static-derived and extracted-execution expectations (label per case); neither the "
                                   "reference application nor a candidate executed"),
                 "cases": cases})
    head["representation"].update({
        "compute": "action compute: function and inputs in the compute field; no input fixture (see spec.md)",
        "computed": ("gain, position, gains (L->L, L->R, R->L, R->R) or levels (position, level) as binary32 numbers; "
                     "comparator per case"),
    })
    (STAGE / "cases.json").write_text(json.dumps(head, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(
        manifest_meta({"template_set": BASE_CHANGES, "per_fixture": per_fixture}), indent=1) + "\n")
    print(len(cases), "cases staged")



if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    else:  # seal and verify live in seal_mv2.py (checks, models, traceability)
        import seal_mv2
        print(json.dumps(seal_mv2.verify(sys.argv[2]), indent=1)) if cmd == "verify" else seal_mv2.seal()
