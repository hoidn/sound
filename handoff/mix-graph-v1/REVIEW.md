# Review disposition

Release: mix-graph-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
fixture-validity, quality and sanitization, evidence-identity and
fixture-sharing checks. Publication metadata outside this package is left to
the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIX-GRAPH-001 to 011,
013 and 014 in [the contract](spec.md), narrowed as listed below.
REQ-MIX-GRAPH-012, 015 and 016 remain unreleased.

- Composed renders. All 11 render cases carry the label "composed render (spec
  conformance)". The README, the contract and the manifest each say plainly
  that these expectations are spec conformance, not measured compatibility,
  and that no render of the original application exists. The reviewer
  recomposed every render expectation from the extracted-execution gains and
  the contract's rules. Two examples: in MIX-GRAPH-024, pan −1 in Stereo mode
  gives the gains (1.4142135, 0, 0, 0.00001), A's send at the stored minimum
  contributes nothing, and the main track's pan law at pan 0 and volume 1 is
  the identity, so the main output is 1.4142135·A.L and 0.00001·A.R. In
  MIX-GRAPH-026, the stored volume 0.5011872053 returns to exactly
  0.5011872053146362 through the fader conversion, so the main output is
  A + 0.5011872·B. The reviewer then rendered every case frame by frame from
  the fixture's mixer values and the shipped signals. The largest deviation
  from the expected coefficients is 4.7·10⁻⁸; the comparator allows 5·10⁻⁶.
- Computation cases. The reviewer's own executable restatement of the contract
  agrees with all 17 computation cases. A mutation of any of the 28 cases is
  caught. Each extracted-execution expectation equals the retained result for
  its inputs. The gate table equals the retained run for all seven categories
  with the switch on and off. The author's cross-check was not relied on.
- Draft corrections kept out of the payload. The draft case on internal solo
  predicates is not released, and no predicate appears in the payload. That
  draft case also misreads the run for one category, whose main gate follows
  the switch. Out-of-range stored volumes have no expectation: whether opening
  keeps such a value as written is unknown in the parent mixer-values
  specification. MIX-GRAPH-019 and 020 store the two domain bounds exactly, and
  021 and 022 store values inside the domain. The reviewer's restatement of the
  fader conversion returns 0.000319 and 0.00033 unchanged within binary32
  rounding, far from the silence limit. The ramp-length rule as written does
  not hold when q/|s| is 2³¹ or more. The reviewer's own static check of the
  pinned build confirmed this, and those inputs stay excluded; MIX-GRAPH-017
  uses ratios from 176 to 176,400. The same check confirmed that a flat segment
  and a stopped transport give no ramp. The time offset between song position
  and envelope time is untraced. The payload takes envelope time as an input
  and excludes the mapping, and no case depends on the offset.
- Independence from open items. No expectation depends on any of these: a
  stored solo taking effect on open; the send-active rule; the send level above
  the stored minimum; the crossfade wiring; the units of automated volume;
  which envelope drives a parameter; what a one-event envelope applies; the
  clip-envelope time base; or the order of the main sum, which the comparator
  absorbs. A send at the exact stored minimum has fader position 0, so it
  contributes nothing under either send-level conversion. In MIX-GRAPH-027 the
  send gate 0 zeroes every send entry. In MIX-GRAPH-028 the return track's main
  gate is 0. The no-solo assumption does not rest on how a stored solo loads.
  The reviewer's static check found that the main track's volume uses the same
  volume curve as every other track's. That supports MIX-GRAPH-023. The automation settings are now independent of any
  parameter (RMG-01).
- Fixture validity. The analysts' structural checker for Live Sets was run on
  an exported copy of all 11 fixtures. It finds no schema deviation, no
  structural refusal and no shape of unknown outcome. The reviewer's own check
  covered the reading-model refusals that checker does not evaluate: a base
  value element without `Value`, a repeated member, and a list item of an
  unknown class. It found none. Every fixture is expected to open. Each one
  equals the MIX-GRAPH-018 template except for the lines that its purpose
  names. The fixtures are distinct, ASCII, tab-indented, with LF endings and a
  final newline.
- Signals. Both WAV files hold only the `fmt ` and `data` chunks: 16-bit PCM,
  two channels, 44,100 Hz, 64 frames, no metadata. Their samples equal the
  integer formulas in the contract, and the largest magnitude is 0.5. They are
  generated test signals. No fixture contains shipped file content, audio,
  program code or assets.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. The only flagged word is in the forbidden-inputs
  list of `AGENTS.md`, worded as in the released packages. Element and
  attribute names are public document names.
- Scope. Rendered audio is released only as composed spec conformance. Timing
  is released only as per-sample computations. Exclusions appear in both the
  contract and the manifest and agree. Reference and candidate execution have
  not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input and signal exists, and every listed hash and
  size matches.

## Scope rulings

- The comparator, 10⁻⁵ times the largest input magnitude, is adopted. It does
  not separate the pan law's 10⁻⁵ floor from silence (MIX-GRAPH-024, right
  channel), as the contract states.
- Releasing REQ-013 and REQ-014 and the gate rows for categories other than
  unaffected as computations without a render observable is accepted. Each is
  graded only on stated inputs, and the conditions that produce those inputs
  from a Live Set are excluded.
- The send-active rule is treated as unsettled. The send clause is narrowed to
  the exact stored minimum. Both are upheld.
- The re-authored cases are accepted: the in-range volume cases, the main-volume
  and pan cases without A's send, and the three automation value cases as
  computations at envelope time.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RMG-01 | Medium | REQ-013's interpolated Float value and REQ-014's ramp lengths hold only when the parameter's automation settings have a value step. With settings that have none, the value is held at each point. The contract stated REQ-013 for any envelope. Two stated assumptions bound mixer parameters to the default settings and gave pan's step; they rest on a step that was not traced. | Narrowed. A defined term, the default automation settings, is added, and both clauses are stated for it. Which parameters use these settings, and so any parameter's value step, is not released. The two assumptions are removed and the remaining one renumbered. No case changed; MIX-GRAPH-017 takes the step as an argument. |
| RMG-02 | Low | The contract and the manifest excluded every envelope on a mixer parameter in render cases. Yet every fixture holds the main track's one-event tempo and time-signature envelopes, which the minimal Live Set rules include. | Narrowed. The exclusion now exempts those two envelopes when the single event equals the stored value, as it does in every fixture. No render gain depends on tempo or time signature. The reviewer's restatement refuses a variant whose tempo event differs. No case changed. |
| RMG-03 | Low | REQ-013 claimed that point times take effect at exact samples. That depends on the mapping from song position, which is not released. The replacement of the first event's time was evidenced for Float envelopes only. | Narrowed. The timing sentence moved to the not-released list in REQ-013 and the exclusions. The replacement is stated for Float envelopes. Bool and Enum values are stated at or after the first event's time, where MIX-GRAPH-016 evaluates them. No case changed. |
| RMG-04 | Info | Ramp length at q/\|s\| of 2³¹ or more. | Exclusion upheld, as described above. |
| RMG-05 | Info | Out-of-range stored volumes, and the draft case on internal predicates. | Excluded as described above. One sentence of the contract that described that draft case was reworded. |
| RMG-06 | Info | Independence from open items, and the composed-render label. | Confirmed for all 28 cases, as described above. |
| RMG-07 | Info | Fixture validity and signals. | All 11 fixtures pass the structural checker and the reviewer's shape check, and all are expected to open. The two signals are original generated data. |
| RMG-08 | Editorial | Wording. | The solo categories are now stated to be labels of the gate rule, with no implied stored or internal state. Pan-law provenance now reads: formula static-derived, example gains by extracted execution. The send exclusion is worded with the two gates. |
| RMG-09 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RMG-10 | Info | Evidence identity. | The evidence runs with every file they list, the program images and the shipped schema were re-hashed on 2026-10-18. All matched the recorded digests. The draft manifest digest equals the one the author recorded. |

## Disposition

**Approved with listed narrowing** (RMG-01 to RMG-03), only for the explicit
partial clauses in the contract. All 28 cases are released unchanged.
Computation expectations are extracted execution or static-derived, as labeled
per case. Extracted execution ran the original program's x86_64 code with
glibc in place of the macOS libraries. The arm64 build is inferred to behave
the same within the stated tolerances. Render expectations are composed spec
conformance under the project's render convention, not measured compatibility.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace independent
reference observations. An isolated implementation workspace remains a
prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
