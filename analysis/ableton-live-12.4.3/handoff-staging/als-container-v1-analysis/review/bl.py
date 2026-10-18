# Reviewer check: list BL/BLR/B/RET instructions in an address range (AArch64), resolving BL targets.
import struct, sys
path = sys.argv[1]; lo = int(sys.argv[2],16); hi = int(sys.argv[3],16)
b = open(path,'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off+24); segs.append((vmaddr, vmsize, fileoff))
    off += size
def v2o(a):
    for va, vs, fo in segs:
        if va <= a < va+vs: return fo + a - va
a = lo
while a < hi:
    w = struct.unpack_from('<I', b, v2o(a))[0]
    op = ''
    if w & 0xfc000000 == 0x94000000:
        imm = w & 0x3ffffff
        if imm & 0x2000000: imm -= 1 << 26
        op = 'bl %s' % hex(a + imm*4)
    elif w & 0xfc000000 == 0x14000000:
        imm = w & 0x3ffffff
        if imm & 0x2000000: imm -= 1 << 26
        op = 'b %s' % hex(a + imm*4)
    elif w & 0xfffffc1f == 0xd63f0000: op = 'blr x%d' % ((w>>5)&31)
    elif w & 0xfffffc1f == 0xd61f0000: op = 'br x%d' % ((w>>5)&31)
    elif w == 0xd65f03c0 or w & 0xfffffbff == 0xd65f0bff: op = 'ret'
    elif w & 0x7f000000 == 0x34000000 or w & 0x7f000000 == 0x35000000: op = 'cbz/cbnz'
    elif w & 0xff000010 == 0x54000000: op = 'b.cond %s' % hex(a + (((w>>5)&0x7ffff) - (1<<19 if (w>>23)&1 else 0))*4)
    elif w & 0xffc00000 == 0x39000000: op = 'strb w%d,[x%d,#%s]' % (w&31, (w>>5)&31, hex((w>>10)&0xfff))
    elif w & 0xffc00000 == 0x39400000: op = 'ldrb w%d,[x%d,#%s]' % (w&31, (w>>5)&31, hex((w>>10)&0xfff))
    elif w & 0xffc00000 == 0xf9400000: op = 'ldr x%d,[x%d,#%s]' % (w&31, (w>>5)&31, hex(((w>>10)&0xfff)*8))
    elif w & 0xffc00000 == 0xf9000000: op = 'str x%d,[x%d,#%s]' % (w&31, (w>>5)&31, hex(((w>>10)&0xfff)*8))
    elif w & 0xff800000 == 0x91000000: op = 'add x%d,x%d,#%s' % (w&31, (w>>5)&31, hex((w>>10)&0xfff))
    elif w & 0xffe0ffe0 == 0xaa0003e0: op = 'mov x%d,x%d' % (w&31, (w>>16)&31)
    print(hex(a), '%08x' % w, op)
    a += 4
