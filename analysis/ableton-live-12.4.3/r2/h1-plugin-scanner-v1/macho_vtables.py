"""Resolve C++ vtable address points in an arm64 Mach-O slice to RTTI names and slots.

Analyst-only, read-only. Usage: python3 -I macho_vtables.py <slice> <0xaddr>...
       python3 -I macho_vtables.py <slice> --find <0xtarget>...  (data words pointing at targets)
Decodes DYLD_CHAINED_PTR_64(_OFFSET) rebase pointers heuristically: a non-bind
pointer keeps its low 36 bits; values below the image base get the base added.
Prints JSON: for each address point, the typeinfo name (vtable[-8] -> typeinfo
-> name) and the first 24 slot targets. Depends only on the slice bytes.
"""
import json, struct, sys

BASE = 0x100000000

def segments(b):
    ncmds = struct.unpack_from('<I', b, 16)[0]
    off, segs = 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((vmaddr, vmsize, fileoff, filesize))
        off += size
    return segs

def reader(b):
    segs = segments(b)
    def foff(va):
        for vm, vs, fo, fs in segs:
            if vm <= va < vm + fs:
                return fo + va - vm
        return None
    def ptr(va):
        o = foff(va)
        if o is None:
            return None
        raw = struct.unpack_from('<Q', b, o)[0]
        if raw >> 63:
            return ('bind', raw & 0xFFFFFF)
        t = (raw & 0xFFFFFFFFF) | (((raw >> 36) & 0xFF) << 56)
        return t + BASE if t and t < BASE else t
    def cstr(va):
        o = foff(va)
        if o is None:
            return None
        return b[o:b.index(b'\0', o)].decode('latin1')
    return ptr, cstr, segs

def find(b, ptr, segs, targets):
    hits = {t: [] for t in targets}
    for vm, vs, fo, fs in segs:
        if fo == 0:
            continue  # skip __TEXT: code, not pointer tables
        for va in range(vm, vm + fs - 7, 8):
            p = ptr(va)
            if p in hits:
                hits[p].append(hex(va))
    return {hex(t): v for t, v in hits.items()}

def main():
    b = open(sys.argv[1], 'rb').read()
    ptr, cstr, segs = reader(b)
    if sys.argv[2] == '--find':
        print(json.dumps(find(b, ptr, segs, [int(a, 16) for a in sys.argv[3:]]), indent=1))
        return
    out = []
    for a in sys.argv[2:]:
        va = int(a, 16)
        ti = ptr(va - 8)
        name = None
        if isinstance(ti, int):
            np = ptr(ti + 8)
            name = cstr(np) if isinstance(np, int) else None
        slots = []
        for i in range(24):
            p = ptr(va + 8 * i)
            if not isinstance(p, int) or not (BASE <= p < BASE + 0x10000000):
                break
            slots.append(hex(p))
        out.append({'address_point': a, 'typeinfo': hex(ti) if isinstance(ti, int) else ti,
                    'rtti_name': name, 'slots': slots})
    print(json.dumps(out, indent=1))

if __name__ == '__main__':
    main()
