"""Reviewer check: the v2 restatement is not vacuous (analyst side; never shipped).

Mutated expectations of the new cases (and of v1's mutation set) must be detected. Probe fixtures made by
changing one attribute text of a package fixture must get no expectation where the contract gives none
(negative zero outside the five note attributes, magnitudes of 1,000,000) and the stated result elsewhere.
usage: python3 -I -B restate_selfcheck.py <package dir>
"""
import copy, gzip, json, sys, zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import restate  # noqa: E402

pkg = Path(sys.argv[1])
cases = {c["id"]: c for c in json.loads((pkg / "cases.json").read_text())["cases"]}


def judged_ok(c, raw):
    got, why = restate.judge(c, raw)
    return got == c["expected"]["outcome"] and (got == "refused" or not why)


def mut(cid, f):
    c = copy.deepcopy(cases[cid])
    f(c)
    return "detected" if not judged_ok(c, (pkg / c["input"]).read_bytes()) else "MISSED"


def note(c, t, i):
    return c["expected"]["saved_notes"]["key_tracks"][t]["notes"][i]


M = {
    "MNS-023 Time 0": ("MNS-023", lambda c: note(c, 0, 0).__setitem__("Time", "0")),
    "MNS-072 Time 0 (exact rounding)": ("MNS-072", lambda c: note(c, 0, 0).__setitem__("Time", "0")),
    "MNS-073 OffVelocity 0": ("MNS-073", lambda c: note(c, 0, 0).__setitem__("OffVelocity", "0")),
    "MNS-073 Probability omitted": ("MNS-073", lambda c: note(c, 0, 1).pop("Probability")),
    "MNS-074 Duration -0": ("MNS-074", lambda c: note(c, 0, 1).__setitem__("Duration", "-0")),
    "MNS-074 Time -0": ("MNS-074", lambda c: note(c, 1, 0).__setitem__("Time", "-0")),
    "MNS-074 Velocity -0 kept": ("MNS-074", lambda c: note(c, 0, 0).__setitem__("Velocity", "-0")),
    "MNS-075 Velocity 127.000008": ("MNS-075", lambda c: note(c, 0, 0).__setitem__("Velocity", "127.000008")),
    "MNS-075 Velocity 0.99999994": ("MNS-075", lambda c: note(c, 0, 1).__setitem__("Velocity", "0.99999994")),
    "MNS-020 Time unrounded": ("MNS-020", lambda c: note(c, 0, 0).__setitem__("Time", "0.123456789")),
    "MNS-047 Value unclamped": ("MNS-047", lambda c: c["expected"]["saved_notes"]["event_lists"][0]["events"][0]
                                .__setitem__("Value", "9000")),
    "MNS-046 loads": ("MNS-046", lambda c: c["expected"].__setitem__("outcome", "loads")),
}
for k, (cid, f) in M.items():
    print("mutation", k, mut(cid, f))


def probe(base, old, new):
    text = zlib.decompress((pkg / f"fixtures/{base}.als").read_bytes(), 31).decode()
    assert text.count(old) == 1, (base, old)
    raw = gzip.compress(text.replace(old, new).encode())
    try:
        saved, order_ok = restate.evaluate(raw)
        return "loads " + json.dumps(saved["key_tracks"][0]["notes"][0]) + " " + json.dumps(saved["event_lists"])
    except (restate.NoExpectation, restate.Refused) as e:
        return f"{type(e).__name__}: {e}"


N1 = '<MidiNoteEvent Time="0" Duration="0.25" Velocity="85" OffVelocity="64" NoteId="1" />'
P = {
    "VelocityDeviation -0": ("MNS-001", N1, N1.replace('OffVelocity', 'VelocityDeviation="-0" OffVelocity')),
    "VelocityDeviation -1e-50 (binary32 -0)": ("MNS-001", N1, N1.replace('OffVelocity', 'VelocityDeviation="-1e-50" OffVelocity')),
    "event Value -0": ("MNS-039", 'Value="100"', 'Value="-0"'),
    "event TimeOffset -0": ("MNS-039", 'TimeOffset="0.0625"', 'TimeOffset="-0"'),
    "event TimeOffset rounding to -0": ("MNS-039", 'TimeOffset="0.0625"', 'TimeOffset="-0.0000001"'),
    "curve control -0": ("MNS-039", 'TimeOffset="0.0625"', 'TimeOffset="0.0625" CurveControl1X="-0"'),
    "Time 1000000": ("MNS-001", N1, N1.replace('Time="0"', 'Time="1000000"')),
    "Time -0 (released)": ("MNS-001", N1, N1.replace('Time="0"', 'Time="-0"')),
    "Probability -0.0 (released)": ("MNS-001", N1, N1.replace('NoteId', 'Probability="-0.0" NoteId')),
    "OffVelocity -1e-50 (binary32 -0, released clause)": ("MNS-001", N1, N1.replace('OffVelocity="64"', 'OffVelocity="-1e-50"')),
}
for k, (base, old, new) in P.items():
    print("probe", k, "->", probe(base, old, new))
