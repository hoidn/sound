"""Find byte patterns (binary64 / binary32 constants) in a Mach-O slice and print their vmaddrs (output is data).

usage: python3 -I findconst.py <slice> d:<float>|f:<float>|hex:<bytes> ...
"""
import struct, sys


def segments(b):
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            nsect = struct.unpack_from('<I', b, off + 64)[0]
            for k in range(nsect):
                s = off + 72 + 80 * k
                sect, seg = b[s:s + 16].rstrip(b'\0').decode(), b[s + 16:s + 32].rstrip(b'\0').decode()
                addr, sz, fo = struct.unpack_from('<QQI', b, s + 32)
                segs.append((seg + ',' + sect, addr, sz, fo))
        off += size
    return segs


def main():
    b = open(sys.argv[1], 'rb').read()
    segs = segments(b)
    for tok in sys.argv[2:]:
        kind, v = tok.split(':', 1)
        pat = {'d': lambda: struct.pack('<d', float(v)), 'f': lambda: struct.pack('<f', float(v)),
               'hex': lambda: bytes.fromhex(v)}[kind]()
        i = b.find(pat)
        while i >= 0:
            for name, addr, sz, fo in segs:
                if fo <= i < fo + sz and fo:
                    print(tok, name, hex(addr + i - fo))
            i = b.find(pat, i + 1)


if __name__ == '__main__':
    main()
