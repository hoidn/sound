"""T1.4 extracted execution of Live 12.4.3 track-output mixing functions (ADR 0003, evidence label X).

Runs original x86_64 functions of the Live slice under the xexec harness (harness/, a copy of
x2-mixer-v1/harness; tools/xexec is not modified). The Live x86_64 functions are anonymous; each
was matched to its named twin in the x86_64 Ableton Live Engine bundle (match_engine.py, same
function size from LC_FUNCTION_STARTS, >= 87 % identical bytes; see addresses.json):

  0x101b40d30  OTrackOutVolumeProcessor::TSendVolumes::Calc(in[13], out[4])   (engine 0x171a20)
  0x101b40cf0  OTrackOutVolumeProcessor::TVolumeSwitch::Calc(in[5], out[4])   (engine 0x1719e0)
  0x101b2b970  ORampInterpolator::SetRamp(float, int)                         (engine 0x15c620)
  0x101b2ba30  ORampInterpolator::GetRamp() -> {float target, int length}     (engine 0x15c6e0)
  0x101b2ba80  ORampInterpolator::Extrapolate(int) -> float                   (engine 0x15c730)
  0x101b2bae0  ORampInterpolator::Inc(int)                                    (engine 0x15c790)
  0x101b243f0  volume-panner input 1 (Pan) setter (block, TRampEvent*, time)  (engine 0x1550a0)
  0x101b244a0  volume-panner input 4 (Volume) setter                          (engine 0x155150)
  0x101b27860  volume-panner recompute (called by the setters)                (engine 0x158510)
  0x101b719e0  TVolumePanner::Calc (the pan law of x2-mixer-v1)               (engine 0x1a26d0)
  0x101ae9e90  OSoloPrehearMode::SIsSpeakerIrrelevant(type)                   (engine 0x11ab30)
  0x101ae9eb0  OSoloPrehearMode::SIsSoloOrPrehear(type)                       (engine 0x11ab50)
  0x101ae9ed0  OSoloPrehearMode::SIsMutedForSolo(type)                        (engine 0x11ab70)
  0x101b3fdc0  OTrackOutSwitchesProcessor::OnSpeaker(float)                   (engine 0x170ab0)
  0x101b3ff50  OTrackOutSwitchesProcessor::OnSoloPrehear(float)               (engine 0x170c40)
  0x101b401c0  OTrackOutSplitSwitchesProcessor::OnIn(float)                   (engine 0x170eb0)
  0x101b0ecb0  NAudioTraits::SInitDebugOptionValues                           (engine 0x13f960)
  0x101b0ee70  NAudioTraits::STrackFadeTime -> samples                        (engine 0x13fb20)
  0x1011f1610  cubic Bezier point (s, double P[8]) -> (x beats, y value), used by the logic
               side to turn a curved envelope segment into 15 interior points (fork notes)
  0x101b1f400  OFloatAutomationSegment::Init(v0, v1, duration, offset)       (engine 0x1500b0)
The switch processors call an output callback through a pointer in the object; the harness points
it at a `ret` instruction of the slice (0x101b0ee93) so the call does nothing, and reads the state
the processor stored.

usage: python3 -I -B run_mix.py      (writes results/mix.json and raw/runs.jsonl next to this file)
Every call sequence runs in its own xexec process. No import is expected to be called.
"""
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'harness'))
from xexec import Runner, as_f32, f32, flt  # noqa: E402

SEND_CALC = 0x101b40d30
SWITCH_CALC = 0x101b40cf0
SET_RAMP = 0x101b2b970
GET_RAMP = 0x101b2ba30
EXTRAPOLATE = 0x101b2ba80
INC = 0x101b2bae0
SET_PAN = 0x101b243f0
SET_VOLUME = 0x101b244a0
SOLO_PREDICATES = [('SIsSpeakerIrrelevant', 0x101ae9e90), ('SIsSoloOrPrehear', 0x101ae9eb0),
                   ('SIsMutedForSolo', 0x101ae9ed0)]
ON_SPEAKER, ON_SOLO_PREHEAR, SPLIT_ON_IN = 0x101b3fdc0, 0x101b3ff50, 0x101b401c0
INIT_TRAITS, TRACK_FADE_TIME = 0x101b0ecb0, 0x101b0ee70
BEZIER = 0x1011f1610
SEGMENT_INIT = 0x101b1f400
SAMPLES_PER_BEAT = 22050.0         # 44.1 kHz at 120 BPM, for the segment runs
RET = 0x101b0ee93                  # a `ret` instruction (end of 0x101b0ee70), used as a no-op callback

R = Runner()


def floats(raw, n):
    return list(struct.unpack(f'<{n}f', raw[:4 * n]))


def interp(raw):
    """An ORampInterpolator: double value at +0, double slope at +8, int remaining at +16."""
    value, slope, remaining = struct.unpack_from('<ddi', raw, 0)
    return {'value': value, 'slope': slope, 'remaining': remaining}


def dump(res, expr):
    for e, _, raw in res.dumps:
        if e == expr:
            return raw
    raise RuntimeError(f'no dump {expr}: rc={res.rc} {res.stderr[-300:]}')


def ramp_event(value, length):
    return 'hex:' + struct.pack('<fi', value, length).hex()


# ---- sends: TSendVolumes::Calc --------------------------------------------------------------
# Input layout (static, from the handlers that write each slot of a send's 13-input block):
#   0 SendsOn  1 SendOutsConnected bit  2 SendIsPost  3 Send level  4..7 the track's panned-volume
#   matrix (L->L, L->R, R->L, R->R; output of the pan law)  8 GroupOn  9..12 group matrix.
# The processor constructor sets 8 to 1 and 9..12 to (1, 0, 0, 1) for every send.
M = (0.9, 0.1, 0.2, 0.6)          # distinct values so the composition is visible
G = (0.5, 0.05, 0.07, 0.25)
ID = (1.0, 0.0, 0.0, 1.0)
SEND_CASES = [
    ('post, defaults for 8..12', (1, 1, 1, 0.5, *M, 1, *ID)),
    ('pre, defaults for 8..12', (1, 1, 0, 0.5, *M, 1, *ID)),
    ('post, group matrix G', (1, 1, 1, 0.5, *M, 1, *G)),
    ('pre, group matrix G', (1, 1, 0, 0.5, *M, 1, *G)),
    ('IsPost 0.5 (mid-ramp)', (1, 1, 0.5, 0.5, *M, 1, *ID)),
    ('SendsOn 0', (0, 1, 1, 0.5, *M, 1, *ID)),
    ('SendsOn 0.5 (mid-ramp)', (0.5, 1, 1, 0.5, *M, 1, *ID)),
    ('not connected', (1, 0, 1, 0.5, *M, 1, *ID)),
    ('send level 0', (1, 1, 1, 0.0, *M, 1, *ID)),
    ('GroupOn 0', (1, 1, 1, 0.5, *M, 0, *ID)),
    ('post, send 1, pan-law matrix of pan -0.5 vol 0.5', (1, 1, 1, 1.0, 0.65328, 0.0, 0.0, 0.270598, 1, *ID)),
    ('pre, send 1, same matrix', (1, 1, 0, 1.0, 0.65328, 0.0, 0.0, 0.270598, 1, *ID)),
]


def sends():
    out = []
    for name, inp in SEND_CASES:
        res = R.run(['call', hex(SEND_CALC), 'buf:8', 'hex:' + struct.pack('<13f', *inp).hex(),
                     'buf:16', 'dump', 'b2', '16'])
        out.append({'case': name, 'in': [f32(x) for x in inp], 'out_LL_LR_RL_RR': floats(dump(res, 'b2'), 4)})
    return out


def switch():
    out = []
    for on in (1.0, 0.0, 0.5):
        inp = (on, 0.9, 0.1, 0.2, 0.6)
        res = R.run(['call', hex(SWITCH_CALC), 'buf:8', 'hex:' + struct.pack('<5f', *inp).hex(),
                     'buf:16', 'dump', 'b2', '16'])
        out.append({'MainOn': on, 'matrix_in': list(inp[1:]), 'out': floats(dump(res, 'b2'), 4)})
    return out


# ---- ramps: ORampInterpolator -----------------------------------------------------------------
def ramps():
    out = []
    # a ramp from 0 to 1 over 4 samples, advanced one sample at a time
    toks = ['call', hex(SET_RAMP), 'buf:24', flt(1.0), 'i:4']
    for _ in range(5):
        toks += ['call', hex(INC), 'ref:b0', 'i:1', 'dump', 'b0', '24']
    res = R.run(toks)
    steps = [interp(raw) for e, _, raw in res.dumps]
    out.append({'case': 'SetRamp(1.0, 4) from 0, then Inc(1) five times', 'states': steps})
    # target and length reported to the next processor, and extrapolation, mid-ramp
    res = R.run(['call', hex(SET_RAMP), 'buf:24', flt(0.5), 'i:100', 'call', hex(INC), 'ref:b0', 'i:30',
                 'call', hex(GET_RAMP), 'ref:b0', 'call', hex(EXTRAPOLATE), 'ref:b0', 'i:20',
                 'call', hex(EXTRAPOLATE), 'ref:b0', 'i:500', 'dump', 'b0', '24'])
    get = res.calls[2]['rax']
    out.append({'case': 'SetRamp(0.5, 100) from 0, Inc(30), GetRamp, Extrapolate(20), Extrapolate(500)',
                'state': interp(dump(res, 'b0')),
                'GetRamp': {'target': as_f32(get & 0xffffffff), 'length': get >> 32},
                'Extrapolate20': as_f32(res.calls[3]['xmm0']), 'Extrapolate500': as_f32(res.calls[4]['xmm0'])})
    # a step below the 1e-12-per-sample threshold jumps at once; a value below 1e-12 reads as 0
    res = R.run(['call', hex(SET_RAMP), 'buf:24', flt(1e-9), 'i:10000', 'dump', 'b0', '24',
                 'call', hex(GET_RAMP), 'ref:b0'])
    get = res.calls[1]['rax']
    out.append({'case': 'SetRamp(1e-9, 10000) from 0 (slope 1e-13 < 1e-12)', 'state': interp(dump(res, 'b0')),
                'GetRamp': {'target': as_f32(get & 0xffffffff), 'length': get >> 32}})
    res = R.run(['call', hex(SET_RAMP), 'buf:24', flt(5e-13), 'i:0', 'call', hex(GET_RAMP), 'ref:b0'])
    get = res.calls[1]['rax']
    out.append({'case': 'SetRamp(5e-13, 0): value below 1e-12', 'GetRamp_target': as_f32(get & 0xffffffff)})
    return out


# ---- the volume-panner ramp calculator ----------------------------------------------------------
# Block: inputs PanModeAmount +0x00, Pan +0x18, SplitL +0x30, SplitR +0x48, Volume +0x60;
# outputs L->L +0x78, L->R +0x90, R->L +0xa8, R->R +0xc0; last sample time +0xe0 (int64).
OUT_OFFS = (0x78, 0x90, 0xa8, 0xc0)
IN_OFFS = (0x00, 0x18, 0x30, 0x48, 0x60)


def panner():
    """Pan and Volume inputs set through the original input setters; outputs read as (target, length)."""
    toks = ['call', hex(SET_RAMP), 'buf:256', flt(0.0), 'i:0',                    # b0: block, PanModeAmount 0
            'call', hex(SET_RAMP), 'ref:b0+0x30', flt(-1.0), 'i:0',               # SplitL -1
            'call', hex(SET_RAMP), 'ref:b0+0x48', flt(1.0), 'i:0',                # SplitR +1
            'call', hex(SET_VOLUME), 'ref:b0', ramp_event(1.0, 0), 'i:0', 'dump', 'b0', '256',
            'call', hex(SET_VOLUME), 'ref:b0', ramp_event(0.5, 100), 'i:0', 'dump', 'b0', '256',
            'call', hex(SET_PAN), 'ref:b0', ramp_event(-1.0, 50), 'i:20', 'dump', 'b0', '256']
    res = R.run(toks)
    names = ['t=0: Volume set to 1 at once (Pan 0, splits -1/+1, PanModeAmount 0)',
             't=0: Volume ramp to 0.5 over 100 samples',
             't=20: Pan ramp to -1 over 50 samples while the Volume ramp runs']
    out = []
    for name, (_, _, raw) in zip(names, res.dumps):
        outputs = []
        for o in OUT_OFFS:
            s = interp(raw[o:o + 24])
            outputs.append({'target': s['value'] + s['slope'] * s['remaining'], 'length': s['remaining']})
        out.append({'step': name, 'inputs': [interp(raw[o:o + 24]) for o in IN_OFFS], 'outputs': outputs})
    return out


def solo():
    out = {'predicates': [], 'switch_word': [], 'split': [], 'track_fade_time': None}
    for name, addr in SOLO_PREDICATES:
        row = {'function': name, 'true_for_types': []}
        for t in range(8):
            res = R.run(['call', hex(addr), f'i:{t}'])
            if res.calls[-1]['rax'] & 0xff:
                row['true_for_types'].append(t)
        out['predicates'].append(row)
    # `call RET buf:N` only allocates the zeroed object b0; the callback pointer is then poked in
    for t in range(8):
        for spk in (0.0, 1.0):
            res = R.run(['call', hex(RET), 'buf:48', 'poke', 'b0+0x10', hex(RET),
                         'call', hex(ON_SPEAKER), 'ref:b0', flt(spk),
                         'call', hex(ON_SOLO_PREHEAR), 'ref:b0', flt(float(t)), 'dump', 'b0', '48'])
            word = struct.unpack_from('<I', dump(res, 'b0'), 8)[0]
            out['switch_word'].append({'solo_type': t, 'speaker': spk, 'word': word,
                                       'MainOn': word & 1, 'SendsOn': (word >> 1) & 1,
                                       'PrehearOn': (word >> 2) & 1, 'bit3': (word >> 3) & 1})
    for word in range(16):
        res = R.run(['call', hex(RET), 'buf:88', 'poke', 'b0+0x08', hex(RET), 'poke', 'b0+0x20', hex(RET),
                     'poke', 'b0+0x38', hex(RET), 'call', hex(SPLIT_ON_IN), 'ref:b0', flt(float(word)),
                     'dump', 'b0', '88'])
        raw = dump(res, 'b0')
        out['split'].append({'word': word, 'MainOn': raw[0x50], 'SendsOn': raw[0x51], 'PrehearOn': raw[0x52]})
    res = R.run(['call', hex(INIT_TRAITS), 'call', hex(TRACK_FADE_TIME)])
    out['track_fade_time'] = {'ok': res.ok, 'samples': res.calls[-1]['rax'] & 0xffffffff if res.ok else None,
                              'stderr': res.stderr[-200:]}
    return out


def bezier_points(t0, v0, t1, v1, x1, y1, x2, y2):
    """The 15 interior points the logic side sends for a curved segment (s = (i+1)/16)."""
    dt, dv = t1 - t0, v1 - v0
    ctrl = struct.pack('<8d', t0, v0, t0 + x1 * dt, v0 + y1 * dv, t0 + x2 * dt, v0 + y2 * dv, t1, v1).hex()
    toks = []
    for i in range(15):
        toks += ['call', hex(BEZIER), 'd:' + ((i + 1) * 0.0625).hex(), 'hex:' + ctrl if i == 0 else 'ref:b0']
    res = R.run(toks)
    return [(struct.unpack('<d', struct.pack('<Q', c['xmm0']))[0], f32(struct.unpack('<d', struct.pack('<Q', c['xmm1']))[0]))
            for c in res.calls]


def segment_value(ta, va, tb, vb, t):
    """Value at song beat t of the engine segment from (ta, va) to (tb, vb), durations in samples."""
    res = R.run(['call', hex(SEGMENT_INIT), 'buf:40', flt(va), flt(vb), 'd:' + ((tb - ta) * SAMPLES_PER_BEAT).hex(),
                 'd:' + ((t - ta) * SAMPLES_PER_BEAT).hex(), 'dump', 'b0', '40'])
    value, _, slope, lo, hi = struct.unpack('<ddddd', dump(res, 'b0'))
    return {'value': value, 'slope_per_sample': slope, 'lo': lo, 'hi': hi}


def automation():
    out = {}
    # E9: Pan (0, -1) with controls 0.5/0/0.5/0, then (4, 1); REQ-AUTOMATION-ENVELOPES-010 (X) gives
    # -0.983523965, -0.75, 0.0164760482 at t = 1, 2, 3
    pts = [(0.0, -1.0)] + bezier_points(0.0, -1.0, 4.0, 1.0, 0.5, 0.0, 0.5, 0.0) + [(4.0, 1.0)]
    played = []
    for t in (1.0, 2.0, 3.0):
        k = max(i for i in range(len(pts) - 1) if pts[i][0] <= t)
        (ta, va), (tb, vb) = pts[k], pts[k + 1]
        played.append({'t': t, 'segment': [pts[k], pts[k + 1]], **segment_value(ta, va, tb, vb, t)})
    out['E9_polyline'] = {'points': pts, 'played': played,
                          'evaluator_REQ010_X': [-0.983523965, -0.75, 0.0164760482]}
    # E13: (L, 1), (4, 0); the leading event's time is sent as -1e7 beats (fork notes, 0x102823cb0)
    out['E13_t0'] = {'played_from_minus_1e7': segment_value(-1e7, 1.0, 4.0, 0.0, 0.0),
                     'evaluator_REQ010_X': 6.341957714539603e-08}
    # E1: (4, 0), (8, 1): linear, t = 5, 6, 7
    out['E1_linear'] = [{'t': t, **segment_value(4.0, 0.0, 8.0, 1.0, t)} for t in (5.0, 6.0, 7.0)]
    # E12: (L, 0), (0, 0), (3, 1) at t = 1; REQ-010 evaluator (X2) gives 0.3333333432674408 (binary32)
    e12 = segment_value(0.0, 0.0, 3.0, 1.0, 1.0)
    out['E12_t1'] = {**e12, 'as_binary32': f32(e12['value']), 'evaluator_REQ010_X': 0.3333333432674408}
    # clamping of the start offset (negative offset counts as 0; result kept inside [v0, v1])
    out['segment_offset_edges'] = [{'case': 'offset -10 samples', **segment_value(0.0, 0.0, 1.0, 1.0, -10 / SAMPLES_PER_BEAT)},
                                   {'case': 'offset beyond the end', **segment_value(0.0, 0.0, 1.0, 1.0, 2.0)},
                                   {'case': 'equal values', **segment_value(0.0, 0.5, 1.0, 0.5, 0.5)}]
    return out


def main():
    results = {'sends': sends(), 'main_switch': switch(), 'ramp_interpolator': ramps(), 'volume_panner': panner(),
               'solo': solo(), 'automation': automation()}
    used = {}
    for _, res in R.log:
        for sym, n in res.used.items():
            used[sym] = used.get(sym, 0) + n
    results['replaced_imports_called'] = dict(sorted(used.items()))
    results['runs'] = {'count': len(R.log), 'not_ok': sum(not r.ok for _, r in R.log)}
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'mix.json').write_text(json.dumps(results, indent=1) + '\n')
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for argv, res in R.log:
            f.write(json.dumps({'argv': argv, 'rc': res.rc, 'stdout': res.stdout,
                                'stderr': res.stderr, 'timeout': res.timeout}) + '\n')
    for r in results['sends']:
        print('send', r['case'], [round(x, 6) for x in r['out_LL_LR_RL_RR']])
    for r in results['main_switch']:
        print('switch', r['MainOn'], [round(x, 6) for x in r['out']])
    for r in results['ramp_interpolator']:
        print('ramp', json.dumps(r))
    for r in results['volume_panner']:
        print('panner', r['step'], [(round(o['target'], 6), o['length']) for o in r['outputs']])
    for r in results['solo']['predicates']:
        print('predicate', r['function'], r['true_for_types'])
    print('switch', [(r['solo_type'], int(r['speaker']), r['word']) for r in results['solo']['switch_word']])
    print('split', [(r['word'], r['MainOn'], r['SendsOn'], r['PrehearOn']) for r in results['solo']['split']])
    print('track fade time', results['solo']['track_fade_time'])
    a = results['automation']
    print('E9 points', [(round(x, 6), round(y, 6)) for x, y in a['E9_polyline']['points']])
    print('E9 played', [(p['t'], p['value']) for p in a['E9_polyline']['played']], 'evaluator', a['E9_polyline']['evaluator_REQ010_X'])
    print('E13 t0 played', a['E13_t0']['played_from_minus_1e7']['value'], 'evaluator', a['E13_t0']['evaluator_REQ010_X'])
    print('E1', [(p['t'], p['value']) for p in a['E1_linear']])
    print('E12 t1', a['E12_t1']['value'], a['E12_t1']['as_binary32'])
    print('edges', [(p['case'], p['value']) for p in a['segment_offset_edges']])
    print('runs', results['runs'], 'replaced imports:', ', '.join(results['replaced_imports_called']) or 'none')


if __name__ == '__main__':
    main()
