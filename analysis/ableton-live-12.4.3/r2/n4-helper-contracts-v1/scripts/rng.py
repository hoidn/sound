import sys
data = open('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64','rb').read()
a = int(sys.argv[1],16)-0x100000000; b = int(sys.argv[2],16)-0x100000000
while a > 0 and data[a-1] != 0: a -= 1
p = a
while p < b:
    q = data.index(b'\0', p)
    if q > p: print(hex(0x100000000+p), repr(data[p:q].decode('latin1')))
    p = q+1
