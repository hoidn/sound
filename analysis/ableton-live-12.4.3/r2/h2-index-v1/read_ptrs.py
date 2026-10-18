"""Read 8-byte pointer slots from a thin arm64 Mach-O by virtual address (no Ghidra).

Usage: python3 -I read_ptrs.py <thin-macho> <vmaddr-hex> <count>
Maps the address through LC_SEGMENT_64 and decodes each word as a chained-fixup rebase
(DYLD_CHAINED_PTR_64 / 64_OFFSET: low 36 bits are the target, as vmaddr or as offset from
0x100000000; bit 63 set means a bind, printed as 'bind'). Prints slot offset, raw word, decoded target.
Limitation: assumes the image uses one of those two pointer formats; it does not read the
LC_DYLD_CHAINED_FIXUPS header to confirm which.
"""
import struct, sys

path, addr, count = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3])
data = open(path, "rb").read()
magic, _, _, _, ncmds, _, _, _ = struct.unpack_from("<IiiIIIII", data, 0)
assert magic == 0xFEEDFACF, "not a thin 64-bit Mach-O"
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from("<II", data, off)
    if cmd == 0x19:  # LC_SEGMENT_64
        name = data[off + 8:off + 24].rstrip(b"\0").decode()
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, off + 24)
        segs.append((name, vmaddr, vmsize, fileoff, filesize))
    off += size
for i in range(count):
    va = addr + 8 * i
    seg = next(s for s in segs if s[1] <= va < s[1] + s[4])
    word = struct.unpack_from("<Q", data, seg[3] + va - seg[1])[0]
    if word >> 63:
        decoded = "bind"
    else:
        target = word & 0xFFFFFFFFF
        decoded = hex(target if target >= 0x100000000 else 0x100000000 + target)
    print(f"+0x{8 * i:x}\t{seg[0]}\t0x{word:016x}\t{decoded}")
