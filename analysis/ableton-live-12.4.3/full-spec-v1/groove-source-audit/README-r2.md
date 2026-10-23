# Grooves audit association correction R2

The [full R1 review](../reviews/groove-source-audit-review.json) requested
GSA-REVIEW-001: assessment GSA-A028 concerns extracting a Rack chain, whereas its
primary Groove012/GRV012 associations concern extracting a groove from a clip.
The source/action distinction is material even though the original assessment's
prose and external Racks022/RCK046 references were correct.

[correction-r2.json](correction-r2.json) clears only those two primary association
arrays in the current audit view. Apply its two literal JSON-pointer replacements
to audit.json; all remaining values stay exact. No generic resolver or parallel
source catalog is added. All six R1 files, original review, source bytes,32blocks,
17resources,14contracts/24cases,32whole-block assessments,10proposals and every
external reference remain untouched. No owner requirement/case or oracle changes.

The retained [R1 read scope and limits](README.md) still apply. Date-only source
capture keeps exact UTC unknown; pixels/destinations and target behavior remain
uninspected/U/unexecuted. Source accounting and a corrected association do not
establish normative adoption, compatibility or completed behavior.

Inspect [check-r2.py](check-r2.py) before this read-only command:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/groove-source-audit/check-r2.py --check
```

It verifies preserved R1 files/review/15inputs, reconstructs exactly the two-field
current view, retains the original pure guards and checks three focused unsafe
mutations. It does not run the old main/check cohort or change old results. No
write mode, source/vendor/original/runtime/input/network/candidate operation exists.
This is a concrete required-review correction, not automatic historical replay.

**AS-OF AUTHOR FREEZE:** focused independent R2 review remains pending. Shared
indexes/plan record subsequent disposition; the full R1 review remains immutable.
