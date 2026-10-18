"""Compare persistent member registrations (corpus records of the AClip, AFollowAction and ASong
registries) with shipped schema field order. Registrations whose flag word is 3 (CONCAT44(3,..) or
0x300000000) are runtime-only and skipped. The m/mp prefix is stripped. Output is data.
usage: python3 -I check_registry_order.py <corpus-excerpts.jsonl> <Schema/12.0_12402.txt>
Checks: AClip registrations == AudioClip/MidiClip fields after `Time` (prefix);
AFollowAction == FollowAction (exact); ASong launch members appear in LiveSet order."""
import json, re, sys
import xml.etree.ElementTree as ET

REG = {"AClip": "0x102435a28", "AFollowAction": "0x1025037a4", "ASong": "0x10266c21c"}


def persistent(code):
    calls = [" ".join(c.split()) for c in re.findall(r"FUN_10147e954\((.*?)\);", code, re.S)]
    return [re.search(r'L"m?p?([A-Z]\w*)"', c).group(1) for c in calls
            if not re.search(r"CONCAT44\(3,|0x300000000", c)]


codes = {}
for line in open(sys.argv[1]):
    r = json.loads(line)["record"]
    codes[r["entry"]] = r["code"]
schema = ET.parse(sys.argv[2]).getroot()
fields = {c: [f.tag for f in schema.find(c)] for c in ("AudioClip", "MidiClip", "FollowAction", "LiveSet")}
clip = persistent(codes[REG["AClip"]])
fa = persistent(codes[REG["AFollowAction"]])
song = persistent(codes[REG["ASong"]])
ok = []
for c in ("AudioClip", "MidiClip"):
    seg = fields[c][1:1 + len(clip)]
    ok.append(seg == clip)
    print(f"AClip {len(clip)} persistent vs {c} fields[1:{1 + len(clip)}]: identical={seg == clip}")
ok.append(fa == fields["FollowAction"])
print(f"AFollowAction {len(fa)} persistent vs FollowAction {len(fields['FollowAction'])}: identical={ok[-1]}")
launch = [m for m in song if m in ("GlobalQuantisation", "GlobalQuantisationKeyMidi", "AutoQuantisation")]
pos = [fields["LiveSet"].index(m) for m in launch]
ok.append(launch == ["GlobalQuantisation", "GlobalQuantisationKeyMidi", "AutoQuantisation"] and pos == sorted(pos))
print(f"ASong launch members {launch} at LiveSet positions {pos}: in order={ok[-1]}")
sys.exit(0 if all(ok) else 1)
