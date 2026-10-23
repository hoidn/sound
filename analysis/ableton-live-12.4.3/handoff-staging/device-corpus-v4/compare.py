"""Measure candidate audio against the finite reference outputs; no audio synthesis."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.signal import firwin, lfilter

HERE = Path(__file__).resolve().parent
FRAMES = 16384


def audio(path):
    path = Path(path)
    if path.stat().st_size != FRAMES * 2 * 4:
        raise ValueError(f'{path.name}: expected exactly {FRAMES} stereo frames')
    data = np.fromfile(path, dtype='<f4').reshape(FRAMES, 2).astype(np.float64)
    if not np.isfinite(data).all():
        raise ValueError(f'{path.name}: non-finite sample')
    return data


def relative_rms(value, reference):
    power = float(np.sum(reference ** 2))
    if power == 0:
        raise ValueError('reference has zero energy in a relative comparison')
    return math.sqrt(float(np.sum((value - reference) ** 2)) / power)


def mode(signal, center, rate, cutoff):
    taps = min(4001, int(3.3 * rate / cutoff) | 1)
    n = np.arange(len(signal))
    h = firwin(taps, cutoff, fs=rate, window='hamming', scale=True)
    z = lfilter(h, [1.0], signal * np.exp(-2j * np.pi * center * n / rate))
    seg = slice(4096 + taps, len(signal))
    t = n[seg] - (taps - 1) // 2
    if len(t) < taps or np.any(np.abs(z[seg]) == 0):
        raise ValueError('mode cannot be measured')
    phase = np.polyfit(t, np.unwrap(np.angle(z[seg])), 1)
    level = np.polyfit(t, np.log(np.abs(z[seg])), 1)
    amplitude = 2 * np.exp(level[0] * 4096 + level[1] + 1j * (phase[0] * 4096 + phase[1]))
    result = (center + phase[0] * rate / (2 * np.pi), level[0], amplitude)
    if not all(np.isfinite(x) for x in result) or amplitude == 0:
        raise ValueError('mode has no finite measurable amplitude')
    return result


def compare(value, reference, metric, rate):
    measured = []

    def limit(name, error, tolerance):
        error = float(error)
        if not math.isfinite(error):
            raise ValueError(f'{name}: non-finite error')
        measured.append({'check': name, 'error': error, 'tolerance': float(tolerance), 'pass': bool(error <= tolerance)})

    kind = metric['kind']
    for channel in range(2):
        y, r = value[:, channel], reference[:, channel]
        label = 'left' if channel == 0 else 'right'
        if kind == 'modal':
            limit(label + ' impulse waveform', relative_rms(y[4096:4352], r[4096:4352]), 0.002)
            for i, point in enumerate(metric['modes'][channel]):
                center, cutoff = point['center_hz'], point['cutoff_hz']
                fy, ry, ay = mode(y, center, rate, cutoff)
                fr, rr, ar = mode(r, center, rate, cutoff)
                theta = 2 * np.pi * fr / rate
                limit(f'{label} mode {i+1} frequency Hz', abs(fy-fr), fr * 4 * (3 * 2**-25 / theta**2 + 2**-23))
                limit(f'{label} mode {i+1} log radius', abs(ry-rr), 8 * 2**-25)
                limit(f'{label} mode {i+1} complex amplitude', abs(ay/ar-1), 0.005)
        elif kind == 'sine':
            n = np.arange(8192, FRAMES)
            f = metric['frequency_hz']
            basis = np.stack([np.sin(2*np.pi*f*n/rate), np.cos(2*np.pi*f*n/rate)], axis=1)
            a, b = [np.linalg.lstsq(basis, s[8192:], rcond=None)[0] for s in (y, r)]
            ratio = complex(*a) / complex(*b)
            if ratio == 0:
                raise ValueError('sine has no measurable gain')
            limit(label + ' gain dB', abs(20 * math.log10(abs(ratio))), 0.01)
            limit(label + ' phase degrees', abs(np.angle(ratio) * 180 / np.pi), 0.5)
        elif kind in ('waveform', 'filter'):
            start = metric['start_frame']
            limit(label + ' waveform', relative_rms(y[start:], r[start:]), 0.0001)
        elif kind == 'ramp_waveform':
            post_y = [float(v) for v in y[4096:]]
            post_r = [float(v) for v in r[4096:]]
            ref_energy = math.fsum(v * v for v in post_r)
            candidate_energy = math.fsum(v * v for v in post_y)
            if ref_energy <= 0 or candidate_energy <= 0:
                raise ValueError('Ramp requires positive energy in both channels')
            error_energy = math.fsum((a - b) * (a - b) for a, b in zip(post_y, post_r))
            limit(label + ' Ramp waveform', math.sqrt(error_energy / ref_energy), 0.01)
        elif kind == 'noteoff_decay_zero_waveform':
            post_y = [float(v) for v in y[4096:]]
            post_r = [float(v) for v in r[4096:]]
            ref_energy = math.fsum(v * v for v in post_r)
            candidate_energy = math.fsum(v * v for v in post_y)
            if ref_energy <= 0 or candidate_energy <= 0:
                raise ValueError('NoteOff zero endpoint requires positive energy in both channels')
            error_energy = math.fsum((a - b) * (a - b) for a, b in zip(post_y, post_r))
            limit(label + ' NoteOff zero endpoint waveform', math.sqrt(error_energy / ref_energy), 0.01)
        elif kind == 'startup':
            limit(label + ' floor before frame 100', float(np.max(np.abs(y[:100]))), 1e-18)
            limit(label + ' onset at frame 100', 0 if abs(y[100]) > 1e-18 else 1, 0)
            limit(label + ' rising gain frames 100 through 199', relative_rms(y[100:200], r[100:200]), 0.0001)
            limit(label + ' settled gain from frame 199', relative_rms(y[199:], r[199:]), 0.0001)
        elif kind == 'lfo':
            n = np.arange(FRAMES)
            h = firwin(801, 80, fs=rate, window='hamming', scale=True)
            zy, zr = [lfilter(h, [1.0], s * np.exp(-2j*np.pi*261.62*n/rate)) for s in (y, r)]
            for t in range(5296, FRAMES-600, 1000):
                k = t+400
                estimates = []
                for z in (zy, zr):
                    segment = z[k-100:k+101]
                    if np.any(np.abs(segment) == 0):
                        raise ValueError('LFO fundamental cannot be measured')
                    estimates.append(np.diff(np.unwrap(np.angle(segment))).mean()*rate/(2*np.pi)+261.62)
                limit(f'{label} LFO frame {t}', abs(estimates[0]-estimates[1]), 0.2)
        elif kind != 'noise':
            raise ValueError('unknown metric kind')
        if kind in ('noise', 'filter'):
            window = np.hanning(8192)
            Y, R = [np.fft.rfft(s[8192:] * window) for s in (y, r)]
            hz = np.fft.rfftfreq(8192, 1/rate)
            for exponent in range(-11, 13):
                lower = 1000 * 2.0**(exponent/3)
                bins = (hz >= lower) & (hz < lower * 2.0**(1/3))
                power_y, power_r = [float(np.sum(np.abs(s[bins])**2)) for s in (Y, R)]
                if power_y <= 0 or power_r <= 0 or bins.sum() < 4:
                    raise ValueError('third-octave band cannot be measured')
                limit(f'{label} band {exponent} dB', abs(10*math.log10(power_y/power_r)), 0.01)
    return {'pass': all(x['pass'] for x in measured), 'measurements': measured}


def run(candidate_directory):
    results = []
    cases = json.loads((HERE/'cases.json').read_text())['cases']
    for case in cases:
        for evaluation in case['evaluations']:
            name = evaluation['id']
            try:
                candidate = audio(Path(candidate_directory)/(name+'.f32'))
                reference = audio(HERE/evaluation['reference'])
                if evaluation['metric']['kind'] == 'ramp_waveform':
                    raw_reference = (HERE/evaluation['reference']).read_bytes()
                    if hashlib.sha256(raw_reference).hexdigest() != '40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec':
                        raise ValueError('Ramp reference hash differs from the pinned capture')
                if evaluation['metric']['kind'] == 'noteoff_decay_zero_waveform':
                    raw_reference = (HERE/evaluation['reference']).read_bytes()
                    if hashlib.sha256(raw_reference).hexdigest() != 'a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829':
                        raise ValueError('NoteOff zero endpoint reference hash differs from the pinned capture')
                result = compare(candidate, reference, evaluation['metric'], evaluation['sample_rate_hz'])
            except (OSError, ValueError, FloatingPointError, ZeroDivisionError) as error:
                result = {'pass': False, 'error': str(error)}
            results.append({'id': name, **result})
    return {'pass': bool(results) and all(x['pass'] for x in results), 'results': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate_directory', type=Path)
    args = parser.parse_args()
    report = run(args.candidate_directory)
    print(json.dumps(report, indent=1, allow_nan=False))
    raise SystemExit(0 if report['pass'] else 1)
