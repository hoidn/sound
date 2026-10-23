---
id: RESEARCH-MIDI-EDITING-TOOLS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# MIDI editor and MIDI Tools evidence

## Question and canonical ownership

What observable editor operations and tool transformations are documented, and
which can be tied to the pinned 12.4.3 build? This analyst packet feeds
[MIDI editor and tools](../specs/midi-editing-tools.md), a partial FEAT-MIDI-EDIT /
FEAT-MIDI-TOOLS contract. The [full-product inventory](full-live-coverage-inventory.md)
owns the denominator and [execution plan](full-live-specification-plan.md) owns
work status. Root maintains shared indexes/log/coverage; this packet contains no
candidate code or original-code execution.

Existing [note storage](midi-note-storage.md) remains canonical for note fields,
normalization and saved representation. Controller transforms belong to
[MIDI mapping](midi-user-mapping.md). Their facts do not establish editor snapping,
quantization or tool algorithms. Existing storage evidence was consulted before
capturing the two specific missing official chapters.

## Sources and retention

Captured 2026-10-19 from official Live 12 documentation. The publisher provides
no patch/build-specific revision on these pages. D12 means text documented there;
**every exact-target behavior is U**. Source HTML is retained unchanged, derived
text is numbered (whitespace-only lines marked `[blank]`), and images were not inspected. HTML/text may include the global
manual navigation after the chapter body; no navigation text is behavioral evidence.

| Source | URL | Retained exact HTML SHA-256 |
| --- | --- | --- |
| SRC-MIDI-EDIT-EDITING-MIDI | [Editing MIDI](https://www.ableton.com/en/live-manual/12/editing-midi/) | `7675902a8115a7a329c693bbfca3efb360493ece560ed83c754ee8d2a99a5ca2` |
| SRC-MIDI-EDIT-MIDI-TOOLS | [MIDI Tools](https://www.ableton.com/en/live-manual/12/midi-tools/) | `ebe83b52ba7b11ada85691f524f8e817534c604eac1c0edd4aa9c7b9327fd6ab` |
| Existing pinned schema | [inventory/12.0_12402.txt](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt), installed 12.4.3 package, TranslatorNumber 12402 | `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` |
| Existing tool inventory | [inventory/midi-tools.json](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/midi-tools.json), 17 current-manual topics | `79084729fbf8195600e5cfcae43fe8dcdeb92ad279d4d47dcefb447c859ccb2a` |

[Source records](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/sources.json)
contain URLs, capture date, HTML digest and stable heading IDs. The spec appendix
maps E1–E23/T1–T19 to exact text ranges and heading IDs. The
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/manifest.json)
pins all packet payloads and the authored spec/research review snapshot.
The capture script uses the existing BeautifulSoup dependency to derive text;
it installs nothing and refuses to overwrite retained HTML. No evidence follows
from executing its text-extraction code beyond the captured bytes and extraction.

## Observed documentary behavior

The Editing MIDI chapter directly documents selection, insertion, note movement,
length, drawing, stretch and note/time utilities, plus velocity/chance lanes,
probability groups, fold/scale display and Session/Arrangement multi-clip focus.
It distinguishes foreground-only velocity/chance editing from multi-clip note
editing, specifies eight-clip/eight-track limits in their respective views,
and states that editing imported MIDI does not rewrite the source MIDI file.
These observations support REQ-MIDI-EDIT-001–022, not a runtime compatibility pass
(E1–E23 in the canonical spec appendix).

The MIDI Tools chapter describes immediate Auto Apply, restoring original notes
when disabled, deferred Apply, undo/redo of notes without undoing tool parameters,
and parameter-only Reset (T1, text 22–41). These are distinct observable state
operations; exact undo grouping and tool/selection transition baselines remain U.
The tool inventory is twelve transformations and five generators. Each gets
its own bounded contract and authored acceptance case below.

## Per-tool correlation and limits

The schema was parsed statically into
[schema-correlation.json](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/schema-correlation.json):
23 Algorithm classes, consisting of 15 native tool profiles and eight selection
filter profiles. This is observed presence/type metadata, not evidence that an
algorithm executes, accepts a numeric domain or presents any specific UI.
Internal names remain analysis-only. No source-level code is included in the spec.
The two Max tools are inventory-profiled separately and have no native Algorithm
class asserted here; their AMXD bodies were neither inspected nor executed.

| Tool / requirement and case | Current manual locator | Pinned schema locator / useful parameter correlation | Unresolved exact behavior |
| --- | --- | --- | --- |
| Arpeggiate / 027 | T3, `arpeggiate` | `ArpeggiateAlgorithm`, lines 49–56: Rate, Steps, Distance, Gate, Style | Eighteen style algorithms, duration/timing/clipping and random styles |
| Chop / 028 | T4, `chop` | `ChopAlgorithm`, 1093–1133: NumParts, Gaps, Stretch, Pattern.0–15, Emphasize.0–15, Variation | Rounding, minimum duration and variation distribution |
| Connect / 029 | T5, `connect` | `ConnectAlgorithm`, 1439–1445: Tie, Density, Spread, Rate | Polyphonic note pairing, filling/endpoints and random selection |
| Glissando / 030 | T6, `glissando` | `GlissandoAlgorithm`, 2665–2669: CurveStart, CurveShape | Numeric bend curve, target ranges and insufficient-input UI response |
| LFO / 031 | T7, `lfo` | `LfoAlgorithm`, 3730–3743: targets, rate/shape, amplitudes/base, attack/decay | Numerical sampling/waves; Notes-view visibility conflict C3 |
| Ornament / 032 | T8, `ornament` | `OrnamentAlgorithm`, 5901–5912: Flam and Grace Notes settings | Grid rounding, collisions, group/expression carryover |
| Quantize / 033 | T9, `quantize`; E23 | `QuantizeAlgorithm`, 6274–6281: Reference, TripletReference, start/end toggles, Amount | Nearest-line ties, zero durations and shortcut conflict C2 |
| Recombine / 034 | T10, `recombine` | `RecombineAlgorithm`, 6285–6292: dimension, shuffle, mirror, rotate/grid | Simultaneous-note ordering, shuffle random stream |
| Span / 035 | T11, `span` | `SpanAlgorithm`, 7416–7422: mode, chord threshold, variation/offset | Single/coincident notes, chord grouping, variation |
| Strum / 036 | T12, `strum` | `StrumAlgorithm`, 7687–7693: chord threshold, low/high, tension | Chord recognition and exact nonlinear offsets |
| Time Warp / 037 | T13, `time-warp` | `TimeWarpAlgorithm`, 8008–8014: breakpoints, stretch end, preserve range, quantize | Speed integration, interpolation, singular speeds |
| Velocity Shaper / 038 | T14, `velocity-shaper` | Max-tool inventory; no native Algorithm asserted | Envelope sampling, MIDI velocity rounding, Max lifecycle |
| Rhythm / 039 | T15, `rhythm` | `RhythmAlgorithm`, 6553–6567: pattern/length, density, pitch, velocity/accent, shift/duration/split | Pattern enumeration, split randomness, boundaries |
| Seed / 040 | T16, `seed` | `SeedAlgorithm`, 6947–6957: pitch/duration/velocity bounds, density, vertical limit | Density-to-count conversion, random law and seed |
| Shape / 041 | T17, `shape` | `ShapeAlgorithm`, 7025–7035: shape levels/presets, rate, tie, density, pitch bounds/variation | Shape sampling, jitter distribution and rounding |
| Stacks / 042 | T18, `stacks` | `StacksAlgorithm`, 7511–7514: Sequence | Chord tables/custom-bank format, voicing and malformed-bank errors |
| Euclidean / 043 | T19, `euclidean` | Max-tool inventory; no native Algorithm asserted | Euclidean pattern phase/distribution, wrap and Max lifecycle |

Native filter-profile presence is retained for Condition, Count, Duration,
Pitch, Probability, Scale, Time and Velocity in the same correlation artifact.
The eight names align with E4's documented filter families, but parameter presence
does not determine Boolean composition, equality bounds or actual matching.
The original schema bytes and inventory manifest own build provenance; this
survey does not relabel current documentation as exact-build evidence.

## Contradictions, inference and unknowns

Three source contradictions remain explicit in the draft: C1 generator existing
content replacement (intro versus `using-midi-tools`, lines 9–10 versus 36–37);
C2 Ctrl/Cmd+Shift+U settings versus application (Editing MIDI 495–520 versus MIDI
Tools 140–148); C3 LFO pitch-curve Notes-view visibility (MIDI Tools 111–114).
No native presence evidence resolves any of them. MED-050–052 carry U outcomes.
Root can retain these under
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

Inferred: matching native class/field names make these sensible exact-build
investigation targets. They do not prove a user transition, default, accepted
range, boundary, ordering or output formula. No unsupported formula for RNG,
quantization, speed curves, chords or audio is proposed. Cases compare bounded
D12 invariants where exact algorithms are absent; all target comparisons stay U.

The canonical spec lists its detailed algorithm/lifecycle gaps. Additional F-04
owners remain required for full MPE editing/input/output, tuning, groove,
conversion, MIDI interchange and general Clip View state. Current availability
of third-party Max content does not define Live's tool ABI. Amp/Cabinet emulation
and candidate-workspace provisioning are outside this analyst packet and retain
the user's existing deferrals.

## Review packet and checks

Revision 1 freezes 43 requirements, 57 authored cases (43 D12, 14 U), two official
HTML captures and a static schema correlation; all exact-build grades U.
No ALS fixtures were generated, no tool parameters were inferred from binaries,
and no note/curve/audio result was observed. Independent review must inspect
source identity, each per-tool clause, case comparators, ambiguous documentation,
version applicability, and missing lifecycle/boundary behavior before expanding
scope or publishing any handoff. This remains partial coverage regardless of
whether mechanical checks pass.

Packet validation checks JSON parsing, unique requirement/case IDs and one-to-one
case mapping, 17-tool inventory names, 23 schema classes, source HTML hashes,
heading/text-range locators, local file links, metadata and frozen payload hashes.
Root supplies inbound indexes and shared log/coverage updates after integration.


## R2 Interval case increment

This narrow successor keeps all43requirement rows and57old case records exact,
then appends MED-058–060 for selected-note slider addition, no-selection slider
setting alone and no-selection button application to all original clip notes.
Current total60cases comprises46D12documentary proposals and14U cases; every
actual target result remains null/U/unexecuted. Legacy `expected`/`comparator`
strings describe documentary proposals, not executed outcomes. The added wrapper
status makes that explicit without rewriting old records or claiming old results.

The [bounded retained-source query](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-utility-source-context-query.json)
reads complete Intervals/Humanize subsections and two Clip paragraphs, not all
244MIDI blocks. Intervals§10.5.9.4 HTML588 paragraph2 explicitly differentiates
selected notes from none; existing MIDI011 already owns that source role while
MED011 only tests Fit to Scale. “Immediately” here supplies the documented lack
of a separate button step, not a zero-time guarantee. The negative slider-alone
case requires a genuinely productive matched Add Interval button baseline, then
reset original data and actual no-selection state. Empty/unsupported/failed
prerequisites stayU. No NoteId/count/clipping/codec/scheduler or button-selected
branch is invented. No instrument, media, MIDI output or audio is supplied/run.

MIDI capture records2026-10-19date only; exactUTC remains unknown. QueryUTC is a
separate extraction timestamp. PublicationVersion12 does not establish target
12.4.3 behavior. Humanize quarter-grid before/after versus Clip half-grid remains
Q053; total-span interpretation is a hypothesis. No RNG/source-defect/default or
new numerical law follows. C1/C2/C3 and old generator-nonempty/Chop-gap R1 review
notes remain open. This is not a fresh full43clause/57oldcase semantic rereview.

[Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/acceptance-cases-r2.json),
[source context](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/source-context-r2.json),
[delta](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/delta-r2.json) and
[consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/consumer-impact-r2.json)
keep this scope explicit. All11oldpacket files, including the formerly replaceable
R1 validation report and manifest, remain byte-identical; before-canonical
snapshots preserve original manifest identities. Existing consumers remain as-of;
no old validator or historical consumer runs against changed canonicals and no
automatic adapter is added. Current successor checks verify immutable inputs,
precise case-only delta, source pointers, nulls and normative Browser ID equality.
**AS-OF AUTHOR FREEZE:** independent R2 review pending; use the
[spec index](../specs/index.md) for current disposition. No release or completion.
