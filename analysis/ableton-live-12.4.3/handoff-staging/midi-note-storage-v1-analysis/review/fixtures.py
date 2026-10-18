"""Reviewer check (analyst-side): gzip form of every fixture (10-byte header, one member, CRC-32 and
length trailer, nothing after it), text form (UTF-8, LF, final newline, tabs only as indentation),
distinctness, and the line diff of each fixture against its base (MNS-001 for the base notes,
MNS-039 for the base list), so each edit can be compared with the case purpose.
usage: python3 -I fixtures.py <package dir>"""
import difflib, json, struct, sys, zlib
from pathlib import Path
pkg = Path(sys.argv[1]); cases = json.loads((pkg / "cases.json").read_text())["cases"]
HDR = bytes.fromhex("1f8b0800000000000213")
def text(p):
    raw = p.read_bytes(); d = zlib.decompressobj(-15); body = d.decompress(raw[10:]); tail = d.unused_data
    crc, size = struct.unpack("<II", tail[:8])
    ok = raw[:10] == HDR and d.eof and len(tail) == 8 and crc == zlib.crc32(body) and size == len(body)
    t = body.decode("utf-8")
    ok = ok and "\r" not in t and t.endswith("\n") and all(not l.lstrip("\t").startswith(("\t", " ")) for l in t.split("\n"))
    return ok, t
base = {k: text(pkg / f"fixtures/{k}.als")[1].split("\n") for k in ("MNS-001", "MNS-039")}
seen = {}
for c in cases:
    ok, t = text(pkg / c["input"]); lines = t.split("\n")
    b = "MNS-039" if "PerNoteEventList" in t else "MNS-001"
    seen.setdefault(t, []).append(c["id"])
    diff = [l for l in difflib.unified_diff(base[b], lines, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    print(f"{c['id']} form={'ok' if ok else 'BAD'} base={b} | {c['purpose']}")
    for l in diff:
        print("    " + l.strip())
print("distinct inputs:", len(seen), "of", len(cases), "| duplicates:", [v for v in seen.values() if len(v) > 1])
