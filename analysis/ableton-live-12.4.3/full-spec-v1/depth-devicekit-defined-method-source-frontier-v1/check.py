"""Read-only selected retained-data check. Never opens chunks, indexes or binaries."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

P=Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(n):
    return json.loads((P/n).read_text())


def lexical(d):
    refs=[]
    for n,line in enumerate(d['code'].splitlines(keepends=True),1):
        for call in re.finditer(r'\b((?:thunk_)?FUN_[0-9a-f]+)\s*\(',line):
            refs.append((n,call[1],'lexical-direct-call'))
        if '(*(code *)' in line or '(**(code **)' in line or '(*pcVar2)' in line:
            refs.append((n,line.strip(),'indirect-expression'))
    return refs


def validate(d):
    c,s,r,claims,front,joins,a,read=d['census'],d['selection'],d['rows'],d['claims'],d['front'],d['joins'],d['assessment'],d['read']
    wanted=s['entries']
    assert len(wanted)==len(set(wanted))==27
    assert [x['entry'] for x in c['records']]==wanted==[x['entry'] for x in r]
    assert len(d['raw_rows'])==27 and sha(b''.join(d['raw_rows']))=='cfbcf09c564efdfd5902f6647d11922f9ba931ee23ae473a4d6fd30a74370ad2'
    assert sum(len(x) for x in d['raw_rows'])==138935
    assert sum(len(x['code'].encode()) for x in r)==121309
    assert sum(len(x['code'].splitlines()) for x in r)==3601
    assert max(len(x['code'].splitlines()) for x in r)==241
    assert len({x['source_path'] for x in c['records']})==8
    assert sum(bool(x['warnings']) for x in r)==4
    retention=d['retention']
    assert retention['selected_raw_bytes']==138935 and retention['retained_sha256']==sha(b''.join(d['raw_rows']))
    assert retention['fresh_chunk_full_hashes']==0 and retention['inherited_chunk_pins']==c['selected_chunk_pins']
    assert len(retention['records'])==27
    offset=0
    for x,m,raw,loc in zip(r,c['records'],d['raw_rows'],retention['records']):
        assert json.loads(raw)==x
        assert len(raw)==m['raw_bytes'] and sha(raw)==m['raw_sha256']
        assert sha(x['code'].encode())==m['code_sha256']
        assert len(x['code'].encode())==m['code_utf8_bytes']
        assert len(x['code'].splitlines())==m['C_lines']
        assert x['body_bytes']==m['native_body_bytes'] and x['body_ranges']==m['native_body_ranges']
        assert sum(int(y,16)-int(z,16)+1 for z,y in x['body_ranges'])==x['body_bytes']
        assert not x['thunk'] and not m['alias_thunk'] and not m['record_thunk']
        assert not x['timed_out'] and not x['partial_code'] and x['error'] is None
        assert x['warnings']==m['warnings']
        assert loc==dict(entry=m['entry'],source_path=m['source_path'],source_line=m['source_line'],source_byte=m['source_byte'],raw_bytes=len(raw),raw_sha256=sha(raw),retained_byte=offset,C_bytes=len(x['code'].encode()),C_lines=m['C_lines'],C_sha256=m['code_sha256'],stat_unchanged=True)
        offset+=len(raw)
    methods=collections.Counter(m['alias_name'].rsplit('::',1)[1] for m in c['records'])
    assert methods==dict(ODeviceKitSampleRateProcessor=2,Init=7,Exit=7,UpdateOutX=2,OnMidi=2,CalcMain=7)
    assert len(claims['premises'])==8
    assert 'not a validated native ABI' in claims['premises'][0]
    assert 'opaque' in claims['premises'][3]
    assert 'not establish actual stub destination' in claims['premises'][4]
    assert 'not complete message layouts' in claims['premises'][5]
    assert 'Warning-bearing' in claims['premises'][6]
    assert [x['entry'] for x in claims['claims']]==wanted
    assert sum(len(x['statements']) for x in claims['claims'])==86
    statement_ids=[]
    for x,m,src in zip(claims['claims'],c['records'],r):
        assert x['source_metadata']==m and x['complete_C_read']
        assert x['read_C_lines']==[1,len(src['code'].splitlines())]
        assert x['warnings']==m['warnings'] and 'metadata only' in x['native_extent_basis']
        assert x['legal_inputs'] is x['stub_recipe'] is x['expected_output'] is None
        assert not x['execution_ready'] and not x['math_leaf']
        lines=src['code'].splitlines(keepends=True)
        assert x['statements']
        for q in x['statements']:
            statement_ids.append(q['id'])
            lo,hi=q['C_start'],q['C_end']
            assert 1<=lo<=hi<=len(lines)
            b=''.join(lines[lo-1:hi]).encode()
            assert len(b)==q['span_utf8_bytes'] and sha(b)==q['span_sha256']
            assert q['premises']==list(range(1,9)) and q['status']=='observed-static-projection'
            assert not q['public_route'] and not q['complete_callable_leaf']
    assert len(statement_ids)==len(set(statement_ids))==86
    assert [x['entry'] for x in front['records']]==wanted
    assert sum(len(x['references']) for x in front['records'])==173
    for x,src in zip(front['records'],r):
        assert [(q['C_line'],q['token'],q['kind']) for q in x['references']]==lexical(src)
        assert all(not q['followed'] and not q['target_body_read'] for q in x['references'])
        assert not x['legal_whole_function_X'] and x['new_original_batch'] is None
        assert len(x['missing'])==4
    assert not front['encounter_follow'] and front['new_native_or_provider_reads']==0 and not front['successor_selected']
    assert [x['entry'] for x in joins['joins']]==wanted and joins['source_occurrences']==37
    assert len(joins['joins'])==27 and not joins['runtime_binding'] and joins['new_resolved_sites']==0
    all_boundary=[]
    for j,m in zip(joins['joins'],c['records']):
        ss=[x for x in d['symbols'] if x['lexical_symbol']=='<EXTERNAL>::'+m['alias_name']]
        aa=[x for x in d['actual'] if x['raw_nlist_fields']['n_value']==int(j['entry'],16)]
        assert len(ss)==len(aa)==1
        sym,act=ss[0],aa[0]
        assert j['stub_declaration']==act['stub_address'] and j['nlist_index']==act['nlist_index']
        assert j['boundary_rows']==sym['boundary_rows']==act['source_rows']
        assert j['external_label']==sym['external_label'] and j['retained_alias']==m['alias_name']
        assert j['n_type']==15 and j['n_desc']==128
        assert not j['actual_stub_destination'] and not j['provider_binding'] and not j['same_current_receiver']
        all_boundary+=j['boundary_rows']
    assert len(all_boundary)==len(set(all_boundary))==37
    for k in ['complete_callable_math_leaves','complete_callable_X_leaves','ready_original_batches','new_site_credit','new_required_outcomes','new_case_grade_release']:
        assert a[k]==0
    for k in ['runtime_stub_binding','actual_provider_binding','actual_current_parameter_binding','actual_audio_or_host_delivery','documentary_fallback','successor_selected']:
        assert a[k] is False
    assert a['legal_inputs'] is a['calibrated_metric'] is None
    assert a['coverage_gate']=='OPEN' and a['required_unsupported']=='U'
    assert a['existing_inventory']==dict(resolved_reference=25071,conditional_class=24,total=25095,all_indirect=268015)
    assert 'separate selection' in a['setup_gate'] and 'No run selected' in a['setup_gate']
    assert read['fresh_semantic_read']==dict(records=27,C_utf8_bytes=121309,C_lines=3601,warning_records=4,whole_bodies=True,all_selected_metadata=True)
    assert not read['source_read_successor'] and read['original_model_comparator_runs']==read['canonical_or_shared_writes']==0
    return True


def main():
    assert sys.argv[1:]==['--check']
    hard={'candidate-census.json':(34533,'2eeae8cc2f6cddfd9f913c8e169f1d5ff3966d9a8228697b075346746d16fcf6'),
          'metadata-census-root.py':(4450,'fa4a3b0ef64def8bac004a58a1199f93ac52ab80642dca64133d61479f49ec53'),
          'selection-metadata-only.json':(2212,'5ec546bd4ec72c4d04eb17368564adbf16665fae1ed0ff1915ff93c36f805b88'),
          'selection-source-read.json':(2144,'16754c5909db05926a232210ca0e023e79fe586592adbd52165ba3e2c1658032')}
    for name,(size,h) in hard.items():
        raw=(P/name).read_bytes();assert len(raw)==size and sha(raw)==h
    pins=load('pins.json');seen=set()
    for v in pins['protected_root']+pins['immutable']:
        q=Path(v['path']);assert '/decomp/' not in str(q) and '/indexes/' not in str(q) and q.suffix in ['.json','.py']
        raw=q.read_bytes();assert len(raw)==v['bytes'] and sha(raw)==v['sha256'];seen.add(str(q))
    asof=[]
    for v in pins['asof']:
        raw=Path(v['path']).read_bytes();asof.append(dict(path=v['path'],matches_asof=len(raw)==v['bytes'] and sha(raw)==v['sha256'],future_gate=False))
    actual_path=next(x['path'] for x in pins['immutable'] if x['role']=='reviewed declaration values only')
    symbols_path=next(x['path'] for x in pins['immutable'] if x['role']=='exact27symbol37boundary navigation')
    raw_rows=(P/'sources.jsonl').read_bytes().splitlines(keepends=True)
    d=dict(census=load('candidate-census.json'),selection=load('selection-source-read.json'),raw_rows=raw_rows,rows=[json.loads(x) for x in raw_rows],retention=load('source-retention.json'),claims=load('claims.json'),front=load('call-frontiers.json'),joins=load('declaration-source-joins.json'),assessment=load('assessment.json'),read=load('read-receipt.json'),actual=json.loads(Path(actual_path).read_text())['rows'],symbols=json.loads(Path(symbols_path).read_text())['symbols'])
    assert validate(d)
    negatives=[]
    def reject(name,fn):
        bad=copy.deepcopy(d);fn(bad)
        try:validate(bad)
        except (AssertionError,KeyError,IndexError,TypeError,ValueError):negatives.append(dict(name=name,rejected=True));return
        raise AssertionError('negative accepted: '+name)
    reject('omit-one-selected-source',lambda x:x['rows'].pop())
    reject('alter-retained-code',lambda x:x['rows'][0].update(code='void f(){}'))
    reject('change-native-metadata',lambda x:x['rows'][0].update(body_bytes=4))
    reject('erase-warning',lambda x:x['rows'][0].update(warnings=[]))
    reject('claim-thunk-as-body',lambda x:x['rows'][0].update(thunk=True))
    reject('wrong-retained-byte-locator',lambda x:x['retention']['records'][0].update(retained_byte=1))
    reject('wrong-original-source-locator',lambda x:x['retention']['records'][0].update(source_byte=0))
    reject('omit-one-whole-method-claim',lambda x:x['claims']['claims'].pop())
    reject('wrong-C-span',lambda x:x['claims']['claims'][0]['statements'][0].update(C_start=28))
    reject('drop-memory-ABI-premise',lambda x:x['claims']['claims'][0]['statements'][0].update(premises=[2,3,4]))
    reject('opaque-helper-promoted-to-known',lambda x:x['claims']['premises'].__setitem__(3,'All helpers understood'))
    reject('invent-public-route',lambda x:x['claims']['claims'][0]['statements'][0].update(public_route=True))
    reject('invent-complete-local-leaf',lambda x:x['claims']['claims'][0]['statements'][0].update(complete_callable_leaf=True))
    reject('invent-legal-input-recipe',lambda x:x['claims']['claims'][0].update(legal_inputs=[0]))
    reject('wrong-encountered-call',lambda x:x['front']['records'][0]['references'][0].update(token='FUN_100000000'))
    reject('drop-call-frontier',lambda x:x['front']['records'][0]['references'].pop())
    reject('autofollow-callee',lambda x:x['front']['records'][0]['references'][0].update(followed=True))
    reject('claim-unread-target-body',lambda x:x['front']['records'][0]['references'][0].update(target_body_read=True))
    reject('swap-declaration-value',lambda x:x['joins']['joins'][0].update(stub_declaration=x['joins']['joins'][1]['stub_declaration']))
    reject('invent-stub-runtime-destination',lambda x:x['joins']['joins'][0].update(actual_stub_destination=True))
    reject('invent-provider-binding',lambda x:x['joins']['joins'][0].update(provider_binding=True))
    reject('invent-same-current-receiver',lambda x:x['joins']['joins'][0].update(same_current_receiver=True))
    reject('invent-callable-X',lambda x:x['assessment'].update(complete_callable_X_leaves=1))
    reject('invent-math-leaf',lambda x:x['assessment'].update(complete_callable_math_leaves=1))
    reject('invent-current-control-binding',lambda x:x['assessment'].update(actual_current_parameter_binding=True))
    reject('invent-audio-host-delivery',lambda x:x['assessment'].update(actual_audio_or_host_delivery=True))
    reject('invent-calibrated-metric',lambda x:x['assessment'].update(calibrated_metric={'rms':0.01}))
    reject('bypass-setup-gate',lambda x:x['assessment'].update(setup_gate='standing approved'))
    reject('invent-site-credit',lambda x:x['assessment'].update(new_site_credit=27))
    reject('close-unsupported',lambda x:x['assessment'].update(required_unsupported='PASS'))
    reject('close-coverage',lambda x:x['assessment'].update(coverage_gate='COMPLETE'))
    reject('documentary-completion',lambda x:x['assessment'].update(documentary_fallback=True))
    reject('select-successor',lambda x:x['assessment'].update(successor_selected=True))
    print(json.dumps(dict(status='PASS',checker_sha256=sha(Path(__file__).read_bytes()),Root4_preserved=True,immutable_document_pins=len(seen),asof_context=asof,records=27,raw_bytes=138935,C_utf8_bytes=121309,C_lines=3601,warning_records=4,claims=86,declaration_joins=27,boundary_occurrences=37,lexical_C_references=173,negative_count=len(negatives),negative_controls=negatives,complete_callable_math_X_leaves=0,original_provider_native_image_decoder_harness_model_comparator_runs=0,shared_or_canonical_writes=0,coverage_gate='OPEN',required_unsupported='U',successor_selected=False,limits='Read-only retained-data integrity and in-memory false-promotion controls, not independent semantic or runtime proof. No chunks/indexes/priorraw/binary/image/provider or old module opened/executed.'),indent=2))


if __name__=='__main__':
    main()
