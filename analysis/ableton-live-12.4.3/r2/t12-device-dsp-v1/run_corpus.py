"""Render the Corpus cases through the bundle's x86_64 slice and check determinism.

    python3 -I run_corpus.py        # writes inputs/, raw/corpus/, results/corpus_runs.json

Every case: CreateInstanceU, SetSampleRateU(fs), SetParameterA for all 38 host indices (Live's
constructor defaults from device-parameter-mapping-native.md, with the case's overrides), then CalcA
over 16384 frames in host blocks, input flag 1, transport {0, 0.0, 120.0}. Inputs are stereo with
the same signal on both channels. Determinism: each listed case is rendered again in a new process
and the variants (block size, MXCSR, sample-rate history, the clock value that seeds rand) are
compared with their base, bit for bit.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import xdevpy  # noqa: E402

FRAMES, IMPULSE_AT = 16384, 4096
# Host index -> value Live passes for a fresh Corpus (N5 table, checked by check_defaults();
# FilterMidFreq 1000 Hz -> log10(20)/log10(360) rounded to binary32; DecayOnNoteOff stored 0 -> 1 - 0).
DEFAULTS = {0: 0, 1: 0.5, 2: 0, 3: 0, 4: 0.5, 5: 0.5, 6: 0.5, 7: 0, 8: 0, 9: 0, 10: 5, 11: 0, 12: 0, 13: 0,
            14: 0.5, 15: 0.1, 16: 0.9, 17: 0, 18: 0, 19: 0, 20: 0.5, 21: 4, 22: 0, 23: 0, 24: 180, 25: 0,
            26: 0, 27: 0, 28: float(np.float32(np.log10(1000 / 50) / np.log10(360))), 29: 4, 30: 0.5,
            31: 1, 32: 0.5, 33: 2, 34: 1, 35: 1, 36: 0, 37: 0}
WET = {32: 1}                                     # DryWet 1: no dry signal in the output
SINES = [261.62, 400.0, 1000.0, 3000.0]


def make_inputs(d):
    d.mkdir(exist_ok=True)
    out = {}
    for fs in (44100, 48000):
        x = np.zeros((FRAMES, 2), np.float32)
        x[IMPULSE_AT] = 1.0
        out[f'impulse{fs // 1000}'] = x
        for f in SINES:
            n = np.arange(FRAMES)
            s = (0.25 * np.sin(2 * np.pi * f * n / fs)).astype(np.float32)
            out[f'sine{int(f)}_{fs // 1000}'] = np.stack([s, s], 1)
    out['dc44'] = np.full((FRAMES, 2), 0.5, np.float32)
    x = np.zeros((FRAMES, 2), np.float32)
    x[IMPULSE_AT, 0] = 1.0
    out['impulseL44'] = x
    rng = np.random.default_rng(1214)
    s = (0.1 * rng.standard_normal(FRAMES)).astype(np.float32)
    out['noise44'] = np.stack([s, s], 1)
    for k, v in out.items():
        v.tofile(d / f'{k}.f32')
    return {k: str(d / f'{k}.f32') for k in out}


def case(name, inp, fs=44100, params=None, block=512, pre=None, mxcsr=None):
    return dict(name=name, input=inp, fs=fs, params={**DEFAULTS, **(params or {})}, block=block,
                pre=pre or [f'rate {fs}'], post=[], mxcsr=mxcsr)


def cases():
    imp = lambda fs: f'impulse{fs // 1000}'  # noqa: E731
    c = [case('defaults_44', 'impulse44'), case('defaults_48', 'impulse48', 48000)]
    for t, nm in enumerate(['beam', 'marimba', 'string', 'membrane', 'plate']):
        c.append(case(f'mode_{nm}_44', 'impulse44', params={**WET, 0: t, 1: 1, 33: 3}))
    for t, nm in [(0, 'beam'), (2, 'string')]:
        c.append(case(f'mode_{nm}_48', 'impulse48', 48000, {**WET, 0: t, 1: 1, 33: 3}))
    for v in (0.25, 0.5625, 0.75, 1.0):
        c.append(case(f'pitch_{v:g}', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 0, 6: v}))
    c.append(case('detune_0.5', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 0, 9: 0.5}))
    for v in (0.25, 0.5, 0.75):
        c.append(case(f'decay_{v:g}', 'impulse44', params={**WET, 0: 2, 33: 1, 1: v}))
    for t in (-1, -0.5, 0.5, 1):
        c.append(case(f'tone_{t:g}', 'impulse44', params={**WET, 0: 2, 33: 1, 1: 0.5, 2: t}))
    c.append(case('decay_0.5_48', 'impulse48', 48000, {**WET, 0: 2, 33: 1, 1: 0.5}))
    for v in (-1, -0.5, 0, 0.5, 1):
        c.append(case(f'hit_{v:g}', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 1, 14: v}))
    for ch, idx in (('L', 15), ('R', 16)):
        for v in (0, 0.5, 1):
            c.append(case(f'listen{ch}_{v:g}', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 1, 14: 1, idx: v}))
    for f in SINES:
        c.append(case(f'sine_{int(f)}', f'sine{int(f)}_44', params={1: 0.1}))
    c.append(case('sine_1000_48', 'sine1000_48', 48000, {1: 0.1}))
    c.append(case('noise_44', 'noise44', params={1: 0.1}))
    for t, nm in [(5, 'pipe'), (6, 'tube')]:
        for fs in (44100, 48000):
            c.append(case(f'wg_{nm}_{fs // 1000}', imp(fs), fs, {**WET, 0: t, 1: 1}))
    c.append(case('filter_on', 'noise44', params={1: 0.1, 27: 1}))
    c.append(case('lfo_sine', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 1, 17: 1, 20: 0.8, 26: 0.3}))
    c.append(case('width_0', 'impulse44', params={**WET, 31: 0}))
    c.append(case('lfo_sah', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 1, 17: 1, 18: 5, 20: 0.8, 26: 0.3}))
    for v in (-0.5, 0.5):
        c.append(case(f'inharm_{v:g}', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 1, 3: v}))
    for v in (-1, 1):
        c.append(case(f'bright_{v:g}', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 1, 11: v}))
    for v in (0.2, 0.8):
        c.append(case(f'ratio_{v:g}', 'impulse44', params={**WET, 0: 3, 1: 1, 33: 1, 4: v}))
    c.append(case('bleed_1', 'impulse44', params={**WET, 0: 2, 1: 1, 33: 0, 36: 1}))
    for nm, extra in (('radius_0', {5: 0}), ('radius_1', {5: 1}), ('opening_0.3', {35: 0.3})):
        c.append(case(f'wg_pipe_{nm}', 'impulse44', params={**WET, 0: 5, 1: 1, **extra}))
    c.append(case('wg_tube_radius_0', 'impulse44', params={**WET, 0: 6, 1: 1, 5: 0}))
    c.append(case('filter_200_bw1', 'noise44', params={1: 0.1, 27: 1, 28: float(np.float32(np.log10(200 / 50) / np.log10(360))), 29: 1}))
    for v in (0, 1):
        c.append(case(f'drive_{v:g}', 'sine1000_44', params={1: 0.1, 30: v}))
    c.append(case('drywet_0.25', 'sine1000_44', params={1: 0.1, 32: 0.25}))
    c.append(case('startup_dry', 'dc44', params={32: 0}))
    c.append(case('left_only', 'impulseL44'))
    return c


# Variants rendered for determinism only: (name, base case, changes)
VARIANTS = [('defaults_44_block64', 'defaults_44', dict(block=64)), ('defaults_44_block256', 'defaults_44', dict(block=256)),
            ('defaults_44_block333', 'defaults_44', dict(block=333)), ('defaults_44_block2048', 'defaults_44', dict(block=2048)),
            ('defaults_44_ftz_daz', 'defaults_44', dict(mxcsr=0x9fc0)),
            ('defaults_48_via_44', 'defaults_48', dict(pre=['rate 44100', 'rate 48000'])),
            ('defaults_44_via_48', 'defaults_44', dict(pre=['rate 48000', 'rate 44100'])),
            ('defaults_48_rate_after_params', 'defaults_48', dict(pre=['rate 44100'], post=['rate 48000'])),
            ('noise_44_block128', 'noise_44', dict(block=128)), ('noise_44_ftz_daz', 'noise_44', dict(mxcsr=0x9fc0)),
            ('lfo_sine_block100', 'lfo_sine', dict(block=100)),
            ('defaults_44_seed1760000000', 'defaults_44', dict(env={'XDEV_TIME': '1760000000'})),
            ('lfo_sine_seed1760000000', 'lfo_sine', dict(env={'XDEV_TIME': '1760000000'})),
            ('lfo_sah_seed1760000000', 'lfo_sah', dict(env={'XDEV_TIME': '1760000000'})),
            # Live's reset sequence as N5 reads it: 1,024 frames of silent input, ResetA, index 0 sent again
            ('defaults_44_warmup_reset', 'defaults_44', dict(post=['inflag 1', 'input zero', 'process 1024 512', 'reset', 'param 0 0.0'])),
            ('wg_tube_44_warmup_reset', 'wg_tube_44', dict(post=['inflag 1', 'input zero', 'process 1024 512', 'reset', 'param 0 6.0'])),
            ('wg_tube_44_reset_only', 'wg_tube_44', dict(post=['reset'])),
            # MIDI side-chain parameters with MidiPitch and MidiGate off; a Decay value in the same controller step
            ('defaults_44_midi_params', 'defaults_44', dict(post=['param 7 12.0', 'param 8 50.0', 'param 10 24.0', 'param 34 0.0', 'param 37 1.0'])),
            ('decay_0.5_same_step', 'decay_0.5', dict(post=['param 1 0.503']))]
RERUN = ['defaults_44', 'defaults_48', 'noise_44', 'mode_plate_44', 'wg_tube_48', 'lfo_sine']


def script(c, inputs):
    lines = ['create', *c['pre']]
    lines += [f'param {i} {float(v)!r}' for i, v in sorted(c['params'].items())] + c['post']
    if c['mxcsr']:
        lines.append(f"mxcsr {c['mxcsr']:#x}")
    lines += ['inflag 1', f"input {inputs[c['input']]}", f"process {FRAMES} {c['block']}", 'destroy']
    return lines


def flags_line(log):
    return next((l for l in log.splitlines() if l.startswith('process')), '')


def check_defaults():
    """DEFAULTS must equal N5's sent_for_default column (n5-device-mapping-v1/out/conversions.tsv)."""
    import csv
    rows = [r for r in csv.DictReader((HERE.parent / 'n5-device-mapping-v1' / 'out' / 'conversions.tsv').open(), delimiter='\t')
            if r['device'] == 'Corpus']
    assert len(rows) == 38 and all(abs(float(r['sent_for_default']) - DEFAULTS[int(r['index'])]) < 1e-6 for r in rows)


def main():
    check_defaults()
    xdevpy.build()
    inputs = make_inputs(HERE / 'inputs')
    raw = HERE / 'raw' / 'corpus'
    raw.mkdir(parents=True, exist_ok=True)
    scratch = Path('/var/tmp/sound-analysis/t12-xdev/rerun')
    scratch.mkdir(parents=True, exist_ok=True)
    all_cases = {c['name']: c for c in cases()}
    runs = {}
    for name, c in all_cases.items():
        _, log = xdevpy.render('Corpus', script(c, inputs), raw / f'{name}.f32')
        (raw / f'{name}.log').write_text(log)
        runs[name] = dict(case=c, sha256=xdevpy.sha256(raw / f'{name}.f32'), process=flags_line(log),
                          imports=xdevpy.used_imports(log), retained=True)
    det = []
    for name in RERUN:
        _, log = xdevpy.render('Corpus', script(all_cases[name], inputs), scratch / f'{name}.f32')
        det.append(dict(check='rerun', case=name, sha256=xdevpy.sha256(scratch / f'{name}.f32'),
                        equal=xdevpy.sha256(scratch / f'{name}.f32') == runs[name]['sha256']))
    for vname, base, change in VARIANTS:
        c = {**all_cases[base], **change, 'name': vname}
        y, log = xdevpy.render('Corpus', script(c, inputs), scratch / f'{vname}.f32', env=c.get('env'))
        (raw / f'{vname}.log').write_text(log)
        yb = np.fromfile(raw / f'{base}.f32', np.float32).reshape(-1, 2)
        lead = len(y) - len(yb)                   # frames rendered before the case's own input (warm-up)
        y = y[lead:]
        diff = np.abs(y.astype(float) - yb.astype(float))
        det.append(dict(check='variant', case=vname, base=base, change={k: v for k, v in change.items()},
                        sha256=xdevpy.sha256(scratch / f'{vname}.f32'), equal=bool(np.array_equal(y.view(np.uint32), yb.view(np.uint32))),
                        max_abs_diff=float(diff.max()), first_diff_frame=int(np.argmax(diff.max(1) > 0)) if diff.max() > 0 else None,
                        peak=float(np.abs(yb).max()), leading_frames_dropped=lead, process=flags_line(log)))
    out = HERE / 'results'
    out.mkdir(exist_ok=True)
    (out / 'corpus_runs.json').write_text(json.dumps(dict(
        frames=FRAMES, impulse_at=IMPULSE_AT, defaults=DEFAULTS, inputs={k: xdevpy.sha256(v) for k, v in inputs.items()},
        bundle=str(xdevpy.BUNDLES['Corpus']), bundle_sha256=xdevpy.sha256(xdevpy.BUNDLES['Corpus']),
        runs=runs, determinism=det), indent=1, default=str))
    bad = [d for d in det if not d['equal']]
    print(f'{len(runs)} cases rendered; determinism checks {len(det)}, unequal: {[d["case"] for d in bad]}')


if __name__ == '__main__':
    main()
