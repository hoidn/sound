"""Reviewer's checks of the warp-markers-v2 candidate (analyst side; never shipped).

usage: python3 -I -B review_checks.py [--full] [PACKAGE_DIR]   (default: the staging copy)
Independent of build_v2.py, check_v2.py, fixture_checks.py and v2_meta.py: an own restatement of the
released clauses judged on every case, a mutation test, carry and supersession checks against the released
warp-markers-v1, the single change of every fixture and the v1 change it keeps, structure shapes the T11
checker does not evaluate, the WAV rebuilt from its stated parameters, the computed-by-rules inputs against
the X2 run range with alternative operation sequences, and package inventory, hashes, links and a
sanitization scan. The T11 checker itself is run separately (review-checks.txt).
"""
import difflib, hashlib, json, math, re, struct, sys, wave
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PKG = Path(ARGS[0]).resolve() if ARGS else HERE.parents[1] / "warp-markers-v2"
V1 = ROOT / "handoff/warp-markers-v1"
X2 = ROOT / "analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1"
T11 = ROOT / "analysis/ableton-live-12.4.3/r2/t11-structure-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
SLICE = Path("/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64")
XBIN = Path("/var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2")
CLIP = "LiveSet/Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip"
SWP = ("LiveSet/Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/"
       "SampleParts/MultiSamplePart/SampleWarpProperties")
PROV = {"static-derived; not observed reference output": "S", "extracted execution; not observed reference output": "X",
        "computed by extracted-execution rules; not observed reference output": "XS"}
N = 3843840.0
H = 2.6015651015651016e-07
DEFAULT = {"GranularityTones": 30, "GranularityTexture": 65, "FluctuationTexture": 25, "TransientResolution": 6,
           "TransientLoopMode": 2, "ComplexProFormants": 100, "ComplexProEnvelope": 128}
DOMAIN = {"GranularityTones": range(12, 101), "GranularityTexture": range(2, 264), "FluctuationTexture": range(0, 101),
          "ComplexProFormants": range(0, 101), "ComplexProEnvelope": range(8, 257), "WarpMode": {0, 1, 2, 3, 4, 6},
          "TransientResolution": range(0, 7), "TransientLoopMode": range(0, 3)}


COMBINED = {}  # add calls: every failing check, in clause order (the first one decides; REQ-015 preamble)


class Refused(Exception):
    pass


class Excluded(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---- own restatement of the released clauses (spec.md wording) ----
NUM = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def number(t):  # REQ-002 clauses 2 to 4 and the excluded forms
    if t == "Invalid" or t.startswith("#") or t[:1] in "\t\n\r\f\v" and t:
        raise Excluded(f"form {t!r}")
    s = t.lstrip(" ")
    body = s[1:] if s[:1] in "+-" else s
    if body.lower().startswith(("0x", "inf", "nan")) or s[:1] in ("\t", "\n", "\r"):
        raise Excluded(f"form {t!r}")
    m = NUM.match(s)
    if not m:
        raise Refused(f"number text {t!r}")
    v = float(m.group(0))  # CPython float(): nearest binary64, ties to even
    if not -1e6 <= v <= 1e6:
        raise Excluded("value out of scope")
    return v


def code(el, tag):
    if el is None:
        if tag in ("IsWarped", "WarpMode"):
            raise Excluded(f"missing {tag}")
        return DEFAULT[tag]
    if set(el.attrib) - {"Value"}:
        raise Excluded(f"attribute on {tag}")
    t = el.get("Value")
    if t is None:
        if tag in DEFAULT:
            return DEFAULT[tag]
        raise Excluded(f"value-less {tag}")
    if tag == "IsWarped":
        if t not in ("true", "false"):
            raise Excluded("IsWarped text")
        return t == "true"
    if tag == "TransientEnvelope":
        if t != "100":
            raise Excluded("TransientEnvelope other than 100")
        return None
    if not re.fullmatch(r"[0-9]+", t) or int(t) not in DOMAIN[tag]:
        raise Excluded(f"{tag} text or range {t!r}")
    return int(t)


def holder(el, audio):
    tags = [c.tag for c in el]
    if len(tags) != len(set(tags)):
        raise Excluded("repeated child")
    st = {}
    for tag in ("IsWarped", "WarpMode", *DEFAULT, "TransientEnvelope"):
        v = code(el.find(tag), tag)
        if v is not None:
            st[tag] = v
    ms = []
    for m in el.find("WarpMarkers"):
        if m.tag != "WarpMarker" or len(m) or m.text and m.text.strip():
            raise Excluded("marker list content")
        if "SecTime" not in m.attrib or "BeatTime" not in m.attrib or not re.fullmatch(r"[0-9]+", m.get("Id", "")):
            raise Excluded("marker attribute")
        ms.append([number(m.get("SecTime")), number(m.get("BeatTime"))])
    ids = [m.get("Id") for m in el.find("WarpMarkers")]
    if len(ids) != len(set(ids)):
        raise Excluded("repeated marker Id")
    if audio and (len(ms) < 2 or any(a[0] >= b[0] or a[1] >= b[1] for a, b in zip(ms, ms[1:]))):
        raise Excluded("audio list shape")
    st["WarpMarkers"] = ms
    return st


def open_doc(raw):
    root = ET.fromstring(raw)
    if root.tag != "Ableton" or root.attrib != {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                                "SchemaChangeCount": "1"} or root[0].tag != "LiveSet":
        raise Excluded("envelope")
    tracks = list(root.find("LiveSet/Tracks"))
    if not any(t.tag in ("AudioTrack", "MidiTrack", "GroupTrack") for t in tracks):
        raise Excluded("base set changed: no player track")
    for t in tracks:
        if t.tag in ("AudioTrack", "MidiTrack"):
            a = len(t.findall("DeviceChain/MainSequencer/ClipSlotList/ClipSlot"))
            if a != len(t.findall("DeviceChain/FreezeSequencer/ClipSlotList/ClipSlot")):
                raise Excluded("base set changed: freeze slots")
    clips = root.findall(".//AudioClip")
    if len(clips) != 1 or root.find(CLIP) is not clips[0]:
        raise Excluded("clip location")
    st = {"AudioClip": holder(clips[0], True)}
    swps = root.findall(".//SampleWarpProperties")
    if swps:
        if len(swps) != 1 or root.find(SWP) is not swps[0]:
            raise Excluded("sample part location")
        st["SampleWarpProperties"] = holder(swps[0], False)
    return st


def q(b):  # REQ-016 clause 1
    s = 1.0 if b >= 0 else -1.0
    return s * math.floor(abs(b + s * (H * 0.5)) * N) / N


def bounds(nb, p):  # REQ-015 clause 5
    d = p - nb[0]
    a, c = nb[1] + d * (5 / 60), nb[1] + d * (999 / 60)
    return min(a, c), max(a, c)


def seg(cs, x):  # REQ-008: largest k in 0..n-2 with cs[k] <= x, else 0
    return max([k for k in range(len(cs) - 1) if cs[k] <= x], default=0)


def interp(xs, ys, x):
    k = seg(xs, x)
    u = (x - xs[k]) / (xs[k + 1] - xs[k])
    return math.fma(u, ys[k + 1], math.fma(-u, ys[k], ys[k]))


def wav_info(path):
    with wave.open(str(path)) as w:
        return w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth(), w.readframes(w.getnframes())


def call(st, c, rate, length):
    """Returns (outcome dict). Raises Excluded for inputs without expectation."""
    clip, f = st["AudioClip"], c["function"]
    args = [v for k, v in c.items() if k != "function"]
    if any(not math.isfinite(v) or abs(v) >= 1e6 for v in args):
        raise Excluded("argument scope")
    ms = clip["WarpMarkers"]
    secs, beats = [m[0] for m in ms], [m[1] for m in ms]
    if f in ("sample_to_beat_time", "beat_to_sample_time"):
        if not clip["IsWarped"]:
            return {"outcome": "refused", "refusal_reason": "not-warped"}
        if f == "sample_to_beat_time":
            return {"outcome": "accepted", "value": interp(secs, beats, c["sample_frames"] / rate)}
        return {"outcome": "accepted", "value": interp(beats, secs, float(c["beat"])) * rate}
    if f == "add_warp_marker":
        p, qq = float(c["sample_time_seconds"]), float(c["beat"])
        vis = ms[:-1]
        i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
        left = ms[i - 1] if i > 0 else None
        right = vis[i] if i < len(vis) else None
        fails = []
        if not clip["IsWarped"]:
            fails.append("not-warped")
        if p < 0 or p > length:
            fails.append("sample-time-out-of-range")
        if left and qq < left[1]:
            fails.append("beat-below-left-neighbour")
        if right and qq > right[1]:
            fails.append("beat-above-right-neighbour")
        qp = q(qq)
        if any(not (lo <= qp <= hi) for lo, hi in (bounds(n, p) for n in (left, right) if n)):
            fails.append("segment-tempo-out-of-range")
        COMBINED.setdefault("add", {})[json.dumps(c)] = fails
        return {"outcome": "refused", "refusal_reason": fails[0]} if fails else {"outcome": "accepted"}
    qp = q(float(c["beat"]))
    hit = next((k for k, m in enumerate(ms) if m[1] == qp), None)
    if f == "move_warp_marker" and len(ms) < 3:
        raise Excluded("move on fewer than three markers")
    if hit is None:
        return {"outcome": "refused", "refusal_reason": "no-such-marker"}
    if hit == len(ms) - 1:
        return {"outcome": "refused", "refusal_reason": "shadow-marker"}
    if f == "move_warp_marker":
        raise Excluded("accepted move")
    return {"outcome": "accepted"}


def judge(case, pkg=None):
    pkg = pkg or PKG
    exp = case["expected"]
    raw = (pkg / case["input"]).read_bytes()
    rate, frames, ch, width, data = wav_info(pkg / case["sample"])
    try:
        st = open_doc(raw)
    except Refused as e:
        return [] if exp["outcome"] == "refused" and case["action"] == "open" else [f"refused: {e}"]
    if case["action"] == "open":
        errs = [] if exp["outcome"] == "opens" else ["opens"]
        for holder_name, kv in exp.get("state", {}).items():
            for k, v in kv.items():
                got = st[holder_name][k]
                if got != v or type(got) is not type(v) and not (isinstance(v, float) and isinstance(got, float)):
                    errs.append(f"{holder_name}/{k} {got!r} != {v!r}")
        return errs
    got = call(st, case["call"], float(rate), frames / rate)
    errs = []
    if got["outcome"] != exp["outcome"] or got.get("refusal_reason") != exp.get("refusal_reason"):
        errs.append(f"{got} != {exp}")
    if "value" in exp:
        tol = 1e-9 if case["call"]["function"] == "sample_to_beat_time" else 1e-6
        if abs(got["value"] - exp["value"]) > tol:
            errs.append(f"value {got['value']!r} != {exp['value']!r}")
        if repr(got["value"]) != repr(float(exp["value"])):
            errs.append(f"value not bit-identical {got['value']!r} {exp['value']!r}")
    return errs


def mutate(exp):
    e = json.loads(json.dumps(exp))
    if "value" in e:
        e["value"] += 1e-3
    elif e.get("refusal_reason"):
        e["refusal_reason"] = "shadow-marker" if e["refusal_reason"] != "shadow-marker" else "no-such-marker"
    elif e.get("state"):
        h = next(iter(e["state"]))
        k = next(iter(e["state"][h]))
        v = e["state"][h][k]
        e["state"][h][k] = (not v) if isinstance(v, bool) else ([[9.0, 9.0]] + v if isinstance(v, list) else v + 1)
    else:
        e = {"outcome": "refused", "refusal_reason": "not-warped"} if e["outcome"] == "accepted" else \
            ({"outcome": "opens"} if e["outcome"] == "refused" else {"outcome": "refused"})
    return e


# ---- computed-by-rules inputs: run range and alternative operation sequences ----
def q_alts():
    def floor_add_half(b):
        s = 1.0 if b >= 0 else -1.0
        return s * math.floor(abs(b) * N + 0.5) / N

    def recip(b):
        s = 1.0 if b >= 0 else -1.0
        return s * math.floor(abs(b + s * (H * 0.5)) * N) * (1 / N)

    def fused(b):
        s = 1.0 if b >= 0 else -1.0
        return s * math.floor(math.fma(abs(b), N, 0.5)) / N

    def exact(b):
        fr = abs(Fraction(b)) * int(N)
        n = math.floor(fr + Fraction(1, 2))
        return math.copysign(float(Fraction(n, int(N))), b)
    return {"stated": q, "floor(|b|N+0.5)": floor_add_half, "x reciprocal": recip, "fma(|b|,N,0.5)": fused,
            "exact half-away": exact}


def b_alts():
    def bpm_d_over60(nb, p):
        d = p - nb[0]
        a, c = nb[1] + (5 * d) / 60, nb[1] + (999 * d) / 60
        return min(a, c), max(a, c)

    def fused(nb, p):
        d = p - nb[0]
        a, c = math.fma(d, 5 / 60, nb[1]), math.fma(d, 999 / 60, nb[1])
        return min(a, c), max(a, c)

    def exact(nb, p):
        d = Fraction(p) - Fraction(nb[0])
        a, c = float(Fraction(nb[1]) + d * 5 / 60), float(Fraction(nb[1]) + d * 999 / 60)
        return min(a, c), max(a, c)
    return {"stated": bounds, "(B x d)/60": bpm_d_over60, "fma(d,B/60,b)": fused, "exact": exact}


def computed_analysis(cases, xres):
    gq = {float(k): v for k, v in xres["warp_edges_REQ015_016"]["beat_grid_round"].items()}
    names = {"p1.5_nb(1,2)": ((1.0, 2.0), 1.5), "p1_nb(1,2)_ds0": ((1.0, 2.0), 1.0),
             "p1.0004_nb(1,2)": ((1.0, 2.0), 1.0004), "p1.5_right_nb(2,3)": ((2.0, 3.0), 1.5)}
    gb = {names[k]: tuple(v) for k, v in xres["warp_edges_REQ015_016"]["add_bounds_lo_hi"].items()}
    fin = {k: v for k, v in gq.items() if math.isfinite(k) and abs(k) < 1e300}
    qa = {n: f for n, f in q_alts().items() if all(f(k) == v for k, v in fin.items() if k == k)}
    ba = {n: f for n, f in b_alts().items() if all(f(*k) == v for k, v in gb.items())}
    run_q = sorted(abs(k) for k in fin if k)
    run_d = sorted(p - nb[0] for nb, p in gb)
    out = {"q_alternatives_consistent_with_x2": sorted(qa), "q_alternatives_rejected_by_x2": sorted(set(q_alts()) - set(qa)),
           "bounds_alternatives_consistent_with_x2": sorted(ba),
           "bounds_alternatives_rejected_by_x2": sorted(set(b_alts()) - set(ba)),
           "x2_q_magnitudes": [run_q[0], run_q[-1]], "x2_bounds_d": [run_d[0], run_d[-1]], "cases": {}}
    for c in cases:
        if PROV[c["expectation_provenance"]] != "XS":
            continue
        st = open_doc((PKG / c["input"]).read_bytes())
        rate, frames = wav_info(PKG / c["sample"])[:2]
        call_ = c["call"]
        row = {"function": call_["function"]}
        if call_["function"] == "sample_to_beat_time":
            ms = st["AudioClip"]["WarpMarkers"]
            x = call_["sample_frames"] / rate
            k = seg([m[0] for m in ms], x)
            u = (x - ms[k][0]) / (ms[k + 1][0] - ms[k][0])
            us = []
            for name, tab in (("warp_WMK016_M1", [(0.0, 0.0), (1.0, 2.0), (2.0, 3.0), (2.015625, 3.03125)]),
                              ("warp_WMK017_M2", [(0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (2.015625, 3.03125)])):
                for t in xres[name]["sample_to_beat"]:
                    xx = float(t) / 48000
                    kk = seg([m[0] for m in tab], xx)
                    us.append((xx - tab[kk][0]) / (tab[kk + 1][0] - tab[kk][0]))
            row.update({"markers": len(ms), "x2_list_lengths": [4], "segment": k, "u": u,
                        "x2_u_range": [min(us), max(us)], "value_tolerance": 1e-9,
                        "plain_formula": ms[k][1] + u * (ms[k + 1][1] - ms[k][1])})
        else:
            p = call_.get("sample_time_seconds")
            qs = q(float(call_["beat"]))
            row["q_input"] = call_["beat"]
            row["q_in_x2_run"] = float(call_["beat"]) in gq
            row["q_by_alternative"] = {n: f(float(call_["beat"])) for n, f in qa.items()}
            if p is not None:
                ms = st["AudioClip"]["WarpMarkers"]
                vis = ms[:-1]
                i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
                nbs = [n for n in ((ms[i - 1] if i > 0 else None), (vis[i] if i < len(vis) else None)) if n]
                row["bounds"] = [{"neighbour": n, "d": p - n[0], "in_x2_run": (tuple(n), p) in gb,
                                  "by_alternative": {a: f(n, p) for a, f in ba.items()},
                                  "q_minus_nearest_bound_stated": min(abs(qs - b) for b in bounds(n, p))} for n in nbs]
            outcomes = set()
            for qn, qf in qa.items():
                for bn, bf in ba.items():
                    qp = qf(float(call_["beat"]))
                    if p is None:
                        hit = next((k for k, m in enumerate(st["AudioClip"]["WarpMarkers"]) if m[1] == qp), None)
                        outcomes.add("refused" if hit is None or hit == len(st["AudioClip"]["WarpMarkers"]) - 1 else "accepted")
                    else:
                        ok = all(lo <= qp <= hi for lo, hi in (bf(n, p) for n in row and nbs))
                        outcomes.add("accepted" if ok else "refused")
            row["outcome_under_every_consistent_alternative"] = sorted(outcomes)
            row["expected"] = c["expected"]["outcome"]
        out["cases"][c["id"]] = row
    return out


# ---- structure shapes not evaluated by the T11 checker (REQ-LIVE-SET-STRUCTURE-001) ----
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
                    walk(item, item.tag, f"{path}/{c.tag}/{item.tag}")
    walk(ET.fromstring(raw).find("LiveSet"), "LiveSet", "LiveSet")
    return out


def warp_part(raw, v1=False):
    """Canonical (tag, attributes) rows of the clip's REQ-001 children and markers, or of the sample part."""
    root = ET.fromstring(raw)
    el = root.find(".//SampleWarpProperties") if root.find(".//SampleWarpProperties") is not None else root.find(".//AudioClip")
    keep = {"IsWarped", "WarpMode", *DEFAULT, "TransientEnvelope", "WarpMarkers"}
    rows = []
    for c in el:
        if c.tag in keep:
            rows.append((c.tag, tuple(sorted(c.attrib.items()))))
            rows += [(m.tag, tuple(sorted(m.attrib.items()))) for m in c]
    return el.tag, rows


def clip_span(lines, tag):
    start = next(i for i, l in enumerate(lines) if l.strip().startswith(f"<{tag}"))
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == f"</{tag}>")
    return start, end


def changed(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(i1, i2, j1, j2) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]


def wav_bytes():
    data = b"\0\0" * 24000
    fmt = struct.pack("<HHIIHH", 1, 1, 8000, 16000, 2, 16)
    return b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVEfmt " + struct.pack("<I", 16) + fmt + \
        b"data" + struct.pack("<I", len(data)) + data


# ---- package helpers ----
def links(md):
    res = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        path, _, anchor = target.partition("#")
        f = (md.parent / path) if path else md
        ok = not re.match(r"[a-z]+:", target) and f.is_file() and f.resolve().is_relative_to(PKG)
        if ok and anchor and f.suffix == ".md":
            heads = [re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.*)$", f.read_text(), re.M)]
            ok = anchor in heads
        res.append((target, ok))
    return res


DENY = [r"0x[0-9a-fA-F]{5,}", r"\bA[A-Z][a-z]+[A-Z]\w*", r"\bO[A-Z][a-z]+[A-Z]\w*", r"FUN_", r"\bm[A-Z][a-z]+Time",
        r"\b(?:analysis|raw|wiki|research|specs|verification)/", r"/home/", r"/var/", r"\.py\b", r"\bT1[0-9]",
        r"T1\.[0-9]", r"\bPRB-", r"\bQ-0\d\d", r"\bWMK-", r"\bLSS-", r"S-cond", r"LIVE-SET-STRUCTURE",
        r"PLAYBACK-CORE", r"[Pp]seudo", r"[Dd]ecompil", r"[Gg]hidra", r"objdump", r"corpus", r"vtable", r"\bslot \+",
        r"\boffset", r"strtod", r"glibc", r"fmsub", r"fmadd", r"frintm", r"roundsd", r"fcvtzs", r"[Ee]ngine",
        r"[Ww]arper", r"\bX2\b", r"harness", r"dossier", r"\bM[0-2]\b", r"\bW0\b", r"Chuck", r"Patience",
        r"Core Library", r"PlayPos", r"\bADR\b", r"packet", r"\bI(?:[1-9]|10)\b", r"\bF[1-7]\b", r"check_rules",
        r"run_x2", r"make_fixture", r"\bstd::", r"Demo Song"]


def scan(p):
    t = p.read_text()
    return sorted({m for pat in DENY for m in re.findall(pat, t)})


def main():
    rep = {}
    # evidence identity
    v1sha = sha((V1 / "manifest.json").read_bytes())
    row = next(l for l in (ROOT / "handoff/index.md").read_text().splitlines() if l.startswith("| [warp-markers-v1]"))
    m1 = json.loads((V1 / "manifest.json").read_text())
    m2 = json.loads((PKG / "manifest.json").read_text())
    xman = json.loads((X2 / "manifest.json").read_text())
    tman = json.loads((T11 / "manifest.json").read_text())["files"]
    rep["evidence"] = {
        "v1_manifest_sha256": v1sha, "v1_manifest_equals_catalog": f"`{v1sha}`" in row,
        "v1_manifest_equals_superseded_digest": m2["supersession"]["superseded_manifest_sha256"] == v1sha,
        "v1_payload_mismatches": [f["path"] for f in m1["files"] if sha((V1 / f["path"]).read_bytes()) != f["sha256"]],
        "x2_file_mismatches": [f for f, h in xman["files"].items() if sha((X2 / f).read_bytes()) != h],
        "x2_slice_matches": sha(SLICE.read_bytes()) == xman["slice"]["sha256"],
        "x2_loader_binary_matches": sha(XBIN.read_bytes()) == xman["loader"]["built_binary"]["sha256"],
        "t11_checker_mismatches": [f for f in ("schema_check.py", "fixture_audit.py", "make_fixture.py")
                                   if sha((T11 / f).read_bytes()) != tman[f]["sha256"]],
        "schema_sha256": sha(SCHEMA.read_bytes()),
    }
    # carry
    d1 = json.loads((V1 / "cases.json").read_text())["cases"]
    d2 = json.loads((PKG / "cases.json").read_text())
    cases = d2["cases"]
    by_id = {c["id"]: c for c in cases}
    rep["carry"] = {
        "v1_records": len(d1),
        "v1_records_absent": [a["id"] for a in d1 if a["id"] not in by_id],
        "records_differing": [a["id"] for a in d1 if a["id"] in by_id
                              and (a != by_id[a["id"]] or json.dumps(a) != json.dumps(by_id[a["id"]]))],
        "carried_in_v1_order": [c["id"] for c in cases[:37]] == [a["id"] for a in d1 if a["id"] in by_id],
        "ids": [c["id"] for c in cases] == [f"WARP-MARKERS-{n:03d}" for n in range(1, 65) if n != 18],
        "v1_fixture_names_kept": sorted({c["input"] for c in d1 if c["id"] in by_id}) == sorted({c["input"] for c in cases[:37]}),
        "wav_identical_to_v1": (PKG / "fixtures/sample.wav").read_bytes() == (V1 / "fixtures/sample.wav").read_bytes(),
    }
    # expectations
    per, agree, caught, labels = {}, 0, 0, {}
    for c in cases:
        try:
            errs = judge(c)
        except Excluded as e:
            errs = [f"excluded input: {e}"]
        per[c["id"]] = errs or "agrees"
        agree += not errs
        labels[PROV[c["expectation_provenance"]]] = labels.get(PROV[c["expectation_provenance"]], 0) + 1
        m = dict(c, expected=mutate(c["expected"]))
        try:
            caught += bool(judge(m))
        except Excluded:
            caught += 1
    rep["expectations"] = {"cases": len(cases), "agree": agree, "disagree": {k: v for k, v in per.items() if v != "agrees"},
                           "mutations_caught": f"{caught}/{len(cases)}", "labels": labels,
                           "labels_new_cases": {k: [c["id"][-3:] for c in cases[37:] if PROV[c["expectation_provenance"]] == k]
                                                for k in ("X", "XS", "S")},
                           "carried_labels": sorted({PROV[c["expectation_provenance"]] for c in cases[:37]})}
    # contract examples
    base = open_doc((PKG / "fixtures/base.xml").read_bytes())["AudioClip"]["WarpMarkers"]
    xs, ys = [m[0] for m in base], [m[1] for m in base]
    rep["contract_examples"] = {
        "s2b(20000)=4": interp(xs, ys, 20000 / 8000) == 4, "b2s(2.5)=12000": interp(ys, xs, 2.5) * 8000 == 12000,
        "q(2.0000001)=2": q(2.0000001) == 2, "q(2.001)": q(2.001) == 2.0010000416250415,
        "q(halfway)": q(2.0000001300782553) == 2.00000026015651,
        "halfway is nearest to 2+1/2 step": 2.0000001300782553 == float(2 + Fraction(1, 2 * 3843840)),
        "q(one ulp below)": q(2.000000130078255) == 2.00000026015651,
        "one ulp below": math.nextafter(2.0000001300782553, 0) == 2.000000130078255,
        "two ulps below": math.nextafter(math.nextafter(2.0000001300782553, 0), 0) == 2.0000001300782544,
        "one ulp below lies below halfway": Fraction(2.000000130078255) < 2 + Fraction(1, 2 * 3843840),
        "q(two below)=2": q(2.0000001300782544) == 2, "h": 1 / 3843840 == H,
        "bounds p1.5": bounds((1.0, 2.0), 1.5) == (2.0416666666666665, 10.325), "bounds p1": bounds((1.0, 2.0), 1.0) == (2.0, 2.0),
        "tempi 120/60/120": [(b[1] - a[1]) / (b[0] - a[0]) * 60 for a, b in zip(base, base[1:])] == [120, 60, 120],
        "shadow 1/32 beat": base[3][1] - base[2][1] == 1 / 32,
    }
    rep["contract_examples_failing"] = [k for k, v in rep["contract_examples"].items() if not v]
    # computed-by-rules inputs
    xres = json.loads((X2 / "results/envelope-warp.json").read_text(),
                      parse_constant={"NaN": math.nan, "Infinity": math.inf, "-Infinity": -math.inf}.__getitem__)
    rep["computed_by_rules"] = computed_analysis(cases, xres)
    rep["add_calls_with_more_than_one_failing_check"] = {c["id"]: COMBINED["add"][json.dumps(c["call"])] for c in cases
                                                         if "call" in c and len(COMBINED.get("add", {}).get(json.dumps(c["call"]), [])) > 1}
    # fixtures
    schema = load_schema()
    fx = sorted((PKG / "fixtures").glob("*.xml"))
    base_raw = (PKG / "fixtures/base.xml").read_text()
    bl = base_raw.splitlines()
    cs, ce = clip_span(bl, "AudioClip")
    frows = {}
    for p in fx:
        raw = p.read_bytes()
        lines = raw.decode("ascii").splitlines()
        ch = changed(bl, lines)
        span = "clip" if all(cs < i1 and i2 <= ce for i1, i2, *_ in ch) else "other"
        root = ET.fromstring(raw)
        devlists = root.findall(".//Devices")
        ids = [int(e.get("Id")) for e in root.iter() if e.tag in ("AutomationTarget", "ModulationTarget")]
        r = {"form_ok": raw.isascii() and b"\r" not in raw and raw.endswith(b"\n") and b"  <" not in raw,
             "changed_hunks": len(ch), "changed_base_lines": sum(i2 - i1 for i1, i2, *_ in ch),
             "changes_within": span if ch else "none", "lss001_shapes": lss001(schema, raw),
             "device_lists": len(devlists), "devices": sum(len(d) for d in devlists),
             "next_pointee_id": int(root.find("LiveSet/NextPointeeId").get("Value")), "largest_target_id": max(ids)}
        v1p = V1 / "fixtures" / p.name
        if v1p.exists():
            r["v1_warp_part_kept"] = warp_part(v1p.read_bytes()) == warp_part(raw)
        if p.name in ("sectime-no-number.xml", "beattime-empty.xml"):
            r["changed_lines"] = [(bl[i1:i2], lines[j1:j2]) for i1, i2, j1, j2 in ch]
            try:
                open_doc(raw)
                r["own_judge"] = "opens"
            except Refused as e:
                r["own_judge"] = f"refused: {e}"
            reverted = "\n".join(lines[:ch[0][2]] + bl[ch[0][0]:ch[0][1]] + lines[ch[0][3]:]) + "\n"
            r["reverting_the_line_gives_base"] = reverted == base_raw and len(ch) == 1
        frows[p.name] = r
    w = wav_info(PKG / "fixtures/sample.wav")
    rep["fixtures"] = {
        "xml_documents": len(fx), "distinct": len({p.read_bytes() for p in fx}) == len(fx),
        "every_document_used": sorted(p.name for p in fx) == sorted({Path(c["input"]).name for c in cases}),
        "form_ok_all": all(r["form_ok"] for r in frows.values()),
        "change_outside_clip": [k for k, r in frows.items() if r["changes_within"] == "other"],
        "documents_holding_a_device": [k for k, r in frows.items() if r["devices"]],
        "device_lists_per_document": sorted({r["device_lists"] for r in frows.values()}),
        "next_pointee_id_and_largest_target": sorted({(r["next_pointee_id"], r["largest_target_id"]) for r in frows.values()}),
        "lss001_shapes": {k: r["lss001_shapes"] for k, r in frows.items() if r["lss001_shapes"]},
        "v1_warp_part_not_kept": [k for k, r in frows.items() if r.get("v1_warp_part_kept") is False],
        "v1_documents_compared": sum("v1_warp_part_kept" in r for r in frows.values()),
        "wav": {"rate": w[0], "frames": w[1], "channels": w[2], "bytes_per_sample": w[3], "all_zero": not any(w[4]),
                "equals_rebuilt_from_parameters": (PKG / "fixtures/sample.wav").read_bytes() == wav_bytes(),
                "stored_duration_and_rate": [open_doc((PKG / "fixtures/base.xml").read_bytes()) and
                                             ET.fromstring((PKG / "fixtures/base.xml").read_bytes()).find(CLIP + "/SampleRef/DefaultDuration").get("Value"),
                                             ET.fromstring((PKG / "fixtures/base.xml").read_bytes()).find(CLIP + "/SampleRef/DefaultSampleRate").get("Value")]},
        "per_document": frows,
    }
    # package
    files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
    listed = {f["path"]: f for f in m2["files"]}
    rep["package"] = {
        "payload_files": len(files),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (PKG / k).is_file()
                                    or sha((PKG / k).read_bytes()) != f["sha256"] or (PKG / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(PKG)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in PKG.rglob("*") if p.is_symlink()],
        "links": {md.name: len(links(md)) for md in sorted(PKG.glob("*.md"))},
        "unresolved_links": {md.name: [t for t, ok in links(md) if not ok] for md in PKG.glob("*.md")
                             if not all(ok for _, ok in links(md))},
        "missing_case_inputs": sorted({x for c in cases for x in (c["input"], c["sample"]) if not (PKG / x).is_file()}),
        "case_count_matches": m2["case_count"] == len(cases),
        "manifest_sha256": sha((PKG / "manifest.json").read_bytes()),
        "release_status": m2["release_status"], "review_status": m2["review"]["status"],
        "cases_status": d2["status"],
    }
    rep["scan_hits"] = {str(p.relative_to(PKG)): h for p in [*files, PKG / "manifest.json"]
                        if p.suffix not in (".xml", ".wav") and (h := scan(p))}
    rep["scan_hits_fixtures"] = sorted({h for p in files if p.suffix == ".xml" for h in scan(p)})
    if "--full" not in sys.argv:
        rep["fixtures"].pop("per_document")
    print(json.dumps(rep, indent=1, default=str))


if __name__ == "__main__":
    main()
