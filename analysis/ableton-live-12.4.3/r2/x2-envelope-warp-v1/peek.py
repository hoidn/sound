"""Read words from a Mach-O slice at vmaddrs (read-only; output is data).

usage: python3 -I peek.py <slice> q|d|f|i|s <vmaddr> <count>   q = qword hex, d = binary64, f = binary32, i = int32,
                                                                s = C string (count ignored)
The x86_64 slice uses classic rebase opcodes with image base 0x100000000, so stored pointers are plain VAs.
"""
import struct, sys


def main():
    path, kind, va, n = sys.argv[1], sys.argv[2], int(sys.argv[3], 16), int(sys.argv[4], 0)
    b = open(path, 'rb').read()
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((vmaddr, fileoff, filesize))
        off += size
    if kind == 's':
        fo = next(fo + va - vm for vm, fo, fs in segs if vm <= va < vm + fs)
        print(f'{va:#x} ' + repr(b[fo:b.index(b'\0', fo)].decode('latin-1')))
        return
    fmt, w = {'q': ('<Q', 8), 'd': ('<d', 8), 'f': ('<f', 4), 'i': ('<i', 4)}[kind]
    for k in range(n):
        v = va + w * k
        fo = next(fo + v - vm for vm, fo, fs in segs if vm <= v < vm + fs)
        x = struct.unpack_from(fmt, b, fo)[0]
        print(f'{v:#x} +{w * k:#05x} ' + (f'{x:#x}' if kind == 'q' else repr(x)))


if __name__ == '__main__':
    main()
