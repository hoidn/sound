"""Write manifest.json: SHA-256 and size of every file in this evidence directory, the external inputs
(the Tension executable and its x86_64 slice, the N6 and H4 tables, the shipped presets) and the tools.

    python3 -I make_manifest.py
"""
import hashlib
import json
import platform
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cases  # noqa: E402
import tension as T  # noqa: E402
import xdevpy  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def slice_identity(path):
    b = Path(path).read_bytes()
    out = dict(path=str(path), file_sha256=hashlib.sha256(b).hexdigest())
    for i in range(struct.unpack_from('>I', b, 4)[0]):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', b, 8 + 20 * i)
        name = {0x01000007: 'x86_64', 0x0100000c: 'arm64'}[cpu]
        out.update({f'{name}_offset': off, f'{name}_size': size, f'{name}_sha256': hashlib.sha256(b[off:off + size]).hexdigest()})
    return out


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
    ext = {'bundle:Tension': slice_identity(xdevpy.BUNDLES['Tension'])}
    for rel in ('n6-device-tables-v1/out/conversions.tsv', 'h4-devices-v1/out/param_tables.json',
                't12-device-dsp-v1/harness/xdev_bind.c'):
        p = HERE.parent / rel
        ext[rel] = dict(path=str(p.resolve()), sha256=sha(p))
    for name, rel in cases.PRESETS.items():
        ext[f'preset:{name}'] = dict(path=str(T.PRESETS / rel), sha256=sha(T.PRESETS / rel))
    tools = dict(host=platform.platform(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__,
                 gcc=first_line(['gcc', '--version']), glibc=first_line(['ldd', '--version']),
                 objdump=first_line(['objdump', '--version']), loader_binary=str(xdevpy.BIN),
                 loader_sha256=sha(xdevpy.BIN) if xdevpy.BIN.exists() else None)
    m = dict(id='t12-tension-v1', created='2026-10-18', packet='T1.2 Tension device audio by extracted execution',
             regenerate='sh run.sh', tools=tools, external_inputs=ext, files=files,
             harness_changes='harness/ is a copy of t12-device-dsp-v1/harness. Only xdev_bind.c differs: integer-valued '
                             'libm results are never perturbed under XDEV_LIBM_ULP, and XDEV_LIBM_ONLY restricts the '
                             'perturbation to named functions. Neither changes an unperturbed render.',
             not_retained='Raw loader outputs, check, sweep and perturbed renders are written under '
                          '/var/tmp/sound-analysis/t12-tension/; their comparisons are in results/.')
    (HERE / 'manifest.json').write_text(json.dumps(m, indent=1) + '\n')
    print(f'{len(files)} files')


if __name__ == '__main__':
    main()
