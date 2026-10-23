"""Driver for the xdev bundle loader (harness/): build it, run one script per process, read the render.

    from xdevpy import render, BUNDLES
    y, log = render('Corpus', ['create', 'rate 44100', 'process 512 512'], 'raw/x.f32')

Each run is a fresh process (20 s timeout). The output file holds interleaved stereo binary32 frames;
the log is the loader's stdout plus stderr. Dependencies: gcc, numpy, the app bundle at APP.
Environment: XDEV_BIN overrides the loader path (default /var/tmp/sound-analysis/t12-collision/xdev).
"""
import hashlib
import os
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
APP = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac')
BUNDLES = {n: APP / f'{n}.bundle/Contents/MacOS/{e}' for n, e in
           (('Corpus', 'Corpus'), ('Analog', 'Analog'), ('Tension', 'Tension'), ('Collision', 'Collision'),
            ('Electric', 'Electric'), ('Amp', 'Amplifier'), ('Cabinet', 'Cabinet'))}
BIN = Path(os.environ.get('XDEV_BIN', '/var/tmp/sound-analysis/t12-collision/xdev'))
SOURCES = ['xdev.c', 'xdev_load.c', 'xdev_bind.c', 'xdev_cxx.c']
CFLAGS = ['-O1', '-g', '-Wall', '-Wextra', '-Wno-missing-field-initializers', '-no-pie']


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build():
    """Compile harness/*.c into BIN (always: the build is part of the evidence)."""
    BIN.parent.mkdir(parents=True, exist_ok=True)
    src = [str(HERE / 'harness' / s) for s in SOURCES]
    subprocess.run(['gcc', *CFLAGS, '-o', str(BIN), *src, '-ldl', '-lm'], check=True)
    return BIN


class RunError(RuntimeError):
    pass


def render(device, lines, out_path, script_path=None, imports=False, env=None):
    """Run one script in a fresh process. Returns (frames x 2 float32 array, log text).
    env adds environment variables (XDEV_LIBM_ULP=+1/-1: the libm sensitivity mode).
    Raises RunError on a trap, fault, timeout or non-zero exit, with the log attached."""
    out_path = Path(out_path)
    script_path = Path(script_path or out_path.with_suffix('.script'))
    script_path.write_text('\n'.join(lines) + '\n')
    argv = [str(BIN), str(BUNDLES[device]), str(script_path), str(out_path)] + (['--imports'] if imports else [])
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=20, env={**os.environ, **(env or {})})
    except subprocess.TimeoutExpired as e:
        raise RunError(f'timeout: {out_path.name}') from e
    log = p.stdout + p.stderr
    if p.returncode != 0:
        raise RunError(f'{out_path.name}: exit {p.returncode}\n{log[-2000:]}')
    return np.fromfile(out_path, np.float32).reshape(-1, 2), log


def used_imports(log):
    """{symbol: calls} from the loader's 'used' lines."""
    return {f[1]: int(f[2]) for f in (l.split() for l in log.splitlines()) if len(f) == 3 and f[0] == 'used'}
