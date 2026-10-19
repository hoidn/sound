# Review disposition

Release: mixer-values-v2, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the
coordinator in its own handoff-review context. It did not author this candidate
and will not implement it. The one reviewer performed the scope and evidence,
supersession, fixture-validity, quality and sanitization, evidence-identity and
fixture-sharing checks. Publication metadata outside this package is left to
the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-MIXER-VALUES-001 to
009, 013 and 014 in [the contract](spec.md). REQ-MIXER-VALUES-010, 011, 012
and 015 remain unreleased.

- Supersession. The mixer-values-v1 manifest digest equals the catalog value
  and the superseded digest recorded here, and every file it lists still
  matches. The 37 carried case records are equal to mixer-values-v1's, in the
  same order and with the same serialized text. Each listed mixer-values-v1
  fixture digest matches its file.
- Fixture change. In all 37 fixtures every mixer value text, `EnabledByUser`
  and the crossfade curve are equal to the mixer-values-v1 fixture of the same
  case. No element of a mixer-values-v1 fixture is missing and no element
  count changed; the added elements are those of the change list. Each fixture
  differs from MIXER-VALUES-001 only in its case's value lines, at most three.
  The tracks are MIDI 1, audio 2 and return 3 in every fixture.
- Fixture validity. The analysts' structural checker for Live Sets was run
  unchanged on an exported copy of every fixture. It finds no schema deviation,
  no structural refusal and no shape of unknown outcome in any of the 37, and
  every case effect is consistent. All 37 are expected to open; none is
  expected to be refused. The reviewer's own check of the shapes that checker
  does not evaluate (a base value element without `Value`, a repeated member,
  a track of an unaccepted class) found none. The same checker finds no refusal
  in the mixer-values-v1 fixtures but a shape of unknown outcome in all 37 (a
  missing send setting per return track), as the supersession states.
- Carried expectations. The reviewer's own restatement of the contract agrees
  with all 37 carried expected results and with the worked examples of
  REQ-006 and REQ-007. No fixture falls under an exclusion. A mutation of any
  listed field is caught.
- Computed expectations. Every one of the 43 computed cases was re-run by
  extracted execution of the same x86_64 code. All 43 results
  equal the payload exactly. All 101 points of both fader curves, read back
  through position to gain, equal the reviewer's restatement of the REQ-005
  construction with the snap applied to each point before the next is
  computed. Under a snap applied only to the finished points, 37 volume points
  would differ by one to three binary32 steps; the send curve is unaffected.
  The reviewer's restatement of both conversions also agrees with the original
  on 1,601 further gains and positions. The curve points of the round-trip
  cases lie at least 0.167 of a binary32 step from a rounding midpoint, and a
  one-step change of either curve point that MIXER-VALUES-051 uses moves its
  position by at most 3.8·10⁻⁹. The pan-law formula agrees with every result
  within the comparison.
- Round trip of other gains. Of 1,601 random binary32 gains on both curves,
  none a curve point, 765 did not return unchanged through both conversions of
  the original code, by up to two binary32 steps. Volume 0.3 returns
  0.30000004. From −6 dB to 0 dB on the volume curve, 44 of 61 sampled gains
  did not return. The contract now claims only the seven run curve points and
  the counting fact for that range (RVM2-01).
- Sanitization was checked by the reviewer's own scan of every payload file.
  No source code, recovered program text, internal identifiers, addresses,
  analyst paths, private evidence links, planning identifiers or per-case
  evidence fields are present. The flagged words are the provenance label
  "x86_64 slice, glibc substitutions", "decompilation" in the forbidden-inputs
  list of `AGENTS.md`, and "probe" in the comparison obligation, all as in
  earlier releases.
- Scope. No runtime, timing, display or audio result is released. No
  expectation depends on an open question. Exclusions appear in both the
  contract and the manifest and agree. Reference and candidate execution have
  not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, and every listed hash and size matches.
  The 37 fixtures are distinct, well-formed XML, ASCII with LF endings and a
  final newline. They contain no shipped file content and no sample.

## Scope rulings

- Computed values without an observation channel. Accepted. The cases state
  values that a candidate computes from listed inputs, and the comparison
  obligation says that the original application offers no observation of them.
  They are not compatibility evidence.
- Exact round trip under the stated exponential assumption. Accepted for the
  seven curve points only. Gains between curve points have no round-trip
  expectation and no bound.
- The 10⁻¹² bound for pan-law gains and crossfade levels. Accepted. It admits
  both 0 and the original's 6·10⁻¹⁷ for the cross-feed of MIXER-VALUES-070 and
  for a level of 0. For every other expected value it admits nothing beyond the
  two binary32 neighbours.
- Crossfade positions. Released only at multiples of 1/4, which are also
  multiples of 1/64. The extracted execution at ±0.95 is not released.
- Pan-mode amount. Released for w of 0 and 1 without the mapping from the
  stored pan mode, which is labelled inconsistently in the parent.
- Template set. It holds no clip, sample or device and no envelope on a mixer
  value. Opening rests on static-derived structural rules, which the checker
  measures.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVM2-01 | Medium | REQ-005 said that most gains between curve points cannot return unchanged. Extracted execution of 1,601 random gains shows 765 that do not return, under half. The counting argument holds only for the range it names. | Narrowed. The contract states the counting fact for the volume curve from −6 dB to 0 dB only, and that neither an exact return nor a bound is released for other gains. The manifest scope says the same. No case affected. |
| RVM2-02 | Medium | REQ-013 stated how the four gains scale the input channels into the outputs, and called the pan a balance control without cross-feed. Both describe the application to audio, which this release excludes. | Narrowed. The gain names are labels for computed values. Which signal each gain scales, and whether, where and when the audio path applies them, are excluded in the contract and the manifest. The consequences are restated as values. No case affected. |
| RVM2-03 | Low | REQ-014 said that each curve has a level at every position from −1 to 1. At other positions the original gives values that the listed ones do not suggest, and how levels are applied is excluded. | Narrowed. Levels are released at the seven listed positions only. The listed levels define no level at other positions, for example by interpolation. No case affected. |
| RVM2-04 | Low | REQ-013 described the original's internal arithmetic and placed the cross-feed difference at a quarter turn, which fits R→L but not L→R. | Restated as a result. In MIXER-VALUES-070 the original gives about 6·10⁻¹⁷ for L→R and R→L where the formula gives 0, and the 10⁻¹² bound absorbs it. |
| RVM2-05 | Low | The change list said that each track gains a name, colour, automation envelopes, group and output routing. The cue track gains none of them. The fixture provenance omitted the scenes' follow action. | Corrected in README change 1, the manifest's fixture changes and the fixture provenance. The element comparison found no other unlisted change. |
| RVM2-06 | Editorial | README, AGENTS, contract, cases and manifest described an unreviewed candidate. | Status set to reviewed local release. This record added and linked. Manifest review and status fields filled; inventory re-hashed by the reviewer. |
| RVM2-07 | Info | The REQ-005 snap feeds each point forward. | Confirmed by extracted execution at all 101 points of both curves. The contract states it that way. |
| RVM2-08 | Info | Fixture validity. | All 37 fixtures pass the structural checker. None is expected to be refused. |
| RVM2-09 | Info | No case exercises a group track or a computed input other than those listed. | The group-track rules are supported but untested; other computed inputs have no expectation. No expectation was invented. |

## Disposition

**Approved with listed narrowing** (RVM2-01 to RVM2-05), only for the explicit
partial clauses in the contract. All 80 cases are kept. The 37 carried case
records and expectations are mixer-values-v1's, on rebuilt fixtures. Expected
results are static-derived or extracted execution, as labeled per case.
Extracted execution ran the original program's x86_64 code with glibc in place
of the macOS libraries; the arm64 build is inferred to give the same results
within each comparison. Neither reference nor candidate application cases have
run, and no compatibility pass is claimed. Candidate-only checks cannot replace
independent reference observations. An isolated implementation workspace
remains a prerequisite.

This release supersedes mixer-values-v1, which stays immutable. This
disposition concerns the local reviewed-handoff workflow; it does not authorize
external publication. Preserve this release unchanged.
