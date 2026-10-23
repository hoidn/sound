"""Author only new mixer interaction predicates from the retained Mixing capture."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
R=P.parent/'routing-monitoring'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text())
DATA=[
('Mixer visibility and components','Mixer controls are available from Session and Arrangement; the bottom-right mixer control shows/hides the section, with its adjacent menu controlling component visibility. Arrangement also offers Track Controls. No geometry, accessibility order or persistence law is supplied.',[3,4,5,6,7],'Use each admitted view with an independently available mixer; toggle section visibility and separately one actually offered component. Retain view/focus/configuration, using keyboard-navigation for traversal.','control'),
('Resizable meter presentation','Increasing mixer height reveals tick marks, numeric volume and resettable peak-level indicators; increased track width adds a decibel scale. These are presentation roles, with no pixel thresholds, calibrated detector or reset duration.',[16,17],'Independently admit compact and expanded mixer/track widths, resize and inspect the named controls; separately reset an actually exposed peak indicator after a known positive meter event.','control'),
('Selected mixer controls move together','With multiple tracks selected, editing one mixer control edits that control for the selected tracks. The source describes preserving existing knob/slider differences; coordinates/units, clamping, boundary interactions and exact transformations remain unknown. Existing mixer values own numeric laws.',[10,11,12,33],'Select two valid tracks with independently admitted distinguishable values and an unselected control track; separately edit volume, pan and Activator on reset copies, inspecting every selected/unselected state. No common numeric delta or boundary law is inferred.','state'),
('Pan mode menu and reset gestures','Pan context menu chooses Stereo versus Split Stereo presentation; Split offers independent left/right controls. Double-clicking Pan or clicking its triangle in the Session/Arrangement mixer resets to the described default. Numeric defaults, ramps and stereo processing remain with mixer values.',[11],'In each admitted mixer view inspect mode menu and corresponding controls, then separately use double-click and triangle reset after independently accepted nondefault pan values. Record resulting values with no new reset-number or signal comparator.','control'),
('Exclusive and multiselected Solo controls','Solo supports selected-track sets. Outside that multi-selection context, ordinary exclusivity is bypassed by Ctrl on Windows/Cmd on Mac or disabled Exclusive Solo preference. S invokes the solo shortcut in an eligible focus context owned by keyboard/remote control. Arbitrary routed graph muting remains separately owned.',[13],'Establish two eligible positive playing tracks plus an unselected control, then separately propose Solo with multi-selection, exclusive preference on/off and platform modifier on/off in admitted focus contexts. Retain actual solo flags and outputs separately; no arbitrary-graph signal oracle.','signal'),
('Nonadjacent track move context','Adjacent/nonadjacent selection is described with Shift/Ctrl-click. Dragging nonadjacent tracks collapses them together at drop; Ctrl+arrow moves without collapsing. This paragraph does not qualify Ctrl by platform, so no Cmd substitution or complete focus/ordering grammar is inferred.',[31,32],'Use four independently ordered tracks and select nonadjacent pair A/C; on reset copies propose drag-drop versus the actually admitted Ctrl+arrow command. Retain full selected/unselected order and focus without assuming a platform alias.','state'),
('Track numbering names','A leading # produces an automatically updated track number when moved; extra # characters add leading zeros. Prefix parsing beyond this example, numbering basis, interaction with renaming/history and exact rendered text remain unknown.',[29,30],'On independently admitted disposable tracks use one and multiple leading # markers, retain names/order, then move a track through its existing owner. Inspect numbering role; do not invent index basis, escaping or a full name grammar.','state'),
('Clip drag to a new track','Dragging one or multiple existing clips into empty space right of Session tracks or below Arrangement tracks creates a new track carrying those clips and the original track devices. This does not establish device-copy state, mappings, media bytes, source ownership or processing equivalence.',[27],'Use an owned clip and independently known device chain, propose drag to the actually offered blank creation area in separate views; retain new track, clip and device presence with original baseline and unselected control.','state'),
('Group creation and nesting','Group Tracks combines selected audio/MIDI tracks, including existing groups nested in a new group. Groups have mixer controls and can host audio effects but cannot contain clips. Group routing is owned by routing-monitoring; Session group slots remain their own owner.',[37,38,39],'Prepare two eligible audio/MIDI tracks and a separate existing group, propose Group Tracks in reset contexts, and inspect hierarchy/mixer/effect affordances. Do not infer all nesting depths, accepted nontrack objects or output sums.','state'),
('Group folding and Arrangement overview','Unfold Group shows/hides contained tracks; Arrangement groups show an overview of contained clips. Hidden tracks are not inferred inactive, and overview graphics are not playable group clips or timing/audio proof.',[40,42],'With independently admitted nonempty group and distinguishable child clips inspect folding in each view and Arrangement overview, retaining positive child playback separately from visibility.','control'),
('Group movement, deletion and ungrouping','Tracks may be dragged into/out of a group. Deleting a group deletes its contents; Ungroup Tracks restores individual tracks. Exact nested deletion/selection, Undo/media deletion and rerouting are not supplied.',[41],'Only in future disposable owned Sets with independent backups and known hierarchy, separately propose moving child in/out, deleting group and Ungroup Tracks on reset copies. Retain track/device/media identities and do not equate track deletion with source-file deletion.','state'),
('Group color applies to active view clips','Assign Track Color to Grouped Tracks and Clips applies group color to contained tracks and clips. In Session it affects Session clips; in Arrangement it affects Arrangement clips. Nested/selected subsets and palette equality remain unresolved.',[44,45],'Use a group with known child track and distinct Session/Arrangement clip colors; run the offered command separately in reset views and inspect both clip populations and a nonmember control. No hidden cross-view color rewrite is assumed.','state'),
('Group descendant solo indicator','A group Solo button appears half colored when a child track or nested group is soloed. The source supplies no exact RGB/pixel measure or complete status precedence.',[46],'With valid group/nested group and independently admitted Solo state on one descendant inspect group indicator; retain an unsoloed baseline and separate direct-group Solo context without guessing precedence.','control'),
('Return Send enable entrypoints','Return Send knobs are documented disabled by default, with Enable Send/Enable All Sends in their context menu. This is a control admission description; no identity with stored EnabledByUser or active-bit derivation, feedback stability or audible send is established.',[53],'On an independently eligible return with a working sender/receiver baseline inspect offered send controls, then propose Enable Send and Enable All Sends on separate reset copies. Retain flags and positive routed input separately; no raw ALS field or feedback signal oracle.','control'),
('Crossfader visibility and curve choice','Crossfader visibility is offered via Mixer Controls or the mixer-control menu; its context menu offers seven curves. The uninspected chart is not a numerical curve source. Existing mixer values retain names/codes/curve functions and assignment laws.',[58,59,60],'Independently admit mixer/crossfader availability, inspect show/hide and offered curve choices, then select an accepted curve on disposable state; retain visible choice without recreating coefficients from the chart.','control'),
('Crossfader mapping gesture contexts','The main slider and absolute left/right positions are separately assignable. The source describes a key assigned to any of left/center/right fields toggling absolute endpoints and two-field held-key press/release snap-back. Focus, repeat, overlapping input and restoration order remain unknown.',[61,62,63],'Using existing remote/key owner first establish valid accepted mappings and focused dispatch; separately propose one mapped field and two mapped fields with one key held as the other is pressed/released. Retain raw key/focus/value history with no endpoint-number, deadline or overlap law.','transform'),
('Crossfader automation entrypoints','Crossfader gestures can be recorded into Arrangement; track assignment edits use Mixer then X-Fade Assign in envelope choosers. This adds the editing entrypoint, not automation timebase, override, persistence or audio coefficients.',[69],'Establish working eligible Arrangement automation and track-envelope contexts through their existing owner; inspect Mixer/X-Fade Assign choices and separately propose an admitted crossfader automation edit with a paired untouched control.','control'),
('Solo in Place and return-solo contexts','Solo in Place is offered in Solo context menu and as an Options default. Soloed clip tracks can leave returns audible in that context; return solo mutes other main outputs while preserving arriving sends. Routing exceptions in the source and existing finite assumptions prevent an all-graph solo law.',[71,72],'Establish independent positive clip/return send and Main paths, explicit Solo in Place setting and admitted ordinary topology; separately propose clip solo and return solo with working receiver baselines. Retain each path independently, without treating an indicator or missing send as audio proof.','signal'),
]
GAPS=[('MULTI','Multi-control units, name/order and focus','Relative multi-edit units/clamping, mixed pan modes, prefix numbering grammar, drag/device state and Ctrl/platform/focus histories remain unknown.'),('GROUP','Group scope and source contexts','Group slot launch/stop context in Mixing B043 versus existing Session group-slot owner, nesting/media/Undo/move/ungroup and color/solo precedence remain unknown.'),('ARM','Arm preference and implicit-arm context','Mixing B014 documents Exclusive Arm and new/empty MIDI instrument implicit arm; recording REQ001 retains preference/implicit-arm U. Preserve this new source context without silently revising that sealed owner.'),('CROSSFADE','Curve and remote gesture context','B066/067 describes unattenuated half ranges without naming a curve; existing finite seven-curve functions differ. Keep source/curve context U and do not replace numeric laws. Keyboard held-input and automation histories remain unknown.'),('LIFECYCLE','Build, state and processing lifecycle','Exact12.4.3 controls/defaults, malformed inputs, permissions/source loss, cancellation, undo/persistence, event ordering, active audio/MIDI/rate changes and teardown remain required unknowns.')]
def build():
 bs=load(R/'manual-mixing-blocks.json');index={b['locator']:b for b in bs};req=[];cases=[]
 for title,claim,nums,action,kind in DATA:
  rid=f'REQ-MIXING-WORKFLOW-{len(req)+1:03d}';cid=f'MXW-{len(cases)+1:03d}';ev=[index[f'mixing:B{n:03d}'] for n in nums]
  req.append(dict(id=rid,title=title,provenance='D12',target_applicability='U',contract=claim,evidence=[dict(block=b['locator'],anchor=b['anchor'],html_line=b['html_line']) for b in ev]))
  visible=kind in {'control','state'} and nums not in [[10,11,12,33],[29,30]]
  cases.append(dict(id=cid,requirements=[rid],title=title,kind=kind,preconditions=['owned-context','positive-guard'],setup_and_action=action,source_claim=claim,documentary_expected='Named visible control/state role only: '+title if visible else None,documentary_comparator='Visible named-role inspection only; no numeric/signal/timing comparator' if visible else None,expected=None,comparison=None,target_grade='U',executed=False))
 for key,title,claim in GAPS:
  rid='REQ-MIXING-WORKFLOW-U-'+key;req.append(dict(id=rid,title=title,provenance='U',target_applicability='U',contract=claim,evidence=[]))
  for n,action in enumerate(['After independently admitted valid control/selection/focus and positive operation baseline, vary one relevant preference, platform, grouping or boundary context in separate reset copies; retain state without a default/refusal oracle.','Use independent working nonzero owned source/content, active processing and valid nonmuted routes/record gates before proposing one relevant control/engine/input transition; retain audio/MIDI/numeric/timing outcomes as U.','After a separately admitted successful control operation and known save/Undo baseline, propose one actually supported cancel/save/reopen/Undo/source-loss/teardown history on disposable state; absent capability is U, not a pass.'],1):cases.append(dict(id=f'MXW-U-{key}-{n}',requirements=[rid],title=title,kind='unresolved',preconditions=['owned-context','positive-guard'],setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False))
 return bs,req,cases
if __name__=='__main__':
 assert not (P/'manifest-author-r1.json').exists(),'sealed; use a preserved successor'
 bs,req,cases=build();write=lambda n,x:(P/n).write_text(json.dumps(x,indent=2)+'\n')
 for n,x in [('source-blocks.json',bs),('requirements.json',req),('cases.json',cases),('source.json',load(R/'mixing-capture.json'))]:write(n,x)
 owners=['mix-graph.md','mixer-values.md','recording-comping.md','routing-monitoring-latency.md','session-view-workflows.md','clip-view-workflows.md','keyboard-navigation.md','remote-control-workflows.md','automation-workflows.md','device-racks.md','project-media-workflows.md','engine-resource-workflows.md']
 paths=[R/n for n in ['manifest-author-r1.json','manual-mixing-blocks.json','manual-mixing.txt','manual-12-mixing-2026-10-19.html','mixing-capture.json','capture.py']]+[ROOT/'wiki/specs'/n for n in owners]
 write('input-owner-pins.json',[dict(path=str(f.relative_to(ROOT)),bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in paths])
 write('fixtures.json',{'owned-context':'Future owned disposable backed-up Sets/tracks/clips/devices/content, admitted actual controls/preferences/platform/focus and valid operations. No original/UI/application/hardware/API/script/candidate operation ran. Group deletion is proposal only.','positive-guard':'Require independently working control/selection/context, valid track/device/source/observer and positive nonzero active source/processing/nonmuted path for signal proposals. Missing source/control/selection/record gate, hidden mixer, empty group, zero gain or stale route is U, never a passing exclusion.','limits':'Visible documentary oracles compare only named roles; all transforms/numeric/text grammar/signal/timing and U documentary outputs null. All target expectations/comparators null/U/unexecuted. No signal, meter, geometry, figure or DSP result is fabricated.'})
 write('counts.json',dict(requirements=len(req),documentary_requirements=len(DATA),unknown_requirements=len(GAPS),cases=len(cases),visible_documentary_oracles=sum(c['documentary_expected'] is not None for c in cases),null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases),source_blocks=len(bs),all_target_U_null_unexecuted=True))
 front='---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
 spec=front.format(id='SPEC-MIXING-WORKFLOWS',type='spec',status='draft')+'''# Mixer interactions and group presentation

Partial F-08/F-09 contracts for additional mixer UI/selection/group/remote
entrypoints from the retained Mixing chapter. D12 is current Version12 publication
text only; all exact12.4.3 outcomes remain U. No original function/application,
UI/audio/MIDI/API/Max/hardware/candidate operation or source example ran.

[Mix graph](mix-graph.md) and [mixer values](mixer-values.md) own finite signal,
values/units/curves/storage laws. [Routing](routing-monitoring-latency.md) owns
routing/cue/send taps/meters/track-delay policy; [recording](recording-comping.md)
owns arm/monitor/record gates; [Session](session-view-workflows.md) owns group
slots/scenes. [Keyboard](keyboard-navigation.md), [remote](remote-control-workflows.md),
[Clip View](clip-view-workflows.md), [automation](automation-workflows.md),
[racks](device-racks.md), [projects](project-media-workflows.md) and
[engine](engine-resource-workflows.md) retain detailed focus/mapping/metadata/
processing/persistence/lifecycle laws. No duplicate algorithm or unqualified
signal law is introduced by these entrypoints.

## Documentary requirements

'''
 for r in req:
  spec+=f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
  if r['evidence']:spec+='Evidence: '+', '.join(f"`{b['block']}` HTML{b['html_line']}" for b in r['evidence'])+'; [retained source](#analysis-only-evidence).\n\n'
 spec+='''## Cases and unresolved source contexts

[33 proposals](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/cases.json)
cover18 documentary roles and15 U histories across23 requirements. Visible role
comparators do not grade numeric differences, naming grammar, pixels, meter
calibration, audio/MIDI or timing. All transforms/signal and U documentary
expectations/comparators remain null; every target expectation/comparison is
null/U/unexecuted. [Setups](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/fixtures.json)
require independent valid controls and positive active source/path where relevant.
No track/group/file was deleted or modified during this documentary work.

Mixing B066/067 half-range prose cannot override seven finite curve functions.
B014 new implicit-arm/preference context is retained for the recording owner,
not silently published over its U clause. B043 group slot context stays with the
Session owner. B053 control enablement does not establish ALS EnabledByUser or
engine send-active identity. These contexts and all new lifecycle branches remain U.

## Analysis-only evidence

Official [Version12 Mixing](https://www.ableton.com/en/live-manual/12/mixing/),
original captureUTC2026-10-19T21:33:28.556179+00:00,276916bytes,SHA-256
`255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e`.
[Exact retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/routing-monitoring/manual-12-mixing-2026-10-19.html)
is reused unchanged. [Source identity](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source.json)
keeps its original gap-capture scope label as history, not a recapture or authority
for all chapter claims. [All94 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source-blocks.json)
retain HTML lines/anchors; root read every block, with figures/chart uninspected.
[Research](../research/mixing-workflows.md) owns routing/context interpretation.
[Author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/manifest-author-r1.json)
freezes only this partial scope for independent review.
'''
 research=front.format(id='RESEARCH-MIXING-WORKFLOWS',type='research',status='current')+'''# Mixing source roles and unresolved contexts

The [partial draft](../specs/mixing-workflows.md) follows the
[coverage design](full-live-specification-design.md) and [plan](full-live-specification-plan.md).
Root read all94 retained Mixing blocks from the earlier routing packet; no new
fetch, figure/chart inspection, native/UI/API/audio/hardware/candidate operation
or source example execution. Original URL/UTC/size/hash bytes remain unchanged;
current Version12 publication is not exact12.4.3 behavior proof.

## Ownership and limits

New scope is18 documentary predicates plusfive U groups (23requirements/33cases):
visibility/resizing, selected control/track movement, numbering names, clip-to-new-
track device presence, group creation/presentation/move/delete/ungroup/color/solo
indicator, return Send menu admission, crossfader menu/key/automation entrypoints
and scoped solo/return contexts. Existing numeric, mix/routing/record/Session/
keyboard/remote/metadata/automation/device/project/engine owners retain laws.

Chapter B009 meter policy, B014 arm gates, B018–022 headroom/clip claims,
B025–026 track-creation shortcuts/Browser admission, B029–030 generic rename/info,
B034 track-to-Set/media collection, B039 grouping routing, B043 group slots,
B048–056 returns/Main/taps, B064–068 numerical assignment, B074–080 cue,
B082–091 delay/monitoring and B093–094 CPU indicators are routed to existing owners.
Their presence in a complete chapter capture does not close all their branches.
No private floating-point architecture, universal non-clipping or visual-meter
signal proof is adopted. The crossfader chart was not inspected or sampled.

## Source-context questions

- MIXW-U-ARM: B014 Exclusive Arm/new-or-empty instrument insertion gives new
  documentary preference/implicit-arm context; recording REQ001 keeps those U
  under its original sealed scope. Any owner successor needs exact source/version
  and positive eligibility, not silent replacement or proof of recording.
- MIXW-U-CURVE: B066/067 unattenuated half-range wording does not name a curve;
  existing seven-curve functions have distinct values. Preserve both contexts,
  source defaults and curve selection; no blanket inequality or unity law.
- MIXW-U-GROUP: B043 launch/stop whenever at least one child clip versus existing
  Session group-slot empty-stop context needs matched slot/control wording; source
  overview does not replace the detailed Session owner or prove a contradiction.
- MIXW-U-SEND: B053 disabled/default Enable Send is control-level source data,
  not proof of the finite stored EnabledByUser-to-active-bit relationship.
- MIXW-U-MULTI: knob/slider differences omit coordinate/units/clamping, and Ctrl
  selection/move text lacks platform qualification. No numeric delta, Cmd alias,
  mixed-mode override or focus-precedence law is invented.

## Evidence, cases and freeze

[Source](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source.json)
retains original capture scope metadata. [Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/source-blocks.json),
[requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/cases.json)
retain exact locators and action linkage. [Inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/input-owner-pins.json)
pin original routing seal/source/parser and12canonical owners. All33target outputs/
comparators are null/U/unexecuted; signal/transform/U documentary outputs also null.
Visible-role proposals are not measured geometry, numeric state or audio criteria.
No deletion, account, file, hardware or application operation occurred.

[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/mixing-workflows/manifest-author-r1.json)
freezes author data/code/prose/snapshots/read-only validator. Source replay,
requirements-browser equality, pins/nulls/links/whitespace are integrity only;
independent semantic review is pending and the whole Mixing family remains partial.
'''
 for f,s in [('wiki/specs/mixing-workflows.md',spec),('wiki/research/mixing-workflows.md',research)]: (ROOT/f).write_text(s)
 (P/'spec-r1.md').write_text(spec);(P/'research-r1.md').write_text(research)
