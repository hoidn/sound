---
id: SPEC-MAX-FOR-LIVE-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary revision parity unknown
---

# Twenty shipped Max for Live device profiles

## Scope and authority

This partial F-06 draft separately owns the twenty `max-device` inventory
profiles. It does not complete those devices or arbitrary Max compatibility.
[Coverage design](../research/full-live-specification-design.md) and
[research](../research/max-for-live-devices.md) govern source interpretation.
**D12** is current English Version 12 chapter prose; **D12-2025** is the dated
2025-06-02 English Version 12 PDF, used only for DS Sampler, Expression Control
Legacy and its migration context. **Every runtime clause's exact 12.4.3
applicability is U.** Documentary revision differences are retained, not merged.
**Dpkg** proves unparsed supplied-file identity only. No original patch/code,
Max/Live/candidate or emulator was executed; no installed file was modified.
Figures were not inspected separately. This is not a released implementation input.

[Max host/templates](max-for-live-hosting.md) owns editing/save/dependencies and
five templates; [MIDI editing/tools](midi-editing-tools.md) owns Euclidean and
VelocityShaper algorithms. [Device racks](device-racks.md), [automation](automation-envelopes.md),
[mapping](midi-user-mapping.md), [MPE](mpe-workflows.md), [tuning](tuning-systems.md)
and [mix graph](mix-graph.md) retain their bounded contracts. Links do not supply
these devices' parameter/curve/MIDI codecs, signals, lifecycle or Max API protocol.
Standalone Shaper is distinct from Shaper MIDI and from VelocityShaper tool;
Envelope Follower differs from Envelope MIDI; Expression Control Legacy receives
no current Expression Control controls or modern-to-Legacy parity assumption.

## Inputs, oracles and case limits

Use [finite future inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/fixtures.json), actual accepted modes,
valid owned samples/notes/source paths and independently eligible mapping targets.
For all no-effect, zero-depth, muted-source and inactive-control probes, retain an
active nonzero paired positive baseline with audible output or visible mapped
response. Silent/unloaded/unsupported inputs or failed positive controls leave U.
Random claims never demand sample equality or a change on every realization.

Documentary control/state comparators inspect only named units, choices, eligibility
and explicit relations. All exact-target `expected`/`comparison` values are null,
`target_grade:U`, `executed:false`; all timing/signal obligations have no documentary
comparator. Input tone definitions are stimuli, not recovered synthesis formulas.
No hidden graph, FM/filter/envelope/curve/RNG algorithm, voice budget, transport/MIDI
encoding, latency, block/rate conversion, normalization or tolerance is invented.
Host defaults are not proven by package presence or documentary default wording.

## Individual device requirements

Each bare requirement-ID row is normative for its stated documentary/file/U
scope and appears in the existing requirements browser. D12/D12-2025 rows have
same-number finite cases; FILE is a data-identity check; LIFECYCLE has ten
explicit required-U cases with concrete per-device setup. Exact source blocks
retain HTML lines/context or PDF physical page plus derived-text line ranges.

## Align Delay

Surface `SURF-MAX-ALIGN-DELAY`. Lifecycle setup: Distinct stereo input, nonzero different L/R delays, Distance Mode, temperature explicit, Link off.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-ALIGN-DELAY-001 | Delay Mode choices Time, Samples and Distance use ms, samples and meters/feet. No time-distance-speed or sample-rounding law is supplied. | D12;target U; `MXD:B060`, `MXD:B061`, `MXD:B062`, `MXD:B063`, `MXD:B064` |
| REQ-MXD-ALIGN-DELAY-002 | Distance supports Temperature with Celsius/Fahrenheit choice and temperature slider. | D12;target U; `MXD:B065` |
| REQ-MXD-ALIGN-DELAY-003 | Link L/R applies left settings to right; right slider is grayed and left edits both. | D12;target U; `MXD:B066` |
| REQ-MXD-ALIGN-DELAY-FILE | Retained inventory/file identity only: 73321 bytes, SHA-256 e8ef40c20a896884ad41ba315e612624d78ee64f2febcd4936bbf5e294f74d6d. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-ALIGN-DELAY-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Envelope Follower

Surface `SURF-MAX-ENVELOPE-FOLLOWER`. Lifecycle setup: Stepped main A anddistinct donor B, Sidechain on Mix 50%, nonzero Gain/Rise/Fall/Delay, active mapped target/nonzeroamount.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-ENVELOPE-FOLLOWER-001 | Map then parameter click assigns target; Multimap exposes up to eight mappings and Unmap removes selected assignment. | D12;target U; `MXD:B069`, `MXD:B070`, `MXD:B071` |
| REQ-MXD-ENVELOPE-FOLLOWER-002 | Modulation permits manual base-value edits with Bipolar centered/Unipolar one-direction depth; Remote Control owns mapped value and prevents manual edit, with Min/Max range. Documentary default Modulation is not a target constructor proof. | D12;target U; `MXD:B072`, `MXD:B073`, `MXD:B074` |
| REQ-MXD-ENVELOPE-FOLLOWER-003 | Input amplitude produces mapped envelope; Gain controls input level and Rise/Fall smooth attack/release. | D12;target U; `MXD:B068`, `MXD:B075` |
| REQ-MXD-ENVELOPE-FOLLOWER-004 | Envelope Delay supports time and synchronized beat divisions. | D12;target U; `MXD:B076` |
| REQ-MXD-ENVELOPE-FOLLOWER-005 | Expanded Audio Routing and Sidechain select external track plus Pre FX/Post FX/Post Mixer and Rack channel; Direct/S.C. meters show respective inputs. | D12;target U; `MXD:B077`, `MXD:B078`, `MXD:B079`, `MXD:B080` |
| REQ-MXD-ENVELOPE-FOLLOWER-006 | Sidechain Mix 0% uses track input only; 100% external donor only for envelope generation. | D12;target U; `MXD:B081` |
| REQ-MXD-ENVELOPE-FOLLOWER-FILE | Retained inventory/file identity only: 524887 bytes, SHA-256 2c3328d8e0eae110fdc441041ca50604d247fb97b61d62dfb741a631a5cbc380. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-ENVELOPE-FOLLOWER-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## LFO

Surface `SURF-MAX-LFO`. Lifecycle setup: Sine, Rate 1 Hz ifaccepted, Depth nonzero, Phase 25%, nonzeroJitter/Smooth, active eligible mapped target.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-LFO-001 | Map then parameter click assigns target; Multimap exposes up to eight mappings and Unmap removes selected assignment. | D12;target U; `MXD:B084`, `MXD:B085`, `MXD:B086` |
| REQ-MXD-LFO-002 | Modulation permits manual base-value edits with Bipolar centered/Unipolar one-direction depth; Remote Control owns mapped value and prevents manual edit, with Min/Max range. Documentary default Modulation is not a target constructor proof. | D12;target U; `MXD:B087`, `MXD:B088`, `MXD:B089` |
| REQ-MXD-LFO-003 | Nine waves: Sine, Up, Down, Triangle, Square, Random, Bin, Stray, Glider. Shape unavailable for Random/Bin/Stray/Glider; Steps unavailable for Random/Bin/Square; Steps up to 24. | D12;target U; `MXD:B090`, `MXD:B091` |
| REQ-MXD-LFO-004 | Jitter randomizes output; Smooth softens output changes including jitter. | D12;target U; `MXD:B092` |
| REQ-MXD-LFO-005 | Rate uses Hz or beat divisions; Hz permits ×10. Depth 0% applies no modulation,100% maximum. | D12;target U; `MXD:B093`, `MXD:B094` |
| REQ-MXD-LFO-006 | Offset centers at 0 and shifts output upward/downward; Phase spans 0-100% cycle. | D12;target U; `MXD:B095`, `MXD:B096` |
| REQ-MXD-LFO-007 | Hold freezes current LFO output; release restarts from held value. R retriggers at Phase position. | D12;target U; `MXD:B097`, `MXD:B098` |
| REQ-MXD-LFO-FILE | Retained inventory/file identity only: 542384 bytes, SHA-256 7b8489f2821a7d3c5004cf486e51cc3968b4b302e027d426a311aa0accac4c47. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-LFO-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Shaper

Surface `SURF-MAX-SHAPER`. Lifecycle setup: Threepointnonflat shape, nonzero Depth, mapped target, Loop andnonzero Rate, Phase 25%, Jitter/Smooth nonzero.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-SHAPER-001 | Map then parameter click assigns target; Multimap exposes up to eight mappings and Unmap removes selected assignment. | D12;target U; `MXD:B101`, `MXD:B102`, `MXD:B103` |
| REQ-MXD-SHAPER-002 | Modulation permits manual base-value edits with Bipolar centered/Unipolar one-direction depth; Remote Control owns mapped value and prevents manual edit, with Min/Max range. Documentary default Modulation is not a target constructor proof. | D12;target U; `MXD:B104`, `MXD:B105`, `MXD:B106` |
| REQ-MXD-SHAPER-003 | Breakpoint envelope generates mapping data. Click creates, Alt Win/Option Mac segment drag curves, Shift-click deletes; Clear removes envelope; six presets replace it. | D12;target U; `MXD:B100`, `MXD:B107`, `MXD:B108` |
| REQ-MXD-SHAPER-004 | Grid controls divisions and Snap moves created/repositioned points to nearest line; small display shows output. | D12;target U; `MXD:B109`, `MXD:B110` |
| REQ-MXD-SHAPER-005 | Jitter randomizes, Smooth softens output, Offset shifts center relative to0. | D12;target U; `MXD:B111`, `MXD:B113` |
| REQ-MXD-SHAPER-006 | Phase spans 0-100%; R retriggers at Phase and is disabled in Sync time mode. | D12;target U; `MXD:B112` |
| REQ-MXD-SHAPER-007 | Trigger modes Loop continuously at Rate,1-Shot via mappable T, Manual scrub control; Rate Hz/sync. Depth 0 none,100 maximum. | D12;target U; `MXD:B114`, `MXD:B115`, `MXD:B116`, `MXD:B117`, `MXD:B118`, `MXD:B119` |
| REQ-MXD-SHAPER-FILE | Retained inventory/file identity only: 567592 bytes, SHA-256 9601e56ea49152c2e0b339b0862db1c24542a23db9bfd6db3d0b817ebd153590. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-SHAPER-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Clang

Surface `SURF-MAX-DS-CLANG`. Lifecycle setup: Clave on with Repeat nonzero, Tone A/B and Noise audible, Filter interior, nonzero Decay/Volume.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-CLANG-001 | Two Tone A/B levels are independent; Noise adds white-noise content. Named components do not define synthesis or RNG implementation. | D12;target U; `MXD:B009`, `MXD:B010`, `MXD:B012` |
| REQ-MXD-DS-CLANG-002 | Filter adjusts high-pass/band-pass cutoff and higher settings increase high-frequency content; no filter curve is given. | D12;target U; `MXD:B011` |
| REQ-MXD-DS-CLANG-003 | Clave enables Repeat for clave repetitions. | D12;target U; `MXD:B013` |
| REQ-MXD-DS-CLANG-004 | Pitch changes pitch, Decay sound length and Volume overall level; upper-half display click previews current settings. | D12;target U; `MXD:B014`, `MXD:B015` |
| REQ-MXD-DS-CLANG-FILE | Retained inventory/file identity only: 99786 bytes, SHA-256 08301ce7fa7066e8a03b9c9273c3b82b356c91405547b71fd66fff0060ed5ac4. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-CLANG-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Clap

Surface `SURF-MAX-DS-CLAP`. Lifecycle setup: Sloppy/Tail nonzero, Spread 50%, Tone interior, nonzero Decay/Volume.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-CLAP-001 | Sloppy changes spacing of panned clap delay lines; Tail adds filtered noise. Exact impulse/delay/noise law is not specified. | D12;target U; `MXD:B017`, `MXD:B018` |
| REQ-MXD-DS-CLAP-002 | Spread 0% is mono and 100% widened stereo; Tone higher increases high-frequency content. | D12;target U; `MXD:B019` |
| REQ-MXD-DS-CLAP-003 | Tune sets pitch, Decay sound length and Volume level. | D12;target U; `MXD:B020` |
| REQ-MXD-DS-CLAP-004 | Upper-half display click previews current settings. | D12;target U; `MXD:B021` |
| REQ-MXD-DS-CLAP-FILE | Retained inventory/file identity only: 125453 bytes, SHA-256 dcc971cc324deabcd1408389b8f448215503ada4d8005d53ab676fbef02d7da7. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-CLAP-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Cymbal

Surface `SURF-MAX-DS-CYMBAL`. Lifecycle setup: Tone interior, Pitch accepted, Decay/Volume nonzero;separated preview andnotes.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-CYMBAL-001 | Cymbal source includes sine/pulse and high-passed noise; Tone raises high-pass cutoff. Names provide no waveform or noise tolerance. | D12;target U; `MXD:B023`, `MXD:B024` |
| REQ-MXD-DS-CYMBAL-002 | Pitch, Decay and Volume adjust pitch, length and overall level. | D12;target U; `MXD:B025` |
| REQ-MXD-DS-CYMBAL-003 | Upper-half display click previews current settings. | D12;target U; `MXD:B026` |
| REQ-MXD-DS-CYMBAL-FILE | Retained inventory/file identity only: 82647 bytes, SHA-256 fea652375f4378f9cb7cbd28b2e7517424c7bb0098fd0fdac4ed1645b4271606. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-CYMBAL-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS FM

Surface `SURF-MAX-DS-FM`. Lifecycle setup: Amnt/Feedb. nonzero, Mod interior, Tone interior, Decay/Volume audible.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-FM-001 | Tone sets low-pass cutoff; Feedb. controls FM feedback with more noise at higher values. No feedback transfer law or alias bound is supplied. | D12;target U; `MXD:B029`, `MXD:B030` |
| REQ-MXD-DS-FM-002 | Amnt controls FM depth; Mod blends modulation types, whose exact identities/law are unspecified. | D12;target U; `MXD:B031` |
| REQ-MXD-DS-FM-003 | Pitch is global pitch, Decay sound length and Volume overall level. | D12;target U; `MXD:B032` |
| REQ-MXD-DS-FM-004 | Upper-half display click previews sound at current settings. | D12;target U; `MXD:B033` |
| REQ-MXD-DS-FM-FILE | Retained inventory/file identity only: 74711 bytes, SHA-256 575a3c09863f3d363d1ed433c653ab5449ff42213f13e9fd4aa419a74b65606b. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-FM-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS HH

Surface `SURF-MAX-DS-HH`. Lifecycle setup: Pink Noise,24 dB pitchedfilter, Attack nonzero, Tone interior, Decay/Volume audible.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-HH-001 | Hat combines noise/sine; Noise selects white or pink. | D12;target U; `MXD:B035`, `MXD:B036` |
| REQ-MXD-DS-HH-002 | Tone sets high-pass cutoff; pitched portion uses resonant high-pass with 12/24 dB slope choices and Attack. | D12;target U; `MXD:B037`, `MXD:B038` |
| REQ-MXD-DS-HH-003 | Pitch is global pitch, Decay sound length and Volume level. | D12;target U; `MXD:B039` |
| REQ-MXD-DS-HH-004 | Upper-half display click previews current settings. | D12;target U; `MXD:B040` |
| REQ-MXD-DS-HH-FILE | Retained inventory/file identity only: 48253 bytes, SHA-256 091f2f67e31905d4d98355b8bdc7e1a237b166347fb5142508b905a1f240df84. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-HH-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Kick

Surface `SURF-MAX-DS-KICK`. Lifecycle setup: Pitch 50 Hz ifaccepted, Drive/OT/Env nonzero, Click on, Attack/Decay/Volume audible.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-KICK-001 | Pitch is in Hz; Drive adds distortion and OT harmonics to modulated-sine kick. | D12;target U; `MXD:B042`, `MXD:B043` |
| REQ-MXD-DS-KICK-002 | Attack smooths sine onset; Click adds transient. | D12;target U; `MXD:B044` |
| REQ-MXD-DS-KICK-003 | Decay controls length, Env pitch modulation, Volume level. | D12;target U; `MXD:B045` |
| REQ-MXD-DS-KICK-004 | Upper-half display click previews current settings. | D12;target U; `MXD:B046` |
| REQ-MXD-DS-KICK-FILE | Retained inventory/file identity only: 97049 bytes, SHA-256 2e0a62e62d68e9afb20d6830826f13c77f1f314892fbad03ead79df723cbf7be. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-KICK-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Sampler

Surface `SURF-MAX-DS-SAMPLER`. Lifecycle setup: Owned sample S, Start interior, Length nonzero, Loop on, Tune +12, Shaper nonzero, Decay/Volume audible.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-SAMPLER-001 | Dated Version 12: load owned sample by dropping on upper display; Start changes sample start and Length playback length. Current HTML omits this profile; exact target availability/behavior U. | D12-2025;target U; `MX25:721:B003`, `MX25:721:B004` |
| REQ-MXD-DS-SAMPLER-002 | Dated Version 12: Tune spans -48 to +48 semitones; Loop toggles sample looping. No pitch/resampling/loop-boundary formula follows. | D12-2025;target U; `MX25:721:B005` |
| REQ-MXD-DS-SAMPLER-003 | Dated Version 12: Decay controls sample amplitude decay, Shaper distortion and Volume overall level. | D12-2025;target U; `MX25:721:B006` |
| REQ-MXD-DS-SAMPLER-FILE | Retained inventory/file identity only: 439147 bytes, SHA-256 6b9bdeec9c6557ada7c94b6536791a17fffe1750d7f2d1704de35be529a3cfa2. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-SAMPLER-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Snare

Surface `SURF-MAX-DS-SNARE`. Lifecycle setup: Color/Tone audible, noise Band Pass, nonzero Decay/Volume.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-SNARE-001 | Color changes pitched-oscillator tone; Tone controls noise presence. | D12;target U; `MXD:B048`, `MXD:B049` |
| REQ-MXD-DS-SNARE-002 | Noise filter choices are low-pass, high-pass and band-pass. | D12;target U; `MXD:B050` |
| REQ-MXD-DS-SNARE-003 | Decay adjusts length, Tune global pitch and Volume overall level. | D12;target U; `MXD:B051` |
| REQ-MXD-DS-SNARE-004 | Upper-half display click previews current settings. | D12;target U; `MXD:B052` |
| REQ-MXD-DS-SNARE-FILE | Retained inventory/file identity only: 84135 bytes, SHA-256 cb0e219cb366ebbd99c65c6341caf05e203eb11fa89f32a5759da78f8cd47b0d. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-SNARE-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## DS Tom

Surface `SURF-MAX-DS-TOM`. Lifecycle setup: Pitch 100 Hz ifaccepted, Color/Tone/Bend nonzero, Decay/Volume audible.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-DS-TOM-001 | Pitch is Hz; Color controls filter gain/cutoff, Tone level of resonant band-pass filters. | D12;target U; `MXD:B054`, `MXD:B055` |
| REQ-MXD-DS-TOM-002 | Bend adjusts pitch envelope, Decay length and Volume level. | D12;target U; `MXD:B056` |
| REQ-MXD-DS-TOM-003 | Upper-half display click previews current settings. | D12;target U; `MXD:B057` |
| REQ-MXD-DS-TOM-FILE | Retained inventory/file identity only: 149956 bytes, SHA-256 539abe4f2e12b98a24baaf622ac2c7e95dbce84985ed6866f7bae481f76fefc9. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-DS-TOM-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Envelope MIDI

Surface `SURF-MAX-ENVELOPE-MIDI`. Lifecycle setup: Nonzero ADSR/Amount, mapped target, Sustain on, Velocity on, Echo mode withnonzero Env Feedback/Time.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-ENVELOPE-MIDI-001 | Map then parameter click assigns target; Multimap exposes up to eight mappings and Unmap removes selected assignment. | D12;target U; `MXD:B123`, `MXD:B124`, `MXD:B125` |
| REQ-MXD-ENVELOPE-MIDI-002 | Modulation permits manual base-value edits with Bipolar centered/Unipolar one-direction depth; Remote Control owns mapped value and prevents manual edit, with Min/Max range. Documentary default Modulation is not a target constructor proof. | D12;target U; `MXD:B126`, `MXD:B127`, `MXD:B128` |
| REQ-MXD-ENVELOPE-MIDI-003 | ADSR mapping modes Free(note), Sync(division), Loop(Global Time), Echo(Time/Feedback); LED flashes each trigger. | D12;target U; `MXD:B122`, `MXD:B129`, `MXD:B130`, `MXD:B131`, `MXD:B132`, `MXD:B133`, `MXD:B134` |
| REQ-MXD-ENVELOPE-MIDI-004 | Global Time1.00 matches ADSR timing; above stretches/below compresses proportionally. Amount 0 none,100 maximum. | D12;target U; `MXD:B135`, `MXD:B136` |
| REQ-MXD-ENVELOPE-MIDI-005 | Attack/Decay/Sustain/Release and ADR Slope edit by values or display; Release returns envelope to0 after note release. | D12;target U; `MXD:B137`, `MXD:B138`, `MXD:B139`, `MXD:B140` |
| REQ-MXD-ENVELOPE-MIDI-006 | Velocity toggle scales envelope peak with incoming velocity. | D12;target U; `MXD:B141` |
| REQ-MXD-ENVELOPE-MIDI-007 | Sustain on holds level while note held then Release; off is one-shot Attack/Decay/Release regardless held duration. | D12;target U; `MXD:B142` |
| REQ-MXD-ENVELOPE-MIDI-FILE | Retained inventory/file identity only: 502857 bytes, SHA-256 e7523da46c9dd2ca7c2081d9e6b46cad73b2d0f29b5ae7feb5744b76913a6931. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-ENVELOPE-MIDI-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Expression Control

Surface `SURF-MAX-EXPRESSION-CONTROL`. Lifecycle setup: Five source tabs, IncrementSteps 4, Random Amount nonzero, active mapped targets, nonzero Rise/Fall, Modulate.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-EXPRESSION-CONTROL-001 | Five source tabs each select Velocity, Modwheel, Pitchbend, Pressure, Keytrack, Expression, Random, Increment, Slide, Sustain; Map then target click assigns selected source. | D12;target U; `MXD:B144`, `MXD:B145`, `MXD:B146` |
| REQ-MXD-EXPRESSION-CONTROL-002 | Modulate permits base edits and bipolar/unipolar ranges; Remote owns parameter and exposes Min/Max. Modulate OutputRange Max represents maximum input. | D12;target U; `MXD:B147`, `MXD:B148`, `MXD:B149` |
| REQ-MXD-EXPRESSION-CONTROL-003 | Linear curve has two points/Curve A; S-curve three, upperA/lowerB and linked inverse editing viaA; Min/Max and S-middleX/Y can edit with display. | D12;target U; `MXD:B150`, `MXD:B151`, `MXD:B152` |
| REQ-MXD-EXPRESSION-CONTROL-004 | Increment activates1-32Steps per cycle; Stop resets count so first note after restart outputs configured minimum. | D12;target U; `MXD:B153` |
| REQ-MXD-EXPRESSION-CONTROL-005 | Random activates Amount and changes deviation each note trigger; no stream/seed/distribution guaranteed. | D12;target U; `MXD:B154` |
| REQ-MXD-EXPRESSION-CONTROL-006 | Smoothing chooses linear/logarithmic; Rise/Fall times0-1000ms reach new rising/falling value. | D12;target U; `MXD:B155`, `MXD:B156` |
| REQ-MXD-EXPRESSION-CONTROL-FILE | Retained inventory/file identity only: 614704 bytes, SHA-256 6ac08cbcb0c96ec78eed2813ede18b0f92736305664822551d5d037f24199388. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-EXPRESSION-CONTROL-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Expression Control Legacy

Surface `SURF-MAX-EXPRESSION-CONTROL-LEGACY`. Lifecycle setup: ActualLegacyidentity, five global expression mappings, distinctMin/Max, Log shape, nonzero Rise/Fall.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-EXPRESSION-CONTROL-LEGACY-001 | Dated Version 12: Velocity, ModulationWheel, PitchBend, Aftertouch and Keytrack each map to one destination via Map then target click. This is Legacy, not current ten-source/five-tab device. | D12-2025;target U; `MX25:731:B003`, `MX25:731:B004` |
| REQ-MXD-EXPRESSION-CONTROL-LEGACY-002 | Dated Version 12: each mapping has independent Min/Max intensity and Log/Lin shape. | D12-2025;target U; `MX25:731:B005`, `MX25:731:B006` |
| REQ-MXD-EXPRESSION-CONTROL-LEGACY-003 | Dated Version 12: Rise/Fall smooth envelope attack/release; Output displays per-mapping output. | D12-2025;target U; `MX25:731:B007`, `MX25:731:B008` |
| REQ-MXD-EXPRESSION-CONTROL-LEGACY-004 | Dated Version 12 says Live 11 Sets containing Expression Control load renamed Expression Control Legacy. Exact target migration and all-version parity remain U. | D12-2025;target U; `MX25:730:B001` |
| REQ-MXD-EXPRESSION-CONTROL-LEGACY-FILE | Retained inventory/file identity only: 501849 bytes, SHA-256 ae8cf0e684150c681facef308ec5d971b8a14459ef828aa7c85ec5b01c09fc69. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-EXPRESSION-CONTROL-LEGACY-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## MIDI Monitor

Surface `SURF-MAX-MIDI-MONITOR`. Lifecycle setup: Note/Flow/MPEviews, two held noteswithdistinct expression, Freeze off, retained stream.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-MIDI-MONITOR-001 | Note view displays incoming notes, root/related chords on keyboard and velocity; chord recognition rules not specified. | D12;target U; `MXD:B158`, `MXD:B159`, `MXD:B160` |
| REQ-MXD-MIDI-MONITOR-002 | Flow lists incoming notes and controller data continuously; Freeze pauses/unpauses display and Clear empties it. | D12;target U; `MXD:B161` |
| REQ-MXD-MIDI-MONITOR-003 | MPE view lists incoming note, velocity, slide, pressure and per-note pitch streams. | D12;target U; `MXD:B162` |
| REQ-MXD-MIDI-MONITOR-FILE | Retained inventory/file identity only: 118902 bytes, SHA-256 21256e4da0dc20173de2a8be34b479f6485ae0c5731b56491ff57e8a43a923f1. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-MIDI-MONITOR-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## MPE Control

Surface `SURF-MAX-MPE-CONTROL`. Lifecycle setup: Three MPE sources on, S-curves distinct, Slide Rel, Smooth nonzero, conversion toggles explicit, two held notes.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-MPE-CONTROL-001 | Press, Slide, NotePB sources independently enable and transform MPE; source selection foregrounds curve. Documented default sources on is not constructor proof. | D12;target U; `MXD:B164`, `MXD:B167`, `MXD:B168` |
| REQ-MXD-MPE-CONTROL-002 | Linear(two points) or S(three) curves allow Min/Max, Curve and display editing; S middle X/Y and unlinkable two segment controls. | D12;target U; `MXD:B169`, `MXD:B170`, `MXD:B171`, `MXD:B172`, `MXD:B173` |
| REQ-MXD-MPE-CONTROL-003 | Advanced panel exposes per-source Smooth and independent Rise/Fall plus source-dependent options. | D12;target U; `MXD:B174`, `MXD:B175` |
| REQ-MXD-MPE-CONTROL-004 | Press Default supplies value to non-MPE notes; Swap to Slide redirects pressure; Press to AT converts to monophonic aftertouch. | D12;target U; `MXD:B177`, `MXD:B178`, `MXD:B179` |
| REQ-MXD-MPE-CONTROL-005 | Slide CC74 offers Default, Centered and Abs/Rel/Ons. Rel starts midrange and changes with subsequent sweep; Ons updates only at Note On and disables smoothing. | D12;target U; `MXD:B181`, `MXD:B182`, `MXD:B183` |
| REQ-MXD-MPE-CONTROL-006 | Slide to Mod converts to ModWheel CC1 for non-MPE instruments. | D12;target U; `MXD:B184` |
| REQ-MXD-MPE-CONTROL-007 | NotePB Pitch Range adjusts controller/instrument range relationship; manual gives2x for ±48 controller/±24 instrument. NotePB to PB converts to standard pitch bend. | D12;target U; `MXD:B186`, `MXD:B187`, `MXD:B188` |
| REQ-MXD-MPE-CONTROL-FILE | Retained inventory/file identity only: 489558 bytes, SHA-256 fc4e510279ab155fb03602bdfa3743628af00ef864c60e6f40d78830b8f36c7d. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-MPE-CONTROL-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Note Echo

Surface `SURF-MAX-NOTE-ECHO`. Lifecycle setup: Sync 4, nonzero Delay/Fback/Pitch, Input Thru, MPE on, Press/Slide/NotePBfeedback 50%, two held notes.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-NOTE-ECHO-001 | Creates MIDI note echoes with decreasing velocity; Sync divisions count sixteenths(4=quarter); off usesms; DelayTime percentage adjusts fraction. | D12;target U; `MXD:B190`, `MXD:B191`, `MXD:B192`, `MXD:B193` |
| REQ-MXD-NOTE-ECHO-002 | Input Thru passes original plus echoes;Mute removes original leaving echoes. | D12;target U; `MXD:B194` |
| REQ-MXD-NOTE-ECHO-003 | Pitch transposes each repeat;Delay controls echo velocity and Fback return amount. | D12;target U; `MXD:B195`, `MXD:B196` |
| REQ-MXD-NOTE-ECHO-004 | MPE on echoes incoming expression with notes;off filters MPE. On enables Press/Slide/NotePBfeedback;below100% progressively decays repeatedMPE. | D12;target U; `MXD:B197`, `MXD:B198` |
| REQ-MXD-NOTE-ECHO-FILE | Retained inventory/file identity only: 295446 bytes, SHA-256 cfff7695130008d9f7707d83e223d0e28288b7fbff35972ee2315c8b8493aa95. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-NOTE-ECHO-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |
## Shaper MIDI

Surface `SURF-MAX-SHAPER-MIDI`. Lifecycle setup: Nonflatshapeonesustain point, Loop on, nonzero Depth/Rate/Echo/Time, Velocity nonzero, active mapped target.

| Requirement | Contract and limits | Evidence/provenance |
| --- | --- | --- |
| REQ-MXD-SHAPER-MIDI-001 | Map then parameter click assigns target; Multimap exposes up to eight mappings and Unmap removes selected assignment. | D12;target U; `MXD:B201`, `MXD:B202`, `MXD:B203` |
| REQ-MXD-SHAPER-MIDI-002 | Modulation permits manual base-value edits with Bipolar centered/Unipolar one-direction depth; Remote Control owns mapped value and prevents manual edit, with Min/Max range. Documentary default Modulation is not a target constructor proof. | D12;target U; `MXD:B204`, `MXD:B205`, `MXD:B206` |
| REQ-MXD-SHAPER-MIDI-003 | MIDI notes trigger envelope;click creates point, Ctrl Win/Cmd Mac creates only one sustain point, Alt/Option curves, Shift-click deletes;Clear and six presets available. Sustainpoint holds while note held. | D12;target U; `MXD:B200`, `MXD:B207`, `MXD:B208`, `MXD:B209` |
| REQ-MXD-SHAPER-MIDI-004 | Grid/Snap nearestline editing;small outputdisplay andtriggerLED. | D12;target U; `MXD:B210`, `MXD:B211` |
| REQ-MXD-SHAPER-MIDI-005 | Jitter randomizes, Smooth softens, Offset sets center shift around 0. | D12;target U; `MXD:B212`, `MXD:B214` |
| REQ-MXD-SHAPER-MIDI-006 | Velocity 0% has no velocity effect;larger values scale lower/higher note velocities down/up. | D12;target U; `MXD:B213` |
| REQ-MXD-SHAPER-MIDI-007 | Loop repeats while note held at Rate and bypasses sustain point;Rate Hz/sync;Depth 0 none,100 maximum. | D12;target U; `MXD:B215`, `MXD:B216`, `MXD:B217` |
| REQ-MXD-SHAPER-MIDI-008 | Echo feedback control governs envelope repetitions;Time sets echo interval. | D12;target U; `MXD:B218` |
| REQ-MXD-SHAPER-MIDI-FILE | Retained inventory/file identity only: 560789 bytes, SHA-256 4b41f2e0f89ee67c3897dcae8969495af9fd26546674686173eddc8b93f30e44. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred. | Dpkg;target U; [Package ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) |
| REQ-MXD-SHAPER-MIDI-LIFECYCLE | Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes. | U;target U; Required unknown |

## Lifecycle and full-coverage obligations

Every profile retains distinct U cases `BOUNDARY`, `AUTOMATION`, `TRANSPORT`,
`PERSISTENCE`, `UNDO`, `MALFORMED`, `CANCEL`, `TEARDOWN`, `RATE` and `ROUTING`.
Their setup uses its named modes/controls/input, not a generic replacement profile.
Endpoints/adjacent text, excess mapping targets, overlapping notes, automation and
manual ownership, stop/seek/restart/tempo, save/reopen/missing AMXD/sample, undo/redo,
malformed copies/dependency loss, edit/save cancellation, target deletion/Set close,
44.1/48/96kHz and64/256 frames, sidechain/routing/MPE/tuning interactions remain U.
Do not force an unoffered control/route or label absence a pass. All failure tests
use disposable copies. These kinds are not omitted as inapplicable.

## Acceptance catalog

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/cases.json) and
[counts](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/counts.json) retain exact per-profile source/case relationships.
There are 135 requirements: 88 D12, 7 D12-2025, 20 Dpkg, 20 U. 315 unexecuted cases contain
88 D12, 7 D12-2025, 20 Dpkg, 200 U. Zero exact-target grades. The 200 lifecycle cases and numerous
signal obligations are not complete control/event-combination coverage.

| Device | D12 / D12-2025 / Dpkg / U requirements | Cases |
| --- | --- | --- |
| Align Delay | 3 / 0 / 1 / 1 | 14 |
| Envelope Follower | 6 / 0 / 1 / 1 | 17 |
| LFO | 7 / 0 / 1 / 1 | 18 |
| Shaper | 7 / 0 / 1 / 1 | 18 |
| DS Clang | 4 / 0 / 1 / 1 | 15 |
| DS Clap | 4 / 0 / 1 / 1 | 15 |
| DS Cymbal | 3 / 0 / 1 / 1 | 14 |
| DS FM | 4 / 0 / 1 / 1 | 15 |
| DS HH | 4 / 0 / 1 / 1 | 15 |
| DS Kick | 4 / 0 / 1 / 1 | 15 |
| DS Sampler | 0 / 3 / 1 / 1 | 14 |
| DS Snare | 4 / 0 / 1 / 1 | 15 |
| DS Tom | 3 / 0 / 1 / 1 | 14 |
| Envelope MIDI | 7 / 0 / 1 / 1 | 18 |
| Expression Control | 6 / 0 / 1 / 1 | 17 |
| Expression Control Legacy | 0 / 4 / 1 / 1 | 15 |
| MIDI Monitor | 3 / 0 / 1 / 1 | 14 |
| MPE Control | 7 / 0 / 1 / 1 | 18 |
| Note Echo | 4 / 0 / 1 / 1 | 15 |
| Shaper MIDI | 8 / 0 / 1 / 1 | 19 |

## Revision-specific source questions and limits

The current English chapter has 18 profiles, while the installed inventory has 20:
DS Sampler and Expression Control Legacy are supplied files but missing as current
English headings. Their own dated Version 12 sections supply useful documented
controls, not exact 12.4.3 support/default/migration proof. Dated PDF p731 begins
with current Expression Control text before its Legacy heading; those preceding
paragraphs are excluded from Legacy evidence. Dated migration context p730 says
Live 11 Expression Control Sets load Legacy; no such Set or target-load result is
retained. It does not authorize transferring modern sources/curves/Random or
Increment to Legacy. The source-version/context gap remains required U, not a
contradiction or current-profile alias.

MPE Control range 2x is retained only as the source's controller ±48/instrument ±24
example; no multiplication/division or clipping formula is inferred. Display
Freeze in MIDI Monitor is not host track Freeze or device pass-through. Note
Echo Input Mute and MPE filtering have distinct roles. Shaper MIDI sustain bypass
when Loop on is distinct from Shaper 1-Shot/Manual and Envelope MIDI Sustain mode.
Mapping Modulation and Remote Control ownership is specified per actual source
paragraph, not by shared class or presumed global modulation law.

## Analyst evidence appendix

[Source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/sources.json) pins two documentary revisions and frozen
inventory/TOC. Current official [Max devices chapter](https://www.ableton.com/en/live-manual/12/max-for-live-devices/),
captured 2026-10-19,299,403 bytes, SHA-256
`b95a0d3ed3d7217505437a0d7d65de68d37e0f894d27e9869122fbfb89728a46`.
[218 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manual-blocks.json) retain exact HTML lines and full
heading context through 33.3.6; sidebar/footer excluded.
[HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manual-max-devices-2026-10-19.html) is immutable source.

Official [dated English Version 12 PDF](https://cdn-resources.ableton.com/resources/pdfs/live-manual/12/2025-06-02/live12-manual-en.pdf),
76,333,838 bytes, SHA-256
`42fbd3794df0d69aaf522aea589bf08dd3dc8db3eb0e135cab041093875db976`.
[Metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/source-dated-pdf.json) and [retained PDF](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manual-12-2025-06-02.pdf)
pin capture identity; only physical pages 721/730/731 support this packet.
[15 dated blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/dated-blocks.json) retain exact page/text-line ranges,
including headings/captions and one separately labelled migration paragraph.
Page text is derived with existing `pdftotext`; diagrams were not inspected.
No other dated-PDF device prose is imported into current requirements.

[Twenty AMXD identities](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/package-identities.json) retain exact external
file paths, byte counts, hashes and 16-byte prefixes matching the frozen inventory.
Contents were not parsed/copied into contracts or executed. Reproduction depends
on those retained external paths; the manual and package identity establish no
arbitrary API/patch or complete-product behavior.
[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/manifest-author-r1.json) freezes payloads/canonical
snapshots; [validation](../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/validation-author-r1.json) checks hashes, locators,
requirements/cases, browser discovery, links and whitespace only. No handoff is
published; all twenty profiles remain partial and pending independent review.
