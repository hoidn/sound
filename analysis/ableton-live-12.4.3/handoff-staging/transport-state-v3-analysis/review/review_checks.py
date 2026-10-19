"""Reviewer's checks of the transport-state-v3 candidate (analyst side; never shipped).

usage: python3 -I -B review_checks.py [--full] [PACKAGE_DIR]   (default: the staging copy)
Independent of build_v3.py, build_v2.py and build_ts1.py: own restatement of the carried clauses, carry check
against the released transport-state-v2, the fixture change, structure conditions the T11 checker does not
evaluate (REQ-LIVE-SET-STRUCTURE-001 shapes), refusal isolation, track insensitivity, package inventory and links,
fixture form and a sanitization scan. The T11 checker itself is run separately (see review-checks.txt).
"""
import difflib, hashlib, json, math, re, struct, sys
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PKG = Path(ARGS[0]).resolve() if ARGS else HERE.parents[1] / "transport-state-v3"
V2 = ROOT / "handoff/transport-state-v2"
SCHEMA = Path("/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt")
getcontext().prec = 80


class Refused(Exception):
    pass


class Excluded(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


KEYMIDI = ("DrawButton Follow PhaseNudgeUp PhaseNudgeDown TapTempo LoopOn Start Stop Record SessionRecord "
           "PrepareSceneForNewRecording ArrangementOverdub AutomationArm BackToArrangement ReEnableAutomation "
           "PunshIn PunshOut MetronomOn MidiPrelisten TriggerCapture FollowActionEnabled IsTempoFollowerInControl "
           "ResyncExternalHardware").split()
KNOWN = ["PhaseNudgeTempo", "LoopOn", "LoopStart", "LoopLength", "LoopIsSongStart", "CurrentTime", "PunchIn",
         "PunchOut", "MetronomeTickDuration"] + [k + "KeyMidi" for k in KEYMIDI] + ["DrawMode"]
assert len(KNOWN) == 33
HEX = set("0123456789abcdefABCDEF")
DEFAULTS = {"LoopOn": False, "LoopStart": 8.0, "LoopLength": 16.0, "CurrentTime": 0.0}
STATE_KEY = {"LoopOn": "loop_on", "LoopStart": "loop_start", "LoopLength": "loop_length", "CurrentTime": "current_time"}


# ---- own restatement of the carried clauses (spec.md wording) ----
def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def read_bool(t):  # REQ-003
    if t in ("true", "1"):
        return True
    if t in ("false", "0"):
        return False
    raise Refused(f"loop switch text {t!r}")


def read_number(t, single):  # REQ-004, REQ-005
    if t.startswith("#"):
        n = 8 if single else 16
        if len(t) == n + 1 and set(t[1:]) <= HEX:
            return struct.unpack(">f" if single else ">d", bytes.fromhex(t[1:]))[0]
        raise Refused(f"# text {t!r}")
    if t == "Invalid":
        raise Excluded(t)
    s = t.lstrip(" ")
    if s[:1] in ("\t", "\n", "\r", "\f", "\v"):
        raise Excluded("leading whitespace other than U+0020")
    body = s[1:] if s[:1] in ("+", "-") else s
    if body.lower().startswith(("0x", "inf", "nan")):
        raise Excluded(t)
    m = re.match(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", s)
    if not m:
        raise Refused(f"number text {t!r}")
    v = float(m.group(0))  # CPython: correctly rounded, keeps the sign of -0
    return f32(v) if single else v


def read_int(t):  # REQ-006, five conditions
    if not t.isascii():
        raise Refused(t)
    i = 0
    while i < len(t) and t[i] == " ":
        i += 1
    lead = i > 0
    plus = i < len(t) and t[i] == "+"
    rest = t[i + 1:] if plus else t[i:]
    body = rest.rstrip(" ")
    trail = len(rest) > len(body)
    if plus and body.startswith("-"):
        raise Refused(f"code text {t!r}")
    if not re.fullmatch(r"-?[0-9]+", body) or len(body) > 63:
        raise Refused(f"code text {t!r}")
    if trail and (lead or plus):
        raise Refused(f"code text {t!r}")
    v = int(body)
    if not -2**31 <= v < 2**31:
        raise Refused(f"code text {t!r}")
    return v


def gap_side(n, l_exact):
    """The binary64 gap at integer n on the side of l_exact."""
    f = float(n)
    nxt = math.nextafter(f, math.inf if l_exact > n else -math.inf)
    return abs(Decimal(nxt) - Decimal(f))


def save_text(x, p):  # REQ-011
    if x == 0:
        return "-0" if math.copysign(1, x) < 0 else "0"
    if not math.isfinite(x):
        raise Excluded("non-finite")
    l_exact = abs(Decimal(x)).log10()
    n = int(l_exact.to_integral_value())
    if l_exact != n:
        off = abs(l_exact - n) / gap_side(n, l_exact)
        if Decimal("0.25") <= off <= Decimal("0.75"):
            raise Excluded(f"half-gap band ({off:.3f})")
    L = float(l_exact)  # nearest binary64 to the exact logarithm
    k = math.ceil(L) if L >= 0 else math.floor(L)
    d = max(0, p - k)
    s = format(Decimal(x).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_EVEN), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def in_range(key, v):
    lo, hi = {"loop_start": (0, 1e6), "current_time": (0, 1e6), "loop_length": (1, 1e6), "tempo": (20, 999)}[key]
    v = 0.0 if v == 0 else v
    if key == "tempo":
        return lo <= v <= hi
    return lo <= v < hi


def only_value(el):
    if set(el.attrib) - {"Value"}:
        raise Excluded(f"unknown attribute on {el.tag}")


def judge_doc(raw, structure=True):
    """Return (outcome, state, saved texts, saved transport children, reason)."""
    root = ET.fromstring(raw)
    if root.tag != "Ableton" or root.attrib != {"MajorVersion": "5", "MinorVersion": "12.0_12402",
                                                "SchemaChangeCount": "1"} or root[0].tag != "LiveSet":
        raise Excluded("envelope")
    ls = root[0]
    if structure:
        tr = ls.find("Tracks")
        players = [t for t in (tr if tr is not None else []) if t.tag in ("AudioTrack", "MidiTrack", "GroupTrack")]
        if not players:
            return "refused", None, None, None, "no player track"
        for t in players:
            main = t.findall("DeviceChain/MainSequencer/ClipSlotList/ClipSlot")
            frz = t.findall("DeviceChain/FreezeSequencer/ClipSlotList/ClipSlot")
            if len(main) != len(frz):
                return "refused", None, None, None, "freeze slot count"
    state, saved = {}, {}
    try:
        tp = ls.find("Transport")
        if tp is None:
            raise Excluded("missing Transport")
        names = [c.tag for c in tp]
        for n in set(names):
            if names.count(n) > 1:
                if n in KNOWN and not n.endswith("KeyMidi"):
                    raise Refused(f"duplicate Transport/{n}")
                raise Excluded("repeated unknown or KeyMidi child")
        for c in tp:
            if c.tag.endswith("KeyMidi"):
                raise Excluded("KeyMidi child in input")
            if c.tag == "LoopIsSongStart" and c.get("Value") != "false":
                raise Excluded("LoopIsSongStart")
            if c.tag in DEFAULTS:
                only_value(c)
        for n, dflt in DEFAULTS.items():
            el = tp.find(n)
            t = None if el is None else el.get("Value")
            v = dflt if t is None else (read_bool(t) if n == "LoopOn" else read_number(t, False))
            if n != "LoopOn" and not in_range(STATE_KEY[n], v):
                raise Excluded(f"{n} out of range")
            state[STATE_KEY[n]] = v
            saved[f"Transport/{n}"] = ("true" if v else "false") if n == "LoopOn" else save_text(v, 17)
        mix = ls.find("MainTrack/DeviceChain/Mixer")
        if mix is None or mix.find("Tempo") is None or mix.find("TimeSignature") is None:
            raise Excluded("missing MainTrack, DeviceChain, Mixer, Tempo or TimeSignature")
        for part in ("Tempo", "TimeSignature"):
            if len(mix.find(part).findall("Manual")) > 1:
                raise Refused(f"duplicate {part}/Manual")
        tm = mix.find("Tempo/Manual")
        t = None if tm is None else tm.get("Value")
        if tm is not None:
            only_value(tm)
        tempo = 120.0 if t is None else read_number(t, True)
        if not in_range("tempo", tempo):
            raise Excluded("tempo out of range")
        state["tempo"] = tempo
        saved["MainTrack/DeviceChain/Mixer/Tempo/Manual"] = save_text(tempo, 9)
        sm = mix.find("TimeSignature/Manual")
        if sm is None or sm.get("Value") is None:
            raise Excluded("missing time-signature Manual or value")
        only_value(sm)
        code = read_int(sm.get("Value"))
        if not 0 <= code <= 494:
            raise Excluded("code outside 0-494")
        saved["MainTrack/DeviceChain/Mixer/TimeSignature/Manual"] = str(code)
    except Refused as e:
        return "refused", None, None, None, str(e)
    order = [n for n in KNOWN if n in names] + [n for n in DEFAULTS if n not in names]
    order.sort(key=KNOWN.index)  # a save writes the four values exactly once, in the REQ-002 order
    return "opens", state, saved, order, None


def judge_case(case, raw):
    exp = case["expected"]
    out, state, saved, order, reason = judge_doc(raw)
    errs = []
    if out != exp["outcome"]:
        errs.append(f"outcome {out} ({reason})")
        return errs, reason
    for k, v in exp.get("state", {}).items():
        if state[k] != v or isinstance(v, bool) != isinstance(state[k], bool):
            errs.append(f"state {k} {state[k]!r} != {v!r}")
    sv = exp.get("saved", {})
    if sv and case["action"] != "open-save":
        errs.append("saved part on an open-only case")
    for p, v in sv.get("values", {}).items():
        if saved.get(p) != v:
            errs.append(f"saved {p} {saved.get(p)!r} != {v!r}")
    for p in sv.get("absent", []):
        if p.startswith("Transport/") and p.split("/", 1)[1] in order:
            errs.append(f"saved {p} present")
    if sv.get("transport_order"):
        if [n for n in order if n in KNOWN] != sorted(order, key=KNOWN.index):
            errs.append("order")
    return errs, reason


# ---- structure conditions that the T11 checker does not evaluate ----
def lss001(schema, raw):
    """REQ-LIVE-SET-STRUCTURE-001 refusals: base value element without Value; duplicate compound member;
    list item of an unaccepted class (Tracks only: the fixtures' only non-empty list)."""
    out = []

    def walk(e, cls, path):
        fields = schema.get(cls, {})
        tags = [c.tag for c in e]
        for n in set(tags):
            if tags.count(n) > 1 and n in fields and fields[n][1] != "-1":
                out.append(f"duplicate member {path}/{n}")
        for c in e:
            f = fields.get(c.tag)
            if f is None:
                continue
            fcls, ftype = f
            if ftype == "-4" and "Value" not in c.attrib:
                out.append(f"base value element without Value: {path}/{c.tag}")
            elif ftype == "0":
                walk(c, fcls, f"{path}/{c.tag}")
            elif ftype == "-1":
                for item in c:
                    if c.tag == "Tracks" and item.tag not in ("AudioTrack", "MidiTrack", "GroupTrack", "ReturnTrack"):
                        out.append(f"list item class {item.tag}")
                    walk(item, item.tag, f"{path}/{c.tag}/{item.tag}")
    walk(ET.fromstring(raw).find("LiveSet"), "LiveSet", "LiveSet")
    return out


def load_schema():
    r = ET.parse(SCHEMA).getroot()
    return {c.tag: {f.tag: (f.get("Class"), f.get("Type")) for f in c} for c in r}


# ---- package helpers ----
def links(md):
    text = md.read_text()
    res = []
    for target in re.findall(r"\]\(([^)]+)\)", text):
        path, _, anchor = target.partition("#")
        f = (md.parent / path) if path else md
        ok = f.is_file() and f.resolve().is_relative_to(PKG)
        if ok and anchor and f.suffix == ".md":
            heads = [re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
                     for h in re.findall(r"^#+ (.*)$", f.read_text(), re.M)]
            ok = anchor in heads
        res.append((target, ok))
    return res


DENY = [r"0x[0-9a-fA-F]{5,}", r"\bA[A-Z][a-z]+[A-Z]\w*", r"\b(?:analysis|raw|wiki|research|specs|verification)/",
        r"/home/", r"/var/tmp", r"\.py\b", r"T11", r"T1\.1", r"LSS-", r"PRB-", r"\bQ-0\d\d", r"\bRV[0-9A-Z]*-\d",
        r"LIVE-SET-STRUCTURE", r"S-cond", r"\baudit", r"\bwalk", r"pseudo", r"decompil", r"[Gg]hidra", r"objdump",
        r"corpus", r"vtable", r"\bslot \+", r"offset", r"strtod", r"log10", r"vsnprintf", r"from_chars",
        r"post-load", r"loader", r"MIN\b", r"skeleton", r"probe", r"packet", r"\bX2\b", r"\bN1\b", r"ADR"]


def scan(p):
    t = p.read_text()
    return sorted({m for pat in DENY for m in re.findall(pat, t)})


def spec_track_block(spec_text):
    m = re.search(r"```xml\n(.*?)```", spec_text, re.S)
    lines = [l for l in m.group(1).splitlines() if l.strip()]  # the closing fence line is indented
    ind = min(len(l) - len(l.lstrip(" ")) for l in lines if l.strip())
    return "".join("    " + l[ind:] + "\n" for l in lines)


def main():
    schema = load_schema()
    rep = {}
    # v2 identity and carry
    catalog = (ROOT / "handoff/index.md").read_text()
    row = next(l for l in catalog.splitlines() if l.startswith("| [transport-state-v2]"))
    v2sha = sha((V2 / "manifest.json").read_bytes())
    m2 = json.loads((V2 / "manifest.json").read_text())
    m3 = json.loads((PKG / "manifest.json").read_text())
    rep["v2_manifest_sha256"] = v2sha
    rep["v2_manifest_equals_catalog"] = f"`{v2sha}`" in row
    rep["v2_manifest_equals_superseded_digest"] = m3["supersession"]["superseded_manifest_sha256"] == v2sha
    rep["v2_payload_mismatches"] = [f["path"] for f in m2["files"] if sha((V2 / f["path"]).read_bytes()) != f["sha256"]]
    d2 = json.loads((V2 / "cases.json").read_text())
    d3 = json.loads((PKG / "cases.json").read_text())
    rep["case_ids_v2_equal_v3_in_order"] = [c["id"] for c in d2["cases"]] == [c["id"] for c in d3["cases"]]
    rep["case_records_differing"] = [a["id"] for a, b in zip(d2["cases"], d3["cases"])
                                     if a != b or json.dumps(a) != json.dumps(b)]
    rep["cases_json_top_level_changed"] = sorted(k for k in set(d2) | set(d3) if k != "cases" and d2.get(k) != d3.get(k))
    same = ("target", "feature_ids", "partial_requirement_scopes", "unreleased_requirements",
            "compatibility_dimensions", "expectation_provenance_labels", "stated_assumptions", "approved_public_sources")
    rep["manifest_fields_changed_from_v2"] = sorted(k for k in same if m2.get(k) != m3.get(k))
    e2, e3 = m2["exclusions"], m3["exclusions"]
    rep["manifest_exclusions_added"] = [x for x in e3["inputs_without_expectation"] if x not in e2["inputs_without_expectation"]]
    rep["manifest_exclusions_removed"] = [x for x in e2["inputs_without_expectation"] if x not in e3["inputs_without_expectation"]]
    rep["manifest_behavior_and_cases_exclusions_equal"] = (e2["behavior"] == e3["behavior"]
                                                           and e2["parent_cases_not_released"] == e3["parent_cases_not_released"])
    # fixture change
    block = spec_track_block((PKG / "spec.md").read_text())
    rep["spec_track_block_lines"] = block.count("\n")
    fx = {}
    base = (PKG / "fixtures/TS-022.xml").read_bytes()
    fixtures_listed = m3["supersession"]["fixture_changes"]["fixtures"]
    rep["fixture_changes_lists_every_case_input"] = sorted(fixtures_listed) == sorted(c["input"] for c in d3["cases"])
    blocktags = sorted({e.tag for e in ET.fromstring(block).iter()})
    rep["track_block_tags"] = blocktags
    rep["track_block_has_transport_name"] = sorted(set(blocktags) & {"Transport", "Tempo", "TimeSignature", "Manual",
                                                    "LoopOn", "LoopStart", "LoopLength", "CurrentTime", "MainTrack",
                                                    "Mixer", "AutomationEnvelopes", "Scenes", "Scene", "MidiClip"})
    for c in d3["cases"]:
        raw = (PKG / c["input"]).read_bytes()
        raw2 = (V2 / c["input"]).read_bytes()
        t2 = raw2.decode("ascii")
        r = {"equals_v2_plus_spec_block": raw.decode("ascii") == t2.replace("  <LiveSet>\n", "  <LiveSet>\n" + block, 1)
             and t2.count("  <LiveSet>\n") == 1,
             "form_ok": raw.isascii() and b"\r" not in raw and b"\t" not in raw and raw.endswith(b"\n"),
             "first_liveset_child": ET.fromstring(raw).find("LiveSet")[0].tag,
             "lss001_shapes": lss001(schema, raw)}
        errs, reason = judge_case(c, raw)
        r["judge"] = errs or "agrees"
        r["refusal_reason"] = reason
        # track insensitivity: the transport reading of the v2 bytes, structure rules off, is the same
        r["transport_reading_same_as_v2_bytes"] = judge_doc(raw, structure=True)[:4] == judge_doc(raw2, structure=False)[:4]
        r["v2_bytes_with_structure"] = judge_doc(raw2)[0]
        if c["expected"]["outcome"] == "refused":
            d = [l for l in difflib.ndiff(base.decode().splitlines(), raw.decode().splitlines()) if l[:2] in ("- ", "+ ")]
            r["lines_differing_from_TS-022"] = [l.strip() for l in d]
            # replace the differing lines by TS-022's: the document must then open
            r["opens_once_tested_line_reverted"] = judge_doc(base)[0] == "opens" and len([l for l in d if l[0] == "+"]) == 1
        fx[c["id"]] = r
    rep["per_case"] = fx
    rep["summary"] = {
        "cases": len(d3["cases"]),
        "judge_agrees": sum(r["judge"] == "agrees" for r in fx.values()),
        "fixtures_equal_v2_plus_spec_block": sum(r["equals_v2_plus_spec_block"] for r in fx.values()),
        "form_ok": sum(r["form_ok"] for r in fx.values()),
        "tracks_first": sum(r["first_liveset_child"] == "Tracks" for r in fx.values()),
        "fixtures_with_lss001_shapes": {k: r["lss001_shapes"] for k, r in fx.items() if r["lss001_shapes"]},
        "transport_reading_same_as_v2_bytes": sum(r["transport_reading_same_as_v2_bytes"] for r in fx.values()),
        "v2_bytes_refused_by_structure": sum(r["v2_bytes_with_structure"] == "refused" for r in fx.values()),
        "refused_isolated": {k: r["opens_once_tested_line_reverted"] for k, r in fx.items() if "lines_differing_from_TS-022" in r},
        "refusal_reasons": {k: r["refusal_reason"] for k, r in fx.items() if r["refusal_reason"]},
        "distinct_fixtures": len({(PKG / c["input"]).read_bytes() for c in d3["cases"]}),
    }
    # worked examples in the contract
    ex = {"93.3333333": f32(93.3333333) == 93.33333587646484375, "#42f00000": read_number("#42f00000", True) == 120,
          "#4012000000000000": read_number("#4012000000000000", False) == 4.5,
          "120": save_text(120.0, 9) == "120", "8": save_text(8.0, 17) == "8", "4.5": save_text(4.5, 17) == "4.5",
          "121.2": save_text(f32(121.2), 9) == "121.199997", "93.3333333 save": save_text(f32(93.3333333), 9) == "93.3333359",
          "0.3": save_text(0.3, 17) == "0.299999999999999989", "3.3": save_text(3.3, 17) == "3.2999999999999998",
          "100.00000000000001": save_text(100.00000000000001, 17) == "100.000000000000014",
          "0.09999999999999999": save_text(0.09999999999999999, 17) == "0.099999999999999992",
          "1000.0000000000001": save_text(1000.0000000000001, 17) == "1000.00000000000011",
          "0.000001": save_text(0.000001, 17) == "0.00000099999999999999995"}
    for t in ("201", " 201", "+201", " +201", "201 ", "00201", "-0", "0" * 60 + "201 "):
        ex[f"int accepts {t!r}"] = read_int(t) in (201, 0)
    for t in (" 201 ", " +201 ", "+201 ", "- 201", "+-201", "--201", "-", "2147483648", "201.0", "2e2", "0x10",
              "abc", "", "-" + "0" * 63):
        try:
            read_int(t)
            ex[f"int refuses {t!r}"] = False
        except Refused:
            ex[f"int refuses {t!r}"] = True
    rep["contract_examples_failing"] = [k for k, v in ex.items() if not v]
    # package
    files = sorted(p for p in PKG.rglob("*") if p.is_file() and p.name != "manifest.json")
    listed = {f["path"]: f for f in m3["files"]}
    rep["package"] = {
        "payload_files": len(files),
        "hash_or_size_mismatches": [k for k, f in listed.items() if not (PKG / k).is_file()
                                    or sha((PKG / k).read_bytes()) != f["sha256"] or (PKG / k).stat().st_size != f["bytes"]],
        "inventory_differences": sorted({str(p.relative_to(PKG)) for p in files} ^ set(listed)),
        "symlinks": [str(p) for p in PKG.rglob("*") if p.is_symlink()],
        "links": {md.name: len(links(md)) for md in sorted(PKG.glob("*.md"))},
        "unresolved_links": {md.name: [t for t, ok in links(md) if not ok] for md in PKG.glob("*.md")
                             if not all(ok for _, ok in links(md))},
        "missing_case_inputs": [c["input"] for c in d3["cases"] if not (PKG / c["input"]).is_file()],
        "case_count_matches": m3["case_count"] == len(d3["cases"]),
        "manifest_sha256": sha((PKG / "manifest.json").read_bytes()),
        "release_status": m3["release_status"], "review_status": m3["review"]["status"],
    }
    rep["scan_hits"] = {str(p.relative_to(PKG)): h for p in [*files, PKG / "manifest.json"]
                        if p.suffix != ".xml" and (h := scan(p))}
    rep["scan_hits_fixtures"] = sorted({h for p in files if p.suffix == ".xml" for h in scan(p)})
    print(json.dumps(rep if "--full" in sys.argv else {k: v for k, v in rep.items() if k != "per_case"}, indent=1))


if __name__ == "__main__":
    main()
