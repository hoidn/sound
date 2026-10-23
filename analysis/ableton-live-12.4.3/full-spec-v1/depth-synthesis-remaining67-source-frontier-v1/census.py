"""Fixed67 metadata census. C strings are measured transiently, never retained or printed."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import sys

P=Path(__file__).resolve().parent
B=P.parent
SELECTION=B/'reviews/synthesis-remaining67-root-metadata-selection.json'
SELECTION_PIN=(4013,'a495e227f04ce9a119d14e25762b6c4cf614b8862a525147d9bfce33f86b5850')
ALIASES=Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl')
ALIAS_PIN=(122340555,'6f05d75085ffb5f74826b4d44f3708fe89466b0b14581e538d912944f8167fcb')
PARENT_ROWS=B/'family-synthesis-instruments-routes-v1/retained-metadata.jsonl'
PARENT_ROWS_PIN=(369263,'5472b3879210ffe72431f08bd12a40b9e1fb06205484c9009decf99cfd710c09')
INPUTS=B/'component-resolution-v1/class-inputs.json'
INPUTS_PIN=(834035,'47b807f450b33ad537eba9cd0e0e8e8346f5f65c973b6011ecef9012326414d0')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def need(v,why):
    if not v:
        raise ValueError(why)


def checked(path, expected):
    b=path.read_bytes()
    need((len(b),sha(b))==expected,'pin mismatch: '+str(path))
    return b


def pin(path,b):
    return dict(path=str(path),bytes=len(b),sha256=sha(b))


def selection_guard(selection,parent,completed):
    entries=selection['entries']
    need(len(entries)==len(set(entries))==67,'all67 unique entries')
    need(len(parent)==len(set(parent))==115 and len(completed)==len(set(completed))==48,'115 and completed48 identities')
    need(entries==sorted(set(parent)-set(completed),key=lambda e:int(e,16)),'complete exact67 difference/order')
    need(not set(entries)&set(completed),'no completed48 replay')
    need(selection['proposed_source_caps']==dict(records=67,C_bytes=2097152,C_lines=50000),'declared source caps')
    need('metadata-only' in selection['decision'] and 'No source retention or semantic C read yet' in selection['limits'],'metadata-only authority')


def measure(record):
    value=record.get('code')
    if value is None:
        value=''
    need(isinstance(value,str),'C must be text or null')
    b=value.encode('utf-8')
    return dict(code_utf8_bytes=len(b),C_lines=len(value.splitlines()),code_sha256=sha(b),code_present=bool(value))


def selfcheck():
    positives=0
    for value,size,lines,present in [('a\nb\n',4,2,True),('\u03bb\n',3,1,True),('',0,0,False),(None,0,0,False)]:
        m=measure(dict(code=value));need((m['code_utf8_bytes'],m['C_lines'],m['code_present'])==(size,lines,present),'measure positive');positives+=1
    parent=[hex(i) for i in range(115)];completed=parent[:48]
    s=dict(entries=parent[48:],proposed_source_caps=dict(records=67,C_bytes=2097152,C_lines=50000),decision='metadata-only',limits='No source retention or semantic C read yet')
    selection_guard(s,parent,completed);positives+=1
    negatives=[]
    for value in [[],{},1,False,b'body']:
        try:measure(dict(code=value))
        except ValueError:negatives.append(dict(name='reject-nontext-'+type(value).__name__,rejected=True))
        else:raise AssertionError('nontext accepted')
    import copy
    mutations=[('drop-seed',lambda q:q['entries'].pop()),('duplicate-seed',lambda q:q['entries'].__setitem__(1,q['entries'][0])),('include-completed48',lambda q:q['entries'].__setitem__(0,completed[0])),('arbitrary-store-only-entry',lambda q:q['entries'].__setitem__(0,'0xffff')),('change-complete-order',lambda q:q['entries'].reverse()),('widen-source-budget',lambda q:q['proposed_source_caps'].update(C_bytes=4194304)),('semantic-read-promotion',lambda q:q.update(limits='Full source read allowed')),('drop-metadata-authority',lambda q:q.update(decision='semantic source'))]
    for name,fn in mutations:
        q=copy.deepcopy(s);fn(q)
        try:selection_guard(q,parent,completed)
        except ValueError:negatives.append(dict(name=name,rejected=True))
        else:raise AssertionError('guard accepted: '+name)
    print(json.dumps(dict(status='PASS',positive_controls=positives,negative_count=len(negatives),negative_controls=negatives,source_index_chunk_native_image_reads=0,original_execution=0),indent=2))


def main():
    need(not (P/'candidate-census.json').exists(),'exclusive census destination')
    need(not (P/'selection-metadata-only.json').exists(),'exclusive selection receipt')
    selection_raw=checked(SELECTION,SELECTION_PIN);selection=json.loads(selection_raw)
    predecessors=[];pre={}
    for k in ['parent_manifest','parent_scope','parent_review','completed48_census','completed48_review']:
        x=selection[k];path=Path(x['path']);b=checked(path,(x['bytes'],x['sha256']));pre[k]=json.loads(b);predecessors.append(pin(path,b))
    selection_guard(selection,pre['parent_scope']['exact_call_seed_entries'],[r['entry'] for r in pre['completed48_census']['records']])
    parent_raw=checked(PARENT_ROWS,PARENT_ROWS_PIN)
    retained=[json.loads(x) for x in parent_raw.splitlines()]
    wanted=set(selection['entries'])
    retained_alias={x['record']['entry']:x for x in retained if x['kind']=='alias' and x['record']['entry'] in wanted}
    need(len(retained_alias)==67,'retained parent67 alias joins')
    input_raw=checked(INPUTS,INPUTS_PIN);inputpins={x['path']:x for x in json.loads(input_raw)['decomp_chunk_pins']}
    # One authorized full aliases pass supplies only exact67 original row/ordinal locators.
    before=ALIASES.stat();digest=hashlib.sha256();offset=ordinal=lines=0;found={}
    with ALIASES.open('rb') as stream:
        for line,raw in enumerate(stream,1):
            digest.update(raw);row=json.loads(raw)
            if row['entry'] in wanted:
                need(row['entry'] not in found,'duplicate exact67 original alias')
                need(row['external'] is False,'selected alias external qualification')
                parent=retained_alias[row['entry']]
                need(row==parent['record'],'parent alias record unchanged')
                need((line,offset,len(raw),sha(raw))==(parent['provider']['line'],parent['provider']['byte'],parent['provider']['bytes'],parent['provider']['sha256']),'parent original alias locator')
                found[row['entry']]=dict(alias_metadata_id=parent['id'],alias_record=row,alias_source=dict(path=str(ALIASES),line=line,byte=offset,bytes=len(raw),sha256=sha(raw)),nonexternal_ordinal=ordinal,chunk_number=ordinal//100)
            if not row['external']:
                ordinal+=1
            offset+=len(raw);lines=line
    after=ALIASES.stat()
    need((before.st_size,before.st_mtime_ns,before.st_ino)==(after.st_size,after.st_mtime_ns,after.st_ino),'alias stream endpoint stat equality')
    need((offset,digest.hexdigest())==ALIAS_PIN and ordinal==418417,'original alias whole-stream custody/ordinal')
    groups=collections.defaultdict(set)
    for entry,v in found.items():groups[v['chunk_number']].add(entry)
    records=[];chunkpins=[];custody=0
    for number,entries in sorted(groups.items()):
        path=Path('/var/tmp/sound-analysis/corpus/decomp/chunks')/f'chunk-{number:05}.jsonl'
        fixed=inputpins[str(path)];b=checked(path,(fixed['bytes'],fixed['sha256']));chunkpins.append(fixed);custody+=len(b);byte=0;seen=set()
        for line,raw in enumerate(b.splitlines(keepends=True),1):
            hit=re.search(br'"entry"\s*:\s*"([^\"]+)"',raw[:100]);entry=hit[1].decode('ascii') if hit else None
            if entry in entries:
                need(entry not in seen,'duplicate exact selected export');seen.add(entry)
                row=json.loads(raw);need(row['entry']==entry,'selected source entry')
                meta=dict(entry=entry,**found[entry],source_path=str(path),source_line=line,source_byte=byte,raw_bytes=len(raw),raw_sha256=sha(raw),export_record_name=row.get('name'),signature=row.get('signature'),**measure(row))
                for k in ['body_bytes','body_ranges','state','warnings','error','timed_out','partial_code','thunk']:
                    meta[k]=row.get(k)
                need('code' not in meta,'C body not retained')
                records.append(meta)
                del row
            byte+=len(raw)
        need(byte==len(b),'complete selected chunk custody')
    records.sort(key=lambda x:int(x['entry'],16));present={x['entry'] for x in records}
    missing_alias=sorted(wanted-set(found),key=lambda x:int(x,16));missing_export=sorted(set(found)-present,key=lambda x:int(x,16))
    C_bytes=sum(x['code_utf8_bytes'] for x in records);C_lines=sum(x['C_lines'] for x in records)
    summary=dict(selected_entries=67,original_aliases_found=len(found),export_records_found=len(records),missing_alias_entries=missing_alias,missing_export_entries=missing_export,missing_is_absence_claim=False,code_utf8_bytes=C_bytes,C_lines=C_lines,max_C_lines=max([x['C_lines'] for x in records],default=0),chunks=len(chunkpins),chunk_custody_bytes=custody,warning_records=sum(bool(x['warnings']) for x in records),warning_occurrences=sum(len(x['warnings'] or []) for x in records),thunk_records=sum(bool(x['thunk']) for x in records),partial_records=sum(bool(x['partial_code']) for x in records),error_records=sum(x['error'] is not None for x in records),timed_out_records=sum(bool(x['timed_out']) for x in records),empty_code_records=sum(not x['code_present'] for x in records),state_counts=dict(collections.Counter(x['state'] for x in records)),within_proposed_whole_source_caps=not missing_alias and not missing_export and len(records)==67 and C_bytes<=2097152 and C_lines<=50000)
    result=dict(schema='fixed67-remaining-synthesis-export-metadata-census-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),selection=pin(SELECTION,selection_raw),predecessor_pins=predecessors,retained_parent_aliases_pin=pin(PARENT_ROWS,parent_raw),class_inputs_pin=pin(INPUTS,input_raw),records=records,summary=summary,selected_chunk_pins=chunkpins,alias_pass=dict(path=str(ALIASES),bytes=offset,lines=lines,sha256=digest.hexdigest(),nonexternal_rows=ordinal,passes=1,stat_endpoints_equal=True),source_reading='METADATA ONLY: transient C strings measured/hashed, never printed/retained/semantically read. All67 selected; no firstN/helper-name exclusion. Missing records are explicit locator gaps, not native absence.',source_caps_proposal=dict(records=67,C_bytes=2097152,C_lines=50000),source_semantics_selected=False,source_retention_selected=False,new_callee_global_slot_native_image_provider_original_model_harness_follow=0,new_site_grade_case_release=0,required_unsupported='U',coverage_gate='OPEN',successor='Separate Root whole-set source-scope approval required; this census selects no retention, semantics or execution.')
    with (P/'selection-metadata-only.json').open('xb') as f:f.write(selection_raw)
    with (P/'candidate-census.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(summary,indent=2))
    print(json.dumps([dict(entry=x['entry'],name=x['alias_record']['name'],C_bytes=x['code_utf8_bytes'],C_lines=x['C_lines'],body_bytes=x['body_bytes'],body_ranges=x['body_ranges'],thunk=x['thunk'],state=x['state'],warnings=x['warnings'],error=x['error'],partial=x['partial_code'],timed_out=x['timed_out']) for x in records],indent=2))


if __name__=='__main__':
    if sys.argv[1:]==['--check']:
        selfcheck()
    elif sys.argv[1:]==['--census']:
        main()
    else:
        raise SystemExit('usage: census.py --check | --census')
