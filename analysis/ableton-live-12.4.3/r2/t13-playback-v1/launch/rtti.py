"""Itanium RTTI walk in a Mach-O x86_64 slice: class name -> typeinfo -> vtables and bases (output is data).

usage: python3 -I rtti.py <slice> <mangled-name>...     e.g. 13ATimeableFloat
For each name: the typeinfo address(es) whose name pointer is that string, the type of typeinfo (si/vmi by its
first word), its bases, and every vtable (address of slot 0) whose typeinfo slot (vtable - 8) holds it, with
offset-to-top. Pointers in the x86_64 slice are plain VAs.
"""
import struct, sys


def load(path):
    b = open(path, 'rb').read()
    ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            name = b[off + 8:off + 24].rstrip(b'\0').decode()
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((name, vmaddr, fileoff, filesize))
        off += size
    return b, segs


def main():
    b, segs = load(sys.argv[1])

    def fo(va):
        return next(f + va - vm for n, vm, f, fs in segs if vm <= va < vm + fs)

    def q(va):
        return struct.unpack_from('<Q', b, fo(va))[0]

    def cstr(va):
        o = fo(va)
        return b[o:b.index(b'\0', o)].decode('latin-1')

    data = [(n, vm, f, fs) for n, vm, f, fs in segs if n in ('__DATA', '__DATA_CONST')]
    words = {}
    for n, vm, f, fs in data:
        for i, w in enumerate(struct.unpack_from('<%dQ' % (fs // 8), b, f)):
            words.setdefault(w, []).append(vm + 8 * i)
    for name in sys.argv[2:]:
        pat, k, svas = name.encode() + b'\0', -1, []
        while (k := b.find(pat, k + 1)) >= 0:
            if b[k - 1] == 0:
                svas += [vm + k - f for n, vm, f, fs in segs if n == '__TEXT' and f <= k < f + fs]
        for ti in [a - 8 for sva in svas for a in words.get(sva, [])]:
            w2 = q(ti + 16)
            if 0x106000000 <= w2 < 0x108000000:          # si: {vt, name, base}
                kind, bases = 'si', [(w2, 0)]
            else:                                         # vmi: {vt, name, flags:4 count:4, {base, offset_flags}...}
                kind, bases = 'vmi', [(q(ti + 24 + 16 * j), q(ti + 32 + 16 * j) >> 8) for j in range(w2 >> 32)]
            bn = []
            for bt, offs in bases:
                try:
                    bn.append(f'{cstr(q(bt + 8))}@{offs:#x}')
                except (StopIteration, ValueError):
                    bn.append(f'{bt:#x}@{offs:#x}')
            print(f'{name}: typeinfo {ti:#x} {kind} bases={bn}')
            for a in words.get(ti, []):
                ott = struct.unpack('<q', struct.pack('<Q', q(a - 8)))[0]
                if -0x10000 < ott <= 0:
                    print(f'   vtable {a + 8:#x} offset_to_top={ott}')
        if not svas:
            print(f'{name}: no such typeinfo name')


if __name__ == '__main__':
    main()
