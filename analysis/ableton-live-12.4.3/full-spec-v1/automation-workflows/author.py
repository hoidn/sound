"""Analyst-only documentary catalog and canonical snapshot builder; no runtime."""
from pathlib import Path
from collections import Counter
import hashlib
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
assert not (P / 'manifest-author-r1.json').exists(), 'Frozen packet must not be regenerated'
requirements, cases = [], []


def dump(name, value):
    (P / name).write_text(json.dumps(value, indent=2) + '\n')


def add(title, refs, contract, action, kind='state', section='Automation'):
    number = len(requirements) + 1
    rid, cid = f'REQ-AUTO-WF-{number:03d}', f'AW-{number:03d}'
    blocks = []
    for ref in refs.split():
        name = 'automation' if ref[0] == 'A' else 'clip-envelopes'
        blocks.append(f'{name}:B{int(ref[1:]):03d}')
    requirements.append(dict(id=rid, title=title, section=section, provenance='D12',
                             target_applicability='U', contract=contract, source_blocks=blocks))
    case(cid, rid, title, kind, action, contract, blocks)


def case(cid, rid, title, kind, action, claim, blocks):
    visible = kind in ('state', 'control', 'boundary') and not '-U-' in rid
    cases.append(dict(id=cid, requirements=[rid], title=title, kind=kind,
                      preconditions=['F0', 'positive-path-gate'], setup_and_action=action,
                      source_blocks=blocks, source_claim=claim,
                      documentary_expected=claim if visible else None,
                      documentary_comparator='Compare only named visible control/state predicates; compound signal/timing clauses remain ungraded, with no numerical or runtime parity proof.' if visible else None,
                      expected=None, comparison=None, target_grade='U', executed=False))


add('Automation and modulation indicators', 'A3 A4',
    'An automated control has a theme-dependent colored indicator, typically red; blue denotes modulation. Session automation is available as a clip envelope, while Arrangement automation is displayed in track lanes.',
    'F-EDITOR: compare an actually automated control, one with modulation and a nonautomated control; inspect indicators and the Session editor versus Arrangement lane. Retain theme; no exact pixel/color metric.')
add('Session automation recording eligibility', 'A8 A9 A10',
    'Session clip automation recording uses Automation Arm, eligible armed tracks and Session Record. Record Session automation in: All Tracks permits recording into all playing Session clips regardless of track arm, including automation overdub without recording MIDI notes.',
    'F-REC: compare armed A and unarmed B with independently playing nonempty clips; enable Automation Arm and Session Record, move an eligible device parameter. In reset trial select All Tracks and repeat with B unarmed. Inspect recorded envelopes; no event codec, event density or negative arm law.')
add('Session recording stop controls', 'A11 A12',
    'Session Record can stop automation recording while playback continues; Stop ends transport and recording. Recorded clip automation is viewed/edited in the Envelope Editor.',
    'F-REC: start a positive Session automation pass with moving parameter and explicit running transport. In separate copies press Session Record or Stop; inspect recording/transport state and editor envelope. Transition timing remains U.')
add('Session transfer and performance recording', 'A7 A13',
    'Session-to-Arrangement recording stores parameter changes as track automation, not Session clip automation, and can record tempo changes. Copying automated Session clips to Arrangement also copies automation as track automation; Session performance recording includes existing clip automation alongside live parameter changes.',
    'F-REC/F-VIEWS: use a Session clip with a visible changing envelope, active output and a second independently changed parameter. In separate trials copy it to Arrangement and record its performance through the recording owner. Inspect envelope ownership; flattening, event merge and scheduling remain U.')
add('Arrangement automation recording', 'A15 A16 A18',
    'With Automation Arm enabled, Arrangement automation recording applies to all tracks. Arrangement Record is described as starting transport/recording by default and records tempo, mixer and device adjustments into track lanes; this is no unconditional transport-start guarantee.',
    'F-REC: on A/B with explicit arm states, enable Automation Arm and Arrangement Record, confirm actual running transport, change a mixer/device parameter and tempo separately. Inspect new track envelopes without deriving arm refusal, point spacing or tempo precedence.')
add('Arrangement recording stop controls', 'A17',
    'Arrangement Record can stop recording while playback continues; the adjacent Stop button ends both transport and recording.',
    'F-REC: positively record a changing Arrangement parameter, then use each stop control on separate copies. Observe record/play state only, not sample-aligned stop or event ownership.')
add('Overwrite and Session touch/latch contexts', 'A20 A21',
    'Adjusting an already automated parameter during recording replaces its recorded adjustments. For Session overwrite, mouse release returns to prior automation, whereas MIDI knobs/faders hold the new setting until clip/loop end. A first Session automation pass uses the hold behavior regardless of input method. No overwrite interval or controller protocol law is supplied.',
    'F-REC/F-MAPPING: compare an existing two-level Session envelope with a first pass in separate copies; record mouse drag/release and separately an actually accepted controller knob. Keep Automation Arm/record, active playback, nonzero parameter excursion and paired prior-envelope baseline. Capture values/events around release and loop end without a timing oracle.', 'timing')
add('Manual override presentation', 'A23 A24 A25',
    'With recording off, manually changing an automated parameter overrides its automation, turns its automation indicator gray and activates Re-Enable Automation. This is distinct from overwriting recorded data.',
    'F-OVERRIDE: two parameters have independently changing active envelopes and positive source/output. Confirm recording off, change only the first manually, inspect gray/inactive indication and active Re-Enable button. Record envelope inventory separately; no stored override law.')
add('Global and per-parameter re-enable', 'A26 A27',
    'The Control Bar Re-Enable Automation button restores all overridden automation; a parameter context-menu command restores only that parameter. The active button indicates at least one overridden automated parameter.',
    'F-OVERRIDE: override two previously active envelopes while not recording. Use the first parameter menu and then the global button on separate/reset copies; inspect active/overridden indicators for both. Value return timing and sound remain U.')
add('Session relaunch re-enable role', 'A27',
    'Relaunching a Session clip that contains automation is another documented way to re-enable overridden automation. This does not identify every affected target, launch boundary or Arrangement-return transition.',
    'F-OVERRIDE/F-VIEWS: with a positively active Session envelope, recording off, override its target then relaunch that automated clip using the launch owner. Retain competing Arrangement state and indicators; observe control/audio return without a launch or reset-time oracle.', 'timing')
add('Session envelope selection', 'A31 A32 A33',
    'The Session Envelope Editor Automation toggle and Device/Control choosers select a target envelope; device/mixer and MIDI Ctrl entries are described. Automated controls/devices have indicators; an unautomated selected control appears as a dashed line at its current value. Actual entries depend on clip type.',
    'F-EDITOR: select a MIDI clip, enable Automation, choose mixer/device/MIDI Ctrl as actually offered, and compare automated and untouched controls. Audio-specific entries are scoped by the clip-type requirement below.')
add('Session adjusted-envelope filter', 'A34 A35 A36',
    'Show Adjusted Envelopes Only combines Session Device/Control choices into an Automated Control chooser; Show All Envelopes restores the full choices. An unautomated envelope already displayed remains displayed when filtering is enabled.',
    'F-EDITOR: display unautomated X alongside automated Y in the chooser, enable the adjusted-only filter, inspect combined chooser and retained X display, then restore All.')
add('Stacked Session control focus', 'A36',
    'With Envelope Editor open and Clip/Device Views stacked, clicking a track device or mixer control displays its envelope, including unautomated controls. Adjusted-only filtering prevents newly opening an unautomated envelope this way.',
    'F-EDITOR: explicitly stack views and open editor; click untouched X and automated Y with filter off, then filter on in reset trial. Grade selection/display only, retaining the already-displayed exception.')
add('Arrangement Automation Mode and choosers', 'A38 A39 A40 A41',
    'Automation Mode button or A opens main track automation lanes. Device/Automation Control select envelopes; None hides the envelope and empties the control chooser. Automated entries have indicators and an untouched selected parameter is dashed.',
    'F-EDITOR: Arrangement focus, computer MIDI keyboard/text focus cleared under keyboard owner, toggle Mode with button and offered key; select device/mixer then None. Compare untouched and automated targets without general shortcut-dispatch assumptions.')
add('Arrangement filters and focus commands', 'A42 A43 A44',
    'Show Automated Parameters Only combines the Arrangement choosers; Show All Parameters restores them. In Automation Mode, clicking a control or its Show Automation/Show Automation in New Lane commands selects its envelope. With automated-only filtering, untouched controls cannot newly open and those menu options are disabled/unavailable; an already displayed untouched envelope remains.',
    'F-EDITOR: compare automated Y and untouched X with filter off/on; invoke both menu options on reset copies and inspect Mode/focus/availability. Include X displayed before enabling filter.')
add('Add lane and main-lane None', 'A45',
    'Add Automation Lane moves the main envelope into an additional lane and sets main Device to None. Selecting a new main target permits another lane; Add is absent while None is selected.',
    'F-EDITOR: main Y selected, Add, inspect new lane/main None/Add absence, select X and inspect Add returning. No data deletion or target duplication is inferred.')
add('Additional lane visibility and order', 'A46 A47 A48',
    'A main-lane toggle hides/shows additional lanes; when main Device is None, hiding promotes the top additional lane to main. Additional lanes can be reordered by drag; arrows navigate lanes or show/hide from main context.',
    'F-EDITOR: create Y/Z lanes, reorder them, set main None and hide/show; inspect promoted target. Use focused lane arrows only through existing keyboard context.')
add('Existing lane focus and duplicate limit', 'A49',
    'Choosing a parameter already in an additional lane focuses that lane. Ctrl-click Windows/Option-click macOS on Add creates a duplicate of the main envelope, with up to two such duplicates documented.',
    'F-EDITOR: create Y additional lane and select Y again; then on reset copy put X in main and attempt first, second and third modified Add. Inspect focus/lane count only; duplicates are views, not additional recorded sources.')
add('All lanes and lane removal', 'A50 A51 A54 A55 A56',
    'Alt Windows/Cmd macOS Add or Add Lane for Each Automated Envelope adds lanes for automated parameters. Remove applies to selected additional lanes; modified Remove also removes lanes below. Main-lane Add and additional-lane Remove are available in the corresponding header menus.',
    'F-EDITOR: A has two automated targets plus untouched X; use all-lanes action. In separate copies remove one, a discontiguous header selection, a Shift range and selected-plus-below. Inspect lanes separately from retained envelopes.')
add('Breakpoint insertion', 'A59 A61 A63',
    'Clicking a selected control’s dashed envelope line inserts a breakpoint and makes it solid. Click-drag sets the new point value, Shift refines the adjustment, and double-click away from the line inserts there. Hover values and Add Value context entry support a chosen displayed value.',
    'F-EDITOR: untouched admitted continuous parameter; use click-line, click-drag, Shift drag, off-line double-click and hover/Add Value on reset copies. Inspect visible points/values, no event Id or float-serialization law.')
add('Breakpoint grid and display', 'A62 A63 A80 A87',
    'Inserted/moved breakpoints snap to grid, with Alt Windows/Cmd macOS bypass. Hover/drag exposes point values; segment hover/drag shows the closest breakpoint’s value. Shift horizontal drag constrains the horizontal axis and Shift vertical drag refines value adjustment.',
    'F-EDITOR: choose known visible grid and three separated points. Compare snap/bypass and horizontal/vertical Shift drags; inspect nearest-point tooltip. No hidden grid arithmetic, tie policy or pixel tolerance.')
add('Discrete envelope presentation', 'A64 A74',
    'Discrete controls such as toggles/radio choices display stepped rather than diagonal automation and permit only the square inserted shape.',
    'F-EDITOR: independently offered Bool/choice target and continuous positive control, insert separated points and inspect shape options. This supplies no Enum numeric mapping or playback interpolation.')
add('Draw Mode and snapping', 'A67 A68 A69',
    'Draw Mode is toggled through Options, Control Bar or B; holding B temporarily enables it when off. Drawing creates grid-width steps by default; grid size and Snap to Grid or Alt Windows/Cmd macOS bypass alter drawing alignment.',
    'F-EDITOR: confirmed editor focus and keyboard context, Draw off then button/menu/key/hold in separate trials; draw across nonempty selection at two offered grids and with snap bypass. Inspect envelope shape only, no smoothing kernel.')
add('Shape insertion extent', 'A71 A72',
    'Context-menu automation shapes can be inserted at a marker or time selection; selection width determines horizontal extent and parameter range the vertical extent, while no selection uses current grid width. Source text names sine, triangle, sawtooth, inverse sawtooth, square, ramps and ADSR.',
    'F-EDITOR: admitted continuous control, proper nonempty selection then marker-only trial at known grid. Insert each text-named offered family on reset copies and inspect displayed extent; figures and numerical waveform construction are not oracles.')
add('Waveform and ramp surroundings', 'A73',
    'Inserted waveforms retain their shape irrespective of surrounding values, whereas ramps depend on values on either side of the insertion selection. Exact ramp coefficients, clipping and boundary events are unknown.',
    'F-EDITOR: two distinct admitted surrounding values and positive visible selection; compare one waveform and one ramp under reversed surroundings on reset copies. Grade visible contextual role only.')
add('Breakpoint deletion and selection', 'A79 A81 A82',
    'Points can be dragged; clicking a breakpoint deletes it and joins its neighbors by a new segment. Background drag selects multiple points, whose point drag moves the selection and whose context Delete removes selected points.',
    'F-EDITOR: three separated interior points with neighbors retained; delete middle, then select/move/delete multiple in reset copies. Record visible point membership, not interpolation or duplicate-time handling.')
add('Segment movement and selection edges', 'A83 A84',
    'Dragging near a segment moves it; Shift-click/hold then releasing Shift is an alternative selection gesture. Moving a segment inside a time selection inserts points at the edges, and moving it outside inserts further edge points. Fine vertical and constrained horizontal drags are documented.',
    'F-EDITOR: proper interior selection on a diagonal envelope with outside neighbors; move segment inside and across the selection boundary in separate copies. Inspect inserted boundary points without sample-time or stored-point law.')
add('Drop overwrites and drag preview', 'A85',
    'Dropping a dragged point/segment onto existing breakpoints overwrites them; while dragging before drop, existing parts are not permanently overwritten. This says nothing about Escape rollback or transaction atomicity.',
    'F-EDITOR: point group with an independently retained destination group; drag over it, inspect preview before release, then drop. Record source/destination points; cancel and Undo have separate U probes.')
add('Diagonal curve gesture', 'A86',
    'Alt Windows/Option macOS segment drag adds a curve only to diagonal segments; modified double-click changes curved to straight. Numeric curve controls and runtime interpolation remain with the finite envelope/mix owners.',
    'F-EDITOR: compare admitted diagonal, horizontal and discrete segments using documented modifier drag, then straighten a curved diagonal. Grade offered visible editing only, no polynomial reconstruction.')
add('Exact value editing', 'A88',
    'Edit Value on a point/segment accepts a typed value. With multiple selected points, the edited point takes that value and the others move relatively. Admission, saturation and error grammar are unknown.',
    'F-EDITOR: use two distinct admitted displayed values on an interior continuous target with headroom. Edit one, then a multi-selection; inspect visible relative movement without extrapolating beyond range or parser rules.')
add('Stretch and skew handles', 'A91 A92 A93 A94 A95',
    'Time-selection handles transform the selected envelope: top/bottom centers stretch vertically, side centers horizontally and corners skew. Outline snaps with horizontal bypass; Shift refines vertical stretch and Alt Windows/Option macOS mirrors opposite handles. Dragging over outside points removes them.',
    'F-EDITOR: known interior selection and retained outside points; separately drag vertical/horizontal/corner handles, Shift and mirrored modifiers, then cross an outside point. Inspect preview/points only; no affine formula or clipping law.')
add('Simplify Envelope command', 'A97',
    'Simplify Envelope on a selected segment reduces unnecessary breakpoints using straight/curved segments. The source supplies no error tolerance, optimum algorithm or guaranteed reduction for every input.',
    'F-EDITOR: select a dense admitted envelope then a sparse one in separate trials and invoke Simplify Envelope. Inspect points/visible shape without waveform equality or an exact count oracle.')
add('Delete Automation parameter action', 'A99',
    'Parameter Delete Automation context action or Ctrl-Backspace Windows/Cmd-Delete macOS deletes that parameter’s automation, removes its indicator and returns the value to its default. This does not identify a numeric default or general clip-editor shortcut dispatch.',
    'F-EDITOR: retain an actually automated eligible parameter, its offered default identity and another automated target; select first parameter, invoke menu then shortcut on reset copies. Compare indicator/envelope removal and visible default, no guessed numeric value.')
add('Clear command scopes', 'A100 A101 A102 A103 A104',
    'Clear Envelope removes selected-parameter envelope; lane-header Clear All Envelopes of… removes automated envelopes for the selected device; Clear All Envelopes removes automation throughout the Set. Partial removal uses point/segment editing instead.',
    'F-EDITOR: multiple parameters in D, a second device, another track and clip envelope. On disposable copies invoke each offered scope command and inventory envelopes separately. Source scope is documentary, not Undo or durable deletion proof.')
add('Tempo envelope and mapped range', 'A107 A108 A109',
    'Tempo can be recorded during Arrangement recording or edited in Main’s Mixer/Song Tempo lane. Tempo Minimum/Maximum Range controls set its displayed BPM range and also the value range of a MIDI controller assigned to tempo. Numeric mapping, global tempo precedence and clock response remain separate.',
    'F-REC/F-MAPPING: positive running Arrangement recording, Automation Arm on; change tempo, inspect Main lane. Then edit admitted visible min/max range and an actually assigned control in reset trial. Observe offered range without borrowing controller normalization or signal-clock arithmetic.', 'control')
add('Lock Envelopes entry point', 'A111',
    'Lock Envelopes is available through its toggle or Options menu. Arrangement REQ-ARRANGEMENT-032 retains the lock-on clip-move contract; the source’s broader lock-off move statement does not close that owner’s partial-selection and transformation unknowns.',
    'F-EDITOR: use toggle and Options on reset copies with a visible Arrangement envelope and nonempty clip. Inspect lock state; route clip movement comparisons to the existing Arrangement owner.')
add('Envelope Edit commands and target transfer', 'A113 A114',
    'Cut, Copy, Duplicate and Delete on an automation-lane time selection affect only selected envelope portions rather than clip content or other portions; multi-lane selections apply to the included envelopes. Segments can be copied across time and parameter targets, without a conversion rule for unrelated controls.',
    'F-EDITOR: two lanes with separate envelope/clip before-inventory. Apply each edit to an interior selection then a multi-lane selection on reset copies; paste between two known admitted targets. Inspect visible scope; cross-domain values, endpoints and conversion remain U.')


def clip(title, refs, contract, action, kind='state'):
    add(title, refs, contract, action, kind, 'Clip envelopes')


clip('Clip-type chooser vocabulary', 'C4 C5 C6 C7 C8',
     'Clip Envelopes tab has Device and Control choosers; audio clips expose Clip sample controls, track effects and mixer, while MIDI clips expose MIDI Ctrl, track devices and mixer. Altered envelopes have adjacent indicators and an adjusted-only filter.',
     'F-EDITOR: separately open owned audio and MIDI clips with known devices; inspect offered categories and altered/untouched target indicators. Do not generalize the Automation chapter’s generic MIDI Ctrl wording to audio clips.')
clip('Session versus Arrangement envelope kinds', 'C9 C10 C38 C40 C41',
     'Session clips offer Automation/Modulation toggles; Arrangement Clip View exposes modulation only and track automation uses lanes. Automation specifies a control’s absolute value while modulation influences its current/automated value. Both kinds can coexist, with separate indicators and knob position/ring presentation; no universal combiner formula follows.',
     'F-EDITOR: compare Session and Arrangement clips, add an actually supported automation and modulation envelope to one Session target, inspect toggles and separate indicators. Keep source active and amounts nonzero; numeric combination is ungraded.')
clip('Clear clip envelope entry', 'C11',
     'Clear Envelope in the Clip View envelope context menu resets the selected clip envelope to its default. Exact default values and the source’s shortcut-to-menu wording remain unresolved; parameter Delete Automation is a distinct context.',
     'F-EDITOR: known altered clip envelope and separately retained offered default state; use context-menu Clear Envelope and inspect selected envelope. Do not use the ambiguous shortcut as a positive oracle.')
clip('MIDI Envelope Auto-Reset option', 'C12',
     'MIDI Envelope Auto-Reset is offered through Options or the Sample Editor context menu and is described as resetting certain MIDI control messages at new clip start. Which messages/values, delivery time and persistence are unknown.',
     'F-MIDI: known nonempty MIDI clip and separately positive controller destination; inspect option availability/state in each documented context. Message capture is an ungraded future probe; no all-controller reset is assumed.', 'control')
clip('Non-destructive sample modulation', 'C17 C18',
     'Clip-envelope modulation is non-destructive to the referenced sample on disk; clips can reuse one sample with different envelopes. Render/resample/consolidate are separate ways to commit audio, owned by their workflow pages.',
     'F-AUDIO: retain identical owned source hash shared by two clips with distinct active envelopes and positive output, edit one envelope and observe source identity/audio separately. Export/consolidation is not executed and no codec or waveform oracle is supplied.', 'signal')
clip('Audio transposition envelope context', 'C20 C21 C22 C23 C25',
     'The audio Clip/Transposition workflow uses Warp on and supports Draw Mode or fine breakpoint edits. The source describes additive influence bounded by the Transpose range and Warp-mode/granularity-dependent response; no frequency law, warp kernel, smoothing or numeric event conversion is added.',
     'F-AUDIO: positively playing warped owned pitched sample, nonzero admitted Transpose base and envelope; inspect Clip/Transposition and fine edits, compare accepted Warp contexts in reset trials. Retain no DSP/timing expectation.', 'signal')
clip('Audio Clip Gain modulation role', 'C27 C28',
     'Clip/Gain envelope can shape sample level. Its influence is relative to Clip Gain, can attenuate to silence and cannot exceed that absolute setting; this documentary role supplies no calibrated gain-domain formula.',
     'F-AUDIO: independently positive source and nonzero Clip Gain, active nonzero envelope; compare upper setting and attenuation in reset copies using paired dry/active baselines. No waveform gain ratio or silence floor oracle.', 'signal')
clip('Sample Offset eligibility', 'C30 C31',
     'Clip/Sample Offset modulation is available only in Beats Warp Mode and is edited as a clip envelope. The chapter’s beat-scrambling examples do not establish random, resampling or analytic cut-and-splice behavior.',
     'F-AUDIO: nonempty independently positive rhythmic sample, Warp on; compare Beats and another actually offered mode with nonzero offset envelope retained for the Beats positive trial. Grade visible eligibility only.')
clip('Track volume stage and indicator', 'C43 C44',
     'Clip Gain and Track Volume are distinct envelope targets; Track Volume modulation affects the mixer’s post-effect gain stage and a dot below its slider indicates the modulated setting. No stored-unit or signal multiplier law is restated.',
     'F-AUDIO: enabled audible effect, nonzero Track Volume and distinct Clip Gain modulation; inspect target identities and slider dot while manually changing the base. Numerical output remains U.', 'control')
clip('Send modulation ceiling role', 'C45',
     'Send modulation is relative to the Send control: it cannot open the send beyond the knob and can reduce it to minus infinity. This does not extend finite send coefficients or define event conversion.',
     'F-AUDIO: nonzero send to independently positive nonmuted wet return with correct monitoring, active nonzero envelope and a paired positive return baseline. Compare attenuation/upper role without a numerical or silence-threshold oracle.', 'signal')
clip('Pan modulation contextual range', 'C47',
     'Pan modulation range depends on the base knob: center permits the full stereo span, movement toward an edge reduces available influence, and full left is described as no-effect. This is not a pan law or formula for every mode.',
     'F-AUDIO: independently positive distinguishable stereo path, admitted nonzero pan envelope; establish centered positive modulation, then an intermediate base and full-left control on reset copies. Confirm active envelope and output before no-effect observation; no channel equality metric.', 'signal')
clip('Device modulation relative role', 'C49',
     'Clip modulation acts on devices in that clip’s track and changes controls relative to their current setting rather than defining preset values. Per-device eligible targets and combination arithmetic require their owners/evidence.',
     'F-AUDIO: an actually eligible device target with active section, nonzero base/amount and independently positive processed output; compare two admitted base settings while keeping envelope. No unsupported target or preset replacement is inferred.', 'signal')
clip('MIDI controller envelope editing', 'C51 C52 C53',
     'MIDI Ctrl/Control selects listed controller envelopes for creation/editing with steps or points, including imported/recorded data indicated by adjacent LEDs. Most controller numbers through 119 are described as supported; this is not every number or a MIDI codec. Receiver conventions may differ from names such as Pitch Bend or Pan.',
     'F-MIDI: independently valid MIDI clip and known listed controller, edit a nonzero changing envelope, inspect imported/recorded indicator in separately accepted fixtures. Receiver path/data semantics remain U.', 'control')
clip('Envelope-local region controls', 'C56 C59 C60',
     'Unlinking gives the selected envelope its own local region/loop controls and colored loop braces. Its Loop switch is independent of the sample’s Loop switch, allowing a one-shot envelope while the sample continues looping.',
     'F-LOOP: positive warped looping sample and a known active envelope; unlink that envelope and toggle its Loop off/on, inspect sample Loop unchanged. Playback duration/phase/reset remains a separate ungraded observation.')
clip('Independent envelope lengths and start markers', 'C67 C68 C69 C70 C71',
     'Each unlinked envelope can have its own loop length, extended by braces or numeric controls, including non-bar-aligned lengths. Its start marker identifies where envelope playback begins on clip start; start/end and braces obey the zoom-adaptive grid. No clip-time equation or sample-rounded extent follows.',
     'F-LOOP: positive sample loop and two admitted unlinked envelopes with distinct nonzero lengths and starts; inspect controls at two zoom levels and an offered non-bar length. Retain phase/clock observations ungraded.', 'timing')
clip('Local-loop rhythmic role', 'C73 C75 C76',
     'Local envelope loops may be shorter or longer than source playback and can be shaped with handles/shapes. The source describes tempo-relative repetition and grid-hidden independent endpoints; it does not specify clock arithmetic, rate limits or a free-running oscillator implementation.',
     'F-LOOP: independently positive long source and short envelope, then short source and long envelope on reset copies. Hide grid and adjust admitted local endpoints. Observe repeated control/audio influence with no period, beat/sample or synchronization comparator.', 'timing')
clip('Linked envelope Warp interaction', 'C78',
     'In Linked mode, moving a clip Warp Marker lengthens/shortens its envelope accordingly, and Warp Markers can be adjusted within the envelope editor. Exact marker/envelope transformation and interpolation stay unknown or with the finite Warp owner.',
     'F-LOOP: positive warped clip, Linked envelope and two independently identified markers; move an interior marker via ordinary editor then envelope editor in reset copies. Inspect visible relative envelope change; no exact time conversion or waveform oracle.')

unknowns = [
    ('RUNTIME', 'Runtime, timebase and finite-law boundary', 'Editing/recording/override/re-enable/runtime outcomes of REQ-AUTOMATION-ENVELOPES-013 remain U. Point generation/Ids, stored transforms/LockEnvelope meaning, modulation normalization, clip timebase/start/loop/Warp, scheduler/ramp alignment and untraced mix-graph owners are not settled by this packet.', 'A20 A21 A27 C38 C78'),
    ('SOURCE', 'Unresolved source contexts', 'Clip Clear Envelope shortcut wording, parameter Delete Automation shortcut dispatch, and sample-replacement all-settings wording versus the existing equal-length Warp-marker predicate need context/build evidence. MIDI auto-reset message set/values and exact copy-across-domain conversions are unknown.', 'A99 A114 C11 C12 C36'),
    ('MAPPING', 'Mapping and automation ownership', 'Controller delivery/takeover, key or MIDI mapping versus automation/override/recording, MPE/controller identity, tempo mapping ranges versus normalization and simultaneous input precedence have no new runtime law.', 'A21 A109 C53'),
    ('BOUNDARY', 'Unspecified edit and record boundaries', 'Empty selections/lanes/clip slots, ineligible targets, equal-time points, endpoints, negative or extreme text/ranges, multi-clip/group/return/Main combinations and crossing/collapsed transforms have no general refusal/repair law.', ''),
    ('STATE', 'History, persistence and cancellation', 'Undo/redo grouping, gesture cancellation, override/arming/filter/selection persistence, save/reopen/duplicate/transfer and automation edit ownership are unknown beyond visible documentary roles. No rollback or event serialization is inferred.', ''),
    ('CLOCK', 'Transport, rates and engine transitions', 'Stop/start/seek/loop/tempo/meter/sync changes during record/edit/re-enable, rate/block changes, engine restart and concurrent processing retain unknown event ordering, phase and audio results.', ''),
    ('LOSS', 'Source and target loss', 'Device/parameter/track/clip/media/controller disappearance during active envelopes or pending edits, unavailable ports and malformed admitted documents have no new diagnostics, recovery or silence oracle.', ''),
    ('TEARDOWN', 'Teardown and concurrent workflows', 'Closing/replacing Set, quitting, losing engine/controller connection or concurrently editing/removing targets while recording or transforming has no established completion, cleanup or transaction outcome.', '')
]
for suffix, title, contract, refs in unknowns:
    rid = f'REQ-AUTO-WF-U-{suffix}'
    blocks = [(('automation' if r[0] == 'A' else 'clip-envelopes') + f':B{int(r[1:]):03d}') for r in refs.split()]
    requirements.append(dict(id=rid, title=title, section='Unknown obligations', provenance='U', target_applicability='U', contract=contract, source_blocks=blocks))

probes = [
 ('RUNTIME', 'record-events', 'recording', 'F-REC: record an independently changing accepted parameter over beats 1-4 and a second loop with Automation Arm/appropriate record and actual running transport confirmed. Retain resulting envelope/event inventory only through understood format; no point thinning, Id, sentinel, overwrite-bound or codec oracle.'),
 ('RUNTIME', 'value-return', 'timing', 'F-OVERRIDE: two independently active envelopes, recording off, positive output; compare per-target re-enable, global re-enable and automated clip relaunch on reset copies. Capture indicator/value/audio return around events, without assuming immediate jumps, ramps, clip-time reset or Back to Arrangement equivalence.'),
 ('RUNTIME', 'arrangement-return', 'transport', 'F-VIEWS: establish positive Arrangement envelope and a different Session envelope; launch, stop Session and request Back to Arrangement in separate trials using existing owners. Keep nonzero source/output and explicit transport; record ownership without extending mix-graph A8 beyond its finite scope.'),
 ('SOURCE', 'clear-shortcut', 'boundary', 'F-EDITOR: on reset copies focus parameter, Session Envelope Editor and Arrangement lane separately with a retained positive altered envelope, then use documented platform deletion shortcut or menu. Record whether menu/direct clear/delete is offered; local source wording supplies no dispatch oracle.'),
 ('SOURCE', 'replacement', 'source-loss', 'F-AUDIO: two owned positive samples with known equal duration, then a different duration in separate trials. Retain envelope and Warp-marker before-inventory, replace sample via existing CV041 owner, compare identities/settings. Do not adopt the clip chapter all-settings wording as marker preservation for unequal samples.'),
 ('SOURCE', 'midi-auto-reset', 'midi-output', 'F-MIDI: with independently accepted controller destination and positive nonzero envelope messages, compare Auto-Reset off/on while launching a different clip. Capture actual messages only with available path; unknown message set, values and timing stay null.'),
 ('MAPPING', 'mapped-overwrite', 'mapping', 'F-MAPPING/F-REC: establish accepted unique MIDI assignment and takeover preference using mapping owner, positive nonzero parameter excursion and active recording first. Compare mouse, MIDI knob and key input separately with recording on/off. No takeover, latch interval or universal key-recording rule is borrowed.'),
 ('MAPPING', 'tempo-range', 'mapping', 'F-MAPPING: independently active nonzero tempo automation, known accepted assigned controller and actual min/max controls; compare two admitted display ranges while transport runs then stops. Retain control/value traces without controller normalization, numeric range repair or global-clock oracle.'),
 ('BOUNDARY', 'inactive-controls', 'negative', 'F-REC/F-AUDIO: first establish recorded automation and active eligible target with nonzero output/base/depth. Then separately disable Automation Arm/record or relevant section/route and edit one parameter. Compare paired positive trial; inactive/silent paths cannot prove no-effect or a universal refusal.'),
 ('BOUNDARY', 'empty-and-edges', 'boundary', 'F-EDITOR: compare a proper nonempty time selection and three separated valid points against empty lane, marker only, exact envelope/clip/loop edge and equal-time candidates in reset copies. Use offered edits only; no reader normalization, event sorting, refusal or half-open endpoint law.'),
 ('BOUNDARY', 'transform-limits', 'boundary', 'F-EDITOR: independently valid interior transform first, then drag handles across each other, collapse width/height or cross outside neighbors in separate copies. Record admitted state, clipping and point loss without formulas or a guaranteed repair.'),
 ('BOUNDARY', 'target-contexts', 'boundary', 'F-REC: start from positive ordinary-track automation, then inspect actually offered targets on group, return, Main and multi-clip selections separately. Preserve valid positive source/receiver paths; broad all-target support is not inferred from practically-all wording.'),
 ('STATE', 'undo-redo', 'undo', 'F-EDITOR/F-REC: on separate copies perform insertion, drag/drop overwrite, clear, transform, recording pass and override/re-enable. Undo then Redo with complete point/control/route before-inventory. No grouping, file or override restoration oracle.'),
 ('STATE', 'cancel', 'cancel', 'F-EDITOR: begin point/segment/handle drag or typed value edit, then use actually offered Escape/cancel before commit; separately dismiss shape/clear menu. Retain preview versus committed state, no atomic rollback law.'),
 ('STATE', 'save-reopen', 'persistence', 'F-REC/F-OVERRIDE: save/reopen owned Set after record, unlinked edits, override and re-enable separately, with source/controller/target present then absent in copies. Inventory envelopes, link/loop state and visible arm/filter/override state; storage/evaluator owners do not imply UI persistence.'),
 ('CLOCK', 'transport-loop', 'transport', 'F-LOOP/F-REC: positive active automation with explicit record/arm and source/output; stop/start, seek, loop, change 120 to 90 BPM and meter on separate copies. Capture point/control traces without expected release, reset, beat conversion or event race order.'),
 ('CLOCK', 'rate-engine', 'sample-rate', 'F-REC: repeat positive pass at actually supported 44.1/48/96 kHz and 64/512-frame blocks, then request rate/block change or engine restart while recording on separate copies. Retain pre-change baseline; no sample-aligned equality, event count or smoothing invariant.'),
 ('LOSS', 'target-removal', 'source-loss', 'F-AUDIO/F-REC: independently active nonzero source/envelope/output first; remove target device, clip or track separately while recording/playing or while a transform is pending. Inventory references, other paths and diagnostics without guessed rebinding, silence or cleanup.'),
 ('LOSS', 'source-controller-loss', 'source-loss', 'F-MAPPING/F-AUDIO: retain positive source and accepted controller delivery, then make only owned media or available controller port absent in separate copies during automation. Record output/record state and recovery; no absent capability is simulated.'),
 ('LOSS', 'malformed', 'malformed', 'F-EDITOR: on owned copies enter abc, NaN or out-of-domain numeric text only in an offered editable control; a malformed saved envelope is used only through independently understood storage-owner format. No hidden parser/schema or all-errors refusal is invented.'),
 ('TEARDOWN', 'close-active', 'teardown', 'F-REC/F-LOOP: while positive automation recording, unlinked playback or a pending transform is active, close/replace Set or quit through offered controls in separate copies. Record prompts, retained state and output without completion, flush, silence or resource deadline.'),
 ('TEARDOWN', 'concurrent-edit', 'concurrency', 'F-REC: independently changing accepted parameter and positive output with running transport; attempt an offered envelope edit, target move/removal or clear during record, separately stop and retry. Record eligibility and resulting inventory, no snapshot-time or transaction ordering law.')
]
for suffix, label, kind, action in probes:
    rid = f'REQ-AUTO-WF-U-{suffix}'
    requirement = next(r for r in requirements if r['id'] == rid)
    case(f'AW-U-{label.upper()}', rid, label.replace('-', ' ').capitalize(), kind, action, None, requirement['source_blocks'])

assert len({r['id'] for r in requirements}) == len(requirements)
assert len({c['id'] for c in cases}) == len(cases)
dump('requirements.json', requirements)
dump('cases.json', cases)
dump('counts.json', dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)), cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)), documentary_oracles=sum(c['documentary_expected'] is not None for c in cases), null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases), retained_blocks=192, target_oracles=0))

owners = ['automation-envelopes.md', 'mix-graph.md', 'mixer-values.md', 'recording-comping.md', 'session-view-workflows.md', 'clip-view-workflows.md', 'arrangement-editing.md', 'keyboard-navigation.md', 'midi-user-mapping.md', 'warp-markers.md']
pins = []
for path in [ROOT / 'wiki/specs' / n for n in owners] + [ROOT / 'handoff/automation-envelopes-v2' / n for n in ['README.md', 'spec.md', 'manifest.json']]:
    data = path.read_bytes()
    pins.append(dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), purpose='Existing authority unchanged; no new runtime evidence'))
dump('existing-authority-pins.json', pins)
dump('fixtures.json', {
    'F0': 'Future investigation only: disposable valid editable Set; exact build/platform, focus/theme, views, selection, recording/arm/overdub, per-track Session/Arrangement ownership, mapping/takeover, target eligibility, tempo/meter, grid, loop/link/start and source/route before-state retained. Baseline choices 120 BPM, 4/4, 48 kHz are scenario choices, not defaults. No original application or fixture execution is supplied.',
    'F-EDITOR': 'Known nonempty editable audio and MIDI clips and Arrangement lanes; independently offered continuous target X, automated target Y, second automated target Z and a supported discrete target. At least three separated admitted interior points with visible neighbors; use two distinct displayed values with headroom. Exact values/grid/selection and clip content retained before each separate action. Text focus, computer MIDI keyboard and mappings recorded before shortcut dispatch.',
    'F-REC': 'Future positive source with eligible device/mixer target, accepted nonzero parameter excursion, enabled active relevant section, nonzero audible output and independently changing automation baseline. Explicit transport running plus Automation Arm and appropriate Session/Arrangement Record; track arm and Record Session automation in preference chosen deliberately. Distinguish first pass from overwrite and audio/MIDI note recording from automation. Positive record inventory required before negative gates.',
    'F-OVERRIDE': 'Two independently active changing envelopes with nonzero source/output; relevant target/base/depth nonzero and enabled. Actual recording off before manual override; preserve envelopes and per-target/global indicators before override/re-enable. Clip relaunch and Back to Arrangement are distinct controls and owner contexts.',
    'F-VIEWS': 'Same shared track with nonempty distinct Session/Arrangement material and separate visible changing envelopes. Retain actual playback ownership, launch/quantization, track record/arm state and nonmuted output. Visible focus is not source ownership; playback and Arrangement owner prerequisites must be met independently.',
    'F-AUDIO': 'Two future test-owned independently readable, distinguishable nonzero samples and a MIDI/instrument source with known positive output. Retain exact bytes/hashes, duration/rate/channels and clip processing. Accepted active device, mixer/send/wet path, nonzero gain/base/amount and separately nonmuted return with correct Monitor/arm/clip state before modulation/no-effect tests. Establish pan center positive modulation before edge probe, nonzero Clip Gain before attenuation and active send/return before send exclusion. No media is created or renderer run.',
    'F-LOOP': 'Future positive warped looping sample, one Linked envelope and two separately admitted Unlinked local regions with distinct nonzero lengths and starts. Retain actual sample/envelope Loop controls, Warp Mode/markers, grid/zoom and explicit transport. Nonzero target/base/depth and active envelope output established before comparing shorter/longer regions; no period or sample-time equation is assumed.',
    'F-MAPPING': 'Open prerequisite: independently accepted controller/port and unique assigned eligible target under MIDI mapping owner, known takeover and controller message identity, positive nonzero excursion/delivery. No controller/hardware capability or fake port is created. Mouse, key and MIDI inputs are separate; missing route remains U.',
    'F-MIDI': 'Future valid MIDI clip with known listed controller and independently accepted nonzero input/output destination. Actual message identity, clip launch and Auto-Reset state retained; receiver convention and codec are separate from menu labels. No MIDI bytes, hardware or message monitor is supplied.',
    'positive-path-gate': 'For every signal/timing/negative probe require a nonempty eligible source, actual automated/modulated target, enabled relevant path/section, nonzero base/depth/amount/gain/send where relevant, correct receiver Monitor/arm/clip state and nonmuted positive source/wet return/output baseline. Recording needs accepted target/excursion, explicit Automation Arm/record and running transport; compare matched positive active/recorded trial before disabling a control. Zero input, absent controller, muted return, unsupported target or inactive automation cannot prove no-effect or a pass. Visibility-only cases retain valid named before-state but prove no sound.',
    'not_provided': ['No ALS/audio/MIDI or retained application results', 'No accepted controller/driver/hardware inventory', 'No numerical timebase, interpolation, combiner, RNG or smoothing law', 'No signal/timing comparator, tolerance or deadline']
})

base = '../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/'
header = '''---
id: SPEC-AUTOMATION-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Version 12 documentary applicability U
---

# Automation recording, editing and clip-envelope workflows

## Scope and provenance

This partial F-04/F-09 draft owns documentary automation record/overwrite,
override/re-enable presentation, lane/editor gestures and local clip-envelope
workflows. [Research](../research/automation-workflows.md) retains source contexts;
the [coverage design](../research/full-live-specification-design.md) governs closure.
It does not close the whole feature or supply a released implementation input.

**D12** means text in two retained official Version 12 chapters, captured
2026-10-19. Every new runtime clause has **exact-12.4.3 applicability U**. All
target expected/comparison fields are null, all grades U and all cases unexecuted.
Visible-control documentary predicates are proposals only. Signal, timing,
recorded-event and wholly unknown probes have null documentary expectations and
comparators; their source claim is retained separately. No UI case closes a
compound timing/audio clause, and no source wording supplies numerical tolerances.

## Existing authorities and exclusions

[Automation envelopes r5](automation-envelopes.md) retains stored containers,
targets/events, load/save checks and its logic evaluator. In particular,
[REQ-AUTOMATION-ENVELOPES-013](automation-envelopes.md#req-automation-envelopes-013--editing-override-recording-and-undo)
remains unknown: this manual packet does not settle its runtime, recorded point/Id,
override persistence, Undo, stored transforms or LockEnvelope meaning. The public
Lock Envelopes command is not a proof of that stored field's meaning.
[automation-envelopes-v2](../../handoff/automation-envelopes-v2/README.md) remains an
unchanged 21-case partial storage release; its exclusions and conditional clauses
are not broadened. No original evaluator or comparator is executed here.

[Mix graph](mix-graph.md) owns its finite playback envelope selection, point-list
evaluation, ramps and units, preserving untraced owners/conversions and A3/A6/A8
conditions. Logic evaluation, engine playback and a visible value are distinct.
Session clip timebase/start/loop/Warp and composed manual/modulation behavior remain
unproven. [Mixer values](mixer-values.md) retains fader, send and pan domains and
coefficients. No user-interface percentage is imported as stored normalization.

[Arrangement editing](arrangement-editing.md) retains clip edits, Back to Arrangement
and REQ032 lock-on movement. The new lock entry point below does not duplicate
that law or settle its lock-off/partial-selection gaps. [Recording](recording-comping.md)
retains note/audio record, count-in, punch and Session performance recording;
this page owns only its automation-specific eligibility and envelope roles.
[Session](session-view-workflows.md), [Clip View](clip-view-workflows.md),
[launch](clip-launch.md), [playback](playback-core.md) and
[transport](transport-state.md) keep their selection, source ownership, launch,
loop and clock contracts. Re-Enable Automation is distinct from Back to Arrangement.

[Keyboard/navigation](keyboard-navigation.md) retains focus and keyboard breakpoint
operations. [MIDI user mapping](midi-user-mapping.md), [MPE](mpe-workflows.md) and
[tuning](tuning-systems.md) retain their bounded input/transform contracts. Ordinary
audio sample transposition is not MPE per-note expression. [Warp markers](warp-markers.md)
retains finite marker/time conversion; Linked envelope editing supplies no new
warp kernel. [Racks](device-racks.md), [project/media](project-media-workflows.md),
[media files](media-file-workflows.md), [export](audio-video-export.md),
[Bounce/Freeze](bounce-freeze-workflows.md) and [Set structure](live-set-structure.md)
retain common device/preset/commit/file and storage behavior. Sample replacement
remains with Clip View REQ041; the chapter's all-settings description is not an
unqualified new Warp-marker preservation law.

## Preconditions and observation

Use the [future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/automation-workflows/fixtures.json),
not guessed constructor states. Record accepted target and values, track/clip/view,
actual playback ownership, explicit arm/record/transport, focus/mapping, envelope
kind/link/local region, grid/zoom and source/route before-state. Each named gesture,
platform entry point and first-pass/overwrite branch needs its own retained result.
Only actually offered controls/formats may be used. Missing prerequisites remain U.

Audio/no-effect probes require active changing automation or modulation, enabled
eligible target/section, nonzero base/depth/amount/gain/send, nonempty source,
nonmuted output/wet return and a separately retained positive baseline. Correct
receiver Monitor/arm/clip state is explicit. A silent source, inactive envelope,
zero send or absent controller cannot prove exclusion/no-effect. Recording probes
also require positive admitted movement, Automation Arm/appropriate record and
explicit running transport, with a paired working pass before a negative gate.

Envelope points, automation/modulation indicators, lane layout, arming and audible
output are separate observables. Templates/examples do not supply signal fixtures,
point-thinning, interpolation, scaling, normalization, MIDI bytes, envelope-time
equations, RNG, rate invariants, CPU performance, atomicity or error messages.
Figures and linked help/PDF bytes have not been inspected.

## Requirements
'''
body = header
for section in ['Automation', 'Clip envelopes', 'Unknown obligations']:
    body += f'\n## {section}\n'
    for r in requirements:
        if r['section'] != section:
            continue
        body += f"\n### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
        if r['source_blocks']:
            links = []
            for ref in r['source_blocks']:
                name = ref.split(':')[0]
                links.append(f'[{ref}]({base}manual-{name}-blocks.json)')
            body += 'Evidence/context: ' + ', '.join(links) + '.\n'
        else:
            body += 'Evidence: unsupported outcome; ungraded investigation obligation.\n'
counts = json.loads((P / 'counts.json').read_text())
body += f'''
## Finite case index

The [{len(cases)} cases]({base}cases.json) map exactly to the
[{len(requirements)} requirements]({base}requirements.json): {counts['requirement_grades']['D12']} D12
and eight U. {counts['documentary_oracles']} cases have only visible documentary
predicates; {counts['null_documentary_oracles']} have null documentary oracles.
All target oracles are null/U and all cases unexecuted. This is partial coverage;
the index does not claim every target/gesture combination, platform or lifecycle
branch is closed. Each case carries exact finite action, fixture gates, source
locators and a separate source_claim field, including signal/timing cases.

| Case | Requirement | Kind | Action focus |
| --- | --- | --- | --- |
'''
for c in cases:
    body += f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |\n"
body += f'''
## Unresolved contexts and closure

[Research source questions](../research/automation-workflows.md#source-context-questions)
preserve the deletion shortcut and replacement contexts. They remain U rather than
globalized UI or marker laws. MIDI Auto-Reset names no complete message set or
reset values. Theme colors and slightly different chooser wording do not prove
exact label aliases or build parity. Example pitch/gain/offset/fade/LFO anecdotes
remain source context rather than waveform recipes or numerical engine laws.

Recording/overwrite point production, input ownership, return-to-automation timing,
envelope/clip-time conversion, automation/modulation combination, undo/cancel,
save/reopen, controller/target/media loss, transport/rate changes and teardown need
bounded evidence. The [whole-product applicability question](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
remains open. No original/native/extracted-original, candidate, controller,
hardware, codec or audio/MIDI runtime is run for this draft.

## Analyst evidence appendix

[Sources]({base}sources.json) pin URLs/final URLs, UTC capture, major edition,
immutable HTML sizes/SHA256. [Authority pins]({base}existing-authority-pins.json)
retain ten existing canonical identities and three immutable automation release
identities unchanged. [Counts]({base}counts.json), [manifest]({base}manifest-author-r1.json)
and the read-only [validator]({base}validate.py) freeze the packet.

| Source | Retained scope | Text view |
| --- | --- | --- |
| D12-AUTOMATION | §26.1–26.9.3, 114 numbered chapter blocks, HTML280–832 | [Automation]({base}manual-automation.txt) |
| D12-CLIP-ENVELOPES | §27.1–27.5.5, 78 numbered chapter blocks, HTML280–460 | [Clip envelopes]({base}manual-clip-envelopes.txt) |

Exact block records preserve original HTML lines, anchors and heading context.
No figures, linked tutorials, native data or private formats supply new laws.
Shared indexes, coverage, questions and log integration belong to the root analyst.
'''
(ROOT / 'wiki/specs/automation-workflows.md').write_text(body)
(P / 'spec-r1.md').write_text(body)

research = f'''---
id: RESEARCH-AUTOMATION-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary target parity unknown
specs: SPEC-AUTOMATION-WORKFLOWS
---

# Automation workflow evidence

## Question and boundary

Which observable record/edit/override and clip-envelope workflows are documented
outside the existing finite storage/evaluator contract? The
[canonical draft](../specs/automation-workflows.md) owns the new partial clauses;
the [coverage plan](full-live-specification-plan.md) and
[coverage design](full-live-specification-design.md) govern F-04/F-09 closure.
This is an analyst context. No original function/application, candidate,
hardware/controller, audio renderer or implementation was executed.

The [existing research](automation-envelopes.md) and
[r5 spec](../specs/automation-envelopes.md) distinguish logic evaluation from
engine playback and preserve REQ013 runtime unknowns. The unchanged
[automation-envelopes-v2 release](../../handoff/automation-envelopes-v2/README.md)
has 21 finite storage cases, excludes REQ004/010/011/013, and is not a workflow or
live-recording oracle. Mix-graph owner/time offset assumptions and finite fader
laws remain unchanged. New manual clauses do not silently replace unknowns.

## Retained evidence

No existing exact chapter capture was found in retained source catalogs. The
inventory [manual TOC](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
identifies §26 Automation and §27 Clip Envelopes with exact official URLs. Two
bounded HTML captures were retained once, including URL/final URL, UTC, edition,
size and SHA in [sources]({base}sources.json). They prove Version 12 publication
text, not the command surface of 12.4.3. All new target applicability is U.

'''
for s in json.loads((P / 'sources.json').read_text()):
    research += f"- {s['id']}: [{s['path']}]({base}{s['path']}), {s['bytes']} bytes, SHA256 `{s['sha256']}`, captured `{s['captured_utc']}`. [Official chapter]({s['url']}).\n"
research += f'''
The pure [parser]({base}source_parser.py) extracts headings, paragraphs and list
items only within numbered chapter content, stopping before manual navigation.
114 Automation plus 78 Clip Envelopes blocks retain text, original HTML line,
anchor, section and heading context. Image captions/figure text are not parsed
or visually inspected. Original bytes remain immutable; normalized text is derived.

## Source-supported interpretation

Automation A008–A018 distinguishes Session arm/preference/record gating from
Arrangement all-track recording and the two stop controls. A007/A013 distinguishes
clip-based writing from Session performance transfer to track envelopes. This
does not settle point generation, overwrite edges, automation transfer merge or
clock timing. A020/A021 distinguishes first pass, existing Session overwrite,
mouse release and accepted MIDI controller hold; these are ungraded timing roles,
not generalized controller/takeover laws or signal comparators.

A023–A027 distinguishes nonrecording manual override from recording overwrite,
per-target/global re-enable and Session relaunch. Back to Arrangement retains its
existing owner and is not equated with re-enable. A031–A057 supplies chooser,
filter/focus, None, lane visibility/ordering/duplication/removal contexts. The two
duplicate-lane limit is a documented view limit, not multiple automation sources.

A059–A104 supplies mouse/draw/shape/point/segment/transform/simplify and delete
workflow. Simplify's word optimal does not specify an optimization metric or
error bound. Shape names and source extent descriptions are not sampled kernels.
Discrete presentation is not a new Bool/Enum evaluator. A107–A114 gives tempo
display/mapped range and selected-envelope edit scope. Lock-on movement is already
Arrangement REQ032; no duplicate law or lock-off transformation is adopted.

Clip C004–C012 distinguishes audio/MIDI chooser entries, Session kinds and
Arrangement modulation-only Clip View. C017–C034 describes non-destructive audio,
Warp-dependent transposition, gain and Beats-only Sample Offset. The examples'
numeric ranges, imagined tape head and escalation/fade anecdotes are retained
context, not new audio, resampling or timing recipes. C038–C049 distinguishes
absolute automation from relative modulation and clip versus post-effect volume,
send and pan roles; no universal percentage arithmetic or normalization follows.
Active nonzero input/base/envelope/wet paths and paired positive baselines are
required before any ceiling/edge/no-effect investigation.

C051–C054 offers listed MIDI controller editing but says most numbers through
119, not every number, and cautions that receivers need not honor names. C056–C078
describes local unlinked loop/region independence, start/zoom-grid contexts and
Linked Warp response without proving clip-time equations, phase restart, frame
rounding or generated envelope values. The audio sample-pitch example is not
MPE per-note behavior. Generic MIDI/MPE, Warp, clock and recording owners remain.

## Source context questions

| Local ID | Exact context | Treatment |
| --- | --- | --- |
| Q-AW-001 | automation:B099 describes parameter Delete Automation with direct Ctrl-Backspace/Cmd-Delete. clip-envelopes:B011 uses wording about those keys opening a context menu followed by Clear Envelope. | Preserve parameter versus editor/context distinction and both texts. Adopt explicit context-menu Clear only for clip editor; shortcut dispatch remains U. No contradiction or global alias is asserted without same control/focus/preconditions/build. |
| Q-AW-002 | clip-envelopes:B036 says all clip settings including envelopes remain on sample replacement, whereas existing Clip View REQ041/CV:B172–B173 conditions Warp-marker retention on equal sample length. | Sample replacement remains Clip View owned. All-settings is not broadened into unequal-length marker preservation; both source contexts and exact-target state remain U. Future equal/different-duration probes retain envelope/marker inventories separately. |
| Q-AW-003 | clip-envelopes:B012 names certain MIDI auto-reset messages without their identities/values; B053 says most controller numbers up to119; automation:B109 connects displayed tempo range to assigned-controller range. | Retain option/role only; no complete reset table, number set, message bytes, takeover, normalization or tempo-clock law. |

Automation B003 qualifies colors by theme, while Clip B038/B041 uses red/blue
language. The draft retains the theme qualifier and functional distinction, not
a fixed pixel metric. Chooser labels also vary slightly across the two chapters;
the texts do not establish exact aliases for every target build/localization.

## Cases, prerequisites and limits

[Fixtures]({base}fixtures.json) are future scenarios, not retained ALS/WAV/MIDI or
accepted host/controller setups. They require valid nonempty source, actual
eligible target and recording context, enabled relevant section, nonzero
base/amount/depth/gain/send, nonmuted positive output/wet return, explicit running
transport for recording and matched positive path before negative gates. Correct
receiver Monitor/arm/clip state and Session/Arrangement ownership are independent.
Missing capability or failed baseline is U, never a no-effect or exclusion pass.

The packet has {len(requirements)} requirements ({counts['requirement_grades']['D12']} D12/eight U)
and {len(cases)} proposed cases: {counts['documentary_oracles']} visible documentary
predicates and {counts['null_documentary_oracles']} null documentary oracles. All target
expected/comparison fields are null/U and unexecuted. Signal/timing/MIDI/controller
probes retain source_claim separately, never as an outcome comparator. Compound
clauses require individual retained branches before coverage closure.

Unknown probes cover record output, return/ownership, ambiguous source contexts,
mapping, empty/equal-time/transform boundaries, inactive gates, Undo/Redo, cancel,
save/reopen, transport/rates, target/controller/media loss, admitted malformed
inputs, concurrency and teardown. No arbitrary hidden command, format, fake
hardware, samplerate invariance, universal latency or atomic rollback is invented.

## Freeze and checks

[Authority pins]({base}existing-authority-pins.json) identify ten pre-existing
specs and three immutable automation release identities unchanged. The
[manifest]({base}manifest-author-r1.json) freezes HTML, derivatives, catalogs,
fixtures, analyst author/parser/validator and both canonical snapshots. The
read-only [validator]({base}validate.py) reproduces 192 blocks, checks all source
and authority hashes/full finite release payload pins, exact requirement/case/
browser ID sets, null oracles, snapshots, local links/anchors and untracked-aware
whitespace. It prints stdout and never creates or rewrites a sealed result.

Independent semantic review is required. No whole feature, release readiness,
candidate or application compatibility follows from packet integrity. Root owns
shared index/coverage/question/log integration; broader applicability remains
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).
'''
(ROOT / 'wiki/research/automation-workflows.md').write_text(research)
(P / 'research-r1.md').write_text(research)
print(json.dumps(json.loads((P / 'counts.json').read_text()), indent=2))
