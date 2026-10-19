"""Static slice comparison aid (analyst tool; output is data): fused multiply-add instructions per function.

Copied unchanged (except this line) from x2-mixer-v1/fp_scan.py.

usage: python3 -I -B fp_scan.py ARM64_IMAGE X86_SLICE OUT_TXT ARM:X86 ...   (hex function entries)

arm64: every scalar FP data-processing (3 source) instruction (FMADD, FMSUB, FNMADD, FNMSUB; single or
double) and every vector or by-element FMLA/FMLS in the function body, decoded from the raw words.
x86_64: every VEX FMA instruction (vfmadd/vfmsub/vfnmadd/vfnmsub) and every call to the _fma/_fmaf
stubs, from objdump. Function bodies run from the entry to the next LC_FUNCTION_STARTS entry.
Only fused operations are reported; the rest of each comparison is in x86-disasm.txt and the notes.
"""
import bisect
import re
import struct
import subprocess
import sys


def segments(data):
    ncmds, off, segs = struct.unpack_from('<I', data, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        if cmd == 0x19:
            segs.append(struct.unpack_from('<QQQQ', data, off + 24))
        off += size
    return segs


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


def arm64_fused(data, entry):
    segs, starts = segments(data), function_starts(data)
    end = starts[bisect.bisect_right(starts, entry)]
    vm, _, fo, _ = next(s for s in segs if s[0] <= entry < s[0] + s[3])
    out = []
    names = {(0, 0): 'fmadd', (0, 1): 'fmsub', (1, 0): 'fnmadd', (1, 1): 'fnmsub'}
    for a in range(entry, end, 4):
        w = struct.unpack_from('<I', data, fo + a - vm)[0]
        if w & 0xff000000 == 0x1f000000:          # FP data-processing, 3 source
            t, o1, o0 = (w >> 22) & 3, (w >> 21) & 1, (w >> 15) & 1
            r = 'sdh?'[{0: 0, 1: 1, 3: 2}.get(t, 3)]
            rd, rn, ra, rm = w & 31, (w >> 5) & 31, (w >> 10) & 31, (w >> 16) & 31
            out.append(f'{a:#x} {w:08x} {names[o1, o0]} {r}{rd},{r}{rn},{r}{rm},{r}{ra}')
        elif w & 0xbfa0fc00 in (0x0e20cc00, 0x0ea0cc00):
            out.append(f'{a:#x} {w:08x} vector {"fmls" if w >> 23 & 1 else "fmla"}')
        elif w & 0xbf80f400 in (0x0f801000, 0x0f805000):
            out.append(f'{a:#x} {w:08x} by-element {"fmls" if w >> 14 & 1 else "fmla"}')
    return end, out


def x86_fused(path, starts, entry):
    end = starts[bisect.bisect_right(starts, entry)]
    text = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', '--adjust-vma=0x100000000',
                           f'--start-address={entry:#x}', f'--stop-address={end:#x}', path],
                          capture_output=True, text=True, check=True).stdout
    hits = [ln.strip() for ln in text.splitlines() if re.search(r'\bvf(n?m(add|sub))', ln)]
    calls = [ln.strip() for ln in text.splitlines() if re.search(r'call\s+0x', ln)]
    return end, hits, calls


def main():
    arm_path, x86_path, out_path, pairs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    arm, x86 = open(arm_path, 'rb').read(), open(x86_path, 'rb').read()
    xstarts = function_starts(x86)
    fma_stubs = set()
    for line in open(sys.argv[0].replace('fp_scan.py', 'imports.txt')) if False else []:
        pass
    lines = []
    for pair in pairs:
        a, x = (int(v, 16) if v != '-' else None for v in pair.split(':'))
        if a is not None:
            end, fused = arm64_fused(arm, a)
            lines.append(f'arm64 {a:#x}..{end:#x}: {len(fused)} fused')
            lines += ['  ' + f for f in fused]
        if x is not None:
            end, hits, calls = x86_fused(x86_path, xstarts, x)
            lines.append(f'x86_64 {x:#x}..{end:#x}: {len(hits)} VEX FMA; calls: '
                         + ', '.join(c.split()[-1] for c in calls))
            lines += ['  ' + h for h in hits]
    open(out_path, 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
