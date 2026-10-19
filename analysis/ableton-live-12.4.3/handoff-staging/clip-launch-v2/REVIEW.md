# Review disposition

Release: clip-launch-v2, 2026-10-18.

Reviewer: separate review agent (Claude Opus 5.5), launched by the coordinator
in its own handoff-review context. It did not author this candidate and will
not implement it. The one reviewer performed the scope and evidence,
supersession, fixture-validity, quality and sanitization, evidence-identity and
fixture-sharing checks. Publication metadata outside this package is left to
the coordinator.

## Scope and checks

Approval covers only the explicit partial clauses of REQ-CLIP-LAUNCH-001 to
007, 009 and 011 to 018 in [the contract](spec.md), narrowed as listed below.
REQ-CLIP-LAUNCH-015 to 018 are approved only as value functions of explicit
inputs, not as launch timing. REQ-CLIP-LAUNCH-008, 010 and 019 to 023 remain
unreleased.

- Supersession. clip-launch-v1's manifest digest equals the catalog value and
  the value recorded here, and all 55 files it lists still match. The 50
  carried cases are identical case records to clip-launch-v1, in content and
  serialization. In every carried fixture the envelope, `GlobalQuantisation`,
  `AutoQuantisation`, each launch element and old-form follow item of each clip
  that clip-launch-v1 had, and the first scene's follow action are identical to
  clip-launch-v1. The new fixtures only add elements: no element or value of a
  clip-launch-v1 fixture is removed or changed. Within clip-launch-v1's clauses
  the expectations are the same: the new 0 to 100 limit cannot change a
  rescaled pair of chances that both lie in 0 to 100, and the reviewer checked
  that the follow-time formula equals clip-launch-v1's rule whenever the value
  is more than 10⁻⁹ from a halfway point and below 1,000,000 (the rounding
  error of the two binary64 steps is below 6 × 10⁻⁴ lattice steps). The
  superset claim holds. The fixture change list was incomplete (RVC2-05) and
  is now complete.
- Fixture validity. The Live Set structure checker that found the
  clip-launch-v1 defect was run by the reviewer on all 62 fixtures. Against
  each fixture's own format version, no fixture has a schema deviation, and the
  checker finds no structure refusal. Of the structure rules, only the
  repeated-child rule refuses a fixture: CLIP-LAUNCH-019, whose repeated
  `LaunchMode` is the reason that case tests. The other five refused
  cases (017, 018, 020, 021 and 022) are refused only by the value text they
  test. The reviewer also read the structure rules directly for every fixture,
  with its own implementation: two player tracks before one return track, two
  session and two freeze slots on each player track, two scenes, one send per
  track for one return, none on the main or cue track, one send-pre item, 66
  pointee Ids 1 to 66 below `NextPointeeId` 69, unique list-item Ids, a `Value`
  on every base value and no repeated child. Each refused fixture differs from
  the template only at the item its case tests. For the `11.0_405` fixtures
  the rules were read after the renames that conversion makes (RVC2-04).
- Extracted execution was re-run by the reviewer (RVC2-08). The original
  x86_64 code computed every grid length, every stored-value reading, every
  rounded beat and every boundary that the 38 value cases list, and the
  chance correction and follow-time rounding of 25 document cases, from the
  staged arguments and fixture text: 146 computations and 25 document values
  agree bit for bit.
- Every case was read one by one. The reviewer's own executable restatement of
  the contract, written from the contract and not from the author's
  cross-check, agreed with all 100 expected outcomes, held values, saved values
  and computed results, and detected 496 of 496 mutated expectations. The
  worked examples of REQ-012, 013 and 015 to 017 hold, and so does REQ-017
  clause 5 for all 3,424 beats one lattice step from a grid line.
- At least one expectation per released requirement was re-derived from the
  evidence: the launch elements' and follow-action children's types and order
  in the shipped `12.0_12402` class list (REQ-001, 002), the two set items
  (REQ-003), the four label lists (REQ-004 to 007), the initial clip and
  follow-action values (REQ-009), the stored-value reading of −99 (REQ-011),
  the conversion steps 406, 417, 421 and 12203, including the follow time 1
  that step 406 gives an absent one (REQ-014), and, for REQ-012, 013 and 015 to
  018, the runs above together with the arm64 instructions of the clip-grid
  selection and of the beat lattice step.
- Sanitization was checked by the reviewer's own scan of every payload file. No
  source code, recovered program text, internal identifiers, addresses, analyst
  paths, private evidence links, planning, probe, question or assumption
  identifiers or per-case evidence fields are present. The flagged words are
  the provenance label and its definition, the generated sample's file name and
  path inside the fixtures (as in the released structure package), the public
  element name `RemoteableTimeSignature`, which the shipped schema lists and
  shipped clips contain, the forbidden-inputs list of `AGENTS.md`, and
  "probe" in the comparison obligation, worded as in clip-launch-v1.
  SPEC-PLAYBACK-CORE is named by ID only, as the owner of launch timing.
- Scope. After RVC2-01 no runtime, timing, render or display result is
  presented as released. No expectation depends on an open question
  (RVC2-02, RVC2-03). Exclusions appear in both the contract and the manifest
  and agree. Expected results are labeled static-derived or extracted
  execution per case and per computation; reference and candidate execution
  have not run, and no compatibility is claimed.
- In a copy outside the analyst checkout, every Markdown link resolves inside
  the package, every case input exists, the 62 fixtures are distinct,
  well-formed ASCII XML with LF endings, tab indentation and a final newline,
  the sample equals the stated generated sine wave sample for sample, and every
  listed hash and size matches. The fixtures were authored for these cases and
  contain no shipped file content; all are suitable for sharing.

## Rulings on the points raised for this review

1. **Framing of REQ-015 to 018.** The value functions may be released, which
   answers clip-launch-v1's removal of REQ-015: this release states functions
   of explicit inputs, and the playback release, which owns launch timing,
   consumes them. The candidate's wording did not keep that boundary. It
   called them computations "that launching uses", named the rounded beat the
   "press beat" and the function `launch-boundary`, called the global argument
   the set's stored value and said that a Global clip "uses" the song's time
   signature. A reader could take the boundary as the beat at which a pressed
   clip starts, which the playback contract does not say in general. Narrowed
   (RVC2-01): the contract, README, manifest and cases now name the rounded
   beat `rounded_beat` and the function `grid-boundary`; they say that the
   functions are not launch timing, that the boundary is not stated to be the
   beat at which a launched clip starts or takes effect, and that a value case
   is not a launch case. No computed value changed.
2. **The Global clause of REQ-016.** In the parent draft that clause says which
   grid a launch uses. The global value a launch takes rests there on an
   assumption of the playback specification about the engine's copy of the
   set's global quantization, so the draft's static label should name that
   assumption. This package releases only what a clip's setting denotes for
   explicit arguments. The reviewer re-read the program's clip-grid function in
   the arm64 build: a clip value that reads as 0 gives the set's grid, the
   set's own stored global quantization applied to the song's time signature;
   any other value k gives grid k − 1 in the clip's own time signature. As a
   function of explicit arguments the selection is therefore static-derived
   without that assumption. Narrowed (RVC2-02): the argument list now says only
   that the clip and global values are on the scale of the stored items, and
   REQ-016, the exclusions and the manifest exclude which global value, time
   signatures and grid a launch uses.
3. **Follow times outside 0 to below 1,000,000.** The parent draft grades such a
   follow time as held unchanged, from a run of the follow-time rounding alone.
   A later step of opening, the clip's own completion step, was not traced and
   could change or refuse such a value. Excluding the parent's case is upheld.
   The candidate excluded the held value but not whether the document opens;
   that is now excluded too (RVC2-03). The out-of-range chance cases do not
   share the gap: under the structure contract's opening order the follow
   action's correction completes first and leaves both chances in 0 to 100, so
   the clip's later step sees values of the kind that the in-range assumption
   already covers.
4. **Older-version fixtures and the structure audit.** Upheld (RVC2-04). The
   audit measures every document with `12.0_12402` names. For each `11.0_405`
   fixture it therefore reports 16 or 17 undeclared elements, two automation
   envelopes without a target (those of the old-named main track) and session
   slots without scenes. Read directly, after the renames that conversion
   makes (the old scene list becomes the scene list, each name-only scene's
   name becomes its `Name`, and the old main track becomes the main track),
   these fixtures satisfy every traced structure rule and have no shape with
   an unknown outcome. The audit's advice to add a current-form scene list to
   clip-launch-v1's `11.0_405` fixtures is wrong for that version: it declares
   no such list, its scenes hold the name as `Value`, and its conversion treats
   a scene that already has a `Name` as an error. CLIP-LAUNCH-041 and 042, the
   migration cases of the parent draft, use these fixtures and are valid.
5. **Extracted execution.** Re-run as described (RVC2-08), with every process
   below the execution tool's call limit.

Other rulings: the wider chance range (both −100 to 200 with |A + B| ≥ 1) is
accepted; it keeps every computed quotient finite. The authored `11.0_405`
form is accepted with its stated conversion assumption (RVC2-09). Removing the
template's devices is accepted: no case uses them, and without them no fixture
depends on the structure contract's untraced rule for device placement. The
`RemoteableTimeSignature` element is accepted as document vocabulary.

## Findings

| ID | Severity | Finding | Resolution |
| --- | --- | --- | --- |
| RVC2-01 | Medium | The value functions of REQ-015 to 018 were worded as computations that launching uses, with a "press beat", a `launch-boundary` function, a "song position" argument and a case purpose saying a Global clip "uses" the song's time signature. They could be read as launch-timing claims, which belong to the separate playback release. | Narrowed: the rounded beat is `rounded_beat`, the function `grid-boundary`; the contract, README, `AGENTS.md`, manifest and four case purposes say that the functions are not launch timing, that the boundary is not stated to be a launch's start, and that a value case is not a launch case. The parent draft's launch cases are described as not released. No computed value changed. |
| RVC2-02 | Low | The argument list called the global value "the set's stored `GlobalQuantisation`", which, read with REQ-016, could state which global value a launch uses; for a launch that rests on an assumption outside this release. | Narrowed: the clip and global values are values on the scale of the stored items; REQ-016, the exclusions and the manifest exclude which global value, time signatures and grid a launch uses. The selection itself is static-derived from the clip-grid function. No case affected. |
| RVC2-03 | Low | For a follow time outside 0 to below 1,000,000 the contract excluded the value held, but not whether the document opens; a later opening step that could refuse such a value was not traced. | Narrowed: whether such a document opens is excluded in the contract, the README and the manifest. No case uses such a value. |
| RVC2-04 | Info | The structure audit measures `11.0_405` documents with current names and reports false problems for them; its advice for clip-launch-v1's `11.0_405` fixtures is wrong. | Not a package defect. The fixtures were checked against their own format version and against the structure rules read directly. The audit tool should be corrected on the analyst side. |
| RVC2-05 | Editorial | The README fixture change list omitted two additions: `HasStop` on each session slot and an empty device chain on each track. | Completed. The reviewer compared every carried fixture with its clip-launch-v1 fixture element by element; nothing else was added, removed or changed. |
| RVC2-06 | Editorial | REQ-017 clause 4 ended with a verification note ("every grid line … that was checked") instead of a rule. | Restated as clause 5, for the grid lengths of q = 5 to 13 with anchor 0. It follows from clause 2, and the reviewer checked it for all 3,424 beats. |
| RVC2-07 | Editorial | README, `AGENTS.md`, the contract, the cases and the manifest described an unreviewed candidate. | Status set to reviewed local release. This record was added and linked. The manifest review and status fields were filled and the inventory was re-hashed by the reviewer. |
| RVC2-08 | Info | Evidence identity and re-execution. | The arm64 program image and the x86_64 build, the two execution-tool builds, the static evidence run, the extracted-execution run and every file it lists, the structure run, the shipped schemas of the three format versions and clip-launch-v1 match their recorded digests. The reviewer's own run used 63 processes of at most 58 calls each (tool limit 256): 57 grid lengths, 10 stored-value readings, 38 beat roundings, 54 boundaries, 17 chance corrections (CLIP-LAUNCH-029 to 036 and 051 to 059), 8 follow-time roundings and 41 text readings. Every text reads as its correctly rounded value, the text `-0` as negative zero, and the both-zero branch disables follow actions. With no grid and anchor 0, the boundary step itself also returns the rounded beat. |
| RVC2-09 | Info | Conversion of the fixtures' other content from older versions is a stated assumption. | Accepted and partly checked: every conversion step above `12.0_12117` that applies to an element class in the fixtures was read, and none refuses or changes a judged item; for `11.0_405`, every step above 405 that can report an error or stop and that applies to an element class in the fixtures was read, and none fires for the fixtures' content. The other steps were not read in full, so the assumption stays stated. |

## Corrections for the parent draft

These do not change this package. The draft specification should be revised
to:

- name the playback specification's assumption about the engine's global value
  beside REQ-016's Global clause, which states which grid a launch uses;
- relabel REQ-011's out-of-range follow-time clause: the run shows the
  follow-time rounding only, and the held value, and whether opening refuses
  such a value, are unknown until the clip's own completion step is read; the
  unknown clause about that step should name follow times as well;
- name the fixture forms of its release cases: complete minimal sets, and the
  authored `11.0_405` form;
- keep the value functions of REQ-015 to 018 apart from launch timing in its
  wording, as this release does.

## Disposition

**Approved with listed narrowing** (RVC2-01 to RVC2-03), only for the explicit
partial clauses in the contract, with 100 cases. Expected results are
static-derived or extracted execution, as labeled per case and per
computation. Extracted execution ran the original program's x86_64 code on a
Linux host; the arm64 build is inferred to behave the same. Neither reference
nor candidate application cases have run, and no compatibility pass is claimed.
Candidate-only checks cannot replace independent reference observations. An
isolated implementation workspace remains a prerequisite.

This release supersedes clip-launch-v1, which stays immutable and valid for its
own clauses, but whose fixtures must not be used. This disposition concerns
the local reviewed-handoff workflow; it does not authorize external
publication. Preserve this release unchanged.
