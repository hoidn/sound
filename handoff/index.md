---
id: NAV-HANDOFF
type: index
status: active
updated: 2026-10-20
access: handoff
---

# Reviewed implementation handoffs

36 finite releases exist, and 19 are current:
als-container-v1, automation-envelopes-v2, browser-index-v1, bundled-device-parameters-v1, clip-launch-v2, device-analog-v1, device-collision-v1, device-corpus-v5, device-electric-v2, device-tension-v1, live-set-structure-v1, midi-config-v4, midi-note-storage-v4, mix-graph-v1, mixer-values-v2, playback-core-v1, plugin-discovery-v1, transport-state-v3, warp-markers-v2. The other 17 are superseded:
automation-envelopes-v1, clip-launch-v1, device-corpus-v1, device-corpus-v2, device-corpus-v3, device-corpus-v4, device-electric-v1, midi-config-v1, midi-config-v2, midi-config-v3, midi-note-storage-v1, midi-note-storage-v2, midi-note-storage-v3, mixer-values-v1, transport-state-v1, transport-state-v2, warp-markers-v1. Each row's Supersedes column gives the chain. Approval
is limited to explicitly partial requirement clauses. Expectations are labelled
by provenance: static-derived, extracted execution of the original x86_64 code
(ADR 0003), or composed spec conformance (ADR 0004). Nothing has been compared
with a running Live. The later analyst plan/neutral project status records a separate implementation
workspace provisioned on2026-10-19; implementation requires a fresh role-appropriate
context there. This catalog does not authorize implementation in an analyst context.

> **Fixture defect, corrected 2026-10-18.**
> [SPEC-LIVE-SET-STRUCTURE](../wiki/specs/live-set-structure.md) shows that opening a
> Live Set always runs a validation walk. The walk refuses a set with no audio,
> MIDI or group track, and a track whose clip slots lack a freeze sequencer. Under
> that rule, 204 fixtures in six releases would be refused although their cases
> expect "opens": transport-state-v1 and v2, automation-envelopes-v1,
> clip-launch-v1, midi-note-storage-v1 and warp-markers-v1. Each one is
> superseded by a release with valid fixtures: transport-state-v3,
> automation-envelopes-v2, clip-launch-v2, midi-note-storage-v2 and
> warp-markers-v2. Do not implement against the superseded payloads. They are
> left unchanged because releases are immutable. Evidence is in the
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
| [transport-state-v3](transport-state-v3/README.md) | Live Set transport values as in v2, with every fixture made openable (a MIDI track added); no expectation changed | SPEC-TRANSPORT-STATE r4, partial REQ-001 to 008, 010, 011 only; 009 and 012 unreleased | [Approved with listed clarifications](transport-state-v3/REVIEW.md) | `2cd4320ac3e6cefab257d8f8ab6bc627284c87ca4b0b7c06e5ea22ae172d329d` | transport-state-v2 (corrects the fixture defect; carries all 33 cases) |
| [midi-note-storage-v2](midi-note-storage-v2/README.md) | MIDI clip notes in Live Sets as in v1, with every fixture made openable (freeze slot and scene added), plus value limits, time-grid rounding and saved number text from extracted execution | SPEC-MIDI-NOTE-STORAGE r3, partial REQ-001 to 010, 013, 014, 016 only; 011, 012, 015, 017 unreleased | [Approved with listed clarifications](midi-note-storage-v2/REVIEW.md) | `697f09ffc4951d5f3b6d67c20b8f851d68671078a0b3d730a220383f94d2dd15` | midi-note-storage-v1 (corrects the fixture defect; carries all 67 cases) |
| [mixer-values-v2](mixer-values-v2/README.md) | Mixer values as in v1 on fixtures rebuilt on the minimal valid set, plus computed fader curves both ways, pan-law gains, crossfade curves and On/Off from extracted execution; where the engine applies gains is excluded | SPEC-MIXER-VALUES r4, partial REQ-001 to 009, 013, 014 only; 010 to 012, 015 unreleased | [Approved with narrowing](mixer-values-v2/REVIEW.md) | `a79d427a2266ec637d18aad9cbd690c1656ddeea629b4c04501f6817389a6ae8` | mixer-values-v1 (carries all 37 cases; adds 43) |
| [mix-graph-v1](mix-graph-v1/README.md) | Per-track signal order, pre- and post-fader sends, return and main summing, mute and solo, ramps and automation application under default settings; computed values from extracted execution and composed renders labelled spec conformance | SPEC-MIX-GRAPH r1, partial REQ-001 to 011, 013, 014 only; 012, 015, 016 unreleased | [Approved with narrowing](mix-graph-v1/REVIEW.md) | `edb507883ccb32055307584d219fabe75a9534665a3ce828b7ec306ee0a33f66` | None |
| [live-set-structure-v1](live-set-structure-v1/README.md) | Live Set document structure: the open-time validation refusals (no audio, MIDI or group track; clip slots without a freeze sequencer), required and optional elements, tracks, slots and scenes, sample references and Ids; a device-free minimal valid set | SPEC-LIVE-SET-STRUCTURE r1, partial REQ-001 to 010, 013 to 016, 018 only; 011, 012, 017 unreleased | [Approved with narrowing](live-set-structure-v1/REVIEW.md) | `b6d9ef7837bcbc0aa47bff6fc3acd7d51fc6da1e407981f712b1fb130e7a598d` | None |
| [automation-envelopes-v2](automation-envelopes-v2/README.md) | Automation envelope storage, targets, event order and load checks on openable fixtures, including the removal on open of under-populated envelopes; no evaluated or playback values | SPEC-AUTOMATION-ENVELOPES r4, partial REQ-001 to 003, 005 to 009, 012 only; 004, 010, 011, 013 unreleased | [Approved with listed corrections](automation-envelopes-v2/REVIEW.md) | `267554cb2edc6c9960bfd5d67bcf996b833de15b9375063edfce4232c09d3791` | automation-envelopes-v1 (corrects the fixture defect; withdraws v1 cases 003, 004 and 011, which were wrong) |
| [warp-markers-v2](warp-markers-v2/README.md) | Warp markers in Live Sets as in v1 on device-free openable fixtures, plus beat-to-sample conversion and the REQ-015 and 016 edges from extracted execution; no playback mapping | SPEC-WARP-MARKERS r4, partial REQ-001 to 004, 007, 008, 010 to 013, 015, 016 only; 005, 006, 009, 014 unreleased | [Approved with narrowing](warp-markers-v2/REVIEW.md) | `8207ba862c73149821da6e2433b4e5f7fffbae118f540652645aadea5f186cd9` | warp-markers-v1 (corrects the fixture defect; withdraws case 018) |
| [clip-launch-v2](clip-launch-v2/README.md) | Stored clip and scene launch settings as in v1 on openable fixtures, plus grid and boundary arithmetic as value functions of explicit inputs (not launch timing), chance rescaling and limits, and follow-time rounding from extracted execution | SPEC-CLIP-LAUNCH r4, partial REQ-001 to 007, 009, 011 to 018 only; 008, 010, 019 to 023 unreleased | [Approved with narrowing](clip-launch-v2/REVIEW.md) | `02c0212fe8d5b454e3d44e64cd0dbd20299919dddf135032693ba33eee8b6024` | clip-launch-v1 (corrects the fixture defect; carries all 50 cases) |
| [playback-core-v1](playback-core-v1/README.md) | Transport, Trigger launch boundaries, MIDI note emission and unwarped PCM audio computations for explicit action scripts; extracted arithmetic with static control paths, no whole-application compatibility result | SPEC-PLAYBACK-CORE r1 (corrections carried into r2), partial REQ-001 to 015 and 017 to 020; 016 and 021 to 023 unreleased | [Approved with clarifications](playback-core-v1/REVIEW.md) | `c4dc2c5c2e6c963cadc5d06e314a38ad85d8ec9664dd4bb4a562119754b1e20b` | None |
| [device-collision-v1](device-collision-v1/README.md) | Two fixed Collision output comparisons: constructor effective silence and the calibrated 44.1 kHz Pipe render; metrics and complete comparison-domain vectors included | SPEC-DEVICE-COLLISION r1, partial REQ-001/002/003/014 only; 2 cases; modal, noise and other outputs unreleased | [Approved finite review](device-collision-v1/REVIEW.md) | `c1ea731dcee088f9c6a64d786ddf2d36ad84a7799aba0af59b961dfb024d7da2` | None |
| [device-electric-v1](device-electric-v1/README.md) | 117 finite mono Electric outputs with complete named control vectors, three explicit parameter histories and calibrated envelope/band/partial measurements; unstable and random-level portions excluded | SPEC-DEVICE-ELECTRIC r2, partial REQ-001, 005 to 012, 014 and 015; other clauses unreleased | [Approved finite review](device-electric-v1/REVIEW.md) | `1f4e84947bf1ffa9fd605f73381a9778ad8ab4af1b6f9e14662458d606e0dd4f` | None |
| [device-corpus-v1](device-corpus-v1/README.md) | 24 finite Corpus groups, 68 evaluations from exact control vectors and generated signals; executable resolved-mode/onset/band/waveform criteria with explicit omitted modes | SPEC-DEVICE-CORPUS r3, partial REQ-001 and 004 to 012; 002, 003 and 013 unreleased | [Approved finite review](device-corpus-v1/REVIEW.md) | `9fa257fa0e76d666d17da3fc363bf0cfd2facd0db3542db05d22a4260b771af2` | None |
| [device-electric-v2](device-electric-v2/README.md) | Electric finite mono outputs as v1; editorial correction to the restricted-workspace permission sentence only; all numerical inputs, outputs and measurements unchanged | SPEC-DEVICE-ELECTRIC r2, same partial scopes and 117 evaluations as v1 | [Approved finite review](device-electric-v2/REVIEW.md) | `c53a829a459bba8a32311b3f537adc54607e2d05c0b2182ed007012b34591273` | device-electric-v1 |
| [device-tension-v1](device-tension-v1/README.md) | 27 calibrated Tension mono outputs: 26 stable settings plus one repeated-strike sequence; fixed waveform and partial comparisons; chaotic and uncalibrated settings excluded | SPEC-DEVICE-TENSION r2, partial REQ-001, 004, 005, 006, 007, 008, 009, 010, 011, 012; 27 evaluations only; other scopes unreleased | [Approved finite review](device-tension-v1/REVIEW.md) | `02f9a0166bd6538ecfca0dcbebaad79b2397b14c75ca8a6608b5de618a1ffa3d` | None |
| [device-analog-v1](device-analog-v1/README.md) | 38 deterministic groups / 42 finite evaluations; selected onset, envelope and stationary audio measurements only | device-analog r1, finite partial REQ-001, 004–008, 011–017 and 023 | [Approved finite review](device-analog-v1/REVIEW.md) | `b98157cd4cc77661f0755002318d8019789a51790138668ff721a50376f6e231` | None |
| [device-corpus-v2](device-corpus-v2/README.md) | Corpus finite comparisons as v1 plus one Free Ramp Up waveform vector under its own 1%per-channel RMS criterion; 24groups/69evaluations, old68exact | SPEC-DEVICE-CORPUS r4, same partial REQ-001 and004–012; 002,003,013 unreleased | [Approved finite extension](device-corpus-v2/REVIEW.md) | `7207cba976e25616e93efdb0e6685533570ed71b805d1920711c44c890047fab` | device-corpus-v1 (strict finite extension) |

| [device-corpus-v3](device-corpus-v3/README.md) | Corpus finite comparisons as v2 plus two exact held-note inputs; 25 groups/71 evaluations, all 69 earlier evaluations retained | SPEC-DEVICE-CORPUS r5, partial REQ-001 and 004–013; 002/003 and general MIDI behavior unreleased | [Approved finite extension](device-corpus-v3/REVIEW.md) | `7b8b13d1b29345a8b29d9709fb8b1a45b35fed88f37a3b50976b469d63649900` | device-corpus-v2 (strict finite extension) |
| [device-corpus-v4](device-corpus-v4/README.md) | Finite Corpus audio: earlier71 comparisons plus one exact note60 On/Off host34-zero history;26groups/72evaluations, dedicated engineering waveform criterion | SPEC-DEVICE-CORPUS r6, finite partial001/004–013 only;002/003 and broader MIDI/host/UI behavior unreleased | [Approved finite review](device-corpus-v4/REVIEW.md) | `5375571b14812cfc901e0970ab0c627b2e6a6a1a51e0ab3e4c6c29f9a959a1ad` | device-corpus-v3 (one finite extension) |

| [device-corpus-v5](device-corpus-v5/README.md) | Finite Corpus audio: earlier72 comparisons plus one exact same-instance ListeningXL step;27groups/73evaluations, four independent pre/post L/R engineering waveform checks | SPEC-DEVICE-CORPUS r7, finite partial001/004–013 only;002/003 and general automation/MIDI/host/UI behavior unreleased | [Approved finite review](device-corpus-v5/REVIEW.md) | `60734632edbc8bae80f0a080e0af70cdc1217e61e8a5433f6ade67845f17f479` | device-corpus-v4 (one finite extension) |

| [midi-note-storage-v3](midi-note-storage-v3/README.md) | All72 v2 comparisons unchanged, plus six conditional Notes/group comparisons: four local refusals/two nonrefusals under A1 and the supplied counter; no public group load/save or later-effect result | SPEC-MIDI-NOTE-STORAGE r5, partial001–010/013–016 only;011/012/017 unreleased;78 cases | [Approved bounded review](midi-note-storage-v3/REVIEW.md) | `fa281c37472e13a6ba840499687e90928654c9862582fa5bd4d04f4436da7c2c` | midi-note-storage-v2 (all72 case objects/fixtures exact; six local additions) |
| [midi-note-storage-v4](midi-note-storage-v4/README.md) | All78 v3 cases and78fixtures exact, plus two conditional local-reader comparisons using explicit decoded Notes edits over an existing authored fixture; no public catch/load/save or rollback result | SPEC-MIDI-NOTE-STORAGE r6, partial001–010/012–016 only;011/017 unreleased;80cases/78fixtures | [Approved bounded content](midi-note-storage-v4/REVIEW.md) | `1d0cc553a37d95e25b66dad0f5048af8fc79349d9663b184228fac1d0ab24800` | midi-note-storage-v3 (all78objects/fixtures/14oldbodies exact; two local additions) |

Local publication2026-10-20 copies the independently sealed v3 tree exactly.
External seal `REVIEW-MIDI-NOTE-STORAGE-V3-FINAL-EXACT-TREE-SEAL`, SHA256
`af2536c413fe1359541ca1f6963c6f85723ed05d35b8a5f81aef50e50ea7d2a4`, approves this manifest only.
The ready-for-coordinator wording in the immutable payload records its state
before copying; this catalog records actual local publication.

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


Local publication2026-10-20: midi-note-storage-v4 is current after independent
content approval, separate final84-file exact-tree approval and full prerelease
lint. The sealed payload was copied byte-for-byte; manifest SHA256
`1d0cc553a37d95e25b66dad0f5048af8fc79349d9663b184228fac1d0ab24800`.
V3 remains immutable and is superseded. Eight local comparison projections are
separate from public Open/Save outcomes; no runtime or compatibility grade.
Payload finalization metadata records its preparation gates; this catalog
records the actual local publication.
