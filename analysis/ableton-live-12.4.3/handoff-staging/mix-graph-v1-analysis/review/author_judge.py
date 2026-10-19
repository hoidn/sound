import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import build_mg1 as B
pkg = Path(sys.argv[2])
cases = json.loads((pkg / "cases.json").read_text())["cases"]
out = {}
for c in cases:
    out[c["id"]] = B.judge_computation(c) if c["kind"] == "computation" else B.judge_render(c, (pkg / c["input"]).read_bytes())
print(json.dumps({"cases": len(cases), "problems": {k: v for k, v in out.items() if v}, "excluded_probes": B.excluded_probes(),
                  "structure_failing": {k: v for k, v in B.structure_checks(cases).items() if v["schema_deviations"] or v["refusals"] or v["unknown_shapes"]}}, indent=1))
