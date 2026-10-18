# Reviewer check: independent fixture inspection and manifest hash verification of an exported package copy.
import hashlib, json, re, struct, sys, zlib
from pathlib import Path
d = Path(sys.argv[1])
man = json.loads((d / "manifest.json").read_text())
listed = {f["path"]: f for f in man["files"]}
actual = sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")
print("inventory equal:", sorted(listed) == actual, len(actual))
bad = [p for p, f in listed.items() if hashlib.sha256((d / p).read_bytes()).hexdigest() != f["sha256"] or (d / p).stat().st_size != f["bytes"]]
print("hash/size mismatches:", bad)
TEMPLATE = ['MajorVersion="5"', 'MinorVersion="12.0_12402"', 'SchemaChangeCount="1"', 'Creator="Ableton Live 12.4.3"',
            'Revision="0123456789abcdef0123456789abcdef01234567"']
DECL = '<?xml version="1.0" encoding="UTF-8"?>'
cases = json.loads((d / "cases.json").read_text())["cases"]
inputs = set()
for c in cases:
    raw = (d / c["input"]).read_bytes()
    inputs.add(raw)
    note = []
    if raw[:2] == b"\x1f\x8b":
        assert c["container"] == "gzip"
        assert raw[:10] == bytes.fromhex("1f8b0800000000000213"), "header"
        o = zlib.decompressobj(-15)
        text = o.decompress(raw[10:]); text += o.flush()
        assert o.eof
        crc, isize = struct.unpack("<II", o.unused_data[:8])
        assert len(o.unused_data) == 8, "trailing"
        assert crc == zlib.crc32(text) and isize == len(text), "trailer"
    else:
        assert c["container"] == "uncompressed"
        text = raw
    s = text.decode("utf-8")
    assert "\r" not in s and (s == "" or s.endswith("\n"))
    lines = s.split("\n")[:-1]
    m = re.search(r"<(\w+)((?: \w+=\"[^\"]*\")*)( ?/?)>", s)
    attrs = re.findall(r'\w+="[^"]*"', m.group(2)) if m else []
    diffs = []
    if s and not s.startswith(DECL): diffs.append("prefix=%r" % s[:s.find("<?") if "<?" in s else 8])
    if m and m.group(1) != "Ableton": diffs.append("root=" + m.group(1))
    if attrs != TEMPLATE:
        missing = [a for a in TEMPLATE if a not in attrs]; extra = [a for a in attrs if a not in TEMPLATE]
        if not missing and not extra: diffs.append("order=" + ",".join(a.split("=")[0] for a in attrs))
        else: diffs.append("attrs -%s +%s" % (missing, extra))
    if "\t<LiveSet />" not in s and s: diffs.append("no LiveSet")
    if s and not s.rstrip("\n").endswith("</%s>" % (m.group(1) if m else "")): diffs.append("no end tag")
    print(c["id"], c["container"][:4], len(raw), len(lines), c["expected"], "|", "; ".join(diffs) or "template")
print("distinct inputs:", len(inputs), "of", len(cases))
