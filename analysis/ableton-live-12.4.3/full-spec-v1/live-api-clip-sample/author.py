"""Bounded documentary author data; creates this packet only when explicitly --write.
No Live, Max, API, patch, JavaScript, media or example execution.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
INV=P.parent/'max-api'

def load(p):return json.loads(p.read_text())
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=sha256(b).hexdigest())

# Each line is one directly declared member's particular documentary predicate.
# These are prose interpretations, not callable signatures or target oracles.
ROLES={
'Clip':'''view|A get-only child refers to the clip's Clip.View; no independent view mutation is declared by this child.
available_warp_modes|For an audio clip, the read-only list contains indexes of available Warp Modes, rather than a promise that every published mode is supported.
color|The integer is a packed RGB color; setting it chooses a nearest color in the clip chooser. Packing and nearest-choice prose is not a target color metric or tie rule.
color_index|An integer clip color index is get/set/observable; the declaration supplies no complete index palette.
end_marker|A beat-valued end marker is independent of loop state and cannot be set earlier than the start marker; refusal/error details are omitted.
end_time|The read/observable end time has separate Session Loop End versus End Marker and Arrangement right-edge contexts.
gain|An audio-only float gain is documented on a normalized zero-to-one domain; it is not a new fader-to-amplitude law.
gain_display_string|For audio clips, a get-only symbol presents a gain display string; the example does not define locale, precision or formatting grammar.
file_path|For audio clips, a get-only symbol identifies the represented audio file location; this supplies no path normalization or file-access policy.
groove|A Groove-valued get/set/observable association is documented, with a since-Live11 note; object identity and removal semantics remain unproved.
has_envelopes|The read/observable boolean reports whether the clip has automation, without specifying serialized envelope ownership or scheduling.
has_groove|A get-only boolean reports a Groove association; the source does not make it an observable property.
is_session_clip|A get-only boolean identifies a Session clip; the source distinguishes Session from Arrangement membership.
is_arrangement_clip|A get-only boolean identifies an Arrangement clip, without declaring a clip-transfer operation.
is_take_lane_clip|A get-only boolean identifies Take Lane membership; the source explicitly also classifies Take Lane clips as Arrangement clips.
is_audio_clip|A get-only boolean distinguishes audio from MIDI clips using the published boolean convention.
is_midi_clip|The get-only boolean is described as opposite to is_audio_clip; it is not an input-conversion operation.
is_overdubbing|A read/observable boolean reports overdubbing; recording engine and note-merge laws remain separate.
is_playing|The source declares get/set access to a boolean that includes recording in the playing state; it does not declare observe or specify the setting transition.
is_recording|A read/observable boolean reports clip recording, without asserting captured media or note content.
is_triggered|A get-only boolean corresponds to a blinking Clip Launch button; it is distinct from already playing or recording.
launch_mode|A get/set/observable integer names Trigger, Gate, Toggle and Repeat in the current reference. Published indexes/default do not replace the finite launch owner.
launch_quantization|A get/set/observable integer names Global, None and listed bar/straight/triplet divisions. The reference indexes do not establish new launch-grid timing.
legato|A get/set/observable boolean corresponds to the Legato switch in Launch settings, not a derived playback-position rule.
length|Read-only length is loop length when looped and start-to-end distance otherwise, in beats; the source says it is not meaningful for unwarped audio.
loop_end|A get/set/observable float denotes loop end when looped and clip end otherwise; context-dependent units are described alongside loop_start.
loop_jump|Observe-only bang notification corresponds to crossing the loop-start position, including a possible projection into the loop; cadence and exact event payload remain unverified.
loop_start|A get/set/observable float denotes loop start or unlooped clip start. MIDI/warped clips use absolute clip beats; unwarped audio uses seconds from the first sample.
looping|The get/set/observable boolean enables looping; the source excludes looping of unwarped audio, without specifying invalid-write behavior.
muted|A get/set/observable boolean denotes the Clip Activator being off; this does not specify a sample-level mute ramp.
name|The source declares a symbol-valued get/set/observable name and gives no further grammar, maximum length or normalization law.
notes|For MIDI clips only, an observe-only bang signals that the note list changed, not a returned note collection or a complete event ordering protocol.
warp_markers|For audio clips, get returns a dictionary of sample_time and beat_time pairs while observe bangs on changes. The source includes an invisible final marker and interpolation context, retained under the existing Warp owner.
pitch_coarse|The audio-only get/set/observable integer describes semitone Transpose, with the published minus48-to48 range; this is not a sound or tuning oracle.
pitch_fine|The audio-only get/set/observable float describes cent Detune, with the published minus50-to49 range; rounding and audible pitch remain unknown here.
playing_position|The read/observable float uses absolute clip beats for MIDI/warped audio and seconds for unwarped audio; stopped position is described as zero, without callback cadence or timing tolerance.
playing_status|An observe-only bang signals a change in playing/trigger status, without a complete transition order or event count.
position|The access line says get/observe, but prose describes setting loop position while preserving loop length and equating its value to loop_start. This conflict remains Q-LCS-001; write capability is not silently added.
ram_mode|A get/set/observable boolean corresponds to an audio clip's RAM switch; no cache, memory or streaming architecture is mandated.
sample_length|A get-only integer describes the clip sample length in samples; this supplies no decoder or duration rounding law.
sample_rate|A get-only float reports the clip sample rate; exact source-rate conversion and valid contexts are not otherwise specified here.
signature_denominator|A get/set/observable integer is declared for the signature denominator; admissible values and invalid-write policy are not given.
signature_numerator|A get/set/observable integer is declared for the signature numerator; admissible values and invalid-write policy are not given.
start_marker|A beat-valued get/set/observable start marker is loop-independent and cannot be placed after the end marker; equality and error handling require evidence.
start_time|A read/observable float describes song-relative start beats, with different Arrangement offset and Session start roles. Session reporting concerns the track's currently playing clip and may be negative after offsets.
velocity_amount|A get/set/observable float describes how triggering-note velocity affects volume, with zero/no-effect and one/full-effect source endpoints; no interpolation or audio law is inferred.
warp_mode|The audio-only get/set/observable integer names Beats, Tones, Texture, Re-Pitch, Complex, REX and Complex Pro in this Clip reference; available_warp_modes and the existing finite owner remain necessary.
warping|The audio-only get/set/observable boolean corresponds to Warp enablement. The source warns of deferred setting and sequencing surprises; no private scheduling design or delay guarantee follows.
will_record_on_start|A get-only boolean has the joint MIDI-clip, triggered, track-armed and MIDI Arrangement Overdub prerequisites; a lone true flag does not prove recorded notes.
add_new_notes|For MIDI clips, the dictionary's notes list contains pitch:int, start_time:float and duration:float, with optional velocity, mute, probability, velocity_deviation and release_velocity fields. A list of newly added note IDs is described as returned; defaults/ranges stay current-source context, not storage or RNG laws.
add_warp_marker|For warped audio only, a marker dictionary has beat_time and optional sample_time floats. Omitted sample_time is described as preserving timing; explicit sample_time has sample-span, adjacent-order and segment-BPM constraints owned by Warp markers, not new target arithmetic here.
apply_note_modifications|For MIDI clips, a notes dictionary uses note records returned by get_notes_extended; a subset is admitted but the source says a batch containing any absent note is ignored. No partial-commit or event-order protocol is inferred.
clear_all_envelopes|The function removes all clip automation according to the source; no return value, undo transaction or sample-accurate side effect is declared.
clear_envelope|A device_parameter argument is documented as an id; its associated clip automation is removed. Valid parameter identity and envelope ownership must be established independently.
crop|Cropping uses the loop region when looped and start/end-marker region otherwise. This describes the API operation's region choice, not media rewrite bytes or an implementation of crop.
deselect_all_notes|For MIDI clips, deselects notes; the source suggests using it before replace_selected_notes and documents a named id-zero output. That referenced function is not declared in this selected Clip body and is not added to the denominator.
duplicate_loop|For MIDI clips, the loop doubles and notes/envelopes duplicate; for an unlooped clip the start/end range is used. Existing region/note/envelope owners retain exact transforms and boundaries.
duplicate_notes_by_id|For MIDI clips, accepts existing note IDs as a list or a dictionary with note_ids and optional destination_time:float/int and transposition_amount:int. Omitted destination follows the selected notes; exact insertion arithmetic is not derived here.
duplicate_region|For MIDI clips, region_start, region_length and destination_time are float/int arguments, with optional pitch:int and transposition_amount:int. The source describes pitch-minus1 as all pitches and transposition, without supplying a new region endpoint law.
fire|The function is described by the Clip Launch button role, without an argument or return declaration; existing launch/playback owners retain actual dispatch and timing.
get_all_notes_extended|For MIDI clips, returns a notes dictionary irrespective of markers/loop bounds. Each record has note_id, pitch, start_time, duration, velocity, mute, probability, velocity_deviation and release_velocity; an optional dictionary return-key list selects fields.
get_notes_by_id|For MIDI clips, existing IDs are passed as a list or a dictionary with note_ids and optional return field-selection list; the returned notes dictionary contains the published record fields. Missing-ID policy is not specified by this valid-ID precondition.
get_notes_extended|For MIDI clips, from_pitch:int, pitch_span:int, from_time:float and time_span:float select note starts; times are beats. The alternative dictionary uses these keys and optional return field list; returned records contain the published extended note fields.
get_selected_notes_extended|For MIDI clips, returns selected-note records with the published extended fields; an optional dictionary return field-list narrows the record keys. Selection identity and ordering remain separate questions.
move_playing_pos|A beats:float argument requests an unquantized relative jump, including negative/backward direction. Unwarped audio, recording audio and recording non-overdub MIDI are expressly excluded; no scheduling or jump-sample oracle is added.
move_warp_marker|beat_time:float identifies a marker and beat_time_distance:float requests its movement; exact constraints/conversions stay with the existing Warp owner.
quantize|quantization_grid:int and amount:float request quantization of all clip notes with song swing_amount taken into account; no grid enum, rounding, swing or numeric transform is inferred.
quantize_pitch|pitch:int, quantization_grid:int and amount:float apply the quantize role to one pitch; the source does not supply an independent quantization algorithm.
remove_notes_by_id|A list of IDs associated with existing notes requests deletion of those notes; note-ID lifetime, invalid batches and serialization are not derived from this valid-ID statement.
remove_notes_extended|from_pitch:int, pitch_span:int, from_time:float and time_span:float request deletion of notes whose starts lie in the area; times are beats, but edge inclusivity remains unresolved.
remove_warp_marker|beat_time:float identifies the marker requested for removal; marker-count, shadow and refusal constraints retain the existing Warp owner.
scrub|beat_time:float requests mouse-like scrubbing that respects Global Quantization and continues until stop_scrub. This is a dispatch role, without a new transport or sample-timing law.
select_all_notes|For MIDI clips, selects all notes independently of prior selection; the source documents a named id-zero output, not a new note-ID protocol.
select_notes_by_id|A list of note IDs selects associated notes; unlike other valid-ID descriptions, the source explicitly says nonexistent IDs do not print a warning/error. Actual result selection and message delivery remain target-U.
set_fire_button_state|state:bool represents a held clip-start button when true until false or another stop; it is not a proof of Gate/Toggle/Repeat timing or release policy.
stop|The function has the track-stop-button role only for this clip actually playing or recording; a merely triggered clip or another clip playing has no effect according to the source.
stop_scrub|The function stops an active scrub; inactive, deleted-object and transport transition policies are not specified.''' ,
'Clip.View':'''grid_is_triplet|A get/set boolean controls whether the displayed clip grid is triplet; observe access is not declared.
grid_quantization|A get/set integer controls displayed grid quantization; no enum or exact note-quantization law is supplied.
hide_envelope|The function hides the Envelopes box, without a declared parameter or return value.
select_envelope_parameter|A DeviceParameter argument selects that parameter in the Envelopes box; invalid or absent envelope parameters require separate evidence.
show_envelope|The function shows the Envelopes box; API return/callback and focus side effects remain unknown.
show_loop|Only when the clip is visible in Detail View, the function brings its current loop into view; this does not declare zoom geometry or a hidden-clip selection operation.''' ,
'Sample':'''beats_granulation_resolution|A get/set/observable integer selects Beats divisions from a bar through thirty-seconds or Transients, as listed; it does not specify a time-stretch algorithm.
beats_transient_envelope|A get/set/observable float describes the per-segment fade duration in Beats mode, with source endpoints fastest decay and no fade; no numeric envelope curve is established.
beats_transient_loop_mode|A get/set/observable integer selects Off, Forward or Back-and-Forth per-segment transient looping in Beats mode; no audio boundary algorithm follows.
complex_pro_envelope|A get/set/observable float controls the Envelope parameter in Complex Pro mode; range, units and signal law are omitted.
complex_pro_formants|A get/set/observable float controls the Formants parameter in Complex Pro mode; range, units and signal law are omitted.
end_marker|A get/set/observable integer denotes the sample end-marker position; the member body does not explicitly give units or bounds.
file_path|A read/observable unicode property identifies the sample file path; write access is not declared.
gain|A get/set/observable float controls sample gain; this declaration supplies no range, units, mapping or clipping law.
length|A get-only integer gives sample-file length in sample frames, not clip beats or bytes.
sample_rate|A get-only integer gives the loaded sample rate; this differs from Clip's float declaration and is not silently coerced.
slices|A read/observable list of integers gives playable-slice positions in sample frames. The source describes division by sample_rate for seconds; no target numerical conversion or rounding oracle is added.
slicing_sensitivity|A get/set/observable float controls slicing sensitivity in the published zero-to-one domain; threshold/detection and clamp behavior are not supplied.
start_marker|A get/set/observable integer denotes sample start-marker position; units, equality and refusal policy are not explicitly declared by this member.
texture_flux|A get/set/observable float controls Flux in Texture mode; no range or randomness law is inferred.
texture_grain_size|A get/set/observable float controls Grain Size in Texture mode; no units or synthesis law are supplied.
tones_grain_size|A get/set/observable float controls Grain Size in Tones mode; no units or synthesis law are supplied.
warp_markers|Get returns a marker dictionary and observe bangs on changes. The source describes a hidden final marker for the last segment's BPM but does not repeat Clip's dictionary schema; it is not fabricated by inheritance.
warp_mode|A get/set/observable integer names Beats, Tones, Texture, Re-Pitch, Complex and Complex Pro. The Sample list omits Clip's REX entry; these lists are not unified or used to replace finite Warp storage enums.
warping|A get/set/observable boolean denotes Warp enabled, without borrowing Clip's deferral warning as a Sample guarantee.
slicing_style|A get/set/observable integer names Transient, Beat, Region and Manual slicing modes; the numeric list is current-source context only.
slicing_beat_division|A get/set/observable integer selects the listed straight/triplet divisions or bar multiples in Beat Slicing mode; no region generation or boundary law is inferred.
slicing_region_count|A get/set/observable integer selects region count in Region Slicing mode; admissible count domain and partition rounding remain unknown.
gain_display_string|The function explicitly returns a list of symbols representing gain text; unlike Clip's gain_display_string property, this is a function. Example formatting is not a locale/precision grammar.
insert_slice|slice_time:int requests adding a slice only when one is absent at that time; unit, valid interval, duplicates and resulting IDs require evidence.
move_slice|source_time:int and destination_time:int request moving an existing slice; collision, ordering and endpoint policy are not specified.
remove_slice|slice_time:int requests removal if a slice exists there; minimum-slice and absent-slice event policies are not specified.
clear_slices|The function clears slices created in Manual Slicing mode; it does not claim deletion of arbitrary automatic-mode slices or sample audio.
reset_slices|The function returns edited slices to original positions; original-baseline identity and interaction with added/removed slices are not specified.''' ,
'SimplerDevice':'''sample|A get/observable Sample child represents the currently loaded sample; object replacement and old-ID invalidation are separate lifecycle questions.
can_warp_as|A read/observable boolean indicates availability of warp_as, not successful execution or an inferred availability formula.
can_warp_double|A read/observable boolean indicates availability of warp_double; the source does not define its exact capability predicate.
can_warp_half|A read/observable boolean indicates availability of warp_half; unavailable capability is not a negative success.
multi_sample_mode|A read/observable boolean indicates multisample mode; transitions and sample-child behavior in this mode are not specified.
pad_slicing|A get/set/observable boolean enables adding slices in Slicing mode by playing notes not assigned to existing slices; note-to-slice mapping is not supplied.
playback_mode|A get/set/observable integer names Classic, One-Shot and Slicing; it does not prove the full voice/envelope/signal law of any mode.
playing_position|A read/observable float gives a source-described normalized sample position between zero and one; update cadence, stopped values and interpolation are not specified.
playing_position_enabled|A read/observable boolean jointly describes sample playback and displayed position; it is not a settable enable control in this reference.
retrigger|A get/set/observable boolean denotes Retrigger enabled; exact voice restart or phase behavior remains owned by Simpler and unresolved where not evidenced.
slicing_playback_mode|A get/set/observable integer names Mono, Poly and Thru for Slicing playback; note allocation and release law are not inferred.
voices|A get/set/observable integer selects voice count; no admissible domain, stealing order or audio implementation is supplied.
crop|The function crops the loaded sample to the active start/end-marker region; file identity, destructive/non-destructive behavior and exact sample output remain unknown.
guess_playback_length|The function explicitly returns a float estimate of beat-time playback length between start/end markers; the estimation algorithm, accuracy and determinism are not supplied.
reverse|The function reverses the loaded sample according to the source, without specifying file rewriting, markers, Warp, slice transforms or waveform oracles.
warp_as|beats:int requests warping the active start/end-marker region to that beat count; capability must be admitted via can_warp_as, and numeric/audio laws remain with Warp/Simpler owners.
warp_double|The function requests doubling playback tempo for the active start/end-marker region; can_warp_double is an independent availability prerequisite, not a derived two-times waveform oracle.
warp_half|The function requests halving playback tempo for the active start/end-marker region; can_warp_half is an independent prerequisite, without a new time-stretch law.
replace_sample|file_path:symbol must name an absolute path to a valid supported audio file; it requests replacement of the loaded sample. Format eligibility, dependencies, object lifetime and media bytes remain separately owned.''' ,
'SimplerDevice.View':'''selected_slice|A get/set/observable integer identifies the selected slice by its slice time, rather than an inferred list index; empty/missing-slice and unit semantics remain unknown.'''
}

FUNCTION_ACTIONS={
'add_new_notes':'Prepare one independently valid new-note dictionary with required pitch/start_time/duration and explicitly chosen optional fields; propose one addition, then separately inspect returned-ID shape and note ownership.',
'add_warp_marker':'On a warped audio copy with admitted bracketing markers and a valid interior beat, propose one marker dictionary without sample_time, then on a fresh copy with admitted interior sample_time; keep Warp-owner constraints independent.',
'apply_note_modifications':'Query two independently known existing note records; propose changing one selected field in one returned record with its admitted ID, retaining the second untouched as a paired control.',
'clear_all_envelopes':'Prepare two distinguishable clip envelopes with valid target parameters; propose clearing all, with a separate clone retaining both as the positive envelope-existence baseline.',
'clear_envelope':'Prepare two envelopes bound to distinct valid DeviceParameter IDs; propose clearing one target while retaining the other control.',
'crop':'Prepare a clip with distinguishable content inside/outside independently admitted loop and marker regions; propose crop on looped and unlooped fresh copies separately.',
'deselect_all_notes':'On a MIDI clip with two admitted selected notes and one unselected control, propose deselection; retain a fresh selected baseline and inspect message/state roles separately.',
'duplicate_loop':'On a MIDI clip with a nonempty admitted region, nonzero distinguishable notes and envelope points, propose duplicate_loop on separate looped/unlooped copies; do not calculate a new exact transform.',
'duplicate_notes_by_id':'Prepare two known existing IDs; propose duplicating only one via list, then on fresh copy via dictionary with an admitted destination and integer transposition; retain untouched-note control.',
'duplicate_region':'Prepare notes clearly inside/outside an admitted beat region and two pitches; propose all-pitch and specified-pitch duplication to a disjoint valid destination on fresh copies.',
'fire':'With actual Session clip, track, launch settings and paired working nonzero routed source admitted, propose fire and compare its dispatch role to an independently working launch-button baseline; no launch sample is predicted.',
'get_all_notes_extended':'Prepare distinct admitted notes inside and outside markers/loop plus a known selection; propose no-argument query and then optional return-field dictionary query on the same stable clip.',
'get_notes_by_id':'Prepare two admitted existing note IDs; propose querying one ID by list and separately by dictionary with return fields; distinguish the unrequested note without guessing result order.',
'get_notes_extended':'Prepare notes whose starts lie strictly inside and outside an independently admitted time/pitch area; propose positional and dictionary query forms, with field filtering separately.',
'get_selected_notes_extended':'Prepare two admitted notes with an explicit known selection of one; propose full and return-field-filtered selected-note queries, retaining the other unselected.',
'move_playing_pos':'Admit active MIDI-overdub or nonrecording warped-audio playback with nonzero routed source and a working jump baseline; propose one valid positive relative beat request, then a negative one on fresh state.',
'move_warp_marker':'With an existing independently admitted interior beat marker and legal destination under the Warp owner, propose one movement and retain a second unmoved marker as control.',
'quantize':'Use a MIDI clip with admitted off-grid note starts, explicit swing/grid/amount settings and untouched clone; propose quantize and record note/state roles without predicting transformed times.',
'quantize_pitch':'Use two admitted pitches with off-grid starts; propose quantization for only one pitch under explicit grid/amount/swing, retaining the other pitch as the paired control.',
'remove_notes_by_id':'With two independently admitted IDs, propose removing exactly one existing ID and retain the other as control; establish identity anew on fresh state.',
'remove_notes_extended':'Use notes strictly inside/outside an admitted beat/pitch area; propose removal for that area, keeping edge-equality variations for the separate unknown boundary case.',
'remove_warp_marker':'Use a disposable warped audio copy with an admitted removable interior marker and valid remaining marker baseline under the Warp owner; propose removal at its known beat time.',
'scrub':'With valid visible clip, active nonzero routed playback, known Global Quantization and transport, propose one interior beat scrub request followed by independently admitted stop_scrub; no scheduling tolerance.',
'select_all_notes':'Prepare two existing MIDI notes with only one selected; propose selecting all and separately inspect named output and selection, retaining a fresh baseline.',
'select_notes_by_id':'Prepare two admitted note IDs and a known selection baseline; propose selecting only one valid ID before the separate nonexistent-ID unknown probe.',
'set_fire_button_state':'On an admitted launchable Session clip with known mode and working button baseline, propose true then false on fresh state; preserve explicit transport/nonzero output and no timing oracle.',
'stop':'Admit this clip actually playing with working nonzero output; propose stop, then separately use fresh triggered-only and other-playing-clip controls to test the documented applicability roles.',
'stop_scrub':'Admit an active scrub via independently working source/transport and start-scrub baseline; propose stop_scrub and retain a separate continuing-scrub control.',
'hide_envelope':'Admit a visible clip Envelopes box and selected valid parameter; propose hide_envelope, with a fresh visible-box baseline.',
'select_envelope_parameter':'Admit two valid DeviceParameters eligible for this clip and visible Envelopes box; propose selecting one, retaining an independent manually selected baseline.',
'show_envelope':'Admit a selected valid clip and independently hidden Envelopes box; propose show_envelope after a working manual show/hide baseline.',
'show_loop':'Admit this clip visible in Detail View with a known loop initially outside the displayed area; propose show_loop, then test hidden-clip context separately as unknown.',
'gain_display_string':'Admit a loaded owned sample with known current gain; propose the Sample function call and record return-role/type separately from Clip property access, with no locale or precision oracle.',
'insert_slice':'Admit a sample in a known slicing context with an empty eligible interior slice time and another existing slice; propose insertion at the empty time, then duplicate-time behavior separately.',
'move_slice':'Admit one existing interior slice and an independently valid unoccupied destination; propose movement while retaining another slice as a paired identity control.',
'remove_slice':'Admit an existing interior removable slice and another retained slice; propose removal at the existing time, then absent-time behavior on fresh state separately.',
'clear_slices':'Admit Manual Slicing mode with explicitly created manual slices and a known untouched clone; propose clear_slices without inferring behavior for automatic-mode slices.',
'reset_slices':'Admit recorded original slice positions and a separately documented edit of one slice; propose reset_slices, retaining unedited baseline; added/removed slice cases remain unknown.',
'guess_playback_length':'Admit an owned loaded sample with explicit valid start/end region and independent eligibility; propose estimate query on two distinguishable valid regions without assuming accuracy or formula.',
'reverse':'Admit owned nonsymmetric nonzero sample and valid active region; propose reverse on disposable state after a working unmodified playback baseline; file/audio/marker results have no oracle.',
'warp_as':'Admit loaded sample, active valid region and independently true can_warp_as; propose one independently supported beats:int request, with a fresh unchanged working baseline.',
'warp_double':'Admit loaded sample, active valid region and independently true can_warp_double; propose warp_double after a working baseline; no numerical playback/audio comparator.',
'warp_half':'Admit loaded sample, active valid region and independently true can_warp_half; propose warp_half after a working baseline; no numerical playback/audio comparator.',
'replace_sample':'Admit two owned readable supported audio files with distinct identity and absolute paths, valid Simpler sample and dependency controls; propose replace_sample with the second path on disposable state.'
}
# Local unknown clauses keep unsupported behavior visible and scoped.
UNKNOWNS=[
('Target applicability and inherited closure','Exact12.4.3 presence, signatures and behavior of all five current-public references remain unknown. SimplerDevice inherits Device and SimplerDevice.View inherits Device.View by source description only; no generic inherited members are flattened or counted as specified here.'),
('Access and type refusal','Wrong property types, read-only writes, unsupported observation and function arity/return/error policy remain unknown, including Clip position access/prose disagreement. No bridge success/failure format is supplied here.'),
('Object and capability lifetime','Missing/deleted clip, replaced sample, stale ID, missing view, absent warp capability and multisample contexts remain unknown; unavailable prerequisites are not negative passes.'),
('Notes dictionary and identity','Malformed note dictionaries, absent/duplicate/stale IDs, mixed valid-invalid batches, optional return lists, field coercion, ordering and atomicity remain unknown except explicitly retained source predicates; storage IDs and API IDs are not presumed identical.'),
('Clip context and region boundaries','Audio/MIDI, Session/Arrangement/TakeLane, recording/overdub, loop/Warp and start/end relationships require independent context evidence; edge equality, reversed/empty intervals and unit conversion remain unknown where not already owned.'),
('Warp, slice and mode dependencies','Warp availability/mode changes, slice collision/minimum counts, original reset baselines, multisample and playback/slicing mode dependencies remain unknown; Clip and Sample marker dictionaries/enums are not unified.'),
('Tuning, expression and quantization','Tuning/MPE, note probability/velocity deviation, grid/swing/amount and voice/retrigger interactions are not numeric, RNG, MIDI-message or signal laws derived from member names.'),
('Media and dependency operations','Sample replacement/crop/reverse, clip crop and RAM/gain/path roles give no file rewrite, codec/dependency/cache/format, gain/sound or transaction guarantees.'),
('Event, transport and rate lifecycle','Observer payload/cadence/order, stopped/playing/recording transitions, transport jumps, Warp deferral and sample-rate effects remain unknown; a bang description is not an event-count or timing oracle.'),
('Persistence and transactional editing','Undo/redo, cancellation, save/reopen, object/track reorder and cross-object identity preservation remain unknown; existing finite storage rules are not proof of API transactions.'),
('Initialization and teardown','Binding before initialization, closing/reopening Set/device/clip view, observer detach/rebind, source loss and teardown behavior remain unknown and retain generic bridge ownership.'),
('Undeclared units and signatures','Where these bodies omit units, ranges, argument forms, returns or access, those details remain unknown. Clip.View grid indexes and Sample marker/slice argument units are not guessed from UI or similarly named fields.')
]
UNKNOWN_CASES=[
(1,'context','After independent capability discovery, reconcile each five-entry declaration against an admitted exact12.4.3 API surface; record absent/unavailable capabilities as U, and keep Device/Device.View inherited-member reconciliation with its future owner.'),
(2,'invalid-type','After a working read/write baseline for Clip name, propose a non-symbol type on a disposable clip; separately test Sample gain with an invalid type after its own valid baseline. Do not assume coercion, refusal, diagnostics or partial state.'),
(2,'read-only-write','After independently working reads of Clip file_path and Sample length, propose a write attempt on fresh disposable objects; keep Clip position conflict separate and do not assume a writable setter from its prose.'),
(2,'observe','After a working observable Clip name binding and independently valid manual name change, separately propose observation of get-only Clip has_groove and get/set-only Clip.View grid_is_triplet; unsupported observer setup is U, without an expected error.'),
(2,'arity-return','After admitted valid function baselines, vary one required argument/type of Sample move_slice and Simpler replace_sample, separately; no omitted return is presumed void or id-zero.'),
(3,'source-loss','After working Clip name and Sample file_path reads, remove a disposable clip or replace the sample by an independently admitted operation; then propose the old binding query and new admitted binding separately.'),
(3,'capability','After admitted true can_warp_as with a working warp request baseline, construct an independently verified unavailable capability context; do not count an unavailable target/control as a passing refusal.'),
(3,'multisample','Admit a real independently verified multisample Simpler context and single-sample positive baseline before probing sample child and crop applicability; missing fixture remains U.'),
(4,'malformed','After a valid add_new_notes dictionary baseline, vary one missing required key, wrong field type or malformed notes container on fresh copies; record atomicity/messages/state as unknown.'),
(4,'invalid-id','After admitted note-ID query and modification baselines, test stale/nonexistent/duplicate IDs and a mixed valid-invalid batch separately for apply_note_modifications and select_notes_by_id; retain their distinct source claims without inventing an error protocol.'),
(4,'return-fields','After a working get_notes_extended query in both published forms, propose empty, unknown, repeated and mistyped return-field lists separately; valid query and stable distinct notes are prerequisites.'),
(5,'boundary','After admitted valid Clip start/end writes, test equality, reversed ordering and empty span on fresh states; separately compare Sample integer marker properties without borrowing Clip beat units or bounds.'),
(5,'region-boundary','After a query selecting notes strictly inside and outside an admitted area, place note starts exactly on each boundary and vary zero/negative spans separately; no endpoint convention is presumed.'),
(5,'clip-context','Admit distinct audio, MIDI, Session, Arrangement and TakeLane clips plus working valid member baselines; vary one context for audio-only gain, MIDI-only notes and start_time separately, without treating missing access as success.'),
(5,'recording','Admit independently working move_playing_pos on a legal playing clip and recording fixtures separately; probe recording audio, non-overdub MIDI recording and overdub MIDI as distinct contexts, with nonzero source and actual arm/monitor state.'),
(6,'mode-dependency','After independent valid sample/mode baselines, vary one of Classic/One-Shot/Slicing, multisample or slicing style, then inspect pad_slicing, selected_slice and warp availability separately; no mode-to-capability formula.'),
(6,'slice-boundary','After valid insert/move/remove slice baselines, test occupied destination, absent source, endpoint times and final remaining slice separately on resettable copies; independently establish actual valid units first.'),
(6,'warp-dictionary','After admitted Clip marker and Sample marker reads, inspect dictionary shape separately; do not copy Clip sample_time/beat_time keys or REX index into Sample without evidence. Malformed marker dictionaries and shadow edits remain unknown.'),
(7,'tuning-expression','With separately admitted tuning/MPE setups and valid untuned baseline, propose the same member-level note query/edit and inspect note identity/expression roles; do not derive tuned pitch, bend or per-note-expression transport.'),
(7,'numeric-rng','With valid off-grid notes, nonzero source/active path and a working quantize/velocity baseline, vary one admitted grid/swing/amount/probability/deviation setting; record unknown numeric, RNG and signal outcomes without tolerances.'),
(8,'dependency','After successful independently admitted supported owned-file loading baseline, propose replace_sample with missing/unreadable/unsupported dependencies separately; no error, fallback or file transaction is predicted.'),
(8,'signal','With a valid nonsymmetric nonzero sample, eligible active Simpler, nonzero gain, nonmuted output and paired unmodified baseline, propose crop/reverse/gain/RAM changes separately; record audio/file/dependency consequences as U.'),
(9,'transport','With working nonzero routed playing clip and admitted observer baseline, propose stop/start, jump and triggered/recording changes separately; observe status/position roles without expected callback counts, order or latency.'),
(9,'sample-rate','With admitted valid owned sample, active processing/nonzero output and baseline at one actual supported rate, propose another independently supported rate; inspect sample_rate/length/position roles without resampling arithmetic.'),
(9,'event-sequencing','After separately working Warp write/read and marker observer baselines, propose a controlled sequence of valid warping and marker operations; source deferral is context only, not an event-loop, thread or completion-time prescription.'),
(10,'undo-redo','After a valid single-member edit of Clip name, note data or Sample slice on separate disposable copies, propose Undo/Redo; inspect identity/state/event roles with a paired untouched baseline and no transaction oracle.'),
(10,'cancellation','After valid independently admitted sample replacement or clip crop setup, propose cancellation only at an actually exposed supported cancellation boundary; absent cancellation capability remains U, not fabricated UI.'),
(10,'persistence','After an admitted valid member edit with known owned assets and independently working save/reopen baseline, propose save/reopen and rebind; inspect state/identity without importing finite storage into API behavior.'),
(10,'reorder','After working sample/clip bindings and valid track/device reorder baseline, reorder a track/device on a disposable Set; inspect old and fresh paths/IDs with bridge ownership and no assumed stability.'),
(11,'initialization','Only with an admitted working initialized bridge/object/member baseline, propose a binding before supported initialization and again after; no helper-script or source example is executed here.'),
(11,'teardown','After a working observer/property baseline with actual initialized owned objects, close/reopen a view, remove device and close Set separately; propose detachment/rebinding with no stale-ID, callback or resource-leak oracle.'),
(12,'unit-signature','After independent supported-unit/signature discovery, probe Sample marker/slice argument units, Clip.View grid indexes and functions with omitted returns; retain distinct known-good inputs and do not infer from names or UI.')
]
OWNER_PATHS=[
'wiki/specs/live-api-bridge-workflows.md','wiki/specs/clip-launch.md','wiki/specs/playback-core.md',
'wiki/specs/midi-note-storage.md','wiki/specs/midi-editing-tools.md','wiki/specs/warp-markers.md',
'wiki/specs/warping-workflows.md','wiki/specs/clip-view-workflows.md','wiki/specs/device-simpler.md',
'wiki/specs/automation-envelopes.md','wiki/specs/automation-workflows.md','wiki/specs/media-file-workflows.md',
'wiki/specs/project-media-workflows.md','wiki/specs/mixer-values.md','wiki/specs/mpe-workflows.md',
'wiki/specs/tuning-systems.md','wiki/research/sources/cycling74-live-api.md',
'wiki/research/full-live-specification-design.md','wiki/research/full-live-specification-plan.md',
]
# Plan/design are routing context, not frozen external inputs: parent updates these.
FROZEN_OWNERS=OWNER_PATHS[:-2]

def owners(name,anchor):
 out=['wiki/specs/live-api-bridge-workflows.md']
 if name.startswith('Simpler') or name=='Sample':out+=['wiki/specs/device-simpler.md']
 if any(s in anchor for s in ['note','quantize','signature']):out+=['wiki/specs/midi-note-storage.md','wiki/specs/midi-editing-tools.md','wiki/specs/mpe-workflows.md','wiki/specs/tuning-systems.md']
 if any(s in anchor for s in ['warp','beats_','complex_','texture_','tones_']):out+=['wiki/specs/warp-markers.md','wiki/specs/warping-workflows.md']
 if any(s in anchor for s in ['launch','fire','stop','playing','scrub','legato','velocity_amount']):out+=['wiki/specs/clip-launch.md','wiki/specs/playback-core.md']
 if 'envelope' in anchor:out+=['wiki/specs/automation-envelopes.md','wiki/specs/automation-workflows.md']
 if any(s in anchor for s in ['sample','file','crop','reverse','ram']):out+=['wiki/specs/media-file-workflows.md','wiki/specs/project-media-workflows.md']
 if name.startswith('Clip'):out+=['wiki/specs/clip-view-workflows.md']
 return list(dict.fromkeys(out))


def build():
 allsources=load(INV/'all-sources-r1.json');allblocks=load(INV/'reference-blocks.json')
 entries=[x for x in load(INV/'lom-entries.json') if x['name'] in ROLES]
 assert [x['name'] for x in entries]==list(ROLES)
 selectedids={x['id'] for x in entries}
 original=[x for x in load(INV/'lom-members.json') if x['reference_entry'] in selectedids]
 assert len(original)==131
 sources=[x for x in allsources if x['id'] in {e['source_id'] for e in entries}]
 blocks={s['id']:allblocks[s['id']] for s in sources}
 reqs=[];cases=[];members=[];profiles=[]
 for entry in entries:
  name=entry['name'];sid=entry['source_id'];rows=blocks[sid]
  roles=dict(line.split('|',1) for line in ROLES[name].splitlines())
  em=[m for m in original if m['reference_entry']==entry['id']]
  assert set(roles)=={m['anchor'] for m in em},name
  profile=dict(entry,documentary_status='partial-current-public-profile',source_inventory_specification=entry['specification'],specification='partial-documentary-only',complete=False,
   canonical_path_declarations=[r for r in rows if r['tag']=='pre'],
   class_context=[r for r in rows if r['block']=='B0002'],
   inherited_members='Device; not flattened, generic member owner pending' if name=='SimplerDevice' else 'Device.View; not flattened, generic member owner pending' if name=='SimplerDevice.View' else 'No additional inherited members asserted by this packet',
   mapped_direct_members=len(em),unmapped_direct_members=0,target_unresolved_direct_members=len(em))
  profiles.append(profile)
  for m in em:
   i=next(i for i,r in enumerate(rows) if r['block']==m['block'])
   j=i+1
   while j<len(rows) and rows[j]['tag'] not in ('h2','h3'):j+=1
   body=rows[i:j]
   accessrow=[r for r in body if r['text'].startswith('Access: ')]
   access=accessrow[0]['text'].removeprefix('Access: ') if accessrow else None
   caps=[x for x in ('get','set','observe') if access and x in access]
   declaredtype=m['heading'].removeprefix(m['anchor']).strip() or None
   ev=[dict(source=sid,block=r['block'],anchor=m['anchor'],html_line=r['html_line'],html_column=r['html_column'],url=m['url'],source_sha256=entry['source_sha256']) for r in body]
   rid=f'REQ-LAPI-CLIP-SAMPLE-{len(reqs)+1:03d}';cid=f'LCS-{len(cases)+1:03d}'
   contract=roles[m['anchor']]
   req=dict(id=rid,title=f"{name}.{m['anchor']} ({m['category']})",provenance='D-current-public',target_applicability='U',contract=contract,direct_member=m['id'],documented_type=declaredtype,documented_access=access,evidence=ev)
   reqs.append(req)
   if m['category']=='functions':
    if m['anchor']=='crop' and name=='SimplerDevice':action='Admit an owned loaded sample with distinct nonzero content inside/outside an independently valid active start/end region; propose SimplerDevice crop on a disposable copy, retaining an unmodified baseline and no media/file oracle.'
    else:action=FUNCTION_ACTIONS[m['anchor']]
    action=f"For {name}.{m['anchor']}: "+action+' Use only an independently admitted signature; omitted source arguments/returns are not invented.'
    kind='function'
   elif m['category']=='children':
    action=f"On an independently admitted {name} object, propose the declared {m['anchor']} child access ({access}); establish actual child type/availability independently, retain a working parent-object baseline, and inspect the child role separately from generic path/ID lifecycle."
    kind='child'
   else:
    action=f"On an independently admitted {name} object in the particular source context below, propose only the declared {m['anchor']} capabilities ({access}). "
    if 'get' in caps:action+='Read the member in two independently distinguishable valid states, retaining a known-good object/member baseline. '
    if 'set' in caps:action+='On a disposable clone, propose one independently admissible alternate value of its declared type and a separate restore; do not infer range, coercion or round-trip guarantees. '
    if 'observe' in caps:action+='After an independently working observer baseline, propose one valid state change through the existing owner and inspect the described notification role without count/order/cadence predictions. '
    action+='Admit the exact predicate: '+contract
    kind='event' if access=='observe' else 'property'
   cases.append(dict(id=cid,requirements=[rid],direct_members=[m['id']],kind=kind,provenance='D-current-public',fixture='fixtures.json#LCS-OWNED',preconditions=['admitted-api-object','member-context','paired-positive-baseline','active-path-if-audible'],setup_and_action=action,source_claim=contract,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=ev))
   members.append(dict(m,documentary_owner='wiki/specs/live-api-clip-sample.md',status='partial-source-role-with-proposed-case',requirements=[rid],cases=[cid],complete=False,documented_type=declaredtype,documented_access=access,documented_capabilities=caps,
    argument_declaration=[r for r in body if re.match(r'Parameters?:',r['text'])] or None,
    return_declaration=[r for r in body if 'Returns' in r['text'] or r['text'].startswith('Output:') or 'Output:' in r['text']] or None,
    argument_return_note='Null means no explicit parameter/return declaration found, not zero arguments or void return; full body retained. Inline prose can describe a role without a formal signature.',
    source_body=body,existing_behavior_owners=owners(name,m['anchor']),target_unresolved=True))
 for n,(title,contract) in enumerate(UNKNOWNS,1):
  reqs.append(dict(id=f'REQ-LAPI-CLIP-SAMPLE-{131+n:03d}',title=title,provenance='U',target_applicability='U',contract=contract,direct_member=None,evidence=[]))
 for n,kind,action in UNKNOWN_CASES:
  r=reqs[130+n]
  cases.append(dict(id=f'LCS-{len(cases)+1:03d}',requirements=[r['id']],direct_members=[],kind=kind,provenance='U',fixture='fixtures.json#LCS-OWNED',preconditions=['admitted-api-object','member-context','paired-positive-baseline','active-path-if-audible'],setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[]))
 counts=dict(reference_profiles=5,direct_members=131,direct_member_categories=dict(Counter(x['category'] for x in members)),members_mapped_to_partial_roles=131,members_unmapped=0,target_unresolved_members=131,inherited_members_flattened=0,complete_profiles=0,complete_members=0,requirements=len(reqs),requirement_provenance=dict(Counter(x['provenance'] for x in reqs)),cases=len(cases),case_provenance=dict(Counter(x['provenance'] for x in cases)),case_kinds=dict(Counter(x['kind'] for x in cases)),source_blocks={e['name']:len(blocks[e['source_id']]) for e in entries},all_documentary_and_target_oracles_null=True)
 fixtures=dict(id='LCS-OWNED',admitted_api_object='Future only: independently establish actual exact-target API/Max capability, initialized owned device/Set, live reachable object and valid path/ID, supported member/type/access and call signature. No source patch, JS, API or Max operation has been executed.',member_context='Admit actual audio/MIDI and Session/Arrangement/TakeLane/recording/overdub state, visible clip/view, valid nonempty region with start<end, valid Warp/mode/capability, owned loaded nonzero sample/file, existing marker/slice/note IDs and independent valid parameter/envelope targets as relevant. Null/unknown units must be established before generating arguments.',paired_positive_baseline='First require an independently working same-object/member and same-context positive operation, stable distinct owned content/notes and fresh resettable copies. An unavailable API/feature/fixture is U, never a negative pass. Query identity and error/message routes remain bridge-owned.',active_path_if_audible='For any future audible/transport/recording consequence require independently nonzero source, active eligible device and routing, nonzero gain/amount, known monitor/arm, unmuted output and an independently working unmodified positive baseline. Transport/rate/tuning are explicit, actual supported conditions, not simulated host claims.',execution=False)
 return dict(sources=sources,source_blocks=blocks,profiles=profiles,members=members,requirements=reqs,cases=cases,counts=counts,fixtures=fixtures)


def pages(data):
 packet='../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/'
 spec='''---
id: SPEC-LIVE-API-CLIP-SAMPLE
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current-public API applicability U
---

# Public Live API Clip and Simpler sample members

## Scope and authority

This bounded partial draft covers exactly Clip, Clip.View, Sample, SimplerDevice
and SimplerDevice.View from the [reviewed public API inventory](../research/sources/cycling74-live-api.md).
**D-current-public** identifies retained current publisher reference text; the
public index declares Live12.4.5. Every exact12.4.3 member, access, signature,
value, event and output remains U. This is not a released handoff or completed
class/API compatibility claim. All five profiles and all131 direct members
remain partial/complete:false, even though each has a documentary role and case.
[Research](../research/live-api-clip-sample.md) retains source identity and questions.
[Coverage design](../research/full-live-specification-design.md) and
[plan](../research/full-live-specification-plan.md) govern closure.

[Generic bridge workflows](live-api-bridge-workflows.md) retain paths, IDs,
get/set/call/observe message framing, binding, initialization and lifecycle.
This page adds particular class/member roles, not bridge wire grammars. Simpler
inherits Device and its view inherits Device.View according to source context;
generic inherited members await their owner and are neither flattened nor
counted as specified here. No inherited view path is fabricated. Literal canonical
path patterns in profiles are public examples, not stable object IDs or complete
path syntax. Clip's paths separately name Session slots and Arrangement clips;
Clip.View's explicit path is Session-based; Sample names a device sample.

[Clip launch](clip-launch.md) and [playback core](playback-core.md) retain finite
launch, storage and scheduling laws. [Note storage](midi-note-storage.md),
[MIDI editing](midi-editing-tools.md), [MPE](mpe-workflows.md), [tuning](tuning-systems.md),
[Warp markers](warp-markers.md), [Warp workflows](warping-workflows.md),
[Clip View](clip-view-workflows.md), [Simpler](device-simpler.md),
[automation envelopes](automation-envelopes.md), [automation workflows](automation-workflows.md),
[mixer values](mixer-values.md), [media files](media-file-workflows.md) and
[project/media](project-media-workflows.md) retain their respective finite storage,
region, sound, file/dependency and editing contracts. Newer API enum lists,
normalized values, argument names or examples do not replace those laws or broaden
an extracted finite result to an API workflow. Member ledger links route overlap;
a route is not proof of an interaction.

## Inputs, outputs and denominator

The [per-member ledger](PACKETmembers.json) preserves all131 exact inventory IDs,
source bodies, heading type/access text, argument/return declarations when present,
existing owners, one particular requirement and one proposed case each. The
[profiles](PACKETprofiles.json) preserve the five original entry IDs/denominators,
class context and literal documented canonical paths. Null declaration fields
mean not explicitly supplied, not zero arguments or void return. Full function
bodies retain dictionary keys, optional fields, published units/ranges/defaults
and version notes as source data; case proposals do not turn them into numeric
or message oracles. Missing source units and conflicts remain explicit unknowns.

All target and documentary expected/comparison fields are null, target grade U,
executed:false. These are API/event/numeric/message/signal/dispatch proposals,
with source_claim prose only; even UI-like members are not graded as observed UI.
[Fixtures](PACKETfixtures.json) require independently admitted actual API capability,
initialized owned reachable objects, valid member/type/access and clip/sample
context, existing IDs/regions/capabilities, and a paired working positive baseline.
Audible consequences additionally require nonzero eligible content, active device,
nonzero gain, actual routing/monitor/arm/transport and nonmuted output. Unavailable
API, feature or fixture is U, never a passing negative. No original, Max/API,
patch, JavaScript, example, audio, hardware, native or candidate was executed;
no runtime/tool installation or new source capture occurred. Figures and linked
help/examples were not separately inspected or run.

## Documentary member clauses

'''.replace('PACKET',packet)
 for r in data['requirements']:
  spec+=f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
  if r['evidence']:
   first,last=r['evidence'][0],r['evidence'][-1]
   spec+=f"Evidence: [{first['source']} #{first['anchor']}]({first['url']}), {first['block']}..{last['block']}, retained HTML{first['html_line']}..{last['html_line']}; exact bytes/hash and argument/access context in the member ledger.\n\n"
  else:spec+='Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.\n\n'
 spec+='''## Case and source indexes

[Requirements](PACKETrequirements.json), [cases](PACKETcases.json),
[sources](PACKETsources.json), [complete selected reference blocks](PACKETsource-blocks.json)
and [counts](PACKETcounts.json) are retained with read-only validation, canonical
snapshots and a sealed manifest. One member case can contain distinct proposed
access branches and does not prove complete positive/negative/boundary coverage.
Unknown cases are separately scoped to refusal, malformed data, identity, mode,
region, lifecycle and dependency interactions. All remain unexecuted.
'''.replace('PACKET',packet)
 research='''---
id: RESEARCH-LIVE-API-CLIP-SAMPLE
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public API applicability U
---

# Clip and Simpler sample API evidence

The [canonical draft](../specs/live-api-clip-sample.md) is the first bounded
member-family reconciliation of the [reviewed53-source API inventory](sources/cycling74-live-api.md).
All379 text blocks of the selected five reference bodies were read: Clip214,
Clip.View20, Sample84, SimplerDevice55, SimplerDevice.View6. Raw retained HTML was
reparsed only for source/locator verification; no reference code was executed.
No recapture, figure, external help, patch, JavaScript or example inspection/run.

## Source identities and scope

[Sources](PACKETsources.json) preserves original URL/final URL, capture UTC, bytes,
SHA256, version and original retained paths; these are reused bytes, not new captures.
[Source blocks](PACKETsource-blocks.json) is an exact subset of inventory R1 blocks.
[External pins](PACKETexternal-pins.json) pins inventory R1 metadata/manifest,
original members/entries, all53-source index/blocks, selected raw pages/parser,
independent inventory/bridge review identity and existing owner/release manifests.
The validator verifies all53 retained source hashes but semantic reading was the
five selected references only. Source/index current12.4.5 is not target12.4.3.

## Documentary reconciliation

All131 direct members have a particular source-backed role and proposed case:
Clip77, Clip.View6, Sample28, SimplerDevice19, SimplerDevice.View1. No source entry
or direct member disappears from its denominator. All131 target outcomes and
all five profiles remain unresolved/partial; no member or class is complete.
Generic Device/Device.View inheritance is explicitly pending, not an invented
flattened API. A member being linked to an existing owner is not semantic proof.
All dictionary fields, public range/index/default notes and types remain exact
source data in member bodies; paraphrased clauses limit their authority to source
roles. Published numeric/message/event/signal/timing claims are never documentary
or target test oracles here. No sample tolerance or result comparator is invented.

## Source-context questions

- Q-LCS-001: Clip position lists get/observe while its prose describes setting
  loop position/preserving loop length. Preserve both; no new set capability.
- Q-LCS-002: Clip is_playing lists get/set without observe, despite the reporting
  role. Simpler playing_position_enabled lists get/observe, despite its name.
  Do not invent toggle/set/observer capabilities by analogy.
- Q-LCS-003: Sample gain_display_string is a function returning list of symbols;
  Clip gain_display_string is a get-only symbol property. Sample sample_rate is
  int; Clip sample_rate is float. Preserve declared differences, not native coercion.
- Q-LCS-004: Clip and Sample Warp mode lists differ at REX; Sample warp_markers
  does not repeat Clip's sample_time/beat_time schema. Existing finite Warp enums,
  marker edits/conversions/shadow rules remain their owner's evidence, not replaced.
- Q-LCS-005: Sample marker and slice function integer units/bounds are not stated
  by their member bodies. Slices property explicitly uses sample frames; do not
  silently transfer that unit to every integer signature or Clip beat marker.
- Q-LCS-006: Clip start_time's Session wording reports the currently playing clip
  on the track regardless of queried clip, unlike a simple per-object start cache.
  Context and negative positions require explicit fixtures and remain target-U.
- Q-LCS-007: Note dictionary APIs retain required/optional fields, valid-ID
  preconditions, field-selection forms and distinct missing-ID wording. Deselect's
  reference to replace_selected_notes does not add an undeclared member or restore
  older signatures. No storage-ID/API-ID identity, RNG or atomicity is inferred.
- Q-LCS-008: Omitted units/arguments/returns and Clip.View grid enum stay unknown.
  Source access prose is not a complete refusal or error protocol. Return snippets
  in the ledger include full mixed paragraphs for faithful context, not parsed ABI.
- Q-LCS-009: Warp deferral/sequence warning describes possible externally noticed
  ordering surprises only, not threads, event loops, latency or internal design.
  Sample warping does not inherit this warning as a guaranteed behavior.
- Q-LCS-010: Simpler can_warp flags need independent available-feature baselines;
  mode, multisample, voice, retrigger, crop/reverse/replacement and sample lifecycle
  supply no algorithm, media transaction, voice allocator or signal prediction.
- Q-LCS-011: Inherited Device and Device.View members/canonical reachability await
  generic member-family work; five profiles are not full inherited member coverage.
- Q-LCS-012: Exact target applicability, malformed/refusal, read-only/observe,
  deleted/missing IDs, dictionaries, region equality, tuning/dependencies,
  cancel/undo/persistence/reorder/transport/rate/teardown all remain U. A failed or
  unavailable prerequisite cannot pass a proposed negative case.

Root owns integration into shared catalogs/questions/coverage/log. This packet
contains no implementation, release, reference execution or compatibility result.
'''.replace('PACKET',packet)
 return spec,research

if __name__=='__main__':
 assert sys.argv[1:]==['--write'],'Author generation requires explicit --write; use validate.py for read-only checks.'
 assert not (P/'manifest-author-r1.json').exists(),'Frozen packet must not be overwritten.'
 data=build()
 for name,v in data.items():dump(P/(name.replace('_','-')+'.json'),v)
 # Pins are external immutable inputs and current exact owner snapshots; no shared mutation.
 pinpaths=[INV/x for x in ['all-sources-r1.json','classes-sources-r1.json','sources-initial.json','lom-members.json','lom-entries.json','reference-blocks.json','manifest-inventory-r1.json','derive_inventory.py']]
 pinpaths += [INV/s['file'] for s in data['sources']]
 pinpaths += [P.parent/'reviews'/x for x in ['max-api-inventory-review.json','max-api-inventory-review-r3-final.json','live-api-bridge-workflows-review.json']]
 pinpaths += [ROOT/x for x in FROZEN_OWNERS]
 pinpaths += [ROOT/x for x in ['tools/spec_browser.py','tools/build_artifact_browser.py']]
 pinpaths += [ROOT/'handoff'/x/'manifest.json' for x in ['clip-launch-v2','midi-note-storage-v2','warp-markers-v2','automation-envelopes-v2','mixer-values-v2']]
 dump(P/'external-pins.json',[pin(x) for x in pinpaths])
 spec,research=pages(data)
 (ROOT/'wiki/specs/live-api-clip-sample.md').write_text(spec)
 (ROOT/'wiki/research/live-api-clip-sample.md').write_text(research)
 (P/'spec-r1.md').write_text(spec);(P/'research-r1.md').write_text(research)
 print(json.dumps(data['counts'],indent=2))
