"""Write manifest.json: SHA-256 of the evidence files, the X2 loader copy and its build, the slice; tool versions."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
from xexec import BIN, SLICE  # noqa: E402  (X2 copy)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]


files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
         if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
manifest = {
    'id': 'X2-TRANSPORT-V1',
    'packet': 'X2 transport state by extracted execution (ADR 0003, evidence label X)',
    'target': 'Ableton Live 12 Suite 12.4.3, Live x86_64 slice; arm64 equivalence by static comparison only',
    'spec': 'SPEC-TRANSPORT-STATE r2 -> r3',
    'slice': {'path': SLICE, 'sha256': sha(SLICE), 'image_base': '0x100000000'},
    'harness': {'base': {'tools/xexec/xexec.c': sha(ROOT / 'tools/xexec/xexec.c'),
                         'tools/xexec/xexec.py': sha(ROOT / 'tools/xexec/xexec.py')},
                'x2_copy_changes': ['xexec.c: _strtod bound to glibc strtod', 'xexec.c: mk command', 'xexec.c: ptrs: argument',
                                    'xexec.py: default loader path'],
                'built_loader': {'path': str(BIN), 'sha256': sha(BIN)}},
    'tools': {'gcc': first_line(['gcc', '--version']), 'gdb': first_line(['gdb', '--version']),
              'objdump': first_line(['objdump', '--version']), 'python': platform.python_version(),
              'glibc': platform.libc_ver()[1], 'kernel': platform.release()},
    'commands': ['sh run.sh'],
    'executed_live_application': False,
    'executed_original_code': 'x86_64 functions listed in addresses.json, in the X2 loader copy on Linux x86_64',
    'files': files,
}
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(f'manifest.json: {len(files)} files')
