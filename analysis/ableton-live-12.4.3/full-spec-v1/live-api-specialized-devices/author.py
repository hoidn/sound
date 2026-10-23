"""Author bounded specialized-device API roles from retained reference text only."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
M=P.parent/'max-api'
load=lambda p:json.loads(p.read_text())
write=lambda n,x:(P/n).write_text(json.dumps(x,indent=2)+'\n')
sha=lambda b:hashlib.sha256(b).hexdigest()
NAMES=['CompressorDevice','DriftDevice','DrumCellDevice','Eq8Device','Eq8Device.View','HybridReverbDevice','LooperDevice','MaxDevice','MeldDevice','PluginDevice','RoarDevice','ShifterDevice','SpectralResonatorDevice','WavetableDevice']
# Specific omissions and context are not filled from similar members or UI labels.
NOTES={
('CompressorDevice','input_routing_type'):'The setter cross-reference says track available_input_routing_types, while the class also declares its own compressor availability list. Preserve this context question; do not silently repair the owning object.',
('DrumCellDevice','gain'):'Normalized is the only range description here; no zero-to-one domain or gain-to-amplitude mapping is supplied. The class description identifies Drum Sampler; its public class spelling is retained.',
('Eq8Device','edit_mode'):'Channel encoding depends on global_mode: L/R0L1R, M/S0M1S, Stereo0A1B(inactive). No new channel-processing law or inactive-write result follows.',
('Eq8Device.View','selected_band'):'No band-index base, accepted interval or out-of-range policy is supplied.',
('LooperDevice','loop_length'):'The unit and valid empty/recording context are unspecified; do not infer beats, seconds or samples.',
('LooperDevice','tempo'):'The body supplies no explicit unit, accuracy, setter or detector law.',
('LooperDevice','overdub_after_record'):'This is scoped to recording a fixed number of bars; do not generalize it to every stop or free-length recording.',
('MaxDevice','get_bank_parameters'):'Empty slots use -1; bank index -1 denotes Best of. These are parameter indices, not LOM IDs or native storage IDs; list ordering and unsupported bank policy remain ungraded.',
('RoarDevice','routing_mode_index'):'The class introduction repeats Roar Device as its parent type; no recursive or repaired inheritance is flattened here.',
('ShifterDevice','pitch_bend_range'):'Unlike Drift, this member body does not explicitly supply semitone units; keep the MIDI Pitch Mode context without borrowing units.',
('SpectralResonatorDevice','pitch_bend_range'):'The printed body supplies no unit/range. Do not import Drift semitone units or a MIDI bend transform.',
('WavetableDevice','oscillator_2_effect_mode'):'The oscillator2 body supplies no enum. Do not transfer oscillator1 Fm/Classic/Modern indexes by analogy.',
('WavetableDevice','set_modulation_value'):'The printed parameter list contains only target/source indices, although prose describes setting an amount. The missing amount argument/type is U; do not invent a third argument.',
}
FUNCTIONS={
('LooperDevice','clear'):'First independently establish fixed recorded content and working playback with nonzero output, then propose clear on a disposable copy, retaining the untouched content baseline.',
('LooperDevice','double_speed'):'Use independently admitted fixed content and active positive playback; propose double_speed on a reset copy and retain speed/state/audio histories without a timing or waveform comparator.',
('LooperDevice','half_speed'):'Use independently admitted fixed content and active positive playback; propose half_speed on a reset copy without assuming reversibility, limits or interpolation.',
('LooperDevice','double_length'):'With independently established fixed nonempty buffer and working playback, propose double_length on a disposable copy; retain content/length/state without predicting duplication, padding or units.',
('LooperDevice','half_length'):'With independently established fixed nonempty buffer and working playback, propose half_length on a disposable copy; retain content/length/state without predicting truncation, wrap or units.',
('LooperDevice','record'):'Independently establish active audio engine, owned nonzero input, eligible Looper and confirmed input path; propose record and retain input/content/state separately. A state flag alone is not recorded-audio proof.',
('LooperDevice','overdub'):'Require independently admitted existing content and active positive playback plus distinct nonzero incoming signal; propose overdub and retain both layers and state with no mix or timing law.',
('LooperDevice','play'):'Establish independently admitted fixed content and valid positive output path; propose play from separately supported states, retaining content/input histories rather than assuming no-input silence means success.',
('LooperDevice','stop'):'Establish active nonzero playback and an untouched continuing-playback control; propose stop and retain state/output without a ramp, deadline or transport-global law.',
('LooperDevice','undo'):'Independently record distinguishable content before and since an admitted Overdub enable transition; propose one undo then a second on the same admitted history, retaining original content baselines without a transaction or exact-audio oracle.',
('LooperDevice','export_to_clip_slot'):'Independently establish actual fixed audio content, engine on and not-recording state, plus an empty ClipSlot on a non-frozen audio track with admitted LOM ID. Propose export and retain content/slot/state; do not treat the source etcetera as an exhaustive eligibility list.',
('MaxDevice','get_bank_count'):'On an independently admitted initialized Max device with known supported parameter banks, propose count query and retain returned type/value without assuming all devices or banks share a count.',
('MaxDevice','get_bank_name'):'Independently admit a valid bank_index and device bank availability, propose name query, and retain the printed list-of-symbols role without forcing it into one symbol or a locale grammar.',
('MaxDevice','get_bank_parameters'):'Independently admit a populated valid bank and parameter list; propose its query and separately an admitted Best-of bank_index=-1, retaining parameter indices and empty-slot markers without assuming universal Best-of support.',
('WavetableDevice','add_parameter_to_modulation_matrix'):'Independently identify an instrument DeviceParameter and positively admit its is_parameter_modulatable result; propose adding it and retain target-list association. A missing/ineligible parameter is U, not a negative pass.',
('WavetableDevice','get_modulation_target_parameter_name'):'Identify an independently valid present modulation-target index and known target parameter, propose name query and retain the symbol separately from object identity.',
('WavetableDevice','get_modulation_value'):'Independently admit populated matrix and valid target/source indices with known positive modulation context; propose value query in two admitted distinct settings without guessing returned type, units or numeric scale.',
('WavetableDevice','is_parameter_modulatable'):'Use an independently eligible instrument DeviceParameter and known positive modulatability context; propose capability query before any add action. Ineligible/wrong-device objects are separate ungraded contexts.',
('WavetableDevice','set_modulation_value'):'Require independent complete accepted-signature evidence before proposing a valid setter; retain actual printed two-index declaration and missing-amount ambiguity. Until that prerequisite exists, do not construct or execute a guessed call.'}
def build():
 entries=[e for e in load(M/'lom-entries.json') if e['name'] in NAMES]
 assert len(entries)==14
 bs=load(M/'reference-blocks.json');selected={e['source_id']:bs[e['source_id']] for e in entries}
 members=[];req=[];cases=[];profiles=[]
 for e in entries:
  rows=selected[e['source_id']];profiles.append(dict(e,source_inventory_mapping=e['specification'],specification='partial-documentary-only',complete=False,inherited_members='Not flattened; class introduction retained verbatim, Device/View owner separate',class_context=rows[:3]))
  for m in [m for m in load(M/'lom-members.json') if m['reference_entry']==e['id']]:
   start=next(i for i,b in enumerate(rows) if b['block']==m['block']);end=next((i for i in range(start+1,len(rows)) if rows[i]['tag'] in ['h2','h3']),len(rows));body=rows[start:end]
   access=next((b['text'][8:] for b in body if b['text'].startswith('Access: ')),None)
   declared_type=m['heading'][len(m['anchor']):].strip() or None
   prose=[b['text'] for b in body[1:] if not b['text'].startswith('Access: ')]
   # Literal body is evidence data, never a computed oracle or guessed ABI.
   role=' '.join(prose)
   note=NOTES.get((e['name'],m['anchor']),'')
   if e['name']=='WavetableDevice' and declared_type is None and m['category']!='functions':note+=' The published selector heading omits a type; do not fill int from similar selectors.'
   contract=f"For {e['name']}.{m['anchor']}, the published declaration is {declared_type or ('function role; formal argument/result declarations only where printed' if m['category']=='functions' else 'member type not declared here')} with {access or 'function-call role; no property access line'}. Documentary role: {role}"
   contract+=' '+note if note else ''
   contract+=' This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.'
   rid=f'REQ-LAPI-SPECIALIZED-{len(req)+1:03d}';cid=f'LAS-{len(cases)+1:03d}'
   req.append(dict(id=rid,title=e['name']+'.'+m['anchor'],provenance='D-current-public',target_applicability='U',contract=contract,direct_member=m['id'],source_id=e['source_id'],source_blocks=[b['block'] for b in body],source_url=m['url'],documented_type=declared_type,documented_access=access))
   if m['category']=='functions':action=FUNCTIONS[(e['name'],m['anchor'])]
   else:
    action=f"On an independently admitted {e['name']} identify the valid {m['anchor']} context and actual declaration/capabilities ({access}). "
    if access and 'get' in access:action+='Query in two independently admitted distinct valid states, preserving a paired known-good member baseline. '
    if access and 'set' in access:action+='Only after independently admitting a complete accepted typed value, propose one alternate value and separate restore on disposable copies. '
    if access and 'observe' in access:action+='With independently working observer/manual-state-change baselines retain actual notification and state, without event-count/order/cadence predictions. '
    if 'index' in m['anchor'] or 'category' in m['anchor'] or 'preset' in m['anchor']:action+='Independently identify eligible current list/category/preset and actual accepted mapping; no zero-based index or list/palette inheritance is guessed. '
    if note:action+='Retain source caveat: '+note
   cases.append(dict(id=cid,requirements=[rid],kind='function' if m['category']=='functions' else 'property',preconditions=['admitted-context','positive-baseline'],setup_and_action=action,source_claim=contract,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False))
   members.append(dict(m,requirements=[rid],cases=[cid],complete=False,target_unresolved=True,source_body=body,documented_type=declared_type,documented_access=access,argument_declarations=[b for b in body if b['text'].startswith(('Parameter:','Parameters:'))] or None,result_declarations=[b for b in body if 'Return' in b['text']] or None,omission_note='Null formal declaration is not zero arguments/void return; full source body retained. No inherited or analogous member details added.'))
 assert len(members)==108 and len(FUNCTIONS)==19
 gaps=[('VERSION','Versions, class names and inherited surface','Exact12.4.3 applicability and inherited Device/View/root/alias closure remain unknown. DrumCellDevice maps by publisher description to Drum Sampler; Roar introduction repeats its own device name, not a reviewed parent hierarchy.'),('TYPES','Types, ranges and omitted signatures','Wavetable selector types, oscillator2 enum, setter amount signature, Looper buffer units, bend units, dictionary serialization, index bounds and function returns remain unresolved where omitted. No type/default/void or analogue inference.'),('CONTEXT','Routing, categories, banks and presets','Compressor setter track/device cross-reference, category/list dependency, plugin editor/preset capabilities, Max banks/IDs, source changes and invalid/stale/member capability interactions remain unknown.'),('PROCESSING','Composed numeric, signal, timing and recording outcomes','Modulation routing, voice allocation, pitch/MPE/tuning, filtering, normalized gain, IR shaping, speed/length, buffer capture/overdub and export audio remain separate device/workflow owners; no algorithm or tolerance follows.'),('LIFECYCLE','Undo, persistence, initialization and teardown','Malformed values, observer/event sequencing, ownership/source loss, cancellation, save/reopen, Undo except its scoped Looper content role, device reordering and teardown remain unknown.')]
 for key,title,claim in gaps:
  rid='REQ-LAPI-SPECIALIZED-U-'+key;req.append(dict(id=rid,title=title,provenance='U',target_applicability='U',contract=claim,source_blocks=[]))
  for n,action in enumerate(['After independently admitted valid exact-target object/member and positive access baseline, vary one relevant context/type/capability on separate disposable copies; retain accepted signature and result without inferred error or default.','With independently admitted initialized processing, owned nonzero input/content and positive nonmuted output, vary one eligible source/setting/context through existing owners; no audio/MIDI/numeric/timing comparator.','After an independently admitted valid edit and save/reopen/Undo or detach baseline, propose one separately supported lifecycle transition, retaining identity/observer/source state. Missing feature or unsupported action is U, not a passing negative.'],1):cases.append(dict(id=f'LAS-U-{key}-{n}',requirements=[rid],kind='unresolved',preconditions=['admitted-context','positive-baseline'],setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False))
 return profiles,selected,members,req,cases
if __name__=='__main__':
 assert not (P/'manifest-author-r1.json').exists(),'sealed; do not overwrite'
 entries,blocks,members,req,cases=build()
 for n,x in [('profiles.json',entries),('source-blocks.json',blocks),('member-ledger.json',members),('requirements.json',req),('cases.json',cases),('sources.json',[s for s in load(M/'all-sources-r1.json') if s['id'] in blocks])]:write(n,x)
 write('counts.json',dict(reference_entries=14,direct_members=108,partial_direct_mappings=108,semantic_complete_members=0,requirements=len(req),cases=len(cases),source_blocks=sum(map(len,blocks.values())),actual_documentary_target_oracles_null=True))
 write('fixtures.json',{'admitted-context':'Future independently owned initialized exact-version Live/Max device/API, complete accepted signature/payload, actual supported property/function/context and nonempty available list/bank/category/preset; no source example or runtime supplied.','positive-baseline':'Require paired known-good object/member access, observer/manual change and eligible parent/context. Audible/record/export proposals require actual owned content/nonzero input, processing on, nonzero gain and valid nonmuted output/record gates. Missing capability/source/hardware, empty content, disabled engine or zero signal is U, never a passing exclusion.','limits':'All API/message/numeric/signal/timing actual documentary and target oracles null/U; source_claim is publication data only. Figures not inspected. No script/example/Max patch/original/candidate or service/hardware operation ran.'})
 inputs=[M/n for n in ['manifest-inventory-r1.json','lom-entries.json','lom-members.json','reference-blocks.json','all-sources-r1.json']]
 owners=[ROOT/'wiki/specs'/f for f in ['live-api-bridge-workflows.md','live-api-control-tuning.md','dynamics-devices.md','synthesis-instruments.md','filter-eq-devices.md','delay-reverb-devices.md','modulation-pitch-loop-devices.md','distortion-devices.md','max-for-live-hosting.md','plugin-hosting.md','routing-monitoring-latency.md','mpe-workflows.md','tuning-systems.md','midi-note-storage.md','device-racks.md']]
 write('input-owner-pins.json',[dict(path=str(f.relative_to(ROOT)),bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in inputs+owners])
 front='---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3; current public API applicability U\n---\n\n'
 spec=front.format(id='SPEC-LIVE-API-SPECIALIZED-DEVICES',type='spec',status='draft')+'''# Specialized device API declarations

Partial direct-member roles for14 exact current-public references/108declarations.
The publisher index states12.4.5; all exact12.4.3 outcomes/applicability remain U.
Raw publication role text is retained in each clause as documentary data with its
own type/access/context caveats, never an executed result, guessed ABI or complete
branch contract. No original application/function/API/Max/JS/patch/example,
candidate, audio/MIDI/hardware or service operation ran.

[Bridge](live-api-bridge-workflows.md) and [control/routing](live-api-control-tuning.md)
retain generic message/bus roles. [Dynamics](dynamics-devices.md),
[synthesis](synthesis-instruments.md), [filter/EQ](filter-eq-devices.md),
[delay/reverb](delay-reverb-devices.md), [modulation](modulation-pitch-loop-devices.md),
[distortion](distortion-devices.md), [Max hosting](max-for-live-hosting.md),
[plug-in hosting](plugin-hosting.md), [routing](routing-monitoring-latency.md),
[MPE](mpe-workflows.md), [tuning](tuning-systems.md) and [racks](device-racks.md)
retain their workflow, processing, values/storage and lifecycle laws. Generic
Device/View API members are a separate owner: no inheritance is flattened here.

## Documentary direct-member contracts

'''
 for r in req:
  spec+=f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
  if r.get('source_url'):spec+=f"Exact [publication member]({r['source_url']}), `{r['source_id']}` "+', '.join(r['source_blocks'])+'.\n\n'
 spec+='''## Acceptance proposals and source limits

[123 future proposals](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/cases.json)
cover108 source roles and15 U probes across113 requirements. Property actions use
capability-conditioned positive setups and member-specific source context; function
actions retain particular content/routing/modulation/bank/identity prerequisites.
They are partial discovery proposals, not all branches or executable fixture files.
Every actual documentary/target result/comparator is null/U/unexecuted. Published
role text stays in source_claim, not a fabricated API or numeric/signal oracle.

## Analysis-only evidence and denominator

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/sources.json)
retain unchanged original URL/UTC/size/hash and paths relative to max-api inventory.
[Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/source-blocks.json)
and [direct-member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/member-ledger.json)
retain exact locators/types/access/argument/result prose and omission flags. All108
map to a partial clause/action; none is semantically complete. Typed schema,
inherited/root/alias closure, numeric/audio/timing and exact-target obligations
remain open. [Research](../research/live-api-specialized-devices.md) owns the
source-context questions. The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/manifest-author-r1.json)
freezes only this partial scope for independent review.
'''
 research=front.format(id='RESEARCH-LIVE-API-SPECIALIZED-DEVICES',type='research',status='current')+'''# Specialized device API source contexts

The [partial draft](../specs/live-api-specialized-devices.md) follows the
[coverage design](full-live-specification-design.md) and [plan](full-live-specification-plan.md).
Root read all retained text blocks for the14 specialized references. Immutable
R1 API sources were reused without recapture; no source example/API/Max/native/
audio/hardware/candidate operation was executed. The source index explicitly
names12.4.5; target12.4.3 applicability/outcomes remain U.

## Exact denominator and evidence

Fourteen entries/108 direct declarations: Compressor4,Drift29,DrumCell1,Eq8three,
Eq8.View1,HybridReverb8,Looper16,Max7,Meld4,Plugin3,Roar3,Shifter2,
SpectralResonator7,Wavetable20. All108 map to partial documentary roles/cases,
zero semantically complete. Five U groups add15 probes, giving113 requirements/
123 future cases; all actual message/numeric/signal/timing documentary/target
outputs/comparators null. The other31 entries/480declarations and all inherited
surface retain their separate owners or unresolved obligations.

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/sources.json),
[blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/source-blocks.json),
[member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/member-ledger.json),
[requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/cases.json)
retain the exact source body/declaration/access/locators, explicit argument/result
paragraphs and missing-signature caveats. A null formal declaration never means
zero arguments or void. Existing source/workflow/finite owners are independently
pinned; source-family canonical and all R1 inventory bytes remain unchanged.

## Source-context questions

- LAS-U-ROUTING: Compressor input_routing_type refers to track availability despite
  its own compressor list. Preserve object context; no dictionary/identifier repair.
- LAS-U-SIGNATURE: Wavetable set_modulation_value lists only target/source indices
  while describing an amount setter. No third argument or amount type is invented.
  Four wavetable selector headings omit type; oscillator2 effect mode omits enum.
- LAS-U-UNITS: Looper buffer length and tempo, Shifter/Spectral bend ranges and
  normalized DrumCell gain omit complete units/ranges or maps. Drift's explicit
  semitones do not populate other members by analogy; seconds for Hybrid IR
  attack/decay and0..1size are source-specific, not DSP formulas.
- LAS-U-IDENTITY: DrumCell identifies Drum Sampler by source description, not an
  invented alias hierarchy. Roar introduction repeats Roar Device as parent;
  inherited Device/View closure remains separately unresolved.
- LAS-U-CONTEXT: lists/categories/preset/matrix/bank dependencies and indices need
  independently accepted values/context. Max bank index -1 Best-of and empty
  parameter slot -1 are distinct roles, never LOM/storage identities. Looper export
  requires empty slot/non-frozen audio track/engine on/actual fixed content and
  not recording; source etcetera means the list is not an exhaustive gate.

No enum/code/default/type not explicitly in the member is transferred from its
sibling, instrument GUI, native storage or numerical spec. Voice counts/indexes,
modulation routing, pitch, IR envelope, oversampling and normalized values do not
specify their synthesis/filtering/processing algorithms. Private mechanisms and
implementation designs are not adopted from source descriptions.

## Author freeze and review

[Manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/manifest-author-r1.json)
freezes exact data/prose/snapshots and read-only validator. Validation checks
unchanged inventory/source/owner pins,108 exact direct mappings,113 browser IDs,
123 null cases, source spans/snapshots/links/whitespace. Independent semantic
review is pending; integrity or counts cannot close any profile or API surface.
'''
 for f,text in [('wiki/specs/live-api-specialized-devices.md',spec),('wiki/research/live-api-specialized-devices.md',research)]: (ROOT/f).write_text(text)
 (P/'spec-r1.md').write_text(spec);(P/'research-r1.md').write_text(research)
