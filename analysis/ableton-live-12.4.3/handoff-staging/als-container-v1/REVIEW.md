# Review disposition

Release: als-container-v1, 2026-10-17.

Reviewer: a separate review subagent (Claude Opus 5.5) launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
quality and sanitization, evidence-identity and fixture-sharing checks.
Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-ALS-CONTAINER-001 to
006 in [the contract](spec.md), narrowed as listed below. REQ-ALS-CONTAINER-007
to 009 remain unreleased.

- Every included clause and all 35 expectations were checked one by one
  against the reviewed static evidence for the pinned build and its shipped
  schema-name list: the container decision from the first two bytes, the gzip
  and the uncompressed route to the XML reader, the exact root name, attribute
  lookup by exact name, each row of the integer rule table, the order of the
  version checks, both newer-version conditions, the schema-name lookup and the
  refusal of a root without a document element. The author's cross-check was
  not relied on.
- The author recorded six inferences that the kept evidence did not establish.
  The reviewer's own static check of the pinned build confirmed two of them
  (RVA-01, RVA-09). The other four are accepted as stated assumptions
  (RVA-09), and the contract now names them (RVA-05).
- The author proposed five corrections to the draft contract. Each was
  confirmed: a general precedence of newer-version over corrupt-document is
  too broad, because reading stops at the first refusal; integer syntax is
  checked at the root start tag, before the version checks; uncompressed
  envelope fixtures would depend on unobserved command behavior; the
  shipped-schema check only tests whether a named schema exists, so only
  letters-only values are graded as naming none; and refusals of unrecognized
  leading bytes have no established class. This package agrees with all five:
  combined failures have no expectation, the precedence clause is not carried,
  envelope cases are stored as gzip, only letters-only non-schema values are
  graded, and those refusals are `unspecified`.
- The 12 cases new relative to the draft (ALS-CONTAINER-006, 007, 011, 017 to
  021 and 032 to 035) each exercise a static-derived draft clause that had no
  case. All 12 are accepted.
- The draft asked for two reference observations before a handoff: how a
  refusal is presented, and which of the alternatives left open by the static
  evidence the open command uses. This package excludes the dependent outcomes
  instead. That is an adequate substitute for a static-derived release.
  Texts, dialogs, details and state after a refusal are excluded, and only
  the two-way class is graded, with a comparison obligation (RVA-06). Every
  graded outcome is the same under each open alternative, and the inputs
  whose outcome differs between them are excluded. Both observations remain
  required before any compatibility claim.
- Sanitization was checked by the reviewer's own scan of every payload file
  and of the decompressed text of every fixture. No source code, recovered
  program text or messages, internal identifiers or addresses, analyst paths,
  private evidence links, planning identifiers or per-case evidence fields are
  present. The only flagged word is in the forbidden-inputs list of
  `AGENTS.md`, worded as in the released packages. No schema file content is
  included. The package names two schema identifiers and the largest suffix
  number of one family. Saved Live Sets carry such identifiers in their
  MinorVersion attribute, so naming them is acceptable.
- Every fixture was read, after decompression where it applies, and compared
  with the template. Each is the template with exactly the change its purpose
  states. Every gzip fixture has the stated 10-byte header, a valid CRC-32 and
  length trailer and nothing after it. Text is UTF-8 with LF endings. The 35
  inputs are distinct.
- Exclusions appear in both the contract and the manifest and agree.
  `envelope-accepted` is defined, and distinguished from a set opening, in the
  README, the contract and its comparison obligations. Every expectation is
  labeled static-derived, with reference and candidate execution not run. No
  compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists and every listed hash and size matches.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVA-01 | Medium | The graded classes of 20 cases (ALS-CONTAINER-009, 010, 012 to 015, 020, 022 to 026 and 031 to 035) rested on an untraced step: that a refusal detected while the root or the document element is read is classified like other parse failures, with a newer-version condition taking effect. The refusal itself never depended on it. | Resolved by evidence. The reviewer's own static check of the pinned build confirmed the step for every refusal these cases raise. The classes stay graded; no case changed. |
| RVA-02 | Low | REQ-ALS-CONTAINER-001 clause 2 ("classified again by these same rules") implied an expectation for gzip content that is itself gzip. Whether that inner layer is decompressed or refused is not established. | Narrowed: excluded in the contract and the manifest. No case is affected. |
| RVA-03 | Low | The plain-XML exclusion listed particular forms. Comments, processing instructions and text other than the fixtures' whitespace outside `LiveSet` were covered by no rule and not excluded, although the original refuses at least some of them. | Narrowed: the exclusion now covers any difference from the fixtures' form that no rule names, with these as examples. No case is affected. |
| RVA-04 | Low | The term for the last digit group of a schema name came from the vocabulary of the shipped schema files' content. | Renamed "suffix number" in the contract, the manifest and the purpose of ALS-CONTAINER-025. No expectation changed. |
| RVA-05 | Low | The contract called every rule static-derived but did not say that some derived steps rest on assumptions that were not traced to the end. | One sentence added that names them behaviorally: standard decompression of the fixtures' gzip form, the version checks applying to a `LiveSet` document element, and use of the shipped schema names. The comparison obligation covers them. |
| RVA-06 | Editorial | Presentation is excluded, yet a class comparison needs the original's report. | Obligation added: a graded class observation must show which of the two reports the original gives, without comparing wording, and is inconclusive if the report does not distinguish them. |
| RVA-07 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RVA-08 | Info | Evidence identity. | The pinned program image, the evidence run with every file it lists, and the schema-name table were re-hashed on 2026-10-17. All matched the recorded digests. |
| RVA-09 | Info | Remaining inferences. The reviewer confirmed that the integer conversion is decimal and stops at the first non-digit. Accepted as assumptions: the version checks apply to a `LiveSet` document element, because the application writes version attributes only for document kinds subject to them and every shipped set carries them; an absent MinorVersion is refused as `corrupt-document` in both cases the evidence leaves open; the version checks use the shipped schema names; gzip in the fixtures' form, used by 25 shipped sets, is decompressed in the standard way. | No expectation invented or changed. The conversion also supports refusing values with spaces on both sides and digit runs that overflow; they stay excluded and are proposed for a later revision. |
| RVA-10 | Info | The 12 new cases, and exclusion in place of the two planned reference observations. | Accepted, as described under scope and checks. |
| RVA-11 | Info | Sharing: `Creator="Ableton Live 12.4.3"` in the template, the invented `Revision` and two schema identifiers. | Acceptable. The creator string is factual, nominative test data; no expectation depends on it, and ALS-CONTAINER-029 replaces it. The `Revision` value is invented, not the build's. |

## Disposition

**Approved with listed narrowing** (RVA-02 and RVA-03), only for the explicit
partial clauses in the contract. All expected outcomes remain static-derived.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
