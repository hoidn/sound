"""Print NUL-terminated strings at VM addresses of a thin arm64 Mach-O.

Usage: python3 -I cstr.py BINARY ADDR [ADDR ...]
"""
import struct, sys

def main(path, addrs):
    data = open(path, 'rb').read()
    _, _, _, _, ncmds, _, _, _ = struct.unpack_from('<IiiIIIII', data, 0)
    off, segs = 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        if cmd == 0x19:
            vm, vms, fo, fs = struct.unpack_from('<QQQQ', data, off + 24)
            segs.append((vm, fo, fs))
        off += size
    for a in addrs:
        vm, fo, fs = next(s for s in segs if s[0] <= a < s[0] + s[2])
        p = fo + a - vm
        print(hex(a), repr(data[p:data.index(b'\0', p)].decode('utf-8', 'replace')))

if __name__ == '__main__':
    main(sys.argv[1], [int(x, 16) for x in sys.argv[2:]])
