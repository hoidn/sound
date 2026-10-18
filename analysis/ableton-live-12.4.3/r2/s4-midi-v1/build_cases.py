"""S4 draft acceptance cases for a midi-config-v2 candidate (analyst-side, not released).

Run: python3.11 -I build_cases.py <out dir>
Writes fixtures/<ID>/UserConfiguration.txt and draft-cases-v2.json.
Expected assignments are HAND-AUTHORED static derivations (see "derivation" rule
IDs, defined in RULES); they are not computed here. The checks below only verify
structure, ranges, fixture bytes, and that host-stdlib configparser (shown
equivalent to Live's shipped configparser for non-raising input, see
configparser-equivalence.json) parses each fixture and exposes each expected
option with the expected integer text. No Live code is imported or executed.
"""
import configparser, hashlib, io, json, sys
from pathlib import Path

RULES = {
    "R-CC": "_UserScript/__init__ parse_int L56-66 (range 128 bound L96); GenericScript is_valid_midi_identifier L24-25",
    "R-GCH": "create_instance L182-184 parse_channel; GenericScript.__init__ L83-95: valid GlobalChannel else 0",
    "R-PCH": "per-control channel tuples: listcomp L148-155, L285-291; GenericScript L239-249, L368-378, L147-155",
    "R-GONLY": "buttons/sends use global_channel only: GenericScript L136-137, L158-166, L274-283 (int not tuple), L313-316, L399-405",
    "R-ENC": "valid encoders compacted in slot order: GenericScript L366-388; width>8 -> 2 banks: _UserScript/DeviceComponent L16",
    "R-BANK": "valid Bank1-8 buttons compacted in slot order: GenericScript L339-363; DeviceComponent._bank_value L397",
    "R-MODE": "MapMode tokens elements_base L27-47; map_modes dictcomp L17; parse_map_mode L51-53 (absent -> Absolute)",
    "R-MSCOPE": "EncoderMapMode L170-171 -> encoders; VolumeMapMode L245-246 -> track/master/cue volume (make_mixer_encoder default L140); SendsMapMode L248-249 -> sends L293; CrossfaderMapMode L251-252 -> crossfader L205-212",
    "R-14": "EncoderElement MAX_14_BIT_CC=95 L27; __init__ L53-56: Absolute14Bit with CC>95 -> Absolute",
    "R-MBK": "MixerButtonsToggle: create_instance L255-258 (getboolean False -> NOTOGGLE); GenericScript L129-137: NOTOGGLE -> momentary else toggle; applies to strip and mixer bank buttons L158-166, L218-224",
    "R-DBK": "device and transport buttons momentary: GenericScript L312-313, L399-420 (NORELEASE never a key, L409)",
    "R-TGT": "target wiring: create_instance L159-171, L176-178, L224-269, L272-317; GenericScript L37-55, L183-302, L321-363, L412-425",
    "R-PAD": "pads read from [Globals] only: create_instance L188-220; note in range(128) L200; channel only read after valid note L201-204; -1 -> raw global L206-207; range(16) L209; (col,row)=(n%4,n//4) L210-211",
    "R-SEC": "sections tested with has_section (exact): create_instance L146, L175, L182, L223, L276, L283",
    "R-OPT": "configparser optionxform lower (L890); unknown keys never queried by create_instance",
    "R-LEX": "configparser defaults L611-616: delimiters = :, full-line # ; comments, no inline comments, DEFAULT section inherited via has_option/get; values stripped",
    "R-BOOL": "configparser BOOLEAN_STATES L608 via getboolean (case-insensitive)",
    "R-INT": "configparser getint -> int(); embedded CPython 3.11.6 int() string rules (Inferred: version string in Live.arm64 @95776493)",
    "D2": "_Tools/UserConfiguration.txt L18-27 message types/channels; L34-46 mode list",
    "D3": "_Tools/UserConfiguration.txt L59-66 pad geometry",
    "D4": "_Tools/UserConfiguration.txt L107-171 device controls",
    "D5": "_Tools/UserConfiguration.txt L175-267 mixer controls",
    "D6": "_Tools/UserConfiguration.txt L269-292 master/cue/crossfader, modes, toggle",
    "D7": "_Tools/UserConfiguration.txt L296-340 transport",
}
SECTIONS = ("Globals", "DeviceControls", "MixerControls", "TransportControls")
MODES = {"Absolute", "Absolute14Bit", "LinearSignedBit", "LinearSignedBit2", "LinearTwoCompliment",
         "LinearBinaryOffset", "AccelSignedBit", "AccelSignedBit2", "AccelTwoCompliment", "AccelBinaryOffset"}


def fx(g=(), d=(), m=(), t=(), names=SECTIONS, pre=()):
    body = [*pre]
    for name, lines in zip(names, (g, d, m, t)):
        if name is None:
            continue
        body += [f"[{name}]", *lines, ""]
    return "\n".join(body).rstrip("\n") + "\n"


def cc(sec, ctl, tgt, n, ch, mode=None, kind=None):
    a = {"section": sec, "control": ctl, "target": tgt, "message_type": "control-change", "number": n, "channel": ch}
    if mode:
        a["map_mode"] = mode
    if kind:
        a["button_kind"] = kind
    return a


def enc(slot, k, n, ch, mode="Absolute"):
    return cc("DeviceControls", f"Encoder{slot}", f"device-parameter:{k}", n, ch, mode)


def pad(i, n, ch):
    return {"section": "Globals", "control": f"Pad{i}Note", "target": f"drum-pad:{i}", "message_type": "note", "number": n, "channel": ch}


def mix(ctl, tgt, n, ch, mode=None, kind=None):
    return cc("MixerControls", ctl, tgt, n, ch, mode, kind)


def dev(ctl, tgt, n, ch):
    return cc("DeviceControls", ctl, tgt, n, ch, kind="momentary")


def tr(ctl, tgt, n, ch):
    return cc("TransportControls", ctl, tgt, n, ch, kind="momentary")


G5 = ["GlobalChannel: 5"]
TRANSPORT = [("Stop", "transport-stop"), ("Play", "transport-play"), ("Rec", "arrangement-record"),
             ("SessionRec", "session-record"), ("Over", "arrangement-overdub"), ("Metro", "metronome"),
             ("Loop", "arrangement-loop"), ("Rwd", "rewind"), ("Ffwd", "fast-forward"), ("PunchIn", "punch-in"),
             ("PunchOut", "punch-out"), ("NudgeUp", "nudge-up"), ("NudgeDown", "nudge-down"), ("TapTempo", "tap-tempo")]
BOOL = [("off", "momentary"), ("No", "momentary"), ("0", "momentary"), ("FaLsE", "momentary"),
        ("on", "toggle"), ("YES", "toggle"), ("1", "toggle")]

# (purpose, requirements, fixture text, assignments, device_parameter_banks, derivation rules)
CASES = [
    ("Single encoder uses global channel and default Absolute mode", "002 003 005 007",
     fx(G5, ["Encoder1: 10"]), [enc(1, 1, 10, 5)], 1, "R-CC R-GCH R-PCH R-ENC R-MODE D4"),
    ("Sparse encoder slots are compacted in slot order", "002 007",
     fx(G5, ["Encoder3: 12", "Encoder7: 14"]), [enc(3, 1, 12, 5), enc(7, 2, 14, 5)], 1, "R-ENC D4"),
    ("Nine valid encoders select the two-bank span", "007",
     fx(G5, [f"Encoder{i}: {19 + i}" for i in range(1, 10)]), [enc(i, i, 19 + i, 5) for i in range(1, 10)], 2, "R-ENC D4"),
    ("Eight valid encoders in slots 9-16 keep the one-bank span", "007",
     fx(G5, ["Encoder1: -1"] + [f"Encoder{i}: {21 + i}" for i in range(9, 17)]),
     [enc(i, i - 8, 21 + i, 5) for i in range(9, 17)], 1, "R-CC R-ENC D4"),
    ("Encoder channel endpoints and fallbacks", "003",
     fx(G5, ["Encoder1: 10", "EncoderChannel1: 0", "Encoder2: 11", "EncoderChannel2: 15", "Encoder3: 12",
             "EncoderChannel3: 16", "Encoder4: 13", "EncoderChannel4: abc", "Encoder5: 14", "EncoderChannel5: -1"]),
     [enc(1, 1, 10, 0), enc(2, 2, 11, 15), enc(3, 3, 12, 5), enc(4, 4, 13, 5), enc(5, 5, 14, 5)], 1, "R-PCH R-GCH"),
    ("Invalid encoder numbers are disabled and excluded from compaction", "002 007",
     fx(G5, ["Encoder1: 128", "Encoder2: -1", "Encoder3: abc", "Encoder4: 127"]), [enc(4, 1, 127, 5)], 1, "R-CC R-ENC"),
    ("EncoderMapMode token LinearTwoCompliment", "005",
     fx(G5, ["Encoder1: 10", "EncoderMapMode: LinearTwoCompliment"]), [enc(1, 1, 10, 5, "LinearTwoCompliment")], 1,
     "R-MODE R-MSCOPE D2"),
    ("Absolute14Bit retained through CC95 and replaced by Absolute at CC96", "005",
     fx(G5, ["Encoder1: 95", "Encoder2: 96", "EncoderMapMode: Absolute14Bit"]),
     [enc(1, 1, 95, 5, "Absolute14Bit"), enc(2, 2, 96, 5, "Absolute")], 1, "R-MODE R-14"),
    ("Four mode keys with four distinct tokens (set A)", "005 009 010",
     fx(G5, ["Encoder1: 10", "EncoderMapMode: AccelSignedBit2"],
        ["VolumeSlider1: 11", "Send1Knob1: 12", "CrossfaderSlider: 13", "VolumeMapMode: LinearSignedBit",
         "SendsMapMode: AccelBinaryOffset", "CrossfaderMapMode: LinearSignedBit2"]),
     [enc(1, 1, 10, 5, "AccelSignedBit2"), mix("VolumeSlider1", "track-volume:1", 11, 5, "LinearSignedBit"),
      mix("Send1Knob1", "track-send-a:1", 12, 5, "AccelBinaryOffset"),
      mix("CrossfaderSlider", "crossfader", 13, 5, "LinearSignedBit2")], 1, "R-MODE R-MSCOPE R-GONLY R-TGT D5 D6"),
    ("Four mode keys with four distinct tokens (set B)", "005 009 010",
     fx(G5, ["Encoder1: 10", "EncoderMapMode: AccelTwoCompliment"],
        ["VolumeSlider1: 11", "Send1Knob1: 12", "CrossfaderSlider: 13", "VolumeMapMode: LinearBinaryOffset",
         "SendsMapMode: AccelSignedBit", "CrossfaderMapMode: Absolute14Bit"]),
     [enc(1, 1, 10, 5, "AccelTwoCompliment"), mix("VolumeSlider1", "track-volume:1", 11, 5, "LinearBinaryOffset"),
      mix("Send1Knob1", "track-send-a:1", 12, 5, "AccelSignedBit"),
      mix("CrossfaderSlider", "crossfader", 13, 5, "Absolute14Bit")], 1, "R-MODE R-MSCOPE R-14 R-TGT"),
    ("Only Bank8Button configured selects the first compacted bank slot", "002 003 008",
     fx(G5, ["Bank8Button: 40"]), [dev("Bank8Button", "device-bank:1", 40, 5)], None, "R-BANK R-GONLY R-DBK D4"),
    ("Bank buttons compacted; noninteger slot disabled", "002 008",
     fx(G5, ["Bank2Button: 41", "Bank3Button: abc", "Bank5Button: 42"]),
     [dev("Bank2Button", "device-bank:1", 41, 5), dev("Bank5Button", "device-bank:2", 42, 5)], None, "R-CC R-BANK"),
    ("Device navigation, lock and activator targets", "008",
     fx(G5, ["NextBankButton: 50", "PrevBankButton: 51", "LockButton: 52", "OnOffButton: 53"]),
     [dev("NextBankButton", "device-bank-next", 50, 5), dev("PrevBankButton", "device-bank-previous", 51, 5),
      dev("LockButton", "device-lock", 52, 5), dev("OnOffButton", "device-on-off", 53, 5)], None, "R-TGT R-DBK D4"),
    ("Invented per-control channel keys are ignored for buttons and sends", "003 013",
     fx(G5, ["LockButton: 52", "LockButtonChannel: 3"],
        ["TrackMuteButton1: 30", "TrackMuteButton1Channel: 3", "Send1Knob1: 12", "Send1Knob1Channel: 3"],
        ["PlayButton: 61", "PlayButtonChannel: 3"]),
     [dev("LockButton", "device-lock", 52, 5), mix("TrackMuteButton1", "track-mute:1", 30, 5, kind="toggle"),
      mix("Send1Knob1", "track-send-a:1", 12, 5, "Absolute"), tr("PlayButton", "transport-play", 61, 5)], None,
     "R-GONLY R-OPT R-MBK"),
    ("Track volume explicit and inherited channel", "003 009",
     fx(["GlobalChannel: 4"], [], ["VolumeSlider1: 7", "Slider1Channel: 3", "VolumeSlider8: 127", "Slider8Channel: -1"]),
     [mix("VolumeSlider1", "track-volume:1", 7, 3, "Absolute"), mix("VolumeSlider8", "track-volume:8", 127, 4, "Absolute")],
     None, "R-PCH R-TGT D5"),
    ("Invalid slider channels with invalid global fall back to channel 0", "003",
     fx(["GlobalChannel: 99"], [], ["VolumeSlider2: 8", "Slider2Channel: 16", "VolumeSlider3: 9", "Slider3Channel: abc"]),
     [mix("VolumeSlider2", "track-volume:2", 8, 0, "Absolute"), mix("VolumeSlider3", "track-volume:3", 9, 0, "Absolute")],
     None, "R-PCH R-GCH"),
    ("Send A and B knobs use SendsMapMode and global channel", "005 009",
     fx(G5, [], ["Send1Knob2: 21", "Send2Knob2: 22", "SendsMapMode: AccelSignedBit"]),
     [mix("Send1Knob2", "track-send-a:2", 21, 5, "AccelSignedBit"), mix("Send2Knob2", "track-send-b:2", 22, 5, "AccelSignedBit")],
     None, "R-GONLY R-MSCOPE R-TGT D5"),
    ("MixerButtonsToggle False makes strip and mixer bank buttons momentary", "009 011",
     fx(G5, [], ["MixerButtonsToggle: False", "TrackMuteButton1: 30", "TrackSoloButton1: 31", "TrackSelectButton1: 32",
                 "TrackArmButton1: 33", "NextBankButton: 34", "PrevBankButton: 35"]),
     [mix("TrackMuteButton1", "track-mute:1", 30, 5, kind="momentary"), mix("TrackSoloButton1", "track-solo:1", 31, 5, kind="momentary"),
      mix("TrackSelectButton1", "track-select:1", 32, 5, kind="momentary"), mix("TrackArmButton1", "track-arm:1", 33, 5, kind="momentary"),
      mix("NextBankButton", "mixer-bank-next", 34, 5, kind="momentary"), mix("PrevBankButton", "mixer-bank-previous", 35, 5, kind="momentary")],
     None, "R-MBK R-TGT D5 D6"),
    ("MixerButtonsToggle True makes mixer buttons toggle", "009 011",
     fx(G5, [], ["MixerButtonsToggle: True", "TrackMuteButton8: 40", "TrackArmButton8: 41"]),
     [mix("TrackMuteButton8", "track-mute:8", 40, 5, kind="toggle"), mix("TrackArmButton8", "track-arm:8", 41, 5, kind="toggle")],
     None, "R-MBK R-TGT"),
    ("Absent MixerButtonsToggle acts as toggle", "011",
     fx(G5, [], ["TrackSoloButton4: 44"]), [mix("TrackSoloButton4", "track-solo:4", 44, 5, kind="toggle")], None, "R-MBK"),
] + [
    (f"MixerButtonsToggle Boolean spelling '{v}'", "011 013",
     fx(G5, [], [f"MixerButtonsToggle: {v}", "TrackMuteButton2: 45"]),
     [mix("TrackMuteButton2", "track-mute:2", 45, 5, kind=k)], None, "R-BOOL R-MBK") for v, k in BOOL
] + [
    ("Device and mixer NextBankButton are distinct keys with distinct button kinds", "008 009 011",
     fx(G5, ["NextBankButton: 50"], ["MixerButtonsToggle: True", "NextBankButton: 51"]),
     [dev("NextBankButton", "device-bank-next", 50, 5), mix("NextBankButton", "mixer-bank-next", 51, 5, kind="toggle")],
     None, "R-TGT R-DBK R-MBK"),
    ("VolumeMapMode Absolute14Bit with CC above 95 on master", "005 010",
     fx(G5, [], ["VolumeMapMode: Absolute14Bit", "VolumeSlider1: 95", "MasterVolumeSlider: 100", "CueVolumeSlider: 31"]),
     [mix("VolumeSlider1", "track-volume:1", 95, 5, "Absolute14Bit"), mix("MasterVolumeSlider", "master-volume", 100, 5, "Absolute"),
      mix("CueVolumeSlider", "cue-volume", 31, 5, "Absolute14Bit")], None, "R-14 R-MSCOPE"),
    ("Mode scope: VolumeMapMode on master/cue, CrossfaderMapMode on crossfader, default sends", "005 010",
     fx(G5, [], ["VolumeMapMode: AccelTwoCompliment", "CrossfaderMapMode: LinearBinaryOffset", "MasterVolumeSlider: 20",
                 "CueVolumeSlider: 21", "CrossfaderSlider: 22", "Send2Knob1: 23"]),
     [mix("MasterVolumeSlider", "master-volume", 20, 5, "AccelTwoCompliment"), mix("CueVolumeSlider", "cue-volume", 21, 5, "AccelTwoCompliment"),
      mix("CrossfaderSlider", "crossfader", 22, 5, "LinearBinaryOffset"), mix("Send2Knob1", "track-send-b:1", 23, 5, "Absolute")],
     None, "R-MSCOPE R-MODE D6"),
    ("All fourteen transport buttons", "002 003 012",
     fx(G5, t=[f"{k}Button: {60 + i}" for i, (k, _) in enumerate(TRANSPORT)]),
     [tr(f"{k}Button", tgt, 60 + i, 5) for i, (k, tgt) in enumerate(TRANSPORT)], None, "R-TGT R-GONLY R-DBK D7"),
    ("FwdButton from the template comment is not a recognized key", "012 013",
     fx(G5, t=["FwdButton: 68"]), [], None, "R-TGT R-OPT D7"),
    ("Transport button with invalid GlobalChannel uses channel 0", "003 012",
     fx(["GlobalChannel: 16"], t=["PlayButton: 61"]), [tr("PlayButton", "transport-play", 61, 0)], None, "R-GCH R-GONLY"),
    ("Pad note inherits valid global channel", "002 003 006",
     fx(["GlobalChannel: 9", "Pad1Note: 36"]), [pad(1, 36, 9)], None, "R-PAD D3"),
    ("Pad note and channel endpoints", "002 003 006",
     fx(G5 + ["Pad16Note: 127", "Pad16Channel: 15", "Pad2Note: 0", "Pad2Channel: 0"]), [pad(16, 127, 15), pad(2, 0, 0)],
     None, "R-PAD"),
    ("Out-of-range pad notes and channels omit the pad", "002 003 006",
     fx(G5 + ["Pad2Note: 128", "Pad3Note: -1", "Pad4Note: 40", "Pad4Channel: 16", "Pad5Note: 41", "Pad5Channel: -2"]), [],
     None, "R-PAD"),
    ("Invalid global channel omits pads lacking a valid explicit channel but not ordinary CCs", "003 006 010",
     fx(["GlobalChannel: 16", "Pad5Note: 41", "Pad6Note: 42", "Pad6Channel: 3"], [], ["MasterVolumeSlider: 20"]),
     [pad(6, 42, 3), mix("MasterVolumeSlider", "master-volume", 20, 0, "Absolute")], None, "R-PAD R-GCH"),
    ("Pad channel is not read when the note is invalid", "002 003 006",
     fx(G5 + ["Pad7Note: -1", "Pad7Channel: abc", "Pad8Note: 44", "Pad8Channel: -1"]), [pad(8, 44, 5)], None, "R-PAD"),
    ("Missing GlobalChannel key omits channel-less pads; ordinary CC uses 0", "003 006",
     fx(["Pad1Note: 36"], [], ["MasterVolumeSlider: 20"]), [mix("MasterVolumeSlider", "master-volume", 20, 0, "Absolute")],
     None, "R-PAD R-GCH"),
    ("Pad keys outside [Globals] are ignored", "006 013",
     fx(G5, [], ["Pad1Note: 36"]), [], None, "R-PAD R-SEC"),
    ("Absent [Globals] section: ordinary CC on channel 0", "003 013",
     fx((), [], ["MasterVolumeSlider: 20"], names=(None, "DeviceControls", "MixerControls", "TransportControls")),
     [mix("MasterVolumeSlider", "master-volume", 20, 0, "Absolute")], None, "R-SEC R-GCH"),
    ("Equals-sign delimiter", "013",
     fx(G5, [], ["MasterVolumeSlider = 20", "MasterSliderChannel=3"]), [mix("MasterVolumeSlider", "master-volume", 20, 3, "Absolute")],
     None, "R-LEX R-PCH"),
    ("Full-line comments and blank lines are ignored", "013",
     fx(["# hash comment", "GlobalChannel: 5", "", "; semicolon comment"], [], ["# x", "MasterVolumeSlider: 20"]),
     [mix("MasterVolumeSlider", "master-volume", 20, 5, "Absolute")], None, "R-LEX"),
    ("Inline comment is part of the value and disables the CC", "002 013",
     fx(G5, [], ["MasterVolumeSlider: 20 ; fader"]), [], None, "R-LEX R-CC"),
    ("Empty value disables the CC", "002 013",
     fx(G5, [], ["MasterVolumeSlider:"]), [], None, "R-LEX R-CC"),
    ("Surrounding whitespace is stripped from values", "013",
     fx(G5, [], ["MasterVolumeSlider:    20   "]), [mix("MasterVolumeSlider", "master-volume", 20, 5, "Absolute")], None, "R-LEX"),
    ("Section names are case-sensitive", "013",
     fx(G5, [], ["MasterVolumeSlider: 20"], names=("Globals", "DeviceControls", "mixercontrols", "TransportControls")),
     [], None, "R-SEC"),
    ("DEFAULT section values are inherited by named sections", "003 013",
     fx([], [], ["MasterVolumeSlider: 20"], pre=("[DEFAULT]", "GlobalChannel: 3", "")),
     [mix("MasterVolumeSlider", "master-volume", 20, 3, "Absolute")], None, "R-LEX R-GCH"),
    ("Ordinary key in the wrong section is ignored", "013",
     fx(G5 + ["MasterVolumeSlider: 20"]), [], None, "R-SEC R-TGT"),
    ("Sign and leading zeros accepted by integer conversion", "002 013",
     fx(G5, [], ["MasterVolumeSlider: +20", "CueVolumeSlider: 0021"]),
     [mix("MasterVolumeSlider", "master-volume", 20, 5, "Absolute"), mix("CueVolumeSlider", "cue-volume", 21, 5, "Absolute")],
     None, "R-INT R-CC"),
    ("Hexadecimal and decimal-point text are conversion failures", "002 013",
     fx(G5, [], ["MasterVolumeSlider: 0x14", "CueVolumeSlider: 20.0"]), [], None, "R-INT R-CC"),
    ("Underscore digit grouping accepted by integer conversion", "002 013",
     fx(G5, [], ["MasterVolumeSlider: 1_0"]), [mix("MasterVolumeSlider", "master-volume", 10, 5, "Absolute")], None, "R-INT R-CC"),
    ("Mixed-case option names across device, mixer, transport and pad keys", "013",
     fx(["GlobalChannel: 5", "pad1note: 36"], ["encoder1: 10", "ENCODERCHANNEL1: 2"], ["trackmutebutton1: 30"], ["PLAYBUTTON: 61"]),
     [enc(1, 1, 10, 2), mix("TrackMuteButton1", "track-mute:1", 30, 5, kind="toggle"), tr("PlayButton", "transport-play", 61, 5),
      pad(1, 36, 5)], 1, "R-OPT R-PAD R-PCH"),
    ("Unknown option alongside a known option", "013",
     fx(G5, [], ["MasterVolumeFader: 20", "CueVolumeSlider: 21"]), [mix("CueVolumeSlider", "cue-volume", 21, 5, "Absolute")],
     None, "R-OPT"),
    ("Noninteger GlobalChannel: ordinary buttons and encoders on channel 0", "003",
     fx(["GlobalChannel: abc"], ["Encoder1: 10"], ["TrackMuteButton1: 30"]),
     [enc(1, 1, 10, 0), mix("TrackMuteButton1", "track-mute:1", 30, 0, kind="toggle")], 1, "R-GCH R-GONLY R-MBK"),
]


def check(case, text):
    errs = []
    if not text.isascii() or "\r" in text or not text.endswith("\n"):
        errs.append("fixture not ASCII/LF/newline-terminated")
    cp = configparser.ConfigParser()
    cp.read_file(io.StringIO(text))  # host stdlib; raises if the fixture is not a non-raising input
    for a in case["expected"]["assignments"]:
        if a["section"] not in SECTIONS or not 0 <= a["number"] <= 127 or not 0 <= a["channel"] <= 15:
            errs.append(f"range/section {a}")
        if "map_mode" in a and a["map_mode"] not in MODES:
            errs.append(f"mode {a}")
        if a["message_type"] == "control-change" and ("map_mode" in a) == ("button_kind" in a):
            errs.append(f"exactly one of map_mode/button_kind expected {a}")
        if not cp.has_section(a["section"]) or not cp.has_option(a["section"], a["control"]):
            errs.append(f"option not visible to configparser {a['section']}.{a['control']}")
        elif int(cp.get(a["section"], a["control"])) != a["number"]:
            errs.append(f"number text mismatch {a['control']}")
    keys = [(a["section"], a["control"]) for a in case["expected"]["assignments"]]
    if len(set(keys)) != len(keys) or len({a["target"] for a in case["expected"]["assignments"]}) != len(keys):
        errs.append("duplicate control or target")
    addrs = [(a["message_type"], a["number"], a["channel"]) for a in case["expected"]["assignments"]]
    if len(set(addrs)) != len(addrs):
        errs.append("duplicate MIDI address (out of scope: collisions)")
    return errs


def main(out):
    out = Path(out)
    cases, problems = [], {}
    for i, (purpose, reqs, text, assigns, banks, rules) in enumerate(CASES, 1):
        cid = f"S4-MIDI-{i:03d}"
        path = out / "fixtures" / cid / "UserConfiguration.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("ascii"))
        unknown = [r for r in rules.split() if r not in RULES]
        assert not unknown, (cid, unknown)
        case = {"id": cid, "purpose": purpose, "requirements": [f"REQ-MIDI-USER-{r}" for r in reqs.split()],
                "input": f"fixtures/{cid}/UserConfiguration.txt",
                "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "expected": {"assignments": assigns, "device_parameter_banks": banks},
                "derivation": rules.split(),
                "expectation_provenance": "static-derived; not observed reference output",
                "reference_execution": "not-run", "candidate_execution": "not-run",
                "comparator": "exact assignment set over all present fields; order immaterial; device_parameter_banks exact"}
        errs = check(case, text)
        if errs:
            problems[cid] = errs
        cases.append(case)
    doc = {"schema": "midi-config-cases-v2-draft", "status": "analyst-draft; not reviewed; not released",
           "target": "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS",
           "representation": {
               "assignment_fields": "section, control (canonical template key), target, message_type (control-change|note), number, channel; map_mode for continuous controls; button_kind (momentary|toggle) for buttons",
               "device_parameter_banks": "1 or 2 when at least one encoder assignment is enabled, else null",
               "note": "project comparison representation, not a Live API or recovered structure; derivation IDs are analyst-only and must be removed for a handoff"},
           "rules": RULES, "cases": cases, "check": {"cases": len(cases), "problems": problems}}
    (out / "draft-cases-v2.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(len(cases), "cases;", "problems:", json.dumps(problems) if problems else "none")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
