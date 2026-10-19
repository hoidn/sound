"""For each VA of a stored function pointer inside a vtable, walk back to the vtable start (an offset-to-top word
followed by a typeinfo whose name pointer is a printable C string) and print class name, vtable VA and slot offset.
usage: python3 -I vtslot.py <slice> <va>...   (x86_64 Mach-O slice; stored pointers are plain VAs; output is data)"""
import struct, sys
b = open(sys.argv[1], 'rb').read()
ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
        segs.append((vmaddr, fileoff, filesize))
    off += size


def fo(va):
    return next((f + va - vm for vm, f, fs in segs if vm <= va < vm + fs), None)


def q(va):
    o = fo(va)
    return None if o is None else struct.unpack_from('<Q', b, o)[0]


def cstr(va):
    o = fo(va)
    if o is None:
        return None
    e = b.find(b'\0', o, o + 300)
    s = b[o:e]
    return s.decode() if e > o and all(32 < c < 127 for c in s) else None


for a in sys.argv[2:]:
    va = int(a, 16)
    for k in range(0, 0x2000, 8):
        v = va - k
        ti, ott = q(v - 8), q(v - 16)
        if ti and ott is not None and (ott == 0 or ott > 0xffff000000000000):
            name = cstr(q(ti + 8) or 0) if q(ti + 8) else None
            if name and name[0].isdigit():
                print(a, name, hex(v), f'+{k:#x}', f'ott={ott - (1 << 64) if ott else 0}')
                break
