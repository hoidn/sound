"""Read-only static reads of the x86_64 Live slice (analyst tool; output is data).

usage: python3 -I xtool.py ptrs <va> <count>        8-byte words (plain VAs: the slice has no chained fixups)
       python3 -I xtool.py consts <va> <fmt>        typed constants, e.g. <4d or <2f
       python3 -I xtool.py dis <va> [<end>]         objdump of one function (end from LC_FUNCTION_STARTS)
Slice: XEXEC_SLICE or the default path of tools/xexec/xexec.py. Depends on objdump.
"""
import bisect
import os
import struct
import subprocess
import sys

SLICE = os.environ.get('XEXEC_SLICE', '/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64')


def segments(b):
    off, segs = 32, []
    for _ in range(struct.unpack_from('<I', b, 16)[0]):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((vm, fs, fo))
        off += size
    return segs


def fileoff(b, va):
    return next(fo + va - vm for vm, fs, fo in segments(b) if vm <= va < vm + fs)


def function_starts(b):
    ncmds, off = struct.unpack_from('<I', b, 16)[0], 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x26:
            fo, fs = struct.unpack_from('<II', b, off + 8)
            starts, addr, p = [], 0x100000000, fo
            while p < fo + fs and b[p]:
                v = sh = 0
                while True:
                    c = b[p]; p += 1; v |= (c & 0x7f) << sh; sh += 7
                    if not c & 0x80:
                        break
                addr += v
                starts.append(addr)
            return starts
        off += size


def dis(va, end=None):
    if end is None:
        b = open(SLICE, 'rb').read()
        s = function_starts(b)
        end = s[bisect.bisect_right(s, va)]
    p = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', '--adjust-vma=0x100000000',
                        f'--start-address={va:#x}', f'--stop-address={end:#x}', SLICE],
                       capture_output=True, text=True, check=True)
    return f'### {va:#x} .. {end:#x}\n' + p.stdout.split('<.data+', 1)[-1].split('\n', 1)[-1]


if __name__ == '__main__':
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == 'dis':
        print(dis(int(a[0], 16), int(a[1], 16) if len(a) > 1 else None), end='')
    else:
        b = open(SLICE, 'rb').read()
        va = int(a[0], 16)
        o = fileoff(b, va)
        if cmd == 'ptrs':
            for i in range(int(a[1], 0)):
                print(f'{va + 8 * i:#x} +{8 * i:#05x} {struct.unpack_from("<Q", b, o + 8 * i)[0]:#x}')
        else:
            raw = b[o:o + struct.calcsize(a[1])]
            print(f'{va:#x} {a[1]} {raw.hex()} {struct.unpack(a[1], raw)}')
