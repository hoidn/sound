"""New offline 006-01 alias/conditioning investigation; no old code imports or writes."""
import hashlib
import json
import os
import sys
from copy import deepcopy
from pathlib import Path

assert sys.dont_write_bytecode and sys.argv[1:] in ([], ['--check'])
assert os.environ.get('OPENBLAS_NUM_THREADS') == '1'
import numpy as np
import scipy
from scipy.linalg import eig, hankel, svd
from scipy.signal import firwin, freqz, lfilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = 'analysis/ableton-live-12.4.3/'
OLD = BASE + 'full-spec-v1/depth-corpus-modal-observability/'
REVIEW = BASE + 'full-spec-v1/reviews/corpus-modal-observability-review.json'
REFERENCE = 'handoff/device-corpus-v1/reference/CORPUS-AUDIO-006-01.f32'
PINS = [OLD + name for name in ['manifest.json', 'README.md', 'diagnose.py', 'diagnostics.json']]
PINS += [REVIEW, REFERENCE, BASE + 'r2/t12-device-dsp-v1/raw/corpus/mode_membrane_44.f32',
         BASE + 'r2/t12-device-dsp-v1/results/corpus_runs.json',
         BASE + 'r2/t12-device-dsp-v1/results/corpus_model.json',
         'handoff/device-corpus-v1/manifest.json', 'handoff/device-corpus-v1/cases.json',
         'handoff/device-corpus-v1/spec.md']
FS, START, PROBE = 44100, 4096, 279.2923
ALIASES = [PROBE, FS / 4 - PROBE, FS / 4 + PROBE, FS / 2 - PROBE]


def pin(path):
    b = (ROOT / path).read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def rounding_cell(y):
    f = np.asarray(y, dtype=np.float32)
    up = np.nextafter(f, np.float32(np.inf)).astype(float) - f.astype(float)
    down = f.astype(float) - np.nextafter(f, np.float32(-np.inf)).astype(float)
    return np.maximum(up, down) / 2


def spectrum(y):
    n = np.arange(len(y))
    # Simultaneous full-rate projections are probes, not isolated-mode estimates.
    a = np.stack([v for f in ALIASES for v in
                  [np.cos(2 * np.pi * f * n / FS), np.sin(2 * np.pi * f * n / FS)]], axis=1)
    coef = np.linalg.lstsq(a, y, rcond=None)[0]
    window = np.hanning(len(y))
    fft = np.abs(np.fft.rfft(y * window, 1 << 17))
    hz = np.fft.rfftfreq(1 << 17, 1 / FS)
    bands = []
    for j, f in enumerate(ALIASES):
        ids = np.flatnonzero(abs(hz - f) < 3)
        k = ids[np.argmax(fft[ids])]
        bands.append({'probe_hz': f, 'joint_sinusoid_amplitude': float(np.hypot(*coef[2*j:2*j+2])),
                      'hann_peak_hz_within_plusminus3': float(hz[k]),
                      'hann_peak_amplitude': float(2 * fft[k] / window.sum()),
                      'hann_band_squared_magnitude': float(np.sum(fft[ids] ** 2))})
    return {'frames': len(y), 'bands': bands,
            'joint_projection_relative_residual': float(np.linalg.norm(y - a @ coef) / np.linalg.norm(y)),
            'role': 'finite full-rate spectral/projection context; no zero/high-band-absence or modal uncertainty claim'}


def estimate(y, eps, stride, height, rank):
    assert y.ndim == 1 and np.isfinite(y).all() and np.linalg.norm(y) > 0
    assert rank < height < len(y)
    h = hankel(y[:height], y[height-1:])
    u, s, _ = svd(h, full_matrices=False)
    u1, u2 = u[:-1, :rank], u[1:, :rank]
    shift = np.linalg.lstsq(u1, u2, rcond=None)[0]
    poles, left, right = eig(shift, left=True, right=True)
    rows = []
    for k, z in enumerate(poles):
        hz = float(np.angle(z) * FS / stride / (2 * np.pi))
        if 270 < hz < 290:
            overlap = abs(np.vdot(left[:, k], right[:, k]))
            rows.append({'hz': hz, 'log_radius_per_raw_sample': float(np.log(abs(z)) / stride),
                         'local_eigenvalue_condition': float(np.linalg.norm(left[:, k]) * np.linalg.norm(right[:, k]) / overlap)})
    rows.sort(key=lambda r: r['hz'])
    e_bound = float(np.linalg.norm(hankel(eps[:height], eps[height-1:]), 'fro'))
    gap = float(s[rank-1] - s[rank])
    return {'candidates_270_290': rows,
            'nearest_probe_label_only': min(rows, key=lambda r: abs(r['hz'] - PROBE)) if rows else None,
            'candidate_count': len(rows), 'cond_U1': float(np.linalg.cond(u1)),
            'cond_full_eigenvector_basis': float(np.linalg.cond(right)),
            'relative_shift_residual': float(np.linalg.norm(u1 @ shift - u2) / np.linalg.norm(u2)),
            'singular_values_at_boundary': [float(s[rank-1]), float(s[rank])],
            'absolute_singular_gap': gap, 'half_ulp_hankel_Frobenius_bound': e_bound,
            'bound_over_singular_gap': e_bound / gap,
            'role': 'condition/sensitivity diagnostics only, not a frequency confidence interval or error bound'}


def math_fixtures(taps):
    n = np.arange(12288)
    alias = np.cos(2 * np.pi * ALIASES[2] * n / FS + .2)
    low = np.cos(2 * np.pi * PROBE * n / FS + .2)
    assert np.max(abs(alias[::4] - low[::4])) < 1e-9
    principals = {str(s): abs((ALIASES[2] + FS/s/2) % (FS/s) - FS/s/2) for s in [4, 5, 7, 8, 16]}
    assert abs(principals['4'] - PROBE) < 1e-8
    assert abs(principals['5'] - PROBE) > 100 and abs(principals['7'] - PROBE) > 100
    filtered_alias = lfilter(taps, 1, alias)
    n2 = n[1602:]
    design = np.stack([np.cos(2*np.pi*ALIASES[2]*n2/FS), np.sin(2*np.pi*ALIASES[2]*n2/FS)], axis=1)
    measured_gain = float(np.linalg.norm(np.linalg.lstsq(design, filtered_alias[1602:], rcond=None)[0]))
    _, response = freqz(taps, worN=[2*np.pi*ALIASES[2]/FS])
    assert abs(measured_gain - abs(response[0])) < 1e-10
    frequencies = [259., PROBE, 280.05, 305., 700., ALIASES[2]]
    amplitudes = [1., .12, .08, .3, .05, .15]
    mixture = sum(a * np.exp(-(.000005 + j*.000001) * n) *
                  np.cos(2*np.pi*f*n/FS + .23*j)
                  for j, (a, f) in enumerate(zip(amplitudes, frequencies))).astype(np.float32).astype(float)
    rows = []
    for rank in [10, 12, 80, 100, 120]:
        record = estimate(mixture[::5], rounding_cell(mixture)[::5], 5, 410, rank)
        label = record['nearest_probe_label_only']
        rows.append({'rank': rank, 'diagnostic': record,
                     'known_probe_error_hz': label['hz'] - PROBE if label else None})
    assert abs(rows[0]['known_probe_error_hz']) > .1
    assert abs(rows[1]['known_probe_error_hz']) < 1e-4
    return {'pure_alias': {'full_rate_hz': ALIASES[2], 'principal_by_stride': principals,
                           'power_of_two_sample_identity_max_abs': float(np.max(abs(alias[::4]-low[::4]))),
                           'filtered_measured_gain': measured_gain,
                           'filtered_analytic_gain': float(abs(response[0]))},
            'abstract_nuisance_mixture': {'frequencies': frequencies, 'amplitudes': amplitudes,
                                          'known_probe_hz': PROBE, 'quantized_to_binary32': True,
                                          'experiments': rows},
            'limits': 'abstract mathematical examples, not Corpus model/parameter law, representative-noise calibration or capture uncertainty'}


def derive():
    run = json.loads((ROOT / (BASE+'r2/t12-device-dsp-v1/results/corpus_runs.json')).read_text())
    b = (ROOT / REFERENCE).read_bytes()
    assert hashlib.sha256(b).hexdigest() == run['runs']['mode_membrane_44']['sha256']
    assert b == (ROOT / (BASE+'r2/t12-device-dsp-v1/raw/corpus/mode_membrane_44.f32')).read_bytes()
    assert (run['frames'], run['impulse_at'], run['runs']['mode_membrane_44']['case']['fs']) == (16384, START, FS)
    raw = np.frombuffer(b, '<f4').reshape(-1, 2).astype(float)
    assert raw.shape == (16384, 2) and np.isfinite(raw).all()
    taps = firwin(801, 1800, fs=FS, window=('kaiser', 8.6))
    _, response = freqz(taps, worN=2*np.pi*np.asarray(ALIASES)/FS)
    fullrate, fits, perturbations = [], [], []
    for j, ch in enumerate(['L', 'R']):
        fullrate.append({'channel': ch, 'raw_frame_interval': [4160, 16384],
                         'post_impulse_nonzero': int(np.count_nonzero(raw[START:, j])),
                         'spectrum': spectrum(raw[4160:, j])})
        eps = rounding_cell(raw[:, j])
        for stride in [5, 7]:
            height = round(2048 / stride)
            for lo, hi in [(64, 6144), (6208, 12288)]:
                for rank in [80, 100, 120]:
                    ix = slice(START+lo, START+hi, stride)
                    fits.append({'channel': ch, 'family': 'coprime-raw', 'stride': stride,
                                 'height': height, 'rank': rank, 'post_impulse_interval': [lo, hi],
                                 'diagnostic': estimate(raw[ix, j], eps[ix], stride, height, rank)})
        filtered = lfilter(taps, 1, raw[:, j])
        filtered_eps_bound = lfilter(abs(taps), 1, eps)
        for rank in [100, 120]:
            ix = slice(START+1602, len(raw), 8)
            fits.append({'channel': ch, 'family': 'filtered-stride8', 'stride': 8,
                         'height': 256, 'rank': rank, 'raw_filter_output_interval': [START+1602, len(raw)],
                         'diagnostic': estimate(filtered[ix], filtered_eps_bound[ix], 8, 256, rank)})
        # Finite sensitivity directions do not span the rounding box or establish worst-case error.
        n = np.arange(len(raw))
        directions = {'alternating': np.where(n % 2, 1., -1.),
                      'probe-phase': np.where(np.cos(2*np.pi*PROBE*n/FS) >= 0, 1., -1.)}
        ix = slice(START+64, len(raw), 5)
        for name, direction in [('unperturbed', np.zeros(len(raw)))] + list(directions.items()):
            for sign in ([0] if name == 'unperturbed' else [-1, 1]):
                perturbed = raw[:, j] + sign * eps * direction
                perturbations.append({'channel': ch, 'direction': name, 'sign': sign,
                                      'stride': 5, 'height': 410, 'rank': 100,
                                      'raw_frame_interval': [4160, 16384],
                                      'diagnostic': estimate(perturbed[ix], eps[ix], 5, 410, 100)})
    return {'kind': 'new-offline006-only-alias-conditioning-investigation',
            'immutable_inputs': {p: pin(p) for p in PINS},
            'tooling': {'numpy': np.__version__, 'scipy': scipy.__version__, 'OpenBLAS_threads': 1},
            'probe_hz_label_not_truth': PROBE, 'common_power_of_two_aliases_below_Nyquist': ALIASES,
            'full_rate': fullrate, 'fits': fits, 'finite_rounding_sensitivities': perturbations,
            'analysis_filter': {'kind': '801-tap Kaiser8.6 lowpass1800Hz', 'fs': FS,
                                'group_delay_raw_samples': 400, 'discard_after_impulse_raw_samples': 1602,
                                'magnitude_at_probe_and_aliases': [float(abs(v)) for v in response],
                                'tap_sha256_little_endian_float64': hashlib.sha256(taps.astype('<f8').tobytes()).hexdigest(),
                                'role': 'offline analysis filter only; not a device design or timing law'},
            'mathematical_fixtures': math_fixtures(taps),
            'calibrated_capture_frequency_uncertainty': None, 'confidence_interval': None,
            'criterion_or_tolerance': None, 'changed_grades': 0, 'omissions_still_ungraded': 174,
            'candidate_or_original_execution': False, 'compatibility_result': None}


def near(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        for k in a: near(a[k], b[k])
    elif isinstance(a, list):
        assert len(a) == len(b)
        for x, y in zip(a, b): near(x, y)
    elif isinstance(a, float):
        assert np.isfinite(a) and abs(a-b) <= 1e-8*max(1, abs(a)), (a, b)
    else:
        assert a == b, (a, b)


if __name__ == '__main__':
    before = {p: pin(p) for p in PINS}
    result = derive()
    assert before == {p: pin(p) for p in PINS}
    if sys.argv[1:] == ['--check']:
        frozen = json.loads((HERE/'results.json').read_text())
        near(result, frozen)
        rejected = []
        for name, mutate in [
                ('invented-confidence-interval', lambda r: r.update(confidence_interval=[279.2922, 279.2925])),
                ('graded-omission', lambda r: r.update(changed_grades=1)),
                ('erased-rank80-failure', lambda r: r['fits'][0]['diagnostic']['nearest_probe_label_only'].update(hz=PROBE)),
                ('erased-underfit-fixture-failure', lambda r: r['mathematical_fixtures']['abstract_nuisance_mixture']['experiments'][0].update(known_probe_error_hz=0)),
                ('power-of-two-alias-claimed-coprime', lambda r: r['mathematical_fixtures']['pure_alias']['principal_by_stride'].update({'5': PROBE}))]:
            bad = deepcopy(frozen)
            mutate(bad)
            try:
                near(result, bad)
            except AssertionError:
                rejected.append(name)
            else:
                raise AssertionError('mutation accepted: ' + name)
        if (HERE/'manifest.json').exists():
            manifest = json.loads((HERE/'manifest.json').read_text())
            for name, expected in manifest['payloads'].items():
                assert pin(str((HERE/name).relative_to(ROOT))) == expected
            assert manifest['immutable_inputs'] == before
            assert set(manifest['payloads']) | {'manifest.json'} == {p.name for p in HERE.iterdir()}
        print(json.dumps({'status': 'pass', 'fits': len(result['fits']),
                          'finite_sensitivities': len(result['finite_rounding_sensitivities']),
                          'uncertainty_and_grades_not_adopted': True, 'pins_unchanged': len(before),
                          'rejected': rejected, 'writes': False}))
    else:
        print(json.dumps(result, separators=(',', ':'), allow_nan=False))
