# Review disposition

Release: midi-config-v2, 2026-10-17.

Reviewer: a separate review subagent (Claude Opus 5.5) launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope, quality and
sanitization, evidence-identity and fixture-sharing checks. Publication
metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIDI-USER-002, 003
and 005 to 013 in [the contract](spec.md). REQ-MIDI-USER-001 and 004 remain
unreleased.

- Every included clause was checked against the reviewed package evidence: the
  two shipped configuration documents and the static analysis behind them. The
  new rules received individual checks: send-knob position (Send B only with
  Send A on the same strip; a lone second send stays excluded), pad channel
  rules, `[DEFAULT]` applying only to sections present in the file, the integer
  text forms, the 14-bit label cutoff above CC 95, encoder and bank-button
  compaction, and the bank span.
- All 55 new cases, MIDI-CONFIG-055 to 109, were read one by one against that
  evidence, including MIDI-CONFIG-084. The reviewer's own executable restatement
  of the evidence also agreed with all 109 expected outputs. The author's
  cross-check was not relied on.
- The 54 restated cases keep their IDs, fixture bytes and logical
  expectations. The added fields follow from the explicit `Absolute` mode keys
  in each of those fixtures.
- Sanitization was checked by the reviewer's own scan of every payload file. No
  source code, recovered program text, internal program identifiers, analyst
  paths, private evidence links or per-case evidence fields are present. Public field names
  describe the external configuration interface. The only flagged word is in
  the forbidden-inputs list of `AGENTS.md`, worded as in midi-config-v1.
- Exclusions appear in both the contract and the manifest. Every expectation
  is labeled static-derived, with reference and candidate execution not run.
  No compatibility is claimed. Supersession and a change list are present.
- In a copy outside the analyst checkout, every Markdown link and case input
  resolves inside the package and every listed hash matches. Fixtures are
  ASCII with LF endings and a final newline, contain no tabs, use public key
  names and three invented comment lines, and have distinct MIDI addresses.
  The 109 case paths hold 107 distinct inputs; MIDI-CONFIG-003, 010 and 017
  share bytes inherited from midi-config-v1.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RV2-01 | Low | The pad rules said that any out-of-range integer disables a pad. Integer text longer than a configurable conversion length limit, never below 640 characters, fails conversion instead, and a failed conversion in a pad field has no expectation. | Narrowed: such text in a pad note, or in a pad channel for an enabled pad note, is excluded in the contract and the manifest. No case is affected. |
| RV2-02 | Low | The contract trimmed spaces around keys and values but did not state how tabs and other ASCII control characters are handled; the reference trimming removes some of them as whitespace. | Narrowed: ASCII control characters other than the LF line ending, including tabs, are excluded. No fixture contains one. midi-config-v1 already limited its grammar to single spaces. |
| RV2-03 | Editorial | "A single underscore may separate two digits" could be read as allowing only one underscore in a value. | Reworded: an underscore may appear only singly between two digits. `1_0` is still 10. No case changed. |
| RV2-04 | Editorial | MIDI-CONFIG-084 exercises the Send B position clause but did not list REQ-MIDI-USER-009. | Added to its requirement list. Input and expected output are unchanged. |
| RV2-05 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release; this record added to the package and linked. |
| RV2-06 | Info | Evidence identity: the digests recorded at the first release for the reviewed configuration-reader files are not available on this host, so a direct comparison is unknown. | Not blocking. Those files and both shipped documents appear, with matching digests, in the pinned application's signed resource inventory. That inventory's digest is embedded in the main executable, whose digest matches the recorded target identity. The reviewed evidence is therefore from the pinned build. |
| RV2-07 | Info | No case exercises `[DEFAULT]` with an absent section, more than one underscore, or the 14-bit cutoff on a send knob or the crossfader above CC 95. | These clauses are supported; cases are proposed for a later revision. No expectation was invented. |

## Disposition

**Approved with listed narrowing** (RV2-01 and RV2-02), only for the explicit
partial clauses in the contract. All expected results remain static-derived.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. midi-config-v1 remains valid for its narrower
scope. Preserve this release unchanged.
