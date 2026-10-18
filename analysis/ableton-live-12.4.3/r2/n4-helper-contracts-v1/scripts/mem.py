# usage: mem.py <va> <n> [ptrs|str|hex|wstr]  -- read Live.arm64 bytes at a VA via segment map
import sys, struct
D=open('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64','rb').read()
ncmds=struct.unpack_from('<I',D,16)[0]; p=32; segs=[]
for _ in range(ncmds):
    cmd,sz=struct.unpack_from('<II',D,p)
    if cmd==0x19:
        name=D[p+8:p+24].rstrip(b'\0').decode(); va,vs,fo,fs=struct.unpack_from('<QQQQ',D,p+24); segs.append((name,va,vs,fo,fs))
    p+=sz
def off(va):
    for n,v,vs,fo,fs in segs:
        if v<=va<v+fs: return fo+va-v
    raise SystemExit('unmapped %x'%va)
def ptr(raw):
    # chained fixups: plain rebase uses low 36 bits target (+ high8) for DYLD_CHAINED_PTR_64; treat bit63 bind
    if raw>>63: return 'bind:%x'%(raw&0xffffff)
    t=raw&0xfffffffff; hi=(raw>>36)&0xff
    return hex((hi<<56)|t if t>=0x100000000 else 0x100000000+t)
va=int(sys.argv[1],16); n=int(sys.argv[2]); mode=sys.argv[3] if len(sys.argv)>3 else 'hex'
o=off(va)
if mode=='ptrs':
    for i in range(n):
        raw=struct.unpack_from('<Q',D,o+8*i)[0]; t=ptr(raw)
        s=''
        try:
            if not t.startswith('bind'):
                to=off(int(t,16)); e=D.index(b'\0',to); s=repr(D[to:min(e,to+60)])
        except SystemExit: pass
        print(hex(va+8*i),hex(raw),t,s)
elif mode=='wstr':
    print(D[o:o+n].decode('utf-32-le',errors='replace'))
else:
    print(D[o:o+n].hex(' '), repr(D[o:o+n]))
