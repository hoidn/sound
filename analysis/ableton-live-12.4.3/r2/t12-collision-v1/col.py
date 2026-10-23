"""Shared definitions for the Collision renders: host parameter sets, scripts and measurements.

    from col import PRESET, idx, script, render, onset, f0
    y, log = render('Collision', script({**PRESET, idx('Mallet/Stiffness'): 0.2}, note(60, 100)), out)

Host values (SetParameterA index -> value) follow the N6 table
(../n6-device-tables-v1/out/conversions.tsv, column sent_for_default): CTOR is what Live sends
for a Collision built from its constructor defaults, PRESET the same with the one sent value the
shipped Defaults preset changes (Resonator1/OnOff true; PerNotePitchBendRange is not sent).
Instruments get no audio input (input flag 0); events are {frame, status, d1, d2} at absolute
output frames; the transport is {0, 0.0, 120.0}. Dependencies: numpy, scipy, xdevpy (this dir).
"""
import csv
from pathlib import Path

import numpy as np

import xdevpy

HERE = Path(__file__).resolve().parent
N6 = HERE.parent / 'n6-device-tables-v1' / 'out' / 'conversions.tsv'
ROWS = [r for r in csv.DictReader(N6.open(), delimiter='\t') if r['device'] == 'Collision' and r['index']]
NAME = {int(r['index']): r['stored_name'] for r in ROWS}
INDEX = {v: k for k, v in NAME.items()}
FS = 44100
DEFAULTS_ADV = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library/Defaults/Instruments/Collision.adv')


def idx(name):
    return INDEX[name]


def P(**kw):
    """PRESET with overrides given as stored names, '/' written as '__' (Mallet__Stiffness=0.2)."""
    return {**PRESET, **{idx(k.replace('__', '/')): float(v) for k, v in kw.items()}}


def note(n=60, v=100, on=4096, dur=22050):
    return [(on, 0x90, n, v), (on + dur, 0x80, n, 0)] if dur is not None else [(on, 0x90, n, v)]


def script(params, events, fs=FS, frames=44100, block=512, pre=(), post=(), mxcsr=None):
    lines = ['create', f'rate {fs}'] + [f'param {i} {v!r}' for i, v in sorted(params.items())] + list(pre)
    lines += [f'event {f} {s:#x} {a} {b}' for f, s, a, b in events]
    if mxcsr:
        lines.append(f'mxcsr {mxcsr:#x}')
    return lines + ['inflag 0', 'input zero', f'process {frames} {block}'] + list(post) + ['destroy']


def render(lines, out, env=None):
    return xdevpy.render('Collision', lines, out, env=env)


def onset(y, thr=0.0):
    k = np.nonzero(np.abs(y).max(1) > thr)[0]
    return int(k[0]) if len(k) else None


def last_above(y, thr=1e-6):
    k = np.nonzero(np.abs(y).max(1) > thr)[0]
    return int(k[-1]) if len(k) else None


def peak_hz(x, fs=FS, lo_hz=20.0, nfft=1 << 20):
    """Frequency of the largest spectral peak (Hann window, parabolic interpolation in log magnitude)."""
    x = np.asarray(x, float)
    s = np.abs(np.fft.rfft(x * np.hanning(len(x)), nfft)) + 1e-300
    hz = np.fft.rfftfreq(nfft, 1 / fs)
    k = int(np.argmax(np.where(hz > lo_hz, s, 0)))
    a, b, c = np.log(s[k - 1:k + 2])
    return float(hz[k] + 0.5 * (a - c) / (a - 2 * b + c) * fs / nfft)


def t60(x, fs=FS, start=0, floor_db=-60.0):
    """Time (s) for the RMS envelope (1024-frame windows) to fall 60 dB below its maximum, by a line fit
    from -5 dB to -35 dB below that maximum, extrapolated to -60."""
    x = np.asarray(x, float)[start:]
    w = 1024
    e = np.array([np.sqrt((x[i:i + w] ** 2).mean()) for i in range(0, len(x) - w, w // 4)]) + 1e-30
    db = 20 * np.log10(e / e.max())
    k0 = int(np.argmax(db))
    sel = [i for i in range(k0, len(db)) if -35 <= db[i] <= -5]
    if len(sel) < 3:
        return None
    t = np.array(sel) * (w // 4) / fs
    m = np.polyfit(t, db[sel], 1)[0]
    return float(floor_db / m)


# ---- stored document values -> host values (N6 conversions; positions per hypothesis) ----
POSITIONS = {f'Resonator{r}/{p}' for r in (1, 2) for p in ('HitX', 'ListeningXL', 'ListeningXR')}
BY_NAME = {r['stored_name']: r for r in ROWS}


def _lo_hi(r):
    lo, hi = r['internal_range'].split('..')
    return float(lo), float(hi)


def stored_to_host(stored, positions='identity'):
    """{stored name: value} (absent names keep the constructor default) -> {index: host value}.
    positions='identity' passes the six position parameters unchanged (N5/N6 traced chain, A1);
    'bipolar' passes 2v - 1 (the untraced rescale that the bundle's -2..2 range would suggest)."""
    host = {int(r['index']): float(r['sent_for_default']) for r in ROWS}   # replaced below for every stored row
    for name, v in {**CTOR_STORED, **stored}.items():
        r = BY_NAME.get(name)
        if r is None or not r['index']:
            continue
        i, conv, mode = int(r['index']), r['user_converter'], r['mode']
        lo, hi = _lo_hi(r)
        v = float(v)
        if conv in ('bool', 'enum'):
            x = float(int(v))
        else:
            x = min(max(v, lo), hi)
            if conv.startswith('legacyint'):
                x = float(int(round(x * 32768) / 32768))
        if mode.startswith('MultiplyOffset'):
            x = 1.0 - x
        elif mode.startswith('IntegerMapping'):
            table = [int(t) for t in mode.split('table=')[1].split(',')]
            x = float(table[int(x)])
        if name in POSITIONS and positions == 'bipolar':
            x = 2 * x - 1
        host[i] = x
    for i, r in ((int(r['index']), r) for r in ROWS):         # mode 8: x 0.125 when the paired target is 4 or 9
        if r['mode'] == 'CollisionScaledMode' and host[i - 1] in (4.0, 9.0):
            host[i] = host[i] * 0.125
    return host


CTOR_STORED = {r['stored_name']: float(r['default']) for r in ROWS if not r['stored_name'].startswith('Dummy')}


def read_adv(path):
    """{stored name: Manual value} of the Collision element of a preset (.adv, gzip XML)."""
    import gzip
    import xml.etree.ElementTree as ET
    root = ET.fromstring(gzip.open(path).read())
    col = root.find('Collision')
    out = {}

    def walk(e, prefix):
        for c in e:
            m = c.find('Manual')
            if m is not None and 'Value' in m.attrib:
                v = m.get('Value')
                out[prefix + c.tag] = 1.0 if v == 'true' else 0.0 if v == 'false' else float(v)
            elif len(c) and c.tag not in ('AutomationTarget', 'ModulationTarget', 'MidiControllerRange', 'LomId', 'Pointee'):
                walk(c, prefix + c.tag + '/')
    walk(col, '')
    return out


CTOR = stored_to_host({})                         # constructor defaults, as Live sends them
PRESET = stored_to_host(read_adv(DEFAULTS_ADV))   # the shipped Defaults preset
assert sorted(CTOR) == list(range(139))
_f32 = lambda d: {i: float(np.float32(v)) for i, v in d.items()}
assert {i for i in CTOR if _f32(CTOR)[i] != _f32(PRESET)[i]} == {INDEX["Resonator1/OnOff"]}, sorted((i, CTOR[i], PRESET[i]) for i in CTOR if CTOR[i] != PRESET[i])
