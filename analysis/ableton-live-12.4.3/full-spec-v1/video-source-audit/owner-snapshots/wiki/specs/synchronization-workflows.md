---
id: SPEC-SYNCHRONIZATION-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
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

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/fixtures.json).
Independently establish connected usable positive sources and nonzero output
before negative/failure trials. A silent source, unarmed recording, unavailable
device or LED alone cannot pass a synchronization or missing-output case.
Compound clauses remain partial until all branches and required case kinds close.

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

**D12/target-U.** The dedicated Link Settings tab configures Link/Link Audio. Show Link Toggle can hide the Control Bar toggle; its adjacent menu switches Link/Audio features, lists audio-enabled peers and offers Configure Link. The manual default visibility is not an exact-build constructor observation.

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

**D12/target-U.** Show Tempo Follower Toggle exposes Follow. Activating Follow enables listening; Tempo Follower does not run while Follow is hidden. If its configured input device channel cannot be connected, the feature is disabled and Follow appears grayed out.

Evidence: `SYNC-B034`, `SYNC-B035`, `SYNC-B036`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-013 — Follower and external sync exclusion

**D12/target-U.** Tempo Follower and External Sync are mutually exclusive; EXT is disabled while Follower is active. Live may still send MIDI clock while Follower is enabled, but cannot receive it. Other mixed-mode transitions, precedence and state restoration are unknown.

Evidence: `SYNC-B037`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-014 — Link with external tempo input

**D12/target-U.** Link can operate alongside Tempo Follower or MIDI synchronization and uses the external-input tempo for the Link session in either case. This does not define arbitration among simultaneous incoming sources or conflicts with peer tempo commands.

Evidence: `SYNC-B006`; [exact routes](#analysis-only-evidence).

### REQ-SYNC-WORKFLOW-015 — MIDI Clock roles

**D12/target-U.** MIDI Clock provides tempo-dependent ticks and song-position messages; Live can act as sender/sync host or receiver/device. This chapter does not establish byte encoding, tick counts, message filtering, transport command sequences or timestamp law.

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

### REQ-SYNC-WORKFLOW-U-PROTOCOL — Protocol, signal and numerical outcomes

**U/target-U.** Link discovery/clock/audio transport, membership/conflict protocol, MIDI Clock/MTC byte codecs, tempo/position/offset/wrap arithmetic, detector behavior and audio/numerical calibration remain unknown.

### REQ-SYNC-WORKFLOW-U-LIFECYCLE — State, persistence and failure lifecycle

**U/target-U.** Undo/cancel/configuration persistence, invalid or unavailable peers/ports, transport/source arbitration, reconnection, resource limits and teardown remain required unknowns.

## Finite acceptance proposals

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases.json)
contains24documentary source-role proposals and12operational U probes for
26requirements (24 D12/2 U). Every target expected/comparison is null/U;
all signal/timing documentary outputs are also null. No future fixture is a result.

| Case | Requirement | Kind / action |
| --- | --- | --- |
| SYNC-001 | REQ-SYNC-WORKFLOW-001 | control: Use two independently confirmed compatible peers on an isolated test network; enable Link separately and inspect membership/count, then leave and rejoin. |
| SYNC-002 | REQ-SYNC-WORKFLOW-002 | timing: Establish a working two-peer session with distinct valid tempos, then change tempo from each peer separately, with and without active Set tempo automation. Retain ordered events before a separate simultaneous-change probe. |
| SYNC-003 | REQ-SYNC-WORKFLOW-003 | timing: Confirm two peers actually exchange tempo; explicitly choose a supported non-None global launch quantum, stop Live, inspect progress and request playback at separate interior phases. |
| SYNC-004 | REQ-SYNC-WORKFLOW-004 | timing: After a paired positive baseline, test both peers enabled, then disable only the receiving peer option and repeat start/stop separately while Link remains connected. |
| SYNC-005 | REQ-SYNC-WORKFLOW-005 | control: Inspect the Link settings tab, explicitly show/hide the toggle, restore it and use Configure Link from the adjacent menu with a known connected audio peer. |
| SYNC-006 | REQ-SYNC-WORKFLOW-006 | control: With two known compatible peers and active nonzero output, explicitly enable both features, set distinct safe names, inspect remote names, then disable Audio alone and Link alone in separate copies. |
| SYNC-007 | REQ-SYNC-WORKFLOW-007 | control: With independently confirmed incoming audio, inspect peer status/buffer display and adjust accepted latency values separately, recording the offered units and settings. |
| SYNC-008 | REQ-SYNC-WORKFLOW-008 | signal: Use two known working audio peers, explicit incoming latency and independently distinguishable local/incoming pulses; enable the option on one participant only. Keep both-enabled behavior a separate unknown probe. |
| SYNC-009 | REQ-SYNC-WORKFLOW-009 | signal: With both features active at both peers and known nonzero source track, choose peer then source track. Apply the recording owner's explicit In/Auto and arm preconditions separately for monitor and record trials. |
| SYNC-010 | REQ-SYNC-WORKFLOW-010 | signal: Select two distinct known audio-output source tracks on an independently capable peer; inspect source choices and capture active positive output. Record exact peer product/build and directions independently. |
| SYNC-011 | REQ-SYNC-WORKFLOW-011 | signal: Configure an available interface channel carrying independently validated nonzero rhythmic audio, explicitly select it for Tempo Follower, and record the input before activating Follow. |
| SYNC-012 | REQ-SYNC-WORKFLOW-012 | control: Establish an available active input first; inspect Show/Follow state, hide the button and restore it. In a separate owned configuration make only that configured input unavailable and inspect disabled state. |
| SYNC-013 | REQ-SYNC-WORKFLOW-013 | timing: With working input and a separately verified usable MIDI clock transmitter/receiver, enable Follower and inspect EXT, output-clock role and incoming-clock role independently, retaining positive baselines with Follower off. |
| SYNC-014 | REQ-SYNC-WORKFLOW-014 | timing: In separate two-peer sessions first establish Follower-driven tempo, then MIDI-driven tempo with Follower off; retain external source and peer state before observing Link tempo roles. |
| SYNC-015 | REQ-SYNC-WORKFLOW-015 | timing: Use a known compatible MIDI receiver/transmitter and explicitly configure each direction in separate trials; independently retain usable message traffic before observing Live role changes. |
| SYNC-016 | REQ-SYNC-WORKFLOW-016 | timing: Use independently validated MTC source, explicitly set Live tempo and sync type, then vary source position separately from tempo. Compare with a positive MIDI Clock trial; no universal byte/timing oracle is available. |
| SYNC-017 | REQ-SYNC-WORKFLOW-017 | control: With known destination connected and selected for Sync, inspect lower indicator while retaining independently observed transmitted clock traffic and receiver baseline; then disable this destination alone. |
| SYNC-018 | REQ-SYNC-WORKFLOW-018 | control: Enable one known usable external source, activate through EXT and separately the menu command, and inspect upper indicator. Establish accepted positive traffic before an invalid/no-input trial. |
| SYNC-019 | REQ-SYNC-WORKFLOW-019 | timing: Confirm usable song-position input with Loop off, then enable a nonempty loop with explicit start/length and send interior, exterior and boundary pointers separately. Retain loop/source positions without inventing a numeric wrap oracle. |
| SYNC-020 | REQ-SYNC-WORKFLOW-020 | control: Select two independently available MIDI devices; explicitly switch each between MIDI Clock and MIDI Timecode, inspecting applicable Rate/Offset controls and recording offered choices. |
| SYNC-021 | REQ-SYNC-WORKFLOW-021 | control: With a validated MTC source at an independently recorded supported rate, select SMPTE All, then separately change Arrangement display format while retaining incoming type. Enumerate actual offered values without presupposing a rate list. |
| SYNC-022 | REQ-SYNC-WORKFLOW-022 | timing: With confirmed MTC input and selected type, enter two accepted nonzero offset values separately, retaining displayed Arrangement and source positions. Test invalid values only in the unknown case set. |
| SYNC-023 | REQ-SYNC-WORKFLOW-023 | timing: Retain two independently audible nonzero percussive patterns and usable sync; select the intended MIDI device and change accepted Sync Delay values while separately recording both outputs. Listening guidance is not a numerical comparator. |
| SYNC-024 | REQ-SYNC-WORKFLOW-024 | timing: First confirm an eligible recording setup with count-in working while Link is off. Enable Link and repeat the same recording action, retaining explicit metronome/count-in selection and arm states. |
| SYNC-U-MALFORMED | REQ-SYNC-WORKFLOW-U-PROTOCOL | malformed: After accepted positive Clock/MTC input, send independently identified malformed, incomplete, mixed-type and unsupported-rate messages separately; no acceptance grammar is assumed. |
| SYNC-U-BOUNDARY | REQ-SYNC-WORKFLOW-U-PROTOCOL | boundary: Use accepted minimum/maximum and just-outside tempo, offset, delay, loop and song-position values; retain offered bounds and response without assuming clamp/reject or modulus. |
| SYNC-U-DETECTOR | REQ-SYNC-WORKFLOW-U-PROTOCOL | detector: Use independently indexed rhythmic, variable-tempo, ambiguous and nonrhythmic nonzero inputs after a working Follower baseline; no tempo-range, acquisition or tracking tolerance exists. |
| SYNC-U-PEERS | REQ-SYNC-WORKFLOW-U-PROTOCOL | peers: After two working compatible peers, vary a third peer, same-name peers, sending-only peer capability and simultaneous tempo/transport changes in separate trials. |
| SYNC-U-AUDIO | REQ-SYNC-WORKFLOW-U-PROTOCOL | audio: After paired nonzero incoming/local audio, vary one/two Sync-to-Incoming participants, accepted latency, source channels and independently accepted audio rates; capture outputs without inventing a tolerance. |
| SYNC-U-MTC | REQ-SYNC-WORKFLOW-U-PROTOCOL | mtc: With validated incoming MTC, vary accepted format, SMPTE All, display format and offset separately, including frame-boundary positions; retain messages and visible states without arithmetic guesses. |
| SYNC-U-UNDO | REQ-SYNC-WORKFLOW-U-LIFECYCLE | undo: Change an offered sync/latency/offset/loop control and invoke Undo/Redo only where available; record command availability and actual state, not presumed undoability. |
| SYNC-U-CANCEL | REQ-SYNC-WORKFLOW-U-LIFECYCLE | cancel: Cancel an offered settings/device permission or connection dialog; observe previously active sync and partial settings. Dialog availability is itself unknown. |
| SYNC-U-PERSISTENCE | REQ-SYNC-WORKFLOW-U-LIFECYCLE | persistence: Save/reopen an owned Set and separately restart application with explicit Link/Follow/MIDI settings; inspect Set-versus-global retention and restored device identities. |
| SYNC-U-LOSS | REQ-SYNC-WORKFLOW-U-LIFECYCLE | loss: After active positive tempo and audio, disconnect only the selected peer/network, audio input or MIDI source in separate trials, then reconnect; record recovery without a deadline. |
| SYNC-U-ARBITRATION | REQ-SYNC-WORKFLOW-U-LIFECYCLE | arbitration: Switch external input types, Follow, Link, EXT and Start Stop Sync across start/stop/seek in separate reset trials; retain event order and no inferred conflict policy. |
| SYNC-U-TEARDOWN | REQ-SYNC-WORKFLOW-U-LIFECYCLE | teardown: Leave peers or close track, Set and application while sync and incoming audio are active; retain remote/local states, prompts and pending recording outcomes. |

## Analysis-only evidence

Official [Version12 synchronization chapter](https://www.ableton.com/en/live-manual/12/synchronizing-with-link-tempo-follower-and-midi/), captured
2026-10-19T21:48:54.932595+00:00, 261580bytes, SHA-256 `55dcef3b8171e721c641ab69476a075db8c3c8893055914538f9e4eb801d00ac`;
[exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manual-sync-2026-10-19.html).
[54 source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-blocks.json)
retain anchors/HTML lines; figures and image glyphs were not inspected.
[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements.json),
[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r1.json)
and exact parser pin in dependencies.json freeze the reviewable partial packet.
The current manual is not immutable12.4.3 evidence. There is no claimed wire
format, detector model, clock convergence, latency/jitter tolerance, supported
rate enumeration, complete platform matrix or full device interoperability.
