# Bounded MIDI Tools owner R4

AS-OF AUTHOR FREEZE: independent owner review pending. The shared
[spec index](../../../../wiki/specs/index.md) owns current disposition.
This is a partial documentary successor, not a target observation or complete
17-tool family. No original/vendor/UI/hardware/network operation ran.

The approved [full retained Tools audit](../midi-tools-source-audit/README.md)
is as-of R2. R4 instead starts from [current R3](README-r3.md): all 38 existing
files, 43 IDs, 72 cases and six gesture refinements are preserved. Twenty-one
existing common/tool rows append control/entry roles; MED073–093 add 21 finite
compound reset proposals. The current catalog is 93 cases, 77 D12 and 16 U.
All actual outcomes remain null/U/not-run. All 21 new legacy expected/comparator
pairs are null; three new named-control documentary comparisons are nonnull
and 18 sensitive/context comparisons are null. Legacy documentary predicates
remain exact, never actual measurements.

[Increment](tools-increment-r4.json) and [delta](delta-r4.json) record bounded
subsets of all 21 audit groups, not closure of their every assertion or lifecycle.
[Guards](fixtures-r4.json) require actual nonempty generator output before
bounds/capacity/origin/absence, and a productive matched operation before negative
comparisons. Empty initial generator targets are allowed. New Strum MED086
requires actual nonzero start offsets before zero reset; old MED036 stays the
historical zero-only case. Current MPE lane/mode actions are selected context,
not Glissando tool-display equivalence. C1/C2/C3, implicit selection/loop context,
MTA-Q04, Q052/Q053 and source-silent lifecycle outcomes stay open.

[Inputs](inputs-r4.json) are immutable snapshots/source/audit/review identities,
not evolving canonical gates. [Prior identities](prior-files-r4.json) preserve
all old bytes in place without a duplicate archive. The
[consumer census](consumer-impact-r4.json) preserves four qualified old-hash
occurrences in one frozen review. Old checks/reports remain as-of; no automatic
adapter or historical replay is required or claimed.

Run the current owned checks only:

```
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/author-r4.py --check
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/validate-r4.py --check
```

Both are read-only in check mode. Author write mode refuses a sealed packet or
existing outputs. Validator checks original sources/302 quotation pointers,
source-qualified new cases, exact R3 preservation, selected current MPE pointers,
Browser IDs, links, whitespace and unsafe mutation fixtures. It imports only
owned pure parser/build code as analyst code; source HTML/examples never execute.
Exact source publication revision/12.4.3 parity and capture UTC remain unknown.
42 image pixels and 17 link destinations were not inspected. Current source
checks establish documentary identity only, never a passing target behavior.

Pre-seal check development: the first equality check incorrectly compared raw
parser resources with audit-added annotations; the corrected check verifies
both dimensions explicitly. A negative wrong-source fixture initially used an
invalid dictionary path and raised KeyError; it now uses a valid wrong block
and verifies rejection by identity. Both were corrected before sealing. No
initial pass, original runtime outcome or frozen-input mutation is claimed.
