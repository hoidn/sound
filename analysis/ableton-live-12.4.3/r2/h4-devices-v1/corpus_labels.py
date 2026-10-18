"""H4 static: evidence for Corpus ResonanceType labels (preset names per stored value; Live string run near 'Beam').

Usage: python3 -I corpus_labels.py <App-Resources dir> <Live.arm64> <out dir>
Writes out/corpus_resonance.json:
  by_value: for each stored ResonanceType Manual value, every shipped document (path, SHA-256, UserName) holding it
  live_run: the NUL-delimited __TEXT,__cstring strings around the single C string 'Beam' in Live, with vmaddr
File names and string adjacency are hints, not proof of an enum label order.
Depends on: Python stdlib; out/occurrences.jsonl from presets.py.
"""
import collections, gzip, hashlib, json, os, struct, sys
import xml.etree.ElementTree as ET


def cstring_section(d):
    off, ncmds = 32, struct.unpack_from("<I", d, 16)[0]
    for _ in range(ncmds):
        cmd, cs = struct.unpack_from("<2I", d, off)
        if cmd == 0x19:
            for k in range(struct.unpack_from("<I", d, off + 64)[0]):
                so = off + 72 + 80 * k
                if d[so:so + 16].rstrip(b"\0") == b"__cstring":
                    addr, size, foff = struct.unpack_from("<2QI", d, so + 32)
                    return addr, size, foff
        off += cs
    raise SystemExit("no __cstring")


def main(res, img, outdir):
    by = collections.defaultdict(list)
    seen = set()
    for line in open(os.path.join(outdir, "occurrences.jsonl")):
        o = json.loads(line)
        if o["device"] != "Corpus" or o["doc"] in seen:
            continue
        seen.add(o["doc"])
        raw = open(os.path.join(res, o["doc"]), "rb").read()
        for dev in ET.fromstring(gzip.decompress(raw)).iter("Corpus"):
            by[dev.find("ResonanceType/Manual").get("Value")].append(
                {"doc": o["doc"], "sha256": hashlib.sha256(raw).hexdigest(), "user_name": dev.find("UserName").get("Value")})
    d = open(img, "rb").read()
    addr, size, foff = cstring_section(d)
    i = d.find(b"\0Beam\0", foff, foff + size) + 1
    assert d.count(b"\0Beam\0") == 1 and i > 0
    lo = d.rfind(b"\0", foff, i - 1)
    for _ in range(14):  # step back 14 strings
        lo = d.rfind(b"\0", foff, lo)
    run, p = [], lo + 1
    while len(run) < 28:
        q = d.index(b"\0", p)
        run.append({"vmaddr": hex(addr + p - foff), "value": d[p:q].decode("latin-1")})
        p = q + 1
    json.dump({"by_value": {k: sorted(v, key=lambda r: r["doc"]) for k, v in sorted(by.items(), key=lambda kv: int(kv[0]))},
               "live_run": run}, open(os.path.join(outdir, "corpus_resonance.json"), "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
