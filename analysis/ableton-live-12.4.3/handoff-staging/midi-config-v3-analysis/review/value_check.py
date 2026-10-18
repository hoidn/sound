"""Reviewer's value checks for midi-config-v3 (analyst side; not payload). Usage: value_check.py PACKAGE_DIR.

Model 1 (`native`): the reviewer's own float32 transliteration of the kept disassembly of the decoder, value
function, apply gate, mode-0 takeover branch, CC receiver (prior blanking, stepped accumulator), 14-bit stores and
combine, and the per-input previous-value table. Takeover choices 1 and 2 are not modelled: reaching them raises,
so an `any` case passes only if no value ever reaches takeover. Model 2 (`contract`): exact rational restatement
of the payload contract text. Neither is the author's model; neither is an oracle.
"""
import json, math, struct, sys
from fractions import Fraction as Q
from pathlib import Path

def F(x): return struct.unpack("<f", struct.pack("<f", float(x)))[0]
FLT_MAX = F(3.4028234663852886e38)
A = [1, 2, 3, 4, 5, 8, 10, 20, 50]  # image 0x10584a5a0 (8 floats) + 50.0 stored by the table init
B = [1, 2, 3, 4, 5, 8, 20, 50]      # image 0x10584a580
ENUM = {"Absolute": 0, "AccelSignedBit": 1, "AccelBinaryOffset": 2, "AccelTwoCompliment": 3, "AccelSignedBit2": 4,
        "Absolute14Bit": 5, "LinearSignedBit": 6, "LinearBinaryOffset": 7, "LinearTwoCompliment": 8, "LinearSignedBit2": 9}

def tab(t, i, fb): return float(t[i]) if 0 <= i < len(t) else fb

def decode(m, v):  # 0x101b7b96c
    w = int(v)
    if m == 1: return tab(A, w - (65 if w >= 65 else 1), 20.0) * (-1 if w >= 65 else 1)
    if m == 2: return tab(B, w - 65 if w > 63 else 63 - w, 50.0) * (-1 if w <= 63 else 1)
    if m == 3: return tab(B, w - 1 if w < 66 else 127 - w, 50.0) * (-1 if w >= 66 else 1)
    if m == 4: return tab(B, w - (65 if w > 64 else 1), 50.0) * (-1 if w <= 64 else 1)
    if m == 6: return v if w < 65 else F(64.0 - v)
    if m == 7: return F(v - 64.0)
    if m == 8: return v if w < 65 else F(v - 128.0)
    if m == 9: return -v if w < 65 else F(v - 64.0)
    return 0.0

def frinta(x): return float(math.copysign(math.floor(abs(Q(x)) + Q(1, 2)), x))

def value_fn(v, m, s, quant, inv, cur, lo, hi):  # 0x101b76bf0
    if m in (0, 5):
        t = F((F(127.0 - v) if inv else v) / 127.0)
        r = F(Q(hi) * Q(t) + Q(F(lo * F(1.0 - t))))  # fmadd
    else:
        d = F(decode(m, v) * s)
        step = 1.0 if d > 0 else -1.0
        if not quant: step = F(F(F(hi - lo) * F(1 / 256)) * d)
        if inv: step = -step
        r = F(step + cur)
        r = hi if hi < r else r
        r = lo if lo > r else r
    return frinta(r) if quant else r

class TakeoverReached(Exception): pass

class Param:
    def __init__(s, p): s.min, s.max, s.quant, s.cur, s.type = F(p["min"]), F(p["max"]), p["stepped"], F(p["initial_value"]), 1

def apply(par, v, prior, m, s, choice):  # 0x101b7fde4, Zoom 1, type 1
    inv = par.max < par.min
    lo, hi = (par.max, par.min) if inv else (par.min, par.max)
    r = value_fn(v, m, s, par.quant, inv, par.cur, lo, hi)
    if m in (0, 5) and par.type == 1 and prior != FLT_MAX:  # takeover 0x101b7c508
        if choice != 0: raise TakeoverReached
        r = hi if r > hi else (lo if r < lo else r)
    par.cur = r  # setter assumed to store exactly (contract precondition)

class CCReceiver:  # 0x101b7f32c init, 0x101b7f894
    def __init__(s, par, avoid): s.par, s.avoid, s.sens, s.acc = par, avoid, 1.0, 0.0
    def __call__(s, v, prior, m, choice):
        if s.avoid: prior = FLT_MAX  # Zoom == 1.0 for script mappings
        if m not in (0, 5) and s.par.quant:
            acc = F(s.acc + (s.sens if decode(m, v) > 0 else -s.sens))
            sign = 1.0 if acc >= 0 else -1.0
            fire = acc * sign >= 1.0
            s.acc = F(acc - sign) if fire else acc
            if not fire: return
        apply(s.par, v, prior, m, s.sens, choice)

class Pair:  # 0x1026094e0 (flag fixed 0), 0x101b8028c / 0x101b802bc / 0x101b7fcc0
    def __init__(s, par): s.par, s.flag, s.h = par, False, [FLT_MAX] * 4  # msb, lsb, prior msb, prior lsb
    def store(s, i, v, prior, choice):
        s.h[i], s.h[i + 2] = v, prior
        if s.h[0] != FLT_MAX and s.h[1] != FLT_MAX:
            val = F(((int(s.h[0]) << 7) | int(s.h[1])) / 129.0)
            pr = FLT_MAX if s.flag or FLT_MAX in s.h[2:] else F(((int(s.h[2]) << 7) | int(s.h[3])) / 129.0)
            apply(s.par, val, pr, 0, 1.0, choice)
            s.h = [FLT_MAX] * 4

def native(mode, avoid, p, msgs, choice):
    par, m = Param(p), ENUM[mode]
    table = {}  # per-input previous values, filled with -129.0 at open
    if m == 5:
        pr = Pair(par); handlers = {20: lambda v, q, c: pr.store(0, v, q, c), 52: lambda v, q, c: pr.store(1, v, q, c)}
    else:
        rx = CCReceiver(par, avoid); handlers = {20: lambda v, q, c: rx(v, q, m, c)}
    out = []
    for msg in msgs:
        st, n, v = (int(x, 16) for x in msg.split())
        assert st == 0xB0
        prior = table.get(n, -129.0); table[n] = float(v)
        if n in handlers: handlers[n](float(v), prior, choice)
        out.append(par.cur)
    return out

DEC = {"LinearSignedBit": lambda v: v if v <= 64 else -(v - 64), "LinearSignedBit2": lambda v: -v if v <= 64 else v - 64,
       "LinearTwoCompliment": lambda v: v if v <= 64 else v - 128, "LinearBinaryOffset": lambda v: v - 64,
       "AccelSignedBit": lambda v: (1 if v <= 64 else -1) * (A[(v if v <= 64 else v - 64) - 1] if 1 <= (v if v <= 64 else v - 64) <= 9 else 20),
       "AccelSignedBit2": lambda v: (-1 if v <= 64 else 1) * (B[(v if v <= 64 else v - 64) - 1] if 1 <= (v if v <= 64 else v - 64) <= 8 else 50),
       "AccelTwoCompliment": lambda v: (1 if v <= 65 else -1) * (B[(v if v <= 65 else 128 - v) - 1] if 1 <= (v if v <= 65 else 128 - v) <= 8 else 50),
       "AccelBinaryOffset": lambda v: (1 if v >= 64 else -1) * (B[(v - 64 if v >= 64 else 64 - v) - 1] if 1 <= (v - 64 if v >= 64 else 64 - v) <= 8 else 50)}

def contract(mode, p, msgs):  # payload spec.md, value transforms
    lo, hi, cur, held, out = Q(p["min"]), Q(p["max"]), Q(p["initial_value"]), {}, []
    rnd = lambda x: Q(math.floor(abs(x) + Q(1, 2))) * (1 if x >= 0 else -1)
    for msg in msgs:
        _, n, v = (int(x, 16) for x in msg.split())
        if mode == "Absolute": cur = lo + (hi - lo) * Q(v, 127)
        elif mode == "Absolute14Bit":
            held["msb" if n == 20 else "lsb"] = v
            if len(held) == 2: cur = lo + (hi - lo) * Q(128 * held["msb"] + held["lsb"], 16383); held = {}
        else:
            d = DEC[mode](v)
            cur = min(hi, max(lo, cur + ((1 if d > 0 else -1) if p["stepped"] else (hi - lo) * Q(d, 256))))
        if p["stepped"]: cur = rnd(cur)
        out.append(cur)
    return out

pkg = Path(sys.argv[1]); res = {"cases": {}, "decode_table_disagreements": [], "probes": {}}
for mode, m in ENUM.items():
    if mode in DEC:
        res["decode_table_disagreements"] += [(mode, v) for v in range(128) if decode(m, float(v)) != DEC[mode](v)]
for c in json.loads((pkg / "cases.json").read_text())["cases"]:
    if "stimulus" not in c: continue
    st, exp = c["stimulus"], c["expected"]["values"]
    (a,) = c["expected"]["assignments"]
    avoid = a["control"] == "CrossfaderSlider"
    rows = {"contract_max_err": max(abs(float(x) - e) for x, e in zip(contract(a["map_mode"], st["parameter"], st["messages"]), exp)),
            "expected_is_contract_rounded_9dp": [round(float(x), 9) for x in contract(a["map_mode"], st["parameter"], st["messages"])] == exp}
    for choice in ((0,) if st["takeover"] == "none" else (0, 1, 2)):
        try:
            got = native(a["map_mode"], avoid, st["parameter"], st["messages"], choice)
            rows[f"native_choice{choice}_max_err"] = max(abs(g - e) for g, e in zip(got, exp))
        except TakeoverReached:
            rows[f"native_choice{choice}_max_err"] = "takeover reached"
    rows["len_ok"] = len(exp) == len(st["messages"])
    res["cases"][c["id"]] = rows
CONT = {"min": 0, "max": 1, "stepped": False, "initial_value": 0.5}
def probe(mode, avoid, p, msgs, choice):
    try: return native(mode, avoid, p, msgs, choice)
    except TakeoverReached: return "takeover reached"
res["probes"] = {  # F1 and F2 checks, not cases
    "crossfader Absolute 0x20, choice 1": probe("Absolute", True, CONT, ["B0 14 20"], 1),
    "crossfader Absolute14Bit 0x20/0x00, choice 1": probe("Absolute14Bit", True, CONT, ["B0 14 20", "B0 34 00"], 1),
    "crossfader Absolute14Bit 0x20/0x00, choice 0": probe("Absolute14Bit", True, CONT, ["B0 14 20", "B0 34 00"], 0),
    "encoder Absolute 0x20, choice 1": probe("Absolute", False, CONT, ["B0 14 20"], 1),
    "reversed min 1 max 0, Absolute 0x00 0x7F, choice 0": probe("Absolute", False, {"min": 1, "max": 0, "stepped": False, "initial_value": 0.5}, ["B0 14 00", "B0 14 7F"], 0),
    "reversed min 1 max 0, LinearSignedBit +1": probe("LinearSignedBit", False, {"min": 1, "max": 0, "stepped": False, "initial_value": 0.5}, ["B0 14 01"], 0),
    "reversed stepped min 3 max 0 from 1, LinearSignedBit +1": probe("LinearSignedBit", False, {"min": 3, "max": 0, "stepped": True, "initial_value": 1}, ["B0 14 01"], 0),
}
bad = [k for k, r in res["cases"].items() if not (r["len_ok"] and r["expected_is_contract_rounded_9dp"] and r["contract_max_err"] <= 1e-6
       and all(isinstance(v, float) and v <= 1e-6 for kk, v in r.items() if kk.startswith("native")))]
res["value_cases"] = len(res["cases"]); res["failing"] = bad
print(json.dumps(res, indent=1))
