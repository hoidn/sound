"""Reference renders of the SPEC-DEVICE-ELECTRIC acceptance cases, their measures and tolerances.

    python3 -I run_cases.py      # writes raw/<case>.wav, raw/<case>.script, results/cases.json

Each case is rendered under el.py's protocol with the clock value fixed at 0 (retained, mono binary32
WAV). Six variants are rendered but not retained: four other clock values (SEEDS, about 37 days
apart, so that the generator's first outputs are unrelated), and every inexact libm result moved one
ulp up and down (XDEV_LIBM_ULP). Their deviations from the reference set each case's graded elements
and tolerances (measure.grade). The noise level is measured between the reference and each of the
four reseeded renders; the case states their mean and range.
"""
import hashlib
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import el  # noqa: E402
import fit  # noqa: E402
import measure as M  # noqa: E402
import xdevpy  # noqa: E402

RAW = HERE / 'raw'
SHORT = 22050                     # 0.5 s single-note cases: on at 0, off at 0.3 s
SEEDS = [1760000000 + k * 3196800 for k in range(4)]
VARIANTS = [(f'seed{k + 1}', {'XDEV_TIME': str(t)}) for k, t in enumerate(SEEDS)] + \
    [('ulp+', {'XDEV_LIBM_ULP': '+1'}), ('ulp-', {'XDEV_LIBM_ULP': '-1'})]


def single(stored, n=60, v=100, fs=44100, frames=SHORT, off=13230):
    return dict(stored=stored, events=el.note(n, v, 0, off), fs=fs, frames=frames, note=n, off=off,
                band_starts=[0, fs // 10, off])


def cases():
    C = el.CONSTRUCTOR
    out = {'defaults_c4': dict(single(C, frames=44100, off=22050), band_starts=[0, 4410, 17640, 22050]),
           'defaults_c4_48': dict(single(C, fs=48000, frames=48000, off=24000), band_starts=[0, 4800, 19200, 24000])}
    for n in (21, 36, 48, 72, 84, 96, 108):
        out[f'key_{n}'] = single(C, n)
    for v in (1, 32, 64, 96, 127):
        out[f'vel_{v}'] = single(C, v=v)
    pr = el.presets()
    out['preset_defaults_c4'] = single(pr['Defaults'])
    for i, name in enumerate(el.NAMES):
        if name in (None, 'Polyphony', 'PitchBendRange', 'Volume', 'PickupModel', 'KeyboardTranspose'):
            continue
        for val in (0.0, 1.0):
            out[f'p{i:02d}_{val:g}'] = single({**C, name: val})
    out['p23_1'] = single({**C, 'PickupModel': 1})
    out['p30_0'] = single({**C, 'KeyboardTranspose': 0})
    out['p30_24'] = single({**C, 'KeyboardTranspose': 24})
    out['p02_1'] = single({**C, 'Volume': 1.0})
    out['p02_0.25'] = single({**C, 'Volume': 0.25})
    for i in (5, 8, 13, 17, 26):
        for n in (36, 84):
            for val in (0.0, 1.0):
                out[f'p{i:02d}_{val:g}_key{n}'] = single({**C, el.NAMES[i]: val}, n)
    phrase = [(0, 0x90, 48, 100), (17640, 0x80, 48, 0)] + [(22050, 0x90, m, 80) for m in (64, 67, 72)] + \
             [(39690, 0x80, m, 0) for m in (64, 67, 72)]
    starts = [0, 4410, 17640, 22050, 26460, 39690]
    for name, st in pr.items():
        if name == 'Defaults':
            continue
        key = 'preset_' + name.lower().replace(' ', '_').replace('-', '')
        out[key] = dict(stored=st, events=phrase, fs=44100, frames=52920, band_starts=starts)
    for name in ('Wurli Classic Piano', 'E-Piano MKI Simple'):
        key = 'preset_' + name.lower().replace(' ', '_').replace('-', '') + '_48'
        out[key] = dict(stored=pr[name], fs=48000, frames=57600, band_starts=[int(s * 48000 / 44100) for s in starts],
                        events=[(int(f * 48000 / 44100), s, a, b) for f, s, a, b in phrase])
    off_all = lambda f, ms: [(f, 0x80, m, 0) for m in ms]  # noqa: E731
    out['poly_2_steal'] = dict(stored={**C, 'Polyphony': 0}, fs=44100, frames=26460, band_starts=[0, 4410, 6615, 13230],
                               events=[(0, 0x90, 60, 100), (2205, 0x90, 64, 100), (4410, 0x90, 67, 100)] + off_all(22050, (60, 64, 67)))
    out['poly_2_released_first'] = dict(stored={**C, 'Polyphony': 0}, fs=44100, frames=26460, band_starts=[0, 6615, 8820, 13230],
                                        events=[(0, 0x90, 60, 100), (2205, 0x90, 64, 100), (4410, 0x80, 64, 0),
                                                (6615, 0x90, 67, 100)] + off_all(22050, (60, 67)))
    out['poly_2_repeat'] = dict(stored={**C, 'Polyphony': 0}, fs=44100, frames=26460, band_starts=[0, 2205, 6615, 13230],
                                events=[(0, 0x90, 60, 100), (2205, 0x90, 60, 100), (4410, 0x90, 64, 100)] + off_all(22050, (60, 64)))
    ns = list(range(36, 69))
    out['poly_32_steal'] = dict(stored=C, fs=44100, frames=44100, band_starts=[0, 4410, 9900, 13230, 30870],
                                events=[(300 * k, 0x90, m, 100) for k, m in enumerate(ns)] + off_all(30870, ns))
    out['auto_volume'] = dict(single(C, frames=SHORT, off=17640), extra=[(8192, 'param 2 0.35')], band_starts=[0, 4410, 13230])
    out['auto_finetune'] = dict(single(C, frames=SHORT, off=17640), extra=[(8192, 'param 3 1.0')], band_starts=[0, 4410, 13230])
    out['auto_forcevel'] = dict(stored=C, fs=44100, frames=SHORT, note=60, off=2048 + 13230, extra=[(0, 'param 9 1.0')],
                                events=el.note(60, 100, 2048, 13230), band_starts=[2048, 6458, 15278])
    return out


def nominal_f0(case):
    s = case['stored']
    t = int(el.host_values(s)[30]) - 12
    return 440 * 2 ** ((case['note'] - 69 + t + (s['KeyboardFineTune'] - 0.5)) / 12)


def ref_f0(x, fs, case, on):
    """Fundamental of a single-note reference: the strongest of harmonics 1..4 near k * nominal
    (+/- 3 %), refined by fit.track over [on + 30 ms, off), divided by k."""
    nom = nominal_f0(case)
    seg = x[on + int(0.03 * fs):case['off']]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 19))
    hz = np.fft.rfftfreq(1 << 19, 1 / fs)
    best = None
    for k in range(1, 5):
        if k * nom > fs / 2 - 200:
            break
        lo, hi = np.searchsorted(hz, k * nom * 0.97), np.searchsorted(hz, k * nom * 1.03)
        j = lo + int(np.argmax(sp[lo:hi]))
        if best is None or sp[j] > best[0]:
            best = (sp[j], k, hz[j])
    _, k, g = best
    t = fit.track(x[:case['off']], g, fs, on + int(0.03 * fs), min(20.0, g / 4))
    return float(t['hz'] / k), k


def run_case(item):
    name, case = item
    host = el.host_values(case['stored'])
    fs = case['fs']
    x, log = el.render(host, case['events'], fs, name, case['frames'], extra=case.get('extra', ()),
                       script_path=RAW / f'{name}.script')
    el.write_wav(RAW / f'{name}.wav', x, fs)
    mcase = dict(band_starts=case['band_starts'])
    on = M.onset(x)
    if 'note' in case and 'extra' not in case and on is not None:
        mcase.update(f0=None, off=case['off'])
        mcase['f0'], mcase['f0_harmonic'] = ref_f0(x, fs, case, on)
    ref = M.measure(x, fs, mcase)
    devs, var = [], {}
    for tag, env in VARIANTS:
        y, _ = el.render(host, case['events'], fs, f'{name}.{tag}', case['frames'], extra=case.get('extra', ()), env=env)
        var[tag] = y
        devs.append(M.element_deviations(ref, M.measure(y, fs, mcase), fs))
    masks, tol, summary = M.grade(devs, ref)
    per_variant = {tag: {k: float(d[k][masks[k]].max()) if masks[k].any() else 0.0 for k in masks}
                   for (tag, _), d in zip(VARIANTS, devs)}
    res = dict(fs=fs, frames=case['frames'], events=case['events'], extra=case.get('extra', []),
               stored_changes={k: v for k, v in case['stored'].items() if abs(v - el.CONSTRUCTOR[k]) > 1e-9},
               host=host, wav=f'raw/{name}.wav', wav_sha256=hashlib.sha256((RAW / f'{name}.wav').read_bytes()).hexdigest(),
               f0=mcase.get('f0'), f0_harmonic=mcase.get('f0_harmonic'), measures=ref,
               onset_same_in_variants=all(d['onset'] for d in devs),
               graded={k: np.nonzero(v)[0].tolist() if v.ndim == 1 else [np.nonzero(r)[0].tolist() for r in v] for k, v in masks.items()},
               tolerances=tol, grading_summary=summary, variant_max_deviation_on_graded=per_variant, imports=xdevpy.used_imports(log),
               process=[l for l in log.splitlines() if l.startswith('process')])
    if on is not None:
        stop = case.get('off', case['frames'])
        lv = [M.noise_level_db(x, var[f'seed{k}'], on, stop) for k in range(1, 5)]
        res['noise_level_db'] = dict(mean=float(np.mean(lv)), min=float(min(lv)), max=float(max(lv)), window=[on, stop])
    return name, res


def main():
    xdevpy.build()
    RAW.mkdir(exist_ok=True)
    cs = cases()
    with Pool(6) as p:
        out = dict(p.map(run_case, sorted(cs.items())))
    meta = dict(protocol='el.py docstring', warm_up=el.WARM, block=el.BLOCK, variants=dict(VARIANTS),
                floors=M.FLOOR, caps=M.CAP, freq_tol_ulp_bounds=M.FREQ_TOL, noise_tol_db=M.NOISE_TOL_DB,
                band_centres_hz=M.band_centres(), constructor=el.CONSTRUCTOR)
    (HERE / 'results' / 'cases.json').write_text(json.dumps(dict(meta=meta, cases=out), indent=1))
    for k, r in out.items():
        t, g, nz = r['tolerances'], r['grading_summary'], r.get('noise_level_db', {})
        print(f"{k:34s} on={r['measures']['onset']}/{r['measures']['onset_1e6']} same={r['onset_same_in_variants']} "
              f"pk={r['measures']['peak']:.3f} f0={r['f0'] or 0:.3f} " + ' '.join(f'{a}={b:.3g}' for a, b in t.items()) + ' | '
              + ' '.join(f'{a}={b:.3g}' for a, b in g.items()) + f" | noise {nz.get('mean', 0):.1f} [{nz.get('min', 0):.1f},{nz.get('max', 0):.1f}]")


if __name__ == '__main__':
    main()
