---
id: RES-SYNTHESIS-INSTRUMENTS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3
---

# Five synthesis and drum instrument profiles

## Authority and bounded investigation

This is the F-06 analyst owner for Drift, Drum Sampler, Meld, Operator and
Wavetable. The [canonical draft](../specs/synthesis-instruments.md) owns behavior;
this page owns evidence interpretation and limitations. Read the
[inventory](full-live-coverage-inventory.md) and
[coverage design](full-live-specification-design.md) for the denominator and
closure rule. None of the five profiles is complete or released.

The existing manual/schema capture from [sample instruments](sample-instruments.md)
was reused, with exact hashes checked; no new fetch or original execution was
needed. The previous author had already retained five inventory-selected shipped
presets, decompressed XML and schema/preset observations. This continuation
preserves those captures and adds finite documentary requirements/cases,
paragraph locators, canonical snapshots and author validation.

## Sources and observations

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/sources.json) contains seven pins: the external
Version 12 instrument HTML captured 2026-10-19T20:27:58.247940+00:00, the external
installed `12.0_12402` schema, and five copied Core Library defaults. The manual
SHA-256 is `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`;
the schema is `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Manual patch parity remains U. The preset roots/fields are directly observed,
not reader/writer execution or a map of constructor defaults. Preset headers say
Live 12.4d1, not 12.4.3. Their package presence remains valid exact-build evidence
of supplied resources while their loading, semantics and DSP remain unproven.

| Device | Observed preset root | Manual section | Schema line | Retained paragraphs/headings |
| --- | --- | --- | --- | --- |
| Drift | `/Ableton/Drift` | §31.3 | 1737 | 95 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drift-blocks.json) |
| Drum Sampler | `/Ableton/DrumCell` | §31.4 | 1909 | 54 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drum-sampler-blocks.json) |
| Meld | `/Ableton/InstrumentMeld` | §31.8 | 3374 | 96 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-meld-blocks.json) |
| Operator | `/Ableton/Operator` | §31.9 | 5640 | 211 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-operator-blocks.json) |
| Wavetable | `/Ableton/InstrumentVector` | §31.13 | 3532 | 111 [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-wavetable-blocks.json) |

[Schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/schema-fields.json) and
[preset observations](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/preset-observations.json) preserve the exact
association. No field spelling establishes an enum, default, clamp, automation
eligibility, signal path or sound. Figures were not inspected separately.

## Source ambiguities and interpretation limits

**Operator restart — unresolved context.** The manual overview §31.9.4
`operator:B039–B041` describes Loop retrigger and restart from current level to
peak to avoid clicks. The complete parameter list §31.9.10.7
`operator:B197–B199` distinguishes general Loop/Beat/Sync, current-to-peak in the
Beat/Sync Repeat entry, and sustain-to-initial movement in Loop Time. These may
refer to distinct modes or phases. No contradiction is declared without matching
mode and preconditions; no prose is silently discarded. SYN-U-OP-LOOP / case
SYN-OP-012 retains distinct Loop/Beat/Sync setups with nonzero Initial/Sustain,
Attack and Loop Time, running/stopped clocks and unknown expected outputs.

**Meld count — unresolved version/context.** §31.8.2 `meld:B009` says twenty-four
types and six scale-aware types. §31.8.3 `meld:B012–B033` names twenty-five macro
types when all four Swarms and Chord are counted. The draft retains the named
macro controls and Chord's documentary scale behavior, but assigns no exact menu
count. The six-type scale-aware list at §31.8.8 `B060` does not include Chord;
this can be a different scale context, so Chord is not silently inserted into it.
SYN-U-ME-TYPES keeps the uncertainty visible. A version-matched UI enumeration or
bounded package mapping is needed to establish available type identities.

**Meld sign wording — target unspecified.** §31.8.6 `meld:B047` describes signed
matrix changes and faster/slower modulators without fixing the target/unit.
SYN-U-ME-TIME / SYN-ME-024 keeps this as a signal obligation and does not turn it
into a universal modulation law. Wavetable's explicitly documented additive and
multiplicative rules are not transferred to Meld or other instruments.

## Finite author packet

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/cases.json)
and [stimulus recipes](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/stimulus-recipes.json) separate documentary
expectations from all-null exact-target results. Every requirement has source
blocks and a finite action, or is an explicit U lifecycle obligation with ten
concrete per-device cases. No omitted negative/malformed/cancel/teardown behavior
is labelled inapplicable. Effect/no-effect tests require active sections, routes,
nonzero depth/gain, valid notes/media and an audible paired positive baseline.
Media setups require future retained owned WAV/AIFF/AMS bytes; they are not
provided reference outputs. The extractor only parses pinned HTML; author tools
write analyst docs/catalogs and assert structural relationships.

| Device | D12 / U requirements | Cases |
| --- | --- | --- |
| Drift | 17 / 1 | 27 |
| Drum Sampler | 18 / 1 | 28 |
| Meld | 24 / 1 | 34 |
| Operator | 23 / 1 | 33 |
| Wavetable | 22 / 1 | 32 |

Total **109 requirements / 154 cases**, no S/X expectations, no executions and no candidate grades.

Required unknowns include exact 12.4.3 parity, audio curves/kernels/phase,
frequency and bend/tuning codecs, rate/block behavior, RNG/statistics, voice
stealing/stacking budgets, media/import failure semantics, automation/history,
state persistence/migration, cancellation, teardown, accessibility and CPU
performance. These prevent complete-draft or whole-profile closure. Existing
finite device handoffs and T1 are unaffected; Amp/Cabinet emulation remains
outside this packet and no restricted implementation workspace is claimed.

## Freeze and review

[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manifest-author-r2.json) freezes packet bytes,
external source pins and exact canonical page snapshots. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/validate-r2.py`
for the focused identity/catalog/link/frontmatter/whitespace checks. The retained
[author validation](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/validation-author-r2.json) reports actual scope;
a pass establishes structural consistency only. Root owns the shared index,
coverage, questions, plan and append-only log integration. Separate analyst
review is required before any reviewed-contract claim or sanitized handoff.

## Revision 2 discoverability correction

The existing 5 U lifecycle requirements now use requirement headings so the
existing requirements browser discovers all 109 IDs. Their IDs, U classification,
body text, 109 requirement records and 154 case records are unchanged. The
[original r1 seal and payloads](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/archive-r1/manifest-author-r1.json)
remain byte-for-byte preserved. The [narrow response](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/response-author-r2.json)
and [revision tool](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/revise-r2.py)
record this presentation-only change. Earlier independent semantic review retains
its prior partial scope; no runtime, whole-profile or compatibility claim expands.

## Revision 3 source-qualified action adoption

The independently reviewed full source audit and its focused Operator
association correction support the bounded current owner successor. The
[source R2 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synthesis-instruments-source-audit-r2-review.json)
approves the25literal association fields, not new target outcomes. Source
retention is Version12, captured2026-10-19T20:27:58.247940+00:00, exact12.4.3U.
The full source read covers567 selected texts and112 literal resources; pixels
and link destinations remain uninspected. This owner read carries the previous
full source authoring and rechecks the37proposals/corrected associations.

The successor appends OP024 and36all-null future action histories; all81old
files/109old requirement objects/154old case objects remain exact. G19 refines
the explicit current-version positive overlay only. Current ME003 source
qualification is semitone indicator st->sd only; it does not adopt Octaves/Cents
unit changes. Operator FilterDrive and continuousMorph associate OP015/G25;
ShaperDrive/wet bypass remains OP017 and a distinct source context. General
Loop current-to-Peak versus LoopTime Sustain-to-Initial and Beat/Sync contexts
stay unresolved, with no selected restart law. Meld24/25, six scale-aware
oscillators versus Chord, signed matrix units and Wavetable arithmetic stay
scoped/unknown. No private DSP, RNG, phase, codec, clock, performance, default,
import fidelity, voice allocation, lifecycle or numeric law is adopted.

The current [adoption ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/adoption-r3.json)
retains all37groups as partial, with direct source quotes and dereferenceable
old requirement/actual-action pointers. G12 selects two macro types only; G20
leaves generic InfoView hover unadopted. The [consumer census](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/consumer-pins-r3.json)
is as-of provenance only; no old tool, replay, adapter or live historical gate
runs. No new assets/reference execution/output are provided. Current owner
review is separately pending; source-audit authorship is disclosed and is not
selfapproval or completion.
## Five-profile synthesis family map — pending review, 2026-10-20

The [bounded family map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-synthesis-instruments-routes-v1/structure.md)
extends approved1a/1b I07/I08 and Playback/Mix/Automation/sample cuts for currentR3
Drift,DrumSampler(DrumCell),Meld(InstrumentMeld),Operator and
Wavetable(InstrumentVector). It freshly reads all110 whole clauses and190 case
action/control/limit contexts. Full567-block source semantics remain inherited
from corrected SourceR2;567 raw-span/line/column and354 current-case source-reference
joins are mechanical geometry only.

Root approved32 primary metadata tables/124selected slots/50lexical stores,
153aliases+22memberships and115one-hop source entries with246direct+37empty-target
indirect rows. Fourteen large prefixes retain leading3 construction/lifetime
entries only;18small prefixes retain whole exported prefixes, including ALL8
typed Wavetable oscillator specializations/6slots each. These are metadata
associations, not actual processors, algorithms, native extents, ABI, voice
ownership, defaults or public delivery. Thirty-eight extra store-only entries
remain unfollowed. Twelve Operator-only named-wrapper matches are a bounded
selector result, not absence of other profiles' functions.

The ledger has585 required predicate/context units:390 D12 annotations and195
required lifecycle unknowns, all no-established-route/targetU. These inventory
units are not requirement/case counts, grades or a whole-product denominator.
All190actual results remain null/U/unexecuted. No C/native/image/provider/
decoder/original/harness/model/comparator execution or callee/global/slot
expansion occurred. No complete callable math/X leaf or legal input/oracle is
established. Actual instance/control/note/media/voice and output-to-mix/host
joins, Operator restart contexts, Meld count/scale/sign ambiguities and EACH/
BOTH productive guards remain explicit. No owner/case/release/grade/site or
successor selected; requiredunsupportedU/coverageOPEN/no documentary fallback.
Root sealing, independent review and canonical/shared adoption remain separate.


## Synthesis family route review approval — 2026-10-20

Root read and adopts the complete [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-synthesis-instruments-routes-v1-review.json),
39,420 bytes, SHA256
`1a576e5de16b10c39a1d5c9540a67b30070b46454ef90391f40c7dc1e2690b3e`.
A truncated middle was separately reread in full. There are no blocking findings.
SYNTH-REVIEW-NOTE-001 records that the mutable plan changed after its as-of pin;
that pin is explicitly nongating and requires no rollback or frozen rewrite.
The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/family-synthesis-instruments-routes-v1/manifest.json),
SHA256 `e775f88a88478e15a12080c9ce54019b56bf3d3a8a0e17586a785930130fae7c`,
seals 22 payloads / 3,286,651 bytes. The exact pending proposal immediately above
is author history, qualified by this approval. The entire 10,709-byte prior
canonical prefix and 2,152-byte proposal remain exact.

Fresh review covered all 110 complete clauses and all 190 action/control/limit
histories, 390 documentary predicates and 39 lifecycle definitions expanded to
195 profile instances. All 585 route units remain unsupported / U (zero X or S),
all 190 actuals null / U. The 567 source geometries and 354 embedded quote
occurrences (343 pointers) were mechanically checked; full source semantics remain
inherited from Source R2. Twenty-six immutable pins and all 27 checker negative
controls passed. Original metadata-stream custody remains inherited.

The exact 664-row metadata scope retains 32 tables / 124 slots / 50 stores,
153 aliases plus 22 memberships, 115 call seeds and 246 direct / 37 unresolved
indirect rows. All eight typed Wavetable prefixes stay separate; 38 store-only
entries remain unfollowed. Operator restart contexts, Meld count/scale/sign and
unit ambiguities, productive EACH/BOTH/nonempty prerequisites, actual media,
voice, control/clock/output and lifecycle joins stay unknown. There is no complete
callable math leaf, legal X recipe, new source/native/provider/original execution,
site, grade, owner, case, release or automatic successor. Unsupported required
behavior keeps family and whole-product coverage OPEN.


# Unapplied append proposal: Synthesis research

Proposed destination: `wiki/research/synthesis-instruments.md`.
Root owns review, adoption, indexes, log and coverage edits. This file changes
no canonical page and selects no successor.

## Complete eight-prefix Wavetable source frontier

Following the independently reviewed Synthesis route inventory, Root selected
all 48 entries from the complete six-slot prefixes of the eight exact typed
Wavetable candidates for a metadata census, then separately selected all 48
source bodies. The retained packet is
`analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-typed-prefix-source-frontier-v1/structure.md`.
The frozen census found 296,613 UTF-8 C bytes / 8,116 lines, maximum 830 lines
per record, with 18 warning records and no missing selected entry. Subsequent
retention acquired exactly 48 raw ranges / 324,282 bytes. All selected bodies
and warnings were read; repeated variants use disclosed lossless line reuse,
not only representative functions or processing-like slots.

Observed decompiler operations provide coherent local setup/update frontiers:
eight return-only bodies, eight shallow warned delete wrappers, eight input
value/coefficient updates, eight helper-backed phase/state wrappers, eight
mode/count/array setup bodies, and eight increment-like updates. Phasor,
FM, ClassicPd, ModernPd and interpolation type encodings remain distinct.
These descriptions infer local purpose from source operations; they establish
no formal class/constructor, actual receiver or public runtime identity.

Global-overlap warnings, incomplete powf/cast/FP representation, unretained
helper/global/table dependencies and FM variant/nonreturn paths prevent a
closed callable math/X leaf or public oscillator result. Eight delete aliases/
thunks and four-byte extent metadata do not prove a complete native destructor,
deallocator or lifecycle operation. No warning, rendered name, NaN/tag expression
or control-flow edge was repaired. The packet includes exact anchors and open
setup/dependency assessments; no encountered dependency was followed.

Current voice/media/control admission, phase/clock/rate ownership, ABI/legal
inputs, actual output consumer and independent expected result remain unknown.
No native/image/provider/original/model/comparator/harness execution, new
behavior grade, instruction-site resolution, case, release or successor is
adopted. The existing 110 clauses / 190 actual-U cases / 585 predicate inventory
is unchanged (0 X / 0 S / 585 no established route). Required unsupported
remains U and whole-Live coverage remains OPEN; documentary/source inventory
completion is not a fallback success.


## Wavetable whole48 source review approval — 2026-10-20

Root read and adopts the complete [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-typed-prefix-source-v1-review.json),
53,020 bytes, SHA256
`2d82e657b8f0150f797c6da3b7d071b162a0b2a1b46b06c8434274e6074545f7`,
with no findings. Both untruncated halves were read. The exact pending proposal
above remains author history, qualified by this approval. The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-typed-prefix-source-frontier-v1/manifest.json)
SHA256 `b1d9fd55186b245adb7734c7d96b3461cdd44e7b6c3e180ea43ecb9a1b6d3e43`
seals 13 payloads / 718,687 bytes. All48 raw records /324,282bytes retain the
complete six-slot prefixes of eight typed candidates:296,613Cbytes /8,116lines.
Fresh review covered19complete bodies/2,270lines and29lossless variants with
452changed/5,394exactly shared lines, all116claim anchors and eight six-slot
joins. All31author and14independent negative controls passed. Original chunk
custody is inherited; no original index/native/image/provider or callee reads.

All18warning records remain:20warning occurrences comprise eight unknown
calling-convention, eight overlapping-global and four nonreturn warnings.
Return-only slot0/four-byte extent metadata does not prove destructor or
lifecycle behavior; slot1delete wrappers do not close deallocator/callee effects.
Slot2literal `(float)((int)value << 0x17)` is not repaired into an IEEE bit cast,
exp2 or public semitone law. Slot3phase/helper updates and unbound table virtual
`+0x28` do not establish audio samples. Slot4mode/count/parity/array setup and
slot5increment-like updates retain powf/packed-cast/global/denominator/helper
and receiver constraints. Numeric mode values are not public Unison mapping.
FM setup unsigned-tag `== 0xffffffff` and increment float-looking `== -NAN`
remain decompiler expressions, not a repaired native CFG, NaN test or failure law.

No complete callable math/X leaf is established. Actual voice/count/lifetime,
legal receiver/ABI/helper/table/media/control inputs, phase/clock/rate ownership,
FP behavior and audio consumer remain unknown. The source review adds no native
site, public route, case, grade, owner, release or automatic successor. Existing
110clauses/190actualU/585unsupported route units are unchanged. Unsupported
required behavior stays U and whole-product coverage OPEN.


# Unapplied synthesis research append proposal

Destination `wiki/research/synthesis-instruments.md`; Root owns review/adoption.

## Complete remaining67 Synthesis source frontier — 2026-10-20 (pending review)

After the whole48Wavetable source packet, Root selected a metadata census for
all67remaining entries of the approved115seed Synthesis frontier, then separately
selected all67source records. The packet at
`analysis/ableton-live-12.4.3/full-spec-v1/depth-synthesis-remaining67-source-frontier-v1/README.md`
preserves its metadata stage and exact source approval separately. Census found
all67aliases/exports,29,288C bytes/1,231lines,max145lines,13warning records with
20occurrences and15marked thunks. Source retention read67exact raw ranges once,
58,352bytes;23chunk/4,030,080byte custody remains inherited from the census.
All67C projections and warnings were freshly read directly, without a subset.

Thirty entries have4Bnative extent metadata. Five false-thunk-flag Operator
wrappers have larger expanded C; all mismatches remain explicit. Recovered
Init/Reset/OnNote/control/voice relations include field writes, opaque helper/
callback dispatch and filter-shaped coefficient fragments, with no native target
body, legal input/ABI/current parameter/voice/clock/audio proof. Cleanup/release
projections and eight breakpoint/nonreturn fragments do not establish complete
lifecycle or observed error behavior. Warning CFG and expressions are not repaired.

The whole set has72anchors/seven bounded claims/five OPEN dependencies and
189lexical C-call expressions, not new resolved native sites or required outcomes.
No complete callable math/X leaf, executable original batch, admitted vector,
calibrated oracle or public runtime route is established. No encountered helper,
global, table, slot destination, native/image/provider/original/model/harness
follow occurred. Existing110clauses/190actualU/585route inventory and Operator/
Meld/FP/productive-source qualifications remain unchanged. Required unsupported
staysU and whole-product coverageOPEN; no documentary fallback, grade/case/release,
canonical edit or automatic successor is adopted by this proposal.


## Remaining67 Synthesis source review approval — 2026-10-20

Root read and adopts the complete [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/synthesis-remaining67-source-v1-review.json),
52,527 bytes, SHA256
`c0f5901d42c0ada0cbe8d1fc21c25f36abcb381aa6b460d9dfcda327aee985df`,
in two untruncated halves, with no findings. The exact pending proposal above
remains author history, qualified by this approval. [Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-synthesis-remaining67-source-frontier-v1/manifest.json)
SHA256 `71fde453c69bd9f03332437bc19377f86ae0bcdf3b8e22baf66104f04c8d3e7a`
seals 21 payloads / 469,922 bytes. All 67 complete C projections / 29,288 bytes /
1,231 lines and 72 anchors were freshly read. Seven bounded claims and five
OPEN frontiers agree with the retained text. The 26 author and 12 independent
negative controls passed; seven metadata-stage files / 154,388 bytes stayed
exact. Original alias/chunk custody and the preceding 567-block source audit
remain inherited, without replay.

All 15 marked thunks, 13 warning records / 20 warning occurrences, 30 four-byte
native extent records and five expanded false-thunk mismatches are preserved.
Expanded Operator Init/Reset/OnNoteOn/OnNoteOff/FilterReset operations are not
attributed to four native bytes or a followed native callee. Four tanf coefficient
expressions in the OnNoteOn projection have no admitted units, input/denominator
state, native filter/ABI or audible consumer. Raw kind values, the local 0.001
comparison, copied scheduler-like words and 0x101 stores establish no public
MIDI codec, enable threshold, rate, voice capacity or filter mode. Cleanup,
delete, sized-release and breakpoint projections establish no full lifecycle,
allocation extent, quiescence or observed failure law.

The 189 lexical references comprise 162 FUN/thunk expressions and 27 indirect
expressions, excluding declarations. This is not every source call or a native
site inventory. All 115 selected Synthesis seed projections have now received
bounded source review across this and the preceding 48-entry packet; this does
not close the classes, table prefixes or product behavior. No complete callable
math/X leaf, ready batch, current control/voice/clock/output route, owner, case,
grade, release, resolved site or automatic successor is established. Existing
110 clauses / 190 actual-U cases / 585 unsupported route units and Operator/Meld
ambiguities remain unchanged. Required unsupported stays U / coverage OPEN.


# Unapplied Wavetable phase-helper source proposal

Proposed owner: wiki/research/synthesis-instruments.md. Root owns adoption.

## Complete Wavetable phase-helper source frontier

The whole17 direct helper-target union across all eight approved phase/update
wrappers has been retained/read:36,647Cbytes/1,239lines, no warning records.
36parent lexical anchors and17exact raw ranges are retained. Eight bank/copy
wrappers, one random-looking update, six phase-distortion/FM projections and
two four-lane lookup math surfaces expose conditional local relationships.
No encountered dependency, global/native/image/provider or original run followed.

The two lookup definitions show explicit third indices and16byte return forms;
callers omit the index and ModernPd usesundefined8 return projections. Literal
integer/float/packed conversions, native registers and validtable/input state
remain unresolved. Conditional16KiB loadgeometry is not current table identity.
Bank allocation/counts, seed/index distribution, phase/rate/control/voice/clock
and actual audio consumer remain unknown. No complete callable X/math leaf,
public route, site/grade/case/release or successor is established. All110clauses/
190actualU/585unsupported routeunits stay unchanged; whole-productOPEN.


## Wavetable phase17 source review approval — 2026-10-20

Root read and adopts the complete [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-phase17-source-v1-review.json),
52,594 bytes, SHA256
`a34c7375e3710280cd17f5d6ecb2dc79f80e8768eb9a690b7c2c25d72890c25e`,
in two untruncated halves, with no findings. The exact pending proposal above
is retained author history, qualified by this approval. [Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-phase17-source-frontier-v1/manifest.json)
SHA256 `e1678dbaf4b3991b34400c45bff3d71cc4e6b74280cc6312e12005c7089fd7df`
seals 17 payloads / 223,238 bytes. All 17 complete bodies / 36,647 C bytes /
1,239 lines and 52 claims were freshly read. The eight parent projections /
36 exact lexical anchors establish the complete selected 17-target union;
41 local lexical dependencies are source navigation, not native sites.
Sixteen author negative controls passed. Independent integer address checks
cover all 1,024 conditional indices per lookup and four invalid premise/mask
controls, without evaluating an original function or FP model.

Eight bank-state/copy wrappers, one random-looking update, six FM/phase-distortion
projections and two four-lane lookup math surfaces stay distinct. Under a valid
base and index 0..1023, the shown lookup loads fit a 16 KiB region, including
wrapped neighbors. This proves conditional address geometry only. ModernPd's
separate float load at table+0x4000 requires an additional valid field beyond
that interval. Neither geometry establishes a currently loaded table/allocation.
The lookup definitions show three arguments and 16-byte returns; source callers
show two arguments, while ModernPd receives undefined8. Native register/packed
lane/cast/FP interpretation remains unknown. The shift/xor helper establishes no
uniform distribution or safe index; one-subtraction updates establish no general
modulo or public phase rule. No expression or calling convention was repaired.

All six setup/native/FP/table/receiver/current control/clock/output frontiers
remain OPEN. No complete callable math/X leaf, expected original result, public
route, site, case, grade or release is established; 110 clauses / 190 actual-U
cases / 585 required route units remain unchanged. Required unsupported stays U.
The [separate Root preparation decision](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-lookup164-root-preparation-selection.json) does not change these source findings.


## Wavetable lookup164 native review approval — 2026-10-20

Root read and adopts the full [independent actual/native review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-lookup164-actual-native-review.json),
40,142 bytes, SHA256
`d651f22119a312ab124fedf80d60ab0c6cb508909f98414b3d9c3ee257b9f81e`,
in three untruncated parts, with no findings. The [actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-lookup-native-v1/manifest.json)
seals 12 payloads / 23,196 bytes. The single static decoder child captured
164 bytes / 41 aligned rows at 03:05:27 UTC, with exit0, no timeout, stderr or
retry, equal 15 recorded before/after identities and zero original calls.
All 41 raw words were independently checked by instruction fields, separately
from decoder ESIL, and contrasted with both complete retained C definitions
(113 lines). All 25 independent controls passed. Full collector source preflight
and readiness preceded the separately recorded actual selection; neither is rerun.

The complete 40-byte and 124-byte normal-flow extents end in RET and contain
no calls, stores or stack accesses. Locally, X0 supplies a load base, full X1
supplies the current index and initial V0.s[0] supplies the scalar multiplier.
The result is available in all 128 bits of V0 at return. Loads supply raw bits
used as four binary32 lanes; the C unsigned64-to-float-looking casts are not
native integer conversions. This narrows local ambiguity, without repairing
historical prototypes or the ModernPd eight-byte caller projection.

Both current loads use X0+(X1<<4) with **no current-index mask**. Neighbor
byte offsets use 16*((low32(X1)+delta)&1023), with delta+1 for linear and
-1/+1/+2 for cubic. This bitvector geometry does not establish table length,
accessible storage, lifetime, alignment or caller index/fraction legality.
The current access must not be silently replaced by modulo1024.

The native graph uses ordered binary32 FSUB/FMUL/FADD operations, constants
0.5 and 1.5, and four architecturally fused FMLAs, all using initial lane0.
The review retains the exact operation graph; an algebraically reassociated
polynomial or separately rounded multiply/add is not an equivalent oracle.
FPCR/FPSR, rounding, NaN/subnormal/exception premises remain unknown. No
explicit FPCR instruction does not imply a fixed FP environment or no effects.

These are conditional local native contracts. Caller preparation/result use,
actual tables, x86 equivalence, voice/control/clock/output identity and public
behavior remain open. No new ready-X/math-leaf admission, original numerical
result, behavior grade, owner/case/release or resolved site follows. All 110
clauses / 190 actual-U cases / 585 required route units remain unchanged.
Root separately selected the [whole-eight x86 typed-prefix metadata census](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-x86-typed8-root-metadata-selection.json).
That exact-name/header/48-slot metadata scope selects no native code or runtime
call. Required unsupported stays U and whole-product coverage OPEN.


## Wavetable x86 typed8 metadata review approval — 2026-10-20

Root read and adopts the complete [independent retained-metadata review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-x86-typed8-metadata-v1-review.json),
21,648 bytes, SHA256
`aab60aced2d1bdb94228c982dae0f8f2f10ed5ee754a865ca6dafb6e7e77e729`,
with no findings. The [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-x86-typed8-metadata-v1/manifest.json)
seals 12 payloads / 109,979 bytes from one pinned-image metadata acquisition.
Review covers the entire419line collector/115line checker, all54commands,
5segments/36sections, all21selected raw spans/1,341bytes and eight typed ARM
metadata joins. The 23 preacquisition synthetic, 13 retained-data and 20
independent mutation controls passed; original image custody is recorded,
not independently reacquired by the reviewer.

The result is bounded **REFUSED-U**. Seven exact names satisfy the selected
preceding-NUL + literal + trailing-NUL predicate and lead to seven candidate
typeinfo/header associations. The first selected literal has zero admitted
matches under that predicate. The whole-eight gate withheld every six-slot
prefix: zero prefixes/slots, and no LC_FUNCTION_STARTS payload read. Raw
candidate typeinfo vptr0x10 remains unresolved, not loaded RTTI/provider identity.

Presence of otherwise exact trailing-NUL occurrences with a nonNUL preceding
byte is **unknown**, because v1 did not enumerate them. It proves no class or
implementation absence. Linker string suffix sharing is a distinct unverified
hypothesis, illustrated only by synthetic data. Root separately selected a
[v2 metadata census](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-x86-typed8-root-metadata-selection-v2.json)
using the same exact eight literals with trailing-NUL matching and exact
name-pointer joins. This selects no alternative spelling, native code, runtime
call, ABI, ready-X admission or public behavior grade. Required unsupported
stays U and whole-product coverage OPEN.


## Wavetable x86 typed8 metadata v2 adoption — 2026-10-21

The independently approved [same-eight metadata packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-wavetable-x86-typed8-metadata-v2/manifest.json) resolves all eight exact trailing-NUL names to candidate typeinfo/primary headers and six-slot prefixes (48 distinct target starts). Root adopts the bounded joins by the [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/wavetable-x86-typed8-metadata-v2-review.json), not by repeating its source review. Its 12 payloads total 175,364 bytes. The preceding-NUL predicate in v1 excluded the first real pointer-joined occurrence: VA `0x105f2a850`, preceding byte `0x3e`. No suffix-sharing or linker mechanism is established; v1 remains unchanged as narrower historical evidence.

All 40 selected raw ranges (1,916 bytes), retained headers and selected current/next start locators were reviewed. The full LC_FUNCTION_STARTS payload is not retained in this packet: its global count/hash is a recorded collector result, not a fresh independent full-payload reparse. The acquisition receipt records one attempt, no retry and no error; outer OS exit status/PID are unknown. Raw typeinfo vptr `0x10`, native bodies, current receiver, ABI, table bounds, architecture equivalence and public delivery remain unknown. The 27 author synthetic, 16 retained and 18 independent controls support only this bounded metadata result.

Under [design revision 12](full-live-specification-design.md), this frozen review is finished and the no-X Wavetable depth frontier is parked. No next capture/source packet is selected. Unsupported required behavior remains U; this adds no behavior case, grade or resolved indirect site.
