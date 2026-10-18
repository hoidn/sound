"""Read the few raw image facts N2 cites from the thin arm64 Live image (no execution).

Usage: python3 -I image_probe.py <Live.arm64> > image-probe.json
Maps vmaddr to file offset with the LC_SEGMENT_64 table; pointers in this derived image are plain.
"""
import json, re, struct, sys

data = open(sys.argv[1], "rb").read()
segs, off = [], 32
for _ in range(struct.unpack_from("<I", data, 16)[0]):
    cmd, size = struct.unpack_from("<II", data, off)
    if cmd == 0x19:
        vm, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", data, off + 24)
        segs.append((vm, filesize, fileoff))
    off += size


def at(va, n):
    for vm, filesize, fileoff in segs:
        if vm <= va < vm + filesize:
            return data[fileoff + va - vm: fileoff + va - vm + n]
    raise ValueError(hex(va))


out = {
    "bytes": {hex(va): at(va, n).hex() for va, n in [(0x10581394d, 3), (0x105815848, 8)]},
    "txml_parser_vtable_0x106676ee0": {f"+0x{i:x}": hex(struct.unpack("<Q", at(0x106676ee0 + i, 8))[0]) for i in range(0, 0x90, 8)},
    "strings": {hex(m.start() + 0x100000000): m.group().decode() for m in
                re.finditer(rb" (?:deflate|inflate) 1\.3\.1 Copyright[^\x00]*|expat_[0-9.]+", data)},
}
print(json.dumps(out, indent=1))
