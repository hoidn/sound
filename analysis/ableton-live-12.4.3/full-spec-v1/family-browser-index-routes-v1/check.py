"""Stdlib data-only route integrity and negative controls. No original/model imports."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    return json.loads((HERE / name).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate(ledger, source, inputs, chains):
    rows = ledger["rows"]
    assert len(rows) == 83 and len({r["id"] for r in rows}) == len(rows)
    assert set(r["route"] for r in rows) <= {"S", "X", "no-established-route"}
    actual = dict(collections.Counter(r["route"] for r in rows))
    actual.setdefault("X", 0)
    assert actual == ledger["counts"] == {"S": 35, "no-established-route": 48, "X": 0}
    assert ledger["denominator"] is None and ledger["whole_family_complete"] is False
    assert ledger["new_grade_count"] == 0
    reqs = {f"REQ-BROWSER-INDEX-{n:03}" for n in range(1, 14)}
    assert {r["requirement"] for r in rows if r["requirement"]} == reqs
    assert {r["context_section"] for r in rows if not r["requirement"]} == {"state", "lifecycle", "error"}
    assert set(inputs["requirement_ids"]) == reqs
    evidence = set(source["evidence_groups"])
    spans = {s["id"] for s in source["normative_spans"]}
    caseids = {c["id"] for c in inputs["draft_cases"]}
    for row in rows:
        assert row["evidence"] and set(row["evidence"]) <= evidence
        assert row["owner_span"] in spans
        assert row["premises_and_limits"]
        assert set(row["case_navigation"]) <= caseids
        assert row["expected"] is row["actual"] is None and row["grade"] == "unchanged"
        if row["route"] == "no-established-route":
            assert row["missing_join"]
    assert len(inputs["draft_cases"]) == 68
    assert {c["id"] for c in inputs["draft_cases"] if c["withdrawn"]} == {"BI-040", "BI-041"}
    assert len(inputs["released_cases"]) == 26
    assert inputs["batch_selection"]["enumerated_X_batch"] == []
    assert inputs["new_execution"] == inputs["new_expectations"] == 0
    records = {r["id"]: r for r in source["retained_records"]}
    assert len(records) == 48
    for r in records.values():
        assert r["domain"] == "Ableton_Index.arm64"
        assert r["partial_code"] is False and r["state"].startswith("exported")
    for group in source["evidence_groups"].values():
        assert set(group.get("records", [])) <= set(records)
    assert len(source["c_expression_spans"]) == 20
    assert next(s for s in source["c_expression_spans"] if s["id"] == "CEX-020")["needle"] == "FUN_1006dbf98(&local_208,&local_b8,uVar11,1)"
    assert chains["address_domains"] == ["Live.arm64", "Ableton_Index.arm64"]
    assert chains["main_indirect_inventory"] == {"resolved_exported_sites": 25071, "sites": 268015, "unchanged": True, "new_resolution_credit": 0}
    assert chains["fresh_traversal"] is False
    assert len(chains["edges"]) == 15 and len(chains["unknown_bridges"]) == 8
    erefs = evidence | {s["id"] for s in source["c_expression_spans"] + source["text_source_spans"]}
    for edge in chains["edges"]:
        assert set(edge["evidence"]) <= erefs
        assert edge["native_call_pc"] is None and edge["new_indirect_resolution_credit"] == 0
    assert all(g["status"] == "unknown" and g["missing_join"] for g in chains["unknown_bridges"])


def source_integrity(source):
    code = {}
    for r in source["retained_records"]:
        raw = (ROOT / r["path"]).read_bytes()[r["byte_start"]:r["byte_start"] + r["bytes"]]
        assert sha(raw) == r["raw_sha256"]
        obj = json.loads(raw)
        assert obj["entry"] == r["entry"] and obj["chunk"] == r["original_chunk"]
        c = obj["code"].encode()
        assert sha(c) == r["code_sha256"] == obj["code_sha256"]
        assert len(c) == r["code_bytes"] == obj["code_bytes"]
        assert obj["body_bytes"] == r["body_bytes"] and obj["body_ranges"] == r["body_ranges"]
        code[r["id"]] = c
    for s in source["c_expression_spans"]:
        block = code[s["record"]][s["code_byte_start"]:s["code_byte_end_exclusive"]]
        assert sha(block) == s["code_span_sha256"] and s["needle"].encode() in block
    for s in source["normative_spans"] + source["text_source_spans"]:
        raw = (ROOT / s["path"]).read_bytes()
        block = raw[s["byte_start"]:s["byte_end_exclusive"]]
        assert len(block) == s["bytes"] and sha(block) == s["sha256"]
        assert raw[:s["byte_start"]].count(b"\n") + 1 == s["line_start"]
    for s in source["sql_row_locators"]:
        raw = (ROOT / s["path"]).read_bytes()[s["byte_start"]:s["byte_start"] + s["bytes"]]
        assert sha(raw) == s["raw_sha256"] and json.loads(raw)["address"] == s["string_address"]


ledger, source, inputs, chains = [read(name) for name in ("route-ledger.json", "source-map.json", "input-sets.json", "chain-edges.json")]
pins = read("pins.json")
for pin in pins["files"]:
    data = (ROOT / pin["path"]).read_bytes()
    assert len(data) == pin["bytes"] and sha(data) == pin["sha256"]
prefix = pins["research_prefix"]
assert sha((ROOT / prefix["path"]).read_bytes()[:prefix["bytes"]]) == prefix["sha256"]
validate(ledger, source, inputs, chains)
source_integrity(source)
# Selected legacy records agree with their retained predecessor manifests, not a new capture.
d2 = ROOT / "analysis/ableton-live-12.4.3/r2/d2-browser-index-v1"
dm = json.loads((d2 / "manifest.json").read_text())
assert sha((d2 / "cited-functions.jsonl").read_bytes()) == dm["files"]["cited-functions.jsonl"]
h2 = ROOT / "analysis/ableton-live-12.4.3/r2/h2-index-v1"
hm = json.loads((h2 / "manifest.json").read_text())
for pin in pins["files"]:
    path = ROOT / pin["path"]
    if path.is_relative_to(h2) and str(path.relative_to(h2)) in hm["outputs"]:
        old = hm["outputs"][str(path.relative_to(h2))]
        assert old["sha256"] == pin["sha256"] and old["size"] == pin["bytes"]
nc = ROOT / "analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/results/n4-0003"
nm = json.loads((nc / "manifest.json").read_text())
for pin in pins["files"]:
    path = ROOT / pin["path"]
    if path.is_relative_to(nc) and str(path.relative_to(nc)) in nm["files"]:
        old = nm["files"][str(path.relative_to(nc))]
        assert old["sha256"] == pin["sha256"] and old["bytes"] == pin["bytes"]
owner = (ROOT / "wiki/specs/browser-index.md").read_bytes()
for c in inputs["draft_cases"]:
    block = owner[c["byte_start"]:c["byte_start"] + c["bytes"]]
    assert sha(block) == c["sha256"] and block.startswith(("| " + c["id"] + " |").encode())
release = json.loads((ROOT / inputs["released_case_source"]).read_text())["cases"]
assert [c["id"] for c in release] == [c["id"] for c in inputs["released_cases"]]
assert all(c["reference_execution"] == c["candidate_execution"] == "not-run" for c in release)
controls = []


def reject(name, mutation, source_check=False):
    l, s, i, c = [copy.deepcopy(x) for x in (ledger, source, inputs, chains)]
    mutation(l, s, i, c)
    try:
        source_integrity(s) if source_check else validate(l, s, i, c)
    except (AssertionError, KeyError):
        controls.append({"name": name, "status": "rejected"})
    else:
        raise AssertionError("negative control accepted: " + name)


reject("duplicate observable id", lambda l,s,i,c: l["rows"][1].update(id=l["rows"][0]["id"]))
reject("invented X route from own model", lambda l,s,i,c: l["rows"][0].update(route="X"))
reject("lost requirement context", lambda l,s,i,c: l.update(rows=[r for r in l["rows"] if r["requirement"] != "REQ-BROWSER-INDEX-012"]))
reject("dangling evidence", lambda l,s,i,c: l["rows"][0].update(evidence=["not-retained"]))
reject("fabricated actual/grade", lambda l,s,i,c: l["rows"][0].update(actual="pass", grade="S"))
reject("helper/main address conflation", lambda l,s,i,c: s["retained_records"][0].update(domain="Live.arm64"))
reject("invented native PC", lambda l,s,i,c: c["edges"][0].update(native_call_pc="0x1002b4b14"))
reject("new main resolved-site credit", lambda l,s,i,c: c["main_indirect_inventory"].update(new_resolution_credit=1))
reject("wrong folder-versus-pack apply expression", lambda l,s,i,c: s["c_expression_spans"][-1].update(needle="FUN_1006dbf98(&local_208,&local_b8,uVar11,0)"))
reject("tampered retained C locator", lambda l,s,i,c: s["c_expression_spans"][0].update(code_span_sha256="0"*64), source_check=True)
links = []
for md in HERE.glob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        f = target.split("#", 1)[0]
        assert f and (md.parent / f).is_file(), (md.name, target)
        links.append({"file": md.name, "target": target})
for path in HERE.iterdir():
    if path.suffix in {".md", ".py", ".json"}:
        assert not any(line.rstrip() != line for line in path.read_text().splitlines()), path
report = {"status": "pass-author-data-checks-independent-structure-review-pending", "predicate_rows": len(ledger["rows"]),
    "route_counts": ledger["counts"], "requirement_ids": 13, "retained_provider_records": 48,
    "c_expression_spans": 20, "source_review_text_spans": 11, "sql_row_locators": len(source["sql_row_locators"]),
    "source_files_pinned": len(pins["files"]), "source_spans": len(source["normative_spans"]),
    "negative_controls": controls, "input_units": inputs["units"], "relationships": 15, "unknown_bridges": 8,
    "local_links": links, "research_prefix_preserved": True, "new_original_calls": 0,
    "new_provider_or_native_reads": 0, "new_model_comparator_or_fixture_runs": 0, "new_grades": 0,
    "limits": "Bounded route inventory only; no complete family/product denominator or behavior/compatibility pass. Data-only selected-source integrity checks do not execute original functions, SQL, models or UI; main indirect baseline is unchanged. Parent atlas/manifest/review/shared routing remain separate."}
(HERE / "author-check.json").write_text(json.dumps(report, indent=2) + "\n")
