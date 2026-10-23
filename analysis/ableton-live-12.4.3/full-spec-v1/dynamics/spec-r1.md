---
id: SPEC-DYNAMICS-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary behavior with exact-build applicability unknown
---

# Compressor, Gate, Glue Compressor, Limiter and Multiband Dynamics

## Scope, authority and evidence

This partial draft owns five individual FEAT-DEVICES profiles from the
[full product inventory](../research/full-live-coverage-inventory.md). Each has
its own stable REQ-DYN prefix; none is complete. It specifies documented controls,
displays and signal roles while keeping effective numerical behavior unresolved.
These are analyst drafts, not released implementation inputs.

[Device chains/racks](device-racks.md) owns insertion, grouping, generic bypass
and preset workflows; [Live Set structure](live-set-structure.md) owns its bounded
storage contract. [Mix graph](mix-graph.md) and [mixer values](mixer-values.md)
own their existing track scopes, not these devices' gain curves or smoothing.
[Automation envelopes](automation-envelopes.md) owns its stored-envelope subset;
its release does not resolve live control ownership here. The seven bundled-device
[host contract](bundled-device-hosting.md) does not silently include these five.

**D12** means documented by the retained official Version 12 manual captured
2026-10-19; every runtime clause has **exact 12.4.3 applicability U**. A documented
number or a matching field name does not close version parity. **Dpkg** means
observed retained installed bytes only. **U** is unresolved and ungraded. There is
no S or X claim in this packet; no original application/function or candidate ran.
The [research page](../research/dynamics-devices.md) owns evidence interpretation.

## Preconditions, inputs and comparison rules

Use one named device on a valid audio track in an editable Set. Disable unrelated
automation, modulation, mappings, rack processing, sends and downstream gain.
Explicitly choose every relevant mode/control and note displayed values; do not
rely on a preset or constructor as a neutral state. Route normal output and
sidechain separately, with no feedback and no source monitoring into the measured
output. Audition Listen is a deliberate replacement of normal output. Main
Dry/Wet and sidechain Dry/Wet are separate controls when both exist.

Case entries below retain finite requests, predicate or null oracle, provenance
and comparison scope. D12 cases test documentary predicates only, and remain
unexecuted against the target. Dpkg cases reparse retained files only. U cases
have no pass criteria; measurement requirements and a calibrated oracle must be
established before grading. Signal definitions are retained in the packet, not
claimed reference outputs. No invented dB conversion, knee/envelope equation,
latency budget, oversampling filter, audio tolerance or whole-device neutral
identity is supplied. A requirement about 'no compression' does not erase other
processing. Meter colors/roles do not imply pixel geometry, refresh rate or
calibration; source figures were not independently inspected.

UI drag cases use macOS modifiers; the manual documents Windows equivalents but
the installed target is macOS. Exact pointer distance, numeric step, accessibility
semantics, automation support per control and cross-platform parity are U. A
requested unavailable numeric value records rejection, not an invented legal
range. Canceled/malformed actions are tested only against disposable copies.

## Individual device requirements

## Compressor

### REQ-DYN-COMPRESSOR-001 — Threshold and ratio

**D12 / E1 compressor:B002, compressor:B003, compressor:B004.** Threshold sets the onset of compression; Ratio sets the documented input/output level-change relation above it. The manual illustrates ratio 3 with input increases of 3 dB and 6 dB producing output increases of 1 dB and 2 dB. Ratio 1 disables compression. These are documentary level-change examples, not calibrated steady-state or sample oracles; unrelated gain and mix processing remains separate.

### REQ-DYN-COMPRESSOR-002 — Knee

**D12 / E1 compressor:B008.** Knee controls the gradual onset of compression. At 0 dB the manual describes no compression below threshold and full compression at/above it. Its 10 dB knee, -20 dB threshold example describes onset at -30 dB and full compression at -10 dB. No interpolation formula, detector calibration or equality outcome in the effective audio is established.

### REQ-DYN-COMPRESSOR-003 — Output and automatic makeup

**D12 / E1 compressor:B005, compressor:B006, compressor:B023.** Out controls output level; the Output meter shows that level and the orange Gain Reduction meter shows gain reduction. Makeup automatically compensates for threshold/ratio changes. With external sidechain active, automatic Makeup is unavailable. Its compensation amount and transition behavior are unknown.

### REQ-DYN-COMPRESSOR-004 — Audio Dry/Wet

**D12 / E1 compressor:B007.** The main Dry/Wet balances compressed and uncompressed audio: 100% selects compressed audio and 0% is documented as effectively bypassed. This does not establish bit identity, latency cancellation, a mixing curve or a bypass ramp.

### REQ-DYN-COMPRESSOR-005 — Display modes

**D12 / E1 compressor:B009, compressor:B010, compressor:B011, compressor:B012, compressor:B018.** The display offers Collapsed, Transfer Curve and Activity views. Transfer Curve uses input level horizontally and output level vertically with dotted knee bounds. Activity shows light-gray input, with GR selecting orange reduction or Output selecting darker-gray output. Collapsed shows essential controls and hides Lin/Log.

### REQ-DYN-COMPRESSOR-006 — Attack, release and Auto Release

**D12 / E1 compressor:B013, compressor:B014.** Attack describes response toward maximum compression after exceeding threshold; Release describes recovery below threshold. Auto Release adapts release to incoming audio. Time labels do not establish time-constant definitions or an envelope function.

### REQ-DYN-COMPRESSOR-007 — Lookahead selections

**D12 / E1 compressor:B016.** Lookahead offers 0, 1 and 10 ms; delaying the input is the documented means of anticipating peaks. Actual latency, compensation, fractional-sample treatment and state when switching are unknown.

### REQ-DYN-COMPRESSOR-008 — Peak, RMS and Expand modes

**D12 / E1 compressor:B017.** Peak responds to short peaks; RMS is documented as less sensitive to very short peaks. Expand supplies upward expansion above threshold: its 1:2 example describes a 1 dB input increase yielding a 2 dB output increase; 1:1 has no expansion. These descriptions supply no RMS window or peak guarantee.

### REQ-DYN-COMPRESSOR-009 — Lin and Log envelopes

**D12 / E1 compressor:B018.** Expanded views expose Lin/Log. Lin response depends on Attack/Release; Log gives more sharply compressed peaks a faster release than less compressed material. Neither label defines the envelope mathematics.

### REQ-DYN-COMPRESSOR-010 — External trigger and gain

**D12 / E1 compressor:B020, compressor:B021, compressor:B022.** Unfolding sidechain exposes source routing. When enabled, a chosen internal routing point drives the detector. Sidechain Gain adjusts trigger input; sidechain Dry/Wet 100% uses only that source, 0% bypasses external sidechain. Normal sidechain operation does not add its audio directly to the output.

### REQ-DYN-COMPRESSOR-011 — Sidechain EQ and Listen

**D12 / E1 compressor:B024, compressor:B025, compressor:B032.** The sidechain EQ selects detector frequency content from internal or external input. The headphones button auditions only sidechain input, bypassing normal compressed output. Frequency/Q are documented in the low-pass ducking example; no filter response, listen gain or channel law is established.

### REQ-DYN-COMPRESSOR-012 — Installed schema and single-preset vocabulary

**Dpkg / E2–E3.** The latest retained 12.0_12402 schema declares Compressor2 at line 1381 with the fields listed in the appendix. One retained shipped preset has root /Ableton/Compressor2; all five sampled files declare Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. These observations establish stored vocabulary/examples only, not legal runtime ranges, enum labels, current defaults or DSP.

### REQ-DYN-COMPRESSOR-013 — Effective audio, timing and boundary behavior

**U / open outcome.** Effective threshold/knee/ratio calibration, peak/RMS/Expand detection, Lin/Log and Auto envelope functions, stereo detector linking, main/sidechain mixture laws and filter response, makeup values, exact lookahead/host compensation and control smoothing remain U.

### REQ-DYN-COMPRESSOR-014 — Automation, persistence and lifecycle

**U / open outcome.** For Compressor, parameter automation/modulation priority and ramps, undo transaction grouping, preset/save restoration, legacy migration, malformed input responses, cancellation, missing routing, transport discontinuity and deletion/teardown behavior are U. Generic chain and storage owners do not establish these device outcomes. The finite cases identify concrete unresolved outputs rather than prescribe fallback policy.

## Gate

### REQ-DYN-GATE-001 — Opening threshold and return

**D12 / E1 gate:B002, gate:B004, gate:B005.** Threshold sets gate sensitivity and can be edited by dragging its blue horizontal display line. Return is hysteresis between opening and closing levels, shown by an orange line; greater hysteresis is documented to reduce rapid chatter. Detector calibration, ties and exact return subtraction are unknown.

### REQ-DYN-GATE-002 — Flip

**D12 / E1 gate:B006.** Flip reverses gating: below-threshold audio passes. Its combination with hysteresis, Floor and envelope history does not yet have an effective numerical oracle.

### REQ-DYN-GATE-003 — Attack, Hold and Release

**D12 / E1 gate:B008, gate:B009.** Attack describes the closed-to-open transition after the signal rises above threshold. After it falls below threshold, Hold runs before closure over Release. No equality rule, envelope curve or exact sample count is established.

### REQ-DYN-GATE-004 — Floor boundaries

**D12 / E1 gate:B010.** Floor sets closed-state attenuation. The documented -inf dB endpoint mutes and 0.00 dB gives no closed-state attenuation; intermediate settings attenuate. This does not establish timing, active-state identity or numeric gain conversion.

### REQ-DYN-GATE-005 — Lookahead

**D12 / E1 gate:B007.** Gate offers Lookahead 0, 1 and 10 ms to anticipate the opening signal by delaying input. Exact latency and switching transients are unknown.

### REQ-DYN-GATE-006 — Input/output display

**D12 / E1 gate:B003, gate:B016.** The display depicts input in light gray and output in darker gray with white outline. While sidechain Listen is on, it instead shows the sidechain input level in green. Meter calibration, sampling and history length are unknown.

### REQ-DYN-GATE-007 — External sidechain

**D12 / E1 gate:B011, gate:B012, gate:B013.** Unfolding exposes Sidechain; a selected track replaces the normal gate trigger. Gain changes external trigger level; external Dry/Wet 100% uses only sidechain and 0% bypasses it. The trigger audio is not directly mixed into normal output.

### REQ-DYN-GATE-008 — Sidechain EQ and Listen

**D12 / E1 gate:B015, gate:B016.** EQ isolates trigger frequency content from the gated signal or external track. Headphones Listen auditions only trigger input in place of gate output. Filter response and listen normalization remain unknown.

### REQ-DYN-GATE-009 — Installed schema and single-preset vocabulary

**Dpkg / E2–E3.** The latest retained 12.0_12402 schema declares Gate at line 2630 with the fields listed in the appendix. One retained shipped preset has root /Ableton/Gate; all five sampled files declare Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. These observations establish stored vocabulary/examples only, not legal runtime ranges, enum labels, current defaults or DSP.

### REQ-DYN-GATE-010 — Effective audio, timing and boundary behavior

**U / open outcome.** Effective detector threshold/equality and Return hysteresis, Flip interaction, attack/hold/release curves, Floor-to-gain calibration, stereo detector linking, sidechain filtering/mix and listen gain, lookahead/host compensation and parameter smoothing remain U.

### REQ-DYN-GATE-011 — Automation, persistence and lifecycle

**U / open outcome.** For Gate, parameter automation/modulation priority and ramps, undo transaction grouping, preset/save restoration, legacy migration, malformed input responses, cancellation, missing routing, transport discontinuity and deletion/teardown behavior are U. Generic chain and storage owners do not establish these device outcomes. The finite cases identify concrete unresolved outputs rather than prescribe fallback policy.

## Glue Compressor

### REQ-DYN-GLUE-COMPRESSOR-001 — Threshold, ratio and implicit knee

**D12 / E1 glue-compressor:B002, glue-compressor:B003.** Threshold/Ratio govern compression above threshold. There is no user-adjustable knee; the documented knee becomes sharper with increasing ratio. No hardware identity or knee law follows from the analog-model description.

### REQ-DYN-GLUE-COMPRESSOR-002 — Attack/release units and Auto

**D12 / E1 glue-compressor:B004.** Attack is labeled in milliseconds, Release in seconds. Release A selects adaptive release, documented with a slower base and faster transient response. Those descriptions do not establish two constants or their combination law.

### REQ-DYN-GLUE-COMPRESSOR-003 — Dry/Wet and Range boundaries

**D12 / E1 glue-compressor:B005.** Main Dry/Wet 100% selects compressed audio and 0% is effectively bypassed. Range limits compression amount; 0 dB means no compression. This does not remove Makeup/Soft Clip, define stored Range conversion, or establish bit identity.

### REQ-DYN-GLUE-COMPRESSOR-004 — Makeup and needle

**D12 / E1 glue-compressor:B006, glue-compressor:B008.** Makeup applies compensating gain. The needle reports gain reduction in dB; its relation to Makeup is practical guidance rather than an automatic equality rule.

### REQ-DYN-GLUE-COMPRESSOR-005 — Soft Clip and indication

**D12 / E1 glue-compressor:B007, glue-compressor:B008, glue-compressor:B016.** Soft Clip enables a fixed waveshaper. The manual states a -0.5 dB maximum with Soft Clip and warns that oversampled loud peaks can still exceed 0 dB. The Clip LED is red above 0 dB output and yellow for clipped peaks with Soft Clip enabled. The exception prevents a universal output bound; waveshape and threshold calibration remain unknown.

### REQ-DYN-GLUE-COMPRESSOR-006 — Oversampling option

**D12 / E1 glue-compressor:B016.** The title-bar context menu toggles Oversampling, documented as internal processing at twice current sample rate with increased CPU use and possible output above 0 dB even with Soft Clip. No interpolation/decimation filter, scheduling or performance tolerance is established.

### REQ-DYN-GLUE-COMPRESSOR-007 — External sidechain

**D12 / E1 glue-compressor:B010, glue-compressor:B011, glue-compressor:B012.** Unfolding exposes external source routing; a chosen internal routing point drives detection. Gain changes external trigger level. External Dry/Wet 100% is external-only, 0% bypasses external sidechain; detector audio is not directly heard in normal output.

### REQ-DYN-GLUE-COMPRESSOR-008 — Sidechain EQ and Listen

**D12 / E1 glue-compressor:B013, glue-compressor:B014.** EQ restricts detector frequency content from compressed input or external source. Headphones Listen sends only sidechain input in place of compressor output. The filter and listen calibration are unknown.

### REQ-DYN-GLUE-COMPRESSOR-009 — Installed schema and single-preset vocabulary

**Dpkg / E2–E3.** The latest retained 12.0_12402 schema declares GlueCompressor at line 2670 with the fields listed in the appendix. One retained shipped preset has root /Ableton/GlueCompressor; all five sampled files declare Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. These observations establish stored vocabulary/examples only, not legal runtime ranges, enum labels, current defaults or DSP.

### REQ-DYN-GLUE-COMPRESSOR-010 — Effective audio, timing and boundary behavior

**U / open outcome.** Effective ratio-dependent knee, compression/Range/Makeup conversion, automatic envelope and stereo linking, waveshaper, oversampling filters and aliasing, Soft Clip peak caveat, sidechain filter/mix/listen, host latency and automation smoothing remain U.

### REQ-DYN-GLUE-COMPRESSOR-011 — Automation, persistence and lifecycle

**U / open outcome.** For Glue Compressor, parameter automation/modulation priority and ramps, undo transaction grouping, preset/save restoration, legacy migration, malformed input responses, cancellation, missing routing, transport discontinuity and deletion/teardown behavior are U. Generic chain and storage owners do not establish these device outcomes. The finite cases identify concrete unresolved outputs rather than prescribe fallback policy.

## Limiter

### REQ-DYN-LIMITER-001 — Ceiling, input gain and reduction meter

**D12 / E1 limiter:B002, limiter:B003, limiter:B004, limiter:B006.** Ceiling sets the documented maximum output. If incoming peaks do not exceed it, the device applies no limiting. Input Gain acts before limiting; the meter shows reduction at ceiling/threshold. This is not proof of bit identity below ceiling, effective peak calibration or universal bound under all modes.

### REQ-DYN-LIMITER-002 — Maximize relabeling and output role

**D12 / E1 limiter:B007.** Maximize changes Ceiling to Threshold and Input Gain to Output. Lowering Threshold amplifies limiter-stage output by the inverse of the Threshold value in the documented control sense; Output sets device target output level. No stored-value transform or effective gain formula is specified.

### REQ-DYN-LIMITER-003 — Release and Auto availability

**D12 / E1 limiter:B008, limiter:B009.** Release controls recovery after audio falls below ceiling/threshold; Auto adapts release continuously to input characteristics and deactivates the manual Release control. The recovery curve and adaptive state remain unknown.

### REQ-DYN-LIMITER-004 — Lookahead options and relative latency

**D12 / E1 limiter:B010.** Lookahead offers 1.5, 3 and 6 ms. Longer lookahead increases documented latency and changes attack response. Exact host compensation, sample delays and switching behavior are unknown.

### REQ-DYN-LIMITER-005 — Ceiling modes

**D12 / E1 limiter:B011.** Ceiling modes are Standard, Soft Clip and True Peak. Standard is the manual-described default, not an established 12.4.3 constructor. Soft Clip adds clipping near ceiling and an LED that flashes for clipping; True Peak is documented to prevent inter-sample peaks. Algorithms and test reconstruction are unknown.

### REQ-DYN-LIMITER-006 — L/R and M/S routing

**D12 / E1 limiter:B005, limiter:B012.** Routing selects L/R or M/S processing. M/S encodes before limiting and decodes to stereo afterward; it is documented to add latency. No mid/side normalization or latency value is established. Independent L/R processing is subject to the Link control, rather than unconditional independence.

### REQ-DYN-LIMITER-007 — Link endpoints

**D12 / E1 limiter:B005.** Link controls how much channel gain reduction is shared, for the pair selected by Routing. At 100%, either channel needing compression causes limiting in both; at 0%, channels are independent. Intermediate linking and separate mode memories are unknown.

### REQ-DYN-LIMITER-008 — Downstream gain interaction

**D12 / E1 limiter:B013.** Later processing can add gain. The documented final-output precaution is placing Limiter last in the Main chain and keeping Main volume below 0 dB. The device alone does not establish the final mixer/output ceiling.

### REQ-DYN-LIMITER-009 — Installed schema and single-preset vocabulary

**Dpkg / E2–E3.** The latest retained 12.0_12402 schema declares Limiter at line 3754 with the fields listed in the appendix. One retained shipped preset has root /Ableton/Limiter; all five sampled files declare Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. These observations establish stored vocabulary/examples only, not legal runtime ranges, enum labels, current defaults or DSP.

### REQ-DYN-LIMITER-010 — Effective audio, timing and boundary behavior

**U / open outcome.** Effective ceiling and gain calibration, release/auto response, Link interpolation, L/R and M/S normalization/coupling, Maximize gain law, Soft Clip transfer, True Peak reconstruction/bound, exact lookahead/mode latency and host compensation remain U.

### REQ-DYN-LIMITER-011 — Automation, persistence and lifecycle

**U / open outcome.** For Limiter, parameter automation/modulation priority and ramps, undo transaction grouping, preset/save restoration, legacy migration, malformed input responses, cancellation, missing routing, transport discontinuity and deletion/teardown behavior are U. Generic chain and storage owners do not establish these device outcomes. The finite cases identify concrete unresolved outputs rather than prescribe fallback policy.

## Multiband Dynamics

### REQ-DYN-MULTIBAND-DYNAMICS-001 — Band count and crossovers

**D12 / E1 multiband-dynamics:B002, multiband-dynamics:B012, multiband-dynamics:B014.** Up to three bands each support Above and Below thresholds and compression/expansion. High/Low toggles disable those bands; with both off only Mid controls incoming audio. Crossovers divide ranges: the manual uses Low=500 Hz, High=2000 Hz to illustrate low/mid/high frequency regions. No crossover order, phase or boundary gain is established.

### REQ-DYN-MULTIBAND-DYNAMICS-002 — Activators, solos and band gain ordering

**D12 / E1 multiband-dynamics:B015.** Each band has activator/solo. An inactive band bypasses its dynamics and gain controls; solo mutes other bands. Per-band Input precedes dynamics and Output follows. Bypass need not remove crossover filtering; summation and multi-solo policy are unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-003 — Meter roles

**D12 / E1 multiband-dynamics:B016.** Large bars show band output and small bars input; aligned tops denote no processing. The scale is dB. Display calibration, latency and history are unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-004 — Threshold drag and modifiers

**D12 / E1 multiband-dynamics:B017.** Dragging the left/right block edges horizontally edits Below/Above thresholds. Ctrl on Windows or Cmd on macOS edits the same threshold across bands. Alt/Option edits both thresholds of one band; Shift gives finer adjustment. Numeric step, clipping and tie rules are unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-005 — Ratio drag, modifiers and reset

**D12 / E1 multiband-dynamics:B018, multiband-dynamics:B019.** Dragging block interiors vertically edits level behavior/ratio. Ctrl/Cmd affects the same block in every band; Alt/Option affects both blocks in one band; Shift gives finer adjustment. Double-click resets selected region volume to its default; that default value is not established here.

### REQ-DYN-MULTIBAND-DYNAMICS-006 — Four processing directions

**D12 / E1 multiband-dynamics:B005, multiband-dynamics:B006, multiband-dynamics:B008, multiband-dynamics:B009, multiband-dynamics:B010, multiband-dynamics:B011, multiband-dynamics:B019.** Lowering Above volume is downward compression; raising Above is upward expansion. Lowering Below is downward expansion; raising Below is upward compression. Each edits the ratio, not a separate output-gain-only parameter. Actual transfer curves are unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-007 — Numeric editor pages

**D12 / E1 multiband-dynamics:B020.** T, B and A choose Time (attack/release), Below (threshold/ratio) and Above (threshold/ratio) columns for every band. Numeric and graphical edits expose the same documented quantities; exact conversion is unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-008 — Attack/release crossing direction

**D12 / E1 multiband-dynamics:B021, multiband-dynamics:B022.** Above attack starts after upward threshold crossing and release after downward crossing; Below attack starts after downward crossing and release after upward crossing. The same named band times describe both regions, but exact envelope combination is unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-009 — Soft Knee and RMS/Peak

**D12 / E1 multiband-dynamics:B023, multiband-dynamics:B024.** Soft Knee starts dynamics gradually approaching thresholds. Peak reacts to short peaks; RMS is less sensitive to very short crossings. Neither establishes knee width, RMS window or detector linkage.

### REQ-DYN-MULTIBAND-DYNAMICS-010 — Global Output, Time and Amount

**D12 / E1 multiband-dynamics:B025, multiband-dynamics:B026, multiband-dynamics:B027.** Global Output adjusts overall output gain. Time scales all Attack/Release durations together while retaining their relative times. Amount adjusts all-band dynamics intensity; at 0% each dynamics ratio is effectively 1. This does not bypass gains or crossover filters, specify the Amount curve, or prove whole-device identity.

### REQ-DYN-MULTIBAND-DYNAMICS-011 — External sidechain

**D12 / E1 multiband-dynamics:B029, multiband-dynamics:B030, multiband-dynamics:B031.** Unfolding Sidechain allows a selected internal routing point to replace trigger input. Gain changes external trigger level; external Dry/Wet 100% is external-only and 0% bypasses external sidechain. It is detector-only in normal output. No undocumented sidechain EQ control is required by this clause.

### REQ-DYN-MULTIBAND-DYNAMICS-012 — Sidechain Listen

**D12 / E1 multiband-dynamics:B032.** Headphones Listen auditions only sidechain input, bypassing normal device output. Its relation to band detectors and channel normalization remains unknown.

### REQ-DYN-MULTIBAND-DYNAMICS-013 — Installed schema and single-preset vocabulary

**Dpkg / E2–E3.** The latest retained 12.0_12402 schema declares MultibandDynamics at line 5279 with the fields listed in the appendix. One retained shipped preset has root /Ableton/MultibandDynamics; all five sampled files declare Creator Ableton Live 12.4d1 and MinorVersion 12.0_12402. These observations establish stored vocabulary/examples only, not legal runtime ranges, enum labels, current defaults or DSP.

### REQ-DYN-MULTIBAND-DYNAMICS-014 — Effective audio, timing and boundary behavior

**U / open outcome.** Crossover magnitude/phase and summation, band bypass and simultaneous solos, Above/Below/Amount transfer, knee/envelope/detector/linking laws, common Time scaling conversion, gain calibration, sidechain band/channel coupling and latency remain U.

### REQ-DYN-MULTIBAND-DYNAMICS-015 — Automation, persistence and lifecycle

**U / open outcome.** For Multiband Dynamics, parameter automation/modulation priority and ramps, undo transaction grouping, preset/save restoration, legacy migration, malformed input responses, cancellation, missing routing, transport discontinuity and deletion/teardown behavior are U. Generic chain and storage owners do not establish these device outcomes. The finite cases identify concrete unresolved outputs rather than prescribe fallback policy.

## Measurable acceptance and unresolved cases

The [case ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/cases.json)
is the canonical finite case expansion. Each ID names one case, even when it
contains explicitly enumerated mode variants. Every requirement has at least one
case; audio and lifecycle U requirements have several distinct boundary, negative,
automation, persistence, undo, malformed, cancellation, transport and teardown
cases per device. A list of requested observations is not a compatibility pass.

| Device | Requirements | D12 cases (target U) | Dpkg file cases | U cases | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Compressor | 14 | 11 | 1 | 15 | 27 |
| Gate | 11 | 8 | 1 | 15 | 24 |
| Glue Compressor | 11 | 8 | 1 | 16 | 25 |
| Limiter | 11 | 8 | 1 | 15 | 24 |
| Multiband Dynamics | 15 | 12 | 1 | 16 | 29 |

| Case | Requirement | Kind | Explicit action and oracle |
| --- | --- | --- | --- |
| DYN-COMPRESSOR-001 | REQ-DYN-COMPRESSOR-001 | boundary; D12 | Inspect the documented ratio-3 examples and the ratio-1 boundary. → The stated changes are respectively (3,1) dB and (6,2) dB; ratio 1 has no compression. |
| DYN-COMPRESSOR-002 | REQ-DYN-COMPRESSOR-002 | boundary; D12 | Inspect Knee=0 dB and the documented Knee=10 dB, Threshold=-20 dB example. → Documentary onset/full-compression labels match the specified endpoints; no audio grading. |
| DYN-COMPRESSOR-003 | REQ-DYN-COMPRESSOR-003 | positive; D12 | Compare external sidechain disabled/enabled while inspecting Makeup availability; inspect Out, Output meter and Gain Reduction meter. → External-sidechain use makes automatic Makeup unavailable; meter and Out roles match the description. |
| DYN-COMPRESSOR-004 | REQ-DYN-COMPRESSOR-004 | boundary; D12 | Inspect the two main Dry/Wet endpoints, 0% and 100%; keep sidechain Dry/Wet distinct. → 0% denotes effective device bypass and 100% only compressed signal. |
| DYN-COMPRESSOR-005 | REQ-DYN-COMPRESSOR-005 | positive; D12 | Select each of Collapsed, Transfer Curve and Activity; in Activity select GR then Output. → All three views and their named series/axes exist; Lin/Log is absent in Collapsed. |
| DYN-COMPRESSOR-006 | REQ-DYN-COMPRESSOR-006 | positive; D12 | Inspect Attack/Release and toggle Auto Release off/on. → The controls have the documented response roles; Auto Release denotes adaptive release. |
| DYN-COMPRESSOR-007 | REQ-DYN-COMPRESSOR-007 | boundary; D12 | Enumerate and select Lookahead 0 ms, 1 ms, 10 ms. → The three named Lookahead options are available. |
| DYN-COMPRESSOR-008 | REQ-DYN-COMPRESSOR-008 | boundary; D12 | Select Peak, RMS, Expand; inspect the documented Expand 1:2 and 1:1 examples. → Three modes exist; expansion examples have the stated level-change meaning. |
| DYN-COMPRESSOR-009 | REQ-DYN-COMPRESSOR-009 | positive; D12 | Select expanded Transfer Curve; select Lin then Log; inspect the documentary response distinction. → Lin/Log is available in expanded view and carries the documented distinction. |
| DYN-COMPRESSOR-010 | REQ-DYN-COMPRESSOR-010 | boundary; D12 | Unfold sidechain; select a second audio track as source; inspect external Dry/Wet at 0% and 100% and Gain role. → The source, gain and trigger-mixture roles match; source audio is detector-only outside Listen. |
| DYN-COMPRESSOR-011 | REQ-DYN-COMPRESSOR-011 | positive; D12 | Inspect EQ with external source off/on; choose low-pass and inspect Frequency/Q; toggle headphones Listen. → EQ acts on detector content; Listen selects sidechain input rather than compressed output. |
| DYN-GATE-001 | REQ-DYN-GATE-001 | positive; D12 | Inspect Threshold knob/blue line and Return/orange line; drag Threshold line to a displayed -20 dB. → The draggable threshold and separate return indicator represent their named quantities. |
| DYN-GATE-002 | REQ-DYN-GATE-002 | positive; D12 | Toggle Flip off/on and inspect its documented below-threshold passing role. → Flip enabled denotes reversed gate operation. |
| DYN-GATE-003 | REQ-DYN-GATE-003 | positive; D12 | Inspect Attack, Hold, Release and the documented falling-level transition order. → Hold precedes Release for closure; Attack describes opening. |
| DYN-GATE-004 | REQ-DYN-GATE-004 | boundary; D12 | Inspect Floor=-inf dB and Floor=0.00 dB while considering the closed state. → Closed-state labels denote mute and no attenuation respectively. |
| DYN-GATE-005 | REQ-DYN-GATE-005 | boundary; D12 | Enumerate/select Lookahead 0, 1, 10 ms. → Those three time selections are available. |
| DYN-GATE-006 | REQ-DYN-GATE-006 | positive; D12 | Inspect normal display then enable sidechain headphones Listen. → Normal input/output roles and green Listen trace match the description. |
| DYN-GATE-007 | REQ-DYN-GATE-007 | boundary; D12 | Inspect sidechain enable/source, Gain and external Dry/Wet endpoints 0%,100%. → Controls route/mix trigger sources with the stated endpoints. |
| DYN-GATE-008 | REQ-DYN-GATE-008 | positive; D12 | Enable EQ with internal then external trigger; toggle headphones Listen. → EQ affects detector content; Listen replaces the normal output with sidechain input. |
| DYN-GLUE-COMPRESSOR-001 | REQ-DYN-GLUE-COMPRESSOR-001 | positive; D12 | Inspect Threshold/Ratio and absence of user Knee control; compare the documented knee behavior at lower/higher ratios. → The device has no adjustable Knee; sharper knee at increasing ratio is the documentary predicate. |
| DYN-GLUE-COMPRESSOR-002 | REQ-DYN-GLUE-COMPRESSOR-002 | positive; D12 | Inspect Attack units, Release units, and select Release A. → Attack uses ms; Release uses seconds and offers A (Auto). |
| DYN-GLUE-COMPRESSOR-003 | REQ-DYN-GLUE-COMPRESSOR-003 | boundary; D12 | Inspect Dry/Wet 0%,100%, and Range 0 dB independently; do not infer complete neutral processing. → Documented endpoint roles are effective dry bypass, compressed-only, and no compression from Range respectively. |
| DYN-GLUE-COMPRESSOR-004 | REQ-DYN-GLUE-COMPRESSOR-004 | positive; D12 | Inspect Makeup and needle labels/roles. → Makeup is a gain control and needle represents gain reduction in dB. |
| DYN-GLUE-COMPRESSOR-005 | REQ-DYN-GLUE-COMPRESSOR-005 | positive; D12 | Inspect Soft Clip switch, red/yellow indicator meanings, and the oversampling exception. → Soft Clip uses a waveshaper; documented maximum carries the oversampling caveat; LED meanings match. |
| DYN-GLUE-COMPRESSOR-006 | REQ-DYN-GLUE-COMPRESSOR-006 | positive; D12 | Open context menu and inspect Oversampling off/on descriptions. → A toggle exists and documented processing-rate factor is two; no CPU percentage is graded. |
| DYN-GLUE-COMPRESSOR-007 | REQ-DYN-GLUE-COMPRESSOR-007 | boundary; D12 | Inspect external source chooser, Gain, external Dry/Wet 0%,100%. → Source/gain/mixture roles match the documented detector-only routing. |
| DYN-GLUE-COMPRESSOR-008 | REQ-DYN-GLUE-COMPRESSOR-008 | positive; D12 | Inspect EQ using internal/external source, then enable headphones Listen. → EQ affects trigger content; Listen auditions sidechain instead of compressed output. |
| DYN-LIMITER-001 | REQ-DYN-LIMITER-001 | boundary; D12 | With Maximize off, inspect Input Gain, Ceiling and Gain Reduction controls and the documented below-ceiling condition. → Input Gain precedes limiting; no limiting is documented for peaks below ceiling; meter represents reduction. |
| DYN-LIMITER-002 | REQ-DYN-LIMITER-002 | positive; D12 | Toggle Maximize off/on/off and inspect the two control labels and roles. → Off: Input Gain/Ceiling. On: Output/Threshold with the documented target-output role. |
| DYN-LIMITER-003 | REQ-DYN-LIMITER-003 | positive; D12 | Toggle Auto off/on and inspect Release availability. → Manual Release is deactivated with Auto on. |
| DYN-LIMITER-004 | REQ-DYN-LIMITER-004 | boundary; D12 | Enumerate/select 1.5, 3, 6 ms and inspect the documented latency direction. → All three selections exist; longer selections mean greater documented latency. |
| DYN-LIMITER-005 | REQ-DYN-LIMITER-005 | positive; D12 | Select Standard, Soft Clip and True Peak; inspect Soft Clip LED availability. → Three named modes exist; LED accompanies Soft Clip; True Peak has the stated inter-sample role. |
| DYN-LIMITER-006 | REQ-DYN-LIMITER-006 | positive; D12 | Select L/R then M/S; inspect processing-channel labels and documentary encode/limit/decode order. → L/R addresses left/right; M/S addresses mid/side and returns stereo; Link qualifies independence. |
| DYN-LIMITER-007 | REQ-DYN-LIMITER-007 | boundary; D12 | For each of L/R and M/S inspect Link at 0% and 100%. → 0% means independent reduction; 100% means shared limiting when either requires it. |
| DYN-LIMITER-008 | REQ-DYN-LIMITER-008 | positive; D12 | Inspect the documented Limiter-last/Main-volume precaution against a chain with later gain. → The device ceiling is not a guarantee for signal after gain-adding downstream processing. |
| DYN-MULTIBAND-DYNAMICS-001 | REQ-DYN-MULTIBAND-DYNAMICS-001 | boundary; D12 | Inspect High/Low toggles in all four on/off combinations and the 500/2000 Hz example. → Both off denotes single Mid-band operation; the example labels ranges below500,500–2000,above2000 Hz. |
| DYN-MULTIBAND-DYNAMICS-002 | REQ-DYN-MULTIBAND-DYNAMICS-002 | positive; D12 | Inspect each band activator and solo; inspect per-band Input/dynamics/Output order. → Inactive-band controls are bypassed, solo mutes others, gain controls have the stated ordering. |
| DYN-MULTIBAND-DYNAMICS-003 | REQ-DYN-MULTIBAND-DYNAMICS-003 | positive; D12 | Inspect small/large band bars and dB scale in a documented no-processing state. → Small input and large output roles match, with aligned tops in the documented no-processing condition. |
| DYN-MULTIBAND-DYNAMICS-004 | REQ-DYN-MULTIBAND-DYNAMICS-004 | positive; D12 | For Mid Above, perform an unmodified horizontal edge drag, Cmd-drag, Option-drag and Shift-drag separately from reset state. → Affected controls: Mid Above; all Above; Mid Above+Below; finer Mid Above. Windows equivalent uses Ctrl/Alt. |
| DYN-MULTIBAND-DYNAMICS-005 | REQ-DYN-MULTIBAND-DYNAMICS-005 | positive; D12 | For Mid Above interior separately perform vertical drag, Cmd-drag, Option-drag, Shift-drag, double-click. → Affected regions and reset-to-default action match the description; no reset number is supplied. |
| DYN-MULTIBAND-DYNAMICS-006 | REQ-DYN-MULTIBAND-DYNAMICS-006 | positive; D12 | Inspect the four Above/Below and raise/lower combinations. → The combinations map respectively to downward compression, upward expansion, downward expansion, upward compression. |
| DYN-MULTIBAND-DYNAMICS-007 | REQ-DYN-MULTIBAND-DYNAMICS-007 | positive; D12 | Select T then B then A. → Editors expose attack/release; Below threshold/ratio; Above threshold/ratio respectively. |
| DYN-MULTIBAND-DYNAMICS-008 | REQ-DYN-MULTIBAND-DYNAMICS-008 | positive; D12 | Inspect Above and Below crossing definitions independently. → Above and Below have the opposite crossing directions described. |
| DYN-MULTIBAND-DYNAMICS-009 | REQ-DYN-MULTIBAND-DYNAMICS-009 | positive; D12 | Toggle Soft Knee; select RMS then Peak and inspect documentary roles. → The controls have the stated gradual-onset and short-peak sensitivity roles. |
| DYN-MULTIBAND-DYNAMICS-010 | REQ-DYN-MULTIBAND-DYNAMICS-010 | boundary; D12 | Inspect global controls; set Amount=0%; compare the documented Time scaling with Mid Attack=20 ms/Release=200 ms before scaling. → Amount0% denotes dynamics ratios1, not total device bypass; Time scales both durations by a common amount. |
| DYN-MULTIBAND-DYNAMICS-011 | REQ-DYN-MULTIBAND-DYNAMICS-011 | boundary; D12 | Inspect source, Gain, external Dry/Wet at 0%,100%. → Named controls affect trigger sources; external audio is not directly mixed into normal output. |
| DYN-MULTIBAND-DYNAMICS-012 | REQ-DYN-MULTIBAND-DYNAMICS-012 | positive; D12 | Toggle headphones Listen with selected external source. → Listen selects sidechain input in place of normal processed output. |
| DYN-COMPRESSOR-012 | REQ-DYN-COMPRESSOR-012 | positive; Dpkg | {"schema_class": "Compressor2", "schema_line": 1381, "fields": ["Threshold", "Ratio", "ExpansionRatio", "Knee", "LookAhead", "Model", "LogEnvelope", "SideChain"], "preset_count": 1} → {"class_present": "Compressor2", "fields_present": ["Threshold", "Ratio", "ExpansionRatio", "Knee", "LookAhead", "Model", "LogEnvelope", "SideChain"], "creator": "Ableton Live 12.4d1", "minor_version": "12.0_12402"} |
| DYN-COMPRESSOR-013 | REQ-DYN-COMPRESSOR-013 | boundary; U | {"sequence": ["run signal S1 for 1 s", "run S0 for 1 s", "disable device for 1 s", "re-enable for 1 s"], "observe": ["sample output", "meter recovery", "click/transient", "latency"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-014 | REQ-DYN-COMPRESSOR-013 | boundary; U | {"threshold_display_dB": -20, "sequence": ["request calibrated detector levels -20.001,-20,-19.999 dB for 1 s each"], "limitation": "Calibration from sample amplitudes into detector dB is unknown; no level is presumed reached.", "observe": ["output gain", "crossing transition", "hysteresis"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-015 | REQ-DYN-COMPRESSOR-013 | boundary; U | {"sequence": ["S3", "swap left/right", "S4"], "duration_seconds_each": 1, "observe": ["gain coupling", "channel leakage", "mode memory"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-016 | REQ-DYN-COMPRESSOR-013 | boundary; U | {"sample_rates_hz": [44100, 48000, 96000], "block_sizes_samples": [1, 64, 511], "sequence": ["change only exposed lookahead/routing/oversampling options if present", "process impulse S2"], "observe": ["first affected sample", "reported host delay", "state transition"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-017 | REQ-DYN-COMPRESSOR-013 | malformed; U | {"sequence": ["select each documented endpoint in preceding requirements", "supply one nonfinite sample at index24000: NaN then +Inf then -Inf in separate runs"], "observe": ["rejection", "silence", "persistence of invalid state", "recovery"], "no_assumed_acceptance": true} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-018 | REQ-DYN-COMPRESSOR-013 | negative; U | {"main": "S3", "sidechain": "S4", "external_dry_wet_percent": [0, 100], "sequence": ["Listen off", "Listen on", "disconnect sidechain source"], "observe": ["main output", "source leakage", "meter and missing-source behavior"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-019 | REQ-DYN-COMPRESSOR-014 | automation; U | {"parameter": "Threshold", "sequence": ["create automation requests at beats0,1,2 using the three values in requested_values", "start playback", "manually edit at beat1", "re-enable automation", "stop/restart"], "observe": ["parameter value", "override indicator", "output transition"], "requested_values": [-30, -20, -10], "requested_units": "displayed dB, except Multiband Dynamics displayed Above ratio", "unresolved_input": "Legal domain, accepted values and exact beat scheduling unknown; rejection is retained, never silently replaced."} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-020 | REQ-DYN-COMPRESSOR-014 | persistence; U | {"sequence": ["Peak, Lin, Lookahead1ms, Threshold-20dB, Knee0dB", "route sidechain to audio track named Trigger at its pre-effects point if supported, recording actual accepted route", "save Set A", "save preset B", "close/reopen A", "load B into new instance"], "observe": ["control values", "display mode", "routing reference", "automation", "audio reset/history"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-021 | REQ-DYN-COMPRESSOR-014 | undo; U | {"parameter": "Threshold", "sequence": ["record explicit prior displayed value", "perform one drag", "Undo once", "Redo once", "toggle one mode", "Undo once"], "observe": ["which values return", "transaction grouping", "audio discontinuity"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-022 | REQ-DYN-COMPRESSOR-014 | malformed; U | {"input": "Separate copies of the retained one-device preset: truncate decompressed XML at midpoint; replace one documented numeric Manual Value with \"NaN\"; replace the specified code/value field with \"999\"; remove device element. Preserve originals.", "numeric_field": "Threshold/Manual/@Value", "enum_field": "Model/Manual/@Value", "observe": ["load acceptance/rejection", "error", "prior device state", "partial mutation"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-023 | REQ-DYN-COMPRESSOR-014 | cancellation; U | {"sequence": ["start preset replacement", "cancel chooser before selection", "enter hot-swap and exit without committing a choice"], "observe": ["device identity", "controls", "external routing", "automation"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-024 | REQ-DYN-COMPRESSOR-014 | cancellation; U | {"parameter": "Threshold", "sequence": ["begin mouse drag from recorded value", "press Escape before release", "release pointer"], "observe": ["value restoration or commit", "undo entry", "focus"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-025 | REQ-DYN-COMPRESSOR-014 | transport; U | {"sequence": ["process S1", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s for3cycles"], "observe": ["envelope memory", "lookahead buffer", "meter history", "first output samples"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-026 | REQ-DYN-COMPRESSOR-014 | teardown; U | {"sequence": ["play S1 with automation and external sidechain if available", "delete device while playing", "Undo deletion", "close Set during playback"], "observe": ["routing references", "automation restoration", "stale meter/audio", "tail", "error/hang"]} → U — ungraded; expected outcome unknown. |
| DYN-COMPRESSOR-027 | REQ-DYN-COMPRESSOR-014 | negative; U | {"parameter": "Threshold", "sequence": ["request text value 1e309", "request text \"nan\"", "request an empty value", "cancel text entry with Escape"], "observe": ["accepted/clamped/rejected value", "error", "prior state", "undo"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-009 | REQ-DYN-GATE-009 | positive; Dpkg | {"schema_class": "Gate", "schema_line": 2630, "fields": ["Threshold", "Return", "Hold", "Gain", "FlipMode", "LookAhead", "SideChain"], "preset_count": 1} → {"class_present": "Gate", "fields_present": ["Threshold", "Return", "Hold", "Gain", "FlipMode", "LookAhead", "SideChain"], "creator": "Ableton Live 12.4d1", "minor_version": "12.0_12402"} |
| DYN-GATE-010 | REQ-DYN-GATE-010 | boundary; U | {"sequence": ["run signal S1 for 1 s", "run S0 for 1 s", "disable device for 1 s", "re-enable for 1 s"], "observe": ["sample output", "meter recovery", "click/transient", "latency"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-011 | REQ-DYN-GATE-010 | boundary; U | {"threshold_display_dB": -20, "sequence": ["request calibrated detector levels -20.001,-20,-19.999 dB for 1 s each"], "limitation": "Calibration from sample amplitudes into detector dB is unknown; no level is presumed reached.", "observe": ["output gain", "crossing transition", "hysteresis"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-012 | REQ-DYN-GATE-010 | boundary; U | {"sequence": ["S3", "swap left/right", "S4"], "duration_seconds_each": 1, "observe": ["gain coupling", "channel leakage", "mode memory"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-013 | REQ-DYN-GATE-010 | boundary; U | {"sample_rates_hz": [44100, 48000, 96000], "block_sizes_samples": [1, 64, 511], "sequence": ["change only exposed lookahead/routing/oversampling options if present", "process impulse S2"], "observe": ["first affected sample", "reported host delay", "state transition"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-014 | REQ-DYN-GATE-010 | malformed; U | {"sequence": ["select each documented endpoint in preceding requirements", "supply one nonfinite sample at index24000: NaN then +Inf then -Inf in separate runs"], "observe": ["rejection", "silence", "persistence of invalid state", "recovery"], "no_assumed_acceptance": true} → U — ungraded; expected outcome unknown. |
| DYN-GATE-015 | REQ-DYN-GATE-010 | negative; U | {"main": "S3", "sidechain": "S4", "external_dry_wet_percent": [0, 100], "sequence": ["Listen off", "Listen on", "disconnect sidechain source"], "observe": ["main output", "source leakage", "meter and missing-source behavior"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-016 | REQ-DYN-GATE-011 | automation; U | {"parameter": "Floor", "sequence": ["create automation requests at beats0,1,2 using the three values in requested_values", "start playback", "manually edit at beat1", "re-enable automation", "stop/restart"], "observe": ["parameter value", "override indicator", "output transition"], "requested_values": [-20, -10, 0], "requested_units": "displayed dB, except Multiband Dynamics displayed Above ratio", "unresolved_input": "Legal domain, accepted values and exact beat scheduling unknown; rejection is retained, never silently replaced."} → U — ungraded; expected outcome unknown. |
| DYN-GATE-017 | REQ-DYN-GATE-011 | persistence; U | {"sequence": ["Flip on, Lookahead1ms, Threshold-20dB, Return6dB, Floor-20dB", "route sidechain to audio track named Trigger at its pre-effects point if supported, recording actual accepted route", "save Set A", "save preset B", "close/reopen A", "load B into new instance"], "observe": ["control values", "display mode", "routing reference", "automation", "audio reset/history"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-018 | REQ-DYN-GATE-011 | undo; U | {"parameter": "Floor", "sequence": ["record explicit prior displayed value", "perform one drag", "Undo once", "Redo once", "toggle one mode", "Undo once"], "observe": ["which values return", "transaction grouping", "audio discontinuity"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-019 | REQ-DYN-GATE-011 | malformed; U | {"input": "Separate copies of the retained one-device preset: truncate decompressed XML at midpoint; replace one documented numeric Manual Value with \"NaN\"; replace the specified code/value field with \"999\"; remove device element. Preserve originals.", "numeric_field": "Threshold/Manual/@Value", "enum_field": "LookAhead/Manual/@Value", "observe": ["load acceptance/rejection", "error", "prior device state", "partial mutation"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-020 | REQ-DYN-GATE-011 | cancellation; U | {"sequence": ["start preset replacement", "cancel chooser before selection", "enter hot-swap and exit without committing a choice"], "observe": ["device identity", "controls", "external routing", "automation"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-021 | REQ-DYN-GATE-011 | cancellation; U | {"parameter": "Floor", "sequence": ["begin mouse drag from recorded value", "press Escape before release", "release pointer"], "observe": ["value restoration or commit", "undo entry", "focus"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-022 | REQ-DYN-GATE-011 | transport; U | {"sequence": ["process S1", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s for3cycles"], "observe": ["envelope memory", "lookahead buffer", "meter history", "first output samples"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-023 | REQ-DYN-GATE-011 | teardown; U | {"sequence": ["play S1 with automation and external sidechain if available", "delete device while playing", "Undo deletion", "close Set during playback"], "observe": ["routing references", "automation restoration", "stale meter/audio", "tail", "error/hang"]} → U — ungraded; expected outcome unknown. |
| DYN-GATE-024 | REQ-DYN-GATE-011 | negative; U | {"parameter": "Floor", "sequence": ["request text value 1e309", "request text \"nan\"", "request an empty value", "cancel text entry with Escape"], "observe": ["accepted/clamped/rejected value", "error", "prior state", "undo"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-009 | REQ-DYN-GLUE-COMPRESSOR-009 | positive; Dpkg | {"schema_class": "GlueCompressor", "schema_line": 2670, "fields": ["Threshold", "Range", "Makeup", "PeakClipIn", "Oversample", "SideChain"], "preset_count": 1} → {"class_present": "GlueCompressor", "fields_present": ["Threshold", "Range", "Makeup", "PeakClipIn", "Oversample", "SideChain"], "creator": "Ableton Live 12.4d1", "minor_version": "12.0_12402"} |
| DYN-GLUE-COMPRESSOR-010 | REQ-DYN-GLUE-COMPRESSOR-010 | boundary; U | {"sequence": ["run signal S1 for 1 s", "run S0 for 1 s", "disable device for 1 s", "re-enable for 1 s"], "observe": ["sample output", "meter recovery", "click/transient", "latency"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-011 | REQ-DYN-GLUE-COMPRESSOR-010 | boundary; U | {"threshold_display_dB": -20, "sequence": ["request calibrated detector levels -20.001,-20,-19.999 dB for 1 s each"], "limitation": "Calibration from sample amplitudes into detector dB is unknown; no level is presumed reached.", "observe": ["output gain", "crossing transition", "hysteresis"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-012 | REQ-DYN-GLUE-COMPRESSOR-010 | boundary; U | {"sequence": ["S3", "swap left/right", "S4"], "duration_seconds_each": 1, "observe": ["gain coupling", "channel leakage", "mode memory"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-013 | REQ-DYN-GLUE-COMPRESSOR-010 | boundary; U | {"sample_rates_hz": [44100, 48000, 96000], "block_sizes_samples": [1, 64, 511], "sequence": ["change only exposed lookahead/routing/oversampling options if present", "process impulse S2"], "observe": ["first affected sample", "reported host delay", "state transition"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-014 | REQ-DYN-GLUE-COMPRESSOR-010 | malformed; U | {"sequence": ["select each documented endpoint in preceding requirements", "supply one nonfinite sample at index24000: NaN then +Inf then -Inf in separate runs"], "observe": ["rejection", "silence", "persistence of invalid state", "recovery"], "no_assumed_acceptance": true} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-015 | REQ-DYN-GLUE-COMPRESSOR-010 | negative; U | {"main": "S3", "sidechain": "S4", "external_dry_wet_percent": [0, 100], "sequence": ["Listen off", "Listen on", "disconnect sidechain source"], "observe": ["main output", "source leakage", "meter and missing-source behavior"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-016 | REQ-DYN-GLUE-COMPRESSOR-010 | boundary; U | {"Soft_Clip": [false, true], "Oversampling": [false, true], "input": "S5", "observe": ["sample maximum", "inter-sample estimates under separately pinned reconstruction", "Clip LED"], "limitation": "No reconstruction/tolerance or peak guarantee is supplied."} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-017 | REQ-DYN-GLUE-COMPRESSOR-011 | automation; U | {"parameter": "Range", "sequence": ["create automation requests at beats0,1,2 using the three values in requested_values", "start playback", "manually edit at beat1", "re-enable automation", "stop/restart"], "observe": ["parameter value", "override indicator", "output transition"], "requested_values": [-20, -10, 0], "requested_units": "displayed dB, except Multiband Dynamics displayed Above ratio", "unresolved_input": "Legal domain, accepted values and exact beat scheduling unknown; rejection is retained, never silently replaced."} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-018 | REQ-DYN-GLUE-COMPRESSOR-011 | persistence; U | {"sequence": ["Release A, Soft Clip on, Oversampling on, Range-20dB", "route sidechain to audio track named Trigger at its pre-effects point if supported, recording actual accepted route", "save Set A", "save preset B", "close/reopen A", "load B into new instance"], "observe": ["control values", "display mode", "routing reference", "automation", "audio reset/history"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-019 | REQ-DYN-GLUE-COMPRESSOR-011 | undo; U | {"parameter": "Range", "sequence": ["record explicit prior displayed value", "perform one drag", "Undo once", "Redo once", "toggle one mode", "Undo once"], "observe": ["which values return", "transaction grouping", "audio discontinuity"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-020 | REQ-DYN-GLUE-COMPRESSOR-011 | malformed; U | {"input": "Separate copies of the retained one-device preset: truncate decompressed XML at midpoint; replace one documented numeric Manual Value with \"NaN\"; replace the specified code/value field with \"999\"; remove device element. Preserve originals.", "numeric_field": "Threshold/Manual/@Value", "enum_field": "Ratio/Manual/@Value", "observe": ["load acceptance/rejection", "error", "prior device state", "partial mutation"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-021 | REQ-DYN-GLUE-COMPRESSOR-011 | cancellation; U | {"sequence": ["start preset replacement", "cancel chooser before selection", "enter hot-swap and exit without committing a choice"], "observe": ["device identity", "controls", "external routing", "automation"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-022 | REQ-DYN-GLUE-COMPRESSOR-011 | cancellation; U | {"parameter": "Range", "sequence": ["begin mouse drag from recorded value", "press Escape before release", "release pointer"], "observe": ["value restoration or commit", "undo entry", "focus"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-023 | REQ-DYN-GLUE-COMPRESSOR-011 | transport; U | {"sequence": ["process S1", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s for3cycles"], "observe": ["envelope memory", "lookahead buffer", "meter history", "first output samples"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-024 | REQ-DYN-GLUE-COMPRESSOR-011 | teardown; U | {"sequence": ["play S1 with automation and external sidechain if available", "delete device while playing", "Undo deletion", "close Set during playback"], "observe": ["routing references", "automation restoration", "stale meter/audio", "tail", "error/hang"]} → U — ungraded; expected outcome unknown. |
| DYN-GLUE-COMPRESSOR-025 | REQ-DYN-GLUE-COMPRESSOR-011 | negative; U | {"parameter": "Range", "sequence": ["request text value 1e309", "request text \"nan\"", "request an empty value", "cancel text entry with Escape"], "observe": ["accepted/clamped/rejected value", "error", "prior state", "undo"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-009 | REQ-DYN-LIMITER-009 | positive; Dpkg | {"schema_class": "Limiter", "schema_line": 3754, "fields": ["Gain", "Ceiling", "LinkAmount", "LinkAmountMidSide", "Routing", "Mode", "Maximize", "Lookahead"], "preset_count": 1} → {"class_present": "Limiter", "fields_present": ["Gain", "Ceiling", "LinkAmount", "LinkAmountMidSide", "Routing", "Mode", "Maximize", "Lookahead"], "creator": "Ableton Live 12.4d1", "minor_version": "12.0_12402"} |
| DYN-LIMITER-010 | REQ-DYN-LIMITER-010 | boundary; U | {"sequence": ["run signal S1 for 1 s", "run S0 for 1 s", "disable device for 1 s", "re-enable for 1 s"], "observe": ["sample output", "meter recovery", "click/transient", "latency"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-011 | REQ-DYN-LIMITER-010 | boundary; U | {"threshold_display_dB": -20, "sequence": ["request calibrated detector levels -20.001,-20,-19.999 dB for 1 s each"], "limitation": "Calibration from sample amplitudes into detector dB is unknown; no level is presumed reached.", "observe": ["output gain", "crossing transition", "hysteresis"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-012 | REQ-DYN-LIMITER-010 | boundary; U | {"sequence": ["S3", "swap left/right", "S4"], "duration_seconds_each": 1, "observe": ["gain coupling", "channel leakage", "mode memory"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-013 | REQ-DYN-LIMITER-010 | boundary; U | {"sample_rates_hz": [44100, 48000, 96000], "block_sizes_samples": [1, 64, 511], "sequence": ["change only exposed lookahead/routing/oversampling options if present", "process impulse S2"], "observe": ["first affected sample", "reported host delay", "state transition"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-014 | REQ-DYN-LIMITER-010 | malformed; U | {"sequence": ["select each documented endpoint in preceding requirements", "supply one nonfinite sample at index24000: NaN then +Inf then -Inf in separate runs"], "observe": ["rejection", "silence", "persistence of invalid state", "recovery"], "no_assumed_acceptance": true} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-015 | REQ-DYN-LIMITER-010 | boundary; U | {"Routing": ["L/R", "M/S"], "Link_percent": [0, 50, 100], "Ceiling_Mode": ["Standard", "Soft Clip", "True Peak"], "Maximize": [false, true], "Ceiling_or_Threshold_dB": -6, "input": "S5", "observe": ["two-channel gain", "mode latency", "overshoot", "inter-sample peak under separately pinned reconstruction"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-016 | REQ-DYN-LIMITER-011 | automation; U | {"parameter": "Ceiling/Threshold", "sequence": ["create automation requests at beats0,1,2 using the three values in requested_values", "start playback", "manually edit at beat1", "re-enable automation", "stop/restart"], "observe": ["parameter value", "override indicator", "output transition"], "requested_values": [-6, -3, -1], "requested_units": "displayed dB, except Multiband Dynamics displayed Above ratio", "unresolved_input": "Legal domain, accepted values and exact beat scheduling unknown; rejection is retained, never silently replaced."} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-017 | REQ-DYN-LIMITER-011 | persistence; U | {"sequence": ["M/S, Link50%, True Peak, Maximize on, Threshold-6dB", "route sidechain to audio track named Trigger at its pre-effects point if supported, recording actual accepted route", "save Set A", "save preset B", "close/reopen A", "load B into new instance"], "observe": ["control values", "display mode", "routing reference", "automation", "audio reset/history"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-018 | REQ-DYN-LIMITER-011 | undo; U | {"parameter": "Ceiling/Threshold", "sequence": ["record explicit prior displayed value", "perform one drag", "Undo once", "Redo once", "toggle one mode", "Undo once"], "observe": ["which values return", "transaction grouping", "audio discontinuity"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-019 | REQ-DYN-LIMITER-011 | malformed; U | {"input": "Separate copies of the retained one-device preset: truncate decompressed XML at midpoint; replace one documented numeric Manual Value with \"NaN\"; replace the specified code/value field with \"999\"; remove device element. Preserve originals.", "numeric_field": "Ceiling/Manual/@Value", "enum_field": "Mode/Manual/@Value", "observe": ["load acceptance/rejection", "error", "prior device state", "partial mutation"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-020 | REQ-DYN-LIMITER-011 | cancellation; U | {"sequence": ["start preset replacement", "cancel chooser before selection", "enter hot-swap and exit without committing a choice"], "observe": ["device identity", "controls", "external routing", "automation"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-021 | REQ-DYN-LIMITER-011 | cancellation; U | {"parameter": "Ceiling/Threshold", "sequence": ["begin mouse drag from recorded value", "press Escape before release", "release pointer"], "observe": ["value restoration or commit", "undo entry", "focus"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-022 | REQ-DYN-LIMITER-011 | transport; U | {"sequence": ["process S1", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s for3cycles"], "observe": ["envelope memory", "lookahead buffer", "meter history", "first output samples"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-023 | REQ-DYN-LIMITER-011 | teardown; U | {"sequence": ["play S1 with automation and external sidechain if available", "delete device while playing", "Undo deletion", "close Set during playback"], "observe": ["routing references", "automation restoration", "stale meter/audio", "tail", "error/hang"]} → U — ungraded; expected outcome unknown. |
| DYN-LIMITER-024 | REQ-DYN-LIMITER-011 | negative; U | {"parameter": "Ceiling/Threshold", "sequence": ["request text value 1e309", "request text \"nan\"", "request an empty value", "cancel text entry with Escape"], "observe": ["accepted/clamped/rejected value", "error", "prior state", "undo"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-013 | REQ-DYN-MULTIBAND-DYNAMICS-013 | positive; Dpkg | {"schema_class": "MultibandDynamics", "schema_line": 5279, "fields": ["SplitLowMid", "SplitMidHigh", "GlobalAmount", "GlobalTime", "SoftKnee", "EnvelopeIsPeak", "SideChain"], "preset_count": 1} → {"class_present": "MultibandDynamics", "fields_present": ["SplitLowMid", "SplitMidHigh", "GlobalAmount", "GlobalTime", "SoftKnee", "EnvelopeIsPeak", "SideChain"], "creator": "Ableton Live 12.4d1", "minor_version": "12.0_12402"} |
| DYN-MULTIBAND-DYNAMICS-014 | REQ-DYN-MULTIBAND-DYNAMICS-014 | boundary; U | {"sequence": ["run signal S1 for 1 s", "run S0 for 1 s", "disable device for 1 s", "re-enable for 1 s"], "observe": ["sample output", "meter recovery", "click/transient", "latency"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-015 | REQ-DYN-MULTIBAND-DYNAMICS-014 | boundary; U | {"threshold_display_dB": -20, "sequence": ["request calibrated detector levels -20.001,-20,-19.999 dB for 1 s each"], "limitation": "Calibration from sample amplitudes into detector dB is unknown; no level is presumed reached.", "observe": ["output gain", "crossing transition", "hysteresis"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-016 | REQ-DYN-MULTIBAND-DYNAMICS-014 | boundary; U | {"sequence": ["S3", "swap left/right", "S4"], "duration_seconds_each": 1, "observe": ["gain coupling", "channel leakage", "mode memory"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-017 | REQ-DYN-MULTIBAND-DYNAMICS-014 | boundary; U | {"sample_rates_hz": [44100, 48000, 96000], "block_sizes_samples": [1, 64, 511], "sequence": ["change only exposed lookahead/routing/oversampling options if present", "process impulse S2"], "observe": ["first affected sample", "reported host delay", "state transition"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-018 | REQ-DYN-MULTIBAND-DYNAMICS-014 | malformed; U | {"sequence": ["select each documented endpoint in preceding requirements", "supply one nonfinite sample at index24000: NaN then +Inf then -Inf in separate runs"], "observe": ["rejection", "silence", "persistence of invalid state", "recovery"], "no_assumed_acceptance": true} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-019 | REQ-DYN-MULTIBAND-DYNAMICS-014 | negative; U | {"main": "S3", "sidechain": "S4", "external_dry_wet_percent": [0, 100], "sequence": ["Listen off", "Listen on", "disconnect sidechain source"], "observe": ["main output", "source leakage", "meter and missing-source behavior"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-020 | REQ-DYN-MULTIBAND-DYNAMICS-014 | boundary; U | {"crossover_Hz": [500, 2000], "Amount_percent": [0, 100], "High_Low_enabled": [[false, false], [true, true]], "sequence": ["deactivate Mid", "solo Mid then also High", "cross low/high controls by text request"], "input": "S6", "observe": ["routing", "crossed-boundary rejection/clamp", "phase", "remaining gain and filters"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-021 | REQ-DYN-MULTIBAND-DYNAMICS-015 | automation; U | {"parameter": "Mid Above ratio", "sequence": ["create automation requests at beats0,1,2 using the three values in requested_values", "start playback", "manually edit at beat1", "re-enable automation", "stop/restart"], "observe": ["parameter value", "override indicator", "output transition"], "requested_values": [2, 3, 4], "requested_units": "displayed dB, except Multiband Dynamics displayed Above ratio", "unresolved_input": "Legal domain, accepted values and exact beat scheduling unknown; rejection is retained, never silently replaced."} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-022 | REQ-DYN-MULTIBAND-DYNAMICS-015 | persistence; U | {"sequence": ["Low500Hz/High2000Hz, RMS, Soft Knee on, Amount50%, editor B", "route sidechain to audio track named Trigger at its pre-effects point if supported, recording actual accepted route", "save Set A", "save preset B", "close/reopen A", "load B into new instance"], "observe": ["control values", "display mode", "routing reference", "automation", "audio reset/history"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-023 | REQ-DYN-MULTIBAND-DYNAMICS-015 | undo; U | {"parameter": "Mid Above ratio", "sequence": ["record explicit prior displayed value", "perform one drag", "Undo once", "Redo once", "toggle one mode", "Undo once"], "observe": ["which values return", "transaction grouping", "audio discontinuity"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-024 | REQ-DYN-MULTIBAND-DYNAMICS-015 | malformed; U | {"input": "Separate copies of the retained one-device preset: truncate decompressed XML at midpoint; replace one documented numeric Manual Value with \"NaN\"; replace the specified code/value field with \"999\"; remove device element. Preserve originals.", "numeric_field": "SplitLowMid/Manual/@Value", "enum_field": "ActiveEditMode/@Value", "observe": ["load acceptance/rejection", "error", "prior device state", "partial mutation"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-025 | REQ-DYN-MULTIBAND-DYNAMICS-015 | cancellation; U | {"sequence": ["start preset replacement", "cancel chooser before selection", "enter hot-swap and exit without committing a choice"], "observe": ["device identity", "controls", "external routing", "automation"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-026 | REQ-DYN-MULTIBAND-DYNAMICS-015 | cancellation; U | {"parameter": "Mid Above ratio", "sequence": ["begin mouse drag from recorded value", "press Escape before release", "release pointer"], "observe": ["value restoration or commit", "undo entry", "focus"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-027 | REQ-DYN-MULTIBAND-DYNAMICS-015 | transport; U | {"sequence": ["process S1", "stop at0.75s", "seek to0.25s", "restart", "loop0.25–0.75s for3cycles"], "observe": ["envelope memory", "lookahead buffer", "meter history", "first output samples"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-028 | REQ-DYN-MULTIBAND-DYNAMICS-015 | teardown; U | {"sequence": ["play S1 with automation and external sidechain if available", "delete device while playing", "Undo deletion", "close Set during playback"], "observe": ["routing references", "automation restoration", "stale meter/audio", "tail", "error/hang"]} → U — ungraded; expected outcome unknown. |
| DYN-MULTIBAND-DYNAMICS-029 | REQ-DYN-MULTIBAND-DYNAMICS-015 | negative; U | {"parameter": "Mid Above ratio", "sequence": ["request text value 1e309", "request text \"nan\"", "request an empty value", "cancel text entry with Escape"], "observe": ["accepted/clamped/rejected value", "error", "prior state", "undo"]} → U — ungraded; expected outcome unknown. |

## Cross-feature obligations and omissions

Transport, start/stop/seek/loop history, real-time versus export parity,
latency compensation, sample-rate/block-size changes, Arrangement/Session
parameter ownership, sidechain deletion/reconnection, undo and Set/preset
restoration remain open. These five devices have separate cases; the generic
rack/host specs supply no implicit successful fallback. Device activation is
separate from main Dry/Wet, Range=0 or Amount=0. No tail, reset, click-free switch,
load rejection, cancellation rollback, NaN policy or teardown deadline is invented.
Limiter's section documents no external sidechain control; this packet does not
invent one, but external routing interaction/teardown still belongs to the host.

Random distributions are inapplicable to the documented controls because no random
control is identified, while deterministic output is still unproven. Hardware
permission prompts are outside the device control description and remain an engine/
platform obligation; no missing hardware pass is asserted. Unknown target-version
applicability and all U audio/lifecycle outcomes prevent profile completion.

## Analysis-only evidence appendix

- **E1 / D12-AUDIO-EFFECTS:** official Live Version 12 audio-effect reference,
  captured 2026-10-19, original URL
  [Ableton manual](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/).
  Reuse the exact [retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html),
  SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`,
  original source identity D12-AUDIO-EFFECTS in audio-utilities/sources.json.
  The per-device blocks retain exact HTML lines and stable local B locators:
  Compressor §29.9, Gate §29.20, Glue §29.21, Limiter §29.24, Multiband §29.26.
  The manual is not an exact-build publication and is not observed execution.
- **E2 / PKG-SCHEMA:** retained installed latest schema 12.0_12402,
  [schema fields](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/schema-fields.json)
  and [source pin](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/sources.json).
  Classes/lines: Compressor2:1381, Gate:2630, GlueCompressor:2670,
  Limiter:3754, MultibandDynamics:5279. Timeable/Remoteable types are documentary
  vocabulary, not proof of exposed controls, automation or legal enum meanings.
- **E3 / bounded installed presets:** one frozen inventoried example per profile;
  exact source path, hash, byte count and retained copy are in sources.json;
  [parsed records](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/package-values.json)
  identify /Ableton/class and preserve original root attributes and field XML.
  Historical Creator 12.4d1 is preserved. Controller ranges and stored values
  are representation only, not legal GUI domains or DSP conversion.

The [requirement mapping](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/requirements.json)
provides exact block locators for each D12 clause. The
[author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/dynamics/manifest-author-r1.json)
freezes all packet payloads and both draft snapshots, with independent review
remaining a separate gate. No published handoff was changed.
