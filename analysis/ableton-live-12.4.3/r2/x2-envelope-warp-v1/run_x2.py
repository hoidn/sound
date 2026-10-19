"""X2 extracted execution: automation-envelope evaluation and warp-marker mapping (ADR 0003, label X).

usage: python3 -I -B run_x2.py          (from any directory; writes results/, raw/, addresses.json, imports.txt)

Runs self-contained x86_64 functions of the Live 12.4.3 x86_64 slice in the X2 loader copy (xexec2.c,
built to $X2_BIN). Every value below is what the original code computes for the given inputs with the
substitutions in tools/xexec/xexec.c plus this packet's additions (see xexec2.c "X2:" and the research
page). Slice results bind to the x86_64 slice; the research page records the static arm64 comparison.
No Live application was run and no document was loaded; object graphs are hand-built or come from the
slice's own constructors and static initialisers.
"""
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from seq import Seq, d2hex, BIN                                   # noqa: E402
import xexec                                                     # noqa: E402
from xexec import as_f32, as_f64                                 # noqa: E402

OPS = 0x107214bb8          # ARemoteableList item-ops table (AListAutomation.mpEvents)
NEW_LIST_AUTO = 0x102687490
NEW_REMOTE_LIST = 0x10155b600
LIST_FIELD = 0x1026881a0   # AListAutomation+0x238 getter? no: returns mpEvents (+0x58)
OPS_END = 0x101562130      # ARemoteableList end-iterator
OPS_INSERT = 0x101562160   # ARemoteableList SDefaultAddController wrapper
NEW_FLOAT_EVENT = 0x1028b13d0
NEW_BOOL_EVENT = 0x1028b0ae0
NEW_ENUM_EVENT = 0x1028b0f50
NEW_WARP_MARKER = 0x102737050
FLOAT_EVAL = 0x102526870   # TFloatAutomationInterpolator evaluator (arm 0x1024095b4)
DISCRETE_EVAL = 0x102527b40  # TDiscreteAutomationInterpolator (arm 0x10240a84c)
BUILD_RECORD = 0x1028b2020   # build transform record from a provider handle (arm 0x102778c98)
SB_CONV = 0x101b6fa60      # sample->beat core (arm 0x101b39e20)
BS_CONV = 0x101b6f970      # beat->sample core (arm 0x101b39d8c)
SHADOW_APPEND = 0x102738d90  # append shadow (arm 0x102612464)
BEAT_Q = 0x102736ce0       # BeatTime setter: rounds to the 1/3,843,840 grid (arm 0x1026101b4)
ADD_BOUNDS = 0x1028e96b0   # add_warp_marker beat bounds for a neighbour (5..999 BPM)
MONOTONE = 0x1011f2080     # cubic-Bezier monotonicity test (arm 0x1012132d8)
REG_CTOR = 0x101474e30     # AClassInfo registration
REGISTER_ALL = 0x101475670  # build the class graph from the registry vector
REG_HEAD, REG_CUR, REG_END = 0x1073e1158, 0x1073e1160, 0x1073e1168
ENVELOPE_ROOTS = [0x107529008, 0x1075332b8, 0x107533128, 0x1075331f0]
# AWarpMarker needs AAbstractWarpMarker then AWarpMarker registered (args read from the slice's initialiser).
WARP_REGS = [(0x10752d3e0, 0x10680f6e4, 0x13, 0x1074ed010, 0x106a360b0, 0x1027368f0),
             (0x10752d4a8, 0x10680f732, 0xb, 0x10752d3e0, 0x106a341c0, 0x1027370b0)]

RUNS = []       # (label, Seq) so run() output goes to raw/runs.jsonl


def warp_regs(s):
    for reg, name, n, base, fac, fn in WARP_REGS:
        s.call(REG_CTOR, f'i:{reg:#x}', f'i:{name:#x}', f'i:{n:#x}', f'i:{base:#x}', f'ref:{fac:#x}*',
               f'i:{fn:#x}', 's:0', 's:0', 's:0')


def registry_subset():
    s = Seq(); s.dump(hex(REG_HEAD), 16); s.dump(f'{REG_HEAD:#x}*', 8 * 2700)
    r = run('registry-dump', s)
    b, e = struct.unpack('<QQ', r.dumps[0][2]); n = (e - b) // 8
    regs = struct.unpack(f'<{n}Q', r.dumps[1][2][:8 * n])
    s = Seq()
    for a in regs:
        s.dump(hex(a), 0x20)
    r = run('registry-bases', s)
    base = {ad: struct.unpack_from('<Q', d, 0x18)[0] for _, ad, d in r.dumps}
    want = set()
    for a in ENVELOPE_ROOTS:
        while True:
            want.add(a)
            if base.get(a, a) in (a, 0):
                break
            a = base[a]
    return [a for a in regs if a in want]


SUB = None


def prologue(warp=False):
    s = Seq()
    if warp:
        warp_regs(s)
    vb = s.mkbuf(8 * len(SUB))
    for k, a in enumerate(SUB):
        s.poke('poke', f'b{vb}+{8 * k}', hex(a))
    s.poke('poke', hex(REG_HEAD), f'b{vb}')
    s.poke('poke', hex(REG_CUR), f'b{vb}+{8 * len(SUB)}')
    s.poke('poke', hex(REG_END), f'b{vb}+{8 * len(SUB)}')
    s.call(REGISTER_ALL)
    return s


def run(label, s):
    r = s.run()
    RUNS.append((label, s.tokens, r))
    return r


# ---------------------------------------------------------------- envelopes
def build_auto(s, events, kind='float'):
    """events: (time, value, [curve4]) ; kind float/bool/enum. Returns the automation buffer index."""
    ctor = {'float': NEW_FLOAT_EVENT, 'bool': NEW_BOOL_EVENT, 'enum': NEW_ENUM_EVENT}[kind]
    _, (ba,) = s.call(NEW_LIST_AUTO, 'buf:8')
    rl, _ = s.call(LIST_FIELD, f'ref:b{ba}*')
    rend, _ = s.call(OPS_END, f'i:{OPS:#x}', f'ref:r{rl}')
    for e in events:
        t, v = e[0], e[1]
        _, (be,) = s.call(ctor, 'buf:8')
        s.poke('poked', f'b{be}*+80', repr(float(t)))
        if kind == 'float':
            s.poke('pokef', f'b{be}*+88', repr(float(v)))
            if len(e) > 2:
                for off, c in zip((0x60, 0x68, 0x70, 0x78), e[2]):
                    s.poke('poked', f'b{be}*+{off}', repr(float(c)))
        else:
            s.poke('poke4', f'b{be}*+88', str(int(v)))
        bi = s.mkbuf(24)
        s.poke('poke', f'b{bi}', f'r{rend}'); s.poke('poke', f'b{bi}+8', f'r{rend}'); s.poke('poke', f'b{bi}+16', f'r{rl}')
        s.call(OPS_INSERT, f'i:{OPS:#x}', f'ref:r{rl}', f'ref:b{bi}', f'ref:b{be}*')
    return ba


def float_record(s, lo, hi, conv='0'):
    ph = s.mkbuf(24); s.poke('poke', f'b{ph}', conv)
    s.poke('pokef', f'b{ph}+8', repr(lo)); s.poke('pokef', f'b{ph}+12', repr(hi)); s.poke('poke4', f'b{ph}+16', '0')
    rec = s.mkbuf(0x48); s.call(BUILD_RECORD, f'ref:b{rec}', f'ref:b{ph}')
    return rec


def float_eval(label, events, times, lo=-1.0, hi=1.0, conv='0'):
    s = prologue(); ba = build_auto(s, events); rec = float_record(s, lo, hi, conv)
    outs = {}
    for t in times:
        _, made = s.call(FLOAT_EVAL, 'buf:40', 'hex:' + d2hex(t) + struct.pack('<Q', 0x7feffffffffffffe).hex(),
                         f'ref:b{ba}*', 'i:0', f'ref:b{rec}')
        outs[t] = made[0]
    r = run(label, s)
    res = {str(t): (struct.unpack('<f', r.outs[bo][:4])[0] if bo in r.outs else None) for t, bo in outs.items()}
    if not r.ok:
        res['run'] = r.fault or r.trap or f'rc={r.rc}'
    return res


def discrete_eval(label, events, times, kind='bool', modes=(0, 1)):
    s = prologue(); ba = build_auto(s, events, kind)
    outs = {}
    for t in times:
        for mode in modes:
            c, _ = s.call(DISCRETE_EVAL, 'i:0', 'hex:' + d2hex(t), f'ref:b{ba}*', f'i:{mode}')
            outs[(t, mode)] = c
    r = run(label, s)
    res = {f'{t}@mode{m}': (as_f32(r.calls[c]['xmm0']) if c < len(r.calls) else None) for (t, m), c in outs.items()}
    if not r.ok:
        res['run'] = r.fault or r.trap or f'rc={r.rc}'
    return res


# ------------------------------------------------------------------- warp
def warp_table(s, markers):
    n = len(markers)
    tb = s.mkbuf(0x20); ab = s.mkbuf(8 * n); asec = s.mkbuf(8 * n)
    for k, (sec, beat) in enumerate(markers):
        s.poke('poked', f'b{ab}+{8 * k}', repr(beat)); s.poke('poked', f'b{asec}+{8 * k}', repr(sec))
    s.poke('poke', f'b{tb}', f'b{ab}'); s.poke('poke4', f'b{tb}+8', str(n))
    s.poke('poke', f'b{tb}+16', f'b{asec}'); s.poke('poke4', f'b{tb}+24', str(n))
    return tb


def warp_convert(label, markers, s2b, b2s, rate=48000.0):
    s = Seq(init=False); tb = warp_table(s, markers)
    sb, bs = {}, {}
    for t in s2b:
        c, _ = s.call(SB_CONV, f'd:{float(t) / rate!r}', f'ref:b{tb}'); sb[t] = c
    for b in b2s:
        c, _ = s.call(BS_CONV, f'd:{float(b)!r}', f'ref:b{tb}'); bs[b] = c
    r = run(label, s)
    out = {'sample_to_beat': {str(t): as_f64(r.calls[c]['xmm0']) for t, c in sb.items()},
           'beat_to_sample': {str(b): as_f64(r.calls[c]['xmm0']) * rate for b, c in bs.items()}}
    return out


def warp_edges():
    out = {}
    # q(): the beat-grid rounding of REQ-016, run on a real AWarpMarker
    import math
    s = prologue(warp=True); _, (bm,) = s.call(NEW_WARP_MARKER, 'buf:8')
    tie = (7687680 + 0.5) / 3843840                     # binary64 nearest to beat 2 + half a grid step
    ntie = -tie
    beats = [2.0000001, 2.001, -0.0, 1e13, float('nan'), float('inf'), -float('inf'),
             1.7976931348623155e308, -1.7976931348623155e308, 1.7976931348623157e308,
             2.0416666666666665, 10.325, 10.325 + 1 / 3843840,
             tie, math.nextafter(tie, 0), math.nextafter(tie, 3), ntie, math.nextafter(ntie, 0)]
    marks = []
    for b in beats:
        s.call(BEAT_Q, f'd:{b!r}', f'ref:b{bm}*'); s.dump(f'b{bm}*+88', 8); marks.append(b)
    r = run('beat-grid-q', s)
    out['beat_grid_round'] = {repr(b): as_f64(int.from_bytes(d[2], 'little')) for b, d in zip(marks, r.dumps)}
    # add bounds: neighbour (sec, beat) and new marker sec -> [bn + ds*5/60, bn + ds*999/60], ordered;
    # the getters read only +0x50 (SecTime) and +0x58 (BeatTime), so plain records stand in for markers
    s = Seq(init=False)
    bounds = {}
    for name, (ns, nbt, ws) in {'p1.5_nb(1,2)': (1.0, 2.0, 1.5), 'p1_nb(1,2)_ds0': (1.0, 2.0, 1.0),
                                'p1.0004_nb(1,2)': (1.0, 2.0, 1.0004),
                                'p1.5_right_nb(2,3)': (2.0, 3.0, 1.5)}.items():
        nb = s.mkbuf(0x60); nw = s.mkbuf(0x60)
        s.poke('poked', f'b{nb}+80', repr(ns)); s.poke('poked', f'b{nb}+88', repr(nbt))
        s.poke('poked', f'b{nw}+80', repr(ws))
        c, _ = s.call(ADD_BOUNDS, f'ref:b{nw}', f'ref:b{nb}'); bounds[name] = c
    cb = bounds['p1.5_nb(1,2)']
    mono = {}
    for name, (c1, c2) in {'linear.5.5': (0.5, 0.5), 'ordered.2.8': (0.2, 0.8),
                           'nonmono1.5': (1.5, -0.5), 'swapped.8.2': (0.8, 0.2)}.items():
        c, _ = s.call(MONOTONE, 'd:0', f'd:{c1!r}', f'd:{c2!r}', 'd:1'); mono[name] = c
    r = run('add-bounds-monotone', s)
    out['add_bounds_lo_hi'] = {k: [as_f64(r.calls[c]['xmm0']), as_f64(r.calls[c]['xmm1'])] for k, c in bounds.items()}
    out['monotone'] = {k: (r.calls[c]['rax'] & 1) for k, c in mono.items()}
    return out


def pan_converter_identity():
    """A1 evidence: the Pan ALinearUserFloatConverter slot +0x28 (value->user) on its own [-1,1] range."""
    s = Seq(init=False); cv = s.mkbuf(0x38)
    s.call(0x1015663a0, 'f:-1.0', 'f:1.0', 'f:0.0158730168', 'f:0.00999999978', f'ref:b{cv}')
    outs = {}
    for v in [-1.0, -0.5, 0.0, 0.33, 0.5, 1.0]:
        c, _ = s.call(0x1015664f0, f'f:{v!r}', 'f:-1.0', 'f:1.0', f'ref:b{cv}'); outs[v] = c
    r = run('pan-converter', s)
    return {str(v): as_f32(r.calls[c]['xmm0']) for v, c in outs.items()}


def warp_shadow(visible=((0.0, 0.0), (1.0, 2.0), (2.0, 3.0)), p1=120.0, p2=1.0, label='shadow-append'):
    """REQ-007 shadow append: from visible markers (0,0),(1,2),(2,3) the appended marker is
    sec = last.sec + (p2*60/p1)*(1/32), beat = q(last.beat + 1/32). Called as the clip's recompute does,
    with p1 the song tempo and p2 the local tempo factor (both 120/1 here, giving the shipped M1 shadow)."""
    s = prologue(warp=True)
    _, (bl,) = s.call(NEW_REMOTE_LIST, 'buf:8'); rend, _ = s.call(OPS_END, f'i:{OPS:#x}', f'ref:b{bl}*')
    for sec, beat in visible:
        _, (bm,) = s.call(NEW_WARP_MARKER, 'buf:8')
        s.poke('poked', f'b{bm}*+80', repr(sec)); s.poke('poked', f'b{bm}*+88', repr(beat))
        bi = s.mkbuf(24)
        s.poke('poke', f'b{bi}', f'r{rend}'); s.poke('poke', f'b{bi}+8', f'r{rend}'); s.poke('poke', f'b{bi}+16', f'b{bl}*')
        s.call(OPS_INSERT, f'i:{OPS:#x}', f'ref:b{bl}*', f'ref:b{bi}', f'ref:b{bm}*')
    s.call(SHADOW_APPEND, f'd:{p1!r}', f'd:{p2!r}', f'ref:b{bl}*')
    # every node from the sentinel's next (+0x18) on: node+0x30 is the item handle, handle+8 the marker
    nxt = f'r{rend}+24*'
    for k in range(len(visible) + 1):
        s.dump(nxt + '+56*+80', 8); s.dump(nxt + '+56*+88', 8)
        nxt += '+24*'
    r = run(label, s)
    return {'formula': 'SecTime = last.SecTime + (p2*60/p1)*(1/32); BeatTime = q(last.BeatTime + 1/32), '
            'q the REQ-016 grid rounding. For visible markers (0,0),(1,2),(2,3) with p1=120, p2=1 this '
            'gives the shipped M1 shadow (2.015625, 3.03125). x86 FUN_102738d90 and arm64 FUN_102612464 '
            'use byte-identical constants (1/32, 60, 3843840); list_after_append is read back from the x86 run.',
            'append_ran_clean_on_x86': r.ok,
            'list_after_append_sec_beat': [[as_f64(int.from_bytes(r.dumps[2 * k][2], 'little')),
                                            as_f64(int.from_bytes(r.dumps[2 * k + 1][2], 'little'))]
                                           for k in range(len(r.dumps) // 2)]}


def main():
    global SUB
    SUB = registry_subset()
    results = {
        'note': 'E(t) values are the x86_64 Float/Discrete interpolator output; the automation transform '
                'record is built full-range with a null converter (the automation path, see research A1). '
                'Times t in beats; values at 32-bit precision unless noted.',
        'float_AEN015_016_hold_event_linear_equal': float_eval(
            'E1', [(-63072000.0, 0.0), (4.0, 0.0), (8.0, 1.0)], [0.0, 2.0, 4.0, 5.0, 6.0, 7.0, 12.0, 100.0]),
        'float_AEN017_equal_then_linear': float_eval(
            'E12', [(-63072000.0, 0.0), (0.0, 0.0), (3.0, 1.0)], [1.0]),
        'float_AEN019_020_step': float_eval(
            'E8', [(-63072000.0, 1.0), (4.0, 1.0), (4.0, -1.0), (8.0, -1.0)], [2.0, 6.0, 10.0]),
        'float_AEN018_ramp_from_L': float_eval(
            'E13', [(-63072000.0, 1.0), (4.0, 0.0)], [0.0, 4.0]),
        'float_AEN021_022_curve': float_eval(
            'E9', [(-63072000.0, -1.0), (0.0, -1.0, (0.5, 0.0, 0.5, 0.0)), (4.0, 1.0)],
            [0.0, 1.0, 2.0, 3.0, 4.0, 6.0]),
        'float_step_modes_E8_t4': float_eval_modes(),
        'float_before_first_event_E4_t-1': float_eval(
            'E4-before-first', [(0.0, 0.0), (4.0, 1.0)], [-1.0]),
        'bool_before_first_event_t-1_mode0': discrete_eval(
            'bool-before-first-m0', [(0.0, 1), (4.0, 0)], [-1.0], 'bool', (0,)),
        'bool_before_first_event_t-1_mode1': discrete_eval(
            'bool-before-first-m1', [(0.0, 1), (4.0, 0)], [-1.0], 'bool', (1,)),
        'bool_AEN023_024': discrete_eval('E14', [(-63072000.0, 1), (4.0, 0), (8.0, 1)],
                                         [0.0, 2.0, 4.0, 6.0, 8.0, 10.0], 'bool'),
        'enum_AEN025': discrete_eval('E15', [(-63072000.0, 1), (4.0, 0), (8.0, 2)],
                                     [2.0, 4.0, 6.0, 8.0, 12.0], 'enum'),
        'A1_pan_converter_slot0x28_on_range': pan_converter_identity(),
        'warp_WMK016_M1': warp_convert('M1', [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (2.015625, 3.03125)],
                                       [-24000, 24000, 48000, 72000, 96000, 120000, 2400000], [0.5, 2.5, 4.0]),
        'warp_WMK017_M2': warp_convert('M2', [(0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (2.015625, 3.03125)],
                                       [0, 12000], []),
        'warp_edges_REQ015_016': warp_edges(),
        'warp_REQ007_shadow_append': warp_shadow(),
        'warp_REQ007_shadow_M0_167bpm': warp_shadow(((0.0, 0.0),), 167.0, 1.0, 'shadow-M0'),
        'warp_REQ007_shadow_offgrid_last': warp_shadow(((0.0, 0.0), (1.0, 2.0000001)), 120.0, 1.0,
                                                       'shadow-offgrid'),
    }
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'envelope-warp.json').write_text(json.dumps(results, indent=1, default=str) + '\n')
    (HERE / 'raw').mkdir(exist_ok=True)
    with open(HERE / 'raw' / 'runs.jsonl', 'w') as f:
        for label, tokens, r in RUNS:
            f.write(json.dumps({'label': label, 'argv': tokens, 'rc': r.rc, 'stdout': r.stdout,
                                'stderr': r.stderr, 'timeout': r.timeout}) + '\n')
    used = {}
    for _, _, r in RUNS:
        for sym, n in r.used.items():
            used[sym] = used.get(sym, 0) + n
    (HERE / 'imports.txt').write_text('\n'.join(f'{k} {v}' for k, v in sorted(used.items())) + '\n')
    print(json.dumps(results, indent=1, default=str))


def float_eval_modes():
    """E8 at the step t=4 under both consumer modes, read from the discrete-search mode used by the
    Float evaluator's left/right choice. The Float evaluator FLOAT_EVAL takes the mode as its 4th int arg."""
    s = prologue(); ba = build_auto(s, [(-63072000.0, 1.0), (4.0, 1.0), (4.0, -1.0), (8.0, -1.0)])
    rec = float_record(s, -1.0, 1.0)
    outs = {}
    for mode in (0, 1):
        _, made = s.call(FLOAT_EVAL, 'buf:40', 'hex:' + d2hex(4.0) + struct.pack('<Q', 0x7feffffffffffffe).hex(),
                         f'ref:b{ba}*', f'i:{mode}', f'ref:b{rec}')
        outs[mode] = made[0]
    r = run('E8-step-modes', s)
    return {f'mode{m}': (struct.unpack('<f', r.outs[bo][:4])[0] if bo in r.outs else None) for m, bo in outs.items()}


if __name__ == '__main__':
    main()
