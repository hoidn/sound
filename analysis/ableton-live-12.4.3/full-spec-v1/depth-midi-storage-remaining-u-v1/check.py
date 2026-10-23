"""Data integrity only; never imports or executes source, models or native tooling."""
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(name):
    return json.loads((HERE / name).read_text())


def block(path, start, size):
    p = Path(path)
    p = p if p.is_absolute() else ROOT / p
    with p.open("rb") as f:
        f.seek(start)
        return f.read(size)


def validate_questions(q):
    rows = q["questions"]
    assert len(rows) == 11 and len({r["id"] for r in rows}) == 11
    assert {r["id"] for r in rows} == {"MNS-011", "MNS-024", "MNS-034", "MNS-035", "MNS-037", "MNS-038", "MNS-053", "MNS-060", "GROUP-FINAL-SAVE", "GROUP-MISSING-NOTE-LATER", "GROUP-WHOLE-LOAD-COUNTER"}
    for r in rows:
        assert r["local_source_answer"] and r["proposal"] and r["remaining_frontier"]
        assert r["owner_case_status"] == "unchanged"
        assert r["expected"] is r["actual"] is None and r["new_grade_count"] == 0
        assert r["public_open_save_error_success"] is False
    unsafe = next(r for r in rows if r["id"] == "MNS-037")
    assert unsafe["scope"] == "excluded-zero-required-safe-refusal-outcomes"
    assert unsafe["required_safe_refusal_outcomes"] == 0
    assert q["units"] == {"existing_U_case_ids": 8, "retained_partial_group_questions": 3, "bounded_questions": 11, "new_case_ids": 0, "new_expected_outputs": 0, "new_original_calls": 0, "new_grades": 0}


def validate_sources(loc):
    rows = {}
    for r in loc["reused_records"]:
        raw = block(r["path"], r["byte_start"], r["bytes"])
        assert sha(raw) == r["raw_sha256"]
        obj = json.loads(raw)
        obj = obj["record"] if r["record_pointer"] else obj
        assert obj["entry"] == r["entry"] and obj["code_sha256"] == r["code_sha256"]
        assert obj["body_bytes"] == r["body_bytes"] and obj["body_ranges"] == r["body_ranges"]
        assert sha(obj["code"].encode()) == r["code_sha256"]
        rows[obj["entry"]] = obj
    assert len(rows) == 25
    new = (HERE / "new-source-rows.jsonl").read_bytes()
    for r in loc["new_records"]:
        raw = new[r["retained_byte_start"]:r["retained_byte_start"] + r["retained_bytes"]]
        assert sha(raw) == r["raw_sha256"]
        assert raw == block(r["source_path"], r["source_byte_start"], r["source_bytes"])
        obj = json.loads(raw)
        assert obj["entry"] == r["entry"] and sha(obj["code"].encode()) == r["code_sha256"]
        assert obj["body_bytes"] == r["body_bytes"] and obj["body_ranges"] == r["body_ranges"]
        assert obj["partial_code"] is False
        rows[obj["entry"]] = obj
    assert len(loc["new_records"]) == 6 and len(rows) == 31
    assert rows["0x1025c6068"]["body_bytes"] == 4 and rows["0x1025c606c"]["body_bytes"] == 312
    for s in loc["c_spans"]:
        raw = rows[s["entry"]]["code"].encode()
        part = raw[s["byte_start"]:s["byte_end_exclusive"]]
        assert sha(part) == s["sha256"] and s["needle"].encode() in part
    assert len(loc["c_spans"]) == 25
    for c in loc["class_projections"]:
        raw = block(c["path"], c["byte_start"], c["bytes"])
        assert sha(raw) == c["raw_sha256"]
        obj = json.loads(raw)
        assert obj["address_point"] == c["address_point"] and obj["literal_type_encoding"] == c["type"]
        slots = {s["offset"]: s for s in obj["slots"]}
        assert all(slots[s["offset"]] == s for s in c["selected_slots"])
        assert c["new_resolution_credit"] == 0
    adapter = next(c for c in loc["class_projections"] if c["address_point"] == "0x1067decd8")
    assert {s["offset"]: s["target"] for s in adapter["selected_slots"]} == {0x2e8: "0x10256314c", 0x308: "0x1025c6068", 0x398: "0x1025654e8"}
    for name, key in [("call-rows.jsonl", "call_rows"), ("indirect-rows.jsonl", "indirect_rows")]:
        data = (HERE / name).read_bytes()
        for r in loc[key]:
            raw = data[r["retained_byte_start"]:r["retained_byte_start"] + r["bytes"]]
            assert sha(raw) == r["raw_sha256"]
            assert raw == block(r["source_path"], r["source_byte_start"], r["bytes"])
    calls = [json.loads(l) for l in (HERE / "call-rows.jsonl").read_text().splitlines()]
    assert len(calls) == 8 and calls[0]["caller"] == calls[0]["site"] == "0x1025c6068"
    assert calls[0]["kind"] == "tail-jump" and calls[0]["to"] == "0x1025c606c"
    for r in calls[1:]:
        assert r["caller"] == "0x1025c606c" and 0x1025c606c <= int(r["site"], 16) <= 0x1025c61a3
    indirect = [json.loads(l) for l in (HERE / "indirect-rows.jsonl").read_text().splitlines()]
    assert {r["site"] for r in indirect} == {"0x1025c6110", "0x1025c6148"}
    assert all(r["resolved_targets"] == [] for r in indirect)
    assert loc["new_indirect_credit"] == 0
    return rows


pins, loc, q = read("pins.json"), read("source-locators.json"), read("questions-and-proposals.json")
for pin in pins["files"]:
    raw = (ROOT / pin["path"]).read_bytes()
    assert sha(raw) == pin["sha256"] and len(raw) == pin["bytes"]
prefix = pins["research_prefix"]
assert sha((ROOT / prefix["path"]).read_bytes()[:prefix["bytes"]]) == prefix["sha256"]
for pin in {r["source_chunk"]: r["chunk_pin"] for r in loc["new_records"]}.values():
    raw = Path(pin["path"]).read_bytes()
    assert len(raw) == pin["bytes"] and sha(raw) == pin["sha256"]
validate_questions(q)
rows = validate_sources(loc)
assert all(set(r["evidence_entries"]) <= set(rows) for r in q["questions"])
controls = []


def reject(name, mutate, source=False):
    obj = copy.deepcopy(loc if source else q)
    mutate(obj)
    try:
        validate_sources(obj) if source else validate_questions(obj)
    except (AssertionError, KeyError):
        controls.append({"name": name, "status": "rejected"})
    else:
        raise AssertionError("Accepted negative control: " + name)


reject("dropped whole-batch question", lambda x: x["questions"].pop())
reject("unsafe MidiKey gets required safe refusal", lambda x: x["questions"][4].update(required_safe_refusal_outcomes=1))
reject("local duplicate Id turned into owner completion", lambda x: x["questions"][5].update(owner_case_status="resolved"))
reject("boundary source turned into event-array oracle", lambda x: x["questions"][6].update(expected="clipped"))
reject("counter comparator turned into public lifecycle proof", lambda x: x["questions"][-1].update(public_open_save_error_success=True))
reject("four-byte thunk treated as expanded implementation", lambda x: next(r for r in x["new_records"] if r["entry"] == "0x1025c6068").update(body_bytes=1317), True)
reject("changed conditional class slot", lambda x: x["class_projections"][1]["selected_slots"][0].update(target="0x1025c606c"), True)
reject("changed exact source span", lambda x: x["c_spans"][0].update(sha256="0" * 64), True)
links = []
for md in HERE.glob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        f = target.split("#", 1)[0]
        assert f and (md.parent / f).is_file()
        links.append(target)
for p in HERE.iterdir():
    if p.suffix in {".md", ".json", ".jsonl", ".py"}:
        assert not any(s.rstrip() != s for s in p.read_text().splitlines()), p
report = {"status": "pass-data-only-integrity-unreviewed-source-proposals", "bounded_questions": 11,
    "existing_U_cases": 8, "group_questions": 3, "reused_records": 25, "new_C1_projections": 6,
    "new_chunk_inputs": 2, "exact_C_spans": 25, "class_projections": 2,
    "call_rows": 8, "unresolved_indirect_rows": 2, "new_indirect_resolution_credit": 0,
    "unsafe_MidiKey_required_safe_refusal_outcomes": 0, "negative_controls": controls,
    "local_links": links, "new_original_calls": 0, "new_model_fixture_build_or_provider_runs": 0,
    "new_expectations_or_grades": 0, "research_prefix_preserved": True,
    "limits": "Source/proposals only; no owner/case/release change or application/compatibility pass. Conditional parser/list/class facts do not establish public lifecycle; body and transaction frontiers remain explicit."}
(HERE / "author-check.json").write_text(json.dumps(report, indent=2) + "\n")
