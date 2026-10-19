"""X2 extracted execution of Live 12.4.3 mixer value functions (ADR 0003, evidence label X).

Runs original x86_64 functions of the Live slice under the xexec harness (harness/xexec.py, a
copy of tools/xexec with a `poke` command and an `--patch` allocator option; see harness/xexec.c).
Targets, from the mixer-values research and the X1 addresses.json:

  fader curves (Q-019, PRB-S9-01):
    0x101aecd40  build the 7-curve registry object (modes 0..6) into a caller buffer
    0x101aecbd0  position -> gain for one curve object        (arm64 0x101ac3498)
    0x101aecc90  gain -> position for one curve object        (arm64 0x101ac353c)
  pan law (PRB-S9-02/03):
    0x101b3b95c  per-track 2x2 output-gain matrix             (arm64 0x101b3b95c, same address)
  crossfade curves (PRB-S9-06):
    0x101b1a470/550/630/6f0/7b0/880/8e0  CrossfadeToLevel{NormalDip,SlightDip,ConstantPower,
      Dipless,SlowCut,FastCut,Transition}                     (arm64 0x101aee8b8.. same order)
  track-switch text (c):
    0x1014353b0  Speaker value -> "On"/"Off" string

usage: python3 -I -B run_mixer.py           (writes results/, raw/runs.jsonl next to this file)

Allocators are redirected: Live's shared-memory pool (0x101ac2ea0) and block allocator
(0x101ac7a40) are patched to a zero-filling aligned_alloc adapter so the curve objects can be
built without initialising the real pool. Every call runs in its own xexec process.
"""
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'harness'))
from xexec import Runner, SLICE, as_f32, dbl, f32, flt, ustr  # noqa: E402

BUILD_CURVES = 0x101aecd40      # (buf) -> buf[1..7] = curve objects for modes 0..6
POS_TO_GAIN = 0x101aecbd0       # (float pos, curve_obj) -> float gain
GAIN_TO_POS = 0x101aecc90       # (float gain, curve_obj) -> float pos
PAN_MATRIX = 0x101b719e0        # (owner, float in[5], float out[4]); arm64 counterpart 0x101b3b95c
SWITCH_TEXT = 0x1014353b0       # (float value, sret) -> "On"/"Off"
EMPTY_STRING = 0x1014206e0      # shared empty Live string initialiser (SWITCH_TEXT needs it)
POOL_ALLOC = 0x101ac2ea0        # OMemoryPool::New (shared memory); patched to a plain allocator
BLOCK_ALLOC = 0x101ac7a40       # block allocator; patched to a plain allocator
PATCH = ['--patch', hex(POOL_ALLOC) + '=alloc32', '--patch', hex(BLOCK_ALLOC) + '=alloc64']

XFADE = [('NormalDip', 0x101b1a470), ('SlightDip', 0x101b1a550), ('ConstantPower', 0x101b1a630),
         ('Dipless', 0x101b1a6f0), ('SlowCut', 0x101b1a7b0), ('FastCut', 0x101b1a880),
         ('Transition', 0x101b1a8e0)]
MODE_VOLUME, MODE_SEND = 1, 0      # curve index used by track volume (mode 1) and sends (mode 0)

R = Runner()


def curve_obj(mode):
    """A dump expression for the mode-th curve object pointer inside the build buffer b0."""
    return f'b0+{(mode + 1) * 8}*'       # buf[mode+1] is the curve object for that mode


def fader():
    """position -> gain and gain -> position for the volume (mode 1) and send (mode 0) curves."""
    out = {'position_to_gain': [], 'gain_to_position': [], 'roundtrip_Q019': []}
    pts = [0.0, 0.25, 0.5, 0.7, 0.85, 1.0]
    for mode, name in ((MODE_VOLUME, 'volume'), (MODE_SEND, 'send')):
        for p in pts:
            res = R.run([*PATCH, 'call', hex(BUILD_CURVES), 'buf:64',
                         'call', hex(POS_TO_GAIN), flt(p), 'ref:' + curve_obj(mode)])
            g = as_f32(res.calls[-1]['xmm0']) if res.ok else None
            out['position_to_gain'].append({'curve': name, 'mode': mode, 'position': p, 'gain_x': g})
    # gain -> position at the gains the released cases name, plus a round trip of stored gains
    gain_cases = {'volume': [0.5, 0.001, 2.0, 1.0, 0.1995263397693634],
                  'send': [0.1000000014901161, 1.0, 0.0003162277571391314]}
    for mode, name in ((MODE_VOLUME, 'volume'), (MODE_SEND, 'send')):
        for g in gain_cases[name]:
            res = R.run([*PATCH, 'call', hex(BUILD_CURVES), 'buf:64',
                         'call', hex(GAIN_TO_POS), flt(g), 'ref:' + curve_obj(mode)])
            p = as_f32(res.calls[-1]['xmm0']) if res.ok else None
            out['gain_to_position'].append({'curve': name, 'mode': mode, 'gain': g, 'position_x': p})
    # Q-019: does stored gain -> position -> gain return the stored gain? (both pure, one process)
    for mode, name in ((MODE_VOLUME, 'volume'), (MODE_SEND, 'send')):
        for g in (0.0003162277571391314, 0.5011872053146362, 1.0,
                  1.9952623844146729 if name == 'volume' else 1.0):
            res = R.run([*PATCH, 'call', hex(BUILD_CURVES), 'buf:64',
                         'call', hex(GAIN_TO_POS), flt(g), 'ref:' + curve_obj(mode)])
            pos = as_f32(res.calls[-1]['xmm0']) if res.ok else None
            res2 = R.run([*PATCH, 'call', hex(BUILD_CURVES), 'buf:64',
                          'call', hex(POS_TO_GAIN), flt(pos), 'ref:' + curve_obj(mode)]) if pos is not None else None
            back = as_f32(res2.calls[-1]['xmm0']) if res2 and res2.ok else None
            out['roundtrip_Q019'].append({'curve': name, 'stored_gain': g, 'position_x': pos,
                                          'gain_back_x': back, 'exact_roundtrip': back == f32(g)})
    return out


def pan_matrix(w, pan, sl, sr, vol):
    data = struct.pack('<fffff', w, pan, sl, sr, vol).hex()
    res = R.run(['call', hex(PAN_MATRIX), 'i:0', 'hex:' + data, 'buf:16', 'dump', 'b1', '16'])
    for expr, _, raw in res.dumps:
        if expr == 'b1':
            return list(struct.unpack('<ffff', raw)), res
    return None, res


def pan_law():
    out = []
    # Stereo mode (w = 0): the pan cases of REQ-013; split pans at their defaults (-1, +1)
    for pan in (-1.0, -0.5, 0.0, 0.5, 1.0):
        g, _ = pan_matrix(0.0, pan, -1.0, 1.0, 1.0)
        out.append({'mode': 'stereo', 'w': 0.0, 'pan': pan, 'splitL': -1.0, 'splitR': 1.0,
                    'vol': 1.0, 'gains_LL_LR_RL_RR': g})
    # Split Stereo mode (w = 1): default splits pass through; splits (0,0) send each input to both
    for sl, sr in ((-1.0, 1.0), (0.0, 0.0), (-0.5, 0.5)):
        g, _ = pan_matrix(1.0, 0.0, sl, sr, 1.0)
        out.append({'mode': 'split', 'w': 1.0, 'pan': 0.0, 'splitL': sl, 'splitR': sr,
                    'vol': 1.0, 'gains_LL_LR_RL_RR': g})
    # vol = 0 gives silence
    g, _ = pan_matrix(0.0, -1.0, -1.0, 1.0, 0.0)
    out.append({'mode': 'stereo', 'w': 0.0, 'pan': -1.0, 'vol': 0.0, 'gains_LL_LR_RL_RR': g})
    return out


def crossfade():
    out = []
    positions = [-1.0, -0.95, -0.5, -0.25, 0.0, 0.25, 0.5, 0.95, 1.0]
    for name, addr in XFADE:
        row = {'curve': name, 'addr': hex(addr), 'levels': []}
        for c in positions:
            res = R.run(['call', hex(addr), flt(c)])
            row['levels'].append({'x': c, 'level_x': as_f32(res.calls[-1]['xmm0']) if res.ok else None})
        out.append(row)
    return out


def switch_text():
    out = []
    for value, expect in ((1.0, 'On'), (0.0, 'Off')):
        text = None
        for _ in range(5):          # the shared-empty-string init is ASLR-sensitive; retry
            res = R.run(['call', hex(EMPTY_STRING), 'call', hex(SWITCH_TEXT), 'buf:8', dbl(value),
                         'dump', 'b0*', '24'])
            if res.ok and res.dumps:
                raw = res.dumps[0][2]
                size = struct.unpack_from('<I', raw, 4)[0]
                text = raw[16:16 + size].decode('utf-16-le').rstrip('\0')
                break
        out.append({'value': value, 'expected': expect, 'text_x': text, 'agree': text == expect})
    return out


def main():
    results = {'fader': fader(), 'pan_law': pan_law(), 'crossfade': crossfade(),
               'switch_text': switch_text()}
    used = {}
    for _, res in R.log:
        for sym, n in res.used.items():
            used[sym] = used.get(sym, 0) + n
    results['replaced_imports_called'] = dict(sorted(used.items()))
    results['runs'] = {'count': len(R.log), 'not_ok': sum(not r.ok for _, r in R.log)}
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'mixer.json').write_text(json.dumps(results, indent=1) + '\n')
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for argv, res in R.log:
            f.write(json.dumps({'argv': argv, 'rc': res.rc, 'stdout': res.stdout,
                                'stderr': res.stderr, 'timeout': res.timeout}) + '\n')
    # console summary
    for r in results['fader']['position_to_gain']:
        print(f"p2g {r['curve']:6} pos {r['position']:<5} -> {r['gain_x']!r}")
    for r in results['fader']['gain_to_position']:
        print(f"g2p {r['curve']:6} gain {r['gain']:<22} -> {r['position_x']!r}")
    for r in results['fader']['roundtrip_Q019']:
        print(f"Q019 {r['curve']:6} {r['stored_gain']:<22} pos {r['position_x']!r} back {r['gain_back_x']!r} exact={r['exact_roundtrip']}")
    for r in results['pan_law']:
        print(f"pan {r['mode']:6} w{r['w']} pan{r.get('pan')} sL{r.get('splitL')} sR{r.get('splitR')} vol{r['vol']} -> {r['gains_LL_LR_RL_RR']}")
    for r in results['crossfade']:
        print(r['curve'], [(l['x'], round(l['level_x'], 6) if l['level_x'] is not None else None) for l in r['levels']])
    for r in results['switch_text']:
        print('switch', r['value'], '->', r['text_x'], 'agree', r['agree'])
    print('runs', results['runs'], 'replaced imports:', ', '.join(results['replaced_imports_called']))


if __name__ == '__main__':
    main()
