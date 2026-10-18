"""Decode typed constants at vmaddrs in the thin arm64 Live slice (read-only; output is data).
usage: python3 -I read_consts.py <Live.arm64> <vmaddr> <struct format, e.g. <4d or <2f>"""
import struct, sys
path, va, f = sys.argv[1], int(sys.argv[2], 16), sys.argv[3]
b = open(path, 'rb').read()
off, segs = 32, []
for _ in range(struct.unpack_from('<I', b, 16)[0]):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24); segs.append((vm, fs, fo))
    off += size
o = next(fo + va - vm for vm, fs, fo in segs if vm <= va < vm + fs)
raw = b[o:o + struct.calcsize(f)]
print(f'{va:#x} {f} {raw.hex()} {struct.unpack(f, raw)}')
