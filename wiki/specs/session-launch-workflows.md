---
id: SPEC-SESSION-LAUNCH-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Version 12 documentary parity unknown
---

# Session launch gestures and Follow Action workflows

## Scope and canonical boundaries

This partial F-04/F-08 draft owns broader documentary runtime roles for launch
modes, Legato, velocity, nudge/scrub and clip/scene Follow workflows. **D12** means
the retained official Version 12 chapter; **every exact 12.4.3 runtime outcome is
U**. It is not a release, compatibility result or complete Session specification.
[Coverage design](../research/full-live-specification-design.md) and
[research](../research/session-launch-workflows.md) govern evidence/limits.
No original application/function, host/emulator, controller or candidate ran.

[Clip launch](clip-launch.md) owns finite storage/enums/load-normalization/grid
clauses and its existing unknown runtime requirements. Specifically:

| Existing canonical requirement | New documentary context only | Exact-target disposition |
| --- | --- | --- |
| `REQ-CLIP-LAUNCH-020` Gate/Toggle/Repeat | Press/release/held input roles below | Remains U; no runtime timing or event matching result |
| `REQ-CLIP-LAUNCH-021` Legato | Same-track play-position takeover role | Remains U; no position/wrap/activation formula |
| `REQ-CLIP-LAUNCH-022` Velocity Amount | Documentary endpoints | Remains U; no launch-velocity gain law |
| `REQ-CLIP-LAUNCH-023` Follow execution | Group/action/enable/time/scene roles | Remains U; no scheduling, chance or jump codec |

[Playback core](playback-core.md) owns finite Trigger/engine dispatch, regions and
stop/fade/output computations, with its own assumptions; they are not transferred
to Follow, scene, Gate/Toggle/Repeat, nudge or scrub. No existing canonical/release is
changed. [Session view](session-view-workflows.md) owns grid/scenes/selection and
cross-view gestures; [Clip View](clip-view-workflows.md) owns region/panel/scrub UI.
[Mapping](midi-user-mapping.md) owns its bounded configuration/takeover; arbitrary
MIDI Learn/user-controller event pairing is not proved. [Arrangement](arrangement-editing.md),
[recording](recording-comping.md), [automation](automation-envelopes.md),
[media](media-file-workflows.md), [warp](warp-markers.md), [MPE](mpe-workflows.md)
and [transport](transport-state.md) retain their bounded scopes.

The ten action-role names use the
[released stored enum vocabulary](../../handoff/clip-launch-v2/spec.md#req-clip-launch-007--partial-follow-action-values)
only as vocabulary. That release specifies stored values, not the label set shown
in every UI or runtime action mapping. Several action labels in current source
are inline images. Figures were not inspected, and no label is recovered from
image filenames/alt text. Descriptive prose supports role contracts below;
exact image/label-to-source/runtime association remains U.

## State, preconditions and oracles

[Finite setups](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/fixtures.json) require retained selected/playing clip
and scene identities, active valid source/output, region/loop/tempo/meter/mode,
quantization/Clip Update Rate, mapping/focus and local/global Follow state.
Every Follow probe requires both local and global enable, valid occupied clip
groups or populated scene targets, accepted timing values, nonzero source/gain and
an independently audible/observable paired positive baseline. A disabled source,
zero chance, empty target, muted output or missing mapping never establishes no
processing. No-action/Stop/disable tests change only their explicit tested state.

All cases have target `expected:null`, `comparison:null`, `target_grade:U` and
`executed:false`. Documentary visible-control/state proposals have separate
comparators; **signal, timing, RNG, launch/Follow event outcomes are ungraded/null**.
Their retained `source_claim` is source prose, not an output oracle. No launch
grid arithmetic, normalization equation, RNG distribution/seed/independence,
finite-success deadline, MIDI codec, velocity/gain formula, Legato wrap, frame
ordering, tolerance or candidate architecture is invented.

## Documentary requirements and cases

Bare first-column IDs are discoverable with the existing requirements browser.
Each D12 row has one same-number `SLC-NNN` case with concrete settings/actions.

| Requirement | Documentary role and limits | Source blocks |
| --- | --- | --- |
| REQ-SESSION-LAUNCH-001 | Session launch setting scope: Launch settings apply to Session clips, not Arrangement timeline clips. Session Clip View exposes them; multi-selection supports editing launch settings together. Shared panel/grid selection belongs to existing owners. | `LC-B004`, `LC-B005`, `LC-B006` |
| REQ-SESSION-LAUNCH-002 | Trigger gesture role: Trigger: down starts clip; release is ignored. The source covers mouse, key and mapped MIDI-note gesture categories but supplies no dispatch/frame/note-off matching law. | `LC-B008`, `LC-B009` |
| REQ-SESSION-LAUNCH-003 | Gate gesture role: Gate: down starts and up stops. Exact quantized release, held/repeated MIDI pairing and cancellation remain U. | `LC-B008`, `LC-B010` |
| REQ-SESSION-LAUNCH-004 | Toggle gesture role: Toggle: down starts, up is ignored, next down stops. Multiple input-source arbitration and grid-boundary timing remain U. | `LC-B008`, `LC-B011` |
| REQ-SESSION-LAUNCH-005 | Repeat gesture role: Repeat retriggers while input remains held at clip quantization rate. None/Global edge behavior, first/last repeat and exact timing are not supplied. | `LC-B008`, `LC-B012` |
| REQ-SESSION-LAUNCH-006 | Legato takeover role: Launching Legato clip takes previous clip play position in same track, including with quantization off. Position units, wrap, unequal lengths and activation timing are unproven for target. | `LC-B014`, `LC-B015`, `LC-B016` |
| REQ-SESSION-LAUNCH-007 | Legato media and RAM context: Different-sample Legato jumps may cause dropouts because material was not preloaded; Clip RAM is documented as remedy. This is no zero-dropout, deadline or RAM/disk-load guarantee. | `LC-B017` |
| REQ-SESSION-LAUNCH-008 | Quantization selector roles: None disables launch onset correction; Global selects Control Bar quantization. Existing enum/grid/Trigger arithmetic retains its canonical owner and assumptions; Follow Action Global behavior is separately unresolved. | `LC-B019`, `LC-B020` |
| REQ-SESSION-LAUNCH-009 | Launch velocity endpoints: Velocity Amount0 gives no launch-note-velocity volume influence;100% says softest notes play silently. Softest valid launch velocity, interpolation, volume codec and non-MIDI launch response remain U. | `LC-B023` |
| REQ-SESSION-LAUNCH-010 | Nudge role: Nudge Backward/Forward jumps within playing clip by global quantization period. Source/file/loop bounds, None behavior and exact rounding remain U. | `LC-B025` |
| REQ-SESSION-LAUNCH-011 | Nudge and scrub mapping affordances: Nudge buttons can map to keys/MIDI; MIDI Map Mode reveals a scrub control between buttons for rotary-encoder continuous scrubbing. Mapping codec/takeover/relative interpretation remains outside this clause. | `LC-B026` |
| REQ-SESSION-LAUNCH-012 | Offset relative to master clock: Sub-bar quantization plus launch, nudge or scrub can offset clip playback relative to master clock. It does not specify a phase-offset equation or reset law. | `LC-B027` |
| REQ-SESSION-LAUNCH-013 | Clip Follow groups: Clip Follow Actions operate within successive occupied slots on one track; empty slots separate groups. Group definition here is clips, not a proven scene-group/empty-scene rule. | `LC-B029` |
| REQ-SESSION-LAUNCH-014 | Scene Follow entry and local enable: Follow Actions also have Scene View controls. Selected clip/scene local Follow button enables/disables them; source describes default disabled and Shift+Enter toggle. Actual constructor/focus/default-load state remains U. | `LC-B030`, `LC-B031` |
| REQ-SESSION-LAUNCH-015 | Two action choices: Each clip/scene exposes two Follow Action choices, A and B. Exact labels/images versus stored-code associations stay with scoped enum evidence and U control-context work. | `LC-B032` |
| REQ-SESSION-LAUNCH-016 | Chance endpoints: The source says A 100%/B 0% selects A every launch and0% suppresses its action. The later B 90%/~one-in-ten example leaves actual coupled-field changes unspecified; no general probability or normalization law follows. | `LC-B033` |
| REQ-SESSION-LAUNCH-017 | Linked versus scene eligibility: Linked/Unlinked is clip-only; Linked is described as default. Follow Time is exposed for both clips and scenes. No saved-field/default constructor parity is inferred. | `LC-B034` |
| REQ-SESSION-LAUNCH-018 | Linked timing role: Linked clip Follow occurs at clip end or after number of loops in Multiplier. Which region/end/loop accounting, nonlooped clips and clock rounding require target evidence. | `LC-B034` |
| REQ-SESSION-LAUNCH-019 | Unlinked Time role: Unlinked clip Follow uses duration in Follow Time; clip/scene Time is bars-beats-sixteenths from point where play starts. Default one bar and editor marker drag are documentary only; exact meter/offset codec remains U. | `LC-B034` |
| REQ-SESSION-LAUNCH-020 | No-follow role: The no-follow description says no Follow occurs; once clip is triggered with No Action, other selected Follow Action in that clip no longer gets a chance even if its Chance100%. Re-launch/re-enable/reset scope remains U. | `LC-B036` |
| REQ-SESSION-LAUNCH-021 | Stop role: Stop description stops clip after chosen Follow Time, overriding clip loop/region settings. Exact linked/unlinked preconditions, stop grid and note/tail cutoff are U. | `LC-B037` |
| REQ-SESSION-LAUNCH-022 | Restart role: Restart description restarts clip; start marker, Legato interaction, repeat counters and exact dispatch are not provided. | `LC-B038` |
| REQ-SESSION-LAUNCH-023 | Previous role: Previous description triggers clip immediately above current. Top-of-group wrap or escape across empty slot is not documented here. | `LC-B039` |
| REQ-SESSION-LAUNCH-024 | Next and clip wrap: Next description selects next clip down within group; last clip wraps to first. This clip statement is not applied automatically to scene-empty-group boundaries. | `LC-B040` |
| REQ-SESSION-LAUNCH-025 | First role: First description launches top clip in group. Exact empty-slot/reordering/concurrent group edits remain U. | `LC-B041` |
| REQ-SESSION-LAUNCH-026 | Last role: Last description launches bottom clip in group; self-target behavior when already last remains unresolved. | `LC-B042` |
| REQ-SESSION-LAUNCH-027 | Any role: Any description permits any clip in group; source gives no uniformity, independence, seed, repeat history or finite completion guarantee. | `LC-B043` |
| REQ-SESSION-LAUNCH-028 | Nonconsecutive role: Other-like description excludes consecutive same clip while current clip is not alone in group; singleton exception does not establish a specific fallback/retrigger law. | `LC-B044` |
| REQ-SESSION-LAUNCH-029 | Jump selector role: Jump exposes Jump Target slider for target clip slot or scene; drag or numeric entry adjusts target. UI numbering, stored jump fields, invalid/empty target behavior and action/image associations remain U. | `LC-B045` |
| REQ-SESSION-LAUNCH-030 | Assigned Follow indicator: Clips/scenes with assigned Follow Actions show striped launch buttons. Assigned versus enabled versus stored default fields is unresolved control context. | `LC-B046` |
| REQ-SESSION-LAUNCH-031 | Global Follow enable: Enable Follow Actions Globally governs all clip and scene Follow Actions. Source says grayed when Set contains none; which fields count as present versus assigned/enabled remains U. | `LC-B048` |
| REQ-SESSION-LAUNCH-032 | Scene precedence role: Clip Follow continues while scene Follow is created/scheduled; scene Follow takes precedence once triggered. Exact same-time priority, affected tracks and pending-request cancellation are U. | `LC-B049` |
| REQ-SESSION-LAUNCH-033 | Cycle construction role: Source describes Next cycles of clips or scenes and occasional alternatives using lower relative chances. This is no general scene-group/wrap or RNG law. | `LC-B060`, `LC-B061` |
| REQ-SESSION-LAUNCH-034 | Create Follow Action Chain: Clip context Create Follow Action Chain sets selected clips to cycle; selection need not be contiguous. Generated action codes, order, times, chances, enable flags and gap crossing are not specified. | `LC-B062` |
| REQ-SESSION-LAUNCH-035 | Intro into loop composition: Documented recipe splits nonlooped introduction from looping tail, places adjacent Session clips, sets first Next 100 and Time to first duration, second Loop on. Editing/transfer owners retain their own laws; exact derived timing remains U. | `LC-B053`, `LC-B054`, `LC-B055`, `LC-B056`, `LC-B057`, `LC-B058` |
| REQ-SESSION-LAUNCH-036 | Temporary restart composition: Single-clip Play Again 80/No Action 20 example restarts a portion and may later continue; the source eventual-language supplies no bounded-trial deadline or finite guarantee. A subsequent looping clip can have separate Follow configuration. | `LC-B065`, `LC-B066` |
| REQ-SESSION-LAUNCH-037 | Legato Follow variation role: Legato Follow can transfer beat-time position among similar clips with differing settings/envelopes/notes. This describes composed roles, not audible identity or complete automation/warp interaction. | `LC-B068`, `LC-B069` |

## Required unknowns and lifecycle

| Requirement | Required unresolved behavior | Finite case IDs |
| --- | --- | --- |
| REQ-SESSION-LAUNCH-U-GLOBAL-FOLLOW | Global Follow quantization wording is unresolved between LC-B021 and LC-B047; no rule is selected. | `SLC-U-GLOBAL-FOLLOW`, `SLC-U-GLOBAL-UI` |
| REQ-SESSION-LAUNCH-U-CHANCE-COUPLING | Chance A/B coupled editing, actual fields and probability/RNG law remain unknown. | `SLC-U-CHANCE-UI`, `SLC-U-CHANCE-TRACE` |
| REQ-SESSION-LAUNCH-U-ACTION-CONTEXT | Image/label/action identity and target control contexts remain unknown beyond released stored enum vocabulary. | `SLC-U-ACTION-LABELS`, `SLC-U-ENABLE-INDICATORS` |
| REQ-SESSION-LAUNCH-U-BOUNDARIES | Region/group/target/time endpoints and ordering require exact target evidence. | `SLC-U-GROUP-BOUNDARY`, `SLC-U-JUMP-BOUNDARY`, `SLC-U-TIME-BOUNDARY`, `SLC-U-PRESS-BOUNDARY`, `SLC-U-SCENE-BOUNDARY` |
| REQ-SESSION-LAUNCH-U-CLIP-LIFECYCLE | Clip-specific automation, storage/error/cancel/rate/teardown remain required unknowns. | `SLC-U-CLIP-AUTOMATION`, `SLC-U-CLIP-TRANSPORT`, `SLC-U-CLIP-PERSISTENCE`, `SLC-U-CLIP-UNDO`, `SLC-U-CLIP-MALFORMED`, `SLC-U-CLIP-CANCEL`, `SLC-U-CLIP-SOURCE-LOSS`, `SLC-U-CLIP-TEARDOWN`, `SLC-U-CLIP-RATE`, `SLC-U-CLIP-OUTPUT` |
| REQ-SESSION-LAUNCH-U-SCENE-LIFECYCLE | Scene-specific automation, storage/error/cancel/rate/teardown remain required unknowns. | `SLC-U-SCENE-AUTOMATION`, `SLC-U-SCENE-TRANSPORT`, `SLC-U-SCENE-PERSISTENCE`, `SLC-U-SCENE-UNDO`, `SLC-U-SCENE-MALFORMED`, `SLC-U-SCENE-CANCEL`, `SLC-U-SCENE-SOURCE-LOSS`, `SLC-U-SCENE-TEARDOWN`, `SLC-U-SCENE-RATE`, `SLC-U-SCENE-OUTPUT` |

Clip and scene lifecycle groups have separate automation, transport, persistence,
undo, malformed, cancellation, source-loss, teardown, rate and output cases. Boundary
cases add group gaps/reorder/delete, Previous-at-top, singletons, self-target, Jump
empty/invalid indices, Time/Multiplier endpoints, held/released gesture races and
scene/clip/global simultaneity. No malformed/cancel/teardown kind is declared
inapplicable. Work uses disposable owned state; inputs, old Sets and runtime logs
are future prerequisites, not supplied fixtures. Common flags never substitute
for a per-case valid/active/nonzero positive path.

## Source-context questions

**SLC-U-GLOBAL-FOLLOW:** LC-B021 (§16.4) says any non-None clip setting quantizes
Follow launches, which includes Global. LC-B047 (§16.7) says Follow circumvents
Global while explicit non-None/non-Global quantization can apply. Matching runtime
mode/preconditions are unproven. Both statements remain retained; neither is
chosen. Trigger/grid arithmetic and stored enum values do not settle this path.
Root links the shared [Q-030](../questions.md) context; its unresolved target state
is unaffected by this documentary draft.

**SLC-U-CHANCE-COUPLING:** LC-B033 starts A 100/B 0, then says changing B 90 makes A
occur approximately one time in ten. It omits whether A changes through coupled
UI controls and which values are actually stored. No A=10, A=100,100/(100+90),
normalization equation or general probability law follows. Existing load-time
chance rescaling is a separate, unchanged contract. Finite traces establish no
uniformity, independence or guaranteed eventual branch. LC-B065 and LC-B073
examples do not guarantee termination or nonrepetition within bounded trials.

**SLC-U-ACTION-CONTEXT:** Exact label sets/image associations, assigned versus
enabled/default state, global graying criteria, Shift+Enter focus, scene grouping,
Jump UI indexing and created-chain fields remain required U. Next's documented
clip last-to-first wrap is not a Previous-wrap or scene-empty-group law.
Scene precedence after trigger does not settle same-sample tie/cancellation.

## Acceptance counts and evidence

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/requirements.json) and [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/cases.json)
contain 43 requirements (37 D12, 6 U) and 68 unexecuted cases
(37 D12, 31 U). Zero target grades. Positive-control and compound case recipes
are finite investigation coverage, not complete mode/event-combination acceptance.

[Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/source.json) retains official
[Launching Clips chapter](https://www.ableton.com/en/live-manual/12/launching-clips/),
captured 2026-10-19T21:43:52.559317+00:00,262,997 bytes, SHA-256
`dc9c4e21a480e1adeeb2daf548d34547ccb73153a2561fb93f56391f003a82af`.
[73 root-retained blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/source-blocks.json) name exact HTML line and
heading anchor;[text](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/source-blocks.txt) is navigation only.
[HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/manual-launching-clips-2026-10-19.html) is immutable source.
[Initial-input pins](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/resumed-inputs.json) preserve all four pre-author
files byte-for-byte; there was no recapture or image inspection.
[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/manifest-author-r1.json) freezes payloads/canonical snapshots;
[validation](../../analysis/ableton-live-12.4.3/full-spec-v1/session-launch-workflows/validation-author-r1.json) checks source/count/case/browser/
link/hash/whitespace scope only. All analysis links require sanitization/review
before handoff. No profile/family completion is claimed.

## Revision and handoff

Revision 1 is author-frozen for independent semantic review. Existing canonical
requirements/releases and shared catalogs, questions, plan/log are not edited.
