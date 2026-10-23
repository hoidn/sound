"""Finite signal measurements only; this module does not synthesize audio."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.signal import firwin, lfilter

HERE = Path(__file__).resolve().parent


def audio(path, frames):
    path = Path(path)
    if path.stat().st_size != frames * 4:
        raise ValueError('expected exactly the specified number of mono binary32 frames')
    value = np.fromfile(path, '<f4').astype(np.float64)
    if not np.isfinite(value).all():
        raise ValueError('non-finite sample')
    return value


def measure(value, evaluation):
    rate = evaluation['sample_rate_hz']
    metric = evaluation['metric']
    found = np.flatnonzero(value)
    if metric['kind'] == 'silence':
        return {'silent': not len(found)}
    if not len(found):
        raise ValueError('required sounding output is silent')
    hop = rate // 100
    count = len(value) // hop
    envelope = 20 * np.log10(np.sqrt(np.mean(value[:count*hop].reshape(count, hop)**2, axis=1)) + 1e-30)
    bands = []
    for start in metric['band_start_frames']:
        segment = value[start:start+4096]
        if len(segment) != 4096:
            raise ValueError('incomplete spectral window')
        spectrum = np.abs(np.fft.rfft(segment * np.hanning(4096)))**2
        hz = np.fft.rfftfreq(4096, 1/rate)
        bands.append([10*math.log10(float(spectrum[(hz >= c*2**(-1/6)) & (hz < c*2**(1/6))].sum())+1e-30)
                      for c in metric['band_centres_hz']])
    result = {'onset_frame': int(found[0]), 'envelope_db': envelope.tolist(), 'bands_db': bands}
    if metric['partials']:
        stop = metric['partial_stop_frame']
        start = metric['partial_start_frame']
        center = metric['fundamental_center_hz']
        cutoff = min(20.0, center/4)
        taps = min(4001, int(3.3*rate/cutoff) | 1)
        n = np.arange(stop)
        time = n[start+taps:] - (taps-1)//2
        if len(time) < taps:
            raise ValueError('partial measurement window is too short')
        kernel = firwin(taps, cutoff, fs=rate, window='hamming', scale=True)
        points = []
        for harmonic in metric['partials']:
            z = lfilter(kernel, [1.0], value[:stop]*np.exp(-2j*np.pi*center*harmonic*n/rate))[start+taps:]
            if np.any(np.abs(z) == 0):
                raise ValueError('required partial is unmeasurable')
            phase = np.polyfit(time, np.unwrap(np.angle(z)), 1)
            level = np.polyfit(time, np.log(np.abs(z)), 1)
            amplitude = 2*np.exp(level[0]*start+level[1])
            points.append({'harmonic': harmonic, 'frequency_hz': float(center*harmonic+phase[0]*rate/(2*np.pi)),
                           'amplitude_db': float(20*np.log10(amplitude+1e-30)),
                           'decay_db_per_second': float(level[0]*rate*20/np.log(10))})
        result['partials'] = points
    return result


def compare(value, evaluation):
    metric = evaluation['metric']
    expected = evaluation['expected_measurements']
    actual = measure(value, evaluation)
    if metric['kind'] == 'silence':
        return {'pass': actual['silent'], 'checks': 1, 'failures': [] if actual['silent'] else ['exact silence']}
    failures = []
    checks = 0

    def check(name, error, bound):
        nonlocal checks
        checks += 1
        if not math.isfinite(float(error)) or error > bound:
            failures.append(name)

    check('onset lower bound', metric['onset_min_frame']-actual['onset_frame'], 0)
    check('onset upper bound', actual['onset_frame']-metric['onset_max_frame'], 0)
    for index in metric['graded']['env']:
        check('envelope '+str(index), abs(actual['envelope_db'][index]-expected['envelope_db'][index]), metric['tolerances']['env'])
    for window, indices in enumerate(metric['graded']['bands']):
        for index in indices:
            check(f'band {window}/{index}', abs(actual['bands_db'][window][index]-expected['bands_db'][window][index]), metric['tolerances']['bands'])
    if metric['partials']:
        reference = {p['harmonic']: p for p in expected['partials']}
        theta = 2*np.pi*metric['fundamental_center_hz']/evaluation['sample_rate_hz']
        frequency_bound = 4*(3*2**-25/theta**2+2**-23)
        for point in actual['partials']:
            k = point['harmonic']
            r = reference[k]
            for field, mask, tolerance in [('amplitude_db', 'amp', 'amp'), ('decay_db_per_second', 'decay', 'decay')]:
                if k-1 in metric['graded'][mask]:
                    check(f'partial {k} '+field, abs(point[field]-r[field]), metric['tolerances'][tolerance])
            if k-1 in metric['graded']['freq']:
                check(f'partial {k} frequency', abs(point['frequency_hz']/r['frequency_hz']-1), frequency_bound)
    return {'pass': not failures, 'checks': checks, 'failures': failures}


def run(directory):
    reports = []
    for case in json.loads((HERE/'cases.json').read_text())['cases']:
        for evaluation in case['evaluations']:
            try:
                value = audio(Path(directory)/(evaluation['id']+'.f32'), evaluation['frames'])
                result = compare(value, evaluation)
            except (OSError, ValueError, FloatingPointError, ZeroDivisionError) as error:
                result = {'pass': False, 'error': str(error)}
            reports.append({'id': evaluation['id'], **result})
    return {'pass': bool(reports) and all(r['pass'] for r in reports), 'results': reports}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate_directory', type=Path)
    report = run(parser.parse_args().candidate_directory)
    print(json.dumps(report, indent=1, allow_nan=False))
    raise SystemExit(0 if report['pass'] else 1)
