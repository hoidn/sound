"""Finite analyst draft and case catalog; no product code or reference execution."""
from pathlib import Path
from collections import Counter
import json
import re

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
DEVICES = [('drift', 'DF', 'Drift', 'Drift'), ('drum-sampler', 'DS', 'Drum Sampler', 'DrumCell'), ('meld', 'ME', 'Meld', 'InstrumentMeld'), ('operator', 'OP', 'Operator', 'Operator'), ('wavetable', 'WT', 'Wavetable', 'InstrumentVector')]
requirements, cases = [], []

def write(name, value):
    (P / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def add(slug, blocks, kind, contract, action):
    device = next(d for d in DEVICES if d[0] == slug)
    prefix, name = device[1:3]
    number = 1 + sum(r['device'] == name for r in requirements)
    rid = f'REQ-SYN-{prefix}-{number:03d}'
    lookup = {b['locator']: b for b in json.loads((P / f'manual-{slug}-blocks.json').read_text())}
    refs = [f'{slug}:B{n:03d}' for n in blocks]
    assert all(b in lookup for b in refs)
    requirements.append({'id': rid, 'device': name, 'provenance': 'D12', 'target_applicability': 'U', 'contract': contract, 'source_id': 'SAMPLE-INSTRUMENTS-MANUAL', 'source_blocks': refs, 'html_lines': sorted({lookup[b]['html_line'] for b in refs})})
    cases.append({'id': f'SYN-{prefix}-{number:03d}', 'requirements': [rid], 'device': name, 'kind': kind, 'preconditions': ['common-setup', 'positive-signal-guard'], 'setup_and_action': action, 'documentary_expected': contract, 'documentary_comparator': None if kind == 'signal-obligation' else 'Compare only named visible controls, units, choices, eligibility or explicit state transitions. No waveform, hidden-state, timing tolerance or DSP assertion.', 'expected': None, 'target_grade': 'U', 'comparison': None, 'executed': False, 'source_blocks': refs, 'fixture': f'stimulus-recipes.json#{prefix}'})

def rows(slug, data):
    for blocks, kind, contract, action in data:
        add(slug, blocks, kind, contract, action)

rows('drift', [
([9,22], 'documented-control', 'Osc 1 offers Sine, Triangle, Shark Tooth, Saturated, Saw, Pulse and Rectangle; Osc 2 offers Sine, Triangle, Saturated, Saw and Rectangle.', 'Open each oscillator chooser and select every listed waveform; do not equate similarly named waveforms across instruments.'),
([10,23,28], 'documented-control', 'Osc 1 Oct transposes octaves and Shape changes its waveform display; Osc 2 Oct transposes octaves and Detune uses semitones. Combined display includes enabled oscillator/noise output.', 'Solo Osc 1, move Shape 0 to 50 to 100%, then enable Osc 2 and vary its Detune; inspect named controls and display response, without waveform equality.'),
(list(range(11,21)), 'signal-obligation', 'Osc 1 Shape sources are Env 1, Env 2/Cyc, LFO, Key, Velocity, Modwheel, Pressure and Slide. Shape Mod Amount spans -100% to 100%; positive Shape Mod can act even with Shape 0%. Key modulation reverses direction with amount sign.', 'Shape 0%, Osc 1 enabled and audible, select LFO with rate 2 Hz and nonzero amount; compare Shape Mod 0%, +50%, -50%, then hold distinct notes for Key with each sign. Quantitative response remains U.'),
([25,26], 'documented-control', 'Two pitch modulation sources affect both oscillators, each with amount -100% to 100%; Ratio-mode LFO pitch modulation is documented as able to produce FM tones.', 'Open both Pitch Mod source menus and set LFO and Env 2, amounts +25% and -25%; select LFO Ratio. Check controls only; exact FM law remains U.'),
([30,31,33], 'signal-obligation', 'Osc 1, Osc 2 and white-noise generator have independent enables/gains and individual filter-routing arrows. Routing off bypasses the filter for that source.', 'Solo Osc 1, enable filter routing and low-pass cutoff 500 Hz; move cutoff 500 to 2000 Hz, then route Osc 1 around filter and repeat. Keep output audible; no numerical bypass equivalence is asserted.'),
([32], 'signal-obligation', 'The manual describes oscillator gain -6 dB and saturation changes above 0 dB in the filter path; it supplies no transfer curve or measured thresholds for this build.', 'Filter routing on, Osc 1 Saw audible; compare -12, -6, 0 and +6 dB oscillator gain with fixed filter settings and output attenuation. Measure future distortion rather than assigning a transfer curve.'),
([34], 'signal-obligation', 'Oscillator R on resets both oscillator phases at each note; R off is free-running.', 'Play separated identical notes with Osc 1/2 enabled, no modulation and Drift minimized; compare R on/off. Exact phase, seed and waveform comparator remain U.'),
([38,41,42,43], 'documented-control', 'Low-pass Type I is labelled 12 dB/octave and Type II 24 dB/octave. Freq/Res and high-pass HP are separate; display dots adjust HP horizontally and LP frequency/resonance horizontally/vertically. Key 0.00 disables note influence on LP frequency; 1.00 follows note direction.', 'Select both Types; drag each filter dot and inspect corresponding controls; set Key 0.00 then 1.00 while playing low/high notes. Grade controls only, not filter response.'),
([44], 'documented-control', 'Two independent low-pass cutoff modulation slots each have amount -100% to 100%.', 'Choose LFO and Env 2 for the two Freq Mod slots; enter -100%, 0% and +100% and inspect displayed values.'),
([49,50,51,52,53,54,55], 'signal-obligation', 'Envelope 1 controls amplitude of both oscillators and noise; Attack reaches peak, Decay reaches Sustain, Sustain holds until note ends, Release returns to zero. Knobs/display and 1/2 selectors edit the selected envelope.', 'Audible oscillator, nonzero Sustain and Release; send note on at beat 1 and off at beat 3, then edit envelope via display and knobs. Capture future stage behavior without invented curve/tolerance.'),
([57,58,59,60,61], 'documented-control', 'Env 2 is a modulation source and can switch ADSR to Cycling; Cycling restarts on each MIDI note, offers Tilt/Hold and Rate/Ratio/Time/Sync using Hz/ratio/ms/beat divisions.', 'Route Env 2 to Osc 1 Shape with nonzero amount; switch ADSR/Cycling and each time mode, adjust Tilt/Hold, send separated notes. Compare visible modes/units only.'),
(list(range(63,76)), 'documented-control', 'LFO time modes are Rate, Ratio, Time and Sync. Nine waveforms include Sine, Triangle, Saw Up/Down, Square, Sample & Hold, Wander, Linear Envelope and Exponential Envelope. R resets per note; off free-runs; Amount and its modulation source/depth control intensity.', 'Enumerate all nine LFO waves and four time modes, select R on/off, route LFO to Shape with +25%, adjust LFO Amount. No random distribution or one-shot curve is graded.'),
([77,78,79,80], 'documented-control', 'Mod section has up to three source/destination slots with -100% to 100% amount. Sources are Env 1, Env 2/Cyc, LFO, Key, Velocity, Modwheel, Pressure, Slide; destinations include oscillator gains/shape/detune, Noise Gain, LP Frequency/Resonance, HP Frequency, LFO/Cyc rate and Main Volume.', 'Fill three slots with LFO->Osc 1 Shape, Velocity->LP Frequency and Slide->Main Volume; inspect menus and amounts, exercise each source independently.'),
([83,84,85,86,87,88,89,90,91], 'signal-obligation', 'Voice modes Poly, Mono, Stereo and Unison use respectively one, up to four, two and four voices per note. At Voices 32, Poly/Stereo/Unison permit 32/16/8 notes. Mono Thickness 0 uses one audible voice; new held-note onset chokes the previous note.', 'At Voices 32 hold respectively 33/17/9 distinct notes in Poly/Stereo/Unison; separately compare Mono Thickness 0/50 and two overlapping notes. Capture voice loss/identity as U; do not assume a stealing order.'),
([92], 'signal-obligation', 'Drift changes per-voice oscillator and filter variation; no seed, distribution, repeatability or exact zero-variation law is supplied.', 'Use fixed audible patch, repeat eight same notes at Drift minimum/interior/maximum, then repeat a held chord. Retain future distributions; do not demand bit equality.'),
([93], 'signal-obligation', 'Mono Legato allows a new held-overlap note to change pitch without restarting envelopes; Glide sets overlapping-note pitch-slide time.', 'Mono, audible sustain, Legato off/on, Glide above zero; compare two overlapping notes with separated notes as a control.'),
([94,95], 'documented-control', 'Volume and Vel > Vol control output/velocity; Transpose spans -48 to +48 semitones. Note PB toggles per-note pitch bend independently of global PB Range.', 'Inspect Transpose -48/0/+48; send equal-pitch notes at velocities 32/96 with nonzero Vel > Vol; send per-note bend on one of two held notes with Note PB off/on, then global bend. Grade labels/state only; per-note sound isolation remains U.')])

rows('drum-sampler', [
([5,6,7,9], 'documented-state', 'Browser double-click or waveform drag/drop loads a sample. Start and Length use percentages of total sample length; Shift-drag Start gives fine adjustment and waveform zoom. Start/Length/Gain update the display.', 'Load owned sample A by drag/drop, then B by browser double-click; set Start 25%, Length 50%, Shift-drag Start and inspect waveform. Actual double-click focus/routing preconditions must be retained.'),
([8,14,41,42], 'documented-control', 'Sample Gain spans -70 to +24 dB, Transpose -48 to +48 semitones, Detune -50 to +50 cents, global Volume -36 to +36 dB. Pan changes stereo position and Velocity to Volume controls velocity response.', 'Inspect all named endpoints and zero; play velocities 32 and 96 with nonzero Velocity to Volume, keeping sample/global gains distinct.'),
([10,11,12,13,15], 'signal-obligation', 'Trigger uses Attack/Hold/Decay and continues through Hold after note release; Hold inf plays the full sample. Gate disables Hold and starts Decay at note release.', 'Sample A, start 0%, full length, effect/filter off; compare short and long notes in Trigger with finite Hold and inf, then Gate with same Attack/Decay. Check Hold eligibility separately; stage/timing output remains U.'),
([17,18,19], 'documented-state', 'Next/Previous Similar Sample cycle related samples; Show Similar Files opens browser results; Return to Reference returns to initial reference and Save as Similarity Reference replaces it. Waveform hot-swap replaces sample; title hot-swap replaces instrument.', 'Use retained sample A and a browser corpus with identified related files; next, previous, Return to Reference, choose B and Save as Similarity Reference, return again. Missing similarity-result ordering remains U; do not invent search matches.'),
([21,22,23], 'documented-control', 'Playback Effect On gates nine choices: Stretch, Loop, Pitch Env, Punch, 8-Bit, FM, Ring Mod, Sub Osc and Noise. Each has two controls; X/Y vertical edits first, horizontal second.', 'Enumerate nine effects with section enabled; for each drag X/Y vertically then horizontally and inspect named controls; compare section disabled eligibility.'),
([24], 'signal-obligation', 'Stretch changes sample length without intended pitch change; Factor is a speed multiple and Grain Size uses milliseconds. Exact grain/window/interpolation law is unknown.', 'Sample A, effect On Stretch, nontrivial Factor 2 and Grain Size 20 ms, compare Factor 1; retain future duration/pitch evidence without tolerance.'),
([25], 'signal-obligation', 'Loop repeats a sample region; Loop Offset is relative to sample start and Loop Length is milliseconds.', 'Sample A, Start 25%, effect On Loop with nonzero Offset and 50 ms Length; compare changed Start and Offset independently during a long Trigger Hold.'),
([26], 'signal-obligation', 'Pitch Env Amount -100% to +100% sets signed pitch change and Decay returns to base pitch defined by global controls.', 'Sample A, effect On Pitch Env, global Transpose +12 st; compare Amount -50/0/+50% with nonzero Pitch Envelope Decay and enough Hold to hear return.'),
([27], 'signal-obligation', 'Punch applies transient ducking; Amount controls reduction and Release controls return to zero gain reduction. Exact attack/envelope law is unknown.', 'Sample A transient, effect On Punch, compare nonzero Amount with zero, two nonzero Releases and audible unmuted output.'),
([28], 'signal-obligation', '8-Bit offers Sample Rate and Decay Time for its low-pass behavior; no bit-depth/aliasing/kernel equivalence follows from the name.', 'Sample A, effect On 8-Bit, compare two distinct nonzero Sample Rate and Decay Time settings, retaining actual displayed values before any output measurement.'),
([29,30,34], 'signal-obligation', 'FM modulates sample pitch with a sine; Ring Mod modulates amplitude with low-rate tremolo and higher-rate ring-modulation character. Both have Amount/Frequency and modulation decay follows global Decay.', 'Sample A, effects On; separately FM then Ring Mod, nonzero Amount/Frequency, compare short and long global Decay using notes long enough for both. No FM or ring multiplication formula is assigned.'),
([31,32], 'signal-obligation', 'Sub Osc and Noise layer a generator following device Attack/Decay. Sub Frequency spans 30-120 Hz; Noise Color filters noise.', 'Sample A, effect On Sub Osc with nonzero Amount, inspect 30/120 Hz; repeat Noise with nonzero Amount and low/high Color, change Attack/Decay in each.'),
([33], 'signal-obligation', 'Time/frequency controls of Stretch, Loop, FM, Ring Mod, Sub Osc and Noise follow global pitch and played MIDI pitch; exact scaling is not supplied.', 'For each of these six enabled effects with nonzero audible effect settings, compare MIDI 48/60/72 and Transpose 0/+12 while keeping other parameters fixed; do not assume a mathematical scaling law.'),
([36,37,38], 'documented-control', 'Filter On gates four types: 12 dB LP, 24 dB LP, 24 dB HP and Peak. LP/HP expose Resonance/Frequency; Peak exposes Peak Gain/Frequency.', 'Select all four filter types with sample playing and Filter On; inspect named controls, then disable filter. Numerical responses remain U.'),
([43,44,45,46,47], 'documented-control', 'Mod source is Velocity or Slide (MPE); destinations are Filter, Attack, Hold, Decay, FX1 and FX2. FX1/FX2 address current effect controls; amount controls depth.', 'Enable filter and selected effect, choose each destination with nonzero amount; change Velocity/Slide independently; change effect type while targeting FX1/2 and inspect target identity.'),
([50,51], 'signal-obligation', 'Enable Per-Note Pitch Bend is documented enabled by default. Envelope Follows Pitch scales envelope relative to sample pitch so it affects the same portion when transposed.', 'Fresh documented instance versus retained preset are separate setups; inspect context toggles, compare per-note bend off/on and Envelope Follows Pitch off/on at MIDI 48/72. Constructor default and acoustic equality for 12.4.3 remain U.'),
([52], 'documented-state', 'Drum Sampler > Simpler replaces the instrument retaining sample Start and Length positions; other parameter translations are not established.', 'Sample A Start 25% Length 50%, invoke conversion in disposable Set; inspect sample identity and these two positions only; preserve other differences as U.'),
([53,54], 'documented-state', 'Save as Default Pad from a Drum Rack pad context makes new samples on empty pads load Drum Sampler.', 'In test-owned Drum Rack save default pad, drop sample A onto empty pad, inspect instrument; restore test preference afterward. Existing filled-pad replacement policy is U.')])

rows('meld', [
([5], 'documented-state', 'Expanded View reveals all modulation sources/targets; A/B selects engine matrix, Copy to A/B copies modulation values and X clears active modulation values.', 'Assign one nonzero A route and a distinct B route; expand, Copy A to B, inspect values, then X in selected B. Scope of unrelated engine state remains U.'),
([7,66], 'documented-state', 'Engines A/B enable independently. Disabling an engine deactivates its filter; a filter can be disabled without disabling its engine.', 'Enable both engines and both filters; disable A then restore, disable Filter A while A remains on; inspect toggles and audible positive baseline.'),
([8,96], 'documented-control', 'Engine Octaves/Semitones/Cents pitch controls become scale-degree transposition when Use Current Scale follows Live Scale Mode; Pitch Quant target is included.', 'Use nonchromatic C major then D minor scale with Use Current Scale off/on; inspect st/sd and Pitch Quant target with nonzero route. Exact tuned output remains U.'),
([9,11,12,13,14,15,16,17,18,19,20,21,22,23], 'documented-control', 'Oscillator macros depend on selected type: Basic Shapes Shape/Tone; Dual Basic Shapes Shape/Detune; Noisy Shapes Shape/Rough; Square Sync Freq 1/2; Square 5th 5th Amt/P Width; Sub Tone/Aux; four Swarms Motion/Spacing; Harmonic Fm Amount/Ratio; Fold Fm Amount/Shape; Squelch Amount/Feedback; Simple Fm Amount/Ratio; Chip Tone/Rate. Overview type count is unresolved.', 'For A then B, select each named type and inspect its two macro labels. Do not assert an exact menu count from the overview.'),
([24], 'signal-obligation', 'Shepard’s Pi Rate 0.0-49.9 descends, 50.0 has no movement, 50.1-100.0 ascends; Width changes octave count.', 'Solo enabled engine A Shepard’s Pi with audible gain and nonzero Width; compare Rate 49.9/50.0/50.1 plus 0/100. No-movement means Rate movement only; static signal still plays.'),
([25,26,27,28,29,30,31,32,33], 'documented-control', 'Remaining described macros are Tarp Decay/Tone; Extratone Pitch/Env Amount; Noise Loop Rate/Fade; Filtered Noise Freq/Width; Bitgrunge Freq/Mult; Crackle Density/Intensity; Rain Tone/Rate; Bubble Density/Spread; Chord Shape/Inversion. Named descriptions do not prove kernels or RNG.', 'Select each listed type on both engines and inspect macro labels; compare Bitgrunge Mult minimum/maximum with active audible output as ungraded signal observations.'),
([33], 'signal-obligation', 'Chord uses four sawtooth oscillators with Shape intervals and Inversion order. With Use Current Scale, chords use selected scale; with no scale set, incoming root uses major. Availability/version/context remains unresolved.', 'If Chord exists, select it with engine A enabled, compare no scale, C major and D minor with Use Current Scale on; vary Shape/Inversion. Retain actual menu context and do not infer exact chord lists.'),
([35,36,37,38], 'documented-control', 'Amp/Mod envelopes offer ADSR and slopes; Trigger plays all segments ignoring Sustain, Loop repeats entire envelope without holding Sustain, AD Loop repeats Attack/Decay. Mod envelope adds Initial/Peak/Final.', 'Select each mode on Amp and Mod envelopes, adjust graph breakpoints/diamonds and numeric fields; inspect Initial/Peak/Final on Mod only. Exact loop event timing is U.'),
([39], 'documented-state', 'Link Envelopes links corresponding engine Amplitude and Modulation envelopes.', 'Create differing A/B envelope values, enable Link and edit A Attack then B Mod Release; inspect corresponding linked values. Behavior of preexisting differences at link activation remains U.'),
([41,42,43,44], 'documented-control', 'Each engine has LFO 1 and 2 with Hz/sync, Phase Offset and Retrigger. LFO 1 types are Basic Shapes, Ramp, Wander, Alternate, Euclid, Pulsate; FX1/2 each describe eighteen serial effects. LFO 1 and processed LFO1 FX are separate sources. LFO 2 offers Sine, Tri, Saw Up/Down, Rectangle, Random S&H.', 'Enumerate LFO types and inspect source identities; route LFO1 and LFO1 FX to different targets with nonzero amounts; select FX1/2 serial effects and nonzero macro settings. Effect menu identities beyond retained prose remain U.'),
([46,47,48], 'documented-state', 'Matrix source columns/target rows accept signed modulation. Clicking parameter adds it to selected engine matrix; unmodulated temporary row disappears on next selection. Additive/multiplicative target assignment and complete units remain U.', 'Select A, click Filter Frequency, assign LFO1 +25; click Volume without amount then Pan. Inspect retained/temporary rows; repeat B without assuming routes are copied.'),
([51,52,53,54], 'signal-obligation', 'Velocity and Pitch sources use note values for that note duration; Random gets new value at note trigger. MIDI Pitch Bend/Press/Wheel and MPE Note Pitch Bend/Slide/Press supply sources, including clip envelopes.', 'Two simultaneous distinct notes and independent expression events; route each source separately to audible target with nonzero depth and event control. Random sampling distribution, seeding and per-note isolation tolerance remain U.'),
([57], 'signal-obligation', 'Osc Key Tracking off produces C3 constant pitch, or scale root in C3 octave when scale mode active; on follows incoming note.', 'A Basic Shapes only, tracking off/on, note 48 then 72, no scale then D minor. Keep engine/octave/cents and modulation fixed; exact note-to-frequency codec remains U.'),
([58], 'documented-control', 'Phase Reset enables Phase Spread. With Reset on, Spread off sets start phase zero; Spread on follows Spread matrix source.', 'Reset off/on; inspect Phase Spread eligibility, then route Spread to eligible phase behavior with nonzero amount; compare Spread off/on under repeated notes, signal output ungraded.'),
([59,60,61], 'documented-control', 'Oscillator Scale Awareness lists Dual Basic Shapes, Swarm Sine/Triangle/Saw/Square and Chip. Filter Scale Awareness lists Plate and Membrane Resonators. These per-engine settings are distinct from Use Current Scale.', 'Inspect both settings per engine and named scale-aware types under C major/D minor; do not silently add Chord to the six-type list.'),
([62,63,64], 'signal-obligation', 'Portamento slides continuously and Glissando in discrete steps, using scale degrees when scale awareness is on. Both Mono and Poly permit Glide, audible only with Glide Time above zero.', 'Two overlapping notes, Glide Time nonzero; compare Porta/Gliss and Mono/Poly, scale off/on. Repeat at Glide Time zero as negative control with positive baseline retained.'),
([67,68,69,70,71,72,73,74,75], 'documented-control', 'Filter types have Frequency and type-dependent macros. SVF 12/24 L-B-H-N morphs LP/BP/HP/notch; MS2 LP/HP, OSR BP, LP Crunch, LP Switched Res Lofi and Filther are described. Q emphasizes cutoff and Drive saturates input.', 'Select each named filter with engine/filter enabled; inspect two macro labels and move Frequency/Q/Drive where present. No circuit equivalence follows.'),
([76,77,78,79,80], 'documented-control', 'Eq Peak Boost/width and Eq Notch Cut/width, Phaser Feedback/Spread, Redux Crush/Lofi, Vowel Morph and Comb +/- Feedback/Damp have distinct roles.', 'Select each named filter, inspect its two macros and change them independently with audible positive baseline; do not equate Redux filter with standalone Redux device.'),
([81,82], 'signal-obligation', 'Plate and Membrane Resonators describe first 32 modes of rectangular plate/circular membrane and scale-following resonant frequencies with Filter Scale Awareness.', 'Enable A filter with each resonator type and audible sustained stimulus; compare scale awareness off/on across C major/D minor and macro changes. Exact mode frequencies/decays remain U.'),
([84,85], 'signal-obligation', 'Per-engine Volume/Pan and Tone Filter are separate; positive Tone reduces lows and negative Tone reduces highs.', 'Solo engine A with broadband oscillator, Volume audible; compare Tone negative/zero/positive then Pan left/right; repeat B. No crossover or gain law is assigned.'),
([86,94,95], 'documented-control', 'Mixer Drive is per voice after engine mixer settings and before per-voice limiter; Limit gates limiter after both engines mixed and global Drive applied. Global Volume sets output.', 'Both engines audible, nonzero Drive; toggle Limit while holding chord and inspect controls; do not assert threshold, gain reduction or output ceiling.'),
([89,90,91], 'signal-obligation', 'Mono permits Legato: overlap with Legato on reuses current envelope position, off restarts envelope. Poly exposes 2-12 voices.', 'Compare Mono Legato off/on using overlap and separated notes; then Poly voices 2 and 12 with one extra held note. Stealing order and release-tail accounting remain U.'),
([92,93], 'signal-obligation', 'Stacked Voices duplicates both engines including filters/modulation/mix. Spread offsets stacked voices, or notes in held chord when Stacked Voices Off. Spread has no effect without a matrix target.', 'Active A/B with audible output: Spread unassigned then mapped to Pan with nonzero amount; Stacked Voices Off then a displayed enabled count, compare Spread 0/interior/max. No-effect case retains mapped positive baseline.'),
([47], 'signal-obligation', 'The matrix paragraph says negative values speed envelopes/LFOs and positive slow them, but the applicable target/preconditions are unspecified; do not generalize that statement to all destinations.', 'Capture selected target and matrix context before changing signs on a time-related target; compare a Pan target separately. Target-dependent law stays U until context is established.')])

rows('operator', [
([6,92], 'documented-control', 'Four oscillators use eleven predefined algorithms; icons describe top-to-bottom routing. Algorithm selector supports MIDI mapping, automation and real-time modulation.', 'Select all eleven displayed algorithms with A carrier and B active audible modulation; inspect icons and automate two selections in a disposable clip. No private FM algorithm is reconstructed.'),
([11,13], 'documented-control', 'Wave chooser includes sine, resynthesized saw/square/triangle variants, Sine 4/8 Bit, Saw D, Square D, Noise Looped, Noise White and User. Numeric harmonic names denote retained harmonic counts, not exact output samples.', 'Open A-D Wave menus and select listed families; distinguish looped/white noise from deterministic waveform tests.'),
([14,15,16,18], 'documented-state', 'Harmonics editor offers 16/32/64 partials, Shift constrains editing to one harmonic, Repeat off truncates above chosen count, even/odd/all drawing and Normalize; waveform copy/paste works across oscillators.', 'On A User waveform edit partials 1/3/5, Shift-edit 3, inspect status number/amplitude; choose 16/32/64 and Repeat off, even/odd/all and Normalize, copy to B. Exact level compensation remains U.'),
([17], 'documented-state', 'Waveform context exports .ams to User Library Samples/Waveforms; browser drag imports .ams into an oscillator; Simpler/Sampler are also documented consumers.', 'Export test-owned User waveform, retain bytes/path, import into B oscillator. Cross-device import semantics belong to their owners and remain ungraded here.'),
([20,171,172,173,174,175], 'documented-control', 'Osc Coarse/Fine set note-relative ratios; Fixed replaces controls with Frequency Hz and Multiplier and ignores note pitch, with described low endpoint 0.1 Hz. The manual states fixed frequency is Freq multiplied by Multi; no note-frequency formula is supplied.', 'Select A Fixed off/on, inspect controls, enter displayed 0.1 Hz endpoint and two valid multipliers; compare MIDI 48/72 with all pitch modulation off. Grade controls only; actual frequency ungraded.'),
([21,184,185], 'signal-obligation', 'Osc < Vel controls signed velocity pitch response; Q quantizes it as Coarse changes.', 'A audible fixed patch, velocity 32/64/96, positive then negative Osc < Vel; Q off/on. Retain audible baseline and do not invent quantization rounding.'),
([22,23,24,180,181,182,187,188], 'signal-obligation', 'Each oscillator Level/envelope responds to Vel/Key; Phase and R control note-start phase/free-run. Feedback acts only on oscillators not modulated by another oscillator.', 'Compare unmodulated A Feedback nonzero/zero, then algorithm where active B modulates A and repeat A Feedback; B must have nonzero level/envelope. Test R on/off with identical separated notes; no bit comparator.'),
([26,90,95,96], 'documented-control', 'Antialias and Interpolation are independently selectable, Tone affects high-frequency content. Manual new-patch default Antialias on does not prove installed constructor/preset defaults or a numerical alias bound.', 'Inspect switches on a newly documented patch and retained preset separately; compare Tone low/high at high note with enabled audible oscillator; grade switches only.'),
([28,29,30,32,33,157,167], 'documented-control', 'LFO routes Dest A to selected oscillators/filter and Dest B to one extra target; global Amount, Vel and envelope scale depths. Range Low describes 50 seconds-30 Hz, Hi 8 Hz-12 kHz and Sync tempo; R resets/free-runs; Rate < Key 100% doubles per octave.', 'LFO On, active Dest A A and filter, Dest B Pan, all amounts nonzero; inspect Low/Hi/Sync, R and Rate < Key and enumerate waves. No waveform/rate interpolation tolerance is inferred.'),
([35,36,37,38,46,190,191,192,193,194,195,196,201], 'signal-obligation', 'Seven envelopes cover oscillators/filter/pitch/LFO; oscillator Attack is documented linear and Decay/Release exponential, ending -inf dB. Filter/pitch slopes and End vary. Note Off starts Release from current value. Shapes copy across oscillators.', 'Audible A with attack/decay/release nonzero; send Note Off separately during attack/decay/sustain and compare; edit filter/pitch slopes and End; copy A shape to B. Curves and numeric time-to-level tolerances remain U.'),
([39,40,42,197,198], 'documented-control', 'Envelope modes include Loop, Beat, Sync and Trigger. Beat repeats note-relative without quantizing notes; Sync first repeat nearest sixteenth while song plays, otherwise Beat-like. Trigger ignores Note Off. Loop restart level is unresolved.', 'Inspect each mode; with 120 BPM running/stopped transport send note deliberately off-grid and short Note Off; retain future repeated-onset evidence without assigning tick rounding or loop restart level.'),
([41,198,199], 'signal-obligation', 'Loop restart wording differs: overview says current level to peak, Loop Time listing says sustain-to-initial then restart, Beat/Sync listing says current-to-peak. Applicability to the same mode/preconditions is unresolved.', 'Separate Loop, Beat and Sync on A envelope with Initial -24 dB, Sustain -12 dB, nonzero Attack and Loop Time; hold note across repeats while stopped/running. Expected restart segment is U for every mode until resolved.'),
([43,89,97,200], 'signal-obligation', 'Global Time, Time < Key and per-envelope Time < Vel scale envelope segments; Beat/Sync repetition beat-time is not changed by global Time or Time < Vel.', 'Envelope Beat then Sync while transport runs, Repeat fixed, vary global Time and Time < Vel with two velocities; paired Loop mode control. Capture repetition versus segment behavior without a rounding law.'),
([44,45,126,127,133,134,135,136,137], 'documented-control', 'Pitch envelope can target A-D and LFO via Dest A and another Dest B; amount +100% follows levels and -100% inverts sign; envelope On gates it.', 'Pitch envelope On, Dest A A and LFO active with nonzero amount, Dest B Pan, inspect signed amounts and toggles. Keep target positive baseline before disabling.'),
([50,51,52,53,54,55,56,57,58,59], 'documented-control', 'Filter types LP/HP/BP/notch/Morph offer 12/24 dB slopes. Clean/OSR apply all types; MS2/SMP/PRD LP/HP. Non-Clean LP/HP/BP expose Drive. Morph sweeps LP/BP/HP/notch and context snaps to named responses.', 'Enumerate type/circuit eligibility and slopes; select Morph and each snap context option; inspect Drive eligibility without assigning coefficients.'),
([60,61,62,63,64,65,146,148], 'documented-state', 'Filter Frequency responds to velocity/key/envelope/LFO; key 100% doubles per octave around C3. Play by Key sets Freq 466 Hz and Freq < Key 100%; this command is distinct from a global tuning formula.', 'Invoke Play by Key after setting arbitrary frequency/key amount, inspect 466 Hz and 100%; enable one modulation route at a time. Frequency codec/tuning interaction stays U.'),
([66,151,152,153], 'signal-obligation', 'Shaper chooser/Drive act on filtered path; Dry/Wet 0% bypasses shaper and shaper drive.', 'Filter On with audible A, choose shaper and nonzero Shaper Drive; compare Drive settings at Dry/Wet 100% positive baseline then at 0%. Do not claim bit-identical bypass.'),
([69,70,93,94], 'signal-obligation', 'Voices supports up to 32; excess notes cut oldest notes. Voices 1 plays overlapping notes legato without retriggering envelopes. Global R retriggers an already enabled note rather than adding a voice.', 'Voices 2: hold notes 48,60,72 in order; then Voices 1 overlapping 48/60; global R off/on duplicate note-on while old note held. Duplicate note-off pairing and Spread voice accounting remain U.'),
([71,72,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124], 'documented-control', 'Velocity, Key, Aftertouch, Pitch Bend and Mod Wheel each route to two targets with independent amounts; fixed Time < Key and PB Range coexist. Targets include Off, oscillator volume/crossfades/feedback/fixed pitch/FM Drive, filter controls, shaper, LFO, pitch envelope, Volume/Pan/Tone/Time; eligibility is target-specific.', 'Route Wheel to Pan and Filter Frequency, nonzero depths; select Off and confirm route control state. Compare Feedback only on eligible oscillator, Fixed Frequency only with Fixed on, Morph only in Morph. No universal source-depth law is assigned.'),
([74,131,132], 'signal-obligation', 'Glide is polyphonic, starts new note at prior-note pitch then slides; legato Glide does not retrigger envelopes; Glide Time has no effect if Glide off.', 'Voices 4, nonzero Glide Time, overlapping and separated notes with Glide off/on; keep audible positive transition baseline.'),
([75,76,128], 'signal-obligation', 'Spread uses two detuned voices per note panned L/R; whether a note uses Spread is determined at Note On.', 'Play held note A with Spread 0 then raise Spread without new note; trigger B with Spread nonzero, lower Spread while B held; keep distinguishable notes. Exact held-note detune updates and voice-budget interaction remain U.'),
([129,207,208,209,210], 'documented-state', 'Transpose changes already-playing notes. Context commands copy oscillator parameters, set all envelope levels to maximum/minimum/middle, edit harmonics and export .ams.', 'Hold audible note and change Transpose; separately inspect envelope-level commands and oscillator copy in disposable patch. Sound change remains qualitative/ungraded; command scope must be retained.'),
([211], 'documented-control', 'Enable Per-Note Pitch Bend is documented on by default and can be disabled in device-title context.', 'Inspect fresh instance context then retained preset separately; two held notes with independent per-note bend, toggle off/on, compare global bend. Exact-build default, bend range and note isolation remain U.')])

rows('wavetable', [
([3,8,9,10], 'documented-control', 'Two oscillators enable independently; tabs select editing, expanded view redistributes controls. Gain/Pan/Semi/Detune are per oscillator. Category/table choosers and arrows traverse category boundaries.', 'Select both tabs and expanded view, inspect controls, step arrows across final table of a category and reverse; no fixed factory table list is inferred.'),
([11,12], 'documented-state', 'Dropping WAV/AIFF on visualization imports it; choosers/arrows then browse its folder. Raw bypasses automatic sample preprocessing.', 'Import owned WAV A and AIFF B, inspect chooser folder context and Raw off/on. Do not invent import segmentation, resampling or normalization kernels.'),
([13,14], 'documented-control', 'Dragging visualization or Wave Position selects table position. Linear/polar show same data with distinct layouts.', 'Move Wave Position via slider then display, switch linear/polar and inspect retained position; no screenshot/pixel or spectral equivalence criterion.'),
([15,16,17,18,19], 'documented-state', 'Oscillator effects are FM (Amt/Tune), Classic (PW/Sync), Modern (Warp/Fold). Two effect values persist across effect-type changes. FM Tune +/-50% and +/-100% describe +/-1 and +/-2 octave modulator offsets.', 'Set effect parameters to nonzero 25% and 50%, cycle FM/Classic/Modern and inspect retained values; inspect signed Tune landmarks without inferring intermediate formula.'),
([21,22,23], 'signal-obligation', 'Sub enables independently with Gain, Tone 0% sine/increasing harmonics, and one/two octave-down switches relative to note/global Transpose.', 'Disable main oscillators, Sub On and Gain audible; compare Tone 0/interior and octave switches with Transpose 0/+12. Exact waveform/frequency law remains U.'),
([26,27,28,29,30,31,32,33,34], 'documented-control', 'Each filter offers LP/HP/BP/notch/Morph, 12/24 dB slopes; Clean/OSR all types and MS2/SMP/PRD LP/HP. Non-Clean LP/HP/BP expose Drive. Display dots adjust Frequency/Resonance; Morph traverses LP/BP/HP/notch.', 'Enable both filters, enumerate type/circuit/slope eligibility; drag each dot, inspect controls and Morph positions. No circuit equivalence to Operator or EQ Eight is asserted.'),
([35,36,37,38], 'signal-obligation', 'Serial sends mains through Filter 1 then 2; Parallel feeds mains to both; Split assigns Osc 1/2 to Filter 1/2 and halves Sub to both. Split leaves corresponding oscillator audible when its filter is off.', 'Use distinct main waves/pans, Sub audible and both filters enabled with different cutoffs; select Serial/Parallel/Split, solo each source and disable its Split filter. Preserve active positive baselines and unmuted output.'),
([40,41,42,43,44,45,46,47,48,49,50], 'signal-obligation', 'Matrix uses source columns/target rows. Additive values sum then add to parameter, neutral 0; multiplicative values multiply then multiply parameter, neutral 1 minimum 0. Source units, depth scaling, clamps and each target assignment remain unresolved except explicit labels.', 'Route Env2 and LFO1 to one documented multiplicative target such as Amount, then one other target with retained context; compare one/two active routes. Do not equate displayed percentages with internal normalized values.'),
([51,52,89], 'documented-state', 'Clicked parameter appears temporarily; nonzero modulation keeps its row, otherwise next selected parameter replaces it. Matrix and MIDI tabs share rows; source headers jump to source panels.', 'Click Pan unassigned then Gain, assign Gain nonzero modulation and click Pan again; switch MIDI tab and inspect shared row; click Env2 source header.'),
([53], 'signal-obligation', 'Time scales all modulator times, negative faster/positive slower. A modulator assigned to Time does not scale itself through that route but still scales other destinations.', 'Route audible Env2 to oscillator position and to Time with nonzero amount, LFO1 to Pan; change Time sign then route LFO1->Time separately. Exact self-exclusion and composed rate law remain U.'),
([54,79,93,105], 'documented-control', 'Global Matrix Amount, LFO Amount, instrument Volume and Unison Amount are documented multiplicative destinations.', 'Click each named target and inspect matrix eligibility; route one active source with nonzero depth at each, retaining audible nonzero base amount.'),
([58,59,60,61,62,63,64,65,66], 'documented-control', 'Amp, Env2 and Env3 have Time/Slope; Env2/3 also Initial/Peak/Final, absent on Amp. Positive slopes start fast then slow; negative slow then fast; zero linear. Sustain/Initial are documented multiplicative where present.', 'Inspect all three envelopes, change breakpoints and slope diamonds with positive/zero/negative values; inspect absence of Amp Initial/Peak/Final.'),
([61,67,68,69,70], 'signal-obligation', 'Envelope None holds Sustain until Note Off; Trigger plays all segments at Note On; Loop repeats whole envelope without Sustain hold until voice ends.', 'Audible Amp envelope and Env2 routed nonzero to position; compare None/Trigger/Loop with short/long held notes, nonzero release and sustain. Exact loop retrigger/voice end timing is U.'),
([72,73,74,75,76,77,78], 'documented-control', 'Two LFOs offer Sine, Saw, Triangle, Square and Random with waveform-dependent Shape. Sync switches rate Hz/beat divisions.', 'Enumerate five waves on LFO1/2; inspect Shape changes and Hz/sync units. Random distribution is not assigned.'),
([80,81,82], 'signal-obligation', 'LFO Offset sets start phase and cannot be modulated; Attack fades in after Note On; Retrigger resets phase on each new note.', 'Route audible LFO1 to Pan with nonzero depth, nonzero Attack/Offset; send repeated notes with Retrigger off/on; inspect Offset matrix ineligibility. Exact phase and fade law remain U.'),
([85,86,87,88], 'signal-obligation', 'MIDI Velocity/Note apply through note duration; Note 100% Filter Frequency tracks pitch around C3. Pitch Bend/Aftertouch/Wheel can use clip envelopes; Random samples at each new note.', 'Route each source separately with nonzero amount; for Note use enabled audible filter and 100%; for Random repeat eight notes. Codec, seed/distribution and MPE extension are U.'),
([92,94,95,96], 'documented-control', 'Transpose uses semitones; Mono is single voice with legato envelopes and permits Glide; Poly enables Poly Voices and disables Glide.', 'Switch Mono/Poly during separated then overlapping notes, inspect Poly Voices/Glide eligibility, set nonzero Glide in Mono. Allocation/held-note transition remains U.'),
([97,98,99,100,101,102,103], 'documented-control', 'Unison choices are none, Classic, Shimmer, Noise, Phase Sync, Position spread and Random note. They differ in detune, phase reset, stereo and position/randomization roles.', 'Select none then each of six modes with enabled main oscillator and Unison Amount nonzero; inspect names. No detune grid, RNG or stereo equation is supplied.'),
([104,105], 'signal-obligation', 'Unison Voices controls oscillators per main wavetable oscillator; Amount is mode-dependent intensity, distinct from Poly Voices note count.', 'Poly Voices fixed, one main oscillator audible; select each unison mode with Voices two displayed values and Amount 0/nonzero. Capture displayed values before future signal comparisons.'),
([107,108,109], 'documented-control', 'Hi-Quality context switch controls quality; off is documented modulation every 32 samples and lower-power filters. CPU saving up to 25% is a conditional manual claim, not a required timing benchmark.', 'Inspect Hi-Quality on/off with a fixed modulated patch; do not assert numerical output parity, CPU percentage or private scheduler implementation.'),
([110,111], 'documented-state', 'As of Live 11.1 the manual describes Hi-Quality off for new/Core Library instances while earlier user presets/Sets retain on for consistency; enabling may produce subtle differences. Migration boundaries for this target are unresolved.', 'Compare fresh instance, retained Core Library preset and identified pre-11.1 user preset/Set if available; do not substitute a historical Creator string for load behavior. Unavailable old fixture remains U.'),
([7], 'signal-obligation', 'Manual claims unmodulated raw oscillator output is band-limited with no aliasing at any pitch. No spectral measurement definition, finite pitch-domain fixture or tolerance accompanies this claim.', 'Osc 1 only, no oscillator effects/modulation/unison, filters bypassed, audible output; future low/mid/high MIDI notes require retained render and defined alias metric before grading. Do not convert prose into a numerical guarantee.')])

states = {
'DF': 'Mono Legato on, Thickness interior, nonzero Glide, Cycling Env2 -> Osc1 Shape and LFO -> cutoff with nonzero depths; oscillator/filter routing active; Note PB on.',
'DS': 'Owned sample A Start 25% Length 50%, Gate envelope, active Loop playback effect and filter, Slide -> FX1 nonzero; separately Trigger Hold inf.',
'ME': 'A/B engines and filters on, nonzero cross-engine modulation, linked envelopes, stacked voices enabled with Spread -> Pan nonzero, Glide nonzero, Use Current Scale on.',
'OP': 'A carrier/B modulator active in retained algorithm, nonzero B level/envelope, LFO/pitch envelope routes active, Loop envelope, Voices 2, nonzero Spread/Glide.',
'WT': 'Owned imported wavetable A with Raw off, both main oscillators active, Split filters, Env2/LFO1 routes nonzero, Loop envelope, Poly Voices set, Unison Classic nonzero.'}
boundary_inputs = {
'DF': 'Transpose -48/0/48 and attempted -49/49 st; Shape Mod -100/0/100 and attempted -101/101%; Voices 32 with 33 held notes in Poly.',
'DS': 'Sample Gain -70/0/24 and attempted -71/25 dB; Detune -50/0/50 and attempted -51/51 cents; Trigger Hold inf then Gate.',
'ME': 'Poly Voices 2 and 12 with 3 and 13 held notes; Shepard’s Pi Rate 49.9/50.0/50.1; Glide Time zero then displayed nonzero.',
'OP': 'Voices 1/2/32 with 2/3/33 held notes; Fixed Frequency displayed 0.1 Hz then attempted negative frequency; envelope Initial -24 dB/Sustain -12 dB.',
'WT': 'FM Tune -100/-50/0/50/100%; LFO Shape low/interior/high displayed values; Poly Voices chosen 2 with 3 held notes; attempt numeric text abc.'}
automation_inputs = {
'DF': 'Transpose 0 to +12 st; Shape Mod 0 to +50%; Mono to Poly.',
'DS': 'Sample Start 0 to 25%; Sample Gain -12 to -6 dB; Trigger to Gate.',
'ME': 'engine A Semitones 0 to +12 with scale off; engine A Pan center to right; Mono to Poly.',
'OP': 'Transpose 0 to +12 st; A Level -12 to -6 dB; two explicitly retained Algorithm icons.',
'WT': 'oscillator Semi 0 to +12; Pan center to right; FM to Classic effect.'}
steps = [
('BOUNDARY', 'boundary', 'Enter documented endpoints then adjacent and out-of-range numeric values for named controls in a disposable patch; add one simultaneous note beyond selected voice limit.', 'Clamp/reject/rounding policy, voice-tail budget and extreme behavior are not established.'),
('AUTOMATION', 'automation', 'Record two valid different displayed control values and a mode change over beats 1-4; stop and re-enable automation; compare playback with manual edits.', 'Eligibility, interpolation/smoothing, modulation-versus-automation precedence and re-enable behavior remain U.'),
('TRANSPORT', 'transport', 'Hold note/captured playback, stop, seek backward and restart at 120 BPM with synced modulation active; send final Note Off.', 'Reset/free-run/retrigger, repeated-note ownership and tail policy on transport changes remain U.'),
('PERSISTENCE', 'persistence', 'Save test-owned Set and device preset, close/reopen and reload; compare visible named settings/routes. For imported/sample media relocate source in a disposable copy and reopen.', 'Device setting/media preservation, missing-file recovery and migration outcome remain U; stored fields prove no load law.'),
('UNDO', 'undo-redo', 'Edit a named mode, modulation route/depth and envelope; undo three operations then redo three, noting each visible state and any still-held note.', 'Undo grouping, sound state rewind and redo invalidation are U; local matrix clear/copy is not proof of global history behavior.'),
('MALFORMED', 'malformed', 'Use test-owned copies only: invalid numeric text, truncated user media where relevant and a disposable saved state with one invalid control value; attempt import/load.', 'Failure message, rejection/normalization, unchanged-state guarantee and crash resistance are U.'),
('CANCEL', 'cancellation', 'Begin preset/media hot-swap or file dialog where exposed, change preview selection, then cancel before commitment; compare active state and held note.', 'Cancellation availability, rollback scope and preview side effects remain U; absence of a documented cancel command does not make case inapplicable.'),
('TEARDOWN', 'teardown', 'While notes/releases/modulation are active, remove device, close Set and disconnect expression source in separate trials; observe output and persistent state.', 'Note-off cleanup, tail cutoff, resource release, disconnection behavior and error recovery remain U.'),
('SAMPLE-RATE', 'sample-rate', 'Repeat fixed patch at 44.1, 48 and 96 kHz with controlled 64/256-frame host blocks; then change rate while stopped and while a note is held if supported.', 'Rate-change support, timing/phase/filter/envelope continuity, block invariance and numerical tolerances remain U.'),
('TUNING-MPE', 'tuning-mpe', 'Use two held notes with independent per-note bend, pressure and slide; apply C major then an identified non-12-tone tuning, compare global bend and source disconnection.', 'Per-device tuning participation, bend codecs/ranges, unsupported-source handling and exact expression isolation remain U; no equal-temperament formula is assumed.')]
for slug, prefix, name, cls in DEVICES:
    rid = f'REQ-SYN-{prefix}-LIFECYCLE'
    requirements.append({'id': rid, 'device': name, 'provenance': 'U', 'target_applicability': 'U', 'contract': 'Required device-specific lifecycle, error, boundary, tuning and expression outcomes below remain unknown.', 'source_blocks': []})
    for suffix, kind, action, unknown in steps:
        cases.append({'id': f'SYN-{prefix}-U-{suffix}', 'requirements': [rid], 'device': name, 'kind': kind, 'preconditions': ['common-setup', 'positive-signal-guard'], 'setup_and_action': states[prefix] + ' ' + (boundary_inputs[prefix] + ' ' if suffix == 'BOUNDARY' else automation_inputs[prefix] + ' ' if suffix == 'AUTOMATION' else '') + action, 'documentary_expected': None, 'documentary_comparator': None, 'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False, 'unknown': unknown, 'source_blocks': [], 'fixture': f'stimulus-recipes.json#{prefix}'})
write('requirements.json', requirements)
write('cases.json', cases)
write('stimulus-recipes.json', {'purpose': 'Finite future analyst setups, not executed reference fixtures or device defaults', 'common-setup': ['Editable test-owned Set; enabled isolated instrument on MIDI track; Monitor In; no later effects; track/master unmuted; output gain audible and attenuated; retain every displayed mode/value.', 'Analyst baseline: 4/4, 120 BPM, 48 kHz, host block 256; separated MIDI 60 velocity 96, beat 1 on/beat 3 off; overlap 48 on beat 1, 60 on beat 2, offs beats 3/4. All are stimulus choices, never product limits.', 'No sample file is fabricated by this author tool. Before media cases retain test-owned 2 s WAV sample A with distinct transient plus sustain and 1 s AIFF B, record bytes/rate/channels/hash. If unavailable case remains U.', 'Independent expression test uses two notes and separately identified per-note pitch/pressure/slide versus global pitch bend; exact transport codec remains with MPE owner.'], 'positive-signal-guard': ['Enable oscillator/engine/sample and destination section, route source to audible output, set nonzero base gain, nonzero modulation/effect amount and nonzero stimulus; clear other routes and avoid mute/dry-only/zero-send baselines.', 'No-effect comparison first needs paired active positive baseline. Change only deliberate zero amount, disabled route, eligibility switch or ineligible target under test; never grade silence from an absent sample/note or inactive path.', 'Controls/state comparators inspect visible named state only. Acoustic adjectives, static package fields, defaults, CPU prose and names never substitute for retained output evidence.'], 'device_states': states, 'original_execution': False, 'candidate_comparison': False})
counts = {name: {'documentary_requirements': sum(r['device']==name and r['provenance']=='D12' for r in requirements), 'unknown_requirements': 1, 'cases': sum(c['device']==name for c in cases), 'kinds': dict(Counter(c['kind'] for c in cases if c['device']==name))} for _,_,name,_ in DEVICES}
write('counts.json', counts)
assert len({r['id'] for r in requirements}) == len(requirements)
assert len({c['id'] for c in cases}) == len(cases)
assert all(c['expected'] is None and c['comparison'] is None and not c['executed'] for c in cases)
assert {r['id'] for r in requirements} == {v for c in cases for v in c['requirements']}

link = '../../analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/'
head = '''---
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

Use the [finite setups](REPLACE_LINKstimulus-recipes.json) with isolated enabled
instruments, valid notes/media, enabled processing sections, nonzero amounts and
unmuted audible output. Every no-effect proposal needs an active paired positive
baseline; disabled engines, absent notes/samples, zero depth or muted output
cannot establish processing behavior. Tests reset held notes, routes and prior
histories between independent trials. Media recipes are future test inputs:
no rendered audio, MIDI captures, sample fixture or original execution is claimed.

The [requirement catalog](REPLACE_LINKrequirements.json) and
[case catalog](REPLACE_LINKcases.json) retain one finite case per documentary
requirement plus ten device-specific U lifecycle cases. Documentary control/state
comparators inspect named visible values, choices, eligibility or transitions.
Signal obligations have no numerical comparator. All exact-target `expected`
values and comparisons are null, all target grades U, all `executed:false`.
Documentary expectations are proposals for Version 12 prose, not 12.4.3 passes.

## Individual requirements

Every row below is D12/target-U. Evidence references resolve to exact retained
HTML paragraph/heading blocks, with HTML line and heading context, in the appendix.
Actions and preconditions are in the case with the same prefix/number.

'''.replace('REPLACE_LINK',link)
for slug,prefix,name,cls in DEVICES:
    obs=next(o for o in json.loads((P/'preset-observations.json').read_text()) if o['device']==name)
    head += f'### {name}\n\nCurrent surface `SURF-DEVICE-{slug.upper()}`; package association `{cls}` / schema line {obs["schema_line"]}.\n\n| Requirement | Documented contract and limits | Exact blocks |\n| --- | --- | --- |\n'
    for r in requirements:
        if r['device']==name and r['provenance']=='D12':
            head += f'| {r["id"]} | {r["contract"]} | ' + ', '.join(f'`{b}`' for b in r['source_blocks']) + ' |\n'
    head += f'\n**REQ-SYN-{prefix}-LIFECYCLE — U:** the ten concrete obligations below remain required, ungraded behavior.\n\n'
head += '''## Lifecycle, boundaries and errors

Each device has distinct `SYN-<prefix>-U-<suffix>` cases for BOUNDARY, AUTOMATION,
TRANSPORT, PERSISTENCE, UNDO, MALFORMED, CANCEL, TEARDOWN, SAMPLE-RATE and
TUNING-MPE. These are not inapplicable omissions: all expected outcomes are U.
Numeric endpoint inspection in D12 cases does not prove adjacent-value handling,
clamping, normalization or rounding. Rate/block choices are analyst stimuli, not
supported device limits. Malformed loads operate only on disposable test copies.

| Device / prefix | Concrete state for all ten lifecycle cases |
| --- | --- |
'''
for _,prefix,name,_ in DEVICES:
    head+=f'| {name} / {prefix} | {states[prefix]} |\n'
head+='''
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
'''
for _,_,name,_ in DEVICES:
    c=counts[name];k=c['kinds']
    head+=f'| {name} | {c["documentary_requirements"]} | 1 | {c["cases"]} | {k.get("documented-control",0)} / {k.get("documented-state",0)} / {k.get("signal-obligation",0)} |\n'
head+=f'\nTotal: **{len(requirements)} requirements** ({len(requirements)-5} D12, 5 U), **{len(cases)} unexecuted cases**. Exact-target graded cases: **0**.\n\n'
head+='''Exact DSP, tuning, randomization/seed, phase, envelope curves/timing, filters,
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

The [source ledger](REPLACE_LINKsources.json) pins the shared manual/schema and
five retained presets. The [block views](REPLACE_LINKmanual-locators.json) retain
source lines and heading context. The [author manifest](REPLACE_LINKmanifest-author-r1.json)
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
  [Field observations](REPLACE_LINKschema-fields.json) establish vocabulary only.
- Five preset copies and decoded XML retain `Creator: Ableton Live 12.4d1`,
  revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`, schema `12.0_12402`.
  Their inclusion in 12.4.3 is observed; that metadata is not a 12.4.3 runtime
  default or migration test. Exact file hashes are in the ledger.

| Device | Manual section / block range | Retained view |
| --- | --- | --- |
'''.replace('REPLACE_LINK',link)
for slug,_,name,_ in DEVICES:
    blocks=json.loads((P/f'manual-{slug}-blocks.json').read_text())
    head+=f'| {name} | §{blocks[0]["text"].split()[0]}; `{slug}:B001–B{len(blocks):03d}` | [Blocks]({link}manual-{slug}-blocks.json), [text]({link}manual-{slug}.txt) |\n'
head+='''
## Revision and handoff

Revision 1 is an author-frozen partial draft awaiting separate analyst review.
No handoff is published and no existing release is expanded by this page.
'''
(ROOT/'wiki/specs/synthesis-instruments.md').write_text(head)

research='''---
id: RES-SYNTHESIS-INSTRUMENTS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Five synthesis and drum instrument profiles

## Authority and bounded investigation

This is the F-06 analyst owner for Drift, Drum Sampler, Meld, Operator and
Wavetable. The [canonical draft](../specs/synthesis-instruments.md) owns behavior;
this page owns evidence interpretation and limitations. Read the
[inventory](full-live-coverage-inventory.md) and
[coverage design](full-live-specification-design.md) for the denominator and
closure rule. None of the five profiles is complete or released.

The existing manual/schema capture from [sample instruments](sample-instruments.md)
was reused, with exact hashes checked; no new fetch or original execution was
needed. The previous author had already retained five inventory-selected shipped
presets, decompressed XML and schema/preset observations. This continuation
preserves those captures and adds finite documentary requirements/cases,
paragraph locators, canonical snapshots and author validation.

## Sources and observations

The [source ledger](REPLACE_LINKsources.json) contains seven pins: the external
Version 12 instrument HTML captured 2026-10-19T20:27:58.247940+00:00, the external
installed `12.0_12402` schema, and five copied Core Library defaults. The manual
SHA-256 is `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`;
the schema is `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Manual patch parity remains U. The preset roots/fields are directly observed,
not reader/writer execution or a map of constructor defaults. Preset headers say
Live 12.4d1, not 12.4.3. Their package presence remains valid exact-build evidence
of supplied resources while their loading, semantics and DSP remain unproven.

| Device | Observed preset root | Manual section | Schema line | Retained paragraphs/headings |
| --- | --- | --- | --- | --- |
'''.replace('REPLACE_LINK',link)
for slug,_,name,cls in DEVICES:
    obs=next(o for o in json.loads((P/'preset-observations.json').read_text()) if o['device']==name)
    blocks=json.loads((P/f'manual-{slug}-blocks.json').read_text())
    research+=f'| {name} | `/Ableton/{cls}` | §{blocks[0]["text"].split()[0]} | {obs["schema_line"]} | {len(blocks)} [blocks]({link}manual-{slug}-blocks.json) |\n'
research+='''
[Schema fields](REPLACE_LINKschema-fields.json) and
[preset observations](REPLACE_LINKpreset-observations.json) preserve the exact
association. No field spelling establishes an enum, default, clamp, automation
eligibility, signal path or sound. Figures were not inspected separately.

## Source ambiguities and interpretation limits

**Operator restart — unresolved context.** The manual overview §31.9.4
`operator:B039–B041` describes Loop retrigger and restart from current level to
peak to avoid clicks. The complete parameter list §31.9.10.7
`operator:B197–B199` distinguishes general Loop/Beat/Sync, current-to-peak in the
Beat/Sync Repeat entry, and sustain-to-initial movement in Loop Time. These may
refer to distinct modes or phases. No contradiction is declared without matching
mode and preconditions; no prose is silently discarded. SYN-U-OP-LOOP / case
SYN-OP-012 retains distinct Loop/Beat/Sync setups with nonzero Initial/Sustain,
Attack and Loop Time, running/stopped clocks and unknown expected outputs.

**Meld count — unresolved version/context.** §31.8.2 `meld:B009` says twenty-four
types and six scale-aware types. §31.8.3 `meld:B012–B033` names twenty-five macro
types when all four Swarms and Chord are counted. The draft retains the named
macro controls and Chord's documentary scale behavior, but assigns no exact menu
count. The six-type scale-aware list at §31.8.8 `B060` does not include Chord;
this can be a different scale context, so Chord is not silently inserted into it.
SYN-U-ME-TYPES keeps the uncertainty visible. A version-matched UI enumeration or
bounded package mapping is needed to establish available type identities.

**Meld sign wording — target unspecified.** §31.8.6 `meld:B047` describes signed
matrix changes and faster/slower modulators without fixing the target/unit.
SYN-U-ME-TIME / SYN-ME-024 keeps this as a signal obligation and does not turn it
into a universal modulation law. Wavetable's explicitly documented additive and
multiplicative rules are not transferred to Meld or other instruments.

## Finite author packet

[Requirements](REPLACE_LINKrequirements.json), [cases](REPLACE_LINKcases.json)
and [stimulus recipes](REPLACE_LINKstimulus-recipes.json) separate documentary
expectations from all-null exact-target results. Every requirement has source
blocks and a finite action, or is an explicit U lifecycle obligation with ten
concrete per-device cases. No omitted negative/malformed/cancel/teardown behavior
is labelled inapplicable. Effect/no-effect tests require active sections, routes,
nonzero depth/gain, valid notes/media and an audible paired positive baseline.
Media setups require future retained owned WAV/AIFF/AMS bytes; they are not
provided reference outputs. The extractor only parses pinned HTML; author tools
write analyst docs/catalogs and assert structural relationships.

| Device | D12 / U requirements | Cases |
| --- | --- | --- |
'''.replace('REPLACE_LINK',link)
for _,_,name,_ in DEVICES:
    c=counts[name];research+=f'| {name} | {c["documentary_requirements"]} / 1 | {c["cases"]} |\n'
research+=f'\nTotal **{len(requirements)} requirements / {len(cases)} cases**, no S/X expectations, no executions and no candidate grades.\n\n'
research+='''Required unknowns include exact 12.4.3 parity, audio curves/kernels/phase,
frequency and bend/tuning codecs, rate/block behavior, RNG/statistics, voice
stealing/stacking budgets, media/import failure semantics, automation/history,
state persistence/migration, cancellation, teardown, accessibility and CPU
performance. These prevent complete-draft or whole-profile closure. Existing
finite device handoffs and T1 are unaffected; Amp/Cabinet emulation remains
outside this packet and no restricted implementation workspace is claimed.

## Freeze and review

[Author manifest](REPLACE_LINKmanifest-author-r1.json) freezes packet bytes,
external source pins and exact canonical page snapshots. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments/validate.py`
for the focused identity/catalog/link/frontmatter/whitespace checks. The retained
[author validation](REPLACE_LINKvalidation-author-r1.json) reports actual scope;
a pass establishes structural consistency only. Root owns the shared index,
coverage, questions, plan and append-only log integration. Separate analyst
review is required before any reviewed-contract claim or sanitized handoff.
'''.replace('REPLACE_LINK',link)
(ROOT/'wiki/research/synthesis-instruments.md').write_text(research)
locators={}
for slug,_,_,_ in DEVICES:
    headings=[]
    for b in json.loads((P/f'manual-{slug}-blocks.json').read_text()):
        if re.fullmatch('h[2-5]',b['kind']):
            level=int(b['kind'][1]);headings=[h for h in headings if h['level']<level]
            headings.append({'level':level,'section':b['section'],'anchor':b['anchor'],'text':b['text']})
        locators[b['locator']]={'file':f'manual-{slug}-blocks.json','html_line':b['html_line'],'heading_context':list(headings),'text':b['text']}
write('manual-locators.json',locators)
print(json.dumps({'requirements':len(requirements),'cases':len(cases),'device_counts':counts},indent=2))
