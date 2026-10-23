---
id: RESEARCH-BOUNCE-FREEZE-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary target parity unknown
specs: SPEC-BOUNCE-FREEZE-WORKFLOWS
---

# Bounce, Freeze and Flatten evidence

## Question and role

Observed source text identifies distinct commit/freeze workflows. The
[canonical draft](../specs/bounce-freeze-workflows.md) owns their proposed
observable contract; this page owns provenance and interpretation. The
[coverage plan](full-live-specification-plan.md) F-07 and
[coverage design](full-live-specification-design.md) govern partial coverage.
No original function/application, candidate, media renderer, hardware or
latency experiment was executed. This analyst context is not a clean implementer.

## Retained sources

All captures below were retained 2026-10-19. They identify major version only,
not the target patch. Exact URL, final URL, UTC time, size and digest are in the
[source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/sources.json).
Three new bounded official pages are immutable. The existing mixing HTML and
its original routing/monitoring source catalog are pinned in place, not copied
or recaptured. The [pure section parser](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/source_parser.py)
retains normalized paragraph/list/heading text with original HTML lines,
section/anchor and heading context. Its output is derived evidence, not HTML.

- D12-BOUNCE: [manual-12-bounce-to-audio-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-12-bounce-to-audio-2026-10-19.html), 250651 bytes; SHA256 `fb9108ece793e2df9aa478d48905d3adf88c14a4157b0c02ab25e00f8df3b3e0`. [Official source](https://www.ableton.com/en/live-manual/12/bounce-to-audio/).
- D12-RESOURCES: [manual-12-resources-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-12-resources-2026-10-19.html), 258140 bytes; SHA256 `9d875319b2562a484f2de7b859d2a4d1bb3f3ef426605bc33c93a30609f75f23`. [Official source](https://www.ableton.com/en/live-manual/12/computer-audio-resources-and-strategies/).
- D11-RESOURCES: [manual-11-resources-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-11-resources-2026-10-19.html), 235065 bytes; SHA256 `38b0860b418d49bb738b0c5c56197f11803f92a2ed571978f7f77f03ec008889`. [Official source](https://www.ableton.com/en/live-manual/11/computer-audio-resources-and-strategies/).
- D12-MIXING: [manual-12-mixing-2026-10-19.html](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-12-mixing-2026-10-19.html), 276916 bytes; SHA256 `255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e`. [Official source](https://www.ableton.com/en/live-manual/12/mixing/).
- ROUTING-MONITORING-CAPTURE-CATALOG: [sources.json](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/sources.json), 2474 bytes; SHA256 `4963c2a29a07be0ed3c2f49fa8792982ba6badecf9b0c20c64e92f92a9303f03`.

## Current Bounce observations

[bounce:B001–B021](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json)
retain the entire §20 chapter. B006–B010 distinguish track replacement from
separate-track selected-source commit/mute and the two-view scope. B008 places
individual bounce after devices and before mixer, with mixer settings copied
and source devices absent from the new track. That source-stage description
is distinct from Arrangement consolidation and export; no existing sample
comparator transfers automatically. B011/B012 describe naming/color and project
path roles without supplying filename collision, codec or unsaved location laws.

B014–B017 distinguish whole-group replacement from selected group material.
B017 expressly describes group processing post-mixer from Main output, includes
inside-group effects/sends and excludes Main processing. It also excludes tracks
routed outside the group and conditions returns on final output reaching Main.
The phrase does not prove arbitrary nested graph traversal, double-counting,
feedback, solo/monitor policy or other tracks' contribution. Those remain U;
source/group/return/Main baselines must be separately established before any
inclusion/exclusion comparison. A silent bounce cannot prove an exclusion when
the source, return, wet path or output was already silent.

B019–B021 describe copy-once/current-at-paste behavior, the bounded source and
destination contexts, empty MIDI-to-audio conversion and disabled paste after
copied source deletion. Actual clipboard encoding, multiple Session-track copy,
occupied destination replacement, partial deletion and Undo are not established.
The scope is the documented positive list, not an inferred refusal table.

## Freeze and command-version distinction

The reused Mixing capture HTML630 only points to resources #track-freeze;
there is no matching Freeze subsection there. The current official resources
chapter provides [freeze12:B001–B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json),
§38.1.4. It supports track holding-clips eligibility, Group/return/Main exclusion,
Freeze/Unfreeze controls, frozen playback/edit availability, explicitly allowed
clip/mixer/automation/scene/record/consolidate operations, tails, two Session
cycles, drop-area tracks, project/temporary paths and external-device cases.
These availability exceptions do not replace their generic operation owners.
Time-effect edits can differ on unfreeze; no forced mismatch or metric follows.
Two Session cycles supply no rounded sample count or full envelope oracle.

Current Bounce B006 says Bounce Track in Place superseded Freeze and Flatten
Track and Flatten for frozen tracks; current Freeze B007 points to Bounce Track
in Place for committing settings. Freeze itself remains documented. This does
not identify the exact command surface shipped in 12.4.3, so that surface and
legacy Flatten outcome remain U in the draft.

For explicit predecessor context, retained Live 11 §33.1.4
[freeze11:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze11-blocks.json)
describes Edit-menu Flatten replacing original clips/devices with the audible
result. It is D11 context only and cannot be promoted to a D12 or 12.4.3 law.
No standalone combined Freeze and Flatten Track law is supplied by the retained
sections. Max for Live device freezing is unrelated evidence and was not used.

Version wording also differs: Live 11 B002 describes one sample per Session clip
plus one for Arrangement; current Live 12 B002 says one per Session and
Arrangement clip. Preserve both source bytes. The proposed D12 contract states
the latter source's role with exact-target applicability U; no legacy file-count
rule or inferred target storage codec is imported. This is source-version drift,
not an observed target implementation change. Broader applicability belongs to
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

## Hardware, files and lifecycle limits

Current Freeze B005 documents real-time processing for qualifying actual hardware
routes and references real-time render options; the existing export owner keeps
those process-control laws. B019 describes Freeze sample locations and discarding
external-device Freeze files on unfreeze. Neither statement proves hardware
availability, rendered signal/latency or broad file cleanup. B020's absent-device
sharing case requires present generated samples and a positive frozen playback
baseline. It cannot settle missing-media recovery or unfreeze without devices.

No actual ALS, audio/MIDI/Freeze/Bounce files, accepted drivers/ports, external
instruments or effect responses were generated or acquired. Future owned stimulus
and positive-path definitions live in [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/fixtures.json).
If accepted control, eligible nonempty source, enabled processing/nonzero amount,
nonmuted wet return or independently known output cannot be established, a case
stays U. Signal and lifecycle comparators are null; no clock, codec, resampling,
normalization, gain, tail threshold or performance law is guessed.

The [41 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/requirements.json)
contain 36 D12 clauses and five U obligations. The
[77 proposed cases](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/cases.json)
contain 42 visible documentary predicates and 35 null documentary oracles;
all target outcomes remain null/U and unexecuted. Compound clauses and multiple
entrypoint branches remain partial until separately evidenced. Case counts are
not whole-workflow or product completion.

## Review packet and checks

The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manifest-author-r1.json)
seals sources, derivatives, JSON, parser/validator and the two canonical snapshots.
The [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/validate.py)
is read-only: source and payload hashes, original reuse identity, all 59 block
records/line views, requirement/case coverage and nulls, positive prerequisites,
counts, snapshots, links/anchors, exact browser ID equality and authored whitespace.
No validation-result file is rewritten after freeze. Independent semantic review
is required; author checks do not establish source completeness or target behavior.
Figures, linked PDFs/help, native code and runtime probes were not inspected.
Shared index, coverage, question and log integration belongs to the root analyst.
