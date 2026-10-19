---
id: SPEC-CLIP-LAUNCH
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 4
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Clip launch settings and launch quantization

## Scope

Feature FEAT-SESSION, with FEAT-TRANSPORT and FEAT-PERSISTENCE, in the
[feature map](feature-map.md). User task: open a Live Set whose session clips carry
launch settings, see and keep those settings, and launch a clip so that it starts on
the quantization grid. This draft specifies:

- where a set stores each clip's launch mode, launch quantization, legato, velocity
  amount and follow action, and the set's global and record quantization;
- the meaning and labels of every stored value;
- initial values, and what a missing or out-of-range value does on load;
- the corrections applied on load (follow-chance rescaling, follow-time rounding);
- the migration of older documents;
- the quantization grid length for each setting, and the rule that places a launch on
  that grid while the transport plays.

Gate, Toggle and Repeat press and release behavior, Legato, velocity scaling and
follow-action timing are **open**. They are listed as unknown requirements. Each names the
probe that would have settled it and, where one exists, a static route that could still
settle it. Revision 4 settles the launch offset near a grid line, and statically the launch
with the transport stopped, through [SPEC-PLAYBACK-CORE](playback-core.md), which owns the
launch sample.

Every requirement is a **proposed contract** supported by a static derivation from the
12.4.3 program, by shipped bytes, by extracted execution of the shipped x86_64 code, or
explicitly unknown. Nothing was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first
draft. Under [ADR 0003](../decisions/adr-0003-no-reference-execution.md) nothing will
be: no reference observation is available, and no probe will run. Revision 3 adds the X
results of packet X2 for the grid arithmetic, the follow-chance rescaling and the
follow-time rounding (appendix). Revision 4 applies the corrections of
[SPEC-PLAYBACK-CORE](playback-core.md) r1, which settles A1 for the Trigger fire path and
defines the launch sample, the pre-delay and the near-boundary rule. Target: 12.4.3,
documents with `MinorVersion="12.0_12402"` unless a clause says otherwise. The
gzip/XML envelope belongs to the draft
[SPEC-ALS-CONTAINER](als-container.md); value text rules and the time-signature code
come from the draft [SPEC-TRANSPORT-STATE](transport-state.md). All document
examples are fragments of the decoded XML.

Excluded: scene launching and scene follow actions (except their migration in
REQ-014), launching through the Live API (`fire` with an explicit quantization,
`set_fire_button_state`), controller and Push launching, recording and the effect of
record quantization, the key and MIDI mapping of the global quantization
(`GlobalQuantisationKeyMidi`), Arrangement override and "back to arrangement",
sample analysis files, the Looper device's own quantization, undo, edits after load
other than the API setters in REQ-011, and the exact text of error messages.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in shipped bytes: the schema files or the Live Sets and clips in the 12.4.3 bundle. These were written by Live 12.4d1 or 12.1d1, not by a 12.4.3 save |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run. An assumption is named beside the clause (A1–A7 below) |
| X | Extracted execution: the shipped x86_64 function was run on the stated inputs in the harness of [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code). It shows what the function computes, not that Live calls it with those inputs; the path and any assumption are stated beside the clause. The arm64 release slice is matched by static comparison (appendix) |
| U | Unknown; no expected result, or only a static expectation that must not be graded. A PRB ID names the Phase 4 probe that would have settled it; under ADR 0003 no probe will run, so no reference observation is available. A static route, where named, is a static reading that could still settle it |

Only D, S and X clauses may enter a release. U clauses block the behavior they name.
"The set does not open" means the document reader stops with a read error, as in
SPEC-TRANSPORT-STATE.

## Assumptions

Each assumption is supported by the evidence but not established. If one fails, the
clauses that name it become unknown. No reference observation will test them
(ADR 0003).

| ID | Assumption | What rests on it |
| --- | --- | --- |
| A1 | **Settled in revision 4 (S)** for the Trigger fire path by [REQ-PLAYBACK-CORE-007](playback-core.md#req-playback-core-007--launch-request-and-grid-settles-spec-clip-launch-a1). A press on a session clip's launch button, and `ClipSlot.fire()` without arguments, reaches the launch-time computation without an explicit target time. The slot-state test means "the slot holds a clip"; the program then uses the clip's own grid when its launch quantization is not Global, and the set's global quantization otherwise. That the engine's global value equals the loaded `GlobalQuantisation` remains an assumption there (its A4), as does which other gestures take this path | REQ-016, REQ-017, REQ-018 |
| A2 | A clip and its follow-action compound read from a document start with the initial values of REQ-009 and REQ-010 and then receive only the members present in the document. A present value inside its stated range is kept as read: the values of REQ-004, REQ-005 and REQ-007 for launch mode, launch quantization and follow actions; the bounds of REQ-009 for velocity amount, loop iterations, chances and jump indices; 0 to below 1,000,000 for follow time. A present launch mode, launch quantization or follow action outside its values is accepted without a range check. Revision 3 (S, both slices): the member's own load step does not limit a value outside its bounds either. The loader stores the value directly, and the post-load hook of the UserFloat and RangedRemoteableInt classes is the generic one, which does not clamp; the RemoteableDouble hook only rounds (REQ-013). A later step that could change such a value is still untraced, except for the chances (REQ-012) | REQ-009 to REQ-013 |
| A3 | The load-time corrections of REQ-012 and REQ-013 run for every clip read from a Live Set | REQ-012, REQ-013 |
| A4 | In a set whose time signature never changes, the grid is anchored at song beat 0 | REQ-017 and the grid cases |
| A5 | Opening a document whose `MinorVersion` has translator number c applies, in increasing order and before the values are loaded, every migration step numbered above c | REQ-014 |
| A6 | Each value label below is the text the user interface shows for that value | Display comparators in the cases |
| A7 | **Settled in revision 3 (X, setter path S).** The rescaling of REQ-012 writes each chance through the chance setter. That setter limits the value to 0–100 and stores it; it does not call the follow-action chance controller. A value inside 0–100 is therefore kept as computed | REQ-012 |

## Requirements

### REQ-CLIP-LAUNCH-001 — clip launch fields: location, types and order

- **D.** Every `AudioClip` and `MidiClip` element carries the launch fields as direct
  children: `LaunchMode/@Value` (integer), `LaunchQuantisation/@Value` (integer),
  `Legato/@Value` (Boolean), `VelocityAmount/@Value` (32-bit float) and the compound
  `FollowAction` (REQ-002). They occur in this order among the clip's children:
  … `Color`, `LaunchMode`, `LaunchQuantisation`, `TimeSignature`, `Envelopes`,
  `ScrollerTimePreserver`, `TimeSelection`, `Legato`, `Ram`, `GrooveSettings`,
  `Disabled`, `VelocityAmount`, `FollowAction`, `Grid` … No other element class in the
  current schema declares `LaunchMode` or `LaunchQuantisation`.
- **D.** Clip elements occur, among other places, at:
  - session slots: `/Ableton/LiveSet/Tracks/{MidiTrack|AudioTrack}/DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/{MidiClip|AudioClip}`;
  - arrangement: `…/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip` and
    `…/MainSequencer/Sample/ArrangerAutomation/Events/AudioClip`;
  - take lanes: `/Ableton/LiveSet/Tracks/MidiTrack/TakeLanes/TakeLanes/TakeLane/ClipAutomation/Events/MidiClip`;
  - the groove pool: `/Ableton/LiveSet/GroovePool/Grooves/Groove/Clip/Value/MidiClip`.

  Clips outside session slots carry and keep the same fields. Only session clips are
  launched in this scope.
- **D.** The tag names are not unique. `Legato` also names a field of an Analog
  envelope, and `VelocityAmount` a field of a groove. Only the clip-child paths above
  are launch settings.
- **S.** The value text is read with the rules of SPEC-TRANSPORT-STATE:
  REQ-TRANSPORT-STATE-003 for the Boolean, REQ-TRANSPORT-STATE-005 for 32-bit floats
  and REQ-TRANSPORT-STATE-006 for integers. Text those rules refuse makes the set not
  open. Two elements with the same name under one clip make the set not open
  (as in REQ-TRANSPORT-STATE-008).
- **S.** On save, each field is written as an element carrying one `Value`
  attribute, in the order above. A written Boolean, or a written number whose value
  has at most six significant decimal digits, reads back with the rules above as the
  stored value.
- **U.** Whether a written number with more significant digits reads back exactly;
  the number text written on save for these fields (whether REQ-TRANSPORT-STATE-011
  applies), and indentation.

### REQ-CLIP-LAUNCH-002 — follow-action compound

- **D.** `FollowAction` holds exactly these children, in this order: `FollowTime`
  (64-bit float, beats), `IsLinked` (Boolean), `LoopIterations` (integer),
  `FollowActionA`, `FollowActionB` (integers, REQ-007), `FollowChanceA`,
  `FollowChanceB`, `JumpIndexA`, `JumpIndexB` (32-bit floats) and
  `FollowActionEnabled` (Boolean). Each has a `Value` attribute.
- **D.** `Scene` elements carry a compound of the same form. Scene behavior is out of
  scope except for its migration (REQ-014).
- **S.** `FollowTime` text follows REQ-TRANSPORT-STATE-004.
- **D.** In shipped 12.4d1 content `FollowActionEnabled` does not follow from the
  other children: 4,101 of 4,130 clips have A = Next with chance 100 and are disabled.

### REQ-CLIP-LAUNCH-003 — set quantization fields

- **D.** `/Ableton/LiveSet/GlobalQuantisation/@Value` (integer, REQ-005) holds the global
  launch quantization and `/Ableton/LiveSet/AutoQuantisation/@Value` (integer,
  REQ-006) the record quantization. `GlobalQuantisationKeyMidi` lies between them
  (excluded).
- **S.** Both follow the integer text rules of REQ-TRANSPORT-STATE-006.

### REQ-CLIP-LAUNCH-004 — launch mode values

- **S.** `LaunchMode`: 0 Trigger, 1 Gate, 2 Toggle, 3 Repeat. The Live API names the
  same values `trigger`, `gate`, `toggle`, `repeat`, and the clip property
  `launch_mode` returns the stored value.

### REQ-CLIP-LAUNCH-005 — launch quantization values

- **S.** Clip `LaunchQuantisation` and set `GlobalQuantisation` use these values:

| Clip value | Global value | Label | Clip API name | Global API name |
| --- | --- | --- | --- | --- |
| 0 | — | Global | `q_global` | — |
| 1 | 0 | None | `q_none` | `q_no_q` |
| 2 | 1 | 8 Bars | `q_8_bars` | `q_8_bars` |
| 3 | 2 | 4 Bars | `q_4_bars` | `q_4_bars` |
| 4 | 3 | 2 Bars | `q_2_bars` | `q_2_bars` |
| 5 | 4 | 1 Bar | `q_bar` | `q_bar` |
| 6 | 5 | 1/2 | `q_half` | `q_half` |
| 7 | 6 | 1/2T | `q_half_triplet` | `q_half_triplet` |
| 8 | 7 | 1/4 | `q_quarter` | `q_quarter` |
| 9 | 8 | 1/4T | `q_quarter_triplet` | `q_quarter_triplet` |
| 10 | 9 | 1/8 | `q_eighth` | `q_eight` |
| 11 | 10 | 1/8T | `q_eighth_triplet` | `q_eight_triplet` |
| 12 | 11 | 1/16 | `q_sixteenth` | `q_sixtenth` |
| 13 | 12 | 1/16T | `q_sixteenth_triplet` | `q_sixtenth_triplet` |
| 14 | 13 | 1/32 | `q_thirtysecond` | `q_thirtytwoth` |

- **S.** Clip value k ≥ 1 denotes the same setting as global value k − 1, with the
  same label; clip value 0 (Global) denotes the set's global setting. Which setting a
  launch uses is REQ-016. The API spellings are as shown, including
  `q_eight`, `q_sixtenth` and `q_thirtytwoth`. The clip property
  `launch_quantization` returns the stored clip value; the song property is
  `clip_trigger_quantization`.

### REQ-CLIP-LAUNCH-006 — record quantization values

- **S.** `AutoQuantisation`: 0 None, 1 1/4, 2 1/8, 3 1/8T, 4 1/8 + 1/8T, 5 1/16,
  6 1/16T, 7 1/16 + 1/16T, 8 1/32. API names `rec_q_no_q`, `rec_q_quarter`,
  `rec_q_eight`, `rec_q_eight_triplet`, `rec_q_eight_eight_triplet`, `rec_q_sixtenth`,
  `rec_q_sixtenth_triplet`, `rec_q_sixtenth_sixtenth_triplet`, `rec_q_thirtysecond`;
  song property `midi_recording_quantization`. Its effect on recording is excluded.

### REQ-CLIP-LAUNCH-007 — follow-action values

- **S.** `FollowActionA` and `FollowActionB`: 0 No Action, 1 Stop, 2 Play Again,
  3 Previous, 4 Next, 5 First, 6 Last, 7 Any, 8 Other, 9 Jump. A short label set
  differs only in "Again" for 2.
- **U.** Where each label set is shown.

### REQ-CLIP-LAUNCH-008 — set initial values and missing set fields

- **S.** A set object starts with global quantization 1 Bar (4) and record
  quantization None (0). The shipped default template stores the same values.
- **U.** That a document without `GlobalQuantisation` or `AutoQuantisation` opens
  with these values (static expectation), and what File > New uses. No reference
  observation is available (ADR 0003). Static route for the missing fields: the song
  loader, not read.

### REQ-CLIP-LAUNCH-009 — clip initial values and missing clip fields

- **S.** A clip starts with Legato off and velocity amount 0, with velocity amount
  bounds 0 and 1. Its follow action starts with follow time 4 beats, linked, one loop
  iteration (bounds 1 and 1,073,741,823), A = Next with chance 100, B = No Action with
  chance 0 (chance bounds 0 and 100), jump indices 1 (bounds −1 and 8,388,608) and
  follow actions disabled.
- **S (assumes A2).** A clip element without `Legato`, `VelocityAmount`,
  `FollowAction`, or any child of `FollowAction`, opens with these values for the
  missing items. A later save writes them.
- **D.** Shipped content stores jump index 0 in 605 clips and 994 scenes. **U:**
  which operation writes 0.
- **U.** Whether every clip creation path (empty MIDI clip, recording, dropping a
  sample) keeps these values.

### REQ-CLIP-LAUNCH-010 — launch mode and quantization of a new clip

- **S.** A clip's initial launch mode and launch quantization are the user's
  default launch mode and default launch quantization preferences.
- **S (assumes A2).** A clip element without `LaunchMode` or `LaunchQuantisation`
  opens with those preference values, not with 0.
- **U.** Which Preferences controls these are, their factory values, whether their
  values use the numbering of REQ-004 and REQ-005, and which creation paths keep them.
  No reference observation is available (ADR 0003; PRB-S5-10). Static route: the
  preference object's constructor and registry for the factory values and numbering,
  and the callers of the clip constructor for the creation paths.

### REQ-CLIP-LAUNCH-011 — out-of-range values

- **S (assumes A2).** Any integer that passes REQ-TRANSPORT-STATE-006 in
  `LaunchMode`, `LaunchQuantisation`, `FollowActionA` or `FollowActionB` does not make
  the set fail to open, including values outside REQ-004, REQ-005 and REQ-007.
- **U.** The value then held, displayed or written on save, and the launch timing.
  Static expectations: the value held is the value as read, since the loader stores
  the index directly; timing has no grid (REQ-015). No reference observation is
  available (ADR 0003; PRB-S5-09). Static route for the saved value: the generic
  writer.
- **S (both slices; X for the getter).** The enum value getter returns 0 for a stored −99
  and the stored value otherwise (X: −100, −98, −1, 15 and the 32-bit extremes are
  returned unchanged). A `LaunchQuantisation` of −99 therefore launches as Global
  (REQ-016).
- **U.** Whether an out-of-range `GlobalQuantisation` or `AutoQuantisation` opens.
  Static route: the song loader, not read.
- **S (both slices).** A velocity amount, loop-iteration count, chance or jump index
  outside the bounds of REQ-009, or a follow time below 0 or from 1,000,000, is not
  refused by the text rules or by the member's load step, which keeps it as read (A2,
  revision 3).
- **X (load path S; assumes A3).** Chances outside 0 to 100 are then rescaled by
  REQ-012 and limited by the chance setter: 150 and 50 give 75 and 25; −10 and 50 give
  0 and 100; 150 and −50 give 100 and 0; −10 and −10 give 50 and 50.
- **X (load path S; assumes A3).** A follow time below 0 or from 1,000,000 is rounded
  by REQ-013 and not limited: −0.3, −5 and 2,000,000 are held unchanged. The
  follow-time controller's minimum of 0.25 belongs to controlled changes, not to the
  load (S).
- **U.** Whether the clip's own post-load hook, which was not read, changes or refuses
  such a value. So the value held after load for a velocity amount, loop-iteration count
  or jump index outside its bounds is unknown. Unknown too: what the user interface
  shows for any out-of-range value.
- **S.** Live API: assigning `launch_mode` a value outside 0–3, or
  `launch_quantization` a value outside 0–14, raises an error, and the stored value
  does not change. Values inside the ranges are accepted.
- **U.** The message text of that error and the form in which a script receives it.
  The program builds a message, but the kept evidence does not show how the error
  reaches a script, and message text is outside this scope. Static route: the
  scripting binding's error translation.

### REQ-CLIP-LAUNCH-012 — follow-chance rescaling on load

- **X (path S; assumes A2, A3).** After a clip's follow action is read, with A and B its
  stored chances (32-bit floats):
  - if A = 0 and B = 0 (−0 counts as 0): chance A becomes 100, chance B stays 0, and
    follow actions become disabled;
  - otherwise: chance A becomes round(A ÷ ((A + B) ÷ 100)) and chance B becomes
    100 − chance A. The arithmetic is 32-bit float, and halves round away from zero.
  - Each new chance is then limited to 0 to 100 by the chance setter (A7, settled).
- **X.** Examples: 30/30 → 50/50; 1/2 → 33/67; 1/7 → 13/87; 1/0 → 100/0;
  3/5 → 38/62 and 5/3 → 63/37 (halves); 1/199 → 1/99; 0.25/0.75 → 25/75;
  99.5/0.5 → 100/0. Values outside 0 to 100 are in REQ-011.
- **U.** Whether the rescaling also runs for scene follow actions. It is the
  follow-action correction made after loading, but A3 covers clips only. Static
  route: whether scene loading runs the same post-load step. No case depends on it,
  because the scene chances in the cases are 100 and 0.

### REQ-CLIP-LAUNCH-013 — follow-time rounding on load

- **X (path S; assumes A2, A3).** After load, a clip's `FollowTime` is rounded to
  the grid of 1/3,843,840 beat, halves away from zero, by the binary64 formula of
  REQ-MIDI-NOTE-STORAGE-006: with h the binary64 value of 1/3,843,840 and s = +1 for
  x ≥ 0 (including −0), else −1, the held value is
  s × (⌊|x + s × h/2| × 3,843,840⌋ / 3,843,840). The values ±1.7976931348623155e308,
  the largest finite value and +∞ are not rounded. Examples:
  2.0000001 → 2; 3.0000002 → 11,531,521/3,843,840 (≈ 3.00000026); 1e-8 → 0; −0 → +0.
  3,843,840 = 2⁸·3·5·7·11·13, so every triplet and bar length of REQ-015 is a whole
  multiple.
- **X.** Next to a halfway point the formula, not exact rounding, decides: a value
  one binary64 step below the nearest value to h/2, 1.3007825507825505e-07, is held as
  h, where exact rounding gives 0. Six of the 18 values run within one step of a
  halfway point differ in this way.
- **U.** Whether the rounding runs for scene follow actions (as in REQ-012). Follow
  times outside 0 to below 1,000,000 are in REQ-011.

### REQ-CLIP-LAUNCH-014 — migration of older documents

Applies to documents opened under SPEC-ALS-CONTAINER whose `MinorVersion` names an
older shipped schema.

- **S (assumes A5).** Migration steps, by translator number:

| Number | Effect |
| --- | --- |
| 17 | Old 11-value clip `LaunchQuantisation` k mapped to 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14 for k = 0…10 (the triplet values are inserted); k ≥ 11 or negative is a read error |
| 406 | Clip `FollowTime`, `FollowActionA/B` and `FollowChanceA/B` move into a new clip `FollowAction`; absent values become follow time 1, chance A 1 and chance B 0. A clip that already has `FollowAction` is unknown (below) |
| 417 | If `FollowActionEnabled` is absent: enabled = (A ≠ 0 and chance A ≠ 0) or (B ≠ 0 and chance B ≠ 0), absent values counting as 0 |
| 421 | `IsLinked` = true, and A := Next, when follow actions are disabled, A = 0, B = 0 and follow time = 4 exactly; otherwise `IsLinked` = false |
| 12008 | `LoopIterations` changes declared type only; no value changes |
| 12203 | Scene without `FollowAction`: one is added with follow time 4, 1 iteration, A and B No Action, chances 100/0, disabled, jump indices 1, linked. Scene with one: any `IsLinked` is replaced by (disabled and follow time 4 and A = Next and B = No Action and chances 100/0) |

- **S (assumes A3, A5).** REQ-012 and REQ-013 apply after migration, so chances
  stored as fractions become percentages (1 and 0 → 100/0; 0.25 and 0.75 → 25/75).
- **S.** Other conversion steps also apply to older documents. Of the steps numbered
  above 405, none outside the table changes a launch field, a follow-action member,
  `GlobalQuantisation` or `AutoQuantisation`. The other steps are outside this
  requirement.
- **U.** Whether a step numbered 405 or below, other than 17, changes these items in
  documents older than `11.0_405` (not checked).
- **U.** Step 406 for a clip that already has `FollowAction`. The program reports an
  error and does not return; the kept evidence does not show whether opening refuses
  the document or the application stops. Static route: the error-report routine and
  how the document reader handles it.
- **U.** What a save writes for a scene: the scene writer was not read. Static route:
  reading it.
- **U.** Whether step 17 is reachable. Every opened document names a shipped schema
  (REQ-ALS-CONTAINER-005), and the oldest is `8.1_220`, so under A5 step 17 never runs
  for a Live Set.
- **D.** The shipped default template has `MinorVersion="12.0_12117"`, so step 12203
  applies to it under A5; its scenes already satisfy the linked condition.

### REQ-CLIP-LAUNCH-015 — quantization grid length

Let a global value q and a time signature n/d be given, and bar = 4·n/d beats rounded
to the nearest multiple of 1/3,843,840 beat (the rounding of REQ-013).

- **X.** The grid length in beats is (every one of the 495 signatures n = 1 to 99,
  d = 1, 2, 4, 8, 16, with q = 1 to 13, and q = −99, −2, −1, 0, 14, 15 and 100 on four
  signatures: 6,463 of 6,463 equal):

| q | Setting | Grid (beats) | 4/4 | 3/4 | 6/8 | 7/8 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 Bars | 8·bar | 32 | 24 | 24 | 28 |
| 2 | 4 Bars | 4·bar | 16 | 12 | 12 | 14 |
| 3 | 2 Bars | 2·bar | 8 | 6 | 6 | 7 |
| 4 | 1 Bar | bar | 4 | 3 | 3 | 3.5 |
| 5 | 1/2 | 2 | 2 | 2 | 2 | 2 |
| 6 | 1/2T | 4/3 | | | | |
| 7 | 1/4 | 1 | | | | |
| 8 | 1/4T | 2/3 | | | | |
| 9 | 1/8 | 1/2 | | | | |
| 10 | 1/8T | 1/3 | | | | |
| 11 | 1/16 | 1/4 | | | | |
| 12 | 1/16T | 1/6 | | | | |
| 13 | 1/32 | 1/8 | | | | |
| 0, negative, ≥ 14 | None or out of range | no grid | | | | |

- **X.** Note values (q ≥ 5) do not depend on the signature: 1/2 is 2 beats in 6/8.
  The triplet lengths are the binary64 values nearest 4/3, 2/3, 1/3 and 1/6; they are
  not rounded to the lattice.
- Not proposed for release: a grid length is observable only by launching (REQ-016 to
  018). Revision 4: A1 is settled (REQ-PLAYBACK-CORE-007), so the launch path no longer blocks a
  release; see the release note below.

### REQ-CLIP-LAUNCH-016 — which grid a launch uses

- **S (A1 settled in revision 4).** A clip with launch quantization 0 (Global) uses the set's
  global value with the song's time signature in effect at the press.
- **S (A1 settled in revision 4).** A clip with launch quantization k ≥ 1 uses grid value k − 1
  with the clip's own time signature (`TimeSignature/TimeSignatures/RemoteableTimeSignature`
  `Numerator` and `Denominator`, truncated to integers). Example: a 6/8 clip set to
  1 Bar uses 3 beats in a 4/4 song.
- **S (X for the grid length and the enum getter).** Clip values 1 (None), negative
  values other than −99, and values ≥ 15 give no grid. A stored −99 is read as 0
  (REQ-011), so that clip uses the global value as Global does. Revision 2 stated that
  every negative value gives no grid; −99 is the exception.
- **U.** Which entry is used when a clip has several time-signature entries.

### REQ-CLIP-LAUNCH-017 — launch boundary while playing

With the transport playing, a launch pressed at song beat t, grid g > 0 (REQ-016),
and anchor a:

- **X (A1 settled in revision 4).** The press time t is the transport's current song time rounded to
  the 1/3,843,840 grid as in REQ-013 (an explicit target time is not rounded). Examples:
  3.99 → 3.990000104062604; 4 ± 1e-9 → 4; 4 + 1/3,843,840 stays.
- **X (A1 settled in revision 4).** The launch boundary is B = a + ⌈(t − a)/g⌉·g, rounded to the
  1/3,843,840 grid, with a = max(0, the anchor) and every operation in binary64 with
  g the binary64 grid length of REQ-015. For bar grids and the note values 2, 1, 1/2,
  1/4 and 1/8, B is the first grid line at or after t. For the triplet grids it is not
  always: when t lies exactly on a triplet grid line, (t − a)/g can exceed the whole
  number of lines by one rounding step, and B is then the next line. Up to beat 64 this
  happens for 15 of 48 lines of 1/2T, 31 of 96 of 1/4T, 63 of 192 of 1/8T and 127 of
  384 of 1/16T (for example 1/4T at t = 10/3 gives B = 4). A press one lattice step
  before or after a grid line gives the first line at or after it in all 3,424 such
  presses run.
- **X (A1 settled in revision 4; assumes A4).** In a set whose time signature never changes, a = 0.
  Examples: 4/4, 1 Bar, t = 5.3 → B = 8; 1/4T, t = 1.0 → B = 4/3; 4/4, 1 Bar,
  t = 1.5, 3.9, 3.99 and 4.0 → B = 4 (PRB-S5-01's presses, before the rule below).
- **S, X (revision 4; [REQ-PLAYBACK-CORE-008 and 009](playback-core.md#req-playback-core-008--launch-boundary-and-pre-delay)).**
  The clip's start counts from B, and its launch takes effect at E = B − o rounded to the
  1/3,843,840 grid. o is a pre-delay that the track's clip player supplies:
  - 0 on a MIDI track;
  - on an audio track, the clips' crossfade length (at most 4 ms in beats) when a session audio
    clip is playing and both clips have `Fade` on, else 0 (X).

  When B − t < o, the launch moves to B + g, but only if g > 0 and the transport was already
  playing before the press sample; otherwise o is reduced to B − t. A press exactly on a grid
  line therefore launches on that line on a MIDI track, at the press sample itself.
  - **Correction.** Revision 3 said the offset objects were "found through the song's track
    list" or "a per-song engine object" and existed only at run time. They are the track's clip
    player (no explicit time) and the track's clip timeable (explicit time). o reduces to pure
    arithmetic, run by extracted execution.
  - **Correction.** The "further track condition" is the song-already-playing test: the
    current sample differs from the sample at which playback last started. It is not a track
    field.
  - **Correction.** The move to B + g also needs g > 0.
- **U.** The audio of either clip between E and B when o > 0 (REQ-PLAYBACK-CORE-009).
- **U.** After a time-signature change, a is the start of the current
  time-signature segment, and not less than 0. Static expectation: with 4/4 changing
  to 3/4 at beat 8, 1 Bar, a press at beat 9 starts at beat 11. No reference
  observation is available (ADR 0003; PRB-S5-02). Static route: the layout of the
  time-signature entry that the anchor reads. X settles the arithmetic only: an anchor
  of 8 with g = 3 and t = 9 gives 11, and an anchor of −5 is used as 0.

### REQ-CLIP-LAUNCH-018 — launches without a grid

- **S (A1 settled in revision 4).** When REQ-016 gives no grid (clip None; Global with global None;
  out-of-range values), the launch is not moved to a grid line.
- **S (revision 4; [REQ-PLAYBACK-CORE-010](playback-core.md#req-playback-core-010--launch-without-a-grid-and-launch-while-stopped)).**
  There is no delay once the request is handled: B is the lattice-rounded press beat and
  o = 0, so the clip starts at the sample where the engine handles the request. When the engine
  handles an interface press relative to the audio buffer is U there.

### REQ-CLIP-LAUNCH-019 — launch with the transport stopped

- **S (revision 4; [REQ-PLAYBACK-CORE-010](playback-core.md#req-playback-core-010--launch-without-a-grid-and-launch-while-stopped)).**
  The engine sets the song position to the start beat if it is a locator, and otherwise to the
  start beat's downbeat (the bar line at or before it). It computes B from there and starts
  the transport. With a start beat of 0 the clip starts on the first played sample.
- **U.** The downbeat helper, the start beat after opening a set, and chasing of notes under
  way at such a start.
- **Correction.** Revision 3's static note that "the grid computation can return no grid when
  the song is not playing" applies to stop requests and empty-slot presses, not to clip
  launches.

### REQ-CLIP-LAUNCH-020 — Gate, Toggle and Repeat

- **U.** Start, stop and retrigger timing on press and release for launch modes 1–3,
  and for Trigger on release. No reference observation is available (ADR 0003;
  PRB-S5-06). Static route: the launch state machine's branches on launch mode,
  request kind and release flag, not yet interpreted. Only the stored values and
  labels (REQ-004) are specified.

### REQ-CLIP-LAUNCH-021 — Legato

- **U.** Where in the clip playback begins when a Legato clip is launched, and when.
  No reference observation is available (ADR 0003; PRB-S5-07). Static route: the
  engine's use of the Legato flag sent at launch. Only the stored value (REQ-001,
  REQ-009) is specified.

### REQ-CLIP-LAUNCH-022 — velocity amount

- **U.** How velocity amount scales clip volume by launch velocity. No reference
  observation is available (ADR 0003; PRB-S5-08). Static route: the engine code that
  reads the velocity amount, not located. Only the stored value and its bounds 0–1
  (REQ-009) are specified.

### REQ-CLIP-LAUNCH-023 — follow-action execution

- **U.** When a follow action fires for linked and unlinked follow actions, the role
  of `LoopIterations`, `FollowTime` and the jump indices, and chance selection. No
  reference observation is available (ADR 0003; PRB-S5-11). Static note: the
  loop-iteration count is passed on for playback only for linked follow actions; the
  follow time always is. Static route: the engine code that receives these values.

## Timing and state

- Units: song and clip positions in beats (quarter notes). Bar grid lengths and
  boundaries are rounded to the 1/3,843,840 lattice; the triplet note values are the
  binary64 values of 4/3, 2/3, 1/3 and 1/6 (REQ-015, REQ-017). Tempo does not change
  grid positions; it may change the unknown offset of REQ-017.
- Ordering on load: migration (REQ-014), then values, then the corrections of REQ-012
  and REQ-013.
- Persistent state: the fields of REQ-001 to REQ-003. A launch changes no stored field.
- Determinism: loading and the boundary rule are deterministic for a given document
  and press position. Follow-action chance selection is random and out of scope.
- Timing tolerance for the grid cases (revision 4): none. The start is graded to the sample by
  [REQ-PLAYBACK-CORE-002](playback-core.md#req-playback-core-002--placing-an-event-on-a-sample).
  Where that requirement allows P or P + 1, either is accepted. Revision 3's ±1/64-beat
  tolerance (375 samples at 48,000 Hz and 120 BPM) came from the PRB-S5-01 measurement design.
  It was coarser than the sample-exact timing dimension of ADR 0004, and is withdrawn. Under
  ADR 0003 only a candidate is measured.
- Undo, edits in the user interface, and cancellation of a pending launch are out of
  scope.

## Acceptance cases

Expectations are static derivations or, where the appendix lists them under "Cases
backed by X", X results of the original x86_64 functions. None has been run against
Live, and under ADR 0003 none will be. Kinds: P positive, N negative/malformed,
B boundary, M missing, S save, G grid timing, U unresolved (not graded).

### Fixtures

| ID | Shipped document | SHA-256 | Content used (D) |
| --- | --- | --- | --- |
| B1 | `Core Library/Lessons/Sets/Drums Lesson.als` | `66648e2054a014549df7681bc1fd52e35b9c575f771ba58b89ce7b6887ea630d` | `12.0_12402`; tempo 90; 4/4 (`TimeSignature/Manual` 201 and one `EnumEvent` 201); global 4, record 0; track 1, slot 1 MidiClip "Slide" and slot 2 "Velocity", each 1-bar loop, clip signature 4/4, launch 0/0, Legato false, velocity 0, follow action (4, true, 1, 4, 0, 100, 0, 1, 1, false) |
| B3 | `Core Library/Templates/Vocal Recording.als` | `d12d2102137fbe08331d69a526518868d5bdc8d3a577815a9f404d73dbb3c26e` | global 0 |
| B4 | `Core Library/Lessons/Sets/Driver Error Compensation.als` | `7459839acddcd42d4eb5b3d8f2c73e1ba3d04f29f764974081ad6850d9185c98` | record 5 |
| B5 | `Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als` | `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b` | 90 arrangement and take-lane clips with launch quantization 1 |
| B6 | `Builtin/Templates/DefaultLiveSet.als` | `aeec3f07599da0a61cc86fd9ddeb78a5ce61fe473f676d50c1ae3e281c289a1f` | `12.0_12117`; global 4, record 0; 8 scenes with follow action (4, true, 1, 4, 0, 100, 0, 0, 0, false) |
| B2 | `Core Library/MIDI Clips/Tonal/Single Chords/Staggered/Chord C Minor9 Staggered.alc` | `1dc59e9759cc9bf381e3df8717d550c443e0c770d2af454311f000841e3f7dc9` | clip launch mode 2, launch quantization 5; input to PRB-S5-09 and 10 only, which will not run (ADR 0003); no case uses it |

Paths are relative to `Contents/App-Resources/` of the 12.4.3 bundle. A fixture is
decoded, changed only as stated, and re-encoded as gzip. "Slide" means B1's slot-1
clip. A song time-signature edit sets `TimeSignature/Manual/@Value` and the
`EnumEvent` value to the same code (REQ-TRANSPORT-STATE-010: 3/4 = 200, 5/4 = 202,
6/8 = 302, 7/8 = 303), so REQ-TRANSPORT-STATE-012 does not arise.

### Document cases

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Fixture |
| --- | --- | --- | --- | --- | --- |
| CLC-001 | 001, 004, 005 | P | Slide `<LaunchMode Value="2" />`, `<LaunchQuantisation Value="5" />`; open | Opens; Slide `launch_mode` 2 (Toggle), `launch_quantization` 5 (1 Bar) | B1 edit |
| CLC-002 | 001, 002 | S | Open, save | Both clips keep the REQ-001 child order and values 0, 0, `false`, 0; `FollowAction` children in REQ-002 order with values unchanged | B1 |
| CLC-003 | 001 | N | Slide `<Legato Value="TRUE" />`; open | Set does not open | B1 edit |
| CLC-004 | 001 | N | Slide `<LaunchMode Value="2.0" />`; open | Set does not open | B1 edit |
| CLC-005 | 001 | N | Two `LaunchMode` elements in Slide; open | Set does not open | B1 edit |
| CLC-006 | 003, 005 | P | `<GlobalQuantisation Value="7" />`; open | Global quantization 1/4 (A6) | B1 edit |
| CLC-007 | 003, 005 | P | Open | Global quantization None | B3 |
| CLC-008 | 003, 006 | P | Open | Record quantization 1/16 (A6) | B4 |
| CLC-009 | 001 | S | Open, save | All 90 clips keep launch quantization 1 | B5 |
| CLC-010 | 007 | P | Slide `FollowActionA` 9, `FollowActionB` 2; open | A Jump, B Play Again or Again (A6) | B1 edit |
| CLC-011 | 009 | M | Delete Slide's `Legato`, `VelocityAmount` and `FollowAction`; open, save | Opens; saved Slide has `Legato` false, `VelocityAmount` 0 and `FollowAction` (4, true, 1, 4, 0, 100, 0, 1, 1, false) | B1 edit |
| CLC-012 | 009 | M | Delete Slide's `FollowAction/JumpIndexA`; open, save | Saved `JumpIndexA` 1 | B1 edit |
| CLC-013 | 010 | M | Delete Slide's `LaunchMode` and `LaunchQuantisation`; open | Opens; values equal the default-launch preferences; the preference values are unresolved (REQ-010) | B1 edit |
| CLC-014 | 011 | N | Slide `<LaunchQuantisation Value="15" />`; open | Opens; held, displayed and saved value and timing unresolved (REQ-011) | B1 edit |
| CLC-015 | 011 | N | Slide `<LaunchMode Value="4" />`; open | Opens; held, displayed and saved value unresolved (REQ-011) | B1 edit |
| CLC-016 | 011 | N | API: `clip.launch_mode = 4` on Slide | Error (its form and message text are not graded, REQ-011); value stays 0 | B1 |
| CLC-017 | 011 | N | API: `clip.launch_quantization = 15` on Slide | Error (its form and message text are not graded, REQ-011); value stays 0 | B1 |
| CLC-018 | 011 | B | API: `clip.launch_mode = 3`, then `clip.launch_quantization = 14` | Both accepted; Repeat and 1/32 | B1 |
| CLC-019 | 012 | P | Slide chances 30 and 30; open, save | Saved chances 50 and 50 | B1 edit |
| CLC-020 | 012 | B | Slide chances 0 and 0, `FollowActionEnabled` true; open, save | Saved chances 100 and 0, enabled false | B1 edit |
| CLC-021 | 012 | B | Slide chances 1 and 7; open, save | Saved chances 13 and 87 (half rounds away from zero) | B1 edit |
| CLC-022 | 012 | P | Slide chances 1 and 2; open, save | Saved 33 and 67 | B1 edit |
| CLC-023 | 011, 012 | B | Slide chances 150 and 50; open, save | Saved chances 75 and 25 | B1 edit |
| CLC-024 | 013 | B | Slide `<FollowTime Value="2.0000001" />`; open, save | Saved follow time parses to exactly 2 | B1 edit |
| CLC-025 | 013 | B | Slide `<FollowTime Value="3.0000002" />`; open | Held follow time is the 64-bit float nearest 11531521/3843840 (3.00000026015651); saved text not graded (REQ-001) | B1 edit |
| CLC-026 | 014 | P | First scene (`Id="0"`) `<IsLinked Value="false" />`, `MinorVersion` unchanged; open | First scene `IsLinked` true after opening; the saved scene form is unknown (REQ-014) | B6 edit |
| CLC-027 | 014 | P | Second scene (`Id="1"`) `<FollowTime Value="8" />`; open | Second scene `IsLinked` false and follow time 8 after opening | B6 edit |
| CLC-028 | 014 | P | A clip saved at `11.0_405` with clip-level follow time 4, A 0, B 0, chance A 1, chance B 0; open | Follow action: time 4, linked, A Next, chances 100/0, disabled | Authored minimal `11.0_405` document with the old clip form after `VelocityAmount`, as clip-launch-v1 `CLIP-LAUNCH-041`; no authentic set ships, and none will be observed (ADR 0003) |
| CLC-029 | 014 | P | As CLC-028 with A 3, chance A 0.5, B 1, chance B 0.5, follow time 8 | Enabled, unlinked, A Previous, B Stop, chances 50/50 | Authored as for CLC-028 (clip-launch-v1 `CLIP-LAUNCH-042`) |
| CLC-030 | 008 | U | Delete `GlobalQuantisation` and `AutoQuantisation`; open | Static expectation 1 Bar and None; not graded | B1 edit |
| CLC-057 | 012 | B | Slide chances 3 and 5; open, save | Saved chances 38 and 62 (37.5 rounds away from zero) | B1 edit |
| CLC-058 | 011, 012 | B | Slide chances −10 and 50; open, save | Saved chances 0 and 100 | B1 edit |
| CLC-059 | 011, 012 | B | Slide chances 150 and −50; open, save | Saved chances 100 and 0 | B1 edit |
| CLC-060 | 013 | B | Slide `<FollowTime Value="0.00000013007825507825505" />`; open | Held follow time is the 64-bit float nearest 1/3,843,840 (2.6015651015651016e-07), not 0; saved text not graded (REQ-001) | B1 edit |
| CLC-061 | 011, 013 | B | Slide `<FollowTime Value="-0.3" />`; open | Held follow time −0.3 (not raised to 0 or 0.25) | B1 edit |

### Grid cases

Common setup: the stated fixture edit; transport playing from beat 0 at 90 BPM;
Slide is launched once by a launch-button press handled at the render sample whose song beat
is t, as defined in [SPEC-PLAYBACK-CORE](playback-core.md#definitions). Comparator: the song
beat at which Slide's playback begins, exactly. The corresponding render samples are
[PBC-020 to PBC-024](playback-core.md#launch-cases). Slide is a MIDI clip, so the pre-delay is 0
and no press moves to B + g (REQ-017). Global value 4 and Slide value 0 unless stated. A1 is
settled (revision 4).

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Fixture |
| --- | --- | --- | --- | --- | --- |
| CLC-031 | 015–017 | G | t = 5.3 | B = 8 | B1 |
| CLC-032 | 015–017 | G | Global 3 (2 Bars); t = 9 | 16 | B1 edit |
| CLC-033 | 015–017 | G | Global 2 (4 Bars); t = 17 | 32 | B1 edit |
| CLC-034 | 015–017 | G | Global 1 (8 Bars); t = 1 | 32 | B1 edit |
| CLC-035 | 015–017 | G | Song 3/4; t = 4 | 6 | B1 edit |
| CLC-036 | 015–017 | G | Song 3/4, global 1 (8 Bars); t = 1 | 24 | B1 edit |
| CLC-037 | 015–017 | G | Song 6/8; t = 1 | 3 | B1 edit |
| CLC-038 | 015–017 | G | Song 7/8; t = 4 | 7 | B1 edit |
| CLC-039 | 015–017 | G | Song 5/4, global 3 (2 Bars); t = 1 | 10 | B1 edit |
| CLC-040 | 015–017 | G | Global 5 (1/2); t = 2.25 | 4 | B1 edit |
| CLC-041 | 015–017 | G | Global 6 (1/2T); t = 1.5 | 8/3 | B1 edit |
| CLC-042 | 015–017 | G | Global 7 (1/4); t = 2.1 | 3 | B1 edit |
| CLC-043 | 015–017 | G | Global 8 (1/4T); t = 1 | 4/3 | B1 edit |
| CLC-044 | 015–017 | G | Global 9 (1/8); t = 3.1 | 3.5 | B1 edit |
| CLC-045 | 015–017 | G | Global 10 (1/8T); t = 0.4 | 2/3 | B1 edit |
| CLC-046 | 015–017 | G | Global 11 (1/16); t = 1.3 | 1.5 | B1 edit |
| CLC-047 | 015–017 | G | Global 12 (1/16T); t = 0.2 | 1/3 | B1 edit |
| CLC-048 | 015–017 | G | Global 13 (1/32); t = 0.13 | 1/4 | B1 edit |
| CLC-049 | 016, 017 | G | Slide value 8 (1/4); t = 2.1 | 3 (not 4: the clip's value wins) | B1 edit |
| CLC-050 | 016, 017 | G | Slide signature 6/8 (`Numerator` 6, `Denominator` 8), value 5 (1 Bar); t = 1.2, then a second run with t = 4.2 | 3, then 6 | B1 edit |
| CLC-051 | 016, 017 | G | Slide signature 6/8, value 0; t = 1.2 | 4 (Global uses the song's 4/4) | B1 edit |
| CLC-052 | 018 | N | Slide value 1 (None); t = 5.3 | Starts at the press (song beat 5.3), not moved to 8 (REQ-018 r4) | B1 edit |
| CLC-053 | 018 | N | Global 0 (None); t = 5.3 | Starts at the press (song beat 5.3) | B1 edit |
| CLC-054 | 017 | G | t = 3.99, and t = 4.0 exactly (44,100 Hz: request sample 117,600) | Starts at 4 for both. At t = 4.0 the start is at the press sample itself (REQ-017; MIDI pre-delay 0) | B1 |
| CLC-055 | 017 | U | 3/4 from beat 8 (second time-signature event); t = 9 | Static expectation 11; not graded (REQ-017) | B1 edit |
| CLC-056 | 019 | U | Transport stopped at beat 5.3; launch Slide | Unresolved. Static expectation (REQ-019 r4): playback and Slide start together at beat 4, the downbeat of 5.3. Not graded: the start beat and the downbeat helper are untraced | B1 |
| CLC-062 | 016, 017 | G | Slide `<LaunchQuantisation Value="-99" />`; t = 5.3 | 8 (−99 is read as Global; the global value is 1 Bar) | B1 edit |
| CLC-063 | 016, 018 | N | Slide `<LaunchQuantisation Value="-1" />`; t = 5.3 | Starts at the press (song beat 5.3; no grid) | B1 edit |
| CLC-064 | 017 | G | Global 8 (1/4T); at 44,100 Hz, a press handled at request sample 98,000, whose song beat is exactly 10/3 | Starts at 4, not 10/3 (X arithmetic, triplet rounding; MIDI pre-delay 0) | B1 edit |

Omitted kinds:

- Cancellation and teardown. A pending launch that is cancelled or replaced is specified in
  [REQ-PLAYBACK-CORE-022](playback-core.md#req-playback-core-022--stop-buttons-and-quantized-stop)
  and graded there (PBC-089).
- REQ-019. It has S clauses since revision 4, but its case CLC-056 stays unresolved.
- The U-only requirements REQ-020 to 023. They have no graded cases, and under ADR 0003 no
  probe will supply the observation. The global-value table rows
for 0 and ≥ 14 are covered by CLC-053 and REQ-011's unresolved cases.

## Open questions

[Q-017](../questions.md#q-017-clip-launch-timing-and-launch-modes) holds the open
items: the boundary offset and track condition (REQ-017), the anchor after a meter
change, unquantized latency, the stopped-transport launch, Gate, Toggle and Repeat,
Legato, the velocity law, follow-action timing, and the default-launch preferences.
Added in revision 1:

- Missing or out-of-range `GlobalQuantisation` and `AutoQuantisation` (REQ-008,
  REQ-011): no S5 probe covered them. Static route: the song loader.
- Reachability of migration step 17 (REQ-014).
- A clip with several time-signature entries (REQ-016).

Added in revision 2, from the clip-launch-v1 staging and review:

- Values outside their stated ranges: bounded values, chances and follow times
  (REQ-011 to 013, A2).
- The message text and form of the scripting-interface error (REQ-011).
- Whether the opening corrections run for scenes (REQ-012, REQ-013).
- A step-406 clip that has both follow-action forms, and the saved form of a scene
  (REQ-014).
- The kept chance values (A7).

Settled or narrowed in revision 3 by extracted execution (X2): A7 and the chances outside
0 to 100 (settled); follow times outside 0 to below 1,000,000 and the near-tie follow-time
rounding (settled); the other bounded values (narrowed: the member's load step keeps them);
the grid lengths and the boundary arithmetic (X; the scheduler still rests on A1); the
offset call (narrowed, not settleable by X). New: the enum getter's −99 rule (REQ-011,
REQ-016), and the triplet-grid boundary for a press exactly on a line (REQ-017).

Settled in revision 4 by [SPEC-PLAYBACK-CORE](playback-core.md) r1 (static reading of the
named Live Engine matched to both Live slices, and X):

- A1 for the Trigger fire path;
- the offset o, which is 0 for MIDI and the audio crossfade length otherwise;
- the "track condition", which is the song-already-playing test;
- the delay of an unquantized launch, which is none once the request is handled;
- the stopped-transport launch, statically.

Still open:

- which gestures besides the launch button take the path;
- the start beat and downbeat helper of a stopped launch (REQ-019);
- the audio between E and B (REQ-017).

The [probe batch](../../analysis/ableton-live-12.4.3/r2/s5-clip-launch-v1/probe-batch.json)
(PRB-S5-01–11) is kept as the record of what observation would have settled. Under
ADR 0003 it will not run.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. Canonical evidence:
[clip launch](../research/clip-launch.md), retained run
`analysis/ableton-live-12.4.3/r2/s5-clip-launch-v1/` (image `Live.arm64` SHA-256
`3a99ceea…d1c383cfad`, base `0x100000000`). Dossiers are cited by query result
(`s5-0001` … `s5-0004`); "C1" marks a pseudocode record in `corpus-excerpts.jsonl`.
No new query was issued for this draft. F1 to F9 are the
[staging findings](clip-launch-handoff-plan.md#findings-while-staging) and RVC-01 to 13
the [review findings](../../handoff/clip-launch-v1/REVIEW.md#findings). Revision 2
re-checked them against the kept dossiers, the staging byte check
[fp_opcodes.py](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1-analysis/fp_opcodes.py) and the reviewer's
[checks](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1-analysis/review/review-checks.txt), without a new query.

| Requirement | Candidate | Evidence | Strength |
| --- | --- | --- | --- |
| 001 | CL-01 | `static-survey.json` `field_order_latest`, `homonyms_latest`, `classes_with_launch_fields_latest`; 4,130 rows of `clip-records.tsv`; paths re-read from B1, B5, B6 and the Driver Error set; `registry-order-check.txt` (28 AClip registrations = schema order); AClip vtable `0x1067b6cc0` slots `+0x140` loader `0x101487310`, `+0x138` writer `0x101486cdc` (`read_ptrs.py`); text conversion `0x10152bfb8` and add-member `0x101472624` from N1; read-back limited to Booleans and numbers of at most six significant digits (RVC-02): shipped written forms are `true`, `false` and plain digits only | D; S for save and text rules |
| 002 | CL-01 | Schema FollowAction order; AFollowAction registry `0x1025037a4` (C1, offsets `0x70`…`0x148`); `checks` in `static-survey.json` | D |
| 003 | CL-02 | Schema `LiveSet` positions 13–15; 376 documents | D |
| 004 | CL-03 | Label list `0x102438b44` (C1); Python enum `0x103abc6e8` (s5-0002, disassembly; strings `trigger` … `repeat`); getter `0x103ac1e94` reads `[clip,#0x270]` | S |
| 005 | CL-04, CL-05 | Clip list `0x102438d00` (s5-0002, 15 string refs in order); global list in ASong ctor `0x10266f738` (s5-0001, string refs `0x102670e0c`–`0x102670f5c`, 14 entries, `mov w2,#0xe`); Python `ClipLaunchQuantization` (s5-0002) and `Song.Quantization` with property `clip_trigger_quantization` (`0x103ba8520`, s5-0003); clip grid `0x102442998` (`sub w1,w0,#0x1`, s5-0001); getter `0x103ac1ed0` | S |
| 006 | CL-06 | Record list in `0x10266f738` (string refs `0x10267102c`–`0x1026710fc`, 9 entries); Python `RecordingQuantization`, `midi_recording_quantization` (s5-0003) | S |
| 007 | CL-07 | `0x102503ea0` (C1, "Play Again"); `0x102505724` (s5-0001, short list with "Again") | S; label use U |
| 008 | CL-08 | `0x10266f738`: `0x101567bfc([+0x388],4,…)`, `([+0x3c0],0,…)` (s5-0001); ASong loader not read | S; missing-field U |
| 009 | CL-09 | AClip ctor `0x102436fc4` (s5-0001): Legato `param_1[0xd]` (+0x68) false, VelocityAmount `0x1015743b0(0, 1.0, 0)`; AFollowAction ctor `0x102505030` (s5-0001): FollowTime 4.0, IsLinked 1, LoopIterations `0x10155afc8(…,1,0x3fffffff00000001)`; `0x102505724` chance `0x10157432c(0,100,default)`, jump `(-1.0, 8388608.0, 1.0)`; FollowActionEnabled 0; UserFloat init (s5-0004) | S; A2 |
| 010 | CL-10, CL-16 | `0x102436fc4`: LaunchMode from `0x1026ab2ec` (`+0x700`, `ClipDefaultLaunchMode`), LaunchQuantisation from `0x1026ab2f4` (`+0x6e8`, `ClipDefaultQuantisation`) on `0x102676cf0()`; 0 when `0x101849958()` is null; registry `0x1026a292c` (C1, registrations `0x6f8`, `0x6e0`); callback `AClip::UpdateEngineForLaunchParameters` | S; A2; preference mapping U |
| 011 | CL-15 | N1: loader stores enum index directly, setter `0x10156675c` not called; API setters `0x1033bbe98` (`cmp w1,#0x4; b.cs`) and `0x1033bc00c` (`cmp w1,#0xf; b.cs`) (s5-0004) throw `std::invalid_argument` with a built message, but its translation for scripts is not in the kept evidence (F2, RVC-10); the load path of the bounded members (UserFloat, ranged integer) was not read (F4, RVC-03) | S (A2) / U; API message U |
| 012 | CL-17 | `0x1025044b4` (s5-0003, disassembly `frinta s8,s0` at `0x102504550`; members `+0xf0` ChanceA, `+0x108` ChanceB, `+0x120` Enabled per registry); AFollowAction post-load at vtable `0x1067c8830` `+0xd0`; setter slot `+0x280`, chance controller `0x10652b4d8` not read (A7, RVC-11); the correction is a follow-action hook, so it may also run for scenes (F9) | S; A2, A3, A7 |
| 013 | CL-18 | `0x101565624(…,1,1)` in `0x102505030` sets flag `+0x70`; hook `0x10156580c` (C1; N1) rounds; bytes `0x101565860`–`0x1015658ac` re-read with `fp_opcodes.py` on 2026-10-18 (F5): sign select, `fmadd` x + s·0.5/3,843,840, `fabs`, `fmul` 3,843,840, `frintm`, `fdiv`, sign, the same sequence as the grid rounding in `0x101aaae44`; reviewer re-check (RVC-09) | S; A2, A3; near-tie U |
| 014 | CL-19 | Registry `0x10148ec98` (C1); `0x101493140` (s5-0002; table `0x105815e9c` re-read from `Live.arm64` on 2026-10-17: 0,1,2,3,4,5,6,8,10,12,14; `b.cs` at `0x1014931a0`; body ends at the throw `0x1014931d8`); `0x1014b6d14`, `0x1014b82d8` (s5-0003); `0x1014b8b00` (s5-0002, `mov w1,#0x4` at `0x1014b8be4`); `0x1014bb048` (C1); `0x1014c04d0` (s5-0004, pseudocode read; the reviewer re-read its retained disassembly and confirmed every condition and default, F7, RVC-08). Step 406 with an existing `FollowAction`: error report `0x101471a98`, then a no-return trap (`0x1014b6d14.c`, F6). Steps above 405 for clip, follow-action, scene, track and song elements checked by the reviewer: none outside the table touches these items (RVC-04). Scene writer not read (F7) | S; A5; step 17 reachability, both-forms clip and saved scenes U |
| 015 | CL-11 | `0x101aaae44` (s5-0001): `sub w8,w1,#1; cmp w8,#0xc; b.hi`; jump table `0x105846ef8` = `00 7a 37 61 2f a4 aa 76 ae 33 ac 2b 31` and sentinels `0x1055d9680` re-read from `Live.arm64` on 2026-10-17; constants 3843840.0 (`0x414d538000000000`), 4/3, 2/3, 1/3, 1/6 | S |
| 016 | CL-12 | `0x102442998` (s5-0001; clip TimeSignature registered at `0x1d0`, value `+0x1d8`); `0x1026e3698` `fcvtzs` (s5-0003); `0x10245efa0` passes `0x102442998(clip,0)` (s5-0002); `0x101acffa4` (s5-0002): override `cmp w6,#0xd; b.ls`, precomputed grid when `[slot,#0x38]`=1 and `[slot,#0x20]`≥2, else global `0x101b0e1c0` when `w7` (requested time = DBL_MAX) | S; A1 (slot test uninterpreted) |
| 017 | CL-13 | `0x101ad0130` (s5-0001) `0x101ad06cc`–`0x101ad0924`: `fcmp d12,#0.0; b.le` skips the ceiling; `0x101abf294` anchor `fmaxnm([sig,#8],0)` (s5-0002); `0x1011be6c8` mode 1 `frintp` then lattice (s5-0001); offset `0x101ad1418` virtual call (s5-0004); condition `0x101acfe68` (s5-0003). Revision 4: Engine names `OAsyncClipFireManager::PrepareClipFire`, `RequestedPredelaySongBeatForClip` (slot +0x48 of the clip player, 0 for MIDI; audio `OAudioClip::SCrossfadeDurBeat` x86 `0x102278eb0`, arm64 `0x102188f34`, X 16 of 16) and `SongWasPlayingBeforeCurrentSample` ([t13-playback-v1](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/manifest.json) `launch/`) | S ceiling; X pre-delay; A1 settled; A4; meter-change anchor U |
| 018 | CL-14 | Grid default 0.0; ceiling skipped when g ≤ 0; with g = 0 the near-boundary branch sets o := B − now. Revision 4: B = lattice(t), o = 0, activation at the request sample (`launch/`) | S |
| 019 | — | `0x101acffa4` immediate-check path returns 0.0 when engine byte `+0x68` ≠ 1: revision 4 reads this as the stop and empty-slot branch. Stopped launch: Engine `OFireManager::FireClip` (x86 `0x101b1c870`, arm64 `0x101af0cbc`) sets the start beat's downbeat unless it is a locator, then requests play | S; start beat and downbeat helper U |
| 020–023 | CL-21–23 | `0x10245efa0` sends Legato (conditional on vtable `+0x300`), launch mode, follow data; `0x10250416c` (s5-0003) sends LoopIterations only when IsLinked (else `0x80000000`) | U |
| Fixtures | CL-20 | `inputs-documents.tsv`; values re-read from B1–B6 on 2026-10-17 | D |

Derived values (grid cases, chances, follow times) were recomputed with a scratch
emulation of the cited disassembly, including 32-bit chance arithmetic; the script was
not retained. Each value can be rechecked by hand from REQ-012, 013, 015 and 017.
Revision 3 replaces that emulation with X runs of the original functions.

**Extracted execution (X2, revision 3).** Evidence:
[x2-notes-launch-v1](../../analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/manifest.json),
regenerated by `sh run.sh`: `results/launch.json` and `results/follow.json` (each run with
its model value), `inputs.json`, `raw/runs.jsonl`, `addresses.json` (matching),
`slice-compare.txt` (arm64 comparison), `imports.txt` and `summary.txt`. The method is on
the research page:
[clip launch, X2 results](../research/clip-launch.md#extracted-execution-results-x2-2026-10-18).

| Requirement | x86_64 function run (arm64 counterpart) | Setup and result | Limits |
| --- | --- | --- | --- |
| 015 | Grid length `0x101ad2ef0` (`0x101aaae44`) | {n, d} in a buffer, q in a register; 6,463 combinations equal the REQ-015 table, bit for bit | How the clip or song signature is read is S (`0x102815210`, `cvttss2si` = arm64 `fcvtzs`) |
| 017 | Lattice helper `0x1011999d0` (`0x1011be6c8`), mode 3 for the press-time rounding; boundary helper `0x101ae8280` (`0x101abf294`), mode 1 | An anchor entry with the anchor at +8; 37 listed presses (PRB-S5-01, every grid case, anchors 8, −5 and 8.0000001) and 5,136 presses on and one lattice step beside every note-value grid line up to beat 64 | The engine's own rounding of the current time is an inline copy of the same sequence (x86 `0x101afa4dd`–`0x101afa553`, S). That the fire path calls the helper for a press (A1) is settled in revision 4. The offset rule is in REQ-PLAYBACK-CORE-008 |
| 011, 016 | Enum getter `0x101556330` (`0x1015661b8`) | Stored −99 returns 0; −100, −98, −1, 0, 1, 14, 15 and the 32-bit extremes are returned as stored | That the clip grid `0x1025612b0` (`0x102442998`) uses this getter on [clip+0x258] is S |
| 012, A7 | Follow-action post-load `0x10262a930` (`0x1025044b4`): slot +0xd0 of vtable `0x106d0dc08` | Hand-built AFollowAction with two UserFloat chances. Each chance has the real vtable `0x106bc35b0`, is set up by the real init `0x101564e20` with the ctor's (0, 100) mapping `0x101566480`, and holds the loaded value stored at +0x58 as the loader stores it. The listener callback and the enabled setter are skipped under gdb and recorded. 28 chance pairs. The chance setter `0x101565360` limits to 0–100; values in range are kept as computed | The real AFollowAction ctor `0x10262b4b0` was not run: it needs the class registries, which need libc++ imports. That A3's post-load runs for each clip is S |
| 013 | ARemoteableDouble post-load `0x101555850` (`0x10156580c`) | Hand-built double with the real vtable `0x106bc07b0` and flag +0x70; the generic part `0x10147e120` skipped under gdb; 33 values with the flag set and 33 without. The binary64 formula equals X for all 66; exact rounding differs for 6 near-tie values | The flag is set by the AFollowAction ctor for `FollowTime` (S, both slices) |

No import was called by any of these runs. The slice comparison found no difference: arm64's
`frinta`, `frintp`, `frintm` and `fmaxnm` match x86's rounding sequences and `maxsd` for
every input class, and arm64's `fmadd` adds an exact product.

**Cases backed by X.** CLC-019 to 025 and 057 to 061 take their values from X runs of the
rescaling, the chance setter and the follow-time rounding, with the load path S and A3.
CLC-031 to 053, 062 and 063 take B from X runs of the grid length and the boundary helper,
with the launch path under A1, settled in revision 4. CLC-054 and 064 become graded in revision 4. CLC-055
records X arithmetic but stays unresolved.

Corrections and contradictions:

- The research page says no shipped document exercises the translators. B6 is at
  `12.0_12117`, below step 12203, so the scene step applies to it under A5 (no value
  changes, since its scenes already meet the linked condition).
- Step 17 precedes the oldest shipped schema (`8.1_220`); under A5 and
  REQ-ALS-CONTAINER-005 it cannot run for an opened Live Set. Recorded as U.
- Two corpus readings were wrong, as the research page records: the lattice and
  chance roundings round to nearest in disassembly.
- Revision 1 graded the API message prefixes, although its scope excludes the text
  of error messages (F2). Revision 2 marks the text unknown.

Downgrades from the research candidates: CL-12's engine use of the clip grid now names
A1, because the slot-state test in `0x101acffa4` is uninterpreted. CL-08 is split: the
initial value is S, a missing set field is U (the ASong loader was not read). CL-15 and
CL-16 load clauses carry A2 (research: inferred); CL-16's resulting values remain U.
Dropped: the velocity-amount API range error (`0x1033bc1a4`, pseudocode only) and the
"no application object" default of 0 (not user-observable). Revision 2 limits A2 to
values inside their stated ranges (RVC-03) and marks CL-15's API message unknown
(RVC-10).

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from S5 (CL-01 to CL-23): 23 requirements (3 D with S parts, 5 S only, 10 S with U parts, 5 U only); 56 unexecuted cases: 4 not graded (CLC-030, 054–056), 3 with unresolved parts (CLC-013–015), 2 without a fixture (CLC-028, 029) |
| 2 | 2026-10-18 | Staging and review findings of clip-launch-v1 applied; none rejected. F1, RVC-01: release proposal for REQ-015 to 018 dropped. F2, RVC-10: REQ-011 API message text U; CLC-016, 017 grade no text. F3, RVC-02: REQ-001 read-back limited to Booleans and numbers of at most six significant digits; CLC-025 grades the held value. F4, RVC-03: A2 limited to the stated ranges; out-of-range bounded values, chances and follow times U; 150/50 example removed; CLC-023 relabelled U. F5, RVC-09: REQ-013 byte evidence; near-tie values U. F6: both-forms clip U. F7, RVC-08: CLC-026, 027 grade held scene values; saved scene form U. F8: CLC-028, 029 use authored `11.0_405` fixtures. F9: scene corrections U. RVC-04: other conversion steps stated. RVC-05: REQ-005 worded as meaning. RVC-11: A7 named. RVC-13 coverage proposals deferred (no error). ADR 0003: probe references now say that no reference observation is available, with static routes. 23 requirements (3 D with S parts, 4 S only, 11 S with U parts, 5 U only); 56 unexecuted cases: 5 not graded (CLC-023, 030, 054–056), 3 with unresolved parts (CLC-013–015), all with a fixture |
| 3 | 2026-10-18 | Extracted execution (packet X2, evidence label X added). REQ-012 and 013 become X with an S path. A7 is settled: the chance setter limits to 0–100 and does not run the chance controller. REQ-015's table and REQ-017's boundary arithmetic become X; REQ-017 still assumes A1, and its near-boundary clause stays U. REQ-011: chances and follow times outside their ranges settled by X; the other bounded values narrowed (S); the −99 rule added. A2 extended statically to out-of-range values. Errors found: REQ-016 said every negative clip value gives no grid, but −99 reads as Global; REQ-017 said B is always the first grid line at or after t, which fails for some presses exactly on a triplet line; REQ-013's near-tie U is replaced by the binary64 formula. CLC-023 becomes gradable (75/25); CLC-057 to 064 added. 23 requirements (3 D with S parts, 3 S only, 1 X only (015), 11 with U parts, 5 U only); 64 unexecuted cases: 5 not graded (CLC-030, 054–056, 064), 3 with unresolved parts (CLC-013–015); of the 59 graded, 12 document cases and 25 grid cases are backed by X, and 22 are static or documented |
| 4 | 2026-10-18 | Corrections from [SPEC-PLAYBACK-CORE](playback-core.md) r1 (packet T1.3). A1 settled for the Trigger fire path (REQ-PLAYBACK-CORE-007). REQ-017: the offset is the track player's pre-delay (0 for MIDI, the audio crossfade length otherwise, X), not a run-time-only value; the "track condition" is the song-already-playing test; the move to B + g needs g > 0; activation at B − o; the audio between B − o and B stays U. REQ-018: no delay once the request is handled (S). REQ-019: stopped launch (S) with the start beat and downbeat helper U; revision 3's "no grid when not playing" note applied to stops, not launches. The ±1/64-beat tolerance is withdrawn in favour of REQ-PLAYBACK-CORE-002. CLC-054 and 064 become graded; CLC-052, 053 and 063 get exact expectations; grid-case setup restated with request samples. 23 requirements (3 D with S parts, 4 S only, 1 X only (015), 11 with U parts, 4 U only); 64 unexecuted cases: 3 not graded (CLC-030, 055, 056), 3 with unresolved parts (CLC-013–015); of the 61 graded, 12 document cases and 27 grid cases are backed by X, and 22 are static or documented |

Revision 1 proposed that a first handoff could carry REQ-001 to 007, 009, 012, 013,
015, 016 and the S clauses of 011, 014, 017 and 018, without REQ-017's near-boundary
clause. Revision 2 drops REQ-015 to 018 from that proposal (F1, RVC-01): REQ-015's
grid lengths are observable only by launching, and REQ-016 to 018 rest on A1, which
is open under Q-017.

Released 2026-10-18: [clip-launch-v1](../../handoff/clip-launch-v1/README.md), 50 cases, approved with narrowing by a separate review agent (partial REQ-001 to 007, 009, 011 to 014 only; 008, 010, 015 to 023 unreleased). The review findings to apply in the next revision are on the [handoff plan](clip-launch-handoff-plan.md#review-outcome). Revision 2 applies them; the revision table lists each one.

clip-launch-v1 stays pinned to revision 1, and revision 3 is unreleased. A later release
revision could carry REQ-012's and 013's X-backed cases and the out-of-range chance cases.
Revision 4 settles A1, so a later release could also carry REQ-015 to 018 and the grid cases,
graded to the sample through SPEC-PLAYBACK-CORE. clip-launch-v1's manifest's partial scopes define
what was released. These draft clauses are broader than the release and unreleased:
clips in take lanes and the groove pool, and repeated clip children other than
launch elements (REQ-001); API names (REQ-004 to 006) and the API setters (REQ-011);
bounds as behavior, shipped jump indices and creation paths (REQ-009); the old-form
defaults for absent chances, steps 17 and 12008, and versions other than `11.0_405`,
`12.0_12117` and `12.0_12402` (REQ-014).
