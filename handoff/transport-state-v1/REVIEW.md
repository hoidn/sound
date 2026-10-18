# Review disposition

Release: transport-state-v1, 2026-10-17.

Reviewer: a separate review subagent (Claude Opus 5.5) launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope, evidence,
sanitization, completeness, fixture-sharing and packaging checks. Publication
metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-TRANSPORT-STATE-001
to 008, 010 and 011 in [the contract](spec.md). REQ-TRANSPORT-STATE-009 and 012
remain unreleased.

- Every included clause was checked against the reviewed package evidence
  from the pinned 12.4.3 build. The analyzed executable's digest equals the
  recorded target identity.
- Each inference the author listed was ruled on. Four are now directly
  supported by evidence the reviewer read: the reading and writing rules hold
  for all six values, not only for the values the author checked; the defaults
  for a missing tempo; the integer conversion behind REQ-006; and the unknown
  `Transport` child in TS-016, which is skipped without refusal whatever the
  document's version attributes. Two are accepted as stated inferences: that a
  read error anywhere stops the open, and that number reading and writing are
  exact and round ties to even. No case value lies on a rounding tie or near a
  power of ten.
- All 18 cases were read one by one. The reviewer's own executable restatement
  of the clauses agreed with all 18 expected outputs, the worked examples in
  REQ-005, 010 and 011, and the 33-name order in REQ-002. The author's
  cross-check was not relied on.
- Sanitization was checked by the reviewer's own scan of every payload file. No
  source code, recovered program text, internal program identifiers, addresses,
  analyst paths, private evidence links, probe or question IDs or per-case
  evidence fields are present. Element and attribute names are public document
  names. The only flagged words are in the forbidden-inputs list of `AGENTS.md`.
- Exclusions appear in both the contract and the manifest. Every expectation
  is labeled static-derived, with reference and candidate execution not run.
  No compatibility is claimed. The comparison representation and the rule for
  embedding a fixture in a full set are usable without analyst material.
- In a copy outside the analyst checkout, every Markdown link and case input
  resolves inside the package and every listed hash matches. The 18 fixtures
  are distinct, well-formed XML, ASCII with LF endings and a final newline, and
  contain no tabs. They were authored for these cases and contain no shipped
  file content.

## Scope rulings

- REQ-006 narrowing and TS-010: upheld. Time-signature text with spaces on both
  sides, or with `+` and trailing spaces, keeps no expectation. The evidence now
  points to refusal rather than the parent draft's acceptance; a later revision
  may release TS-010 as a refused case.
- Upper bound of 1,000,000 for loop and position values: accepted as an
  explicit scope limit of this release. It is narrower than the evidence
  requires and makes no claim about the original.
- REQ-010 without a case: accepted as a definitional clause. No released
  observable can exercise it until loading or editing a code other than 201 is
  resolved; a case is required in that later revision.
- TS-008 and TS-020 narrowed to the saved `Manual` text: upheld. Whether the
  automation event is written is excluded.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV1-01 | Low | REQ-006 refused time-signature text longer than 63 characters counting trailing spaces. The length limit applies to the text without its trailing spaces, so digits followed by many spaces are not refused on length. | Narrowed: the length refusal now applies only to text that does not end in a space; text longer than 63 characters that ends in a space has no expectation, in the contract and the manifest. No case is affected. |
| RV1-02 | Low | The comparison obligation put the TS-009 text `201.0` into the time-signature automation event too. That event is itself an integer, so a reference run would refuse the set whatever `Manual` does. | Clarified: for TS-009 the event holds `201`. The expected outcome is unchanged. |
| RV1-03 | Editorial | "Same format version" for the full set did not name the root attributes. | Clarified: the full set's root carries the fixture's `MajorVersion`, `MinorVersion` and `SchemaChangeCount` values. No expectation changed. |
| RV1-04 | Editorial | The manifest omitted the decimal-separator locale exclusion and excluded unknown attributes more widely than the contract. | Aligned with the contract. No case affected. |
| RV1-05 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release; this record added to the package and linked. |
| RV1-06 | Info | The REQ-008 rule for unknown `Transport` children rests, for names other than the one in TS-016, on an accepted inference about which names this format version knows. | Accepted; TS-016 does not depend on it. |
| RV1-07 | Info | No case exercises accepted time-signature spellings with spaces or `+`, a value-less `LoopOn` or `CurrentTime`, a duplicate `Manual`, or the saved time-signature `Manual`. | These clauses are supported; cases are proposed for a later revision. No expectation was invented. |

## Disposition

**Approved with listed narrowing** (RV1-01), only for the explicit partial
clauses in the contract. All expected results remain static-derived. Neither
reference nor candidate application cases have run, and no compatibility pass
is claimed. Candidate-only checks cannot replace independent reference
observations. An isolated implementation workspace remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
