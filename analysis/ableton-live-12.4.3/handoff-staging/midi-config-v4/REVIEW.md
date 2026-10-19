# Review disposition

Release: midi-config-v4, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, precision, quality and sanitization, evidence-identity and
fixture-sharing checks. Publication metadata outside this package is left to
the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIDI-USER-002, 003
and 005 to 013 in [the contract](spec.md), narrowed as listed below.
REQ-MIDI-USER-001 and 004 remain unreleased.

- Supersession. Cases MIDI-CONFIG-001 to 127 are byte-identical case records,
  and their fixtures byte-identical files, to the released midi-config-v3. That
  release's manifest digest equals the catalog value, and all 132 files it
  lists still match. The changed midi-config-v3 text is limited to titles and
  status lines, the provenance paragraph, the target-parameter, `Absolute`,
  `Absolute14Bit` and relative sentences, the takeover section, the starting
  state, the value-case fields and tolerance, two exclusion paragraphs, the
  comparison obligations, and the change and fixture-provenance sections. No
  midi-config-v3 case, fixture or expected value changed. The change list
  missed the comparison obligations, and two general clauses needed precision
  corrections (RV4-01, RV4-02), so the strict-superset claim no longer holds as
  written. The change list is completed and the relationship reworded (RV4-03).
- Extracted execution was re-run by the reviewer. The program build, the
  execution tool and every evidence file match their recorded digests. The
  evidence run, repeated in a copy of its directory, reproduced every result
  file byte for byte; only its run log, which records memory addresses, differs.
  It used at most 201 calls per process, below the execution tool's limit of
  256. The reviewer then gave the original code each new case's
  messages, parameter and takeover choice exactly as the payload states them,
  one process per case and at most 8 calls per process. All 34 results equal
  the expected values within 5e-10. They cover Pick-Up and Value Scaling,
  reversed ranges (MIDI-CONFIG-136 to 140) and the first 14-bit pair after the
  input opens (MIDI-CONFIG-141 to 145 and 150).
- All 52 value cases were read one by one. The reviewer's own exact
  restatement of the contract agrees with every expected value within its τ;
  the largest difference is 0.154τ (MIDI-CONFIG-161). The `any` cases agree
  under all three choices. A reviewer binary32 model of both builds, written
  from the reviewer's reading of their instructions, equals every
  extracted-execution value on the x86_64 build. On the arm64 build it stays
  within τ of every expected value. The builds differ only where the smaller
  bound is not 0, by at most 0.032τ (MIDI-CONFIG-151).
- A reviewer-side interpretation model, written for the midi-config-v2 review
  and not by the author, agrees with all 161 assignment and bank-span
  expectations.
- The reviewer read the takeover and Pick-Up instructions of both builds. They
  use the same operations, comparisons and constants. Their only fused
  operation multiplies by plus or minus one, so it is exact. A completed pair
  is judged with the same windows as a single message. The four-case previous
  value of a pair equals both builds' combination of the halves for all 16,641
  combinations of present and missing halves.
- Precision. The reviewer computed, for every test that each new case reaches,
  how far apart its two sides lie. The cases within 8τ are exactly
  MIDI-CONFIG-149 and 152 to 161, and the cases with a Value Scaling move are
  exactly the ten that the contract lists. Every other new case is at least
  1,938τ from every bound.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. The only flagged words are in the
  forbidden-inputs list of `AGENTS.md`, worded as in the released packages,
  and in a carried sentence of the contract that says what the fixture set is
  not. Host, build and library names appear only in the provenance label, its
  definition and the stated assumptions, as in transport-state-v2.
- Scope. No timing, display or audio result is released. No expected value
  depends on an open item: the default choice, the displayed wording, on/off
  parameters, notifications, and the ordering and deferral of values are
  excluded. Exclusions appear in both the contract and the manifest and agree.
  Reference and candidate execution have not run, and no compatibility is
  claimed.
- Every new fixture was read. The 34 new fixtures have three authored
  contents: `Encoder1` with `Absolute` or with `Absolute14Bit`, and
  `CrossfaderSlider` with `Absolute14Bit`, each on number 20 and channel 0. They are ASCII with LF
  endings and a final newline, use public key names and contain no shipped
  file content. The message bytes and parameter descriptions are authored for
  these cases. No fixture is a Live Set. The Live Set structure checker
  classifies all 161 fixtures as other documents, so its validity check does
  not apply.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size matches
  the inventory.

## Scope rulings

- Value Scaling moves: the exclusion is upheld. The author measured up to 3.8τ
  between a single-precision move and the exact formula on a sample of data
  values. The full set of 14-bit pairs gives far more: two adjacent pairs near
  the top of the range, with the current value at the lower bound, give 96τ
  on 0 to 1, 386τ on 0 to 3 and 408τ on 0 to 127. The exclusion covers every
  move outside the listed cases, so its scope is right. The ten listed moves
  hold: each has a smaller bound of 0, where both builds compute the same
  values, and each lies within 0.154τ of the exact rule.
- The 8τ band near a bound is upheld. Over all 7-bit values and 14-bit pairs
  on 419 ranges and both builds, a target lies at most 0.78τ from its exact
  value. On 21 chosen ranges, a pair's previous target formed from a missing
  half lies at most 1.73τ from its exact value. Rounding the window bounds adds at most about 0.5τ. With the
  current value placed in steps of τ/8 around every bound on nine ranges, the
  single-precision decision differed from the exact one only within 0.32τ of
  the bound. Both sides of a test are therefore off by less than about 2.3τ,
  and 8τ leaves a margin above three. A narrower band would need a proven
  bound. The same band now serves the stepped exclusion (RV4-01).
- The test for a previous target of exactly −129 (MIDI-CONFIG-149) and the
  four-case previous value of a pair (MIDI-CONFIG-141 to 146 and 150) are kept.
  Both are observable, confirmed by extracted execution and worded as
  behavior.
- The three stated assumptions are accepted: arm64 equivalence, supported by
  the instruction comparison above; the parameter description and previous
  data values the application supplies, as preconditions; and the displayed
  wording of the choices, which only labels a reference comparison.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV4-01 | Low | A stepped target value is rounded in single precision. When its exact value lies very near a half-integer, it can round to the other whole number. The reviewer's model finds such results for 14-bit pairs on stepped ranges from 0 to 5,000 upward, all within 0.36τ of the half-integer. None occurs for 7-bit values, or for pairs on ranges up to 0 to 1,000. The contract named only two kinds of result that can lie farther than τ from the exact rules. midi-config-v3 has the same rounding rule. | Narrowed: a target value *n* or *p* of a stepped parameter within 8τ of a half-integer has no expectation, in the contract and the manifest. Every case lies at least 3,900τ from one. This narrows a midi-config-v3 clause for such values; no midi-config-v3 case is affected. |
| RV4-02 | Low | Rounding adds up over relative messages in a row on a parameter that is not stepped. The reviewer ran the original code on 200 messages in a row. On 0 to 5.3 the value drifted 5.2τ from the exact rule, and on −3.3 to 4.9 it was first beyond τ after 25 messages. One message rounds by at most 0.33τ in the reviewer's model. The contract said τ covers the original's rounding. | Clarified: a value reached by *k* relative messages in a row is compared within *k* × τ, in the contract and the manifest. Each step of the relative cases is exact in single precision, so no case or comparator changes. midi-config-v3 compared such values within 1e-6. |
| RV4-03 | Low | The change list omitted the changed comparison obligations: choices selected by position, with the wording recorded, and the crossfader rescaling rule extended to MIDI-CONFIG-150. With RV4-01 and RV4-02, "strict superset" was no longer accurate. | Change list completed in the README and the manifest. The supersession is stated as a superset with two precision corrections to general clauses, and no midi-config-v3 case affected. |
| RV4-04 | Low | The extracted-execution definition did not name the two parts of the code that did not run. One is a notification Pick-Up gives after it decides a value. The other is the route that applies a value later instead of at once. | Both named in the contract and the manifest. No expectation depends on either: the notification follows the decision, and when a value is applied is excluded. |
| RV4-05 | Editorial | The contract says a Value Scaling move is not rounded, even for a stepped parameter. Yet a stepped parameter takes only whole-number values and must keep the value set on it. | Clarified: none of the listed moves is on a stepped parameter, and a stepped parameter's value after a move has no expectation. |
| RV4-06 | Info | The author's figure for how far a Value Scaling move can lie from the exact formula (3.8τ) came from a sample. The true error reaches hundreds of τ. | Exclusion upheld as ruled above. The figure should be corrected outside this package. |
| RV4-07 | Info | Evidence identity. | The program build, the execution tool and every evidence file match their recorded digests. The evidence run reproduced its results byte for byte, and every new case was re-run. |
| RV4-08 | Info | The analyst plan also notes catalog wording for midi-config-v3. | Outside this package; not edited. |
| RV4-09 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |

## Disposition

**Approved with listed narrowing** (RV4-01) and clarifications (RV4-02 to
RV4-05), only for the explicit partial clauses in the contract. Expected values
are static-derived or extracted execution, as labeled per case. Extracted
execution ran the original program's x86_64 code with glibc in place of the
macOS libraries; the arm64 build is inferred to behave the same. Neither
reference nor candidate application cases have run, and no compatibility pass
is claimed. Candidate-only checks cannot replace independent reference
observations. An isolated implementation workspace remains a prerequisite.

This release supersedes midi-config-v3, which stays immutable and valid for
its own scope apart from the two precision corrections. This disposition
concerns the local reviewed-handoff workflow; it does not authorize external
publication. Preserve this release unchanged.
