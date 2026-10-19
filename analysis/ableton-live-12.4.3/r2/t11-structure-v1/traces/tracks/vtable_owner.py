"""Name the class whose vtable holds a given function pointer (read-only; output is data).
For each function vmaddr: find data words pointing at it (as scan_ptrs.py), then walk back
word by word (at most 600) to the vtable header: a zero offset-to-top word followed by a typeinfo
pointer whose name pointer (typeinfo+8) leads to a printable Itanium RTTI name. Prints slot offset,
vtable address point, typeinfo and name. Heuristic: a secondary vtable reports its own header.
usage: python3 -I vtable_owner.py <Live.arm64> <func vmaddr>...
"""
import re, struct, sys

path, funcs = sys.argv[1], [int(a, 16) for a in sys.argv[2:]]
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        name = b[off + 8:off + 24].rstrip(b'\0').decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
        segs.append((name, vmaddr, fileoff, filesize))
    off += size


def fo(v):
    for name, vm, f, fs in segs:
        if vm <= v < vm + fs:
            return f + v - vm
    return None


def word(v):
    o = fo(v)
    if o is None:
        return None
    w = struct.unpack_from('<Q', b, o)[0]
    return None if w >> 63 else w & 0xFFFFFFFFF


def cstr(v):
    o = fo(v)
    if o is None:
        return None
    s = b[o:o + 200].split(b'\0', 1)[0]
    return s.decode('ascii', 'replace') if re.fullmatch(rb'[ -~]{2,}', s or b'') else None


data = [(n, vm, f, fs) for n, vm, f, fs in segs if n.startswith('__DATA')]
for fn in funcs:
    for n, vm, f, fs in data:
        for (w,), i in zip(struct.iter_unpack('<Q', b[f:f + fs - fs % 8]), range(0, fs, 8)):
            if w >> 63 or (w & 0xFFFFFFFFF) != fn:
                continue
            loc = vm + i
            for k in range(1, 600):
                ti = word(loc - 8 * k)
                top = struct.unpack_from('<q', b, fo(loc - 8 * k - 8))[0]
                nm = cstr(word(ti + 8)) if ti and top <= 0 and word(ti + 8) else None
                if nm and re.fullmatch(r'(N\w+E|\d+\w+)', nm):
                    print(f'{fn:#x} at {loc:#x}: slot +{8 * (k - 1):#x} of vtable {loc - 8 * (k - 1):#x} '
                          f'(offset-to-top {top}, typeinfo {ti:#x}, name {nm})')
                    break
            else:
                print(f'{fn:#x} at {loc:#x}: no header within 600 words')
