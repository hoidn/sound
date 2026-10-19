# Review disposition

Release: transport-state-v2, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, quality and sanitization, evidence-identity and fixture-sharing
checks. Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-TRANSPORT-STATE-001
to 008, 010 and 011 in [the contract](spec.md). REQ-TRANSPORT-STATE-009 and 012
remain unreleased.

- Supersession. The 18 carried cases (TS-001 to 009, 011 to 016 and 020 to
  022) are byte-identical case records, and their fixtures byte-identical
  files, to the released transport-state-v1. That release's manifest digest
  equals the catalog value, and every file it lists still matches. Apart from
  titles and status lines, the changed transport-state-v1 text is the REQ-011
  step 1 rule, the negative-zero, `#`, time-signature spelling and logarithm
  exclusions, the REQ-006 restatement and the REQ-010 sentence on codes other
  than 201. Within transport-state-v1's scope the corrected step 1 gives the
  same k as the old one: a logarithm at least 1e-12 from an integer is many
  binary64 gaps from it for every value in range, and an exact power of ten has
  an exact logarithm. The superset claim holds in effect. The change list was
  incomplete (RV2-01) and is now complete.
- Extracted execution was re-run by the reviewer. The evidence run was repeated
  in a copy of its directory and reproduced every result file byte for byte.
  The program build and the execution tool match their recorded digests. The
  reviewer also ran the original reading and writing code on all 15 new cases
  and the 11 REQ-011 worked examples, at most two calls per process. Every
  result equals the expected output. Every refusal is the reader rejecting the
  text. The evidence run itself used at most 200 calls per process, below the
  execution tool's 256-call limit.
- REQ-011 step 1. An 80-digit decimal restatement of the rule, with L
  correctly rounded, reproduces all texts of the retained 6,539-value sweep
  except 11. Those 11 lie 0.4955 to 0.5559 gaps from an integer, where glibc's
  logarithm is not correctly rounded. All of them are inside the excluded band
  of 1/4 to 3/4 of a gap, and no value outside the band differs. The case
  values lie 0.022 to 0.163 gaps from an integer. The rule's general claim
  needed an accuracy assumption that was not stated (RV2-02).
- All 33 cases were read one by one. The reviewer's own executable restatement
  of the contract agreed with all 33 expected outputs and with the worked
  examples in REQ-004, 005, 006, 010 and 011. No fixture falls under an
  exclusion. The author's cross-check was not relied on.
- Each extracted-execution expectation is the reader's or the writer's own
  result: the value read, the refusal, or the saved text. Whether a document
  opens or is refused, and the save, stay static-derived, as in
  transport-state-v1. TS-028 judges the sign of negative zero only through its
  saved text. The static evidence shows that the read value is stored
  unchanged, with no range check, and written back on save. TS-030 judges only
  that the document opens, not that code 0 takes effect. No meter text is
  released.
- Each new case carries the label "extracted execution (x86_64 slice, glibc
  substitutions); arm64 equivalence inferred", which states its limits. The
  contract defines the label and lists the assumptions in behavioral terms.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. Long digit strings are case values or SHA-256
  digests. The only flagged words are in the provenance label, its definition
  and the stated assumptions, or in the forbidden-inputs list of `AGENTS.md`,
  worded as in the released packages.
- Scope. No runtime, timing, display or audio result is released. No
  expectation depends on an open question. Exclusions appear in both the
  contract and the manifest and agree. Reference and candidate execution have
  not run, and no compatibility is claimed.
- Every new fixture was read. Each is the transport-state-v1 template with
  exactly one `Value` changed, as its purpose states. The 33 fixtures are
  distinct, well-formed XML, ASCII with LF endings and a final newline, and
  contain no tabs. They contain no shipped file content.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size
  matches.

## Scope rulings

- Assumptions from staging. Arm64 equivalence is accepted. The reviewer
  compared the retained arm64 instructions for the time-signature reader
  (window, 63-character limit, `+-` and ASCII checks) and for the 17-digit
  number text (zero test, floor or ceiling chosen by the sign of L,
  max(0, P − k)) with the rule. The logarithm and number-grammar assumptions
  are accepted as widened by RV2-02 and RV2-03. Ties to even remain an accepted
  inference, as in transport-state-v1; no case lies on a tie.
- Carried cases keep the static-derived label even where extracted execution
  agrees with them. Relabelling would change transport-state-v1 records.
- TS-030 is kept. Opening a document with code 0 rests on the same static
  evidence as code 201: the stored code is not range-checked when it is read.
  Whether the code takes effect stays excluded.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV2-01 | Low | The change list was incomplete. transport-state-v1 gave no expectation for opening a document whose code is not 201, and TS-030 now judges one. The README's change 5 announced an added exclusion without naming it, and the stated assumptions were not listed as a change. | README changes 3, 5 and 6 and the manifest change list completed. No expectation changed. |
| RV2-02 | Low | Outside the excluded band, REQ-011 step 1 assumes that the original's logarithm errs by less than 3/4 of a gap where its last bit decides k. The contract stated this only for TS-024 to TS-027, with a 0.8-gap bound. README change 1 also stated the correctly rounded logarithm as what the original program does, though the run used glibc's, which differs inside the band. | General assumption added to the contract and the manifest. REQ-011 now points to the band exclusion. README change 1 reworded. The manifest REQ-011 scope says "outside the half-gap band". No case affected. |
| RV2-03 | Low | Two results depend on glibc's functions, not the original code, and this was not stated: the nearest-value decimal reading of TS-024 to TS-028, including the sign of `-0`, and the exact save text with the sign of negative zero. | The reading and save-text assumptions in the contract and the manifest were widened to cover them. No expectation changed. |
| RV2-04 | Editorial | The definition of extracted execution named only the reading of text. The save cases also ran the writer on the value read. | Definition clarified in the contract and the manifest. |
| RV2-05 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RV2-06 | Info | Evidence identity. | The program build, the execution tool and every evidence file match their recorded digests. A full re-run reproduced the results byte for byte. |
| RV2-07 | Info | The band is conservative on the side of the integer toward zero. There k is the same whichever way L rounds. | Accepted. A later revision may narrow the exclusion to the far side. |
| RV2-08 | Info | Supported clauses without a case: `#` text of other lengths refused, `1e` read as 1, and the accepted `-` spellings that give codes outside 0 to 494, which stay excluded. | Proposed for a later revision. No expectation invented. |

## Disposition

**Approved with listed clarifications** (RV2-01 to RV2-04), only for the
explicit partial clauses in the contract. Expected results are static-derived
or extracted execution, as labeled per case. Extracted execution ran the
original program's x86_64 code with glibc in place of the macOS libraries. The
arm64 build is inferred to behave the same. Neither reference nor candidate
application cases have run, and no compatibility pass is claimed.
Candidate-only checks cannot replace independent reference observations. An
isolated implementation workspace remains a prerequisite.

This release supersedes transport-state-v1, which stays immutable and valid for
its own scope. This disposition concerns the local reviewed-handoff workflow;
it does not authorize external publication. Preserve this release unchanged.
