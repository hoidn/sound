# Reviewer check: decode a few AArch64 instruction kinds in an address range of the thin arm64 Live slice
# (read-only; output is data). Kinds: bl, ldr/str x imm, add imm, adrp (with resolved page), movz/movk,
# orr-register mov, ldr literal-free. Anything else prints as raw.
# usage: python3 -I dis_site.py <Live.arm64> <from_hex> <to_hex>
import struct, sys
path = sys.argv[1]; lo = int(sys.argv[2], 16); hi = int(sys.argv[3], 16)
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24); segs.append((vmaddr, vmsize, fileoff))
    off += size
def v2o(a):
    for va, vs, fo in segs:
        if va <= a < va + vs: return fo + a - va
def sx(v, bits): return v - (1 << bits) if v >> (bits - 1) & 1 else v
a = lo
while a < hi:
    w = struct.unpack_from('<I', b, v2o(a))[0]; rd = w & 31; rn = (w >> 5) & 31; op = ''
    if w & 0xfc000000 == 0x94000000: op = 'bl %s' % hex(a + sx(w & 0x3ffffff, 26) * 4)
    elif w & 0x9f000000 == 0x90000000:
        imm = sx(((w >> 5) & 0x7ffff) << 2 | (w >> 29) & 3, 21); op = 'adrp x%d,%s' % (rd, hex((a & ~0xfff) + (imm << 12)))
    elif w & 0x7f800000 == 0x11000000: op = 'add %s%d,%s%d,#%s' % ('xw'[w >> 31 ^ 1], rd, 'xw'[w >> 31 ^ 1], rn, hex((w >> 10) & 0xfff << (12 if w >> 22 & 1 else 0)))
    elif w & 0xffc00000 == 0xf9400000: op = 'ldr x%d,[x%d,#%s]' % (rd, rn, hex(((w >> 10) & 0xfff) * 8))
    elif w & 0xffc00000 == 0xf9000000: op = 'str x%d,[x%d,#%s]' % (rd, rn, hex(((w >> 10) & 0xfff) * 8))
    elif w & 0x7f800000 == 0x52800000: op = 'movz %s%d,#%s,lsl %d' % ('xw'[w >> 31 ^ 1], rd, hex((w >> 5) & 0xffff), ((w >> 21) & 3) * 16)
    elif w & 0x7f800000 == 0x72800000: op = 'movk %s%d,#%s,lsl %d' % ('xw'[w >> 31 ^ 1], rd, hex((w >> 5) & 0xffff), ((w >> 21) & 3) * 16)
    elif w & 0x7fe0ffe0 == 0x2a0003e0: op = 'mov %s%d,%s%d' % ('xw'[w >> 31 ^ 1], rd, 'xw'[w >> 31 ^ 1], (w >> 16) & 31)
    print(hex(a), '%08x' % w, op)
    a += 4
