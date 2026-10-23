"""Author a documentary Max host/template packet, not a Max host or patch implementation."""
from pathlib import Path
from collections import Counter
import hashlib
import json

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
BLOCKS={r['locator']:r for r in json.loads((P/'manual-blocks.json').read_text())}
TEMPLATES=json.loads((P/'template-files.json').read_text())
REQ=[]
CASES=[]

def write(name,value):
    (P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def add(rid,title,contract,refs,provenance='D12',template=None):
    assert all(r in BLOCKS for r in refs) if provenance=='D12' else True
    REQ.append({'id':rid,'title':title,'contract':contract,'provenance':provenance,'target_applicability':'U','source_id':'D12-MAX-HOST' if provenance=='D12' else template if provenance=='Dpkg' else None,'source_blocks':refs,'template':template})

def case(cid,rid,kind,action,expected=None,refs=None):
    r=next(r for r in REQ if r['id']==rid)
    CASES.append({'id':cid,'requirements':[rid],'kind':kind,'template':r['template'],'provenance':r['provenance'],'fixture':'fixtures.json#MAX-HOST-F0','setup_and_action':action,'documentary_expected':r['contract'] if expected is True else expected,'documentary_comparator':'Exact source bytes/hash/size and frozen inventory association only; no patch parsing or runtime proof.' if expected is True and r['provenance']=='Dpkg' else 'Compare only specified public menus/labels/roles, source-file relations or visible editing/save/discovery transitions; no numerical audio/MIDI/file codec, timing, CPU or API assertion.' if expected is True and kind not in ['signal-obligation','timing-obligation'] else None,'expected':None,'comparison':None,'target_grade':'U','executed':False,'source_blocks':r['source_blocks'] if refs is None else refs})

host=[
([6], 'positive', 'Bundled setup context', 'The manual describes Max for Live as included with Suite and Standard plus the Max for Live add-on, without separate installation. Entitlement/activation/platform failure behavior is not specified.', 'Inspect declared edition and Max-for-Live entitlement before testing host actions; unavailable entitlement is U. Do not install or authorize anything as part of this packet.'),
([7,8], 'timing-obligation', 'Selected editor application', 'File & Folder settings can select a specific Max application path instead of bundled editor; changing path takes effect after Live restart, when opening editor launches chosen Max.', 'In a future owned environment retain existing bundled/alternate valid Max identity, set alternate path, compare editor-open before and after restart. Capture chosen editor identity; no default version, supported version range or pre-restart transition oracle beyond documented restart prerequisite.'),
([10,11], 'positive', 'Device browser surfaces', 'Core Library Max instruments/effects appear in Instruments, Audio Effects, MIDI Effects and Modulators; Max for Live label includes installed third-party/user devices and MIDI Tools. This is discovery UI, not proof every arbitrary AMXD works.', 'With independently valid installed/user/Pack examples, inspect named labels and offered device identities. Twenty inventoried devices stay separately pending; do not load or infer their algorithms here.'),
([10], 'positive', 'Modulator role', 'Modulators are documented as controlling Live parameters with modulation signals. Specific mappings, ranges, parameter ownership, timing and device algorithms are not supplied.', 'Inspect Modulators browser label and an independently identified compatible device entry. An executable mapping test needs nonzero source/amount and paired positive response under its future individual-device owner.'),
([12], 'positive', 'Preset workflow', 'Max devices can have supplied presets and user-created/edited presets similar to ordinary device presets. Exact patch-definition versus parameter-state identity and sharing rules remain U.', 'Select an independently valid Max device with two identified presets and inspect preset/save entry points; route generic device/preset operations to device-racks owner. No constructor default or common preset-codec law.'),
([16,17], 'positive', 'Open device editor', 'For Max devices, Edit in Max in title-bar context or Show Options launches Max and opens selected device in editor/patcher.', 'Test each menu route with one selected owned device, retaining selected device/editor identities; compare two instances in separate trials. Editor process/lifecycle and latency remain U.'),
([18], 'positive', 'Developer edit button context', 'The manual distinguishes pre-12.2 device-title Edit button from current Edit in Max command. It documents -MaxForLiveDeveloperMode in Options.txt as restoring button functionality. Exact 12.4.3 option parsing/effective restart/default behavior is U.', 'Inspect documented menu versus button contexts in a future disposable configuration; retain Options.txt presence/version and device type. This author packet does not create or edit Options.txt; MIDI Tools Edit remains its own context.'),
([19], 'positive', 'Device Save instance scope', 'After editing a device, Max File Save updates all instances of the same device in the Set. Meaning of same-device identity versus preset copies, dirty state and atomicity is not established.', 'Prepare owned patch A with two instances and separate copy B; edit an observable presentation label on A in editor and Save; inspect both A instances and B without assigning identity from equal display names.'),
([19], 'positive', 'Device Save As confirmation', 'Device Save As opens confirmation asking whether changes apply only to edited preset or all instances.', 'Owned A in two instances: Save As to distinct new AMXD path, choose edited-only then all-instances in reset trials; retain dialog choice and resulting references/presentation. Cancel/file overwrite/history are U cases.'),
([20], 'positive', 'Default device save folders', 'Max device default save location is the User Library folder appropriate to type, including Max Audio Effect and Max MIDI Effect. The chapter does not enumerate the exact folder name for every other type.', 'Invoke Save As for owned audio-effect and MIDI-effect copies and inspect offered User Library destination; do not infer an unlisted exact Instrument folder or overwrite installed templates.'),
([21], 'positive', 'Separate AMXD references', 'Max devices are separate AMXD files rather than embedded in Set. Moving/renaming referenced AMXD can break path; File Manager offers location repair. Exact relocation/search/copy behavior remains U.', 'Save owned Set referencing A.amxd, rename/move test-owned A externally, reopen and inspect File Manager entry; exact warning/refusal/recovery/relinked state ungraded until its U cases. Collection/reference canon remains project/media.'),
([25,26], 'positive', 'Existing tool editor route', 'An existing Max for Live MIDI Tool can be a starting point. Selected tool/template Edit button launches Max editor; this tool UI is distinct from current device-title Edit in Max.', 'Select a separately owned copy of an identified Max MIDI Tool in appropriate panel, inspect Edit and select it; retain editor/tool identity. Do not edit or execute Euclidean/Velocity Shaper algorithm as part of this packet.'),
([27], 'positive', 'Tool saving', 'Max MIDI Tools are saved with patcher File Save or Save As. The device Save all-instances rule is not automatically transferred to tool selections.', 'Owned tool copy with harmless visible label edit; inspect Save and Save As to separate paths. Actual saved-content/persistence/state propagation remains U.'),
([28,29,30], 'positive', 'Tool default folders', 'Documented default tool directories are ~/Music/Ableton/User Library/MIDI Tools/Max Transformations and .../Max Generators. User Library relocation/platform path resolution remains U.', 'Open Save As for owned Transformation then Generator and inspect offered path against declared User Library location. Exact path literal is documented context, not Linux original support.'),
([31,32], 'negative', 'Tool discovery locations', 'Tools stored in default folders or browser Places appear in corresponding tool dropdowns; elsewhere they are not found by Indexer and do not appear there. Timing, cache invalidation, recursion and ambiguous duplicate resolution are U.', 'Use uniquely named owned valid tools in declared default folder, a separately added Places folder and a folder in neither; inspect appropriate dropdown after independently established indexing readiness. No automatic refresh deadline or immediate move disappearance is asserted.'),
([35,36,37], 'positive', 'Dependencies and device freeze', 'Max devices may depend on samples, images or other patches. Device freezing packages files needed to use device; it is distinct from Freeze Track. Exact dependency discovery, supported file types, package grammar and portability are not specified.', 'Independently authored owned patch with recorded sample/image/subpatch references and working unfrozen positive baseline; inspect offered device Freeze route and retained dependency identities. Exact command UI, frozen import/execution and missing-dependency outcomes remain U.'),
([33,39], 'positive', 'Reference entry points', 'Max Help Reference opens built-in documentation with a Max for Live category; MIDI Tools guide is routed through category Guides. Availability/documentation versions and full API/object contracts are not captured here.', 'In future available Max editor inspect Help Reference and Max-for-Live category/Guides; do not treat links to external docs as retained API or compatibility proof.')]
for n,(nums,kind,title,contract,action) in enumerate(host,1):
    rid=f'REQ-MAX-HOST-{n:03d}';refs=[f'MAX:B{i:03d}' for i in nums]
    add(rid,title,contract,refs);case(f'MAX-H-{n:03d}',rid,kind,action,True)

roles={
'Max Audio Effect':('AE',[14,15,16,17],'The named default Max Audio Effect is a starting point dragged from browser into Set for editing. The manual describes incoming chain audio being passed onward to subsequent devices. This documentary default role supplies no measured unity gain, bit identity, channel/latency/bypass law or arbitrary edited-patch behavior.','An active audio input with two distinguishable channels; no instrument requirement inferred.','Max Audio Effect browser default, chain upstream/downstream identity, Edit in Max route. Preserve audible upstream/downstream positive baseline; no exact passthrough metric.'),
'Max Instrument':('IN',[15,16,17],'The named Max Instrument default can be dragged from browser into Set as a new editable Max device. This text does not specify its default note/audio behavior, voice model or channel mapping.','MIDI note input available and an identified output route, without assuming template synthesizes audio.','Max Instrument browser default and editor identity. Sending notes is a future U probe, not a documented output oracle.'),
'Max MIDI Effect':('ME',[15,16,17],'The named Max MIDI Effect default can be dragged from browser into Set as a new editable Max device. Template presence/name supplies no MIDI pass-through, ordering, translation or output-message law.','MIDI input and inspectable downstream route, without assuming template passes notes.','Max MIDI Effect browser default and editor identity; no default message-byte or note-output assertion.'),
'Max MIDI Generator':('GE',[24,26,27,28,30],'Max MIDI Generator is the default tool starting point in Generative Tools panel/tab; selected template Edit opens patcher and Save/Save As saves tool. No default generated notes, randomness, seed or generation range is established.','Editable MIDI clip and Generative Tools panel; no occupied-region behavior or generated-note content assumed.','Generator template in Generative panel, Edit route, Save As path to owned Max Generators folder. Generation button/output behavior remains U.'),
'Max MIDI Transformation':('TR',[24,26,27,28,29],'Max MIDI Transformation is the default tool starting point in Transformation panel/tab; selected template Edit opens patcher and Save/Save As saves tool. No default note/expression transformation, pass-through or selection scope is established.','Editable MIDI clip with two selected notes and Transformation panel; no original-note replacement or expression behavior assumed.','Transformation template in Transform panel, Edit route, Save As path to owned Max Transformations folder. Transformation output remains U.')}
for f in TEMPLATES:
    key,nums,contract,pre,action=roles[f['name']];refs=[f'MAX:B{i:03d}' for i in nums]
    rid=f'REQ-MAX-TEMPLATE-{key}-ROLE';add(rid,f['name']+' documentary role',contract,refs,template=f['id'])
    case(f'MAX-T-{key}-ROLE',rid,'signal-obligation' if key=='AE' else 'positive',pre+' Select '+action,True)
    rid=f'REQ-MAX-TEMPLATE-{key}-FILE'
    add(rid,f['name']+' retained identity','Inventory identifies '+f['name']+' at '+f['original_path']+'; retained '+f['file']+' is '+str(f['bytes'])+' bytes with SHA-256 '+f['sha256']+'. This is supplied-file identity only; contents unparsed and no runtime I/O, default or API behavior follows.',[],provenance='Dpkg',template=f['id'])
    case(f'MAX-T-{key}-FILE',rid,'package','Compare pinned inventory record, original file and retained copy size/hash/prefix without parsing patch contents or loading Max.',True)
    rid=f'REQ-MAX-TEMPLATE-{key}-RUNTIME'
    add(rid,f['name']+' required runtime/lifecycle outcomes','Required template-specific runtime I/O, edits, host timing, saved-state/error/cancel/teardown outcomes remain unknown; use only independently accepted controls and owned copies.',[],provenance='U',template=f['id'])
    for suffix,kind,action in [
('IO','signal-obligation',pre+' Retain accepted target template/editor identity, apply isolated input or nonempty clip stimulus, inspect output then edited-label/control state. No note/audio/message/pass-through result is presumed.'),
('SAVE','persistence',pre+' Save owned copy, instantiate/select second copy, save/reopen Set or clip/tool context, reload preset, rename source AMXD and one declared dependency in separate trials. Record reference/state and missing-source behavior; no inherited all-instance policy.'),
('MALFORMED','malformed',pre+' Attempt load/edit of separate truncated AMXD copy and missing/wrong-type dependency; attempt invalid numeric control text only where a control is actually offered. Record failure/recovery/state, never use immutable source copies.'),
('CANCEL','cancellation',pre+' Begin editor dirty edit then close/cancel, or Save As to distinct path and cancel confirmation. Undo/Redo harmless label edit where available; retain instance/tool selection and source bytes. Atomicity and history scope U.'),
('TEARDOWN','teardown',pre+' During an active note/input/clip edit or editor operation, remove device/deselect tool, close editor, stop/restart transport and close Set in separate trials; inspect output/held notes/pending edits/resources. All timing/cleanup outcomes U.')]:
        case(f'MAX-T-{key}-U-{suffix}',rid,kind,action)

unknowns=[
('APP','Application selection/availability and editor coordination remain unknown.',[
('APP-LOSS','error','Future available environment: select absent, moved, wrong-version or non-executable alternate Max path on disposable configuration; open device/tool editor before/after restart. Record error/fallback and previous-path retention; do not install tooling.'),
('EDITOR-RACE','selection','Two different owned devices and one tool selected in separate contexts; open multiple editors, switch selection while launch/Save As pending, close/reopen editor. Record device identity, focus, single/multiple-process/window and dirty-state ownership.')]),
('SAVE','Save/save-as/preset/shared-reference transactions remain unknown beyond documented confirmation scope.',[
('SAVE-CANCEL','cancellation','Two instances of owned A and separate-copy B; Save As, cancel destination picker, then cancel apply-to-all confirmation separately, and retry with source path overwrite on disposable copies. Inspect all references/files/dirty states; no rollback policy assumed.'),
('SAVE-FAIL','error','Owned A save into unwritable/full destination or lost User Library; close/reopen Set with referenced A renamed/missing and attempt File Manager repair. Record partial files, messages, prior state, fallback and retry outcomes.')]),
('DEPENDENCY','Dependency discovery, freeze/unfreeze and dependency-loss outcomes remain unknown.',[
('DEPENDENCY-LOSS','source-loss','Owned A with sample/image/subpatch declared separately; establish functioning source-specific positive baseline, freeze if available, remove one original dependency at a time and reload. Compare unfrozen/frozen copies; supported dependency kinds and missing results remain U.'),
('FREEZE-CANCEL','cancellation','Start offered Freeze or Save on owned dependency-rich patch and cancel/interrupt at retained progress points; separately unfreeze/edit/refreeze if offered, then rename an embedded/dependent file in disposable copy. Record files/state/cleanup without inferring container format or atomicity.')]),
('TOOLS','Tool indexing and clip apply/select/editor interactions remain unknown.',[
('INDEX-BOUNDARY','boundary','Unique owned valid Generator/Transformation copies in default folders/Places/neither; move/rename/delete then duplicate visible names across two allowed roots, retain actual readiness state and tool type. Record discovery/selection/cache precedence, not an immediate-rescan deadline.'),
('TOOL-APPLY','undo-redo','MIDI clip with notes and per-note expression under recorded selection/loop/scale; select own tool/template, invoke Apply then change selection while editor active, Undo/Redo and close/reopen clip. Original/generated/transformed notes and histories are U; tool algorithms remain with MIDI editing owner.')]),
('ENGINE','Host DSP/MIDI/clock/performance/API behavior remains unknown.',[
('ENGINE','sample-rate','Only for independently functioning owned patch with documented accepted I/O, repeat nonzero audio/MIDI at 44.1/48/96kHz and64/256frames,90/120BPM; stop/start/seek, real-time/offline and engine suspend/resume separately. Latency, phase/tails/clock and output equality U.'),
('API','api','No API/object protocol fixture supplied. A future separately scoped source must pin supported public API/object versions, permissions, parameter and event behavior before an application observation case can be graded; host/manual links or template hashes are insufficient.')]),
('STATE','Automation/mapping/history/persistence and teardown ownership remain unknown.',[
('AUTOMATION','automation','Owned patch with independently offered exposed parameter: accepted A/B values, manual change then recorded automation/re-enable, rack macro and MIDI mapping in separate trials; editor Save while automated. Eligibility, scaling, smoothing and precedence U.'),
('TEARDOWN','teardown','Owned patch active with held notes/audio and open dirty editor, pending save or dependency operation; bypass/remove device, deselect tool, lose MIDI source, close Set and quit app in separate trials. Output, pending work, files, history, resource release and recovery U.')])]
for group,contract,entries in unknowns:
    rid='REQ-MAX-HOST-U-'+group;add(rid,group+' unknown obligations',contract,[],provenance='U')
    for suffix,kind,action in entries:case('MAX-U-'+suffix,rid,kind,action)

write('requirements.json',REQ)
write('cases.json',CASES)
write('fixtures.json',{'id':'MAX-HOST-F0','status':'Future analyst input recipes only; no Max patch, executable, rendered audio or MIDI output supplied','common':['Disposable Set/User Library/configuration, known supporting Live edition/add-on and Max editor identity in a future available original environment. This packet authorizes no original execution, installation or option-file changes.','Own copies only; never edit installed templates or retained source bytes. Save paths must be test-owned and distinct; retain AMXD/dependency byte hashes, paths and references before/after actions.','F-MULTI: independently authored patch A with harmless visible label and optional independently accepted exposed parameter; two same-device instances and distinct file copy B. Same-device identity is recorded, not inferred from title/preset name.','F-DEPS: independently authored device with individually identified supported sample, image and subpatch dependencies. Functioning unfrozen positive baseline and actual offered freeze/unfreeze commands required before dependency-loss observations. No fixture patch authored or executed here.','F-MIDI: editable clip with distinct notes and expression under explicit note/time selection, scale, loop and tool panel. Euclidean/VelocityShaper algorithms remain owned by MIDI editing.','F-AUDIO: future retained owned 4-second dual-channel stimulus with distinct content, audible nonzero gains and routes. Source/channel/rate/byte identity required before input-output comparisons; no output/duration/phase/latency equality promised.'],'positive_signal_guard':'Only actually offered correct device/template controls; nonzero input and relevant processing amount, active sections/routes, unmuted upstream/downstream output and independently confirmed positive response. A missing/unloaded patch, zero depth, absent note, silent generator, muted path or unresolved dependency is inconclusive/U, never a pass.','template_preconditions':{name:r[3] for name,r in roles.items()},'original_execution':False,'candidate_comparison':False})
source=json.loads((P/'source.json').read_text())
sources=[source]
for name in ['devices.json','manual-toc.json']:
    path=P.parent/'inventory'/name;data=path.read_bytes();sources.append({'id':'INVENTORY-'+name.upper().replace('.','-'),'file':'../inventory/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'limit':'Frozen discovery records only, not behavioral proof'})
sources += [{**r,'limit':'Exact unparsed source-file identity only; no default I/O, algorithm, API or patch execution proof'} for r in TEMPLATES]
write('sources.json',sources)
counts={'requirements':len(REQ),'requirement_provenance':dict(Counter(r['provenance'] for r in REQ)),'cases':len(CASES),'case_kinds':dict(Counter(c['kind'] for c in CASES)),'template_count':len(TEMPLATES),'target_graded':0}
write('counts.json',counts)
assert len(REQ)==38 and len(CASES)==64
assert len({r['id'] for r in REQ})==len(REQ) and len({c['id'] for c in CASES})==len(CASES)
assert {r['id'] for r in REQ}=={r for c in CASES for r in c['requirements']}
link='../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/'
spec='''---
id: SPEC-MAX-FOR-LIVE-HOSTING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary Version 12 applicability unknown
---

# Max for Live host and template workflows

## Scope and authority

This partial F-05/F-08 draft owns documented Max editor selection, device/tool
editing and save/discovery/dependency workflows, plus individual documentary
roles and retained identity for five inventoried templates. It establishes no
arbitrary Max compatibility, full Live API/object/event protocol, AMXD codec,
patch algorithm, DSP/MIDI engine or complete host coverage. **D12** is captured
Version 12 prose; **every runtime clause has exact 12.4.3 applicability U**.
**Dpkg** is supplied-file identity only. U outcomes have null expectations and
comparators; no original application/patch/function, external editor or candidate
ran. This is an analyst draft, not a released implementation input.

[Coverage design](../research/full-live-specification-design.md) and
[research](../research/max-for-live-hosting.md) own method/source interpretation.
[Device racks](device-racks.md) owns common chains/presets, [browser](browser-workflows.md)
and [project/media](project-media-workflows.md) own their bounded file/discovery
operations, [automation](automation-envelopes.md) and [mapping](midi-user-mapping.md)
own their finite contracts. [MIDI editing/tools](midi-editing-tools.md) owns
Euclidean/VelocityShaper algorithms (REQ-MIDI-EDIT-043/038) and tool note editing;
this page adds no algorithmic or occupied-region oracle. [Clip View](clip-view-workflows.md)
owns shared panels. Twenty shipped Max devices in the
[inventory boundary](REPLACE_LINKinventory-boundary.json) remain separately pending;
this host packet does not cover their controls, maps or sound. Third-party
[plug-in host](plugin-hosting.md) and [bundled host](bundled-device-hosting.md)
contracts do not imply Max ABI or arbitrary patch support.

## Input and acceptance boundaries

[Finite future setups](REPLACE_LINKfixtures.json) require owned file copies,
explicit edition/Max version, application path and restart state, selected
instance/tool, save identity, dependencies, panel/focus and actual accepted
controls. No fixture patch or executable is supplied. The five AMXD copies are
immutable analyst sources: content unparsed, no executable use. Missing Max,
patch support, controls, dependencies or positive response leaves a case U.

Audio/MIDI/no-effect observations need active nonzero input/depth/route, unmuted
output and independently functioning paired positive baseline. A nominally
empty template is not assigned silence, pass-through, notes or audio from its
name. A public default audio-flow description is not a numerical unity/bit/phase
oracle. Save-confirmation UI does not prove rollback, identity, shared-instance
state or file atomicity beyond its documented predicate. Device freeze differs
from track Freeze; no private patch graph/process/API architecture is prescribed.

## Host requirements

All following rows are D12/target-U. Exact retained blocks include source HTML
lines and numbered heading context. The same-number MAX-H-NNN case provides
finite actions. Timing or signal obligations stay ungraded.

| Requirement | Documented contract and limits | Source blocks |
| --- | --- | --- |
'''.replace('REPLACE_LINK',link)
for r in REQ:
    if r['id'].startswith('REQ-MAX-HOST-') and r['provenance']=='D12':
        spec+=f'| {r["id"]} — {r["title"]} | {r["contract"]} | '+', '.join('`'+b+'`' for b in r['source_blocks'])+' |\n'
spec+='\n## Five individually scoped templates\n\n'
for f in TEMPLATES:
    key=roles[f['name']][0];role=next(r for r in REQ if r['id']==f'REQ-MAX-TEMPLATE-{key}-ROLE')
    spec+=f'### {f["name"]}\n\nSurface `{f["id"]}`. **REQ-MAX-TEMPLATE-{key}-ROLE (D12/target-U):** {role["contract"]}\n\nEvidence: '+', '.join('`'+b+'`' for b in role['source_blocks'])+f'. **REQ-MAX-TEMPLATE-{key}-FILE (Dpkg):** retained `{f["file"]}`, {f["bytes"]} bytes, SHA-256 `{f["sha256"]}`. [Template file ledger]({link}template-files.json) retains original/copy paths and prefixes; no source content was parsed.\n\n**REQ-MAX-TEMPLATE-{key}-RUNTIME (U):** five concrete cases cover I/O, save/reopen/reference loss, malformed AMXD/dependency, cancel/undo and teardown/transport. No default behavior or lifecycle output is inferred from the template name or bytes.\n\n'
spec+='''## Required unknown host behavior

| Requirement | Required missing outcomes | Concrete U cases |
| --- | --- | --- |
'''
for group,contract,entries in unknowns:
    spec+=f'| REQ-MAX-HOST-U-{group} | {contract} | '+', '.join('`MAX-U-'+e[0]+'`' for e in entries)+' |\n'
spec+='''
Cases retain invalid app path, lost/unwritable AMXD/User Library, same-device and
copy identity, Save As cancellation/overwrite, dependency source loss and freeze
interruption, duplicate/outside-location tool indexing, clip Apply/selection/undo,
rate/block/transport, automation/mapping and device/editor/Set teardown. Malformed
inputs use disposable truncated copies, never source evidence. These are required
unknowns, not inapplicable omissions. Missing prerequisites are not a pass.

## Case catalog and source limits

[Requirements](REPLACE_LINKrequirements.json) contain **38 clauses: 22 D12, 5 Dpkg,
11 U**. [64 cases](REPLACE_LINKcases.json) include 22 documentary proposals, 5 package
identity checks and 37 U lifecycle/runtime obligations. All 64 have
`executed:false`, `target_grade:U`, `expected:null` and `comparison:null`.
A separate documentary field proposes only source-supported named visible state;
signal/timing obligations have no documentary comparator. There are zero target
oracles or compatibility grades. Positive/negative/boundary cases accompany
malformed/cancel/save/undo/source-loss/transport/rate/teardown/automation/API gaps.
Compound cases remain bounded investigation recipes, not exhaustive closure.

The chapter's device Edit in Max versus pre-12.2 Edit button statement is scoped
to device-title controls. MIDI Tools keep their own Edit button context. They are
not asserted contradictory. Editor selection affects launch after restart but
supplies no supported Max-version matrix. Device Save updates same-device
instances as documented; tool Save propagation is left U. Default-location or
Places discovery needs known valid tool and indexing readiness; no immediate
refresh guarantee. Device freezing packages dependencies as documented, while
file-type closure, external objects, licenses, search paths and platform binaries
remain unsupported. No dependency-free, portable, sandboxed or security-isolation
claim follows. Full API protocol needs its own retained versioned sources.

## Analyst evidence appendix

Official [Max for Live chapter](https://www.ableton.com/en/live-manual/12/max-for-live/),
Version 12, captured 2026-10-19. [Source metadata](REPLACE_LINKsource.json) retains exact
UTC/URL/250,005-byte capture; HTML SHA-256
`2f771ab26d3e08d4c7df737fbf2a2f95e62cc501739ba65a4531de90d0de69dc`.
[42 blocks](REPLACE_LINKmanual-blocks.json) retain paragraphs/headings, HTML lines
and full context for §§32–32.6, excluding sidebar/footer. [HTML](REPLACE_LINKmanual-max-for-live-2026-10-19.html)
is immutable source and [normalized text](REPLACE_LINKmanual-text.txt) navigation.
Figures were not inspected; source links to Max docs are not retained API evidence.

[Sources](REPLACE_LINKsources.json) pin manual, inventory/TOC and five inventoried
AMXD template copies. [Inventory boundary](REPLACE_LINKinventory-boundary.json)
contains 20 max-device, 2 max-midi-tool and 5 max-template records; twenty individual
patches were neither parsed nor executed, and no compatibility follows.
[Author manifest](REPLACE_LINKmanifest-author-r1.json) freezes exact payloads and
canonical snapshots. [Validation](REPLACE_LINKvalidation-author-r1.json) checks
source/hash/catalog/link/whitespace scope only. These analysis links require
sanitization and review before any handoff. No profile/host family is complete.

## Revision and handoff

Revision1 is author-frozen for separate semantic review. No handoff, public
publication, installation or implementation workspace is created by this draft.
'''.replace('REPLACE_LINK',link)
(ROOT/'wiki/specs/max-for-live-hosting.md').write_text(spec)
research='''---
id: RES-MAX-FOR-LIVE-HOSTING
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# Max for Live host and five template evidence

## Scope and selection

This partial F-05/F-08 analyst packet supports the
[canonical host/template draft](../specs/max-for-live-hosting.md), under the
[coverage design](full-live-specification-design.md). Existing inventory/TOC
selected official `/en/live-manual/12/max-for-live/`; no existing chapter capture
was found among active packets. One retained
[HTML capture](REPLACE_LINKmanual-max-for-live-2026-10-19.html), 250,005 bytes, SHA-256
`2f771ab26d3e08d4c7df737fbf2a2f95e62cc501739ba65a4531de90d0de69dc`, has exact
UTC/URL in [source metadata](REPLACE_LINKsource.json). Version 12 is established,
exact 12.4.3 applicability remains U. [42 blocks](REPLACE_LINKmanual-blocks.json)
retain HTML paragraph lines and heading context through 32.6; sidebar/footer
excluded. Figures were not inspected separately. Nothing was executed in Max,
Live, a dynamic loader/emulator or a candidate; no tooling was installed.

## Evidence boundaries and individual template roles

[Source ledger](REPLACE_LINKsources.json) retains eight pins: chapter, device
inventory, TOC and five copied template sources. [Template files](REPLACE_LINKtemplate-files.json)
match the inventoried supplied bytes, original paths, size/SHA and 16-byte prefix.
Contents were intentionally left unparsed: there is no graph, constructor,
interface, I/O, parameter/domain, algorithm or runtime proof from AMXD bytes.
The source copies are analyst evidence, not working user patches or clean-room
implementation inputs. Exactly five small inventoried sources were read; no
broader patch/native binary analysis was launched.

| Template | Documentary support | Limit |
| --- | --- | --- |
| Max Audio Effect | MAX:B014-B017: drag default into Set and edit; default passes incoming chain audio onward. | No numerical unity, bit/phase/latency/channel/bypass law or arbitrary edited-patch behavior. |
| Max Instrument | MAX:B015-B017: new editable device from named browser default. | No documented default synth/voice/audio/note response in this chapter. |
| Max MIDI Effect | MAX:B015-B017: new editable device from named browser default. | No default MIDI pass-through, message order/codec or transformation law. |
| Max MIDI Generator | MAX:B024/B026-B027/B030: Generative panel starting point, Edit, Save/Save As and default folder. | No default note/random/occupied-region or expression output. |
| Max MIDI Transformation | MAX:B024/B026-B027/B029: Transformation panel starting point, Edit, Save/Save As and default folder. | No default selection, pass-through, replacement or expression transformation. |

[Inventory boundary](REPLACE_LINKinventory-boundary.json) contains 27 entries:
20 shipped Max devices, 2 MIDI Tools, 5 templates. Twenty devices retain separate
pending F-06 scope. [MIDI editing research](midi-editing-tools.md)/its canonical
spec own Euclidean and VelocityShaper algorithms. Tool host/template editing does
not silently extend their version parity or API coverage. General third-party
plug-in contracts and seven bundled native host component models likewise do
not establish Max patch hosting. Shared file/preset/browser/mapping/automation
owners apply only inside their already bounded clauses.

## Context distinctions and open outcomes

Device context MAX:B016-B019 distinguishes current Edit in Max from pre12.2
button and describes optional developer setting. Tool context MAX:B026 names
its own Edit button; context alone explains the different UI and no contradiction
is declared. No Options.txt was edited. MAX:B007-B008 editor path/restart prose
supports selection workflow only, not compatible-Max-version negotiation.
MAX:B019 Save/Save As instance scope is not automatically copied to tools.
MAX:B021 separate AMXD references are not an embedded-Set or transactional-save
codec. MAX:B031-B032 location eligibility supplies no indexing deadline/cache
invalidation rule. MAX:B035-B037 dependency freezing is not Freeze Track, nor
proof of arbitrary external object/sample/license/platform packaging.

No linked API/Max object reference was fetched or treated as an API contract;
MAX:B003 only establishes an advertised Live API surface. Complete Max API,
object/message scheduling, security/permissions, host process isolation, DSP,
MIDI/MPE/tuning, file codec, defaults, clock/performance and arbitrary patch
compatibility require their own exact sources and tests. The host/template
partial draft names those obligations rather than supplying an emulator or fake
host. Unknown dependency loss/save/cancel/history/transport/teardown cannot be
closed by a readable file or a manual statement.

## Finite packet and checks

[38 requirements](REPLACE_LINKrequirements.json): 22 D12, 5 Dpkg, 11 U.
[64 cases](REPLACE_LINKcases.json): 22 documentary, 5 package identity and 37 U
runtime/lifecycle obligations; all target expected/comparison null/U/unexecuted.
[Inputs](REPLACE_LINKfixtures.json) are future owned-patch/media/clip recipes,
not supplied reference fixtures. Positive baselines require correct offered type,
valid dependency/input, active nonzero signal route/depth and unmuted output;
failed prerequisites stay U. Template-specific five-case groups preserve I/O,
save/reference loss, malformed dependency/AMXD, cancel/undo and teardown/transport
unknowns. Host groups retain app selection, instance/preset identity, discovery,
dependencies/freeze, engine/API and automation/state gaps.

[Author manifest](REPLACE_LINKmanifest-author-r1.json) freezes both canonical
snapshots and every payload; [validation](REPLACE_LINKvalidation-author-r1.json)
checks hashes, source locator text/context, original/copy template identity,
inventory roles/counts, cases/null outcomes, local files/metadata and untracked
whitespace. Run
`python3 analysis/ableton-live-12.4.3/full-spec-v1/max-host/validate.py`.
Structural success is no behavioral pass. Separate semantic review and root's
shared catalog/coverage/question/plan/log integration remain required; this
packet modifies none of those shared surfaces and publishes no handoff.
'''.replace('REPLACE_LINK',link)
(ROOT/'wiki/research/max-for-live-hosting.md').write_text(research)
print(json.dumps(counts,indent=2))
