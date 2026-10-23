"""Read-only retained-source checks. Never executes recovered code."""
import copy
import hashlib
import json
from pathlib import Path
import sys

if sys.argv[1:] != ["--check"]:
    raise SystemExit("usage: check.py --check")

here = Path(__file__).resolve().parent
root = here.parents[3]
digest = lambda b: hashlib.sha256(b).hexdigest()
load = lambda n: json.loads((here / n).read_text())

for pin in load("pins.json"):
    raw = (root / pin["path"]).read_bytes()
    assert len(raw) == pin["bytes"] and digest(raw) == pin["sha256"]

rows = [json.loads(line) for line in (here / "source-rows.jsonl").read_bytes().splitlines()]
assert [r["entry"] for r in rows] == ["0x10256314c", "0x1025654e8"]
assert sum(len(r["code"].encode()) for r in rows) == 4966
locators = load("source-locators.json")["selected"]
for row, loc in zip(rows, locators, strict=True):
    assert row["entry"] == loc["entry"]
    raw = Path(loc["chunk"]).read_bytes()
    assert len(raw) == loc["chunk_bytes"] and digest(raw) == loc["chunk_sha256"]
    selected = raw[loc["offset"]:loc["offset"] + loc["raw_bytes"]]
    assert digest(selected) == loc["raw_sha256"] and json.loads(selected) == row
    assert digest(row["code"].encode()) == loc["code_sha256"] == row["code_sha256"]
    assert not row["partial_code"] and not row["timed_out"]

def validate(findings):
    assert findings["native_site_resolution_credit"] == 0
    outcomes = findings["outcome_dispositions"]
    assert [o["variant"] for o in outcomes] == list("abcd")
    for o in outcomes:
        assert o["existing_case"] == "MNS-053"
        assert o["required_public_result"] == "unknown"
        assert o["expected"] is None and o["actual"] is None and o["new_grade"] == 0
        assert len(o["missing_joins"]) == 4
    assert len(findings["selected_bodies"]) == 2
    for body, row in zip(findings["selected_bodies"], rows, strict=True):
        assert body["entry"] == row["entry"]
        assert body["native_body_bytes_metadata"] == row["body_bytes"]
        for span in body["spans"]:
            a, b = span["C_lines"]
            raw = "".join(row["code"].splitlines(keepends=True)[a - 1:b]).encode()
            assert len(raw) == span["C_span_bytes"] and digest(raw) == span["C_span_sha256"]

findings = load("findings.json")
validate(findings)
controls = []
for name in ["omitted variant", "invented expected", "invented grade", "indirect credit", "changed source span"]:
    bad = copy.deepcopy(findings)
    if name == "omitted variant": bad["outcome_dispositions"].pop()
    elif name == "invented expected": bad["outcome_dispositions"][0]["expected"] = []
    elif name == "invented grade": bad["outcome_dispositions"][1]["new_grade"] = 1
    elif name == "indirect credit": bad["native_site_resolution_credit"] = 2
    else: bad["selected_bodies"][0]["spans"][0]["C_span_sha256"] = "0" * 64
    try:
        validate(bad)
    except AssertionError:
        controls.append(name)
    else:
        raise AssertionError("false promotion accepted: " + name)
print(json.dumps({"status": "pass", "records": 2, "C_utf8_bytes": 4966,
                  "outcomes_still_unknown": 4, "negative_controls_rejected": controls,
                  "new_original_calls": 0, "new_grades": 0}, indent=2))
