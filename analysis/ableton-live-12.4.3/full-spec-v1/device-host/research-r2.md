---
id: RESEARCH-DEVICE-HOST-PROTOCOL
type: research
status: draft
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3 macOS arm64
revision: 2
---

# Bundled-device processing protocol

This page owns the remaining Live-side processing boundary in [Q-025](../questions.md#q-025-device-host-protocol-and-device-audio-acceptance).
[N5](device-parameter-mapping-native.md) owns bundle loading, capabilities and parameter mapping;
[N6](device-tables-native.md) owns the nested parameter tables. The existing
[extracted DSP study](device-dsp-extracted.md) and individual device pages own bundle-side audio.
The [hosting draft](../specs/bundled-device-hosting.md) retains application gaps and
one conditional settled mixing law. Recovered intermediate transformations below
are non-normative component models, excluded from application compatibility coverage.
Common device-chain/rack editing belongs to [racks](../specs/device-racks.md).

## Evidence and method

Static read-only inspection on 2026-10-19 of retained Ghidra 12.1.4 exports for
`Live.arm64`, SHA-256 `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad`,
image base `0x100000000`, macOS arm64, Live 12 Suite 12.4.3. No original code,
application, candidate or harness was executed. No Ghidra project was mutated.
The [packet](../../analysis/ableton-live-12.4.3/full-spec-v1/device-host/README.md)
retains **51 unchanged JSONL source records**, source-line/record/code digests,
corpus-run metadata and the existing H4 bundle identities and N5 manifest.
`record-locators.json` identifies each original chunk and line; `live-records.jsonl`
line numbers below refer to immutable retained records. Source records are original
exports, not analyst reconstructions. Only `capture.py`, notes, case vectors and
manifest are analyst-authored. H4's full bundle identities remain canonical; the
packet copy pins the seven executable/slice identities without restating them here.

Every finding below is **Observed in static code (S)** unless labelled inferred or
unknown. A function's presence does not show when an audio scheduler invokes it.
Decompiler signatures are imperfect: the split helper has stack-probe recovery,
and the processing wrapper is typed `void` although a caller consumes its result.
These limitations specifically block an exact activity/stop contract and arbitrary
block sizes. The finite transformations below are conditional on the stated path.

## Signal preparation and host mixing

`0x102fc0e2c` (record 39) chooses instrument processing for input-role 1 and
an effect path for role 2. H4/N5 establish instrument/effect applicability.
`0x102fc070c` (37) copies both source channels into the effect's working output
buffers when both input pointers exist, otherwise zeros both. Its initial activity
flag is **input presence**, not a scan for nonzero samples. Therefore a supplied
all-zero stereo buffer and absent input are different boundary inputs. Instruments
instead initialize the flag from queued-event count; their working output is not
filled from the audio input on this branch. In-place buffers alone do not imply
that a stopped effect is always called.

Amp/Cabinet's dual-instance capability selects `0x102fc0294` (35) when DualMono
is enabled: independent left and right processing with the same event/transport
context; activity is ORed. Disabled DualMono uses `0x102fc04dc` (36): the wet input
is `(L+R)/2`, processed once, then used for both wet channels. Original dry stereo
remains available to the mix. The flag still reflects both inputs being present.
This establishes signal preparation; it supplies no Amp/Cabinet DSP output.

Those two paths call `0x101df082c` (7) for host dry/wet mixing. At a settled control
value d, wet weight is `sin(d*pi/2)` and dry weight is
`sqrt(1-wet_weight^2)`, with separate original L/R dry samples. The transition uses
an iterative update and a 0.001 control step per sample; do not substitute a
linear crossfade or claim a sample-exact transition from this draft. N5 owns how
stored DryWet reaches this control; `OnDryWet` (49) forwards into its setter.
Corpus's own DryWet is a bundle parameter, not this Amp/Cabinet host crossfade.

## Parameter delivery and processing boundaries

`OnParameter` (45; duplicate body 30) stores the last value for each index and
records first-seen index order. An entry is accepted only with an existing primary
instance, index below 256 and fewer than 256 distinct pending entries. At full
capacity even a repeated index is ignored because the count guard precedes lookup.
`0x102fbfe54` (32) delivers that order to primary and any secondary instance, then
clears the pending entries/count. For the reset-capable group it also remembers
index 0. These are queue observations, not a claim that UI automation is sampled
only once per audio block.

`0x102fc0a38` (38) normally flushes before processing. For the reset-capable group,
more than 10 pending distinct values instead select a grouped-change path; active
processing starts a fade of `int(0.03 * sample_rate)` frames, otherwise dispatch
begins immediately. `0x102fbf9a0` (27) transfers pending values into another queue,
disables processing and posts reset/dispatch work. Resume handlers (19/21) re-enable
or repeat the sequence. Scheduler timing, observed interruption duration and
which user edits cross this threshold remain unknown. No compatibility requirement
requires a 10-entry queue, fade implementation or original call sequence.

## Events and partitioning

`0x102fbfb5c` (28), gated by readiness and device On, accepts logical event types
1/2/6, and type 3 with controller code -2, -1, 1, 64, 74 or 120. The bit mask is
`0x100000000000401` after subtracting 64. Other logical types/codes are not queued
by this path. Queue capacity is 4,096 events; subsequent arrivals are ignored.
Accepted events trigger processing activity. These are logical-event filter
observations, not a claim that MIDI transformations before this path are absent.

The queue uses `0x101ab4ee4` (4) → `0x101a541a4` (2) for the current scheduler offset
and `0x101b4456c` (5) for MIDI-byte conversion. Notes use note-on/note-off status
with channel nibble, pitch byte and converted velocity; type 6 becomes CC123=0.
The scheduler offset's origin is **unknown**: neither this getter nor copying it
establishes whether Live's event coordinate starts at 0 or 1. This packet does
not settle fractional velocity rounding across the whole event path, MPE, channel
remapping or Corpus's MIDI side-chain routing.

When a processing request exceeds the capability maximum, `0x102fbe73c` (13) and
inline copies choose a split helper `0x102fbe964` (15). For a supported request of
1,024 frames with a 512-frame maximum, the helper processes two subblocks. Events
strictly before each subblock end are copied and their timestamp is reduced by
that subblock's start. Thus event coordinate 512 belongs to the second subblock
at 0; 511 belongs to the first at 511. This translation preserves coordinates;
it does not determine their original time base. The local event limit is 2,048
per subblock; overflow behavior is incompletely characterized because the source
cursor advances past the entire selected range. Events must already be ordered
for the binary search to be meaningful; upstream ordering was not proved.

The caller calculates a quotient `frames / maximum`; no remainder path is present
in the exported split helper. Its decompile has stack-probe recovery. Therefore
non-multiple request sizes, zero maximum and invalid sizes remain **U**, not an
inferred claim that Live drops audio. The real scheduler may constrain requests;
this packet has not established that constraint.

## Transport context

The pre-buffer callback `0x102fcce00` (50) copies playing state, position and tempo
from scheduler status; tempo is converted binary32→binary64. It also supplies loop
start/end and loop-enabled state. Field semantics follow the bundle-side context
in the DSP study, but the scheduler status producer is not fully traced.

For each split subblock, record 15 leaves position unchanged while stopped. While
playing it advances position by `tempo * start_frame / (sample_rate * 60)`.
**Inferred unit:** quarter-note beats, consistent with the formula; no independent
scheduler-unit proof is retained here. If looping is enabled and the subblock
advance crosses the copied loop end, a helper adjusts the position. Its exact
boundary/modulo rule is **U**. Non-normative numeric model vectors below deliberately
avoid loop crossings. No wall-clock, tempo-change or transport-jump latency follows.

## Initialization, reset, sample rate and teardown

Initialization and loading remain owned by N5. This packet adds:

- `NewRate` (31/44): if a primary exists, temporarily disables readiness, stores
  the new rate in primary and secondary, delivers rate updates to both, resets
  both, re-delivers cached index 0 to the primary for the reset-capable group,
  clears queued events and restores prior readiness. Return values of rate/reset
  calls are not used here. Which notes are re-sent by upstream scheduling is U.
- Ordinary `Reset` (26/42): resets primary and secondary and restores cached
  index 0 for the reset-capable primary. **No warm-up is called on this path.**
- `ResetAndDispatch` (18→20): flushes the transferred parameters; for reset-capable
  engines calls `0x102fbff98` **four times**, first with an event, next three with
  no events; then resets primary, re-delivers index 0 and resets secondary.
  Each warm-up helper invocation requests 1,024 frames (33), split into two
  512-frame calls for the five non-Softube devices. Total is therefore 4,096
  warm-up frames on this path, not 1,024. Its synthetic event constructor (6)
  is retained, but its exact semantic identity is not assigned here.
- `Exit` (25/41) disables readiness, marks exit and unregisters pre/post callbacks.
  The destructor (24) destroys each extant engine, frees its wrapper and decrements
  the shared loader count. When it reaches zero `0x102f999fc` (8) clears export
  pointers and releases the CFBundle. This is static resource teardown, not proof
  of a particular device-delete sound or UI timing.

**Correction to earlier summaries:** N5's capability table and the DSP study's
“How Live drives a bundle” shorthand must not be read as a single universal
1,024-frame reset sequence. The retained N5 record of `0x102fbff98` remains correct
per helper invocation. Records 20, 26 and 44 establish distinct reset paths and
four helper invocations in the dispatch path. Old extracted tests using 1,024
warm-up frames remain exactly those tests; they do not become 4,096-frame tests
and are not invalidated as finite extracted evidence. Application initialization,
new-rate/reset renders and grouped-change renders remain ungraded until separately
supported. Root integration owns the backlinks/correction notices in N5 and the
DSP overview; this new page owns the expanded finding.

## Activity, failures and remaining questions

The call wrapper (14) converts a boolean input flag to an integer for processing,
converts the output back to boolean and returns success separately. The split
helper (15) ORs subblock activity and success separately, starting every subblock
with the original input-present flag. Effect paths (35–37) return activity.
Processing (39) stores activity for post-buffer notification (51). `CalcMain`
(43) gates further work using On/input state, a change/event flag, previous output
state, fade state and dry/wet smoothing state. It clears its output reference
when processing is unavailable or inactive. Therefore “Live always ignores the
flag” is unsupported; “flag 0 always stops processing immediately” is also
unsupported. Return-type recovery in records 39/43 and upstream scheduler/input
flags keep exact stop/restart and tail preservation **U**.

N5 still owns load/error findings. This trace does not prove missing-bundle output,
notice text, retry timing, a null create-result outcome, crash isolation, unsupported
sample-rate handling, or user-visible deletion/cancellation. Full host conformance,
all seven devices' DSP and Q-025 remain open. Amp/Cabinet emulation/fake identity
remains deferred by user; T1.6 remains pending. No clean implementation is authorized
by these analyst findings.

## Non-normative component model checks

Independent review [BDH-REVIEW-001](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/device-host-review.json)
confirmed these static transformations but rejected their r1 classification as
application compatibility cases. The observer boundary was analyst-selected:
prepared channels, delivery order/count, subblock context and one cleared queue
are not independently established external inputs/outputs. Renaming them logical
values does not change that limitation. These 11 finite derivations remain useful
source/model checks, never required candidate interfaces, graded application cases
or covered application requirements. Corresponding spec case IDs remain U.

The inputs assume the selected internal path; controls exclude grouped changes
and 256-entry capacity; events are ordered, within range, at most 2,048 per
subblock, and split into exact 512-frame multiples; transport has explicitly
supplied numeric context and no loop crossing. Those constraints explain the
model derivation only. They do not prove a public scheduling interval or frame base.

| Model check | Analyst-supplied component input | Statically derived intermediate result; non-normative |
| --- | --- | --- |
| BDH-001 | Corpus, present Left=[1,-1], Right=[0.25,-0.25] | Prepared channels equal each respective input; present=true |
| BDH-002 | Corpus, both channels present and [0,0] | Prepared zeros; present=true |
| BDH-003 | Corpus, Left=[1,1], Right absent | Both prepared channels [0,0]; present=false |
| BDH-004 | Amp/Cabinet DualMono=true; L=[1,-1], R=[0.25,-0.25] | Independent wet inputs [1,-1] and [0.25,-0.25] |
| BDH-005 | Same with DualMono=false | Mono wet input [0.625,-0.625], same wet result for both channels |
| BDH-006 | DualMono=false; L=[1], R=[-1] | Wet input [0]; original dry inputs retained as [1],[-1] |
| BDH-010 | Pending A=0.1, B=0.2, A=0.3; normal delivery | A=0.3 then B=0.2, once each; same values for any secondary processor |
| BDH-011 | Immediately deliver again with no new control | Empty control delivery |
| BDH-012 | N=1024,max=512; ordered note actions at coordinates 0,511,512,1023 | First range coordinates [0,511]; second [0,511]; note payload/order unchanged |
| BDH-013 | fs=48000,N=1024; Position=4,Tempo=120; substart=512; Playing=1 then 0; no loop | Playing case Position=4+8/375; stopped case=4; tempo and playing preserved |
| BDH-014 | Existing engine, queue note-on pitch60 at coordinate100; rate notification 44100→48000 before delivery | New processing rate 48000; that queue delivers no note-on |

The three settled DryWet arithmetic vectors BDH-007–009 remain in the draft as
conditional output-composition checks. Their wet samples and finite tolerance
are project choices, not captured Amp/Cabinet DSP. They establish no application
or full-device audio pass. All application reset, activity, scheduler, failure,
removal and rate-change continuity cases remain ungraded.

## Validation and review boundary

The capture self-check asserts the pinned corpus identity, 51 unique requested
records, unchanged source record bytes, code digests and no timed-out/partial
records. Its first invocation had an analyst path error before copying H4/N5
metadata; correcting the packet-relative root and rerunning completed capture.
No reference failure was involved. The revision 2 packet manifest pins authored
page snapshots for focused re-review.
Revision 1 seal and all its payloads are retained unchanged under `revisions/r1/`;
the original 51 JSONL source records and newline-inclusive hashes are unchanged.
The revised classification is 12 requirements (1 conditional S,11 U), 26 case
entries (3 conditional S arithmetic,23 U application) and 11 non-normative model
checks excluded from compatibility coverage. No original application/candidate
case passed. Findings BDH-REVIEW-001/002 are addressed in this revision; acceptance
remains for the separate reviewer. Root integration owns indexes, coverage, Q-025
and append-only log entries. This is a useful partial protocol draft, not whole-host closure.
