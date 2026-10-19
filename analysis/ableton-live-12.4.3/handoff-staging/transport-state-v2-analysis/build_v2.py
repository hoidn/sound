"""Stage the transport-state-v2 handoff candidate (analyst side; not reviewed, not released).

Run with CPython 3 and -I from anywhere:
  python3 -I build_v2.py build          # fixtures/, cases.json, draft manifest.json, traceability.json, diff
  python3 -I build_v2.py seal           # manifest files[] + checks -> author-validation.json
  python3 -I build_v2.py verify <dir>   # same checks against an exported copy (no manifest rewrite)

Inputs: the released handoff/transport-state-v1 (carried case records and fixture bytes), the v1 build
script (fixture generator and judge, imported unchanged), and the X evidence in
analysis/ableton-live-12.4.3/r2/x2-transport-v1/results (for the extracted-execution cases).
spec.md, README.md and AGENTS.md are hand-written. The model() below is an independent re-reading of the
v2 clauses used to cross-check the expectations; it is not an oracle. The X check compares each new
expectation with the result the original x86_64 code gave.
"""
import difflib, hashlib, json, math, re, shutil, struct, sys
from decimal import Decimal, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = HERE.parent / "transport-state-v2"
V1 = ROOT / "handoff/transport-state-v1"
X2 = ROOT / "analysis/ableton-live-12.4.3/r2/x2-transport-v1"
sys.path.insert(0, str(HERE.parent / "transport-state-v1-analysis"))
sys.dont_write_bytecode = True  # never write a cache into the v1 analysis directory
import build_ts1 as v1  # noqa: E402  (doc, edit, ORDER, judge, links, f32: reused unchanged)

R = "REQ-TRANSPORT-STATE-"
PROV_X = "extracted execution (x86_64 slice, glibc substitutions); arm64 equivalence inferred"
COMPARATOR = v1.COMPARATOR
D63 = "0" * 60 + "201"

# id, kind, requirements, purpose, fixture text, action, expected
NEW = [
    ("TS-010", "negative", ["006"], "Time-signature code text with spaces on both sides and a + is refused",
     v1.doc(tsig='<Manual Value=" +201 " />'), "open", {"outcome": "refused"}),
    ("TS-024", "save", ["004", "011"], "A loop start just above 100 is saved with one more digit than the exact logarithm gives",
     v1.doc(v1.edit("LoopStart", "100.00000000000001")), "open-save",
     {"outcome": "opens", "state": {"loop_start": 100.00000000000001},
      "saved": {"values": {"Transport/LoopStart": "100.000000000000014"}}}),
    ("TS-025", "save", ["004", "011"], "A loop length just above 1000 is saved with one more digit than the exact logarithm gives",
     v1.doc(v1.edit("LoopLength", "1000.0000000000001")), "open-save",
     {"outcome": "opens", "state": {"loop_length": 1000.0000000000001},
      "saved": {"values": {"Transport/LoopLength": "1000.00000000000011"}}}),
    ("TS-026", "save", ["004", "011"], "A position just below 0.1 is saved with one fewer digit than the exact logarithm gives",
     v1.doc(v1.edit("CurrentTime", "0.09999999999999999")), "open-save",
     {"outcome": "opens", "state": {"current_time": 0.09999999999999999},
      "saved": {"values": {"Transport/CurrentTime": "0.099999999999999992"}}}),
    ("TS-027", "save", ["004", "011"], "Loop start 0.000001 (stored just below 10^-6) is saved with one fewer digit",
     v1.doc(v1.edit("LoopStart", "0.000001")), "open-save",
     {"outcome": "opens", "state": {"loop_start": 1e-06},
      "saved": {"values": {"Transport/LoopStart": "0.00000099999999999999995"}}}),
    ("TS-028", "boundary", ["004", "011"], "Loop start -0 reads as negative zero and is saved as -0",
     v1.doc(v1.edit("LoopStart", "-0")), "open-save",
     {"outcome": "opens", "saved": {"values": {"Transport/LoopStart": "-0"}}}),
    ("TS-029", "negative", ["006"], "Time-signature code text with + and a trailing space is refused",
     v1.doc(tsig='<Manual Value="+201 " />'), "open", {"outcome": "refused"}),
    ("TS-030", "positive", ["006"], "Time-signature code text -0 is accepted as code 0",
     v1.doc(tsig='<Manual Value="-0" />'), "open", {"outcome": "opens"}),
    ("TS-031", "negative", ["006"], "Time-signature code text beyond the 32-bit integer range is refused",
     v1.doc(tsig='<Manual Value="2147483648" />'), "open", {"outcome": "refused"}),
    ("TS-032", "boundary", ["006"], "A 63-character code body followed by a space is accepted",
     v1.doc(tsig=f'<Manual Value="{D63} " />'), "open", {"outcome": "opens"}),
    ("TS-033", "negative", ["006"], "A 64-character code body (minus sign and 63 digits) is refused",
     v1.doc(tsig=f'<Manual Value="-{"0" * 63}" />'), "open", {"outcome": "refused"}),
    ("TS-034", "positive", ["004"], "Loop length text with spaces on both sides and a + sign reads as 4.5",
     v1.doc(v1.edit("LoopLength", " +4.5 ")), "open", {"outcome": "opens", "state": {"loop_length": 4.5}}),
    ("TS-035", "negative", ["004"], "Loop start text with a space between sign and digits is refused",
     v1.doc(v1.edit("LoopStart", "- 4.5")), "open", {"outcome": "refused"}),
    ("TS-036", "positive", ["004"], "Loop start # form with 16 hex digits reads as those bits",
     v1.doc(v1.edit("LoopStart", "#4012000000000000")), "open", {"outcome": "opens", "state": {"loop_start": 4.5}}),
    ("TS-037", "positive", ["005"], "Tempo # form with 8 lowercase hex digits reads as those bits",
     v1.doc(tempo='<Manual Value="#42f00000" />'), "open", {"outcome": "opens", "state": {"tempo": 120.0}}),
]
ORDER_IDS = ["TS-%03d" % i for i in range(1, 38)]

# X evidence for each new case: (kind, text) of the text conversion in parse.json, and (kind, value) of the
# writer run in writer.json when a saved text is judged.
X_EVIDENCE = {
    "TS-010": [("int", " +201 ")], "TS-029": [("int", "+201 ")], "TS-030": [("int", "-0")],
    "TS-031": [("int", "2147483648")], "TS-032": [("int", D63 + " ")], "TS-033": [("int", "-" + "0" * 63)],
    "TS-024": [("double", "100.00000000000001"), ("write-double", 100.00000000000001)],
    "TS-025": [("double", "1000.0000000000001"), ("write-double", 1000.0000000000001)],
    "TS-026": [("double", "0.09999999999999999"), ("write-double", 0.09999999999999999)],
    "TS-027": [("double", "0.000001"), ("write-double", 1e-06)],
    "TS-028": [("double", "-0"), ("write-double", -0.0)],
    "TS-034": [("double", " +4.5 ")], "TS-035": [("double", "- 4.5")], "TS-036": [("double", "#4012000000000000")],
    "TS-037": [("float", "#42f00000")],
}
# Carried cases whose conversion step the same evidence (and the X1 pilot) also ran; records unchanged.
X_CORROBORATES = {
    "TS-001": [("bool", "true"), ("write-bool", None)], "TS-002": [("bool", "1")], "TS-003": [("bool", "0")],
    "TS-004": [("bool", "TRUE")], "TS-005": [("bool", "")], "TS-006": [("double", "4.5abc"), ("write-double", 4.5)],
    "TS-007": [("double", "abc")], "TS-008": [("float", "93.3333333"), ("write-float", 93.3333333)],
    "TS-009": [("int", "201.0")], "TS-020": [("float", "121.2"), ("write-float", 121.2)],
    "TS-021": [("double", "0.3"), ("write-double", 0.3)],
}


# ---- independent cross-check model of the v2 clauses (not an oracle) ----
Refused, Excluded = v1.Refused, v1.Excluded
getcontext().prec = 80


def read_number(text, single):
    rest = text.lstrip(" ").lstrip("+-").lower()
    if text == "Invalid" or rest.startswith(("0x", "inf", "nan")) or re.match(r"^ *[^\S ]", text):
        raise Excluded(text)
    if len(text) == (9 if single else 17) and text[0] == "#" and re.fullmatch(r"[0-9A-Fa-f]+", text[1:]):
        b = bytes.fromhex(text[1:])
        return struct.unpack(">f" if single else ">d", b)[0]
    m = re.match(r"^ *([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)", text)
    if not m:
        raise Refused(text)
    return v1.f32(float(m.group(1))) if single else float(m.group(1))


def read_int(text):
    if not text.isascii():
        raise Refused(text)
    lead = len(text) - len(text.lstrip(" "))
    core = text[lead:]
    plus = core.startswith("+")
    core = core[1:] if plus else core
    body = core.rstrip(" ")
    trail = len(core) - len(body)
    if (not re.fullmatch(r"-?\d+", body) or len(body) > 63 or (plus and body.startswith("-"))
            or (trail and (lead or plus))):
        raise Refused(text)
    value = int(body)
    if not -2 ** 31 <= value < 2 ** 31:
        raise Refused(text)
    if not 0 <= value <= 494:
        raise Excluded(text)
    return value


def fmt(x, p):
    if x == 0:
        return "-0" if math.copysign(1, x) < 0 else "0"
    lg = Decimal(abs(x)).log10()
    n = int(lg.to_integral_value())
    if lg != n:
        nf = float(n)
        side = math.nextafter(nf, math.inf if lg > n else -math.inf)
        gap = Decimal(abs(side - nf))
        if Decimal(1) / 4 <= abs(lg - n) / gap <= Decimal(3) / 4:
            raise Excluded(f"log10 near half a gap: {x!r}")
    L = float(lg)
    k = math.floor(L) if L < 0 else math.ceil(L)
    s = "%.*f" % (max(0, p - k), x)
    return s.rstrip("0").rstrip(".") if "." in s else s


def model(xml_text):
    """Return (outcome, state, saved_xml_root or None); v1.model with the v2 readers and writer."""
    saved_v1 = (v1.read_number, v1.read_int, v1.fmt)
    v1.read_number, v1.read_int, v1.fmt = read_number, read_int, fmt
    try:
        return v1.model(xml_text)
    finally:
        v1.read_number, v1.read_int, v1.fmt = saved_v1


# ---- X evidence lookup ----
def x_results():
    parse = json.loads((X2 / "results/parse.json").read_text())
    writer = json.loads((X2 / "results/writer.json").read_text())
    conv = {(r["kind"], r["text"]): r for r in parse["int"] + parse["number_and_bool"]}
    writes = {(r["kind"], r["x"]): r for r in writer["attribute_writer_specials"] + writer["attribute_writer_case_values"]}
    return conv, writes


def x_check(case, ev, conv, writes):
    """Compare one case's expectation with the X results it cites. Returns a list of problems."""
    errs, exp = [], case["expected"]
    state_key = {"Transport/LoopStart": "loop_start", "Transport/LoopLength": "loop_length",
                 "Transport/CurrentTime": "current_time"}
    for kind, arg in ev:
        if kind.startswith("write-"):
            if kind == "write-bool":
                continue                      # Boolean writer not run; text is the literal token
            r = writes.get((kind[6:], repr(v1.f32(arg) if kind == "write-float" else arg)))
            if r is None:
                r = writes.get((kind[6:], repr(arg)))
            saved = list(exp.get("saved", {}).get("values", {}).values())
            got = [w["text"] for w in r["writes"]] if r else None
            if not r or got != saved[:1]:
                errs.append(f"writer {arg!r}: X {got} vs expected {saved}")
            continue
        r = conv.get((kind, arg))
        if r is None:
            errs.append(f"no X record for {kind} {arg!r}")
        elif exp["outcome"] == "refused":
            if r["result"] != "refused":
                errs.append(f"{kind} {arg!r}: X {r['result']} but case refused")
        else:
            if r["result"] != "value":
                errs.append(f"{kind} {arg!r}: X refused but case opens")
            for k, v in exp.get("state", {}).items():
                xv = float(r["value"]) if kind in ("double", "float") else r["value"]
                if k in state_key.values() or k == "tempo":
                    if xv != v:
                        errs.append(f"{kind} {arg!r}: X {xv!r} vs state {k}={v!r}")
            if kind == "double" and arg == "-0" and r.get("bits") != "8000000000000000":
                errs.append("-0 did not read as negative zero")
    return errs


# ---- packaging ----
def sha(b):
    return hashlib.sha256(b).hexdigest()


def manifest_skeleton(n_cases):
    v1m = json.loads((V1 / "manifest.json").read_text())
    scopes = dict(v1m["partial_requirement_scopes"])
    scopes.update({
        R + "004": "Decimal-prefix reading with leading spaces skipped and trailing text ignored; nearest binary64; "
                   "# with 16 hex digits of either case reads raw bits, most significant first; no prefix refused",
        R + "005": "Tempo read as REQ-004 then rounded to nearest binary32; # with 8 hex digits reads raw bits",
        R + "006": "Five-condition integer rule (ASCII; optional - and digits, at most 63 characters; no +-; no "
                   "trailing spaces after leading spaces or +; 32-bit range); accepted codes outside 0-494 excluded",
        R + "011": "Boolean and integer text; fixed-precision decimal text with P=17 or 9, k from the binary64 "
                   "logarithm, for in-range finite values; positive and negative zero",
    })
    return {
        "schema": "handoff-manifest-v1",
        "release_id": "transport-state-v2",
        "release_status": "staged candidate; not reviewed; not released",
        "release_date": None,
        "target": v1.TARGET,
        "specification": {"id": "SPEC-TRANSPORT-STATE", "parent_revision": 3, "release_revision": 3},
        "feature_ids": ["FEAT-TRANSPORT", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": scopes,
        "unreleased_requirements": [R + "009", R + "012"],
        "compatibility_dimensions": {
            "project-files": "static-derived and extracted-execution expectations for the listed document values; "
                             "reference execution not-run",
            "behavior": "effective transport state after opening excluded",
            "audio": "excluded", "ui": "excluded", "timing": "excluded",
        },
        "expectation_provenance_labels": {
            "static-derived; not observed reference output": "derived from evidence reviewed before sanitization",
            PROV_X: "the value's text conversion in the original program's x86_64 build ran on the case's text on a "
                    "Linux x86_64 host, with glibc in place of the macOS system libraries; locating, opening and "
                    "saving remain static-derived",
        },
        "stated_assumptions": [
            "The macOS arm64 build converts these texts as the x86_64 build does. All cases with the "
            "extracted-execution label depend on it.",
            "The reference's binary64 base-10 logarithm errs by less than 0.8 of a binary64 gap at the values of "
            "TS-024 to TS-027, whose logarithms lie 0.02 to 0.17 gaps from an integer. With that error the result "
            "is the integer, as it is in the correctly rounded result and in the glibc run.",
            "The reference's decimal reading of TS-034 and TS-035 follows the C-standard number grammar in a locale "
            "whose decimal separator is '.', as the glibc run did.",
            "Exact decimal ties on save round to even (as in transport-state-v1); no case lies on a tie.",
        ],
        "exclusions": {
            "inputs_without_expectation": [
                "number text starting (after spaces and sign) with 0x, inf or nan; Invalid; leading whitespace other than U+0020",
                "values outside the spec.md ranges (negative zero counts as zero); non-finite and largest finite values",
                "saved binary64 values whose log10 is not an integer but lies between 1/4 and 3/4 of a binary64 gap from one",
                "accepted time-signature codes outside 0 to 494",
                "missing TimeSignature/Manual or its value; missing Transport, Tempo, TimeSignature, Mixer, DeviceChain or MainTrack",
                "unknown attributes on any element this release reads; repeated unknown children; any *KeyMidi child in the input; LoopIsSongStart other than false",
                "automation events or scene values that disagree with Manual",
                "other envelopes, format versions, compressed containers and document kinds",
            ],
            "behavior": v1m["exclusions"]["behavior"],
            "parent_cases_not_released": ["TS-017", "TS-018", "TS-019", "TS-023"],
        },
        "fixture_origin": v1m["fixture_origin"],
        "approved_public_sources": [],
        "review": {"status": "pending", "reviewers": [], "date": None, "findings": [], "disposition": None,
                   "record": None},
        "supersedes": "transport-state-v1",
        "supersession": {
            "relationship": "superset on publication; transport-state-v1 stays immutable and valid for its own scope; "
                            "its REQ-011 step 1 is exact only within that scope",
            "superseded_manifest_sha256": sha((V1 / "manifest.json").read_bytes()),
            "restated_cases": "TS-001 to 009, 011 to 016, 020 to 022: case records and fixture bytes identical to transport-state-v1",
            "changes": [
                "REQ-011 step 1: k from the logarithm rounded to binary64 instead of the exact logarithm (differs only "
                "next to powers of ten, which v1 excluded); cases TS-024 to TS-027",
                "REQ-011 and REQ-004: negative zero written -0 and read from -0; the negative-zero exclusion removed; TS-028",
                "REQ-006 restated as five conditions; spellings v1 excluded (spaces on both sides, + with trailing spaces, "
                "- sign, long text ending in a space) decided; TS-010, TS-029 to TS-033",
                "REQ-004 and REQ-005: # forms with exactly 16 or 8 hex digits of either case; other # text refused; "
                "TS-034 to TS-037",
                "exclusion near integer logarithms narrowed from within 1e-12 to between 1/4 and 3/4 of a binary64 gap; "
                "accepted codes outside 0 to 494 excluded",
                "provenance label extracted execution added; carried records unchanged",
            ],
        },
        "entrypoint": "README.md",
        "case_count": n_cases,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"],
        "files": [],
    }


def traceability(cases):
    rx = "analysis/ableton-live-12.4.3/r2/x2-transport-v1/results/"
    loc = {"int": rx + "parse.json int[text]", "bool": rx + "parse.json number_and_bool[kind=bool,text]",
           "double": rx + "parse.json number_and_bool[kind=double,text]",
           "float": rx + "parse.json number_and_bool[kind=float,text]",
           "write-double": rx + "writer.json attribute_writer_*[kind=double,x]",
           "write-float": rx + "writer.json attribute_writer_*[kind=float,x]",
           "write-bool": "not run (literal token)"}
    out = {"schema": "transport-state-v2-traceability-v1", "spec": "SPEC-TRANSPORT-STATE r3",
           "x_evidence": {"manifest": "analysis/ableton-live-12.4.3/r2/x2-transport-v1/manifest.json",
                          "research": "wiki/research/transport-state-native.md#extracted-execution-results-x2-2026-10-18",
                          "functions": "analysis/ableton-live-12.4.3/r2/x2-transport-v1/addresses.json",
                          "substitutions": "glibc 2.39 log10, vsnprintf (C locale), strtod; integer path original code only"},
           "static_evidence": {"v1_plan": "wiki/specs/transport-state-handoff-plan.md#evidence-traceability",
                               "v1_review": "handoff/transport-state-v1/REVIEW.md"},
           "clauses": {
               "004 # form": "x86 converter double branch: 17-character # check, hex mask for A-F and a-f, byte swap "
                             "(parse.json #4012000000000000, #3ff0000000000000, #8000000000000000; wrong lengths refused); "
                             "arm64 0x10152bfb8 same structure (n1-0006)",
               "004 sign and spaces": "glibc strtod through the original consumption check (parse.json ' +4.5 ', '- 4.5', "
                                      "'+-4.5', '+', '-'); inference: C-standard grammar on macOS",
               "005 # form": "x86 converter float branch: 9-character check (parse.json #42f00000, #42F00000)",
               "006": "x86 parser 0x100375650 and converter 0x10151b630 on 72 texts, no library substituted; arm64 "
                      "0x1002fd908 window min(len - start, len - trailing) and limit 63 identical (n1-0006 disassembly)",
               "011 k": "x86 formatters 0x10142b6c0/0x10142b980 on 6,539 values: correctly rounded L model 6,528/6,539, "
                        "exact-logarithm model 5,714/6,539, glibc L model 6,539/6,539 (writer.json sweep); arm64 "
                        "0x101431584/0x101431788 same branch structure (n1-0007)",
               "011 zero": "x86 writers 0x10150f6a0/0x10150f7a0 with -0.0 -> '-0' (writer.json specials); zero test "
                           "true for -0.0 in both slices",
           },
           "cases": {}}
    for c in cases:
        cid = c["id"]
        entry = {"requirements": c["requirements"], "provenance": c["expectation_provenance"]}
        if cid in X_EVIDENCE:
            entry["x_evidence"] = [f"{loc[k]} = {a!r}" for k, a in X_EVIDENCE[cid]]
            entry["static_steps"] = "field location, open and save outcome as in transport-state-v1 (plan traceability)"
        else:
            entry["static_evidence"] = "transport-state-v1, same case record (plan traceability and review)"
            if cid in X_CORROBORATES:
                entry["x_corroboration"] = [f"{loc[k]} = {a!r}" for k, a in X_CORROBORATES[cid]]
        out["cases"][cid] = entry
    return out


def text_diff():
    out = []
    for name in ("README.md", "AGENTS.md", "spec.md"):
        a = (V1 / name).read_text().splitlines(keepends=True)
        b = (STAGE / name).read_text().splitlines(keepends=True)
        out += difflib.unified_diff(a, b, f"transport-state-v1/{name}", f"transport-state-v2/{name}")
    return "".join(out)


def build():
    shutil.rmtree(STAGE / "fixtures", ignore_errors=True)
    (STAGE / "fixtures").mkdir(parents=True)
    v1cases = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
    regenerated = {cid: text for cid, _, _, _, text, _, _ in v1.CASES}
    cases = []
    new = {n[0]: n for n in NEW}
    for cid in ORDER_IDS:
        if cid in v1cases:
            c = v1cases[cid]
            raw = (V1 / c["input"]).read_bytes()
            assert raw == regenerated[cid].encode(), f"v1 generator does not reproduce {cid}"
            (STAGE / c["input"]).write_bytes(raw)
            cases.append(c)
        elif cid in new:
            _, kind, reqs, purpose, text, action, expected = new[cid]
            rel = f"fixtures/{cid}.xml"
            (STAGE / rel).write_text(text)
            cases.append({"id": cid, "kind": kind, "purpose": purpose, "requirements": [R + r for r in reqs],
                          "input": rel, "action": action, "expected": expected, "expectation_provenance": PROV_X,
                          "reference_execution": "not-run", "candidate_execution": "not-run",
                          "comparator": COMPARATOR[action]})
    v1doc = json.loads((V1 / "cases.json").read_text())
    (STAGE / "cases.json").write_text(json.dumps({
        "schema": v1doc["schema"], "target": v1doc["target"],
        "scope": "transport-state-v2 partial requirement clauses only (see spec.md)",
        "status": "staged candidate; not reviewed; not released",
        "fixture_origin": v1doc["fixture_origin"],
        "oracle_status": "Static-derived and extracted-execution expectations (label per case); neither the reference "
                         "application nor a candidate executed",
        "representation": v1doc["representation"],
        "cases": cases}, indent=1) + "\n")
    (STAGE / "manifest.json").write_text(json.dumps(manifest_skeleton(len(cases)), indent=1) + "\n")
    (HERE / "traceability.json").write_text(json.dumps(traceability(cases), indent=1) + "\n")
    (HERE / "v1-to-v2-text.diff").write_text(text_diff())
    print(len(cases), "cases staged")


ALLOWED = [PROV_X, "x86_64 build", "x86_64 host", "macOS arm64 build", "glibc in place of the macOS system libraries",
           "the glibc run"]  # wording of the provenance label and its definition
DENY = v1.DENY + [r"xexec", r"\bX[12]\b", r"x[12]-", r"extracted-execution\.md", r"from_chars", r"vsnprintf", r"strtod",
                  r"[Ss]etValue", r"\bgdb\b", r"harness", r"\bstubs?\b", r"\btrap", r"\bslice", r"glibc", r"x86",
                  r"cvtsd2ss|fcvt|frint|roundsd", r"0x[0-9a-f]{6,}", r"\bREVIEW\.md\b"]


def mutation_check(cases, conv, writes):
    """Each new case with one expectation changed must be caught by the model or the X check."""
    caught = 0
    for c in cases:
        if c["id"] not in X_EVIDENCE:
            continue
        m = json.loads(json.dumps(c))
        e = m["expected"]
        if e.get("saved"):
            path = next(iter(e["saved"]["values"]))
            e["saved"]["values"][path] += "0" if "." in e["saved"]["values"][path] else ".5"
        else:
            m["expected"] = {"outcome": "opens"} if e["outcome"] == "refused" else {"outcome": "refused"}
        raw = (STAGE / c["input"]).read_text()
        outcome, state, saved = model(raw)
        if v1.judge(m["expected"], outcome, state, saved) and x_check(m, X_EVIDENCE[c["id"]], conv, writes):
            caught += 1
    return caught


def check(pkg, rewrite):
    pkg = pkg.resolve()
    doc_ = json.loads((pkg / "cases.json").read_text())
    conv, writes = x_results()
    v1cases = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
    problems, x_problems = {}, {}
    for c in doc_["cases"]:
        raw = (pkg / c["input"]).read_bytes()
        errs = [] if raw.isascii() and b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n") else ["format"]
        try:
            outcome, state, saved = model(raw.decode("ascii"))
            errs += v1.judge(c["expected"], outcome, state, saved)
        except Excluded as e:
            errs.append(f"fixture hits an exclusion: {e}")
        if errs:
            problems[c["id"]] = errs
        if c["id"] in X_EVIDENCE:
            xe = x_check(c, X_EVIDENCE[c["id"]], conv, writes)
            if xe:
                x_problems[c["id"]] = xe
    carried = [cid for cid in v1cases]
    carry_diff = [cid for cid in carried
                  if next((c for c in doc_["cases"] if c["id"] == cid), None) != v1cases[cid]
                  or (pkg / v1cases[cid]["input"]).read_bytes() != (V1 / v1cases[cid]["input"]).read_bytes()]
    corroboration = {cid: x_check(next(c for c in doc_["cases"] if c["id"] == cid), ev, conv, writes)
                     for cid, ev in X_CORROBORATES.items()}
    files = sorted(p for p in pkg.rglob("*") if p.is_file() and p.name != "manifest.json")
    manifest = json.loads((pkg / "manifest.json").read_text())
    if rewrite:
        manifest["files"] = [{"path": str(p.relative_to(pkg)), "sha256": sha(p.read_bytes()),
                              "bytes": p.stat().st_size} for p in files]
        (pkg / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    listed = {f["path"]: f for f in manifest["files"]}

    def scan(p):
        t = p.read_text()
        for a in ALLOWED:
            t = t.replace(a, "")
        return sorted({m for pat in DENY for m in re.findall(pat, t)})
    return {
        "cases": len(doc_["cases"]), "manifest_case_count": manifest["case_count"],
        "provenance_counts": {k: sum(c["expectation_provenance"] == k for c in doc_["cases"])
                              for k in sorted({c["expectation_provenance"] for c in doc_["cases"]})},
        "case_problems": problems, "x_evidence_problems": x_problems,
        "mutations_caught_by_model_and_x": f"{mutation_check(doc_['cases'], conv, writes)}/{len(X_EVIDENCE)}",
        "x_corroboration_of_carried_cases": {k: v or "agrees" for k, v in corroboration.items()},
        "carried_cases": len(carried), "carried_records_or_fixtures_changed": carry_diff,
        "duplicate_fixtures": len(files) - len({p.read_bytes() for p in files}),
        "payload_files": len(files), "files_including_manifest": len(files) + 1,
        "manifest_sha256": sha((pkg / "manifest.json").read_bytes()),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (pkg / k).is_file()
                                    or sha((pkg / k).read_bytes()) != f["sha256"] or (pkg / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(pkg)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in pkg.rglob("*") if p.is_symlink()],
        "markdown_links": {md.name: len(v1.links(pkg, md)) for md in pkg.glob("*.md")},
        "unresolved_links": {md.name: [t for t, ok in v1.links(pkg, md) if not ok] for md in pkg.glob("*.md")
                             if not all(ok for _, ok in v1.links(pkg, md))},
        "missing_case_inputs": [c["input"] for c in doc_["cases"] if not (pkg / c["input"]).is_file()],
        "deny_list_hits": {str(p.relative_to(pkg)): hits for p in [*files, pkg / "manifest.json"] if (hits := scan(p))},
        "limits": "Checks authored consistency and agreement with the retained extracted-execution results only: the "
                  "reference application and a candidate were not executed; the cross-check model re-reads the same "
                  "evidence and is not an oracle.",
    }


if __name__ == "__main__":
    assert fmt(1000.0000000000001, 17) == "1000.00000000000011" and fmt(-0.0, 17) == "-0"
    assert read_int(" +201") == 201 and read_int("-0") == 0
    for bad in (" +201 ", "+201 ", "+-0", "-" + "0" * 63, "2147483648"):
        try:
            read_int(bad)
            raise AssertionError(bad)
        except Refused:
            pass
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "seal":
        rep = check(STAGE, rewrite=True)
        rep = {"schema": "author-validation-v1", "package": "transport-state-v2 (staged candidate)",
               "python": sys.version.split()[0], **rep}
        (HERE / "author-validation.json").write_text(json.dumps(rep, indent=1) + "\n")
        print(json.dumps(rep, indent=1))
    elif cmd == "verify":
        print(json.dumps(check(Path(sys.argv[2]), rewrite=False), indent=1))
