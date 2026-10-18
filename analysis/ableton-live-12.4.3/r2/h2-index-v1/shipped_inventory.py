"""Structural inventory of browser-index inputs shipped in Ableton Live 12.4.3 App-Resources.

Usage: python3 -I shipped_inventory.py <App-Resources dir> <scratch copy of filerefmap.db> <out.json>
Records schema, counts and vocabularies only (no content dumps):
  * filerefmap.db: sqlite_master SQL, row counts, pragmas, meta_info key names and value lengths,
    aggregate distributions of the mapping columns.
  * every 'Ableton Folder Info' directory (AppleDouble '._*' files skipped): file counts by
    extension and by name; Properties.cfg/other text cfg class and field vocabulary.
  * every .xmp sidecar: header values, element vocabulary, item counts, whether each
    ablFR:filePath resolves relative to the folder that contains 'Ableton Folder Info', keyword
    depth histogram and top-level keyword segment counts.
  * Previews/*.ogg: whether the source item exists at the same relative path without '.ogg'.
The database must be a scratch copy; it is opened with mode=ro.
"""
import collections, hashlib, json, os, re, sqlite3, sys
import xml.etree.ElementTree as ET

NS = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "dc": "http://purl.org/dc/elements/1.1/",
      "ablFR": "https://ns.ableton.com/xmp/fs-resources/1.0/"}
UUID_NAME = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-([0-9a-f])[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}\.xmp$")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def filerefmap(path):
    c = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    q = lambda sql: c.execute(sql).fetchall()
    tables = [n for (n,) in q("select name from sqlite_master where type='table' order by name")]
    ext = lambda col: dict(collections.Counter(os.path.splitext(v)[1].lower() for (v,) in q(f"select {col} from sample_mapping")).most_common())
    return {
        "sha256": sha256(path), "bytes": os.path.getsize(path),
        "schema": [list(r) for r in q("select type, name, tbl_name, sql from sqlite_master order by type, name")],
        "row_counts": {t: q(f'select count(*) from "{t}"')[0][0] for t in tables},
        "pragmas": {p: q(f"pragma {p}")[0][0] for p in ("user_version", "application_id", "page_size", "encoding", "schema_version")},
        "meta_info": [{"key": k, "value_length": n} for k, n in q("select key, length(value) from meta_info")],
        "sample_mapping": {
            "src_type": dict(q("select src_type, count(*) from sample_mapping group by 1")),
            "dst_type": dict(q("select dst_type, count(*) from sample_mapping group by 1")),
            "src_packid_empty": q("select count(*) from sample_mapping where src_packid=''")[0][0],
            "dst_packid_empty": q("select count(*) from sample_mapping where dst_packid=''")[0][0],
            "dst_packid_null": q("select count(*) from sample_mapping where dst_packid is null")[0][0],
            "distinct_src_packid": q("select count(distinct src_packid) from sample_mapping")[0][0],
            "distinct_dst_packid": q("select count(distinct dst_packid) from sample_mapping")[0][0],
            "dst_packids_in_pack_names": q("select count(distinct dst_packid) from sample_mapping where dst_packid in (select packid from pack_names)")[0][0],
            "src_packids_in_pack_names": q("select count(distinct src_packid) from sample_mapping where src_packid in (select packid from pack_names)")[0][0],
            "same_ref": q("select count(*) from sample_mapping where src_ref=dst_ref")[0][0],
            "absolute_src_ref": q("select count(*) from sample_mapping where src_ref like '/%'")[0][0],
            "absolute_dst_ref": q("select count(*) from sample_mapping where dst_ref like '/%'")[0][0],
            "src_ref_extensions": ext("src_ref"), "dst_ref_extensions": ext("dst_ref"),
        },
        "pack_names": {"packid_length_min_max": list(q("select min(length(packid)), max(length(packid)) from pack_names")[0])},
    }


def text_cfg(path):
    """Header and 'Type Name' field vocabulary of an Ableton text cfg; None for binary/XML."""
    raw = open(path, "rb").read().removeprefix(b"\xef\xbb\xbf")
    if raw.startswith(b"<?xml"):
        root = ET.fromstring(raw)
        return {"format": "xml", "root": root.tag, "attributes": sorted(root.attrib), "child": [c.tag for c in root][:3]}
    if not raw.startswith(b"Ableton#"):
        return {"format": "binary", "magic_hex": raw[:8].hex()}
    text = raw.decode("utf-8", "replace")
    classes = re.findall(r"^\s*([A-Za-z]\w*)\s*$", text, re.M)
    fields = re.findall(r"^\s*([A-Z]\w*(?:<[^>]*>)?)\s+(\w+)\s*=", text, re.M)
    return {"format": "text", "header": text.split("\n", 1)[0], "classes": classes, "fields": [f"{t} {n}" for t, n in fields]}


def xmp(path, base):
    root = ET.parse(path).getroot()
    tags = collections.Counter(re.sub(r"\{[^}]*\}", lambda m: {v: k + ":" for k, v in NS.items()}.get(m.group(0)[1:-1], m.group(0)), e.tag) for e in root.iter())
    desc = root.find(".//rdf:Description", NS)
    head = {k: (desc.findtext(f"{k.split(':')[0]}:{k.split(':')[1]}", namespaces=NS)) for k in ("dc:format", "ablFR:resource", "ablFR:platform", "ablFR:packVersion")}
    items = desc.findall("ablFR:items/rdf:Bag/rdf:li", NS)
    resolved = missing = 0
    depth, top = collections.Counter(), collections.Counter()
    for it in items:
        fp = it.findtext("ablFR:filePath", namespaces=NS)
        if fp is not None:
            if os.path.lexists(os.path.join(base, fp)):
                resolved += 1
            else:
                missing += 1
        for kw in it.findall("ablFR:keywords/rdf:Bag/rdf:li", NS):
            parts = (kw.text or "").split("|")
            depth[len(parts)] += 1
            top[parts[0]] += 1
    m = UUID_NAME.match(os.path.basename(path))
    return {"head": head, "has_pack_unique_id": desc.find("ablFR:packUniqueId", NS) is not None,
            "uuid_version": m.group(1) if m else None, "tags": tags, "items": len(items),
            "filepath_resolved": resolved, "filepath_missing": missing, "keyword_depth": depth, "keyword_top": top}


def main(app, db, out):
    result = {"filerefmap": filerefmap(db)}
    dirs, by_ext, by_name, cfg = [], collections.Counter(), collections.Counter(), {}
    x = {"files": 0, "head": collections.Counter(), "tags": collections.Counter(), "items": 0, "resolved": 0,
         "missing": 0, "keyword_depth": collections.Counter(), "keyword_top": collections.Counter(),
         "uuid_version": collections.Counter(), "with_pack_unique_id": 0, "per_file": []}
    prev = {"ogg": 0, "source_exists": 0, "asd_companions": 0}
    for cur, subdirs, files in os.walk(app):
        files = [f for f in files if not f.startswith("._")]
        if os.path.basename(cur) == "Ableton Folder Info":
            dirs.append(os.path.relpath(cur, app))
        if "Ableton Folder Info" not in cur.split(os.sep):
            continue
        info_root = cur[:cur.index(os.sep + "Ableton Folder Info")]
        for f in files:
            p = os.path.join(cur, f)
            by_ext[os.path.splitext(f)[1].lower()] += 1
            if f.endswith((".cfg", ".json", ".als", ".xmp")):
                by_name[f if not f.endswith(".xmp") else "<*.xmp>"] += 1
            if f.endswith(".cfg"):
                key = f
                summary = text_cfg(p)
                cfg.setdefault(key, collections.Counter())[json.dumps(summary, sort_keys=True)] += 1
            if f.endswith(".xmp"):
                r = xmp(p, info_root)
                x["files"] += 1
                x["head"][json.dumps(r["head"], sort_keys=True)] += 1
                x["tags"].update(r["tags"])
                x["items"] += r["items"]; x["resolved"] += r["filepath_resolved"]; x["missing"] += r["filepath_missing"]
                x["keyword_depth"].update(r["keyword_depth"]); x["keyword_top"].update(r["keyword_top"])
                x["uuid_version"][str(r["uuid_version"])] += 1
                x["with_pack_unique_id"] += r["has_pack_unique_id"]
                x["per_file"].append({"path": os.path.relpath(p, app), "resource": r["head"]["ablFR:resource"], "items": r["items"],
                                      "resolved": r["filepath_resolved"], "missing": r["filepath_missing"],
                                      "hide_keywords": r["tags"].get("ablFR:hideKeywords", 0)})
            if f.endswith(".ogg") and os.sep + "Previews" in cur:
                prev["ogg"] += 1
                rel = os.path.relpath(p, os.path.join(info_root, "Ableton Folder Info", "Previews"))
                prev["source_exists"] += os.path.lexists(os.path.join(info_root, rel[:-4]))
                prev["asd_companions"] += os.path.exists(p + ".asd")
    result["folder_info"] = {"directories": len(dirs), "directory_parents": dict(collections.Counter(d.split(os.sep)[0] for d in dirs)),
                             "files_by_extension": dict(by_ext), "cfg_json_als_xmp_by_name": dict(by_name),
                             "cfg_structures": {k: [{"count": n, "summary": json.loads(s)} for s, n in v.most_common()] for k, v in cfg.items()}}
    result["xmp"] = {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in x.items()}
    result["xmp"]["per_file"] = sorted(x["per_file"], key=lambda r: r["path"])
    result["xmp"]["head"] = [{"count": n, "values": json.loads(s)} for s, n in x["head"].most_common()]
    result["previews"] = prev
    json.dump(result, open(out, "w"), indent=1, sort_keys=True, default=str)


if __name__ == "__main__":
    main(*sys.argv[1:4])
