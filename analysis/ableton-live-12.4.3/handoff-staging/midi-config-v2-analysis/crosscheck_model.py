"""Analyst cross-check for midi-config-v2: an independent re-reading of the S4 bytecode
listings as executable rules (NOT an oracle; never shipped). Host CPython 3.11 configparser
stands in for the shipped one, which is equivalent for non-raising input (S4 evidence).
Usage: python3.11 -I crosscheck_model.py <cases.json>  (fixture paths relative to it)."""
import configparser, json, sys
from pathlib import Path

MODES = {"Absolute", "Absolute14Bit", "LinearSignedBit", "LinearSignedBit2", "LinearTwoCompliment",
         "LinearBinaryOffset", "AccelSignedBit", "AccelSignedBit2", "AccelTwoCompliment", "AccelBinaryOffset"}
TRANSPORT = [("Stop", "transport-stop"), ("Play", "transport-play"), ("Rec", "arrangement-record"),
             ("SessionRec", "session-record"), ("Over", "arrangement-overdub"), ("Metro", "metronome"),
             ("Loop", "arrangement-loop"), ("Rwd", "rewind"), ("Ffwd", "fast-forward"), ("PunchIn", "punch-in"),
             ("PunchOut", "punch-out"), ("NudgeUp", "nudge-up"), ("NudgeDown", "nudge-down"), ("TapTempo", "tap-tempo")]


def interpret(text):
    cp = configparser.ConfigParser()
    cp.read_string(text)

    def pint(rng, sec, opt):
        if cp.has_option(sec, opt):
            try:
                v = cp.getint(sec, opt)
                return v if v in range(rng) else -1
            except ValueError:
                return -1
        return -1

    ident = lambda s, o: pint(128, s, o)
    chan = lambda s, o: pint(16, s, o)

    def mode(s, o):
        if cp.has_option(s, o):
            v = cp.get(s, o)
            assert v in MODES, f"unknown mode token out of scope: {v!r}"
            return v
        return "Absolute"

    def eff(m, cc):
        return "Absolute" if m == "Absolute14Bit" and cc > 95 else m

    out, banks = [], None
    gch_raw = chan("Globals", "GlobalChannel") if cp.has_section("Globals") else -1
    g = gch_raw if 0 <= gch_raw < 16 else 0

    def a(sec, ctl, tgt, n, ch, mode=None, kind=None, mt="control-change"):
        d = {"section": sec, "control": ctl, "target": tgt, "message_type": mt, "number": n, "channel": ch}
        if mode: d["map_mode"] = mode
        if kind: d["button_kind"] = kind
        out.append(d)

    if cp.has_section("Globals"):
        for p in range(1, 17):
            o = f"Pad{p}Note"
            if not cp.has_option("Globals", o):
                continue
            note = cp.getint("Globals", o)  # raises on noninteger: out of scope
            if note not in range(128):
                continue
            ch = cp.getint("Globals", f"Pad{p}Channel") if cp.has_option("Globals", f"Pad{p}Channel") else -1
            if ch == -1 and gch_raw != -1:
                ch = gch_raw
            if ch in range(16):
                a("Globals", o, f"drum-pad:{p}", note, ch, mt="note")
    if cp.has_section("DeviceControls"):
        S = "DeviceControls"
        dm = mode(S, "EncoderMapMode")
        k = 0
        for i in range(1, 17):
            cc, ch = ident(S, f"Encoder{i}"), chan(S, f"EncoderChannel{i}")
            if cc >= 0:
                k += 1
                a(S, f"Encoder{i}", f"device-parameter:{k}", cc, ch if ch >= 0 else g, eff(dm, cc))
        banks = None if k == 0 else (2 if k > 8 else 1)
        k = 0
        for i in range(1, 9):
            cc = ident(S, f"Bank{i}Button")
            if cc >= 0:
                k += 1
                a(S, f"Bank{i}Button", f"device-bank:{k}", cc, g, kind="momentary")
        for key, tgt in (("NextBankButton", "device-bank-next"), ("PrevBankButton", "device-bank-previous"),
                         ("LockButton", "device-lock"), ("OnOffButton", "device-on-off")):
            cc = ident(S, key)
            if cc >= 0:
                a(S, key, tgt, cc, g, kind="momentary")
    if cp.has_section("TransportControls"):
        for key, tgt in TRANSPORT:
            cc = ident("TransportControls", f"{key}Button")
            if cc >= 0:
                a("TransportControls", f"{key}Button", tgt, cc, g, kind="momentary")
    if cp.has_section("MixerControls"):
        S = "MixerControls"
        vm, sm, xm = mode(S, "VolumeMapMode"), mode(S, "SendsMapMode"), mode(S, "CrossfaderMapMode")
        kind = "momentary" if cp.has_option(S, "MixerButtonsToggle") and not cp.getboolean(S, "MixerButtonsToggle") else "toggle"
        for key, chk, tgt, m in (("MasterVolumeSlider", "MasterSliderChannel", "master-volume", vm),
                                 ("CueVolumeSlider", "CueSliderChannel", "cue-volume", vm),
                                 ("CrossfaderSlider", "CrossfaderSliderChannel", "crossfader", xm)):
            cc, ch = ident(S, key), chan(S, chk)
            if cc >= 0:
                a(S, key, tgt, cc, ch if ch >= 0 else g, eff(m, cc))
        for key, tgt in (("NextBankButton", "mixer-bank-next"), ("PrevBankButton", "mixer-bank-previous")):
            cc = ident(S, key)
            if cc >= 0:
                a(S, key, tgt, cc, g, kind=kind)
        for t in range(1, 9):
            cc, ch = ident(S, f"VolumeSlider{t}"), chan(S, f"Slider{t}Channel")
            if cc >= 0:
                a(S, f"VolumeSlider{t}", f"track-volume:{t}", cc, ch if ch >= 0 else g, eff(vm, cc))
            for key, tgt in (("TrackArmButton", "track-arm"), ("TrackMuteButton", "track-mute"),
                             ("TrackSoloButton", "track-solo"), ("TrackSelectButton", "track-select")):
                cc = ident(S, f"{key}{t}")
                if cc >= 0:
                    a(S, f"{key}{t}", f"{tgt}:{t}", cc, g, kind=kind)
            pos = 0  # sends are compacted per strip; position decides the send
            for s, key in enumerate(("Send1Knob", "Send2Knob")):
                cc = ident(S, f"{key}{t}")
                if cc >= 0:
                    a(S, f"{key}{t}", f"track-send-{'ab'[pos]}:{t}", cc, g, eff(sm, cc))
                    pos += 1
    return {"assignments": out, "device_parameter_banks": banks}


def canon(exp):
    return (sorted(json.dumps(x, sort_keys=True) for x in exp["assignments"]), exp.get("device_parameter_banks"))


if __name__ == "__main__":
    cases_path = Path(sys.argv[1]); base = cases_path.parent
    bad = 0
    for c in json.loads(cases_path.read_text())["cases"]:
        got = interpret((base / c["input"]).read_text())
        if canon(got) != canon(c["expected"]):
            bad += 1
            print("MISMATCH", c["id"], c.get("purpose"), "\n  got ", canon(got), "\n  want", canon(c["expected"]))
    print("mismatches:", bad)
