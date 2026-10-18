"""H4 static: byte-level presence of device-bundle interface anchors in the Live image (no Ghidra project opened).

Usage: python3 -I live_strings.py <Live.arm64> <out dir>
For each anchor, counts exact NUL-delimited C-string occurrences per Mach-O section and reports vmaddr/offset of up to
five. Presence is a fact about bytes only; which code references a string, and why, is a Live-project query.
Also cross-checks every device parameter leaf name from out/params.json (path tail, '.N' suffix removed) against
the Live image (NUL-delimited C string; UTF-16LE byte sequence anywhere) and the owning bundle's __cstring
strings (out/bundle_strings.jsonl, exact or as a substring).
Writes out/live_strings.json. Depends on: Python stdlib; out/params.json; out/bundle_strings.jsonl.
"""
import hashlib, json, os, struct, sys

ANCHORS = ["CreateInstanceU", "DestroyInstanceU", "GetPlugInfoU", "SetSampleRateU", "CalcA", "SetParameterA", "ResetA",
           "Amp.bundle", "Cabinet.bundle", "Analog.bundle", "Tension.bundle", "Collision.bundle", "Electric.bundle",
           "Corpus.bundle", "Devices", "Mac", ".bundle", "com.ableton.live", "com.softube.Amplifier",
           "com.ableton.analog", "Amplifier",
           "Amp", "Cabinet", "UltraAnalog", "StringStudio", "Collision", "LoungeLizard", "Corpus",
           "AmpType", "CabinetType", "MicrophoneTypeSwitch", "MicrophonePosition", "DualMono", "MalletStiffness",
           "FilterCutoffFrequency", "ExcitatorStiffness", "PickupModel", "Resonator1", "SignalChain1"]


def sections(d):
    magic, cpu, _, _, ncmds, _, _, _ = struct.unpack_from("<8I", d)
    assert magic == 0xFEEDFACF and cpu == 0x100000C
    out, off = [], 32
    for _ in range(ncmds):
        cmd, cs = struct.unpack_from("<2I", d, off)
        if cmd == 0x19:
            nsect = struct.unpack_from("<I", d, off + 64)[0]
            for k in range(nsect):
                so = off + 72 + 80 * k
                name = d[so + 16:so + 32].rstrip(b"\0").decode() + "," + d[so:so + 16].rstrip(b"\0").decode()
                addr, size, foff = struct.unpack_from("<2QI", d, so + 32)
                if foff:
                    out.append((name, addr, size, foff))
        off += cs
    return out


def main(img, outdir):
    d = open(img, "rb").read()
    secs = sections(d)
    res = {"image": img, "size": len(d), "sha256": hashlib.sha256(d).hexdigest(), "anchors": {}}
    for a in ANCHORS:
        pat, hits, i = b"\0" + a.encode() + b"\0", [], 0
        while True:
            i = d.find(pat, i)
            if i < 0:
                break
            o = i + 1
            sec = next((s for s in secs if s[3] <= o < s[3] + s[2]), None)
            hits.append({"offset": o, "section": sec[0] if sec else None,
                         "vmaddr": hex(sec[1] + o - sec[3]) if sec else None})
            i = o
        by = {}
        for h in hits:
            by[h["section"]] = by.get(h["section"], 0) + 1
        res["anchors"][a] = {"count": len(hits), "by_section": by, "first": hits[:5],
                             "utf16le_count": d.count(a.encode("utf-16-le"))}
    owner = {"Amp": "Amp.bundle", "Cabinet": "Cabinet.bundle", "UltraAnalog": "Analog.bundle",
             "StringStudio": "Tension.bundle", "Collision": "Collision.bundle", "LoungeLizard": "Electric.bundle",
             "Corpus": "Corpus.bundle"}
    bstr = {}
    for line in open(os.path.join(outdir, "bundle_strings.jsonl")):
        r = json.loads(line)
        bstr.setdefault(r["bundle"], []).append(r["value"])
    params = json.load(open(os.path.join(outdir, "params.json")))
    res["param_names"] = {}
    for dev, r in params.items():
        rows = {}
        for path in r["params"]:
            leaf = path.split("/")[-1].split(".")[0]
            rows[path] = {"leaf": leaf, "live_cstring": d.count(b"\0" + leaf.encode() + b"\0"),
                          "live_utf16le": d.count(leaf.encode("utf-16-le")),
                          "bundle_exact": sum(v == leaf for v in bstr[owner[dev]]),
                          "bundle_substring": sum(leaf in v for v in bstr[owner[dev]])}
        res["param_names"][dev] = {
            "params": len(rows),
            "in_live_utf16le": sum(x["live_utf16le"] > 0 for x in rows.values()),
            "in_live_cstring": sum(x["live_cstring"] > 0 for x in rows.values()),
            "in_live_neither": sorted(p for p, x in rows.items() if not x["live_utf16le"] and not x["live_cstring"]),
            "in_bundle_exact": sorted(p for p, x in rows.items() if x["bundle_exact"]),
            "rows": rows}
    json.dump(res, open(os.path.join(outdir, "live_strings.json"), "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
