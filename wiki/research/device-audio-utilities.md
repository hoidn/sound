---
id: RESEARCH-DEVICE-AUDIO-UTILITIES
type: research
status: current
updated: 2026-10-20
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Utility, Tuner and Spectrum evidence

F-06 now has separate canonical behavioral owners for
[Utility](../specs/device-utility.md), [Tuner](../specs/device-tuner.md) and
[Spectrum](../specs/device-spectrum.md). This page owns evidence synthesis,
source identity and limits. The device specs own the contracts. No device is
complete. The bounded original-function capture below is distinct from a whole
application run; no candidate was executed.

Current D03 depth work is the [reviewed owned-state history/public-binding gap](#reviewed-owned-state-history-and-public-binding-gap--2026-10-20).
The sections below retain successive as-of source and preparation findings;
follow the [sole execution plan](full-live-specification-plan.md)
for current selections. Static decoding is distinct from original execution.
The specs remain the owners of application outcome grades.

**D12 exact-target U:** the current official Version 12 manual is documentary
support for the described interface/behavior, not proof of 12.4.3 applicability.
The installed schema and historical presets establish target-package fields and
saved values; they do not promote manual DSP or display clauses to S or X.
There is no numerical audio, pitch, display or timing compatibility oracle here.

## Captures and exact locators

`D12-AUDIO-EFFECTS` is the official
[Live Audio Effect Reference](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
captured 2026-10-19, page title Version 12, no exact publication/build revision.
[Retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html)
is 588,328 bytes, SHA-256
`9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
The [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/sources.json)
records exact URL/path, date, SHA-256 and size for all 24 sources: HTML, schema,
10 Utility presets, 11 Spectrum presets and the Guitar Recording template.
The [capture extractor](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/capture.py)
uses Python standard-library HTTP/HTML/gzip/XML handling and refuses changed
capture overwrites; it runs no original code. Figures were not inspected.

| Source section | Exact retained locator | What it supports |
| --- | --- | --- |
| `#utility`, h2 29.40 | HTML line 2218; [14 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-utility-blocks.json), `utility:B01–B14` | Documentary control relationships and stated domains; no kernel, precision or smoothing |
| `#tuner`, h2 29.39 | HTML line 2134; [21 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-tuner-blocks.json), `tuner:B01–B21` | Documentary monophonic analysis, transparent signal, views/reference/readout; no detection algorithm/tolerance |
| Tuner h3 anchors | `#view-switches` line 2146, `#classic-view` line 2158, `#histogram-view` line 2182, `#note-spellings` line 2194, `#reference-slider` line 2206 | Stable h3 routing in captured HTML; paragraph blocks retain separate start lines |
| `#spectrum`, h2 29.38 | HTML line 2108; [11 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-spectrum-blocks.json), `spectrum:B01–B11` | Documentary analysis/display controls and transparent signal; no FFT, latency, window or dB calibration |
| `PKG-SCHEMA` | [Latest shipped schema](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/12.0_12402.txt): `SpectrumAnalyzer` lines 7476–7510; `StereoGain` 7515–7553; `Tuner` 8236–8267 | Stored field declarations; no constructor defaults, permitted ranges or runtime behavior |

The copied schema is 441,285 bytes, SHA-256
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Its source is the inventory's retained exact copy of installed
`Contents/App-Resources/Schema/12.0_12402.txt`. The inventory's
[device aliases](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/devices.json)
map Utility→StereoGain, Tuner→Tuner, Spectrum→SpectrumAnalyzer by named preset/template
roots plus package directories. The new packet retains the actual compressed
file bytes as well as [parsed values](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/package-values.json).

## Observed target-package state

All 22 retained documents identify Creator `Ableton Live 12.4d1`,
`MinorVersion="12.0_12402"`, revision
`42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. They are historical content shipped
inside 12.4.3, not saves observed from the target application. Parsing succeeded
for all 22; each has one occurrence of the intended device class.

[Schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/schema-fields.json)
retain full class declarations and line numbers. The following selection separates
saved vocabulary from behavioral meaning:

| Device | Exact stored observations | Limit |
| --- | --- | --- |
| Utility | `PhaseInvertL/R`, `ChannelMode`, `StereoWidth`, `MidSideBalance`, `MidSideBalanceOn`, `Mono`, `BassMono`, `BassMonoAudition`, `BassMonoFrequency`, `Balance`, `Gain`, `LegacyGain`, `Mute`, `DcFilter`, `LegacyMode` | Field types include timeable versus remoteable, but do not prove automation UI, live interpolation or coupling |
| Utility presets | `Bass Mono.adv`: BassMono=true, frequency=120, Gain=1. `Left.adv`: ChannelMode=0; `Right.adv`: 2. `Phase Invert.adv`: both phase flags true. `Mid Only.adv`/`Sides Only.adv`: MidSideBalanceOn=true, MidSideBalance=0/2 respectively | Filename/value association is observed; enum map, normalization and actual sound are not |
| Utility historical state | All ten have LegacyMode=false. Difference.adv has Gain=2.61015725 and LegacyGain=8.33333302; other selected presets often have Gain=1 and LegacyGain=0 | No conversion law or migration branch is inferred from these paired values |
| Tuner template | ViewMode=0, TuningFreq/Manual=440, DisplayPitchInHz=false, StrobeMode=false, HistogramCenterNote=0, HistogramNoteRange=3.5, HistogramFollowsPitch=true, AccidentalSpelling=0, IgnoreTuningSystem=false | A saved 440 example corroborates vocabulary, not the documented default constructor or tuning-system behavior |
| Spectrum presets | All eleven have Window=3, AnalyzeOn=true, ChannelMode=2, AutoScaleY=true, ShowMax=true. Length codes seen: 0,1,2,3; ScaleXMode: 0,1,2; NumAverages: 1,2,3,4,6,8; MinRefreshTime: 40,80,100,198,200 | Observed values are not legal domains, units, Block counts, channel enum mapping or timing measurements |
| Spectrum hidden vocabulary | Window, AnalyzeOn and the full retained range/analysis fields appear in the schema | The manual does not establish a user-selectable window control or what Window=3 means |

## Evidence discipline and interactions

[Track mixer values](mixer-values.md) and [mix graph](mix-graph.md) are canonical
for their track/engine scopes. No traced caller path connects their fader curves,
silence floor, pan matrix or ramps to Utility's StereoGain control in this packet.
Reusing their mathematics would therefore invent device signal behavior. The
three new contracts explicitly leave gain/pan/mono normalization, filter response,
control ordering and smoothing unknown.

For Tuner, the manual supplies orientation and readout meaning. It does not give
pitch estimator, note-boundary ties, frequency/amplitude validity range, silence
state, confidence, cent/color thresholds, Hz rounding or acquisition latency.
The target's IgnoreTuningSystem field creates a concrete unresolved interaction
with Set tuning; its name alone supplies no semantics.

For Spectrum, Block/Avg/Refresh descriptions do not prove an FFT implementation,
window family, overlap, zero padding, amplitude normalization, effective latency
or averaging in linear magnitude versus power versus dB. Both-channel combination
and peak-history persistence/reset event details remain unknown. Window=3 is
specifically not a recovered window law.

The [device/rack draft](../specs/device-racks.md) owns generic host actions;
[Set structure](../specs/live-set-structure.md) owns its narrower T1 structure.
Neither makes these devices part of its released device subset. Save/reopen,
malformed state, undo/redo, cancellation, transport, automation, source/device
failure and teardown receive finite U cases in each device packet. Platform
accessibility/permissions remain cross-feature gaps; no figure inspection, binary
search or broad native analysis was performed solely to expand documentation.

## Packet and review boundary

| Device | Requirements | D12 cases, target U | Dpkg file-only cases | U cases | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Utility | 15 | 22 | 3 | 12 | 37 |
| Tuner | 12 | 15 | 1 | 16 | 32 |
| Spectrum | 14 | 19 | 2 | 13 | 34 |
| Total | 41 | 56 | 6 | 41 | 103 |

[Finite signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/fixture-signals.json)
are analyst probe parameters, not generated audio or reference outputs.
[Utility cases](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/utility-cases.json),
[Tuner cases](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/tuner-cases.json)
and [Spectrum cases](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/spectrum-cases.json)
retain requirement IDs, setup/actions/parameters, stated oracle or null, provenance,
comparison scope and unexecuted status. A D12 case is documentary only; a Dpkg
case can confirm retained file contents, never application acceptance or sound.

The [frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r1.json)
pins source/spec/research/fixture bytes for independent review. Root owns shared
index, inventory routing, coverage, questions and append-only log integration.
This packet is a partial draft submitted for independent review; a review cannot
turn unknown numerical/lifecycle behavior into supported behavior.

## Revision 2 source-audit adoption

The independently approved full selected-section audit assessed 46 blocks and 101 qualified judgments, not the complete Audio Effects chapter or all device behavior. [Current R2 catalogs](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/cases-r2.json) preserve all 103 R1 cases verbatim and append nine bounded histories: four Utility, three Tuner, two Spectrum. Current totals: 41 requirement IDs, 112 cases (63 D12 documentary, six historical Dpkg file-only, 43 U); every application outcome remains target U/unexecuted. The original tables/counts above describe R1. No file grade is reexecuted.

Only Utility 005 and 013 append source qualifiers: continuous 0-to-100M controller context, and relevant low/DC content PLUS nonlinear processing AFTER Utility as a necessary, not sufficient, sonic condition. No exact DSP, interpolation, detector, FFT/window-3, color threshold, pixel, CPU or timing law follows. The [nine-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/delta-r2.json) maps actual guarded actions and retained subsets. All nine new documentary/actual expected and comparison fields are null; their source claims do not grade outcomes.

Both Width AND Mid/Side must be genuinely productive before Left/Right no-function contrasts; sustained NONZERO downstream tails precede Mute; DC requires known low/DC plus productive downstream nonlinear processing, without promised audibility. Tuner colors in BOTH views, Classic arrows and in-tune Target require genuinely accepted monophonic contexts, not inferred frequency truth. Independent positive detection precedes unsupported-input absence/negative histories. Spectrum requires actual manual Range AND zoom before Auto, and genuinely visible maximum history before each clear/restart contrast. Both units/views and both display routes remain preserved. Song-restart route and Max double-click interaction stay U.

Selected S06 FAQ states as of Live 12.1 that Tuner's reference follows selected tuning. This remains a separately guarded U probe: IgnoreTuningSystem has a UI action only IF independently found; TUN-015 is external MPE-receiver configuration and gives no Tuner result. The three audit questions, full lifecycle/algorithm gaps and exact 12.4.3 applicability remain open. Source date-only capture has unknown UTC; images and destinations were not inspected.

[Preservation and historical consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/consumer-history-r2.json) retains old exact canonical providers and qualified pointers. They are as-of contexts, not mutable live gates; old validators/reviews remain historical and were not replayed. [R2 manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r2.json) seals current owner evidence/delta. AS-OF AUTHOR FREEZE: independent review pending; current disposition is routed through the shared research/spec indexes. No runtime execution, coverage completion or handoff release.


## D03 Mute membership frontier — 2026-10-20

The [conditional signal trace](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-trace-review.json)
and [model-routing review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-model-routing-review.json)
approve only their local source/association predicates. The later
[seven-body membership query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-membership-frontier-2026-10-20.json)
is unreviewed exploration:2799C-text bytes, exact declaration context, and
40instruction bytes decoded as data. No original function, emulator or Live
application ran. Original image/source hashes and raw locations are retained.

The declaration's offset0x350 is forwarded into descriptor field0x38, with
field0x30=-1. Conditional on successful retrieval of that same descriptor
for the actual modelD, the existing accessor selects D+0x350 and its pointer
at D+0x358. Tiny register checks resolve one metadata-address return and the
base initializer's X0 preservation; the constructor's actual argument setup
remains a separate premise. These are local layout facts, not a proof that
the actual queried Mute member is admitted or bound to the audio processor.

The name-prefix branch depends on a runtime type word at unbacked image
storage. No file word or zero is substituted for it. Thus `mpMute`, a generated
`Mute` name, a `childMute` member and processor Mute are not equated by spelling.
Actual initialized type/name, same-descriptor map/cache/member eligibility,
model identity and callback/current-value delivery remain open. The generic
helper branch stops here without an absence/infeasibility finding. All38Utility
application scenarios remainU; no numerical law, new case, execution route or
complete-profile grade is added. Reuse these exact remaining boundaries.


### Exact type-reference index availability — 2026-10-20

The [bounded index/schema query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-type-reference-frontier-2026-10-20.json)
inspects retained C2 index filenames, samples and exporter schema as data. Those
artifacts cover strings, calls, indirect flow, named vtables and function aliases,
with no general lookup for references to arbitrary data at106e51ba8. No exact
reference query was performed through those indexes; the count remains unknown.
This is a retention limitation, not evidence of no writer, unreachable state
or runtime absence. The actual initialized type, descriptor/map admission and
processor delivery remain open. No new body, original call or grade follows.


### Stopped type/name construction branch — 2026-10-20

Later exact-literal navigation retained six records containing DAT_106e51ba8;
this is separate from the missing general data-reference index above, not a
count of native references or writers. The [initializer query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-type-initializer-frontier-2026-10-20.json)
retains the registration call supplying that storage address, literal
ATimeableBool and declaration-function argument1026eb938. Its selected body
names mpCurrent, mpManual, mpAutomationTarget and mpMidiCCOnOffThresholds.
These are source declarations, not actual initialized values, invocation or
proof that a Mute member is admitted. These later queries remain exploratory,
without independent semantic approval or public behavioral credit.

The [registration-core query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-type-registration-core-frontier-2026-10-20.json)
and [base query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-type-base-frontier-2026-10-20.json)
narrow local construction under actual forwarding, valid-memory and normal
execution premises. The base has an explicit first-four-byte zero store before
its helper call. This does not prove the later/current runtime word, type ID,
public Mute default or membership-prefix branch. The registration argument0xd
is not promoted to a type ID or a proved name-length role. Actual runtime
firstword/type/name/key and same-member/cache admission remain unknown.

The [name query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-type-name-frontier-2026-10-20.json)
and [buffer query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-type-buffer-frame-frontier-2026-10-20.json)
show a conditional returned address16bytes after its header and a two-byte
terminator-shaped write in the source projection. Actual aliases, count/encoding,
unread-helper writes and later initialization remain unresolved. They do not
prove survival of the earlier zero or the actual member key. This generic
name/buffer branch is stopped, without a no-writer or infeasible-route finding.

The [private synthesis proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-type-name-synthesis-proposal-2026-10-20.json)
provides20exact source-pointer citations and remaining-unknown mappings.
Root checked those pointers and read seven source bodies in six selected
queries, including both initializer/declaration bodies; this is not original execution or
independent approval of runtime behavior. The useful next boundary returns to
actual AStereoGain-specific descriptor/member/cache admission and parameter-unit
delivery to the separately registered processor callback. Source names alone
do not equate mpMute, generated Mute, childMute and processor Mute. All38Utility
application scenarios remain unknown; no normative case, numerical law,
execution route or complete-profile credit is added.


### Specific enrollment callback and metadata getter — 2026-10-20

The [exact callback-word query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-enrollment-callback-word-2026-10-20.json)
reads only the source-named storage at106536580: raw7093f50201000000 gives
102f59370, the already retained enrollment adapter. Root independently
[rechecked the pinned image, segment mapping and eight bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-enrollment-callback-word-coordinator-recheck.json).
Under the recovered constructor load/call interpretation, callback identity no
longer rests on its printed alias alone. File storage is not current runtime
storage, invocation, candidate admission or actual D+358 identity.

The [specific virtual+170 getter query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-model-metadata-getter-frontier-2026-10-20.json)
retains the complete64C-byte body of102f4f834, returning&DAT_106e6e618. Root
read the body and independently matched its exact original export row/hash.
This gives the +170 target its own source evidence; the earlier +168 association
is no substitute for it. Both new queries remain exploratory source research,
not runtime or public behavioral approval.

Neither result reveals initialized map contents, exact lookup key/node/type,
member admission, generated unit/model identity or connection to the same
processor Mute endpoint. The later [bounded literal navigation](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-model-map-literal-frontier-2026-10-20.json)
retains eight matching records/44occurrences across two chunks, with at most
three lines per occurrence. These are source-literal matches, not exhaustive
native references. Its selected class/declaration continuation is below.
All38application scenarios remainU.


The [two-body class/declaration successor](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-model-map-declaration-frontier-2026-10-20.json)
retains full102f7b860 and non-thunk102f4fb10 (11,919C bytes total), read by Root.
The former supplies the same DAT106e6e618 with literal AStereoGain, parent/factory
operands and a recovered thunk callback operand; a later call labels its getter
result Utility. The latter supplies that same metadata address, literal mpMute
and offset0x350 to10147e954, with locally obtained metadata/flag operands. This
narrows source declaration provenance; it does not equate wrapperD+350 with
childD+358 or prove actual map entries, helper ABI, callback invocation or
runtime initialized type. The expanded thunk record is not an independent
second implementation or a verified pointer word. [Independent association review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-model-map-association-review.json) approved the exact file/source associations only, with no required findings.
Actual runtime type/key/map admission, unit/processor identity and public
delivery remain unknown. The next source-only question is the registered
declaration callback invocation and metadata map population, not another
name/string/buffer helper. One exact retained registry-literal search, capped
at12records/three context lines per occurrence, may select at most two clearly
relevant complete bodies/12000Cbytes. No new image word, provider or original
execution is selected. Literal matches cannot prove all native references or
actual runtime initialization/invocation.


### Registry declaration and map construction — 2026-10-20

The [registry query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-map-initialization-frontier-2026-10-20.json)
[passed partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-map-initialization-review.json).
Three retained records/43literal occurrences are not all native references.
One new complete function10147ef4c (10297Cbytes) invokes each reached metadata
entry's+40callback, optionally+48, then on a later pass walks its descriptor
list and attempts+88map population through10148d148, storing the descriptor
in returnedentry+18. Intervening10147f568, exact key/insertion semantics,
actual node/registry membership and startup invocation remain qualified.

The separate [12-byte wrapper query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-registration-wrapper-register-frontier-2026-10-20.json)
[passed independent raw-data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-registration-wrapper-register-review.json).
Exact10147e7c4..e7cf is LDRB W8,[SP], STRB W8,[SP], then non-link branch to
10147e458. Conditional on reaching that branch with valid ordinary stable
stack memory, receiverX0/callbackX5 andSP remain unchanged. X8 changes and
one stack byte is read/written; no all-register/no-stack-traffic claim or proof
of caller assignments/actual invocation. Root checked the pinned image,
header/segments and only those12instruction bytes as data.

These narrow registered declaration-to-map construction. Actual mpMute key/node
admission, wrapperD+350 versus childD+358, created unit and processor/public
Mute delivery remain unknown. All38application scenarios stayU; no signal law,
feasibility/no-route finding, case or grade. This branch is stopped at these
boundaries; no further callee/word or original execution selected.


### Conditional map-entry storage — 2026-10-20

The direct10148d148 selection first [stopped at metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-map-entry-helper-frontier-2026-10-20.json):
its complete9293C bytes exceeded the initial6000C cap. Root explicitly expanded
only that same body to10000C. The [complete successor](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-map-entry-helper-body-frontier-2026-10-20.json)
[passed partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-map-entry-helper-body-review.json),
with exact raw row, seven source spans and the known caller span checked;
six watched paths stayed unchanged. No source/native function was executed.

Conditional source result: with valid stable non-null key/storage, recovered
argument correspondence and normal returns from unread helpers, search can
return an existing entry. Otherwise a new32-byte entry receives the
key-associated pointer at+10, zero at+18, is linked and returned. The known
caller supplies &local80 with local80=N+40, then stores that enumerated nodeN
at returnedentry+18. Existing entries can also have their payload replaced.
This narrows key-associated storage, without establishing actual mpMute lookup
or a public duplicate-name policy.

The recovered four-parameter helper signature versus five caller operands,
null-relative reads, unaff_x25 expressions and unread extraction/discriminator/
rehash/cleanup operations prevent a complete ABI, empty-key or error policy.
Actual mpMute node provenance after preprocessing, matching lookup key, runtime
registration/admission and wrapper/child/unit/processor delivery remain unknown.
All38application scenarios remainU. No generic hash/allocator chase is selected.
The next source selection is only10147f568, called on the same metadata receiver
immediately before its descriptor-list traversal: one complete non-thunk body
within12000C bytes, to identify list construction/mutation/preservation, then
stop before callees or further words. No original Utility execution is selected.


The selected [preprocessing body](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-descriptor-preprocessing-frontier-2026-10-20.json)
[passed partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-descriptor-preprocessing-review.json):
988C bytes, four exact source spans/caller span, six watched paths unchanged.
Under its guard, it walks a referenced receiver's nodes, passes new allocations
and those nodes through an unread constructor and list helper, then writes a
flag. The recovered self-call omits its receiver. This is an augmentation-like
attempt; clone/merge semantics and preservation of the local mpMute node are
unproved. This selection is exhausted. No constructor/list/hash/allocator
callee or word is currently selected; all38application scenarios remainU.


Root separately selected only the direct list helper10144a040 after metadata
screening (535C/60native-body bytes). The [new source query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-descriptor-list-splice-frontier-2026-10-20.json)
retains a source-local splice interpretation under valid list, fresh-node and
argument/layout premises. [Independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-descriptor-list-splice-review.json)
approved its conditional local result: existing links change, while non-link
key/offset fields remain untouched under valid disjoint-list/storage premises.
This supplies no actual mpMute membership or runtime result. No constructor, recursive call,
key/hash helper, image word or original function was followed.


### Conditional declaration-node list binding — 2026-10-20

The [direct008helper query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-declaration-list-binding-frontier-2026-10-20.json)
[passed partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-declaration-list-binding-review.json):
517newC bytes/two exact spans,2193reused builder/constructor C bytes with warnings
preserved, exact declaration context and eight unchanged watched paths.

Under recovered argument/layout and valid fresh-node/list/lifetime premises,
the declaration builder passes the same allocated node through construction
and appends it to that metadata receiver's M+50list. The008helper changes the
old-tail/sentinel links and counters, not old non-link key/offset fields.
Later isolated040fresh-node insertions preserve its relative reachability and
non-link fields under their explicit premises. This source-local node/list
binding narrows the prior provenance gap; it is not an observed runtime member.

Actual construction/base identity, key encoding/spelling, runtime type word,
recursive/other mutations, matching lookup and processor/public delivery remain
unknown. Name length0xd is not a proven typeID; mpMute and Mute are not equated.
No further D03callee/word/native is selected; all38application scenarios stayU.


### Conditional preprocessed-node field copies — 2026-10-20

The [selected preprocessing constructor](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-preprocessed-node-constructor-frontier-2026-10-20.json)
[passed conditional source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-preprocessed-node-constructor-review.json).
Complete101480d60/2118C bytes directly copies source+30/+38, and assigns the
source+40 key-associated pointer with conditional pointed-counter updates and
an unread release call/source reload. Other shown pointer/scalar stores are
retained. There is no visible name transformation or offset rebasing in these
assignments; no deep-copy/every-byte or unconditional pointee preservation law.
Seven author-watch providers and eight reviewer-watch paths stayed unchanged.
The initial author search displayed the body before a separate metadata-only
projection and exposed one incidental67C thunk; the query preserves this lapse,
and no inference uses the thunk.

Base-return/allocation identity, initializer/release/reentrancy effects and
recursive/runtime admission remain conditional. This narrows one constructor
boundary, not the actual key/type lookup or public Mute/processor connection.
All38application outcomes remainU. Further selection should target the missing
lookup/processor edge from retained evidence, without expanding an ownership
helper chain merely because it is unread. No original Utility run is selected.


### Candidate-name delegation boundary — 2026-10-20

The retained-evidence [lookup frontier proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-lookup-join-proposal-2026-10-20.json)
selects the actual cached descriptor's query-key provenance. The [direct name helper](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-candidate-name-frontier-2026-10-20.json)
[passed bounded source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-candidate-name-review.json):
complete101482918/271C bytes delegates through recovered receiver+18's vptr+18.
Both indirect-jump/call recovery warnings remain material. The caller projects
an output-like local90 address and candidateplVar21; this C alone cannot assign
those to native receiver/output arguments or identify a name/key/virtual target.
Seven reviewer-watch paths stayed unchanged. No mpMute/Mute equality follows.

The required predicate remains same admittedD+358 candidate→cached queryQ→same
metadataM+88 entry→descriptorN30=-1/N38=350→D+350wrapper+8, with native forwarding
and actual invocation/lifetime premises. The unit/processor/public-gesture join
is separate. All38application outcomes remainU. Root selects only exact C2
caller1025c1ea8→101482918 metadata and a proposed helper16B/caller-window<=48B
static decoding preparation if a unique callsite is identified. No actual new
image extraction/decoding, virtual word, callee follow or original run selected.


### Actual candidate-name helper static data — 2026-10-20

Root read all six sealed preparation files and selected the exact16-byte
helper extraction/static decode once at11:10:54UTC. The [frozen actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-candidate-name-instruction-data/manifest.json)
contains12payloads/13files; one installed Rizin attempt/PID297066 exited0 with
empty stderr and four byte-exact rows. All20inner/41outer scoped watched paths
stayed unchanged; [Root receipts](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-candidate-name-static-root-execution/receipt.json)
retain the selection and actual stdout/stderr. Static decoding executes no
original instructions; Corpus original children remain17, Utility original0.

Root independently decoded raw load/branch bitfields: X0 loads entryX0+0x18,
X9 loads that object's vptr, X1 loads vptr+0x18, then a non-linking BR X1.
These four instructions leave X8 and LR locally unchanged. This does not prove
what caller operand enteredX0, that X8 carries local90, or the target's output
convention/name/key. Separate actual-data review is pending. Nine retained C2
callsites do not identify the bool branch; the caller window remains disabled.
The known C2 schema cannot query the proposed arbitrary-data reference; no
query/zero-hit or native absence claim is made. No targetword/callee/original
execution is selected. All38application outcomes remainU.


The [independent actual-data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-candidate-name-static-actual-review.json)
now approves only that conditional16-byte register result: fresh pinned image,
header/mapping/same16bytes and all four bitfields checked,75scoped paths unchanged.
Preparation authorship is disclosed; this is independent actual-data checking,
not independent reapproval of the reviewer's method. X1 is overwritten; local
X8/LR preservation does not prove any actual output carrier or target return.

Retained caller contexts show1067e18f8 is a shared intermediate descriptor vptr
in eight branches; it cannot uniquely identify the bool branch. The later typed
1067e1d18 plus virtual330→descriptor+28 sequence is a stronger possible local
discriminator. Root selects preparation only for nine exact128B windows
[callsite-16,callsite+112),1152B total, all inside the existing5352B caller body.
All nine results must be retained; no site-order or shared-vptr inference,
no automatic window/callee expansion if branch evidence is absent/ambiguous.
No caller image bytes are selected for extraction until the new preparation
passes full source inspection. Runtime same-candidate/key/processor/public
joins remain unknown; all38application outcomes stayU.


### Actual fixed caller windows — 2026-10-20

Root fully read the new7910B runner and all five preparation files, then
separately selected the nine fixed128B windows at11:19:49UTC. The [actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-candidate-name-callsite-instruction-data/manifest.json)
binds64payloads/65files:1152selected instruction bytes, nine decoder attempts/
PIDs/exit0/empty stderr, all288rows byte-exact. All14inner/139outer scoped paths
stayed unchanged, including all99first-v5stage/preparation files. [Root receipts](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-candidate-name-callsite-static-root-execution/receipt.json)
retain selection/exit and preservation. No original instructions or ESIL ran.

Root read all288rows and independently decoded native argument/BL and adjacent
ADRP/ADD bitfields. All nine calls setX8=SP+0x40; the first passesX22 inX0 and
other eight passX28. Only the selected2470window contains typed1067e1d18
construction at24b4/24b8→store[X25], followed byX28vptr+330→BLR→byte[X25+28].
Local null/counter branches rejoin24b4. This matches the retained conditional
bool-descriptor source context by actual literals/operations, without ordinal
or shared-vptr inference. Independent actual-data/correlation review is pending.

This is a conditional local ABI/source correlation. X28's actual D+358 identity,
admission, namegetter target/return contents, stable stack/key/type/map, other
helper effects and sameunit/processor/public delivery remain unknown. Normal
calls/callee-saveX25/X28, valid pointers/lifetime and no interference are premises;
no unselected or out-of-window branch path is followed. No global-unique or
all-path claim follows. No targetword/callee/original run is selected; all38
application outcomes remainU.


The [independent caller-data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-candidate-name-callsite-static-actual-review.json)
now approves only this conditional selected-window register/source correlation.
It freshly checked all288rows/same1152imagebytes,17ADRP/ADDpairs, all nine BL/local
argument setups, the unique selected typed sequence and local branch rejoins;
220scoped paths stayed unchanged. Four valid-encoding perturbations reject the
typedliteral/storebase/330offset/branch predicates. Preparation authorship is
explicit; no decoder/ESIL/runner/original replay or extra image/source occurred.
No actualD+358/name/key/unit/processor/public result follows. Next navigation
uses existing retained evidence only to identify a concrete remaining predicate;
no new source body/index/image/word/original run is selected.


The next concrete retained-source predicate is enumeration provenance:
modelvirtual+60→interfacevirtual+20(D,node)→returnedwrapper+8→candidate. Existing
records C140–152 and the retained model+60word/getter101482c00 show the interface
object address106ccb370, not its vtable. Root selects only that object's exact
8B imageDATA firstword, with fresh identity/header/mapping verification. Stop
before any resultingvptr+20word/callee selection. No candidate/name/key/runtime
or public behavior is inferred before that evidence is reviewed.


### Conditional enumeration-node resolver — 2026-10-20

The [interface object firstword](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-enumeration-interface-word-frontier-2026-10-20.json)
[passed exact data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-enumeration-interface-word-review.json):
106ccb370storage contains candidatevptr106674880, not a vtable at106ccb370.
The separately selected [vptr+20word/resolver](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-enumeration-member-resolver-frontier-2026-10-20.json)
[passed conditional source/data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-enumeration-member-resolver-review.json).
Exact8B at1066748a0 identifies101489084; its complete235C body selects D or
load64(D+u32N30) according to signedN30, then adds signedN38. Under actual same
node N(-1,350), valid current model/vptr/ABI/storage and normal no-interference
premises, the wrapper ADDRESS is D+0x350. Existing caller reads wrapper+8:
child C=load64(D+0x358). C is not the storage address D+0x358. Earlier compact
'D358' references denote this still-conditional field/child path, not pointer
identity with that address.

Root rechecked each selected word/image identity/header/mapping and exact raw
resolver record/spans. Ten scoped review paths stayed unchanged. No instruction
decode or original function ran. This closes one conditional direct-node layout
edge, not which node/callback/type actually admits C, its name/key/cache, same
unit/processor or public Mute delivery. All38application outcomes remainU.
Next navigation reuses retained evidence only; no more source/index/image word/
callee/original execution is selected.


Root next selects only101aa8400 metadatafirst, then a complete nonthunk body
within4000C if available. Existing registry caller1021407cc explicitly supplies
StereoGain and callback10215eafc; the retained callback constructs Mute bytes
and calls its receiver virtual58. The question is concrete descriptor-builder/
registry-entry provenance for the existing entrytable consumer, not an entry
kind inferred from the name. No automatic callee, word or runtime expansion.


### Conditional processor callback registration — 2026-10-20

The [selected registration source](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-processor-registration-frontier-2026-10-20.json)
[passed bounded source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-processor-registration-review.json).
Complete585C body101aa8400 receives the retained StereoGain callback10215eafc.
Conditional on valid helper result R and recovered arguments, it writes that
callback to R+0x28, four captured bytes to R+0x30 and eight captured bytes to
R+0x38. It does not invoke the callback. Helper101aae52c and setup values remain
opaque; its DAT106f563b8 is distinct from consumer lookup DAT106f56368 and
PTR106ccd5a0. No equality or conversion between those records is established.

Root verified the exact raw JSONL/body/spans and retained caller/callback
associations; six scoped paths remained unchanged. No new image word, native
instruction or original code ran. Actual callback receiver/builder, consumer
entry kind and same unit/processor/public Mute joins remain unknown. All38
application outcomes stayU. The next navigation reads existing retained evidence
only for a specific later callback invocation or receiver-construction edge;
no new export body, image word, decoder or runtime call is selected.


Existing-evidence navigation then stopped: selected Utility providers retain
the exact callback store and separate consumer lookup, but no later invoker
of R+0x28 or builder-to-consumer construction edge. Following101aae52c would
reopen generic insertion, without supplying that bridge. No named next body
is selected. This is a retained-evidence gap, not native absence or a proved
infeasible route. No additional source query/report or execution was produced.


### Callback invocation and consumer-table construction — 2026-10-20

A new exact-literal navigation over retained export chunks found four records
containing DAT106f563b8, not a count of native references. Root displayed their
metadata/matching lines, then selected only the complete6945C101aa85a0 body.
The [frozen query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-callback-invocation-frontier-2026-10-20.json)
[passed independent conditional source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-callback-invocation-review.json).
It reads source node+28 and invokes that callback
with a local builder carrying vptr operand106755e10, then constructs a table
assigned to DAT106f56368 using handle storage PTR106ccd5a0. It copies a local
vector into destination+180 and writes count+17c. This conditionally narrows
the previously missing bridge; the source and destination globals are still
distinct, not equal pointers. Header+100 is not each vector entry's kind+100.

Actual registered-node membership, startup/order, recovered ABI/helper effects,
vector contents and Mute entry kind remain unknown, along with current model/
unit/processor/public delivery. No new word/decoder/original execution or grade;
all38application outcomes remainU. No further body/word is selected until
independent source review. First in-memory query draft hit a duplicate-anchor
assertion before writing; final query uses explicit spans and discloses it.


Independent review confirmed all four exact spans and seven scoped provider
identities unchanged. The minimum-one allocation capacity does not imply a
nonzero recorded vector count. Header+100/+108 receive post-callback locals;
identity with pre-callback registration values additionally requires no relevant
callback mutation. The memcpy at destination+168 crosses into first-slot
storage and is not characterized as entirely header-only. These qualifications
leave actual registration/type/key/processor/public outcomes unknown.

Root next selects only the source-named builder-vptr+58 image word106755e68,
with fresh full-image/header/mapping verification. Synthesis retains that one
8B data result; no resulting body, adjacent word, decoder or original code is
selected. A file word cannot establish current runtime vptr or invocation.


The selected [builder+58 file word](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-builder-virtual58-word-frontier-2026-10-20.json)
[passed exact data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-builder-virtual58-word-review.json).
VA106755e68 maps uniquely to __DATA_CONST fileoffset108355176; raw8B
1883aa0101000000 gives101aa8318. Root independently rechecked full image
identity, header/53loadcommands, mapping and same8B; six scoped paths unchanged.
No original function/instruction ran. File slot and source operand only give a
conditional dispatch association, not actual invocation or an entry kind.
Root next selects101aa8318 metadatafirst and its complete nonthunk C body only
if within4000B. No other body/word/opcode/runtime is selected.


### Conditional builder entry forwarding — 2026-10-20

The [selected101aa8318body](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-builder-entry-frontier-2026-10-20.json)
[passed bounded source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-builder-entry-review.json).
Complete199C/warning-free projection forwards(param1,param2,7) to101aa7f64 and
stores originalparam3 as eight bytes at the returned base+110. The literal7
is not yet a kind: this body contains no direct kind-field store or append.
Root checked exact raw row/body/span and six scoped paths unchanged.

Root separately reread existing consumer102329954: entry+100 kind7 branches to
10232d250, distinct from kind1→10232cd38. This is a future conditional consumer
route, not an established Mute entry type. Selected successor is only helper
101aa7f64 metadatafirst/completebody<=5000C to test actual kind/store/returned
entry identity. No consumer branch body, other callee/word/opcodes/runtime is
selected. Actual initialized registration/admission/processor/public outcomes
remain unknown; all38application scenariosU.


### Conditional appended kind and return-value gap — 2026-10-20

The [complete3468C helper query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-builder-append-kind-frontier-2026-10-20.json)
[passed bounded source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-builder-append-kind-review.json).
Under valid ordered vector/storage and normal helper premises, builder end
advances by120 and appended entry E=end−120. The explicit late four-byte
store at end−20 is E+100 and receives caller literal7. This source-local kind
store narrows the consumer branch without deriving a kind from the Mute name.
The following eight-byte allones store is E+104. Allocation/name/fill helpers,
actual vector contents/runtime callback/table identity remain qualified.

The helper projection declares void and bare return, while its caller consumes
a returned long before the E+110 callback-value store. Returned-base==E is
not yet established. Root verified raw row/fullbody/spans/pins and seven scoped
paths unchanged. A [design-only fixed96B tail](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-builder-return-instruction-preparation-2026-10-20.json)
was read/accepted for preparation:101aa80cc..101aa812b,24static instruction
slots, within the existing456Bbody. Authoring reuses the inspected data-only
collector pattern; no extraction/decoder run is selected before source review.
Opaque call-return/ABI and outside-window origins remain explicit limits.
No original instructions, application or Utility instance ran; all38U.


### Actual builder tail data and conditional kind7 unit — 2026-10-20

Root fully read/reconstructed the6744Bcollector preparation; [source preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-builder-return-instruction-preflight-review.json)
passed fixed bounds/pins/AST and CLIrefusal. Root selected exactly one static
96Bdata decode at12:03:51UTC: [actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-builder-return-instruction-data/manifest.json)
1855B/SHA1b6ceaf4e295dce15a623ad50acd835074a2bb4f085732c447cc972c79e44a2b,
11payloads/12files. All24rows byte-exact, RizinPID339764/exit0/empty stderr,
12inner/2182outerpaths unchanged. No original instructions executed.
[Root receipts](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-builder-return-root-execution/receipt.json)
retain attempt/PID/status/maps; independent actual-data review is pending.

At80f4 X0=X21;80fc calls opaque1054d70a0; eight instruction rows8100..811c
do not redefine X0 before normal RET8120. Thus only survival of the last call's
returned X0 is supported locally. X21==appended E and actual lastcall return
semantics remain external/outside-window premises; source naming alone does
not prove the actual import target. The frozen Root assessment's mistaken
count 'six' has a separate [count-only correction](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-builder-return-root-assessment-addendum.json);
raw data and assessment remain immutable. No predecessor/callee/import/word is
selected by this result. All38application outcomes remainU.

Root separately selected exact consumer kind7 target10232d250 metadatafirst/
complete796Cbody, retaining a [private query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-unit-frontier-2026-10-20.json)
under independent Modulation review. Projected helper supplies U; U+50=graphG,
U+58=entryE, then another helper receives(G,U). U+64's byte1 is decimal100,
distinct from entry+100(hex)kind7; bind's literal3 is a separate argument.
Actual allocation/type/bind/attach/helper effects and same model/processor are
not established. No downstream helper body or original/runtime call selected.


The [actual96B review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-builder-return-static-actual-review.json)
approved all24row operand fields and the corrected eight-row X0survival claim;
25reviewer artifacts/image stayed exact. The separately preflighted [32Bprefix](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-builder-entry-origin-instruction-data/manifest.json)
ran once12:12:38UTC:8byteexactrows/RizinPID341290/exit0/empty errors,12inner/
2193outerpaths unchanged, old96Bpacket exact. On reached80bc the store writes
X25 to OLDX21+2b0;80c0 sets NEWX21=X25−120. Origins/validity of oldbuilder/end
and opaque import-return semantics remain premises. Independent actualdata
review pending; no new window/callee/import selected.

[Kind7 unit review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-unit-frontier-review.json)
and [bind query/review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-bind-review.json)
approve only local projection/field associations. Complete286Cbind writes
U+4c=byte3,U+18=load64(P)=E,U+20=load8(P+8); adjacent-source byte is not E+8,
and projected local40=0 does not prove stack adjacency/value. New251C
construction query is frozen under Root review; no allocation/type/implicit
object ABI or public behavior conclusion is adopted. All38application U.


The [independent32Bactual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-builder-entry-origin-static-actual-review.json)
approved all eight operand rows and conditional old/new X21 distinction;37
reviewer artifacts including old96Bpacket remained exact, plus fresh same-image
identity/mapping verification. Origins/currentend/validity/lastBLreturn contract
remain premises. Exact retained metadata only for lastBLsite80fc/target1054d70a0
is now selected to test the import association; no callee/word or runtime follow.

### Conditional unit first-word association — 2026-10-20

The [construction query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-construction-frontier-2026-10-20.json)
[passed Root partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-construction-review.json).
Complete251C102311b5c obtains U from1012d9850(68), calls recovered zero-argument
102328380, writes literaladdress1067938a0 to U's firstword, writes U through
output O, then increments intU+8. These stores are projected source facts under
valid result/output/ABI/normalhelper premises; allocation size/type/constructor
implicit receiver/refcount meaning are not inferred. Root verified exact raw
row/code/fourspans/callercontexts/provider identities; seven scoped paths unchanged.

The exact firstword operand supplies a concrete laterunit-consumer direction.
Modulation selects only retained C2vtable/alias/index metadata for1067938a0;
no table word or arbitrary slot/method/body is selected. All runtime/type/key/
unit/processor/publicMute joins and38application outcomes remainU.


### Exact unit-table and import metadata frontiers — 2026-10-20

The [unit-table metadata query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-vtable-metadata-frontier-2026-10-20.json)
[passed bounded availability review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-vtable-metadata-review.json):
none of five exact retained C2indexes contains literal1067938a0. Root
independently streamed their hashes/linecounts/exact case-insensitive lookup.
Nine scoped query/provider paths stayed exact. This is a retained-index limit,
not absence of a vtable/type/reference/runtime route. No slot was guessed.
Root separately selects the known kind7 directcall102322e58(G,U), metadatafirst/
completebody<=6000C only, for a concrete attachment/later-consumer edge.
No automatic callee/tableword/instruction or runtime expansion follows.

The [lastcall import metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-lastcall-import-metadata-frontier-2026-10-20.json)
[passed exact source-association review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-lastcall-import-metadata-review.json).
Exact caller101aa7f64/site101aa80fc/target1054d70a0 has primaryIMPORTED_strncpy,
thunkEXTERNAL:6a6 and external library/usr/lib/libSystem.B.dylib in retained
C2metadata. Root checked exact three rows and exporter-schema spans/provider
hashes; seven scoped paths unchanged. This strengthens the file-symbol
association beyond the projected label, not actual loader/binding/library
implementation/return-value proof. Synthesis selects only primary Apple/POSIX
documentation for that public return contract, preserving it as a conditional
external premise; no original library/code/instance runs or publicMute grade.


### Conditional builder return and unit attachment — 2026-10-20

The [reviewed public string contracts](sources/c-library-string-contracts.md)
supply the external destination-pointer return premise. Composing that contract
with the reviewed native prefix/tail supports helper-return E only if the actual
call is conforming, its ABI and buffers are valid and it completes normally.
Import metadata does not establish runtime binding or current library behavior.
No original library/Utility execution or application grade follows.

The [2165C attachment query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-attachment-frontier-2026-10-20.json)
[passed Root source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-attachment-review.json).
Projected102322e58(G,U) increments U+8, conditionally compacts/grows storage, then
appends U to G+40's pointer list and increments ushort countG+52. CapacityG+50
and compaction byteG+58 are different bases from U+50=G/U+58=E. Actual capacity,
lifetime and later traversal/dispatch remain premises; this body does not read
entry+110's callback or a unit method. Root verified exact row/body/spans/pins.

Two count-first locator queries stopped without inspecting candidate metadata
or body snippets: [two literals](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-graph-list-locator-frontier-2026-10-20.json)
returned214matches; [three literals](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-graph-list-registry-locator-frontier-2026-10-20.json)
returned81, both exceeding20record cap. These are author-retained search counts,
not fresh Root recensus or semantic review of418417records. Offset cooccurrence
does not prove graph identity; absence from either predicate excludes no route.
No narrower lexical search or first20subset is selected.

### Exact unit address-block data — 2026-10-20

Root separately selected exactly64B [1067938a0,1067938e0), starting at the
reviewed construction literal. [Frozen query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-dispatch-block-frontier-2026-10-20.json)
21043B/SHA71c2c838f07260914a015a2ef622f00907347317adba58b32105d9d08173fbe7
[passed independent literal-data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-dispatch-block-review.json).
Fresh full image/hash/header/53loadcommands and unique file-backed DATA_CONST
mapping passed; raw64 SHA2a48b37b0e2ee5e5bb181df01e7a9a53c3580dc768b59809dee1e5d87ceff38a.
Eight physical LEu64 values are102313778,102313810,10128eed4,10024a140,
102324ee4,102312d24,1023286d4,1023286dc; all eight provider pins and nine
reviewer-scoped paths unchanged. Root read the complete peer review; fresh full
image/data reconstruction is carried by that independent review.

These bytes establish neither a whole table/extent nor logical slot roles,
signatures/callability/actual relocated pointer values. Root next selects exact
retained metadata only for those eight values; no target body/opcode, extra word,
runtime dispatch or public Mute association follows automatically. All38Utility
application outcomes remainU, with no new normative ID/case/grade.


### Selected unit projections and initialization limits — 2026-10-20

Exact eight-target metadata led to [eight complete retained projections](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-selected-bodies-frontier-2026-10-20.json),
3659Cbytes within4000cap. Root read all bodies/claims and the [independent source
review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-selected-bodies-review.json);
all rawrows/metadata/spans/eightaliases matched,16author pins/17reviewer paths
unchanged. Recovery warnings remain explicit. This approves function-local
source associations only, without actual object/ABI/dispatch/public semantics.

Warned10128eed4 projects firstword(P)+20 indirection with omitted arguments,
then separately reloads firstword(P)+8 and calls with P. Each read independently
requires actual firstword1067938a0 to associate physical values102324ee4 and
102313810; no vptr persistence across the first call is established. In102324ee4,
nonsentinel uintP+30 indexes unread106797358 with &local receiver copies/P+28,
then unread10128ee2c(P). That is no entryE+110 callback join. Two other projections
read bytesP+64/P+66; source caller-store joins need sameU/no-interference/ABI.
No explicit direct U+18/U+4c/U+58/E+110 access occurs in these eight projections;
unread helpers/aliases can access them, so no global absence follows.

Known constructioncallee102328380's [314C initializer](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-initialization-frontier-2026-10-20.json)
[passed Root source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-initialization-review.json):
P is unread102312d04's result, not proved allocationU. It writes firstword
106798da8, qwordzeroP+50/P+58/P+5d(through64), word0202P+65 and byte1P+67.
Root verified rawrow/wholecode/fourspans/directcaller/eightpins; ninepaths exact.
No direct payload28/index30/U18/U20/U4c/E110 access, nor proof of default survival.
The next141C source query for102312d04 is frozen under Root review; projected
void return versus parent value consumption leaves an explicit native-ABI gap.
Root selects only named102323d98 source<=6000C for concrete inherited payload/
index initialization; no further generic descent or table/opcode/runtime follow.
All38Utility application outcomes remain U.


The [141C base projection](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-base-initialization-frontier-2026-10-20.json)
and [827C payload initializer](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-payload-initialization-frontier-2026-10-20.json)
[passed Root local-source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-base-and-payload-initialization-review.json),
all original rows/code/spans/parent pointers/eight+ninepins verified,12unique
paths unchanged. Base102312d04 writes Q firstword1067939c8, but declares void
while parent consumes a pointer. Payload102323d98 similarly obtains R from unread
10128ed98 and declares void while parent consumes its result. R/Q/P/U remain
distinct unknown identities; no more generic initializer descent selected.

Under validR,827C directly stores payloadR+28=zero/indexR+30=zero, R+38=zero,
R+40=zero, R+48=00ff00ff, byteR+4c=zero; R+18 gets a word through a global-associated
pointer and byteR+20=1. Guards/empty-text literal/private names establish no
actual singleton/key/default. Even a conditional R=U does not prove current
payload/index/admissibility or entryE+110 delivery. Root instead selects only
existing reviewed Mute callback operand1065411a0's associated target10216533c,
metadatafirst/source<=6000C after exact prior-word-evidence reconciliation;
no new word/callee/opcode/runtime is selected. All38application outcomes U.


### Registered Mute callback endpoint — 2026-10-20

The [446C endpoint query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-registered-callback-endpoint-frontier-2026-10-20.json)
[passed Root bounded source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-registered-callback-endpoint-review.json).
Existing model-routing word record /word_reads/reads/0 at1065411a0 retains bytes
3c53160201000000→10216533c; exact frozen record/manifest/review and registration
source244–247 reconcile, with no fresh image/word read. Callback metadata names
OStereoGainProcessor::OnMute; that name is not actual receiver/delivery proof.

For recovered receiverP/inputF, source stores predicate(F!=0) atP+161. Distinct
byteP+162==1 selects unread10215f3e0 with omitted arguments; otherwise it calls
1047bd760(P+48,F!=0). P+48 state, P+161 saved flag and P+162 selector are distinct
bases/fields, not graph unitU/entryE. Root read completebody/claims/reconciliation,
verified rawrow/code/three spans/priorword/sourcepointer/sixpins; sevenpaths exact.
Actual ABI/input domain/receiver/invocation/entryE+110 binding/helper/audio effects
remain U. Root next selects these two exact branch helpers metadatafirst, complete
bodies only if aggregate<=6000C, no other callee/table/word/opcode/runtime.

A separate32B[102312d04,102312d24) native-return investigation is preparation
only. Synthesis adapts the inspected32B data collector with fixedrange/destination/
pins/map changes; no selected instruction bytes/extraction/decoder before Root
fullpreflight and separate actual selection. It can address the recovered void/
consumed-pointer gap only, not automatically R/Q/P/U identity or runtime behavior.


### Native base-return data and callback storage frontier — 2026-10-20

The first32Breturn preparation remains frozen/unexecuted. Root's [focused R1
preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-return-code-preflight-r1.json)
found UTBASE-PREFLIGHT-001: matching synthetic rows with invalid type/empty opcode
passed its inherited metadata guard. This was no actual decoder failure or
retroactive failure of independently verified historical windows. [R2 preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-return-code-preflight-r2.json)
closed the finding: normalized rejection,26fixtures(two valid/24rejects), exact
two collector changes inverse-reconstruct R1, fresh image/tool/header/TEXTmap,
25watched paths unchanged. Root fully read oldcollector/metadata and all newdeltas.

Root separately selected one static32B decode at13:07:31UTC: [actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-kind7-base-return-instruction-data-r2/manifest.json)
2025B/SHA059c1d1d8959c4971d492fa314971a18c6e3aabf8f430159dcd89b0b7ef5ae5c,
11payloads/12files; all8rows byte-exact, decoderPID354992/exit0/empty errors,
25inner/[2219outer paths](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-return-root-execution/receipt.json)
unchanged. No original instructions executed. Independent actual review pending.
Root provisionally reads BL102323d98, then X8=1067939c8/STRX8[X0]/RET with no X0
redefinition. The opaque helper's returned pointer survives as a carrier; its
object identity and actual parent consumption/ABI/R/Q/P/U remain conditional.

The [two branch helpers](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-callback-branch-helpers-frontier-2026-10-20.json)
[passed Root source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-callback-branch-helpers-review.json),
1977C/rawrows/five spans/ninepins verified,tenpaths unchanged. Explicit setter
S=P+48 writes byteS+cf=P+117, distinct from P+161/P+162. SelectorR=P is unproved
because its caller omits arguments. Reached148/149/162/161 predicates supply
operand1065411b0 to101aa4b94(handleR+260,...); repeated162reads need independent
state premises across opaque calls. No public enum/flag/audio law follows.

Exact8Boperand1065411b0 [passed Root fresh data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-selected-branch-word-review.json)
with same image/header/53commands/uniqueDATA_CONST mapping, sixpaths unchanged;
rawa853160201000000→1021653a8. Its271C target and748C handle-storage helper are
frozen under independent source review. Target's name CalcLegacyMute alone
supplies no silence proof; its projection stores qwordP+40=0. Handle storage/
forwarding does not establish invocation/target receiver. No additional body,
word/opcode/runtime or application grade follows. All38application outcomes U.


The [independent32Bactual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-return-static-actual-review.json)
now approves all8raw operand rows and opaque X0 carrier only. Fresh sameimage/
header/53commands/TEXTmap/same32B, manifest/25inner/2219outer current identities
passed;2250unique reviewer paths unchanged after resolving seven duplicate
relative/absolute spellings. Reviewer-authored141C source is disclosed rather
than independently reapproved. IncomingX0 and returnedX0 need not be equal;
parent consumption/ABI/currentobjects/RQPU/runtime/publicMute remain U.

The [271C target and748C handle source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-selected-branch-and-handle-storage-review.json)
approves exact rows/sixspans/priorassociations/providerpins, ninepaths unchanged.
Target stores qwordP+40=0; neither field purpose nor silence is established.
Helper stores F at H firstword, computes C=load64(T+18)+signed32(H+10)*18hex
with T=load64(H+8), then reads C+8 AFTER that first store. Pointer-transition
shorthand requires this order, not function-entry state under arbitrary aliases.
On an admitted change it stores F at C+8 and calls101a41ce8(load64(T+28),
load32(C+10),&localoperand), choosing F or a source fallback. No direct F invocation,
receiver binding, global route absence or audio result follows;18hex row stride
is not registry120hex stride. All38application outcomes remain U.

The [direct forwarder metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-direct-forwarder-metadata-frontier-2026-10-20.json)
stopped7481C>6000 without a body read. Root separately selected the SAME full
7481C under8000cap; [body query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-direct-forwarder-body-frontier-2026-10-20.json)
is frozen under independent review, no extra callee/word/opcode/runtime selected.
A separate count-first typed-unit locator uses exact same-body literals
`param_1 + 0x18`, `param_1 + 0x4c`, `0x110`; cap20metadata records/2000field-line
bytes. Known binder/entry offsets motivate this selection, but cooccurrence is
not actual sameU/E identity. Over-cap must stop before metadata/snippet reading;
no automatic narrower query, full body or application grade follows.


### Forwarder source review and typed locator limits — 2026-10-20

The [7481C forwarder](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-direct-forwarder-body-frontier-2026-10-20.json)
[passed independent bounded source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-direct-forwarder-body-review.json).
Root read the complete retained body and review. The prior6000cap metadata STOP
is preserved; the separately selected8000cap admitted only this same body.
Recovered V+10==0 normalizes null to a fallback, writes a10hex-stride table and
conditionally copies selected entries into18hex-stride records. The other
branch normalizes equality to fallback to null and updates a16hex-stride region
with literal marker, pointer or displacement stores. These source stores are
not decoded region instructions or evidence that the region executes. Different
labels do not prove selected F differs from current fallback. Saved V+50 gates
the only explicit further call,1011a6778; no direct call through F or explicit
storage of the caller-local address is identified. Alias/lifetime/helper effects,
actual receiver, runtime delivery, public Mute and audio effects remain unknown.

The [global three-literal locator](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-unit-entry-three-literal-frontier-2026-10-20.json)
counted89matches>20 and stopped before matching metadata/snippet/body reading.
Root separately selected [all89metadata under100cap](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-unit-entry-three-literal-metadata-frontier-2026-10-20.json).
No body was selected from that set; Root read all89compact name/entry/size/state
rows, not a fresh full semantic review of the entire metadata packet. Named
other-device processors do not identify this Unit route; generic names do not
prove its absence. The predicate may miss typed or separate-helper accesses.

A provider-local two-literal query accidentally selected chunk01643; its zero
result and [locator correction](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-binder-local-two-literal-provider-addendum-2026-10-20.json)
are retained. Known binder102324f44 is actually chunk01644:1. A separately
[corrected chunk01644 selection](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-binder-corrected-local-two-literal-frontier-2026-10-20.json)
finds only that already-known binder; two matching field lines total88C, no new
complete body. Neither local result is global absence or route-blocking proof.

Next selected source target is exactly1011a6778: metadata first, complete body
only if nonthunk/recovered and<=6000C. No additional callee, region word/opcode,
runtime run or new application grade follows. All38application outcomes remain U.


The exact [112C terminal helper](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-terminal-region-helper-frontier-2026-10-20.json)
[passed Root source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-terminal-region-helper-review.json):
recovered pointer B and expression(long)int N are forwarded to named operand
_sys_icache_invalidate, then return. Exact rawrow/code/two spans/parent call and
five provider pins reconcile; six Root-watched paths unchanged. The named
external contract/binding/effect was not inspected. No target F invocation,
processor receiver, region execution or public Mute/audio result is established.
This delegation branch stops at that external name.

Root next separately selects exactly64physical data bytes[1067938e0,106793920),
following the earlier64BUnitaddress block. No vtable extent, slot role or class
identity is inferred. Up to eight exact-address metadata lookups only; no body,
opcode, runtime or automatic follow. This asks whether further physical words
nominate a processing source beyond the first eight already read.


The separate [100-cap graph-list metadata pass](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-graph-list-registry-metadata-frontier-2026-10-20.json)
retains all81matches to exact40/52/78literal conjunction. Original4185file and
81locator catalog digests reproduce; earlier214/81over20 STOPs are unchanged.
Root read all81compact entry/name/Csize/native size/state/provider rows, not every
metadata field or any body. Named results identify other device processors;
no specific graph consumer is selected from generic names or address proximity.
The conjunction can exclude actual consumers that never access G+78, so this
is navigation evidence only. No actual G/Unit/entry/callback join or absence
finding follows, and no body is authorized from this set.


### Further physical unit words — 2026-10-20

The exact [64B continuation](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-dispatch-continuation-2026-10-20.json)
[passed Root independent data/metadata review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-dispatch-continuation-review.json).
Root read complete7016Bmethod as data and all retained query metadata/limits;
no supplied method was run/imported. Fresh fullimage/header53commands6944B/
uniqueDATA_CONST mapping/file108607712 and same64B/LEwords/sevenexact rawrow/
metadata identities verified,19paths unchanged. Raw SHA
f3e4237bd23973ddf995fabea6b40c31351313414df6be68c221914a3264439f.

Eight physical little-endian values are102325a98,102325b9c,1022fb9a0,1022fb9a4,
102312fa4,102328524,102311bfc,zero. Seven have exact genericFUN/undefined-signature
source metadata; four carry nonreturn recovery warnings. Zero is not a proved
terminator; adjacency does not establish table extent, slot roles, class identity,
current vptr/relocation or callability. No body was read for this data result.

Root separately selects these exact seven complete retained projections under
8500aggregateC cap (metadata sums7999), preserving all warnings. Synthesis owns
source analysis only; no callee/helper/word/opcode/runtime follow. Any field/
callback association must be expressed by source, not inferred from physical
adjacency. All38application outcomes remain U; no new requirement/case/grade.


The [seven-body query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-continuation-selected-bodies-frontier-2026-10-20.json)
[passed independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-continuation-selected-bodies-review.json).
Root read all7999C and the full6977Breview. All four nonreturn warnings remain;
complete source text is no verified native ABI. Receiver+38/+40 discriminants,
local pointer layers, allocation/link stores and indexed visitor-style calls
are explicit. One visitor return feeds byte[result+1] to two unread helpers.
In102328524, returned bit0==0 leads to a load of the THEN-CURRENT receiver
firstword and a call through its+70 with the receiver. No vptr preservation
across the visitor is assumed. Three other projections show bare or zero returns.
These are no UnitU+18/U+4c/entryE+110 delivery or processor/audio laws, and no global
absence follows. Reviewer11paths unchanged; preceding data authorship disclosed.

Next fixed data selection is only16B[106793890,1067938a0), two physical words
preceding the source firstword literal. It may provide type navigation but no
RTTI/header/offset-to-top/vtable-boundary role is assumed. Exact nonzero-address
symbol/metadata lookup only; no target string/data/body/opcode/runtime follow.


### Physical name-like prefix and section stop — 2026-10-20

The [preceding16B query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-preceding-words-frontier-2026-10-20.json)
[passed independent data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-preceding-words-review.json):
[106793890,1067938a0) maps to file108607632 and retains zero/106793e20;
11reviewer paths unchanged. Nested construction_context deictic wording refers
to historical prior64B query, not a current read at the excluded8a0endpoint.
Root read full10025Bmethod/query facts and complete5228Breview as data.

The separately selected [target16B query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-referenced-words-frontier-2026-10-20.json)
[passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-referenced-words-review.json):
[106793e20,106793e30) maps to file108609056 and retains10/105879dcd;
15reviewer paths unchanged. Root read complete currentmethod delta against the
previously read fullmethod, all selected query facts and5013Bpeer report. Both
nonzero values have zero exact top-level alias/vtable index matches; availability
only, not absence or RTTI/typeinfo/class/layout/runtime identity. No target text
was read in either16B result.

A [C-string-eligible selection](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-selected-literal-2026-10-20.json)
[correctly stopped at metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-selected-literal-stop-review.json):
105879dcd lies in unique file-backed__TEXT,__const, flags/type0, not required
C-string type2. No raw file or target bytes were produced. Root full7046Bmethod
and query scope read, fresh fullimage/header53commands6944B/exactsection/raw80/
filemapping independently checked,18paths unchanged. This is no no-string finding.

Root separately selected [fixed64B data](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-selected-const64-data-2026-10-20.json)
[105879dcd,105879e0d) inside that__const section, preserving the earlier guardSTOP.
A printable19Bprefix `17AFloatEventInPort` ends at NULindex19;44suffix bytes remain
uninterpreted. Synthesis independently reviews only this raw/mapping/prefix data.
The literal is not a proved RTTI/type name, actual class/Unit/receiver, float
callback ABI or public Mute law. No other string, body, opcode or runtime follows;
all38application outcomes remain U and no case/criterion/grade is added.


The [fixed64B data review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-kind7-const64-data-review.json)
now approves only mapping/rawidentity/19BASCIIprefix; Root read full7133Breport.
Fresh sameimage/header53commands/unique__const section/raw80/file92773837/same64B
verified,18Root/21reviewer paths unchanged. The prior sectionguardSTOP remains
exact;44suffix bytes uninterpreted. Neither prefix nor leading digits is adopted
as an ABI-demangled type, runtime class or float-delivery contract.

Next metadata-only navigation selects exact substringAFloatEventInPort in the
top-levelname fields of existing aliases/vtables indexes only. Count-first20cap;
overcap stops before matching metadata, otherwise allmatchingidentifier metadata,
no sourcebody/text/otherindex/fallback/runtime. This is literal navigation only,
not a type/receiver/Unit/entry/publicMute association or absence finding.


The [two-index top-level-name query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-floatevent-name-index-frontier-2026-10-20.json)
reports zero selected matches: aliases420470eligible name strings; vtables80rows
with zero eligible top-levelname strings. No alternativekey/index/nestedfield/
body fallback was selected; sixprovider paths unchanged. Root currently carries
the author result only, not a fresh full independent metadata review. Zero means
scoped lookup availability, not a type or route absence finding.

Root next selects PREPARATION ONLY fixed64B[102311b5c,102311b9c),16ARM64rows,
at the already-reviewed251Cunit-construction entry. Metadata reports72native
bytes, which is not the selectedwindow extent. This asks about allocation/result/
hiddenreceiver carriers, not constructor/type/object identity from a label.
The inherited32Bdata collector's per-row byte-length check needs strengthening
in this NEWsuccessor: a3/5byte synthetic cancellation can evade aggregate-only
length checks. UTCTOR-PREFLIGHT-001 requires a focused old-accept/new-reject
fixture and eachrow exactly4bytes, alongside normalized validtype/opcode and
exact64B/cumulativeaddresses. Prior immutable method/actual captures remain;
this author-reported guard concern does not invalidate manually checked oldrows.
Root and peer fullcode preflight/separateactualselection remain necessary;
no Utilitywindowextraction/decoder/originalrun or behaviorgrade selected yet.


Root [independent name-index review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-floatevent-name-index-review.json)
now verifies the scoped zero result:420470alias name strings/zero matches and
80vtables rows/zero eligible top-level name strings. Seven paths unchanged;
no alternative field/index fallback or route/type absence inference. This
literal-name branch stops here.

The new64B construction preparation [passed Root full-code/check review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-construction-root-code-preflight.json)
and [independent full-code preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-construction-code-preflight-review.json).
Exact12literal changes reproduce the retained32B parent; each current row must
have4decoded bytes. Independent old8/count-only16 controls accept a cancelling
3/5-byte boundary counterexample; new16 rejects it. UTCTOR-PREFLIGHT-001 closes
only in the successor; old immutable method/captures remain unchanged and their
manually checked rows are not retroactively failed.29fixtures=2valid27bad,
7source guards and52watched paths passed. Root read full14747Bpeer report.

Execution qualifications remain explicit: collector inherits environment/stdin/
limits and does not itself set core0. The selected outer capture must enforce
and record core0/minimal environment/DEVNULL/PID/exit/timeout/cleanup and paired
maps. Inherited plan13:03 timestamp and fixture8matching label are historical;
current seal14:11 and operative16rows are distinct. Root separately selected
one fixed64B[102311b5c,102311b9c) extraction/pdj16 to Modulation; actual review
remains separate. No original Utility instruction/execution or behavior grade;
all38application outcomes remain unknown.


### Native construction input carrier — 2026-10-20

The selected64B construction capture [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-kind7-construction-instruction-data/manifest.json)
2674B/SHA1818eb3081d1c38d431b2c05e2ef65677ede666b33d2545986204d1afbdbaa8c
[passed Root independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-construction-root-actual-review.json).
Modulation authored the actual capture/assessment; Root coordinated selection
and independently checked all16native encodings, fresh same64B/image/header/
53commands/uniqueTEXT file36772700,10inner/11outer payloads and52/3128retained
paired maps/current identities. Root3150fresh watched paths unchanged. First
own scratch method failed at parse before execution; corrected own checks passed,
no supplied code/decoder rerun. Collector373372/decoder373377 exit0; outercore0,
minimal environment/DEVNULL/timeout55/no retry recorded. Original Utility runs0.

Conditional native fact: X20 copies entryX8, W0=104 zeroextendsX0 before
BL1012d9850. On normal return, MOVX19,X0 leaves X0 unchanged; the following
BL102328380 therefore receives that same first-call result in X0. This narrows
the recovered zero-argument call ambiguity; it does not establish allocation
success/extent, runtime class or public ABI. Post-second-call X0 need not equal
X19. With ordinary callee-save/validmemory/stack/reachability premises, stores
use savedX19 and entryX8-carriedX20. First[ X19 ] receives1067938a0, then[ X20 ]
receivesX19, then the THEN-CURRENT32bit[X19+8] increments modulo2^32. Output and
addressed region are not assumed disjoint. No initialcounter/refcount/ownership/
atomicity/thread-safety law follows. The [author addendum](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-construction-author-actual-assessment-addendum.json)
retains these order/alias qualifications. Last row is LDPFP/LR, no RET in64B;
remaining8metadata bytes were not selected or read.

Next selected PREPARATION ONLY is fixed32B[102328380,1023283a0)/8ARMrows at the
already-reviewed initializer. Its retained native metadata is56B; a proposed64B
selection exceeded that metadata and was resized before preparation/extraction.
Reuse strengthened per-row4B/type/opcode/accounting guards with literal changes;
no containment relaxation or forged metadata. Root/peer full-code checks and
separate actual selection remain necessary. All38application outcomes stay U;
no original execution, new clause/case/criterion/behavior grade.


Initializer [Root full-code preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-initializer-root-code-preflight.json)
now passes complete6917Bcollector/7915Bchecker,11inverse changes,29fixtures/
7sourceguards/88watched paths; no window/decoder run. The inherited plan label
before64B is historical wording; operative32B/pdj8/end3a0 are verified. Independent
preparation review and separate actual gate remain pending at this checkpoint.


Initializer [independent code preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-initializer-code-preflight-review.json)
now approves bounded readiness, no required findings. Root read full8128Breport:
11inverse operations/77pins/9oldparent files/8payloads,29synthetic controls/
7source mutations/fresh53command map/88paths unchanged. Copied before64B label
and historical timestamps remain qualified. Root separately selected one32B/
pdj8static capture to Synthesis with outercore0/minimalenv/DEVNULL/timeout55/
paired maps; actual status/adoption still requires independent review. No
original Utility instructions or new behavior grade.


The selected initializer32B capture succeeded; retained eight rows are undergoing
independent actual review. It calls102312d04 without a local X0 definition, then
uses returned/current X0 for literal and overlapping zero stores; no entry/result
identity is adopted from the author observation. Root separately selected only
PREPARATION of fixed200B[102323d98,102323e60)/50ARMrows at the previously retained
827C payload initializer. Existing metadata is200B, not a proven native extent.
The collector already admits equal containment; the checker-only strict> guard
will become>= with equal-boundary/overrun controls. No containment relaxation
beyond the retained bound, new helper/sourcebody/window or actual decoder run.


The initializer32B [actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-kind7-initializer-instruction-data/manifest.json)
3247B/SHAeaf145114e062fc429b6df379d732b2489982d7db305901ef88420c556bc8e79
[passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-initializer-static-actual-review.json).
Root read full8455Bauthor assessment/eight rows and7748Bpeer report. Ten actual/
11outer payloads,88inner/3171outer paired maps/current identities and3192reviewer
watched paths passed. Fresh same32B/header53commands/uniqueTEXT mapping and all
eight native bitfields independently verified. Wrapper377211/collector377219/
decoder377223 exit0, empty errors/no retries. The firstBL receives entryX0
locally unchanged; subsequent currentX0 is not equated to entry. STR64 writes
literal106798da8, STP64 zeros+50..+5f then STUR64 zeros+5d..+64, with overlap;
validmemory/normalreturn/reachability premises retained. No field/default/type/
object/extent/publicMute law, original instruction or further target read.
All38application outcomes remain unknown.


### Payload return carrier and base-entry gate — 2026-10-20

The selected200B payload [actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-kind7-payload-instruction-data/manifest.json)
3228B/SHA27ecd16734f7be588b139fd1bc45125214c791cb648907dd393eaf7313c21692
[passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-payload-static-actual-review.json).
Root read the full10525Bpeer report and all50retained rows, carrying the peer's
native bitfield/fresh same200B/header53commands/127inner3222outer paired-map and
3244current-path verification; Root did not independently replay that entire
verification or freshly read the full25979Bauthor assessment. Wrapper379867/
collector379868/decoder379880 exit0, empty errors/no retry; no original execution.

Before BL10128ed98 the prefix does not define X0. The post-first-call X0 receives
the literal106796e00 and conditional initialization stores. The common path
returns without assigning X0. Slow paths save X0 atSP+8 before opaque calls and
restore it before joining that common path. Thus visible joining paths preserve
the POST-FIRST-CALL value under normal returns, stable stack/saved slot, callee-save
X19, valid memory and no interfering alias premises. It is not yet the entry
receiver. Opaque global pointers/values, helper semantics and actual path remain U.
Raw pair fields verify SP+30 despite Rizin's displayed 0lr label; row10 is LDAPRB,
not a NOP. Neither display issue was patched or decoded again.

The separately selected [base-entry source query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-kind7-base-entry-source-frontier-2026-10-20.json)
retains complete144C at chunk00721:27, native metadata24B. Recovered void C writes
an address at+0,32bit zero+8 and64bit zero+16; it cannot establish native X0 return
preservation. No referenced global/callee was followed. Root selected only
[24B preparation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-kind7-base-entry-instruction-preparation/manifest-preparation.json)
for[10128ed98,10128edb0)/6rows. Its [Root code preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-entry-root-code-preflight.json)
passes29synthetic controls/2boundary controls/7unsafe mutations/168unchanged paths.
Independent source/code review and separate actual selection remain required.
No pointer-chain composition, public Mute law or grade is adopted; all38U remain.


The base-entry24B [actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-kind7-base-entry-instruction-data/manifest.json)
3252B/SHAe0b962d971d3ad1912bd9dc2b3addfa68c7fe59a4db537138bf4a5e41b4eb741
[passed Root independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-entry-root-actual-review.json).
Root verified all6native fields/fresh same24B/header53commands/10inner11outer
payloads/168inner3270outer paired maps. Own3285path watch stayed unchanged.
One unrelated unsealed Corpus driver draft changed after capture; the exact
historical pair remains valid and current drift is retained explicitly, not
misreported as a frozen-source change or future immutability. The [author addendum](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-base-entry-author-actual-assessment-addendum.json)
qualifies all seven concurrent draft snapshots. Wrapper385042/collector385043/
decoder385055 succeeded once; no errors/retry/original-code execution.

Selected six instructions form106662d50 inX8, store64X8 at[X0], zero32 at[X0+8],
zero64 at[X0+16], and RETX30. No X0 assignment or call occurs. Reached normal
straight-line execution with valid writable memory, stable code/no interference
and valid return therefore preserves entryX0. No referenced target data was read.

[Root conditional composition adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-carrier-composition-root-adoption.json)
reviews the [eight-step proposal](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-kind7-carrier-composition-conditional-2026-10-20.json).
Define F as the constructor's first-call RETURNED X0, distinct from constructor
entryX0 overwritten byW0=104. Reviewed prologues forwardF to the leaf; its local
preservation plus payload saved-slot/common-return and base-return facts associate
the SELECTED initializer stores withF. Normal calls, stable stack/control state,
valid accesses, saved slots, callee-saveX19/X20 and no interfering aliases remain
explicit predicates. This is a conditional carrier relation, not actual runtime
object/type/public delivery. No unselected initializer tail is required for these
pre-tail stores; native full return/tail65/67 remain unproved. Constructor later
stores use savedX19 regardless initializer-returnX0; an output alias can alter
F+8 before the counter load, so no initial-one/refcount/default law follows.
All38application outcomes remain U, with no new clause/case/grade/release.

Next selected work returns to the concrete nonlegacy Mute setter: exact decoded
source substring `param_1 + 0xcf` across the same pinned4185chunk population,
count-first20record cap, metadata-only all matches or over-cap stop. The reviewed
1047bd760 setter writes this field; matching text alone does not establish a
consumer/read role, same receiver or sound. No snippets/bodies/automatic cap
expansion, additional initializer tail or native/global/callee read is selected.


The first exact-prefix field search [stopped at179>20](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-state-cf-literal-metadata-frontier-2026-10-20.json)
without retaining matching metadata; it also matches longer hex spellings.
A separately selected closing-parenthesis predicate `param_1 + 0xcf)`
[stopped at32>20](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-state-cf-close-literal-metadata-frontier-2026-10-20.json).
A NEW40record-cap selection retained [all32 metadata records](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-state-cf-close-all-metadata-frontier-2026-10-20.json),
not a first-N subset. [Root independent navigation review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-state-cf-metadata-root-review.json)
freshly hashes4185chunks, scans418417JSONrows/418354code strings, reproduces both
counts and all32raw-row/code hashes/metadata, and verifies six context pins.
This is one finite independent pass, not an exhaustive reference/receiver/read
role or absence finding; equivalent casts/spacing/aliases can escape the predicate.

Root separately selected only complete4633C FUN1047bd790 at chunk03483:39 under
6000Ccap. It is an unreviewed candidate chosen from the exact-field metadata and
its adjacency to the known setter1047bd760; adjacency is a selection heuristic,
not same class/receiver/consumer evidence. No other body/callee/global/native or
automatic follow is selected. All38application outcomes stay unknown.


The complete4633C [candidate body](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-state-cf-1047bd790-source-frontier-2026-10-20.json)
[passed Root function-local source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-state-cf-1047bd790-source-root-review.json):
exact rawrow/metadata/seven spans/sevenpins verified. Its C projection tests bit0
atS+cf and immediately returns literal0.0 when set, before the shown two input
reads and state updates. Later packed CONCAT44/tiny-float mode comparisons remain
recovery notation, not an enum/arithmetic law. No explicit FUN_* invocation or
direct param2 destination write appears; aliasing remains possible. C returnzero
alone does not prove native channel ABI, buffer clearing, silence or public Mute.

A separately selected exact `FUN_1047bd790(` [metadata lookup](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-state-cf-function-reference-metadata-frontier-2026-10-20.json)
retains three textual matches, including the self-declaration. They are not yet
proved native callers. Root selected only the two complete non-self candidates,
10215ffbc/397C and named CalcMain wrapper1021658b0/556C, aggregate953C under2000cap.
They may clarify local argument/result consumption; names/text do not establish
actual invocation or processor identity. No other body/native/callee/global or
numerical follow selected; all38application outcomes remain unknown.


The two [result-consumer projections](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-state-cf-result-consumer-source-frontier-2026-10-20.json)
[passed Root partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-state-cf-result-consumer-source-root-review.json).
Full953C/sixclaims read; two rawrows/both LF hashes/code hashes/spans/eightpins
independently verified. First own check assumed a missing schema key and failed
before output; corrected lookup of retained preservation pins passed without any
source mutation. Both source calls pass base+48 and store recovered result at
base+40. The generic second base+44 store uses param2; the named wrapper uses
unassigned in_s1. Separate C locals do not prove stack adjacency, vector width,
second return/channel semantics or both outputs zero. Metadata is thunkfalse/
72native bytes for both, regardless informal callback-wrapper terminology.

Root now selects PREPARATION ONLY of fixed72B[1021658b0,1021658f8)/18ARMrows at the
named CalcMain wrapper, using strengthened per-row/accounting/containment guards.
Source-anchor keys change explicitly for the two-record query; no generic resolver.
Root/peer full-code preflights and separate actual selection precede any extraction
or decoder. No second caller/helper/native/global/callee follow, no original run;
all38application outcomes remain unknown.


### Native Mute result carriers — 2026-10-20

The fixed72B CalcMain preparation passed [Root preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-calcmain-root-code-preflight.json)
and [independent code review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-calcmain-code-preflight-review.json).
Root then separately selected one static capture at15:55:46–48UTC. The
[actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-mute-calcmain-instruction-data/manifest.json)
1949B/SHA78f01161ff5fadfc96ac6032476628ca0edcb66f162efbd0f2dcc898048d3ca1
[passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-calcmain-static-actual-review.json)
and [Root adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-calcmain-root-actual-adoption.json).
All18native instruction fields/fresh same72B/header mapping,10actual11outer
payloads and210inner3394outer paired identities checked;3415fresh reviewer paths
stayed exact. One decoder process, exit0, no retry or original instruction run.
Root read full author/peer reports and all18rows; fresh native-bitfield/header/
large-map verification is carried from the independent peer, not claimed twice.

Conditionally on valid memory/stack, normal helper return and callee-preserved
X19, the wrapper dereferences entry+30/+38 and places two32bit inputs at adjacent
SP+8/+12. It calls1047bd790 with X0=entry+48 and X1=SP+8, then stores current
S0/S1 to entry+40/+44. This resolves the native local layout and result carriers,
not helper output values, same public receiver, channel meaning or both-zero
behavior. Source names and72B metadata do not prove actual invocation or extent.
All38application outcomes remain unknown, with no new requirement/case/grade.

Root selected PREPARATION ONLY of the helper's fixed32B prefix
[1047bd790,1047bd7b0), eight rows. [Frozen preparation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-mute-core-prefix-instruction-preparation/manifest-preparation.json)
2043B/SHA69393610d01e0035f0a4b1d13a56009e11d7c1b45dd42c2133f1f5bf245a410b
[passes Root code preflight](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-core-prefix-root-code-preflight.json):
full collector/checker, exact11/23literal changes,29synthetic cases,three
containment controls,seven mutations and183unchanged paths. True metadata remains
744B ending1047bda78; synthetic containment acceptance of744 is not permission
to read744. Independent code review and SEPARATE actual selection are pending.
No branch destination, remaining712B, second caller, global or original run is
selected. The prefix may nominate a flag/branch path for later explicit selection.


### Conditional Mute zero return — 2026-10-20

The selected32B helper prefix [passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-core-prefix-static-actual-review.json)
6862B/SHA82c06be6e58b10f800015d02a0dfbff455012c2f88ae2318d2bb0c3562e5fbbc.
Fresh same32B/header/unique mapping/all eight instruction fields,183inner3410outer
pairs and3431fresh reviewer paths checked. It loads byte[X0+cf], zeros low64D0/D1,
and TBNZ tests bit0 with destination1047bda74. Not-taken input loads/multiplies
remain operand facts only. No destination or return was assumed from that prefix.

Root separately selected exactly4B[1047bda74,1047bda78) using a
[small data-only method](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-core-return-word-read.py),
with no decoder/process, rather than another copied collector. The
[five-payload packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-mute-core-return-word/manifest.json)
873B/SHA653575d409c4317ba70c70d70d0d6cedca230a42ec5ccb91cbd5f99ce5695b21
[passed independent word/path review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-core-return-word-review.json)
6640B/SHA14246409ad9a67d84e4dddf834f5a86cf96dd6e373a00a696a592f20328c8f36.
Wordd65f03c0 is RET X30; independent fresh image/header/unique mapping/same4B,
RET mask/BR counterexample and six paired inputs passed. This narrow read makes
no global preservation or general pretry/I/O guarantee. The immutable
[geometry addendum](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-core-return-word-review-geometry-addendum.json)
corrects the skipped interval to724B, including16already read and708unread bytes.
Prefix32+return4 leave708unread metadata bytes; no extra body read follows.

[Root adopts the conditional local path](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-core-return-root-adoption.json):
let M be the reviewed wrapper entry and K=M+48 its actual call operand. If bit0
of the byte loaded atK+cf is set, the selected helper path zeroes lowS0/S1 and
returns directly; the reviewed wrapper then stores32zero bits each atM+40/+44.
Valid receiver/input/output/stack accesses, reached entry and return, valid LR,
normal control flow/preservation and no interfering changes remain explicit
premises. This is a conditional local storage result. Actual public Mute delivery,
same model/Unit/processor identity, channel/audio meaning, timing and defaults are
not established. All38application outcomes remain U; no case/grade/release added.

Next Root selection is metadata-only discovery in the pinned main Live x86 slice:
count symbols containing StereoGainProcessor plus OnMute, and separately plus
CalcMain; cap20 per predicate, all matches or count-only stop. This nominates a
possible later extracted route, not instruction/function/ABI/public-binding proof.
No original Utility execution, body export, decoder or wider native read is selected.


The main x86 [two-predicate symbol lookup](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-x86-selected-symbol-metadata-2026-10-20.json)
19648B/SHA9bd461534822ef974cef5595bf6bbb2cd49fafbf3be2edece7127faeedf861f3
[passed Root independent metadata review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-selected-symbol-root-review.json).
All81311nlist rows yield exactly one match each: OnMute10224e760/index70756 and
CalcMain10224ef20/index70768. Exact raw/mangled names,16B nlist records and section
metadata are retained; no demangling or counterpart/ABI/type proof is inferred.
Main universal313453600B/52289af6…35ef and existing x86 slice163716848B/
1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0 are pinned.
Root freshly checked nine providers, header/command/table/string hashes, all
predicate counts and both records; segment/section interpretation is carried
from the fully inspected method. Mutable source-page hashes are as-of context,
not future gates. No instruction was selected in this metadata operation.

Root selects PREPARATION ONLY of OnMute's physical240B prefix at10224e760,
pdj16 with variable1–15byte instructions and opaque unconsumed suffix. Use the
existing x86 prefix method with fixed main-target/header/destination pins; no
native extent assumption, second wrapper or call/branch destination follow.
Root and independent code preflights then a separate actual selection are required.
No extraction, decoder or original function call is currently selected.


### Reviewed x86 conditional Mute store — 2026-10-20

The separately selected OnMute static prefix at16:35:02–03UTC passed
[independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-onmute-static-actual-review.json)
6909B/SHAcadb996edbd08d7aa3a7744d997a509e3f1ba6c5d0d0a94ce5d67c6cf888eee7.
The240B physical window yielded16rows/55B; unused185B were initially opaque.
One decoder attempt, outer/collector/decoder0,52inner/3495outer identities exact;
3518fresh reviewer paths checked. All16instruction operands were independently
checked. This was decoding data; no original Utility instruction ran.

Under reached entry, valid memory/stack/control and no floating exception,
comparison-derived CL stores atP+161; byte[P+162] selects the branch. The unequal
branch forms a masked lowESI carrier and RDI=P+48. No actual floating outcome or
ABI/public receiver is established. Six separately selected retained bytes
5de9c3df9302 [passed jump review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-onmute-continuation-review.json):
POP RBP then JMP104b8c760. Remaining179window bytes stay opaque.

A new eight-byte target read554889e54088b7cf intentionally stopped UNKNOWN:
prologue plus incomplete instruction. Its [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-setter-data-review.json)
preserves that result. Five separately selected completion bytes0000005dc3
[passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-setter-completion-review.json)
3988B/SHAe7421e4108cdc6923084a9a3d92c2564ddeeb0a41eb0428abdfb7b41924472dd.
Together13bytes encode PUSH RBP;MOV RBP,RSP;MOV byte[RDI+cf],SIL;POP RBP;RET.
REX40 makes the byte source SIL. [Root adopts only the conditional local path](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-local-path-root-adoption.json):
valid reached unequal path, preserved carriers, valid stack/memory and normal
return give store address(P+48)+cf=P+117. No actual value/object, public delivery,
channel/audio meaning, defaults or arm64 equivalence follows. All38application
outcomes stayU. The earlier strict UNKNOWN packet remains immutable.

Root separately selected [CalcMain PREPARATION ONLY](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-mute-x86-calcmain-entry-preparation/manifest.json)
1498B/SHA68b37b95e054245c1cbda56096b310b3e2b5577756d03a462437c9a1439a52b1:
existing nlist70768 nominates10224ef20, fixed physical240B/pdj16 with opaque
suffix, same reviewed method and main-image/header pins. No target window or
callee read yet. Root/peer code review and separate actual selection remain
required. No original Utility execution, grade, case or release was added.


### Reviewed x86 processing wrapper and flag frontier — 2026-10-20

The separately selected CalcMain static prefix ran once at16:59:36–38UTC and
[passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-calcmain-static-actual-review.json)
5073B/SHA5cb348cd252efdb4ea4c7fbd364bdb24d47db9a94ff67d532b011cfb2f963bc9.
Actual manifest1915B/SHAa6c83940fb33caa579a411101aa67609b2401ab4a743159e8c53bef775be752f
retains12payloads;70inner/3585outer pairs and3609reviewer identities checked exact.
Outer406454/collector406455/decoder406457 exited0, no retry or original instruction
execution. The peer qualifies an earlier preparation-parent attribution: OnMute
preparation was Delay's; current CalcMain preparation is Synthesis's and actual
selection is Root's. This does not alter evidence bytes or current independence.

All16rows occupy56B of the240B physical window;184B stay opaque. Under valid
memory/stack/nonfaulting accesses and normal preserved registers, receiver is
saved inRBX, RDI becomes receiver+48, two pointers load from receiver+30/+38 and
two32-bit values copy into adjacent RBP-10/-c. RSI addresses that pair. The direct
call nominates104b8c7b0. On normal return, MOVLPS stores low64XMM0 at receiver+40.
The prefix ends after ADD RSP8; no full return, actual value, helper output,
public delivery or audio law is established. All38application outcomes stayU.

After reading the complete peer, Root separately selected exactly32B at
104b8c7b0 as [raw data only](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-mute-x86-process-prefix-data/manifest.json),
using the existing fixed data-reader method without a decoder or target call.
Independent encoding review is pending; no branch destination or continuation
was selected by that read. The full original target did not execute.


The32B helper prefix [passed independent encoding review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-process-prefix-review.json)
3506B/SHAeefb29b3758600831bd4ae7c9255bd2173ecf31535f9fb65da263c4fdd34f8f1:
XORPS clearsXMM0; CMP tests the full byte atRDI+cf against0; JNE nominates104b8cb37.
Seven complete instructions occupy30B; the final0f87 remains incomplete and
uninterpreted. Root separately selected exactly one byte at the nominated
branch destination. That [independent return review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-process-return-review.json)
3787B/SHAb98fd74af52e4ff77e0006d0f5da8824e0cb436d66890947aa2c363612c3a35b
confirms C3 nearRET. Five fixed input pairs and11reviewer identities stayed exact;
no decoder or original instruction ran. Under reached entry, valid nonzero flag
byte, normal caller stack/return and no interference, the selected path returns
low64XMM0 zero. With the separately reviewed wrapper's own preservation/validity
premises, it stores two zero32-bit words at receiver+40/+44. This is conditional
machine behavior only. X86 tests full byte!=0; ARM tests bit0, so no architecture
or public Mute equivalence is inferred. All38application outcomes remainU.

The existing [owned-buffer harness feasibility query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-xexec-owned-buffer-feasibility-2026-10-20.json)
and [source/recipe provenance addendum](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-xexec-source-recipe-provenance-addendum-2026-10-20.json)
identify a sufficient existing integer/buffer/low64XMM protocol without a new API.
Current source differs from X1 only by the77B256-call guard; current loader binary
is not byte-identical to X1, and source-to-binary binding remains unproved.
No MXCSR control/readback exists in the inspected protocol. Root selects only
preparation of one owned loader reproduction build with the existing recipe and
an exclusive new output; no default binary overwrite, loader or original call.


The existing-recipe owned loader build passed Root and
[independent code review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-xexec-owned-build-code-preflight-review.json)
before a separate compiler selection. At17:13:50UTC outer441834/collector442600/
gcc442687 exited0; one compiler attempt, empty compile stdout/stderr. The
[actual build packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-xexec-owned-build/manifest.json)
retains a74040B new binary, SHA5d236b76351b3a30f56addd37305e8e8935a34ba959fd9be0873cd84886d5385,
exact whole bytes equal to the old loader.16inner/5102outer paired identities
remained exact; a finite post-group check found no residuals. This binds the
reviewed current source and existing command to new output under ordinary build
premises; transitive build dependencies are not hermetic. Independent actual
review is pending. Neither loader copy or original instruction ran.

Two Root setup errors preceded any collector/compiler attempt: the wrapper
inverse check used an overlapping filename prefix, and Root then prematurely
invoked that draft before inspecting the failure; it stopped at missing selection
JSON before Popen. Both are [retained](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-xexec-owned-build-selected-execution/preselection-setup-failure.json).
Exact assignment literals fixed the inverse check without changing draft wrapper
bytes. A separate frozen selection then preceded the sole compiler attempt.
There was no compiler retry, source/default-binary overwrite or normalization.

Root next selects PREPARATION ONLY for a fixed two-call X question with this
existing loader: set bytecf=1 in an owned208B buffer using the reviewed setter,
then call the proved nonzero-flag helper path with that buffer, an owned8B input
and nonzero incoming low64XMM0. Fixed mapped-code dumps would bind only the
already retained13/16/1bytes; low64return and bounded owned-state dumps would be
recorded. No alternate flag path, initializer, constructor, model/global or
application execution is selected. Build actual approval, Root/peer method/code
readiness and a separate Root invocation are still required. The preparation
adds no harness API or FP-control promise; all38application outcomes stayU.


The [independent owned-build actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-xexec-owned-build-actual-review.json)
4705B/SHA400593ad00d0cbc415eb1e28e93c45345e4ea52095b4b7a9d73a3b3d7423dc20
approves that finite source/command/output event, with11actual/13outer payloads
and5126current reviewer identities exact. Root read the full peer and adopts
that limited result. No historical build event, runtime import/ABI/bounds/FP or
public Mute behavior is proved. Existing xexec has no pause between code dumps
and calls; future mapped-code comparisons would be post-hoc only. Prelaunch
exact image/source/binary pins and explicit control premises remain distinct.


### Reviewed owned-buffer x86 mute capture — 2026-10-20

**Observed, extracted execution:** the separately selected two-call study ran
once at17:29:52–53UTC. Outer755905/collector755906/original xexec755908 exited0;
there was one original child and two completed original function call-return
rows, without retry, timeout or forced kill. The [actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-xexec-mute-zero/manifest.json)
1576B/SHAa2f1315358806cd39d406982d6c713d3245246f6e6b8d5ba4c550fc9091e8ad9
and [independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-xexec-mute-zero-actual-review.json)
7377B/SHA5f45fbc335c2b91e37b958ad44863285bf8ed95aac3a4632a1fc7e9df9a44678
retain exact methods, commands, identities and raw results. Root read the full
peer and adopts its bounded result:28inner/5116outer paired identities and5138
reviewer paths unchanged; finite post-group observation found no residuals.

The reviewed newly reproduced loader first called104b8c760 with an owned208B
zero-initialized buffer and integer1, then104b8c7b0 with the same buffer, a distinct
owned8B input0000803f000000c0 and protocol d:0x1p+0. The after-setter and after-helper
state dumps contain only bytecf=1; the input dump is unchanged. The helper return
row records low64XMM0 zero. Buffer zeroing before the first call is source-bound,
not a separately captured initial dump.208B is sufficient for this selected
nonzero-flag path, not a recovered object size. The incoming FP token specifies
nonzero low64 bits with low32 zero; no incoming register trace or upper64XMM
return was captured. RAX/RDX and the setter return are not audio conclusions.

The three mapped13/16/1byte dumps match the previously retained setter/helper/RET
bytes **post hoc**; the protocol has no pre-call comparison barrier.1882unique
import rows report103Linux/42781trap slots and no positive used rows; these are
resolver instrumentation, not exhaustive proof of absence of import work or
current import target identity. No MXCSR control/readback, public receiver,
channel audio, wrapper delivery or general off-flag behavior is established.
Expected/comparison fields remain null; all38application outcomes remain unknown,
revision2 requirements/cases unchanged. Whole Live did not execute.

**Next static method:** one [owned four-byte decoder fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-byte-count-json-fixture/manifest.json)
1910B/SHA79f62c51a089d781fcc2faff41dbf2c4981eff1ca6a62a9962c98b113e5a7512
ran at17:36:10UTC, PID771183exit0, using pDj4 on separately owned bytes
90/6690/c3. Three rows concatenate exactly four bytes. Root's
[independent fixture review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-byte-count-json-fixture-root-review.json)
checks all12payloads/four paired identities without replay. This validates one
bounded command observation only. Root selected preparation of a fixed904B
static span[104b8c7b0,104b8cb38) with pDj904;904 is a physical study cap, not a
native function extent or complete control-flow proof. Preparation adds no
original call and requires code review and separate actual selection.


### Reviewed x86 processing span and table frontier — 2026-10-20

After Root and independent code preflights, one separately selected static decoder
at17:48:18–20UTC returned0: outer786874/collector786877/decoder786886. All203rows
concatenate exactly904B in[104b8c7b0,104b8cb38). The [actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-process-span/manifest.json)
1885B/SHAf7ffec77a3edd07e2d200d2fa733f7b827e323ab8bb96a13815b0876a50c0da2
[passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-process-span-static-actual-review.json)
4757B/SHA86bd24a65e14f77aff90ee7a21242e408f8bab4a81b35f4e517b26ed1fb8e4fb.
Root read the full peer:12actual/12outer inventories,100inner/3128outer pairs and
3152reviewer paths exact. No retry/timeout/kill/original instruction; finite
post-group snapshot empty. Physical coverage is not a native extent or full CFG.

The native key-field review confirms dword[RDI+c8] zero-extends into RAX, an
unsigned compare against3, then LEA base104b8cb38, MOVSXD signed32[base+index*4],
ADD base and JMP computed target. The table lies outside904B and was not covered
by that decoder. After the peer, Root separately selected exactly16B as data:
[table packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-mode-table-data/manifest.json)
657B/SHA3d38fcd0a7ea36b10e70763b1f7c8b210480f8f4c85d84c4f8ffe7048df631ec.
Four signed little32 words give offsets -841/-819/-832/-823; base-plus-offset
expressions are104b8c7ef/104b8c805/104b8c7f8/104b8c801. Independent literal/native
expression review is pending. No new target bytes were read and no original instruction executed.
This simple data read has no standalone child PID/command receipt.

Next source study is the conditional numeric-index1 path using retained span and
table only: identify exact owned-state accesses and finite pair result under
explicit state/FP premises. It selects no original invocation or public default/
control-name mapping. The earlier one-child/two-call mute capture stays the only
Utility original execution in this continuation; all38application outcomes stayU.


The [table literal/expression peer](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-mode-table-review.json)
3342B/SHA67e9152452c0c7e7ad0d3487309a9d0872f936c93d3671b11b36277c4f7cfd20
approved the four words and reached unsigned0..3 index gate. Root read it fully;
five recorded input pairs and11reviewer identities unchanged, no new target read.
The [conditional state query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-x86-mode1-owned-state-source-query-2026-10-20.json)
and [positive-step companion](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-x86-mode1-positive-step-source-companion-2026-10-20.json)
[passed independent Root source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-mode1-positive-step-root-source-review.json)
1784B/SHA32d9406b8e1e161a53e84f059e78a59582954092061f7f38c50f22b675952094.
With explicitly chosen208B owned state, separate8B input, index1/flags0, balance
pair[1,1], width pair[1,0]/zero step, common pair[1,1]/step[.5,.25] and counters0,
two reached nonfaulting ordinarySSE/SSE3 calls conditionally use OLD common gains
for outputs[1,-2] then[1.5,-2.5]. The updated common pairs[1.5,1.25] then[2,1.5]
are stored for later calls; counters+48/+88 become1 then2. Source-ordering is
explicit: load old pair, add/store updated pair, multiply with old register.
These exact finite operations avoid a cancellation-zero sign assumption; ambient
MXCSR remains unmeasured. They are source algebra, not observed output or a new
numeric oracle. A subsequent nonzero-cf entry conditionally returns zero before
reading input or advancing these fields, under the separately reviewed early path.

Root now selects only preparation of one four-call history in the existing owned
loader: helper, helper, setter1, helper; bounded state dumps after each and final
input dump, fixed post-hoc13/920mapped-byte checks against retained setter and
904+16span/table. No new harness API/build, constructor, public binding, FP control
or original invocation is selected. Protocol validity must retain differing state
or return values as counterevidence. Expected/comparison fields and application
grades remain unchanged; all38application outcomes stay unknown.


### Reviewed owned-state history and public-binding gap — 2026-10-20

**Observed, bounded original execution:** the fixed four-call history ran once
at18:05:44–45UTC, outer857997/collector858014/originalxexec858017 exit0. The
[actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-xexec-chained-state/manifest.json)
1581B/SHA63846593390a469fc9883f8c574b2b67a72c59739a98e5704feda92140c5d4e4
[passed independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-xexec-chained-state-actual-review.json)
8142B/SHAafb68e38e0e38b9283953a58f3187ff3fc3d7f9043e1f03802dea249c94717bf.
Root read the full peer and adopts the finite observations:10actual/12outer
payloads,48inner/5136outer pairs and5158reviewer identities exact, no retry,
timeout, forced kill or observed group residual. The unchanged reviewed loader
made helper/helper/setter1/helper calls with the prescribed208B state and8B input.

Returned helper low64words are c00000003f800000/c02000003fc00000/0, decoding as
binary32 pairs[1,-2], [1.5,-2.5], [0,0]. Dumped common pairs progress from
[1.5,1.25] to[2,1.5] on the first two calls, then remain[2,1.5]. Both selected
counters progress1,2,2,2. Setter changes only observed byte207, and the final
helper's entire208B dump equals the post-setter dump. These agree with the
source question at these inputs; numerical differences were never a protocol
validity filter. Expected/comparison remain null and no criterion/grade is added.
The input dump after call0 equals the final dump; no pre-first-call state/input
snapshot was captured. Initial values are bound by argv/loader source only.
Mapped13/920bytes match retained13/904+16bytes **post hoc**. Import instrumentation
remains1882symbols/103Linux slots/42781trap slots with no positive used rows,
without an exhaustive absence-of-import-work or target-binding claim.

This continuation now has **two Utility original children/six returned calls**.
All38application outcomes remain unknown: owned208B is not a real object size;
no public enum/default/gain/smoothing/timing/FP-control/ARM equivalence follows.
No more internal numeric examples are selected. The [canonical-only frontier](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-public-binding-minimum-frontier-2026-10-20.json)
identifies the missing public-value delivery and same processor receiver between
registered OnMute and CalcMain; alternatively a concrete consumer of receiver+40
into a host output buffer is missing. Its mutable-page as-of prefix/anchor check
explicitly excludes a concurrent append from whole-file equality.

Root selected only bounded main-x86 symbol metadata for class tokens AStereoGain
and OStereoGainProcessor, cap96each/count all before retention. The frozen query
is awaiting independent review. Names alone cannot equate the model and processor
classes; the existing OnMute/CalcMain entries are detail::TMemberFuncTypes
OStereoGainProcessor callback thunks. No new callback/body/host claim follows.


The [class-token metadata query](../../analysis/ableton-live-12.4.3/full-spec-v1/queries/utility-mute-x86-class-token-symbol-metadata-2026-10-20.json)
[passed independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-mute-x86-class-token-symbol-metadata-review.json)
6475B/SHAb743a6990399e876501a51560ed9a62624ecb9aa332c29e24c5dcbd9d8ee96cd.
Root read the full10046Bmethod, complete compact40rows and peer: all81311nlist
records counted first, yielding6AStereoGain/34OStereoGainProcessor matches below
cap96each, all40rows retained;13provider identities/15reviewer paths unchanged.
Matches include View/Reduction and typeinfo/string records, not40callable methods.
Raw nlist178 names SNewCompoundI11AStereoGain at10309e0f0;8568 names
OProcessorCreateManager::SOnProcessorCreateI20OStereoGainProcessor at1022313c0.
These are names/values only. Root subsequently selected the fixed240B/pdj16
entry-prefix decoder before the plan revision4 steering arrived. The retained
[static capture](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-processor-create-entry-instructions/manifest.json)
completed at18:20:01UTC, exit0:16rows occupy47bytes [1022313c0,1022313ef), leaving
193selected bytes uninterpreted. Its local calls name101ad08a0 and102231400;
neither callee was followed. The actual-result independent review remains
pending; this capture is not behavioral evidence or original instruction
execution. No public creation role, class equivalence, complete function extent
or executable ABI follows. The amended plan now selects component recovery
before integration; this local frontier selects no successor.


### Processor-create prefix Root readback — 2026-10-20

The retained [240-byte capture received Root readback](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-processor-create-entry-root-readback.json):
all 12 payload hashes, identical recorded before/after watch maps, the header-map
pin, exact source-image range and all 16 decoded row bytes match. The two relative
call encodings independently give `0x101ad08a0` and `0x102231400`. Only 47 bytes
are decoded; 193 selected bytes remain uninterpreted. This is Root result
readback, not a separate-worker semantic review. Independent actual-result
review remains pending. No original instructions ran, no decoder was relaunched,
no public behavior gained evidence, and neither callee is selected for expansion.


## Utility family route inventory — 2026-10-20 (pending review)

The [bounded Utility route map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-utility-routes-v1/structure.md)
extends approved integration I07/I08 with retained device/model/enrollment,
registered callback, processor-state and owned-buffer evidence. It is pending
independent structure review and Root seal. Its current15-requirement observable
inventory distinguishes documentary UI/audio relations and explicit lifecycle
unknowns from two retained-file predicate families (three historical checks). All38application case outcomes
remain U; current Version12manual applicability is not exact12.4.3 evidence.

The two reviewed original children/six returned calls remain finite owned-state
X evidence, indexed as route dependencies rather than public Mute acceptance.
No actual public control→same processor receiver→host output bridge is closed.
Stored presets do not prove defaults/load/save/legacy migration. The earlier
processor-create240Bprefix has only Root readback,193opaque bytes and unpursued
callees; it is not independent actual-result approval. The map selects no
execution or source expansion and changes no requirement, case, grade or release.


## Utility family route review approval — 2026-10-20

The [independent structure review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-utility-routes-v1-review.json),
SHA256 `9f5eae3321459d52a2845300e57e2bce50c554c14b228a363a3939a003951da5`,
approves manifest `e2c0aa18109c53514368ba256634ad31d7ee4077f41d938d5723dd0463867652`
as bounded structure only. All 48 predicates/15 requirements are represented:
two retained-file S routes, 46 missing complete exact-target public routes and
zero X. All 41 case objects are navigation; all 38 application outcomes remain
U. The three historical file checks differ from the two stored-file predicates.

Selected source/provider/case/manual spans and the two owned-state histories
were checked as retained data, not rerun. D/G/U/E/P/M/S identities, per-read
vptr/path premises, actual model admission/callback/result-cell-to-host joins,
708 unread versus 724 skipped bytes and the 240-byte prefix/193 opaque bytes
remain qualified. Current-manual D12 is not exact-target evidence. Existing
six local returns are auxiliary X, not public outcomes or new grades.

The earlier pending-review map append is author history. No original/native/
model/callee/source expansion, norm/case/release/grade or complete profile
follows. Independent review of the already captured pre-steering prefix is
now assigned separately; this map approval does not supply that disposition
or select a callee. D03 and all public binding/audio outcomes remain open.


## Processor-create prefix independent provenance approval — 2026-10-20

Root read the complete [separate actual-result review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-processor-create-entry-actual-review.json), SHA256 `da6d7ae634038e90b906edcdaabcd1be314317ce1a30b0d88da4ac3a1974919d`. It approves only the already retained static capture/provenance: manifest `dfd4534450a0570cb293395b8c7414775e7e0b62bc00fb922b1860fe4c3cce73`,12payloads/60,329bytes, sixteen rows occupying47of240selected bytes. The remaining193bytes remain opaque. The independent reviewer compared exactly the selected240source bytes, checked retained header geometry, encoded rows and both relative-call targets, and rejected six malformed-data controls. Recorded watch maps were compared as data; their underlying universes and the full image were not replayed.

The earlier pending-review statements and Root readback retain their dated historical meaning. No original instructions ran, no decoder/provider was relaunched, neither callee was followed and no creation/ABI/receiver/public behavior, case or grade is established. This review selects no successor. Root separately selected one retained-data whole-frontier batch across the approved map's six missing public-binding bridges; source absence remains unknown rather than native infeasibility. All38application outcomes and D03 remain open.


## Utility public-binding whole frontier — 2026-10-20 (pending independent review)

Root selected one [retained-data static batch](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-public-binding-frontier-v1/structure.md) across all six G01–G06 gaps in the approved Utility family map. It follows the current amended revision4 selector and the separately approved processor-create prefix provenance. No original/native/provider/decoder/harness/model/comparator/fixture/build operation or callee successor is selected. Earlier pending prefix/map descriptions above remain dated history.

The [whole-frontier ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-public-binding-frontier-v1/frontier-ledger.json) keeps all six bridges unknown: host graph→actual Utility admission; public current value→same registered callback; OnMute receiver→same later CalcMain receiver and order; result cells→host output; stored state→active load/default/migration/lifecycle; and local x86→ARM/public equivalence. Constructor-like code, declaration/list/resolver/enrollment, builder callback and kind7 binding add conditional local associations, not actual instance/value delivery. D/G/U/E/P/M/S and owned/host buffers remain distinct. The registration callback receives a builder object; that is not OnMute(P,F). Private +328 selects a role and is not the current public Mute float. Stored names, vptrs and equal offsets do not prove receiver identity or preservation across calls.

[Exact retained queries and locators](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-public-binding-frontier-v1/query-records.json) reference74 C records/73 distinct entry+codehash pairs,26 exact C searches,five metadata searches and one selection over the24 existing class-slot records. Eleven C queries,one constructor-spelling metadata query and the selected class-slot query have zero matches in their stated finite sets. No match is a native absence or infeasibility proof. Nominal Init/Reset/NewRate/legacy symbols do not define lifecycle behavior. Exact missing source frontiers remain unselected; neither processor-create callee is followed. Forty-seven decoded prefix bytes and193 opaque selected bytes remain separate.

The predecessor48predicate inventory,41case objects,two retained-file S routes and38 application outcomes U are unchanged. Six frontier units,21qualified local associations,source records and query counts are not new outcomes or grades. Existing two owned-state children/six original returns remain auxiliary and ungraded; no additional numeric examples, portable law, class/ABI/creation success or public compatibility follows. ARM bit0 and x86 whole-byte tests remain distinct; generic TrackOut ports do not identify a result-cell consumer. Control composition,clock/order,load/save,legacy,hotswap,undo/deletion,suspension,failure and rate/block boundaries remain unknown.

The [data-only author check](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-public-binding-frontier-v1/author-check.json) checks selected identities/source pointers/query results,all six predecessor gaps,prefix preservation and14 false-promotion controls. This additive batch is pending independent review; Root owns its shared atlas/index/coverage/log adoption. No owner,case,criterion,release,grade,indirect-site credit or successor changes.


## Whole Utility public-binding frontier approval — 2026-10-20

Root read/adopted the complete [independent whole-frontier review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-utility-public-binding-frontier-v1-review.json), SHA256 `c824d7177469d50aa2e3e5bace537e60342a8256d17a41c6857976a4352b4c33`. It approves manifest `318c86299090666d6e99d8c0c2a2571afc3370df6030a960b9f825d187e4203c`,eight payloads/139,499bytes as bounded retained-source/query reconciliation. All six G01–G06 bridges remain unknown; no complete public route, indirect-site or grade is added. All38application outcomes/48family predicate rows remain qualified.

The reviewer checked49immutable pins/74C references/73entry-code pairs,26C queries, five nlist queries, one24-row class-slot query,21association pointers and14false-promotion controls. Eleven C queries and one metadata query returned zero; the class-slot query found zero matches. These are bounded results, never whole-program absence. Selected full bodies/spans were reread; prior full73-body semantics and earlier native/owned-state/capture evidence remain inherited.59watched paths and the133,664-byte research prefix/3,395-byte append remained exact. Plan identity advanced as mutable as-of context; it was not used as a live hash gate.

Metadata getters/declarations do not supply actual current values; builder registration is distinct from OnMute(P,F); U/E binding does not prove the callback consumer; equal offsets do not identify P/M or host buffers. Actual model admission/current value, receiver/order, output, construction/load/legacy and lifecycle relationships remain open. The earlier pending section is author history. No new source expansion, callee/global/slot selection, binary/native/provider/decoder/harness/original/model/comparator/fixture/build execution, owner/case/release change or completed profile follows.


## Utility class construction/lifecycle source frontier — 2026-10-20 (pending independent review)

Root selected one [supporting class-level source batch](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-class-construction-frontier-v1/structure.md) across all six existing Utility public-binding gaps. Exact retained1a metadata yields five table prefixes/87slot records and three store candidates; these are not complete tables or class instances. Six fixed C1 records passed metadata-first bounds:3,198expanded C bytes total,max38lines per record,within6records/32,768Cbytes/300lines per record. Four selected chunk hashes match the approved1a pins. Exact new records occur once in the packet; no other slot/callee/global/native body is expanded.

The [source facts and role assessments](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-class-construction-frontier-v1/source-facts.json) distinguish initialization-like10215f2b8 from its4-byte thunk10215f3d8,which the exporter expands to repeated C. The returned base B receives a processor-vptr operand and helper argument B+0x48; separate param1/Q field writes do not prove B=Q or an actual live processor. A reached zero store spanning Q+0x15f..0x162 does not establish current public Mute/default/branch state after unread helpers. Model102f4fadc installs four address points on one returned base at0/0x50/0x58/0x1b8,consistent with retained RTTI offsets-to-top0/−80/−88/−440; its lifecycle role and actual model identity remain unknown.

The10216412c/10216416c projections are cleanup/deletion-shaped inferences,not constructor evidence:they replace a vptr operand,call an unread helper,clear field+0x20 and call another unread helper. The latter passes that helper's return to operator_delete,not an explicitly identified incoming receiver. Formal destructor,ownership,actual teardown/Undo/error and vptr-continuity laws are not established.101aa4b90 is return-only in recovered C; no callable ABI or machine-state guarantee follows. Five nonthunk records are metadata units,not five newly validated implementations.

[Exact existing call-index associations](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-class-construction-frontier-v1/call-associations.json) retain four fixed-target matches,including caller10214b954→thunk10215f3d8. These are prior index sites,not newly native-confirmed PCs or indirect credit. That caller's body/arguments remain outside selection; proximity to another create-related address proves no association. Zero exact direct-call spellings in the prior73C-field set are bounded results,not global absence or infeasibility. Neither this caller nor any encountered callee is selected for follow-up.

The [six-bridge reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-class-construction-frontier-v1/frontier-ledger.json) keeps G01–G06 unknown:actual construction/admission,current-value callback delivery,sameP/M receiver/order,result-cell→host output,load/default/legacy/lifecycle and ARM/x86/public correspondence. All38application outcomes and the48family predicate inventory stay unchanged. The [read-only data check](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-class-construction-frontier-v1/author-check.json) validates caps/source/metadata/span/prefix identities and14false-promotion controls. No new binary/native/provider/decoder/harness/original/model/comparator/fixture/build/install operation,numeric helper example,owner/case/release/grade or successor follows. This additive packet awaits independent review; shared routing/log/index/coverage belong to Root.


## Utility class construction source review approval — 2026-10-20

Root read/adopted the complete [independent class-source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-utility-class-construction-frontier-v1-review.json), SHA256 `567df4c6af2df0e9dddd693c39b18092b303b14d48db5007d0e3f99ecdcb4d6f`. It approves manifest `5c53a7ec4d2b998294d83ebb8aab091cc7f4384be47c825af444ceea10a91e10`, eleven payloads/72,018bytes, six retained C records and five table prefixes/87slots as bounded source relationships only. Six records total3,198Cbytes/max38lines; four approved chunks,16pins/eight spans/six aliases and selected table/store/call slices were checked with14negative controls. Twenty-nine paths/eighteen slices and the138,953-byte research prefix remained exact.

Initialization-like, cleanup-shaped and deletion-shaped roles remain distinct inferences. A returned base B is not identified with supplied Q/P; expanded4-byte thunk C is not a second native implementation. The zero span Q+0x15f..0x162 and helper calls establish no public Mute/default/final state. Model address-point installation is conditional layout evidence, not actual model admission. Incoming receiver versus returned deletion pointer, ownership, ABI and host lifecycle remain unknown. All six G bridges,38application outcomes and48family predicate rows remain unchanged; zero new sites, grades, clauses, cases or releases follow.

Root separately selects one bounded retained-C1 batch across the base-return and creation frontier: entries `101bc3aa0`, `1023a1004`, `101aff380` and `10214b954`, metadata first, at most four records/65,536Cbytes/500lines per record. It supports all six existing gaps rather than another numeric example. No encountered callee/global/slot/body or old x86 prefix callee is automatically selected. No binary/provider/decoder/harness/original/model/comparator/fixture/build or install operation is selected. The pending section above retains its author-time meaning.


## Utility base-return/creation source frontier — 2026-10-20 (pending independent review)

Root selected the fixed four retained C1 bodies for one [whole-six-gap supporting source batch](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-base-creation-frontier-v1/structure.md), following the approved class-source review above. [Metadata-first bounds](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-base-creation-frontier-v1/metadata-gate.json) passed before C text was displayed: four nonthunk records,3,544C UTF-8 bytes total,max85lines,within4records/65,536Cbytes/500lines per record. Four selected chunk hashes match approved1a pins. Recorded native extents12/64/128/488bytes are retained export metadata,not new instruction reads or full-function/ABI proof. Exact raw records occur once; no other callee/global/slot/body is expanded.

The [ten source facts](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-base-creation-frontier-v1/source-facts.json) expose a projection boundary:101bc3aa0 initializes internal V from an unread helper,but its own C declares void and ends bare return,while earlier10215f2b8 consumes that call as B. Neither native return/implicit incoming registers nor B=V=Q follows; C void is also not proof of native no-return-value.101aff380 explicitly zeroes20bytes. Substituting the nine retained caller arguments yields disjoint20byte intervals at Q+0x168 through Q+0x228,excluding Q+0x15f..0x162 under source/valid-memory premises. This narrows one explicit-store interference concern; it establishes no actual invocation,preserved active flag,current public Mute/default or Q=P=M.

Caller10214b954 obtains H from an unread helper with0x28 operand,passes a loaded field at H+0x18 and its two arguments to the known thunk,then calls an unread helper and returns H. The existing selected index row associates the thunk with10215f3d8/resolved10215f2b8; it is no new native site. Three caller arguments versus two named target-projection parameters leave native argument/control correspondence unknown. H,its field and size-shaped literal prove no allocation success,ownership,public factory or Live instance. Address proximity does not equate this caller with10214b918.

Model/base1023a1004 writes through internal V from an unread helper and separately through incoming T; V=T is unknown. Reference/callback-shaped expressions and fields+b8/c0 are not actual parameter lanes or host buffers. Its own source returns T,while earlier102f4fadc consumes a no-named-argument call; native argument/return mapping and outer B=T remain unresolved. Callback symbol/lambda operands are data,not delivered values,AB/Undo semantics or lifetime guarantees. Formal construction/destruction roles and helper success remain unknown.

The [six-bridge ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-base-creation-frontier-v1/frontier-ledger.json) keeps actual construction/admission,current-value delivery,same receiver/order,result-cell→host output,load/default/legacy/lifecycle and ARM/x86/public correspondence unknown. All38application U outcomes and48family predicate rows remain unchanged. [Read-only author checks](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-base-creation-frontier-v1/author-check.json) verify selected rows/spans/pins,finite composition,projection discrepancies,prefix preservation and18false-promotion controls. Source counts/facts/ranges are auxiliary,not new outcomes or grades. No binary/native/provider/decoder/harness/original/model/comparator/fixture/build/install operation,new clause/case/release/grade/site credit or successor is selected. Neither101ad08a0 nor102231400 is followed. This additive packet awaits separate independent review; Root owns shared routing/index/log/coverage.


## Utility base-return/creation source review approval — 2026-10-20

Root read/adopted the complete [independent base/creation review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-utility-base-creation-frontier-v1-review.json), SHA256 `b65cafca9f13806d6ee93ca5780a268312f87e8541ddf591afeb29d3fd28612a`. Manifest `d80c5b2da7613bb56194cbd5f5651bbfc9abc6b5df22b86a889ac6272caa6ecd` binds ten payloads/67,116bytes, four complete selected C projections/3,544Cbytes and ten source spans. Sixteen pins/four approved chunks/four aliases/one inherited call slice/nine finite source intervals and18negative controls passed;28watched paths/five slices and144,608-byte research prefix/3,816-byte append stayed exact.

The nine explicit20byte helper-write ranges exclude the earlier flag interval only under same-Q,valid nonwrapping/nonalias memory and correctly recovered arguments. This narrows explicit source interference; hidden effects, native invocation, active flag preservation, actual public Mute/default and Q=P=M remain unknown. Three projection discrepancies remain open: a consumed result whose selected callee declares void, an omitted model-helper argument, and three caller arguments versus two target parameters. Internal V/returned B/incoming Q or T are not equated by convention. J1/J2 may alias. Initialization/reference/callback-shaped expressions prove no formal constructor, allocator success, ownership, model admission or host lifecycle.

All six public bridges/38application outcomes U/48family predicate rows remain unchanged. No native instruction/provider/decoder/harness/original/model/comparator/fixture/build ran; neither x86 prefix callee nor an encountered helper/global/slot was selected. The earlier pending section is author history. The review adds no indirect-site credit, normative clause/case/release/grade or automatic successor. D03 remains open with precise ABI, current-value, receiver, host-output and lifecycle frontiers; further selection belongs to the plan.


## Native ABI frontier selection — 2026-10-20 (preparation only)

Root separately selected [seven fixed native-window preparation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-native-abi-frontier-preparation/selection.json), SHA256 `6fb6333c80c3c8091c7f45149244eacfb23d37e4260a7930da5e123533f7a9ac`, across the already reviewed whole-six-gap base/creation records. The exact996physical bytes/249ARM64words cover101aff380,101bc3aa0,10214b954,10215f2b8,10215f3d8,1023a1004 and102f4fadc at their pinned single C1 metadata ranges. This aims to disambiguate recovered register/return/argument relationships; metadata ranges are not complete dynamic control-flow evidence.

Only retained metadata/previous header and tool pins were read for this selection. No selected image window was read or extracted, decoder/native/provider/original instructions executed, nor code/tool installed. Existing Rizin is the only proposed decoder; future capture must freshly verify image/tool/header identities, retain bounded exact raw bytes/byte-exact decoded rows/attempt and failure receipts, and pass source preflight plus independent readiness before execution. Encountered callees/globals/slots and both old x86 prefix callees remain outside selection. All6G/38applicationU remain open; no current public identity, compatibility, case/grade/release or indirect-site credit follows.


## Utility native ABI static review approval — 2026-10-20

Root read/adopted the complete [independent actual-result review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-native-abi-frontier-actual-review.json), SHA256 `dde3fb2d95ef1e0b4342ffff734b6e9d89b6771cc8836e31b8f70b44a21075e6`. It approves manifest `d07b68ae0e057d5037b05acda3f91e7e23ed68b73935cf134ccf006970ab3fb5`,52payloads/109,950bytes, the single23:41:35UTC static capture and ten conditional native relationships. All249rows/996bytes/seven decoder PID-exit records/14recorded before-after identities were checked. Thirty-eight BL/oneB targets, two malformed pair operands and selected register/store/address fields received independent raw-bit arithmetic checks. The reviewer reopened no source image/tool, reran no decoder and read no outside-window body/global/slot.

The new evidence narrows recovered-C omissions at native register-carrier scope. In the processor base frame, post-unread-call X0 reaches return unchanged and is the carrier consumed by its parent; this local V=B relation does not equate it with incomingQ. The initializer explicitly returns incomingQ through savedX19,while its first vptr store uses the distinct base-resultB. In the outer model frame,incomingX0/T is forwarded and received back from the selected helper under the stated normal-return/saved-register premises; inner post-helperV=T remains unknown. The caller passes load64(H+0x18),A,C in X0/X1/X2 and later returnsH; the target's lack of a direct X2 read does not prove X2 unused by unread callees. Formal constructor/factory roles,complete ABI,allocation,ownership and actual live instances are not established.

A four-byte zero store at initializerQ+0x15f precedes only nine selected20-byte zeroing-helper calls and subsequent disjoint field stores. Under valid nonwrapping/nonalias memory, saved-carrier/stack preservation, normal return and no interfering write, the four bytes stay zero at that return. This is an initializer-local conditional fact,not public Mute/default/legacy/load behavior or Q=P=M. Existing public current-value/callback/order/host-output joins remain unknown.

UDN-001 retains two malformed Rizin operand strings `0lr` unchanged at10214b960/10214b9c0. Separate raw pair fields reconstruct the48-byte stack displacement with fp/lr/sp; frozen decoder text is not silently repaired. Byte association and these selected field checks do not independently prove every operand or complete native flow. Actual BL10215f2e8→1047bd0cc remains unjoined with the recovered name thunk_FUN1047bcd58; neither target is followed. All cleanup receipts report the process group already gone after normal completion; timeout/surviving-descendant-kill/failure paths were not exercised. Outer PID remains unavailable,with all seven decoder PIDs retained.

All six public bridges/38application outcomes U/48family predicate rows remain unchanged. No original instructions ran,no indirect-site credit,normative clause/case/release/grade or complete profile follows. Earlier preparation/pending descriptions retain their dated status. Root separately selected metadata-only investigation of three existing x86 construction-frontier entries:factory1022313c0 and prior direct targets101ad08a0/102231400. Only existing header/function-start metadata parsing is selected; no instruction window,opaque193-byte suffix,callee body,decoder/provider/original/harness/model/comparator/fixture/build or installation is selected. Any future capture requires a separate reviewed bounded selection.


## Utility x86 construction metadata review and capture preparation — 2026-10-20

Root read/adopted the complete [independent metadata review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-construction-metadata-v1-review.json) (`d12531ba905db5c746831e30772dd5950a6b5c2a8e7b7248d1044f549fc04edd`). Manifest `9aab5cfeb484327fef07e8b13389ac67e0e0707b162958f2edf92238b310b244` binds five payloads/31,235bytes. Author and reviewer each read566,608metadata bytes only:32header/6,832loadcommands/559,744LC_FUNCTION_STARTS. All three selected entries and immediate successors were independently parsed. The412,317positive start records are linker navigation, not formal function extents or coverage. Full image SHA remains inherited at this metadata stage; no instruction bytes were read/decoded. The final checker was strengthened after acquisition; no pre-acquisition final-checker claim follows.

Root separately selected [capture preparation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-construction-preparation/selection.json), SHA256 `598ed96b52fea43a73270f0cd6137633a782c02b934dd56032d5a529146930fe`:101ad08a0–101ad0910(112bytes),1022313c0–102231400(64),102231400–102231490(144),320physical bytes total. Adjacent linker starts cap the selection without proving complete CFG/function/ABI or constructor roles. A single installed-tool [local command-help query](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-decoder-command-help.json) confirmed pDj takes a byte count; it read only/dev/null and ran no target decoder/original instructions. Preparation is active, requiring complete source preflight, independent readiness and a separate Root actual selection before target capture; fresh image/tool identities are required.

Prospective overlap is208of the historical240raw bytes:161of the old193opaque bytes could be decoded,32old bytes stay outside selection,112new image bytes are added. This is selection arithmetic, not a capture result. Historical evidence stays immutable. All6G/38applicationU/48family inventory remain unchanged; encountered callees/globals/slots, runtime/public identities and any original execution remain unselected.


## Utility x86 static capture — pending actual-result review, 2026-10-20

Root read/adopted the complete [independent preparation readiness](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-construction-preparation-review.json), SHA256 `f761b5e6d559dd329bae5ab4ab48d91d370d6d57414f1d2426bd1ff7ea27244e`, after its complete source preflight. A separate [Root actual selection](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-construction-root-actual-selection.json) pinned exact source/preparation/both reviews and isolated launch/DEVNULL/core0/outerdeadline. One capture ran2026-10-21T00:13:17.693–18.109UTC:three decoders/93rows/320selected bytes,exit0/empty stderr/no timeouts,17recorded fresh before-after identities equal. Zero original instructions executed. All cleanup receipts are already-gone; timeout/descendantkill/failurepaths untested and outerPID unavailable. No target expansion or retry.

[The frozen actual packet](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-construction-native-v1/manifest.json), SHA256 `e73746f56e4da53c256f71c5483894d2f3528868ef89100fae17c502935f4a9c`, binds27payloads/53,024bytes. Root read all93rows and checked16E8signedrel32targets/22selected opcode encodings. [A count correction](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-construction-root-readback-count-correction.json) qualifies the frozen narrative's mistaken23encoding count without rewriting it. Seven conditional facts remain pending independent interpretation review. The208overlap matches oldraw;161previously opaque bytes now have byte-associated rows,32oldraw bytes remain outside selection and112new image bytes are captured. Historical240/47/193provenance remains immutable.

A frame-local carrier is passed through the two prior directtargets; the selected normal path returns a saved opaque carrier after a load64(H+0x18)/three-register call to102247e80. That target and all other encountered outsidebodies remain unread/unselected. Similar carrier patterns do not equate this x86target with ARM10215f2b8,identify an allocator/constructor or prove current controls/host delivery. Unread-call normalreturn/preserved registers-stack/validmemory premises remain explicit. All6G/38applicationU/48inventory unchanged; no grade/site/clause/case/release or public route follows.


## Utility x86 static review approval — 2026-10-20

Root read/adopted the complete [independent actual-result review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-construction-native-actual-review.json), SHA256 `b5f95b0d6e0f31d95062c3419838b00082ca1fc55145b0de34915acfe4876252`. It approves the exact27payload/53,024byte packet and seven conditional facts with the explicit [22-encoding count correction](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-construction-root-readback-count-correction.json). All93rows/320rawbytes/16E8displacements/22selected carrier encodings/208oldraw overlap were independently checked. Three sequential decoder receipts and17before-after records agree;15retained-data watches were freshly rehashed by the reviewer,while fresh fullimage/tool identities remain the collector receipt scope. No image/tool/decoder reopened or original instructions executed by review.

Two direct targets were already part of the fixed batch; raw-check's generic “not followed” annotation means no additional expansion, not that those two selected bodies were unread. The physical post-RET suffix establishes no exception/error/teardown path. Frame-local carriers,opaque helper outputs,0x28/0x268 literals andload64(H+0x18) establish no formal constructor/allocator/protocol/class/ABI or ARM/x86 identity. All seven facts retain normal-return,saved-register/stack,valid nonalias memory and no-interference premises; outside-target behavior is unproved. Cleanup failure/timeout/descendantkill paths remain unexercised.

All6G/38applicationU/48family inventory stay unchanged,zero grade/site/norm/case/release or completed profile. Earlier pending prose records its as-of status. Root now separately selects metadata-only four-entry wrapper-frontier investigation at102247e80/101ac8330/101acf4c0/101acf650 from the reviewed call chain, supporting the whole-six-bridge study. Only freshheader/loadcommand/function-start metadata and selected adjacent bounds are selected; no new codewindow/decoder/original/callee-chain expansion. Future byte caps remain proposals,not capture authorization.


## Utility x86 four-target metadata approval and preparation — 2026-10-20

Root read/adopted the complete [independent four-target metadata review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-wrapper-frontier-metadata-v1-review.json), SHA256 `7e4b36d2ae87cba8e1b6b8e6f70456a9a4fde00055363267c86fca319df7b618`. Manifest `c2061a78e24aa412f9e6f800ca803bbacecae54452788a3f752563e6cc2c24c6` binds seven payloads/36,786bytes. The author source/synthetic preflight preceded its single566,608-byte metadata acquisition with unchanged reader SHA. Independent review read complete source before data-only check,verified17negative controls/eight immutablepins and separately reread exactly32header+6,832loadcommands+559,744function-start metadata bytes. All four ordinals/successors/ULEB/file mappings match; fullimage SHA remains inherited,not freshly verified at metadata stage.

The exact physical caps are101ac8330→101ac8340(16bytes),101acf4c0→101acf530(112),101acf650→101acf660(16),102247e80→102247e90(16),total160bytes. No instructionwindow,tool/oldopaque/targetbody/decoder/original was read or run. Lengths and adjacent starts establish no formal function/CFG/thunk/allocator/constructor/ABI or public role. All6G/38applicationU/48inventory unchanged,zero newsite/grade/norm/case/release.

After rereading the amended selector,Root separately selected [four-target static preparation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-wrapper-frontier-preparation/selection.json),5,704bytes/SHA256 `73ebe6098f0797bede038992d39eb2dd62a6ee40b75c60296a0c40ac03d7576a`. Only preparation is active:fullRootsourcepreflight,independentreadiness and separateRootactualselection are required. Future capture would freshly verify image/tool once before/after the batch,cover only160physicalbytes with at mostfour byte-count decoderchildren,and read no oldrawcode payload/compareprefix. No capture,original execution or further callee/global/slot following is selected here.


## Four-target static capture — pending actual-result review, 2026-10-20

Root read/adopted [preparation readiness](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-wrapper-frontier-preparation-review.json),SHA2563d25d96748a28c92c59ec116d9b716bb2e9e73be7c12afe22b99f5f3b6b238d5,after complete sourcepreflight. SeparateRootactualselection pinned exact source/manifest/bothreviews. One isolatedcapture ran2026-10-21T00:31:58.272–58.727UTC:fourchildren/51rows/160rawbytes,all exit0/emptystderr/no timeout,14recordedbeforeafter identities equal,zerooriginal/priorrawcode reads. Cleanupallalready-gone;failure/timeout/descendantkill paths untested,outerPID unavailable.

[Actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-wrapper-frontier-native-v1/manifest.json),SHA2564dcc2cf197f6e581a797af0d80bf8d9254653e0c5d552a699f308a255e287e71,binds32payloads/41,040bytes/sevenconditionalfacts. Raw5E8+2E9,RIPaddress106c98b78,FF20and24carrier encodings checked. Localx86tail101acf65c targetunknown,no mainARMsitecredit. H-storedaddress is not equated withload64(A);H/Aidentity unknown. Allnormalreturn/savedregister-stack/validmemory premises and6G/38U/48inventory remain;no encounteredtarget/global/table/pointerword followed. Independentactualreview active.


## Utility x86 four-target static review approval — 2026-10-20

Root read/adopted the complete [independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-wrapper-frontier-native-actual-review.json),SHA25611615d3543958a42a0fa9cc8ea9ad3d34d6d15b86560a805a8ad06e78685f2dd. It approves32payloads/41,040bytes,51rows/160rawbytes,fourchild PID/exit0/no-timeout receipts and seven conditional facts. Fourteen recorded beforeafter identities agree;12retained documents were independently rehashed,while fresh fullimage/tool hashes remain collector-recorded scope. No sourceimage/tool/priorraw/decoder/original was reopened/run by review. Raw5E8+2E9,RIPrelativeaddress106c98b78,FF20and24carrier encodings were independently checked.

The selected helper stores post-unread-call A atH+0x18 and returnsA;the next reviewed outer load forwards that carrier under explicit normal-return,savedregister/stack,valid nonalias memory and no-interference premises. H+0x20 is actually reloaded after an unread call;it is not assumed equal to originalF8. H=A and H!=A are both unproved. The address stored throughH is not equated withload64(A). Localx86indirecttail101acf65c still hasunknown target,no mainARMsite/resolution credit or Init/class/public role. Post-RET physicalsuffix is not an exception/destruction law. All6G/38applicationU/48inventory and zero grade/norm/case/release remain unchanged;failure/timeout/descendantkill paths were not exercised.

### UDN-002 — inconsistent auxiliary ESIL branch targets

UWF-ACTUAL-NOTE-001 records two auxiliary Rizin ESIL strings that disagree with retained instruction bytes. At101ac8335,raw e906f7ffff gives101ac7a40;ESIL instead contains101b87a40. At102247e85,raw e996feffff gives102247d20;ESIL instead contains102287d20. Opcode/disasm/jump fields agree with independently checked signed-rel32 arithmetic. Frozen output remains exact;the adopted readback uses raw bytes and agreeing fields,not ESIL. Do not execute,translate or use those ESIL strings as model/target proof. No rerun or corrective packet is needed for the supported conditional facts;this is not a universal decoder-semantics audit.

Root separately selected [352-byte inner-entry preparation](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-inner-entry-preparation/selection.json),SHA2562d5061a1175eecbae738198c5d8216143735e3e21964ea684c4c614f6126a595. The raw-verified tail target102247d20 is the independently verified immediate previous linker start before102247e80 in existing metadata;their difference is352physical bytes. Existing metadata is reused,no fresh table traversal. This is preparation only,requiring fullRootsourcepreflight,independentreadiness and separateactualselection;no selected codewindow or original execution. No function extent/constructor/ABI/public role or automatic further target/global/slot follows.

## Inner-entry static capture — pending actual-result review, 2026-10-20

Root read/adopted full [independent readiness](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-inner-entry-preparation-review.json),SHA256b32e9fc9b5d0a304647aac06337ad4f4e87e530940b443d8852a99bad6e64ab5,after complete sourcepreflight3804f28b.... Separate [actual selection](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-inner-entry-root-actual-selection.json) pinned source/manifest/bothreviews;one isolated attempt ran2026-10-21T00:55:26.858–27.181UTC,one decoderchildPID1115552/64rows/352bytes,exit0/empty stderr/no timeout,14recorded identities equal/zerooriginal. OuterPID unavailable;cleanupalreadygone,failure/timeout/descendantkill untested.

[Actual manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-inner-entry-native-v1/manifest.json),SHA2563baf25a5dfbc0b6b686f17e925a33f9bfc5af953411031d07a1f393d1fef001d,binds14payloads/37,740bytes/sevenconditionalfacts. Root checked all rows/rawbytes,14E8+oneEBsignedtargets/threeRIPaddresses. No callees/globals/constants/slots followed. Preliminary normal-path readback returns late load64(T+10),not provedQorzero;opaque helper writes/roles and all public binding remain unknown. AllESIL excluded;postRET EB00 ancillarytarget disagrees with raw/opcode/jump. Independent actualreview active;no semantic adoption,original/norm/case/grade/site/release or successor. All6G/38U/48inventory and confirmedOPENclosure unchanged.


## Utility x86 inner-entry static review approval — 2026-10-20

Root read/adopted the complete [independent actual review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-x86-inner-entry-native-actual-review.json),34,029bytes/SHA2561514d49122e1398acbf9c856bdc601ad8c25b48b332d64d4b5130ad1599b6477,with no findings. [Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-x86-inner-entry-native-v1/manifest.json)3baf25a5... binds14payloads/37,740bytes;all64rows/352bytes,14E8(12preRET/twopostRET)+oneEB/threeRIPaddresses and33further instruction witnesses passed. Gates precede actual;onechildPID1115552/exit0/empty stderr/no timeout;14recorded identities equal,12retained documents freshly hashed by review. Image/tool hashes remain collector-recorded;no fresh image/tool/priorraw/decoder/original read by reviewer. Normal cleanupgroupalreadygone;timeout/failure/descendant killing and outerPID remain unobserved.

Seven conditional facts are adopted at their exact local scopes. Q/T are incoming RDI/RSI saved toRBX/R14. Address106cb7268 is computed/stored throughQ without table/class role. Two signed32-to-single loads throughT and opaque globalbits precede unread helpers;no sample-rate/numeric/ABI law. Nine101b2b930calls receive Q-relative addresses168,180,198,1b0,1c8,1e0,1f8,210,228;helper writes/extents/results remain unknown,no ARM20byte rule. Explicit localstores are operations,not surviving defaults:Q+15f dword overlaps the last byte ofQ+158 qword,so not disjoint fields.

The normal path returns L=late load64(T+10),stored atQ+258,then localQ+260/Q+30..3f/Q+40zeroing andQ+8=32 without changingRAX. L is not provedzero,Q,a prior helperreturn or processor/modelpointer. All normal-return/callee-saved/intact-stack/valid-memory/no-interference premises remain explicit. Finalstores must not corrupt savedstack/returnstate. The suffix afterRET has no provedentry/exception/destruction law;itsRBX is only a hypothetical registercarrier,not automaticallyQ.

### UDN-002 continuation: inner-entry auxiliary target

The independent review records EB00 at102247e5c:rawPC+2+0 andagreeing opcode/jump yield102247e5e;ancillaryESIL instead says102287e5e. This extends the [UDN-002 qualification](#udn-002--inconsistent-auxiliary-esil-branch-targets) to the new packet without changing historicaloutput. ALL ESIL,including malformed SSEstrings,is excluded from semantic/branch/modelproof. No rerun or frozenrepair. Physical adjacentstarts/completebytes prove no formalfunction/CFG/constructor or cross-slice equivalence. All6G/38publicU/48familyinventory remain unchanged;no original/norm/case/oracle/grade/site/release or automatic successor. Requiredunsupportedbehavior keeps closureOPEN.
