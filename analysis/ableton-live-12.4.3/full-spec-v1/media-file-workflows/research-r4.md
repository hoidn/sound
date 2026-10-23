---
id: RESEARCH-MEDIA-FILE-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3
---

# Media/cache/analysis and clip interchange evidence

The [canonical contract](../specs/media-file-workflows.md) closes a documentation
ownership gap left deliberately by project/media and render packets. It reuses
the exact Managing Files HTML and source identity from
[project/media research](project-media-workflows.md); no duplicate chapter bytes
or new source revision are created. Exact hash and six heading locators are
in [sources.json](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/sources.json).

The captured manual supports useful file/reference/UI workflows but not decoder
algorithms or sample/byte equality. Compressed files may decode promptly while a
long sample still cannot play during analysis; these statements concern distinct
states and do not justify a timing guarantee. Existing valid ASD/default/creation/
auto-warp branches require independent setups, not a single blanket cache law.
The practical meaning of arbitrary length/rate/depth is left bounded by valid
inputs and unknown resource/codec limits.

The partial draft has17 requirements/32 case definitions spanning import formats,
cache controls/refusal/relocation, sidecar identity/readiness/defaults, MIDI file
ownership/destinations/export and Live Clip load classes. All exact target grades
are U; malformed/failure/cancel/undo/teardown and numerical/format oracles remain
null. No assets, cache, Set, original function or candidate was operated on.
The unchanged clauses retain their prior independent partial review; the R4
case-history correction requires focused independent review. This is not a complete
file-format or persistence contract.

## R4 explicit creation-On/Off history correction

The [approved owner reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-owner-reconciliation-review.json)
identified that historical MF-011 used unspecified default analysis options,
whereas MF-015 explicitly selected Off. [SET-B058](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/source-blocks.json)
states that Create Analysis Files determines creation on import. The retained
[analysis-files-asd source](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#analysis-files-asd)
separately describes first-add creation, analysis completion, existing ASD,
Auto-Warp Long Samples Off, creation Off and Save Default Clip exceptions.

[Current cases R4](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/cases-r4.json)
change only the MF-011 and MF-015 action fields: explicit On and explicit Off
with separate fresh initially no-ASD owned copies, writable directories, an
independently admitted analysis path, recorded other settings and genuinely
completed productive analysis. Unavailable controls, ineligible sources or failed,
suppressed or incomplete analysis cannot establish a passing no-sidecar observation. The paired histories
are future prerequisites, not executed results or a sidecar codec/transaction law.
The legacy documentary predicates/basis/unknown fields and exact-target U/not-run
metadata are unchanged; no actual expectation, comparison or pass was introduced.
No constructor default or complete option-interaction matrix is inferred.

All original sources, catalogs, IDs, predicates and old packet bytes/seals remain
in place. Only the two old canonical pages needed new exact historical copies:
[spec before R4](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/spec-before-r4.md)
and [research before R4](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/research-before-r4.md).
The prior packet manifest is revision3 after a whitespace-only correction while
the prior canonical frontmatter says revision2; R4 preserves both identities.
[Impact identities](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/impact-r4.json)
record exact as-of JSON pointers. Other frozen consumers were not edited or
replayed against changed pages; root owns historical redirection/integration.
Recording RC-020 default-versus-explicit-Off remains a separate Q051 gap.

[Delta](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/delta-r4.json),
[read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/validate-r4.py)
and [R4 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/README-r4.md)
bound the correction. Focused source reading covers the ASD section paragraphs
and SET-B058, both changed actions, all unchanged case records for exact equality,
and prior review identities; it is not a fresh semantic audit of the whole
Managing Files chapter or all downstream owners. All target outcomes remain U.
