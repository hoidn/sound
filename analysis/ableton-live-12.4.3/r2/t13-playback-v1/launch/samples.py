"""T1.3 launch cases: expected launch sample indices from the static rules (analyst tool; output is data).

usage: python3 -I -B samples.py        (writes samples.json next to this file and prints a table)

Rules used (each is S, cited in the fork B report; the grid boundaries B come from the X2 runs,
r2/x2-notes-launch-v1/results/launch.json, boundary_cases):
  samples per beat   spb = (SR / T) * 60 in binary64, T the binary32 tempo   (Engine OScheduler::DoSetTempo 0x10c2e0)
  lattice            L(x) = s * floor(|x + s*h/2| * 3843840) / 3843840, h = 1/3843840 (binary64), s = sign
  event sample       N(b) = ceil((b - b0) * spb + n0), with (n0, b0) = (0, 0): beat 0 plays at sample 0 and the
                     scheduler is anchored there                            (Live x86 0x101ade8a0, Engine 0x10f540)
  launch pre-delay   o = 0 for MIDI clips; for audio clips the crossfade length (X: run_launch.py)
  event beat         E = L(B - o); the clip's start maps to song beat B
  near-boundary      if B - L(t) < o and the song was already playing: B := B + g (when g > 0)
The (n0, b0) = (0, 0) anchor is an assumption owned by the transport workstream; with another anchor N changes.
"""
import json
import math
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
H = 1 / 3843840


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def lattice(x):
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * H * 0.5) * 3843840.0) / 3843840.0)


def spb(sr, tempo):
    return (sr / f32(tempo)) * 60.0


def n_event(b, sr, tempo):
    return math.ceil(b * spb(sr, tempo))


def xfade(tempo, loop_secs=None, loop_beats=None):
    """Session clip with Fade on: min(half loop length in beats, 4 ms in beats) (X-confirmed formula)."""
    t = f32(tempo)
    half = (loop_beats * 0.5) if loop_beats is not None else ((loop_secs * 0.5) * t) / 60.0
    return min(half, (4.0 * 0.001 * t) / 60.0)


def case(cid, desc, tempo, t, g, B, o=0.0, playing=True, immediate=False):
    tl = lattice(t)
    if playing and g > 0 and B - tl < o:
        B = B + g
    E = lattice(B - o)
    row = {'id': cid, 'desc': desc, 'tempo': tempo, 'press_beat': t, 'press_lattice': tl, 'grid': g, 'B': B, 'o': o,
           'event_beat': E}
    for sr in (48000, 44100):
        row[f'spb_{sr}'] = spb(sr, tempo)
        row[f'event_sample_{sr}'] = None if immediate else n_event(E, sr, tempo)
        row[f'clip_origin_exact_{sr}'] = B * spb(sr, tempo)
    return row


X2 = json.load(open(HERE.parent.parent / 'x2-notes-launch-v1' / 'results' / 'launch.json'))
XB = {r['label']: (r['t']['v'], r['g']['v'], float.fromhex(r['B']['hex'])) for r in X2['boundary_cases']}

ROWS = []
for lab in ['CLC-031', 'CLC-032', 'CLC-033', 'CLC-034', 'CLC-035', 'CLC-036', 'CLC-037', 'CLC-038', 'CLC-039',
            'CLC-040', 'CLC-041', 'CLC-042', 'CLC-043', 'CLC-044', 'CLC-045', 'CLC-046', 'CLC-047', 'CLC-048',
            'CLC-049', 'CLC-050a', 'CLC-050b', 'CLC-051']:
    t, g, B = XB[lab]
    ROWS.append(case(lab, 'MIDI clip Slide, B1, X2 boundary', 90.0, t, g, B))
# press exactly on a grid line, MIDI: B = t; B - o <= now and the song was playing -> processed at the request
ROWS.append(case('PB-on-line-MIDI', 'MIDI, 1 Bar, press exactly at beat 8', 90.0, 8.0, 4.0, 8.0, immediate=True))
# audio: APC20 Demo track 4 (100 BPM, 1 Bar), session clips with Fade on, edited to IsWarped false (loop 0..28 s)
o100 = xfade(100.0, loop_secs=28.0)
ROWS.append(case('PB-audio-first', 'audio, no clip playing on the track (o = 0), t = 5.3', 100.0, 5.3, 4.0, 8.0, o=0.0))
ROWS.append(case('PB-audio-replace', 'audio replaces a playing audio clip, both Fade on, t = 5.3', 100.0, 5.3, 4.0, 8.0, o=o100))
ROWS.append(case('PB-audio-near', 'audio replaces, press 0.005 beat before B (B - t < o)', 100.0, 7.995, 4.0, 8.0, o=o100))
ROWS.append(case('PB-audio-far', 'audio replaces, press 0.01 beat before B (B - t > o)', 100.0, 7.99, 4.0, 8.0, o=o100))
ROWS.append(case('PB-audio-on-line', 'audio replaces, press exactly at beat 8', 100.0, 8.0, 4.0, 8.0, o=o100))
ROWS.append(case('PB-midi-near', 'MIDI clip, same press 0.005 beat before B (o = 0)', 100.0, 7.995, 4.0, 8.0))
ROWS.append(case('PB-120', 'MIDI, 120 BPM, 1 Bar, t = 5.3', 120.0, 5.3, 4.0, 8.0))

json.dump(ROWS, open(HERE / 'samples.json', 'w'), indent=1)
for r in ROWS:
    print(f"{r['id']:18} T={r['tempo']:5} t={r['press_beat']:<6} B={r['B']!r:20} o={r['o']!r:22} E={r['event_beat']!r:20} "
          f"N48={r['event_sample_48000']} N44.1={r['event_sample_44100']} origin48={r['clip_origin_exact_48000']!r} "
          f"origin44.1={r['clip_origin_exact_44100']!r}")

assert n_event(8.0, 48000, 90.0) == 256001 and n_event(8.0, 44100, 90.0) == 235200   # spb 32000.000000000004 / 29400
assert lattice(8.0 - o100) == 30725094 / 3843840 and n_event(lattice(8.0 - o100), 48000, 100.0) == 230208
