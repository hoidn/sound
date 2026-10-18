"""S2 static: inventory shipped Ableton documents (container, gzip header, XML envelope).

Usage: python3 -I doc_inventory.py <App-Resources dir> <out dir>
Reads the bundle read-only. Writes documents.jsonl, magic_scan.json, inputs.jsonl.
Standard library only. AppleDouble `._*` files are skipped and counted.
"""
import hashlib, json, os, re, struct, sys, zlib
import xml.parsers.expat

DOC_EXTS = {"als", "alc", "adv", "adg", "agr", "alp", "ask", "amxd", "xmp"}
GZIP_FLAGS = [(1, "FTEXT"), (2, "FHCRC"), (4, "FEXTRA"), (8, "FNAME"), (16, "FCOMMENT")]
DECL_RE = re.compile(rb"""^<\?xml\s+version=(["'])([^"']*)\1(?:\s+encoding=(["'])([^"']*)\3)?(?:\s+standalone=(["'])([^"']*)\5)?\s*\?>""")


def ext_of(name):
    return name.rsplit(".", 1)[1].lower() if "." in name else "(none)"


def parse_gzip_header(b):
    """RFC 1952 member header. Returns dict; raises ValueError on short/invalid header."""
    if b[:2] != b"\x1f\x8b":
        raise ValueError("not gzip")
    cm, flg, mtime, xfl, os_b = b[2], b[3], struct.unpack_from("<I", b, 4)[0], b[8], b[9]
    pos, h = 10, {"cm": cm, "flg": flg, "flags": [n for bit, n in GZIP_FLAGS if flg & bit],
                  "reserved_bits": flg & 0xE0, "mtime": mtime, "xfl": xfl, "os": os_b}
    if flg & 4:
        (xlen,) = struct.unpack_from("<H", b, pos); h["fextra_len"] = xlen; pos += 2 + xlen
    if flg & 8:
        end = b.index(b"\0", pos); h["fname"] = b[pos:end].decode("latin-1"); pos = end + 1
    if flg & 16:
        end = b.index(b"\0", pos); h["fcomment"] = b[pos:end].decode("latin-1"); pos = end + 1
    if flg & 2:
        pos += 2
    h["header_len"] = pos
    return h


def gunzip(b):
    """Decompress first gzip member (CRC32/ISIZE verified by zlib). Returns payload, trailing bytes count, trailer isize."""
    d = zlib.decompressobj(31)
    out = d.decompress(b) + d.flush()
    if not d.eof:
        raise ValueError("truncated gzip member")
    end = len(b) - len(d.unused_data)
    return out, len(d.unused_data), struct.unpack_from("<I", b, end - 4)[0]


def xml_envelope(p):
    """Declaration, root element/attrs (ordered), first child, well-formedness of whole payload."""
    r = {"bom": p.startswith(b"\xef\xbb\xbf")}
    body = p[3:] if r["bom"] else p
    m = DECL_RE.match(body)
    r["decl"] = body[: m.end()].decode("latin-1") if m else None
    r["decl_version"] = m.group(2).decode() if m else None
    r["decl_encoding"] = m.group(4).decode() if m and m.group(4) else None
    r["decl_quote"] = m.group(1).decode() if m else None
    r["crlf"] = b"\r\n" in p
    r["ends_with_newline"] = p.endswith(b"\n")
    st = {"depth": 0, "root": None, "root_attrs": None, "first_child": None, "elements": 0}
    px = xml.parsers.expat.ParserCreate()
    px.ordered_attributes = True

    def start(name, attrs):
        st["elements"] += 1
        if st["depth"] == 0:
            st["root"], st["root_attrs"] = name, [[attrs[i], attrs[i + 1]] for i in range(0, len(attrs), 2)]
            st["root_line"], st["root_byte"] = px.CurrentLineNumber, px.CurrentByteIndex
        elif st["depth"] == 1 and st["first_child"] is None:
            st["first_child"] = name
        st["depth"] += 1

    def end(name):
        st["depth"] -= 1

    px.StartElementHandler, px.EndElementHandler = start, end
    try:
        px.Parse(p, True)
        r["well_formed"], r["parse_error"] = True, None
    except xml.parsers.expat.ExpatError as e:
        r["well_formed"], r["parse_error"] = False, f"{e} (line {e.lineno} col {e.offset})"
    r.update(st)
    del r["depth"]
    return r


def classify_magic(head):
    if head[:2] == b"\x1f\x8b":
        return "gzip"
    if head[:2] == b"\xab\x1e":
        return "ab1e-binary"
    h = head[3:] if head.startswith(b"\xef\xbb\xbf") else head
    if h.lstrip()[:5] == b"<?xml" or h.lstrip()[:1] == b"<":
        return "xml-like"
    return "other"


def main(root, out):
    os.makedirs(out, exist_ok=True)
    appledouble, magic, docs, inputs = {}, {}, [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            path = os.path.join(dirpath, fn)
            if os.path.islink(path) or not os.path.isfile(path):
                continue
            if fn.startswith("._"):
                appledouble[ext_of(fn[2:])] = appledouble.get(ext_of(fn[2:]), 0) + 1
                continue
            ext = ext_of(fn)
            rel = os.path.relpath(path, root)
            with open(path, "rb") as f:
                head = f.read(4096)
            kind = classify_magic(head)
            ableton = None
            if kind == "gzip" and ext not in DOC_EXTS:
                try:  # peek at decompressed start only
                    ableton = b"<Ableton" in zlib.decompressobj(31).decompress(open(path, "rb").read(1 << 16), 4096)
                except zlib.error:
                    ableton = False
            elif kind == "xml-like":
                ableton = b"<Ableton" in head
            key = f"{kind}{'+ableton' if ableton else ''}"
            magic.setdefault(ext, {}).setdefault(key, 0)
            magic[ext][key] += 1
            if ext not in DOC_EXTS and not ableton and kind != "ab1e-binary":
                continue
            raw = open(path, "rb").read()
            sha = hashlib.sha256(raw).hexdigest()
            inputs.append({"path": rel, "size": len(raw), "sha256": sha})
            row = {"path": rel, "ext": ext, "top": rel.split(os.sep, 1)[0], "size": len(raw), "sha256": sha,
                   "magic16": raw[:16].hex(), "container": kind}
            if kind == "gzip":
                try:
                    row["gzip"] = parse_gzip_header(raw)
                    payload, trailing, isize = gunzip(raw)
                    row["gzip"].update(trailing_bytes=trailing, isize=isize)
                    row["payload_size"], row["payload_sha256"] = len(payload), hashlib.sha256(payload).hexdigest()
                    row["xml"] = xml_envelope(payload)
                except (ValueError, zlib.error) as e:
                    row["error"] = f"gzip: {e}"
            elif kind == "xml-like":
                row["payload_size"], row["payload_sha256"] = len(raw), sha
                row["xml"] = xml_envelope(raw)
            docs.append(row)
    with open(os.path.join(out, "documents.jsonl"), "w") as f:
        for r in docs:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    with open(os.path.join(out, "inputs.jsonl"), "w") as f:
        for r in inputs:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    json.dump({"root": root, "appledouble_skipped_by_ext": dict(sorted(appledouble.items())),
               "appledouble_skipped_total": sum(appledouble.values()),
               "magic_by_ext": dict(sorted(magic.items()))}, open(os.path.join(out, "magic_scan.json"), "w"),
              indent=1, sort_keys=True)
    print(len(docs), "documents;", sum(appledouble.values()), "AppleDouble skipped")


def _selftest():
    import gzip, io
    buf = io.BytesIO()
    with gzip.GzipFile(filename="x.als", mode="wb", fileobj=buf, mtime=7) as g:
        g.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<Ableton MajorVersion="5" Creator="t"><LiveSet/></Ableton>\n')
    b = buf.getvalue()
    h = parse_gzip_header(b)
    assert h["flags"] == ["FNAME"] and h["fname"] == "x.als" and h["mtime"] == 7, h
    p, trailing, isize = gunzip(b + b"junk")
    assert trailing == 4 and isize == len(p)
    x = xml_envelope(p)
    assert x["root"] == "Ableton" and x["root_attrs"][0] == ["MajorVersion", "5"] and x["first_child"] == "LiveSet"
    assert x["decl_encoding"] == "UTF-8" and x["well_formed"]
    assert xml_envelope(b"<?xml version='1.0' encoding='UTF-8'?><a><b/>")["well_formed"] is False


if __name__ == "__main__":
    _selftest()
    main(sys.argv[1], sys.argv[2])
