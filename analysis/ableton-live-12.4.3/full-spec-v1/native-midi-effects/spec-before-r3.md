---
id: SPEC-NATIVE-MIDI-EFFECTS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3
---

# Native MIDI effects

## Scope and evidence boundary

This canonical partial draft owns the eight native MIDI effects: Arpeggiator,
CC Control, Chord, Note Length, Pitch, Random, Scale and Velocity
(`SURF-DEVICE-ARPEGGIATOR`, `SURF-DEVICE-CC-CONTROL`, `SURF-DEVICE-CHORD`,
`SURF-DEVICE-NOTE-LENGTH`, `SURF-DEVICE-PITCH`, `SURF-DEVICE-RANDOM`,
`SURF-DEVICE-SCALE`, `SURF-DEVICE-VELOCITY`). It describes incoming events,
control actions and outgoing MIDI; it does not specify audio from downstream
instruments. No application, original function or candidate was executed.

**D12** means documented in the captured current Live 12 manual, whose revision
is not pinned to 12.4.3. **S-presence** means directly observed schema/preset
bytes from the installed 12.4.3 package; it establishes stored vocabulary only.
**U** means an unsupported outcome, including exact-build applicability of every
D12 clause. There are no S behavioral-law, X or compatibility-pass claims here.
A documentary predicate can be reviewed without granting an exact-build grade.

[Research](../research/native-midi-effects.md) owns source identities, package
observations and contradictions. [MIDI editing/tools](midi-editing-tools.md)
owns destructive clip transformations and generators; these are live devices.
[MIDI user mapping](midi-user-mapping.md) owns controller-to-parameter transforms.
[MIDI note storage](midi-note-storage.md) owns clip data and reader limits;
[playback core](playback-core.md) owns upstream clip event emission. Their note
off and range laws do not automatically apply after a MIDI effect.
[Device chains and racks](device-racks.md) owns common chain insertion,
activation and preset interactions, while device-specific sounding-note behavior
remains open below. [Automation](automation-envelopes.md) does not by itself
settle when an effect samples a changing parameter.

## Inputs, observables and comparison rules

Cases start with one enabled device in a MIDI chain and no unrelated processing,
except cases explicitly exercising bypass. Set every named control through its
visible unit; a number in an XML preset is not a UI enum decoder. Incoming events
have note pitch, on/off identity, velocity and event time; CC, pitch bend,
channel pressure, sustain and per-note expression are distinct event types.
Unless stated, use isolated nonoverlapping notes, scale awareness off, and
nonextreme legal note values. Octave names follow the source/UI spelling; cases
using C3 do not silently translate it to a MIDI key number.

Compare emitted pitch sets/sequences, selected velocity values, event categories,
and visible enable/disable or learning state only where the case states a
supported predicate. Ordering excludes equal-time tie ordering unless explicit.
Documentary durations compare the nominal musical/millisecond relation; there
is no approved sample, scheduling-jitter or latency tolerance for these effects.
A note-on predicate alone says nothing about note-off matching, channel,
expression, untouched-event forwarding or error handling. All cases remain
unexecuted; U cases have a null oracle and cannot pass.

## Requirements

Each clause marked D12 is a proposed documentary contract. The parenthetical
`M` locator refers to numbered lines of the retained manual text in the appendix.
Every requirement also retains the exact-build U boundary above.

### REQ-NATIVE-MIDI-001 — scale-aware pitch controls

**D12 (M 0003–0004).** Enabling Use Current Scale changes pitch controls from
semitones to scale degrees. Device-specific ownership of root/scale appears
below. **U:** absent clip/scale, out-of-scale input selection, tuning systems,
scale changes while notes sound, and rounding of nonintegral transpositions.

### REQ-NATIVE-MIDI-002 — Arpeggiator sequence styles

**D12 (M 0011–0020, 0026).** Style selects and displays a note pattern; previous
and next buttons cycle styles. Play Order follows input play order; Chord Trigger
repeats the held pitches together. Random continuously randomizes; Random Other
avoids reusing a note until the others have been used; Random Once repeats one
random ordering until incoming MIDI changes. Pattern Offset 1 starts at the
second pattern position and moves the former first to last. **U:** exact orders
for Up/Down/Converge/Diverge and all other styles, duplicate-pitch identity,
random seed/distribution, what changes invalidate Random Once, and offsets beyond
one cycle. A finite random test does not prove distribution or fairness.

### REQ-NATIVE-MIDI-003 — Arpeggiator rate, gate and transposition

**D12 (M 0021–0024).** Rate is milliseconds in Free or a tempo-synced division.
Gate expresses duration as a percentage of Rate; values over 100% overlap.
Distance is semitones or scale degrees; Steps counts successive transpositions
following the original pattern. Distance +12 st, Steps 2 gives original, +12,
+24. Negative Distance lowers successive repetitions. Root/Scale choosers set
local scale; Use Current Scale takes the clip scale and disables these choosers.
**U:** first event phase, exact division catalog, timing grid, gate rounding,
end-of-pattern overlaps, groove interaction and pitches beyond the MIDI range.

### REQ-NATIVE-MIDI-004 — Arpeggiator held set, retrigger and repetition

**D12 (M 0025, 0030–0035).** Hold keeps a pattern after physical release; adding
held keys adds pitches and playing a pitch a second time removes it as described
by the manual. Retrigger Off does not restart the pattern, Note restarts on a
new note, Beat restarts at Interval; the retrigger LED flashes. Repeats controls
pattern repetition; its documented default is infinite. **U:** replacement versus
addition when all physical keys are up (the manual also says repetition continues
until another key), pedal interaction, last-note removal, finite-repeat restart,
transport stop/jump and held-note retirement. The held-set ambiguity is retained,
not resolved by choosing an interpretation.

### REQ-NATIVE-MIDI-005 — Arpeggiator velocity and groove

**D12 (M 0027–0029, 0036–0037).** Groove selects swing influenced by Global
Groove Amount. Velocity enables Target/Decay; Decay is the time to Target.
Velocity Retrigger restarts the velocity slope when the pattern retriggers.
**U:** decay curve, event velocities, target-zero note suppression, groove
quantities, retrigger phase and behavior when toggled during a held pattern.

### REQ-NATIVE-MIDI-006 — CC Control event families

**D12 (M 0041–0049).** The three fixed controls produce modulation, pitch bend
and channel pressure; Pitch Bend has downward negative and upward positive
values. Custom A switches between on/off or minimum/maximum and can be assigned
through CC Type Chooser; CC64 sustain is its documented intended use. There are
12 customizable dials B–M. Pitch bend and pressure must be observed as their own
MIDI event families, not assumed to be 7-bit CC messages. **U:** numeric ranges,
wire encoding, channel choice, quantization, reset-to-center and repeated-value
suppression; this source does not supply their byte-level laws.

### REQ-NATIVE-MIDI-007 — CC Control assignment, Send and automation

**D12 (M 0050–0052).** B–M have custom names and assignments, shown on Push and
saveable as presets. Values can be automated or moved in real time. Bank toggles
show controls 1–8 or 9–16. Send outputs current MIDI CC values. Learn assigns
incoming CC data to a customizable control. Existing CC automation and outgoing
CC Control data merge. **U:** learning target selection, multi-message learning,
consumption versus forwarding, Send order/count and treatment of non-CC fixed
controls, duplicate assignments, same-time merge order, smoothing, preset-load
emission and hardware receipt. Preset storage is a documentary promise, not an
observed successful round trip.

### REQ-NATIVE-MIDI-008 — Chord pitches and duplicate shifts

**D12 (M 0056–0058).** An input note supplies the root and up to six additional
pitches with Shift 1–6 in −36..+36 st. +4 and +7 form the root major triad,
independent of which slots hold those values. Reassigning the same pitch to
another Shift deactivates that additional assignment. **U:** zero-shift slot
activation, collision with another input note, pitch overflow, note-off ownership
and simultaneous ordering.

### REQ-NATIVE-MIDI-009 — Chord learning

**D12 (M 0059).** With Learn enabled, the first held key is the root and consumes
no Shift; subsequent held pitches fill Shift slots in play order. Additional
held keys extend the learned chord; disabling Learn ends assignment.
**U:** more than six additions, release/repress, sustain, removal, monitoring
while learning, cancelling a partially learned chord and undo grouping.

### REQ-NATIVE-MIDI-010 — Chord dynamics and chance

**D12 (M 0060–0063).** Each generated note has relative Velocity 1%..200%; 100%
matches input velocity. Chance is 0%..100%, with 100% generating that note for
every input. **U:** velocity multiply rounding/clipping, chance seed/distribution
or correlation, and note-off behavior after a suppressed note. No finite trial
count is required to reproduce a probability proportion.

### REQ-NATIVE-MIDI-011 — Chord strum, scale and per-note events

**D12 (M 0064–0073).** Strum offers delays up to 400 ms between notes; positive
order is original then Shift1..Shift6, negative reverses it. The context option
allows duplicate notes when strumming. Positive Tension accelerates successive
strums; negative slows them. Crescendo raises or lowers successive velocities.
Use Current Scale selects degree shifts. Send Per Note Events to Generated Notes
extends MPE data to generated notes; with scale awareness, per-note bend follows
the clip scale. **U:** delay curve/exact timestamps, tension/crescendo arithmetic,
late note-offs during a pending strum, duplicate policy with Strum zero, expression
channel allocation and bend values.

### REQ-NATIVE-MIDI-012 — Note Length triggered on note-on

**D12 (M 0077–0078).** With Trigger Source Note On and Latch off, output duration
is Length multiplied by Gate/100; Gate 50%, 100%, 200% yields half, full, double
Length. Time Mode selects milliseconds or tempo divisions. **U:** exact start
latency, source note-off suppression, same-key retrigger, gate/length control
bounds and updating Length or tempo while an output note sounds.

### REQ-NATIVE-MIDI-013 — Note Length triggered on note-off

**D12 (M 0079).** With Note Off selected, the output note starts when its input
note is released, rather than at input note-on, and then uses Gate and Length.
**U:** unpaired release, simultaneous releases, sustain's effect with Latch off,
output note-off velocity and event-grid placement.

### REQ-NATIVE-MIDI-014 — Note Length release dynamics

**D12 (M 0080–0083).** In Note Off mode, Release Velocity blends input on/off
velocities. Decay begins at incoming note-on; its value at note-off sets output
velocity, reaching zero after Decay Time. Positive Key Scale lengthens notes
below C3 and shortens those above; negative reverses that relationship.
**U:** blend equation, decay shape, order of operations, pitch scaling law and
zero-velocity result. No numeric output oracle follows from the qualitative law.

### REQ-NATIVE-MIDI-015 — Note Length latch

**D12 (M 0084).** Note On latch sustains triggered notes until the next note-on.
Note Off latch depends on all keys/pedal being released and a new note-off.
Latch disables Gate and Length; in Note Off latch, Release Velocity, Decay Time
and Key Scale are also disabled. **U:** exact Note Off latch transition (especially
which release qualifies), chord release ordering, pedal and repeated-note cases.
The documented UI disablement is gradable; the ambiguous Note Off event sequence
is not assigned a fabricated oracle.

### REQ-NATIVE-MIDI-016 — Pitch transposition and step controls

**D12 (M 0088–0092).** Pitch offers ±128 st or ±30 scale degrees. Step Up/Down
changes Pitch by Step Width, 1..48 st or 1..30 degrees. Controls accept key/MIDI
mapping (mapping math belongs to the mapping spec). **U:** clipping/wrapping at
control bounds, overflowed outgoing keys, off-scale degree selection and effects
of an automated pitch change on already sounding notes.

### REQ-NATIVE-MIDI-017 — Pitch range modes

**D12 (M 0093–0097).** Lowest and Range define permitted pitches. Block drops
out-of-range notes and flashes its LED; Fold transposes them into range; Limit
moves below-range notes to the lower bound and above-range notes to the upper
bound. **U:** range width/end inclusion, filtering before versus after Pitch,
Fold interval and empty/one-note range. Cases use Pitch zero to avoid inventing
the processing order and avoid unproven exact upper endpoints.

### REQ-NATIVE-MIDI-018 — Random pitch selection and signs

**D12 (M 0101–0104, 0107–0114).** Chance controls probability of pitch alteration;
Choices has 1..24 possibilities and Interval controls their spacing. Add raises,
Sub lowers, Bi permits both; the +/0/− LEDs identify the direction. The documented
Random/Add example Choices 1, Interval 12, Chance 50% restricts outputs to C3 or
C4 for input C3. Choices12/Interval1 permits unaltered C3 or C#3..C4.
**U:** seed/distribution, finite proportions, exact Chance thresholds, Bi zero
handling and overflow. The examples authorize pitch-membership predicates only,
not a fixed random sequence or a 50/50 finite-sample test.

### REQ-NATIVE-MIDI-019 — Random Alt mode and contradictory examples

**D12 (M 0105).** Alt uses a cyclic order. Chance100% advances to the next step;
Chance0% outputs the incoming pitch. **U (M 0106):** a 12-choice example describes
C3 through C4 before reset (13 notes), while Choices2/Interval2 describes only
C3,D3 (2 notes). These cannot support a single generalized cycle-length formula.
Both setups are retained as ungraded cases; phase/reset and intermediate Chance
are unknown. No algorithm is inferred from the parameter names.

### REQ-NATIVE-MIDI-020 — Random with a scale

**D12 (M 0115).** Use Current Scale constrains generated pitches to the clip
scale. **U:** degree spacing with Interval, inclusion of off-scale dry notes,
scale changes during Alt and cross-note versus per-pitch cycle state.

### REQ-NATIVE-MIDI-021 — Scale matrix and root

**D12 (M 0119–0122).** Matrix columns select incoming notes and rows outgoing
notes; mapping C to D converts incoming Cs to Ds. Base/Scale Name choose the
mapping; Use Current Scale uses the clip root/scale and disables those choosers.
User mode permits moving or deleting highlighted assignments; deletion prevents
that input note from producing output. **U:** top/right 13th grid cell semantics,
selection gestures and mapping ordinal encodings. The manual calls it a 13×13
grid representing 12 notes; no extra note class is inferred.

### REQ-NATIVE-MIDI-022 — Scale User fold

**D12 (M 0124).** In User mode, Fold changes a mapped pitch when its distance
from input exceeds six semitones. The documented C3→A3 mapping becomes C3→A2.
**U:** exactly ±6, downward counterpart, transpose ordering and range edges.

### REQ-NATIVE-MIDI-023 — Scale transposition and selected range

**D12 (M 0123, 0125).** Transpose is ±36 st. Lowest C2, Range+36 applies mapping
to C2..B4 and leaves other notes alone; Transpose+7 applies within that same
range. **U:** arbitrary range interpretation, one-note/zero ranges, overflow,
range versus fold/transpose order outside this documented example.

### REQ-NATIVE-MIDI-024 — Velocity transfer and operation

**D12 (M 0129–0132).** Lowest/Range select the input velocity interval; Out Low/Hi
select the output interval. The displayed curve shows the transfer. Operation
chooses Note On, Note Off (Rel. Vel.) or both. Out Low80/Hi127 constrains outputs
to the higher range. **U:** exact transfer formula and rounding, velocity zero,
fractional upstream velocities, swapped ranges and off-event ownership.
The manual's “essentially bypassed” example authorizes no bit-identity claim.

### REQ-NATIVE-MIDI-025 — Velocity outside-range modes

**D12 (M 0133–0136).** Clip constrains incoming out-of-range velocities; Gate
removes out-of-range events and flashes its LED when blocking a note; Fixed sets
outgoing velocity to Out Hi regardless of incoming velocity. **U:** exact range
endpoint inclusion, whether a gated note-on suppresses its later note-off,
release-only Gate lifecycle and precedence of Fixed versus Random/curve controls.

### REQ-NATIVE-MIDI-026 — Velocity randomness and curve shaping

**D12 (M 0137–0142).** Random modulates velocity within the output range; the
OutLow60/Hi127, Random50 example permits up/down changes of at most50 while
remaining in60..127. Positive Drive favors higher velocities; negative favors
lower. Positive Compand expands toward extremes; negative compresses toward the
middle. **U:** formulas, distribution, seed, correlation, curve sampling and
processing order. Shading represents the random range; it is not a distribution
measurement.

### REQ-NATIVE-MIDI-027 — device lifecycle and failures

**U.** For every device independently, establish automation at an event boundary
and during a held note, bypass/re-enable, stop/continue/reset, save/reopen, undo,
cancel, malformed input and deletion/track teardown. Stored `Timeable*` fields
and `On` prove none of these emitted-event outcomes. Do not borrow upstream clip
note-off laws or assume reset clears random/held state. Concrete probes below
capture outstanding obligations without prescribing guessed behavior.

## Acceptance cases

The canonical machine-readable setups, documentary predicates, sources and null
oracles are in [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/cases.json).
`NME-*` IDs are stable. Every case has `execution: unexecuted` and
`exact_build_grade: U`. D12 grade means only that its stated partial predicate
is supported; fields outside that predicate remain unknown. Source line ranges
are exact locators in the capture, not live web numbering.

| Group | Cases | Compared subset |
| --- | --- | --- |
| Shared pitch awareness | NME-001 | UI unit change only |
| Arpeggiator | NME-002–014 | chord/ordered/random style predicates, rate/gate nominal relations, transposition, hold, repeat, local-scale ownership, velocity controls |
| CC Control | NME-015–021 | event families, assignment/UI banks, Send presence, learning, preset names and merging |
| Chord | NME-022–030 | major-triad pitch set, duplicate shifts, learning, velocity/chance, strum order and options |
| Note Length | NME-031–039 | nominal durations, release trigger, latch disablement; uncertain release and dynamics timing ungraded |
| Pitch | NME-040–045 | octave transposition, step change, range mode class; Fold exact pitch remains U |
| Random | NME-046–052 | support sets, directional signs, Alt zero chance; contradictory cycle examples U |
| Scale | NME-053–059 | matrix conversion/deletion, documented fold example, selected range transposition, scale-owned choosers |
| Velocity | NME-060–066 | output interval, Fixed/Gate, operation selection, random interval; curve arithmetic U |
| Per-device lifecycle | NME-ARP/CC/CH/NL/PI/RA/SC/VE-L01–L10 | ten separately recorded probes for each device; all U |

Revision 2 corrects the Note Length active Length automation/Undo setups to
Latch off, because Latch disables Length. Pitch lower-bound cases use an accepted
positive Range value without assigning an unsupported unit. NME-064 grades
only the documented output interval; its modulation-displacement baseline is U.
The original revision 1 seal and all payload bytes are retained in the
[author-r1 archive](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/author-r1-snapshot.tar.gz).

The lifecycle rows cover positive automation/round-trip setups and negative,
boundary, malformed, cancellation, undo and teardown kinds for all eight devices.
They are not graded merely because they are enumerated. The device-specific
case sets avoid malformed wire payloads until L03 and do not test sound/audio.
Cancellation is a control/learning operation, not cancelling an already emitted
MIDI event. No applicable case class is excluded as inherently irrelevant.

## Remaining contract gaps

All eight profiles remain partial. Exact-build behavior, ranges not stated by
the manual, channel/per-note ownership, outgoing MIDI range handling, held-note
retirement, random distributions, event timing and device-specific lifecycle
are open. Random Alt cycle length, Arpeggiator hold replacement and Note Off
latch wording need separate evidence. No application comparison, hardware
receipt or supported load/save round trip has been observed.

## Analyst evidence appendix

Remove/review for a handoff. **M** is
[retained text](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manual-midi-effects.txt),
derived from [official HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manual-12-midi-effects-2026-10-19.html),
URL [Live MIDI Effect Reference](https://www.ableton.com/en/live-manual/12/live-midi-effect-reference/),
captured 2026-10-19, SHA-256
`33739cb549d6577624acd91466dafeafe8faaeea03044ac358043233015603a9`.
The immutable bytes describe current Live 12, not an identified 12.4.3 revision.
The [source record](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/source.json)
retains anchors for all eight sections. M0003–0142 is chapter prose; following
text includes site navigation and creates no extra device requirement.

[Schema excerpts](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/schema-excerpts.json)
and [shipped preset pins](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/shipped-presets.json)
corroborate package surfaces. Their storage labels and preset values cannot be
used as behavioral enum meanings, defaults or accepted-file promises.
The [packet manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/native-midi-effects/manifest-author-r2.json)
freezes the authored scope for independent review; no release is implied.
