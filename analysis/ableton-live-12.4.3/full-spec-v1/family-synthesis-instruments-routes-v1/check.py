#!/usr/bin/env python3
"""Read-only stdlib packet check. No old scripts, corpus indexes or code bodies."""
from pathlib import Path
import json, hashlib, collections, copy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
OWNER=BASE/'synthesis-instruments'
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_text())
def objhash(obj):return sha(json.dumps(obj,sort_keys=True,separators=(',',':')).encode())
EXPECTED={'class-table-header':32,'class-slot':124,'literal-store-candidate':50,
          'alias':153,'alias-membership':22,'outgoing-call':246,'indirect':37}
def validate(d):
    reqs=d['reqs'];cases=d['cases'];spec=d['spec'];ci=d['clauses'];ledger=d['ledger']
    meta=d['metadata'];approval=d['approval'];components=d['components']['components'];front=d['frontiers']
    assert len(reqs)==len({r['id'] for r in reqs})==110
    assert len(cases)==len({c['id'] for c in cases})==190
    assert all(c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
    assert all(r['target_applicability']=='U' for r in reqs)
    assert len(ci['requirements'])==110 and len(ci['cases'])==190 and ci['case_rows_are_not_outcome_denominator'] is True
    lines=spec.splitlines(keepends=True);case_ids={c['id'] for c in cases}
    for i,(r,x) in enumerate(zip(reqs,ci['requirements'])):
        assert x['id']==r['id'] and x['device']==r['device'] and x['contract_pointer']=='/'+str(i)+'/contract'
        assert x['contract_characters']==len(r['contract']) and x['contract_sha256']==sha(r['contract'].encode())
        a,b=x['owner_lines'];assert 1<=a<=b<=len(lines) and sha(''.join(lines[a-1:b]).encode())==x['owner_span_sha256']
        if not r['id'].endswith('LIFECYCLE'):assert r['contract'] in ''.join(lines[a-1:b])
        assert x['source_blocks']==r['source_blocks'] and x['target_applicability']=='U'
        assert x['cases']==[dict(id=c['id'],pointer='/'+str(j)) for j,c in enumerate(cases) if r['id'] in c['requirements']]
    for i,(c,x) in enumerate(zip(cases,ci['cases'])):
        assert x['id']==c['id'] and x['pointer']=='/'+str(i) and x['object_sha256']==objhash(c)
        assert x['requirements']==c['requirements'] and x['source_blocks']==c['source_blocks']
        assert x['actual_expected'] is x['actual_comparison'] is None and x['target_grade']=='U' and not x['executed']
        for key,span in x['field_spans'].items():
            assert span['characters']==len(c[key]) and span['sha256']==sha(c[key].encode()) and span['pointer']=='/'+str(i)+'/'+key
    assert collections.Counter(x['kind'] for x in meta)==EXPECTED
    assert [x['id'] for x in meta]==['SM%04d'%i for i in range(1,665)]
    points={x['address_point']:x for x in approval['class_points']};seeds=set(approval['exact_call_seed_entries'])
    assert len(points)==32 and len(seeds)==115
    aliases={x['record']['entry']:x for x in meta if x['kind']=='alias'}
    assert len(aliases)==153
    tables=[x for x in meta if x['kind']=='class-table-header'];slots=[x for x in meta if x['kind']=='class-slot']
    assert {x['record']['address_point'] for x in tables}==set(points)
    assert len(components)==32 and len({x['address_point'] for x in components})==32
    small=large=variants=0;slot_entries=set();store_entries=set()
    for header in tables:
        h=header['record'];ap=h['address_point'];ss=[x for x in slots if x['record']['address_point']==ap]
        assert h['literal_type_encoding']==points[ap]['type'] and h['offset_to_top']==0
        assert len(ss)==h['selected_slot_count']==points[ap]['selected_slots']
        assert [x['record']['slot_index'] for x in ss]==list(range(len(ss)))
        assert [x['record']['offset'] for x in ss]==[i*8 for i in range(len(ss))]
        assert all(x['provider']['pointer']=='/slots/'+str(i) for i,x in enumerate(ss))
        if h['exported_prefix_slot_count']>8:
            assert len(ss)==3 and h['selection_scope']=='leading three construction/lifetime prefix only';large+=1
        else:
            assert len(ss)==h['exported_prefix_slot_count'] and h['selection_scope']=='whole small exported prefix';small+=1
        if h['literal_type_encoding'].startswith('N7ableton7devices9wavetable25WavetableUnisonOscillatorI'):
            assert len(ss)==6;variants+=1
        slot_entries.update(x['record']['target'] for x in ss)
    assert (large,small,variants)==(14,18,8)
    for x in components:
        assert x['actual_instance'] is False and x['receiver_ABI']=='unknown'
        assert x['native_extent'] is x['C_body_locator'] is None and x['complete_callable_leaf'] is False and x['public_route_credit']==0
        assert x['address_point'] in points
    for x in meta:
        loc=x['provider'];assert loc['line']>0 and loc['byte']>=0 and loc['bytes']>0 and len(loc['sha256'])==64
        assert '/decomp/' not in loc['path'] and not loc['path'].endswith('.bin')
        if x['kind']=='literal-store-candidate':
            rec=x['record'];assert rec['address_point'] in points and rec['code_line']>0 and rec['quote'] and rec['status'].startswith('literal decompiled store candidate')
            store_entries.add(rec['entry'])
        if x['kind']=='outgoing-call':assert x['record']['caller'] in seeds
        if x['kind']=='indirect':assert x['record']['function'] in seeds and x['record']['resolved_targets']==[]
        if x['kind']=='alias-membership':assert x['record']['entry'] in aliases and x['record']['kind']=='alias_membership'
    named={x['entry'] for x in d['census']['named_frontier_rule']['entries']}
    assert len(named)==12 and seeds==slot_entries|named
    assert set(aliases)==slot_entries|named|store_entries and len(set(aliases)-seeds)==38
    assert set(front['store_only_unfollowed'])==store_entries-seeds
    assert front['complete_callable_X_leaves']==front['complete_callable_math_leaves']==front['execution_inputs_or_metrics_adopted']==0 and front['successor_selected'] is False
    assert {x['entry'] for x in front['approved_one_hop_entries']}==seeds
    for x in front['approved_one_hop_entries']:
        assert x['C_locator'] is x['native_extent'] is x['legal_inputs'] is x['expected_result'] is None
        assert x['whole_callable_leaf'] is x['public_route'] is False and len(x['missing'])==4
    kinds=collections.Counter(x['record']['kind'] for x in meta if x['kind']=='indirect');assert kinds==dict(call=26,jump=11)
    edges=d['chain']['edges'];assert len(edges)==14 and [x['id'] for x in edges]==['SY%02d'%i for i in range(1,15)]
    assert {x['id'] for x in edges if x['status']=='observed-static'}=={'SY05','SY07','SY09'}
    assert all(x['status']=='unknown' for x in edges if x['id'] not in ['SY05','SY07','SY09'])
    assert d['chain']['new_resolved_sites']==0 and d['chain']['inherited_indirect_inventory']==dict(exported_reference_sites=25071,conditional_additions=24,combined=25095,all_sites=268015)
    assert d['chain']['all_public_required_bindings']=='unknown'
    outcomes=ledger['outcomes'];assert len(outcomes)==ledger['required_predicates']==585
    assert [x['id'] for x in outcomes]==['SI%04d'%i for i in range(1,586)]
    assert {x['requirement'] for x in outcomes}=={x['id'] for x in reqs}
    assert ledger['route_counts']=={'X-route':0,'S-route':0,'no-established-route':585}
    assert ledger['documentary_D12_annotations']==390 and ledger['source_annotations']=={'D12':390,'U':195}
    assert ledger['source_semantics_inherited'] is True and ledger['auxiliary_helpers_are_not_required_outcomes'] is True
    assert ledger['all_actual_U'] is True and ledger['requirements']==110 and ledger['cases']==190
    assert ledger['required_unsupported']=='U' and ledger['coverage_gate']=='OPEN' and ledger['documentary_complete_fallback'] is False
    assert ledger['new_grade_site_norm_case_release']==0 and ledger['successor_selected'] is False and len(ledger['unresolved_enumeration'])==3
    definitions=d['units'].splitlines();life=d['life']['units'];seen=collections.Counter();life_seen=collections.Counter()
    for x in outcomes:
        rid=x['requirement'];i=next(i for i,r in enumerate(reqs) if r['id']==rid);r=reqs[i];source=x['source']
        assert x['clause_pointer']=='/requirements/'+str(i) and source['pointer']=='/'+str(i)+'/contract'
        assert source['body_sha256']==sha(r['contract'].encode()) and source['owner_lines']==ci['requirements'][i]['owner_lines']
        assert x['route']=='no-established-route' and x['route_is_inventory_not_grade'] is True
        assert x['target_grade']=='U' and x['source_annotation']==r['provenance']
        assert x['actual_expected'] is x['actual_comparison'] is None and not x['executed'] and x['grade_change']==0
        assert x['missing_join'] and len(x['missing_join_ids'])>=6 and x['case_links_are_navigation_only'] is True
        assert all(z in case_ids for z in x['existing_cases'])
        assert len(x['premises'])==5 and 'UI-only' in x['premises'][1] and 'BOTH' in x['premises'][2] and 'NONEMPTY' in x['premises'][2] and 'NONZERO' in x['premises'][2]
        assert x['enumerable_inputs']['native_function'] is x['enumerable_inputs']['legal_call_inputs'] is None and x['enumerable_inputs']['execution_ready'] is False
        if x['lifecycle_context'] is None:
            n=source['unit_source_line'];suffix,rest=definitions[n-1].split('|',1);anchor,predicate=rest.split(' :: ',1)
            assert rid=='REQ-SYN-'+suffix and x['observable']==predicate
            a=source['contract_anchor'];assert r['contract'][a['start']:a['end']]==anchor and sha(anchor.encode())==a['sha256']
            seen[n]+=1
            assert x['existing_cases']==[z['id'] for z in ci['requirements'][i]['cases']]
        else:
            assert rid.endswith('LIFECYCLE') and x['observable'] in life[x['lifecycle_context']]
            case=x['case_context'];j=int(case['pointer'][1:]);c=cases[j]
            assert c['id']==case['id'] and rid in c['requirements'] and case['unknown_sha256']==sha(c['unknown'].encode()) and x['existing_cases']==[c['id']]
            life_seen[(rid,x['lifecycle_context'],x['observable'])]+=1
        if rid=='REQ-SYN-ME-003':assert 'only semitone indicator st->sd' in x['current_qualification']
        if rid in ['REQ-SYN-OP-011','REQ-SYN-OP-012']:assert 'unresolved' in x['restart_qualification'] and 'no selected law' in x['restart_qualification']
    assert set(seen)=={i for i,s in enumerate(definitions,1) if s and not s.startswith('#')} and set(seen.values())=={1}
    assert len(life_seen)==195 and set(life_seen.values())=={1}
    geometry=d['geometry'];blocks=d['audit']['blocks'];manual=d['manual']
    assert len(geometry['blocks'])==len(blocks)==567 and geometry['source_texts_semantically_reaudited']==0
    assert geometry['case_reference_occurrences']==354 and geometry['case_unique_source_pointers']==343
    for i,(g,b) in enumerate(zip(geometry['blocks'],blocks)):
        a,z=g['raw_character_start'],g['raw_character_end'];assert g['audit_pointer']=='/blocks/'+str(i)
        assert g['global_source_id']==b['id'] and manual[a:z]==b['raw_html']
        assert sha(b['text'].encode())==g['text_sha256'] and sha(b['raw_html'].encode())==g['raw_html_sha256']
        assert g['html_line']==manual.count('\n',0,a)+1 and g['html_column']==a-(manual.rfind('\n',0,a)+1)
    overlay=d['fixtures']['current_version_overlay']
    assert [x['id'] for x in overlay['actual_oracles']]==[x['id'] for x in cases]
    assert all(x['expected'] is x['comparison'] is None and x['target']=='U' and x['executed'] is False for x in overlay['actual_oracles'])
    assert 'Only the semitone indicator st->sd' in overlay['unit_qualification']['current_scoped_predicate']

def main():
    assert sha((HERE/'scope-approval-root.json').read_bytes())=='ca9060260a68e7f279a583aa0948058772fcd908f4a1af996e77882139893666'
    assert sha((HERE/'metadata-scope-census.json').read_bytes())=='337dca125b2672cf8c5b9d53ff03bcb9862b2dda54f9bd644179a18e2ada5ad3'
    assert sha((HERE/'retained-metadata.jsonl').read_bytes())=='5472b3879210ffe72431f08bd12a40b9e1fb06205484c9009decf99cfd710c09'
    checked=[];asof=[]
    for pin in read(HERE/'pins.json')['pins']:
        path=ROOT/pin['path'];data=path.read_bytes();matched=len(data)==pin['bytes'] and sha(data)==pin['sha256']
        if 'as-of' in pin['role']:asof.append(dict(path=pin['path'],matches_asof=matched,future_gate=False))
        else:assert matched,pin['path'];checked.append(pin['path'])
    geometry=read(HERE/'source-geometry.json');manual=(ROOT/geometry['source']['path']).read_bytes()
    assert len(manual)==geometry['source']['bytes'] and sha(manual)==geometry['source']['sha256']
    d=dict(reqs=read(OWNER/'requirements-r3.json'),cases=read(OWNER/'cases-r3.json'),spec=(OWNER/'spec-r3.md').read_text(),
           fixtures=read(OWNER/'fixtures-r3.json'),clauses=read(HERE/'clause-index.json'),ledger=read(HERE/'route-ledger.json'),
           metadata=[json.loads(x) for x in (HERE/'retained-metadata.jsonl').read_text().splitlines()],
           approval=read(HERE/'scope-approval-root.json'),census=read(HERE/'metadata-scope-census.json'),
           components=read(HERE/'components.json'),frontiers=read(HERE/'prospective-frontiers.json'),chain=read(HERE/'chain-edges.json'),
           units=(HERE/'predicate-units.txt').read_text(),life=read(HERE/'lifecycle-predicate-units.json'),
           geometry=geometry,audit=read(BASE/'synthesis-instruments-source-audit/audit.json'),manual=manual.decode('utf-8'))
    validate(d)
    mutations=[
      ('drop-required-predicate',lambda z:z['ledger']['outcomes'].pop()),
      ('pad-outcome-with-helper',lambda z:z['ledger']['outcomes'].append(copy.deepcopy(z['ledger']['outcomes'][0]))),
      ('wrong-owner-body',lambda z:z['reqs'][0].update(contract='invented')),
      ('wrong-owner-span',lambda z:z['clauses']['requirements'][0].update(owner_lines=[1,1])),
      ('change-case-action',lambda z:z['cases'][0].update(setup_and_action='inspect only')),
      ('invent-target-expected',lambda z:z['cases'][0].update(expected=0)),
      ('promote-D12-to-S',lambda z:z['ledger']['outcomes'][0].update(route='S-route')),
      ('promote-symbol-to-X',lambda z:z['ledger']['outcomes'][0].update(route='X-route')),
      ('invent-actual-class',lambda z:z['components']['components'][0].update(actual_instance=True)),
      ('invent-native-body-extent',lambda z:z['components']['components'][0].update(native_extent=4)),
      ('drop-typed-specialization',lambda z:z['components']['components'].pop()),
      ('add-unselected-slot',lambda z:next(x for x in z['metadata'] if x['kind']=='class-table-header' and x['record']['exported_prefix_slot_count']>8)['record'].update(selected_slot_count=4)),
      ('follow-store-only',lambda z:next(x for x in z['metadata'] if x['kind']=='outgoing-call')['record'].update(caller=z['frontiers']['store_only_unfollowed'][0])),
      ('invent-indirect-target',lambda z:next(x for x in z['metadata'] if x['kind']=='indirect')['record']['resolved_targets'].append({'to':'0x1'})),
      ('close-control-clock',lambda z:z['chain']['edges'][2].update(status='observed-static')),
      ('invent-resolved-site',lambda z:z['chain'].update(new_resolved_sites=1)),
      ('invent-C-body-frontier',lambda z:z['frontiers']['approved_one_hop_entries'][0].update(C_locator='new-body')),
      ('invent-legal-call-input',lambda z:z['ledger']['outcomes'][0]['enumerable_inputs'].update(legal_call_inputs=[0])),
      ('invent-complete-math-leaf',lambda z:z['frontiers'].update(complete_callable_math_leaves=1)),
      ('erase-productive-premise',lambda z:z['ledger']['outcomes'][0]['premises'].__setitem__(2,'enabled flag')),
      ('erase-Meld-unit-qualification',lambda z:next(x for x in z['ledger']['outcomes'] if x['requirement']=='REQ-SYN-ME-003').update(current_qualification='all pitch controls degrees')),
      ('choose-Operator-restart-law',lambda z:next(x for x in z['ledger']['outcomes'] if x['requirement']=='REQ-SYN-OP-012').update(restart_qualification='always current-to-peak')),
      ('wrong-manual-span',lambda z:z['geometry']['blocks'][0].update(raw_character_start=0)),
      ('claim-full-source-reaudit',lambda z:z['geometry'].update(source_texts_semantically_reaudited=567)),
      ('close-U-coverage',lambda z:z['ledger'].update(coverage_gate='CLOSED')),
      ('documentary-fallback',lambda z:z['ledger'].update(documentary_complete_fallback=True)),
      ('select-successor',lambda z:z['frontiers'].update(successor_selected=True))]
    negatives=[]
    for name,mutate in mutations:
        z=copy.deepcopy(d);mutate(z)
        try:validate(z)
        except (AssertionError,ValueError,KeyError,IndexError,TypeError):negatives.append(dict(name=name,rejected=True))
        else:raise AssertionError('negative accepted: '+name)
    print(json.dumps(dict(status='PASS',checker_sha256=sha(Path(__file__).read_bytes()),immutable_selected_pins=len(checked),asof_context=asof,
                          metadata_rows=664,requirements=110,cases=190,required_predicates=585,D12_annotations=390,U_lifecycle_predicates=195,
                          route_counts={'X-route':0,'S-route':0,'no-established-route':585},source_geometry_blocks=567,current_case_quote_occurrences=354,
                          negative_controls=negatives,negative_count=len(negatives),
                          original_index_chunk_native_image_provider_decoder_harness_model_comparator_runs=0,
                          shared_or_canonical_writes=0,required_unsupported='U',coverage_gate='OPEN',successor_selected=False,
                          limits='Mechanical retained-data integrity/negative controls only. No semantic oracle, full-source re-audit, original execution, grade or closure. Mutable canonical/selector identities are as-of provenance, not future gates.'),indent=2))
if __name__=='__main__':main()
