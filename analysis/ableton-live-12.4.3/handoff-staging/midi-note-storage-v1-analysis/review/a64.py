"""Reviewer check (analyst-side): print the 32-bit words of a Mach-O arm64 image in a VA range
and decode the few instruction classes needed here (fcmp, fccmp, b.cond, b, bl, cbz/cbnz, ldr
d-register immediate, ret). Anything else prints as '?'.
usage: python3 -I a64.py <image> <lo hex> <hi hex>"""
import struct, sys
b = open(sys.argv[1], 'rb').read()
lo, hi = int(sys.argv[2], 16), int(sys.argv[3], 16)
ncmds = struct.unpack_from('<I', b, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        segs.append(struct.unpack_from('<QQQ', b, off + 24))
    off += size
def v2o(a):
    for va, vs, fo in segs:
        if va <= a < va + vs:
            return fo + a - va
COND = 'eq ne cs cc mi pl vs vc hi ls ge lt gt le al nv'.split()
def sx(v, n):
    return v - (1 << n) if v >> (n - 1) else v
def dec(a, w):
    if w & 0xff000010 == 0x54000000:
        return 'b.%s 0x%x' % (COND[w & 15], a + 4 * sx((w >> 5) & 0x7ffff, 19))
    if w & 0x7c000000 == 0x14000000:
        return ('bl' if w >> 31 else 'b') + ' 0x%x' % (a + 4 * sx(w & 0x3ffffff, 26))
    if w & 0x7e000000 == 0x34000000:
        return ('cbnz' if w >> 24 & 1 else 'cbz') + ' %s%d,0x%x' % ('x' if w >> 31 else 'w', w & 31, a + 4 * sx((w >> 5) & 0x7ffff, 19))
    if w & 0xff20fc07 == 0x1e202000:
        t = 'd' if w >> 22 & 1 else 's'
        rm = '#0.0' if w & 8 else '%s%d' % (t, w >> 16 & 31)
        return 'fcmp%s %s%d,%s' % ('e' if w & 16 else '', t, w >> 5 & 31, rm)
    if w & 0xff200c10 == 0x1e200400:
        t = 'd' if w >> 22 & 1 else 's'
        return 'fccmp %s%d,%s%d,#%d,%s' % (t, w >> 5 & 31, t, w >> 16 & 31, w & 15, COND[w >> 12 & 15])
    if w & 0xffc00000 == 0xfd400000:
        return 'ldr d%d,[x%d,#0x%x]' % (w & 31, w >> 5 & 31, (w >> 10 & 0xfff) * 8)
    if w == 0xd65f03c0:
        return 'ret'
    return '?'
for a in range(lo, hi + 1, 4):
    w = struct.unpack_from('<I', b, v2o(a))[0]
    print('0x%x %08x %s' % (a, w, dec(a, w)))
