"""S1 native query anchors: exact string and symbol locations in Live.arm64.

Usage: python3 -I s1_anchors.py <Live.arm64> <schema.txt> <out.json>
Parses the thin Mach-O 64 header for segments/sections and LC_SYMTAB, then for
each term records NUL-delimited ASCII hits, ASCII hits that are only the
suffix of a longer C string, and \\0\\0-delimited UTF-16LE hits, each with file
offset, section and static VM address. Also lists RTTI-name strings and symbol
table entries for S1 classes, UTF-16 member-name strings ("mp"/"m" + field)
with neighbouring __ustring entries, and how many schema class and field names
have each string form. Static byte facts only: no reference is resolved.
"""
import hashlib, json, re, struct, subprocess, sys
import xml.etree.ElementTree as ET

VOCAB = ["Transport", "LoopOn", "LoopStart", "LoopLength", "LoopIsSongStart", "CurrentTime",
         "PhaseNudgeTempo", "PunchIn", "PunchOut", "MetronomeTickDuration", "DrawMode",
         "Tempo", "TimeSignature", "TimeSignatures", "TimeSignatureId", "IsTempoEnabled",
         "IsTimeSignatureEnabled", "RemoteableTimeSignature", "Numerator", "Denominator",
         "Time", "Manual", "MidiControllerRange", "Min", "Max", "AutomationTarget",
         "ModulationTarget", "LockEnvelope", "LomId", "Value", "Id", "MainTrack", "MasterTrack",
         "DeviceChain", "Mixer", "Scenes", "Scene", "LiveSet", "Ableton", "MajorVersion",
         "MinorVersion", "SchemaChangeCount", "Creator", "Revision", "AutomationEnvelope",
         "EnvelopeTarget", "PointeeId", "Events", "FloatEvent", "EnumEvent", "true", "false",
         "LoopOnKeyMidi", "TapTempoKeyMidi", "AbletonSchema", "TranslatorNumber",
         "TranslatorCount", "ChangeCount", "InternalName", "LiveDocument", "TrackDevice",
         "TimeableSongTempo", "TimeableTimeSignature", "SingleTimeSignatureManager",
         "MainTrackDevice", "MainTrackDeviceChain",
         "%g", "%.8g", "%.9g", "%.15g", "%.16g", "%.17g", "%f", "%.6f"]
CLASSES = ["ATransport", "ALoopOn", "ALoopStart", "ALoopLength", "ACurrentTime",
           "ATimeableSongTempo", "ATimeableTimeSignature", "ATimeSignatureStringConverter",
           "ATimeSignatureNumerator", "ATimeSignatureDenominator", "ASingleTimeSignatureManager",
           "ARemoteableTimeSignature", "AMainTrackDevice", "ASongTempoArrangementAutomationRecorder",
           "ATimeableSongTempoOceanCreator", "ATimeableTimeSignatureOceanCreator"]


def macho(data):
    magic, cpu, _, _, ncmds, _, _, _ = struct.unpack_from("<IiiIIIII", data, 0)
    if magic != 0xFEEDFACF:
        raise ValueError(f"not a thin little-endian Mach-O 64: magic {magic:#x}")
    off, sects, symtab = 32, [], None
    for _ in range(ncmds):
        cmd, size = struct.unpack_from("<II", data, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            nsects = struct.unpack_from("<I", data, off + 64)[0]
            for i in range(nsects):
                s = off + 72 + 80 * i
                sect, seg = (data[s:s + 16].rstrip(b"\0").decode(), data[s + 16:s + 32].rstrip(b"\0").decode())
                addr, ssize, foff = struct.unpack_from("<QQI", data, s + 32)
                if foff:
                    sects.append((foff, foff + ssize, addr, f"{seg},{sect}"))
        elif cmd == 0x2:  # LC_SYMTAB
            symtab = struct.unpack_from("<IIII", data, off + 8)
            sects.append((symtab[2], symtab[2] + symtab[3], None, "__LINKEDIT:symtab-strings"))
        elif cmd in (0x22, 0x80000022):  # LC_DYLD_INFO(_ONLY)
            v = struct.unpack_from("<10I", data, off + 8)
            for i, name in enumerate(["rebase", "bind", "weak-bind", "lazy-bind", "export-trie"]):
                sects.append((v[2 * i], v[2 * i] + v[2 * i + 1], None, f"__LINKEDIT:{name}"))
        off += size
    return cpu, sects, symtab


def locate(sects, foff):
    for lo, hi, addr, name in sects:
        if lo <= foff < hi:
            return name, None if addr is None else hex(addr + foff - lo)
    return None, None


def cneighbours(data, p, n=3):
    """n C strings before and after the one starting at p (context only)."""
    lo = p
    for _ in range(n):
        lo = data.rfind(b"\0", 0, lo - 1) + 1
    hi = p
    for _ in range(n + 1):
        hi = data.index(b"\0", hi) + 1
    return [x.decode("latin-1")[:60] for x in data[lo:hi - 1].split(b"\0")]


S1_PATH = re.compile(r"^[A-Za-z]+(/[A-Za-z]+)+$")
S1_TERMS = ("Bpm", "Tempo", "Loop", "Signature", "Transport", "CurrentTime", "MasterTrack",
            "MasterChain", "MasterDevice", "MainTrack")


def path_strings(data, sects):
    """Slash-separated element paths in __TEXT,__cstring mentioning S1 terms."""
    lo, blob, _ = section(data, sects, "__TEXT,__cstring")
    out, p = [], 0
    for x in blob.split(b"\0"):
        t = x.decode("latin-1")
        if S1_PATH.match(t) and any(k in t for k in S1_TERMS):
            out.append([hex(lo + p), locate(sects, lo + p)[1], t])
        p += len(x) + 1
    return out


def hits(data, sects, term):
    a, u = term.encode(), term.encode("utf-16-le")
    out = {"ascii_exact": [], "ascii_suffix_of": [], "utf16_exact": [], "ascii_any": data.count(a),
           "utf16_any": data.count(u)}
    for m in re.finditer(re.escape(a + b"\0"), data):
        p = m.start()
        if p and data[p - 1] == 0:
            out["ascii_exact"].append([hex(p), *locate(sects, p), cneighbours(data, p)])
        elif p and 0x20 <= data[p - 1] < 0x7F:
            start = data.rfind(b"\0", 0, p) + 1
            out["ascii_suffix_of"].append([hex(p), *locate(sects, p),
                                           data[start:p + len(a)].decode("latin-1")[-80:]])
    for m in re.finditer(re.escape(u + b"\0\0"), data):
        p = m.start()
        if p % 2 == 0 and p >= 2 and data[p - 2:p] == b"\0\0":
            out["utf16_exact"].append([hex(p), *locate(sects, p)])
    for k in ("ascii_exact", "ascii_suffix_of", "utf16_exact"):  # ponytail: cap lists, counts kept
        out[f"{k}_count"] = len(out[k])
        out[k] = out[k][:25]
    return out


MESSAGES = [  # UTF-16 document-framework messages (exact __ustring entries)
    'Member "{}" of Class {} is missing',
    'Type mismatch: expected to set a value of type {}, but the document contained a value of type {}',
    'Type mismatch: expected to get a value of type {}, but the document contained a value of type {}',
    'Member {} has wrong class ({}) or type ({})',
    'Unknown class "{}" found',
    "Unexpected node '{}'",
    'Parse error at {}: Encountered "{}"; expected "{}".',
    'Class mismatch for {}/{} on line/offset {}: expected {}, found {}',
    'Missing compound model for class "{}"',
    'Compound model for class {} found twice',
    'Wrong class found. Expected a "{}" or subclass, found a "{}"',
    'Non-Ascii characters in XML element/attribute names are not supported',
    'ACompound::SaveXmlStream',
    'Unsupported -DocumentStreamType value \u201c$1\u201d; supported values are \u201cXML\u201d, \u201cBinary\u201d, and \u201cText\u201d.',
    'The document {} is corrupt: unknown base type id {}',
    'Current schema has changed', 'Current schema corrupt', 'Current schema not found',
    '0123456789+-.', 'Invalid value for control: "{}"']
ASCII_MESSAGES = [  # exact __TEXT,__cstring entries relevant to S1 value handling
    "Value ", " out of range for '", "Enum value out of range", "Enum (Float) value out of range",
    "Enum out of range", "Event of unautomated parameter is not at 0.0", "Unknown event type found: ",
    "Unexpected event type while converting a float parameter automation.",
    "CloseUnautomatedAutomationLanesAfterDocumentTranslation",
    "Incorrect node type for this translator. Should be TrackDevice, SongPrefData or Song only.",
    "Tempo out of range", "SignatureNumerator value is out of range",
    "SignatureDenominator value is out of range", "TXmlCompoundParser"]
MEMBER_FIELDS = ["Transport", "LoopOn", "LoopStart", "LoopLength", "LoopIsSongStart",
                 "CurrentTime", "PhaseNudgeTempo", "PunchIn", "PunchOut", "MetronomeTickDuration",
                 "DrawMode", "LoopOnKeyMidi", "MainTrack", "Scenes", "Tempo", "TimeSignature",
                 "Manual", "MidiControllerRange", "AutomationTarget", "ModulationTarget",
                 "TimeSignatures", "Numerator", "Denominator", "LomId", "Value", "Id"]


def section(data, sects, name):
    lo, hi, addr, _ = next(x for x in sects if x[3] == name)
    return lo, data[lo:hi], addr


def cstrings(data, sects):
    _, blob, _ = section(data, sects, "__TEXT,__cstring")
    return set(blob.split(b"\0"))


def ustrings(data, sects):
    """Sequential UTF-16LE strings of __TEXT,__ustring: [(file offset, text)]."""
    lo, blob, _ = section(data, sects, "__TEXT,__ustring")
    out, p = [], 0
    while p < len(blob):
        q = p
        while q + 1 < len(blob) and blob[q:q + 2] != b"\0\0":
            q += 2
        if q > p:
            out.append((lo + p, blob[p:q].decode("utf-16-le", "replace")))
        p = q + 2
    return out


def members(sects, ulist):
    index = {t: i for i, (_, t) in reversed(list(enumerate(ulist)))}
    out = {}
    for f in MEMBER_FIELDS:
        for name in (f"mp{f}", f"m{f}"):
            i = index.get(name)
            if i is not None:
                off = ulist[i][0]
                out[name] = {"offset": hex(off), "vmaddr": locate(sects, off)[1],
                             "count": sum(t == name for _, t in ulist),
                             "neighbours": [t for _, t in ulist[max(0, i - 4):i + 5]]}
    return out


def coverage(schema, cset, uset, factories):
    """How many latest-schema class/field names have each static string form."""
    root = ET.parse(schema).getroot()
    classes = {c.tag for c in root}
    fields = {f.tag for c in root for f in c}
    only_fields = fields - classes
    def frac(names, pred):
        hit = sorted(n for n in names if pred(n))
        return {"total": len(names), "hit": len(hit),
                "missing_examples": sorted(set(names) - set(hit))[:15]}
    return {
        "schema": schema,
        "class_names_ascii_cstring": frac(classes, lambda n: n.encode() in cset),
        "class_names_with_SNewCompound_A": frac(classes, lambda n: f"A{n}" in factories),
        "field_only_names_ascii_cstring": frac(only_fields, lambda n: n.encode() in cset),
        "field_names_utf16_member_mp_or_m": frac(fields, lambda n: f"mp{n}" in uset or f"m{n}" in uset),
        "class_names_utf16_member_mp_or_m": frac(classes, lambda n: f"mp{n}" in uset or f"m{n}" in uset),
    }


def factory_classes(data, symtab):
    symoff, nsyms, stroff, _ = symtab
    out = set()
    for i in range(nsyms):
        strx = struct.unpack_from("<I", data, symoff + 16 * i)[0]
        name = data[stroff + strx:data.index(b"\0", stroff + strx)].decode("latin-1")
        m = re.fullmatch(r"__Z12SNewCompoundI(\d+)(\w+?)E4TPtrI9ACompoundEv", name)
        if m and len(m.group(2)) == int(m.group(1)):
            out.add(m.group(2))
    return out


def symbols(data, symtab, sects):
    symoff, nsyms, stroff, _ = symtab
    rows = []
    for i in range(nsyms):
        strx, ntype, nsect, _, value = struct.unpack_from("<IBBHQ", data, symoff + 16 * i)
        end = data.index(b"\0", stroff + strx)
        name = data[stroff + strx:end].decode("latin-1")
        if any(re.search(rf"\d{c}(E|$|[^A-Za-z0-9_])", name) for c in CLASSES) and \
                re.search(r"__ZT[ISV]|SNewCompound|AMember", name):
            rows.append([hex(value), name])
    names = subprocess.run(["c++filt", "-_"], input="\n".join(n for _, n in rows),
                           capture_output=True, text=True, check=True).stdout.splitlines()
    return [[a, n, d] for (a, n), d in zip(rows, names)]


def main(binary, schema, out_path):
    data = open(binary, "rb").read()
    cpu, sects, symtab = macho(data)
    ulist = ustrings(data, sects)
    factories = factory_classes(data, symtab)
    rtti = {}
    for c in CLASSES:
        for name in (f"{len(c)}{c}", f"7AMemberI{len(c)}{c}E"):
            b = name.encode() + b"\0"
            rtti[name] = [[hex(m.start()), *locate(sects, m.start())]
                          for m in re.finditer(re.escape(b), data)
                          if m.start() and data[m.start() - 1] == 0]
    out = {"binary": binary, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
           "cputype": cpu, "vm_address_note": "static VM address = section addr + (offset - section fileoff)",
           "vocab": {t: hits(data, sects, t) for t in VOCAB},
           "rtti_names": rtti,
           "symbols": symbols(data, symtab, sects),
           "utf16_members": members(sects, ulist),
           "cstring_paths": path_strings(data, sects),
           "ascii_messages": {m: [[hex(o), locate(sects, o)[1], cneighbours(data, o, 2)]
                                  for o in (x.start() + 1 for x in re.finditer(
                                      re.escape(b"\0" + m.encode() + b"\0"), data))
                                  if locate(sects, o)[0] == "__TEXT,__cstring"]
                              for m in ASCII_MESSAGES},
           "constant_minus_63072000": {
               "double_le": [[hex(m.start()), *locate(sects, m.start())]
                             for m in re.finditer(re.escape(struct.pack("<d", -63072000.0)), data)],
               "float_le": [[hex(m.start()), *locate(sects, m.start())]
                            for m in re.finditer(re.escape(struct.pack("<f", -63072000.0)), data)]},
           "utf16_messages": {m: [[hex(o), locate(sects, o)[1]] for o, t in ulist if t == m]
                              for m in MESSAGES},
           "schema_coverage": coverage(schema, cstrings(data, sects), {t for _, t in ulist}, factories),
           "SNewCompound_classes": len(factories)}
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
