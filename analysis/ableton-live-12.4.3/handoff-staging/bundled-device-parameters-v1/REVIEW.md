# Review disposition

Release: bundled-device-parameters-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the coordinator
in its own handoff-review context. It did not author this candidate and will
not implement it. The one reviewer performed the scope and evidence, quality
and sanitization, evidence-identity and fixture-sharing checks. Publication
metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of
REQ-BUNDLED-DEVICE-PARAMETERS-001 to 004, 006, 007, 011, 012 and 014 in
[the contract](spec.md), narrowed as listed below. REQ-BUNDLED-DEVICE-PARAMETERS-005,
008, 009, 010, 013 and 015 remain unreleased.

- **Tables.** The reviewer's own reader, written without the author's tools,
  went through every shipped device preset, rack, clip and Live Set of the
  pinned build that holds one of the seven devices: 599 documents, 268 of them
  device presets. In every device preset the device element is the root's only
  child. After the 20 members that all devices share, it holds exactly the
  members of its table, in table order. Every parameter has the stated shape
  and the fixture form. Its stored range equals the table domain, Bool text is
  `true` or `false`, and no value lies outside its domain or is fractional where
  the table says whole numbers. Every plain field holds the table's text. Each
  table domain also equals the most frequent unmapped stored range of its
  parameter across all 599 documents.
- **Ranges and the value read on open.** The reviewer re-derived, from the
  static evidence for the pinned build, the range the program gives a
  parameter when it creates the device. At least one parameter per device was
  checked, and every one equals the table domain: Amp `Bass` 0..10 and
  `DryWet` 0..1; Cabinet `DryWet` 0..1, `CabinetType` with five labels and
  `MicrophonePosition` with three; Electric `KeyboardTranspose` 0..24 and
  `PerNotePitchBendRange` 0..48, both in whole numbers, and `KeyboardStretch`
  0..1; Corpus `Transpose` −48..48, `FineTranspose` −50..50 and
  `PitchBendRange` 0..24, all in whole numbers; Analog `Octave` −3..3 and
  Tension `PitchBendRange` 0..12, both in whole numbers; Collision
  `Noise/VelToFreq` −8..8 and `Lfo1/Phase` 0..360. The 28 parameters marked
  "whole numbers" are exactly the stored Float parameters the program steps in
  whole numbers. In the program's value-text reader the reviewer confirmed
  that Float text is read as a binary64 number and then narrowed to binary32,
  that Enum text goes to the same integer reader as the released time-signature
  code, and that Bool text is compared exactly.
- **Expectations.** All 82 cases were read one by one. The reviewer's own
  restatement of the contract rules agrees with every remaining expected
  outcome, value and label. Every fixture is either a complete preset (values
  inside every domain, or every parameter at its lower or upper bound) or the
  device's complete preset with values inside every domain, changed exactly as
  its purpose states. In the bound cases every judged value equals its bound.
  The 82 inputs are distinct. Errors in the author's draft were checked
  separately (RVB-05).
- **Excluded dependencies.** No case depends on the value of a missing member,
  the values of a newly inserted device, anything written on save or the
  handling of out-of-range values. Every fixture holds every member of its
  table once, in order and in the fixture form. Every value that is read lies
  inside its domain, and whole-number parameters hold whole numbers. Boundary cases sit
  exactly on the bounds. No case judges written output. The absent shared
  members are covered by the precondition and the comparison obligation.
- **Assumptions.** The three assumptions the contract names are accepted as
  stated. Because every fixture holds every member, no rule for missing values
  can affect a judged value. For the label assumption, the reviewer re-read
  each of the seven released label lists in the program; each list's order is
  its value order. For the Bool switch the order differs from the candidate
  (RVB-01). The contract also relies on two further points, and both are
  accepted: the absent shared members do not by themselves change a judged
  outcome, which the comparison obligation tests; and no element of these
  devices is named `Foo`.
- **Sanitization.** The reviewer scanned every payload file with its own list.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, probe or question identifiers or
  per-case evidence fields are present. Element, attribute and plain-field
  names are document vocabulary. The only flagged word is in the
  forbidden-inputs list of `AGENTS.md`, worded as in the released packages.
- **Fixtures and sharing.** Every fixture was read. Each has the stated
  declaration and the three root attributes, and is ASCII with LF endings,
  two-space indentation, no tabs and a final newline. Values are computed, not
  taken from shipped presets. For Analog, Tension, Collision, Electric and
  Corpus, the largest share of equal values between a complete-device fixture
  and any shipped preset of the same device is 0.42. For the nine-parameter
  Amp and the five-parameter Cabinet it reaches 0.44 and 0.8, at their bounds,
  where shipped presets also sit. The only text values not computed are
  the table's plain-field texts, such as `MidiIn/None` and `No Output`. They
  are factual document values. The package holds 1.2 MB of fixtures.
- **Exclusions.** The exclusions appear in both the contract and the manifest,
  and they agree. Every expectation is labeled documented or static-derived,
  with reference and candidate execution not run. No compatibility is claimed.
- **Package.** In a copy outside the analyst checkout, every Markdown link
  resolves inside the package, every case input exists, and every listed hash
  and size matches.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVB-01 | Medium | REQ-014 and cases 004 and 070 to 074 gave Cabinet `MicrophoneTypeSwitch` false as Dynamic and true as Condenser. The reviewer's own static reading of the pinned build gives the reverse. The two-text display rule this switch uses shows its first text, Dynamic, for true, and reads that text back as true. At the other two-text switches the reviewer checked in the build, the texts are passed in true-then-false order, for example On then Off and Inverted then Normal. A shipped rack names the macro that drives this switch "Con/Dyn". | Narrowed. The switch's labels are excluded from REQ-014 and the manifest, and removed from the six cases. Cases 070 to 074 no longer judge the switch. Its values stay judged in cases 004 to 006, 049 and 050. The other seven label lists are unchanged. |
| RVB-02 | Low | Cases 013 to 015, 019 to 021 and 062 judged the values of the nine position parameters: Corpus `ExcitationX`, `ListeningXL` and `ListeningXR`, and Collision `HitX`, `ListeningXL` and `ListeningXR` of each resonator. REQ-015 is unreleased, and the candidate's own scope keeps only their table rows. | Narrowed. The 30 state entries are removed. REQ-006 clause 2 now excludes these parameters, the tables mark them "position", and the REQ-015 exclusion, the excluded behavior and the manifest say their values have no expectation. Their rows, kind and stored range stay, as does their fixture form. |
| RVB-03 | Editorial | The comparison obligation inserted the shared members "before the first member". In case 063 an unknown element precedes the first member, so that wording allowed two inputs. | The shared members are now inserted as the first children of the device element. No expectation changed. |
| RVB-04 | Info | Ranges, whole-number marks, labels and value-text rules were re-derived, as described under scope and checks. | Agrees, apart from RVB-01. The draft calls the program's range for Amp and Cabinet `DryWet` untraced; the reviewer found it, and it equals 0..1. |
| RVB-05 | Info | The author's draft has three known errors. Its plain-field clause lists three Collision fields as stored with shipped values, although no document stores them. Its Corpus side-chain list omits `LowerDisplayString` and `MpePitchBendUsesTuning`. It gives inexact label lists for Electric `Polyphony` and Corpus `LfoType`, `LfoSync` and `LfoStereoMode`. | No shipped document of any kind stores those Collision names, and the Collision table lists only its three stored plain fields. All 36 shipped Corpus occurrences carry the seven side-chain fields with the table's texts. No case carries the inexact labels. None of these errors reaches the payload. |
| RVB-06 | Info | For 22 of the 59 Enum parameters of Analog, Tension and Collision, no shipped document stores the upper bound. These domains rest on the stored range alone, and so do the upper-bound cases 009, 012 and 015. | Accepted. The value read does not depend on the number of labels, under the stated assumption that a value read is not changed while the device is created. |
| RVB-07 | Info | Evidence identity. | On 2026-10-18 the reviewer re-hashed the pinned program image and every output file of the three device evidence runs the candidate cites. All match their recorded digests. |
| RVB-08 | Info | Sharing. The tables restate element names, kinds and stored ranges of shipped devices, and the fixtures carry the plain-field texts. | Acceptable. These are behavioral and document-format facts. No preset bytes, preset names, copied parameter values or internal names are included. |
| RVB-09 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record was added and linked. The manifest review and status fields were filled, and the inventory was re-hashed by the reviewer. |

## Disposition

**Approved with listed narrowing** (RVB-01 and RVB-02), only for the explicit
partial clauses in the contract. The release keeps all 82 cases. All expected
outcomes remain documented or static-derived. Neither reference nor candidate
application cases have run, and no compatibility pass is claimed.
Candidate-only checks cannot replace independent reference observations. An
isolated implementation workspace remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
