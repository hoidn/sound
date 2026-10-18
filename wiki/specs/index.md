---
id: NAV-SPECS
type: index
status: active
updated: 2026-10-17
access: analysis
---

# Behavioral specification index

Specifications define what must be observable, independent of the original's
internal implementation. This directory contains analyst-side drafts. The
[first configuration release](../../handoff/midi-config-v1/README.md) and its superset
[midi-config-v2](../../handoff/midi-config-v2/README.md) approve
explicitly partial clauses only; REQ-001, REQ-004 and the runtime clauses remain unreleased.

| Page                                                           | Purpose                                                                     |
| -------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [MIDI configuration handoff plan](midi-config-handoff-plan.md) | Finite static-supported release candidate and review gates                  |
| [MIDI configuration v2 handoff plan](midi-config-v2-handoff-plan.md) | Released midi-config-v2 (109 cases): scope, narrowing, traceability |
| [Feature map](feature-map.md)                                  | Whole-app planning inventory and stable feature IDs                         |
| [ALS container](als-container.md) | Revision 1 draft: container recognition, root and version envelope, save envelope; 9 requirements, 27 unexecuted cases, 7 probes |
| [ALS container handoff plan](als-container-handoff-plan.md) | Unreviewed als-container-v1 candidate: partial REQ-ALS-CONTAINER-001 to 006, 35 unexecuted cases; scope, exclusions, traceability, review gates |
| [Transport state](transport-state.md) | Revision 1 draft: 12 requirements (5 static-derived, 6 static with unknown parts, 1 unknown), 23 unexecuted cases for tempo, time signature and loop fields |
| [Plug-in discovery](plugin-discovery.md) | Revision 1 draft: 16 requirements (12 documented or static with unknown parts, 4 unknown), 42 unexecuted cases (6 unresolved) for VST3 and VST2 folders, candidates, change detection and Rescan; crash, hang and batch limit unknown |
| [Browser index](browser-index.md) | Revision 1 draft: 13 requirements (content kinds, tag sidecar read and write format and names, previews, change handling, rebuild); 52 unexecuted cases (24 static-derived, 28 unknown); probes PRB-BI-01 to 05 (proposed), PRB-H2-03 to 06, 09 |
| [Clip launch](clip-launch.md) | Revision 1 draft: 23 requirements (3 documented with static parts, 5 static-derived, 10 static with unknown parts, 5 unknown), 56 unexecuted cases (4 not graded, 2 without a fixture) for stored launch fields, values, load corrections, migration, quantization grid and launch boundary; launch modes, Legato, velocity and follow-action timing open |
| [MIDI note storage](midi-note-storage.md) | Revision 1 draft: 17 requirements (4 without unknown parts, 12 with unknown parts, 1 unknown and excluded) for note structure, load defaults, clamping, time grid, NoteIds, per-note expression and probability groups; 60 unexecuted cases (45 gradable, 6 blocked, 9 unresolved); probes PRB-S7-01 to 10 |
| [Bundled device parameters](bundled-device-parameters.md) | Revision 1 draft: 15 requirements (1 documented only, 2 documented and static, 12 with unknown parts) and tables for the 502 stored parameters of Amp, Cabinet, Analog, Tension, Collision, Electric and Corpus; 37 unexecuted cases (4 not graded); new-instance defaults, out-of-range handling and save output open |
| [Automation envelopes](automation-envelopes.md) | Revision 1 draft: 13 requirements (1 documented and static, 1 static only, 10 with unknown parts, 1 unknown only) for envelope storage, targets, load checks, curves and Float, Bool and Enum evaluation; 31 unexecuted cases (10 unresolved, 1 partly); dangling targets excluded (Q-020); PRB-S6-01 to 07, proposed 08 to 11 |
| [Warp markers](warp-markers.md) | Revision 1 draft: 16 requirements (3 without unknown parts, 11 with unknown parts, 2 unknown): marker storage, shadow marker, empty-list refusal, enumerations, setting domains, scripting sample/beat conversion and edit limits; 35 unexecuted cases (28 gradable, 7 unresolved); probes PRB-S8-01 to 11 |
| [Mixer values](mixer-values.md) | Revision 1 draft: 15 requirements (3 documented and static only, 9 with unknown parts, 1 conditional on Q-019, 2 unknown) for mixer storage, fader curves, dB and pan text, crossfade assign and save text; 45 unexecuted cases (27 static or documented, 11 renders needing measurement, 7 unresolved); probes PRB-S9-01 to 08 |
| [Transport-state handoff plan](transport-state-handoff-plan.md) | Staged transport-state-v1 candidate (18 unexecuted cases): scope, exclusions, traceability, review gates |
| [MIDI user mapping](midi-user-mapping.md) | Revision 3 draft: documented, static, static-conditional and unknown clauses; REQ-005 now carries the native value transforms for all ten map modes; cases MT-01 to MT-23 added (18 static, 5 static-conditional); unexecuted |

**Browse every requirement in one place:** the
[requirements browser](../../analysis/ableton-live-12.4.3/browse/specs/index.html)
lists each draft-spec requirement and each candidate below in one searchable
table, linked back to its source section. Regenerate it with
`python3 tools/spec_browser.py`.

## Candidate specifications

Revision 2 research packets propose candidate requirements from shipped files
and decompiled code. None is a draft spec yet and none is released. The source
section owns the evidence, its strength and the open questions. One row per
target spec:

| Target | Candidates | Source section | Next step |
| --- | --- | --- | --- |
| SPEC-CORPUS-DEVICE | CD-C01–CD-C08 (8) | [Corpus DSP (decompiled)](../research/corpus-dsp-static.md#candidate-requirements-for-spec-corpus-device) | Live-side conversion (N5), then Phase 4 measurements |

When a candidate set becomes a draft under this directory, replace its row
here with the draft's catalog row above.

Author bounded contracts with the [spec template](../../templates/spec.md).
Each future spec gets requirement IDs, a feature-map link, original-side evidence,
and acceptance cases. Add its catalog row here in the same change.

Approved snapshots are listed in the [handoff index](../../handoff/index.md).
Candidate code and design are maintained in [implementation](../implementation/index.md);
original-versus-candidate results are maintained in [verification](../verification/index.md).
