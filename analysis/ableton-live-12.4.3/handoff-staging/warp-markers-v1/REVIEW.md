# Review disposition

Release: warp-markers-v1, 2026-10-18.

Reviewer: a separate review agent (Claude Opus 5.5) launched by the
coordinator in its own handoff-review context. It did not author this
candidate and will not implement it. The one reviewer performed the scope and
evidence, quality and sanitization, evidence-identity and fixture-sharing
checks. Publication metadata outside this package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-WARP-MARKERS-001 to
004, 007, 008, 010 to 013, 015 and 016 in [the contract](spec.md), narrowed as
listed below. REQ-WARP-MARKERS-005, 006, 009 and 014 remain unreleased. All 38
cases are kept. Case WARP-MARKERS-024 has a new sample time (RVW-04) and case
011 a shorter purpose text (RVW-05). No other input or expectation changed.

- No case grades anything saved, no case grades a value returned by
  `sample_to_beat_time` or `beat_to_sample_time`, and no case opens an audio
  clip whose marker list is empty. The draft's assumptions about saving, about
  conversion values and about the empty-list refusal support no expectation.
- Every load case and every call that depends on the marker list or the
  settings also rests on opening leaving them as read. The reviewer's own
  static check covered that premise for the document read and for the
  completion step that runs for each read clip, marker and sample part. The
  rest of the premise is excluded, and the comparison obligation now detects
  it (RVW-01).
- Every expectation was re-derived by the reviewer's own restatement, written
  without the author's model. It agrees with all 38. Calls were evaluated
  twice: by the contract's clauses with exact rational tempo, and by the add
  and lookup procedure as the static evidence shows it, with its own
  floating-point grid rounding and inclusive beat bounds. Both agree with
  every expectation. The sample covers each released requirement: storage
  (001, 002, 018), number text (003 to 008), lists held as read (001 to 006),
  the sample part's empty list (018), the shadow marker (032 to 034), refused
  conversions (019, 020), defaults (009, 010), codes (011 to 017), setting
  ranges (001), the add (021 to 032), the lookup (033 to 038) and the beat grid
  (005, 026, 028, 029, 035 to 037).
- REQ-WARP-MARKERS-015 was re-derived from the evidence. The order of checks
  is: audio clip, warped, then 0 ≤ p ≤ the sample length, with a value that is
  not a number refused. The position is before the first visible marker whose
  `SecTime` exceeds p, else before the shadow marker. Both neighbour beat
  checks use the beat as given. The right check is skipped when the next
  marker is the shadow, and there is no left neighbour before the first
  marker. Then come the add's rounding and, for each neighbour, inclusive beat
  bounds at the neighbour's beat plus 5/60 and 999/60 beat per second of
  distance. There is no bound toward the shadow. These bounds equal the
  contract's 5 to 999 BPM rule except near the limits and at zero distance
  (RVW-03). Each tempo case was recomputed: 120 and 120, 60 and 60, and 120
  BPM for the accepted adds. The refused adds give about 1.2 BPM to the left,
  about 1.2 BPM to the right, and 60,000 BPM. The lookup rounds in the same
  way and takes the first marker whose beat equals the result. Remove and move
  check only that the clip is an audio clip.
- REQ-WARP-MARKERS-010 and 013 were re-derived: the creation values 30, 65,
  25, 100 and 128, the codes 6 and 2 and the five ranges are confirmed.
  Creation stores each value without a clamp. The `ComplexProFormants`
  default of 100 is its own value and does not depend on `TransientEnvelope`.
  No case grades `TransientEnvelope` (RVW-02).
- Sanitization was checked by the reviewer's own scan of every payload file,
  wider than the author's deny list. No source code, recovered program text or
  messages, internal identifiers or addresses, analyst paths, private evidence
  links, planning identifiers or per-case evidence fields are present. The
  seven refusal reasons are short labels, not message text. The five
  scripting function names and the element names are public. The remaining
  hits are "clip slot", "Max for Live" and the sample reference and
  `MarkersGenerated` element names in the comparison obligation, all public,
  and the forbidden-inputs list of `AGENTS.md`, worded as in the released
  packages.
- Exclusions appear in both the contract and the manifest, and they agree.
  Every expectation is labeled static-derived. Reference and candidate
  execution have not run, and no compatibility is claimed.
- Fixtures were read one by one (RVW-08). In a copy outside the analyst
  checkout, every Markdown link and case input resolves inside the package,
  and every listed hash and size matches.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVW-01 | High | Every graded held value, and every call outcome that depends on the list or the settings, assumed that nothing changes them between reading and the observation or call. The draft attached that assumption only to saved values, and it is open. The pinned build contains an automatic-warping facility whose activity on opening was not traced. | Resolved in part by evidence. The reviewer's static check of the read and of the completion steps of the clip, its markers and the sample part found no step that writes a marker time, adds or removes a marker, or writes one of the value children. Those steps set flags, link markers to the clip and to onsets, register the sample, trim onsets past the sample end, round the clip's position and region values to the beat grid, copy the sample part's warp mode to its chooser and compute a pitch factor. Two onset helpers and a few indirect calls were not traced further. Narrowed for the rest. The contract defines values held after opening as the values once the document has been read. Any change the application then makes by itself is excluded behavior. The comparison obligation keeps the application's saved sample reference and `MarkersGenerated`, requires the observation right after opening, and uses cases 001 and 002 as controls. No expectation changed. |
| RVW-02 | Medium | The inputs without an expectation included "any `TransientEnvelope` value", yet every fixture carries one, which would leave every case without an expectation. | Reworded: only values other than 100 have no expectation, and the held value is not judged. Every shipped audio clip carries 100. Creation stores 100 without a clamp, and opening stores the text directly, so no expectation depends on the open range. |
| RVW-03 | Medium | The bands that excluded inputs near a tempo limit and near a rounding tie (0.000001 BPM, 0.000001 grid step), together with the exclusion of an add exactly at a neighbour's time, were narrower than the arithmetic the evidence shows. Within the released magnitudes, a reviewer search found the original's bounds and the contract's exact tempo disagreeing at up to about 0.000004 BPM from a limit, and the add's rounding disagreeing with exact rounding at up to about 0.0002 grid step from a tie. Near zero distance the bounds collapse. | Narrowed in the contract and the manifest: a tempo within 0.001 BPM of 5 or 999, a beat within 0.001 grid step of a tie, and a sample time less than 0.0005 s from a neighbour's `SecTime` have no expectation. No case is affected; the closest case is 0.1 grid step from a tie and 3.8 BPM from a limit. |
| RVW-04 | Low | Case 024 was the only case whose outcome depended on the unit of the sample length that the add compares with. At 50 s it would be accepted if the length were counted in milliseconds or frames. | The sample time is now 900,000 s, above the length in seconds, milliseconds or frames at up to 192 kHz, and below the argument limit. The expected refusal is unchanged. The length is still stated as an assumption. |
| RVW-05 | Low | The `TransientResolution` labels and the label of `WarpMode` code 5 came from stored enumeration lists. The evidence does not establish them as displayed text; the same kind of list holds internal loop-mode names. | Removed from the contract and from the purpose of case 011. The six `WarpMode` labels are kept as the labels of the warp mode chooser. |
| RVW-06 | Info | The contract listed as an assumption that the scripting test for a warped clip reflects the `IsWarped` value read. | Confirmed by the reviewer's static check: the test reads the clip's own value stored under the `IsWarped` element name. The assumption was removed from the contract. |
| RVW-07 | Info | Remaining stated assumptions: marker times held as binary64, the sample length being the sample's duration, no further error after an add or remove passes its checks, and the lookup. | Accepted. Marker times are kept as 64-bit numbers and shipped marker text matches the 64-bit writing rule; that reading uses the 64-bit conversion stays assumed. The insertion has its own path for a marker past the shadow's time (case 032). The insertion and the removal contain no error exit; what they call was not traced. |
| RVW-08 | Info | Fixtures and sharing. | Each of the 18 XML documents is ASCII with LF endings, a final newline and no tabs. Each has the stated envelope and one holder at the stated path, and is the template with exactly the change its purpose states. The 18 inputs are distinct. The WAV is a RIFF/WAVE file with one 16-byte PCM format chunk (mono, 16-bit, 8,000 Hz, byte rate 16,000, block align 2) and one data chunk of 48,000 zero bytes, which is 24,000 frames or 3.0 s. Its sizes are consistent and it has no other chunk or metadata. All content is invented or generated, and none is shipped. The build is byte-identical. Evidence identity: the pinned program image and every file of the kept evidence run match their recorded digests, and the two unretained query rounds match the digests in the draft. They are acceptable for this release and should be retained before the next revision. |
| RVW-09 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; the inventory was re-hashed. |

## Corrections for the draft contract

These are behavioral corrections for the next revision of the parent
specification. They do not change this package.

- Split the open-and-save assumption into its two halves. The reading half is
  now supported by static evidence for the read and the completion steps.
  State the remainder, changes the application makes by itself after
  reading, as its own assumption. Attach it to every load and scripting
  clause, not only to saved values.
- State REQ-WARP-MARKERS-015's limit as inclusive beat bounds per neighbour.
  Say what happens at zero distance and before the first marker, where there
  is no left check. Carry the bands of RVW-03. Record that `move_warp_marker`,
  like the remove, does not test whether the clip is warped. Record that an
  accepted add or remove can leave the list unchanged.
- Mark the `TransientResolution` labels and the code 5 label as inferred
  display text, as the loop-mode labels already are.
- `TransientEnvelope` is created at 100 without a clamp. Only its range, and
  values other than 100, remain open.
- Update the stale statements about the question register and about the
  handoff plan.

## Disposition

**Approved with listed narrowing** (RVW-01, RVW-03, RVW-04 and RVW-05), only
for the explicit partial clauses in the contract. All expected outcomes remain
static-derived. Neither reference nor candidate application cases have run,
and no compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This disposition concerns the local reviewed-handoff workflow; it does not
authorize external publication. Preserve this release unchanged.
