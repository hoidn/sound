# usage: python3 -I words.py <slice-file> <image-base> <start-va> <count>  -> 8-byte words, with C-string preview when a word points into the slice
import sys, struct
base = int(sys.argv[2], 16); va = int(sys.argv[3], 16); n = int(sys.argv[4])
data = open(sys.argv[1], 'rb').read()
def cstr(a):
    o = a - base
    if 0 <= o < len(data):
        e = data.find(b'\0', o, o + 80); s = data[o:e if e != -1 else o + 80]
        if s and all(32 <= c < 127 for c in s): return s.decode()
    return ''
for k in range(n):
    a = va + 8 * k; w = struct.unpack_from('<Q', data, a - base)[0]
    print(hex(a), hex(w), cstr(w))
