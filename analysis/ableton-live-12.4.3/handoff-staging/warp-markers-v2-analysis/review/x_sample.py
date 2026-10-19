"""Reviewer's extracted-execution check of warp-markers-v2 (analyst side; never shipped).

usage: python3 -I -B x_sample.py [PACKAGE_DIR] > x_sample.out
For every case labelled extracted execution: (1) decode the retained X2 raw runs (raw/runs.jsonl, not
results/) and compare the deciding values bit for bit with the case; (2) re-run those deciding values in
fresh processes of the X2 loader through the X2 driver (read-only import), with inputs taken from the
package: the marker list parsed from the case's fixture, the argument from cases.json. Conversion cores get
x = frames / 8000 (or the beat) and the result is multiplied by 8000 here; grid rounding runs in the marker
beat setter; the bounds routine runs once per neighbour. Each process makes at most 256 calls.
Also: whether the seconds X2 passed (frames / 48000) equal the case's (frames / 8000), and whether the
multiplication by 8000 is exact. No computed-by-rules input is run here.
"""
import json, struct, sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
X2 = ROOT / "analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1"
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PKG = Path(ARGS[0]).resolve() if ARGS else HERE.parents[1] / "warp-markers-v2"
sys.path.insert(0, str(X2))
import run_x2 as D  # noqa: E402  (module import only; its main() is not run)
from seq import Seq  # noqa: E402

PROV_X = "extracted execution; not observed reference output"
RATE = 8000.0
CMDS = {"call", "mkbuf", "poke", "poke4", "poked", "pokef", "dump", "init", "mk"}
NARGS = {"mkbuf": 1, "poke": 2, "poke4": 2, "poked": 2, "pokef": 2, "dump": 2, "init": 2, "mk": 1}


def f64(bits):
    return struct.unpack("<d", struct.pack("<Q", bits))[0]


def markers(fx):
    root = ET.parse(PKG / fx).getroot()
    clip = root.find("LiveSet/Tracks/AudioTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/AudioClip")
    return [(float(m.get("SecTime")), float(m.get("BeatTime"))) for m in clip.find("WarpMarkers")]


# ---- (1) the retained raw runs, decoded from argv and stdout ----
def parse_run(rec):
    toks, i, calls, bufs, nbuf = rec["argv"], 0, [], {}, 0
    while i < len(toks):
        t = toks[i]
        if t == "call":
            j = i + 2
            while j < len(toks) and toks[j] not in CMDS:
                j += 1
            args = toks[i + 2:j]
            calls.append((int(toks[i + 1], 16), args))
            nbuf += sum(a.split(":", 1)[0] in ("buf", "hex", "str") for a in args)
            i = j
            continue
        if t == "mkbuf":
            nbuf += 1
        if t == "poked":
            b, _, off = toks[i + 1].partition("+")
            bufs.setdefault(b, {})[int(off or 0)] = float(toks[i + 2])
        if t == "poke":
            b, _, off = toks[i + 1].partition("+")
            bufs.setdefault(b, {})[("ptr", int(off or 0))] = toks[i + 2]
        i += 1 + NARGS.get(t, 0)
    regs = [dict(x.split("=") for x in l.split()[3:]) for l in rec["stdout"].splitlines() if l.startswith("call ")]
    assert len(regs) == len(calls), (rec["label"], len(regs), len(calls))
    return calls, bufs, regs


def retained():
    conv, q, bounds = {}, {}, {}
    for line in (X2 / "raw/runs.jsonl").read_text().splitlines():
        rec = json.loads(line)
        if rec["label"] not in ("M1", "M2", "beat-grid-q", "add-bounds-monotone"):
            continue
        calls, bufs, regs = parse_run(rec)
        for (addr, args), r in zip(calls, regs):
            if addr in (D.SB_CONV, D.BS_CONV):
                tb = bufs[args[1].split(":")[1]]
                beats, secs = bufs[tb[("ptr", 0)]], bufs[tb[("ptr", 16)]]
                table = tuple((secs[8 * k], beats[8 * k]) for k in range(len(beats)))
                kind = "s2b" if addr == D.SB_CONV else "b2s"
                conv[(table, kind, float(args[0][2:]))] = f64(int(r["xmm0"], 16))
            elif addr == D.BEAT_Q:
                q[float(args[0][2:])] = f64(int(r["xmm0"], 16))
            elif addr == D.ADD_BOUNDS:
                new, nb = bufs[args[0].split(":")[1]], bufs[args[1].split(":")[1]]
                bounds[((nb[80], nb[88]), new[80])] = [f64(int(r["xmm0"], 16)), f64(int(r["xmm1"], 16))]
    return conv, q, bounds


# ---- deciding values of a case (own neighbour rule, REQ-015 clause 3) ----
def neighbours(ms, p):
    vis = ms[:-1]
    i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
    return [n for n in ((ms[i - 1] if i > 0 else None), (vis[i] if i < len(vis) else None)) if n]


def needs(case):
    c, f = case["call"], case["call"]["function"]
    ms = tuple(markers(case["input"]))
    if f == "sample_to_beat_time":
        return [("conv", ms, "s2b", c["sample_frames"] / RATE)]
    if f == "beat_to_sample_time":
        return [("conv", ms, "b2s", float(c["beat"]))]
    out = [("q", float(c["beat"]))]
    if f == "add_warp_marker":
        out += [("bounds", nb, float(c["sample_time_seconds"])) for nb in neighbours(list(ms), float(c["sample_time_seconds"]))]
    return out


# ---- (2) fresh runs ----
MAXCALLS = [0]


def go(s):
    MAXCALLS[0] = max(MAXCALLS[0], s.tokens.count("call"))
    assert s.tokens.count("call") <= 256
    r = s.run()
    assert r.ok, (r.rc, r.trap, r.fault, r.stderr[-300:])
    return r


def table(s, ms):
    tb, ab, asec = s.mkbuf(0x20), s.mkbuf(8 * len(ms)), s.mkbuf(8 * len(ms))
    for k, (sec, beat) in enumerate(ms):
        s.poke("poked", f"b{ab}+{8 * k}", beat.hex())
        s.poke("poked", f"b{asec}+{8 * k}", sec.hex())
    s.poke("poke", f"b{tb}", f"b{ab}"); s.poke("poke4", f"b{tb}+8", str(len(ms)))
    s.poke("poke", f"b{tb}+16", f"b{asec}"); s.poke("poke4", f"b{tb}+24", str(len(ms)))
    return tb


def rerun(items):
    res = {}
    convs = [x for x in items if x[0] == "conv"]
    for ms in sorted({x[1] for x in convs}):
        s, idx = Seq(init=False), {}
        tb = table(s, ms)
        for _, m, kind, v in convs:
            if m == ms and (kind, v) not in idx:
                c, _ = s.call(D.SB_CONV if kind == "s2b" else D.BS_CONV, f"d:{v.hex()}", f"ref:b{tb}")
                idx[(kind, v)] = c
        r = go(s)
        for (kind, v), c in idx.items():
            res[("conv", ms, kind, v)] = f64(r.calls[c]["xmm0"])
    qs = sorted({x[1] for x in items if x[0] == "q"})
    if qs:
        D.SUB = D.registry_subset()
        s = D.prologue(warp=True)
        _, (bm,) = s.call(D.NEW_WARP_MARKER, "buf:8")
        for b in qs:
            s.call(D.BEAT_Q, f"d:{b.hex()}", f"ref:b{bm}*"); s.dump(f"b{bm}*+88", 8)
        r = go(s)
        for b, d in zip(qs, r.dumps):
            res[("q", b)] = f64(int.from_bytes(d[2], "little"))
    bs = sorted({(x[1], x[2]) for x in items if x[0] == "bounds"})
    if bs:
        s, idx = Seq(init=False), {}
        for nb, p in bs:
            b_nb, b_new = s.mkbuf(0x60), s.mkbuf(0x60)
            s.poke("poked", f"b{b_nb}+80", nb[0].hex()); s.poke("poked", f"b{b_nb}+88", nb[1].hex())
            s.poke("poked", f"b{b_new}+80", p.hex())
            idx[(nb, p)], _ = s.call(D.ADD_BOUNDS, f"ref:b{b_new}", f"ref:b{b_nb}")
        r = go(s)
        for k, c in idx.items():
            res[("bounds",) + k] = [f64(r.calls[c]["xmm0"]), f64(r.calls[c]["xmm1"])]
    return res


def lookup_retained(item, conv, q, bounds):
    if item[0] == "conv":
        _, ms, kind, v = item
        return conv.get((ms, kind, v))
    if item[0] == "q":
        return q.get(item[1])
    return bounds.get((item[1], item[2]))


def final(case, item, v):
    """The case-level value from a core result: frames for beat_to_sample_time."""
    if item[0] == "conv" and item[2] == "b2s":
        return v * RATE
    return v


def judge(case, vals):
    """Outcome from the deciding values (as-given checks and the rest of the call are the model's)."""
    exp, f = case["expected"], case["call"]["function"]
    if f in ("sample_to_beat_time", "beat_to_sample_time"):
        return {"value": vals[0]} == {"value": exp.get("value")}
    qv = vals[0]
    if f == "add_warp_marker":
        inside = all(lo <= qv <= hi for lo, hi in vals[1:])
        return ("accepted" if inside else "refused") == exp["outcome"]
    ms = markers(case["input"])
    hit = next((k for k, m in enumerate(ms) if m[1] == qv), None)
    return (hit is None) == (exp.get("refusal_reason") == "no-such-marker")


def main():
    cases = [c for c in json.loads((PKG / "cases.json").read_text())["cases"] if c["expectation_provenance"] == PROV_X]
    conv, q, bounds = retained()
    plan = {c["id"]: needs(c) for c in cases}
    fresh = rerun([x for v in plan.values() for x in v])
    out = {"package": str(PKG), "x_labelled_cases": len(cases), "cases": {}}
    for c in cases:
        rows, kept_vals, fresh_vals = [], [], []
        for item in plan[c["id"]]:
            kv, fv = lookup_retained(item, conv, q, bounds), fresh[item]
            kept_vals.append(None if kv is None else final(c, item, kv))
            fresh_vals.append(final(c, item, fv))
            row = {"what": item[0] if item[0] != "conv" else f"{item[2]} core", "input": repr(item[-1] if item[0] != "bounds" else (item[1], item[2])),
                   "retained_run": kv, "fresh_run": fv, "same_bits": kv is not None and repr(kv) == repr(fv)}
            if item[0] == "conv" and item[2] == "s2b":
                frames = c["call"]["sample_frames"]
                row["x2_frames_at_48000"] = frames * 6
                row["seconds_equal"] = frames * 6 / 48000.0 == frames / RATE
            if item[0] == "conv" and item[2] == "b2s":
                row["times_8000_exact"] = Fraction(fv) * 8000 == Fraction(fv * RATE)
            rows.append(row)
        out["cases"][c["id"]] = {"deciding": rows, "all_in_retained_run": None not in kept_vals,
                                 "retained_agrees_with_case": None not in kept_vals and judge(c, kept_vals),
                                 "fresh_agrees_with_case": judge(c, fresh_vals)}
    out["max_calls_per_process"] = MAXCALLS[0]
    out["all_ok"] = all(v["all_in_retained_run"] and v["retained_agrees_with_case"] and v["fresh_agrees_with_case"]
                        and all(r["same_bits"] for r in v["deciding"]) for v in out["cases"].values())
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
