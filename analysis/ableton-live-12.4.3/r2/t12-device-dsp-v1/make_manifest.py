"""Write manifest.json: SHA-256 and size of every file in this evidence directory, the external
inputs (bundle executables with their x86_64 slices, the N5/N6 tables, the port page) and the tools.

    python3 -I make_manifest.py
"""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe_others  # noqa: E402
import xdevpy  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or r.stderr).splitlines()[0]
    except (OSError, IndexError):
        return 'unavailable'


def main():
    import numpy
    import scipy
    files = {str(p.relative_to(HERE)): dict(sha256=sha(p), bytes=p.stat().st_size)
             for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name != 'manifest.json'}
    ext = {f'bundle:{n}': dict(path=str(p), **probe_others.slice_identity(p)) for n, p in xdevpy.BUNDLES.items()}
    for rel in ('n5-device-mapping-v1/out/conversions.tsv', 'n6-device-tables-v1/out/conversions.tsv',
                'corpus-dsp-v1/tables.py', '../demos/corpus-traced/index.html'):
        p = HERE.parent / rel
        ext[rel] = dict(path=str(p.resolve()), sha256=sha(p))
    tools = dict(host=platform.platform(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__,
                 gcc=first_line(['gcc', '--version']), glibc=first_line(['ldd', '--version']), node=first_line(['node', '--version']),
                 objdump=first_line(['objdump', '--version']), loader_binary=str(xdevpy.BIN),
                 loader_sha256=sha(xdevpy.BIN) if xdevpy.BIN.exists() else None)
    m = dict(id='t12-device-dsp-v1', created='2026-10-18', packet='T1.2 feasibility gate (device audio by extracted execution)',
             regenerate='sh run.sh', tools=tools, external_inputs=ext, files=files,
             not_retained='Determinism re-runs, block-size and MXCSR variants, libm-perturbed renders, sweeps and port renders are '
                          'written under /var/tmp/sound-analysis/t12-xdev/; their SHA-256 and comparisons are in results/.')
    (HERE / 'manifest.json').write_text(json.dumps(m, indent=1) + '\n')
    print(f'{len(files)} files')


if __name__ == '__main__':
    main()
