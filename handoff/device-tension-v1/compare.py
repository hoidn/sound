"""Finite audio measurements only; no instrument synthesis."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.signal import firwin, lfilter

HERE = Path(__file__).resolve().parent


def audio(path, frames):
    path = Path(path)
    if frames <= 0 or path.stat().st_size != frames*4:
        raise ValueError('expected exactly the specified mono binary32 frame count')
    value = np.fromfile(path, '<f4').astype(np.float64)
    if not np.isfinite(value).all():
        raise ValueError('non-finite sample')
    return value


def partial(signal, center, cutoff, start, stop, rate):
    taps = min(4001, int(3.3*rate/cutoff) | 1)
    n = np.arange(stop)
    time = n[start+taps:]-(taps-1)//2
    if len(time) < taps:
        raise ValueError('partial window is too short')
    kernel = firwin(taps, cutoff, fs=rate, window='hamming', scale=True)
    z = lfilter(kernel, [1.0], signal[:stop]*np.exp(-2j*np.pi*center*n/rate))[start+taps:]
    if np.any(np.abs(z) == 0):
        raise ValueError('partial has no measurable magnitude')
    phase = np.polyfit(time, np.unwrap(np.angle(z)), 1)
    level = np.polyfit(time, np.log(np.abs(z)), 1)
    result = (center+phase[0]*rate/(2*np.pi), level[0],
              2*np.exp(level[0]*start+level[1]+1j*(phase[0]*start+phase[1])))
    if not all(np.isfinite(x) for x in result) or result[1] == 0 or result[2] == 0:
        raise ValueError('partial estimate is missing or non-finite')
    return result


def compare(value, reference, metric, rate):
    if value.ndim != 1 or reference.ndim != 1 or not len(value) or value.shape != reference.shape:
        raise ValueError('expected nonempty matching mono arrays')
    if not np.isfinite(value).all() or not np.isfinite(reference).all():
        raise ValueError('non-finite sample')
    if metric['kind'] not in ('stable', 'repeated-strike') or not metric['waveform_windows']:
        raise ValueError('missing comparison requirements')
    if metric['kind'] == 'stable' and not metric['partials']:
        raise ValueError('required stable partial list is empty')
    checks, failures = 0, []

    def check(name, error, bound):
        nonlocal checks
        checks += 1
        if not math.isfinite(float(error)) or error > bound:
            failures.append(name)

    on = metric['onset_frame']
    found = np.flatnonzero(value)
    if not len(found):
        raise ValueError('required sounding output is silent')
    check('exact onset', abs(int(found[0])-on), 0)
    for start, stop, tolerance, label in metric['waveform_windows']:
        if not 0 <= start < stop <= len(reference):
            raise ValueError('empty or invalid waveform window')
        power = float(np.sum(reference[start:stop]**2))
        if power <= 0 or not math.isfinite(power):
            raise ValueError('reference waveform denominator is zero')
        error = math.sqrt(float(np.sum((value[start:stop]-reference[start:stop])**2))/power)
        check(label, error, tolerance)
    for index, mode in enumerate(metric['partials']):
        args = (mode['center_hz'], metric['partial_cutoff_hz'], *metric['partial_window'], rate)
        frequency, radius, amplitude = partial(value, *args)
        fref, rref, aref = partial(reference, *args)
        check(f'partial {index+1} frequency', abs(frequency/fref-1), 2e-6)
        check(f'partial {index+1} log radius', abs(radius/rref-1), 6e-4)
        check(f'partial {index+1} complex amplitude', abs(amplitude-aref)/metric['amplitude_normalizer'], 5e-4)
    return {'pass': not failures, 'checks': checks, 'failures': failures}


def run(directory):
    reports = []
    for case in json.loads((HERE/'cases.json').read_text())['cases']:
        for e in case['evaluations']:
            try:
                value = audio(Path(directory)/(e['id']+'.f32'), e['frames'])
                reference = audio(HERE/e['reference'], e['frames'])
                result = compare(value, reference, e['metric'], e['sample_rate_hz'])
            except (OSError, ValueError, FloatingPointError, ZeroDivisionError) as error:
                result = {'pass': False, 'error': str(error)}
            reports.append({'id': e['id'], **result})
    return {'pass': bool(reports) and all(r['pass'] for r in reports), 'results': reports}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate_directory', type=Path)
    report = run(parser.parse_args().candidate_directory)
    print(json.dumps(report, indent=1, allow_nan=False))
    raise SystemExit(0 if report['pass'] else 1)
