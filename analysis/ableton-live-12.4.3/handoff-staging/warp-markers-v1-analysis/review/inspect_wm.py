"""Reviewer check of an exported warp-markers-v1 copy (analyst side; not payload).
Usage: python3 -I inspect_wm.py <package dir>
Checks: inventory and every hash and size; Markdown links resolve inside the package; each case input and
sample exists; inputs distinct; each XML fixture is well formed, ASCII, LF only, final newline, no tabs, has the
stated envelope and exactly one holder, and differs from its template by the stated change only; the WAV
header, chunk layout and data; a sanitization scan wider than the author's deny list."""
import hashlib, json, re, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

d = Path(sys.argv[1]).resolve()
man = json.loads((d / "manifest.json").read_text())
listed = {f["path"]: f for f in man["files"]}
actual = sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")
print("inventory equal:", sorted(listed) == actual, len(actual), "files + manifest")
print("hash/size mismatches:", [p for p, f in listed.items()
      if hashlib.sha256((d / p).read_bytes()).hexdigest() != f["sha256"] or (d / p).stat().st_size != f["bytes"]])
for md in sorted(d.glob("*.md")):
    for t in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        path = t.split("#")[0]
        dest = (md.parent / path).resolve() if path else md
        print("link", md.name, "->", t, "ok" if dest.is_file() and d in dest.parents else "UNRESOLVED")
cases = json.loads((d / "cases.json").read_text())["cases"]
print("case inputs missing:", sorted({x for c in cases for x in (c["input"], c["sample"]) if not (d / x).is_file()}))
print("distinct XML inputs:", len({(d / c["input"]).read_bytes() for c in cases}), "of", len({c["input"] for c in cases}),
      "fixture names used")

CLIPP = "LiveSet/Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip"
SWPP = ("LiveSet/Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/"
        "SampleParts/MultiSamplePart/SampleWarpProperties")


def holder(raw):
    r = ET.fromstring(raw)
    assert r.tag == "Ableton" and r.attrib == {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                               "SchemaChangeCount": "1"} and r[0].tag == "LiveSet", "envelope"
    hs = [e for e in r.iter() if e.tag in ("AudioClip", "SampleWarpProperties")]
    assert len(hs) == 1, "one holder"
    h = r.find(CLIPP) if r.find(CLIPP) is not None else r.find(SWPP)
    assert h is hs[0], "holder path"
    rows = []
    for el in h:
        if el.tag == "WarpMarkers":
            rows += [("WarpMarker", tuple(sorted(m.attrib.items())), len(list(m))) for m in el] or [("WarpMarkers", "empty")]
        else:
            rows.append((el.tag, tuple(sorted(el.attrib.items())), len(list(el))))
    return h.tag, rows


base_tag, base = holder((d / "fixtures/base.xml").read_bytes())
for f in sorted((d / "fixtures").glob("*.xml")):
    raw = f.read_bytes()
    form = (raw.isascii(), b"\r" not in raw, raw.endswith(b"\n"), b"\t" not in raw, raw.startswith(
        b'<?xml version="1.0" encoding="UTF-8"?>\n'))
    tag, rows = holder(raw)
    if tag == base_tag:
        diff = [("-",) + r for r in base if r not in rows] + [("+",) + r for r in rows if r not in base]
    else:
        diff = rows
    print(f.name, len(raw), "form ok" if all(form) else f"FORM {form}", tag, diff if f.name != "base.xml" else "(template)")

wav = (d / "fixtures/sample.wav").read_bytes()
riff, size, wave_ = struct.unpack_from("<4sI4s", wav, 0)
chunks, off = [], 12
while off < len(wav):
    cid, csz = struct.unpack_from("<4sI", wav, off)
    chunks.append((cid, csz, off + 8))
    off += 8 + csz + (csz & 1)
fmt = next(c for c in chunks if c[0] == b"fmt ")
tag, ch, rate, brate, align, bits = struct.unpack_from("<HHIIHH", wav, fmt[2])
data = next(c for c in chunks if c[0] == b"data")
print("wav:", riff, wave_, "riff size ok:", size == len(wav) - 8, "chunks:", [(c[0], c[1]) for c in chunks],
      "end ok:", off == len(wav))
print("wav fmt: PCM" if tag == 1 else f"wav fmt tag {tag}", ch, "ch", rate, "Hz", bits, "bit", "byte rate ok:",
      brate == rate * ch * bits // 8, "align ok:", align == ch * bits // 8, "fmt size", fmt[1])
print("wav frames:", data[1] // align, "seconds:", data[1] / align / rate, "all zero:",
      set(wav[data[2]:data[2] + data[1]]) <= {0}, "other chunks:", [c[0] for c in chunks if c[0] not in (b"fmt ", b"data")])

WIDE = [r"0x[0-9a-fA-F]{4,}", r"\+0x", r"FUN_", r"\bslot\b", r"vtable", r"\bmember", r"[Rr]emoteable", r"getter",
        r"setter", r"constructor", r"\bclass\b", r"callback", r"post-?load", r"post-?read", r"AfterRead",
        r"dossier", r"corpus", r"pseudo", r"disassembl", r"Ghidra", r"\bA[A-Z][a-z]+[A-Z]\w+", r"\b[OFN][A-Z][a-z]+\w*::",
        r"\bm[A-Z][a-z]+[A-Z]", r"\bmp[A-Z]", r"kM(in|ax)", r"Constraints", r"LoopOs|LoopFwd|LoopAlt", r"1 Bar",
        r"\bREX\b", r"Transients\b", r"[Uu]nwarped", r"adjacent", r"Segment length", r"can't|doesn't", r"Empty warp",
        r"only available", r"\bWMK-|\bPRB-|\bQ-0|\bWM-\d|\b[AIF][1-9]\b|\bM[0-2]\b|\b[dsn][1-9]-0|\bS8\b|\bN1\b",
        r"analysis/|raw/|wiki/|\.\./", r"/home/|/var/|/tmp/", r"Live\.arm64", r"Patience|Chuck Sutton|Core Library|Vocal",
        r"DBL_MAX|strto|from_chars", r"Python|Max for Live", r"MarkersGenerated|SamplesToAutoWarp|SampleRef"]
for p in [*sorted(d.glob("*.md")), d / "cases.json", d / "manifest.json", *sorted((d / "fixtures").glob("*.xml"))]:
    text = p.read_text()
    hits = sorted({m.group(0) for pat in WIDE for m in re.finditer(pat, text)})
    if hits:
        print("scan", p.relative_to(d), hits)
