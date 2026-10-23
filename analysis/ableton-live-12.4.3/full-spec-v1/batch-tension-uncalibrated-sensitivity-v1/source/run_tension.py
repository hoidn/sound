"""Render every case of cases.py through the Tension x86_64 slice and retain it.

    python3 -I run_tension.py        # writes raw/<case>.wav, raw/<case>.script, results/runs.json

Each render is one fresh loader process (xdevpy.render). The retained file is IEEE-float 32-bit WAV at
the case's rate: mono when the two output channels are bit-identical, else stereo. runs.json records
the SHA-256 of the WAV and of the loader's raw output (interleaved stereo binary32), whether the
channels are identical, the bound imports called and the per-block flag summary. The raw output is
written to /var/tmp/sound-analysis/t12-tension/raw and not retained. Four renders run in parallel.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
from scipy.io import wavfile  # noqa: E402

import cases  # noqa: E402
import tension as T  # noqa: E402
import xdevpy  # noqa: E402

RAW = HERE / 'raw'
SCRATCH = Path('/var/tmp/sound-analysis/t12-tension/raw')


def render_case(name):
    c = cases.CASES[name]
    lines = cases.script(c)
    y, log = T.render(lines, SCRATCH / f'{name}.f32', env=None)
    (RAW / f'{name}.script').write_text('\n'.join(lines) + '\n')
    same = bool(np.array_equal(y[:, 0].view(np.uint32), y[:, 1].view(np.uint32)))
    wavfile.write(RAW / f'{name}.wav', c['fs'], y[:, 0].copy() if same else y.copy())
    return name, dict(wav_sha256=xdevpy.sha256(RAW / f'{name}.wav'), raw_f32_sha256=xdevpy.sha256(SCRATCH / f'{name}.f32'),
                      channels_identical=same, frames=int(len(y)), fs=c['fs'], group=c['group'], changes=c['changes'],
                      preset=c['preset'], events=c['events'], imports=xdevpy.used_imports(log),
                      process=next(l for l in log.splitlines() if l.startswith('process')))


def load(name):
    """Reference render as (frames, 2) float64."""
    fs, y = wavfile.read(RAW / f'{name}.wav')
    y = y.astype(float)
    return np.stack([y, y], 1) if y.ndim == 1 else y


def main():
    xdevpy.build()
    RAW.mkdir(exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(4) as ex:
        runs = dict(ex.map(render_case, cases.CASES))
    out = dict(bundle=str(xdevpy.BUNDLES['Tension']), bundle_sha256=xdevpy.sha256(xdevpy.BUNDLES['Tension']),
               n6_conversions_sha256=xdevpy.sha256(T.N6), protocol='create; rate; all 129 host values in index order; events; '
               'inflag 0; input zero; process frames in blocks of 512; destroy', runs=runs)
    (HERE / 'results' / 'runs.json').write_text(json.dumps(out, indent=1))
    print(len(runs), 'renders;', sum(r['channels_identical'] for r in runs.values()), 'mono')


if __name__ == '__main__':
    main()
