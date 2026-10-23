---
id: SPEC-ARRANGEMENT-EDITING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
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

R2 (ARR-B104/B106): clicking the loop brace or Edit Select Loop selects material within the loop; this is distinct from Loop Selection, which sets/enables the loop. Track unfold/height controls are separately specified in REQ-041. Keyboard Move Clips setting and focus remain with the navigation owner.

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

R2 literal platform inputs (ARR-B079): CtrlShift (Win) / ShiftOption (Mac) performs slip; CtrlAltShift (Win) / CmdOptionShift (Mac) bypasses the grid during slip. This source role does not infer unwarped support or source-coordinate wrapping.

### REQ-ARRANGEMENT-006 — Editing grid and object snapping

D-manual (A6.7, A6.10): clip edits snap to the editing grid and to relevant clip
edges, locators and meter changes. The grid supports adaptive and fixed modes,
narrow/wide steps, triplets and on/off. Cmd-1 doubles line density; Cmd-2 halves
it; Cmd-3 toggles triplets; Cmd-4 toggles snapping; Cmd-5 toggles fixed/adaptive.
Cmd temporarily bypasses an enabled grid, and temporarily enables a disabled
grid during an action. Snap priority, attraction distance, rounding ties,
adaptive zoom thresholds and grid extrema are U; no nearest-grid formula is
asserted.

R2 (ARR-B113/B114/B120/B121): grid width is offered in Arrangement main-lane and MIDI Note Editor context menus; the listed adjustment shortcuts are also Options menu commands. Current adjacent grid-line spacing is displayed above the time ruler at the lower right. The source gives Alt (Win) / Cmd (Mac) for temporary grid bypass/enable; this differs from the slip modifier. Existing numeric examples remain documentary only.

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

R2 (ARR-B135/B136): Consolidate is offered by Edit, main-lane context menu and CtrlJ (Win) / CmdJ (Mac). After admission the generated clip can be moved; MIDI clip edges can be dragged for repetitions. Eligibility and repetition/storage laws remain with the corresponding clip owners.

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

R2 (ARR-B043–045): Create Add Locator and scrub-context Add Locator are separate entrypoints. The Set/Delete Locator control roles depend on actual locator selection. Recording eligibility/capture is owned by Recording; naming the recording context does not prove it runs.

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

R2 (ARR-B048): move by drag or arrows; Rename through Edit or CtrlR (Win) / CmdR (Mac); Edit Info Text through Edit or locator context; delete through Delete key, Create Delete Locator, or the Delete Locator button. Locator text limits and generic clip metadata remain separately owned.

### REQ-ARRANGEMENT-017 — Arrangement loop selection and brace editing

D-manual (A6.6): Loop Selection sets the brace to the time selection and enables
the Arrangement loop. The loop start and length can be edited numerically.
Dragging brace edges changes its start/end; dragging the bar translates it
without changing length. Left/right arrows nudge by the grid; up/down shifts by
its length. Cmd-left/right changes length by the grid; Cmd-up/down doubles/halves
length. Set Song Start Time Here on the brace makes playback start there instead
of the insert marker/selection. Clamp and rounding behavior is U. Stored fields
and scheduler behavior remain owned by the transport/playback specs.

R2 (ARR-B063–072): the Control Bar toggle directly activates the Arrangement Loop. In the documented no-clip/no-time-selection context the brace covers the Arrangement; no constructor/reset rule is inferred. Loop Start/Length fields expose start and length. Edit Loop Selection and CtrlL (Win) / CmdL (Mac) address selected time; the shortcut can toggle looping with a clip/time selection. The brace context menu provides its separate Set Song Start Time Here input. Competing locator/brace overrides remain U.

### REQ-ARRANGEMENT-018 — Add and edit meter markers

D-manual (A6.5): Insert Time Signature Change places a meter marker at the insert
marker. Markers can be moved, edited with Edit Time Signature/Cmd-R, or deleted.
The documented text grammar accepts a one- or two-digit numerator and a
denominator in {1,2,4,8,16}, separated by slash, comma, period or spaces. Updating
the Control Bar meter changes the meter at the current play location, stopped
or running. Invalid/zero values, exact text parsing and migration are U; this
does not replace the narrower stored-value grammar in SPEC-TRANSPORT-STATE.

R2 (ARR-B051–056/B061): marker insertion is offered through Create or scrub context; move by mouse or left/right arrows; Edit Time Signature through Edit, scrub context or CtrlR (Win) / CmdR (Mac); delete by Delete or Edit Delete. Actual meter changes show an automation LED in the Control Bar fields; the marker area below the ruler is hidden if there are no changes. MIDI import offers the saved-meter-information branch; accepting it is documented to create meter markers. This adds only the offered choice/marker roles, not MIDI bytes, exact positions, tempo import or a replacement for Media/Transport laws.

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

R2 (CON-B042): the global return control is documented in Session Main and at the top-right of the Arrangement scrub area. The existing per-track return remains distinct. Current Session R3 SV041 supplies deliberate nonsequential requests; old SV001 only supplies its actual neighboring A/B gestures and is not used as nonsequential proof.

### REQ-ARRANGEMENT-022 — Access clip fade controls

D-manual (A6.8): audio clip beginnings and ends have editable fades; adjacent
clips on the same audio track can have a crossfade. Handles are accessible by
hovering with enough track height. In Automation Mode, holding F while hovering
an automation lane temporarily exposes fade controls. Fades belong to clips and
are independent of automation envelopes. This is not the automatic Session
launch fade already covered in SPEC-PLAYBACK-CORE.

R2 (ARR-B082–084/B097): a folded or too-small track must be enlarged to expose the handles; ordinary clip hover and Automation Mode plus held F are distinct inputs. Clip-owned fade versus Arrangement envelope editing is a control-state distinction, not proof of independent rendered audio.

### REQ-ARRANGEMENT-023 — Edit/create fades and crossfades

D-manual (A6.8): fade start/end handles change fade duration without moving fade
peaks; fade edges cannot pass those peaks. Curve handles shape the fade.
Selecting time including a clip beginning/end enables Create Fade In/Out
(Cmd-Option-F). A fade handle dragged across a neighboring clip edge creates a
crossfade; selecting time spanning their boundary enables Create Crossfade.
Curve coefficients, equal-power/linear laws, rendered gains and rounding are U.

R2 (ARR-B085/B088–090): separately drag Fade In Start/Fade Out End duration handles with peaks retained, drag a fade over the adjacent edge, then drag its crossfade slope handle. Visible controls do not establish numerical curves.

### REQ-ARRANGEMENT-024 — Fade boundaries and defaults

D-manual (A6.8): fades cannot cross clip loop boundaries and a clip's start/end
fades cannot overlap. Selecting a handle displays its limiting boundary. Delete
on a fade handle removes the fade when Create Fades on Clip Edges is off; with
that preference on it resets to a documented default 4 ms. That preference also
creates 4 ms crossfades between adjacent audio clips. Limits on very short clips
and the exact audio realization of 4 ms are U, so no sample-count rounding is
specified.

R2 (ARR-B092/B096): select a fade handle to display its dotted limiting boundary; preference-created adjacent crossfades can subsequently be edited like manual ones. The nominal 4 ms source description remains uncalibrated and is not a numeric/sample oracle.

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

R2 (ARR-B004/B005/B016/B018/B022–026): the Arrangement Overview spans the complete Arrangement and outlines its displayed portion. Horizontal/vertical drags scroll/zoom; within-outline double-click returns to the whole Arrangement. The beat-time ruler has the same drag axes; double-click zooms to selection, or the whole Arrangement without selection. Time-ruler horizontal drag scrolls. Progressive zoom uses +/− or Ctrl (Win) / Cmd (Mac) wheel/trackpad; CtrlAlt (Win) / CmdOption (Mac) drag pans. Optimize Height/Width and H/W fit the track/layout display. Alt (Win) / Option (Mac) wheel in a main lane vertically zooms the selected track, or all tracks with content in a time selection. Selecting Arrangement clip time also zooms the Clip View editor to it. Follow is offered by Control Bar and Options. Pause/resumption claims require genuinely moving playhead and automatically scrolling Arrangement before an actual pause trigger; stop alone does not promise moving scrolling while stopped. Current Clip R2 REQ031/CV063–067 owns the within-clip Overview and editor Follow contexts, not the Arrangement axes or Arrangement pause triggers. No viewport, timing or public dispatch formula is added.

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

### REQ-ARRANGEMENT-036 — Arrangement scrub inputs

D-manual (A6.1, A6.3; ARR-B006/B036–039): with Permanent Scrub Areas enabled, clicking the Arrangement scrub area starts playback from the chosen point. Held left button repeats the area according to global launch quantization; jumps between points are documented as quantized. With that setting off, Shift-click in the Arrangement scrub area or beat-time ruler still scrubs. Settings owns setting exposure; Clip View owns its separate clip scrub. Quantized boundaries, repeated duration, actual playback, sound, default initialization and dispatch outcomes remain U; no scheduler law is inferred.

### REQ-ARRANGEMENT-037 — Device drop-area track creation

D-manual (A6.1; ARR-B015): dragging an available instrument or MIDI effect into the Mixer Drop Area below Arrangement tracks creates a MIDI track; an available audio effect creates an audio track. This is the bare-device entrypoint, separate from Mixing existing-clip/device-chain drag. Unsupported device admission, failure, transaction, default routing and actual device processing remain U.

### REQ-ARRANGEMENT-038 — Waveform display zoom

D-manual (A6.1; ARR-B017): Waveform Vertical Zoom Level enlarges the waveform display without requiring a clip-gain adjustment; its display setting applies to all Arrangement audio tracks and new clips as recorded. This is a display role, not an audio gain equivalence, waveform amplitude formula, recording-capture result or pixel mapping.

### REQ-ARRANGEMENT-039 — Public transport and Arrangement Position inputs

D-manual (A6.3; ARR-B028–035): Play and Stop request Arrangement playback start/stop; space toggles playback. The insert marker determines the ordinary start position; Shift-space continues from the last stopped position. Home (Win) / Function-left (Mac) returns the marker to the starting play position. Double Stop remains Session REQ003. Selecting an Arrangement Position bars/beats/sixteenths field permits vertical drag, typed number plus Enter or up/down arrows; adjusting the fields moves the insert marker. The publisher initial-marker wording is documentation context, not observed factory/reset behavior. Engine timing, parsing, sample/beat arithmetic, competing starts, range/rounding and universal key interception remain U.

### REQ-ARRANGEMENT-040 — Chase MIDI Notes option

D-manual (A6.3; ARR-B040): Options Chase MIDI Notes can deactivate/reactivate the documented chase behavior when playback begins inside a note. The publisher describes chasing as default; initial, saved/custom and reset histories remain distinct and unverified. This names an option and intended context only. Note messages, scheduling, audible output, numeric timing, channel/voice and default initialization remain U under the existing Playback late-note obligation.

### REQ-ARRANGEMENT-041 — Unfold and resize Arrangement tracks

D-manual (A6.9; ARR-B104): the button next to a track name or U unfolds selected tracks to access clip time. The split line changes unfolded height; Alt+/Alt− (Win) / Option+/Option− (Mac) are named alternatives. Alt (Win) / Option (Mac) pinch resizes on a supported trackpad/touchscreen. Holding that modifier while resizing one track resizes all; modifier-clicking the unfold button or AltU (Win) / OptionU (Mac) unfolds all. Capability, actual key dispatch, limits, geometry, persistence and unsupported input hardware remain U.

### REQ-ARRANGEMENT-042 — Arrangement mixer entrypoints and control surfaces

D-manual (A6.1, A6.15; ARR-B013/B019/B160–164): the Arrangement mixer is offered by View Mixer, CtrlAltM (Win) / CmdOptionM (Mac), and the bottom-right mixer control. View Mixer Controls customizes mixer controls; View Arrangement Track Controls separately customizes individual track controls. The source states shared values/settings between those surfaces; Performance Impact, track delays and crossfader are named mixer-only examples. Mixing REQ001/MXW001 already owns actual access to the section/components and individual controls; Engine ER006/007 and Mixing MXW015 own their named displays. No all-control bijection, new mixer coefficient, track-delay/CPU law, key interception or layout persistence is inferred.

## Timing, state and comparators

D-manual documentary grading is limited by the versioned R2 catalog to named
visible input/control/selection roles. Retained R1 extents, file-location and
playback predicates remain source claims where the R2 documentary oracle is null.
Every actual outcome remains null/U. Every case below states its proposed subset. A partly unspecified action is not upgraded by a neighboring D case.
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
| AR-002 | 001 | boundary | Drag time 4–8 on A; Shift-extend to B Then use Shift-arrows on reset to extend and shorten a known nonempty selection. | Time selection extends across those tracks; exact anchor rule ungraded (D A6.9) |
| AR-003 | 002 | negative | Select A only; ordinary Copy On reset owned clips with clear compatible destinations, separately use ordinary Cut, Paste and Duplicate after productive Copy; retain another-track control. No occupied destination or duplicate-position rule is assumed. | Copy is scoped to A's selection, not all-track time insertion (D A6.9/11); clipboard bytes U |
| AR-004 | 003 | positive | Drag A's clip bar from 0 to a clear grid point 8 Separately transfer that admitted clip to another compatible same-type track with a clear target. | Clip changes position to the effective snapped point (D A6.7) |
| AR-005 | 003 | positive | Drag left/right edge of a compatible interior clip | Corresponding edge changes clip extent (D A6.7); source-edge bounds U |
| AR-006 | 003 | negative | Drag inside unfolded waveform without slip modifiers | Time selection changes instead of moving the bar (D A6.7/9) |
| AR-007 | 004 | negative | Try placing audio clip on M; repeat MIDI on A First independently establish a compatible same-type transfer (AR004); use validated audio/MIDI clips, not unavailable inputs. | Neither successfully inserts the incompatible clip type (D C3.8); feedback U |
| AR-008 | 005 | positive | Shift-Option drag M content; repeat warped audio | Content shifts while clip boundaries stay fixed (D A6.7); exact note mapping U |
| AR-009 | 005 | boundary | Slip an unwarped audio clip | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: unsupported extension of documented gesture |
| AR-010 | 006 | positive | Cmd-1 from eighth-note grid, then Cmd-2 | Sixteenth-note then eighth-note grid (D A6.10) |
| AR-011 | 006 | positive | Toggle triplets, fixed/adaptive and snapping via commands | Corresponding modes toggle; no adaptive threshold asserted (D A6.10) |
| AR-012 | 006 | boundary | Edit with Cmd held, grid initially on and then off | Meter-grid snapping bypassed when on, temporarily enabled when off (D A6.10); object-snap priority U |
| AR-013 | 007 | positive | Select audio across A/B and press 0 | Selected material deactivated (D A6.9); second-press law U |
| AR-014 | 007 | negative | Select M plus audio and invoke Reverse Clip(s) First establish genuine productive audio-only Reverse through AR015; then reset with known MIDI plus audio. No absent capability can count as rejection. | Mixed selection cannot be reversed (D A6.9); partial rejection feedback U |
| AR-015 | 007 | positive | Select audio-only range and invoke Reverse Clip(s) | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Audio selection reversed (D A6.9); exact file/waveform values U |
| AR-016 | 008 | positive | Clip at 0–16, insertion point 8; Split After successful Split actually move then edit one admitted new part; inspect a separately retained other part, without a note/source identity law. | Independently editable parts at 0–8 and 8–16 (D A6.12); note edge ownership U |
| AR-017 | 008 | positive | Clip at 0–16; select 4–12; Split After successful isolation actually move/edit that part on reset; retain the outer parts separately. | Selection becomes distinct clip with edges 4/12, outer material separate (D A6.12) |
| AR-018 | 008,033 | boundary | Split exactly at existing edge | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: no-op, selection and undo effects not established |
| AR-019 | 009 | positive | Adjacent A clips at 0–4/4–8; select both; Consolidate | One editable A clip represents selected material (D A6.13); exact metadata U |
| AR-020 | 009 | positive | Repeat AR-019 simultaneously on A/B | One consolidated clip for each selected track (D A6.13) |
| AR-021 | 010 | positive | Save Set in Project; consolidate A/B | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. New samples placed under that Project's Samples/Processed/Consolidate (D A6.13); naming/format U |
| AR-022 | 010 | boundary | Unsaved Set, configured Temporary Folder; consolidate A | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Generated sample uses Temporary Folder (D A6.13); relocation after save U |
| AR-023 | 010 | negative | Compare consolidation with track effect on/off and altered mixer; same clip processing First establish actually playing nonzero owned clip processing and independently active nonzero track effect plus mixer contribution with a nonmuted wet/return/output route. Retain the same input, processing and route across each contrast; a visible enabled flag or zero contribution is insufficient. All documentary signal/file/timing comparisons remain null. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Consolidated source signal precedes effects/mixer and includes clip processing (D A6.13); no numerical render comparator established |
| AR-024 | 011 | positive | All tracks have later clips; select two-beat range on A; Delete Time | All-track two-beat removal; later material two beats earlier; duration shorter by two (D A6.11); boundary-crossing clips U |
| AR-025 | 011 | positive | Cut a two-beat range; later Paste Time in clear region | Cut reduces and paste adds that duration; cut material is available for paste (D A6.11); mapping details U |
| AR-026 | 012 | positive | Select two-beat timespan; Duplicate Time | Copy inserted, total duration increases two beats, all-track time insertion (D A6.11); insertion position U |
| AR-027 | 013 | positive | Marker at beat 8; Insert Silence of two beats | Empty interval inserted at 8, all tracks gain two beats of timeline space (D A6.11); effects-tail audio U |
| AR-028 | 014 | positive | Stopped, no range, marker at 12; Set Locator | Locator at 12 (D A6.4) |
| AR-029 | 014 | boundary | Stopped, selected time 8–12; Set Locator | Locator at selection start 8 (D A6.4) |
| AR-030 | 014 | timing | Running, nonzero global quantization; Set Locator between grid lines First establish actual running nonempty Arrangement with positive audible output and usable nonzero quantization; keep exact boundary/timestamp U. Separately admit a Recording-owned productive record context before Set Locator there. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Addition follows global quantization (D A6.4); precise boundary/sample ungraded U |
| AR-031 | 015 | positive | Stopped; double-click a locator at 16 | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Locator selected, playback starts there (D A6.4); latency U |
| AR-032 | 015 | boundary | At first/last locator use Previous/Next | Navigation reaches Arrangement start/end respectively (D A6.4) |
| AR-033 | 015 | positive | Enable Set Song Start Time Here on locator; select elsewhere; Play | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Playback starts at locator rather than time selection (D A6.4); competing brace override U |
| AR-034 | 016 | positive | Rename, annotate, move, then delete selected locator Use actual drag then arrows, Edit Rename then CmdR (Mac) / CtrlR (Win), Edit versus locator-context Edit Info Text, and separate Delete key/Create Delete Locator/Delete Locator button histories; retain selected Set-to-Delete state. | Requested visible text/position edits and deletion apply (D A6.4); text limits U |
| AR-035 | 016 | positive | Locators at 8/16; Loop to Next Locator from 8 | Loop spans those locators (D A6.4); sample scheduling follows separate scope |
| AR-036 | 016 | boundary | Last locator; Loop to Next Locator | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: no next-locator fallback established |
| AR-037 | 017 | positive | Select time 8–16; Loop Selection | Loop enabled with brace covering selection (D A6.6) |
| AR-038 | 017 | positive | Drag brace bar to another clear position | Start/end translate and length unchanged (D A6.6) |
| AR-039 | 017 | boundary | From four-beat length, Cmd-up then Cmd-down | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Length doubles to eight then halves to four beats (D A6.6); lower limit U |
| AR-040 | 018 | positive | Insert meter at marker 8, enter 7/8; move/edit/delete On separate resets use Create and scrub-context insertion; move by drag and left/right arrows; Edit and scrub-context Edit Time Signature plus CmdR/CtrlR; Delete key versus Edit Delete. No invalid-text preservation is inferred. | Requested marker operations apply for documented meter text (D A6.5) |
| AR-041 | 018 | malformed | Enter 7/3, zero numerator, or nonnumeric meter text | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: refusal/coercion and prior-state preservation unknown |
| AR-042 | 019 | boundary | Meter change inside an existing bar on editing grid | Fragmentary bar is permitted and indicated (D A6.5) |
| AR-043 | 019 | positive | From known fragment, Delete Fragmentary Bar Time; separately Complete Fragmentary Bar | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. First removes fragment time; second inserts missing time across tracks; next change lands on barline (D A6.5); exact duration calculation U |
| AR-044 | 020 | positive | A/B Arrangement playing; launch Session clip on A Require independently known nonempty actually playing Arrangement A/B and unmuted output, then an admitted Session launch; selection or eligibility is not playing proof. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. A plays Session, B keeps Arrangement; view switches leave clip choice unchanged (D C3.6–7) |
| AR-045 | 021 | positive | A/B overridden by Session; use A's Back to Arrangement First independently establish actual nonempty A/B Session takeover from productive Arrangement playback and nonmuted return paths; inspect A return separately from B. Do not grade empty/stopped transition timing. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. A resumes Arrangement; B remains overridden (D C3.7); transition sample U |
| AR-046 | 021 | positive | A/B overridden; activate global Back to Arrangement First independently establish both actual nonempty Session takeovers and productive Arrangement routes; on reset invoke the global control in Session Main versus Arrangement scrub area. Retain actually active clip identities separately from requested/selected ones. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Both return to Arrangement; button indicates override while Session tracks active (D C3.7); transition/empty-region rules U |
| AR-047 | 022 | positive | Expanded audio track; enable Automation Mode, hover lane while holding F First compare ordinary hover on folded/too-small versus enlarged admitted track. With Automation Mode truly active hold then release F while hovering the lane; do not infer default key focus. | Fade controls temporarily accessible; clip fades remain distinct from envelopes (D A6.8) |
| AR-048 | 023 | positive | Select time at beginning/end; Create Fade In/Out; adjust curve | Fade created on relevant clip edge and curve editable (D A6.8); numerical curve U |
| AR-049 | 023 | positive | Adjacent A clips; select time over boundary; Create Crossfade | Crossfade created between adjacent clips (D A6.8); gain law U |
| AR-050 | 024 | boundary | Try extending fade through loop edge, across opposite fade, or edge past peak First perform a successful shorter nonzero fade edit with genuine clip-loop/opposite-fade/peak bounds; select each handle and inspect its limit line before attempted extensions. | Stated fade limits hold (D A6.8); exact limiting value on very short clips U |
| AR-051 | 024 | positive | Preference off; select fade handle; Delete | Fade removed (D A6.8) |
| AR-052 | 024 | boundary | Preference on; delete fade handle; create adjacent audio clips Retain nominal4ms only as source_claim, not numeric oracle. After a genuinely preference-created crossfade, actually edit its offered duration/curve controls. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Deleted fade resets to nominal 4 ms; adjacent clips get nominal 4 ms crossfade (D A6.8); sample rounding/short-clip limit U |
| AR-053 | 025,026 | positive | Link A/B; inspect indicator; add M with Cmd-Link Tracks; unlink M | Membership indicators/select behavior and requested add/remove operations work; each track in at most one linked instance (D A6.14.1); residual singleton policy U |
| AR-054 | 027 | positive | A/B linked, matching clips 0–16; select 4–12 and Split | Both linked tracks isolate matching selected portions (D A6.14.2); mismatched-content rules U |
| AR-055 | 028 | negative | Linked A/B fades start at different times; adjust A Before this negative establish successful simultaneous create/edit of same-start linked A/B fades on reset; then use differing actual start positions with the same admitted operation. No hidden propagation grade. | Simultaneous adjustment does not cover mismatched-start fades (D A6.14.2); any other selection changes U |
| AR-056 | 029 | positive | Z-zoom twice; X twice; separately edit during Follow Use owned nonempty Arrangement, actually moving playhead and genuine automatic Arrangement scrolling across its visible boundary before a real edit. Establish actual paused Follow after edit before separate stop/restart histories. Stop alone never asserts moving scrolling while stopped; shared Clip editor Follow/Overview stays with current Clip R2. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Previous Z zoom states restored; edit pauses Follow; restart resumes it (D A6.2); pixels/timing U |
| AR-057 | 030 | boundary | Linked A/B; B take lanes hidden; rename corresponding lane | Documented linked rename includes hidden lane (D A6.14.2); recorded/comped material behavior U |
| AR-058 | 031 | persistence input | Inspect pinned demo through an independent document reader | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. 64 main-lane clips: 9 AudioClip under Sample, 55 MidiClip under ClipTimeable; 9 named locators (D-package P); not a save/reopen pass |
| AR-059 | 032 | negative | Lock Envelopes on; move a clip with Arrangement envelope underneath Use nonempty owned clip and independently real changing Arrangement envelope at song position; first establish a productive clip move then reset Lock ON. No inactive/static envelope or zero processing can prove lock behavior. | Envelope remains at song position (D A6.1); lock-off/breakpoint laws U |
| AR-060 | 033 | boundary | Ordinary Duplicate into occupied timeline, overlap-drop, resize to zero, or no-selection Split First establish corresponding productive ordinary duplicate/drop/resize/Split on compatible nonempty material; then each boundary on reset. Invalid/zero/no-selection outcomes remain U. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: destination, replacement, limits and command availability unknown |
| AR-061 | 034 | undo/redo | Split/drag/time insertion/consolidate/link, then Undo and Redo Establish a genuinely successful nonempty named operation first; then separate Undo/Redo histories without promised grouping or rollback. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: grouping, restored state and media side effects unknown |
| AR-062 | 034 | cancellation | Begin clip/fade/locator drag; press Esc; separately cancel consolidation Establish genuinely active admitted gesture/consolidation before offering cancel; retain unknown accepted cancellation input and outcome. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: accepted cancel input, rollback and temporary media unknown |
| AR-063 | 034 | error | Consolidation destination unwritable or full Require independently valid owned writable destination and successful nonempty consolidation baseline before a separately supplied safe failure fixture. No real disk exhaustion or destructive setup is performed. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: diagnostics, partial files and original material state unknown |
| AR-064 | 035 | persistence | Save/reopen after clip, fade, locator, link and song-start edits Require successful concrete edits and independently admitted valid save/reopen baseline before persistence probes; no old package-only inspection substitutes for a write roundtrip. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: exact reopened fields/identity/playback and source paths unknown |
| AR-065 | 035 | teardown | Close/replace Set during drag, consolidation or pending locator jump Require a genuinely active admitted gesture/consolidation/pending locator operation before close/replace; mere eligibility is insufficient. | Source claim only; documentary numeric/signal/timing/file or unresolved outcome/comparator null. Ungraded U: prompts, cleanup, pending operation cancellation and retained state unknown |
| AR-066 | 029 | documented-control-context | Use owned nonempty Arrangement with distinct extents, two tracks and visible ClipView. Separately drag Overview horizontally/vertically, double-click inside outline; beat-ruler drag and double-click with versus without selection; time-ruler horizontal drag; plus/minus, platform-modified wheel and pan; actual H/W controls; Option/Alt main-lane wheel with one selected track versus multitrack time selection. Independently select Arrangement time and inspect ClipView extent, distinct from CV own-editor zoom. Reset focus/key/grid histories per trial. Use literal +/−, Ctrl (Win)/Cmd (Mac) wheel and CtrlAlt (Win)/CmdOption (Mac) drag. Use View Zoom to Arrangement Time Selection separately from Z. Compare only Arrangement display roles; current CV063 owns within-clip overview axes. | Only complete Arrangement overview/displayed-outline, separately admitted display input roles, selection-to-editor and named height/width controls; geometry/zoom quantities U. |
| AR-067 | 036 | outcome-obligation | With genuinely playing distinguishable nonempty Arrangement material and nonmuted positive output, independently admit the actual Arrangement scrub surface. Explicitly set ON and click separate points, hold/release left button; on reset set OFF then Shift-click Arrangement scrub and beat-time ruler. Retain global quantization and selected region separately, record actual offered setting/default provenance. Reuse CV033/034 only for the distinct clip editor branch. Declare exact ON/OFF setting and invoke actual click, held-left-button then release, OFF Shift-click in scrub versus beat-time ruler; no repeat period/release result is guessed. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-068 | 037,038 | documented-control-context | Use independently available actual instrument, MIDI effect and audio effect in separate reset trials; drop each into known blank area below Arrangement tracks, retaining track type/device presence. Contrast MXW008 actual existing-clip drag. On owned distinct audio A/B use waveform zoom slider with unchanged declared clip gain; inspect both displays and a separately admitted recording-owner new-clip context, not audio output.  | Bare available instrument/MIDI-effect versus audio-effect drop provides the named MIDI/audio-track creation roles; waveform slider is a shared display control without a gain/output comparator. |
| AR-069 | 029 | outcome-obligation | Independently establish actual moving playhead and automatic Arrangement scrolling across visible boundary, then separately edit, scroll horizontally or click beat-time ruler and observe Follow state. On reset use Control Bar toggle versus Options Follow command. After positively observed pause try stop, restart, Arrangement scrub and clip scrub as separate histories; do not assert moving scrolling while stopped. This is actual Arrangement scrolling, distinct from current ClipR2 CV031/063–067 editor contexts. Reset separately for Options Follow versus toggle, each of edit/horizontal-scroll/beat-time-ruler-click pause triggers, and stop-alone/restart/Arrangement-scrub/clip-scrub resumption. Preserve stopped versus playing states. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-070 | 039 | outcome-obligation | Use actual nonempty Arrangement and positively audible playing source before Stop/space-off; separately stopped Play and space-on. Use distinct known stopped and insert positions before Shift-space. Independently select each actually offered Position field and drag, type admitted value+Enter, or arrow; inspect visible insert marker. Reuse SV003 for doubleStop; retain Home Windows/Fn-left Mac as separately admitted return-marker role and source starting-play-position wording without equating all histories to1.1.1. Use actual Play, Stop, space ON and OFF, Shift-space, Home (Win)/Function-left (Mac). Select each offered Position field separately for vertical drag, typed admitted number plus Enter, and up/down arrows. Double Stop is current Session003/SV003; no duplicated semantics. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-071 | 040 | outcome-obligation | Use independently admitted MIDI instrument/clip with a sustained nonzero note and a genuine normal full-start audible baseline. Retain an actually offered Chase MIDI Notes option and separately selected ON/OFF histories before starting inside the note. Record initial/fresh versus saved/custom state separately; do not determine exact note events, order or output from option label. Publisher default is source context only, not a measured fresh/reset result. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-072 | 014,015,016,021 | outcome-obligation | With known distinct locators and successful creation baseline, use Create and scrub-context Add Locator separately; compare stopped insert/range to genuinely running Set Locator and separately eligible recording context. Actually click an interior locator and Previous/Next between interior locators before endpoint trials. Retain genuine active playback and output before running jumps. Refine AR034 to actual drag/arrows, Rename menu/chord, Edit Info Text entries and each Delete entry; inspect Set/Delete role. Exercise actually offered global controls in Session Main versus Arrangement scrub, with per-track return remaining AR045. After genuine Arrangement-to-Session takeover, retain a separately admitted Session end/stopped history before manual return; do not assign a new slot/StopAll law to this source. Current SessionR3 SV041 owns deliberate C/A/E requests; historical SV001 is only A-name/Enter, neighbor-B/arrows, B-triangle. Set Locator in a recording history requires an independently established productive Recording-owned recording path, not merely eligibility. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-073 | 018 | documented-control-context | Use independently valid one/two-digit numerator examples, each named denominator and slash/comma/period/spaces delimiter as admitted inputs; reset on invalid unsupported control. Actually change Control Bar numerator/denominator in stopped and genuinely running histories, inspect LED with real meter changes and marker-area absent/present contrast. Refine marker drag/arrows/Edit-menu/context/chord/Delete entry actions. Use independently validated MIDI file containing known meter changes; retain offered import-meter option accept versus decline separately, with MF019 marker insertion baseline. For source grammar use admitted examples 7/8, 12,4, 5.2, and 9   16 plus denominator1 separately; do not claim exhaustive parser. In Control Bar separately type/adjust numerator and denominator while stopped versus genuinely playing; compare actual marker-area absent/present and automation LED. Meter-bearing validated MIDI: offered import-meter accept versus decline with actual MF019 import baseline; exact positions/numeric/file results U. | Named meter input/menu and absent/present marker-area/automation-LED roles; import-meter choice is offered separately, without numeric marker positions or MIDI-file oracle. |
| AR-074 | 017 | documented-control-context | On owned nonempty Arrangement establish current selection/clip states and productive Loop Selection. Separately use direct Control Bar loop toggle, independently no-selection brace context, actual Loop Start/Length field edit, selected-clip/time CmdL/CtrlL toggling, left/right grid nudge, up/down whole-length shifts, Cmd/Ctrl-left/right length edits, left/right edge drags and existing bar translation. Use brace Set Song Start Time Here separately from existing locator AR033; competing locator/brace flags stays U. Actually use CtrlL (Win)/CmdL (Mac), Edit Loop Selection versus direct Control Bar toggle. With explicitly no clip/time selected inspect documented whole-Arrangement brace context; reset for numeric Start/Length fields, left/right, up/down, Ctrl/Cmd-left/right, each edge and bar drags. Brace SongStart tested separately from locator with competing flags U. | Named Control Bar loop toggle, selected-time Loop Selection, brace inputs and separate SongStart entrypoints only; all numeric extents and playback results U. |
| AR-075 | 022,023,024,028 | documented-control-context | Use admitted audio clips with real visible fades: fold/too-small then enlarge and hover; compare ordinary hover with actual AutomationMode/F held and released. Drag duration handle with visible peak retained, then curve. Separately drag fade across adjacent clip edge, then crossfade slope; retain selected-handle limit-line observation. After auto-created preference-ON crossfade, actually edit it. For linked A/B first create/edit fades at the same actual position successfully, then on reset use differing starts with exact productive baseline. Before bound attempts establish successful shorter nonzero fade edit and genuine loop/opposite-fade boundaries. Separately edit an admitted fade versus Arrangement envelope and inspect retained clip-owned control state; no numeric or rendered-audio independence comparator. Use Create Fade In/Out and CtrlAltF (Win)/CmdOptionF (Mac) as separate entrypoints; Create Crossfade is separate. Nominal4ms is source context only, not an audio/numeric comparator. | Only admitted fade/curve/limit-line input controls and clip-versus-envelope ownership; no duration, audio or rendered independence grade. |
| AR-076 | 001,007,041 | documented-control-context | Use two known nonempty tracks; actual unfold button and U, resize splitline versus offered shortcuts/pinch only on admitted hardware; separately modifier-resize all and modifier-button/all-unfold shortcut. Actually click brace or Edit Select Loop to select material, distinct from Loop Selection. Shift-arrow extend and shorten known nonempty selection. For track-header0 first establish genuine active audible nonempty track and selection, separately from current multiclips AR013; do not assume reactivation second press. Use selected-track U and unfold button, splitline resize, Alt+/Alt− (Win)/Option+/Option− (Mac), admitted modifier-pinch, modifier-resize all, modifier-click unfold all and AltU/OptionU on separate resets. Actually click brace versus Edit Select Loop, not Loop Selection. For track-header0 require genuinely active audible nonempty selected track before action; no second-press law. | Named unfold/height/select-loop and track-header-deactivation input contexts; no geometry, audio, dispatch or reactivation grade. |
| AR-077 | 006 | documented-control-context | Use owned nonempty clips, locators and meter changes at independently distinct admitted positions. Actually move near each object separately with grid state declared; preserve effective observed snapped position without nearest rule. Use Arrangement main-lane and separately admitted MIDI editor width context menu and Options alternatives; inspect current-spacing display after a known successful change, not a calibrated width/time mapping. Keep object edges, locators and meter-change snap targets independently distinct with declared grid state. Use Arrangement main-lane context and Options width command alternatives; MIDI editor width is its admitted external context. Preserve Alt (Win)/Cmd (Mac) bypass versus CtrlShift/ShiftOption slip distinction. | Named grid context/Options commands and spacing-display role only; no snapped numeric position, priority or threshold grade. |
| AR-078 | 002,003,008 | documented-control-context | Use compatible test-owned populated clips and known clear targets: ordinary Cut, Copy, Paste and Duplicate on reset selections with another-track control; actual same-type transfer to another track, distinct from AR007 invalid cross-type attempts. After point/range Split, actually move/edit a new part and retain another part independently. Keep occupied/edge/zero/invalid branches in AR060 U after productive successful operations.  | Named ordinary commands and actually admitted compatible transfer/new-part edit roles; no identity, destination, overlap or numeric position law. |
| AR-079 | 009,010 | outcome-obligation | On independently nonempty adjacent eligible clips use actual Edit/main-lane context/chord Consolidate inputs separately. After successful generated-clip admission, move it and separately try admitted MIDI edge repetitions under its owner. For AR023 establish actual playing nonzero clip processing and independently active nonzero track effect/mixer contribution with nonmuted wet/return/output baseline before on/off contrast; same owned input/clip processing and exact route retained. Saved/Temporary branches remain AR021/022, export post-fader role remains EXP003. Use Edit/main-lane-context/CtrlJ (Win)/CmdJ (Mac) separately. Export post-fader signal stays with Export; no new render law. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-080 | 025,026 | documented-control-context | Use owned nonempty independently admitted track set, one populated Group and two distinct disjoint linked instances. Actually use selected-header versus Group-header Link on resets; hover and click each indicator, then existing Cmd/Ctrl-add and Unlink. Separately link selected subset and linked/unlinked mixture; retain all prior/selected/unselected memberships without predicting residual grouping.  | Named Link/Unlink and actual indicator hover/highlight/click/select roles on the declared finite groups; residual singleton/group algorithm U. |
| AR-081 | 027,011,012,013 | documented-control-context | Start with genuine matching nonempty linked A/B clips and unlinked nonempty C. On reset copies actually move, resize both edges, select clip/time without edit, perform a named Time operation, and consolidate adjacent matched material; retain C because Time remains all-track regardless of links. Existing AR054 actual linked Split preserved. Admit each operation positively before mismatched/disabled negative variants. Use separate Cut Time, Delete Time, Paste Time, Duplicate Time and Insert Silence histories without reducing their all-track scope to linked A/B. | Named linked operation roles on matched eligible material; all-track Time scope includes C. No numerical transform or mismatch law. |
| AR-082 | 030 | outcome-obligation | Use genuinely linked eligible nonempty A/B plus unlinked C and independently valid take lanes. First establish productive ordinary arm/lane/Audition actions through Recording001/020/021. Actually arm then disarm linked tracks in separate histories; rename, insert and delete lanes, and Audition ON then OFF with B lanes separately hidden. Before OFF require genuinely playing nonempty take material, active transport and positive audible output/recording route where relevant. Retain no-corresponding-lane branch U. Recording001/020/021 retain underlying ordinary arm/take/Audition laws. Require actual playing nonempty take, active transport and nonmuted audible output before OFF. | Source claim only; documentary outcome/comparator null. See versioned catalog. |
| AR-083 | 042 | documented-control-context | Use exact admitted Arrangement mixer and individual Track Controls with productive pointer control baseline. Separately actual View Mixer, bottom-right toggle and platform chord; View Mixer Controls versus View Arrangement Track Controls show/hide. Choose one actually shared offered control, alter it in one surface and inspect the other, then reverse on reset; retain its existing value owner with no new coefficient law. Inspect mixer-only offered Impact, Track Delay and Crossfader separately; reuse ER006/007 and MXW015 actual visibility, no hidden control assumption. Use literal CtrlAltM (Win)/CmdOptionM (Mac) for the mixer input. Other offered controls retain the actual MXW001/ER006/ER007/MXW015 owners. | Named Arrangement mixer/individual-controls access/menu roles and one actually offered shared control relationship only; no coefficient/CPU/delay measurement. |
| AR-084 | 005 | documented-control-context | Use genuinely editable nonempty warped audio and MIDI with known interior asymmetric content and fixed visible edges. Establish normal modifier slip actually changes content first, then separately use documented bypass chord with declared grid on/off; compare no-slip bar/waveform roles. Keep actual unwarped audio probe AR009 U and no guessed note/source clamp. Use literal CtrlAltShift (Win)/CmdOptionShift (Mac) for bypass on the declared platform. | Only documented slip versus bypass input roles and fixed visible clip-boundary relation; numeric content mapping and sound U. |

Case presence is a finite proposal inventory, not full source or behavior closure. Every actual expected/comparison is null, target U and unexecuted. The R2 catalog explicitly separates retained source claims from documentary visible-role predicates; signal, timing, file and numeric outcomes have null documentary oracles. These proposals include finite boundary/lifecycle contexts, without exhausting them. Malformed input is confined to actual text
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
| A6.n | `SRC-ARRANGEMENT-MANUAL-12-20261019`: captured [Arrangement chapter](https://www.ableton.com/en/live-manual/12/arrangement-view/), sections 6.1–6.15 as individually named above. [Retained text](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-arrangement.txt), headings and `ANCHOR` lines delimit each section. HTML SHA-256 `caf57b34a10fa4163300bced0a4384656d2823eefba340ad82327e9118e05842`; text SHA-256 `f6ce9d5acdf9014be94e9e858084cf9b8cfb309c1bc4e1172581cc951d7cd36f`. Captured 2026-10-19; Live 12, exact build unidentified; prose examined, linked images not visually inspected |
| C3.n | `SRC-CONCEPTS-MANUAL-12-20261019`: captured [Concepts chapter](https://www.ableton.com/en/live-manual/12/live-concepts/), sections 3.6, 3.7 and 3.8. [Retained text](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-concepts.txt). HTML SHA-256 `da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5`; text SHA-256 `808c0bb7658060ccfcbd5f829c735dfb94d77b7ba496d8f6aca73d8454e58be7`; same version/capture/image limitations as A |
| P | `SRC-ARRANGEMENT-PACKAGE-12403`: [schema/demo inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/schema-demo-survey.json), exact JSON keys `schema.classes` and `demo.main_lane_clips`/`demo.locators` carry field/XPath locators. Installed `12.0_12402.txt` SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`; demo SHA-256 `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b`. Bundle 12.4.3; demo Creator 12.4d1, revision `42bc084cd8152e4fb737ef3fefd04b2bea5320e7`. No edit/save run; main lanes only |
| N | `SRC-ARRANGEMENT-REGISTRY-12403`: [retained native record](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/native-command-registry.jsonl), arm64 entry `0x101741430`, source chunk/offset/line SHA-256 carried in record. Exact names include Split, Consolidate, Duplicate, LoopSelection, CreateFade, BackToArrangement, Undo and Redo; S corroboration of name registration only. No dispatch reachability or edit law inferred; image pin in manifest |

D-package representation does not promote manual clauses to S or X. A prior
clip-launch inventory's 90 Arrangement/take-lane clips is a different selection
from this packet's 64 main-lane clips; neither count invalidates the other.

## Historical revision 1 and handoff

Revision 1 adds 35 requirements and 65 acceptance scenarios: 51 fully scoped
D-manual documentation checks, one D-package representation check, and 13
ungraded or partly ungraded cases (AR-009, 018, 023, 030, 036, 041, 043,
060–065). D cases often name additional excluded observations explicitly;
only their stated expectation is proposed for grading. No X-backed edit behavior,
release, original-versus-candidate comparison, or compatibility pass is claimed.

## Revision 2 source-audit adoption

The independently reviewed complete retained Arrangement/selected Concepts text
audit R2 motivates 19 bounded groups. R1 remains exact in the [prior spec](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/spec-r1.md).
The [R2 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/README-r2.md)
owns exact clauses, actions, source-facet reconciliation, immutable inputs and delta.
The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/arrangement/fixtures-r2.json)
add actual productive-operation/output gates; they supply no media, Set or run.
Seven new public-role clauses supplement the retained 35 IDs; 19 compound reset
cases supplement the retained 65 IDs. All exact-build outcomes remain U/null
and unexecuted; no topic, case family or source chapter is complete. The initial
R1 source-inventory validation and review remain historical, not a current pass.

Current [Session grid/scenes](session-view-workflows.md) owns its deliberate
nonsequential SV041 requests; old neighboring SV001 gestures remain bounded.
Current [Clip View](clip-view-workflows.md) owns its within-clip Overview and
editor Follow productive baselines. Arrangement-specific controls above do not
replace those roles or the finite playback, note, Warp, automation, recording,
mixer, storage or export laws. Every source image and linked destination remains
uninspected. Independent review of this owner successor is pending as of freeze.
