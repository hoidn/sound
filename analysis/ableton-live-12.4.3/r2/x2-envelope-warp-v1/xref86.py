"""Find RIP-relative references (disp32 operands) to given VAs in the x86_64 slice's __text (output is data).

usage: python3 -I xref86.py <slice> <va>...
Scans every byte offset for a REX.W 8B/8D (mov/lea r64, [rip+disp32]) or F2/F3/66 0F 10/28/59/5C/58
(movsd/movss/movapd/mulsd/subsd/addsd xmm, [rip+disp32]) whose target equals a given VA, and prints the
instruction address and the function start from LC_FUNCTION_STARTS. Heuristic; confirm with objdump.
"""
import bisect, struct, sys


def main():
    b = open(sys.argv[1], 'rb').read()
    targets = {int(x, 16) for x in sys.argv[2:]}
    ncmds, off = struct.unpack_from('<I', b, 16)[0], 32
    text = starts = None
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            nsect = struct.unpack_from('<I', b, off + 64)[0]
            for k in range(nsect):
                s = off + 72 + 80 * k
                if b[s:s + 16].rstrip(b'\0') == b'__text':
                    addr, sz, fo = struct.unpack_from('<QQI', b, s + 32)
                    text = (addr, sz, fo)
        if cmd == 0x26:
            fo, fs = struct.unpack_from('<II', b, off + 8)
            starts, a, p = [], 0x100000000, fo
            while p < fo + fs and b[p]:
                v = sh = 0
                while True:
                    c = b[p]; p += 1; v |= (c & 0x7f) << sh; sh += 7
                    if not c & 0x80:
                        break
                a += v; starts.append(a)
        off += size
    addr, sz, fo = text
    for i in range(fo, fo + sz - 8):
        c0, c1, c2 = b[i], b[i + 1], b[i + 2]
        n = None
        if c0 in (0x48, 0x4c) and c1 in (0x8b, 0x8d) and (c2 & 0xc7) == 0x05:
            n = 3
        elif c0 in (0xf2, 0xf3, 0x66) and c1 == 0x0f and b[i + 2] in (0x10, 0x28, 0x59, 0x5c, 0x58, 0x5e) and (b[i + 3] & 0xc7) == 0x05:
            n = 4
        if n:
            va = addr + i - fo
            tgt = va + n + 4 + struct.unpack_from('<i', b, i + n)[0]
            if tgt in targets:
                f = starts[bisect.bisect_right(starts, va) - 1]
                print(f'{tgt:#x} referenced at {va:#x} in function {f:#x}')


if __name__ == '__main__':
    main()
