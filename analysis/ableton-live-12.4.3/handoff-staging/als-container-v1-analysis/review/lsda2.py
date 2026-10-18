# Reviewer check: decode LSDA call-site/action/type tables for given function entries.
import struct, sys
path = sys.argv[1]; funcs = [int(x,16) for x in sys.argv[2:]]
b = open(path,'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off = 32; secs = {}; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off+24)
        segs.append((vmaddr, vmsize, fileoff))
        nsects = struct.unpack_from('<I', b, off+64)[0]; s = off+72
        for i in range(nsects):
            sect = b[s:s+16].rstrip(b'\0'); addr, ssize, soff = struct.unpack_from('<QQI', b, s+32)
            secs[sect] = (addr, ssize, soff); s += 80
    off += size
def v2o(a):
    for va, vs, fo in segs:
        if va <= a < va+vs: return fo + a - va
def uleb(p):
    r=s=0
    while True:
        x=b[p]; p+=1; r|=(x&0x7f)<<s; s+=7
        if x<0x80: return r,p
def sleb(p):
    r=s=0
    while True:
        x=b[p]; p+=1; r|=(x&0x7f)<<s; s+=7
        if x<0x80:
            if x&0x40: r-=1<<s
            return r,p
addr, ssize, soff = secs[b'__unwind_info']
ver, ceo, cec, peo, pec, iso, ic = struct.unpack_from('<7I', b, soff)
idx = [struct.unpack_from('<III', b, soff+iso+12*i) for i in range(ic)]
lsda = {}
for j in range((idx[-1][2]-idx[0][2])//8):
    fo, lo = struct.unpack_from('<II', b, soff+idx[0][2]+8*j); lsda[0x100000000+fo] = 0x100000000+lo
for f in funcs:
    if f not in lsda: print(hex(f), 'no LSDA'); continue
    p = v2o(lsda[f]); start = p
    lpenc = b[p]; p+=1
    if lpenc != 0xff: print('lpstart enc', lpenc); 
    ttenc = b[p]; p+=1; ttbase=None
    if ttenc != 0xff:
        tto, p = uleb(p); ttbase = p + tto
    csenc = b[p]; p+=1; cslen, p = uleb(p); csend = p+cslen
    sites=[]
    while p < csend:
        if csenc == 1:
            st,p=uleb(p); ln,p=uleb(p); lp,p=uleb(p); ac,p=uleb(p)
        else:
            st,ln,lp = struct.unpack_from('<III', b, p); p+=12; ac,p=uleb(p)
        sites.append((hex(f+st), ln, hex(f+lp) if lp else 0, ac))
    print(hex(f), 'ttenc', hex(ttenc), 'csenc', csenc, 'sites:')
    for s in sites: print('   ', s)
    acts = set(a for *_, a in sites if a)
    for a in sorted(acts):
        q = csend + a - 1; chain=[]
        while True:
            filt,q2 = sleb(q); nxt,_ = sleb(q2); chain.append(filt)
            if nxt == 0: break
            q = q2 + nxt
        print('    action', a, 'filters', chain)
        if ttbase:
            for flt in chain:
                if flt > 0:
                    size = 4 if (ttenc & 0x0f) in (3,0xb) else 8
                    ep = ttbase - flt*size
                    val = struct.unpack_from('<i' if size==4 else '<q', b, ep)[0]
                    print('      type filter', flt, 'raw', hex(val & 0xffffffffffffffff), 'enc', hex(ttenc))
