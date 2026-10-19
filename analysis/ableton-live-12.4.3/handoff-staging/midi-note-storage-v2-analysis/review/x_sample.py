"""Reviewer's own extracted-execution re-run of the five new midi-note-storage-v2 cases (analyst side; never shipped).

usage: python3 -I -B x_sample.py > x_sample.out
For every note of the MNS-023 and MNS-072 to 075 fixtures, from the fixture text itself:
  1. the attribute text-to-value conversion (x86 0x10151b630) on each Time, Duration, Velocity, OffVelocity
     and Probability text (X2 transport loader, under gdb, two calls per process);
  2. the note value limits (0x102a2a7f0) and then the note time grid (0x102a2a9b0) on the converted values
     (X2 notes loader, two calls per process);
  3. the double and float attribute value writers (0x10150f7a0, 0x10150f6a0; X2 transport loader, two calls)
     and the number-text functions alone (0x10142b980 P=17, 0x10142b6c0 P=9; two calls) on each held value.
Then the saved notes are assembled with the static omission rule (REQ-004) and compared with cases.json.
Every process makes at most two calls, far below the loader's 256-call limit.
"""
import importlib.util, json, math, struct, sys, zlib
import xml.etree.ElementTree as ET
from pathlib import Path

A = Path(__file__).resolve().parents[3]          # analysis/ableton-live-12.4.3
REPO = A.parents[1]
PKG = A / "handoff-staging/midi-note-storage-v2"
NOTES_LOADER = Path("/var/tmp/sound-analysis/xexec-x2-notes-launch/xexec")


def load(name, path, loader):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.build = lambda: Path(loader)                 # use the recorded built loader; never rebuild
    return m


xn = load("xexec_notes", REPO / "tools/xexec/xexec.py", NOTES_LOADER)
xt = load("xexec_transport", A / "r2/x2-transport-v1/xexec.py", "/var/tmp/sound-analysis/xexec/xexec-x2-transport")
RN, RT = xn.Runner(), xt.Runner()

INIT = 0x1014206e0
LIMITS, GRID = 0x102a2a7f0, 0x102a2a9b0
FMT9, FMT17 = 0x10142b6c0, 0x10142b980
WRITE_F32, WRITE_F64 = 0x10150f6a0, 0x10150f7a0
CONVERT, VT = 0x10151b630, 0x106a4b178
SET = {0x105a4d44c: "double", 0x105a4d452: "float"}
SKIP = {0x105a4d446: ["$rsi"], 0x105a4d44c: ["$xmm0.v2_int64[0]"], 0x105a4d452: ["$xmm0.v4_int32[0]"],
        0x105a4d458: ["$rsi"]}
TID = {"float": 0x12, "double": 0x17}
SLOT30, SLOT38 = 0x103c3e940, 0x103caf380
KIND = {"Time": "double", "Duration": "double", "Velocity": "float", "VelocityDeviation": "float",
        "OffVelocity": "float", "Probability": "float"}
ORDER = ["Time", "Duration", "Velocity", "VelocityDeviation", "OffVelocity", "Probability", "IsEnabled", "NoteId"]
stats = {"processes": 0, "max_calls_per_process": 0}


def run(runner, tokens, skip=None):
    stats["processes"] += 1
    stats["max_calls_per_process"] = max(stats["max_calls_per_process"], tokens.count("call"))
    return runner.run(tokens, skip=skip)


def b64(x):
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def b32(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def convert(kind, text):
    """Original attribute text conversion -> bits of the value it sets (or the refusal)."""
    raw = text.encode()
    res = run(RT, ["call", hex(INIT), "mk", "hex:" + struct.pack("<I", TID[kind]).hex(), "mk", f"ptrs:{VT:#x},b0",
                   "mk", "hex:" + raw.hex() + "00", "call", hex(CONVERT), "ref:b1", f"ptrs:b2,{len(raw)}"], skip=SKIP)
    assert len(res.hits) == 1 and SET[res.hits[0][1]] == kind, (text, res.hits, res.trap, res.stderr[-300:])
    v = res.hits[0][2][0]
    return struct.unpack("<d", struct.pack("<Q", v))[0] if kind == "double" else \
        struct.unpack("<f", struct.pack("<I", v & 0xffffffff))[0]


def limits_grid(n):
    b = bytearray(0x60)
    struct.pack_into("<dd", b, 0x30, n["Time"], n["Duration"])
    struct.pack_into("<ffff", b, 0x40, n["Velocity"], n["VelocityDeviation"], n["OffVelocity"], n["Probability"])
    b[0x50] = 1
    struct.pack_into("<q", b, 0x58, int(n["NoteId"]))
    res = run(RN, ["call", hex(LIMITS), "hex:" + bytes(b).hex(), "call", hex(GRID), "ref:b0+0x28", "buf:48"])
    assert res.ok, res.stderr[-400:]
    t, d = struct.unpack_from("<dd", res.outs[1], 0)
    vel, vd, ov, pr = struct.unpack_from("<ffff", res.outs[1], 0x10)
    return {"Time": t, "Duration": d, "Velocity": vel, "VelocityDeviation": vd, "OffVelocity": ov, "Probability": pr}


def member_writer(kind, x):
    fn, arg = (WRITE_F64, xt.dbl(x)) if kind == "double" else (WRITE_F32, xt.flt(x))
    skip = {SLOT30: ["*(unsigned int*)(*(long*)$rsi+4)"] + [f"*(unsigned long*)(*(long*)$rsi+{16 + 8 * i})"
                                                            for i in range(100)]}
    res = run(RT, ["call", hex(INIT), "mk", f"ptrs:0,0,0,0,0,0,{SLOT30:#x},{SLOT38:#x}", "call", hex(fn), arg,
                   "ptrs:b0"], skip=skip)
    assert len(res.hits) == 1 and res.hits[0][1] == SLOT30, (res.hits, res.stderr[-400:])
    vals = res.hits[0][2]
    return b"".join(struct.pack("<Q", v) for v in vals[1:])[:vals[0]].decode("utf-16-le").rstrip("\0")


def formatter(kind, x):
    res = run(RN, ["call", hex(INIT), "call", hex(FMT9 if kind == "float" else FMT17), "buf:8", xn.dbl(x),
                   "dump", "b0*+16", "b0*+4@"])
    assert res.ok, res.stderr[-400:]
    return xn.ustr(res.dumps[0][2])


cache = {}


def memo(key, f):
    if key not in cache:
        cache[key] = f()
    return cache[key]


def fixture_notes(path):
    root = ET.fromstring(zlib.decompress(path.read_bytes(), 31))
    kts = root.find("LiveSet/Tracks/MidiTrack/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/"
                    "MidiClip/Notes/KeyTracks")
    return [(kt.find("MidiKey").get("Value"), [dict(e.attrib) for e in kt.find("Notes")]) for kt in kts]


cases = {c["id"]: c for c in json.loads((PKG / "cases.json").read_text())["cases"]}
out = {"cases": {}}
for cid in ("MNS-023", "MNS-072", "MNS-073", "MNS-074", "MNS-075"):
    c = cases[cid]
    saved_tracks, rows = [], []
    for key, notes in fixture_notes(PKG / c["input"]):
        saved = []
        for a in notes:
            n = {"VelocityDeviation": 0.0, "Probability": 1.0, "NoteId": a["NoteId"]}   # REQ-003 defaults (static)
            read = {}
            for k, kind in KIND.items():
                if k in a:
                    n[k] = memo(("conv", kind, a[k]), lambda: convert(kind, a[k]))
                    py = float(a[k]) if kind == "double" else struct.unpack("<f", struct.pack("<f", float(a[k])))[0]
                    read[k] = {"text": a[k], "X_bits": hex(b64(n[k]) if kind == "double" else b32(n[k])),
                               "equals_correctly_rounded": (b64(n[k]) if kind == "double" else b32(n[k]))
                               == (b64(py) if kind == "double" else b32(py))}
            held = memo(("lg",) + tuple((k, b64(n[k]) if KIND[k] == "double" else b32(n[k])) for k in KIND)
                        + (n["NoteId"],), lambda: limits_grid(n))
            texts = {}
            for k, kind in KIND.items():
                x = held[k]
                mw = memo(("mw", kind, b64(x)), lambda: member_writer(kind, x))
                fm = memo(("fm", kind, b64(x)), lambda: formatter(kind, x))
                texts[k] = {"held_bits": hex(b64(x) if kind == "double" else b32(x)), "member_writer": mw,
                            "formatter": fm}
            s = {"Time": texts["Time"]["member_writer"], "Duration": texts["Duration"]["member_writer"],
                 "Velocity": texts["Velocity"]["member_writer"]}
            if held["VelocityDeviation"] != 0:                                    # REQ-004 omission (static)
                s["VelocityDeviation"] = texts["VelocityDeviation"]["member_writer"]
            s["OffVelocity"] = texts["OffVelocity"]["member_writer"]
            if held["Probability"] != 1:
                s["Probability"] = texts["Probability"]["member_writer"]
            s["NoteId"] = a["NoteId"]
            saved.append(s)
            rows.append({"key": key, "note_id": a["NoteId"], "read": read, "held": texts,
                         "writers_agree": all(t["member_writer"] == t["formatter"] for t in texts.values())})
        saved_tracks.append({"midi_key": key, "notes": saved})
    exp = c["expected"]["saved_notes"]
    agree = exp["key_tracks"] == saved_tracks and all(list(n) == [k for k in ORDER if k in n]
                                                      for t in exp["key_tracks"] for n in t["notes"])
    out["cases"][cid] = {"notes": rows, "X_saved_key_tracks": saved_tracks, "agrees_with_case": agree}
out["all_agree"] = all(v["agrees_with_case"] for v in out["cases"].values())
out["all_writers_agree"] = all(r["writers_agree"] for v in out["cases"].values() for r in v["notes"])
out["all_readings_correctly_rounded"] = all(r2["equals_correctly_rounded"] for v in out["cases"].values()
                                            for r in v["notes"] for r2 in r["read"].values())
out["minus_zero_readings"] = {f"{key[1]}:{key[2]}": hex(b64(v)) if key[1] == "double" else hex(b32(v))
                              for key, v in cache.items() if key[0] == "conv" and key[2].startswith("-0")}
out.update(stats)
print(json.dumps(out, indent=1))
