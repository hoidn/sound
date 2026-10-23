---
id: RESEARCH-LIVE-API-SPECIALIZED-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public API applicability U
---

# Specialized device API source contexts

The [partial draft](../specs/live-api-specialized-devices.md) follows the
[coverage design](full-live-specification-design.md) and [plan](full-live-specification-plan.md).
Root read all retained text blocks for the14 specialized references. Immutable
R1 API sources were reused without recapture; no source example/API/Max/native/
audio/hardware/candidate operation was executed. The source index explicitly
names12.4.5; target12.4.3 applicability/outcomes remain U.

## Exact denominator and evidence

Fourteen entries/108 direct declarations: Compressor4,Drift29,DrumCell1,Eq8three,
Eq8.View1,HybridReverb8,Looper16,Max7,Meld4,Plugin3,Roar3,Shifter2,
SpectralResonator7,Wavetable20. All108 map to partial documentary roles/cases,
zero semantically complete. Five U groups add15 probes, giving113 requirements/
123 future cases; all actual message/numeric/signal/timing documentary/target
outputs/comparators null. The other31 entries/480declarations and all inherited
surface retain their separate owners or unresolved obligations.

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/sources.json),
[blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/source-blocks.json),
[member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/member-ledger.json),
[requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/cases.json)
retain the exact source body/declaration/access/locators, explicit argument/result
paragraphs and missing-signature caveats. A null formal declaration never means
zero arguments or void. Existing source/workflow/finite owners are independently
pinned; source-family canonical and all R1 inventory bytes remain unchanged.

## Source-context questions

- LAS-U-ROUTING: Compressor input_routing_type refers to track availability despite
  its own compressor list. Preserve object context; no dictionary/identifier repair.
- LAS-U-SIGNATURE: Wavetable set_modulation_value lists only target/source indices
  while describing an amount setter. No third argument or amount type is invented.
  Four wavetable selector headings omit type; oscillator2 effect mode omits enum.
- LAS-U-UNITS: Looper buffer length and tempo, Shifter/Spectral bend ranges and
  normalized DrumCell gain omit complete units/ranges or maps. Drift's explicit
  semitones do not populate other members by analogy; seconds for Hybrid IR
  attack/decay and0..1size are source-specific, not DSP formulas.
- LAS-U-IDENTITY: DrumCell identifies Drum Sampler by source description, not an
  invented alias hierarchy. Roar introduction repeats Roar Device as parent;
  inherited Device/View closure remains separately unresolved.
- LAS-U-CONTEXT: lists/categories/preset/matrix/bank dependencies and indices need
  independently accepted values/context. Max bank index -1 Best-of and empty
  parameter slot -1 are distinct roles, never LOM/storage identities. Looper export
  requires empty slot/non-frozen audio track/engine on/actual fixed content and
  not recording; source etcetera means the list is not an exhaustive gate.

No enum/code/default/type not explicitly in the member is transferred from its
sibling, instrument GUI, native storage or numerical spec. Voice counts/indexes,
modulation routing, pitch, IR envelope, oversampling and normalized values do not
specify their synthesis/filtering/processing algorithms. Private mechanisms and
implementation designs are not adopted from source descriptions.

## Author freeze and review

[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/manifest-author-r1.json)
freezes exact data/prose/snapshots and read-only validator. Validation checks
unchanged inventory/source/owner pins,108 exact direct mappings,113 browser IDs,
123 null cases, source spans/snapshots/links/whitespace. Independent semantic
review is pending; integrity or counts cannot close any profile or API surface.
