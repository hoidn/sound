"""Pointee trace image reads (read-only; output is data). usage: python3 -I image_reads.py <Live.arm64>
Prints the vtable slots, typeinfo names, lambda vtable and constants cited in trace.txt."""
import struct, sys
b = open(sys.argv[1], 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24); segs.append((vm, fo, fs))
    off += size
def fo(v): return next(f + v - vm for vm, f, fs in segs if vm <= v < vm + fs)
def q(v): return struct.unpack_from('<Q', b, fo(v))[0]
def cstr(v): o = fo(v); return b[o:b.index(b'\0', o)].decode()
def tname(vt_header): return cstr(q((q(vt_header + 8) & 0xFFFFFFFFF) + 8) & 0x7fffffffffffffff)
# (vtable header address, slot offsets to print)
for hdr, slots in [(0x1067f24e0, (0xd0, 0x308, 0x318)), (0x106679770, (0xd0, 0x308, 0x318)),
                   (0x106677828, (0x80, 0xd0)), (0x1067c6b80, (0x80, 0xd0)), (0x1067f4938, (0x30,))]:
    print(f'vtable {hdr:#x} {tname(hdr)}:', ' '.join(f'+{s:#x}={q(hdr + 16 + s) & 0xFFFFFFFFF:#x}' for s in slots))
print('ADocument ctor constant 0x105818b28 (int32 x2):', struct.unpack_from('<ii', b, fo(0x105818b28)))
print('APointee member name 0x1062acd64:', b[fo(0x1062acd64):fo(0x1062acd64) + 6].decode('utf-16-le'))
