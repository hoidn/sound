# Review disposition

Release: midi-note-storage-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this
candidate and will not implement it. The one reviewer performed the scope and
evidence, quality and sanitization, evidence-identity and fixture-sharing
checks. Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIDI-NOTE-STORAGE-001
to 010, 013, 014 and 016 in [the contract](spec.md), narrowed as listed below.
REQ-MIDI-NOTE-STORAGE-011 is excluded, and 012, 015 and 017 remain unreleased.

- Every included clause and all 67 expectations were checked against the
  reviewed static evidence for the pinned build. At least one expectation per
  released requirement was re-derived from that evidence directly: the note
  structure and the refusal of other elements among the notes, number,
  Boolean and integer text, the per-note defaults, the save order and
  omission rules, the value limits, the time grid, NoteId uniqueness, the
  next-id raise and numbering, the per-note list rules and the saved number
  text.
- The reviewer's own executable restatement of the contract, written without
  the author's cross-check, agreed with all 67 outcomes and every saved notes
  element. Seven mutated expectations were each detected, and 18 excluded
  inputs received no expectation.
- The author recorded seven inferences that the kept evidence did not
  establish. The reviewer's static check established one of them, that the
  open-time steps run when a Live Set is opened (RVN-01). It also re-established
  from retained records the per-note list clauses whose evidence had not been
  retained (RVN-02). The others are accepted as stated assumptions (RVN-11).
- The author proposed ten corrections to the parent draft. Each was checked
  and is carried in this package: MNS-001 does not compare probability groups;
  the `Invalid` cases depend on REQ-002; the order clause of REQ-010 requires
  notes that do not overlap; the 64-bit integer limit is signed; MNS-003 also
  judges n2; controller numbers, keys and ids are limited to plain decimal
  text; the saved order of per-note lists and of event attributes is not
  compared; and twelve cases were added. Using an authored set that is opened
  and saved, in place of the parent's shipped clip file, is accepted because
  shipped content cannot travel. The tenth correction, unretained evidence, is
  resolved by RVN-02.
- The 12 cases new relative to the parent draft (MNS-061 to MNS-071, with
  MNS-071 split into two) each exercise a released clause that had no case.
  All are accepted. MNS-036 stays narrowed to its outcome.
- Sanitization was checked by the reviewer's own scan of every payload file
  and of the decompressed text of every fixture. No source code, recovered
  program text or messages, internal identifiers or addresses, analyst paths,
  private evidence links, planning identifiers or per-case evidence fields are
  present. The only scan hits are in the forbidden-inputs list of
  `AGENTS.md`, worded as in the released packages, a general sentence about
  candidate adapters, and the manifest's self-hash note.
- Every fixture was decompressed and compared with its base. Each is the
  carrier with the base notes or the base list and exactly the change its
  purpose states. Each has the stated 10-byte gzip header, one member, a valid
  CRC-32 and length trailer and nothing after it. Text is UTF-8 with LF
  endings, tab indentation and a final newline. The 67 inputs are distinct.
  No fixture holds a MIDI key other than 36 or 38.
- No released expectation depends on probability-group content, the group
  generator's next id, the MIDI key range, key order other than ascending,
  empty key tracks, key track or list ids, re-sorting of notes, or per-note
  lists that reach their note's edges. Exclusions appear in both the contract
  and the manifest and agree.
- Every expectation is labeled static-derived, with reference and candidate
  execution not run. No compatibility is claimed. In a copy outside the analyst
  checkout, every Markdown link resolves inside the package, every case input
  exists and every listed hash and size matches.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVN-01 | Medium | The value limits of REQ-005 were released under a stated assumption that they run when a set is opened, with four cases (MNS-014 to MNS-017) said to depend on it. The same untraced condition governs every step applied after the note text is read: the limits, the NoteId checks, the next-id raise and numbering, and the per-note list rules. Forty-six cases rely on at least one such step, not four. | Resolved by evidence. The reviewer's static check of the pinned build confirmed that the condition holds when a Live Set is read. The assumption was removed from the contract and from the provenance of MNS-014 to MNS-017. No case changed. |
| RVN-02 | Medium | REQ-014 clauses 4 and 5 (empty lists removed; lists strictly inside their note unchanged) traced only to an evidence record that was not retained. Sixteen cases save or remove a kept list and depend on them: MNS-039, 040, 042, 044a to c, 047, 048, 049a, 049b, 050, 051a, 051b, 069, 071a and 071b. | Resolved by evidence. The reviewer re-established both clauses from retained records of the pinned build, identical to the unretained record, and from the build itself. No case changed. |
| RVN-03 | Low | REQ-009 clause 2 said that key tracks are numbered in ascending key order. The evidence supports the stored order, which equals ascending key order only when the key tracks are stored that way. | Narrowed: the clause now applies to key tracks stored in ascending key order, and other orders are not part of this release. No case is affected. |
| RVN-04 | Low | The purpose of MNS-001 said the saved notes equal the input, and the open-save comparator did not name the group generator's next id as not compared. Both read as an expectation for probability groups, which REQ-015 leaves unknown. | Reworded. No expectation names group content or the group generator's next id. |
| RVN-05 | Low | The manifest excluded every value of magnitude 1,000,000 or more, which includes `Invalid` and so contradicted MNS-017, MNS-051a and MNS-051b. | Aligned with the contract: `Invalid` is excepted. No case changed. |
| RVN-06 | Editorial | The reference obligation did not classify a set that opens with the case's clip present but holding no notes. | Such an observation is now inconclusive. |
| RVN-07 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed. |
| RVN-08 | Info | Evidence identity. | The pinned program image, both evidence runs with every file they list, the unretained record and the retained records used were re-hashed on 2026-10-18. All matched. |
| RVN-09 | Info | The cases that read the text `Invalid` (MNS-017, MNS-051a, MNS-051b) depend on REQ-002. | They list REQ-002, which states the reading for `Duration` and `TimeOffset` only. The reviewer confirmed that the exact seven-character text reads as the largest finite value. |
| RVN-10 | Info | The MIDI key range, missing and repeated keys and the other open key and order questions. | None becomes an expectation. They are excluded inputs, and no fixture uses a key other than 36 or 38. |
| RVN-11 | Info | Remaining inferences: a refusal stops the read; open then save changes the notes only by these rules; a carrier set reads the notes as a full set does; correctly rounded number text; standard gzip; the integer reading of keys, controller numbers and ids. | Accepted as stated assumptions, covered by the reference obligation. The reviewer confirmed that the integer conversion accepts a leading minus sign, which the base list's controller number needs. |
| RVN-12 | Info | Sharing, new cases and narrowing. | `Creator="Ableton Live 12.4.3"` is factual, nominative test data, and the `Revision` is invented. No shipped content is included. The 12 new cases and the MNS-036 narrowing are accepted. |

## Disposition

**Approved with listed narrowing** (RVN-03), only for the explicit partial
clauses in the contract. All expected results remain static-derived. Neither
reference nor candidate application cases have run, and no compatibility pass
is claimed. Candidate-only checks cannot replace independent reference
observations. An isolated implementation workspace remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
