"""Set the mixer-values-v2 manifest's review and status fields, apply the review narrowing and re-hash (analyst side).

usage: python3 -I -B finalize_manifest.py
Run after apply_review_edits.py and after REVIEW.md is written. Writes manifest.json in the author's layout
(json indent 1, final newline) and prints its SHA-256.
"""
import hashlib, json
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "mixer-values-v2"
p = PKG / "manifest.json"
m = json.loads(p.read_text())


def swap(text, old, new):
    if new in text:  # already applied (re-run)
        return text
    assert text.count(old) == 1, old
    return text.replace(old, new)


sc = m["partial_requirement_scopes"]
sc["REQ-MIXER-VALUES-005"] = swap(sc["REQ-MIXER-VALUES-005"], "exact round trip at the seven listed curve points only;",
                                  "exact round trip at the seven listed curve points only; neither an exact return nor "
                                  "a bound for the round trip of other gains;")
sc["REQ-MIXER-VALUES-013"] = swap(sc["REQ-MIXER-VALUES-013"], "Pan-law gain matrix as computed values for w and v each 0 or 1 "
                                  "at the listed inputs only; which w and v the audio path supplies,",
                                  "Pan-law gains as computed values for w and v each 0 or 1 at the listed inputs only; the "
                                  "gain names are labels only; which w and v the audio path supplies, which signal each "
                                  "gain scales,")
sc["REQ-MIXER-VALUES-014"] = swap(sc["REQ-MIXER-VALUES-014"], "as computed values; the crossfader-to-position mapping,",
                                  "as computed values; no level at other positions, by interpolation or otherwise; the "
                                  "crossfader-to-position mapping,")
beh = m["exclusions"]["behavior"]
i = next(n for n, t in enumerate(beh) if t.startswith("the gains the audio path computes"))
beh[i] = swap(beh[i], "which w and v feed the pan law,", "which w and v feed the pan law, which signal each pan-law gain scales,")
tpl = m["supersession"]["fixture_changes"]["template_set"]
i = next(n for n, t in enumerate(tpl) if t.startswith("each track"))
tpl[i] = swap(tpl[i], "each track gains Name", "each track except the cue track gains Name")
m["release_status"] = "released"
m["release_date"] = "2026-10-18"
m["review"] = {
    "status": "approved",
    "reviewers": ["separate review agent (Claude Opus 5.5) in a coordinator-launched handoff-review context; "
                  "not the author; will not implement"],
    "date": "2026-10-18",
    "findings": [
        "RVM2-01 medium: REQ-005 said most gains between curve points cannot return unchanged; extracted execution of "
        "1,601 random gains gives 765 that do not; narrowed to the counting fact for -6 to 0 dB on the volume curve, "
        "no exactness or bound for other gains; no case affected",
        "RVM2-02 medium: REQ-013 stated how the gains scale the input channels and called the pan a balance control; "
        "that is application to audio; narrowed: gain names are labels, which signal each gain scales and application "
        "excluded; no case affected",
        "RVM2-03 low: REQ-014 implied a level at every position; narrowed to the seven listed positions, no level "
        "defined elsewhere; no case affected",
        "RVM2-04 low: REQ-013 described internal arithmetic for the 6e-17 cross-feed; restated as a result of "
        "MIXER-VALUES-070 absorbed by the 1e-12 bound",
        "RVM2-05 low: change list said each track gains name, colour, envelopes, group and routing; the cue track gains "
        "none; scenes' follow action not described; corrected in README, fixture_changes and fixture provenance",
        "RVM2-06 editorial: payload status set to reviewed release; review record added",
        "RVM2-07 info: forward snap of REQ-005 confirmed by extracted execution at all 101 points of both curves",
        "RVM2-08 info: all 37 fixtures pass the structural checker; none is expected to be refused",
        "RVM2-09 info: no case exercises a group track or other computed inputs; no expectation invented",
    ],
    "disposition": "Approved with listed narrowing, only for the explicit partial clauses; 80 cases; case records "
                   "MIXER-VALUES-001 to 037 carried from mixer-values-v1 on rebuilt fixtures; expectations "
                   "static-derived or extracted execution as labeled; reference and candidate execution not-run; "
                   "restricted implementation workspace required",
    "record": "REVIEW.md",
}
files = sorted(f for f in PKG.rglob("*") if f.is_file() and f.name != "manifest.json")
m["files"] = [{"path": str(f.relative_to(PKG)), "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
               "bytes": f.stat().st_size} for f in files]
p.write_text(json.dumps(m, indent=1) + "\n")
print(len(m["files"]), "files;", "manifest sha256", hashlib.sha256(p.read_bytes()).hexdigest())
