---
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

The [per-member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/members.json) preserves all131 exact inventory IDs,
source bodies, heading type/access text, argument/return declarations when present,
existing owners, one particular requirement and one proposed case each. The
[profiles](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/profiles.json) preserve the five original entry IDs/denominators,
class context and literal documented canonical paths. Null declaration fields
mean not explicitly supplied, not zero arguments or void return. Full function
bodies retain dictionary keys, optional fields, published units/ranges/defaults
and version notes as source data; case proposals do not turn them into numeric
or message oracles. Missing source units and conflicts remain explicit unknowns.

All target and documentary expected/comparison fields are null, target grade U,
executed:false. These are API/event/numeric/message/signal/dispatch proposals,
with source_claim prose only; even UI-like members are not graded as observed UI.
[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/fixtures.json) require independently admitted actual API capability,
initialized owned reachable objects, valid member/type/access and clip/sample
context, existing IDs/regions/capabilities, and a paired working positive baseline.
Audible consequences additionally require nonzero eligible content, active device,
nonzero gain, actual routing/monitor/arm/transport and nonmuted output. Unavailable
API, feature or fixture is U, never a passing negative. No original, Max/API,
patch, JavaScript, example, audio, hardware, native or candidate was executed;
no runtime/tool installation or new source capture occurred. Figures and linked
help/examples were not separately inspected or run.

## Documentary member clauses

### REQ-LAPI-CLIP-SAMPLE-001 — Clip.view (children)

**D-current-public/target-U.** A get-only child refers to the clip's Clip.View; no independent view mutation is declared by this child.

Evidence: [C74-LOM-CLIP #view](https://docs.cycling74.com/apiref/lom/clip/#view), B0007..B0008, retained HTML36..37; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-002 — Clip.available_warp_modes (properties)

**D-current-public/target-U.** For an audio clip, the read-only list contains indexes of available Warp Modes, rather than a promise that every published mode is supported.

Evidence: [C74-LOM-CLIP #available_warp_modes](https://docs.cycling74.com/apiref/lom/clip/#available_warp_modes), B0010..B0012, retained HTML39..41; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-003 — Clip.color (properties)

**D-current-public/target-U.** The integer is a packed RGB color; setting it chooses a nearest color in the clip chooser. Packing and nearest-choice prose is not a target color metric or tie rule.

Evidence: [C74-LOM-CLIP #color](https://docs.cycling74.com/apiref/lom/clip/#color), B0013..B0015, retained HTML42..44; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-004 — Clip.color_index (properties)

**D-current-public/target-U.** An integer clip color index is get/set/observable; the declaration supplies no complete index palette.

Evidence: [C74-LOM-CLIP #color_index](https://docs.cycling74.com/apiref/lom/clip/#color_index), B0016..B0018, retained HTML47..49; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-005 — Clip.end_marker (properties)

**D-current-public/target-U.** A beat-valued end marker is independent of loop state and cannot be set earlier than the start marker; refusal/error details are omitted.

Evidence: [C74-LOM-CLIP #end_marker](https://docs.cycling74.com/apiref/lom/clip/#end_marker), B0019..B0021, retained HTML50..52; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-006 — Clip.end_time (properties)

**D-current-public/target-U.** The read/observable end time has separate Session Loop End versus End Marker and Arrangement right-edge contexts.

Evidence: [C74-LOM-CLIP #end_time](https://docs.cycling74.com/apiref/lom/clip/#end_time), B0022..B0024, retained HTML53..55; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-007 — Clip.gain (properties)

**D-current-public/target-U.** An audio-only float gain is documented on a normalized zero-to-one domain; it is not a new fader-to-amplitude law.

Evidence: [C74-LOM-CLIP #gain](https://docs.cycling74.com/apiref/lom/clip/#gain), B0025..B0027, retained HTML56..58; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-008 — Clip.gain_display_string (properties)

**D-current-public/target-U.** For audio clips, a get-only symbol presents a gain display string; the example does not define locale, precision or formatting grammar.

Evidence: [C74-LOM-CLIP #gain_display_string](https://docs.cycling74.com/apiref/lom/clip/#gain_display_string), B0028..B0030, retained HTML59..61; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-009 — Clip.file_path (properties)

**D-current-public/target-U.** For audio clips, a get-only symbol identifies the represented audio file location; this supplies no path normalization or file-access policy.

Evidence: [C74-LOM-CLIP #file_path](https://docs.cycling74.com/apiref/lom/clip/#file_path), B0031..B0033, retained HTML62..64; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-010 — Clip.groove (properties)

**D-current-public/target-U.** A Groove-valued get/set/observable association is documented, with a since-Live11 note; object identity and removal semantics remain unproved.

Evidence: [C74-LOM-CLIP #groove](https://docs.cycling74.com/apiref/lom/clip/#groove), B0034..B0036, retained HTML65..67; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-011 — Clip.has_envelopes (properties)

**D-current-public/target-U.** The read/observable boolean reports whether the clip has automation, without specifying serialized envelope ownership or scheduling.

Evidence: [C74-LOM-CLIP #has_envelopes](https://docs.cycling74.com/apiref/lom/clip/#has_envelopes), B0037..B0039, retained HTML70..72; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-012 — Clip.has_groove (properties)

**D-current-public/target-U.** A get-only boolean reports a Groove association; the source does not make it an observable property.

Evidence: [C74-LOM-CLIP #has_groove](https://docs.cycling74.com/apiref/lom/clip/#has_groove), B0040..B0042, retained HTML73..75; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-013 — Clip.is_session_clip (properties)

**D-current-public/target-U.** A get-only boolean identifies a Session clip; the source distinguishes Session from Arrangement membership.

Evidence: [C74-LOM-CLIP #is_session_clip](https://docs.cycling74.com/apiref/lom/clip/#is_session_clip), B0043..B0045, retained HTML78..80; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-014 — Clip.is_arrangement_clip (properties)

**D-current-public/target-U.** A get-only boolean identifies an Arrangement clip, without declaring a clip-transfer operation.

Evidence: [C74-LOM-CLIP #is_arrangement_clip](https://docs.cycling74.com/apiref/lom/clip/#is_arrangement_clip), B0046..B0048, retained HTML82..84; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-015 — Clip.is_take_lane_clip (properties)

**D-current-public/target-U.** A get-only boolean identifies Take Lane membership; the source explicitly also classifies Take Lane clips as Arrangement clips.

Evidence: [C74-LOM-CLIP #is_take_lane_clip](https://docs.cycling74.com/apiref/lom/clip/#is_take_lane_clip), B0049..B0051, retained HTML86..88; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-016 — Clip.is_audio_clip (properties)

**D-current-public/target-U.** A get-only boolean distinguishes audio from MIDI clips using the published boolean convention.

Evidence: [C74-LOM-CLIP #is_audio_clip](https://docs.cycling74.com/apiref/lom/clip/#is_audio_clip), B0052..B0054, retained HTML90..92; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-017 — Clip.is_midi_clip (properties)

**D-current-public/target-U.** The get-only boolean is described as opposite to is_audio_clip; it is not an input-conversion operation.

Evidence: [C74-LOM-CLIP #is_midi_clip](https://docs.cycling74.com/apiref/lom/clip/#is_midi_clip), B0055..B0057, retained HTML93..95; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-018 — Clip.is_overdubbing (properties)

**D-current-public/target-U.** A read/observable boolean reports overdubbing; recording engine and note-merge laws remain separate.

Evidence: [C74-LOM-CLIP #is_overdubbing](https://docs.cycling74.com/apiref/lom/clip/#is_overdubbing), B0058..B0060, retained HTML96..98; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-019 — Clip.is_playing (properties)

**D-current-public/target-U.** The source declares get/set access to a boolean that includes recording in the playing state; it does not declare observe or specify the setting transition.

Evidence: [C74-LOM-CLIP #is_playing](https://docs.cycling74.com/apiref/lom/clip/#is_playing), B0061..B0063, retained HTML99..101; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-020 — Clip.is_recording (properties)

**D-current-public/target-U.** A read/observable boolean reports clip recording, without asserting captured media or note content.

Evidence: [C74-LOM-CLIP #is_recording](https://docs.cycling74.com/apiref/lom/clip/#is_recording), B0064..B0066, retained HTML102..104; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-021 — Clip.is_triggered (properties)

**D-current-public/target-U.** A get-only boolean corresponds to a blinking Clip Launch button; it is distinct from already playing or recording.

Evidence: [C74-LOM-CLIP #is_triggered](https://docs.cycling74.com/apiref/lom/clip/#is_triggered), B0067..B0069, retained HTML105..107; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-022 — Clip.launch_mode (properties)

**D-current-public/target-U.** A get/set/observable integer names Trigger, Gate, Toggle and Repeat in the current reference. Published indexes/default do not replace the finite launch owner.

Evidence: [C74-LOM-CLIP #launch_mode](https://docs.cycling74.com/apiref/lom/clip/#launch_mode), B0070..B0072, retained HTML108..110; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-023 — Clip.launch_quantization (properties)

**D-current-public/target-U.** A get/set/observable integer names Global, None and listed bar/straight/triplet divisions. The reference indexes do not establish new launch-grid timing.

Evidence: [C74-LOM-CLIP #launch_quantization](https://docs.cycling74.com/apiref/lom/clip/#launch_quantization), B0073..B0075, retained HTML117..119; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-024 — Clip.legato (properties)

**D-current-public/target-U.** A get/set/observable boolean corresponds to the Legato switch in Launch settings, not a derived playback-position rule.

Evidence: [C74-LOM-CLIP #legato](https://docs.cycling74.com/apiref/lom/clip/#legato), B0076..B0078, retained HTML137..139; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-025 — Clip.length (properties)

**D-current-public/target-U.** Read-only length is loop length when looped and start-to-end distance otherwise, in beats; the source says it is not meaningful for unwarped audio.

Evidence: [C74-LOM-CLIP #length](https://docs.cycling74.com/apiref/lom/clip/#length), B0079..B0081, retained HTML142..144; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-026 — Clip.loop_end (properties)

**D-current-public/target-U.** A get/set/observable float denotes loop end when looped and clip end otherwise; context-dependent units are described alongside loop_start.

Evidence: [C74-LOM-CLIP #loop_end](https://docs.cycling74.com/apiref/lom/clip/#loop_end), B0082..B0084, retained HTML145..147; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-027 — Clip.loop_jump (properties)

**D-current-public/target-U.** Observe-only bang notification corresponds to crossing the loop-start position, including a possible projection into the loop; cadence and exact event payload remain unverified.

Evidence: [C74-LOM-CLIP #loop_jump](https://docs.cycling74.com/apiref/lom/clip/#loop_jump), B0085..B0087, retained HTML149..151; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-028 — Clip.loop_start (properties)

**D-current-public/target-U.** A get/set/observable float denotes loop start or unlooped clip start. MIDI/warped clips use absolute clip beats; unwarped audio uses seconds from the first sample.

Evidence: [C74-LOM-CLIP #loop_start](https://docs.cycling74.com/apiref/lom/clip/#loop_start), B0088..B0090, retained HTML152..154; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-029 — Clip.looping (properties)

**D-current-public/target-U.** The get/set/observable boolean enables looping; the source excludes looping of unwarped audio, without specifying invalid-write behavior.

Evidence: [C74-LOM-CLIP #looping](https://docs.cycling74.com/apiref/lom/clip/#looping), B0091..B0093, retained HTML158..160; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-030 — Clip.muted (properties)

**D-current-public/target-U.** A get/set/observable boolean denotes the Clip Activator being off; this does not specify a sample-level mute ramp.

Evidence: [C74-LOM-CLIP #muted](https://docs.cycling74.com/apiref/lom/clip/#muted), B0094..B0096, retained HTML161..163; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-031 — Clip.name (properties)

**D-current-public/target-U.** The source declares a symbol-valued get/set/observable name and gives no further grammar, maximum length or normalization law.

Evidence: [C74-LOM-CLIP #name](https://docs.cycling74.com/apiref/lom/clip/#name), B0097..B0098, retained HTML164..165; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-032 — Clip.notes (properties)

**D-current-public/target-U.** For MIDI clips only, an observe-only bang signals that the note list changed, not a returned note collection or a complete event ordering protocol.

Evidence: [C74-LOM-CLIP #notes](https://docs.cycling74.com/apiref/lom/clip/#notes), B0099..B0101, retained HTML166..168; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-033 — Clip.warp_markers (properties)

**D-current-public/target-U.** For audio clips, get returns a dictionary of sample_time and beat_time pairs while observe bangs on changes. The source includes an invisible final marker and interpolation context, retained under the existing Warp owner.

Evidence: [C74-LOM-CLIP #warp_markers](https://docs.cycling74.com/apiref/lom/clip/#warp_markers), B0102..B0108, retained HTML170..189; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-034 — Clip.pitch_coarse (properties)

**D-current-public/target-U.** The audio-only get/set/observable integer describes semitone Transpose, with the published minus48-to48 range; this is not a sound or tuning oracle.

Evidence: [C74-LOM-CLIP #pitch_coarse](https://docs.cycling74.com/apiref/lom/clip/#pitch_coarse), B0109..B0111, retained HTML199..201; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-035 — Clip.pitch_fine (properties)

**D-current-public/target-U.** The audio-only get/set/observable float describes cent Detune, with the published minus50-to49 range; rounding and audible pitch remain unknown here.

Evidence: [C74-LOM-CLIP #pitch_fine](https://docs.cycling74.com/apiref/lom/clip/#pitch_fine), B0112..B0114, retained HTML203..205; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-036 — Clip.playing_position (properties)

**D-current-public/target-U.** The read/observable float uses absolute clip beats for MIDI/warped audio and seconds for unwarped audio; stopped position is described as zero, without callback cadence or timing tolerance.

Evidence: [C74-LOM-CLIP #playing_position](https://docs.cycling74.com/apiref/lom/clip/#playing_position), B0115..B0117, retained HTML207..209; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-037 — Clip.playing_status (properties)

**D-current-public/target-U.** An observe-only bang signals a change in playing/trigger status, without a complete transition order or event count.

Evidence: [C74-LOM-CLIP #playing_status](https://docs.cycling74.com/apiref/lom/clip/#playing_status), B0118..B0120, retained HTML216..218; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-038 — Clip.position (properties)

**D-current-public/target-U.** The access line says get/observe, but prose describes setting loop position while preserving loop length and equating its value to loop_start. This conflict remains Q-LCS-001; write capability is not silently added.

Evidence: [C74-LOM-CLIP #position](https://docs.cycling74.com/apiref/lom/clip/#position), B0121..B0123, retained HTML219..221; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-039 — Clip.ram_mode (properties)

**D-current-public/target-U.** A get/set/observable boolean corresponds to an audio clip's RAM switch; no cache, memory or streaming architecture is mandated.

Evidence: [C74-LOM-CLIP #ram_mode](https://docs.cycling74.com/apiref/lom/clip/#ram_mode), B0124..B0126, retained HTML222..224; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-040 — Clip.sample_length (properties)

**D-current-public/target-U.** A get-only integer describes the clip sample length in samples; this supplies no decoder or duration rounding law.

Evidence: [C74-LOM-CLIP #sample_length](https://docs.cycling74.com/apiref/lom/clip/#sample_length), B0127..B0129, retained HTML225..227; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-041 — Clip.sample_rate (properties)

**D-current-public/target-U.** A get-only float reports the clip sample rate; exact source-rate conversion and valid contexts are not otherwise specified here.

Evidence: [C74-LOM-CLIP #sample_rate](https://docs.cycling74.com/apiref/lom/clip/#sample_rate), B0130..B0132, retained HTML228..230; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-042 — Clip.signature_denominator (properties)

**D-current-public/target-U.** A get/set/observable integer is declared for the signature denominator; admissible values and invalid-write policy are not given.

Evidence: [C74-LOM-CLIP #signature_denominator](https://docs.cycling74.com/apiref/lom/clip/#signature_denominator), B0133..B0134, retained HTML231..232; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-043 — Clip.signature_numerator (properties)

**D-current-public/target-U.** A get/set/observable integer is declared for the signature numerator; admissible values and invalid-write policy are not given.

Evidence: [C74-LOM-CLIP #signature_numerator](https://docs.cycling74.com/apiref/lom/clip/#signature_numerator), B0135..B0136, retained HTML233..234; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-044 — Clip.start_marker (properties)

**D-current-public/target-U.** A beat-valued get/set/observable start marker is loop-independent and cannot be placed after the end marker; equality and error handling require evidence.

Evidence: [C74-LOM-CLIP #start_marker](https://docs.cycling74.com/apiref/lom/clip/#start_marker), B0137..B0139, retained HTML235..237; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-045 — Clip.start_time (properties)

**D-current-public/target-U.** A read/observable float describes song-relative start beats, with different Arrangement offset and Session start roles. Session reporting concerns the track's currently playing clip and may be negative after offsets.

Evidence: [C74-LOM-CLIP #start_time](https://docs.cycling74.com/apiref/lom/clip/#start_time), B0140..B0142, retained HTML238..240; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-046 — Clip.velocity_amount (properties)

**D-current-public/target-U.** A get/set/observable float describes how triggering-note velocity affects volume, with zero/no-effect and one/full-effect source endpoints; no interpolation or audio law is inferred.

Evidence: [C74-LOM-CLIP #velocity_amount](https://docs.cycling74.com/apiref/lom/clip/#velocity_amount), B0143..B0145, retained HTML245..247; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-047 — Clip.warp_mode (properties)

**D-current-public/target-U.** The audio-only get/set/observable integer names Beats, Tones, Texture, Re-Pitch, Complex, REX and Complex Pro in this Clip reference; available_warp_modes and the existing finite owner remain necessary.

Evidence: [C74-LOM-CLIP #warp_mode](https://docs.cycling74.com/apiref/lom/clip/#warp_mode), B0146..B0148, retained HTML250..252; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-048 — Clip.warping (properties)

**D-current-public/target-U.** The audio-only get/set/observable boolean corresponds to Warp enablement. The source warns of deferred setting and sequencing surprises; no private scheduling design or delay guarantee follows.

Evidence: [C74-LOM-CLIP #warping](https://docs.cycling74.com/apiref/lom/clip/#warping), B0149..B0151, retained HTML261..263; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-049 — Clip.will_record_on_start (properties)

**D-current-public/target-U.** A get-only boolean has the joint MIDI-clip, triggered, track-armed and MIDI Arrangement Overdub prerequisites; a lone true flag does not prove recorded notes.

Evidence: [C74-LOM-CLIP #will_record_on_start](https://docs.cycling74.com/apiref/lom/clip/#will_record_on_start), B0152..B0154, retained HTML267..269; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-050 — Clip.add_new_notes (functions)

**D-current-public/target-U.** For MIDI clips, the dictionary's notes list contains pitch:int, start_time:float and duration:float, with optional velocity, mute, probability, velocity_deviation and release_velocity fields. A list of newly added note IDs is described as returned; defaults/ranges stay current-source context, not storage or RNG laws.

Evidence: [C74-LOM-CLIP #add_new_notes](https://docs.cycling74.com/apiref/lom/clip/#add_new_notes), B0156..B0157, retained HTML271..272; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-051 — Clip.add_warp_marker (functions)

**D-current-public/target-U.** For warped audio only, a marker dictionary has beat_time and optional sample_time floats. Omitted sample_time is described as preserving timing; explicit sample_time has sample-span, adjacent-order and segment-BPM constraints owned by Warp markers, not new target arithmetic here.

Evidence: [C74-LOM-CLIP #add_warp_marker](https://docs.cycling74.com/apiref/lom/clip/#add_warp_marker), B0158..B0162, retained HTML295..309; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-052 — Clip.apply_note_modifications (functions)

**D-current-public/target-U.** For MIDI clips, a notes dictionary uses note records returned by get_notes_extended; a subset is admitted but the source says a batch containing any absent note is ignored. No partial-commit or event-order protocol is inferred.

Evidence: [C74-LOM-CLIP #apply_note_modifications](https://docs.cycling74.com/apiref/lom/clip/#apply_note_modifications), B0163..B0164, retained HTML313..314; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-053 — Clip.clear_all_envelopes (functions)

**D-current-public/target-U.** The function removes all clip automation according to the source; no return value, undo transaction or sample-accurate side effect is declared.

Evidence: [C74-LOM-CLIP #clear_all_envelopes](https://docs.cycling74.com/apiref/lom/clip/#clear_all_envelopes), B0165..B0166, retained HTML322..323; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-054 — Clip.clear_envelope (functions)

**D-current-public/target-U.** A device_parameter argument is documented as an id; its associated clip automation is removed. Valid parameter identity and envelope ownership must be established independently.

Evidence: [C74-LOM-CLIP #clear_envelope](https://docs.cycling74.com/apiref/lom/clip/#clear_envelope), B0167..B0168, retained HTML324..325; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-055 — Clip.crop (functions)

**D-current-public/target-U.** Cropping uses the loop region when looped and start/end-marker region otherwise. This describes the API operation's region choice, not media rewrite bytes or an implementation of crop.

Evidence: [C74-LOM-CLIP #crop](https://docs.cycling74.com/apiref/lom/clip/#crop), B0169..B0170, retained HTML328..329; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-056 — Clip.deselect_all_notes (functions)

**D-current-public/target-U.** For MIDI clips, deselects notes; the source suggests using it before replace_selected_notes and documents a named id-zero output. That referenced function is not declared in this selected Clip body and is not added to the denominator.

Evidence: [C74-LOM-CLIP #deselect_all_notes](https://docs.cycling74.com/apiref/lom/clip/#deselect_all_notes), B0171..B0172, retained HTML330..331; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-057 — Clip.duplicate_loop (functions)

**D-current-public/target-U.** For MIDI clips, the loop doubles and notes/envelopes duplicate; for an unlooped clip the start/end range is used. Existing region/note/envelope owners retain exact transforms and boundaries.

Evidence: [C74-LOM-CLIP #duplicate_loop](https://docs.cycling74.com/apiref/lom/clip/#duplicate_loop), B0173..B0174, retained HTML336..337; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-058 — Clip.duplicate_notes_by_id (functions)

**D-current-public/target-U.** For MIDI clips, accepts existing note IDs as a list or a dictionary with note_ids and optional destination_time:float/int and transposition_amount:int. Omitted destination follows the selected notes; exact insertion arithmetic is not derived here.

Evidence: [C74-LOM-CLIP #duplicate_notes_by_id](https://docs.cycling74.com/apiref/lom/clip/#duplicate_notes_by_id), B0175..B0176, retained HTML338..339; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-059 — Clip.duplicate_region (functions)

**D-current-public/target-U.** For MIDI clips, region_start, region_length and destination_time are float/int arguments, with optional pitch:int and transposition_amount:int. The source describes pitch-minus1 as all pitches and transposition, without supplying a new region endpoint law.

Evidence: [C74-LOM-CLIP #duplicate_region](https://docs.cycling74.com/apiref/lom/clip/#duplicate_region), B0177..B0178, retained HTML353..354; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-060 — Clip.fire (functions)

**D-current-public/target-U.** The function is described by the Clip Launch button role, without an argument or return declaration; existing launch/playback owners retain actual dispatch and timing.

Evidence: [C74-LOM-CLIP #fire](https://docs.cycling74.com/apiref/lom/clip/#fire), B0179..B0180, retained HTML361..362; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-061 — Clip.get_all_notes_extended (functions)

**D-current-public/target-U.** For MIDI clips, returns a notes dictionary irrespective of markers/loop bounds. Each record has note_id, pitch, start_time, duration, velocity, mute, probability, velocity_deviation and release_velocity; an optional dictionary return-key list selects fields.

Evidence: [C74-LOM-CLIP #get_all_notes_extended](https://docs.cycling74.com/apiref/lom/clip/#get_all_notes_extended), B0181..B0182, retained HTML363..364; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-062 — Clip.get_notes_by_id (functions)

**D-current-public/target-U.** For MIDI clips, existing IDs are passed as a list or a dictionary with note_ids and optional return field-selection list; the returned notes dictionary contains the published record fields. Missing-ID policy is not specified by this valid-ID precondition.

Evidence: [C74-LOM-CLIP #get_notes_by_id](https://docs.cycling74.com/apiref/lom/clip/#get_notes_by_id), B0183..B0184, retained HTML388..389; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-063 — Clip.get_notes_extended (functions)

**D-current-public/target-U.** For MIDI clips, from_pitch:int, pitch_span:int, from_time:float and time_span:float select note starts; times are beats. The alternative dictionary uses these keys and optional return field list; returned records contain the published extended note fields.

Evidence: [C74-LOM-CLIP #get_notes_extended](https://docs.cycling74.com/apiref/lom/clip/#get_notes_extended), B0185..B0186, retained HTML416..417; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-064 — Clip.get_selected_notes_extended (functions)

**D-current-public/target-U.** For MIDI clips, returns selected-note records with the published extended fields; an optional dictionary return field-list narrows the record keys. Selection identity and ordering remain separate questions.

Evidence: [C74-LOM-CLIP #get_selected_notes_extended](https://docs.cycling74.com/apiref/lom/clip/#get_selected_notes_extended), B0187..B0188, retained HTML447..448; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-065 — Clip.move_playing_pos (functions)

**D-current-public/target-U.** A beats:float argument requests an unquantized relative jump, including negative/backward direction. Unwarped audio, recording audio and recording non-overdub MIDI are expressly excluded; no scheduling or jump-sample oracle is added.

Evidence: [C74-LOM-CLIP #move_playing_pos](https://docs.cycling74.com/apiref/lom/clip/#move_playing_pos), B0189..B0190, retained HTML472..473; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-066 — Clip.move_warp_marker (functions)

**D-current-public/target-U.** beat_time:float identifies a marker and beat_time_distance:float requests its movement; exact constraints/conversions stay with the existing Warp owner.

Evidence: [C74-LOM-CLIP #move_warp_marker](https://docs.cycling74.com/apiref/lom/clip/#move_warp_marker), B0191..B0192, retained HTML477..478; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-067 — Clip.quantize (functions)

**D-current-public/target-U.** quantization_grid:int and amount:float request quantization of all clip notes with song swing_amount taken into account; no grid enum, rounding, swing or numeric transform is inferred.

Evidence: [C74-LOM-CLIP #quantize](https://docs.cycling74.com/apiref/lom/clip/#quantize), B0193..B0194, retained HTML481..482; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-068 — Clip.quantize_pitch (functions)

**D-current-public/target-U.** pitch:int, quantization_grid:int and amount:float apply the quantize role to one pitch; the source does not supply an independent quantization algorithm.

Evidence: [C74-LOM-CLIP #quantize_pitch](https://docs.cycling74.com/apiref/lom/clip/#quantize_pitch), B0195..B0196, retained HTML486..487; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-069 — Clip.remove_notes_by_id (functions)

**D-current-public/target-U.** A list of IDs associated with existing notes requests deletion of those notes; note-ID lifetime, invalid batches and serialization are not derived from this valid-ID statement.

Evidence: [C74-LOM-CLIP #remove_notes_by_id](https://docs.cycling74.com/apiref/lom/clip/#remove_notes_by_id), B0197..B0198, retained HTML492..493; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-070 — Clip.remove_notes_extended (functions)

**D-current-public/target-U.** from_pitch:int, pitch_span:int, from_time:float and time_span:float request deletion of notes whose starts lie in the area; times are beats, but edge inclusivity remains unresolved.

Evidence: [C74-LOM-CLIP #remove_notes_extended](https://docs.cycling74.com/apiref/lom/clip/#remove_notes_extended), B0199..B0200, retained HTML499..500; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-071 — Clip.remove_warp_marker (functions)

**D-current-public/target-U.** beat_time:float identifies the marker requested for removal; marker-count, shadow and refusal constraints retain the existing Warp owner.

Evidence: [C74-LOM-CLIP #remove_warp_marker](https://docs.cycling74.com/apiref/lom/clip/#remove_warp_marker), B0201..B0202, retained HTML508..509; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-072 — Clip.scrub (functions)

**D-current-public/target-U.** beat_time:float requests mouse-like scrubbing that respects Global Quantization and continues until stop_scrub. This is a dispatch role, without a new transport or sample-timing law.

Evidence: [C74-LOM-CLIP #scrub](https://docs.cycling74.com/apiref/lom/clip/#scrub), B0203..B0204, retained HTML511..512; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-073 — Clip.select_all_notes (functions)

**D-current-public/target-U.** For MIDI clips, selects all notes independently of prior selection; the source documents a named id-zero output, not a new note-ID protocol.

Evidence: [C74-LOM-CLIP #select_all_notes](https://docs.cycling74.com/apiref/lom/clip/#select_all_notes), B0205..B0206, retained HTML514..515; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-074 — Clip.select_notes_by_id (functions)

**D-current-public/target-U.** A list of note IDs selects associated notes; unlike other valid-ID descriptions, the source explicitly says nonexistent IDs do not print a warning/error. Actual result selection and message delivery remain target-U.

Evidence: [C74-LOM-CLIP #select_notes_by_id](https://docs.cycling74.com/apiref/lom/clip/#select_notes_by_id), B0207..B0208, retained HTML521..522; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-075 — Clip.set_fire_button_state (functions)

**D-current-public/target-U.** state:bool represents a held clip-start button when true until false or another stop; it is not a proof of Gate/Toggle/Repeat timing or release policy.

Evidence: [C74-LOM-CLIP #set_fire_button_state](https://docs.cycling74.com/apiref/lom/clip/#set_fire_button_state), B0209..B0210, retained HTML529..530; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-076 — Clip.stop (functions)

**D-current-public/target-U.** The function has the track-stop-button role only for this clip actually playing or recording; a merely triggered clip or another clip playing has no effect according to the source.

Evidence: [C74-LOM-CLIP #stop](https://docs.cycling74.com/apiref/lom/clip/#stop), B0211..B0212, retained HTML532..533; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-077 — Clip.stop_scrub (functions)

**D-current-public/target-U.** The function stops an active scrub; inactive, deleted-object and transport transition policies are not specified.

Evidence: [C74-LOM-CLIP #stop_scrub](https://docs.cycling74.com/apiref/lom/clip/#stop_scrub), B0213..B0214, retained HTML534..535; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-078 — Clip.View.grid_is_triplet (properties)

**D-current-public/target-U.** A get/set boolean controls whether the displayed clip grid is triplet; observe access is not declared.

Evidence: [C74-LOM-CLIP_VIEW #grid_is_triplet](https://docs.cycling74.com/apiref/lom/clip_view/#grid_is_triplet), B0006..B0008, retained HTML34..36; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-079 — Clip.View.grid_quantization (properties)

**D-current-public/target-U.** A get/set integer controls displayed grid quantization; no enum or exact note-quantization law is supplied.

Evidence: [C74-LOM-CLIP_VIEW #grid_quantization](https://docs.cycling74.com/apiref/lom/clip_view/#grid_quantization), B0009..B0011, retained HTML37..39; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-080 — Clip.View.hide_envelope (functions)

**D-current-public/target-U.** The function hides the Envelopes box, without a declared parameter or return value.

Evidence: [C74-LOM-CLIP_VIEW #hide_envelope](https://docs.cycling74.com/apiref/lom/clip_view/#hide_envelope), B0013..B0014, retained HTML41..42; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-081 — Clip.View.select_envelope_parameter (functions)

**D-current-public/target-U.** A DeviceParameter argument selects that parameter in the Envelopes box; invalid or absent envelope parameters require separate evidence.

Evidence: [C74-LOM-CLIP_VIEW #select_envelope_parameter](https://docs.cycling74.com/apiref/lom/clip_view/#select_envelope_parameter), B0015..B0016, retained HTML43..44; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-082 — Clip.View.show_envelope (functions)

**D-current-public/target-U.** The function shows the Envelopes box; API return/callback and focus side effects remain unknown.

Evidence: [C74-LOM-CLIP_VIEW #show_envelope](https://docs.cycling74.com/apiref/lom/clip_view/#show_envelope), B0017..B0018, retained HTML46..47; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-083 — Clip.View.show_loop (functions)

**D-current-public/target-U.** Only when the clip is visible in Detail View, the function brings its current loop into view; this does not declare zoom geometry or a hidden-clip selection operation.

Evidence: [C74-LOM-CLIP_VIEW #show_loop](https://docs.cycling74.com/apiref/lom/clip_view/#show_loop), B0019..B0020, retained HTML48..49; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-084 — Sample.beats_granulation_resolution (properties)

**D-current-public/target-U.** A get/set/observable integer selects Beats divisions from a bar through thirty-seconds or Transients, as listed; it does not specify a time-stretch algorithm.

Evidence: [C74-LOM-SAMPLE #beats_granulation_resolution](https://docs.cycling74.com/apiref/lom/sample/#beats_granulation_resolution), B0006..B0008, retained HTML34..36; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-085 — Sample.beats_transient_envelope (properties)

**D-current-public/target-U.** A get/set/observable float describes the per-segment fade duration in Beats mode, with source endpoints fastest decay and no fade; no numeric envelope curve is established.

Evidence: [C74-LOM-SAMPLE #beats_transient_envelope](https://docs.cycling74.com/apiref/lom/sample/#beats_transient_envelope), B0009..B0011, retained HTML44..46; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-086 — Sample.beats_transient_loop_mode (properties)

**D-current-public/target-U.** A get/set/observable integer selects Off, Forward or Back-and-Forth per-segment transient looping in Beats mode; no audio boundary algorithm follows.

Evidence: [C74-LOM-SAMPLE #beats_transient_loop_mode](https://docs.cycling74.com/apiref/lom/sample/#beats_transient_loop_mode), B0012..B0014, retained HTML50..52; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-087 — Sample.complex_pro_envelope (properties)

**D-current-public/target-U.** A get/set/observable float controls the Envelope parameter in Complex Pro mode; range, units and signal law are omitted.

Evidence: [C74-LOM-SAMPLE #complex_pro_envelope](https://docs.cycling74.com/apiref/lom/sample/#complex_pro_envelope), B0015..B0017, retained HTML56..58; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-088 — Sample.complex_pro_formants (properties)

**D-current-public/target-U.** A get/set/observable float controls the Formants parameter in Complex Pro mode; range, units and signal law are omitted.

Evidence: [C74-LOM-SAMPLE #complex_pro_formants](https://docs.cycling74.com/apiref/lom/sample/#complex_pro_formants), B0018..B0020, retained HTML59..61; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-089 — Sample.end_marker (properties)

**D-current-public/target-U.** A get/set/observable integer denotes the sample end-marker position; the member body does not explicitly give units or bounds.

Evidence: [C74-LOM-SAMPLE #end_marker](https://docs.cycling74.com/apiref/lom/sample/#end_marker), B0021..B0023, retained HTML62..64; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-090 — Sample.file_path (properties)

**D-current-public/target-U.** A read/observable unicode property identifies the sample file path; write access is not declared.

Evidence: [C74-LOM-SAMPLE #file_path](https://docs.cycling74.com/apiref/lom/sample/#file_path), B0024..B0026, retained HTML65..67; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-091 — Sample.gain (properties)

**D-current-public/target-U.** A get/set/observable float controls sample gain; this declaration supplies no range, units, mapping or clipping law.

Evidence: [C74-LOM-SAMPLE #gain](https://docs.cycling74.com/apiref/lom/sample/#gain), B0027..B0029, retained HTML68..70; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-092 — Sample.length (properties)

**D-current-public/target-U.** A get-only integer gives sample-file length in sample frames, not clip beats or bytes.

Evidence: [C74-LOM-SAMPLE #length](https://docs.cycling74.com/apiref/lom/sample/#length), B0030..B0032, retained HTML71..73; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-093 — Sample.sample_rate (properties)

**D-current-public/target-U.** A get-only integer gives the loaded sample rate; this differs from Clip's float declaration and is not silently coerced.

Evidence: [C74-LOM-SAMPLE #sample_rate](https://docs.cycling74.com/apiref/lom/sample/#sample_rate), B0033..B0035, retained HTML74..76; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-094 — Sample.slices (properties)

**D-current-public/target-U.** A read/observable list of integers gives playable-slice positions in sample frames. The source describes division by sample_rate for seconds; no target numerical conversion or rounding oracle is added.

Evidence: [C74-LOM-SAMPLE #slices](https://docs.cycling74.com/apiref/lom/sample/#slices), B0036..B0038, retained HTML79..81; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-095 — Sample.slicing_sensitivity (properties)

**D-current-public/target-U.** A get/set/observable float controls slicing sensitivity in the published zero-to-one domain; threshold/detection and clamp behavior are not supplied.

Evidence: [C74-LOM-SAMPLE #slicing_sensitivity](https://docs.cycling74.com/apiref/lom/sample/#slicing_sensitivity), B0039..B0041, retained HTML84..86; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-096 — Sample.start_marker (properties)

**D-current-public/target-U.** A get/set/observable integer denotes sample start-marker position; units, equality and refusal policy are not explicitly declared by this member.

Evidence: [C74-LOM-SAMPLE #start_marker](https://docs.cycling74.com/apiref/lom/sample/#start_marker), B0042..B0044, retained HTML87..89; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-097 — Sample.texture_flux (properties)

**D-current-public/target-U.** A get/set/observable float controls Flux in Texture mode; no range or randomness law is inferred.

Evidence: [C74-LOM-SAMPLE #texture_flux](https://docs.cycling74.com/apiref/lom/sample/#texture_flux), B0045..B0047, retained HTML90..92; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-098 — Sample.texture_grain_size (properties)

**D-current-public/target-U.** A get/set/observable float controls Grain Size in Texture mode; no units or synthesis law are supplied.

Evidence: [C74-LOM-SAMPLE #texture_grain_size](https://docs.cycling74.com/apiref/lom/sample/#texture_grain_size), B0048..B0050, retained HTML93..95; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-099 — Sample.tones_grain_size (properties)

**D-current-public/target-U.** A get/set/observable float controls Grain Size in Tones mode; no units or synthesis law are supplied.

Evidence: [C74-LOM-SAMPLE #tones_grain_size](https://docs.cycling74.com/apiref/lom/sample/#tones_grain_size), B0051..B0053, retained HTML96..98; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-100 — Sample.warp_markers (properties)

**D-current-public/target-U.** Get returns a marker dictionary and observe bangs on changes. The source describes a hidden final marker for the last segment's BPM but does not repeat Clip's dictionary schema; it is not fabricated by inheritance.

Evidence: [C74-LOM-SAMPLE #warp_markers](https://docs.cycling74.com/apiref/lom/sample/#warp_markers), B0054..B0056, retained HTML99..101; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-101 — Sample.warp_mode (properties)

**D-current-public/target-U.** A get/set/observable integer names Beats, Tones, Texture, Re-Pitch, Complex and Complex Pro. The Sample list omits Clip's REX entry; these lists are not unified or used to replace finite Warp storage enums.

Evidence: [C74-LOM-SAMPLE #warp_mode](https://docs.cycling74.com/apiref/lom/sample/#warp_mode), B0057..B0059, retained HTML106..108; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-102 — Sample.warping (properties)

**D-current-public/target-U.** A get/set/observable boolean denotes Warp enabled, without borrowing Clip's deferral warning as a Sample guarantee.

Evidence: [C74-LOM-SAMPLE #warping](https://docs.cycling74.com/apiref/lom/sample/#warping), B0060..B0062, retained HTML115..117; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-103 — Sample.slicing_style (properties)

**D-current-public/target-U.** A get/set/observable integer names Transient, Beat, Region and Manual slicing modes; the numeric list is current-source context only.

Evidence: [C74-LOM-SAMPLE #slicing_style](https://docs.cycling74.com/apiref/lom/sample/#slicing_style), B0063..B0065, retained HTML118..120; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-104 — Sample.slicing_beat_division (properties)

**D-current-public/target-U.** A get/set/observable integer selects the listed straight/triplet divisions or bar multiples in Beat Slicing mode; no region generation or boundary law is inferred.

Evidence: [C74-LOM-SAMPLE #slicing_beat_division](https://docs.cycling74.com/apiref/lom/sample/#slicing_beat_division), B0066..B0068, retained HTML125..127; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-105 — Sample.slicing_region_count (properties)

**D-current-public/target-U.** A get/set/observable integer selects region count in Region Slicing mode; admissible count domain and partition rounding remain unknown.

Evidence: [C74-LOM-SAMPLE #slicing_region_count](https://docs.cycling74.com/apiref/lom/sample/#slicing_region_count), B0069..B0071, retained HTML139..141; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-106 — Sample.gain_display_string (functions)

**D-current-public/target-U.** The function explicitly returns a list of symbols representing gain text; unlike Clip's gain_display_string property, this is a function. Example formatting is not a locale/precision grammar.

Evidence: [C74-LOM-SAMPLE #gain_display_string](https://docs.cycling74.com/apiref/lom/sample/#gain_display_string), B0073..B0074, retained HTML143..144; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-107 — Sample.insert_slice (functions)

**D-current-public/target-U.** slice_time:int requests adding a slice only when one is absent at that time; unit, valid interval, duplicates and resulting IDs require evidence.

Evidence: [C74-LOM-SAMPLE #insert_slice](https://docs.cycling74.com/apiref/lom/sample/#insert_slice), B0075..B0076, retained HTML145..146; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-108 — Sample.move_slice (functions)

**D-current-public/target-U.** source_time:int and destination_time:int request moving an existing slice; collision, ordering and endpoint policy are not specified.

Evidence: [C74-LOM-SAMPLE #move_slice](https://docs.cycling74.com/apiref/lom/sample/#move_slice), B0077..B0078, retained HTML148..149; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-109 — Sample.remove_slice (functions)

**D-current-public/target-U.** slice_time:int requests removal if a slice exists there; minimum-slice and absent-slice event policies are not specified.

Evidence: [C74-LOM-SAMPLE #remove_slice](https://docs.cycling74.com/apiref/lom/sample/#remove_slice), B0079..B0080, retained HTML151..152; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-110 — Sample.clear_slices (functions)

**D-current-public/target-U.** The function clears slices created in Manual Slicing mode; it does not claim deletion of arbitrary automatic-mode slices or sample audio.

Evidence: [C74-LOM-SAMPLE #clear_slices](https://docs.cycling74.com/apiref/lom/sample/#clear_slices), B0081..B0082, retained HTML154..155; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-111 — Sample.reset_slices (functions)

**D-current-public/target-U.** The function returns edited slices to original positions; original-baseline identity and interaction with added/removed slices are not specified.

Evidence: [C74-LOM-SAMPLE #reset_slices](https://docs.cycling74.com/apiref/lom/sample/#reset_slices), B0083..B0084, retained HTML156..157; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-112 — SimplerDevice.sample (children)

**D-current-public/target-U.** A get/observable Sample child represents the currently loaded sample; object replacement and old-ID invalidation are separate lifecycle questions.

Evidence: [C74-LOM-SIMPLERDEVICE #sample](https://docs.cycling74.com/apiref/lom/simplerdevice/#sample), B0004..B0006, retained HTML32..34; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-113 — SimplerDevice.can_warp_as (properties)

**D-current-public/target-U.** A read/observable boolean indicates availability of warp_as, not successful execution or an inferred availability formula.

Evidence: [C74-LOM-SIMPLERDEVICE #can_warp_as](https://docs.cycling74.com/apiref/lom/simplerdevice/#can_warp_as), B0008..B0010, retained HTML36..38; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-114 — SimplerDevice.can_warp_double (properties)

**D-current-public/target-U.** A read/observable boolean indicates availability of warp_double; the source does not define its exact capability predicate.

Evidence: [C74-LOM-SIMPLERDEVICE #can_warp_double](https://docs.cycling74.com/apiref/lom/simplerdevice/#can_warp_double), B0011..B0013, retained HTML39..41; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-115 — SimplerDevice.can_warp_half (properties)

**D-current-public/target-U.** A read/observable boolean indicates availability of warp_half; unavailable capability is not a negative success.

Evidence: [C74-LOM-SIMPLERDEVICE #can_warp_half](https://docs.cycling74.com/apiref/lom/simplerdevice/#can_warp_half), B0014..B0016, retained HTML42..44; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-116 — SimplerDevice.multi_sample_mode (properties)

**D-current-public/target-U.** A read/observable boolean indicates multisample mode; transitions and sample-child behavior in this mode are not specified.

Evidence: [C74-LOM-SIMPLERDEVICE #multi_sample_mode](https://docs.cycling74.com/apiref/lom/simplerdevice/#multi_sample_mode), B0017..B0019, retained HTML45..47; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-117 — SimplerDevice.pad_slicing (properties)

**D-current-public/target-U.** A get/set/observable boolean enables adding slices in Slicing mode by playing notes not assigned to existing slices; note-to-slice mapping is not supplied.

Evidence: [C74-LOM-SIMPLERDEVICE #pad_slicing](https://docs.cycling74.com/apiref/lom/simplerdevice/#pad_slicing), B0020..B0022, retained HTML48..50; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-118 — SimplerDevice.playback_mode (properties)

**D-current-public/target-U.** A get/set/observable integer names Classic, One-Shot and Slicing; it does not prove the full voice/envelope/signal law of any mode.

Evidence: [C74-LOM-SIMPLERDEVICE #playback_mode](https://docs.cycling74.com/apiref/lom/simplerdevice/#playback_mode), B0023..B0025, retained HTML51..53; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-119 — SimplerDevice.playing_position (properties)

**D-current-public/target-U.** A read/observable float gives a source-described normalized sample position between zero and one; update cadence, stopped values and interpolation are not specified.

Evidence: [C74-LOM-SIMPLERDEVICE #playing_position](https://docs.cycling74.com/apiref/lom/simplerdevice/#playing_position), B0026..B0028, retained HTML57..59; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-120 — SimplerDevice.playing_position_enabled (properties)

**D-current-public/target-U.** A read/observable boolean jointly describes sample playback and displayed position; it is not a settable enable control in this reference.

Evidence: [C74-LOM-SIMPLERDEVICE #playing_position_enabled](https://docs.cycling74.com/apiref/lom/simplerdevice/#playing_position_enabled), B0029..B0031, retained HTML60..62; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-121 — SimplerDevice.retrigger (properties)

**D-current-public/target-U.** A get/set/observable boolean denotes Retrigger enabled; exact voice restart or phase behavior remains owned by Simpler and unresolved where not evidenced.

Evidence: [C74-LOM-SIMPLERDEVICE #retrigger](https://docs.cycling74.com/apiref/lom/simplerdevice/#retrigger), B0032..B0034, retained HTML63..65; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-122 — SimplerDevice.slicing_playback_mode (properties)

**D-current-public/target-U.** A get/set/observable integer names Mono, Poly and Thru for Slicing playback; note allocation and release law are not inferred.

Evidence: [C74-LOM-SIMPLERDEVICE #slicing_playback_mode](https://docs.cycling74.com/apiref/lom/simplerdevice/#slicing_playback_mode), B0035..B0037, retained HTML66..68; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-123 — SimplerDevice.voices (properties)

**D-current-public/target-U.** A get/set/observable integer selects voice count; no admissible domain, stealing order or audio implementation is supplied.

Evidence: [C74-LOM-SIMPLERDEVICE #voices](https://docs.cycling74.com/apiref/lom/simplerdevice/#voices), B0038..B0040, retained HTML72..74; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-124 — SimplerDevice.crop (functions)

**D-current-public/target-U.** The function crops the loaded sample to the active start/end-marker region; file identity, destructive/non-destructive behavior and exact sample output remain unknown.

Evidence: [C74-LOM-SIMPLERDEVICE #crop](https://docs.cycling74.com/apiref/lom/simplerdevice/#crop), B0042..B0043, retained HTML76..77; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-125 — SimplerDevice.guess_playback_length (functions)

**D-current-public/target-U.** The function explicitly returns a float estimate of beat-time playback length between start/end markers; the estimation algorithm, accuracy and determinism are not supplied.

Evidence: [C74-LOM-SIMPLERDEVICE #guess_playback_length](https://docs.cycling74.com/apiref/lom/simplerdevice/#guess_playback_length), B0044..B0045, retained HTML78..79; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-126 — SimplerDevice.reverse (functions)

**D-current-public/target-U.** The function reverses the loaded sample according to the source, without specifying file rewriting, markers, Warp, slice transforms or waveform oracles.

Evidence: [C74-LOM-SIMPLERDEVICE #reverse](https://docs.cycling74.com/apiref/lom/simplerdevice/#reverse), B0046..B0047, retained HTML80..81; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-127 — SimplerDevice.warp_as (functions)

**D-current-public/target-U.** beats:int requests warping the active start/end-marker region to that beat count; capability must be admitted via can_warp_as, and numeric/audio laws remain with Warp/Simpler owners.

Evidence: [C74-LOM-SIMPLERDEVICE #warp_as](https://docs.cycling74.com/apiref/lom/simplerdevice/#warp_as), B0048..B0049, retained HTML82..83; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-128 — SimplerDevice.warp_double (functions)

**D-current-public/target-U.** The function requests doubling playback tempo for the active start/end-marker region; can_warp_double is an independent availability prerequisite, not a derived two-times waveform oracle.

Evidence: [C74-LOM-SIMPLERDEVICE #warp_double](https://docs.cycling74.com/apiref/lom/simplerdevice/#warp_double), B0050..B0051, retained HTML85..86; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-129 — SimplerDevice.warp_half (functions)

**D-current-public/target-U.** The function requests halving playback tempo for the active start/end-marker region; can_warp_half is an independent prerequisite, without a new time-stretch law.

Evidence: [C74-LOM-SIMPLERDEVICE #warp_half](https://docs.cycling74.com/apiref/lom/simplerdevice/#warp_half), B0052..B0053, retained HTML87..88; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-130 — SimplerDevice.replace_sample (functions)

**D-current-public/target-U.** file_path:symbol must name an absolute path to a valid supported audio file; it requests replacement of the loaded sample. Format eligibility, dependencies, object lifetime and media bytes remain separately owned.

Evidence: [C74-LOM-SIMPLERDEVICE #replace_sample](https://docs.cycling74.com/apiref/lom/simplerdevice/#replace_sample), B0054..B0055, retained HTML89..90; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-131 — SimplerDevice.View.selected_slice (properties)

**D-current-public/target-U.** A get/set/observable integer identifies the selected slice by its slice time, rather than an inferred list index; empty/missing-slice and unit semantics remain unknown.

Evidence: [C74-LOM-SIMPLERDEVICE_VIEW #selected_slice](https://docs.cycling74.com/apiref/lom/simplerdevice_view/#selected_slice), B0004..B0006, retained HTML32..34; exact bytes/hash and argument/access context in the member ledger.

### REQ-LAPI-CLIP-SAMPLE-132 — Target applicability and inherited closure

**U/target-U.** Exact12.4.3 presence, signatures and behavior of all five current-public references remain unknown. SimplerDevice inherits Device and SimplerDevice.View inherits Device.View by source description only; no generic inherited members are flattened or counted as specified here.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-133 — Access and type refusal

**U/target-U.** Wrong property types, read-only writes, unsupported observation and function arity/return/error policy remain unknown, including Clip position access/prose disagreement. No bridge success/failure format is supplied here.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-134 — Object and capability lifetime

**U/target-U.** Missing/deleted clip, replaced sample, stale ID, missing view, absent warp capability and multisample contexts remain unknown; unavailable prerequisites are not negative passes.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-135 — Notes dictionary and identity

**U/target-U.** Malformed note dictionaries, absent/duplicate/stale IDs, mixed valid-invalid batches, optional return lists, field coercion, ordering and atomicity remain unknown except explicitly retained source predicates; storage IDs and API IDs are not presumed identical.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-136 — Clip context and region boundaries

**U/target-U.** Audio/MIDI, Session/Arrangement/TakeLane, recording/overdub, loop/Warp and start/end relationships require independent context evidence; edge equality, reversed/empty intervals and unit conversion remain unknown where not already owned.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-137 — Warp, slice and mode dependencies

**U/target-U.** Warp availability/mode changes, slice collision/minimum counts, original reset baselines, multisample and playback/slicing mode dependencies remain unknown; Clip and Sample marker dictionaries/enums are not unified.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-138 — Tuning, expression and quantization

**U/target-U.** Tuning/MPE, note probability/velocity deviation, grid/swing/amount and voice/retrigger interactions are not numeric, RNG, MIDI-message or signal laws derived from member names.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-139 — Media and dependency operations

**U/target-U.** Sample replacement/crop/reverse, clip crop and RAM/gain/path roles give no file rewrite, codec/dependency/cache/format, gain/sound or transaction guarantees.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-140 — Event, transport and rate lifecycle

**U/target-U.** Observer payload/cadence/order, stopped/playing/recording transitions, transport jumps, Warp deferral and sample-rate effects remain unknown; a bang description is not an event-count or timing oracle.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-141 — Persistence and transactional editing

**U/target-U.** Undo/redo, cancellation, save/reopen, object/track reorder and cross-object identity preservation remain unknown; existing finite storage rules are not proof of API transactions.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-142 — Initialization and teardown

**U/target-U.** Binding before initialization, closing/reopening Set/device/clip view, observer detach/rebind, source loss and teardown behavior remain unknown and retain generic bridge ownership.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

### REQ-LAPI-CLIP-SAMPLE-143 — Undeclared units and signatures

**U/target-U.** Where these bodies omit units, ranges, argument forms, returns or access, those details remain unknown. Clip.View grid indexes and Sample marker/slice argument units are not guessed from UI or similarly named fields.

Evidence: unresolved; no supported target oracle. See local research questions and proposed cases.

## Case and source indexes

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/requirements.json), [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/cases.json),
[sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/sources.json), [complete selected reference blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/source-blocks.json)
and [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-clip-sample/counts.json) are retained with read-only validation, canonical
snapshots and a sealed manifest. One member case can contain distinct proposed
access branches and does not prove complete positive/negative/boundary coverage.
Unknown cases are separately scoped to refusal, malformed data, identity, mode,
region, lifecycle and dependency interactions. All remain unexecuted.
