"""Author new workspace predicates; route the rest of Concepts to existing owners."""
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
blocks={r['id']:r for r in json.loads((P/'source-blocks.json').read_text())}
DATA=[
('Control Bar grouping','The chapter groups Control Bar roles into nine named sections: Browser Options; Tempo Settings and Metronome; Scale Settings; Follow and Arrangement Position; Transport Controls; Automation and Capture MIDI; Arrangement Loop Settings; MIDI and CPU Settings; View Selector. This is a documentary grouping, not pixel/order/visibility geometry or a new definition of the domain controls.',list(range(4,15)),'On an identified supported workspace inspect named Control Bar roles and actually offered controls, retaining visible configuration. Use the linked owners for their transport/recording/mapping/CPU/routing operations.','control'),
('Shared scale selection and future clips','Control Bar scale controls reflect the selected clip and offer Scale Mode, Root Note and Scale Name. With no clip selected, chosen scale settings apply to subsequently created clips. This adds the global selection/default context to Clip View properties; accepted scale lists, data codec, preference scope and numerical pitch transforms remain with existing owners or unknown.',[8,74,75,76],'In an owned Set use two clips with independently admitted distinct scale settings and select each, inspecting Control Bar. Separately clear clip selection, explicitly choose an accepted root/scale and create a new clip through an existing supported creation workflow.','state'),
('Scale controls with multiple clips','Control Bar Scale controls can turn Scale Mode on/off or set the same scale for multiple selected clips. Mixed audio/MIDI selections, incompatible tuning, empty-slot versus existing-clip propagation and merge/display precedence remain unknown. This does not redefine perclip Scale or a device retuning law.',[76],'Select two valid owned clips with independently distinguishable scale states, set an offered shared scale or toggle Scale Mode in separate reset copies, then inspect each. Keep nonselected clip C as a control; mixed/ineligible selections remain ungraded.','state'),
('Status messages and update context','Status Bar can display error information and available-release updates, the latter in the documented Automatic Updates enabled context. Error wording, severity, retention, availability checks, update protocol/consent and whether other notifications appear are unknown; delivery owns update operations.',[16],'Inspect Status Bar after a separately admitted reversible error or known available update notice in an owned future setup with explicit update setting. Do not trigger an installation or invent a failure message for this proposal.','control'),
('Selected-note Status Bar details','With a selected MIDI Note Editor note, Status Bar provides its location, pitch, velocity and probability details. Numeric encoding, pitch naming, formatting, rounding, multi-selection aggregation and update deadlines remain unknown; note values/editing remain MIDI-owner contracts.',[17],'In an owned MIDI clip select two independently admitted notes with distinguishable location/pitch/velocity/probability in separate trials. Inspect the named Status Bar fields without prescribing spelling, units or exact rendered text.','control'),
('Insert-marker hover feedback','Hovering an actually offered insert marker in the documented Session/Arrangement context displays its location in Status Bar. Which Session/editor marker is intended, exact location grammar/precision, hidden-marker handling and focus/hover timing remain unknown; no marker coordinate formula is inferred.',[17],'For each actually offered view/editor insert-marker context, retain known insert position and hover it with Status Bar visible. If no corresponding marker exists in that context the prerequisite is missing, not a passing negative case.','control'),
('Two-window view swap','With two Live windows and Use Tab Key to Navigate disabled, Tab swaps Session and Arrangement between the windows. Existing keyboard-navigation owns the one-window Tab switch, preference-conditioned focus traversal and platform view shortcuts; this adds only the paired-window swap context.',[34],'Use an independently supported two-window workspace, record which window shows Session/Arrangement and focus, explicitly disable Tab navigation, then press Tab. Repeat with navigation enabled as a separate control through its existing owner.','state'),
('View switching versus playing state','The chapter describes Session/Arrangement view switching during playback/recording as a UI change that does not change the currently playing clips. It does not specify sample continuity, a no-glitch deadline, record event ordering or arbitrary UI-command independence; transport/launch/record owners retain those laws.',[35,36],'Establish independently active positive nonzero clip playback and separately eligible recording through existing owners; switch views using admitted controls and retain playing-clip/transport history and output. No timing or signal comparator is supplied.','timing'),
('Track-title Device View entry','Double-clicking a track title opens Device View for its device chain. This adds an entry gesture, not device insertion/classification/routing or clip/device stack behavior. Generic device focus remains with keyboard-navigation and stacking/Clip View selection with Clip View.',[63],'Select an owned track with an independently known supported device chain, double-click its title and inspect Device View. Separately try an empty track only as an ungraded context; do not infer insertion or output.','control'),
]
GAPS={
 'SCALE':('Scale propagation and folding contexts','Global no-selection/future-clip/empty-slot propagation, mixed-selection state, Fold to Scale exceptions, scale-aware device/MIDI-tool conversion and tuning interactions remain unresolved beyond linked owners.',[
 ('SCALE-HISTORY','Set distinct explicit scales on selected existing clips, empty slots and no-selection workspace in separate histories, then create/select further clips. Retain transitions without assuming all future selections are overwritten.'),
 ('SCALE-MIXED','Use compatible/incompatible tuning and mixed audio/MIDI/empty selections separately; inspect offered global scale controls and actual perclip state without a universal propagation or rejection rule.'),
 ('FOLD-CONTEXT','Compare Concepts only-scale-rows wording with MIDI owner retained out-of-scale-note exception using independently admitted notes inside/outside the active scale. Preserve both source contexts, no replacement rule.')]),
 'FEEDBACK':('Status and control feedback limits','Error/update, marker/note field grammar, multi-selection/hidden/focus contexts, warnings and inaccessible or unavailable controls have no complete feedback oracle.',[
 ('STATUS-CONTEXT','Use no note, multiple notes, text-edit focus and hidden Status Bar in separate future contexts, inspecting available feedback without assuming a blank/stale value policy.'),
 ('MARKER-CONTEXT','Identify offered Session/Arrangement/editor insert markers and their coordinate systems, then test boundary/outside/hidden markers only where actually admitted. No universal precise-location format is defined.')]),
 'WINDOWS':('Workspace layout and window outcomes','Window creation/closure, selected-view conflicts, minimization, displays/scaling, unavailable shortcuts, focus restoration and layout persistence remain required unknowns.',[
 ('WINDOW-BOUNDARY','Compare one/two actually supported windows, closed/hidden selected views, alternate focus, text editor and modal/plugin contexts with explicit Tab preference; retain dispatch without a global shortcut guarantee.'),
 ('DISPLAY','In a separately supported owned display setup move windows, change scale or remove a monitor; inspect fallback and active view roles without pixel/geometry or timing predictions.'),
 ('WORKSPACE-PERSISTENCE','Save/reopen two owned Sets and restart application separately with explicit views/global scale/no-selection state; distinguish perSet from global/window retention without presuming scope.')]),
 'LIFECYCLE':('Workspace failures and lifecycle','Undo/redo/cancel, invalid/unsupported settings, object/media/device loss, audio-rate/engine/transport changes, concurrent controls and teardown remain unknown.',[
 ('UNDO','Change scale, selected clips and an offered workspace control separately; invoke Undo/Redo only where available and inspect actual command/state boundaries.'),
 ('CANCEL','Cancel an actually offered setting/selection/dialog or drag gesture separately; record retained state and missing cancellation support without an atomicity assumption.'),
 ('LOSS','After an active positive owned clip/device and selection baseline, remove only that owned object or media and inspect global scale/status/view feedback; no fallback or error text is assumed.'),
 ('RATE','Change an admitted sample rate/buffer or engine configuration while an owned clip plays; retain actual positive output and views, with no timing/audio-invariance oracle.'),
 ('ORDER','Switch views/global scale and explicit selection around accepted start/stop/record actions on separate copies; record order without inventing scheduler, queued input or sample deadlines.'),
 ('TEARDOWN','Close a window, clip, track, Set or application during an offered view/scale gesture in separate trials; retain prompts, focus, pending state and saved files.')])}
reqs,cases=[],[]
for i,(title,contract,refs,action,kind) in enumerate(DATA,1):
 rid=f'REQ-WORKSPACE-CONTROL-{i:03d}'
 evidence=[dict(block=f'CONCEPT-B{n:03d}',anchor=blocks[f'CONCEPT-B{n:03d}']['anchor'],html_line=blocks[f'CONCEPT-B{n:03d}']['html_line']) for n in refs]
 reqs.append(dict(id=rid,title=title,contract=contract,strength='D12',target_applicability='U',evidence=evidence))
 visible=kind in {'control','state'}
 cases.append(dict(id=f'WORKSPACE-{i:03d}',requirements=[rid],kind=kind,fixture='fixtures.json#WORKSPACE-OWNED',setup_and_action=action,source_claim=contract,documentary_expected=contract if visible else None,documentary_comparator='Named visible control/status/view/selection relationship only; no pixel, numeric, text grammar, signal or timing grade.' if visible else None,expected=None,comparison=None,target_grade='U',executed=False,evidence=evidence))
for group,(title,contract,probes) in GAPS.items():
 rid='REQ-WORKSPACE-CONTROL-U-'+group;reqs.append(dict(id=rid,title=title,contract=contract,strength='U',target_applicability='U',evidence=[]))
 for suffix,action in probes:cases.append(dict(id='WORKSPACE-U-'+suffix,requirements=[rid],kind=suffix.lower(),fixture='fixtures.json#WORKSPACE-OWNED',setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[]))
assert len(reqs)==13 and len(cases)==23 and len({c['id'] for c in cases})==23
def save(name,value):
 raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode() if not isinstance(value,str) else value.encode();p=P/name
 assert not p.exists() or p.read_bytes()==raw,name
 p.write_bytes(raw)
save('requirements.json',reqs);save('cases.json',cases)
helper=P.parent/'session-workflows/capture.py'
save('dependencies.json',[dict(path=str(helper.relative_to(ROOT)),bytes=helper.stat().st_size,sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),role='existing analyst chapter_content parser, no original code')])
save('fixtures.json',dict(id='WORKSPACE-OWNED',status='future owned setups only; no original UI/media/output supplied',setup='Owned editable Set with three clips A/B/C, independently admitted distinct clip scale settings and MIDI notes with distinct location/pitch/velocity/probability; explicit no-selection and empty-slot histories. Record exact build/OS/edition, keyboard/focus/Tab preference, single/two-window availability, current view/layout/global scale/transport/update settings. Use independently admitted positive active clips/device chain/nonmuted nonzero audio and eligible recording through their canonical owners.',guard='Before a negative or unchanged-feedback trial independently establish relevant accepted controls/selection/context, valid source/device/note/marker and positive output. Absent marker, hidden view, missing second window, no selected clip, unavailable feature, zero input/gain or failed record gate leaves U. Do not create an unsupported error, marker coordinate or private format.',scope='Global UI predicates only. No actual UI/API/network/install/account/update/audio/hardware/candidate operation occurs; displayed status alone is not signal or timing proof.'))
front='---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
spec=front.format(id='SPEC-APPLICATION-WORKSPACE',type='spec',status='draft')+'''# Shared workspace controls and feedback

This partial F-08 contract adds Control Bar grouping/global scale-selection,
Status Bar feedback, paired-window view switching and track-title view entry
predicates. The [coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/application-workspace.md) owns sources and
owner routing. It is not a complete UI, layout, scale or source-chapter contract.

**D12/target-U:** current Version12 documentary roles only. All exact12.4.3
expected/comparison fields remain null/U/unexecuted. No UI, original function,
audio/MIDI/API, update/network, hardware or candidate ran. Figures were not
inspected. Timing/signal outputs are source_claim only, not graded oracles.

## Canonical owners

[Keyboard navigation](keyboard-navigation.md) owns focus/traversal, Tab preference,
single-window switching and platform shortcuts; this adds only paired-window
swap. [Clip View](clip-view-workflows.md) owns stacking and perclip properties;
[MIDI editing](midi-editing-tools.md) owns note/scale/folding values and operations.
This adds global selection/default context and Status Bar presentation only.
[Tuning](tuning-systems.md), [native MIDI effects](native-midi-effects.md),
[modulation](modulation-pitch-loop-devices.md) and [synthesis](synthesis-instruments.md)
retain actual scale-aware device/tuning roles, not a new pitch conversion here.

[Transport](transport-state.md), [launch](session-launch-workflows.md),
[recording](recording-comping.md), [automation](automation-workflows.md),
[Arrangement](arrangement-editing.md), [routing](routing-monitoring-latency.md),
[device hosting](bundled-device-hosting.md), [Browser](browser-workflows.md),
[projects](project-media-workflows.md), [media](media-file-workflows.md),
[export](audio-video-export.md), [settings](settings-learning-workflows.md),
[engine/resource](engine-resource-workflows.md) and [delivery](delivery-recovery-workflows.md)
retain their detailed controls/operations. Control Bar grouping and overview
examples neither duplicate their laws nor close the other Concepts sections.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/fixtures.json)
with explicit selection/preferences/focus/feature availability and positive
active source/output where relevant. Compound branches require individual
evidence; no single UI observation closes an error, output or lifecycle branch.

'''
for r in reqs:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
 if r['evidence']:spec+='Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact routes](#analysis-only-evidence).\n\n'
spec+='''## Source-context questions

**WORKSPACE-U-SCALE-HISTORY:** CONCEPT-B008 mentions subsequently created clips
or selected slots; B075 explicitly describes no-selection/future creation. This
does not establish that selecting any existing clip overwrites its scale.

**WORKSPACE-U-FOLD:** B077 describes only scale rows, while REQ-MIDI-EDIT-017
retains an out-of-scale-note visibility exception. Preserve overview/detailed
contexts; the existing owner remains authoritative for its partial scope.

**WORKSPACE-U-MARKER:** B017's Session/Arrangement insert-marker context needs
an actually offered marker/editor and coordinate-system match. No synthetic
marker, exact location grammar or absent-control rejection is inferred.

## Finite acceptance proposals

[23 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/cases.json)
cover9D12roles/14operational U probes for13requirements (9D12/4U). Eight
documentary visible-control/state proposals have named role expectations;
the timing case and all14U cases have null documentary outputs/comparators.
All23target outputs/comparisons are null/U/unexecuted; setups are future,
not retained UI/media or compatibility results.

## Analysis-only evidence

'''
source=json.loads((P/'source.json').read_text())
spec+=f'''Official [current Version12 Concepts]({source['url']}), captureUTC
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[exact HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/{source['file']}).
[125 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/source-blocks.json)
retain anchors/HTML lines; figures uninspected and patch applicability unknown.
The parser is pinned in dependencies.json. An earlier distinct Concepts capture
remains preserved in the Arrangement packet; it is not this byte identity and
is not silently replaced. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/requirements.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/manifest-author-r1.json)
freeze only the new predicates. Other chapter material is routed, not declared
specified completely or nonbehavioral from its overview title.
'''
research=front.format(id='RES-APPLICATION-WORKSPACE',type='research',status='current')+f'''# Workspace evidence and Concepts routing

The [canonical draft](../specs/application-workspace.md) follows the
[execution plan](full-live-specification-plan.md). Root read all125retained
Concepts blocks, using only distinct workspace predicates for new requirements;
generic operations remain with existing owners. No original application/function,
UI, API/Max, audio/MIDI, network/update/hardware or candidate ran.

## Exact source and ownership

Official [Version12 Concepts]({source['url']}), captureUTC
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[retained bytes](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/{source['file']}).
The current website names Version12 without an immutable patch revision;
all12.4.3 behavior/feature availability is U. The separately retained earlier
Arrangement Concepts capture has another byte identity and remains unchanged.
The pinned Session analyst parser extracts only chapter_content; all125blocks
retain heading anchor and HTML line, without inspected figures or glyph labels.

## Section routing and limits

| Captured section | Canonical behavior owner / unresolved scope |
| --- | --- |
|3.1Control Bar/3.2Status Bar| New workspace grouping/selection/feedback predicates only; detailed domain controls retain owners |
|3.3Browser/3.4Sound Similarity| Browser owner and remaining content/services packet; root adds no ranking/embedding or preview law |
|3.5Live Sets/3.21Saving and Exporting| Project/media, file/container/clip interchange and export owners; not a universal save/codec guarantee |
|3.6Arrangement and Session/3.7Tracks| Arrangement, Session, transport/launch, recording/comping; only paired-window/UI-only switch predicates added |
|3.8Audio and MIDI/3.9Audio Clips/3.10MIDI Clips| Routing, media, Clip View, MIDI editing and Warp; generic descriptions are not complete channel/file/DSP laws |
|3.11Devices/3.12Clip and Device View| Hosting, racks, devices, Clip View and keyboard focus; only track-title entry gesture added |
|3.13Scale Awareness| Global selection/default/multiclip predicates here; Clip View/MIDI/tuning/individual device owners retain properties and transformations |
|3.14Mixer/3.16Routing| Mix graph/mixer values and routing owners; stereo-chain/instrumentless mixer-control wording still needs percontext reconciliation |
|3.15Presets and Racks| Hosting/rack/project owners; presets do not imply every device/configuration accepted |
|3.17Recording/3.18Automation/3.19Clip Envelopes| Recording and automation workflow owners; no new timestamp/evaluator/envelope timebase law |
|3.20MIDI and Key Remote| Existing generic remote workflow and finite mapping owners; dedicated Push support reference does not close controller protocols |

Routing is not complete paragraph coverage or source-to-requirement acceptance.
The chapter remains in the880heading/708leaf denominator. New scope comprises
13requirements/23cases only; no source-derived global hardware, UI architecture,
unbounded device capacity, actual first-open default or perfect timing is inferred.

## Source questions

WORKSPACE-U-SCALE-HISTORY retains B008's selected-slot/future-clip wording and
B075's no-selection/future-creation context. Existing-clip selection does not
prove overwrite or persistence. WORKSPACE-U-FOLD retains B077's broad scale-row
description with existing REQ-MIDI-EDIT-017 out-of-scale-note exception, without
changing that sealed owner. WORKSPACE-U-MARKER retains B017's Session/editor
insert-marker applicability and unknown exact displayed coordinate grammar.

Audio clip scale selection does not prove a waveform change: Clip View retains
its scale-aware-device distinction. Multi-selection must inspect each clip with
a nonselected control, not infer every future clip/slot changed. View switching
is source-described UI-only but supplies no audio continuity/timing comparator.
Status Bar presence or messages prove neither actual update availability, signal
output, completed recording nor correct timestamps. Existing owners retain them.

## Finite cases and review

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/requirements.json)
contain9D12roles and4U obligations; [23cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/cases.json)
contain8visible documentary/15null proposals. All target outcomes/comparisons
are null/U/unexecuted. Future owned configurations/notes/markers/outputs are not
retained reference stimuli. The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-concepts/manifest-author-r1.json)
supports independent partial-scope review. Full scale propagation/formatting,
focus/window/display, undo/cancel/persistence/source-loss/rate/ordering/teardown
remain required unknowns. Root owns index/question/coverage/log integration.
'''
for name,text,canonical in [('spec-r1.md',spec,'wiki/specs/application-workspace.md'),('research-r1.md',research,'wiki/research/application-workspace.md')]:
 path=ROOT/canonical;assert not path.exists() or path.read_text()==text
 path.write_text(text);save(name,text)
print('13 requirements /23 cases authored; freeze/check separately')
