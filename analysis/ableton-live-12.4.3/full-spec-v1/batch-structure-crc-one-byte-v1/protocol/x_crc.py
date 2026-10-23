"""Extracted execution (X) of Live's sample-identity CRC step on this host (ADR 0003).

Runs the x86_64 function 0x101191310 (arm64 counterpart 0x1011b6e88; caller 0x10125a540 /
arm64 0x101279eac, which feeds it the first min(size, 16384) bytes of a sample file) with
(data, length, &crc = 0) and compares the 16-bit result with the CRC-16 rule used by
SPEC-LIVE-SET-STRUCTURE (poly 0x8005, MSB first, init 0, no reflection, no final xor).
Inputs: the generated fixture sample, the standard check string, and fixed pseudo-random buffers.
Usage: python3 -I x_crc.py <out.json>   (XEXEC_BIN defaults to a T1.1-owned build path)
Writes <out.json> (per input: result, rule, equality; byte-stable) and x-crc-raw.jsonl beside it.
"""
import hashlib, json, os, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
os.environ.setdefault("XEXEC_BIN", "/var/tmp/sound-analysis/xexec-t11/xexec")
sys.path.insert(0, str(ROOT / "tools" / "xexec"))
from xexec import Runner, SLICE  # noqa: E402

STEP = 0x101191310


def crc16(data):
    c = 0
    for b in data:
        c ^= b << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x8005) if c & 0x8000 else (c << 1)
            c &= 0xFFFF
    return c


def main():
    wav = (HERE.parent / "fixtures" / "Samples" / "T11-tone.wav").read_bytes()
    rng = random.Random(1101)
    inputs = [("fixture T11-tone.wav, first 16384 bytes", wav[:16384]),
              ("ASCII 123456789", b"123456789"),
              ("one zero byte", b"\x00"),
              ("one 0xff byte", b"\xff")]
    inputs += [(f"pseudo-random {n} bytes (seed 1101)", bytes(rng.randrange(256) for _ in range(n))) for n in (1, 7, 1000, 16384)]
    r = Runner()
    rows = []
    for name, data in inputs:
        # The loader takes at most 4,096 bytes per hex buffer, so longer inputs are fed in 4,096-byte
        # pieces with the running CRC word (buffer b1) passed back in, as Live's caller does per block.
        chunks = [data[i:i + 4096] for i in range(0, len(data), 4096)]
        toks = ["call", hex(STEP), "hex:" + chunks[0].hex(), f"i:{len(chunks[0])}", "buf:4"]
        for c in chunks[1:]:
            toks += ["call", hex(STEP), "hex:" + c.hex(), f"i:{len(c)}", "ref:b1"]
        toks += ["dump", "b1", "4"]
        res = r.run(toks)
        got = int.from_bytes(res.dumps[-1][2][:4], "little") & 0xFFFF if res.ok and res.dumps else None
        rows.append({"input": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                     "x86_result": got, "rule": crc16(data), "equal": got == crc16(data),
                     "calls": len(res.calls), "ok": res.ok, "trap": res.trap, "fault": res.fault, "used_imports": res.used})
    out = {"slice": SLICE, "function": hex(STEP), "arm64_counterpart": "0x1011b6e88", "runs": rows,
           "all_equal": all(x["equal"] for x in rows)}
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + "\n")
    # raw runs: argv, exit code, stdout and stderr (heap addresses vary between runs: ASLR)
    raw = Path(sys.argv[1]).with_name("x-crc-raw.jsonl")
    raw.write_text("".join(json.dumps({"argv": a, "rc": x.rc, "stdout": x.stdout, "stderr": x.stderr}) + "\n" for a, x in r.log))
    print("all equal:", out["all_equal"], [(x["input"], x["x86_result"]) for x in rows])


if __name__ == "__main__":
    main()
