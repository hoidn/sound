"""Set the mix-graph-v1 manifest's scopes, exclusions, review and status fields and re-hash the inventory.

usage: python3 -I -B finalize_manifest.py
Run after apply_review_edits.py and after REVIEW.md is written. Writes manifest.json in the author's layout
(json indent 1, final newline) and prints its SHA-256. Re-runnable.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "mix-graph-v1"
p = PKG / "manifest.json"
m = json.loads(p.read_text())
R = "REQ-MIX-GRAPH-"
s = m["partial_requirement_scopes"]
s[R + "013"] = ("Playback value of an envelope as a computation: point list with the first time of a Float envelope at "
                "-10,000,000 beats, 16-piece curved segments, lookup at envelope time with the later of two equal times, "
                "segment value in samples under the default automation settings, hold, Bool and Enum without "
                "interpolation at or after the first event; envelope time, the samples at which point times take effect, "
                "drive, each parameter's automation settings and units not released")
s[R + "014"] = ("Ramp length of an automated value under the default automation settings: max(200, min(65536, "
                "trunc(q / |slope|))) while playing, none for a flat segment or a stopped transport; last ramp shortened, "
                "new segment at each point; q is an input (one thousandth of the driven parameter's range); which "
                "parameters use the default settings, and their q, not released; only q / |slope| below 2^31")
inp = m["exclusions"]["inputs_without_expectation"]


def swap(lst, old, new):
    if new in lst:
        return
    i = lst.index(old)
    lst[i] = new


swap(inp, "a send stored above its minimum 0.0003162277571 whose output can reach the main track (its track's send gate "
          "on and the return playing); sends with EnabledByUser false above their minimum",
     "a send stored above its minimum 0.0003162277571 whose output can reach the main track (its track's send gate not 0 "
     "and its return track's main gate not 0); sends with EnabledByUser false above their minimum")
swap(inp, "automation envelopes that drive a mixer or device parameter during a render case; clip envelopes",
     "in render cases, automation envelopes on any mixer or device parameter other than the main track's one-event tempo "
     "and time-signature envelopes whose single event equals the stored value (every fixture holds these two); clip "
     "envelopes")
beh = m["exclusions"]["behavior"]
swap(beh, "which envelope drives a parameter and when, the mapping from song position to envelope time, and automated "
          "against manual values (REQ-MIX-GRAPH-012, 016)",
     "which envelope drives a parameter and when, the mapping from song position to envelope time and the samples at "
     "which point times take effect, and automated against manual values (REQ-MIX-GRAPH-012, 016)")
extra = "which parameters use the default automation settings, and the value step of any parameter"
if extra not in beh:
    beh.insert(1, extra)
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RMG-01 medium: REQ-013's Float value and REQ-014 hold only for the default automation settings; two stated "
        "assumptions bound mixer parameters and pan's step to them; narrowed to the defined default settings, which "
        "parameters use them and their step not released, assumptions removed; no case changed",
        "RMG-02 low: the render-case envelope exclusion contradicted the main track's one-event tempo and "
        "time-signature envelopes in every fixture; those two exempted when equal to the stored value; no case changed",
        "RMG-03 low: REQ-013's sample-timing sentence depends on the unreleased song-position mapping and the "
        "first-time replacement was shown for Float envelopes only; moved to not released and scoped; no case changed",
        "RMG-04 info: ramp-length rule fails for q/|s| of 2^31 or more (reviewer's static check); exclusion upheld",
        "RMG-05 info: out-of-range stored volumes and the draft internal-predicate case stay out; one sentence reworded",
        "RMG-06 info: no expectation depends on an open item; every render case is labeled composed spec conformance "
        "and was recomposed and rendered by the reviewer",
        "RMG-07 info: all 11 fixtures pass the structural checker and the reviewer's shape check; signals generated",
        "RMG-08 editorial: category labels, pan-law provenance and send-exclusion wording",
        "RMG-09 editorial: payload status set to reviewed release; review record added",
        "RMG-10 info: evidence identity re-hashed; all match",
    ],
    "disposition": "Approved with listed narrowing (RMG-01 to RMG-03), only for the explicit partial clauses; 28 cases "
                   "released unchanged; computation expectations extracted execution or static-derived as labeled; "
                   "render expectations composed spec conformance, not measured compatibility; reference and candidate "
                   "execution not-run; restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(f for f in PKG.rglob("*") if f.is_file() and f.name != "manifest.json")
m["files"] = [{"path": str(f.relative_to(PKG)), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
               "bytes": f.stat().st_size} for f in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files;", "manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
