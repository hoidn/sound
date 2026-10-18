"""Recover the file-type registry calls from FUN_10029bb10 pseudocode (Ableton_Index.arm64).

Usage: python3 -I file_types.py <pseudocode.c> <out.tsv>
The function calls FUN_10029e710(id, fourcc, description, &extension_vector, mac_type, flag) once per
type, after storing extension string literals into the vector's buffer. Output columns: id, fourcc
(ASCII), description, extensions, mac type (ASCII or 0), flag. Static derivation from decompiler
output; the meaning of 'flag' is not established.
"""
import re, sys

def fourcc(v):
    n = int(v, 16)
    if n == 0:
        return "0"
    b = n.to_bytes(4, "big")
    return b.decode("latin-1") if all(32 <= c < 127 for c in b) else hex(n)

ASSIGN = re.compile(r"^\s*\*?(local_[0-9a-f]+)(?:\[(\d+)\])?\s*=\s*\"([^\"]*)\";")
CALL = re.compile(r"FUN_10029e710\((0x[0-9a-f]+|\d+),(0x[0-9a-f]+|\d+),\"([^\"]*)\",&(local_[0-9a-f]+),(0x[0-9a-f]+|\d+),(\d+)\)")
exts, rows = {}, []
for line in open(sys.argv[1]):
    m = ASSIGN.match(line)
    if m:
        exts.setdefault(m.group(1), {})[int(m.group(2) or 0)] = m.group(3)
        continue
    m = CALL.search(line)
    if m:
        ident, code, desc, var, mac, flag = m.groups()
        ext = [e for _, e in sorted(exts.pop(var, {}).items())]
        rows.append((int(ident, 0), fourcc(hex(int(code, 0))), desc, " ".join(ext), fourcc(hex(int(mac, 0))), flag))
with open(sys.argv[2], "w") as o:
    o.write("id\tfourcc\tdescription\textensions\tmac_type\tflag\n")
    for r in sorted(rows):
        o.write("\t".join(map(str, r)) + "\n")
print(len(rows), "registrations")
