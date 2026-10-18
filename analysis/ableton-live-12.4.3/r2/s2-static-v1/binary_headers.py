"""S2 static: byte-level header identification for non-XML containers (.alp, binary .agr/.adv, .amxd).

Usage: python3 -I binary_headers.py <out dir> <file>...
Writes <out>/binary_headers.json. Bounded: header bytes, entropy profile, size-field and
embedded-signature probes, trial raw/zlib inflate at the first offsets. No extraction.
"""
import hashlib, json, math, os, struct, sys, zlib
from collections import Counter

SIGS = {b"PK\x03\x04": "zip-local", b"\x1f\x8b\x08": "gzip", b"\x89PNG": "png", b"<?xml": "xml-decl",
        b"RIFF": "riff", b"OggS": "ogg", b"SQLite format 3": "sqlite", b"\x28\xb5\x2f\xfd": "zstd",
        b"\xfd7zXZ": "xz", b"BZh": "bzip2"}


def entropy(b):
    if not b:
        return 0.0
    c = Counter(b)
    return -sum(n / len(b) * math.log2(n / len(b)) for n in c.values())


def probe(path):
    raw = open(path, "rb").read()
    n = len(raw)
    blocks = [raw[i:i + 65536] for i in range(0, n, 65536)]
    ent = [round(entropy(b), 3) for b in blocks]
    tail_zero_run = len(raw) - len(raw.rstrip(b"\0"))
    # u32/u64 header words that equal file size or size minus a small header
    size_hits = []
    for off in range(0, 64, 4):
        for fmt in ("<I", ">I"):
            v = struct.unpack_from(fmt, raw, off)[0]
            if 0 < n - v < 64 or v == n:
                size_hits.append({"offset": off, "fmt": fmt, "value": v, "file_size_minus_value": n - v})
    sig_hits = {name: [i for i in _find_all(raw, s)][:5] for s, name in SIGS.items()}
    inflate = {}
    for off in range(0, 32):
        for label, wbits in (("raw", -15), ("zlib", 15)):
            try:
                d = zlib.decompressobj(wbits)
                out = d.decompress(raw[off:off + 65536], 64)
                if len(out) >= 16:
                    inflate.setdefault(label, []).append(off)
            except zlib.error:
                pass
    return {"path": path, "size": n, "sha256": hashlib.sha256(raw).hexdigest(), "head64": raw[:64].hex(),
            "tail64": raw[-64:].hex(), "tail64_nonzero_offsets_from_end": [64 - i for i, c in enumerate(raw[-64:]) if c],"entropy_whole": round(entropy(raw), 4),
            "entropy_per_64KiB_min_median_max": [min(ent), sorted(ent)[len(ent) // 2], max(ent)],
            "entropy_first_block": ent[0], "entropy_last_block": ent[-1],
            "zero_byte_fraction": round(raw.count(0) / n, 4), "trailing_zero_bytes": tail_zero_run,
            "header_size_field_hits": size_hits, "embedded_signature_offsets_first5": {k: v for k, v in sig_hits.items() if v},
            "inflate_ok_at_offsets_0_31": inflate}


def _find_all(b, s):
    i = b.find(s)
    while i != -1:
        yield i
        i = b.find(s, i + 1)


if __name__ == "__main__":
    assert entropy(b"\0" * 8) == 0.0 and abs(entropy(bytes(range(256))) - 8.0) < 1e-9
    out = sys.argv[1]
    json.dump([probe(p) for p in sys.argv[2:]], open(os.path.join(out, "binary_headers.json"), "w"), indent=1)
