"""Behavior checks on the Tension x86_64 slice that need extra renders (not retained):
determinism, event timing, controller quantization, pitch, level, polyphony and edge cases.

    python3 -I checks_tension.py > results/checks.txt      # also writes results/checks.json

Renders go to /var/tmp/sound-analysis/t12-tension/checks (eight loader processes at a time). Every
comparison is stated with its rule in the JSON. Dependencies: numpy, scipy, run_tension.py renders.
"""
import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import cases  # noqa: E402
import measure as M  # noqa: E402
import tension as T  # noqa: E402
import xdevpy  # noqa: E402
from run_tension import load  # noqa: E402

TMP = Path('/var/tmp/sound-analysis/t12-tension/checks')
_n = [0]


def R(lines, env=None):
    """Render a script in a fresh process; returns (frames, 2) float32."""
    _n[0] += 1
    path = TMP / f'c{_n[0]:05d}_{hashlib.sha1(chr(0).join(lines).encode() + repr(env).encode()).hexdigest()[:10]}.f32'
    return T.render(lines, path, env=env)[0]


def many(jobs):
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(lambda j: R(*j) if isinstance(j, tuple) else R(j), jobs))


def same(a, b):
    return bool(np.array_equal(np.asarray(a).view(np.uint32), np.asarray(b).view(np.uint32)))


def maxdiff(a, b):
    return float(np.abs(np.asarray(a, float) - np.asarray(b, float)).max())


H0 = T.host_values()
NOTE = T.note(60, 100, 4096, 22050)


def determinism():
    ref = load('defaults_44')
    s = lambda **kw: T.script(H0, NOTE, frames=44100, **kw)   # noqa: E731
    jobs = {'rerun': (s(),), 'block_64': (s(block=64),), 'block_256': (s(block=256),), 'block_333': (s(block=333),),
            'ftz_daz_0x9fc0': (s(mxcsr=0x9fc0),), 'clock_1760000000': (s(), {'XDEV_TIME': '1760000000'}),
            'clock_12345': (s(), {'XDEV_TIME': '12345'})}
    ys = dict(zip(jobs, many(list(jobs.values()))))
    out = {k: dict(bit_identical=same(y[:, 0], ref[:, 0].astype(np.float32)), max_abs_diff=maxdiff(y[:, 0], ref[:, 0]))
           for k, y in ys.items()}
    # seed dependence of the random features: same settings, clock 0 against 1760000000
    for tag, ch in (('KeyboardError_1', {'KeyboardError': 1}), ('Vibrato_on_error_0.5', {'VibratoToggle': 1}),
                    ('Vibrato_on_error_0', {'VibratoToggle': 1, 'VibratoError': 0}),
                    ('LFO_shapes_0_to_4_filter', None), ('Unison_on', {'KeyboardUnisonToggle': 1, 'KeyboardUnison': 1})):
        sets = [ch] if ch is not None else [{'LFOToggle': 1, 'LFOWaveShape': w, 'FilterToggle': 1, 'FilterCutoffFrequencyLFOMod': 0.5}
                                            for w in range(5)]
        dep = []
        for c in sets:
            h = T.host_values(c)
            a, b = many([(T.script(h, NOTE, frames=44100),), (T.script(h, NOTE, frames=44100), {'XDEV_TIME': '1760000000'})])
            dep.append(maxdiff(a, b))
        out[f'seed_dependence_{tag}'] = dict(max_abs_diff=dep, seed_dependent=[d > 0 for d in dep])
    # rate change and reset sequence
    r48 = load('defaults_48')
    c48 = cases.CASES['defaults_48']
    y = R(T.script(H0, c48['events'], fs=44100, frames=48000, post=['rate 48000']))
    out['rate_44100_then_48000_vs_defaults_48'] = dict(bit_identical=same(y[:, 0], r48[:, 0].astype(np.float32)), max_abs_diff=maxdiff(y[:, 0], r48[:, 0]),
                                                      rel_rms=M.rel_rms(y[:, 0].astype(float), r48[:, 0]))
    y = R(T.script(H0, NOTE, frames=44100, post=['inflag 0', 'input zero', 'process 1024 512', 'reset', f'param 0 {H0[0]!r}']))[1024:]
    out['reset_sequence_before_note'] = dict(bit_identical=same(y[:, 0], ref[:, 0].astype(np.float32)), max_abs_diff=maxdiff(y[:, 0], ref[:, 0]))
    y = R(T.script(H0, NOTE, frames=44100, post=['inflag 0', 'input zero', 'process 1024 512', 'reset']))[1024:]
    out['reset_without_index0_resend'] = dict(bit_identical=same(y[:, 0], ref[:, 0].astype(np.float32)), max_abs_diff=maxdiff(y[:, 0], ref[:, 0]))
    y = R(T.script(H0, [], frames=44100))
    out['no_events_output_all_zero'] = bool(not np.any(y))
    y = R(T.script(T.host_values({'ExcitatorToggle': 0}), NOTE, frames=44100))
    out['ExcitatorToggle_off_output_all_zero'] = bool(not np.any(y))
    y = R(T.script(T.host_values({'ExcitatorVelocityVelMod': 1}), T.note(60, 127, 4096, 22050), frames=44100))
    out['VelMod_1_velocity_127_output_all_zero'] = bool(not np.any(y))
    y = R(T.script(T.host_values({'BodyToggle': 1, 'BodyMix': 0}), NOTE, frames=44100))
    out['Body_on_mix_0_equals_body_off'] = same(y[:, 0], ref[:, 0].astype(np.float32))
    return out


def grid_rule(f, block, period):
    """Frame after the start of the control period (period = fs // 1000 frames) containing f; if that
    period began in an earlier host block, the frame after the start of the next period (Analog's rule)."""
    g = period * (f // period)
    return (g if g >= block * (f // block) else g + period) + 1


def timing():
    out = {}
    for label, fs, block in (('on_44_b512', 44100, 512), ('on_44_b64', 44100, 64), ('on_44_b333', 44100, 333), ('on_48_b512', 48000, 512)):
        frames = list(range(1000, 1200, 2)) + list(range(3060, 3100, 1))
        ys = many([T.script(H0, [(f, 0x90, 60, 100)], fs=fs, block=block, frames=4096) for f in frames])
        rows = [dict(event=f, first_nonzero=M.onset(y[:, 0]), effective=grid_rule(f, block, fs // 1000) - 1) for f, y in zip(frames, ys)]
        offs = sorted({r['first_nonzero'] - r['effective'] for r in rows})
        # an event renders bit-identically to an event placed at its effective frame
        eff = [r['effective'] for r in rows[::7]]
        ye = many([T.script(H0, [(e, 0x90, 60, 100)], fs=fs, block=block, frames=4096) for e in eff])
        ident = all(same(a[:, 0], b[:, 0]) for a, b in zip(ys[::7], ye))
        out[label] = dict(fs=fs, block=block, period=fs // 1000, onset_minus_effective=offs, shifted_identical=ident, n=len(rows))
    frames = list(range(4000, 4200, 2))
    for label, fs, ch in (('off_44_b512', 44100, {}), ('off_48_b512', 48000, {}), ('off_44_b512_hammer', 44100, {'ExcitatorType': 1}),
                          ('off_44_b512_bow', 44100, {'ExcitatorType': 0}),
                          ('off_44_b512_damper_gated', 44100, {'DamperToggle': 1, 'DamperGated': 1})):
        h = T.host_values(ch)
        held = R(T.script(h, [(1024, 0x90, 60, 100)], fs=fs, frames=8192))
        ys = many([T.script(h, [(1024, 0x90, 60, 100), (f, 0x80, 60, 0)], fs=fs, frames=8192) for f in frames])
        diffs = [M.onset(y[:, 0].astype(float) - held[:, 0].astype(float)) for y in ys]
        out[label] = dict(rule='first frame that differs from the held note = effective frame + d', changes=ch, fs=fs,
                          d=sorted({d - (grid_rule(f, 512, fs // 1000) - 1) for f, d in zip(frames, diffs)}), n=len(frames))
    ys = many([T.script(H0, [(1024, 0x90, 60, 100), (f, 0x90, 60, 0)], frames=8192) for f in frames[:10]])
    out['note_on_velocity_0_acts_as_note_off'] = all(same(a, b) for a, b in zip(ys, ys and many(
        [T.script(H0, [(1024, 0x90, 60, 100), (f, 0x80, 60, 0)], frames=8192) for f in frames[:10]])))
    # excitator travel: first non-zero frame after the effective frame, per excitator type and velocity
    trav = {}
    for et in range(4):
        for vel in (1, 64, 127):
            y = R(T.script(T.host_values({'ExcitatorType': et}), [(1056, 0x90, 60, vel)], frames=4096))
            trav[f'type{et}_vel{vel}'] = M.onset(y[:, 0]) - 1056
    out['onset_delay_frames_after_grid_point_1056'] = trav
    return out


def quantization():
    """Host value classes per index: 'stepped' if 0.25 and 0.253 render identically but 0.25 - 1e-6 differs
    (128 controller steps, c = 128v or 126v + 1), 'continuous' if 0.25 and 0.253 differ, 'none' if no change
    was seen in this context. Context: every section switched on, note 72 velocity 90."""
    base = T.host_values({'DamperToggle': 1, 'TerminationToggle': 1, 'PickupToggle': 1, 'BodyToggle': 1, 'FilterToggle': 1,
                          'FilterEnvelopeToggle': 1, 'LFOToggle': 1, 'VibratoToggle': 1, 'VibratoError': 0, 'PortamentoToggle': 1})
    ev = [(1024, 0x90, 72, 90), (7000, 0x80, 72, 0)]
    idx = [r['index'] for r in json.load(open(HERE.parent / 'h4-devices-v1' / 'out' / 'param_tables.json'))['Tension']['rows']
           if r['kind'] == 0]
    jobs = []
    for i in idx:
        for v in (0.25, 0.253, float(np.nextafter(np.float32(0.25), np.float32(0)))):
            h = dict(base); h[i] = v
            jobs.append(T.script(h, ev, frames=12000))
    ys = many(jobs)
    out = {}
    for n, i in enumerate(idx):
        a, b, c = ys[3 * n: 3 * n + 3]
        out[str(i)] = 'continuous' if not same(a, b) else 'stepped' if not same(a, c) else 'none'
    # step boundaries for one stepped index (48, ExcitatorVelocity): boundaries at k/128 below 0.5, (k - 1)/126 above
    pts = [float(np.float32(p)) for p in (0.0078125, 0.5, 64 / 126, 65 / 126, 1.0)]
    eps = [float(np.nextafter(np.float32(p), np.float32(-1))) for p in pts]
    ys = many([T.script({**H0, 48: v}, NOTE, frames=8192) for p in zip(pts, eps) for v in p])
    out['boundaries_index48'] = {f'{p:.7f}': not same(ys[2 * k], ys[2 * k + 1]) for k, p in enumerate(pts)}
    # position parameters: distinct outputs over the 129 host values k/128, damper and pickup on
    hp = T.host_values({'DamperToggle': 1, 'PickupToggle': 1})
    for i, name in ((24, 'GeoExcitatorPosition'), (30, 'GeoDamperPosition'), (55, 'PickupPosition')):
        for n in (36, 60):
            ys = many([T.script({**hp, i: k / 128}, T.note(n, 100, 1024, 3000), frames=8192) for k in range(129)])
            changes = [k for k in range(1, 129) if not same(ys[k], ys[k - 1])]
            out[f'positions_{name}_note_{n}'] = dict(distinct=len({y.tobytes() for y in ys}), changes_at_k_over_128=changes)
    return out


C4 = 440 * 2 ** (-9 / 12)


def f1(y, fexp, fs=44100, on=4096):
    m = M.modes(y[:, 0].astype(float), fexp, (M.onset(y[:, 0]) or on) + 1500, len(y), fs, K=2)
    return m['partials'][0]['hz'] if m['partials'] else None


def pitch():
    jobs, exp = [], []
    def add(tag, ch, n=60, pre_ev=(), fe=None):   # noqa: E306
        ev = list(pre_ev) + T.note(n, 100, 4096, 0)
        jobs.append(T.script(T.host_values(ch), ev, frames=40000))
        exp.append((tag, fe or 440 * 2 ** ((n - 69) / 12)))
    for n in range(24, 109, 12):
        add(f'note_{n}', {}, n)
    add('Octave_+1', {'Octave': 1}, fe=2 * C4); add('Octave_-1', {'Octave': -1}, fe=C4 / 2)
    add('Octave_+3', {'Octave': 3}, fe=8 * C4); add('Octave_-3', {'Octave': -3}, fe=C4 / 8)
    add('Transpose_+7', {'Transpose': 7}, fe=C4 * 2 ** (7 / 12)); add('Transpose_-12', {'Transpose': -12}, fe=C4 / 2)
    for v in (0, 0.25, 0.75, 1):
        add(f'FineTune_{v}', {'KeyboardFineTune': v}, fe=C4 * 2 ** ((v - 0.5) * 100 / 1200))
    for n in (36, 60, 84):
        for v in (0, 0.25, 1):
            add(f'Stretch_{v}_note_{n}', {'KeyboardStretch': v}, n)
    for pb in (0x0000, 0x1000, 0x3000, 0x3fff):
        add(f'bend_{pb:#06x}_range_2', {}, pre_ev=[(100, 0xE0, pb & 0x7f, pb >> 7)], fe=C4 * 2 ** (2 * (pb - 8192) / 8192 / 12))
    add('bend_0x3fff_range_12', {'PitchBendRange': 12}, pre_ev=[(100, 0xE0, 0x7f, 0x7f)], fe=C4 * 2 ** (12 * 8191 / 8192 / 12))
    add('KeyboardError_1_seed0', {'KeyboardError': 1})
    ys = many(jobs)
    out = {}
    for (tag, fe), y in zip(exp, ys):
        f = f1(y, fe)
        out[tag] = dict(expected_equal_tempered_hz=fe, measured_hz=f, cents=float(1200 * np.log2(f / fe)) if f else None)
    c48 = cases.CASES['defaults_48']
    y = load('defaults_48')
    out['note_60_48k'] = dict(expected_equal_tempered_hz=C4, measured_hz=f1(y, C4, 48000), cents=float(1200 * np.log2(f1(y, C4, 48000) / C4)))
    return out


def level():
    ref = load('defaults_44')[:, 0]
    vals = [0, 1 / 128, 0.1, 0.25, 0.5, 0.6, 0.705, 0.75, 0.9, 1.0]
    ys = many([T.script(T.host_values({'BodyLevel': v}), NOTE, frames=44100) for v in vals])
    m = np.abs(ref) > 1e-3
    def n_of(v):   # noqa: E306
        c = 128 * v if v <= 0.5 else 126 * v + 1
        return 0.5 if c == 64 else c / 127
    out = {}
    for v, y in zip(vals, ys):
        r = y[:, 0].astype(float)[m] / ref[m]
        pred = (n_of(v) / n_of(0.705)) ** 2
        out[f'{v:g}'] = dict(gain_vs_default=float(r.mean()), spread=float(r.std()), predicted_n_squared=pred,
                             rel_error=float(r.mean() / pred - 1) if pred else float(r.mean()))
    return out


def polyphony():
    ch0 = {'StringDecay': 1, 'StringDecayRatio': 0}
    f24 = 440 * 2 ** ((24 - 69) / 12)
    def lvl(x, a, b):   # noqa: E306
        t = np.arange(a, b); w = np.hanning(b - a)
        return abs((x[a:b] * w * np.exp(-2j * np.pi * f24 * t / 44100)).sum())
    def survives(poly, others, same_note=False):   # noqa: E306
        ev = [(4096, 0x90, 24, 100)] + [(4096 + 441 * (i + 1), 0x90, 72 if same_note else 72 + i, 100) for i in range(others)]
        end = 4096 + 441 * (others + 1) + 441
        h = T.host_values({**ch0, 'Polyphony': poly})
        y, ys = many([T.script(h, ev, frames=end + 8820), T.script(h, ev[:1], frames=end + 8820)])
        return lvl(y[:, 0].astype(float), end, end + 8820) / lvl(ys[:, 0].astype(float), end, end + 8820)
    voices = {}
    for poly in range(10):
        r = [survives(poly, k) for k in range(0, 34)]
        voices[str(poly)] = next((k for k, v in enumerate(r) if v < 0.5), None)
    same_note = {str(k): survives(2, k, True) for k in (3, 4, 8)}
    # how a stolen voice ends: C1 alone vs C1 stolen by the second note (polyphony stored 0, one voice)
    h = T.host_values({**ch0, 'Polyphony': 0})
    a, b = many([T.script(h, [(4096, 0x90, 24, 100)], frames=20000),
                 T.script(h, [(4096, 0x90, 24, 100), (8800, 0x90, 96, 100)], frames=20000)])
    d = b[:, 0].astype(float) - a[:, 0].astype(float)
    return dict(voices_by_stored_value=voices, rule='first note silent once that many later notes have started',
                repeated_same_note_c1_level_ratio=same_note,
                mono_steal_first_changed_frame=M.onset(d))


def filter_linearity():
    """Filter response (filtered / unfiltered, measure.transfer, partials within 40 dB of the strongest) of the
    bright C2 string at ExcitatorVelocity 0.5 (the filt_* cases) against 0.25 and 0.4 (22 and 8 dB quieter)."""
    ev = T.note(36, 100, 4096, 22050)
    def H(ch, filt):   # noqa: E306
        a, b = many([T.script(T.host_values({**cases.BRIGHT, **ch}), ev, frames=44100),
                     T.script(T.host_values({**cases.BRIGHT, **ch, 'FilterToggle': 1, **filt}), ev, frames=44100)])
        return M.transfer(b[:, 0].astype(float), a[:, 0].astype(float), 6000, 26146, 44100, floor_db=-40)
    out = {}
    for tag, filt in (('type1_q0', {'FilterType': 1}), ('type1_q0.5', {'FilterType': 1, 'FilterQFactor': 0.5}), ('type8', {'FilterType': 8})):
        f0, h0 = H({}, filt)
        for v in (0.25, 0.4):
            f, h = H({'ExcitatorVelocity': v}, filt)
            d, p = [], []
            for q, x in zip(f, h):
                j = int(np.argmin(abs(f0 - q)))
                if abs(f0[j] - q) < 1:
                    d.append(abs(20 * np.log10(abs(x) / abs(h0[j])))); p.append(abs(np.angle(x / h0[j])))
            out[f'{tag}_vel{v}'] = dict(partials=len(d), max_gain_diff_db=max(d), max_phase_diff_rad=max(p))
    return out


def extremes():
    """Peak and all-zero flag of settings at the ends of their ranges (C4, velocity 100 unless stated)."""
    sets = {'hammer_velocity_0': ({'ExcitatorType': 1, 'ExcitatorVelocity': 0}, 100), 'hammer_velocity_1': ({'ExcitatorType': 1, 'ExcitatorVelocity': 1}, 100),
            'plectrum_damping_1': ({'ExcitatorDamping': 1}, 100), 'plectrum_velocity_1': ({'ExcitatorVelocity': 1}, 100),
            'bow_x_0.25': ({'ExcitatorType': 0, 'ExcitatorParameterX': 0.25}, 100), 'bow_velocity_1': ({'ExcitatorType': 0, 'ExcitatorVelocity': 1}, 100),
            **{f'velmod_1_velocity_{v}': ({'ExcitatorVelocityVelMod': 1}, v) for v in (32, 64, 100, 127)}}
    ys = many([T.script(T.host_values(ch), T.note(60, v, 4096, 22050), frames=44100) for ch, v in sets.values()])
    return {k: dict(peak=float(np.abs(y).max()), all_zero=bool(not np.any(y))) for k, y in zip(sets, ys)}


def string_curves():
    """First-partial T60 while held against StringDecay; release T60 against StringDecayRatio; key amounts at notes 36, 60, 84."""
    out = {}
    def t60(y, n, a, b):   # noqa: E306
        m = M.modes(y[:, 0].astype(float), 440 * 2 ** ((n - 69) / 12), a, b, 44100, K=2)
        return m['partials'][0]['t60_s'] if m['partials'] and m['partials'][0]['k'] == 1 else None
    vals = [0.25, 0.5, 0.75, 1.0]
    ys = many([T.script(T.host_values({'StringDecay': v}), T.note(60, 100, 4096, 0), frames=60000) for v in vals])
    out['decay_held_t60_s'] = {f'{v:g}': t60(y, 60, 6144, 60000) for v, y in zip(vals, ys)}
    vals = [0, 0.25, 0.5, 0.75]
    ys = many([T.script(T.host_values({'StringDecayRatio': v}), NOTE, frames=60000) for v in vals])
    out['ratio_release_t60_s'] = {f'{v:g}': t60(y, 60, 26146 + 882, 60000) for v, y in zip(vals, ys)}
    km = {}
    for n in (36, 60, 84):
        for ch in ({}, {'StringDecayKbdMod': 1}, {'StringDecayKbdMod': -1}, {'StringDampingKbdMod': 1}):
            y = R(T.script(T.host_values(ch), T.note(n, 100, 4096, 0), frames=40000))
            km[f'{n}_{json.dumps(ch)}'] = y
    out['key_amounts'] = {k: dict(identical_to_no_amount=same(y, km[k.split('_')[0] + '_{}']),
                                  t60_k1_s=t60(y, int(k.split('_')[0]), 5600, 40000)) for k, y in km.items()}
    return out


def filter_maps():
    """Type 1: -3 dB frequency (log interpolation between harmonics) against cutoff at Q 0; peak against cutoff at Q 1;
    peak against Q at cutoff 0.5. Responses as measure.transfer of the bright C2 string (filt_base)."""
    ev = T.note(36, 100, 4096, 22050)
    base = R(T.script(T.host_values(cases.BRIGHT), ev, frames=44100))[:, 0].astype(float)
    def resp(ch):   # noqa: E306
        return R(T.script(T.host_values({**cases.BRIGHT, 'FilterToggle': 1, 'FilterType': 1, **ch}), ev, frames=44100))[:, 0].astype(float)
    def H(y):   # noqa: E306
        f, h = M.transfer(y, base, 6194, 26146, 44100)
        return f, 20 * np.log10(np.abs(h))
    def cross(f, g, lvl):   # noqa: E306
        i = np.nonzero(g < lvl)[0]
        if not len(i) or i[0] == 0:
            return None
        j = i[0]; t = (lvl - g[j - 1]) / (g[j] - g[j - 1])
        return float(np.exp(np.log(f[j - 1]) + t * (np.log(f[j]) - np.log(f[j - 1]))))
    out = {'minus3db_hz_q0': {}, 'peak_q1': {}, 'peak_cutoff0.5': {}}
    for v in (0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0):
        f, g = H(resp({'FilterCutoffFrequency': v}))
        out['minus3db_hz_q0'][f'{v:g}'] = dict(hz=cross(f, g, -3), gain_at_65hz_db=float(g[0]))
        f, g = H(resp({'FilterCutoffFrequency': v, 'FilterQFactor': 1}))
        out['peak_q1'][f'{v:g}'] = dict(hz=float(f[np.argmax(g)]), db=float(g.max()))
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        f, g = H(resp({'FilterQFactor': q}))
        out['peak_cutoff0.5'][f'{q:g}'] = dict(hz=float(f[np.argmax(g)]), db=float(g.max()))
    return out


def corpus_crosscheck():
    """This loader on three retained t12 Corpus scripts: bit-identity with t12's raw renders, and the revised
    libm perturbation against t12's libm_sensitivity window figure (rel RMS from frame 4096)."""
    t12 = HERE.parent / 't12-device-dsp-v1'
    sens = json.loads((t12 / 'results' / 'libm_sensitivity.json').read_text())
    out = {}
    for name in ('pitch_0.25', 'defaults_44', 'mode_string_44'):
        lines = (t12 / 'raw' / 'corpus' / f'{name}.script').read_text().splitlines()
        ref = np.fromfile(t12 / 'raw' / 'corpus' / f'{name}.f32', np.float32).reshape(-1, 2)
        row = {}
        for d in ('0', '+1', '-1'):
            path = TMP / f'corpus_{name}_{d}.f32'
            y = xdevpy.render('Corpus', lines, path, script_path=TMP / f'corpus_{name}_{d}.script',
                              env={'XDEV_LIBM_ULP': d} if d != '0' else None)[0]
            r = ref.astype(float)
            row[d] = dict(bit_identical=same(y, ref), window_rel_rms=M.rel_rms(y[4096:].astype(float), r[4096:]),
                          t12_window=sens.get(name, {}).get(d, {}).get('window'))
        out[name] = row
    return out


def main():
    xdevpy.build()
    TMP.mkdir(parents=True, exist_ok=True)
    out = dict(determinism=determinism(), timing=timing(), quantization=quantization(), pitch=pitch(), level=level(),
               polyphony=polyphony(), filter_linearity=filter_linearity(), extremes=extremes(), string_curves=string_curves(),
               filter_maps=filter_maps(), corpus_crosscheck=corpus_crosscheck())
    (HERE / 'results' / 'checks.json').write_text(json.dumps(out, indent=1))
    for k, v in out.items():
        print('==', k)
        print(json.dumps(v, indent=1)[:6000])


if __name__ == '__main__':
    main()
