# Review disposition

Release: warp-markers-v2, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, provenance, fixture-validity, quality and sanitization,
evidence-identity and fixture-sharing checks. Publication metadata outside this
package is left to the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-WARP-MARKERS-001 to
003, 007, 008, 010 to 013, 015 and 016 in [the contract](spec.md), narrowed as
listed below. REQ-WARP-MARKERS-004, 005, 006, 009 and 014, and clause 2 of
REQ-WARP-MARKERS-001, remain unreleased.

- Supersession. The warp-markers-v1 manifest digest equals the catalog value
  and the superseded digest recorded here, and every file it lists still
  matches. 37 of its 38 case records are carried in their order, equal as data
  and as serialized text; WARP-MARKERS-018 is withdrawn (RVW2-01). Each of the
  17 documents that keep a warp-markers-v1 name holds the same warp children
  and marker list as its warp-markers-v1 counterpart. The structural checker
  below finds a track with clip slots but no freeze slots in 17 of the 18
  warp-markers-v1 documents, as the change list says.
- Fixture validity. The analysts' structural checker for Live Sets was run
  unchanged on an exported copy of every fixture. It finds no structural
  refusal, no shape of unknown outcome and no schema deviation in any of the 20
  documents, and no contradicted or non-isolating case. The reviewer's own
  check of the shapes that checker does not evaluate (a base value element
  without `Value`, a repeated member) found none. The seven value-less settings
  of WARP-MARKERS-010 are compound members whose `Value` is an attribute, not
  base value elements. Every document has four empty device lists and a next
  pointee identifier of 67, above its largest identifier, 66. Each document
  differs from `base.xml` only inside the clip. WARP-MARKERS-007 and 008 differ
  from it in one line, the tested marker attribute; `base.xml` opens, and the
  reviewer's restatement refuses each only for its number text. The WAV fixture
  is mono 16-bit PCM at 8,000 Hz with 24,000 zero frames. It equals, byte for
  byte, a WAV rebuilt from those parameters and the warp-markers-v1 file, so it
  is generated.
- Extracted-execution labels. Each of the 15 cases labelled extracted
  execution (WARP-MARKERS-039 to 050, 052, 056 and 057) was checked against the
  raw outputs of the retained run, not only its summary. Every deciding value
  is there and equals the case bit for bit: the conversion result for 039 to
  050, the rounded beat and both neighbours' bounds for 052, the rounded beat
  for 056 and 057. The reviewer then re-ran all of them in fresh processes of
  the same extraction setup, with inputs taken from the package: at most 10 calls per
  process, against a limit of 256. Every value was reproduced bit for bit,
  including 2.000000130078255 → 2.00000026015651 for WARP-MARKERS-057. No case
  claims extracted execution without a retained run. WARP-MARKERS-051, the
  conversion on two markers, is labelled computed: the run converted on
  four-marker lists only. Two statements of the label were broader than what
  ran (RVW2-03).
- Computed-by-rules cases. In the 7 cases (WARP-MARKERS-051, 053 to 055 and
  058 to 060) every deciding value the run did not cover has inputs inside
  the run's range. The rounded beats lie between 2 and 12, inside the run's 0 to
  10¹³, and on the run's side of zero. The bounds use neighbour distances of
  0.5 and −0.5, as in the run. The one exception, distance −1 toward the right
  neighbour in 059 and 060, decides nothing, because the rounded beat lies at
  least 0.41 beat inside those bounds. Two alternative operation orders are
  also consistent with every run value: a reciprocal multiplication in the
  rounding, and the tempo multiplied by the distance before the division by 60
  in the bounds. Each computed case keeps its outcome under them. 054, which
  equals its bound exactly, uses the run's distance 0.5. For 051, the reviewer's
  reading of the target build's conversion finds no step that depends on the
  list length. Its interpolation factor of 89.07 lies inside the run's −1 to
  3,072, and its value is compared within 1e-9 beat.
- Expectations. The reviewer's own executable restatement of the contract
  agrees with all 63 expected outcomes, and every conversion value is
  bit-identical. A mutation of any expectation is caught (63 of 63). The worked
  examples of REQ-008, 015 and 016 hold, including the binary64 neighbours of
  the halfway point in REQ-016. For WARP-MARKERS-061 to 063 the reviewer re-read
  the target build's add, remove, move and delete. The add skips the left check
  and bound for a position before the first marker. Neither remove nor move
  tests whether the clip is warped. The delete returns without change below
  three markers. 064 rests on the opening steps that the carried cases rest on
  and that the warp-markers-v1 review checked: none moves the last marker. The
  author's cross-check was not relied on.
- Shadow-marker formula. Its exclusion is clean. The payload states no formula
  and no value of a newly placed shadow marker. "Where and when the application
  creates or re-places the shadow marker, and the values it gives it" is
  excluded in the contract and the manifest. The cases that use a shadow
  marker take it from the fixture as stored: 043 to 045, 050, 051, 063 and 064.
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. The flagged words are one in the
  forbidden-inputs list of `AGENTS.md`, worded as in the released packages, and
  the host and build names in the provenance label, as in the other releases
  with extracted execution. The fused multiply-add and the rounding sequences
  are stated as arithmetic.
- Scope. No runtime, timing, playback, display or audio result is released
  after RVW2-02. No expectation depends on an open question after RVW2-01. The
  remaining derived steps are stated assumptions covered by the comparison
  obligation. Exclusions appear in both the contract and the manifest and agree.
  Reference and candidate execution have not run, and no compatibility is
  claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input and sample exists, and every listed hash and
  size matches. The 20 XML fixtures are distinct, well-formed ASCII with LF
  endings, tab indentation and a final newline. No fixture contains shipped
  file content.

## Scope rulings

- Device placement. The candidate's base set placed an instrument directly in
  the MIDI track's device list and an effect directly in the audio track's.
  Whether a track's device list accepts a device is an open question. Every
  case rested on it, and WARP-MARKERS-018 also judged the sample part of a
  Simpler placed there. Both devices are removed from the base set and so from
  every document. Their two automation targets go with them, and the next
  pointee identifier becomes 67. An empty device list is a form of saved sets,
  so no case rests on device placement any more. WARP-MARKERS-018 cannot be
  kept without a device. It is withdrawn, with clause 2 of
  REQ-WARP-MARKERS-001 and REQ-WARP-MARKERS-004, whose only released clause it
  judged. Its identifier stays unused. No other expectation changed.
- REQ-WARP-MARKERS-009. The candidate released one statement without a case:
  a session clip that is not warped does not use its markers when it plays.
  It is a playback claim. No output this release grades can show it, and the
  silent WAV fixture could not show it even in an audio comparison. The
  requirement stays unreleased, as in warp-markers-v1.
- Combined failures. The calls of WARP-MARKERS-023 to 027 also lie outside the
  beat bounds. Their expected reasons are those of the first failing check, in
  the order of REQ-WARP-MARKERS-015, which the reviewer's reading of the add
  confirms. The contract now says so. Other combinations still have no
  expectation.
- The two-marker list of `two-markers.xml` holds a shadow marker 1/32 beat after
  the first marker at 167 BPM. Its `SecTime` text is that arithmetic value to
  18 significant digits, the same value a shipped set holds. A single computed
  number is not shipped content, and the rest of the document is authored.
  It is accepted.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVW2-01 | Medium | Every case rested on the open question of where devices may be placed, through the base set's instrument and effect; WARP-MARKERS-018 also judged a Simpler's sample part. | Narrowed: both devices removed from every document, the next pointee identifier set to 67, WARP-MARKERS-018 withdrawn with REQ-WARP-MARKERS-001 clause 2 and REQ-WARP-MARKERS-004, and devices and sample parts excluded, in the contract, README, cases and manifest. The structure assumption no longer names devices. |
| RVW2-02 | Medium | The REQ-WARP-MARKERS-009 statement was a playback claim that no released output can observe. | Narrowed: REQ-WARP-MARKERS-009 unreleased; playback excluded in the contract, README and manifest. |
| RVW2-03 | Low | The extracted-execution label said the original code computed each deciding value for the case's inputs. For the conversions it computed the step between seconds and beats; the frame division and multiplication by the rate did not run there, and the run used 48,000 Hz positions six times larger. The rounding ran in another part of the program than the add and the lookup. | Clarified in the contract and the manifest: the frame scaling is static-derived and exact for every case with the label (checked), and the add and lookup use the same rounding operations (static-derived). No label changed. |
| RVW2-04 | Low | The conversion values rest on an untraced step, that a conversion right after opening uses the marker list held after opening, which the stated assumptions did not name. | Stated assumption 8 added, for WARP-MARKERS-039 to 051. |
| RVW2-05 | Low | "A call that breaks more than one rule has no expectation" contradicted WARP-MARKERS-023 to 027, which also lie outside the beat bounds. | Clarified: an add is decided by its first failing check. No case changed. |
| RVW2-06 | Info | Extracted-execution labels. | All 15 checked against the retained raw outputs and re-run bit for bit, as described above. |
| RVW2-07 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RVW2-08 | Info | Computed-by-rules cases. | Accepted, as described above. |
| RVW2-09 | Info | Fixture validity. | All 20 documents pass the structural checker; 007 and 008 are refused only for their marker text; the WAV is generated. |
| RVW2-10 | Info | Evidence identity. | The retained extraction run, the program image it ran, the build of its loader, the structural checker and the schema list were re-hashed on 2026-10-18. All matched their recorded digests. |

## Disposition

**Approved with listed narrowing** (RVW2-01 and RVW2-02), only for the explicit
partial clauses in the contract. Expected results are static-derived,
extracted execution, or computed by extracted-execution rules, as labelled per
case. Extracted execution ran the original program's x86_64 code with the host's
C library in place of the macOS libraries. The arm64 build is inferred to
behave the same. Opening and the other checks of each call are static-derived.
Neither reference nor candidate application cases have run, and no
compatibility pass is claimed. Candidate-only checks cannot replace independent
reference observations. An isolated implementation workspace remains a
prerequisite.

This release supersedes warp-markers-v1, which stays immutable; its fixtures
must not be used, and its case WARP-MARKERS-018 has no expectation here. This
disposition concerns the local reviewed-handoff workflow; it does not authorize
external publication. Preserve this release unchanged.
