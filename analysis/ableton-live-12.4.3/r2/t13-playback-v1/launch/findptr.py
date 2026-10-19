"""Find 8-byte-aligned qwords equal to given VAs in the data segments of a Mach-O slice (output is data).

usage: python3 -I findptr.py <slice> <va>...
The x86_64 slice stores rebased pointers as plain VAs (image base 0x100000000), so a typeinfo, vtable or
function address appears verbatim wherever it is referenced from data.
"""
import struct, sys


def main():
    b = open(sys.argv[1], 'rb').read()
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            name = b[off + 8:off + 24].rstrip(b'\0').decode()
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
            if name in ('__DATA', '__DATA_CONST'):
                segs.append((name, vmaddr, fileoff, filesize))
        off += size
    targets = {int(x, 16) for x in sys.argv[2:]}
    for name, vm, fo, fs in segs:
        words = struct.unpack_from('<%dQ' % (fs // 8), b, fo)
        for i, w in enumerate(words):
            if w in targets:
                print(f'{w:#x} at {vm + 8 * i:#x} ({name})')


if __name__ == '__main__':
    main()
