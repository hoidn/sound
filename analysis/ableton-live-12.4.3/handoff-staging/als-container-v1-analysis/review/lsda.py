# Reviewer check: which functions in a range have an LSDA (landing pads) per __unwind_info.
import struct, sys
path = sys.argv[1]; lo = int(sys.argv[2], 16); hi = int(sys.argv[3], 16)
b = open(path, 'rb').read()
magic, cpu, sub, ftype, ncmds, sizeofcmds, flags, _ = struct.unpack_from('<IiiIIIII', b, 0)
assert magic == 0xfeedfacf, hex(magic)
off = 32; base = None; uw = None
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        segname = b[off+8:off+24].rstrip(b'\0')
        vmaddr, vmsize, fileoff, filesize, maxp, initp, nsects, fl = struct.unpack_from('<QQQQiiII', b, off+24)
        if segname == b'__TEXT': base = vmaddr
        s = off + 72
        for i in range(nsects):
            sect = b[s:s+16].rstrip(b'\0'); seg = b[s+16:s+32].rstrip(b'\0')
            addr, ssize, soff = struct.unpack_from('<QQI', b, s+32)
            if sect == b'__unwind_info': uw = (addr, ssize, soff)
            s += 80
    off += size
addr, ssize, soff = uw
ver, ceo, cec, peo, pec, iso, ic = struct.unpack_from('<7I', b, soff)
lsda = {}
idx = [struct.unpack_from('<III', b, soff + iso + 12*i) for i in range(ic)]
first = idx[0][2]; last = idx[-1][2]
for j in range((last - first)//8):
    fo, lo2 = struct.unpack_from('<II', b, soff + first + 8*j)
    lsda[fo] = lo2
print('base', hex(base), 'lsda entries', len(lsda))
for fo in sorted(lsda):
    a = base + fo
    if lo <= a <= hi: print(hex(a), 'LSDA at', hex(base + lsda[fo]))
