"""Re-derive the case expectations from the retained extracted-execution results (analyst side; never shipped).

usage: python3 -I -B x_rederive.py
Reads x2-transport-v1 results (after checking their digests against that run's manifest) and, for every case
whose tested text or saved value the run covered, compares the run's result with the expectation. Also runs a
mutation test of review_checks.judge_case: every case with its expectation changed must be caught.
"""
import hashlib, json, struct, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import review_checks as rc  # noqa: E402

X2 = HERE.parents[2] / "r2/x2-transport-v1"
PKG = HERE.parents[1] / "transport-state-v3"
TESTED = {  # case -> (kind, tested text) as in the fixture
    "TS-001": ("bool", "true"), "TS-002": ("bool", "1"), "TS-003": ("bool", "0"), "TS-004": ("bool", "TRUE"),
    "TS-005": ("bool", ""), "TS-006": ("double", "4.5abc"), "TS-007": ("double", "abc"),
    "TS-008": ("float", "93.3333333"), "TS-009": ("int", "201.0"), "TS-010": ("int", " +201 "),
    "TS-020": ("float", "121.2"), "TS-021": ("double", "0.3"), "TS-024": ("double", "100.00000000000001"),
    "TS-025": ("double", "1000.0000000000001"), "TS-026": ("double", "0.09999999999999999"),
    "TS-027": ("double", "0.000001"), "TS-028": ("double", "-0"), "TS-029": ("int", "+201 "),
    "TS-030": ("int", "-0"), "TS-031": ("int", "2147483648"), "TS-032": ("int", "0" * 60 + "201 "),
    "TS-033": ("int", "-" + "0" * 63), "TS-034": ("double", " +4.5 "), "TS-035": ("double", "- 4.5"),
    "TS-036": ("double", "#4012000000000000"), "TS-037": ("float", "#42f00000"), "TS-022": ("double", "8"),
}


def main():
    man = json.loads((X2 / "manifest.json").read_text())
    bad = [f for f, h in man["files"].items() if hashlib.sha256((X2 / f).read_bytes()).hexdigest() != h]
    parse = json.loads((X2 / "results/parse.json").read_text())
    writer = json.loads((X2 / "results/writer.json").read_text())
    reads = {(x["kind"], x["text"]): x for x in parse["number_and_bool"] + parse["int"]}
    writes = {}
    for x in writer["attribute_writer_case_values"] + writer["attribute_writer_specials"]:
        writes.setdefault((x["kind"], x.get("x_bits") or x["x"]), x["writes"][0]["text"])
    cases = {c["id"]: c for c in json.loads((PKG / "cases.json").read_text())["cases"]}
    out = {"x2_files_mismatching_manifest": bad, "cases": {}}
    for cid, (kind, text) in TESTED.items():
        c, r = cases[cid], reads.get((kind, text))
        exp = c["expected"]
        row = {"provenance": c["expectation_provenance"].split(";")[0], "in_run": r is not None}
        if r is None:
            out["cases"][cid] = row
            continue
        row["run_result"] = r["result"]
        tested_refused = r["result"] == "refused"
        row["outcome_agrees"] = tested_refused == (exp["outcome"] == "refused")
        if not tested_refused and kind in ("double", "float"):
            bits = r.get("bits")
            v = struct.unpack(">d" if kind == "double" else ">f", bytes.fromhex(bits))[0]
            for k, ev in exp.get("state", {}).items():
                if k != "loop_on":
                    row[f"state_{k}_agrees"] = v == ev
            saved = list(exp.get("saved", {}).get("values", {}).values())
            if saved and cid != "TS-022":
                wbits = bits if kind == "double" else struct.pack(">d", v).hex()
                w = writes.get((kind, bits)) or writes.get((kind, wbits))
                row["saved_text_in_run"] = w
                row["saved_agrees"] = w == saved[0] if w is not None else None
        out["cases"][cid] = row
    # mutation test of the reviewer's own judge
    caught = 0
    for c in cases.values():
        m = json.loads(json.dumps(c))
        e = m["expected"]
        if e.get("saved", {}).get("values"):
            p = next(iter(e["saved"]["values"]))
            e["saved"]["values"][p] += "1"
        elif e.get("state"):
            k = next(iter(e["state"]))
            e["state"][k] = (not e["state"][k]) if isinstance(e["state"][k], bool) else e["state"][k] * 2 + 1
        elif e.get("saved", {}).get("absent"):
            e["saved"]["absent"] = ["Transport/LoopOn"]
        else:
            m["expected"] = {"outcome": "opens"} if e["outcome"] == "refused" else {"outcome": "refused"}
        caught += bool(rc.judge_case(m, (PKG / c["input"]).read_bytes())[0])
    out["mutations_caught"] = f"{caught}/{len(cases)}"
    rows = out["cases"].values()
    out["summary"] = {"cases_in_run": sum(r["in_run"] for r in rows),
                      "disagreements": [k for k, r in out["cases"].items()
                                        if any(v is False for kk, v in r.items() if kk.endswith("agrees"))]}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
