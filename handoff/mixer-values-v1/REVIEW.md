# Review disposition

Release: mixer-values-v1, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this
candidate and will not implement it. The one reviewer performed the scope and
evidence, quality and sanitization, evidence-identity and fixture-sharing
checks. Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIXER-VALUES-001 to
004 and 006 to 009 in [the contract](spec.md), with the corrections listed
below. REQ-MIXER-VALUES-005 and 010 to 015 remain unreleased.

- Every included clause was checked against the reviewed static evidence for
  the pinned 12.4.3 build and its shipped schema and documents. Each released
  requirement had at least one expectation re-derived from that evidence: the
  mixer location and element order per track type, and the main track sharing
  the other tracks' mixer setup (001); the volume and send gain ranges (002,
  003); the pan setup and pan mode names (004); the decibel text rule (006);
  the pan text rule (007); the track switch text (008); and the crossfade
  assignment names, crossfader setup and curve names (009). The author's
  cross-check was not relied on.
- The reviewer's own executable restatement of the clauses read every fixture,
  checked its form against the contract's preconditions and agreed with all 37
  expected results. It also agreed with the 12 worked examples of
  REQ-MIXER-VALUES-006 and the 10 of REQ-MIXER-VALUES-007, and with the stated
  pan 0.33 example. Pan 0.33 is read as the binary32 number 0.33000001311…;
  50 times that is 16.50000065565…, so the text is `17R`. The decimal 0.33
  would give exactly 16.5, a tie.
- No graded gain is near the −69.7 dB limit. The closest graded inputs are
  −69.6 dB and −69.8 dB, both 0.1 dB away. Measured on the exact decibel
  value, the closest graded gain is 0.000413 dB from ±0.0005 dB (0.99999) and
  0.0001 dB from a three-decimal halfway point (0.5, at −6.0205999 dB). Every
  graded decibel text stays the same when the logarithm is off by up to three
  binary32 steps either way.
- Every number text in the fixtures reads to the same binary32 number whether
  rounded directly or through binary64.
- No graded expectation depends on an open question, an audio render, a fader
  position or saved text. The open questions about the values used for audio,
  the meaning of the solo sink switch and which display shows which text form
  are all outside the released clauses. The text clauses describe only the
  text rule attached to each value, and an observation in another form is
  inconclusive.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers or addresses,
  parameter display names, analyst paths, private evidence links, planning or
  draft case identifiers, or per-case evidence fields are present. Element and
  attribute names are public document names, and the value texts and code
  names are user-visible. The only flagged word is in the forbidden-inputs
  list of `AGENTS.md`, worded as in the released packages.
- Every fixture was read and compared with the template. Each is the template
  with exactly the change its purpose states, and the values that differ from
  the template are exactly the values its case lists. The 37 inputs are
  distinct, well-formed XML, ASCII with LF endings and a final newline, and
  contain no tabs.
- Exclusions appear in both the contract and the manifest and agree. Every
  expectation is labeled static-derived, with reference and candidate
  execution not run. No compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link and case input
  resolves inside the package and every listed hash and size matches.

## Scope rulings

- Value texts may be graded although the display that shows each form is not
  established. The texts are the output of the text rule attached to each
  value. Which display shows them is excluded, and the comparison obligation
  makes an observation in another form inconclusive.
- Saving (REQ-MIXER-VALUES-010) stays excluded. What a save by the target
  build writes is not established, so no saved text can be graded.
- The meaning of `EnabledByUser` is not released, and no case grades it. The
  fixtures hold it fixed as a precondition: `true` on the audio and MIDI sends
  and `false` on the return mixer's own send. Other values have no
  expectation. The draft case behind MIXER-VALUES-001 grades it; the parent
  specification must drop that clause or define what it changes.
- Out-of-domain values, fader positions, curve shapes and audio effects stay
  excluded, as the author proposed.
- The 13 cases that are new relative to the draft each exercise a
  static-derived or documented clause that had no case. All are accepted.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVM-01 | Medium | The track switch text `On`/`Off` (REQ-MIXER-VALUES-008) and the binding of the seven curve names to the set's crossfade curve (REQ-MIXER-VALUES-009) had no evidence citation in the parent specification. The contract listed the curve binding as an untraced assumption. | Resolved by evidence. The reviewer's own static check of the pinned build confirmed both against machine code. The track switch is given a text rule in the same way as the volume's decibel text, and that rule returns `Off` for zero and `On` otherwise. The set's crossfade curve value is set up with the seven names in the stated order, with code 2 as its initial value. Both clauses stay, and MIXER-VALUES-001, 030 and 031 to 036 are unchanged. The curve-binding assumption was removed from the contract. The parent specification must add these citations. |
| RVM-02 | Low | REQ-MIXER-VALUES-002 called 1.99526238 the binary32 number nearest to 10^(6/20). It is one binary32 step above that number (1.9952622652…). A domain bound derived from that wording would leave MIXER-VALUES-006 and 014 without an expectation. | Corrected: the bounds are the binary32 values of the two texts, within 0.000001 dB of −70 dB and +6 dB. No expectation changed. The parent specification has the same error. |
| RVM-03 | Low | The contract did not say that its text expectations assume that some display shows these texts, computed from the value as read. Two pan cases, MIXER-VALUES-020 (0.01) and 025 (0.33), would change text if the value given to the text rule differed by one binary32 step. | One assumption added to the contract. No case changed. The decibel texts do not depend on it within three binary32 steps. |
| RVM-04 | Editorial | The comparison obligation named the display forms for volumes, sends and pans but not for the track switch. | Added: `On` or `Off`. |
| RVM-05 | Editorial | README, AGENTS, the contract, the cases and the manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled, and the inventory re-hashed by the reviewer. |
| RVM-06 | Info | Evidence identity. | The pinned program image and both evidence runs, with every file they list, were re-hashed on 2026-10-18. All matched the recorded digests. |
| RVM-07 | Info | Rulings on the author's stated inferences. | Confirmed by the reviewer against machine code: both split pans use the same text rule as the pan, and the curve binding (RVM-01). Accepted as stated assumptions, which the contract names: values are read as the nearest binary32 number; a code's name is its list entry; and the displays (RVM-03). The logarithm's last-digit accuracy is accepted, and no graded text depends on it. |
| RVM-08 | Info | The author's proposed corrections to the parent specification. | All nine confirmed: the two missing citations (RVM-01); the revision note's case list; save cases that grade only the unknown part; the reading rule not carried over from the transport values; unlisted out-of-domain values; the undefined `EnabledByUser` grading; an unstated boundary width, here set at 0.00005 dB, which the reviewer's own margin check supports; and the missing 0.33 case. Corrections to the parent specification belong to the analyst. |
| RVM-09 | Info | Sharing: three fixture numbers also occur in shipped sets (main volume 0.7367056608, MIDI volume 0.03548133373 and cue volume 1.99526238). | Acceptable. They are bare numbers and carry no content. Every fixture comes from one template authored for this release. |

## Disposition

**Approved with listed corrections** (RVM-02 to RVM-04), only for the explicit
partial clauses in the contract. All expected results remain static-derived.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
