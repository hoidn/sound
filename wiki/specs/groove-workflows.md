---
id: SPEC-GROOVE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentation, exact-build applicability unknown
---

# Groove pool, extraction and application

## Scope and evidence boundary

Canonical F-04 owner for groove loading, pool controls, clip assignment,
extraction, editing and commit. This is a partial draft: D12 means retained
current official Version 12 documentation, and **every exact 12.4.3 behavior
remains U**. Installed schema/AGR files provide S-presence only. No reference,
candidate, extraction algorithm or random generator was executed.

[MIDI editing](midi-editing-tools.md) owns direct note edits and Quantize tool;
[note storage](midi-note-storage.md) owns note fields. [Warp markers](warp-markers.md)
owns marker representation, conversions and existing playback clauses. Groove
application and generation of markers belong here; Warp's piecewise mapping does
not prove groove landmark generation. Container/file management and rack chain
extraction have separate owners. No groove RNG/distribution/interpolation law
is derived from class names or an example preset.

## Inputs, state and comparison

A groove is selected from a valid AGR or extracted from a clip. Its Base is a
musical note division; test times use quarter-note beats (1/8 note = 0.5 beat).
Quantize, Timing, Random, Velocity and Global Amount are displayed percentages;
only explicitly documented domains/endpoints below are contractual. Input clip
notes/transients, playing portion, Warp enablement, groove assignment, shared
pool settings, global amount and committed clip data are separate states.

Cases use reset copies, finite times well away from grid ties and loop boundaries,
and no random component unless specifically requested. They compare note data,
assignment/pool state or marker presence as stated. Audio waveform, timing latency,
unquantized note pairing, velocity-to-gain conversion and tolerances remain U.

## Requirements

All rows are D12 with target U; G locators refer to the analyst appendix.

| ID | Preconditions / inputs | Observable transition and limits | Evidence |
| --- | --- | --- | --- |
| REQ-GROOVE-001 | Drag a library AGR onto a clip; or double-click it in browser. Or select a pooled entry with the Clip Groove chooser. | Dropping assigns/applies groove timing to clip; double-click loads it into Groove Pool before assignment. Pool contains loaded and assigned grooves; unused entries have grayed parameters. Duplicate import/identity handling U. The Clip Groove chooser selects the groove for a clip from entries available in the Groove Pool. | G1–G2; CV:B062 |
| REQ-GROOVE-002 | Assign groove to a MIDI or audio clip. | MIDI supports grooves; audio supports them through Warp and requires Warp enabled. Assignment to unwarped audio has no supported groove effect; exact disable/auto-enable/refusal UI U. | G1 |
| REQ-GROOVE-003 | Use browser view-control entry or Ctrl+Alt+6 (Win)/Cmd+Option+6 (Mac); adjust shared groove control. | Toggle pool visibility. Pool settings can change in real time and affect clips using that groove. Update boundary, automation/mapping and persistence U. | G2 |
| REQ-GROOVE-004 | Select Base 1/4 or 1/8. | Groove note offsets are measured relative to nearest corresponding grid division, affecting assigned clip notes proportionally. A groove note exactly on reference grid contributes no timing offset to its corresponding clip notes. Nearest-grid tie and correspondence rules U. | G3 |
| REQ-GROOVE-005 | Set Quantize before application, Base explicit. | Apply straight quantization before groove: 100% snaps notes to nearest Base positions; 0% keeps original positions at this stage. Partial-amount law, tie and endpoint rounding U. | G3 |
| REQ-GROOVE-006 | Change Timing with all other controls explicit. | Timing controls the groove pattern's timing influence. Zero Timing contributes no pattern timing; exact interpolation, saturation and over-100 behavior U. | G3, G6 |
| REQ-GROOVE-007 | Set Random nonzero on simultaneous voices. | Apply random timing fluctuation separately per voice, allowing formerly coincident notes to separate. No requirement that every realization differs, and no numeric bound, distribution, seed, loop repeat, statistical independence or cross-voice/cross-clip correlation law is supplied. | G3 |
| REQ-GROOVE-008 | Set Velocity within -100..100%. | Velocity controls use of groove velocity information; negative values reverse its emphasis (loud becomes quiet and vice versa). Zero gives no groove velocity influence. Numeric blending, rounding, clipping, audio gain mapping and note-off velocity U. | G3, G6 |
| REQ-GROOVE-009 | Change Global Amount, including 100% or upper endpoint 130%. | Scale Timing, Random and Velocity across all grooves; 100% uses configured values. Quantize is outside this stated scale. Control-bar global slider appears when grooves are assigned to Set clips. Exact composite equation and lower endpoint U. | G3 |
| REQ-GROOVE-010 | Commit groove on assigned MIDI/audio clip. | Write groove result: MIDI notes move; audio obtains Warp Markers at appropriate positions. Assignment then becomes None. Exact note/velocity/marker data, duplicate/endpoint marker policy, random realization, repeat commit and undo scope U. For a groove using positive velocity values, committing to an audio clip creates a volume clip envelope to represent that velocity information as audio volume changes, overwriting a volume clip envelope already in the clip. This named envelope relation supplies no velocity-to-gain, point/curve, marker, sample or timing law. | G4; CV:B064 |
| REQ-GROOVE-011 | Drag AGR from browser or pool into MIDI track. | Create a MIDI clip containing editable groove material; normal MIDI edits apply. Re-extract edited clip to create a groove. Initial naming, track insertion/target conflicts and round-trip normalization U. | G5 |
| REQ-GROOVE-012 | Drag audio/MIDI clip into pool or invoke Extract Groove on clip. | Create a groove using timing/volume information from playing portion only. Transient detection, volume-to-velocity measurement, playing-region endpoint rules, naming and defaults U. | G5 |
| REQ-GROOVE-013 | Set Timing=Random=Velocity=0; adjust Base/Quantize. | Provide real-time nondestructive quantization; groove file contents do not affect this mode. Before commit this is a playback modification, rather than rewriting source note positions. Exact rendered/audio schedule U. | G6 |
| REQ-GROOVE-014 | Enable Hot-Swap above clip Groove chooser and select other grooves while playing; use pool save/hot-swap buttons. | Clip groove can be auditioned by replacement while playing; pool exposes save/hot-swap. Dialog overwrite/cancel, other-clip sharing/duplicate-entry behavior, autosave, media locations and failure recovery U. After enabling Clip Hot-Swap, double-clicking the selected alternative groove or pressing Enter loads it onto the clip and replaces the previously loaded groove in the Groove Pool as well. The source does not specify how other clips or duplicate/shared entry identities change. | G1–G2; CV:B063 |

## Acceptance cases and lifecycle

The current [Groove-only R3 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-cases-r3.json)
contain **GRV-001–034:23 D12 source-context proposals and11 U cases**. The24
original Groove records remain verbatim, including13 old D12 proposals/11 U;
ten source-context cases are appended without new numerical or signal oracles. All
target-build grades U, all unexecuted. GRV-005 uses notes at 0.1/0.6 beats and
Base 1/8 with Quantize 100%, Timing/Random/Velocity zero: documented straight
positions are 0/0.5 beats. GRV-013 compares two distinct groove files with those
same controls, grading equality of quantization only. GRV-007 deliberately has
no fixed random stream or guaranteed separation on an individual trial.
GRV-010 commits the same nonidentity MIDI setup as GRV-005 and compares stored
note starts 0/0.5 beats plus assignment None. Its audio subcase compares only
assignment None; marker count, positions, identity and changes remain U.
Nonzero Timing alone does not guarantee displacement, and an audio clip may
already have appropriate markers before commit.

GRV-007 is U for its numerical/statistical grading criterion. GRV-015–024 enumerate malformed AGR, no-Warp interaction, boundary/tie/negative
time, extraction region edges, save cancellation, undo/redo, save/reopen, deletion
of shared grooves, commit randomness and running transport/teardown. Each stays
ungraded wherever sources omit the outcome. Pool sharing does not specify what
deleting an in-use entry does. Immediate parameter editing establishes neither
atomic cancellation nor an audio-block update guarantee. Disabling Warp during
playback, stopping/deleting a clip and closing the Set need explicit cleanup
evidence before any teardown contract can close.

Remaining required behavior includes AGR variants/validation/migration,
assignment None/default and drag targeting, pool order/rename/delete/multi-edit,
exact full control domains, swing and landmark mapping, durations/expression
carryover, loop scheduling, audio velocity transfer, extracted transient analysis,
groove length/repetition, channel voices and all random-state persistence. These
are unresolved full-product obligations, not removed scope.

## R3 explicit gesture and envelope contexts

Use the [additional future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-fixtures-r3.json)
with independently valid owned groove/clip data, exact offered controls and
explicit Warp/transport/focus/pool/assignment/parameter histories. Before zero,
Warp-off, cancel or no-effect comparisons, independently establish a genuinely
productive matched effect/control operation and active unmuted nonzero output
where relevant. A flag, filename, absent source or failed baseline never passes.
For audio Commit overwrite, confirm positive groove velocity influence and an
identifiable nonflat existing clip-volume envelope; the old Quantize100/Velocity0
MIDI Commit and audio-assignment-only subcases are not that trial. A separate
admitted no-existing-envelope context concerns creation only. No numerical
velocity-to-gain, envelope point/curve, marker, PCM or file/time oracle is added.

| Current case | Audit group | Actual future action subset |
| --- | --- | --- |
| GRV-025 | GSA-G01 | Separate pool visibility menu/platform inputs |
| GRV-026 | GSA-G02 | Actual pool Save versus Hot-Swap before cancel/failure |
| GRV-027 | GSA-G03 | Separate Base1/4 and1/8 contexts; no new numerical comparator |
| GRV-028 | GSA-G04 | Productive Timing/Velocity zero histories; signal oracle null |
| GRV-029 | GSA-G05 | Audio Warp-off after confirmed groove effect; output oracle null |
| GRV-030 | GSA-G06 | Pool versus Control Bar Global Amount inputs |
| GRV-031 | GSA-G07 | Both groove-to-MIDI routes and genuine edited re-extraction |
| GRV-032 | GSA-G08 | Positive-velocity audio Commit creation/overwrite |
| GRV-033 | GSA-G10 | Actually choose a Groove Pool entry in Clip Groove chooser |
| GRV-034 | GSA-G10 | Clip Hot-Swap double-click versus Enter; clip/pool identities |

The [ten-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-adoption-r3.json)
records nine bounded local source subsets. GSA-G09 Random texture advice remains
research-only: no distinct realization, independent stream, seed, distribution,
correlation, threshold or subjective sound grade. REQ007 and GRV007/023 are exact.
Existing aligned1/8 GRV004, finite Quantize/Commit GRV005/010, both extraction
routes GRV012 and two-file nondestructive GRV013 remain exact. Pool Save/Hot-Swap
control presence does not establish file transaction, cancellation or recovery.
Clip Hot-Swap's stated clip/pool replacement does not establish every sharing
clip's assignment, duplicate identity, deletion or merge policy.

The [current actual-status declaration](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-actual-status-r3.json)
keeps all34 target outcomes null/U/unexecuted. Old `expected`/`comparator` strings
are unchanged documentary proposals, not measurements. The ten new cases have
explicit actual-null fields; seven compare only named visible roles and three
have null documentary comparators. The original shared83-case catalog, all MPE27
and Tuning32 records, sources/seals and prior review corrections remain exact.
No Rack-chain extraction case is duplicated; selected Racks022/RCK046 stays its
own bounded owner, distinct from Groove012's Extract Groove operation.

**AS-OF AUTHOR FREEZE:** R3 independent Groove owner review is pending; the
[spec index](index.md) owns current disposition. The reviewed source audit and
its association correction do not self-approve this owner increment. No source,
application, vendor/native function, hardware, network, input or candidate ran.

## Analyst evidence appendix

[Research and exact source hashes](../research/mpe-tuning-grooves.md) and
[source records](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/sources.json)
pin the official Using Grooves HTML and numbered `manual-12-using-grooves.txt`.
Images were not inspected; text from line 74 onward is manual navigation.

| Locator | Exact section / numbered text lines |
| --- | --- |
| G1 | Introduction, 3–13 |
| G2 | `groove-pool`, 14–32 |
| G3 | `adjusting-groove-parameters`, 30–46 |
| G4 | `committing-grooves`, 47–51 |
| G5 | `editing-grooves` / `extracting-grooves`, 52–59 |
| G6 | `non-destructive-quantization`, 68–70 |

Installed schema lines 1246–1248 and 2742–2760 declare groove/assignment/pool
vocabulary. Retained `Quantize 8.agr` is shipped historical content (Creator
Live 10.1.6); its XML note data and pool amounts prove file presence only, not
current decoding or playback behavior. No new file-format owner is created.

Revision 2 applies MTG-REVIEW-001's finite Commit precondition and
MTG-REVIEW-002's nonstatistical wording. Counts are unchanged; the original
revision-1 review packet is retained under the research page's revision archive.

## R3 evidence and preserved history

The [effective source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/groove-source-audit/README-r2.md)
and [independent focused review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/groove-source-audit-review-final.json)
retain32 whole-block assessments, not a per-claim coverage score. SourceVersion12
capture is date-only2026-10-19; exact UTC is unknown. Clip View source062–064,
retained under its original Version12 source identity/captureUTC/hash, supplies
chooser, actual loading and conditional envelope relations. These exact context
pointers are carried by the new cases. Pixels and destinations are uninspected;
no patch12.4.3 parity, default, detection or RNG follows from their names.

[Exact R3 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-delta-r3.json)
refines only001/010/014 and appends ten cases. All61old packet files remain
immutable in place, including archives and old seals/reports; original research
and Groove spec bytes have exact before snapshots. The
[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/groove-manifest-author-r3.json)
pins this partial successor. No current full coverage or handoff release.
