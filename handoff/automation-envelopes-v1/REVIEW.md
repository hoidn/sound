# Review disposition

Release: automation-envelopes-v1, 2026-10-18.

Reviewer: a separate review agent (Claude Opus 5.5) launched by the
coordinator in its own handoff-review context. It did not author this
candidate and will not implement it. The one reviewer performed the scope and
evidence, quality and sanitization, evidence-identity and fixture-sharing
checks. Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of
REQ-AUTOMATION-ENVELOPES-001 to 003, 005 to 009 and 012 in
[the contract](spec.md), narrowed as listed below.
REQ-AUTOMATION-ENVELOPES-004, 010, 011 and 013 remain unreleased.

- The candidate had 29 cases. 21 are approved; the 8 cases that read an
  envelope's value at a time were withdrawn (RVE-01). Cases 001 to 020 are
  unchanged. Case 021 has a new input (RVE-02).
- Every approved expectation was re-derived from the contract by the
  reviewer's own restatement, written without the author's model. It agrees
  with all 21 outcomes and every saved attribute text. The sample covers each
  released requirement: storage locations and shape (001, 010), the binding by
  Id (021), event elements by value kind (014, 015, 021), the one-event list
  (002), a later negative time (009), every load check (002 to 012), curve
  controls kept and written (017 to 020) and the number text on open and save
  (006, 007, 013 to 016, 018). The reviewer checked the saved texts digit by
  digit against the save rule, among them `-63072000`, `0.3000000119`,
  `0.299999999999999989`, `0.800000000000000044` and `0.200000000000000011`.
  It also checked that the stated condition on curve controls makes the curve
  coordinate non-decreasing. Within [0, 1] with c1 > c2, that holds exactly
  when c1² + c2² − c1·c2 − c1 ≤ 0.
- The weakest cases were examined individually. Case 021 is new and is the only
  save case for Bool and integer values. It was changed (RVE-02). Cases 014 and
  015 refuse Bool and integer text. They rest on the stated assumption that
  these values use the Boolean and integer rules, which are the same as in the
  transport-state-v1 release. That assumption is accepted (RVE-05). Case 010 is
  the clip-envelope counterpart of the refused clip cases. Case 019 relies on a
  missing control reading as 0.5. Both are accepted.
- The candidate's other new cases (002, 007, 010, 014, 015, 019 and 020) each
  exercise a clause that had no case. All are accepted. New cases 028 and 029
  were withdrawn with the other value cases.
- Saved Ids: no case or comparison rule assumes that a save keeps or
  renumbers Ids (RVE-03).
- Inputs: no fixture is or contains a shipped set. No fixture holds an input
  whose outcome this release leaves open. The reviewer checked each fixture
  (RVE-04).
- Sanitization was checked by the reviewer's own scan of every payload file,
  wider than the author's deny list. No source code, recovered program text or
  messages, internal identifiers or addresses, analyst paths, private evidence
  links, planning identifiers or per-case evidence fields are present.
  Remaining hits are public document element names, the refused text example
  `0x1`, and neutral wording in the forbidden-inputs list of `AGENTS.md`.
- Exclusions appear in both the contract and the manifest and agree. Every
  expectation is labeled static-derived. Reference and candidate execution have
  not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link and case input
  resolves inside the package, and every listed hash and size matches.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVE-01 | High | Every value case (022 to 029) assumed that a parameter's reported value is its stored event value, unchanged and in stored units. That covered event times, after the last event and between equal values. Whether the original reports a stored value unchanged was not established for the targets of this release; the static evidence leaves room for a per-parameter mapping of the value. The candidate stated this as an assumption, but nothing in the kept evidence supports it, so the Float expectations were not exact. The candidate treated the Bool and Enum values as free of that step. The reviewer could not confirm this. Those cases also assumed that a parameter follows its envelope after open and that envelope times are song positions in beats, and neither was traced. | Narrowed: cases 022 to 029 withdrawn. REQ-AUTOMATION-ENVELOPES-010 and 011 unreleased. REQ-AUTOMATION-ENVELOPES-004 unreleased, since its only case read values. REQ-005 narrowed to accepting a one-event list, and REQ-006 to document order and later negative times. The value an envelope supplies at any time is excluded in the contract and the manifest. The `open-evaluate` action, the `values` field and their comparison obligation were removed. |
| RVE-02 | Low | Case 021 saved a Bool and an Enum envelope whose event at L has a value that differs from the next event's value. Whether a save keeps such a leading value is not established. In the other save cases the two values are equal. | Fixture changed: the event at L now has the next event's value (`false`; `0`). The saved texts `true`, `false`, `0` and `2` are still exercised. The envelopes are now listed in an order different from their targets' order. The binding by Id therefore keeps a case after case 029's withdrawal. The new behavior is excluded, and the contract states the fixture precondition. |
| RVE-03 | Info | Saved target Ids. Every save case judges the saved `PointeeId` only against the `Id` of the saved target. Event Ids are present but not compared. | Confirmed. No case, comparison rule or obligation assumes that a save keeps or renumbers target or event Ids, and the contract excludes Id handling on save. Two assumptions remain stated: that a save keeps each envelope bound to its target, and that open reaches the envelope checks. |
| RVE-04 | Info | Fixture inputs. | All 21 fixtures were written for this release from one template, and the reviewer compared each with it. Each is the template with exactly the envelopes its purpose states. No fixture copies a shipped set or contains shipped content. In every fixture, each `PointeeId` names exactly one of the four targets in its stated relation, and no two envelopes name one target. Times do not decrease, and no two events share a time. Every event has `Id`, `Time` and `Value`, with Ids distinct in their list. Values are in range and of the target's kind, there is no stored transform, and each `LockEnvelope` is `0`. The text is ASCII with LF endings, and the 21 inputs are distinct. |
| RVE-05 | Info | Assumptions that stay stated in the contract. They are: opening a Live Set applies the envelope checks; Bool and Enum values use the Boolean and integer rules; a save keeps each envelope bound to its target. | Accepted. The format declares these values as Boolean and integer. The rules are the reviewed transport-state-v1 rules. The comparison obligation covers all three. |
| RVE-06 | Info | Evidence identity. | The pinned program image and every file of the evidence run were re-hashed on 2026-10-18. All matched the recorded digests. |
| RVE-07 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. The contract also noted two pairs of identical inputs, which no longer exist. | Status set to reviewed local release. This record was added and linked. Manifest review and status fields were filled, and the inventory was re-hashed. |

## Disposition

**Approved with listed narrowing** (RVE-01 and RVE-02), only for the explicit
partial clauses in the contract. All expected outcomes remain static-derived.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
