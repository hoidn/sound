---
id: RESEARCH-DEVICE-RACKS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 5
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


## Historical R2 bounded primary-Racks owner adoption

Earlier research body text remains exact as-of corrected R1; its pending-recheck
wording is historical. [Focused R1 final review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-review-final.json)
approved RR01/RR02 corrections as partial before this successor. The new
[source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/racks-source-audit/README.md)
and [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-source-audit-review.json)
reconcile124primaryblocks/264judgments/53resources/22proposals against28actual
clause bodies and61fullactions, plus only seven CommonDevicesdefault paragraphs.
All those primary source assertions/qualifiers, original actions, proposals and
RR01/RR02 were read for this adoption. Not full CommonDevices153/A-B/defaults,
images or separately linked resources; only existing retained bytes are used.
Primary Racks HTML288006bytes/SHA9b93de0730839152a58dcb843bd74ab0385b6cfa1fb6d58bb28306200ad582fb,
captured2026-10-19T20:01:50.641719Z. CommonDevicesHTML302488bytes/SHA
6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82,
captured2026-10-19T20:01:52.371400Z. These currentVersion12 source identities
are not exact-build12.4.3 execution.

[Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases-r2.json)
are81:61verbatimoldplus20new,3installed assertions/66documentary/12U. All
actual outcomesnullU/unexecuted, including original nonnull expected strings.
Sixold clause bodies append local control/entry roles under unchanged28IDs;
023–026/common cases048–052 stay exact for the separate CommonDevices owner.
[The22-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/adoption-r2.json)
records bounded inputs, not entire assertions/groups completed. G14controller
protocols remainU; G22reuses053–061U. Only three new named UI-role documentary
pairs are nonnull;17and allnew numeric/signal/file/message/RNG/timing pairs null.

ActualnoteANDCC positives, sustained nonzero no-exit tail, BOTH genuinely
productive mapped controls and per-chain note reception precede exclusion/
no-effect/mute/delete. Sound requires working nonzero source/processing/wet/
send/return/output; editor controls require no audio. A flag/zone/name or empty
source is not success; absent/failed capability staysU. KEYfade020 differs from
newVelocity/MIDIselector; browserlayer042 differs from pad-to-pad; configured
Multi043 differs from Receivechange. Actualpan044/equalvolume045 and two
extraction046/047routes remain true. No borrowing one action for allcontrols.

RR01 same-unitANDsame-range unit exception and independent genericname remain;
new same-unit/different-range trial has nullnumeric comparator. RR02 factory
no-custom/no-preset eight, factoryVolume/no-useroverride and factorysampledrop
Simpler remain qualified. Empty-altglyphs and eight-step illustration are not
inspected; no plus/minus or geometry law. Only sixreturns supported; seventh061U.
No gain/fade/RNG/codec/timing, controller/hardware or lifecycle/default law.

[Preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/prior-files-r2.json)
retains18old packet files and both original seals exactly in place, with before
canonical snapshots matching the source audit embedded identities. [Historical
consumers](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/consumer-impact-r2.json)
retain28old-hash occurrences in26externalJSONfiles as-of, not current semantic
failures or immutable dependencies on evolving pages. No old checker/capture/
author replay, consumer edit or automatic adapter. Current own immutable pins,
[delta](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/delta-r2.json),
guards, snapshots and independent owner review govern.
**AS-OF AUTHOR FREEZE:** R2 independent review pending; [spec index](../specs/index.md)
owns current disposition. No original/vendor/native/application/UI/hardware/
network/account/install/source-example/candidate execution or source recapture.
No full Rack or source-topic completion/coverage credit.

## R3 source-role clarification

[RACKS-R2-REVIEW-001](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r2-review.json)
identified ambiguous grouped wording in007/066: B044 explicitly resizes either
section at edges, but the move target is the zone itself. R3 names an admitted
lower-main interior zone drag and leaves independent fade-section translation U.
This does not assert that an operation is absent in Live or the source conflicts.
The source-audit A089/A090/G05 shorthand needs [additive qualification](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/audit-shorthand-qualification-r3.json),
not rewriting its frozen bytes or adopting its zero-credit proposal as authority.

The [current catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases-r3.json)
keeps28requirements/81cases (3installed/66documentary/12U). Only one appended
clause and one setup action change; source_claim/oracle/pointer/guard fields and
all61original records stay exact. All36R2files and existing before snapshots
remain in place. The [correction](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/correction-r3.json)
reconstructs literal differences and pins the immutable required-finding review.
The full124primary/28old clauses/61old+20new actions review carries only unchanged
material. Current focused checks retain18meaningful guards and reject the movement
conflation. No old main/writer/consumer replay, adapter or live canonical gate.
All actual outcomes remain null/U/unexecuted; seven selected Common defaults are
context only, and no full153Common Devices owner adoption occurs here.
**AS-OF AUTHOR FREEZE:** R3 independent focused review pending; [spec index](../specs/index.md)
owns current disposition. No source image/pixel, geometry, gain, RNG, file, timing,
lifecycle, controller or exact12.4.3 outcome is newly established.

## R4 bounded Common Devices adoption

All earlier current/pending wording is historical as-of R1–R3. R3focused correction
was [independently approved](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r3-review.json)
without widening the B044whole-zone movement predicate. The approved
[Common Devices full-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/device-chain-source-audit/README.md)
and [review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/device-chain-source-audit-review.json)
cover153fullsource paragraphs/list/headings,153whole-context judgments (not atomic
facets),20audit proposals and41selected actual neighboring predicates/actions.
All153texts/qualifiers,20proposals,41selected neighbors and current28contracts/
81fullactions were read. All140baseURL/caption/empty-alt roles were inspected;
responsive variants hashchecked only; no image pixels or linked destinations.
Verbose repeated-field outputs were reread in bounded projections where truncated.

The retained CommonDevicesHTML remains302488bytes, SHA256
6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82,
original capture2026-10-19T20:01:52.371400Z, Version12current with precise
publication and target12.4.3 parity unknown. No recapture/date substitution.
R4refines only023–026 and adds029–038 for distinct A/B/default families.
[Current38requirements/101cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/README-r4.md)
keep all81R3records verbatim, including sourceclaims/oracles. Twenty new actions
are D12proposals; only seven named UI-role pairs have documentary criteria,
thirteen null and allactual/numeric/audio/message/time/RNG/filecomparisonsnullU.
No completion or reference/candidate run occurred.

The20-group ledger retains bounded missing inputs without completing entire
groups. True WORKSPACE009/CV001/NAV014/NAV079, RMLmonitor/compensation,
PluginHosting009/PH017, Project019/PMW026–028, Browser040 and APIA-B records
remain their own narrow scopes. Current ConversionATM036/037 already requires
factory/no-custom histories and actualNONEMPTYnotes plus genuinely nonzero active
preview; old029absence is not substituted. Pitched custom defaults may use a
single instrument OR Rack; Drums must use nonnested DrumRack. No arbitrary
conversion input is promised notes. Allold primaryRack laws, RR01sameunitAND
range and RR02factory qualifications remain exact.

A/Bautomation needs actualchangingparametercontribution, selected-state PARAMETER
context Re-Enable, and no automatic restoration or global substitute. Selected
copy/duplicate/preset state is documentary, not numeric/codec/fileequality.
Preset and sample HotSwap differ; expanded Sampler top-left button is always
visible while fourother contexts use hover. -EnableHotSwapOnSelection remains
inert source text; future tests require independently recognized EXISTING owned
configurations, no Options edits. Plug-in configuration saves LISTnotVALUES;
families keep factory/custom/lastADDED/Project contexts distinct. Recognized
successful save/load and genuinely productive controls precede absence/overwrite;
flags/names/folders alone fail that prerequisite. Editor controls need no audio.

[Preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/prior-files-r4.json),
[exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/delta-r4.json) and
[consumer census](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/consumer-impact-r4.json)
keep49old files/seals and oldconsumer as-of identities unchanged, no automatic
adapter or replay. Own immutable source/current-snapshot pins govern this draft;
no futuremutablewiki gate. DCA-Q01–04, target/default/Option parser/build/context,
failures/undo/persistence/transport/teardown, numerical/DSP/CPU/headroom/latency/
RNG/protocol/codec/fileatomicity stayU. No original/vendor/native/UI/audio/MIDI/
hardware/network/account/install/config/fileoperation/sourceexample ran.
**AS-OF AUTHOR FREEZE:** R4independent owner review pending; [spec index](../specs/index.md)
owns current disposition; this author does not self-approve or close coverage.

## R5 historical audit scope versus current owner metadata

The [formal R4review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r4-review.json)
required only COMMON-R4-REVIEW-001: all20remaining_U fields copied the audit-only
no-adoption sentence without identifying its historical scope. The audit adopted
no IDs/cases; the bounded R4owner adopted10IDs/20cases. The current
[R5ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/adoption-r5.json)
separates **AS-OF SOURCE AUDIT** text, current adoption counts and remaining
unknown outcomes. No source or behavioral inference changes.

All38contracts/101cases, sourceclaims/oracles/guards/counts remain exact R4,
including7newnamedUIpairs/13nullpairs and3installed/86D12/12U. Current behavioral
providers stay R4requirements/cases; allactualnullU/unexecuted/0complete. The
[response](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/response-r5.json)
records20exactfield replacements and pins all67oldfiles/seals, the required review
and reusedR4beforeproviders. No duplicate archive, oldtool/consumer replay, adapter
or evolving canonical gate. Earlier pending/current prose remains historical
as-of its authorfreeze. No new source read, capture, original/vendor/native/UI/
audio/MIDI/hardware/network/configuration/fileoperation/install/candidate run.
**AS-OF AUTHOR FREEZE:** focused R5independent review pending; [spec index](../specs/index.md)
owns current disposition.
