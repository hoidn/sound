---
id: SPEC-BOUNCE-FREEZE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Version 12 documentation with target applicability unknown
---

# Bounce, Freeze and Flatten workflows

## Scope and evidence boundary

This partial F-07/FEAT-RENDER analyst contract owns Bounce Track in Place,
Bounce to New Track, their group variants, Paste Bounced Audio and track
Freeze/Unfreeze workflow distinctions. Flatten remains an explicit version gap.
[Research](../research/bounce-freeze-workflows.md) distinguishes retained current
Live 12 behavior from Live 11 predecessor context. These are public manual
observations and proposed acceptance cases, not original execution or a release.

**D12** means documented in the retained current Version 12 manual captured
2026-10-19. Every D12 clause has exact **12.4.3 applicability U**, including
command names, shortcuts, availability and defaults. **U** means insufficient
behavioral evidence. Live 11 Flatten text is context only, never a target law.
All cases have target `expected`/`comparison` null, grade U and `executed:false`.
Signal and wholly unknown case documentary oracles are null too. No numeric
render, codec, resampling, tail, latency, scheduling or comparison tolerance is
inferred from qualitative manual wording or existing finite render fixtures.

## Existing owners

- [Arrangement editing](arrangement-editing.md), especially its consolidation
  requirements, owns generic selection/edit semantics and consolidation before
  effects/mixer. Bounce is a distinct command with different signal roles.
  [Clip View](clip-view-workflows.md), [Session](session-view-workflows.md),
  [launch](clip-launch.md) and [recording](recording-comping.md) retain ordinary
  clip, scene, take, recording and launch semantics. This page adds only the
  expressly documented availability of those operations while frozen.
- [Routing/monitoring](routing-monitoring-latency.md), [mix graph](mix-graph.md),
  [mixer values](mixer-values.md), [automation](automation-envelopes.md),
  [transport](transport-state.md) and [playback](playback-core.md) retain their
  finite controls, coefficients, envelope and scheduling contracts. A documented
  bounce source stage does not extend those finite contracts or define graph
  implementation, compensation arithmetic or automation transfer.
- [Audio/video export](audio-video-export.md) owns generic export controls,
  encoding, render ranges, Render as Loop, real-time waiting/restart/cancel
  options and external-device export classification. Freeze's documented
  real-time hardware predicate is stated here; process options are referenced
  there. Export cleanup laws do not silently apply to bounce/freeze.
- [Projects/media](project-media-workflows.md), [media files](media-file-workflows.md)
  and [Set structure](live-set-structure.md) retain save/collect/repair, cache,
  formats and saved-state ownership. Generated path roles below do not supply
  a file codec, ALS representation, relocation rule or filesystem transaction.
- [Racks](device-racks.md), [plug-in hosting](plugin-hosting.md) and
  [external hardware devices](external-hardware-devices.md) own devices, ports,
  chains, hardware gain/return and Hardware Latency. Track Freeze is distinct
  from Max for Live device freezing; neither supplies the other's behavior.

## Preconditions and observables

Use the future scenario definitions in [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/fixtures.json).
They do not include actual ALS/audio/MIDI/generated samples, original results
or accepted hardware/driver/device configurations. Record exact target context,
view, selected clips/time, track eligibility, source references, Project and
Temporary Folder before each operation. Tracks are shared between views, while
source playback ownership remains with its existing owner. Fresh editable Set
state is a prerequisite, not a guessed product default.

Audio observations require independently nonempty eligible sources, enabled
relevant processing, admitted nonzero amount/send/gain and separately nonmuted
wet return/output baselines. Establish each receiver's actual Monitor/arm/clip
state. Confirm direct/dry, group, return and Main contributions before isolating
or excluding paths. A zero send, silent instrument, absent external port, muted
return or unsupported command cannot establish a negative/no-effect result.
A failed positive-path gate remains inconclusive. Meter or file presence alone
cannot prove that processing was committed correctly.

Track/clip/device membership, names/colors, copied mixer settings, mute state,
command availability, frozen/editable status, visible tail clips, generated
references and source audio are separate observations. Numerical waveform,
clock/latency, file bytes and lifecycle outcomes remain open. The full compound
requirement is not closed by one visible-control case; each named action branch
needs its own retained result. No case in this draft closes even target UI parity.

## Requirements

### REQ-BF-001 — Bounce Track in Place

**D12/target-U.** Bounce Track in Place, from a track title-bar or clip context menu, creates a new audio track replacing the source track.

Evidence: [bounce:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-002 — Bounce to New Track

**D12/target-U.** Bounce to New Track, from a clip/selection context menu or Ctrl+B (Windows)/Cmd+B (macOS), creates new audio clips on a separate track and mutes the source clips or selection.

Evidence: [bounce:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-003 — Individual-track signal stage

**D12/target-U.** Individual-track bouncing is post-FX and pre-mixer: device processing is included in bounced audio, while volume, pan and sends are excluded from the audio commit. No numerical or automation-transfer law follows.

Evidence: [bounce:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-004 — Copied mixer state and removed devices

**D12/target-U.** Individual-track bouncing preserves the source mixer adjustments in the new track settings and does not retain the source processing devices on the bounced track.

Evidence: [bounce:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-005 — Multiple Arrangement tracks

**D12/target-U.** For a time selection spanning multiple Arrangement tracks, Bounce to New Track creates a separate audio track for every track on which a clip is selected. Empty-track handling beyond that predicate is unknown.

Evidence: [bounce:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-006 — In-place cross-view scope

**D12/target-U.** Bounce Track in Place replaces the shared track in both views and bounces both its Arrangement and Session clips, even when invoked in one view.

Evidence: [bounce:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json), [bounce:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-007 — New-track cross-view scope

**D12/target-U.** Bounce to New Track creates the shared new track in both views but bounces only selected clips in the invoking view; the documented Session example leaves the new Arrangement track empty.

Evidence: [bounce:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json), [bounce:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-008 — Bounce names and color

**D12/target-U.** Created tracks/clips inherit the source name with (Bounce) appended; an unnamed source clip produces a clip named (Bounce). The new track inherits source track color. Collision, repeated-suffix and Unicode rules are unknown.

Evidence: [bounce:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-009 — Bounce project location

**D12/target-U.** Bounced audio files are stored in the Current Project under Samples/Processed/Bounce. Unsaved-project location, filenames, file count, format and subsequent collection are not established by this statement.

Evidence: [bounce:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

Existing owners: [project-media-workflows](project-media-workflows.md).

### REQ-BF-010 — Bounce Group in Place

**D12/target-U.** Bounce Group in Place creates a new audio track replacing the whole Group Track. Entry points are the group title-bar context menu, Session group-slot context menu and Arrangement group main-lane context menu.

Evidence: [bounce:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json), [bounce:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-011 — Bounce Group to New Track

**D12/target-U.** Bounce Group to New Track commits selected clips or a time selection within the group to a separate track and mutes the source clips/selection. Entry points are Session group-slot or Arrangement group main-lane context menu and Ctrl+B (Windows)/Cmd+B (macOS).

Evidence: [bounce:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-012 — Group signal stage

**D12/target-U.** Group bouncing is post-mixer, unlike individual-track bouncing. The documented signal is processed from Main output, including effects and sends used inside the group while excluding processing on Main. This does not define arbitrary graph summing or a calibrated waveform.

Evidence: [bounce:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

Existing owners: [routing-monitoring-latency](routing-monitoring-latency.md), [mix-graph](mix-graph.md).

### REQ-BF-013 — Group external destinations

**D12/target-U.** Tracks routed outside the Group Track are excluded from its bounce; this may produce silence. Their exclusion does not prove an all-silent group result when other active contributions remain.

Evidence: [bounce:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-014 — Group return prerequisite

**D12/target-U.** A return in the group signal path is included in the group bounce only if its final output reaches Main. Other routing combinations and feedback are unknown.

Evidence: [bounce:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-015 — Paste uses current source state

**D12/target-U.** Paste Bounced Audio bounces copied source material in its current state at paste time, allowing source changes and repeated paste without selecting/copying that source again.

Evidence: [bounce:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-016 — Copy selection for bounced paste

**D12/target-U.** The documented copy sources are clips within a single Session track, Arrangement clips or a time selection, and a time selection in a group main lane in Arrangement. Copy or Ctrl+C (Windows)/Cmd+C (macOS) supplies the copied source.

Evidence: [bounce:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-017 — Bounced-paste destinations

**D12/target-U.** Paste Bounced Audio is available through a track main-lane context menu or Ctrl+Alt+V (Windows)/Cmd+Opt+V (macOS) for an audio track, an empty MIDI track or a take lane. The copied material is bounced/pasted; a MIDI destination is converted to audio. Other destination eligibility is unknown.

Evidence: [bounce:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

Existing owners: [recording-comping](recording-comping.md).

### REQ-BF-018 — Deleted copied source

**D12/target-U.** Deleting the copied source material makes Paste Bounced Audio unavailable until new material is copied. Partial source deletion, undo and foreign clipboard behavior are unknown.

Evidence: [bounce:B021](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json).

### REQ-BF-019 — Freeze command entry points

**D12/target-U.** Freeze Track is available through Edit and track/clip context menus; the documented shortcut for a selected track is Ctrl+Alt+Shift+F (Windows)/Cmd+Option+Shift+F (macOS).

Evidence: [freeze12:B003](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-020 — Freeze track eligibility

**D12/target-U.** Freeze applies to tracks holding clips. Group, return and Main tracks cannot be frozen. Bounce Group is a separate operation, not an exception to Freeze eligibility. Other empty/frozen/recording-track cases remain unknown.

Evidence: [freeze12:B004](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json), [freeze12:B007](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-021 — Frozen clip playback

**D12/target-U.** Freeze creates a sample file for each Session and Arrangement clip on the selected track, and those clips play frozen samples in place of recalculating device and clip processing. File layout is documentary context, not a prescribed implementation architecture or sample oracle.

Evidence: [freeze12:B002](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-022 — Frozen settings and unfreeze

**D12/target-U.** While frozen, device and clip settings cannot be adjusted in the frozen Device/Clip View areas. Unfreeze Track is available from Edit or the track context menu to permit settings changes again. The expressly listed editing exceptions below remain available.

Evidence: [freeze12:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json), [freeze12:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-023 — Frozen launch and mixer controls

**D12/target-U.** Frozen clips remain launchable and volume, pan and sends remain available. This documents control availability, not unchanged sound or playback scheduling.

Evidence: [freeze12:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [clip-launch](clip-launch.md), [mixer-values](mixer-values.md).

### REQ-BF-024 — Frozen clip editing availability

**D12/target-U.** Cut, copy, paste, duplicate and trim remain available on frozen clips. Their general edits and transaction semantics retain their existing owners.

Evidence: [freeze12:B009](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [arrangement-editing](arrangement-editing.md), [clip-view-workflows](clip-view-workflows.md).

### REQ-BF-025 — Frozen mixer automation availability

**D12/target-U.** Drawing/editing mixer automation and mixer clip envelopes remains available on frozen tracks. Envelope values, event scheduling and audio outcomes are separate contracts.

Evidence: [freeze12:B010](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [automation-envelopes](automation-envelopes.md).

### REQ-BF-026 — Other frozen workflow availability

**D12/target-U.** Frozen tracks permit consolidation, recording Session launches into Arrangement, and creating/moving/duplicating Session scenes. Only this frozen-state eligibility is owned here; each operation retains its existing semantics.

Evidence: [freeze12:B011](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json), [freeze12:B012](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json), [freeze12:B013](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [arrangement-editing](arrangement-editing.md), [recording-comping](recording-comping.md), [session-view-workflows](session-view-workflows.md).

### REQ-BF-027 — Frozen MIDI to audio drag

**D12/target-U.** Frozen MIDI clips can be dragged into audio tracks. Exact audio content, transferred envelopes, target placement and resulting source identity are unknown here.

Evidence: [freeze12:B014](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-028 — Edits across freeze and unfreeze

**D12/target-U.** With time-based effects, edits while frozen can sound different after unfreezing because live processing responds to the edited source again. This is a documented caveat, not a promise that every edit must change sound or a numeric difference threshold.

Evidence: [freeze12:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-029 — Arrangement frozen tails

**D12/target-U.** Relevant material beyond clip lengths, such as effect tails, plays while frozen and is represented by adjacent crosshatched temporary clips; these temporary tail clips disappear on unfreeze. Selecting both pieces when moving is advice, not automatic move-linkage. Tail length, cutoff, samples and clip-boundary ownership are unknown.

Evidence: [freeze12:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-030 — Session frozen loop extent

**D12/target-U.** A frozen Session sample contains two loop cycles. Longer unlinked clip envelopes may differ after the second cycle; no universal audible difference or sample-rounded boundary is promised.

Evidence: [freeze12:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-031 — Frozen clip drop-area track

**D12/target-U.** Dragging a frozen clip to a Session or Arrangement drop area creates a new frozen track containing it. A partially selected Arrangement clip produces only that selected portion in the new frozen track.

Evidence: [freeze12:B018](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-032 — Freeze project location

**D12/target-U.** Freeze samples are stored in Current Project under Samples/Processed/Freeze. Names, codec, byte identity and reuse/collection rules are unknown.

Evidence: [freeze12:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [project-media-workflows](project-media-workflows.md).

### REQ-BF-033 — Unsaved Freeze location

**D12/target-U.** For a Set not yet saved, the Freeze sample folder is specified by Temporary Folder. Later relocation on save is not established here.

Evidence: [freeze12:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [project-media-workflows](project-media-workflows.md).

### REQ-BF-034 — Hardware Freeze mode

**D12/target-U.** A track containing External Audio Effect or External Instrument routed to hardware is frozen in real time when detected as requiring it. Real-time process controls are referenced to the export owner; no hardware acceptance, deadline, calibration or numeric latency law follows.

Evidence: [freeze12:B005](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

Existing owners: [audio-video-export](audio-video-export.md), [external-hardware-devices](external-hardware-devices.md).

### REQ-BF-035 — External-device unfreeze files

**D12/target-U.** Freeze files for a track containing External Instrument or External Audio Effect are discarded on unfreeze. This is not a broad cleanup, rollback or unrelated-file deletion guarantee.

Evidence: [freeze12:B019](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-036 — Frozen playback with unavailable devices

**D12/target-U.** The documented sharing use case permits a Set to play frozen tracks on a computer lacking the devices used by those tracks. Required frozen samples must be present; this does not prove unfreeze works without devices or missing-sample recovery.

Evidence: [freeze12:B020](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-U-FLATTEN — Flatten version boundary

**U/target-U.** Exact-12.4.3 availability and outcomes of Flatten and Freeze and Flatten Track are unknown. The current Live 12 Bounce text describes their supersession; the retained Live 11 Flatten description is predecessor context only and cannot supply a target law.

Evidence: [bounce:B006](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json), [freeze11:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze11-blocks.json).

### REQ-BF-U-SIGNAL — Audio and automation commit details

**U/target-U.** Rendered samples, inclusion/transfer of specific automation/envelopes, clip processing, tails/ranges, source-tap scheduling, mixer coefficients, codec/rate/resampling/dither/normalization, numerical latency and comparison tolerances remain unknown beyond the documentary roles above.

Evidence: [bounce:B008](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json), [bounce:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce-blocks.json), [freeze12:B015](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json), [freeze12:B016](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json), [freeze12:B017](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12-blocks.json).

### REQ-BF-U-BOUNDARY — Unspecified eligibility and ranges

**U/target-U.** Empty or zero-length selections, gaps/endpoints, stopped/playing/recording/armed/frozen input, mixed selections, nested groups, multiple return paths and unsupported paste destinations require evidence. Do not infer refusal, silence or repair from absent documentation.

Evidence: no supported outcome retained; ungraded obligation.

### REQ-BF-U-STATE — State and transaction lifecycle

**U/target-U.** Save/reopen, reference migration, undo/redo grouping, cancellation, automation ownership, transport/rate changes, engine restart and teardown outcomes are unknown for each bounce/freeze/unfreeze/legacy-flatten operation.

Evidence: no supported outcome retained; ungraded obligation.

Existing owners: [project-media-workflows](project-media-workflows.md), [transport-state](transport-state.md).

### REQ-BF-U-ERROR — Failure and source loss

**U/target-U.** Missing inputs/devices/freeze files, source removal during processing, invalid controls, read-only/full/unavailable destinations, interrupted hardware, concurrent writes and recovery have no established diagnostics, cleanup or transaction oracle here.

Evidence: no supported outcome retained; ungraded obligation.

## Acceptance cases

All 77 cases are proposed and unexecuted. Forty-two have visible documentary
control/state/eligibility/reference-role predicates only; 35 have null documentary
oracles. All 77 target oracles remain null/U. The complete actions, preconditions,
evidence and comparator fields are retained in [cases.json](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/cases.json).
The table is an index, not a claim that every branch is exercised or every
applicable lifecycle case is known. Group and individual bounce, paste, Freeze,
Unfreeze and any actually offered legacy Flatten need separate lifecycle trials.

| Case | Requirement | Kind | Action focus | Documentary criterion |
| --- | --- | --- | --- | --- |
| BF-001 | REQ-BF-001 | state | Individual in-place replacement | visible named state only |
| BF-002 | REQ-BF-002 | state | New-track selection and source mute | visible named state only |
| BF-003 | REQ-BF-003 | signal | Individual source stage | U / null |
| BF-004 | REQ-BF-004 | state | Mixer copying and device disposition | visible named state only |
| BF-005 | REQ-BF-005 | state | Multi-track Arrangement selection | visible named state only |
| BF-006 | REQ-BF-006 | state | In-place both views | visible named state only |
| BF-007 | REQ-BF-007 | state | New-track invoking view | visible named state only |
| BF-008 | REQ-BF-008 | state | Named bounce suffix | visible named state only |
| BF-009 | REQ-BF-008 | boundary | Unnamed source clip | visible named state only |
| BF-010 | REQ-BF-008 | state | Track color inheritance | visible named state only |
| BF-011 | REQ-BF-009 | state | Saved Bounce location | visible named state only |
| BF-012 | REQ-BF-010 | state | Whole-group replacement | visible named state only |
| BF-013 | REQ-BF-011 | state | Group new-track and mute | visible named state only |
| BF-014 | REQ-BF-012 | signal | Group post-mixer and Main exclusion | U / null |
| BF-015 | REQ-BF-013 | signal | Child routed outside group | U / null |
| BF-016 | REQ-BF-014 | signal | Return final output condition | U / null |
| BF-017 | REQ-BF-015 | signal | Paste after source processing change | U / null |
| BF-018 | REQ-BF-016 | control | Single Session-track copy source | visible named state only |
| BF-019 | REQ-BF-016 | control | Arrangement clips and time copy | visible named state only |
| BF-020 | REQ-BF-016 | control | Group main-lane copy | visible named state only |
| BF-021 | REQ-BF-017 | state | Audio paste destination | visible named state only |
| BF-022 | REQ-BF-017 | state | Empty MIDI conversion | visible named state only |
| BF-023 | REQ-BF-017 | state | Take-lane destination | visible named state only |
| BF-024 | REQ-BF-018 | boundary | Deleted copied source disables paste | visible named state only |
| BF-025 | REQ-BF-019 | control | Freeze entry points | visible named state only |
| BF-026 | REQ-BF-020 | boundary | Group is not Freeze eligible | visible named state only |
| BF-027 | REQ-BF-020 | boundary | Return is not Freeze eligible | visible named state only |
| BF-028 | REQ-BF-020 | boundary | Main is not Freeze eligible | visible named state only |
| BF-029 | REQ-BF-021 | signal | Frozen sample playback role | U / null |
| BF-030 | REQ-BF-021 | state | Per-clip Freeze file roles | visible named state only |
| BF-031 | REQ-BF-022 | control | Frozen settings exclusion | visible named state only |
| BF-032 | REQ-BF-022 | control | Unfreeze allows settings | visible named state only |
| BF-033 | REQ-BF-023 | control | Frozen launch available | visible named state only |
| BF-034 | REQ-BF-023 | control | Frozen mixer available | visible named state only |
| BF-035 | REQ-BF-024 | control | Frozen clip edit variants | visible named state only |
| BF-036 | REQ-BF-025 | control | Mixer automation and clip envelope availability | visible named state only |
| BF-037 | REQ-BF-026 | control | Frozen Consolidate availability | visible named state only |
| BF-038 | REQ-BF-026 | control | Record frozen Session launches availability | visible named state only |
| BF-039 | REQ-BF-026 | control | Frozen scene edits available | visible named state only |
| BF-040 | REQ-BF-027 | state | Frozen MIDI drag to audio | visible named state only |
| BF-041 | REQ-BF-028 | signal | Time-effect edit after unfreeze | U / null |
| BF-042 | REQ-BF-029 | state | Frozen tail presentation | visible named state only |
| BF-043 | REQ-BF-029 | signal | Frozen tail audio | U / null |
| BF-044 | REQ-BF-029 | state | Unfreeze removes temporary tail clips | visible named state only |
| BF-045 | REQ-BF-030 | signal | Two Session cycles and longer envelopes | U / null |
| BF-046 | REQ-BF-031 | state | Frozen drop area in each view | visible named state only |
| BF-047 | REQ-BF-031 | boundary | Partial Arrangement frozen drop | visible named state only |
| BF-048 | REQ-BF-032 | state | Saved Freeze path | visible named state only |
| BF-049 | REQ-BF-033 | boundary | Unsaved Freeze path | visible named state only |
| BF-050 | REQ-BF-034 | state | Hardware Freeze real-time mode | visible named state only |
| BF-051 | REQ-BF-034 | signal | Hardware Freeze delivered result | U / null |
| BF-052 | REQ-BF-035 | state | External-device unfreeze sample discard | visible named state only |
| BF-053 | REQ-BF-036 | signal | Missing device with retained frozen samples | U / null |
| BF-054 | REQ-BF-U-FLATTEN | boundary | Actual Flatten command/version boundary | U / null |
| BF-055 | REQ-BF-U-SIGNAL | automation | Automation inclusion versus transfer | U / null |
| BF-056 | REQ-BF-U-SIGNAL | signal | Bounce range and tail boundaries | U / null |
| BF-057 | REQ-BF-U-SIGNAL | sample-rate | Rate and render output metadata | U / null |
| BF-058 | REQ-BF-U-SIGNAL | signal | Compensation and source taps | U / null |
| BF-059 | REQ-BF-U-BOUNDARY | boundary | Empty and unselected source | U / null |
| BF-060 | REQ-BF-U-BOUNDARY | boundary | Zero selection and range endpoints | U / null |
| BF-061 | REQ-BF-U-BOUNDARY | boundary | Mixed paste and track selection | U / null |
| BF-062 | REQ-BF-U-BOUNDARY | signal | Nested group routing | U / null |
| BF-063 | REQ-BF-U-BOUNDARY | transport | Playing armed and recording states | U / null |
| BF-064 | REQ-BF-U-STATE | undo | Undo and redo transactions | U / null |
| BF-065 | REQ-BF-U-STATE | cancel | Cancellation phases | U / null |
| BF-066 | REQ-BF-U-STATE | persistence | Save reopen and relocation | U / null |
| BF-067 | REQ-BF-U-STATE | transport | Transport while processing | U / null |
| BF-068 | REQ-BF-U-STATE | automation | Automation during processing | U / null |
| BF-069 | REQ-BF-U-STATE | sample-rate | Rate change and engine restart | U / null |
| BF-070 | REQ-BF-U-STATE | teardown | Close replace Set and teardown | U / null |
| BF-071 | REQ-BF-U-ERROR | source-loss | Source removal during commit | U / null |
| BF-072 | REQ-BF-U-ERROR | source-loss | Missing frozen samples | U / null |
| BF-073 | REQ-BF-U-ERROR | recovery | Unavailable devices during processing | U / null |
| BF-074 | REQ-BF-U-ERROR | error | Destination failure and disk space | U / null |
| BF-075 | REQ-BF-U-ERROR | malformed | Malformed admitted inputs | U / null |
| BF-076 | REQ-BF-U-ERROR | source-loss | External return loss | U / null |
| BF-077 | REQ-BF-U-ERROR | recovery | Interrupted operation recovery | U / null |

## Open obligations

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns manual/build applicability. In particular, retain the current command
supersession description alongside the predecessor Flatten text; do not decide
which commands 12.4.3 offers by choosing the newer page. Bounce automation
inclusion/transfer, tails/ranges, frozen edit/recalculation output, sample format,
rate conversion, latency and missing-device/media behavior need bounded evidence.
No standalone Freeze and Flatten Track law is supplied by either retained section.

The lifecycle probes cover supported commands only through offered controls or
independently understood formats. Save/reopen, Undo/Redo, cancellation, disk and
source failure, automation/transport/rate changes, recovery and teardown remain
U. No malformed ALS/codec or fake hardware harness is invented. Generic codec,
media, recording and export gaps remain with their existing owners.

## Analyst evidence appendix

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/sources.json)
pins captures, URL/final URL, UTC capture time, major version, size and SHA256.
[Counts](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/counts.json)
and [frozen manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manifest-author-r1.json)
identify the review packet. Block records carry exact HTML line, anchor, section
and heading context; normalized line views are retained alongside immutable HTML.
Figures, linked tutorials/help, PDF bytes, native code and application execution
were not inspected for this packet.

| Source | Exact scope | Retained view |
| --- | --- | --- |
| D12-BOUNCE | §20, §20.1 individual, §20.2 groups, §20.3 paste; HTML280–408; 21 blocks | [Bounce text](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-bounce.txt) |
| D12-RESOURCES | §38.1.4 #track-freeze; HTML338–378; 20 blocks | [Current Freeze text](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze12.txt) |
| D11-RESOURCES | §33.1.4 #track-freeze; HTML336–352; 18 predecessor blocks, especially B017 Flatten | [Predecessor text](../../analysis/ableton-live-12.4.3/full-spec-v1/bounce-freeze/manual-freeze11.txt) |
| D12-MIXING | HTML630 links to resources #track-freeze; no Freeze subsection in mixing | [Existing capture](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-12-mixing-2026-10-19.html) |
