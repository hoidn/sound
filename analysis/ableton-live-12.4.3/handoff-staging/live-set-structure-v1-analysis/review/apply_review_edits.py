"""Reviewer's edits to the live-set-structure-v1 candidate (analyst side; never shipped).

usage: python3 -I -B apply_review_edits.py tooling   # lss_cases.py, build_lss.py (then: build_lss.py build)
       python3 -I -B apply_review_edits.py text      # spec.md, README.md, AGENTS.md, cases.json status
       python3 -I -B apply_review_edits.py text-fixups   # spec.md: second pass (term list, line wrapping)
       python3 -I -B apply_review_edits.py text-fixups-2 # spec.md: keyed state values compare by listed track
Each edit replaces text that must occur exactly once; a second run fails rather than editing twice.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AN = HERE.parent
PKG = AN.parent / "live-set-structure-v1"


def edit(path, pairs):
    t = path.read_text()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, f"{path.name}: {n} occurrences of {old[:70]!r}"
        t = t.replace(old, new)
    path.write_text(t)
    print(f"{path.name}: {len(pairs)} edits")


TOOLING = {
    AN / "lss_cases.py": [
        ('def e_return_first(r):',
         'def device_free(r):\n'
         '    """Review narrowing (device placement is an open question): both device lists of T11-MIN are emptied.\n'
         '    Their two targets (Ids 67 and 68) go with them, and NextPointeeId becomes 67, one more than the largest\n'
         '    remaining target Id (66), as REQ-015 clause 1 describes a written set."""\n'
         '    for tag in ("MidiTrack", "AudioTrack"):\n'
         '        clear(trk(r, tag).find("DeviceChain/DeviceChain/Devices"))\n'
         '    ls(r).find("NextPointeeId").set("Value", "67")\n\n\n'
         'def e_return_first(r):'),
        ("T11-MIN's own rules: next target Ids 69, 70; NextPointeeId 71", "T11-MIN's own rules: next target Ids 67, 68; NextPointeeId 69"),
        ("    ids.n = 68\n", "    ids.n = 66\n"),
        ('action="open", assumptions=(DP,), prov="static"', 'action="open", assumptions=(), prov="static"'),
        ('basis A6 only (A4 is not needed to open; its check is case 031)"',
         'basis A6 only (A4 is not needed to open; its check is case 031); review: the devices are removed from '
         'T11-MIN and every fixture, so no case rests on A6 (open in Q-022)"'),
        ('with target Ids 69 and 70 "\n         "and NextPointeeId 71"', 'with target Ids 67 and 68 "\n         "and NextPointeeId 69"'),
        ('case(25, "LSS-020", "NextPointeeId 68", "refusal", ["015"],\n'
         '         e_set(lambda r: ls(r).find("NextPointeeId"), "Value", "68"), REF, ["nextpointee"],\n'
         '         check={"refusals": [R015n]}, assumptions=()),',
         'case(25, "LSS-020", "NextPointeeId 66, equal to the largest target Id", "refusal", ["015"],\n'
         '         e_set(lambda r: ls(r).find("NextPointeeId"), "Value", "66"), REF, ["nextpointee"],\n'
         '         "review: 66, the largest target Id once the devices are removed (68 in the draft)",\n'
         '         check={"refusals": [R015n]}, assumptions=()),'),
        ('opens(audio_clip_file="Samples/T11-tone.wav"), ["resolution", "fileref-fields"],\n         assumptions=(DP, SF)),',
         'opens(audio_clip_file="Samples/T11-tone.wav"), ["resolution", "fileref-fields"],\n         assumptions=(SF,)),'),
        ('    DP: "The original accepts an Analog instrument (UltraAnalog) as the only device in a MIDI track\'s device "\n'
         '        "list and an Amp effect (Amp) as the only device in an audio track\'s device list, in T11-MIN\'s form",\n', ''),
        ('"Tracks in display order; refused without a player track or with a player track after a return;',
         '"Tracks in display order; refused without an audio, MIDI or group track, or with one of those after a return track;'),
        ('"Element forms; children matched by name;', '"Element forms (compound, value, list, array); children matched by name;'),
        ('a repeated child of a non-list element,', 'a repeated child of a compound element,'),
        ('fallback to Path for 0, 1, 2, 6 and not for 3, 5, 7; a missing sample does not refuse"',
         'fallback to Path for 0 and 1; a missing sample does not refuse"'),
        ('"Reference minimal set T11-MIN opens with the listed content (assumption); element status table"',
         '"Reference minimal set T11-MIN, whose device lists are empty, opens with the listed content; element status table"'),
        ('stored length or rate differing from the file; RelativePathType 2 to 7 beyond whether Path is used",',
         'stored length or rate differing from the file; RelativePathType 2 to 7",'),
        ('"device classes and positions other than T11-MIN\'s two",', '"any device in a device list (every device list of the fixtures is empty)",'),
        ('"fixture": "make_fixture.py; out/schema-check-fixture.jsonl (no deviation; all structure measurements as required)",',
         '"fixture": "make_fixture.py; out/schema-check-fixture.jsonl (no deviation; all structure measurements as required); '
         'review: device lists emptied (lss_cases.device_free); shipped sets hold empty device lists on 4 MIDI and 21 audio '
         'tracks (out/documents.json chain_devices)",'),
        ('"new-send": "wiki/specs/mixer-values.md REQ-MIXER-VALUES-003 (new send 0.0003162277571);',
         '"new-send": "wiki/research/mixer-values.md#constructor-defaults-and-ranges (send holder 0x102658f54: Send '
         '0.0003162277571, s9-0002); appended holders 0x10271d824 -> 0x102659a78 -> 0x102658f54 (reviewer check, '
         'review/review-checks.txt); draft wiki/specs/mixer-values.md REQ-MIXER-VALUES-003 (unreleased there);'),
        ('"A6": "SPEC-LIVE-SET-STRUCTURE A6: bundled device classes accepted in track chains (open; listed in Q-022)",',
         '"A6": "SPEC-LIVE-SET-STRUCTURE A6: bundled device classes accepted in track chains (open; listed in Q-022); not '
         'used: the review removed both devices from T11-MIN and every fixture",'),
    ],
    AN / "build_lss.py": [
        ("The XML must equal that packet's fixtures/T11-MIN.xml byte for byte;",
         "The XML must equal that packet's fixtures/T11-MIN.xml byte for byte after the review's narrowing\n"
         "(lss_cases.device_free: both device lists emptied, NextPointeeId 67);"),
        ('    base = t11_min(sample)\n    root = ET.fromstring(base)\n    assert text(root) == base, "ElementTree round trip changes T11-MIN"\n',
         '    packet = t11_min(sample)\n    root = ET.fromstring(packet)\n    assert text(root) == packet, "ElementTree round trip changes T11-MIN"\n'
         '    lc.device_free(root)  # review narrowing: no fixture holds a device\n    base = text(root)\n'),
        ('    if texts[MIN_ALS] != (T11 / "fixtures/T11-MIN.xml").read_bytes():\n'
         '        problems["T11-MIN"] = "decoded XML differs from the t11 packet\'s T11-MIN.xml"\n',
         '    packet = ET.fromstring((T11 / "fixtures/T11-MIN.xml").read_bytes())\n'
         '    lc.device_free(packet)\n'
         '    if texts[MIN_ALS] != text(packet):\n'
         '        problems["T11-MIN"] = "decoded XML differs from the t11 packet\'s T11-MIN.xml with the device lists emptied"\n'),
        ('fixed.find("LiveSet/NextPointeeId").set("Value", "69")', 'fixed.find("LiveSet/NextPointeeId").set("Value", "67")'),
        ('rules measured with Value 69 restored"', 'rules measured with Value 67 restored"'),
        ('"devices": "excluded (REQ-LIVE-SET-STRUCTURE-012); two placements under a stated assumption",',
         '"devices": "excluded (REQ-LIVE-SET-STRUCTURE-012); every device list of the fixtures is empty",'),
    ],
}

SPEC = [
    ("**Status: unreviewed candidate.** It is not an implementation input until a\n"
     "separate review approves it and it is published as a release.",
     "**Status: reviewed local release.** A separate review approved the clauses\n"
     "below with the narrowing recorded in [the review disposition](REVIEW.md).\n"
     "Implementation requires a fresh, restricted implementation workspace."),
    ("remains the authority for a later comparison. Three derived steps rest on the",
     "remains the authority for a later comparison. Two derived steps rest on the"),
    ('for example `<NextPointeeId Value="69" />` |',
     'for example `<NextPointeeId Value="67" />` |\n'
     '| Array | An element whose children are items of one name without an `Id`. In the fixtures only `KeyTrack/Notes`, whose items are `MidiNoteEvent` elements |'),
    ("   parent or as a value element; or a list. Which values are attributes\n   follows the fixtures,",
     "   parent or as a value element; a list; or an array. Which values are\n   attributes follow the fixtures,"),
    ("   - an element that is not a list holds two children of the same name. The\n",
     "   - a compound element holds two children of the same name (lists and\n"
     "     arrays are not compound elements). The\n"),
    ("2. The set is refused when `Tracks` holds no player track. This includes an\n",
     "2. The set is refused when `Tracks` holds no player track, that is no audio,\n"
     "   MIDI or group track. This includes an\n"),
    ("   other bases; this release states only whether they use `Path`\n   (REQ-LIVE-SET-STRUCTURE-009 clause 2).",
     "   other bases; this release states nothing more about them."),
    ("2. When the relative path gives no existing file, `RelativePathType` 0, 1, 2\n"
     "   and 6 use the absolute `Path`, if it is not empty, without comparing the\n"
     "   file with the stored size and checksum. `RelativePathType` 3, 5 and 7 do not\n"
     "   use `Path`.",
     "2. When the relative path gives no existing file, `RelativePathType` 0 and 1\n"
     "   use the absolute `Path`, if it is not empty, without comparing the file\n"
     "   with the stored size and checksum. Whether the codes 2 to 7 use `Path` is\n"
     "   outside this release."),
    ("Under the device-placement assumption, T11-MIN opens and holds the content",
     "T11-MIN opens and holds the content"),
    ("- Envelope as in the preconditions; `NextPointeeId` 69; 68 target elements\n  with Ids 1 to 68.",
     "- Envelope as in the preconditions; `NextPointeeId` 67; 66 target elements\n  with Ids 1 to 66."),
    ("velocity 100. Its device list holds\n  `UltraAnalog Id=\"0\"` with only its `On` parameter. Its track envelope sets",
     "velocity 100. Its device list is\n  empty. Its track envelope sets"),
    ("`DefaultDuration` 44100 and\n  `DefaultSampleRate` 44100. Its device list holds `Amp Id=\"0\"` with only its\n  `On` parameter.",
     "`DefaultDuration` 44100 and\n  `DefaultSampleRate` 44100. Its device list is empty."),
    ("- The return track has an empty device list.", "- The return and main tracks also have empty device lists."),
    ("| `Tracks` with at least one `MidiTrack` or `AudioTrack`, return tracks last | Required |",
     "| `Tracks` with at least one audio, MIDI or group track, return tracks last | Required |"),
    ("| Device list content | Write | Only the two placements of T11-MIN have an expectation, under the device-placement assumption |",
     "| `DeviceChain/DeviceChain/Devices`, empty | Write | A device in a device list has no expectation |"),
    ("| `device-placement` | The original accepts an Analog instrument (`UltraAnalog`) as the only device in a MIDI track's device list, "
     "and an Amp effect (`Amp`) as the only device in an audio track's device list, in the element form of T11-MIN. Live's shipped "
     "documents place these devices only inside racks, in lists of the same kind | Every case whose input holds these devices and "
     "whose expected outcome is `opens` |\n", ""),
    ("- device classes and positions other than the two of T11-MIN, including an\n  instrument on an audio track and two instruments in one list;",
     "- any device in a device list;"),
    ("`RelativePathType` 2 to 7 apart from REQ-LIVE-SET-STRUCTURE-009\n  clause 2;", "`RelativePathType` 2 to 7;"),
    ("  expects `opens` and rests on the device-placement assumption is", "  expects `opens` is"),
    ("T11-MIN's values, Ids and names are invented. The sample",
     "T11-MIN's values, Ids and names are invented, and its device lists are\nempty. The sample"),
    ("included. Review status is recorded in [the manifest](manifest.json).",
     "included. Review status is recorded in [the manifest](manifest.json) and\n[the review disposition](REVIEW.md)."),
]

README = [
    ("**Unreviewed candidate.** This package is not an implementation input until a\n"
     "separate review approves it and it is published as a release. Read\n"
     "[the contract](spec.md), [the cases](cases.json),\n"
     "[the role instructions](AGENTS.md) and [the manifest](manifest.json).",
     "**Reviewed local release.** Read [the contract](spec.md),\n"
     "[the cases](cases.json), [the role instructions](AGENTS.md),\n"
     "[the manifest](manifest.json) and [the review disposition](REVIEW.md). The\n"
     "stated partial scope, with the narrowing recorded in the review, is approved\n"
     "as a contract for a fresh, restricted implementation workspace. Such a\n"
     "workspace has not been provisioned by this release."),
    ("The package has 34 cases. Their inputs are the generated minimal set T11-MIN,\n",
     "The package has 34 cases. Their inputs are the generated minimal set T11-MIN,\n"
     "whose device lists are empty,\n"),
    ("sample. Three stated assumptions support some of the expectations; the contract\nnames them, and each case lists those it needs.",
     "sample. Two stated assumptions support four of the expectations; the contract\nnames them, and each case lists those it needs."),
]

AGENTS = [
    ("This package is an unreviewed release candidate. Until a separate review\n"
     "approves it and it is published, it is not an implementation input. After\n"
     "publication, application implementation requires a fresh, restricted\n"
     "implementation workspace that contains only permitted materials. Publication\n"
     "does not provision one.",
     "This is a reviewed local release for its explicit partial scope. Application\n"
     "implementation requires a fresh, restricted implementation workspace that\n"
     "contains only permitted materials. Publication does not provision one."),
]

SPEC_FIXUPS_2 = [  # third pass: comparison of keyed state values (found by review_checks.py)
    ("  numbers as numbers, lists element for element. Keys that a case does not\n  list are not judged.",
     "  numbers as numbers, lists element for element. Keys that a case does not\n  list are not judged. For `send_texts` and `automated_parameters`, which are\n"
     "  keyed by track number, only the track numbers a case lists are judged."),
]

SPEC_FIXUPS = [  # second pass, after reading the result of "text"
    ("`ClipSlotList`, `Sends`, `Devices`, `Envelopes`,", "`ClipSlotList`, `Sends`, `Envelopes`,"),
    ("T11-MIN opens and holds the content\nlisted below. The status table states, for each element, what follows from\nthe clauses above.",
     "T11-MIN opens and holds the content listed below. The status table states,\nfor each element, what follows from the clauses above."),
    ("velocity 100. Its device list is\n  empty. Its track envelope sets\n  the volume target (Id 11) to 1 from the start and to 0.5 at beat 4.",
     "velocity 100. Its device list is\n  empty. Its track envelope sets the volume target (Id 11) to 1 from the start\n  and to 0.5 at beat 4."),
    ("  expects `opens` is\n  inconclusive.", "  expects `opens` is inconclusive."),
    ("T11-MIN's values, Ids and names are invented, and its device lists are\nempty. The sample is a generated sine\ntone.",
     "T11-MIN's values, Ids and names are invented, and its device lists are\nempty. The sample is a generated sine tone."),
]

if __name__ == "__main__":
    if sys.argv[1] == "tooling":
        for p, pairs in TOOLING.items():
            edit(p, pairs)
    elif sys.argv[1] == "text":
        edit(PKG / "spec.md", SPEC)
        edit(PKG / "README.md", README)
        edit(PKG / "AGENTS.md", AGENTS)
        c = json.loads((PKG / "cases.json").read_text())
        assert c["status"] == "candidate-unreviewed"
        c["status"] = "released-reviewed"
        (PKG / "cases.json").write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n")
        print("cases.json: status released-reviewed")
    elif sys.argv[1] == "text-fixups":
        edit(PKG / "spec.md", SPEC_FIXUPS)
    elif sys.argv[1] == "text-fixups-2":
        edit(PKG / "spec.md", SPEC_FIXUPS_2)
