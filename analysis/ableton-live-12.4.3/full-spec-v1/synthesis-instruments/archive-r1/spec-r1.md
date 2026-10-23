---
id: SPEC-SYNTHESIS-INSTRUMENTS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary Live 12 behavior with exact-build applicability unknown
---

# Drift, Drum Sampler, Meld, Operator and Wavetable

## Scope and authority

This partial F-06 draft owns the five named current instrument profiles under
[the full-product inventory](../research/full-live-coverage-inventory.md).
It specifies documented controls, eligible routes, voices, envelope/modulation
roles and instrument-specific state. It does not establish complete profiles,
DSP equivalence or a released implementation input. The
[coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/synthesis-instruments.md) owns source interpretation.

**D12** means official Version 12 manual prose captured 2026-10-19.
**Every runtime clause has U exact-12.4.3 applicability.** Package schema and
shipped presets establish field/root presence only, never constructor defaults,
enum domains, control laws, DSP or loading behavior. No S/X execution or
candidate comparison is present. Named waveform/circuit/mode algorithms describe
public behavior, not a required private implementation. No unstated frequency,
FM, envelope, filter, interpolation, RNG, voice-stealing, CPU or tolerance law
is inferred. Figure contents were not separately inspected.

[Device racks](device-racks.md) owns insertion/bypass/common preset workflows and
Drum Rack pad context; [automation](automation-envelopes.md) owns its finite
storage/evaluation clauses, not these controls' eligibility/smoothing.
[Simpler](device-simpler.md) and [Sampler](device-sampler.md) own their receiving
instrument behavior. [MPE](mpe-workflows.md), [tuning](tuning-systems.md),
[MIDI notes](midi-note-storage.md), [transport](transport-state.md),
[media](media-file-workflows.md), [browser](browser-workflows.md) and
[persistence](live-set-structure.md) retain their bounded contracts. Links do
not establish composed behavior, source codec, global bend range, default tuning
or undocumented per-instrument support.

## Setup, state and grading

Use the [finite setups](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/stimulus-recipes.json) with isolated enabled
instruments, valid notes/media, enabled processing sections, nonzero amounts and
unmuted audible output. Every no-effect proposal needs an active paired positive
baseline; disabled engines, absent notes/samples, zero depth or muted output
cannot establish processing behavior. Tests reset held notes, routes and prior
histories between independent trials. Media recipes are future test inputs:
no rendered audio, MIDI captures, sample fixture or original execution is claimed.

The [requirement catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/requirements.json) and
[case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/cases.json) retain one finite case per documentary
requirement plus ten device-specific U lifecycle cases. Documentary control/state
comparators inspect named visible values, choices, eligibility or transitions.
Signal obligations have no numerical comparator. All exact-target `expected`
values and comparisons are null, all target grades U, all `executed:false`.
Documentary expectations are proposals for Version 12 prose, not 12.4.3 passes.

## Individual requirements

Every row below is D12/target-U. Evidence references resolve to exact retained
HTML paragraph/heading blocks, with HTML line and heading context, in the appendix.
Actions and preconditions are in the case with the same prefix/number.

### Drift

Current surface `SURF-DEVICE-DRIFT`; package association `Drift` / schema line 1737.

| Requirement | Documented contract and limits | Exact blocks |
| --- | --- | --- |
| REQ-SYN-DF-001 | Osc 1 offers Sine, Triangle, Shark Tooth, Saturated, Saw, Pulse and Rectangle; Osc 2 offers Sine, Triangle, Saturated, Saw and Rectangle. | `drift:B009`, `drift:B022` |
| REQ-SYN-DF-002 | Osc 1 Oct transposes octaves and Shape changes its waveform display; Osc 2 Oct transposes octaves and Detune uses semitones. Combined display includes enabled oscillator/noise output. | `drift:B010`, `drift:B023`, `drift:B028` |
| REQ-SYN-DF-003 | Osc 1 Shape sources are Env 1, Env 2/Cyc, LFO, Key, Velocity, Modwheel, Pressure and Slide. Shape Mod Amount spans -100% to 100%; positive Shape Mod can act even with Shape 0%. Key modulation reverses direction with amount sign. | `drift:B011`, `drift:B012`, `drift:B013`, `drift:B014`, `drift:B015`, `drift:B016`, `drift:B017`, `drift:B018`, `drift:B019`, `drift:B020` |
| REQ-SYN-DF-004 | Two pitch modulation sources affect both oscillators, each with amount -100% to 100%; Ratio-mode LFO pitch modulation is documented as able to produce FM tones. | `drift:B025`, `drift:B026` |
| REQ-SYN-DF-005 | Osc 1, Osc 2 and white-noise generator have independent enables/gains and individual filter-routing arrows. Routing off bypasses the filter for that source. | `drift:B030`, `drift:B031`, `drift:B033` |
| REQ-SYN-DF-006 | The manual describes oscillator gain -6 dB and saturation changes above 0 dB in the filter path; it supplies no transfer curve or measured thresholds for this build. | `drift:B032` |
| REQ-SYN-DF-007 | Oscillator R on resets both oscillator phases at each note; R off is free-running. | `drift:B034` |
| REQ-SYN-DF-008 | Low-pass Type I is labelled 12 dB/octave and Type II 24 dB/octave. Freq/Res and high-pass HP are separate; display dots adjust HP horizontally and LP frequency/resonance horizontally/vertically. Key 0.00 disables note influence on LP frequency; 1.00 follows note direction. | `drift:B038`, `drift:B041`, `drift:B042`, `drift:B043` |
| REQ-SYN-DF-009 | Two independent low-pass cutoff modulation slots each have amount -100% to 100%. | `drift:B044` |
| REQ-SYN-DF-010 | Envelope 1 controls amplitude of both oscillators and noise; Attack reaches peak, Decay reaches Sustain, Sustain holds until note ends, Release returns to zero. Knobs/display and 1/2 selectors edit the selected envelope. | `drift:B049`, `drift:B050`, `drift:B051`, `drift:B052`, `drift:B053`, `drift:B054`, `drift:B055` |
| REQ-SYN-DF-011 | Env 2 is a modulation source and can switch ADSR to Cycling; Cycling restarts on each MIDI note, offers Tilt/Hold and Rate/Ratio/Time/Sync using Hz/ratio/ms/beat divisions. | `drift:B057`, `drift:B058`, `drift:B059`, `drift:B060`, `drift:B061` |
| REQ-SYN-DF-012 | LFO time modes are Rate, Ratio, Time and Sync. Nine waveforms include Sine, Triangle, Saw Up/Down, Square, Sample & Hold, Wander, Linear Envelope and Exponential Envelope. R resets per note; off free-runs; Amount and its modulation source/depth control intensity. | `drift:B063`, `drift:B064`, `drift:B065`, `drift:B066`, `drift:B067`, `drift:B068`, `drift:B069`, `drift:B070`, `drift:B071`, `drift:B072`, `drift:B073`, `drift:B074`, `drift:B075` |
| REQ-SYN-DF-013 | Mod section has up to three source/destination slots with -100% to 100% amount. Sources are Env 1, Env 2/Cyc, LFO, Key, Velocity, Modwheel, Pressure, Slide; destinations include oscillator gains/shape/detune, Noise Gain, LP Frequency/Resonance, HP Frequency, LFO/Cyc rate and Main Volume. | `drift:B077`, `drift:B078`, `drift:B079`, `drift:B080` |
| REQ-SYN-DF-014 | Voice modes Poly, Mono, Stereo and Unison use respectively one, up to four, two and four voices per note. At Voices 32, Poly/Stereo/Unison permit 32/16/8 notes. Mono Thickness 0 uses one audible voice; new held-note onset chokes the previous note. | `drift:B083`, `drift:B084`, `drift:B085`, `drift:B086`, `drift:B087`, `drift:B088`, `drift:B089`, `drift:B090`, `drift:B091` |
| REQ-SYN-DF-015 | Drift changes per-voice oscillator and filter variation; no seed, distribution, repeatability or exact zero-variation law is supplied. | `drift:B092` |
| REQ-SYN-DF-016 | Mono Legato allows a new held-overlap note to change pitch without restarting envelopes; Glide sets overlapping-note pitch-slide time. | `drift:B093` |
| REQ-SYN-DF-017 | Volume and Vel > Vol control output/velocity; Transpose spans -48 to +48 semitones. Note PB toggles per-note pitch bend independently of global PB Range. | `drift:B094`, `drift:B095` |

**REQ-SYN-DF-LIFECYCLE — U:** the ten concrete obligations below remain required, ungraded behavior.

### Drum Sampler

Current surface `SURF-DEVICE-DRUM-SAMPLER`; package association `DrumCell` / schema line 1909.

| Requirement | Documented contract and limits | Exact blocks |
| --- | --- | --- |
| REQ-SYN-DS-001 | Browser double-click or waveform drag/drop loads a sample. Start and Length use percentages of total sample length; Shift-drag Start gives fine adjustment and waveform zoom. Start/Length/Gain update the display. | `drum-sampler:B005`, `drum-sampler:B006`, `drum-sampler:B007`, `drum-sampler:B009` |
| REQ-SYN-DS-002 | Sample Gain spans -70 to +24 dB, Transpose -48 to +48 semitones, Detune -50 to +50 cents, global Volume -36 to +36 dB. Pan changes stereo position and Velocity to Volume controls velocity response. | `drum-sampler:B008`, `drum-sampler:B014`, `drum-sampler:B041`, `drum-sampler:B042` |
| REQ-SYN-DS-003 | Trigger uses Attack/Hold/Decay and continues through Hold after note release; Hold inf plays the full sample. Gate disables Hold and starts Decay at note release. | `drum-sampler:B010`, `drum-sampler:B011`, `drum-sampler:B012`, `drum-sampler:B013`, `drum-sampler:B015` |
| REQ-SYN-DS-004 | Next/Previous Similar Sample cycle related samples; Show Similar Files opens browser results; Return to Reference returns to initial reference and Save as Similarity Reference replaces it. Waveform hot-swap replaces sample; title hot-swap replaces instrument. | `drum-sampler:B017`, `drum-sampler:B018`, `drum-sampler:B019` |
| REQ-SYN-DS-005 | Playback Effect On gates nine choices: Stretch, Loop, Pitch Env, Punch, 8-Bit, FM, Ring Mod, Sub Osc and Noise. Each has two controls; X/Y vertical edits first, horizontal second. | `drum-sampler:B021`, `drum-sampler:B022`, `drum-sampler:B023` |
| REQ-SYN-DS-006 | Stretch changes sample length without intended pitch change; Factor is a speed multiple and Grain Size uses milliseconds. Exact grain/window/interpolation law is unknown. | `drum-sampler:B024` |
| REQ-SYN-DS-007 | Loop repeats a sample region; Loop Offset is relative to sample start and Loop Length is milliseconds. | `drum-sampler:B025` |
| REQ-SYN-DS-008 | Pitch Env Amount -100% to +100% sets signed pitch change and Decay returns to base pitch defined by global controls. | `drum-sampler:B026` |
| REQ-SYN-DS-009 | Punch applies transient ducking; Amount controls reduction and Release controls return to zero gain reduction. Exact attack/envelope law is unknown. | `drum-sampler:B027` |
| REQ-SYN-DS-010 | 8-Bit offers Sample Rate and Decay Time for its low-pass behavior; no bit-depth/aliasing/kernel equivalence follows from the name. | `drum-sampler:B028` |
| REQ-SYN-DS-011 | FM modulates sample pitch with a sine; Ring Mod modulates amplitude with low-rate tremolo and higher-rate ring-modulation character. Both have Amount/Frequency and modulation decay follows global Decay. | `drum-sampler:B029`, `drum-sampler:B030`, `drum-sampler:B034` |
| REQ-SYN-DS-012 | Sub Osc and Noise layer a generator following device Attack/Decay. Sub Frequency spans 30-120 Hz; Noise Color filters noise. | `drum-sampler:B031`, `drum-sampler:B032` |
| REQ-SYN-DS-013 | Time/frequency controls of Stretch, Loop, FM, Ring Mod, Sub Osc and Noise follow global pitch and played MIDI pitch; exact scaling is not supplied. | `drum-sampler:B033` |
| REQ-SYN-DS-014 | Filter On gates four types: 12 dB LP, 24 dB LP, 24 dB HP and Peak. LP/HP expose Resonance/Frequency; Peak exposes Peak Gain/Frequency. | `drum-sampler:B036`, `drum-sampler:B037`, `drum-sampler:B038` |
| REQ-SYN-DS-015 | Mod source is Velocity or Slide (MPE); destinations are Filter, Attack, Hold, Decay, FX1 and FX2. FX1/FX2 address current effect controls; amount controls depth. | `drum-sampler:B043`, `drum-sampler:B044`, `drum-sampler:B045`, `drum-sampler:B046`, `drum-sampler:B047` |
| REQ-SYN-DS-016 | Enable Per-Note Pitch Bend is documented enabled by default. Envelope Follows Pitch scales envelope relative to sample pitch so it affects the same portion when transposed. | `drum-sampler:B050`, `drum-sampler:B051` |
| REQ-SYN-DS-017 | Drum Sampler > Simpler replaces the instrument retaining sample Start and Length positions; other parameter translations are not established. | `drum-sampler:B052` |
| REQ-SYN-DS-018 | Save as Default Pad from a Drum Rack pad context makes new samples on empty pads load Drum Sampler. | `drum-sampler:B053`, `drum-sampler:B054` |

**REQ-SYN-DS-LIFECYCLE — U:** the ten concrete obligations below remain required, ungraded behavior.

### Meld

Current surface `SURF-DEVICE-MELD`; package association `InstrumentMeld` / schema line 3374.

| Requirement | Documented contract and limits | Exact blocks |
| --- | --- | --- |
| REQ-SYN-ME-001 | Expanded View reveals all modulation sources/targets; A/B selects engine matrix, Copy to A/B copies modulation values and X clears active modulation values. | `meld:B005` |
| REQ-SYN-ME-002 | Engines A/B enable independently. Disabling an engine deactivates its filter; a filter can be disabled without disabling its engine. | `meld:B007`, `meld:B066` |
| REQ-SYN-ME-003 | Engine Octaves/Semitones/Cents pitch controls become scale-degree transposition when Use Current Scale follows Live Scale Mode; Pitch Quant target is included. | `meld:B008`, `meld:B096` |
| REQ-SYN-ME-004 | Oscillator macros depend on selected type: Basic Shapes Shape/Tone; Dual Basic Shapes Shape/Detune; Noisy Shapes Shape/Rough; Square Sync Freq 1/2; Square 5th 5th Amt/P Width; Sub Tone/Aux; four Swarms Motion/Spacing; Harmonic Fm Amount/Ratio; Fold Fm Amount/Shape; Squelch Amount/Feedback; Simple Fm Amount/Ratio; Chip Tone/Rate. Overview type count is unresolved. | `meld:B009`, `meld:B011`, `meld:B012`, `meld:B013`, `meld:B014`, `meld:B015`, `meld:B016`, `meld:B017`, `meld:B018`, `meld:B019`, `meld:B020`, `meld:B021`, `meld:B022`, `meld:B023` |
| REQ-SYN-ME-005 | Shepard’s Pi Rate 0.0-49.9 descends, 50.0 has no movement, 50.1-100.0 ascends; Width changes octave count. | `meld:B024` |
| REQ-SYN-ME-006 | Remaining described macros are Tarp Decay/Tone; Extratone Pitch/Env Amount; Noise Loop Rate/Fade; Filtered Noise Freq/Width; Bitgrunge Freq/Mult; Crackle Density/Intensity; Rain Tone/Rate; Bubble Density/Spread; Chord Shape/Inversion. Named descriptions do not prove kernels or RNG. | `meld:B025`, `meld:B026`, `meld:B027`, `meld:B028`, `meld:B029`, `meld:B030`, `meld:B031`, `meld:B032`, `meld:B033` |
| REQ-SYN-ME-007 | Chord uses four sawtooth oscillators with Shape intervals and Inversion order. With Use Current Scale, chords use selected scale; with no scale set, incoming root uses major. Availability/version/context remains unresolved. | `meld:B033` |
| REQ-SYN-ME-008 | Amp/Mod envelopes offer ADSR and slopes; Trigger plays all segments ignoring Sustain, Loop repeats entire envelope without holding Sustain, AD Loop repeats Attack/Decay. Mod envelope adds Initial/Peak/Final. | `meld:B035`, `meld:B036`, `meld:B037`, `meld:B038` |
| REQ-SYN-ME-009 | Link Envelopes links corresponding engine Amplitude and Modulation envelopes. | `meld:B039` |
| REQ-SYN-ME-010 | Each engine has LFO 1 and 2 with Hz/sync, Phase Offset and Retrigger. LFO 1 types are Basic Shapes, Ramp, Wander, Alternate, Euclid, Pulsate; FX1/2 each describe eighteen serial effects. LFO 1 and processed LFO1 FX are separate sources. LFO 2 offers Sine, Tri, Saw Up/Down, Rectangle, Random S&H. | `meld:B041`, `meld:B042`, `meld:B043`, `meld:B044` |
| REQ-SYN-ME-011 | Matrix source columns/target rows accept signed modulation. Clicking parameter adds it to selected engine matrix; unmodulated temporary row disappears on next selection. Additive/multiplicative target assignment and complete units remain U. | `meld:B046`, `meld:B047`, `meld:B048` |
| REQ-SYN-ME-012 | Velocity and Pitch sources use note values for that note duration; Random gets new value at note trigger. MIDI Pitch Bend/Press/Wheel and MPE Note Pitch Bend/Slide/Press supply sources, including clip envelopes. | `meld:B051`, `meld:B052`, `meld:B053`, `meld:B054` |
| REQ-SYN-ME-013 | Osc Key Tracking off produces C3 constant pitch, or scale root in C3 octave when scale mode active; on follows incoming note. | `meld:B057` |
| REQ-SYN-ME-014 | Phase Reset enables Phase Spread. With Reset on, Spread off sets start phase zero; Spread on follows Spread matrix source. | `meld:B058` |
| REQ-SYN-ME-015 | Oscillator Scale Awareness lists Dual Basic Shapes, Swarm Sine/Triangle/Saw/Square and Chip. Filter Scale Awareness lists Plate and Membrane Resonators. These per-engine settings are distinct from Use Current Scale. | `meld:B059`, `meld:B060`, `meld:B061` |
| REQ-SYN-ME-016 | Portamento slides continuously and Glissando in discrete steps, using scale degrees when scale awareness is on. Both Mono and Poly permit Glide, audible only with Glide Time above zero. | `meld:B062`, `meld:B063`, `meld:B064` |
| REQ-SYN-ME-017 | Filter types have Frequency and type-dependent macros. SVF 12/24 L-B-H-N morphs LP/BP/HP/notch; MS2 LP/HP, OSR BP, LP Crunch, LP Switched Res Lofi and Filther are described. Q emphasizes cutoff and Drive saturates input. | `meld:B067`, `meld:B068`, `meld:B069`, `meld:B070`, `meld:B071`, `meld:B072`, `meld:B073`, `meld:B074`, `meld:B075` |
| REQ-SYN-ME-018 | Eq Peak Boost/width and Eq Notch Cut/width, Phaser Feedback/Spread, Redux Crush/Lofi, Vowel Morph and Comb +/- Feedback/Damp have distinct roles. | `meld:B076`, `meld:B077`, `meld:B078`, `meld:B079`, `meld:B080` |
| REQ-SYN-ME-019 | Plate and Membrane Resonators describe first 32 modes of rectangular plate/circular membrane and scale-following resonant frequencies with Filter Scale Awareness. | `meld:B081`, `meld:B082` |
| REQ-SYN-ME-020 | Per-engine Volume/Pan and Tone Filter are separate; positive Tone reduces lows and negative Tone reduces highs. | `meld:B084`, `meld:B085` |
| REQ-SYN-ME-021 | Mixer Drive is per voice after engine mixer settings and before per-voice limiter; Limit gates limiter after both engines mixed and global Drive applied. Global Volume sets output. | `meld:B086`, `meld:B094`, `meld:B095` |
| REQ-SYN-ME-022 | Mono permits Legato: overlap with Legato on reuses current envelope position, off restarts envelope. Poly exposes 2-12 voices. | `meld:B089`, `meld:B090`, `meld:B091` |
| REQ-SYN-ME-023 | Stacked Voices duplicates both engines including filters/modulation/mix. Spread offsets stacked voices, or notes in held chord when Stacked Voices Off. Spread has no effect without a matrix target. | `meld:B092`, `meld:B093` |
| REQ-SYN-ME-024 | The matrix paragraph says negative values speed envelopes/LFOs and positive slow them, but the applicable target/preconditions are unspecified; do not generalize that statement to all destinations. | `meld:B047` |

**REQ-SYN-ME-LIFECYCLE — U:** the ten concrete obligations below remain required, ungraded behavior.

### Operator

Current surface `SURF-DEVICE-OPERATOR`; package association `Operator` / schema line 5640.

| Requirement | Documented contract and limits | Exact blocks |
| --- | --- | --- |
| REQ-SYN-OP-001 | Four oscillators use eleven predefined algorithms; icons describe top-to-bottom routing. Algorithm selector supports MIDI mapping, automation and real-time modulation. | `operator:B006`, `operator:B092` |
| REQ-SYN-OP-002 | Wave chooser includes sine, resynthesized saw/square/triangle variants, Sine 4/8 Bit, Saw D, Square D, Noise Looped, Noise White and User. Numeric harmonic names denote retained harmonic counts, not exact output samples. | `operator:B011`, `operator:B013` |
| REQ-SYN-OP-003 | Harmonics editor offers 16/32/64 partials, Shift constrains editing to one harmonic, Repeat off truncates above chosen count, even/odd/all drawing and Normalize; waveform copy/paste works across oscillators. | `operator:B014`, `operator:B015`, `operator:B016`, `operator:B018` |
| REQ-SYN-OP-004 | Waveform context exports .ams to User Library Samples/Waveforms; browser drag imports .ams into an oscillator; Simpler/Sampler are also documented consumers. | `operator:B017` |
| REQ-SYN-OP-005 | Osc Coarse/Fine set note-relative ratios; Fixed replaces controls with Frequency Hz and Multiplier and ignores note pitch, with described low endpoint 0.1 Hz. The manual states fixed frequency is Freq multiplied by Multi; no note-frequency formula is supplied. | `operator:B020`, `operator:B171`, `operator:B172`, `operator:B173`, `operator:B174`, `operator:B175` |
| REQ-SYN-OP-006 | Osc < Vel controls signed velocity pitch response; Q quantizes it as Coarse changes. | `operator:B021`, `operator:B184`, `operator:B185` |
| REQ-SYN-OP-007 | Each oscillator Level/envelope responds to Vel/Key; Phase and R control note-start phase/free-run. Feedback acts only on oscillators not modulated by another oscillator. | `operator:B022`, `operator:B023`, `operator:B024`, `operator:B180`, `operator:B181`, `operator:B182`, `operator:B187`, `operator:B188` |
| REQ-SYN-OP-008 | Antialias and Interpolation are independently selectable, Tone affects high-frequency content. Manual new-patch default Antialias on does not prove installed constructor/preset defaults or a numerical alias bound. | `operator:B026`, `operator:B090`, `operator:B095`, `operator:B096` |
| REQ-SYN-OP-009 | LFO routes Dest A to selected oscillators/filter and Dest B to one extra target; global Amount, Vel and envelope scale depths. Range Low describes 50 seconds-30 Hz, Hi 8 Hz-12 kHz and Sync tempo; R resets/free-runs; Rate < Key 100% doubles per octave. | `operator:B028`, `operator:B029`, `operator:B030`, `operator:B032`, `operator:B033`, `operator:B157`, `operator:B167` |
| REQ-SYN-OP-010 | Seven envelopes cover oscillators/filter/pitch/LFO; oscillator Attack is documented linear and Decay/Release exponential, ending -inf dB. Filter/pitch slopes and End vary. Note Off starts Release from current value. Shapes copy across oscillators. | `operator:B035`, `operator:B036`, `operator:B037`, `operator:B038`, `operator:B046`, `operator:B190`, `operator:B191`, `operator:B192`, `operator:B193`, `operator:B194`, `operator:B195`, `operator:B196`, `operator:B201` |
| REQ-SYN-OP-011 | Envelope modes include Loop, Beat, Sync and Trigger. Beat repeats note-relative without quantizing notes; Sync first repeat nearest sixteenth while song plays, otherwise Beat-like. Trigger ignores Note Off. Loop restart level is unresolved. | `operator:B039`, `operator:B040`, `operator:B042`, `operator:B197`, `operator:B198` |
| REQ-SYN-OP-012 | Loop restart wording differs: overview says current level to peak, Loop Time listing says sustain-to-initial then restart, Beat/Sync listing says current-to-peak. Applicability to the same mode/preconditions is unresolved. | `operator:B041`, `operator:B198`, `operator:B199` |
| REQ-SYN-OP-013 | Global Time, Time < Key and per-envelope Time < Vel scale envelope segments; Beat/Sync repetition beat-time is not changed by global Time or Time < Vel. | `operator:B043`, `operator:B089`, `operator:B097`, `operator:B200` |
| REQ-SYN-OP-014 | Pitch envelope can target A-D and LFO via Dest A and another Dest B; amount +100% follows levels and -100% inverts sign; envelope On gates it. | `operator:B044`, `operator:B045`, `operator:B126`, `operator:B127`, `operator:B133`, `operator:B134`, `operator:B135`, `operator:B136`, `operator:B137` |
| REQ-SYN-OP-015 | Filter types LP/HP/BP/notch/Morph offer 12/24 dB slopes. Clean/OSR apply all types; MS2/SMP/PRD LP/HP. Non-Clean LP/HP/BP expose Drive. Morph sweeps LP/BP/HP/notch and context snaps to named responses. | `operator:B050`, `operator:B051`, `operator:B052`, `operator:B053`, `operator:B054`, `operator:B055`, `operator:B056`, `operator:B057`, `operator:B058`, `operator:B059` |
| REQ-SYN-OP-016 | Filter Frequency responds to velocity/key/envelope/LFO; key 100% doubles per octave around C3. Play by Key sets Freq 466 Hz and Freq < Key 100%; this command is distinct from a global tuning formula. | `operator:B060`, `operator:B061`, `operator:B062`, `operator:B063`, `operator:B064`, `operator:B065`, `operator:B146`, `operator:B148` |
| REQ-SYN-OP-017 | Shaper chooser/Drive act on filtered path; Dry/Wet 0% bypasses shaper and shaper drive. | `operator:B066`, `operator:B151`, `operator:B152`, `operator:B153` |
| REQ-SYN-OP-018 | Voices supports up to 32; excess notes cut oldest notes. Voices 1 plays overlapping notes legato without retriggering envelopes. Global R retriggers an already enabled note rather than adding a voice. | `operator:B069`, `operator:B070`, `operator:B093`, `operator:B094` |
| REQ-SYN-OP-019 | Velocity, Key, Aftertouch, Pitch Bend and Mod Wheel each route to two targets with independent amounts; fixed Time < Key and PB Range coexist. Targets include Off, oscillator volume/crossfades/feedback/fixed pitch/FM Drive, filter controls, shaper, LFO, pitch envelope, Volume/Pan/Tone/Time; eligibility is target-specific. | `operator:B071`, `operator:B072`, `operator:B098`, `operator:B099`, `operator:B100`, `operator:B101`, `operator:B103`, `operator:B104`, `operator:B105`, `operator:B106`, `operator:B107`, `operator:B108`, `operator:B109`, `operator:B110`, `operator:B111`, `operator:B112`, `operator:B113`, `operator:B114`, `operator:B115`, `operator:B116`, `operator:B117`, `operator:B118`, `operator:B119`, `operator:B120`, `operator:B121`, `operator:B122`, `operator:B123`, `operator:B124` |
| REQ-SYN-OP-020 | Glide is polyphonic, starts new note at prior-note pitch then slides; legato Glide does not retrigger envelopes; Glide Time has no effect if Glide off. | `operator:B074`, `operator:B131`, `operator:B132` |
| REQ-SYN-OP-021 | Spread uses two detuned voices per note panned L/R; whether a note uses Spread is determined at Note On. | `operator:B075`, `operator:B076`, `operator:B128` |
| REQ-SYN-OP-022 | Transpose changes already-playing notes. Context commands copy oscillator parameters, set all envelope levels to maximum/minimum/middle, edit harmonics and export .ams. | `operator:B129`, `operator:B207`, `operator:B208`, `operator:B209`, `operator:B210` |
| REQ-SYN-OP-023 | Enable Per-Note Pitch Bend is documented on by default and can be disabled in device-title context. | `operator:B211` |

**REQ-SYN-OP-LIFECYCLE — U:** the ten concrete obligations below remain required, ungraded behavior.

### Wavetable

Current surface `SURF-DEVICE-WAVETABLE`; package association `InstrumentVector` / schema line 3532.

| Requirement | Documented contract and limits | Exact blocks |
| --- | --- | --- |
| REQ-SYN-WT-001 | Two oscillators enable independently; tabs select editing, expanded view redistributes controls. Gain/Pan/Semi/Detune are per oscillator. Category/table choosers and arrows traverse category boundaries. | `wavetable:B003`, `wavetable:B008`, `wavetable:B009`, `wavetable:B010` |
| REQ-SYN-WT-002 | Dropping WAV/AIFF on visualization imports it; choosers/arrows then browse its folder. Raw bypasses automatic sample preprocessing. | `wavetable:B011`, `wavetable:B012` |
| REQ-SYN-WT-003 | Dragging visualization or Wave Position selects table position. Linear/polar show same data with distinct layouts. | `wavetable:B013`, `wavetable:B014` |
| REQ-SYN-WT-004 | Oscillator effects are FM (Amt/Tune), Classic (PW/Sync), Modern (Warp/Fold). Two effect values persist across effect-type changes. FM Tune +/-50% and +/-100% describe +/-1 and +/-2 octave modulator offsets. | `wavetable:B015`, `wavetable:B016`, `wavetable:B017`, `wavetable:B018`, `wavetable:B019` |
| REQ-SYN-WT-005 | Sub enables independently with Gain, Tone 0% sine/increasing harmonics, and one/two octave-down switches relative to note/global Transpose. | `wavetable:B021`, `wavetable:B022`, `wavetable:B023` |
| REQ-SYN-WT-006 | Each filter offers LP/HP/BP/notch/Morph, 12/24 dB slopes; Clean/OSR all types and MS2/SMP/PRD LP/HP. Non-Clean LP/HP/BP expose Drive. Display dots adjust Frequency/Resonance; Morph traverses LP/BP/HP/notch. | `wavetable:B026`, `wavetable:B027`, `wavetable:B028`, `wavetable:B029`, `wavetable:B030`, `wavetable:B031`, `wavetable:B032`, `wavetable:B033`, `wavetable:B034` |
| REQ-SYN-WT-007 | Serial sends mains through Filter 1 then 2; Parallel feeds mains to both; Split assigns Osc 1/2 to Filter 1/2 and halves Sub to both. Split leaves corresponding oscillator audible when its filter is off. | `wavetable:B035`, `wavetable:B036`, `wavetable:B037`, `wavetable:B038` |
| REQ-SYN-WT-008 | Matrix uses source columns/target rows. Additive values sum then add to parameter, neutral 0; multiplicative values multiply then multiply parameter, neutral 1 minimum 0. Source units, depth scaling, clamps and each target assignment remain unresolved except explicit labels. | `wavetable:B040`, `wavetable:B041`, `wavetable:B042`, `wavetable:B043`, `wavetable:B044`, `wavetable:B045`, `wavetable:B046`, `wavetable:B047`, `wavetable:B048`, `wavetable:B049`, `wavetable:B050` |
| REQ-SYN-WT-009 | Clicked parameter appears temporarily; nonzero modulation keeps its row, otherwise next selected parameter replaces it. Matrix and MIDI tabs share rows; source headers jump to source panels. | `wavetable:B051`, `wavetable:B052`, `wavetable:B089` |
| REQ-SYN-WT-010 | Time scales all modulator times, negative faster/positive slower. A modulator assigned to Time does not scale itself through that route but still scales other destinations. | `wavetable:B053` |
| REQ-SYN-WT-011 | Global Matrix Amount, LFO Amount, instrument Volume and Unison Amount are documented multiplicative destinations. | `wavetable:B054`, `wavetable:B079`, `wavetable:B093`, `wavetable:B105` |
| REQ-SYN-WT-012 | Amp, Env2 and Env3 have Time/Slope; Env2/3 also Initial/Peak/Final, absent on Amp. Positive slopes start fast then slow; negative slow then fast; zero linear. Sustain/Initial are documented multiplicative where present. | `wavetable:B058`, `wavetable:B059`, `wavetable:B060`, `wavetable:B061`, `wavetable:B062`, `wavetable:B063`, `wavetable:B064`, `wavetable:B065`, `wavetable:B066` |
| REQ-SYN-WT-013 | Envelope None holds Sustain until Note Off; Trigger plays all segments at Note On; Loop repeats whole envelope without Sustain hold until voice ends. | `wavetable:B061`, `wavetable:B067`, `wavetable:B068`, `wavetable:B069`, `wavetable:B070` |
| REQ-SYN-WT-014 | Two LFOs offer Sine, Saw, Triangle, Square and Random with waveform-dependent Shape. Sync switches rate Hz/beat divisions. | `wavetable:B072`, `wavetable:B073`, `wavetable:B074`, `wavetable:B075`, `wavetable:B076`, `wavetable:B077`, `wavetable:B078` |
| REQ-SYN-WT-015 | LFO Offset sets start phase and cannot be modulated; Attack fades in after Note On; Retrigger resets phase on each new note. | `wavetable:B080`, `wavetable:B081`, `wavetable:B082` |
| REQ-SYN-WT-016 | MIDI Velocity/Note apply through note duration; Note 100% Filter Frequency tracks pitch around C3. Pitch Bend/Aftertouch/Wheel can use clip envelopes; Random samples at each new note. | `wavetable:B085`, `wavetable:B086`, `wavetable:B087`, `wavetable:B088` |
| REQ-SYN-WT-017 | Transpose uses semitones; Mono is single voice with legato envelopes and permits Glide; Poly enables Poly Voices and disables Glide. | `wavetable:B092`, `wavetable:B094`, `wavetable:B095`, `wavetable:B096` |
| REQ-SYN-WT-018 | Unison choices are none, Classic, Shimmer, Noise, Phase Sync, Position spread and Random note. They differ in detune, phase reset, stereo and position/randomization roles. | `wavetable:B097`, `wavetable:B098`, `wavetable:B099`, `wavetable:B100`, `wavetable:B101`, `wavetable:B102`, `wavetable:B103` |
| REQ-SYN-WT-019 | Unison Voices controls oscillators per main wavetable oscillator; Amount is mode-dependent intensity, distinct from Poly Voices note count. | `wavetable:B104`, `wavetable:B105` |
| REQ-SYN-WT-020 | Hi-Quality context switch controls quality; off is documented modulation every 32 samples and lower-power filters. CPU saving up to 25% is a conditional manual claim, not a required timing benchmark. | `wavetable:B107`, `wavetable:B108`, `wavetable:B109` |
| REQ-SYN-WT-021 | As of Live 11.1 the manual describes Hi-Quality off for new/Core Library instances while earlier user presets/Sets retain on for consistency; enabling may produce subtle differences. Migration boundaries for this target are unresolved. | `wavetable:B110`, `wavetable:B111` |
| REQ-SYN-WT-022 | Manual claims unmodulated raw oscillator output is band-limited with no aliasing at any pitch. No spectral measurement definition, finite pitch-domain fixture or tolerance accompanies this claim. | `wavetable:B007` |

**REQ-SYN-WT-LIFECYCLE — U:** the ten concrete obligations below remain required, ungraded behavior.

## Lifecycle, boundaries and errors

Each device has distinct `SYN-<prefix>-U-<suffix>` cases for BOUNDARY, AUTOMATION,
TRANSPORT, PERSISTENCE, UNDO, MALFORMED, CANCEL, TEARDOWN, SAMPLE-RATE and
TUNING-MPE. These are not inapplicable omissions: all expected outcomes are U.
Numeric endpoint inspection in D12 cases does not prove adjacent-value handling,
clamping, normalization or rounding. Rate/block choices are analyst stimuli, not
supported device limits. Malformed loads operate only on disposable test copies.

| Device / prefix | Concrete state for all ten lifecycle cases |
| --- | --- |
| Drift / DF | Mono Legato on, Thickness interior, nonzero Glide, Cycling Env2 -> Osc1 Shape and LFO -> cutoff with nonzero depths; oscillator/filter routing active; Note PB on. |
| Drum Sampler / DS | Owned sample A Start 25% Length 50%, Gate envelope, active Loop playback effect and filter, Slide -> FX1 nonzero; separately Trigger Hold inf. |
| Meld / ME | A/B engines and filters on, nonzero cross-engine modulation, linked envelopes, stacked voices enabled with Spread -> Pan nonzero, Glide nonzero, Use Current Scale on. |
| Operator / OP | A carrier/B modulator active in retained algorithm, nonzero B level/envelope, LFO/pitch envelope routes active, Loop envelope, Voices 2, nonzero Spread/Glide. |
| Wavetable / WT | Owned imported wavetable A with Raw off, both main oscillators active, Split filters, Env2/LFO1 routes nonzero, Loop envelope, Poly Voices set, Unison Classic nonzero. |

Lifecycle actions include endpoints/out-of-range text and excess voices;
manual versus automated changes/re-enable; stop/seek/restart with sync and held
notes; save/reopen/preset/media relocation; three undo/redo edits; truncated
media/invalid saved control; preview/dialog cancellation; removal/Set close/source
disconnection during notes/releases; 44.1/48/96 kHz and 64/256-frame changes; and
two-note expression plus identified non-12-tone tuning. Their cases retain
specific actions and missing-result explanations. Common presets, stored tags,
control visibility or generic global contracts do not settle any of them.

## Acceptance catalog and scope gaps

| Instrument | D12 requirements | U requirements | Cases | Control / state / signal proposals |
| --- | --- | --- | --- | --- |
| Drift | 17 | 1 | 27 | 9 / 0 / 8 |
| Drum Sampler | 18 | 1 | 28 | 4 / 4 / 10 |
| Meld | 24 | 1 | 34 | 10 / 4 / 10 |
| Operator | 23 | 1 | 33 | 10 / 4 / 9 |
| Wavetable | 22 | 1 | 32 | 9 / 4 / 9 |

Total: **109 requirements** (104 D12, 5 U), **154 unexecuted cases**. Exact-target graded cases: **0**.

Exact DSP, tuning, randomization/seed, phase, envelope curves/timing, filters,
modulation scaling/clamping, polyphony interactions, import/AMS codecs,
automation/persistence/history/cancellation/errors, UI accessibility, load/CPU
and complete factory content remain uncovered or partial. No profile is complete.
Operator's documented oldest-note policy does not assign the same policy to other
instruments. Wavetable Unison Voices is not Poly Voices; Drift voice budget is not
note count; Meld's Spread requires a routed target. Drum Sampler Hold inf/Trigger
is distinct from Gate. Global pitch bend is distinct from per-note bend.

## Open source questions

- **SYN-U-OP-LOOP:** Operator §31.9.4 and parameter list §§31.9.10.7 use different
  restart descriptions. Preserve `operator:B039–B041`, `B197–B199`; Loop versus
  Beat/Sync and return-to-initial phases may differ. Until identical mode and
  preconditions are established, neither contradiction nor a selected restart
  law is asserted. Signal case SYN-OP-012 remains U.
- **SYN-U-ME-TYPES:** Meld `meld:B009` says twenty-four oscillator types; the macro
  paragraphs `B012–B033` describe twenty-five names when four Swarms and Chord
  are counted. Current manual revision/context may differ. Neither 24 nor 25 is
  an exact-build menu requirement. Chord scale behavior remains documentary only.
- **SYN-U-ME-TIME:** `meld:B047` sign wording does not identify its target/unit;
  no universal sign law is inferred. Case SYN-ME-024 is an ungraded obligation.
- Target-version parity, all required lifecycle outcomes and the numerical signal
  criteria remain open. These local IDs allow root to link canonical questions
  without silently closing them.

## Analyst evidence appendix

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/sources.json) pins the shared manual/schema and
five retained presets. The [block views](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-locators.json) retain
source lines and heading context. The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manifest-author-r1.json)
freezes the exact packet and canonical page snapshots for separate review.
These analysis links must be sanitized before a handoff.

- Official [Version 12 instrument chapter](https://www.ableton.com/en/live-manual/12/live-instrument-reference/),
  captured 2026-10-19T20:27:58.247940+00:00, retained in
  [sample-instruments](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-instruments-2026-10-19.html),
  SHA-256 `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`.
  Live 12 is known; patch-level applicability is unknown.
- Schema `12.0_12402` from pinned 12.4.3, retained in
  [sample-instruments](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/12.0_12402.txt),
  SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
  [Field observations](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/schema-fields.json) establish vocabulary only.
- Five preset copies and decoded XML retain `Creator: Ableton Live 12.4d1`,
  revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`, schema `12.0_12402`.
  Their inclusion in 12.4.3 is observed; that metadata is not a 12.4.3 runtime
  default or migration test. Exact file hashes are in the ledger.

| Device | Manual section / block range | Retained view |
| --- | --- | --- |
| Drift | §31.3; `drift:B001–B095` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drift-blocks.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drift.txt) |
| Drum Sampler | §31.4; `drum-sampler:B001–B054` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drum-sampler-blocks.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-drum-sampler.txt) |
| Meld | §31.8; `meld:B001–B096` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-meld-blocks.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-meld.txt) |
| Operator | §31.9; `operator:B001–B211` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-operator-blocks.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-operator.txt) |
| Wavetable | §31.13; `wavetable:B001–B111` | [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-wavetable-blocks.json), [text](../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/manual-wavetable.txt) |

## Revision and handoff

Revision 1 is an author-frozen partial draft awaiting separate analyst review.
No handoff is published and no existing release is expanded by this page.
