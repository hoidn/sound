"""Stage the browser-index-v1 release candidate (analyst side; not reviewed, not released).

Run from any directory with CPython 3.11+ and -I:
  python3 -I build_bi.py build          # fixtures/ + cases.json + manifest.json (files[] empty)
  python3 -I build_bi.py seal           # manifest files[], author-validation.json, traceability.json
  python3 -I build_bi.py verify <dir>   # hashes, inventory, links, inputs, deny-list of an exported copy

Fixtures are authored here: minimal PCM WAV files and sidecar texts from one template written for
this release. No shipped file is copied. Expected results are the hand-authored static derivations in
CASES. seal cross-checks them with crosscheck_bi.py (independent restatements over the same static
evidence, not an oracle), runs its mutation probe, and writes the analyst-only traceability held in
trace_bi.py. README.md, AGENTS.md and spec.md in the stage directory are hand-written.
"""
import json, re, struct, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # keep the analysis directory free of caches
sys.path.insert(0, str(HERE))  # sibling analyst modules; -I leaves the script directory off sys.path
import trace_bi  # noqa: E402
from crosscheck_bi import (AFI, SIDE, FOLDER_DOC, CORE_NAME, BUILTIN_NAME, NoExpectation, sha,  # noqa: E402
                           parse_sidecar, model_read, model_write, norm, check_kinds, check_names, check_evidence,
                           inspect_fixture, mutation_probe)

STAGE = HERE.parent / "browser-index-v1"
PROV = "static-derived; not observed reference output"
TARGET = "Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07) / macOS arm64"

# Release labels (project comparison labels, not names used by the application) -> lowercase extensions.
KINDS = {
    "clips": ["alc"], "live presets": ["adv", "adg"], "grooves": ["agr"], "Max devices": ["amxd", "amp"],
    "REX files": ["rex", "rcy", "rx2"],
    "other audio": ["wav", "aif", "aiff", "ams", "sd2", "mp7", "eflac", "wv", "bwf", "rf64"],
    "encoded audio": ["mp3", "ogg", "flac"], "Windows Media audio": ["wma"], "MPEG-4 audio": ["m4a"],
    "video": ["mov", "avi", "dv", "mp4", "m4v", "wmv", "mpg", "m2v"],
    "images": ["bmp", "pcx", "tif", "tiff", "jpg", "jpeg", "png"], "plug-in presets": ["aupreset", "vstpreset"],
    "other files": ["als", "abl", "ablbundle", "alp", "mid", "midi", "scl", "ascl", "stacks", "appc", "sf", "sf2",
                    "gig", "exs", "nki", "toast", "iso"],
    "none": ["asd", "xmp", "cfg", "txt", "json", "xml", "ini", "zip", "gz", "py", "log", "lng", "ask", "fxp", "fxb",
             "ablpresetbundle", "auz", "idx", "db", "lock", "dmp", "aad", "ard", "band", "exe", "com"],
}
EXT_KIND = {e: k for k, exts in KINDS.items() for e in exts}
# Bit values returned by the kind map for each release label (analyst-side join only; never shipped).
LABEL_BITS = {"none": 0, "other files": 0x1, "clips": 0x2, "other audio": 0x4, "grooves": 0x8, "Max devices": 0x10,
              "live presets": 0x20, "video": 0x40, "REX files": 0x80, "images": 0x400, "encoded audio": 0x800,
              "Windows Media audio": 0x1000, "MPEG-4 audio": 0x2000, "plug-in presets": 0x4000}


# ---- fixture authoring ----
def wav():
    """Minimal valid RIFF/WAVE: PCM, 1 channel, 44,100 Hz, 16 bit, 8 zero samples (60 bytes)."""
    data = b"\0" * 16
    fmt = struct.pack("<HHIIHH", 1, 1, 44100, 88200, 2, 16)
    return (b"RIFF" + struct.pack("<I", 4 + 8 + len(fmt) + 8 + len(data)) + b"WAVE" + b"fmt " +
            struct.pack("<I", len(fmt)) + fmt + b"data" + struct.pack("<I", len(data)) + data)


def bag(tag, values, ind):
    lis = "".join(f"<rdf:li>{v}</rdf:li>" for v in values)
    return f"{ind}<ablFR:{tag}>\n{ind} <rdf:Bag>{lis}</rdf:Bag>\n{ind}</ablFR:{tag}>\n"


def sidecar(items, platform="mac", xmp_props=False):
    """Sidecar text in the release's fixture form. items: [(filePath, keywords, colors or None)]."""
    lis = ""
    for path, kws, colors in items:
        lis += f'     <rdf:li rdf:parseType="Resource">\n      <ablFR:filePath>{path}</ablFR:filePath>\n'
        if kws:
            lis += bag("keywords", kws, "      ")
        if colors is not None:
            lis += bag("colors", colors, "      ")
        lis += "     </rdf:li>\n"
    xmlns_xmp = '\n    xmlns:xmp="http://ns.adobe.com/xap/1.0/"' if xmp_props else ""
    props = ("   <xmp:CreatorTool>Example Tool 1.0</xmp:CreatorTool>\n"
             "   <xmp:CreateDate>2026-01-01T00:00:00Z</xmp:CreateDate>\n"
             "   <xmp:MetadataDate>2026-01-01T00:00:00Z</xmp:MetadataDate>\n") if xmp_props else ""
    text = ('<x:xmpmeta xmlns:x="adobe:ns:meta/">\n'
            ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '  <rdf:Description rdf:about=""\n'
            '    xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
            f'    xmlns:ablFR="https://ns.ableton.com/xmp/fs-resources/1.0/"{xmlns_xmp}>\n'
            f"{props}"
            "   <dc:format>application/vnd.ableton.folder</dc:format>\n"
            "   <ablFR:resource>folder</ablFR:resource>\n"
            f"   <ablFR:platform>{platform}</ablFR:platform>\n"
            "   <ablFR:items>\n    <rdf:Bag>\n" + lis + "    </rdf:Bag>\n   </ablFR:items>\n"
            "  </rdf:Description>\n </rdf:RDF>\n</x:xmpmeta>\n")
    return text.encode("utf-8")


A_ITEM = ("a.wav", ["Character|Bright"], None)  # the item of the release's base sidecar
BASE = sidecar([A_ITEM])
SIDE_REL = f"{AFI}/{SIDE}"

# ---- cases ----
# Each entry: dict with n, purpose, reqs, kind, and one of:
#   names -> {file name: release label}                              (classification)
#   tree -> {relative path: bytes}, tags/labels -> {item: [values]}  (read)
#   tree, edit -> {item, tags, labels}, doc -> expected data model   (write to a user folder)
#   override -> {"content": ..., "name": ...}                        (write for factory or built-in content)


def names(stem_exts, explicit=None):
    pairs = explicit or [(f"item.{e}", e) for e in stem_exts]
    return {n: EXT_KIND[e] for n, e in pairs}


def folder_doc(entries):
    return {"document": dict(FOLDER_DOC),
            "items": [{"filePath": p, "keywords": sorted(k), "colors": [str(c) for c in sorted(c_)],
                       "hideKeywords": []} for p, k, c_ in entries]}


CASES = [
    dict(n=1, purpose="Ten document and audio file names across seven kinds", reqs=["001"], kind="positive",
         names=names(None, [("a.wav", "wav"), ("b.aif", "aif"), ("c.alc", "alc"), ("d.adg", "adg"), ("e.adv", "adv"),
                            ("f.agr", "agr"), ("g.amxd", "amxd"), ("h.rx2", "rx2"), ("i.mid", "mid"), ("j.als", "als")])),
    dict(n=2, purpose="Text, data, analysis, sidecar, configuration and archive files have no kind", reqs=["001"],
         kind="negative", names=names(None, [("k.txt", "txt"), ("l.json", "json"), ("m.asd", "asd"), ("n.xmp", "xmp"),
                                            ("o.cfg", "cfg"), ("p.zip", "zip")])),
    dict(n=3, purpose="Plug-in program and bank files and preset bundles have no kind", reqs=["001"], kind="negative",
         names=names(None, [("q.fxp", "fxp"), ("r.fxb", "fxb"), ("s.ablpresetbundle", "ablpresetbundle")])),
    dict(n=4, purpose="Remaining extensions of the other audio kind", reqs=["001"], kind="positive",
         names=names(["aiff", "ams", "sd2", "mp7", "eflac", "wv", "bwf", "rf64"])),
    dict(n=5, purpose="Compressed audio extensions in three kinds", reqs=["001"], kind="positive",
         names=names(["mp3", "ogg", "flac", "wma", "m4a"])),
    dict(n=6, purpose="Remaining Max device and REX extensions", reqs=["001"], kind="positive",
         names=names(["amp", "rex", "rcy"])),
    dict(n=7, purpose="Video extensions", reqs=["001"], kind="positive",
         names=names(["mov", "avi", "dv", "mp4", "m4v", "wmv", "mpg", "m2v"])),
    dict(n=8, purpose="Image extensions", reqs=["001"], kind="positive",
         names=names(["bmp", "pcx", "tif", "tiff", "jpg", "jpeg", "png"])),
    dict(n=9, purpose="Plug-in preset extensions", reqs=["001"], kind="positive", names=names(["aupreset", "vstpreset"])),
    dict(n=10, purpose="Remaining extensions of the other files kind", reqs=["001"], kind="positive",
         names=names(["abl", "ablbundle", "alp", "midi", "scl", "ascl", "stacks", "appc", "sf", "sf2", "gig", "exs",
                      "nki", "toast", "iso"])),
    dict(n=11, purpose="Remaining extensions without a kind", reqs=["001"], kind="negative",
         names=names(["ini", "gz", "py", "log", "lng", "ask", "auz", "idx", "db", "lock", "dmp", "aad", "ard", "band",
                      "exe", "com", "xml"])),
    dict(n=12, purpose="Base sidecar in F's sidecar folder gives a.wav its tag", reqs=["003", "004", "005", "006"],
         kind="positive", tree={"a.wav": wav(), SIDE_REL: BASE},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": []}),
    dict(n=13, purpose="The same sidecar in a folder not named Ableton Folder Info is not read", reqs=["003"],
         kind="negative", tree={"a.wav": wav(), f"Tags/{SIDE}": BASE}, tags={"a.wav": []}, labels={"a.wav": []}),
    dict(n=14, purpose="Base sidecar with informational xmp creator and date properties", reqs=["004"], kind="positive",
         tree={"a.wav": wav(), SIDE_REL: sidecar([A_ITEM], xmp_props=True)},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": []}),
    dict(n=15, purpose="Sidecar truncated to the first half of the base sidecar's bytes (not well-formed)",
         reqs=["004"], kind="malformed", tree={"a.wav": wav(), SIDE_REL: BASE[:len(BASE) // 2]},
         tags={"a.wav": []}, labels={"a.wav": []}),
    # Cases 16 (entry "sub/b.wav") and 17 (entry naming the folder "kit") removed in review (RVB-01): the reviewer's
    # static check shows a folder sidecar's entries bind only to files directly inside F, by name. IDs are not reused.
    dict(n=18, purpose="An entry naming no file does not affect another entry", reqs=["005"], kind="negative",
         tree={"a.wav": wav(), SIDE_REL: sidecar([A_ITEM, ("gone.wav", ["Type|Loop"], None)])},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": []}),
    dict(n=19, purpose="Color label entries 2 and 5", reqs=["006"], kind="positive",
         tree={"a.wav": wav(), SIDE_REL: sidecar([("a.wav", ["Character|Bright"], ["2", "5"])])},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": [2, 5]}),
    dict(n=20, purpose="Color label entries 0, 8, 3 and an empty entry", reqs=["006"], kind="boundary",
         tree={"a.wav": wav(), SIDE_REL: sidecar([("a.wav", ["Character|Bright"], ["0", "8", "3", ""])])},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": [3]}),
    dict(n=21, purpose="All seven color label entries, 1 to 7", reqs=["006"], kind="boundary",
         tree={"a.wav": wav(), SIDE_REL: sidecar([("a.wav", ["Character|Bright"], [str(i) for i in range(1, 8)])])},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": list(range(1, 8))}),
    dict(n=22, purpose="Three tags on one item", reqs=["006"], kind="positive",
         tree={"a.wav": wav(),
               SIDE_REL: sidecar([("a.wav", ["Character|Bright", "Character|Warm", "Genres|Ambient"], None)])},
         tags={"a.wav": ["Character|Bright", "Character|Warm", "Genres|Ambient"]}, labels={"a.wav": []}),
    dict(n=23, purpose="The user sets the tags of a.wav to Character|Warm in a folder without a sidecar",
         reqs=["004", "007"], kind="positive", tree={"a.wav": wav()},
         edit={"item": "a.wav", "tags": ["Character|Warm"], "labels": []},
         doc=folder_doc([("a.wav", ["Character|Warm"], [])])),
    dict(n=24, purpose="The user gives a.wav color label 3 in a folder without a sidecar", reqs=["006", "007"],
         kind="positive", tree={"a.wav": wav()}, edit={"item": "a.wav", "tags": [], "labels": [3]},
         doc=folder_doc([("a.wav", [], [3])])),
    dict(n=25, purpose="The user sets two tags and color labels 7 and 1 on a.wav in a folder without a sidecar",
         reqs=["006", "007"], kind="positive", tree={"a.wav": wav()},
         edit={"item": "a.wav", "tags": ["Genres|Ambient", "Character|Warm"], "labels": [7, 1]},
         doc=folder_doc([("a.wav", ["Character|Warm", "Genres|Ambient"], [1, 7])])),
    dict(n=26, purpose="The user changes the tags of one item of the installed Core Library", reqs=["007"],
         kind="positive", override={"content": "Core Library", "name": CORE_NAME}),
    dict(n=27, purpose="The user changes the tags of one item of the built-in content", reqs=["007"], kind="positive",
         override={"content": "built-in content", "name": BUILTIN_NAME}),
    dict(n=28, purpose="A copy of the case 12 folder, with its sidecar folder, added on another installation",
         reqs=["008"], kind="positive", tree={"a.wav": wav(), SIDE_REL: BASE},
         tags={"a.wav": ["Character|Bright"]}, labels={"a.wav": []}),
]

DENY = [r"analysis/", r"wiki/", r"\.\./", r"0x[0-9a-fA-F]{4,}", r"FUN_", r"DAT_", r"disassembl", r"decompil",
        r"pseudocode", r"Ghidra", r"[Ee]xpat", r"Python", r"vtable", r"corpus", r"\bBI-\d", r"PRB-", r"\bQ-0",
        r"\bI[1-9]\b", r"\bF[1-9]\b", r"\bD2\b", r"\bH2\b", r"TFile", r"MapFileType", r"typeId", r"file_kind",
        r"fourcc", r"four-character", r"browser-default", r"other-audio", r"live-presets", r"max-patches",
        r"rex-files", r"device-folders", r"other-folders", r"plugin-presets", r"restricted-", r"app-resource",
        r'"builtin"', r"\bbuiltin\b", r"Legacy Pack", r"Write Metadata", r"Remove empty", r"Error reading",
        r"UserLibrary", r"stoul", r"to_string", r"boost", r"SQL", r"[Ss]qlite", r"nanomsg", r"IPC", r"Ableton Index",
        r"helper", r"XMP Core", r"xmptk", r"Adobe XMP", r"SDK", r"uuid5", r"derivation", r"Live\.arm64", r"/home/",
        r"/var/", r"/tmp/", r"ev_[0-9a-f]", r"\+0x", r"\bkind bit", r"bitmask"]
ALLOWED_HITS = {"AGENTS.md": {"decompil"}}  # forbidden-inputs list, same wording as released packages


def cid(n):
    return f"BROWSER-INDEX-{n:03d}"


def rq(r):
    return f"REQ-BROWSER-INDEX-{r}"


EXCLUDED_INPUTS = [
    "extensions not in the REQ-BROWSER-INDEX-001 table, including other extensions the application recognizes; "
    "extensions with upper-case letters; names without an extension; folders, device folders and plug-ins",
    "sidecar folders with another letter case; sidecar folders below F; files with any other name in F's sidecar "
    "folder; any other location of a sidecar; user folders inside the User Library",
    "sidecar text in another form than REQ-BROWSER-INDEX-004 clause 1: a packet wrapper, an XML declaration, another "
    "encoding, attribute or other alternative RDF forms, carriage returns, unknown properties, document-level tags or "
    "labels, and hideKeywords, assetId or contentHash in input",
    "a resource, format or platform other than folder, application/vnd.ableton.folder and mac",
    "a filePath that differs from an item only in letter case, absolute paths, . or .. levels, \\ separators, or a "
    "trailing /; a filePath that contains / or names a folder; the tags and labels of items inside a subfolder of F",
    "color entries other than exactly 1 to 7, 0, 8 or empty; keyword entries that are empty, repeated, of one level, "
    "or of four or more levels; leading or trailing spaces in any value",
    "the tags and labels of items inside a tagged folder; more than one sidecar for the same folder",
    "edits to items inside a subfolder of F; edits when F already has a sidecar folder; edits that leave an item with "
    "no tags and no labels; read-only volumes; a missing User Library",
    "inputs that combine conditions this release excludes",
]
EXCLUDED_BEHAVIOR = [
    "whether and how files and folders are listed or offered in any browser view or category, including files "
    "without a content kind and the sidecar folder itself",
    "how tags and color labels are presented, grouped, searched or filtered",
    "when a sidecar is written after an edit, any batching, and what happens on quit",
    "the name of the folder between Ableton Folder Info and the sidecars for factory and built-in content, their "
    "content, and how they are read",
    "whether other entries of an existing sidecar are kept when it is rewritten, and whether the application rewrites "
    "a sidecar after reading it, for example without the entries that name no file",
    "previews, changes on disk, missing or moved items, unavailable locations, unsupported or undecodable files, and "
    "the application's index (REQ-BROWSER-INDEX-002, 009 to 013, unreleased)",
    "messages, logs and dialogs, undo, progress and timing",
]


def manifest_meta():
    return {
        "schema": "handoff-manifest-v1", "release_id": "browser-index-v1", "release_status": "candidate-unreviewed",
        "release_date": None, "target": TARGET,
        "specification": {"id": "SPEC-BROWSER-INDEX", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-UI", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {
            rq("001"): "Content kind of a file from its lowercase extension, for the listed extensions only; listing excluded",
            rq("003"): "Only a sidecar whose parent folder is named exactly Ableton Folder Info is read; the user-folder sidecar name in F's sidecar folder is read and describes files directly inside F",
            rq("004"): "Folder-resource sidecar form of the fixtures; informational xmp properties ignored; a sidecar that is not well-formed gives no tags or labels",
            rq("005"): "An entry whose filePath is exactly the name of a file directly inside F applies to that file; an entry naming nothing does not affect other entries",
            rq("006"): "keywords entries give tags; colors entries 1 to 7 give labels, 0, 8 and empty entries are ignored; written encoding",
            rq("007"): "User-folder sidecar name, location and data model of a new sidecar for an item directly in F; override file names for the Core Library and built-in content; timing and the override folder excluded",
            rq("008"): "A folder copied with its sidecar folder keeps its tags when added on another installation",
        },
        "unreleased_requirements": [rq("002"), rq("009"), rq("010"), rq("011"), rq("012"), rq("013")],
        "compatibility_dimensions": {
            "file-classification": "static-derived expectations; reference execution not-run; observation channel to be designed",
            "sidecar-read": "static-derived expectations; reference execution not-run",
            "sidecar-written": "static-derived name, location and data model; reference execution not-run; write timing excluded",
            "ui": "excluded", "index-storage": "excluded (internal)", "audio": "excluded", "timing": "excluded",
        },
        "exclusions": {"inputs_without_expectation": EXCLUDED_INPUTS, "behavior": EXCLUDED_BEHAVIOR},
        "fixture_origin": "independently authored minimal WAV files and sidecar texts from one template; no shipped file content or program code",
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": None, "entrypoint": "README.md", "case_count": len(CASES),
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def case_json(c):
    n = c["n"]
    base = {"id": cid(n), "purpose": c["purpose"], "requirements": [rq(r) for r in c["reqs"]], "case_kind": c["kind"]}
    if "names" in c:
        base["input"] = {"file_names": list(c["names"])}
        base["expected"] = {"content_kind": c["names"]}
        base["comparator"] = "content_kind exact per file name"
    elif "edit" in c:
        base["input"] = {"folder": f"fixtures/{cid(n)}/F"}
        base["action"] = {"item": c["edit"]["item"], "set_tags": c["edit"]["tags"], "set_labels": c["edit"]["labels"]}
        base["expected"] = {"sidecar_path": SIDE_REL, "sidecar": c["doc"],
                            "example_serialization": f"fixtures/{cid(n)}/expected-sidecar.xmp"}
        base["comparator"] = "sidecar data model (spec.md); an absent file is inconclusive"
    elif "override" in c:
        o = c["override"]
        base["input"] = {"precondition": f"the target's {o['content']} is installed and indexed; the User Library exists"}
        base["action"] = {"item": f"one item of the {o['content']}", "set_tags": ["Character|Warm"], "set_labels": []}
        base["expected"] = {"override_file_name": o["name"],
                            "override_parent": "a folder directly inside <User Library>/Ableton Folder Info/ whose name is the decimal text of an integer (not compared)",
                            "no_sidecar_written_inside": f"the {o['content']}"}
        base["comparator"] = "file name exact; parent depth exact; parent name not compared; content not compared; no sidecar file inside the named content created or changed; an absent file is inconclusive"
    else:
        base["input"] = {"folder": f"fixtures/{cid(n)}/F"}
        base["action"] = "add F as a user folder in a fresh state and let indexing complete"
        base["expected"] = {"tags": c["tags"], "labels": c["labels"]}
        base["comparator"] = "tags and labels as sets, for the listed items only"
    base.update({"expectation_provenance": PROV, "reference_execution": "not-run", "candidate_execution": "not-run"})
    return base


def build():
    fx = STAGE / "fixtures"
    if fx.exists():  # rebuild from scratch so stale fixtures cannot survive
        for p in sorted(fx.rglob("*"), reverse=True):
            p.unlink() if p.is_file() else p.rmdir()
    for c in CASES:
        for rel, data in c.get("tree", {}).items():
            p = fx / cid(c["n"]) / "F" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        if "edit" in c:
            (fx / cid(c["n"]) / "F").mkdir(parents=True, exist_ok=True)
            d = c["doc"]["items"][0]
            ser = sidecar([(d["filePath"], d["keywords"], d["colors"] or None)])
            (fx / cid(c["n"]) / "expected-sidecar.xmp").write_bytes(ser)
    doc_ = {"schema": "browser-index-cases-v1", "target": TARGET,
            "scope": "browser-index-v1 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
            "fixture_origin": "Independently authored minimal files; no shipped file copied",
            "oracle_status": "Static-derived expectations; neither reference nor candidate executed",
            "representation": {
                "content_kind": "release label per file name, or none",
                "tags": "set of tag texts assigned to an item", "labels": "set of color label numbers 1 to 7",
                "sidecar": "sidecar data model as defined in spec.md",
                "note": "project comparison representation, not an API of the original application or a required design"},
            "cases": [case_json(c) for c in CASES]}
    (STAGE / "cases.json").write_text(json.dumps(doc_, indent=1, ensure_ascii=False) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(), indent=1) + "\n")
    print(len(CASES), "cases staged")


# ---- package checks ----
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
    refs = [c["input"]["folder"] for c in cases if "folder" in c["input"]] + \
           [c["expected"]["example_serialization"] for c in cases if "example_serialization" in c["expected"]]
    missing_inputs = [r for r in refs if not (d / r).exists()]
    symlinks = [str(p.relative_to(d)) for p in d.rglob("*") if p.is_symlink()]
    deny = {}
    for p in [*files, d / "manifest.json"]:
        text = p.read_bytes().decode("latin-1")
        hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad_links, "missing_case_inputs": missing_inputs, "symlinks": symlinks,
            "deny_list_hits": deny, "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    by_id = {cid(c["n"]): c for c in CASES}
    problems = {}
    for cj in cases:
        c, errs = by_id[cj["id"]], []
        try:
            if "tags" in c:
                got = model_read(STAGE / cj["input"]["folder"], list(c["tags"]))
                if got != ({k: sorted(v) for k, v in c["tags"].items()}, {k: sorted(v) for k, v in c["labels"].items()}):
                    errs.append(f"model_read {got} != expected")
            elif "edit" in c:
                got = model_write(STAGE / cj["input"]["folder"], c["edit"])
                if norm(got) != norm(c["doc"]):
                    errs.append(f"model_write {got} != expected")
                ser = parse_sidecar((STAGE / cj["expected"]["example_serialization"]).read_bytes())
                if norm(ser) != norm(c["doc"]):
                    errs.append("example serialization data model differs from expected")
        except NoExpectation as e:
            errs.append(f"model has no expectation: {e}")
        if errs:
            problems[cj["id"]] = errs
    fixtures = {str(p.relative_to(STAGE)): inspect_fixture(p) for p in sorted((STAGE / "fixtures").rglob("*")) if p.is_file()}
    bad_fixtures = {k: v for k, v in fixtures.items() if not all(x for x in v.values() if isinstance(x, bool))
                    and not k.endswith(f"{cid(15)}/F/{SIDE_REL}")}
    trunc = fixtures[f"fixtures/{cid(15)}/F/{SIDE_REL}"]
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "browser-index-v1 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "kind_table": check_kinds(EXT_KIND, LABEL_BITS, CASES),
              "mutation_probe": mutation_probe(STAGE, CASES, EXT_KIND, LABEL_BITS, cid), "sidecar_names": check_names(), "evidence_identity": check_evidence(),
              "fixtures": fixtures, "fixture_problems": bad_fixtures,
              "truncated_fixture_not_well_formed": trunc["well_formed"] is False, **verify(STAGE),
              "limits": "Checks authored consistency only: no reference or candidate executed; the models restate the "
                        "same static evidence and are not an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    trace = {"schema": "browser-index-traceability-v1", "spec": "SPEC-BROWSER-INDEX r1", "clauses": trace_bi.CLAUSES,
             "evidence": trace_bi.E, "inferred_links": trace_bi.I,
             "cases": {cid(n): {"source": src, "evidence": ev, "inferred": inf} for n, (src, ev, inf) in trace_bi.TRACE.items()}}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    assert all(k in trace_bi.E for _, ev, _ in trace_bi.TRACE.values() for k in ev)
    assert all(i in trace_bi.I for *_, inf in trace_bi.TRACE.values() for i in inf)
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "kind_table", "mutation_probe", "sidecar_names", "evidence_identity",
                                             "fixture_problems", "truncated_fixture_not_well_formed", "payload_files",
                                             "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
                                             "missing_case_inputs", "deny_list_hits", "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"build": build, "seal": seal}[cmd]()
