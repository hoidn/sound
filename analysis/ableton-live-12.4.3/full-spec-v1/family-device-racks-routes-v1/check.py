"""Read-only retained-DATA checks. No author query, old imports or providers."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import os
import re
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
F=HERE.parent

def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path):return json.loads(path.read_bytes())
def canon(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def guards(ledger,census,sem,nav):
    assert len(ledger['bundles'])==38 and len({x['id'] for x in ledger['bundles']})==38
    assert ledger['counts']==dict(whole_clause_bundles=38,retained_file_S=1,application_none=37,D12_annotations=35,total_context_records=73,X=0)
    assert len(ledger['contexts'])==73
    assert ledger['coverage_open_until_evidence_supports_required_outcomes']
    for key in ['new_native_sites','new_indirect_resolutions','new_body_reads','new_original_calls','new_grades']:assert ledger[key]==0
    assert ledger['selected_successor'] is None
    bundles={x['id']:x for x in ledger['bundles']};contexts=collections.defaultdict(list)
    for x in ledger['contexts']:
        b=bundles[x['bundle']];assert x['requirement']==b['requirement']
        assert x['whole_contract_qualifiers_mandatory'] and x['candidate_case_navigation']==b['case_navigation']
        assert all(x[k] is None for k in ['actual','comparison','new_grade','native_PC'])
        expected='S-retained-file-only' if x['context']=='retained-file' else 'no-established-exact-target-route' if x['context']=='documentary' else 'no-established-route'
        assert x['route']==expected and x['source_annotation_not_extra_outcome']==(x['context']=='documentary')
        contexts[b['id']].append(x['context'])
    for b in ledger['bundles']:
        assert not b['atomic_or_complete_family_denominator'] and b['whole_contract_qualifiers_mandatory']
        assert b['route']==('S-retained-file-only' if b['provenance']=='D-installed' else 'no-established-route')
        assert contexts[b['id']]==(['retained-file'] if b['provenance']=='D-installed' else ['documentary','target-application'] if b['provenance']=='D12' else ['target-application'])
    assert census['counts']==dict(tables=32,slots=115,available_slots=1747,stores=64,aliases=220,memberships=104,alias_memberships=324,named_seed_entries=104,slot_store_frontier_entries=116,call_indirect=220,calls=175,indirect=45)
    assert census['caps']==dict(tables=32,slots=512,stores=128,alias_memberships=512,call_indirect=512)
    assert census['within_caps'] and all(census['counts'][k]<=v for k,v in census['caps'].items())
    assert census['primary_offset_to_top']==0 and len(census['models'])==20 and len(census['small'])==12
    assert census['new_native_site_credit']==0 and not census['actual_public_route'] and census['selected_successor'] is None
    truth=['EACH_chain_and_BOTH_mapped_controls_productive','note_AND_CC_positive_before_selector_exclusion','sustained_NONZERO_no_exit_tail_before_exit','nonempty_active_processing_wet_send_return_output','factory_no_custom_no_preset_initial_eight','factory_Volume_no_user_override_exclusion','factory_sample_drop_Simpler_only','RR01_same_unit_AND_same_range_exception','generic_macro_name_independent_of_unit_exception','parameter_context_ReEnable_selected_AB_state','recognized_successful_save_AND_load_before_absence','Sampler_EXPANDED_always_visible_exception','known_LAST_ADDED_history','NONEMPTY_notes_AND_nonzero_preview','full_clause_and_case_limits_mandatory','coverage_open_until_evidence']
    falsehood=['independent_fade_section_translation_proved','Drum_stored_selector_proves_editor','Random_included_control_must_change','new_Volume_mapping_auto_excluded','HotSwap_exit_restores_old_preset','option_string_proves_recognized_config','plugin_configuration_saves_VALUES','AB_commands_available_on_Rack_Max_plugin','global_ReEnable_substitutes_parameter','returning_AB_state_auto_restores_automation','LAST_ADDED_means_timestamp_or_name_sort','key_fade_case_covers_velocity_and_selector','browser_layer_case_is_pad_to_pad','configured_Multi_is_Receive_change','pan_action_proves_all_mixer_controls','seventh_return_supported','UI_only_requires_audio','metadata_name_proves_numeric_math_body','whole_product_or_family_complete']
    assert set(sem)==set(truth+falsehood)
    assert all(sem[k] is True for k in truth) and all(sem[k] is False for k in falsehood)
    assert len(nav['records'])==101 and nav['old_R3_exact']==81 and nav['new_R4_null']==20
    assert nav['historical_file_roles']==3 and nav['application_roles']==98 and nav['all_actual_U']
    assert nav['documentary_domains']==dict(installed=3,D12=86,U=12) and nav['new_R4_named_UI_pairs']==7 and nav['new_R4_null_pairs']==13
    for x in nav['records']:assert x['actual_expected'] is x['actual_comparison'] is x['new_grade'] is None and x['target']=='U' and not x['executed']

def metadata_guard(row):
    r=row['record']
    if row['kind']=='table-prefix':
        assert r['offset_to_top']==0 and r['native_table_extent'] is None
        assert not r['complete_class_function_or_role_established'] and not r['actual_public_instance_established']
    if row['kind']=='indirect':assert r['resolved_targets']==[]

def read_row(row):
    l=row['locator']
    with (ROOT/l['path']).open('rb') as f:f.seek(l['byte_start']);raw=f.read(l['bytes'])
    assert len(raw)==l['bytes'] and sha(raw)==l['raw_sha256']
    return json.loads(raw)

def main():
    if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no query, authoring, provider or execution mode.')
    ledger,census,sem,nav=[load(HERE/n) for n in ['route-ledger.json','query-census.json','semantic-guards.json','case-navigation.json']]
    guards(ledger,census,sem,nav)
    pins=load(HERE/'pins.json');provider={}
    for p in pins['providers']:
        path=ROOT/p['path'];assert path.suffix in ['.json','.md','.html']
        raw=path.read_bytes();assert len(raw)==p['bytes'] and sha(raw)==p['sha256'];provider[p['path']]=raw
    assert len(provider)==36 and pins['manifest_owner']=='Root' and not pins['snapshot_copies_added']
    owner=load(F/'racks/manifest-author-r5.json');known={p['path']:p for p in owner['files']}
    for p in pins['providers']:
        if p['path'] in known:assert (p['bytes'],p['sha256'])==(known[p['path']]['bytes'],known[p['path']]['sha256'])
    for name,expected in [('racks-owner-r5-review.json','approved-partial'),('racks-owner-r3-review.json','approved-partial'),('racks-source-audit-review.json','approved-partial-source-reconciliation'),('device-chain-source-audit-review.json','approved-partial-source-audit')]:
        assert load(F/'reviews'/name)['disposition']==expected
    q=load(F/'racks/requirements-r4.json');cases=load(F/'racks/cases-r4.json')['cases'];old=load(F/'racks/cases-r3.json')['cases'];actual=load(F/'racks/actual-status-r4.json')['cases']
    assert len(q)==38 and len(cases)==101 and len(old)==81 and cases[:81]==old
    assert len(actual)==101 and all(x['actual_expected'] is x['actual_comparison'] is None and x['target']=='U' and not x['executed'] and not x['complete'] for x in actual)
    text=(F/'racks/spec-r5.md').read_text();clauses=load(HERE/'clause-index.json')['clauses']
    current_pin=next(p for p in pins['as_of'] if p['path']=='wiki/specs/device-racks.md')
    assert sha(text.encode())==current_pin['sha256'] and len(text.encode())==current_pin['bytes']
    assert len(clauses)==38
    for i,(r,b,c) in enumerate(zip(q,ledger['bundles'],clauses)):
        s=b['source'];body=r['contract'];assert r['id']==b['requirement']==c['id'] and s==c['source']
        assert s['pointer']==f'/{i}/contract' and text[s['char_start']:s['char_end']]==body and sha(body.encode())==s['contract_sha256']
        assert text[:s['char_start']].count('\n')+1==s['line']
        assert b['provenance']==('D-installed' if i==0 else 'U' if i in [26,27] else 'D12')
        ids=[x['id'] for x in cases if r['id'] in x['requirements']];assert b['case_navigation']==c['case_navigation']==ids and ids
    for i,(r,c,a) in enumerate(zip(nav['records'],cases,actual)):
        assert r['pointer']==f'/cases/{i}' and r['id']==c['id']==a['id'] and r['object_sha256']==canon(c) and r['requirements']==c['requirements']
        assert r['all_non_source_fields_sha256']=={k:canon(v) for k,v in c.items() if k not in ['source_claim','source_contexts']}
        assert r['source_context_pointers']==c.get('source_contexts',[])
        if i>=81:assert c['actual_expected'] is c['actual_comparison'] is None
    assert sum(c['documentary_expected'] is not None for c in cases[81:])==7
    assert len(os.path.commonprefix([c['setup_action'] for c in cases[61:81]]))==852
    assert len(os.path.commonprefix([c['setup_action'] for c in cases[81:]]))==567
    assert all(c['positive_guard']==cases[61]['positive_guard'] and all(c['positive_guard'].values()) for c in cases[61:81])
    assert all(c['positive_guard']==cases[81]['positive_guard'] and all(c['positive_guard'].values()) for c in cases[81:])
    response=load(F/'racks/response-r5.json');adoption=load(F/'racks/adoption-r5.json')
    assert len(response['exact_field_deltas'])==len(adoption['groups'])==20
    for delta in response['exact_field_deltas']:
        index=int(delta['json_pointer'].split('/')[2]);current=adoption['groups'][index]['remaining_U']
        assert current==delta['after'] and current['historical_source_audit_scope']['as_of']=='AS-OF SOURCE AUDIT'
        assert current['current_owner_adoption']==dict(bounded_new_requirement_IDs=10,bounded_new_cases=20,total_requirement_IDs=38,total_cases=101,metadata_correction_only=True)
    scope=load(HERE/'source-scope.json');assert scope['current_owner_requirements']==38 and scope['current_owner_cases']==101 and scope['source_audit_scope_not_current_owner_denominator'] and not scope['source_pixels_or_destinations_inspected']
    source_count=0
    for catalog,expected in zip(scope['audits'],[(124,264,53,22,4),(153,153,140,20,4)]):
        audit=load(ROOT/catalog['path']);manual=(ROOT/audit['source'].get('path',audit['source'].get('file_pin',{}).get('path',''))).read_text()
        assert (len(audit['blocks']),len(audit['assessments']),len(audit['resources']),len(audit['proposals']),len(audit['source_questions']))==expected
        assert catalog['historical_audit_comparison']==dict(requirements=28,cases=61)
        assert len(catalog['blocks'])==len(audit['blocks'])
        for loc,b in zip(catalog['blocks'],audit['blocks']):
            assert loc['id']==b['id'] and manual[loc['raw_start']:loc['raw_end']]==b['raw_html']
            assert sha(b['raw_html'].encode())==loc['raw_sha256'] and sha(b['text'].encode())==loc['text_sha256']
            source_count+=1
    audit_by_path={c['path']:load(ROOT/c['path']) for c in scope['audits']};source_context_count=0
    for c in cases:
        for loc in c.get('source_contexts',[]):
            assert loc['catalog'] in audit_by_path and re.fullmatch(r'/blocks/\d+',loc['json_pointer'])
            block=audit_by_path[loc['catalog']]['blocks'][int(loc['json_pointer'].split('/')[-1])]
            assert block['id']==loc['block'];source_context_count+=1
    assert source_context_count==189
    # Decode no source or fixture: these are already retained schema/example JSON DATA.
    schema=load(F/'racks/schema-fields.json')['classes'];doc=scope['documentary_file_assertions']
    assert doc['schema_classes']=={k:dict(line=v['line'],field_count=len(v['fields'])) for k,v in schema.items()}
    assert len(schema)==13 and doc['suite_demo_counts']=={'AudioEffectGroupDevice':23,'MidiEffectGroupDevice':1,'InstrumentGroupDevice':8,'DrumGroupDevice':1} and doc['slicing_snapshots']==5
    for k in ['AudioEffectGroupDevice','MidiEffectGroupDevice','InstrumentGroupDevice','DrumGroupDevice']:
        fields={x['name'] for x in schema[k]['fields']};assert all(f'MacroControls.{i}' in fields for i in range(16))
    snap={x['name'] for x in schema['MacroSnapshot']['fields']};assert all(f'{k}.{i}' in snap for k in ['MacroValues','MacroHasValue'] for i in range(16))
    for field in ['suite_demo_creator','slicing_creator']:assert doc[field]['Creator']=='Ableton Live 12.4d1' and doc[field]['MinorVersion']=='12.0_12402'
    component={x['path']:x for x in load(F/'component-resolution-v1/manifest.json')['files']};index={x['path']:x for x in load(F/'component-resolution-v1/packet-inputs.json')['retained_indexes_verified']};authorities={x['path']:x for x in pins['metadata_authority']}
    assert len(authorities)==6
    for path,a in authorities.items():
        parent=index[path] if path in index else component[Path(path).name]
        assert (a['bytes'],a['sha256'])==(parent['bytes'],parent['sha256'])
    md=[json.loads(x) for x in (HERE/'metadata-rows.jsonl').read_text().splitlines()];assert len(md)==640
    assert collections.Counter(x['kind'] for x in md)==dict(**{'table-prefix':32,'store-candidate':64},alias=220,membership=104,call=175,indirect=45)
    models={str(len(x))+x for x in census['models']};small={str(len(x))+x for x in census['small']};points=set();slots=available=0;seen=set();frontier=set();aliases={x['record']['entry']:x for x in md if x['kind']=='alias'};seeds=set(census['named_seeds'])
    for row in md:
        l=row['locator'];assert l['path'] in authorities
        key=(l['path'],l['byte_start'],l['bytes']);assert key not in seen;seen.add(key)
        original=read_row(row);r=row['record'];metadata_guard(row)
        if row['kind']=='table-prefix':
            name=r['literal_type_encoding'];assert name in models|small
            assert all(r[k]==(v[:3] if k=='slots' and name in models else v) for k,v in original.items())
            assert r['available_exported_prefix_slots']==len(original['slots'])
            header=bytes.fromhex(r['raw_header16_hex']);top,ti=struct.unpack('<qQ',header)
            assert top==r['offset_to_top']==0 and ti==int(r['typeinfo'],16)
            assert int(r['address_point'],16)-int(r['table_header'],16)==r['address_point_file_offset']-r['header_file_offset']==16
            assert [s['offset'] for s in r['slots']]==list(range(0,len(r['slots'])*8,8))
            for s in r['slots']:
                assert int.from_bytes(bytes.fromhex(s['raw8_hex']),'little')==int(s['target'],16)
                if s['function']:
                    a=aliases[s['target']];assert a['locator']['line']==s['function']['alias_line'] and a['record']['name']==s['function']['name']
            points.add(r['address_point']);slots+=len(r['slots']);available+=len(original['slots']);frontier.update(s['target'] for s in r['slots'])
        else:assert r==original
        if row['kind']=='store-candidate':frontier.add(r['entry'])
        if row['kind']=='membership':
            a=aliases[r['entry']];assert r['entry'] in seeds and r['source']==[a['locator']['line'],a['locator']['byte_start'],a['locator']['bytes']]
        if row['kind']=='call':assert r['caller'] in seeds
        if row['kind']=='indirect':assert r['function'] in seeds
    assert len(points)==32 and slots==115 and available==1747 and sorted(frontier)==census['frontier_entries']
    assert all(x['record']['address_point'] in points for x in md if x['kind']=='store-candidate')
    pattern=re.compile(r'(?:^|[^A-Za-z0-9_])(?:'+'|'.join(map(re.escape,census['models']+census['small']))+r')::')
    named=set()
    for x in aliases.values():
        r=x['record'];n=any(pattern.search(z) for z in [r['name']]+[s['name'] for s in r['symbols']]);assert n or r['entry'] in frontier
        if n:named.add(r['entry'])
    assert named==seeds and len(seeds)==104 and frontier<=set(aliases)
    edges=load(HERE/'chain-edges.json');assert len(edges['edges'])==11 and edges['integration_boundaries']==['I-05','I-06','I-07','I-08']
    assert all(x['public_route']=='unknown' and not x['runtime_sequence_proved'] and x['new_native_site_credit']==0 for x in edges['edges'])
    edgeids={x['id'] for x in edges['edges']};assert all(set(x['chain_edges'])<=edgeids for x in ledger['contexts'])
    prospective=load(HERE/'prospective-frontiers.json');assert len(prospective['candidates'])==12 and prospective['small_prefix_slots']==55 and not prospective['distinct_algorithms_claim']
    byid={x['id']:x for x in md}
    for x in prospective['candidates']:
        r=byid[x['metadata_id']]['record'];assert r['slots']==x['selected_slots'] and r['address_point']==x['address_point'] and r['literal_type_encoding'] in small
        assert all(not x[k] for k in ['body_math_or_DSP_proof','legal_input_state_ABI','public_route_established','body_or_original_batch_selected'])
        assert x['whole_clause_sources']==[next(c['source'] for c in clauses if c['id']==i) for i in x['owner_clause_navigation']]
    assert prospective['selected_successor'] is prospective['selected_original_batch'] is edges['selected_successor'] is None
    change=load(HERE/'research-change.json');assert change==pins['research_change'];raw=(ROOT/change['path']).read_bytes();prefix=raw[:change['updated_prefix_bytes']];append=raw[change['updated_prefix_bytes']:change['updated_prefix_bytes']+change['append_bytes']]
    assert len(prefix)==21886 and sha(prefix)==change['updated_prefix_sha256'] and sha(prefix.replace(b'updated: 2026-10-20\n',b'updated: 2026-10-19\n',1))==change['original_prefix_sha256']
    assert len(append)==change['append_bytes'] and sha(append)==change['append_sha256']
    negatives=[]
    def reject(name,mutation):
        l,c,s,n=copy.deepcopy((ledger,census,sem,nav));mutation(l,c,s,n)
        try:guards(l,c,s,n)
        except (AssertionError,KeyError):negatives.append(dict(name=name,rejected=True));return
        raise AssertionError('Unsafe mutation accepted: '+name)
    reject('omit whole clause',lambda l,c,s,n:l['bundles'].pop())
    reject('pad outcome from numeric example',lambda l,c,s,n:l['bundles'].append(l['bundles'][0]))
    reject('D12 annotation becomes target S',lambda l,c,s,n:next(x for x in l['contexts'] if x['context']=='documentary').update(route='S-retained-file-only'))
    reject('application clause becomes file S',lambda l,c,s,n:l['bundles'][1].update(route='S-retained-file-only'))
    reject('file assertion becomes actual pass',lambda l,c,s,n:n['records'][0].update(actual_expected=True))
    reject('arbitrary model slot window',lambda l,c,s,n:c['counts'].update(slots=512))
    reject('cap widened to broad census',lambda l,c,s,n:c['caps'].update(tables=1798))
    reject('metadata becomes site credit',lambda l,c,s,n:l.update(new_native_sites=1))
    for key in ['EACH_chain_and_BOTH_mapped_controls_productive','note_AND_CC_positive_before_selector_exclusion','sustained_NONZERO_no_exit_tail_before_exit','RR01_same_unit_AND_same_range_exception','parameter_context_ReEnable_selected_AB_state','recognized_successful_save_AND_load_before_absence','Sampler_EXPANDED_always_visible_exception','NONEMPTY_notes_AND_nonzero_preview','coverage_open_until_evidence']:
        reject(key,lambda l,c,s,n,key=key:s.update({key:False}))
    for key in ['independent_fade_section_translation_proved','Drum_stored_selector_proves_editor','Random_included_control_must_change','new_Volume_mapping_auto_excluded','HotSwap_exit_restores_old_preset','option_string_proves_recognized_config','plugin_configuration_saves_VALUES','AB_commands_available_on_Rack_Max_plugin','global_ReEnable_substitutes_parameter','returning_AB_state_auto_restores_automation','LAST_ADDED_means_timestamp_or_name_sort','key_fade_case_covers_velocity_and_selector','browser_layer_case_is_pad_to_pad','configured_Multi_is_Receive_change','pan_action_proves_all_mixer_controls','seventh_return_supported','UI_only_requires_audio','metadata_name_proves_numeric_math_body']:
        reject(key,lambda l,c,s,n,key=key:s.update({key:True}))
    for kind in ['complete-prefix','guessed-indirect','raw-digest']:
        row=copy.deepcopy(next(x for x in md if x['kind']==('indirect' if kind=='guessed-indirect' else 'table-prefix')))
        if kind=='complete-prefix':row['record']['complete_class_function_or_role_established']=True
        elif kind=='guessed-indirect':row['record']['resolved_targets']=['synthetic-invalid']
        else:row['locator']['raw_sha256']='0'*64
        try:read_row(row) if kind=='raw-digest' else metadata_guard(row)
        except AssertionError:negatives.append(dict(name=kind,rejected=True))
        else:raise AssertionError('Unsafe metadata mutation accepted: '+kind)
    links=0
    for target in re.findall(r'\]\(([^)]+)\)',(HERE/'structure.md').read_text()):
        if target.startswith(('http:','https:','#')):continue
        # The own check result is produced after this successful read-only check.
        if target=='author-check.json' and not (HERE/target).exists():continue
        assert (HERE/target.split('#')[0]).is_file(),target;links+=1
    for p in HERE.iterdir():
        if p.suffix in ['.md','.py','.json','.jsonl']:assert all(x==x.rstrip() for x in p.read_text().splitlines()),p.name
    if (HERE/'manifest.json').exists():
        for x in load(HERE/'manifest.json')['files']:
            raw=(HERE/x['path']).read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
    print(json.dumps(dict(status='PASS-bounded-Rack-family-data-check',whole_clause_bundles_not_atomic=38,cases=101,old_R3_objects_exact=81,new_R4_null_histories=20,all_actual_U=True,file_only_S=1,application_none=37,D12_annotations=35,contexts=73,X=0,metadata_rows=640,tables=32,selected_slots=115,available_prefix_slots=1747,stores=64,aliases=220,memberships=104,named_seeds=104,direct_calls=175,unresolved_indirect=45,providers=len(provider),mechanical_source_spans=source_count,case_source_contexts=source_context_count,R5_metadata_qualifications=20,source_scopes_separate=True,research_prefix_bytes=21886,focused_links=links,negative_controls=negatives,new_source_body_native_original_runs=0,new_native_site_credit=0,selected_successor=None),indent=2))

if __name__=='__main__':main()
