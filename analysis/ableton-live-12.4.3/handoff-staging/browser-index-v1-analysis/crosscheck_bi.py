"""Analyst cross-check for browser-index-v1 (never shipped; not an oracle).

Independent restatements of the released rules over the same static evidence: the extension table
recomputed by compiling the retained kind-map pseudocode with gcc and joining it with the H2 registry
table; a reader and a writer model for user-folder sidecars in the release's fixture form; sidecar names
recomputed with uuid.uuid5; evidence identity re-hashed against the H2 and D2 manifests. Imported by
build_bi.py (seal); has no command line of its own.
"""
import hashlib, json, re, struct, subprocess, tempfile, uuid
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
R2 = ROOT / "analysis/ableton-live-12.4.3/r2"
REG = R2 / "h2-index-v1/out/file-type-registry.tsv"
D2 = R2 / "d2-browser-index-v1/cited-functions.jsonl"
ADDENDUM = HERE / "kept/corpus-addendum.jsonl"
APP = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources")  # optional legacy-name check
HELPER = Path("/var/tmp/sound-analysis/helpers/Ableton_Index/Ableton_Index.arm64")
AFI = "Ableton Folder Info"
SIDE = "dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp"
CORE_NS = uuid.UUID("c55d131f-2661-5add-aece-29afb7099dfa")
CORE_ID = "www.ableton.com/0"
CORE_NAME = "b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp"
BUILTIN_NAME = "b769aafb-73f9-57e9-8dba-740d64be2541.xmp"
NS = {"x": "adobe:ns:meta/", "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "dc": "http://purl.org/dc/elements/1.1/", "ablFR": "https://ns.ableton.com/xmp/fs-resources/1.0/",
      "xmp": "http://ns.adobe.com/xap/1.0/"}
FOLDER_DOC = {"dc:format": "application/vnd.ableton.folder", "ablFR:resource": "folder", "ablFR:platform": "mac"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---- cross-check models ----
class NoExpectation(Exception):
    pass


def q(tag):
    p, local = tag.split(":")
    return f"{{{NS[p]}}}{local}"


def bag_values(el, tag):
    prop = el.find(q(tag))
    if prop is None:
        return []
    b = prop.find(q("rdf:Bag"))
    if b is None or len(prop) != 1:
        raise NoExpectation(f"{tag} not a single rdf:Bag")
    return [(li.text or "") for li in b.findall(q("rdf:li"))]


def parse_sidecar(data):
    """Data model of a sidecar in the release's fixture form; ET.ParseError when not well-formed."""
    if b"<?xpacket" in data or data.startswith(b"<?xml") or b"\r" in data:
        raise NoExpectation("wrapper, declaration or CR")
    root = ET.fromstring(data)
    descs = root.findall(f"{q('rdf:RDF')}/{q('rdf:Description')}")
    if root.tag != q("x:xmpmeta") or len(descs) != 1:
        raise NoExpectation("not a single rdf:Description in x:xmpmeta")
    d = descs[0]
    doc, items = {}, []
    for ch in d:
        ns, local = ch.tag[1:].split("}")
        if ns == NS["xmp"]:
            continue  # informational
        key = {NS["dc"]: "dc:", NS["ablFR"]: "ablFR:"}.get(ns)
        if key is None:
            raise NoExpectation(f"property in namespace {ns}")
        if ch.tag == q("ablFR:items"):
            for li in ch.find(q("rdf:Bag")).findall(q("rdf:li")):
                if li.get(q("rdf:parseType")) != "Resource":
                    raise NoExpectation("item not parseType Resource")
                fields = {c.tag for c in li}
                if fields - {q("ablFR:filePath"), q("ablFR:keywords"), q("ablFR:colors")}:
                    raise NoExpectation("item field outside the release")
                items.append({"filePath": li.find(q("ablFR:filePath")).text, "keywords": bag_values(li, "ablFR:keywords"),
                              "colors": bag_values(li, "ablFR:colors"), "hideKeywords": []})
        elif ch.tag in (q("dc:format"), q("ablFR:resource"), q("ablFR:platform")):
            doc[key + local] = ch.text
        else:
            raise NoExpectation(f"document property {local}")
    if doc != FOLDER_DOC:
        raise NoExpectation(f"document properties {doc}")
    return {"document": doc, "items": items}


def label_of(text):
    if text == "" or text in ("0", "8"):
        return None
    if text in {str(i) for i in range(1, 8)}:
        return int(text)
    raise NoExpectation(f"color entry {text!r}")


def model_read(folder, items):
    """Tags and labels of the listed items after F is indexed, under the released read rules."""
    tags, labels = {i: set() for i in items}, {i: set() for i in items}
    for side in sorted(folder.rglob("*.xmp")):
        if side.parent.name != AFI:
            continue  # parent-name test fails: not a sidecar
        if side.parent.parent != folder or side.name != SIDE:
            raise NoExpectation(f"sidecar {side.relative_to(folder)}")
        try:
            doc = parse_sidecar(side.read_bytes())
        except ET.ParseError:
            continue  # not well-formed: contributes nothing
        for e in doc["items"]:
            p = e["filePath"]
            if p.startswith("/") or "\\" in p or any(s in (".", "..", "") for s in p.split("/")):
                raise NoExpectation(f"filePath {p!r}")
            if "/" in p or (folder / p).is_dir():
                raise NoExpectation(f"filePath {p!r} is not the name of a file directly in F")  # review RVB-01
            if not (folder / p).exists():
                continue  # names nothing: skipped
            if p not in items:
                continue
            for k in e["keywords"]:
                if k == "" or k.count("|") not in (1, 2) or k != k.strip(" "):
                    raise NoExpectation(f"keyword {k!r}")
            if len(set(e["keywords"])) != len(e["keywords"]):
                raise NoExpectation("repeated keyword")
            tags[p] |= set(e["keywords"])
            labels[p] |= {lab for lab in map(label_of, e["colors"]) if lab is not None}
    return {i: sorted(v) for i, v in tags.items()}, {i: sorted(v) for i, v in labels.items()}


def model_write(folder, edit):
    """Data model of the new user-folder sidecar written for an edit of an item directly in F."""
    if "/" in edit["item"] or (folder / AFI).exists():
        raise NoExpectation("nested item or existing sidecar")
    if not edit["tags"] and not edit["labels"]:
        raise NoExpectation("edit leaves no tags and no labels")
    entry = {"filePath": Path(edit["item"]).name, "keywords": sorted(set(edit["tags"])),
             "colors": [str(i) for i in range(1, 8) if i in edit["labels"]], "hideKeywords": []}
    return {"document": dict(FOLDER_DOC), "items": [entry]}


def norm(doc):
    return {"document": doc["document"],
            "items": sorted(({"filePath": e["filePath"], "keywords": sorted(e["keywords"]), "colors": sorted(e["colors"]),
                              "hideKeywords": sorted(e["hideKeywords"])} for e in doc["items"]),
                            key=lambda e: json.dumps(e, sort_keys=True))}


def kindmap_eval():
    """Compile the retained kind-map pseudocode and evaluate it for every registry code."""
    code = next(json.loads(l)["code"] for l in D2.open() if json.loads(l)["entry"] == "0x10016b758")
    body = code[code.index("{"):]
    body = re.sub(r"LAB_10016bf88:\n.*?return 0;\n\}", "LAB_10016bf88:\n  return -1;\n}", body, flags=re.S)
    for decl in ("undefined8 uVar3;", "undefined1 auStack_28 [8];", "int iVar2;"):
        body = body.replace(decl, "")
    src = ("#include <stdio.h>\n#include <stdlib.h>\ntypedef unsigned int uint;\nlong km(unsigned long param_1)\n" + body +
           '\nint main(int c,char**v){for(int i=1;i<c;i++)printf("%ld\\n",km(strtoul(v[i],0,16)));return 0;}\n')
    rows = [l.rstrip("\n").split("\t") for l in REG.open()][1:]
    with tempfile.TemporaryDirectory() as d:
        Path(d, "k.c").write_text(src)
        subprocess.run(["gcc", "-w", "-O0", "-o", f"{d}/k", f"{d}/k.c"], check=True)
        out = subprocess.run([f"{d}/k"] + [r[1].encode("latin-1").hex() for r in rows], capture_output=True, text=True,
                             check=True).stdout.split()
    ext_bits = {}
    for r, bits in zip(rows, out):
        for e in r[3].split():
            assert e.startswith(".") and e[1:] not in ext_bits
            ext_bits[e[1:]] = int(bits)
    return ext_bits, subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.split("\n")[0]


def check_kinds(EXT_KIND, LABEL_BITS, CASES):
    ext_bits, gcc = kindmap_eval()
    bits_label = {v: k for k, v in LABEL_BITS.items()}
    problems = []
    for e, bits in sorted(ext_bits.items()):
        if bits == -1:  # unknown to the kind map: excluded from the release
            if e in EXT_KIND:
                problems.append(f".{e} unknown to the kind map but in the release table")
            continue
        if EXT_KIND.get(e) != bits_label.get(bits):
            problems.append(f".{e}: kind map {bits:#x} vs release {EXT_KIND.get(e)}")
    if set(EXT_KIND) - set(ext_bits):
        problems.append(f"release extensions not registered: {sorted(set(EXT_KIND) - set(ext_bits))}")
    covered = [n.rsplit(".", 1)[1] for c in CASES if "names" in c for n in c["names"]]
    if sorted(covered) != sorted(EXT_KIND):
        problems.append("cases 1-11 do not cover every release extension exactly once")
    excluded = sorted(e for e, b in ext_bits.items() if b == -1)
    return {"gcc": gcc, "registered_extensions": len(ext_bits), "release_extensions": len(EXT_KIND),
            "unknown_to_kind_map": excluded, "problems": problems}


def check_names():
    nil = uuid.UUID(int=0)
    out = {
        "user_folder": str(uuid.uuid5(uuid.uuid5(nil, "folder"), ".")) + ".xmp" == SIDE,
        "factory_namespace": uuid.uuid5(nil, "factory-pack") == CORE_NS,
        "core_library": str(uuid.uuid5(CORE_NS, CORE_ID)) + ".xmp" == CORE_NAME,
        "builtin": str(uuid.uuid5(uuid.uuid5(nil, "app-resource"), "builtin")) + ".xmp" == BUILTIN_NAME,
    }
    lp = APP / "Builtin/Legacy Pack Data" / AFI
    if lp.is_dir():
        files = sorted(p for p in lp.glob("*.xmp") if not p.name.startswith("._"))
        match = 0
        for p in files:
            m = re.search(rb"<ablFR:packUniqueId>([^<]*)</ablFR:packUniqueId>", p.read_bytes())
            match += bool(m) and str(uuid.uuid5(CORE_NS, m.group(1).decode())) + ".xmp" == p.name
        out["legacy_pack_names"] = f"{match} of {len(files)} match uuid5(namespace, packUniqueId)"
        core = APP / "Core Library" / AFI / f"{CORE_NS}.xmp"
        out["core_library_pack_id"] = re.search(rb"<ablFR:packUniqueId>([^<]*)<", core.read_bytes()).group(1).decode()
    else:
        out["legacy_pack_names"] = "application copy not present; not rechecked"
    return out


def check_evidence():
    h2 = json.loads((R2 / "h2-index-v1/manifest.json").read_text())
    d2 = json.loads((R2 / "d2-browser-index-v1/manifest.json").read_text())
    out = {"registry_tsv": sha(REG.read_bytes()) == h2["outputs"]["out/file-type-registry.tsv"]["sha256"],
           "d2_files": all(sha((R2 / "d2-browser-index-v1" / f).read_bytes()) == h for f, h in d2["files"].items()),
           "addendum_sha256": sha(ADDENDUM.read_bytes())}
    if HELPER.is_file():
        out["helper_slice"] = sha(HELPER.read_bytes()) == h2["inputs"]["helper_slice"]["slice_sha256"]
    return out


def inspect_fixture(p):
    b = p.read_bytes()
    if p.suffix == ".wav":
        ok = (b[:4] == b"RIFF" and b[8:16] == b"WAVEfmt " and struct.unpack_from("<I", b, 4)[0] == len(b) - 8
              and struct.unpack_from("<HH", b, 20) == (1, 1) and b[36:40] == b"data")
        return {"bytes": len(b), "valid_pcm_wav": ok}
    text = b.decode("utf-8")
    try:
        ET.fromstring(b)
        wf = True
    except ET.ParseError:
        wf = False
    return {"bytes": len(b), "well_formed": wf, "lf_only": "\r" not in text, "ends_with_lf": text.endswith("\n"),
            "ascii": b.isascii()}


def mutation_probe(stage, cases, ext_kind, label_bits, cid):
    """Alter one expectation at a time; each alteration must be rejected by the models above."""
    import copy
    by = {c["n"]: c for c in cases}

    def read_ok(c):
        got = model_read(stage / f"fixtures/{cid(c['n'])}/F", list(c["tags"]))
        return got == ({k: sorted(v) for k, v in c["tags"].items()}, {k: sorted(v) for k, v in c["labels"].items()})

    def write_ok(c):
        return norm(model_write(stage / f"fixtures/{cid(c['n'])}/F", c["edit"])) == norm(c["doc"])

    out = {}
    for name, n, field, value, ok in [
        ("labels gain 0", 20, "labels", {"a.wav": [0, 3]}, read_ok),
        ("sidecar outside the sidecar folder read", 13, "tags", {"a.wav": ["Character|Bright"]}, read_ok),
        ("truncated sidecar gives its tag", 15, "tags", {"a.wav": ["Character|Bright"]}, read_ok),
        ("unresolved entry blocks the other", 18, "tags", {"a.wav": []}, read_ok),
        ("informational properties drop the tag", 14, "tags", {"a.wav": []}, read_ok)]:  # review: case 16 removed
        m = copy.deepcopy(by[n]); m[field] = value
        out[name] = ok(m)
    m = copy.deepcopy(by[23]); m["doc"]["document"]["ablFR:platform"] = "win"; out["written platform win"] = write_ok(m)
    m = copy.deepcopy(by[25]); m["doc"]["items"][0]["colors"] = ["1"]; out["written label 7 dropped"] = write_ok(m)
    for ext, label in (("amp", "REX files"), ("fxp", "plug-in presets")):
        out[f".{ext} as {label}"] = not check_kinds({**ext_kind, ext: label}, label_bits, cases)["problems"]
    try:
        label_of("03")
        out["color text 03 graded"] = True
    except NoExpectation:
        out["color text 03 graded"] = False
    return {"mutations": len(out), "accepted": sorted(k for k, v in out.items() if v)}
