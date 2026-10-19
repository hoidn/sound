"""Reviewer's checks of the mixer-values-v2 candidate (analyst side; never shipped).

usage: python3 -I -B review_checks.py [PACKAGE_DIR]   (default: the staging copy)   -> JSON on stdout
Independent of build_mv2.py, seal_mv2.py and build_mv1.py: own restatement of the carried clauses (spec.md text) on
the 37 fixtures, exclusion hits, a mutation test of the own judge, carry against the released mixer-values-v1, the
fixture change (value texts equal to v1, element paths added and removed), structure shapes the T11 checker does not
evaluate (REQ-LIVE-SET-STRUCTURE-001), package inventory, hashes, links, fixture form and a sanitization scan.
The T11 checker itself and the X re-run are separate (review-checks.txt, x_sample.py).
"""
import hashlib, json, math, re, struct, sys
import xml.etree.ElementTree as ET
from collections import Counter
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PKG = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[1] / "mixer-values-v2"
V1 = ROOT / "handoff/mixer-values-v1"
V1_CATALOG = "5f6b8401b9324d0cf3d60da47d190e61b93e1935f96995128021f29c9f39cd60"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
getcontext().prec = 60
LN10 = Decimal(10).ln()


class Excluded(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ---- own restatement of the carried clauses ----
NUM = re.compile(r"-?\d+(\.\d+)?\Z")
MIXERS = {"audio": "Tracks/AudioTrack/DeviceChain/Mixer", "midi": "Tracks/MidiTrack/DeviceChain/Mixer",
          "return": "Tracks/ReturnTrack/DeviceChain/Mixer", "main": "MainTrack/DeviceChain/Mixer",
          "cue": "PreHearTrack/DeviceChain/Mixer"}
ORDER = ["Sends", "Speaker", "SoloSink", "PanMode", "Pan", "SplitStereoPanL", "SplitStereoPanR", "Volume",
         "CrossFadeState"]
PANMODE = {0: "Stereo", 1: "Split Stereo"}
XFSTATE = {0: "A", 1: "None", 2: "B"}
CURVES = ["Dipped", "Intermediate", "Constant Power", "Slow Fade", "Slow Cut", "Fast Cut", "Transition"]
VMIN, VMAX = f32(0.0003162277571), f32(1.99526238)


def number(t):
    if not NUM.match(t):
        raise Excluded(f"number text {t!r}")
    return f32(float(t))


def code(t):
    if not re.fullmatch(r"\d+", t):
        raise Excluded(f"code text {t!r}")
    return int(t)


def boolean(t):
    if t not in ("true", "false"):
        raise Excluded(f"Boolean text {t!r}")
    return t == "true"


def db_text(g):  # REQ-006
    exact = Decimal(g).ln() / LN10 * 20
    near = [Decimal("-69.7"), Decimal("0.0005"), Decimal("-0.0005")]
    half = (exact * 1000).to_integral_value(rounding="ROUND_FLOOR") + Decimal("0.5")
    if any(abs(exact - b) <= Decimal("0.00005") for b in near) or abs(exact - half / 1000) <= Decimal("0.00005"):
        raise Excluded(f"gain {g!r} near a text boundary")
    db = f32(f32(math.log10(g)) * 20)
    if db <= -69.7:
        return "-inf dB"
    if round(db * 1000) == 0:
        return "0.0 dB"
    s = str(Decimal(db).quantize(Decimal("0.001"), rounding=ROUND_HALF_EVEN))
    while s.split(".")[1][-1] == "0" and len(s.split(".")[1]) > 1:
        s = s[:-1]
    return s + " dB"


def pan_text(p):  # REQ-007
    if p in (-0.75, -0.25, 0.25, 0.75):
        raise Excluded(f"pan {p} halfway")
    if Fraction(-1, 100) <= Fraction(p) <= Fraction(1, 100):
        return "C"
    n = abs(Fraction(p)) * 50
    return f"{round(n)}{'L' if p < 0 else 'R'}"


def read(raw):
    """Return {key: {value, text|name}} for every value the release describes, and the send counts."""
    ls = ET.fromstring(raw).find("LiveSet")
    out, counts = {}, {}
    for m, path in MIXERS.items():
        mixers = ls.findall(path)
        if len(mixers) != 1:
            raise Excluded(f"{m}: {len(mixers)} mixers")
        mx = mixers[0]
        tags = [c.tag for c in mx if c.tag in ORDER + ["CrossFade"]]
        if tags != ORDER + (["CrossFade"] if m == "main" else []):
            raise Excluded(f"{m}: value elements {tags}")
        if any(c.tag.endswith("KeyMidi") for c in mx.iter()):
            raise Excluded("KeyMidi in mixer")
        holders = mx.findall("Sends/TrackSendHolder")
        counts[m] = len(holders)
        want = 0 if m in ("main", "cue") else 1
        if len(holders) != want:
            raise Excluded(f"{m}: {len(holders)} holders")
        for h in holders:
            if h.get("Id") != "0":
                raise Excluded("holder Id")
            if boolean(h.find("EnabledByUser").get("Value")) != (m != "return"):
                raise Excluded("EnabledByUser")
            if m != "return":
                g = number(h.find("Send/Manual").get("Value"))
                if not VMIN <= g <= 1:
                    raise Excluded("send range")
                out[f"{m}/Send"] = {"value": g, "text": db_text(g)}
        if boolean(mx.find("SoloSink").get("Value")):
            raise Excluded("SoloSink")
        v = number(mx.find("Volume/Manual").get("Value"))
        if not VMIN <= v <= VMAX:
            raise Excluded("volume range")
        out[f"{m}/Volume"] = {"value": v, "text": db_text(v)}
        for k in ("Pan", "SplitStereoPanL", "SplitStereoPanR"):
            p = number(mx.find(f"{k}/Manual").get("Value"))
            if not -1 <= p <= 1:
                raise Excluded("pan range")
            out[f"{m}/{k}"] = {"value": p, "text": pan_text(p)}
        pm = code(mx.find("PanMode").get("Value"))
        if pm not in PANMODE:
            raise Excluded("pan mode")
        out[f"{m}/PanMode"] = {"value": pm, "name": PANMODE[pm]}
        sp = boolean(mx.find("Speaker/Manual").get("Value"))
        out[f"{m}/Speaker"] = {"value": sp, "text": "On" if sp else "Off"}
        xs = code(mx.find("CrossFadeState/Manual").get("Value"))
        if xs not in XFSTATE:
            raise Excluded("crossfade state")
        out[f"{m}/CrossFadeState"] = {"value": xs, "name": XFSTATE[xs]}
        if m == "main":
            c = number(mx.find("CrossFade/Manual").get("Value"))
            if not -1 <= c <= 1:
                raise Excluded("crossfader range")
            out["main/CrossFade"] = {"value": c}
    if len(ls.findall("Tracks/ReturnTrack")) != 1:
        raise Excluded("return tracks")
    cc = code(ls.find("CrossfadeCurve").get("Value"))
    if cc > 6:
        raise Excluded("curve code")
    out["set/CrossfadeCurve"] = {"value": cc, "name": CURVES[cc]}
    return out, counts


def judge(exp, raw):
    vals, counts = read(raw)
    errs = [] if exp["outcome"] == "opens" else ["outcome"]
    for k, e in exp["values"].items():
        got = {f: vals[k][f] for f in e if f in vals[k]}
        if got != e:
            errs.append(f"{k}: {got} != {e}")
    if "send_counts" in exp and {m: counts[m] for m in exp["send_counts"]} != exp["send_counts"]:
        errs.append("send_counts")
    return errs


# ---- fixture change against mixer-values-v1 ----
def paths(raw):
    root = ET.fromstring(raw)
    out = Counter()

    def walk(e, p):
        for c in e:
            q = f"{p}/{c.tag}"
            out[q] += 1
            walk(c, q)
    walk(root, root.tag)
    return out


def value_texts(raw):
    """Every Value attribute under the five mixers and the curve, keyed by track type and path."""
    ls = ET.fromstring(raw).find("LiveSet")
    out = {}
    for m, path in MIXERS.items():
        mx = ls.find(path)
        for k in ORDER + ["CrossFade"]:
            el = mx.find(k)
            if el is None:
                continue
            for e in el.iter():
                if "Value" in e.attrib and e.tag in ("Manual", "EnabledByUser", k):
                    out[f"{m}/{k}/{e.tag}"] = e.get("Value")
    out["set/CrossfadeCurve"] = ls.find("CrossfadeCurve").get("Value")
    return out


# ---- REQ-LIVE-SET-STRUCTURE-001 shapes not evaluated by the T11 checker ----
def load_schema():
    r = ET.parse(SCHEMA).getroot()
    return {c.tag: {f.tag: (f.get("Class"), f.get("Type")) for f in c} for c in r}


def lss001(schema, raw):
    out = []

    def walk(e, cls, path):
        fields = schema.get(cls, {})
        tags = [c.tag for c in e]
        for n in set(tags):
            if tags.count(n) > 1 and n in fields and fields[n][1] != "-1":
                out.append(f"duplicate member {path}/{n}")
        for c in e:
            f = fields.get(c.tag)
            if f is None:
                continue
            fcls, ftype = f
            if ftype == "-4" and "Value" not in c.attrib:
                out.append(f"base value element without Value: {path}/{c.tag}")
            elif ftype == "0":
                walk(c, fcls, f"{path}/{c.tag}")
            elif ftype == "-1":
                for item in c:
                    if c.tag == "Tracks" and item.tag not in ("AudioTrack", "MidiTrack", "GroupTrack", "ReturnTrack"):
                        out.append(f"list item class {item.tag}")
                    walk(item, item.tag, f"{path}/{c.tag}/{item.tag}")
    walk(ET.fromstring(raw).find("LiveSet"), "LiveSet", "LiveSet")
    return out


# ---- package helpers ----
def links(md):
    res = []
    for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        path, _, anchor = target.partition("#")
        f = (md.parent / path) if path else md
        ok = f.is_file() and f.resolve().is_relative_to(PKG)
        if ok and anchor and f.suffix == ".md":
            heads = [re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.*)$", f.read_text(), re.M)]
            ok = anchor in heads
        res.append((target, ok))
    return res


DENY = [r"0x[0-9a-fA-F]{4,}", r"\b[A-Z][a-z]+[A-Z]\w*\(", r"\bO[A-Z][a-z]+[A-Z]\w*", r"\bA[A-Z][a-z]+[A-Z]\w*",
        r"\b(?:analysis|raw|wiki|research|specs|verification)/", r"/home/", r"/var/tmp", r"/tmp/", r"\.py\b",
        r"T11", r"T1\.1", r"LSS-", r"PRB-", r"\bQ-0\d\d", r"\bMV-\d", r"\bMG-\d", r"\bI\d+\b", r"\bF\d\b",
        r"LIVE-SET-STRUCTURE", r"MIX-GRAPH", r"S-cond", r"\baudit", r"\bwalk", r"pseudo", r"decompil", r"[Gg]hidra",
        r"objdump", r"corpus", r"vtable", r"offset", r"exp10f", r"cosf", r"fmadd", r"fnmsub", r"\bfma\b", r"xexec",
        r"harness", r"slice", r"NormalDip", r"SlightDip", r"Dipless", r"ConstantPower", r"FastCut", r"SlowCut",
        r"CrossfadeToLevel", r"PanModeAmount", r"StereoSplitPan", r"OnVolume", r"Ramp\w*", r"registry", r"builder",
        r"0\.95", r"129", r"loader", r"MIN\b", r"skeleton", r"probe", r"packet", r"\bX2\b", r"\bADR", r"mpmath"]


def scan(p):
    t = p.read_text()
    return sorted({m for pat in DENY for m in re.findall(pat, t)})


def main():
    rep = {"package": str(PKG)}
    cases = json.loads((PKG / "cases.json").read_text())["cases"]
    v1cases = json.loads((V1 / "cases.json").read_text())["cases"]
    opens = [c for c in cases if c["action"] == "open"]
    # carried clauses
    agree, excluded, missed = [], {}, []
    for c in opens:
        raw = (PKG / c["input"]).read_bytes()
        try:
            errs = judge(c["expected"], raw)
        except Excluded as e:
            excluded[c["id"]] = str(e)
            continue
        if errs:
            rep.setdefault("disagreements", {})[c["id"]] = errs
        else:
            agree.append(c["id"])
        for k, e in c["expected"]["values"].items():  # mutation of each listed field
            for f in e:
                m = json.loads(json.dumps(c["expected"]))
                v = m["values"][k][f]
                m["values"][k][f] = (v + "x" if isinstance(v, str) else (not v) if isinstance(v, bool)
                                     else v + 1 if isinstance(v, int) else struct.unpack("<f", struct.pack(
                                         "<i", struct.unpack("<i", struct.pack("<f", v))[0] + 1))[0])
                if not judge(m, raw):
                    missed.append(f"{c['id']} {k} {f}")
    rep["open_cases_agree"] = len(agree)
    rep["open_cases_excluded"] = excluded
    rep["mutations_missed"] = missed
    rep["db_examples"] = {g: db_text(f32(float(g))) for g in ("1", "0.5011872053", "0.5", "0.25", "0.30725",
                          "0.7367056608", "1.5", "1.99526238", "0.99999", "0.0003311311302", "0.0003235936455",
                          "0.0003162277571")}
    rep["pan_examples"] = {p: pan_text(f32(float(p))) for p in ("-1", "-0.6", "-0.5", "0.2", "0.5", "1",
                           "0.004999999888", "0.01", "0.0101", "-0.0101", "0.33")}
    # carry
    rep["carried_records_equal_v1"] = sum(a == b for a, b in zip(cases[:37], v1cases))
    rep["carried_records_serialized_equal_v1"] = sum(json.dumps(a) == json.dumps(b) for a, b in zip(cases[:37], v1cases))
    rep["v1_case_count"] = len(v1cases)
    # fixture change
    v1fx = {c["id"]: (V1 / c["input"]).read_bytes() for c in v1cases}
    rep["value_texts_equal_v1"] = sum(value_texts((PKG / c["input"]).read_bytes()) == value_texts(v1fx[c["id"]])
                                      for c in opens)
    p1, p2 = paths(v1fx["MIXER-VALUES-001"]), paths((PKG / "fixtures/MIXER-VALUES-001.xml").read_bytes())
    rep["paths_removed_from_v1"] = sorted(set(p1) - set(p2))
    added = sorted(set(p2) - set(p1))
    rep["paths_added_count"] = len(added)
    rep["paths_added_top"] = sorted({re.sub(r"^(Ableton/LiveSet/(?:Tracks/\w+|\w+)(?:/DeviceChain(?:/Mixer)?)?(?:/\w+)?).*",
                                            r"\1", a) for a in added})
    rep["paths_count_changed"] = {k: [p1[k], p2[k]] for k in set(p1) & set(p2) if p1[k] != p2[k]}
    rep["fixtures_with_v1_paths_missing_or_recounted"] = [
        c["id"] for c in opens if (lambda a, b: bool(set(a) - set(b)) or any(a[k] != b[k] for k in a))(
            paths(v1fx[c["id"]]), paths((PKG / c["input"]).read_bytes()))]
    fx2 = [ET.fromstring((PKG / c["input"]).read_bytes()).find("LiveSet") for c in opens]
    rep["prehear_children"] = sorted({c.tag for ls in fx2 for c in ls.find("PreHearTrack")})
    rep["track_order_and_ids"] = sorted({tuple((t.tag, t.get("Id")) for t in ls.find("Tracks")) for ls in fx2})
    # every fixture equals fixture 001 outside the value texts (template set)
    base = (PKG / "fixtures/MIXER-VALUES-001.xml").read_text().split("\n")
    diff_lines = {}
    for c in opens:
        lines = (PKG / c["input"]).read_text().split("\n")
        d = [b.strip() + " -> " + a.strip() for a, b in zip(lines, base) if a != b]
        diff_lines[c["id"]] = d if len(lines) == len(base) else ["line count differs"]
    rep["lines_differing_from_001"] = {k: v for k, v in diff_lines.items() if len(v) > 3 or any(
        "Manual" not in x and "PanMode" not in x and "SoloSink" not in x and "CrossfadeCurve" not in x for x in v)}
    rep["max_lines_differing_from_001"] = max(len(v) for v in diff_lines.values())
    # structure shapes
    schema = load_schema()
    rep["lss001_hits"] = {c["id"]: h for c in opens if (h := lss001(schema, (PKG / c["input"]).read_bytes()))}
    # fixture form
    raws = [(PKG / c["input"]).read_bytes() for c in opens]
    rep["fixtures_form_ok"] = sum(r.isascii() and b"\r" not in r and r.endswith(b"\n") for r in raws)
    rep["fixtures_distinct"] = len(set(raws))
    rep["fixture_bytes_range"] = [min(map(len, raws)), max(map(len, raws))]
    # package
    man = json.loads((PKG / "manifest.json").read_text())
    files = sorted(str(p.relative_to(PKG)) for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
    rep["payload_files"] = len(files)
    rep["inventory_differences"] = sorted(set(files) ^ {f["path"] for f in man["files"]})
    rep["hash_or_size_mismatches"] = [f["path"] for f in man["files"] if not (PKG / f["path"]).is_file() or
                                      sha((PKG / f["path"]).read_bytes()) != f["sha256"] or
                                      (PKG / f["path"]).stat().st_size != f["bytes"]]
    rep["symlinks"] = [str(p) for p in PKG.rglob("*") if p.is_symlink()]
    rep["links"] = {p.name: len(links(p)) for p in PKG.glob("*.md")}
    rep["unresolved_links"] = {p.name: [t for t, ok in links(p) if not ok] for p in PKG.glob("*.md")
                               if any(not ok for _, ok in links(p))}
    rep["missing_inputs"] = [c["input"] for c in cases if c["input"] and not (PKG / c["input"]).is_file()]
    rep["unused_fixtures"] = sorted(set(f for f in files if f.startswith("fixtures/")) - {c["input"] for c in cases})
    rep["manifest_sha256"] = sha((PKG / "manifest.json").read_bytes())
    rep["case_count"] = [len(cases), man["case_count"]]
    # supersession
    v1m = json.loads((V1 / "manifest.json").read_text())
    rep["v1_manifest_sha256_is_catalog"] = sha((V1 / "manifest.json").read_bytes()) == V1_CATALOG == \
        man["supersession"]["superseded_manifest_sha256"]
    rep["v1_file_mismatches"] = [f["path"] for f in v1m["files"] if sha((V1 / f["path"]).read_bytes()) != f["sha256"]]
    per = man["supersession"]["fixture_changes"]["per_fixture"]
    rep["per_fixture_v1_digest_mismatches"] = [k for k, v in per.items()
                                               if sha((V1 / k).read_bytes()) != v["mixer_values_v1_sha256"]]
    rep["per_fixture_entries"] = len(per)
    # sanitization
    rep["scan"] = {str(p.relative_to(PKG)): h for p in sorted(PKG.rglob("*")) if p.is_file() and p.suffix in
                   (".md", ".json") and (h := scan(p))}
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
