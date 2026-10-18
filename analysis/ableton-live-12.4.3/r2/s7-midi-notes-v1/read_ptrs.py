"""Read 8-byte words at vmaddrs from the thin arm64 Live slice (read-only; output is data).
usage: python3 -I read_ptrs.py <Live.arm64> <vmaddr> <count>
Chained-fixup rebases are decoded as base + low 36 bits (DYLD_CHAINED_PTR_64_OFFSET style); binds are shown raw."""
import struct, sys
path, va, n = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3])
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:  # LC_SEGMENT_64
        name = b[off+8:off+24].rstrip(b'\0').decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off+24)
        segs.append((name, vmaddr, vmsize, fileoff, filesize))
    off += size
def fo(v):
    for name, vm, vs, fo_, fs in segs:
        if vm <= v < vm + fs: return fo_ + v - vm, name
    raise SystemExit(f'unmapped {v:#x}')
for i in range(n):
    v = va + 8 * i
    o, seg = fo(v)
    w = struct.unpack_from('<Q', b, o)[0]
    bind = w >> 63
    dec = (w & 0xFFFFFFFFF) if not bind else None
    print(f'{v:#x} +{8*i:#05x} raw={w:#018x} ' + (f'-> {dec:#x}' if dec else 'bind'))
