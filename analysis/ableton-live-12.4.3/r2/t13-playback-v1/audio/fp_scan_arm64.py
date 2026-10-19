"""Classify the floating-point instructions of arm64 functions in the thin Live arm64 slice (read-only; output is data).

usage: python3 -I fp_scan_arm64.py <slice> <va-hex> <count-of-words> [...more va count pairs]
Prints each word and a class for FP data-processing encodings that matter for bit-exactness: fused multiply-add
(scalar fmadd/fmsub/fnmadd/fnmsub, vector fmla/fmls), plain fmul/fadd/fsub/fdiv (scalar s/d), conversions and
rounding. Adapted from handoff-staging/clip-launch-v1-analysis/fp_opcodes.py (single-precision and vector forms added).
"""
import struct, sys

PAT = [
    (0xFFE08000, 0x1F000000, 'FMADD s'), (0xFFE08000, 0x1F008000, 'FMSUB s'), (0xFFE08000, 0x1F200000, 'FNMADD s'),
    (0xFFE08000, 0x1F208000, 'FNMSUB s'), (0xFFE08000, 0x1F400000, 'FMADD d'), (0xFFE08000, 0x1F408000, 'FMSUB d'),
    (0xFFE08000, 0x1F600000, 'FNMADD d'), (0xFFE08000, 0x1F608000, 'FNMSUB d'),
    (0xBFA0FC00, 0x0E20CC00, 'FMLA vec'), (0xBFA0FC00, 0x0EA0CC00, 'FMLS vec'),
    (0xBF80F400, 0x0F801000, 'FMLA elem'), (0xBF80F400, 0x0F805000, 'FMLS elem'),
    (0xFFE0FC00, 0x1E200800, 'fmul s'), (0xFFE0FC00, 0x1E202800, 'fadd s'), (0xFFE0FC00, 0x1E203800, 'fsub s'),
    (0xFFE0FC00, 0x1E201800, 'fdiv s'), (0xFFE0FC00, 0x1E600800, 'fmul d'), (0xFFE0FC00, 0x1E602800, 'fadd d'),
    (0xFFE0FC00, 0x1E603800, 'fsub d'), (0xFFE0FC00, 0x1E601800, 'fdiv d'),
    (0xBFA0FC00, 0x2E20DC00, 'fmul vec'), (0xBFA0FC00, 0x0E20D400, 'fadd vec'), (0xBFA0FC00, 0x0EA0D400, 'fsub vec'),
    (0xBF80F400, 0x0F809000, 'fmul elem'), (0xBFBFFC00, 0x2E30D800, 'faddp vec'), (0xFFBFFC00, 0x7E30D800, 'faddp scalar'),
    (0xFFFFFC00, 0x1E624000, 'fcvt s,d'), (0xFFFFFC00, 0x1E22C000, 'fcvt d,s'), (0xFF3FFC00, 0x1E230000, 'ucvtf s'),
    (0xFF000000, 0x1E000000, 'other fp scalar'), (0x9F000000, 0x0E000000, 'other simd'),
]


def main():
    path, args = sys.argv[1], sys.argv[2:]
    b = open(path, 'rb').read()
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((vm, fo, fs))
        off += size
    for va, n in zip(args[0::2], args[1::2]):
        va, n = int(va, 16), int(n)
        o = next(f + va - vm for vm, f, fs in segs if vm <= va < vm + fs)
        fused = 0
        for i in range(n):
            w = struct.unpack_from('<I', b, o + 4 * i)[0]
            name = next((nm for m, p, nm in PAT if w & m == p), '')
            fused += name.startswith(('FMADD', 'FMSUB', 'FNM', 'FMLA', 'FMLS'))
            if name:
                print(f'{va + 4 * i:#x} {w:08x} {name}')
        print(f'# {va:#x} words={n} fused={fused}')


if __name__ == '__main__':
    main()
