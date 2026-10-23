---
id: SPEC-SYNCHRONIZATION-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 3
target: Ableton Live 12 Suite 12.4.3
---

# Link, Link Audio, Tempo Follower and MIDI synchronization

This partial F-08/F-09 contract adds documented synchronization-specific controls,
source roles and interactions. The [coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/synchronization-workflows.md) owns exact
source identities and limitations. It is not a complete protocol or released contract.

**D12/target-U:** the captured current Version12 manual supports documentary
prose only. Every exact12.4.3 outcome/comparison is null/U/unexecuted, including
whether the captured Link Audio feature exists in that build. Figures were not
inspected. No peer/network/MIDI/audio/hardware/native/candidate run occurred.
Signal, tempo, transport, RNG-free phase and timing cases have null documentary
expectations/comparators as well; source prose is retained only as source_claim.

[Recording](recording-comping.md) owns arm/monitor/count-in behavior, and
[routing](routing-monitoring-latency.md) owns port roles, channel/tap and monitor
selection. This page adds only Link/external synchronization predicates.
[Clip launch](clip-launch.md) owns finite launch quantization and
[Session launch](session-launch-workflows.md) owns Follow/Legato gestures; no
network clock extension of those laws follows here. [Video](video-workflows.md)
owns movie presentation; no video/MTC conversion is implied.
[External devices](external-hardware-devices.md) own Hardware Latency; Sync Delay
is a separate documented synchronization control without a calibration result.
Max API, controller/Push protocols and general preferences remain separate open scopes.

R2 adopts nine independently reviewed retained-source audit proposals as a
partial successor. [Audit adoption](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/audit-adoption-r2.json)
records the exact routes. A new source-only continuity clause does not broaden
membership indicators into synchronization proof. Existing hidden-Follow law
remains in012; its refined case now requires genuine running processing first.

R3 adds only two reviewed Hardware Resync roles, preserving every R2 clause and
case record. [Resync source reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/resync-source-reconciliation/README.md)
and [independent source review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/resync-source-reconciliation-review.json)
retain exact output-Sync contexts and symbolic mode names/order. They supply no
byte codec, total event count, schedule, correction algorithm or actual hardware
result. A shared Control Bar button does not establish per-port/all-port fanout;
Don’t Resync concerns resync messages, not ordinary Clock suppression.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/fixtures-r2.json).
Explicitly establish usable compatible sources and nonzero active paths before
negative/absence trials. Hidden Follow requires independently genuine active
Follower interpretation before hiding; an active input or lit button alone is
insufficient. Initial Link visibility requires known preference provenance,
not assumed factory/reset state. No future action is a result or authorization.

### REQ-SYNC-WORKFLOW-001 — Network session entry

**D12/target-U.** With peers on the same wired or wireless network, enabling Link automatically starts or joins a Link session. The toggle shows the peer count. Discovery, membership ordering, network interface selection and count refresh deadlines are unknown.

Evidence: `SYNC-B019`, `SYNC-B020`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-002 — Peer tempo ownership

**D12/target-U.** The first participant supplies initial tempo; any peer may change tempo, and the source describes the last participant making a simultaneous change as setting tempo. Peer tempo changes override Set tempo automation. No distributed causal order, convergence deadline or tempo-ramp law is specified.

Evidence: `SYNC-B022`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-003 — Independent transport and launch phase

**D12/target-U.** Peers may start/stop independently. With another connected peer and Live stopped, Arrangement Position shows global-launch-quantization progress; playback waits for progress completion. Beat/phase synchronization is a documented role, without clock, scheduler, rounding or jitter tolerance.

Evidence: `SYNC-B004`, `SYNC-B005`, `SYNC-B021`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-004 — Optional shared start and stop

**D12/target-U.** Start Stop Sync shares transport commands only with peers that also enable that option. The independent-transport role otherwise remains. Quantization of shared commands, mixed peer races and command delivery guarantees are unknown.

Evidence: `SYNC-B005`, `SYNC-B011`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-005 — Link settings entry points

**D12/target-U.** The dedicated Link Settings tab configures Link/Link Audio. The chapter describes the Control Bar Link toggle as displayed by default; this is documentary initial-visibility context, not an exact-build constructor, factory/reset, prior-preference or migration observation. Show Link Toggle can hide it; its adjacent menu switches Link/Audio features, lists connected Audio-enabled peers and offers Configure Link.

Evidence: `SYNC-B008`, `SYNC-B009`, `SYNC-B010`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-006 — Audio enable and advertised name

**D12/target-U.** Link Audio requires Link enabled; streaming peers must enable both Link and Audio. Name supplies the name shown to other peers. Name encoding, validation, collisions, persistence and legacy-peer capability are unknown.

Evidence: `SYNC-B013`, `SYNC-B014`, `SYNC-B026`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-007 — Incoming latency and peer display

**D12/target-U.** Latency adjusts incoming audio input latency; each Link Audio peer entry displays status and buffered amount, updated when latency is adjusted. Units, range, precision and exact buffer/sample relation are unknown. This display does not prescribe private buffering architecture.

Evidence: `SYNC-B015`, `SYNC-B017`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-008 — Sync to incoming audio

**D12/target-U.** Sync to Incoming Audio aligns monitored Link Audio with Live audio/clips by delaying Live playback by the specified latency amount. The manual says only one participant should enable this option for Link Audio to work. It does not give a measured delay law, topology failure policy or enforcement UI.

Evidence: `SYNC-B016`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-009 — Peer and source-track input routing

**D12/target-U.** An audio track selects a Link Audio peer through Input Type and a source track through Input Channel. Monitoring/record arming gates remain with SPEC-RECORDING-COMPING and general routing with SPEC-ROUTING-MONITORING-LATENCY; this adds the Link source prerequisite only.

Evidence: `SYNC-B026`, `SYNC-B027`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-010 — Audio output and peer capabilities

**D12/target-U.** Tracks with audio output may stream to peers. The manual describes Live and Push as send/receive capable, while other applications/devices may send only. This is not an interoperability matrix, arbitrary-peer capability promise or proof of any particular Push firmware.

Evidence: `SYNC-B028`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-011 — Tempo Follower source

**D12/target-U.** Tempo Follower analyzes incoming audio and interprets tempo. Its Ext. In channel is selected in Tempo & MIDI Settings. Clear rhythm is an optimization statement, not a rejection rule for other audio. No detector algorithm, acquisition time, supported tempo range or tracking error is established.

Evidence: `SYNC-B031`, `SYNC-B033`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-012 — Follower visibility and missing channel

**D12/target-U.** Show Tempo Follower Toggle exposes Follow, described alongside other tempo-related parameters at the left of the Control Bar. This textual placement context gives no pixel geometry or all-window-layout guarantee. Activating Follow enables listening; Tempo Follower does not run while Follow is hidden. If its configured input device channel cannot be connected, the feature is disabled and Follow appears grayed out.

Evidence: `SYNC-B034`, `SYNC-B035`, `SYNC-B036`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-013 — Follower and external sync exclusion

**D12/target-U.** Tempo Follower and External Sync are mutually exclusive; EXT is disabled while Follower is active. Live may still send MIDI clock while Follower is enabled, but cannot receive it. Other mixed-mode transitions, precedence and state restoration are unknown.

Evidence: `SYNC-B037`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-014 — Link with external tempo input

**D12/target-U.** Link can operate alongside Tempo Follower or MIDI synchronization and uses the external-input tempo for the Link session in either case. This does not define arbitration among simultaneous incoming sources or conflicts with peer tempo commands.

Evidence: `SYNC-B006`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-015 — MIDI Clock roles

**D12/target-U.** MIDI Clock provides tempo-dependent ticks and song-position messages. Changing the sync host tempo is described as causing the receiving device to follow the change; Live can act as sender/sync host or receiver/device. No byte encoding, tick count, filtering, MIDI transport command sequence, numerical tracking/convergence or timestamp law is established.

Evidence: `SYNC-B039`, `SYNC-B040`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-016 — MIDI Timecode receiver role

**D12/target-U.** MTC conveys seconds/frames, interpreted as Arrangement position; it supplies no meter information or tempo-change tracking, so tempo must be set manually. Live is an MTC receiver, not an MTC sync host. No wire decoder or frame-to-position arithmetic is supplied.

Evidence: `SYNC-B041`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-017 — Clock send setup and lower indicator

**D12/target-U.** Enable the connected sequencer as a sync destination in Tempo & MIDI Settings and configure it to receive MIDI sync. The lower LED beside EXT flashes while Live sends sync messages. Indicator activity alone proves neither receiving-device synchronization nor usable signal timing.

Evidence: `SYNC-B043`, `SYNC-B044`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-018 — External source setup and upper indicator

**D12/target-U.** After enabling an external sync source, EXT appears; its button or Options External Sync command activates sync. The upper LED flashes for usable incoming sync. General port role selection stays in the routing owner; no detector acceptance grammar or indicator refresh deadline is specified.

Evidence: `SYNC-B046`, `SYNC-B047`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-019 — Song position and looping

**D12/target-U.** With external MIDI sync, accepted song position pointers may move Live to the host song position. With Control Bar Loop enabled, pointers are described as wrapped into loop length. Exact modulus, origin, negative values, bounds and message scheduling remain unknown.

Evidence: `SYNC-B048`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-020 — Per-device Timecode controls

**D12/target-U.** Selecting a MIDI device in Tempo & MIDI Settings MIDI Ports exposes its Timecode settings. Rate and Offset are relevant only when MIDI Sync Type is MIDI Timecode. Availability wording does not establish disabled-vs-hidden presentation or cross-device persistence.

Evidence: `SYNC-B050`, `SYNC-B051`, `SYNC-B052`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-021 — Timecode rate and display format

**D12/target-U.** Timecode Rate selects incoming Timecode type; SMPTE All auto-detects incoming format. The source says usual SMPTE rates without enumerating them. Arrangement display format is separately selected in Options Time Ruler Format. No exact supported rate set, drop-frame law or detection tolerance follows.

Evidence: `SYNC-B051`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-022 — Timecode offset

**D12/target-U.** MTC Offset supplies a SMPTE offset interpreted as Arrangement start time when MTC is the selected sync type. Accepted text grammar, sign, range, subframes, conversion and persistence remain unknown.

Evidence: `SYNC-B052`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-023 — Per-device Sync Delay

**D12/target-U.** Selecting a MIDI device exposes its Sync Delay control, which delays Live's internal time base relative to the sync signal. The chapter suggests aligning separately audible percussive patterns by listening. No range, sign law, sample precision, jitter tolerance or calibration result is supplied.

Evidence: `SYNC-B054`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-024 — Link recording count-in boundary

**D12/target-U.** The metronome recording count-in cannot be used while Link is enabled. This is an additional synchronization precondition on the recording owner, not a replacement for its other record/count-in behavior or an assertion about ordinary metronome playback.

Evidence: `SYNC-B023`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-025 — Remaining-peer continuity on participant join or leave

**D12/target-U.** The manual describes participants joining or leaving a Link session at any time without interrupting synchronization between other remaining peers. This source continuity role supplies no discovery or membership order, leader election, wire protocol, phase/audio/jitter tolerance, convergence or interruption deadline. Exact-target and arbitrary-peer compatibility remain unknown.

Evidence: `SYNC-B005`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-026 — Hardware Resync configuration and command

**D12/target-U.** For a MIDI output with Sync enabled, the triangle next to the port name opens additional options. Hardware Resync selects a resync behavior when Resync External Hardware is enabled; when enabled, the Resync External Hardware button appears in the Control Bar and can be used to send resync messages to external gear. Drift during playback is a documented useful context, not an exclusive eligibility condition or a correction guarantee. The shared button versus per-port fanout and exact option-enable location beyond the named context remain unknown.

Evidence: `routing:B038`, `routing:B041`, `routing:B042`; [additional source](#resync-source-and-preserved-history).

### REQ-SYNC-WORKFLOW-027 — Hardware Resync symbolic mode roles

**D12/target-U.** The manual describes Stop and Start as the default resync behavior: a MIDI Clock Stop event followed by a MIDI Clock Start event. Start Only sends just the MIDI Clock Start resync event; Don’t Resync sends no resync messages. These symbolic source roles supply no byte encoding, total event count, spacing, timestamp, drift/phase correction, convergence or successful-device guarantee. Documentary default is not an exact-build constructor/reset/migration observation. Don’t Resync does not establish suppression of ordinary MIDI Clock traffic; per-output/all-output fanout and interactions with tempo, preroll, transport, Clock Type or Sync Delay remain unknown.

Evidence: `routing:B043`; [additional source](#resync-source-and-preserved-history).

### REQ-SYNC-WORKFLOW-U-PROTOCOL — Protocol, signal and numerical outcomes

**U/target-U.** Link discovery/clock/audio transport, membership/conflict protocol, MIDI Clock/MTC byte codecs, tempo/position/offset/wrap arithmetic, detector behavior and audio/numerical calibration remain unknown.

### REQ-SYNC-WORKFLOW-U-LIFECYCLE — State, persistence and failure lifecycle

**U/target-U.** Undo/cancel/configuration persistence, invalid or unavailable peers/ports, transport/source arbitration, reconnection, resource limits and teardown remain required unknowns.

## Finite acceptance proposals

[Current R3 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements-r3.json)
and [current R3 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases-r3.json)
retain all27 R2 requirements and37 R2 case records verbatim, adding two clauses,
one visible-control proposal, three separate accepted-mode proposals and one
explicit U lifecycle proposal. There are29 requirements (27D12/2U),42 cases,
nine visible documentary proposals and33 null documentary proposals. All actual
expected/comparison fields remain null/U/unexecuted. Every Resync message/timing,
signal, numeric and operational outcome/comparator is null. Mode prose is only
source_claim; no encoded events, count, spacing, phase or successful correction
oracle follows. Existing running-Follower-before-hide and third-peer continuity
positive guards remain unchanged. Future no-resync/disabled histories require
separately genuine usable Clock/receiver synchronization and identifiable
nonzero unmuted output, including a known positive resync-capable baseline for
Don’t Resync. Missing feature, receiver or failed baseline stays U.

## Analysis-only evidence

Official [Version12 synchronization chapter](https://www.ableton.com/en/live-manual/12/synchronizing-with-link-tempo-follower-and-midi/), captured
2026-10-19T21:48:54.932595+00:00, 261580bytes, SHA-256 `55dcef3b8171e721c641ab69476a075db8c3c8893055914538f9e4eb801d00ac`;
[exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manual-sync-2026-10-19.html).
[54 source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-blocks.json)
retain anchors/HTML lines; figures and image glyphs were not inspected.
[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements-r2.json),
[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r2.json)
and exact parser pin in dependencies.json freeze the reviewable partial packet.
The current manual is not immutable12.4.3 evidence. There is no claimed wire
format, detector model, clock convergence, latency/jitter tolerance, supported
rate enumeration, complete platform matrix or full device interoperability.

The [original R1 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/archive-r1/manifest-author-r1.json)
and all original26/36 catalog bytes remain unchanged. The current
[read-only R2 checker](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/validate-r2.py)
checks source identities, exact deltas, browser IDs and explicit historical pin
resolutions; it establishes no compatibility result.

## Resync source and preserved history

The additional official [Routing Sync subsection](https://www.ableton.com/en/live-manual/12/routing-and-i-o/#sync)
is retained at its original [full HTML path](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-routing-and-i-o-2026-10-19.html).
Its exact capture identity, direct paragraph anchors (null), actual heading
ancestry, source catalogs and locators are in [R3 sources](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-r3.json).
No recapture occurred. Preroll, tempo/transport transitions, Sync Delay/Clock Type
interactions, device compatibility and lifecycle outcomes remain unknown.
The published default is documentary context, not target constructor/reset proof.

All48 existing R2-tree files remain exact in place, including old catalogs,
snapshots, failed-preflight evidence, seal and validation/freeze records; no full
archive was added. [Canonical consumer inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/canonical-consumers-r3.json)
discloses four R2 self-history rows and an unaffected as-of Warp context. Older
checkers expecting live R2 canonicals are historical; exact spec-r2/research-r2
snapshots remain available. Existing four R1 routes remain unchanged. Root owns
combined historical replay/shared integration; consumers/tools were not edited.
[R3 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/delta-r3.json),
[read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/validate-r3.py)
and [R3 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r3.json)
bind this partial successor; independent review remains pending.
