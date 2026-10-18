"""Independent cross-check reader for bundled-device-parameters-v1 (analyst side).

Model(spec_md) reads only the payload contract: the device table of REQ-001, the parameter tables and the
label lists of REQ-014. Model.read(xml_bytes) applies the released rules to a device preset and returns
(outcome, state, labels) or raises NoExpectation for inputs the release excludes. It shares the static evidence
behind the contract and is not an oracle. Uses only the standard library (xml.etree on Expat).
"""
import copy, re, struct
import xml.etree.ElementTree as ET

ROOT_ATTRS = {"MajorVersion": "5", "MinorVersion": "12.0_12402", "SchemaChangeCount": "1"}
SHAPE = {"Float": ["LomId", "Manual", "MidiControllerRange", "AutomationTarget", "ModulationTarget"],
         "Enum": ["LomId", "Manual", "AutomationTarget", "MidiControllerRange"],
         "Bool": ["LomId", "Manual", "AutomationTarget", "MidiCCOnOffThresholds"]}
UNKNOWN = "Foo"


class NoExpectation(Exception):
    pass


class Refused(Exception):
    pass


def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def float_text(t):
    s = t.lstrip(" ")
    if t[:1] in "\t\n\r\f\v" and t:
        raise NoExpectation("leading whitespace other than space")
    body = s[1:] if s[:1] in "+-" else s
    if re.match(r"(?i)0x|inf|nan", body) or t == "Invalid" or t.startswith("#"):
        raise NoExpectation(f"excluded Float form {t!r}")
    m = re.match(r"[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", s)
    if not m:
        raise Refused("no decimal prefix")
    return f32(float(m.group(0)))


def enum_text(t):
    if t.strip(" ") == "" or not t.isascii():
        raise Refused("empty, spaces only or non-ASCII")
    s = t.lstrip(" ")
    lead, plus = len(s) < len(t), s.startswith("+")
    r = s[1:] if plus else s
    if r == "" or (plus and r.startswith("-")):
        raise Refused("nothing after plus, or plus then minus")
    body = r.rstrip(" ")
    digits = body[1:] if body.startswith("-") else body
    if any(c not in "0123456789" for c in digits):
        raise Refused("character other than a digit")
    if body.startswith("-") or body == "":
        raise NoExpectation("minus sign or plus with only spaces")
    if len(t) > 63:
        if t.endswith(" "):
            raise NoExpectation("long text ending in a space")
        raise Refused("longer than 63 characters")
    if len(r) > len(body) and (lead or plus):
        raise NoExpectation("decoration on both sides")
    return int(body)


def bool_text(t):
    if t in ("true", "1"):
        return True
    if t in ("false", "0"):
        return False
    raise Refused(f"Bool text {t!r}")


class Model:
    def __init__(self, spec_md):
        text = spec_md.read_text()
        req1 = text.split("### REQ-BUNDLED-DEVICE-PARAMETERS-001", 1)[1].split("\n### ", 1)[0]
        self.names = dict(re.findall(r"^\| (\w+) \| `(\w+)` \|$", req1, re.M))  # name -> element
        tables = text.split("## Parameter tables", 1)[1].split("\n## ", 1)[0]
        self.members = {}
        for el, body in re.findall(r"^### \w+ \(`(\w+)`\)\n(.*?)(?=^### |\Z)", tables, re.M | re.S):
            rows = re.findall(r"^\| `([^`]+)` \| ([\w ]+) \| (.+?) \| (.*?) \|$", body, re.M)
            self.members[el] = {p: (k, d, n) for p, k, d, n in rows}
            self.members[el]["__order__"] = [p for p, *_ in rows]
        req14 = text.split("### REQ-BUNDLED-DEVICE-PARAMETERS-014", 1)[1].split("\n## ", 1)[0]
        self.labels = {}
        for name, path, labs in re.findall(r"^- (\w+) `([^`]+)`(?: \([^)]*\))?: (.+)\.$", req14, re.M):
            self.labels.setdefault(self.names[name], {})[path] = labs.split(", ")
        assert set(self.names.values()) == set(self.members) and len(self.members) == 7

    def read(self, raw):
        try:
            root = ET.fromstring(raw)
        except ET.ParseError:
            return "refused", None, None
        if root.tag != "Ableton" or dict(root.attrib) != ROOT_ATTRS or len(root) != 1:
            raise NoExpectation("root")
        dev = root[0]
        if dev.tag not in self.members or dev.attrib:
            raise NoExpectation("device element")
        el, spec = dev.tag, self.members[dev.tag]
        order = spec["__order__"]
        groups = {"/".join(p.split("/")[:i]) for p in order for i in range(1, p.count("/") + 1)}
        state = {}
        try:
            self._walk(dev, "", spec, order, groups, state)
        except Refused:
            return "refused", None, None
        labels = {p: labs[int(state[p])] for p, labs in self.labels.get(el, {}).items()}
        return "opens", state, labels

    def _walk(self, node, prefix, spec, order, groups, state):
        expected = []
        for p in order:
            if p.startswith(prefix):
                head = p[len(prefix):].split("/")[0]
                if head not in expected:
                    expected.append(head)
        seen = []
        for c in node:
            if c.tag == UNKNOWN:
                continue
            if c.tag not in expected:
                raise NoExpectation(f"unlisted element {prefix}{c.tag}")
            full = prefix + c.tag
            if c.tag in seen:
                if full in groups or spec[full][0] in SHAPE:
                    raise Refused(f"duplicate {full}")
                raise NoExpectation(f"duplicate plain field {full}")
            seen.append(c.tag)
            if full in groups:
                if c.attrib:
                    raise NoExpectation("group attributes")
                self._walk(c, full + "/", spec, order, groups, state)
            elif spec[full][0] in SHAPE:
                state[full] = self._param(c, full, *spec[full])
            elif dict(c.attrib) != {"Value": spec[full][1].strip('`"')} or len(c):
                raise NoExpectation(f"plain field {full}")
        if seen != expected:
            raise NoExpectation(f"members of {prefix or 'device'} missing or reordered")

    def _param(self, c, path, kind, dom, note):
        kids = [k for k in c if k.tag != UNKNOWN]
        tags = [k.tag for k in kids]
        if tags.count("Manual") > 1:
            raise Refused("two Manual elements")
        if c.attrib or tags != SHAPE[kind]:
            raise NoExpectation(f"shape of {path}")
        lo, hi = dom.split("..") if kind != "Bool" else ("64", "127")
        for k in kids:
            sub = [(x.tag, dict(x.attrib), len(x)) for x in k]
            if k.tag == "LomId":
                ok = dict(k.attrib) == {"Value": "0"} and not len(k)
            elif k.tag == "Manual":
                ok = set(k.attrib) == {"Value"} and not len(k)
            elif k.tag in ("MidiControllerRange", "MidiCCOnOffThresholds"):
                ok = not k.attrib and sub == [("Min", {"Value": lo}, 0), ("Max", {"Value": hi}, 0)]
            else:
                ok = dict(k.attrib) == {"Id": "0"} and sub == [("LockEnvelope", {"Value": "0"}, 0)]
            if not ok:
                raise NoExpectation(f"{path}/{k.tag} not in fixture form")
        t = kids[1].attrib["Value"]
        v = {"Float": float_text, "Enum": enum_text, "Bool": bool_text}[kind](t)
        if kind != "Bool" and not float(lo) <= v <= float(hi):
            raise NoExpectation(f"{path} value {v} outside {dom}")
        if note == "whole numbers" and v != int(v):
            raise NoExpectation(f"{path} fractional")
        return v


def same(a, b):
    return type(a) is type(b) and a == b


def compare(model, raw, exp):
    try:
        outcome, state, labels = model.read(raw)
    except NoExpectation as e:
        return [f"model has no expectation: {e}"]
    errs = [] if outcome == exp["outcome"] else [f"outcome {outcome} != {exp['outcome']}"]
    if outcome == "opens" and exp["outcome"] == "opens":
        errs += [f"state {k}: {state.get(k)!r} != {v!r}" for k, v in exp.get("state", {}).items()
                 if not same(state.get(k), v)]
        errs += [f"label {k}: {labels.get(k)!r} != {v!r}" for k, v in exp.get("labels", {}).items() if labels.get(k) != v]
    return errs


def self_test(model, stage, cases):
    """Mutated expectations must be detected; excluded inputs must have no expectation in the model."""
    by_id = {c["id"]: c for c in cases}
    out = []

    def raw_of(cid):
        return (stage / by_id[cid]["input"]).read_bytes()

    first = {}
    for c in cases:
        first.setdefault((c["device"], c["purpose"].startswith("Complete"), c["expected"]["outcome"]), c["id"])
    mid = {d: first[(d, True, "opens")] for d in ("LoungeLizard", "Cabinet", "Collision")}
    for cid, mutate, what in [
        (mid["LoungeLizard"], lambda e: e["state"].update(KeyboardStretch=0.25000003), "state off by one binary32 step"),
        (mid["Cabinet"], lambda e: e["state"].update(CabinetType=3), "Enum state"),
        (mid["Cabinet"], lambda e: e["state"].update(DualMono=not e["state"]["DualMono"]), "Bool state"),
        (mid["Collision"], lambda e: e.update(outcome="refused"), "outcome"),
    ] + [(c["id"], lambda e: e["labels"].update({next(iter(e["labels"])): "x"}), "label")
         for c in cases if c["expected"].get("labels")][:1]:
        e = copy.deepcopy(by_id[cid]["expected"])
        mutate(e)
        out.append({"probe": f"mutated {what} in {cid}", "ok": bool(compare(model, raw_of(cid), e))})

    def variant(cid, path, fn, what):
        root = ET.fromstring(raw_of(cid))
        node = root[0]
        for part in path.split("/"):
            node = next(k for k in node if k.tag == part)
        fn(node)
        try:
            model.read(ET.tostring(root))
            ok = False
        except NoExpectation:
            ok = True
        out.append({"probe": f"excluded input has no expectation: {what}", "ok": ok})

    def manual(text):
        return lambda n: n.find("Manual").set("Value", text)

    e, c, col = mid["LoungeLizard"], mid["Cabinet"], mid["Collision"]
    for t in ["0x1", "-inf", "nan", "Invalid", "#3F000000", "\t0.5", "1.5", "-0.5"]:
        variant(e, "KeyboardStretch", manual(t), f"Float text {t!r}")
    for t in [" 3 ", "+3 ", "-1", "5", " " + "0" * 63 + "3 "]:
        variant(c, "CabinetType", manual(t), f"Enum text {t!r}")
    variant(col, "Resonator1/Transpose", manual("3.5"), "fractional whole-number value")
    variant(e, "KeyboardStretch", lambda n: n.remove(n.find("Manual")), "missing Manual")
    variant(e, "KeyboardStretch", lambda n: n.find("Manual").attrib.pop("Value"), "Manual without Value")
    variant(e, "KeyboardStretch", lambda n: n.insert(1, ET.Element("KeyMidi")), "KeyMidi child")
    variant(e, "KeyboardStretch", lambda n: n.find("AutomationTarget").set("Id", "7"), "target Id 7")
    variant(e, "KeyboardStretch", lambda n: n.find("MidiControllerRange/Max").set("Value", "0.5"), "narrower range")
    variant(e, "KeyboardStretch", lambda n: n.append(ET.Element("Bar")), "unknown name other than Foo")
    variant(col, "CurrentTab", lambda n: n.set("Value", "3"), "other plain field value")
    return out
