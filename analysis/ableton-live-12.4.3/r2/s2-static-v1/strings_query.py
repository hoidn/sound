"""S2 static: locate container/version vocabulary and loader-message strings in a thin Mach-O 64 image.

Usage: python3 -I strings_query.py <Live.arm64> <out dir>
Writes <out>/strings_queries.json. File offsets are into the given thin slice; vmaddr is
section.addr + (offset - section.offset), i.e. the unslid address Ghidra shows for a
Mach-O loaded at its preferred base. Strings are data only; no code references are resolved.
"""
import hashlib, json, os, re, struct, sys

EXACT = ["MajorVersion", "MinorVersion", "SchemaChangeCount", "Creator", "Revision", "Ableton",
         "AbletonSchema", "TranslatorNumber", "TranslatorCount", "ChangeCount", "LiveSet",
         "GroupDevicePreset", "Groove", "Theme", ".als", ".alc", ".adv", ".adg", ".agr", ".alp", ".ask",
         "als", "alc", "adv", "adg", "agr", "alp", "ask", "Ableton Live ", "12.4.3", "12.0_12402", "12402"]
PHRASES = ["newer version", "older version", "could not be opened", "cannot be opened", "can't be opened",
           "could not be read", "cannot be read", "corrupt", "damaged", "unsupported", "not supported",
           "schema", "was created", "created with", "created by", "MinorVersion", "MajorVersion",
           "SchemaChangeCount", "Creator", "Ableton Live", "gzip", "inflate", "zlib", "xml", "translator",
           "invalid file", "unknown file", "file format", "upgrade", "Live Set", "could not load",
           "failed to load", "can not be", "cannot be loaded", "could not be loaded", "is not a valid",
           "%d.%d_%d", "_%d", "%s_%d", "d1"]
# (exact C-string text, what a cross-reference query should establish)
ANCHORS = [
    ("Ableton", "Root element name check on read; root name emitted on save"),
    ("MajorVersion", "Read: accepted values; Save: value written"),
    ("MinorVersion", "Read: parse of '<major>.<minor>_<translator>' and comparison with current translator; Save: value written"),
    ("SchemaChangeCount", "Read: optional or required, comparison rule; Save: value written (shipped schema 12.0_12402 ChangeCount=5)"),
    ("Creator", "Save: value written; Read: whether compared (same pooled string also used by browser code)"),
    ("Revision", "Save: value written (candidate BuildRevisions string); Read: ignored or checked"),
    ("Binary", "Stream-type dispatch neighbour of the root-attribute names"),
    ("Unknown Compound Stream Type", "Container detection: which stream types (binary/XML/gzip) exist and how chosen"),
    ("Can't read a gzip'ed document from a non-file", "Gzip detection path and its source restriction"),
    ("CompoundTool doesn't support XML documents", "Tool path restricted to non-XML streams"),
    ("sErrorDocumentCorruptWhileReading", "User-facing error key for corrupt documents; triggering conditions"),
    ("sErrorDocumentIsFromNewerVersion", "User-facing error key for newer documents; comparison that raises it"),
    ("sErrorDocumentIsFromSpecificNewerVersion", "Variant naming the newer version; which attribute supplies it"),
    ("sErrorClassesMissingFromSchema", "Error when document classes are absent from the schema"),
    ("TXmlCompoundParser", "XML document parser class; root of the reader call graph"),
    ("No document found", "Empty or rootless stream behaviour"),
    ("The document hasn't been created by \"", "Origin/Creator check: condition and expected prefix"),
    ("MajorVersion attribute missing from 'Ableton' root node", "Missing MajorVersion is an error"),
    ("MinorVersion attribute missing from 'Ableton' root node", "Missing MinorVersion is an error"),
    ("Unsupported MajorVersion (", "Accepted MajorVersion set or range"),
    ("Unsupported MinorVersion ($1)", "Accepted MinorVersion format and range"),
    ("Illegal tag format '$1'", "Element-name validation"),
    ("More than one document in one stream", "Multiple root documents rejected"),
    ("Expected 'Ableton' root node, got '$1' instead", "Wrong root element rejected"),
    ("Unknown class '$1' encountered", "Unknown element/class handling"),
    ("The document appears to be corrupt.", "Generic corrupt-document message and its triggers"),
    ("Unknown attribute '$1'", "Unknown attribute handling"),
    ("ByteBags are not supported in XML streams", "Binary-only payload types"),
    ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "XML declaration emitted on save"),
    ("Loading document ", "Load logging entry point"),
    ("Loaded document was created by ", "Logged Creator after load"),
    ("AbletonSchema", "Schema reader root check"),
    ("TranslatorNumber", "Schema translator attribute (newer form)"),
    ("TranslatorCount", "Schema translator attribute (older form)"),
    ("ChangeCount", "Schema change counter"),
    ("No schema found", "Schema lookup failure path"),
    ("Unsupported schema version", "Accepted schema Version values"),
    ("Live: Finding schema file failed: ", "Runtime schema-file lookup: whether Schema/*.txt is read at runtime"),
    ("Live: Reading schema files failed: ", "Runtime schema-file reading"),
    ("Schema: Current schema not found", "Current-schema self-check"),
    ("12.4.3", "Application version string; candidate Creator source"),
    ("12.0", "Adjacent to '12.4.3'; candidate MinorVersion prefix"),
    ("Ableton Live ", "Candidate Creator prefix"),
    ("Init: BuildRevisions: ", "Followed by a 40-hex build revision; candidate Revision value"),
    ("e3d8be4d07c71dbd4de9e4183bf90652f680375b", "Candidate Revision value written by 12.4.3"),
    ("Ableton Live Set", "Document-type registry: .als"),
    ("Ableton Live Clip", "Document-type registry: .alc"),
    ("Ableton Live Pack", "Document-type registry: .alp"),
    (".als", "Extension registry"), (".alc", "Extension registry"), (".adv", "Extension registry"),
    (".adg", "Extension registry"), (".agr", "Extension registry"), (".alp", "Extension registry"),
    (".ask", "Extension registry"),
]
# raw byte anchors (no NUL framing): label, bytes, purpose
BYTE_ANCHORS = [
    ("magic AB1E1234", bytes.fromhex("ab1e1234"), "Binary stream magic (matches Misc/MidiPreHear.adv)"),
    ("magic AB1E5678", bytes.fromhex("ab1e5678"), "Binary stream magic (matches 103 .agr and Metadata.cfg)"),
    ("UTF-16BE 'Ableton#'", "Ableton#".encode("utf-16-be"), "Text-stream signature candidate"),
    ("UTF-16LE 'Ableton#'", "Ableton#".encode("utf-16-le"), "Text-stream signature candidate"),
]
STR_RE = re.compile(rb"[\x20-\x7e\t\r\n]{3,}")


def sections(img):
    magic, cpu, _, ftype, ncmds, _, _, _ = struct.unpack_from("<IiiIIIII", img, 0)
    if magic != 0xFEEDFACF:
        raise SystemExit(f"not a thin little-endian Mach-O 64: magic {magic:#x}")
    out, off = [], 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from("<II", img, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            seg = img[off + 8:off + 24].rstrip(b"\0").decode()
            nsects = struct.unpack_from("<I", img, off + 64)[0]
            for i in range(nsects):
                s = off + 72 + 80 * i
                sect = img[s:s + 16].rstrip(b"\0").decode()
                addr, sz, foff = struct.unpack_from("<QQI", img, s + 32)
                out.append({"seg": seg, "sect": sect, "addr": addr, "size": sz, "offset": foff})
        off += size
    return out


def locate(secs, foff):
    for s in secs:
        if s["offset"] and s["offset"] <= foff < s["offset"] + s["size"]:
            return f'{s["seg"]},{s["sect"]}', s["addr"] + foff - s["offset"]
    return None, None


def _fmt(loc):
    return loc[0], hex(loc[1]) if loc[1] is not None else None


def main(path, out):
    img = open(path, "rb").read()
    secs = sections(img)
    strings = [(m.start(), m.group()) for m in STR_RE.finditer(img)]
    exact = {}
    for w in EXACT:
        hits = []
        for m in re.finditer(re.escape(b"\0" + w.encode() + b"\0"), img):
            sec, va = locate(secs, m.start() + 1)
            hits.append({"offset": m.start() + 1, "section": sec, "vmaddr": hex(va) if va else None})
        utf16 = [m.start() for m in re.finditer(re.escape(w.encode("utf-16-le") + b"\0\0"), img)]
        exact[w] = {"cstring_exact": hits, "substring_count": img.count(w.encode()),
                    "utf16le_terminated_offsets": utf16[:20], "utf16le_count": len(utf16)}
    phrases = {}
    for p in PHRASES:
        rx = re.compile(re.escape(p.encode()), re.I)
        hits = [(o, s) for o, s in strings if rx.search(s)]
        rows = []
        for o, s in hits[:150]:
            sec, va = locate(secs, o)
            rows.append({"offset": o, "section": sec, "vmaddr": hex(va) if va else None, "text": s.decode("ascii")[:300]})
        w16 = len(re.findall(re.escape(p.encode("utf-16-le")), img, re.I)) if len(p) > 3 else None
        phrases[p] = {"strings_matching": len(hits), "shown": rows, "utf16le_occurrences": w16}
    anchor_rows = []
    for text, purpose in ANCHORS:
        offs = [m.start() + 1 for m in re.finditer(re.escape(b"\0" + text.encode() + b"\0"), img)]
        anchor_rows.append({"text": text, "purpose": purpose, "cstring_count": len(offs),
                            "hits": [dict(zip(("offset", "section", "vmaddr"), (o, *_fmt(locate(secs, o))))) for o in offs]})
    for label, pat, purpose in BYTE_ANCHORS:
        offs = [m.start() for m in re.finditer(re.escape(pat), img)]
        anchor_rows.append({"text": label, "purpose": purpose, "cstring_count": None,
                            "hits": [dict(zip(("offset", "section", "vmaddr"), (o, *_fmt(locate(secs, o))))) for o in offs]})
    json.dump({"image": path, "size": len(img), "sha256": hashlib.sha256(img).hexdigest(),
               "string_regex": STR_RE.pattern.decode(), "sections": secs, "anchors": anchor_rows, "exact": exact, "phrases": phrases},
              open(os.path.join(out, "strings_queries.json"), "w"), indent=1)


if __name__ == "__main__":
    t = [{"seg": "__TEXT", "sect": "__cstring", "addr": 0x100001000, "size": 0x10, "offset": 0x1000}]
    assert locate(t, 0x1004) == ("__TEXT,__cstring", 0x100001004) and locate(t, 0x2000) == (None, None)
    main(sys.argv[1], sys.argv[2])
