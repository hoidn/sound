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
| [Transport state](transport-state.md)                                | Revision 3 draft: 12 requirements; REQ-011 k from binary64-rounded log10, negative zero, REQ-006 integer rule and meter codes settled by extracted execution; 36 graded cases (26 X, 7 S, 3 U), TS-023 withdrawn; 18 released as [transport-state-v1](../../handoff/transport-state-v1/README.md); transport-state-v2 staged |
| [Plug-in discovery](plugin-discovery.md)                             | Revision 2 draft: 16 requirements (2 D and S with U parts, 10 S with U parts, 4 U only); 62 unexecuted cases (56 graded, 6 unresolved); release cases adopted as PD-043 to 062; partial clauses released as [plugin-discovery-v1](../../handoff/plugin-discovery-v1/README.md) (35 cases) |
| [Browser index](browser-index.md)                                    | Revision 2 draft: 13 requirements (12 with static-derived clauses, 012 unknown only); 68 case IDs (66 active: 36 static-derived, 30 unknown; 2 withdrawn); sidecars bind to direct files only; partial clauses released as [browser-index-v1](../../handoff/browser-index-v1/README.md) (26 cases) |
| [Clip launch](clip-launch.md)                                        | Revision 3 draft: 23 requirements; grid and boundary arithmetic, chance rescaling and limits, follow-time rounding settled by extracted execution; REQ-016 and 017 corrected; 64 cases (59 graded: 37 X, 22 S or D; 5 U); partial clauses released as [clip-launch-v1](../../handoff/clip-launch-v1/README.md) (50 cases) |
| [MIDI note storage](midi-note-storage.md)                            | Revision 3 draft: 17 requirements; value limits, time grid and saved number text settled by extracted execution; no MidiKey range guard (REQ-011 permanently excluded); 75 cases (61 gradable: 17 X, 44 S or D; 6 blocked; 8 U); partial clauses released as [midi-note-storage-v1](../../handoff/midi-note-storage-v1/README.md) (67 cases) |
| [Bundled device parameters](bundled-device-parameters.md)            | Revision 2 draft: 15 requirements (1 D only, 2 D and S, 12 with U parts) and tables in document order for the seven bundled devices; 37 cases (4 not graded, 4 with unresolved parts); Cabinet microphone labels corrected; DryWet 0..1; partial clauses released as [bundled-device-parameters-v1](../../handoff/bundled-device-parameters-v1/README.md) (82 cases) |
| [Automation envelopes](automation-envelopes.md)                      | Revision 2 draft: 13 requirements (1 D and S, 1 S only, 10 with U parts, 1 U only); 33 case IDs (17 S, 14 U, 2 withdrawn); A1 covers every Float value; Bool and Enum have no conversion step (partly unretained lookups); partial clauses released as [automation-envelopes-v1](../../handoff/automation-envelopes-v1/README.md) (21 cases) |
| [Warp markers](warp-markers.md)                                      | Revision 2 draft: 16 requirements (2 without U parts, 12 with U parts, 2 U only); 36 cases (29 gradable, 4 in part; 7 unresolved); A2 opening and A4 saving split; REQ-015 inclusive bounds; partial clauses released as [warp-markers-v1](../../handoff/warp-markers-v1/README.md) (38 cases) |
| [Mixer values](mixer-values.md)                                      | Revision 3 draft: 15 requirements; fader curves both ways with exact round trip, pan law, crossfade gains and On/Off settled by extracted execution; 48 cases (6 X, 20 static or documented, 11 unmeasured renders, 11 ungraded); partial clauses released as [mixer-values-v1](../../handoff/mixer-values-v1/README.md) (37 cases) |
| [Transport-state handoff plan](transport-state-handoff-plan.md)      | Released transport-state-v1 (18 cases, approved with narrowing): scope, exclusions, traceability |
| [MIDI user mapping](midi-user-mapping.md)                            | Revision 5 draft: 13 requirements; takeover (Pick-Up, Value Scaling, reversed ranges, first 14-bit pair) settled by extracted execution; tolerance max(1e-6, 2⁻²² × max(abs min, abs max)); cases MT-01 to 56 (18 S, 34 X, 4 S-cond); [midi-config-v3](../../handoff/midi-config-v3/README.md) released (127 cases) |
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
