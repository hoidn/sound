"""Reviewer's checks of the transport-state-v2 candidate (analyst side; never shipped).

usage: python3 -I -B review_checks.py [PACKAGE_DIR]   (default: the staging copy)
Independent of build_v2.py and build_ts1.py: own restatement of the v2 clauses, carry check against the
released transport-state-v1, package inventory and links, fixture form, and a sanitization scan.
"""
import hashlib, json, math, re, struct, sys
import xml.etree.ElementTree as ET
from decimal import Decimal, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PKG = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[1] / "transport-state-v2"
V1 = ROOT / "handoff/transport-state-v1"
getcontext().prec = 80


class Refused(Exception):
    pass


class Excluded(Exception):
    pass


KEYMIDI = ("DrawButton Follow PhaseNudgeUp PhaseNudgeDown TapTempo LoopOn Start Stop Record SessionRecord "
           "PrepareSceneForNewRecording ArrangementOverdub AutomationArm BackToArrangement ReEnableAutomation "
           "PunshIn PunshOut MetronomOn MidiPrelisten TriggerCapture FollowActionEnabled IsTempoFollowerInControl "
           "ResyncExternalHardware").split()
KNOWN = ["PhaseNudgeTempo", "LoopOn", "LoopStart", "LoopLength", "LoopIsSongStart", "CurrentTime", "PunchIn",
         "PunchOut", "MetronomeTickDuration"] + [k + "KeyMidi" for k in KEYMIDI] + ["DrawMode"]
assert len(KNOWN) == 33
HEX = set("0123456789abcdefABCDEF")


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def read_bool(t):
    if t in ("true", "1"):
        return True
    if t in ("false", "0"):
        return False
    raise Refused(t)


def read_number(t, single):
    """REQ-004 / REQ-005 as worded in spec.md."""
    if t.startswith("#"):
        n = 8 if single else 16
        if len(t) == n + 1 and set(t[1:]) <= HEX:
            return struct.unpack(">f" if single else ">d", bytes.fromhex(t[1:]))[0]
        raise Refused(t)
    if t == "Invalid":
        raise Excluded(t)
    s = t.lstrip(" ")
    if s[:1] in ("\t", "\n", "\r", "\f", "\v"):
        raise Excluded("leading whitespace other than U+0020")
    body = s[1:] if s[:1] in "+-" and s else s
    if body.lower().startswith(("0x", "inf", "nan")):
        raise Excluded(t)
    m = re.match(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", s)
    if not m:
        raise Refused(t)
    v = float(m.group(0))
    return f32(v) if single else v


def read_int(t):
    """REQ-006: leading spaces, at most one +, body, trailing spaces; five conditions."""
    if not t.isascii():
        raise Refused(t)
    i = 0
    while i < len(t) and t[i] == " ":
        i += 1
    lead = i
    plus = i < len(t) and t[i] == "+"
    if plus:
        i += 1
    rest = t[i:]
    body = rest.rstrip(" ")
    trail = len(rest) - len(body)
    if not re.fullmatch(r"-?[0-9]+", body) or len(body) > 63:
        raise Refused(t)
    if plus and body.startswith("-"):
        raise Refused(t)
    if trail and (lead or plus):
        raise Refused(t)
    v = int(body)
    if not -2**31 <= v <= 2**31 - 1:
        raise Refused(t)
    if not 0 <= v <= 494:
        raise Excluded("code outside 0-494")
    return v


def write_number(x, p):
    """REQ-011 step 1 to 3 with L the correctly rounded binary64 log10; the half-gap band is excluded."""
    if x == 0:
        return "-0" if math.copysign(1.0, x) < 0 else "0"
    lg = Decimal(abs(x)).log10()
    n = int(lg.to_integral_value())
    if lg != n and n != 0:
        nb = math.nextafter(float(n), math.inf if lg > n else -math.inf)
        off = abs(lg - n) / Decimal(abs(nb - float(n)))
        if Decimal("0.25") <= off <= Decimal("0.75"):
            raise Excluded("log10 in the half-gap band")
    L = float(lg)
    k = math.ceil(L) if L >= 0 else math.floor(L)
    s = "%.*f" % (max(0, p - k), x)
    return s.rstrip("0").rstrip(".") if "." in s else s


RANGES = {"loop_start": (0, 1e6), "loop_length": (1, 1e6), "current_time": (0, 1e6), "tempo": (20, 999)}
TP = "MainTrack/DeviceChain/Mixer/Tempo"
SP = "MainTrack/DeviceChain/Mixer/TimeSignature"


def model(xml_bytes):
    """-> (outcome, state, saved values dict, saved Transport child names) for one fixture."""
    root = ET.fromstring(xml_bytes)
    assert root.tag == "Ableton" and root.attrib == {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                                     "SchemaChangeCount": "1"}, root.attrib
    ls = root[0]
    assert ls.tag == "LiveSet"
    tr = ls.find("Transport")
    if tr is None or ls.find(TP) is None or ls.find(SP) is None:
        raise Excluded("missing container")
    refused, state = [], {"loop_on": False, "loop_start": 8.0, "loop_length": 16.0, "current_time": 0.0}
    seen = {}
    for ch in tr:
        if ch.tag.endswith("KeyMidi"):
            raise Excluded("KeyMidi in input")
        if ch.tag not in KNOWN:
            continue                                  # unknown child: skipped
        if set(ch.attrib) - {"Value"}:
            raise Excluded("unknown attribute")
        seen[ch.tag] = seen.get(ch.tag, 0) + 1
        if seen[ch.tag] > 1:
            refused.append("duplicate " + ch.tag)
            continue
        v = ch.get("Value")
        if ch.tag == "LoopIsSongStart" and v != "false":
            raise Excluded("LoopIsSongStart")
        key = {"LoopOn": "loop_on", "LoopStart": "loop_start", "LoopLength": "loop_length",
               "CurrentTime": "current_time"}.get(ch.tag)
        if key is None or v is None:
            continue
        try:
            state[key] = read_bool(v) if key == "loop_on" else read_number(v, False)
        except Refused as e:
            refused.append(str(e))
    tm = ls.find(TP).findall("Manual")
    sm = ls.find(SP).findall("Manual")
    state["tempo"] = 120.0
    if len(tm) > 1 or len(sm) > 1:
        refused.append("duplicate Manual")
    if tm and tm[0].get("Value") is not None:
        try:
            state["tempo"] = read_number(tm[0].get("Value"), True)
        except Refused as e:
            refused.append(str(e))
    if not sm or sm[0].get("Value") is None:
        raise Excluded("missing TimeSignature/Manual")
    code = None
    try:
        code = read_int(sm[0].get("Value"))
    except Refused as e:
        refused.append(str(e))
    if refused:
        return "refused", None, None, None
    for k, (lo, hi) in RANGES.items():
        v = state[k]
        if not (lo <= v < hi if k != "tempo" else lo <= v <= hi):
            raise Excluded(f"{k} out of range")
    saved = {"Transport/LoopOn": "true" if state["loop_on"] else "false",
             "Transport/LoopStart": write_number(state["loop_start"], 17),
             "Transport/LoopLength": write_number(state["loop_length"], 17),
             "Transport/CurrentTime": write_number(state["current_time"], 17),
             TP + "/Manual": write_number(state["tempo"], 9), SP + "/Manual": str(code)}
    written = [ch.tag for ch in tr if ch.tag in KNOWN]
    written = sorted(set(written) | {"LoopOn", "LoopStart", "LoopLength", "CurrentTime"}, key=KNOWN.index)
    return "opens", state, saved, written


def judge(exp, outcome, state, saved, written):
    errs = []
    if exp["outcome"] != outcome:
        return [f"outcome {outcome} vs {exp['outcome']}"]
    for k, v in exp.get("state", {}).items():
        got = state[k]
        if got != v or (k == "tempo" and f32(v) != v):
            errs.append(f"state {k}: {got!r} vs {v!r}")
    s = exp.get("saved", {})
    for path, text in s.get("values", {}).items():
        if saved.get(path) != text:
            errs.append(f"saved {path}: {saved.get(path)!r} vs {text!r}")
    for path in s.get("absent", []):
        if path.startswith("Transport/") and path.split("/", 1)[1] in written:
            errs.append(f"absent {path} written")
    if s.get("transport_order") and written != sorted(written, key=KNOWN.index):
        errs.append("order")
    return errs


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


DENY = [r"0x[0-9A-Fa-f]+", r"\b[0-9a-f]{12,}\b", r"\bFUN_", r"\bA[A-Z][a-z]+[A-Z]\w*", r"\bL[A-Z][a-z]+[A-Z]\w*",
        r"\bm[A-Z]\w+", r"\bmp[A-Z]\w+", r"::", r"vtable", r"\bslot\b", r"[Ss]etValue", r"from_chars", r"strtod",
        r"vsnprintf", r"%\.\*", r"\blog10\(", r"\bgdb\b", r"harness", r"xexec", r"\bstubs?\b", r"\btrap", r"Ghidra",
        r"[Dd]ecompil", r"pseudocode", r"disassembl", r"\bX[0-9]\b", r"\bn1-", r"\bx2-", r"PRB-", r"\bQ-0", r"ADR",
        r"analysis/", r"raw/", r"wiki/", r"research", r"\.py\b", r"Mach-O", r"dyld", r"\bApple\b", r"probe batch",
        r"corpus", r"traceab", r"\bS1\b", r"\bN1\b", r"glibc", r"x86", r"arm64", r"\bslice\b", r"Linux", r"exception",
        r"\bthrow", r"libm|libc", r"cvt|fcvt|fcsel|fcmp", r"dossier", r"exported", r"/var/|/home/|/tmp/"]
# Wording that names the provenance label and its definition; reported separately, not as a defect.
LABEL = ["extracted execution (x86_64 slice, glibc substitutions); arm64 equivalence inferred"]


def scan(text):
    for a in LABEL:
        text = text.replace(a, "<LABEL>")
    hits = {}
    for pat in DENY:
        for m in re.finditer(pat, text):
            ctx = text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
            hits.setdefault(pat, []).append(ctx)
    return hits


def links(md):
    out = []
    for target in re.findall(r"\]\(([^)]+)\)", md.read_text()):
        path, _, frag = target.partition("#")
        if re.match(r"[a-z]+://", target):
            out.append((target, False))
            continue
        f = (md.parent / path) if path else md
        ok = f.is_file() and PKG in f.resolve().parents or f.resolve() == md.resolve()
        if ok and frag and f.suffix == ".md":
            heads = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.*)$", f.read_text(), re.M)}
            ok = frag in heads
        out.append((target, ok))
    return out


def main():
    rep = {"package": str(PKG)}
    cases = json.loads((PKG / "cases.json").read_text())
    v1c = {c["id"]: c for c in json.loads((V1 / "cases.json").read_text())["cases"]}
    ids = [c["id"] for c in cases["cases"]]
    rep["case_count"] = len(ids)
    rep["ids_unique"] = len(ids) == len(set(ids))
    # carry
    rep["carried_ids"] = sorted(v1c)
    rep["carried_record_or_fixture_differs"] = [cid for cid in v1c if
        next((c for c in cases["cases"] if c["id"] == cid), None) != v1c[cid]
        or (PKG / v1c[cid]["input"]).read_bytes() != (V1 / v1c[cid]["input"]).read_bytes()]
    rep["new_ids"] = [i for i in ids if i not in v1c]
    rep["new_case_provenance"] = sorted({c["expectation_provenance"] for c in cases["cases"] if c["id"] not in v1c})
    rep["superseded_manifest_sha256"] = sha(V1 / "manifest.json")
    # model
    problems, excluded = {}, {}
    for c in cases["cases"]:
        raw = (PKG / c["input"]).read_bytes()
        try:
            errs = judge(c["expected"], *model(raw))
        except Excluded as e:
            excluded[c["id"]] = str(e)
            continue
        if errs:
            problems[c["id"]] = errs
    rep["model_disagreements"] = problems
    rep["fixtures_hitting_exclusions"] = excluded
    # spec worked examples
    ex = {"120": (120.0, 17), "8": (8.0, 17), "4.5": (4.5, 17), "121.199997": (f32(121.2), 9),
          "93.3333359": (f32(93.3333333), 9), "0.299999999999999989": (0.3, 17), "3.2999999999999998": (3.3, 17),
          "100.000000000000014": (100.00000000000001, 17), "0.099999999999999992": (0.09999999999999999, 17),
          "1000.00000000000011": (1000.0000000000001, 17), "0.00000099999999999999995": (0.000001, 17), "-0": (-0.0, 17)}
    rep["req011_examples_disagree"] = [t for t, (x, p) in ex.items() if write_number(x, p) != t]
    rep["req004_examples"] = {t: read_number(t, False) for t in ("4.5abc", " +4.5 ", "#4012000000000000", "-0")}
    rep["req005_examples"] = {t: read_number(t, True) for t in ("#42f00000", "93.3333333")}
    acc = ["201", " 201", "+201", " +201", "201 ", "00201", "-0", "0" * 60 + "201 "]
    ref = [" 201 ", " +201 ", "+201 ", "- 201", "+-201", "--201", "-", "2147483648", "201.0", "2e2", "0x10", "abc", "",
           "-" + "0" * 63]
    def ok_int(t):
        try:
            return read_int(t)
        except Refused:
            return "refused"
    rep["req006_accepted_examples"] = {t: ok_int(t) for t in acc}
    rep["req006_refused_examples_all_refused"] = all(ok_int(t) == "refused" for t in ref)
    rep["req010_examples"] = {f"{n}/{d}": (n - 1) + 99 * int(math.log2(d)) for n, d in
                              ((4, 4), (6, 8), (7, 8), (1, 1), (99, 16))}
    # fixtures
    fx = sorted((PKG / "fixtures").iterdir())
    rep["fixture_count"] = len(fx)
    rep["fixture_form_problems"] = [p.name for p in fx if not (p.read_bytes().isascii() and b"\r" not in p.read_bytes()
                                    and b"\t" not in p.read_bytes() and p.read_bytes().endswith(b"\n"))]
    rep["fixture_duplicates"] = len(fx) - len({p.read_bytes() for p in fx})
    rep["inputs_missing"] = [c["input"] for c in cases["cases"] if not (PKG / c["input"]).is_file()]
    rep["fixtures_unreferenced"] = sorted({f"fixtures/{p.name}" for p in fx} - {c["input"] for c in cases["cases"]})
    # manifest inventory
    man = json.loads((PKG / "manifest.json").read_text())
    files = sorted(str(p.relative_to(PKG)) for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
    listed = {f["path"]: f for f in man["files"]}
    rep["inventory_differences"] = sorted(set(files) ^ set(listed))
    rep["hash_or_size_mismatches"] = [k for k, f in listed.items() if not (PKG / k).is_file() or
                                      sha(PKG / k) != f["sha256"] or (PKG / k).stat().st_size != f["bytes"]]
    rep["manifest_case_count_matches"] = man["case_count"] == len(ids)
    rep["manifest_sha256"] = sha(PKG / "manifest.json")
    rep["symlinks"] = [str(p) for p in PKG.rglob("*") if p.is_symlink()]
    rep["links"] = {md.name: links(md) for md in sorted(PKG.glob("*.md"))}
    rep["unresolved_links"] = {k: [t for t, ok in v if not ok] for k, v in rep["links"].items() if not all(o for _, o in v)}
    rep["status_strings"] = sorted({man["release_status"], cases["status"]})
    # sanitization
    rep["scan_hits"] = {str(p.relative_to(PKG)): h for p in sorted(PKG.rglob("*")) if p.is_file()
                        and (h := scan(p.read_text()))}
    rep["label_occurrences"] = {str(p.relative_to(PKG)): p.read_text().count(LABEL[0]) for p in sorted(PKG.rglob("*"))
                                if p.is_file() and LABEL[0] in p.read_text()}
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    assert write_number(1000.0000000000001, 17) == "1000.00000000000011" and read_int(" +201") == 201
    main()
