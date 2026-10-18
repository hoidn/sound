"""Read typed little-endian values at a vmaddr from the thin arm64 Live slice (read-only; output is data).
usage: python3 -I read_mem.py <Live.arm64> <vmaddr> <struct-char: i|I|f|d|Q> <count>
Prints each value; floats also with their hex bits and, for gains, 20*log10 in dB."""
import math, struct, sys
path, va, ch, n = sys.argv[1], int(sys.argv[2], 16), sys.argv[3], int(sys.argv[4])
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:  # LC_SEGMENT_64
        name = b[off+8:off+24].rstrip(b'\0').decode()
        segs.append((name,) + struct.unpack_from('<QQQQ', b, off+24))
    off += size
w = struct.calcsize('<' + ch)
for i in range(n):
    v = va + w * i
    seg = next(s for s in segs if s[1] <= v < s[1] + s[4])
    o = seg[3] + v - seg[1]
    x = struct.unpack_from('<' + ch, b, o)[0]
    extra = ''
    if ch in 'fd':
        extra = f' bits={b[o:o+w][::-1].hex()}' + (f' dB={20*math.log10(x):.6f}' if x > 0 else '')
    print(f'{v:#x} [{i}] {seg[0]} {x!r}{extra}')
