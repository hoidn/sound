---
id: SPEC-MODULATION-PITCH-LOOP-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary behavior with exact-build applicability unknown
---

# Modulation, pitch, spectral and looping devices

## Scope and authority

This partial F-06 draft owns ten individual current native profiles under the
[full product inventory](../research/full-live-coverage-inventory.md). It covers
documented modes, controls, routing, capture and state roles. It establishes
neither full DSP nor completed device profiles and is not a released implementation
input. [Coverage design](../research/full-live-specification-design.md) governs
closure; the [research owner](../research/modulation-pitch-loop-devices.md) owns
source interpretation and the reviewed spectral association correction.

**D12** means documentary prose from the retained official Version 12 manual,
captured 2026-10-19. **Every runtime clause's exact 12.4.3 applicability is U.**
Installed schema/preset observations are Dpkg presence only; names and historical
preset Creator values prove no DSP, constructor default, enum domain or runtime
control law. U outcomes have `expected: null`, no comparator and no pass.
There is no S/X execution or original-versus-candidate result in this packet.

[Device chains/racks](device-racks.md) owns common insertion, bypass, presets,
chain order and tail gating. [Automation envelopes](automation-envelopes.md)
owns its finite storage/evaluation contract; it does not prove these controls'
automation eligibility or smoothing. [Tuning systems](tuning-systems.md) and
[MPE workflows](mpe-workflows.md) retain global context/codec gaps; Auto Shift,
Shifter and Spectral Resonator keep their own destinations and voice behavior.
[Recording/comping](recording-comping.md) owns track recording/Capture MIDI,
which do not specify Looper recording or Spectral Time freezing. The seven-device
[bundled-host draft](bundled-device-hosting.md) does not cover these ten devices.
[Clip launch](clip-launch.md), [transport](transport-state.md),
[media files](media-file-workflows.md) and [mix graph](mix-graph.md) supply only
their already bounded contracts. Looper-specific quantization, import/export and
Insert-Looper paths belong here. Common Link/network behavior remains open.

The legacy Auto Pan, Chorus, Phaser, Flanger and Frequency Shifter profiles
remain separate owners; current device prose is not their alias or behavior
contract. Spectral Resonator is associated with `Transmute` (schema line 8118),
Spectral Time with `Spectral` (line 7423) by checked shipped folder/root/control
vocabulary. This corrects two discovery associations without changing frozen
inventory bytes or deriving runtime semantics from field names.

## Inputs, observations and grading

Use a valid editable test-owned Set and an isolated enabled device; select all
named modes, source/tapping points and amounts explicitly. Reset memory, latches,
held notes and capture histories between independent trials. Source, wet path,
monitoring and output must be active and unmuted. No-effect or silence proposals
need a paired positive baseline with an active path, appropriate stimulus and
nonzero amount. A dry-only path, disabled section, zero send, absent carrier/note,
muted output or zero modulation is insufficient evidence about active processing.
Only deliberate documented zero exceptions change their target setting to zero.

[Stimulus recipes](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/stimulus-recipes.json)
retain concrete 4/4, 120 BPM, 48 kHz, four-second tone/burst and owned MIDI setups.
These are analyst choices, not product limits or captured reference outputs.
Input tone formulas define inputs only. Distinct stereo inputs are not assumed
to yield equal signals merely because channel LFO waveforms coincide.
Unpitched/voiced recordings and hardware inputs must be retained and identified
before a future case uses them. No source material was played or recorded here.

The packet contains **106 requirements: 96 D12 clauses and ten U lifecycle
obligations**; **186 unexecuted cases** contain 46 documented control proposals,
9 documented state proposals, 41 ungraded signal obligations and 90 U lifecycle
cases. Documentary proposals compare only the named choices/units/endpoints or
visible transitions. All 186 exact-target expectations/grades remain null/U.
No waveform, frequency/pitch codec, filter/FFT/coefficient, random seed/distribution,
clock rounding, measured latency, deadline or tolerance is invented. Public
processing descriptions impose no private algorithm or candidate architecture.

## Individual requirements

Every following behavioral row is D12/target-U. Evidence cells identify exact
block IDs in this packet; each block retains HTML line, section/heading context
and text in the analyst appendix. Corresponding `MPL-<device>-NNN` cases retain
finite setup/action and a documentary expectation, with signal grading null.

### Auto Pan-Tremolo

Current surface `SURF-DEVICE-AUTO-PAN-TREMOLO`; artifact association `AutoPan2` / latest schema line 695.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-AP-001 | Panning uses two LFOs to alternate channel amplitudes; Tremolo uses one amplitude LFO. Mode changes waveform/control presentation and position versus amplitude visualization. | `auto-pan-tremolo:B003, B004` |
| REQ-MPL-AP-002 | Waveform choices are Sine, Triangle, Shark Tooth, Saw Up, Saw Down, Square, Random, Wander and S&H. | `auto-pan-tremolo:B005` |
| REQ-MPL-AP-003 | Time modes are Rate, Time, Synced, Dotted, Triplet and 16th. Rate exposes Freq in Hz; Time exposes Time in ms with 100 ms to 200 s period; beat modes expose Rate in beat divisions. | `auto-pan-tremolo:B006, B016` |
| REQ-MPL-AP-004 | Stereo Offset offers Phase or Spin, but Random, Wander and S&H permit Phase only. Phase offsets channel LFOs in degrees; 180 degrees is opposite phase; Spin progressively diverges them by percentage. | `auto-pan-tremolo:B007` |
| REQ-MPL-AP-005 | Phase Offset is available for beat-division Time modes and offsets LFO cycle start relative to grid; with Random, Wander or S&H it functions as stereo width. | `auto-pan-tremolo:B008, B009` |
| REQ-MPL-AP-006 | Invert flips LFO polarity. Shape changes Panning overlap/transition and Tremolo rounded versus angular peaks; ramp extrema with Invert off/on produce gating/pumping. | `auto-pan-tremolo:B010, B018` |
| REQ-MPL-AP-007 | Tremolo offers Harmonic, alternating high/low modulation around a fixed 600 Hz crossover, and Vintage, adding nonlinear shaping to amplitude modulation. | `auto-pan-tremolo:B011, B012, B013` |
| REQ-MPL-AP-008 | Amount determines modulation depth; Amount and LFO rate values are shared by Panning and Tremolo rather than independently stored per mode. | `auto-pan-tremolo:B015, B017` |
| REQ-MPL-AP-009 | Attack Time sets milliseconds to reach maximum modulation after a detected transient; longer values preserve initial transient center/impact before sustained modulation. | `auto-pan-tremolo:B019` |
| REQ-MPL-AP-010 | Dynamic Frequency Modulation makes louder input increase LFO rate at positive values and decrease it at negative values. | `auto-pan-tremolo:B020` |

**REQ-MPL-AP-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Auto Shift

Current surface `SURF-DEVICE-AUTO-SHIFT`; artifact association `AutoShift` / latest schema line 754.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-AS-001 | Auto Shift processes monophonic audio. Input Pitch displays note/cents; High/Mid/Bass range LEDs indicate matching input range; range changes affect latency. Input Gain ranges -24 to +24 dB. Live Mode reduces latency with possible onset/rapid-change glitches. | `auto-shift:B002, B005, B006, B007, B008, B009` |
| REQ-MPL-AS-002 | MIDI In shows/hides routing panel; MIDI On activates input and replaces Quantizer with MIDI tab. Source selects a separate MIDI track; Pre FX bypasses its MIDI effects and Post FX/Post Mixer includes them. | `auto-shift:B011, B012, B013, B014, B024` |
| REQ-MPL-AS-003 | Mono uses one correction voice and Glide for overlapping notes. Poly offers maximum counts 2, 4 or 8. | `auto-shift:B015` |
| REQ-MPL-AS-004 | In MIDI mode the processed path only produces sound when notes are received. Dry/Wet mixes original/processed, so dry monitoring must be excluded when testing this condition. | `auto-shift:B016, B052` |
| REQ-MPL-AS-005 | Quantizer follows selected/included scale notes; meter reports cents correction and target note. Correction Strength increases correction; Smooth retains more natural vibrato and smooths transitions with 0-200 ms Smoothing Time. Scale-degree Pitch Shift follows correction. | `auto-shift:B018, B019, B020, B021` |
| REQ-MPL-AS-006 | Use Current Scale follows clip scale, highlights included notes purple and disables Root/Scale choosers. Scale awareness is unavailable with MIDI input; source Scale MIDI effect needs Post FX/Post Mixer to apply. | `auto-shift:B022, B026` |
| REQ-MPL-AS-007 | MIDI tab visualizes received notes and offers Attack 0-1000 ms, Release 0-5 s, Note Latch holding until next Note On, and Pitch Bend Range 0-48 semitones. | `auto-shift:B025, B027, B028, B029` |
| REQ-MPL-AS-008 | Pitch, Formant, Volume and Pan each offer Velocity, Pressure, Mod Wheel, Pitch Bend, Note PB or Slide as modulation sources with dedicated depth. | `auto-shift:B029` |
| REQ-MPL-AS-009 | LFO Reset retriggers phase at note onset. Quantizer onset follows a period of unpitched audio; MIDI onset is start of a new note; indicator changes from Onset to Trigger. | `auto-shift:B031, B032` |
| REQ-MPL-AS-010 | LFO Delay is 0-1.5 s, Attack 0-2 s. Waveforms are Sine, Triangle, Triangle 8, Triangle 16, Saw Up, Saw Down, Rectangle, Random, Random S&H. Rate uses ms or tempo divisions; depths target Pitch/Formant/Volume/Pan. | `auto-shift:B033, B034, B035, B036` |
| REQ-MPL-AS-011 | LFO, semitone/cent Pitch Shift and Formant Shift work without correction. Formant Shift spans -100% to +100%; Formant Follow sets how much formants follow pitch shifting. | `auto-shift:B037, B040, B041, B042, B043` |
| REQ-MPL-AS-012 | Vibrato works with/without correction; Amount is 0-200 cents, Rate 2-15 Hz, Fade In is ms and Natural adds rate/depth variation. Dry/Wet ranges from original at 0% to processed at 100%, with balanced 50%. | `auto-shift:B045, B046, B047, B048, B049, B050, B051, B052` |

**REQ-MPL-AS-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Chorus-Ensemble

Current surface `SURF-DEVICE-CHORUS-ENSEMBLE`; artifact association `Chorus2` / latest schema line 1178.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-CE-001 | Mode chooser selects Chorus, Ensemble or Vibrato; display shows active delay lines. Chorus adds time-modulated delays; Ensemble describes three phase-offset delays; Vibrato emphasizes pitch modulation. | `chorus-ensemble:B003, B004, B005, B006` |
| REQ-MPL-CE-002 | Each mode offers high-pass enable and frequency 20 Hz to 2 kHz; enabled filter reduces modulation below chosen frequency. | `chorus-ensemble:B007` |
| REQ-MPL-CE-003 | Chorus/Ensemble Width sets wet mid/side balance: 0% mono, 100% balanced and 200% sides twice mid level. | `chorus-ensemble:B008` |
| REQ-MPL-CE-004 | Chorus offers Auto or fixed Delay Time and one/two taps. Auto scales delay per tap with modulation amount; fixed delay does not scale with amount. | `chorus-ensemble:B009` |
| REQ-MPL-CE-005 | Vibrato offers channel Offset with opposite LFO phase at 180 degrees and Shape from sine at 0% to triangle at 100%. | `chorus-ensemble:B010` |
| REQ-MPL-CE-006 | Rate is Hz; Amount controls delay-time modulation; Feedback feeds each channel output to input and can produce audible delays after stop; Feedback Invert reverses feedback polarity. | `chorus-ensemble:B012, B013, B014` |
| REQ-MPL-CE-007 | Feedback and Dry/Wet controls are disabled in Vibrato mode. | `chorus-ensemble:B014, B018` |
| REQ-MPL-CE-008 | Output gains processed signal; Warmth adds distortion/filtering; Dry/Wet balances processed/original outside Vibrato. | `chorus-ensemble:B016, B017, B018` |

**REQ-MPL-CE-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Phaser-Flanger

Current surface `SURF-DEVICE-PHASER-FLANGER`; artifact association `PhaserNew` / latest schema line 6054.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-PF-001 | Phaser/Flanger/Doubler select distinct display/control roles. Phaser offers Notches, Center, Spread and Blend (Center at 0, Spread at 1); Flanger/Doubler offer Time with opposite visualization directions. | `phaser-flanger:B003, B004, B005, B006, B007, B008, B009, B010, B011, B012` |
| REQ-MPL-PF-002 | Unfold reveals main LFO detail, second LFO, envelope and Safe Bass. Main Freq/Rate is Hz or tempo-sync. Shapes include Sine, Triangle, Saw Up/Down, Rectangle, Random, Random S&H, Triangle Analog/8/16. | `phaser-flanger:B013, B014, B015, B016, B017, B018` |
| REQ-MPL-PF-003 | Phase changes channel LFO relationship with opposite phase at 180 degrees; Spin detunes the two LFO rates. | `phaser-flanger:B019, B020, B021` |
| REQ-MPL-PF-004 | Duty Cycle skews the waveform period toward front at +100% or back at -100%, neutral at 0%; it does not affect Random or Random S&H. | `phaser-flanger:B022` |
| REQ-MPL-PF-005 | LFO2 is triangular, with independent Hz/synced rate. LFO2 Mix 0% selects main only and 100% selects LFO2 only. | `phaser-flanger:B023, B024, B025` |
| REQ-MPL-PF-006 | Amount affects both LFOs. Feedback returns channel output, supports polarity inversion, and in Doubler can continue as audible delays after stop; high feedback may raise levels quickly. | `phaser-flanger:B027, B028, B029` |
| REQ-MPL-PF-007 | Envelope modulation requires Env Fol on and nonzero Envelope Amount; negative amount inverts envelope phase. Attack/Release govern rising/falling modulation response. | `phaser-flanger:B030, B031, B032` |
| REQ-MPL-PF-008 | Safe Bass is a high-pass reducing effect below selected frequency, with 5-3000 Hz range. | `phaser-flanger:B033` |
| REQ-MPL-PF-009 | Output gains processed signal; Warmth adds distortion/filtering; Dry/Wet balances processed/original. | `phaser-flanger:B034` |

**REQ-MPL-PF-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Shifter

Current surface `SURF-DEVICE-SHIFTER`; artifact association `Shifter` / latest schema line 7036.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-SH-001 | Pitch mode exposes semitone Coarse and cent Fine transposition; Freq shifts Hz; Ring adds/subtracts the entered Hz frequency to/from input. | `shifter:B004, B021, B022, B023, B024` |
| REQ-MPL-SH-002 | Wide inverts Spread for right channel, shifting right down while left shifts up; Wide has no effect at Spread zero. | `shifter:B005` |
| REQ-MPL-SH-003 | Pitch offers Window size; Tone cuts high frequencies in delay feedback. Delay enable exposes free or beat-synced time and Feedback; source describes free units as Hertz. | `shifter:B006, B007` |
| REQ-MPL-SH-004 | LFO offers Duty Cycle, Phase/Spin and beat-sync Offset. Deterministic shapes allow Phase/Spin; Random uses Phase, Random S&H uses Width. Width endpoints describe LFO channels, not necessarily equal/opposite audio. | `shifter:B010, B011, B012, B013, B014` |
| REQ-MPL-SH-005 | LFO choices are Sine, Triangle, Triangle Analog, Triangle 8/16, Saw Up/Down, Rectangle, Random and Random S&H; Rate is Hz or tempo subdivisions and Amount sets modulation. | `shifter:B012, B015` |
| REQ-MPL-SH-006 | Env Fol enables input-amplitude modulation; Attack/Release govern rising/falling response. Amount uses semitones in Pitch or Hz in Freq/Ring. | `shifter:B017, B018, B019` |
| REQ-MPL-SH-007 | Drive distortion is available only in Ring mode, with amount slider. | `shifter:B025` |
| REQ-MPL-SH-008 | Dry/Wet balances original/processed output. | `shifter:B026` |
| REQ-MPL-SH-009 | Unfolded Pitch Mode selects Internal (Coarse/Fine) or MIDI (incoming note). MIDI exposes source, Glide in ms and PB range 0-24 semitones. | `shifter:B028, B029` |

**REQ-MPL-SH-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Spectral Resonator

Current surface `SURF-DEVICE-SPECTRAL-RESONATOR`; artifact association `Transmute` / latest schema line 8118.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-SR-001 | Internal fixes resonator pitch; MIDI follows external notes. MIDI source/tapping chooses before/after source effects; Mono/Poly selects one or poly voices, with Polyphony 2-16. | `spectral-resonator:B002, B004, B005, B006, B007, B008` |
| REQ-MPL-SR-002 | Mono MIDI Gate on requires held notes for resonance; off still responds to audio. Gate is always active in Poly. Glide is active only in Mono; PB is 0-24 semitones and MPE reception is supported. | `spectral-resonator:B009, B010, B011` |
| REQ-MPL-SR-003 | Internal Freq supports Hz or note; Use Current Scale replaces it with SD Shift and follows clip scale or chromatic when no scale active. MIDI Transp spans +/-48 semitones or +/-28 scale degrees. Active tuning makes Freq/Transp use note indices. | `spectral-resonator:B013, B014, B015` |
| REQ-MPL-SR-004 | Stretch compresses spacing below 0 and expands above; 100% produces odd harmonics. Shift transposes input spectrum +/-48 semitones, distinct from resonator spectrum. | `spectral-resonator:B016, B017` |
| REQ-MPL-SR-005 | Decay controls resonance persistence; HF/LF Damp affect partials in ranges following current/internal or incoming MIDI pitch. | `spectral-resonator:B018, B019` |
| REQ-MPL-SR-006 | Modulation modes None, Chorus, Wander and Granular select no modulation, triangle partial modulation, random sawtooth, or random exponential-envelope grains respectively. Mod Rate/Pch. Mod set rate and pitch range. | `spectral-resonator:B021, B022, B023, B024, B025, B026` |
| REQ-MPL-SR-007 | None applies no modulation; Chorus at Mod Rate zero modulates partial amplitudes only. Pitch modulation is bipolar except Granular's positive grain envelopes. | `spectral-resonator:B022, B023, B024, B025, B026` |
| REQ-MPL-SR-008 | Spectrogram displays dry yellow/wet blue and can hide. Harmonics sets count shared evenly across poly voices; Quantize snaps harmonics to active scale/tuning or chromatic fallback. | `spectral-resonator:B028, B029, B030` |
| REQ-MPL-SR-009 | Input Send gains processed signal with limiter-use LED; Unison adds detuned partial copies and Uni. Amt sets detuning. Wander/Granular modulate voices independently. Dry/Wet balances paths. | `spectral-resonator:B032, B033, B034` |

**REQ-MPL-SR-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Spectral Time

Current surface `SURF-DEVICE-SPECTRAL-TIME`; artifact association `Spectral` / latest schema line 7423.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-ST-001 | Freezer and Delay have separate On controls; Frz > Dly/Dly > Frz selects processing order. Generic freezer-feeds-delay prose is read in Frz > Dly context, not as unconditional order. | `spectral-time:B003, B016, B032` |
| REQ-MPL-ST-002 | Spectrogram dry/wet is yellow/blue and hideable. Zero Dry Signal Latency avoids aligning dry to processed output. Lower Resolution reduces latency at fidelity cost. | `spectral-time:B004, B005, B029` |
| REQ-MPL-ST-003 | Freezer must be On and Freeze toggled for effect in both Manual/Retrigger. Manual Freeze captures audio with Fade In/Fade Out in ms. | `spectral-time:B007, B008` |
| REQ-MPL-ST-004 | Retrigger offers Onsets with Sensitivity 0-100% (lowest/highest) or Sync with Interval in ms or beat time. | `spectral-time:B009, B010, B011` |
| REQ-MPL-ST-005 | Retrigger Crossfade fades new freeze in while old/dry fades out; X-Fade is relative to interval. Envelope uses ms Fade In/Out and stacks up to eight simultaneous freezes. | `spectral-time:B012, B013, B014` |
| REQ-MPL-ST-006 | Delay Time modes are Time (ms), Notes (beat divisions), 16th, 16th Triplet and 16th Dotted (count of selected sixteenths). | `spectral-time:B017, B018, B019, B020` |
| REQ-MPL-ST-007 | Delay Feedback returns output to input; Shift adds frequency shift per successive delay; Stereo adjusts Tilt/Spray width. Delay Dry/Wet affects only Delay section. | `spectral-time:B021, B022, B023, B024` |
| REQ-MPL-ST-008 | Positive Tilt delays high frequencies more, negative delays low more; Spray randomizes frequency delay times in its range; positive/negative Mask limits Tilt/Spray to high/low frequencies. | `spectral-time:B025, B026, B027` |
| REQ-MPL-ST-009 | Input Send sets input gain; global Dry/Wet balances whole processed/dry device, separate from Delay Dry/Wet. | `spectral-time:B031, B032, B033` |

**REQ-MPL-ST-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Vocoder

Current surface `SURF-DEVICE-VOCODER`; artifact association `Vocoder` / latest schema line 8542.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-VO-001 | Device track input is modulator; carrier choices are Noise, External, Modulator and Pitch Tracking. Noise X/Y changes downsampling/density; External selects internal audio routing; Modulator uses same input for both roles. | `vocoder:B003, B004, B005, B006, B007, B008` |
| REQ-MPL-VO-002 | Pitch Tracking is monophonic, bounded by High/Low and selectable sawtooth/three pulse shapes with coarse Pitch. It updates only on clear pitch and holds last detected pitch otherwise; reset/grouping may change sound. | `vocoder:B009` |
| REQ-MPL-VO-003 | Enhance normalizes carrier spectrum/dynamics for brightness; Unvoiced adds noise. Sens 100% keeps unvoiced generator on, 0% uses main carrier only; Fast/Slow changes detection switching. | `vocoder:B010, B011, B012` |
| REQ-MPL-VO-004 | Band display allows attenuation; Bands selects filter count; Range limits filter frequencies; BW controls overlap. Precise has equal gain/bandwidth; Retro narrows/raises higher bands. | `vocoder:B013, B014, B015, B016` |
| REQ-MPL-VO-005 | Gate silences below-threshold filter bands; Level sets output gain. Depth 0% discards modulator envelope, 100% classic vocoding, 200% uses high-amplitude peaks. Attack/Release govern amplitude response. | `vocoder:B017, B018, B019, B020` |
| REQ-MPL-VO-006 | Channel modes are Mono (both mono), Stereo (mono modulator/stereo carrier) and L/R (both stereo). | `vocoder:B021` |
| REQ-MPL-VO-007 | Formant shifts carrier filterbank frequencies; Dry/Wet balances modulator original and processed result. | `vocoder:B022, B023` |
| REQ-MPL-VO-008 | External vocoding uses vocal/modulator track and separate synthesizer carrier track selected in Audio From; Post FX is recommended. Live-input example arms both tracks; soloing voice track isolates documented vocoded result. | `vocoder:B028, B029, B030, B031, B032, B033` |

**REQ-MPL-VO-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Beat Repeat

Current surface `SURF-DEVICE-BEAT-REPEAT`; artifact association `BeatRepeat` / latest schema line 868.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-BR-001 | Interval ranges 1/32 to 4 Bars and is tempo-relative; Offset shifts capture forward. At Interval 1 Bar, Offset 8/16 selects third beat in a four-beat-bar example. | `beat-repeat:B003` |
| REQ-MPL-BR-002 | Chance 100% always repeats at requested Interval/Offset; 0% never repeats. | `beat-repeat:B004` |
| REQ-MPL-BR-003 | Gate sets total repeat span in sixteenths; Grid sets slice size. Gate 4/16 spans one beat. Repeat overrides automatic timing/chance/gate and captures/repeats until disabled. No Triplets makes grid binary. | `beat-repeat:B005, B006, B007` |
| REQ-MPL-BR-004 | Variation 0 fixes Grid; greater values vary it. Variation modes Trigger, 1/4, 1/8, 1/16 and Auto schedule changes at trigger, periodic intervals or each repetition. | `beat-repeat:B007, B008` |
| REQ-MPL-BR-005 | Pitch lowers repeats by resampling and lengthens segments without recompression; Pitch Decay lowers each successive slice. | `beat-repeat:B009` |
| REQ-MPL-BR-006 | Combined low/high-pass filter has enable, center frequency and passed-band width. | `beat-repeat:B010` |
| REQ-MPL-BR-007 | Mix passes original and adds repeats; Insert mutes original only during repeats; Gate passes only repeats. | `beat-repeat:B011` |
| REQ-MPL-BR-008 | Volume sets output level and Decay fades repetitions. | `beat-repeat:B012` |

**REQ-MPL-BR-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

### Looper

Current surface `SURF-DEVICE-LOOPER`; artifact association `Looper` / latest schema line 3931.

| Requirement | Documented observable contract and limits | Evidence |
| --- | --- | --- |
| REQ-MPL-LP-001 | Record captures and overwrites existing loop; Overdub adds layers at original length; Play plays without new recording; Stop halts playback. Display is red recording, then position/length in bars/beats. Running Set uses selected quantization; stopped Set acts immediately. | `looper:B003, B004, B005` |
| REQ-MPL-LP-002 | Clear during Overdub with running global transport empties buffer but preserves tempo/length; other modes reset tempo/length. | `looper:B006` |
| REQ-MPL-LP-003 | Looper Undo removes material since latest Overdub enable, preserving original and earlier overdub passes; Redo restores removed pass. | `looper:B007` |
| REQ-MPL-LP-004 | Multi-Purpose single click: empty to Record; Record/Overdub/Stopped to Play; Play to Overdub. Double click stops Play/Overdub. Two-second hold in Play invokes Undo/Redo; hold stopped clears. | `looper:B008, B009` |
| REQ-MPL-LP-005 | Multi-Purpose button supports MIDI-foot-switch mapping through MIDI Map Mode, clicking control, pressing switch then exiting mapping. | `looper:B010` |
| REQ-MPL-LP-006 | Tempo Control None decouples internal/global tempo; Follow changes playback speed to global tempo; Set & Follow sets global tempo from recorded material then follows later global changes. | `looper:B011, B012, B013, B014` |
| REQ-MPL-LP-007 | With Set running, x bars records until another transport button; fixed bars stops at chosen length into Play/Overdub. With Set stopped, x bars guesses tempo at Overdub/Play/Stop, while fixed bars fits recording into chosen bars. | `looper:B015, B016, B017` |
| REQ-MPL-LP-008 | Song Control None leaves global transport; Start Song starts global on entering Play/Overdub but Stop leaves it; Start & Stop Song also stops global. Start via Looper adjusts connected Link apps' phrase position. | `looper:B018, B019, B020, B021, B022` |
| REQ-MPL-LP-009 | x2 duplicates existing buffer and doubles length; /2 retains currently playing half and discards the other half. | `looper:B023, B024` |
| REQ-MPL-LP-010 | Drag me exports buffer to browser/track as file/clip with Re-Pitch Warp default; dragging audio file into Drag me replaces buffer and allows later overdubs. | `looper:B025` |
| REQ-MPL-LP-011 | Speed changes playback speed/pitch; octave arrows double/halve speed and are quantized. Reverse plays previous audio backwards; overdubs made reversed play forward then reverse when Reverse is disabled; Reverse is quantized. | `looper:B026, B027` |
| REQ-MPL-LP-012 | Feedback acts only in Overdub and changes next repetition: 100% retains old level, 50% halves each pass. Play repetitions keep level regardless of Feedback. | `looper:B028` |
| REQ-MPL-LP-013 | Input -> Output options: Always; Never; Rec/OVR (Record/Overdub); Rec/OVR/Stop (all except Play). These govern input monitoring independently of stored-loop playback. | `looper:B029, B030, B031, B032, B033` |
| REQ-MPL-LP-014 | Looper can source and receive internal audio through Insert-Looper: route another track from/to Looper, select Insert-Looper taps, Monitor In and use Overdub for processed feedback layers. | `looper:B035, B036, B037, B038, B039, B040, B041, B042, B043, B044` |

**REQ-MPL-LP-LIFECYCLE — U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.

## Device-specific lifecycle and boundary obligations

Each row has nine distinct retained cases, one each for numeric/tempo boundary,
automation, transport stop/seek/restart, persistence/source loss, global undo/redo,
malformed input/state, cancellation, teardown and sample-rate change. Case IDs
are `MPL-<prefix>-U-BOUNDARY`, `-AUTOMATION`, `-TRANSPORT`, `-PERSISTENCE`, `-UNDO`,
`-MALFORMED`, `-CANCEL`, `-TEARDOWN` and `-SAMPLE-RATE`. Their expected values and
comparators are null. There is no lifecycle omission classified inapplicable:
these are required unknowns. Malformed tests use disposable copies and input
text, never immutable evidence or recovered source code.

| Device / U requirement | Concrete state requiring those nine outcomes |
| --- | --- |
| Auto Pan-Tremolo / REQ-MPL-AP-LIFECYCLE | Wander waveform in Synced Panning, Amount nonzero, Phase Offset nonzero; controls under transition: Amount, Time mode and Phase Offset. |
| Auto Shift / REQ-MPL-AS-LIFECYCLE | MIDI On, Poly 8, source with held notes, Note Latch on, attack/release nonzero; controls under transition: MIDI On, correction strength, modulation depth and pitch range. |
| Chorus-Ensemble / REQ-MPL-CE-LIFECYCLE | Chorus with nonzero Feedback and Amount, then Vibrato with disabled Feedback/Dry-Wet; controls under transition: Mode, Rate, Amount and Feedback Invert. |
| Phaser-Flanger / REQ-MPL-PF-LIFECYCLE | Doubler with nonzero Feedback, enabled Env Fol with nonzero amount and LFO2 Mix interior; controls under transition: Mode, Envelope Amount, LFO2 Mix and sync rate. |
| Shifter / REQ-MPL-SH-LIFECYCLE | MIDI Pitch Mode with held source note, Pitch mode, Delay on and nonzero Feedback; controls under transition: Pitch Mode, Coarse, Delay sync and Wide/Spread. |
| Spectral Resonator / REQ-MPL-SR-LIFECYCLE | MIDI Poly 16 with gate active, held notes, active tuning, nonzero resonance and Granular mode; controls under transition: Polyphony, Use Current Scale, Quantize and Decay. |
| Spectral Time / REQ-MPL-ST-LIFECYCLE | Freezer On, Freeze active, Retrigger Envelope, overlapping freezes, Delay On and Frz > Dly; controls under transition: Freeze, processing order, interval units and Resolution. |
| Vocoder / REQ-MPL-VO-LIFECYCLE | External carrier from existing track, L/R mode, nonzero Unvoiced and active band levels; controls under transition: Carrier source, channel mode, Sens and band attenuation. |
| Beat Repeat / REQ-MPL-BR-LIFECYCLE | Repeat active with captured material, Gate output mode, nonzero Volume, Variation 0; controls under transition: Repeat, Interval/Offset, Chance and Variation mode. |
| Looper / REQ-MPL-LP-LIFECYCLE | owned loop A, completed overdub B, active overdub C, monitoring Never and Follow song tempo; controls under transition: Feedback, Reverse, Song Control and Quantization. |

Documented numeric endpoints are already present in the control cases; the
boundary cases add adjacent/invalid entries and clock/event boundaries without
asserting clamp/reject policy. Native local Looper Undo is distinct from global
Undo History. MIDI mode in Shifter or Spectral Resonator is not assigned Auto
Shift's no-notes silence rule. Spectral Time Freezer requires both section On
and Freeze; Delay's Dry/Wet is separate from global Dry/Wet. Pure control
eligibility cases (for example Vibrato-disabled Feedback) do not grade signal
invariance. Modulation/no-effect cases require the enabled/nonzero positive
conditions above and still leave their quantitative signal result unknown.

## Acceptance catalog

The [requirement view](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/requirements.json)
and [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/cases.json)
retain exact requirement-to-source-to-case links. All cases have `executed:false`;
all target expectations are null and target grades U. Only the documentary
control/state comparator can compare visible named fields; acoustic adjectives,
internal buffers or latent DSP state are not a reference comparator.

| Device | D12 / U requirements | Control / state / signal proposals | Additional U cases |
| --- | --- | --- | --- |
| Auto Pan-Tremolo | 10 / 1 | 6 / 0 / 4 | 9 |
| Auto Shift | 12 / 1 | 8 / 0 / 4 | 9 |
| Chorus-Ensemble | 8 / 1 | 5 / 0 / 3 | 9 |
| Phaser-Flanger | 9 / 1 | 4 / 0 / 5 | 9 |
| Shifter | 9 / 1 | 6 / 0 / 3 | 9 |
| Spectral Resonator | 9 / 1 | 5 / 0 / 4 | 9 |
| Spectral Time | 9 / 1 | 4 / 0 / 5 | 9 |
| Vocoder | 8 / 1 | 4 / 0 / 4 | 9 |
| Beat Repeat | 8 / 1 | 3 / 0 / 5 | 9 |
| Looper | 14 / 1 | 1 / 9 / 4 | 9 |

## Analyst evidence appendix

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/sources.json)
pins the external shared capture, schema/inventory and retained preset copies.
The [dependency ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/dependencies.json)
additionally pins the original capture catalog and reviewed spectral correction;
[reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/association-reconciliation.json)
identifies historical R1 spectral source IDs explicitly.
The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manifest-author-r1.json)
freezes payloads plus both canonical page snapshots for independent review.
These links are analysis-only and must be sanitized/reviewed before handoff.

- D12-AUDIO-EFFECTS: [official Version 12 chapter](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
  retained [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html),
  captured 2026-10-19, SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`.
  It supports documented prose, not pinned-patch behavior; figures were not separately inspected.
- PKG-SCHEMA: [12.0_12402 schema](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt),
  SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`;
  [class/field observations](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/schema-fields.json)
  prove storage vocabulary only.
- Ten shipped [preset observations](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/package-values.json)
  retain roots, fields, source paths and historical Creator metadata. No constructor/default/audio claim follows.
- The [bounded spectral folder ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/spectral-folder-observations.json)
  records eight Resonator `Transmute` presets and six Time `Spectral` presets plus
  fourteen excluded `._` sidecars; all bytes/paths are pinned. Discovery aliases
  are an artifact association, not proof that private names expose any particular control law.

| Device | Exact manual section / blocks | Retained paragraph/heading view |
| --- | --- | --- |
| Auto Pan-Tremolo | §29.3; `auto-pan-tremolo:B001–B020` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-auto-pan-tremolo-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-auto-pan-tremolo.txt) |
| Auto Shift | §29.4; `auto-shift:B001–B052` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-auto-shift-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-auto-shift.txt) |
| Chorus-Ensemble | §29.8; `chorus-ensemble:B001–B020` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-chorus-ensemble-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-chorus-ensemble.txt) |
| Phaser-Flanger | §29.29; `phaser-flanger:B001–B034` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-phaser-flanger-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-phaser-flanger.txt) |
| Shifter | §29.35; `shifter:B001–B036` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-shifter-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-shifter.txt) |
| Spectral Resonator | §29.36; `spectral-resonator:B001–B041` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-spectral-resonator-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-spectral-resonator.txt) |
| Spectral Time | §29.37; `spectral-time:B001–B033` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-spectral-time-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-spectral-time.txt) |
| Vocoder | §29.42; `vocoder:B001–B040` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-vocoder-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-vocoder.txt) |
| Beat Repeat | §29.5; `beat-repeat:B001–B012` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-beat-repeat-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-beat-repeat.txt) |
| Looper | §29.25; `looper:B001–B044` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-looper-blocks.json), [line-numbered text](../../analysis/ableton-live-12.4.3/full-spec-v1/modulation-pitch-loop/manual-looper.txt) |
