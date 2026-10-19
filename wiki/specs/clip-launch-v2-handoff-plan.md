---
id: PLAN-CLIP-LAUNCH-V2-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Second clip-launch handoff: candidate and review plan

## Decision and boundary

Stage a superseding candidate, clip-launch-v2, from
[SPEC-CLIP-LAUNCH revision 4](clip-launch.md). It follows the
[clip-launch-v1 plan](clip-launch-handoff-plan.md), the
[transport-state-v2 plan](transport-state-v2-handoff-plan.md) (a superseding release with
extracted-execution cases), the [als-container plan](als-container-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff).

Why a new release: [clip-launch-v1](../../handoff/clip-launch-v1/README.md) has invalid
fixtures. Opening a Live Set always runs the validation walk of
[SPEC-LIVE-SET-STRUCTURE](live-set-structure.md), and 49 of the 50 v1 fixtures hold a
session slot without a freeze sequencer (REQ-LIVE-SET-STRUCTURE-006). Of their cases, 43
expect the set to open, and 6 refusal cases no longer isolate the rule they test
([audit](../../analysis/ableton-live-12.4.3/r2/t11-structure-v1/released-fixture-audit.json)).
Released payloads are immutable, so v2 carries all 50 v1 case records unchanged, rebuilds
every fixture on the minimal set T11-MIN, and adds the clauses settled since v1. Those are
REQ-012 and 013 by extracted execution (X2), REQ-015 to 018 as a value contract only, and the
REQ-016 and 017 corrections of revision 3.

Launch timing in samples belongs to [SPEC-PLAYBACK-CORE](playback-core.md) and its own
release. v2 therefore releases the grid and boundary arithmetic only as functions of explicit
arguments. It contains no request sample, pre-delay, activation sample or move to B + g.

New cases carry the provenance "extracted execution (x86_64 slice); arm64 equivalence inferred".
Carried records keep "static-derived". Opening, reading the text, saving and the grid selection
of REQ-016 stay static-derived in every case. No reference application or candidate has run, and
no compatibility is claimed (ADR 0002, ADR 0003).

This page is the analyst-side plan and traceability record, not an implementation input. The
candidate is **staged, unreviewed and unpublished**. Nothing has been written into `handoff/`.

## Scope

Selection rule: release only D, S and X clauses with exact values. Exclude S-cond and U clauses,
runtime, timing and audio, and anything that rests on an open item of
[Q-017](../questions.md#q-017-clip-launch-timing-and-launch-modes) or
[Q-024](../questions.md#q-024-playback-core-render-semantics).

| Requirement | Included in v2 | Excluded remainder |
| --- | --- | --- |
| 001 to 007, 009, 014 | v1 clauses, unchanged | As in v1 |
| 011 | v1 clause. New: chances outside 0 to 100 follow REQ-012 (X); −99 counts as Global in the REQ-016 value (X getter) | Held, displayed or saved value of out-of-range enums; held value of an out-of-range follow time (finding F2); velocity, loop and jump values out of range (U) |
| 012 | Rescaling as v1, plus the 0 to 100 limit (A7 settled, X); chances both 0–100, or both −100 to 200 with \|A+B\| ≥ 1; −0 counts as 0 | Scenes (U); other chance pairs |
| 013 | Binary64 formula (X, 66 of 66) for 0 ≤ x < 1,000,000; v1's near-half exclusion removed | Out-of-range follow times (F2); scenes |
| 015 | Grid-length table as a value G(q, n/d), n 1–99, d ∈ {1, 2, 4, 8, 16} (X, 6,463 of 6,463) | Use at launch |
| 016 | The grid a clip's setting denotes, from explicit arguments (clip value, global value, clip and song signatures). Selection S (clip grid `0x102442998`), −99 getter X | Which grid a launch uses at run time (A1 and playback-core A4); reading the signatures; several signature entries (U) |
| 017 | Press beat L(t) and B = L(a′ + ⌈(p − a′)/g⌉·g), a′ = max(0, a), for explicit t, g, a (X); triplet next-line correction | Which t and anchor a launch uses; A4 (anchor 0); pre-delay, B + g move, E = B − o, samples (SPEC-PLAYBACK-CORE); anchor after a meter change (U) |
| 018 | No grid: B = L(t) (S) | "No delay once handled" (timing) |
| 008, 010, 019 to 023 | None | All of it |

### Case disposition

The 100 cases comprise 50 carried v1 cases, 12 new document cases and 38 value cases.

| Candidate | Source | Note |
| --- | --- | --- |
| CLIP-LAUNCH-001 to 050 | clip-launch-v1, same IDs | Records byte-identical as JSON; fixtures rebuilt (below) |
| 051 to 055 | CLC-057; REQ-012 examples 5/3, 1/199, 99.5/0.5, −0/0 | X `follow.json` chances |
| 056 to 059 | CLC-023, 058, 059; REQ-011 example −10/−10 | X; out-of-range chances |
| 060 to 062 | CLC-060; two further X near-half values | X `follow_time` (formula ≠ exact rounding) |
| 063 to 067 | REQ-015 table | X `grid` |
| 068 | REQ-016 and REQ-011 −99 | Grid X, selection S |
| 069 to 095 | CLC-031 to 054, 062, 063, 064 in value form | clip-grid then launch-boundary; CLC-054 and 064 carry beats only, not request samples |
| 096 to 100 | REQ-017 press rounding (PRB-S5-01 presses), triplet lines and one-step presses (sweep), anchor arithmetic (CLC-055's arithmetic), REQ-018 | X except the g = 0 boundary (S) |
| Not released | CLC-013, 016 to 018 (API), 030, 055 (U), 056 (U), 061 (F2) | Unreleased requirements or U |

## Findings while staging

Proposed for a spec revision 5. This page does not edit the spec.

- **F1. REQ-016 label.** The Global bullet ("uses the set's global value with the song's time
  signature") is labelled S (A1 settled). [REQ-PLAYBACK-CORE-007](playback-core.md#req-playback-core-007--launch-request-and-grid-settles-spec-clip-launch-a1)
  labels the same selection S-cond (its A4: the engine's global value is the loaded
  `GlobalQuantisation`), and clip-launch's own A1 row says A4 remains an assumption. The
  bullet should name playback-core A4. v2 avoids the dependency, because it releases only the
  value the setting denotes, from the static clip-grid and song-grid functions.
- **F2. Out-of-range follow times.** REQ-011 grades a follow time below 0 or from 1,000,000 as
  X "held unchanged" (CLC-061). Yet A2 (r3) says that "a later step that could change such a
  value is still untraced, except for the chances", and REQ-011's U clause says that the clip's
  own post-load hook was not read. X ran only the member's rounding. Either that hook should be
  shown not to touch `FollowTime`, or the clause should become S-cond or U. CLC-061 is not
  released.
- **F3. Fixture section.** The spec's fixtures B1 to B6 are edited shipped documents. Its
  release cases now use authored T11-MIN sets, as SPEC-LIVE-SET-STRUCTURE asks of other specs.
  The spec should name that fixture form, and the 11.0_405 form below, for its document cases.
- **F4. Audit tool (not the spec).** `released-fixture-audit.json` measures every document
  with 12.0_12402 names. For the 11.0_405 fixtures CLIP-LAUNCH-041 to 045 it recommends a
  12402-form `Scenes` element, which the 11.0_405 schema does not declare (scenes there are
  `SceneNames`, renamed by step 414). Run unchanged on v2, it reports five false
  "slots without scenes" shapes for the same reason (`fixture-audit-run.json`).
- **F5. Integer text.** REQ-001 cites REQ-TRANSPORT-STATE-006, which transport-state-v2
  extended: it decides the `-` sign and other spellings. clip-launch-v1 and v2 restate the
  narrower v1 rule, which leaves those spellings without expectation, so nothing conflicts. The
  stored −99 and −1 of CLC-062 and 063 therefore enter v2 only as integer arguments of the
  value function. A later revision could carry the transport-state-v2 rule.

## Deliverables

- Payload (staged): [clip-launch-v2/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v2/README.md)
  (supersession, change list, fixture change list), `AGENTS.md`, `spec.md`, `cases.json`
  (100 cases), `fixtures/CLIP-LAUNCH-*.xml` (62), `fixtures/Samples/T11-tone.wav`, and a draft
  `manifest.json` (`release_status: candidate-unreviewed`; supersedes clip-launch-v1 with its
  manifest digest). The manifest lists 67 payload files; with itself the package has 68. Draft
  manifest SHA-256: `50f4c1ea7f9daa778a574e8054f316c76ada749bfb1dede83e686b93e39946a8`. Review
  edits will change it.
- Analyst side, never shipped, in `clip-launch-v2-analysis/`:
  - [build_v2.py](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v2-analysis/build_v2.py),
    which builds, seals and verifies, with `fixtures_v2.py` (T11-MIN bases and version forms),
    `cases_v2.py`, `model_v2.py` (cross-check model reusing v1's `build_clip.py`) and
    `meta_v2.py`;
  - [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v2-analysis/traceability.json),
    with a source, X reference, evidence and assumptions for every case;
  - [fixture-changes.json](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v2-analysis/fixture-changes.json),
    listing for each fixture its version, its edits from the base and, for carried cases, the
    launch content kept from v1 and the clips the base adds;
  - `author-validation.json`, `schema-check.jsonl`, `fixture-audit-run.json` and
    `export-verify.json`.

## Evidence traceability

| Release cases | Clauses | Kept evidence | Assumptions |
| --- | --- | --- | --- |
| 001 to 050 | v1 clauses | As in the [v1 plan](clip-launch-handoff-plan.md#evidence-traceability) (S5, N1) | A2, A3, A5 as in v1 |
| 051 to 059 | 011, 012 | [X2](../../analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/manifest.json) `results/follow.json` chances (setter limit; enabled setter recorded); r3 A2 static extension | A2, A3, arm64 |
| 060 to 062 | 013 | X2 `follow_time`, flag 1 | A2, A3, arm64 |
| 063 to 068 | 011, 015, 016 | X2 `grid` (6,463 rows), `enum_getter`; clip grid `0x102442998` (s5-0001) | arm64 |
| 069 to 100 | 015 to 018 | X2 `boundary_cases`, `gridline_sweep`; g = 0 skip (S) | arm64 |
| all fixtures | — | T11-MIN `make_fixture.py`; `schema_check.py`, `fixture_audit.py` (t11-structure-v1) | Conversion of the other content of 12117 and 405 fixtures does not refuse (new, stated) |

The X2 run manifest has SHA-256 `aaa42a0b…cc1af`, and all 16 files it lists matched on
2026-10-18. Each X-backed expected value is a hand-written literal, and `seal` compares it bit
for bit with the X2 record its `xref` names. No query server was used, and nothing was
executed except the build scripts and the T11 checkers.

## Fixture construction and sanitization

The base is T11-MIN, regenerated by `make_fixture.build` and rendered byte-identical to
`T11-MIN.xml` (checked by assertion), with its two devices removed. The device list is V in the
minimal-set table, T11-MIN's return and main tracks already have empty lists, and removing the
devices drops SPEC-LIVE-SET-STRUCTURE's A6 from every opening case. NextPointeeId stays 69, above
the remaining 66 pointees. Version forms:

- `12.0_12117`: MinorVersion, and the undeclared `FileRef/SourceHint` and the
  `MidiControllerRange` of `TimeableEnum` and `TimeableTimeSignature` removed.
- `11.0_405`: `MainTrack` becomes `MasterTrack` and `Scenes` becomes `SceneNames`, whose name-only
  scenes carry the name as attribute `Value`. Track and clip `Color` becomes `ColorIndex`. Both
  clips use the old form with follow items 4, 0, 0, 1 and 0. Undeclared elements (also
  `EnabledByUser`, `NoteProbabilityGroups`, `ProbabilityGroupIdGenerator`) are removed. The
  renames reverse conversion steps that the v1 reviewer read in `review/other-steps.c`.
  Removing an undeclared element changes nothing that is read, because the reader skips it.

Each case's fixture is its base plus the v1 edit, restated (`cases_v2.CARRIED`), or the new
edit. CLIP-LAUNCH-005 adds an arrangement clip in the T11-MIN MIDI-clip form. The sample is
`make_fixture.wav` output, 176,444 bytes and generated.

The payload names no T11-MIN, packet, probe, question, assumption or CLC ID. It holds no address
or internal class name, and no link outside the package. One allowed deny-list hit remains: the
document element `RemoteableTimeSignature` inside every fixture's clip `TimeSignature`. It is
public document vocabulary, present in every shipped clip, and the reviewer should confirm
it. The payload mentions SPEC-PLAYBACK-CORE by ID only, as the owner of launch timing.

## Mechanical checks performed

`python3 -I build_v2.py seal` (CPython 3.13.9) wrote `author-validation.json`:

- 100 cases. The model agrees with every expectation, and mutating each case's first judged
  value was detected in 100 of 100. Every X-backed value equals its X2 record bit for bit. All
  50 carried records equal the v1 records.
- In every carried fixture the launch content equals v1's at each location v1 had: envelope,
  `GlobalQuantisation`, `AutoQuantisation`, the launch and old-form children of each clip, and
  the first scene's follow action.
- Every fixture equals its base plus its listed edit. Each refused case's base opens under the
  model, so the edit is the only defect.
- `schema_check.py` against each fixture's own schema (`schema-check.jsonl`) found 62
  documents, 0 deviations and no refusal by the traced structure rules. `fixtures_v2.measure`,
  which applies the 405 renames, found no refusal and no unknown shape.
- `fixture_audit.py`, run unchanged on a copy, reported 0 refused, 0 contradicted and 0
  non-isolating fixtures. Its 5 unknown shapes are F4.
- Hashes and sizes of all 67 listed files match. The inventory equals the directory, there are
  no symlinks, the 14 Markdown links resolve inside the package, and the deny list has no hit.
- A second `build` and `seal` gave the same manifest hash. In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export/clip-launch-v2`,
  `verify` and `sha256sum -c` matched 67 of 67, and the copy is byte-identical to staging.

Not checked: any reference or candidate execution, A2, A3, A5, arm64 equivalence, the
conversion of the 12117 and 405 fixtures' other content, and F1 and F2.

## Review gates still required

1. **Scope review** in a separate context. Rule on whether REQ-015 to 018 may be released as a
   value contract. The v1 review, RVC-01, removed REQ-015 because a grid length is observable
   only by launching. v2 answers that the launch-timing release consumes these values, and that
   the payload states that the application shows them only through launch timing. Also rule on
   F1 and F2, the wider chance range, and the authored 405 form with its new conversion
   assumption.
2. **Fixture review.** Confirm that each fixture is a valid set and that its change list is
   complete: README and `fixture-changes.json`. Rule on removing the devices and on the
   `RemoteableTimeSignature` allowance.
3. **Quality and sanitization review**, **evidence identity** (re-hash X2, S5 and T11), and
   **finalize** (REVIEW.md, manifest review fields, re-seal, isolated export, catalog hash).
4. **Publish** only after approval: copy unchanged to `handoff/clip-launch-v2/`, then update the
   catalog (and its fixture-defect note), the spec status, coverage, indexes, log and Q-017, and
   apply F1 to F3 in r5. Add this page to the [spec index](index.md) with the release record.
5. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 100 cases, partial REQ-CLIP-LAUNCH-001 to 007,
009 and 011 to 018, with 008, 010 and 019 to 023 unreleased. It is not published.
clip-launch-v1 remains the only release for SPEC-CLIP-LAUNCH, and its fixtures stay invalid.
