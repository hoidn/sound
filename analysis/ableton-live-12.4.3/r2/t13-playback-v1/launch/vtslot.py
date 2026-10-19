"""Name the vtable holding a data address: scan back from <addr> to the vtable header (offset-to-top, typeinfo)
and print the class name from the typeinfo's name pointer, plus the slot offset (output is data).

usage: python3 -I vtslot.py <slice> <addr>...      (x86_64 Live slice; pointers are plain VAs)
"""
import struct, sys


def load(path):
    b = open(path, 'rb').read()
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((vmaddr, fileoff, filesize))
        off += size
    return b, segs


def fo(segs, va):
    for vm, f, fs in segs:
        if vm <= va < vm + fs:
            return f + va - vm
    return None


def q(b, segs, va):
    o = fo(segs, va)
    return None if o is None else struct.unpack_from('<Q', b, o)[0]


def cstr(b, segs, va):
    o = fo(segs, va)
    return None if o is None else b[o:b.index(b'\0', o)].decode('latin-1')


def main():
    b, segs = load(sys.argv[1])
    for a in (int(x, 16) for x in sys.argv[2:]):
        v = a
        while v > a - 0x4000:
            v -= 8
            ti, ott = q(b, segs, v), q(b, segs, v - 8)
            if ott is not None and (ott == 0 or ott > 0xffffffff00000000) and ti and 0x106000000 <= ti < 0x108000000:
                name = cstr(b, segs, q(b, segs, ti + 8) or 0)
                if name and name[:1].isdigit():
                    print(f'{a:#x}: vtable {v + 8:#x} slot +{a - v - 8:#x} offset-to-top {ott:#x} class {name}')
                    break


if __name__ == '__main__':
    main()
