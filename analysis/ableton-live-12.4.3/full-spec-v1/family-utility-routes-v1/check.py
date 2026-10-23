#!/usr/bin/env python3
"""Owned stdlib integrity only. No capture, decoding, old script or numerical model."""
import collections,copy,hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def digest(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((HERE/n).read_text())
def pointer(value,path):
    for part in path.split('/')[1:] if path else []:
        part=part.replace('~1','/').replace('~0','~')
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value
def objhash(v):return digest(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def validate(ledger,inputs,edges,refs):
    rows=ledger['rows']; assert len(rows)==48
    assert ledger['denominator'] is None and ledger['whole_family_complete'] is False and ledger['new_grade_count']==0
    assert collections.Counter(r['route'] for r in rows)=={'no-established-route':46,'S':2}
    assert set(r['id'] for r in rows)=={f'UT-OUT-{i:03d}' for i in range(1,49)}
    assert {r['requirement'] for r in rows}=={f'REQ-DEVICE-UTILITY-{i:03d}' for i in range(1,16)}
    for r in rows:
        assert r['expected'] is None and r['actual'] is None and r['comparison'] is None and r['new_grade'] is False
        assert r['source_span']==r['requirement']
        assert r['route'] in ['S','no-established-route']
        if r['route']=='S':assert r['route_scope']=='retained-file-only' and r['requirement'].endswith('014')
        else:assert r['route_scope']=='exact-target-public-application' and r['missing_join']
        assert r['context_and_premises'] and r['observable']
    records=inputs['case_navigation']; assert len(records)==41
    assert {c['id'] for c in records}=={f'DUT-{i:03d}' for i in range(1,42)}
    assert sum(c['existing_target_grade']=='U' for c in records)==38
    assert sum(c['existing_target_grade']=='Dpkg' for c in records)==3
    assert all(c['execution']=='unexecuted' for c in records)
    assert inputs['totals']=={'requirements':15,'case_objects':41,'application_U':38,'retained_file_checks':3,'existing_original_children':2,'existing_returned_original_calls':6,'new_calls':0,'new_cases':0}
    assert {c for r in rows for c in r['existing_cases']}=={c['id'] for c in records}
    assert [x['returned_original_calls'] for x in inputs['auxiliary_leaf_sets']]==[2,4]
    assert [x['child_count'] for x in inputs['auxiliary_leaf_sets']]==[1,1]
    assert len(edges['edges'])==18 and edges['runtime_sequence_established'] is False
    for e in edges['edges']:
        assert e['new_runtime_observation'] is False
        assert all(r in refs['references'] for r in e['evidence'])
        assert e['premises_or_missing_join']
    byid={e['id']:e for e in edges['edges']}
    for i in ['E01','G01','G02','G03','G04','G05','G06']:assert byid[i]['classification']=='unknown'
    for i in ['E10','E11']:assert byid[i]['classification']=='existing-X-ungraded'
    assert byid['E12']['classification']=='root-readback-only nomination'
    assert '193opaque' in byid['E12']['state_or_data'] and 'pending' in byid['E12']['premises_or_missing_join']
    assert 'bit0' in byid['E08']['state_or_data'] and 'fullbyte!=0' in byid['E09']['premises_or_missing_join']
    assert '708unread' in byid['E08']['premises_or_missing_join'] and '724skipped' in byid['E08']['premises_or_missing_join']
    guard=next(r for r in rows if r['observable'].startswith('Disabled Width'))
    assert 'EACH' in guard['context_and_premises'] and 'BOTH' in guard['context_and_premises']
    dc=next(r for r in rows if r['observable'].startswith('Relevant low/DC'))
    assert 'not sufficient' in dc['context_and_premises'] and 'AFTER' in dc['context_and_premises']
    tail=next(r for r in rows if r['observable'].startswith('Mute can cut'))
    assert 'NONZERO' in tail['context_and_premises'] and 'BEFORE' in tail['context_and_premises']
def main():
    if sys.argv[1:]!=['--check']:raise SystemExit('Only --check is supported; no execution/write/seal mode.')
    pins=read('pins.json')['providers']; data={}; before={};asof=[]
    for p in pins:
        path=ROOT/p['path']; b=path.read_bytes(); actual={'bytes':len(b),'sha256':digest(b)}
        before[p['path']]=actual
        if p['kind']=='immutable':assert actual=={k:p[k] for k in actual},p['id']
        else:asof.append({'id':p['id'],'equal_asof':actual=={k:p[k] for k in actual}})
        if path.suffix=='.json':data[p['id']]=json.loads(b)
    ledger=read('route-ledger.json');inputs=read('input-sets.json');edges=read('chain-edges.json');refs=read('evidence-locators.json')
    validate(ledger,inputs,edges,refs)
    profile=data['catalog']['profiles']['utility']; assert len(profile['requirements'])==15 and len(profile['cases'])==41
    for c in inputs['case_navigation']:
        v=pointer(data[c['provider']],c['pointer']);assert v['id']==c['id'] and objhash(v)==c['object_sha256']
        assert v['target_grade']==c['existing_target_grade'] and v['execution']==c['execution']
    filegroup=inputs['groups']['retained-file-vocabulary'];assert len(filegroup['saved_records'])==10
    for f in [filegroup['schema_record']]+filegroup['saved_records']:
        v=pointer(data[f['provider']],f['pointer']);assert objhash(v)==f['object_sha256']
    assert pointer(data['schema-fields'],filegroup['schema_record']['pointer'])['class']=='StereoGain'
    for f in filegroup['saved_records']:assert pointer(data['package-values'],f['pointer'])['device']=='Utility'
    for m in read('source-spans.json')['manual']:
        v=pointer(data[m['provider']],m['pointer']);assert v['locator']==m['locator'] and digest(v['text'].encode())==m['text_sha256']
    spans=read('source-spans.json')['requirements'];assert len(spans)==15
    snapshots={p['id']:ROOT/p['path'] for p in pins}
    for s in spans:
        b=snapshots[s['provider']].read_bytes();raw=b[s['start_byte']:s['end_byte_exclusive']]
        assert digest(raw)==s['sha256'] and b[:s['start_byte']].count(b'\n')+1==s['start_line']
        q=pointer(data['catalog'],s['catalog_pointer']); assert q['id']==s['id']
        assert digest(q['contract'].encode())==s['contract_sha256'] and q['contract'].encode() in raw
    resolved=[]
    for key,ref in refs['references'].items():
        value=pointer(data[ref['provider']],ref['pointer']);resolved.append({'id':key,'provider':ref['provider'],'pointer':ref['pointer'],'value_sha256':objhash(value)})
    for a in inputs['auxiliary_leaf_sets']:
        argv=pointer(data[a['provider']],a['pointer']); assert isinstance(argv,list) and argv
        parsed=data[a['parsed_provider']]
        if a['id']=='X-OWNED-4':assert parsed['actual_expected'] is None and parsed['comparison'] is None and parsed['new_grade']==0
        else:assert 'actual_expected' not in parsed and 'comparison' not in parsed  # parent format: no grading fields, not an inferred null record
        assert parsed['completed_original_call_rows']==a['returned_original_calls']
    delta=read('research-change.json');b=(ROOT/delta['path']).read_bytes()
    assert delta['after_bytes']==delta['before_bytes']+len(delta['append'].encode())
    research_current_is_author_asof=(len(b)==delta['after_bytes'] and digest(b)==delta['after_sha256'])
    if research_current_is_author_asof:
        assert digest(b[:delta['before_bytes']])==delta['before_sha256']
        assert b[delta['before_bytes']:delta['after_bytes']]==delta['append'].encode()
    # A later canonical edit is an as-of report, never a future live-page gate.
    tests=[]
    def bad(name,alter):
        v=copy.deepcopy((ledger,inputs,edges,refs));alter(*v)
        try:validate(*v)
        except (AssertionError,KeyError):tests.append(name)
        else:raise AssertionError('accepted unsafe mutation: '+name)
    bad('promote-public-Mute-to-X',lambda l,i,e,r:next(x for x in l['rows'] if x['observable'].startswith('Mute silences')).update(route='X'))
    bad('package-values-runtime',lambda l,i,e,r:next(x for x in l['rows'] if x['route']=='S').update(route_scope='exact-target-public-application'))
    bad('invent-application-actual',lambda l,i,e,r:l['rows'][0].update(actual='pass'))
    bad('freeze-whole-denominator',lambda l,i,e,r:l.update(denominator=48))
    bad('omit-lifecycle-context',lambda l,i,e,r:l['rows'].pop())
    bad('case-grade-promotion',lambda l,i,e,r:i['case_navigation'][0].update(existing_target_grade='X'))
    bad('calls-counted-as-public-outcomes',lambda l,i,e,r:i['totals'].update(application_U=32))
    bad('owned-history-extra-child',lambda l,i,e,r:i['auxiliary_leaf_sets'][1].update(child_count=2))
    bad('generic-mix-proves-Utility',lambda l,i,e,r:e['edges'][0].update(classification='proved'))
    bad('prefix-readback-independent-approval',lambda l,i,e,r:e['edges'][11].update(classification='independently-approved'))
    bad('consume-opaque-prefix-suffix',lambda l,i,e,r:e['edges'][11].update(state_or_data='240decodedbytes'))
    bad('ARM-bit0-equals-x86-fullbyte',lambda l,i,e,r:e['edges'][8].update(premises_or_missing_join='same semantics'))
    bad('wrong-return-geometry',lambda l,i,e,r:e['edges'][7].update(premises_or_missing_join='all744read'))
    bad('no-productive-width',lambda l,i,e,r:next(x for x in l['rows'] if x['observable'].startswith('Disabled Width')).update(context_and_premises='enabled flags'))
    bad('DC-sufficient',lambda l,i,e,r:next(x for x in l['rows'] if x['observable'].startswith('Relevant low/DC')).update(context_and_premises='always audible'))
    bad('silent-tail-positive',lambda l,i,e,r:next(x for x in l['rows'] if x['observable'].startswith('Mute can cut')).update(context_and_premises='effect enabled'))
    for p in pins:
        b=(ROOT/p['path']).read_bytes();assert before[p['path']]=={'bytes':len(b),'sha256':digest(b)},p['path']
    print(json.dumps({'status':'PASS-author-data-integrity-only','requirements':15,'route_rows':48,'routes':{'X':0,'S_file_only':2,'no_established_public_route':46},'case_objects':41,'application_U':38,'file_checks':3,'existing_children':2,'existing_returned_calls':6,'new_calls':0,'new_grades':0,'immutable_pins':sum(p['kind']=='immutable' for p in pins),'watched_unchanged':len(pins),'asof_context':asof,'contract_spans':len(spans),'dereferenced_evidence':resolved,'negative_controls_rejected':tests,'research_prefix_preserved_at_author_asof':research_current_is_author_asof,'new_source_or_binary_reads':False,'old_script_imports_or_executions':False},indent=2))
if __name__=='__main__':main()
