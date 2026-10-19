"""Cross-check model of the clip-launch-v2 clauses (analyst side; not an oracle).

Restates the candidate's clauses: document reading, conversion, opening corrections and save (reusing the
clip-launch-v1 model in ../clip-launch-v1-analysis/build_clip.py for the unchanged parts), and the value
functions of REQ-015 to 018. It shares the static and X evidence with the expectations, so agreement checks
consistency, not truth.
"""
import copy, math, sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "clip-launch-v1-analysis"))
import build_clip as b1  # noqa: E402


N = 3843840.0
H = 1 / 3843840
Refused, NoExpectation = b1.Refused, b1.NoExpectation
read, kids, leaf_value, num, add_leaf, f32, frinta = b1.read, b1.kids, b1.leaf_value, b1.num, b1.add_leaf, b1.f32, b1.frinta
FA_NAMES, FA_INIT, LAUNCH, ENUMS, RANGE = b1.FA_NAMES, b1.FA_INIT, b1.LAUNCH, b1.ENUMS, b1.RANGE
SC, SA, AR, SN, GQ, AQ = b1.SC, b1.SA, b1.AR, b1.SN, b1.GQ, b1.AQ
MINOR = {"12.0_12402": 12402, "12.0_12117": 12117, "11.0_405": 405}


def lattice(x):
    """REQ-CLIP-LAUNCH-013 binary64 formula for 0 <= x < 1,000,000 (s = +1)."""
    if not 0.0 <= x < 1e6:
        raise NoExpectation(f"lattice input {x!r}")
    return math.floor(abs(x + (H * 1.0) * 0.5) * N) / N


def chances_in_scope(a, b):
    if 0.0 <= a <= 100.0 and 0.0 <= b <= 100.0:
        return True
    return -100.0 <= a <= 200.0 and -100.0 <= b <= 200.0 and abs(f32(a + b)) >= 1.0


def is_negzero(x):
    return isinstance(x, float) and x == 0.0 and math.copysign(1.0, x) < 0


def load_fa(fa_el):
    """Read a follow action (absent items keep initial values), then apply the opening corrections."""
    v = dict(FA_INIT)
    if fa_el is not None:
        for c in fa_el:
            if c.tag not in FA_NAMES:
                raise NoExpectation(f"unknown follow-action child {c.tag}")
        for n in FA_NAMES:
            t = leaf_value(fa_el, n, required=False)
            if t is not None:
                v[n] = read(n, t)
    for n in ("LoopIterations", "JumpIndexA", "JumpIndexB"):
        if not RANGE[n][0] <= v[n] <= RANGE[n][1]:
            raise NoExpectation(f"{n} out of range")
    for n in ("FollowTime", "JumpIndexA", "JumpIndexB"):
        if is_negzero(v[n]):
            raise NoExpectation(f"negative zero {n}")
    a, b = v["FollowChanceA"], v["FollowChanceB"]
    if not chances_in_scope(a, b):
        raise NoExpectation("chances out of scope")
    if a == 0 and b == 0:
        v["FollowChanceA"], v["FollowActionEnabled"] = 100.0, False
    else:
        ra = frinta(f32(a / f32(f32(a + b) / 100.0)))
        rb = f32(100.0 - ra)
        v["FollowChanceA"], v["FollowChanceB"] = min(max(ra, 0.0), 100.0), min(max(rb, 0.0), 100.0)
    v["FollowTime"] = lattice(v["FollowTime"])
    return v


def load_clip(clip):
    for n in LAUNCH:
        if len(kids(clip, n)) > 1:
            raise Refused("duplicate " + n)
    v = {"LaunchMode": read("LaunchMode", leaf_value(clip, "LaunchMode")),
         "LaunchQuantisation": read("LaunchQuantisation", leaf_value(clip, "LaunchQuantisation"))}
    for n, d in b1.CLIP_INIT.items():
        v[n] = num(clip, n, d)
    if not 0.0 <= v["VelocityAmount"] <= 1.0 or is_negzero(v["VelocityAmount"]):
        raise NoExpectation("velocity amount out of scope")
    fa = kids(clip, "FollowAction")
    return v, load_fa(fa[0] if fa else None)


def model(text):
    """Return (outcome, values {path: value}, out-of-range enum names, saved LiveSet element or None)."""
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return "refused", None, None, None
    assert root.tag == "Ableton" and root.get("MajorVersion") == "5" and root.get("SchemaChangeCount") == "1"
    c = MINOR[root.get("MinorVersion")]
    live = copy.deepcopy(root.find("LiveSet"))
    clips = {p: live.find(p) for p in (SC, SA, AR) if live.find(p) is not None}
    try:
        for clip in clips.values():  # conversion steps above c, in increasing order
            if c < 406:
                b1.step406(clip)
            fa = kids(clip, "FollowAction")
            if c < 417 and fa:
                b1.step417(fa[0])
            if c < 421 and fa:
                b1.step421(fa[0])
        if c < 414 and live.find("SceneNames") is not None:
            live.find("SceneNames").tag = "Scenes"  # the old scene list; its scenes carry only a name
        scene = live.find(SN)
        if scene is not None and c < 12203:
            b1.step12203(scene)
        values, wide = {}, []
        for name in (GQ, AQ):
            values[name] = read(name, leaf_value(live, name))
            if not RANGE[name][0] <= values[name] <= RANGE[name][1]:
                raise NoExpectation(f"{name} out of range")
        loaded = {}
        for p, clip in clips.items():
            cv, fv = load_clip(clip)
            loaded[p] = (cv, fv)
            values.update({f"{p}/{k}": x for k, x in cv.items()})
            values.update({f"{p}/FollowAction/{k}": x for k, x in fv.items()})
            wide += [k for k in ENUMS if not RANGE[k][0] <= cv.get(k, fv.get(k)) <= RANGE[k][1]]
        if scene is not None:
            fv = load_fa(scene.find("FollowAction"))
            values.update({f"{SN}/FollowAction/{k}": x for k, x in fv.items()})
    except Refused:
        return "refused", None, None, None
    saved = ET.Element("LiveSet")
    for p, (cv, fv) in loaded.items():
        parent = saved
        for part in p.split("/"):
            parent = ET.SubElement(parent, part.split("[")[0])
        for n in LAUNCH[:4]:
            add_leaf(parent, n, cv[n])
        fa = ET.SubElement(parent, "FollowAction")
        for n in FA_NAMES:
            add_leaf(fa, n, fv[n])
    return "opens", values, wide, saved


# ---- value functions (REQ-015 to 018) ----
NOTE = {5: 2.0, 6: 4 / 3, 7: 1.0, 8: 2 / 3, 9: 0.5, 10: 1 / 3, 11: 0.25, 12: 1 / 6, 13: 0.125}


def grid_length(q, n, d):
    if not (1 <= n <= 99 and d in (1, 2, 4, 8, 16)):
        raise NoExpectation(f"time signature {n}/{d}")
    bar = 4.0 * n / d
    if 1 <= q <= 4:
        return {1: 8 * bar, 2: 4 * bar, 3: 2 * bar, 4: bar}[q]
    return NOTE.get(q, 0.0)


def clip_grid(clip_value, global_value, clip_time_signature, song_time_signature):
    if not 0 <= global_value <= 13 or abs(clip_value) >= 10 ** 6:
        raise NoExpectation("value out of scope")
    k = 0 if clip_value == -99 else clip_value
    if k == 0:
        return grid_length(global_value, *song_time_signature)
    return grid_length(k - 1, *clip_time_signature)


def launch_boundary(beat, grid, anchor):
    p = lattice(beat)
    if grid == 0.0:
        return p, p
    a = max(anchor, 0.0)
    if a > p or anchor <= -1e6:
        raise NoExpectation("anchor out of scope")
    return p, lattice(a + math.ceil((p - a) / grid) * grid)


def compute(function, arguments):
    if function == "grid-length":
        return {"grid": grid_length(arguments["q"], *arguments["time_signature"])}
    if function == "clip-grid":
        return {"grid": clip_grid(**arguments)}
    if function == "grid-boundary":
        if arguments["grid"] != 0.0 and arguments["grid"] not in {grid_length(q, n, d) for q in range(1, 14)
                                                                  for n in range(1, 100) for d in (1, 2, 4, 8, 16)}:
            raise NoExpectation("grid not a grid length")
        p, b = launch_boundary(arguments["beat"], arguments["grid"], arguments["anchor"])
        return {"rounded_beat": p, "boundary": b}
    raise ValueError(function)
