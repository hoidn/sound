"""Author documentary remote-control packet; never executes Live or a controller."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[3]


def write(name, value):
    (P / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def pin(path, role):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'role': role}


blocks = {r['id']: r for r in json.loads((P / 'source-blocks.json').read_text())}
rows = []


def add(title, kind, contract, numbers, action):
    n = len(rows) + 1
    rows.append({'id': f'REQ-REMOTE-WORKFLOW-{n:03d}', 'title': title,
                 'kind': kind, 'contract': contract, 'blocks': numbers,
                 'case_id': f'RC-{n:03d}', 'action': action})


add('Slot-bound assignments', 'mapping-effect',
    'MIDI and computer-key assignments to Session slots belong to the slot, not the contained clip. Clip launch effects remain with the Session/clip-launch owners; replacement, move and delete identity rules beyond this distinction remain U.', [3],
    'Use two populated slots A/B with distinct active clips and a confirmed mapped A baseline. Replace only A content on an owned copy, then move a clip separately; retain slot, clip, assignment and playing identities. No launch or remapping identity oracle is supplied.')
add('Assigned MIDI notes and track input', 'signal',
    'The chapter describes a MIDI note assigned to remote control as unavailable for MIDI-track instrument input. This is a documentary exclusivity role, not a general channel/port interception, note-off or MPE dispatch law.', [10, 11],
    'Confirm a valid note produces nonzero output on a known armed/monitored instrument and separate remote target. Assign that note to a slot, retain exact input port/channel and independently observed events, then compare an unassigned neighboring note. Do not infer a MIDI byte/filter law.')
add('Named surface setup', 'control',
    'For a natively supported surface, choose its name in Control Surface settings and choose input/output ports in adjacent columns. The source describes up to six supported surfaces simultaneously; an absent chooser entry leads to manual setup, not proof of incompatibility or any particular profile protocol.', [12, 14, 15, 25],
    'With an independently identified supported surface and available ports, inspect its named row and input/output choices. Compare a separate unlisted controller through manual setup. Inspect offered rows; a seventh-device result is U.')
add('Conditional preset-dump setup', 'protocol',
    'Some surfaces require a preset dump and expose an enabled Dump button for setup. The hardware must first be ready to receive it using its own documented preparation. No universal dump requirement, payload, success detector, timeout or device-state restoration follows.', [16],
    'Retain an independently supported surface setup and manufacturer readiness procedure. Inspect whether Dump is offered/enabled and compare a known no-dump setup. Any future actual dump requires separately authorized hardware context; payload and setup outcome remain U.')
add('Manual override of instant assignments', 'mapping-effect',
    'Manual assignments may override instant mappings, with Remote enabled for the relevant ports. The override scope, conflict arbitration, release/restoration and host effect are not established by this chapter or by the finite configuration release.', [18, 19],
    'Establish a positive instant-controlled parameter on device A, then create one manual mapping for that physical control to distinct eligible B. Retain Remote/focus/selection and compare deletion in a reset copy. No winner, timing or restored-route oracle is assigned.')
add('Selection-following instant control', 'mapping-effect',
    'Instant mappings are described as following selected devices. Exact per-surface parameter banks, unsupported devices, selection/focus races and host delivery remain U; this does not complete the existing host/bank unknowns.', [18, 20],
    'Use a known supported instant surface and two independently responsive unlocked devices A/B with distinct controls. Select A then B while retaining actual bank/target state; separately change view focus without selecting another device. Host target/value results stay U.')
add('Lock menu and status affordances', 'control',
    'For a surface that supports device locking, the device-title context menu Lock to entry enables/disables its lock; the available surface names correspond to configured surfaces, and a hand icon indicates locked status. Some surfaces do not support locking. This clause owns the generic entry/status affordance only.', [21, 22, 23],
    'With independently confirmed lock-capable surface S, inspect device A context menu, select S and inspect hand status; revisit the same entry to unlock. Compare an independently known unsupported surface without presuming its menu presentation.')
add('Lock focus and arming context', 'mapping-effect',
    'The manual describes supported device locking as retaining access across focus changes and describes a default automatic instrument lock when a MIDI track is armed. These are documentary contexts only: capability, arm-selection interaction, constructor default, bank contents and host lock effects remain U under the existing mapping owner.', [21, 23],
    'With lock-capable S and independently responsive instruments A/B, explicitly lock A, select B and vary focus. In separate reset fresh/loaded copies arm A with lock state retained. Record actual control destinations without assuming default lock or resolving host semantics.')
add('Manual setup entry boundary', 'control',
    'An unlisted control surface can be set up for manual mapping through MIDI Ports. This workflow uses the routing owner\'s Remote input/output roles, rather than redefining Track/Sync/Remote or promising arbitrary hardware support.', [25, 26],
    'Identify an available input from an unlisted owned controller, inspect MIDI Ports and explicitly enable the routing owner\'s Remote input role. Keep Track/Sync settings declared; verify usable input separately before attempting an assignment.')
add('Feedback prerequisite', 'signal',
    'Physical/visual feedback surfaces require the output-port Remote role so value changes can be reflected by faders or LEDs. The general port switch belongs to routing; feedback eligibility, startup state, bytes, loops and physical movement law remain U.', [27],
    'Use an independently working feedback surface, selected output and active mapped target; retain a positive feedback baseline. Disable only output Remote in a reset trial, preserving input and value changes. No feedback bytes, motor deadline or silence criterion is supplied.')
add('Incoming activity indicator', 'control',
    'The Control Bar MIDI indicators flash when Live recognizes incoming MIDI. This is an activity indicator role, not proof of a mapping, source identity, output feedback, MIDI-track admission or hardware synchronization.', [28],
    'Retain independently identified usable controller traffic and inspect incoming activity, then separately send an unmapped eligible control. Keep mapped-target response and track input observations independent of indicator status.')
add('Takeover selection context', 'control',
    'The source presents None, Pick-Up and Value Scaling for absolute controls used across destination banks. This clause supplies documentary chooser vocabulary and setup context only; finite transforms, previous-value history, exemptions and precision stay with REQ-MIDI-USER-005/010 and midi-config-v4. Target displayed labels/default remain unproven.', [29, 31, 32, 33, 34],
    'Inspect the offered takeover choices and record the explicitly selected choice. Use two known destination banks and nonmatching physical/current parameter positions only for separately ungraded value trials; do not assume a default or test a new convergence formula.')
add('Mapping Browser view and columns', 'control',
    'The Mapping Browser is shown for the active manual MIDI, key or Macro mapping mode and lists that mode\'s mappings with control element, parameter path/name and Min/Max. This owns common browser presentation; rack Macro assignment/delegation remains with device-racks.', [36],
    'Prepare distinct manual MIDI and key mappings and a separately owned rack Macro map. Enter each mode individually and inspect visible rows/columns; compare their target identities and return to normal view. Macro assignment behavior is not retested here.')
add('Range edit and inversion entrypoints', 'control',
    'Mapping Browser Min/Max entries can be edited, and a context command inverts them. This is an editing affordance only: accepted domains, parsing, stored representation, target scaling/rounding and resulting values remain with existing finite owners or U.', [36],
    'Select a known manual mapping with two independently accepted unequal endpoints; edit each endpoint and invoke the inversion command. Retain displayed before/after entries without assigning a numerical target or exact serialization oracle.')
add('Delete a selected mapping', 'control',
    'The Mapping Browser deletes selected mappings with Backspace on Windows or Delete on Mac. Restoration of target value, control ownership, held-input cleanup and Undo grouping are not specified.', [36],
    'Create two distinct confirmed browser mappings A/B; select only A row, invoke the platform deletion key, and inspect remaining rows. Test target input, undo and held-note effects separately as U; do not delete source media or devices.')
add('Instant mappings outside the browser', 'control',
    'Context-based instant mappings are not listed in the Mapping Browser. Absence from this manual-mapping list does not prove absence of active instant control.', [37],
    'Establish positive instant control with no manual assignments, open MIDI Map Mode and inspect browser; then create one independent manual row. Retain positive device response separately from list membership.')
add('MIDI Map Mode entry and exit', 'control',
    'The MIDI switch enters Map Mode, highlighting assignable controls blue and exposing Mapping Browser; the switch exits and hides the browser. Reentering allows review. Ctrl+Alt+B on Windows or Cmd+Option+B on Mac opens a closed Browser in this context; exact geometry/color metrics are not specified.', [39, 40, 43],
    'In the main window outside text/modal/plugin focus, enter MIDI Map Mode, inspect eligible highlights/browser, close and reopen Browser with the platform chord, then exit and reenter. Retain key/navigation preferences and active view.')
add('Create a manual MIDI assignment', 'control',
    'In MIDI Map Mode, select an eligible parameter and send a controller MIDI message; the new assignment is listed in Mapping Browser. Supported message grammar, duplicate/conflict resolution, transaction boundaries and host delivery are not established here.', [39, 40, 41, 42],
    'With active Remote input, known channel and independently received eligible control, select one highlighted unassigned target and send that input. Inspect new row/control/target identity and reenter for review; compare a different unassigned target in a reset copy.')
add('Note-target roles', 'mapping-effect',
    'The source assigns note gestures to switches/options and describes a single note toggling a variable parameter between endpoints, while a note range supplies discrete spaced values. Session slot input follows its Launch Mode owner. Exact note grammar, toggle dispatch, spacing/interpolation, endpoint codec and timing remain U.', [45, 46, 47, 48, 49],
    'In separate mappings use a known eligible note for an activator, finite option selector and variable control with accepted endpoints, then a known supported note range. Retain actual message/channel identity and active baseline; launch mode is declared separately and no value equation is graded.')
add('Chromatic slot-range assignment gesture', 'control',
    'For a chromatic Session-slot note range, the documented assignment gesture holds a root key, then a lower and higher key to define bounds. The root is described as default transposition. Transposition, note allocation, range codec and sound remain U.', [50],
    'With a populated audible slot selected in MIDI Map Mode, use three independently identified distinct supported notes in root/lower/upper order with root held. Retain created mapping fields; compare release/order/boundary variants only as unknown probes, without pitch-output criteria.')
add('Absolute input family boundary', 'transform',
    'The chapter describes absolute control input, pitch bend and high-resolution absolute input with target-dependent effects. Its numerical threshold/range examples are retained as source context only. The released configuration transforms remain scoped to their stated parameters/assumptions; no manual-Learn, switch, radio or slot law is imported from them.', [52, 53, 54, 55, 56, 57],
    'Use independently supported absolute CC, pitch-bend and high-resolution input in separate fresh mappings to an active eligible target. Retain actual offered mode and raw source identity. Do not infer half-pairing, switch threshold, radio quantization or fader/gain law from prose.')
add('Relative-mode detection and selection', 'control',
    'The source names Signed Bit, Signed Bit 2, Bin Offset and Twos Complement families plus linear variants. For unsupported-native surfaces it describes detection of type/acceleration, aided by a slow left movement during assignment; a Status Bar mode chooser offers a suggestion and manual selection. Detection success, exact UI list and mapping to configuration tokens remain U.', [59, 60, 61, 62, 68],
    'With an independently known relative encoder family and eligible active target, assign using slow left movement, record the suggested and offered modes, and select the known offered type manually. Repeat one other family separately; no classifier success or byte-decoder oracle is assigned.')
add('Relative target roles', 'transform',
    'Relative increment/decrement gestures are described as slot down/up equivalents, switch on/off and option forward/back; continuous interpretation depends on controller type. Exact codecs, steps, acceleration, endpoint/wrap and event dispatch remain U here; existing released relative computations are not broadened.', [63, 64, 65, 66, 67],
    'Use a positively identified relative encoder and separately eligible slot, switch, option and continuous targets. Establish active responses, send each declared direction separately, and retain offered mode, endpoints and launch mode. No arbitrary raw value or exact step is predicted.')
add('Relative Session mapping strip', 'control',
    'Both MIDI and Key Map modes expose a strip of assignable controls below the Session grid for relative navigation/launch roles. This is a mapping entrypoint, not a launch/scene scheduling law.', [70, 71],
    'Use Session with populated A/B/C scenes and distinct tracks. Enter MIDI then Key Map Mode separately, inspect the assignable strip, and exit each. Grid/focus/selection rendering remains with Session View.')
add('Highlighted-scene navigation assignment', 'mapping-effect',
    'The strip offers up/down highlighted-scene controls assignable to keys/notes/controllers and a scene-number box assignable to a MIDI controller for scrolling. Endpoint/wrap, number encoding, relative decoder and focus precedence remain U.', [72, 73],
    'Map separate eligible up/down controls and a known encoder to the scene box; start at middle populated scene B among A/B/C and retain highlight, focus and mapped input before each direction. Probe first/last and empty scenes separately as U.')
add('Highlighted-scene launch and cancel entrypoints', 'control',
    'The strip offers launch-highlighted-scene and cancel-triggered-scene assignment targets. Scene launch/cancel behavior and Select Next Scene on Launch stay with REQ-SESSION-VIEW-010/011; this clause adds only mapped entrypoints.', [74, 75],
    'In Map Mode inspect and separately assign highlighted-scene launch/cancel targets using distinct controls. Declare Select Next Scene on Launch and selected scene. Future cancel trials require independently confirmed pending state under the existing scene owner, with timing ungraded.')
add('Per-track highlighted-row clip launch target', 'control',
    'The strip supplies per-track assignable controls to launch the clip at the highlighted scene. This is a target-entrypoint role only; empty-slot recording/stop, clip launch timing and playing/selection changes remain with existing owners or U.', [76],
    'Use two active tracks with distinct populated clips in highlighted scene B, inspect corresponding assignable strip controls and create distinct mappings. Retain track/slot/scene identities; empty and armed-slot effects remain unknown.')
add('Highlighted-scene viewport role', 'control',
    'Relative Session mapping is described as keeping the highlighted scene centered in Session View. No pixel metric, edge-of-list padding, hidden-row or resizing policy is established.', [77],
    'Use enough owned scenes to scroll, map valid navigation and begin at an interior scene; inspect highlighted-row viewport placement after two separate moves. First/last scene and resize behavior remain U, with no pixel tolerance.')
add('Clip View mapping follows selection context', 'mapping-effect',
    'Mappings created for Clip View controls can affect different selected clips, including multi-selection; the manual recommends relative controls to avoid value jumps. Shared panel/selection UI stays with Clip View. This is not a numerical smoothing guarantee, target identity formula or general multi-edit transaction law.', [79],
    'Use two independently active clips with the same eligible Clip View control but distinct current values. Map once, select A then B and then both in reset trials; retain selected identities and actual mapping. Do not assume clip-specific binding or target value continuity.')
add('Key Map Mode entry and exit', 'control',
    'The KEY switch enters Key Map Mode with red-highlighted assignable controls and Mapping Browser; the View menu can show a hidden Browser. Exiting hides Mapping Browser, and reentering allows review. This does not define global shortcut or Computer MIDI Keyboard dispatch.', [81, 82, 85],
    'With main window focus and explicit keyboard layout, Computer MIDI Keyboard and navigation preferences, enter KEY mode, inspect eligible highlights/browser, show hidden Browser via View menu, exit and reenter. Keep text/modal/plugin focus out of the positive trial.')
add('Create a computer-key assignment', 'control',
    'In Key Map Mode select a red-highlighted eligible control and press a computer key; Mapping Browser displays the new assignment. Only highlighted controls are offered for mapping; duplicate keys, reserved chords, layouts and text-focus interception remain U.', [83, 84],
    'In KEY mode choose one red-highlighted unassigned target and a known otherwise unused key under retained layout/focus/preferences. Inspect the new row and target identity; separately inspect a nonhighlighted control without presuming a click/error result.')
add('Computer-key target roles', 'mapping-effect',
    'Mapped computer keys are described as operating slot clips according to Launch Mode, toggling switches and cycling option buttons. This is manual key mapping, distinct from Computer MIDI Keyboard note generation; global shortcuts, key-repeat, held releases and precedence remain U.', [86, 87, 88, 89, 90],
    'Use separate known unused mapped keys for an active slot, switch and finite option selector, with actual focus/layout/Computer MIDI Keyboard state declared. Retain down/up/repeat and compare an unmapped key. Launch and input arbitration outputs stay ungraded.')

unknowns = [
    ('CONTEXT', 'Key and focus arbitration', 'Layout/IME, Computer MIDI Keyboard, global shortcuts, text/modal/plugin focus, navigation preferences, repeats and duplicate input-source precedence remain unknown.',
     [('KEY-CONTEXT', 'context', 'Repeat a positively mapped key with Computer MIDI Keyboard on/off, declared Tab/navigation settings, text edit, modal and plugin focus, then a second layout/IME in separate owned trials.'),
      ('DUPLICATE', 'conflict', 'After one working manual mapping add duplicate key or MIDI address, competing instant mapping and two input ports/channels separately; retain actual accepted assignments and input order.')]),
    ('NUMERICAL', 'Manual mapping numerical and protocol outcomes', 'Manual MIDI Learn admission, message bytes, relative detection/codecs, scales, display curves, thresholds, takeover application, feedback and sample/event timing remain unknown beyond separately released finite clauses.',
     [('NUMERIC', 'transform', 'For known eligible active targets retain accepted Min/Max, current value, actual mode and raw input; compare equal/reversed endpoints, stepped targets, takeover after bank change and first high-resolution input without a new numeric oracle.'),
      ('FEEDBACK', 'signal', 'With positive feedback and nonzero mapped target path retain actual outbound messages and hardware state through bank/focus changes, disabled output and reconnect; do not infer bytes or motor/LED timing.'),
      ('TIMING', 'timing', 'Retain actual input timestamps and active target/source across transport stopped/running, tempo changes and accepted sample rates/block sizes. No cadence, debounce, latency, key-repeat or rate-equivalence criterion exists.')]),
    ('PROFILES', 'Per-profile and host behavior', 'Generic setup does not specify the 149 inventoried controller directories, Push generations, arbitrary scripts, user-profile discovery/reload, exact device bank contents, host lock/arm effects or preset-dump protocols.',
     [('PROFILE', 'profile', 'Select one independently identified profile/build and available supported device; retain offered banks, lock capability, host target identities and required hardware setup. Other profiles remain individually untested.'),
      ('DUMP', 'protocol', 'For separately authorized future hardware work only, retain known readiness and active baseline, then explore unavailable/failed/interrupted dump and recovery. This packet authorizes and executes no dump.')]),
    ('BOUNDARIES', 'Assignment domains and malformed controls', 'Invalid/unsupported controls/messages/ranges, empty or deleted targets, range gestures, exhausted surface rows, and cancellation commit points lack output oracles.',
     [('BOUNDARY', 'boundary', 'After positive active mappings inspect first/last/empty scenes, nonhighlighted targets, zero/equal/reversed/offered-boundary ranges, note-range order and sixth/seventh surface rows. Record offered bounds rather than inventing clamp/reject.'),
      ('MALFORMED', 'malformed', 'In disposable owned settings enter invalid/nonfinite range text and unsupported/partial MIDI input separately after accepted baseline; retain errors and resulting mappings without assuming accepted grammar.'),
      ('CANCEL', 'cancellation', 'Begin mapping/range or offered surface settings operation, cancel with available Escape/dialog control before and after independently observed commit in separate copies; do not assume rollback.')]),
    ('LIFECYCLE', 'Persistence, undo, automation and teardown', 'Set/global ownership, save/reopen/migration, undo grouping, automation override, source loss/reconnection, reset history and cleanup during held input/device deletion remain required unknowns.',
     [('PERSISTENCE', 'persistence', 'Save/reopen an owned Set and separately restart with explicit mappings, ranges, relative modes, takeover and locked surface; import an owned clip/device/rack into another Set and retain mapping/identity/settings ownership.'),
      ('UNDO', 'undo-redo', 'Create/edit/delete one mapping and change a surface lock/range, then request Undo/Redo only where available; retain browser rows, target value and settings separately.'),
      ('AUTOMATION', 'automation', 'With known eligible automated target and active mapped input, vary manual/mapped control, clip/Arrangement envelope and re-enable in separate reset trials; no override arbitration or interpolation rule follows.'),
      ('LOSS', 'source-loss', 'After usable mapped input and feedback disconnect only selected controller/input/output, reconnect and change port identity separately; retain held inputs, mapping rows and physical/target states.'),
      ('TEARDOWN', 'teardown', 'With active mapped target and held note/key or pending feedback, delete target/device/track, close Set, remove surface and close app in separate future trials. Stuck-note prevention, reset history and resource cleanup remain U.')])
]

requirements, cases = [], []
for row in rows:
    evidence = [{k: blocks[f'RC-B{n:03d}'][k] for k in ('id', 'anchor', 'html_line')} for n in row['blocks']]
    requirements.append({'id': row['id'], 'title': row['title'], 'contract': row['contract'],
                         'strength': 'D12', 'target_applicability': 'U', 'evidence': evidence})
    visible = row['kind'] == 'control'
    cases.append({'id': row['case_id'], 'requirements': [row['id']], 'kind': row['kind'],
                  'provenance': 'D12', 'fixture': 'fixtures.json#RC-OWNED',
                  'preconditions': ['common', 'active-positive-guard'],
                  'setup_and_action': row['action'], 'source_claim': row['contract'],
                  'documentary_expected': row['contract'] if visible else None,
                  'documentary_comparator': 'Named visible entry, eligibility, mapping-row and indicator relations only; no MIDI byte, numeric value, event/audio/timing or hardware compatibility proof.' if visible else None,
                  'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False,
                  'evidence': evidence})
for suffix, title, contract, probes in unknowns:
    rid = 'REQ-REMOTE-WORKFLOW-U-' + suffix
    requirements.append({'id': rid, 'title': title, 'contract': contract,
                         'strength': 'U', 'target_applicability': 'U', 'evidence': []})
    for cid, kind, action in probes:
        cases.append({'id': 'RC-U-' + cid, 'requirements': [rid], 'kind': kind,
                      'provenance': 'U', 'fixture': 'fixtures.json#RC-OWNED',
                      'preconditions': ['common', 'active-positive-guard'], 'setup_and_action': action,
                      'source_claim': None, 'documentary_expected': None, 'documentary_comparator': None,
                      'expected': None, 'comparison': None, 'target_grade': 'U', 'executed': False,
                      'unknown': contract, 'evidence': []})
write('requirements.json', requirements)
write('cases.json', cases)
write('fixtures.json', {
    'id': 'RC-OWNED', 'status': 'future finite owned setups; no controller/media/message/reference result supplied',
    'common': 'Reset owned editable Set/configuration per trial. Retain exact OS/build, keyboard layout/IME, main/text/modal/plugin focus, Computer MIDI Keyboard, navigation/key preferences, view/selection/arm/monitor/transport, actual input/output ports and channels, Track/Sync/Remote roles, surface/profile/firmware/capability, manual/instant/rack mappings, mode, bank, lock, takeover and independently accepted target kind/current value/range. No profile capability or default is assumed.',
    'active-positive-guard': 'Independently confirm usable eligible controller/key input and the active mapped target/device on the intended route, actual known focus/channel/preferences, and nonzero source/depth/gain with unmuted output for audible paths. Establish a matched positive response before zero/disabled/unmapped/no-effect claims; feedback needs independently working output/hardware. Change only the explicitly tested state. LED/browser row presence alone is not delivery, value, feedback or audio proof.',
    'setups': {'manual': 'Two active tracks with distinct populated A/B clips, eligible activator/option/continuous targets with accepted unequal ranges, and two independently identified controller inputs.',
               'surface': 'Independently supported surface S with usable ports, known instant target/banks and declared lock/feedback/dump capability; no hardware supplied or invoked.',
               'key': 'Two unused keys under declared layout, repeat and Computer MIDI Keyboard state; positive trials outside text/modal/plugin focus.',
               'session': 'At least three populated scenes A/B/C on two active tracks; distinct mapped navigation/launch/cancel controls and independently confirmed pending state for future cancel observations.'},
    'unavailable': 'Missing target eligibility, compatible surface, source, accepted range, permission or positive baseline leaves U, never pass.',
    'original_execution': False, 'candidate_comparison': False})

owner_paths = ['wiki/specs/midi-user-mapping.md', 'wiki/specs/keyboard-navigation.md',
               'wiki/specs/routing-monitoring-latency.md', 'wiki/specs/mpe-workflows.md',
               'wiki/specs/device-racks.md', 'wiki/specs/max-for-live-hosting.md',
               'wiki/specs/clip-view-workflows.md', 'wiki/specs/session-view-workflows.md',
               'wiki/specs/clip-launch.md', 'wiki/specs/session-launch-workflows.md',
               'wiki/specs/automation-envelopes.md']
owner_paths += ['handoff/midi-config-v4/' + name for name in ('README.md', 'spec.md', 'REVIEW.md', 'manifest.json')]
write('owner-pins.json', [pin(ROOT / name, 'existing canonical/release owner, unchanged') for name in owner_paths])
release = ROOT / 'handoff/midi-config-v4'
release_manifest = json.loads((release / 'manifest.json').read_text())
for record in release_manifest['files']:
    raw = (release / record['path']).read_bytes()
    assert len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256']
write('release-boundary.json', {'release': 'midi-config-v4', 'payloads_checked': len(release_manifest['files']),
                              'finite_only': True, 'manual_Learn_host_profiles_or_UI_parity_inferred': False})
from collections import Counter
counts = {'requirements': len(requirements), 'requirement_provenance': dict(Counter(r['strength'] for r in requirements)),
          'cases': len(cases), 'case_provenance': dict(Counter(c['provenance'] for c in cases)),
          'case_kinds': dict(Counter(c['kind'] for c in cases)), 'source_blocks': len(blocks),
          'documentary_control_proposals': sum(c['documentary_expected'] is not None for c in cases),
          'all_target_null_U_unexecuted': True, 'original_execution': False, 'candidate_comparison': False}
write('counts.json', counts)
source = json.loads((P / 'source.json').read_text())
base = '../../analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/'
spec = '''---
id: SPEC-REMOTE-CONTROL-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Manual MIDI/key mapping and generic control-surface workflows

## Scope and canonical owners

This partial F-08 draft owns documented manual assignment/edit/delete and common
Mapping Browser, generic surface setup, lock entry/status and mapping-context
roles. **D12** means current Version12 prose, not exact12.4.3 evidence. All target
outcomes are null/U/unexecuted. This is not a release or compatibility result.
[Coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/remote-control-workflows.md) owns interpretation/questions.

[MIDI user mapping](midi-user-mapping.md) revision6 and the immutable
[midi-config-v4 release](../../handoff/midi-config-v4/README.md) retain finite
configuration/tokens/addresses, numeric transforms, takeover/history/precision,
encoder compaction and bank-span laws. No finite law is copied or broadened to
manual MIDI Learn, arbitrary scripts, buttons or a whole host. Existing
REQ-MIDI-USER-007/008 bank contents/host lock effects stay unknown. New lock
affordances and source prose below do not settle those host effects.

[Keyboard/navigation](keyboard-navigation.md) owns global shortcuts, focus,
accessibility and its discovery catalog. Manual key assignment does not imply
global dispatch or Computer MIDI Keyboard notes. [Routing](routing-monitoring-latency.md)
REQ-RML-011/012 owns port/channel and Track/Sync/Remote roles; this page links those
prerequisites. [Racks](device-racks.md) owns Macro assignment/ranges/delegation;
[MPE](mpe-workflows.md) owns expression/zone configuration;
[Max hosting](max-for-live-hosting.md) owns its editor/API scope, without arbitrary
patch or controller compatibility. [Clip View](clip-view-workflows.md) owns panel
selection. [Session View](session-view-workflows.md) owns scene navigation/launch/
cancel; [clip launch](clip-launch.md) and [Session launch](session-launch-workflows.md)
retain their finite laws and runtime unknowns. [Automation](automation-envelopes.md)
retains evaluation and unresolved override/editing; mapped input supplies no new
interpolation or arbitration law. Generic setup closes none of the149 controller
directory profiles or Push-specific protocols.

## Inputs, state and comparison

The [future fixture](REPLACEfixtures.json) requires actual eligible active targets,
usable input/channel/port, known focus/layout/key preferences and independently
working mapped-device response. Audible/feedback/no-effect probes require
nonzero eligible input, active unmuted source/output and paired positive baseline.
The rows/settings/LED are not delivery, protocol, numeric value or audio proof.
No source MIDI/media/hardware is supplied and no Live/native/candidate ran.

All cases have target `expected:null`, `comparison:null`, `target_grade:U`,
`executed:false`. Only named visible control/browser/status proposals have
documentary predicates. Signal, transform, mapping-event, protocol and timing
cases also have null documentary expected/comparator; their `source_claim` is
source context only. No numerical curve, codec, quantization, default, convergence
law, feedback byte, hardware action, timing tolerance or architecture is invented.

## Documentary requirements

'''.replace('REPLACE', base)
for r in requirements:
    spec += f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
    if r['evidence']:
        spec += 'Evidence: ' + ', '.join(f"`{e['id']}` (#{e['anchor']}, HTML{e['html_line']})" for e in r['evidence']) + '.\n\n'
spec += f'''## Finite acceptance proposals and unknowns

[{len(cases)} cases]({base}cases.json) cover {len(rows)} D12 roles and5 U requirements.
Compound clauses remain partial until each branch, applicable platform/controller
and lifecycle kind closes. Unknown categories include context/conflicts, numeric/
feedback/timing, per-profile/dump, boundary/malformed/cancel, persistence/undo/
automation/loss/teardown. Missing controls or actual dialog availability remains U.

| Case | Requirement | Kind / finite action |
| --- | --- | --- |
'''
for c in cases:
    spec += f"| {c['id']} | {c['requirements'][0]} | {c['kind']}: {c['setup_and_action']} |\n"
spec += f'''
## Analysis-only evidence and freeze

Official [Version12 MIDI and Key Remote Control]({source['url']}),
captured {source['capture_utc']}, {source['bytes']}bytes,
SHA-256 `{source['sha256']}`. [Retained HTML]({base}{source['file']})
and [90 exact text blocks]({base}source-blocks.json) preserve anchors/HTML lines;
figures were not separately inspected. Current web documentation has no immutable
12.4.3 publication identity. Numerical threshold examples and lock-on-arm default
wording are context, not a new released oracle. [Requirements]({base}requirements.json),
[counts]({base}counts.json), [owner pins]({base}owner-pins.json) and
[manifest]({base}manifest-author-r1.json) freeze the partial review packet.
'''
research = f'''---
id: RES-REMOTE-CONTROL-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Remote-control documentation and unresolved host contexts

The [canonical draft](../specs/remote-control-workflows.md) follows the
[full coverage plan](full-live-specification-plan.md). Existing
[mapping research](midi-user-mapping.md) and the revision6 canonical spec retain
their finite numeric/configuration/host boundaries. This new source fills a
manual mapping and generic setup gap, not per-profile completion.

## Source identity and method

Official [Version12 chapter]({source['url']}), captured UTC
{source['capture_utc']}, {source['bytes']}bytes,
SHA-256 `{source['sha256']}`;
[exact bytes]({base}{source['file']}). The separate web-tool reading is not
this capture identity. [90 blocks]({base}source-blocks.json) were extracted with
the already retained guarded Session chapter parser pinned in dependencies.json.
Anchors and exact HTML lines are preserved; figures/inline glyphs are uninspected.
No application, original function/native host, controller, hardware dump, audio,
MIDI output or independent candidate executed. No tooling was installed.

## Interpretation and source questions

- RC-B003 distinguishes slot binding from clip content, without move/delete or
  empty armed-slot policy. RC-B010/011 describes exclusive remote-note use, but
  supplies no per-port/channel grammar, note-off or MPE interception law.
- RC-B014/015 gives generic named-surface setup and a six-surface documentary
  limit; it is no complete supported-profile list or seventh-row error oracle.
  RC-B016 preset dump is conditional on actual hardware readiness. No dump bytes
  or action are authorized by this documentation task.
- RC-B019/020 manual override/selected-device roles do not establish host
  dispatch. RC-B021 default instrument lock-on-arm, hand status RC-B022 and
  unsupported locking RC-B023 must remain capability/context qualified. These
  observations do not resolve existing REQ-MIDI-USER-007/008 host/bank unknowns.
- RC-B026/027 adds setup/feedback context to routing's existing Remote roles.
  Incoming indicator RC-B028 cannot prove mapped-target response or feedback.
- RC-B031..034 names None/Pick-Up/Value Scaling in current documentation. Existing
  released numeric laws/precision and exact-target label/default assumptions
  stay unchanged. Source smooth/1:1 wording is no new curve or error tolerance.
- RC-B036/037 supports general browser columns/mode visibility, edit/invert/delete
  entrypoints and instant-map exclusion. Rack Macro laws stay with racks; Undo,
  target ownership restoration and held-input cleanup remain unresolved.
- RC-B045..057 and RC-B063..067 describe note/absolute/relative input roles and
  numeric thresholds. Those thresholds are retained context, not new acceptance
  outputs. Manual assignment route, switch grammar, radio quantization, pitch bend,
  high-resolution pairing and parameter display/gain conversion remain U here.
- RC-B060..062 uses UI-family words including Twos Complement, whereas existing
  exact configuration tokens include the literal Compliment spelling. No direct
  family-to-token association or complete UI list is inferred. Auto-detection and
  acceleration are documentary suggestions, without classifier success bounds.
- RC-B070..077 provides relative strip entrypoints; exact navigation/scene number,
  empty/boundary behavior and cancel deadlines are not supplied. Existing scene
  selection/launch/cancel law is linked, not reauthored.
- RC-B079 warns that Clip View mappings can affect selected/multiselected clips;
  it recommends relative controllers, not guaranteed smoothness. Panel rendering
  and selection remain Clip View's. RC-B082..090 KEY mapping cannot establish
  global shortcuts, Computer MIDI Keyboard, IME/text/plugin precedence or repeats.

Root owns canonical question-register integration. Required local questions are
retained as five U requirements and concrete null probes, rather than choosing a
law from another input route or silently narrowing the product denominator.

## Freeze, coverage and remaining evidence

{len(requirements)} requirements = {len(rows)} D12 +5 U;
{len(cases)} cases = {len(rows)} documentary roles +{len(cases)-len(rows)} U probes.
All target outputs/comparisons are null/U/unexecuted; only visible browser/control
predicates have documentary proposals. Signal/event/numeric/timing/protocol
outputs are null as well. [Fixtures]({base}fixtures.json) are finite future
recipes, not supplied sources/results. Compound branch, automation/transport/
sample-rate, saved-state migration, malformed/cancel/undo/failure/recovery/teardown
and every controller's actual protocol remain partial or unknown.

[Owner pins]({base}owner-pins.json) retain existing canonical/release bytes;
all {len(release_manifest['files'])} midi-config-v4 payload hashes were independently
checked, without editing the release. [Snapshots and manifest]({base}manifest-author-r1.json)
freeze the reviewable packet. Read-only validation checks source extraction,
IDs/cases/nulls/guards, exact browser equality, links, pins and untracked whitespace.
Run `python3 -B analysis/ableton-live-12.4.3/full-spec-v1/remote-control-workflows/validate.py`.
Separate semantic review is required. Shared catalogs/coverage/plan/questions/log
are integrated by root; this packet closes no entire UI/controller family.
'''
specpath, respath = ROOT / 'wiki/specs/remote-control-workflows.md', ROOT / 'wiki/research/remote-control-workflows.md'
assert not (P / 'manifest-author-r1.json').exists(), 'Never rewrite a frozen author revision'
specpath.write_text(spec)
respath.write_text(research)
(P / 'spec-r1.md').write_text(spec)
(P / 'research-r1.md').write_text(research)
print(json.dumps(counts, indent=2))
