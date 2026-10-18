---
id: PLAN-CLIP-LAUNCH-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Clip launch settings handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [clip-launch-v1](../../handoff/clip-launch-v1/README.md),
approved with narrowing by a separate review agent
([review record](../../handoff/clip-launch-v1/REVIEW.md)); manifest SHA-256
`ecf755b1c4ea2d3356bd31ff3fdc0efc4034b05a6ecb11c08d8502c86d945bea`. All 50 cases
are kept, and the reviewer's independently written model agrees with every one. The narrowings are:
- REQ-015 is removed, because a grid length is observable only by launching.
- REQ-001 read-back is claimed only for Booleans and numbers of at most six significant digits; no case grades saved text.
- The "kept as read" assumption is limited to the stated ranges.
- REQ-005 and 014 are reworded.
- The REQ-011 message prefixes are not carried.

For the draft spec: remove the REQ-011 prefixes and the 150/50 chance example, or mark them unknown. Grade the saved 3.0000002 follow time as a held value, mark the both-forms clip unknown, and drop the proposal to release REQ-015 to 018. The tables below describe the staged candidate.

## Decision and boundary

Stage a finite candidate, clip-launch-v1, from
[SPEC-CLIP-LAUNCH revision 1](clip-launch.md). The candidate follows the
[als-container plan](als-container-handoff-plan.md) and
[transport-state plan](transport-state-handoff-plan.md), and the
[release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
every expectation is a static derivation. Nothing was executed, and no
compatibility is claimed.

The scope covers stored values only: launch fields and set quantization as
document data, value domains and labels, reading and refusal, missing items,
the two corrections made on opening, conversion of older follow actions, and
the grid length each quantization value stands for. Launching itself is out of
scope. Q-017 holds the timing, launch modes, Legato, velocity and follow-action
behavior ([Q-017](../questions.md#q-017-clip-launch-timing-and-launch-modes)).
Q-017 also lists missing or out-of-range set quantization, step 17 and the
clip-grid assumption A1, so the candidate releases none of them.

This page is the analyst-side plan and traceability record. It is not an
implementation input. The candidate is **staged, unreviewed and unpublished**.
Nothing has been copied into `handoff/`.

## Scope

| Requirement | Included in v1 | Excluded remainder |
| --- | --- | --- |
| 001 | Launch elements of session MIDI and audio clips and arrangement MIDI clips: location, types, reading rules restated from transport-state-v1, refusal, repeated launch element refused, saved shape, relative order and read-back value; homonyms | Saved text (U); indentation; take-lane and groove-pool clips |
| 002 | Ten children, types, reading; saved with exactly these children in order | Scene compound except conversion; FollowActionEnabled observation (D, no rule) |
| 003 | Location, integer type, refusal | Saved form (no claim in r1); GlobalQuantisationKeyMidi |
| 004 | Values and labels | API names |
| 005 | Clip and global values, labels, k − 1 and Global meaning | API names and spellings |
| 006 | Values and labels | API names; effect on recording |
| 007 | Values, labels, short "Again" | Where each label set is shown (U) |
| 008 | None | All of it (missing set fields U; Q-017) |
| 009 | Initial clip and follow-action values for absent items, written on save | Bounds as behavior; jump index 0 in shipped content; creation paths (U) |
| 010 | None | All of it (preference mapping U; PRB-S5-10; Q-017) |
| 011 | Out-of-range enum values of at most nine digits do not refuse | Value held, displayed or saved, timing (PRB-S5-09); set-level out-of-range (Q-017); Live API setters and messages |
| 012 | Rescaling for chances 0 to 100 in binary32, halves away; enabled unchanged except the zero case | Negative chances and chances above 100 (CLC-023); scene chances |
| 013 | Rounding to 1/3,843,840 for 0 ≤ x < 1,000,000, not within 1e-9 of a half-multiple | Negative, non-finite and near-tie values |
| 014 | Steps 406, 417, 421 for clips of `11.0_405` documents; 12203 for scenes of `12.0_12117`; no conversion at `12.0_12402` | Step 17 (Q-017); 12008 (no value change); the 406 error for a clip with both forms; absent old A/B or chances; other versions |
| 015 | Grid length per global value and time signature, definitional, no case | Lattice rounding of bar (a no-op for d in {1, 2, 4, 8, 16}); use at launch |
| 016–023 | None | All of it (A1, A4, U clauses; Q-017) |

Assumptions carried, named behaviorally in the payload: A2 (absent items keep
initial values; present values kept without range adjustment), A3 (corrections
run for every clip, after conversion), A5 (conversion order) and a new A7: the
chance values written through the float's setting call are kept as computed.
A7 is the r1 REQ-012 U clause, which the candidate restricts to integral
results in 0 to 100. A1, A4 and A6 are not needed. Labels define meaning only,
and no displayed text is graded.

### Case disposition

The 50 release cases carry 24 r1 cases, some narrowed, and 26 new cases. Each
new case exercises a static clause of r1 that had no case.

| r1 cases | Candidate | Change |
| --- | --- | --- |
| CLC-001, 002, 003, 004, 005, 006, 007, 008, 010, 011, 012, 019, 020, 021, 022, 024 | 002, 001, 017, 018, 019, 006, 007, 009, 011, 023, 024, 029, 030, 031, 032, 037 | Re-authored on minimal fixtures; B1/B3/B4 shipped edits replaced by template edits |
| CLC-009 | 005 | Authored arrangement clip in place of the 90 shipped clips of B5 |
| CLC-014, 015 | 026, 027 | Narrowed to `opens` |
| CLC-025 | 038 | Judges the held value, not saved text (finding F3) |
| CLC-026, 027 | 046, 047 | Authored `12.0_12117` scene; judges held values, not the saved scene (F7) |
| CLC-028, 029 | 041, 042 | Authored `11.0_405` fixtures; the authentic-set need moves to the comparison obligation (F8) |
| CLC-013, 030 | Not released | REQ-010 and REQ-008 unreleased |
| CLC-016, 017, 018 | Not released (018's values via a document in 003) | Scripting interface excluded |
| CLC-023 | Not released | Chance above the 0–100 bound (F4) |
| CLC-031–056 | Not released | Launch timing; REQ-016 to 019 |

## Findings while staging

Proposed corrections for a spec revision 2. This page does not edit the spec.

- **F1.** The revision note proposes releasing REQ-016 and the S clauses of
  017 and 018. All three rest on A1, and Q-017 lists A1's uninterpreted
  slot-state test as an open gap. Under the selection rule none can be
  released yet. The note contradicts Q-017.
- **F2.** The scope excludes "the exact text of error messages". Yet REQ-011,
  CLC-016 and CLC-017 grade the message prefixes `Invalid launch mode` and
  `Invalid launch quantization`.
- **F3.** REQ-001 marks the number text written on save as unknown. CLC-025
  nevertheless expects a saved follow time that "parses to exactly
  11531521/3843840", which holds only if the saved text carries enough digits.
  The candidate judges the held value. It judges saved numbers only where they
  have short exact forms (integers, 0.5).
- **F4.** CLC-023 (chances 150 and 50) lies outside the chance bounds 0–100 of
  REQ-009. The A2 evidence for storing without a range check covers enum
  indices: the loader stores the index directly. It does not cover a bounded
  binary32 value. transport-state-v1 likewise gave out-of-range floats no
  expectation. The case should be relabelled U or given a probe variant.
- **F5.** REQ-013 cites only the pseudocode of `0x10156580c`. The bytes
  `0x101565860`–`0x1015658ac` were re-read on 2026-10-18 with
  [fp_opcodes.py](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1-analysis/fp_opcodes.py):
  `fcmp`/`fcsel` (sign), `fmadd` (x + s·(1/3,843,840)·0.5), `fabs`,
  `fmul 3843840.0`, `frintm`, `fdiv`, `fmul` (sign), which is the same sequence
  as the grid rounding in `0x101aaae44`. This confirms "nearest, halves away
  from zero" except within floating error of a half-multiple, which the
  candidate excludes. The corpus truncating cast is harmless here, because the
  half step is added before `frintm`.
- **F6.** REQ-014 calls a clip that has both the old fields and `FollowAction`
  "a read error". In `0x1014b6d14.c` the error report is followed by a
  no-return trap. The kept evidence does not show whether opening refuses the
  document or stops the application. It is excluded, and r2 should mark it U.
- **F7.** The step-12203 clause rests on pseudocode (`0x1014c04d0`, s5-0004;
  disassembly retained, not cited). The Scene writer was not read, so the saved
  form of a scene is not established. CLC-026 and 027 grade "saved IsLinked".
  The candidate grades scene values held after opening. The reviewer should
  check the retained disassembly.
- **F8.** CLC-028 and 029 have no fixture. The candidate authors minimal
  `11.0_405` documents in the old clip order of the `11.0_405` schema. The
  obligation states that the reference comparison needs an authentic set of
  that version, which the bundle lacks.
- **F9.** REQ-012 and 013 speak of "a clip's follow action". The correction is
  a follow-action post-load hook, so it presumably applies to scenes too.
  Nothing graded depends on it, because scene chances in the cases are 100
  and 0.

## Deliverables

- Payload (staged):
  [clip-launch-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1/README.md),
  `AGENTS.md`, `spec.md`, `cases.json` (50 cases), `fixtures/CLIP-LAUNCH-*.xml`
  (50) and a draft `manifest.json` (`release_status: candidate-unreviewed`,
  review pending). The manifest lists 54 payload files; with itself the package
  has 55. Draft manifest SHA-256:
  `91f46d7cee570f00b52320cca06dac85fc39e31b091400778b84057d2d4668e4`. Review
  edits will change it.
- Analyst side, never shipped: `clip-launch-v1-analysis/` with
  [build_clip.py](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1-analysis/build_clip.py)
  (fixtures, cases, manifest, cross-check model, seal and verify),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1-analysis/traceability.json),
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/clip-launch-v1-analysis/author-validation.json)
  and `fp_opcodes.py`.

## Evidence traceability

Evidence is the [S5 run](../../analysis/ableton-live-12.4.3/r2/s5-clip-launch-v1/manifest.json).
The run manifest has SHA-256 `a5758e8290ed4ab8…`, and all 87 listed files
matched on 2026-10-18. `Live.arm64` is `3a99ceea…d1c383cfad`, which matched
the same day. The transport-state reading rules come from the released
[transport-state-v1](../../handoff/transport-state-v1/spec.md) and its
[N1 evidence](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/manifest.json).
Per-case keys are in `traceability.json`. The payload contains none of them.

| Release cases | Clauses | Kept evidence | Assumptions |
| --- | --- | --- | --- |
| 001–005, 012–020 | 001, 002 | `static-survey.json` field order and homonyms; `registry-order-check.txt`; AClip and AFollowAction vtables: loader `0x101487310`, writer `0x101486cdc`; N1 `0x10152bfb8`, `0x1002fd908`, add-member `0x101472624` | none |
| 006–010, 021 | 003, 005, 006 | Label lists in `0x10266f738` (s5-0001), `0x102438d00` (s5-0002); clip grid `0x102442998` `sub w1,w0,#1` | none |
| 011, 022 | 002, 007 | `0x102503ea0`, `0x102505724` | none |
| 023–025, 036 | 009 | Constructors `0x102436fc4`, `0x102505030`, `0x102505724`; `0x1015743b0` | A2 |
| 026–028 | 011 | N1 loader stores the enum index directly; `0x10156675c` is not called | A2 |
| 029–036 | 012 | `0x1025044b4` disassembly `0x1025044f0`–`0x102504584`; post-load slot `+0xd0` | A2, A3, A7 |
| 016, 037–040 | 013 | `0x101565624(…,1,1)` in `0x102505030`; F5 byte check | A2, A3 |
| 041–045 | 014 (406, 417, 421) | `0x1014b6d14.c`, `0x1014b82d8.c` (s5-0003); `0x1014b8b00` (s5-0002, `mov w1,#0x4` at `0x1014b8be4`); `11.0_405` schema clip order; schemas.json | A2, A3, A5, A7 |
| 046–050 | 014 (12203) | `0x1014c04d0.c` (s5-0004); registry `0x10148ec98` | A2, A3, A5 |
| none | 015 | `0x101aaae44` (s5-0001), jump table `0x105846ef8`; targets for 1, 3, 5, 10, 12 and 13 spot-checked in the dossier on 2026-10-18 | none |

## Fixture construction and sanitization

`build_clip.py build` writes every fixture from a template written for this
release. It reads no shipped file. The template is a 12.0_12402 envelope with
one MIDI track and a session clip holding only the five launch elements, at
the values of a new follow action, followed by `GlobalQuantisation` 4 and
`AutoQuantisation` 0. Each case changes the template as its purpose states.
The `11.0_405` fixtures use the old clip form: the five follow fields directly
under the clip, after `VelocityAmount`, as in that schema, and no `Scenes`,
which that version's `LiveSet` lacks. The fixtures are decoded XML, as in
transport-state-v1. The container belongs to als-container-v1.

The payload contains no API names, message strings, assumption or probe IDs,
shipped file names or r1 case IDs. Assumptions are described behaviorally
(RVA-05 precedent). The vocabulary avoids schema-file terms: "suffix number"
replaces "translator number" (RVA-04 precedent), and "conversion step" names
the migration steps. The payload names three schema identifiers and the
factory default set's version, both acceptable under RVA-11.

## Mechanical checks performed

`python3 -I build_clip.py seal` (CPython 3.13.9) wrote the author validation:

- The cross-check model agrees with all 50 expectations. A mutation of each
  case's first judged value was detected in 50 of 50 cases. The model restates
  the same static evidence and is not an oracle.
- Fixtures: 50 distinct inputs, all well-formed. They are ASCII with LF endings
  and a final newline, contain no tabs, and none hits an exclusion.
- Hashes and sizes of the 54 listed files match. The inventory equals the
  directory, all case inputs exist, and there are no symlinks. A second
  `build` and `seal` produced the same manifest hash.
- The deny list covers addresses, internal class and member names, schema-file
  vocabulary, tool and derivation terms, analyst paths, probe, question,
  assumption and r1 case IDs, API names, message strings and shipped file
  names. It found no hit. A probe copy with planted terms was flagged.
- In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export/clip-launch-v1`,
  `verify` matched all 54 hashes and resolved all 7 Markdown links inside the
  package. An independent hash recheck matched as well, and the copy is
  byte-identical to staging.

Not checked: any reference or candidate execution, A2, A3, A5 and A7, and
F6 and F7.

## Review gates still required

1. **Scope review** in a separate context. Check every included clause and all
   50 expectations against the locators. Rule on A2, A3, A5 and A7 and on F1
   to F9. Decide whether the scene cases and the authored `11.0_405` fixtures
   stay graded, and whether REQ-015 stays as a definitional clause without a
   case (transport-state-v1 REQ-010 precedent).
2. **Quality and sanitization review**: behavioral completeness, exclusions in
   both spec and manifest, no internal structure or analyst link, and no claim
   beyond static derivation. Labels define meaning only.
3. **Evidence identity**: the S5 manifest and image hashes matched on
   2026-10-18. Re-check before release.
4. **Fixture and sharing review** of the 50 authored XML documents.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/clip-launch-v1/`. Then update the catalog, spec status, coverage,
   indexes, log and Q-017, and apply F1 to F9 to r2.
7. This page has no index entry yet. Add one to the [spec index](index.md) with
   the release record.
8. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 50 cases, partial
REQ-CLIP-LAUNCH-001 to 007, 009 and 011 to 015, with 008, 010 and 016 to 023
unreleased. It is not published, and no handoff exists for SPEC-CLIP-LAUNCH.
