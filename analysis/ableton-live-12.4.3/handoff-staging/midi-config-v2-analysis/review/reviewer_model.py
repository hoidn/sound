"""Reviewer's own transliteration of the read listings (not the author's model)."""
import json, sys
from configparser import ConfigParser
from pathlib import Path

MODES = {"Absolute", "Absolute14Bit", "LinearSignedBit", "LinearSignedBit2", "LinearTwoCompliment",
         "LinearBinaryOffset", "AccelSignedBit", "AccelSignedBit2", "AccelTwoCompliment", "AccelBinaryOffset"}
TRANSPORT = {"Stop": "transport-stop", "Play": "transport-play", "Rec": "arrangement-record",
             "SessionRec": "session-record", "Over": "arrangement-overdub", "Metro": "metronome",
             "Loop": "arrangement-loop", "Rwd": "rewind", "Ffwd": "fast-forward", "PunchIn": "punch-in",
             "PunchOut": "punch-out", "NudgeUp": "nudge-up", "NudgeDown": "nudge-down", "TapTempo": "tap-tempo"}

def parse_int(cp, rng, sec, opt):
    if not cp.has_option(sec, opt): return -1
    try:
        v = cp.getint(sec, opt)
    except ValueError:
        return -1
    return v if v in range(rng) else -1

def mode(cp, sec, opt):
    if cp.has_option(sec, opt):
        v = cp.get(sec, opt)
        assert v in MODES, ("excluded unknown token", v)
        return v
    return "Absolute"

def interpret(text):
    cp = ConfigParser(); cp.read_string(text)
    ident = lambda s, o: parse_int(cp, 128, s, o)
    chan = lambda s, o: parse_int(cp, 16, s, o)
    out = []
    def enc(sec, ctl, tgt, cc, ch, mm):
        if 0 <= cc < 128 and 0 <= ch < 16:
            out.append(dict(section=sec, control=ctl, target=tgt, message_type="control-change", number=cc, channel=ch,
                            map_mode="Absolute" if (mm == "Absolute14Bit" and cc > 95) else mm))
            return True
    def btn(sec, ctl, tgt, cc, ch, kind):
        if 0 <= cc < 128:
            out.append(dict(section=sec, control=ctl, target=tgt, message_type="control-change", number=cc, channel=ch, button_kind=kind))
            return True
    gch_raw = chan("Globals", "GlobalChannel") if cp.has_section("Globals") else -1
    g = gch_raw if 0 <= gch_raw < 16 else 0
    # pads
    if cp.has_section("Globals"):
        for p in range(1, 17):
            if cp.has_option("Globals", f"Pad{p}Note"):
                note = cp.getint("Globals", f"Pad{p}Note")
                if note in range(128):
                    ch = cp.getint("Globals", f"Pad{p}Channel") if cp.has_option("Globals", f"Pad{p}Channel") else -1
                    if ch == -1 and gch_raw != -1: ch = gch_raw
                    if ch in range(16):
                        out.append(dict(section="Globals", control=f"Pad{p}Note", target=f"drum-pad:{p}", message_type="note", number=note, channel=ch))
    # device
    banks = None
    if cp.has_section("DeviceControls"):
        dm = mode(cp, "DeviceControls", "EncoderMapMode"); k = 0
        for i in range(1, 17):
            cc = ident("DeviceControls", f"Encoder{i}"); ch = chan("DeviceControls", f"EncoderChannel{i}")
            if enc("DeviceControls", f"Encoder{i}", f"device-parameter:{k+1}", cc, ch if 0 <= ch < 16 else g, dm): k += 1
        banks = None if k == 0 else (2 if k > 8 else 1)
        for key, tgt in (("NextBankButton", "device-bank-next"), ("PrevBankButton", "device-bank-previous"),
                         ("LockButton", "device-lock"), ("OnOffButton", "device-on-off")):
            btn("DeviceControls", key, tgt, ident("DeviceControls", key), g, "momentary")
        k = 0
        for i in range(1, 9):
            if btn("DeviceControls", f"Bank{i}Button", f"device-bank:{k+1}", ident("DeviceControls", f"Bank{i}Button"), g, "momentary"): k += 1
    # transport
    if cp.has_section("TransportControls"):
        for key, tgt in TRANSPORT.items():
            btn("TransportControls", f"{key}Button", tgt, ident("TransportControls", f"{key}Button"), g, "momentary")
    # mixer
    if cp.has_section("MixerControls"):
        S = "MixerControls"
        vm = mode(cp, S, "VolumeMapMode"); sm = mode(cp, S, "SendsMapMode"); xm = mode(cp, S, "CrossfaderMapMode")
        kind = "momentary" if (cp.has_option(S, "MixerButtonsToggle") and not cp.getboolean(S, "MixerButtonsToggle")) else "toggle"
        for key, chk, tgt, mm in (("MasterVolumeSlider", "MasterSliderChannel", "master-volume", vm),
                                  ("CueVolumeSlider", "CueSliderChannel", "cue-volume", vm),
                                  ("CrossfaderSlider", "CrossfaderSliderChannel", "crossfader", xm)):
            ch = chan(S, chk); enc(S, key, tgt, ident(S, key), ch if 0 <= ch < 16 else g, mm)
        btn(S, "NextBankButton", "mixer-bank-next", ident(S, "NextBankButton"), g, kind)
        btn(S, "PrevBankButton", "mixer-bank-previous", ident(S, "PrevBankButton"), g, kind)
        for n in range(1, 9):
            ch = chan(S, f"Slider{n}Channel")
            enc(S, f"VolumeSlider{n}", f"track-volume:{n}", ident(S, f"VolumeSlider{n}"), ch if 0 <= ch < 16 else g, vm)
            for key, tgt in (("TrackArmButton", "track-arm"), ("TrackMuteButton", "track-mute"),
                             ("TrackSoloButton", "track-solo"), ("TrackSelectButton", "track-select")):
                btn(S, f"{key}{n}", f"{tgt}:{n}", ident(S, f"{key}{n}"), g, kind)
            pos = 0  # sends compacted per strip, connected by position
            for s in (1, 2):
                cc = ident(S, f"Send{s}Knob{n}")
                if 0 <= cc < 128:
                    assert not (s == 2 and pos == 0), "excluded lone Send2"
                    enc(S, f"Send{s}Knob{n}", f"track-send-{'ab'[pos]}:{n}", cc, g, sm); pos += 1
    return {"assignments": out, "device_parameter_banks": banks}

def key(a): return json.dumps(a, sort_keys=True)
root = Path(sys.argv[1]); cases = json.loads((root / "cases.json").read_text())["cases"]
bad = 0
for c in cases:
    got = interpret((root / c["input"]).read_text())
    exp = c["expected"]
    ok = sorted(map(key, got["assignments"])) == sorted(map(key, exp["assignments"])) and got["device_parameter_banks"] == exp["device_parameter_banks"]
    if not ok:
        bad += 1; print("DISAGREE", c["id"], got, exp)
print(f"{len(cases)} cases, {bad} disagreements")
