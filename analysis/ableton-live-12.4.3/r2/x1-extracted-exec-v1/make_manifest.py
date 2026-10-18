"""Write manifest.json: SHA-256 of the evidence files, harness sources, built loader and slice; tool versions."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
from xexec import BIN, SLICE  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]


files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
         if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
manifest = {
    'id': 'X1-EXTRACTED-EXEC-V1',
    'packet': 'X1 extracted-execution pilot (ADR 0003, evidence label X)',
    'target': 'Ableton Live 12 Suite 12.4.3, Live x86_64 slice',
    'slice': {'path': SLICE, 'sha256': sha(SLICE), 'image_base': '0x100000000',
              'note': 'x86_64 slice of Contents/MacOS/Live; see helpers slice.json for the fat-file offset'},
    'harness': {'tools/xexec/xexec.c': sha(ROOT / 'tools/xexec/xexec.c'),
                'tools/xexec/xexec.py': sha(ROOT / 'tools/xexec/xexec.py'),
                'built_loader': {'path': str(BIN), 'sha256': sha(BIN)}},
    'tools': {'gcc': first_line(['gcc', '--version']), 'gdb': first_line(['gdb', '--version']),
              'objdump': first_line(['objdump', '--version']), 'python': platform.python_version(),
              'glibc': platform.libc_ver()[1], 'kernel': platform.release()},
    'commands': ['sh run.sh'],
    'executed_live_application': False,
    'executed_original_code': 'x86_64 functions listed in addresses.json, in the xexec harness on Linux x86_64',
    'inputs': {f'handoff/{h}/cases.json': sha(ROOT / 'handoff' / h / 'cases.json')
               for h in ('mixer-values-v1', 'midi-config-v3', 'transport-state-v1')},
    'files': files,
}
(HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
print(f'manifest.json: {len(files)} files')
