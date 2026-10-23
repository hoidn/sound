"""Check retained packet data only; no original sources or executable calls."""
from pathlib import Path
import copy
import hashlib
import json
import re

P=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((P/n).read_text())
def need(v,why):
    if not v:raise ValueError(why)

def snapshot():
    return dict(census=load('candidate-census.json'),selection=load('selection-source-read.json'),raw=(P/'selected-records.jsonl').read_bytes(),receipt=load('source-retention-receipt.json'),assessment=load('source-assessment.json'),readmap=load('source-read-map.json'))

def verify(x):
    c=x['census'];s=x['selection'];raw=x['raw'];receipt=x['receipt'];a=x['assessment'];rm=x['readmap']
    entries=[r['entry'] for r in c['records']]
    need(len(entries)==len(set(entries))==17 and entries==s['entries'],'whole17 selection')
    lines=raw.splitlines(keepends=True);rows=[json.loads(l) for l in lines]
    need([r['entry'] for r in rows]==entries,'whole17 rawrecords')
    need(len(raw)==receipt['retained']['bytes']==receipt['raw_content_bytes']==44124 and sha(raw)==receipt['retained']['sha256'],'retained raw identity')
    need(receipt['raw_range_reads']==17,'one17range acquisition')
    offset=0
    for r,b,meta,ret in zip(rows,lines,c['records'],receipt['records'],strict=True):
        need(len(b)==meta['raw_bytes']==ret['raw_bytes'] and sha(b)==meta['raw_sha256']==ret['raw_sha256'],'raw record pin')
        code=r['code'];need(isinstance(code,str),'C text');cb=code.encode()
        need(len(cb)==meta['code_utf8_bytes'] and sha(cb)==meta['code_sha256'] and len(code.splitlines())==meta['C_lines'],'C identity')
        need(ret['entry']==r['entry'] and ret['retained_byte']==offset and ret['original_byte']==meta['source_byte'] and ret['original_path']==meta['source_path'],'retention locator')
        need(r['body_bytes']==meta['native_body_bytes'] and r['body_ranges']==meta['native_body_ranges'] and r['thunk']==meta['record_thunk'],'native metadata only')
        need(r['warnings']==meta['warnings']==[] and r['error'] is None and r['partial_code'] is False and r['timed_out'] is False,'export states')
        offset+=len(b)
    need(sum(len(r['code'].encode()) for r in rows)==36647 and sum(len(r['code'].splitlines()) for r in rows)==1239,'complete size')
    need([r['entry'] for r in a['records']]==entries==[r['entry'] for r in rm['records']],'assessment/readmap whole17')
    anchors=refs=0
    for r,obs,read in zip(rows,a['records'],rm['records'],strict=True):
        code=r['code'];cl=code.splitlines();digest=sha(code.encode())
        need(obs['code_sha256']==read['code_sha256']==digest and obs['C_lines']==read['C_lines']==len(cl),'observation identity')
        need(read['fresh_full_line_ranges']==[[1,len(cl)]] and read['lossless_variant_reuse'] is False,'full direct read')
        need(obs['warnings']==r['warnings'] and obs['native_extent_bytes_metadata_only']==r['body_bytes'],'literal metadata')
        need(obs['complete_callable_math_leaf'] is False and obs['complete_callable_X_leaf'] is False and obs['public_route'] is False,'no callable/public promotion')
        for anchor in obs['anchors']:
            lo,hi=anchor['C_lines'];need(1<=lo<=hi<=len(cl),'anchor bounds');text='\n'.join(cl[lo-1:hi]);need(text==anchor['text'] and sha(text.encode())==anchor['sha256'],'anchor quote');anchors+=1
        expected=[]
        for n,line in enumerate(cl,1):
            for m in re.finditer(r'(?<![A-Za-z0-9_])((?:thunk_)?FUN_[0-9a-f]+|_memcpy|NEON_fmov|ABS)\s*\(',line):
                if m[1]!='FUN_'+r['entry'][2:]:expected.append((n,m[1],line))
        actual=obs['lexical_dependencies'];need([(q['C_line'],q['name'],q['text']) for q in actual]==expected,'lexical references exclude declarations')
        need(all(q['text_sha256']==sha(q['text'].encode()) for q in actual),'reference hashes');refs+=len(actual)
    need(anchors==a['summary']['anchors']==52 and refs==a['summary']['lexical_dependency_occurrences']==41,'anchor/reference counts')
    need(a['dependencies']==[dict(entry=o['entry'],**q) for o in a['records'] for q in o['lexical_dependencies']],'whole reference frontier')
    need(a['candidate_math_surfaces']==['0x1047be9c4','0x1047be9ec'],'two bounded math surfaces')
    need(len(a['frontiers'])==6 and all(q['status']=='OPEN' for q in a['frontiers']),'open prerequisites')
    need(a['source_expression_repairs'] is False and a['native_or_original_or_model_execution']==a['new_site_grade_case_release']==0 and a['successor_selected'] is False,'scope/repair/grade boundary')
    need(a['summary']['complete_callable_math_leaves']==a['summary']['complete_callable_X_leaves']==a['summary']['public_routes']==0 and a['required_unsupported']=='U' and a['coverage_gate']=='OPEN','U/OPEN')
    need(len(a['parent_joins'])==8 and sum(len(q['anchors']) for q in a['parent_joins'])==36 and {q['target'] for p in a['parent_joins'] for q in p['anchors']}==set(entries),'complete parent union')
    return dict(records=17,C_bytes=36647,C_lines=1239,anchors=anchors,lexical_references=refs)

def main():
    x=snapshot();stats=verify(x);controls=[]
    mutations=[('drop-source',lambda q:q.update(raw=b''.join(q['raw'].splitlines(keepends=True)[:-1]))),('drop-assessment',lambda q:q['assessment']['records'].pop()),('wrong-code-pin',lambda q:q['assessment']['records'][0].update(code_sha256='0'*64)),('lost-read-range',lambda q:q['readmap']['records'][0].update(fresh_full_line_ranges=[[2,88]])),('lost-warning-metadata',lambda q:q['census']['records'][0].update(warnings=['invented'])),('wrong-anchor',lambda q:q['assessment']['records'][0]['anchors'][0].update(text='changed')),('invent-math-ABI',lambda q:q['assessment']['records'][-1].update(complete_callable_math_leaf=True)),('invent-public',lambda q:q['assessment']['records'][0].update(public_route=True)),('drop-dependency',lambda q:q['assessment']['records'][0]['lexical_dependencies'].pop()),('repair-source',lambda q:q['assessment'].update(source_expression_repairs=True)),('close-frontier',lambda q:q['assessment']['frontiers'][0].update(status='CLOSED')),('invent-grade',lambda q:q['assessment'].update(new_site_grade_case_release=1)),('select-successor',lambda q:q['assessment'].update(successor_selected=True)),('close-coverage',lambda q:q['assessment'].update(coverage_gate='CLOSED')),('drop-parent',lambda q:q['assessment']['parent_joins'].pop()),('wrong-original-locator',lambda q:q['receipt']['records'][0].update(original_byte=0))]
    for name,fn in mutations:
        q=copy.deepcopy(x);fn(q)
        try:verify(q)
        except (ValueError,AssertionError):controls.append(name)
        else:raise AssertionError('accepted '+name)
    print(json.dumps(dict(status='PASS',**stats,negative_count=len(controls),negative_controls=controls,original_index_chunk_native_image_provider_reads=0,original_model_harness_calls=0)))

if __name__=='__main__':main()
