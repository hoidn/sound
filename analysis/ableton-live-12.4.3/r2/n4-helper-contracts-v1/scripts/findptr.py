# usage: findptr.py <va>... : find 8-byte little-endian occurrences of the VA in the slice (data refs)
import sys, struct, re
exec(open(__file__.rsplit('/',1)[0]+'/memlib.py').read())
def va_of(o):
    for v,fs,fo in segs:
        if fo<=o<fo+fs and v: return v+o-fo
for a in sys.argv[1:]:
    pat=struct.pack('<Q',int(a,16))
    print(a,[hex(va_of(m.start())) for m in re.finditer(re.escape(pat),D)][:20])
