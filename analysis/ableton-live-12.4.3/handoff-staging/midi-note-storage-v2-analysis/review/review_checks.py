"""Reviewer checks for midi-note-storage-v2 (analyst side; never shipped).

usage: python3 -I -B review_checks.py <package dir> > <out.json>
Supersession and carry against handoff/midi-note-storage-v1, fixture additions, MNS-012, numeric claims
of the contract, package inventory, hashes and links. Written by the reviewer; imports only restate.py
(the reviewer's restatement) for the grid and number-text rules.
"""
import hashlib, json, math, re, struct, sys, zlib
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import restate  # noqa: E402

PKG = Path(sys.argv[1]).resolve()
REPO = Path(__file__).resolve().parents[5]
V1 = REPO / "handoff/midi-note-storage-v1"
sha = lambda b: hashlib.sha256(b).hexdigest()
text = lambda p: zlib.decompress(p.read_bytes(), 31).decode("utf-8")
out = {}

# ---- supersession -------------------------------------------------------------------------------------------
m1 = json.loads((V1 / "manifest.json").read_text())
m2 = json.loads((PKG / "manifest.json").read_text())
catalog = (REPO / "handoff/index.md").read_text()
row = next(l for l in catalog.splitlines() if l.startswith("| [midi-note-storage-v1]"))
out["v1_manifest_sha256"] = sha((V1 / "manifest.json").read_bytes())
out["v1_digest_equals_catalog_and_claim"] = (out["v1_manifest_sha256"] in row
                                             and m2["supersession"]["superseded_manifest_sha256"] == out["v1_manifest_sha256"])
out["v1_files_mismatched"] = [f["path"] for f in m1["files"] if sha((V1 / f["path"]).read_bytes()) != f["sha256"]]
c1 = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
c2 = {c["id"]: c for c in json.loads((PKG / "cases.json").read_text())["cases"]}
out["carried_ids_all_present"] = set(c1) <= set(c2)
out["new_ids"] = sorted(set(c2) - set(c1))
out["carried_records_changed"] = [k for k in c1 if c1[k] != c2[k]]
out["carried_records_serialized_identical"] = all(json.dumps(c1[k], sort_keys=True) == json.dumps(c2[k], sort_keys=True)
                                                  for k in c1)

FREEZE = ("\t\t\t\t\t<FreezeSequencer>\n\t\t\t\t\t\t<ClipSlotList>\n\t\t\t\t\t\t\t<ClipSlot Id=\"0\">\n"
          "\t\t\t\t\t\t\t\t<ClipSlot>\n\t\t\t\t\t\t\t\t\t<Value />\n\t\t\t\t\t\t\t\t</ClipSlot>\n"
          "\t\t\t\t\t\t\t\t<HasStop Value=\"true\" />\n\t\t\t\t\t\t\t</ClipSlot>\n\t\t\t\t\t\t</ClipSlotList>\n"
          "\t\t\t\t\t</FreezeSequencer>\n")
SCENES = ("\t\t<Scenes>\n\t\t\t<Scene Id=\"0\">\n\t\t\t\t<Name Value=\"\" />\n\t\t\t\t<Color Value=\"-1\" />\n"
          "\t\t\t\t<Tempo Value=\"120\" />\n\t\t\t\t<IsTempoEnabled Value=\"false\" />\n"
          "\t\t\t\t<TimeSignatureId Value=\"201\" />\n\t\t\t\t<IsTimeSignatureEnabled Value=\"false\" />\n"
          "\t\t\t</Scene>\n\t\t</Scenes>\n")
MS_END = "\t\t\t\t\t</MainSequencer>\n"
TR_END = "\t\t</Tracks>\n"


def v1_form(t2):
    """Remove exactly the two additions at their stated places; None if they are not there exactly once."""
    if t2.count(FREEZE) != 1 or t2.count(SCENES) != 1 or t2.count(MS_END + FREEZE) != 1 or t2.count(TR_END + SCENES) != 1:
        return None
    return t2.replace(MS_END + FREEZE, MS_END).replace(TR_END + SCENES, TR_END)


def notes_xml(t):
    i, j = t.find("\t\t\t\t\t\t\t\t\t\t\t<Notes>"), t.find("\t\t\t\t\t\t\t\t\t\t\t</Notes>")
    return t[i:j]


carry, notes_changed, added_lines = [], [], set()
for k in c1:
    t1, t2 = text(V1 / c1[k]["input"]), text(PKG / c2[k]["input"])
    if v1_form(t2) != t1:
        carry.append(k)
    if notes_xml(t1) != notes_xml(t2) or not notes_xml(t1):
        notes_changed.append(k)
    added_lines.add(len(t2.splitlines()) - len(t1.splitlines()))
out["carried_fixture_not_v1_plus_two_additions"] = carry
out["carried_clip_notes_text_changed"] = notes_changed
out["added_line_counts"] = sorted(added_lines)

# New fixtures: the v2 MNS-001 fixture with only note attribute text changed, as each purpose states.
base = text(PKG / "fixtures/MNS-001.als").splitlines()
new = {}
for k in out["new_ids"]:
    t = text(PKG / c2[k]["input"]).splitlines()
    assert len(t) == len(base)
    new[k] = {"purpose": c2[k]["purpose"], "changed": [(a.strip(), b.strip()) for a, b in zip(base, t) if a != b]}
out["new_fixture_changes"] = new

# MNS-012: the repeated attribute is its only defect.
t12 = text(PKG / "fixtures/MNS-012.als")
dup = [l for l in t12.splitlines() if len(re.findall(r'(\w+)="', l)) != len(set(re.findall(r'(\w+)="', l)))]
fixed = t12
for l in dup:
    names = re.findall(r'(\w+)="[^"]*"', l)
    rep = next(n for n in names if names.count(n) > 1)
    occ = list(re.finditer(rf' {rep}="[^"]*"', l))
    fixed = fixed.replace(l, l[:occ[-1].start()] + l[occ[-1].end():])
out["MNS-012"] = {"repeated_attribute_lines": [l.strip() for l in dup],
                  "without_last_repeat_equals_MNS-001": fixed == text(PKG / "fixtures/MNS-001.als")}

# Counts
cs = list(c2.values())
out["counts"] = {"cases": len(cs), "manifest_case_count": m2["case_count"],
                 "loads": sum(c["expected"]["outcome"] == "loads" for c in cs),
                 "refused": sum(c["expected"]["outcome"] == "refused" for c in cs),
                 "open_save": sum(c["action"] == "open-save" for c in cs),
                 "provenance": {p: sum(c["expectation_provenance"] == p for c in cs)
                                for p in sorted({c["expectation_provenance"] for c in cs})}}

# ---- numeric claims of the contract -------------------------------------------------------------------------
H, N = 1 / 3843840, 3843840
f32 = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]
b64 = lambda x: struct.unpack("<Q", struct.pack("<d", x))[0]
x72 = float("0.00000013007825507825505")
exact = lambda x: (lambda k: k)(math.floor(abs(Fraction(x) * N) + Fraction(1, 2)))
out["numeric"] = {
    "h_repr": repr(H), "h_bits": hex(b64(H)),
    "MNS-072_text_is_one_step_below_h_over_2": x72 == math.nextafter(H / 2, 0),
    "MNS-072_formula_gives_h": restate.grid(x72) == H,
    "MNS-072_exact_half_away_gives_0": exact(x72) == 0,
    "MNS-072_saved_text": restate.text_num(restate.grid(x72), 17),
    "REQ-005_127.00001": format(Fraction(f32(127.00001)), ""), "REQ-005_127.00001_bits": hex(struct.unpack("<I", struct.pack("<f", 127.00001))[0]),
    "REQ-005_0.99999994": str(Fraction(f32(0.99999994))), "REQ-005_0.99999994_bits": hex(struct.unpack("<I", struct.pack("<f", 0.99999994))[0]),
    "REQ-005_127.00001_decimal": f"{f32(127.00001):.20f}", "REQ-005_0.99999994_decimal": f"{f32(0.99999994):.24f}",
    "REQ-006_examples": {t: restate.text_num(restate.grid(float(t)), 17) for t in
                         ("0.123456789", "0.3333333333", "-0.0000002", "0.00000013", "0.000000131",
                          "0.00000013007825507825505", "-0.0000001", "-0")},
    "REQ-006_minus0_sign": math.copysign(1, restate.grid(-0.0)), "REQ-006_minus1e-7_sign": math.copysign(1, restate.grid(-1e-7)),
    "REQ-016_examples": {"33.3": restate.text_num(f32(33.3), 9), "80.578949": restate.text_num(f32(80.578949), 9),
                         "0.2": restate.text_num(0.2, 17), "8191": restate.text_num(8191.0, 9),
                         "-8192": restate.text_num(-8192.0, 9), "-0 float": restate.text_num(f32(-0.0), 9),
                         "-0 double": restate.text_num(-0.0, 17)},
    "new_saved_log10": {"h": math.log10(H), "127": math.log10(127)},
}

# ---- package inventory, hashes, links -------------------------------------------------------------------------
files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
listed = {f["path"]: f for f in m2["files"]}
out["package"] = {
    "payload_files": len(files),
    "inventory_differences": sorted({str(p.relative_to(PKG)) for p in files} ^ set(listed)),
    "hash_or_size_mismatches": [k for k, f in listed.items() if not (PKG / k).is_file()
                                or sha((PKG / k).read_bytes()) != f["sha256"] or (PKG / k).stat().st_size != f["bytes"]],
    "symlinks": [str(p) for p in PKG.rglob("*") if p.is_symlink()],
    "missing_case_inputs": [c["input"] for c in cs if not (PKG / c["input"]).is_file()],
    "distinct_fixtures": len({(PKG / c["input"]).read_bytes() for c in cs}),
    "manifest_sha256": sha((PKG / "manifest.json").read_bytes()),
}


def slug(h):
    return re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")


links = {}
for md in sorted(PKG.glob("*.md")):
    res = []
    for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        path, _, frag = target.partition("#")
        dest = (md.parent / path) if path else md
        ok = dest.resolve().is_file() and str(dest.resolve()).startswith(str(PKG))
        if ok and frag:
            ok = frag in {slug(h) for h in re.findall(r"^#+ (.*)$", dest.read_text(), re.M)}
        res.append((target, ok))
    links[md.name] = {"links": len(res), "unresolved": [t for t, ok in res if not ok]}
out["links"] = links
print(json.dumps(out, indent=1, ensure_ascii=False))
