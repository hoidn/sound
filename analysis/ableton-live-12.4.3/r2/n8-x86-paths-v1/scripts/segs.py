# usage: python3 -I segs.py <macho-slice> [va...]  -> LC_SEGMENT_64 table, then the segment containing each VA
import sys, struct
d = open(sys.argv[1], 'rb').read()
ncmds = struct.unpack_from('<I', d, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', d, off)
    if cmd == 0x19:
        name = d[off + 8:off + 24].rstrip(b'\0').decode(); vm, vs, fo, fs = struct.unpack_from('<QQQQ', d, off + 24)
        segs.append((name, vm, vs, fo, fs))
    off += size
for s in segs: print('%-12s vm %#x size %#x fileoff %#x' % s[:4])
for v in sys.argv[2:]:
    x = int(v, 16); print(v, [s[0] for s in segs if s[1] <= x < s[1] + s[2]])
