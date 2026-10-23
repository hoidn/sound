---
id: SPEC-WARP-MARKERS
type: spec
status: draft
revision: 5
updated: 2026-10-19
access: analysis
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Warp markers and warp settings

## Scope

Feature FEAT-WARP, with FEAT-PERSISTENCE, in the [feature map](feature-map.md).
User task: open a Live Set containing a warped audio clip or a Sampler/Simpler sample,
inspect or edit its warp markers, and save it again. This draft specifies:

- where warp markers and warp settings are stored and in what form;
- marker order, the minimum count and the empty-list refusal;
- the shadow marker at the end of a list;
- defaults for absent settings;
- the warp mode, transient resolution and transient loop mode codes and their labels;
- the domains and defaults of the mode settings;
- the conversion between sample time and beat time offered by the scripting interface;
- the limits that the scripting interface applies to marker edits.

Every requirement is a **proposed contract**. Each clause is documented, supported by a
static derivation, supported by extracted execution of the shipped x86_64 code, or explicitly
unknown. The whole Live application was not run, and will not be: under
[ADR 0003](../decisions/adr-0003-no-reference-execution.md) static evidence and extracted
execution of self-contained functions are the only sources of reference behavior. [ADR 0002](../decisions/adr-0002-static-first-analysis.md)
permits a static-first draft.
The target is documents with `MinorVersion="12.0_12402"`. The gzip and XML envelope belongs
to [SPEC-ALS-CONTAINER](als-container.md). Number text follows
[SPEC-TRANSPORT-STATE](transport-state.md) REQ-004 and REQ-011. Both are dependencies. All
examples are fragments of decoded XML.

"Scripting interface" means the clip functions that Live exposes to control-surface scripts
and Max for Live (`sample_to_beat_time`, `beat_to_sample_time`, `add_warp_marker`,
`remove_warp_marker`, `move_warp_marker`). These are public names.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented: present in the shipped schema for `12.0_12402`, in shipped documents (written by 12.4d1 or 12.1d1, not by 12.4.3), or in the scripting interface's built-in help text |
| S | Static derivation from the 12.4.3 executable; not an observed run |
| X | Extracted execution: what a named x86_64 function of the shipped slice computed for the given inputs in the harness ([ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)). Results bind to the x86_64 slice; arm64 equivalence is inferred from static comparison. Evidence: [x2-envelope-warp-v1](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/results/envelope-warp.json) |
| U | Unknown; no expected result. A PRB ID names the Phase 4 probe that would have settled it. No reference observation is available (ADR 0003), so a U clause stays unknown unless the static route in [Open questions](#open-questions) settles it |

Only D, S and X clauses may enter a release. U clauses block the behavior they name. Inferred
statements are marked **Inferred** and carry no requirement.

Static clauses rest on these assumptions:

| ID | Assumption | Affects |
| --- | --- | --- |
| A1 | Settled S, reconciled 2026-10-19: the set-open reader sets context flag +0x2c and runs each post-load check. [SPEC-LIVE-SET-STRUCTURE A1](live-set-structure.md#assumptions) and its retained load-path trace establish the flag that REQ-004 needs | REQ-004; no longer an open assumption |
| A2 | Opening leaves each marker and warp setting as the document gives it, and a scripting call made right after opening sees those values. A static check in the warp-markers-v1 review found that the read, and the completion steps that run for each read clip, marker and sample part, write no marker time, add or remove no marker and write no value child. Two onset helpers and five indirect calls in those steps were not traced, nor whether automatic warping acts on opening. Revision 2 narrowed A2 to opening; the saving half is A4 | Every clause marked (A2): held values and scripting calls in REQ-002 to 004, 006 to 008 and 010 to 016. Every graded case except WMK-005, 006 and 025 to 027, which are decided while reading |
| A3 | A conversion called right after opening uses the marker list as loaded. The conversion table is built on first use; when it is rebuilt after edits was not traced | REQ-008 cases |
| A4 | Saving a set with no edit writes the values held after opening: nothing between opening and saving, and nothing in the save, changes markers or warp settings (no re-analysis, auto-warp or region-driven change). Not traced | Every clause marked (A4); the saved values of WMK-001 to 004, 007, 014, 021, 023 and 024 |

**Held after opening** means the values a clip or sample part holds once the document has been
read, including the completion steps that run for each read clip, marker and sample part. A
change the application then makes by itself, such as automatic warping or sample analysis, is
excluded behavior. Scripting clauses describe a call made right after opening, before any other
action, on the values held after opening.

**Refused** means that loading stops with an error of the corrupt-document class of
SPEC-ALS-CONTAINER. What the user then sees, and what stays loaded, is U
(REQ-ALS-CONTAINER-009). For the scripting interface, **refused** means the call raises an
error and the list is unchanged; the error kinds are named in the requirement.

## Exclusions

These have no requirement in this revision. They are not graded, and fixtures avoid them.

- **Audio output.** Time-stretching output for every warp mode, the audible effect of the
  mode settings, Re-Pitch pitch change and the quality switches. Compatibility would need a
  measured comparison (PRB-S8-11), which ADR 0003 rules out.
- **Changes after reading.** Any change the application makes by itself after it has read a
  document, such as automatic warping or sample analysis.
- **Playback timing.** Which position of the sample plays at a given song time, beyond the
  conversion step of REQ-009. Playback of clips with warping off belongs to
  [SPEC-PLAYBACK-CORE](playback-core.md) (REQ-017 to 021 there).
- **Clip region fields.** `Loop` children (`LoopStart`, `LoopEnd`, `HiddenLoopStart`,
  `HiddenLoopEnd`, `OutMarker`) and their units, and `DefaultDuration`/`DefaultSampleRate`
  semantics (PRB-S8-09). Cases keep the base set's region fields unchanged.
- **Other warp-related fields.** `Onsets`, `SavedWarpMarkersForStretched`,
  `MarkersGenerated`, `SamplesToAutoWarp`, `IsSongTempoLeader`, `Sync`, `HiQ`, `Fade`, the
  pitch fields, and the sampler's `TimeSignature` and `BeatGrid`.
- **Spellings.** Enumeration and setting values other than plain decimal text; marker `Id`
  values that are missing or duplicated; NaN and infinite marker values; a missing
  `IsWarped`.
- **Edits outside the scripting interface.** Dragging markers, auto-warp, Warp From Here,
  tempo leader, recording, undo; and the scripting `move_warp_marker` distance limits.
- **Older documents** and the migration of pre-`9.5_305` sampler warp data.

## Requirements

### REQ-WARP-MARKERS-001 — where warp state is stored

Support: documented and static-derived, with an unknown part.

- **D.** An audio clip stores its warp state as children of `AudioClip`: `IsWarped`
  (Boolean), `WarpMode`, `TransientResolution` and `TransientLoopMode` (integer codes),
  `GranularityTones`, `GranularityTexture`, `FluctuationTexture`, `TransientEnvelope`,
  `ComplexProFormants` and `ComplexProEnvelope` (floating point), and `WarpMarkers`. Each
  value child is an empty element with one `Value` attribute, for example
  `<WarpMode Value="4" />`.
- **D.** A Sampler or Simpler sample stores the same marker list, `WarpMode`, the same eight
  settings and `IsWarped` in `SampleWarpProperties`, a child of each `MultiSamplePart`.
- **D.** The texture fluctuation setting is named `FluctuationTexture`; no field is named
  `FluxTexture`.
- **S.** The runtime warp-mode chooser and tempo value of a clip are not document fields;
  none of the 2,878 shipped audio clips contains them. How the save omits them is U.

### REQ-WARP-MARKERS-002 — marker element and number text

Support: documented and static-derived, with unknown parts.

- **D.** `WarpMarkers` contains zero or more `WarpMarker` elements, each with the attributes
  `Id`, `SecTime` and `BeatTime`:
  `<WarpMarker Id="10" SecTime="0" BeatTime="0" />`. `SecTime` and `BeatTime` are attributes,
  not child elements, and hold 64-bit floating-point values.
- **S.** `SecTime` and `BeatTime` text is read as REQ-TRANSPORT-STATE-004 reads a 64-bit
  field: the longest numeric prefix, `Invalid` as the largest finite value, `#` with 16 hex
  digits as raw bits. Text with no numeric prefix is refused.
- **S (A2).** The loaded value is held without rounding, clamping or a range check.
- **S (A4).** On save both are written by the 64-bit rule of REQ-TRANSPORT-STATE-011. All
  44,058 shipped values match that rule (D).
- **S-cond (SPEC-LIVE-SET-STRUCTURE A5).** Duplicate `Id`s in one marker list,
  negative `Id`s and non-integer `Id` text refuse the set under
  [REQ-LIVE-SET-STRUCTURE-016](live-set-structure.md#req-live-set-structure-016--list-item-ids).
  That shared list-loader assumption is still open; no unconditional refusal is inferred.
- **U.** Whether `Id` is preserved, and the outcome when it is absent. Shipped `Id`s
  are unique within a list but not always ascending (18 lists). Cases do not compare `Id`.
- **Inferred.** `SecTime` is seconds from the start of the sample and `BeatTime` is beats of
  clip time. Support: REQ-008 divides a sample-frame position by the sample rate before
  comparing it with `SecTime`, and shipped region fields agree with markers extrapolated to
  the sample start and end (330 and 292 of 399 warped clips).

### REQ-WARP-MARKERS-003 — well-formed marker lists

Support: documented and static-derived.

- **D.** In shipped documents every marker list with two or more markers is strictly
  increasing in both `SecTime` and `BeatTime` (10,250 of 10,250). Every shipped audio clip has
  at least two markers, warped or not; shipped `SampleWarpProperties` have 0, 2 or 3.
- **S (A2).** An audio clip list of at least two markers, strictly increasing in both
  attributes, opens and is held with each marker's values as stored and in document order.
- **S (A4).** A later save writes the same values in the same order.

### REQ-WARP-MARKERS-004 — empty marker list

Support: static-derived, with unknown parts.

- **S (A1 settled).** An `AudioClip` whose `WarpMarkers` has no `WarpMarker` is refused. The error
  detail is an empty warp marker array.
- **S.** `SampleWarpProperties` have no such check: an empty list there does not cause a
  refusal. 4,244 shipped `SampleWarpProperties` have empty lists (D).
- **S (A2).** The sample part's list is then empty after opening.
- **U.** What the user sees and what stays loaded (PRB-S8-01, REQ-ALS-CONTAINER-009).

### REQ-WARP-MARKERS-005 — malformed marker lists

Support: unknown, with one static-derived clause.

- **S.** A one-marker audio clip list is not refused by REQ-004's check.
- **U.** What a one-marker list then loads as, shows and saves (PRB-S8-02).
- **U.** Lists out of order, with a beat below its predecessor, or with two equal `SecTime`
  values: refused, sorted or kept (PRB-S8-03). No sort or order check was found on load, and
  later operations assume ascending order.

### REQ-WARP-MARKERS-006 — missing or `Invalid` marker positions

Support: static-derived, with unknown parts.

- **S (A2).** A `WarpMarker` without `SecTime` or `BeatTime` keeps the largest finite 64-bit
  value for that attribute. `Invalid` text loads the same value (REQ-002).
- **U.** Whether such a set opens, what the clip shows and what a save writes (PRB-S8-04).

### REQ-WARP-MARKERS-007 — the shadow marker

Support: documented and static-derived, with unknown parts.

- **S.** Live treats the last element of an audio clip's marker list as the *shadow marker*.
  In the scripting conversion, the segment from the last visible marker to the shadow marker
  governs everything after the last visible marker (REQ-008). Revision 4: warped playback
  converts beats to file time through the same mapping, so the same segment applies there
  (REQ-009, S).
- **S.** Where Live creates or re-places the shadow marker, it puts it 1/32 beat after the
  preceding marker, with the beat rounded as in REQ-016. Which user operations do this is U.
- **U.** Which user operations create or re-place the shadow and what times they
  give it. The extracted append routine has no observable acceptance case: its
  caller arguments are untraced. Its formula is retained as research in the
  [evidence appendix](#analyst-evidence-appendix), not a release-ready requirement.
- **D.** In shipped lists the last marker is exactly 1/32 beat after the previous one in
  2,869 of 2,878 audio clips and 7,313 of 7,372 sampler lists; the others use 1/16 or 1/64.
- **S (A2).** On load a different spacing is kept: no completion step moves the last marker.
- **S (A2).** The scripting interface refuses to delete or move the shadow marker and never
  makes it a new marker's right neighbour (REQ-015).
- **U.** Whether a later edit or save re-places a shadow that is not 1/32 beat after its
  predecessor (PRB-S8-07); whether a sampler list's last marker has the same role.

### REQ-WARP-MARKERS-008 — scripting conversion between sample time and beat time

Support: documented and static-derived, with unknown parts.

Let the clip's list be (s₀, b₀) … (sₙ₋₁, bₙ₋₁) in list order (`SecTime`, `BeatTime`), with
n ≥ 2 and both coordinates strictly increasing, and let R be the clip's sample rate in Hz.

- **D, S (A2).** `sample_to_beat_time` and `beat_to_sample_time` are available for audio
  clips only and raise an error when the clip is not warped, as its `IsWarped` was read.
- **S (A2, A3).** `sample_to_beat_time(t)` takes a position t in sample frames and sets
  x = t / R. It selects segment k: the largest index from 0 to n − 2 with sₖ ≤ x, or 0 when
  x < s₀. It returns bₖ + (x − sₖ)(bₖ₊₁ − bₖ)/(sₖ₊₁ − sₖ) in 64-bit floating point.
- **S (A2, A3).** `beat_to_sample_time(b)` selects k the same way over b₀ … bₙ₋₂, computes
  x = sₖ + (b − bₖ)(sₖ₊₁ − sₖ)/(bₖ₊₁ − bₖ) and returns x × R.
- **S (A2, A3).** The result is linear inside each segment. Before the first marker the first
  segment is extended. At or after the last visible marker sₙ₋₂ the segment to the shadow
  marker is extended. Results are not limited to the sample or to the marker range.
- **X.** The two conversion cores (x86_64 `0x101b6fa60` seconds → beats and `0x101b6f970`
  beats → seconds; arm64 `0x101b39e20` and `0x101b39d8c`) were run on the conversion table of
  M1 and M2: they compute the formulas above, including both extensions, with
  bₖ + u·(bₖ₊₁ − bₖ) evaluated as fma(u, bₖ₊₁, fma(−u, bₖ, bₖ)). WMK-016 to 018 give exactly the
  expected values ([results](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/results/envelope-warp.json), `warp_WMK016_M1`, `warp_WMK017_M2`). Both slices fuse the same two
  operations (arm64 `fmsub`/`fmadd`; x86_64 glibc `fma`), so the results are bit-identical.
  **Limits:** the table was built in harness buffers in list order (`BeatTime` to the first
  array, `SecTime` to the second), as the builder `0x1028b4f00` / `0x10277b71c` does (S); the
  scripting entry points' audio-clip and warped tests, and the division and multiplication by
  the sample rate, are S.
- **U.** Results for n = 1, equal adjacent coordinates, or an unsorted list; the result after
  marker edits (A3).

### REQ-WARP-MARKERS-009 — playback position of a warped clip

Support: static-derived for the conversion step (revision 4), with unknown parts.

- **S (revision 4).** The conversion cores of REQ-008 are the engine's marker-list
  conversions. Names come from the x86_64 Live Engine:
  - x86_64 `0x101b6f970` is `OWarpMarkerList::BeatToSampleTime` and `0x101b6fa60` is
    `SampleToBeatTime` (96.3 % equal bytes at the same size).
  - In the Engine, the audio warpers' playback functions call them:
    `OWarperBase::PlayPosFileSmpl`, `OWarperBase::StartSample` and `OWarpData::FileBeatToFileSmpl`;
    the Re-Pitch warper's playing range; the Beats warper's grain and transient functions; the
    Complex warpers' start, drift and jump functions; and the preload range estimates.
  - Live x86_64 has 23 callers of the beats-to-seconds core. The arm64 core `0x101b39d8c` also
    has 23, in the corresponding warper code (not matched one by one).
- **S (revision 4).** For a warped clip, the play position takes the current song beat less the
  clip's start offset, passes it through the clip's time map when one is present, and converts
  it with the marker mapping of REQ-008 to seconds of file time. It then multiplies by the
  file's sample rate (`OWarperBase::PlayPosFileSmpl`).
  - **Extensions.** Before the first marker and after the last visible marker the mapping is
    extended as in REQ-008.
  - **Frame clamp.** `OWarpData::FileBeatToFileSmpl` limits the result to frames 0 to the last
    frame.
  - **What this establishes.** Warped playback places file positions by the scripting
    conversion's mapping, and revision 3's "Inferred" clause becomes S for that step. The
    arithmetic itself is X (REQ-008).
- **S (revision 4), warping off.** A session clip with `IsWarped` false does not use its markers:
  - its start frame and read position come from its loop start in seconds and a fixed read step
    ([REQ-PLAYBACK-CORE-017](playback-core.md#req-playback-core-017--unwarped-audio-clip-start-read-step-and-read-position));
  - the unwarped warper uses the extrapolating marker conversion only for an arrangement clip's
    start (`OWarperUnWarped::StartFileSmpl`, Engine names, x86_64);
  - the scripting conversion refuses unwarped clips (REQ-008).

  This is a playback claim: a marker or document-value comparison cannot observe it.
  Its render acceptance belongs to SPEC-PLAYBACK-CORE, and REQ-009 remains unreleased
  (warp-markers-v2 review RVW2-02).
- **U.** For warped playback:
  - which file sample each output sample reads, in each warp mode: the Beats grains,
    Tones/Texture, Complex and Complex Pro, and Re-Pitch's rate;
  - the time map's effect, which is groove and is excluded;
  - preload and rounding;
  - whether `PlayPosFileSmpl` drives the audio or only position feedback;
  - the arm64 correspondence beyond the caller count.

  Warped audio playback is outside target T1
  ([ADR 0004](../decisions/adr-0004-target-scope-t1.md)), so these items do not block it.
- **Correction (revision 4).** Revision 3 said no static caller connects the conversion cores
  to the engine's playback position. The callers above do. Revision 3 had followed only Live's
  unnamed arm64 callers, without the Engine's names.

### REQ-WARP-MARKERS-010 — absent warp settings

Support: static-derived, with unknown parts.

- **S (A2).** An absent setting element, or one without its `Value` attribute, leaves the
  value set when the clip or sample was created. For both holders these are the defaults in
  REQ-012 and REQ-013: `TransientResolution` 6, `TransientLoopMode` 2, `GranularityTones` 30,
  `GranularityTexture` 65, `FluctuationTexture` 25, `TransientEnvelope` 100,
  `ComplexProFormants` 100, `ComplexProEnvelope` 128. Absence is not refused.
- **S.** `TransientEnvelope` is created at 100 although its parameter's maximum is 1.0: creation
  stores the value without a clamp. Its range is U (REQ-013).
- **S.** A new `SampleWarpProperties` takes `WarpMode` from the default-warp-mode preference
  (preference index 0 to 5 gives code 0, 1, 2, 3, 4, 6). A new audio clip does the same when
  the application's preference store is present, and takes 0 otherwise.
- **U.** The `WarpMode` an audio clip gets when the element is absent from a loaded set, and
  the preference's factory value (PRB-S8-10). **Inferred:** the preference is the Default
  Warp Mode setting.

### REQ-WARP-MARKERS-011 — warp mode codes

Support: static-derived, with unknown parts.

- **S.** `WarpMode` codes are 0 to 6. Codes 0 to 4 and 6 are the six modes of Live's warp
  mode chooser: 0 Beats, 1 Tones, 2 Texture, 3 Re-Pitch, 4 Complex, 6 Complex Pro. The chooser
  has no entry for code 5. Shorter four- and five-entry chooser lists also exist; when they are
  used is U.
- **Inferred.** Code 5 is REX. That label comes only from the stored code list, which is not
  established as display text.
- **S (A2).** A `WarpMode` of 0 to 4 or 6 is held as stored after opening (REQ-014 for other
  codes).
- **Inferred.** The chooser shows the label of the stored code. Shipped audio clips use 0, 3,
  4 and 6; sampler lists also 1 and 2; no shipped document uses 5 (D).

### REQ-WARP-MARKERS-012 — transient resolution and transient loop mode codes

Support: static-derived.

- **S.** `TransientResolution` codes are 0 to 6. Default 6.
- **S.** `TransientLoopMode` codes are 0, 1 and 2. Default 2.
- **S (A2).** A code in these lists is held as stored after opening (REQ-014 for other codes).
- **Inferred.** The `TransientResolution` labels are 0 1 Bar, 1 1/2, 2 1/4, 3 1/8, 4 1/16,
  5 1/32, 6 Transients. They come from a stored code list, which is not established as display
  text.
- **Inferred.** The stored loop-mode names `LoopOs`, `LoopFwd` and `LoopAlt` are internal value
  names. The displayed loop-mode labels are Off, Loop Forward and Loop Back-and-Forth.

### REQ-WARP-MARKERS-013 — mode setting domains and defaults

Support: static-derived, with unknown parts.

- **S.** Live creates each setting with this range and default:

  | Field | Parameter name (inferred) | Minimum | Maximum | Default |
  | --- | --- | --- | --- | --- |
  | `GranularityTones` | Granularity Tones | 12 | 100 | 30 |
  | `GranularityTexture` | Granularity Texture | 2 | 263 | 65 |
  | `FluctuationTexture` | Fluctuation Texture | 0 | 100 | 25 |
  | `ComplexProFormants` | Complex Pro spectral envelope factor | 0 | 100 | 100 |
  | `ComplexProEnvelope` | Complex Pro spectral envelope order | 8 | 256 (integer steps) | 128 |
  | `TransientEnvelope` | — | 0 | U | 100 |

- **Inferred.** The parameter names are those Live assigns when it creates each setting. They
  look like internal parameter names; that Live displays them is not established.
- **S (A2).** A value within its range is held as stored after opening (REQ-014 for others).
- **D.** Every shipped audio clip carries the defaults. Shipped sampler values lie inside the
  ranges (Tones 12–80.0625, Texture 2–132.5, Fluctuation 0–100, TransientEnvelope 0–100,
  Formants 0–100, ComplexProEnvelope 8–128).
- **U.** The range of `TransientEnvelope`: the parameter is created with maximum 1.0 and
  default 100, stored without a clamp (REQ-010), while its curve and shipped values use 0–100
  (PRB-S8-06).
- **Inferred.** Beats uses the three transient settings, Tones uses `GranularityTones`,
  Texture uses `GranularityTexture` and `FluctuationTexture`, and Complex Pro uses the two
  `ComplexPro*` settings.

### REQ-WARP-MARKERS-014 — out-of-range codes and settings on load

Support: static-derived, with unknown parts.

- **S (A2).** A well-formed `WarpMode`, `TransientResolution`, `TransientLoopMode` or
  setting value outside its codes or range does not cause a refusal. It is held as stored,
  without a check or a clamp.
- **U.** The value Live then uses, displays and writes on the next save, for `WarpMode` 5 on
  a non-REX sample, 7 or −1 (PRB-S8-05), and for settings outside REQ-013 (PRB-S8-06).

### REQ-WARP-MARKERS-015 — marker edits through the scripting interface

Support: static-derived, with unknown parts.

`add_warp_marker` takes a sample time p (seconds, the unit of `SecTime`) and a beat q. Its
checks run in the order below; the first that fails refuses the call.

- **S (A2).** The add is refused when the clip is not an audio clip, when it is not warped, or
  when p is not within 0 ≤ p ≤ the sample length in seconds (a NaN p is refused). That this
  length is the duration of the clip's sample in seconds is assumed; its source was not traced.
- **S (A2).** The new marker goes before the first visible marker whose `SecTime` is greater
  than p, or before the shadow marker if none is. The marker before that position is the left
  neighbour; when p is below the first marker's `SecTime` there is none. The marker at that
  position is the right neighbour, unless it is the shadow marker.
- **S (A2).** Refused if q, as given, is below the left neighbour's beat or above the right
  neighbour's beat. A missing neighbour has no check.
- **S (A2).** q is then rounded as in REQ-016, giving q′. For each neighbour (sₙ, bₙ), let
  Δs = p − sₙ. The add is refused unless q′ lies within the inclusive bounds bₙ + Δs × 5/60 and
  bₙ + Δs × 999/60, the smaller being the lower bound; a NaN q′ is refused. No bound applies
  toward the shadow marker or toward a missing left neighbour. Live computes the bounds in
  64-bit floating point.
- **X.** The bounds are computed exactly as Δs = p − sₙ, a = bₙ + Δs × (5/60),
  c = bₙ + Δs × (999/60), each operation rounded to 64 bits with no fused operation, returned as
  (min(a, c), max(a, c)) (x86_64 `0x1028e96b0` with `0x102275e80`; arm64 `0x1027afd40` with
  `0x1021862f0`, the same order). Run: neighbour (1, 2), p = 1.5 → [2.0416666666666665, 10.325];
  p = 1 → [2, 2]; p = 1.0004 → [2.0000333333333336, 2.0066599999999992]; right neighbour (2, 3),
  p = 1.5 → [−5.324999999999999, 2.9583333333333335] ([results](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/results/envelope-warp.json), re-derived by [check_rules.py](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/check_rules.py)).
  The comparison with q′ is inclusive (S, both slices).
- **S.** For Δs ≠ 0 this is the condition that the segment tempo (q′ − bₙ) / Δs × 60 lies
  within 5 to 999 BPM inclusive. At Δs = 0, when p equals the left neighbour's `SecTime`, both
  bounds are bₙ, so only q′ = bₙ passes.
- **S (A2).** An add that passes every check raises no error. The insertion leaves the list
  unchanged when a marker with an equal `SecTime` or `BeatTime` exists, so an accepted add at
  Δs = 0 has no effect. Support is pseudocode; the insertion's callees were not traced.
- **S (A2).** `remove_warp_marker(q)` and `move_warp_marker(q, d)` find the first marker whose
  beat equals q rounded as in REQ-016 (lookup derived with weaker support; see the appendix).
  They are refused when no marker matches or when it is the shadow marker. Neither requires
  the clip to be warped.
- **S (A2).** A remove that passes these checks raises no error. It leaves the list unchanged
  when the list has fewer than three markers: removing the first marker of M0 is accepted with
  no effect. Support is pseudocode.
- **X.** Inside the former uncertainty bands (a segment tempo within 0.001 BPM of 5 or 999, q
  within 0.001 grid step of a rounding tie, p less than 0.0005 s from a neighbour's `SecTime`)
  the outcome is decided by the 64-bit sequences of this clause and of REQ-016, which are
  now settled by X. A candidate must reproduce those sequences, not the exact rule, at these
  edges. Revision 2's bands are withdrawn; cases WMK-037 to 039 test the edges.
- **U.** The resulting list after any other accepted add or remove, including the shadow; the
  limits of `move_warp_marker` and the result of an accepted move; the warp modes the scripting
  `warp_mode` setter accepts; whether interactive edits apply the same limits.

### REQ-WARP-MARKERS-016 — beat grid

Support: documented and static-derived, with an unknown part.

- **S.** Live's marker beat setter, the scripting add and the scripting marker lookups round a
  beat to the nearest multiple of 1/3,843,840 beat, with halves away from zero, computed in
  64-bit floating point. The values ±1.7976931348623155e308, the largest finite value and +∞
  are not rounded.
- **X.** The rounding is exactly q(b) = s × ⌊|b + s × (2.6015651015651016e−07 × 0.5)| × 3,843,840⌋
  / 3,843,840 with s = +1 when b ≥ 0 and −1 otherwise, each operation rounded to 64 bits
  (x86_64 `0x102736ce0`, arm64 `0x1026101b4`; arm64 fuses the add with an exact product and
  uses `frintm`, x86_64 adds and uses `roundsd` floor, so the slices agree bit for bit). Run on
  a real `AWarpMarker` ([results](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/results/envelope-warp.json), `beat_grid_round`, re-derived by [check_rules.py](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/check_rules.py)):
  2.0000001 → 2; 2.001 → 2.0010000416250415; 10.325 → 10.325; +∞ and the three sentinels
  unchanged; −∞ → −∞; NaN → NaN; **−0 → +0**. It differs from exact rounding only within about
  3 × 10⁻⁹ grid step of a halfway point: the 64-bit value nearest to beat 2 + ½ step, and the
  value one unit in the last place below it, both round up to 2 + 1/3,843,840, although the
  latter is below the halfway point; two units below, the result is 2.
- **S (A2).** Load does not round: a loaded `BeatTime` is held with its value (REQ-002).
- **S.** The scripting add does not round `SecTime`.
- **D.** All 22,029 shipped `BeatTime` values lie on the 1/3,843,840-beat grid.

## Timing and state

- **Units.** Marker seconds and beats as in REQ-002 (inferred); segment tempo in BPM; sample
  rate in Hz; scripting sample positions in frames. All arithmetic is 64-bit floating point.
- **Persistent state.** The marker list and the settings of REQ-001. The clip region fields
  are a separate concern (exclusions).
- **Determinism.** Reading, writing and the scripting conversion are deterministic for a given
  document. Save text is exact per attribute (REQ-TRANSPORT-STATE-011).
- **Interactions.** The empty-list refusal belongs to the failure classes of SPEC-ALS-CONTAINER.
  Song tempo (SPEC-TRANSPORT-STATE) does not enter REQ-008. No timing, cancellation or undo
  behavior is specified.

## Acceptance cases

**Base W0.** The shipped set `Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12
Suite Demo).als` (SHA-256 `3f1c0f924b750c2adba2525838f2bc00856e52faea09d43b9279c6a0fe40952b`,
`MinorVersion="12.0_12402"`, written by 12.4d1). The Core Library must be installed so that
its samples resolve.

**Clip C.** The first `AudioClip` in document order: `<AudioClip Id="5" Time="0">`, named
"Vocal Main", on the eleventh track ("Vocal Main"), second clip slot. Its sample is
`Samples/Loops/Tonal/Vocal/Vocal Patience Main.wav` (`DefaultDuration` 2,138,444,
`DefaultSampleRate` 48,000; sample length 44.5509166… s). In W0 it has `IsWarped` true,
`WarpMode` 4, the default settings of REQ-013 and the list M0.

**Fragment M0** (W0 as shipped; shadow tempo 167 BPM):

```xml
<WarpMarkers>
  <WarpMarker Id="10" SecTime="0" BeatTime="0" />
  <WarpMarker Id="11" SecTime="0.0112275449101796407" BeatTime="0.03125" />
</WarpMarkers>
```

**Fragment M1** (three visible markers and a shadow; segment tempi 120, 60 and 120 BPM):

```xml
<WarpMarkers>
  <WarpMarker Id="10" SecTime="0" BeatTime="0" />
  <WarpMarker Id="11" SecTime="1" BeatTime="2" />
  <WarpMarker Id="12" SecTime="2" BeatTime="3" />
  <WarpMarker Id="13" SecTime="2.015625" BeatTime="3.03125" />
</WarpMarkers>
```

**Fragment M2.** M1 with its first marker replaced by
`<WarpMarker Id="10" SecTime="0.5" BeatTime="1" />`.

**Construction.** Decode W0, change only clip C as stated, and re-encode as gzip.

**Procedures.**

- *Open*: fresh preferences; File > Open Live Set; record whether the set opens.
- *Save*: Open, then Save As a new set with no edit; compare clip C's elements in the saved
  set (A4).
- *Script*: Open, then, right after opening and before any other action, call the named
  scripting function on clip C; record the return value or the error. A case listing several
  calls makes each on a fresh Open.

**Comparators.** Attribute text is compared exactly, except marker `Id`s. Scripting beats
are compared within 1e-9 beat and sample positions within 1e-6 frame. Labels in *italics*
are inferred display text and are not graded. Cases expecting "unresolved" must not be
graded as passes. WMK-001 and WMK-002 also check A2 and A4: if their saved values differ from
the document's, the other save comparisons are inconclusive.

**Case kinds.** P positive, N negative (refused), B boundary, M missing input, S save text,
U unresolved. Expected results are static derivations, shipped-document facts, or values
from extracted execution of the x86_64 slice (revision 3: WMK-016 to 019 and 037 to 039). No case
has been run against Live, and under ADR 0003 none will be.

| Case ID | Requirement | Kind | Setup (change to clip C) and action | Expected result | Fixture |
| --- | --- | --- | --- | --- | --- |
| WMK-001 | 001, 002, 003 | S | None; Save | Opens. Saved list: `SecTime="0" BeatTime="0"`, then `SecTime="0.0112275449101796407" BeatTime="0.03125"`. Saved `WarpMode` 4 and the eight settings as in W0 | W0 |
| WMK-002 | 003 | S | List M1; Save | Opens. Saved in order: `SecTime="0" BeatTime="0"`, `SecTime="1" BeatTime="2"`, `SecTime="2" BeatTime="3"`, `SecTime="2.015625" BeatTime="3.03125"` | W0+M1 |
| WMK-003 | 002, 016 | S | M1 with second marker `BeatTime="2.0000001"`; Save | Opens; saved `BeatTime="2.0000000999999998"` (not moved to the grid) | W0+M1 |
| WMK-004 | 002 | B | M1 with second marker `SecTime="1.0e0"`; Save | Opens; saved `SecTime="1"` | W0+M1 |
| WMK-005 | 002 | N | M1 with second marker `SecTime="abc"`; Open | Refused | W0+M1 |
| WMK-006 | 004 | N | `<WarpMarkers />`; Open | Refused (A1); presentation unresolved (PRB-S8-01) | W0 |
| WMK-007 | 004 | P | None; Save | Opens. Each of the 14 `SampleWarpProperties` with `<WarpMarkers />` in W0 is saved with an empty list | W0 |
| WMK-008 | 005 | U | List of one marker `<WarpMarker Id="10" SecTime="0" BeatTime="0" />`; Open, Save | Unresolved (PRB-S8-02); not refused by REQ-004's check | W0 |
| WMK-009 | 005 | U | M1 in reverse document order; Open, Save | Unresolved (PRB-S8-03) | W0+M1 |
| WMK-010 | 005 | U | M1 with second marker `BeatTime="-1"`; Open, Save | Unresolved (PRB-S8-03) | W0+M1 |
| WMK-011 | 005 | U | M1 with third marker `SecTime="1"`; Open, Save | Unresolved (PRB-S8-03) | W0+M1 |
| WMK-012 | 006 | U | M0 with the second marker's `BeatTime` attribute removed; Open, Save | Unresolved (PRB-S8-04); stored beat is the largest finite value | W0 |
| WMK-013 | 006 | U | M0 with second marker `BeatTime="Invalid"`; Open, Save | Unresolved (PRB-S8-04); as WMK-012 | W0 |
| WMK-014 | 007 | S | Second marker `SecTime="0.022455089820359281" BeatTime="0.0625"` (1/16 beat, 167 BPM); Save | Opens; saved `SecTime="0.0224550898203592815" BeatTime="0.0625"` | W0 |
| WMK-015 | 007, 015 | N | None; Script `remove_warp_marker(0.03125)`; `move_warp_marker(0.03125, 1)` | Each refused: shadow marker | W0 |
| WMK-016 | 008 | P | M1; Script `sample_to_beat_time(t)` for t = −24000, 24000, 48000, 72000, 96000, 120000, 2400000 | −1, 1, 2, 2.5, 3, 4, 99 | W0+M1 |
| WMK-017 | 008 | P | M2; Script `sample_to_beat_time(t)` for t = 0, 12000 | 0, 0.5 | W0+M2 |
| WMK-018 | 008 | P | M1; Script `beat_to_sample_time(b)` for b = 0.5, 2.5, 4 | 12000, 72000, 120000 | W0+M1 |
| WMK-019 | 008 | P | None; Script `sample_to_beat_time(48000)` | 2.783333333333333 (167/60) | W0 |
| WMK-020 | 008 | N | `<IsWarped Value="false" />`; Script `sample_to_beat_time(0)`; `beat_to_sample_time(0)` | Each refused: clip not warped | W0 |
| WMK-021 | 010, 013 | M | Delete the eight setting elements; Save | Opens; saved `GranularityTones` 30, `GranularityTexture` 65, `FluctuationTexture` 25, `TransientResolution` 6, `TransientLoopMode` 2, `TransientEnvelope` 100, `ComplexProFormants` 100, `ComplexProEnvelope` 128 | W0 |
| WMK-022 | 010 | U | Delete `WarpMode`; Save, under Default Warp Mode Beats and then Complex Pro | Unresolved (PRB-S8-10): 0 or the preference's code | W0 |
| WMK-023 | 011 | S | `WarpMode` 0, 1, 2, 3, 6 in turn; Save | Opens; saved value unchanged. Chooser: *Beats, Tones, Texture, Re-Pitch, Complex Pro* | W0 |
| WMK-024 | 012 | S | `TransientResolution` 4, `TransientLoopMode` 1; Save | Opens; saved 4 and 1. Display: *1/16*, *Loop Forward* | W0 |
| WMK-025 | 014 | B | `WarpMode` 7, then −1; Open, Save | Opens; value used, shown and saved unresolved (PRB-S8-05) | W0 |
| WMK-026 | 014 | B | `WarpMode` 5 (the sample is a WAV); Open, Save | Opens; effect unresolved (PRB-S8-05) | W0 |
| WMK-027 | 013, 014 | B | `GranularityTones` 500, `ComplexProEnvelope` 4, `TransientEnvelope` 150; Open, Save | Opens; values used, shown and saved unresolved (PRB-S8-06) | W0 |
| WMK-028 | 015 | N | `<IsWarped Value="false" />`; Script `add_warp_marker` (0.005 s, beat 0.01) | Refused: clip not warped | W0 |
| WMK-029 | 015 | N | M1; Script add (−0.1 s, 0); add (10,000,000 s, 100) | Each refused: sample time out of range. The second time exceeds the sample's length counted in seconds, milliseconds or frames (revision 2; the former 50 s would pass a length in milliseconds or frames) | W0+M1 |
| WMK-030 | 015 | N | M1; Script add (1.5 s, 1.9) | Refused: beat below the left neighbour | W0+M1 |
| WMK-031 | 015 | N | M1; Script add (1.5 s, 3.5) | Refused: beat above the right neighbour | W0+M1 |
| WMK-032 | 015 | N | M1; Script add (1.5 s, 2.01); add (0.5 s, 1.99) | Each refused: segment tempo out of range (left side 1.2 BPM; right side 1.2 BPM) | W0+M1 |
| WMK-033 | 015 | P | M1; Script add (1.5 s, 2.5) | Accepted (tempi 60 and 60 BPM) | W0+M1 |
| WMK-034 | 015 | B | M1; Script add (2.5 s, 4) | Accepted: the next marker is the shadow, so there is no right neighbour and only the left limit applies (120 BPM) | W0+M1 |
| WMK-035 | 015, 016 | B | M1; Script `remove_warp_marker(2.0000001)`; `remove_warp_marker(2.001)` | First accepted (rounds to beat 2); second refused: no such marker | W0+M1 |
| WMK-036 | 015 | B | M1 and `<IsWarped Value="false" />`; Script `remove_warp_marker(2)`; `move_warp_marker(2.001, 1)` | First accepted; second refused: no such marker. Neither is refused as not warped | W0+M1 |
| WMK-037 | 015 | B | M1; Script add (1.5 s, 2.0416666666666665); add (1.5 s, 2.0416664065101564) | First accepted (left segment tempo exactly 5 BPM: q′ equals the computed lower bound); second refused: segment length out of range (one grid step below) | W0+M1 |
| WMK-038 | 015 | B | M1; Script add (2.5 s, 11.325); add (2.5 s, 11.325000260156509) | First accepted (segment from the last visible marker at exactly 999 BPM; the next marker is the shadow, so there is no right bound); second refused: segment length out of range (one grid step above) | W0+M1 |
| WMK-039 | 015, 016 | B | M1; Script `remove_warp_marker(2.0000001300782553)`; `remove_warp_marker(2.000000130078255)`; `remove_warp_marker(2.0000001300782544)` | First and second refused: no marker at the rounded beat 2 + 1/3,843,840. The second is below the exact half-step and distinguishes the binary64 sequence from exact rounding (X for q()). Third accepted: rounds to 2 (computed by the confirmed sequence) | W0+M1 |

Cancellation and teardown kinds are omitted: loading, saving and the scripting calls in scope
have no cancellable step or resource. REQ-009 has no case. Both its warped-conversion
claim and its unwarped claim require playback output, which these document and scripting
cases do not observe. Per-mode warped playback is excluded, and the measurement that
PRB-S8-08 describes is not available (ADR 0003). The REQ-015 clauses on an unchanged list have
no case: no procedure here observes the list after a call except a save, under A4. The
shadow append of REQ-007 has no case: no procedure here makes the clip recompute its shadow.
Thirty-nine cases: 32 gradable (WMK-006 for refusal only, WMK-025 to 027 for opening only) and
7 unresolved (WMK-008 to 013, 022). Correction, revision 5: X2 ran the M1/M2
conversion cores for WMK-016 to 018; WMK-019 uses M0, which it did not run.
WMK-019 is computed by the confirmed formula, with frame scaling static-derived.
The wrappers, document opening and scripting dispatch were not executed. WMK-037 to 039 take their
outcomes from the X-settled 64-bit sequences of REQ-015 and REQ-016.

## Open questions

[Q-021](../questions.md#q-021-warp-playback-mapping-and-load-handling) tracks the playback
mapping and load handling. Each item below names the probe in the
[S8 probe batch](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/probe-batch.json) that would
have settled it. No reference observation is available (ADR 0003), so each item stays unknown
unless its static route, where one exists, settles it:

- empty-list presentation (PRB-S8-01): trace how opening reports a corrupt-document error
  (REQ-ALS-CONTAINER-009). A1 is now settled by the set-open trace in
  SPEC-LIVE-SET-STRUCTURE; the empty-list refusal is S, while its presentation remains U;
- one-marker, unordered and equal-time lists (PRB-S8-02, 03) and missing or `Invalid`
  positions (PRB-S8-04): trace the steps that use the list on opening and saving; what the clip
  shows has no practical static route;
- out-of-range `WarpMode` (PRB-S8-05) and settings, including the `TransientEnvelope` range
  (PRB-S8-06): trace the readers of the stored values and the `TransientEnvelope` curve;
- shadow spacing after edits and saves (PRB-S8-07): trace the callers of the steps that create
  or re-place the shadow;
- playback mapping (PRB-S8-08). The conversion step is settled in revision 4 (REQ-009). The
  per-mode read position remains, with no practical static route for the stretch modes.
  Region-field units (PRB-S8-09) are settled for unwarped clips by REQ-PLAYBACK-CORE-017
  (seconds). For warped clips, trace the readers of the `Loop` fields;
- absent `WarpMode` and the preference (PRB-S8-10): trace whether the preference store exists
  while a set is read, and where the preference's factory value is set;
- per-mode audio (PRB-S8-11): no practical static route; it stays excluded;
- covered by no probe: A2's untraced remainder (onset helpers, indirect calls and the
  automatic-warping trigger on opening), A3 (when the conversion table is rebuilt), A4 (the
  save path), the list after an accepted scripting edit, the `move_warp_marker` limits and the
  scripting `warp_mode` setter. Each can be traced from the routines the appendix names for it.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. The canonical evidence is
[warp markers](../research/warp-markers.md), with retained run
`analysis/ableton-live-12.4.3/r2/s8-warp-v1/` (dossiers s8-0001 to s8-0003, `notes.md`,
`static-survey.json`, `getter-constants.txt`, `vtable-reads.txt`). Image `Live.arm64`,
SHA-256 `3a99ceea…d1c383cfad`, base `0x100000000`. ✓ marks a branch or constant this author
re-read in dossier disassembly while drafting.

**Drafting rounds.** Two query rounds, **d7-0001** (8 dossiers: `0x1033bf160`, `0x1027beb9c`,
`0x102893b1c`, `0x1028939a4`, `0x10277b71c`, `0x101b39e20`, `0x1033bf250`, `0x101b39d8c`) and
**d7-0002** (8 dossiers: `0x1027bec54`, `0x101b39d74`, `0x101b39d80`, `0x10261026c`,
`0x102610264`, `0x1027c6ed0`, `0x1027c6ec0`, `0x102883578`). They are retained unchanged in
`analysis/ableton-live-12.4.3/r2/d7-warp-v1/`; its 34 files matched its manifest on
2026-10-18. `queries.json` SHA-256 prefixes: d7-0001 `1dede799`, d7-0002 `ce8a537e`;
`manifest.json`: `90af824c`, `d55bc6f8`. Image reads made with scratch scripts (not
retained): AAudioClip vtable `0x10680bea0` slots `+0x300` → `0x10243ea38`, `+0x4a8` →
`0x1027c6ec0`, `+0x4b0` → `0x1027c6ed0`, `+0x4b8` → `0x1027beb9c`, `+0x4c0` → `0x1027bec54`;
helper vtable `0x10681f1f8` (installed by `0x1028937bc`: `adrp x8,0x10681f000; add
x8,x8,#0x1f8`) slots `+0x190` → `0x1028939a4`, `+0x198` → `0x102893b1c`, `+0x1a0` →
`0x102893b28`; wrappers `0x102248700` = `add x0,x0,#0x10; b 0x101b39e20` and `0x1022485d8` =
`add x0,x0,#0x10; b 0x101b39d8c`; AWarpMarker vtable `0x1067e6f08` `+0x38`/`+0x40` →
`0x100249f40`/`0x100249f48` (both `return 0`, pseudocode); getter `0x10224e2e8` word
`0x0f026460` = `movi v0.2s,#0x43,lsl #24` = 128.0, which `getter-constants.txt` left
undecoded.

| Requirement | Evidence (function entry, result) | Strength |
| --- | --- | --- |
| 001 | Schema `12.0_12402` holders and evolution (`static-survey.json` `schema`); AAudioClip registration `0x1027aff6c` adds runtime `DisplayWarpMode` and `RightTempo`, absent from all 2,878 shipped clips; their omission on save not traced | D; S |
| 002 | AAbstractWarpMarker registration `0x10260fdd8` ✓ (s8-0001): `mSecTime` +0x50, `mBeatTime` +0x58, flag 4 (attribute). Generic loader `0x101487310` and text conversion `0x10152bfb8` (n1); the Double branch is assumed from the schema class and the 64-bit getters `0x102610264`/`0x10261026c` ✓ (d7-0002). AWarpMarker post-load `0x101486fa8` calls slots +0x38/+0x40, which return 0. `checks.number_text_rule` 44,058; `ids_unique=True|ids_ascending=False` 15 + 3 | D; S (Double branch assumed) |
| 003 | `checks.*strictly_increasing` 2,878 + 7,372; `count=…` rows. Document order: the list loader's child order is not traced; for strictly increasing input any sorting gives the same order | D; S (A2, A4) |
| 004 | AAudioClip post-load slot +0xd0 = `0x1027c1c7c` ✓ (s8-0001): `ldr x0,[x19,#0x658]; bl 0x10156da34; cbnz` → `Empty warp marker array.` → `0x101488e64` ✓ → `0x10148229c`. Empty test `0x10156da34`/`0x101467280` ✓ (s8-0003). ASampleWarpProperties post-load `0x10288538c` ✓ (s8-0002) has no such test. Post-load runs when context flag +0x2c is set (A1) | S (A1) |
| 005 | One marker: the conversion `0x101b39e20` ✓ then reads index 1 of a one-element array; segment helpers return −60 / DBL_MAX (`0x10261093c` ✓, `0x10261097c`). Ascending assumptions: `0x1027b7cf0`, `0x1027c79d0` (pseudocode) | U |
| 006 | AWarpMarker constructor `0x1026105ec` ✓ (s8-0001): both fields DBL_MAX | S / U |
| 007 | Is-shadow `0x1026102c0` ✓ (last element). Append `0x102612464` ✓: `Beat = q(last + 0.03125)`, `Sec = last + d9·60/d8·0.03125` (the operands' meaning is not traced, so the seconds formula is not specified). Rescale `0x102610bc4` ✓ re-places the last marker at `q(prev + 0.03125)`. `0x1027d304c`, `0x102610fb0` (pseudocode). Remove `0x1033bfa68` ✓, move `0x1033bfb94` ✓. `checks.last_beat_step_is_1/32` | S; D |
| 008 | API `0x1033bf160` ✓ (d7-0001): audio-clip class test, slot +0x300 warped test, `fdiv d0,d8,d0` (t / rate from `0x1027b7514`, pseudocode), tail call slot +0x4b8 with `w1 = 1`. Slot `0x1027beb9c` ✓: helper at clip +0x5b0 (stored by the constructor ✓ s8-0001 at `0x1027b119c`), helper slot +0x198 `0x102893b1c` ✓ → +0x190 `0x1028939a4` ✓: builds once and caches at helper +0x28 a table from clip slot +0x4b0 → +0x4a8 `0x1027c6ec0` ✓ (`ldr x0,[x0,#0x658]`, the list REQ-004 tests) via `0x10277b71c` ✓ (list order, BeatTime → array +0 via `0x101b39d74` ✓, SecTime → array +0x10 via `0x101b39d80` ✓). With `w1 ≠ 0` → `0x102248700` → `0x101b39e20` ✓: upper bound over the first n−1 seconds, k = max(j − 1, 0), `fsub; fsub; fdiv; fmsub; fmadd`, so the value is (bₖ − u·bₖ) + u·bₖ₊₁ with fused operations and no guard for sₖ₊₁ = sₖ. The `w1 = 0` path `0x10224869c` clamps to [0, length] and is not used here. Inverse: `0x1033bf250` ✓ (slot +0x4c0, then `fmul` by the rate), `0x1027bec54` ✓, `0x1022485d8`, `0x101b39d8c` ✓. Help strings at `0x105c1dc05`, `0x105c1dc9c`; errors `Conversion is only available for audio clips`, `Cannot convert sample to beat time for unwarped clips.` | D; S (A3) |
| 009 | Other callers of `0x101b39e20` (`0x10224869c` … `0x102250b34`, `0x102610fb0`, `0x1026119f0`, `0x10282cbe0`) not traced. Collinearity delete `0x1027c724c` ✓ (0.001 s). `checks.warped|…extrapolated…` 292/399, 330/399. Revision 4: Engine `OWarpMarkerList::BeatToSampleTime` `0x1a0660` / `SampleToBeatTime` `0x1a0750` match x86_64 `0x101b6f970` / `0x101b6fa60`. Their Engine callers: `OWarperBase::PlayPosFileSmpl` `0xa94400` (x86_64 `0x10235d1c0`), `OWarperBase::StartSample` `0xa93230` (`0x10235bff0`), `OWarpData::FileBeatToFileSmpl` `0xa928b0`, `_Extrapolate` `0xa92930` (`0x10235b6f0`), `OWarperUnWarped::StartFileSmpl` `0xaa8750` (non-slot branch only), `OWarperRePitch::FindPlayingRange`, `OWarperBeats` and `OWarperElastique` functions. Counts: x86_64 23 callers of `0x101b6f970`, arm64 23 of `0x101b39d8c`. Evidence: [t13-playback-v1](../../analysis/ableton-live-12.4.3/r2/t13-playback-v1/manifest.json) `audio/match-x86.txt`, [playback core](../research/playback-core.md#corrections-to-existing-pages) | S (conversion step); per-mode U |
| 010 | AAudioClip constructor `0x1027b0e40` ✓ (s8-0001): getter triples (`getter-constants.txt`), enum inits `mov w1,#0x6`, `#0x2`; WarpMode at `0x1027b1b00`: `0x101849958` null → 0, else `0x102676cf0` → `0x1026a9ec4` (table `0x105889f90` = 0,1,2,3,4,6). ASampleWarpProperties constructor `0x102883578` ✓ (d7-0002): the same getter triples, `0x1027b2794`/`0x1027b29e0`, and WarpMode from `0x102676cf0` → `0x1026a9ec4` with no null test (`0x102883a14`). Its `IsWarped` default (false in pseudocode) is not specified. Loader skips absent members (n1) | S / U |
| 011 | Stored list `0x1026a9ef8` ✓ (`mov w2,#0x7`); chooser `0x1026aa13c` ✓; short twin `0x1026aa354`, lists `0x1026a9a08` (4), `0x1026a9820` (5) (pseudocode). `distributions.*WarpMode` | S; D |
| 012 | `0x1027b279c` ✓, `0x1027b29e8` ✓; label block `0x105af67ac` (`vtable-reads.txt`); long labels referenced by test code `0x100718e6c`, `0x102820654` | S; labels inferred |
| 013 | Getters in `getter-constants.txt`; labels set in `0x1027b0e40`; integer-step curve `0x101577e1c`; `setting_ranges` | S; D; TransientEnvelope U |
| 014 | Direct store in `0x101487310` (n1); ARemoteableEnum setter range check `0x10156675c` not on the load path | S / U |
| 015 | `0x1033bf42c` ✓ (s8-0001): class and warped tests; `fcmp d8,#0; fccmp d8,d0,#2,ge; b.hi`; insertion scan by `SecTime` stopping at the shadow; left `b.mi` and right checks; q(); bounds `0x1027afd40` ✓ (s8-0002; 999 and 5 BPM; called only from the add). Lookup `0x1027c79d0` (pseudocode): q() then exact match, scan stops past the target. Move limits `0x1027b83bc` not traced. Warp-mode setter `0x1033bded8`/`0x1033be004` (pseudocode, list partly read). Messages: `Cannot add warp marker to an unwarped clip.`, `Warp marker sample time is out of range.`, `Warp marker beat time is ahead of left adjacent marker's beat time.` (beat below the left neighbour), `Warp marker beat time is behind right adjacent marker's beat time.`, `Segment length out of range.`, `The shadow marker can't be deleted.`, `The shadow marker can't be moved.`, `The specified warp marker doesn't exist` | S / U |
| 016 | BeatTime setter `0x1026101b4` ✓ (s8-0003); q() in `0x1033bf42c` ✓; sentinels `0x1055d9680` = (−1.7976931348623155e308, 1.7976931348623155e308, DBL_MAX, +∞) (`s7-midi-notes-v1/vtable-reads.txt` line 470). SecTime setter `0x1026101a0` (pseudocode). `checks.beat_on_1/3843840_grid` 22,029 | S; D |

**Shadow-append evidence (X; no behavioral acceptance case).**

- **X.** The append routine (x86_64 `0x102738d90`, arm64 `0x102612464`) adds a marker with
  `BeatTime = q(b + 1/32)` and `SecTime = s + (p₂ × 60 / p₁) / 32`, where (s, b) is the last
  marker and p₁, p₂ are its two arguments. Run on real `AWarpMarker` lists: (0, 0), (1, 2),
  (2, 3) with p₁ = 120, p₂ = 1 gives (2.015625, 3.03125), M1's shadow; (0, 0) with p₁ = 167,
  p₂ = 1 gives `SecTime` 0.0112275449101796407 and `BeatTime` 0.03125, M0's shadow, bit for
  bit; a last beat of 2.0000001 gives a shadow beat of 2.03125 (rounded) ([results](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/results/envelope-warp.json),
  `warp_REQ007_shadow_*`). **U.** What p₁ and p₂ are at each caller: the clip passes a tempo
  value and its slot +0x2d0 value, neither traced; inferred: the tempo in BPM and a rate
  factor of 1 for an unaltered clip.

**Revision 3 evidence (X).** Extracted execution,
[x2-envelope-warp-v1](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/manifest.json)
(`sh run.sh`; `results/envelope-warp.json`, `raw/runs.jsonl`, `addresses.json`,
`check_rules.py`). Functions run: conversion cores `0x101b6fa60`, `0x101b6f970` (arm64
`0x101b39e20`, `0x101b39d8c`; matched through the scripting entry points `0x103530e40` and
`0x103530f20`, which reference the same error strings, and clip slots +0x4b8/+0x4c0 → helper
slot +0x198 → wrappers `0x10235b790`/`0x10235b660`); shadow append `0x102738d90` (arm64
`0x102612464`, same constants); beat setter `0x102736ce0` (arm64 `0x1026101b4`); add bounds
`0x1028e96b0` (arm64 `0x1027afd40`, called by the add `0x1035310c0` / `0x1033bf42c`). Setup: the
conversion table was written into harness buffers in list order; markers are real `AWarpMarker`
objects from `SNewCompound<AWarpMarker>` `0x102737050`, after the slice's static initialisers
and a class-registry subset (the `AAbstractWarpMarker` and `AWarpMarker` registries were
constructed with the arguments of initialiser 1237, which stops earlier at a `std::regex`); the
setter's change notification `0x10154dfb0` was skipped under gdb; bounds take plain records,
since their getters read only +0x50 and +0x58. Slice comparison: conversion cores fused in both
slices (arm64 `fmsub`/`fmadd`, x86_64 glibc `fma`); q() and the bounds use the same operation
order with no inexact fused step; the only substitution reached is glibc `fma`, which is
correctly rounded like the arm64 instructions.

**Revision 2 evidence.** The warp-markers-v1 review record
[review-checks.txt](../../analysis/ableton-live-12.4.3/handoff-staging/warp-markers-v1-analysis/review/review-checks.txt)
(section 5), its retained corpus records `corpus-excerpts.jsonl` and its edge search
`edges-output.txt` in the same directory. This author re-read the insertion, delete and
`TransientEnvelope` creation records there.

- A2: the review traced `0x1027c1c7c` and its callees (`0x102441a30`, `0x1024dece8`,
  `0x1024dece0`, `0x1015654e0`, `0x1015652f0`, `0x10155e55c`, `0x1027b3928` → `0x102610134`,
  `0x1027b7cf0`, `0x10243afa0`, `0x10256d5ac`, `0x10279b15c`, `0x102440ff0`, `0x10283b098`,
  `0x10283adb8`, `0x101505400`, `0x101506558`), the sample part's `0x10288538c` →
  `0x102884178`, and `0x101486fa8`. Untraced: onset helpers `0x10283b20c` and `0x10283b344`;
  indirect calls `+0x1e8`, `+0x2a0`, `+0x2b0`, `+0x248` and `+0x1b0`.
  `AAudioClip::SetupAutoWarpMarkers` (`0x1027ce7b8`), `AutoWarpIsPending`, `MarkersGenerated`
  and `SamplesToAutoWarp` exist. Their trigger on opening, and whether opening reaches the
  marker writers, were not bounded.
- 008: the warped test, slot `+0x300` = `0x10243ea38` → `0x1015645a0`, reads the member
  registered for `IsWarped` by `0x102435a28` (RVW-06).
- 010, 013: `TransientEnvelope` creation `0x1015743b0` → `0x101568960` stores the initial value
  at `+0x58` with no clamp (corpus).
- 011, 012: the `TransientResolution` labels and `REX` occur only in the stored lists
  `0x1027b279c` and `0x1026a9ef8`; the chooser `0x1026aa13c` has no REX entry (RVW-05).
- 015: `0x1027afd40` selects the lower and upper bound with `fcsel`; `b.hi` and `b.lt` make the
  bounds inclusive and refuse NaN; `0x1021862f0` = (BPM / 60) × Δs. The scan skips the left
  check for the first node. The insertion `0x1027baad8` (corpus) returns when an existing
  marker's `SecTime` or `BeatTime` equals the new marker's. The delete `0x1027c6eec` (corpus)
  returns when the list count is below 3. The move `0x1033bfb94` (s8-0003) tests only the
  audio-clip class. The sample length's source `0x1027b6954` is untraced (RVW-04).
- 015, 016: for gaps of at least 0.0005 s the bounds and the exact tempo disagree only within
  about 0.000004 BPM of a limit, and the add's rounding differs from exact rounding only within
  about 0.0002 grid step of a tie (`edges-output.txt`).

Case values were recomputed with a scratch script (not retained) from the REQ-008 formula and
the REQ-TRANSPORT-STATE-011 writer rule. W0's 14 empty sampler lists and clip C's position
were counted in the decoded W0.

**Corrections to the source packet.**

- The research page says the conversion routine was not located. It is the scripting pair
  above; WM-09 becomes S for the scripting interface (REQ-008) and stays U for playback
  (REQ-009).
- The extension after the last visible marker uses the last two list elements, so it is the
  shadow segment, as WM-09 inferred.
- `getter-constants.txt` left the ComplexProEnvelope default undecoded; it is 128.
- Revision 2: the research page's label and edit-limit statements are corrected in its note of
  2026-10-18.

**Traceability and dropped claims (WM-01 to WM-16).**

| Candidate | Disposition |
| --- | --- |
| WM-01 | REQ-001 |
| WM-02 | REQ-002; units stay inferred |
| WM-03 | REQ-002, REQ-016 |
| WM-04 | Dropped: schema history is not a requirement while older documents are excluded |
| WM-05 | REQ-003, REQ-005; "editing keeps beats non-decreasing" narrowed to the scripting add (REQ-015) |
| WM-06 | REQ-003 |
| WM-07 | REQ-004 under A1 |
| WM-08 | REQ-007; the shadow's seconds formula dropped (operands not traced) |
| WM-09 | REQ-008 (S, scripting) and REQ-009 (U, playback) |
| WM-10 | REQ-006, REQ-010 |
| WM-11 | REQ-015, narrowed to the scripting add; interactive edits U |
| WM-12 | REQ-011, REQ-010; the absent-`WarpMode` default for audio clips is U |
| WM-13 | REQ-014 |
| WM-14 | REQ-012, REQ-013 |
| WM-15 | Dropped to the exclusions (PRB-S8-09). Revision 4: for unwarped clips the seconds unit is S and D in REQ-PLAYBACK-CORE-017 |
| WM-16 | Exclusion (PRB-S8-11) |

Also not carried: the Seg. BPM display rule (pseudocode only; PRB-S8-02 and 07 would have
observed it), the scripting `warp_mode` setter list, the selection of the four- and five-entry
choosers, the recording-path collinearity delete (support for REQ-009 only), and the sampler
`IsWarped` default.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from packet S8 (WM-01 to WM-16) plus two verification rounds (d7-0001, d7-0002) that located and confirmed the scripting conversion. 16 requirements: 3 without unknown parts (003, 012, 016), 11 with D or S clauses and unknown parts, 2 unknown (005, 009). 35 unexecuted cases: 28 gradable (4 in part), 7 unresolved |
| 2 | 2026-10-18 | Applies the warp-markers-v1 review findings ([plan](warp-markers-handoff-plan.md#review-outcome), [REVIEW.md](../../handoff/warp-markers-v1/REVIEW.md)). Applied: F1 and RVW-01 (A2 narrowed to opening and marked on every load and scripting clause, including REQ-003's load clause; saving half is the new A4; "held after opening" defined; later changes by the application excluded); F3 and RVW-03 (REQ-015 as inclusive beat bounds, the zero-distance and first-marker cases, U bands of 0.001 BPM, 0.001 grid step and 0.0005 s; REQ-016 tie band U); F4 (accepted add or remove can leave the list unchanged); F5 (move has no warped check; new WMK-036); F6 and RVW-05 (TransientResolution labels and the code 5 label inferred; loop-mode and parameter names inferred internal names); RVW-02 (TransientEnvelope created at 100 without a clamp; range U); RVW-04 (WMK-029 now 10,000,000 s; sample-length unit assumed); RVW-06 and RVW-07 (assumptions confirmed or stated); RVW-08 (d7 rounds cited from their retained run). F7 needed no change: the text was fixed at release. Rejected: F2, because the review's corpus check shows creation stores 100 without a clamp, so REQ-010 and WMK-021 keep the default; RVW-09, which concerns release status text only. ADR 0003: probe wording changed and static routes named. 16 requirements: 2 without unknown parts (003, 012), 12 with D or S clauses and unknown parts, 2 unknown (005, 009). 36 unexecuted cases: 29 gradable (4 in part), 7 unresolved |
| 3 | 2026-10-18 | Extracted execution X2 ([x2-envelope-warp-v1](../../analysis/ableton-live-12.4.3/r2/x2-envelope-warp-v1/manifest.json)). Added label X. REQ-008 conversion X (cores run, WMK-016 to 019 confirmed); REQ-007 shadow append X with its seconds formula (operands' meaning U); REQ-015 bounds and REQ-016 rounding X as exact 64-bit sequences, which replace revision 2's uncertainty bands; new finding: q(−0) = +0. REQ-009 playback stays U (no static caller to the engine found). New cases WMK-037 to 039. 16 requirements: 2 without unknown parts (003, 012), 12 with D, S or X clauses and unknown parts, 2 unknown (005, 009). 39 cases: 32 gradable (4 in part), 7 unresolved |
| 4 | 2026-10-18 | Correction from [SPEC-PLAYBACK-CORE](playback-core.md) r1 (packet T1.3). REQ-009: revision 3's "no static caller" is wrong. The conversion cores are the Engine's marker-list conversions, called by the warpers' playback functions. The conversion step of warped playback becomes S (Engine names; x86_64 matched; arm64 by caller count). Warping off is stated as not using the markers for session clips (SPEC-PLAYBACK-CORE REQ-017). Per-mode read positions stay U, outside T1. REQ-007's playback inference becomes S. WM-15's unit settled for unwarped clips. 16 requirements: 2 without unknown parts (003, 012), 13 with D, S or X clauses and unknown parts (009 now among them), 1 unknown (005). 39 cases unchanged: 32 gradable (4 in part), 7 unresolved |
| 5 | 2026-10-19 | applies the v2 staging/review findings F1 to F6 and RVW2-02. WMK-019 is computed from confirmed rules, not run by X; WMK-039 adds the discriminating one-ulp-below-half input. A1 is settled by the structure load trace; REQ-002 references the shared conditional list-Id refusal. The unobservable shadow append formula moves to the evidence appendix; REQ-009 explicitly needs playback acceptance and stays unreleased. 16 requirements and 39 cases remain (32 gradable, 7 unresolved); no released expectation changes. |

Before the 2026-10-18 review, a first release candidate could
contain the D and S clauses of REQ-001 to 004, 007, 008 and 010 to 016 with their gradable
cases, under assumptions A1 to A3.

Released 2026-10-18: [warp-markers-v1](../../handoff/warp-markers-v1/README.md), 38 cases, approved with narrowing by a separate review agent (partial REQ-001 to 004, 007, 008, 010 to 013, 015, 016 only; 005, 006, 009, 014 unreleased). The review findings to apply in the next revision are on the [handoff plan](warp-markers-handoff-plan.md#review-outcome). Revision 2 applies them; the release stays pinned to revision 1. The plan's [scope table](warp-markers-handoff-plan.md#scope) lists the released part of each requirement; every other clause of this draft is broader than v1. The current [warp-markers-v2](../../handoff/warp-markers-v2/README.md), released
2026-10-18 with 63 cases, supersedes v1 and repairs its invalid fixture carriers.
Its review withdraws device placement and sample-part case 018 (RVW2-01), excludes
REQ-009 (RVW2-02), and distinguishes executed values from computed-by-rules values
(RVW2-03). It excludes the unobservable shadow-append formula. Revision 5's settled
A1 does not retroactively release the empty-list clause, which v2 omitted.
