---
id: SPEC-EXTERNAL-HARDWARE-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary behavior with exact-build applicability unknown
---

# External Instrument and External Audio Effect

## Scope and authority

This partial F-06/F-09 draft owns the individual routing/control behavior of
`SURF-DEVICE-EXTERNAL-AUDIO-EFFECT` and `SURF-DEVICE-EXTERNAL-INSTRUMENT`.
The [full coverage design](../research/full-live-specification-design.md) governs
closure; [research](../research/external-hardware-devices.md) owns source
interpretation and installed-presence limits. Neither profile is complete or
released for implementation.

**D12** is prose in the retained official Version 12 manuals captured 2026-10-19.
All runtime clauses have **exact 12.4.3 applicability U**. **Dpkg** observations
prove schema/inventory presence only, not behavioral aliases or runtime fields.
All 56 case `expected` values are null and every case is unexecuted. Twenty
cases retain documentary control/state proposals; ten signal probes and 26
lifecycle probes have null documentary expectations and comparators. There is
no S/X execution, hardware experiment or original-versus-candidate result.

[Device chains/racks](device-racks.md) owns common insertion, bypass, presets and
chain composition; [plug-in hosting](plugin-hosting.md) owns its bounded host
workflows. A qualifying multitimbral plug-in and its auxiliary outputs are
prerequisites here, not a promise of arbitrary plug-in support. [Audio/video
export](audio-video-export.md), especially REQ-EXPORT-019–022, owns real-time
versus offline rendering, countdown, restart and render cancellation. Do not
classify a render solely from either device's presence or duplicate its laws here.

[Mix graph](mix-graph.md) explicitly excludes general routing/monitoring,
latency-reporting devices, real-time scheduling and the physical audio-device
stage. Its finite mixer laws are not evidence for these round trips or latency
compensation. [Automation](automation-envelopes.md), [MIDI configuration](midi-user-mapping.md),
[transport](transport-state.md), [clip launch](clip-launch.md) and
[recording/comping](recording-comping.md) retain their bounded owners; none
closes these devices' automation, MIDI delivery, active-clip or recording/render
interactions. Global audio preferences/driver lifecycle and general routing
remain separate open engine/control scope.

## Controlled inputs and observable state

Use a valid editable test-owned Set and explicitly admitted settings. The
[fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/fixtures.json)
separate physical hardware, qualifying internal plug-in, owned audio/MIDI and
selected-unit rate setups. Port identity, enabled channel, active monitoring,
source and nonmuted return/output must be independently established before any
signal claim. Hardware/plug-in availability is an unproven prerequisite on this
analyst host; a selected name or schema class is insufficient.

All signal/no-effect/silence probes need a paired positive baseline, active
device, admitted nonzero relevant send/return gain and appropriate source.
External Audio Effect also needs nonzero wet contribution; an interior mix is
needed to distinguish dry from processed-return behavior. External Instrument
does not inherit a Dry/Wet or separate send-Gain control from the effect.
Dry-only monitoring, absent carrier/note, muted return, zero gain or unavailable
hardware supplies no evidence about an active path. No baseline was captured.

The proposed 128 samples, 2.5 ms, 48/44.1 kHz and 120 BPM are authored finite
inputs, not product ranges or constructor defaults. If entry or rate change
is unavailable or not representable, the documentary case remains unexecuted.
Selected-unit retention is separate from physical alignment and cross-unit
conversion; no rounding law, tolerance, gain coefficient or MIDI byte codec is
established. All measurements of actual returned signals remain unknown.

## Individual requirements

Every D12 row below is target-U. Evidence names exact blocks in the packet,
including the retained HTML line and major-release source identity.

### External Audio Effect

Surface `SURF-DEVICE-EXTERNAL-AUDIO-EFFECT`; frozen discovery association `BufferAudioDevice` at schema line 939 is inferred presence only, not a behavioral/runtime alias.

| Requirement | Preconditions, documented result and limits | Evidence |
| --- | --- | --- |
| REQ-EHW-EA-001 | **D12.** With External Audio Effect in an audio path, Audio To selects physical audio outputs to the external processor and Audio From selects physical inputs returning its processed signal. This is a hardware-routing effect; the section supplies no internal effect algorithm. | external-audio-effect:B002, external-audio-effect:B003 |
| REQ-EHW-EA-002 | **D12.** Available Audio To and Audio From choices depend on Audio Settings. Configure… at the bottom of each chooser reaches those settings. No complete port domain, mono/stereo grouping, order or unavailable-port policy is specified. | external-audio-effect:B003 |
| REQ-EHW-EA-003 | **D12.** A Peak level indicator below each chooser shows the highest attained audio level; clicking an indicator resets it. Measurement convention, observation window, reset sentinel and update timing are unknown. | external-audio-effect:B004 |
| REQ-EHW-EA-004 | **D12.** Separate Gain knobs beside the choosers adjust the level going out to the processor and the level coming back into Live. Gain domains, dB-to-amplitude law and clipping behavior are unknown. | external-audio-effect:B005 |
| REQ-EHW-EA-005 | **D12.** Dry/Wet controls the balance of dry and externally processed signals; the manual recommends 100% when placed on a return track. This recommendation is not a mandatory insertion setting or a specified mixing law. | external-audio-effect:B006 |
| REQ-EHW-EA-006 | **D12.** Invert applies phase inversion to the processed signal returning into Live. No phase convention, channel matrix, numeric negation rule or dry-path sample comparator is established. | external-audio-effect:B007 |
| REQ-EHW-EA-007 | **D12.** Hardware Latency allows manual compensation for hardware delay not automatically detected by Live. Its adjacent button selects milliseconds or samples. Sample fine tuning followed by a return to milliseconds before a rate change is documented guidance; conversion, range and precision are unknown. | external-audio-effect:B008 |
| REQ-EHW-EA-008 | **D12.** When Hardware Latency is set in samples, the specified sample count is retained across a sample-rate change. The selected count is the state observation, not a promised measured hardware delay. | external-audio-effect:B008 |
| REQ-EHW-EA-009 | **D12.** When Hardware Latency is set in milliseconds, the specified duration is retained across a sample-rate change. No sample conversion, rounding or compensation implementation is specified. | external-audio-effect:B008 |
| REQ-EHW-EA-010 | **D12.** Unchecking Delay Compensation in the Options menu disables Hardware Latency. Restored value, hidden-state updates and audible behavior on re-enabling are unknown. | external-audio-effect:B009 |
| REQ-EHW-EA-SIGNAL | **U.** Required quantitative audio/MIDI, gain, phase, metering, conversion and latency outcomes for External Audio Effect remain unknown. The documentary role descriptions and stored class presence provide no numerical oracle or internal mechanism. | Required unknown; no supplied outcome |
| REQ-EHW-EA-LIFECYCLE | **U.** Required boundary, automation, transport, persistence, undo, malformed, cancellation, disconnect, sample-rate failure, bypass, ownership, recovery and teardown outcomes for External Audio Effect remain unknown. Existing common-device, export and finite mix contracts do not establish these external-route interactions. | Required unknown; no supplied outcome |

### External Instrument

Surface `SURF-DEVICE-EXTERNAL-INSTRUMENT`; frozen discovery association `BufferInstrument` at schema line 963 is inferred presence only, not a behavioral/runtime alias.

| Requirement | Preconditions, documented result and limits | Evidence |
| --- | --- | --- |
| REQ-EHW-EI-001 | **D12.** External Instrument sends MIDI and returns audio for external synthesizers or multitimbral plug-ins. For a physical destination, the upper MIDI To chooser selects the MIDI port and the lower chooser supplies MIDI channel numbers. No channel domain or wire encoding is specified here. | external-instrument:B002, external-instrument:B003 |
| REQ-EHW-EI-002 | **D12.** When another Set track contains a qualifying multitimbral plug-in, the upper MIDI To chooser can select that track and the lower chooser selects a specific MIDI channel in that plug-in. Arbitrary plug-in support is not established. | external-instrument:B004 |
| REQ-EHW-EI-003 | **D12.** For a hardware synthesizer, Audio From selects interface inputs connected to the synthesizer outputs. Available choices depend on Audio Settings. This section does not independently establish a Configure… entry in this chooser. | external-instrument:B005 |
| REQ-EHW-EI-004 | **D12.** For a qualifying multitimbral plug-in on another track, Audio From lists the plug-in auxiliary outputs. Its main outputs are heard on the track that contains the instrument. This does not specify channel matrices, gain or summing. | external-instrument:B006 |
| REQ-EHW-EI-005 | **D12.** Gain adjusts the audio returning from the selected sound source. The section specifies no separate MIDI-send gain, amplitude law, legal range or clipping limiter. | external-instrument:B007 |
| REQ-EHW-EI-006 | **D12.** For external hardware, Hardware Latency permits manual compensation of delay Live cannot automatically detect, using milliseconds or samples. Sample fine tuning and switching back to milliseconds before changing rate is guidance; no conversion or rounding is specified. | external-instrument:B008 |
| REQ-EHW-EI-007 | **D12.** With a hardware route and Hardware Latency in samples, the specified sample count is retained when the sample rate changes. This does not establish physical alignment or event latency. | external-instrument:B008 |
| REQ-EHW-EI-008 | **D12.** With a hardware route and Hardware Latency in milliseconds, the specified duration is retained when the sample rate changes. No sample conversion or numerical rounding law is established. | external-instrument:B008 |
| REQ-EHW-EI-009 | **D12.** For internal routing, latency introduced by devices within Live is documented as automatically compensated, and External Instrument Hardware Latency is disabled. Its timing accuracy, limits and algorithm remain ungraded; this is not an internal mechanism requirement. | external-instrument:B008 |
| REQ-EHW-EI-010 | **D12.** Unchecking Delay Compensation in Options disables Hardware Latency. The internal-route restriction also applies; neither statement promises a physical route is always editable under every other condition. | external-instrument:B009 |
| REQ-EHW-EI-SIGNAL | **U.** Required quantitative audio/MIDI, gain, phase, metering, conversion and latency outcomes for External Instrument remain unknown. The documentary role descriptions and stored class presence provide no numerical oracle or internal mechanism. | Required unknown; no supplied outcome |
| REQ-EHW-EI-LIFECYCLE | **U.** Required boundary, automation, transport, persistence, undo, malformed, cancellation, disconnect, sample-rate failure, bypass, ownership, recovery and teardown outcomes for External Instrument remain unknown. Existing common-device, export and finite mix contracts do not establish these external-route interactions. | Required unknown; no supplied outcome |

## Timing, lifecycle and boundary obligations

Sample-mode retention preserves a count; millisecond-mode retention preserves
the selected duration after a successful rate change. Neither establishes
physical round-trip compensation, an exact converted count, drift/jitter or a
sample/event ordering law. External Instrument's disabled internal-route slider
is a control predicate; it cannot demonstrate the documented automatic
compensation goal numerically. Delay Compensation off disables the slider in
both devices, without establishing bypassed audio or restoration on re-enable.

For each device thirteen distinct lifecycle probes cover numeric boundaries,
automation/mapping, transport, persistence/missing sources, undo, malformed
state, cancellation, disconnect, rate failure/change, bypass, selection/focus
ownership, recovery and teardown. All are required unknowns, with no lifecycle
kind marked inapplicable. A missing physical device or qualifying plug-in keeps
its probe unexecuted. The effect's Configure… route is documented; it is not
silently assigned to the instrument. Hardware side effects and third-party
state restoration are not assumed to be controlled by Set Undo or reload.

## Acceptance catalog

The [requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/cases.json)
retain complete setup/action, source references and null unknowns. Documentary
comparators inspect only named controls, choices, disabled state and admitted
selected-unit retention. They do not grade gain, peak values, phase, MIDI, returned
audio or timing. Every exact-target expectation is null.

| Device | D12 / U requirements | Control / state cases | Signal / lifecycle U cases |
| --- | --- | --- | --- |
| External Audio Effect | 10 / 2 | 8 / 2 | 6 / 13 |
| External Instrument | 10 / 2 | 8 / 2 | 4 / 13 |

Total: **24 requirements (20 D12, four U); 56 unexecuted cases (20 documentary, 36 U)**.

| Case | Requirements | Kind | Finite action / proposed observation or required unknown |
| --- | --- | --- | --- |
| EHW-EA-001 | REQ-EHW-EA-001 | documented-control | Inspect Audio To and Audio From using an independently identified configured output/input pair; keep the two selector roles distinct. Audio To offers outgoing hardware outputs and Audio From offers returning hardware inputs; actual transmission and returned samples are ungraded. |
| EHW-EA-002 | REQ-EHW-EA-002 | documented-control | Open each chooser and choose Configure… separately with a valid audio configuration. Each chooser provides Configure… leading to Audio Settings; exact port inventory depends on the separately retained configuration. |
| EHW-EA-003 | REQ-EHW-EA-003 | documented-control | Locate both indicators and exercise each click target separately; use the distinct ungraded peak-signal probe for measurement/reset behavior. There is a click-reset peak indicator below each chooser; no peak number, reset value or refresh deadline is graded. |
| EHW-EA-004 | REQ-EHW-EA-004 | documented-control | Identify send and return Gain separately and enter two accepted nonzero interior values in one control at a time. Distinct send and return Gain controls can be addressed beside their respective choosers; no audible gain or isolation equality is graded. |
| EHW-EA-005 | REQ-EHW-EA-005 | documented-control | In separate valid audio-track and return-track placements inspect Dry/Wet, and request the documented 100% value on the return placement. Dry/Wet is available and admits the documented 100% setting when otherwise editable; mix samples and all other numeric ranges remain ungraded. |
| EHW-EA-006 | REQ-EHW-EA-006 | documented-control | Select an active external-return configuration and toggle Invert off/on; retain control state separately from the signal probe. Invert offers the stated on/off control; its processed-return audio effect has no supplied numerical oracle. |
| EHW-EA-007 | REQ-EHW-EA-007 | documented-control | With a configured hardware route and Delay Compensation on, select samples and milliseconds separately; enter 128 samples or 2.5 ms only if admitted. Both documented units can be selected on the editable latency control; no automatic measurement, exact round-trip alignment or cross-unit conversion is graded. |
| EHW-EA-008 | REQ-EHW-EA-008 | documented-state | With editable hardware latency, successfully set 128 samples at 48 kHz; leave samples selected and request 44.1 kHz then 48 kHz. If either entry or rate is unavailable, leave the case unexecuted. After each successfully accepted rate change, the selected-unit amount remains the admitted 128-sample count; equivalent formatting is allowed, while rounding and physical timing remain ungraded. |
| EHW-EA-009 | REQ-EHW-EA-009 | documented-state | With editable hardware latency, successfully set 2.5 ms at 48 kHz; leave milliseconds selected and request 44.1 kHz then 48 kHz. If either entry or rate is unavailable, leave the case unexecuted. After each successfully accepted rate change, the selected-unit amount remains the admitted 2.5 ms duration; equivalent formatting is allowed, while sample conversion and actual timing remain ungraded. |
| EHW-EA-010 | REQ-EHW-EA-010 | documented-control | On a valid configured hardware route, inspect Hardware Latency with Delay Compensation on, then uncheck Delay Compensation. Hardware Latency is disabled while Delay Compensation is unchecked; no additional bypass, timing or re-enable state claim is made. |
| EHW-EI-001 | REQ-EHW-EI-001 | documented-control | With a separately identified active physical MIDI destination, inspect both MIDI To choosers and select two available channels in separate reset trials. The upper chooser addresses the physical MIDI destination and the lower chooser lists channel numbers; emitted messages and synthesizer response are ungraded. |
| EHW-EI-002 | REQ-EHW-EI-002 | documented-control | Prepare an independently known qualifying multitimbral plug-in on another track; choose that track and inspect its offered MIDI channel choices. The qualifying plug-in track and its channel choice are selectable; plug-in callback, scheduling and sound are ungraded. |
| EHW-EI-003 | REQ-EHW-EI-003 | documented-control | With independently identified active synth-return inputs, inspect Audio From before and after a supported change to enabled audio inputs in Audio Settings. Audio From offers hardware returns according to the accepted audio configuration; exact inventory/order, hotplug and disappearance behavior are unknown. |
| EHW-EI-004 | REQ-EHW-EI-004 | documented-control | Use a qualifying plug-in with independently identified distinct main and auxiliary outputs; inspect Audio From and record which track hosts the instrument. The auxiliary-output choices are listed for that plug-in; host-track main-output ownership is documentary context with its audio probe ungraded, not an asserted waveform or absence predicate. |
| EHW-EI-005 | REQ-EHW-EI-005 | documented-control | On an active return configuration, identify Gain and enter two admitted nonzero interior values separately. The return Gain control is addressable; returned audio and any effect on external or plug-in state remain ungraded. |
| EHW-EI-006 | REQ-EHW-EI-006 | documented-control | With a configured hardware route and Delay Compensation on, select both units; request 128 samples or 2.5 ms only if admitted. Both documented units are selectable on an editable hardware-route latency control; measured latency and cross-unit numerical conversion are ungraded. |
| EHW-EI-007 | REQ-EHW-EI-007 | documented-state | Successfully set hardware latency to 128 samples at 48 kHz; keep samples selected and request 44.1 kHz then 48 kHz, leaving the case unexecuted if entry or rate is unavailable. The admitted selected-unit amount remains 128 samples after successful rate changes; exact formatting, conversion and measured timing are outside this state comparator. |
| EHW-EI-008 | REQ-EHW-EI-008 | documented-state | Successfully set hardware latency to 2.5 ms at 48 kHz; keep milliseconds selected and request 44.1 kHz then 48 kHz, leaving the case unexecuted if entry or rate is unavailable. The admitted selected-unit amount remains 2.5 ms after successful rate changes; exact formatting, sample conversion and measured timing are outside this state comparator. |
| EHW-EI-009 | REQ-EHW-EI-009 | documented-control | With Delay Compensation enabled, select a qualifying internal multitimbral plug-in route and inspect Hardware Latency. Test a separately reset physical route only as a context distinction. Hardware Latency is disabled for the internal route; automatic compensation is a documented signal goal with a separate null-oracle probe, not a measured timing result. |
| EHW-EI-010 | REQ-EHW-EI-010 | documented-control | Inspect a valid physical route and a qualifying internal plug-in route separately with Delay Compensation unchecked, then inspect the internal route with it checked. Hardware Latency is disabled whenever Delay Compensation is unchecked and remains disabled for the internal route; re-enabled hidden values and sound remain unknown. |
| EHW-EA-SIGNAL-ROUTE | REQ-EHW-EA-001, REQ-EHW-EA-SIGNAL | signal | Use independently known working physical send/return ports with a positive returned-audio baseline; send distinct owned bursts and select Audio To/From explicitly. Port/channel signal membership, buffering, conversion and exact returned samples remain unknown; no transparent hardware is assumed. |
| EHW-EA-SIGNAL-PEAK | REQ-EHW-EA-003, REQ-EHW-EA-SIGNAL | signal | With independent active send and return baselines, apply amplitude steps, click each peak indicator separately, then apply another nonzero burst. Peak convention, maximum window, send/return measurement points, reset value, smoothing and refresh timing are unknown. |
| EHW-EA-SIGNAL-GAIN | REQ-EHW-EA-004, REQ-EHW-EA-SIGNAL | signal | On a positive active physical loop, keep wet output audible and change only send Gain, reset, then only return Gain, between two admitted nonzero values. Separate path roles are documented, but numeric gain law, external processor response, clipping and exact unaffected-branch samples are unknown. |
| EHW-EA-SIGNAL-MIX | REQ-EHW-EA-005, REQ-EHW-EA-SIGNAL | signal | Keep dry input and independently known distinct hardware return both active and unmuted; select 100% and two admitted interior Dry/Wet values in separate reset trials. Mix law, dry/return alignment, dry contribution at exact endpoints and numerical output are unknown. |
| EHW-EA-SIGNAL-INVERT | REQ-EHW-EA-006, REQ-EHW-EA-SIGNAL | signal | With a known active nonzero return and distinct live dry source, use an admitted interior mix; compare Invert off/on, then repeat with an admitted full-wet setting. Processed-return targeting is documented; phase convention, numeric sign/channel action, dry-path equality and cancellation depth remain ungraded. |
| EHW-EA-SIGNAL-LATENCY | REQ-EHW-EA-007, REQ-EHW-EA-SIGNAL | signal | With separately identified physical timing/calibration prerequisites and a positive return baseline, vary an admitted nonzero Hardware Latency in samples and milliseconds; compare Delay Compensation on/off separately. Actual round-trip compensation, driver/gear latency, sample/ms conversion, rounding, drift, jitter and transitions are unknown; no successful alignment is asserted. |
| EHW-EA-U-BOUNDARY | REQ-EHW-EA-LIFECYCLE | boundary | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; test two admitted nonzero interior settings, then adjacent endpoint/zero/negative entries for exposed numeric controls in Audio To/From, both Gains, Dry/Wet, Invert and latency units; do not infer a legal range. Clamp/reject policy, endpoint restoration, zero semantics, unit switching, numeric precision and event-boundary ordering are unknown. |
| EHW-EA-U-AUTOMATION | REQ-EHW-EA-LIFECYCLE | automation | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; attempt supported automation or mapping of exposed controls in Audio To/From, both Gains, Dry/Wet, Invert and latency units; run manual and automated changes separately over a positive signal baseline. Eligibility, mapping ownership, smoothing, port-change scheduling and equivalence of manual/mapped/automated changes are unknown. |
| EHW-EA-U-TRANSPORT | REQ-EHW-EA-LIFECYCLE | transport | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; play the owned audio/note source, stop, seek, resume and separately seek during playback at 4/4 120 BPM. Held-note release, external/plug-in tails, port flushing, compensation restart and signal lifetime are unknown; no transport deadline is asserted. |
| EHW-EA-U-PERSISTENCE | REQ-EHW-EA-LIFECYCLE | persistence | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; save an owned Set/preset where supported, close/reopen with the same configuration, then in a disposable copy reopen with missing or renamed ports/source tracks. Saved routing/gain/unit identities, hardware reconnection matching, external/plug-in state ownership and missing-source handling are unknown. |
| EHW-EA-U-UNDO | REQ-EHW-EA-LIFECYCLE | undo | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; edit two controls in Audio To/From, both Gains, Dry/Wet, Invert and latency units, replace the device or preset, then use global Undo/Redo in separate reset trials. Undo grouping, restoration of route/unit/held-note state, engine reconfiguration and captured external/plug-in state are unknown. |
| EHW-EA-U-MALFORMED | REQ-EHW-EA-LIFECYCLE | malformed | On disposable owned copies only, attempt empty/truncated preset import and invalid numeric text including NaN, inf and 1e309 in exposed editable controls in Audio To/From, both Gains, Dry/Wet, Invert and latency units. Admission, parser/field validation, diagnostics, retained state and recovery are unknown; no private file encoding is assumed. |
| EHW-EA-U-CANCEL | REQ-EHW-EA-LIFECYCLE | cancel | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; open a routing chooser and dismiss before selection; separately begin a supported device/preset replacement and cancel where offered. For External Audio Effect also enter Audio Settings through Configure… and dismiss without committing edits. Cancellation availability, commit point, port reconfiguration, partial updates and preservation of previous signal/state are unknown. |
| EHW-EA-U-DISCONNECT | REQ-EHW-EA-LIFECYCLE | disconnect | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on with a positive baseline; in separately reset future trials disconnect the identified physical port/interface and remove or unload an internal source/plugin track where that route is applicable. Hotplug/source-loss detection, stale selectors, diagnostics, note release, reconnection identity and returned audio are unknown; no hardware connection or disconnection occurred here. |
| EHW-EA-U-SAMPLE-RATE | REQ-EHW-EA-LIFECYCLE | sample-rate | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; request 48 to 44.1 to 48 kHz while stopped and separately while active; test supported refusal/failure contexts separately and switch sample/ms units only in a distinct trial. Successful selected-unit retention has the bounded D12 cases; unsupported-rate response, conversion rounding, discontinuities, clock drift, queued notes, failure and recovery remain unknown. |
| EHW-EA-U-BYPASS | REQ-EHW-EA-LIFECYCLE | bypass | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; on a positive nonzero source/return path toggle device/chain activation, then restore it while the external or plug-in source remains active. Bypass routing, held notes, return/tail lifetime, residual hardware activity and reactivation are unknown; common device activation does not supply an external-route signal oracle. |
| EHW-EA-U-OWNERSHIP | REQ-EHW-EA-LIFECYCLE | ownership | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; change selected/focused track and Session/Arrangement view, then separately change which owned clip supplies active input, retaining explicit source routing. Focus/selection effects on monitoring/control ownership, active-clip changes and delivery to external/plugin destinations remain unknown beyond their linked finite owners. |
| EHW-EA-U-RECOVERY | REQ-EHW-EA-LIFECYCLE | recovery | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on; in a disposable supported configuration request a route whose audio-engine/port activation is refused or unavailable, then restore the previously functioning configuration. Diagnostics, refused activation, permission/driver failure, rollback, retry and preservation of prior state are unknown; no fault injection or driver changes occurred here. |
| EHW-EA-U-TEARDOWN | REQ-EHW-EA-LIFECYCLE | teardown | Initialize active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on with a positive signal baseline; remove device, undo removal, close the owned Set and separately close the application while source/held note is active. Port/resource release, outstanding MIDI, tails, compensation teardown, external hardware state and save/close prompts are unknown; no forced external reset or cleanup deadline is asserted. |
| EHW-EI-SIGNAL-MIDI-ROUTE | REQ-EHW-EI-001, REQ-EHW-EI-SIGNAL | signal | Use an independently known working external synth/MIDI port and admitted channels, a valid owned note clip and positive audible return; select each physical destination/channel in separate reset trials. Emitted MIDI bytes, delivery/ordering, channel isolation, external note response and resulting audio remain unknown. |
| EHW-EI-SIGNAL-PLUGIN-OUTPUTS | REQ-EHW-EI-004, REQ-EHW-EI-SIGNAL | signal | Use a separately known qualifying multitimbral plug-in with distinguishable main/auxiliary signals; keep the instrument-host track and External Instrument track monitored and unmuted, explicitly select an auxiliary return and MIDI channel. The documented main-on-host and auxiliary-return roles have no supplied numerical routing/mix oracle, plug-in callback contract, duplicate suppression or channel matrix. |
| EHW-EI-SIGNAL-GAIN | REQ-EHW-EI-005, REQ-EHW-EI-SIGNAL | signal | For separately reset positive hardware and qualifying internal-plugin returns, vary only External Instrument Gain between admitted nonzero values while the owned note input and return remain active. Return gain law, clipping, external/plug-in response and numerical output are unknown; no MIDI-send gain or limiter is inferred. |
| EHW-EI-SIGNAL-LATENCY | REQ-EHW-EI-009, REQ-EHW-EI-SIGNAL | signal | With Delay Compensation on, compare a positive qualifying internal-plugin return and a separately calibrated physical route with admitted nonzero Hardware Latency; request samples/ms only on the physical route. Internal automatic compensation and external manual compensation are documented goals; measured accuracy, conversion, latency limits and scheduling are unknown. A disabled internal slider is not proof of compensated audio. |
| EHW-EI-U-BOUNDARY | REQ-EHW-EI-LIFECYCLE | boundary | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; test two admitted nonzero interior settings, then adjacent endpoint/zero/negative entries for exposed numeric controls in MIDI port/track/channel, Audio From, Gain, latency units and Delay Compensation; do not infer a legal range. Clamp/reject policy, endpoint restoration, zero semantics, unit switching, numeric precision and event-boundary ordering are unknown. |
| EHW-EI-U-AUTOMATION | REQ-EHW-EI-LIFECYCLE | automation | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; attempt supported automation or mapping of exposed controls in MIDI port/track/channel, Audio From, Gain, latency units and Delay Compensation; run manual and automated changes separately over a positive signal baseline. Eligibility, mapping ownership, smoothing, port-change scheduling and equivalence of manual/mapped/automated changes are unknown. |
| EHW-EI-U-TRANSPORT | REQ-EHW-EI-LIFECYCLE | transport | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; play the owned audio/note source, stop, seek, resume and separately seek during playback at 4/4 120 BPM. Held-note release, external/plug-in tails, port flushing, compensation restart and signal lifetime are unknown; no transport deadline is asserted. |
| EHW-EI-U-PERSISTENCE | REQ-EHW-EI-LIFECYCLE | persistence | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; save an owned Set/preset where supported, close/reopen with the same configuration, then in a disposable copy reopen with missing or renamed ports/source tracks. Saved routing/gain/unit identities, hardware reconnection matching, external/plug-in state ownership and missing-source handling are unknown. |
| EHW-EI-U-UNDO | REQ-EHW-EI-LIFECYCLE | undo | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; edit two controls in MIDI port/track/channel, Audio From, Gain, latency units and Delay Compensation, replace the device or preset, then use global Undo/Redo in separate reset trials. Undo grouping, restoration of route/unit/held-note state, engine reconfiguration and captured external/plug-in state are unknown. |
| EHW-EI-U-MALFORMED | REQ-EHW-EI-LIFECYCLE | malformed | On disposable owned copies only, attempt empty/truncated preset import and invalid numeric text including NaN, inf and 1e309 in exposed editable controls in MIDI port/track/channel, Audio From, Gain, latency units and Delay Compensation. Admission, parser/field validation, diagnostics, retained state and recovery are unknown; no private file encoding is assumed. |
| EHW-EI-U-CANCEL | REQ-EHW-EI-LIFECYCLE | cancel | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; open a routing chooser and dismiss before selection; separately begin a supported device/preset replacement and cancel where offered. For External Audio Effect also enter Audio Settings through Configure… and dismiss without committing edits. Cancellation availability, commit point, port reconfiguration, partial updates and preservation of previous signal/state are unknown. |
| EHW-EI-U-DISCONNECT | REQ-EHW-EI-LIFECYCLE | disconnect | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route with a positive baseline; in separately reset future trials disconnect the identified physical port/interface and remove or unload an internal source/plugin track where that route is applicable. Hotplug/source-loss detection, stale selectors, diagnostics, note release, reconnection identity and returned audio are unknown; no hardware connection or disconnection occurred here. |
| EHW-EI-U-SAMPLE-RATE | REQ-EHW-EI-LIFECYCLE | sample-rate | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; request 48 to 44.1 to 48 kHz while stopped and separately while active; test supported refusal/failure contexts separately and switch sample/ms units only in a distinct trial. Successful selected-unit retention has the bounded D12 cases; unsupported-rate response, conversion rounding, discontinuities, clock drift, queued notes, failure and recovery remain unknown. |
| EHW-EI-U-BYPASS | REQ-EHW-EI-LIFECYCLE | bypass | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; on a positive nonzero source/return path toggle device/chain activation, then restore it while the external or plug-in source remains active. Bypass routing, held notes, return/tail lifetime, residual hardware activity and reactivation are unknown; common device activation does not supply an external-route signal oracle. |
| EHW-EI-U-OWNERSHIP | REQ-EHW-EI-LIFECYCLE | ownership | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; change selected/focused track and Session/Arrangement view, then separately change which owned clip supplies active input, retaining explicit source routing. Focus/selection effects on monitoring/control ownership, active-clip changes and delivery to external/plugin destinations remain unknown beyond their linked finite owners. |
| EHW-EI-U-RECOVERY | REQ-EHW-EI-LIFECYCLE | recovery | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route; in a disposable supported configuration request a route whose audio-engine/port activation is refused or unavailable, then restore the previously functioning configuration. Diagnostics, refused activation, permission/driver failure, rollback, retry and preservation of prior state are unknown; no fault injection or driver changes occurred here. |
| EHW-EI-U-TEARDOWN | REQ-EHW-EI-LIFECYCLE | teardown | Initialize separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route with a positive signal baseline; remove device, undo removal, close the owned Set and separately close the application while source/held note is active. Port/resource release, outstanding MIDI, tails, compensation teardown, external hardware state and save/close prompts are unknown; no forced external reset or cleanup deadline is asserted. |

## Unknowns and evidence appendix

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns exact-build/whole-product coverage gaps. Required unknowns include port
domains and naming/grouping, configuration failure and restoration, hardware or
plug-in availability, MIDI delivery/codec/channel domain, main/auxiliary signal
composition, gain/mix/phase/peak laws, limits and rounding, compensation accuracy,
automation, undo, persistence, cancellation, hotplug, driver failures and teardown.
No source specifies an external-device protocol, private DSP mechanism or full
saved-state API. No figure, FAQ or linked routing chapter was independently
inspected for this packet.

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/sources.json)
pins seven reused external sources, including original capture catalogs and the
frozen inventory/schema. D12-AUDIO-EFFECTS is the original audio-utilities source
identity: [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html),
SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`,
[official chapter](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
§29.18, heading HTML line 1144, paragraphs line 1154.
SAMPLE-INSTRUMENTS-MANUAL is the original sample-instruments identity:
[HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-instruments-2026-10-19.html),
SHA-256 `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`,
[official chapter](https://www.ableton.com/en/live-manual/12/live-instrument-reference/),
§31.6, heading HTML line 1016, paragraphs line 1026. Both were captured
2026-10-19 and identify Version 12, not exact patch behavior.

The two [manual block views](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-audio-effect-blocks.json)
and [instrument blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-instrument-blocks.json)
retain 18 paragraphs plus two headings. The
[schema view](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/schema-fields.json)
and [discovery associations](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/inventory-associations.json)
are Dpkg presence only. The latest schema hash is
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Both profiles have no matched preset example in the frozen inventory; fields
and inferred class associations prove no port serialization or runtime behavior.

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manifest-author-r2.json)
freezes payloads and both canonical snapshots. The
[validator](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validate-r2.py)
and [result](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validation-author-r2.json)
check packet integrity only. These analysis-only links require review and
sanitization before any handoff. No source bytes were rewritten and no original,
candidate, external device or plug-in was executed. Independent semantic review
is a separate gate; no release, installation or publication occurs here.

## Revision 2 formatting correction

EHW-REVIEW-001 is addressed by keeping each requirement table’s first cell a
bare requirement ID and placing its D12/U grade beside the contract text.
The 24 requirement statements, 56 cases, source identities and null target
outcomes are unchanged. The exact [revision 1 seal and 15 payloads](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/archive-r1/manifest-author-r1.json)
are preserved; [response](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/response-author-r2.json)
records the narrow correction. Browser discovery is an integrity check, not a
behavioral or compatibility result.
