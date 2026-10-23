"""Own analyst document authoring only; no old module/tool/body imports."""
from pathlib import Path
import collections
import hashlib
import json
import re

P = Path(__file__).resolve().parent
F = P.parent
D = F / 'modulation-pitch-loop'
R = F.parents[2]
J = lambda p: json.loads(Path(p).read_bytes())
H = lambda b: hashlib.sha256(b).hexdigest()
OH = lambda x: H(json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def write(name, data):
    with (P/name).open('xb') as out:
        out.write((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode())


def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=H(raw))


def main():
    if __import__('sys').argv[1:]:
        raise SystemExit('Fixed own document authoring only')
    approval = J(P/'scope-approval-root.json')
    proposal = J(P/'census-proposal.json')
    assert H((P/'scope-approval-root.json').read_bytes()) == 'bbecac079bb0aa6ca570a178f7f8a6d9c92e873fa348b289121352c513d888b9'
    req, cases = J(D/'requirements.json'), J(D/'cases-r3.json')
    overlay, adoption = J(D/'actual-overlay-r4.json')['cases'], J(D/'adoption-r4.json')['groups']
    spec, prefix = (D/'spec-r4.md').read_bytes(), (R/'wiki/research/modulation-pitch-loop-devices.md').read_bytes()
    assert len(req)==106 and len(cases)==208 and cases[:186]==J(D/'cases.json') and len(prefix)==15924
    assert (R/'wiki/specs/modulation-pitch-loop-devices.md').read_bytes()==spec
    for c,o in zip(cases,overlay,strict=True):
        assert cases[int(o['case_pointer'][1:])]['id']==c['id']==o['id']
        assert c['expected'] is None and o['actual_expected'] is None and o['actual_comparison'] is None and o['target']=='U' and not o['executed']
    for a in adoption:
        assert cases[int(a['case_pointer'][1:])]['id']==a['case_id']
    rows = [json.loads(b) for b in (P/'native-data.jsonl').read_bytes().splitlines()]
    assert len(rows)==704
    codes = {r['device']:r['id'].split('-')[2] for r in req}
    devices = {v:k for k,v in codes.items()}
    families = {
        'AP':'AAutoPan2 LAutoPan2 OAutoPan2Processor AAutoPan2Module TAutoPan2LfoCurveHelper',
        'AS':'AAutoShift LAutoShift OAutoShiftProcessor AAutoShiftModule',
        'CE':'AChorus2 LChorus2 OChorus2Processor AChorus2Module TChorus2LfoCurveHelper',
        'PF':'APhaserNew LPhaserNew OPhaserNewProcessor APhaserNewModule',
        'SH':'AShifter LShifter OShifterProcessor AShifterModule',
        'SR':'ATransmute LTransmute OTransmuteProcessor ATransmuteModule',
        'ST':'ASpectralTime LSpectralTime OSpectralTimeProcessor ASpectralModule',
        'VO':'AVocoder OVocoderProcessor AVocoderModule',
        'BR':'ABeatRepeat OBeatRepeatControlProcessor ABeatRepeatUnit',
        'LP':'ALooper OLooperProcessor ALooperModule'}
    def family(name):
        hit=[code for code,names in families.items() if any(re.search(r'(?<![A-Za-z0-9_])'+re.escape(n)+r'(?![A-Za-z0-9_])', name) for n in names.split())]
        assert len(hit)==1,(name,hit)
        return hit[0]
    fields=['table_rows','store_rows','alias_rows','selected_named_seed_rows','excluded_seed_rows','outgoing_call_rows','indirect_rows']
    associations={code:dict(device=name,**{k:[] for k in fields},public_binding='unknown',new_C_bodies=0,new_resolved_site_credit=0) for code,name in devices.items()}
    points,aliases={},{}
    excluded=set(approval['exact_seed_exclusions'])
    for i,row in enumerate(rows,1):
        d=row['record']
        if row['kind']=='table-data':
            code=family(re.fullmatch(r'\d+(.+)',d['literal_type_encoding'])[1])
            associations[code]['table_rows'].append(i)
            points[d['address_point']]=code
        elif row['kind']=='alias-data':
            code=family(d['name'])
            associations[code]['alias_rows'].append(i)
            associations[code]['excluded_seed_rows' if d['entry'] in excluded else 'selected_named_seed_rows'].append(i)
            aliases[d['entry']]=code
    for i,row in enumerate(rows,1):
        d=row['record']
        if row['kind']=='store-data': associations[points[d['address_point']]]['store_rows'].append(i)
        elif row['kind']=='call-data': associations[aliases[d['caller']]]['outgoing_call_rows'].append(i)
        elif row['kind']=='indirect-data': associations[aliases[d.get('function') or d['caller']]]['indirect_rows'].append(i)
    assert sum(len(a['selected_named_seed_rows']) for a in associations.values())==122
    write('processor-associations.json',associations)
    write('named-seeds.json',dict(policy=proposal['proposed_seed_selection'],entries=[dict(entry=r['record']['entry'],name=r['record']['name'],alias_native_data_line=i,selected_outgoing_seed=r['record']['entry'] not in excluded) for i,r in enumerate(rows,1) if r['kind']=='alias-data'],counts=dict(named_frontier=133,selected=122,excluded_UI_group=11),new_body_selection=False))
    def span(start,length):
        b=spec[start:start+length]
        return dict(path=str(D/'spec-r4.md'),byte_start=start,byte_length=length,line_start=spec[:start].count(b'\n')+1,line_end=spec[:start+length].count(b'\n')+1,sha256=H(b))
    lines=spec.splitlines(keepends=True)
    offsets=[]
    offset=0
    for line in lines: offsets.append(offset);offset+=len(line)
    spans,ledger=[],[]
    for i,r in enumerate(req):
        code=r['id'].split('-')[2]
        if r['strength']=='D12':
            b=r['contract'].encode();assert spec.count(b)==1
            source=[span(spec.index(b),len(b))]
        else:
            start=spec.index(('### '+r['id']+' — lifecycle obligations').encode())
            end=spec.index(b'\n\n',spec.index(b'**U.**',start))
            source=[span(start,end-start)]
            k=next(k for k,line in enumerate(lines) if line.startswith(('| '+r['device']+' / '+r['id']+' |').encode()))
            source.append(span(offsets[k],len(lines[k].rstrip(b'\n'))))
        spans.append(dict(requirement=r['id'],catalog_path=str(D/'requirements.json'),catalog_pointer=f'/{i}',record_sha256=OH(r),contract_sha256=H(r['contract'].encode()),source_spans=source,source_role='literal complete D12contract' if r['strength']=='D12' else 'U summary plus device nine-outcome matrix; catalog sentence is derived, not verbatim canonical'))
        ledger.append(dict(id=f'MPLR-{i+1:03d}',requirement=r['id'],device=r['device'],unit='whole complete current clause bundle; not atomic outcome',predicate=r['contract'],source_annotation=r['strength'],exact_target_applicability='U',actual_status='U',route='no-established-route',grade_changed=False,public_binding='unknown',owner_span_pointer=f'owner-spans.json#/{i}',related_cases_navigation_only=[c['id'] for c in cases if r['id'] in c['requirements']],prerequisites=f'prerequisites.json#/devices/{code}',integration_edges=['MPL-E01','MPL-E03','MPL-E05','MPL-E06'],metadata_context=f'processor-associations.json#/{code}',missing_join='Actual reached device/instance/receiver, input/state domain, control dispatch/provider/ABI, processing/output/host and lifecycle result remain unknown. Documentary wording, table/store/alias/call references and retained fields close no portion of this complete clause.',enumeration='Whole clause subconditions, modes, contexts, guards and limits retained via exact owner and all related complete case fields; unsupported permutations and continuous domains remainU, not declared exhaustive.'))
    write('owner-spans.json',spans)
    auxiliary=[]
    reconciliations=J(D/'association-reconciliation.json')
    for i,v in enumerate(J(D/'package-values.json')):
        a=reconciliations[i]
        auxiliary.append(dict(id=f'MPL-AUX-FILE-{i+1:02d}',required_outcome=False,route='S-route',historical_inventory_surface=v['inventory_surface'],corrected_inventory_surface=a['corrected_inventory_surface'],source_id_is_historical=a['source_id_is_historical'],association_provider=str(D/'association-reconciliation.json'),association_pointer=f'/{i}',association_sha256=OH(a),class_name=v['class'],provider=str(D/'package-values.json'),pointer=f'/{i}',record_sha256=OH(v),root_locator=v['locator'],Creator=v['root_attributes']['Creator'],MinorVersion=v['root_attributes']['MinorVersion'],raw_reopened=False,scope='Retained installed-file class/root/field presence only; historical12.4d1attribute. No current runtime/default/load/public API/DSP/lifecycle grade. Corrected spectral association is artifact-only.'))
    write('route-ledger.json',dict(schema='whole-current-clause-family-routes-v1',owner_revision=4,required_units=106,unit_policy='106whole-clause bundles, NOT atomic denominator;96D12and10U annotations on SAME106units, not96extraoutcomes;208cases navigation only;10fileSauxiliary outside required count',route_inventory=dict(X=0,S=0,no_established=106),source_annotations=dict(D12=96,U=10),required_outcomes=ledger,auxiliary=auxiliary,closure_gate='OPEN',new_grade_spec_case_release_site_credit=0))
    nav=[]
    for i,(c,o) in enumerate(zip(cases,overlay,strict=True)):
        nav.append(dict(id=c['id'],device=c['device'],requirements=c['requirements'],kind=c['kind'],provider=str(D/'cases-r3.json'),pointer=f'/{i}',record_sha256=OH(c),keys=sorted(c),field_sha256={k:OH(v) for k,v in c.items()},overlay_path=str(D/'actual-overlay-r4.json'),overlay_pointer=f'/cases/{i}',actual_record_sha256=OH(o),actual_status='U',old_exact=i<186,clause_units=[x['id'] for x in ledger if x['requirement'] in c['requirements']],read_scope='Full unique setup/action/expected/control/limit fields freshly read; shared fields equality-projected with all unique values/counts. No actual run or case-body copy.'))
    write('case-navigation.json',dict(provider=str(D/'cases-r3.json'),cases=nav,total=208,old_exact=186,new_null=22,actual_null_U=208,application_contexts=208,artifact_case_contexts=0,role='Navigation only; no independent outcomes/grades'))
    audit=J(F/'modulation-pitch-loop-source-audit/audit.json')
    html=(F/'audio-utilities/manual-audio-effects-2026-10-19.html').read_text()
    geometry,local=[],{}
    for i,b in enumerate(audit['blocks']):
        assert html[b['raw_start']:b['raw_end']]==b['raw_html']
        before=html[:b['raw_start']]
        assert before.count('\n')+1==b['html_line'] and len(before.rsplit('\n',1)[-1])==b['html_column']
        name=audit['local_owner_block_crosswalk'][b['id']];local[name]=(i,b)
        geometry.append(dict(id=b['id'],local=name,audit_pointer=f'/blocks/{i}',html_line=b['html_line'],html_column=b['html_column'],character_start=b['raw_start'],character_end=b['raw_end'],raw_utf8_sha256=H(b['raw_html'].encode()),text_sha256=H(b['text'].encode())))
    joins=[]
    for i,c in enumerate(cases):
        for j,name in enumerate(c['source_blocks']):
            k,b=local[name]
            joins.append(dict(case=c['id'],case_pointer=f'/{i}/source_blocks/{j}',local=name,audit_pointer=f'/blocks/{k}',block=b['id'],text_sha256=H(b['text'].encode())))
    write('source-geometry.json',dict(source=pin(F/'audio-utilities/manual-audio-effects-2026-10-19.html'),audit=pin(F/'modulation-pitch-loop-source-audit/audit.json'),blocks=geometry,current_case_source_block_joins=joins,scope='Fresh332rawspan/Unicodegeometry/locator joins ONLY; full332source semantics/resources inherited, not renewed. No pixel/destination inspection.'))
    write('metadata-census.json',dict(proposal=str(P/'census-proposal.json'),approval=str(P/'scope-approval-root.json'),counts=approval['counts'],selected_DATA_rows=704,row_kinds=dict(collections.Counter(r['kind'] for r in rows)),exported_prefix_slots_metadata_only=1770,selected_slots=102,unselected_slots=1668,large_leading3=20,whole_small=12,broad_census=proposal['broad_query'],caps=proposal['caps'],within_caps=True,selection='Exact approved class/addresspoint pairs;all133aliases/memberships;122seeds/160outgoingdirect/27indirect. No incoming/transitive.',exclusions=proposal['exclusions'],curve_helper_limit=proposal['curve_helper_limit'],new_C_bodies=0,new_resolved_site_credit=0))
    batch={}
    for code,a in associations.items():
        batch[code]=dict(device=devices[code],status='NOT SELECTED / not execution-ready',named_frontier_entries=[rows[k-1]['record']['entry'] for k in a['selected_named_seed_rows']],excluded_UI_seed_entries=[rows[k-1]['record']['entry'] for k in a['excluded_seed_rows']],store_entries=sorted({rows[k-1]['record']['entry'] for k in a['store_rows']}),prefix_targets=sorted({s['target'] for k in a['table_rows'] for s in rows[k-1]['record']['slots']}),case_inputs=[dict(id=c['id'],pointer=f'/{i}',action_pointer=f'/{i}/setup_and_action',controls_limits_provider='full immutable case plus prerequisites.json') for i,c in enumerate(cases) if c['device']==devices[code]],callable_X_leaves_established=[],missing_execution_inputs='Target/body bytes unread; no receiver/ABI/state/provider/public binding or complete input-domain proof. No stubs/model/comparator/fixture/output oracle invented.')
    write('batch-inputs.json',batch)
    paths=[D/n for n in ['manifest-author-r4.json','spec-r4.md','requirements.json','cases-r3.json','cases.json','actual-overlay-r4.json','adoption-r4.json','stimulus-recipes.json','package-values.json','schema-fields.json','association-reconciliation.json','spectral-folder-observations.json','sources.json']]
    paths += [F/'reviews'/n for n in ['modulation-pitch-loop-owner-r4-review.json','modulation-pitch-loop-source-audit-review.json','inventory-spectral-alias-review.json','component-resolution-v1-review.json','integration-structure-v1-review.json','family-mix-routes-v1-review.json','family-automation-routes-v1-review.json']]
    paths += [F/n for n in ['modulation-pitch-loop-source-audit/manifest.json','modulation-pitch-loop-source-audit/audit.json','audio-utilities/manual-audio-effects-2026-10-19.html','component-resolution-v1/manifest.json','integration-structure-v1/manifest.json','integration-structure-v1/mix-structure.md','integration-structure-v1/mix-component-edges.json','family-mix-routes-v1/manifest.json','family-mix-routes-v1/structure.md','family-automation-routes-v1/manifest.json','family-automation-routes-v1/structure.md']]
    paths += [Path(p) for p in sorted({r['provider'] for r in rows})]
    write('source-pins.json',dict(files=[pin(p) for p in paths],scope='Selected immutable owner/provider/review inputs; metadata fullprovider hashes custody only. No whole old archive/universe replay, Cbody or provider tool. Mutable governance as-of only, no future gate.'))
    write('research-prefix.json',dict(path=str(R/'wiki/research/modulation-pitch-loop-devices.md'),bytes=len(prefix),sha256=H(prefix),policy='Entire15924byte prior research prefix, including date metadata, stays exact. Separate research-append.md is proposed for Root adoption only.'))
    write('sources.json',dict(owner_manifest=pin(D/'manifest-author-r4.json'),owner_spec=pin(D/'spec-r4.md'),owner_review=pin(F/'reviews/modulation-pitch-loop-owner-r4-review.json'),source_audit_manifest=pin(F/'modulation-pitch-loop-source-audit/manifest.json'),source_audit_review=pin(F/'reviews/modulation-pitch-loop-source-audit-review.json'),source_semantics='Full332blocks inherited; geometry fresh only. SealedR3 inadequatepointercheck historical/not replayed. Correct230metadata pointers use top-level/i.',component=dict(manifest_sha256='392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b',original_resolved_sites=25071,conditional_additions=24,combined_inventory=25095,denominator=268015,new_credit=0),integration=dict(manifest_sha256='7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83',interfaces=['I-05','I-06','I-07','I-08','I-09','I-10'],limits='Approved bounded prior map inherited; no new traversal. Event/control/device/host/save/recording joins not implied.'),spectral='Resonator→Transmute,Time→Spectral corrected package/schema associations only; crossed discovery sources historical. No runtimeequivalence.'))
    print(json.dumps(dict(status='authored-in-owned-directory',required_units=106,D12_same_unit_annotations=96,U_same_unit_annotations=10,cases=208,old_exact=186,actual_U=208,selected_DATA_rows=704,geometry_blocks=len(geometry),case_source_joins=len(joins),pins=len(paths),research_unchanged=True,final_manifest_written=False)))


if __name__=='__main__':
    main()
