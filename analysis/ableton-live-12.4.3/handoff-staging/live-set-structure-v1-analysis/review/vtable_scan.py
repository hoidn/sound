"""Reviewer's check of the A2 premise (analyst side; never shipped; output is data).
Scans every vtable header of the thin arm64 Live image (offset-to-top 0, typeinfo pointer whose name is an
Itanium class name) and prints, for each document-object class (slot +0x140 is the generic member loader
0x101487310), its slot +0xd0 (member post-load) and +0x100 (validation walk) functions.
usage: python3 -I -B vtable_scan.py <Live.arm64> [name-regex]
"""
import re, struct, sys

path = sys.argv[1]
rx = re.compile(sys.argv[2]) if len(sys.argv) > 2 else None
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
    for _, vm, f, fs in segs:
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
    o = fo(v) if v else None
    if o is None:
        return None
    s = b[o:o + 200].split(b'\0', 1)[0]
    return s.decode() if re.fullmatch(rb'\d+[A-Za-z_]\w*', s or b'') else None


LOADER, BASE_WALK = 0x101487310, 0x101487c3c
rows = []
for n, vm, f, fs in segs:
    if not n.startswith('__DATA'):
        continue
    for i in range(0, fs - 16, 8):
        if struct.unpack_from('<q', b, f + i)[0] != 0:
            continue
        ti = word(vm + i + 8)
        if not ti:
            continue
        nm = cstr(word(ti + 8)) if fo(ti + 8) is not None else None
        if not nm:
            continue
        ap = vm + i + 16
        if word(ap + 0x140) != LOADER:
            continue
        rows.append((nm, ap, word(ap + 0xd0), word(ap + 0x100)))
print(f'document-object vtables (slot +0x140 = {LOADER:#x}): {len(rows)}')
walks = {}
for nm, ap, d0, w in rows:
    walks.setdefault(w, []).append(nm)
print('distinct +0x100 (walk) functions:')
for w, names in sorted(walks.items(), key=lambda x: -len(x[1])):
    tag = 'base no-op' if w == BASE_WALK else 'override'
    print(f'  {w:#x} {tag} x{len(names)}: {" ".join(sorted(names)[:12])}{" ..." if len(names) > 12 else ""}')
if rx:
    print(f'classes matching {rx.pattern}:')
    for nm, ap, d0, w in sorted(rows):
        if rx.search(nm):
            print(f'  {nm} vtable {ap:#x} +0xd0 {d0:#x} +0x100 {w:#x}')
