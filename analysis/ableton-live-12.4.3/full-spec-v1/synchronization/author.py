"""Author partial analyst synchronization proposals from the retained manual."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
blocks = {r['id']: r for r in json.loads((P/'source-blocks.json').read_text())}
# title, documentary scope, source blocks, future action, observable role
DATA = [
('Network session entry', 'With peers on the same wired or wireless network, enabling Link automatically starts or joins a Link session. The toggle shows the peer count. Discovery, membership ordering, network interface selection and count refresh deadlines are unknown.', [19,20], 'Use two independently confirmed compatible peers on an isolated test network; enable Link separately and inspect membership/count, then leave and rejoin.', 'control'),
('Peer tempo ownership', 'The first participant supplies initial tempo; any peer may change tempo, and the source describes the last participant making a simultaneous change as setting tempo. Peer tempo changes override Set tempo automation. No distributed causal order, convergence deadline or tempo-ramp law is specified.', [22], 'Establish a working two-peer session with distinct valid tempos, then change tempo from each peer separately, with and without active Set tempo automation. Retain ordered events before a separate simultaneous-change probe.', 'timing'),
('Independent transport and launch phase', 'Peers may start/stop independently. With another connected peer and Live stopped, Arrangement Position shows global-launch-quantization progress; playback waits for progress completion. Beat/phase synchronization is a documented role, without clock, scheduler, rounding or jitter tolerance.', [4,5,21], 'Confirm two peers actually exchange tempo; explicitly choose a supported non-None global launch quantum, stop Live, inspect progress and request playback at separate interior phases.', 'timing'),
('Optional shared start and stop', 'Start Stop Sync shares transport commands only with peers that also enable that option. The independent-transport role otherwise remains. Quantization of shared commands, mixed peer races and command delivery guarantees are unknown.', [5,11], 'After a paired positive baseline, test both peers enabled, then disable only the receiving peer option and repeat start/stop separately while Link remains connected.', 'timing'),
('Link settings entry points', 'The dedicated Link Settings tab configures Link/Link Audio. Show Link Toggle can hide the Control Bar toggle; its adjacent menu switches Link/Audio features, lists audio-enabled peers and offers Configure Link. The manual default visibility is not an exact-build constructor observation.', [8,9,10], 'Inspect the Link settings tab, explicitly show/hide the toggle, restore it and use Configure Link from the adjacent menu with a known connected audio peer.', 'control'),
('Audio enable and advertised name', 'Link Audio requires Link enabled; streaming peers must enable both Link and Audio. Name supplies the name shown to other peers. Name encoding, validation, collisions, persistence and legacy-peer capability are unknown.', [13,14,26], 'With two known compatible peers and active nonzero output, explicitly enable both features, set distinct safe names, inspect remote names, then disable Audio alone and Link alone in separate copies.', 'control'),
('Incoming latency and peer display', 'Latency adjusts incoming audio input latency; each Link Audio peer entry displays status and buffered amount, updated when latency is adjusted. Units, range, precision and exact buffer/sample relation are unknown. This display does not prescribe private buffering architecture.', [15,17], 'With independently confirmed incoming audio, inspect peer status/buffer display and adjust accepted latency values separately, recording the offered units and settings.', 'control'),
('Sync to incoming audio', 'Sync to Incoming Audio aligns monitored Link Audio with Live audio/clips by delaying Live playback by the specified latency amount. The manual says only one participant should enable this option for Link Audio to work. It does not give a measured delay law, topology failure policy or enforcement UI.', [16], 'Use two known working audio peers, explicit incoming latency and independently distinguishable local/incoming pulses; enable the option on one participant only. Keep both-enabled behavior a separate unknown probe.', 'signal'),
('Peer and source-track input routing', 'An audio track selects a Link Audio peer through Input Type and a source track through Input Channel. Monitoring/record arming gates remain with SPEC-RECORDING-COMPING and general routing with SPEC-ROUTING-MONITORING-LATENCY; this adds the Link source prerequisite only.', [26,27], 'With both features active at both peers and known nonzero source track, choose peer then source track. Apply the recording owner\'s explicit In/Auto and arm preconditions separately for monitor and record trials.', 'signal'),
('Audio output and peer capabilities', 'Tracks with audio output may stream to peers. The manual describes Live and Push as send/receive capable, while other applications/devices may send only. This is not an interoperability matrix, arbitrary-peer capability promise or proof of any particular Push firmware.', [28], 'Select two distinct known audio-output source tracks on an independently capable peer; inspect source choices and capture active positive output. Record exact peer product/build and directions independently.', 'signal'),
('Tempo Follower source', 'Tempo Follower analyzes incoming audio and interprets tempo. Its Ext. In channel is selected in Tempo & MIDI Settings. Clear rhythm is an optimization statement, not a rejection rule for other audio. No detector algorithm, acquisition time, supported tempo range or tracking error is established.', [31,33], 'Configure an available interface channel carrying independently validated nonzero rhythmic audio, explicitly select it for Tempo Follower, and record the input before activating Follow.', 'signal'),
('Follower visibility and missing channel', 'Show Tempo Follower Toggle exposes Follow. Activating Follow enables listening; Tempo Follower does not run while Follow is hidden. If its configured input device channel cannot be connected, the feature is disabled and Follow appears grayed out.', [34,35,36], 'Establish an available active input first; inspect Show/Follow state, hide the button and restore it. In a separate owned configuration make only that configured input unavailable and inspect disabled state.', 'control'),
('Follower and external sync exclusion', 'Tempo Follower and External Sync are mutually exclusive; EXT is disabled while Follower is active. Live may still send MIDI clock while Follower is enabled, but cannot receive it. Other mixed-mode transitions, precedence and state restoration are unknown.', [37], 'With working input and a separately verified usable MIDI clock transmitter/receiver, enable Follower and inspect EXT, output-clock role and incoming-clock role independently, retaining positive baselines with Follower off.', 'timing'),
('Link with external tempo input', 'Link can operate alongside Tempo Follower or MIDI synchronization and uses the external-input tempo for the Link session in either case. This does not define arbitration among simultaneous incoming sources or conflicts with peer tempo commands.', [6], 'In separate two-peer sessions first establish Follower-driven tempo, then MIDI-driven tempo with Follower off; retain external source and peer state before observing Link tempo roles.', 'timing'),
('MIDI Clock roles', 'MIDI Clock provides tempo-dependent ticks and song-position messages; Live can act as sender/sync host or receiver/device. This chapter does not establish byte encoding, tick counts, message filtering, transport command sequences or timestamp law.', [39,40], 'Use a known compatible MIDI receiver/transmitter and explicitly configure each direction in separate trials; independently retain usable message traffic before observing Live role changes.', 'timing'),
('MIDI Timecode receiver role', 'MTC conveys seconds/frames, interpreted as Arrangement position; it supplies no meter information or tempo-change tracking, so tempo must be set manually. Live is an MTC receiver, not an MTC sync host. No wire decoder or frame-to-position arithmetic is supplied.', [41], 'Use independently validated MTC source, explicitly set Live tempo and sync type, then vary source position separately from tempo. Compare with a positive MIDI Clock trial; no universal byte/timing oracle is available.', 'timing'),
('Clock send setup and lower indicator', 'Enable the connected sequencer as a sync destination in Tempo & MIDI Settings and configure it to receive MIDI sync. The lower LED beside EXT flashes while Live sends sync messages. Indicator activity alone proves neither receiving-device synchronization nor usable signal timing.', [43,44], 'With known destination connected and selected for Sync, inspect lower indicator while retaining independently observed transmitted clock traffic and receiver baseline; then disable this destination alone.', 'control'),
('External source setup and upper indicator', 'After enabling an external sync source, EXT appears; its button or Options External Sync command activates sync. The upper LED flashes for usable incoming sync. General port role selection stays in the routing owner; no detector acceptance grammar or indicator refresh deadline is specified.', [46,47], 'Enable one known usable external source, activate through EXT and separately the menu command, and inspect upper indicator. Establish accepted positive traffic before an invalid/no-input trial.', 'control'),
('Song position and looping', 'With external MIDI sync, accepted song position pointers may move Live to the host song position. With Control Bar Loop enabled, pointers are described as wrapped into loop length. Exact modulus, origin, negative values, bounds and message scheduling remain unknown.', [48], 'Confirm usable song-position input with Loop off, then enable a nonempty loop with explicit start/length and send interior, exterior and boundary pointers separately. Retain loop/source positions without inventing a numeric wrap oracle.', 'timing'),
('Per-device Timecode controls', 'Selecting a MIDI device in Tempo & MIDI Settings MIDI Ports exposes its Timecode settings. Rate and Offset are relevant only when MIDI Sync Type is MIDI Timecode. Availability wording does not establish disabled-vs-hidden presentation or cross-device persistence.', [50,51,52], 'Select two independently available MIDI devices; explicitly switch each between MIDI Clock and MIDI Timecode, inspecting applicable Rate/Offset controls and recording offered choices.', 'control'),
('Timecode rate and display format', 'Timecode Rate selects incoming Timecode type; SMPTE All auto-detects incoming format. The source says usual SMPTE rates without enumerating them. Arrangement display format is separately selected in Options Time Ruler Format. No exact supported rate set, drop-frame law or detection tolerance follows.', [51], 'With a validated MTC source at an independently recorded supported rate, select SMPTE All, then separately change Arrangement display format while retaining incoming type. Enumerate actual offered values without presupposing a rate list.', 'control'),
('Timecode offset', 'MTC Offset supplies a SMPTE offset interpreted as Arrangement start time when MTC is the selected sync type. Accepted text grammar, sign, range, subframes, conversion and persistence remain unknown.', [52], 'With confirmed MTC input and selected type, enter two accepted nonzero offset values separately, retaining displayed Arrangement and source positions. Test invalid values only in the unknown case set.', 'timing'),
('Per-device Sync Delay', 'Selecting a MIDI device exposes its Sync Delay control, which delays Live\'s internal time base relative to the sync signal. The chapter suggests aligning separately audible percussive patterns by listening. No range, sign law, sample precision, jitter tolerance or calibration result is supplied.', [54], 'Retain two independently audible nonzero percussive patterns and usable sync; select the intended MIDI device and change accepted Sync Delay values while separately recording both outputs. Listening guidance is not a numerical comparator.', 'timing'),
('Link recording count-in boundary', 'The metronome recording count-in cannot be used while Link is enabled. This is an additional synchronization precondition on the recording owner, not a replacement for its other record/count-in behavior or an assertion about ordinary metronome playback.', [23], 'First confirm an eligible recording setup with count-in working while Link is off. Enable Link and repeat the same recording action, retaining explicit metronome/count-in selection and arm states.', 'timing'),
]
reqs, cases = [], []
for i, (title, contract, refs, action, kind) in enumerate(DATA, 1):
    rid = f'REQ-SYNC-WORKFLOW-{i:03d}'
    evidence = [dict(block=f'SYNC-B{n:03d}', anchor=blocks[f'SYNC-B{n:03d}']['anchor'], html_line=blocks[f'SYNC-B{n:03d}']['html_line']) for n in refs]
    reqs.append(dict(id=rid, title=title, contract=contract, strength='D12', target_applicability='U', evidence=evidence))
    cases.append(dict(id=f'SYNC-{i:03d}', requirements=[rid], kind=kind, fixture='fixtures.json#SYNC-OWNED', setup_and_action=action, source_claim=contract, documentary_expected=contract if kind=='control' else None, documentary_comparator='Named visible control/state roles only; no clock/audio/device synchronization proof.' if kind=='control' else None, expected=None, comparison=None, target_grade='U', executed=False, evidence=evidence))
gaps = {
 'PROTOCOL': ('Protocol, signal and numerical outcomes', 'Link discovery/clock/audio transport, membership/conflict protocol, MIDI Clock/MTC byte codecs, tempo/position/offset/wrap arithmetic, detector behavior and audio/numerical calibration remain unknown.', [
 ('MALFORMED', 'After accepted positive Clock/MTC input, send independently identified malformed, incomplete, mixed-type and unsupported-rate messages separately; no acceptance grammar is assumed.'),
 ('BOUNDARY', 'Use accepted minimum/maximum and just-outside tempo, offset, delay, loop and song-position values; retain offered bounds and response without assuming clamp/reject or modulus.'),
 ('DETECTOR', 'Use independently indexed rhythmic, variable-tempo, ambiguous and nonrhythmic nonzero inputs after a working Follower baseline; no tempo-range, acquisition or tracking tolerance exists.'),
 ('PEERS', 'After two working compatible peers, vary a third peer, same-name peers, sending-only peer capability and simultaneous tempo/transport changes in separate trials.'),
 ('AUDIO', 'After paired nonzero incoming/local audio, vary one/two Sync-to-Incoming participants, accepted latency, source channels and independently accepted audio rates; capture outputs without inventing a tolerance.'),
 ('MTC', 'With validated incoming MTC, vary accepted format, SMPTE All, display format and offset separately, including frame-boundary positions; retain messages and visible states without arithmetic guesses.')]),
 'LIFECYCLE': ('State, persistence and failure lifecycle', 'Undo/cancel/configuration persistence, invalid or unavailable peers/ports, transport/source arbitration, reconnection, resource limits and teardown remain required unknowns.', [
 ('UNDO', 'Change an offered sync/latency/offset/loop control and invoke Undo/Redo only where available; record command availability and actual state, not presumed undoability.'),
 ('CANCEL', 'Cancel an offered settings/device permission or connection dialog; observe previously active sync and partial settings. Dialog availability is itself unknown.'),
 ('PERSISTENCE', 'Save/reopen an owned Set and separately restart application with explicit Link/Follow/MIDI settings; inspect Set-versus-global retention and restored device identities.'),
 ('LOSS', 'After active positive tempo and audio, disconnect only the selected peer/network, audio input or MIDI source in separate trials, then reconnect; record recovery without a deadline.'),
 ('ARBITRATION', 'Switch external input types, Follow, Link, EXT and Start Stop Sync across start/stop/seek in separate reset trials; retain event order and no inferred conflict policy.'),
 ('TEARDOWN', 'Leave peers or close track, Set and application while sync and incoming audio are active; retain remote/local states, prompts and pending recording outcomes.')])}
for group, (title, contract, probes) in gaps.items():
    rid = 'REQ-SYNC-WORKFLOW-U-'+group
    reqs.append(dict(id=rid, title=title, contract=contract, strength='U', target_applicability='U', evidence=[]))
    for suffix, action in probes:
        cases.append(dict(id='SYNC-U-'+suffix, requirements=[rid], kind=suffix.lower(), fixture='fixtures.json#SYNC-OWNED', setup_and_action=action, source_claim=None, documentary_expected=None, documentary_comparator=None, expected=None, comparison=None, target_grade='U', executed=False, evidence=[]))
assert len(reqs)==26 and len(cases)==36 and len({c['id'] for c in cases})==36

def save(name, value):
    raw = (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode() if not isinstance(value, str) else value.encode()
    path = P/name
    assert not path.exists() or path.read_bytes()==raw, name
    path.write_bytes(raw)

save('requirements.json', reqs)
save('cases.json', cases)
helper = P.parent/'session-workflows/capture.py'
save('dependencies.json', [dict(path=str(helper.relative_to(ROOT)), bytes=helper.stat().st_size, sha256=hashlib.sha256(helper.read_bytes()).hexdigest(), role='existing analyst chapter_content parser, no original code')])
save('fixtures.json', dict(id='SYNC-OWNED', status='future owned setup; no peers, hardware, audio, messages or reference results supplied', setup='Two independently validated compatible Link peers on an isolated network, explicit capabilities/builds and nonempty audio-output source tracks; owned nonzero distinguishable local/incoming pulse audio, active gain/unmuted output, audio interface input and independently validated MIDI Clock/MTC source/receiver. Retain accepted rate, loop, tempo, offset, delay, monitoring/arming, Follower/EXT/Start Stop Sync and count-in states; reset per trial. Use isolated owned test configurations.', positive_guard='Retain usable source traffic, connected peer and actual positive audio/tempo path before absence/disabled/gap/failure trials. Count/name/LED presence alone is not sync/audio proof. Record gates are owned by recording-comping. No actual network/hardware/reference run is authorized or claimed by this packet.', unavailable='Missing compatible peer, source, permission, driver, input, supported option or accepted baseline leaves U. Numeric, signal and timing oracles remain null.', platform='Record exact OS/build, peer products/firmware, network, interface, sample rate and MIDI source formats. Current Version12 Link Audio prose does not establish this feature exists in12.4.3.'))
source = json.loads((P/'source.json').read_text())
front = '---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
spec = front.format(id='SPEC-SYNCHRONIZATION-WORKFLOWS', type='spec', status='draft')+'''# Link, Link Audio, Tempo Follower and MIDI synchronization

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

'''
for r in reqs:
    spec += f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
    if r['evidence']:
        spec += 'Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact routes](#analysis-only-evidence).\n\n'
spec += '''## Finite acceptance proposals

The [case catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases.json)
contains24documentary source-role proposals and12operational U probes for
26requirements (24 D12/2 U). Every target expected/comparison is null/U;
all signal/timing documentary outputs are also null. No future fixture is a result.

| Case | Requirement | Kind / action |
| --- | --- | --- |
'''
for c in cases:
    spec += '| '+c['id']+' | '+c['requirements'][0]+' | '+c['kind']+': '+c['setup_and_action']+' |\n'
spec += f'''
## Analysis-only evidence

Official [Version12 synchronization chapter]({source['url']}), captured
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/{source['file']}).
[54 source blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-blocks.json)
retain anchors/HTML lines; figures and image glyphs were not inspected.
[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements.json),
[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r1.json)
and exact parser pin in dependencies.json freeze the reviewable partial packet.
The current manual is not immutable12.4.3 evidence. There is no claimed wire
format, detector model, clock convergence, latency/jitter tolerance, supported
rate enumeration, complete platform matrix or full device interoperability.
'''
research = front.format(id='RES-SYNCHRONIZATION-WORKFLOWS', type='research', status='current')+f'''# Synchronization evidence and unresolved boundaries

The [canonical draft](../specs/synchronization-workflows.md) follows the
[execution plan](full-live-specification-plan.md). It owns synchronization-specific
documentary roles, with shared recording/routing/launch behavior linked rather
than redefined. No original, peer, network connection, audio/MIDI device or candidate ran.

## Exact capture and version limits

Official [Version12 chapter]({source['url']}), captureUTC {source['capture_utc']},
{source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/{source['file']}).
This source is the current website, without an immutable publication revision
or exact12.4.3 applicability. Link Audio presence/availability in the target is
unknown. The separate web-tool reading view is not this byte identity.
The [54-block extraction](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/source-blocks.json)
uses only chapter_content through the existing Session analyst parser, pinned
in dependencies.json; headings, text and anchors are retained, figures uninspected.

## Interpretation and ownership

- Link beat/phase/global-quantization language supplies no distributed clock,
  scheduler or finite launch formula. Last participant tempo wording gives no
  causal ordering or convergence guarantee for simultaneous changes.
- Link Audio latency and buffered display describe public control roles, not
  private buffer structure or numerical sample delay. Sync to Incoming Audio
  is documented for only one participant; multiple-enabled failure/enforcement
  remains unknown. Peer name/count/status is not clock or audio proof.
- Source selection and feature enabling add prerequisites to existing routing
  and recording owners; they do not redefine In/Auto/Off/arm gates. Live/Push
  send/receive prose supplies no perfirmware compatibility matrix.
- Tempo Follower clear-rhythm optimization is not an input restriction, detector
  algorithm, bounded tempo error or acquisition time. Hidden Follow and missing
  channel conditions are distinct from no audible input. Follower/EXT exclusion
  does not resolve every transition or simultaneous external/peer source conflict.
- MIDI Clock/MTC roles are documented without encoding/tick counts or parser
  grammar. MTC receiver-only, manual tempo and no meter tracking stay distinct
  from MIDI Clock tempo following. The usual SMPTE rates are not enumerated;
  no drop-frame law, offset grammar or frame-to-beat conversion is inferred.
- Song-position loop wrapping gives no mathematical modulo/boundary law.
  Per-device Sync Delay listening guidance gives no precision/tolerance or
  measured calibration and does not replace device Hardware Latency.
- Count-in unavailability applies to Link-enabled recording, not ordinary
  metronome output. Reliable synchronization marketing supplies no benchmark.

## Review and required evidence

[26 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/requirements.json)
cover24D12 documentary roles and2U obligations;
[36 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/cases.json)
include12operational U proposals. All exact-target outcomes/comparisons remain
null/U/unexecuted; signal/timing documentary outputs are also null. Owned setups
are future prerequisites, not retained source stimuli or measured results.
Numeric/protocol/source-arbitration, malformed/boundary, cancel/undo/persistence,
source-loss/reconnect/rate and teardown outcomes remain required unknowns.
Independent semantic review follows the
[author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/synchronization/manifest-author-r1.json).
No whole synchronization, Push, network or controller family is complete.
'''
for name, text, canonical in [('spec-r1.md',spec,'wiki/specs/synchronization-workflows.md'),('research-r1.md',research,'wiki/research/synchronization-workflows.md')]:
    path = ROOT/canonical
    assert not path.exists() or path.read_text()==text
    path.write_text(text)
    save(name,text)
print('26 requirements /36 cases authored; no target execution')
