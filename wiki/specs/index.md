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
| [Transport state](transport-state.md) | Revision 1 draft: 12 requirements (5 static-derived, 6 static with unknown parts, 1 unknown), 23 unexecuted cases for tempo, time signature and loop fields |
| [Transport-state handoff plan](transport-state-handoff-plan.md) | Staged transport-state-v1 candidate (18 unexecuted cases): scope, exclusions, traceability, review gates |
| [MIDI user mapping](midi-user-mapping.md)                      | Revision 2 draft: documented, static, static-conditional and unknown clauses; static expectations, unexecuted cases |

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
| SPEC-PLUGIN-DISCOVERY | PD-01–PD-14 (14) | [Plug-in scanner](../research/plugin-scanner-static.md#candidate-requirements-for-spec-plugin-discovery) | Live-side contract ([Q-016](../questions.md#q-016-plug-in-discovery-live-side-contract)) |
| SPEC-BROWSER-INDEX | BI-C01–BI-C12 (12) | [Browser index](../research/browser-index-static.md#candidate-requirements-for-a-future-spec-browser-index) | Draft spec when scoped |
| Per-device parameter specs | DEV-C01–DEV-C10 (10) | [Device bundles](../research/device-bundles-static.md#candidate-requirements-for-per-device-parameter-specs) | Per-device parameter mapping |
| SPEC-CORPUS-DEVICE | CD-C01–CD-C08 (8) | [Corpus DSP (decompiled)](../research/corpus-dsp-static.md#candidate-requirements-for-spec-corpus-device) | Live-side conversion (N5), then Phase 4 measurements |

When a candidate set becomes a draft under this directory, replace its row
here with the draft's catalog row above.

Author bounded contracts with the [spec template](../../templates/spec.md).
Each future spec gets requirement IDs, a feature-map link, original-side evidence,
and acceptance cases. Add its catalog row here in the same change.

Approved snapshots are listed in the [handoff index](../../handoff/index.md).
Candidate code and design are maintained in [implementation](../implementation/index.md);
original-versus-candidate results are maintained in [verification](../verification/index.md).
