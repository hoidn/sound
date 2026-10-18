"""Build the N2 container acceptance-case documents (analysis-only; nothing is executed).

Usage: python3 -I make_cases.py <App-Resources dir> <out dir>
Writes <out>/cases/<id>.als and <out>/cases.json (id, requirement, kind, bytes, sha256, expected,
provenance). Expectations are hand-authored static derivations or "unknown"; they are not
observations of Live. Base document B is a shipped 12.0_12402 Live Set; N2-021 is the shipped default set (digests checked).
Gzip output uses zlib level 9, wbits 31, so the header OS byte is the build platform's.
"""
import hashlib, json, pathlib, re, sys, zlib

BASE = "Core Library/Lessons/Sets/Recording Audio.als"
BASE_SHA256 = "af57ff8f9eb1c2c51220ef6633a58838532350d53640df5f48dc01659023c043"
DEFAULT_SET = "Builtin/Templates/DefaultLiveSet.als"
DEFAULT_SET_SHA256 = "aeec3f07599da0a61cc86fd9ddeb78a5ce61fe473f676d50c1ae3e281c289a1f"
DECL = b'<?xml version="1.0" encoding="UTF-8"?>\n'
ROOT = re.compile(rb"<Ableton [^>]*>")
GOOD = 'MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1" Creator="Ableton Live 12.4d1" Revision="42bc084cd8152e4fb737ef3fefd04b2bea5320e7"'


def gz(data):
    c = zlib.compressobj(9, zlib.DEFLATED, 31)
    return c.compress(data) + c.flush()


def with_attrs(payload, attrs):
    out, n = ROOT.subn(b"<Ableton " + attrs.encode() + b">", payload, count=1)
    assert n == 1
    return out


def stub(attrs, root="Ableton"):
    return DECL + f'<{root} {attrs}>\n\t<LiveSet />\n</{root}>\n'.encode()


def cases(base_gz, payload, default_set):
    S, U = "static-derived", "unknown"
    corrupt = "not opened; corrupt-document error"
    newer = "not opened; newer-version error"
    return [
        ("N2-001", "001", "positive", base_gz, "opens", S),
        ("N2-002", "001", "positive", payload, "opens (dispatcher accepts plain XML; caller-level checks unknown)", S),
        ("N2-003", "001", "malformed", b"\xef\xbb\xbf" + payload, corrupt + ", detail Unknown Compound Stream Type (general reader entry)", S),
        ("N2-004", "001", "malformed", b"\n" + payload, corrupt + ", detail Unknown Compound Stream Type (general reader entry)", S),
        ("N2-005", "001", "malformed", payload[len(DECL):], corrupt + ", detail Unknown Compound Stream Type (general reader entry)", S),
        ("N2-006", "002", "negative", stub(GOOD, root="Live"), corrupt + ", detail Expected 'Ableton' root node, got 'Live' instead", S),
        ("N2-007", "002", "negative", stub(GOOD, root="ableton"), corrupt + ", detail Expected 'Ableton' root node, got 'ableton' instead", S),
        ("N2-008", "003", "negative", stub(GOOD.replace('MajorVersion="5" ', "")), corrupt + ", detail MajorVersion attribute missing from 'Ableton' root node", S),
        ("N2-009", "003", "boundary", stub(GOOD.replace('MajorVersion="5"', 'MajorVersion="0"')), corrupt + ", detail MajorVersion attribute missing from 'Ableton' root node", S),
        ("N2-010", "003", "malformed", stub(GOOD.replace('MajorVersion="5"', 'MajorVersion="five"')), corrupt + ", detail Illegal value for int attribute: five", S),
        ("N2-011", "003", "boundary", stub(GOOD.replace('MajorVersion="5"', 'MajorVersion="3"')), corrupt + ", detail Unsupported MajorVersion (3)", S),
        ("N2-012", "003", "boundary", with_attrs(payload, GOOD.replace('MajorVersion="5"', 'MajorVersion="4"')), "passes the container check; whole-set load unknown", S),
        ("N2-013", "004", "boundary", stub(GOOD.replace('MajorVersion="5"', 'MajorVersion="6"')), newer + " (generic or naming a version)", S),
        ("N2-014", "003", "boundary", with_attrs(payload, GOOD.replace('MajorVersion="5"', 'MajorVersion=" +5 "')), "opens (spaces and '+' accepted)", S),
        ("N2-015", "003", "negative", stub(GOOD.replace('MinorVersion="12.0_12402" ', "")), corrupt + ", detail MinorVersion attribute missing from 'Ableton' root node", S),
        ("N2-016", "003", "boundary", stub(GOOD.replace('MinorVersion="12.0_12402"', 'MinorVersion=""')), corrupt + "; detail is the missing-MinorVersion text or Unsupported MinorVersion ()", "static-derived class; detail inferred"),
        ("N2-017", "005", "malformed", stub(GOOD.replace("12.0_12402", "garbage")), corrupt + ", detail Unsupported MinorVersion (garbage)", S),
        ("N2-018", "005", "negative", stub(GOOD.replace("12.0_12402", "12.0_12050")), corrupt + " (Unsupported MinorVersion) or newer-version error; depends on reader entry", U),
        ("N2-019", "004", "boundary", stub(GOOD.replace("12.0_12402", "12.0_12403")), newer + " (generic or naming a version)", S),
        ("N2-020", "004", "boundary", stub(GOOD.replace("12.0_12402", "13.0_13000")), newer + " expected; reader-entry dependence unresolved", U),
        ("N2-021", "005", "positive", default_set, "opens (older schema 12.0_12117 exists; gzip FNAME header)", S),
        ("N2-022", "006", "positive", with_attrs(payload, GOOD.replace(' Creator="Ableton Live 12.4d1"', "").replace(' Revision="42bc084cd8152e4fb737ef3fefd04b2bea5320e7"', "")), "opens", S),
        ("N2-023", "006", "positive", with_attrs(payload, GOOD.replace("Ableton Live 12.4d1", "Somebody Else 1.0").replace("42bc084cd8152e4fb737ef3fefd04b2bea5320e7", "not-hex")), "opens", S),
        ("N2-024", "006", "positive", with_attrs(payload, GOOD.replace(' SchemaChangeCount="1"', "") + ' Extra="1"'), "opens", S),
        ("N2-025", "006", "malformed", stub(GOOD.replace('SchemaChangeCount="1"', 'SchemaChangeCount="x"')), corrupt + ", detail Illegal value for int attribute: x", S),
        ("N2-026", "001", "malformed", payload[: len(payload) // 2], corrupt + " (XML not well-formed)", S),
        ("N2-027", "001", "malformed", base_gz[: len(base_gz) // 2], "not opened; error class unknown (truncated gzip)", U),
    ]


def main():
    res, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    base_gz = (res / BASE).read_bytes()
    assert hashlib.sha256(base_gz).hexdigest() == BASE_SHA256
    payload = zlib.decompress(base_gz, 31)
    (out / "cases").mkdir(parents=True, exist_ok=True)
    rows = []
    default_set = (res / DEFAULT_SET).read_bytes()
    assert hashlib.sha256(default_set).hexdigest() == DEFAULT_SET_SHA256
    for cid, req, kind, data, expected, prov in cases(base_gz, payload, default_set):
        (out / "cases" / f"{cid}.als").write_bytes(data)
        rows.append({"id": cid, "requirement": f"REQ-ALS-CONTAINER-{req}", "kind": kind, "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest(), "expected": expected, "provenance": prov})
    (out / "cases.json").write_text(json.dumps({"base": BASE, "base_sha256": BASE_SHA256, "cases": rows}, indent=1) + "\n")


if __name__ == "__main__":
    main()
