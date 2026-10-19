"""Generate the T1.1 minimal Live Set fixture T11-MIN (authored; no shipped content is copied).

Usage: python3 -I make_fixture.py <out dir>
Writes <out>/Samples/T11-tone.wav (generated: 1 s, 44,100 Hz, 16-bit PCM, 2 channels, a 441 Hz
sine at amplitude 8,192 on both channels; modification time set to LASTMOD), then
<out>/T11-MIN.xml (plain XML, for reading) and <out>/T11-MIN.als (the same bytes as one gzip
member with FLG 0 and MTIME 0). The set references the sample by a Document-relative path
(RelativePathType 1, "Samples/T11-tone.wav"), so the .als and the Samples folder must stay together.
Every value, Id and name below is invented for this fixture. Element names and nesting follow the
shipped schema 12.0_12402 (checked by schema_check.py). The element list with its required /
optional classification is SPEC-LIVE-SET-STRUCTURE's minimal-set table; this script is its
executable form.
"""
import gzip, math, os, struct, sys, wave

L = "-63072000"  # lower time bound (SPEC-AUTOMATION-ENVELOPES)
LASTMOD = 1760000000  # invented file time (seconds since the epoch) written as LastModDate


def crc16(data):
    """Sample identity CRC: CRC-16, poly 0x8005, MSB first, init 0, no final xor (x-crc/x_crc.py checks it
    against the original x86_64 code)."""
    c = 0
    for b in data:
        c ^= b << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x8005) if c & 0x8000 else (c << 1)
            c &= 0xFFFF
    return c


class Ids:
    """Pointee Ids: unique, nonzero, allocated upward from 1; NextPointeeId = last + 1."""

    def __init__(self):
        self.n = 0

    def __call__(self):
        self.n += 1
        return self.n


def el(tag, attrs=None, *kids):
    return (tag, attrs or {}, list(kids))


def v(tag, value):
    return el(tag, {"Value": str(value)})


def target(tag, ids):
    t = el(tag, {"Id": str(ids())}, v("LockEnvelope", 0))
    return t, int(t[1]["Id"])


def param(tag, manual, ids, rng=None, modulation=True, enum=False):
    """A Timeable parameter: Manual, MidiControllerRange (after AutomationTarget for an Enum),
    AutomationTarget, ModulationTarget (Float only)."""
    kids = [v("Manual", manual)]
    at, at_id = target("AutomationTarget", ids)
    rng_el = [el("MidiControllerRange", None, v("Min", rng[0]), v("Max", rng[1]))] if rng else []
    kids += ([at] + rng_el) if enum else (rng_el + [at])
    if modulation:
        kids.append(target("ModulationTarget", ids)[0])
    return el(tag, None, *kids), at_id


def mixer(ids, holders, main=False):
    """Track mixer (SPEC-MIXER-VALUES REQ-001 fields, in schema order)."""
    out = {}
    on, out["On"] = param("On", "true", ids, modulation=False)
    sends = []
    for hid, enabled in holders:
        s, out[f"Send{hid}"] = param("Send", "0.0003162277571", ids, ("0.0003162277571", "1"))
        sends.append(el("TrackSendHolder", {"Id": str(hid)}, s, v("EnabledByUser", enabled)))
    speaker, out["Speaker"] = param("Speaker", "true", ids, modulation=False)
    pan, out["Pan"] = param("Pan", "0", ids, ("-1", "1"))
    spl, _ = param("SplitStereoPanL", "-1", ids, ("-1", "1"))
    spr, _ = param("SplitStereoPanR", "1", ids, ("-1", "1"))
    vol, out["Volume"] = param("Volume", "1", ids, ("0.0003162277571", "1.99526238"))
    xfs, out["CrossFadeState"] = param("CrossFadeState", "1", ids, ("0", "2"), modulation=False, enum=True)
    kids = [on, el("Sends", None, *sends), speaker, v("SoloSink", "false"), v("PanMode", 0), pan, spl, spr, vol, xfs]
    if main:
        tempo, out["Tempo"] = param("Tempo", "120", ids, ("60", "200"))
        tsig, out["TimeSignature"] = param("TimeSignature", "201", ids, ("0", "494"), modulation=False, enum=True)
        cf, out["CrossFade"] = param("CrossFade", "0", ids, ("-1", "1"))
        kids += [tempo, tsig, cf]
    return el("Mixer", None, *kids), out


def routing(tag, target_text):
    return el(tag, None, v("Target", target_text))


def envelope(eid, pointee, events):
    return el("AutomationEnvelope", {"Id": str(eid)},
              el("EnvelopeTarget", None, v("PointeeId", pointee)),
              el("Automation", None, el("Events", None, *events),
                 el("AutomationTransformViewState", None, v("IsTransformPending", "false"), el("TimeAndValueTransforms"))))


def follow_action():
    return el("FollowAction", None, v("FollowTime", 4), v("IsLinked", "true"), v("LoopIterations", 1),
              v("FollowActionA", 4), v("FollowActionB", 0), v("FollowChanceA", 100), v("FollowChanceB", 0),
              v("JumpIndexA", 1), v("JumpIndexB", 1), v("FollowActionEnabled", "false"))


def clip_common(name, color, end):
    return [v("CurrentStart", 0), v("CurrentEnd", end),
            el("Loop", None, v("LoopStart", 0), v("LoopEnd", end), v("StartRelative", 0), v("LoopOn", "true"),
               v("OutMarker", end), v("HiddenLoopStart", 0), v("HiddenLoopEnd", end)),
            v("Name", name), v("Color", color), v("LaunchMode", 0), v("LaunchQuantisation", 0),
            el("TimeSignature", None, el("TimeSignatures", None, el("RemoteableTimeSignature", {"Id": "0"},
                                                                     v("Numerator", 4), v("Denominator", 4), v("Time", 0)))),
            el("Envelopes", None, el("Envelopes")),
            v("Legato", "false"), v("VelocityAmount", 0), follow_action()]


def midi_clip():
    notes = el("Notes", None,
               el("KeyTracks", None,
                  el("KeyTrack", {"Id": "0"},
                     el("Notes", None,
                        el("MidiNoteEvent", {"Time": "0", "Duration": "1", "Velocity": "100", "OffVelocity": "64",
                                             "NoteId": "1"}),
                        el("MidiNoteEvent", {"Time": "2", "Duration": "1", "Velocity": "100", "OffVelocity": "64",
                                             "NoteId": "2"})),
                     v("MidiKey", 60))),
               el("PerNoteEventStore", None, el("EventLists")),
               el("NoteProbabilityGroups"),
               el("ProbabilityGroupIdGenerator", None, v("NextId", 1)),
               el("NoteIdGenerator", None, v("NextId", 3)))
    return el("MidiClip", {"Id": "0", "Time": "0"}, *clip_common("Two Notes", 15, 4), v("IsWarped", "true"), notes)


def audio_clip(wav):
    fileref = el("FileRef", None, v("RelativePathType", 1), v("RelativePath", "Samples/T11-tone.wav"),
                 v("Path", "/T11/Samples/T11-tone.wav"), v("Type", 2), v("LivePackName", ""),
                 v("LivePackId", ""), v("OriginalFileSize", len(wav)), v("OriginalCrc", crc16(wav[:16384])),
                 v("SourceHint", ""))
    sref = el("SampleRef", None, fileref, v("LastModDate", LASTMOD), v("DefaultDuration", 44100),
              v("DefaultSampleRate", 44100))
    return el("AudioClip", {"Id": "0", "Time": "0"}, *clip_common("Tone", 3, 2), v("IsWarped", "false"), sref,
              v("WarpMode", 0),
              el("WarpMarkers", None, el("WarpMarker", {"Id": "0", "SecTime": "0", "BeatTime": "0"}),
                 el("WarpMarker", {"Id": "1", "SecTime": "0.015625", "BeatTime": "0.03125"})))


def slots(first_clip, n):
    out = []
    for i in range(n):
        content = [first_clip] if (i == 0 and first_clip) else []
        out.append(el("ClipSlot", {"Id": str(i)}, el("ClipSlot", None, el("Value", None, *content)),
                      v("HasStop", "true")))
    return el("ClipSlotList", None, *out)


def name(user, effective):
    return el("Name", None, v("EffectiveName", effective), v("UserName", user))


def track(tag, tid, user, effective, color, mix, envelopes, sequencer, devices, freeze_slots=None):
    chain = [routing("AudioOutputRouting", "AudioOut/Main"), mix]
    if sequencer is not None:
        chain.append(sequencer)
    if freeze_slots is not None:  # same slot count as the main sequencer (refused otherwise)
        chain.append(el("FreezeSequencer", None, slots(None, freeze_slots)))
    chain.append(el("DeviceChain", None, el("Devices", None, *devices)))
    return el(tag, {"Id": str(tid)}, name(user, effective), v("Color", color),
              el("AutomationEnvelopes", None, el("Envelopes", None, *envelopes)), v("TrackGroupId", -1),
              el("DeviceChain", None, *chain))


def device(tag, did, ids):
    on, _ = param("On", "true", ids, modulation=False)
    return el(tag, {"Id": str(did)}, on)


def build(wav):
    ids = Ids()
    scenes = 2
    m_mix, m_t = mixer(ids, [(0, "true")])
    a_mix, _ = mixer(ids, [(0, "true")])
    r_mix, _ = mixer(ids, [(0, "false")])
    main_mix, main_t = mixer(ids, [], main=True)
    pre_mix, _ = mixer(ids, [])
    analog = device("UltraAnalog", 0, ids)
    amp = device("Amp", 0, ids)
    vol_env = envelope(0, m_t["Volume"], [el("FloatEvent", {"Id": "0", "Time": L, "Value": "1"}),
                                          el("FloatEvent", {"Id": "1", "Time": "4", "Value": "0.5"})])
    tracks = el("Tracks", None,
                track("MidiTrack", 1, "Lead", "Lead", 15, m_mix, [vol_env],
                      el("MainSequencer", None, slots(midi_clip(), scenes)), [analog], scenes),
                track("AudioTrack", 2, "", "2-Audio", 3, a_mix, [],
                      el("MainSequencer", None, slots(audio_clip(wav), scenes)), [amp], scenes),
                track("ReturnTrack", 3, "", "A-Return", 55, r_mix, [], None, []))
    main = el("MainTrack", None, name("", "Main"), v("Color", 69),
              el("AutomationEnvelopes", None, el("Envelopes", None,
                 envelope(0, main_t["TimeSignature"], [el("EnumEvent", {"Id": "0", "Time": L, "Value": "201"})]),
                 envelope(1, main_t["Tempo"], [el("FloatEvent", {"Id": "0", "Time": L, "Value": "120"})]))),
              el("DeviceChain", None, routing("AudioOutputRouting", "AudioOut/External/S0"), main_mix,
                 el("DeviceChain", None, el("Devices"))))
    prehear = el("PreHearTrack", None, el("DeviceChain", None, pre_mix))
    scene_els = [el("Scene", {"Id": str(i)}, follow_action(), v("Name", f"Scene {i + 1}"), v("Color", -1),
                    v("Tempo", 120), v("IsTempoEnabled", "false"), v("TimeSignatureId", 201),
                    v("IsTimeSignatureEnabled", "false")) for i in range(scenes)]
    liveset = el("LiveSet", None, v("NextPointeeId", ids.n + 1), tracks, main, prehear,
                 el("SendsPre", None, el("SendPreBool", {"Id": "0", "Value": "false"})),
                 el("Scenes", None, *scene_els),
                 el("Transport", None, v("LoopOn", "false"), v("LoopStart", 0), v("LoopLength", 8), v("CurrentTime", 0)),
                 v("GlobalQuantisation", 4), v("AutoQuantisation", 0), v("CrossfadeCurve", 2))
    return el("Ableton", {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1"}, liveset)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render(node, depth, out):
    tag, attrs, kids = node
    a = "".join(f' {k}="{esc(x)}"' for k, x in attrs.items())
    pad = "\t" * depth
    if kids:
        out.append(f"{pad}<{tag}{a}>")
        for k in kids:
            render(k, depth + 1, out)
        out.append(f"{pad}</{tag}>")
    else:
        out.append(f"{pad}<{tag}{a} />")


def wav(path):
    rate, n = 44100, 44100
    frames = b"".join(struct.pack("<hh", s, s) for s in (round(8192 * math.sin(2 * math.pi * 441 * i / rate)) for i in range(n)))
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)
    os.utime(path, (LASTMOD, LASTMOD))
    return open(path, "rb").read()


def main():
    out = sys.argv[1]
    os.makedirs(os.path.join(out, "Samples"), exist_ok=True)
    sample = wav(os.path.join(out, "Samples", "T11-tone.wav"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    render(build(sample), 0, lines)
    data = ("\n".join(lines) + "\n").encode("utf-8")
    open(os.path.join(out, "T11-MIN.xml"), "wb").write(data)
    open(os.path.join(out, "T11-MIN.als"), "wb").write(gzip.compress(data, compresslevel=9, mtime=0))


if __name__ == "__main__":
    main()
