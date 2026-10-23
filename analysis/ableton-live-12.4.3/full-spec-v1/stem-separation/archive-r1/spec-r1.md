---
id: SPEC-STEM-SEPARATION
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Stem separation workflows

This partial F-04/F-07 contract covers documented stem selection, dialog commands,
result placement, source-region/effect/automation roles and generated-file context.
The [coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/stem-separation.md) owns exact sources and interpretations.
This is not an audio/model specification, complete chapter coverage or released input.

**D12/target-U:** current Version12 manual prose only. Feature/command/model
availability in12.4.3 and all target outcomes/comparisons remain null/U/unexecuted.
All signal/timing/file documentary outputs/comparators are also null; source
claims are retained as context. No model, original application, audio processing,
native function, network, hardware or candidate ran. Figures were not inspected.

## Canonical boundaries

[Media](media-file-workflows.md) owns admitted source import/decode and generic
file/cache behavior; [Clip View](clip-view-workflows.md), [Arrangement](arrangement-editing.md)
and [Warp](warp-markers.md) retain region/loop/split/crop and finite marker laws.
This adds only stem-specific region/placement predicates, without stretching or
boundary algorithms. [Recording](recording-comping.md) retains output-format
settings; [project/media](project-media-workflows.md) owns file management.
[Racks](device-racks.md), [hosting](bundled-device-hosting.md),
[automation](automation-envelopes.md) and [routing](routing-monitoring-latency.md)
retain device/track/envelope semantics. This page adds transfer roles only.
Existing owner/releases and unknowns are preserved; no algorithm or finite law is expanded.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/fixtures.json).
Confirm supported available inputs and active nonzero source/effect/automation
before absence/placement trials. Compound branches and missing case kinds stay
open. Feature label, silence, track presence or a file extension is not DSP proof.

### REQ-STEM-SEPARATION-001 — Offline separation and source roles

**D12/target-U.** The manual describes separation inside Live without Internet or additional external tools, for mono/stereo recorded audio. This is an offline-workflow claim, not a requirement to reproduce the named private deep-learning mechanism or accept every file/container. Existing media owners retain import/decode eligibility.

Evidence: `STEM-B006`, `STEM-B007`, `STEM-B008`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-002 — Command entry and options dialog

**D12/target-U.** Separate Stems to New Audio Tracks is documented in context/Create menus for Browser audio files and Session/Arrangement audio clips; invoking it opens the separation options dialog. Exact unsupported input, command enablement and platform shortcut behavior remain unknown.

Evidence: `STEM-B010`, `STEM-B011`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-003 — Element selection

**D12/target-U.** Vocals, Drums, Bass and Others toggles choose included elements. Others denotes parts not detected as the other three. No exact classifier, perceptual-purity, reconstruction, source-isolation or stochastic-output law follows.

Evidence: `STEM-B007`, `STEM-B012`, `STEM-B032`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-004 — Merge selection eligibility

**D12/target-U.** Merge to Single Track combines selected parts and can be enabled only with two or three elements selected. With one or all four selected the checkbox cannot be activated. Zero-selected behavior, changing selection after enable and disabled-versus-hidden presentation are unknown.

Evidence: `STEM-B013`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-005 — Quality selector

**D12/target-U.** The dialog offers High Speed and High Quality. They represent documented speed/quality choices, without a processing-time bound, SDR threshold, universal quality ordering, model identity or output-sample oracle.

Evidence: `STEM-B014`, `STEM-B026`, `STEM-B027`, `STEM-B028`, `STEM-B031`, `STEM-B032`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-006 — Separate and transport stop

**D12/target-U.** Separate starts the process; if playback is running it stops when separation begins. Completion latency, stop timing, recording interaction, cancellation and failure atomicity remain unknown.

Evidence: `STEM-B015`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-007 — Separate multiple-element structure and colors

**D12/target-U.** For multiple unmerged output elements, each resulting stem is a clip on its own track in a new Group Track. Stem track/clip colors correspond to dialog toggles; the group uses the source clip track color. Exact palette, source-less Browser color and track placement/order are unknown.

Evidence: `STEM-B016`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-008 — Single and merged output structure

**D12/target-U.** One separated element creates a single track/clip instead of a group. With Merge enabled the merged stem is placed on a new track whose track/clip color uses source track color. Exact input insertion position and effect/automation placement in these nongroup branches are unknown.

Evidence: `STEM-B017`, `STEM-B018`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-009 — Clip region and warped-loop processing

**D12/target-U.** For Session/Arrangement clips, adjusted start/end markers restrict separation to the audible region. With a warped loop, the manual describes processing from the start marker through the active loop region. Exact end inclusivity, loop cycles, offset mapping, Warp rendering and sample boundaries remain unknown.

Evidence: `STEM-B019`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-010 — Arrangement time-selection command

**D12/target-U.** Separate Stems for Time Selection is a clip context-menu route on an Arrangement time selection and opens the same dialog. After Separate, the clip splits at selection edges and only selected audio is processed. Exact boundary rounding, overlapping clips and transaction/undo behavior remain unknown.

Evidence: `STEM-B020`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-011 — Effects and automation transfer for grouped outputs

**D12/target-U.** In the documented grouped-output case, source-track audio effects are added to the Group Track rather than baked into separated audio; track automation goes to the group and clip automation/modulation to individual stem clips. This is a placement role, not a rendered equivalence or device identity/deep-copy law. Single/merged nongroup target placement is unresolved.

Evidence: `STEM-B021`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-012 — Source clip deactivation

**D12/target-U.** After stems are created, the source clip is deactivated to prevent doubled output; selecting it and pressing 0 reactivates it. Exact key focus/layout, failed-process/cancel behavior and source-file rewriting are unknown; general clip activation remains with the editing owner.

Evidence: `STEM-B022`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-013 — Browser destination and empty-Set tempo condition

**D12/target-U.** Browser-source results go to Session or Arrangement according to focus. In an empty Set with warping for samples enabled in Record, Warp & Launch settings, project tempo is updated to source audio tempo. This conditional role does not define detection, empty-Set predicate, tempo estimate, beat conversion or behavior when the conditions are false.

Evidence: `STEM-B023`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-014 — Generated file destination and format roles

**D12/target-U.** Stem files are documented under Current Project Samples/Processed/Stems. Merge also creates individual stem files along with the merged file. Output uses Record, Warp & Launch file type,44100Hz and source bit depth according to this captured chapter. Accepted source representations, names, collisions, file codec/resampling, metadata and target output values remain unverified.

Evidence: `STEM-B024`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-015 — High Quality Others dependencies

**D12/target-U.** For High Quality with Others selected, all parts are processed even if only some are requested. The example Vocals+Others adds only those two to the Set, while Drums/Bass files are stored in Stems. This gives an externally documented file/Set distinction; it does not mandate private pass structure or a completion-time relation.

Evidence: `STEM-B030`; [exact routes](#analysis-only-evidence).

### REQ-STEM-SEPARATION-U-OUTPUT — Algorithm, numerical and boundary outcomes

**U/target-U.** Classifier/model output, quality/SDR/reconstruction, stochastic behavior, Warp/time/sample boundaries, accepted formats, bit-depth/file codecs and unsupported input/output remain required unknowns.

### REQ-STEM-SEPARATION-U-PLACEMENT — Single, merged and interaction gaps

**U/target-U.** Effects/automation placement for nongroup branches, Browser source-less color, device identity/parameter bindings, multiple-source/track ordering, time-selection fragment activation and source preservation remain unknown.

### REQ-STEM-SEPARATION-U-LIFECYCLE — Lifecycle, failure and resource outcomes

**U/target-U.** Undo/redo/cancel/save, source/output loss, disk/network/build/feature availability, rate/resource limits, transport/record ordering and teardown remain required unknowns.

## Source-context questions and acceptance proposals

**STEM-U-NONGROUP:** the source says effects/track automation go to a Group Track,
but one-element/merged results have no group. Retain the grouped predicate and
leave nongroup placement unknown rather than inventing a destination. Similarly,
Browser input has no source track for the source-track color relation.

**STEM-U-REGION:** start/end and warped-loop prose gives no inclusive endpoint,
cycle count, marker-to-sample/tempo map or fragment activation rule. Separate
Stems for Time Selection's split does not specify all original-fragment state.

[29 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/cases.json)
cover15D12 source-role proposals and14operational U probes, for18requirements
(15D12/3U). Eight documentary visible-control/state roles have proposed outputs;
seven signal/timing/file and all14U cases have null documentary outputs. All29
target expected/comparison values are null, grade U and unexecuted.

## Analysis-only evidence

Official [Version12 Stem Separation](https://www.ableton.com/en/live-manual/12/stem-separation/), captureUTC
2026-10-19T22:02:16.363028+00:00, 254199bytes, SHA-256 `62235634fac7ed29ff6bf6a586e8bf0d4980890a444f20becb0eb250a6499dcf`;
[retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manual-stem-separation-2026-10-19.html).
[32 source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/source-blocks.json)
retain anchors/HTML lines; figures uninspected. The current website has no
immutable publication revision or exact12.4.3 pin. The parser is independently
pinned in dependencies.json. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/requirements.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/stem-separation/manifest-author-r1.json)
freeze only this partial analyst scope. The manual's learning model/pass/CPU/GPU
statements remain research context, not candidate architecture or measured performance.
