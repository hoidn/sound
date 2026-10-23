"""Read-only stdlib data integrity. No inherited helpers or execution providers."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def canonical(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()


def read_selected_row(wrapper):
    loc = wrapper['locator']
    with (ROOT / loc['path']).open('rb') as stream:
        stream.seek(loc['byte_start'])
        raw = stream.read(loc['bytes'])
    assert raw.endswith(b'\n') and sha(raw) == loc['raw_sha256'], wrapper['id']
    return json.loads(raw)


def metadata_guards(metadata, calls):
    for wrapper in metadata:
        if wrapper['kind'] == 'table-prefix':
            rec = wrapper['record']
            assert not rec['complete_class_or_function_established']
            assert not rec['actual_public_instance_established']
            assert rec['native_table_extent'] is None
    for wrapper in calls:
        if wrapper['kind'] == 'indirect':
            assert wrapper['record']['resolved_targets'] == []


def guards(ledger, census, scope, fixtures):
    assert len(ledger['requirements']) == ledger['full_clause_count'] == 63
    assert len(ledger['case_navigation']) == ledger['full_case_count'] == 102
    assert ledger['required_application_predicates'] == ledger['application_no_established_route'] == len(ledger['predicates']) == 350
    assert ledger['required_S'] == ledger['required_X'] == 0
    assert ledger['documentary_annotations_not_extra_outcomes'] == 221
    assert len(ledger['contexts']) == ledger['total_context_records'] == 571
    assert not ledger['atomic_or_product_denominator']
    assert ledger['source_metadata_fixtures_not_required_outcomes']
    assert ledger['selected_successor'] is ledger['new_grade'] is None
    predicates = {r['id']:r for r in ledger['predicates']}
    assert len(predicates) == 350
    assert set(predicates) == {p for r in ledger['requirements'] for p in r['predicate_ids']}
    contexts = collections.defaultdict(list)
    for r in ledger['contexts']:
        pred = predicates[r['predicate_id']]
        assert r['requirement'] == pred['requirement'] and r['missing_joins'] and r['chain_edges']
        assert r['actual'] is r['comparison'] is r['new_grade'] is r['native_PC_basis'] is None
        assert r['route_basis']['case_set_is_input_navigation_not_outcome_count']
        assert r['state_data_ownership']
        if r['context'] == 'documentary':
            assert r['route'] == 'no-established-exact-target-route'
            assert r['source_annotation_not_extra_outcome'] and r['documentary_evidence'] == 'D12'
        else:
            assert r['context'] == 'target-application' and r['route'] == 'no-established-route'
            assert not r['source_annotation_not_extra_outcome'] and r['documentary_evidence'] is None
        contexts[pred['id']].append(r['context'])
    for r in predicates.values():
        assert contexts[r['id']] == (['documentary','target-application'] if r['evidence_kind']=='D12' else ['target-application'])
        assert r['numeric_examples_and_choice_instances_not_extra_predicates']
    assert census['selected_counts'] == {'table-prefix':32,'store-candidate':59,'alias':222,'membership':118}
    assert census['selected_tables'] == census['caps']['tables'] == 32
    assert census['selected_slots'] == 93 <= census['caps']['selected_slots'] == 512
    assert census['available_prefix_slots'] == 512 and census['omitted_prefix_slots'] == 419
    assert census['model_prefixes'] == census['small_prefixes'] == 16
    assert census['model_selected_slots'] == 41 and census['small_selected_slots'] == 52
    assert 59 <= census['caps']['stores'] == 128
    assert census['combined_alias_membership'] == 340 <= census['caps']['aliases_memberships'] == 512
    assert census['call_rows'] == 92 and census['unresolved_indirect_rows'] == 57
    assert census['combined_call_indirect'] == 149 <= census['caps']['call_indirect'] == 512
    assert census['boundary_seed_count'] == len(census['boundary_seeds']) == 118
    assert census['new_body_reads'] == census['new_native_reads'] == census['new_native_site_credit'] == 0
    assert not census['actual_application_route'] and census['selected_successor'] is None
    assert scope['fresh_full_requirement_bodies'] == 63 and scope['fresh_full_cases'] == 102
    assert scope['source_blocks'] == len(scope['block_locators']) == 309
    assert len(scope['correction_fields']) == 18 and scope['resource_roles'] == 104
    assert scope['old_owner_objects'] == 61 and scope['old_cases'] == 88
    assert scope['new_null_history_cases'] == 14
    assert scope['adopted_source_groups'] == 13 and scope['other_source_groups'] == 20
    assert not scope['pixels_inspected'] and not scope['new_source_equations']
    expected = {'D12_is_exact_target_S':False,'fixture_header_proves_application_admission':False,
        'Wave_or_schema_proves_audio_output':False,'chooser_display_is_chooser_invocation':False,
        'WarpAs_setup_is_button_action':False,'unlooped_End_applies_to_enabled_loops':False,
        'Volume_End_control_invented':False,'Volume_LFO_positive_proves_Filter_route':False,
        'Sampler_main_Filter_positive_proves_all_modulation':False,'Spread_latch_transferred_to_Sampler':False,
        'Impulse_per_sample_latch_applies_to_globals':False,'Impulse_Gate_is_Simpler_FadeOut':False,
        'middle_six_Impulse_notes_invented':False,'retained_4sec_fixture_extended':False,
        'REX_Pack_hardware_provisioned':False,'UI_only_requires_audio':False,'new_actual_oracle':False,
        'excluded_native_type_removes_required_context':False,'proper_independent_productive_paths_required':True}
    assert scope['semantic_guards'] == expected
    assert len(fixtures['records']) == fixtures['auxiliary_S_records'] == 5
    assert fixtures['application_route_credit'] == 0 and fixtures['selected_original_batch'] is None
    for r in fixtures['records']:
        assert r['route'] == 'S-retained-fixture-only'
        assert not r['actual_Live_output'] and not r['counts_as_required_predicate']
        if r.get('header_bytes'):
            assert r['declared_frames'] == 192000 and r['rate'] == 48000
            assert not r['signal_samples_decoded']


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no execution, provider or write mode.')
    ledger,census,scope,fixtures,pins = [load(n) for n in ['route-ledger.json','query-census.json','source-and-read-scope.json','fixture-routes.json','pins.json']]
    guards(ledger,census,scope,fixtures)
    providers = {}
    for pin in pins['providers']:
        path = ROOT / pin['path']
        assert path.suffix in {'.json','.md','.html'}
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'],pin['id']
        providers[pin['id']] = raw
    assert len(providers) == 31 and pins['manifest_owner'] == 'Root' and not pins['snapshot_copies_added']
    owner_manifest = json.loads(providers['owner-manifest'])
    owner_review = json.loads(providers['owner-review'])
    assert owner_review['reviewed_manifest']['sha256'] == sha(providers['owner-manifest'])
    assert owner_review['disposition'] == 'approved-as-partial-analyst-owner-successor'
    source_review = json.loads(providers['audit-focused-review'])
    assert source_review['reviewed_manifest']['sha256'] == sha(providers['audit-manifest'])
    assert source_review['disposition'] == 'approved-partial-focused-correction'
    for pin in pins['providers']:
        if pin['path'] in owner_manifest['payloads']:
            assert owner_manifest['payloads'][pin['path']]['sha256'] == pin['sha256']
    audit_manifest = json.loads(providers['audit-manifest'])
    for key in ['audit','correction']:
        pin = next(r for r in pins['providers'] if r['id']==key)
        assert audit_manifest['files'][Path(pin['path']).name]['sha256'] == pin['sha256']
    req,old_req,cases,old_cases = [json.loads(providers[k]) for k in ['requirements','old-requirements','cases','old-cases']]
    assert sum(map(len,req.values())) == 63 and sum(map(len,old_req.values())) == 61
    for device in req:
        assert req[device][:len(old_req[device])] == old_req[device]
    assert len(cases) == 102 and len(old_cases) == 88
    case_by_id = {r['id']:r for r in cases}
    assert len(case_by_id) == 102 and all(case_by_id[r['id']]==r for r in old_cases)
    overlay = json.loads(providers['overlay'])['current_version_overlay']['actual_oracles']
    assert {r['id'] for r in overlay} == set(case_by_id) and len(overlay)==102
    assert all(r['expected'] is r['comparison'] is None and r['target']=='U' and not r['executed'] for r in overlay)
    clause_by_id = {r['id']:r for rows in req.values() for r in rows}
    for r in ledger['requirements']:
        body = clause_by_id[r['id']]['body']
        assert sha(body.encode()) == r['body_sha256']
        assert providers['owner-'+r['device']].decode().splitlines()[r['body_line']-1] == body
        assert r['case_ids'] == [c['id'] for c in cases if c['requirement']==r['id']]
        assert r['fresh_full_body_reviewed'] and r['complete_clause_limits_preserved']
    for r in ledger['predicates']:
        src=r['source'];body=clause_by_id[r['requirement']]['body'];a,z=src['text_chars']
        assert body[a:z] == src['anchor'] and sha(body.encode()) == src['body_sha256']
    for r in ledger['case_navigation']:
        case=cases[int(r['pointer'][1:])]
        assert case['id']==r['id'] and sha(canonical(case))==r['object_sha256']
        assert {k:sha(json.dumps(case[k],sort_keys=True,ensure_ascii=False).encode()) for k in r['action_field_sha256']} == r['action_field_sha256']
        assert set(r['action_field_sha256']) == set(case) & {'setup','action','expected','comparator','documented_predicate','positive_control'}
        assert r['fresh_full_setup_action_expected_and_positive_fields_read'] and r['current_actual'] is r['new_grade'] is None
    clauses=load('clause-index.json')
    assert clauses['clauses']==ledger['requirements'] and clauses['requirements']==63 and clauses['cases']==102
    audit=json.loads(providers['audit']);manual=providers['manual'].decode()
    for loc,block in zip(scope['block_locators'],audit['blocks']):
        assert loc['id']==block['id'] and manual[loc['raw_start']:loc['raw_end']]==block['raw_html']
        assert sha(block['raw_html'].encode())==loc['raw_sha256'] and sha(block['text'].encode())==loc['text_sha256']
    changes=json.loads(providers['correction'])['changes']
    assert len(changes)==18
    for loc,r in zip(scope['correction_fields'],changes):
        assert loc['catalog']==r['catalog'] and loc['pointer']==r['pointer']
        assert loc['before_sha256']==sha(json.dumps(r['before'],sort_keys=True).encode())
        assert loc['after_sha256']==sha(json.dumps(r['after'],sort_keys=True).encode())
    component=json.loads(providers['component']);index_inputs=json.loads(providers['index-authority'])
    authorities={r['path']:r for r in pins['metadata_authority']}
    for auth in authorities.values():
        if auth['authority']=='component':
            parent=next(r for r in component['files'] if r['path']==Path(auth['path']).name)
        else:
            parent=next(r for r in index_inputs['retained_indexes_verified'] if r['path']==auth['path'])
        assert (auth['bytes'],auth['sha256'])==(parent['bytes'],parent['sha256'])
    metadata=[json.loads(z) for z in (HERE/'metadata-rows.jsonl').read_text().splitlines()]
    calls=[json.loads(z) for z in (HERE/'call-rows.jsonl').read_text().splitlines()]
    assert collections.Counter(r['kind'] for r in metadata)==census['selected_counts'] and len(metadata)==431 and len(calls)==149
    metadata_guards(metadata,calls)
    raw_records={}
    for wrapper in metadata+calls:
        loc=wrapper['locator'];assert loc['path'] in authorities
        obj=read_selected_row(wrapper);raw_records[wrapper['id']]=obj
        if wrapper['kind']!='table-prefix':
            assert obj==wrapper['record']
        else:
            rec=wrapper['record'];enc=rec['literal_type_encoding']
            assert not rec['complete_class_or_function_established'] and not rec['actual_public_instance_established']
            assert rec['native_table_extent'] is None
            expected=obj['slots'][:3] if enc in census['selected_model_encodings'] else obj['slots']
            assert rec['slots']==expected and rec['available_exported_prefix_slots']==len(obj['slots'])
            assert {k:v for k,v in obj.items() if k!='slots'} == {k:v for k,v in rec.items() if k not in {'slots','available_exported_prefix_slots','selection','complete_class_or_function_established','actual_public_instance_established'}}
    tables=[r for r in metadata if r['kind']=='table-prefix'];stores=[r for r in metadata if r['kind']=='store-candidate']
    assert sum(len(r['record']['slots']) for r in tables)==93
    assert sum(r['record']['available_exported_prefix_slots'] for r in tables)==512
    assert {r['record']['literal_type_encoding'] for r in tables}==set(census['selected_model_encodings']+census['selected_small_encodings'])
    points={r['record']['address_point'] for r in tables}
    assert all(r['record']['address_point'] in points for r in stores)
    frontier={s['target'] for r in tables for s in r['record']['slots']}|{r['record']['entry'] for r in stores}
    assert sorted(frontier)==census['slot_store_frontier_entries']
    pattern=re.compile(r'(?:^|[^A-Za-z0-9_])(?:'+'|'.join(map(re.escape,census['selected_class_spellings']))+r')::')
    seeds=set()
    for r in metadata:
        obj=r['record']
        if r['kind']=='alias':
            named=any(pattern.search(n) for n in [obj['name']]+[s['name'] for s in obj['symbols']])
            assert named or obj['entry'] in frontier
            if named:seeds.add(obj['entry'])
    assert sorted(seeds)==census['boundary_seeds']
    assert all(r['record']['entry'] in seeds for r in metadata if r['kind']=='membership')
    assert collections.Counter(r['kind'] for r in calls)=={'call':92,'indirect':57}
    for r in calls:
        key='caller' if r['kind']=='call' else 'function'
        assert r['record'][key] in seeds
        if r['kind']=='indirect':assert r['record']['resolved_targets']==[]
    for r in fixtures['records']:
        raw=(ROOT/r['path']).read_bytes()
        assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
        if r.get('header_bytes'):
            assert raw[:4]==b'RIFF' and raw[8:12]==b'WAVE' and raw[36:40]==b'data'
            assert sha(raw[:44])==r['header_sha256']
            fmt,ch,rate,byte_rate,align,bits=struct.unpack_from('<HHIIHH',raw,20)
            assert (fmt,ch,rate,bits)==(1,2,48000,16)
            assert struct.unpack_from('<I',raw,40)[0]//align==r['declared_frames']
    edges=load('chain-edges.json');prospective=load('prospective-frontiers.json')
    assert len(edges['edges'])==12 and all(r['public_route']=='unknown' and r['new_native_site_credit']==0 for r in edges['edges'])
    assert all(set(r['chain_edges']) <= {e['id'] for e in edges['edges']} for r in ledger['contexts'])
    assert edges['application_routes_established']==edges['new_native_site_credit']==0 and edges['selected_successor'] is None
    assert prospective['candidate_count']==len(prospective['candidates'])==16
    assert all(not r['public_route_established'] and not r['legal_input_state_ABI_established'] and not r['body_or_original_batch_selected'] for r in prospective['candidates'])
    assert prospective['selected_successor'] is prospective['selected_original_batch'] is None
    change=pins['research_change'];assert change
    research=(ROOT/change['path']).read_bytes();prefix=research[:change['updated_prefix_bytes']]
    append=research[change['updated_prefix_bytes']:change['updated_prefix_bytes']+change['append_bytes']]
    assert sha(prefix)==change['updated_prefix_sha256'] and sha(append)==change['append_sha256'] and len(append)==change['append_bytes']
    original=prefix.replace(b'updated: 2026-10-20\n',b'updated: 2026-10-19\n',1)
    assert len(original)==change['original_prefix_bytes'] and sha(original)==change['original_prefix_sha256']
    assert research.count(b'## 2026-10-20: sample-instrument route map v1 (pending review)')==1
    for file in HERE.iterdir():
        if file.suffix in {'.md','.py','.json','.jsonl'}:
            text=file.read_text();assert all(line==line.rstrip() for line in text.splitlines()),file.name
            if file.suffix=='.md':
                for target in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',text):
                    if not re.match(r'[a-z]+:',target):assert (file.parent/target).exists(),target
    if (HERE/'manifest.json').exists():
        manifest=load('manifest.json')
        for r in manifest['files']:
            raw=(HERE/r['path']).read_bytes();assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
    negatives=[]
    def reject(label,mutate):
        ll,cc,ss,ff=copy.deepcopy((ledger,census,scope,fixtures));mutate(ll,cc,ss,ff)
        try:guards(ll,cc,ss,ff)
        except AssertionError:negatives.append(dict(id=label,result='rejected'));return
        raise AssertionError('false promotion accepted: '+label)
    reject('omit-required-predicate',lambda l,c,s,f:l['predicates'].pop())
    reject('pad-numeric-instance',lambda l,c,s,f:l['predicates'].append(copy.deepcopy(l['predicates'][0])))
    reject('D12-promoted-to-target-S',lambda l,c,s,f:l['contexts'][0].update(route='S'))
    reject('fixture-promoted-to-application-outcome',lambda l,c,s,f:f['records'][0].update(counts_as_required_predicate=True))
    for key in ['chooser_display_is_chooser_invocation','WarpAs_setup_is_button_action','unlooped_End_applies_to_enabled_loops','Volume_End_control_invented','Volume_LFO_positive_proves_Filter_route','Sampler_main_Filter_positive_proves_all_modulation','Spread_latch_transferred_to_Sampler','Impulse_per_sample_latch_applies_to_globals','Impulse_Gate_is_Simpler_FadeOut','middle_six_Impulse_notes_invented','retained_4sec_fixture_extended','excluded_native_type_removes_required_context']:
        reject(key,lambda l,c,s,f,key=key:s['semantic_guards'].update({key:True}))
    reject('metadata-cap-widened',lambda l,c,s,f:c.update(selected_slots=513))
    reject('public-route-from-class-name',lambda l,c,s,f:c.update(actual_application_route=True))
    for label,kind in [('complete-class-from-exported-prefix','class'),('guessed-indirect-target','indirect'),('changed-selected-source-digest','source')]:
        mm,cc=copy.deepcopy((metadata,calls))
        if kind=='class':
            next(r for r in mm if r['kind']=='table-prefix')['record']['complete_class_or_function_established']=True
        elif kind=='indirect':
            next(r for r in cc if r['kind']=='indirect')['record']['resolved_targets']=['synthetic-guessed-target']
        else:
            mm[0]['locator']['raw_sha256']='0'*64
        try:
            if kind=='source':read_selected_row(mm[0])
            else:metadata_guards(mm,cc)
        except AssertionError:negatives.append(dict(id=label,result='rejected'))
        else:raise AssertionError('false metadata promotion accepted: '+label)
    print(json.dumps(dict(status='PASS',scope='Read-only author structural/provenance check; no semantic grade, source body or original execution.',providers_checked=31,full_clause_pointers=63,full_case_action_pointers=102,application_predicates=350,application_routes_established=0,documentary_annotations=221,context_records=571,auxiliary_fixture_S=5,inherited_source_blocks_located=309,correction_field_pins=18,metadata_selected_rows=431,call_indirect_rows=149,negative_controls=negatives,prefreeze_check_history='Initial check rejected a case-object hash serialization mismatch in this checker (ASCII escaping); aligned with the already-recorded canonical JSON serialization, then all checks passed. No source/case bytes changed.',research_prefix_restoration='exact except dated metadata change',new_native_site_credit=0,selected_successor=None),indent=2))


if __name__=='__main__':
    main()
