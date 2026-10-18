---
id: PLAN-MIXER-VALUES-HANDOFF
type: research
status: current
updated: 2026-10-18
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Mixer values handoff: candidate and review plan

## Review outcome

Released 2026-10-18 as [mixer-values-v1](../../handoff/mixer-values-v1/README.md).
A separate review agent approved it with listed corrections
([review record](../../handoff/mixer-values-v1/REVIEW.md)). The manifest
SHA-256 is `5f6b8401b9324d0cf3d60da47d190e61b93e1935f96995128021f29c9f39cd60`.

All 37 cases are kept, and no expected result changed.

- **REQ-008 and REQ-009:** both clauses are kept. The reviewer checked them
  against the machine code: the `On` and `Off` text, and the seven curve names,
  in order, for `CrossfadeCurve`.
- **Independent model:** it agrees with every case, including pan 0.33 giving
  `17R`. No graded input is within 0.1 dB of −69.7 dB.
- **Wording corrections:** the volume upper-bound wording, a stated display
  assumption, and `On` and `Off` added to the comparison obligation.

The draft spec needs three fixes:

1. Add citations for REQ-008 and REQ-009.
2. Correct REQ-002. 1.99526238 is one binary32 step above the nearest value to
   10^(6/20).
3. Drop or define the `EnabledByUser` clause in MV-001. No case grades it.

## Decision and boundary

Stage a finite candidate, mixer-values-v1, from
[SPEC-MIXER-VALUES revision 1](mixer-values.md). The candidate follows the
pattern and gates of the [als-container plan](als-container-handoff-plan.md),
the [transport-state plan](transport-state-handoff-plan.md) and the
[release workflow](../workflows.md#release-a-handoff). Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md#specification-and-verification-boundary)
every expectation is a static derivation; nothing was executed.

The scope is what opening a document establishes: where each mixer value is
stored, the value it is read into, and the value text or code name the
application gives it. Excluded: REQ-011, which is conditional on
[Q-019](../questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine);
every audio render case (REQ-011, 013, 014); the U-only requirements 012 and
015; the fader curves (005); and saving (010), whose 12.4.3 part is U
(PRB-S9-07). The release is therefore display and storage only. It applies the
correction on the [research page](../research/mixer-values.md#candidate-requirements-for-spec-mixer-values)
(float32 pan 0.33 displays `17R`) as a new case, and keeps the −69.7 dB
boundary out of every graded input.

This page is the analyst-side plan and traceability record, not an
implementation input. The candidate is **unreviewed and unpublished**. No
reference or candidate execution has run, and no compatibility is claimed.

## Scope

| Requirement | Included | Excluded remainder |
| --- | --- | --- |
| 001 | Mixer at `<track>/DeviceChain/Mixer` for all six track types; the value elements, their text locations and relative order; main-only `CrossFade`; `LiveSet/CrossfadeCurve`; same rules for every track type | Other mixer children (controller ranges, automation and modulation targets, `On`, view state); other orders; group tracks have the clause but no case |
| 002 | `Volume/Manual` binary32 gain; expectations from 0.0003162277571 to 1.99526238 | New-mixer default and range (track creation is an edit); stored range text; cue volume as preview level (U) |
| 003 | One holder per return on audio, MIDI, group and return mixers, none on main and cue; `Send/Manual` binary32 gain from 0.0003162277571 to 1 | `EnabledByUser` meaning and new-holder value; the return's own send; more than one return; holder `Id` other than `0` (U, PRB-S9-07) |
| 004 | Pan and split ranges −1 to 1; pan mode codes 0 Stereo, 1 Split Stereo | New-mixer defaults; effect on audio (013) |
| 006 | Volume and send text rule for in-range gains | Surface binding and the second text form (U, Q-019); inputs within 0.00005 dB of a text boundary; \|dB\| ≥ 100 (unreachable) |
| 007 | Pan text rule for pan and both splits | ±0.25, ±0.75 ties (U); surface binding |
| 008 | `Speaker` Boolean, text On/Off | `SoloSink` meaning (U, Q-019); new-mixer default |
| 009 | `CrossFadeState` codes A/None/B; crossfader location and −1 to 1; curve codes 0–6 and names | New-mixer default; curve shapes and crossfade effect (014); crossfader orientation and text |
| 005, 010–015 | None | All of it |

### Case disposition

| Draft case | Release case | Change |
| --- | --- | --- |
| MV-001 | 001 | Narrowed: the `EnabledByUser` meaning and the return's own send are not judged. A MIDI track is added, and main and cue list volume (main also pan and crossfader) |
| MV-002, 003, 005–009 | 002, 003, 006–010 | As written |
| MV-004 | 004, 005 | Split, one value per fixture |
| MV-010, 011 | 015, 016 | As written |
| MV-012 | 018 | As written |
| MV-013, 014, 015 | 019–024 | Split |
| MV-016 to 019 | 027 to 030, 035 | MV-017 split into 028 and 029 |
| MV-020–022 | Not released | REQ-010: the graded output is the 12.4.3 save, the U part (finding F4) |
| MV-023–026 | Not released | REQ-005: positions unobservable in scope; last-ulp platform values |
| MV-027 | Not released | Track creation is an edit; saved defaults are REQ-010's U part |
| MV-028, 040–045 | Not released | U |
| MV-029–039 | Not released | Audio renders that need measurement; MV-029–034 also depend on Q-019 |
| New | 011–014, 017, 025, 026, 031–034, 036, 037 | Each exercises an S or D clause with no draft case: two-decimal strip (011); MIDI, return and cue tracks (012–014); send floor (017); pan 0.33 (025); main pan (026); curve codes 0, 1, 3, 4, 6 (031–034, 036); crossfader (037) |

Draft case IDs do not appear in the payload. The mapping is in
`traceability.json`.

## Findings while staging

These are proposed corrections for a spec revision 2. This page does not edit
the spec.

- **F1.** REQ-008's On/Off text has no locator in the appendix row. The evidence
  is in the S9 run: `0x10271b660.c` lines 284–287 pass the text object from
  `0x10143b884` (corpus record kept, vtable `0x106670bc8`). `image-reads.txt`
  gives that vtable's `+0x28` as `0x10143ba28`, whose kept corpus record
  returns "Off" for 0.0 and "On" otherwise.
- **F2.** REQ-009 cites the curve name list `0x102672204`, but not its binding
  to the set. The C1 corpus record `0x102672448` (the set constructor, not
  retained) initialises an enum with that list and index 2. The binding of
  that member to `CrossfadeCurve` is untraced, so it stays an inferred link
  (I3). Census while staging: 375 of the 376 shipped LiveSet documents store
  `2` and one stores `6`. The spec mentions only B0.
- **F3.** The revision note lists the first candidate as REQ-001, 002, 003,
  004, 006, 007, 009 and 010 "with MV-001–026". MV-023–026 exercise REQ-005,
  which that list omits. REQ-008 (MV-018) is static, yet it is missing from
  the list.
- **F4.** MV-020–022 are labelled "S; U part of REQ-010". Every output they
  grade is what a 12.4.3 save writes, and that is the U part. Under the spec's
  own rule ("the U parts ... must not be graded"), nothing in them can be
  graded. Proposed: relabel them U until PRB-S9-07 runs, or state the 12.4.3
  save as an explicit inferred clause with its evidence.
- **F5.** The comparator sentence "Malformed text ... follows the value text
  rules of SPEC-TRANSPORT-STATE" is not supported for mixer classes. Row 015
  says the loader rule was not re-traced for them. In schema `12.0_12402`,
  `Tempo` is a `TimeableSongTempo`, while volume, pan and send are
  `TimeableFloat`, so the transport-state-v1 check does not carry over by
  class identity. The candidate accepts only plain decimal text and records
  the reading as I1.
- **F6.** REQ-015 leaves some values out: volumes and sends in
  (0, 0.0003162277571), sends ≤ 0, a crossfader outside −1 to 1, and curve
  codes outside 0–6. The candidate excludes every value outside the stated
  domains.
- **F7.** MV-001 grades R's send as disabled and A's as enabled. No S or D
  clause defines what `EnabledByUser` does that can be observed.
- **F8.** REQ-006 says gains "within a few float32 ulps of −69.7" are not
  graded, but gives no width. The same platform `log10` dependence also
  applies at every three-decimal halfway point and at ±0.0005 dB. The
  candidate uses 0.00005 dB at each of them, at least 2.5 times the worst-case
  uncertainty in range (about 2·10⁻⁵ dB near −70 dB, from a two-step `log10f`
  error plus the product rounding). The closest graded gain, 0.5, is
  9.99·10⁻⁵ dB from a halfway point. A first choice, 1.01840961 at
  5.02·10⁻⁵ dB, was replaced by 1.5.
- **F9.** The recorded 0.33 → `17R` correction has no draft case. The
  candidate adds MIXER-VALUES-025.

## Deliverables

- Payload: [mixer-values-v1/README.md](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v1/README.md),
  `AGENTS.md`, `spec.md` (behavioral contract, comparison convention and
  reference obligation), `cases.json` (37 cases), `fixtures/` (37 XML files)
  and a draft `manifest.json` (`release_status: candidate-unreviewed`, review
  pending). The manifest lists 41 payload files; with itself the package has
  42. Draft manifest SHA-256:
  `c4ccc14b33f06b014df11104f223f0221f71dcb00c2800f21593d04e727ea3e4`. Review
  edits will change it.
- Analyst side, never shipped: `mixer-values-v1-analysis/` with
  [build_mv1.py](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v1-analysis/build_mv1.py)
  (fixtures, cases, manifest, cross-check model, seal and verify),
  [traceability.json](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v1-analysis/traceability.json)
  (each case and each released clause mapped to evidence keys and inferred
  links) and
  [author-validation.json](../../analysis/ableton-live-12.4.3/handoff-staging/mixer-values-v1-analysis/author-validation.json).

## Evidence traceability

Evidence comes from the [S9 run](../../analysis/ableton-live-12.4.3/r2/s9-mixer-v1/manifest.json)
(manifest SHA-256 `6a1686b3…66871`, 89 files) and the
[D8 queries](../../analysis/ableton-live-12.4.3/r2/d8-mixer-v1/manifest.json)
(`8231ad12…2aed7`, 30 files). Both use `Live.arm64` `3a99ceea…d1c383cfad`.
`build_mv1.py seal` re-hashed every file on 2026-10-18, and all matched. On
the same day the analyst re-read these locators: `0x10143a290.c`,
`0x101437334.c`, the `0x101431c6c` disassembly at `0x101431ca8`–`0x101431d38`,
the `0x102183bf4` disassembly, `0x102658f54.c` lines 70–96, `0x10271b660.c`
lines 284–287, the corpus records `0x10143b884`, `0x10143ba28`, `0x102672204`
and `0x102672448`, and `image-reads.txt`. Locators per case are in
`traceability.json`. The payload contains none of them.

| Release cases | Draft source | Kept evidence | Inferred links |
| --- | --- | --- | --- |
| 001 | MV-001, narrowed | All rows below; `static-survey.json` `documents.tracks`, `returns_per_doc`; schema `TrackDevice`, `MainTrackDevice`, `TrackSendHolder` | I1–I6 |
| 002–010 | MV-002–009 | s9-0001 `0x10271b660` (volume setup at `0x10271be44`, text format (3,1,1,1) at `0x10271c138`); `image-reads.txt` gain ranges; s9-0002 `0x102183bf4` (log10f × 20 in float32); s9-0001 `0x101437334`, `0x101431c6c` | I1, I4, I6 |
| 011–014 | New | As 002–010, plus the shared constructor for every track type (`static-survey.json` schema) | I1, I4, I6 |
| 015–017 | MV-010, 011; new | s9-0002 `0x102658f54` lines 72–96 (the send's own (3,1,1,1) text format, `0x1026f0b58(0, 1, curve(0))`) | I1, I4, I6 |
| 018–026 | MV-012–015; new | s9-0002 `0x10143a290`; d8-0002 `0x101431c60`; s9-0001 `0x10271c734`; vtable `0x106670828` | I1, I6 |
| 027 | MV-016 | As above, plus s9-0004 `0x101567ad8` (pan mode entries) | I1, I2, I5, I6 |
| 028, 029 | MV-017 | `0x10271bf38` (entries A/None/B); d8-0002 `0x1026ef0dc` | I1, I2 |
| 030 | MV-018 | F1 locators | I1, I6 |
| 031–036 | MV-019; new | F2 locators; s9-0003 `0x101aed36c` (same order of seven tables) | I1, I2, I3 |
| 037 | New | `static-survey.json` (main `CrossFade` `0`, range `-1`–`1`) | I1 |

| Link | Inference not established by kept evidence | Affects |
| --- | --- | --- |
| I1 | Mixer value text is read by the generic loader: plain decimal to the nearest binary64, then to binary32; Booleans `true`/`false`; codes in decimal. Not re-traced for these classes (F5). Every fixture number rounds the same way directly or through binary64 | Every value |
| I2 | An enum's value text is its entry name | Pan mode, crossfade assignment and curve names |
| I3 | `CrossfadeCurve` is the enum the set constructor initialises with the seven names (F2) | 001, 031–036 |
| I4 | Apple `log10f` is within one binary32 step of the correctly rounded result. The model tolerates two steps and the margin covers more | Volume and send texts |
| I5 | Both split pans use the pan text object. Pseudocode `0x10271c734` assigns the same singleton for all three; the confirmed branch is Pan's | 001, 027 |
| I6 | The primary text form (unit and `-inf`) is shown somewhere in the user interface. The second form (`0x1014374b4`, no unit and no `-inf`) is excluded, and the spec's comparison obligation makes a different form inconclusive | Every text |

## Fixture construction and sanitization

`build_mv1.py build` writes every fixture from one template authored for this
release. The template has the transport-state-v1 envelope (`MajorVersion="5"`,
`MinorVersion="12.0_12402"`, `SchemaChangeCount="1"`), audio, MIDI and return
tracks with invented `Id`s 11–13, main and cue tracks, and `CrossfadeCurve`
`2`. Each track has only `DeviceChain/Mixer` with the value elements in schema
order. No shipped file is read or copied. Three case numbers also occur in
shipped sets: main volume `0.7367056608` (Sample Reference.als), MIDI volume
`0.03548133373` (APC40 Demo.als) and cue volume `1.99526238`. They are bare
numbers and carry no content. The payload names public document elements,
UI-visible value texts and the code names. It contains no display names of
parameters and no recovered messages.

## Mechanical checks performed

`python3 -I build_mv1.py seal` (CPython 3.13.9) wrote the author validation:

- The cross-check model reproduces all 37 hand-authored expectations. A
  mutation of one expected entry in each case was detected 37 times out of 37.
  Ten excluded probes (pan 0.25, volume 2 and 0.0001, send 1.0000001, the
  exponent form, −69.7 dB, a −6.0625 dB tie, pan mode 2, curve 7, speaker `1`)
  were all rejected. The model shares the same static evidence and is not an
  oracle.
- Fixtures are distinct, well-formed, ASCII with LF endings, no tabs and a
  final newline. Each differs from the template only in its stated lines.
- All 41 hashes and sizes match. The inventory equals the directory, there are
  no symlinks, and every case input exists. Two consecutive build and seal
  runs gave the same manifest digest.
- The sanitization deny-list covers analyst paths, addresses, internal class
  and member names, tool and function names, probe, question and draft-case
  IDs, inferred-link labels, recovered parameter display names and the names
  of shipped documents. Its only hit is "decompil" in the forbidden-inputs
  list of `AGENTS.md`, as in the released packages. Five planted terms were
  flagged.
- In the export copy
  `/tmp/claude-1000/-home-ollie-Documents-sound/5c433942-c5e3-420d-833a-756602393383/scratchpad/export/mixer-values-v1/`,
  `verify` matched all 41 hashes and resolved all 6 Markdown links inside the
  package. An independent hash recheck and the midi-config-v2 reviewer's
  `verify_copy.py` also passed; that script's only flag is `arm64` in the
  target identity, which als-container-v1 also carries. The copy is
  byte-identical to staging.

Not checked: any reference or candidate execution, and any proof of I1 to I6.

## Review gates still required

1. **Scope review**, in a separate context. Check every included clause and
   all 37 expectations against the locators. Rule on I1 to I6 and F1 to F9. In
   particular, decide whether value text may be graded while the surface is
   unknown, given the inconclusive-form obligation, and whether excluding
   REQ-010 is preferable to accepting PRB-S9-07 as a stated limitation.
2. **Quality and sanitization review**: behavioral completeness, exclusions
   present and in agreement in both the spec and the manifest, no internal
   structure or analyst link, and no claim beyond static derivation.
3. **Evidence identity**: the S9 and D8 manifests and the image hash matched
   on 2026-10-18. Re-check them before release.
4. **Fixture and sharing review** of the 37 authored fixtures and the three
   shared numbers.
5. **Finalize**: add `REVIEW.md`; set the manifest review fields,
   `release_status` and `release_date`; re-run `seal`; verify an isolated
   export; record the manifest hash in the handoff catalog.
6. **Publish** only after approval. Copy the package unchanged to
   `handoff/mixer-values-v1/`. Then update the catalog, spec status, coverage,
   indexes, questions and log. This page has no inbound index link yet.
7. An isolated implementation workspace remains unprovisioned.

## Current disposition

Staged on 2026-10-18 as an unreviewed candidate: 37 cases, partial
REQ-MIXER-VALUES-001 to 004 and 006 to 009. REQ-005 and 010 to 015 are
unreleased. The candidate is not published, and no handoff exists for
SPEC-MIXER-VALUES.
