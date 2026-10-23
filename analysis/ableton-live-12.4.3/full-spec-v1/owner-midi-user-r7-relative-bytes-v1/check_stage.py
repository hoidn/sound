#!/usr/bin/env python3
"""Owner mapping/preservation from Root's approved summaries. Actual packet is never reopened."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ACTUAL='analysis/ableton-live-12.4.3/full-spec-v1/batch-midi-user-relative-bytes-v1'
NAMES={1:'AccelSignedBit',2:'AccelBinaryOffset',3:'AccelTwoCompliment',4:'AccelSignedBit2',6:'LinearSignedBit',7:'LinearBinaryOffset',8:'LinearTwoCompliment',9:'LinearSignedBit2'}
OLD={1:{1},2:{65,70},3:{1,8},4:{0,1,7},6:{1,64},7:{0,64,65,127},8:{1,65},9:{1,64}}
def read(path):
    p=Path(path).resolve();assert not p.is_relative_to(ROOT/ACTUAL),'Actual packet read prohibited';return p.read_bytes()
def load(path):return json.loads(read(path))
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def reqs(t):return {m[1]:m[0] for m in re.finditer(r'^### (REQ-MIDI-USER-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',t,re.M|re.S)}
def rows(t):return {m[1]:m[0] for m in re.finditer(r'^\| (MT-\d{2}) \|[^\n]*\n',t,re.M)}
def section(t,h):
    a=t.index(h);b=t.find('\n## ',a+len(h));return t[a:b if b>=0 else len(t)]
def assemble(old,d):
    new=old
    for op in d['operations']:assert new.count(op['old'])==1;new=new.replace(op['old'],op['new'],1)
    return new
def preservation(old,new,before,d):
    assert len(old.encode())==before['owner']['bytes'] and sha(old.encode())==before['owner']['sha256']
    assert len(new.encode())==d['proposed_owner']['bytes'] and sha(new.encode())==d['proposed_owner']['sha256']
    reverse=new
    for op in reversed(d['operations']):assert reverse.count(op['new'])==1;reverse=reverse.replace(op['new'],op['old'],1)
    assert reverse==old
    a,b=reqs(old),reqs(new);assert len(a)==len(b)==13
    for r in before['requirements']:
        v=a[r['id']].encode();assert len(v)==r['bytes'] and sha(v)==r['sha256']
        if r['id']!='REQ-MIDI-USER-005':assert a[r['id']]==b[r['id']]
    assert b['REQ-MIDI-USER-005'].startswith(a['REQ-MIDI-USER-005'])
    assert rows(old)==rows(new) and len(rows(new))==56
    for r in before['MT_rows']:
        v=rows(new)[r['id']].encode();assert len(v)==r['bytes'] and sha(v)==r['sha256']
    for r in before['preserved_sections']:
        v=section(new,r['heading']).encode();assert len(v)==r['bytes'] and sha(v)==r['sha256']
    assert 'portable expected output and comparator are null' in new and 'these calls do not observe UI enum selection' in new
def approved(review,pins):
    assert review['disposition']=='APPROVED_FINITE_1006_FRESH_RELATIVE_BYTE_OBSERVATIONS_AND_18_INHERITED_JOINS'
    assert review['blocking_findings']==review['required_corrections']==[]
    assert review['manifest']==pins['approved_batch_manifest']
    assert review['mode_name_binding']['names']=={str(k):v for k,v in NAMES.items()}
    assert len(review['reviewed_points'])==1024
def mapping(cases,catalog,legacy,binding,review,manifest):
    assert binding['entries']==[{'native_code':k,'mode_name':v} for k,v in NAMES.items()] and binding['new_calls_establish_UI_binding'] is False
    assert len(binding['source_spans'])==2
    for span,expected in zip(binding['source_spans'],([85,87],[100,102])):
        assert span['line_span']==expected
        raw=span['text'].encode();assert len(raw)==span['bytes'] and sha(raw)==span['sha256']
        assert span['source']['sha256'] in review['mode_name_binding']['basis']
        literal=ast.literal_eval(span['text'].split('=',1)[1].strip())
        assert {n:literal[n] for n in NAMES.values()}=={v:k for k,v in NAMES.items()}
    points=review['reviewed_points'];assert [(p['mode'],p['byte']) for p in points]==[(m,v) for m in NAMES for v in range(128)]
    assert len(cases)==1006 and len(catalog)==1024 and len(legacy)==18
    assert [c['id'] for c in cases]==[f'MUR-REL-{i:04d}' for i in range(1,1007)]
    bycase={c['source']['batch_row_id']:c for c in cases};assert len(bycase)==1006;fresh=[]
    for i,(p,cat) in enumerate(zip(points,catalog)):
        m,v=p['mode'],p['byte'];assert p['id']==f'MR{m:02d}-{v:03d}'
        assert cat['mode_name']==NAMES[m] and cat['native_code']==m and cat['byte']==v and cat['batch_row_id']==p['id']
        assert cat['batch_input_pointer']==f'/rows/{i}' and cat['batch_observation_pointer']==f'/{i}'
        assert cat['expected_reference_x86_bits32']==p['bits32'] and cat['provenance']==p['provenance']
        if v in OLD[m]:
            assert p['provenance']=='inherited-X1' and p['actual_child_this_batch'] is None
            assert cat['new_case_id'] is None and cat['historical_reference']==p['historical_locator'] and p['id'] not in bycase
        else:
            assert p['provenance']=='fresh-selected' and cat['new_case_id']==bycase[p['id']]['id'] and cat['historical_reference'] is None
            fresh.append((i,p))
    assert legacy==[r for r in catalog if r['provenance']=='inherited-X1'];next_offset={}
    for c,(i,p) in zip(cases,fresh):
        m,v=p['mode'],p['byte'];j=p['call_index'];ci=list(NAMES).index(m)
        assert c['input']=={'mode_name':NAMES[m],'native_code':m,'data_byte':v,'current_bits32':'3f000000','minimum_bits32':'00000000','maximum_bits32':'3f800000','range_packed_bits64':'3f80000000000000','prior_bits32':'7f7fffff','sensitivity_bits32':'3f800000','quantized':False,'reversed':False,'record_bytes_le':p['input_le16']}
        assert c['requirements']==['REQ-MIDI-USER-005'] and c['kind']=='H' and c['label']=='X'
        assert c['expected_reference_x86']=={'low_XMM0_binary32_hex':p['bits32'],'classification':'finite'}
        assert c['portable_expected'] is None and c['portable_comparator'] is None and c['application_grade']=='unknown' and c['candidate_execution']=='not-run'
        assert c['prior_case_id'] is None and c['prior_reference_observation'] is None
        assert c['precall_oracle']['classification']=='current-REQ005-exact-dyadic-binary32' and c['precall_oracle']['bits32']==p['bits32']
        s=c['source'];assert s['batch_manifest']==manifest and s['batch_row_id']==p['id'] and s['input_pointer']==f'/rows/{i}' and s['observation_pointer']==f'/{i}'
        assert s['return_projection']=='low32 saved XMM0' and s['receipt_pointer']==f'/children/{ci}'
        assert s['call_pointer']==f'/children/{ci}/parsed/calls/{j}' and s['buffer_pointer']==f'/children/{ci}/parsed/buffers/{j-1}'
        # Recorded text reconstruction from approved carriers, not an original computation or raw reopen.
        regs=p['registers_hex'];line=(f'call {j} 0x101bb27b0 '+' '.join(f'{k}={hex(int(regs[k],16))}' for k in ('rax','rdx','xmm0','xmm1'))+'\n').encode()
        raw=s['raw_stdout_call'];assert raw['path']==ACTUAL+f'/attempts/mode-{m}/stdout.txt'
        assert raw['line']==1883+2*j and raw['bytes']==len(line) and raw['sha256']==sha(line) and raw['offset']>=0
        if m in next_offset:assert raw['offset']==next_offset[m]
        b=p['buffer_after'];assert b['index']==j-1 and b['bytes_le']==p['input_le16']
        out=f'out b{b["index"]} {b["address"]} {b["bytes_le"]}\n'.encode();next_offset[m]=raw['offset']+len(line)+len(out)
def main():
    assert sys.argv[1:]==['--check-proposed']
    before=load(HERE/'before-identities.json');delta=load(HERE/'owner-delta.json');old=read(ROOT/'wiki/specs/midi-user-mapping.md').decode();new=assemble(old,delta);preservation(old,new,before,delta)
    pins=load(HERE/'pins.json');pin=pins['actual_review'];b=read(ROOT/pin['path']);assert len(b)==pin['bytes'] and sha(b)==pin['sha256'];review=json.loads(b);approved(review,pins)
    cases=load(HERE/'cases-added.json')['cases'];catalog=load(HERE/'complete-catalog.json')['rows'];legacy=load(HERE/'inherited-references.json')['rows'];binding=load(HERE/'mode-binding.json');mapping(cases,catalog,legacy,binding,review,pins['approved_batch_manifest'])
    raw=read(ROOT/before['release']['cases_file']['path']);assert len(raw)==before['release']['cases_file']['bytes'] and sha(raw)==before['release']['cases_file']['sha256'];released=json.loads(raw)['cases'];assert len(released)==161 and [sha(canonical(c)) for c in released]==before['release']['case_object_sha256']
    mutations=[('drop-fresh-case',lambda c,t,l,b:c.pop()),('duplicate-case-ID',lambda c,t,l,b:c[1].update(id=c[0]['id'])),('swap-enum-table-order',lambda c,t,l,b:b['entries'][1].update(mode_name='AccelTwoCompliment')),('invent-UI-selection-proof',lambda c,t,l,b:b.update(new_calls_establish_UI_binding=True)),('wrong-input-bits',lambda c,t,l,b:c[0]['input'].update(current_bits32='00000000')),('wrong-output-bits',lambda c,t,l,b:c[0]['expected_reference_x86'].update(low_XMM0_binary32_hex='00000000')),('portable-ARM-comparator',lambda c,t,l,b:c[0].update(portable_comparator='exact-bits')),('public-grade-promotion',lambda c,t,l,b:c[0].update(application_grade='pass')),('wrong-observation-pointer',lambda c,t,l,b:c[0]['source'].update(observation_pointer='/1023')),('old-control-new-case',lambda c,t,l,b:l[0].update(new_case_id='MUR-REL-0001')),('omit-logical-byte',lambda c,t,l,b:t.pop()),('repair-prior-case-history',lambda c,t,l,b:c[0].update(prior_case_id='MT-01')),('wrong-raw-lane-lineage',lambda c,t,l,b:c[0]['source']['raw_stdout_call'].update(sha256='0'*64)),('wrong-relative-raw-offset',lambda c,t,l,b:c[1]['source']['raw_stdout_call'].update(offset=0))]
    negatives=[]
    for name,mutate in mutations:
        c,t,l,b=copy.deepcopy((cases,catalog,legacy,binding));mutate(c,t,l,b)
        try:mapping(c,t,l,b,review,pins['approved_batch_manifest'])
        except (AssertionError,IndexError,KeyError):negatives.append(name)
        else:raise AssertionError('negative accepted '+name)
    for name,needle in [('other-REQ-body','A letter-prefixed directory'),('old-MT-row','| MT-01 | S'),('general-S-law','current + (max − min) × d/256'),('precision-exclusions','8τ'),('held-state-history','Only the\ncontrol-surface call')]:
        assert needle in new;changed=new.replace(needle,needle+' ALTERED',1)
        try:preservation(old,changed,before,delta)
        except AssertionError:negatives.append(name)
        else:raise AssertionError('preservation negative accepted '+name)
    blocked=copy.deepcopy(review);blocked['blocking_findings']=['unapproved']
    try:approved(blocked,pins)
    except AssertionError:negatives.append('approval-with-blocker')
    else:raise AssertionError('blocked approval accepted')
    for pin in pins['pins']:
        b=read(ROOT/pin['path']);assert len(b)==pin['bytes'] and sha(b)==pin['sha256']
    assert delta['status']=='FROZEN-PROPOSED-NOT-APPLIED'
    print(json.dumps({'status':'PASS-FROZEN-OWNER-PROPOSAL','new_cases':1006,'logical_catalog':1024,'historical_no_new_ids':18,'other_REQ_bodies_exact':12,'old_MT_rows_exact':56,'released_objects_exact':161,'negative_controls':negatives,'canonical_owner_unchanged':True,'approved_actual_review_sha256':pins['actual_review']['sha256'],'actual_packet_opens':0,'new_original_calls':0,'new_numeric_model_execution':0,'raw_offset_scope':'All1006line hashes/relativeoffsets checked from approvedcarriers/buffers; absolute firsttarget offsets are transcribed authorlocators under approvedbatch citation.'}))
if __name__=='__main__':main()
