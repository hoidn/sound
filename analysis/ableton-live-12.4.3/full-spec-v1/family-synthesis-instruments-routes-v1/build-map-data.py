#!/usr/bin/env python3
"""Author bounded data from current owner and approved retained metadata only."""
from pathlib import Path
import json, hashlib, collections, datetime

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
OWNER=BASE/'synthesis-instruments'
def read(path):return json.loads(path.read_text())
def digest(data):return hashlib.sha256(data).hexdigest()
def pin(path,role):
    b=path.read_bytes();return dict(path=str(path.relative_to(ROOT)),bytes=len(b),sha256=digest(b),role=role)
def save(name,data):
    with (HERE/name).open('x') as stream:json.dump(data,stream,indent=2);stream.write('\n')
def canonical_hash(data):return digest(json.dumps(data,sort_keys=True,separators=(',',':')).encode())
reqs=read(OWNER/'requirements-r3.json');cases=read(OWNER/'cases-r3.json')
spec=(OWNER/'spec-r3.md').read_text();lines=spec.splitlines(keepends=True)
assert (ROOT/'wiki/specs/synthesis-instruments.md').read_text()==spec
assert len(reqs)==110 and len(cases)==190
assert all(c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
req_index={r['id']:i for i,r in enumerate(reqs)}
case_index={c['id']:i for i,c in enumerate(cases)}
meta=[json.loads(s) for s in (HERE/'retained-metadata.jsonl').read_text().splitlines()]
by_kind=collections.defaultdict(list)
for row in meta:by_kind[row['kind']].append(row)
census=read(HERE/'metadata-scope-census.json');approval=read(HERE/'scope-approval-root.json')
assert digest((HERE/'scope-approval-root.json').read_bytes())=='ca9060260a68e7f279a583aa0948058772fcd908f4a1af996e77882139893666'
assert digest((HERE/'metadata-scope-census.json').read_bytes())==approval['census']['sha256']
fixtures=read(OWNER/'fixtures-r3.json');overlay=fixtures['current_version_overlay']
assert [x['id'] for x in overlay['actual_oracles']]==[x['id'] for x in cases]

# Fresh source geometry only. No inherited source judgments/proposals are executed or re-audited.
audit_path=BASE/'synthesis-instruments-source-audit/audit.json'
audit=read(audit_path);blocks=audit['blocks'];assert len(blocks)==567
manual_path=BASE/'sample-instruments/manual-instruments-2026-10-19.html'
manual_raw=manual_path.read_bytes();assert digest(manual_raw)=='3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a'
manual=manual_raw.decode('utf-8')
local=read(OWNER/'manual-locators.json');geometry=[];block_by_local={};ordinal=0
for profile,count in [('drift',95),('drum-sampler',54),('meld',96),('operator',211),('wavetable',111)]:
    for i in range(1,count+1):
        block=blocks[ordinal];key=profile+':B%03d'%i;loc=local[key]
        assert loc['text']==block['text'] and loc['html_line']==block['html_line']
        a,b=block['raw_start'],block['raw_end'];raw_html=block['raw_html']
        assert 0<=a<b<=len(manual) and manual[a:b]==raw_html
        assert manual.count('\n',0,a)+1==block['html_line']
        assert a-(manual.rfind('\n',0,a)+1)==block['html_column']
        g=dict(id=key,audit_pointer='/blocks/'+str(ordinal),global_source_id=block['id'],
               html_line=block['html_line'],html_column=block['html_column'],
               raw_character_start=a,raw_character_end=b,raw_html_sha256=digest(raw_html.encode()),
               text_sha256=digest(block['text'].encode()),kind=block['kind'])
        geometry.append(g);block_by_local[key]=g;ordinal+=1
refs=0
for case in cases:
    for ref in case.get('source_references',[]):
        n=int(ref['pointer'].split('/')[-1]);assert blocks[n]['id']==ref['block_id'] and blocks[n]['text']==ref['quote'];refs+=1
assert ordinal==567 and refs==354
save('source-geometry.json',dict(scope='Fresh mechanical raw-span/line/column/local-source/354 current-case quote joins only;567-source semantics and corrected associations inherited from approved Source R2.',
                              source=pin(manual_path,'retained D12 manual; exact target applicability unknown'),
                              audit=pin(audit_path,'inherited source audit; no full semantic re-audit'),
                              local_locators=pin(OWNER/'manual-locators.json','source metadata'),
                              blocks=geometry,case_reference_occurrences=354,case_unique_source_pointers=343,
                              source_texts_semantically_reaudited=0,source_images_or_link_destinations_inspected=0))

clauses=[]
for i,r in enumerate(reqs):
    rid=r['id'];body=r['contract'];related=[dict(id=c['id'],pointer='/'+str(j)) for j,c in enumerate(cases) if rid in c['requirements']]
    if rid.endswith('LIFECYCLE'):
        start=next(n for n,s in enumerate(lines) if s.startswith('### '+rid+' '));end=start+3
    else:
        matching=[n for n,s in enumerate(lines) if body in s];assert len(matching)==1,(rid,matching)
        start=end=matching[0]
    clauses.append(dict(id=rid,requirement_pointer='/'+str(i),contract_pointer='/'+str(i)+'/contract',
                        contract_characters=len(body),contract_sha256=digest(body.encode()),device=r['device'],
                        source_annotation=r['provenance'],target_applicability='U',
                        owner_file='synthesis-instruments/spec-r3.md',owner_lines=[start+1,end+1],
                        owner_span_sha256=digest(''.join(lines[start:end+1]).encode()),
                        source_blocks=r['source_blocks'],cases=related,
                        case_link_scope='Same-requirement navigation only; not every case exercises every predicate.'))
case_nav=[]
for i,c in enumerate(cases):
    fields={k:dict(characters=len(v),sha256=digest(v.encode()),pointer='/'+str(i)+'/'+k) for k,v in c.items() if isinstance(v,str) and k not in ['id','device','kind','target_grade','fixture','provenance','adoption_group']}
    case_nav.append(dict(id=c['id'],pointer='/'+str(i),device=c['device'],kind=c['kind'],requirements=c['requirements'],
                         object_sha256=canonical_hash(c),field_spans=fields,source_blocks=c['source_blocks'],fixture=c['fixture'],
                         documentary_comparator_named=c['documentary_comparator'] is not None,
                         actual_expected=None,actual_comparison=None,target_grade='U',executed=False))
save('clause-index.json',dict(owner_revision=3,requirements=clauses,cases=case_nav,
                           current_version_overlay_pointer='synthesis-instruments/fixtures-r3.json#/current_version_overlay',
                           source_geometry='source-geometry.json',case_rows_are_not_outcome_denominator=True))

family_by_ap={t['address_point']:t['family'] for t in census['table_proposal']['tables']}
components=[]
for row in by_kind['class-table-header']:
    d=row['record'];ap=d['address_point'];slots=[x for x in by_kind['class-slot'] if x['record']['address_point']==ap]
    stores=[x for x in by_kind['literal-store-candidate'] if x['record']['address_point']==ap]
    components.append(dict(id='SC%02d'%(len(components)+1),device=family_by_ap[ap],
                           literal_type_encoding=d['literal_type_encoding'],address_point=ap,
                           header_metadata=row['id'],slot_metadata=[x['id'] for x in slots],
                           literal_store_metadata=[x['id'] for x in stores],
                           selected_entries=[x['record']['target'] for x in slots],
                           ownership='literal type/class association only; actual processor/model/current voice owner unknown',
                           classification='observed-static metadata; semantic family role inferred from exact qualified literal',
                           actual_instance=False,receiver_ABI='unknown',native_extent=None,C_body_locator=None,
                           complete_callable_leaf=False,public_route_credit=0))
save('components.json',dict(scope='32 Root-selected primary metadata candidates only; all other class/adjusted receiver contexts unselected, not absent.',components=components))

chain=[
 ('SY01','Document/preset resource vocabulary','Admitted loaded instrument instance','unknown','Stored root/field names and supplied preset metadata do not establish version admission, constructor defaults, loading or legal media/voice state.','synthesis-instruments/spec-r3.md lines23-41,303-310','Document owns storage; actual instrument instance/provider/receiver owner unknown'),
 ('SY02','I03/I04 playback note/event dispatch','Same synthesis processor and active-note owner','unknown','101ab5cec due-event virtual+0x10 has no exact selected device receiver/event codec/timebase join. A NoteOn/Off wrapper name is not that join.','integration-structure-v1/mix-component-edges.json#/execution_interfaces/0','Playback owns due events; actual per-note/device/voice ownership unknown'),
 ('SY03','I05/I06 stored/logic envelope values','Current synthesis parameter/control target','unknown','Stored values/E(t)/ideal P(t) are distinct from loaded provider units, clip/song time, control sampling and ramped samples; A3/A6/A8 remain.','family-automation-routes-v1/structure.md#keep-the-value-and-time-boundaries-separate','Automation owns stored/evaluated values; actual parameter provider/current device target unknown'),
 ('SY04','Generic instantiated device chain','Mix unit InL/R','unknown','No exact synthesis instance/voice/output buffer supplies unit+0x168/+0x170 merely because a processor/module name exists.','integration-structure-v1/mix-component-edges.json#/edges/5','Instrument should own voice/output state; concrete owner/chain unknown'),
 ('SY05','Mix unit InL/R','Constructed TrackOut member','observed-static','102731438 C1482-1489 registers inputs; C1898-1903 links unit+0x168/+0x170 to TrackOut+0x428. This is local construction under helper/receiver/lifetime premises, not runtime device delivery.','integration-structure-v1/mix-component-edges.json#/edges/5','Mix builder owns constructed unit fields; actual reached processor receiver unknown'),
 ('SY06','TrackOut local wrapper/destinations','Main bus/export/host output','unknown','101b1c114 and101b1afbc local input/state/output expressions do not bind actual main/send destinations or callback order.','family-mix-routes-v1/structure.md#state-data-and-call-chain-boundaries','Mix local referenced state known conditionally; host/device output owner and clock unknown'),
 ('SY07','Exact RTTI/address-point candidate','Selected exported slot target','observed-static','32 structural metadata headers/124 selected prefix slots constrain candidate membership only; no physical receiver/slot/native-PC/ABI proof. Large leading3 are construction/lifetime prefix only.','components.json','Metadata candidate type association; no runtime data owner proved'),
 ('SY08','Lexical literal-store candidate','Actual constructor/current vptr/receiver','unknown','50 stored-address lexical quotes retain source-line/hash/warnings but no full C/native body or receiver/lifetime proof.38 extra store-only entries are not followed.','retained-metadata.jsonl kind literal-store-candidate','Construction/state lifetime unknown'),
 ('SY09','Selected source entry','One-hop indexed direct target','observed-static','246 direct call-index references from exact115 approved sources. Targets are next frontier only; no execution order, preserved receiver, arguments or callee semantics inferred.','retained-metadata.jsonl kind outgoing-call','Caller/target addresses are index metadata; actual argument/state transfer unknown'),
 ('SY10','Selected computed call/jump site','Unresolved target','unknown','37 indirect rows:26 calls and11 jumps, all empty resolved targets. No global/slot or encountered-callee query selected; no new resolved-site credit.','retained-metadata.jsonl kind indirect','Current receiver, vptr and dispatch-state ownership unknown'),
 ('SY11','UI command/control gesture','Same loaded/current selected engine/parameter','unknown','Type/menu/enum/field/callback names do not establish actual offered control, gesture dispatch, selected engine, units or resulting visible/audio state.','synthesis-instruments/spec-r3.md lines352-373','UI owns selections/gestures; actual current model/control receiver unknown'),
 ('SY12','Sample/AMS/wavetable resource or media source','Admitted productive synthesis/sample consumer','unknown','DrumCell/InstrumentVector/schema roots and presets do not establish valid current media admission, preprocessing, samples/positions, waveform import/export, source loss or consumer identity.','family-sample-instruments-routes-v1/structure.md','Media/container owners distinct from actual sample/oscillator/voice buffers'),
 ('SY13','Device/voice/control state transition','Undo/save/reopen/cancel/teardown/error result','unknown','Named stored state, flags, callbacks and lexical destructors do not establish transaction grouping, rollback, active-note cleanup, errors, resource release or history continuity.','synthesis-instruments/spec-r3.md lines226-250','Document/history/media/voice resource owners not composed by generic edges'),
 ('SY14','Typed Wavetable oscillator specialization metadata','Accepted oscillator/interpolation/phase/unison algorithm','unknown','All8 exact specializations/whole6-slot exported prefixes are retained as metadata. Typed names and template enum numerals are not current algorithm/domain/phase/output proof.','components.json selected eight WavetableUnisonOscillator candidates','Actual oscillator/current table/voice/history state and consumer unknown')]
edges=[dict(id=a,source=b,target=c,status=d,reason=e,evidence=f,state_and_data_owner=g) for a,b,c,d,e,f,g in chain]
save('chain-edges.json',dict(scope='Family cut extending approved1a/1b I07/I08, Playback/Automation/Mix/sample boundaries; not a disconnected new runtime graph.',edges=edges,
                           all_public_required_bindings='unknown',new_resolved_sites=0,
                           inherited_indirect_inventory=dict(exported_reference_sites=25071,conditional_additions=24,combined=25095,all_sites=268015),
                           no_new_C_native_provider_original_or_callee_global_slot_execution=True))

units=[]
for n,text in enumerate((HERE/'predicate-units.txt').read_text().splitlines(),1):
    if not text or text.startswith('#'):continue
    suffix,rest=text.split('|',1);anchor,predicate=rest.split(' :: ',1);rid='REQ-SYN-'+suffix
    r=reqs[req_index[rid]];start=r['contract'].index(anchor)
    units.append(dict(requirement=rid,device=r['device'],predicate=predicate,unit_source_line=n,
                      contract_anchor=dict(start=start,end=start+len(anchor),sha256=digest(anchor.encode())),
                      context='Current owner clause and linked admitted mode/state histories; same-clause cases are navigation, not exhaustive predicate exercises.',
                      lifecycle_context=None,case_context=None))
life=read(HERE/'lifecycle-predicate-units.json')['units']
for r in reqs:
    if not r['id'].endswith('LIFECYCLE'):continue
    prefix=r['id'].split('-')[2]
    for kind,predicates in life.items():
        cid='SYN-'+prefix+'-U-'+kind;case=cases[case_index[cid]]
        for predicate in predicates:
            units.append(dict(requirement=r['id'],device=r['device'],predicate=predicate,
                              unit_source_line=None,contract_anchor=None,lifecycle_context=kind,
                              context='Required per-device lifecycle predicate in the canonical ten-context obligation; concrete action/state remains at the referenced existing case, not copied or executed.',
                              case_context=dict(id=cid,pointer='/'+str(case_index[cid]),unknown_pointer='/'+str(case_index[cid])+'/unknown',unknown_sha256=digest(case['unknown'].encode()))))
assert len(units)==585
doc_count=sum(u['lifecycle_context'] is None for u in units)
outcomes=[]
for i,u in enumerate(units,1):
    rid=u['requirement'];ci=req_index[rid];r=reqs[ci];device=u['device']
    ids=[x['id'] for x in clauses[ci]['cases']]
    gaps=['SY01','SY02','SY03','SY04','SY06','SY11']
    if u['lifecycle_context']:gaps=['SY01','SY02','SY03','SY04','SY06','SY12','SY13']
    if any(t in u['predicate'].lower() for t in ['sample','wavetable','ams','import','media']):gaps+=['SY12']
    if device=='Wavetable':gaps+=['SY14']
    missing='No exact legal '+device+' instance/receiver, current control/mode and actual event/gesture delivery bind this required predicate. Selected metadata and generic I07/I08 construction do not establish its public state/audio/output result.'
    if u['lifecycle_context']:missing='Required '+device+' '+u['lifecycle_context']+' result lacks admitted same-device/history/voice/media transaction and observable output binding; names, stored fields and generic construction do not establish this transition/error law.'
    row=dict(id='SI%04d'%i,requirement=rid,clause_pointer='/requirements/'+str(ci),device=device,
             observable=u['predicate'],source=dict(requirements='synthesis-instruments/requirements-r3.json',pointer='/'+str(ci)+'/contract',
                                                  body_sha256=clauses[ci]['contract_sha256'],contract_anchor=u['contract_anchor'],
                                                  owner_lines=clauses[ci]['owner_lines'],unit_definition_file='lifecycle-predicate-units.json' if u['lifecycle_context'] else 'predicate-units.txt',
                                                  unit_source_line=u['unit_source_line']),
             context=u['context'],lifecycle_context=u['lifecycle_context'],case_context=u['case_context'],
             existing_cases=ids if not u['case_context'] else [u['case_context']['id']],
             case_links_are_navigation_only=True,source_annotation=r['provenance'],target_grade='U',
             route='no-established-route',route_is_inventory_not_grade=True,
             route_evidence=dict(integration_cut=['SY04','SY05','SY06'],metadata_component_ids=[x['id'] for x in components if x['device']==device],
                                 metadata_and_body_boundary='Observed-static index/class/store association only; new C/native body locator null; no self-contained computation or public binding established.'),
             missing_join_ids=list(dict.fromkeys(gaps)),missing_join=missing,
             premises=['Independently admitted actual offered control/mode and legal current instance/state/history; unknown if unavailable.',
                       'UI-only operations need no audio/hardware; actual gesture differs from configuration/inspection.',
                       'Signal/absence/zero/loss/order require EACH/BOTH independent identifiable productive NONEMPTY source/voice/target, NONZERO control and nonmuted output first.',
                       'No schema/preset/class/template alias becomes runtime identity, control units, default, voice count or algorithm proof.',
                       'Target FP/library/ABI/clock/rate/block/state ownership and output consumer remain unknown; no ARM/x86 or cross-device transfer.'],
             enumerable_inputs=dict(existing_action_pointers=['synthesis-instruments/cases-r3.json#/'+str(case_index[x])+'/setup_and_action' for x in (ids if not u['case_context'] else [u['case_context']['id']])],
                                    native_function=None,legal_call_inputs=None,execution_ready=False,reason='Case recipes are future documentary contexts, not native ABI/legal setup/oracles. No numerical/call batch selected.'),
             actual_expected=None,actual_comparison=None,executed=False,grade_change=0)
    if rid=='REQ-SYN-ME-003':row['current_qualification']='fixtures-r3.json#/current_version_overlay/unit_qualification and spec-r3.md lines360-365 override broad historical degree-unit wording; only semitone indicator st->sd adopted.'
    if rid in ['REQ-SYN-OP-011','REQ-SYN-OP-012']:row['restart_qualification']='Loop overview current-to-Peak versus LoopTime Sustain-to-Initial and Beat/Sync contexts unresolved; no selected law. OP011 unresolved summary is not counted again beyond OP012 mode-context predicates.'
    outcomes.append(row)
save('route-ledger.json',dict(schema='bounded-synthesis-required-predicate-route-ledger-v1',owner_revision=3,
                             required_inventory_scope='Only current five-profile110-clause stated observable/context scope;585 units are inventory, not grades/atomic whole-product denominator.',
                             required_predicates=len(outcomes),documentary_D12_annotations=doc_count,
                             route_counts={'X-route':0,'S-route':0,'no-established-route':len(outcomes)},
                             source_annotations=dict(collections.Counter(x['source_annotation'] for x in outcomes)),
                             requirements=110,cases=190,all_actual_U=True,source_semantics_inherited=True,
                             outcomes=outcomes,auxiliary_helpers_are_not_required_outcomes=True,
                             unresolved_enumeration=[
                              dict(scope='Continuous oscillator/filter/envelope/modulation/FP/RNG/time domains and histories',status='required unknown; accepted native inputs, metrics/tolerances and full branch product not enumerated',owner_lines=[264,267]),
                              dict(scope='Unspecified accessibility, complete factory-content, CPU/load/performance and feature-availability contexts',status='current owner identifies uncovered/partial nouns without bounded observable/context predicates; finer enumeration unresolved, never declared complete/excluded',owner_lines=[264,267]),
                              dict(scope='Source-context parity and current menu/type availability',status='D12 is not exact12.4.3; Meld24/25/Chord/six-aware contexts remain unresolved',owner_lines=[273,288])],
                             no_route_means='No established complete public route under ADR0003 and these selected premises; not global impossibility or exclusion.',
                             required_unsupported='U',coverage_gate='OPEN',documentary_complete_fallback=False,
                             new_grade_site_norm_case_release=0,successor_selected=False))

frontiers=[]
for entry in approval['exact_call_seed_entries']:
    alias=next(x for x in by_kind['alias'] if x['record']['entry']==entry)
    refs=[x['id'] for x in meta if x['kind'] in ['outgoing-call','indirect'] and x['record'].get('caller',x['record'].get('function'))==entry]
    frontiers.append(dict(entry=entry,alias_metadata=alias['id'],one_hop_metadata=refs,
                          C_locator=None,native_extent=None,whole_callable_leaf=False,public_route=False,
                          legal_inputs=None,expected_result=None,
                          missing=['Selected body/actual role and finite side-effect dependencies','Valid native ABI/legal constructed receiver/state/media/voice/clock','Admitted parameter units and output consumer','Independent oracle/FP/library policy and any applicable construction/setup gate']))
save('prospective-frontiers.json',dict(scope='Auxiliary fixed metadata frontiers only; no source/body/input/model/original successor selected.',
                                     complete_callable_X_leaves=0,complete_callable_math_leaves=0,
                                     approved_one_hop_entries=frontiers,store_only_unfollowed=[x['entry'] for x in census['seed_metadata'] if x['roles']==['literal-store-candidate']],
                                     named_wrappers=[x['entry'] for x in census['named_frontier_rule']['entries']],
                                     eight_typed_Wavetable_variants='All8 primary candidates/whole6-slot exported prefixes retained; no algorithm/enum/unit/phase/DSP proof.',
                                     execution_inputs_or_metrics_adopted=0,successor_selected=False))

predecessors=['component-resolution-v1/manifest.json','integration-structure-v1/manifest.json',
 'integration-structure-v1/mix-structure.md','integration-structure-v1/mix-component-edges.json',
 'family-mix-routes-v1/manifest.json','family-mix-routes-v1/structure.md',
 'family-automation-routes-v1/manifest.json','family-automation-routes-v1/structure.md',
 'family-sample-instruments-routes-v1/manifest.json','family-sample-instruments-routes-v1/structure.md',
 'reviews/integration-structure-v1-review.json','reviews/family-mix-routes-v1-review.json',
 'reviews/family-automation-routes-v1-review.json','reviews/family-sample-instruments-routes-v1-review.json',
 'synthesis-instruments/manifest-author-r3.json','synthesis-instruments/spec-r3.md',
 'synthesis-instruments/requirements-r3.json','synthesis-instruments/cases-r3.json',
 'synthesis-instruments/fixtures-r3.json','synthesis-instruments/manual-locators.json','synthesis-instruments/sources.json',
 'synthesis-instruments-source-audit/manifest-r2.json','synthesis-instruments-source-audit/audit.json',
 'reviews/synthesis-instruments-source-audit-review.json','reviews/synthesis-instruments-source-audit-r2-review.json',
 'reviews/synthesis-instruments-owner-r3-review.json']
save('pins.json',dict(scope='Minimal selected predecessors/current providers only; no full prior payload universe replay or copied spec snapshot.',
                     pins=[pin(BASE/n,'immutable predecessor or selected data provider; historical pending flags remain history') for n in predecessors]+[
                         pin(ROOT/'wiki/specs/synthesis-instruments.md','current owner as-of'),
                         pin(ROOT/'wiki/research/synthesis-instruments.md','canonical context as-of; not future gate'),
                         pin(ROOT/'wiki/research/full-live-specification-plan.md','amended rev4 selector as-of; not future gate')],
                     main_ARM64_identity_inherited='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad',
                     no_image_tool_chunk_or_unselected_provider_reads=True))
print(json.dumps(dict(requirements=110,cases=190,predicates=len(outcomes),doc_annotations=doc_count,
                      lifecycle_predicates=len(outcomes)-doc_count,source_geometry=567,metadata_rows=664,
                      routes={'X':0,'S':0,'none':len(outcomes)},coverage='OPEN'),indent=2))
