---
id: SPEC-MIDI-EDITING-TOOLS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentation, exact-build applicability unknown
---

# MIDI editor and note transformation/generation tools

## Scope and evidence boundary

Canonical owner for FEAT-MIDI-EDIT note editing and FEAT-MIDI-TOOLS: clip creation,
note/time selection, drawing, movement, resize/stretch, utility operations,
velocity/chance editing, folding, multi-clip focus and the 17 inventoried tools.
This is a **partial documented-domain contract**. D12 means documented in retained
current Live 12 manual bytes captured 2026-10-19; **every exact 12.4.3 behavior
remains U**, including rows whose parameter names occur in the pinned schema.
No original program, candidate, DSP or random-seed implementation was executed.
No requirements on this page are released or independently accepted.

[MIDI note storage](midi-note-storage.md) owns note domains, normalization and
serialization; [MIDI user mapping](midi-user-mapping.md) owns controller mapping,
not these editor transformations. [Playback core](playback-core.md) owns existing
engine timing/emission clauses; [automation envelopes](automation-envelopes.md)
owns existing envelope behavior. [Recording and comping](recording-comping.md)
owns recording/capture. Audio Warp remains with [warp markers](warp-markers.md).
MPE editor/input/output, tuning systems, groove extraction/application, conversion,
MIDI file import/export and full general Clip View properties remain separate
unclosed F-04 surfaces; this page does not acquire their behavior by association.

## Preconditions, units and comparison

Unless a row says otherwise: valid editable MIDI clip in Notes editor, audible
instrument only for preview, no incompatible modal state, and explicitly chosen
selection/grid/scale/loop settings. Cases start from a reset copy of the stated
fixture. Beats are quarter-note beats; musical fractions are note values, so
1/8 note equals half a beat in the authored cases. Windows/macOS modifiers are
written explicitly where relevant; Linux original-UI operation is not asserted.
Numeric comparisons concern represented note/time/value state, not pixel layout,
sound or host scheduling. Random cases compare documented bounds/invariants,
never a prescribed random stream. UI latency, curve samples, number rounding,
undo transaction size and overlap boundary equality remain U unless stated.

IDs below are stable. Every row is D12 with target U. E/T locators refer to the
analyst appendix; applicability/unknown clauses are part of each requirement.

## Requirements

| ID | Operation | Preconditions/input | Observable contract and limits | Evidence |
| --- | --- | --- | --- | --- |
| REQ-MIDI-EDIT-001 | Create empty clip | Empty Session slot on a MIDI track; double-click or Insert Empty MIDI Clip(s). In Arrangement select an empty timespan on a MIDI track and invoke the same command. Explicit remaining entries are Create > Insert Empty MIDI Clip(s) on an empty Session slot, Arrangement track-display double-click, and CtrlShiftM Win/CmdShiftM Mac on an empty Arrangement MIDI timespan. | Create a MIDI clip in that location. Initial length for double-click, defaults and occupied/audio-slot behavior remain U. | D12/E1; target U |
| REQ-MIDI-EDIT-002 | Draw and erase | Focused Notes editor; toggle Draw Mode with B; click empty grid, then existing note. In inactive Draw Mode double-click empty grid or an existing note. Explicit Draw entries are Control Bar button and focused B; Pitch Lock preference state is declared. | Draw adds notes; clicking an existing note in Draw Mode deletes it. Outside Draw Mode double-click adds or deletes respectively. Pitch-lock preference confines a draw gesture to one pitch; Alt/Option temporarily reverses pitch-lock behavior. With Pitch Lock OFF drawing is melodic and Alt Win/Option Mac temporarily enables pitch lock. Melodic overdraw erases an existing note; pitch-locked backtracking erases drawn notes. Focused Options/context labels state Draw Mode (Pitch Lock On/Off). | D12/E2; target U |
| REQ-MIDI-EDIT-003 | Selection and insertion | Click empty editor, drag a time span, click a note, Shift-click another note, or press Escape. | Empty click sets insert marker; dragging selects time and contained notes; Enter toggles time/note selection; Shift-click adds/removes a note; Escape deselects. Invert Selection swaps a proper subset with its complement. | D12/E3; target U |
| REQ-MIDI-EDIT-004 | Find and select | Enable Find and Select Notes and change Pitch, Time, Chance, Condition, Count, Duration, Scale or Velocity filter parameters. | Matching notes are selected as parameters change; Invert selects nonmatches; Select reapplies current criteria. Pitch matches across octaves. Clicking editor deactivates applied filters and deselects notes. Combining-filter Boolean rules and range inclusivity U. | D12/E4; target U |
| REQ-MIDI-EDIT-005 | Grid snapping | Drag selected note or resize edge with grid on; toggle grid off or use the temporary grid modifier. Exact grid entry controls include Grid Settings button, Options Snap to Grid and Ctrl4 Win/Cmd4 Mac. | Movement is initially free until a grid/offset point, then snaps; original grid offset can be retained. Modifier temporarily reverses grid-enabled state. Snap thresholds, ties and zoom-dependent grid choice U. | D12/E5; target U |
| REQ-MIDI-EDIT-006 | Move, copy and overlap | Select notes, drag or use arrows; paste clipboard notes at insert marker; place a same-pitch new note over an old note. Copy-drag uses Ctrl Win/Option Mac, including introducing the modifier after a drag starts. | Horizontal movement changes time; vertical movement changes pitch. Paste begins at insert marker. A new note overlapping the old note start replaces the old note; overlap limited to the old note end shortens the old note. Exact touching-edge and expression collision results U. The admitted modifier drag makes copies at the destination; exact identities and collisions U. | D12/E6; target U |
| REQ-MIDI-EDIT-007 | Resize and duration | Drag note edge or use Shift+left/right; choose Duration then Set Length in utilities. | Edge and keyboard changes follow grid unless bypassed. Set Length applies chosen duration to selected notes, or all clip notes if none selected. Fit to Time Range fits selected note starts/ends to selected range. Minimum duration and edge reversal U. | D12/E7; target U |
| REQ-MIDI-EDIT-008 | Proportional stretch | Select multiple notes or time; drag a Note Stretch marker. | Selected material scales proportionally; crossing the other marker mirrors note order. Interior pseudo marker stretches/compresses within fixed boundaries without changing outside material. Linked clip envelope timing follows stretch; unlinked envelope timing does not. Exact envelope curve resampling U. | D12/E8; target U |
| REQ-MIDI-EDIT-009 | Deactivate and undo | Select notes and invoke Deactivate or 0, then 0 again. Edit notes imported from a MIDI file and invoke Undo. Deactivate Note(s) entries include Edit menu, piano-ruler context and MIDI Note Editor context. | Deactivated notes are muted/grayed; second toggle reactivates. Undo permits return to prior clip state. Editing imported MIDI leaves original file bytes unchanged. Undo grouping for gestures and persistence of history U. | D12/E9; target U |
| REQ-MIDI-EDIT-010 | Split, chop and join | Use Split on an intersected note, Chop Note(s) on Grid on selected notes, or Join on same-pitch selected notes. | Split divides into two; command without note selection requires a note intersecting insert marker/spanning time selection. Chop divides according to current grid. Join creates one note per selected pitch and joins MPE envelopes with notes. Conflicting values/gaps/overlap expression interpolation U. | D12/E10; target U |
| REQ-MIDI-EDIT-011 | Pitch utilities | Transpose selection; use Fit to Scale with active clip scale; use Invert or Add Interval. | Transpose uses semitones or active scale degrees; octave shortcut transposes by octaves. Fit to Scale moves to nearest scale pitch, with equal-distance ties downward, and is disabled without active scale. Invert flips pitch ordering. Interval slider immediately adds selected-note intervals; with no selection Add Interval applies to all notes. | D12/E11; target U |
| REQ-MIDI-EDIT-012 | Time utilities | Use Stretch factor, double/halve, Humanize, Reverse or Legato in Pitch and Time Utilities. | Stretch factor changes note duration without changing loop length; double/halve scales targeted note duration, time selection or loop by two. Humanize shifts starts within a quarter-grid division either direction at maximum amount. Reverse flips note-time order; Legato ends notes at next start, final note at loop end. Precise random law and reverse pivot U. | D12/E12; target U |
| REQ-MIDI-EDIT-013 | Velocity edit and draw | Edit selected velocity marker by drag or numeric entry; draw in velocity lane. | Numeric entry plus Enter sets selected value. Drawing affects notes in traversed grid division, restricted to selected notes if a selection exists. Without selection drawing can affect all notes there. Ramp assigns first/last values and evenly distributes intervening note velocities. Clipping/rounding and same-time ramp tie order U. | D12/E13; target U |
| REQ-MIDI-EDIT-014 | Velocity randomization and deviation | Invoke Randomize with selected notes or none; set Velocity Deviation on a note. Randomize can target selected notes or selected markers; validating a typed Randomization Amount with Enter is a separate entry. | Randomize changes selected velocities or all notes if none selected, within the stated amount relative to originals. Deviation is a playback-time range; velocity 60 with +20 yields values in 60..80. Double-click a deviated marker resets deviation to zero. Random distribution/seed/repeatability U. Validating the typed amount with Enter triggers randomization; no guaranteed changed realization follows. | D12/E14; target U |
| REQ-MIDI-EDIT-015 | Chance editing | Show Chance lane; edit marker by drag or typed numeric value and Enter; use randomize amount. | Chance lies in documented 0..100 percent range. Probability 50 with randomize amount 25 yields 25..75 percent. With no note selection, changing amount alone does not apply; Enter or Randomize applies to all. With selection parameter change applies immediately. RNG law and out-of-range text handling U. | D12/E15; target U |
| REQ-MIDI-EDIT-016 | Probability groups | Select notes and create Play All or Play One group; remove a member with Ungroup or add it to another group. | One shared probability marker replaces individual markers: diamond for Play All, triangle for Play One. All group notes share trigger decision in Play All; Play One chooses at most one group note per decision, selected randomly when triggered. Adding to a new group removes original membership. Ungroup restores individual markers. Cross-time decision scheduling U. | D12/E16; target U |
| REQ-MIDI-EDIT-017 | Fold and scale display | Enable Fold to Notes, or enable scale and Fold to Scale. | Fold to Notes hides unused pitches. Fold to Scale hides out-of-scale rows except those containing notes. Drum Rack without Fold to Notes displays populated-device pad rows. Folding applies globally across clips; it changes visible rows, not note deletion. Scale highlighting is global. | D12/E17; target U |
| REQ-MIDI-EDIT-018 | Crop and time commands | Crop Clip with loop brace; Crop to Time Selection; use Duplicate Time, Delete Time or Insert Time. | Crop deletes MIDI outside loop/time selection and creates no new file. Duplicate Time inserts copied selected time and notes; Delete Time closes selected gap; Insert Time inserts selected-length silence before selection. These time commands do not change clip start/end or loop-brace settings. Notes crossing crop/cut boundaries U. | D12/E18; target U |
| REQ-MIDI-EDIT-019 | Loop duplication | Select loop brace and Duplicate. | Double loop length, duplicate original loop notes, zoom out as needed, and shift later notes so their distance from loop end is retained. MIDI clips loop by default; disabling loop grays brace. Crossing-edge notes U. | D12/E19; target U |
| REQ-MIDI-EDIT-020 | Multi-clip focus | Select multiple MIDI clips; enable Focus Mode; select a foreground clip by note or loop bar. | Focus limits editing to foreground clip; others remain visible/inactive. Without Focus, note editing may span selected clips. Velocity/Chance lanes always target one foreground clip. Focus ignores loop-bar multiselection. Notes display clip colors when active, gray when inactive. | D12/E20; target U |
| REQ-MIDI-EDIT-021 | Session and Arrangement multi-clip limits | Select Session MIDI clips or Arrangement time selection across MIDI tracks. | Session displays up to eight MIDI clips, all looped, ordered by track then scene; repeats loops until realignment. Arrangement displays MIDI clips from up to eight tracks, ordered by track/time, allows drawing across clip boundaries except in Focus, and fits first-to-last clip range. Excess/unlooped-selection fallback U. | D12/E21; target U |
| REQ-MIDI-EDIT-022 | Preview and follow | Instrument present; enable Preview and add/move note. Enable Follow during playback then edit. | Preview auditions corresponding pitch; Preview switch state is shared across MIDI tracks. Follow pauses for editor edits and resumes upon Follow activation or transport restart. Preview note-off lifecycle and exact output/onset U. | D12/E22; target U |
| REQ-MIDI-EDIT-023 | Tool target and application | Open Transform/Generate, select tool; choose time/note selection or none. | Transform replaces transformed input notes, targeting time selection, note selection or loop if none; priority when both coexist U. Generator targets time selection or loop. Generator treatment of existing material remains U because source statements differ (C1). Record time/note/loop selection separately; occupied-generator treatment and combined-selection precedence stay U. | D12/T1; target U |
| REQ-MIDI-EDIT-024 | Auto Apply and deferred Apply | Auto Apply initially enabled; adjust valid tool settings; disable Auto Apply; edit settings; press Apply. | Enabled adjustments immediately transform/generate notes; disabling restores original notes; with disabled state settings changes wait for Apply. Ctrl/Cmd+Enter also applies current tool. Meaning of original after switching selection/tool and commit boundaries U. Apply has literal Ctrl+Enter Windows / Cmd+Enter macOS entries; the documented initially enabled state does not establish an arbitrary saved/default history. | D12/T1; target U |
| REQ-MIDI-EDIT-025 | Tool undo, redo and reset | Apply a tool; use Undo/Redo; change tool parameters then Reset. | Undo/Redo changes MIDI note results, not parameter values. Reset affects selected-tool parameters, not notes, and is disabled when defaults restored. Exact defaults and undo granularity U. Reset is grayed out/disabled after selected-tool defaults are restored; its parameter-only scope is distinct from note Undo/Redo. | D12/T1; target U |
| REQ-MIDI-EDIT-026 | Scale-aware tools and Max availability | Enable clip scale and use pitch-related tool parameter; select bundled Max tools. | Pitch parameters use scale degrees instead of semitones when scale active. Velocity Shaper and Euclidean are documented bundled Max tools in Standard/Suite; third-party discovery accepts AMXD under dedicated library tool directories or browser Places. Max load/failure/authorization/editor ABI U. Use the Browser MIDI Tools group or MIDI Tool Content tag. Bundled Velocity Shaper/Euclidean Standard/Suite availability is distinct from Suite or Standard plus Max for Live add-on prerequisites for editing/building tools and third-party tools. | D12/T2; target U |
| REQ-MIDI-EDIT-027 | Arpeggiate | Selected chord; configure Style, Distance, Steps, Rate and Gate. | Split selected notes into a sequence using one of 18 styles. Distance controls transposed-step interval in semitones/scale degrees, Steps count, Rate spacing, Gate duration. Gate below 100 percent shortens, above 100 lengthens. Exact styles, retriggering, clipping and random modes U. Expose Style chooser, Distance, Steps, Rate and Gate as separate controls; scale state qualifies Distance units. | D12/T3; target U |
| REQ-MIDI-EDIT-028 | Chop tool | Select note(s); choose Parts 2..64, Gaps, pattern/emphasis, Stretch Chunks and Variation. | Divide notes into selected parts; positive Gaps inserts a gap after that many notes, negative Gaps sets gaps after each note. Pattern has at most 16 parts and repeats above 16. Manual gap edits replace Gaps display with dash; changing Gaps replaces manual pattern. Emphasis stretches chunks by 2..8. Exact variation law U. Positive Gaps replaces a pattern-note position after that many notes; it does not assert timeline insertion. Emphasis toggles qualify Stretch Chunks and gray corresponding pattern positions; Variation is a separate control. | D12/T4; target U |
| REQ-MIDI-EDIT-029 | Connect | Select notes separated in time; set Spread, Density, Rate and Tie. | Insert notes into gaps; Spread bounds randomized pitch shift relative to original pitches; Density specifies filled fraction, with 100 percent filling gaps; Rate controls inserted lengths and Tie extension chance to next original. Precise randomness, polyphonic pairing and endpoints U. Spread, Density, Rate and Tie are independently settable controls on a productive gap-insertion target. | D12/T5; target U |
| REQ-MIDI-EDIT-030 | Glissando | At least two selected successive notes; set Start percent and Curve. | Tie pitches by per-note pitch-bend curve; Start controls bend start relative to note length; Curve controls shape. Bend visible in MPE editor. With fewer than two notes no glissando can be created; exact UI rejection/no-op U. Bend mapping/range clipping U. Start/Curve can be edited directly or by dragging the tool display yellow breakpoint horizontally and connecting line vertically. These tool-display gestures are distinct from generic MPE lane editing; C3 remains U. | D12/T6; target U |
| REQ-MIDI-EDIT-031 | LFO tool | Selected notes; select Pitch Bend, Slide or Pressure; choose Sine/Square/Triangle/Random, Rate, envelope and amount. | Write selected expression using oscillator. Rate 1 corresponds to 4 beats; range 1..1/128. Attack 100 percent resets Decay to 0. Bend Amount spans twice clip bend range and base spans that range; Slide/Pressure controls allow -127..127. Curve visibility C3 and exact waveform/sampling/random law U. Offer separate expression targets, shape/Shape/Reseed, Rate/Time Shift, Amount/Base and Attack/Decay controls. Display/optional-lane claims retain C3. | D12/T7; target U |
| REQ-MIDI-EDIT-032 | Ornament | Select notes; choose Flam or Grace Notes; set Position, Velocity and grace pitch/count/chance. | Flam adds one initial note; Position sign replaces beginning or prepends, magnitude uses grid fraction. Grace adds equal-duration notes filling grid fraction; alternating notes shift up/down semitone or scale degree, or Same keeps pitch. Reapplication adds further ornaments. Chance/velocity relative to originals; exact rounding/cross-boundary handling U. Flam and Grace Notes have separate toggles and Position/Velocity controls; Grace additionally exposes pitch mode, Chance and Amount. | D12/T8; target U |
| REQ-MIDI-EDIT-033 | Quantize tool | Select notes; set grid/meter, start/end targets and Amount. | Quantize chosen start/end times toward specified divisions, including triplets. End quantization changes length; Amount applies a fraction of movement. Edit-menu Quantize uses tool settings. Exact nearest-line tie law, zero-length prevention and conflicting settings shortcut C2 U. The tool accepts Current Grid or a specific meter including triplets, start/end/both targets, and Edit > Quantize Settings opens its panel; C2 shortcut context remains U. | D12/T9; target U |
| REQ-MIDI-EDIT-034 | Recombine | Select notes; choose Position/Pitch/Duration/Velocity; enable Shuffle/Mirror and nonzero Rotate. | Permute chosen values among notes in order Shuffle then Mirror then Rotate. Without Rotate on Grid, steps span up to note count minus one in either direction. Grid rotation uses grid-cell count. Shuffle generates new permutation per Apply, with no guarantee of difference. Simultaneous-note ordering U. Rotate supports value dragging and step buttons, signed directions and Rotate on Grid; each Position/Pitch/Duration/Velocity column has its own controls. | D12/T10; target U |
| REQ-MIDI-EDIT-035 | Span | Select successive notes; choose Legato, Tenuto or Staccato with Offset/Variation. | Legato ends notes at next start and final note at time-selection end or loop end. Tenuto preserves length with zero controls. Staccato uses half minimum inter-start distance. Positive Offset lengthens and negative shortens up to grid step; positive Variation shortens randomly, negative lengthens. Coincident/single-note minimum U. Offset/Variation and Apply are actual controls in all three Span modes, with final-note time-selection versus loop context explicit. | D12/T11; target U |
| REQ-MIDI-EDIT-036 | Strum | Select chord; set Strum Low, High and Tension. | Adjust note starts by pitch-position curve. Low/High at ±100 percent offset lowest/highest by up to one grid step respectively; zero Tension distributes offsets evenly; zero Low and High has no effect. Exact nonlinear curve and chord grouping U. At least one nonzero Low/High value is required for a productive Strum comparison. Direct values and display breakpoints can edit Low/High/Tension. | D12/T12; target U |
| REQ-MIDI-EDIT-037 | Time Warp tool | Select notes/time range; enable one to three speed breakpoints; set time/speed and toggles. | Map speed curve over selection; Quantize snaps warped notes according to grid. Preserve Time Range keeps results within original range. Include Note End accounts for note ends in transformation and may change duration. Integration/interpolation and zero-speed domains U. Breakpoint enable toggles and display drags edit Time/Speed, with selected-breakpoint feedback; Quantize, Preserve Time Range and Include Note End are separate controls. | D12/T13; target U |
| REQ-MIDI-EDIT-038 | Velocity Shaper | Working Max tool; select notes, edit envelope, minimum/maximum, Loop, Rotate and Division. | Shape note velocities with breakpoint envelope bounded by chosen minimum/maximum. Loop sets envelope repetition count; Rotate shifts by Division steps (Rotate 1 at Grid shifts one grid step right). Exact sample/interpolation and equal-time ordering U. Envelope points can be added/dragged; Loop is independently settable, distinct from Rotate/Division. | D12/T14; target U |
| REQ-MIDI-EDIT-039 | Rhythm | Choose pitch/pad, Steps up to 16, pattern, Density, duration, Split, Shift and accents. | Repeat pattern through selected time. Density note-count maximum equals Steps; Step Duration determines repetitions. Shift moves by steps; Split probabilistically halves step. Accent Frequency 1 accents every note. Exact pattern enumeration/random splitting U. Pitch/pad and Alt/Option piano entry, signed Shift, Split and Accent controls complement Steps/Pattern/Duration; layering after deselection remains C1 context. | D12/T15; target U |
| REQ-MIDI-EDIT-040 | Seed | Choose pitch/duration/velocity ranges plus Voices and Density. | Random notes stay in selected ranges; equal pitch handles yield one pitch. Duration chooser spans 1/128 note..whole note; velocity 1..127. Voices bounds simultaneous notes; Density controls population relative to pitch range. Distribution/seed and exact density-to-count U. Pitch/duration/velocity ranges have handles; pitch handles merge to a single pitch and can separate by click/different Min/Max. Alt/Option piano entry is explicit. | D12/T16; target U |
| REQ-MIDI-EDIT-041 | Shape | Choose/draw pitch shape, pitch bounds, Rate, Tie, Density and Jitter. | Generate pitches along shape in bounds. Rate sets minimum length; Tie can extend to next note. Jitter 0 follows shape, larger Jitter departs randomly but remains within pitch bounds. Shape sampling/pitch rounding and distribution U. Shape presets/drawing, Alt/Option range entry, Rate/Tie/Density and Jitter are explicit controls. | D12/T17; target U |
| REQ-MIDI-EDIT-042 | Stacks | Choose chord(s), root, inversion, duration and offset in selected scale. | Fill time selection or loop with chords; add/remove progression chords. Clip scale initializes root and restricts root choices to scale pitches. Duration/offset use eighths of original chord length; controls refer to selected chord. Custom .stacks bank from browser Places replaces default. Chord tables, malformed-bank response and exact voice-leading U. Chord pad click/drag and Ctrl/Cmd Up/Down select chords with Status Bar feedback. Root/piano/arrows, Add/Delete Chord and selected-chord settings are explicit; owned .stacks entry uses Places double-click and Stacks tag context. | D12/T18; target U |
| REQ-MIDI-EDIT-043 | Euclidean | Working Max generator; enable up to four voices and set pitch, velocity, rotation, steps, density, division. | Generate within selection/loop. Each voice has enable, pitch, velocity and rotation; disabled voices contribute no notes. Division controls step length; shorter patterns repeat/wrap; Density controls repetitions and wraps if needed. Rotation randomization changes voice offsets; exact Euclidean pattern algorithm U. Pattern and Voices tabs expose per-voice enable/rotation/randomize, pitch/velocity and all-pitch arrows; Steps/Density/Division retain their separate roles. | D12/T19; target U |

## Acceptance cases

[Current R4 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/acceptance-cases-r4.json)
contain93records:77D12 documentary proposals and16U cases. All72R3 records
remain verbatim, including twelve gesture histories and the seventeen old tool
actions. MED073–093 add bounded Tools controls/gestures. Three new named-control
documentary comparisons are nonnull and eighteen are null; all new legacy
expected/comparator pairs are null. All actual outcomes remain null/U/unexecuted.

Existing finite FitScale, Stretch/Humanize, Span and Seed documentary examples
remain exact old records; no numeric law is newly adopted here. MED020 performs
foreground Velocity and MED072 adds Chance. MED086 supplies the productive
nonzero Strum history absent from historical zero-only MED036. Generator bounds/
capacity/origin/absence probes require actual NONEMPTY output, not Density flags;
empty initial generator targets remain allowed. C1/C2/C3 and implicit-loop/input
context remain unknown. No fixture or original tool action is supplied or run.

## Historical R2 Interval acceptance contexts and Q053

The detailed retained Intervals paragraph explicitly distinguishes an existing
note selection, where changing Interval Size adds and selects notes without a
separate Add Interval press, from no selection, where the slider only sets the
interval and the button applies it to all existing clip notes. This is already
owned by unchanged REQ-MIDI-EDIT-011. MED-011 only exercises Fit to Scale; the
three appended scenarios supply actual future actions for these distinct branches.
The no-selection slider-alone trial first needs a genuinely productive matched
button-addition baseline on a known original nonempty clip, then a separate reset
and verified no-selection state. Unsupported controls, accidental selection or
failed positives remain U, never a successful no-addition result. “Immediately”
specifies the separate-button distinction here, not a wall-clock deadline.

[Source context](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/source-context-r2.json)
retains exact source/query pointers. [Q053](../questions.md#q-053-midi-utility-gesture-and-humanize-source-contexts)
still retains Humanize half-grid versus quarter-grid before/after wording without
choosing total-span equivalence, RNG or a new displacement law. Original C1/C2/C3,
all old expectations and the nonblocking R1 generator/Chop notes remain open.
This case increment is not whole-tool, source-topic or target compatibility.
**AS-OF AUTHOR FREEZE:** R2 independent review is pending; the [spec index](index.md)
owns current disposition. Original payloads and [exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/delta-r2.json)
are preserved. No source example or original tool was executed.

## State, persistence and lifecycle

Note selection, time selection, insert marker, foreground clip, focus, visible
lanes, clip data, tool parameters and preview/transport state are distinct.
Focus Mode restriction and foreground-only velocity/chance access apply before
cross-clip editing. Tool undo changes notes, while parameter Reset and note undo
have distinct documented scopes. Auto Apply disabling has the finite restore
clause in REQ-024; it is not a general promise of atomic cancellation.

General Undo permits returning to previous clip state, but per-drag history,
redo invalidation, clip deletion, save persistence and teardown are U. Timing
laws in storage do not settle editor snapping or engine update boundaries.
A graphical note edit does not prove which note-off is sent for a sounding note.
Malformed file handling routes to storage/container owners; malformed editor or
tool input, missing Max dependencies, cancellation and resource failures remain
ungraded on this page. No background task, cache or host architecture is specified.

## Contradictions and incomplete behavior

These current-manual conflicts are retained rather than silently choosing a law.
They feed [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

| ID | Exact evidence conflict | Consequence |
| --- | --- | --- |
| C1 | T1 chapter introduction says existing clip/selection notes are replaced; `using-midi-tools` says additions coexist if nonoverlapping and replace if overlapping. | REQ-023 leaves occupied-generator-target semantics U; MED-050. No pitch/time overlap predicate is inferred. |
| C2 | T9 describes Ctrl/Cmd+Shift+U as applying without opening panel; E23 describes it as opening settings. | No settings-shortcut behavior specified; MED-051. Explicit Quantize menu/tool application remains distinct. |
| C3 | T7 says Pitch Bend modulation is displayed in MIDI Note Editor, then says modulation appears only in MPE Editor and is invisible in Notes view. | Notes-view LFO visibility U; MED-052. Generated expression versus display remains distinct. |

Partiality also includes initial/default clip/note/tool values; all find-filter
combination/order/boundary laws; exact snap thresholds and offset priority;
minimum lengths and pitch/time clipping; expression transformations, same-time
ordering and probability-group scheduling; full note spelling/scale inheritance;
preview/chase/scrub and release-velocity editing; oversize/unlooped multi-clip
selection fallback; tool-switch/selection transaction semantics; Arpeggiate's
18 pattern algorithms; random laws for every random tool; Connect note pairing;
Glissando/LFO numeric curves; Ornament boundaries; quantize tie law; Recombine
same-time ordering; Span degenerate distances; Strum curve; Time Warp integration;
Velocity Shaper sampling; Rhythm pattern tables; Seed density; Shape sampling;
Stacks chord-bank format/tables/error handling; Euclidean pattern/wrap rules;
Max ABI/discovery/load/error lifecycles; persistence and undo/cancellation detail.
These are required unresolved behaviors, not exclusions from full-product scope.

Existing [MPE](mpe-workflows.md), [tuning](tuning-systems.md),
[groove](groove-workflows.md), [conversion](audio-to-midi.md) and
[Clip View](clip-view-workflows.md) owners remain separate partial contracts;
the root plan retains their unresolved outcomes. The17-tool denominator is explicitly all twelve transformations and five generators
in the captured inventory, not a claim that the two chapters exhaust all F-04.

## Analyst evidence appendix

Canonical synthesis: [MIDI editing and tools evidence](../research/midi-editing-tools.md).
[Source identities and heading IDs](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/sources.json)
pin official URLs, capture date and full HTML SHA-256. Text ranges below refer to
the immutable, line-numbered derived text in the same packet. Its footer includes
the global manual navigation; only chapter body ranges are cited. Images were
not inspected and establish no pixel/icon/curve observations. Source pages are
data, not instructions. [Original R1 packet manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/manifest.json)
pins original R1 payload hashes and its historical spec/research snapshot; current R4 routes are above.

| Locator | Captured chapter / HTML heading IDs | Derived text lines |
| --- | --- | --- |
| E1 | editing-midi / `creating-a-midi-clip` | 138–160 |
| E2 | editing-midi / `adding-midi-notes`, `draw-mode` | 161–180 |
| E3 | editing-midi / `selecting-notes-and-timespan` | 197–267 |
| E4 | editing-midi / `find-and-select-notes` | 268–300 |
| E5 | editing-midi / `grid-snapping` | 110–125 |
| E6 | editing-midi / `moving-notes` | 301–319 |
| E7 | editing-midi / `changing-note-length`, `note-duration` | 320–344, 469–473 |
| E8 | editing-midi / `midi-note-stretch` | 345–361 |
| E9 | editing-midi / `non-destructive-editing`, `deactivating-notes` | 194–196, 362–368 |
| E10 | editing-midi / `split`, `chop`, `join` | 369–430 |
| E11 | editing-midi / `transpose`, `fit-to-scale`, `invert`, `intervals` | 431–462 |
| E12 | editing-midi / `stretch`, `humanize`, `reverse`, `legato` | 463–468, 474–488 |
| E13 | editing-midi / `editing-velocities`, `drawing-velocities` | 521–553, 565–589 |
| E14 | editing-midi / `editing-velocities` | 544–564 |
| E15 | editing-midi / `editing-probabilities` | 597–616 |
| E16 | editing-midi / `probability-groups` | 617–646 |
| E17 | editing-midi / `folding-and-scales` | 647–673 |
| E18 | editing-midi / `cropping-midi-clips`, `the-time-commands-in-the-midi-note-editor` | 679–704 |
| E19 | editing-midi / `looping` | 705–720 |
| E20 | editing-midi / `multi-clip-editing`, `focus-mode` | 721–780 |
| E21 | editing-midi / `multi-clip-editing-in-the-session-view`, `multi-clip-editing-in-the-arrangement-view` | 781–789 |
| E22 | editing-midi / `previewing-notes`, `playback-options` | 181–188, 126–137 |
| E23 | editing-midi / `quantizing-notes` | 495–520 |
| T1 | midi-tools / introduction, `using-midi-tools` | 1–41 |
| T2 | midi-tools / `using-max-for-live-midi-tools` | 42–57 |
| T3 | midi-tools / `arpeggiate` | 61–71 |
| T4 | midi-tools / `chop` | 72–80 |
| T5 | midi-tools / `connect` | 81–88 |
| T6 | midi-tools / `glissando` | 89–99 |
| T7 | midi-tools / `lfo` | 100–114 |
| T8 | midi-tools / `ornament` | 115–131 |
| T9 | midi-tools / `quantize` | 132–148 |
| T10 | midi-tools / `recombine` | 149–160 |
| T11 | midi-tools / `span` | 161–171 |
| T12 | midi-tools / `strum` | 172–180 |
| T13 | midi-tools / `time-warp` | 181–187 |
| T14 | midi-tools / `velocity-shaper` | 188–197 |
| T15 | midi-tools / `rhythm` | 201–218 |
| T16 | midi-tools / `seed` | 219–230 |
| T17 | midi-tools / `shape` | 231–243 |
| T18 | midi-tools / `stacks` | 244–268 |
| T19 | midi-tools / `euclidean` | 269–283 |

The retained schema correlation (23 Algorithm classes: 15 native tool and eight
filter classes) supports **surface/field presence only**. It supplies no S-grade
UI or numerical algorithm clauses. Velocity Shaper/Euclidean Max profiles remain
with the inventory's separately hashed AMXD records; their bytecode was not read
or executed here. Internal fields are retained in analyst research only.

## Revision and handoff

| Revision | Date | Scope |
| --- | --- | --- |
| 1 | 2026-10-19 | 43 partial D12 requirements; all 17 inventoried tools have concrete independent clauses; 57 unexecuted acceptance cases; target applicability U throughout. Frozen for separate review, no release or completion claim. |
| 2 | 2026-10-19 | Same43requirement rows,60cases;57oldrecords verbatim plus three Interval selection/button branches. All actual target outcomesU/unexecuted; independent review pending as of author freeze, current status in spec index. |
| 3 | 2026-10-19 | Same43IDs, six source-entry/role refinements and72cases;60old records verbatim plus12gesture/selection proposals. All17tool rows/actions exact; current owner review pending as of author freeze. |
| 4 | 2026-10-19 | Same43IDs;21bounded common/tool control refinements and93cases;72old records exact plus21Tools proposals. All actual outcomesU/unexecuted; review pending as of author freeze. |


## Historical R3 bounded gesture and case increment

The [complete retained Editing MIDI audit](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing-source-audit/README.md)
[passed independent partial source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-editing-source-audit-review.json).
This owner adopts selected subsets of eleven groups, not the full38group ledger.
Current43IDs remain; only001/002/005/006/009/014 add explicit source entries/roles.
All other rows, particularly17individual tool contracts, remain byte-equivalent.
SourceVersion12/date2026-10-19 gives no patch12.4.3 parity; captureUTC remains null.

| New case | Group | Separate actual future action |
| --- | --- | --- |
| MED061 | G03 | Grid entries and admitted nonzero original-offset history |
| MED062 | G06 | Remaining Session menu/Arrangement creation entries |
| MED063 | G07 | Draw button/B, PitchLockOff reversal and erase histories |
| MED064 | G12 | Copy-drag with early versus late modifier |
| MED065 | G15 | Three Deactivate menu contexts with actual reactivation |
| MED066 | G18 | Actual Double/Halve per independently admitted target |
| MED067 | G19 | Reverse selected/no-selection button branches |
| MED068 | G19 | Actual utility Legato button, distinct from Span |
| MED069 | G20 | Humanize Amount then button; output U under Q053 |
| MED070 | G23 | Velocity Randomize targets and typed Amount+Enter |
| MED071 | G24 | Actual Ramp Start/End on distinct-time notes |
| MED072 | G35 | Foreground Chance with FocusOff, distinct from old Velocity |

Use [future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/fixtures-r3.json)
and separate exact-original resets. Negative/erase/exclusion observations require
a genuinely productive matched operation first; empty/unsupported controls, flags
alone or failed positives stayU. Accepted symbolic values are independently
required; saved note domains do not prove UI admission. Pure editor-data actions
need no instrument/hardware. No new numeric/random stream, note/clipboard codec,
held-note delivery, pixel/gesture threshold, target precedence or timing law.
Reverse ordering does not supply a pivot/coordinate formula; Legato, Double/Halve
and random outputs keep new documentary numerical comparators null. Ramp grades
only admitted endpoint controls/first-last values, with intermediate samples U.
Chance foreground exclusion requires actual successful edits on each clip before
reset and comparison. Humanize Q053 has no new bound or source equivalence; no
retained private coefficient becomes a public law. C1/C2/C3/Q052 stay open.

[Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/delta-r3.json)
and [consumer history](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/consumer-impact-r3.json)
preserve25old files and exact R2 provider snapshots. Active MIDI Tools audit inputs
remain as-of, not live canonical equality gates. No historical replay/adapter or
blanket old-checker green result follows. Remaining audit groups/facets and all
source-silent lifecycle outcomes remain required open work.
**AS-OF AUTHOR FREEZE:** R3 independent owner review pending; the [spec index](index.md)
owns current status. Source audit approval is not this increment's self-approval.

## R4 bounded MIDI Tools control and action increment

The [complete retained Tools audit](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-tools-source-audit/README.md)
and its [independent partial review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/midi-tools-source-audit-review.json)
support bounded additions to existing023–043;001–022 remain exact current R3.
The [current93-case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/acceptance-cases-r4.json)
retains all72old records, including twelve gesture cases, and adds MED073–093.
There are77D12 documentary proposals and16U; all actual outcomes are null/U/unexecuted.
Only three new named-control documentary comparisons are nonnull; the other18
new documentary comparisons, and all21 new legacy expected/comparator pairs,
are null. Historical numeric documentary examples stay historical and unchanged.

Each of21audit groups contributes a limited control/entry/action subset, not
full algorithm or lifecycle closure. Independent admitted controls, exact resets
and genuinely productive matched effects are mandatory before negatives.
Generators may start empty; actual NONEMPTY output precedes range/capacity/origin/
absence checks, not a nonzero Density flag. MED086 adds nonzero Strum before
reset to zero; old MED036 remains the historical zero-only trial. Editor data
needs no hardware/audio. Max bundled Standard/Suite selection is separate from
Suite or Standard plus Max for Live add-on editing/building/third-party context.
Tool display gestures do not duplicate generic MPE lane editing or settle C3.

C1/C2/C3, MTA-Q04 implicit-loop/input context, selection precedence, built-in editability,
Q052/Q053 and source-silent malformed/cancel/save/undo/transport/teardown/rate
outcomes remain open. Random reapplication need not differ. No new waveform,
curve, arithmetic, RNG, protocol, file, timeline-insertion or timing law is adopted.
[Exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/delta-r4.json),
[guards](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/fixtures-r4.json)
and [historical consumers](../../analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/consumer-impact-r4.json)
preserve old files and as-of providers without automatic historical replay.
**AS-OF AUTHOR FREEZE:** R4 independent owner review pending; the [spec index](index.md)
owns current disposition. No full family or exact-build completion is claimed.
