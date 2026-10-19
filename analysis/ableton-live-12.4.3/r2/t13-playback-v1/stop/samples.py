"""Stop instants of the proposed acceptance cases, in beats and output-sample indices (harness arithmetic; data).

usage: python3 -I samples.py        (reads results/stop.json; writes results/samples.json)

Rules applied (each is a static reading cited in the fork report; none is X except where results/stop.json is used):
  B       the stop boundary: X values from results/stop.json (grid 0x101ad2ef0, press rounding 0x1011999d0 mode 3,
          boundary 0x101ae8280); o, the predelay: X values from results/stop.json (0x102278eb0) for audio
          tracks, 0 for MIDI tracks (S: the MIDI clip player's predelay slot returns 0.0).
  near    if B - t < o and the song was already playing: B := B + grid (S, 0x101af9eb0).
  event   the stop event's song beat E = B - o, rounded to the 1/3,843,840 lattice by the scheduler (S,
          0x101ad9760 = Engine OScheduler::ScheduleAbsoluteBeatEvent, the same formula as REQ-CLIP-LAUNCH-013).
  sample  the first output sample with the stop applied: ceil((E - b0) * spb + n0), spb = (SR / tempo) * 60 in
          binary64 with tempo binary32 (S, Engine OScheduler::DoSetTempo and ProcessNextEvents; the scheduler
          rule is owned by the transport fork, which may refine it). b0 = 0, n0 = 0: transport started at song
          beat 0 on output sample 0, tempo constant since.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 3843840


def lattice(x):
    s = 1.0 if x >= 0 else -1.0
    return s * (math.floor(abs(x + s * (1.0 / N) / 2) * N) / N)


def sample(e, sr, tempo=90.0):
    return math.ceil((e - 0.0) * ((sr / tempo) * 60.0) + 0)


X = json.loads((HERE / 'results' / 'stop.json').read_text())
B = {r['label']: r for r in X['stop_boundary']}
O = {r['label']: r['predelay_beats'] for r in X['predelay']}
O_AUDIO = O['stop: warped 1-bar session clip, Fade on, 90 BPM']


def case(cid, label, kind, o):
    r = B[label]
    b, t, g = r['B'], r['t_lattice'], r['grid']
    near = g > 0 and b - t < o
    if near:
        b = b + g
    e = lattice(b - o)
    immediate = (b - o) <= t
    return {'case': cid, 'stop_press': label, 'track': kind, 'grid': g, 'press_lattice': t, 'B': b,
            'next_line_rule': near, 'predelay_beats': o, 'event_beat': e, 'immediate': immediate,
            'sample_48000': None if immediate else sample(e, 48000), 'sample_44100': None if immediate else sample(e, 44100)}


rows = [
    case('STP-01', 'STP-quantized 4/4 1 Bar t=5.3', 'MIDI', 0.0),
    case('STP-02', 'STP-quantized 4/4 2 Bars t=9', 'MIDI', 0.0),
    case('STP-03', 'STP-quantized 4/4 1/4 t=2.1', 'MIDI', 0.0),
    case('STP-04', 'STP-quantized 3/4 1 Bar t=4', 'MIDI', 0.0),
    case('STP-05', 'STP-quantized 4/4 None t=5.3', 'MIDI', 0.0),
    case('STP-09', 'STP-quantized 4/4 1 Bar t=5.3', 'audio, Fade on', O_AUDIO),
    case('STP-10', 'STP-quantized 4/4 1 Bar t=7.996 (inside 0.006 of 8)', 'audio, Fade on', O_AUDIO),
    case('STP-11', 'STP-quantized 4/4 1 Bar t=7.996 (inside 0.006 of 8)', 'MIDI', 0.0),
    case('STP-12', 'STP-quantized 4/4 1 Bar t=5.3', 'audio, Fade off', 0.0),
    case('STP-17', 'STP-quantized 4/4 1/4T t=10/3', 'MIDI', 0.0),
    case('STP-18', 'STP-quantized 4/4 1 Bar t=8 exactly', 'MIDI', 0.0),
    case('STP-19', 'STP-quantized 4/4 1 Bar t=8 exactly', 'audio, Fade on', O_AUDIO),
    case('STP-20', 'STP-quantized 4/4 1/16 t=1.3', 'MIDI', 0.0),
]
# unlooped and unwarped clip ends (no press): event beats from results/stop.json
U = X['unwarped_end']
rows.append({'case': 'STP-14', 'what': 'unlooped warped 1-bar clip launched at beat 4 ends at 4 + (LoopEnd - LoopStart) = 8',
             'event_beat': lattice(4.0 + 4.0), 'sample_48000': sample(lattice(8.0), 48000), 'sample_44100': sample(lattice(8.0), 44100)})
for r, sr in ((U[0], 48000), (U[2], 44100)):
    e = lattice(r['end_beat'])
    rows.append({'case': 'STP-15', 'what': f'unwarped 2.0 s unlooped clip launched at beat 8, {sr} Hz', 'end_beat_x': r['end_beat'],
                 'event_beat': e, f'sample_{sr}': sample(e, sr), f'launch_sample_{sr}': sample(8.0, sr),
                 'length_samples': sample(e, sr) - sample(8.0, sr)})
(HERE / 'results' / 'samples.json').write_text(json.dumps(rows, indent=1) + '\n')
for r in rows:
    print(json.dumps(r))
