#!/bin/sh
# Regenerate H6 (web connector, add-ons, swapper) static evidence.
# Read-only on the bundle and on the helper corpora; executes nothing from either.
set -eu
B="/home/ollie/Ableton Live 12 Suite.app/Contents"
HP=/var/tmp/sound-analysis/helpers
H=$(cd "$(dirname "$0")" && pwd)
P="$B/App-Resources/Python"
E="$B/App-Resources/Extensions"
rm -rf "$H/pyc-listings"
python3 -I "$H/pyc311.py" "$P/lib/opcode.pyc" "$H/pyc-listings" "$P/abl.webconnector" "$P/scripts"
python3 -I "$H/macho_meta.py" "$E/WebConnector/Ableton Web Connector" "$E/WebConnector/Ableton Swapper" \
  "$E/WebConnector/xdelta3" "$E/AddOns/Ableton AddOns" > "$H/macho-meta.json"
python3 -I "$H/find_strings.py" "$B/MacOS/Live" "$H/live-strings.txt" > "$H/live-anchors.json"
python3 -I "$H/helper_evidence.py" "$HP/Ableton_Web_Connector" "$H/wc-strings.txt" "$H/wc-entries.txt" > "$H/wc-evidence.json"
python3 -I "$H/helper_evidence.py" "$HP/Ableton_AddOns" "$H/addons-strings.txt" "$H/addons-entries.txt" > "$H/addons-evidence.json"
python3 -I "$H/helper_evidence.py" "$HP/Ableton_Swapper" "$H/swapper-strings.txt" "$H/swapper-entries.txt" > "$H/swapper-evidence.json"
python3 -I - "$H" "$B" "$HP" <<'PY'
import hashlib, json, os, platform, sys, zipfile
h, b, hp = sys.argv[1:4]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
roots = ["App-Resources/Extensions", "App-Resources/Python/abl.webconnector", "App-Resources/Python/scripts",
         "App-Resources/Python/lib/opcode.pyc", "App-Resources/Misc/example_packs.json", "App-Resources/Misc/Splice"]
rows, skipped = [], 0
for r in roots:
    full = os.path.join(b, r)
    walk = [(os.path.dirname(full), [], [os.path.basename(full)])] if os.path.isfile(full) else os.walk(full)
    for d, dirs, files in walk:
        dirs.sort()
        for f in sorted(files):
            if f.startswith("._"):
                skipped += 1
                continue
            p = os.path.join(d, f)
            rows.append(f"{sha(p)}\t{os.path.getsize(p)}\t{os.path.relpath(p, b)}\n")
open(f"{h}/bundle-inventory.tsv", "w").write("".join(rows))
z = zipfile.ZipFile(f"{b}/App-Resources/Misc/Splice/SpliceAbletonLive_1.1.0_e0c725d.zip")
open(f"{h}/splice-zip-listing.tsv", "w").write(
    "".join(f"{i.file_size}\t{oct(i.external_attr >> 16)}\t{i.filename}\n" for i in z.infolist()))
helpers = {s: {"slice": json.load(open(f"{hp}/{s}/slice.json")),
               "coverage_counts": json.load(open(f"{hp}/{s}/corpus/decomp/coverage.json"))["counts"],
               "indexes_manifest_sha256": sha(f"{hp}/{s}/corpus/indexes/manifest.json")}
           for s in ("Ableton_Web_Connector", "Ableton_AddOns", "Ableton_Swapper")}
out = []
for d, dirs, files in os.walk(h):
    dirs.sort()
    out += [os.path.relpath(os.path.join(d, f), h) for f in sorted(files) if f != "manifest.json"]
m = {"id": "H6-WEB-V1", "packet": "H6 web connector, add-ons and swapper (FEAT-ECOSYSTEM, FEAT-DELIVERY)",
     "target": "Ableton Live 12 Suite 12.4.3", "bundle": b, "host": platform.platform(),
     "python": sys.version.split()[0], "command": "sh run.sh",
     "inputs": {"helpers": helpers, "live_binary_sha256": json.load(open(f"{h}/live-anchors.json"))["sha256"],
                "bundle_inventory": "bundle-inventory.tsv", "appledouble_skipped": skipped},
     "outputs": {f: {"sha256": sha(f"{h}/{f}"), "bytes": os.path.getsize(f"{h}/{f}")} for f in sorted(out)}}
json.dump(m, open(f"{h}/manifest.json", "w"), indent=1)
PY
