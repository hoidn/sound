"""Classify FP instructions in a range of the thin arm64 slice (read-only)."""
import struct, sys
path, va, n = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3])
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off+24)
        segs.append((vmaddr, fileoff, filesize))
    off += size
def fo(v):
    for vm, f, fs in segs:
        if vm <= v < vm + fs: return f + v - vm
PAT = [(0xFFFFFC00, 0x1E664000, 'frinta d'), (0xFFFFFC00, 0x1E264000, 'frinta s'), (0xFFFFFC00, 0x1E644000, 'frintn d'),
       (0xFFFFFC00, 0x1E65C000, 'frintz d'), (0xFFFFFC00, 0x1E64C000, 'frintp d'), (0xFFFFFC00, 0x1E654000, 'frintm d'),
       (0xFFFFFC00, 0x9E780000, 'fcvtzs x,d'), (0xFFFFFC00, 0x1E780000, 'fcvtzs w,d'), (0xFFFFFC00, 0x9E640000, 'fcvtas x,d'),
       (0xFFFFFC00, 0x9E620000, 'scvtf d,x'), (0xFFE0FC00, 0x1E600800, 'fmul d'), (0xFFE0FC00, 0x1E602800, 'fadd d'),
       (0xFFE0FC00, 0x1E601800, 'fdiv d'), (0xFFE0FC00, 0x1E603800, 'fsub d'), (0xFFFFFC00, 0x1E60C000, 'fabs d'),
       (0xFFE08000, 0x1F400000, 'fmadd d'), (0xFFE08000, 0x1F408000, 'fmsub d'), (0xFFFFFC00, 0x1E604000, 'fmov d,d'),
       (0xFFE0FC00, 0x1E602000, 'fcmp d'), (0xFF000000, 0x1E000000, 'other fp')]
o = fo(va)
for i in range(n):
    w = struct.unpack_from('<I', b, o + 4*i)[0]
    name = next((nm for m, p, nm in PAT if w & m == p), '')
    print(f'{va+4*i:#x} {w:08x} {name}')
