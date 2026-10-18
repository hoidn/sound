---
id: NAV-SPECS
type: index
status: active
updated: 2026-10-18
access: analysis
---

# Behavioral specification index

Specifications define what must be observable, independent of the original's
internal implementation. This directory contains analyst-side drafts. Thirteen
reviewed releases approve explicitly partial clauses only. The
[handoff catalog](../../handoff/index.md) lists them. The MIDI configuration line is
[midi-config-v1](../../handoff/midi-config-v1/README.md), then
[v2](../../handoff/midi-config-v2/README.md), then
[v3](../../handoff/midi-config-v3/README.md); MIDI REQ-001, REQ-004 and the runtime
clauses remain unreleased. The other ten are one release per draft spec below:
transport-state-v1, als-container-v1 and the eight revision 1 releases of
2026-10-18. Each handoff plan's review outcome lists the corrections owed to its
draft spec.

| Page                                                                 | Purpose                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [MIDI configuration handoff plan](midi-config-handoff-plan.md)       | Finite static-supported release candidate and review gates                                                                                                                                                                                                                                                                                                |
| [MIDI configuration v2 handoff plan](midi-config-v2-handoff-plan.md) | Released midi-config-v2 (109 cases): scope, narrowing, traceability                                                                                                                                                                                                                                                                                       |
| [Feature map](feature-map.md)                                        | Whole-app planning inventory and stable feature IDs                                                                                                                                                                                                                                                                                                       |
| [ALS container](als-container.md)                                    | Revision 2 draft: container recognition, root and version envelope, save envelope; 9 requirements, 27 unexecuted cases, 7 probes; partial 001 to 006 released as als-container-v1 |
| [ALS container handoff plan](als-container-handoff-plan.md)          | Released als-container-v1 (35 cases, approved with narrowing): scope, exclusions, traceability |
| [Transport state](transport-state.md)                                | Revision 2 draft: 12 requirements (3 static-derived, 8 static with unknown parts, 1 unknown), 22 unexecuted cases for tempo, time signature and loop fields; 18 released as transport-state-v1 |
| [Plug-in discovery](plugin-discovery.md)                             | Revision 1 draft: 16 requirements (12 documented or static with unknown parts, 4 unknown), 42 unexecuted cases (6 unresolved) for VST3 and VST2 folders, candidates, change detection and Rescan; crash, hang and batch limit unknown; partial clauses released as [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) (35 cases) |
| [Browser index](browser-index.md)                                    | Revision 1 draft: 13 requirements (content kinds, tag sidecar read and write format and names, previews, change handling, rebuild); 52 unexecuted cases (24 static-derived, 28 unknown); probes PRB-BI-01 to 05 (proposed), PRB-H2-03 to 06, 09; partial clauses released as [browser-index-v1](../../handoff/browser-index-v1/README.md) (26 cases) |
| [Clip launch](clip-launch.md)                                        | Revision 1 draft: 23 requirements (3 documented with static parts, 5 static-derived, 10 static with unknown parts, 5 unknown), 56 unexecuted cases (4 not graded, 2 without a fixture) for stored launch fields, values, load corrections, migration, quantization grid and launch boundary; launch modes, Legato, velocity and follow-action timing open; partial clauses released as [clip-launch-v1](../../handoff/clip-launch-v1/README.md) (50 cases) |
| [MIDI note storage](midi-note-storage.md)                            | Revision 1 draft: 17 requirements (4 without unknown parts, 12 with unknown parts, 1 unknown and excluded) for note structure, load defaults, clamping, time grid, NoteIds, per-note expression and probability groups; 60 unexecuted cases (45 gradable, 6 blocked, 9 unresolved); probes PRB-S7-01 to 10; partial clauses released as [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md) (67 cases) |
| [Bundled device parameters](bundled-device-parameters.md)            | Revision 1 draft: 15 requirements (1 documented only, 2 documented and static, 12 with unknown parts) and tables for the 502 stored parameters of Amp, Cabinet, Analog, Tension, Collision, Electric and Corpus; 37 unexecuted cases (4 not graded); new-instance defaults, out-of-range handling and save output open; partial clauses released as [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) (82 cases) |
| [Automation envelopes](automation-envelopes.md)                      | Revision 1 draft: 13 requirements (1 documented and static, 1 static only, 10 with unknown parts, 1 unknown only) for envelope storage, targets, load checks, curves and Float, Bool and Enum evaluation; 31 unexecuted cases (10 unresolved, 1 partly); dangling targets excluded (Q-020); PRB-S6-01 to 07, proposed 08 to 11; partial clauses released as [automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md) (21 cases) |
| [Warp markers](warp-markers.md)                                      | Revision 1 draft: 16 requirements (3 without unknown parts, 11 with unknown parts, 2 unknown): marker storage, shadow marker, empty-list refusal, enumerations, setting domains, scripting sample/beat conversion and edit limits; 35 unexecuted cases (28 gradable, 7 unresolved); probes PRB-S8-01 to 11; partial clauses released as [warp-markers-v1](../../handoff/warp-markers-v1/README.md) (38 cases) |
| [Mixer values](mixer-values.md)                                      | Revision 1 draft: 15 requirements (3 documented and static only, 9 with unknown parts, 1 conditional on Q-019, 2 unknown) for mixer storage, fader curves, dB and pan text, crossfade assign and save text; 45 unexecuted cases (27 static or documented, 11 renders needing measurement, 7 unresolved); probes PRB-S9-01 to 08; partial clauses released as [mixer-values-v1](../../handoff/mixer-values-v1/README.md) (37 cases) |
| [Transport-state handoff plan](transport-state-handoff-plan.md)      | Released transport-state-v1 (18 cases, approved with narrowing): scope, exclusions, traceability |
| [MIDI user mapping](midi-user-mapping.md)                            | Revision 3 draft: documented, static, static-conditional and unknown clauses; REQ-005 now carries the native value transforms for all ten map modes; cases MT-01 to MT-23 added (18 static, 5 static-conditional); unexecuted; partial clauses released as [midi-config-v3](../../handoff/midi-config-v3/README.md) (127 cases) |
| [MIDI configuration v3 handoff plan](midi-config-v3-handoff-plan.md) | Released midi-config-v3 (127 cases, approved): scope, exclusions, traceability, review outcome |
| [Clip launch handoff plan](clip-launch-handoff-plan.md) | Released clip-launch-v1 (50 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [MIDI note storage handoff plan](midi-note-storage-handoff-plan.md) | Released midi-note-storage-v1 (67 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Mixer values handoff plan](mixer-values-handoff-plan.md) | Released mixer-values-v1 (37 cases, approved with corrections): scope, exclusions, traceability, review outcome |
| [Automation envelopes handoff plan](automation-envelopes-handoff-plan.md) | Released automation-envelopes-v1 (21 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Bundled device parameters handoff plan](bundled-device-parameters-handoff-plan.md) | Released bundled-device-parameters-v1 (82 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Browser index handoff plan](browser-index-handoff-plan.md) | Released browser-index-v1 (26 cases, approved with narrowing): scope, exclusions, traceability, review outcome |
| [Plug-in discovery handoff plan](plugin-discovery-handoff-plan.md) | Released plugin-discovery-v1 (35 cases, approved with clarifications): scope, exclusions, traceability, review outcome |
| [Warp markers handoff plan](warp-markers-handoff-plan.md) | Released warp-markers-v1 (38 cases, approved with narrowing): scope, exclusions, traceability, review outcome |

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
