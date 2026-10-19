"""Checks, seal and verify for the midi-config-v4 candidate (analyst side; never shipped). See build_v4.py.

  python3.11 -I seal_v4.py seal            # after build_v4.py build
  python3.11 -I seal_v4.py verify <dir>    # an exported copy, given as an absolute path
"""
import configparser, difflib, io, json, re, sys
from fractions import Fraction as Fr

from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I does not add the script directory
from build_v4 import (b3, EXCLUDED_ROWS, HERE, MOVE_CASES, NEAR, NEAR_CASES, NEW, NUM, SPEC, STAGE, V3, V3A,  # noqa: E402
                      V3_MANIFEST_SHA, X2, model4, pair_previous, r5_table, tau, x_records)

# ---- checks ----------------------------------------------------------------------------------------------------
DENY = [x for x in b3.DENY if x != r"-129"] + [  # -129 is now a released behavioral value (case 149)
    r"xexec", r"\bX[12]\b", r"[Xx]2-", r"\bT[KB]-\d", r"\bgdb\b", r"\bstub", r"harness(?! for the original application)", r"run_x2", r"\bfmaf?\b",
    r"multiply-add", r"libm", r"cxa", r"pthread", r"operator new", r"\bApply\b", r"value function", r"combiner",
    r"setter", r"PickUp", r"TakeOver", r"LMidi", r"sControl", r"input_history", r"InputHistory", r"Launch",
    r"\bE1[56]\b", r"MidiInput", r"\bprior", r"sentinel", r"Languages", r"\bI[7-9]\b", r"\bRV[23]-", r"REVIEW\.md",
    r"\bF[1-4]\b"]


def verify(d):
    b3.DENY = DENY  # b3.verify scans with its module-level DENY; use the widened list
    return b3.verify(d)


def msgs_of(case):
    return [(int(s[3:5], 16), int(s[6:8], 16)) for s in case["stimulus"]["messages"]]


def close(a, b, t):
    return len(a) == len(b) and all(abs(Fr(x) - Fr(y)) <= t for x, y in zip(a, b))


def run_model(case, takeover=None):
    a = case["expected"]["assignments"][0]
    return model4(a["control"], a["map_mode"], takeover or case["stimulus"]["takeover"], case["stimulus"]["parameter"],
                  msgs_of(case))


def check_new(cases, table, xr):
    """New cases against X, the r5 table and the restatement; exception lists; selection; mutation."""
    by_id, problems, caught = {c["id"]: c for c in cases}, {}, 0
    names = {"none": "None", "pick-up": "Pick-Up", "value-scaling": "Value Scaling"}
    for n, mt, control, _ in NEW:
        c, errs = by_id[b3.cid(n)], []
        r, x, p, got = table[mt], xr[mt], c["stimulus"]["parameter"], c["expected"]["values"]
        t, take = tau(p), c["stimulus"]["takeover"]
        if r["label"] != "X" or x.get("label", "X") != "X":
            errs.append("not an X row")
        if c["stimulus"]["messages"] != x["input"] or msgs_of(c) != r["messages"] or len(got) != len(r["messages"]):
            errs.append("messages differ from X or the r5 table")
        if not close(got, x["x"], Fr(1, 2 * 10 ** 9)) or c["expected"]["assignments"][0]["map_mode"] != x["mode"]:
            errs.append(f"expected {got} is not the X result {x['x']}")
        if names[take] not in r["condition"] or any(v in r["condition"] for k, v in names.items() if k != take):
            errs.append(f"takeover {take} vs r5 condition {r['condition']!r}")
        spec_vals = [Fr(s.replace("−", "-")) for s in r["values"].split(", ")]
        if not close(got, spec_vals, t):
            errs.append(f"r5 table {r['values']} not within tau")
        vals, near, moves = run_model(c)
        if not close(got, vals, t):
            errs.append(f"restatement {[float(v) for v in vals]} not within tau")
        if (min(near, default=1) < NEAR * t) != (n in NEAR_CASES) or (moves > 0) != (n in MOVE_CASES):
            errs.append(f"exception lists: near {float(min(near, default=1))}, moves {moves}")
        if not re.search(r"= [0-9.e-]+ absolute$", c["comparator"]) or float(t) != float(c["comparator"].split()[-2]):
            errs.append("comparator tau")
        bumped = [v + 2 * float(t) for v in got]  # mutation: every value moved by 2 tau must fail both checks
        caught += not close(bumped, x["x"], Fr(1, 2 * 10 ** 9)) and not close(bumped, vals, t)
        if errs:
            problems[c["id"]] = errs
    x_rows = {k for k, v in table.items() if v["label"] == "X"}
    scond = {k for k, v in table.items() if v["label"] == "S-cond"}
    selection = {"released_rows": sorted(mt for _, mt, _, _ in NEW), "excluded_rows": EXCLUDED_ROWS,
                 "released_equal_r5_X_rows": {mt for _, mt, _, _ in NEW} == x_rows,
                 "excluded_equal_r5_S_cond_rows": set(EXCLUDED_ROWS) == scond,
                 "mutations_caught": f"{caught}/{len(NEW)}"}
    return problems, selection


def check_carried(cases, xr):
    """v3 value cases: the v4 rules reproduce them under every named choice, and X corroborates them."""
    trace3 = json.loads((V3A / "traceability.json").read_text())["cases"]
    out = {}
    for c in cases:
        if "stimulus" not in c:
            continue
        mt = re.search(r"MT-\d\d", trace3[c["id"]]["source"])[0]
        choices = ["none", "pick-up", "value-scaling"] if c["stimulus"]["takeover"] == "any" else ["none"]
        model_ok = all(close(c["expected"]["values"], run_model(c, ch)[0], Fr(1, 10 ** 6)) for ch in choices)
        x_ok = close(c["expected"]["values"], xr[mt]["x"], Fr(1, 10 ** 6))
        out[c["id"]] = {"row": mt, "v4_rules_agree": model_ok, "x_agrees": x_ok, "tau": float(tau(c["stimulus"]["parameter"]))}
    return out


def check_rules():
    """Pair previous values against the bitwise form; rescaled crossfader cases; excluded inputs; decode rows."""
    pair_ok = all(pair_previous(m, l) == Fr(((-129 if m is None else m) << 7) | (-129 if l is None else l), 129)
                  for m in [None, *range(128)] for l in [None, *range(128)])
    cases = {c["id"]: c for c in json.loads((STAGE / "cases.json").read_text())["cases"]}
    rescaled = {}
    for cid in ("MIDI-CONFIG-126", "MIDI-CONFIG-150"):
        c = cases[cid]
        base = run_model(c, "pick-up")[0]
        for a, b in ((-1, 1), (0, 2), (-5, 3), (1, -1)):
            p = {**c["stimulus"]["parameter"], "min": a, "max": b,
                 "initial_value": float(a + (b - a) * Fr(c["stimulus"]["parameter"]["initial_value"]))}
            got = model4("CrossfaderSlider", c["expected"]["assignments"][0]["map_mode"], "pick-up", p, msgs_of(c))[0]
            rescaled[f"{cid} range {a}..{b}"] = got == [a + (b - a) * v for v in base]
    cont = {"kind": "continuous", "stepped": False, "min": 0, "max": 1, "initial_value": 0.5}
    probes = {}
    for name, args in {
        "on/off parameter": ("Encoder1", "Absolute", "none", {**cont, "kind": "on/off"}, [(NUM, 0x40)]),
        "min equals max": ("Encoder1", "Absolute", "none", {**cont, "min": 1, "max": 1, "initial_value": 1}, [(NUM, 1)]),
        "stepped, non-integer value": ("Encoder1", "LinearSignedBit", "any", {**cont, "stepped": True, "max": 3},
                                       [(NUM, 1)]),
        "current value outside the range": ("Encoder1", "Absolute", "none", {**cont, "initial_value": 2}, [(NUM, 1)]),
        "Absolute, continuous, takeover any": ("Encoder1", "Absolute", "any", cont, [(NUM, 0x40)]),
    }.items():
        try:
            model4(*args)
            probes[name] = "EXPECTATION GIVEN (wrong)"
        except b3.NoExpectation as e:
            probes[name] = f"no expectation: {e}"
    row = re.compile(r"\s*\| `(?:Linear|Accel)\w+` \|")
    rows = [[x.strip() for x in f.read_text().splitlines() if row.match(x)] for f in (SPEC, STAGE / "spec.md")]
    return {"pair_previous_equals_bitwise_form_all_16641": pair_ok, "crossfader_rescaled_cases_exact": rescaled,
            "excluded_input_probes": probes, "decode_rows_equal_parent_spec": rows[0] == rows[1] and len(rows[1]) == 8}


def x2_identity():
    man = json.loads((X2 / "manifest.json").read_text())
    bad = [k for k, v in man["files"].items() if not (X2 / k).is_file() or b3.sha((X2 / k).read_bytes()) != v]
    return {"x2_manifest_sha256": b3.sha((X2 / "manifest.json").read_bytes()), "x2_slice_sha256": man["slice"]["sha256"],
            "x2_files_listed": len(man["files"]), "x2_file_mismatches": bad,
            "note": "raw/runs.jsonl is listed; heap addresses in it change on a re-run, the results files do not"}


# ---- analyst traceability (never shipped); E10-E14 locators are those of midi-config-v3, E15-E16 spec r5 -------
X2REL = "analysis/ableton-live-12.4.3/r2/x2-midi-v1/"
EVIDENCE_NEW = {
    "v3": f"handoff/midi-config-v3/ (manifest sha256 {V3_MANIFEST_SHA}, REVIEW.md); per-case sources in "
          "analysis/ableton-live-12.4.3/handoff-staging/midi-config-v3-analysis/traceability.json",
    "E15": X2REL + "static-e15.txt and x86-disasm.txt: preference constructor x86 0x1023e0050 / arm64 0x1022cc18c builds "
           "the entries from sControlNoTakeOverEntry, sControlPickUpTakeOverEntry, sControlValueScalingTakeOverEntry in "
           "that order; change handler x86 0x1023e2a60 / arm64 0x1022cec38 posts OSetMidiTakeOverMode with the chooser "
           "index (unset -99 sends 0); engine handler x86 0x101bc0770 / arm64 0x101b83750 stores it for the takeover; "
           "reset: MidiInputRouter.ResetInputHistory (arm64 0x101b68f98, refill 0x101b65c1c), sole poster 0x10259b710 = "
           "reset_input_history, called only by Launch_Control_XL among the shipped scripts. Localized words not read",
    "E16": X2REL + "run_x2.py under tools/xexec + gdb (sh run.sh); x86 receiver 0x101bbc3b0, 14-bit setters "
           "0x101bbced0/0x101bbcf10, combiner 0x101bbc870, Apply 0x101bbc9c0, value function 0x101bb27b0, takeover "
           "0x101bb8b70, Pick-Up 0x101bb8990 (arm64 matches in addresses.json); stubs 0x101abb210, 0x101b3d680, "
           "0x101b6f830 (current value), 0x101b3d360 (setter); Pick-Up notification post jumped over; previous value "
           "supplied by the harness per E10; imports operator new, cxa guards, __cxa_atexit, pthread keys; no libm",
}
INFERRED_NEW = {
    "I1": "Revision 5 (E15) makes the entry-to-choice mapping static: first entry 0 = none, second 1 = pick-up, third 2 = "
          "value-scaling. Residual: the displayed words of the three text keys are None, Pick-Up, Value Scaling (not "
          "read; resources packed). Stated in the contract as an assumption affecting reference labels only.",
    "I6": "arm64 equivalence of the X results: static slice comparison in E16; the only fused operation that differs is "
          "the value function fmadd (difference <= 1 binary32 ulp of R, 0 when lo = 0); the takeover fmadd has s1 = +-1.",
    "I7": "The application passes the previous data value as the static dispatcher reading gives it (E10): the last data "
          "value on the same input, channel and controller, -129 when none. The X harness supplied it; the dispatcher "
          "and the per-input table did not run.",
    "I8": "The harness built the parameter details record (kind, min, max, quantized, Zoom 1.0) and simulated the "
          "parameter; which application parameter reports which kind, range and stepping is excluded (PRB-N7-04).",
}
CLAUSES = {
    "midi-config-v3 clauses, cases and fixtures, carried": (["v3"], []),
    "takeover: three choices by preference position; none applies every value": (["E14", "E15", "E16"], ["I1"]),
    "takeover: exemptions (relative; enumerated and other; crossfader Absolute); crossfader pairs not exempt": (["E10", "E11", "E13", "E16"], ["I2"]),
    "previous data values: per input, channel and number; empty on open; every message counts; nothing else empties it": (["E10", "E15"], ["I7"]),
    "pair previous value (four cases, equal to ((128m)|l)/129 with -129 for a missing half)": (["E11", "E16"], ["I7"]),
    "Pick-Up and Value Scaling rules, sorted bounds, -129 test, inclusive bounds, clamping, unrounded move": (["E14", "E16"], ["I6", "I7", "I8"]),
    "reversed ranges: Absolute, Absolute14Bit, relative (stepped toward max) and takeover": (["E12", "E16"], ["I6"]),
    "tolerance tau = max(1e-6, 2^-22 R)": (["E16"], ["I6"]),
    "exclusion: tests within 8 tau of a bound outside cases 149 and 152-161 (r5 Timing and state; plan finding F2; precision-model.txt; band width an author choice)": (["E16"], ["I6"]),
    "exclusion: Value Scaling moves outside the listed cases (cross-slice magnification up to 18 tau, r5; exact-versus-binary32 up to 3.8 tau with lo = 0, plan finding F1, precision-model.txt)": (["E16"], ["I6"]),
    "exclusion: on/off parameters (S-cond, PRB-N7-04); default choice; displayed wording; notification": (["E13", "E15"], []),
}


def text_diff():
    diffs, removed = [], {}
    for name in ("README.md", "AGENTS.md", "spec.md"):
        old, new = (V3 / name).read_text().splitlines(), (STAGE / name).read_text().splitlines()
        diffs += difflib.unified_diff(old, new, f"midi-config-v3/{name}", f"midi-config-v4/{name}", lineterm="")
        removed[name] = sum(1 for line in difflib.ndiff(old, new) if line.startswith("- "))
    (HERE / "v3-to-v4-text.diff").write_text("\n".join(diffs) + "\n")
    return removed


def seal():
    cm = b3.load("v2_crosscheck_model", b3.V2A / "crosscheck_model.py")
    doc, v3doc = (json.loads((d / "cases.json").read_text()) for d in (STAGE, V3))
    cases, v3 = doc["cases"], v3doc["cases"]
    carry = {"v3_case_records_identical": cases[:len(v3)] == v3,
             "v3_fixture_bytes_identical": all((STAGE / c["input"]).read_bytes() == (V3 / c["input"]).read_bytes() for c in v3),
             "v3_representation_fields_changed": sorted(k for k, v in v3doc["representation"].items()
                                                        if doc["representation"].get(k) != v)}
    problems = {}
    for c in cases:
        raw, errs = (STAGE / c["input"]).read_bytes(), []
        if not raw.isascii() or b"\r" in raw or not raw.endswith(b"\n") or re.search(rb"[\x00-\x09\x0b-\x1f\x7f]", raw):
            errs.append("fixture not ASCII/LF/newline-terminated or has control characters")
        configparser.ConfigParser().read_file(io.StringIO(raw.decode("ascii")))  # must not raise
        if cm.canon(cm.interpret(raw.decode("ascii"))) != cm.canon(c["expected"]):
            errs.append("v2 interpretation cross-check disagrees")
        if errs:
            problems[c["id"]] = errs
    table, xr = r5_table(), x_records()
    vproblems, selection = check_new(cases[len(v3):], table, xr)
    for k, v in vproblems.items():
        problems.setdefault(k, []).extend(v)
    carried_values = check_carried(cases[:len(v3)], xr)
    man = json.loads((STAGE / "manifest.json").read_text())
    man["files"] = [{"path": str(p.relative_to(STAGE)), "sha256": b3.sha(p.read_bytes()), "bytes": p.stat().st_size}
                    for p in b3.payload(STAGE)]
    (STAGE / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    report = {"schema": "author-validation-v1", "package": "midi-config-v4 (staged candidate)",
              "python": sys.version.split()[0], "cases": len(cases), "case_problems": problems,
              "carried_from_v3": carry, "carried_value_cases": carried_values, "value_selection": selection,
              "rules": check_rules(), "near_band_tau_multiple": NEAR, "v3_lines_changed_or_removed": text_diff(),
              "evidence_identity": x2_identity(), "text_diff": "v3-to-v4-text.diff", **verify(STAGE),
              "limits": "Authored consistency only: no reference or candidate executed. Expected values of new cases are "
                        "the X results; the restatement and the r5 table share that evidence, so none is an oracle."}
    (HERE / "author-validation.json").write_text(json.dumps(report, indent=1) + "\n")
    t3 = json.loads((V3A / "traceability.json").read_text())
    trace = {"schema": "midi-config-v4-traceability", "status": "analyst-only; never part of the payload",
             "parent_spec": "SPEC-MIDI-USER-MAPPING revision 5 (wiki/specs/midi-user-mapping.md)",
             "plan": "wiki/specs/midi-config-v4-handoff-plan.md", "supersedes": "midi-config-v3",
             "evidence_identity": x2_identity(), "evidence": {**t3["evidence"], **EVIDENCE_NEW},
             "inferred": {**t3["inferred"], **INFERRED_NEW},
             "clauses": {k: {"evidence": e, "inferred": i} for k, (e, i) in CLAUSES.items()},
             "cases": {c["id"]: {"source": f"midi-config-v3 {c['id']} (record and fixture unchanged)", "evidence": ["v3"],
                                 **({"x_corroboration": f"{X2REL}results/mt.json {carried_values[c['id']]['row']} "
                                                        f"agrees within 1e-6: {carried_values[c['id']]['x_agrees']}"}
                                    if c["id"] in carried_values else {})} for c in v3},
             "excluded_spec_cases": EXCLUDED_ROWS}
    for n, mt, _, _ in NEW:
        trace["cases"][b3.cid(n)] = {"source": f"SPEC-MIDI-USER-MAPPING r5 {mt} (label X)", "x_result": X2REL + xr[mt]["source"],
                                     "evidence": ["E10", "E11", "E12", "E13", "E14", "E15", "E16"], "inferred": ["I2", "I3", "I4", "I6", "I7", "I8"],
                                     "near_bound_exception": n in NEAR_CASES, "value_scaling_move_case": n in MOVE_CASES}
    assert set(trace["cases"]) == {c["id"] for c in cases}
    (HERE / "traceability.json").write_text(json.dumps(trace, indent=1) + "\n")
    print(json.dumps({k: report[k] for k in ("cases", "case_problems", "carried_from_v3", "value_selection", "rules",
                                             "payload_files", "hash_or_size_mismatches", "inventory_differences",
                                             "unresolved_links", "missing_case_inputs", "deny_list_hits",
                                             "manifest_sha256")}, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        print(json.dumps(verify(sys.argv[2]), indent=1))
    else:
        assert sys.argv[1:] == ["seal"]
        seal()
