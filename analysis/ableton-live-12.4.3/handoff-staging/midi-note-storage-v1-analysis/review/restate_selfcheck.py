"""Reviewer check: the restatement is not vacuous. Mutated expectations must be detected, and the
author's excluded-input probes (fixtures built with mns_cases.py) must get no expectation or refusal.
usage: python3 -I restate_selfcheck.py <package dir> <author analysis dir>"""
import copy, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(1, sys.argv[2])
import restate
from mns_cases import PROBES, document, gz
pkg = Path(sys.argv[1]); cases = {c["id"]: c for c in json.loads((pkg / "cases.json").read_text())["cases"]}
def mut(cid, f):
    c = copy.deepcopy(cases[cid]); f(c); got, why = restate.judge(c, (pkg / c["input"]).read_bytes())
    return "detected" if not (got == c["expected"]["outcome"] and (got == "refused" or not why)) else "MISSED"
sn = lambda c: c["expected"]["saved_notes"]
M = {"MNS-020 Time unrounded": ("MNS-020", lambda c: sn(c)["key_tracks"][0]["notes"][0].__setitem__("Time", "0.123456789")),
     "MNS-047 Value unclamped": ("MNS-047", lambda c: sn(c)["event_lists"][0]["events"][0].__setitem__("Value", "9000")),
     "MNS-033 next id 100": ("MNS-033", lambda c: sn(c).__setitem__("note_id_next", "100")),
     "MNS-051b list kept": ("MNS-051b", lambda c: sn(c)["event_lists"].append({"NoteId": "1", "CC": "-2", "events": []})),
     "MNS-019 Velocity 33.3": ("MNS-019", lambda c: sn(c)["key_tracks"][0]["notes"][1].__setitem__("Velocity", "33.3")),
     "MNS-004 order": ("MNS-004", lambda c: sn(c)["key_tracks"][0]["notes"].__setitem__(0, dict(reversed(list(sn(c)["key_tracks"][0]["notes"][0].items()))))),
     "MNS-046 loads": ("MNS-046", lambda c: c["expected"].__setitem__("outcome", "loads"))}
for k, (cid, f) in M.items():
    print("mutation", k, mut(cid, f))
for name, frag in PROBES.items():
    try:
        out = restate.evaluate(gz(document(frag)))
        print("probe", name, "loads, order_ok=%s" % out[1])
    except (restate.NoExpectation, restate.Refused, AssertionError) as e:
        print("probe", name, type(e).__name__, e)
