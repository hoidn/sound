"""Stdlib route/source integrity only; no original/model/tool imports or execution."""
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


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pointer(obj, path):
    for key in path.strip("/").split("/"):
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj


def validate(ledger, source, inputs, chains):
    rows = ledger["rows"]
    assert len(rows) == len({r["id"] for r in rows}) == len({r["observable"] for r in rows}) == 84
    counts = dict(collections.Counter(r["route"] for r in rows))
    counts.setdefault("X", 0)
    assert counts == ledger["counts"] == {"S": 53, "no-established-route": 31, "X": 0}
    assert ledger["denominator"] is None and ledger["whole_family_complete"] is False
    assert ledger["new_grade_count"] == 0
    ids = {f"REQ-PLUGIN-DISCOVERY-{n:03}" for n in range(1, 17)}
    assert {r["requirement"] for r in rows} == ids == set(inputs["requirement_ids"])
    cases = {c["id"]: c for c in inputs["draft_cases"]}
    assert len(cases) == 62 and sum(c["kind"] == "U" for c in cases.values()) == 6
    groups = set(source["evidence_groups"])
    spans = {s["id"] for s in source["owner_spans"]}
    for row in rows:
        assert row["evidence"] and set(row["evidence"]) <= groups
        assert row["owner_span"] in spans and row["premises_and_limits"]
        assert row["expected"] is row["actual"] is None and row["grade"] == "unchanged"
        for cid in row["case_navigation"]:
            assert cid in cases and row["requirement"] in cases[cid]["requirement_ids"], (row["id"], cid)
        if row["route"] == "no-established-route":
            assert row["missing_join"]
        if row["requirement"][-3:] in {"012", "013", "014", "015"}:
            assert row["route"] == "no-established-route", "U-only requirement promoted"
    sources = {s["id"]: s for s in source["retained_sources"]}
    assert len(sources) == 44
    assert sum(s["domain"] == "Ableton_Plugin_Scanner.arm64" for s in sources.values()) == 32
    for sid, s in sources.items():
        assert s["domain"] == ("Live.arm64" if sid.startswith("LIVE-") else "Ableton_Plugin_Scanner.arm64")
    for group in source["evidence_groups"].values():
        assert set(group["sources"]) <= set(sources) and set(group["text"]) <= spans
    assert len(source["historical_unretained_pointers"]) == 14
    assert all(x["entry"] not in {s["entry"] for s in sources.values()} for x in source["historical_unretained_pointers"])
    assert inputs["batch_selection"]["enumerated_X_batch"] == []
    assert inputs["new_expectations"] == inputs["new_grades"] == inputs["batch_selection"]["new_calls"] == 0
    assert chains["main_indirect_inventory"] == {"resolved_exported_sites": 25071, "sites": 268015, "unchanged": True, "new_resolution_credit": 0}
    assert chains["fresh_traversal"] is False
    assert chains["address_domains"] == ["Live.arm64", "Ableton_Plugin_Scanner.arm64"]
    assert len(chains["edges"]) == 14 and len(chains["unknown_bridges"]) == 9
    refs = groups | spans | {s["id"] for s in source["c_expression_spans"]}
    for edge in chains["edges"]:
        assert edge["evidence"] and set(edge["evidence"]) <= refs
        assert edge["native_call_pc"] is None and edge["new_indirect_resolution_credit"] == 0
    assert all(g["status"] == "unknown" and g["missing_join"] for g in chains["unknown_bridges"])


def source_check(source):
    for s in source["owner_spans"]:
        raw = (ROOT / s["path"]).read_bytes()
        block = raw[s["byte_start"]:s["byte_end_exclusive"]]
        assert sha(block) == s["sha256"] and len(block) == s["bytes"]
        assert raw[:s["byte_start"]].count(b"\n") + 1 == s["line_start"]
    for s in source["retained_sources"]:
        raw = (ROOT / s["path"]).read_bytes()
        assert sha(raw) == s["sha256"] and len(raw) == s["bytes"]
    byid = {s["id"]: s for s in source["retained_sources"]}
    assert len(source["c_expression_spans"]) == 21
    for s in source["c_expression_spans"]:
        raw = (ROOT / byid[s["source"]]["path"]).read_bytes()
        block = raw[s["byte_start"]:s["byte_end_exclusive"]]
        assert sha(block) == s["sha256"] and s["needle"].encode() in block
        assert raw[:s["byte_start"]].count(b"\n") + 1 == s["line_start"]
    assert len(source["historical_table_pointers"]) == 6
    for s in source["historical_table_pointers"]:
        assert pointer(json.loads((ROOT / s["path"]).read_text()), s["json_pointer"]) == s["value"]
        assert s["domain"] == "Ableton_Plugin_Scanner.arm64"


ledger, source, inputs, chains = [read(name) for name in ("route-ledger.json", "source-map.json", "input-sets.json", "chain-edges.json")]
pins = read("pins.json")
for pin in pins["files"]:
    raw = (ROOT / pin["path"]).read_bytes()
    assert sha(raw) == pin["sha256"] and len(raw) == pin["bytes"]
prefix = pins["research_prefix"]
assert sha((ROOT / prefix["path"]).read_bytes()[:prefix["bytes"]]) == prefix["sha256"]
validate(ledger, source, inputs, chains)
source_check(source)
# Check only selected retained payload identities against old manifests, not their full universes.
h1 = ROOT / "analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1"
hm = json.loads((h1 / "manifest.json").read_text())
n4 = ROOT / "analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1"
nm = {f["path"]: f for f in json.loads((n4 / "manifest.json").read_text())["files"]}
checked = 0
for pin in pins["files"]:
    path = ROOT / pin["path"]
    old = None
    if path.is_relative_to(h1):
        old = hm["files"].get(str(path.relative_to(h1)))
    if path.is_relative_to(n4):
        old = nm.get(str(path.relative_to(n4)))
    if old:
        assert old["bytes"] == pin["bytes"] and old["sha256"] == pin["sha256"]
        checked += 1
owner = (ROOT / "wiki/specs/plugin-discovery.md").read_bytes()
for c in inputs["draft_cases"]:
    raw = owner[c["byte_start"]:c["byte_start"] + c["bytes"]]
    assert sha(raw) == c["sha256"] and raw.startswith(("| " + c["id"] + " |").encode())
release = json.loads((ROOT / inputs["released_case_source"]).read_text())["cases"]
assert len(release) == 35 and [c["id"] for c in release] == [c["id"] for c in inputs["released_cases"]]
assert all(c["reference_execution"] == c["candidate_execution"] == "not-run" for c in release)
controls = []


def reject(name, mutate, integrity=False):
    l, s, i, c = [copy.deepcopy(x) for x in (ledger, source, inputs, chains)]
    mutate(l, s, i, c)
    try:
        source_check(s) if integrity else validate(l, s, i, c)
    except (AssertionError, KeyError):
        controls.append({"name": name, "status": "rejected"})
    else:
        raise AssertionError("Accepted negative control: " + name)


def promote_u(l, s, i, c):
    l["rows"][0].update(route="no-established-route", missing_join="synthetic control context")
    next(r for r in l["rows"] if r["requirement"].endswith("012"))["route"] = "S"


reject("U crash derivation promoted with unchanged aggregate counts", promote_u)
reject("own model given X route", lambda l,s,i,c: l["rows"][0].update(route="X"))
reject("duplicate predicate id", lambda l,s,i,c: l["rows"][1].update(id=l["rows"][0]["id"]))
reject("missing requirement context", lambda l,s,i,c: l.update(rows=[r for r in l["rows"] if not r["requirement"].endswith("015")]))
reject("dangling evidence group", lambda l,s,i,c: l["rows"][0].update(evidence=["not-retained"]))
reject("fabricated actual result", lambda l,s,i,c: l["rows"][0].update(actual="pass"))
reject("wrong case navigation requirement", lambda l,s,i,c: l["rows"][0].update(case_navigation=["PD-040"]))
reject("helper source conflated with main image", lambda l,s,i,c: s["retained_sources"][0].update(domain="Live.arm64"))
reject("historical source made newly resolved indirect credit", lambda l,s,i,c: c["main_indirect_inventory"].update(new_resolution_credit=1))
reject("function entry invented as call PC", lambda l,s,i,c: c["edges"][0].update(native_call_pc="0x10035e3fc"))
reject("retained expression span tampered", lambda l,s,i,c: s["c_expression_spans"][0].update(sha256="0"*64), True)
reject("vtable field substituted for public route", lambda l,s,i,c: s["historical_table_pointers"][0].update(value="0x1005a87f0"), True)
links = []
for md in HERE.glob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        f = target.split("#", 1)[0]
        assert f and (md.parent / f).is_file(), (md.name, target)
        links.append({"file": md.name, "target": target})
for file in HERE.iterdir():
    if file.suffix in {".md", ".py", ".json"}:
        assert not any(line.rstrip() != line for line in file.read_text().splitlines()), file
report = {"status": "pass-author-data-only-integrity-independent-structure-review-pending",
    "predicate_rows": 84, "route_counts": ledger["counts"], "current_requirement_ids": 16,
    "input_units": inputs["units"], "retained_C_sources": 44, "source_text_spans": 28,
    "C_expression_spans": 21, "historical_vtable_pointers": 6, "unretained_pointers": 14,
    "source_files_pinned": len(pins["files"]), "selected_old_manifest_payloads_checked": checked,
    "qualified_relationships": 14, "unknown_bridges": 9, "negative_controls": controls,
    "local_links": links, "protected_research_prefix": True,
    "U_only_requirements_012_through_015_preserved": True,
    "new_original_calls": 0, "new_native_provider_binary_reads": 0,
    "new_modules_models_comparators_builds_or_fixtures_run": 0, "new_grades": 0,
    "limits": "Bounded route inventory, not a family/product outcome denominator or compatibility pass. Hash/source checks do not execute scanner, module, SQL or application behavior; no old scripts imported. Parent manifest/atlas/review/shared routing pending."}
(HERE / "author-check.json").write_text(json.dumps(report, indent=2) + "\n")
