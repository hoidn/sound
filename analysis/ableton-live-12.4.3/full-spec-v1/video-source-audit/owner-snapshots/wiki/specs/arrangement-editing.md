---
id: SPEC-ARRANGEMENT-EDITING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Arrangement editing

## Scope and evidence boundary

Feature FEAT-ARRANGEMENT in the [feature map](feature-map.md). User task: arrange
clips on a linear song timeline, edit selected material, manipulate song time,
navigate with locators, and return tracks from Session playback to Arrangement.
This is a bounded **proposed** contract, not a released implementation input.

**The behavioral source is the online Live 12 manual captured 2026-10-19. It
identifies major version 12, not build 12.4.3. Every manual-derived behavior below
is D for that captured documentation and U for exact 12.4.3 parity.** Installed
12.4.3 schema and shipped Set bytes corroborate representable objects; a retained
native command registry corroborates command names, not their runtime semantics.
No Live run, extracted execution of an edit command, or candidate test was made.
See the [research page](../research/arrangement-editing.md) and exact appendix.

| Label | Meaning in this draft |
| --- | --- |
| D-manual | Directly documented in the captured Live 12 manual; build parity unknown |
| D-package | Directly present in named shipped 12.4.3 package bytes; a shipped Set can have an older Creator |
| S | Static derivation from pinned native evidence; presence of a registry entry proves neither reachability nor edit behavior |
| X | Extracted execution of original functions; **none in this packet** |
| U | Unknown; no expected result and no pass/fail grading for the missing clause |

The short label D in the cases means D-manual unless stated D-package. D cases
are proposed documentation-conformance checks; none is a verified 12.4.3 result.
All cases are unexecuted, including D-package checks as application acceptance
cases. The source-inventory script is evidence tooling, not an application test.

Dependencies retain their canonical ownership: [transport state](transport-state.md)
for stored loop/tempo values, [playback core](playback-core.md) for scheduler and
playback arithmetic, [clip launch](clip-launch.md) for Session launch controls,
[MIDI notes](midi-note-storage.md) for note storage, [Warp](warp-markers.md) for
source-time mapping, [automation](automation-envelopes.md) for envelope values,
and [Set structure](live-set-structure.md) for the already specified reader
structure. That last draft explicitly excludes Arrangement clips; this draft
adds observations of their placement without claiming its reader rules extend
without qualification.

Excluded from the bounded contract: take-lane creation and comping semantics,
recording capture, groove changes, audio-to-MIDI conversion, MIDI note editing,
freeze/bounce, import/export rendering, device processing, and pixel-identical
layout. Linked-track propagation into recording and take lanes is recorded as a
boundary in REQ-030, not a specification of those subsystems.

## Requirements

Positions below are musical timeline positions. Examples use quarter-note beats
from song start with 4/4 meter; [a,b] describes visible clip extent, without
asserting ownership of a note/event exactly on b. Command names are normative
inputs; macOS shortcuts named below are equivalent inputs only where documented.
Every requirement's evidence key resolves in the appendix.

### REQ-ARRANGEMENT-001 — Select clips, time, and insertion position

D-manual (A6.9): clicking a clip selects it. Clicking empty Arrangement background
places an insert marker. Dragging through time selects a timespan, including
within an unfolded clip's waveform or MIDI display. Shift-click extends an
existing selection within or across tracks; Shift plus arrows extends or
shortens it. Arrow keys move the insert marker in time or between tracks. On
macOS, Option plus left/right moves it to locators or selected-track clip edges.
Selection anchoring, ties and collapsed-track hit regions beyond this prose are U.

### REQ-ARRANGEMENT-002 — Scope ordinary selection commands

D-manual (A6.9, A6.11): Cut, Copy, Paste and Duplicate operate on the selected
material; their ordinary forms do not insert/delete song time across all tracks.
This does not specify what occupies an already occupied destination. Ordinary
Duplicate destination, overwrite/splitting rules, clipboard track mapping, and
copy identity semantics are U (REQ-033).

### REQ-ARRANGEMENT-003 — Move and resize clips

D-manual (A6.7): dragging a clip's bar moves it to a new song position or track;
dragging its left/right edge changes its length. Dragging the waveform or MIDI
content selects time rather than moving the bar. Cross-type destinations are
limited by REQ-004. Minimum size, extension beyond source boundaries, destructive
overlap handling, and motion before song start are U.

### REQ-ARRANGEMENT-004 — Clip type and track compatibility

D-manual (C3.8): audio clips belong on audio tracks and MIDI clips on MIDI tracks;
an audio clip cannot be added to a MIDI track or the reverse. The feedback,
conversion alternatives, and state of an invalid drop are U; this requirement
only rules out successful insertion as the incompatible clip type.

### REQ-ARRANGEMENT-005 — Slip content inside fixed clip edges

D-manual (A6.7): Shift-Option dragging a warped audio clip's waveform or a MIDI
clip's content slides its contents while keeping its visible clip boundaries.
Adding Cmd bypasses grid snapping for this gesture. Unwarped audio behavior,
loop-wrap arithmetic, source-edge clamps and note-boundary behavior are U.

### REQ-ARRANGEMENT-006 — Editing grid and object snapping

D-manual (A6.7, A6.10): clip edits snap to the editing grid and to relevant clip
edges, locators and meter changes. The grid supports adaptive and fixed modes,
narrow/wide steps, triplets and on/off. Cmd-1 doubles line density; Cmd-2 halves
it; Cmd-3 toggles triplets; Cmd-4 toggles snapping; Cmd-5 toggles fixed/adaptive.
Cmd temporarily bypasses an enabled grid, and temporarily enables a disabled
grid during an action. Snap priority, attraction distance, rounding ties,
adaptive zoom thresholds and grid extrema are U; no nearest-grid formula is
asserted.

### REQ-ARRANGEMENT-007 — Selection activation and reversal

D-manual (A6.9): 0 deactivates selected material, including a range spanning
multiple clips. With a track header selected, 0 deactivates the track. Reverse
Clip(s), also R, reverses an audio time selection across clips. A selection
containing MIDI clips cannot be reversed. Exact reverse render samples, file
creation, partial-clip splitting and reactivation toggle semantics are U.

### REQ-ARRANGEMENT-008 — Split at a point or around selected time

D-manual (A6.12): Split, also Cmd-E, divides a clip at an insertion point inside
its waveform/MIDI display. Splitting a nonempty interior time selection isolates
that portion as its own clip, with independent editable edges. The new parts can
be moved and edited independently. Source references, event ownership at the
split, note retriggering, generated fades, and a split at an existing edge are U.

### REQ-ARRANGEMENT-009 — Consolidate adjacent material per track

D-manual (A6.13): Consolidate, also Cmd-J, combines selected adjacent clip material
into one new clip on each selected track; selection may span multiple tracks.
The result can be moved and edited as a clip. Inclusion of empty gaps, mixed
clip-type selections, single-clip behavior, output metadata and note-merging
rules are U.

### REQ-ARRANGEMENT-010 — Audio consolidation signal and destination

D-manual (A6.13): audio consolidation creates a new sample per selected audio
track from the signal before that track's effects and mixer, incorporating clip
attenuation, Warp, pitch and applicable clip envelopes. Saved Sets place results
under Project `Samples/Processed/Consolidate`; unsaved Sets use the configured
Temporary Folder. Exact output rate, sample format, naming, sample values,
normalization, disk-failure handling and transaction cleanup are U. This is a
signal-placement contract, not a calibrated waveform comparator.

### REQ-ARRANGEMENT-011 — Cut and Delete Time

D-manual (A6.11): Cut Time and Delete Time remove the selected duration across
all Arrangement tracks, bringing later material earlier and reducing the
Arrangement duration by the removed duration. Cut Time also cuts the selected
time for later Paste Time. Time-signature markers in the selected region are
affected. Exact automation, locator, loop-brace, hidden-lane and selection
transformations are U; this draft does not equate “all tracks” with a proven
rule for every kind of object.

### REQ-ARRANGEMENT-012 — Paste and Duplicate Time

D-manual (A6.11): Paste Time inserts copied time and lengthens the Arrangement by
that duration. Duplicate Time inserts a copy of the selected timespan and
lengthens it by the selected duration. Their time insertion acts across tracks.
The exact duplicate insertion location, clipboard compatibility across Sets,
and transformations of non-clip objects are U.

### REQ-ARRANGEMENT-013 — Insert Silence

D-manual (A6.11): Insert Silence adds the chosen duration of empty time starting
at the insert marker, across Arrangement tracks. The exact choice dialog,
zero/negative input behavior, later locator/automation/loop changes and limits
are U. No audible silence guarantee is made for instruments or effects with
existing tails.

### REQ-ARRANGEMENT-014 — Locator creation

D-manual (A6.4): Set Locator adds a locator during playback/recording according
to global launch quantization. While stopped it adds one at the insert marker
or start of the time selection. Add Locator in Create/scrub-area context menus
also adds locators. A selected locator changes Set Locator to Delete Locator.
The scheduling boundary, duplicate-position policy and ordering of concurrent
locator/transport actions are U.

### REQ-ARRANGEMENT-015 — Locator navigation and song-start override

D-manual (A6.4): clicking a locator or Previous/Next Locator triggers a jump;
jumps follow global launch quantization (A6.1). Beyond the first/last locator,
Previous/Next reaches Arrangement start/end. Double-clicking a locator while
stopped selects it and starts playback there. Set Song Start Time Here on a
locator overrides the normal selection-based playback start. Locator mapping is
available, but mapping arithmetic stays in its own spec. Exact sample of the
jump and precedence between competing song-start overrides are U.

### REQ-ARRANGEMENT-016 — Locator editing and loop to next

D-manual (A6.4): selected locators can be dragged or moved with arrows, renamed
with Rename/Cmd-R, annotated using Edit Info Text, and deleted via Delete or
Delete Locator. Loop to Next Locator sets up playback looping between that
locator and the next. The last-locator case, equal-position locators, maximum
text length and locator-crossing reorder behavior are U.

### REQ-ARRANGEMENT-017 — Arrangement loop selection and brace editing

D-manual (A6.6): Loop Selection sets the brace to the time selection and enables
the Arrangement loop. The loop start and length can be edited numerically.
Dragging brace edges changes its start/end; dragging the bar translates it
without changing length. Left/right arrows nudge by the grid; up/down shifts by
its length. Cmd-left/right changes length by the grid; Cmd-up/down doubles/halves
length. Set Song Start Time Here on the brace makes playback start there instead
of the insert marker/selection. Clamp and rounding behavior is U. Stored fields
and scheduler behavior remain owned by the transport/playback specs.

### REQ-ARRANGEMENT-018 — Add and edit meter markers

D-manual (A6.5): Insert Time Signature Change places a meter marker at the insert
marker. Markers can be moved, edited with Edit Time Signature/Cmd-R, or deleted.
The documented text grammar accepts a one- or two-digit numerator and a
denominator in {1,2,4,8,16}, separated by slash, comma, period or spaces. Updating
the Control Bar meter changes the meter at the current play location, stopped
or running. Invalid/zero values, exact text parsing and migration are U; this
does not replace the narrower stored-value grammar in SPEC-TRANSPORT-STATE.

### REQ-ARRANGEMENT-019 — Fragmentary bars

D-manual (A6.5): meter markers obey the editing grid rather than launch
quantization and may divide an existing bar. A fragmentary bar is indicated in
the scrub area. Delete Fragmentary Bar Time removes that duration across all
tracks so the next meter change reaches a barline. Complete Fragmentary Bar
inserts time at the beginning of the fragment to complete it. Exact duration
calculation with adjacent irregular meters and non-clip state transformations
are U.

### REQ-ARRANGEMENT-020 — Session overrides Arrangement per track

D-manual (C3.6–3.7): changing between Session and Arrangement views changes the
view without changing playing clips. A track plays at most one clip, from
Session or Arrangement. Launching a Session clip takes that track over from
Arrangement while other tracks can keep playing Arrangement. Arrangement does
not automatically resume on that track; Back to Arrangement is the documented
return action. Stop-slot and stop-all interactions are U here.

### REQ-ARRANGEMENT-021 — Return one or all tracks to Arrangement

D-manual (C3.7): the global Back to Arrangement control lights when one or more
tracks are playing Session instead of Arrangement; activating it returns all
tracks to Arrangement playback. A track's Back to Arrangement control restores
that track individually. Exact return sample, fade, pending launch cancellation,
behavior over an empty Arrangement region and stopped-transport behavior are U.

### REQ-ARRANGEMENT-022 — Access clip fade controls

D-manual (A6.8): audio clip beginnings and ends have editable fades; adjacent
clips on the same audio track can have a crossfade. Handles are accessible by
hovering with enough track height. In Automation Mode, holding F while hovering
an automation lane temporarily exposes fade controls. Fades belong to clips and
are independent of automation envelopes. This is not the automatic Session
launch fade already covered in SPEC-PLAYBACK-CORE.

### REQ-ARRANGEMENT-023 — Edit/create fades and crossfades

D-manual (A6.8): fade start/end handles change fade duration without moving fade
peaks; fade edges cannot pass those peaks. Curve handles shape the fade.
Selecting time including a clip beginning/end enables Create Fade In/Out
(Cmd-Option-F). A fade handle dragged across a neighboring clip edge creates a
crossfade; selecting time spanning their boundary enables Create Crossfade.
Curve coefficients, equal-power/linear laws, rendered gains and rounding are U.

### REQ-ARRANGEMENT-024 — Fade boundaries and defaults

D-manual (A6.8): fades cannot cross clip loop boundaries and a clip's start/end
fades cannot overlap. Selecting a handle displays its limiting boundary. Delete
on a fade handle removes the fade when Create Fades on Clip Edges is off; with
that preference on it resets to a documented default 4 ms. That preference also
creates 4 ms crossfades between adjacent audio clips. Limits on very short clips
and the exact audio realization of 4 ms are U, so no sample-count rounding is
specified.

### REQ-ARRANGEMENT-025 — Create and identify linked-track groups

D-manual (A6.14.1): Link Tracks links selected track headers or a Group Track's
tracks. A Set can contain multiple linked groups, but a track belongs to at most
one. Members show a link indicator; hovering highlights the members, and clicking
the indicator selects them. Group-track recursion and empty groups are U.

### REQ-ARRANGEMENT-026 — Change and remove linked membership

D-manual (A6.14.1): Cmd with Link Tracks on an existing member adds selected tracks
to that group. Linking a selected subset or mixture of linked/unlinked tracks
forms a linked group for that selection. Unlink Track(s) removes selected
members. Exact membership/order left in prior groups, and singleton dissolution
are U; this draft asserts no hidden union algorithm.

### REQ-ARRANGEMENT-027 — Edit linked clips and selections together

D-manual (A6.14.2): linked tracks support simultaneous clip move/resize,
clip/time selection, time commands, Split and Consolidate. Concrete matching
clip fixtures are graded here; applying operations when linked clips have
different lengths, gaps, Warp settings or locked states is U. All-track time
commands retain REQ-011–013's all-track scope, even for unlinked tracks.

### REQ-ARRANGEMENT-028 — Linked fade synchronization boundary

D-manual (A6.14.2): creating/editing fades can affect linked tracks together,
but only fades starting at the same timeline position can be adjusted together.
No automatic alignment of differing fade starts is promised. Curve propagation
when the two clips impose different limits is U.

### REQ-ARRANGEMENT-029 — Navigation, zoom and follow state

D-manual (A6.1–6.2): the Overview and rulers allow timeline pan/zoom. Z zooms to
the selected time; X returns through previous Z zoom states. Follow scrolls with
song position, pauses on editing/horizontal scrolling or a beat-ruler click,
and resumes on stop/restart or clicking an Arrangement/clip scrub area. Exact
viewport dimensions, animation timing and scroll thresholds are U.

### REQ-ARRANGEMENT-030 — Linked recording/take-lane interaction boundary

D-manual (A6.14.2): linked editing also covers arm/disarm, take-lane insertion,
renaming/deletion and Audition Mode, even with hidden take lanes. The list is a
documented propagation boundary. Input capture, lane correspondence, comping
choice, phase accuracy and monitoring behavior require their own contract and
are U here; no acceptance case grades recorded audio.

### REQ-ARRANGEMENT-031 — Observable Set representation

D-package (P): the shipped 12.4d1-created demo has Arrangement `MidiClip` events
under each MIDI track's `DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events`
and `AudioClip` events under the audio track's analogous `Sample/ArrangerAutomation/Events`.
Clips carry `CurrentStart`/`CurrentEnd`. The shipped schema declares clip fade
fields, locator time/name/annotation/song-start state and linked-track membership.
This requirement records supported document representation, without inferring
defaults, legal numeric domains, how edits rewrite these values, persistence of
UI state or every malformed-document outcome. Those transitions are U.

### REQ-ARRANGEMENT-032 — Envelope lock interaction

D-manual (A6.1): Lock Envelopes anchors Arrangement envelopes to song position so
moving a clip does not move those envelopes. Exact transformations with lock
off, partial selections, time commands, clip envelopes, linked tracks and crossed
breakpoints are U; envelope evaluation remains in SPEC-AUTOMATION-ENVELOPES.

### REQ-ARRANGEMENT-033 — Duplicate, overlap and invalid edit outcomes

U: ordinary duplicate placement and source/clip identity; same-track overlap
replacement; paste over occupied regions; dragging before song start; zero-length
selections and minimum clip length; resizing unwarped audio to/beyond sample
bounds; Split at edges; and command availability with no compatible selection.
The manual describes the usable actions but does not establish these outcomes.
The native registry is S evidence of command names only (N), not a remedy.

### REQ-ARRANGEMENT-034 — Undo, cancellation and transactional failure

U: undo/redo grouping for drag/split/time/consolidate/link operations, Esc during
gestures, cancellation of consolidation, atomicity after storage failure,
clipboard lifetime, orphan media after undo, and interaction with active audio
playback. No successful rollback, unchanged-state guarantee or cancellation
shortcut is invented. The retained native registry names Undo/Redo (N), which
cannot establish any of those semantics.

### REQ-ARRANGEMENT-035 — Persistence and teardown

U: save/reopen after edits must eventually have an explicit contract, including
locators, linked groups, clip positions, fades, references to consolidated media,
and loop/song-start state. The observed representation (REQ-031) supplies inputs
but not a proven save/reopen result. Closing/replacing a Set during a gesture,
consolidation or pending locator jump; unsaved-change handling; and temporary
media cleanup are also unknown. Existing persistence releases do not close these
Arrangement exclusions.

## Timing, state and comparators

D-manual case grading compares named UI states, clip extents, material identities,
track membership and project path class. Every case below states its asserted
subset. A partly unspecified action is not upgraded by a neighboring D case.
Neither response-time limits nor an audio tolerance are established. Meter/grid
positions chosen by a fixture are exact musical positions, but the pixel-to-time
mapping and boundary rounding of a pointer gesture are U: an eventual fixture
must invoke a named numeric position or record its effective snapped position.

Do not apply the Trigger Session launch arithmetic of SPEC-PLAYBACK-CORE to
locator jumps, Arrangement override returns or edits without an explicit trace.
Loop scheduling, clip-note ownership, effects tails and sample gain remain owned
by their named specs and gaps. Schema fields are not undo, save or playback proof.

## Acceptance cases

Fixtures below are reproducible **scenario definitions**, not retained generated
Sets or original runs. Use two audio tracks A/B with distinguishable source
material, a MIDI track M, and matching compatible clips where stated. Default
transport is stopped, Automation Mode off and grid fixed at one beat; preference
and linked membership are stated per case. Physical file/audio assertions require
a future retained fixture and comparator before any execution can count as pass.

| Case | Requirement suffix | Kind | Setup and action | Proposed expectation and evidence |
| --- | --- | --- | --- | --- |
| AR-001 | 001 | positive | Click clip A, then click empty time 12 | Clip selected first, then insert marker at effective click position (D A6.9) |
| AR-002 | 001 | boundary | Drag time 4–8 on A; Shift-extend to B | Time selection extends across those tracks; exact anchor rule ungraded (D A6.9) |
| AR-003 | 002 | negative | Select A only; ordinary Copy | Copy is scoped to A's selection, not all-track time insertion (D A6.9/11); clipboard bytes U |
| AR-004 | 003 | positive | Drag A's clip bar from 0 to a clear grid point 8 | Clip changes position to the effective snapped point (D A6.7) |
| AR-005 | 003 | positive | Drag left/right edge of a compatible interior clip | Corresponding edge changes clip extent (D A6.7); source-edge bounds U |
| AR-006 | 003 | negative | Drag inside unfolded waveform without slip modifiers | Time selection changes instead of moving the bar (D A6.7/9) |
| AR-007 | 004 | negative | Try placing audio clip on M; repeat MIDI on A | Neither successfully inserts the incompatible clip type (D C3.8); feedback U |
| AR-008 | 005 | positive | Shift-Option drag M content; repeat warped audio | Content shifts while clip boundaries stay fixed (D A6.7); exact note mapping U |
| AR-009 | 005 | boundary | Slip an unwarped audio clip | Ungraded U: unsupported extension of documented gesture |
| AR-010 | 006 | positive | Cmd-1 from eighth-note grid, then Cmd-2 | Sixteenth-note then eighth-note grid (D A6.10) |
| AR-011 | 006 | positive | Toggle triplets, fixed/adaptive and snapping via commands | Corresponding modes toggle; no adaptive threshold asserted (D A6.10) |
| AR-012 | 006 | boundary | Edit with Cmd held, grid initially on and then off | Meter-grid snapping bypassed when on, temporarily enabled when off (D A6.10); object-snap priority U |
| AR-013 | 007 | positive | Select audio across A/B and press 0 | Selected material deactivated (D A6.9); second-press law U |
| AR-014 | 007 | negative | Select M plus audio and invoke Reverse Clip(s) | Mixed selection cannot be reversed (D A6.9); partial rejection feedback U |
| AR-015 | 007 | positive | Select audio-only range and invoke Reverse Clip(s) | Audio selection reversed (D A6.9); exact file/waveform values U |
| AR-016 | 008 | positive | Clip at 0–16, insertion point 8; Split | Independently editable parts at 0–8 and 8–16 (D A6.12); note edge ownership U |
| AR-017 | 008 | positive | Clip at 0–16; select 4–12; Split | Selection becomes distinct clip with edges 4/12, outer material separate (D A6.12) |
| AR-018 | 008,033 | boundary | Split exactly at existing edge | Ungraded U: no-op, selection and undo effects not established |
| AR-019 | 009 | positive | Adjacent A clips at 0–4/4–8; select both; Consolidate | One editable A clip represents selected material (D A6.13); exact metadata U |
| AR-020 | 009 | positive | Repeat AR-019 simultaneously on A/B | One consolidated clip for each selected track (D A6.13) |
| AR-021 | 010 | positive | Save Set in Project; consolidate A/B | New samples placed under that Project's Samples/Processed/Consolidate (D A6.13); naming/format U |
| AR-022 | 010 | boundary | Unsaved Set, configured Temporary Folder; consolidate A | Generated sample uses Temporary Folder (D A6.13); relocation after save U |
| AR-023 | 010 | negative | Compare consolidation with track effect on/off and altered mixer; same clip processing | Consolidated source signal precedes effects/mixer and includes clip processing (D A6.13); no numerical render comparator established |
| AR-024 | 011 | positive | All tracks have later clips; select two-beat range on A; Delete Time | All-track two-beat removal; later material two beats earlier; duration shorter by two (D A6.11); boundary-crossing clips U |
| AR-025 | 011 | positive | Cut a two-beat range; later Paste Time in clear region | Cut reduces and paste adds that duration; cut material is available for paste (D A6.11); mapping details U |
| AR-026 | 012 | positive | Select two-beat timespan; Duplicate Time | Copy inserted, total duration increases two beats, all-track time insertion (D A6.11); insertion position U |
| AR-027 | 013 | positive | Marker at beat 8; Insert Silence of two beats | Empty interval inserted at 8, all tracks gain two beats of timeline space (D A6.11); effects-tail audio U |
| AR-028 | 014 | positive | Stopped, no range, marker at 12; Set Locator | Locator at 12 (D A6.4) |
| AR-029 | 014 | boundary | Stopped, selected time 8–12; Set Locator | Locator at selection start 8 (D A6.4) |
| AR-030 | 014 | timing | Running, nonzero global quantization; Set Locator between grid lines | Addition follows global quantization (D A6.4); precise boundary/sample ungraded U |
| AR-031 | 015 | positive | Stopped; double-click a locator at 16 | Locator selected, playback starts there (D A6.4); latency U |
| AR-032 | 015 | boundary | At first/last locator use Previous/Next | Navigation reaches Arrangement start/end respectively (D A6.4) |
| AR-033 | 015 | positive | Enable Set Song Start Time Here on locator; select elsewhere; Play | Playback starts at locator rather than time selection (D A6.4); competing brace override U |
| AR-034 | 016 | positive | Rename, annotate, move, then delete selected locator | Requested visible text/position edits and deletion apply (D A6.4); text limits U |
| AR-035 | 016 | positive | Locators at 8/16; Loop to Next Locator from 8 | Loop spans those locators (D A6.4); sample scheduling follows separate scope |
| AR-036 | 016 | boundary | Last locator; Loop to Next Locator | Ungraded U: no next-locator fallback established |
| AR-037 | 017 | positive | Select time 8–16; Loop Selection | Loop enabled with brace covering selection (D A6.6) |
| AR-038 | 017 | positive | Drag brace bar to another clear position | Start/end translate and length unchanged (D A6.6) |
| AR-039 | 017 | boundary | From four-beat length, Cmd-up then Cmd-down | Length doubles to eight then halves to four beats (D A6.6); lower limit U |
| AR-040 | 018 | positive | Insert meter at marker 8, enter 7/8; move/edit/delete | Requested marker operations apply for documented meter text (D A6.5) |
| AR-041 | 018 | malformed | Enter 7/3, zero numerator, or nonnumeric meter text | Ungraded U: refusal/coercion and prior-state preservation unknown |
| AR-042 | 019 | boundary | Meter change inside an existing bar on editing grid | Fragmentary bar is permitted and indicated (D A6.5) |
| AR-043 | 019 | positive | From known fragment, Delete Fragmentary Bar Time; separately Complete Fragmentary Bar | First removes fragment time; second inserts missing time across tracks; next change lands on barline (D A6.5); exact duration calculation U |
| AR-044 | 020 | positive | A/B Arrangement playing; launch Session clip on A | A plays Session, B keeps Arrangement; view switches leave clip choice unchanged (D C3.6–7) |
| AR-045 | 021 | positive | A/B overridden by Session; use A's Back to Arrangement | A resumes Arrangement; B remains overridden (D C3.7); transition sample U |
| AR-046 | 021 | positive | A/B overridden; activate global Back to Arrangement | Both return to Arrangement; button indicates override while Session tracks active (D C3.7); transition/empty-region rules U |
| AR-047 | 022 | positive | Expanded audio track; enable Automation Mode, hover lane while holding F | Fade controls temporarily accessible; clip fades remain distinct from envelopes (D A6.8) |
| AR-048 | 023 | positive | Select time at beginning/end; Create Fade In/Out; adjust curve | Fade created on relevant clip edge and curve editable (D A6.8); numerical curve U |
| AR-049 | 023 | positive | Adjacent A clips; select time over boundary; Create Crossfade | Crossfade created between adjacent clips (D A6.8); gain law U |
| AR-050 | 024 | boundary | Try extending fade through loop edge, across opposite fade, or edge past peak | Stated fade limits hold (D A6.8); exact limiting value on very short clips U |
| AR-051 | 024 | positive | Preference off; select fade handle; Delete | Fade removed (D A6.8) |
| AR-052 | 024 | boundary | Preference on; delete fade handle; create adjacent audio clips | Deleted fade resets to nominal 4 ms; adjacent clips get nominal 4 ms crossfade (D A6.8); sample rounding/short-clip limit U |
| AR-053 | 025,026 | positive | Link A/B; inspect indicator; add M with Cmd-Link Tracks; unlink M | Membership indicators/select behavior and requested add/remove operations work; each track in at most one linked instance (D A6.14.1); residual singleton policy U |
| AR-054 | 027 | positive | A/B linked, matching clips 0–16; select 4–12 and Split | Both linked tracks isolate matching selected portions (D A6.14.2); mismatched-content rules U |
| AR-055 | 028 | negative | Linked A/B fades start at different times; adjust A | Simultaneous adjustment does not cover mismatched-start fades (D A6.14.2); any other selection changes U |
| AR-056 | 029 | positive | Z-zoom twice; X twice; separately edit during Follow | Previous Z zoom states restored; edit pauses Follow; restart resumes it (D A6.2); pixels/timing U |
| AR-057 | 030 | boundary | Linked A/B; B take lanes hidden; rename corresponding lane | Documented linked rename includes hidden lane (D A6.14.2); recorded/comped material behavior U |
| AR-058 | 031 | persistence input | Inspect pinned demo through an independent document reader | 64 main-lane clips: 9 AudioClip under Sample, 55 MidiClip under ClipTimeable; 9 named locators (D-package P); not a save/reopen pass |
| AR-059 | 032 | negative | Lock Envelopes on; move a clip with Arrangement envelope underneath | Envelope remains at song position (D A6.1); lock-off/breakpoint laws U |
| AR-060 | 033 | boundary | Ordinary Duplicate into occupied timeline, overlap-drop, resize to zero, or no-selection Split | Ungraded U: destination, replacement, limits and command availability unknown |
| AR-061 | 034 | undo/redo | Split/drag/time insertion/consolidate/link, then Undo and Redo | Ungraded U: grouping, restored state and media side effects unknown |
| AR-062 | 034 | cancellation | Begin clip/fade/locator drag; press Esc; separately cancel consolidation | Ungraded U: accepted cancel input, rollback and temporary media unknown |
| AR-063 | 034 | error | Consolidation destination unwritable or full | Ungraded U: diagnostics, partial files and original material state unknown |
| AR-064 | 035 | persistence | Save/reopen after clip, fade, locator, link and song-start edits | Ungraded U: exact reopened fields/identity/playback and source paths unknown |
| AR-065 | 035 | teardown | Close/replace Set during drag, consolidation or pending locator jump | Ungraded U: prompts, cleanup, pending operation cancellation and retained state unknown |

All applicable categories have cases. Malformed input is confined to actual text
input/storage boundaries; a mouse gesture itself has no file grammar. Disk errors,
undo, cancellation and teardown are deliberately ungraded. Crash recovery,
recording and rendering remain excluded subsystems, not passing omissions.

## Open questions

These local IDs identify concrete contract gaps; a project-wide register may
route here without duplicating the claims.

| Question | Missing evidence and effect | Narrow next evidence task |
| --- | --- | --- |
| Q-ARR-001 | Captured manual may describe a later Live 12 revision; every D-manual clause has 12.4.3 parity U | Trace selected command dispatch and transforms in pinned native corpus, then release only matched clauses |
| Q-ARR-002 | Duplicate/overlap/minimum-size rules U, REQ-033 | Trace ordinary Duplicate, drag placement, Split and resize boundary paths with finite candidate coordinates |
| Q-ARR-003 | Undo/cancel/failure/teardown atomicity U, REQ-034–035 | Trace transaction and task-cancellation paths for split, time edits and consolidation separately |
| Q-ARR-004 | Consolidation samples/format and resource failure U | Establish pre-effect render call, file writer settings and failure path; extracted isolated arithmetic only if bounded |
| Q-ARR-005 | Locator, loop, meter and time-command object transforms U | Trace each object update path; separate UI edit grid from scheduler quantization |
| Q-ARR-006 | Linked mismatched-content and prior-group cleanup U | Finite membership/selection matrices against linked edit dispatch, including hidden lanes |
| Q-ARR-007 | Fade sample gains and clamp laws U | Trace Arrangement fade storage-to-render path; do not substitute Session fade law |
| Q-ARR-008 | Post-edit save/reopen and UI-state persistence U | Trace Arrangement reader/writer at exact schema fields; retain schema-conformant scenarios with explicit expectations |

## Analyst evidence appendix

This appendix is analysis-only and must be reviewed out of a clean handoff.
Full digests, capture metadata and retained evidence are in the packet
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manifest.json).

| Key | Exact locator, target and limitation |
| --- | --- |
| A6.n | `SRC-ARRANGEMENT-MANUAL-12-20261019`: captured [Arrangement chapter](https://www.ableton.com/en/live-manual/12/arrangement-view/), sections 6.1–6.14.2 as individually named above. [Retained text](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-arrangement.txt), headings and `ANCHOR` lines delimit each section. HTML SHA-256 `caf57b34a10fa4163300bced0a4384656d2823eefba340ad82327e9118e05842`; text SHA-256 `f6ce9d5acdf9014be94e9e858084cf9b8cfb309c1bc4e1172581cc951d7cd36f`. Captured 2026-10-19; Live 12, exact build unidentified; prose examined, linked images not visually inspected |
| C3.n | `SRC-CONCEPTS-MANUAL-12-20261019`: captured [Concepts chapter](https://www.ableton.com/en/live-manual/12/live-concepts/), sections 3.6, 3.7 and 3.8. [Retained text](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-concepts.txt). HTML SHA-256 `da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5`; text SHA-256 `808c0bb7658060ccfcbd5f829c735dfb94d77b7ba496d8f6aca73d8454e58be7`; same version/capture/image limitations as A |
| P | `SRC-ARRANGEMENT-PACKAGE-12403`: [schema/demo inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/schema-demo-survey.json), exact JSON keys `schema.classes` and `demo.main_lane_clips`/`demo.locators` carry field/XPath locators. Installed `12.0_12402.txt` SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`; demo SHA-256 `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b`. Bundle 12.4.3; demo Creator 12.4d1, revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. No edit/save run; main lanes only |
| N | `SRC-ARRANGEMENT-REGISTRY-12403`: [retained native record](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/native-command-registry.jsonl), arm64 entry `0x101741430`, source chunk/offset/line SHA-256 carried in record. Exact names include Split, Consolidate, Duplicate, LoopSelection, CreateFade, BackToArrangement, Undo and Redo; S corroboration of name registration only. No dispatch reachability or edit law inferred; image pin in manifest |

D-package representation does not promote manual clauses to S or X. A prior
clip-launch inventory's 90 Arrangement/take-lane clips is a different selection
from this packet's 64 main-lane clips; neither count invalidates the other.

## Revision and handoff

Revision 1 adds 35 requirements and 65 acceptance scenarios: 51 fully scoped
D-manual documentation checks, one D-package representation check, and 13
ungraded or partly ungraded cases (AR-009, 018, 023, 030, 036, 041, 043,
060–065). D cases often name additional excluded observations explicitly;
only their stated expectation is proposed for grading. No X-backed edit behavior,
release, original-versus-candidate comparison, or compatibility pass is claimed.
