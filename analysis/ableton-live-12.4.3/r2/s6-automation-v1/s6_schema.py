"""S6 static half: automation classes across all shipped schema files.

Usage: python3 -I s6_schema.py <Schema dir> <out.json>
For the automation vocabulary (envelopes, events, targets, ListAutomation and the
fields that hold them) records, per class, the ordered segments of versions with an
identical field list, and for 12.0_12402 the field table with 1-based line numbers and
the owner classes of every *Target-class field. Version order is (major, minor,
translator) from the file name. Read-only; output is data.
"""
import collections, hashlib, json, os, re, sys
import xml.etree.ElementTree as ET

CLASSES = re.compile(r"^(AutomationEnvelopes?|ClipEnvelopes?|ListAutomation|(Float|Bool|Enum)(Event|AutomationTarget)"
                     r"|PerNoteEvent|PtrBase|Pointee|TimeableModulationTarget|UserFloatModulationTarget|"
                     r"AutomationTransformViewState|TimeAndValueTransform|TrackAutomationEnvelopeParent|"
                     r"Timeable(Float|Bool|Enum|SongTempo|TimeSignature|PluginFloat|PluginEnum|MidiClip|Sample)|"
                     r"MidiControllers|AutomationLanes?|TakeLane)$")
HOLDER_FIELDS = re.compile(r"^(AutomationEnvelopes|Envelopes|ArrangerAutomation|ModulationAutomation|ClipAutomation|"
                           r"AutomationTarget|ModulationTarget|NextPointeeId|AutomationMode|SnapAutomationToGrid|"
                           r"UserTempoAutomation|AutomationEnvelopesListWrapper)$")


def vkey(name):
    return tuple(int(x) for x in re.fullmatch(r"(\d+)\.(\d+)_(\d+)\.txt", name).groups())


def main():
    sdir, out = sys.argv[1:3]
    files = sorted((f for f in os.listdir(sdir) if not f.startswith("._")), key=vkey)
    seg = collections.defaultdict(list)       # class -> [[first, last, fields]]
    holders = collections.defaultdict(list)   # (owner, field, class, type) -> versions
    digests = []
    for f in files:
        data = open(os.path.join(sdir, f), "rb").read()
        digests.append([f, hashlib.sha256(data).hexdigest()])
        v = f[:-4]
        for c in ET.fromstring(data):
            fields = [[x.tag, x.get("Class"), x.get("Type")] for x in c]
            if CLASSES.match(c.tag):
                s = seg[c.tag]
                if s and s[-1][2] == fields and s[-1][1] == prev_of(files, f):
                    s[-1][1] = v
                else:
                    s.append([v, v, fields])
            for x in c:
                if HOLDER_FIELDS.match(x.tag):
                    holders[f"{c.tag}.{x.tag}:{x.get('Class')}:{x.get('Type')}"].append(v)
    latest = files[-1]
    lines = open(os.path.join(sdir, latest), encoding="utf-8").read().split("\n")
    pos = {m.group(1): i + 1 for i, l in enumerate(lines) for m in [re.match(r"^\t<(\w[\w.]*)>$", l)] if m}
    table, target_owners = {}, collections.defaultdict(list)
    for c in ET.parse(os.path.join(sdir, latest)).getroot():
        if CLASSES.match(c.tag):
            table[c.tag] = {"line": pos.get(c.tag), "fields": [[x.tag, x.get("Class"), x.get("Type")] for x in c]}
        for x in c:
            if (x.get("Class") or "").endswith("Target"):
                target_owners[x.get("Class")].append(f"{c.tag}.{x.tag}")
    json.dump({
        "schema_files": len(files), "order": "(major, minor, translator) from file name",
        "digests": digests, "latest": latest,
        "segments": {k: [{"from": a, "to": b, "fields": fl} for a, b, fl in v] for k, v in sorted(seg.items())},
        "holder_fields": {k: {"count": len(v), "first": v[0], "last": v[-1]} for k, v in sorted(holders.items())},
        "latest_classes": dict(sorted(table.items())),
        "latest_target_owner_counts": {k: len(v) for k, v in sorted(target_owners.items())},
        "latest_target_owner_examples": {k: sorted(v)[:15] for k, v in sorted(target_owners.items())},
    }, open(out, "w"), indent=1)


def prev_of(files, f):
    """Version immediately before f in sort order (None for the first)."""
    i = [x[:-4] for x in files].index(f[:-4])
    return files[i - 1][:-4] if i else None


if __name__ == "__main__":
    main()
