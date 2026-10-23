"""New offline numerical diagnostics of two immutable captures; no device/model imports."""
import hashlib
import json
import os
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

assert sys.dont_write_bytecode and sys.argv[1:] in ([], ['--check'])
assert os.environ.get('OPENBLAS_NUM_THREADS') == '1'
import numpy as np
import scipy
from scipy.linalg import hankel, svd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = 'analysis/ableton-live-12.4.3/'
TRACE = BASE + 'handoff-staging/device-corpus-v1-analysis/traceability.json'
MODEL = BASE + 'r2/t12-device-dsp-v1/results/corpus_model.json'
RUNS = BASE + 'r2/t12-device-dsp-v1/results/corpus_runs.json'
PRE = BASE + 'full-spec-v1/depth-preflight-corpus/preflight.json'
REF = 'handoff/device-corpus-v1/reference/CORPUS-AUDIO-'
PINS = [TRACE, MODEL, RUNS, PRE,
        BASE + 'full-spec-v1/depth-preflight-corpus/manifest.json',
        BASE + 'r2/t12-device-dsp-v1/fit.py',
        BASE + 'r2/t12-device-dsp-v1/analyze_corpus.py',
        BASE + 'handoff-staging/device-corpus-v1-analysis/build.py',
        'handoff/device-corpus-v1/manifest.json', 'handoff/device-corpus-v1/cases.json',
        'handoff/device-corpus-v1/spec.md']
for ev, run in [('009', 'pitch_0.25'), ('006', 'mode_membrane_44')]:
    PINS += [REF + ev + '-01.f32']
    PINS += [BASE + 'r2/t12-device-dsp-v1/raw/corpus/' + run + ext for ext in ['.f32', '.script', '.log']]


def pin(path):
    b = (ROOT / path).read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def load(path):
    return json.loads((ROOT / path).read_text())


def subspace(y, stride, height, rank):
    """SVD shift-invariance estimate. Frequencies are not supplied to the fit."""
    assert y.ndim == 1 and np.isfinite(y).all() and np.linalg.norm(y) > 0
    assert rank < height < len(y)
    u, s, _ = svd(hankel(y[:height], y[height - 1:]), full_matrices=False)
    poles = np.linalg.eigvals(np.linalg.lstsq(u[:-1, :rank], u[1:, :rank], rcond=None)[0])
    rows = sorted(({'hz': float(np.angle(z) * 44100 / stride / (2 * np.pi)),
                    'log_radius_per_raw_sample': float(np.log(abs(z)) / stride)}
                   for z in poles if np.angle(z) > 1e-6), key=lambda x: x['hz'])
    spectrum = {'first_twelve_relative': [float(x / s[0]) for x in s[:12]],
                'rank_boundary_relative': [float(s[rank - 1] / s[0]), float(s[rank] / s[0])]}
    return rows, spectrum


def numeric_fixture():
    # Abstract mathematical fixture, not a Corpus signal model or a compatibility oracle.
    n = np.arange(1536)
    frequencies = [63.25, 127.75, 201.5, 261.625, 279.29]
    y = sum((1 / (j + 1)) * np.exp(-0.00005 * n) *
            np.cos(2 * np.pi * f * n / (44100 / 8) + 0.2 * j)
            for j, f in enumerate(frequencies))
    rows, _ = subspace(y, 8, 128, 10)
    err = max(abs(r['hz'] - f) for r, f in zip(rows, frequencies))
    assert len(rows) == 5 and err < 1e-7
    return {'known_tones': frequencies, 'maximum_recovery_error_hz': err,
            'role': 'numerical code sanity only; no observed-device tolerance or calibration'}


def derive():
    trace, model, runs, pre = (load(x) for x in [TRACE, MODEL, RUNS, PRE])
    omissions, summaries = [], []
    for ei, ev in enumerate(trace['evaluations']):
        if not ev['ungraded_modes']:
            continue
        run = ev['source_run']
        for ch in ['L', 'R']:
            r = model['modes'][run][ch]
            summaries.append({'evaluation': ev['evaluation'], 'channel': ch,
                              'pointer': '/modes/' + run + '/' + ch,
                              'summary': {k: v for k, v in r.items() if k not in ['modes', 'f0']}})
        for oi, omission in enumerate(ev['ungraded_modes']):
            ch, mode = omission['channel'], omission['mode']
            mi, row = next((j, r) for j, r in enumerate(model['modes'][run][ch]['modes']) if r['k'] == mode)
            category = 'historically-unresolved-decay'
            if row['resolved']:
                category = ('model-estimator-bias-also-outside-band' if
                            abs(row['model_est_hz'] / row['pole_hz'] - 1) >= 1e-4 else
                            'reference-offset-with-small-model-estimator-bias')
                assert abs(row['render_hz'] / row['pole_hz'] - 1) >= 1e-4
            cutoff = min(100, 0.4 * row['gap_hz'])
            requested = int(3.3 * runs['runs'][run]['case']['fs'] / cutoff) | 1
            omissions.append({'evaluation': ev['evaluation'], 'run': run,
                              'trace_pointer': f'/evaluations/{ei}/ungraded_modes/{oi}',
                              'measurement_pointer': f'/modes/{run}/{ch}/modes/{mi}',
                              'channel': ch, 'mode': mode, 'historical_reason': omission['why'],
                              'retained_numeric_projection': {k: row[k] for k in
                                  ['resolved', 'pole_hz', 'render_hz', 'model_est_hz',
                                   'estimator_bias', 'gap_hz', 'weight'] if k in row},
                              'diagnostic_category': category,
                              'historical_requested_taps': requested,
                              'historical_track_capped_taps': min(4001, requested),
                              'status': 'ungraded-unchanged'})
    expected = {(x['evaluation'], g['channel'], k) for x in pre['omitted_modal_modes']
                for g in x['groups'] for k in g['mode_indices']}
    assert expected == {(x['evaluation'], x['channel'], x['mode']) for x in omissions}
    assert len(omissions) == 174 and len({x['evaluation'] for x in omissions}) == 14
    raw_checks, experiments = [], []
    for ev, run in [('009', 'pitch_0.25'), ('006', 'mode_membrane_44')]:
        path = REF + ev + '-01.f32'
        b = (ROOT / path).read_bytes()
        assert hashlib.sha256(b).hexdigest() == runs['runs'][run]['sha256']
        assert b == (ROOT / (BASE + 'r2/t12-device-dsp-v1/raw/corpus/' + run + '.f32')).read_bytes()
        raw = np.frombuffer(b, dtype='<f4').reshape(-1, 2).astype(float)
        assert raw.shape == (16384, 2) and np.isfinite(raw).all()
        raw_checks.append({'evaluation': 'CORPUS-AUDIO-' + ev + '-01', 'reference': path,
                           'frames': len(raw), 'sample_rate_from_retained_case': 44100,
                           'channels': [{'channel': ch, 'post_impulse_nonzero_samples': int(np.count_nonzero(raw[4096:, j])),
                                         'post_impulse_peak_abs': float(np.max(np.abs(raw[4096:, j]))),
                                         'post_impulse_rms': float(np.sqrt(np.mean(raw[4096:, j] ** 2)))}
                                        for j, ch in enumerate(['L', 'R'])]})
        # Controls intentionally retain weak/underfitted variants, not only successful settings.
        settings = ([(lo, 12288, stride, 96, 8) for lo in [64, 1024, 3072] for stride in [8, 16]] +
                    [(lo, 12288, 16, 128, rank) for lo in [64, 1024, 3072] for rank in [10, 12]] +
                    [(lo, hi, stride, 192, 8) for lo, hi in [(64, 6144), (6208, 12288)] for stride in [4, 8]]
                    if ev == '009' else
                    [(64, 12288, stride, height, rank) for stride, height in [(4, 512), (8, 256), (16, 128)] for rank in [80, 100, 120]] +
                    [(lo, hi, stride, 192, 100) for lo, hi in [(64, 6144), (6208, 12288)] for stride in [4, 8]])
        for ch, j in [('L', 0), ('R', 1)]:
            for lo, hi, stride, height, rank in settings:
                y = raw[4096 + lo:4096 + hi:stride, j]
                rows, singular = subspace(y, stride, height, rank)
                # Selection is post-fit labeling only, never an input frequency/initialization.
                selected = [r for r in rows if (50 < r['hz'] < 280 if ev == '009' else 240 < r['hz'] < 350)]
                experiments.append({'evaluation': 'CORPUS-AUDIO-' + ev + '-01', 'channel': ch,
                                    'offset_after_frame4096': [lo, hi], 'stride': stride,
                                    'hankel_height': height, 'rank': rank, 'sample_count': len(y),
                                    'selected_positive_poles': selected,
                                    'singular_spectrum_summary': singular})
    return {'kind': 'new-offline-retained-numeric-diagnostics-not-reference-execution',
            'immutable_inputs': {p: pin(p) for p in PINS},
            'tooling': {'numpy': np.__version__, 'scipy': scipy.__version__, 'OpenBLAS_threads': 1},
            'historical_omission_count': 174, 'historical_omission_evaluations': 14,
            'classification_counts': dict(Counter(x['diagnostic_category'] for x in omissions)),
            'measurement_summaries': summaries, 'omissions': omissions,
            'raw_capture_checks': raw_checks, 'experiments': experiments,
            'numerical_fixture': numeric_fixture(),
            'changed_grades': 0, 'new_required_outcome_numerator': None,
            'reference_or_candidate_execution': False, 'compatibility_result': None,
            'new_expected_or_comparison_oracle': None, 'independent_review': 'pending-as-of-freeze'}


def near(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a: near(a[k], b[k])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b): near(x, y)
    elif isinstance(a, float):
        assert np.isfinite(a) and abs(a - b) <= 1e-8 * max(1, abs(a)), (a, b)
    else:
        assert a == b, (a, b)


if __name__ == '__main__':
    before = {p: pin(p) for p in PINS}
    result = derive()
    assert before == {p: pin(p) for p in PINS}
    if sys.argv[1:] == ['--check']:
        frozen = json.loads((HERE / 'diagnostics.json').read_text())
        near(result, frozen)
        rejected = []
        for name, mutate in [
                ('wrong-actual-measurement-pointer', lambda x: x['omissions'][0].update(measurement_pointer='/modes/pitch_0.25/L/modes/0')),
                ('omitted-status-promoted', lambda x: x['omissions'][0].update(status='graded')),
                ('new-compatibility-credit', lambda x: x.update(compatibility_result='pass')),
                ('frequency-result-replaced-with-static-center', lambda x: x['experiments'][0]['selected_positive_poles'][0].update(hz=66.14462745838128))]:
            bad = deepcopy(frozen)
            mutate(bad)
            try:
                near(result, bad)
            except AssertionError:
                rejected.append(name)
            else:
                raise AssertionError('mutation accepted: ' + name)
        if (HERE / 'manifest.json').exists():
            manifest = json.loads((HERE / 'manifest.json').read_text())
            for name, expected in manifest['payloads'].items():
                b = (HERE / name).read_bytes()
                assert expected == {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
            assert manifest['immutable_inputs'] == before
            assert set(manifest['payloads']) | {'manifest.json'} == {x.name for x in HERE.iterdir()}
        print(json.dumps({'status': 'pass', 'omissions_still_ungraded': 174,
                          'experiments_reproduced': len(result['experiments']),
                          'pins_unchanged': len(before), 'rejected': rejected, 'writes': False}))
    else:
        print(json.dumps(result, indent=2, allow_nan=False))
