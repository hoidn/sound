"""Tie bytecode digests to the pinned main executable via its code signature (read-only)."""
import base64, hashlib, json, plistlib, struct, sys
from pathlib import Path

app = Path(sys.argv[1]); hashes = json.loads(Path(sys.argv[2]).read_text())
exe = (app / "Contents/MacOS/Live").read_bytes()
print("exe sha256", hashlib.sha256(exe).hexdigest())
cr_bytes = (app / "Contents/_CodeSignature/CodeResources").read_bytes()
cr_sha256 = hashlib.sha256(cr_bytes).digest(); cr_sha1 = hashlib.sha1(cr_bytes).digest()

def slices(b):
    magic = struct.unpack(">I", b[:4])[0]
    if magic in (0xCAFEBABE, 0xCAFEBABF):
        n = struct.unpack(">I", b[4:8])[0]; out = []
        for i in range(n):
            if magic == 0xCAFEBABE:
                cpu, sub, off, size, align = struct.unpack(">iiIII", b[8+20*i:28+20*i])
            else:
                cpu, sub, off, size, align, _ = struct.unpack(">iiQQII", b[8+32*i:40+32*i])
            out.append((cpu, b[off:off+size]))
        return out
    return [(None, b)]

def code_dirs(m):
    ncmds = struct.unpack("<I", m[16:20])[0]; p = 32  # 64-bit header
    for _ in range(ncmds):
        cmd, size = struct.unpack("<II", m[p:p+8])
        if cmd == 0x1D:  # LC_CODE_SIGNATURE
            off, sz = struct.unpack("<II", m[p+8:p+16]); sb = m[off:off+sz]
            count = struct.unpack(">I", sb[8:12])[0]
            for i in range(count):
                typ, boff = struct.unpack(">II", sb[12+8*i:20+8*i])
                if struct.unpack(">I", sb[boff:boff+4])[0] == 0xFADE0C02:
                    yield sb[boff:]
        p += size

for cpu, m in slices(exe):
    for cd in code_dirs(m):
        (magic, length, version, flags, hashOffset, identOffset, nSpecial, nCode, codeLimit,
         hashSize, hashType) = struct.unpack(">IIIIIIIIIBB", cd[:38])
        slot3 = cd[hashOffset - 3*hashSize: hashOffset - 2*hashSize]
        ident = cd[identOffset:cd.index(b"\0", identOffset)].decode()
        want = cr_sha256 if hashType == 2 else cr_sha1
        print(f"cpu {cpu} ident {ident} hashType {hashType} slot-3 matches CodeResources: {slot3 == want[:hashSize]}")

files2 = plistlib.loads(cr_bytes)["files2"]
for row in hashes["files"]:
    rel = row["path"].removeprefix("Contents/")
    ent = files2.get(rel)
    got = ent.get("hash2") if isinstance(ent, dict) else None
    actual = hashlib.sha256((app / row["path"]).read_bytes()).hexdigest()
    print(("BOUND" if got and got.hex() == row["sha256"] == actual else "NOT-BOUND"), row["path"].split("/")[-1], row["sha256"][:12])
