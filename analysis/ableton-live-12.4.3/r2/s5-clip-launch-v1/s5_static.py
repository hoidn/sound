"""S5 static half: clip launch settings in Live's shipped schemas and LiveSet documents.

Usage: python3 -I s5_static.py <bundle Contents dir> <out.json> <inputs.tsv> <clip-records.tsv>
Read-only on inputs. Schema part: every non-AppleDouble App-Resources/Schema/*.txt, ordered by
(major, minor, number) from the file name (presentation order, not proven migration order);
per-version fields of the launch-related classes and their evolution segments. Document part:
every non-AppleDouble *.als / *.alc below Contents (gzip or plain XML); every AudioClip/MidiClip
element with its context, launch fields and FollowAction; LiveSet GlobalQuantisation and
AutoQuantisation; scene FollowAction; consistency checks named in `checks`.
inputs.tsv: sha256, bytes, gzip flag, relative path of each document read.
clip-records.tsv: one row per clip element (document, context, class, launch fields, FollowAction).
"""
import collections, gzip, hashlib, json, os, re, sys
import xml.etree.ElementTree as ET

CLASSES = {  # class -> fields of interest (None = all fields)
    "AudioClip": ["LaunchMode", "LaunchQuantisation", "Legato", "VelocityAmount", "FollowAction",
                  "FollowTime", "FollowActionA", "FollowActionB", "FollowChanceA", "FollowChanceB"],
    "MidiClip": ["LaunchMode", "LaunchQuantisation", "Legato", "VelocityAmount", "FollowAction",
                 "FollowTime", "FollowActionA", "FollowActionB", "FollowChanceA", "FollowChanceB"],
    "FollowAction": None, "Scene": ["FollowAction"],
    "LiveSet": ["GlobalQuantisation", "GlobalQuantisationKeyMidi", "AutoQuantisation"],
    "RemoteableEnum": None, "RemoteableBool": None, "UserFloat": None, "RemoteableDouble": None,
    "RemoteableInt": None, "RangedRemoteableInt": None,
}
LAUNCH = ["LaunchMode", "LaunchQuantisation", "Legato", "VelocityAmount"]
FA = ["FollowTime", "IsLinked", "LoopIterations", "FollowActionA", "FollowActionB",
      "FollowChanceA", "FollowChanceB", "JumpIndexA", "JumpIndexB", "FollowActionEnabled"]


def vkey(name):
    m = re.fullmatch(r"(\d+)\.(\d+)_(\d+)\.txt", name)
    if not m:
        raise ValueError(f"unexpected schema file name {name!r}")
    return tuple(int(x) for x in m.groups())


def vname(k):
    return f"{k[0]}.{k[1]}_{k[2]}"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def schema_part(sdir):
    files = sorted((f for f in os.listdir(sdir) if f.endswith(".txt") and not f.startswith("._")), key=vkey)
    skipped = sorted(f for f in os.listdir(sdir) if f.startswith("._"))
    versions, segs, latest = [], collections.OrderedDict(), None
    for f in files:
        raw = open(os.path.join(sdir, f), "rb").read()
        root = ET.fromstring(raw)
        v = vname(vkey(f))
        versions.append({"version": v, "sha256": sha(raw)})
        cur = {}
        for cls, want in CLASSES.items():
            el = root.find(cls)
            for i, fl in enumerate([] if el is None else el):
                if want is None or fl.tag in want:
                    cur[f"{cls}.{fl.tag}"] = f"{fl.get('Class')}:{fl.get('Type')}"
        for key in sorted(set(cur) | set(segs)):
            s = segs.setdefault(key, [])
            val = cur.get(key)
            if s and s[-1]["value"] == val and s[-1]["last"] == versions[-2]["version"]:
                s[-1]["last"] = v
            else:
                s.append({"value": val, "first": v, "last": v})
        latest = root
    order = {c: [fl.tag for fl in latest.find(c)] for c in ("AudioClip", "MidiClip", "FollowAction")}
    launch_holders = sorted(c.tag for c in latest if c.find("LaunchQuantisation") is not None
                            or c.find("LaunchMode") is not None)
    homonyms = {t: sorted(c.tag for c in latest if c.find(t) is not None)
                for t in ("Legato", "VelocityAmount", "FollowAction", "LaunchMode")}
    evolution = {k: [x for x in s if x["value"] is not None] for k, s in sorted(segs.items())}
    return {"files_parsed": len(files), "appledouble_skipped": len(skipped), "versions": versions,
            "evolution": evolution, "field_order_latest": order,
            "classes_with_launch_fields_latest": launch_holders, "homonyms_latest": homonyms}


def read_doc(path):
    raw = open(path, "rb").read()
    gz = raw[:2] == b"\x1f\x8b"
    return raw, gz, ET.fromstring(gzip.decompress(raw) if gz else raw)


def val(el, sub, attr="Value"):
    x = el.find(sub) if el is not None else None
    return None if x is None else x.get(attr)


def context(path):
    if "/ClipSlot/ClipSlot/Value/" in path:
        return "session"
    if "/ArrangerAutomation/Events/" in path:
        return "arrangement-take" if "/TakeLanes/" in path else "arrangement"
    if "/GroovePool/" in path:
        return "groove-pool"
    return "other:" + "/".join(path.split("/")[-4:])


def clips(root):
    stack = [(root, root.tag)]
    while stack:
        el, path = stack.pop()
        for c in el:
            p = f"{path}/{c.tag}"
            if c.tag in ("AudioClip", "MidiClip"):
                yield p, c
            stack.append((c, p))


def fa_values(fa):
    return None if fa is None else {k: val(fa, k) for k in FA}


def doc_part(contents):
    paths = sorted(os.path.join(d, f) for d, _, fs in os.walk(contents) for f in fs
                   if f.endswith((".als", ".alc")) and not f.startswith("._"))
    skipped = sum(1 for d, _, fs in os.walk(contents) for f in fs
                  if f.endswith((".als", ".alc")) and f.startswith("._"))
    inputs, dist, records = [], collections.defaultdict(collections.Counter), []
    checks = collections.Counter()
    order_ok = collections.Counter()
    for p in paths:
        raw, gz, root = read_doc(p)
        rel = os.path.relpath(p, contents)
        inputs.append(f"{sha(raw)}\t{len(raw)}\t{int(gz)}\t{rel}")
        ls = root.find("LiveSet")
        minor = root.get("MinorVersion")
        dist["doc.minor_creator"][f"{minor}|{root.get('Creator')}"] += 1
        if ls is None:
            continue
        for k in ("GlobalQuantisation", "AutoQuantisation"):
            dist[f"liveset.{k}"][val(ls, k)] += 1
        for sc in ls.findall("Scenes/Scene"):
            f = fa_values(sc.find("FollowAction"))
            for k, v in (f or {}).items():
                dist[f"scene.FollowAction.{k}"][v] += 1
        for path, c in clips(root):
            ctx = context(path)
            rec = {"doc": rel, "context": ctx, "type": c.tag,
                   **{k: val(c, k) for k in LAUNCH}, "fa": fa_values(c.find("FollowAction")),
                   "loop": [val(c, "Loop/LoopStart"), val(c, "Loop/LoopEnd"), val(c, "Loop/LoopOn")],
                   "current": [val(c, "CurrentStart"), val(c, "CurrentEnd")]}
            records.append(rec)
            dist["clip.context"][ctx] += 1
            for k in LAUNCH:
                dist[f"clip.{k}"][rec[k]] += 1
                dist[f"clip.{k}.by_context"][f"{ctx}|{rec[k]}"] += 1
            for k, v in (rec["fa"] or {}).items():
                dist[f"clip.FollowAction.{k}"][v] += 1
            kids = [x.tag for x in c]
            order_ok[f"{c.tag}|{'FollowAction' in kids and kids.index('FollowAction') == kids.index('VelocityAmount') + 1}"] += 1
            f = rec["fa"]
            if f and f["FollowActionEnabled"] is not None:
                derived = (f["FollowActionA"] != "0" and float(f["FollowChanceA"]) != 0) or \
                          (f["FollowActionB"] != "0" and float(f["FollowChanceB"]) != 0)
                checks[f"enabled={f['FollowActionEnabled']}|translator-0x1a1-rule={str(derived).lower()}"] += 1
                if f["IsLinked"] == "true" and rec["loop"][0] is not None:
                    span = float(rec["loop"][1]) - float(rec["loop"][0])
                    checks[f"linked|followtime==loop_span:{float(f['FollowTime']) == span}"] += 1
    return {"files": len(paths), "appledouble_skipped": skipped,
            "distributions": {k: dict(sorted(v.items(), key=lambda kv: (-kv[1], str(kv[0])))) for k, v in dist.items()},
            "checks": dict(sorted(checks.items())), "followaction_after_velocityamount": dict(order_ok),
            }, inputs, records


def main():
    contents, out, tsv, rtsv = sys.argv[1:5]
    res = {"schema": schema_part(os.path.join(contents, "App-Resources", "Schema"))}
    res["documents"], inputs, records = doc_part(contents)
    json.dump(res, open(out, "w"), indent=1, sort_keys=False)
    open(tsv, "w").write("sha256\tbytes\tgzip\tpath\n" + "\n".join(inputs) + "\n")
    cols = ["doc", "context", "type"] + LAUNCH
    with open(rtsv, "w") as o:
        o.write("\t".join(cols + FA) + "\n")
        for r in records:
            o.write("\t".join(str(r[c]) for c in cols) + "\t" +
                    "\t".join(str((r["fa"] or {}).get(k)) for k in FA) + "\n")


if __name__ == "__main__":
    main()
