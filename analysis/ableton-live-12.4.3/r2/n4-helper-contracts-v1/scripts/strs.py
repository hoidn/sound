import re, sys
data = open('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64','rb').read()
pat = sys.argv[1].encode()
ctx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
for m in re.finditer(re.escape(pat), data):
    # find string start
    s = m.start()
    while s > 0 and data[s-1] != 0: s -= 1
    e = data.index(b'\0', m.end())
    print(hex(0x100000000 + s), repr(data[s:e].decode('latin1')))
    if ctx:
        # print neighbors
        a = s; out=[]
        p = e+1
        for _ in range(ctx):
            q = data.index(b'\0', p); out.append((hex(0x100000000+p), data[p:q].decode('latin1'))); p = q+1
        for x in out: print('   +', x)
