"""Find vtables of Itanium-RTTI class names in the thin arm64 Live slice and print chosen slots (read-only).
usage: rtti_vtable.py <Live.arm64> <slot,slot,...> <ClassName>...
Pointers decoded as chained-fixup rebases (low 36 bits), binds skipped, as in T11 read_ptrs.py."""
import re, struct, sys
path, slots, names = sys.argv[1], [int(s, 16) for s in sys.argv[2].split(',')], sys.argv[3:]
b = open(path, 'rb').read()
ncmds, off, segs = struct.unpack_from('<I', b, 16)[0], 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        n = b[off + 8:off + 24].rstrip(b'\0').decode()
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24)
        segs.append((n, vm, fo, fs))
    off += size
def fo(v):
    return next((f + v - vm for n, vm, f, fs in segs if vm <= v < vm + fs), None)
def va(o):
    return next((vm + o - f for n, vm, f, fs in segs if f <= o < f + fs), None)
def word(v):
    o = fo(v)
    if o is None: return None
    w = struct.unpack_from('<Q', b, o)[0]
    return None if w >> 63 else w & 0xFFFFFFFFF
data = [(n, vm, f, fs) for n, vm, f, fs in segs if n.startswith('__DATA')]
words = {}
for n, vm, f, fs in data:
    for i, (w,) in enumerate(struct.iter_unpack('<Q', b[f:f + fs - fs % 8])):
        if not w >> 63:
            words.setdefault(w & 0xFFFFFFFFF, []).append(vm + 8 * i)
for cls in names:
    mangled = f'{len(cls)}{cls}'.encode() + b'\0'
    for m in re.finditer(re.escape(mangled), b):
        if b[m.start() - 1:m.start()] not in (b'\0',): continue
        s = va(m.start())
        for ti8 in words.get(s, []):
            ti = ti8 - 8
            for vt1 in words.get(ti, []):
                top = struct.unpack_from('<q', b, fo(vt1 - 8))[0]
                ap = vt1 + 8
                print(cls, f'name {s:#x} typeinfo {ti:#x} vtable point {ap:#x} offset-to-top {top}',
                      ' '.join(f'+{k:#x}={word(ap + k):#x}' if word(ap + k) else f'+{k:#x}=?' for k in slots))
