"""Electric (LoungeLizard) render protocol: host values, presets, scripts, WAV output.

    import el
    host = el.host_values(el.CONSTRUCTOR)              # stored values -> 33 host values (index -> float)
    y, log = el.render(host, [(0, 0x90, 60, 100), (22050, 0x80, 60, 0)], 44100, 'raw/x')   # writes raw/x.wav

Protocol of every reference render (REQ-DEVICE-ELECTRIC-001): CreateInstanceU; SetSampleRateU(fs);
all 33 host values in index order; WARM[fs] frames of processing with no events (output discarded);
then the case's events, at frames counted from the end of the warm-up, processed in host blocks of
512 frames, input flag 0, transport {0, 0.0, 120.0}. The warm-up is a whole number of host blocks and
of the device's 1 ms control periods, so render frame 0 is a block start and a control-grid point.
Dependencies: numpy, xdevpy (the loader driver in this directory), the app bundle.
"""
import csv
import gzip
import re
import struct
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import xdevpy  # noqa: E402

N5 = HERE.parent / 'n5-device-mapping-v1' / 'out' / 'conversions.tsv'
PRESETS = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library/Devices/Instruments/Electric')
DEFAULTS_PRESET = PRESETS.parent.parent.parent / 'Defaults' / 'Instruments' / 'Electric.adv'
WARM = {44100: 11264, 48000: 12288}           # 22 * 512 = 256 * 44; 24 * 512 = 256 * 48
BLOCK = 512
SCRATCH = Path('/var/tmp/sound-analysis/t12-electric')

# Host index -> stored parameter name (N5 table; index 32 is Live's runtime DummyPerNotePitchBendRange).
NAMES = ['Polyphony', 'PitchBendRange', 'Volume', 'KeyboardFineTune', 'MalletStiffness', 'MalletStiffnessKeyboard',
         'MalletStiffnessVelocity', 'MalletForceStrength', 'MalletForceKeyboard', 'MalletForceVelocity', 'MalletNoisePitch',
         'MalletNoiseDecay', 'MalletNoiseAmount', 'MalletNoiseKeyboardScaling', 'ForkReleaseTime', 'ForkTineDecay',
         'ForkTineVolume', 'ForkTineKeyboardScaling', 'ForkTineColor', 'ForkToneBarDecay', 'ForkToneBarVolume',
         'PickupSymmetry', 'PickupDistance', 'PickupModel', 'PickupAmpIn', 'PickupAmpOut', 'PickupAmpKeyboardScaling',
         'DamperTone', 'DamperAmount', 'DamperBalance', 'KeyboardTranspose', 'KeyboardStretch', None]
INDEX = {n: i for i, n in enumerate(NAMES) if n}


def _n5_rows():
    rows = [r for r in csv.DictReader(N5.open(), delimiter='\t') if r['device'] == 'LoungeLizard' and r['index']]
    assert [r['stored_name'] for r in rows][:32] == NAMES[:32], 'N5 index order changed'
    return rows


def constructor_values():
    """Stored values of a new Electric without a preset (SPEC-BUNDLED-DEVICE-PARAMETERS "Default when
    absent"). Volume is the constructor's binary32 0x3f346d11 = 0.7047892213 (N5 prints it rounded)."""
    vals = {r['stored_name']: float(r['default']) for r in _n5_rows()[:32]}
    vals['Volume'] = struct.unpack('<f', struct.pack('<I', 0x3f346d11))[0]
    return vals


CONSTRUCTOR = constructor_values()
DOMAIN = {n: (0.0, 30.0) if n == 'Polyphony' else (0.0, 1.0) if n == 'PickupModel' else (0.0, 24.0) if n == 'KeyboardTranspose'
          else (0.0, 1.0) for n in NAMES if n}


def f32(x):
    return float(np.float32(x))


def host_values(stored):
    """Stored values (name -> number) -> {index: host value}, as N5 traces Live's conversion (S):
    clamp to the domain; Polyphony and PickupModel pass their index; KeyboardTranspose is rounded to
    the nearest 1/32768 and truncated toward zero; every other value passes unchanged as binary32;
    index 32 is always 48."""
    out = {}
    for i, n in enumerate(NAMES):
        if n is None:
            out[i] = 48.0
            continue
        lo, hi = DOMAIN[n]
        v = min(max(float(stored[n]), lo), hi)
        if n in ('Polyphony', 'PickupModel'):
            v = float(int(v))
        elif n == 'KeyboardTranspose':
            v = float(int(round(v * 32768) / 32768))
        out[i] = f32(v)
    return out


def read_preset(path):
    """Stored Manual values of a LoungeLizard preset (.adv, gzip XML) -> name -> float."""
    text = gzip.decompress(Path(path).read_bytes()).decode()
    body = text[text.index('<LoungeLizard'):]
    vals = {}
    for n in NAMES[:32]:
        m = re.search(rf'<{n}>\s*<LomId Value="\d+" />\s*<Manual Value="([^"]+)" />', body)
        if not m:
            raise ValueError(f'{path.name}: no {n}')
        vals[n] = float(m.group(1))
    return vals


def presets():
    """Shipped Electric presets, name -> stored values, plus 'Defaults' (the Defaults preset)."""
    out = {p.stem: read_preset(p) for p in sorted(PRESETS.rglob('*.adv')) if not p.name.startswith('._')}
    out['Defaults'] = read_preset(DEFAULTS_PRESET)
    return out


def script(host, events, fs, frames, block=BLOCK, warm=None, extra=()):
    """Loader script. events: (frame, status, d1, d2) with frames counted from render frame 0.
    extra: (frame, 'param I V' or 'reset') commands applied between blocks at that render frame
    (must be a multiple of block)."""
    warm = WARM[fs] if warm is None else warm
    lines = ['create', f'rate {fs}'] + [f'param {i} {v!r}' for i, v in sorted(host.items())]
    lines += [f'event {warm + f} {s:#x} {a} {b}' for f, s, a, b in events]
    lines += ['inflag 0', 'input zero']
    if warm:
        lines.append(f'process {warm} {block}')
    t = 0
    for f, cmd in sorted(extra):
        assert f % block == 0 and f >= t
        if f > t:
            lines.append(f'process {f - t} {block}')
            t = f
        lines.append(cmd)
    lines += [f'process {frames - t} {block}', 'destroy']
    return lines


def write_wav(path, x, fs):
    """Mono IEEE-float 32-bit WAV."""
    x = np.asarray(x, '<f4')
    data = x.tobytes()
    hdr = b'RIFF' + struct.pack('<I', 36 + len(data)) + b'WAVE' + b'fmt ' + struct.pack('<IHHIIHH', 16, 3, 1, fs, 4 * fs, 4, 32)
    Path(path).write_bytes(hdr + b'data' + struct.pack('<I', len(data)) + data)


def read_wav(path):
    b = Path(path).read_bytes()
    assert b[:4] == b'RIFF' and b[36:40] == b'data'
    return np.frombuffer(b[44:], '<f4').astype(float), struct.unpack_from('<I', b, 24)[0]


def render(host, events, fs, name, frames, env=None, block=BLOCK, warm=None, extra=(), script_path=None):
    """Run one render in a fresh process. Returns (left channel after the warm-up, as float64; log).
    Asserts that the warm-up output is exactly zero and that both channels are bit-identical.
    The stereo binary32 output goes to SCRATCH/name.f32; the script to script_path (default scratch)."""
    lines = script(host, events, fs, frames, block, warm, extra)
    w = WARM[fs] if warm is None else warm
    SCRATCH.mkdir(parents=True, exist_ok=True)
    out = SCRATCH / f'{name}.f32'
    y, log = xdevpy.render('Electric', lines, out, script_path=script_path or SCRATCH / f'{name}.script', env=env)
    assert not np.any(y[:w]), 'warm-up output not silent'
    assert np.array_equal(y[:, 0].view(np.uint32), y[:, 1].view(np.uint32)), 'channels differ'
    return y[w:, 0].astype(float), log


def note(n, v=100, on=0, dur=13230):
    return [(on, 0x90, n, v), (on + dur, 0x80, n, 0)]
