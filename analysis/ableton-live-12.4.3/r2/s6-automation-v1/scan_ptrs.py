"""Find 8-byte-aligned data words in the thin arm64 Live slice that point at given vmaddrs
(read-only; output is data). Used to walk RTTI name -> typeinfo -> vtable when Ghidra kept no
reference. Words are decoded like read_ptrs.py: chained-fixup rebase = low 36 bits; binds skipped.
usage: python3 -I scan_ptrs.py <Live.arm64> <vmaddr>...
Prints, per target, every (segment, vmaddr) holding a pointer to it.
"""
import struct, sys

path, targets = sys.argv[1], {int(a, 16) for a in sys.argv[2:]}
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        name = b[off + 8:off + 24].rstrip(b'\0').decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
        if name.startswith('__DATA'):
            segs.append((name, vmaddr, fileoff, filesize))
    off += size
hits = {t: [] for t in targets}
for name, vm, fo, fs in segs:
    for (w,), i in zip(struct.iter_unpack('<Q', b[fo:fo + fs - fs % 8]), range(0, fs, 8)):
        if w >> 63:
            continue
        d = w & 0xFFFFFFFFF
        if d in hits:
            hits[d].append(f'{name}:{vm + i:#x}')
for t in sorted(hits):
    print(f'{t:#x}', ' '.join(hits[t]) or '-')
