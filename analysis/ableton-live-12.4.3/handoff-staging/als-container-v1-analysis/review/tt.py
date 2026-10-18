# Reviewer check: resolve the catch type of filter 1 in the LSDA of a function to a typeinfo address.
import struct, sys
path = sys.argv[1]; f = int(sys.argv[2],16)
b = open(path,'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]; off = 32; segs = []; secs = {}
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off+24); segs.append((vmaddr, vmsize, fileoff))
        nsects = struct.unpack_from('<I', b, off+64)[0]; s = off+72
        for i in range(nsects):
            sect = b[s:s+16].rstrip(b'\0'); addr, ssize, soff = struct.unpack_from('<QQI', b, s+32); secs[sect]=(addr,ssize,soff); s+=80
    off += size
def v2o(a):
    for va, vs, fo in segs:
        if va <= a < va+vs: return fo + a - va
def o2v(o):
    for va, vs, fo in segs:
        if fo <= o < fo+vs: return va + o - fo
def uleb(p):
    r=s=0
    while True:
        x=b[p]; p+=1; r|=(x&0x7f)<<s; s+=7
        if x<0x80: return r,p
addr, ssize, soff = secs[b'__unwind_info']
ver, ceo, cec, peo, pec, iso, ic = struct.unpack_from('<7I', b, soff)
idx = [struct.unpack_from('<III', b, soff+iso+12*i) for i in range(ic)]
lsda = {}
for j in range((idx[-1][2]-idx[0][2])//8):
    fo, lo = struct.unpack_from('<II', b, soff+idx[0][2]+8*j); lsda[0x100000000+fo] = 0x100000000+lo
p = v2o(lsda[f]); p += 1; ttenc = b[p]; p += 1; tto, p = uleb(p); ttbase = p + tto
for flt in (1, 2):
    ep = ttbase - 4*flt
    rel = struct.unpack_from('<i', b, ep)[0]
    if rel == 0: print('filter', flt, 'catch-all'); continue
    slot = o2v(ep) + rel
    raw = struct.unpack_from('<Q', b, v2o(slot))[0]
    print('filter', flt, 'GOT slot', hex(slot), 'raw', hex(raw), 'bind' if raw >> 63 else 'rebase target(low36)+base', hex(0x100000000 + (raw & 0xfffffffff)))
