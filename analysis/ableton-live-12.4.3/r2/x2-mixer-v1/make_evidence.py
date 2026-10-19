"""Write x86-disasm.txt (objdump of every function run or compared) and manifest.json (SHA-256s).

usage: python3 -I -B make_evidence.py            (run after run_mixer.py)
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
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE / 'harness'))
from xexec import BIN, SLICE  # noqa: E402

ADDRS = [0x101aecd40, 0x101aec640, 0x101aec510, 0x101aecbd0, 0x101aecc90, 0x101aed3a0, 0x101aed490,
         0x101b719e0, 0x101b1a470, 0x101b1a550, 0x101b1a630, 0x101b1a6f0, 0x101b1a7b0, 0x101b1a880,
         0x101b1a8e0, 0x101b191e0, 0x101b198c0, 0x1014353b0]


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
    (HERE / 'x86-disasm.txt').write_text(disassemble(SLICE, ADDRS))
    files = {str(p.relative_to(HERE)): sha(p) for p in sorted(HERE.rglob('*'))
             if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    manifest = {
        'id': 'X2-MIXER-V1',
        'packet': 'X2 extracted execution: mixer fader curves, pan law, crossfade curves (ADR 0003, label X)',
        'target': 'Ableton Live 12 Suite 12.4.3, Live x86_64 slice',
        'slice': {'path': SLICE, 'sha256': sha(SLICE), 'image_base': '0x100000000'},
        'harness': {'harness/xexec.c': sha(HERE / 'harness/xexec.c'),
                    'harness/xexec.py': sha(HERE / 'harness/xexec.py'),
                    'built_loader': {'path': str(BIN), 'sha256': sha(BIN)},
                    'note': 'copy of tools/xexec with a poke command and an --patch allocator option; '
                            'tools/xexec was not modified'},
        'tools': {'gcc': first_line(['gcc', '--version']), 'objdump': first_line(['objdump', '--version']),
                  'python': platform.python_version(), 'glibc': platform.libc_ver()[1],
                  'kernel': platform.release()},
        'commands': ['sh run.sh'],
        'executed_live_application': False,
        'executed_original_code': 'x86_64 functions listed in addresses.json, in the xexec harness on Linux x86_64',
        'files': files,
    }
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    print(f'x86-disasm.txt and manifest.json written ({len(files)} files)')


if __name__ == '__main__':
    main()
