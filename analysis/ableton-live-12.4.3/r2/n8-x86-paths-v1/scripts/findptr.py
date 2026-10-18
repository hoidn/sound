# usage: python3 -I findptr.py <slice-file> <image-base> <0xvalue>...  -> VAs holding each 8-byte LE pointer
import sys, struct, mmap
base = int(sys.argv[2], 16)
with open(sys.argv[1], 'rb') as f:
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    for v in sys.argv[3:]:
        needle = struct.pack('<Q', int(v, 16)); i = m.find(needle); hits = []
        while i != -1:
            if i % 8 == 0: hits.append(hex(base + i))
            i = m.find(needle, i + 1)
        print(v, hits or 'none')
