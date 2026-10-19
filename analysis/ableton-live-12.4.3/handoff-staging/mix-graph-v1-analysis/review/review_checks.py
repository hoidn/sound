"""Reviewer's checks of the mix-graph-v1 candidate (analyst side; never shipped).

usage: python3 -I -B review_checks.py [PACKAGE_DIR]   (default: the staging copy)
Independent of build_mg1.py: own restatement of the released clauses (spec.md wording) evaluated on every
case, a frame-by-frame render of every render case from the fixture's mixer values and the shipped signals,
a cross-check of the X inputs against the retained result files, the volume-curve round trip for the two
silence-limit fixtures (SPEC-MIXER-VALUES REQ-005 construction), REQ-LIVE-SET-STRUCTURE-001 shapes the T11
checker does not evaluate, the WAV chunk layout, package inventory, hashes, links, fixture form and a
sanitization scan. The T11 checker itself is run separately (see review-checks.txt).
"""
import hashlib, json, math, re, struct, sys, wave
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVID = HERE.parents[2]
PKG = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[1] / "mix-graph-v1"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
MIX = json.loads((EVID / "r2/t14-mix-v1/results/mix.json").read_text())
MIXER = json.loads((EVID / "r2/x2-mixer-v1/results/mixer.json").read_text())


class Excluded(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


MIN, VMAX, LIMIT = f32(0.0003162277571), f32(1.99526238), f32(0.00032)
assert abs(LIMIT - 0.0003199999919) < 1e-13  # binary32 0x39a7c5ac


# ---- own restatement (spec.md) ----
def pan_law(w, p, sl, sr, v):  # REQ-004
    th = lambda u: (u + 1) * math.pi / 4  # noqa: E731
    return [f32(x) for x in (v * (w * math.cos(th(sl)) + (1 - w) * max(1e-5, math.sqrt(2) * math.cos(th(p)))),
                             v * w * math.sin(th(sl)), v * w * math.cos(th(sr)),
                             v * (w * math.sin(th(sr)) + (1 - w) * max(1e-5, math.sqrt(2) * math.sin(th(p)))))]


def send_matrix(g, e, a, q, P):  # REQ-005
    I = (1.0, 0.0, 0.0, 1.0)
    return [f32(g * e * a * (q * p + (1 - q) * i)) for p, i in zip(P, I)]


GATES = {"unaffected": lambda s: (s, s), "following": lambda s: (s, s), "cue": lambda s: (s, s),
         "soloed": lambda s: (1, 1), "muted": lambda s: (0, 0), "indirectly-muted": lambda s: (s, 0),
         "return-solo-muted": lambda s: (0, s)}  # REQ-007, 008 table


def ramp_values(start, target, n, advances):  # REQ-009, binary32 step and accumulation
    d = f32((target - start) / n)
    if abs(d) < 1e-12:
        return [target] * advances
    out, cur = [], f32(start)
    for k in range(1, advances + 1):
        cur = target if k >= n else f32(cur + d)
        out.append(cur)
    return out


def ramp_start(start, target, n):  # REQ-009
    v = target if n == 0 or abs((target - start) / n) < 1e-12 else start
    return 0.0 if abs(v) < 1e-12 else v


def pan_ramp(initial, changes):  # REQ-004, REQ-009: targets at the end of the shortest running ramp
    names = ["split_amount", "pan", "split_l", "split_r", "volume_gain"]
    st = {k: [initial[k], 0.0, 0] for k in names}  # value, slope, remaining
    now, out = 0, []
    for ch in changes:
        dt = ch["sample"] - now
        for s in st.values():
            k = min(dt, s[2])
            s[0] += k * s[1]
            s[2] -= k
        now = ch["sample"]
        s = st[ch["input"]]
        s[1], s[2] = (ch["target"] - s[0]) / ch["length"], ch["length"]
        L = min(x[2] for x in st.values() if x[2] > 0)
        at = {k: x[0] + min(L, x[2]) * x[1] for k, x in st.items()}
        out.append({"matrix_target": pan_law(at["split_amount"], at["pan"], at["split_l"], at["split_r"],
                                              at["volume_gain"]), "length": L})
    return out


def bezier_points(a, b, c):  # REQ-013 polyline
    (ta, va), (tb, vb) = a, b
    dt, dv = tb - ta, vb - va
    P = [(ta, va), (ta + c[0] * dt, va + c[1] * dv), (ta + c[2] * dt, va + c[3] * dv), (tb, vb)]
    pts = []
    for i in range(1, 16):
        s = i / 16
        w = [(1 - s) ** 3, 3 * s * (1 - s) ** 2, 3 * s * s * (1 - s), s ** 3]
        pts.append([sum(wi * p[0] for wi, p in zip(w, P)), f32(sum(wi * p[1] for wi, p in zip(w, P)))])
    return pts


def point_list(events):
    pts = []
    for i, e in enumerate(events):
        t = -1e7 if i == 0 else float(e[0])
        pts.append((t, e[1]))
        if len(e) == 3 and any(x != 0.5 for x in e[2]) and i + 1 < len(events):
            pts += [tuple(p) for p in bezier_points((t, e[1]), (events[i + 1][0], events[i + 1][1]), e[2])]
    return pts


def grid(t):
    return math.copysign(math.floor(abs(t) * 3843840 + 0.5), t) / 3843840


def current(pts, t):
    idx = [i for i, p in enumerate(pts) if p[0] <= grid(t)]
    return idx[-1]


def playback_value(events, spb, t):  # REQ-013 Float value
    pts = point_list(events)
    i = current(pts, t)
    if i == len(pts) - 1:
        return pts[i][1]
    (ta, va), (tb, vb) = pts[i], pts[i + 1]
    if va == vb:
        return va
    slope = f32(vb - va) / ((tb - ta) * spb)
    v = va + max(0.0, (grid(t) - ta) * spb) * slope
    return min(max(v, min(va, vb)), max(va, vb))


def discrete_value(events, t):  # REQ-013 Bool and Enum
    return point_list(events)[current(point_list(events), t)][1]


def ramp_length(q, seg, spb, transport):  # REQ-014
    ta, va, tb, vb = seg
    s = f32(vb - va) / ((tb - ta) * spb)
    if s == 0 or transport != "playing":
        return 0
    r = q / abs(s)
    if r >= 2 ** 31:
        raise Excluded("r >= 2^31")
    return max(200, min(65536, math.trunc(r)))


def compute(comp, a):
    if comp == "send-matrix":
        return {"matrix": send_matrix(a["gain"], a["send_gate"], a["active"], a["post"], a["pan_matrix"])}
    if comp == "main-matrix":
        return {"matrix": [f32(a["main_gate"] * p) for p in a["pan_matrix"]]}
    if comp == "gates":
        m, e = GATES[a["solo_category"]](int(a["track_switch"]))
        return {"main_gate": m, "send_gate": e}
    if comp == "fade-length":
        return {"samples": 75}
    if comp == "ramp-advance":
        return {"values": ramp_values(a["start"], a["target"], a["length"], a["advances"])}
    if comp == "ramp-start":
        return {"value": ramp_start(a["start"], a["target"], a["length"])}
    if comp == "pan-ramp":
        return {"after_changes": pan_ramp(a["initial"], a["changes"])}
    if comp == "polyline":
        return {"points": bezier_points(a["start"], a["end"], a["controls"])}
    if comp == "playback-value":
        return {"values": [playback_value(a["events"], a["samples_per_beat"], t) for t in a["times"]]}
    if comp == "discrete-value":
        return {"values": [discrete_value(a["events"], t) for t in a["times"]]}
    if comp == "ramp-length":
        return {"length": ramp_length(a["step"], a["segment"], a["samples_per_beat"], a["transport"])}
    raise KeyError(comp)


def close(a, b, tol):
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str):
        return a == b
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    return abs(a - b) <= tol


# ---- volume curve (SPEC-MIXER-VALUES REQ-005 construction, float32) ----
def table(top):
    E = [f32(top)]
    for _ in range(60):
        E.append(f32(E[-1] - f32(0.4)))
    s = f32(0.4)
    for _ in range(61, 97):
        s = f32(s + f32(0.04))
        E.append(f32(E[-1] - s))
    a = f32(s + f32(0.04))
    E.append(f32(E[-1] - a))
    b = f32((3 * a + (-70.0 - E[97])) / 6)
    E.append(f32(E[97] - f32(a - b)))
    E.append(f32(E[98] + f32(b - f32(a - b))))
    E.append(-70.0)
    D = [0.0 if abs(x) < 1e-4 else x for x in E[::-1]]
    return [f32(10 ** f32(d * f32(0.05))) for d in D]


G1 = table(6.0)


def to_pos(g):
    if g <= G1[0]:
        return 0.0
    if g >= G1[100]:
        return 1.0
    k = max(i for i in range(100) if G1[i] <= g)
    return f32((k + (g - G1[k]) / (G1[k + 1] - G1[k])) / 100)


def to_gain(p):
    if p <= 0:
        return G1[0]
    if p >= 1:
        return G1[100]
    k = math.floor(100 * p)
    f = 100 * p - k
    f = 0.0 if f <= 2 ** -17 else (1.0 if f >= 1 - 2 ** -17 else f)
    return f32(f * G1[k + 1] + (1 - f) * G1[k]) if k < 100 else G1[100]


# ---- render ----
def num(el):
    return f32(float(el.get("Value")))


def mixer_of(t):
    return t.find("DeviceChain/Mixer")


def read_set(xml):
    root = ET.fromstring(xml)
    ls = root.find("LiveSet")
    tracks = {t.find("Name/EffectiveName").get("Value"): t for t in ls.find("Tracks")}
    tracks["M"] = ls.find("MainTrack")
    if sorted(t.tag for t in ls.find("Tracks")) != ["AudioTrack", "AudioTrack", "ReturnTrack"]:
        raise Excluded("track list")
    sp = ls.findall("SendsPre/SendPreBool")
    if len(sp) != 1:
        raise Excluded("SendsPre")
    vals = {}
    for k, t in tracks.items():
        mx = mixer_of(t)
        if mx.find("SoloSink").get("Value") != "false":
            raise Excluded("solo")
        if mx.find("CrossFadeState/Manual").get("Value") != "1":
            raise Excluded("crossfade assignment")
        v = {"vol": num(mx.find("Volume/Manual")), "pan": num(mx.find("Pan/Manual")),
             "sl": num(mx.find("SplitStereoPanL/Manual")), "sr": num(mx.find("SplitStereoPanR/Manual")),
             "mode": int(mx.find("PanMode").get("Value")), "on": mx.find("Speaker/Manual").get("Value") == "true"}
        if not MIN <= v["vol"] <= VMAX or any(not -1 <= v[x] <= 1 for x in ("pan", "sl", "sr")) or v["mode"] not in (0, 1):
            raise Excluded("value domain")
        holders = mx.findall("Sends/TrackSendHolder")
        if k == "M":
            if holders or not v["on"]:
                raise Excluded("main track")
        else:
            if len(holders) != 1:
                raise Excluded("holders")
            v["send"] = num(holders[0].find("Send/Manual"))
            v["enabled"] = holders[0].find("EnabledByUser").get("Value") == "true"
            if not MIN <= v["send"] <= 1:
                raise Excluded("send domain")
            if t.find("DeviceChain/AudioOutputRouting/Target").get("Value") != "AudioOut/Main":
                raise Excluded("output")
            if list(t.find("DeviceChain/DeviceChain/Devices")):
                raise Excluded("device")
            if t.findall(".//AudioClip") or t.findall(".//MidiClip") or list(t.find("AutomationEnvelopes/Envelopes")):
                raise Excluded("clip or envelope")
        vals[k] = v
    # main track: only the one-event tempo and time-signature envelopes, each equal to its Manual
    mx = mixer_of(tracks["M"])
    ids = {mx.find("Tempo/AutomationTarget").get("Id"): mx.find("Tempo/Manual").get("Value"),
           mx.find("TimeSignature/AutomationTarget").get("Id"): mx.find("TimeSignature/Manual").get("Value")}
    for env in tracks["M"].findall("AutomationEnvelopes/Envelopes/AutomationEnvelope"):
        ev = list(env.find("Automation/Events"))
        if env.find("EnvelopeTarget/PointeeId").get("Value") not in ids or len(ev) != 1 \
                or ev[0].get("Value") != ids[env.find("EnvelopeTarget/PointeeId").get("Value")]:
            raise Excluded("main envelope")
    return vals


def volume_gain(g):
    v = to_gain(to_pos(g))
    return 0.0 if v <= LIMIT else v


def coefficients(vals):
    """{output channel: {input channel: coefficient}} from the rules, with each send checked."""
    main = vals["M"]
    PM = pan_law(main["mode"], main["pan"], main["sl"], main["sr"], volume_gain(main["vol"]))
    out = {"L": {}, "R": {}}
    r_plays = vals["R"]["on"]
    for k in ("A", "B", "R"):
        v = vals[k]
        s = 1 if v["on"] else 0
        if v["send"] != MIN and s == 1 and (k == "R" or r_plays):
            raise Excluded(f"send of {k} above its minimum reaches the main track")
        if k == "R":
            continue  # R's input is zero (sends at the minimum) or R's main gate is 0
        P = [s * x for x in pan_law(v["mode"], v["pan"], v["sl"], v["sr"], volume_gain(v["vol"]))]
        # main track matrix PM applied after the track's matrix P (main gate 1)
        ll = PM[0] * P[0] + PM[2] * P[1]
        lr = PM[1] * P[0] + PM[3] * P[1]
        rl = PM[0] * P[2] + PM[2] * P[3]
        rr = PM[1] * P[2] + PM[3] * P[3]
        for ch, inp, c in (("L", "L", ll), ("R", "L", lr), ("L", "R", rl), ("R", "R", rr)):
            if abs(c) > 1e-12:
                out[ch][f"{k}.{inp}"] = c
    return out


def wav(path):
    b = path.read_bytes()
    assert b[:4] == b"RIFF" and b[8:12] == b"WAVE" and struct.unpack("<I", b[4:8])[0] == len(b) - 8
    chunks, i = [], 12
    while i < len(b):
        cid, n = b[i:i + 4], struct.unpack("<I", b[i + 4:i + 8])[0]
        chunks.append(cid.decode())
        i += 8 + n + (n & 1)
    with wave.open(str(path), "rb") as w:
        params = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes(), w.getcomptype())
        frames = [(a / 32768, c / 32768) for a, c in struct.iter_unpack("<hh", w.readframes(w.getnframes()))]
    return chunks, params, frames


SIG_FORMULA = {"x-a.wav": lambda n: (1024 * ((n % 32) - 16), 2048 * abs((n % 16) - 8) - 8192),
               "x-b.wav": lambda n: (12000 if n % 8 < 4 else -12000, 512 * ((5 * n) % 64 - 32))}


def render_check(case, xml):
    vals = read_set(xml)
    sigs = set(case["render"]["signals"])  # a track without a signal has no input
    mine = {ch: {k: c for k, c in d.items() if k.split(".")[0] in sigs} for ch, d in coefficients(vals).items()}
    exp = case["expected"]["main"]
    coef_ok = all(set(mine[c]) == set(exp[c]) and all(abs(mine[c][k] - exp[c][k]) <= 1e-7 * max(1, abs(exp[c][k]))
                                                     for k in exp[c]) for c in ("L", "R"))
    sig = {k: wav(PKG / p)[2] for k, p in case["render"]["signals"].items()}
    X = max(abs(s) for fr in sig.values() for f in fr for s in f)
    worst = 0.0
    for n in range(case["render"]["frames"]):
        for ch in ("L", "R"):
            y = f32(sum(f32(c * sig[k.split(".")[0]][n][0 if k.endswith(".L") else 1]) for k, c in mine[ch].items()))
            ref = sum(c * sig[k.split(".")[0]][n][0 if k.endswith(".L") else 1] for k, c in exp[ch].items())
            worst = max(worst, abs(y - ref))
    return {"coefficients_agree": coef_ok, "X": X, "worst_abs_error": worst,
            "within_comparator": worst <= case["tolerance_factor"] * X, "mine": mine}


# ---- REQ-LIVE-SET-STRUCTURE-001 shapes the T11 checker does not evaluate ----
def schema():
    r = ET.parse(SCHEMA).getroot()
    return {c.tag: {f.tag: (f.get("Class"), f.get("Type")) for f in c} for c in r}


def lss001(sch, root):
    out = []

    def walk(e, cls):
        fields = sch.get(cls, {})
        names = [c.tag for c in e]
        for n in set(names):
            f = fields.get(n)
            if f and f[1] == "0" and names.count(n) > 1:
                out.append(f"repeated compound {cls}/{n}")
        for c in e:
            f = fields.get(c.tag)
            if f is None:
                continue
            fc, ft = f
            if ft == "-4" and "Value" not in c.attrib:
                out.append(f"base value without Value {cls}/{c.tag}")
            elif ft == "0":
                walk(c, fc)
            elif ft == "-1":
                for item in c:
                    if item.tag not in sch:
                        out.append(f"list item of unknown class {cls}/{c.tag}/{item.tag}")
                    else:
                        walk(item, item.tag)

    walk(root.find("LiveSet"), "LiveSet")
    return out


DENY = [r"analysis/", r"wiki/", r"raw/", r"\.\./", r"0x[0-9a-fA-F]{3,}", r"FUN_", r"DAT_", r"decompil", r"disassem",
        r"pseudocode", r"Ghidra", r"objdump", r"vtable", r"typeinfo", r"corpus", r"harness", r"xexec", r"glibc",
        r"\bPRB-", r"\bQ-0\d\d", r"\bMG-0", r"\bMV-0", r"\bAEN-", r"\bA[1-8]\b", r"\bE(?:1|4|9|12|13)\b", r"\bB0\b",
        r"T11", r"T1\.\d", r"\bF[1-7]\b", r"x2-", r"t14", r"MainOn", r"SendsOn", r"PrehearOn", r"SoloPrehear",
        r"SendIsPost", r"PanModeAmount", r"GroupOn", r"mpActive", r"\bmp[A-Z]\w+", r"\bTSend", r"TVolume", r"ORamp",
        r"OTrack", r"OFloat", r"OAuto", r"OAsync", r"OMake", r"OCross", r"OConvert", r"AConvert", r"ALevel",
        r"ATrack", r"AMain", r"ATimeable", r"SControl", r"SAudio", r"SetRamp", r"GetRamp", r"Extrapolat", r"\bSIs",
        r"STrackFade", r"CalcStep", r"SegmentUpdate", r"MinSegment", r"cvtt", r"Following Solo", r"Player Solo",
        r"Prehear", r"Pre-hear", r"Timeable", r"Remoteable", r"\+0x", r"Live\.arm64", r"/home/", r"/var/", r"/tmp/",
        r"Recording Audio", r"\bslot \d", r"Python", r"\bpc\b", r"✓", r"bitset", r"jump table", r"switch word"]
ALLOWED = {"AGENTS.md": {"decompil"}}


def links(md):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text()):
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md
        ok = not re.match(r"[a-z]+:", target) and dest.is_file() and PKG in dest.parents
        if ok and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok = anchor in slugs
        out.append((target, ok))
    return out


def main():
    cases_doc = json.loads((PKG / "cases.json").read_text())
    cases = cases_doc["cases"]
    report = {"package": str(PKG), "cases": len(cases), "computation": {}, "render": {}}
    # X inputs and expectations against the retained result files
    xcheck = {
        "pan -1 stereo": [p for p in MIXER["pan_law"] if p["w"] == 0 and p["pan"] == -1 and p["vol"] == 1][0]["gains_LL_LR_RL_RR"]
        == pan_law(0, -1, -1, 1, 1),
        "split (0, 0)": [p for p in MIXER["pan_law"] if p["w"] == 1 and p.get("splitL") == 0][0]["gains_LL_LR_RL_RR"]
        == pan_law(1, 0, 0, 0, 1),
        "pan 0 stereo identity": pan_law(0, 0, -1, 1, 1) == [1.0, 0.0, 0.0, 1.0],
        "round trip exact (X) for min, -6 dB, 0 dB, max": all(r["exact_roundtrip"] for r in MIXER["fader"]["roundtrip_Q019"]
                                                            if r["curve"] == "volume"),
        "own approximate table (REQ-005 construction): round trip per X value (informational)": {
            str(r["stored_gain"]): [to_pos(r["stored_gain"]), r["position_x"], to_gain(to_pos(r["stored_gain"])), r["gain_back_x"]]
            for r in MIXER["fader"]["roundtrip_Q019"] if r["curve"] == "volume"},
        "send at the exact minimum has send-curve position 0 (X)": [r for r in MIXER["fader"]["roundtrip_Q019"]
                                                                   if r["curve"] == "send" and r["stored_gain"] == MIN][0]["position_x"] == 0.0,
        "gate table equals switch-word run, types 0-6": all(
            GATES[["unaffected", "soloed", "following", "muted", "indirectly-muted", "return-solo-muted", "cue"][r["solo_type"]]](int(r["speaker"]))
            == (r["MainOn"], r["SendsOn"]) for r in MIX["solo"]["switch_word"] if r["solo_type"] <= 6),
        "fade length run": MIX["solo"]["track_fade_time"]["samples"] == 75,
    }
    report["x_inputs"] = xcheck
    report["silence_limit_round_trip"] = {str(g): {"volume_gain": volume_gain(f32(g)), "round_trip": to_gain(to_pos(f32(g))),
                                                   "relative_change": to_gain(to_pos(f32(g))) / f32(g) - 1}
                                          for g in (0.000319, 0.00033, 0.0003162277571)}
    for c in cases:
        if c["kind"] == "computation":
            res = []
            for ev in c["evaluations"]:
                got = compute(c["computation"], ev["arguments"])
                res.append(close(got, ev["expected"], max(c["tolerance"], 1e-15)))
            report["computation"][c["id"]] = all(res)
        else:
            xml = (PKG / c["input"]).read_bytes()
            r = render_check(c, xml)
            report["render"][c["id"]] = {k: v for k, v in r.items() if k != "mine"}
    # exclusion probes: the own judge must refuse these variants of the template
    base = (PKG / "fixtures/MIX-GRAPH-018.xml").read_text()
    probes = {"send 0.000318 on A": ('<Manual Value="0.0003162277571" />', '<Manual Value="0.000318" />', 1),
              "SoloSink true": ('<SoloSink Value="false" />', '<SoloSink Value="true" />', 1),
              "crossfade A": ('<CrossFadeState>\n\t\t\t\t\t\t\t<Manual Value="1" />', '<CrossFadeState>\n\t\t\t\t\t\t\t<Manual Value="0" />', 1),
              "tempo envelope value differs": ('Time="-63072000" Value="120"', 'Time="-63072000" Value="121"', 1)}
    pr = {}
    for name, (old, new, n) in probes.items():
        assert old in base, name
        try:
            coefficients(read_set(base.replace(old, new, n).encode()))
            pr[name] = "NOT refused"
        except Excluded as e:
            pr[name] = f"excluded ({e})"
    try:
        ramp_length(0.002, [0.0, 0.0, 100.0, 1e-7], 22050.0, "playing")
        pr["ramp length r >= 2^31"] = "NOT refused"
    except Excluded as e:
        pr["ramp length r >= 2^31"] = f"excluded ({e})"
    report["exclusion_probes"] = pr
    # mutation: each case with its first expected number changed by 1 % must fail the own judge
    missed = []
    for c in cases:
        c2 = json.loads(json.dumps(c))
        if c2["kind"] == "computation":
            def bump(x):  # change the first number or Boolean leaf
                for k in (list(x) if isinstance(x, dict) else range(len(x))):
                    v = x[k]
                    if isinstance(v, (dict, list)):
                        if bump(v):
                            return True
                    else:
                        x[k] = (not v) if isinstance(v, bool) else v + (1 if isinstance(v, int) else 0.01)
                        return True
                return False
            assert bump(c2["evaluations"][-1]["expected"])
            ok = all(close(compute(c2["computation"], e["arguments"]), e["expected"], max(c2["tolerance"], 1e-15))
                     for e in c2["evaluations"])
        else:
            m = c2["expected"]["main"]["L"]
            m["A.L"] = m.get("A.L", 0.0) + 0.01
            ok = render_check(c2, (PKG / c2["input"]).read_bytes())["within_comparator"] and \
                render_check(c2, (PKG / c2["input"]).read_bytes())["coefficients_agree"]
        if ok:
            missed.append(c2["id"])
    report["mutation_missed"] = missed
    # fixtures: form, distinctness, REQ-LIVE-SET-STRUCTURE-001 shapes, single-change from the template
    sch = schema()
    fx = {}
    tmpl = base.split("\n")
    seen = {}
    for p in sorted((PKG / "fixtures").glob("*.xml")):
        b = p.read_bytes()
        changed = [(i + 1, a.strip(), x.strip()) for i, (a, x) in enumerate(zip(tmpl, b.decode().split("\n"))) if a != x]
        fx[p.name] = {"ascii_lf_final_newline": b.isascii() and b"\r" not in b and b.endswith(b"\n"),
                      "duplicate_of": seen.get(b), "lss001_shapes": lss001(sch, ET.fromstring(b)),
                      "lines_changed": changed}
        seen[b] = p.name
    report["fixtures"] = fx
    report["signals"] = {}
    for p in sorted((PKG / "fixtures/signals").glob("*.wav")):
        chunks, params, frames = wav(p)
        report["signals"][p.name] = {"chunks": chunks, "params": list(params),
                                     "matches_formula": frames == [(a / 32768, c / 32768) for a, c in map(SIG_FORMULA[p.name], range(64))],
                                     "max_abs": max(abs(s) for f in frames for s in f)}
    # package
    man = json.loads((PKG / "manifest.json").read_text())
    files = sorted(str(p.relative_to(PKG)) for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
    report["package"] = {
        "manifest_sha256": hashlib.sha256((PKG / "manifest.json").read_bytes()).hexdigest(),
        "listed": len(man["files"]), "inventory_equal": files == sorted(f["path"] for f in man["files"]),
        "hash_or_size_mismatch": [f["path"] for f in man["files"] if hashlib.sha256((PKG / f["path"]).read_bytes()).hexdigest()
                                  != f["sha256"] or (PKG / f["path"]).stat().st_size != f["bytes"]],
        "symlinks": [str(p) for p in PKG.rglob("*") if p.is_symlink()],
        "links": {p.name: [t for t, ok in links(p)] for p in PKG.glob("*.md")},
        "unresolved_links": {p.name: [t for t, ok in links(p) if not ok] for p in PKG.glob("*.md") if any(not ok for _, ok in links(p))},
        "case_count_matches": man["case_count"] == len(cases),
        "missing_inputs": [x for c in cases for x in ([c["input"]] if c["input"] else []) +
                           list(c.get("render", {}).get("signals", {}).values()) if not (PKG / x).is_file()],
    }
    deny = {}
    for p in [*(PKG / f for f in files), PKG / "manifest.json"]:
        if p.suffix == ".wav":
            continue
        t = p.read_text()
        hits = sorted({m for pat in DENY for m in re.findall(pat, t)} - ALLOWED.get(p.name, set()))
        if hits:
            deny[str(p.relative_to(PKG))] = hits
    report["deny_hits"] = deny
    print(json.dumps(report, indent=1, default=str))


if __name__ == "__main__":
    main()
