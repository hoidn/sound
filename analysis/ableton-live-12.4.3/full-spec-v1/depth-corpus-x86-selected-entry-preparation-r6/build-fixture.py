"""Construct analyst-owned Mach-O DATA only; never load or execute guest bytes."""
from pathlib import Path
import hashlib, json, struct, sys
OUT = Path(__file__).resolve().parent / 'synthetic-corpus-x86.macho'

def fixture_bytes():
    image = bytearray(0x10000)
    header = struct.pack('<8I', 0xfeedfacf, 0x01000007, 3, 8, 1, 152, 0, 0)
    segment = struct.pack('<II16sQQQQiiII', 0x19, 152, b'__TEXT', 0, 0x10000, 0, 0x10000, 5, 5, 1, 0)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT', 0x2000, 0xe000, 0x2000, 4, 0, 0, 0x80000400, 0, 0, 0)
    image[:32] = header; image[32:184] = segment + section
    image[0x2000:0x10000] = b'\xcc' * 0xe000
    image[0x23b0:0x23b6] = bytes.fromhex('b82a000000c3')  # MOV EAX,42; RET
    image[0x85e0:0x85e3] = bytes.fromhex('31c0c3')        # XOR EAX,EAX; RET
    assert struct.unpack_from('<8I', image) == (0xfeedfacf, 0x01000007, 3, 8, 1, 152, 0, 0)
    assert len(image) == 0x10000 and len(segment + section) == 152
    assert image[0x23b0:0x23b6].hex() == 'b82a000000c3' and image[0x85e0:0x85e3].hex() == '31c0c3'
    assert 0x23b0 + 4096 <= 0x10000 and 0x85e0 + 4096 <= 0x10000
    return bytes(image)

def main():
    if sys.argv[1:] != ['--build-own-fixture']: raise SystemExit('Only owned-data fixture construction selected')
    data = fixture_bytes()
    with OUT.open('xb') as f: f.write(data)
    print(json.dumps(dict(path=str(OUT), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), guest_execution=False)))
if __name__ == '__main__': main()
