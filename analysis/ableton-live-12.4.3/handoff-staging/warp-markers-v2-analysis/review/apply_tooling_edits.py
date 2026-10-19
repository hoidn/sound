"""Reviewer's edits to the author's warp-markers-v2 tooling (analyst side; never shipped).

usage: python3 -I -B apply_tooling_edits.py      (idempotent; each edit must match exactly once or be applied)
Narrowings of the review: (RVW2-01) both device lists of the base set emptied, as in the live-set-structure-v1
review, and WARP-MARKERS-018 withdrawn with REQ-001 clause 2 and REQ-004, since device placement is open
(Q-022); (RVW2-02) REQ-009 unreleased; (RVW2-03) extracted-execution label clarified; (RVW2-04) stated
assumption 8; (RVW2-05) combined failures of an add. check_v2.py and fixture_checks.py are made to key by
case ID (the withdrawn ID leaves a gap) and to compare base.xml with T11-MIN minus its devices.
"""
from pathlib import Path

A = Path(__file__).resolve().parents[1]


def edit(name, pairs):
    p = A / name
    t = p.read_text()
    for old, new in pairs:
        if new in t and old not in t:
            continue
        assert t.count(old) == 1, (name, old[:80])
        t = t.replace(old, new)
    p.write_text(t)


edit("build_v2.py", [
    ('''DEVICES_PATH = ["LiveSet", "Tracks", "MidiTrack", "DeviceChain", "DeviceChain", "Devices"]
''', ''),
    ('''SIMPLER_FIELDS = [("WarpMode", "0"), ("GranularityTones", "30"), ("GranularityTexture", "65"),
                  ("FluctuationTexture", "25"), ("ComplexProFormants", "100"), ("ComplexProEnvelope", "128"),
                  ("TransientResolution", "6"), ("TransientLoopMode", "2"), ("TransientEnvelope", "100"),
                  ("IsWarped", "false")]
''', ''),
    ('''    kid(clip, "WarpMarkers")[2][:] = markers(M1)
    return root
''', '''    kid(clip, "WarpMarkers")[2][:] = markers(M1)
    # review RVW2-01 (device placement is open, Q-022): both device lists emptied, as the live-set-structure-v1
    # review did for T11-MIN; their targets 67 and 68 go with them, so NextPointeeId is 67 (largest target Id 66)
    for track in ("MidiTrack", "AudioTrack"):
        at(root, ["LiveSet", "Tracks", track, "DeviceChain", "DeviceChain", "Devices"])[2][:] = []
    setv(kid(root, "LiveSet"), "NextPointeeId", 67)
    return root
'''),
    ('''def simpler(root):
    """The MIDI track's instrument replaced by a Simpler whose one sample part has an empty marker list."""
    devices = at(root, DEVICES_PATH)
    on = kid(kid(devices, "UltraAnalog"), "On")  # keeps the base's pointee Id
    swp = mf.el("SampleWarpProperties", None, mf.el("WarpMarkers"), *[mf.v(t, x) for t, x in SIMPLER_FIELDS])
    player = mf.el("Player", None, mf.el("MultiSampleMap", None, mf.el(
        "SampleParts", None, mf.el("MultiSamplePart", {"Id": "0"}, swp))))
    devices[2][:] = [mf.el("OriginalSimpler", {"Id": "0"}, on, player)]


''', ''),
    ('''    "simpler-empty-markers.xml": fixture(simpler),
''', ''),
    ('''    cases = v1_cases() + [case_json(*c) for c in NEW]
    assert [c["id"] for c in cases] == [cid(n) for n in range(1, 65)]''',
     '''    # review RVW2-01: WARP-MARKERS-018 (a Simpler sample part) is withdrawn; its ID stays unused
    cases = [c for c in v1_cases() if c["id"] != cid(18)] + [case_json(*c) for c in NEW]
    assert [c["id"] for c in cases] == [cid(n) for n in range(1, 65) if n != 18]'''),
    ('''"paths": "relative to /Ableton/LiveSet; the clip is the only AudioClip; the sample part is the only SampleWarpProperties (one fixture)",''',
     '''"paths": "relative to /Ableton/LiveSet; the clip is the only AudioClip",'''),
    ('''        "children of AudioClip or SampleWarpProperties other than those the fixtures carry, other child orders, repeated children",
        "any change to the fixtures' context: the document outside the clip's warp children and marker list and the sample part's children, including the clip's sample reference, and the WAV file",
        "scripting arguments that are not finite or have magnitude 1,000,000 or more; a move on a list of fewer than three markers; a call that breaks more than one rule",''',
     '''        "children of AudioClip other than those the fixtures carry, other child orders, repeated children",
        "any change to the fixtures' context: the document outside the clip's warp children and marker list, including the clip's sample reference, and the WAV file; any device in a device list (every device list of the fixtures is empty), including a Sampler or Simpler and its sample parts",
        "scripting arguments that are not finite or have magnitude 1,000,000 or more; a move on a list of fewer than three markers; a call that breaks more than one rule, except an add_warp_marker call, which the first failing check of REQ-015 clauses 1 to 5 decides",'''),
    ('''        "an audio clip whose marker list is empty (REQ-004); one-marker,''',
     '''        "an empty marker list, in an audio clip or a sample part (REQ-004); one-marker,'''),
    ('''        "which sample position plays at a given beat for a warped clip (REQ-009); how a clip that is not warped plays, beyond the statement of REQ-009 clause 1; arrangement clips; the audio output of every warp mode",
        "the default WarpMode of an audio clip or sample part and the default warp mode preference; sample-part defaults",''',
     '''        "playback (REQ-009): which sample position plays at a given beat, whether a clip that is not warped uses its warp markers, arrangement clips; the audio output of every warp mode",
        "the default WarpMode of an audio clip and the default warp mode preference",
        "Sampler and Simpler sample parts: where they store warp state (REQ-001 clause 2), their marker lists (REQ-004), codes, settings and defaults; any device in a device list",'''),
    ('''    "fixtures: every XML document rebuilt as a complete Live Set (the base set of spec.md) with the warp-markers-v1 change of its case;''',
     '''    "fixtures: every XML document rebuilt as a complete Live Set (the base set of spec.md, whose device lists are empty) with the warp-markers-v1 change of its case;'''),
    ('''    "cases 007 and 008 now isolate the number-text refusal: their v1 documents were also refused for their structure",''',
     '''    "case WARP-MARKERS-018 withdrawn, with REQ-001 clause 2 and REQ-004: its document needs a Simpler in a track's device list, and whether the target build accepts a device there is not established; simpler-empty-markers.xml removed",
    "cases 007 and 008 now isolate the number-text refusal: their v1 documents were also refused for their structure",'''),
    ('''    "REQ-009 partially released as an ungraded statement: a session audio clip that is not warped does not use its warp markers when it plays",''',
     '''    "REQ-009 stays unreleased, as in warp-markers-v1: no case of this release can observe playback",'''),
    ('''stated assumptions extended to the sample rate and the arm64 build; carried records unchanged",''',
     '''stated assumptions extended to the sample rate, the marker list a conversion uses and the arm64 build; the carried records unchanged",'''),
    ('''the fixtures' context, the structure rules and sample resolution newly excluded",''',
     '''the fixtures' context, the structure rules, sample resolution, device lists and Sampler and Simpler sample parts newly excluded",'''),
])

edit("v2_meta.py", [
    ('''    18: ("WMK-007 narrowed to one Simpler sample part", ["swppostload", "schema", "shipped", "t11min"], ["I3"]),
''', ''),
    ('''    "001.2": ("Sampler/Simpler list and settings in SampleWarpProperties", "D", ["schema", "shipped"], []),
''', ''),
    ('''    "004.1": ("empty sample-part list not refused, held empty", "S; D", ["swppostload", "shipped"], ["I3"]),
''', ''),
    ('''    "009.1": ("a session clip that is not warped does not use its markers in playback (statement, no case)", "S",
              ["t13unwarped"], []),
''', ''),
    ('''UNRELEASED = ["REQ-WARP-MARKERS-005", "REQ-WARP-MARKERS-006", "REQ-WARP-MARKERS-014"]''',
     '''UNRELEASED = ["REQ-WARP-MARKERS-004", "REQ-WARP-MARKERS-005", "REQ-WARP-MARKERS-006", "REQ-WARP-MARKERS-009",
              "REQ-WARP-MARKERS-014"]  # review: 004 (RVW2-01) and 009 (RVW2-02) added'''),
    ('''"AudioClip warp children and their empty single-Value form; Sampler/Simpler list and settings in SampleWarpProperties; FluctuationTexture name; IsWarped true/false",''',
     '''"AudioClip warp children and their empty single-Value form; FluctuationTexture name; IsWarped true/false",'''),
    ('''    "REQ-WARP-MARKERS-004": "Empty marker list of a sample part not refused",
''', ''),
    ('''    "REQ-WARP-MARKERS-009": "Statement only, no case: a session audio clip that is not warped does not use its warp markers when it plays",
''', ''),
    ('''    PROV_X: "the deciding binary64 values of the case (the conversion result, or the rounded beat and the beat bounds "
            "that decide the outcome) were computed by the original program's x86_64 code for this case's inputs, run "
            "on a Linux x86_64 host outside the application; the macOS arm64 build is inferred to compute the same; "
            "opening, the call's other checks and the sample rate are static-derived",''',
     '''    PROV_X: "the deciding binary64 values of the case (the conversion result, or the rounded beat and the beat bounds "
            "that decide the outcome) were computed by the original program's x86_64 code for this case's inputs, run "
            "on a Linux x86_64 host outside the application; for a conversion, that code computed the step between "
            "seconds and beats, and the division of a position in frames by the sample rate and the multiplication "
            "of a result by it are static-derived and exact for every case with this label; the grid rounding ran "
            "in another part of the original program that rounds a beat with the same operations as the add and the "
            "marker lookup (static-derived); the macOS arm64 build is inferred to compute the same; opening, the "
            "comparisons of the deciding values, the call's other checks and the sample rate are static-derived",'''),
    ('''    "The base set opens in the target build. Its structure follows static-derived rules, which assume that a MIDI track's device list accepts the base set's instrument (in case 018, the Simpler) and an audio track's device list its effect (every case).",''',
     '''    "The base set, whose device lists are empty, opens in the target build. Its structure follows static-derived rules (every case).",'''),
    ('''    "The macOS arm64 build computes the conversions, the grid rounding and the beat bounds with the same binary64 operations as the x86_64 build (cases 039 to 060).",
]''', '''    "The macOS arm64 build computes the conversions, the grid rounding and the beat bounds with the same binary64 operations as the x86_64 build (cases 039 to 060).",
    "A conversion made right after opening uses the marker list held after opening (cases 039 to 051).",
]'''),
    ('''            "playback": "excluded, except the ungraded statement of REQ-WARP-MARKERS-009",''',
     '''            "playback": "excluded",'''),
    ('''            "relationship": "superset in effect: carries every warp-markers-v1 case record unchanged with rebuilt fixtures; within warp-markers-v1's scope both give the same expectations; warp-markers-v1 stays immutable, but its fixtures must not be used (the target build refuses 17 of its 18 documents)",''',
     '''            "relationship": "supersedes with one case withdrawn: carries 37 of the 38 warp-markers-v1 case records unchanged with rebuilt fixtures; WARP-MARKERS-018 is withdrawn and has no expectation; for every other case and clause of warp-markers-v1 both give the same expectations; warp-markers-v1 stays immutable, but its fixtures must not be used (the target build refuses 17 of its 18 documents)",'''),
    ('''            "restated_cases": "WARP-MARKERS-001 to 038: case records identical to warp-markers-v1; fixture names and the WAV bytes identical; every XML fixture rebuilt as a complete Live Set",''',
     '''            "restated_cases": "WARP-MARKERS-001 to 017 and 019 to 038: case records identical to warp-markers-v1; fixture names and the WAV bytes identical; every XML fixture rebuilt as a complete Live Set without devices",
            "withdrawn_cases": {"WARP-MARKERS-018": "its document needs a Simpler in a track's device list; whether the target build accepts a device there is not established, so the case has no expectation; REQ-001 clause 2 and REQ-004 are withdrawn with it"},'''),
])

edit("check_v2.py", [
    ('''    v1 = json.loads((ROOT / V1 / "cases.json").read_text())["cases"]
    same = [a["id"] for a, b in zip(v1, cases) if json.dumps(a, indent=1) == json.dumps(b, indent=1)]
    return {"v1_records": len(v1), "identical": len(same), "problems": sorted({c["id"] for c in v1} - set(same))}''',
     '''    v1 = json.loads((ROOT / V1 / "cases.json").read_text())["cases"]
    by_id = {c["id"]: c for c in cases}  # review: keyed by ID; WARP-MARKERS-018 is withdrawn
    same = [a["id"] for a in v1 if a["id"] in by_id and json.dumps(a, indent=1) == json.dumps(by_id[a["id"]], indent=1)]
    withdrawn = sorted({c["id"] for c in v1} - set(by_id))
    return {"v1_records": len(v1), "identical": len(same), "withdrawn": withdrawn,
            "problems": sorted({c["id"] for c in v1} - set(same) - {"WARP-MARKERS-018"})
            + ([] if withdrawn == ["WARP-MARKERS-018"] else ["withdrawn set"])}'''),
    ('''    for n, c in enumerate(cases, 1):
        rules = ("x", "exact") if n <= 38 else ("x",)''',
     '''    for c in cases:
        n = int(c["id"][-3:])  # review: by ID, not position
        rules = ("x", "exact") if n <= 38 else ("x",)'''),
    ('''    differs = sorted(k for k, v in exact.items() if not agrees(v, cases[int(k[-3:]) - 1]["expected"],
                                                               cases[int(k[-3:]) - 1].get("call")))''',
     '''    by_id = {c["id"]: c for c in cases}
    differs = sorted(k for k, v in exact.items() if not agrees(v, by_id[k]["expected"], by_id[k].get("call")))'''),
    ('''                                  "provenance": cases[n - 1]["expectation_provenance"]}''',
     '''                                  "provenance": {c["id"]: c for c in cases}[B.cid(n)]["expectation_provenance"]}'''),
])

edit("fixture_checks.py", [
    ('''    t11 = (ROOT / T11 / "fixtures/T11-MIN.xml").read_text()''',
     '''    t11 = (ROOT / T11 / "fixtures/T11-MIN.xml").read_text()
    # review RVW2-01: base.xml is T11-MIN without its two devices (and NextPointeeId 67), plus the clip change
    t11 = re.sub(r"<Devices>\\n.*?</Devices>", "<Devices />", t11, flags=re.S)
    assert t11.count('<NextPointeeId Value="69" />') == 1
    t11 = t11.replace('<NextPointeeId Value="69" />', '<NextPointeeId Value="67" />')'''),
])
print("tooling edits applied")
