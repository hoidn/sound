import struct, os
N=os.environ.get('N','12')
D=open('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64','rb').read()
ncmds=struct.unpack_from('<I',D,16)[0]; p=32; segs=[]
for _ in range(ncmds):
    cmd,sz=struct.unpack_from('<II',D,p)
    if cmd==0x19:
        va,vs,fo,fs=struct.unpack_from('<QQQQ',D,p+24); segs.append((va,fs,fo))
    p+=sz
def off(va):
    for v,fs,fo in segs:
        if v<=va<v+fs: return fo+va-v
    return None
def rd(va):
    o=off(va)
    if o is None: return 0
    raw=struct.unpack_from('<Q',D,o)[0]
    if raw>>63: return 0
    t=raw&0xfffffffff
    return t if t>=0x100000000 else (0x100000000+t if t else 0)
def cstr(va):
    o=off(va)
    if o is None: return '?'
    return D[o:D.index(b'\0',o)].decode('latin1')
