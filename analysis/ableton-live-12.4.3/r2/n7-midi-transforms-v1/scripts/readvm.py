"""readvm.py VMADDR COUNT [ptr|f32|u32|bytes]: read the Live.arm64 Mach-O image at a VM address.
Pointers are decoded as chained-fixup rebases (low 36 bits; < 0x100000000 means image offset)."""
import sys, struct
P = '/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64'
data = open(P, 'rb').read()
ncmds = struct.unpack_from('<I', data, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', data, off)
    if cmd == 0x19:
        name = data[off+8:off+24].rstrip(b'\0').decode(); vm, vs, fo, fs = struct.unpack_from('<QQQQ', data, off+24)
        segs.append((name, vm, vs, fo, fs))
    off += size
def fo(va):
    for n, vm, vs, f, fs in segs:
        if vm <= va < vm + fs: return f + va - vm
    raise SystemExit('unmapped %x' % va)
def ptr(v):
    if v >> 63: return 'bind:%x' % v
    t = v & ((1 << 36) - 1)
    if t and t < 0x100000000: t += 0x100000000
    return '%x' % t
va = int(sys.argv[1], 16); n = int(sys.argv[2]); kind = sys.argv[3] if len(sys.argv) > 3 else 'ptr'
for i in range(n):
    if kind == 'ptr':
        v = struct.unpack_from('<Q', data, fo(va + 8*i))[0]; print('%x +%d: %s' % (va + 8*i, 8*i, ptr(v)))
    elif kind == 'f32':
        print('%x: %r' % (va + 4*i, struct.unpack_from('<f', data, fo(va + 4*i))[0]))
    elif kind == 'f64':
        print('%x: %r' % (va + 8*i, struct.unpack_from('<d', data, fo(va + 8*i))[0]))
    elif kind == 'u32':
        print('%x: %#x' % (va + 4*i, struct.unpack_from('<I', data, fo(va + 4*i))[0]))
    else:
        print(data[fo(va):fo(va)+n].hex()); break
