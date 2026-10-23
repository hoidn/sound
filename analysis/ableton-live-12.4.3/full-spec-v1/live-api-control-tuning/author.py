"""Freeze a new analyst-only direct-member proposal; refuse to overwrite a seal."""
from pathlib import Path
import hashlib
import json
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
assert not (P/'manifest-author-r1.json').exists(), 'sealed; create an explicit successor'
M=P.parent/'max-api'
load=lambda p:json.loads(p.read_text())
write=lambda n,x:(P/n).write_text(json.dumps(x,indent=2)+'\n')
sha=lambda b:hashlib.sha256(b).hexdigest()
names=['ControlSurface','DeviceIO','Groove','GroovePool','TuningSystem','this_device']
entries=[e for e in load(M/'lom-entries.json') if e['name'] in names]
assert len(entries)==6
ids={e['source_id'] for e in entries}
blocks={k:v for k,v in load(M/'reference-blocks.json').items() if k in ids}
write('source-blocks.json',blocks)
write('sources.json',[s for s in load(M/'all-sources-r1.json') if s['id'] in ids])
# Each statement and action is deliberately specific to the member's retained text.
D={
'ControlSurface':{
'pad_layout':('The symbol is get/observe only. Printed Push2/3 layouts distinguish melodic64, melodic64+variations, sequencer, sequencer+32notes; drum variations,64pads,loop selector,16velocities,16pitches; and session. Instrument and Note/Session/Layout context conditions apply. This is not a settable layout selector or a Push1 protocol.', 'Independently establish supported Push2/3 mode and instrument contexts, then query/observe pad_layout while changing only an actually supported mode through its existing owner. Retain full returned symbols and availability; no invented layout-switch API.'),
'get_control':('Parameter name is printed without a declared type; the function returns the named control. Control object class, missing-name return and usable name grammar are not supplied.', 'On an independently admitted active surface choose a known name from its admitted name listing, request that control, and retain returned identity. Missing surface or name-list access is not an unsupported-name result.'),
'get_control_names':('Returns a list of all control names for that surface. Ordering, name encoding, list length and implicit function arguments are unspecified.', 'For one admitted active surface request its control-name list and independently validate one known available control; repeat after a separately supported surface reconfiguration only as ungraded lifecycle evidence.'),
'grab_control':('Parameter control is printed without a type. Taking ownership releases standard functionality of that control for exclusive Max for Live use; the statement is scoped to that owned control, not a global hardware mute.', 'Use an independently identified control and establish its ordinary positive functionality; propose grab, retain ownership/functionality observations, then independently restore/release on a reset copy. Never use absent functionality as sole proof of a successful grab.'),
'grab_midi':('Forwarding concerns messages the surface script receives and explicitly requests from Live. Pure realtime track messages can bypass that script; Push Note pads are the source example, contrasted with Session. This does not promise all raw MIDI from the hardware.', 'With independently admitted script-requested and bypassing track message contexts, establish positive reception at their respective owners, then compare surface API forwarding after grab. Do not treat unavailable script or missing input as a passing exclusion.'),
'register_midi_control':('MaxForLive surface only: name[symbol],status[int],number[int]. Printed status codes are144 note-on,176 CC,224 pitchbend. Returns the control LOM ID; associated forwarding is described after registration plus grab. A send_value call on the returned control is mentioned without defining that separate object member.', 'On an independently admitted MaxForLive surface propose separate valid note,CC,pitchbend registrations with independently accepted numbers/names, then obtain and grab each returned control. Record IDs and associated forwarding; no numeric ID, wire codec or send_value signature oracle.'),
'release_control':('Parameter control is printed without a type. Release re-establishes the standard functionality for that control; return value and repeated/unowned-release semantics are unspecified.', 'Establish a positively functioning ordinary control and separately confirmed grab, propose release, and retain ordinary functionality/ownership observations. Repeated or wrong-owner release remains ungraded.'),
'release_midi':('Stops forwarding messages received from that surface to Max for Live. Interaction with other receivers or automatic cleanup is unspecified.', 'Establish positive script-requested forwarding after an independently admitted grab, propose release_midi, and retain both source activity and API output so silence cannot be attributed to missing input.'),
'send_midi':('Parameter midi_message is a list of int, sent to the surface. Range, message framing, running status, supported message classes, acknowledgement and return type are unspecified.', 'Use a separately admitted surface and non-destructive valid message owned by an independently documented profile; retain input and actual surface/output response. No arbitrary integer sequence, protocol bytes or success oracle is supplied here.'),
'send_receive_sysex':('Printed parameters sysex_message[list of int],timeout[symbol,int] coexist with prose specifying timeout followed by a float and a default0.2 with no unit in this entry. It awaits a response: ungrabbed timed-out response is not forwarded; grabbed MIDI is always forwarded while timeout is still reported. Exact report grammar, units, response correlation and boundary timing remain U.', 'Establish an independently admitted non-destructive request/response profile; separately propose timely and timed-out responses with MIDI grab off/on, retaining positive send/receive controls. Do not invent a seconds unit, int/float coercion, timeout boundary or response/report order.')},
'DeviceIO':{
'available_routing_channels':('Dictionary get/observe. Printed key available_routing_channels holds a list of dictionaries described by routing_channel. This is an availability listing, not audio-path activation proof.', 'Identify an eligible bus and independently available channel, query/observe available_routing_channels and retain the list/schema before and after a supported routing-context change.'),
'available_routing_types':('Dictionary get/observe. Printed key available_routing_types holds a list of dictionaries described by routing_type; ordering and empty-list meaning are unspecified.', 'Identify an eligible bus and known available type, query/observe available_routing_types, and retain returned identifiers separately from labels and actual signal routing.'),
'default_external_routing_channel_is_none':('Bool get/set, described since Live11:1 means the default channel for External routing types is none. Other values, initialization, persistence and switching/selection side effects are not specified.', 'On an admitted External-routing bus record explicit default state, propose separately accepted boolean settings and change type in reset contexts. Retain resulting selections without presuming current routing changes immediately.'),
'routing_channel':('Dictionary get/set/observe with display_name[symbol] and identifier[symbol]; can be set to values found in available_routing_channels. Label alone is not the stable identity or a complete serialization law.', 'Query the current positive availability list, choose an independently valid alternative channel, propose setting the listed value, and retain query/notification and actual positive routing controls separately.'),
'routing_type':('Dictionary get/set/observe with display_name[symbol] and identifier[symbol]; can be set to values found in available_routing_types. Compatibility with current channel and invalid/stale selection behavior remain U.', 'From a positive available-type listing choose an independently eligible alternative in a reset copy, propose setting that listed value, and retain channel interactions and notifications without a guessed fallback.')},
'Groove':{
'base':('Printed under Children despite primitive int; get/set only. Index-based values are0=1/4,1=1/8,2=1/8T,3=1/16,4=1/16T,5=1/32. Do not silently reclassify as an object child or infer an observable capability.', 'Use one independently loaded groove, query base, and propose each separately admitted printed index on reset copies. Retain actual value/acceptance without deriving beat durations, quantization or timing output.'),
'name':('Printed under Children as symbol get/set/observe; represents the groove name. Encoding, duplicate-name identity and persistence are unspecified.', 'With an admitted groove propose two valid owned names in reset copies, query/observe them, and retain identity independently of display spelling.'),
'quantization_amount':('Printed under Children as float get/set/observe; represents the quantization amount. No unit, accepted range, percent conversion or timing algorithm is provided.', 'Independently establish two accepted distinguishable quantization amounts, propose read/set/observe within those contexts, and retain values separately from any note/signal transformation.'),
'random_amount':('Printed under Children as float get/set/observe; represents random amount. Range, units, random distribution, seed and note correlation are unspecified.', 'Use two independently admitted random-amount settings in reset contexts and retain queried/observed values. No random output inequality, distribution or repeatability oracle is supplied.'),
 'timing_amount':('Printed under Children as float get/set/observe; represents timing amount. Units, scale, extrapolation, mapping and timing transformation remain unknown.', 'Independently admit two valid timing amounts, then propose read/set/observe with fixed valid groove/clip context; retain actual values with no timing comparator.'),
'velocity_amount':('Printed under Children as float get/set/observe; represents velocity amount. Units, signed range, clipping and interaction with notes/groove dynamics remain unknown.', 'On a valid groove independently admit two distinct velocity amounts, propose read/set/observe, and retain property values without replacing finite note velocity/storage laws.')},
'GroovePool':{'grooves':('Child list of Groove, get/observe only; source says top-to-bottom pool order, accessible by index. Empty/stale indices, reordering, loading/removal and notification ordering are unspecified.', 'Establish two independently identified loaded grooves with distinguishable names and visible pool order; query/observe list and inspect accepted indices while preserving identity separately from names.')},
'TuningSystem':{
'name':('Symbol get/set/observe; names the currently active tuning system. Renaming is not evidence of loading a different system or changing pitch.', 'Independently establish an active valid tuning system, propose two admitted names and retain queried/observed name separately from pitch/sound behavior.'),
'pseudo_octave_in_cents':('Float get only; pseudo-octave in cents for the current system. No setter, accepted numerical range or relationship to an octave number is specified.', 'Use an independently loaded system with independently documented pseudo-octave, propose query only, and retain the actual value; no universal1200-cent or octave conversion is inferred.'),
'lowest_note':('Dictionary get/set/observe describing note index within pseudo-octave and octave of the lowest note. Key names, key types, integer ranges and inclusive/exclusive boundary behavior are not supplied.', 'Use a separately admitted complete lowest-note dictionary for an active system; propose get/set/observe with an independently valid alternate boundary, retaining the complete returned structure without invented keys.'),
'highest_note':('Dictionary get/set/observe describing note index within pseudo-octave and octave of the highest note. Missing schema and range/interaction rules remain U.', 'Use an independently admitted complete highest-note dictionary and compatible lower bound, propose get/set/observe in a reset context and retain boundary interactions without constructing an undocumented dictionary.'),
'reference_pitch':('Dictionary get/set/observe for current reference pitch. Keys, units, tuning reference coordinate and validation rules are unspecified.', 'Require an independently admitted reference-pitch dictionary, propose query and accepted alternate setting/observation, and retain full return structure without assuming frequency/note keys or a440Hz default.'),
'note_tunings':('Dictionary get/set/observe; relative note tunings in cents, described as a single-element dictionary holding an array. The key, array size/order, reference meaning and accepted values are not supplied.', 'Require independently admitted complete note-tuning dictionaries for one active system, propose query/set/observe on reset copies and retain complete structure; no array keyed schema or pitch transform is guessed.')}
}
req=[];cases=[];ledger=[]
for e in entries:
 rows=blocks[e['source_id']]
 for member in [m for m in load(M/'lom-members.json') if m['reference_entry']==e['id']]:
  name=member['anchor'];claim,action=D[e['name']][name]
  start=next(i for i,b in enumerate(rows) if b['block']==member['block'])
  end=next((i for i in range(start+1,len(rows)) if rows[i]['tag'] in ['h2','h3']),len(rows))
  context=rows[start:end];rid=f'REQ-LAPI-CONTROL-{len(req)+1:03d}'
  r=dict(id=rid,title=e['name']+'.'+name,provenance='D-current-public',target_applicability='U',contract=claim,reference_entry=e['id'],member=member['id'],declaration=member['heading'],category_as_published=member['category'],source_id=e['source_id'],source_blocks=[b['block'] for b in context],source_url=member['url'])
  req.append(r);cases.append(dict(id=f'LAC-{len(cases)+1:03d}',requirements=[rid],title=r['title'],kind='message-role',preconditions=['owned-context','positive-guard'],setup_and_action=action,source_claim=claim,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False))
  ledger.append(dict(member=member['id'],reference_entry=e['id'],requirements=[rid],cases=[cases[-1]['id']],mapping='partial-direct-documentary-contract',target_applicability='U',semantic_complete=False))
assert len(ledger)==28
r=dict(id='REQ-LAPI-CONTROL-029',title='this_device root context',provenance='D-current-public',target_applicability='U',contract='The root identifies the Device containing the live.path object receiving goto this_device. The entry prints an ordinary track/device canonical path example; nested/return/Main placements and lifetime follow their own evidence, not an all-devices-on-tracks law. The entry declares zero direct members; Device inheritance is routed to its separate owner.',reference_entry='SURF-API-LOM-THIS_DEVICE',member=None,source_id='C74-LOM-THIS_DEVICE',source_blocks=['B0001','B0002','B0003','B0004'],source_url='https://docs.cycling74.com/apiref/lom/this_device/')
req.append(r);cases.append(dict(id='LAC-029',requirements=[r['id']],title=r['title'],kind='message-role',preconditions=['owned-context','positive-guard'],setup_and_action='Independently identify the actual containing Device for an admitted live.path object, propose goto this_device, and retain returned identity and actual canonical path. Nested/return/Main contexts require separately admitted placements; absence is U.',source_claim=r['contract'],documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False))
gaps={
'CONTROL':('Controller ownership, timeout and lifecycle','Surface ordering differs between Application list and root path; script-requested versus realtime forwarding, grab/release ownership, wrong-owner cleanup, disconnect, timeout parameter int/float discrepancy and unspecified units need matched evidence.', ['With independently valid profile/control/message and confirmed ordinary functionality, propose grab/release/disconnect/reconnect in separate reset histories; retain ownership and positive source reception.','Use independently admitted request/response timing profiles to distinguish timely, boundary and late responses with grab off/on; no timing tolerance, response grammar or order is supplied.','Compare independently identified surface IDs using Application listing and root paths under configuration changes; no same-index identity inference.']),
'ROUTING':('Routing dictionary and bus lifecycle','Bus identity/cardinality, dictionary serialization, stale/invalid routing IDs, type/channel interaction, persistence and actual signal/latency outcomes remain unknown.', ['Require independently valid positive bus/type/channel setup; retain accepted dictionaries and actual positive signal paths before proposing a supported selection.','After a separately supported device/configuration change retain current/available values and observers; stale ID response and fallback remain ungraded.','Propose save/reopen or device removal only in an independently owned future disposable context; retain route/observer/positive audio histories, no persistence or latency oracle.']),
'GROOVE':('Groove amounts and pool lifecycle','Printed Children primitives do not establish navigable object children; amount units/ranges/algorithms, pool mutation/identity, probability/timing and commit/persistence remain unknown.', ['With independently admitted grooves/values compare direct get/set/observe capabilities and metadata; do not call object-navigation methods on primitive declarations by assumption.','Use positive MIDI note/groove fixtures through existing groove/MIDI owners before proposing timing/velocity/random comparisons; outputs remain null.','After independently supported groove reorder/removal and save/reopen retain pool IDs/order/indices and source activity; no identity or event-order oracle.']),
'TUNING':('Tuning dictionaries and active-system lifecycle','Missing dictionary keys/units/ranges and empty/no-system behavior prevent complete typed payload contracts; scale/clip/device/pitch conversion and persistence remain unknown.', ['Require independently admitted full active-system dictionaries; retain actual schema and get/set/observe capabilities with positive output, without inventing reference/boundary keys.','Use independently eligible scales/devices/clips and valid note input before proposed system change; retain audio/MIDI/pitch and availability separately, all signal outputs null.','Propose no-system/load/unload/save/reopen in separately admitted disposable contexts; record association, property availability and observer lifetime, not an inferred default or cleanup law.'])}
for key,(title,claim,actions) in gaps.items():
 rid='REQ-LAPI-CONTROL-U-'+key;req.append(dict(id=rid,title=title,provenance='U',target_applicability='U',contract=claim,source_blocks=[]))
 for i,action in enumerate(actions,1):cases.append(dict(id=f'LAC-U-{key}-{i}',requirements=[rid],title=title,kind='unresolved',preconditions=['owned-context','positive-guard'],setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False))
write('requirements.json',req);write('cases.json',cases);write('member-ledger.json',ledger)
write('fixtures.json',{'owned-context':'Future independently owned/admitted valid Live/Max object, Set/profile/device/bus/groove/tuning inputs, exact versions and API capabilities; no patch/example or runtime supplied or executed.','positive-guard':'Before any unchanged/silent/error/exclusion proposal establish available feature/member, valid accepted payload, independent object/control identity and positive input/receiver/output through existing owners. Missing hardware/account/input/route, uninitialized Max, zero gain or failed gate is U, never a passing negative.','limits':'All message/numeric/signal/timing documentary and target comparisons are null. Source_claim is publication data only. No candidate implementation, device script, Max patch, original/API/audio/hardware or network operation occurred.'})
inputs=['manifest-inventory-r1.json','lom-entries.json','lom-members.json','reference-blocks.json','all-sources-r1.json']
write('inventory-pins.json',[dict(path=str((M/n).relative_to(ROOT)),bytes=(M/n).stat().st_size,sha256=sha((M/n).read_bytes())) for n in inputs])
owners=['wiki/specs/live-api-bridge-workflows.md','wiki/specs/remote-control-workflows.md','wiki/specs/push-controller-workflows.md','wiki/specs/routing-monitoring-latency.md','wiki/specs/mpe-workflows.md','wiki/specs/tuning-systems.md','wiki/specs/groove-workflows.md','wiki/specs/midi-editing-tools.md','wiki/specs/midi-note-storage.md','wiki/specs/device-racks.md','wiki/specs/device-parameter-storage.md']
owners=[n for n in owners if (ROOT/n).exists()]
write('owner-pins.json',[dict(path=n,bytes=(ROOT/n).stat().st_size,sha256=sha((ROOT/n).read_bytes())) for n in owners])
write('counts.json',dict(references=6,direct_members=28,documentary_member_contracts=28,direct_members_without_contract=0,semantic_complete_members=0,documentary_root_contracts=1,requirements=33,cases=41,documentary_visible_oracles=0,all_target_null_U_unexecuted=True,source_blocks=sum(map(len,blocks.values()))))
front='---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3; current public API applicability U\n---\n\n'
spec=front.format(id='SPEC-LIVE-API-CONTROL-TUNING',type='spec',status='draft')+'''# Public API control, routing, groove and tuning members

Partial F-05/F-08 contracts for six exact public reference entries,28 explicit
direct member declarations and this_device root context. The publisher index
explicitly names12.4.5; every exact12.4.3 applicability/outcome remains U.
D-current-public records source prose, not a tested API result or complete typed
payload schema. No original application/function, Max/JS/patch/API/script,
candidate, audio/MIDI/hardware or network operation was executed.

[Bridge](live-api-bridge-workflows.md) owns generic path/object/message roles.
[Remote](remote-control-workflows.md), [Push](push-controller-workflows.md),
[routing](routing-monitoring-latency.md), [racks](device-racks.md),
[grooves](groove-workflows.md), [tuning](tuning-systems.md),
[MIDI editing](midi-editing-tools.md) and [notes](midi-note-storage.md) retain
workflow/finite values/storage/signal laws. Device inheritance belongs to the
separate device/rack API owner; no inherited member is flattened or declared
covered here. Groove's primitive members remain under their published Children
category; that placement is not repaired into a different API model.

## Direct documentary contracts

'''
for r in req:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
 if r.get('source_url'):
  spec+=f"Published declaration: `{r.get('declaration','root context')}`; [exact source section]({r['source_url']}); `{r['source_id']}` "+', '.join(r['source_blocks'])+'.\n\n'
spec+='''## Finite acceptance proposals and unresolved contexts

[41 proposed actions](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/cases.json)
cover29 documentary roles and12 explicit U probes across33 requirements. Every
actual message/numeric/signal/timing documentary and target expectation/comparator
is null/U/unexecuted. Actions require [independently admitted positive setups](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/fixtures.json);
source prose is stored separately as source_claim, not used as a fabricated result.

ControlSurface.send_receive_sysex prints int in the timeout parameter annotation
but float in prose and supplies no timeout unit here. Tuning dictionaries omit
keys; Groove amounts omit units/ranges. These gaps stay unresolved, with no
runtime call, invented schema, seconds conversion or numeric comparator.

## Analysis-only evidence and denominator

[Six retained source identities](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/sources.json)
include original URLs/capture timestamps/full hashes and unchanged local paths.
[Exact blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/source-blocks.json)
retain source IDs/HTML lines/columns/anchors. This reuses the independently reviewed
[R1 inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/manifest-inventory-r1.json),
not mutable source-family prose or recaptured pages. [Source/owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/inventory-pins.json)
and [member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/member-ledger.json)
map all28 declarations to partial contracts/cases; zero members are semantically
complete. this_device has zero direct declarations and one separately labeled
root-context contract, not an invented member. Full45-entry/588-declaration
coverage, inheritance, version, lifecycle and legal/profile obligations remain open.
[Author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/manifest-author-r1.json)
freezes this partial packet for independent review.
'''
research=front.format(id='RESEARCH-LIVE-API-CONTROL-TUNING',type='research',status='current')+'''# Public API control and tuning source contexts

The [partial draft](../specs/live-api-control-tuning.md) follows the
[coverage design](full-live-specification-design.md) and [plan](full-live-specification-plan.md).
Root read every retained block for ControlSurface, DeviceIO, Groove, GroovePool,
TuningSystem and this_device. Sources are unchanged reviewed R1 captures;
no recapture, example execution or API/hardware/application/candidate operation.

## Denominator and provenance

Six exact entries expose28 direct declarations: ControlSurface10,DeviceIO5,
Groove6,GroovePool1,TuningSystem6,this_device0. All28 receive a source-specific
partial documentary contract and action; none is semantically complete. The zero-
member root gets a distinct context contract. Four U groups add12 probes, giving
33 requirements/41 cases, all actual documentary/target outputs/comparators null.
The source index states12.4.5, not target12.4.3; published since-version labels
are retained as source claims without proving this runtime or complete support.

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/sources.json),
[blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/source-blocks.json),
[direct-member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/member-ledger.json),
[requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/cases.json)
retain exact locators and action linkage. Owner pins preserve the existing
bridge/remote/Push/routing/rack/groove/tuning/MIDI/notes context. No finite law,
released payload or reference source is revised by adding this packet.

## Source-context questions

- LAC-U-CONTROL: ControlSurface B0002 explicitly distinguishes root-path order
  from Application listing. B0029–0030 timeout annotation int versus prose float
  lacks a unit. Script requests versus realtime track forwarding and ownership/
  disconnect cleanup remain context-dependent; no protocol or timing tolerance.
- LAC-U-ROUTING: DeviceIO dictionaries name display_name/identifier and availability
  wrapper keys, but do not define serialization, stable identity, bus cardinality,
  stale/type-channel fallback or real audio routing. Printed bool1 none-default is
  not a complete current-selection or persistence law.
- LAC-U-GROOVE: six primitive declarations are printed under Children; retain
  category and capabilities without assuming object navigation. Amount units,
  ranges, RNG/quantization/timing/velocity algorithms and pool mutation remain U.
- LAC-U-TUNING: dictionary keys, ordering, range/reference conventions and no-system
  behavior remain missing. A single-element dictionary of cents array is not a
  supplied schema or frequency conversion; existing scale/tuning owners retain laws.

The this_device reference uses a Device root description plus ordinary canonical
path example. No restriction to top-level tracks, inherited member closure or
identity lifetime follows. The broader bridge root-omission question remains open.

## Author freeze and checks

[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-control-tuning/manifest-author-r1.json)
pins source catalogs/blocks, per-member data/actions/ledger, owner/inventory pins,
author script, read-only validator and exact spec/research snapshots. Validation
reproduces source sections from unchanged inventory data, checks original R1
payload hashes, exact28-member set/33 browser IDs/41 null cases, links and whitespace.
A pass establishes author integrity only; independent semantic review is required.
'''
(ROOT/'wiki/specs/live-api-control-tuning.md').write_text(spec)
(ROOT/'wiki/research/live-api-control-tuning.md').write_text(research)
(P/'spec-r1.md').write_text(spec);(P/'research-r1.md').write_text(research)
