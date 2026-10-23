---
id: SPEC-AUDIO-VIDEO-EXPORT
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Live 12 documentary behavior, exact-build applicability unknown
---

# Audio and video export

## Scope and evidence boundary

FEAT-RENDER and FEAT-DELIVERY. This partial draft owns user-selected export
signals/ranges, rendering/encoding options, video eligibility and external-device
render controls. [Project/media workflows](project-media-workflows.md) owns
Set/project dependencies, collection and Packs. [Mix graph](mix-graph.md) and
[playback core](playback-core.md) own their previously stated signal/timing
contracts; their composed expectations are not a measured Live export oracle.
Freeze/flatten, bounce, MIDI export, video editing and detailed codec/DSP quality
remain separate unclosed surfaces.

D12 means stated in the retained official Live 12 chapter, captured 2026-10-19.
**All D12 clauses have exact 12.4.3 applicability U.** U outcomes are ungraded.
No original program/function, codec, external hardware or candidate was run.
The chapter's description of passes/libraries does not require a candidate to
copy the original processing architecture. This contract concerns observable
options, files, signals and workflow; exact samples still need supported metrics.

## Preconditions and controlled state

Use a valid editable test Set, a fresh writable destination and explicitly chosen
track/clip/routing/encoding settings. Reset unrelated automation, solo, mute,
external sync and preferences. State which Session or Arrangement clip is active
on each track. Audio comparisons require a nonzero independently defined source
and known pre/post-fader signals; do not use a constant-zero fixture to test gain,
normalization or tail wrapping. Frame and encoded-duration rounding remain U.

For hardware cases, explicitly configure a functioning external device and route;
absence of that capability leaves those scenarios unexecuted. The Linux analyst
host cannot establish them. An external-device object name alone does not prove
that a particular render must run in real time.

## Requirements

| Requirement ID | Input/state | Observable documented result | Evidence |
| --- | --- | --- | --- |
| REQ-EXPORT-001 | Invoke Export Audio/Video | Open export controls for Set audio and eligible video. | D12/E1 |
| REQ-EXPORT-002 | Choose Main, individual track, all individual or selected tracks | Render the selected post-fader output scope; all-individual includes groups/returns/Main; selected scope uses tracks selected before opening the dialog. | D12/E2 |
| REQ-EXPORT-003 | Individual export includes MIDI-only tracks | Omit MIDI track without instrument/audio effects; a MIDI track with audio effects but no instrument produces silent audio. File naming/collisions U. | D12/E2 |
| REQ-EXPORT-004 | Export multiple tracks over one range | Give all exported track files equal render length. Exact frame and codec-padding interpretation U. | D12/E2 |
| REQ-EXPORT-005 | Set Render Start/Length or select Arrangement time before dialog | Use chosen interval; default covers Set length, preselection supplies the selected interval. Empty/negative/out-of-range values U. | D12/E2 |
| REQ-EXPORT-006 | Session overrides Arrangement, switch focused view | Render active clips per track; switching view alone does not select different source clips. | D12/E2; Arrangement owns override law |
| REQ-EXPORT-007 | Include Return and Main Effects for individual/selected export | Include used returns and Main effects; option disabled for Main output. Numeric mixing, feedback and latency behavior U. | D12/E3 |
| REQ-EXPORT-008 | Render as Loop with an effect tail crossing selected end | Wrap tail contribution into the beginning without extending selected length. Exact initialization/history, tail criterion, gain, samples and arbitrary feedback U. | D12/E3 |
| REQ-EXPORT-009 | Convert to Mono | Create mono output. Channel-combination/gain/phase law U. | D12/E3 |
| REQ-EXPORT-010 | Normalize nonzero finite audio | Apply gain toward documented maximum-headroom peak goal. Numeric peak convention, rounding, silence/NaN and sample comparator U. | D12/E3 |
| REQ-EXPORT-011 | Enable Create Analysis File | Create accompanying ASD; its bytes and later cache/analysis behavior remain outside this contract. | D12/E3 |
| REQ-EXPORT-012 | Choose output sample rate | Encode output at chosen rate. Lower-rate export requires resampling; exact filter, quality bound, delay and internal pass count are not specified here. | D12/E3 |
| REQ-EXPORT-013 | Enable PCM and choose format/depth | Lossless output options include WAV/AIFF/FLAC and 16/24/32-bit controls. Supported format/depth combinations and exact container encoding need separate evidence. | D12/E4 |
| REQ-EXPORT-014 | Select depth below 32 bits | Offer No Dither, Rectangular, Triangular and POW-r 1/2/3; documented default Triangular. Noise sequence, spectrum, correlation, seed and quantitative bound U. | D12/E4 |
| REQ-EXPORT-015 | Enable MP3, alone or with PCM | Offer 320-kbps CBR MP3; documented leading silence makes sample alignment U. Exact padding/metadata/encoding version U. | D12/E4 |
| REQ-EXPORT-016 | Disable both PCM and MP3 | Disable Export action. This is an eligibility rule, not a promised disk-state rollback. | D12/E4 |
| REQ-EXPORT-017 | Create Video with Arrangement video and PCM | Permit accompanying video; video-only or MP3-only video export is unavailable. Output shares audio destination and includes rendered audio. | D12/E5 |
| REQ-EXPORT-018 | Choose installed video encoder | Expose installed choices; Edit settings only when encoder configurable. Default resolution follows source clip unless overridden. Multiple source resolutions and platform codec availability U. | D12/E5 |
| REQ-EXPORT-019 | Render output routed through external audio effect/instrument | Render affected Main/individual scope in real time; unaffected individual tracks can remain offline. Route classification boundaries and measured timing U. | D12/E6 |
| REQ-EXPORT-020 | Begin required real-time render | Show waiting countdown, documented initial value ten seconds; allow a changed duration, countdown Restart and Skip. Timer precision and tail-detection guarantee U. | D12/E6 |
| REQ-EXPORT-021 | Auto-Restart enabled; dropout detected | Restart real-time render; expose attempt count. Detection threshold, false positives, retry limit and completed-file selection U. | D12/E6 |
| REQ-EXPORT-022 | Real-time render Restart/Cancel | Restart returns to waiting stage; Cancel stops and deletes partially rendered file. Unrelated output files, crash atomicity and failure to delete U. | D12/E6 |
| REQ-EXPORT-023 | Invalid path/media/encoder, overwrite, failure, general cancellation or teardown | U: diagnostics, refusal/repair, partial output, prompt/transaction order, cleanup and state retention beyond REQ-022. | U |

## Timing and observability

Audio range, signal scope, file metadata, channel count, options, output eligibility
and progress states are separate comparisons. A correct file header does not
prove resampling, mono summing, dither, normalization or return processing.
No generic audio tolerance or response deadline has been established. Decoder
padding prevents applying PCM sample-count rules to MP3 by assumption.

The manual describes two-pass loop rendering and a named downsampling library.
Those are explanatory implementation observations, not required architecture.
The retained documentary contract is the output/range goal; exact audio still
has an explicitly ungraded oracle gap. Real-time rendering is not the T1 offline
comparison vehicle and does not inherit its settled-start convention silently.

## Acceptance cases

F1: valid Set with two audio tracks A/B containing distinct nonzero PCM clips,
a group G, return R and Main; a pure-MIDI track M0 without instrument/audio
FX, and MIDI track MF with only audio effects whose behavior with zero input
has been independently established as silent. F2: separately controlled Session
and Arrangement clips. F3: known audible effect with a tail crossing the selected
range. F4: a valid video clip placed in the Arrangement and an installed configurable
encoder. EXP-023 additionally requires both configurable and nonconfigurable
installed choices; otherwise that scenario is unexecuted. F5: functioning
external hardware route. Every scenario resets its own fixture/preferences.

| Case | Requirement | Kind | Controlled action | Proposed comparator / explicit limit |
| --- | --- | --- | --- | --- |
| EXP-001 | 001 | Positive | Open export dialog from F1. | Named controls present; no rendered output yet asserted. |
| EXP-002 | 002 | Signal scope | Export Main, then A alone. | Chosen post-fader scope; audio oracle needed for sample grading. |
| EXP-003 | 002 | Multi-track | Select A/B before dialog, choose Selected. | Only selected eligible outputs; destination names U. |
| EXP-004 | 002 | Group/return | Export all individual F1 tracks. | G/R/Main included in eligible output inventory. |
| EXP-005 | 003 | MIDI boundary | Inspect M0 and MF results in all-individual export. | M0 omitted; MF silent output; silence cannot test other DSP clauses. |
| EXP-006 | 004 | Range | Export A/B/G/R/Main with equal PCM settings. | Equal file lengths; exact interval endpoint ownership U. |
| EXP-007 | 005 | Range | Choose nonempty time selection, open dialog; then edit start/length. | Selected then chosen interval reflected; frame rounding U. |
| EXP-008 | 006 | Ownership | F2 Session overrides A; switch focused view and export. | Source clip choice unchanged by focus; exact scheduler sample U. |
| EXP-009 | 007 | Effects | Keep identifiable Return/Main effects enabled and A→R send nonzero; toggle Include Return/Main Effects off/on. | Inclusion follows option; numeric audio result ungraded. |
| EXP-010 | 007 | Negative | Choose Main output. | Include Return/Main Effects disabled. |
| EXP-011 | 008 | Tail | F3, compare normal/loop export over same interval. | Same interval length; documented tail-wrap goal, waveform/tolerance U. |
| EXP-012 | 009 | Channels | Export known stereo F1 with mono enabled. | One output channel; combination law U. |
| EXP-013 | 010 | Gain | F1 nonzero finite signal, Normalize on. | Documented peak goal only; quantitative normalization comparator U. |
| EXP-014 | 011 | Sidecar | Export with ASD enabled to empty destination. | Accompanying ASD exists; byte format U. |
| EXP-015 | 012 | Rate | Export at Set rate, higher rate and lower rate. | Chosen output-rate metadata; resampling quality/delay U. |
| EXP-016 | 013 | Encoding | Choose each offered PCM format and supported depth. | Corresponding format/depth metadata; unsupported pair behavior U. |
| EXP-017 | 014 | Dither UI | At supported sub-32-bit depth, inspect modes/default. | Documented choices/default; no stochastic-audio pass. |
| EXP-018 | 014 | Boundary | Select 32-bit depth. | Dither behavior U outside documented sub-32-bit condition. |
| EXP-019 | 015 | MP3 | Export MP3 alone, then MP3+PCM. | Requested output formats; 320-kbps CBR metadata; padding/audio U. |
| EXP-020 | 016 | Negative | PCM off and MP3 off. | Export disabled. |
| EXP-021 | 017 | Video eligibility | F4 with PCM on, then PCM off/MP3 only. | Video availability follows stated prerequisite; files ungraded for unsupported path. |
| EXP-022 | 017 | Video output | Export F4 eligible audio+video. | Shared destination and rendered audio included; encode quality U. |
| EXP-023 | 018 | Encoder | Select configurable and nonconfigurable installed encoders. | Edit availability differs; external settings semantics U. |
| EXP-024 | 018 | Resolution | F4 single source resolution, no override. | Output resolution follows source; encoder rounding U. |
| EXP-025 | 019 | Hardware route | Export F5 affected Main and unaffected individual track. | Real-time versus offline mode classification; runtime/latency U. |
| EXP-026 | 020 | Countdown | Begin F5 render; change countdown; Restart; Skip. | Documented displayed states; no wall-clock tolerance asserted. |
| EXP-027 | 021 | Dropout | With Auto-Restart on, observe a dropout acknowledged/detected by Live. | Conditional restart/attempt indication; whether an injected physical gap triggers detection U. |
| EXP-028 | 022 | Restart | Restart active F5 render. | Waiting stage entered again. |
| EXP-029 | 022 | Cancellation | Cancel after a partial F5 file is created. | Stop and partial-file deletion; deletion-failure branch U. |
| EXP-030 | 023 | Malformed | Invalid source/video or unavailable encoder. | U diagnostics, decoder failure and preserved state. |
| EXP-031 | 023 | Failure | Unwritable/full/disconnected destination. | U partial outputs, rollback and retry. |
| EXP-032 | 023 | Overwrite | Existing output names collide. | U prompts, naming and replacement atomicity. |
| EXP-033 | 023 | General cancel | Cancel offline/multipass export or video encoding. | U beyond the specific real-time case. |
| EXP-034 | 023 | Teardown | Close/replace Set or application during export. | U operation ownership, prompts, saved state and cleanup. |

These are 34 unexecuted scenario definitions, not executable renderer fixtures.
Most D12 cases are narrow option/state/metadata checks; their ungraded audio,
platform and scheduler clauses remain visible. All exact-target results are U.
Applicable malformed/negative/boundary/cancel/teardown kinds are explicit;
undo has no established export transaction contract and stays U under REQ-023.

## Open questions and remaining scope

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns version applicability. Remaining export gaps: frame rounding, active-clip
scheduler capture, returned-effect composition/latency, loop initialization/tails,
mono gain, normalization precision, resampler quality/delay, dither distribution,
format/depth support matrix, MP3 padding, filenames/overwrite, video/multi-source
resolution/codecs, external route classification, dropout detection, partial-file
failure/rollback, cancel/teardown and whether any export operation is undoable.

## Analyst evidence appendix

The owning [research page](../research/audio-video-export.md) links the shared
immutable source capture. This packet reuses the same captured chapter as
project/media workflows, without making a second competing original.

| Key | Exact HTML heading ID in retained Managing Files and Sets capture |
| --- | --- |
| E1 | `exporting-audio-and-video` |
| E2 | `selection-options` |
| E3 | `rendering-options` |
| E4 | `encoding-options` |
| E5 | `video-rendering-options` |
| E6 | `real-time-rendering` |

No image was inspected. Named original libraries and pass descriptions do not
release an implementation design, original source or observed codec result.

## Revision and handoff

Revision 1 adds 23 requirements and 34 scenarios, partial documentary behavior
with quantitative/platform/lifecycle gaps. Independent review pending; no release.
