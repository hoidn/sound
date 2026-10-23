---
id: SPEC-GROOVE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
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
| REQ-GROOVE-001 | Drag a library AGR onto a clip; or double-click it in browser. | Dropping assigns/applies groove timing to clip; double-click loads it into Groove Pool before assignment. Pool contains loaded and assigned grooves; unused entries have grayed parameters. Duplicate import/identity handling U. | G1–G2 |
| REQ-GROOVE-002 | Assign groove to a MIDI or audio clip. | MIDI supports grooves; audio supports them through Warp and requires Warp enabled. Assignment to unwarped audio has no supported groove effect; exact disable/auto-enable/refusal UI U. | G1 |
| REQ-GROOVE-003 | Use browser view-control entry or Ctrl+Alt+6 (Win)/Cmd+Option+6 (Mac); adjust shared groove control. | Toggle pool visibility. Pool settings can change in real time and affect clips using that groove. Update boundary, automation/mapping and persistence U. | G2 |
| REQ-GROOVE-004 | Select Base 1/4 or 1/8. | Groove note offsets are measured relative to nearest corresponding grid division, affecting assigned clip notes proportionally. A groove note exactly on reference grid contributes no timing offset to its corresponding clip notes. Nearest-grid tie and correspondence rules U. | G3 |
| REQ-GROOVE-005 | Set Quantize before application, Base explicit. | Apply straight quantization before groove: 100% snaps notes to nearest Base positions; 0% keeps original positions at this stage. Partial-amount law, tie and endpoint rounding U. | G3 |
| REQ-GROOVE-006 | Change Timing with all other controls explicit. | Timing controls the groove pattern's timing influence. Zero Timing contributes no pattern timing; exact interpolation, saturation and over-100 behavior U. | G3, G6 |
| REQ-GROOVE-007 | Set Random nonzero on simultaneous voices. | Add random timing fluctuation independently per voice, allowing formerly coincident notes to separate. No requirement that every realization differs, and no numeric bound, distribution, seed, loop repeat or cross-clip correlation law is supplied. | G3 |
| REQ-GROOVE-008 | Set Velocity within -100..100%. | Velocity controls use of groove velocity information; negative values reverse its emphasis (loud becomes quiet and vice versa). Zero gives no groove velocity influence. Numeric blending, rounding, clipping, audio gain mapping and note-off velocity U. | G3, G6 |
| REQ-GROOVE-009 | Change Global Amount, including 100% or upper endpoint 130%. | Scale Timing, Random and Velocity across all grooves; 100% uses configured values. Quantize is outside this stated scale. Control-bar global slider appears when grooves are assigned to Set clips. Exact composite equation and lower endpoint U. | G3 |
| REQ-GROOVE-010 | Commit groove on assigned MIDI/audio clip. | Write groove result: MIDI notes move; audio obtains Warp Markers at appropriate positions. Assignment then becomes None. Exact note/velocity/marker data, duplicate/endpoint marker policy, random realization, repeat commit and undo scope U. | G4 |
| REQ-GROOVE-011 | Drag AGR from browser or pool into MIDI track. | Create a MIDI clip containing editable groove material; normal MIDI edits apply. Re-extract edited clip to create a groove. Initial naming, track insertion/target conflicts and round-trip normalization U. | G5 |
| REQ-GROOVE-012 | Drag audio/MIDI clip into pool or invoke Extract Groove on clip. | Create a groove using timing/volume information from playing portion only. Transient detection, volume-to-velocity measurement, playing-region endpoint rules, naming and defaults U. | G5 |
| REQ-GROOVE-013 | Set Timing=Random=Velocity=0; adjust Base/Quantize. | Provide real-time nondestructive quantization; groove file contents do not affect this mode. Before commit this is a playback modification, rather than rewriting source note positions. Exact rendered/audio schedule U. | G6 |
| REQ-GROOVE-014 | Enable Hot-Swap above clip Groove chooser and select other grooves while playing; use pool save/hot-swap buttons. | Clip groove can be auditioned by replacement while playing; pool exposes save/hot-swap. Dialog overwrite/cancel, replacement sharing, autosave, media locations and failure recovery U. | G1–G2 |

## Acceptance cases and lifecycle

The authored [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mpe-tuning-grooves/cases.json)
contain **GRV-001–024: 13 D12 field-gradable proposals and 11 U cases**; all
target-build grades U, all unexecuted. GRV-005 uses notes at 0.1/0.6 beats and
Base 1/8 with Quantize 100%, Timing/Random/Velocity zero: documented straight
positions are 0/0.5 beats. GRV-013 compares two distinct groove files with those
same controls, grading equality of quantization only. GRV-007 deliberately has
no fixed random stream or guaranteed separation on an individual trial.

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
