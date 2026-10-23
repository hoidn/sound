"""Twenty separate documentary Max-device profiles; no original patch or host code."""
from pathlib import Path
from collections import Counter
import hashlib, json, re
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
INV=json.loads((P/'inventory-devices.json').read_text())
BLOCKS={b['locator']:b for b in json.loads((P/'manual-blocks.json').read_text())+json.loads((P/'dated-blocks.json').read_text())}
REQ=[];CASES=[]
def write(name, value):(P/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def add(name, refs, kind, contract, action, grade='D12'):
 device=next(d for d in INV if d['name']==name);key=device['id'].removeprefix('SURF-MAX-')
 n=1+sum(r['device']==name for r in REQ);rid=f'REQ-MXD-{key}-{n:03d}'
 refs=[f'MXD:B{r:03d}' if isinstance(r, int) else r for r in refs]
 assert all(r in BLOCKS for r in refs)
 REQ.append({'id':rid,'device':name,'surface':device['id'],'provenance':grade,'target_applicability':'U','contract':contract,'source_id':'D12-2025-MAX-GAPS' if grade=='D12-2025' else 'D12-MAX-DEVICES','source_blocks':refs})
 CASES.append({'id':f'MXD-{key}-{n:03d}','requirements':[rid],'device':name,'kind':kind,'provenance':grade,'fixture':'fixtures.json#MXD-F0','setup_and_action':action,'documentary_expected':contract,'documentary_comparator':None if kind in ['signal-obligation','timing-obligation'] else 'Compare only named control choices/units/eligibility, mapping/selection/data-display roles or explicit visible state transitions; no numerical DSP/MIDI/scheduling/private-state oracle.','expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':refs})
def rows(name, data, grade='D12'):
 for r in data:add(name,*r, grade=grade)
rows('DS Clang',[
([9,10,12],'signal-obligation','Two Tone A/B levels are independent; Noise adds white-noise content. Named components do not define synthesis or RNG implementation.','Valid DS Clang, audible Volume; preview with Tone A nonzero/B zero, then reverse, then both plus nonzero Noise; retain each active source response.'),
([11],'signal-obligation','Filter adjusts high-pass/band-pass cutoff and higher settings increase high-frequency content; no filter curve is given.','Audible tones/noise, Filter low/interior/high displayed values; retain relevant-band positive baseline.'),
([13],'control','Clave enables Repeat for clave repetitions.','Toggle Clave off/on with audible output, set Repeat to distinct accepted values; no count/spacing law inferred.'),
([14,15],'control','Pitch changes pitch, Decay sound length and Volume overall level; upper-half display click previews current settings.','Click upper display with Volume nonzero, vary Pitch/Decay, then trigger notes separately; preview versus MIDI identity/output tolerance remains U.')])
rows('DS Clap',[
([17,18],'signal-obligation','Sloppy changes spacing of panned clap delay lines; Tail adds filtered noise. Exact impulse/delay/noise law is not specified.','Audible preview, fixed Decay; compare low/high Sloppy and Tail zero/nonzero with retained nonzero clap baseline.'),
([19],'signal-obligation','Spread 0% is mono and 100% widened stereo; Tone higher increases high-frequency content.','Audible clap with nonzero Tail and Sloppy; compare Spread 0/50/100% and Tone low/high; no channel equality or width metric assigned.'),
([20],'control','Tune sets pitch, Decay sound length and Volume level.','Inspect Tune/Decay/Volume and change two accepted values each with audible positive baseline.'),
([21],'control','Upper-half display click previews current settings.','Click upper half, then note trigger in reset trials; no note/preview velocity or phase equivalence claimed.')])
rows('DS Cymbal',[
([23,24],'signal-obligation','Cymbal source includes sine/pulse and high-passed noise; Tone raises high-pass cutoff. Names provide no waveform or noise tolerance.','Audible preview, compare Tone low/interior/high and retain high-band stimulus/output.'),
([25],'control','Pitch, Decay and Volume adjust pitch, length and overall level.','Change Pitch/Decay/Volume independently to two displayed accepted values; no numerical waveform/frequency law.'),
([26],'control','Upper-half display click previews current settings.','Click upper display and retain settings and audible output prerequisite.')])
rows('DS FM',[
([29,30],'signal-obligation','Tone sets low-pass cutoff; Feedb. controls FM feedback with more noise at higher values. No feedback transfer law or alias bound is supplied.','Audible preview, Tone interior; compare Feedb. zero/nonzero/high and Tone low/high without clipping output.'),
([31],'signal-obligation','Amnt controls FM depth; Mod blends modulation types, whose exact identities/law are unspecified.','Nonzero Amnt, move Mod between accepted endpoints/interior; compare Amnt zero only after active positive baseline.'),
([32],'control','Pitch is global pitch, Decay sound length and Volume overall level.','Inspect Pitch/Decay/Volume and change accepted values independently.'),
([33],'control','Upper-half display click previews sound at current settings.','Click upper display with nonzero gain; no sample-identical repeat criterion.')])
rows('DS HH',[
([35,36],'control','Hat combines noise/sine; Noise selects white or pink.','Enumerate Noise toggle with audible output, keeping other controls fixed; no RNG or exact spectrum law.'),
([37,38],'control','Tone sets high-pass cutoff; pitched portion uses resonant high-pass with 12/24 dB slope choices and Attack.','Inspect slopes, vary Tone/Attack at audible output; do not infer coefficients or shared response with other filters.'),
([39],'control','Pitch is global pitch, Decay sound length and Volume level.','Change named controls independently at accepted values.'),
([40],'control','Upper-half display click previews current settings.','Click upper display with Volume audible, reset between repeated trials.')])
rows('DS Kick',[
([42,43],'control','Pitch is in Hz; Drive adds distortion and OT harmonics to modulated-sine kick.','Inspect Pitch Hz and choose accepted 50/100 Hz if offered; compare Drive/OT zero versus nonzero with active positive baseline.'),
([44],'signal-obligation','Attack smooths sine onset; Click adds transient.','Audible kick, compare Attack low/high and Click off/on; exact click content and envelope ungraded.'),
([45],'control','Decay controls length, Env pitch modulation, Volume level.','Keep Volume audible and Env nonzero, compare two Decay/Env settings independently.'),
([46],'control','Upper-half display click previews current settings.','Click upper half and retain signal/settings; no note-frequency codec inferred.')])
rows('DS Snare',[
([48,49],'signal-obligation','Color changes pitched-oscillator tone; Tone controls noise presence.','Audible snare, compare Color and Tone independently, keeping positive pitched/noise baselines.'),
([50],'control','Noise filter choices are low-pass, high-pass and band-pass.','Select each filter with nonzero noise Tone and audible output; no kernel law.'),
([51],'control','Decay adjusts length, Tune global pitch and Volume overall level.','Inspect and vary named controls independently at accepted displayed values.'),
([52],'control','Upper-half display click previews current settings.','Click upper display with sound-producing settings; no repeatability law.')])
rows('DS Tom',[
([54,55],'control','Pitch is Hz; Color controls filter gain/cutoff, Tone level of resonant band-pass filters.','Inspect Hz Pitch, adjust Color/Tone separately with audible output; exact filter modes/coefficients ungraded.'),
([56],'control','Bend adjusts pitch envelope, Decay length and Volume level.','Set Bend nonzero and Volume audible, compare two Bend/Decay values.'),
([57],'control','Upper-half display click previews current settings.','Click upper display and compare note-trigger route only as U output obligation.')])
rows('DS Sampler',[
(['MX25:721:B003','MX25:721:B004'],'state','Dated Version 12: load owned sample by dropping on upper display; Start changes sample start and Length playback length. Current HTML omits this profile; exact target availability/behavior U.','Owned validated sample S, drop upper display; set accepted distinct Start/Length and retain sample reference and displayed region.'),
(['MX25:721:B005'],'control','Dated Version 12: Tune spans -48 to +48 semitones; Loop toggles sample looping. No pitch/resampling/loop-boundary formula follows.','Loaded S and audible output; inspect Tune -48/0/+48 and Loop off/on with nonzero playable region.'),
(['MX25:721:B006'],'control','Dated Version 12: Decay controls sample amplitude decay, Shaper distortion and Volume overall level.','Loaded S, audible nonzero Volume; compare Decay and Shaper independently, preserving positive baseline.')], grade='D12-2025')
rows('Align Delay',[
([60,61,62,63,64],'control','Delay Mode choices Time, Samples and Distance use ms, samples and meters/feet. No time-distance-speed or sample-rounding law is supplied.','Distinct stereo owned input, choose each mode and accepted nonzero delays; inspect units, do not equate unit switches with a conversion formula.'),
([65],'control','Distance supports Temperature with Celsius/Fahrenheit choice and temperature slider.','Select Distance, inspect temperature controls and change two accepted values; no atmospheric equation or exact latency oracle.'),
([66],'state','Link L/R applies left settings to right; right slider is grayed and left edits both.','Set accepted differing L/R delays, enable Link, change left, inspect both values/right ineligibility; unlink state retention U.')])
# Mapping clauses are separate per device, with each device's own evidence.
def mapping(name, refs):
 a, b, c, d, e, f=refs
 rows(name,[
 ([a, b, c],'state','Map then parameter click assigns target; Multimap exposes up to eight mappings and Unmap removes selected assignment.','Use owned target with known eligible nonzero parameter response; assign eight distinct eligible targets, inspect ninth eligibility, unmap one. Exact replacement/limit-error policy U.'),
 ([d, e, f],'state','Modulation permits manual base-value edits with Bipolar centered/Unipolar one-direction depth; Remote Control owns mapped value and prevents manual edit, with Min/Max range. Documentary default Modulation is not a target constructor proof.','Map active source to valid target with nonzero amount; compare Mod/Remote, manual edit, polarity and Min/Max; exact parameter codec/automation precedence U.')])
mapping('Envelope Follower',[69,70,71,72,73,74])
rows('Envelope Follower',[
([68,75],'signal-obligation','Input amplitude produces mapped envelope; Gain controls input level and Rise/Fall smooth attack/release.','Use stepped main audio A, mapped eligible target with nonzero depth and visible positive response; vary Gain/Rise/Fall separately, no envelope formula.'),
([76],'control','Envelope Delay supports time and synchronized beat divisions.','Active envelope/target, inspect delay modes/units and two accepted nonzero settings at 120 BPM.'),
([77,78,79,80],'state','Expanded Audio Routing and Sidechain select external track plus Pre FX/Post FX/Post Mixer and Rack channel; Direct/S.C. meters show respective inputs.','Distinct stepped A main/B donor, source track active and routable; enable Sidechain and inspect each tap/channel/meter; donor is not assumed audible admission.'),
([81],'signal-obligation','Sidechain Mix 0% uses track input only; 100% external donor only for envelope generation.','Mapped positive response from each A/B individually, nonzero amount/gain; compare Mix 0/50/100 with separate donor/main mute; retain active wet/output target baseline.')])
mapping('LFO',[84,85,86,87,88,89])
rows('LFO',[
([90,91],'control','Nine waves: Sine, Up, Down, Triangle, Square, Random, Bin, Stray, Glider. Shape unavailable for Random/Bin/Stray/Glider; Steps unavailable for Random/Bin/Square; Steps up to 24.','Enumerate all nine, inspect Shape/Steps eligibility and Steps 0/interior/24 only where offered; no claim disabled values frozen.'),
([92],'signal-obligation','Jitter randomizes output; Smooth softens output changes including jitter.','Active mapping/nonzero depth, compare Jitter 0/nonzero then Smooth low/high; RNG/distribution/filter law U.'),
([93,94],'control','Rate uses Hz or beat divisions; Hz permits ×10. Depth 0% applies no modulation,100% maximum.','Set active mapping and nonzero source/depth positive baseline; inspect Hz/sync/×10, then Depth 0/100; exact target movement/time law U.'),
([95,96],'control','Offset centers at 0 and shifts output upward/downward; Phase spans 0-100% cycle.','Active Sine mapping, inspect Offset signs and Phase 0/50/100; exact normalized units or phase samples U.'),
([97,98],'state','Hold freezes current LFO output; release restarts from held value. R retriggers at Phase position.','Active mapped nonzero Sine, Hold during mid-cycle then release, R with Phase 25%; displayed/target state only, sample/event tolerance U.')])
mapping('Shaper',[101,102,103,104,105,106])
rows('Shaper',[
([100,107,108],'state','Breakpoint envelope generates mapping data. Click creates, Alt Win/Option Mac segment drag curves, Shift-click deletes; Clear removes envelope; six presets replace it.','Active nonzero mapping; create three points, curve segment, delete middle, select each preset then Clear. Exact endpoints/minimum point count/curve formula U.'),
([109,110],'control','Grid controls divisions and Snap moves created/repositioned points to nearest line; small display shows output.','Set explicit grid, Snap off/on, create away from grid tie; inspect point position/display, no tie/zoom/sampling law.'),
([111,113],'signal-obligation','Jitter randomizes, Smooth softens output, Offset shifts center relative to0.','Nonflat envelope, mapped positive response/nonzero depth, compare Jitter 0/nonzero, Smooth low/high and Offset signs; no distribution/curve tolerance.'),
([112],'control','Phase spans 0-100%; R retriggers at Phase and is disabled in Sync time mode.','Inspect Phase endpoints and R in Hz versus Sync; no implicit reset on mode switch.'),
([114,115,116,117,118,119],'state','Trigger modes Loop continuously at Rate,1-Shot via mappable T, Manual scrub control; Rate Hz/sync. Depth 0 none,100 maximum.','Nonflat envelope/nonzero mapped target, compare three trigger modes with accepted rate, T and Manual0/interior/end, then Depth 0 with active 100 baseline; clock law U.')])
mapping('Envelope MIDI',[123,124,125,126,127,128])
rows('Envelope MIDI',[
([122,129,130,131,132,133,134],'state','ADSR mapping modes Free(note), Sync(division), Loop(Global Time), Echo(Time/Feedback); LED flashes each trigger.','Mapped positive target, accepted nonzero Amount, send note48 then60; select each mode and explicit accepted rate/feedback, inspect controls/LED without exact scheduler oracle.'),
([135,136],'control','Global Time1.00 matches ADSR timing; above stretches/below compresses proportionally. Amount 0 none,100 maximum.','ADSR nonzero, mapped active target; inspect Global Time0.5/1/2 and Amount 0/100 after positive baseline. Display scaling only; rates/clamps/time tolerance U.'),
([137,138,139,140],'control','Attack/Decay/Sustain/Release and ADR Slope edit by values or display; Release returns envelope to0 after note release.','Set nonzero ADSR, inspect numeric/display handles and slopes; short/long note and release mid-attack output remain ungraded.'),
([141],'signal-obligation','Velocity toggle scales envelope peak with incoming velocity.','Amount/depth nonzero, two notes velocity32/96 with Velocity off/on; retain positive envelope baseline and no numeric scaling beyond documentary direction.'),
([142],'state','Sustain on holds level while note held then Release; off is one-shot Attack/Decay/Release regardless held duration.','Active mapped envelope, nonzero sustain/release, compare held/released notes with Sustain off/on; exact retrigger/overlap law U.')])
rows('Expression Control',[
([144,145,146],'state','Five source tabs each select Velocity, Modwheel, Pitchbend, Pressure, Keytrack, Expression, Random, Increment, Slide, Sustain; Map then target click assigns selected source.','Enumerate ten sources on all five tabs, map distinct valid targets and send separated source events; no modern controls transferred to Legacy.'),
([147,148,149],'state','Modulate permits base edits and bipolar/unipolar ranges; Remote owns parameter and exposes Min/Max. Modulate OutputRange Max represents maximum input.','Active expression source and nonzero mapped target; compare Modulate/Remote manual-edit eligibility and polarity/range controls; parameter combination law U.'),
([150,151,152],'control','Linear curve has two points/Curve A; S-curve three, upperA/lowerB and linked inverse editing viaA; Min/Max and S-middleX/Y can edit with display.','Select both curve types, changeA/B/link and middleX/Y where offered; no interpolation/codec equation.'),
([153],'state','Increment activates1-32Steps per cycle; Stop resets count so first note after restart outputs configured minimum.','Mapped target min distinct max, Increment Steps 1/4/32, send more than one cycle then Stop/restart/note; exact increment schedule and simultaneous notes U.'),
([154],'signal-obligation','Random activates Amount and changes deviation each note trigger; no stream/seed/distribution guaranteed.','Random Amount 0/nonzero after active response, repeat eight notes; no forced difference or equality across repeats.'),
([155,156],'control','Smoothing chooses linear/logarithmic; Rise/Fall times0-1000ms reach new rising/falling value.','Source changes with mapped nonzero depth; inspect smoothing types and0/500/1000ms endpoints; exact curve/granularity/latency U.')])
rows('Expression Control Legacy',[
(['MX25:731:B003','MX25:731:B004'],'state','Dated Version 12: Velocity, ModulationWheel, PitchBend, Aftertouch and Keytrack each map to one destination via Map then target click. This is Legacy, not current ten-source/five-tab device.','Select actual Legacy, inspect five named sources and map each separately to valid target; current Slide/Random/Increment controls not presumed.'),
(['MX25:731:B005','MX25:731:B006'],'control','Dated Version 12: each mapping has independent Min/Max intensity and Log/Lin shape.','Two Legacy source mappings with nonzero ranges; vary Min/Max then Log/Lin individually, no curve formula.'),
(['MX25:731:B007','MX25:731:B008'],'control','Dated Version 12: Rise/Fall smooth envelope attack/release; Output displays per-mapping output.','Send stepped global controller with active mapping, compare Rise/Fall accepted settings and read Output; no MIDI-to-parameter codec.'),
(['MX25:730:B001'],'state','Dated Version 12 says Live 11 Sets containing Expression Control load renamed Expression Control Legacy. Exact target migration and all-version parity remain U.','Requires separately version-proven Live 11 Set, absent here; inspect actual loaded identity and offered upgrade/replacement only in future owned copy. No existing AMXD proves old-Set behavior.')], grade='D12-2025')
rows('MIDI Monitor',[
([158,159,160],'control','Note view displays incoming notes, root/related chords on keyboard and velocity; chord recognition rules not specified.','Send single note60 and known48/52/55 chord with velocity32/96; inspect view fields without asserting chord algorithm/name/spelling.'),
([161],'state','Flow lists incoming notes and controller data continuously; Freeze pauses/unpauses display and Clear empties it.','Send alternating note, bend, aftertouch; freeze, send more, clear, unfreeze; exact retention/order, Freeze+Clear interactions and MIDI pass-through U.'),
([162],'control','MPE view lists incoming note, velocity, slide, pressure and per-note pitch streams.','Two identified notes with distinct expression, inspect MPE view; no codec, time resolution, buffer limit or voice-label oracle.')])
rows('MPE Control',[
([164,167,168],'control','Press, Slide, NotePB sources independently enable and transform MPE; source selection foregrounds curve. Documented default sources on is not constructor proof.','Two-note expression source fixture; select and enable/disable each source separately, recording actual routed events/output as U.'),
([169,170,171,172,173],'control','Linear(two points) or S(three) curves allow Min/Max, Curve and display editing; S middle X/Y and unlinkable two segment controls.','Inspect each curve type/source, change endpoints andS midpoint/link; no numeric curve/rounding rule.'),
([174,175],'control','Advanced panel exposes per-source Smooth and independent Rise/Fall plus source-dependent options.','Expand and inspect each source; toggle Smooth with distinct nonzero Rise/Fall and event changes. Exact smoothing math/order U.'),
([177,178,179],'control','Press Default supplies value to non-MPE notes; Swap to Slide redirects pressure; Press to AT converts to monophonic aftertouch.','MPE and non-MPE note fixtures, actual compatible downstream; inspect Default, Swap, AT and future message effects, without polyphonic reduction/priority codec.'),
([181,182,183],'state','Slide CC74 offers Default, Centered and Abs/Rel/Ons. Rel starts midrange and changes with subsequent sweep; Ons updates only at Note On and disables smoothing.','Two distinct onset Slide values and later sweeps, compare modes; inspect Ons smoothing ineligibility and centered control, no normalization equation.'),
([184],'control','Slide to Mod converts to ModWheel CC1 for non-MPE instruments.','Send distinct per-note Slide events to declared compatible target with toggleoff/on; exact channel/reduction/order/messages remain U.'),
([186,187,188],'control','NotePB Pitch Range adjusts controller/instrument range relationship; manual gives2x for ±48 controller/±24 instrument. NotePB to PB converts to standard pitch bend.','Retain controller/instrument declared ranges, inspectPitch Range and conversiontoggle with two held notes; preserve manualexample only, no scaling/divisor/clip law or priorityoracle.')])
rows('Note Echo',[
([190,191,192,193],'control','Creates MIDI note echoes with decreasing velocity; Sync divisions count sixteenths(4=quarter); off usesms; DelayTime percentage adjusts fraction.','Active MIDI path and audible compatible instrument, Delay/Fback nonzero; inspectSync 4 vs ms and percentage changes, exacteventrounding U.'),
([194],'state','Input Thru passes original plus echoes;Mute removes original leaving echoes.','Single note with nonzero audible echo baseline then compareThru/Mute; exactnote-off, original MPE andscheduling U.'),
([195,196],'control','Pitch transposes each repeat;Delay controls echo velocity and Fback return amount.','Distinct nonzero Pitch/Delay/Fback, one note then two overlapping notes; no velocity recurrence, echo count orfeedbackstability formula.'),
([197,198],'state','MPE on echoes incoming expression with notes;off filters MPE. On enables Press/Slide/NotePBfeedback;below100% progressively decays repeatedMPE.','Two distinctnotes/expression, MPE off/on, feedback 50/100 withactive echoes; no exact channel allocation, event pairing ordecay equation.')])
mapping('Shaper MIDI',[201,202,203,204,205,206])
rows('Shaper MIDI',[
([200,207,208,209],'state','MIDI notes trigger envelope;click creates point, Ctrl Win/Cmd Mac creates only one sustain point, Alt/Option curves, Shift-click deletes;Clear and six presets available. Sustainpoint holds while note held.','Active nonflat mapped envelope;create points andone sustain point, attempt second, curve/delete/preset/Clear separately;no second point replacement/refusaloracle.'),
([210,211],'control','Grid/Snap nearestline editing;small outputdisplay andtriggerLED.','Explicit grid, point away from tie, Snap off/on, reposition;send notes andinspect LED. No pixel/tie/trigger deadline.'),
([212,214],'signal-obligation','Jitter randomizes, Smooth softens, Offset sets center shift around 0.','Active nonzero mapped depth, nonflat shape;compareJitter 0/nonzero, Smooth low/high, Offset signs, withpaired positive baseline.'),
([213],'signal-obligation','Velocity 0% has no velocity effect;larger values scale lower/higher note velocities down/up.','Two notes velocity32/96 andnonzero depth;compareVelocity 0/50/100 only if offered, positivebaseline;no exactamplitude or message formula.'),
([215,216,217],'state','Loop repeats while note held at Rate and bypasses sustain point;Rate Hz/sync;Depth 0 none,100 maximum.','Envelope withsustain point, held note, Loop off/on, Rate Hz/sync;Depth 0 after 100 active baseline. ExactNote Off/release/clockU.'),
([218],'control','Echo feedback control governs envelope repetitions;Time sets echo interval.','NonzeroEcho/Time andmapped depth, one shortthenheld note;compareaccepted feedback/time values, no echo equation/tail deadline.')])

states={
'DS Clang':'Clave on with Repeat nonzero, Tone A/B and Noise audible, Filter interior, nonzero Decay/Volume.',
'DS Clap':'Sloppy/Tail nonzero, Spread 50%, Tone interior, nonzero Decay/Volume.',
'DS Cymbal':'Tone interior, Pitch accepted, Decay/Volume nonzero;separated preview andnotes.',
'DS FM':'Amnt/Feedb. nonzero, Mod interior, Tone interior, Decay/Volume audible.',
'DS HH':'Pink Noise,24 dB pitchedfilter, Attack nonzero, Tone interior, Decay/Volume audible.',
'DS Kick':'Pitch 50 Hz ifaccepted, Drive/OT/Env nonzero, Click on, Attack/Decay/Volume audible.',
'DS Sampler':'Owned sample S, Start interior, Length nonzero, Loop on, Tune +12, Shaper nonzero, Decay/Volume audible.',
'DS Snare':'Color/Tone audible, noise Band Pass, nonzero Decay/Volume.',
'DS Tom':'Pitch 100 Hz ifaccepted, Color/Tone/Bend nonzero, Decay/Volume audible.',
'Align Delay':'Distinct stereo input, nonzero different L/R delays, Distance Mode, temperature explicit, Link off.',
'Envelope Follower':'Stepped main A anddistinct donor B, Sidechain on Mix 50%, nonzero Gain/Rise/Fall/Delay, active mapped target/nonzeroamount.',
'LFO':'Sine, Rate 1 Hz ifaccepted, Depth nonzero, Phase 25%, nonzeroJitter/Smooth, active eligible mapped target.',
'Shaper':'Threepointnonflat shape, nonzero Depth, mapped target, Loop andnonzero Rate, Phase 25%, Jitter/Smooth nonzero.',
'Envelope MIDI':'Nonzero ADSR/Amount, mapped target, Sustain on, Velocity on, Echo mode withnonzero Env Feedback/Time.',
'Expression Control':'Five source tabs, IncrementSteps 4, Random Amount nonzero, active mapped targets, nonzero Rise/Fall, Modulate.',
'Expression Control Legacy':'ActualLegacyidentity, five global expression mappings, distinctMin/Max, Log shape, nonzero Rise/Fall.',
'MIDI Monitor':'Note/Flow/MPEviews, two held noteswithdistinct expression, Freeze off, retained stream.',
'MPE Control':'Three MPE sources on, S-curves distinct, Slide Rel, Smooth nonzero, conversion toggles explicit, two held notes.',
'Note Echo':'Sync 4, nonzero Delay/Fback/Pitch, Input Thru, MPE on, Press/Slide/NotePBfeedback 50%, two held notes.',
'Shaper MIDI':'Nonflatshapeonesustain point, Loop on, nonzero Depth/Rate/Echo/Time, Velocity nonzero, active mapped target.'}
# Explicit device states are future setup choices; accepted values still require evidence.
steps=[
('BOUNDARY','boundary','Inspect named documented endpoints then adjacent/out-of-range numeric text and mode eligibility; mapping devices add eighth then ninth target; input devices two overlapping notes.','Control domains, clamp/reject/rounding, minimum lengths, voice/message limits andconflictingmapped targets U.'),
('AUTOMATION','automation','Choose two distinct accepted named control values, record bar 1-to-2 change;manual override/re-enable, clip envelope andrack macro separately;edit mapping target while active.','Eligibility, scaling, smoothing, ownerprecedence andmappingtarget lifetime U.'),
('TRANSPORT','transport','With input/modulation/held notes active, Stop/Start/seek/loop at 120 then 90 BPM;repeat held note across boundary.','Reset/retriggerphase, increment exceptions beyonddocumented stopcase, echo/notes/tails andsame-time ordering U.'),
('PERSISTENCE','persistence','Save owned preset/Set, reopen andcompare controls, mappingtarget identities, curve/stream/loop state. Relocate AMXD andsample S if applicable in separate copies.','Savedfieldset, reference repair, migration, random/tail/buffer retention andmissingmedia U.'),
('UNDO','undo-redo','Change two named controls andone mode/mapping/envelope, Undo/Redo each;remove/reinsertdevice in separate trial.','Historygrouping, parameter/target/file restoration andtransient state U.'),
('MALFORMED','malformed','Disposable AMXD copy truncated;missing dependency;invalid numeric text or duplicate/unknown saved parameter only if correspondingcontrols exist.','Refusal/repair, error UI, partial state, priorstate preservation andcrashrecovery U.'),
('CANCEL','cancellation','Begin dirty editor/control edit then Escape;cancel preset/source/SaveAs/mappinggesture at recorded stages where offered.','Cancelavailability, rollback/atomicity, selection/files/dirtyflags andhistoryscope U.'),
('TEARDOWN','teardown','During active input/held notes/mappedmodulation/echo, unmap/delete target, bypass/remove device, disconnect source, close editor/Set in separate trials.','Final note-offs, mappingownership restoration, pendingevents/tails/resources andcleanup U.'),
('RATE','sample-rate','Repeat retained inputs at 44.1/48/96 kHz,64/256 frames and 90/120 BPM;stopped/active ratechange andreal-time/offline separately if supported.','Supportedrates/changes, latency/block invariance, curves/timing andperformancecriteria U.'),
('ROUTING','routing','Change upstream/downstream track/Rack/channel, target manual/automated state andexternal donor where actually offered;two independent MPE notes, tuning active if applicable.','Audio/MIDI pass-through, sidechain admission, disabledpath, tuning/MPE/channelcodec andmappedparameterinteraction U.')]
for d in INV:
 name=d['name'];key=d['id'].removeprefix('SURF-MAX-');file=next(f for f in json.loads((P/'package-identities.json').read_text()) if f['id']==d['id'])
 rid=f'REQ-MXD-{key}-FILE'
 REQ.append({'id':rid,'device':name,'surface':d['id'],'provenance':'Dpkg','target_applicability':'U','contract':'Retained inventory/file identity only: '+str(file['bytes'])+' bytes, SHA-256 '+file['sha256']+'. AMXD contents unparsed; no control/default/DSP/API/load behavior inferred.','source_id':d['id'],'source_blocks':[]})
 CASES.append({'id':f'MXD-{key}-FILE','requirements':[rid],'device':name,'kind':'package','provenance':'Dpkg','fixture':'fixtures.json#MXD-F0','setup_and_action':'Compare frozen inventory record and exact external AMXD path, size/hash/prefix in package-identities.json without parsing/loading the patch.','documentary_expected':REQ[-1]['contract'],'documentary_comparator':'Exact inventory/file byte count/hash/prefix only; no runtime proof.','expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':[]})
 rid=f'REQ-MXD-{key}-LIFECYCLE'
 REQ.append({'id':rid,'device':name,'surface':d['id'],'provenance':'U','target_applicability':'U','contract':'Required numerical signal/MIDI/API, clock/automation/history/persistence, error/cancel/routing/teardown outcomes remain unknown; ten device-specific cases below are obligations, not coverage passes.','source_id':None,'source_blocks':[]})
 for suffix, kind, action, unknown in steps:
  CASES.append({'id':f'MXD-{key}-U-{suffix}','requirements':[rid],'device':name,'kind':kind,'provenance':'U','fixture':'fixtures.json#MXD-F0','setup_and_action':states[name]+' '+action,'documentary_expected':None,'documentary_comparator':None,'expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':[],'unknown':unknown})

write('requirements.json', REQ);write('cases.json', CASES)
write('fixtures.json',{'id':'MXD-F0','status':'Future finite analyst input recipes only; no patch/PCM/MIDI/reference render executed or supplied','common':['Correct actually offered inventoried profile, knownsupportededition, owned disposableSet/preset/AMXD copies. Exact12.4.3 identity andsupport unknown; no Maxinstallation or originalexecution here.','Future audioA:retained4second dualmono multitone100/440/1000/6000Hz, componentpeak0.02 at48kHz;B distinct330Hz burst at1-2 and3-4seconds fordonor. Stimulusdefinitions only, not DSP equations.','Future notes:48onbeat1,60onbeat2, offbeats3/4;velocities32/96 in independenttrials. Separate globalWheel/Bend/Aftertouch/CCand per-noteMPEpress/slide/bend with identifiedcodec; alloutputoraclesU.','Owned sample S forDSSampler:independentlyvalidated2secondWAV withdistincttransient+sustain, byte/rate/channelidentity retained beforeuse;no samplefixturesupplied.','Mappings require independentlyeligible automatabletarget withnonzero base/amount andretainedvisiblepositive response. Isolate competingmaps/macros/automation; do not assume names/targetranges or genericparameter law.'],'positive_signal_guard':'Enable relevant device/section/source/route;nonzero input/note/media, modulation/echo/feedbackamount andgain, unmuted output. Establish pairedactive nonzero processed/targetresponse before any no-effect/boundarycase. Missingpatch/control/dependency orfailedbaseline remainsinconclusive/U. Random output equality orforced change is never a comparator.','device_states':states,'original_execution':False,'candidate_comparison':False})
sources=[json.loads((P/'source.json').read_text()), json.loads((P/'source-dated-pdf.json').read_text())]
for n in ['devices.json','manual-toc.json']:
 b=(P.parent/'inventory'/n).read_bytes();sources.append({'id':'INVENTORY-'+n.upper().replace('.','-'),'file':'../inventory/'+n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'limit':'Frozen discovery only'})
write('sources.json', sources)
counts={'requirements':len(REQ),'requirement_provenance':dict(Counter(r['provenance'] for r in REQ)),'cases':len(CASES),'case_provenance':dict(Counter(c['provenance'] for c in CASES)),'profiles':20,'target_graded':0}
write('counts.json', counts)
assert len({r['id'] for r in REQ})==len(REQ) and len({c['id'] for c in CASES})==len(CASES)
assert {r['id'] for r in REQ}=={r for c in CASES for r in c['requirements']}
link='../../analysis/ableton-live-12.4.3/full-spec-v1/max-devices/'
spec='''---
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

Use [finite future inputs](REPLACE_LINKfixtures.json), actual accepted modes,
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

'''.replace('REPLACE_LINK', link)
for d in INV:
 name=d['name'];key=d['id'].removeprefix('SURF-MAX-');own=[r for r in REQ if r['device']==name]
 spec+=f'## {name}\n\nSurface `{d["id"]}`. Lifecycle setup: {states[name]}\n\n| Requirement | Contract and limits | Evidence/provenance |\n| --- | --- | --- |\n'
 for r in own:
  evidence=', '.join('`'+b+'`' for b in r['source_blocks']) if r['source_blocks'] else '[Package ledger]('+link+'package-identities.json)' if r['provenance']=='Dpkg' else 'Required unknown'
  spec+=f'| {r["id"]} | {r["contract"]} | {r["provenance"]};target U; {evidence} |\n'
spec+='''
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

[Requirements](REPLACE_LINKrequirements.json), [cases](REPLACE_LINKcases.json) and
[counts](REPLACE_LINKcounts.json) retain exact per-profile source/case relationships.
There are REQCOUNT requirements: GRADECOUNT. CASECOUNT unexecuted cases contain
CASEGRADECOUNT. Zero exact-target grades. The 200 lifecycle cases and numerous
signal obligations are not complete control/event-combination coverage.

| Device | D12 / D12-2025 / Dpkg / U requirements | Cases |
| --- | --- | --- |
'''.replace('REPLACE_LINK', link).replace('REQCOUNT', str(len(REQ))).replace('CASEGRADECOUNT',', '.join(f'{v} {k}' for k, v in Counter(c['provenance'] for c in CASES).items())).replace('GRADECOUNT',', '.join(f'{v} {k}' for k, v in Counter(r['provenance'] for r in REQ).items())).replace('CASECOUNT', str(len(CASES)))
for d in INV:
 own=[r for r in REQ if r['device']==d['name']];c=Counter(r['provenance'] for r in own)
 spec+=f'| {d["name"]} | {c["D12"]} / {c["D12-2025"]} / {c["Dpkg"]} / {c["U"]} | {sum(x["device"]==d["name"] for x in CASES)} |\n'
spec+='''
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

[Source ledger](REPLACE_LINKsources.json) pins two documentary revisions and frozen
inventory/TOC. Current official [Max devices chapter](https://www.ableton.com/en/live-manual/12/max-for-live-devices/),
captured 2026-10-19,299,403 bytes, SHA-256
`b95a0d3ed3d7217505437a0d7d65de68d37e0f894d27e9869122fbfb89728a46`.
[218 blocks](REPLACE_LINKmanual-blocks.json) retain exact HTML lines and full
heading context through 33.3.6; sidebar/footer excluded.
[HTML](REPLACE_LINKmanual-max-devices-2026-10-19.html) is immutable source.

Official [dated English Version 12 PDF](https://cdn-resources.ableton.com/resources/pdfs/live-manual/12/2025-06-02/live12-manual-en.pdf),
76,333,838 bytes, SHA-256
`42fbd3794df0d69aaf522aea589bf08dd3dc8db3eb0e135cab041093875db976`.
[Metadata](REPLACE_LINKsource-dated-pdf.json) and [retained PDF](REPLACE_LINKmanual-12-2025-06-02.pdf)
pin capture identity; only physical pages 721/730/731 support this packet.
[15 dated blocks](REPLACE_LINKdated-blocks.json) retain exact page/text-line ranges,
including headings/captions and one separately labelled migration paragraph.
Page text is derived with existing `pdftotext`; diagrams were not inspected.
No other dated-PDF device prose is imported into current requirements.

[Twenty AMXD identities](REPLACE_LINKpackage-identities.json) retain exact external
file paths, byte counts, hashes and 16-byte prefixes matching the frozen inventory.
Contents were not parsed/copied into contracts or executed. Reproduction depends
on those retained external paths; the manual and package identity establish no
arbitrary API/patch or complete-product behavior.
[Author manifest](REPLACE_LINKmanifest-author-r1.json) freezes payloads/canonical
snapshots; [validation](REPLACE_LINKvalidation-author-r1.json) checks hashes, locators,
requirements/cases, browser discovery, links and whitespace only. No handoff is
published; all twenty profiles remain partial and pending independent review.
'''.replace('REPLACE_LINK', link)
(ROOT/'wiki/specs/max-for-live-devices.md').write_text(spec)
research='''---
id: RES-MAX-FOR-LIVE-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Twenty shipped Max-device source profiles

## Scope and evidence selection

This partial F-06 packet supports the
[canonical device draft](../specs/max-for-live-devices.md) under
[coverage design](full-live-specification-design.md). The frozen inventory owns
twenty max-device records, distinct from five templates and two MIDI Tools.
[Max host/templates](max-for-live-hosting.md) owns its workflows; the tools remain
[MIDI editing](midi-editing-tools.md). No host-generic clause substitutes for any
of these twenty device profiles. No Max patch/original/candidate ran, no tooling
was installed and no broad binary analysis was launched.

The exact inventory TOC URL selected current English
`/en/live-manual/12/max-for-live-devices/`. No existing capture of that chapter
was found. [Source metadata](REPLACE_LINKsource.json) retains one capture of
299,403 bytes, SHA-256
`b95a0d3ed3d7217505437a0d7d65de68d37e0f894d27e9869122fbfb89728a46`.
[218 paragraph/heading blocks](REPLACE_LINKmanual-blocks.json) preserve HTML lines
and full heading contexts through 33.3.6, excluding sidebar/footer. Version 12
exact 12.4.3 applicability remains U. Figures were not separately inspected.

## Two profiles omitted by current English headings

Current HTML has 18 individual profiles; installed inventory has 20, nine of which
are DS instruments. DS Sampler and Expression Control Legacy are absent from
current English headings. Bounded official-source search found both named in
an official dated English Version 12 PDF under 2025-06-02 path. The entire immutable
PDF was retained because the web reader rejected its 76,333,838-byte size; the
existing `pdftotext` extracted only physical pages 721/730/731. No dependency was
installed. Exact SHA-256 is
`42fbd3794df0d69aaf522aea589bf08dd3dc8db3eb0e135cab041093875db976` in
[metadata](REPLACE_LINKsource-dated-pdf.json).

[15 dated blocks](REPLACE_LINKdated-blocks.json) comprise DS Sampler 6
heading/caption/paragraph blocks on p721, Expression Control Legacy 8 on p731 and
one separately labelled current-to-Legacy migration paragraph on p730. The p731
text preceding the Legacy heading belongs to current Expression Control and is
excluded, preventing Random/Increment/smoothing-source contamination. Source
revision mismatch is explicit D12-2025/target-U, not silently current-build proof.
The p730 Live 11-Set migration statement has no retained old Set/target output.

## Individual device interpretation

The draft assigns each device its own controls/modes/state/finite cases from its
own paragraphs. Nine DS profiles retain distinct tone/noise/filter/pitch/envelope
roles. DS Sampler sample-drop is not inferred as a preview action. Align Delay
keeps unit/temperature/Link UI without deriving sound-speed or frame arithmetic.
Envelope Follower carries main-versus-donor, taps/meters/mix and mapped envelope;
LFO carries waveform exclusions, Depth/Hold/Phase; Shaper its editor/trigger modes;
Envelope MIDI its ADSR/Loop/Sync/Echo/Sustain/velocity roles. Current Expression
Control differs from Legacy's five global-source/one-target-per-source document.
MIDI Monitor display Freeze is not a MIDI-pass-through law. MPE Control keeps
source-specific curves/conversion/modes and the unexpanded 2x example. Note Echo
retains time/Input/MPE distinction; Shaper MIDI its note/sustain/loop/velocity and
echo envelope behavior. Numerical transfer/curve/MIDI/RNG/timing laws stay U.

[Package identities](REPLACE_LINKpackage-identities.json) were rehashed at the
exact twenty inventoried AMXD paths, checking sizes and 16-byte prefixes. These
bounded reads supply identity only. No patch content/control graph was parsed,
no original algorithm was recovered/executed and no field/default/API behavior
was inferred. External files are not duplicated here; retention depends on
recorded paths and checksums. The two manual versions are separate pinned sources.

## Packet, review and remaining evidence

[Requirements](REPLACE_LINKrequirements.json), [cases](REPLACE_LINKcases.json)
and [counts](REPLACE_LINKcounts.json) retain exact device/source links.
Each device has one file-identity clause and one U lifecycle clause with ten
separate, device-specific setup cases, alongside its supported documentary rows.
All exact-target expectations/comparisons are null, U, unexecuted. Documentary
control/state checks grade no application; acoustic/timing obligations have no
numeric comparator. [Future inputs](REPLACE_LINKfixtures.json) require accepted
controls, valid notes/media, mapping targets and paired active positive baselines.
Missing dependencies, absent controls or silent source never yields pass.

Exact-version parity, current menu/constructor defaults, AMXD/API protocols,
all DSP/filter/oscillator/envelope/curve/random/message codecs, voice allocation,
automation/transport/rate/latency, reference/persistence/undo/malformed/cancel/
dependency-loss/routing/teardown and complete accessibility remain required U.
All twenty profiles are partial. Source-supported eligibility/role prose and
browser discovery do not close combinations or entire families.

[Manifest](REPLACE_LINKmanifest-author-r1.json) freezes exact sources/payloads
and both canonical snapshots. [Validation](REPLACE_LINKvalidation-author-r1.json)
checks source/file/hash identity, paragraph locators, counts/case kinds, null target
oracles, all normative IDs through existing `tools/spec_browser.py`, local links,
metadata and untracked-aware whitespace. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/max-devices/validate.py`.
Separate semantic review is pending. Root owns shared catalogs, coverage, questions,
execution plan and append-only log; no shared surface or released handoff is edited.
'''.replace('REPLACE_LINK', link)
(ROOT/'wiki/research/max-for-live-devices.md').write_text(research)
print(json.dumps(counts, indent=2))
