"""Decode the first instructions of tiny arm64 leaf functions in the thin Live slice (read-only; output is data).
usage: python3 -I read_words.py <Live.arm64> <vmaddr>...
Prints up to 6 words per address until RET, decoding only MOVZ/MOVK (w/x), FMOV s/d from a general register,
FMOV s/d immediate, MOVI d0 #0 and RET; anything else is printed raw as '?'. Floats decoded from the built constant."""
import struct, sys
b = open(sys.argv[1], 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]; off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24); segs.append((vm, fo, fs))
    off += size
def fo(v):
    for vm, f, fs in segs:
        if vm <= v < vm + fs: return f + v - vm
    raise SystemExit(f'unmapped {v:#x}')
def fimm8(i, dbl):
    s, e, f = i >> 7, (i >> 4) & 7, i & 15  # VFPExpandImm: exponent field bcd -> 1..4, -3..0
    return (-1) ** s * (16 + f) / 16 * 2.0 ** [1, 2, 3, 4, -3, -2, -1, 0][e]
for a in sys.argv[2:]:
    v = int(a, 16); regs = {}; out = []
    for i in range(6):
        w = struct.unpack_from('<I', b, fo(v + 4 * i))[0]
        if w == 0xd65f03c0: out.append('ret'); break
        if (w & 0x7f800000) in (0x52800000, 0x72800000):  # movz/movk w or x (sf ignored)
            rd, imm, hw = w & 31, (w >> 5) & 0xffff, (w >> 21) & 3
            prev = regs.get(rd, 0) if (w & 0x7f800000) == 0x72800000 else 0
            regs[rd] = (prev & ~(0xffff << 16 * hw)) | imm << 16 * hw
            out.append(f'mov{"k" if prev or (w & 0x7f800000) == 0x72800000 else "z"} r{rd}={regs[rd]:#x}')
        elif (w & 0xfffffc00) in (0x1e270000, 0x9e670000):  # fmov s/d, w/x
            n = (w >> 5) & 31; dbl = w & 0x80000000
            x = regs.get(n, 0) if n != 31 else 0
            val = struct.unpack('<d', struct.pack('<Q', x))[0] if dbl else struct.unpack('<f', struct.pack('<I', x & 0xffffffff))[0]
            out.append(f'fmov {"d" if dbl else "s"}{w & 31}=r{n} ({val!r})')
        elif (w & 0xff201fe0) == 0x1e201000:  # fmov s/d, #imm
            dbl = (w >> 22) & 1; out.append(f'fmov {"d" if dbl else "s"}{w & 31}=#{fimm8((w >> 13) & 0xff, dbl)!r}')
        elif w == 0x2f00e400: out.append('movi d0=#0')
        else: out.append(f'? {w:#010x}')
    print(a, '; '.join(out))
