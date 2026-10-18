"""Stage the als-container-v1 release candidate (analyst side; not reviewed, not released).

Run from any directory with CPython 3.11 and -I:
  python3.11 -I build_als.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3.11 -I build_als.py seal           # manifest files[], author-validation.json, traceability.json
  python3.11 -I build_als.py verify <dir>   # hashes, inventory, links, deny-list of an exported copy

Fixtures are authored here from a four-line template; no shipped file is read. Expected outcomes
are the hand-authored static derivations in CASES. The seal step cross-checks every expectation
against model(), an independent re-statement of the released rules that uses the real shipped
schema-name list from the S2 static run. It shares the same static evidence and is not an oracle.
README.md, AGENTS.md and spec.md in the stage directory are hand-written.
"""
import hashlib, json, re, struct, sys, zlib
import pyexpat
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "als-container-v1"
SCHEMAS = ROOT / "analysis/ableton-live-12.4.3/r2/s2-static-v1/out/schemas.json"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"
PROV = "static-derived; not observed reference output"
GZ_HEADER = bytes.fromhex("1f8b0800000000000213")  # FLG 0, MTIME 0, XFL 2, OS 19: the form of all 25 shipped .als
DECL = '<?xml version="1.0" encoding="UTF-8"?>\n'
BOM = b"\xef\xbb\xbf"
BASE = [("MajorVersion", "5"), ("MinorVersion", "12.0_12402"), ("SchemaChangeCount", "1"),
        ("Creator", "Ableton Live 12.4.3"), ("Revision", "0123456789abcdef0123456789abcdef01234567")]
A, R = "envelope-accepted", "refused"
C, N, U = "corrupt-document", "newer-version", "unspecified"


def doc(attrs=BASE, root="Ableton", child=True, decl=True, end=True):
    a = " ".join(f'{k}="{v}"' for k, v in attrs)
    text = (DECL if decl else "") + f"<{root} {a}>\n" + ("\t<LiveSet />\n" if child else "") + (f"</{root}>\n" if end else "")
    return text.encode("utf-8")


def gz(data):
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    return GZ_HEADER + c.compress(data) + c.flush() + struct.pack("<II", zlib.crc32(data), len(data))


def put(name, value):
    return [(k, value if k == name else v) for k, v in BASE]


def drop(*names):
    return [(k, v) for k, v in BASE if k not in names]


# (number, purpose, requirement suffixes, fixture bytes, outcome, class); class None when accepted
CASES = [
    (1, "Template document in a gzip container", ["001"], gz(doc()), A, None),
    (2, "Template document uncompressed", ["001"], doc(), A, None),
    (3, "UTF-8 byte order mark before the XML declaration", ["001"], BOM + doc(), R, U),
    (4, "Line feed before the XML declaration", ["001"], b"\n" + doc(), R, U),
    (5, "No XML declaration: the file starts with the root element", ["001"], doc(decl=False), R, U),
    (6, "gzip container whose content starts with a UTF-8 byte order mark", ["001"], gz(BOM + doc()), R, U),
    (7, "Empty file", ["001"], b"", R, U),
    (8, "gzip content truncated before the root end tag (not well-formed)", ["001"], gz(doc(end=False)), R, C),
    (9, "Root element named Live", ["002"], gz(doc(root="Live")), R, C),
    (10, "Root element named ableton (letter case differs)", ["002"], gz(doc(root="ableton")), R, C),
    (11, "Root with valid attributes and no child element", ["002"], gz(doc(child=False)), R, C),
    (12, "MajorVersion absent", ["003"], gz(doc(drop("MajorVersion"))), R, C),
    (13, 'MajorVersion "0"', ["003"], gz(doc(put("MajorVersion", "0"))), R, C),
    (14, 'MajorVersion "five"', ["003"], gz(doc(put("MajorVersion", "five"))), R, C),
    (15, 'MajorVersion "3"', ["003"], gz(doc(put("MajorVersion", "3"))), R, C),
    (16, 'MajorVersion "4"', ["003"], gz(doc(put("MajorVersion", "4"))), A, None),
    (17, 'MajorVersion "+5"', ["003"], gz(doc(put("MajorVersion", "+5"))), A, None),
    (18, 'MajorVersion " 5" (leading space)', ["003"], gz(doc(put("MajorVersion", " 5"))), A, None),
    (19, 'MajorVersion "5 " (trailing space)', ["003"], gz(doc(put("MajorVersion", "5 "))), A, None),
    (20, "Attribute spelled majorversion instead of MajorVersion", ["003"],
     gz(doc([("majorversion" if k == "MajorVersion" else k, v) for k, v in BASE])), R, C),
    (21, "Root attributes in reverse order", ["003"], gz(doc(BASE[::-1])), A, None),
    (22, "MinorVersion absent", ["003"], gz(doc(drop("MinorVersion"))), R, C),
    (23, 'MinorVersion ""', ["003"], gz(doc(put("MinorVersion", ""))), R, C),
    (24, 'MajorVersion "6"', ["003", "004"], gz(doc(put("MajorVersion", "6"))), R, N),
    (25, 'MinorVersion "12.0_12403", above the largest family 12.0 translator number in S', ["004", "005"],
     gz(doc(put("MinorVersion", "12.0_12403"))), R, N),
    (26, 'MinorVersion "garbage"', ["005"], gz(doc(put("MinorVersion", "garbage"))), R, C),
    (27, 'MinorVersion "12.0_12117", an older name in S', ["005"], gz(doc(put("MinorVersion", "12.0_12117"))), A, None),
    (28, "Creator and Revision absent", ["006"], gz(doc(drop("Creator", "Revision"))), A, None),
    (29, 'Creator "Somebody Else 1.0" and Revision "not-hex"', ["006"],
     gz(doc([(k, {"Creator": "Somebody Else 1.0", "Revision": "not-hex"}.get(k, v)) for k, v in BASE])), A, None),
    (30, 'SchemaChangeCount absent and an extra attribute Extra="1"', ["006"],
     gz(doc(drop("SchemaChangeCount") + [("Extra", "1")])), A, None),
    (31, 'SchemaChangeCount "x"', ["003", "006"], gz(doc(put("SchemaChangeCount", "x"))), R, C),
    (32, 'SchemaChangeCount "" (present and empty)', ["003", "006"], gz(doc(put("SchemaChangeCount", ""))), R, C),
    (33, 'SchemaChangeCount "+-1"', ["003", "006"], gz(doc(put("SchemaChangeCount", "+-1"))), R, C),
    (34, 'SchemaChangeCount "１" (U+FF11 fullwidth digit one)', ["003", "006"],
     gz(doc(put("SchemaChangeCount", "１"))), R, C),
    (35, "SchemaChangeCount of 64 ASCII digits: 63 zeros then 1", ["003", "006"],
     gz(doc(put("SchemaChangeCount", "0" * 63 + "1"))), R, C),
]

# Analyst-only traceability: release case -> SPEC-ALS-CONTAINER r1 case or clause, evidence, inferred links.
EV = "analysis/ableton-live-12.4.3/r2/n2-container-v1/"
E = {
    "dispatch": EV + "results/n2-0002/functions/0x10148389c.json disassembly 0x1014838cc-0x101483b90; "
                     + EV + "results/n2-0002/functions/0x10146c258.c (other prefix -> null document; <2 bytes -> 0x101488e64); "
                     + EV + "corpus/0x10143354c.c, 0x101433570.c (FE FF / FF FE); image-probe.json 0x10581394d = EF BB BF",
    "gzip": EV + "results/n2-0002/functions/0x10148389c.json 0x1014838e4-0x10148396c (1F 8B -> gzip stream 0x10146208c, recursion); "
                 "r2/s2-static-v1/out/documents.jsonl (25 .als: FLG 0, MTIME 0, XFL 2, OS 19)",
    "xmlerr": EV + "corpus/0x1012475a8.c (isFinal at EOF; error != 35 -> 0x101247828), 0x101247828.c, 0x101247760.c, 0x101529970.c "
                   "(+0x28); results/n2-0003/functions/0x1015289c8.c step 4 -> 0x10148229c; corpus/0x10148229c.c key 0x106f4f708; "
                   "results/n2-0002/functions/0x10148e4cc.c L35 sErrorDocumentCorruptWhileReading",
    "root": EV + "results/n2-0002/functions/0x1015299e0.json 0x101529c5c-0x101529c8c (len 7, 'Able'/'eton'); 0x1015299e0.c throw",
    "nodoc": EV + "results/n2-0003/functions/0x1015289c8.c (+0xa0 null -> 0x101488e64 'No document found'); corpus/0x101488e64.c -> 0x10148229c",
    "attrs": EV + "results/n2-0003/functions/0x10152a900.c and 0x10152ab04.c (strlen+memcmp exact name; first match; absent int -> 0)",
    "int": EV + "results/n2-0005/functions/0x1002fd908.json full disassembly (empty/all-space, 0x20-only trim, '+', '+-', >0x3f, >=0x80, "
                "converter 0x1002fda78 must consume to end with ec 0); 0x10152a900.c (fail -> 'Illegal value for int attribute')",
    "vcheck": EV + "results/n2-0002/functions/0x101529024.json 0x101529038-0x101529078, 0x101529120-0x101529130 (signed >= 6 sets +0x29)",
    "versioned": EV + "results/n2-0002/functions/0x1015299e0.c (first child: 0x10147fcc0, 0x10147fdbc class+0xbe gates 0x101529024); "
                      + EV + "results/n2-0003/functions/0x10147fdbc.c; results/n2-0002/functions/0x101485240.c L32/L101 (writer emits versions only when class+0xbe)",
    "post": EV + "results/n2-0003/functions/0x1015289c8.c (newer flag first; +0x38 parse via 0x101514e30; family compare; scan 0x101514f7c; "
                 "+0x60; +0x28; +0xa0); n2-0005 0x101528c84.c; corpus/0x101488ec0.c key 0x106f4f720; n2-0002 0x101535400.c specific key",
    "lookup": EV + "results/n2-0003/functions/0x101514c6c.c; results/n2-0005/functions/0x101514954.c ('<MinorVersion>.txt' exists check)",
    "scan": EV + "corpus/0x101514f7c.c (stem a.b_c, same family, keep max c); r2/s2-static-v1/out/schemas.json suffix_ranges 12.0 max 12402",
    "form": EV + "results/n2-0005/functions/0x101514e30.c (digits '.' digits '_' digits end)",
    "S": "r2/s2-static-v1/out/schemas.json schemas['12.0_12117'], schemas['12.0_12402'], suffix_ranges['12.0'].max = 12402",
    "revision": EV + "results/n2-0001/refs/0x105b91713.json (only the writer 0x101485240); index-lookups.jsonl strings row",
    "creator": EV + "results/n2-0002/functions/0x101528e2c.c (newer paths only); corpus/0x101573d24.c (non-refusing event)",
}
I = {
    "I1": "Exception thrown by the start-element handler is caught at the callback boundary, the parse aborted with the stored "
          "message and the post-parse decision runs (catch site not in kept evidence; supported by 0x1012475a8 abort handling "
          "and the flags set before each throw). Governs the refusal class, not the refusal.",
    "I2": "LiveSet's class carries the versioned flag (writer emits versions only for flagged classes; every shipped set has them).",
    "I3": "Converter 0x1002fda78 is a base-10 whole-string integer conversion (from_chars-like signature; untraced).",
    "I4": "Absent MinorVersion: shared empty string 0x106e0ca98 may be null; lookup assumed null-safe (string helpers null-check).",
    "I5": "Lookup base and scan base are both the shipped Contents/App-Resources/Schema directory (base global untraced).",
    "I6": "Gzip stream object 0x10146208c inflates a standard single-member gzip with the shipped header form (untraced).",
}
TRACE = {
    1: ("N2-001 (narrowed: minimal body; 'opens' -> envelope-accepted)", ["gzip", "dispatch", "vcheck", "lookup", "S"], ["I6"]),
    2: ("N2-002 (reader-level; command-level acceptance excluded, PRB-N2-02)", ["dispatch", "vcheck", "lookup", "S"], []),
    3: ("N2-003 (class dropped: reading-path dependent, PRB-N2-05)", ["dispatch"], []),
    4: ("N2-004 (class dropped)", ["dispatch"], []),
    5: ("N2-005 (class dropped)", ["dispatch"], []),
    6: ("clause REQ-001 'decompressed content recognized by the same rule' (new case)", ["gzip", "dispatch"], ["I6"]),
    7: ("clause REQ-001 'content shorter than two bytes' (new case)", ["dispatch"], []),
    8: ("N2-026 (gzip and minimal; truncated before </Ableton>)", ["gzip", "xmlerr"], ["I6"]),
    9: ("N2-006", ["root"], ["I1", "I6"]),
    10: ("N2-007", ["root"], ["I1", "I6"]),
    11: ("clause REQ-002 'root with no child element' (new case)", ["nodoc", "attrs"], ["I6"]),
    12: ("N2-008", ["attrs", "vcheck", "versioned"], ["I1", "I2", "I6"]),
    13: ("N2-009", ["int", "vcheck", "versioned"], ["I1", "I2", "I3", "I6"]),
    14: ("N2-010", ["int"], ["I1", "I3", "I6"]),
    15: ("N2-011", ["int", "vcheck", "versioned"], ["I1", "I2", "I3", "I6"]),
    16: ("N2-012 (narrowed: envelope-accepted only)", ["int", "vcheck", "lookup", "S"], ["I3", "I6"]),
    17: ("clause REQ-003 accepted spelling '+5' (new case)", ["int", "vcheck"], ["I3", "I6"]),
    18: ("clause REQ-003 accepted spelling ' 5' (new case)", ["int", "vcheck"], ["I3", "I6"]),
    19: ("clause REQ-003 accepted spelling '5 ' (new case)", ["int", "vcheck"], ["I3", "I6"]),
    20: ("clause REQ-003 'exact, case-sensitive name' (new case)", ["attrs", "vcheck", "versioned"], ["I1", "I2", "I6"]),
    21: ("clause REQ-003 'order does not matter' (new case)", ["attrs"], ["I6"]),
    22: ("N2-015 (class only)", ["attrs", "vcheck", "lookup", "post", "versioned"], ["I1", "I2", "I4", "I6"]),
    23: ("N2-016 (class only)", ["attrs", "vcheck", "lookup", "post", "versioned"], ["I1", "I2", "I6"]),
    24: ("N2-013", ["vcheck", "post", "versioned"], ["I1", "I2", "I3", "I6"]),
    25: ("N2-019", ["vcheck", "lookup", "post", "scan", "form", "S", "versioned"], ["I1", "I2", "I5", "I6"]),
    26: ("N2-017", ["vcheck", "lookup", "post", "form", "versioned"], ["I1", "I2", "I5", "I6"]),
    27: ("N2-021 (narrowed: FLG 0 header and minimal body; FNAME aspect excluded, PRB-N2-07)", ["lookup", "S"], ["I5", "I6"]),
    28: ("N2-022 (narrowed: envelope-accepted only)", ["attrs", "revision", "creator"], ["I6"]),
    29: ("N2-023 (narrowed: envelope-accepted only)", ["attrs", "revision", "creator"], ["I6"]),
    30: ("N2-024 (narrowed: envelope-accepted only)", ["attrs"], ["I6"]),
    31: ("N2-025", ["int"], ["I1", "I3", "I6"]),
    32: ("clause REQ-003/006 'empty or only spaces' (new case)", ["int"], ["I1", "I6"]),
    33: ("clause REQ-003/006 '+ followed by -' (new case)", ["int"], ["I1", "I6"]),
    34: ("clause REQ-003/006 'byte outside ASCII' (new case)", ["int"], ["I1", "I6"]),
    35: ("clause REQ-003/006 'longer than 63 characters' (new case)", ["int"], ["I1", "I6"]),
}
DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{5,}", r"FUN_", r"disassembl", r"decompil", r"pseudocode", r"Ghidra",
        r"[Ee]xpat", r"zlib", r"Python", r"vtable", r"dossier", r"corpus", r"\bN2-", r"PRB-", r"\bQ-0", r"\bI[1-6]\b",
        r"reading path", r"version-aware", r"\bcatch", r"Compound", r"TXml", r"sError", r"Languages", r"\bChangeCount\b",
        r"TranslatorNumber", r"AbletonSchema", r"Illegal value", r"Unsupported (?:Major|Minor)", r"attribute missing",
        r"No document found", r"Expected 'Ableton'", r"derivation", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/",
        r"ev_[0-9a-f]", r"\bL\d{2,}\b", r"from_chars", r"strto", r"\+0x"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cid(n):
    return f"ALS-CONTAINER-{n:03d}"


def manifest_meta():
    return {
        "schema": "handoff-manifest-v1", "release_id": "als-container-v1", "release_status": "candidate-unreviewed",
        "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-ALS-CONTAINER", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {
            "REQ-ALS-CONTAINER-001": "Container from first bytes; gzip content classified again; listed malformed starts refused (class unspecified); not well-formed XML refused as corrupt-document",
            "REQ-ALS-CONTAINER-002": "Root named exactly Ableton; root without child element refused",
            "REQ-ALS-CONTAINER-003": "Exact attribute names in any order; integer rule table; MajorVersion range; MinorVersion absent or empty refused",
            "REQ-ALS-CONTAINER-004": "MajorVersion 6 or more, and a schema name above its family's largest translator number in S, refused as newer-version",
            "REQ-ALS-CONTAINER-005": "MinorVersion in S passes; letters-only value refused as corrupt-document",
            "REQ-ALS-CONTAINER-006": "Creator and Revision free and optional; SchemaChangeCount optional but integer; other attributes ignored",
        },
        "unreleased_requirements": ["REQ-ALS-CONTAINER-007", "REQ-ALS-CONTAINER-008", "REQ-ALS-CONTAINER-009"],
        "compatibility_dimensions": {
            "document-envelope-classification": "static-derived expectations; reference execution not-run",
            "file-format-written": "excluded (REQ-ALS-CONTAINER-007, 008)",
            "ui": "excluded (REQ-ALS-CONTAINER-009)", "behavior-after-acceptance": "excluded",
            "audio": "excluded", "timing": "excluded",
        },
        "exclusions": {
            "inputs_without_expectation": [
                "leading bytes other than those listed in REQ-ALS-CONTAINER-001, including other Live document formats",
                "gzip other than one member with the fixtures' header, a valid trailer and no trailing bytes; damaged or truncated compressed data; header flags and optional fields",
                "plain XML other than the fixtures' form: other declarations or encodings, a processing instruction first, document type declarations, references in root attributes, namespaces, carriage returns",
                "document element other than LiveSet; a second child of the root; content inside LiveSet",
                "integer values marked no expectation, including both leading and trailing decoration, a minus sign not preceded by plus, leading zeros, and ten or more digits within 63 characters",
                "MinorVersion values outside REQ-ALS-CONTAINER-003 to 005, including families absent from S, names below their family's largest translator number but not in S, digit groups of ten or more digits, and non-letter values that are not schema names",
                "documents that break more than one rule",
            ],
            "behavior": [
                "refusal presentation: texts, dialogs, details, named versions, logging, state after refusal (REQ-ALS-CONTAINER-009)",
                "container and envelope written on save (REQ-ALS-CONTAINER-007, 008)",
                "whether a document with an accepted envelope opens; content; conversion of older documents",
                "which user commands read a file and their filtering by name, extension or container, including uncompressed files",
                "non-refusing effects of Creator",
                "comparison of SchemaChangeCount with the named schema; unknown element names",
                "progress, cancellation, timing and undo",
            ],
        },
        "fixture_origin": "independently authored minimal documents from a four-line template; no shipped file content, schema content or program code",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def build():
    (STAGE / "fixtures").mkdir(parents=True, exist_ok=True)
    cases = []
    for n, purpose, reqs, data, outcome, cls in CASES:
        rel = f"fixtures/{cid(n)}.als"
        (STAGE / rel).write_bytes(data)
        expected = {"outcome": outcome} if cls is None else {"outcome": outcome, "refusal_class": cls}
        comparator = ("outcome exact" if cls is None else
                      "outcome exact; refusal_class not compared" if cls == U else "outcome exact; refusal_class exact")
        cases.append({"id": cid(n), "purpose": purpose, "requirements": [f"REQ-ALS-CONTAINER-{r}" for r in reqs],
                      "input": rel, "container": "gzip" if data[:2] == b"\x1f\x8b" else "uncompressed",
                      "expected": expected, "expectation_provenance": PROV,
                      "reference_execution": "not-run", "candidate_execution": "not-run", "comparator": comparator})
    doc_ = {"schema": "als-container-cases-v1", "target": TARGET,
            "scope": "als-container-v1 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
            "fixture_origin": "Independently authored minimal documents; no shipped file copied",
            "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
            "representation": {
                "outcome": "envelope-accepted or refused",
                "refusal_class": "refused only: corrupt-document, newer-version, or unspecified (not compared)",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1, ensure_ascii=False) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- cross-check model: the released rules restated over the real shipped schema-name list ----
class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


D = r"(?:0|[1-9][0-9]{0,8})"


def int_attr(attrs, name):
    if name not in attrs:
        return 0
    v = attrs[name]
    if v.strip(" ") == "" or not v.isascii() or v.lstrip(" ").startswith("+-") \
            or (len(v) > 63 and re.fullmatch(r"[0-9]+", v)) or re.search(r"[A-Za-z]", v):
        raise Refused(C)
    m = re.fullmatch(rf"\+({D})| +({D})|({D}) +|({D})", v)
    if not m:
        raise NoExpectation(f"integer form {v!r}")
    return int(next(g for g in m.groups() if g is not None))


def version_rules(major, minor, names):
    if major == 0 or minor == "":
        raise Refused(C)
    if major not in (4, 5):
        raise Refused(N if major >= 6 else C)
    if minor in names:
        return
    m = re.fullmatch(r"([0-9]{1,9})\.([0-9]{1,9})_([0-9]{1,9})", minor)
    if m:
        fam = [int(x.split("_")[1]) for x in names if x.split("_")[0] == f"{m[1]}.{m[2]}"]
        if fam and int(m[3]) > max(fam):
            raise Refused(N)
        raise NoExpectation(f"MinorVersion {minor!r}")
    if re.fullmatch(r"[A-Za-z]+", minor):
        raise Refused(C)
    raise NoExpectation(f"MinorVersion {minor!r}")


def model_xml(data, names):
    st = {"depth": 0, "doc": False}

    def start(name, attrs):
        st["depth"] += 1
        if st["depth"] == 1:
            if name != "Ableton":
                raise Refused(C)
            st["major"] = int_attr(attrs, "MajorVersion")
            st["minor"] = attrs.get("MinorVersion", "")
            int_attr(attrs, "SchemaChangeCount")
        elif st["depth"] == 2:
            if st["doc"] or name != "LiveSet":
                raise NoExpectation("document element")
            st["doc"] = True
            version_rules(st["major"], st["minor"], names)

    def end(name):
        st["depth"] -= 1

    p = pyexpat.ParserCreate()
    p.StartElementHandler, p.EndElementHandler = start, end
    try:
        p.Parse(data, True)
    except pyexpat.ExpatError:
        return (R, C)
    except Refused as e:
        return (R, e.args[0])
    return (A, None) if st["doc"] else (R, C)


def model(data, names):
    if len(data) < 2:
        return (R, U)
    if data[:2] == b"\x1f\x8b":
        if data[:10] != GZ_HEADER:
            raise NoExpectation("gzip header")
        d = zlib.decompressobj(31)
        inner = d.decompress(data) + d.flush()
        if d.unused_data or not d.eof:
            raise NoExpectation("gzip trailer")
        return model(inner, names)
    if data[:2] == b"<?":
        return model_xml(data, names)
    if data[:1] in (b" ", b"\t", b"\n", b"\r") or data[:1] == b"<" or data[:4] == BOM + b"<":
        return (R, U)
    raise NoExpectation("leading bytes")


# ---- checks ----
def payload(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md_path, root):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md_path.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md_path.parent / path).resolve() if path else md_path
        ok = dest.is_file() and root.resolve() in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((target, "ok" if ok else "UNRESOLVED"))
    return out


def verify(d):
    d = Path(d)
    man = json.loads((d / "manifest.json").read_text())
    files = payload(d)
    mismatches = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
                  or sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inventory = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    link_rows = {str(p.relative_to(d)): links(p, d) for p in d.glob("*.md")}
    bad_links = {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    missing_inputs = [c["input"] for c in cases if not (d / c["input"]).is_file()]
    deny = {}
    for p in [*files, d / "manifest.json"]:
        if p.suffix == ".als":
            text = p.read_bytes().decode("latin-1")
            if p.read_bytes()[:2] == b"\x1f\x8b":
                text = zlib.decompress(p.read_bytes(), 31).decode("utf-8", "replace")
        else:
            text = p.read_text()
        hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad_links, "missing_case_inputs": missing_inputs, "deny_list_hits": deny,
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def seal():
    names = set(json.loads(SCHEMAS.read_text())["schemas"])
    assert len(names) == 203
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    problems, fixtures = {}, {}
    for c in cases:
        raw = (STAGE / c["input"]).read_bytes()
        exp = c["expected"]
        try:
            got = model(raw, names)
        except NoExpectation as e:
            got = ("no-expectation", str(e))
        errs = []
        if got != (exp["outcome"], exp.get("refusal_class")):
            errs.append(f"model {got} != expected")
        text = zlib.decompress(raw, 31) if raw[:2] == b"\x1f\x8b" else raw
        if text and (b"\r" in text or not text.endswith(b"\n")):
            errs.append("not LF-terminated")
        if raw[:2] == b"\x1f\x8b" and raw[:10] != GZ_HEADER:
            errs.append("gzip header differs")
        if errs:
            problems[c["id"]] = errs
        lines = text.decode("utf-8").split("\n")
        root_line = (re.search(r"<(?:Ableton|Live|ableton)\b[^>]*>", text.decode("utf-8")) or [""])[0]
        fixtures[c["id"]] = {"bytes": len(raw), "decompressed_bytes": len(text), "first_bytes": text[:6].hex(),
                             "root_start_tag": root_line, "lines": len(lines) - 1}
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "als-container-v1 (staged candidate)",
              "python": sys.version.split()[0], "zlib": zlib.ZLIB_RUNTIME_VERSION, "expat": pyexpat.EXPAT_VERSION,
              "cases": len(cases), "case_problems": problems, "fixtures": fixtures, **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the model restates the "
                        "same static evidence and is not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    trace = {"schema": "als-container-traceability-v1", "spec": "SPEC-ALS-CONTAINER r1", "evidence": E, "inferred_links": I,
             "cases": {cid(n): {"source": src, "evidence": ev, "inferred": inf} for n, (src, ev, inf) in TRACE.items()}}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "payload_files", "hash_or_size_mismatches",
                                             "inventory_differences", "unresolved_links", "missing_case_inputs",
                                             "deny_list_hits", "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
