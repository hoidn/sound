"""Write x86-disasm.txt (objdump of every Live x86_64 function run) and manifest.json (SHA-256s).

usage: python3 -I -B make_evidence.py            (run after run_mix.py)
Copied from x2-mixer-v1/make_evidence.py; the address list, ids and notes changed.
"""
import bisect
import hashlib
import json
import platform
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'harness'))
from xexec import BIN, SLICE  # noqa: E402

ENGINE = '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64'
ARM64 = HERE.parents[1] / 'derived' / 'Live.arm64'
ADDRS = json.loads((HERE / 'addresses.json').read_text())['run']


def function_starts(data):
    ncmds, off = struct.unpack_from('<I', data, 16)[0], 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        if cmd == 0x26:
            fo, fs = struct.unpack_from('<II', data, off + 8)
            starts, addr, p = [], 0x100000000, fo
            while p < fo + fs and data[p]:
                v = sh = 0
                while True:
                    b = data[p]; p += 1; v |= (b & 0x7f) << sh; sh += 7
                    if not b & 0x80:
                        break
                addr += v
                starts.append(addr)
            return starts
        off += size
    raise ValueError('no LC_FUNCTION_STARTS')


def disassemble(path, addrs):
    starts, out = function_starts(open(path, 'rb').read()), []
    for a in sorted(addrs):
        end = starts[bisect.bisect_right(starts, a)]
        out.append(f'### {a:#x} .. {end:#x}\n')
        p = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64',
                            '--adjust-vma=0x100000000', f'--start-address={a:#x}',
                            f'--stop-address={end:#x}', path], capture_output=True, text=True, check=True)
        out.append(p.stdout.split('\n', 7)[-1])
    return ''.join(out)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def first_line(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[0]


def main():
    (HERE / 'x86-disasm.txt').write_text(disassemble(SLICE, [int(r['live_x86'], 16) for r in ADDRS]))
    files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
             if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    manifest = {
        'id': 'T14-MIX-V1',
        'packet': 'T1.4 mix graph and automation in playback: static tracing of the x86_64 Ableton Live '
                  'Engine (named) and both Live slices, plus extracted execution (ADR 0003, label X)',
        'target': 'Ableton Live 12 Suite 12.4.3; Live x86_64 slice for X runs',
        'slices': {'live_x86_64': {'path': SLICE, 'sha256': sha(SLICE), 'image_base': '0x100000000'},
                   'engine_x86_64': {'path': ENGINE, 'sha256': sha(ENGINE), 'image_base': '0x0',
                                     'note': 'static only (symbol donor); not executed'},
                   'live_arm64': {'path': str(ARM64.relative_to(HERE.parents[3])), 'sha256': sha(ARM64),
                                  'image_base': '0x100000000', 'note': 'static comparison only (fma-scan.txt)'}},
        'harness': {'harness/xexec.c': sha(HERE / 'harness/xexec.c'),
                    'harness/xexec.py': sha(HERE / 'harness/xexec.py'),
                    'built_loader': {'path': str(BIN), 'sha256': sha(BIN)},
                    'note': 'xexec.c is an unchanged copy of x2-mixer-v1/harness/xexec.c (poke command, '
                            '--patch, 256-call check); xexec.py changes only BIN; tools/xexec was not modified'},
        'tools': {'gcc': first_line(['gcc', '--version']), 'objdump': first_line(['objdump', '--version']),
                  'python': platform.python_version(), 'glibc': platform.libc_ver()[1],
                  'kernel': platform.release()},
        'commands': ['sh run.sh'],
        'executed_live_application': False,
        'executed_original_code': 'Live x86_64 functions listed in addresses.json "run", in the xexec harness',
        'static_notes': ['notes-mix.txt', 'notes-solo.txt', 'notes-automation.txt', 'notes-q019.txt'],
        'files': files,
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    print(f'x86-disasm.txt and manifest.json written ({len(files)} files)')


if __name__ == '__main__':
    main()
