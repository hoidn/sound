"""Read-only selected-DATA integrity and scope checks; no query/old modules/imports."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

P=Path(__file__).resolve().parent
R=P.parents[3]
F=P.parent

def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path):return json.loads(path.read_bytes())
def canon(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())

def guards(ledger,census,sem,curves,nav):
    assert len(ledger['bundles'])==ledger['bundle_count']==67
    assert len({x['id'] for x in ledger['bundles']})==67
    assert ledger['counts']==dict(whole_clause_bundles=67,file_only_S=9,application_none=58,D12_annotations=47,total_context_records=114,X=0)
    assert len(ledger['contexts'])==114 and ledger['counts_are_inventory_not_grades']
    assert ledger['new_native_sites']==ledger['new_original_calls']==ledger['new_grades']==0 and ledger['selected_successor'] is None
    bundles={x['id']:x for x in ledger['bundles']};contexts=collections.defaultdict(list)
    for x in ledger['contexts']:
        b=bundles[x['bundle']];assert b['requirement']==x['requirement']
        assert x['actual'] is x['comparison'] is x['new_grade'] is x['native_PC'] is None
        contexts[b['id']].append(x['context'])
        assert x['route']==('S-retained-file-only' if x['context']=='retained-file' else 'no-established-exact-target-route' if x['context']=='documentary' else 'no-established-route')
    for b in bundles.values():
        assert b['whole_contract_qualifiers_mandatory']
        assert b['route']==('S-retained-file-only' if b['provenance']=='Dpkg' else 'no-established-route')
        assert contexts[b['id']]==(['retained-file'] if b['provenance']=='Dpkg' else ['documentary','target-application'] if b['provenance']=='D12' else ['target-application'])
    assert census['counts']==dict(tables=29,selected_slots=105,available_prefix_slots=789,stores=35,aliases=136,memberships=41,combined_alias_memberships=177,named_alias_entries=607,boundary_seeds=41,call_rows=62,indirect_rows=22,call_indirect=84)
    assert census['within_caps'] and all(census['counts'][k]<=v for k,v in census['caps'].items())
    assert census['caps']==dict(tables=32,selected_slots=512,stores=128,combined_alias_memberships=512,call_indirect=512)
    assert census['broad_exact_owner_alias_census']==dict(aliases=702,memberships=607,combined=1309,retained=False)
    assert len(census['selected_visualization_updates'])==9 and len(census['boundary_seeds'])==41
    assert census['unselected_named_alias_entries']==566 and census['selected_successor'] is None
    truekeys=['EACH_NONEMPTY_NONZERO_control_sensitive_positive','BOTH_relevant_channels_stages_modulators_targets_productive','Erosion_enabled_Width_before_modifier','Erosion_S1_first_second_only','Roar_filter_AND_shaper_positive','Roar037_explicit_gainstage_Frequency_action','Roar_BOTH_manual_Feedback_controls_positive_before_MIDI','Roar_MIDI_both_Feedback_controls_inactive_D12_preserved','Listen_replacement_not_normal_mix','gate_tail_requires_sustaining_feedback','Waveshaper_Drive_distinct_from_main_Drive','zero_envelope_only_follower_gate']
    falsekeys=['UI_only_requires_audio','S0_proves_generator_or_tail_absence','settings_or_flags_prove_active_path','preset_is_constructor_default','file_schema_proves_live_admission','modern_legacy_algorithms_merged','Roar007_030_imply_actual_gainstage_Frequency_edit','Roar_analysis_feedback_Frequency_satisfy_gainstage','Saturator_wet_clip_bound_applies_arbitrary_dry_mix','optional_recipes_guaranteed_sound','graph_visualization_proves_audio_DSP','new_body_or_original_selection']
    assert all(sem[k] is True for k in truekeys) and all(sem[k] is False for k in falsekeys)
    assert len(curves['candidates'])==7 and curves['candidate_original_batch'] is curves['selected_successor'] is None
    for x in curves['candidates']:assert not x['body_math_or_DSP_proof'] and not x['callable_input_state_ABI'] and not x['selected_for_body_or_execution'] and x['graph_to_audio_join']=='unknown'
    assert len(nav['records'])==200 and nav['old_exact']==190 and nav['new_null']==10 and nav['artifact_roles']==18 and nav['application_roles']==182 and nav['all_actual_U']
    assert all(x['actual_expected'] is x['actual_comparison'] is None and x['target']=='U' and not x['executed'] for x in nav['records'])

def main():
    if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no metadata query, old helpers or native execution.')
    ledger,census,sem,curves,nav=[load(P/n) for n in ['route-ledger.json','query-census.json','semantic-guards.json','curve-frontiers.json','case-navigation.json']]
    guards(ledger,census,sem,curves,nav)
    pins=load(P/'pins.json')
    for pin in pins['providers']:
        raw=(R/pin['path']).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],pin['path']
    frozen=load(F/'distortion/manifest-author-r3.json')['files']
    for name in ['requirements.json','cases-r3.json','cases.json','actual-overlay-r3.json','adoption-r3.json','fixture-signals.json','schema-fields.json','package-values.json','spec-r3.md']:
        raw=(F/'distortion'/name).read_bytes();assert len(raw)==frozen[name]['bytes'] and sha(raw)==frozen[name]['sha256']
    q=load(F/'distortion/requirements.json');cases=load(F/'distortion/cases-r3.json');old=load(F/'distortion/cases.json');owner=(F/'distortion/spec-r3.md').read_text();clause=load(P/'clause-index.json')
    assert cases[:190]==old and len(q)==67 and len(cases)==200
    assert clause['owner_sha256']==sha(owner.encode()) and len(clause['requirements'])==67
    overlay=load(F/'distortion/actual-overlay-r3.json')['cases']
    for i,(r,b,c) in enumerate(zip(q,ledger['bundles'],clause['requirements'])):
        s=b['source'];assert r['id']==b['requirement']==c['id'] and s==c['source']
        assert s['requirement_pointer']==f'/{i}/contract' and owner[s['char_start']:s['char_end']]==r['contract'] and sha(r['contract'].encode())==s['contract_sha256']
        assert b['provenance']==r['provenance'] and b['device']==r['device']
        expected=[x['id'] for x in cases if r['id'] in list(dict.fromkeys([x['requirement'],*x.get('requirements',[])]))]
        assert b['case_navigation']==c['case_navigation']==expected and expected
    for i,(n,c,o) in enumerate(zip(nav['records'],cases,overlay)):
        assert c['id']==n['id']==o['id'] and n['pointer']==f'/{i}' and canon(c)==n['object_sha256'] and canon(c['input'])==n['input_sha256']
        assert n['requirements']==list(dict.fromkeys([c['requirement'],*c.get('requirements',[])]))
        assert o['actual_expected'] is o['actual_comparison'] is None and o['target']=='U' and not o['executed']
        if i>=190:assert c['expected'] is c['comparison'] is c['documentary_expected'] is c['documentary_comparison'] is None
    scope=load(P/'source-scope.json');audit=load(F/'distortion-source-audit/audit.json');html=(R/scope['manual_path']).read_text()
    assert len(scope['blocks'])==len(audit['blocks'])==216 and sha(html.encode())==scope['source_sha256']=='9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299' and len(html.encode())==588328
    assert not scope['corrected_Roar007_030_are_Frequency_gestures'] and scope['R3_Roar037_explicit_Frequency_gesture_proposal'] and not scope['pixels_destinations_inspected']
    for loc,b in zip(scope['blocks'],audit['blocks']):
        assert loc['id']==b['id'] and html[loc['raw_start']:loc['raw_end']]==b['raw_html'] and sha(b['text'].encode())==loc['text_sha256'] and sha(b['raw_html'].encode())==loc['raw_sha256']
    response=load(F/'distortion-source-audit/response-r2.json');assert len(response['changes'])==4 and response['actual_expected'] is response['actual_comparison'] is None and not response['executed']
    schema=load(F/'distortion/schema-fields.json');pkg=load(F/'distortion/package-values.json');assert len(scope['package_facts'])==9
    for fact in scope['package_facts']:
        s=schema[int(fact['schema_pointer'][1:])];p=pkg[int(fact['package_pointer'][1:])]
        assert s['class']==p['class']==fact['class_name'] and s['line']==fact['schema_line'] and p['locator']==fact['package_root'] and p['root_attributes']['Creator']==fact['Creator']=='Ableton Live 12.4d1' and p['root_attributes']['MinorVersion']==fact['MinorVersion']=='12.0_12402'
        assert not fact['runtime_admission_default_or_DSP']
    md=[json.loads(x) for x in (P/'metadata-rows.jsonl').read_text().splitlines()]
    assert collections.Counter(x['kind'] for x in md)=={'table-prefix':29,'store-candidate':35,'alias':136,'membership':41,'call':62,'indirect':22}
    authority={x['path']:x for x in pins['metadata_authority']};models={str(len(x))+x for x in census['models']};points=set();slots=0;aliases=set();seeds=set(census['boundary_seeds'])
    component={x['path']:x for x in load(F/'component-resolution-v1/manifest.json')['files']}
    index={x['path']:x for x in load(F/'component-resolution-v1/packet-inputs.json')['retained_indexes_verified']}
    for path,a in authority.items():
        old=index[path] if path in index else component[Path(path).name]
        assert a['bytes']==old['bytes'] and a['sha256']==old['sha256']
    for row in md:
        loc=row['locator'];assert loc['path'] in authority
        with Path(loc['path']).open('rb') as stream:stream.seek(loc['byte_start']);raw=stream.read(loc['bytes'])
        assert len(raw)==loc['bytes'] and sha(raw)==loc['raw_sha256'];original=json.loads(raw);rec=row['record']
        if row['kind']=='table-prefix':
            for k,v in original.items():assert rec[k]==(v[:3] if k=='slots' and original['literal_type_encoding'] in models else v)
            assert rec['offset_to_top']==0 and rec['native_table_extent'] is None and not rec['complete_class_or_processing_interface_established'] and not rec['actual_public_instance_established']
            points.add(rec['address_point']);slots+=len(rec['slots'])
        else:assert rec==original
        if row['kind']=='alias':aliases.add(rec['entry'])
        if row['kind']=='call':assert rec['caller'] in seeds
        if row['kind']=='indirect':assert rec['function'] in seeds and rec['resolved_targets']==[]
    assert len(points)==29 and slots==105 and len(aliases)==136 and seeds<=aliases
    assert {x['record']['entry'] for x in md if x['kind']=='membership'}==seeds
    assert all(x['record']['address_point'] in points for x in md if x['kind']=='store-candidate')
    byid={x['id']:x for x in md}
    for c in curves['candidates']:
        table=byid[c['table_metadata_id']]['record'];assert table['literal_type_encoding']==str(len(c['name']))+c['name'] and c['selected_slots']==table['slots']
        assert c['owner_clause_proofs']==[next(x['source'] for x in clause['requirements'] if x['id']==ident) for ident in c['requirements']]
        for a in c['qualified_update_aliases']:assert byid[a['id']]['record']['entry']==a['entry'] and byid[a['id']]['record']['name']==a['name']
    change=load(P/'research-change.json');research=(R/change['path']).read_bytes();prefix=research[:change['prefix_bytes_after_date_update']]
    assert sha(prefix)==change['prefix_sha256_after_date_update'] and sha(prefix.replace(b'updated: 2026-10-20',b'updated: 2026-10-19',1))==change['original_prefix_sha256']
    start,size=change['append_start_byte'],change['append_bytes'];assert sha(research[start:start+size])==change['append_sha256']
    negatives=[]
    def reject(name,mutation):
        l,c,s,f,n=copy.deepcopy((ledger,census,sem,curves,nav));mutation(l,c,s,f,n)
        try:guards(l,c,s,f,n)
        except (AssertionError,KeyError):negatives.append(dict(name=name,rejected=True))
        else:raise AssertionError('Unsafe mutation accepted:'+name)
    mutations=[('omit whole clause',lambda l,c,s,f,n:l['bundles'].pop()),('pad numeric/case outcome',lambda l,c,s,f,n:l['bundles'].append(l['bundles'][0])),('D12 annotation becomes target S',lambda l,c,s,f,n:next(x for x in l['contexts'] if x['context']=='documentary').update(route='S-retained-file-only')),('application clause gets file S',lambda l,c,s,f,n:next(x for x in l['bundles'] if x['provenance']=='D12').update(route='S-retained-file-only')),('actual pass from file metadata',lambda l,c,s,f,n:n['records'][0].update(actual_expected=True)),('arbitrary model slot window',lambda l,c,s,f,n:c['counts'].update(selected_slots=512)),('alias cap widened',lambda l,c,s,f,n:c['caps'].update(combined_alias_memberships=1309)),('metadata gains site credit',lambda l,c,s,f,n:l.update(new_native_sites=1)),('legacy modes merged',lambda l,c,s,f,n:s.update(modern_legacy_algorithms_merged=True)),('S0 proves no generator',lambda l,c,s,f,n:s.update(S0_proves_generator_or_tail_absence=True)),('one path sufficient',lambda l,c,s,f,n:s.update(BOTH_relevant_channels_stages_modulators_targets_productive=False)),('inactive Erosion width edits',lambda l,c,s,f,n:s.update(Erosion_enabled_Width_before_modifier=False)),('wrong Erosion S1 segment',lambda l,c,s,f,n:s.update(Erosion_S1_first_second_only=False)),('filter baseline becomes Frequency gesture',lambda l,c,s,f,n:s.update(Roar007_030_imply_actual_gainstage_Frequency_edit=True)),('different Frequency control substituted',lambda l,c,s,f,n:s.update(Roar_analysis_feedback_Frequency_satisfy_gainstage=True)),('MIDI control gate one baseline',lambda l,c,s,f,n:s.update(Roar_BOTH_manual_Feedback_controls_positive_before_MIDI=False)),('graph becomes DSP proof',lambda l,c,s,f,n:s.update(graph_visualization_proves_audio_DSP=True)),('curve name becomes callable',lambda l,c,s,f,n:f['candidates'][0].update(callable_input_state_ABI=True)),('recipe guarantees sound',lambda l,c,s,f,n:s.update(optional_recipes_guaranteed_sound=True)),('wet clip bound covers dry mix',lambda l,c,s,f,n:s.update(Saturator_wet_clip_bound_applies_arbitrary_dry_mix=True)),('preset proves default',lambda l,c,s,f,n:s.update(preset_is_constructor_default=True))]
    for name,mutation in mutations:reject(name,mutation)
    links=0
    for target in re.findall(r'\]\(([^)]+)\)',(P/'structure.md').read_text()):
        if target.startswith(('http:','https:','#')):continue
        assert (P/target.split('#')[0]).is_file(),target;links+=1
    print(json.dumps(dict(status='PASS-bounded-distortion-family-data-check',requirements=67,bundles_not_atomic=67,cases=200,preserved_old=190,new_null_histories=10,actual_all_U=True,file_only_S=9,application_none=58,D12_annotations=47,context_records=114,X=0,metadata_rows=325,tables=29,selected_slots=105,available_prefix_slots=789,stores=35,aliases=136,memberships=41,seeds=41,calls=62,unresolved_indirect=22,pins=len(pins['providers']),mechanical_source_blocks=216,research_prefix_bytes=change['original_prefix_bytes'],focused_links=links,negative_controls=negatives,new_body_native_original_model_comparator_runs=0,selected_successor=None),indent=2))

if __name__=='__main__':main()
