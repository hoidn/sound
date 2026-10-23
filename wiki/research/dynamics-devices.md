---
id: RES-DYNAMICS-DEVICES
type: research
status: current
updated: 2026-10-20
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Five native dynamics devices: documentary contracts and open audio behavior

## Question and canonical ownership

What observable control/routing contracts can the retained manual and bounded
installed artifacts support for Compressor, Gate, Glue Compressor, Limiter and
Multiband Dynamics? The [individual requirements](../specs/dynamics-devices.md)
own the contract; this page owns evidence interpretation and limitations. These
are five assigned partial profiles under the [coverage design](full-live-specification-design.md)
and F-06 of the [execution plan](full-live-specification-plan.md). They are not
complete profiles, releases or application compatibility results.

Consulted existing owners: [rack/chain workflows](../specs/device-racks.md),
[mix graph](../specs/mix-graph.md), [bundled hosting](../specs/bundled-device-hosting.md)
and [Utility/Tuner/Spectrum evidence](device-audio-utilities.md). No gain law,
ramp, latency or host assumption migrates from those narrower scopes into these
five devices just because the same terms occur. This packet adds no candidate
implementation and no original executable/function execution.

## Sources, capture and boundedness

The [capture program](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/capture.py)
uses the Python standard library to parse exact retained manual bytes and five
inventoried shipped presets. It reads only the latest schema and inventory
needed to identify these devices; it does not scan native binaries or execute
product code. The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/sources.json)
retains source identities, paths, dates, sizes and SHA-256 digests.

| Evidence | Identity and exact locator | Establishes | Limit |
| --- | --- | --- | --- |
| D12-AUDIO-EFFECTS | [Original official URL](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/); reused [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html), captured 2026-10-19, SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`; original identity D12-AUDIO-EFFECTS in audio-utilities/sources.json | Version 12 documented prose | Not exact 12.4.3 applicability or observed audio; source figures not separately inspected |
| PKG-SCHEMA | [Latest retained schema](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt), SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`; [five class records](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/schema-fields.json) | Installed classes/field types | No exposed control, default, legal domain, enum or DSP semantics inferred from names |
| Five bounded presets | [Retained copies, hashes and original source paths](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/sources.json); [parsed root/field records](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/package-values.json) | One stored representation per device, historical Creator metadata | No constructor defaults or full parameter domains inferred; no Set/preset was loaded in Live |

The shared HTML is an external packet dependency pinned by hash and original
source identity rather than silently copied as a fresh web capture. Five per-device
block JSON/text pairs retain paragraph identity and exact HTML line; the current
manual snapshot has 123 selected blocks:

| Device | Manual section / selected blocks | Latest class / line | Bounded shipped example |
| --- | --- | --- | --- |
| Compressor | §29.9 / 33; compressor:B001–B033 | Compressor2 / 1381 | Acoustic Kick Compressor.adv |
| Gate | §29.20 / 16; gate:B001–B016 | Gate / 2630 | Flipside.adv |
| Glue Compressor | §29.21 / 16; glue-compressor:B001–B016 | GlueCompressor / 2670 | Bass - Low Extender.adv |
| Limiter | §29.24 / 13; limiter:B001–B013 | Limiter / 3754 | Defaults/Audio Effects/Limiter.adv |
| Multiband Dynamics | §29.26 / 45; multiband-dynamics:B001–B045 | MultibandDynamics / 5279 | A Standard Multiband Comp.adv |

All five files have `MinorVersion="12.0_12402"`, `Creator="Ableton Live 12.4d1"`
and Revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. Their presence in the
pinned 12.4.3 installation establishes installed examples, not that their
historical Creator equals the application target or constructor behavior.

## Observed documentary findings

**Observed D12:** the manual distinguishes normal audio Dry/Wet from external
trigger Dry/Wet for Compressor and Glue. Sidechain audio drives detection and
is heard directly only under Listen, which replaces normal output. Compressor
also disables automatic Makeup for external-sidechain use. Gate, Glue and
Compressor document detector EQ; Multiband's captured sidechain section documents
source/Gain/Dry-Wet/Listen without adding an EQ control. Limiter's section does
not establish external sidechain controls. Exact per-claim blocks are mapped in
[requirements.json](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/requirements.json).

**Observed D12:** Compressor and Gate offer 0/1/10 ms Lookahead; Limiter offers
1.5/3/6 ms. Limiter documents greater latency for longer lookahead and M/S mode.
Glue documents a two-times internal sample-rate oversampling toggle. These values
are documented choices or rate factors, not measured delays or a prescribed
implementation filter. Sample counts, scheduling and compensation remain unknown.

**Observed D12:** Limiter's Link endpoints explicitly qualify channel interaction:
0% independent reduction versus 100% shared limiting for the selected L/R or M/S
pair (limiter:B005,B012). Therefore the L/R paragraph cannot be generalized into
unconditional channel independence. No other device in this packet has a
supported effective stereo detector/linking law.

**Observed D12:** Glue's fixed Soft Clip waveshaper has a documented -0.5 dB
maximum but an explicit oversampling exception in the same source: loud peaks
may exceed 0 dB (glue-compressor:B007,B016). The draft preserves the caveat rather
than asserting an all-mode ceiling. The waveform, reconstruction and calibration
needed for numerical testing remain unknown. Limiter's True Peak description
similarly supplies no reconstruction kernel, tolerance or test signal denominator.

**Observed D12:** Multiband Amount=0% gives an effective ratio of 1 for dynamics;
band input/output gains and crossover processing are separate. Glue Range=0 dB
means no compression while Makeup/Soft Clip remain independent. Compressor
Ratio=1 means no compression. These statements do not establish whole-device
neutral sample identity (multiband-dynamics:B015,B027; glue-compressor:B005–B007;
compressor:B004,B006–B007).

**Observed Dpkg, representation only:** selected Compressor preset stores
Threshold/Manual `0.1791548878`, Knee/Manual `0.421875`, Ratio/Manual `4` and
LookAhead/Manual `1`. Gate Flipside stores Gain/Manual `-75` and LookAhead/Manual
`0`. Glue Bass - Low Extender stores Range/Manual `25`, Ratio/Manual `1`,
PeakClipIn/Manual `true` and Oversample/@Value `true`. These differing encodings
are a concrete reason to avoid copying displayed dB values directly into every
private field or inferring enum meaning. Limiter stores Mode/Manual `0`,
Routing/Manual `0`, LinkAmount/Manual `1`, Maximize/Manual `false`; those do not
prove the user-visible labels of their codes. Multiband stores SplitLowMid/Manual
`159.999985` and SplitMidHigh/Manual `6000.00049` as example representations.
Each locator is /Ableton/class/field in package-values.json and the retained ADV.

## Draft, cases and unresolved outcomes

The preserved revision-1 packet has 62 requirements and 129 case entries: 47 D12 documentary cases,
five Dpkg file-only cases and 77 U cases. Every D12 runtime clause has target
12.4.3 applicability U. Dpkg cases establish bytes, never application acceptance.
There are 15 or more U cases per device covering effective audio and lifecycle;
none has an invented expected fallback or a passing status.

[Finite signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/fixture-signals.json)
use explicit sample amplitudes and mathematical frequencies without pretending
they are detector dB levels. The [case ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/cases.json)
retains explicit mode combinations, requested settings, signal references,
provenance, comparison rule and null unknown oracles. Requesting unavailable
values does not imply acceptance. Formula-to-audio rounding is an open probe
prerequisite. No fixture is captured device output.

Open effective laws include knee/threshold/ratio/gain calibration, envelope and
auto response, peak/RMS windows, stereo detector interaction, dry/wet and
sidechain blending, EQ, crossover filters/summation, waveshaping, oversampling,
True Peak reconstruction, latency, parameter ramps and all required state and
failure cases. Close these with independently reviewed exact-target evidence;
manual prose or controller-range metadata cannot discharge them. Required
cross-feature gaps include real-time/export parity, sample-rate changes,
Arrangement/Session ownership, reconnection, undo, save/reopen, legacy migration,
malformed/canceled loads, transport discontinuities and deletion/close.

The [frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/manifest-author-r1.json)
records every packet payload plus spec/research snapshots and external pins.
The [focused validator](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/validate.py)
checks source/locator/field integrity and requirement/case coverage. Mechanical
checks are not semantic acceptance. Separate review and root-owned catalog,
coverage, question and log updates are required before integration. No current
handoff, original evidence file or shared index was edited by this worker.

## Revision 2 current action successor

The [approved source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics-source-audit/README.md)
and [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/dynamics-source-audit-review.json)
support bounded control/history subsets. The audit reviewer is this R2 author;
ROOT independent owner review remains required, with no selfapproval. All 62
requirement IDs/body texts and all 129 original case objects remain unchanged.
The [current R2 catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/cases-r2.json)
adds 24 concrete compound/reset proposals (153 total: 47 D12, five file-only Dpkg,
101 U). All new documentary and all actual pairs are null U/unexecuted.

[The explicit overlay](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/fixtures-r2.json)
qualifies future signal negatives with genuine NONEMPTY productive normal and,
where used, independently productive detector paths; both relevant band/channel
members before loss/order. UI-only actions need no audio/hardware. Listen,
neutral-amount exceptions, N01/N02 and old finite documentary claims retain their
limits. Optional examples remain advice with no guaranteed outcome. Source is
Version12/date-only2026-10-19/UTCnull, not exact12.4.3; pixels remain uninspected.

All 27 old packet files and the seal are preserved. Existing exact spec-r1.md and
research-r1.md are reused as historical wiki providers; no redundant archive or
old-tool replay. [Consumer hash pointers](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/consumers-asof-r2.json)
retain exact as-of dependencies without rewriting consumers or introducing old
live gates/adapters. [R2 README](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/README-r2.md)
records preservation, delta, check command and current freeze. This is partial
analyst documentation, pending independent review, not product completion.


## Five-device family route map — 2026-10-20 (pending independent structure review)

The unchanged R2 owner and [final owner review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/dynamics-owner-r2-review.json) remain partial. Earlier pending-review wording above is author-time history. Root selected one [family structure/route map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-dynamics-routes-v1/structure.md) under the amended revision4 selector,extending approved1a/1b I07/I08 and approved mix/automation context. The canonical Filter/EQ scope is adjacent context only;its active map is not a dependency. No shared routing,owner,case,release or grade changes.

The [ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-dynamics-routes-v1/route-ledger.json) identifies271unique required predicates:251application predicates have no established route,20have retained-file-only S routes,and0have X routes in this selected evidence scope.142D12 source-evidence annotations reuse those predicate IDs;the413total context records are not413atomic outcomes or a frozen whole-product denominator. D12 annotations use no-established-exact-target-route,not S:Version12 source support never proves12.4.3behavior. All62clauses/153case navigation remain pinned;case counts,numeric examples,helpers and metadata do not pad predicates. Optional advice and the no-invented-Multiband-EQ scope qualifier are not extra required outcomes.

[Metadata selection](../../analysis/ableton-live-12.4.3/full-spec-v1/family-dynamics-routes-v1/query-census.json) retains32exact table associations,88selected of784available exported prefix slots,and26store candidates. Root chose whole8processor prefixes/28slots and only leading3-or-less construction/lifetime frontier slots for24model/LLimiter prefixes/60slots;696exported slots stay unselected. This is no full-class/native-extent/processing-slot claim and no arbitrary60slot slice.337aliases plus22boundary memberships=359;22named lifecycle/CalcMain seeds yield46call rows and2unresolved indirect rows. All fit declared caps;there are0new C bodies/native reads/resolved-site credits. Class names,vptrs,store candidates and method labels do not prove construction,actual receiver,current values,threshold/transfer/latency/default laws or successful lifecycle.

Limiter DeviceKit Init/Exit/CalcMain wrappers reach retained named EXTERNAL imports;their library bodies/native ABI/actual binding remain unknown. The two selected NewRate/Reset indirect sites keep empty target lists. No encountered callee/global/slot/body is expanded. Constructed unit ports do not identify actual dynamics processors,detector buffers or host output. Model/provider/entry/callback/processor identities and A1/timebase/order remain unjoined.

The [source/history scope](../../analysis/ableton-live-12.4.3/full-spec-v1/family-dynamics-routes-v1/history-scope.json) preserves the approved123block audit,38literal resources/20groups/fourquestions and24null compound/reset proposals. Full audit semantics remain inherited;pixels/destinations are not inspected.129old case objects stay exact. Productive NONEMPTY main/detector/both-band-channel premises,Listen replacement,N01/N02 calibration/rate questions,Glue oversampling caveat and Ratio1/Range0/Amount0 nonidentity stay explicit. Link endpoints retain L/R andM/S contexts;no midpoint law,latency,TruePeak reconstruction or target runtime guarantee is added. Automation/load/save/legacy/malformed/cancel/missing-route/undo/transport/delete/close remain U.

[Read-only author checks](../../analysis/ableton-live-12.4.3/full-spec-v1/family-dynamics-routes-v1/author-check.json) verify current clause/case/source pointers,selected metadata/pins and12false-promotion controls. Prior research bytes are preserved except this frontmatter date update and additive section. No original/native/binary/provider/decoder/harness/model/comparator/fixture/build/tool or old-helper execution occurred. No successor batch is selected. This author map awaits independent review;Root owns shared atlas/index/log/coverage and adoption.


## Dynamics family route review approval — 2026-10-20

Root read/adopted the complete [independent family-map review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-dynamics-routes-v1-review.json), SHA256 `34288d5250a46a28438fbc902e984cc8d3d10293723f425b914e48381d27c237`. Manifest `75e4d2a5cd3aa391b804af53603d2e12db2eb079a895b1f75c95df05094f5b06` binds13payloads/1,353,290bytes. All62clause joins/153case pointers/129old objects/24new null histories and26pins were checked. The271required predicates comprise251application predicates without an established exact-target route and20retained-file-only S predicates,zeroX. The142mirrored D12 source annotations add no required outcome and remain separate;413total contextual records are not an atomic denominator or162target-S routes.

Fresh semantic scope covers all62current clause bodies/all271predicate wording, selected setup/overlay qualifiers and complete structure/chain/census claims. The123audit spans and465selected raw rows were checked mechanically; the prior full123-block audit semantics and original case review remain inherited. Twelve false-promotion controls passed. The11,998-byte research prefix restores exactly after reversing only its authorized updated date; the4,105-byte append is preserved.

Thirty-two table associations/88selected slots from784available/26stores/337aliases plus22memberships and46call/two unresolved indirect rows are bounded metadata. Twenty-four model prefixes retain only leading-three-or-less construction/lifetime navigation;696slots remain unselected. Limiter DeviceKit EXTERNAL names do not prove a loaded provider, native ABI, current instance or callable processing route. Actual controls/receivers/detector/processed output/display/host/export, clock/calibration, error/Undo/load/lifecycle and productive audio baselines stay unknown. Ratio1/Range0/Amount0 limit only the stated dynamics; unrelated gains/mixes/crossovers/SoftClip remain separate. No native body/original execution, new indirect site, normative clause/case/release/grade or completed profile follows. Pending author prose above is history; the plan owns successor selection.


The shared [DeviceKit provider frontier](program-structure.md#devicekit-provider-frontier--2026-10-20) passed bounded independent metadata review. It owns the external-label/import/provider distinction and missing retained-input limits for these families. No actual provider/currentreceiver/control/audio binding or grade follows;required unsupported outcomes remainU. Consumer load-command work is preparation only.


The cross-family [DeviceKit fixed27 source approval](program-structure.md#devicekit-fixed27-source-review-approval--2026-10-20)
owns newly reviewed conditional wrapper/list/queue/feedback dispatch evidence.
It establishes no current control/receiver/ABI, callable DSP leaf or audio/host
route. This family's requirements, cases, grades and required unknowns are unchanged.


The [seven-delegate DeviceKit source approval](program-structure.md#devicekit-seven-delegate-source-review-approval--2026-10-20)
extends the reviewed parent source navigation. The atlas owns its signature,
callback-list and opaque-helper qualifications. Current controls, callable DSP,
public output and this family's requirements/cases/grades remain unchanged.
