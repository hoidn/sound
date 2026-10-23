---
id: RES-BUNDLED-DEVICE-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current-manual applicability unresolved
---

# Broader documented workflows for seven bundled devices

## Canonical scope and method

The [new workflow draft](../specs/bundled-device-workflows.md) owns only the
previously unowned documentary interaction facets selected below. Existing
[bundled parameters](../specs/bundled-device-parameters.md),
[hosting](../specs/bundled-device-hosting.md), and the five individual audio
owners remain authoritative for exact storage, ranges, labels, finite
coefficients, vectors and comparison criteria. The
[coverage design](full-live-specification-design.md) and
[execution plan](full-live-specification-plan.md) govern partial coverage.
No old draft, source, release, implementation or shared catalog was edited.

Observed evidence here is text in public manuals, not a run of Live. D12 has
exact-12.4.3 applicability U for every new runtime clause. Existing finite
extracted-original X outputs do not corroborate another mode, controller,
transition, UI or app host context merely because the device name matches.
The draft’s finite-authority table routes those results without copying or
weakening their laws. New signal or lifecycle outcomes remain ungraded.

## Exact reused sources

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/sources.json)
pins four records: two official manual chapters and their two original capture
catalogs. Original source IDs, URL/capture metadata and exact bytes are retained.
There was no new web fetch or runtime capture.

| Source | Version/capture | Bytes / SHA-256 |
| --- | --- | --- |
| SAMPLE-INSTRUMENTS-MANUAL | [Instrument reference](https://www.ableton.com/en/live-manual/12/live-instrument-reference/); Version 12, captured 2026-10-19T20:27:58.247940+00:00; [retained original](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-instruments-2026-10-19.html) | 618718 / `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a` |
| D12-AUDIO-EFFECTS | [Audio-effect reference](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/); Version 12, captured 2026-10-19; [retained original](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html) | 588328 / `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299` |

The [capture script](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/capture.py)
uses standard-library HTML parsing on those exact bytes only. It retains device
section blocks, original HTML lines/anchors and heading context. Figures and
linked FAQs/tutorials were not inspected, so no figure-only layout or implied
capability is claimed. Public physical-model narrative supplies no required
private implementation, binary structure or platform shim.

| Device | Section / blocks | Newly selected workflow facets |
| --- | --- | --- |
| Analog | §31.1; [analog:B001–B076](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-analog-blocks.json) | Panel/MPE presentation, Shape/LFO eligibility, Quick Routing preservation, Follow control, envelope modes, sync/phase UI, vibrato wheel, unison/glide, MPE destinations |
| Collision | §31.2; [collision:B001–B088](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-collision-blocks.json) | Tabs, model-dependent controls, copy buttons, LFO targets/cross-modulation, MIDI/MPE targets and repeated-note Retrig |
| Corpus | §29.10; [corpus:B001–B049](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-corpus-blocks.json) | Model eligibility, MIDI sidechain/taps, Frequency mode/priority, Off Decay, synchronized LFO eligibility, running-resonance admission and limiter indication |
| Electric | §31.5; [electric:B001–B036](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-electric-blocks.json) | Section-selection gestures and separately presented global/per-note bend ranges |
| Tension | §31.12; [tension:B001–B110](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-tension-blocks.json) | Tabs/shared Volume, exciter labels/eligibility, Gated damper, filter subsection gates, LFO sync, wheel/Error, MPE and portamento/unison |
| Amp | §29.1; [amp:B001–B024](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-amp-blocks.json) | Common model controls, qualitative Gain/Volume/EQ/Presence roles, mono/Dual selector and optional companion placement |
| Cabinet | §29.6; [cabinet:B001–B018](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manual-cabinet-blocks.json) | Separate speaker/placement/mic-type controls, Output/host-mix boundary and multiple-mic rack workflow |

There are **401 retained blocks**. This denominator is the extracted source
context, not 401 fully specified behavior units. Only the selected clauses have
requirements/cases; broader content and compound branches remain open.

## Existing authorities retained unchanged

The [authority pins](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/existing-authority-pins.json)
freeze the consulted seven current spec identities and fifteen manifest/README/
spec identities across five releases. They record scope/identity, not evidence
for new UI or sound claims. The validator also verifies each of those immutable
release manifests’ listed payload hashes without running comparison programs.

- [Analog](../specs/device-analog.md) retains all numerical waveform/filter/
  envelope/priority laws. [device-analog-v1](../../handoff/device-analog-v1/README.md)
  has 38 groups/42 evaluations; arbitrary glide, unison and unrendered modes
  are not added by this packet.
- [Collision](../specs/device-collision.md) retains enabled-resonator/order,
  note/voice and selected signal laws. [device-collision-v1](../../handoff/device-collision-v1/README.md)
  has only two cases; the broader draft and concurrent-edit evidence remain
  untouched. No noise or arbitrary-mode metric is invented.
- [Corpus](../specs/device-corpus.md) retains constant-parameter mixing, models,
  position assumptions and finite modulation results.
  [device-corpus-v1](../../handoff/device-corpus-v1/README.md) covers 24 groups/68
  evaluations; MIDI sidechain and app routing remain separate unknowns.
- [Electric](../specs/device-electric.md) retains component, pitch/Stretch,
  global-bend and voice laws. [device-electric-v2](../../handoff/device-electric-v2/README.md)
  has 117 evaluations; a global-bend result is not a per-note-bend result.
- [Tension](../specs/device-tension.md) retains component/voice results and
  render-defined modulation. [device-tension-v1](../../handoff/device-tension-v1/README.md)
  covers 27 finite cases, not arbitrary controller or portamento behavior.
- [Bundled parameter labels](../specs/bundled-device-parameters.md#req-bundled-device-parameters-014--enumeration-labels)
  keep their existing mappings, including the corrected Cabinet microphone
  labels. [Hosting](../specs/bundled-device-hosting.md) keeps conditional
  Amp/Cabinet composition with supplied wet audio; no wet signal is produced.

No archived comparator, audio fixture or original binary was executed. Hash
checks establish retention only, not candidate or application compatibility.

## Source-context cautions

Observed in Analog analog:B064–B065: Quick Routing describes four shortcut
layouts and preservation of oscillator level/tuning/waveform. The new clause
covers the gesture and exposed state; it neither copies the numeric routing
coefficients nor claims an atomic update or running-tail preservation. The
existing Analog REQ021/023 gaps still own numerical glide/unison and controller
results. Source envelope modes and synchronized controls do not close them.

Observed in Collision collision:B040: copy buttons act on resonator settings.
No tail buffer or global/MPE routing copy is established. The chapter’s serial
paragraph B075 uses “both resonators” as its source wording, and its Tube text
B037 describes closed ends while B052 refers to a permanently open end. These
wordings are not adopted as new topology/physical-model requirements. The
existing Collision REQ003/014 authorities and unresolved mode limits remain in
place; no editorial repair, Corpus/Collision model equivalence or hidden graph
is inferred from the manual. A source-context question is required before any
new physical or serial-signal claim uses those passages.

Observed in Corpus corpus:B043 and B045–B049: changing Dry/Wet is described as
input admission around already sounding resonance, and MIDI sidechain controls
have separate Frequency and Off Decay roles. These give new finite investigation
questions, not a replacement for Corpus REQ004’s constant-parameter law, REQ012’s
retained transitions or REQ013’s unresolved MIDI path. Note priorities, Note Off
endpoints and limiter words supply no new timing, threshold, note aggregation,
sustain-pedal or sample-equality criterion. A positive old tail and a distinct
new stimulus are both needed; a silent/dry-only path cannot prove admission.

Observed in Electric electric:B036: global and per-note bend ranges are separate.
The prior X global-bend result does not establish per-note delivery or isolation.
Electric’s public Stretch narrative (B035) is not promoted to a new tuning law;
its finite pitch/Stretch observations remain with the current owner.

Observed in Tension tension:B006, B014, B042, B078–B092: panel, control eligibility
and controller destinations are documentary facets separate from component DSP.
The source warns that parameter combinations can be silent or very loud
(B035/B108); silence from an unproductive exciter/string path is inconclusive.
New Priority/voice formulas are not copied from the manual: Tension REQ014’s
finite voice result and open mono-priority context remain authoritative.

Observed in Amp/Cabinet amp:B015 and cabinet:B006: mono/Dual are described
controls and doubled-CPU language is supplied. CPU language remains context
with no calibrated load or benchmark. Cabinet placement/mic-type roles do not
redefine its stored enumeration labels, and rack duplication is owned by the
rack workflow. No virtual microphone, circuit, host or DSP implementation is
mandated by the public physical-model story.

## Authored definitions and remaining gaps

The draft contains **55 requirements: 41 D12 and 14 U**. Its
[118 case definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/cases.json)
contain **33 visible control/state documentary proposals and 85 null documentary
oracles**: eight signal obligations plus eleven required unknown probes per
device. Every target expected/comparison value is null, grade U and unexecuted.
No new D/S/X runtime outcome or broadened finite release is claimed.

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/fixtures.json)
are finite future owned audio/note setups with accepted nonzero source, output,
processing/base/depth/wet and paired positive controls. They retain distinct
per-note versus global expression and prior-tail versus new-excitation context.
No WAV, MIDI, ALS, hardware baseline or captured wet response is supplied here.
Default loading, exact domains, engine codecs, MPE/tuning composition, random
laws, numerical transitions, copy/state transactions, malformed/UI admission,
automation, undo/cancel, persistence, transport/rate and teardown remain required
unknowns. Existing finite owners are linked rather than duplicated.

The **Amp/Cabinet execution route remains blocked**. This work creates no fake
Live identity, CoreFoundation/Objective-C host, shim, emulator or original code
probe and performs no native/runtime/audio execution or installation. Qualifying
wet input/output is an unproven future prerequisite, not an assertion that a
blocked route is feasible. T1.6 and clean implementation are not advanced.

## Freeze and validation

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/manifest-author-r1.json)
pins sources, exact blocks, source/authority identities, requirement/case/fixture
catalogs, canonical snapshots, capture/validation scripts and the
[validation result](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/validation-author-r1.json).
The [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/bundled-workflows/validate.py)
checks the existing requirements browser discovers exactly all 55 normative IDs,
source/authority/release pins, block derivations, catalog/count/oracle/coverage
consistency, links/anchors, snapshots and authored untracked-aware whitespace.
Run with Python 3 -B; no bytecode or source artifact mutation is needed.

These are author integrity checks; independent semantic review remains separate.
No tool installation, release, publication or commit occurred. Root integrates
shared indexes, coverage, questions, execution plan and append-only log. No
whole-device or whole-product completion or compatibility follows from this packet.
