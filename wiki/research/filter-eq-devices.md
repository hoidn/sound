---
id: RESEARCH-FILTER-EQ-DEVICES
type: research
status: current
updated: 2026-10-20
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3
---

# Filter and equalizer device evidence

Current R4 acceptance is selected in the final section below. Earlier counts, case tables and review-status prose are preserved R3 history; all128 original records remain unchanged.

The [filter/EQ draft](../specs/filter-eq-devices.md) is the canonical partial
behavioral owner for Auto Filter, Channel EQ, EQ Eight and EQ Three. This page
owns evidence provenance, static file observations and unresolved applicability.
Auto Filter Legacy remains a separate target-parity obligation; the
[legacy-device owner](../specs/legacy-native-devices.md#auto-filter-legacy) retains
its separately qualified predecessor/package contracts.
No original application, original function, candidate, emulator or binary
analysis ran for this packet. Static XML and HTML parsing is not DSP validation.

## Source identity and method

The packet reuses `D12-AUDIO-EFFECTS` from the
[existing audio-utilities capture](device-audio-utilities.md#captures-and-exact-locators).
Its exact [retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html)
is 588,328 bytes, SHA-256
`9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`,
original URL [Live Audio Effect Reference](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/).
The recorded capture date is 2026-10-19; an exact original HTTP fetch timestamp
was not retained and is unknown. The page says Version 12, without a publication
revision identifying 12.4.3. No second copy or fetch is used. D12 clauses stay
exact-target U even when target schema/preset names corroborate a control’s
presence. Source text is evidence data, not instructions.

The [source manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/sources.json)
records explicit external pins, source URLs/paths, capture dates, byte sizes,
SHA-256 and source version limits. A source reuse is not a new web observation.
The [bounded capture tool](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/capture.py)
checks the known HTML/schema hashes, extracts only four named sections, reads
five inventory-selected shipped presets and parses their XML with standard
library tools. It refuses changes to retained captures. Figures were not inspected.

| Manual owner | Exact retained h2 locator | Paragraph/heading records | Contract scope |
| --- | --- | ---: | --- |
| Auto Filter | §29.2 `#auto-filter`, HTML line 292 | [65 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-auto-filter-blocks.json), `auto-filter:B01–B65` | Filter/mode controls, LFO, envelope, drive/circuits, output, sidechain; not exact DSP |
| Channel EQ | §29.7 `#channel-eq`, line 684 | [12 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-channel-eq-blocks.json), `channel-eq:B01–B12` | Three bands, high-pass, adaptive/asymmetric response description, output/display |
| EQ Eight | §29.15 `#eq-eight`, line 1074 | [23 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-eq-eight-blocks.json), `eq-eight:B01–B23` | Per-band choices, modes/edit selection, graph/numeric editing, Adaptive Q, held Audition, Analyze/Scale/Oversampling |
| EQ Three | §29.16 `#eq-three`, line 1122 | [8 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manual-eq-three-blocks.json), `eq-three:B01–B08` | Band gains/enables, activity LEDs, crossovers and slope/coloration descriptions |

Block records retain normalized text, kind, exact original HTML start line and
heading anchor. Inline markup is normalized into readable text only; the source
bytes remain authoritative. The readable `manual-*.txt` files are derived aids.

## Observed target-package vocabulary

`PKG-SCHEMA` is an external pin to the inventory’s exact retained
[12.0_12402.txt](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt),
441,285 bytes, SHA-256
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
The installed source is `Contents/App-Resources/Schema/12.0_12402.txt` under the
pinned target package. [Filtered declarations](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/schema-fields.json)
retain these exact class start lines: AutoFilter 547, AutoFilter2 588,
AutoFilterLfo 657, ChannelEq 1064, Eq8 2261, Eq8Band 2304,
Eq8BandParameter 2308, Eq8SpectrumAnalyzer 2315, FilterEQ3 2480,
SideChain 7097 and SidechainRoutingDeviceHelper 7109. These are storage
vocabulary, not validation rules, runtime ranges or signal behavior.

Five compressed presets and their decompressed XML are retained under
`filter-eq/package/`. Each compressed source is rehashed against its exact
[inventory-selected example](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/devices.json).
All five identify historical Creator `Ableton Live 12.4d1`, MinorVersion
`12.0_12402`, revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`.
They are shipped content inside 12.4.3, not saves made during target execution.
[Package observations](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/package-values.json)
retain exact original file identity, root attributes and every attributed XML path.

| File/root | Selected observed strings | What remains unknown |
| --- | --- | --- |
| Defaults/Audio Effects/Auto Filter.adv → AutoFilter2 | Filter_Frequency/Manual `9999.99805`, Filter_Type `0`, Filter_Slope `1`, Filter_MorphSlope `2`, Lfo_Phase `4`, Envelope_HoldOn `true`, Output `1`, DryWet `1`, SideChainEq_Mode `5`, SideChainMono `true`, HiQuality `false` | No constructor defaults, enum maps, unit conversions, precise DSP or HiQuality meaning follows from a named default file |
| Channel EQ/Boom Capture.adv → ChannelEq | HighpassOn `false`, LowShelfGain `4.15796185`, MidGain `0.5138325095`, MidFrequency `119.999985`, HighShelfGain `0.535472393`, Gain `1.05609536` | Numeric saved gain values do not establish displayed dB mapping or shelf shape |
| Defaults/Audio Effects/EQ Eight.adv → Eq8 | Precision `0`, Mode `0`, GlobalGain `0`, Scale `1`, Bands.0/ParameterA/Freq `30`, ParameterB/Freq `40`, AdaptiveQ `true`, AdaptiveQFactor `1.12`, AdaptiveQAffectsShelves `false` | No A/B-to-L/R/M/S map, Precision-to-Oversampling map, adaptive-Q formula or legacy-shelf law |
| EQ Three/Boost HiHats.adv → FilterEQ3 | GainLo/GainMid `1`, GainHi `1.99526203`, FreqLo `464.754883`, FreqHi `2037.84412`, all band enables `true`, Slope `0`, FlatResponse `false` | No gain conversion, slope enum mapping, FlatResponse migration or flat transfer oracle |
| Legacy/Auto Filter Legacy/Auto Filter (Legacy).adv → AutoFilter | LegacyMode `false`, Cutoff `127`, LegacyQ `0.8199999928`, Resonance `0.1379310191`, Attack `6`, Release `200`; nested AutoFilterLfo and SideChain fields | Distinct saved class is supported; current AutoFilter2 control semantics do not apply by analogy. LegacyMode is not a device identity test |

Values in this table refer to `/Manual/@Value` for timeable parameters and direct
`@Value` for plain/remoteable properties; package-values.json supplies complete
paths. Manual numeric labels and XML float values need separate conversion
proof before any equality assertion joins them.

## Source discrepancies and boundaries

**Observed wording discrepancy:** `auto-filter:B59`, HTML line 422, lists
sidechain Type options low-shelf, peak, high-shelf, low-pass, band-pass, high-pass.
`B63` on the same line instead explains Notch with low-pass and high-pass, without
explaining band-pass. The draft does not infer a seven-entry union or silently
correct either passage. The complete chooser domain and enum map remain U;
the sidechain-enum case requires a retained target observation before closure.

**Observed detector-tap ambiguity:** `auto-filter:B02`, HTML line 306, says the
envelope follower responds to the filtered signal or external sidechain;
`B53`, line 390, says it uses its input source by default. Neither the schema nor
preset root establishes the internal detector stage. The AF source-ambiguity
case retains an explicit prefilter/postfilter distinction; no one tap is asserted.

**Inferred alias only where supported:** named preset root plus schema and
inventory directory support the four device identities. That is not a
per-clause reconciliation between the current manual and target build. Distinct
AutoFilter/AutoFilter2 roots justify a separate legacy obligation, not modern
behavior inherited into Legacy. The four bounded current-device sections do
not supply version-matched 12.4.3 Legacy interaction/audio evidence. The separate
[legacy-device owner](../specs/legacy-native-devices.md#auto-filter-legacy) now
retains D11 predecessor-only and package contracts; they do not establish target
parity or assign current D12 laws to Legacy. No new source search or native
investigation is claimed by this editorial correction.

Documented 6/12/24/48 dB labels do not define attenuation at the cutoff, polynomial
coefficients, Q convention, modulation smoothing or measured octave slope.
Likewise EQ Eight’s documentary doubled processing rate does not establish
resampler filters, latency or exact target operation. EQ Three’s −24 dB LED
threshold lacks detector/reference/timing calibration; threshold-neighbor
outcomes are U probes rather than graded expectations. A unity-looking EQ
setting is not a transparent-audio fixture, especially for EQ Three’s documented
48 dB coloration. No signal recipe supplies a reference render or numerical
compatibility tolerance.

## Packet completeness and review boundary

| Owner | Requirements | D12 scenarios, exact-target U | Dpkg file-only scenarios | Ungraded U scenarios | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Auto Filter | 30 | 41 | 1 | 17 | 59 |
| Channel EQ | 9 | 8 | 1 | 8 | 17 |
| EQ Eight | 17 | 20 | 1 | 12 | 33 |
| EQ Three | 9 | 9 | 1 | 9 | 19 |
| Total | 65 | 78 | 4 | 46 | 128 |

[Requirements.json](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/requirements.json)
and [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/cases.json)
retain stable IDs, device ownership, concrete setups/actions, documentary/file
expected results or null, evidence locators, comparison scope and unexecuted
state. File-only assertions are actually checked by the packet validator; case
execution labels remain unexecuted because no application scenario ran.
[Finite signal recipes](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/fixture-signals.json)
are proposed probe inputs only. The four current device profiles remain partial;
Auto Filter Legacy target interaction/audio parity remains unknown; its
predecessor/package contracts belong to the linked legacy-device owner. No denominator percentage, complete
profile, release, implementation or compatibility pass is claimed.

Automation, transport/clock changes, Set save/reopen, presets, undo/redo, invalid
text/malformed state, cancel, source failure, engine suspension, deletion and
teardown have finite per-device U scenarios. Generic host ownership is linked in
the spec. Accessibility/focus, Arrangement/Session automation ownership, platform
permissions and full engine routing/failure remain cross-feature obligations.
The freeze is ready for separate source/semantic review after focused checks;
root alone integrates indexes, coverage, questions, execution plan and log.

The [validation tool](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/validate-r3.py)
checks source hashes/sizes and preset strings, original HTML lines/text and
schema locators, requirement/case closure and lifecycle kinds, local links and
frontmatter. [Validation results](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/validation-author-r3.json)
state exactly that mechanical scope. The
[author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/manifest-author-r3.json)
pins both canonical pages and packet files for independent review; shared
catalog integration is intentionally a root responsibility, not silently claimed
by local validation.

## Review correction — revision 2

The [independent r1 review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/filter-eq-review.json)
found a vacuous modulation-fixture risk: the retained AutoFilter2 default has
`Lfo_Amount/Manual=0` and `Envelope_Amount/Manual=0` (same exact preset and XML
paths retained above). A source signal alone does not activate either path.
Revision 2 defines proposed isolated LFO/envelope setups with accepted nonzero
tested amounts, the other amount zero, suitable active filtering and nonmuted
wet output. It requires independently observed curve and output response before
comparisons and marks missing/indeterminate baselines U. Spin gray-state checks
remain UI-only; separate AF-C058/059 retain stochastic sound outcomes as U.
No new reference observation or supported numeric control domain is claimed.

The included Peak in EQ8-C018 now requires accepted nonzero gain and two distinct
accepted Scale values plus observable baseline. EQ3-C005–007 now require a stable
lit LED before disabling the respective band while holding input constant.
Scaling law, saved-value mutation, LED calibration and detector timing remain U.
The [author response](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/review-response-r2.json)
identifies all corrected scenarios and remaining limits.

The exact r1 seal (SHA-256
`0f25052e22eacc205ba7bf5d5a902027c1902051e3174e9c66f1ab22fcc3c49e`)
and all its 29 payloads were copied and rehashed before edits under
[revisions/author-r1](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/revisions/author-r1/manifest-author-r1.json),
with original repository-relative paths preserved beneath that directory. The
root r1 manifest is unchanged; its archived payloads provide its historical
resolution after mutable pages advance. The r2 seal is separate and all seven
original source identities remain unchanged. Counts are 65 requirements and 128
scenarios (78 D12, 4 file-only, 46 U). Neither revision has application execution,
a numerical sound oracle, complete profile or target compatibility pass.

## Revision 3 legacy provenance correction

The legacy source-absence wording now refers specifically to version-matched
12.4.3 interaction/audio evidence. The separately qualified D11 predecessor-only
and package contracts are routed to the legacy-device owner; no current D12 law
is borrowed and target parity remains U. All 65 requirement and 128 case records
and original evidence bytes are unchanged. The exact
[r2 seal and 30 payloads](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/revisions/author-r2/manifest-author-r2.json)
and prior r1 history are preserved. The
[response](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/response-author-r3.json)
records the editorial-only delta. Prior semantic review retains its original
partial scope; this is no runtime or whole-profile completion claim.

## R4 bounded control-history adoption

The independently reviewed [full four-section source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq-source-audit/README.md) and [review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/filter-eq-source-audit-review.json) support twelve bounded future histories. The current [catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/cases-r4.json) contains65unchanged requirement IDs and140cases:90D12 documentary proposals, four unchanged historical file-only Dpkg assertions and46U. All128old case objects and all99old packet/history files remain exact; no old requirement body is changed. Twelve new documentary/actual pairs are null/U/unexecuted, without a numerical or signal comparator.

Use independently owned valid editable audio-track/device targets and separate exact original reset copies. Record accepted controls, source/route/mode/selection, filter settings, both relevant input identities, wet/output and transport context. UI-only inspection/editing needs no audio. Every signal/absence/no-effect comparison requires actual NONZERO source and independently productive tested-control contribution through active nonmuted processed output BEFORE the contrast; flags, a preset or a mathematical signal definition are insufficient. Preserve existing AF-AUDIO/LFO/ENV isolation and accepted-value preflights, other modulator zero, genuine filter-curve AND output response and recheck after every mode/source override. Missing or failed prerequisites remain U.

| New case | Audit group | Bounded action |
| --- | --- | --- |
| AF-C060 | FEA-G01 | Actual LFO waveform and shape operations |
| AF-C061 | FEA-G02 | Productive resonance before Resampling contrast |
| AF-C062 | FEA-G03 | Productive circuit before unsupported-filter contrast |
| AF-C063 | FEA-G04 | Explicit internal and external Listen histories |
| AF-C064 | FEA-G05 | Actually select all three external tapping points |
| AF-C065 | FEA-G06 | Actual sidechain frequency and Q edits |
| CEQ-C018 | FEA-G07 | Channel EQ on two productive Drum Rack pads |
| EQ8-C034 | FEA-G08 | Actual edits in expanded eight-filter view |
| EQ8-C035 | FEA-G09 | Direct Gain and Q number-field entries |
| EQ8-C036 | FEA-G10 | Scale histories for both shelf types |
| EQ8-C037 | FEA-G11 | Genuine two-filter Audition history |
| EQ3-C020 | FEA-G12 | Productive EQ Three band and coloration histories |

Each full action, prerequisite, exact source quote/pointer and remaining limit is in the current structured catalog and [adoption ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/adoption-r4.json). These histories distinguish actual selections/edits from enumeration or inspection. Res and Circuit require independently productive controls in an eligible mode before ineligible no-effect branches; Listen separates internal and explicitly enabled external routes; both shelf Scale histories and both Audition contributions must be genuinely productive. Allthree existing lit-LED histories remain unchanged.

Both Auto Filter source ambiguities, stochastic/reset and every old lifecycle U remain open. No modern Auto Filter law transfers to Legacy; its qualified D11/package route retains exact-target U. No waveform, gain, Q, filter coefficient, detector, FFT, CPU, geometry, timing, codec, file transaction, default or cleanup law is added. No original/vendor/native/UI/audio/MIDI/hardware/network/install/candidate executed.

The [R4 integrity guide](../../analysis/ableton-live-12.4.3/full-spec-v1/filter-eq/README-r4.md) pins exact before/current providers and qualified historical consumers without replay or adapters. AS-OF AUTHOR FREEZE: independent R4 review pending; shared indexes own current disposition. No complete profile, compatibility pass or release follows.


## Four-device family route map — 2026-10-20

**Pending independent structure review.** The [bounded family cut](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/README.md)
extends approved component/class recovery and integration I07/I08, with existing
Utility, mix, automation and device-host boundaries. It uses the independently
approved R4 owner: 65 requirement bundles and 140 case pointers, including all
128 historical objects and twelve null/U/unexecuted action additions. The
[ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/route-ledger.json)
separately inventories the 46 existing U action contexts. These units are not
atomic source facets, a complete family/product denominator or a behavior grade.
Four S routes support retained file/schema strings only; the other 61 bundles
have no established exact-target public route. D12 remains current-manual
context without exact 12.4.3 applicability; historical 12.4d1 files are not current
constructor defaults, working modulation or audio behavior.

A fixed [census and selection](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/query-census.json)
precedes materialization. Seven exact table prefixes/21 slots, ten store
candidates, 177 memberships and 202 aliases stay within the declared caps.
The [native metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/metadata-rows.jsonl)
and [call data](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/call-rows.jsonl)
retain exact byte/line/hash locators. The 453 call/jump records comprise 429
unconditional calls and 24 jumps; 39 additional indirect sites remain unresolved,
with zero new resolution credit. Literal types, three-slot prefixes, store
candidates and callback names are not render methods or public-control/instance
proofs. AutoFilter2/ChannelEq sample-rate wrapper edges end at externally resolved
device-kit symbol frontiers; bodies and actual public processing remain unjoined.
Two EQ Eight edges to external exp10f are auxiliary math dependencies, not a
public gain/Mode law. No fixed edge uniquely nominates a shared Biquad coefficient
body; that universe is not materialized. Legacy AutoFilter stays separate.

The [input/context sets](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/input-sets.json)
retain productive nonzero source/control/wet-output prerequisites, isolated
AF-AUDIO/LFO/ENV and rechecks, external/Listen/tapping identities, Hold attack
outlasting the pulse, two productive Audition contributions and actual
press/hold/release, prior lit-LED baselines and unknown return/cleanup states.
All four source questions and approved 108-block audit semantics remain qualified.
No enum, neutral state, detector choice, transfer/FFT/coefficient, latency,
smoothing, stochastic or timing law follows by analogy. Missing joins remain
unknown rather than absence. [Source locators](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/source-locators.json)
and the [new read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/family-filter-eq-routes-v1/check.py)
preserve exact owner/case/source identities and false-promotion controls. No new
native body/source expansion, binary/provider/decoder/harness/original/model/
comparator/fixture generation/build, old-module import or candidate execution
occurs. No owner, case, grade or release changes; root owns the seal, independent
review and shared atlas/index/log routing.


## Filter/EQ family route review approval — 2026-10-20

Root read/adopted the complete [independent family-map review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-filter-eq-routes-v1-review.json), SHA256 `6f42e1798baed4fb495a4cfb3e23c27bd7d49d2b421568b654b81653e6e64cab`. Manifest `0e7a16a3f811137985942a492fad865c7e24492636941b048bff36e279b7fcce` binds14payloads/1,110,843bytes. All65whole-clause bundles/140case pointers/46existingU action contexts were checked as separate inventory units:four historical-file-only S routes/61none/zeroX, with every public exact-target runtime outcomeU. Twenty-five pins/532metadata plus492call-indirect rows/25chain joins/108source-context locators/16file strings and13negative controls passed;41paths/1,024slices and the authorized date-only prefix/additive append remained exact.

Fresh semantic scope covers all65contract summaries and17chain edges plus selected R4 action histories. Full108manual-block semantics and the earlier owner R4 judgments remain inherited; this is not another complete140-action semantic audit. Seven table prefixes/21slots/ten stores/379aliases-memberships are metadata;39additional indirect sites remain unresolved. AutoFilter2/ChannelEq device-kit symbol dependencies and two EQ Eight external exp10f references are not native coefficient/render/control laws or complete callable X routes. Shared Biquad names select no unique body. Separate legacy AutoFilter/file vocabulary does not prove current or legacy parity.

Productive source/nonzero control/wet-output, isolated modulators, AF curve-and-output checks, Hold attack outlasting pulse, both productive Audition contributions/actual press-hold-release and stable-lit EQThree LED baselines stay prerequisites. Detector tap/Type ambiguity, Audition return/cleanup, numeric transfer/Scale/adaptiveQ/neutrality/latency, actual receiver/control/sidechain/output/display and error/lifecycle joins remain unknown. No new native body/original execution, site credit, normative clause/case/release/grade or completed profile follows. Pending author prose above retains its historical status; the current plan owns any successor selection.


The shared [DeviceKit provider frontier](program-structure.md#devicekit-provider-frontier--2026-10-20) passed bounded independent metadata review. It owns the external-label/import/provider distinction and missing retained-input limits for these families. No actual provider/currentreceiver/control/audio binding or grade follows;required unsupported outcomes remainU. Consumer load-command work is preparation only.


The cross-family [DeviceKit fixed27 source approval](program-structure.md#devicekit-fixed27-source-review-approval--2026-10-20)
owns newly reviewed conditional wrapper/list/queue/feedback dispatch evidence.
It establishes no current control/receiver/ABI, callable DSP leaf or audio/host
route. This family's requirements, cases, grades and required unknowns are unchanged.


The [seven-delegate DeviceKit source approval](program-structure.md#devicekit-seven-delegate-source-review-approval--2026-10-20)
extends the reviewed parent source navigation. The atlas owns its signature,
callback-list and opaque-helper qualifications. Current controls, callable DSP,
public output and this family's requirements/cases/grades remain unchanged.
