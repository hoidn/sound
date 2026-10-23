#!/usr/bin/env python3
"""Read-only, stdlib documentary checks. Never execute recovered code or old helpers."""
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read_json(path):
    return json.loads(path.read_text())


def ident(data):
    if isinstance(data, str):
        data = data.encode()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def require(value, message):
    if not value:
        raise AssertionError(message)


def requirements(text):
    matches = list(re.finditer(r"^### (REQ-MIDI-NOTE-STORAGE-\d{3})[^\n]*\n(.*?)(?=^#{2,3} |\Z)", text, re.M | re.S))
    require(len(matches) == len({m.group(1) for m in matches}), "duplicate requirement")
    return {m.group(1): m.group(2) for m in matches}


def cases(text):
    matches = list(re.finditer(r"^\| (MNS-\d{3}) \|.*$", text, re.M))
    require(len(matches) == len({m.group(1) for m in matches}), "duplicate case")
    return {m.group(1): m.group(0) for m in matches}


def apply_patch(text, patch, reverse=False):
    """Apply this packet's ordinary newline-terminated unified diff in memory."""
    lines = text.splitlines(keepends=True)
    diff = patch.splitlines(keepends=True)
    require(diff[:2] == ["--- a/wiki/specs/midi-note-storage.md\n", "+++ b/wiki/specs/midi-note-storage.md\n"], "patch target")
    output, cursor, i = [], 0, 2
    while i < len(diff):
        header = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n", diff[i])
        require(header is not None, "patch hunk header")
        oldstart, oldcount, newstart, newcount = header.groups()
        oldstart, oldcount = int(oldstart), int(oldcount or 1)
        newstart, newcount = int(newstart), int(newcount or 1)
        i += 1
        old, new = [], []
        while i < len(diff) and not diff[i].startswith("@@ "):
            row = diff[i]
            require(row[:1] in [" ", "-", "+"], "patch row marker")
            if row[0] != "+":
                old.append(row[1:])
            if row[0] != "-":
                new.append(row[1:])
            i += 1
        require(len(old) == oldcount and len(new) == newcount, "patch hunk counts")
        if reverse:
            old, new, oldstart, oldcount = new, old, newstart, newcount
        pos = oldstart - 1 if oldcount else oldstart
        require(pos >= cursor and lines[pos:pos + len(old)] == old, "patch exact context")
        output.extend(lines[cursor:pos])
        output.extend(new)
        cursor = pos + len(old)
    output.extend(lines[cursor:])
    return "".join(output)


def check_semantics(text, route, before, after):
    req = requirements(text)
    rows = cases(text)
    require(list(req) == list(before["requirements_before"]), "requirement IDs/order")
    require(list(rows) == after["case_ids_after"], "case IDs/order")
    require(set(rows) == {f"MNS-{i:03}" for i in range(1, 78)}, "only two new IDs")
    for key, value in before["cases_before"].items():
        require(ident(rows[key]) == value, "changed original case " + key)
    changed = [key for key, value in before["requirements_before"].items() if ident(req[key]) != value]
    require(changed == before["permitted_requirement_changes"], "only 002/012/014 changed")
    require([r["id"] for r in route["dispositions"]] == ["MNS-011", "MNS-024", "MNS-034", "MNS-035", "MNS-037", "MNS-038", "MNS-053", "MNS-060", "GROUP-FINAL-SAVE", "GROUP-MISSING-NOTE-LATER", "GROUP-WHOLE-LOAD-COUNTER"], "whole eleven-question set")
    require(all(r["original_public_expectation"] is None for r in route["dispositions"]), "public outcome promoted")
    unsafe = next(r for r in route["dispositions"] if r["id"] == "MNS-037")
    require(unsafe["required_safe_refusal_outcomes"] == 0, "unsafe refusal manufactured")
    require(route["units"] == {"existing_U_case_questions": 8, "retained_group_questions": 3, "new_local_case_ids": 2, "public_U_resolutions": 0, "required_safe_refusal_outcomes_for_unsafe_keys": 0, "new_original_calls": 0, "new_resolved_indirect_sites": 0, "new_public_or_candidate_grades": 0, "new_fixtures": 0}, "unit/promotion error")
    require([r["id"] for r in route["new_local_cases"]] == ["MNS-076", "MNS-077"], "local cases")
    for row, original in zip(route["new_local_cases"], ["MNS-011", "MNS-038"]):
        require(row["existing_input_case"] == original, "local input source")
        require(row["input_setup_text"] == rows[original].split("|")[4].strip(), "invented local input")
        require(row["expected"] == {"local_reader_outcome": "refused"} and row["comparison"] == "local_reader_outcome", "local output broadened")
        require(row["public_expectation"] is None and row["saved_state_expected"] is None, "local/public promotion")
        require(row["requires_public_api"] is False and row["requires_native_call_or_pipeline"] is False and row["fixture_created"] is False, "API/pipeline/fixture invented")
        require(row["route"] == "S" and "ordinary reader context" in row["premises"] and "current field/class association conditional" in row["premises"] and "A3 where field type binding applies" in row["premises"], "dropped reader premise")
        require("Local reader refused" in rows[row["id"]] and "public load and saved" in rows[row["id"]], "new row scope")
    require(set(route["premise_separation"]) == {"A1", "A2", "A3"}, "assumption separation")
    require(route["status"] == "pending-independent-owner-review", "unreviewed adoption")


def main():
    before = read_json(HERE / "selection-and-preservation-before.json")
    after = read_json(HERE / "owner-after-and-preservation.json")
    route = read_json(HERE / "route-delta.json")
    current = (ROOT / after["owner"]["path"]).read_bytes()
    frozen = current[:after["owner"]["bytes"]]
    require(ident(frozen) == {k: after["owner"][k] for k in ["bytes", "sha256"]}, "owner frozen prefix")
    text = frozen.decode()
    patch = (HERE / "owner-delta.patch").read_text()
    predecessor = apply_patch(text, patch, reverse=True)
    require(ident(predecessor) == {k: before["owner_before"][k] for k in ["bytes", "sha256"]}, "reverse predecessor identity")
    require(apply_patch(predecessor, patch) == text, "forward exact delta")
    for key, value in requirements(predecessor).items():
        require(ident(value) == before["requirements_before"][key], "predecessor requirement ledger")
    for key, value in cases(predecessor).items():
        require(ident(value) == before["cases_before"][key], "predecessor case ledger")
    check_semantics(text, route, before, after)
    for key, value in requirements(text).items():
        require(ident(value) == after["requirements_after"][key], "after requirement identity")
    for key, value in after["new_cases_after"].items():
        require(ident(cases(text)[key]) == value, "new case identity")
    x_pattern = r"^- \*\*X[^\n]*(?:\n(?!- ).*)*"
    require(re.findall(x_pattern, predecessor.split("## Timing and state")[0], re.M) == re.findall(x_pattern, text.split("## Timing and state")[0], re.M), "changed X clause")
    prefix = before["research_prefix"]
    require(ident((ROOT / prefix["path"]).read_bytes()[:prefix["bytes"]]) == {k: prefix[k] for k in ["bytes", "sha256"]}, "changed research prefix")
    for item in before["predecessors"]:
        require(ident((ROOT / item["path"]).read_bytes()) == {k: item[k] for k in ["bytes", "sha256"]}, "predecessor pin " + item["path"])
    source = HERE.parent / "depth-midi-storage-remaining-u-v1"
    source_manifest = read_json(source / "manifest.json")
    for item in source_manifest["files"]:
        require(ident((source / item["path"]).read_bytes()) == {k: item[k] for k in ["bytes", "sha256"]}, "source payload " + item["path"])
    review = read_json(HERE.parent / "reviews/depth-midi-storage-remaining-u-v1-review.json")
    require(review["disposition"] == "approved-bounded-source-proposals" and review["findings"] == [], "source approval")
    require(review["packet"]["sha256"] == before["predecessors"][0]["sha256"], "reviewed source identity")
    question_ids = [r["id"] for r in read_json(source / "questions-and-proposals.json")["questions"]]
    require(question_ids == [r["id"] for r in route["dispositions"]], "source question identities")
    spans = {r["id"]: r for r in read_json(source / "source-locators.json")["c_spans"]}
    for row in route["dispositions"]:
        require(all(key in spans and spans[key]["entry"] in row["source_entries"] for key in row["source_span_ids"]), "source span identity")
    negatives = []
    def reject(name, document=text, delta=None, diff=None):
        try:
            if diff is not None:
                restored = apply_patch(document, diff, reverse=True)
                require(ident(restored) == {k: before["owner_before"][k] for k in ["bytes", "sha256"]}, "corrupt reverse delta")
            else:
                check_semantics(document, delta if delta is not None else route, before, after)
        except (AssertionError, KeyError):
            negatives.append({"name": name, "status": "rejected"})
            return
        raise AssertionError("negative not rejected: " + name)
    reject("public MNS011 refusal replaces original U", text.replace(cases(text)["MNS-011"], cases(text)["MNS-011"].replace("Unresolved; the static reading is refused", "Refused")))
    reject("public MNS038 load/savedIds promotion", text.replace(cases(text)["MNS-038"], cases(text)["MNS-038"].replace("Load outcome and saved Ids unresolved", "Refused")))
    reject("expression endpoint oracle", text.replace(cases(text)["MNS-053"], cases(text)["MNS-053"].replace("Unresolved;", "Saved event array;")))
    d = copy.deepcopy(route); next(r for r in d["dispositions"] if r["id"] == "MNS-037")["required_safe_refusal_outcomes"] = 1
    reject("unsafe key required safe refusal", delta=d)
    d = copy.deepcopy(route); d["dispositions"] = d["dispositions"][:-1]
    reject("omitted whole-load group-counter question", delta=d)
    d = copy.deepcopy(route); d["new_local_cases"][0]["expected"]["saved_notes"] = []
    reject("local comparison gains saved state", delta=d)
    d = copy.deepcopy(route); d["new_local_cases"][1]["requires_public_api"] = True
    reject("native/public validation pipeline required", delta=d)
    d = copy.deepcopy(route); d["new_local_cases"][1]["input_setup_text"] = 'Both KeyTracks Id="6"'
    reject("invented input fixture semantics", delta=d)
    d = copy.deepcopy(route); d["new_local_cases"][1]["premises"].remove("current field/class association conditional")
    reject("conditional class premise erased", delta=d)
    d = copy.deepcopy(route); next(r for r in d["dispositions"] if r["id"] == "GROUP-FINAL-SAVE")["original_public_expectation"] = "savedgroups"
    reject("group final Save promotion", delta=d)
    reject("unrelated requirement change", text.replace("128-slot map", "129-slot map", 1))
    reject("corrupted reversible patch", diff=patch.replace("+revision: 6", "+revision: 7", 1))
    # Check local Markdown links without following analyst sources into runtime execution.
    links = 0
    for path in [HERE / "README.md"]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            require((path.parent / target.split("#")[0]).resolve().exists(), "missing local link " + target)
            links += 1
    if (HERE / "manifest.json").exists():
        manifest = read_json(HERE / "manifest.json")
        require({i["path"] for i in manifest["files"]} == {f.name for f in HERE.iterdir() if f.is_file() and f.name != "manifest.json"}, "exact packet payload tree")
        for item in manifest["files"]:
            require(ident((HERE / item["path"]).read_bytes()) == {k: item[k] for k in ["bytes", "sha256"]}, "payload hash " + item["path"])
    print(json.dumps({"schema": "bounded-owner-documentary-check-v1", "status": "pass", "owner_revision": 6, "reversible_patch": "both directions exact", "requirement_ids": 17, "unchanged_requirement_bodies": 14, "unchanged_old_case_rows": 75, "public_U_case_rows_preserved": 8, "new_separately_scoped_local_case_ids": ["MNS-076", "MNS-077"], "whole_batch_questions": 11, "predecessor_pins": len(before["predecessors"]), "source_payloads_verified": len(source_manifest["files"]), "source_records_reexecuted": 0, "all_X_clauses_preserved": True, "research_prefix_preserved": True, "local_links_verified": links, "manifest_policy": "verify exact payload tree and hashes whenever manifest is present", "negative_controls": negatives, "new_original_calls": 0, "new_public_or_candidate_grades": 0, "required_safe_refusal_outcomes_for_unsafe_keys": 0, "limits": ["Read-only stdlib checks establish documentary integrity, not reference behavior.", "No binary/provider/native/decoder/harness/original/model/comparator/fixture/build or old-script execution.", "Source payload identities checked; source predecessor universes/main image not replayed.", "Owner review and release remain pending."]}, indent=2))


if __name__ == "__main__":
    main()
