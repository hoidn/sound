"""H4 static: parameter inventory of the seven bundle-backed devices as stored in shipped documents.

Usage: python3 -I presets.py <App-Resources dir> <out dir>
Scans every non-AppleDouble .adv/.adg/.als/.alc under Core Library/ and Builtin/ (gzip XML), selects documents
whose bytes mention a device element, and parses them with ElementTree. A device occurrence is an element named
in DEVICES whose parent is the 'Ableton' root, a 'Devices' list, or a rack preset's 'Device' slot (AbletonDevicePreset). Inside an occurrence:
  parameter = descendant element with a direct <Manual> child (Timeable* wrapper); path relative to the device
  field     = any other descendant leaf with a Value attribute outside a parameter (Remoteable*/Int fields)
Manual values of a device at the root of Core Library/Defaults/**.adv are reported as default_preset.
Envelopes anywhere in the document (elements with EnvelopeTarget/PointeeId and Automation/Events) are matched
to parameter AutomationTarget/ModulationTarget Ids of the same document.
Writes out/inputs.jsonl (path, size, SHA-256 of every scanned file), out/occurrences.jsonl, out/params.json, out/fields.json, out/envelopes.json, out/scan.json.
Depends on: Python stdlib; out/schema_devices.json (from schema_devices.py) for declared classes.
Values are reported as stored text; no unit or display conversion is applied. params.json keeps every
distinct Manual value; other distributions keep their 8 most common values.
"""
import collections, gzip, hashlib, json, os, re, sys
import xml.etree.ElementTree as ET

DEVICES = ["Amp", "Cabinet", "UltraAnalog", "StringStudio", "Collision", "LoungeLizard", "Corpus"]
TAG_RE = re.compile(rb"<(" + b"|".join(d.encode() for d in DEVICES) + rb")[ >/]")
EXTS = {".adv", ".adg", ".als", ".alc"}


def kind(v):
    if v in ("true", "false"):
        return "bool"
    try:
        int(v)
        return "int"
    except ValueError:
        pass
    try:
        float(v)
        return "float"
    except ValueError:
        return "string"


def num(v):
    return {"true": 1.0, "false": 0.0}.get(v, None) if v in ("true", "false") else float(v)


class Agg:
    """Distribution of stored text values: count, kinds, numeric extremes, most common values."""

    def __init__(self):
        self.c, self.kinds, self.lo, self.hi = collections.Counter(), collections.Counter(), None, None

    def add(self, v):
        self.c[v] += 1
        k = kind(v)
        self.kinds[k] += 1
        if k != "string":
            x = num(v)
            self.lo = x if self.lo is None else min(self.lo, x)
            self.hi = x if self.hi is None else max(self.hi, x)

    def dump(self, top=8):
        return {"n": sum(self.c.values()), "kinds": dict(self.kinds), "min": self.lo, "max": self.hi,
                "distinct": len(self.c), "top": self.c.most_common(top)}


def walk_device(dev):
    """Yield ('param', path, elem) and ('field', path, elem) under one device element."""
    stack = [(child, child.tag) for child in reversed(list(dev))]
    while stack:
        e, path = stack.pop()
        kids = list(e)
        if any(k.tag == "Manual" for k in kids):
            yield "param", path, e
            continue
        if not kids and e.get("Value") is not None:
            yield "field", path, e
        stack += [(k, f"{path}/{k.tag}") for k in reversed(kids)]


def find_devices(root):
    out, stack = [], [(root, None, 0)]
    other = collections.Counter()
    while stack:
        e, parent, depth = stack.pop()
        if e.tag in DEVICES:
            if parent is not None and (parent.tag in ("Devices", "Device") or parent is root):
                out.append((e, "root" if parent is root else parent.tag, depth))
                continue
            other[e.tag] += 1
        nd = depth + (1 if e.tag == "Devices" else 0)
        stack += [(k, e, nd) for k in e]
    return out, other


def main(res, outdir):
    schema = json.load(open(os.path.join(outdir, "schema_devices.json")))
    declared = {d: dict(map(tuple, fs)) for d, fs in schema["current"].items()}
    base = {f for f, _ in schema["device_base_prefix"]}
    params = {d: collections.defaultdict(lambda: collections.defaultdict(Agg)) for d in DEVICES}
    pcount = {d: collections.Counter() for d in DEVICES}
    fields = {d: collections.defaultdict(Agg) for d in DEVICES}
    env = {d: collections.defaultdict(lambda: {"envelopes": 0, "events": collections.Counter(), "value": Agg(),
                                                "target": collections.Counter(), "docs": set()}) for d in DEVICES}
    pathsets = {d: collections.Counter() for d in DEVICES}
    defaults = {d: {} for d in DEVICES}  # Manual values in Core Library/Defaults/<kind>/<Device>.adv
    scan = {"roots": ["Core Library", "Builtin"], "files_by_ext": collections.Counter(),
            "docs_with_tag_bytes": 0, "docs_with_devices": 0, "non_device_tag_uses": collections.Counter(),
            "occurrences": collections.Counter(), "occ_by_ext": collections.Counter(), "parse_errors": [],
            "minor_versions": collections.Counter(), "envelopes_seen": collections.Counter(),
            "set_clip_docs_checked_for_target_id_uniqueness": 0, "set_clip_docs_with_duplicate_target_ids": 0}
    occ_out = open(os.path.join(outdir, "occurrences.jsonl"), "w")
    inputs_out = open(os.path.join(outdir, "inputs.jsonl"), "w")
    for top in scan["roots"]:
        for d, dirs, fs in os.walk(os.path.join(res, top)):
            dirs.sort()
            for f in sorted(fs):
                ext = os.path.splitext(f)[1].lower()
                if f.startswith("._") or ext not in EXTS:
                    continue
                p = os.path.join(d, f)
                scan["files_by_ext"][ext] += 1
                raw = open(p, "rb").read()
                inputs_out.write(json.dumps({"path": os.path.relpath(p, res), "size": len(raw),
                                             "sha256": hashlib.sha256(raw).hexdigest()}) + "\n")
                if raw[:2] != b"\x1f\x8b":
                    continue
                xml = gzip.decompress(raw)
                if not TAG_RE.search(xml):
                    continue
                scan["docs_with_tag_bytes"] += 1
                try:
                    root = ET.fromstring(xml)
                except ET.ParseError as e:
                    scan["parse_errors"].append([os.path.relpath(p, res), str(e)])
                    continue
                devs, other = find_devices(root)
                scan["non_device_tag_uses"].update(other)
                if not devs:
                    continue
                scan["docs_with_devices"] += 1
                rel, sha = os.path.relpath(p, res), hashlib.sha256(raw).hexdigest()
                ids = {}
                for dev, ctx, depth in devs:
                    name = dev.tag
                    scan["occurrences"][name] += 1
                    scan["occ_by_ext"][f"{name}{ext}"] += 1
                    scan["minor_versions"][f"{name} {root.get('MinorVersion')}"] += 1
                    n, keymidi, ps = 0, 0, []
                    for what, path, e in walk_device(dev):
                        if path.split("/")[0] in base:
                            continue
                        if what == "field":
                            fields[name][path].add(e.get("Value"))
                            continue
                        n += 1
                        ps.append(path)
                        pcount[name][path] += 1
                        a = params[name][path]
                        kid = {k.tag: k for k in e}
                        a["Manual"].add(kid["Manual"].get("Value"))
                        if rel.startswith("Core Library/Defaults/") and ctx == "root":
                            defaults[name][path] = kid["Manual"].get("Value")
                        km = kid.get("KeyMidi")
                        mapped = km is not None
                        keymidi += mapped
                        if mapped:
                            a["KeyMidi.Channel"].add(km.find("Channel").get("Value"))
                            a["KeyMidi.NoteOrController"].add(km.find("NoteOrController").get("Value"))
                        for rng in ("MidiControllerRange", "MidiCCOnOffThresholds"):
                            r = kid.get(rng)
                            if r is not None:
                                tag = f"{rng}{'.mapped' if mapped else ''}"
                                a[f"{tag}.Min"].add(r.find("Min").get("Value"))
                                a[f"{tag}.Max"].add(r.find("Max").get("Value"))
                                a[f"{tag}.pair"].add(f"{r.find('Min').get('Value')}..{r.find('Max').get('Value')}")
                        for tgt in ("AutomationTarget", "ModulationTarget"):
                            t = kid.get(tgt)
                            if t is not None:
                                a[f"{tgt}.present"].add("1")
                                a[f"{tgt}.IdIsZero{ext}"].add(str(t.get("Id") == "0").lower())
                                if t.get("Id") != "0":
                                    ids[t.get("Id")] = (name, path, tgt)
                        extra = sorted(set(kid) - {"LomId", "KeyMidi", "Manual", "MidiControllerRange",
                                                   "MidiCCOnOffThresholds", "AutomationTarget", "ModulationTarget"})
                        a["children.extra"].add(",".join(extra) or "-")
                        a["declared_class"].add(declared[name].get(path, "undeclared"))
                    pathsets[name][hashlib.sha256("\n".join(ps).encode()).hexdigest()[:16]] += 1
                    lp = dev.find("LastPresetRef/Value/*/FileRef/RelativePath")
                    occ_out.write(json.dumps({
                        "doc": rel, "doc_sha256": sha, "ext": ext, "minor_version": root.get("MinorVersion"),
                        "device": name, "context": ctx, "devices_depth": depth, "id_attr": dev.get("Id"),
                        "params": n, "macro_or_midi_mapped": keymidi,
                        "user_name": dev.find("UserName").get("Value") if dev.find("UserName") is not None else None,
                        "last_preset": lp.get("Value") if lp is not None else None}, sort_keys=True) + "\n")
                if ext in (".als", ".alc"):  # are nonzero target ids unique across the whole document?
                    tid = collections.Counter(e.get("Id") for e in root.iter() if e.tag in ("AutomationTarget", "ModulationTarget")
                                              and e.get("Id") != "0")
                    scan["set_clip_docs_checked_for_target_id_uniqueness"] += 1
                    scan["set_clip_docs_with_duplicate_target_ids"] += any(v > 1 for v in tid.values())
                for e in root.iter():
                    pid = e.find("EnvelopeTarget/PointeeId")
                    evs = e.find("Automation/Events")
                    if pid is None or evs is None:
                        continue
                    scan["envelopes_seen"][ext] += 1
                    if pid.get("Value") not in ids:
                        continue
                    name, path, tgt = ids[pid.get("Value")]
                    r = env[name][path]
                    r["envelopes"] += 1
                    r["target"][f"{e.tag}->{tgt}"] += 1
                    r["docs"].add(rel)
                    for ev in evs:
                        r["events"][ev.tag] += 1
                        if ev.get("Value") is not None:
                            r["value"].add(ev.get("Value"))
    occ_out.close()
    inputs_out.close()
    out_params = {}
    for d in DEVICES:
        out_params[d] = {"occurrences": scan["occurrences"][d], "distinct_param_path_sets": len(pathsets[d]),
                         "params": {}}
        for path in sorted(params[d], key=lambda p: list(declared[d]).index(p) if p in declared[d] else 10 ** 6):
            out_params[d]["params"][path] = {"present_in": pcount[d][path], "default_preset": defaults[d].get(path),
                                             **{k: v.dump(None if k == "Manual" else 8) for k, v in sorted(params[d][path].items())}}
        out_params[d]["declared_not_seen"] = [p for p, c in declared[d].items()
                                              if c.startswith("Timeable") and p not in params[d]]
    json.dump(out_params, open(os.path.join(outdir, "params.json"), "w"), indent=1)
    json.dump({d: {p: a.dump(5) for p, a in sorted(fields[d].items())} for d in DEVICES},
              open(os.path.join(outdir, "fields.json"), "w"), indent=1)
    json.dump({d: {p: {"envelopes": r["envelopes"], "docs": sorted(r["docs"]), "events": dict(r["events"]),
                       "target": dict(r["target"]), "value": r["value"].dump(5)} for p, r in sorted(env[d].items())}
               for d in DEVICES}, open(os.path.join(outdir, "envelopes.json"), "w"), indent=1)
    json.dump({k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in scan.items()},
              open(os.path.join(outdir, "scan.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
