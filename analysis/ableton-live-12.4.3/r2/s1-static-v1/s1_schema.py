"""S1 static half: transport-state fields in Live's shipped schema files.

Usage: python3 -I s1_schema.py <Schema dir> <out.json>
Reads every non-AppleDouble *.txt in the Schema dir (XML, root AbletonSchema),
records format facts, per-version field tables for selected classes, a
field evolution table, and per-version resolution of document paths through
field Class attributes. Read-only on inputs. Version order is the sort key
(major, minor, number) parsed from file names; it is a presentation order,
not proven migration order.
"""
import collections, hashlib, json, os, re, sys
import xml.etree.ElementTree as ET

FULL = ["Transport", "LoopOn", "LoopStart", "LoopLength", "CurrentTime",
        "TimeableSongTempo", "TimeableFloat", "TimeableTimeSignature",
        "RemoteableFloat", "RemoteableEnum", "RemoteableBool", "UserFloat",
        "MidiControllerRange", "FloatAutomationTarget", "EnumAutomationTarget",
        "SingleTimeSignatureManager", "RemoteableTimeSignature",
        "TimeSignatureNumerator", "TimeSignatureDenominator"]
PARTIAL = {  # big classes: only fields relevant to S1
    "LiveSet": ["Transport", "MasterTrack", "MainTrack", "Scenes"],
    "MasterTrack": ["DeviceChain", "MasterChain"], "MainTrack": ["DeviceChain"],
    "MasterTrackDeviceChain": ["Mixer"], "MainTrackDeviceChain": ["Mixer"],
    "MasterTrackDevice": ["Tempo", "TimeSignature", "TempoAutomationViewBottom",
                          "TempoAutomationViewTop", "UserTempoAutomation"],
    "MainTrackDevice": ["Tempo", "TimeSignature", "TempoAutomationViewBottom",
                        "TempoAutomationViewTop", "UserTempoAutomation"],
    "Scene": ["Tempo", "IsTempoEnabled", "TimeSignatureId", "IsTimeSignatureEnabled"],
}
TRACK = ["MasterTrack", "MainTrack"]
CHAIN = ["DeviceChain", "MasterChain"]
PATHS = {  # document element paths below /Ableton, resolved via field Class
    "transport.<f>": ["LiveSet", "Transport", "*"],
    "tempo.manual": ["LiveSet", TRACK, CHAIN, "Mixer", "Tempo", "Manual", "Value"],
    "tempo.range.min": ["LiveSet", TRACK, CHAIN, "Mixer", "Tempo", "MidiControllerRange", "Min", "Value"],
    "tempo.autotarget.id": ["LiveSet", TRACK, CHAIN, "Mixer", "Tempo", "AutomationTarget", "Id"],
    "timesig.manual": ["LiveSet", TRACK, CHAIN, "Mixer", "TimeSignature", "Manual", "Value"],
}


def vkey(name):
    m = re.fullmatch(r"(\d+)\.(\d+)_(\d+)\.txt", name)
    if not m:
        raise ValueError(f"unexpected schema file name {name!r}")
    return tuple(int(x) for x in m.groups())


def vname(k):
    return f"{k[0]}.{k[1]}_{k[2]}"


def load(path):
    """Return (root attrs, {class: (class attrs, [(field, attrs), ...], line)})."""
    root = ET.parse(path).getroot()
    if root.tag != "AbletonSchema":
        raise ValueError(f"{path}: root {root.tag!r}")
    classes = {}
    for c in root:
        if c.tag in classes:
            raise ValueError(f"{path}: duplicate class {c.tag}")
        classes[c.tag] = (dict(c.attrib), [(f.tag, dict(f.attrib)) for f in c])
        if any(len(f) for f in c):
            raise ValueError(f"{path}: nested field below {c.tag}")
    return dict(root.attrib), classes


def class_lines(path, names):
    """1-based line of each top-level class start tag (one tab indent)."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            m = re.match(r"\t<([A-Za-z0-9_]+)[ >]", line)
            if m and m.group(1) in names and m.group(1) not in out:
                out[m.group(1)] = n
    return out


def resolve(classes, steps):
    """Walk field names from class LiveSet; return chain or failure string."""
    cls, chain = "LiveSet", ["LiveSet"]
    for step in steps[1:]:
        fields = dict(classes.get(cls, ({}, []))[1])
        names = step if isinstance(step, list) else [step]
        hit = [n for n in names if n in fields]
        if not hit:
            return f"missing field {names} in class {cls}"
        f = fields[hit[0]]
        if f.get("Type") == "-4":  # leaf attribute
            chain.append(f"@{hit[0]}:{f['Class']}")
            return " > ".join(chain)
        cls = f["Class"]
        chain.append(f"{hit[0]}:{cls}")
    return " > ".join(chain)


def homonyms(path):
    """Every class in one schema declaring a field with an S1 field name."""
    _, classes = load(path)
    names = ["Transport", "LoopOn", "LoopStart", "LoopLength", "CurrentTime", "Tempo",
             "TimeSignature", "PhaseNudgeTempo", "Manual"]
    out = {n: [] for n in names}
    for cname, (_, fields) in classes.items():
        for f, a in fields:
            if f in out:
                out[f].append([cname, a.get("Class"), a.get("Type")])
    out["Manual"] = {"classes_declaring": len(out["Manual"])}
    return out


def segments(series):
    """series: list of (version, value or None) -> runs of equal value."""
    runs = []
    for v, val in series:
        if runs and runs[-1]["value"] == val:
            runs[-1]["to"], runs[-1]["n"] = v, runs[-1]["n"] + 1
        else:
            runs.append({"from": v, "to": v, "n": 1, "value": val})
    return runs


def main(schema_dir, out_path):
    names = sorted(os.listdir(schema_dir))
    skipped = [n for n in names if n.startswith("._")]
    files = sorted((n for n in names if not n.startswith("._")), key=vkey)
    versions, tables, fmt = [], {}, collections.Counter()
    resolved = collections.defaultdict(list)
    wanted = set(FULL) | set(PARTIAL)
    for name in files:
        path = os.path.join(schema_dir, name)
        data = open(path, "rb").read()
        rattrs, classes = load(path)
        v = vname(vkey(name))
        lines = class_lines(path, wanted)
        versions.append({"version": v, "file": name, "bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest(), "root": rattrs,
                         "classes": len(classes),
                         "fields": sum(len(f) for _, f in classes.values())})
        for cname, (cattrs, fields) in classes.items():
            fmt[("class_attrs", tuple(sorted(cattrs)))] += 1
            for fname, fa in fields:
                fmt[("field_attrs", tuple(sorted(fa)))] += 1
                fmt[("Type", fa.get("Type"))] += 1
        for cname in sorted(wanted):
            if cname not in classes:
                continue
            keep = PARTIAL.get(cname)
            tables.setdefault(cname, {})[v] = {
                "line": lines.get(cname), "class_attrs": classes[cname][0],
                "fields": [[f, a] for f, a in classes[cname][1] if keep is None or f in keep]}
        for key, steps in PATHS.items():
            if steps[-1] == "*":
                for f, _ in classes.get("Transport", ({}, []))[1]:
                    resolved[f"transport.{f}"].append(
                        (v, resolve(classes, steps[:-1] + [f, "Value"])))
            else:
                resolved[key].append((v, resolve(classes, steps)))
    order = [x["version"] for x in versions]
    evolution = {}
    for cname, per_v in tables.items():
        fnames = []
        for v in order:
            for f, _ in per_v.get(v, {"fields": []})["fields"]:
                if f not in fnames:
                    fnames.append(f)
        evo = {"class_present": segments([(v, v in per_v) for v in order])}
        for f in fnames:
            series = []
            for v in order:
                a = dict(per_v[v]["fields"]).get(f) if v in per_v else None
                series.append((v, None if a is None else " ".join(f"{k}={a[k]}" for k in sorted(a))))
            evo[f] = segments(series)
        evolution[cname] = evo
    # field order of Transport per version, compressed
    t_order = segments([(v, [f for f, _ in tables["Transport"][v]["fields"]])
                        for v in order if v in tables["Transport"]])
    out = {
        "schema_dir": schema_dir, "files_parsed": len(files),
        "appledouble_skipped": len(skipped),
        "version_order": "sorted by (major, minor, number) from file name",
        "format_counts": [[list(k), n] for k, n in sorted(fmt.items(), key=str)],
        "versions": versions,
        "class_tables_latest": {c: t[order[-1]] for c, t in tables.items() if order[-1] in t},
        "evolution": evolution,
        "transport_field_order": t_order,
        "path_resolution": {k: segments(v) for k, v in resolved.items()},
        "homonyms_latest": homonyms(os.path.join(schema_dir, files[-1])),
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
