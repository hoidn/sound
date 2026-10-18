"""S6 static half: automation envelopes in shipped Live documents.

Usage: python3 -I s6_documents.py <bundle Contents dir> <Schema dir> <out.json> <inputs.tsv>
Walks Contents for *.als/.alc/.adv/.adg/.agr/.alp (skipping AppleDouble '._*'),
gunzips or reads plain XML, and for every ListAutomation 'Events' list records the
container, event classes, times, values, curve-control attributes and event Ids.
Envelope targets (EnvelopeTarget/PointeeId) are resolved against elements carrying an
Id attribute whose tag is AutomationTarget, ModulationTarget or Pointee. The target's
value kind (Float/Bool/Enum) comes from the schema of the document's MinorVersion:
the classes having that target field whose field set contains the target parent's
child tags. Read-only on inputs; output is data.
"""
import bisect, collections, gzip, hashlib, json, math, multiprocessing, os, re, struct, sys
import xml.etree.ElementTree as ET

EXTS = {".als", ".alc", ".adv", ".adg", ".agr", ".alp"}
APPLEDOUBLE = bytes.fromhex("00051607")
LOW = -63072000.0
CURVE = ("CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y")
TRACKS = {"AudioTrack", "MidiTrack", "GroupTrack", "ReturnTrack", "MainTrack", "MasterTrack", "PreHearTrack"}
CLIPS = {"AudioClip", "MidiClip"}
CAP = 12  # example lists per key


def schema_kinds(path, cache={}):
    """{field tag: [(field set, owner class, field class)]} for fields whose class ends in Target."""
    if path not in cache:
        r = ET.parse(path).getroot()
        out = collections.defaultdict(list)
        for c in r:
            fields = {f.tag: f.get("Class") for f in c}
            for t, k in fields.items():
                if k.endswith("Target"):
                    out[t].append((frozenset(fields), c.tag, k))
        cache[path] = dict(out)
    return cache[path]


def is_target(el):
    """Pointee, or an Id-carrying element whose only children are LockEnvelope (target classes)."""
    if el.get("Id") is None:
        return False
    return el.tag == "Pointee" or (len(el) > 0 and all(c.tag == "LockEnvelope" for c in el))


def kind_of(target, parent, kinds):
    """Target class from the schema: owner classes with this field whose field set equals the
    parent's child tags up to omitted *KeyMidi fields."""
    if target.tag == "Pointee":
        return "Pointee", []
    tags = {c.tag for c in parent}
    cands = sorted({(cls, k) for fs, cls, k in kinds.get(target.tag, [])
                    if tags <= fs and all(m.endswith("KeyMidi") for m in fs - tags)})
    ks = {k for _, k in cands}
    return (ks.pop() if len(ks) == 1 else ("ambiguous" if ks else "unmatched")), [c for c, _ in cands][:6]


def fnum(s):
    return float(s) if s is not None else None


def work(args):
    root_dir, rel, schema_dir = args
    data = open(os.path.join(root_dir, rel), "rb").read()
    out = {"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
           "gzip": data[:2] == b"\x1f\x8b"}
    if not out["gzip"] and not data.startswith(b"<?xml"):
        return out
    root = ET.fromstring(gzip.decompress(data) if out["gzip"] else data)
    out["parsed"] = True
    minor = root.get("MinorVersion", "")
    out["minor"], out["creator"] = minor, root.get("Creator")
    sp = os.path.join(schema_dir, f"{minor}.txt")
    kinds = schema_kinds(sp) if os.path.exists(sp) else {}
    out["schema_used"] = os.path.basename(sp) if kinds else None
    parent = {c: p for p in root.iter() for c in p}

    def anc(el, tags):
        while el in parent:
            el = parent[el]
            if el.tag in tags:
                return el
        return None

    targets, dup = {}, []
    for el in root.iter():
        if is_target(el):
            if el.get("Id") in targets:
                dup.append(el.get("Id"))
            p = parent[el]
            k, cands = kind_of(el, p, kinds)
            man = p.find("Manual")
            rng = [p.find("MidiControllerRange/Min"), p.find("MidiControllerRange/Max")]
            targets[el.get("Id")] = {
                "tag": el.tag, "param": p.tag, "kind": k, "classes": cands, "el": el,
                "manual": None if man is None else man.get("Value"),
                "range": None if None in rng else [r.get("Value") for r in rng],
                "lock": (el.find("LockEnvelope").get("Value") if el.find("LockEnvelope") is not None else None),
                "track": anc(el, TRACKS)}
    out["target_counts"] = dict(collections.Counter(f"{t['tag']}:{t['kind']}" for t in targets.values()))
    out["target_lock"] = dict(collections.Counter(f"{t['tag']}:{t['lock']}" for t in targets.values()))
    out["is_liveset"] = root.find("LiveSet") is not None
    out["target_tags"] = dict(collections.Counter(re.sub(r"\.\d+$", ".N", t["el"].tag) for t in targets.values()))
    out["duplicate_target_ids"] = dup[:CAP]
    out["duplicate_target_id_count"] = len(dup)
    ls = root.find("LiveSet")
    npi = None if ls is None or ls.find("NextPointeeId") is None else int(ls.find("NextPointeeId").get("Value"))
    ids = [int(i) for i in targets]
    out["next_pointee_id"] = npi
    out["max_target_id"] = max(ids) if ids else None

    envs = []
    for ev in root.iter("Events"):
        holder = parent[ev]
        if holder.tag not in ("Automation", "ClipAutomation", "ArrangerAutomation"):
            continue
        owner = parent[holder]
        if owner.tag in ("AutomationEnvelope", "ClipEnvelope", "TakeLane", "ClipTimeable", "Sample"):
            kind = f"{owner.tag}/{holder.tag}"
        else:  # pre-10.0_367 layout: ListAutomation inside the parameter itself
            kind = "legacy-parameter/ArrangerAutomation"
        evs = list(ev)
        rec = {"kind": kind, "n": len(evs), "param": owner.tag if kind.startswith("legacy") else None, "tags": sorted({e.tag for e in evs}),
               "events": [[e.tag, e.get("Id"), e.get("Time"), e.get("Value")] +
                          [e.get(c) for c in CURVE] +
                          [sorted(set(e.attrib) - {"Id", "Time", "Value", *CURVE})] for e in evs]}
        if owner.tag in ("AutomationEnvelope", "ClipEnvelope"):
            pid = owner.find("EnvelopeTarget/PointeeId")
            rec["envelope_id"] = owner.get("Id")
            rec["pointee"] = None if pid is None else pid.get("Value")
            t = targets.get(rec["pointee"])
            if t is None:
                rec["target"] = None
            else:
                rec["target"] = {k: t[k] for k in ("tag", "param", "kind", "classes", "manual", "range", "lock")}
                rec["target"]["same_track"] = (t["track"] is not None and t["track"] is anc(owner, TRACKS))
            if owner.tag == "ClipEnvelope":
                clip = anc(owner, CLIPS)
                loop = None if clip is None else clip.find("Loop")
                g = lambda x: None if loop is None or loop.find(x) is None else loop.find(x).get("Value")
                rec["clip"] = None if clip is None else {
                    "tag": clip.tag, "loop_start": g("LoopStart"), "loop_end": g("LoopEnd"),
                    "start_rel": g("StartRelative"), "loop_on": g("LoopOn"),
                    "current_start": clip.find("CurrentStart").get("Value") if clip.find("CurrentStart") is not None else None,
                    "current_end": clip.find("CurrentEnd").get("Value") if clip.find("CurrentEnd") is not None else None}
            ats = owner.find("Automation/AutomationTransformViewState")
            rec["transform_state"] = None if ats is None else ET.tostring(ats, encoding="unicode").split()[:12]
        envs.append(rec)
    out["envelopes"] = envs
    return out


def bucket(n):
    return str(n) if n <= 3 else "4-10" if n <= 10 else "11-100" if n <= 100 else ">100"


def feq(a, b):
    try:
        return float(a) == float(b) or (a in ("true", "false") and a == b)
    except (TypeError, ValueError):
        return a == b


def summarize(res):
    C = lambda: collections.Counter()
    S = collections.defaultdict(C)
    ex = collections.defaultdict(list)
    minmax = {}

    def note(key, item):
        if len(ex[key]) < CAP:
            ex[key].append(item)

    def mm(key, v):
        lo, hi = minmax.get(key, (v, v))
        minmax[key] = (min(lo, v), max(hi, v))

    per_doc = []
    for r in res:
        if not r.get("parsed"):
            continue
        S["docs_by_minor_creator"][f"{r['minor']}|{r['creator']}"] += 1
        S["schema_used"][str(r["schema_used"])] += 1
        for k, v in r["target_counts"].items():
            S["targets"][k] += v
        for k, v in r["target_lock"].items():
            S["target_lockenvelope"][k] += v
        for k, v in r["target_tags"].items():
            S["target_tags"][k] += v
        S["duplicate_target_ids"][f"liveset={r['is_liveset']}|dups={bool(r['duplicate_target_id_count'])}"] += 1
        if r["duplicate_target_id_count"] and r["is_liveset"]:
            note("duplicate_target_ids", [r["path"], r["duplicate_target_ids"][:4]])
        if r["next_pointee_id"] is not None and r["max_target_id"] is not None:
            S["next_pointee_id_vs_max_target"]["greater" if r["next_pointee_id"] > r["max_target_id"] else "not_greater"] += 1
            if r["next_pointee_id"] <= r["max_target_id"]:
                note("next_pointee_not_greater", [r["path"], r["next_pointee_id"], r["max_target_id"]])
        kinds = collections.Counter(e["kind"] for e in r["envelopes"])
        if r["envelopes"]:
            per_doc.append([r["path"], r["sha256"], r["minor"], dict(kinds), sum(e["n"] for e in r["envelopes"])])
        for e in r["envelopes"]:
            K, evs, loc = e["kind"], e["events"], [r["path"], e.get("envelope_id"), e.get("pointee")]
            S["containers"][K] += 1
            S["containers_by_minor"][f"{K}|{r['minor']}"] += 1
            if e.get("param"):
                S["legacy_params"][e["param"]] += 1
            S["events_by_container_tag"][f"{K}|{','.join(e['tags']) or '-'}"] += e["n"]
            S["event_count_bucket"][f"{K}|{bucket(e['n'])}"] += 1
            if not evs:
                continue
            times = [float(x[2]) for x in evs]
            S["first_time"][f"{K}|{'LOW' if times[0] == LOW else evs[0][2]}"] += 1
            if times[0] != LOW:
                note(f"first_not_low|{K}", loc + [evs[0][2], e["n"]])
            S["low_elsewhere"][K] += sum(1 for t in times[1:] if t == LOW)
            neg = [t for t in times[1:] if t < 0 and t != LOW]
            S["negative_non_low"][K] += len(neg)
            if neg:
                note(f"negative_non_low|{K}", loc + [neg[:3]])
            rest = times[1:] if times[0] == LOW else times
            if rest:
                mm(f"time_min_non_low|{K}", min(rest)); mm(f"time_max|{K}", max(rest))
            dec = sum(1 for a, b in zip(times, times[1:]) if b < a)
            S["sorted"][f"{K}|{'nondecreasing' if not dec else 'decreasing_steps'}"] += 1
            if dec:
                note(f"unsorted|{K}", loc + [dec])
            run, best, pairs = 1, 1, 0
            for a, b in zip(times, times[1:]):
                run = run + 1 if a == b else 1
                pairs += a == b
                best = max(best, run)
            S["equal_time_adjacent_pairs"][K] += pairs
            S["max_events_same_time"][f"{K}|{best}"] += 1
            if pairs:
                vals = [(x[2], x[3]) for x in evs]
                same_val = sum(1 for (ta, va), (tb, vb) in zip(vals, vals[1:]) if ta == tb and feq(va, vb))
                S["equal_time_pairs_same_value"][K] += same_val
            ids = [x[1] for x in evs]
            S["event_id_present"][f"{K}|{all(i is not None for i in ids)}"] += 1
            if all(i is not None for i in ids):
                S["event_id_unique"][f"{K}|{len(set(ids)) == len(ids)}"] += 1
                S["low_event_id"][f"{K}|{ids[0] if times[0] == LOW else 'n/a'}"] += 1
                iv = [int(i) for i in ids]
                S["event_ids_increasing_with_order"][f"{K}|{all(a < b for a, b in zip(iv, iv[1:]))}"] += 1
            for x in evs:
                for a in x[8]:
                    S["other_event_attributes"][f"{x[0]}:{a}"] += 1
                if x[0] == "BoolEvent":
                    S["bool_tokens"][x[3]] += 1
                elif x[0] == "EnumEvent":
                    S["enum_value_is_int"][str(bool(re.fullmatch(r"-?\d+", x[3] or "")))] += 1
            # curves
            for i, x in enumerate(evs):
                cv = x[4:8]
                present = sum(c is not None for c in cv)
                if present == 0:
                    continue
                S["curve_attr_count"][f"{x[0]}|{present}"] += 1
                if present != 4:
                    note("curve_partial", loc + [i])
                    continue
                f = [float(c) for c in cv]
                for name, v in zip(("x1", "y1", "x2", "y2"), f):
                    mm(f"curve_{name}", v)
                S["curve_position"]["on_low_event" if times[i] == LOW else "last_event" if i == len(evs) - 1
                                    else "next_same_time" if times[i + 1] == times[i] else "segment_start"] += 1
                if i + 1 < len(evs):
                    S["curve_next_value_differs"][str(not feq(x[3], evs[i + 1][3]))] += 1
                    if feq(x[3], evs[i + 1][3]):
                        note("curve_flat_segment", loc + [i, x[3]])
                S["curve_x1_le_x2"][str(f[0] <= f[2])] += 1
                S["curve_default_like"][str(f == [0.5, 0.5, 0.5, 0.5])] += 1
            # targets
            if "pointee" in e:
                t = e.get("target")
                if t is None:
                    S["target_resolution"][f"{K}|unresolved"] += 1
                    note(f"unresolved|{K}", loc)
                    continue
                S["target_resolution"][f"{K}|{t['tag']}:{t['kind']}"] += 1
                if all(x[0] == "FloatEvent" for x in evs):
                    for x in evs:
                        mm(f"float_value|{K}|{t['tag']}", float(x[3]))
                elif all(x[0] == "EnumEvent" for x in evs):
                    for x in evs:
                        mm(f"enum_value|{K}|{t['param']}", int(x[3]))
                S["event_tag_vs_target_kind"][f"{K}|{','.join(e['tags'])}|{t['tag']}:{t['kind']}"] += 1
                if K.startswith("AutomationEnvelope"):
                    S["target_same_track"][f"{K}|{t['same_track']}"] += 1
                    if not t["same_track"]:
                        note("target_other_track", loc + [t["param"]])
                if t["kind"] in ("ambiguous", "unmatched"):
                    note(f"target_kind_{t['kind']}", loc + [t["param"], t["classes"]])
                if e["n"] == 1:
                    S["one_event_params"][f"{K}|{t['param']}|{evs[0][0]}"] += 1
                    eq = feq(evs[0][3], t["manual"])
                    S["one_event_value_equals_manual"][f"{K}|{t['tag']}|{eq}"] += 1
                    if not eq:
                        note(f"one_event_ne_manual|{K}", loc + [t["param"], evs[0][3], t["manual"]])
                elif times[0] == LOW:
                    S["multi_event_low_value_equals_manual"][f"{K}|{t['tag']}|{feq(evs[0][3], t['manual'])}"] += 1
                    S["multi_event_low_value_equals_next"][f"{K}|{feq(evs[0][3], evs[1][3])}"] += 1
                if t["range"] and all(x[0] == "FloatEvent" for x in evs):
                    try:
                        lo, hi = sorted(float(v) for v in t["range"])
                    except ValueError:
                        lo = hi = None
                    if lo is not None:
                        out_n = sum(1 for x in evs if not lo <= float(x[3]) <= hi)
                        S["float_values_within_controller_range"][f"{K}|{t['tag']}|{out_n == 0}"] += 1
                        if out_n:
                            note(f"outside_controller_range|{K}", loc + [t["param"], t["range"], out_n])
            if e.get("clip") and times:
                c = e["clip"]
                try:
                    ls_, le_ = float(c["loop_start"]), float(c["loop_end"])
                    st, en = float(c["current_start"]), float(c["current_end"])
                except (TypeError, ValueError):
                    S["clip_time_check"]["no_loop_fields"] += 1
                    continue
                inside = all(ls_ <= t <= le_ for t in rest)
                S["clip_time_check"][f"all_non_low_within_loop:{inside}"] += 1
                if not inside:
                    lo_, hi_ = (min(rest), max(rest)) if rest else (None, None)
                    note("clip_events_outside_loop", loc + [lo_, hi_, ls_, le_, st, en])
            if e.get("transform_state"):
                S["transform_state"][" ".join(e["transform_state"])] += 1
    out = {k: dict(sorted(v.items())) for k, v in S.items()}
    out["minmax"] = {k: list(v) for k, v in sorted(minmax.items())}
    out["examples"] = dict(sorted(ex.items()))
    out["per_document"] = per_doc
    return out


def walk(contents):
    files, skipped = [], collections.Counter()
    for d, _, names in os.walk(contents):
        for n in names:
            ext = os.path.splitext(n)[1].lower()
            if ext not in EXTS:
                continue
            p = os.path.join(d, n)
            if n.startswith("._"):
                with open(p, "rb") as fh:
                    skipped[f"{ext}:{fh.read(4) == APPLEDOUBLE}"] += 1
                continue
            files.append(os.path.relpath(p, contents))
    return sorted(files), skipped


def main():
    contents, schema_dir, out_json, out_tsv = sys.argv[1:5]
    files, skipped = walk(contents)
    with multiprocessing.Pool() as pool:
        res = pool.map(work, [(contents, f, schema_dir) for f in files], chunksize=8)
    with open(out_tsv, "w") as fh:
        for r in res:
            fh.write(f"{r['sha256']}\t{r['bytes']}\t{int(r['gzip'])}\t{int(bool(r.get('parsed')))}\t{r['path']}\n")
    summary = summarize(res)
    summary["inputs"] = {"files": len(res), "parsed": sum(1 for r in res if r.get("parsed")),
                         "appledouble_skipped": dict(skipped),
                         "by_ext": dict(collections.Counter(os.path.splitext(r["path"])[1].lower() for r in res))}
    json.dump(summary, open(out_json, "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
