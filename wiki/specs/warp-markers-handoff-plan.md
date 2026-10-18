---
id: PLAN-WARP-MARKERS-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Warp markers handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [warp-markers-v1](../../handoff/warp-markers-v1/README.md).
A separate review agent approved it with narrowing
([review record](../../handoff/warp-markers-v1/REVIEW.md)). Manifest SHA-256
`f8546a3e95788074a2cf1cd99564637b8689af853db705fd9beba1af1764ef46`.

All 38 cases are kept. Case 024 now uses a sample time of 900,000 s; no other
expectation changed. The narrowings:

- **Values after opening:** the release grades the values as read from the
  document. Anything the application changes by itself afterwards, such as
  automatic warping, is excluded. Cases 001 and 002 now serve as controls.
- **Tempo-limit and rounding-tie edges:** the bands widen from 0.000001 to
  0.001 BPM and 0.001 grid step, plus a 0.0005 s gap from a neighbouring
  marker's time.
- **Labels:** the TransientResolution labels and the label for code 5 are
  removed.
- **TransientEnvelope:** nothing grades it.

The draft spec needs these changes:

- Split the open-and-save assumption into separate opening and saving
  assumptions.
- Restate REQ-015 as inclusive bounds.
- Mark the REQ-012 and REQ-013 labels as inferred.
- Note that TransientEnvelope is created at 100 without a clamp.

Applied in revision 2 (2026-10-18); rejected: F2 (the review's corpus check shows creation stores `TransientEnvelope` 100 without a clamp, so the default stays static-derived) and RVW-09 (release status text only).

## Decision and boundary

Stage a finite candidate, warp-markers-v1, from
[SPEC-WARP-MARKERS revision 1](warp-markers.md). The candidate follows the
pattern and gates of the [als-container plan](als-container-handoff-plan.md)
and the [release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary),
every expectation is a static derivation; nothing was executed.

The scope is the documented and static-derived part of the draft that does not
depend on [Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling).
Q-021 names the playback mapping, load handling of malformed lists and of
missing or out-of-range values, the Transient Envelope range, the absent-`WarpMode`
default and the spec's assumptions A1 to A3. This candidate therefore excludes,
in addition to every U clause and all audio:

- A1: the empty audio-clip list refusal (REQ-004 first clause, WMK-006);
- A2: everything saved, so every save comparison of the draft. The spec scopes
  A2 to saved values; load and scripting observations keep its load half as a
  stated assumption (finding F1);
- A3: every conversion value (REQ-008 formula, WMK-016 to 019);
- REQ-014 entirely, including "does not refuse" (WMK-025 to 027), and every
  `TransientEnvelope` value and default (finding F2).

What remains is how warp state is read when a set is opened, and which
scripting edits are refused or accepted. Fixtures are new minimal documents and
one generated WAV of silence; no shipped content or audio is included.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | AudioClip warp children and empty single-`Value` form; Sampler/Simpler list and settings in `SampleWarpProperties`; `FluctuationTexture` name; `IsWarped` `true`/`false` | Runtime chooser and tempo omission on save (U); other Boolean spellings; missing `IsWarped` |
| 002 | Attribute form; binary64; released decimal-prefix rule of REQ-TRANSPORT-STATE-004; no prefix refused; no rounding on load | Save text (A2); `Invalid`, `#`, `0x`, inf/nan (REQ-006, Q-021); `Id` (U); values beyond ±1,000,000 (scope limit) |
| 003 | Load clause: strictly increasing list of two or more held as read, in order | Save clause (A2) |
| 004 | Sample-part empty list not refused | Audio clip empty list refused (A1); presentation (U) |
| 005, 006, 009, 014 | None | All (U or Q-021) |
| 007 | Last element is the shadow; scripting remove and move refuse it; never a right neighbour | Placement at 1/32 beat and when (U); "different spacing kept on load" (tagged A2); conversion and playback role; sample-part lists |
| 008 | Both conversions refused on a clip that is not warped | Conversion values (A3); non-audio clips |
| 010 | Seven audio clip settings absent or value-less take defaults | `TransientEnvelope` (F2); `WarpMode` (U); sample-part defaults and the preference |
| 011 | Code table; codes 0–4, 6 held as stored | Chooser display and its short variants (U); code 5 (REQ-014) |
| 012 | Codes and defaults; codes held as stored | Display labels (inferred); internal loop-mode names (F6) |
| 013 | Ranges and defaults of five settings; in-range integers held | `TransientEnvelope` (U); parameter names (F6); out-of-range (REQ-014) |
| 015 | Add: warped, range, position and neighbours, as-given beat checks, rounding, 5–999 BPM per neighbour, none toward the shadow; accepted = no error; remove/move lookup, no-such-marker and shadow refusals; remove without the warped condition | List after accepted edits (U); move limits and accepted moves (U); `warp_mode` setter; interactive edits; non-audio clips; p below the first marker or at a neighbour's time, tempi near the limits (F3) |
| 016 | Rounding in the scripting add and lookup; no rounding on load | Interactive beat setter; sentinel values |

Combined failures have no expectation. Release case IDs are WARP-MARKERS-001
to 038; the payload carries no draft case ID.

### Case disposition

| Draft case | Release cases | Change |
| --- | --- | --- |
| WMK-001, 002 | 001 | Load part only. Settings set to non-default in-range values so that reading is visible |
| WMK-003, 004, 005 | 005, 003, 007 | Load part only (save excluded, A2) |
| WMK-006 | None | A1 |
| WMK-007 | 018 | One Simpler sample part; load only |
| WMK-008 to 013, 022 | None | Unresolved in the draft |
| WMK-014 | None | REQ-007 load clause tagged A2; the draft grades only save text |
| WMK-015 | 033, 034 | Split; on list M1 (shadow beat 3.03125) |
| WMK-016 to 019 | None | A3 |
| WMK-020 | 019, 020 | Split |
| WMK-021 | 009 | Load part; `TransientEnvelope` dropped (F2) |
| WMK-023, 024 | 013 to 017; 001, 011, 012 | Load part; display not graded |
| WMK-025 to 027 | None | REQ-014 (Q-021) |
| WMK-028 | 021 | On list M1 with (0.5 s, beat 1) |
| WMK-029 | 023, 024 | Split; sample now 3 s |
| WMK-030 to 034 | 025, 027, 028 and 029, 031, 032 | WMK-032 split |
| WMK-035 | 035, 036 | Split |

Of the draft's 28 gradable cases, 19 are carried (some split) and 9 are not;
none of the 7 unresolved cases is carried. Twelve cases are new, each for a
static-derived clause without a draft case: 002 (`IsWarped` false), 004
(leading space), 006 (text after the number), 008 (empty text), 010 (no
`Value`), 011 and 012 (transient codes 0), 022 (accepted counterpart of 021),
026 (beat checked before rounding), 030 (upper tempo limit), 037 (move with no
match) and 038 (remove on a clip that is not warped).

## Findings while staging

Spec errors and proposed corrections for a revision 2. This page does not edit
the spec.

- **F1. A2 scope.** A2 says opening and saving with no edit leaves markers and
  settings unchanged, but its Affects column lists only cases that compare
  saved values. Every load observation and scripting case rests on the
  opening half too. REQ-007's "different spacing is kept on load" is tagged A2,
  while REQ-003's equivalent load clause is not. The audio clip's post-read step
  (dossier `0x1027c1c7c`) calls `0x1027b3928`, which sets owner and onset links
  only (corpus `0x1027b3928`, `0x1027b7cf0`, `0x102610134`). Later post-read
  calls (`0x10283b098`, `0x10283adb8`, `0x10256d5ac`) are untraced. Proposed:
  split A2 into an opening half (attached to REQ-003, 007, 008 and 015) and a
  save half. This candidate states the opening half as an assumption (I3).
- **F2. `TransientEnvelope` default.** REQ-010 gives its default 100 as S and
  WMK-021 grades it. REQ-013 records that the parameter is created with
  maximum 1.0, so whether the held default is 100 is the same open range
  question (PRB-S8-06, Q-021). Proposed: mark it U in REQ-010 and drop it from
  WMK-021.
- **F3. Tempo limit form.** `0x1027afd40` returns beat bounds
  nb.beat + Δs·999/60 and nb.beat + Δs·5/60, and the add compares the rounded
  beat with them. This is not a computed tempo. The two agree for Δs ≠ 0 except
  at floating-point edges. At Δs = 0 (p equal to a neighbour's time) the bounds
  collapse, while REQ-015's tempo is undefined. When p lies below the first
  marker's time, the add has no left neighbour and skips the left check (the
  scan's first-element branch); REQ-015 is silent on that case. The candidate
  excludes these inputs.
- **F4. Accepted edits need not change the list.** The insert
  (`0x1027baad8`, corpus) returns without change when a marker with an equal
  `SecTime` or `BeatTime` exists. The delete (`0x1027c6eec`, corpus) returns
  without change when fewer than three markers remain. A remove of the first
  marker of a two-marker list such as M0 is therefore accepted with no
  effect. Proposed: record this under REQ-015 (S after a dossier read).
- **F5.** `move_warp_marker` also has no warped condition (`0x1033bfb94`
  runs only the class test). REQ-015 says this only for the remove.
- **F6.** REQ-012's S labels `LoopOs`, `LoopFwd` and `LoopAlt`, and REQ-013's
  parameter-name column, look like internal value and parameter names rather
  than display text. The payload carries only codes and element names.
- **F7. Stale text.** "Open questions" says no question-register entry exists
  for FEAT-WARP; Q-021 does. "Revision and handoff" says no handoff plan
  exists; this page now does.

## Deliverables

- Payload under `analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1/`:
  [README.md](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1/README.md),
  `AGENTS.md`, `spec.md`, `cases.json` (38 cases), `fixtures/` (18 XML
  documents and `sample.wav`) and a draft `manifest.json`
  (`release_status: candidate-unreviewed`, review pending). The manifest lists
  23 payload files; with itself the package has 24. Draft manifest SHA-256:
  `302ee8def2d46c98c0740febe1bcb5a53df9694e6154dc601e17c8226a8c7903`. Review
  edits will change it.
- Analyst side, never shipped: `warp-markers-v1-analysis/` with
  [build_wm.py](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1-analysis/build_wm.py)
  (fixtures, cases, manifest, cross-check model, mutation check, seal and
  verify), [wm_meta.py](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1-analysis/wm_meta.py)
  (evidence, inferences, traceability, deny-list, draft manifest, evidence
  re-hash), [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1-analysis/traceability.json)
  (every case and every released clause mapped to evidence keys and inferred
  links) and
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1-analysis/author-validation.json).

## Evidence traceability

Evidence is the [S8 run](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/manifest.json)
(manifest SHA-256 `29df9ec7…e607e793`, `Live.arm64` `3a99ceea…d1c383cfad`), the
unretained d7-0001/d7-0002 dossiers cited by the spec appendix, the N1 loader
dossiers and corpus lookups made on 2026-10-18. Each locator was re-read before
inclusion. Per-case and per-clause locators are in `traceability.json`; the
payload contains none of them.

| Release cases | Kept evidence | Inferred links |
| --- | --- | --- |
| 001–008 | Marker registration `0x10260fdd8` (s8-0001); 64-bit getters (d7-0002); N1 loader `0x101487310` and text conversion `0x10152bfb8`; static survey schema and shipped checks | I1, I3; I2 (007, 008) |
| 009, 010 | Audio clip constructor `0x1027b0e40` (s8-0001), `getter-constants.txt`; loader skips absent members | I3 |
| 011–017 | Code lists `0x1026a9ef8`, `0x1027b279c`, `0x1027b29e8` (s8-0002); direct store on load | I3 |
| 018 | Sample-part post-load `0x10288538c` (s8-0002) has no empty test; 4,244 shipped empty lists; element paths of a decoded shipped set | I3 |
| 019–021 | Conversions `0x1033bf160`, `0x1033bf250` (d7-0001); add `0x1033bf42c` (s8-0001) | I7 |
| 022–032 | Add `0x1033bf42c` (range incl. p = length, scan, as-given checks, q()); bounds `0x1027afd40` (s8-0002); is-shadow `0x1026102c0`; insert `0x1027baad8` (corpus) | I3, I4 (range and accepted), I5 (accepted) |
| 033–038 | Remove `0x1033bfa68` (s8-0002); move `0x1033bfb94` (s8-0003); lookup `0x1027c79d0` and delete `0x1027c6eec` (corpus) | I3, I6; I5 (035, 038) |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | Marker times are binary64 members read by the 64-bit conversion branch (the spec's "Double branch assumed") | 001, 003–008 values |
| I2 | A conversion error while a nested value is read stops the open, as for the transport-state-v1 refusals | 007, 008 |
| I3 | Nothing between reading and the observation or call changes markers or settings (F1) | All except 007, 008, 019–021 and 024 |
| I4 | The add's sample length is the clip's sample duration (`0x1027b6954` source untraced); cases keep at least 0.5 s of margin | 022, 024, 031, 032 |
| I5 | After its checks pass, an add or remove raises no further error (no throw in the insert and delete; callees untraced) | 022, 031, 032, 035, 038 |
| I6 | The lookup behaves as its corpus pseudocode reads | 033–038 |
| I7 | The warped test (slot `+0x300`) reflects the loaded `IsWarped` | 019–021 |

## Fixture construction and sanitization

`build_wm.py build` writes every fixture from one template written for this
release: the transport-state-v1 envelope (`MajorVersion="5"`,
`MinorVersion="12.0_12402"`, `SchemaChangeCount="1"`, no container), the
audio-clip path with the ten value children in schema order holding invented
values, and list M1 (three visible markers and a shadow 1/32 beat after the
last). Each clip fixture changes one property. The sample-part fixture is a
Simpler path with an empty list and default settings. The paths and child
orders were checked in a decoded shipped set; no content was copied. The WAV
is 24,000 zero frames, mono, 16-bit, 8,000 Hz (48,044 bytes), written by the
standard-library `wave` module. Two builds are byte-identical.

## Mechanical checks performed

`build_wm.py seal` (CPython 3.11.13 `-I`) wrote the author validation:

- The cross-check model agrees with all 38 expectations. It restates the
  released clauses, including exact rational grid rounding and the tempo
  formula of REQ-015, and raises "no expectation" for excluded inputs. A mutated
  copy of every expectation was detected. The model shares the static evidence
  and is not an oracle.
- Fixtures: ASCII, LF only, final newline, no tabs, the stated envelope, exactly
  one holder; the WAV parameters and all-zero data were checked.
- Hashes and sizes of the 23 listed files match; the inventory equals the
  directory; every case input and sample exists.
- The deny-list covers analyst paths, addresses, internal class and member
  names, recovered message strings, draft case, probe, question and inference
  IDs, tool names, absolute paths and the shipped set's name. Its only allowed
  hit is "decompil" in the forbidden-inputs list of `AGENTS.md`, worded as in
  the released packages. A probe copy with planted terms was flagged.
- In an export copy outside the checkout, `verify` matched all 23 hashes and
  resolved all 6 Markdown links inside the package; an independent
  `sha256sum -c` matched as well.
- Evidence identity on 2026-10-18: all 76 files of the S8 manifest and the
  `Live.arm64` digest matched; the d7 `queries.json` and `manifest.json`
  prefixes match the spec appendix.

Not checked: any reference or candidate execution, and any proof of I1 to I7.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and
   all 38 expectations against the locators. Rule on F1: whether the opening
   half of A2 may stand as the stated assumption I3 or whether all load and
   scripting cases must wait for a probe. Rule on I4 to I7, the 12 new cases,
   and the exclusion of WMK-025 to 027's "opens".
2. **Quality and sanitization review**: behavioral completeness, exclusions in
   both spec and manifest, no internal structure or analyst link, no claim beyond
   static derivation. Confirm that the five public scripting function names and
   the seven refusal-reason labels are acceptable, and that the labels carry no
   recovered message text.
3. **Evidence identity**: decide whether the unretained d7 dossiers suffice or
   must first be copied into a retained run.
4. **Fixture and sharing review** of the 18 authored documents and the
   generated WAV.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/warp-markers-v1/`. Then update the catalog, spec status,
   coverage, indexes and log, and apply F1 to F7 in a spec revision 2.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 38 cases, partial
REQ-WARP-MARKERS-001 to 004, 007, 008, 010 to 013, 015 and 016, with 005, 006,
009 and 014 unreleased. It is not published, and no handoff exists for
SPEC-WARP-MARKERS. This page has no index entry yet; the coordinator adds it.
