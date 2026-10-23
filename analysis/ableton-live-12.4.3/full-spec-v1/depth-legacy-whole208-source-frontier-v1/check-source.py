"""Owned read-only source check: owned packet + four immutable minimal parent docs.

No original aliases/chunks/image/provider/native/original/model/harness, no old
collector/checker import or execution. Source reconstruction is text only.
"""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys
P=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
    if not v:raise ValueError(msg)
def jread(name):return json.loads((P/name).read_bytes())
def anchor_ok(a,rows):
    i=a['ordinal'];need(1<=i<=208,'anchor ordinal');r=rows[i-1];lo,hi=a['C_lines'];ls=r['code'].splitlines(keepends=True)
    need(a['entry']==r['entry'] and 1<=lo<=hi<=len(ls),'anchor identity/range')
    need(a['code_sha256']==sha(r['code'].encode()) and a['span_sha256']==sha(''.join(ls[lo-1:hi]).encode()),'anchor exact bytes')

def lexical(rows):
    libs={'_exp','___exp10f','_atanf','___sincosf_stret','_cosf','_tanf','_sin','_powf','_ldexp','operator_new','operator_delete'}
    out=[]
    for i,r in enumerate(rows,1):
        for ln,line in enumerate(r['code'].splitlines(),1):
            if line.lstrip().startswith('/*') or line.lstrip().startswith('* '):continue
            for mt in re.finditer(r'\b[A-Za-z_][A-Za-z_0-9]*\b',line):
                t=mt.group();kind=None
                if re.fullmatch(r'(?:thunk_)?FUN_[0-9a-fA-F]+',t):kind='unfollowed-named-helper-token'
                elif re.fullmatch(r'_?(?:DAT|UNK)_[0-9a-fA-F]+',t) or re.fullmatch(r'PTR_[A-Za-z0-9_]+_[0-9a-fA-F]+',t):kind='unread-global-or-pointer-token'
                elif t in libs:kind='library-or-allocation-token'
                elif t.startswith('NEON_') or re.fullmatch(r'(?:CONCAT|SUB|ZEXT)[0-9]+',t) or t in {'ABS','SQRT'}:kind='decompiler-operator-token'
                if kind:out.append(dict(ordinal=i,entry=r['entry'],C_line=ln,column=mt.start()+1,token=t,kind=kind,line_sha256=sha(line.encode()),followed=False,native_site_credit=False))
            if re.search(r'\(\s*code\s*\*\*\s*\)',line):out.append(dict(ordinal=i,entry=r['entry'],C_line=ln,column=1,token='indirect-expression-line',kind='unbound-indirect-expression-line',line_sha256=sha(line.encode()),followed=False,native_site_credit=False))
    return out

def validate(rows,census,receipt,readmap,assess,deps,whole,readreceipt,named):
    meta=census['records'];need(len(rows)==len(meta)==len(receipt['records'])==len(readmap['records'])==len(assess['records'])==208,'whole208 no drop')
    entries=[r['entry'] for r in rows];need(entries==[r['entry'] for r in meta]==sorted(set(entries),key=lambda x:int(x,16)),'exact208 order')
    need(entries==sorted([r['entry'] for r in named['entries'] if r['selected_outgoing_seed']],key=lambda x:int(x,16)) and len(named['entries'])==208,'all approved mapseeds')
    need(sum(len(r['code'].encode()) for r in rows)==666796 and sum(len(r['code'].splitlines()) for r in rows)==15298,'whole C sizes')
    offset=0;explicit=shared=lossless=0
    for i,(r,cm,rr,rm,ar) in enumerate(zip(rows,meta,receipt['records'],readmap['records'],assess['records']),1):
        code=r['code'];cl=code.splitlines(keepends=True)
        need(sha(code.encode())==cm['code_sha256'] and len(code.encode())==cm['code_utf8_bytes'] and len(cl)==cm['C_lines'],'all full C hashes/lines')
        need(r.get('name')==cm['export_record_name'] and r.get('signature')==cm['signature'],'exportname/signature')
        for key in ['warnings','body_bytes','body_ranges','thunk','state','error','partial_code','timed_out']:need(r.get(key)==cm[key],'all export metadata preserved '+key)
        need(all(w in code for w in r['warnings']),'all literal warnings in C')
        need(rr==dict(entry=r['entry'],retained_byte=offset,raw_bytes=cm['raw_bytes'],raw_sha256=cm['raw_sha256'],original_path=cm['source_path'],original_line=cm['source_line'],original_byte=cm['source_byte']),'original/retained exact locators')
        offset+=cm['raw_bytes']
        need(rm['ordinal']==i and rm['entry']==r['entry'] and rm['total_lines']==len(cl),'readmap record')
        if rm['base_ordinal'] is None:
            need(rm['method']=='whole-body-direct' and rm['pieces']==[] and rm['explicit_lines']==len(cl) and rm['shared_lines']==0,'whole direct')
        else:
            lossless+=1;baseord=rm['base_ordinal'];need(1<=baseord<i and rm['method']=='lossless-prior-base-and-all-differences','prior acyclic base')
            base=rows[baseord-1]['code'].splitlines(keepends=True);aend=bend=0;built=[];reuse=0;changed=0
            for piece in rm['pieces']:
                a,b=piece['base_range'];c,d=piece['target_range'];tag=piece['op']
                need(a==aend and c==bend and 0<=a<=b<=len(base) and 0<=c<=d<=len(cl),'two sided complete partition')
                bs=''.join(base[a:b]);ts=''.join(cl[c:d]);need(sha(bs.encode())==piece['base_sha256'] and sha(ts.encode())==piece['target_sha256'],'all span hashes')
                if tag=='equal':need(b-a==d-c and bs==ts and b>a,'exact equality');built.extend(base[a:b]);reuse+=d-c
                else:
                    need(tag in ['insert','delete','replace'],'known delta op')
                    need((tag!='insert' or a==b) and (tag!='delete' or c==d) and (tag!='replace' or (a<b and c<d)),'opcode shape')
                    built.extend(cl[c:d]);changed+=d-c
                aend=b;bend=d
            need(aend==len(base) and bend==len(cl) and ''.join(built)==code,'lossless entire reconstruction')
            need(rm['shared_lines']==reuse and rm['explicit_lines']==changed,'lossless counts')
        explicit+=rm['explicit_lines'];shared+=rm['shared_lines']
        need(ar['ordinal']==i and ar['entry']==r['entry'] and ar['name']==r['name'],'perrecord assessment identity')
        anchor_ok(ar['whole_source_anchor'],rows)
        need(ar['source_bytes']==cm['code_utf8_bytes'] and ar['C_lines']==cm['C_lines'] and ar['native_extent_metadata']==r['body_bytes'] and ar['warnings']==r['warnings'] and ar['thunk_metadata']==r['thunk'],'assessment metadata')
        need(ar['read_method']==rm['method'] and ar['base_ordinal']==rm['base_ordinal'],'read method join')
        need(ar['callability']=='NOTREADY' and ar['public_route']=='UNKNOWN' and ar['ready_batch'] is ar['complete_callable_math_X'] is False,'perrecord no promotion')
        need(all(ar[k] for k in ['observed_source_projection','legal_inputs','memory','native_ABI_FP']),'perrecord substantive fields')
    need((lossless,explicit,shared)==(57,9710,5588) and readmap['total_lines']==15298 and readmap['explicit_lines']==9710 and readmap['shared_lines']==5588,'whole read counts')
    need(receipt['raw_range_reads']==208 and receipt['raw_content_bytes']==offset==792807 and receipt['retained_sha256']=='4ebc695640d4e901b2a964c2f72b56b76fa6def8bfe7c3f4cb6f8d9ca5389876' and receipt['source_expansion'] is False and receipt['original_calls']==0,'retention limits')
    need(sum(bool(r['warnings']) for r in rows)==6 and sum(len(r['warnings']) for r in rows)==10 and sum(r['thunk'] for r in rows)==0 and sum(r['body_bytes']==4 for r in rows)==76,'warnings/extent flags')
    need(all(len(r['code'].splitlines())>=47 for r in rows if r['body_bytes']==4),'expanded4B preserved')
    lex=lexical(rows);need(deps['records']==lex and len(lex)==1466,'all declared lexical occurrences/order')
    need(deps['summary']==dict(occurrences=1466,kinds=dict(collections.Counter(d['kind'] for d in lex)),followed=0,native_sites=0),'lexical limits')
    for i,ar in enumerate(assess['records'],1):need(ar['source_lexical_navigation_occurrences']==sum(d['ordinal']==i for d in lex),'perrecord lexical count')
    for doc in [assess,whole]:need(doc['required_unsupported']=='U' and doc['coverage_gate']=='OPEN' and doc['status']=='AUTHOR-PROPOSAL-PENDING-ROOT-SEAL-INDEPENDENT-REVIEW','document status scope')
    need(assess['summary']==dict(records=208,C_bytes=666796,C_lines=15298,warning_occurrences=10,four_byte_extents=76,NOTREADY_records=208,ready_batch=0,complete_callable_math_X=0,new_public_routes=0,new_site_grade_case_release=0),'no record credit')
    need([q['id'] for q in whole['whole_source_claims']]==[f'L208-C{i:02}' for i in range(1,13)],'all12claims')
    for q in whole['whole_source_claims']:
        need(q['status']=='OBSERVED-SOURCE-PROJECTION-ONLY' and q['limits'] and q['anchors'] and q['public_route'] is q['complete_callable_math_X'] is q['ready_batch'] is False and q['native_site_credit']==0,'source claims conditional')
        for a in q['anchors']:anchor_ok(a,rows)
    need([q['id'] for q in whole['open_frontiers']]==[f'L208-F{i:02}' for i in range(1,9)],'all8frontiers')
    for q in whole['open_frontiers']:
        need(q['status']=='UNKNOWN' and q['unknown'] and q['closure'] is q['next_selection'] is False,'frontiers stay open')
        for a in q['anchors']:anchor_ok(a,rows)
    need([q['id'] for q in whole['math_and_callable_prospects']]==[f'L208-P{i:02}' for i in range(1,13)],'all12prospects')
    for q in whole['math_and_callable_prospects']:
        need(q['status']=='NOTREADY' and q['ready_batch'] is q['complete_callable_math_X'] is False and q['original_calls']==0 and q['admission_gaps'],'notready prospects')
        need(all(q[k]=='UNKNOWN' for k in ['legal_inputs','memory_model','native_executable_counterpart','ABI','FP_semantics','independent_original_oracle','public_route']),'every admission gate unknown')
        need(q['ordinals']==[a['ordinal'] for a in q['anchors']],'complete prospect source set')
        for a in q['anchors']:anchor_ok(a,rows)
    need(whole['inventory']==dict(whole_clauses=77,atomic_denominator=False,file_only_S=8,application_none=69,application_S=0,X=0,annotations_same77=dict(D11=45,Dpkg=8,U=24),actual_U=194,ready_batch=0,new_site_grade_owner_case_release=0),'inherited unchanged inventory')
    need(whole['successor']=='No automatic successor; Root owns seal/review/adoption and separately selects any future evidence route.','no successor')
    need((readreceipt['records'],readreceipt['C_bytes'],readreceipt['C_lines'],readreceipt['direct_bodies'],readreceipt['lossless_bodies'],readreceipt['explicit_lines'],readreceipt['exact_shared_lines'])==(208,666796,15298,151,57,9710,5588),'author read accounting')
    need([q['index'] for q in readreceipt['display_chunks']]==list(range(35)) and all(q['read_complete'] and not q['truncated'] for q in readreceipt['display_chunks']),'complete author display receipt')
    need(readreceipt['original_model_harness_calls']==readreceipt['native_site_grade_case_release']==0 and readreceipt['coverage_gate']=='OPEN','read scope')
    # Concrete source spellings are not silently repaired into ideal formulas.
    for i,text in [(30,'param_2 * param_2 * param_2 * 100.0 + 0.5'),(107,'(float)(uVar1 & 0x7fffff | 0x3f800000)'),(166,'_powf(fVar1 * param_2,0x40800000)'),(188,'_ldexp(0x3ff0000000000000'),(200,'return true;'),(204,'operator_new(0x10)'),(206,'auStack_58 [56]')]:need(text in rows[i-1]['code'],'literal source qualification')

def main():
    need(sys.argv[1:]==['--check'],'data-only --check only')
    pins=jread('pins-source.json')
    for q in pins['pins']:
        path=Path(q['path']);path=path if q.get('parent_document') else P/path
        b=path.read_bytes();need((len(b),sha(b))==(q['bytes'],q['sha256']),'fixed pin '+str(path))
    gate=jread('selection-source-read.json')
    for q in gate['metadata8']:
        b=(P/Path(q['path']).name).read_bytes();need((len(b),sha(b))==(q['bytes'],q['sha256']),'all metadata8 unchanged')
    need(gate['caps']==dict(records=208,C_bytes=2097152,C_lines=50000),'whole source cap')
    raw=(P/'selected-records.jsonl').read_bytes();need((len(raw),sha(raw))==(792807,'4ebc695640d4e901b2a964c2f72b56b76fa6def8bfe7c3f4cb6f8d9ca5389876'),'exact raw208')
    rows=[];c=jread('candidate-census.json')
    for rb,cm in zip(raw.splitlines(keepends=True),c['records']):need((len(rb),sha(rb))==(cm['raw_bytes'],cm['raw_sha256']),'raw row identity');rows.append(json.loads(rb))
    args=[rows,c,jread('source-retention-receipt.json'),jread('lossless-read-map.json'),jread('source-assessment.json'),jread('source-dependencies.json'),jread('whole-set-assessment.json'),jread('source-read-receipt.json')]
    selection=jread('selection-metadata-only.json');q=selection['parent_seeds'];b=Path(q['path']).read_bytes();need((len(b),sha(b))==(q['bytes'],q['sha256']),'parent seeds')
    named=json.loads(b);args.append(named);validate(*args)
    negatives=[]
    def reject(name,change):
        bad=copy.deepcopy(args);change(bad)
        try:validate(*bad)
        except (ValueError,KeyError,IndexError,TypeError):negatives.append(dict(name=name,rejected=True));return
        raise AssertionError('mutation accepted '+name)
    loss=next(i for i,q in enumerate(args[3]['records']) if q['base_ordinal'])
    eq=next(i for i,q in enumerate(args[3]['records'][loss]['pieces']) if q['op']=='equal')
    reject('drop-whole-record',lambda q:q[0].pop())
    reject('duplicate-record',lambda q:q[0].__setitem__(1,q[0][0]))
    reject('alter-C-literal',lambda q:q[0][29].update(code=q[0][29]['code'].replace('100.0','101.0')))
    reject('drop-warning',lambda q:q[0][0].update(warnings=[]))
    reject('repair-native4B',lambda q:q[0][35].update(body_bytes=400))
    reject('repair-thunk',lambda q:q[0][35].update(thunk=True))
    reject('change-signature',lambda q:q[0][0].update(signature='other'))
    reject('retained-offset-corrupt',lambda q:q[2]['records'][0].update(retained_byte=1))
    reject('original-range-corrupt',lambda q:q[2]['records'][0].update(original_byte=0))
    reject('source-read-replay',lambda q:q[2].update(raw_range_reads=209))
    reject('future-base-cycle',lambda q:q[3]['records'][loss].update(base_ordinal=208))
    reject('drop-delta-piece',lambda q:q[3]['records'][loss]['pieces'].pop())
    reject('false-equal-range',lambda q:q[3]['records'][loss]['pieces'][eq]['target_range'].__setitem__(1,999))
    reject('rewrite-shared-hash',lambda q:q[3]['records'][loss]['pieces'][eq].update(base_sha256='0'*64))
    reject('representative-only-read',lambda q:q[3]['records'][loss].update(explicit_lines=0))
    reject('drop-whole-assessment',lambda q:q[4]['records'].pop())
    reject('false-source-anchor',lambda q:q[4]['records'][0]['whole_source_anchor']['C_lines'].__setitem__(0,0))
    reject('invent-public-route',lambda q:q[4]['records'][29].update(public_route='S'))
    reject('cube-as-readyX',lambda q:q[4]['records'][29].update(complete_callable_math_X=True,ready_batch=True))
    reject('drop-lexical-reference',lambda q:q[5]['records'].pop())
    reject('dependency-to-native-site',lambda q:q[5]['records'][0].update(native_site_credit=True))
    reject('follow-encountered-helper',lambda q:q[5]['records'][0].update(followed=True))
    reject('drop-whole-claim',lambda q:q[6]['whole_source_claims'].pop())
    reject('sourceclaim-to-public',lambda q:q[6]['whole_source_claims'][0].update(public_route=True))
    reject('sourceclaim-to-runtime-equivalence',lambda q:q[6]['whole_source_claims'][0].update(status='RUNTIME-PROVED'))
    reject('drop-OPEN-frontier',lambda q:q[6]['open_frontiers'].pop())
    reject('close-frontier',lambda q:q[6]['open_frontiers'][0].update(closure=True,status='CLOSED'))
    reject('drop-NOTREADY-prospect',lambda q:q[6]['math_and_callable_prospects'].pop())
    reject('invent-legal-object-model',lambda q:q[6]['math_and_callable_prospects'][0].update(memory_model='ADMITTED'))
    reject('invent-original-oracle',lambda q:q[6]['math_and_callable_prospects'][0].update(independent_original_oracle='PASS'))
    reject('promote-batch',lambda q:q[6]['math_and_callable_prospects'][0].update(ready_batch=True))
    reject('count-source-as-extra-outcomes',lambda q:q[6]['inventory'].update(whole_clauses=285))
    reject('grade-U',lambda q:q[6]['inventory'].update(actual_U=0))
    reject('close-coverage',lambda q:q[6].update(coverage_gate='CLOSED'))
    reject('invent-successor',lambda q:q[6].update(successor='execute now'))
    reject('hide-display-truncation',lambda q:q[7]['display_chunks'][0].update(truncated=True))
    reject('omit-display',lambda q:q[7]['display_chunks'].pop())
    print(json.dumps(dict(status='PASS-data-only-owned-source-integrity',whole_records=208,C_bytes=666796,C_lines=15298,raw_bytes=792807,warnings=10,warned_records=6,four_byte_extents=76,lossless_bodies=57,direct_bodies=151,explicit_lines=9710,shared_lines=5588,lexical_occurrences=1466,whole_claims=12,unknown_frontiers=8,NOTREADY_prospects=12,NOTREADY_records=208,negative_count=len(negatives),negative_controls=negatives,metadata8_unchanged=True,parent_documents=4,original_alias_chunk_native_image_provider_model_harness_reads_or_calls=0,application_S_X=0,ready_batches=0,new_site_grade_owner_case_release=0,coverage_gate='OPEN',scope='Mechanical source integrity and admission guards only; not semantic review or native/runtime equivalence',writes=False),indent=2))
if __name__=='__main__':main()
