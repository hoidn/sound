---
id: SPEC-DEVICE-UTILITY
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Utility device

This is the canonical partial contract for `SURF-DEVICE-UTILITY` under
FEAT-DEVICES / FEAT-AUDIO in the [feature map](feature-map.md), following
[ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md).
Inputs, controls, observable outputs and state are specified below; numerical
algorithms and unsupported lifecycle outcomes remain explicit gaps.

**D12 exact-target U:** D12 means the captured current official Version 12 manual,
not an observation of Live 12.4.3. Every D12 clause's exact-build applicability
is U. Dpkg means direct observation of retained files shipped in the target
package; it grades only stored bytes/values. No S or X audio/display claim is
made. U has no oracle and must never pass. All application cases are unexecuted.
This page is an analyst draft, not a released implementation input or complete
device specification. [Research and source limits](../research/device-audio-utilities.md)
own evidence synthesis; this page owns behavior.

The [device-chain/rack contract](device-racks.md) owns generic insertion,
reordering, activation, preset actions and deletion. [Set structure](live-set-structure.md)
and [ALS container](als-container.md) own their stated container/structure scopes;
their T1 device subset does not prove Utility save/reopen. [Automation](automation-envelopes.md)
owns its envelope representation/evaluation clauses, not untraced device scheduling.
[Mix graph](mix-graph.md) owns track routing/mixing. [Mixer values](mixer-values.md)
describes track faders; it does not supply this device's gain, pan or smoothing law.
The current-manual source does not settle platform differences, keyboard access,
permissions, recovery, latency or transport coupling beyond explicit clauses.

## Requirements

### REQ-DEVICE-UTILITY-001 — audio input and output

**D12.** Input is the stereo audio arriving at this device-chain position; output is the signal processed by the selected Utility controls. Device insertion, ordering, deletion and generic activation belong to SPEC-DEVICE-RACKS. The manual does not establish a complete processing order among Utility controls.

Evidence: `utility:B02–B14`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-002 — independent phase controls

**D12.** Provide separate Left and Right Phase controls that invert the corresponding input-channel phase. The composition order with channel selection, Mono, Width, Bass Mono, gain and balance is U. This clause does not specify coefficient precision, latency or ramping.

Evidence: `utility:B03`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-003 — channel selection

**D12.** Channel Mode can select the Left source: ignore the right source and present the left source on both outputs. The documented disablement rule also names Right mode. Right-mode sample routing, the full mode list and numeric enum-to-label mapping require separate evidence; preset filenames do not prove those laws.

Evidence: `utility:B04, B07`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-004 — Width

**D12.** Width 0% gives mono; values greater than 100% widen the stereo panorama. If Channel Mode is Left or Right, Width is disabled and has no function. Complete domain, width matrix, normalization, 100% identity and behavior for already mono input are U.

Evidence: `utility:B05, B07`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-005 — Mid/Side view and endpoints

**D12.** The Width context menu switches between Width and Mid/Side controls. At 100M audio is summed to mono; from 0 toward 100S the stereo/out-of-phase components are emphasized. At 100S only the side signal is heard and the output channels are 180 degrees out of phase. Left/Right Channel Mode disables this control. Parameter remapping, endpoint gain and remembered hidden values are U.

Evidence: `utility:B06–B07`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-006 — Mono

**D12.** Enabling Mono converts stereo input to mono. Summing coefficients and interactions with Channel Mode, Width/Mid-Side, Bass Mono, phase and Balance are U.

Evidence: `utility:B08`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-007 — Bass Mono cutoff

**D12.** Enabling Bass Mono converts low frequencies to mono. Bass Mono Frequency adjusts a cutoff over 50–500 Hz. Filter type, order, slope, crossover phase, normalization and exact response around cutoff are U.

Evidence: `utility:B09`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-008 — Bass Mono Audition

**D12.** Enabling Bass Mono Audition makes only the low frequencies audible. Dependence on the Bass Mono switch, cutoff transition and bypass/off behavior are U.

Evidence: `utility:B10`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-009 — Gain domain

**D12.** Gain adjusts the input level over minus infinity dB through +35 dB. No linear-to-dB formula, numerical floor, float precision, automation interpolation, clipping or smoothing is claimed. Track fader laws from SPEC-MIXER-VALUES have not been traced to this device and do not apply by name alone.

Evidence: `utility:B11`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-010 — Gain arrow editing

**D12.** Up/down arrow editing changes Gain in 1 dB steps between −18 and +35 dB; between −18 and minus infinity the adjustment smoothly accelerates. Repetition cadence, exact lower-region sequence, endpoint key handling and text-entry parsing are U.

Evidence: `utility:B11`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-011 — Balance

**D12.** Balance pans the signal within the stereo field. Pan law, center gain, normalized storage range, extreme-channel attenuation, mono behavior and coupling with other controls are U.

Evidence: `utility:B12`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-012 — Mute at chain position

**D12.** Mute silences the incoming signal at Utility’s device-chain position. Utility can precede a delay or reverb and mute its input without switching off that downstream device’s output. Tail waveform/duration is owned by the downstream effect and is not specified here.

Evidence: `utility:B13`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-013 — DC filtering

**D12.** DC filters out DC offsets and extremely low frequencies below the audible range. Cutoff, filter response, startup/transient behavior, numerical precision and interaction order are U. The manual’s audibility discussion does not establish sample-exact output.

Evidence: `utility:B14`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-014 — retained preset state vocabulary

**Dpkg.** The retained StereoGain schema and ten shipped presets establish named stored fields and exact saved values, summarized in the research packet. They do not establish constructor defaults, accepted malformed ranges, load/save normalization or live UI state. LegacyGain and LegacyMode are retained historical fields; their migration semantics are U.

Evidence: `PKG-SCHEMA:StereoGain; package-values.json device=Utility`; [source locators](#analysis-only-evidence).

### REQ-DEVICE-UTILITY-015 — lifecycle and numerical gaps

**U.** Exact 12.4.3 applicability of every D12 clause is U. Save/reopen, preset replace/hot-swap, undo/redo, aborted edits, invalid numeric text, malformed files, automation scheduling, sample-rate/block-size changes, suspension, audio-device failure, deletion and teardown require outcome evidence. This draft provides finite ungraded probes, not invented success behavior.

Evidence: `No outcome evidence`; [source locators](#analysis-only-evidence).

## Acceptance cases

These finite scenarios have retained parameters in the
[case packet](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/utility-cases.json) and [signal definitions](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/fixture-signals.json).
A D12 case compares only its stated documented relation or UI state; it supplies
no sample/pixel/cents/time tolerance and cannot grade exact-target compatibility.
Dpkg cases compare exact retained XML values only. Cases marked U have no
expected outcome. Named neutral settings mean other switches off, normal stereo
channel mode, Gain displayed 0 dB, Balance centered and Width displayed 100%,
where those controls exist; this setup is a proposed probe configuration, not a
factory default or proven transparent processing chain. No UI image was inspected.

| Case | Requirements | Kind; setup and action | Expected / criterion | Evidence |
| --- | --- | --- | --- | --- |
| DUT-001 | 002 | positive: SIG-STEREO; all unrelated controls neutral. Enable Left Phase only | Left input-channel phase is inverted; separate Right control exists. Combined-control processing order and numerical output remain U. | D12: `utility:B03` |
| DUT-002 | 002 | positive: SIG-STEREO. Enable Right Phase only | Right input-channel phase is inverted independently. | D12: `utility:B03` |
| DUT-003 | 001, 003 | positive: SIG-STEREO with distinct frequencies. Choose Left Channel Mode | Right source is ignored; both outputs carry the left source. Gain normalization and exact samples U. | D12: `utility:B04` |
| DUT-004 | 004, 005 | negative: Channel Mode Left. Attempt to edit Width and Mid/Side | Both controls are disabled and have no function. | D12: `utility:B07` |
| DUT-005 | 004, 005 | negative: Channel Mode Right. Attempt to edit Width and Mid/Side | Both controls are disabled and have no function. | D12: `utility:B07` |
| DUT-006 | 004 | boundary: SIG-STEREO; channel mode supports Width. Set Width 0% | Output is mono; summing gain and tolerance U. | D12: `utility:B05` |
| DUT-007 | 004 | positive: SIG-STEREO; Width available. Compare Width 100% and 150% | 150% is described as a widened panorama; exact stereo metric, level and 100% identity U. | D12: `utility:B05` |
| DUT-008 | 005 | positive: Width visible. Choose Mid/Side Mode from Width context menu | The visible control changes between Width and Mid/Side; hidden-value retention U. | D12: `utility:B06` |
| DUT-009 | 005 | boundary: SIG-STEREO; Mid/Side available. Set 100M | Audio sums to mono; endpoint gain U. | D12: `utility:B06` |
| DUT-010 | 005 | boundary: SIG-STEREO; Mid/Side available. Set 100S | Only side signal is heard; output L/R are 180 degrees out of phase; normalization and tolerance U. | D12: `utility:B06` |
| DUT-011 | 006 | positive: SIG-STEREO. Enable Mono | Stereo input becomes mono. | D12: `utility:B08` |
| DUT-012 | 007 | positive: SIG-BASS-SIDE. Enable Bass Mono at 120 Hz | Low frequencies become mono. Exact crossover response and residual tolerance U. | D12: `utility:B09` |
| DUT-013 | 007 | boundary: Bass Mono available. Set cutoff 50 Hz then 500 Hz | Both documented cutoff endpoints are in the control domain. Response at endpoints U. | D12: `utility:B09` |
| DUT-014 | 008 | positive: SIG-BASS-SIDE; Bass Mono enabled at 120 Hz. Enable Bass Mono Audition | Only low-frequency content is heard; rejection amount and cutoff shape U. | D12: `utility:B10` |
| DUT-015 | 009 | boundary: SIG-440. Set Gain to minus infinity and +35 dB using the control | Both documented endpoint settings exist. Numerical silence floor, output amplitude, clipping and transitions U. | D12: `utility:B11` |
| DUT-016 | 010 | positive: Gain −18 dB. Press Up once | Gain becomes −17 dB. | D12: `utility:B11` |
| DUT-017 | 010 | positive: Gain +35 dB. Press Down once | Gain becomes +34 dB. | D12: `utility:B11` |
| DUT-018 | 010 | boundary: Gain −17 dB. Press Down once | Gain becomes −18 dB; lower-region sequence is ungraded. | D12: `utility:B11` |
| DUT-019 | 011 | positive: SIG-STEREO. Move Balance left then right | Signal pans in the stereo field; exact channel gains U. | D12: `utility:B12` |
| DUT-020 | 012 | positive: SIG-STEREO; Utility directly before capture point. Enable Mute | Incoming signal is silenced at this position; transient/timing tolerance U. | D12: `utility:B13` |
| DUT-021 | 012 | positive: Utility before active downstream reverb with an existing tail. Enable Utility Mute | Utility cuts the input without disabling the downstream output; no exact tail is graded. | D12: `utility:B13` |
| DUT-022 | 013 | positive: SIG-DC plus SIG-440. Enable DC | DC offset is filtered; exact attenuation, settling time and audible-tone preservation tolerance U. | D12: `utility:B14` |
| DUT-023 | 014 | file observation: Retained package/Utility/Bass Mono.adv. Decode gzip/XML without application execution | StereoGain has BassMono/Manual=true, BassMonoFrequency/Manual=120, Gain/Manual=1 and LegacyMode=false. | Dpkg: `package/Utility/Bass Mono.adv:.//StereoGain` |
| DUT-024 | 014 | file observation: Retained package/Utility/Phase Invert.adv. Decode gzip/XML | PhaseInvertL/Manual=true and PhaseInvertR/Manual=true; no output assertion. | Dpkg: `package/Utility/Phase Invert.adv:.//StereoGain` |
| DUT-025 | 014 | file observation: Retained Left.adv and Right.adv. Read ChannelMode/Manual | Left.adv stores 0; Right.adv stores 2. Enum labels/engine mapping remain ungraded. | Dpkg: `package/Utility/{Left,Right}.adv:.//StereoGain/ChannelMode/Manual` |
| DUT-026 | 015 | negative: Gain −18 dB. Press Down repeatedly and record values | Unknown; no oracle, do not grade. | U: `U` |
| DUT-027 | 015 | boundary: Gain +35 dB. Press Up; enter a value above +35 dB | Unknown; no oracle, do not grade. | U: `U` |
| DUT-028 | 015 | malformed: Utility Gain text field. Enter NaN, infinity and nonnumeric text; then Enter | Unknown; no oracle, do not grade. | U: `U` |
| DUT-029 | 015 | error: Copy of saved Utility preset. Remove Gain; duplicate ChannelMode; set invalid ChannelMode enum and BassMonoFrequency negative | Unknown; no oracle, do not grade. | U: `U` |
| DUT-030 | 015 | cancel: Gain text editing in progress. Type replacement value then Escape | Unknown; no oracle, do not grade. | U: `U` |
| DUT-031 | 015 | undo: Mono off and Gain 0 dB. Toggle Mono; change Gain; Undo twice; Redo twice | Unknown; no oracle, do not grade. | U: `U` |
| DUT-032 | 015 | persistence: Nondefault phase/channel/width/mono/bass/gain/balance/DC settings. Save Set; reopen; compare every setting and output; repeat with preset save/replace | Unknown; no oracle, do not grade. | U: `U` |
| DUT-033 | 015 | automation: Gain/Mute/Bass Mono automation while audio streams. Cross automation breakpoints and manually override then re-enable | Unknown; no oracle, do not grade. | U: `U` |
| DUT-034 | 015 | teardown: Audio streams through Utility. Delete Utility; Undo deletion; disable/re-enable audio engine | Unknown; no oracle, do not grade. | U: `U` |
| DUT-035 | 015 | timing: SIG-STEREO. Change sample rate and processing block size; toggle phase and Mute at named sample offsets | Unknown; no oracle, do not grade. | U: `U` |
| DUT-036 | 015 | coupling: SIG-STEREO. Combine PhaseInvertR, Left mode, Mono, Bass Mono, Width, Balance and DC; compare isolated stages | Unknown; no oracle, do not grade. | U: `U` |
| DUT-037 | 015 | legacy: Historical Utility preset with LegacyMode true. Open then save in target; compare migration and audible result | Unknown; no oracle, do not grade. | U: `U` |

Counts: 15 requirements; 37 scenarios: 22 D12
(documentary relationships, exact-target U), 3 Dpkg (stored-file
observations only), 12 U (ungraded). Zero target application executions,
zero target audio/display acceptance passes. Supported and unknown clauses may
coexist in a requirement; the labels do not promote its unknown parts.

Positive, negative, boundary, malformed/error, cancel, undo, persistence, timing
and teardown cases are explicit. File/device errors are distinct from valid audio
input outside an analyzer's intended signal class. No asynchronous cancelable
operation is documented for these controls; Escape/edit/menu cases remain U,
rather than inventing a new cancel workflow. State ownership on view change,
transport restart, preset replacement, Set close and engine suspension remains
unknown except the documentary clauses named above. Unknowns keep full-device
coverage open and are not exclusions from the whole-product target.

## Analysis-only evidence

Source `D12-AUDIO-EFFECTS`: [official current manual](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/#utility),
captured 2026-10-19 as [retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html).
[Block locators](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-utility-blocks.json) retain h2/h3 anchors, paragraph
kind, exact HTML line and text; [readable extract](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-utility.txt).
`utility:Bnn` points to that numbered block; ranges are inclusive.
The source says Version 12, without a 12.4.3 publication pin.

`PKG-SCHEMA` is the [retained latest shipped schema](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/12.0_12402.txt);
[filtered fields](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/schema-fields.json) retain class start lines.
[Package values](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/package-values.json) retain XML locators, historical
Creator/revision, and exact values. [Source identity manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/sources.json)
pins URL/path, capture date, byte size and SHA-256 for the HTML, schema and each
shipped file. [Frozen author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manifest-author-r1.json) pins this
specification revision and packet for separate review. These are source/file
observations, not runtime validation, a read/write guarantee or host topology.

## Revision history

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | First bounded F-06 Utility contract; documentary/file-only evidence and finite ungraded lifecycle/numerical probes |
