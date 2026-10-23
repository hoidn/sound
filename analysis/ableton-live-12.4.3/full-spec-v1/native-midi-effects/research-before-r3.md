---
id: RESEARCH-NATIVE-MIDI-EFFECTS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Native MIDI effects evidence

This page supports the canonical [native MIDI effects draft](../specs/native-midi-effects.md)
for Arpeggiator, CC Control, Chord, Note Length, Pitch, Random, Scale and Velocity.
It is an F-06 partial packet under the [full coverage design](full-live-specification-design.md).
These effects process live MIDI; the [MIDI editor/tools page](midi-editing-tools.md)
owns clip rewriting, and [user mapping](midi-user-mapping.md) owns controller
mapping. No observed audio or runtime behavior is claimed here.

## Source identities and retention

Packet root:
[full-spec-v1/native-midi-effects](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/).

| Source ID | Exact source and locator | Observed scope and limit |
| --- | --- | --- |
| SRC-NATIVE-MIDI-MANUAL-20261019 | [Official current Live 12 chapter](https://www.ableton.com/en/live-manual/12/live-midi-effect-reference/); [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manual-12-midi-effects-2026-10-19.html), capture 2026-10-19; 265,958 bytes; SHA-256 `33739cb549d6577624acd91466dafeafe8faaeea03044ac358043233015603a9` | Eight named sections, retained numbered text0003–0142; current Version12, no 12.4.3 publication pin. Text describes behavior (D12); exact build U. Images not inspected |
| SRC-NATIVE-MIDI-SCHEMA-12402 | Retained [schema excerpts](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/schema-excerpts.json); parent [12.0_12402.txt](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt), SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` | Eight exact class blocks with original line numbers; stored vocabulary, not load acceptance, defaults, limits or DSP |
| SRC-NATIVE-MIDI-PRESETS-1243 | Seven retained compressed `.adv` files and decompressed `.xml`; [source paths and hashes](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/shipped-presets.json); [literal observations](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/preset-observations.json) | Product-shipped historical presets declare Creator 12.4d1/MinorVersion 12.0_12402, not freshly saved 12.4.3 state. No CC Control example in inventory. No preset executed |
| SRC-NATIVE-MIDI-ALIASES-ARM64 | Existing arm64 [retained selected symbol rows](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/native-presence.json), external source `/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl`; source and line SHA-256 inside packet | At most three Reset/Exit/OnOn aliases per processor; 15 rows. Presence establishes bounded follow-up anchors only; no function body/call graph/runtime law |

[Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/source.json)
retains the manual URL/date/hash/heading anchors. The [inventory](full-live-coverage-inventory.md)
pins installed product identity and original preset choices. The extractor reads
those retained inventory records, verifies the seven source digests, copies their
original bytes, decompresses XML as data and reads only eight schema blocks.
No original code, bytecode, patch or host was executed; no tooling was installed.

## Observations and implications

The following are **Observed stored fields**, not behavior deductions. Full
original declarations and source line bounds are in the schema packet.

| Device / schema lines | Exact stored surface | Supported implication and boundary |
| --- | --- | --- |
| Arpeggiator 4208–4259 | Mode, PatternOffset, RepeatCount, SyncState, SyncedRate, FreeRate, Gate, Retrigger, Hold, transposition and velocity fields; four compatibility-mode Booleans | Rate/hold/retrigger surfaces corroborated. Compatibility flags make inferred modern behavior for older presets especially unsafe; no flag meaning inferred |
| CC Control 4284–4348 | ModWheel, PitchBend, Pressure, CustomBoolName/Target/Value; 12 indexed custom names, targets and values | Event families/custom controls have storage. No CC wire-range, Send or Learn ordering established |
| Chord 4349–4405 | Six shifts, separate degree shifts, velocities and chances; Strum/Tension/Crescendo; duplicate-strum and per-note-event flags | Current manual's additional Chord controls have installed schema counterparts; no strum schedule or probability distribution established |
| Note Length 4862–4893 | Mode, Latch, SyncState, SyncedLength, TimeLength, Gate, Balance, DecayTime, DecayKeyScale | Latch/dynamic controls present. No mode enum decoding or note-off matching proven |
| Pitch 4901–4939 | Pitch, PitchScaleDegrees, Lowest, Range, RangeMode, UseCurrentScale, StepWidth and mapping keys | Degree/range/step surfaces present. No range inclusion, Fold law or overflow handling proven |
| Random 4940–4968 | Chance, Choices, Scale, Sign, Alternate, UseCurrentScale | Stored field named Scale is not independently proven to encode current Interval labels/range; cycle math remains unsupported |
| Scale 4973–5020 | Base, InternalScale, Transpose, Fold, Lowest, Range, Mapping.0..11 | Twelve mappings stored despite manual's13×13 display description. No extra13th pitch class inferred |
| Velocity 5107–5138 | Drive, Compand, Random, Mode, Operation, MaxOut, MinOut, Range, Lowest | Control surfaces present; neither mode codes nor curve arithmetic established |

Examples of literal values: `Pitch/+12.adv` stores Pitch 12, Lowest 0, Range 127;
`Scale/8-Tone Spanish.adv` stores Range 128 and 12 mapping fields; Note Length's
`16th Notes.adv` stores SyncedLength 5, TimeLength 10000, Gate 100. These do **not**
prove common Range units, a UI division decoder or the active setting behind a
preset name. `Arpeggiator/Bach 16th.adv` stores PatternOffset −1 and RepeatCount 0;
no “−1 means first” or “0 means infinite” law is asserted. The Chord sample has
multiple zero shifts: these do not prove which zero-shift slots are enabled.
The preset case is only byte-level corroboration of parameters, not a behavioral
acceptance oracle.

The retained native names include Arpeggiator Reset/Exit/OnOn, NoteLength
Reset/Exit/OnOn, Random Reset/OnOn and analogous activation hooks. These name
anchors make bypass/reset questions concrete but do not settle held-note output,
random reseeding or the user's actions that reach a reset. No native-law S grade
is justified from this packet.

## Documentary contracts and unresolved readings

The draft assigns 27 stable requirements and 146 concrete cases: 54 documentary
partial predicates and 92 U cases. Every case is unexecuted and all 146 exact-build
grades are U. Cases001–066 cover device behavior; the 80 `-L01`..`-L10` cases
individually cover automation, pitch/overlap boundary, malformed input,
cancellation, undo, bypass, reset/transport, save/reopen, teardown and non-note
forwarding for every device. [Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/case-counts.json)
separate positive 75, boundary 24, cancellation 9, negative 13, teardown 9,
malformed 8 and undo 8. Counts are authored scenario counts, never executed results
or evidence that eight profiles are complete.

Three source ambiguities must remain visible:

1. **Random Alt (text0105–0106).** Choices12/Interval1 is said to cycle C3 through
   C4, suggesting13 positions including the original, whereas Choices2/Interval2
   is said to alternate C3/D3, only2 positions. These are retained in NME-050/051
   with null oracles; no generalized cycle cardinality is approved. D12 Alt's
   Chance0 passthrough and cyclic-order statement remain separable clauses.
2. **Arpeggiator Hold (0025).** Repeat-until-another-key wording coexists with
   adding pitches and toggling them out. NME-010 grades only continuation after
   release without another key; NME-014 leaves replacement/addition when all keys
   are up unknown.
3. **Note Off latch (0084).** The all-keys/pedal-released plus new-note-off wording
   does not supply an unambiguous multi-note transition. NME-038 grades only
   disabled controls; NME-039 probes note/pedal ordering without an invented
   output schedule.

Other material uncertainties: no known channel forwarding, changed-parameter
held-note policy, clamp at MIDI0/127, random seed/distribution, exact rate or
sample placement, unsupported/malformed-input handling, automation event priority,
undo/cancel grouping, save/load emissions or teardown cleanup. S-presence does
not narrow these U cases. Target fidelity remains open even for clear manual
clauses. The draft's prospective acceptance predicates are not observations.

## Capture and validation record

The first capture attempt successfully retained the HTML but stopped when it
encountered CC Control's null preset example. No source bytes were lost. The
extractor was corrected to preserve the existing HTML and record the absent
example explicitly; the resumed capture completed with eight schema classes
and seven preset sources. An initial schema-block endpoint selector included
following classes; it was corrected to stop at each exact closing class tag
before author freeze. These were packet-construction failures, not Live results.

[validate.py](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/validate.py)
checks raw and derived source correspondence, seven preset source hashes/XML,
eight exact schema blocks, numbered text locators, case-ID uniqueness,27 declared
requirement references,146 case grade/oracle coherence, all per-device lifecycle
case kinds, relative links/frontmatter and frozen payload hashes. Its retained
[validation result](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/validation.json)
reports actual checks. Hashes and a lint pass establish packet integrity only.
Root owns shared indexes, coverage, questions and append-only log integration.
The frozen author manifest is review input; a separate review must assess semantic
support before any reviewed-contract or release claim.

## Revision 2 review corrections

The [independent revision 1 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/native-midi-effects-review.json)
requested changes to NME-NL-L01/L05: their Note On Latch setup disabled Length,
which they attempted to edit. M0084 supports that finding. Revision 2 uses
Latch off, Free Length200ms, Gate100%, with Length enabled and an output note
still sounding. Both event outcomes remain U. Lower-priority findings were also
corrected: NME-043/044/045 use a positive accepted UI Range value with unit/end
semantics U; NME-064 compares only output membership in60..127, keeping the
unresolved random-modulation baseline and displacement U. No transfer formula
was added. Counts remain27 requirements,146 cases,54 D12 partial predicates,
92 U and146 exact-build U/unexecuted.

The exact revision 1 manifest and all30 payloads were verified and archived
before edits in [author-r1-snapshot.tar.gz](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/author-r1-snapshot.tar.gz),
SHA-256 `c6967748a7b453dd5d8b4bb336faf42fe417bb3d1bd129e801f5a9e9a0b9864a`.
The original manifest remains unchanged; its historical path entries resolve
against that archive. The [revision 2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manifest-author-r2.json)
pins current payloads, the archive and the original seal.
[Correction dispositions](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/review-corrections-r2.json)
name all three findings. The validator verifies archive contents against the
original seal, checks the corrected case setups/predicate and checks current
payload pins. Source capture bytes are unchanged. Revision 2 is ready for
focused independent review; no runtime or compatibility result follows.
