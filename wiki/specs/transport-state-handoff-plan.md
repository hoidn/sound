---
id: PLAN-TRANSPORT-STATE-HANDOFF
type: research
status: current
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Transport-state handoff: candidate and review plan

## Decision and boundary

Stage a finite candidate, transport-state-v1, from
[SPEC-TRANSPORT-STATE revision 1](transport-state.md). It follows the structure
and gates of the [midi-config-v2 plan](midi-config-v2-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
a static-supported contract may be reviewed without a reference run. Every
expected outcome is static-derived and unexecuted, and no compatibility is
claimed.

This page is the analyst-side plan and traceability record. It is not an
implementation input. The candidate is **staged, not reviewed and not
released**. Nothing has been published into `handoff/`.

## Scope

Before staging, the analyst re-read each included clause against the kept
dossiers and corpus excerpts listed under
[evidence traceability](#evidence-traceability). The candidate carries 18 of the
draft's 23 cases.

| Requirement | Included in v1 | Excluded remainder |
| --- | --- | --- |
| 001 | Paths and value types of the six values; homonyms are different values | Units (inferred only) |
| 002 | Empty single-`Value` shape for the four Transport values and both `Manual`s; those four written once; relative order of all 33 known children | Whether KeyMidi or the other six children are written; whitespace and layout; envelopes (PRB-N1-07) |
| 003 | All S clauses | None |
| 004 | Decimal-prefix reading, leading U+0020 skipped, trailing text ignored, no prefix refused | `0x`, `inf`, `nan`, `Invalid`, `#` forms; locale; non-space whitespace |
| 005 | REQ-004 then nearest binary32 | `#` 8-digit and `Invalid` forms |
| 006 | Accepted spellings without trailing spaces after a leading space or `+`; refusals | Spaces on both sides or `+` plus trailing spaces (see contradictions); `-` sign |
| 007 | Defaults 8, 16, 0, off and 120 for missing element or `Value` | Time-signature default (PRB-N1-04); missing parents |
| 008 | Duplicate known non-KeyMidi Transport children and duplicate `Manual` refused; unknown Transport child skipped and not saved | Unknown attributes (versioned-mode condition, PRB-N1-08); repeated unknown children |
| 009 | None | All of it (PRB-N1-03, PRB-N1-06) |
| 010 | Code meaning only, without a case | Load or edit paths (PRB-N1-04) |
| 011 | Boolean, integer and fixed-precision text for in-range finite values; positive zero | `Invalid` and `#` output; negative zero; logarithm edge near powers of ten |
| 012 | None | All of it (PRB-N1-04, PRB-N1-05) |

The range bounds stated in the candidate (loop start and position 0 to
<1,000,000, loop length 1 to <1,000,000) are a scope limit this plan chose. Their
lower bounds come from REQ-009, and the upper bound is arbitrary but explicit.
Loop end, derived on load, is part of REQ-009 and is not released.

### Case disposition

| Draft case | Candidate | Change |
| --- | --- | --- |
| TS-001–007, 009, 011–016, 021, 022 | Released as written | Requirement lists widened where a save is judged (TS-001: +002, 011; TS-022: +011). TS-022 judges only the order and the four values, not the presence of other children |
| TS-008, TS-020 | Released, narrowed | Saved `Manual` text only. The draft also expected the automation event text, but whether 12.4.3 writes the envelopes is U (REQ-002, PRB-N1-07) |
| TS-010 | Not released | Contradiction 1 below |
| TS-017–019 | Not released | REQ-009 effective values unknown |
| TS-023 | Not released | Contradiction 2 below |

Fixtures are new minimal XML documents: no `.als` container, envelope
`MajorVersion="5"`, `MinorVersion="12.0_12402"` and `SchemaChangeCount="1"`, the
10 Transport children with filler values, and `Tempo`/`TimeSignature` with only
`Manual`. They contain no automation and no scenes. The candidate spec states how
the validation analyst must embed them in a full set: equal envelope events,
disabled scene overrides, the factory default set and a `.` locale. The
factory-default precondition neutralizes PRB-N1-02, because the factory template
holds the same values as the constructor defaults (8, 16, 0, off, 120).

## Contradictions and corrections for the draft owner

1. **REQ-006 / TS-010 versus the container analysis.** The draft accepts
   ` +201 ` after trimming. The disassembly of `0x1002fd908` (n1-0006 dossier,
   `0x1002fd97c`–`0x1002fd9a4`) computes the converted length as
   `min(len − start, end index after trailing spaces)`. That keeps the trailing
   space when the value has leading spaces or `+`, which agrees with
   [document container native](../research/document-container-native.md#corrections-to-the-packet-notes-and-cases)
   (N2-014 relabelled unknown). The converter `0x1002fda78` is untraced. So
   ` +201 ` is unknown, likely refused. Proposed: correct the REQ-006 S clause,
   relabel TS-010 U and give it a PRB-N1-06-style probe.
2. **TS-023 versus the draft's own scope.** The draft's "Timing and state" section
   puts edits after load out of scope, yet TS-023 edits the meter in the UI. The
   UI path, the logic-layer initialisation (`0x1026f7420`) and envelope handling
   are untraced. Proposed: drop TS-023 or relabel it U.
3. **REQ-011 "Zero is written `0`".** The traced zero branch also applies to
   −0.0 (`fcmp d0,#0.0`), so negative zero would be written `-0`. Proposed:
   say "positive zero".
4. **REQ-004 `#` forms.** The hex-to-bytes helper `0x10152cff8` is not kept. The
   byte swap after it implies most-significant-first, but that is inferred.

## Evidence traceability

Analyst-only. Image `Live.arm64` SHA-256 `3a99ceea…d1c383cfad`. Run
[n1-transport-state-v1](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/manifest.json)
(dossiers `results/n1-000x/functions/`, corpus records in `corpus-excerpts.jsonl`)
and [s1-static-v1](../../analysis/ableton-live-12.4.3/r2/s1-static-v1/manifest.json).

| Clause | Checked against | Residual inference |
| --- | --- | --- |
| 001 paths, types | `schema-survey.json` `path_resolution` (`tempo.manual`, `timesig.manual`, `transport.*` for 12.0_12402), `homonyms_latest`; `documents-survey.json` roots (5, 12.0_12402, 1) | None for location |
| 002 shape, order, presence | Writer `0x101486cdc` (n1-0008: flag-4 attributes, then `flags & 6 == 0` children in registration order; slot `+0x150` = `0x101483030` returns 0); `mValue` flag 4 (`0x101564330`, `0x4fffffffc`); `check_registry_order.py` 33/33 identical; slot `+0x148` = `0x100249f88` (returns 0) for ALoopOn and ALoopStart (`vtable-reads.txt`) | Vtables of ALoopLength, ACurrentTime and both `Manual` classes not read; shared base behaviour inferred |
| 003 | `0x10152bfb8` bool branch (n1-0006); `0x10152bf4c` length plus `memcmp` (corpus); `"0"` at `0x105ab32f8` | None |
| 004, 005 | `0x10152bfb8` float/double branches: `Invalid` by length 7, `#` by length 9/17, otherwise strtod with a no-consumption throw, `(float)` conversion | macOS strtod correct rounding and grammar (C standard); locale |
| 006 | `0x1002fd908` pseudocode and disassembly (n1-0006) | Converter `0x1002fda78` untraced (decimal, no whitespace skipping assumed) |
| 007 | Loader `0x101487310` walks node members (n1-0008); slot `+0xc8` empty (`0x100249f70`); ATransport constructor disassembly: `[x19,#0x1c8]`=8.0, `#0x1e0`=16.0, `#0x228` false, `#0x240`=0.0, matching member offsets `0x1c0`/`0x1d8`/`0x220`/`0x238` (+8) in `0x10275dccc`; tempo 20/999/120 constants (`0x1026f4d98` disassembly) passed to `0x1026f0bcc`, which stores 120 into `param_4[0x49]` = `mpManual` `0x240`+8 (`0x1026f0390`); compound element without attributes is legal (`0x10152adb0` type-0 branch) | Store body `0x101568960` not kept; tempo post-load `0x1026fc4cc` callees unread (envelope equal in all cases); top-level load untraced |
| 008 | Add slot `0x101472624` "already has member" (n1-0007); unknown child → ignored frame `0x1015299e0` (n1-0007) | Fate of the `Unexpected node` record under the versioned, equal-change-count condition (in-memory ChangeCount unknown) |
| 010 | Encoder `0x101abea70`, list builder `0x1026e10a8` loops 5 × 99 (n1-0008) | None for the formula |
| 011 | Formatters `0x101520c70`, `0x101520dbc` (`Invalid`, `#%8.8X`/`#%16.16llX`), `0x101431584`/`0x101431788` disassembly (precision 9/17 − k, `frintm`/`frintp` on `log10`, zero precision 8/16, `%.*lf`, trailing-zero strip); `0x10143157c` widens float; bool `0x101520b08`; `number-format-check.txt` 376/376 per field | libm `log10` near powers of ten; printf rounding of exact binaries |
| Refusal outcome | Throws carry the corrupt-document key (`0x10148229c`) | Catch step inferred, shared with the container packet |

## Deliverables

- Payload (staged):
  [transport-state-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v1/README.md),
  `AGENTS.md`, `spec.md`, `cases.json` (18 cases), `fixtures/TS-*.xml` (18) and
  a draft `manifest.json` (review fields pending). The manifest lists 22 payload
  files (23 with itself). Draft manifest SHA-256:
  `45c60b410c13aacb1998e85e30ba546bcf28f75085d0c362970b45d620ac4202`. Review
  edits will change it.
- Analyst side, never shipped:
  [build_ts1.py](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v1-analysis/build_ts1.py)
  (`build`, `seal`, `verify`; holds the case table and an independent
  cross-check model) and
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/transport-state-v1-analysis/author-validation.json).

## Mechanical checks performed

These used `python3 -I build_ts1.py seal` with CPython 3.13.9:

- The cross-check model agrees with all 18 expectations. Six mutated
  expectations were each detected. The model is not an oracle: it re-reads the
  same evidence.
- No fixture hits an exclusion. Fixtures are ASCII with LF endings and no tabs.
- All 22 hashes and sizes match. The inventory equals the directory, and there
  are no symlinks.
- The copy at `/var/tmp/sound-analysis/scratch/stage-ts/transport-state-v1`
  passed both `build_ts1.py verify` and the midi-config-v2 reviewer's
  `verify_copy.py`. All 7 Markdown links resolve, the hashes match, and neither
  deny list (addresses, internal class and function names, tool names, analyst
  paths and IDs, probe IDs, derivation and traceability terms, base-document
  name) has a hit.

Not checked: no reference or candidate was executed, and no expectation has
independent proof.

## Review gates still required

1. **Scope review** in a separate context. Check every included clause against
   the traceability table. Give particular attention to the residual inferences,
   the REQ-006 narrowing, the range bounds and the decision to release REQ-010
   without a case.
2. **Quality and sanitization review.** Check behavioral completeness, that
   exclusions appear in both `spec.md` and the manifest, that no internal
   structure or analyst link remains, and that nothing claims more than static
   derivation. The comparison convention and the embedding rule must be
   intelligible without analyst access.
3. **Evidence identity.** Confirm that the N1 image digest matches the pinned
   12.4.3 slice.
4. **Fixture and sharing review** of the 18 authored XML documents.
5. **Finalize**: add `REVIEW.md`, set the manifest review fields,
   `release_status` and `release_date`, re-run `seal`, re-verify in an isolated
   copy, and record the manifest hash in the handoff catalog.
6. **Publish** only after approval: copy unchanged to `handoff/transport-state-v1/`
   and add a row to the [handoff index](../../handoff/index.md). In the same
   change, update the spec status, coverage, indexes and log, and apply the
   draft corrections above. Track the remaining unknowns in
   [Q-012](../questions.md#q-012-transport-state-load-and-save-semantics).
7. An isolated implementation workspace is still unprovisioned.
