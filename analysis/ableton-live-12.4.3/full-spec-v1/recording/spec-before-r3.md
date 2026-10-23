---
id: SPEC-RECORDING-COMPING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Recording, Capture MIDI and comping

## Scope

FEAT-RECORDING: turn selected audio/MIDI input into clips, retain takes, retrieve
recent MIDI input and assemble an Arrangement comp. This draft owns recording
transitions, count-in, punch, Capture MIDI, take-lane operations and their
recording-specific persistence/undo questions. It distinguishes recording new
input from recording Session playback into Arrangement. It describes behavior,
file and UI semantics; it supplies no measured audio/timing equivalence.

Dependencies retain their canonical ownership: [clip launch](clip-launch.md)
owns launch grids and record-quantization enum values; [MIDI note
storage](midi-note-storage.md) owns saved notes; [Live Set
structure](live-set-structure.md) owns sample references and general document
reading; [transport](transport-state.md), [playback](playback-core.md),
[warp](warp-markers.md) and [automation](automation-envelopes.md) own their
existing contracts. Their playback/load evidence does not prove recording.
General routing, hardware setup, DSP, automation writing and platform dialogs
are outside this draft except where needed to state a recording boundary.

## Evidence and grading

- **D12**: observed documentation in the official online Live **12** manual,
  captured 2026-10-19. The patch/build is unstated. A D12 clause describes
  documented behavior; its applicability to **12.4.3 remains U**.
- **D12403**: observed bytes in the pinned bundle's schema/shipped documents.
  This proves the named storage inventory, not the result of a recording action.
- **S-inventory**: retained native corpus strings/reference inventory only;
  no state transition is inferred from a name or reference.
- **X**: extracted original execution; **none** for this draft.
- **U**: insufficient evidence. No comparator, tolerance or pass is invented.

All cases below are unexecuted; D12 cases have a documented comparator but are
**ungraded for the pinned target**. D12403 cases permit a static artifact audit
only. No application compatibility pass or released handoff exists. Evidence
keys and exact HTML section IDs are in the [appendix](#analyst-evidence-appendix).

## Requirements

### REQ-RECORDING-COMPING-001 — input and arm selection

**D12, R19 §19.1–19.2.** A track records the input selected in its In/Out
controls. Audio inputs can be mono/stereo; MIDI input can select device/channel;
another track can be the source. Session and Arrangement Arm controls address
the same tracks. In the documented ordinary arm operation, clicking one Arm
disarms other tracks; Ctrl on Windows/Cmd on macOS allows multiple arms.
For multiple selected tracks, clicking an Arm arms the other selected tracks.
Arming selects the track. **U:** preference-dependent exceptions, implicit arm,
frozen/nonrecordable tracks and arm changes during recording.

### REQ-RECORDING-COMPING-002 — input monitoring

**D12, R17 §17.1.** Auto passes input when armed and inhibits monitoring while
clips play. In continuously passes input and suppresses clip output regardless
of arm. Off disables monitoring; it permits recording with external monitoring.
A Monitor choice applies to all selected tracks. This clause specifies a
selection/gating result, not a latency or signal-processing tolerance.
**U:** factory/new-track defaults: R19 §19.2 calls monitoring of armed tracks
the default, while R17 §17.1 describes reset defaults of Off for audio and Auto
for MIDI. Preserve the contextual distinction; do not impose one global default.

### REQ-RECORDING-COMPING-003 — Arrangement record start

**D12, R19 §19.3.1.** With Start Playback with Record enabled, Arrangement
Record starts recording. Disabled, Record waits for Play or a Session clip
launch. Shift while pressing Record reverses that preference's behavior.
Recording creates clips on armed tracks. **U:** exact scheduler order at the
start event and pressing Record again before the delayed start.

### REQ-RECORDING-COMPING-004 — Arrangement MIDI overdub

**D12, R19 §19.3.1.** With MIDI Arrangement Overdub enabled, a new MIDI clip
combines the track's existing MIDI signal and new input. The function applies
to MIDI tracks. It does not define an audio overdub operation. **U:** overlapping
same-pitch note merge/retrigger rules and exact behavior with Overdub disabled.

### REQ-RECORDING-COMPING-005 — punch gates

**D12, R19 §19.3.1.** Enabled Punch-In prevents recording before the Arrangement
loop start. Enabled Punch-Out prevents recording after its loop end. These
allow a pre-roll without recording over protected material. **U:** ownership of
an event exactly at either endpoint, held-note splitting, sample alignment and
moving the loop/punch points during recording.

### REQ-RECORDING-COMPING-006 — retention across audio loop passes

**D12, R19 §19.3.1.** Arrangement loop recording retains audio across passes.
The resulting sample can contain the whole recorded run; Clip View's loop
brace selects the last pass and moving its markers can audition prior passes.
The manual also describes repeated Undo to unroll the recording. Take-lane
creation is REQ-018. **U:** partial last passes, segmentation between files,
pass-specific Undo granularity and disk reclamation.

### REQ-RECORDING-COMPING-007 — Session slot record and playback

**D12, R19 §19.3.2.** Empty slots on armed tracks show record controls. Session
Record records the selected scene in armed tracks; the recording clip has a red
launch control. Pressing Session Record again changes recording to loop
playback. A slot's record control starts that slot; its launch control changes
it to loop playback. Clip Stop or transport Stop stops the clip. A non-None
Global Quantization is the documented setup for musically cut clips.
**U:** exact recording start/end scheduling and occupied-slot behavior.

### REQ-RECORDING-COMPING-008 — scene launch and New

**D12, R19 §19.3.2.** By default a scene launch does not record its empty armed
slots; Start Recording on Scene Launch enables that behavior. New stops clips
in armed tracks and selects a scene available for new recordings, creating a
scene when needed. The captured manual exposes New in Key/MIDI Map Mode.
**U:** the scene-search ordering and interaction with follow actions.

### REQ-RECORDING-COMPING-009 — Session MIDI overdub

**D12, R19 §19.3.3.** In an armed MIDI track with a looping clip, Session Record
adds played notes on successive passes. Further presses toggle between
overdub and playback so rehearsal input is not added while overdub is off.
Undo can remove the last take while overdubbing; note editing remains
available. **U:** precise take grouping, duplicate-note handling and Undo while
a note is held. This is independent of Arrangement Overdub (REQ-004).

### REQ-RECORDING-COMPING-010 — stopped-transport step recording

**D12, R19 §19.3.4.** With the MIDI track armed, clip editor Preview enabled
and an insert marker placed, Right Arrow advances by the editor grid and adds
held notes. Continuing to hold while advancing extends them. Left Arrow with
those keys held removes newly entered notes. Transport need not run.
**U:** grid-off behavior, event timing while keys change and undo grouping.

### REQ-RECORDING-COMPING-011 — record quantization and undo

**D12, R19 §19.5.** Record Quantization aligns incoming notes to the selected
subdivision. For Arrangement recording its quantization is a separate Undo
step: Undo can remove quantization while retaining the recording. The setting
cannot change during ordinary Session/Arrangement recording; during overdub
with Clip View Loop on, changes apply immediately and their quantization is
not separately undoable. These are distinct documented modes. Enum/storage
values remain [REQ-CLIP-LAUNCH-006](clip-launch.md#req-clip-launch-006--record-quantization-values).
**U:** rounding/ties, note-off treatment, mixed-grid selection and exact input
timestamps. No grid formula is imported from clip launching.

### REQ-RECORDING-COMPING-012 — count-in

**D12, R19 §19.6.** A non-None count-in delays recording until it finishes.
The Arrangement Position display shows its bars/beats/sixteenths in blue;
the documented two-bar example counts from −2.1.1 to 1.1.1, when recording
begins. **U:** buffered input during count-in, held notes crossing its end,
already-running transport and combining count-in with punch/pre-roll.

### REQ-RECORDING-COMPING-013 — recording metronome

**D12, R19 §19.4–19.4.1.** The enabled metronome starts with playback or a clip
launch; Preview Volume controls its level. Auto tick division follows the meter
denominator. A selected division that no longer fits a bar falls back to Auto,
then returns if a later meter permits it. With Enable Only While Recording and
the metronome enabled, it sounds during recording; enabled Punch-In postpones
that sound to the punch-in point. **U:** tick sample waveform, phase and latency.

### REQ-RECORDING-COMPING-014 — Capture MIDI eligibility

**D12, R19 §19.10.** Capture MIDI retrieves recently played input from armed or
input-monitored MIDI tracks without prior Record. **U:** buffer capacity,
eviction, clear/reset triggers, no-input behavior, controllers, MPE expression
and the relationship of armed eligibility to suppressed Auto monitoring.

### REQ-RECORDING-COMPING-015 — Capture MIDI in an empty stopped Set

**D12, R19 §19.10.1.** In an empty stopped Set, Capture creates a phrase clip
on each monitored MIDI track, in the currently focused Session or Arrangement
view. It infers tempo within 80–160 BPM and loop boundaries, and starts loop
playback. Material preceding the chosen phrase remains before the start
marker. **U:** the detection algorithm, exact phrase, tempo or alignment for
arbitrary input; tempo-automated Sets use REQ-017's documented branch.

### REQ-RECORDING-COMPING-016 — single-note Capture MIDI

**D12, R19 §19.10.1 note.** With a single note in the first captured MIDI clip,
the documented loop bounds are that note's start/end and the inferred tempo
produces a one-, two-, four- or eight-bar loop. **U:** how the bar count is
chosen, zero-duration input, tempo at exact boundaries and held/incomplete notes.

### REQ-RECORDING-COMPING-017 — Capture MIDI in an established Set

**D12, R19 §19.10.2.** If transport runs, other clips exist, or tempo is
automated, Capture uses the existing tempo instead of changing it. It selects
a loop from the played phrase and retains preceding material. Playing over a
running clip on the same track and pressing Capture adds the material to that
clip. **U:** stopped/nonplaying occupied-slot placement, capture repeated
without new input and collisions with ordinary recording/overdub.

### REQ-RECORDING-COMPING-018 — recording takes

**D12, R21 §21.1, §21.3.** Arrangement recording creates take lanes and clips
on armed audio/MIDI tracks. Recording over existing clips adds a lane per pass,
including looping passes. Existing lanes are reused when no other clip exists
after the punch-in point. The latest recorded clip is copied to the main lane
and is available for playback. **U:** the reuse search order, first-pass
preexisting-main preservation and partial-pass clipping. The manual's reuse
condition does not establish a greedy lane-allocation algorithm.

### REQ-RECORDING-COMPING-019 — lane visibility

**D12, R21 §21.1–21.2.** Audio/MIDI Arrangement tracks have a main lane and
can have multiple take lanes. Show Take Lanes toggles their visibility; inserting
a lane unfolds them. Take lanes are hidden in Automation Mode; requesting
their display or insertion exits that mode. **U:** display persistence and
accessibility/focus transitions beyond these actions.

### REQ-RECORDING-COMPING-020 — lane management

**D12, R21 §21.2.** Selected tracks accept Insert Take Lane. Lanes can be
duplicated, deleted, reordered within their track, renamed and resized.
Delete All Take Lanes removes all lanes; Delete All Unused Take Lanes removes
lanes lacking recorded material used in the main comp. **U:** sample-file
deletion, undo/redo grouping, linked tracks and edge conditions in unused-lane
classification. Deleting a lane is not evidence of deleting its audio file.

### REQ-RECORDING-COMPING-021 — audition

**D12, R21 §21.1, §21.5.** The main lane is normally heard; take lanes are
heard through Audition. The speaker control or T auditions a take lane. Only
one lane per track may be auditioned; different tracks may audition together.
When a selection spans lanes/tracks, the last selected lane per track is used.
**U:** audition/record overlap, switch timing, gaps, teardown and suppression of
the main lane during every audition boundary.

### REQ-RECORDING-COMPING-022 — comp copies and source independence

**D12, R21 §21.6.** Enter or Copy Selection to Main Lane copies selected take
material to the main lane. Main/take clips are independent copies: editing one
does not edit the other. This describes clip content independence, not a second
physical audio file. Take clips allow ordinary Arrangement edits and can be
copied/dragged to Session slots. **U:** cross-type paste refusal and exact
non-grid boundary handling.

### REQ-RECORDING-COMPING-023 — choosing alternate comp material

**D12, R21 §21.6.** Ctrl on Windows/Cmd on macOS with Up/Down replaces selected
main material with previous/next take clips, skipping empty lanes. A take-lane
time selection also moves to the chosen take. Draw Mode copies a dragged take
selection to main on release; clicking a take with a main time selection
replaces the corresponding interval. **U:** dragging cancellation, endpoint
ties, cross-track selections and the no-alternative boundary.

### REQ-RECORDING-COMPING-024 — source highlights

**D12, R21 §21.7.** Used take material is highlighted with the track color;
unused material is desaturated. Highlights require matching clip positions and
properties. Dragging the highlight edge adjusts the split between adjacent
comp pieces. **U:** the complete property equivalence predicate, floating-point
tolerances and effects of unmatched edits. A shared TakeId alone does not prove
that two clips match.

### REQ-RECORDING-COMPING-025 — comp crossfades

**D12, R21 §21.6.** With Create Fades on Clip Edges enabled, adjacent comp clips
receive four-millisecond crossfades. The documented manual crossfade command
also applies to selected clips. **U:** curve law, overlap/minimum-length rules,
rounding at sample rates and numerical render output. Four milliseconds is a
documented duration, not a measured waveform tolerance.

### REQ-RECORDING-COMPING-026 — recorded audio files

**D12, R19 §19.7–19.8; R17 §17.2.1.** Recording File Type and Bit Depth settings
choose the recorded sample format. Mono input records mono; other selected
audio input records stereo. Recorded media belongs under the Set project's
`Samples/Recorded`; before saving, its location follows Temporary Folder.
**U:** naming/collision policy, precise first-save move/copy transaction,
encoding details, disk-full/write failure, unsaved close and unused-file cleanup.
Sample-reference structure remains SPEC-LIVE-SET-STRUCTURE's contract.

### REQ-RECORDING-COMPING-027 — stored lane inventory

**D12403, E-SCHEMA; E-DOCS.** Both AudioTrack and MidiTrack declare TakeLanes.
Its nested TakeLanes list holds TakeLane entries and a folded-state field.
TakeLane declares name, annotation, height, selection, clip automation and
Audition fields, with `ClipAutomation/Events` holding saved clips. AudioClip and
MidiClip declare TakeId. Shipped documents corroborate concrete lane entries
and MIDI clips. This requirement inventories stored state; it does not assert
allocation, source matching, numeric range, save/restore behavior or how TakeId
is generated. Existing document specs govern common field parsing.

### REQ-RECORDING-COMPING-028 — save, undo, redo and deletion lifecycle

**U.** Other than the documented Undo clauses in REQ-006, 009 and 011, no
recording/comp transaction boundary or redo result is established. Persistence
of an in-progress record, captured history, audition state, lane fold/selection,
comp linkage, unsaved recordings and physical sample ownership remains open.
Schema declarations cannot settle these behaviors. No recovery guarantee follows
from the presence of a saved clip.

### REQ-RECORDING-COMPING-029 — cancellation, failure and teardown

**U.** Stop is a documented recording/clip control (REQ-007, 031), but cancel
before start, stop during count-in, disconnecting an input, disk full, permission
failure, sample-write failure, device/track deletion, closing the Set while
recording and process failure have no established transition or error wording.
Retained media, final note-offs, retry and rollback results must remain ungraded.

### REQ-RECORDING-COMPING-030 — recording timing

**U.** No bound is established for input-to-note/sample timestamp, monitor or
record latency compensation, buffer scheduling, punch inclusivity, click-free
switching, jitter or real-time capacity. The monitoring-latency preference
documented by R17 §17.1 has no numeric transfer rule here. Clip-launch and
playback-core timing results cannot be substituted for the recording path.

### REQ-RECORDING-COMPING-031 — Session performance into Arrangement

**D12, R7 §7.5.** Arrangement Record captures Session clip launches and their
property changes into Arrangement on the appropriate tracks/song positions;
it also records eligible mixer/device automation and tempo/meter changes
included in the names of launched scenes.
Press Record again or stop playback to finish. This produces Arrangement clips
without new audio data. Session/Arrangement clips are independent. Playback
ownership and return controls belong to
[REQ-ARRANGEMENT-020](arrangement-editing.md#req-arrangement-020--session-overrides-arrangement-per-track)
and [REQ-ARRANGEMENT-021](arrangement-editing.md#req-arrangement-021--return-one-or-all-tracks-to-arrangement).
**U:** recording tempo/meter changes from scene fields without the documented
scene-name condition, precise clip segment boundaries, automation arming
dependencies and quantized transition latency. Automation write detail belongs
to the automation contract.

### REQ-RECORDING-COMPING-032 — remote recording actions

**D12, R19 §19.9.** Arrangement Record, transport, track Arm, Session Record,
New, individual slots and relative Session navigation can be assigned through
key/MIDI mapping. Step recording navigators can also be mapped. These are
alternate triggers for this draft's actions. **U:** simultaneous mappings,
conflicts, press/release edges and remote action timing; controller protocol
details belong to their respective feature families.

## Timing and state

The observable states used here are prepared/armed, waiting for playback,
counting in, recording, looping playback, MIDI overdubbing, stopped and
take audition. They are descriptive; the draft does not impose one hidden
state machine or require mutual exclusion across independent tracks/views.
Preconditions in each clause matter: ordinary recording, looping MIDI overdub
and Capture have different quantization/tempo rules.

Musical positions use bars/beats/sixteenths where the manual does; the tempo
range in REQ-015 and duration in REQ-025 are documentary values. No exact input
beat/sample conversion, event ordering, Capture heuristic or latency tolerance
is supplied. Persistence and undo have only the finite clauses above.

## Acceptance cases

Case kind: P positive; N negative; B boundary; C cancellation; T teardown;
M malformed/error; F static file audit. The evidence column is an exact source
section locator using the appendix keys. Each D12 row is **ungraded against
12.4.3**, with the following result as its documentary comparator. U rows have
no asserted result. No generated fixture or captured execution is claimed.

| Case | Req suffix | Kind | Setup/action | Documented result or unresolved comparator | Evidence |
| --- | --- | --- | --- | --- | --- |
| RC-001 | 001 | P | Select a mono external audio input; arm; record | Selected input is the recording source | D12 R19 §19.1 |
| RC-002 | 001 | P | Select MIDI device/channel; record matching input | Record uses the chosen source | D12 R19 §19.1 |
| RC-003 | 001 | P | Arm in Session, inspect Arrangement Arm | Same track state | D12 R19 §19.2 |
| RC-004 | 001 | P | Arm A then B; repeat with platform modifier | Ordinary click disarms A; modified click permits A+B | D12 R19 §19.2 |
| RC-005 | 001 | P | Select A+B; click one Arm | Both armed; armed track selected | D12 R19 §19.2 |
| RC-006 | 002 | P | Armed Auto track, no clip playing; then play a clip | Monitor input initially; inhibit monitoring while clip plays | D12 R17 §17.1 |
| RC-007 | 002 | P | Select In; disarm; play a clip | Input remains monitored; clip output suppressed | D12 R17 §17.1 |
| RC-008 | 002 | P | Arm with Off; record input using external monitoring | Recording possible without input monitoring in Live | D12 R17 §17.1 |
| RC-009 | 003 | P | Stopped; Start Playback with Record on; Record | Recording starts | D12 R19 §19.3.1 |
| RC-010 | 003 | P | Same preference off; Record then Play | Wait, then record | D12 R19 §19.3.1 |
| RC-011 | 003 | P | Repeat both settings with Shift+Record | Opposite start behavior | D12 R19 §19.3.1 |
| RC-012 | 004 | P | Record new MIDI over existing MIDI, Overdub on | New clip contains existing and input MIDI | D12 R19 §19.3.1 |
| RC-013 | 005 | N | Punch-In on; input strictly before loop start | Protected interval not recorded | D12 R19 §19.3.1 |
| RC-014 | 005 | N | Punch-Out on; input strictly after loop end | Protected interval not recorded | D12 R19 §19.3.1 |
| RC-015 | 006 | P | Record several complete audio loop passes; inspect sample | Earlier passes retained; markers permit audition | D12 R19 §19.3.1 |
| RC-016 | 007 | P | Arm A+B with empty selected-scene slots; Session Record | Both slots record; recording launch indicators red | D12 R19 §19.3.2 |
| RC-017 | 007 | P | Press Session Record again during recording | Clips enter loop playback | D12 R19 §19.3.2 |
| RC-018 | 007 | P | Use individual empty-slot Record, then clip Launch | That slot records then loops | D12 R19 §19.3.2 |
| RC-019 | 007 | P | Stop a recording/playing Session clip by Clip Stop | Clip stops | D12 R19 §19.3.2 |
| RC-020 | 008 | N | Default scene-record preference; launch scene with empty armed slots | Scene launch alone does not record empty slots | D12 R19 §19.3.2 |
| RC-021 | 008 | P | Enable Start Recording on Scene Launch; repeat | Empty armed slots record | D12 R19 §19.3.2 |
| RC-022 | 008 | P | Invoke mapped New while armed clips play | Armed clips stop; a scene for recording is selected/created | D12 R19 §19.3.2 |
| RC-023 | 009 | P | Loop an armed MIDI clip; Session Record; add two passes | Successive input is added | D12 R19 §19.3.3 |
| RC-024 | 009 | N | Toggle Session Record off; play rehearsal notes | Clip keeps playing; rehearsal not added | D12 R19 §19.3.3 |
| RC-025 | 009 | P | Undo last take during looping overdub | Last take removable; exact grouping ungraded | D12 R19 §19.3.3 |
| RC-026 | 010 | P | Stopped, armed, Preview on; hold notes and press Right twice | Grid step entry then duration extension | D12 R19 §19.3.4 |
| RC-027 | 010 | P | Keep new notes held and press Left | Newly entered notes removed as documented | D12 R19 §19.3.4 |
| RC-028 | 011 | P | Arrangement record with quantization; Undo quantization | Recording retained without that quantization step | D12 R19 §19.5 |
| RC-029 | 011 | N | Try to change quantization during ordinary Session/Arrangement record | Change unavailable during the recording | D12 R19 §19.5 |
| RC-030 | 011 | P | Loop overdub; change quantization | New setting applies immediately; no separate quantization Undo | D12 R19 §19.5 |
| RC-031 | 012 | P | Stopped; two-bar count-in; start record | Blue count-in −2.1.1 to 1.1.1; recording waits for completion | D12 R19 §19.6 |
| RC-032 | 013 | P | Enabled metronome with Only While Recording and Punch-In | Metronome audible after punch-in during recording | D12 R19 §19.4.1 |
| RC-033 | 013 | P | Set a tick division, change meter so it no longer fits, restore meter | Auto fallback, then selected division restored | D12 R19 §19.4.1 |
| RC-034 | 014 | P | Play on armed/input-monitored MIDI track without Record; Capture | Recent played MIDI can be retrieved | D12 R19 §19.10 |
| RC-035 | 015 | P | Empty stopped Set, multiple monitored MIDI tracks; Capture in Session focus | Phrase clips in focused view; loop playback starts | D12 R19 §19.10.1 |
| RC-036 | 015 | P | Repeat with Arrangement focus | Capture places clips in Arrangement | D12 R19 §19.10.1 |
| RC-037 | 015 | B | Empty stopped Set; capture a played phrase | Inferred tempo in 80–160 BPM; exact value ungraded | D12 R19 §19.10.1 |
| RC-038 | 016 | B | First captured clip contains one completed note | Note start/end bound loop; one/two/four/eight bars, choice ungraded | D12 R19 §19.10.1 note |
| RC-039 | 017 | N | Existing clip, stopped; Capture new phrase | Song tempo unchanged | D12 R19 §19.10.2 |
| RC-040 | 017 | N | Running transport; Capture new phrase | Song tempo unchanged | D12 R19 §19.10.2 |
| RC-041 | 017 | N | Tempo automated; Capture new phrase | Capture does not adjust tempo | D12 R19 §19.10.2 |
| RC-042 | 017 | P | Play over a running clip on same track; Capture | New material added to existing clip | D12 R19 §19.10.2 |
| RC-043 | 018 | P | Record complete passes over existing audio/MIDI Arrangement clips | New take lane per pass; last clip copied to main | D12 R21 §21.3 |
| RC-044 | 018 | B | Existing lane has no clip after punch-in; record | Existing lane can be reused; selection ordering ungraded | D12 R21 §21.3 |
| RC-045 | 019 | P | In Automation Mode, request Show Take Lanes | Exit Automation Mode and show lanes | D12 R21 §21.1 |
| RC-046 | 019,020 | P | Select tracks; Insert Take Lane while folded | Insert lanes and unfold them | D12 R21 §21.2 |
| RC-047 | 020 | P | Duplicate, rename and reorder selected lane | Named operations available within track | D12 R21 §21.2 |
| RC-048 | 020 | P | Delete All Unused Take Lanes with unused/used lanes | Remove lanes without recorded material used in main comp | D12 R21 §21.2 |
| RC-049 | 021 | P | Audition lane A then lane B on same track | Only one take lane auditioned on track | D12 R21 §21.5 |
| RC-050 | 021 | P | Audition take lanes on two tracks | Both tracks may audition simultaneously | D12 R21 §21.5 |
| RC-051 | 022 | P | Select take interval; Enter | Copy that interval to main lane | D12 R21 §21.6 |
| RC-052 | 022 | N | Edit copied main clip; inspect original take; reverse direction | Corresponding source/copy unchanged by other clip's edit | D12 R21 §21.6 |
| RC-053 | 023 | P | Main selection; next/previous-take command with an empty lane between | Replacement from nonempty take; empty lane skipped | D12 R21 §21.6 |
| RC-054 | 023 | P | Draw a take selection and release; use main time selection and click take | Corresponding take interval copied to main | D12 R21 §21.6 |
| RC-055 | 024 | P | Main comp with matching take positions/properties | Used portions track-colored, unused desaturated | D12 R21 §21.7 |
| RC-056 | 024 | P | Drag highlight edge between adjacent comp pieces | Comp split point changes | D12 R21 §21.7 |
| RC-057 | 025 | P | Create adjacent comp clips with Create Fades on Clip Edges | Documented four-ms crossfades; waveform ungraded | D12 R21 §21.6 |
| RC-058 | 026 | P | Record mono input, repeat stereo input | Mono then stereo sample files | D12 R17 §17.2.1 |
| RC-059 | 026 | P | Record in saved project; inspect retained media location | Under project's Samples/Recorded | D12 R19 §19.8 |
| RC-060 | 026 | P | Record in unsaved Set with designated Temporary Folder | Recording location follows that preference | D12 R19 §19.8 |
| RC-061 | 027 | F | Inspect pinned schema TakeLane/TakeLanes | Declared field inventory matches REQ-027 | D12403 E-SCHEMA, class keys |
| RC-062 | 027 | F | Inspect pinned AudioTrack/MidiTrack and AudioClip/MidiClip schema classes | Track TakeLanes and clip TakeId declarations | D12403 E-SCHEMA, class keys |
| RC-063 | 027 | F | Inspect shipped Patience Suite Demo TakeLane records | Concrete lane entries and MIDI event clips retained | D12403 E-DOCS, source SHA 3f1c0f92…40952b, take_lanes paths |
| RC-064 | 027 | F | Inspect Vocal Recording template lane records | Five lane entries, including empty Events; no runtime claim | D12403 E-DOCS, source SHA d12d2102…b3c26e, take_lanes paths |
| RC-065 | 028 | P | Save/reopen comp with edited independent clips and lane metadata | Unknown preservation/identity/linkage result | U |
| RC-066 | 028 | P | Undo/redo comp replacement, lane deletion and capture | Unknown transaction grouping and media ownership | U |
| RC-067 | 029 | C | Stop/cancel count-in before recording begins | Unknown clip/media retention and input flush | U |
| RC-068 | 029 | T | Close Set, delete track or disconnect input during recording | Unknown stop/finalize/error/rollback result | U |
| RC-069 | 029 | M | Exhaust disk space or remove write permission during audio record | Unknown retained-media/error/retry result | U |
| RC-070 | 030 | B | Input exactly at punch, loop or count-in boundary; note held across boundary | Unknown inclusion/timestamp and note splitting | U |
| RC-071 | 014,017 | B | Repeated Capture with no new input; overflow capture history | Unknown deduplication/eviction/reset behavior | U |
| RC-072 | 024 | B | Change source clip property but retain TakeId/position | Complete highlight matching predicate unknown | U |
| RC-073 | 031 | P | Record Session launches into Arrangement; finish with Record/Stop | Arrangement clip copies; no new audio data | D12 R7 §7.5 |
| RC-074 | 031 | P | During recorded Session performance, exercise playback ownership/return | Use canonical Arrangement AR-044–046 and REQ-020/021 comparators; no separate recording law | D12 R7 §7.5; [Arrangement ownership](arrangement-editing.md#req-arrangement-020--session-overrides-arrangement-per-track) |
| RC-075 | 032 | P | Assign recording/slot/step actions using Key/MIDI mapping | Actions available through assigned controls | D12 R19 §19.9 |
| RC-076 | 029 | C | Start Draw comp gesture then cancel before mouse release | Unknown mutation/undo result | U |
| RC-077 | 029 | M | Malformed, duplicate or dangling lane/TakeId data on open | Recording-specific validation unknown; general loader rules separate | U |
| RC-078 | 025,030 | B | Crossfade at unusual sample rate or shorter-than-four-ms clips | Duration rounding, curve and overlap unknown | U |
| RC-079 | 031 | P | Arrangement Record on; launch a scene whose name supplies recognized 100-BPM and 3/4 values | Arrangement records those tempo/meter changes; parsing syntax and exact event timestamp ungraded | D12 R7 §7.5 |
| RC-080 | 026 | P | Choose one available File Type F and Bit Depth B; record one short audio clip | Created sample's format/depth match F/B; available-option enumeration and encoding details ungraded | D12 R19 §19.7 |
| RC-081 | 031 | B | Launch scene with tempo/meter fields set but no values in its name during Arrangement Record | Broader field-based recording result unknown | U |

Counts: **32 requirements; 81 cases: 65 D12 documentary comparators, four
D12403 artifact audits and 12 U cases.** All 77 application-behavior cases are
ungraded for 12.4.3; the four artifact audits are not application tests. No S or
X recording expectation is asserted. Negative, boundary, cancellation,
teardown and malformed cases are explicit. Audio-DSP fixture generation is
omitted because no original recording/crossfade output has been established.

## Open questions

The canonical [research gaps](../research/recording-comping.md#open-evidence-gaps)
R-G01–R-G09 delimit missing exact-build behavior, timing, Capture heuristics,
take allocation/matching, Undo, persistence, failures, preferences and
crossfades. They must be reconciled through reviewed evidence before a release
can claim those clauses. Documentary choices do not close these gaps.

## Analyst evidence appendix

Analysis only; do not copy original-derived identifiers or restricted source
links into a handoff. The [research page](../research/recording-comping.md) owns
findings and source limitations. The [packet](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/README.md)
owns hashes, raw captures and reproduction details.

| Key | Exact retained evidence and locator | Authority/limit |
| --- | --- | --- |
| R19 | [Recording New Clips capture](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-recording-new-clips-2026-10-19.html): §19.1 `choosing-an-input`; §19.2 `arming-record-enabling-tracks`; §19.3.1 `recording-into-the-arrangement`; §19.3.2 `recording-into-session-slots`; §19.3.3 `overdub-recording-midi-patterns`; §19.3.4 `midi-step-recording`; §19.4.1 `metronome-settings`; §19.5 `recording-quantized-midi-notes`; §19.6 `recording-with-count-in`; §19.7 `setting-up-file-types`; §19.8 `where-are-the-recorded-samples`; §19.9 `using-remote-control-for-recording`; §19.10 `capturing-midi`; §19.10.1 `starting-a-new-live-set`; §19.10.2 `adding-material-to-an-existing-live-set` | D12; captured 2026-10-19, patch unstated |
| R21 | [Comping capture](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-comping-2026-10-19.html): §21.1 `take-lanes`; §21.2 `inserting-and-managing-take-lanes`; §21.3 `recording-takes`; §21.5 `auditioning-take-lanes`; §21.6 `creating-a-comp`; §21.7 `source-highlights` | D12; patch unstated; images not examined |
| R17 | [Routing capture](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-routing-and-i-o-2026-10-19.html): §17.1 `monitoring`; §17.2.1 `monostereo-conversions` | D12; monitoring/input channel boundary only |
| R7 | [Session capture](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-session-view-2026-10-19.html): §7.5 `recording-sessions-into-the-arrangement` | D12; automation dependencies not resolved |
| E-SCHEMA | [schema-fields.json](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/schema-fields.json), `classes[class=TakeLane|TakeLanes|AudioTrack|MidiTrack|AudioClip|MidiClip|Transport|Metronome|LiveSet]`; original `Schema/12.0_12402.txt`, SHA-256 b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299 | D12403; declarations, not runtime save/read guarantees |
| E-DOCS | [shipped-documents.json](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/shipped-documents.json), each exact `source`, `sha256` and `take_lanes[].path` | D12403 bundle contents; documents may originate in earlier authoring versions |
| E-NATIVE | [native-string-excerpts.json](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/native-string-excerpts.json), exact source line/hash/address for CaptureMidi, CountInDurationInBars, TakeLane, Audition, PunchIn/PunchOut | S-inventory only; no behavioral acceptance comparator |

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-19 | First analyst draft: recording, Capture MIDI, comping, retained manual/schema/document evidence, 32 requirements and 78 unexecuted cases with distinct documentary/file/U provenance |
| 1 (unreleased review corrections) | 2026-10-19 | Narrow REQ-031 to launched-scene names; broader scene-field branch U; single-owner links to Arrangement playback ownership; add RC-079–081 including recording format/depth. Now 81 cases: 65 D12, four artifact audits, 12 U |

No release. Draft alone is not an implementation contract.
