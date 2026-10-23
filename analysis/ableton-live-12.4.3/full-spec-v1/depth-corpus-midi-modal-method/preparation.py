"""ONE data-only calibration after Root source approval; never render device audio."""
from pathlib import Path
import hashlib
import cmath
import importlib.util
import json
import math
import struct
import sys
import tempfile

PROTOCOL = Path('/tmp/corpus-midi-note72-modal-preparation.protocol.json')
RATE, FRAMES, IMPULSE, CUTOFF = 44100, 16384, 4096, 100.0


def identity(path):
    data = Path(path).read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def hypothesis(pitch):
    """Stated rounding approximation of REQ005/007, NOT vendor FP emulation."""
    w0 = struct.unpack('<f', struct.pack('<I', 0x44cd79d3))[0]
    pi, damping = f32(math.pi), f32(8.0 / 35.0)
    result = []
    for index in range(16):
        w = f32(f32(w0 * f32(2.0 ** pitch)) * f32(index + 1))
        theta = f32(w / RATE)
        alpha = f32(f32(f32(pi / f32(pi - theta)) * f32(math.sin(theta)))
                    * f32(damping / w))
        denominator = f32(1.0 + alpha)
        a1 = f32(f32(-2.0 * f32(math.cos(theta))) / denominator)
        a2 = f32(f32(1.0 - alpha) / denominator)
        assert 0.0 < a2 < 1.0
        cosine = -a1 / (2.0 * math.sqrt(a2))
        assert -1.0 < cosine < 1.0
        result.append({'mode': index + 1, 'w_rad_s': w,
                       'a1_binary32': a1, 'a2_binary32': a2,
                       'center_hz': math.acos(cosine) * RATE / (2.0 * math.pi),
                       'pole_log_radius': 0.5 * math.log(a2), 'cutoff_hz': CUTOFF})
    return result


def encoded(fit):
    frequency, radius, amplitude = fit
    assert all(math.isfinite(float(x)) for x in
               [frequency, radius, amplitude.real, amplitude.imag])
    return {'frequency_hz': float(frequency), 'log_radius_per_frame': float(radius),
            'complex_amplitude': [float(amplitude.real), float(amplitude.imag)],
            'amplitude_magnitude': float(abs(amplitude))}


def diagnostic_halves(module, signal, center):
    """Same FIR and fit equations; ONLY fit slices change. Never grade halves."""
    np = module.np
    taps = min(4001, int(3.3 * RATE / CUTOFF) | 1)
    n = np.arange(len(signal))
    h = module.firwin(taps, CUTOFF, fs=RATE, window='hamming', scale=True)
    z = module.lfilter(h, [1.0], signal * np.exp(-2j * np.pi * center * n / RATE))
    first, last = IMPULSE + taps, len(signal)
    middle = (first + last) // 2
    rows = []
    for start, stop in [(first, middle), (middle, last)]:
        seg = slice(start, stop)
        t = n[seg] - (taps - 1) // 2
        if len(t) < taps or np.any(np.abs(z[seg]) == 0):
            raise ValueError('diagnostic half cannot be measured')
        phase = np.polyfit(t, np.unwrap(np.angle(z[seg])), 1)
        level = np.polyfit(t, np.log(np.abs(z[seg])), 1)
        amplitude = 2 * np.exp(level[0] * IMPULSE + level[1]
                               + 1j * (phase[0] * IMPULSE + phase[1]))
        row = encoded((center + phase[0] * RATE / (2 * np.pi), level[0], amplitude))
        if row['amplitude_magnitude'] == 0:
            raise ValueError('diagnostic zero amplitude')
        rows.append({'fit_frames_half_open': [start, stop], **row})
    return rows


def selftests(module, p0, p1):
    np = module.np
    checks = []
    def rejects(name, action):
        try:
            action()
        except (ValueError, FloatingPointError, ZeroDivisionError):
            checks.append({'name': name, 'pass': True})
        else:
            raise AssertionError(name + ' unexpectedly accepted')
    with tempfile.TemporaryDirectory(prefix='corpus-modal-data-fixtures-') as directory:
        path = Path(directory) / 'fixture.f32'
        path.write_bytes(b'\0' * (FRAMES * 8 - 8))
        rejects('short F32 rejected by exact released audio()', lambda: module.audio(path))
        samples = np.zeros((FRAMES, 2), dtype='<f4')
        samples[0, 0] = np.nan
        path.write_bytes(samples.tobytes())
        rejects('NaN prefix rejected by exact released audio()', lambda: module.audio(path))
    zero = np.zeros(FRAMES)
    rejects('zero mode unmeasurable', lambda: module.mode(zero, 1000.0, RATE, CUTOFF))
    rejects('zero reference energy rejected', lambda: module.relative_rms(zero, zero))
    n = np.arange(FRAMES) - IMPULSE
    active = n >= 0
    # Analytic measurement fixtures only, NOT a Corpus signal generator/model.
    first = {'frequency': 1000.0, 'rho': -0.0001, 'amplitude': 0.25, 'phase': 0.25}
    second = {'frequency': 4000.0, 'rho': -0.00007, 'amplitude': 0.08, 'phase': -0.4}
    def wave(tone):
        signal = np.zeros(FRAMES)
        signal[active] = tone['amplitude'] * np.exp(tone['rho'] * n[active]) * np.cos(
            2 * np.pi * tone['frequency'] * n[active] / RATE + tone['phase'])
        return signal
    def known_mode(signal, tones, target_index, center):
        tone = tones[target_index]
        taps = min(4001, int(3.3 * RATE / CUTOFF) | 1)
        g = (taps - 1) // 2
        h = module.firwin(taps, CUTOFF, fs=RATE, window='hamming', scale=True)
        j = np.arange(taps)
        def response(component, sign):
            delta = 2 * math.pi * (sign * component['frequency'] - center) / RATE
            rate = complex(component['rho'], delta)
            # G = exp((rho+i*delta)*g) sum h[j] exp(-(rho+i*delta)*j).
            return cmath.exp(rate * g) * complex(np.sum(h * np.exp(-rate * j)))
        gain = response(tone, 1)
        expected = tone['amplitude'] * cmath.exp(
            1j * (tone['phase'] - 2 * math.pi * center * IMPULSE / RATE)) * gain
        fit = module.mode(signal, center, RATE, CUTOFF)
        theta = 2 * math.pi * tone['frequency'] / RATE
        frequency_limit = tone['frequency'] * 4 * (3 * 2**-25 / theta**2 + 2**-23)
        errors = {'frequency_hz': abs(fit[0] - tone['frequency']),
                  'log_radius': abs(fit[1] - tone['rho']),
                  'complex_amplitude_ratio': abs(fit[2] / expected - 1)}
        # Bound the known conjugate-image and other-tone complex contributions
        # relative to the desired positive component across the entire fit slice.
        fit_times = [IMPULSE + taps - g - IMPULSE, FRAMES - 1 - g - IMPULSE]
        leakage_bound = 0.0
        for index, component in enumerate(tones):
            for sign in (1, -1):
                if index == target_index and sign == 1:
                    continue
                envelope_ratio = max(math.exp((component['rho'] - tone['rho']) * t)
                                     for t in fit_times)
                leakage_bound += (component['amplitude'] / tone['amplitude']
                                  * abs(response(component, sign) / gain) * envelope_ratio)
        result = {'center_hz': center, 'known_tone': tone, 'fit': encoded(fit),
                  'expected_complex_amplitude': [expected.real, expected.imag],
                  'known_FIR_response': [gain.real, gain.imag],
                  'errors': errors, 'limits': {'frequency_hz': frequency_limit,
                  'log_radius': 8 * 2**-25, 'complex_amplitude_ratio': 0.005},
                  'analytic_relative_leakage_bound': leakage_bound}
        assert errors['frequency_hz'] <= frequency_limit, json.dumps(result)
        assert errors['log_radius'] <= 8 * 2**-25, json.dumps(result)
        assert errors['complex_amplitude_ratio'] <= 0.005, json.dumps(result)
        assert leakage_bound < 0.005, json.dumps(result)
        return result, fit, expected, gain
    signal = wave(first)
    single, fit, expected, gain = known_mode(signal, [first], 0, 1005.0)
    # Preserve the earlier tighter frequency/radius sanity checks as well.
    assert abs(fit[0] - 1000.0) < 0.0001 and abs(fit[1] + 0.0001) < 1e-8
    checks.append({'name': 'known complex damped-mode response at frame4096',
                   'pass': True, 'result': single})
    g = (min(4001, int(3.3 * RATE / CUTOFF) | 1) - 1) // 2
    rate = complex(first['rho'], 2 * math.pi * (first['frequency'] - 1005.0) / RATE)
    wrong_expected = {'factor_two_error': expected * 2,
                      'missing_global_demodulation_phase': expected * cmath.exp(
                          1j * 2 * math.pi * 1005.0 * IMPULSE / RATE),
                      'missing_group_delay_factor': expected / cmath.exp(rate * g)}
    contrasts = {name: abs(fit[2] / wrong - 1) for name, wrong in wrong_expected.items()}
    assert all(error > 0.005 for error in contrasts.values()), json.dumps(contrasts)
    checks.append({'name': 'wrong amplitude/time-origin conventions rejected', 'pass': True,
                   'complex_ratio_errors': contrasts, 'unchanged_limit': 0.005})
    mixture = signal + wave(second)
    components = [known_mode(mixture, [first, second], i, center)[0]
                  for i, center in [(0, 1005.0), (1, 3995.0)]]
    target_metric = {'kind': 'modal', 'modes': [[{'center_hz': 1005.0,
                     'cutoff_hz': CUTOFF}] for unused in range(2)]}
    # A strong out-of-band nuisance can preserve target-mode recovery while the
    # existing WHOLE modal criterion correctly rejects its early waveform.
    nuisance = module.compare(np.column_stack([mixture, mixture]),
                              np.column_stack([signal, signal]), target_metric, RATE)
    wave_checks = [r for r in nuisance['measurements'] if r['check'].endswith('impulse waveform')]
    assert not nuisance['pass'] and len(wave_checks) == 2
    assert all(not r['pass'] for r in wave_checks), json.dumps(nuisance)
    checks.append({'name': 'two known modes and bounded nuisance whole-metric contrast',
                   'pass': True, 'components': components,
                   'whole_nuisance_comparison': nuisance,
                   'scope': 'Synthetic measurement controls only; no capture tolerance changed.'})
    assert 1.99 * p0[0]['center_hz'] < p1[0]['center_hz'] < 2.01 * p0[0]['center_hz']
    assert p0 != p1
    checks.append({'name': 'independently computed p0/p1 hypotheses differ', 'pass': True})
    return checks


def main():
    if sys.argv[1:] != ['--calibrate-data-once']:
        raise SystemExit('Prepared data-only calibration; Root approval required. No capture/replay/write mode.')
    config = json.loads(PROTOCOL.read_text())
    assert identity(__file__) == config['script_identity']
    watched = [str(PROTOCOL), str(Path(__file__).resolve())] + [x['path'] for x in config['pins']]
    before = {p: identity(p) for p in watched}
    for pin in config['pins']:
        assert identity(pin['path']) == {k: pin[k] for k in ('bytes', 'sha256')}, pin['path']
    p0, p1 = hypothesis(0), hypothesis(1)
    hypothetical_gap = min(b['center_hz'] - a['center_hz'] for a, b in zip(p1, p1[1:]))
    assert CUTOFF <= 0.4 * hypothetical_gap, 'Fixed100Hz navigation cutoff invalid; STOP, no alternative chosen'
    # Centers/cutoffs fixed from the hypothesis BEFORE importing/fitting any audio.
    points = [{'center_hz': r['center_hz'], 'cutoff_hz': CUTOFF} for r in p1]
    metric = {'kind': 'modal', 'modes': [points, [dict(r) for r in points]]}
    previous_bytecode_setting = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location('pinned_released_corpus_measurement', config['comparator_path'])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # Fully read definitions/imports; __main__/run never invoked.
    finally:
        sys.dont_write_bytecode = previous_bytecode_setting
    checks = selftests(module, p0, p1)
    reference = module.audio(config['note72_path'])
    wrong = module.audio(config['note60_path'])
    assert all(float(module.np.sum(reference[IMPULSE:, c] ** 2)) > 0 for c in range(2))
    assert all(float(module.np.sum(wrong[IMPULSE:, c] ** 2)) > 0 for c in range(2))
    channels = []
    for channel in range(2):
        rows = []
        for point, static in zip(points, p1):
            row = {'mode': static['mode'], 'hypothesis': static}
            try:
                full = encoded(module.mode(reference[:, channel], point['center_hz'], RATE, CUTOFF))
                relative = abs(full['frequency_hz'] - point['center_hz']) / point['center_hz']
                row.update(full_fit=full, relative_frequency_to_hypothesis=relative,
                           eligible_relative_1e_minus4=relative <= 1e-4)
            except (ValueError, FloatingPointError, ZeroDivisionError, AssertionError) as error:
                row['full_fit_error'] = repr(error)
            try:
                halves = diagnostic_halves(module, reference[:, channel], point['center_hz'])
                row['diagnostic_half_fits'] = halves
                if 'full_fit' in row:
                    differences = []
                    for h in halves:
                        ratio = complex(*h['complex_amplitude']) / complex(*full['complex_amplitude'])
                        differences.append({
                            'frequency_difference_hz': h['frequency_hz'] - full['frequency_hz'],
                            'log_radius_difference': h['log_radius_per_frame'] - full['log_radius_per_frame'],
                            'amplitude_magnitude_ratio': abs(ratio),
                            'complex_amplitude_ratio': [ratio.real, ratio.imag],
                            'complex_ratio_minus_one_magnitude': abs(ratio - 1),
                            'phase_difference_radians': cmath.phase(ratio)})
                    row['diagnostic_full_vs_halves'] = differences
            except (ValueError, FloatingPointError, ZeroDivisionError, AssertionError) as error:
                row['diagnostic_half_error'] = repr(error)
            try:
                row['wrong_note60_fit'] = encoded(module.mode(wrong[:, channel], point['center_hz'], RATE, CUTOFF))
            except (ValueError, FloatingPointError, ZeroDivisionError, AssertionError) as error:
                row['wrong_note60_fit_error'] = repr(error)
            rows.append(row)
        strongest = max((r['full_fit']['amplitude_magnitude'] for r in rows if 'full_fit' in r), default=0)
        for row in rows:
            if 'full_fit' in row and strongest > 0:
                row['relative_amplitude'] = row['full_fit']['amplitude_magnitude'] / strongest
                row['significant_relative_1e_minus3'] = row['relative_amplitude'] >= 1e-3
        significant = [r for r in rows if r.get('significant_relative_1e_minus3')]
        for row in significant:
            gaps = [abs(row['full_fit']['frequency_hz'] - other['full_fit']['frequency_hz'])
                    for other in significant if other is not row]
            row['nearest_measured_significant_gap_hz'] = min(gaps) if gaps else None
            row['fixed100_cutoff_valid_among_measured_significant'] = (
                CUTOFF <= 0.4 * min(gaps)) if gaps else None
        channels.append({'channel': channel, 'all16_mode_rows': rows,
                         'all_16_full_fits_available': all('full_fit' in r for r in rows),
                         'eligible_modes': [r['mode'] for r in rows if r.get('eligible_relative_1e_minus4')],
                         'significant_modes': [r['mode'] for r in significant],
                         'significant_gap_scope': 'Only these16 measured regular modes. Unmodeled components/bleed and missing fits do not become a complete significant-gap proof.'})
    early_wrong = [{'channel': c, 'relative_RMS': module.relative_rms(
        wrong[4096:4352, c], reference[4096:4352, c]), 'existing_limit': 0.002}
        for c in range(2)]
    comparisons = {}
    for label, value in [('note72_self', reference), ('WRONG_note60_against_note72', wrong)]:
        try:
            comparisons[label] = module.compare(value, reference, metric, RATE)
        except (ValueError, FloatingPointError, ZeroDivisionError) as error:
            comparisons[label] = {'pass': False, 'error': repr(error),
                                  'scope': 'Exact released comparison aborted as designed; no hidden replacement estimate.'}
    after = {p: identity(p) for p in watched}
    assert before == after, 'Input/script/provider changed during calibration'
    report = {'status': 'conditional data-only calibration, independent review pending; no normative adoption',
              'protocol': config, 'hypothesis_p0': p0, 'hypothesis_p1': p1,
              'fixed_navigation_metric_all16': metric,
              'hypothetical_minimum_regular_pole_gap_hz': hypothetical_gap,
              'selftests': checks, 'reference_mode_fits': channels,
              'whole_existing_modal_comparisons': comparisons,
              'wrong_note60_early_RMS_independent_of_later_fit_errors': early_wrong,
              'watch_before': before, 'watch_after_equal': True,
              'scope': 'All16 modes reported without selecting looser thresholds or silently filtering failures. Half fits describe sensitivity only. No FFT, device synthesis, original/native/candidate execution, comparator CLI/run or old model main.',
              'limitations': config['limitations'], 'grade': None, 'adopted': False}
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
