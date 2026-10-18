"""Phase 4 reference observation batch: merge every packet probe record into one list.

Usage (from the repository root): python3 -I analysis/ableton-live-12.4.3/r2/phase4-batch-v1/build_batch.py
Reads the five probe-batch.json files verbatim and the wiki probe tables transcribed below
(each with its page locator), adds normalized fields, and writes batch.json, fixture-plan.json
and manifest.json beside this script. Nothing here runs or reads Ableton Live.
"""
import hashlib, json, os, sys

OUT = os.path.dirname(os.path.abspath(__file__))
R2 = "analysis/ableton-live-12.4.3/r2"
JSON_SOURCES = {
    "S4": f"{R2}/s4-midi-v1/probe-batch.json",
    "N1": f"{R2}/n1-transport-state-v1/probe-batch.json",
    "N2": f"{R2}/n2-container-v1/probe-batch.json",
    "H1": f"{R2}/h1-plugin-scanner-v1/probe-batch.json",
    "H2": f"{R2}/h2-index-v1/probe-batch.json",
}
WIKI = {
    "N3": "wiki/research/transport-transitions-native.md",
    "N4": "wiki/research/helper-launch-live-side.md",
    "N5": "wiki/research/device-parameter-mapping-native.md",
    "H4": "wiki/research/device-bundles-static.md",
    "P5": "wiki/research/push3-helper-static.md",
    "CORPUS": "wiki/research/corpus-dsp-static.md",
    "H6": "wiki/research/web-addons-swapper-static.md",
    "T1": "wiki/research/native-transport-study.md",
}
SUMMARY_PAGES = {  # wiki pages that list (not own) the JSON records
    "S4": ["wiki/research/midi-closure-r2.md#phase-4-probe-batch", "wiki/specs/midi-user-mapping.md"],
    "N1": ["wiki/research/transport-state-native.md#phase-4-probes", "wiki/specs/transport-state.md"],
    "N2": ["wiki/research/document-container-native.md#remaining-unknowns-and-phase-4-probes", "wiki/specs/als-container.md#open-questions"],
    "H1": ["wiki/research/plugin-scanner-static.md#phase-4-probe-batch"],
    "H2": ["wiki/research/browser-index-static.md#phase-4-probe-batch"],
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- original records
def json_records():
    recs = []
    for packet, path in JSON_SOURCES.items():
        d = json.load(open(path))
        common = d.get("common_prerequisites") or d.get("shared_setup") or d.get("policy")
        for i, p in enumerate(d["probes"]):
            recs.append({
                "id": p["id"], "original_id": p["id"], "packet": packet,
                "source": {"path": path, "locator": f"/probes/{i}", "summarized_in": SUMMARY_PAGES[packet]},
                "original": {
                    "question": p["question"],
                    "existing_evidence": p.get("existing_evidence"),
                    "why_static_insufficient": p.get("why_static_insufficient"),
                    "affected": p.get("clauses") or p.get("requirements"),
                    "minimal_input": p.get("minimal_input"),
                    "discriminating_observation": p.get("discriminating_observation"),
                    "stop_condition": p.get("stopping_condition") or p.get("stop_condition"),
                    "prerequisites": p.get("environment") or common,
                },
            })
    return recs


def T(id_, packet, anchor, question, evidence, minimal_input, observation, stop, original_id=True):
    """A record transcribed from a wiki table or section (verbatim cell text)."""
    return {
        "id": id_, "original_id": id_ if original_id else None, "packet": packet,
        "source": {"path": WIKI[packet], "locator": anchor + (f" row {id_}" if original_id else ""), "summarized_in": []},
        "original": {"question": question, "existing_evidence": evidence, "why_static_insufficient": None,
                     "affected": None, "minimal_input": minimal_input,
                     "discriminating_observation": observation, "stop_condition": stop, "prerequisites": None},
    }


N4A, N5A, H4A, P5A = "#phase-4-probe-records", "#phase-4-probe-records", "#phase-4-probe-records", "#phase-4-probe-records"
TABLE_RECORDS = [
    T("PRB-N4-01", "N4", N4A, "Scanner argv for Rescan and modifier-Rescan", None, "`ps -axww -o pid,ppid,args` during each", "`--vst3 user=…,local=…`; `--reset all` only with the modifier; no `--au`", "One capture per kind"),
    T("PRB-N4-02", "N4", N4A, "Scanner relaunch on crash and on limit", None, "Test plug-in that crashes on load; 60 new test modules", "Log `stopped prematurely.  Restart` vs `finished a chunk of work.  Continue`; launch count", "Scan reaches `done`"),
    T("PRB-N4-03", "N4", N4A, "Index options file", None, "Copy `com.ableton.index.*.txt` at launch", "Key set and values above, `db-path` folder and name", "One capture"),
    T("PRB-N4-04", "N4", N4A, "Restart caps", None, "`kill -9` the index (or add-ons) helper repeatedly", "Restarts stop after 100 (index) and 10 (add-ons) launches with `Giving up`", "Cap reached once"),
    T("PRB-N4-05", "N4", N4A, "Observer timeouts", None, "Replace a helper by a stub that never sends sync; and one that ignores shutdown", "Killed about 60 s after launch; killed about 5 s after shutdown request", "Three repeats"),
    T("PRB-N4-06", "N4", N4A, "Web connector commands", None, "Copy `web_connector_args_<pid>.txt` with auto-update on/off and with < 3 GiB free", "`check_for_auto_updates` present only with > 3 GiB and the setting on", "Four combinations"),
    T("PRB-N4-07", "N4", N4A, "Swapper-running guard", None, "Start Live while a process named `Ableton Swapper` exists", "Dialog text above; exit status 42", "One capture"),
    T("PRB-N4-08", "N4", N4A, "Push 3 sockets and restart", None, "`lsof -U` for Live and Push3; `kill -9` Push3", "Live listens on flip and push-to-live; Push3 relaunched about 1.5 s later", "Three repeats"),
    T("PRB-N4-09", "N4", N4A, "MultiF0 selection", None, "Convert Harmony on arm64 Live with logging", "`Audio2Midi: Use builtin MultiF0 lib`", "One capture"),
    T("P4-N5-01", "N5", N5A, "Is the passed value the internal value, with the index order above? Do the Corpus positions arrive as 0..1 or −1..1?", "Tables above; value chain Inferred; open position contradiction", "Breakpoint or trace on each bundle's `_SetParameterA` (Amp `0x3490`, Electric `0xc2b8`, Corpus `0x4f40` arm64); load one shipped preset per device, plus Corpus copies with `ExcitationX` 0 and 1", "Logged (index, value): Amp `Bass` 5 → (1, 0.5); Electric `KeyboardTranspose` 12 → (30, 12); Corpus `FilterMidFreq` 1000 → (28, ≈0.509); Corpus `ExcitationX` 0/1 → (14, 0/1) on this chain or (14, −1/1); index 37 arrives and is ignored", "Three values per device match, or any mismatch is recorded"),
    T("P4-N5-02", "N5", N5A, "Do Amp and Cabinet create two engine instances, and the others one?", "Selector 4 path", "Breakpoint on `_CreateInstanceU`; insert each device once", "Hit count per insert", "All seven counted"),
    T("P4-N5-03", "N5", N5A, "Does a fresh Electric take `PickupAmpIn` 0.42 (Defaults preset) or 0.5 (constructor)?", "Code 0.5 vs preset 0.42", "Empty set; insert Electric; save", "Saved `PickupAmpIn`", "One save inspected; refines P4-H4-03"),
    T("P4-N5-04", "N5", N5A, "What does the user see when a bundle is absent?", "`sErrorTextPluginLoadFailed` path", "Only if a disposable application copy with a removed `Corpus.bundle` can be run without breaking code signing; otherwise skip", "Notice text; device state; save output", "Observed once or recorded as infeasible"),
    T("P4-H4-01", "H4", H4A, "What does 12.4.3 write when it saves each device?", "DEV-C01–C09 come from shipped content only", "Insert each device fresh; also load each default or shipped preset; save as `.adv`, and save a set holding all seven", "XML diff against the inputs: field order, value text, IDs, ranges, envelope", "Seven presets and one set saved and diffed"),
    T("P4-H4-02", "H4", H4A, "Does load clamp, reject or keep out-of-range values?", "DEV-C05", "Copies of one Amp and one Analog preset with `Manual` above max, below min, non-numeric and missing; an enum index past its maximum", "The value shown after load and after re-save; any error dialog", "Each case observed once"),
    T("P4-H4-03", "H4", H4A, "What values does a fresh Amp, Cabinet or Corpus have, and does editing `Defaults/*.adv` change a fresh Analog?", "No default preset for three devices", "Empty set; insert each device; save", "Saved `Manual` values", "Values recorded for all seven"),
    T("P4-H4-04", "H4", H4A, "Which labels and units belong to each stored domain?", "Units appear only as engine strings", "A control-surface or Max for Live script dumping each parameter's name, min, max, quantization, value items and string for value, if the API is confirmed present in 12.4.3", "Parameter table per device", "All seven tables captured"),
    T("P4-H4-05", "H4", H4A, "What do Amp and Cabinet do at a rate without a model (for example 32 kHz)?", "Six model rates; `Sample rate not supported`", "Set the audio device rate; insert Amp", "Output signal present or absent; any message", "One rate observed"),
    T("P5-01", "P5", P5A, "Does Live launch the helper, and with which arguments?", None, "Start Live with Push 3 in Control mode; `ps -axo pid,ppid,args`", "`Helpers/Push3.app/.../Push3` child with `--parent-process-id=<Live pid>`", "One capture each with and without Push 3"),
    T("P5-02", "P5", P5A, "Socket roles and paths", None, "`lsof -U -a -p <pid>` for both processes; list `$TMPDIR`", "Listener of each of the three channel names", "All three attributed"),
    T("P5-03", "P5", P5A, "Watchdog timing", None, "(a) `kill -9 <Live pid>`; (b) `kill -STOP <Live pid>` for 30 s; time the helper's exit and read `Push3.log`", "Static prediction: (a) exit after about 5 s; (b) no exit, because `kill(pid, 0)` still succeeds", "Three repeats of each"),
    T("P5-04", "P5", P5A, "Behavior without hardware", None, "Launch path with Push 3 unplugged and replugged", "No launch, \"No Push hardware found\", or a hotplug wait", "Each case once"),
    T("P5-05", "P5", P5A, "Display frame encoding", None, "USB capture of the bulk OUT endpoint", "Header and payload sizes; frame rate; pixel/mask pattern on a known screen", "10 s capture"),
    T("P5-06", "P5", P5A, "Push 2 path", None, "Connect Push 2 instead", "Which display process runs", "One capture"),
    T("P5-07", "P5", P5A, "Network activity in Control mode", None, "`tcpdump` on `224.76.78.75` and the update host", "Packets present or absent", "5-minute capture"),
    T("P5-08", "P5", P5A, "MIDI path", None, "Live MIDI preferences plus `lsof`/MIDI Monitor", "Whether pads reach Live through CoreMIDI or the push-to-live channel", "One pad press per path"),
    T("P5-09", "P5", P5A, "Real-time segment", None, "`vmmap`/`lsof` on the helper", "Backing file or shared-memory name", "One capture"),
    T("ESC-N3-01", "N3", "#adr-0002-escalation-record (whole section; the page assigns no ID)",
      "For the default preconditions, what does the user observe after Play, Stop, Stop, and after a Play then Stop within one audio buffer? Specifically, the song position display and the saved `CurrentTime`, and whether the Play control and `is_playing` lag the request.",
      "This page: the request and reflection paths, T-01 to T-08.",
      "default set, extern sync, Link and count-in off, Arrangement Record off; move the insert marker to bar 5 (beat 16); press Play, wait 2 s, press Stop, wait 1 s, press Stop; separately, Play then Stop within 50 ms; separately, enable Loop and \"loop is song start\" (if exposed in the interface), then press Play.",
      "Position display and LOM `current_song_time` after each step. T-03 predicts 0.0 after the second Stop. LOM `is_playing` sampled every 10 ms around each press, to measure the reflection lag. Saved `CurrentTime` after the final step. Start position with loop-is-song-start: T-08 predicts the loop start.",
      "One capture per scenario. If the second Stop does not return to 0.0, record the observed value and reopen T-03 statically at `0x10270087c`; do not iterate further at runtime.",
      original_id=False),
    T("P4B-CORPUS-01", "CORPUS", "#candidate-requirements-for-spec-corpus-device (section text: 'for the Phase 4 probe batch to measure')",
      "Does Corpus output match the static predictions CD-C01 to CD-C08?", "Candidate table CD-C01–CD-C08 and the port checks on the same page", None, None, None, original_id=False),
    T("P4B-H6-01", "H6", "#web-connector-addons-and-swapper-static-evidence (intro) and #unknowns-and-questions-for-the-main-live-project (last bullet)",
      "Runtime order, timing and actual network traffic of the Web Connector, AddOns and Swapper helpers ('Runtime confirmation of any of the above (Phase 4)')", None, None, None, None, original_id=False),
    T("P4B-T1-01", "T1", "#study-p1-loop-enable-persistence (closing paragraph 'An optional bounded reference probe…', case families P1-A to P1-F)",
      "Optional bounded reference probe to discriminate the first material loop-enable ambiguity, such as whether a missing field preserves initialization or triggers migration", "Case families P1-A to P1-F and their seeds on the same page",
      "Not chosen; one of P1-A to P1-F. The page names what to capture (load outcome, observable loop-enable state, saved XML), not which result discriminates", None, None, original_id=False),
]

# ---------------------------------------------------------------- normalized overlay
NONE_NET = "off"
BASE_TOOLS = ["screen capture", "shasum -a 256", "gzip/xxd for saved files"]


def O(session, order, minutes, risk, risk_note, affected, unblocks, procedure, fixtures, *, why=None, hardware=(), plugins=(),
      app_copy="plain disposable copy", network=NONE_NET, tools=(), depends=(), merge=None, flags=(), mapped_affected=None):
    return dict(session=session, order=order, minutes=minutes, risk=risk, risk_note=risk_note, affected=affected, unblocks=unblocks,
                procedure=procedure, fixtures=fixtures, why=why, hardware=list(hardware), plugins=list(plugins), app_copy=app_copy,
                network=network, tools=list(tools), depends=list(depends), merge=merge, flags=list(flags), mapped_affected=mapped_affected)


MIDI_TOOLS = ["IAC Driver bus (availability unverified)", "MIDI sender able to emit single CC/note messages (none established)", "screen capture"]
MIDI_FX = ["FX-ENV", "FX-APP", "FX-MIDI", "FX-S4-PROFILES"]
H2S = "H3 handoff candidate (SPEC-ALS-CONTAINER r1)"
H1S = "H2 handoff candidate (SPEC-TRANSPORT-STATE r1)"
TS_REQ = "REQ-TRANSPORT-STATE-"
AC = "REQ-ALS-CONTAINER-"
DOC_FX = ["FX-ENV", "FX-APP"]
REQ_MISMATCH = "requirement-ID mismatch: the probe-batch.json IDs predate spec r1 numbering; affected_ids follow the spec's own PRB citations (spec > analysis)"
SCAN_TOOLS = ["process-argument capture (`ps -axww` polling, or `eslogger exec` if established)", "sqlite3 on read-only copies", "screen capture"]
DBG = ["debugger able to attach to a disposable Live copy (lldb; attach to a hardened-runtime app is not established)"]
LOM_HARNESS = "LOM sampling harness (Max for Live device or control-surface script); availability in 12.4.3 not established"

OV = {
    # ---- S4 MIDI (session F)
    "PRB-S4-01": O("F", 1, 15, "low", "writes only to the test account's User Remote Scripts folder", {"requirements": ["REQ-MIDI-USER-001"], "questions": ["Q-010"]},
                   "REQ-MIDI-USER-001 (not released in midi-config-v2); a successor MIDI handoff",
                   ["Create profile folders 'S4 Probe' and 'S4Probe2' with the one-line profile", "Without restarting, capture the Control Surface menu", "Quit, relaunch, capture the menu again; retain Log.txt"], DOC_FX + ["FX-S4-PROFILES"], tools=["screen capture"]),
    "PRB-S4-02": O("F", 2, 10, "low", "as PRB-S4-01", {"requirements": ["REQ-MIDI-USER-001"], "questions": ["Q-010"]}, "REQ-MIDI-USER-001 name rules",
                   ["Add the five differently named folders", "Restart; capture the menu order"], DOC_FX + ["FX-S4-PROFILES"], depends=["PRB-S4-01"], tools=["screen capture"]),
    "PRB-S4-03": O("F", 3, 20, "low", "malformed profile in the test account only", {"requirements": ["REQ-MIDI-USER-002", "REQ-MIDI-USER-003", "REQ-MIDI-USER-011", "REQ-MIDI-USER-013"], "questions": ["Q-008"]},
                   "Host outcome of a raising profile, excluded from midi-config-v2 (REQ-002c/d, 003e, 011b, 013d)",
                   ["Select the duplicate-option profile; restart", "Send CC20 and CC21 on channel 0; capture master volume, menu state, dialogs, Log.txt", "Only if not a uniform load failure: repeat with the Pad1Note and MixerButtonsToggle variants"], MIDI_FX, tools=MIDI_TOOLS),
    "PRB-S4-04": O("F", 4, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-005"], "questions": ["Q-008"]}, "REQ-MIDI-USER-005c unknown-mode outcome",
                   ["Select the lowercase-mode profile; restart", "Send CC20 0 then 127 and CC30 127; capture master volume, track 1 mute, Log.txt"], MIDI_FX, tools=MIDI_TOOLS),
    "PRB-S4-05": O("F", 5, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-005", "REQ-MIDI-USER-010"], "questions": ["Q-009"]}, "REQ-MIDI-USER-005d/010d Absolute scaling",
                   ["Select the MasterVolumeSlider: 20 profile", "Send CC20 = 0, 64, 127 one at a time; capture the master volume display after each"], MIDI_FX, tools=MIDI_TOOLS),
    "PRB-S4-06": O("F", 6, 15, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-004", "REQ-MIDI-USER-012"], "questions": ["Q-009", "Q-010"]},
                   "REQ-MIDI-USER-004 (not released in midi-config-v2)",
                   ["Select the transport profile with an empty set", "Send 127, 0, 127 to each of Play, Stop, Loop and Metro notes/CCs; capture transport state after each"], MIDI_FX, tools=MIDI_TOOLS,
                   flags=["related: ESC-N3-01 observes the same Play/Stop states through the UI"]),
    "PRB-S4-07": O("F", 7, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-004", "REQ-MIDI-USER-012"], "questions": ["Q-009"]}, "REQ-MIDI-USER-004b/012c seek timing",
                   ["Set position 1.1.1 and tempo 120", "Hold FfwdButton (CC68 127) for 2.0 s then send 0; capture the position", "Repeat once"], MIDI_FX, tools=MIDI_TOOLS + ["timed MIDI sender (2.0 s hold)"]),
    "PRB-S4-08": O("F", 8, 15, "low", "test set uses generated tones only", {"requirements": ["REQ-MIDI-USER-006"], "questions": ["Q-010"]}, "REQ-MIDI-USER-006b/c pad translation",
                   ["Build a Drum Rack with 16 generated tones on the visible pads (in the UI)", "Select the pad profile; send note 60 on/off then 75 on/off; capture which pad lights and plays"], MIDI_FX + ["FX-WAV"], tools=MIDI_TOOLS),
    "PRB-S4-09": O("X", 1, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-007"], "questions": ["Q-009"]}, "REQ-MIDI-USER-007c/d device parameter addressing",
                   ["Only after the static `_Generic/Devices` trace leaves name-to-parameter resolution material: select the Encoder1-8 profile with Auto Filter selected", "Send CC10..17 = 127 in turn; capture which parameter moves"], MIDI_FX, tools=MIDI_TOOLS,
                   flags=["deferred by its own record until the `_Generic/Devices` static trace is done"]),
    "PRB-S4-10": O("F", 9, 15, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-008"], "questions": ["Q-009", "Q-010"]}, "REQ-MIDI-USER-008b/c/d/f bank, on/off and lock",
                   ["Insert a device with 3 banks; select the bank/lock profile", "Press Next 4 times, OnOff once, Lock then select another device; capture bank, activator and encoder target"], MIDI_FX, tools=MIDI_TOOLS,
                   flags=["input gap: the record does not name the 3-bank device; choose it from the static bank tables before the sitting"]),
    "PRB-S4-11": O("F", 10, 15, "low", "test set only", {"requirements": ["REQ-MIDI-USER-009"], "questions": ["Q-010"]}, "REQ-MIDI-USER-009b strip-to-track order",
                   ["Build the 9-track set (one folded group of 2, 2 returns) in the UI", "Send each select CC before and after one Next; capture selected track names"], MIDI_FX, tools=MIDI_TOOLS,
                   flags=["run only if the cheaper static `_Framework/MixerComponent` trace (midi-closure-r2 next steps) has not settled it"]),
    "PRB-S4-12": O("F", 11, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-011", "REQ-MIDI-USER-009"], "questions": ["Q-009"]}, "REQ-MIDI-USER-011c/f, 009c toggles and arm-select",
                   ["Select the MixerButtonsToggle: True profile", "Send 127 then 0 to mute 1 and arm 2; capture mute, arm and selection", "Repeat with False only if the outcome differs from prediction"], MIDI_FX, tools=MIDI_TOOLS),
    "PRB-S4-13": O("F", 12, 15, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-011"], "questions": ["Q-009"]}, "REQ-MIDI-USER-011e mute feedback bytes",
                   ["Route the surface output to a MIDI monitor", "Toggle track 1 mute in the UI with InvertMuteButtonFeedback True and False; capture CC30 bytes"], MIDI_FX, tools=MIDI_TOOLS + ["MIDI monitor on the output port"]),
    "PRB-S4-14": O("F", 13, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-001", "REQ-MIDI-USER-013"], "questions": ["Q-010"]}, "Q-010 reload timing",
                   ["With the CC20 profile active, edit it to CC21 while Live runs", "Test CC20/CC21 after the edit, after reselecting the surface, after restart"], MIDI_FX, tools=MIDI_TOOLS),
    "PRB-S4-15": O("F", 14, 10, "low", "disables the IAC bus temporarily", {"requirements": ["REQ-MIDI-USER-004", "REQ-MIDI-USER-012"], "questions": ["Q-010"]}, "Q-010 teardown",
                   ["Hold NudgeUp (CC71 127)", "Deselect the surface; capture whether nudge stops", "Repeat holding, then disable the IAC bus"], MIDI_FX, tools=MIDI_TOOLS),
    "PRB-S4-16": O("F", 15, 10, "low", "test profile only", {"requirements": ["REQ-MIDI-USER-013"], "questions": ["Q-010"]}, "REQ-MIDI-USER-013h encoding (low priority)",
                   ["Select the UTF-8 'é' comment profile; test CC20", "Repeat with the UTF-8 BOM profile; capture Log.txt"], MIDI_FX, tools=MIDI_TOOLS),
    # ---- N1 transport-state documents (sessions A, D)
    "PRB-N1-07": O("A", 1, 15, "low", "saves to the test folder only", {"requirements": [TS_REQ + "002", TS_REQ + "008", TS_REQ + "011"], "questions": ["Q-012"]},
                   H1S + ": confirms REQ-002/REQ-011 on a real save; supplies the SchemaChangeCount for REQ-008 and PRB-N1-08",
                   ["Open a copy of N2-001.als (byte-identical to the shipped `Recording Audio.als` base)", "Set tempo 121.2, 7/8, loop start 0.5 beat, loop length 3.3 beats", "Save As a new file; hash it; decompress and retain the XML"],
                   DOC_FX + ["FX-N1-BASE"], tools=BASE_TOOLS, merge={"group": "M-SAVE", "relation": "primary", "with": ["PRB-N2-01"]},
                   mapped_affected=True, flags=[REQ_MISMATCH + " (record lists REQ-011 and nonexistent REQ-013)"]),
    "PRB-N1-04": O("A", 3, 15, "low", "test documents only", {"requirements": [TS_REQ + "012", TS_REQ + "007"], "questions": ["Q-012"]},
                   H1S + ": REQ-012 and TS cases are excluded until this runs; also the REQ-007 time-signature default",
                   ["Open each of the three time-signature variants from a fresh launch", "Capture the displayed meter", "Re-save each; retain Manual and EnumEvent values"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS, mapped_affected=True),
    "PRB-N1-05": O("A", 4, 15, "low", "test documents only", {"requirements": [TS_REQ + "012"], "questions": ["Q-012"]}, H1S + ": REQ-012 tempo precedence",
                   ["Open each of the three tempo variants without launching a scene", "Capture the displayed tempo", "Re-save; retain Manual and FloatEvent"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS),
    "PRB-N1-01": O("D", 1, 15, "low", "test documents only", {"requirements": [TS_REQ + "003"], "questions": ["Q-012"]}, H1S + ": REQ-003 token outcomes and the read-error presentation",
                   ["Open the four LoopOn variants from a fresh launch each", "Capture loop switch state or dialog text and Log.txt"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS,
                   flags=["related: dialog text overlaps PRB-N2-03 (shared read-error presentation)"]),
    "PRB-N1-02": O("D", 2, 20, "low", "test documents only", {"requirements": [TS_REQ + "007"], "questions": ["Q-012"]}, H1S + ": REQ-007 defaults versus a template",
                   ["Open the three omission variants (base edited to LoopStart 4, LoopLength 8)", "Capture loop brace and tempo", "Re-save each"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS,
                   mapped_affected=True, flags=[REQ_MISMATCH + " (record lists REQ-006)"]),
    "PRB-N1-03": O("D", 3, 30, "low", "test documents only", {"requirements": [TS_REQ + "009"], "questions": ["Q-012"]}, H1S + ": cases TS-017 and TS-018 (excluded until run)",
                   ["Open the six out-of-range variants", "Capture opens/refuses and displayed values", "Re-save each"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS),
    "PRB-N1-06": O("D", 4, 15, "low", "test documents only", {"requirements": [TS_REQ + "009", TS_REQ + "010"], "questions": ["Q-012"]}, H1S + ": case TS-019 (excluded until run)",
                   ["Open the codes 495, -1 and 201.0", "Capture meter, Log.txt 'out of range' lines and the re-saved code"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS,
                   mapped_affected=True, flags=[REQ_MISMATCH + " (record lists REQ-010 only; spec cites it under REQ-009)"]),
    "PRB-N1-08": O("D", 5, 20, "low", "test documents only", {"requirements": [TS_REQ + "008"], "questions": ["Q-012"]}, H1S + ": REQ-008 user-visible outcomes",
                   ["Build the SchemaChangeCount variant from PRB-N1-07's saved value", "Open the four variants; capture opens/refuses, error text and loop state"], DOC_FX + ["FX-N1-VAR"], tools=BASE_TOOLS,
                   depends=["PRB-N1-07"], mapped_affected=True, flags=[REQ_MISMATCH + " (record lists REQ-007 and REQ-008)"]),
    # ---- N2 container (sessions A, D)
    "PRB-N2-01": O("A", 2, 10, "low", "saves to the test folder only", {"requirements": [AC + "007", AC + "008"], "questions": ["Q-012", "Q-006"]}, H2S + ": REQ-007/008 save container and envelope",
                   ["Fresh launch; File > New Live Set; Save As 'n2-probe-01.als'", "Hash; capture the first 10 bytes and the first three decompressed lines byte-for-byte"], DOC_FX + ["FX-NEWSET"], tools=BASE_TOOLS,
                   merge={"group": "M-SAVE", "relation": "near-duplicate", "with": ["PRB-N1-07"]}),
    "PRB-N2-02": O("A", 5, 10, "low", "test documents only", {"requirements": [AC + "001", AC + "007"], "questions": ["Q-006"]}, H2S + ": REQ-001 plain-XML acceptance (case N2-002)",
                   ["Open N2-002.als", "Save; capture the saved file's first bytes (1f 8b versus '<?')"], DOC_FX + ["FX-N2-CASES"], tools=BASE_TOOLS,
                   mapped_affected=True, flags=["spec open-questions table also cites REQ-ALS-CONTAINER-007 (record lists 001 only)"]),
    "PRB-N2-03": O("A", 6, 30, "low", "test documents only", {"requirements": [AC + "001", AC + "002", AC + "003", AC + "005", AC + "009"], "questions": ["Q-006"]}, H2S + ": REQ-009 failure presentation",
                   ["With a known set open, open each of the ten corrupt cases", "Capture dialog text, Log.txt, and whether the previous set stays open"], DOC_FX + ["FX-N2-CASES"], tools=BASE_TOOLS),
    "PRB-N2-04": O("A", 7, 15, "low", "test documents only", {"requirements": [AC + "004"], "questions": ["Q-006"]}, H2S + ": REQ-004 newer-version text",
                   ["Open N2-013, N2-019, then N2-019 with Creator removed", "Capture dialog text and which version it names"], DOC_FX + ["FX-N2-CASES"], tools=BASE_TOOLS,
                   flags=["input gap: 'N2-019 with Creator removed' is not among the 27 retained cases; construct it before the sitting"]),
    "PRB-N2-05": O("D", 6, 10, "low", "test documents only", {"requirements": [AC + "004", AC + "005"], "questions": ["Q-006"]}, H2S + ": cases N2-018 and N2-020",
                   ["Open N2-018 and N2-020", "Capture corrupt versus newer-version dialog"], DOC_FX + ["FX-N2-CASES"], tools=BASE_TOOLS, flags=["related: same newer-version path as PRB-N2-04"]),
    "PRB-N2-06": O("D", 7, 25, "low", "test documents only", {"requirements": [AC + "003", AC + "005", AC + "006"], "questions": ["Q-006"]}, H2S + ": cases N2-012 and N2-014 and the positive envelope variants",
                   ["Open N2-012, 014, 021, 022, 023, 024", "Capture opens without dialog or the dialog text"], DOC_FX + ["FX-N2-CASES"], tools=BASE_TOOLS),
    "PRB-N2-07": O("D", 8, 5, "low", "test documents only", {"requirements": [AC + "001"], "questions": ["Q-006"]}, H2S + ": case N2-027",
                   ["Open N2-027.als; capture dialog text and Log.txt"], DOC_FX + ["FX-N2-CASES"], tools=BASE_TOOLS),
    # ---- N3 escalation (session B)
    "ESC-N3-01": O("B", 1, 40, "low", "UI interaction and one save in the test folder", {"requirements": [], "candidates": ["T-01", "T-02", "T-03", "T-05", "T-08", "T-13"], "questions": ["Q-007"]},
                   "S3 transition table (no transitions spec drafted yet); timing inputs for S5 clip launch",
                   ["New default set with extern sync, Link, count-in and Arrangement Record off; insert marker at bar 5", "Play, wait 2 s, Stop, wait 1 s, Stop; capture display and LOM values; save and retain CurrentTime",
                    "Separately Play then Stop within 50 ms", "Separately Loop on with loop-is-song-start (if exposed), then Play"],
                   DOC_FX + ["FX-NEWSET", "FX-LOM"], tools=["screen recording at 60 fps or more", LOM_HARNESS],
                   why="Position after Stop depends on scheduler internals (`0x101a54364`) and the untraced song setter `0x10270087c`; report timing depends on the audio thread (page: 'Why runtime')",
                   flags=["tool gap: the 10 ms `is_playing` sampling needs a LOM harness that is not established; without it only the display and saved CurrentTime are observable"]),
    # ---- N5 / H4 devices (sessions C, E, J, X)
    "P4-N5-01": O("C", 1, 60, "high", "debugging needs a re-signed disposable copy or a SIP change; never on the installed app", {"requirements": [], "candidates": ["DEV-M01", "DEV-M02", "DEV-M03", "CD-C02"], "questions": ["Q-006"]},
                  "SPEC-CORPUS-DEVICE (candidates CD-C01–CD-C08): the Corpus position-range contradiction; DEV-M01–M03",
                  ["Attach the debugger to the disposable copy; break or log on `_SetParameterA` in Amp, Electric and Corpus", "Load one shipped preset per device and the two Corpus ExcitationX copies", "Record (index, value) pairs; compare with `n5-device-mapping-v1/out/live_index_map.tsv`"],
                  ["FX-ENV", "FX-APP-DEBUG", "FX-N5-PRESETS"], app_copy="re-signed disposable copy (debuggable)", tools=DBG,
                  why="Value chain into the bundle is inferred and the position range contradicts the bundle's expected input (page 'Static evidence so far'; corpus-dsp-static 'Open: position range')"),
    "P4-N5-02": O("C", 2, 20, "high", "as P4-N5-01", {"requirements": [], "candidates": ["DEV-M08"], "questions": ["Q-006"]}, "DEV-M08 dual-mono instance count",
                  ["Break on `_CreateInstanceU`", "Insert each of the seven devices once; record hit counts"], ["FX-ENV", "FX-APP-DEBUG"], app_copy="re-signed disposable copy (debuggable)", tools=DBG,
                  why="Only the selector 4 path is traced; the Live-side instance creation for DualMono is unknown"),
    "P4-H4-01": O("E", 1, 60, "low", "saves to the test folder only", {"requirements": [], "candidates": ["DEV-C01", "DEV-C02", "DEV-C03", "DEV-C04", "DEV-C05", "DEV-C06", "DEV-C07", "DEV-C08", "DEV-C09", "DEV-M04"], "questions": ["Q-006"]},
                  "Device candidates DEV-C01–C09 (no device spec drafted yet)",
                  ["Insert each of the seven devices fresh into an empty set; save each as .adv", "Load each default or shipped preset; re-save as .adv", "Save one set holding all seven; diff all XML against inputs"],
                  DOC_FX + ["FX-NEWSET"], tools=BASE_TOOLS, why="DEV-C01–C09 rest on shipped content written by earlier builds, not on a 12.4.3 save",
                  merge={"group": "M-DEV-DEFAULTS", "relation": "primary", "with": ["P4-H4-03", "P4-N5-03"]}),
    "P4-N5-03": O("E", 2, 0, "low", "covered by P4-H4-01", {"requirements": [], "candidates": ["DEV-M04", "DEV-C08"], "questions": ["Q-006"]}, "DEV-M04/DEV-C08 default source",
                  ["Read `PickupAmpIn` from P4-H4-01's fresh Electric save"], DOC_FX, why="Constructor sets 0.5, the Defaults preset 0.42; which applies at insert is not traced",
                  merge={"group": "M-DEV-DEFAULTS", "relation": "near-duplicate", "with": ["P4-H4-01", "P4-H4-03"]}),
    "P4-H4-02": O("E", 3, 30, "low", "test presets only", {"requirements": [], "candidates": ["DEV-C05", "DEV-M06"], "questions": ["Q-006"]}, "DEV-C05/DEV-M06 out-of-domain handling",
                  ["Load each edited Amp and Analog preset copy", "Capture the displayed value and any dialog; re-save; diff"], DOC_FX + ["FX-H4-PRESETS"], tools=BASE_TOOLS,
                  why="The document reader's clamp/reject/keep behavior for out-of-domain values is not traced"),
    "P4-H4-04": O("E", 4, 30, "low", "a dump script in the test account only", {"requirements": [], "candidates": ["DEV-M05", "DEV-C10"], "questions": ["Q-006"]}, "DEV-M05 labels and units",
                  ["Only if the parameter API is confirmed present: run the dump script against each device", "Retain one table per device"], DOC_FX + ["FX-LOM"], tools=[LOM_HARNESS],
                  why="Units appear only as engine strings; display mapping is Live-side and untraced",
                  flags=["tool gap: the dump script and its API are not established; the record makes the probe conditional on them"]),
    "P4-H4-05": O("E", 5, 15, "low", "changes the audio device rate; restore afterwards", {"requirements": [], "candidates": [], "questions": ["Q-006"]}, "Device signal behavior at unsupported rates (no spec drafted)",
                  ["Set the audio device to 32 kHz", "Insert Amp; play a generated tone; capture output presence and any message"], DOC_FX + ["FX-AUDIO32K", "FX-WAV"], hardware=["audio device that offers 32 kHz"],
                  tools=["output level meter or loopback capture"], why="Model selection by sample rate and the `Sample rate not supported` path are not traced Live-side"),
    "P4-H4-03": O("J", 1, 15, "medium", "edits `Core Library/Defaults` inside the disposable copy, which may break its code-signature seal", {"requirements": [], "candidates": ["DEV-C08", "DEV-M04"], "questions": ["Q-006"]},
                  "DEV-C08 Defaults source",
                  ["Fresh-insert values come from P4-H4-01", "In a second disposable copy, edit `Defaults/Instruments/Analog.adv` (one Manual value); insert Analog; save"], ["FX-ENV", "FX-APP-MODIFIED"], app_copy="modified disposable copy",
                  tools=BASE_TOOLS, why="No default preset exists for three devices; whether `Defaults/*.adv` is read at insert is not traced",
                  merge={"group": "M-DEV-DEFAULTS", "relation": "near-duplicate", "with": ["P4-H4-01", "P4-N5-03"]}),
    "P4-N5-04": O("J", 2, 20, "high", "removes `Corpus.bundle` from a disposable copy; skip if the copy will not launch", {"requirements": [], "candidates": ["DEV-M10"], "questions": ["Q-006"]}, "DEV-M10 load-failure notice",
                  ["In a modified copy without `Corpus.bundle`, insert Corpus", "Capture notice text, device state and the saved set"], ["FX-ENV", "FX-APP-MODIFIED"], app_copy="modified disposable copy",
                  tools=BASE_TOOLS, why="The sender and text of the load-failure notice are untraced"),
    # ---- N4 helpers (sessions G, H, I, J)
    "PRB-N4-01": O("H", 1, 30, "medium", "places test plug-ins in system and user plug-in folders", {"requirements": [], "candidates": ["PD-02", "PD-11", "PD-14"], "questions": ["Q-016"]},
                   "Plug-in discovery candidates PD-02/PD-11/PD-14 (no spec drafted)",
                   ["Install one healthy test VST3 in each of the system and user folders", "For each Plug-In Sources configuration, Rescan and modifier-Rescan; capture argv"], ["FX-ENV", "FX-APP", "FX-VST3"], plugins=["healthy test VST3 x2"],
                   tools=SCAN_TOOLS, why="Argument assembly is now traced (N4 'Plug-in scanner'); folder values, domain IDs and the modifier key are runtime-confirmed only by a capture",
                   merge={"group": "M-SCAN-ARGV", "relation": "primary", "with": ["PRB-H1-01"]}),
    "PRB-N4-02": O("H", 3, 0, "medium", "covered by PRB-H1-02 and PRB-H1-04", {"requirements": [], "candidates": ["PD-10", "PD-12"], "questions": ["Q-016"]}, "PD-10/PD-12 release (Q-016)",
                   ["Record the relaunch log lines and launch counts during PRB-H1-02 and PRB-H1-04"], ["FX-ENV", "FX-APP", "FX-VST3"], plugins=["crash VST3", "60 distinct test VST3s"], tools=SCAN_TOOLS,
                   why="Lifecycle table is static; whether a crash loop or chunking ends as predicted needs execution",
                   merge={"group": "M-SCAN-RELAUNCH", "relation": "near-duplicate", "with": ["PRB-H1-02", "PRB-H1-04"]}),
    "PRB-N4-03": O("G", 1, 10, "low", "read-only capture", {"requirements": [], "candidates": [], "questions": ["Q-014"]}, "Q-014 index launch contract",
                   ["Start Live with an empty user library", "Capture the Index argv and copy `com.ableton.index.*.txt` while it exists", "Stop if no index process within 60 s of the main window"], ["FX-ENV", "FX-APP"],
                   tools=["process-argument capture", "file copy of the options file"], why="Option values (db-path, folder) are computed at run time from path services",
                   merge={"group": "M-INDEX-LAUNCH", "relation": "primary", "with": ["PRB-H2-01"]}),
    "PRB-N4-04": O("G", 9, 40, "medium", "about 100 forced helper kills; index database churn in the test account", {"requirements": [], "candidates": [], "questions": ["Q-014", "Q-015"]}, "Q-014/Q-015 restart caps",
                   ["`kill -9` the index helper on each relaunch until `Giving up`; count launches", "Repeat for add-ons (cap 10)"], ["FX-ENV", "FX-APP"], tools=["kill loop script on the macOS host", "Log.txt"],
                   why="Caps are compare constants in code; whether the count resets or other paths relaunch needs execution"),
    "PRB-N4-06": O("G", 10, 40, "medium", "runs a disposable copy from a nearly full disk image; network must stay off so no update downloads", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Q-015 web connector start conditions",
                   ["Copy `web_connector_args_<pid>.txt` with auto-update on and off", "Repeat with the copy on a disk image with < 3 GiB free"], ["FX-ENV", "FX-APP", "FX-SMALLVOL"], tools=["file copy of the args file"],
                   why="The free-space field and the preference wiring are inferred; the args file shows them directly"),
    "PRB-N4-07": O("G", 7, 10, "low", "a renamed `sleep` process only", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Q-015 swapper guard",
                   ["Start a process named `Ableton Swapper`", "Launch Live; capture the dialog and exit status (expected 42)"], ["FX-ENV", "FX-APP", "FX-SWAPPER-PROC"], tools=["shell to read exit status"],
                   why="Dialog presentation and exit path are runtime; static trace gives the code only"),
    "PRB-N4-09": O("G", 8, 15, "low", "converts a generated clip only", {"requirements": [], "candidates": [], "questions": ["Q-013"]}, "Q-013 MultiF0 default on arm64",
                   ["Drop a generated chord WAV into a set", "Convert Harmony to New MIDI Track; capture the Log.txt line"], ["FX-ENV", "FX-APP", "FX-WAV"], tools=["Log.txt"],
                   why="Static trace shows the default branch; the log line confirms it runs"),
    "PRB-N4-08": O("I", 3, 15, "medium", "kills the Push3 helper", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Q-015 Push channel roles and relaunch",
                   ["With Push 3 connected, run `lsof -U` on Live and Push3", "`kill -9` Push3; time the relaunch; repeat three times"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"],
                   tools=["lsof", "ps polling"], why="Bind/connect roles and the 1500 ms timer are static; a capture confirms them",
                   merge={"group": "M-PUSH3-PROC", "relation": "near-duplicate", "with": ["P5-02"]}),
    "PRB-N4-05": O("J", 3, 45, "high", "replaces a helper executable in a disposable copy", {"requirements": [], "candidates": [], "questions": ["Q-015", "Q-016"]}, "Q-015/Q-016 shared process-controller timeouts",
                   ["In a modified copy, replace one helper with a stub that never sends sync; time the kill", "Replace with a stub that ignores shutdown; quit Live; time the kill", "Three repeats each"],
                   ["FX-ENV", "FX-APP-MODIFIED", "FX-STUB"], app_copy="modified disposable copy", tools=["ps polling with timestamps"],
                   why="Timer units are assumed (milliseconds) and the kill slot `+0x38` is unknown", flags=["related: PRB-H1-03 tests the connected-then-hung case (no timeout predicted)"]),
    # ---- H1 scanner (session H)
    "PRB-H1-01": O("H", 2, 0, "medium", "covered by PRB-N4-01", {"requirements": [], "candidates": ["PD-02", "PD-11", "PD-14"], "questions": ["Q-016"]}, "as PRB-N4-01",
                   ["Run as PRB-N4-01 (adds the custom-folder and VST2 toggles)"], ["FX-ENV", "FX-APP", "FX-VST3"], plugins=["healthy test VST3 x2"], tools=SCAN_TOOLS,
                   merge={"group": "M-SCAN-ARGV", "relation": "duplicate", "with": ["PRB-N4-01"]}),
    "PRB-H1-02": O("H", 4, 30, "medium", "crashing test plug-in in the user plug-in folder", {"requirements": [], "candidates": ["PD-10"], "questions": ["Q-016"]}, "PD-10 release (Q-016 forbids release without this probe)",
                   ["Install the crash VST3 beside a healthy one; Rescan", "Count scanner launches; read scanstate from a database copy after each", "Rescan manually until scanstate 2 or three rescans without change"],
                   ["FX-ENV", "FX-APP", "FX-VST3"], plugins=["crash VST3", "healthy VST3"], tools=SCAN_TOOLS,
                   merge={"group": "M-SCAN-RELAUNCH", "relation": "primary", "with": ["PRB-N4-02"]}),
    "PRB-H1-05": O("H", 5, 20, "medium", "as PRB-H1-02", {"requirements": [], "candidates": ["PD-07", "PD-10"], "questions": ["Q-016"]}, "PD-07 fingerprint rule",
                   ["Replace the disabled module's executable with a healthy build; Rescan", "`touch` a healthy module's executable; Rescan; read fingerprint and scanstate"], ["FX-ENV", "FX-APP", "FX-VST3"],
                   plugins=["crash VST3 (from PRB-H1-02)", "healthy VST3"], tools=SCAN_TOOLS, depends=["PRB-H1-02"]),
    "PRB-H1-03": O("H", 6, 25, "medium", "hanging plug-in; the scanner may need a manual kill at the cap", {"requirements": [], "candidates": ["PD-01"], "questions": ["Q-016"]}, "Q-016 timeout policy",
                   ["Install the hang VST3; Rescan", "Time scanner start to exit; record signal, scanstate and log lines", "Stop at exit or 15 minutes, then kill the scanner"], ["FX-ENV", "FX-APP", "FX-VST3"],
                   plugins=["hang VST3"], tools=SCAN_TOOLS, flags=["N4 now predicts statically that a connected, hung scanner is not timed out by Live", "related: PRB-N4-05"]),
    "PRB-H1-04": O("H", 7, 40, "medium", "60 test modules in the user plug-in folder", {"requirements": [], "candidates": ["PD-12"], "questions": ["Q-016"]}, "PD-12 release (Q-016 forbids release without this probe)",
                   ["Install 60 distinct test VST3s; Rescan", "Count launches and confirmed modules per launch until all 60 are listed"], ["FX-ENV", "FX-APP", "FX-VST3"], plugins=["60 distinct test VST3s"], tools=SCAN_TOOLS,
                   merge={"group": "M-SCAN-RELAUNCH", "relation": "primary", "with": ["PRB-N4-02"]}, flags=["N4: Live passes `--limit` only under a debug option, so the scanner default 50 applies"]),
    "PRB-H1-06": O("H", 8, 15, "low", "uses an Apple-supplied AU", {"requirements": [], "candidates": ["PD-14"], "questions": ["Q-016"]}, "PD-14 AU discovery location",
                   ["Enable Use Audio Units v2; Rescan", "Capture helper processes and arch=1 rows in a database copy"], ["FX-ENV", "FX-APP", "FX-AU"], plugins=["one AU v2 effect (Apple-supplied, availability to establish)"], tools=SCAN_TOOLS),
    "PRB-H1-07": O("H", 9, 10, "low", "read-only listing", {"requirements": [], "candidates": [], "questions": ["Q-016"]}, "Q-016 database folder",
                   ["Take `--db` from PRB-N4-01's capture", "List the preferences and cache folders before and after one Rescan"], ["FX-ENV", "FX-APP"], tools=SCAN_TOOLS, depends=["PRB-N4-01"]),
    "PRB-H1-08": O("H", 10, 25, "medium", "copies and a symlink in plug-in folders", {"requirements": [], "candidates": ["PD-02"], "questions": ["Q-016"]}, "Q-016 duplicate presentation",
                   ["Same VST3 in system and user folders (copy, then symlink); Rescan", "Two bundles with one class ID; Rescan; read rows and browser entries"], ["FX-ENV", "FX-APP", "FX-VST3"],
                   plugins=["healthy VST3 copy and symlink", "two bundles sharing a class ID"], tools=SCAN_TOOLS),
    # ---- H2 index (sessions G, J, X)
    "PRB-H2-01": O("G", 2, 0, "low", "covered by PRB-N4-03", {"requirements": [], "candidates": [], "questions": ["Q-014"]}, "as PRB-N4-03",
                   ["Run as PRB-N4-03"], ["FX-ENV", "FX-APP"], merge={"group": "M-INDEX-LAUNCH", "relation": "duplicate", "with": ["PRB-N4-03"]}),
    "PRB-H2-02": O("G", 3, 5, "low", "query on a database copy", {"requirements": [], "candidates": ["BI-C09"], "questions": ["Q-014"]}, "Q-014 database name and version",
                   ["List the db-path folder from PRB-N4-03", "On a copy: SELECT version, platform FROM version"], ["FX-ENV", "FX-APP"], tools=["sqlite3 on a copy"], depends=["PRB-N4-03"]),
    "PRB-H2-03": O("G", 4, 20, "low", "user folder with generated WAVs", {"requirements": [], "candidates": ["BI-C07"], "questions": ["Q-014"]}, "BI-C07 change detection",
                   ["Add the user folder with three WAVs", "Add, rename, delete one file while Live runs; capture browser and files table with timestamps"], ["FX-ENV", "FX-APP", "FX-WAV"], tools=["sqlite3 on a copy", "screen capture"]),
    "PRB-H2-05": O("G", 5, 25, "medium", "mounts and unmounts a test disk image", {"requirements": [], "candidates": ["BI-C08", "BI-C11"], "questions": ["Q-014"]}, "BI-C08/C11 retention",
                   ["Tag and color a sample on the removable image", "Unmount, remount, then move it within a user folder; capture browser and rows each step"], ["FX-ENV", "FX-APP", "FX-WAV", "FX-REMOVABLE"], tools=["hdiutil", "sqlite3 on a copy"]),
    "PRB-H2-06": O("G", 11, 40, "medium", "replaces the test account's index database three times", {"requirements": [], "candidates": ["BI-C09"], "questions": ["Q-014"]}, "BI-C09 rebuild behavior",
                   ["Quit Live; substitute (a) truncated, (b) version 99999, (c) foreign-platform copies", "Start Live each time; capture messages, indicator file, new file and keyword survival"], ["FX-ENV", "FX-APP"], tools=["sqlite3 on a copy"]),
    "PRB-H2-08": O("G", 12, 20, "low", "preference toggle in the test account", {"requirements": [], "candidates": [], "questions": ["Q-014"]}, "Q-014 sound-similarity scheduling",
                   ["Fresh database with one user sample folder", "Toggle the preference; capture fe_values counts until stable 5 min"], ["FX-ENV", "FX-APP", "FX-WAV"], tools=["sqlite3 on a copy"]),
    "PRB-H2-09": O("G", 6, 15, "low", "test media files only", {"requirements": [], "candidates": ["BI-C05"], "questions": ["Q-014"]}, "BI-C05 presentation of bad media",
                   ["Add a folder with the truncated WAV, zero-byte .als, .xyz and .wma", "Capture browser and files rows"], ["FX-ENV", "FX-APP", "FX-MEDIA-BAD"], tools=["sqlite3 on a copy", "screen capture"],
                   flags=["fixture gap: no .wma source is established; the .wma item may be dropped"]),
    "PRB-H2-04": O("J", 4, 15, "medium", "tagging a Core Library preset may write inside the disposable copy's bundle", {"requirements": [], "candidates": ["BI-C08"], "questions": ["Q-014"]}, "BI-C08 tag persistence",
                   ["Tag one user sample and one Core Library preset", "Find new or changed *.xmp under any 'Ableton Folder Info'; stop after 2 min and a quit with no change"], ["FX-ENV", "FX-APP-MODIFIED", "FX-WAV"], app_copy="modified disposable copy (may be written)",
                   tools=["find -newer", "screen capture"]),
    "PRB-H2-07": O("X", 2, 20, "medium", "requires the destination pack to be installed; installing one may need network and an account", {"requirements": [], "candidates": ["BI-C10"], "questions": ["Q-014"]}, "BI-C10 legacy reference redirection",
                   ["Only if a matching destination pack is already installed: open a set whose FileRef matches one shipped src row", "Capture where the sample loads from; re-save and inspect"], ["FX-ENV", "FX-APP", "FX-FILEREF-SET"],
                   flags=["prerequisite gap: destination-pack availability without network or sign-in is not established"]),
    # ---- P5 Push hardware (session I)
    "P5-01": O("I", 1, 15, "medium", "connects Push 3 to the test account", {"requirements": [], "candidates": [], "questions": ["Q-015", "Q-005"]}, "Push scope decision (Q-005) and Q-015",
               ["Start Live with Push 3 in Control mode; capture `ps -axo pid,ppid,args`", "Repeat without Push 3"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["ps"],
               why="Helper launch arguments are now traced Live-side (N4 'Push 3'); hardware-gated launch needs a capture",
               flags=["related: M-PUSH3-PROC"]),
    "P5-02": O("I", 2, 10, "low", "read-only capture", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Q-015 channel roles",
               ["`lsof -U -a -p` for Live and Push3; list `$TMPDIR`", "Attribute the listener of each of the three channel names"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["lsof"],
               why="Bind/connect roles are static (N4); socket paths exist only at run time",
               merge={"group": "M-PUSH3-PROC", "relation": "primary", "with": ["PRB-N4-08"]}),
    "P5-03": O("I", 4, 30, "medium", "force-kills and stops Live; unsaved state lost", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push helper watchdog contract",
               ["(a) `kill -9` Live; time the helper's exit; read Push3.log", "(b) `kill -STOP` Live for 30 s; observe; `kill -CONT`", "Three repeats each"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["ps polling with timestamps"],
               why="Watchdog interval derives from decompiled helper code; timing needs measurement"),
    "P5-04": O("I", 5, 15, "low", "plugging and unplugging only", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push hotplug behavior",
               ["Launch with Push 3 unplugged; then plug it in; capture processes and logs"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["ps", "Log.txt"],
               why="Presence flag `+0x94` writer is unknown (N4)"),
    "P5-05": O("I", 6, 20, "high", "USB capture on macOS may need privileged capture setup or SIP changes", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push display protocol (scope-dependent)",
               ["Capture the bulk OUT endpoint for 10 s with a known screen"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["USB capture tool (not established)"],
               why="Frame encoding is in helper code; a capture confirms sizes and rate", flags=["tool gap: USB capture capability on the macOS host is not established"]),
    "P5-06": O("I", 7, 15, "medium", "connects Push 2", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push 2 versus Push 3 path",
               ["Connect Push 2 instead; capture which display process runs"], ["FX-ENV", "FX-APP", "FX-PUSH2"], hardware=["Push 2"], tools=["ps"],
               why="Selection between Push2DisplayProcess and Push3 by hardware type is untraced"),
    "P5-07": O("I", 8, 10, "medium", "network interface up for local multicast; no internet route", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push network behavior in Control mode",
               ["Run `tcpdump` on 224.76.78.75 and DNS for the update host for 5 minutes in Control mode"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], network="local link only (no internet route; attempts still visible)",
               tools=["tcpdump"], why="Discovery and update traffic are runtime only",
               flags=["capture may contain identifiers; keep the pcap out of Git until reviewed"]),
    "P5-08": O("I", 9, 15, "low", "read-only observation", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push MIDI path",
               ["Press one pad; observe CoreMIDI (MIDI Monitor) and `lsof` for the push-to-live channel"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["MIDI monitor", "lsof"],
               why="Which transport carries pad input is a runtime choice"),
    "P5-09": O("I", 10, 10, "low", "read-only capture", {"requirements": [], "candidates": [], "questions": ["Q-015"]}, "Push real-time segment",
               ["`vmmap` and `lsof` on the helper; record the backing name"], ["FX-ENV", "FX-APP", "FX-PUSH3"], hardware=["Push 3"], tools=["vmmap", "lsof"],
               why="Shared-memory creation is untraced Live-side"),
    # ---- assigned records without a prepared probe
    "P4B-CORPUS-01": O("X", 3, None, "unknown", "not designed", {"requirements": [], "candidates": ["CD-C01", "CD-C02", "CD-C03", "CD-C04", "CD-C05", "CD-C06", "CD-C07", "CD-C08"], "questions": ["Q-006", "Q-007"]},
                       "SPEC-CORPUS-DEVICE; this is measured audio comparison (FEAT-AUDIO), closer to verification than to a Phase 4 probe", [], [],
                       why="Output signal properties need measurement under ADR 0002 ('audio output where numerical fidelity is required')",
                       flags=["incomplete: no minimal input", "incomplete: no discriminating observation", "incomplete: no stop condition", "needs an audio render/capture harness and tolerances (Q-001)"]),
    "P4B-H6-01": O("X", 4, None, "high", "observing real update traffic needs network and could let the updater act on the installation", {"requirements": [], "candidates": [], "questions": ["Q-015"]},
                   "Q-015 helper runtime order and traffic", [], [], network="internet (conflicts with the batch safety policy)",
                   why="Page: runtime order, timing and actual network traffic stay unknown until a Phase 4 capture",
                   flags=["incomplete: no discriminating observation", "incomplete: no stop condition", "partly covered by PRB-N4-06 and PRB-N4-07"]),
    "P4B-T1-01": O("X", 5, 0, "low", "superseded", {"requirements": [TS_REQ + "003", TS_REQ + "007", TS_REQ + "008"], "candidates": ["P1-A", "P1-B", "P1-C", "P1-D", "P1-E", "P1-F"], "questions": ["Q-012"]},
                   "None beyond PRB-N1-01/02/07/08", [], [], why="Page: 'An optional bounded reference probe should discriminate the first material ambiguity'",
                   merge={"group": "M-T1-LOOP", "relation": "duplicate (superseded)", "with": ["PRB-N1-01", "PRB-N1-02", "PRB-N1-07", "PRB-N1-08"]},
                   flags=["incomplete: no stop condition", "incomplete: discriminating observation unspecified", "gap: P1-F (undo/redo of loop enable) is covered by no prepared probe"]),
}

SESSIONS = [
    {"id": "S0", "title": "Setup and identity pinning", "minutes_fixed": 45, "prerequisites": "All batch safety measures; tool availability checks"},
    {"id": "A", "title": "Handoff blockers: saves, precedence and container failures", "prerequisites": "Disposable copy; N1 variants; N2 cases"},
    {"id": "B", "title": "Transport timing (S3 escalation)", "prerequisites": "Screen recording at 60 fps or more; LOM harness if approved"},
    {"id": "C", "title": "Device engine trace (Corpus position range)", "prerequisites": "Debuggable re-signed disposable copy (user decision)"},
    {"id": "D", "title": "Remaining document-load probes", "prerequisites": "As session A"},
    {"id": "E", "title": "Built-in device saves and defaults", "prerequisites": "Disposable copy; preset copies; 32 kHz audio device for P4-H4-05"},
    {"id": "F", "title": "MIDI remote-script profiles", "prerequisites": "IAC bus, MIDI sender and monitor; probe profiles"},
    {"id": "G", "title": "Helpers and browser index without plug-ins or hardware", "prerequisites": "Disposable copy; small and removable disk images; generated media"},
    {"id": "H", "title": "Plug-in scanner with test plug-ins", "prerequisites": "Test VST3 builds; process-argument capture"},
    {"id": "I", "title": "Push hardware", "prerequisites": "Push 3 (and Push 2 for P5-06)"},
    {"id": "J", "title": "Modified-copy probes (run last, then delete the copy)", "prerequisites": "Second disposable copy that may be modified; stub helpers"},
    {"id": "X", "title": "Deferred or not runnable as prepared", "prerequisites": "Static work or a user decision first"},
]

FIXTURES = [
    {"id": "FX-ENV", "kind": "environment", "status": "to prepare at the sitting", "description": "Separate macOS user account (preferred) or a moved-aside backup of Live's preferences, application-support, cache and User Library folders; record their paths and hashes before and after; network off; no account sign-in. Live's authorization state in a new account is not established."},
    {"id": "FX-APP", "kind": "application copy", "status": "to prepare at the sitting", "description": "Disposable copy of the installed app made with `ditto`; verify the universal executable SHA-256 52289af638f1b26590c84a9bc08eabdc35127883087057add909d2718a7a35ef and the Schema folder digest before use; never modify the installed app."},
    {"id": "FX-APP-DEBUG", "kind": "application copy", "status": "needs user decision", "description": "Disposable copy that a debugger can attach to (for example re-signed ad hoc with a debugging entitlement), or a SIP change; feasibility and effect on licensing and device bundles not established."},
    {"id": "FX-APP-MODIFIED", "kind": "application copy", "status": "needs user decision", "description": "Second disposable copy that probes may modify (helper replaced, Corpus.bundle removed, Defaults edited, Core Library tagged); whether a modified copy still launches is not established; delete after session J."},
    {"id": "FX-N1-BASE", "kind": "document", "status": "exists", "path": f"{R2}/n2-container-v1/cases/N2-001.als", "sha256": "af57ff8f9eb1c2c51220ef6633a58838532350d53640df5f48dc01659023c043", "description": "Byte-identical to the shipped `Core Library/Lessons/Sets/Recording Audio.als`; the PRB-N1-07 input and the base of every N1 variant."},
    {"id": "FX-N1-VAR", "kind": "documents", "status": "to construct before the sitting (not built here)", "description": "Edited gzip copies of FX-N1-BASE: N1-01 LoopOn 1/0/TRUE/empty (4); N1-02 base with LoopStart 4 and LoopLength 8, then three omissions (3, plus the edited base); N1-03 six out-of-range values; N1-04 three Manual/EnumEvent pairs; N1-05 three tempo variants; N1-06 three codes; N1-08 three variants now plus one built at the sitting from PRB-N1-07's SchemaChangeCount. 25 files; a builder script analogous to n2 `make_cases.py` with a hash list."},
    {"id": "FX-N2-CASES", "kind": "documents", "status": "exists", "path": f"{R2}/n2-container-v1/cases/", "index": f"{R2}/n2-container-v1/cases.json", "description": "N2-002 to N2-027 with SHA-256 in cases.json. Used: 002, 003, 005, 006, 008, 010, 011, 012, 013, 014, 015, 017, 018, 019, 020, 021, 022, 023, 024, 025, 026, 027. Missing: N2-019 with Creator removed (PRB-N2-04), to construct."},
    {"id": "FX-NEWSET", "kind": "document", "status": "created in the app at the sitting", "description": "File > New Live Set from the factory template (PRB-N2-01, ESC-N3-01, P4-H4-01)."},
    {"id": "FX-S4-PROFILES", "kind": "configuration files", "status": "to write before the sitting (not built here)", "description": "UserConfiguration.txt directories for PRB-S4-01 to 16 exactly as each record's minimal input; about 25 directories. The 55 draft-case fixtures in s4-midi-v1/fixtures/ exist but none matches a probe input."},
    {"id": "FX-MIDI", "kind": "tools", "status": "to establish", "description": "IAC Driver bus enabled; a sender for single CC/note messages with timed holds; a MIDI monitor for output bytes. None is established on the macOS host."},
    {"id": "FX-WAV", "kind": "media", "status": "to generate (own content)", "description": "Generated sine tones and one chord: 16 tones for the Drum Rack (PRB-S4-08), three WAVs for the user folder (PRB-H2-03/05/08), a chord for Convert Harmony (PRB-N4-09), a tone for P4-H4-05."},
    {"id": "FX-MEDIA-BAD", "kind": "media", "status": "to construct", "description": "Truncated WAV (from FX-WAV), zero-byte .als, arbitrary .xyz; .wma has no established source."},
    {"id": "FX-H4-PRESETS", "kind": "documents", "status": "to construct before the sitting (not built here)", "description": "Copies of one shipped Amp preset and one Analog preset with Manual above max, below min, non-numeric, missing, and an enum past its maximum; domains from h4-devices-v1/out/param_table.tsv."},
    {"id": "FX-N5-PRESETS", "kind": "documents", "status": "to construct before the sitting (not built here)", "description": "One shipped preset per device (Amp, Electric, Corpus) used as-is, plus two Corpus preset copies with ExcitationX 0 and 1."},
    {"id": "FX-VST3", "kind": "plug-in folders", "status": "to build (needs user approval and a toolchain)", "description": "From the public VST3 SDK samples: two healthy builds, one that aborts in GetPluginFactory, one that blocks forever, 60 copies with distinct bundle names and class IDs, two bundles sharing one class ID; ad hoc signed. Install into the test account's ~/Library and, for PRB-N4-01/H1-08, /Library (admin, affects every user)."},
    {"id": "FX-AU", "kind": "plug-in", "status": "to establish", "description": "An Apple-supplied AU v2 effect present on macOS."},
    {"id": "FX-STUB", "kind": "executables", "status": "to write (needs user approval)", "description": "Two stub helpers for PRB-N4-05: one never sends sync, one ignores shutdown."},
    {"id": "FX-SWAPPER-PROC", "kind": "process", "status": "trivial at the sitting", "description": "A copy of /bin/sleep named `Ableton Swapper`, started before Live (PRB-N4-07)."},
    {"id": "FX-SMALLVOL", "kind": "disk image", "status": "to create at the sitting", "description": "A disk image holding a disposable app copy with < 3 GiB free (PRB-N4-06)."},
    {"id": "FX-REMOVABLE", "kind": "disk image", "status": "to create at the sitting", "description": "A mountable image acting as a removable volume with one sample (PRB-H2-05)."},
    {"id": "FX-FILEREF-SET", "kind": "document", "status": "blocked", "description": "A set whose sample FileRef matches one shipped filerefmap.db src row (type 2, empty pack id) whose destination pack is installed; pack availability without network is not established."},
    {"id": "FX-LOM", "kind": "harness", "status": "needs user decision", "description": "A Max for Live device or control-surface script that samples `is_playing`/`current_song_time` every 10 ms (ESC-N3-01) or dumps parameter tables (P4-H4-04); API availability in 12.4.3 not established."},
    {"id": "FX-AUDIO32K", "kind": "hardware", "status": "to establish", "description": "An audio device that offers 32 kHz (P4-H4-05)."},
    {"id": "FX-PUSH3", "kind": "hardware", "status": "availability not established", "description": "Ableton Push 3 (Control mode). Decline any firmware-update prompt."},
    {"id": "FX-PUSH2", "kind": "hardware", "status": "availability not established", "description": "Ableton Push 2 (P5-06 only)."},
]

EXISTING_REFERENCE_FILES = [
    f"{R2}/n1-transport-state-v1/number-format-check.txt",
    f"{R2}/n2-container-v1/cases.json",
    f"{R2}/n5-device-mapping-v1/out/live_index_map.tsv",
    f"{R2}/h4-devices-v1/out/param_table.tsv",
    f"{R2}/h2-index-v1/out/file-type-registry.tsv",
]


def build():
    recs = json_records() + TABLE_RECORDS
    ids = [r["id"] for r in recs]
    assert len(ids) == len(set(ids)), "duplicate ids"
    assert set(ids) == set(OV), (set(ids) ^ set(OV))
    fx_ids = {f["id"] for f in FIXTURES}
    sess_ids = {s["id"] for s in SESSIONS}
    out = []
    for r in recs:
        o, orig = OV[r["id"]], r["original"]
        assert o["session"] in sess_ids and set(o["fixtures"]) <= fx_ids, r["id"]
        for dep in o["depends"] + ((o["merge"] or {}).get("with") or []):
            assert dep in OV, (r["id"], dep)
        derived = ["procedure", "prerequisites", "risk_to_host", "estimated_minutes", "unblocks"]
        why = orig["why_static_insufficient"]
        if not why and o["why"]:
            why = o["why"]; derived.append("why_static_insufficient")
        if not orig["affected"] or o["mapped_affected"]:
            derived.append("affected_ids")
        flags = list(o["flags"])
        for k in ("discriminating_observation", "stop_condition"):
            if not orig[k] and not any(k.replace("_", " ").split()[-1] in f for f in flags):
                flags.append(f"incomplete: no {k.replace('_', ' ')}")
        out.append({
            "id": r["id"], "original_id": r["original_id"], "packet": r["packet"], "source": r["source"],
            "session": o["session"], "order": o["order"],
            "question": orig["question"],
            "existing_evidence": orig["existing_evidence"],
            "why_static_insufficient": why,
            "affected_ids": o["affected"], "original_affected": orig["affected"],
            "prerequisites": {"app_copy": o["app_copy"], "network": o["network"], "hardware": o["hardware"], "plugins": o["plugins"],
                              "second_machine": False, "tools": o["tools"], "depends_on": o["depends"], "original": orig["prerequisites"]},
            "minimal_inputs": orig["minimal_input"], "fixtures": o["fixtures"],
            "procedure": o["procedure"],
            "discriminating_observation": orig["discriminating_observation"],
            "stop_condition": orig["stop_condition"],
            "risk_to_host": {"level": o["risk"], "note": o["risk_note"]},
            "estimated_minutes": o["minutes"],
            "unblocks": o["unblocks"],
            "merge": o["merge"], "flags": flags, "batch_derived_fields": derived,
        })
    out.sort(key=lambda x: ([s["id"] for s in SESSIONS].index(x["session"]), x["order"]))
    sessions = []
    for s in SESSIONS:
        members = [x for x in out if x["session"] == s["id"]]
        mins = s.get("minutes_fixed", 0) + sum(x["estimated_minutes"] or 0 for x in members)
        sessions.append({**{k: v for k, v in s.items() if k != "minutes_fixed"}, "estimated_minutes": mins, "records": [x["id"] for x in members]})
    groups = {}
    for x in out:
        if x["merge"]:
            groups.setdefault(x["merge"]["group"], []).append({"id": x["id"], "relation": x["merge"]["relation"]})
    incomplete = [x["id"] for x in out if any(f.startswith("incomplete") for f in x["flags"])]
    sources = sorted({x["source"]["path"] for x in out})
    batch = {
        "schema": "phase4-probe-batch-v1", "id": "PHASE4-BATCH-V1", "created": "2026-10-17", "status": "prepared; not run",
        "target": "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS host only; universal executable SHA-256 52289af638f1b26590c84a9bc08eabdc35127883087057add909d2718a7a35ef",
        "policy": "ADR-0002 runtime escalation; one prepared sitting on the macOS host; not a gate for Phases 1-3; captures retained under analysis/ableton-live-12.4.3/r2/phase4-run-v1/<record id>/",
        "safety": ["Never run or modify the installed app; use FX-APP (and FX-APP-MODIFIED only in session J)",
                   "Separate macOS user account, or a recorded backup of Live's preference, support, cache and User Library folders",
                   "Network off unless a record's prerequisites.network says otherwise; never sign in to an account; decline update and firmware prompts",
                   "Record executable SHA-256 and preference-folder hashes before and after each session"],
        "counts": {"records": len(out), "with_original_id": sum(1 for x in out if x["original_id"]), "batch_assigned_id": sum(1 for x in out if not x["original_id"]),
                   "merge_groups": len(groups), "records_in_merge_groups": sum(len(v) for v in groups.values()),
                   "duplicate_or_near_duplicate": sum(1 for x in out if x["merge"] and x["merge"]["relation"] != "primary"),
                   "flagged_incomplete": len(incomplete)},
        "sessions": sessions, "merge_groups": groups, "flagged_incomplete": incomplete,
        "sources": [{"path": p, "sha256": sha(p)} for p in sources],
        "records": out,
    }
    plan = {"schema": "phase4-fixture-plan-v1", "id": "PHASE4-FIXTURES-V1", "created": "2026-10-17",
            "rule": "Do not construct Ableton documents from shipped content in this packet; constructed inputs are listed with recipes and built in a later, approved step",
            "fixtures": [{**f, "used_by": [x["id"] for x in out if f["id"] in x["fixtures"]]} for f in FIXTURES],
            "existing_reference_files": [{"path": p, "sha256": sha(p)} for p in EXISTING_REFERENCE_FILES]}
    for name, obj in (("batch.json", batch), ("fixture-plan.json", plan)):
        with open(os.path.join(OUT, name), "w") as f:
            json.dump(obj, f, indent=1, ensure_ascii=False); f.write("\n")
    files = sorted(n for n in os.listdir(OUT) if n != "manifest.json" and os.path.isfile(os.path.join(OUT, n)))
    man = {"schema": "evidence-manifest-v1", "packet": "Phase 4 batch v1", "created": "2026-10-17",
           "command": "python3 -I analysis/ableton-live-12.4.3/r2/phase4-batch-v1/build_batch.py (from the repository root)",
           "inputs": batch["sources"] + plan["existing_reference_files"], "excludes": ["manifest.json (self)"],
           "files": [{"path": n, "bytes": os.path.getsize(os.path.join(OUT, n)), "sha256": sha(os.path.join(OUT, n))} for n in files]}
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(man, f, indent=1); f.write("\n")
    return batch


if __name__ == "__main__":
    b = build()
    print(json.dumps(b["counts"]))
    for s in b["sessions"]:
        print(s["id"], s["estimated_minutes"], len(s["records"]), s["title"])
