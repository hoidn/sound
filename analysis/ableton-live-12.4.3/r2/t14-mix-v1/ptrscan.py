"""Find 8-byte little-endian occurrences of given addresses in a slice (data pointers to functions).

usage: python3 -I ptrscan.py SLICE BASE ADDR...   prints VA (file offset + BASE) of each occurrence
Live x86_64: BASE 0x100000000; engine: BASE 0. Read-only; output is data.
"""
import struct, sys
d = open(sys.argv[1], 'rb').read(); base = int(sys.argv[2], 16)
for a in sys.argv[3:]:
    pat, i = struct.pack('<Q', int(a, 16)), 0
    hits = []
    while (i := d.find(pat, i)) != -1:
        hits.append(hex(i + base)); i += 1
    print(a, hits)
