"""Checks, cross-check models and traceability for the mixer-values-v2 candidate (analyst side; never shipped).

Called through build_mv2.py (seal, verify). The models restate the contract's computed clauses from the same evidence;
they are not oracles. The structure checks run the T1.1 checkers unchanged.
"""
import json, math, random, re, struct, subprocess, sys, tempfile
from bisect import bisect_right
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

from build_mv2 import (COMPARATORS, EVID, HERE, R, SCHEMA, STAGE, T11, V1PKG, V1_MANIFEST_SHA, X2, cid, computed_cases,
                       doc, f32, v1, v1_records)

def close32(got, exp, abs_tol=None):
    """got is exp, one of exp's two binary32 neighbours, or (if abs_tol) within abs_tol of exp."""
    if got == exp or (abs_tol is not None and abs(got - exp) <= abs_tol):
        return True
    b = lambda z: struct.unpack("<i", struct.pack("<f", z))[0]
    key = lambda z: b(z) if b(z) >= 0 else -(b(z) & 0x7FFFFFFF)  # monotone integer order of binary32 values
    return f32(got) == got and abs(key(got) - key(exp)) == 1


def judge_compute(c, result):
    """Compare a computed result with a case's expectation by its comparator; return a list of errors."""
    exp, kind = c["expected"], c["comparator"]
    if "gain" in exp and "gains" not in exp:
        ok = result["gain"] == exp["gain"] if kind == COMPARATORS["exact"] else close32(result["gain"], exp["gain"])
        return [] if ok else [f"gain {result['gain']!r} != {exp['gain']!r}"]
    if "position" in exp:
        return [] if abs(result["position"] - exp["position"]) <= 1e-6 else [f"position {result['position']!r}"]
    pairs = (list(exp["gains"].items()) if "gains" in exp else
             [(l["position"], l["level"]) for l in exp["levels"]])
    got = result["gains"] if "gains" in result else {l["position"]: l["level"] for l in result["levels"]}
    return [f"{k}: {got[k]!r} != {e!r}" for k, e in pairs if not close32(got[k], e, 1e-12)]



# ---- independent cross-check model of the computed clauses (restates the contract; not an oracle) ----
getcontext().prec = 80
LN10 = Decimal(10).ln()


def f32_nearest(q):
    """Binary32 nearest to an exact positive rational q (ties to even), and q's distance from the rounding midpoint
    on its side, in binary32 steps (0.5 means q is a binary32 value)."""
    n = f32(float(q))
    g = min((n, v1.f32_step(n, -1), v1.f32_step(n, 1)),
            key=lambda c: (abs(Fraction(c) - q), struct.unpack("<I", struct.pack("<f", c))[0] & 1))
    side = v1.f32_step(g, 1 if q > Fraction(g) else -1)
    return g, float(Fraction(1, 2) - abs(q - Fraction(g)) / abs(Fraction(side) - Fraction(g)))


def curve(top, snap_each=True):
    """The contract's REQ-005 construction: points D[0..100] (position k/100) and gains G with midpoint margins.
    snap_each=False applies the 0.0001 snap only to the finished points (the other reading of the parent spec)."""
    cut = lambda z: 0.0 if abs(z) < f32(0.0001) else z
    snap = cut if snap_each else (lambda z: z)
    c4, c04, B = f32(0.4), f32(0.04), f32(-70.0)
    e = [snap(f32(top))]
    for _ in range(60):
        e.append(snap(f32(e[-1] - c4)))
    s = c4
    for _ in range(36):
        s = f32(s + c04)
        e.append(snap(f32(e[-1] - s)))
    a = f32(s + c04)
    e97 = f32(e[96] - a)
    b = f32(f32(f32(3 * a) + f32(B - e97)) / 6)  # x86_64 form: product and sum rounded separately
    e.append(snap(e97))
    e.append(snap(f32(e[97] - f32(a - b))))
    e.append(snap(f32(e[98] + f32(b - f32(a - b)))))
    e.append(B)
    D = [d if snap_each else cut(d) for d in e[::-1]]
    G, M = zip(*(f32_nearest(Fraction((Decimal(f32(d * f32(0.05))) * LN10).exp())) for d in D))
    return D, list(G), list(M)


def pos_to_gain(p, G):
    if p <= 0:
        return G[0]
    if p >= 1:
        return G[100]
    xx = p * 100.0
    k = int(xx)
    f = xx - k
    f = 0.0 if f <= 2.0 ** -17 else 1.0 if f >= 1 - 2.0 ** -17 else f
    return f32((1 - f) * G[k] + f * G[k + 1])


def gain_to_pos(g, G):
    i = bisect_right(G, g)
    if i == 0:
        return 0.0
    if i == len(G):
        return 1.0
    return f32((i - 1 + (g - G[i - 1]) / (G[i] - G[i - 1])) / 100)


def pan_law(w, p, sl, sr, v):
    th = lambda z: (z + 1) * math.pi / 4
    lift = lambda z: max(1e-5, math.sqrt(2) * z)
    return {"L->L": f32(v * (w * math.cos(th(sl)) + (1 - w) * lift(math.cos(th(p))))),
            "L->R": f32(v * w * math.sin(th(sl))), "R->L": f32(v * w * math.cos(th(sr))),
            "R->R": f32(v * (w * math.sin(th(sr)) + (1 - w) * lift(math.sin(th(p)))))}


def model_compute(c, curves):
    cp = c["compute"]
    fn = cp["function"]
    if fn in ("position-to-gain", "gain-to-position", "round-trip"):
        G = curves[cp["curve"]][1]
        if fn == "position-to-gain":
            return {"gain": pos_to_gain(cp["position"], G)}
        if fn == "gain-to-position":
            return {"position": gain_to_pos(cp["gain"], G)}
        return {"gain": pos_to_gain(gain_to_pos(cp["gain"], G), G)}
    if fn == "pan-law":
        return {"gains": pan_law(cp["w"], cp["pan"], cp["split_left"], cp["split_right"], cp["v"])}
    return None  # crossfade levels: no closed form in the parent spec; checked against X and for shape only


# ---- checks ----
DENY = [d for d in v1.DENY if d != r"\bslot"] + [  # clip slots are public document content in v2 fixtures
    r"T11", r"make_fixture", r"schema_check", r"fixture_audit", r"\bx2\b", r"\bX2\b", r"mixer\.json", r"NormalDip",
    r"SlightDip", r"Dipless", r"ConstantPower", r"FastCut", r"SlowCut", r"CrossfadeToLevel", r"ConvertLevel",
    r"CrossFadeHelper", r"PanModeAmount", r"StereoSplitPan", r"TSendVolumes", r"xexec", r"fmadd", r"fnmsub", r"cosf",
    r"\bLSS-", r"\bMG-0", r"LIVE-SET-STRUCTURE", r"MIX-GRAPH", r"mpmath", r"\bADR", r"Q-019", r"roundtrip_Q019",
    r"vtable slot", r"Live_x86", r"build_mv"]
ALLOWED = {"AGENTS.md": {"decompil"}}


def deny_hits(text, name):
    hits = sorted({m for pat in DENY for m in re.findall(pat, text)})
    return [h for h in hits if not any(h.startswith(a) for a in ALLOWED.get(name, ()))]


def verify(d):
    d = Path(d).resolve()  # v1.links compares resolved paths
    man = json.loads((d / "manifest.json").read_text())
    files = v1.payload(d)
    bad = [f["path"] for f in man["files"] if not (d / f["path"]).is_file()
           or v1.sha((d / f["path"]).read_bytes()) != f["sha256"] or (d / f["path"]).stat().st_size != f["bytes"]]
    inventory = sorted({str(p.relative_to(d)) for p in files} ^ {f["path"] for f in man["files"]})
    link_rows = {str(p.relative_to(d)): v1.links(p, d) for p in d.glob("*.md")}
    cases = json.loads((d / "cases.json").read_text())["cases"]
    return {"dir": str(d), "payload_files": len(files), "files_including_manifest": len(files) + 1,
            "manifest_sha256": v1.sha((d / "manifest.json").read_bytes()), "hash_or_size_mismatches": bad,
            "inventory_differences": inventory, "symlinks": [str(p) for p in d.rglob("*") if p.is_symlink()],
            "markdown_links": {k: len(v) for k, v in link_rows.items()},
            "unresolved_links": {k: [t for t, s in v if s != "ok"] for k, v in link_rows.items() if any(s != "ok" for _, s in v)},
            "missing_case_inputs": [c["input"] for c in cases if c["input"] and not (d / c["input"]).is_file()],
            "unused_fixtures": sorted({str(p.relative_to(d)) for p in (d / "fixtures").iterdir()} - {c["input"] for c in cases}),
            "deny_list_hits": {str(p.relative_to(d)): h for p in [*files, d / "manifest.json"]
                               if (h := deny_hits(p.read_text(), p.name))}}


def structure_checks(cases):
    """Run the T1.1 checkers on every fixture; return the summary and write their outputs here."""
    out = HERE / "structure-check"
    out.mkdir(exist_ok=True)
    fx = sorted(str(p) for p in (STAGE / "fixtures").glob("*.xml"))
    res = subprocess.run([sys.executable, "-I", str(T11 / "schema_check.py"), str(SCHEMA), *fx],
                         capture_output=True, text=True, check=True).stdout
    (out / "schema-check.jsonl").write_text(res.replace(str(STAGE) + "/", ""))
    want = {"player_tracks": 2, "returns_after_others": True, "trailing_returns": 1, "grouped_tracks": 0,
            "scenes": 2, "freeze_slots_equal_main": True, "main_slots_equal_scenes": True,
            "holders_more_than_returns": False, "holders_fewer_than_returns": False, "main_prehear_no_sends": True,
            "sendspre_present": True, "sendspre_equal_returns": True, "pointees": 66, "pointee_without_id_or_zero": 0,
            "pointee_ids_unique": True, "next_pointee_id": 67, "max_pointee_id": 66, "next_pointee_id_above_max": True,
            "dangling_envelopes": 0, "list_item_ids_unique": True}
    rows = [json.loads(l) for l in res.splitlines()]
    schema_problems = {r["doc"].rsplit("/", 1)[-1]: [r["deviations"], {k: r["rules"].get(k) for k in want
                                                                        if r["rules"].get(k) != want[k]}]
                       for r in rows if r["deviations"] or any(r["rules"].get(k) != want[k] for k in want)}
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "mixer-values-v2").symlink_to(STAGE)
        subprocess.run([sys.executable, "-I", "-B", str(T11 / "fixture_audit.py"), str(SCHEMA), t,
                        str(out / "fixture-audit.json")], capture_output=True, text=True, check=True)
    audit = json.loads((out / "fixture-audit.json").read_text())["releases"][0]
    s = audit["summary"]
    return {"schema_check": {"documents": len(rows), "problems": schema_problems},
            "fixture_audit": {**s, "after_additions_needed": [e["fixture"] for e in audit["fixtures"]
                                                              if e.get("minimal_addition") or e.get("recommended_addition")],
                              "case_effects": sorted({c["effect"] for e in audit["fixtures"] for c in e["cases"]})},
            "ok": not schema_problems and s["fixtures"] == 37 and s["refused"] == 0 and s["with_unknown_shapes"] == 0
            and not s["cases_contradicted"] and not s["cases_not_isolating"]}


def fixture_checks(cases):
    base = doc().decode().split("\n")
    seen, out, problems = {}, {}, {}
    edits = {cid(n): changes for n, _, _, _, changes, _, _ in v1.CASES}
    for c in cases:
        if not c["input"]:
            continue
        raw = (STAGE / c["input"]).read_bytes()
        errs = []
        try:
            errs += v1.judge(c["expected"], *v1.model(raw))
        except v1.Excluded as e:
            errs.append(f"input has no expectation: {e}")
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n"):
            errs.append("not ASCII/LF/final newline")
        if raw in seen:
            errs.append(f"same bytes as {seen[raw]}")
        seen[raw] = c["id"]
        lines = raw.decode().split("\n")
        changed = [ln.strip() for ln, b in zip(lines, base) if ln != b]
        if len(lines) != len(base) or len(changed) != len(edits[c["id"]]) or \
                sorted(f'<Manual Value="{t}" />' if k not in ("SoloSink", "PanMode", "CrossfadeCurve")
                       else f'<{k} Value="{t}" />' for (_, k), t in edits[c["id"]].items()) != sorted(changed):
            errs.append(f"differs from the template set in other lines: {changed}")
        if errs:
            problems[c["id"]] = errs
        out[c["id"]] = {"bytes": len(raw), "lines": raw.count(b"\n"), "lines_changed_from_template": changed}
    probes = {"pan 0.25": {("audio", "Pan"): "0.25"}, "volume 2": {("audio", "Volume"): "2"},
              "volume 0.0001": {("audio", "Volume"): "0.0001"}, "send 1.0000001": {("audio", "Send"): "1.0000001"},
              "volume exponent": {("audio", "Volume"): "1e0"}, "volume -69.7 dB": {("audio", "Volume"): "0.00032734069"},
              "pan mode 2": {("audio", "PanMode"): "2"}, "curve 7": {("set", "CrossfadeCurve"): "7"},
              "speaker 1": {("audio", "Speaker"): "1"},
              "dB tie -6.0625": {("audio", "Volume"): str(f32(10 ** (-6.0625 / 20)))}}
    rejected = {}
    for name, ch in probes.items():
        try:
            v1.model(doc(ch))
            rejected[name] = False
        except v1.Excluded:
            rejected[name] = True
    return problems, out, rejected


def computed_checks(cases):
    """X agreement, model agreement under each comparator, shape checks and the margins the assumptions state."""
    curves = {"volume": curve(6.0), "send": curve(0.0)}
    want = {cid(n): (fn, fields, exp) for n, (fn, _, _, fields, exp, _, _) in enumerate(computed_cases(), start=38)}
    problems, model_exact = {}, {}
    for c in cases:
        if c["action"] != "compute":
            continue
        fn, fields, exp = want[c["id"]]
        errs = [] if (c["compute"] == {"function": fn, **fields} and c["expected"] == exp) else ["differs from X2"]
        m = model_compute(c, curves)
        if m is not None:
            errs += [f"model: {e}" for e in judge_compute(c, m)]
            model_exact[c["id"]] = m == c["expected"]
        else:
            lv = [l["level"] for l in c["expected"]["levels"]]
            if lv[0] != 1.0 or lv[-1] != 0.0 or any(a < b for a, b in zip(lv, lv[1:])):
                errs.append("crossfade level shape")
        if errs:
            problems[c["id"]] = errs
    rt = [c for c in cases if c["action"] == "compute" and c["compute"]["function"] == "round-trip"]
    margins = {f"{c['compute']['curve']} {c['compute']['gain']!r}": curves[c["compute"]["curve"]][2][
        curves[c["compute"]["curve"]][1].index(c["compute"]["gain"])] for c in rt}
    G = curves["volume"][1]
    g001 = f32(0.001)
    k = bisect_right(G, g001) - 1
    shifts = []
    for d in (-1, 1):  # a one-step change of a bottom curve point (arm64 fused multiply-add) moves this position by:
        G2 = list(G)
        G2[k] = v1.f32_step(G[k], d)
        shifts.append(abs(gain_to_pos(g001, G2) - gain_to_pos(g001, G)))
    rng = random.Random(20261018)
    general = {}
    for name, (_, Gc, _) in curves.items():  # finding F1: the round trip is not exact for gains between curve points
        steps, n = [], 4000
        for _ in range(n):
            g = f32(math.exp(rng.uniform(math.log(Gc[0]), math.log(Gc[100]))))
            back = pos_to_gain(gain_to_pos(g, Gc), Gc)
            bits = lambda z: struct.unpack("<i", struct.pack("<f", z))[0]
            steps.append(abs(bits(back) - bits(g)))
        general[name] = {"sampled": n, "not_exact": sum(s > 0 for s in steps), "worst_steps": max(steps)}
    end_snap = {name: sum(a != b for a, b in zip(curve(top, snap_each=False)[1], curves[name][1]))
                for name, top in (("volume", 6.0), ("send", 0.0))}  # finding F2: gains that differ under that reading
    return {"problems": problems, "model_equals_x2_exactly": model_exact,
            "curve_points_differing_if_snapped_only_at_end": end_snap,
            "round_trip_point_midpoint_margins": margins, "min_margin": min(margins.values()),
            "gain_0.001_position_shift_for_one_step_at_point": {"k": k, "shifts": shifts},
            "round_trip_of_other_gains_model": general,
            "ok": not problems and min(margins.values()) >= 0.16 and max(shifts) < 1e-6}


def mutation_probe(cases, curves=None):
    missed = []
    for c in cases:
        exp = json.loads(json.dumps(c["expected"]))
        if c["action"] == "open":
            e = next(iter(exp["values"].values()))
            if "text" in e:
                e["text"] += "x"
            elif "name" in e:
                e["name"] += "x"
            else:
                e["value"] = not e["value"] if isinstance(e["value"], bool) else e["value"] + 1
            caught = bool(v1.judge(exp, *v1.model((STAGE / c["input"]).read_bytes())))
        else:
            k = next(iter(exp))
            if k in ("gain", "position"):
                exp[k] = v1.f32_step(exp[k] or 1e-30, 2) if k == "gain" else exp[k] + 2e-6
            elif k == "gains":
                exp[k]["L->L"] = v1.f32_step(exp[k]["L->L"], 2) if exp[k]["L->L"] else 1e-9
            else:
                exp[k][1]["level"] = v1.f32_step(exp[k][1]["level"], 2)
            caught = bool(judge_compute({**c, "expected": exp}, c["expected"]))
        if not caught:
            missed.append(c["id"])
    planted = deny_hits("see analysis/x, T11 and 0x10143a290 via PRB-S9-04 in NormalDip", "spec.md")
    return {"mutated_cases": len(cases), "missed": missed, "planted_deny_terms_flagged": len(planted)}


def evidence_identity():
    out = v1.evidence_identity()
    for run, key in (("r2/x2-mixer-v1", None), ("r2/t11-structure-v1", "sha256")):
        m = json.loads((EVID / run / "manifest.json").read_text())
        files = {p: (h[key] if key else h) for p, h in m["files"].items()}
        if run.endswith("t11-structure-v1"):  # only the generator and checkers this build imports or runs
            files = {p: h for p, h in files.items() if p in ("make_fixture.py", "schema_check.py", "fixture_audit.py")}
        out[run] = {"manifest_sha256": v1.sha((EVID / run / "manifest.json").read_bytes()), "checked": len(files),
                    "mismatches": [p for p, h in files.items() if v1.sha((EVID / run / p).read_bytes()) != h]}
    sl = json.loads((X2 / "manifest.json").read_text())["slice"]
    p = Path(sl["path"])
    out["x2_slice_sha256_matches"] = (v1.sha(p.read_bytes()) == sl["sha256"]) if p.is_file() else "unknown: slice absent"
    out["schema_sha256"] = v1.sha(SCHEMA.read_bytes())
    v1m = json.loads((V1PKG / "manifest.json").read_text())
    out["mixer_values_v1"] = {"manifest_sha256_matches_catalog": v1.sha((V1PKG / "manifest.json").read_bytes()) == V1_MANIFEST_SHA,
                              "file_mismatches": [f["path"] for f in v1m["files"]
                                                  if v1.sha((V1PKG / f["path"]).read_bytes()) != f["sha256"]]}
    return out


# ---- traceability (analyst-only; never shipped) ----
E2 = {
    "template-set": ("analysis/ableton-live-12.4.3/r2/t11-structure-v1/make_fixture.py (T11-MIN generator, imported "
                     "unchanged; its clips, sample, devices and MIDI volume envelope left out); wiki/specs/live-set-structure.md "
                     "r1 REQ-018 table (R/V/W/O) and REQ-001, 002, 004 to 006, 013 to 016 (S; A1 to A3 settled); "
                     "structure-check/schema-check.jsonl and fixture-audit.json (no deviation, no refusal, no unknown shape)"),
    "x2-fader": ("analysis/ableton-live-12.4.3/r2/x2-mixer-v1/results/mixer.json fader.position_to_gain, gain_to_position, "
                 "roundtrip_Q019; run_mixer.py; x86-disasm.txt 0x101aec640 (curve builder: per-point snap feeding the next "
                 "point), 0x101aecbd0 (position to gain), 0x101aecc90 (gain to position); s9-mixer-v1/derive_curves.py "
                 "line 84 (2^-17 fraction snap, arm64 0x101ac3498)"),
    "x2-pan": "x2-mixer-v1 results/mixer.json pan_law; x86-disasm.txt 0x101b719e0 (binary64 theta and cos; binary32 combine)",
    "x2-xfade": ("x2-mixer-v1 results/mixer.json crossfade (x86 0x101b1a470 to 0x101b1a8e0, code order as the seven "
                 "names, s9-0003 0x101aed36c); positions +-0.95 not released (not multiples of 1/64)"),
    "x2-switch": "x2-mixer-v1 results/mixer.json switch_text (0x1014353b0: 1.0 -> On, 0.0 -> Off)",
    "slices": "x2-mixer-v1/fma-scan.txt (arm64 fused operations: curve builder landing point, conversions in binary64, "
              "pan theta, Dipped and Intermediate)",
}
I2 = {
    "I7": "arm64 equivalence of the extracted functions within each comparison (fma-scan.txt).",
    "I8": "The reference exp10f rounds the round-trip curve points to nearest (margin >= 0.16 step, model).",
    "I9": "Apple exp10f and cos within one binary32 step of glibc at the case inputs (comparators allow one step).",
    "I10": ("The template set opens: it meets every traced structural condition of SPEC-LIVE-SET-STRUCTURE r1 and "
            "writes every W element as T11-MIN does; it holds no clip, sample or device, so A4 and A6 are not involved; "
            "A5 concerns refusals and A7 saving only."),
}
NEW_TRACE = {"position-to-gain": "MV-023/MV-024", "gain-to-position": "MV-025", "round-trip": "REQ-005 X round-trip bullet",
             "pan-law": "MV-048 (gains behind MV-035 to 037)", "crossfade-level": "MV-047"}
NEW_EVIDENCE = {"position-to-gain": "x2-fader", "gain-to-position": "x2-fader", "round-trip": "x2-fader",
                "pan-law": "x2-pan", "crossfade-level": "x2-xfade"}
NEW_LINKS = {"round-trip": ["I7", "I8"], "pan-law": ["I7", "I9"], "crossfade-level": ["I7", "I9"],
             "position-to-gain": ["I7", "I9"], "gain-to-position": ["I7", "I9"]}


def traceability(cases):
    xl = {cid(n): loc for n, (*_, loc) in enumerate(computed_cases(), start=38)}
    trace = {"schema": "mixer-values-traceability-v2", "spec": "SPEC-MIXER-VALUES r4", "evidence": {**v1.E, **E2},
             "inferred_links": {**v1.I, **I2},
             "clauses": {**{k: {"evidence": ev + ["template-set"], "inferred": inf + ["I10"]}
                            for k, (ev, inf) in v1.CLAUSES.items()},
                         R + "005 curves, conversions, round trip at curve points": {"evidence": ["x2-fader", "slices"],
                                                                                     "inferred": ["I7", "I8", "I9"]},
                         R + "008 track switch text (X)": {"evidence": ["x2-switch"], "inferred": ["I7"]},
                         R + "013 pan-law gains, w and v in {0, 1}": {"evidence": ["x2-pan", "slices"], "inferred": ["I7", "I9"]},
                         R + "014 crossfade levels at multiples of 1/4": {"evidence": ["x2-xfade", "slices"],
                                                                          "inferred": ["I7", "I9"]}},
             "cases": {}}
    for c in cases:
        n = int(c["id"][-3:])
        if c["action"] == "open":
            els = sorted({k.split("/")[1] for k in c["expected"]["values"]})
            ev = {e for el in els for e in v1.CASE_EVIDENCE[el]} | {"template-set"} | (
                {"doc-form"} if "send_counts" in c["expected"] else set()) | ({"x2-switch"} if "Speaker" in els else set())
            trace["cases"][c["id"]] = {"source": v1.TRACE[n] + " (carried from mixer-values-v1)", "evidence": sorted(ev),
                                       "inferred": sorted({i for el in els for i in v1.CASE_LINKS[el]} | {"I10"})}
        else:
            fn = c["compute"]["function"]
            trace["cases"][c["id"]] = {"source": NEW_TRACE[fn], "x2_record": xl[c["id"]],
                                       "evidence": [NEW_EVIDENCE[fn], "slices"], "inferred": NEW_LINKS[fn]}
    return trace


def seal():
    cases = json.loads((STAGE / "cases.json").read_text())["cases"]
    fixture_problems, fixtures, rejected = fixture_checks(cases)
    structure = structure_checks(cases)
    computed = computed_checks(cases)
    carried_identical = [a == b for a, b in zip(v1_records(), cases[:37])]
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": v1.sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in v1.payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v2", "package": "mixer-values-v2 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases),
              "carried_records_identical_to_v1": sum(carried_identical), "fixture_problems": fixture_problems,
              "structure_checks": structure, "computed_checks": computed,
              "excluded_input_probes_rejected": rejected, "mutation_probe": mutation_probe(cases),
              "evidence_identity": evidence_identity(), "fixtures": fixtures, **verify(STAGE),
              "limits": ("Checks authored consistency only: no reference or candidate executed; the models restate the same "
                         "evidence and are not oracles; the crossfade levels have no model; the structure checkers "
                         "measure SPEC-LIVE-SET-STRUCTURE r1's traced rules, not the original reader.")}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    (HERE / "traceability.json").write_text(json.dumps(traceability(cases), indent=1) + "\n")
    keys = ("cases", "carried_records_identical_to_v1", "fixture_problems", "excluded_input_probes_rejected",
            "mutation_probe", "payload_files", "hash_or_size_mismatches", "inventory_differences", "unresolved_links",
            "missing_case_inputs", "unused_fixtures", "deny_list_hits", "manifest_sha256")
    print(json.dumps({**{k: report[k] for k in keys}, "structure_ok": structure["ok"],
                      "computed_ok": computed["ok"], "computed_problems": computed["problems"],
                      "evidence_identity": report["evidence_identity"]}, indent=1))


