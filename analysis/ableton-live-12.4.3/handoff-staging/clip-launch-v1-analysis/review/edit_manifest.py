"""Reviewer edits to clip-launch-v1/manifest.json: scope, exclusions, review record, status.

usage: python3 -I edit_manifest.py <package dir>   (then verify_copy.py <package dir> --rehash)
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / "manifest.json"
m = json.loads(p.read_text())
R = "REQ-CLIP-LAUNCH-"
s = m["partial_requirement_scopes"]
assert s.pop(R + "015").startswith("Grid length")
s[R + "001"] = ("Launch elements of session MIDI and audio clips and arrangement MIDI clips: location, types, reading "
                "rules, refusal of refused text and of a repeated launch element, saved form, relative order, and "
                "read-back value for Booleans and numbers of at most six significant digits. Saved text not released")
s[R + "005"] = ("Clip launch quantization 0-14 and global quantization 0-13 with labels; clip value k>=1 denotes the "
                "setting of global value k-1, clip value 0 the set's global setting; use at launch excluded")
s[R + "014"] = ("Conversion steps 406, 417 and 421 for clips of 11.0_405 documents and 12203 for scenes of 12.0_12117 "
                "documents, applied before reading; no conversion at 12.0_12402; other conversion steps excluded")
m["unreleased_requirements"] = sorted(m["unreleased_requirements"] + [R + "015"])
ex = m["exclusions"]["inputs_without_expectation"]
def rep(lst, old_start, new):
    i = [k for k, x in enumerate(lst) if x.startswith(old_start)]
    assert len(i) == 1, old_start
    lst[i[0]] = new
rep(ex, "a launch element or follow-action child without",
    "an item of the item table without a Value attribute, with other attributes or with child elements")
rep(ex, "VelocityAmount outside 0-1",
    "VelocityAmount outside 0-1; chances negative or above 100; jump indices outside -1 to 8,388,608; "
    "LoopIterations outside 1 to 1,073,741,823; FollowTime negative, 1,000,000 or more, or within 1e-9 of a "
    "half-multiple of 1/3,843,840; non-finite values and negative zero")
rep(ex, "clips other than at the named locations",
    "clips other than at the named locations, including take lanes and the groove pool; more than one clip at a "
    "named location")
bh = m["exclusions"]["behavior"]
rep(bh, "launching:",
    "launching: start time, the grid length of a quantization value, grid placement, the time signature a launch "
    "uses, launches without a grid or with the transport stopped, Gate, Toggle and Repeat, Legato, velocity scaling, "
    "follow-action timing, loop iterations, jump indices and chance selection")
rep(bh, "text written for numbers",
    "text written for numbers and Booleans, and exact read-back of a written number with more than six significant "
    "digits; layout; save container and envelope; saved form of set-level values and of scenes")
rep(bh, "conversion steps other than",
    "conversion steps other than 406, 417, 421 and 12203; the conversion error for a clip that has both forms; "
    "documents older than 11.0_405")
rep(bh, "effect of record quantization",
    "effect of record quantization; scene follow actions other than their conversion; the key and MIDI assignment "
    "of the global quantization")
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVC-01 medium: REQ-015 grid length has no observable outside launching (excluded, Q-017 timing); removed from the release, now unreleased",
        "RVC-02 low: REQ-001 clause 6 claimed exact read-back of every written number although saved number text is unknown; narrowed to Booleans and numbers of at most six significant digits; no case affected",
        "RVC-03 low: assumption 'present value kept as read, without adjustment to a range' implied unchecked storage of out-of-range floats; narrowed to values inside the precondition ranges; no case affected",
        "RVC-04 low: REQ-014 clause 2 read as an exhaustive list of conversion steps; other steps apply to older documents; reworded, reviewer confirmed none changes an item of this release",
        "RVC-05 low: REQ-005 said clip value 0 'uses' the global setting, a launch-behavior phrase; reworded as meaning; use at launch excluded",
        "RVC-06 editorial: spec and manifest exclusions aligned (item shape, non-finite values, several clips, old clip-level FollowActionEnabled or IsLinked, loop iterations and jump indices at launch, global-quantization key assignment)",
        "RVC-07 editorial: payload status wording set to reviewed release; review record added and linked",
        "RVC-08 info: scene conversion step 12203 confirmed in the retained disassembly; scene cases stay graded",
        "RVC-09 info: follow-time rounding instruction sequence re-read; nearest multiple, halves away from zero, confirmed",
        "RVC-10 info: REQ-011 message prefixes not observable as established and outside scope; not carried; draft spec must be corrected",
        "RVC-11 info: assumptions ruled on; out-of-range chances carry no expectation; evidence identity re-hashed and matched",
    ],
    "disposition": "Approved with listed narrowing (RVC-01 to RVC-05), only for the explicit partial clauses; "
                   "expectations static-derived; reference and candidate execution not-run; restricted "
                   "implementation workspace required",
    "record": "REVIEW.md",
}
p.write_text(json.dumps(m, indent=1) + "\n")
print("manifest edited")
