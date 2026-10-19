"""Reviewer's own extracted-execution re-run for clip-launch-v2 (analyst side; never shipped).

usage: python3 -I -B x_sample.py > x_sample.out
Runs original x86_64 Live 12.4.3 code with the recorded X2 loaders (never rebuilt), from the
staged cases.json and fixture text, not from the X2 result files:
  1. grid length 0x101ad2ef0 for every (n, d, q) that a grid-length or clip-grid computation needs;
  2. enum getter 0x101556330 for every clip value of a clip-grid computation;
  3. lattice helper 0x1011999d0 (mode 3) on every beat argument, then boundary helper 0x101ae8280
     (mode 1, anchor poked at entry+8) on the rounded beat, for every boundary computation with g > 0;
     for g = 0 the helper is also run, for information only (REQ-018's skip is static);
  4. follow-action post-load 0x10262a930 on UserFloat chances (setup as X2) for the chance pairs of
     CLIP-LAUNCH-029 to 036 and 051 to 059, read from the fixture text;
  5. ARemoteableDouble post-load 0x101555850 (quantize flag set) on the follow times of
     CLIP-LAUNCH-016, 037 to 040 and 060 to 062;
  6. the attribute text conversion 0x10151b630 (X2 transport loader) on every chance and follow-time
     text of those fixtures, so the X inputs are the values the text reads as.
Every process makes at most 120 calls (loader limit 256). Prints JSON.
"""
import importlib.util, json, math, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

A = Path(__file__).resolve().parents[3]          # analysis/ableton-live-12.4.3
REPO = A.parents[1]
PKG = A / "handoff-staging/clip-launch-v2"
SC = "Tracks/MidiTrack[1]/DeviceChain/MainSequencer/ClipSlotList/ClipSlot[1]/ClipSlot/Value/MidiClip"


def load(name, path, loader):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.build = lambda: Path(loader)                # recorded built loader; never rebuild
    return m


xn = load("xexec_notes", REPO / "tools/xexec/xexec.py", "/var/tmp/sound-analysis/xexec-x2-notes-launch/xexec")
xt = load("xexec_transport", A / "r2/x2-transport-v1/xexec.py", "/var/tmp/sound-analysis/xexec/xexec-x2-transport")
RN, RT = xn.Runner(), xt.Runner()
stats = {"processes": 0, "max_calls_per_process": 0}

GRID, LATTICE, BOUNDARY, ENUM_GET = 0x101ad2ef0, 0x1011999d0, 0x101ae8280, 0x101556330
ALLOC = 0x1002c4280
FA_POSTLOAD, FA_NOTIFY, BOOL_SET = 0x10262a930, 0x102630ef0, 0x101554600
UF_VTABLE, UF_VTABLE2, UF_INIT, RAW_FLOAT_STORE, MAPPING_CTOR = 0x106bc35b0, 0x106bc3848, 0x101564e20, 0x101558d40, 0x101566480
RD_VTABLE, RD_POSTLOAD, GENERIC_POSTLOAD = 0x106bc07b0, 0x101555850, 0x10147e120
INIT_STR, CONVERT, VT = 0x1014206e0, 0x10151b630, 0x106a4b178
SET = {0x105a4d44c: "double", 0x105a4d452: "float"}
SKIP_CONV = {0x105a4d446: ["$rsi"], 0x105a4d44c: ["$xmm0.v2_int64[0]"], 0x105a4d452: ["$xmm0.v4_int32[0]"],
             0x105a4d458: ["$rsi"]}
TID = {"float": 0x12, "double": 0x17}


def bits(x):
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def same(a, b):
    return bits(float(a)) == bits(float(b))


def run(runner, toks, skip=None):
    stats["processes"] += 1
    stats["max_calls_per_process"] = max(stats["max_calls_per_process"], toks.count("call"))
    assert toks.count("call") <= 120
    res = runner.run(toks, skip=skip)
    assert res.ok, (res.trap, res.fault, res.stderr[-600:])
    return res


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


cases = json.loads((PKG / "cases.json").read_text())["cases"]
comps = [(c["id"], k) for c in cases for k in c["expected"].get("computations", [])]


def g_args(comp):
    a = comp["arguments"]
    if comp["function"] == "grid-length":
        return [(*a["time_signature"], a["q"])]
    if comp["function"] == "clip-grid":
        k0 = 0 if a["clip_value"] == -99 else a["clip_value"]   # contract REQ-016 clause 1 (checked in step 2)
        return [(*a["song_time_signature"], a["global_value"])] if k0 == 0 else \
            [(*a["clip_time_signature"], k0 - 1)]
    return []


# 1. grid length
need = sorted({t for _, k in comps for t in g_args(k)})
grid = {}
for part in chunks(need, 100):
    toks = ["call", hex(ALLOC), "buf:8"]
    for n, d, q in part:
        toks += ["poke", "b0", f"{(d << 32) | n:#x}", "call", hex(GRID), "ref:b0", f"i:{q & 0xffffffff}"]
    res = run(RN, toks)
    for (n, d, q), c in zip(part, res.calls[1:]):
        grid[(n, d, q)] = xn.as_f64(c["xmm0"])

# 2. enum getter
kvals = sorted({k["arguments"]["clip_value"] for _, k in comps if k["function"] == "clip-grid"})
toks = ["call", hex(ALLOC), "buf:232"]
for v in kvals:
    toks += ["poke", "b0+216", f"{v & 0xffffffff:#x}", "call", hex(ENUM_GET), "ref:b0"]
res = run(RN, toks)
getter = {v: struct.unpack("<i", struct.pack("<I", c["rax"] & 0xffffffff))[0] for v, c in zip(kvals, res.calls[1:])}

# 3. lattice then boundary
bds = [(cid, k) for cid, k in comps if k["function"] == "grid-boundary"]
lat = {}
for part in chunks(sorted({k["arguments"]["beat"] for _, k in bds}), 100):
    toks = ["call", hex(ALLOC), "buf:16"]
    for t in part:
        toks += ["call", hex(LATTICE), "i:3", xn.dbl(t), xn.dbl(1.0), xn.dbl(0.0)]
    res = run(RN, toks)
    lat.update({t: xn.as_f64(c["xmm0"]) for t, c in zip(part, res.calls[1:])})
bnd = {}
keys = sorted({(k["arguments"]["beat"], k["arguments"]["grid"], k["arguments"]["anchor"]) for _, k in bds})
for part in chunks(keys, 100):
    toks = ["call", hex(ALLOC), "buf:16"]
    for t, g, a in part:
        toks += ["poke", "b0+8", f"{bits(a):#x}", "call", hex(BOUNDARY), "ref:b0", xn.dbl(lat[t]), xn.dbl(g), "i:1"]
    res = run(RN, toks)
    bnd.update({key: xn.as_f64(c["xmm0"]) for key, c in zip(part, res.calls[1:])})


# 6 (first, so 4 and 5 use the values the text reads as). Text conversion.
def convert(kind, text):
    raw = text.encode()
    res = run(RT, ["call", hex(INIT_STR), "mk", "hex:" + struct.pack("<I", TID[kind]).hex(), "mk",
                   f"ptrs:{VT:#x},b0", "mk", "hex:" + raw.hex() + "00", "call", hex(CONVERT), "ref:b1",
                   f"ptrs:b2,{len(raw)}"], skip=SKIP_CONV)
    assert len(res.hits) == 1 and SET[res.hits[0][1]] == kind, (text, res.hits)
    v = res.hits[0][2][0]
    return xn.as_f64(v) if kind == "double" else xn.as_f32(v)


def fa_of(cid):
    root = ET.parse(PKG / f"fixtures/{cid}.xml").getroot()
    return root.find("LiveSet/" + SC + "/FollowAction")


chance_cases = [f"CLIP-LAUNCH-{n:03d}" for n in (*range(29, 37), *range(51, 60))]
time_cases = [f"CLIP-LAUNCH-{n:03d}" for n in (16, 37, 38, 39, 40, 60, 61, 62)]
texts = {}
for cid in chance_cases:
    fa = fa_of(cid)
    for nm in ("FollowChanceA", "FollowChanceB"):
        e = fa.find(nm)
        if e is not None:
            texts[(cid, nm)] = ("float", e.get("Value"))
for cid in time_cases:
    texts[(cid, "FollowTime")] = ("double", fa_of(cid).find("FollowTime").get("Value"))
read = {k: convert(*v) for k, v in texts.items()}


# 4. chance rescaling
def userfloat(toks, nb, lo, hi, default, value, mapbuf, cbbuf):
    o = bytearray(0x90)
    struct.pack_into("<QI", o, 0, UF_VTABLE, 1)
    struct.pack_into("<Q", o, 0x70, UF_VTABLE2)
    ob = nb[0]
    toks += ["call", hex(ALLOC), "hex:" + bytes(o).hex()]
    nb[0] += 1
    toks += ["call", hex(UF_INIT), xn.flt(lo), xn.flt(hi), xn.flt(default), f"ref:b{ob}", f"ref:b{mapbuf}",
             f"ref:b{cbbuf}", "call", hex(RAW_FLOAT_STORE), f"ref:b{ob}", xn.flt(value)]
    return ob


chance = {}
for cid in chance_cases:
    a = read.get((cid, "FollowChanceA"), 100.0)     # an absent chance keeps its initial value (REQ-009)
    b = read.get((cid, "FollowChanceB"), 0.0)
    toks, nb = ["call", hex(ALLOC), "buf:56"], [1]
    toks += ["call", hex(MAPPING_CTOR), xn.flt(0), xn.flt(100), xn.flt(1), xn.flt(1), "ref:b0"]
    toks += ["call", hex(ALLOC), "hex:" + struct.pack("<QQ", FA_NOTIFY, 0).hex()]
    nb[0] = 2
    ab = userfloat(toks, nb, 0, 100, 100, a, 0, 1)
    bb = userfloat(toks, nb, 0, 100, 0, b, 0, 1)
    eb, fa = nb[0], nb[0] + 1
    toks += ["call", hex(ALLOC), "buf:104", "call", hex(ALLOC), "buf:320"]
    toks += ["poke", f"b{fa}+0xf0", f"b{ab}", "poke", f"b{fa}+0x108", f"b{bb}", "poke", f"b{fa}+0x120", f"b{eb}"]
    first = toks.count("call")
    toks += ["call", hex(FA_POSTLOAD), f"ref:b{fa}", "dump", f"b{ab}+0x58", "4", "dump", f"b{bb}+0x58", "4"]
    res = run(RN, toks, skip={BOOL_SET: ["$rdi", "$esi"], FA_NOTIFY: ["$rdi", "$rsi", "$edx"]})
    held = [struct.unpack("<f", x)[0] for _, _, x in res.dumps]
    enabled_false = any(addr == BOOL_SET and vals[-1] == 0 for k, addr, vals in res.hits if k >= first)
    chance[cid] = {"loaded": [a, b], "held": held, "enabled_set_false": enabled_false,
                   "a_negative_zero": a == 0 and math.copysign(1, a) < 0}

# 5. follow-time rounding
ft = {}
toks = []
o = bytearray(0x78)
struct.pack_into("<QI", o, 0, RD_VTABLE, 1)
o[0x70] = 1
toks += ["call", hex(ALLOC), "hex:" + bytes(o).hex()]
order = []
for cid in time_cases:
    x = read[(cid, "FollowTime")]
    toks += ["poke", "b0+0x58", f"{bits(x):#x}", "call", hex(RD_POSTLOAD), "ref:b0", "dump", "b0+0x58", "8"]
    order.append(cid)
res = run(RN, toks, skip={GENERIC_POSTLOAD: ["$rdi"]})
for cid, (_, _, raw) in zip(order, res.dumps):
    ft[cid] = struct.unpack("<d", raw)[0]

# ---- compare with the staged cases ----
out = {"value_computations": 0, "value_mismatches": [], "getter": {str(k): v for k, v in getter.items()},
       "g0_boundary_helper_info": {}}
for cid, k in comps:
    a, r = k["arguments"], k["result"]
    out["value_computations"] += 1
    if k["function"] == "grid-length":
        ok = same(grid[(*a["time_signature"], a["q"])], r["grid"])
    elif k["function"] == "clip-grid":
        ok = getter[a["clip_value"]] == (0 if a["clip_value"] == -99 else a["clip_value"])
        ok &= same(grid[g_args(k)[0]], r["grid"])
    else:
        p = lat[a["beat"]]
        ok = same(p, r["rounded_beat"])
        b = bnd[(a["beat"], a["grid"], a["anchor"])]
        if a["grid"] > 0:
            ok &= same(b, r["boundary"])
        else:
            out["g0_boundary_helper_info"][f"{cid} t={a['beat']!r}"] = {"helper": b.hex(), "p": p.hex(),
                                                                        "equal": same(b, p)}
            ok &= same(r["boundary"], p)          # REQ-018: B = p (static); p itself is X
    if not ok:
        out["value_mismatches"].append(cid)

by = {c["id"]: c for c in cases}
doc = {}
for cid in chance_cases:
    v = by[cid]["expected"]["values"]
    exp = [v[SC + "/FollowAction/FollowChanceA"], v[SC + "/FollowAction/FollowChanceB"]]
    en = v.get(SC + "/FollowAction/FollowActionEnabled")
    ok = all(same(x, y) for x, y in zip(chance[cid]["held"], exp))
    if en is False and chance[cid]["loaded"][0] == 0 and chance[cid]["loaded"][1] == 0:
        ok &= chance[cid]["enabled_set_false"]
    doc[cid] = {**chance[cid], "expected": exp, "agrees": ok}
for cid in time_cases:
    exp = by[cid]["expected"]["values"][SC + "/FollowAction/FollowTime"]
    doc[cid] = {"text": texts[(cid, "FollowTime")][1], "read": read[(cid, "FollowTime")],
                "read_equals_python_float": same(read[(cid, "FollowTime")], float(texts[(cid, "FollowTime")][1].rstrip("abc"))),
                "held": ft[cid], "expected": exp, "agrees": same(ft[cid], exp)}
out["text_readings"] = {f"{k[0]} {k[1]}": {"text": v[1], "value": read[k]} for k, v in texts.items()}
out["document_cases"] = doc
out["all_value_computations_agree"] = not out["value_mismatches"]
out["all_document_cases_agree"] = all(d["agrees"] for d in doc.values())
out.update(stats)
print(json.dumps(out, indent=1))
