"""Read bytes at vmaddrs from a thin Mach-O image (read-only; output is data). usage: img_read.py <image> hex|dbl|str <vmaddr> [n]"""
import struct, sys
path, mode, va = sys.argv[1], sys.argv[2], int(sys.argv[3], 16)
n = int(sys.argv[4]) if len(sys.argv) > 4 else 2
b = open(path, 'rb').read()
ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24)
        segs.append((vm, fs, fo))
    off += size
o = next(fo + va - vm for vm, fs, fo in segs if vm <= va < vm + fs)
if mode == 'dbl':
    for i in range(n):
        raw = struct.unpack_from('<Q', b, o + 8 * i)[0]
        print(f'{va + 8*i:#x} {raw:#018x} {struct.unpack_from("<d", b, o + 8*i)[0]!r}')
elif mode == 'hex':
    print(b[o:o + n].hex())
else:
    print(b[o - n:o + n].replace(b'\0', b'|').decode('latin1'))
