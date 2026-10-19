"""Itanium RTTI walk in the thin arm64 Live slice: class name -> typeinfo -> vtables, plus chosen slots
(read-only; output is data). Chained-fixup rebases are decoded as the low 36 bits (as in
r2/s7-midi-notes-v1/read_ptrs.py); a decoded value below 0x100000000 is taken as an image offset and the base
0x100000000 is added.

usage: python3 -I rtti_arm64.py <Live.arm64> <slot-offset-hex,...> <mangled-name>...
"""
import struct, sys


def main():
    path, slots, names = sys.argv[1], [int(x, 16) for x in sys.argv[2].split(',')], sys.argv[3:]
    b = open(path, 'rb').read()
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            name = b[off + 8:off + 24].rstrip(b'\0').decode()
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((name, vmaddr, fileoff, filesize))
        off += size

    def dec(w):
        if w >> 63:
            return None
        v = w & 0xFFFFFFFFF
        return v + 0x100000000 if v < 0x100000000 else v

    data = [(n, vm, fo, fs) for n, vm, fo, fs in segs if n.startswith('__DATA')]
    ptrs = {}
    for n, vm, fo, fs in data:
        for i, w in enumerate(struct.unpack_from('<%dQ' % (fs // 8), b, fo)):
            d = dec(w)
            if d:
                ptrs.setdefault(d, []).append(vm + 8 * i)

    def word(va):
        for n, vm, fo, fs in segs:
            if vm <= va < vm + fs:
                return struct.unpack_from('<Q', b, fo + va - vm)[0]

    text = next(s for s in segs if s[0] == '__TEXT')
    for nm in names:
        needle = nm.encode() + b'\0'
        i = b.find(needle, text[2], text[2] + text[3])
        while i >= 0 and b[i - 1] != 0:
            i = b.find(needle, i + 1, text[2] + text[3])
        sva = text[1] + i - text[2]
        for ref in ptrs.get(sva, []):
            ti = ref - 8
            for vref in ptrs.get(ti, []):
                vt = vref + 8
                ott = word(vref - 8)
                s = ' '.join(f'+{o:#x}={dec(word(vt + o)) or 0:#x}' for o in slots)
                print(f'{nm}: name {sva:#x} typeinfo {ti:#x} vtable {vt:#x} offset-to-top {ott:#x} {s}')


if __name__ == '__main__':
    main()
