"""Seal and verify the warp-markers-v2 candidate (analyst side). See build_v2.py for the run order.

  python3 -I check_v2.py seal           # after build: all checks, manifest files[], reports in this directory
  python3 -I check_v2.py verify <dir>   # an exported copy: hashes, inventory, links, case inputs, deny-list

seal writes author-validation.json, traceability.json and v1-to-v2-text.diff here, and through
fixture_checks.py schema-check.jsonl and fixture-audit.json (the T1.1 checkers, run unchanged). The cross-check model restates the released clauses (it shares the evidence and
is not an oracle); the X check compares deciding values with the retained X2 results. Read-only elsewhere.
"""
import difflib, json, math, re, sys, wave
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_v2 as B  # noqa: E402
from fixture_checks import fixture_report, single_change, structure_checks  # noqa: E402
from v2_meta import (ALLOWED_HITS, CLAUSES, DENY, E, I, PROV_X, PROV_XS, TRACE, V1, X2,  # noqa: E402
                     evidence_identity, sha)

ROOT, STAGE = B.ROOT, B.STAGE
NW, OOR, BL, BR, TEMPO, NOM, SH = ("not-warped", "sample-time-out-of-range", "beat-below-left-neighbour",
                                   "beat-above-right-neighbour", "segment-tempo-out-of-range", "no-such-marker",
                                   "shadow-marker")
ACC, REF = {"outcome": "accepted"}, {"outcome": "refused"}


class Refused(Exception):
    pass


class NoExpectation(Exception):
    pass


def no(reason):
    return {"outcome": "refused", "refusal_reason": reason}


# ---- loading: the released clauses REQ-001 to 004, 010 to 013 restated ----
PREFIX = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
INIT = {"GranularityTones": 30, "GranularityTexture": 65, "FluctuationTexture": 25, "TransientResolution": 6,
        "TransientLoopMode": 2, "ComplexProFormants": 100, "ComplexProEnvelope": 128}
RANGES = {"GranularityTones": (12, 100), "GranularityTexture": (2, 263), "FluctuationTexture": (0, 100),
          "ComplexProFormants": (0, 100), "ComplexProEnvelope": (8, 256), "WarpMode": {0, 1, 2, 3, 4, 6},
          "TransientResolution": set(range(7)), "TransientLoopMode": {0, 1, 2}}
WARP_TAGS = {"IsWarped", "WarpMode", *INIT}
CLIP_X = "/".join(B.CLIP_PATH[1:])
SWP_X = "Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/SampleParts/" \
        "MultiSamplePart/SampleWarpProperties"


def position(text):
    t = text.lstrip(" ")
    if re.match(r"[+-]?(0[xX]|inf|nan|#|Invalid)", t, re.I) or t[:1] in ("\t", "\n", "\r"):
        raise NoExpectation(f"number form {text!r}")
    m = PREFIX.match(t)
    if not m:
        raise Refused()
    v = float(m.group(0))
    if abs(v) > 1e6:
        raise NoExpectation("position outside scope limit")
    return v


def value(tag, text):
    if tag == "IsWarped":
        return {"true": True, "false": False}[text]
    if not re.fullmatch(r"0|[1-9][0-9]*", text):
        raise NoExpectation(f"setting text {text!r}")
    v, r = int(text), RANGES.get(tag)
    if r is not None and (v not in r if isinstance(r, set) else not r[0] <= v <= r[1]):
        raise NoExpectation(f"{tag} outside its codes or range")
    return v


def holder_state(holder, audio_clip):
    state = dict(INIT)
    for el in holder:
        if el.tag == "WarpMarkers":
            state["WarpMarkers"] = [[position(m.attrib["SecTime"]), position(m.attrib["BeatTime"])] for m in el]
        elif el.tag == "TransientEnvelope":
            if el.get("Value") != "100":
                raise NoExpectation("TransientEnvelope other than 100")
        elif el.tag in WARP_TAGS and "Value" in el.attrib:
            state[el.tag] = value(el.tag, el.attrib["Value"])
    ms = state["WarpMarkers"]
    if audio_clip and (len(ms) < 2 or any(a[0] >= b[0] or a[1] >= b[1] for a, b in zip(ms, ms[1:]))):
        raise NoExpectation("audio clip list not well formed")
    return state


def load(path):
    """Return (states by holder, sample length in s, sample rate in Hz); raise Refused for a refused document."""
    root = ET.fromstring(path.read_bytes())
    assert root.attrib == {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1"}
    ls = root.find("LiveSet")
    clip = ls.find(CLIP_X)
    assert len(list(ls.iter("AudioClip"))) == 1 and clip is not None
    states = {"AudioClip": holder_state(clip, True)}
    swp = ls.find(SWP_X)
    assert len(list(ls.iter("SampleWarpProperties"))) == (swp is not None)
    if swp is not None:
        states["SampleWarpProperties"] = holder_state(swp, False)
    sref = clip.find("SampleRef")
    with wave.open(str(path.parent / sref.find("FileRef/RelativePath").get("Value"))) as w:
        frames, rate = w.getnframes(), w.getframerate()
    assert (int(sref.find("DefaultDuration").get("Value")), int(sref.find("DefaultSampleRate").get("Value"))) == \
        (frames, rate)
    return states, frames / rate, float(rate)


# ---- the scripting clauses REQ-008, 015, 016: binary64 sequences ("x") and warp-markers-v1's exact rules ----
def grid_x(b):  # REQ-016 clause 1
    s = 1.0 if b >= 0 else -1.0
    y = abs(b + s * ((1 / 3843840) * 0.5)) * 3843840.0
    return s * float(math.floor(y)) / 3843840.0


def grid_exact(b):  # warp-markers-v1: nearest grid point, halves away from zero, tie band excluded
    x = Fraction(b) * 3843840
    n = math.floor(abs(x) + Fraction(1, 2))
    if abs(abs(x) - math.floor(abs(x)) - Fraction(1, 2)) < Fraction(1, 10 ** 3):
        raise NoExpectation("beat near a rounding tie")
    return float(Fraction(n if x >= 0 else -n, 3843840))


def bounds_x(nb, p):  # REQ-015 clause 5
    d = p - nb[0]
    a, c = nb[1] + d * (5 / 60), nb[1] + d * (999 / 60)
    return min(a, c), max(a, c)


def tempo_ok_exact(nb, p, qb):  # warp-markers-v1: exact tempo within 5 to 999 BPM, bands excluded
    if abs(Fraction(p) - Fraction(nb[0])) < Fraction(5, 10 ** 4):
        raise NoExpectation("add near a neighbour's sample time")
    tempo = (Fraction(qb) - Fraction(nb[1])) / (Fraction(p) - Fraction(nb[0])) * 60
    if min(abs(tempo - 5), abs(tempo - 999)) < Fraction(1, 1000):
        raise NoExpectation("tempo at a limit")
    return 5 <= tempo <= 999


def segment(coords, x):  # REQ-008: largest k in 0..n-2 with coords[k] <= x, else 0
    k = 0
    for j in range(len(coords) - 1):
        if coords[j] <= x:
            k = j
    return k


def interpolate(xs, ys, x):
    k = segment(xs, x)
    u = (x - xs[k]) / (xs[k + 1] - xs[k])
    return math.fma(u, ys[k + 1], math.fma(-u, ys[k], ys[k]))


def convert_model(state, call, rate, rule):
    if not state["IsWarped"]:
        return no(NW)
    if rule == "exact":
        raise NoExpectation("conversion value (excluded in warp-markers-v1)")
    secs, beats = [m[0] for m in state["WarpMarkers"]], [m[1] for m in state["WarpMarkers"]]
    if call["function"] == "sample_to_beat_time":
        return {"outcome": "accepted", "value": interpolate(secs, beats, call["sample_frames"] / rate)}
    return {"outcome": "accepted", "value": interpolate(beats, secs, float(call["beat"])) * rate}


def lookup_model(ms, call, rule):
    move = call["function"] == "move_warp_marker"
    if len(ms) < 3 and (move or rule == "exact"):
        raise NoExpectation("move, or a v1 remove, on fewer than three markers")
    q = (grid_x if rule == "x" else grid_exact)(float(call["beat"]))
    hit = next((i for i, (_, b) in enumerate(ms) if b == q), None)
    if hit is None:
        return no(NOM)
    if hit == len(ms) - 1:
        return no(SH)
    if move:
        raise NoExpectation("accepted move")
    return ACC


def add_model(state, call, length, rule):
    if not state["IsWarped"]:
        return no(NW)
    p, b, ms = float(call["sample_time_seconds"]), float(call["beat"]), state["WarpMarkers"]
    if not 0 <= p <= length:
        return no(OOR)
    vis = ms[:-1]
    i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
    left, right = (ms[i - 1] if i > 0 else None), (vis[i] if i < len(vis) else None)
    if left is None and rule == "exact":
        raise NoExpectation("add before the first marker (excluded in warp-markers-v1)")
    if left and b < left[1]:
        return no(BL)
    if right and b > right[1]:
        return no(BR)
    qb = (grid_x if rule == "x" else grid_exact)(b)
    for nb in (n for n in (left, right) if n):
        if rule == "x":
            lo, hi = bounds_x(nb, p)
            if not lo <= qb <= hi:
                return no(TEMPO)
        elif not tempo_ok_exact(nb, p, qb):
            return no(TEMPO)
    return ACC


def model(case, rule="x"):
    try:
        states, length, rate = load(STAGE / case["input"])
    except Refused:
        return REF
    call = case.get("call")
    if call is None:
        want = case["expected"].get("state", {})
        return {"outcome": "opens", "state": {k: {f: states[k][f] for f in v} for k, v in want.items()}}
    st = states["AudioClip"]
    if call["function"] in ("sample_to_beat_time", "beat_to_sample_time"):
        return convert_model(st, call, rate, rule)
    if call["function"] in ("remove_warp_marker", "move_warp_marker"):
        return lookup_model(st["WarpMarkers"], call, rule)
    return add_model(st, call, length, rule)


def agrees(got, exp, call=None):
    """Comparators of spec.md: values within 1e-9 beat or 1e-6 frame; everything else exact."""
    if "value" in exp:
        tol = 1e-9 if call["function"] == "sample_to_beat_time" else 1e-6
        return set(got) == set(exp) and got["outcome"] == exp["outcome"] and abs(got["value"] - exp["value"]) <= tol
    return json.dumps(got, sort_keys=True) == json.dumps(exp, sort_keys=True)


def mutate(exp):
    m = json.loads(json.dumps(exp))
    if "value" in m:
        m["value"] += 1
    elif "state" in m:
        k = next(iter(m["state"]))
        f = next(iter(m["state"][k]))
        v = m["state"][k][f]
        m["state"][k][f] = (not v) if isinstance(v, bool) else (v + [[9.0, 9.0]] if isinstance(v, list) else v + 1)
    elif m["outcome"] == "refused" and "refusal_reason" in m:
        m["refusal_reason"] = OOR if m["refusal_reason"] != OOR else NW
    else:
        m = {"outcome": "opens", "state": {}} if m["outcome"] == "refused" else no(NOM)
    return m


# ---- agreement with the retained extracted-execution results (X2) ----
def x_results():
    nan = {"NaN": math.nan, "Infinity": math.inf, "-Infinity": -math.inf}
    return json.loads((ROOT / X2 / "results/envelope-warp.json").read_text(), parse_constant=nan.__getitem__)


XTABLE = {"fixtures/base.xml": "warp_WMK016_M1", "fixtures/first-marker-later.xml": "warp_WMK017_M2"}
XBOUNDS = {((1.0, 2.0), 1.5): "p1.5_nb(1,2)", ((1.0, 2.0), 1.0): "p1_nb(1,2)_ds0",
           ((1.0, 2.0), 1.0004): "p1.0004_nb(1,2)", ((2.0, 3.0), 1.5): "p1.5_right_nb(2,3)"}


def deciding(case, X):
    """The deciding binary64 values of a call, each as (what, X value or None when X2 did not run it, model value)."""
    call, exp = case["call"], case["expected"]
    states, length, rate = load(STAGE / case["input"])
    ms, f = states["AudioClip"]["WarpMarkers"], call["function"]
    rows = []
    if f in ("sample_to_beat_time", "beat_to_sample_time"):
        if "value" not in exp:
            return rows
        tab = X.get(XTABLE.get(case["input"]), {})
        if f == "sample_to_beat_time":
            key = str(round(call["sample_frames"] / rate * 48000))  # X2 inputs: seconds x 48,000
            xv = tab.get("sample_to_beat", {}).get(key)
        else:
            xv = tab.get("beat_to_sample", {}).get(str(float(call["beat"])))
            xv = None if xv is None else xv / 48000 * rate
        return [(f"{f} {key if f == 'sample_to_beat_time' else call['beat']}", xv, exp["value"])]
    q = grid_x(float(call["beat"]))
    if exp.get("refusal_reason") in (NW, OOR, BL, BR):
        return rows
    rows.append((f"q({call['beat']!r})", X["warp_edges_REQ015_016"]["beat_grid_round"].get(repr(float(call["beat"]))),
                 q))
    if f == "add_warp_marker":
        p, vis = float(call["sample_time_seconds"]), ms[:-1]
        i = next((k for k, m in enumerate(vis) if m[0] > p), len(vis))
        for nb in [n for n in ((ms[i - 1] if i > 0 else None), (vis[i] if i < len(vis) else None)) if n]:
            key = XBOUNDS.get(((nb[0], nb[1]), p))
            xv = X["warp_edges_REQ015_016"]["add_bounds_lo_hi"].get(key) if key else None
            rows.append((f"bounds({nb}, {p})", xv, list(bounds_x(nb, p))))
    return rows


def x_check(cases):
    X, out, bad = x_results(), {}, []
    for c in cases:
        if "call" not in c:
            continue
        rows = deciding(c, X)
        ran = [r for r in rows if r[1] is not None]
        agree = all(r[1] == r[2] for r in ran)
        label = c["expectation_provenance"]
        if label == PROV_X and not (rows and len(ran) == len(rows) and agree):
            bad.append((c["id"], "labelled extracted execution but a deciding value was not run or disagrees"))
        if label == PROV_XS and not (rows and len(ran) < len(rows) and agree):
            bad.append((c["id"], "labelled computed-by-rules but every deciding value was run, or a run value disagrees"))
        if ran:
            out[c["id"]] = {"label": label, "deciding": [{"what": w, "x2": xv, "model": mv} for w, xv, mv in rows]}
    return {"cases_with_x2_values": out, "problems": bad}


# ---- carry, package checks and seal ----
def carry_check(cases):
    v1 = json.loads((ROOT / V1 / "cases.json").read_text())["cases"]
    by_id = {c["id"]: c for c in cases}  # review: keyed by ID; WARP-MARKERS-018 is withdrawn
    same = [a["id"] for a in v1 if a["id"] in by_id and json.dumps(a, indent=1) == json.dumps(by_id[a["id"]], indent=1)]
    withdrawn = sorted({c["id"] for c in v1} - set(by_id))
    return {"v1_records": len(v1), "identical": len(same), "withdrawn": withdrawn,
            "problems": sorted({c["id"] for c in v1} - set(same) - {"WARP-MARKERS-018"})
            + ([] if withdrawn == ["WARP-MARKERS-018"] else ["withdrawn set"])}


def payload(d):
    return sorted(p for p in d.rglob("*") if p.is_file() and p.name != "manifest.json")


def links(md_path, root):
    out = []
    for target in re.findall(r"\]\(([^)\s]+)\)", md_path.read_text()):
        if re.match(r"[a-z]+:", target):
            out.append((target, "external URL not allowed"))
            continue
        path, _, anchor = target.partition("#")
        dest = (md_path.parent / path).resolve() if path else md_path
        ok_ = dest.is_file() and root.resolve() in dest.parents
        if ok_ and anchor:
            slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.+)$", dest.read_text(), re.M)}
            ok_ = anchor in slugs
        out.append((target, "ok" if ok_ else "UNRESOLVED"))
    return out


def verify(d):
    d = Path(d)
    man = json.loads((d / "manifest.json").read_text())
    files = payload(d)
    mismatches = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
                  or sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inventory = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    link_rows = {str(p.relative_to(d)): links(p, d) for p in d.glob("*.md")}
    bad_links = {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    missing = sorted({x for c in cases for x in (c["input"], c["sample"]) if not (d / x).is_file()})
    deny = {}
    for p in [*files, d / "manifest.json"]:
        if p.suffix == ".wav":
            continue
        text = p.read_text()
        hits = sorted({m if isinstance(m, str) else m[0] for pat in DENY for m in re.findall(pat, text)} - {""})
        hits = [h for h in hits if not any(h.startswith(a) for a in ALLOWED_HITS.get(p.name, ()))]
        if hits:
            deny[str(p.relative_to(d))] = hits
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": mismatches,
            "inventory_differences": inventory, "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": bad_links, "missing_case_inputs": missing, "deny_list_hits": deny,
            "case_count_matches": man["case_count"] == len(cases),
            "allowed_hits": {k: sorted(v) for k, v in ALLOWED_HITS.items()}}


def model_check(cases):
    problems, undetected, exact = {}, [], {}
    for c in cases:
        n = int(c["id"][-3:])  # review: by ID, not position
        rules = ("x", "exact") if n <= 38 else ("x",)
        for rule in rules:
            try:
                got = model(c, rule)
            except NoExpectation as e:
                got = {"no-expectation": str(e)}
            if not agrees(got, c["expected"], c.get("call")):
                problems[f"{c['id']} ({rule})"] = f"model {got} != expected {c['expected']}"
            elif rule == "x" and agrees(got, mutate(c["expected"]), c.get("call")):
                undetected.append(c["id"])
            if rule == "x" and "value" in c["expected"] and got.get("value") != c["expected"]["value"]:
                problems[f"{c['id']} (exact value)"] = f"model value {got.get('value')!r} is not bit-identical"
        if n > 38:
            try:
                exact[c["id"]] = model(c, "exact")
            except NoExpectation as e:
                exact[c["id"]] = {"no-expectation": str(e)}
    by_id = {c["id"]: c for c in cases}
    differs = sorted(k for k, v in exact.items() if not agrees(v, by_id[k]["expected"], by_id[k].get("call")))
    return {"case_problems": problems, "mutations_undetected": undetected,
            "new_cases_without_expectation_or_other_outcome_under_v1_rules": differs}


def text_diff():
    out = []
    for name in ("AGENTS.md", "README.md", "spec.md"):
        a, b = (ROOT / V1 / name).read_text().splitlines(), (STAGE / name).read_text().splitlines()
        out += difflib.unified_diff(a, b, f"warp-markers-v1/{name}", f"warp-markers-v2/{name}", lineterm="")
    (HERE / "v1-to-v2-text.diff").write_text("\n".join(out) + "\n")
    return len(out)


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    checks = {"model": model_check(cases), "x2": x_check(cases), "carry": carry_check(cases),
              "structure": structure_checks(), "single_change": single_change(), "fixtures": fixture_report()}
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    ver = verify(STAGE)
    report = {"schema": "author-validation-v1", "package": "warp-markers-v2 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), **checks,
              "evidence_identity": evidence_identity(ROOT), "text_diff_lines": text_diff(), **ver,
              "limits": "Authored consistency only: no reference application or candidate executed. The model restates "
                        "the released clauses from the same evidence and is not an oracle. The structure checks are "
                        "the T1.1 static rules (SPEC-LIVE-SET-STRUCTURE r1), not an observed open."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1, default=str) + "\n")
    trace = {"schema": "warp-markers-traceability-v2", "spec": "SPEC-WARP-MARKERS r4", "evidence": E,
             "inferred_links": I, "clauses": {k: {"clause": c, "support": s, "evidence": ev, "inferred": inf}
                                              for k, (c, s, ev, inf) in CLAUSES.items()},
             "cases": {B.cid(n): {"source": s, "evidence": ev, "inferred": inf,
                                  "provenance": {c["id"]: c for c in cases}[B.cid(n)]["expectation_provenance"]}
                       for n, (s, ev, inf) in TRACE.items()},
             "x2_corroboration": checks["x2"]["cases_with_x2_values"]}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    used = {x for row in [*trace["cases"].values(), *trace["clauses"].values()] for x in row["evidence"]}
    linked = {x for row in [*trace["cases"].values(), *trace["clauses"].values()] for x in row["inferred"]}
    assert used <= set(E) and linked <= set(I), (used - set(E), linked - set(I))
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1, ensure_ascii=False) + "\n")
    summary = {k: report[k] for k in ("cases", "payload_files", "hash_or_size_mismatches", "inventory_differences",
                                      "unresolved_links", "missing_case_inputs", "deny_list_hits", "manifest_sha256")}
    summary.update({"model": report["model"], "x2_problems": report["x2"]["problems"], "carry": report["carry"],
                    "structure": {k: v for k, v in report["structure"].items() if k != "audit_summary"},
                    "single_change_problems": report["single_change"]["problems"],
                    "duplicate_fixtures": report["fixtures"]["duplicates"],
                    "evidence_mismatches": {k: v["mismatches"] for k, v in report["evidence_identity"].items()
                                            if isinstance(v, dict)}})
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        {"seal": seal}[sys.argv[1]]()
