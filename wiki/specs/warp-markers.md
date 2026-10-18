---
id: SPEC-WARP-MARKERS
type: spec
status: draft
revision: 1
updated: 2026-10-17
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
static derivation, or explicitly unknown. Nothing was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first draft.
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
| U | Unknown; no expected result. PRB IDs name the Phase 4 probe that would settle it |

Only D and S clauses may enter a release. U clauses block the behavior they name. Inferred
statements are marked **Inferred** and carry no requirement.

Static clauses rest on these assumptions:

| ID | Assumption | Affects |
| --- | --- | --- |
| A1 | The per-object check that runs after an audio clip is read runs when a Live Set is opened. This is inferred, not traced; it is the same assumption as in SPEC-MIDI-NOTE-STORAGE | REQ-004 |
| A2 | Opening a set and saving it with no edit does not change a clip's markers or warp settings (no re-analysis, auto-warp or region-driven change). Not traced | Every case that compares saved values |
| A3 | A conversion called right after opening uses the marker list as loaded. The conversion table is built on first use; when it is rebuilt after edits was not traced | REQ-008 cases |

**Refused** means that loading stops with an error of the corrupt-document class of
SPEC-ALS-CONTAINER. What the user then sees, and what stays loaded, is U
(REQ-ALS-CONTAINER-009). For the scripting interface, **refused** means the call raises an
error and the list is unchanged; the error kinds are named in the requirement.

## Exclusions

These have no requirement in this revision. They are not graded, and fixtures avoid them.

- **Audio output.** Time-stretching output for every warp mode, the audible effect of the
  mode settings, Re-Pitch pitch change and the quality switches. Compatibility needs measured
  comparison (PRB-S8-11).
- **Playback timing.** Which position of the sample plays at a given song time (REQ-009).
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
  digits as raw bits. Text with no numeric prefix is refused. The loaded value is stored
  without rounding, clamping or a range check.
- **S.** On save both are written by the 64-bit rule of REQ-TRANSPORT-STATE-011. All
  44,058 shipped values match that rule (D).
- **U.** How `Id` is read and whether it is preserved. Shipped `Id`s are unique within a list
  but not always ascending (18 lists). Cases do not compare `Id`.
- **Inferred.** `SecTime` is seconds from the start of the sample and `BeatTime` is beats of
  clip time. Support: REQ-008 divides a sample-frame position by the sample rate before
  comparing it with `SecTime`, and shipped region fields agree with markers extrapolated to
  the sample start and end (330 and 292 of 399 warped clips).

### REQ-WARP-MARKERS-003 — well-formed marker lists

Support: documented and static-derived.

- **D.** In shipped documents every marker list with two or more markers is strictly
  increasing in both `SecTime` and `BeatTime` (10,250 of 10,250). Every shipped audio clip has
  at least two markers, warped or not; shipped `SampleWarpProperties` have 0, 2 or 3.
- **S.** An audio clip list of at least two markers, strictly increasing in both attributes,
  loads with each marker's values as stored and in document order. A later save writes the
  same values in the same order (A2).

### REQ-WARP-MARKERS-004 — empty marker list

Support: static-derived, with unknown parts.

- **S (A1).** An `AudioClip` whose `WarpMarkers` has no `WarpMarker` is refused. The error
  detail is an empty warp marker array.
- **S.** `SampleWarpProperties` have no such check: an empty list there does not cause a
  refusal. 4,244 shipped `SampleWarpProperties` have empty lists (D).
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

- **S.** A `WarpMarker` without `SecTime` or `BeatTime` keeps the largest finite 64-bit value
  for that attribute. `Invalid` text loads the same value (REQ-002).
- **U.** Whether such a set opens, what the clip shows and what a save writes (PRB-S8-04).

### REQ-WARP-MARKERS-007 — the shadow marker

Support: documented and static-derived, with unknown parts.

- **S.** Live treats the last element of an audio clip's marker list as the *shadow marker*.
  In the scripting conversion, the segment from the last visible marker to the shadow marker
  governs everything after the last visible marker (REQ-008); for playback this is inferred
  (REQ-009).
- **S.** Where Live creates or re-places the shadow marker, it puts it 1/32 beat after the
  preceding marker, with the beat rounded as in REQ-016. Which user operations do this is U.
- **D.** In shipped lists the last marker is exactly 1/32 beat after the previous one in
  2,869 of 2,878 audio clips and 7,313 of 7,372 sampler lists; the others use 1/16 or 1/64.
- **S (A2).** On load a different spacing is kept: no step moves the last marker.
- **S.** The scripting interface refuses to delete or move the shadow marker (REQ-015).
- **U.** Whether a later edit or save re-places a shadow that is not 1/32 beat after its
  predecessor (PRB-S8-07); whether a sampler list's last marker has the same role.

### REQ-WARP-MARKERS-008 — scripting conversion between sample time and beat time

Support: documented and static-derived, with unknown parts.

Let the clip's list be (s₀, b₀) … (sₙ₋₁, bₙ₋₁) in list order (`SecTime`, `BeatTime`), with
n ≥ 2 and both coordinates strictly increasing, and let R be the clip's sample rate in Hz.

- **D, S.** `sample_to_beat_time` and `beat_to_sample_time` are available for audio clips
  only and raise an error when the clip is not warped.
- **S.** `sample_to_beat_time(t)` takes a position t in sample frames and sets x = t / R. It
  selects segment k: the largest index from 0 to n − 2 with sₖ ≤ x, or 0 when x < s₀. It
  returns bₖ + (x − sₖ)(bₖ₊₁ − bₖ)/(sₖ₊₁ − sₖ) in 64-bit floating point.
- **S.** `beat_to_sample_time(b)` selects k the same way over b₀ … bₙ₋₂, computes
  x = sₖ + (b − bₖ)(sₖ₊₁ − sₖ)/(bₖ₊₁ − bₖ) and returns x × R.
- **S.** The result is linear inside each segment. Before the first marker the first segment
  is extended. At or after the last visible marker sₙ₋₂ the segment to the shadow marker is
  extended. Results are not limited to the sample or to the marker range.
- **U.** Results for n = 1, equal adjacent coordinates, or an unsorted list; the result after
  marker edits (A3).

### REQ-WARP-MARKERS-009 — playback position of a warped clip

Support: unknown.

- **U.** Which sample position plays at a given clip beat (PRB-S8-08).
- **Inferred.** Playback uses the mapping of REQ-008, including both extensions. Support: the
  same interpolation is shared by other callers whose roles were not traced; shipped region
  fields match the extended mapping; Live deletes a marker recorded on the straight line of
  its neighbours, which only makes sense for a piecewise-linear mapping.

### REQ-WARP-MARKERS-010 — absent warp settings

Support: static-derived, with unknown parts.

- **S.** An absent setting element, or one without its `Value` attribute, leaves the value
  set when the clip or sample was created. For both holders these are the defaults in REQ-012
  and REQ-013: `TransientResolution` 6, `TransientLoopMode` 2, `GranularityTones` 30,
  `GranularityTexture` 65, `FluctuationTexture` 25, `TransientEnvelope` 100,
  `ComplexProFormants` 100, `ComplexProEnvelope` 128. Absence is not refused.
- **S.** A new `SampleWarpProperties` takes `WarpMode` from the default-warp-mode preference
  (preference index 0 to 5 gives code 0, 1, 2, 3, 4, 6). A new audio clip does the same when
  the application's preference store is present, and takes 0 otherwise.
- **U.** The `WarpMode` an audio clip gets when the element is absent from a loaded set, and
  the preference's factory value (PRB-S8-10). **Inferred:** the preference is the Default
  Warp Mode setting.

### REQ-WARP-MARKERS-011 — warp mode codes

Support: static-derived, with unknown parts.

- **S.** `WarpMode` codes and their labels: 0 Beats, 1 Tones, 2 Texture, 3 Re-Pitch,
  4 Complex, 5 REX, 6 Complex Pro.
- **S.** Live's warp mode chooser lists six labels: Beats, Tones, Texture, Re-Pitch, Complex,
  Complex Pro (no REX). Shorter four- and five-entry chooser lists also exist; when they are
  used is U.
- **Inferred.** The chooser shows the label of the stored code. Shipped audio clips use 0, 3,
  4 and 6; sampler lists also 1 and 2; no shipped document uses 5 (D).

### REQ-WARP-MARKERS-012 — transient resolution and transient loop mode codes

Support: static-derived.

- **S.** `TransientResolution`: 0 1 Bar, 1 1/2, 2 1/4, 3 1/8, 4 1/16, 5 1/32, 6 Transients.
  Default 6.
- **S.** `TransientLoopMode`: 0 LoopOs, 1 LoopFwd, 2 LoopAlt. Default 2.
- **Inferred.** The displayed loop-mode labels are Off, Loop Forward and Loop Back-and-Forth.

### REQ-WARP-MARKERS-013 — mode setting domains and defaults

Support: static-derived, with unknown parts.

- **S.** Live creates each setting with this range and default:

  | Field | Parameter name | Minimum | Maximum | Default |
  | --- | --- | --- | --- | --- |
  | `GranularityTones` | Granularity Tones | 12 | 100 | 30 |
  | `GranularityTexture` | Granularity Texture | 2 | 263 | 65 |
  | `FluctuationTexture` | Fluctuation Texture | 0 | 100 | 25 |
  | `ComplexProFormants` | Complex Pro spectral envelope factor | 0 | 100 | 100 |
  | `ComplexProEnvelope` | Complex Pro spectral envelope order | 8 | 256 (integer steps) | 128 |
  | `TransientEnvelope` | — | 0 | U | 100 |

- **D.** Every shipped audio clip carries the defaults. Shipped sampler values lie inside the
  ranges (Tones 12–80.0625, Texture 2–132.5, Fluctuation 0–100, TransientEnvelope 0–100,
  Formants 0–100, ComplexProEnvelope 8–128).
- **U.** The range of `TransientEnvelope`: the parameter is created with maximum 1.0 and
  default 100, while its curve and shipped values use 0–100 (PRB-S8-06).
- **Inferred.** Beats uses the three transient settings, Tones uses `GranularityTones`,
  Texture uses `GranularityTexture` and `FluctuationTexture`, and Complex Pro uses the two
  `ComplexPro*` settings.

### REQ-WARP-MARKERS-014 — out-of-range codes and settings on load

Support: static-derived, with unknown parts.

- **S.** A well-formed `WarpMode`, `TransientResolution`, `TransientLoopMode` or setting
  value outside its codes or range does not cause a refusal. It is stored without a check or
  a clamp.
- **U.** The value Live then uses, displays and writes on the next save, for `WarpMode` 5 on
  a non-REX sample, 7 or −1 (PRB-S8-05), and for settings outside REQ-013 (PRB-S8-06).

### REQ-WARP-MARKERS-015 — marker edits through the scripting interface

Support: static-derived, with unknown parts.

`add_warp_marker` takes a sample time p (seconds, the unit of `SecTime`) and a beat q.

- **S.** The add is refused when the clip is not an audio clip, when it is not warped, or
  when p is not within 0 ≤ p ≤ the sample length in seconds (a NaN p is refused).
- **S.** The new marker goes before the first marker whose `SecTime` is greater than p, or
  before the shadow marker if none is. The marker before it is the left neighbour; the marker
  after it is the right neighbour, unless that is the shadow marker.
- **S.** Refused if q, as given, is below the left neighbour's beat or above the right
  neighbour's beat.
- **S.** q is then rounded as in REQ-016. Refused if, with the rounded beat, the segment tempo
  to the left neighbour or to the right neighbour would lie outside 5 to 999 BPM, where the
  segment tempo is Δbeat / Δseconds × 60. No limit applies on the shadow side.
- **S.** `remove_warp_marker(q)` and `move_warp_marker(q, d)` find the marker whose beat
  equals q rounded as in REQ-016 (lookup derived with weaker support; see the appendix). They
  are refused when no marker matches or when it is the shadow marker. The remove does not require the clip to be warped.
- **U.** The resulting list after an accepted add, including the shadow; the limits of
  `move_warp_marker`; the warp modes the scripting `warp_mode` setter accepts; whether
  interactive edits apply the same limits.

### REQ-WARP-MARKERS-016 — beat grid

Support: documented and static-derived.

- **S.** Live's marker beat setter, the scripting add and the scripting marker lookups round a
  beat to the nearest multiple of 1/3,843,840 beat, with halves away from zero. The values ±1.7976931348623155e308, the largest finite value and +∞ are
  not rounded.
- **S.** Load does not round: a loaded `BeatTime` keeps its value (REQ-002). The scripting add
  does not round `SecTime`.
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
  set.
- *Script*: Open, then call the named scripting function on clip C with no prior edit; record
  the return value or the error. A case listing several calls makes each on a fresh Open.

**Comparators.** Attribute text is compared exactly, except marker `Id`s. Scripting beats
are compared within 1e-9 beat and sample positions within 1e-6 frame. Labels in *italics*
are inferred display text and are not graded. Cases expecting "unresolved" must not be
graded as passes.

**Case kinds.** P positive, N negative (refused), B boundary, M missing input, S save text,
U unresolved. All expected results are static derivations or shipped-document facts; none
has been run.

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
| WMK-029 | 015 | N | M1; Script add (−0.1 s, 0); add (50 s, 100) | Each refused: sample time out of range | W0+M1 |
| WMK-030 | 015 | N | M1; Script add (1.5 s, 1.9) | Refused: beat below the left neighbour | W0+M1 |
| WMK-031 | 015 | N | M1; Script add (1.5 s, 3.5) | Refused: beat above the right neighbour | W0+M1 |
| WMK-032 | 015 | N | M1; Script add (1.5 s, 2.01); add (0.5 s, 1.99) | Each refused: segment tempo out of range (left side 1.2 BPM; right side 1.2 BPM) | W0+M1 |
| WMK-033 | 015 | P | M1; Script add (1.5 s, 2.5) | Accepted (tempi 60 and 60 BPM) | W0+M1 |
| WMK-034 | 015 | B | M1; Script add (2.5 s, 4) | Accepted: the right neighbour is the shadow, so only the left limit applies (120 BPM) | W0+M1 |
| WMK-035 | 015, 016 | B | M1; Script `remove_warp_marker(2.0000001)`; `remove_warp_marker(2.001)` | First accepted (rounds to beat 2); second refused: no such marker | W0+M1 |

Cancellation and teardown kinds are omitted: loading, saving and the scripting calls in scope
have no cancellable step or resource. REQ-009 has no case: it is U, and PRB-S8-08 defines its
measurement. Thirty-five cases: 28 gradable (WMK-006 for refusal
only, WMK-025 to 027 for opening only) and 7 unresolved (WMK-008 to 013, 022).

## Open questions

No question-register entry exists for FEAT-WARP yet. Open items, each with its probe in the
[S8 probe batch](../../analysis/ableton-live-12.4.3/r2/s8-warp-v1/probe-batch.json):

- empty-list presentation and assumption A1 (PRB-S8-01);
- one-marker, unordered and equal-time lists (PRB-S8-02, 03);
- missing and `Invalid` positions (PRB-S8-04);
- out-of-range `WarpMode` (PRB-S8-05) and settings, including the `TransientEnvelope` range
  (PRB-S8-06);
- shadow spacing after edits and saves (PRB-S8-07);
- playback mapping (PRB-S8-08); region-field units (PRB-S8-09);
- absent `WarpMode` and the preference (PRB-S8-10); per-mode audio (PRB-S8-11);
- not yet covered by any probe: assumption A2, A3, the list after an accepted scripting add,
  and the scripting `warp_mode` setter. PRB-S8-08 could add WMK-016 to 018 as scripting calls.

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
`0x102610264`, `0x1027c6ed0`, `0x1027c6ec0`, `0x102883578`). They sit in
`/var/tmp/sound-analysis/query-spool-2/results/d7-000{1,2}/` and are not yet copied into a
retained run. `queries.json` SHA-256 prefixes: d7-0001 `1dede799`, d7-0002 `ce8a537e`;
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
| 003 | `checks.*strictly_increasing` 2,878 + 7,372; `count=…` rows. Document order: the list loader's child order is not traced; for strictly increasing input any sorting gives the same order | D; S (A2) |
| 004 | AAudioClip post-load slot +0xd0 = `0x1027c1c7c` ✓ (s8-0001): `ldr x0,[x19,#0x658]; bl 0x10156da34; cbnz` → `Empty warp marker array.` → `0x101488e64` ✓ → `0x10148229c`. Empty test `0x10156da34`/`0x101467280` ✓ (s8-0003). ASampleWarpProperties post-load `0x10288538c` ✓ (s8-0002) has no such test. Post-load runs when context flag +0x2c is set (A1) | S (A1) |
| 005 | One marker: the conversion `0x101b39e20` ✓ then reads index 1 of a one-element array; segment helpers return −60 / DBL_MAX (`0x10261093c` ✓, `0x10261097c`). Ascending assumptions: `0x1027b7cf0`, `0x1027c79d0` (pseudocode) | U |
| 006 | AWarpMarker constructor `0x1026105ec` ✓ (s8-0001): both fields DBL_MAX | S / U |
| 007 | Is-shadow `0x1026102c0` ✓ (last element). Append `0x102612464` ✓: `Beat = q(last + 0.03125)`, `Sec = last + d9·60/d8·0.03125` (the operands' meaning is not traced, so the seconds formula is not specified). Rescale `0x102610bc4` ✓ re-places the last marker at `q(prev + 0.03125)`. `0x1027d304c`, `0x102610fb0` (pseudocode). Remove `0x1033bfa68` ✓, move `0x1033bfb94` ✓. `checks.last_beat_step_is_1/32` | S; D |
| 008 | API `0x1033bf160` ✓ (d7-0001): audio-clip class test, slot +0x300 warped test, `fdiv d0,d8,d0` (t / rate from `0x1027b7514`, pseudocode), tail call slot +0x4b8 with `w1 = 1`. Slot `0x1027beb9c` ✓: helper at clip +0x5b0 (stored by the constructor ✓ s8-0001 at `0x1027b119c`), helper slot +0x198 `0x102893b1c` ✓ → +0x190 `0x1028939a4` ✓: builds once and caches at helper +0x28 a table from clip slot +0x4b0 → +0x4a8 `0x1027c6ec0` ✓ (`ldr x0,[x0,#0x658]`, the list REQ-004 tests) via `0x10277b71c` ✓ (list order, BeatTime → array +0 via `0x101b39d74` ✓, SecTime → array +0x10 via `0x101b39d80` ✓). With `w1 ≠ 0` → `0x102248700` → `0x101b39e20` ✓: upper bound over the first n−1 seconds, k = max(j − 1, 0), `fsub; fsub; fdiv; fmsub; fmadd`, so the value is (bₖ − u·bₖ) + u·bₖ₊₁ with fused operations and no guard for sₖ₊₁ = sₖ. The `w1 = 0` path `0x10224869c` clamps to [0, length] and is not used here. Inverse: `0x1033bf250` ✓ (slot +0x4c0, then `fmul` by the rate), `0x1027bec54` ✓, `0x1022485d8`, `0x101b39d8c` ✓. Help strings at `0x105c1dc05`, `0x105c1dc9c`; errors `Conversion is only available for audio clips`, `Cannot convert sample to beat time for unwarped clips.` | D; S (A3) |
| 009 | Other callers of `0x101b39e20` (`0x10224869c` … `0x102250b34`, `0x102610fb0`, `0x1026119f0`, `0x10282cbe0`) not traced. Collinearity delete `0x1027c724c` ✓ (0.001 s). `checks.warped|…extrapolated…` 292/399, 330/399 | U; inferred |
| 010 | AAudioClip constructor `0x1027b0e40` ✓ (s8-0001): getter triples (`getter-constants.txt`), enum inits `mov w1,#0x6`, `#0x2`; WarpMode at `0x1027b1b00`: `0x101849958` null → 0, else `0x102676cf0` → `0x1026a9ec4` (table `0x105889f90` = 0,1,2,3,4,6). ASampleWarpProperties constructor `0x102883578` ✓ (d7-0002): the same getter triples, `0x1027b2794`/`0x1027b29e0`, and WarpMode from `0x102676cf0` → `0x1026a9ec4` with no null test (`0x102883a14`). Its `IsWarped` default (false in pseudocode) is not specified. Loader skips absent members (n1) | S / U |
| 011 | Stored list `0x1026a9ef8` ✓ (`mov w2,#0x7`); chooser `0x1026aa13c` ✓; short twin `0x1026aa354`, lists `0x1026a9a08` (4), `0x1026a9820` (5) (pseudocode). `distributions.*WarpMode` | S; D |
| 012 | `0x1027b279c` ✓, `0x1027b29e8` ✓; label block `0x105af67ac` (`vtable-reads.txt`); long labels referenced by test code `0x100718e6c`, `0x102820654` | S; labels inferred |
| 013 | Getters in `getter-constants.txt`; labels set in `0x1027b0e40`; integer-step curve `0x101577e1c`; `setting_ranges` | S; D; TransientEnvelope U |
| 014 | Direct store in `0x101487310` (n1); ARemoteableEnum setter range check `0x10156675c` not on the load path | S / U |
| 015 | `0x1033bf42c` ✓ (s8-0001): class and warped tests; `fcmp d8,#0; fccmp d8,d0,#2,ge; b.hi`; insertion scan by `SecTime` stopping at the shadow; left `b.mi` and right checks; q(); bounds `0x1027afd40` ✓ (s8-0002; 999 and 5 BPM; called only from the add). Lookup `0x1027c79d0` (pseudocode): q() then exact match, scan stops past the target. Move limits `0x1027b83bc` not traced. Warp-mode setter `0x1033bded8`/`0x1033be004` (pseudocode, list partly read). Messages: `Cannot add warp marker to an unwarped clip.`, `Warp marker sample time is out of range.`, `Warp marker beat time is ahead of left adjacent marker's beat time.` (beat below the left neighbour), `Warp marker beat time is behind right adjacent marker's beat time.`, `Segment length out of range.`, `The shadow marker can't be deleted.`, `The shadow marker can't be moved.`, `The specified warp marker doesn't exist` | S / U |
| 016 | BeatTime setter `0x1026101b4` ✓ (s8-0003); q() in `0x1033bf42c` ✓; sentinels `0x1055d9680` = (−1.7976931348623155e308, 1.7976931348623155e308, DBL_MAX, +∞) (`s7-midi-notes-v1/vtable-reads.txt` line 470). SecTime setter `0x1026101a0` (pseudocode). `checks.beat_on_1/3843840_grid` 22,029 | S; D |

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
| WM-15 | Dropped to the exclusions (PRB-S8-09) |
| WM-16 | Exclusion (PRB-S8-11) |

Also not carried: the Seg. BPM display rule (pseudocode only; PRB-S8-02 and 07 observe it),
the scripting `warp_mode` setter list, the selection of the four- and five-entry choosers, the
recording-path collinearity delete (support for REQ-009 only), and the sampler `IsWarped`
default.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from packet S8 (WM-01 to WM-16) plus two verification rounds (d7-0001, d7-0002) that located and confirmed the scripting conversion. 16 requirements: 3 without unknown parts (003, 012, 016), 11 with D or S clauses and unknown parts, 2 unknown (005, 009). 35 unexecuted cases: 28 gradable (4 in part), 7 unresolved |

Not reviewed, not released, and no handoff plan exists. A first release candidate could
contain the D and S clauses of REQ-001 to 004, 007, 008 and 010 to 016 with their gradable
cases, under assumptions A1 to A3.
