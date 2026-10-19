# Review disposition

Release: midi-note-storage-v2, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, fixture-validity, quality and sanitization, evidence-identity and
fixture-sharing checks. Publication metadata outside this package is left to
the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIDI-NOTE-STORAGE-001
to 010, 013, 014 and 016 in [the contract](spec.md). REQ-MIDI-NOTE-STORAGE-011,
012, 015 and 017 remain unreleased.

- Supersession. The 67 carried cases are identical case records to the
  released midi-note-storage-v1, in content and serialization. That release's
  manifest digest equals the catalog value and the value recorded here, and
  every file it lists still matches. Each carried fixture's text, with the
  freeze slot after `MainSequencer` and the `Scenes` list after `Tracks`
  removed, equals its midi-note-storage-v1 fixture byte for byte; each gains
  exactly those 20 lines and nothing else, and its clip's notes element is
  unchanged. Apart from status lines, the changed contract text is the
  negative-zero, halfway-point and binary32-bound clauses, the narrowed
  exclusion, the stated assumptions and the fixture structure. Each is a
  release of a clause that midi-note-storage-v1 excluded, or a qualification
  for negative zero, which it also excluded, so within its scope every
  expectation is the same. The superset claim holds in effect. The change list
  was incomplete (RVN2-04) and is now complete.
- Fixture validity. The Live Set structure checker that found the defect in
  midi-note-storage-v1 was run by the reviewer on all 72 fixtures. 71 parse;
  none is refused by a known structure rule and none has an unknown shape.
  Each has one MIDI track with one session slot, one freeze slot and one
  scene. The only schema deviation is MNS-013's `Foo`, the element that case
  tests. MNS-012 fails to parse only at its repeated `Velocity`; without the
  repeat it is the MNS-001 fixture byte for byte. Every other refused case
  differs from the base notes or the base list by the one edit its purpose
  states, and the reviewer's restatement refuses it by that rule. The
  additions lie outside the clip, hold no clip, note or per-note list, and
  every judged rule is scoped to the case's clip, so they cannot change a
  note expectation.
- Extracted execution was re-run by the reviewer. The evidence run was
  repeated in a copy of its directory. Every result file, the summary and the
  recorded inputs were reproduced byte for byte; the raw process log differs
  only in values that change from run to run. The evidence run made at most 241 calls per
  process, below the execution tool's 256-call limit. The reviewer then ran the
  original code on the five new cases from the fixture text itself, at most two
  calls per process: the attribute text conversion on every number text of the
  three notes, the value limits and the time grid on the values read, and both
  the attribute writers and the number-text functions on every held value.
  Assembled with the omission rule, the saved notes equal the expected output
  of all five cases.
- Every case was read one by one. The reviewer's own executable restatement
  of the contract, written from the contract and not from the author's
  cross-check, agreed with all 72 expected outcomes and saved notes, and with
  the worked examples in REQ-005, 006 and 016. It detected 12 of 12 mutated
  expectations. Probe inputs with negative zero in `VelocityDeviation`, an
  event's `TimeOffset` or `Value`, or a curve control get no expectation.
- The arm64 instructions of the value limits and the note time grid were
  compared with the rule for the new inputs. Negative zero takes the sign +1,
  a `Velocity` of −0 becomes 1, an `OffVelocity`, `Probability` or `Duration`
  of −0 is kept by the limits, and the half step is added with one rounding,
  which equals the separate addition because the scaled step is exact.
- Each extracted-execution expectation is the program's own result for the
  value of the case's text: the limits, the grid and the saved text. Locating
  the notes, reading other text, opening and saving stay static-derived, as the
  label says. The label, its definition and the stated assumptions agree in the
  contract and the manifest.
- Sanitization was checked by the reviewer's own scan of every payload file and
  of the decompressed text of every fixture. No source code, recovered program
  text, internal identifiers, addresses, analyst paths, private evidence links,
  planning or structure-analysis identifiers or per-case evidence fields are
  present. The only flagged words are in the provenance label, its definition
  and the stated assumptions, public element names, or the forbidden-inputs
  list of `AGENTS.md`, worded as in the released packages.
- Scope. No runtime, timing, display or audio result is released. No
  expectation depends on an open question: the scene addition removes the one
  structure shape whose outcome is unknown. Exclusions appear in both the
  contract and the manifest and agree. Reference and candidate execution have
  not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, the 72 fixtures are distinct
  single-member gzip files with the stated header and trailer, UTF-8 text with
  LF endings and a final newline, and every listed hash and size matches. They
  were authored for these cases and contain no shipped file content.

## Scope rulings

- Requirement IDs added by the author to MNS-073 to MNS-075: upheld, and
  extended to MNS-072 (RVN2-03).
- "Values on the grid are unchanged" against "−0 is stored as +0":
  confirmed. The contract's REQ-006 clause 3 now excepts negative zero, and
  REQ-007 had the same conflict (RVN2-01). Both now say the same thing in the
  contract, the README and the manifest.
- Stating `-0` in REQ-002 clause 3: accepted.
- Negative zero excluded in `VelocityDeviation`, an event's `Value` and the
  curve controls: upheld. The exclusion now also names `TimeOffset`
  (RVN2-02).
- REQ-016 step 1 kept from midi-note-storage-v1: accepted, as in the
  transport-state-v2 review. The new saved values are 0, −0, 1, 127 and one
  grid unit; 1 is an exact power of ten, and the logarithms of 127 and of one
  grid unit (2.104 and −6.585) are far from an integer.
- Carried records keep the static-derived label: accepted. Relabelling
  would change midi-note-storage-v1 records.
- Stated assumptions: accepted, and widened for MNS-072 (RVN2-03). Arm64
  equivalence is accepted on the instruction comparison above.
- A carrier that satisfies the known structure rules reads the notes as a full
  set would: accepted as an inference; the reference comparison
  obligation covers it.
- The scene is required, not optional. A set whose slot count differs from its
  scene count has no established outcome, so `loads` without a scene would
  depend on an open question.
- `TrackGroupId` is absent from every fixture. The reviewer read the cited
  record of the track's initial state, which sets the group to none, and its
  test of that value. An absent member keeps its initial value. Accepted as a
  stated inference, as for the other absent track elements.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVN2-01 | Low | REQ-007 said that a note with `Duration` 0 loads and saves unchanged. Negative zero compares equal to 0, but a `Duration` of −0 is saved as `0` (REQ-006 clause 4, MNS-074). This is the conflict the author found in REQ-006, in a second clause. | Clarified: REQ-007 now names positive zero and points to REQ-006 clause 4, in the contract and the manifest; README change 2 says so. No expectation changed. |
| RVN2-02 | Low | The negative-zero exclusion named only `VelocityDeviation`, an event's `Value` and the curve controls. REQ-002 clause 3 also gives no expectation for −0 read in an event's `TimeOffset`. | Narrowed explicitly in the contract's exclusions, the manifest, README change 2 and the change list. No case affected. |
| RVN2-03 | Low | MNS-072 depends at full precision on the nearest-value reading of its text, which is static-derived: the retained run passed the value, not the text. A value one binary64 step lower is stored as 0. The case did not list REQ-002, and the number-text assumption did not name it. | REQ-002 added to MNS-072, as the author did for MNS-075. The assumption names MNS-072 in the contract and the manifest. The reviewer's run of the original reading code on the text, with glibc's conversion, gave the correctly rounded value. The expected output is unchanged. |
| RVN2-04 | Editorial | The change list did not mention three things: the number-text assumption now names ties to even on save, REQ-006 clause 3 now excepts negative zero, and the changes of RVN2-01 and RVN2-02. | README changes 2 and 5 and the manifest change list completed. The supersession relationship now says that these clauses are qualified only for negative zero, which midi-note-storage-v1 excluded. |
| RVN2-05 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RVN2-06 | Info | Evidence identity. | The program build, both builds of the execution tool and every file of the two extracted-execution runs and the structure run match their recorded digests. The structure run's record was refreshed after staging, so the digest mismatch noted at staging no longer exists. A full re-run reproduced the extracted-execution results byte for byte. |
| RVN2-07 | Info | For the parent specification draft, not this package. REQ-006's "values already on the grid are unchanged" and REQ-007's "a note with `Duration` 0 … unchanged" conflict with −0 being stored as +0. The case table omits REQ-002 for MNS-072 to MNS-075 and REQ-004 for MNS-073. REQ-002 does not state that `-0` reads as negative zero. | To be corrected in a later revision of the draft. |

## Disposition

**Approved with listed clarifications** (RVN2-01 to RVN2-04), only for the
explicit partial clauses in the contract, with 72 cases. Expected results are
static-derived or extracted execution, as labeled per case. Extracted
execution ran the original program's x86_64 code with glibc in place of the
macOS libraries. The arm64 build is inferred to behave the same. Neither
reference nor candidate application cases have run, and no compatibility pass
is claimed. Candidate-only checks cannot replace independent reference
observations. An isolated implementation workspace remains a prerequisite.

This release supersedes midi-note-storage-v1, which stays immutable and valid
for its own clauses, but whose fixtures must not be used. This disposition
concerns the local reviewed-handoff workflow; it does not authorize external
publication. Preserve this release unchanged.
