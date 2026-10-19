"""Reviewer: the T11 checker (schema_check.check/rules and fixture_audit.measure/refusals/unknowns, imported unchanged)
on every set fixture of a package copy, with each case's expected outcome (analyst side; output is data).
usage: python3 -I -B t11_checker_summary.py <package dir>
LIVE-SET-STRUCTURE-014 (<NextPointeeId />) stops rules(); it is also measured as a probe copy with Value 67 restored."""
import copy, gzip, json, sys
import xml.etree.ElementTree as ET
from pathlib import Path

T11 = Path(__file__).resolve().parents[3] / "r2/t11-structure-v1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(T11))
import fixture_audit as fa  # noqa: E402
from schema_check import load_schema  # noqa: E402

SCHEMA = "/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt"
d = Path(sys.argv[1])
schema = load_schema(SCHEMA)
fa.LIVESET_ORDER[:] = list(schema["LiveSet"])
cases = json.loads((d / "cases.json").read_text())["cases"]
by_input = {}
for c in cases:
    by_input.setdefault(c["input"], []).append((c["id"], c["expected"].get("outcome")))
rows = {}
for p in sorted(d.glob("fixtures/*.als")):
    rel = str(p.relative_to(d))
    root = ET.fromstring(gzip.decompress(p.read_bytes()))
    row = {"cases": by_input.get(rel, [])}
    try:
        dev, r = fa.measure(schema, root)
    except TypeError as e:
        row["checker"] = f"stops: {e}"
        root = copy.deepcopy(root)
        root.find("LiveSet/NextPointeeId").set("Value", "67")
        dev, r = fa.measure(schema, root)
        row["probe"] = "Value 67 restored"
    row["refusals"] = fa.refusals(r, dev)
    row["unknown_shapes"] = fa.unknowns(r)
    row["deviations"] = sorted(dev)
    rows[rel] = row
print(json.dumps(rows, indent=1))
