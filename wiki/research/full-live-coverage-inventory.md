---
id: RESEARCH-FULL-LIVE-COVERAGE-INVENTORY
type: research
status: current
updated: 2026-10-23
access: analysis
target: Ableton Live 12 Suite 12.4.3
revision: 11
---

# Full Live specification inventory

At the start of this inventory, the [feature map](../specs/feature-map.md) had 14
broad planning families and 19 draft specifications. Those drafts and finite
partial handoffs cover portions of those
families. They do not describe the whole product. This inventory adds a finite,
auditable discovery baseline from the installed package and the official manual.
Inventory membership establishes an obligation to investigate; it establishes no
behavioral requirement, implementation result, or compatibility pass.

## Sources and method

Observed package: [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md), local
`/home/ollie/Ableton Live 12 Suite.app`. The current capture rehashes the universal
Live executable to `52289af638f1b26590c84a9bc08eabdc35127883087057add909d2718a7a35ef`.
The [capture manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manifest.json)
pins every initial output, exact source paths, byte counts and SHA-256 digests. Its
[retained extractor](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/capture_inventory.py)
uses Python standard-library directory reads, gzip/XML parsing and HTML parsing.
No original executable, bytecode, Max patch or device function was executed.

Observed manual: Ableton's [Version 12 manual contents](https://www.ableton.com/en/live-manual/12/welcome-to-live/),
captured 2026-10-19. Exact [HTML bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-12-toc-2026-10-19.html)
hash to `584d4b61d119c96ecdb7941ef34ac9d4e0282a3e40c8bc474b6cf24892640d80`.
The document says Version 12, without a 12.4.3 revision pin. Each extracted
[TOC row](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
retains its URL, anchor, original section number and exact captured HTML line.
The anchor-derived `SURF-MAN-...` IDs are stable within this captured revision;
future title/anchor changes require explicit aliases rather than silent ID reuse.

Observed latest installed schema: `Contents/App-Resources/Schema/12.0_12402.txt`,
SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Its [retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt)
and [412 class records](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/schema-classes.json)
give exact top-level class lines and field declarations. A class declares stored
structure, not a separate user feature or an accepted-file behavioral contract.
Prior [package findings](ableton-package-structure.md) remain the canonical account
of package boundaries and the limits of dependency observations.

## Denominator and status rules

The machine-readable [denominator](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/coverage-denominator.json)
freezes initial discovery revision1. These are separate, overlapping dimensions;
adding them would count the same surface several times.

| Dimension | Finite denominator | Meaning and limit |
| --- | ---: | --- |
| Manual navigation baseline | 880 numbered TOC entries, 708 navigation leaves, 43 chapters | Every captured topic gets an applicability decision and a behavioral mapping or a reviewed reason why it creates no new obligation |
| Device profiles | 102 | 63 current native devices, 4 racks, 8 legacy native devices, 20 Max devices, 2 Max MIDI tools and 5 Max templates; profiles overlap manual topics and tool rows |
| MIDI tools | 17 | Twelve transformation and five generation topics; includes the two shipped Max tool profiles |
| Persistence vocabulary | 412 classes | Every latest-schema class needs a disposition; classes are not all devices or user features |
| Service/package identities | 13 files | 12 executable candidates and the application plist; package presence does not establish runtime topology |
| Controller/module profiles | 149 directories | Includes internal/framework support directories; does not mean 149 supported controllers |
| Keyboard binding discovery (revision2 addition) | 292 rows in27 tables | Separate retained shortcut chapter; contextual duplicates, alternatives and gestures, not292 unique or completely specified commands |
| Public Live API discovery (revision5 addition) |45reference entries,588explicit declarations and6bridges |Current publisher index declares12.4.5; explicit headings only, inherited/alias/signature/version mapping pending, not behavioral requirements |
| Captured manual source-heading discovery (revision11; includes revision10) |1,066 distinct actual heading URLs,833 numbered-outline leaf URLs;186 additional h4 URLs across18chapters |Finite retained44capture/43chapter discovery only; includes14Browser headings, preserves original880rows/708navigation-leaf flags; paragraph/behavior reconciliation remains open |

**Mapped** means a stable surface ID is routed to a proposed owning feature/spec
and an applicability question. **Specified partially** means cited clauses and
cases exist for a bounded subset. **Specified completely** requires a reviewed
finite contract covering the applicable surface's states, errors, timing,
persistence, interactions and acceptance cases, with no unresolved in-scope
clauses. **Released** means a reviewed immutable handoff exists for its declared
subset. **Implemented** and **verified** require independent evidence and are
tracked separately. The current device ledger has **zero complete profiles**.
This revision does not claim the entire discovery denominator is mapped.
The frozen JSON ledger retains discovery-time statuses. The tables on this page
route later reviewed partial drafts; those additions do not rewrite the retained
baseline or close a profile.

Every future discovery adds a new revision and changes the denominator visibly.
An unresolved platform or manual-version question stays open; it cannot be
removed from the denominator to improve a completion percentage. A reviewed
post-target or nonbehavioral disposition may close that inventory obligation,
while retaining its evidence and reason.

## Revision2 integration and keyboard discovery

The original twelve-payload inventory manifest and all initial JSON denominators
remain unchanged. This mutable revision routes later partial contracts and adds
a finer-grained [shortcut binding discovery catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/shortcut-bindings.json).
Its [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/keyboard-navigation/manifest.json)
pins the separately retained current keyboard chapter and exact HTML row locators.
The292 rows overlap manual topics and actions already in the feature map. They
remain unclosed pending per-binding context, applicability and canonical action
reconciliation; do not add them to device/manual/schema counts or call them
executable cases. [Navigation/accessibility](../specs/keyboard-navigation.md)
provides a bounded partial owner, not coverage of every command.

## Revision3 corrected spectral-device associations

The original ledger crossed Spectral Resonator and Spectral Time's schema classes
and factory examples. The [companion device ledger revision2](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r2-spectral-aliases/devices-r2.json)
corrects only those two existing profiles: all eight named Resonator factory
presets have `Transmute` roots, while all six Time presets have `Spectral` roots.
The respective schema control vocabularies corroborate that association. Exact
14 source hashes, original attributes, class lines and a read-only audit are
pinned by the [correction manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r2-spectral-aliases/manifest.json).
The [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-spectral-alias-review.json)
verified all original presets and unchanged source history; the other100 rows,
102IDs/order/statuses and zero-complete count are unchanged. This corrects
package associations only; runtime alias/DSP behavior is unobserved.

Use the companion ledger for current class/example associations. The original
`inventory/devices.json`, all twelve initial payloads and original review remain
exact historical evidence. Their two crossed associations are superseded, not
silently rewritten. Profile/manual/schema denominators have not changed.

## Revision4 manual reconciliation routes — reviewed navigation only

The [manual-routing companion](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r3-manual-routing/manifest.json)
retains all880 original heading IDs, URLs, HTML lines and708leaf flags. It uses
chapter entry points and exact existing device/manual descendant associations to
propose where an analyst should reconcile each topic. This is navigation, not
clause-level specification coverage, applicability evidence or a second work queue.
The [current plan](full-live-specification-plan.md) remains the sole selector.

Its frozen pre-settings-authoring snapshot has607leaves with candidate entry
points and101without a canonical owner. All708leaf requirement/case mappings
remain pending; all topic applicability is U and zero topics are complete. The
missing routes include first steps, Live Concepts, Stem Separation, Push1/2,
MIDI Fact Sheet and intro/credits disposition. No introduction/credits topic is
automatically excluded as nonbehavioral. The two device-reference chapter root
headings also lack a single canonical owner; descendant device routes do not
close those chapter summaries. Newly authored owners do not rewrite this snapshot.

[Exact routing rows](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r3-manual-routing/manual-routing.json),
[summary](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r3-manual-routing/summary.json)
and read-only `derive.py --check` preserve the source denominator and expose missing
owners without inventing requirements. [Independent routing review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/manual-routing-r3-review.json)
approved candidate navigation only, with no required findings. Original inventory
bytes, statuses and spectral-correction history stay unchanged.

## Revision5 exact citation cohort and public API discovery

The [four-packet citation crosswalk](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r4-citation-crosswalk/manifest.json)
adds exact source-anchor links for video/synchronization/settings/stem only:
83requirements/123cases/195blocks, distinct from the separate engine195blocks.
It preserves all880TOCrows/708leaves and maps111evidence citations to27topics
(22leaves/5nonleaves);8unmatched references at3URLs and9Uclauses without evidence
stay explicit. Other packets/releases are outside this first cohort, not declared
uncited or unowned. The [independent audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/manual-citation-crosswalk-r4-review.json)
reconstructed every119evidence reference and all128record pointers, approving
citation navigation only. All topic semantic coverage/completion remains unknown;
no leaf is complete, all708full-clause reconciliations remain pending.

The [Cycling74 Live API source family](sources/cycling74-live-api.md) adds a separate
overlapping discovery dimension:45listed reference entries,588explicit direct
member headings (64children/361properties/163functions),6bridge/lifecycle references
and53retained source pages. The index declaresLive12.4.5, not12.4.3. All member/
entry applicability and clause/case ownership remain U/unmapped, with zero complete
entries. Inherited members, root/alias semantics, overloads, bridge generic Max
attributes and actual event/message outcomes require reconciliation. [Independent inventory review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/max-api-inventory-review.json)
approved source-inventory mechanics only; no API contract, runtime or compatibility follows.
The original manual/device/schema/controller/service/shortcut snapshots stay intact.

## Revision6 editorial manual-topic dispositions

The [editorial-topic packet](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r5-nonbehavioral-topics/manifest.json)
retains all five Welcome body blocks and26Credits blocks. It classifies original
TOC numbers1,1.1 and43 (three headings/two leaves) as welcome/editorial/reference
and manual-publication/authorship/contact/trademark/provider notices, without an
application input/state/output contract. [Independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/nonbehavioral-manual-topics-review.json)
read all31blocks and raw chapter context and approved these source-topic
dispositions only. The two manual leaf obligations need no application contract
from these passages; all880heading/708leaf identities remain in the denominator.
This is no legal interpretation or finding that application About/help/support/
branding/authorization features are absent. Those product obligations remain open.
Figures/logos were not inspected; no application-image behavior is claimed.

[Source identities](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r5-nonbehavioral-topics/sources.json)
preserve original Welcome capture date only (exact UTC unknown), and new Credits
240882bytes SHA`fb95a51814b50c71ff783aefa47e136f20153b3a0b46c96681da1c759c4a6b76`.
Original statuses/complete=false rows remain unchanged; no application profile,
requirement or compatibility case passed. Earlier routing/citation snapshots retain
their original pending-state scope and are not rewritten after later dispositions.

## Revision7 bounded public API member mappings

The original frozen source inventory retains45 reference entries/588 direct
headings and its original unmapped discovery fields. New partial mapping companions
preserve those bytes rather than rewriting source discovery into a completion claim.
[Clip/Sample](../specs/live-api-clip-sample.md) maps131 direct declarations across
five entries to reviewed partial contracts/cases;143 requirements/163 proposals.
[Control/tuning](../specs/live-api-control-tuning.md) maps28 declarations across six
entries plus one separately labeled zero-member root context;33 requirements/
41 proposals are frozen for independent review. All actual member oracles remain
null/U/unexecuted, and zero entries/members are semantically complete. Core/session
and device/rack families are authoring separately; inheritance, complete schemas,
version applicability and the other reference entries remain open. These mapping
companions overlap manual/device/workflow owners and do not add independent product
features or a compatibility percentage.

## Revision8 complete direct-member routing, incomplete behavior

The five bounded API member families now provide a partial mapping owner for all
45 original reference entries/588 explicit direct declarations. They are
[Clip/Sample](../specs/live-api-clip-sample.md), corrected
[control/tuning](../specs/live-api-control-tuning.md),
[device/rack](../specs/live-api-device-rack.md),
[core/Session](../specs/live-api-core-session.md) and
[specialized devices](../specs/live-api-specialized-devices.md).
All five have independent partial-scope reviews, including preserved corrected
control/tuning and core/Session successors. DrumPad.delete_all_chains is heading-only and its semantic
contract stays U; mapping its identity does not supply an operation. Every member
is incomplete/target-U, including inherited/root/alias and full typed/error/
lifecycle/processing obligations. Original inventory mapping fields and all53
source captures remain unchanged. This routing milestone is not API completion,
full-product coverage or candidate compatibility. Cross-packet cases/questions
use packet-qualified identities under coverage design revision5. The frozen
[direct-member companion](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r7-api-member-mappings/manifest.json)
reconciles all45entries/588members,626requirements and702qualified cases with
exact JSON pointers; its separate [navigation-only review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/api-member-mappings-r7-review.json)
is approved, without new API semantic approval.

## Revision9 second literal citation cohort

The [R6 companion](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r6-citation-crosswalk/manifest.json)
adds Push/engine/Browser/workspace only; its
[independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/manual-citation-crosswalk-r6-review.json)
accepts exact navigation, not source-topic semantics. All880original rows/708leaves/
43chapters remain unchanged. The162requirements/221cases cite666requirement-source
references:290literal matches (192D12/98Ucontext) on62topics/55leaves;376unjoined
references remain explicit. Of these330Push blocks have direct null anchors,
which are not filled from ancestor context;46Browser references use14URLs absent
from the original TOC. Those references stay visible and require disposition,
not normalization or removal. Fifteen U engine requirements retain source-context
citations; a matching anchor never upgrades them to documented outcomes. The
original R4cohort remains separate and unchanged; these overlapping counts are
not summed into a coverage numerator. Zero source topics are declared complete
by either citation companion.

## Revision10 retained Browser headings outside navigation

The [R8 successor](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r8-browser-heading-dispositions/manifest-r2.json)
and [independent source-heading review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/browser-heading-dispositions-r8-review.json)
verify14real h4 headings with four-part numbers: five under Splice4.7.3 andnine
under User Library4.7.6. Both retained documents have the identical880number/
title/URL navigation sequence and omit these heading IDs/links. The original
parser accepts four-part numbers, so a parser depth filter is not the explanation;
precise publisher/capture-version causality remains unknown.

Each new record preserves exact source URL/full hash/heading HTML/tag/number/
line-column and a typed source-outline-child relation. The two original parents'
leaf flags remain historical navigation metadata; source children are separately
retained. All46R6references stay literally unjoined; no parent/alias is substituted,
no behavioral credit or complete topic is claimed. The broader retained-chapter census is recorded in revision11 below. The original880/
708counts are an open navigation baseline, not the complete source heading or
paragraph denominator.

The original R8checker hit tuple-versus-JSON-list representation mismatch. The
first seal/all6payloads remain unchanged. Its preserved successor normalizes the
reconstruction for comparison and checks both manifests,42inputs and all9current
payloads; use check.py --check, not historical derive.py --check. No failed
validation was recast as a pass and no source evidence was changed.

## Revision11 actual captured chapter-heading census

The [R9 census](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r9-captured-manual-headings/README.md)
and [independent structural review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/captured-manual-headings-r9-review.json)
resolve the frozen134physical HTML paths into44distinct selected Version12
captures at all43original chapter URLs. They retain1,088numbered heading
occurrences and1,066distinct literal heading URLs. All880original navigation
URLs match with unchanged numbers/titles;186additional actual h4 URLs occur
across18chapters. The14Browser headings from revision10 are a subset, not an
additional count. Separate actual numbered-outline discovery has833distinct
leaf URLs;61original navigation leaves have actual source children. Original
880rows/708leaf flags/order remain immutable.

All355source catalog records,200explicit physical manifest bindings and283input
pins were replayed. Twenty-five identical physical bindings remain visible;
two different Concepts hashes at the same URL remain separate observations.
Eight selected captures retain unknown UTC. The20heading-level gaps retain
actual ancestors without invented intermediate parents. The reviewer independently
reconstructed every selected heading's tag/attributes/ID/number/text/line-column,
outline and leaf status. This checks discovery only: paragraph meanings, images,
examples, exact12.4.3applicability and full product completeness remain unknown.
The census neither repairs old literal citation joins nor closes an application
obligation. Future captures/discoveries require explicit successors.

## Package corroboration and version uncertainty

Observed [directory captures](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/package-device-directories.json)
show all 63 native manual device names in `Builtin/Devices` category directories.
The [device ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/devices.json)
also binds them to latest-schema classes and, where available, an exact hashed
shipped preset and XML locator. Matching a named preset's root supports a device
alias. A schema name and directory alone leave the semantic alias inferred.
Shipped default/preset files are historical content carried by 12.4.3; their
Creator attributes must not be treated as reference captures made by this build.

The [preset-root inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/preset-device-roots.json)
records the parsed document denominator, zero parser failures, type occurrence
counts and exact hashed examples. Repeated preset occurrences do not add device
profiles. Max AMXD profiles retain source byte hashes and paths; their presence
does not establish patch behavior. Max application examples and arbitrary third
party content are outside this shipped Live-device list and remain part of the
separate Max-host/API scope decision.

All manual clauses remain **version-uncertain** until individually reconciled
with target evidence. Installed product-name corroboration does not validate
the current manual's detailed parameters or behavior. In particular, current
manual topics for Stem Separation, Bounce to Audio, Link Audio, Splice,
Ableton Cloud, accessibility settings and later device revisions require an
explicit 12.4.3 applicability check. No conclusion here says these features are
absent; a later manual can add behavior to an already present feature.

## Device profiles

Rows below route the device denominator; exact paths, hashes and schema locators
belong to the machine-readable ledger. `partial` means selected parameter or DSP
clauses only. Every other profile remains behaviorally unspecified. Common
device-chain persistence does not specify a device's sound or interaction model.

### Current native devices (63)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-DEVICE-AMP` | Amp | `Amp` | [Partial storage](../specs/bundled-device-parameters.md); host-emulation deferred |
| `SURF-DEVICE-AUTO-FILTER` | Auto Filter | `AutoFilter2` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-AUTO-PAN-TREMOLO` | Auto Pan-Tremolo | `AutoPan2` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-AUTO-SHIFT` | Auto Shift | `AutoShift` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-BEAT-REPEAT` | Beat Repeat | `BeatRepeat` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-CABINET` | Cabinet | `Cabinet` | [Partial storage](../specs/bundled-device-parameters.md); host-emulation deferred |
| `SURF-DEVICE-CHANNEL-EQ` | Channel EQ | `ChannelEq` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-CHORUS-ENSEMBLE` | Chorus-Ensemble | `Chorus2` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-COMPRESSOR` | Compressor | `Compressor2` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-CORPUS` | Corpus | `Corpus` | [Partial DSP/storage](../specs/device-corpus.md) |
| `SURF-DEVICE-DELAY` | Delay | `Delay` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-DRUM-BUSS` | Drum Buss | `DrumBuss` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-DYNAMIC-TUBE` | Dynamic Tube | `Tube` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-ECHO` | Echo | `Echo` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-EQ-EIGHT` | EQ Eight | `Eq8` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-EQ-THREE` | EQ Three | `FilterEQ3` | [Partial filter/EQ draft](../specs/filter-eq-devices.md); corrected partial draft reviewed; exact-build U |
| `SURF-DEVICE-EROSION` | Erosion | `Erosion2` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-EXTERNAL-AUDIO-EFFECT` | External Audio Effect | `BufferAudioDevice` | [Partial hardware-routing contract](../specs/external-hardware-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-FILTER-DELAY` | Filter Delay | `FilterDelay` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-GATE` | Gate | `Gate` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-GLUE-COMPRESSOR` | Glue Compressor | `GlueCompressor` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-GRAIN-DELAY` | Grain Delay | `GrainDelay` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-HYBRID-REVERB` | Hybrid Reverb | `Hybrid` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-LIMITER` | Limiter | `Limiter` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-LOOPER` | Looper | `Looper` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-MULTIBAND-DYNAMICS` | Multiband Dynamics | `MultibandDynamics` | [Partial dynamics draft](../specs/dynamics-devices.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-OVERDRIVE` | Overdrive | `Overdrive` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-PEDAL` | Pedal | `Pedal` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-PHASER-FLANGER` | Phaser-Flanger | `PhaserNew` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-REDUX` | Redux | `Redux2` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-RESONATORS` | Resonators | `Resonator` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-REVERB` | Reverb | `Reverb` | [Partial device contract](../specs/delay-reverb-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-ROAR` | Roar | `Roar` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-SATURATOR` | Saturator | `Saturator` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-SHIFTER` | Shifter | `Shifter` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SPECTRAL-RESONATOR` | Spectral Resonator | `Transmute` (corrected association) | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SPECTRAL-TIME` | Spectral Time | `Spectral` (corrected association) | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SPECTRUM` | Spectrum | `SpectrumAnalyzer` | [Reviewed partial contract](../specs/device-spectrum.md); exact-build U |
| `SURF-DEVICE-TUNER` | Tuner | `Tuner` | [Reviewed partial contract](../specs/device-tuner.md); exact-build U |
| `SURF-DEVICE-UTILITY` | Utility | `StereoGain` | [Reviewed partial contract](../specs/device-utility.md); exact-build U |
| `SURF-DEVICE-VINYL-DISTORTION` | Vinyl Distortion | `Vinyl` | [Partial device contract](../specs/distortion-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-VOCODER` | Vocoder | `Vocoder` | [Partial device contract](../specs/modulation-pitch-loop-devices.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-ARPEGGIATOR` | Arpeggiator | `MidiArpeggiator` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-CC-CONTROL` | CC Control | `MidiCcControl` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-CHORD` | Chord | `MidiChord` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-NOTE-LENGTH` | Note Length | `MidiNoteLength` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-PITCH` | Pitch | `MidiPitcher` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-RANDOM` | Random | `MidiRandom` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-SCALE` | Scale | `MidiScale` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-VELOCITY` | Velocity | `MidiVelocity` | [Partial MIDI-effect contract](../specs/native-midi-effects.md); corrected partial draft reviewed, exact-build U |
| `SURF-DEVICE-ANALOG` | Analog | `UltraAnalog` | [Partial DSP/storage](../specs/device-analog.md) |
| `SURF-DEVICE-COLLISION` | Collision | `Collision` | [Partial DSP/storage](../specs/device-collision.md) |
| `SURF-DEVICE-DRIFT` | Drift | `Drift` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-DRUM-SAMPLER` | Drum Sampler | `DrumCell` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-ELECTRIC` | Electric | `LoungeLizard` | [Partial DSP/storage](../specs/device-electric.md) |
| `SURF-DEVICE-EXTERNAL-INSTRUMENT` | External Instrument | `BufferInstrument` | [Partial hardware-routing contract](../specs/external-hardware-devices.md), corrected partial scope reviewed; exact-build U |
| `SURF-DEVICE-IMPULSE` | Impulse | `InstrumentImpulse` | [Partial sample-instrument draft](../specs/device-impulse.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-MELD` | Meld | `InstrumentMeld` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-OPERATOR` | Operator | `Operator` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |
| `SURF-DEVICE-SAMPLER` | Sampler | `MultiSampler` | [Partial sample-instrument draft](../specs/device-sampler.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-SIMPLER` | Simpler | `OriginalSimpler` | [Partial sample-instrument draft](../specs/device-simpler.md), partial draft reviewed; exact-build U |
| `SURF-DEVICE-TENSION` | Tension | `StringStudio` | [Partial DSP/storage](../specs/device-tension.md) |
| `SURF-DEVICE-WAVETABLE` | Wavetable | `InstrumentVector` | [Partial instrument contract](../specs/synthesis-instruments.md), partial scope reviewed; exact-build U |

### Racks (4)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-DEVICE-AUDIO-EFFECT-RACK` | Audio Effect Rack | `AudioEffectGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |
| `SURF-DEVICE-MIDI-EFFECT-RACK` | MIDI Effect Rack | `MidiEffectGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |
| `SURF-DEVICE-INSTRUMENT-RACK` | Instrument Rack | `InstrumentGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |
| `SURF-DEVICE-DRUM-RACK` | Drum Rack | `DrumGroupDevice` | [Reviewed partial rack contract](../specs/device-racks.md); exact-build U |

### Legacy native devices (8)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-DEVICE-LEGACY-AUTO-FILTER-LEGACY` | Auto Filter Legacy | `AutoFilter` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-AUTO-PAN` | Auto Pan | `AutoPan` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-CHORUS` | Chorus | `Chorus` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-EROSION-LEGACY` | Erosion Legacy | `Erosion` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-FLANGER` | Flanger | `Flanger` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-FREQUENCY-SHIFTER` | Frequency Shifter | `FrequencyShifter` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-PHASER` | Phaser | `Phaser` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |
| `SURF-DEVICE-LEGACY-REDUX-LEGACY` | Redux Legacy | `Redux` | [Reviewed predecessor/file contract](../specs/legacy-native-devices.md); target parity U |

### Shipped Max devices (20)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-MAX-ALIGN-DELAY` | Align Delay | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-ENVELOPE-FOLLOWER` | Envelope Follower | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-LFO` | LFO | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-SHAPER` | Shaper | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-CLANG` | DS Clang | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-CLAP` | DS Clap | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-CYMBAL` | DS Cymbal | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-FM` | DS FM | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-HH` | DS HH | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-KICK` | DS Kick | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-SAMPLER` | DS Sampler | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-SNARE` | DS Snare | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-DS-TOM` | DS Tom | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-ENVELOPE-MIDI` | Envelope MIDI | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-EXPRESSION-CONTROL` | Expression Control | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-EXPRESSION-CONTROL-LEGACY` | Expression Control Legacy | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-MIDI-MONITOR` | MIDI Monitor | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-MPE-CONTROL` | MPE Control | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-NOTE-ECHO` | Note Echo | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |
| `SURF-MAX-SHAPER-MIDI` | Shaper MIDI | Hashed AMXD in ledger | [Partial individual device contract](../specs/max-for-live-devices.md), partial scope independently reviewed; exact-build U |

### Shipped Max MIDI tools (2)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-MAX-EUCLIDEAN` | Euclidean | Hashed AMXD in ledger | [Partial tool contract](../specs/midi-editing-tools.md); algorithm/Max-host/exact-build U |
| `SURF-MAX-VELOCITY-SHAPER` | Velocity Shaper | Hashed AMXD in ledger | [Partial tool contract](../specs/midi-editing-tools.md); algorithm/Max-host/exact-build U |

### Max templates (5)

| Surface ID | Device | Schema class / source | Specification status |
| --- | --- | --- | --- |
| `SURF-MAX-TEMPLATE-MAX-AUDIO-EFFECT` | Max Audio Effect | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-INSTRUMENT` | Max Instrument | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-MIDI-EFFECT` | Max MIDI Effect | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-MIDI-GENERATOR` | Max MIDI Generator | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |
| `SURF-MAX-TEMPLATE-MAX-MIDI-TRANSFORMATION` | Max MIDI Transformation | Hashed AMXD in ledger | [Partial host/template contract](../specs/max-for-live-hosting.md), corrected partial scope independently reviewed; runtime/API U |


## Services, controllers and platform boundaries

The [service identities](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/services-platforms.json)
pin main Live, AddOns, Index, Plugin Scanner, Web Connector, Swapper, xdelta3,
Push2DisplayProcess, Push3, Max, the Live Engine bundle and ReWire, plus plist.
Canonical helper findings already exist for
[scanner discovery](plugin-scanner-static.md), [browser indexing](browser-index-static.md),
[helper launches](helper-launch-live-side.md), [Push3](push3-helper-static.md),
[web/add-ons/updating](web-addons-swapper-static.md), and
[x86-only/ReWire/MultiF0](x86-only-bundles.md). These remain partial findings,
without full service lifecycle or failure contracts. Third party frameworks and
dependencies are recorded by the existing package/dependency inventory; their
presence must not create invented user-visible features.

The [controller/module ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/controller-profiles.json)
retains each shipped top-level MIDI Remote Script directory and its hashed
`__init__.pyc` when present. Names beginning with `_` and `ableton` are explicitly
marked support/internal; other names are discovery candidates rather than
behavioral support claims. Existing [user mapping](midi-user-mapping.md) covers a
small controller-configuration path. Push1, Push2, Push3, Move integration, NKS,
all other named scripts, hardware setup and reconnection need individual
applicability and interaction contracts. A bytecode hash proves identity only.

The target source is a macOS universal package. Separate applicability is needed
for macOS arm64, macOS x86_64 and any Windows behavior. The existing x86-only
findings prohibit assuming that ReWire's presence establishes arm64 support.
Windows behavior is not established by this package or by macOS captures.

## Feature families requiring explicit owners

These are proposed refinements to the broad feature map, not recovered behavior.
The manual section numbers below are exact locators in this captured revision.

| Proposed owner | Manual/package seeds | Missing contract |
| --- | --- | --- |
| FEAT-MIDI-TOOLS | §11; [17 tool profiles](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/midi-tools.json); schema Algorithm classes | Arpeggiate, Chop, Connect, Glissando, LFO, Ornament, Quantize, Recombine, Span, Strum, Time Warp, Velocity Shaper; Rhythm, Seed, Shape, Stacks, Euclidean; selection, defaults, randomness, undo |
| FEAT-MIDI-EDIT | §10, §12 | Note operations, probability/deviation, multi-clip focus, MPE editing and external MPE setup, separate from note storage |
| FEAT-TUNING | §3.13, §15; TuningSystem classes and shipped Tunings | Scale awareness, tuning import, reference pitch, layouts, bypass and device interaction |
| FEAT-GROOVES | §14; Groove/GroovePool/ClipGrooveSettings | Extract, preview, timing/velocity/randomness, commit and persistence |
| FEAT-RECORDING | §7.5, §19; AudioRecorder/MidiRecorder | Arm/monitor, punch/count-in, overdub, capture, quantization, Session-to-Arrangement and cancellation |
| FEAT-COMPING | §21; TakeLane/TakeLanes/LinkedTrackGroup | Take creation, audition, promoting regions, linked edits and undo |
| FEAT-RENDER | §5.1.3, §20, §38.1.4, §39 | Audio/video/MIDI export, conversion/dither, bounce, freeze/flatten, tails and cancellation |
| FEAT-MEDIA | §8.4, §9, §13, §22, §28 | Formats, decoding cache, ASD, destructive editing, reverse, warp DSP, conversion, stem separation applicability, video |
| FEAT-PROJECT-MANAGEMENT | §5 | Merge, templates, dependencies, missing files, collect, unused-file management and pack creation; ALS envelope alone leaves these open |
| FEAT-BROWSER-WORKFLOW | §3.4, §4 | Search/filter/tag editing, similarity, preview interaction, loading and browser history; index records alone leave these open |
| FEAT-RACKS | §25; four rack types and macro schemas | Chains, key/velocity/selector zones, macros, variations/randomization, Drum Rack I/O/choke and nesting |
| FEAT-DEVICE-CATALOG | §23, §29–33; 102 profiles | Each device's full interaction/state/audio contract, including legacy loading; five finite DSP releases leave most modes and Live host protocol open |
| FEAT-PLUGIN-HOST | §24; AU/VST schema types | AU/VST2/VST3 lifecycle, editor, automation/MPE, buses, latency, crashes, missing plug-ins, state and platform restrictions; discovery alone leaves these open |
| FEAT-SYNC | §37; Link settings | Link, Link Audio applicability, tempo follower, MIDI clock/timecode, sync delay, join/leave and loss recovery |
| FEAT-MAX | §32–33; Max app/templates/AMXD | Lifecycle, live API, patch state/dependencies, scheduling, edit/reload, offline/failure behavior and host security boundary |
| FEAT-CONTROLLERS | §34–36; 149 script folders and Push helpers | Controller identities, modes, display, mappings, device banks, connect/disconnect and hardware limits |
| FEAT-ACCESSIBILITY | §41–42 | Focus/order, screen reader semantics, keyboard navigation, menus, shortcuts and conflict handling |
| FEAT-SETTINGS-PLATFORM | §2, §38; plist/helpers | Authorization, updates, preferences, themes, audio/MIDI devices, sample-rate changes, performance, failure and teardown |

Arrangement editing (§6), Session follow actions (§7/16), automation recording and
override (§26/27), routing/monitoring/latency (§17/18), undo history (§5.4.2), file
recovery and desktop interactions remain gaps inside existing broad families.
The new list must not imply that previously named families are already complete.

## Concrete next draft packets

1. Reconcile the existing specifications and current releases against stable
   surface IDs and exact clauses; keep all unresolved clauses open. Keep T1.6
   pending by user decision; specification mapping does not depend on provisioning
   an implementation workspace.
2. Draft the four rack contracts from latest schemas, shipped racks and bounded
   native readers: state/chain/zones/macros first, then routing and audio. Start
   native device packets with Utility, MIDI effects, sample instruments and
   common device lifecycle, each with finite states/cases rather than one
   omnibus device spec. Amp/Cabinet host-emulation work stays deferred by the
   user's 2026-10-19 decision.
3. Draft MIDI editing/tools, groove and tuning contracts from their per-tool and
   schema inventories, keeping random seed distributions and selection/undo
   behavior unknown until supported. Separate Max tools from native algorithms.
4. Draft Arrangement editing, recording/comping, rendering/media and project
   management as workflow packets. Bind version-uncertain stem/bounce topics to
   target evidence before turning them into 12.4.3 requirements.
5. Draft platform/host/Max/controller/synchronization/UI packets, using the
   existing helper findings as seeds. Public manual prose can identify a user
   task but cannot establish sample-exact DSP, timing or recovery behavior.

Each packet must update its owning research/spec page and inventories, state
preconditions and negative/boundary/cancellation/teardown cases, and pass the
existing review/handoff workflow. Extracted execution remains available only
under the governing bounded-probe rules. Missing evidence is unknown, never a
pass; no original-versus-candidate verification or clean implementation has
been performed by this inventory.

## Focused validation

The completed capture parsed 3,634 shipped ALS/ALC/ADV/ADG documents without
parser failures. All 880 manual URL/HTML-line locators and all 412 schema
class/line locators resolve in retained bytes. The 102 device IDs are unique;
the current Erosion profile uses `Erosion2`, with legacy `Erosion` separate.
All manifest payload hashes and sizes were checked, all page-relative file
links resolve, frontmatter fields are present, and all 102 profiles have a table
row. No device profile is complete. Root integration owns this page's inbound
index, coverage, roadmap and analyst log changes.

## Independent inventory review — 2026-10-19

The [coordinator review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-review.json)
verified all twelve payload hashes/sizes, all manual URL/line and schema/class
locators, unique device IDs and no-complete statuses, plus 261 external source
hashes (715,732,194 bytes read). Approved only as an open discovery baseline.
Later draft additions and feature-map refinements do not change its frozen
source denominators; a future inventory revision must retain explicit mappings.

## Conditional observation routing — 2026-10-22

The [current family route projection](program-structure.md#conditional-observation-route-projection--2026-10-22) applies ADR0006 to the32approved frozen cuts:691X/1076S/3857O-pending/0none, observedO0. Required units without X/S are now conditionally observable after D-07, still U; no discovery denominator, complete-profile count, applicability, evidence or grade changes. The original discovery/census JSON remains frozen. Existing units retain their source IDs, contexts, schema boundaries and limitations; no per-unit source proof was repeated.

## Windows preparation and current owner routing — 2026-10-23

[The complete137-record preparation](phase4-probe-batch.md#remaining137-windows-preparation-adopted--2026-10-23) is an observation-planning companion to this inventory. It preserves the separate Windows profile, macOS/hardware/plugin dependencies and all incomplete/source-version conditions; no new surface discovery, observed outcome, platform equivalence or complete device profile follows. No original inventory manifest, source bytes, surface IDs or baseline census is changed. The [feature map](../specs/feature-map.md#current-observation-preparation--2026-10-23) points to the current partial owners and the [plan checkpoint](full-live-specification-plan.md#current-execution-checkpoint) selects work. Required unsupported behavior remains unknown and whole-Live coverage OPEN.


[Analog expanded native adoption](device-analog-dsp.md#expanded49-native-study-adopted-local-chains-and-complete-frontier--2026-10-23) carries21qualified local groups and the complete remaining dependency nomination, with no runtime/public/ABI/numerical/site-grade claim. The [next metadata cohort](device-analog-dsp.md#complete6415524-locator-cohort-selected--2026-10-23) follows the current S selection: all64destinations/155points/24sites/sixloadfields, one frozen packet/sole peer and RootCITEONLY. Existing inventory denominators, unknowns and closure rules remain unchanged; no further opaque-return scope or guest interaction is selected.


The [complete64locator metadata adoption](device-analog-dsp.md#complete64-locator-metadata-adopted-66-declarations-and-qualified-hint--2026-10-23) and [next complete66/67fragment native selection](device-analog-dsp.md#complete6667fragment-native-cohort-selected--2026-10-23) advance the existing S queue, preserving both gaps, runtime/object unknowns, one sole peer and RootCITEONLY. The newly encountered static hint authorizes only an explicitly selected target-locator lookup in the same packet, no target-body or automatic follow. [Primary-source Session0 methods](phase4-probe-batch.md#session0-capability-methods-primary-source-followup-adopted--2026-10-23) qualify future CPU/audio/video/MIDI measurements without a new approval/completeness gate, guest execution or readiness claim. Existing scope/denominators/opaquereturn limits and Claude guesthold remain unchanged; no new behavioral case, grade, site, O or closure.


[Complete66native adoption](device-analog-dsp.md#complete66-native-study-adopted-27-qualified-groups-and-cache-history--2026-10-23) preserves its27qualified groups, two return-identity refinements and failed peer cache-inspection history without bytecode-equivalence/runtime/grade proof. The [next combined63frontier/dispatch cohort](device-analog-dsp.md#complete63-frontier-and-known-dispatch-leg-selected--2026-10-23) groups the complete metadata frontier with the already admitted168-byte target body/112file-field bytes, under one freeze/sole peer and full unchanged budgets. New63destination/point/hint bodies and virtual/pointee prefixes remain unselected; raw candidates stay distinct from addresses/objects. Existing route/source denominators, case/release/site counts, unknown/closure and opaque-return limits remain unchanged.


The [combined frontier/dispatch cohort is adopted](device-analog-dsp.md#complete63-frontier-and-dispatch-adopted--2026-10-23); [complete67 native work](device-analog-dsp.md#complete67-native-frontier-selected--2026-10-23) is the current S selection. Host-only Windows archive/media preparation follows the [Phase4 record](phase4-probe-batch.md#host-only-tools-and-calibration-transfer-selected-and-adopted--2026-10-23). These studies and preparations change no inventory surface, predicate denominator or acceptance outcome; unsupported required behavior stays unknown.


[Complete67 native findings](device-analog-dsp.md#complete67-native-study-adopted-with-two-semantic-refinements--2026-10-23) are adopted with two semantic refinements and retained author/resource history. [The next combined59 cohort](device-analog-dsp.md#complete59-frontier-and-admitted-dispatch-legs-selected--2026-10-23) selects the whole metadata frontier and only already admitted unread content, with full current concurrency from the first point. These bounded static findings change no surface census, predicate denominator or acceptance outcome; required unsupported behavior stays unknown.


## Frozen S-route scope assessment and new metadata questions — 2026-10-23

The [planning projection](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/s-route-scope-assessment-2026-10-23-v1.json),205008bytes/SHA256 `445700062754564ed773693658441f0ac5a9cf7b50b5f98e1fd1c98f297a17c3`, accounts for every frozen S membership, exact census line/ID/required pointer/route pointer and unchanged family count. It derives only from the already approved [required-unit census](../../analysis/ableton-live-12.4.3/full-spec-v1/family-route-ledger-census-v1/required-units.jsonl),1816361bytes/SHA256 `6ca3275d5933198bd757b5020f3c9659e1ddbe31dee64ab9ae1338f281c993c9`, whose [sole review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-route-ledger-census-v1-review.json),15073bytes/SHA256 `1c58ffb7f52659680240ae49e8370ea315ff25783f6f7291af645e79ceb19023`, remains inherited. Root checked immutable census identity,32family membership,1076S total and exact reference preservation; no old census generator/checker, raw source/native/fixture or compatibility proof was rerun.

**1046S memberships across the31non-Analog cuts were scope-assessed**, including six zero-required-S cuts; Analog's30remain in active shared factory depth, with its whole59successor [capacity-pending](device-analog-dsp.md#complete59-resource-admission-gap-no-original-acquisition--2026-10-23). Counts remain heterogeneous existing route labels, not unread functions, atomic behaviors, newly passed requirements or a percentage. All public/runtime/native-state joins remainunknown where previouslyunknown. Narrow local rows without a listed missing join do not confer public binding. This planning assessment changes no requirement, ID, criterion, failed/unattempted history, grade, release, case count, route census or closure rule.

| Ledger family | Frozen S units | Current scope disposition |
| --- | ---: | --- |
| analog | 30 | Existing factory/shared current-value depth remains active; whole59 is capacity-pending before original acquisition. This compilation does not re-assess those30units. |
| electric | 11 | Existing loader/mappings; A1/A2/currentreceiver/output joins remain U. No new content cohort admitted in assessed metadata. |
| tension | 12 | Existing loader/mappings/default relation; public receiver/output/A1/A2 remain U. TNR022 ownerX vs ledgerS preserved. |
| corpus | 83 | Existing host/mapping/controller/modal/pickup/filter/LFO/transition/state associations; current poles/A1/public timing remain U; parked96B not extent. |
| playback | 69 | Existing clock/control/launch/MIDI/audio/stop claims; actual player/receiver/file/chunk/output and F6–F9 joins remain U. |
| collision | 10 | Existing mappings/default/modal/listening/excitor claims; A1/Type6/physicalpoles/noise-oracle/output remain U. |
| transport | 44 | Existing stores/reader/postload/writer forms; node storage/publicOpenSave/recovery/effective ranges/generalprecedence U. |
| automation | 69 | Existing storage/validation/normalization; distinct E(t)/idealP(t)/ramped samples, provider/timebase/persistence/sample delivery U. Wholecaller METADATA census selected. |
| clip-launch | 98 | 98existing narrow claims; complete20AClippostload-question nomination and separate2unaddressedSongconstructorquestions. Architecture/extent require authority. |
| midi-user | 31 | 26configuration/bytecode-associated +5native-associated units; actual ingress/currentvalue/notification/deferred-delivery/lifecycle U. |
| mix | 70 | Six units list no missing join at their local boundary;64 retain publicreceiver/provider/bus/callback/clock/load/transport joins. |
| mixer | 52 | 35general conditional units +17 specially qualified conversion/table/writer/signal/timing units; public interpolation/audio U. |
| midi-note | 52 | 18actual-load +4loadsave +9savelifecycle +10parser +7catch +3groupshape +1memberwriter classes; all4MNS053 variants remain whole metadata nomination. |
| warp | 50 | Approvedv2 governs; v1 correction-required history. One local row lacks listedjoin,49 retain completion/receiver/cache/parameter/dispatch/edit dependencies. |
| bundled-parameters | 120 | Jdoc44/Jread25/Jsave16/Jdefault14/Junit5/Jui16; storedfacts/constructormemory/emission/visiblecontrols remain distinct. |
| structure-als | 129 | 92LSSO+37ALSO; envelope acceptance/graph/activestate/media/repair/publicsave-reopen/durability joins remain U. |
| arrangement | 6 | Six stored representation units; package-to-public-edit join open. |
| audio-video-export | 0 | Zero required S units in this frozen cut; auxiliary source/file claims outside the cut add no required S credit or global-exhaustion claim. |
| browser-index | 35 | 35conditional local units/eight publicbridges; whole48Index declaration/identity/map nomination,57384declared B/77ranges, physical map U. |
| delay-reverb | 0 | Zero required S units in this frozen cut; auxiliary source/file claims outside the cut add no required S credit or global-exhaustion claim. |
| device-racks | 1 | One installed rack vocabulary/example clause, no defaults/DSP/publicroute grade. |
| distortion | 9 | Nine retained representation clauses; complete bounded source-frontier metadata remains nomination, no DSP/default proof. |
| dynamics | 20 | Twenty schema/example/Creator/MinorVersion predicates; separate context route pointers preserved. |
| filter-eq | 4 | Four retained state/schema clauses, no processing/default proof. |
| legacy-native | 8 | Eight retained schema/preset identities; D11 applicability U. |
| modulation-pitch-loop | 0 | Zero required S units in this frozen cut; auxiliary source/file claims outside the cut add no required S credit or global-exhaustion claim. |
| native-midi-effects | 0 | Zero required S units in this frozen cut; auxiliary source/file claims outside the cut add no required S credit or global-exhaustion claim. |
| plugin-discovery | 53 | Two documentary +51conditional local units/nine publicbridges; whole44retained+14historical+6table metadata nomination, failed1005a30f8U/no retry. |
| recording-comping | 8 | Eight TakeLanes/TakeId vocabulary/example predicates, no publicrecording proof. |
| sample-instruments | 0 | Zero required S units in this frozen cut; auxiliary source/file claims outside the cut add no required S credit or global-exhaustion claim. |
| synthesis-instruments | 0 | Zero required S units in this frozen cut; auxiliary source/file claims outside the cut add no required S credit or global-exhaustion claim. |
| utility | 2 | Two StereoGain vocabulary/preset clauses; G01–G06 and18edges remain public questions. |

### Coherent metadata nominations in ledger order

- **Automation:**the selected [whole immediate-M-caller frontier census](automation-envelopes.md#whole-immediate-m-caller-frontier-metadata-selected--2026-10-23) covers all ten unread fields/eight address-only references and complete unresolved control-flow/site membership. Its approved scalar summary does not enumerate the entire frontier; geometry/key gaps remainU until a permitted metadata authority supplies them. Exact architecture attribution is required;86direct CALL occurrences and36computed calls are separate, not unique target counts.
- **Clip launch:**the complete20-context AClip question is CLR-062–077/087–088/107–108, with one named later post-load hook0x102441a30 at the approved ledger's `/join_catalog/postload`. Declared extent/architecture attribution require authority before lookup or content; one hook is not an established complete constructor/load graph. The two Song-constructor contexts CLR-057/058remain a separate unnamed-loader question.
- **MIDI note storage:**all four MNS-053variants remain one class. The approved [expression-boundaries report](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/depth-midi-expression-boundaries-v1-review.json),5293bytes/SHA256 `60f16989eebef6be56fe17a0b153b3f04ae6fe9109598b605473cd1f0f779595`, `/semantic_assessment`, names two callees0x10156da64/0x10156d4c8,two interval-global keys0x105847020/0x105847028 and three unresolved slot predicates+0x3c8/+0x3d8/+0x250. Source-body native counts836/320bytes for0x10256314c/0x1025654e8do not provide exact range topology here. Unnamed transaction-helper/current-receiver/provider questions stayU; no body/pointee follows automatically.
- **Browser/Index:**the whole48retained declaration class,57384declared bytes/77discrete ranges, is nominated with all eight BIG01–08bridges. The approved source-map metadata `/retained_records/0..47`,79459bytes/SHA256 `9866a645f23a47e1cbcd8e6bc2bf33deb6854f41d9b0441d5b04d4de3e109bc7`, and10903bytechain/SHA256 `9b2850f3d12a7596835a564171c3cff11ce132fa20bf35b711daa21806ffe1c6` supply declaration/identity questions, not a physically admitted image map or native acquisition.
- **Plugin discovery:**the whole44retained identities(32Scanner+12Live),14historical-unretained identities,six historical table associations and nine PDG01–09bridges remain one metadata nomination. Source-map55481bytes/SHA256 `8be30047cb6443c40a31f457a8ef7600eff6b210e634aae9ee501b0a39ab8da6`,chain10958bytes/SHA256 `7a16f84925f9d065c6a5192e57e61608caaa71e85caeddbc46464686cf7f0c5f`; failed0x1005a30f8staysfailed/U,no retry. Native geometry remainsunknown.

Whole bounded Racks/Distortion/Dynamics/FilterEQ/Legacy/Recording metadata frontiers remain candidates within their canonical family limits, not newly selected content. Existing zero-X/readiness/legacy applicability restrictions and all unsupported predicates remain explicit; zero required S proves no global exhaustion. New finite metadata selection may resolve locator/geometry questions while preserving public behaviorU, but never authorizes automatic source/native/provider/runtime follow.

The three remaining batches accounted for192+602+146=940members, after Electric11/Tension12/Corpus83scope filing. Scope-worker history includes one initial broad census-report display exposing the beginning of an embedded owned-checker string at `/independent_checker_source`; it was not executed or reopened. Subsequent reads used explicit metadata projections. No blanket zero-helper-text-seen claim is made; no underlying source/native/image/tool/guest proof was replayed. Source maps above are inherited metadata references, not newly acquired bodies or recertified prior proofs. WholeLiveOPEN.


[The AClip named-hook locator study is now explicitly selected](clip-launch.md#aclip-post-load-locator-metadata-selected--2026-10-23), after Automation, as an independent finite metadata question. CanonicalEvidence/Reading-and-writing establishes ARM64 attribution for0x102441a30; exact extent/runtimebinding and x86counterpart remainU. This resolves the nomination’s architecture question without changing the frozen projection or claiming the hook answers all20creation/preference/member-load contexts; the2Songconstructor questions remainseparate.


The first new nominations now have sole [Automationmetadata approval](automation-envelopes.md#whole-caller-frontier-metadata-adopted--2026-10-23) and [AClipdeclaration approval with retained failure/classifier limits](clip-launch.md#failed-locator-and-qualified-recovery-metadata-adopted--2026-10-23). Four Automationbody overlaps are alreadyread/citation-only; subsequent native selections retain the whole question classes and every public/runtime unknown. These declarations change no S-unit census, case/grade/site/O/release count or completion status.


[AClip native adoption](clip-launch.md#whole-aclip-hook-native-findings-adopted--2026-10-23) qualifies local order/carriers/flags only; all20AClip+2Songpublicjoins remainU. [Automationnativev2partial](automation-envelopes.md#native-v2-partial-capture-and-protocol-breach-retained--2026-10-23) and [MNSpre-acquisition stop](midi-note-storage.md#mns-053-preparation-stopped-before-acquisition--2026-10-23) add no approved native/source coverage. Shared capacity holds further captures/audits with full contracts retained. Frozen1076S/case/grade/site/O/release counts and whole-product OPEN are unchanged.


[Automationv2solepartialrecord](automation-envelopes.md#native-v2-sole-partial-record-adopted--2026-10-23) is adopted as truthfulpartial only:fourinherited/sixguarded/onediagnostic/sevenunattempted, all18newpoststophintsquarantined/all92public-runtimequestionsretained. The separatelyselectedv3owneddiagnostic/static-tool recovery is nowposthandoffconditional, preserving oldbyteproofbycite and reviewing onlyNEWsemantic/recoveryclaims. No runtime/provider/FP/site/behavioralcase/O/release/closure credit.


[AllfourMNS053frontier metadata is adopted](midi-note-storage.md#all-four-frontier-metadata-adopted--2026-10-23):fourdisjoint836/320/16/8Bdeclarations1180B/295prospectiverows, zerobodysemantics. Twointervalglobalpointsretainwidth/value/extentU; threeproviderpredicatesremainoffsets, actualPC/target/currentreceiverU. Bothwarningclasses/allfourpublicoutcomes/r6v4criteria/oldfailures preserved. No actualsite/native/runtime/case/grade/O/release/closure credit or automaticsuccessor.


[Four current staticadoptions](index.md) qualify localregister/control/custody and metadata only: Analog59/AutoV3/Clipfrontier32B/MNS4native. Public/currentprovider/FP/runtimeandhostjoins remainU; [boundedcross-cohortsharing](program-structure.md#cross-cohort-static-reference-reconciliation--2026-10-23) changes only futurebyte-readeligibility, not S-unitcensus, case/grade/site/O/releasecounts or wholeLiveOPEN.


## Confirmed Windows handoff and sitting-first routing — 2026-10-23

[ADR0006's confirmed handoff/priority](../decisions/adr-0006-reference-observation-reopened.md#confirmed-handoff-and-windows-sitting-priority-supersede-static-queues--2026-10-23) and the [current plan checkpoint](full-live-specification-plan.md#current-execution-checkpoint), mirrored exactly in the [session handoff](session-handoff.md#current-selection), supersede earlier dated Claude-exclusive holds and active static-author/peer scheduling on this page. Root alone resumes the offline/no-NIC guest for **Session0 then all nine SessionA records**, with one sole NEW sitting-evidence/code review after freeze. Workers stay host-only; no new static follow, semantic work or queued static review runs ahead of Windows. Approved INPUT/tool/source proofs are inherited without a second proof review, and per-record unavailable prerequisites remain explicit not-observed/U rather than a new universal readiness gate.

Claude's authorized-offline Live12.4.3/build/hash, WindowsPro26300/unactivated observer profile and44.1kHz ich9HDA audio are reported handoff context, not reviewed current capability/results. The203924 authorization-session crash is separate setup history. Root records oldPID1588360 disappearing before first key and one supplied-script offline existing-disk relaunch, without reinstall/revert/duplicate process; newPID1590872/desktop is Root-reported, actual identity/results UNVERIFIED. No new Windows-key/AUZ/credentials request or NIC use is selected.

[Analog57](device-analog-dsp.md#windows-priority-parks-the-analog57-author-partial--2026-10-23) is a truthful frozen author partial; [Clip9](clip-launch.md#windows-priority-parks-the-nine-callee-review--2026-10-23) and [Automation frontier](automation-envelopes.md#windows-priority-parks-the-recovered-frontier-author-freeze--2026-10-23) are author-frozen UNREVIEWED, peers unbegun/parked. [MNS dependency](midi-note-storage.md#windows-priority-parks-the-once-census-terminal-record--2026-10-23) has a once-census terminal author freeze, with mapping/73-membership/synthesis/ordinary checker/sole peer and Automation peer unattempted. Frozen bytes, source scopes, full budgets and all failed/unattempted/ASOF histories remain unchanged; no automatic continuation. Current24,051draft additions, reviewedO0, main25,095of268,015, releases36total/19current/17superseded and wholeLiveOPEN stay exact. This scheduling amendment changes no behavioral criterion, case/grade/site/release, source denominator, opaque policy, failed-X/audio retry rule or completion rule.


Current execution uses three concurrent O/S/X workers on Session0/SessionA's document container/save path, transport state, mixer values and MIDI note storage, under user-amended plan revision6. O drives the guest alone; S and X run host-only. Each source retains its own existing adoption path, unknowns and platform labels; current authoring/observations add no reviewed coverage or resolved-site credit before their sole reviews. The inventory denominator and whole-Live OPEN rule are unchanged.
