---
id: RESEARCH-DEVICE-RACKS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Device chains and racks evidence

## Question, route and limits

F-05 asks which rack/chain workflows can be specified from the installed package,
retained native exports and the official manual, without running Live. The
canonical proposed behavioral owner is [SPEC-DEVICE-RACKS](../specs/device-racks.md).
The [full inventory](full-live-coverage-inventory.md) identifies four rack types;
they are part of 102 overlapping device profiles, not a behavior-complete rack
inventory. [ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md)
and the [coverage design](full-live-specification-design.md) require supported
transitions/cases and retain all unknowns.

Read the existing [parameter storage](../specs/bundled-device-parameters.md),
[Set structure](../specs/live-set-structure.md), [device bundles](device-bundles-static.md)
and [parameter mapping](device-parameter-mapping-native.md) before capture.
Their rack parameter binding observation (Channel 16 with a small controller
index and mapping range) remains an observed representation with unresolved
macro-index semantics; current manual prose does not trace that serialization.
This packet does not revise those clauses or expand any existing release.

## Source capture and reproducibility

All paths, sizes, hashes, capture timestamps and source versions are in
[sources.json](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/sources.json).
The retained [capture script](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/capture.py)
uses standard-library HTTP, HTML parsing, gzip/XML reads and JSON filtering.
Reruns reuse captured HTML, preserving its original bytes/timestamp. No package,
original code, Max patch or application was executed; no tool was installed.

| Evidence | Exact identity/locator | What it establishes |
| --- | --- | --- |
| RACKS-MAN-RACKS | [Official rack chapter](https://www.ableton.com/en/live-manual/12/instrument-drum-and-effect-racks/), Version 12, captured 2026-10-19T20:01:50.641719Z; SHA-256 `9b93de0730839152a58dcb843bd74ab0385b6cfa1fb6d58bb28306200ad582fb`; [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-racks-2026-10-19.html), [headings with exact HTML lines](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-racks-headings.json) | Documented chain/zones/macros/drum/pad/extraction interactions; 12.4.3 parity U |
| RACKS-MAN-DEVICES | [Official device chapter](https://www.ableton.com/en/live-manual/12/working-with-instruments-and-effects/), Version 12, captured 2026-10-19T20:01:52.371400Z; SHA-256 `6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82`; [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-devices-2026-10-19.html), [heading records](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manual-devices-headings.json) | Documented common device insertion/move/paste/activator/preset actions; 12.4.3 parity U |
| RACKS-SCHEMA | Installed `Schema/12.0_12402.txt`, 441,285 bytes; SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`; [13-class extraction](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/schema-fields.json) | Exact stored field declarations and source class lines, not runtime or accepted-file semantics |
| RACKS-DEMO | Installed Suite Demo, 3,942,573 bytes; SHA-256 `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b`; [33 rack/branch records](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/shipped-racks.json) | Historical examples shipped in target, Creator 12.4d1; no current save/load observation |
| RACKS-VARIATION-EXAMPLE | Installed `Core Library/Defaults/Slicing/Default.adg`; original [ADG](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/variation-example.adg), [identity and five snapshot excerpts](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/variation-example.json) | Snapshot value/presence representation exists in a shipped file; recall meaning not traced |
| RACKS-NATIVE-STRINGS | Retained arm64 `corpus/indexes/strings.jsonl`, 103,127,314 bytes; SHA-256 `eca2037497cf83b538a48330e974a8d1bf37048a1cf9913345aee4deef8e0f31`; [12 exact line/hash/ref records](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/native-strings.json) | Names and references only; no caller sequence, execution or behavioral proof |

The installed-source identity remains [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md).
The Suite Demo is a different source from the Intro Demo used in the inventory;
its bytes/hash and rack counts must not be substituted for the Intro capture.
The original schema is retained by the existing inventory; this packet stores
excerpts and its hash rather than making a second source revision.

## Observations and interpretation

**Observed, installed schema.** Four rack classes each expose sixteen macros,
visibility state, randomization/snapshot exclusions and variation state. The
ZoneRange class declares Min, Max, CrossfadeMin and CrossfadeMax; ZoneSettings
contains key and velocity ranges. Instrument/MIDI branches reference
ZoneSettings. DrumBranch references BranchInfo of class DrumZoneSettings, which
contains ReceivingNote, SendingNote and ChokeGroup. MacroSnapshot has sixteen
MacroValues and sixteen MacroHasValue fields; MacroVariations holds a snapshot
list. Exact lines and declarations live in the extraction above. These names
are analyst evidence, not a candidate implementation prescription.

**Observed, shipped documents.** The retained Suite Demo has 23 audio-effect,
one MIDI-effect, eight instrument and one drum rack elements (nested elements
count individually). The first instrument and MIDI-effect branch examples
store key bounds 0..127, velocity 1..127, selector 0..0. The demo has no
MacroSnapshot entries. A separately retained slicing default has five. Both
files identify Creator 12.4d1 with MinorVersion 12.0_12402, so they demonstrate
historical shipped representations. They are not fresh 12.4.3 outputs.

**Documented, Version 12.** The official rack chapter provides concrete semantic
rules absent from the schema. The spec separates key/velocity filtering,
selector filtering, velocity versus output-audio fades, and the treatment of
existing tails with/without selector fades. It also distinguishes a pad's note
identity from chain identity, Receive All Notes from a single note, and drum
chain extraction through the Session mixer from extraction through the chain
list. Macro randomization exclusions and variation exclusions are independent
controls. No random distribution or sample-level audio rule is supplied by the
chapter. All runtime clauses therefore retain exact-build applicability U.

**Inferred, deliberately not promoted.** Matching schema/field names and manual
titles suggest that documented workflows concern present surfaces. This is
presence corroboration only. In particular DrumBranch stores a selector range
although the manual says Drum Racks have no zones. That is not a contradiction:
file field presence does not prove an exposed editor or active filter. No Drum
selector semantic was invented from that shared storage.

## Case and claim boundary

The draft contains 28 requirements and [61 authored cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases.json):
3 installed-source assertions, 46 criteria gradeable only in the documented
Version 12 domain, and 12 ungraded U experiments. None ran against Live or a
candidate; all runtime comparisons keep target-build parity U. Cases separate
positive, negative, boundary, malformed, cancellation and teardown scenarios.
Their literal inputs and comparator scope are retained in JSON; the table in
the spec remains the canonical human-readable contract.

Unsupported outcomes include exact fades/summation, note-off/sustain handling,
MPE and simultaneous choke arbitration, macro range interpolation and binding
encoding, random distribution, selector/recall scheduling, latency/CPU behavior,
resource limits, failed-load atomicity, shared-note extraction, nested mapping
preservation, undo grouping, migration and rack-specific malformed-file repair.
A device activator's documented “unprocessed” description is narrowed to a
qualitative audio-effect bypass criterion; the instrument's MIDI-to-audio case
stays U. Esc exits Hot-Swap but is not asserted to roll back a loaded preset.
The current manual's A/B device-state subsection and broader defaults behavior
need separate applicability/ownership work and are not covered here.

## Review packet and downstream work

The first independent review requested two source/fixture corrections, RR-01
and RR-02. Direct parsing of the retained HTML confirmed that multiple mappings
reset the generic macro name independently of the units exception, and that
custom defaults/presets can change initial rack state. REQ-013 and RCK-026 now
separate same-unit/range and different-unit outcomes. REQ-011/RCK-023 require
factory rack creation without custom defaults/presets; REQ-014/RCK-028 require
an unmodified factory Instrument Rack preset without an exclusion override.
Counts remain 28 requirements and 61 cases. The original author seal is retained
as [manifest-author-r1.json](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manifest-author-r1.json);
the current seal includes these corrections and awaits a focused recheck.

[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/manifest.json)
freezes the author packet, including exact page hashes. Independent review must
check claim/source alignment, case counts, platform modifiers and all exclusions.
No rack profile is complete, no release was modified and no host-protocol gap
was closed. The root coordinator owns catalog, coverage, questions and log
integration. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
tracks whole-product evidence/version applicability;
[Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance)
retains host/mapping gaps. Amp/Cabinet host emulation remains blocked and T1.6
remains pending; neither was needed for this read-only documentary packet.
