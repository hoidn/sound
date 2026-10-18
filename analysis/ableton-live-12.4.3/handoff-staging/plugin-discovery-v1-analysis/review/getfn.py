"""Print decompiled functions from a corpus chunk by address, with code SHA-256.

Usage: python3 -I getfn.py CORPUS_ROOT CHUNK ADDR [ADDR...]
"""
import hashlib, json, sys
from pathlib import Path

root, chunk, addrs = Path(sys.argv[1]), sys.argv[2], {a.lower() for a in sys.argv[3:]}
path = root / "decomp" / "chunks" / f"chunk-{chunk}.jsonl"
for line in path.open():
    rec = json.loads(line)
    addr = next((str(rec[k]).lower() for k in ("address", "addr", "entry") if k in rec), None)
    if addr in addrs or ("0x" + addr if addr else None) in addrs:
        code = rec.get("code") or rec.get("c") or ""
        print("//", addr, {k: v for k, v in rec.items() if k not in ("code", "c")})
        print("// code sha256", hashlib.sha256(code.encode()).hexdigest())
        print(code)
