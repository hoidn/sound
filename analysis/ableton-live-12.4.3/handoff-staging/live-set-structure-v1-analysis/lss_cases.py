"""Case data for live-set-structure-v1 (analyst side): edits, expectations, isolation declarations,
payload texts for the manifest, and the analyst-only traceability (evidence locators, draft sources).
Imported by build_lss.py. Draft case IDs (LSS-0xx) and analysis assumption IDs (A4-A6) stay here and in
traceability.json; the payload uses release case IDs and behavioral assumption names only.
"""
import copy
import xml.etree.ElementTree as ET

TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"


def cid(n):
    return f"LIVE-SET-STRUCTURE-{n:03d}"


# ---- edits on the parsed T11-MIN tree ----
def ls(r):
    return r.find("LiveSet")


def trk(r, tag):
    return r.find(f"LiveSet/Tracks/{tag}")


def clear(e):
    for c in list(e):
        e.remove(c)


def drop(parent, path):
    parent.remove(parent.find(path))


def insert_after(parent, sibling_tag, el):
    parent.insert(list(parent).index(parent.find(sibling_tag)) + 1, el)


def audio_pan_target(r):
    return trk(r, "AudioTrack").find("DeviceChain/Mixer/Pan/AutomationTarget")


def midi_env_target(r):
    return trk(r, "MidiTrack").find("AutomationEnvelopes/Envelopes/AutomationEnvelope/EnvelopeTarget/PointeeId")


def file_ref(r):
    return trk(r, "AudioTrack").find("DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip/"
                                     "SampleRef/FileRef")


def device_free(r):
    """Review narrowing (device placement is an open question): both device lists of T11-MIN are emptied.
    Their two targets (Ids 67 and 68) go with them, and NextPointeeId becomes 67, one more than the largest
    remaining target Id (66), as REQ-015 clause 1 describes a written set."""
    for tag in ("MidiTrack", "AudioTrack"):
        clear(trk(r, tag).find("DeviceChain/DeviceChain/Devices"))
    ls(r).find("NextPointeeId").set("Value", "67")


def e_return_first(r):
    t = ls(r).find("Tracks")
    ret = t.find("ReturnTrack")
    t.remove(ret)
    t.insert(1, ret)
    for s in t.iter("Sends"):
        clear(s)


def e_second_holder(r):
    import make_fixture as mf  # T11-MIN's own rules: next target Ids 67, 68; NextPointeeId 69
    ids = mf.Ids()
    ids.n = 66
    send, _ = mf.param("Send", "0.0003162277571", ids, ("0.0003162277571", "1"))
    lines = []
    mf.render(mf.el("TrackSendHolder", {"Id": "1"}, send, mf.v("EnabledByUser", "true")), 0, lines)
    trk(r, "AudioTrack").find("DeviceChain/Mixer/Sends").append(ET.fromstring("\n".join(lines)))
    ls(r).find("NextPointeeId").set("Value", str(ids.n + 1))


def e_set(path_fn, attr, value):
    return lambda r: path_fn(r).set(attr, value)


def e_scene_ids(r):
    for s, i in zip(ls(r).find("Scenes"), ("7", "3")):
        s.set("Id", i)


def e_audio_slot_ids(r):
    for s, i in zip(trk(r, "AudioTrack").find("DeviceChain/MainSequencer/ClipSlotList"), ("7", "3")):
        s.set("Id", i)


def e_dup_color(r):
    m = trk(r, "MidiTrack")
    insert_after(m, "Color", copy.deepcopy(m.find("Color")))


def e_no_tracks_element(r):
    drop(ls(r), "Tracks")
    clear(ls(r).find("SendsPre"))


def e_empty_tracks(r):
    clear(ls(r).find("Tracks"))
    clear(ls(r).find("SendsPre"))


def e_return_only(r):
    t = ls(r).find("Tracks")
    for tag in ("MidiTrack", "AudioTrack"):
        drop(t, tag)


def e_last_midi_freeze_slot(r):
    lst = trk(r, "MidiTrack").find("DeviceChain/FreezeSequencer/ClipSlotList")
    lst.remove(list(lst)[-1])


# ---- expectations ----
KINDS = ["midi", "audio", "return"]
CLIPS = [["Two Notes", None], ["Tone", None]]
T11_STATE = {"track_kinds": KINDS, "scene_names": ["Scene 1", "Scene 2"], "session_clips": CLIPS,
             "send_counts": [1, 1, 1]}
OPEN = {"outcome": "opens"}
REF = {"outcome": "refused"}


def opens(**state):
    return {"outcome": "opens", "state": state}


R002 = "REQ-002: no audio, MIDI or group track"
R002o = "REQ-002: player track after a return track"
R006 = "REQ-006: freeze slot count differs from session slot count"
R013 = "REQ-013: more send holders than return tracks"
R015z = "REQ-015: pointee with Id 0 or without Id"
R015n = "REQ-015: NextPointeeId not above the largest pointee Id"
R016d = "REQ-016: duplicate list-item Id (S-cond A5)"
R016n = "REQ-016: negative list-item Id (S-cond A5)"
U013 = "REQ-013 U: SendsPre length differs from the number of return tracks (no load check found)"
DP, LI, SF = "device-placement", "list-item-ids", "sample-folder"


def case(n, src, purpose, kind, reqs, edit, expected, ev, change="as written", setup="with-samples",
         action="open", assumptions=(), prov="static", check=None):
    a = {DP: "A6", LI: "A5", SF: "A4"}
    return {"n": n, "src": src, "purpose": purpose, "kind": kind, "reqs": reqs, "edit": edit, "expected": expected,
            "ev": ev, "change": change, "setup": setup, "action": action, "assumptions": list(assumptions),
            "a": [a[x] for x in assumptions], "prov": prov, "check": check or {}}


CASES = [
    case(1, "LSS-001", "Open the reference minimal set T11-MIN", "positive",
         ["001", "002", "003", "004", "005", "006", "007", "008", "013", "015", "016", "018"], None,
         opens(**T11_STATE), ["fixture", "schema-check", "survey", "walk-tracks", "walk-slots", "holders", "nextpointee"],
         "narrowed: track names, colours and devices are not judged (displayed name U; REQ-012 unreleased); "
         "basis A6 only (A4 is not needed to open; its check is case 031); review: the devices are removed from T11-MIN and every fixture, so no case rests on A6 (open in Q-022)", prov="doc-static"),
    case(2, "LSS-002", "Tracks emptied, and the SendPreBool removed", "refusal", ["002"], e_empty_tracks, REF,
         ["walk-tracks", "open-path"], check={"refusals": [R002]}, assumptions=()),
    case(3, "LSS-005", "Tracks element removed, and the SendPreBool removed", "refusal", ["001", "002"],
         e_no_tracks_element, REF, ["walk-tracks", "song-ctor", "open-path"],
         "SendPreBool also removed, so that no SendsPre-count unknown remains (as in LSS-002)",
         check={"refusals": [R002]}, assumptions=()),
    case(4, "LSS-003", "Audio and MIDI tracks removed; the return track kept", "refusal", ["002"], e_return_only,
         REF, ["walk-tracks", "open-path"], check={"refusals": [R002]}, assumptions=()),
    case(5, "LSS-004", "Return track moved before the audio track, and every Sends list emptied", "refusal",
         ["002"], e_return_first, REF, ["walk-tracks", "holders", "open-path"],
         "Sends emptied: with the return moved, R is 0 and one holder per mixer would be refused first by "
         "REQ-013 (root post-load precedes the walk). SendsPre keeps one item, equal to the number of return "
         "tracks; the checker compares it with R (0) and reports the REQ-013 unknown shape",
         check={"refusals": [R002o], "unknowns": [U013]}, assumptions=()),
    case(6, "LSS-006", "An item FooTrack Id 9 inserted as the first item of Tracks", "refusal", ["001", "002"],
         lambda r: ls(r).find("Tracks").insert(0, ET.Element("FooTrack", {"Id": "9"})), REF,
         ["list-loader", "reader-n1"], "inserted first, not appended, so that R stays 1 for a reader that skipped it",
         check={"deviations": ["unknown-class LiveSet/Tracks/* FooTrack"]}, assumptions=()),
    case(7, "new (REQ-002 grouping clause)", "MIDI track TrackGroupId 7 in a set without group tracks", "refusal",
         ["002"], e_set(lambda r: trk(r, "MidiTrack").find("TrackGroupId"), "Value", "7"), REF,
         ["walk-grouping", "open-path"], "new case", check={"extra": ["REQ-002: grouped track in a set without group tracks"]},
         assumptions=()),
    case(8, "LSS-019", "Audio track Id 5, which is also a target Id of the set", "positive", ["003", "015", "016"],
         e_set(lambda r: trk(r, "AudioTrack"), "Id", "5"), opens(track_kinds=KINDS), ["survey", "list-id-attr"],
         prov="doc-static"),
    case(9, "LSS-016", "Audio track Id 1, equal to the MIDI track's Id", "refusal", ["003", "016"],
         e_set(lambda r: trk(r, "AudioTrack"), "Id", "1"), REF, ["list-loader"], check={"refusals": [R016d]},
         assumptions=(LI,)),
    case(10, "LSS-017", "Audio track Id -1", "refusal", ["016"], e_set(lambda r: trk(r, "AudioTrack"), "Id", "-1"),
         REF, ["list-id-attr"], check={"refusals": [R016n]}, assumptions=(LI,)),
    case(11, "new (REQ-016 non-integer clause)", "Audio track Id a", "refusal", ["016"],
         e_set(lambda r: trk(r, "AudioTrack"), "Id", "a"), REF, ["list-id-attr"], "new case",
         check={"extra": ["REQ-016: list-item Id not an integer: LiveSet/Tracks/AudioTrack"]}, assumptions=(LI,)),
    case(12, "LSS-031", "Unknown child element Foo Value 1 after the MIDI track's Color", "positive", ["001"],
         lambda r: insert_after(trk(r, "MidiTrack"), "Color", ET.Element("Foo", {"Value": "1"})),
         opens(track_kinds=KINDS), ["unknown-child", "reader-n1"],
         "narrowed: the save part (S-cond A7) is not released", check={"deviations": ["unknown-element MidiTrack Foo"]}),
    case(13, "new (REQ-001 duplicate-member clause)", "Second Color element in the MIDI track", "refusal", ["001"],
         e_dup_color, REF, ["reader-n1"], "new case", check={"extra": ["REQ-001: duplicate member MidiTrack/Color"]},
         assumptions=()),
    case(14, "LSS-023", "NextPointeeId written without Value", "refusal", ["001", "015"],
         lambda r: ls(r).find("NextPointeeId").attrib.clear(), REF, ["reader-n1"],
         check={"extra": ["REQ-001: value element without Value: LiveSet/NextPointeeId"]}, assumptions=()),
    case(15, "LSS-029", "MainTrack removed", "missing-element", ["004"], lambda r: drop(ls(r), "MainTrack"),
         opens(tempo=120), ["song-ctor", "tempo-default"],
         "obligation added: factory default set; the value 120 does not distinguish it from T11-MIN's tempo"),
    case(16, "LSS-030", "PreHearTrack removed", "missing-element", ["004"], lambda r: drop(ls(r), "PreHearTrack"),
         opens(track_kinds=KINDS), ["song-ctor"]),
    case(17, "LSS-007", "Audio track's FreezeSequencer removed", "refusal", ["006"],
         lambda r: drop(trk(r, "AudioTrack").find("DeviceChain"), "FreezeSequencer"), REF,
         ["walk-slots", "freeze-empty", "open-path"], check={"refusals": [R006]}, assumptions=()),
    case(18, "LSS-008", "Last freeze slot of the MIDI track removed", "refusal", ["006"], e_last_midi_freeze_slot, REF,
         ["walk-slots", "freeze-empty", "open-path"],
         "changed: removes a freeze slot instead of appending a session slot, which made session slots (3) "
         "differ from scenes (2), the REQ-006 unknown", check={"refusals": [R006]}, assumptions=()),
    case(19, "LSS-011", "Scene Ids changed to 7 and 3", "positive", ["006", "016"], e_scene_ids,
         opens(scene_names=["Scene 1", "Scene 2"]), ["survey", "list-loader"], prov="doc-static"),
    case(20, "LSS-012", "Audio track's session slot Ids changed to 7 and 3", "positive", ["006", "016"],
         e_audio_slot_ids, opens(session_clips=CLIPS), ["survey", "list-loader"], prov="doc-static"),
    case(21, "LSS-013", "MIDI track's Sends emptied", "repair", ["013"],
         lambda r: clear(trk(r, "MidiTrack").find("DeviceChain/Mixer/Sends")),
         opens(send_counts=[1, 1, 1], send_texts={"1": ["-inf dB"]}), ["holders", "new-send"]),
    case(22, "LSS-014", "Second send holder on the audio track, written like the first, with target Ids 67 and 68 "
         "and NextPointeeId 69", "refusal", ["013"], e_second_holder, REF, ["holders"],
         "the holder's two targets get new Ids and NextPointeeId is raised, by T11-MIN's rules",
         check={"refusals": [R013]}, assumptions=()),
    case(23, "LSS-028", "MIDI track envelope's PointeeId changed to 999999", "repair", ["014"],
         e_set(midi_env_target, "Value", "999999"), opens(automated_parameters={"1": 0}), ["dangling"],
         "narrowed: the save and reopen part (S-cond A7) is not released"),
    case(24, "new (REQ-014 PointeeId 0 clause)", "MIDI track envelope's PointeeId changed to 0", "repair", ["014"],
         e_set(midi_env_target, "Value", "0"), opens(automated_parameters={"1": 0}), ["dangling"], "new case"),
    case(25, "LSS-020", "NextPointeeId 66, equal to the largest target Id", "refusal", ["015"],
         e_set(lambda r: ls(r).find("NextPointeeId"), "Value", "66"), REF, ["nextpointee"],
         "review: 66, the largest target Id once the devices are removed (68 in the draft)",
         check={"refusals": [R015n]}, assumptions=()),
    case(26, "LSS-021", "NextPointeeId removed", "refusal", ["015"], lambda r: drop(ls(r), "NextPointeeId"), REF,
         ["nextpointee"], check={"refusals": [R015n]}, assumptions=()),
    case(27, "LSS-022", "NextPointeeId 100000", "positive", ["015"],
         e_set(lambda r: ls(r).find("NextPointeeId"), "Value", "100000"), opens(track_kinds=KINDS), ["nextpointee"]),
    case(28, "LSS-024", "Audio track's Pan AutomationTarget Id 0", "refusal", ["015"],
         e_set(audio_pan_target, "Id", "0"), REF, ["pointee-postload", "preset-flag"], check={"refusals": [R015z]},
         assumptions=()),
    case(29, "LSS-025", "Audio track's Pan AutomationTarget without Id", "refusal", ["015"],
         lambda r: audio_pan_target(r).attrib.clear(), REF, ["pointee-postload", "preset-flag"],
         check={"refusals": [R015z]}, assumptions=()),
    case(30, "LSS-027", "Audio track's Pan AutomationTarget element removed", "missing-element", ["015"],
         lambda r: drop(trk(r, "AudioTrack").find("DeviceChain/Mixer/Pan"), "AutomationTarget"),
         opens(track_kinds=KINDS), ["registration"]),
    case(31, "LSS-032", "T11-MIN opened from a new folder with its Samples folder", "positive", ["008", "009"], None,
         opens(audio_clip_file="Samples/T11-tone.wav"), ["resolution", "fileref-fields"],
         assumptions=(SF,)),
    case(32, "LSS-033", "T11-MIN opened without its Samples folder", "positive", ["009"], None,
         opens(session_clips=CLIPS), ["resolution"],
         "narrowed: the missing-file report is U; only opening and the kept clip are judged; the sample is "
         "absent by setup instead of deletion", setup="without-samples"),
    case(33, "LSS-034", "Audio clip's RelativePath Samples/absent.wav; Path set to the copied sample at setup",
         "positive", ["009"], e_set(lambda r: file_ref(r).find("RelativePath"), "Value", "Samples/absent.wav"),
         opens(audio_clip_file="Samples/T11-tone.wav"), ["resolution"], setup="with-samples-absolute-path"),
    case(34, "LSS-036", "Identity values of the fixture sample", "computed", ["008", "010"], None,
         {"identity": {"OriginalFileSize": 176444, "OriginalCrc": 47018, "DefaultDuration": 44100,
                       "DefaultSampleRate": 44100}}, ["crc", "duration", "fileref-fields"],
         "extended: DefaultDuration and DefaultSampleRate added (REQ-008 D clause)", setup=None,
         action="compute-identity", assumptions=(), prov="doc-x"),
]


def comparator(c):
    if c["action"] == "compute-identity":
        return "identity values exact"
    return "outcome exact" + ("; listed state keys exact" if c["expected"].get("state") else "")


PROVENANCE = {
    "static": "static-derived; not observed reference output",
    "doc-static": "documented and static-derived; not observed reference output",
    "doc-x": "documented rule and extracted execution of the original's checksum routine; not observed "
             "reference output",
}
ASSUMPTIONS = {
    LI: "The list-item Id rule (negative, lettered or repeated Ids refused) applies to every list of an opened "
        "Live Set, Tracks included",
    SF: "When a set is opened from a file, a relative sample path of type 0 or 1 is joined to the folder that "
        "holds the set file",
}
SCOPES = {
    "REQ-LIVE-SET-STRUCTURE-001": "Element forms (compound, value, list, array); children matched by name; absence not itself a refusal; unknown child skipped; refusals: NextPointeeId without Value, a repeated child of a compound element, an unknown item name in Tracks",
    "REQ-LIVE-SET-STRUCTURE-002": "Tracks in display order; refused without an audio, MIDI or group track, or with one of those after a return track; TrackGroupId other than -1 refused in a set without group tracks",
    "REQ-LIVE-SET-STRUCTURE-003": "Track Id form; Name and Color elements written",
    "REQ-LIVE-SET-STRUCTURE-004": "Main and cue track placement; tempo, time signature and crossfader locations; absent main or cue track replaced by a new one (tempo 120)",
    "REQ-LIVE-SET-STRUCTURE-005": "DeviceChain children per track kind; mixer and device list locations; AudioOut/Main in the fixtures",
    "REQ-LIVE-SET-STRUCTURE-006": "Scenes, session and freeze slots, slot form; Ids do not order; freeze slot count must equal session slot count; scene fields written",
    "REQ-LIVE-SET-STRUCTURE-007": "Clip element in the slot, kind per track, Id and Time attributes, Name held as read",
    "REQ-LIVE-SET-STRUCTURE-008": "SampleRef and FileRef children; RelativePathType 0 and 1; Path and Type; size, checksum, frame count and rate rules",
    "REQ-LIVE-SET-STRUCTURE-009": "Type 0 and 1 resolution against the set's folder (assumption); fallback to Path for 0 and 1; a missing sample does not refuse",
    "REQ-LIVE-SET-STRUCTURE-010": "Stored length and rate equal the file's; fixture sample form only",
    "REQ-LIVE-SET-STRUCTURE-013": "One send holder per return; SendsPre form; fewer holders added at -70 dB; more than R refused",
    "REQ-LIVE-SET-STRUCTURE-014": "Envelope locations; envelopes with PointeeId 0 or naming no target removed on opening",
    "REQ-LIVE-SET-STRUCTURE-015": "Target Id form; absent NextPointeeId reads 1; Id 0 or no Id refused; NextPointeeId not above the largest Id refused; absent target element tolerated",
    "REQ-LIVE-SET-STRUCTURE-016": "List-item Id form; negative, lettered or repeated Ids refused (assumption); Ids do not order or link",
    "REQ-LIVE-SET-STRUCTURE-018": "Reference minimal set T11-MIN, whose device lists are empty, opens with the listed content; element status table",
}
EXCLUSIONS = {
    "inputs_without_expectation": [
        "envelopes, containers and format versions other than the preconditions'",
        "session slot count different from scene count; slots with no scenes or no Scenes element; two clips in a slot or a clip of the other track kind",
        "SendsPre length different from the number of return tracks",
        "missing samples beyond REQ-LIVE-SET-STRUCTURE-009 clause 3; other sample files, or stored length or rate differing from the file; RelativePathType 2 to 7",
        "any device in a device list (every device list of the fixtures is empty)",
        "repeated or negative target Ids",
        "list items without Id; list-item Id text other than digits, -1 and a",
        "items of Tracks of a known kind that is not a track; items of other lists of unknown or unaccepted kind",
        "output routing other than AudioOut/Main, or none, on audio, MIDI or return tracks",
        "group tracks beyond REQ-LIVE-SET-STRUCTURE-002 clause 4",
        "value elements without Value other than NextPointeeId; repeated children ending in KeyMidi; unknown attributes",
        "whether a track envelope whose target exists is kept",
        "documents that break more than one rule",
    ],
    "behavior": [
        "what a save writes (REQ-LIVE-SET-STRUCTURE-011, 017)",
        "device placement rules and device content (REQ-LIVE-SET-STRUCTURE-012)",
        "refusal presentation and state after a refusal",
        "displayed track names, EffectiveName derivation and colour display",
        "which scene a session slot belongs to; scene tempo, time signature and launching",
        "clip timing and loop fields, playback and audio",
        "which new Id an absent target element receives",
        "missing-sample report, search and playback",
        "which return a send feeds and what SendPreBool selects",
        "meaning of Type; use of LastModDate, OriginalFileSize and OriginalCrc on opening",
        "undo, edits after opening, cancellation and timing",
    ],
}

# ---- analyst-only traceability (relative to evidence_root unless a path starts with wiki/ or r2/) ----
E = {
    "fixture": "make_fixture.py; out/schema-check-fixture.jsonl (no deviation; all structure measurements as required); review: device lists emptied (lss_cases.device_free); shipped sets hold empty device lists on 4 MIDI and 21 audio tracks (out/documents.json chain_devices)",
    "schema-check": "schema_check.py; out/schema-check-als.jsonl, out/schema-check-alc.jsonl (375 documents: field, list and order form)",
    "survey": "t11_survey.py; out/documents.json (track kinds and order, track and list Ids, 39 track Ids equal to pointee Ids, chain children, routing, slots, scenes, holders, SendsPre)",
    "reader-n1": "wiki/research/transport-state-native.md#how-a-set-reaches-the-transport-objects: 0x1015299e0 start element, 0x10152adb0 -> 0x10152b45c required Value for type -4 elements, 0x101472624 duplicate member (n1-0007); r2/n1-transport-state-v1/notes.md round 2",
    "unknown-child": "r2/n1-transport-state-v1/notes.md round 2: 0x1015299e0 ignored frame; Unexpected node only when versioned and SchemaChangeCount equals the schema ChangeCount (1 != 5)",
    "list-loader": "traces/pointee/trace.txt 'List-item Ids (reader)': 0x1014674b4 unknown class, slot +0x190 class test, duplicate Id -> Non-unique list ids; x86 0x10145f320 (traces/pointee/x86-10145f320-list-loader.txt)",
    "list-id-attr": "traces/pointee/trace.txt: 0x10152b77c Id parsed with int rule 0x1002fd908; failure or < 0 throws; flag +0x61 (A5)",
    "walk-tracks": "traces/tracks/trace.txt item 3; x86 0x1027b1a00 (traces/tracks/x86-1027b1a00.txt 1027b1a48-1027b1ac5)",
    "walk-grouping": "traces/tracks/trace.txt item 3 grouping: open-group stack; TrackGroupId != -1 needs a matching open group, else Track grouping corrupt",
    "walk-slots": "traces/tracks/trace.txt item 4; x86 0x1026f1720 (traces/tracks/x86-1026f1720.txt): freeze vs session ClipSlotList size",
    "freeze-empty": "traces/a1a2/trace.txt, reach.txt: chain ctors 0x1027df560, 0x10291f76c; sequencer base 0x10265b61c empty list; no load step adds slots (A2 settled)",
    "open-path": "traces/a1a2/trace.txt, x86-load-sequence.txt: load step x86 0x10147e150 runs +0xd0 then the walk 0x10147e2e0 unconditionally (A1 settled)",
    "song-ctor": "traces/tracks/trace.txt item 6: ASong ctor 0x10266f738 creates cue and main tracks and empty SendsPre, Scenes, Tracks",
    "tempo-default": "wiki/specs/transport-state.md REQ-TRANSPORT-STATE-007 (tempo 120 for a new main track's tempo); wiki/research/transport-state-native.md",
    "holders": "traces/tracks/trace.txt item 5; x86 0x1027c1640 (traces/tracks/x86-1027c1640.txt 1027c18a2-1027c18f3): R trailing returns, fewer appended, more refused",
    "new-send": "wiki/research/mixer-values.md#constructor-defaults-and-ranges (send holder 0x102658f54: Send 0.0003162277571, s9-0002); appended holders 0x10271d824 -> 0x102659a78 -> 0x102658f54 (reviewer check, review/review-checks.txt); draft wiki/specs/mixer-values.md REQ-MIXER-VALUES-003 (unreleased there); handoff/mixer-values-v1/spec.md REQ-MIXER-VALUES-006 (-inf dB at or below -69.7 dB)",
    "pointee-postload": "traces/pointee/trace.txt 'Pointee post-load hook' 0x101535954; x86 0x101525600 (traces/pointee/x86-101525600-pointee-postload.txt)",
    "preset-flag": "traces/a1a2/trace.txt preset exemption off on the open path (A3 settled)",
    "nextpointee": "traces/pointee/trace.txt 'Document post-load pointee check' 0x1015441a8 steps 1-2; x86 0x101533ae0, 0x10153df90; ADocument ctor NextPointeeId 1",
    "registration": "traces/pointee/trace.txt step 4 and 0x10154368c: a pointee constructed with Id 0 gets the counter",
    "dangling": "traces/pointee/trace.txt 'Dangling envelope purge': 0x1026869b0, dangling test 0x101536090 (PointeeId 0 or unregistered); gate byte set by app ctor",
    "fileref-fields": "traces/fileref/trace.txt; traces/fileref/fileref-survey.json",
    "crc": "traces/fileref/crc_check.py, crc-check.txt (2,984 of 2,984); out/x-crc.json (x86 0x101191310 on the T11 sample prefix: 47018; 123456789: 65256)",
    "duration": "traces/fileref/duration_check.py, duration-check.txt (2,983 of 2,983 WAV and AIFF)",
    "resolution": "traces/fileref/trace.txt: 0x1014e8504 (x86 0x1014d8e20; fallback to Path without identity 0x1014d90e5); candidates 0x1014e9d78; missing status 0x10279d228; no throwing branch",
}
A = {
    "A4": "SPEC-LIVE-SET-STRUCTURE A4: sample-path resolution context present on open, base = folder of the set file (open)",
    "A5": "SPEC-LIVE-SET-STRUCTURE A5: every list read by the generic list loader (open)",
    "A6": "SPEC-LIVE-SET-STRUCTURE A6: bundled device classes accepted in track chains (open; listed in Q-022); not used: the review removed both devices from T11-MIN and every fixture",
    "A1, A2, A3": "settled statically in revision 1; walk-dependent cases (REQ-002, 006) and the Id-0 case rest on them as S",
}
CLAUSES = {
    "001 clauses 1-3": ["schema-check", "reader-n1"], "001 clause 4": ["unknown-child"],
    "001 clause 5": ["reader-n1", "list-loader"], "002 clauses 1-3": ["survey", "walk-tracks", "open-path"],
    "002 clause 4": ["walk-grouping"], "003": ["survey"], "004 clauses 1-2": ["survey"],
    "004 clause 3": ["song-ctor", "tempo-default"], "005": ["survey"], "006 clauses 1-3, 5-6": ["survey"],
    "006 clause 4": ["walk-slots", "freeze-empty", "open-path"], "007": ["schema-check", "survey"],
    "008": ["fileref-fields", "crc", "duration"], "009": ["resolution"], "010": ["duration"],
    "013": ["survey", "holders", "new-send"], "014": ["dangling"],
    "015": ["survey", "pointee-postload", "preset-flag", "nextpointee", "registration"],
    "016": ["survey", "list-loader", "list-id-attr"], "018": ["fixture"],
}
EXCLUDED = {
    "LSS-009, LSS-010": "U (REQ-006 slots against scenes; zero scenes)",
    "LSS-015": "U (SendsPre count)", "LSS-018": "U (Id-less list item)", "LSS-026": "U (duplicate pointee Ids)",
    "LSS-035": "type-7 outcome can be changed by the U library relocation and missing-file search (Q-022 missing samples)",
    "LSS-037": "S-cond A6, an open Q-022 item; REQ-012 unreleased", "LSS-038": "U (device class per chain)",
    "LSS-039, LSS-040": "save: S-cond A7 and REQ-011 U (RelativePathType); REQ-011 and 017 unreleased",
}
DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"FUN_", r"disassembl", r"decompil", r"pseudocode",
        r"Ghidra", r"corpus", r"vtable", r"dossier", r"\bLSS-", r"\bQ-0", r"PRB-", r"\bA[1-7]\b", r"S-cond",
        r"\bT1(?:\.\d)?\b", r"ADR", r"Python", r"zlib", r"[Ee]xpat", r'(?i)(?<!")\bschema\b(?!\s+content|")',
        r"\bA[A-Z][a-z]{2,}", r"Remoteable(?!TimeSignature)", r"Timeable", r"\bpointees?\b", r"constructor",
        r"post-load", r"validation walk", r"loader", r"\+0x", r"/home/", r"/var/", r"/tmp/",
        r"Slot count mismatch", r"Set has no player", r"out of order", r"grouping corrupt", r"Non-unique",
        r"too low", r"Invalid Pointee", r"Illegal", r"Unknown class", r"Required attribute", r"already has member",
        r"send knobs"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages
