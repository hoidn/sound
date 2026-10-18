"""Cross-check model for automation-envelopes-v1 (analyst side, never shipped).

An independent restatement of the released clauses of SPEC-AUTOMATION-ENVELOPES r1: load checks
(REQ-007), event text (REQ-012), curve controls (REQ-008, 009), saved text and the envelope value at t
(REQ-010, 011). model() returns the release representation or raises NoExpectation for inputs the
release excludes. It shares the static evidence of the expectations and is not an oracle.
"""
import json, math, re, struct
import xml.etree.ElementTree as ET
from decimal import Decimal, localcontext

F, B, N = "FloatEvent", "BoolEvent", "EnumEvent"
OPENS, REFUSED = "opens", "refused"
LOW = -63072000.0
CC = ("CurveControl1X", "CurveControl1Y", "CurveControl2X", "CurveControl2Y")

class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


KIND = {"Pan": (F, -1.0, 1.0), "Speaker": (B, None, None), "CrossFadeState": (N, 0, 2),
        "ControllerTargets.6": (F, 0.0, 127.0)}
DEC = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def read_double(text):
    s = text.lstrip(" ")
    if re.match(r"[+-]?(?:0[xX]|inf|nan)", s, re.I) or s == "Invalid" or s[:1] in ("#", "\t", "\n", "\r", "\f", "\v"):
        raise NoExpectation(f"number form {text!r}")
    m = DEC.match(s)
    if not m:
        raise Refused(f"no numeric prefix {text!r}")
    return float(m.group())


def to32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def read_bool(text):
    if text in ("true", "1"):
        return True
    if text in ("false", "0"):
        return False
    raise Refused(f"bool {text!r}")


def read_int(text):
    if re.fullmatch(r" *\+?[0-9]+|[0-9]+ +", text) and len(text.lstrip(" ").lstrip("+").rstrip(" ")) <= 63:
        return int(text)
    if text.strip(" ") == "" or not text.isascii() or re.search(r"[^0-9 +-]", text):
        raise Refused(f"int {text!r}")
    raise NoExpectation(f"int form {text!r}")


def monotone(c1, c2):  # REQ-009 M(c1, c2), restated from the spec
    if not (math.isfinite(c1) and math.isfinite(c2)):
        return False
    if 0 <= c1 <= c2 <= 1:
        return True
    d = c1 * c1 + c2 * c2 - c1 * c2 - c1
    if d <= 2.0 ** -52:
        return True
    q, a = 2 * (3 * c1 - 3 * c2 + 1), c2 - 2 * c1
    if q == 0:
        raise NoExpectation("degenerate curve")
    r1, r2 = (2 * math.sqrt(d) - 2 * a) / q, (-2 * math.sqrt(d) - 2 * a) / q
    if 0 < r1 < 1:
        return False
    return r2 <= 0 or r2 >= 1


def released_kept(c1, c2):  # the release's sufficient condition, with its margin
    return 0 <= c1 <= 1 and 0 <= c2 <= 1 and (c1 <= c2 or c1 * c1 + c2 * c2 - c1 * c2 - c1 <= -1e-6)


def fmt(x, p):  # REQ-012 save rule (P = 17 for binary64, 9 for binary32 values widened exactly)
    if x == 0:
        if math.copysign(1, x) < 0:
            raise NoExpectation("negative zero on save")
        return "0"
    with localcontext() as ctx:
        ctx.prec = 60
        lg = Decimal(abs(x)).log10()
    nearest = lg.to_integral_value()
    if abs(lg - nearest) < Decimal("1e-12") and Decimal(abs(x)) != Decimal(10) ** int(nearest):
        raise NoExpectation("log10 near an integer")
    k = math.ceil(lg) if abs(x) >= 1 else math.floor(lg)
    s = format(Decimal(x), f".{max(0, p - k)}f")
    return s.rstrip("0").rstrip(".") if "." in s else s


def load(data):
    root = ET.fromstring(data)
    npi = int(root.find("LiveSet/NextPointeeId").get("Value"))
    targets = {}
    for e in root.iter():
        if e.tag == "AutomationTarget" or e.tag.startswith("ControllerTargets."):
            if e.get("Id") in targets or int(e.get("Id")) >= npi or e.find("LockEnvelope").get("Value") != "0":
                raise NoExpectation("target ids")
            targets[e.get("Id")] = e
    parent = {c: p for p in root.iter() for c in p}
    name_of = {v: (parent[v].tag if v.tag == "AutomationTarget" else v.tag) for v in targets.values()}
    audio = root.find("LiveSet/Tracks/AudioTrack")
    out = {"track": {}, "clip": []}
    for env in root.iter():
        if env.tag not in ("AutomationEnvelope", "ClipEnvelope"):
            continue
        pid = env.find("EnvelopeTarget/PointeeId").get("Value")
        same = [e for e in root.iter() if e.get("Id") == pid]
        if pid not in targets or len(same) != 1:
            raise NoExpectation("dangling or ambiguous PointeeId")
        tname = name_of[targets[pid]]
        if env.tag == "AutomationEnvelope" and not (tname in ("Pan", "Speaker", "CrossFadeState")
                                                     and targets[pid] in audio.iter() and env in audio.iter()):
            raise NoExpectation("track target relation")
        if env.tag == "ClipEnvelope" and tname != "ControllerTargets.6":
            raise NoExpectation("clip target relation")
        state = env.find("Automation/AutomationTransformViewState")
        if state.find("IsTransformPending").get("Value") != "false" or len(state.find("TimeAndValueTransforms")):
            raise NoExpectation("stored transform")
        cls, lo, hi = KIND[tname]
        evs = []
        for e in env.find("Automation/Events"):
            if e.tag != cls or not {"Id", "Time", "Value"} <= set(e.attrib):
                raise NoExpectation("event class or missing attribute")
            t = read_double(e.get("Time"))
            v = (to32(read_double(e.get("Value"))) if cls == F else read_bool(e.get("Value")) if cls == B
                 else read_int(e.get("Value")))
            cc = {k: read_double(e.get(k)) for k in CC if k in e.attrib}
            if cc and cls != F:
                raise NoExpectation("controls on a non-Float event")
            evs.append({"id": e.get("Id"), "t": t, "v": v, "cc": cc, "tag": cls})
        if not evs:
            raise Refused("empty event list")
        if not (evs[0]["t"] == LOW or evs[0]["t"] == 0.0):
            raise Refused("first event time")
        if len({e["id"] for e in evs}) != len(evs):
            raise NoExpectation("duplicate ids")
        times = [e["t"] for e in evs]
        if times != sorted(times) or any(times.count(x) > 2 for x in times) \
                or any(not (LOW <= x < 1e6) for x in times):
            raise NoExpectation("order or time range")
        if lo is not None and any(not (lo <= e["v"] <= hi) for e in evs):
            raise NoExpectation("value range")
        for i, e in enumerate(evs):
            if not e["cc"]:
                continue
            full = {k: e["cc"].get(k, 0.5) for k in CC}
            ok_pos = 0 < i < len(evs) - 1 and evs[i + 1]["t"] > e["t"] and evs[i + 1]["v"] != e["v"]
            if not (ok_pos and released_kept(full["CurveControl1X"], full["CurveControl2X"])
                    and released_kept(full["CurveControl1Y"], full["CurveControl2Y"])):
                raise NoExpectation("curve controls outside the released condition")
            assert monotone(full["CurveControl1X"], full["CurveControl2X"])
            assert monotone(full["CurveControl1Y"], full["CurveControl2Y"])
            e["cc"] = full
        if env.tag == "AutomationEnvelope":
            if tname in out["track"]:
                raise NoExpectation("two envelopes on one target")
            out["track"][tname] = evs
        else:
            out["clip"].append(evs)
    return out


def save_text(evs):
    rows = []
    for e in evs:
        a = {"Time": fmt(e["t"], 17)}
        a["Value"] = fmt(e["v"], 9) if e["tag"] == F else ("true" if e["v"] else "false") if e["tag"] == B else str(e["v"])
        a.update({k: fmt(c, 17) for k, c in e["cc"].items() if c != 0.5})
        rows.append({"element": e["tag"], "attributes": a})
    return rows


def evaluate(evs, t):
    if t < 0 or t < evs[0]["t"]:
        raise NoExpectation("time before the first event or negative")
    at = [e for e in evs if e["t"] == t]
    if evs[0]["tag"] != F:
        if at:
            raise NoExpectation("discrete value at an event time")
        return [e for e in evs if e["t"] < t][-1]["v"]
    if t > evs[-1]["t"]:
        return evs[-1]["v"]
    if len(at) == 1:
        return at[0]["v"]
    if at:
        raise NoExpectation("step")
    a = [e for e in evs if e["t"] < t][-1]
    b = [e for e in evs if e["t"] > t][0]
    if a["v"] == b["v"]:
        return a["v"]
    raise NoExpectation("interior value between different values")


def model(data, action, expected):
    try:
        m = load(data)
    except Refused:
        return {"outcome": REFUSED}
    got = {"outcome": OPENS}
    if action == "open-save":
        got["saved"] = {"envelopes": [{"target": x["target"], "events": save_text(m["track"][x["target"]])}
                                      for x in expected["saved"]["envelopes"]]}
    if action == "open-evaluate":
        got["values"] = [{"target": x["target"], "time": x["time"], "value": evaluate(m["track"][x["target"]], x["time"])}
                         for x in expected["values"]]
    return got


def same(got, exp):
    if got.get("outcome") != exp["outcome"] or set(got) != set(exp):
        return False
    if "values" in exp:
        for g, e in zip(got["values"], exp["values"]):
            if g["target"] != e["target"] or g["time"] != e["time"] or isinstance(g["value"], bool) != isinstance(e["value"], bool):
                return False
            if isinstance(e["value"], bool) or KIND[e["target"]][0] == N:
                if g["value"] != e["value"]:
                    return False
            elif to32(float(e["value"])) != g["value"]:
                return False
        return len(got["values"]) == len(exp["values"])
    return got == exp


def mutate(exp):
    m = json.loads(json.dumps(exp))
    if "values" in m:
        v = m["values"][0]
        v["value"] = (not v["value"]) if isinstance(v["value"], bool) else v["value"] + 1
    elif "saved" in m:
        a = m["saved"]["envelopes"][0]["events"][-1]["attributes"]
        a["Value"] = {"true": "false", "false": "true"}.get(a["Value"], a["Value"] + "1")
    else:
        m["outcome"] = OPENS if m["outcome"] == REFUSED else REFUSED
    return m
