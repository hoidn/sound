"""H4 static: schema declarations of the seven bundle-backed device classes across all shipped schemas.

Usage: python3 -I schema_devices.py <Schema dir> <out dir>
Writes out/schema_devices.json:
  device_base_prefix: fields shared, in order, by every device class in 12.0_12402 (the common device envelope)
  current[<class>]: flattened device-specific fields of 12.0_12402 as [path, class]; composite classes declared
                    in the schema are expanded unless they are Timeable*/Remoteable*/shared wrappers
  history[<class>]: per schema file (ordered by family, then translator number) the first appearance and
                    added/removed device-specific flattened paths (base envelope excluded) relative to the previous file declaring the class
Depends on: Python stdlib only. Schema files are data.
"""
import json, os, re, sys
import xml.etree.ElementTree as ET

DEVICES = ["Amp", "Cabinet", "UltraAnalog", "StringStudio", "Collision", "LoungeLizard", "Corpus"]
LEAF_PREFIXES = ("Timeable", "Remoteable", "Slot", "List", "Python", "Pointee", "Int", "Float", "Bool", "String")


def load(path):
    root = ET.parse(path).getroot()
    return {c.tag: [(f.tag, f.get("Class")) for f in c] for c in root}


def flatten(classes, name, prefix="", depth=0):
    out = []
    for field, cls in classes.get(name, []):
        path = f"{prefix}{field}"
        if cls in classes and not cls.startswith(LEAF_PREFIXES) and depth < 6 and cls not in DEVICES:
            out += flatten(classes, cls, path + "/", depth + 1)
        else:
            out.append([path, cls])
    return out


def key(fn):
    fam, tr = re.match(r"^(\d+\.\d+)_(\d+)\.txt$", fn).groups()
    return tuple(int(x) for x in fam.split(".")), int(tr)


def main(schema_dir, outdir):
    files = sorted((f for f in os.listdir(schema_dir) if re.match(r"^\d+\.\d+_\d+\.txt$", f)), key=key)
    current = load(os.path.join(schema_dir, "12.0_12402.txt"))
    # the shared device envelope: longest common ordered prefix of all classes that carry OverwriteProtectionNumber
    devlike = [c for c, fs in current.items() if any(f == "OverwriteProtectionNumber" for f, _ in fs) and fs[0][0] == "LomId"]
    prefix = current[devlike[0]]
    for c in devlike:
        n = 0
        while n < min(len(prefix), len(current[c])) and prefix[n] == current[c][n]:
            n += 1
        prefix = prefix[:n]
    base = {f for f, _ in prefix}
    res = {"schema_dir": schema_dir, "order": "family (numeric), then translator number", "files": len(files),
           "device_like_classes": len(devlike), "device_base_prefix": prefix, "current": {}, "history": {}}
    for d in DEVICES:
        res["current"][d] = [p for p in flatten(current, d) if p[0].split("/")[0] not in base]
        res["current_base_matches_prefix"] = res.get("current_base_matches_prefix", {})
        res["current_base_matches_prefix"][d] = current[d][:len(prefix)] == prefix
    hist, prev = {d: [] for d in DEVICES}, {d: None for d in DEVICES}
    for f in files:
        cl = load(os.path.join(schema_dir, f))
        for d in DEVICES:
            if d not in cl:
                continue
            cur = {tuple(p) for p in flatten(cl, d) if p[0].split("/")[0] not in base}  # device-specific only
            if prev[d] is None:
                hist[d].append({"schema": f[:-4], "event": "first", "fields": len(cur)})
            elif cur != prev[d]:
                hist[d].append({"schema": f[:-4], "event": "changed", "fields": len(cur),
                                "added": sorted(map(list, cur - prev[d])), "removed": sorted(map(list, prev[d] - cur))})
            prev[d] = cur
    res["history"] = hist
    json.dump(res, open(os.path.join(outdir, "schema_devices.json"), "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
