"""Read-only fixed67 census integrity. No original alias/chunk or acquisition reader access."""
from pathlib import Path
import collections
import copy
import hashlib
import json

P=Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def validate(c,s,parent):
    rows=c['records'];wanted=s['entries']
    assert len(wanted)==len(set(wanted))==len(rows)==67
    assert [x['entry'] for x in rows]==wanted
    chunks={x['path']:x for x in c['selected_chunk_pins']}
    assert len(chunks)==23 and sum(x['bytes'] for x in chunks.values())==4030080
    assert c['source_semantics_selected'] is c['source_retention_selected'] is False
    assert c['new_callee_global_slot_native_image_provider_original_model_harness_follow']==c['new_site_grade_case_release']==0
    assert c['required_unsupported']=='U' and c['coverage_gate']=='OPEN'
    ranges=collections.defaultdict(list)
    for x in rows:
        p=parent[x['entry']]
        assert x['alias_record']==p['record'] and x['alias_source']==p['provider'] and x['alias_metadata_id']==p['id']
        assert x['alias_record']['external'] is False
        assert x['chunk_number']==x['nonexternal_ordinal']//100
        assert Path(x['source_path']).name==f"chunk-{x['chunk_number']:05}.jsonl"
        ch=chunks[x['source_path']]
        assert x['source_line']>=1 and x['source_byte']>=0 and x['raw_bytes']>0 and x['source_byte']+x['raw_bytes']<=ch['bytes']
        assert len(x['raw_sha256'])==len(x['code_sha256'])==64 and 'code' not in x
        assert x['code_present'] and x['code_utf8_bytes']>0 and 0<x['C_lines']<=145
        assert not x['partial_code'] and x['error'] is None and not x['timed_out']
        assert x['body_bytes']>0 and sum(int(hi,16)-int(lo,16)+1 for lo,hi in x['body_ranges'])==x['body_bytes']
        assert x['state']==('exported-with-warnings' if x['warnings'] else 'exported')
        ranges[x['source_path']].append((x['source_byte'],x['source_byte']+x['raw_bytes']))
    for rs in ranges.values():
        rs.sort();assert all(a[1]<=b[0] for a,b in zip(rs,rs[1:]))
    summary=c['summary']
    assert summary==dict(selected_entries=67,original_aliases_found=67,export_records_found=67,missing_alias_entries=[],missing_export_entries=[],missing_is_absence_claim=False,code_utf8_bytes=29288,C_lines=1231,max_C_lines=145,chunks=23,chunk_custody_bytes=4030080,warning_records=13,warning_occurrences=20,thunk_records=15,partial_records=0,error_records=0,timed_out_records=0,empty_code_records=0,state_counts={'exported-with-warnings':13,'exported':54},within_proposed_whole_source_caps=True)
    assert sum(x['code_utf8_bytes'] for x in rows)==29288 and sum(x['C_lines'] for x in rows)==1231
    assert sum(bool(x['warnings']) for x in rows)==13 and sum(len(x['warnings']) for x in rows)==20 and sum(x['thunk'] for x in rows)==15
    assert sum(x['body_bytes']==4 for x in rows)==30
    assert [x['entry'] for x in rows if x['body_bytes']==4 and not x['thunk'] and x['C_lines']>11]==['0x101c18384','0x101c183f0','0x101c18550','0x101c18554','0x101f62e5c']
    assert c['alias_pass']==dict(path='/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl',bytes=122340555,lines=420470,sha256='6f05d75085ffb5f74826b4d44f3708fe89466b0b14581e538d912944f8167fcb',nonexternal_rows=418417,passes=1,stat_endpoints_equal=True)


def main():
    raw=(P/'candidate-census.json').read_bytes();assert (len(raw),sha(raw))==(125476,'a8d46906206e5be905d34866467be349734102bc28b1410ffff28ccccf02dfc5')
    sr=(P/'selection-metadata-only.json').read_bytes();assert (len(sr),sha(sr))==(4013,'a495e227f04ce9a119d14e25762b6c4cf614b8862a525147d9bfce33f86b5850')
    c,s=json.loads(raw),json.loads(sr)
    cp=c['retained_parent_aliases_pin'];pr=Path(cp['path']).read_bytes();assert len(pr)==cp['bytes'] and sha(pr)==cp['sha256']
    parent={x['record']['entry']:x for x in map(json.loads,pr.splitlines()) if x['kind']=='alias'}
    validate(c,s,parent)
    negatives=[]
    def reject(name,fn):
        bad=copy.deepcopy(c);fn(bad)
        try:validate(bad,s,parent)
        except (AssertionError,KeyError,ValueError,TypeError,IndexError):negatives.append(dict(name=name,rejected=True));return
        raise AssertionError('negative accepted: '+name)
    reject('drop-selected67-entry',lambda q:q['records'].pop())
    reject('duplicate-selected67-entry',lambda q:q['records'].__setitem__(1,q['records'][0]))
    reject('change-retained-alias',lambda q:q['records'][0]['alias_record'].update(name='other'))
    reject('change-alias-byte-locator',lambda q:q['records'][0]['alias_source'].update(byte=0))
    reject('wrong-chunk-ordinal',lambda q:q['records'][0].update(chunk_number=0))
    reject('negative-source-offset',lambda q:q['records'][0].update(source_byte=-1))
    reject('source-range-beyond-chunk',lambda q:q['records'][0].update(raw_bytes=9999999))
    reject('retain-C-body',lambda q:q['records'][0].update(code='void f(){}'))
    reject('alter-C-size',lambda q:q['records'][0].update(code_utf8_bytes=0))
    reject('erase-warning',lambda q:q['records'][0].update(warnings=[]))
    reject('repair-false-thunk-native-extent',lambda q:q['records'][4].update(body_bytes=4096))
    reject('drop-whole-chunk-pin',lambda q:q['selected_chunk_pins'].pop())
    reject('promote-semantic-read',lambda q:q.update(source_semantics_selected=True))
    reject('promote-source-retention',lambda q:q.update(source_retention_selected=True))
    reject('follow-callee',lambda q:q.update(new_callee_global_slot_native_image_provider_original_model_harness_follow=1))
    reject('claim-missing-is-absence',lambda q:q['summary'].update(missing_is_absence_claim=True))
    reject('second-alias-pass',lambda q:q['alias_pass'].update(passes=2))
    reject('invent-site-grade',lambda q:q.update(new_site_grade_case_release=67))
    reject('close-coverage',lambda q:q.update(coverage_gate='CLOSED'))
    print(json.dumps(dict(status='PASS',metadata_records=67,C_utf8_bytes=29288,C_lines=1231,max_C_lines=145,warning_records=13,warning_occurrences=20,thunks=15,source_chunks=23,original_alias_passes_inherited=1,source_semantic_reads=0,source_retention=0,original_index_chunk_native_image_reads_by_checker=0,negative_count=len(negatives),negative_controls=negatives,coverage_gate='OPEN',required_unsupported='U',source_approval='Separate Root decision required; no retention or C semantics authorized by checker'),indent=2))


if __name__=='__main__':
    main()
