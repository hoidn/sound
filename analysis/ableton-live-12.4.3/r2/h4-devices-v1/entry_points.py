"""H4 static: retain the C1 records cited by the device-bundle page and compare the exported entry points.

Usage: python3 -I entry_points.py <helpers root> <out dir>
Copies, unchanged, the C1 corpus records (entry, name, signature, state, warnings, code_sha256, code) of the seven
exported entry points of each bundle plus the CITED functions below into out/entry_points.jsonl, and writes
out/entry_compare.json: per entry point a hash of the pseudocode with addresses and generated names replaced by
'X', grouped into implementation families. Pseudocode is analyst-only evidence; it never crosses the handoff boundary.
Depends on: Python stdlib; /var/tmp/sound-analysis/helpers/<slug>/{corpus/decomp/chunks,slice.json}.
"""
import collections, glob, hashlib, json, os, re, sys

SLUGS = ["Amplifier", "Cabinet", "Analog", "Tension", "Collision", "Electric", "Corpus"]
ENTRY = ["_CreateInstanceU", "_DestroyInstanceU", "_SetSampleRateU", "_GetPlugInfoU", "_CalcA", "_SetParameterA", "_ResetA"]
CITED = {  # function entries cited on wiki/research/device-bundles-static.md
    "Amplifier": ["0x2431c", "0x2ca78", "0x49a90"],          # SetParamFloatValue, CSoftubeParameter::SetAll, AC30Clean 44.1k model
    "Cabinet": ["0x4d1c4"],                                   # 1x12 44.1k model
    "Analog": ["0x18640", "0x179a4", "0x17aa8", "0x17c44", "0x17d58", "0x18d8", "0x1c280"],
    "Tension": ["0x1f7c", "0x13b80"],
    "Collision": ["0x2530"],
    "Electric": ["0x3ddc", "0xc650", "0xc754", "0xc8a4", "0xc9f8"],
    "Corpus": ["0xc40c"],
}
KEEP = ["entry", "name", "signature", "state", "warnings", "body_bytes", "code_sha256", "code"]


def main(root, outdir):
    out = open(os.path.join(outdir, "entry_points.jsonl"), "w")
    norm = collections.defaultdict(dict)
    for slug in SLUGS:
        sl = json.load(open(f"{root}/{slug}/slice.json"))
        want = set(CITED.get(slug, []))
        for f in sorted(glob.glob(f"{root}/{slug}/corpus/decomp/chunks/chunk-*.jsonl")):
            for line in open(f):
                r = json.loads(line)
                if r["name"] in ENTRY or r["entry"] in want:
                    out.write(json.dumps({"helper": slug, "slice_sha256": sl["slice_sha256"],
                                          **{k: r[k] for k in KEEP}}, sort_keys=True) + "\n")
                if r["name"] in ENTRY:
                    n = re.sub(r"(DAT|PTR|FUN|LAB|UNK|switchD|s)_[0-9A-Za-z_]+|0x[0-9a-f]+", "X", r["code"])
                    norm[r["name"]][slug] = hashlib.sha256(n.encode()).hexdigest()[:16]
    out.close()
    families = {}
    for name, d in norm.items():
        groups = collections.defaultdict(list)
        for slug, h in d.items():
            groups[h].append(slug)
        families[name] = sorted(groups.values())
    json.dump({"normalized_hash": norm, "families": families}, open(os.path.join(outdir, "entry_compare.json"), "w"),
              indent=1, sort_keys=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
