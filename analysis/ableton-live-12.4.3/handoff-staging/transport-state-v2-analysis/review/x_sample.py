"""Reviewer's own extracted-execution sample for transport-state-v2 (analyst side; never shipped).

usage: python3 -I -B x_sample.py > x_sample.out
Re-runs the original x86_64 code for every new case through the X2 evidence directory's loader and
driver (read-only import), one or two calls per process, so the loader's 256-call limit cannot apply.
Then recomputes REQ-011 step 1 independently (80-digit decimal log10) and the half-gap band.
"""
import json, math, struct, sys
from decimal import Decimal, getcontext
from pathlib import Path

X2 = Path(__file__).resolve().parents[3] / "r2/x2-transport-v1"
sys.path.insert(0, str(X2))
from xexec import Runner, dbl, flt, f32  # noqa: E402

FMT9, FMT17, INIT = 0x10142b6c0, 0x10142b980, 0x1014206e0
WRITE_F32, WRITE_F64 = 0x10150f6a0, 0x10150f7a0
CONVERT, INT_PARSE, VT = 0x10151b630, 0x100375650, 0x106a4b178
SET = {0x105a4d446: "bool", 0x105a4d44c: "double", 0x105a4d452: "float", 0x105a4d458: "int"}
SKIP = {0x105a4d446: ["$rsi"], 0x105a4d44c: ["$xmm0.v2_int64[0]"], 0x105a4d452: ["$xmm0.v4_int32[0]"],
        0x105a4d458: ["$rsi"]}
TID = {"bool": 0x10, "int": 0x11, "float": 0x12, "double": 0x17}
SLOT30, SLOT38 = 0x103c3e940, 0x103caf380
R = Runner()
getcontext().prec = 80
D63 = "0" * 60 + "201"
out = {"max_calls_per_process": 0}


def run(tokens, skip=None):
    out["max_calls_per_process"] = max(out["max_calls_per_process"], tokens.count("call"))
    return R.run(tokens, skip=skip)


def fmt_text(kind, x):
    """Number-text function alone: two calls (empty-string init, formatter)."""
    res = run(["call", hex(INIT), "call", hex(FMT9 if kind == "float" else FMT17), "buf:8",
               dbl(f32(x) if kind == "float" else x), "dump", "b0*+16", "b0*+4@"])
    assert res.ok, res.stderr
    return res.dumps[0][2].decode("utf-16-le").rstrip("\0")


def writer_text(kind, x):
    fn, arg = (WRITE_F64, dbl(x)) if kind == "double" else (WRITE_F32, flt(x))
    nq = 100
    skip = {SLOT30: ["*(unsigned int*)(*(long*)$rsi+4)"] + [f"*(unsigned long*)(*(long*)$rsi+{16 + 8 * i})" for i in range(nq)]}
    res = run(["call", hex(INIT), "mk", f"ptrs:0,0,0,0,0,0,{SLOT30:#x},{SLOT38:#x}", "call", hex(fn), arg, "ptrs:b0"], skip=skip)
    assert len(res.hits) == 1 and res.hits[0][1] == SLOT30, (res.hits, res.stderr[-400:])
    vals = res.hits[0][2]
    raw = b"".join(struct.pack("<Q", v) for v in vals[1:])
    return raw[:vals[0]].decode("utf-16-le").rstrip("\0")


def convert(kind, text):
    raw = text.encode("utf-8")
    res = run(["call", hex(INIT), "mk", "hex:" + struct.pack("<I", TID[kind]).hex(), "mk", f"ptrs:{VT:#x},b0",
               "mk", "hex:" + raw.hex() + "00", "call", hex(CONVERT), "ref:b1", f"ptrs:b2,{len(raw)}"], skip=SKIP)
    if res.hits:
        _, addr, (v,) = res.hits[0]
        if SET[addr] == "double":
            return "value", "%016x" % v
        if SET[addr] == "float":
            return "value", "%08x" % (v & 0xffffffff)
        return "value", struct.unpack("<i", struct.pack("<I", v & 0xffffffff))[0]
    return ("refused", res.trap) if res.trap else ("error", res.stderr[-300:])


def int_parse(text):
    raw = text.encode()
    res = run(["call", hex(INT_PARSE), "hex:" + raw.hex() if raw else "buf:1", f"i:{len(raw)}"])
    rax = res.calls[-1]["rax"]
    return struct.unpack("<i", struct.pack("<I", rax & 0xffffffff))[0] if rax >> 32 & 1 else None


# ---- independent REQ-011 model ----
def cr_log10(a):
    return float(Decimal(a).log10())


def rule(x, p):
    if x == 0:
        return "-0" if math.copysign(1, x) < 0 else "0"
    L = cr_log10(abs(x))
    k = math.ceil(L) if L >= 0 else math.floor(L)
    t = "%.*f" % (max(0, p - k), x)
    return t.rstrip("0").rstrip(".") if "." in t else t


def exact_rule(x, p):
    lg = Decimal(abs(x)).log10()
    k = math.ceil(lg) if lg >= 0 else math.floor(lg)
    t = "%.*f" % (max(0, p - k), x)
    return t.rstrip("0").rstrip(".") if "." in t else t


def offset(x):
    """Distance of exact log10|x| from the nearest integer n, in gaps between n and its neighbour on that side."""
    lg = Decimal(abs(x)).log10()
    n = int(lg.to_integral_value())
    nf = float(n)
    nb = math.nextafter(nf, math.inf if lg > n else -math.inf)
    return n, float(abs(lg - n) / Decimal(abs(nb - nf)))


SAVE = {"TS-024": 100.00000000000001, "TS-025": 1000.0000000000001, "TS-026": 0.09999999999999999,
        "TS-027": 1e-06, "TS-028": -0.0}
EXPECT_SAVE = {"TS-024": "100.000000000000014", "TS-025": "1000.00000000000011", "TS-026": "0.099999999999999992",
               "TS-027": "0.00000099999999999999995", "TS-028": "-0"}
TEXTS = {"TS-010": ("int", " +201 "), "TS-029": ("int", "+201 "), "TS-030": ("int", "-0"),
         "TS-031": ("int", "2147483648"), "TS-032": ("int", D63 + " "), "TS-033": ("int", "-" + "0" * 63),
         "TS-024": ("double", "100.00000000000001"), "TS-025": ("double", "1000.0000000000001"),
         "TS-026": ("double", "0.09999999999999999"), "TS-027": ("double", "0.000001"), "TS-028": ("double", "-0"),
         "TS-034": ("double", " +4.5 "), "TS-035": ("double", "- 4.5"), "TS-036": ("double", "#4012000000000000"),
         "TS-037": ("float", "#42f00000")}

cases = json.loads((Path(__file__).resolve().parents[2] / "transport-state-v2/cases.json").read_text())["cases"]
by_id = {c["id"]: c for c in cases}
rows = {}
for cid, (kind, text) in TEXTS.items():
    c = by_id[cid]
    got = convert(kind, text)
    row = {"text": text, "converter": got}
    if kind == "int":
        row["parser_alone"] = int_parse(text)
    exp = c["expected"]
    ok = (got[0] == "refused") == (exp["outcome"] == "refused")
    if got[0] == "refused":
        ok = ok and got[1] == "___cxa_allocate_exception"
    for k, v in exp.get("state", {}).items():
        bits = struct.unpack("<Q", struct.pack("<d", v))[0]
        if k == "tempo":
            ok = ok and got[1] == "%08x" % struct.unpack("<I", struct.pack("<f", v))[0]
        else:
            ok = ok and got[1] == "%016x" % bits
    if cid == "TS-028":
        ok = ok and got[1] == "8000000000000000"
    if cid in SAVE:
        x = SAVE[cid]
        row["formatter_alone"] = fmt_text("double", x)
        row["attribute_writer"] = writer_text("double", x)
        row["independent_rule"] = rule(x, 17)
        if x:
            row["exact_log_rule"] = exact_rule(x, 17)
            row["log_offset_gaps"] = offset(x)
            row["glibc_log10_is_cr"] = math.log10(abs(x)) == cr_log10(abs(x))
        ok = ok and row["formatter_alone"] == row["attribute_writer"] == row["independent_rule"] == EXPECT_SAVE[cid] \
            == exp["saved"]["values"][next(iter(exp["saved"]["values"]))]
    row["agrees_with_case"] = ok
    rows[cid] = row
out["cases"] = rows

# REQ-011 worked examples in spec.md, through the formatter in fresh processes and the independent rule.
EX = [("double", 1000.0000000000001, "1000.00000000000011"), ("double", 1e-06, "0.00000099999999999999995"),
      ("double", 120.0, "120"), ("double", 8.0, "8"), ("double", 4.5, "4.5"), ("float", 121.2, "121.199997"),
      ("float", 93.3333333, "93.3333359"), ("double", 0.3, "0.299999999999999989"),
      ("double", 3.3, "3.2999999999999998"), ("double", 100.00000000000001, "100.000000000000014"),
      ("double", 0.09999999999999999, "0.099999999999999992")]
out["spec_examples"] = [{"kind": k, "x": repr(x), "expected": e, "X": fmt_text(k, x),
                         "rule": rule(f32(x) if k == "float" else x, 9 if k == "float" else 17)} for k, x, e in EX]
out["spec_examples_all_agree"] = all(r["expected"] == r["X"] == r["rule"] for r in out["spec_examples"])

# The retained sweep: does X equal the correctly rounded rule outside the 1/4..3/4 band, and where does it not?
sweep = json.loads((X2 / "results/writer.json").read_text())["sweep"]
inside, outside_bad, cr_mismatch = 0, [], []
for r in sweep:
    x = float.fromhex(r["value_hex"])
    x = f32(x) if r["kind"] == "float" else x
    n, off = offset(x)
    band = n != 0 and 0.25 <= off <= 0.75 and Decimal(abs(x)).log10() != n
    inside += band
    mine = rule(x, 9 if r["kind"] == "float" else 17)
    if r["X"] != mine:
        cr_mismatch.append({"value_hex": r["value_hex"], "n": n, "offset": off, "in_band": band})
        if not band:
            outside_bad.append(r["value_hex"])
out["sweep"] = {"values": len(sweep), "in_band": inside, "X_differs_from_independent_cr_rule": len(cr_mismatch),
                "of_those_outside_band": outside_bad,
                "mismatch_offsets": sorted(round(m["offset"], 4) for m in cr_mismatch)}
out["all_new_cases_agree"] = all(r["agrees_with_case"] for r in rows.values())
print(json.dumps(out, indent=1))
