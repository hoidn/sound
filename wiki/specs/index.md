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
| [Plug-in discovery](plugin-discovery.md)                             | Revision 2 draft: 16 requirements (2 D and S with U parts, 10 S with U parts, 4 U only); 62 unexecuted cases (56 graded, 6 unresolved); release cases adopted as PD-043 to 062; partial clauses released as [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) (35 cases) |
| [Browser index](browser-index.md)                                    | Revision 2 draft: 13 requirements (12 with static-derived clauses, 012 unknown only); 68 case IDs (66 active: 36 static-derived, 30 unknown; 2 withdrawn); sidecars bind to direct files only; partial clauses released as [browser-index-v1](../../handoff/browser-index-v1/README.md) (26 cases) |
| [Clip launch](clip-launch.md)                                        | Revision 2 draft: 23 requirements (3 D with S parts, 4 S only, 11 S with U parts, 5 U only); 56 unexecuted cases (5 not graded, 3 with unresolved parts); REQ-015 to 018 release proposal dropped; partial clauses released as [clip-launch-v1](../../handoff/clip-launch-v1/README.md) (50 cases) |
| [MIDI note storage](midi-note-storage.md)                            | Revision 2 draft: 17 requirements (4 without U parts, 12 with U parts, 1 U excluded); 71 unexecuted cases (56 gradable, 6 blocked, 9 unresolved); A1 established; REQ-009 key-order precondition; partial clauses released as [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md) (67 cases) |
| [Bundled device parameters](bundled-device-parameters.md)            | Revision 2 draft: 15 requirements (1 D only, 2 D and S, 12 with U parts) and tables in document order for the seven bundled devices; 37 cases (4 not graded, 4 with unresolved parts); Cabinet microphone labels corrected; DryWet 0..1; partial clauses released as [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) (82 cases) |
| [Automation envelopes](automation-envelopes.md)                      | Revision 2 draft: 13 requirements (1 D and S, 1 S only, 10 with U parts, 1 U only); 33 case IDs (17 S, 14 U, 2 withdrawn); A1 covers every Float value; Bool and Enum have no conversion step (partly unretained lookups); partial clauses released as [automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md) (21 cases) |
| [Warp markers](warp-markers.md)                                      | Revision 2 draft: 16 requirements (2 without U parts, 12 with U parts, 2 U only); 36 cases (29 gradable, 4 in part; 7 unresolved); A2 opening and A4 saving split; REQ-015 inclusive bounds; partial clauses released as [warp-markers-v1](../../handoff/warp-markers-v1/README.md) (38 cases) |
| [Mixer values](mixer-values.md)                                      | Revision 2 draft: 15 requirements (3 D/S only, 9 with U parts, 1 conditional on Q-019, 2 U only); 46 cases (24 static or documented, 11 renders with static expectations only, 6 of them also on Q-019, 11 ungraded); partial clauses released as [mixer-values-v1](../../handoff/mixer-values-v1/README.md) (37 cases) |
| [Transport-state handoff plan](transport-state-handoff-plan.md)      | Released transport-state-v1 (18 cases, approved with narrowing): scope, exclusions, traceability |
| [MIDI user mapping](midi-user-mapping.md)                            | Revision 4 draft: 13 requirements (all D + U clauses; 12 with S clauses; 6 with S-cond: 004, 005, 008, 009, 011, 012); cases MT-01–23 (18 S, 5 S-cond); crossfader exemption Absolute only; reversed-range stepped rule; [midi-config-v3](../../handoff/midi-config-v3/README.md) released (127 cases) |
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
