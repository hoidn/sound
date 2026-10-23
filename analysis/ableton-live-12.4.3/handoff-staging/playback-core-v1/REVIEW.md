# Review disposition

Release: playback-core-v1, 2026-10-19.

Reviewer: Codex independent handoff-review agent, in a separate review context.
The reviewer did not author the candidate and will not implement the application.
Scope, evidence, fixture validity, sanitization, identities and sharing were
reviewed. Publication outside this staged package belongs to the coordinator.

## Scope approved

Approval covers only the explicit partial clauses of
REQ-PLAYBACK-CORE-001 to 015 and 017 to 020 in [the contract](spec.md).
REQ-PLAYBACK-CORE-016 and 021 to 023 remain unreleased. All 92 cases are
approved with their expected results unchanged.

Sample timing and unwarped clip audio are accepted under the project's offline
render convention. The request sample and settled start define the comparison
vehicle. They do not claim a corresponding interface in the original application.
The clock, boundary, event and audio arithmetic have extracted-execution or
static-derived provenance, as stated per case. Their composition into session
output depends on the statically derived playback paths and the stated
assumptions. It is not a measured application render or compatibility result.

The arithmetic formulas describe observable sample positions and signal values.
They require no particular scheduler, data structure or application architecture.
Restating the launch-grid table and boundary arithmetic makes this package
self-contained; it does not expand any other release's scope.

## Checks performed

- Every case was independently recomputed from its fixture and script using
  the contract's rules. All 82 MIDI cases agree exactly: 592 events, including
  event order, key, unrounded velocity and every allowed render sample.
  The ten audio cases agree at all 4,784 listed sample values. Audio steps and
  gains were selected independently from the retained extracted-execution
  results using the fixture's rate, pitch and gain. The author's expectation
  model was not used by this recomputation.
- A changed expected velocity or audio value was planted in each case. All
  92 mutations were detected. This checks the review comparator, not the
  original application or a candidate implementation.
- All 58 generated sets pass the structural and document-schema checks with
  no deviations, refusal, contradicted case or shape of unknown outcome.
  An additional schema-directed shape check finds no repeated member,
  missing base-value attribute or list item of an unknown class. Every set has
  one track, scene and clip, equal session and freeze slot counts, no devices
  or returns, and tempo and time-signature events equal to the stored values.
- The gzip form and XML envelopes match the contract. The two WAV files are
  mono 16-bit PCM, at 48,000 Hz with 480 frames and at 44,100 Hz with 441
  frames. Both contain only format and data chunks. Every frame equals the
  independently recomputed integer signal formula. They contain generated
  test data, and no shipped audio or metadata.
- The retained evidence manifest and all 153 files it lists were re-hashed.
  The three pinned program images and the launch-boundary results also match
  their recorded digests. These identity checks execute no program functions.
- Every payload file was examined as text, decompressed XML or generated WAV
  data. Independent and existing deny-list checks find no recovered program
  text, internal identifiers, addresses, private paths, restricted links or
  source-to-case traceability. The sole word exception is the forbidden-inputs
  list of the role instructions, as in earlier releases. XML names are
  document-format names.
- A byte-identical copy outside the checkout has every required case input,
  all Markdown links resolve within the package, and every inventory hash
  and size matches. There are no symlinks. No approved public dependency is
  required.

## Findings and scope rulings

| ID | Finding | Disposition |
| --- | --- | --- |
| RPC-01 | The non-integer tempo example is the binary32 value nearest 280/3, rather than nearest the shorter decimal approximation. | Candidate wording is correct; carried into the mutable parent specification. |
| RPC-02 | A press exactly at beat 10/3 cannot be placed on an integer request sample at 90 BPM and 48,000 Hz. Relaunching a clip on its own note beat also depends on excluded event ordering. | The impossible-rate case and the coincident relaunch are excluded. On-line presses of an idle clip are covered. |
| RPC-03 | A tolerance relative to an interpolated result is unsafe near cancellation. | Adopted the candidate's absolute bound: two binary32 units in the last place of the largest source-frame magnitude read by the window. This is limited to the released linear cases. |
| RPC-04 | A song-loop jump shifts later clip-event beats and places them from the new anchor. Independent placement as though no jump occurred can differ by one sample. | The candidate's explicit shift rule is approved. Both readings agree in every released loop case; no general sample-identity claim is approved. |
| RPC-05 | With fades off and the region extending through the file, silence after the final frame cannot reveal the clip's end sample. | REQ-PLAYBACK-CORE-021 and its end-sample cases are excluded. Past-file silence under REQ-PLAYBACK-CORE-020 is independently observable and remains included. |
| RPC-06 | Activation without a grid and the first MIDI note are different observables; immediate activation with a nonzero pre-delay has no graded observable here. | Notes are placed from their lattice beats. Nonzero pre-delay and crossfade output remain excluded. |
| RPC-07 | A nonzero MIDI start offset is evidenced; the unresolved start-offset behavior concerns audio clips. | MIDI start-offset case approved; audio offsets other than zero excluded. |
| RPC-08 | The candidate was labelled unreviewed in its entry points and machine-readable metadata. | This review added, approval and date recorded, entry points corrected, inventory resealed. |

The stated assumptions remain explicit: inferred arm64 equivalence, stored
values reaching audio playback, the loaded global quantization, the grid's
beat-zero anchor, and the macOS library values equal to the selected extracted
steps and gains. These checks do not establish those assumptions.

Tempo changes, clip stops, replacing launches, nonzero audio pre-delay,
crossfades, fades, resampled HiQ audio, per-note expression, overlapping notes,
other launch gestures and modes, and the remainder of the excluded inputs stay
outside this release. No new original-program investigation was needed.

## Disposition

**Approved with listed clarifications**, solely for the explicit partial
clauses and 92 cases above. Neither the reference application nor a candidate
application was run. Conformance to these expectations is not a compatibility
pass. A fresh restricted implementation workspace remains required.

This disposition concerns the local reviewed-handoff workflow. It does not
authorize external publication. Preserve the released package unchanged;
corrections require a new release.
