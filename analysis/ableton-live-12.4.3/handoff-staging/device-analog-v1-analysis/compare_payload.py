"""Finite audio measurements only; this file contains no instrument synthesis."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.signal import firwin, lfilter

HERE = Path(__file__).resolve().parent


def audio(path, frames):
    path = Path(path)
    if path.stat().st_size != frames*2*4:
        raise ValueError('wrong stereo binary32 byte length')
    value = np.fromfile(path, dtype='<f4').reshape(frames, 2).astype(float)
    if not np.isfinite(value).all():
        raise ValueError('non-finite sample')
    return value


def frequency(signal, center, rate):
    cutoff = min(20.0, center/4)
    taps = min(4001, int(3.3*rate/cutoff) | 1)
    if len(signal)-taps < taps:
        raise ValueError('frequency window too short')
    n = np.arange(len(signal))
    h = firwin(taps, cutoff, fs=rate, window='hamming', scale=True)
    z = lfilter(h, [1.0], signal*np.exp(-2j*np.pi*center*n/rate))[taps:]
    if np.any(np.abs(z)==0):
        raise ValueError('frequency has no measurable amplitude')
    slope = np.polyfit(n[taps:]-(taps-1)/2, np.unwrap(np.angle(z)), 1)[0]
    result = center+slope*rate/(2*np.pi)
    if not math.isfinite(result) or result<=0:
        raise ValueError('frequency is not measurable')
    return float(result)


def harmonic_fit(signal, center, rate, count):
    n = np.arange(len(signal))/rate
    columns = []
    for k in range(1, count+1):
        columns += [np.cos(2*np.pi*k*center*n), np.sin(2*np.pi*k*center*n)]
    columns.append(np.ones(len(signal)))
    coefficients = np.linalg.lstsq(np.stack(columns, axis=1), signal, rcond=None)[0]
    amplitudes = np.hypot(coefficients[:-1:2], coefficients[1:-1:2])
    return amplitudes, float(coefficients[-1])


def compare(value, reference, metric, rate):
    measurements = []

    def limit(name, error, tolerance):
        error, tolerance = float(error), float(tolerance)
        if not math.isfinite(error):
            raise ValueError(name+': non-finite measurement')
        measurements.append({'check':name, 'error':error, 'tolerance':tolerance, 'pass':bool(error<=tolerance)})

    for channel in range(2):
        y, r = value[:,channel], reference[:,channel]
        label = 'left' if channel==0 else 'right'
        nz = np.flatnonzero(y!=0)
        if not len(nz):
            raise ValueError(label+': silent output')
        limit(label+' first nonzero frame', abs(int(nz[0])-metric['first_nonzero']), 0)
        if metric['last_nonzero'] is not None:
            limit(label+' final nonzero frame', abs(int(nz[-1])-metric['last_nonzero']), 1)
        for start, stop in metric['onset_windows']:
            power = float(np.sum(r[start:stop]**2))
            if power<=0:
                raise ValueError('reference onset has zero energy')
            limit(f'{label} onset {start}', math.sqrt(float(np.sum((y[start:stop]-r[start:stop])**2))/power), 0.005)
        win = rate//100
        number = len(r)//win
        rr = np.sqrt(np.mean(r[:number*win].reshape(number, win)**2, axis=1))
        yy = np.sqrt(np.mean(y[:number*win].reshape(number, win)**2, axis=1))
        threshold = float(rr.max())*0.001
        for i in np.flatnonzero(rr>=threshold):
            if yy[i]<=0:
                raise ValueError('candidate envelope window is silent')
            limit(f'{label} envelope {int(i)}', abs(20*math.log10(yy[i]/rr[i])), 0.05)
        for point in metric['steady_windows']:
            start, stop, center = point['start_frame'], point['stop_frame'], point['center_hz']
            if point['frequency_graded']:
                fy, fr = [frequency(s[start:stop], center, rate) for s in (y,r)]
                limit(f'{label} frequency {start}', abs(fy/fr-1), 1e-5)
            ay, dy = harmonic_fit(y[start:stop], center, rate, point['harmonic_count'])
            ar, dr = harmonic_fit(r[start:stop], center, rate, point['harmonic_count'])
            for k in point['graded_harmonics']:
                if ay[k-1]<=0 or ar[k-1]<=0:
                    raise ValueError('a required harmonic cannot be measured')
                limit(f'{label} harmonic {k} at {start}', abs(20*math.log10(ay[k-1]/ar[k-1])), 0.05)
            limit(f'{label} DC at {start}', abs(dy-dr), float(np.max(np.abs(r[start:stop])))*0.001)
    return {'pass':all(x['pass'] for x in measurements), 'measurements':measurements}


def run(directory):
    results = []
    for case in json.loads((HERE/'cases.json').read_text())['cases']:
        for evaluation in case['evaluations']:
            try:
                candidate = audio(Path(directory)/(evaluation['id']+'.f32'), evaluation['frames'])
                reference = audio(HERE/evaluation['reference'], evaluation['frames'])
                result = compare(candidate,reference,evaluation['metric'],evaluation['sample_rate_hz'])
            except (OSError, ValueError, FloatingPointError, ZeroDivisionError) as error:
                result = {'pass':False,'error':str(error)}
            results.append({'id':evaluation['id'],**result})
    return {'pass':bool(results) and all(x['pass'] for x in results), 'results':results}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate_directory',type=Path)
    args=parser.parse_args()
    report=run(args.candidate_directory)
    print(json.dumps(report,indent=1,allow_nan=False))
    raise SystemExit(0 if report['pass'] else 1)
