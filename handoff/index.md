---
id: NAV-HANDOFF
type: index
status: active
updated: 2026-10-18
access: handoff
---

# Reviewed implementation handoffs

Fourteen finite releases exist, eleven of them current;
midi-config-v1, midi-config-v2 and transport-state-v1 are superseded. midi-config-v3 is a strict superset of v2, which is a strict superset of v1. v3 adds the value each map mode
produces from incoming controller values. transport-state-v2 (which corrects v1's number-text rule) and
als-container-v1 cover a Live Set's transport values and its container and
version envelope. The eight first releases of 2026-10-18 cover these areas:

- clip and scene launch settings;
- MIDI clip notes;
- mixer values and their display text;
- automation envelope storage;
- bundled device preset parameters;
- browser content kinds and tag sidecars;
- plug-in search folders and candidates;
- warp markers.

Approval is limited to explicitly partial requirement clauses, and runtime
compatibility is unverified. A fresh restricted implementation workspace is
still required.

> **Known fixture defect (found 2026-10-18).**
> [SPEC-LIVE-SET-STRUCTURE](../wiki/specs/live-set-structure.md) shows that opening a
> Live Set always runs a validation walk. That walk refuses a set with no audio or
> MIDI track, and a track with clip slots but no freeze sequencer. Under that rule,
> fixtures in six releases would be refused, although their cases expect them to
> open. The six are transport-state-v1 and v2, automation-envelopes-v1,
> clip-launch-v1, midi-note-storage-v1 and warp-markers-v1: 204 fixtures and 178
> cases. Do not implement or verify against those "opens" expectations.
> Superseding releases with corrected fixtures are being prepared. The payloads
> stay unchanged, because releases are immutable. Evidence is in the
> [audit](../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json).

| Release | Target scope | Spec revisions | Review record | Manifest SHA-256 | Supersedes |
| --- | --- | --- | --- | --- | --- |
| [midi-config-v1](midi-config-v1/README.md) | Master/cue/crossfader configuration interpretation | SPEC-MIDI-USER-MAPPING r1, partial REQ-002/003/010/013 only | [Approved review](midi-config-v1/REVIEW.md) | `9e3ab46efba170f61bcd7b9fce5d579c263aefd90097dc06695339594308b6ee` | None |
| [midi-config-v2](midi-config-v2/README.md) | Configuration interpretation: CC and pad enablement, channels, device/mixer/transport/pad targets, map-mode labels, button kinds, bank span | SPEC-MIDI-USER-MAPPING r2, partial REQ-002/003/005–013 only; 001 and 004 unreleased | [Approved with narrowing](midi-config-v2/REVIEW.md) | `889b52fa3b7f19c1bd085f26db39e0f62f00cbf7dc85be050e32207f012eb4d7` | midi-config-v1 (strict superset) |
| [transport-state-v1](transport-state-v1/README.md) | Live Set transport values: loop switch, loop start and length, position, tempo, time-signature code; locations, load text acceptance and refusal, missing, duplicate and unknown items, saved text | SPEC-TRANSPORT-STATE r1 (corrections carried into r2), partial REQ-001 to 008, 010, 011 only; 009 and 012 unreleased | [Approved with narrowing](transport-state-v1/REVIEW.md) | `b2fdf0294fb1209fd34b252fb83327edfb78ca466d22ff40cbd505a04045baba` | None |
| [als-container-v1](als-container-v1/README.md) | Live Set container and version envelope: first-byte container, root element, version attributes and integer rule, newer-version and shipped-schema checks, optional root attributes | SPEC-ALS-CONTAINER r1 (corrections carried into r2), partial REQ-001 to 006 only; 007 to 009 unreleased | [Approved with narrowing](als-container-v1/REVIEW.md) | `f5ca758dd3785a14a5b8f2384fc7a1038d3ed1649eeb63f6b67446577e62d1de` | None |
| [midi-config-v3](midi-config-v3/README.md) | Configuration interpretation as in v2, plus the value each map mode produces from incoming CC and 14-bit CC pairs, with takeover | SPEC-MIDI-USER-MAPPING r3, partial REQ-002/003/005–013 only; 001 and 004 unreleased; MT-17 to 21 out | [Approved](midi-config-v3/REVIEW.md) | `2e7d93767bbb9fffa79cec191b242d7eec52aeb1d20f6f33f1bbdc0beff40458` | midi-config-v2 (strict superset) |
| [clip-launch-v1](clip-launch-v1/README.md) | Stored clip and scene launch settings: fields, value domains, load corrections and migration | SPEC-CLIP-LAUNCH r1, partial REQ-001 to 007, 009, 011 to 014 only; 008, 010, 015 to 023 unreleased | [Approved with narrowing](clip-launch-v1/REVIEW.md) | `ecf755b1c4ea2d3356bd31ff3fdc0efc4034b05a6ecb11c08d8502c86d945bea` | None |
| [midi-note-storage-v1](midi-note-storage-v1/README.md) | MIDI clip notes in Live Sets: note structure, values and limits on open, time grid, NoteIds, per-note expression | SPEC-MIDI-NOTE-STORAGE r1, partial REQ-001 to 010, 013, 014, 016 only; 011, 012, 015, 017 unreleased | [Approved with narrowing](midi-note-storage-v1/REVIEW.md) | `90e799158256b226dde22aff88bae18cdc789d49952469611a455b25cc08e0d4` | None |
| [mixer-values-v1](mixer-values-v1/README.md) | Mixer values in Live Sets: where each is stored, the value read, dB and pan display text, code names | SPEC-MIXER-VALUES r1, partial REQ-001 to 004, 006 to 009 only; 005, 010 to 015 unreleased | [Approved with corrections](mixer-values-v1/REVIEW.md) | `5f6b8401b9324d0cf3d60da47d190e61b93e1935f96995128021f29c9f39cd60` | None |
| [automation-envelopes-v1](automation-envelopes-v1/README.md) | Automation envelopes in Live Sets: storage, targets, event order and load checks; no evaluated values | SPEC-AUTOMATION-ENVELOPES r1, partial REQ-001 to 003, 005 to 009, 012 only; 004, 010, 011, 013 unreleased | [Approved with narrowing](automation-envelopes-v1/REVIEW.md) | `793c1d7d5432de529c21c628e7fa6c46eecb1fa9128a4da9db1d1dfc34378302` | None |
| [bundled-device-parameters-v1](bundled-device-parameters-v1/README.md) | Device presets of seven bundled devices: parameter tables, the value read on open, duplicate and unknown elements, labels | SPEC-BUNDLED-DEVICE-PARAMETERS r1, partial REQ-001 to 004, 006, 007, 011, 012, 014 only; 005, 008 to 010, 013, 015 unreleased | [Approved with narrowing](bundled-device-parameters-v1/REVIEW.md) | `02927f0ec9ca68a7810f863a264c3d6de3607730d06c2b867a1e0369618b4f8e` | None |
| [browser-index-v1](browser-index-v1/README.md) | Browser content kind by file extension; tag sidecar read and write format, names and colours | SPEC-BROWSER-INDEX r1, partial REQ-001, 003 to 008 only; 002, 009 to 013 unreleased | [Approved with narrowing](browser-index-v1/REVIEW.md) | `c47068980e7a10440f059acde5797b5760a2f18478ab97869c19340ead7225a5` | None |
| [plugin-discovery-v1](plugin-discovery-v1/README.md) | VST3 and VST2 search folders and which entries are plug-in candidates | SPEC-PLUGIN-DISCOVERY r1, partial REQ-001, 002, 004, 005 only; 003, 006 to 016 unreleased | [Approved with clarifications](plugin-discovery-v1/REVIEW.md) | `9c3c739b0cf624d793a18bff6c36f5677934863af4da6be61dcd4a55555f6113` | None |
| [warp-markers-v1](warp-markers-v1/README.md) | Warp markers in Live Sets: marker storage, the shadow marker, enumerations, setting domains and scripting edit limits; no playback mapping or saved values | SPEC-WARP-MARKERS r1, partial REQ-001 to 004, 007, 008, 010 to 013, 015, 016 only; 005, 006, 009, 014 unreleased | [Approved with narrowing](warp-markers-v1/REVIEW.md) | `f8546a3e95788074a2cf1cd99564637b8689af853db705fd9beba1af1764ef46` | None |
| [transport-state-v2](transport-state-v2/README.md) | Live Set transport values as in v1, with the corrected number-text rule next to powers of ten, negative zero, integer and number text acceptance, and time-signature codes; new cases from extracted execution of the original x86_64 code | SPEC-TRANSPORT-STATE r3, partial REQ-001 to 008, 010, 011 only; 009 and 012 unreleased | [Approved with listed clarifications](transport-state-v2/REVIEW.md) | `398a88a62114552595830f99ba2fc1bc4d8c0e1f0d2ae65a70d21aa2324c17c8` | transport-state-v1 (corrects REQ-011; carries its 18 cases byte-identical) |
| [midi-config-v4](midi-config-v4/README.md) | Configuration interpretation as in v3, plus Pick-Up and Value Scaling takeover, reversed ranges, the first 14-bit pair and a range-relative value tolerance; new cases from extracted execution of the original x86_64 code | SPEC-MIDI-USER-MAPPING r5, partial REQ-002/003/005–013 only; 001 and 004 unreleased | [Approved with narrowing](midi-config-v4/REVIEW.md) | `0911e9b57730b9d41c143cd18a5bacc80d8439ce51b202201820bef9ff8cef65` | midi-config-v3 (superset with two precision corrections) |

## Release contract

Each future release is a self-contained immutable directory with:

- A role-scoped `AGENTS.md` for the implementation environment.
- Behavioral specs with stable requirement IDs and explicit acceptance cases.
- Reviewed fixtures and approved public sources with versions and provenance.
- A manifest listing scope, exclusions, unknowns, file digests, and reviewer disposition.
- A change list and explicit supersession relationship when replacing a release.

The catalog can advance; existing release payloads cannot. Implementation docs
pin a release and spec revision. Analysts keep the source/evidence traceability
mapping separately; handoffs must not link to private analysis to be intelligible.

Use the [manifest template](../templates/handoff-manifest.md) and
[release workflow](../wiki/workflows.md#release-a-handoff). The isolated export
must include self-contained copies of necessary neutral instructions with links
rewritten for that package. This repository is the staging workspace, not the
isolated export itself.

Implementation begins at its [own index](../wiki/implementation/index.md).
