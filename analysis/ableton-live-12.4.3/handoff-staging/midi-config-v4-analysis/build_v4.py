"""Stage the midi-config-v4 release candidate (analyst side; not reviewed, not released).

Run with CPython 3.11 and -I (3.11.13, the host parser used for midi-config-v2 and v3):
  python3.11 -I build_v4.py build          # fixtures/, cases.json, manifest.json (files[] empty) in ../midi-config-v4/
  python3.11 -I seal_v4.py seal            # checks, manifest files[], author-validation.json, traceability.json, diff
  python3.11 -I seal_v4.py verify <dir>    # hashes, inventory, links, deny-list of an exported copy (absolute path)

Inputs (read only): the released midi-config-v3 package, carried unchanged (127 case records and fixture bytes);
build_v3.py, imported unchanged (fixture generator, decode tables, rounding, links, package verify); the
SPEC-MIDI-USER-MAPPING revision 5 MT table; the X2 packet r2/x2-midi-v1 (results/mt.json for MT-19 to MT-21,
acceptance-cases-x2.json for MT-24 to MT-56, manifest.json). New expected values are the X results rounded to nine
decimals. model4() is an exact-rational restatement of the value clauses in spec.md. seal_v4.py compares it, the
r5 table and the X results within tau, checks the two exception lists (tests near a bound, Value Scaling moves),
runs a mutation check, and checks fixtures, hashes, links and a deny-list. The restatement and the table rest on
the same evidence as X; none is an independent oracle. README.md, AGENTS.md and spec.md are hand-written.
"""
import configparser, difflib, io, json, re, struct, sys
from fractions import Fraction as Fr
from pathlib import Path

sys.dont_write_bytecode = True  # never write caches into the v3 or v2 analysis directories
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # repository root
STAGE = HERE.parent / "midi-config-v4"
V3 = ROOT / "handoff/midi-config-v3"
V3A = HERE.parent / "midi-config-v3-analysis"
X2 = ROOT / "analysis/ableton-live-12.4.3/r2/x2-midi-v1"
SPEC = ROOT / "wiki/specs/midi-user-mapping.md"
sys.path.insert(0, str(V3A))
import build_v3 as b3  # noqa: E402  (fixture, DECODE, nearest, links, payload, verify, crosscheck paths)

V3_MANIFEST_SHA = "2e7d93767bbb9fffa79cec191b242d7eec52aeb1d20f6f33f1bbdc0beff40458"
PROV_X = "extracted execution of the original x86_64 code (glibc substitutions); arm64 equivalence inferred"
NUM = b3.NUM  # controller number 20 on channel 0; the 14-bit LSB is 52
NEAR = 8      # a takeover test within NEAR * tau of its bound has no expectation outside NEAR_CASES
TAKEOVER = {"none": "none", "pickup": "pick-up", "scaling": "value-scaling"}

# (case number, r5 row, control, purpose); takeover, mode, parameter and messages come from X2 and the r5 table
NEW = [
    (128, "MT-19", "Encoder1", "Pick-Up: targets below the value are held until a move from the previous target crosses it, then targets apply"),
    (129, "MT-20", "Encoder1", "Value Scaling: the first message keeps the value; rising targets move it by the travelled fraction of the distance to max"),
    (130, "MT-21", "Encoder1", "Pick-Up: the first Absolute message after the input opens keeps the value"),
    (131, "MT-24", "Encoder1", "Pick-Up: targets above the value are held until a downward move crosses it"),
    (132, "MT-25", "Encoder1", "Pick-Up: one move from below the value to above it applies the target"),
    (133, "MT-26", "Encoder1", "Value Scaling: falling targets move the value by the travelled fraction of the distance to min"),
    (134, "MT-27", "Encoder1", "Value Scaling: a repeated data value keeps the value"),
    (135, "MT-28", "Encoder1", "Value Scaling: the first Absolute message after the input opens keeps the value"),
    (136, "MT-29", "Encoder1", "Pick-Up with a reversed range (min 1, max 0): the window uses the sorted bounds"),
    (137, "MT-30", "Encoder1", "Value Scaling with a reversed range (min 1, max 0): falling targets move the value toward the lower bound"),
    (138, "MT-31", "Encoder1", "Value Scaling with a reversed range (min 1, max 0): a rising target moves the value toward the upper bound"),
    (139, "MT-32", "Encoder1", "Pick-Up with a reversed range: a previous target within (hi - lo)/256 of the value applies the new target"),
    (140, "MT-33", "Encoder1", "Pick-Up with a reversed range (min 3, max -1): a value inside the window takes the target"),
    (141, "MT-34", "Encoder1", "Absolute14Bit, Pick-Up: the first pair after the input opens applies a target above the value"),
    (142, "MT-35", "Encoder1", "Absolute14Bit, Pick-Up: the first pair after the input opens keeps the value when its target is below it"),
    (143, "MT-36", "Encoder1", "Absolute14Bit, Value Scaling: the first pair after the input opens moves the value although its target is below it"),
    (144, "MT-37", "Encoder1", "Absolute14Bit, Value Scaling: a previous MSB without a previous LSB (even MSB) gives the previous data value -1"),
    (145, "MT-38", "Encoder1", "Absolute14Bit, Value Scaling: a previous LSB without a previous MSB gives the previous data value -128 + LSB/129"),
    (146, "MT-39", "Encoder1", "Absolute14Bit, Pick-Up: each later pair uses the data values that preceded its halves"),
    (147, "MT-40", "Encoder1", "Stepped parameter, Pick-Up: the previous target is rounded like the new one"),
    (148, "MT-41", "Encoder1", "Enumerated parameter, Pick-Up: the target applies directly"),
    (149, "MT-42", "Encoder1", "Pick-Up, range -129 to 0: a previous target of exactly -129 keeps the value"),
    (150, "MT-45", "CrossfaderSlider", "Crossfader Absolute14Bit, Pick-Up: the first pair is subject to takeover and keeps the value when its target is below it"),
    (151, "MT-46", "Encoder1", "Absolute under takeover none, range 20 to 999: values compared within the range-scaled tolerance"),
    (152, "MT-47", "Encoder1", "Value Scaling, range 0 to 127: a value exactly (max - min)/256 above the previous target is in sync"),
    (153, "MT-48", "Encoder1", "Value Scaling, range 0 to 127: one binary32 step farther above is not in sync, so the value moves"),
    (154, "MT-49", "Encoder1", "Value Scaling, range 0 to 127: a value exactly (max - min)/256 below the previous target is in sync"),
    (155, "MT-50", "Encoder1", "Value Scaling, range 0 to 127: one binary32 step farther below is not in sync, so the value moves"),
    (156, "MT-51", "Encoder1", "Pick-Up, range 0 to 127: a value exactly (max - min)/64 above the larger target is inside the window"),
    (157, "MT-52", "Encoder1", "Pick-Up, range 0 to 127: a value one binary32 step above the window keeps the value"),
    (158, "MT-53", "Encoder1", "Pick-Up, range 0 to 127: a value exactly (max - min)/64 below the smaller target is inside the window"),
    (159, "MT-54", "Encoder1", "Pick-Up, range 0 to 127: a value one binary32 step below the window keeps the value"),
    (160, "MT-55", "Encoder1", "Value Scaling, range 0 to 127: a target exactly (max - min)/64 from the value applies"),
    (161, "MT-56", "Encoder1", "Value Scaling, range 0 to 127: a target one binary32 step farther from the value moves it"),
]
NEAR_CASES = {149} | set(range(152, 162))           # spec.md: tests on or one step beyond a bound
MOVE_CASES = {129, 133, 137, 138, 143, 144, 145, 153, 155, 161}  # spec.md: cases that state a Value Scaling move
EXCLUDED_ROWS = {"MT-17": "S-cond: on/off thresholds (PRB-N7-04)", "MT-18": "S-cond: on/off, relative (PRB-N7-04)",
                 "MT-43": "S-cond: 14-bit on/off (PRB-N7-04)", "MT-44": "S-cond: on/off, reversed thresholds (PRB-N7-04)"}


# ---- inputs -----------------------------------------------------------------------------------------------
def r5_table():
    """MT rows of the revision 5 table: label, condition text, messages [(number, data)], values."""
    rows = {}
    pat = re.compile(r"^\|\s*(MT-\d\d)\s*\|\s*(S|S-cond|X)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")
    for line in SPEC.read_text().splitlines():
        m = pat.match(line)
        if m:
            msgs = [(NUM + 32, int(t[2:], 16)) if t.startswith("L:") else (NUM, int(t, 16)) for t in m[4].split()]
            rows[m[1]] = {"label": m[2], "condition": m[3], "messages": msgs, "values": m[5]}
    assert len(rows) == 56, len(rows)
    return rows


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def x_records():
    """X result per row: map mode, takeover, parameter, messages and values (binary32 as double)."""
    out = {}
    for c in json.loads((X2 / "results/mt.json").read_text())["cases"]:
        out[c["case"]] = {"mode": c["map_mode"], "takeover": c["takeover_settings_run"], "param": c["parameter"],
                          "input": c["input"], "x": c["x"], "source": f"results/mt.json {c['case']}"}
    for c in json.loads((X2 / "acceptance-cases-x2.json").read_text())["cases"]:
        out[c["id"]] = {"mode": c["map_mode"], "takeover": [c["takeover"]], "param": c["parameter"],
                        "input": c["input"], "x": c["expected_after_each_message"], "label": c["label"],
                        "source": f"acceptance-cases-x2.json {c['id']} (results/takeover.json {c['source_run']})"}
    return out


def num(x):
    return int(x) if float(x).is_integer() else x


def parameter(control, xp):
    kind = {"enum": "enumerated", "onoff": "on/off"}.get(xp["kind"], xp["kind"])
    return {"target": b3.ASSIGN[control]["target"], "kind": kind, "stepped": xp["quantized"],
            "min": num(xp["min"]), "max": num(xp["max"]), "initial_value": num(f32(xp["value"]))}


def tau(p):
    return max(Fr(1, 10 ** 6), Fr(1, 2 ** 22) * max(abs(Fr(p["min"])), abs(Fr(p["max"]))))


# ---- exact restatement of the released value clauses (spec.md "Value transforms") ------------------------------
def pair_previous(m, l):
    if m is not None and l is not None:
        return Fr(128 * m + l, 129)
    if m is None and l is None:
        return Fr(-1, 129)
    if m is None:
        return -128 + Fr(l, 129)
    return Fr(-1, 129) if m % 2 else Fr(-1)


def model4(control, mode, takeover, p, msgs, n=NUM):
    """Values after each message, the distances of takeover tests to their bounds, and the number of moves."""
    if p["kind"] == "on/off":
        raise b3.NoExpectation("on/off parameter")
    mn, mx, cur = (Fr(float(p[k])) for k in ("min", "max", "initial_value"))
    lo, hi = min(mn, mx), max(mn, mx)
    if mn == mx or not lo <= cur <= hi:
        raise b3.NoExpectation("range precondition")
    stepped = p["stepped"]
    if stepped and any(x.denominator != 1 for x in (mn, mx, cur)):
        raise b3.NoExpectation("stepped parameter with non-integer bound or value")
    if mode == "Absolute14Bit" and n > 95:
        mode = "Absolute"  # label rule
    exempt = (mode in b3.DECODE or p["kind"] in ("enumerated", "other")
              or (control == "CrossfaderSlider" and mode == "Absolute"))
    near, state = [], {"moves": 0}

    def target(x):
        t = mn + (mx - mn) * x / 127
        return b3.nearest(t) if stepped else t

    def take(x, xp):  # xp: previous data value, None when an Absolute message has none
        nv = target(x)
        if takeover == "none" or exempt:
            return nv
        if takeover not in ("pick-up", "value-scaling"):
            raise b3.NoExpectation("value subject to takeover without a named choice")
        c = cur
        if xp is None:
            return c
        pv, w = target(xp), (hi - lo) / 64
        near.append(abs(pv + 129))
        if pv == -129:
            return c
        near.append(abs(abs(pv - c) - (hi - lo) / 256))
        if abs(pv - c) <= (hi - lo) / 256:
            return nv
        if takeover == "pick-up":
            a, b = min(nv, pv) - w, max(nv, pv) + w
            near.extend((abs(c - a), abs(c - b)))
            return nv if a <= c <= b else c
        near.append(abs(abs(nv - c) - w))
        if abs(nv - c) <= w:
            return nv
        if xp != x:
            near.append(abs(pv - nv))
        if pv == nv:
            return c
        state["moves"] += 1
        return c + (hi - c) * (nv - pv) / (hi - pv) if nv > pv else c - (c - lo) * (pv - nv) / (pv - lo)

    last, held, out = {}, {}, []
    for number, v in msgs:
        before, last[number] = last.get(number), v
        if mode == "Absolute14Bit" and number in (n, n + 32):
            held["msb" if number == n else "lsb"] = (v, before)
            if len(held) == 2:
                (hm, pm), (hl, pl) = held["msb"], held["lsb"]
                cur = min(max(take(Fr(128 * hm + hl, 129), pair_previous(pm, pl)), lo), hi)
                held = {}
        elif number == n and mode == "Absolute":
            cur = min(max(take(Fr(v), None if before is None else Fr(before)), lo), hi)
        elif number == n:
            d = b3.DECODE[mode](v)
            step = (1 if d > 0 else -1) * (1 if mx > mn else -1) if stepped else (mx - mn) * Fr(d, 256)
            cur = min(max(cur + step, lo), hi)
        out.append(cur)
    return out, near, state["moves"]


# ---- payload -------------------------------------------------------------------------------------------------
def write(rel, data):
    path = STAGE / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def comparator(t):
    return ("exact assignment set over all fields; order immaterial; device_parameter_banks exact; values: parameter "
            "value after each message, in order, within tau = max(1e-6, 2^-22 * max(|min|, |max|)) = "
            f"{float(t)!r} absolute")


def new_case(n, mt, control, purpose, table, xr):
    r, x = table[mt], xr[mt]
    takeover = TAKEOVER[x["takeover"][0]]
    p = parameter(control, x["param"])
    meta = b3.ASSIGN[control]
    return {
        "id": b3.cid(n), "purpose": purpose, "origin": "new in midi-config-v4",
        "requirements": ["REQ-MIDI-USER-005"] + (["REQ-MIDI-USER-010"] if control == "CrossfaderSlider" else []),
        "input": f"fixtures/{b3.cid(n)}/UserConfiguration.txt",
        "stimulus": {"takeover": takeover, "parameter": p, "messages": ["B0 %02X %02X" % m for m in r["messages"]]},
        "expected": {"assignments": [{"section": meta["section"], "control": control, "target": meta["target"],
                                      "message_type": "control-change", "number": NUM, "channel": 0,
                                      "map_mode": x["mode"]}],
                     "device_parameter_banks": meta["banks"], "values": [round(v, 9) for v in x["x"]]},
        "expectation_provenance": PROV_X, "reference_execution": "not-run", "candidate_execution": "not-run",
        "comparator": comparator(tau(p)),
    }


def manifest_meta(case_count):
    v3 = json.loads((V3 / "manifest.json").read_text())
    ex = v3["exclusions"]
    drop_inputs = {
        "a target parameter reporting a minimum equal to or above its maximum; a stepped parameter with a non-integer minimum, maximum or current value; a current value outside the range; a parameter that changes a value after it is set",
        "under a takeover choice other than none: Absolute and Absolute14Bit values for a continuous parameter, except Absolute values of the crossfader (crossfader Absolute14Bit values included)",
        "other MIDI input during a value case, including running status"}
    drop_behavior = {"Pick-Up and Value Scaling takeover, the labels of the takeover choices other than none, and the default choice"}
    inputs = [x for x in ex["inputs_without_expectation"] if x not in drop_inputs]
    behavior = [x for x in ex["behavior"] if x not in drop_behavior]
    assert len(inputs) == len(ex["inputs_without_expectation"]) - 3 and len(behavior) == len(ex["behavior"]) - 1
    scopes = dict(v3["partial_requirement_scopes"])
    scopes["REQ-MIDI-USER-005"] = (
        "Map-mode labels: ten exact tokens, absent default, key scope, 14-bit label above CC 95; value transforms of "
        "Absolute, Absolute14Bit and the eight relative modes for continuous, enumerated and other parameters, for "
        "either range order; the three takeover choices by preference position; Pick-Up and Value Scaling with "
        "previous data values, the previous value of a 14-bit pair and the sorted bounds; the values exempt from "
        "takeover; value tolerance tau")
    scopes["REQ-MIDI-USER-010"] = (
        "Master/cue/crossfader targets and their map-mode keys; their values follow the REQ-MIDI-USER-005 transforms; "
        "crossfader Absolute values exempt from takeover, crossfader Absolute14Bit pairs subject to it")
    labels = json.loads((V3 / "cases.json").read_text())["cases"][0]["expectation_provenance"]
    return {
        "schema": "handoff-manifest-v1", "release_id": "midi-config-v4", "release_status": "candidate-unreviewed",
        "release_date": None, "target": b3.TARGET,
        "specification": {"id": "SPEC-MIDI-USER-MAPPING", "parent_revision": 5, "release_revision": 5},
        "feature_ids": ["FEAT-MIDI-USER-MAPPING"],
        "partial_requirement_scopes": scopes,
        "unreleased_requirements": v3["unreleased_requirements"],
        "compatibility_dimensions": {
            **v3["compatibility_dimensions"],
            "parameter-values": "static-derived and extracted-execution values in value cases, compared within tau; "
                                "reference execution not-run",
        },
        "expectation_provenance_labels": {
            labels: "derived from evidence about the pinned build, reviewed before sanitization; cases MIDI-CONFIG-001 to 127",
            PROV_X: "the original program's x86_64 code that turns each Control Change message into a parameter value "
                    "(message and 14-bit half handling, the value computation and takeover) ran on the case's messages "
                    "on a Linux x86_64 host, with glibc in place of the macOS system libraries; the run supplied the "
                    "target parameter and the previous data values; the interpreted assignments, the previous-value "
                    "rules and the takeover choice positions remain static-derived; cases MIDI-CONFIG-128 to 161",
        },
        "exclusions": {
            "inputs_without_expectation": inputs + [
                "a target parameter whose minimum equals its maximum; a stepped parameter with a non-integer minimum, maximum or current value; a current value outside the closed interval between minimum and maximum; a parameter that changes a value after it is set",
                "a Value Scaling move (the value moved by the travelled fraction), and every later value of its sequence, except in cases MIDI-CONFIG-129, 133, 137, 138, 143 to 145, 153, 155 and 161",
                "a takeover comparison or test whose two sides lie within 8 tau of each other, other than p = n for one and the same data value, and every later value of its sequence, except in cases MIDI-CONFIG-149 and 152 to 161",
                "other MIDI input during a value case, including running status; anything else that empties the record of previous data values, such as another control surface on the same input",
            ],
            "behavior": behavior + [
                "the default takeover choice, the displayed wording of the three choices, and any notification or display while takeover holds a value",
            ],
        },
        "stated_assumptions": [
            "The macOS arm64 build computes the extracted-execution values as the x86_64 build does, except that it rounds once where the x86_64 build rounds twice when it forms the target value of an absolute message; the results then differ by at most one binary32 unit in the last place of max(|min|, |max|), none when the smaller bound is 0, which tau covers. Cases MIDI-CONFIG-128 to 161 depend on it.",
            "The application passes this code the parameter's reported range, kind and stepping, its current value and the previous data values as the contract states them, and the parameter keeps the value set on it. Every value case depends on it.",
            "The three preference entries, which select none, pick-up and value-scaling by position, display as None, Pick-Up and Value Scaling; their wording was not read. Only the labels used in a reference run depend on it.",
        ],
        "value_tolerance": "tau = max(1e-6, 2^-22 * max(|min|, |max|)) absolute, with the case parameter's min and max; 1e-6 for cases MIDI-CONFIG-110 to 127",
        "fixture_origin": v3["fixture_origin"],
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None, "record": None},
        "supersedes": "midi-config-v3",
        "supersession": {
            "relationship": "strict superset on publication; midi-config-v3 stays immutable and valid for its narrower scope",
            "superseded_manifest_sha256": V3_MANIFEST_SHA,
            "restated_cases": "MIDI-CONFIG-001 to 127: case records and fixture bytes identical to midi-config-v3",
            "corrected_expectations": "none; parent revision 5 corrected no expectation of a midi-config-v3 case",
            "changes": CHANGES,
        },
        "entrypoint": "README.md", "case_count": case_count,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


CHANGES = [
    "REQ-MIDI-USER-005 takeover: Pick-Up and Value Scaling specified, with the record of previous data values, the previous value of a 14-bit pair, the sorted bounds and inclusive comparisons; the three choices named none, pick-up and value-scaling and selected by preference position",
    "the midi-config-v3 assumption that the never-acting choice is the one labelled None is narrowed: which entry selects which choice is now static-derived; only the displayed wording is assumed",
    "reversed ranges: min below max is no longer required; Absolute, Absolute14Bit and relative values and takeover hold for either order, a stepped relative step moves toward max when d > 0",
    "REQ-MIDI-USER-010: crossfader Absolute14Bit pairs are subject to takeover (midi-config-v3 left them without expectation under the other two choices)",
    "value tolerance tau = max(1e-6, 2^-22 * max(|min|, |max|)) replaces 1e-6; tau is 1e-6 for every midi-config-v3 case",
    "stepped rounding: a Value Scaling move is not rounded",
    "exclusions: removed values subject to takeover under the choices other than none, and min above max; min equal to max stays excluded; added tests within 8 tau of a bound and Value Scaling moves outside the listed cases, with the later values of their sequences, and anything that empties the record of previous data values; the default choice stays excluded, the displayed wording of the choices and any takeover notification are listed",
    "provenance: the extracted-execution label is new and carried by every new case; carried cases keep the static-derived label; stated assumptions revised",
    "representation: takeover gains pick-up and value-scaling; the initial value is stated to be a binary32 number; the values note and new comparators state tau",
    "cases MIDI-CONFIG-128 to 161 added (34 value cases)",
    "no midi-config-v3 case, fixture or expectation changed; nothing in midi-config-v3 is contradicted; the sentences that left takeover unspecified now point to the new rules",
]


def build():
    v3 = json.loads((V3 / "cases.json").read_text())
    table, xr = r5_table(), x_records()
    cases = []
    for c in v3["cases"]:
        write(c["input"], (V3 / c["input"]).read_bytes())
        cases.append(c)
    for n, mt, control, purpose in NEW:
        write(f"fixtures/{b3.cid(n)}/UserConfiguration.txt", b3.fixture(control, xr[mt]["mode"]))
        cases.append(new_case(n, mt, control, purpose, table, xr))
    rep = dict(v3["representation"])
    rep.update({
        "stimulus": "value cases only: takeover (none, pick-up, value-scaling, or any = every takeover choice); parameter "
                    "(target, kind, stepped, min, max, initial_value, a binary32 number); messages (three-byte Control "
                    "Change messages in hexadecimal, applied in order)",
        "values": "value cases only: expected.values, the target parameter value after each message rounded to nine "
                  "decimals (exact results for static-derived cases, extracted-execution results otherwise), compared "
                  "within tau = max(1e-6, 2^-22 * max(|min|, |max|)) absolute; tau is 1e-6 for cases 110 to 127",
    })
    doc = {"schema": "midi-config-cases-v4", "target": b3.TARGET,
           "scope": "midi-config-v4 partial requirement clauses only (see spec.md)", "status": "candidate-unreviewed",
           "fixture_origin": v3["fixture_origin"],
           "oracle_status": "Static-derived and extracted-execution expectations, labeled per case; neither reference "
                            "nor candidate executed",
           "representation": rep, "cases": cases}
    (STAGE / "cases.json").write_text(json.dumps(doc, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_meta(len(cases)), indent=1) + "\n")
    print(len(cases), "cases staged")



if __name__ == "__main__":
    assert sys.argv[1:] == ["build"], "usage: build_v4.py build  (seal and verify: seal_v4.py)"
    build()
