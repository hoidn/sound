# Review disposition

Release: transport-state-v3, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, fixture-validity, quality and sanitization, evidence-identity and
fixture-sharing checks. Publication metadata outside this package is left to
the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-TRANSPORT-STATE-001
to 008, 010 and 011 in [the contract](spec.md). REQ-TRANSPORT-STATE-009 and 012
remain unreleased.

- Supersession. The transport-state-v2 manifest digest equals the catalog value
  and the superseded digest recorded here, and every file it lists still
  matches. All 33 case records are equal to transport-state-v2's, in the same
  order and with the same serialized text. Requirement scopes, provenance
  labels, stated assumptions and the other exclusions are unchanged. The only
  added exclusion is the track list one. Apart from titles and status lines,
  the changed text is the track-list precondition, the fixture provenance and
  the change list. The parent revision states only clarifications that
  transport-state-v2 already carries. No clause or case is added.
- Fixture change. Each of the 33 fixtures equals the transport-state-v2 file
  of the same name with the 21 lines of the track list in
  [the preconditions](spec.md#document-scope-and-preconditions) inserted after
  the `<LiveSet>` start tag. The lines were taken from the contract's own
  listing. No other byte differs. The track list is the first `LiveSet` child
  in all 33.
- Fixture validity. The analysts' structural checker for Live Sets was run on an
  exported copy of every fixture. It finds no structural refusal and no shape
  of unknown outcome in any of the 33. The transport-state-v2 fixtures are all
  refused, for the missing track. The only schema deviations are carried from
  transport-state-v2: `MainTrack` after `Transport`, which does not change what
  is read, and the unknown `Foo` that TS-016 tests. The reviewer's own check
  covered the shape refusals that checker does not evaluate: a base value
  element without `Value`, a repeated member, and a track of an unaccepted
  class. Only TS-015's tested duplicate `LoopOn` was found. The value-less
  elements of TS-012 and TS-014 are not base-value elements. Their `Value` is
  an attribute that may be absent, and the field keeps its new-document value,
  as REQ-007 states.
- Refusal isolation. Each of the 10 refused fixtures differs from TS-022 in
  exactly one line, the tested `Transport` child or `Manual`. TS-022 opens. The
  reviewer's restatement refuses each of the 10 only for its tested text, or
  for TS-015 the duplicate.
- Track and transport values. The track list holds no element of the six
  value paths. The track has no mixer, clips, scenes, automation or devices,
  and the document format gives a track's mixer no tempo or time-signature
  field. Every judged path is anchored at `LiveSet` and does not pass through
  `Tracks`. On open, the loop end is derived from start and length with no
  clamp, and none of the traced open steps reads the track list into a
  transport value. The fixtures hold no automation envelopes, so no step that
  reconciles a stored value with its automation applies; REQ-012 stays
  excluded. The added track therefore changes no expectation.
- Expectations. The reviewer's own executable restatement of the contract
  agrees with all 33 expected outputs and with the worked examples of REQ-004,
  005, 006 and 011. A mutation of any expectation is caught (33 of 33). No
  fixture falls under an exclusion. The retained extracted-execution results
  match their recorded digests. They cover the tested text of 26 cases, and
  every result agrees with the case: refusal, value read and saved text. For
  TS-011 to 016 and TS-022 the static evidence was re-read: the new-document
  values, the duplicate and unknown-child rules, and the saved order of the
  known `Transport` children. The author's cross-check was not relied on.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. The only flagged words are `log10` in the
  REQ-011 notation and the word "probe" in the comparison obligation, both
  carried from transport-state-v2.
- Scope. No runtime, timing, display or audio result is released. No
  expectation depends on an open question. Exclusions appear in both the
  contract and the manifest and agree. Reference and candidate execution have
  not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size matches.
  The 33 fixtures are distinct, well-formed XML, ASCII with LF endings and a
  final newline, with no tabs. They contain no shipped file content.

## Scope rulings

- Minimal addition. The fixtures add the track list only. They still omit
  scenes, the cue track, `NextPointeeId`, the groove pool, quantization and
  view state. Opening without them rests on static-derived evidence: an absent
  member keeps its new-document value and is not an error, and no structural
  check run on open requires them. A complete set would add scene tempo and
  time-signature fields, which bear on the excluded REQ-012, so the minimal
  addition is preferred.
- The track list is inserted as the first `LiveSet` child, its schema position.
  The carried order deviation of `MainTrack` is kept, because order does not
  change what is read and fixing it is not a validity change.
- The transport-state-v1 fixtures have the same defect. That release is already
  superseded and stays immutable. The README and manifest record it.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV3-01 | Low | The contract, README change 1 and the manifest said that a set with no audio or MIDI track is not opened (static-derived). The derived rule is narrower: no audio, MIDI or group track. A set holding only group tracks is refused by other grouping rules or has no derived outcome. | Restated as derived in the contract, README change 1 and the manifest. Such sets were already among the inputs without expectation. No case affected. |
| RV3-02 | Low | The supersession said only that transport-state-v2's fixtures must not judge whether a document opens. Its 10 refused fixtures also fail to isolate their tested text, so a candidate that misses the text rule still passes them. | README and manifest now say that those fixtures must not be used to judge any case. |
| RV3-03 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RV3-04 | Info | Fixture validity. | All 33 fixtures pass the structural checker. Each refused fixture fails only for its tested text, as described above. |
| RV3-05 | Info | The added track and the transport values. | No interaction found, as described above. No expectation changed. |
| RV3-06 | Info | Opening still rests on static-derived evidence for the omitted members, including a set with no scenes and empty clip lists. | Accepted, as described under scope rulings. |

## Disposition

**Approved with listed clarifications** (RV3-01 and RV3-02), only for the
explicit partial clauses in the contract. Every case record and expectation is
transport-state-v2's. Expected results are static-derived or extracted
execution, as labeled per case. Extracted execution ran the original program's
x86_64 code with glibc in place of the macOS libraries. The arm64 build is
inferred to behave the same. Opening and saving are static-derived. Neither
reference nor candidate application cases have run, and no compatibility pass
is claimed. Candidate-only checks cannot replace independent reference
observations. An isolated implementation workspace remains a prerequisite.

This release supersedes transport-state-v2, which stays immutable; its fixtures
must not be used to judge its cases. This disposition concerns the local
reviewed-handoff workflow; it does not authorize external publication.
Preserve this release unchanged.
