---
id: RESEARCH-MEDIA-FILE-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
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
Separate source/scope/predicate review remains required. This is not a complete
file-format or persistence contract.
