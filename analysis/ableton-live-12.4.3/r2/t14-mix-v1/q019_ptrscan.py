"""Find 8-byte little-endian occurrences of given addresses in a Mach-O slice (pointer/vtable scan).

usage: python3 -I q019_ptrscan.py SLICE ADDR...   prints VA of every qword equal to ADDR (VA = vmaddr + offset in segment)
Read-only; output is data.
"""
import struct, sys
d = open(sys.argv[1], 'rb').read()
ncmds, off, segs = struct.unpack_from('<I', d, 16)[0], 32, []
for _ in range(ncmds):
    cmd, cs = struct.unpack_from('<II', d, off)
    if cmd == 0x19:
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', d, off + 24)
        segs.append((vm, fo, fs))
    off += cs
for a in sys.argv[2:]:
    pat, hits = struct.pack('<Q', int(a, 16)), []
    for vm, fo, fs in segs:
        i = d.find(pat, fo, fo + fs)
        while i != -1:
            hits.append(hex(vm + i - fo)); i = d.find(pat, i + 1, fo + fs)
    print(a, hits)
