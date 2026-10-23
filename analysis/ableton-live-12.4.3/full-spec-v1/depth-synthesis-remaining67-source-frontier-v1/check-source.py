"""Read-only fixed67 retained-source integrity and false-promotion guards."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

P=Path(__file__).resolve().parent


def sha(b):return hashlib.sha256(b).hexdigest()


def load(n):return json.loads((P/n).read_text())


def refs(row):
    out=[];lines=row['code'].splitlines();start=next(i for i,l in enumerate(lines,1) if l.strip()=='{')
    for i,l in enumerate(lines,1):
        if i<=start:continue
        for m in re.finditer(r'\b((?:thunk_)?FUN_[0-9a-f]+)\s*\(',l):out.append((i,'lexical-FUN-call',m[1]))
        if '(**(code **)' in l or '(*(code *)' in l or '(*pcVar1)' in l:out.append((i,'indirect-expression',l.strip()))
    return out


def validate(d):
    c,s,rows,a,read,front,whole,receipt=(d[x] for x in ['census','selection','rows','assessment','read','front','whole','receipt'])
    assert len(rows)==len(c['records'])==len(a['records'])==len(read['records'])==len(front['records'])==67
    assert [x['entry'] for x in rows]==s['entries']==[x['entry'] for x in c['records']]
    assert sum(len(x['code'].encode()) for x in rows)==29288 and sum(len(x['code'].splitlines()) for x in rows)==1231
    assert sum(bool(x['warnings']) for x in rows)==13 and sum(len(x['warnings']) for x in rows)==20
    assert sum(x['thunk'] for x in rows)==15 and sum(x['body_bytes']==4 for x in rows)==30
    assert len(a['premises'])==7 and 'Expanded4B' in a['premises'][1] and 'unread' in a['premises'][3]
    assert len(receipt['records'])==receipt['raw_range_reads']==67 and receipt['raw_content_bytes']==58352
    assert receipt['retained_sha256']=='ec6ea5faa2ad337d3264464947771be52a13b880f869072f6da7cff5acf4e454' and not receipt['source_expansion']
    anchors=0;offset=0;expanded=[]
    for i,(row,meta,item,rec,rd,fr) in enumerate(zip(rows,c['records'],a['records'],receipt['records'],read['records'],front['records'])):
        lines=row['code'].splitlines(keepends=True)
        assert row['entry']==item['entry']==rec['entry']==rd['entry']==fr['entry']
        assert row['code_sha256']==meta['code_sha256']==item['code_sha256']==rd['code_sha256']==sha(row['code'].encode())
        assert len(row['code'].encode())==meta['code_utf8_bytes'] and len(lines)==meta['C_lines']
        for k in ['body_bytes','body_ranges','thunk','warnings','state','error','partial_code','timed_out']:assert row[k]==meta[k]
        assert item['native_body_bytes']==row['body_bytes'] and item['native_body_ranges']==row['body_ranges'] and item['record_thunk']==row['thunk'] and item['warning_texts']==row['warnings']
        assert not row['partial_code'] and not row['timed_out'] and row['error'] is None
        assert item['extent_basis']=='retained metadata only; no native instruction/ABI/full-target proof'
        expect=row['body_bytes']==4 and not row['thunk'] and len(lines)>11
        assert item['expanded_4B_false_thunk']==expect
        if expect:expanded.append(row['entry'])
        assert item['fresh_full_C_read'] and item['whole_C_lines']==[1,len(lines)] and item['premises']==list(range(1,8))
        assert item['complete_callable_X_leaf'] is item['complete_callable_math_leaf'] is item['public_route'] is False
        assert item['legal_inputs'] is item['expected_result'] is None
        assert item['role'] not in ['constructor','destructor','complete-filter','math-X']
        assert item['anchors']
        for x in item['anchors']:
            lo,hi=x['C_start'],x['C_end'];assert 1<=lo<=hi<=len(lines)
            b=''.join(lines[lo-1:hi]).encode();assert len(b)==x['span_utf8_bytes'] and sha(b)==x['span_sha256'];anchors+=1
        assert rec['retained_byte']==offset and rec['raw_bytes']==meta['raw_bytes'] and rec['raw_sha256']==meta['raw_sha256']
        assert (rec['original_path'],rec['original_line'],rec['original_byte'])==(meta['source_path'],meta['source_line'],meta['source_byte']);offset+=rec['raw_bytes']
        assert rd['C_lines']==[1,len(lines)] and rd['method']=='direct complete numbered C projection; all warning text read'
        assert [(x['C_line'],x['kind'],x['token']) for x in fr['references']]==refs(row)
        assert all(x['followed'] is False for x in fr['references']) and not fr['legal_complete_function_X'] and fr['new_execution'] is None
        assert len(fr['missing'])==4
    assert anchors==72 and expanded==['0x101c18384','0x101c183f0','0x101c18550','0x101c18554','0x101f62e5c'] and offset==58352
    assert sum(len(x['references']) for x in front['records'])==front['references']==189
    assert not front['callee_global_slot_native_provider_follow'] and front['new_original_batch'] is None and not front['successor_selected']
    assert a['complete_callable_math_leaves']==a['complete_callable_X_leaves']==a['ready_original_batches']==a['new_required_outcome_site_grade_case_release']==0
    assert a['legal_inputs'] is a['calibrated_metric'] is None and not a['successor_selected']
    assert a['required_unsupported']=='U' and a['coverage_gate']=='OPEN'
    assert a['existing_inventory']==dict(required_clauses=110,actual_U_cases=190,required_predicate_inventory=585,X=0,S=0,no_established_route=585,resolved_indirect_inventory=25095,total_indirect_inventory=268015)
    assert read['complete_records']==67 and read['C_utf8_bytes']==29288 and read['C_lines']==1231 and read['warning_records']==13 and read['warning_occurrences']==20
    assert read['new_alias_chunk_hash_passes']==0 and not read['source_expansion']
    assert len(whole['claims'])==7 and len(whole['frontiers'])==5 and not whole['new_selection']
    assert all(x['status']=='OPEN' and x['missing'] for x in whole['frontiers'])


def main():
    assert sys.argv[1:]==['--check']
    stage_raw=(P/'metadata-stage.json').read_bytes();assert (len(stage_raw),sha(stage_raw))==(1539,'638a17ee223815762d6ea0bef6df5bad6130d274d2701ec76dbf1c02fbcdb733')
    stage=json.loads(stage_raw)
    for x in stage['files']:
        b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
    sr=(P/'selection-source-read.json').read_bytes();assert (len(sr),sha(sr))==(3582,'4994ea2c0ff9281d75280b173507b17650747a08914aea7133048b5e0e3d432c')
    raw=(P/'selected-records.jsonl').read_bytes();assert (len(raw),sha(raw))==(58352,'ec6ea5faa2ad337d3264464947771be52a13b880f869072f6da7cff5acf4e454')
    rawrows=raw.splitlines(keepends=True);c=load('candidate-census.json')
    for b,m in zip(rawrows,c['records']):assert len(b)==m['raw_bytes'] and sha(b)==m['raw_sha256']
    d=dict(census=c,selection=json.loads(sr),rows=[json.loads(x) for x in rawrows],assessment=load('source-assessment.json'),read=load('source-read-map.json'),front=load('call-frontiers.json'),whole=load('whole-set-claims.json'),receipt=load('source-retention-receipt.json'))
    validate(d);neg=[]
    def reject(name,fn):
        q=copy.deepcopy(d);fn(q)
        try:validate(q)
        except (AssertionError,ValueError,KeyError,TypeError,IndexError,StopIteration):neg.append(dict(name=name,rejected=True));return
        raise AssertionError(name)
    reject('omit-whole67-entry',lambda q:q['rows'].pop())
    reject('change-source-body',lambda q:q['rows'][0].update(code='void f(){}'))
    reject('erase-source-warning',lambda q:q['rows'][0].update(warnings=[]))
    reject('repair-fourB-nativeextent',lambda q:q['assessment']['records'][4].update(native_body_bytes=200))
    reject('erase-expanded-projection-mismatch',lambda q:q['assessment']['records'][4].update(expanded_4B_false_thunk=False))
    reject('attribute-full-native-target',lambda q:q['assessment']['records'][4].update(extent_basis='full native target verified'))
    reject('invent-constructor-role',lambda q:q['assessment']['records'][4].update(role='constructor'))
    reject('invent-destructor-role',lambda q:q['assessment']['records'][2].update(role='destructor'))
    reject('wrong-anchor-start',lambda q:q['assessment']['records'][0]['anchors'][0].update(C_start=6))
    reject('wrong-retained-offset',lambda q:q['receipt']['records'][0].update(retained_byte=4))
    reject('wrong-original-locator',lambda q:q['receipt']['records'][0].update(original_byte=0))
    reject('remove-memory-ABI-premises',lambda q:q['assessment']['records'][0].update(premises=[1,2]))
    reject('invent-callable-math',lambda q:q['assessment']['records'][7].update(complete_callable_math_leaf=True))
    reject('invent-legal-X-vector',lambda q:q['assessment']['records'][7].update(legal_inputs=[440]))
    reject('invent-calibrated-output',lambda q:q['assessment'].update(calibrated_metric=0.01))
    reject('invent-public-route',lambda q:q['assessment']['records'][34].update(public_route=True))
    reject('follow-source-callee',lambda q:q['front']['records'][0]['references'][0].update(followed=True))
    reject('drop-call-frontier',lambda q:q['front']['records'][0]['references'].pop())
    reject('source-call-header-as-edge',lambda q:q['front']['records'][0]['references'].append(dict(C_line=2,kind='lexical-FUN-call',token='FUN_10128eed4',followed=False)))
    reject('replay-alias-hash-pass',lambda q:q['read'].update(new_alias_chunk_hash_passes=1))
    reject('source-expansion',lambda q:q['read'].update(source_expansion=True))
    reject('invent-outcome-grade',lambda q:q['assessment'].update(new_required_outcome_site_grade_case_release=67))
    reject('close-required-U',lambda q:q['assessment'].update(required_unsupported='PASS'))
    reject('close-coverage',lambda q:q['assessment'].update(coverage_gate='CLOSED'))
    reject('close-dependency-frontier',lambda q:q['whole']['frontiers'][0].update(status='CLOSED'))
    reject('select-successor',lambda q:q['assessment'].update(successor_selected=True))
    print(json.dumps(dict(status='PASS',metadata_stage_files_preserved=7,raw_source_records=67,raw_bytes=58352,C_utf8_bytes=29288,C_lines=1231,anchors=72,lexical_references=189,warning_records=13,warning_occurrences=20,marked_thunks=15,fourBnative_metadata=30,expanded_false_thunk_mismatches=5,whole_set_claims=7,OPEN_frontiers=5,complete_callable_math_X_leaves=0,source_checker_external_index_chunk_native_image_provider_reads=0,original_harness_model_comparator_runs=0,canonical_shared_writes=0,negative_count=len(neg),negative_controls=neg,required_unsupported='U',coverage_gate='OPEN',successor_selected=False,limits='Packet-only retained-data integrity and false-promotion controls, not independent semantic approval, ABI proof or execution.'),indent=2))


if __name__=='__main__':main()
