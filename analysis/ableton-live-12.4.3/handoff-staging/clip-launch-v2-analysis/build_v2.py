"""Stage the clip-launch-v2 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I:
  python3 -I build_v2.py build          # fixtures/, cases.json, draft manifest.json in ../clip-launch-v2/
  python3 -I build_v2.py seal           # all checks; manifest files[]; author-validation.json, traceability.json,
                                        # fixture-changes.json, fixture-audit-run.json
  python3 -I build_v2.py verify <dir>   # the same checks on an exported copy (no rewrite)
spec.md, README.md and AGENTS.md are hand-written. Fixtures come from fixtures_v2 (T11-MIN, no shipped bytes);
case records of 001-050 are copied from handoff/clip-launch-v1/cases.json; new cases from cases_v2.
"""
import hashlib, json, math, re, shutil, struct, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I does not add the script directory
import cases_v2 as C  # noqa: E402
import fixtures_v2 as F  # noqa: E402
import meta_v2 as M  # noqa: E402
import model_v2 as MD  # noqa: E402

b1 = MD.b1
HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / "clip-launch-v2"
V1 = F.REPO / "handoff/clip-launch-v1"
X2 = F.REPO / "analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1"
COMPARATOR = {**{k: v for k, v in b1.COMPARATOR.items()},
              "compute": "each listed result exact (binary64 equality); arguments as given"}
TEXT = (".md", ".json", ".xml")


def cid(n):
    return f"CLIP-LAUNCH-{n:03d}"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def v1_cases():
    return {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}


def doc_record(n, kind, reqs, purpose, action, expected):
    return {"id": cid(n), "kind": kind, "purpose": purpose, "requirements": [C.R + r for r in reqs],
            "input": f"fixtures/{cid(n)}.xml", "action": action, "expected": expected,
            "expectation_provenance": C.PROV_X, "reference_execution": "not-run", "candidate_execution": "not-run",
            "comparator": COMPARATOR[action]}


def val_record(n, reqs, purpose, comps):
    return {"id": cid(n), "kind": "value", "purpose": purpose, "requirements": [C.R + r for r in reqs],
            "input": None, "action": "compute",
            "expected": {"computations": [{k: c[k] for k in ("function", "arguments", "result", "basis")}
                                          for c in comps]},
            "expectation_provenance": C.PROV_X, "reference_execution": "not-run", "candidate_execution": "not-run",
            "comparator": COMPARATOR["compute"]}


def fixtures():
    """{n: (version, edits)} for every document case."""
    out = dict(C.CARRIED)
    out.update({n: (v, e) for n, _, _, _, v, e, _, _, _ in C.NEW_DOC})
    return out


def build():
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures/Samples").mkdir(parents=True)
    F.wav_bytes(STAGE / "fixtures/Samples/T11-tone.wav")
    for n, (version, edits) in fixtures().items():
        (STAGE / f"fixtures/{cid(n)}.xml").write_text(F.render(F.build_fixture(version, edits)))
    old = v1_cases()
    cases = [old[cid(n)] for n in sorted(C.CARRIED)]
    cases += [doc_record(n, k, r, p, a, e) for n, k, r, p, _, _, a, e, _ in C.NEW_DOC]
    cases += [val_record(n, r, p, comps) for n, r, p, comps in C.NEW_VAL]
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": "clip-launch-cases-v2", "target": M.TARGET,
        "scope": "clip-launch-v2 partial requirement clauses only (see spec.md)", "status": "released-reviewed",
        "fixture_origin": "Independently authored complete minimal Live Sets and a generated sample; no shipped file copied or excerpted",
        "oracle_status": "Static-derived and extracted-execution expectations (label per case); neither the reference application nor a candidate executed",
        "representation": {
            "paths": "relative to /Ableton/LiveSet; X[1] is the first child element named X",
            "values": "value held after opening; type by element name (see spec.md); binary32 compared after exact widening",
            "saved": "values: path -> value read back from the saved Value text; absent: paths; clip_order: clip path whose launch elements and follow-action children are checked for order",
            "computations": "compute cases: function, arguments and expected result of a value function of spec.md; basis names the provenance of each result",
            "note": "project comparison representation, not an API of the original application or a required design"},
        "cases": cases}, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(M.manifest_skeleton(len(cases)), indent=1) + "\n")
    print(len(cases), "cases staged")


# ---- X2 evidence ----
def x2():
    m = json.loads((X2 / "manifest.json").read_text())
    bad = [k for k, h in m["files"].items() if sha((X2 / k).read_bytes()) != h]
    launch, follow = (json.loads((X2 / f"results/{k}.json").read_text()) for k in ("launch", "follow"))
    return {"manifest_sha256": sha((X2 / "manifest.json").read_bytes()), "files_listed": len(m["files"]),
            "mismatches": bad,
            "grid": {(r["n"], r["d"], r["q"]): float.fromhex(r["x"]) for r in launch["grid"]},
            "getter": {r["stored"]: r["getter"] for r in launch["enum_getter"]},
            "boundary": {r["label"]: r for r in launch["boundary_cases"]},
            "sweep": {(r["q"], r["k"], r["step"]): r for r in launch["gridline_sweep"]},
            "chance": {r["label"]: r for r in follow["chances"]},
            "ft": {repr(r["input"]["v"]): r for r in follow["follow_time"] if r["flag"] == 1}}


def bits(x):
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def same(a, b):
    return bits(float(a)) == bits(float(b))


def xcheck(xr, comp):
    """Compare one computation (or document expectation) with the X2 records its xref names."""
    errs, args, res = [], comp.get("arguments", {}), comp.get("result", {})
    for tok in comp["xref"].split("|"):
        kind, _, key = tok.partition(":")
        if kind == "grid":
            n, d, q = map(int, key.split("/"))
            if not same(xr["grid"][(n, d, q)], res["grid"]):
                errs.append(f"{tok} {xr['grid'][(n, d, q)]} != {res['grid']}")
        elif kind == "getter":
            k = int(key)
            if xr["getter"][k] != (0 if k == -99 else k):
                errs.append(tok)
        elif kind in ("boundary", "sweep"):
            r = xr["boundary"][key] if kind == "boundary" else xr["sweep"][tuple(map(int, key.split("/")))]
            v = (lambda f: float.fromhex(r[f]["hex"])) if kind == "boundary" else (lambda f: float.fromhex(r[f]))
            ok = same(v("t"), args["beat"]) and same(v("t_lattice"), res["rounded_beat"])
            if args["grid"] != 0.0:
                ok &= same(v("B"), res["boundary"])
                if kind == "boundary":
                    ok &= same(v("g"), args["grid"]) and same(v("a"), args["anchor"])
            errs += [] if ok else [tok]
        elif kind == "chance":
            r = xr["chance"][key]
            a, b = comp["loaded"]
            ok = [x["v"] for x in r["loaded"]] == [b1.f32(a), b1.f32(b)] and r["held_after_postload"] == comp["held"]
            ok &= all(not math.copysign(1, x["v"]) < 0 or math.copysign(1, y) < 0 for x, y in zip(r["loaded"], (a, b)))
            errs += [] if ok else [tok]
        elif kind == "ft":
            errs += [] if same(xr["ft"][key]["held"]["v"], comp["held"]) else [tok]
    return errs


# ---- checks ----
def launch_content(root):
    """What a clip-launch case reads: envelope, set quantization, launch children of each clip, first scene FA."""
    ls = root.find("LiveSet")
    lc = {"root": dict(root.attrib), "set": [(c.tag, dict(c.attrib)) for c in ls if c.tag in (MD.GQ, MD.AQ)]}
    for p in (MD.SC, MD.SA, MD.AR):
        el = ls.find(p)
        if el is not None:
            lc[p] = [(c.tag, dict(c.attrib), [(g.tag, dict(g.attrib)) for g in c]) for c in el
                     if c.tag in MD.LAUNCH or c.tag in b1.OLD]
    sc = ls.find(MD.SN)
    if sc is not None:
        fa = sc.find("FollowAction")
        lc["scene"] = None if fa is None else [(g.tag, dict(g.attrib)) for g in fa]
    return lc


def check_doc(pkg, c, old, xr, out):
    errs, raw = [], (pkg / c["input"]).read_bytes()
    out["inputs"].add(raw)
    if not (raw.isascii() and b"\r" not in raw and raw.endswith(b"\n")):
        errs.append("format")
    root = ET.fromstring(raw)
    n = int(c["id"][-3:])
    version, edits = fixtures()[n]
    try:
        outcome, values, wide, saved = MD.model(raw.decode("ascii"))
        errs += b1.judge(c["expected"], outcome, values, wide, saved)
        out["mutants"] += bool(b1.judge(b1.mutate(c["expected"]), outcome, values, wide, saved))
    except MD.NoExpectation as e:
        errs.append(f"fixture hits an exclusion: {e}")
    base = F.base(version)
    if raw.decode() != F.render(F.apply(F.base(version), edits)):
        errs.append("fixture differs from base + listed edit")
    dev, r, ref, unk = F.measure(root)
    errs += [f"schema deviation {k}" for k in dev] + ref + unk
    edit_diff = F.diff(base, root)
    out["edits"][c["id"]] = edit_diff
    if c["expected"]["outcome"] == "refused":  # the case's edit is the only defect
        if MD.model(F.render(base))[0] != "opens" or not edit_diff:
            errs.append("refusal not isolated")
    if n <= 50:
        if c != old[c["id"]]:
            errs.append("record differs from clip-launch-v1")
        v1root = ET.parse(V1 / c["input"]).getroot()
        lv1, lv2 = launch_content(v1root), launch_content(root)
        kept = [k for k in lv1 if lv1[k] == lv2.get(k)]
        if kept != list(lv1):
            errs.append(f"launch content changed at {[k for k in lv1 if k not in kept]}")
        out["v1"][c["id"]] = {"kept": kept, "added_by_base": [k for k in lv2 if k not in lv1]}
    else:
        x = next(t for t in C.NEW_DOC if t[0] == n)
        v = c["expected"]["values"]
        if x[8].startswith("chance:"):
            fa = x[5][0][2]
            comp = {"xref": x[8], "loaded": [float(fa["FollowChanceA"]), float(fa["FollowChanceB"])],
                    "held": [v[MD.SC + "/FollowAction/FollowChanceA"], v[MD.SC + "/FollowAction/FollowChanceB"]]}
        else:
            comp = {"xref": x[8], "held": v[MD.SC + "/FollowAction/FollowTime"]}
        errs += xcheck(xr, comp)
    return errs


def check_val(c, xr, out):
    errs = []
    comps = next(t[3] for t in C.NEW_VAL if cid(t[0]) == c["id"])
    for got, src in zip(c["expected"]["computations"], comps):
        try:
            m = MD.compute(got["function"], got["arguments"])
        except MD.NoExpectation as e:
            errs.append(f"arguments hit an exclusion: {e}")
            continue
        if set(m) != set(got["result"]) or not all(same(m[k], got["result"][k]) for k in m):
            errs.append(f"model {m} != {got['result']}")
        errs += xcheck(xr, {**got, "xref": src["xref"]})
        if any(got[k] != src[k] for k in ("function", "arguments", "result", "basis")):
            errs.append("payload computation differs from cases_v2")
    first = c["expected"]["computations"][0]
    k = next(iter(first["result"]))
    m = MD.compute(first["function"], first["arguments"])
    out["mutants"] += not same(m[k], first["result"][k] * 2 + 1)
    return errs


def scan_deny(pkg, files):
    deny = {}
    for p in [*files, pkg / "manifest.json"]:
        if p.suffix not in TEXT:
            continue
        text = p.read_text()
        hits = sorted({m for pat in b1.DENY + M.DENY_EXTRA for m in re.findall(pat, text)})
        allowed = {"AGENTS.md": ("decompil",)}.get(p.name, ("Remoteable",) if p.suffix == ".xml" else ())
        hits = [h for h in hits if not h.startswith(allowed)] if allowed else hits
        if p.suffix == ".xml":  # the only allowed fixture hit is the element name RemoteableTimeSignature
            hits += [] if set(re.findall(r"Remoteable\w*", text)) <= {"RemoteableTimeSignature"} else ["Remoteable*"]
        if hits:
            deny[str(p.relative_to(pkg))] = hits
    return deny


def check(pkg, rewrite):
    pkg = pkg.resolve()
    doc = json.loads((pkg / "cases.json").read_text())
    old, xr = v1_cases(), x2()
    out = {"inputs": set(), "mutants": 0, "edits": {}, "v1": {}}
    problems = {}
    for c in doc["cases"]:
        errs = check_doc(pkg, c, old, xr, out) if c["input"] else check_val(c, xr, out)
        if errs:
            problems[c["id"]] = errs
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()),
                              "bytes": p.stat().st_size} for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}
    wav = pkg / "fixtures/Samples/T11-tone.wav"
    return {
        "cases": len(doc["cases"]), "manifest_case_count": manifest["case_count"], "case_problems": problems,
        "mutations_detected": f"{out['mutants']}/{len(doc['cases'])}", "distinct_fixture_inputs": len(out["inputs"]),
        "document_cases": sum(1 for c in doc["cases"] if c["input"]),
        "value_cases": sum(1 for c in doc["cases"] if not c["input"]),
        "carried_records_identical_to_v1": sum(1 for c in doc["cases"] if c["id"] in old and c == old[c["id"]]),
        "sample_matches_t11": sha(wav.read_bytes()) == sha(F.wav_bytes()),
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(b1.links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in b1.links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in b1.links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in doc["cases"] if c["input"] and not (pkg / c["input"]).is_file()],
        "deny_list_hits": scan_deny(pkg, files),
        "x2_evidence": {k: xr[k] for k in ("manifest_sha256", "files_listed", "mismatches")},
        "limits": "Authored consistency only: no reference or candidate executed; the model restates the same static "
                  "and X evidence and is not an oracle.", "_edits": out["edits"], "_v1": out["v1"]}


def audit_run():
    """Run t11-structure-v1/fixture_audit.py unchanged on a copy laid out like handoff/."""
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(STAGE, Path(td) / "clip-launch-v2")
        res = subprocess.run([sys.executable, "-I", "-B", str(F.T11 / "fixture_audit.py"),
                              str(F.SCHEMA_DIR / "12.0_12402.txt"), td, str(Path(td) / "a.json")],
                             capture_output=True, text=True, check=True)
        a = json.loads((Path(td) / "a.json").read_text())["releases"][0]
    unk = {e["fixture"]: e["unknown_shapes"] for e in a["fixtures"] if e.get("unknown_shapes")}
    return {"command": "fixture_audit.py <12.0_12402 schema> <copy> <out>", "stdout": res.stdout.strip(),
            "summary": a["summary"], "unknown_shapes_by_fixture": unk,
            "note": "the tool measures every document with the 12.0_12402 names; 11.0_405 fixtures store scenes in "
                    "SceneNames, which a conversion step renames Scenes, so it reports slots without scenes for "
                    "them; fixtures_v2.measure applies that rename and finds no unknown shape"}


def seal():
    rep = check(STAGE, rewrite=True)
    edits, v1map = rep.pop("_edits"), rep.pop("_v1")
    rep = {"schema": "author-validation-v1", "package": "clip-launch-v2 (staged candidate)",
           "python": sys.version.split()[0], **rep}
    (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1) + "\n")
    (HERE / "fixture-audit-run.json").write_text(json.dumps(audit_run(), indent=1) + "\n")
    changes = {"base_forms": {v: (F.base(v), F.FORM_NOTES[v])[1] for v in (F.V12402, F.V12117, F.V405)},
               "fixtures": {k: {"version": fixtures()[int(k[-3:])][0], "edits_from_base": e, **v1map.get(k, {})}
                            for k, e in edits.items()}}
    (HERE / "fixture-changes.json").write_text(json.dumps(changes, indent=1) + "\n")
    trace = {"schema": "clip-launch-v2-traceability-v1", "spec": "SPEC-CLIP-LAUNCH r4", "evidence": M.E,
             "assumptions": M.A, "x2_manifest_sha256": rep["x2_evidence"]["manifest_sha256"], "cases": {},
             "parent_cases_not_released": M.NOT_RELEASED}
    for n in sorted(C.CARRIED):
        reqs = [r[-3:] for r in v1_cases()[cid(n)]["requirements"]]
        trace["cases"][cid(n)] = {"source": f"clip-launch-v1 {cid(n)} (record identical; fixture rebuilt)",
                                  "evidence": sorted({k for r in reqs for k in M.EV[r]} | {"structure"}),
                                  "assumptions": sorted({a for r in reqs for a in M.AS.get(r, [])})}
    for n, _, reqs, *_, xref in C.NEW_DOC:
        trace["cases"][cid(n)] = {"source": C.SPEC_CASE[n], "xref": xref, "evidence": sorted(
            {k for r in reqs for k in M.EV[r]} | {"structure"}), "assumptions": sorted(
            {a for r in reqs for a in M.AS.get(r, [])} | {"ARM"})}
    for n, reqs, _, comps in C.NEW_VAL:
        trace["cases"][cid(n)] = {"source": C.SPEC_CASE[n], "xrefs": [c["xref"] for c in comps],
                                  "evidence": sorted({k for r in reqs for k in M.EV[r]}), "assumptions": ["ARM"]}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: rep[k] for k in ("cases", "case_problems", "mutations_detected", "distinct_fixture_inputs",
                                          "carried_records_identical_to_v1", "payload_files", "hash_or_size_mismatches",
                                          "inventory_differences", "unresolved_links", "deny_list_hits",
                                          "x2_evidence", "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        seal()
    else:
        r = check(Path(sys.argv[2]), rewrite=False)
        r.pop("_edits"), r.pop("_v1")
        print(json.dumps(r, indent=1))
