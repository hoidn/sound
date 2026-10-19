"""Find 8-byte little-endian occurrences of pointer values in a Mach-O x86_64 slice; print their VAs (data).
usage: python3 -I findptr.py <slice> <va>...     (stored pointers are plain VAs: rebase slide 0)"""
import struct, sys
b = open(sys.argv[1], 'rb').read()
ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        name = b[off + 8:off + 24].rstrip(b'\0').decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
        segs.append((name, vmaddr, fileoff, filesize))
    off += size
for a in sys.argv[2:]:
    pat = struct.pack('<Q', int(a, 16))
    i = b.find(pat)
    while i >= 0:
        for name, vm, fo, fs in segs:
            if fo <= i < fo + fs and fs:
                print(a, name, hex(vm + i - fo))
        i = b.find(pat, i + 1)
