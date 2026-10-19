"""Case definitions of the playback-core-v1 candidate (analyst side; imported by build_playback.py).

Each case names a generated fixture, the set content it holds, the render rate, the action script, the source case or
clause of SPEC-PLAYBACK-CORE r1 and the stated assumptions. Clip helpers build the clip dicts that
build_playback.py turns into Live Set XML; note times are held as the lattice values the set stores after opening.
"""
import model_playback as m

KEY = 60
PROV_X = ("extracted-execution arithmetic (x86_64 build, glibc in place of the macOS libraries); arm64 equivalence "
          "inferred; playback path static-derived; not observed reference output")
PROV_S = "static-derived; not observed reference output"


# ---- clips ----
def note(t, d, vel=100.0, off=64.0, on=True):
    def txt(x):
        return repr(x) if x != int(x) else str(int(x))
    return {"time": txt(t), "dur": txt(d), "t": m.L(t), "d": m.L(d), "vel": m.f32(vel), "off": m.f32(off),
            "vel_text": txt(vel), "off_text": txt(off), "on": on, "key": KEY}


def probe(times, q, le, dur=0.0625, sig=(4, 4)):
    return {"name": "Probe", "notes": [note(t, dur) for t in times], "ls": 0, "le": le, "sr": 0, "loop_on": False,
            "q": q, "sig": sig}


def pulse(q=0, sig=(4, 4), edit=None, start_rel=0, loop_on=True):
    notes = [note(0.5 * k, 0.25) for k in range(8)]
    if edit:
        edit(notes)
    return {"name": "Pulse", "notes": notes, "ls": 0, "le": 4, "sr": start_rel, "loop_on": loop_on, "q": q, "sig": sig}


# ---- cases ----
def S(track, tempo="120", sig=201, gq=4, loop=None):
    return {"tempo": tempo, "sig": sig, "gq": gq, "track": track, **({"loop": loop} if loop else {})}


def play(b=0.0):
    return {"at": 0, "action": "play", "start_beat": b}


def launch(r):
    return {"at": r, "action": "launch", "track": 1, "slot": 1}


CASES = []  # dicts: id, fixture, set, sr, script, window, kind, purpose, reqs, prov, assume, source


def add(fixture, s, sr, script, purpose, reqs, prov, assume, source, kind="timing", window=None):
    CASES.append({"id": f"PLAYBACK-CORE-{len(CASES) + 1:03d}", "fixture": fixture, "set": s, "sr": sr,
                  "script": script, "window": window, "kind": kind, "purpose": purpose, "reqs": reqs, "prov": prov,
                  "assume": assume, "source": source})


R_CLOCK = ["REQ-PLAYBACK-CORE-001", "REQ-PLAYBACK-CORE-002", "REQ-PLAYBACK-CORE-004", "REQ-PLAYBACK-CORE-010",
           "REQ-PLAYBACK-CORE-011", "REQ-PLAYBACK-CORE-012"]
R_GRID = ["REQ-PLAYBACK-CORE-002", "REQ-PLAYBACK-CORE-007", "REQ-PLAYBACK-CORE-008", "REQ-PLAYBACK-CORE-009",
          "REQ-PLAYBACK-CORE-011", "REQ-PLAYBACK-CORE-012"]
CLOCK = [  # fixture, sr, tempo text, probe note times, loop end, source, extra requirement
    ("clock-120", 48000, "120", [0, 0.25, 1, 4 / 3, 10 / 3, 4, 64], 65, "PBC-001", []),
    ("clock-140", 48000, "140", [0, 0.25, 1, 4, 7], 8, "PBC-002", []),
    ("clock-120", 44100, "120", [0, 0.25, 1, 4 / 3, 10 / 3, 4, 64], 65, "PBC-003 (120 BPM)", []),
    ("clock-128", 44100, "128", [0, 1, 1000], 1001, "PBC-003 (128 BPM)", []),
    ("clock-121.2", 44100, "121.1999969482421875", [0, 4], 5, "PBC-003 (binary32 121.2 BPM)", ["REQ-PLAYBACK-CORE-003"]),
    ("clock-93.3", 48000, "93.33333587646484375", [0, 1, 7], 8, "PBC-004", ["REQ-PLAYBACK-CORE-003"]),
    ("clock-90", 48000, "90", [0, 1, 8 / 3, 8], 9, "PBC-005", []),
]
for fx, sr, tempo, times, le, src, extra in CLOCK:
    add(fx, S(("midi", probe(times, 1, le)), tempo), sr, [play(), launch(0)],
        f"Clock at {tempo} BPM and {sr} Hz: note events at song beats {', '.join(f'{t:g}' for t in times)}",
        R_CLOCK + extra, PROV_X, ["AS-1"], src)
add("clock-140-start", S(("midi", probe([0, 1, 16], 1, 17)), "140"), 48000, [play(3.5), launch(0)],
    "Play from start beat 3.5: sample 0 plays beat 3.5; probe started there with no grid", R_CLOCK, PROV_X, ["AS-1"],
    "PBC-006")
add("clock-120-bar", S(("midi", probe([0, 1], 5, 2))), 48000, [play(-2.0), launch(0)],
    "Play with a negative start beat starts from beat 0; a 1 Bar press at sample 0 starts at once",
    R_GRID + ["REQ-PLAYBACK-CORE-004"], PROV_S, ["AS-1", "AS-4"], "PBC-007 (observed through a 1 Bar press)")
add("clock-140-quarter", S(("midi", probe([0, 1], 8, 2)), "140"), 48000,
    [play(), {"at": 30000, "action": "stop"}, {"at": 35000, "action": "continue"}, launch(40000)],
    "Stop holds the song beat; Continue resumes from it; a 1/4 press after Continue starts at beat 2",
    R_GRID + ["REQ-PLAYBACK-CORE-001", "REQ-PLAYBACK-CORE-005"], PROV_X, ["AS-1", "AS-4"],
    "PBC-008 (observed through a 1/4 press)")
LOOP_PROBE = dict(times=[0, 1, 2.5], dur=0.25, le=3)
LOOPS = [  # fixture, sr, tempo, loop, start beat, probe q, probe signature, press sample, source, provenance
    ("loop-4-8-120", 48000, "120", (True, "4", "4"), 4.0, 5, (3, 4), 390000, "PBC-009", PROV_X),
    ("loop-4-8-140", 48000, "140", (True, "4", "4"), 4.0, 5, (3, 4), 335000, "PBC-010", PROV_X),
    ("loop-4-8-140", 44100, "140", (True, "4", "4"), 0.0, 5, (3, 4), 310000, "PBC-011", PROV_X),
    ("loop-2-third", 48000, "120", (True, "2", "3.3333333333333335"), 0.0, 8, (4, 4), 290000, "PBC-012", PROV_X),
    ("loop-4-8-120", 48000, "120", (True, "4", "4"), 10.0, 5, (3, 4), 30000, "PBC-013", PROV_X),
]
for fx, sr, tempo, loop, sb, q, sig, r, src, prov in LOOPS:
    pr = probe(LOOP_PROBE["times"], q, LOOP_PROBE["le"], LOOP_PROBE["dur"], sig)
    add(fx, S(("midi", pr), tempo, loop=loop), sr, [play(sb), launch(r)],
        f"Song loop {loop[1]} + {float(loop[2]):g} on, Play from {sb:g}: a press at sample {r} is placed on the "
        "looped song time; the playing probe is not moved by later jumps", R_GRID + ["REQ-PLAYBACK-CORE-006"], prov,
        ["AS-1", "AS-4"], src + " (observed through a press after the listed jumps)")
add("loop-0-half", S(("midi", probe([0, 0.5], 9, 1, 0.25)), loop=(True, "0", "0.5")), 48000, [play(), launch(78000)],
    "Stored loop length 0.5 is used as 1 beat: jumps every 24,000 samples; a 1/4T press after the third jump",
    R_GRID + ["REQ-PLAYBACK-CORE-006"], PROV_S, ["AS-1", "AS-4"], "PBC-016 (observed through a 1/4T press)")

LV = {  # launch-case set variants: (song signature code, GlobalQuantisation, clip q, clip signature, tempo)
    "base": (201, 4, 0, (4, 4), "90"), "g3": (201, 3, 0, (4, 4), "90"), "g2": (201, 2, 0, (4, 4), "90"),
    "g1": (201, 1, 0, (4, 4), "90"), "s34": (200, 4, 0, (4, 4), "90"), "s34-g1": (200, 1, 0, (4, 4), "90"),
    "s68": (302, 4, 0, (4, 4), "90"), "s78": (303, 4, 0, (4, 4), "90"), "s54-g3": (202, 3, 0, (4, 4), "90"),
    **{f"g{q}": (201, q, 0, (4, 4), "90") for q in range(5, 14)},
    "c8": (201, 4, 8, (4, 4), "90"), "c68-5": (201, 4, 5, (6, 8), "90"), "c68-0": (201, 4, 0, (6, 8), "90"),
    "base-120": (201, 4, 0, (4, 4), "120"), "c1": (201, 4, 1, (4, 4), "90"), "g0": (201, 0, 0, (4, 4), "90"),
}
GRID_PRESSES = [("CLC-031", "base", 5.3), ("CLC-032", "g3", 9), ("CLC-033", "g2", 17), ("CLC-034", "g1", 1),
                ("CLC-035", "s34", 4), ("CLC-036", "s34-g1", 1), ("CLC-037", "s68", 1), ("CLC-038", "s78", 4),
                ("CLC-039", "s54-g3", 1), ("CLC-040", "g5", 2.25), ("CLC-041", "g6", 1.5), ("CLC-042", "g7", 2.1),
                ("CLC-043", "g8", 1), ("CLC-044", "g9", 3.1), ("CLC-045", "g10", 0.4), ("CLC-046", "g11", 1.3),
                ("CLC-047", "g12", 0.2), ("CLC-048", "g13", 0.13), ("CLC-049", "c8", 2.1), ("CLC-050a", "c68-5", 1.2),
                ("CLC-050b", "c68-5", 4.2), ("CLC-051", "c68-0", 1.2), ("CLC-054 (t = 3.99)", "base", 3.99),
                ("CLC-054 (t = 4 exactly)", "base", 4.0)]
VLABEL = {201: "4/4", 200: "3/4", 202: "5/4", 302: "6/8", 303: "7/8"}


def launch_set(var):
    sig, gq, q, csig, tempo = LV[var]
    return S(("midi", pulse(q, csig)), tempo, sig, gq)


def press_sample(t, sr, tempo):
    return round(t * (sr / m.f32(float(tempo))) * 60.0)


def setup_text(var):
    sig, gq, q, csig, tempo = LV[var]
    clip = "Global" if q == 0 else ("None" if q == 1 else f"own value {q}")
    return f"song {VLABEL[sig]}, GlobalQuantisation {gq}, Pulse launch quantization {clip} with clip signature " \
           f"{csig[0]}/{csig[1]}, {tempo} BPM"


for src, var, t in GRID_PRESSES:
    for sr in (44100, 48000):
        r = press_sample(t, sr, LV[var][4])
        add(f"launch-{var}", launch_set(var), sr, [play(), launch(r)],
            f"Press at sample {r} (song beat {t:g}); {setup_text(var)}", R_GRID,
            PROV_X, ["AS-1", "AS-4"] + (["AS-3"] if LV[var][2] == 0 else []), f"PBC-020/021/022/024 with {src}")
add("launch-g8", launch_set("g8"), 44100, [play(), launch(98000)],
    "1/4T press exactly on the triplet line 10/3 (sample 98,000) launches at beat 4, not 10/3", R_GRID, PROV_X,
    ["AS-1", "AS-3", "AS-4"], "PBC-024 with CLC-064")
add("launch-base-120", launch_set("base-120"), 48000, [play(), launch(127200)],
    "Press at song beat 5.3, 120 BPM, 1 Bar: starts at beat 8", R_GRID, PROV_X, ["AS-1", "AS-3", "AS-4"], "PBC-025")
for sr in (44100, 48000):
    r = press_sample(5.3, sr, "90")
    add("launch-c1", launch_set("c1"), sr, [play(), launch(r)],
        f"Clip launch quantization None: the clip's start is the press beat (sample {r})",
        ["REQ-PLAYBACK-CORE-002", "REQ-PLAYBACK-CORE-007", "REQ-PLAYBACK-CORE-010", "REQ-PLAYBACK-CORE-011",
         "REQ-PLAYBACK-CORE-012"], PROV_S, ["AS-1"], "PBC-026 (CLC-052)")
add("launch-g0", launch_set("g0"), 44100, [play(), launch(press_sample(5.3, 44100, "90"))],
    "Global quantization None with a Global clip: the clip's start is the press beat",
    ["REQ-PLAYBACK-CORE-002", "REQ-PLAYBACK-CORE-007", "REQ-PLAYBACK-CORE-010", "REQ-PLAYBACK-CORE-011",
     "REQ-PLAYBACK-CORE-012"], PROV_S, ["AS-1", "AS-3"], "CLC-053")
add("launch-base", launch_set("base"), 44100,
    [{"at": 0, "action": "launch", "track": 1, "slot": 1, "transport": "stopped", "start_beat": 0.0}],
    "Launch while stopped with start beat 0: the transport starts and the first note-on is at sample 0",
    ["REQ-PLAYBACK-CORE-010", "REQ-PLAYBACK-CORE-011", "REQ-PLAYBACK-CORE-012"], PROV_S, ["AS-1", "AS-3", "AS-4"],
    "PBC-027")


def edit(i, n):
    def f(notes):
        if i is None:
            notes.append(n)
        else:
            notes[i] = n
    return f


R_MIDI = ["REQ-PLAYBACK-CORE-002", "REQ-PLAYBACK-CORE-011", "REQ-PLAYBACK-CORE-012", "REQ-PLAYBACK-CORE-013",
          "REQ-PLAYBACK-CORE-015"]
MIDI = [  # fixture, clip, window, purpose, extra requirements, provenance, source
    ("midi-pulse", pulse(5), 288000, "Two passes of a looped 1-bar clip launched at beat 4", [], PROV_X, "PBC-040"),
    ("midi-startrel", pulse(5, start_rel=0.125), 285000,
     "StartRelative 0.125: the note under way at the start is not played; pass 2 starts at 189,000", [], PROV_X, "PBC-041"),
    ("midi-cut", pulse(5, edit=edit(7, note(3.5, 1, off=80))), 288000,
     "A note held across the loop end is cut at the wrap with velocity 64, before the next note-on",
     ["REQ-PLAYBACK-CORE-014"], PROV_S, "PBC-042"),
    ("midi-off-at-end", pulse(5, edit=edit(7, note(3.5, 0.5, off=90))), 288000,
     "A note-off exactly at the loop end keeps its own velocity and comes before the wrap's note-on", [], PROV_S,
     "new: REQ-013 note-off at Le"),
    ("midi-zero", pulse(5, edit=edit(1, note(0.5, 0))), 192000,
     "A zero-length note: note-off one lattice step after its note-on", [], PROV_X, "PBC-043"),
    ("midi-unlooped", pulse(5, loop_on=False), 240000, "LoopOn false: one pass, then nothing",
     ["REQ-PLAYBACK-CORE-014"], PROV_X, "PBC-044"),
    ("midi-unlooped-held", pulse(5, loop_on=False, edit=edit(7, note(3.5, 1, off=80))), 240000,
     "LoopOn false: a note still sounding at the clip end gets velocity 64 there", ["REQ-PLAYBACK-CORE-014"],
     PROV_S, "PBC-045"),
    ("midi-disabled", pulse(5, edit=edit(2, note(1.0, 0.25, on=False))), 192000,
     "A disabled note sends neither note-on nor note-off", [], PROV_X, "PBC-046"),
    ("midi-at-end", pulse(5, edit=edit(None, note(4, 0.25))), 288000,
     "A note at the loop end (clip time 4) never plays", [], PROV_S, "PBC-047"),
    ("midi-velocity", pulse(5, edit=edit(3, note(1.5, 0.25, vel=63.5))), 192000,
     "A fractional velocity 63.5 is sent unrounded", [], PROV_X, "new: REQ-012 velocity clause"),
]
for fx, clip, win, purpose, extra, prov, src in MIDI:
    add(fx, S(("midi", clip)), 48000, [play(), launch(24000)], purpose + " (120 BPM, 48,000 Hz, press at beat 1)",
        R_MIDI + R_GRID[1:4] + extra, prov, ["AS-1", "AS-4"], src, kind="midi", window=win)
add("midi-pulse-110", S(("midi", pulse(5)), "110"), 44100, [play(), launch(24055)],
    "110 BPM at 44,100 Hz (samples per beat 24,054.545...): first note-on at 96,219", R_MIDI + R_GRID[1:4], PROV_X,
    ["AS-1", "AS-4"], "PBC-049", kind="midi", window=192437)
add("midi-pulse-90", S(("midi", pulse(5)), "90"), 48000, [play(), launch(32000)],
    "90 BPM at 48,000 Hz: whole-beat note events at P or P + 1", R_MIDI + R_GRID[1:4], PROV_X, ["AS-1", "AS-4"],
    "PBC-050", kind="midi", window=256000)


def aclip(wav="tone48.wav", hiq=False, coarse="0", volume="1", ls="0"):
    return {"name": "Tone", "wav": wav, "ls": ls, "le": "0.01", "hiq": hiq, "coarse": coarse, "volume": volume,
            "q": 5, "sig": (4, 4)}


R_AUDIO = ["REQ-PLAYBACK-CORE-007", "REQ-PLAYBACK-CORE-008", "REQ-PLAYBACK-CORE-009", "REQ-PLAYBACK-CORE-017",
           "REQ-PLAYBACK-CORE-018", "REQ-PLAYBACK-CORE-019", "REQ-PLAYBACK-CORE-020"]
AUDIO = [  # fixture, clip, sr, press sample, purpose, provenance, assumptions, source
    ("audio-direct-hiq", aclip(hiq=True), 48000, 24000, "48 kHz file at 48 kHz, HiQ on: direct copy",
     PROV_X, [], "PBC-060"),
    ("audio-direct", aclip(), 48000, 24000, "48 kHz file at 48 kHz, HiQ off: direct copy", PROV_X, [],
     "PBC-060 (HiQ off)"),
    ("audio-linear", aclip("tone44.wav"), 48000, 24000, "44.1 kHz file at 48 kHz, HiQ off: linear interpolation, "
     "step 0.91875", PROV_X, [], "PBC-062"),
    ("audio-octave", aclip(coarse="12"), 48000, 24000, "PitchCoarse 12, HiQ off: linear interpolation with step "
     "8,589,939,712 / 2^32", PROV_X, ["AS-5"], "PBC-065"),
    ("audio-gain-6db", aclip(volume="0.5011872336272722"), 48000, 24000, "SampleVolume 0.5011872336272722",
     PROV_X, ["AS-5"], "PBC-066"),
    ("audio-gain-zero", aclip(volume="0"), 48000, 24000, "SampleVolume 0 plays at -70 dB, not silence", PROV_X,
     ["AS-5"], "PBC-066"),
    ("audio-gain-10", aclip(volume="10"), 48000, 24000, "SampleVolume 10", PROV_X, ["AS-5"], "PBC-066"),
    ("audio-gain-20", aclip(volume="20"), 48000, 24000, "SampleVolume 20 is limited to +24 dB", PROV_X, ["AS-5"],
     "PBC-066"),
    ("audio-loopstart", aclip(ls="0.00251"), 48000, 24000, "LoopStart 0.00251 s: output starts at frame 120 with "
     "fraction 0", PROV_S, [], "PBC-067 (new value)"),
    ("audio-direct", aclip(), 44100, 22050, "48 kHz file at 44.1 kHz, HiQ off: linear interpolation, step "
     "48000/44100", PROV_X, [], "new: REQ-017 step at 44,100 Hz"),
]
for fx, clip, sr, r, purpose, prov, extra, src in AUDIO:
    add(fx, S(("audio", clip)), sr, [play(), launch(r)], purpose + f" (120 BPM, press at sample {r}, launch at beat 4)",
        R_AUDIO, prov, ["AS-1", "AS-2", "AS-4"] + extra, src, kind="audio")
