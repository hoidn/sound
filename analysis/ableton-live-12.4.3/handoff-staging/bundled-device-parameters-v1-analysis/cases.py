"""Case table and manifest metadata for bundled-device-parameters-v1 (analyst side).

cases(tables, B) -> list of case dicts consumed by build_bdp.build(); B is the build module (tree helpers).
Text-form expectations below are hand-authored constants; complete-device expectations are the numeric values
build_bdp.value_of() wrote into the fixture. crosscheck_model.py re-reads every fixture independently.
"""
PS = "static-derived; not observed reference output"
PDS = "documented and static-derived; not observed reference output"
REQ = "REQ-BUNDLED-DEVICE-PARAMETERS-"
NAMES = {"Amp": "Amp", "Cabinet": "Cabinet", "UltraAnalog": "Analog", "StringStudio": "Tension",
         "Collision": "Collision", "LoungeLizard": "Electric", "Corpus": "Corpus"}
# (device, path, text, expected value or None for refused, purpose)
FLOAT_TEXT = [
    ("LoungeLizard", "KeyboardStretch", "0.3", 0.30000001192092896, "Float text 0.3 reads as the nearest binary32 value"),
    ("LoungeLizard", "KeyboardStretch", "0.6000000238", 0.6000000238418579, "Float text with ten significant digits"),
    ("LoungeLizard", "KeyboardStretch", " 0.5", 0.5, "Float text with a leading space"),
    ("LoungeLizard", "KeyboardStretch", "+0.5", 0.5, "Float text with a leading plus sign"),
    ("LoungeLizard", "KeyboardStretch", ".5", 0.5, "Float text without an integer digit"),
    ("LoungeLizard", "KeyboardStretch", "5e-1", 0.5, "Float text with an exponent"),
    ("LoungeLizard", "KeyboardStretch", "0.5abc", 0.5, "Float text with trailing letters after the number"),
    ("LoungeLizard", "KeyboardStretch", "0.5e", 0.5, "Float text ending in an exponent marker without digits"),
    ("LoungeLizard", "KeyboardStretch", "0.5 ", 0.5, "Float text with a trailing space"),
    ("LoungeLizard", "KeyboardStretch", "1", 1.0, "Float text of an integer at the upper domain bound"),
    ("LoungeLizard", "KeyboardStretch", "abc", None, "Float text without a number is refused"),
    ("LoungeLizard", "KeyboardStretch", "", None, "Empty Float text is refused"),
    ("LoungeLizard", "KeyboardStretch", "e5", None, "Float text of an exponent without a number is refused"),
    ("Corpus", "Detune", "-0.75", -0.75, "Negative Float text"),
    ("Corpus", "FilterMidFreq", "1234.567", 1234.5670166015625, "Float text above 1000 reads as the nearest binary32 value"),
    ("Corpus", "FilterMidFreq", "2.5E+3", 2500.0, "Float text with an upper-case exponent marker and a plus sign"),
]
ENUM_TEXT = [("3", 3, "Enum text of plain digits"), (" 3", 3, "Enum text with leading spaces"),
             ("+3", 3, "Enum text with a leading plus sign"), (" +3", 3, "Enum text with a space and a plus sign"),
             ("3 ", 3, "Enum text with a trailing space"), ("3.0", None, "Enum text with a fraction is refused"),
             ("0x3", None, "Hexadecimal Enum text is refused"), ("", None, "Empty Enum text is refused"),
             (" ", None, "Enum text of only a space is refused"), ("+-3", None, "Enum text with a plus and a minus sign is refused"),
             ("0" * 63 + "3", None, "Enum text of 64 digits is refused")]
BOOL_TEXT = [("1", True, "Bool text 1 reads as true"), ("0", False, "Bool text 0 reads as false"),
             ("TRUE", None, "Upper-case Bool text is refused"), ("True", None, "Capitalized Bool text is refused"),
             ("", None, "Empty Bool text is refused"), (" true", None, "Bool text with a leading space is refused")]


SRC_FLOAT = {"0.3": "BDP-005 (narrowed to the value read on open; save excluded; Amp Bass moved to Electric KeyboardStretch)",
             "abc": "BDP-006 (moved to Electric KeyboardStretch)", "0.5abc": "BDP-007 (narrowed to the value read; save excluded)"}
SRC_ENUM = {"3.0": "BDP-010 (moved from Analog Polyphony to Cabinet CabinetType)",
            "0x3": "BDP-011 (moved from Corpus ResonanceType 0x5 to Cabinet CabinetType)"}
SRC_BOOL = {"TRUE": "BDP-008", "1": "BDP-009 (narrowed to the value read; save excluded)"}


def cases(tables, B):
    out = []

    def add(**c):
        c["id"] = f"BUNDLED-DEVICE-PARAMETERS-{len(out) + 1:03d}"
        c.setdefault("base", "mid")
        out.append(c)

    for el, name in NAMES.items():
        rows = tables[el]
        reqs = ["001", "002", "003", "006"] + (["007"] if any(m.get("whole") for m in rows) else []) + \
               (["011"] if any("value" in m for m in rows) else []) + ["012"]
        mid = B.base_values(rows, "mid")
        for mode, kind, what in [("mid", "positive", "values inside every domain"),
                                 ("min", "boundary", "every parameter at its lower bound (Bool false)"),
                                 ("max", "boundary", "every parameter at its upper bound (Bool true)")]:
            lab = B.LABELS.get(el, {}) if mode == "mid" else {}
            add(device=el, base=mode, kind=kind, reqs=reqs + (["014"] if lab else []), outcome="opens", prov=PDS,
                labels={p: v[int(mid[p])] for p, v in lab.items()},
                purpose=f"Complete {name} device preset with {what}",
                src="BDP-001 replaced by an authored complete preset (shipped fixtures F1-F7 not used)" +
                    ("; BDP-013 bounds narrowed to the value read, save excluded" if mode != "mid" else ""))
    new = "new case for a REQ-004 clause of the draft"
    for el, path, text, exp, purpose in FLOAT_TEXT:
        src = SRC_FLOAT.get(text, new) if el == "LoungeLizard" else new
        if exp is None:
            add(device=el, kind="negative", reqs=["004"], texts={path: text}, outcome="refused", prov=PS, purpose=purpose,
                src=src)
        else:
            add(device=el, kind="positive", reqs=["004", "006"], texts={path: text}, outcome="opens", state_keys=[path],
                state={path: exp}, prov=PS, purpose=purpose, src=src)
    for text, exp, purpose in ENUM_TEXT:
        c = dict(device="Cabinet", reqs=["004"], texts={"CabinetType": text}, prov=PS, purpose=purpose + " (Cabinet CabinetType)",
                 src=SRC_ENUM.get(text, new))
        add(**c, kind="negative", outcome="refused") if exp is None else \
            add(**dict(c, reqs=["004", "006"]), kind="positive", outcome="opens", state_keys=["CabinetType"],
                state={"CabinetType": exp})
    for text, exp, purpose in BOOL_TEXT:
        c = dict(device="Cabinet", reqs=["004"], texts={"MicrophoneTypeSwitch": text}, prov=PS,
                 purpose=purpose + " (Cabinet MicrophoneTypeSwitch)", src=SRC_BOOL.get(text, new))
        add(**c, kind="negative", outcome="refused") if exp is None else \
            add(**dict(c, reqs=["004", "006"]), kind="positive", outcome="opens", state_keys=["MicrophoneTypeSwitch"],
                state={"MicrophoneTypeSwitch": exp})

    def dup(path):
        def edit(tree):
            *g, leaf = path.split("/")
            parent = B.find(tree, "/".join(g)) if g else tree
            i = next(i for i, k in enumerate(parent.kids) if k.tag == leaf)
            parent.kids.insert(i + 1, parent.kids[i].clone())
        return edit

    def dup_manual(path):
        def edit(tree):
            node = B.find(tree, path)
            i = next(i for i, k in enumerate(node.kids) if k.tag == "Manual")
            node.kids.insert(i + 1, node.kids[i].clone())
        return edit

    def insert(path, node_fn, where):
        def edit(tree):
            parent = B.find(tree, path) if path else tree
            i = {"first": 0, "last": len(parent.kids)}.get(where)
            if i is None:
                i = next(i for i, k in enumerate(parent.kids) if k.tag == where) + 1
            parent.kids.insert(i, node_fn())
        return edit

    add(device="Cabinet", kind="negative", reqs=["002"], edits=[dup("CabinetType")], outcome="refused", prov=PS,
        purpose="Cabinet with the CabinetType parameter element twice", src="BDP-012 (moved from Amp Bass to Cabinet CabinetType)")
    add(device="LoungeLizard", kind="negative", reqs=["002"], edits=[dup_manual("KeyboardStretch")], outcome="refused",
        prov=PS, purpose="Electric KeyboardStretch with two Manual elements", src="new case for the REQ-002 duplicate clause")
    add(device="Collision", kind="negative", reqs=["002"], edits=[dup("Resonator1/Quality")], outcome="refused",
        prov=PS, purpose="Collision with the Quality parameter twice in the Resonator1 group",
        src="new case for the REQ-002 duplicate clause")
    add(device="Collision", kind="negative", reqs=["002"], edits=[dup("Mallet")], outcome="refused", prov=PS,
        purpose="Collision with the Mallet group twice", src="new case for the REQ-002 duplicate clause")
    def repeat_attr(path):
        def edit(tree):
            node = B.find(tree, path + "/Manual")
            node.attrs.append(("Value", "3"))
        return edit

    add(device="Cabinet", kind="negative", reqs=["002"], edits=[repeat_attr("CabinetType")], outcome="refused", prov=PS,
        purpose="Cabinet CabinetType Manual with the Value attribute twice (not well-formed XML)",
        src="new case for the REQ-002 repeated-attribute clause")
    rows = {el: [m["path"] for m in tables[el] if "value" not in m] for el in NAMES}
    add(device="Amp", kind="positive", reqs=["011"], edits=[insert("", lambda: B.V("Foo", "1"), "last")],
        outcome="opens", prov=PDS, purpose="Amp with an unknown element Foo after its last member",
        src="BDP-029 (narrowed to the values read; save excluded)")
    add(device="LoungeLizard", kind="positive", reqs=["011"],
        edits=[insert("KeyboardStretch", lambda: B.N("Foo", kids=[B.V("Manual", "0.75")]), "Manual")],
        outcome="opens", state_keys=["KeyboardStretch"], prov=PDS,
        purpose="Electric KeyboardStretch with an unknown element Foo holding a Manual element; its content is not read",
        src="BDP-030 (narrowed to the value read; save excluded; moved from Amp Bass)")
    add(device="Collision", kind="positive", reqs=["011"], edits=[insert("Resonator1", lambda: B.V("Foo", "1"), "last")],
        outcome="opens", state_keys=[p for p in rows["Collision"] if p.startswith("Resonator1/")], prov=PDS,
        purpose="Collision with an unknown element Foo at the end of the Resonator1 group", src="new case for the REQ-011 unknown-element clause")
    add(device="StringStudio", kind="positive", reqs=["011"], edits=[insert("", lambda: B.N("Foo"), "first")],
        outcome="opens", prov=PDS, purpose="Tension with an empty unknown element Foo before its first member",
        src="new case for the REQ-011 unknown-element clause")
    for el, lab in B.LABELS.items():
        mid = B.base_values(tables[el], "mid")
        for k in range(max(len(v) for v in lab.values())):
            vals = {p: (bool(k % 2) if p == "MicrophoneTypeSwitch" else k % len(v)) for p, v in lab.items()}
            if all(vals[p] == mid[p] for p in lab):
                continue  # same fixture as the mid case, which carries these labels
            add(device=el, kind="positive", reqs=["006", "014"], values=vals, outcome="opens", state_keys=list(lab),
                labels={p: v[k % len(v)] for p, v in lab.items()}, prov=PS,
                src={("Amp", 4): "BDP-035 (authored fixture instead of shipped F5)",
                     ("Corpus", 5): "BDP-036 (authored fixture instead of shipped F7)"}.get((el, k), "new case for a REQ-014 label list"),
                purpose=f"{NAMES[el]} labels for " + ", ".join(f"{p} {vals[p] if not isinstance(vals[p], bool) else str(vals[p]).lower()}" for p in lab))
    return out


EXCL_INPUTS = [
    "a document whose device element lacks a member of its table, holds its members in another order, or differs from the fixture form in any way its case does not state",
    "a Manual element without a Value attribute, and every other missing element or attribute",
    "a parameter element with a KeyMidi child (a parameter mapped to a rack macro or MIDI)",
    "MidiControllerRange or MidiCCOnOffThresholds values other than the fixture form; LomId, LockEnvelope or target Id values other than 0",
    "plain field values other than those in the tables",
    "Float, Enum or Bool values outside their domain, and fractional values of whole-number parameters",
    "Float text whose remainder after leading spaces and an optional sign starts with 0x or 0X, or with inf or nan in any letter case; the text Invalid; text starting with #; leading whitespace other than U+0020",
    "Enum text with spaces both before and after the digits, or with a plus sign and trailing spaces; Enum text with a minus sign; Enum text longer than 63 characters that ends in a space",
    "duplicated plain fields and duplicated children of a parameter other than Manual; repeated unknown elements",
    "element names that the original may define for a parent although this release does not list them, including the members shared by all devices and KeyMidi",
    "unknown attributes on any element",
    "root attributes other than exactly MajorVersion 5, MinorVersion 12.0_12402 and SchemaChangeCount 1; other format versions and their upgrade; a second child of the root",
    "XML that differs from the fixtures' form in a way no rule names: other declarations or encodings, document type declarations, comments or processing instructions, namespaces, entity or character references, carriage returns",
    "the compressed file container; racks, Live Sets, clips and any other document kind",
    "documents that break more than one rule",
]
EXCL_BEHAVIOR = [
    "the value of a parameter whose element or Value is missing (REQ-BUNDLED-DEVICE-PARAMETERS-008)",
    "the values of a newly inserted device (REQ-BUNDLED-DEVICE-PARAMETERS-009)",
    "what is opened, displayed, used and saved for out-of-range, narrower-range and fractional values (REQ-BUNDLED-DEVICE-PARAMETERS-010)",
    "everything written on save: element order and omissions, value text, ranges and target identifiers (REQ-BUNDLED-DEVICE-PARAMETERS-005)",
    "rack macro and MIDI bindings (REQ-BUNDLED-DEVICE-PARAMETERS-013)",
    "the value read for a Corpus or Collision position parameter, and what part of the resonator it addresses (REQ-BUNDLED-DEVICE-PARAMETERS-015)",
    "labels other than those of REQ-BUNDLED-DEVICE-PARAMETERS-014, including Cabinet MicrophoneTypeSwitch; display text and units",
    "the meaning of plain fields; the members shared by all devices",
    "sound, the values sent to the sound engine, playback and timing",
    "edits after opening, automation and modulation, undo, presentation of refusals",
]

REVIEW = {  # separate handoff review, 2026-10-18 (record: REVIEW.md in the payload)
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVB-01 medium: Cabinet MicrophoneTypeSwitch labels; the review's static reading gives true Dynamic, false Condenser, the reverse of the candidate; narrowed, its labels excluded from REQ-BUNDLED-DEVICE-PARAMETERS-014 and from six cases; its values stay judged in five other cases",
        "RVB-02 low: values of the nine Corpus and Collision position parameters were judged in seven cases although REQ-BUNDLED-DEVICE-PARAMETERS-015 is unreleased; narrowed, 30 state entries removed, table rows kept and marked",
        "RVB-03 editorial: comparison obligation now inserts the shared members at the start of the device element, so the input of the case with an unknown element before the first member is unambiguous",
        "RVB-04 info: ranges, whole-number marks, labels and the value text rules re-derived per device from the static evidence; every expectation re-derived by the review's own reading; no other difference",
        "RVB-05 info: the draft's stored-field claims, side-chain field list and inexact label lists checked against every shipped document; none reaches the payload",
        "RVB-06 info: upper Enum bounds of 22 Analog, Tension and Collision parameters rest on the stored range alone; accepted under the stated assumption",
        "RVB-07 info: evidence identity re-hashed; all digests match",
        "RVB-08 info: sharing; element names, kinds, stored ranges and plain-field texts are document facts, values are computed; no shipped preset content",
        "RVB-09 editorial: payload status wording set to reviewed release; review record added",
    ],
    "disposition": "Approved with listed narrowing (RVB-01, RVB-02), only for the explicit partial clauses; expectations documented and static-derived; reference and candidate execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}


def manifest_meta(n, target):
    scopes = {
        "001": "Element names of the seven devices; in a device preset the device element is the root's only child",
        "002": "Members of each device element and group in table order; duplicated parameters, groups and Manual elements refused",
        "003": "Element shapes of Float, Enum and Bool parameters and plain fields; fixture form",
        "004": "Manual text on load for Float, Enum and Bool parameters within the domain, with the listed exclusions",
        "006": "Domains of the tables; values within the domain are the values read, except the position parameters of REQ-BUNDLED-DEVICE-PARAMETERS-015",
        "007": "Whole-number Float parameters hold whole numbers; fractional values have no expectation",
        "011": "Unknown elements under the device element, a group or a parameter skipped with their content; documented plain field values",
        "012": "Target Id attribute present; device presets store 0",
        "014": "Labels of Amp AmpType; Cabinet CabinetType, MicrophonePosition; Electric PickupModel; Corpus ResonanceType, ResonatorQuality, MidiMode",
    }
    return {
        "schema": "handoff-manifest-v1", "release_id": "bundled-device-parameters-v1",
        "release_status": "released", "release_date": "2026-10-18", "target": target,
        "specification": {"id": "SPEC-BUNDLED-DEVICE-PARAMETERS", "parent_revision": 1, "release_revision": 1},
        "feature_ids": ["FEAT-DEVICES", "FEAT-PERSISTENCE"],
        "partial_requirement_scopes": {REQ + k: v for k, v in scopes.items()},
        "unreleased_requirements": [REQ + k for k in ("005", "008", "009", "010", "013", "015")],
        "compatibility_dimensions": {
            "device-preset-reading": "documented and static-derived expectations; reference execution not-run",
            "enumeration-labels": "static-derived expectations for the listed parameters; reference execution not-run",
            "file-format-written": "excluded (REQ-BUNDLED-DEVICE-PARAMETERS-005)",
            "defaults": "excluded (REQ-BUNDLED-DEVICE-PARAMETERS-008, 009)",
            "out-of-range-values": "excluded (REQ-BUNDLED-DEVICE-PARAMETERS-010)",
            "audio": "excluded", "timing": "excluded", "ui-other-than-labels": "excluded"},
        "exclusions": {"inputs_without_expectation": EXCL_INPUTS, "behavior": EXCL_BEHAVIOR},
        "fixture_origin": "independently authored device presets written from the parameter tables with computed values; no shipped file content, program code or assets",
        "approved_public_sources": [],
        "review": REVIEW,
        "supersedes": None, "entrypoint": "README.md", "case_count": n,
        "inventory_excludes": ["manifest.json (self-hash recorded outside package)"], "files": [],
    }
