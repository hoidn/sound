"""Print a kept N7 dossier's disassembly with call targets. Usage: dis.py ENTRY [FROM [TO]]."""
import json, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[3] / "r2/n7-midi-transforms-v1/results"
entry = sys.argv[1]
path = next(root.glob(f"*/functions/{entry}.json"))
d = json.loads(path.read_text())
lo = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3], 16) if len(sys.argv) > 3 else 1 << 64
refs = {r["from"]: r.get("target", {}).get("symbol") for r in d["references_from_body"]}
print(path.relative_to(root))
for ins in d["disassembly"]:
    a = int(ins["address"], 16)
    if lo <= a <= hi:
        print(ins["address"], ins["text"], ("; " + str(refs[ins["address"]])) if ins["address"] in refs else "")
