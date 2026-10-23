"""Validate finite reviewed-result adoption as DATA; never run old tooling or originals."""
import collections,copy,hashlib,json,pathlib,re,struct
P=pathlib.Path(__file__).resolve().parent
ROOT=next(p for p in P.parents if (p/'wiki/specs/mixer-values.md').exists())
B=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'

def clauses(text):
    return {m.group(1):m.group(2) for m in re.finditer(r'^### (REQ-MIXER-VALUES-\d{3})[^\n]*\n(.*?)(?=^### REQ-|^## |\Z)',text,re.M|re.S)}

def old_case_rows(text):
    return [s for s in text.splitlines() if re.match(r'\| MV-0(?:0[1-9]|[1-3]\d|4[0-8]) \|',s)]

def validate(cases,source,lineage,old,new):
    assert len(source)==301 and sum(x['historical_overlap'] for x in source)==49
    chosen=[(i,r) for i,r in enumerate(source) if r['historical_overlap'] is False]
    assert len(chosen)==252 and len(cases)==252
    ids=[f'MV-{i:03d}' for i in range(49,301)];assert [r['id'] for r in cases]==ids
    functions={r['function']:r['curve'] for r in lineage['groups']}
    for c,(i,r) in zip(cases,chosen):
        assert c['source']['pointer']==f'/{i}' and c['source']['historical_X2_overlap'] is False
        assert c['source']['function_x86']==r['function']
        assert c['input']['curve']==functions[r['function']]
        assert c['input']['position_hex']==r['position_hex']
        assert c['input']['position_binary32_hex']==struct.pack('>f',float.fromhex(r['position_hex'])).hex()
        assert c['expected']=={'level_binary32_hex':r['level_binary32_hex']}
        assert c['requirements']==['REQ-MIXER-VALUES-014'] and c['label']=='X'
        assert c['comparison_scope']=='recorded-x86-helper-and-substituted-Linux-math-only'
        assert c['application_grade']=='unknown' and c['candidate_execution']=='not-run'
    assert collections.Counter(c['input']['curve'] for c in cases)==dict.fromkeys(range(7),36)
    assert len({(c['input']['curve'],c['input']['position_binary32_hex']) for c in cases})==252
    a,z=clauses(old),clauses(new);assert len(a)==len(z)==15
    for k in a:
        if k!='REQ-MIXER-VALUES-014':assert a[k]==z[k],k
    assert z['REQ-MIXER-VALUES-014'].startswith(a['REQ-MIXER-VALUES-014'].rstrip()+'\n')
    assert old_case_rows(old)==old_case_rows(new) and len(old_case_rows(old))==48
    assert 'revision: 6\n' in new and 'MV-049–MV-300' in new
    assert 'supplies no new tolerance for ARM/Apple math' in new
    assert 'not establish a general one-ulp bound' in new
    assert '0xb33bbd2e' in new and '129-point table' in new

def main():
    old=(P/'spec-r5.md').read_text();new=(ROOT/'wiki/specs/mixer-values.md').read_text()
    data=json.loads((P/'cases-added.json').read_text());c=data['cases']
    source=json.loads((B/'batch-mix-leaves-v1/boundary-levels.json').read_text());l=json.loads((B/'reviews/mix-boundary-owner-reconciliation-v2.json').read_text());validate(c,source,l,old,new)
    pins=json.loads((P/'pins.json').read_text())['pins']
    for pin in pins:
        blob=(ROOT/pin['path']).read_bytes();assert len(blob)==pin['bytes'] and hashlib.sha256(blob).hexdigest()==pin['sha256'],pin['path']
    def flip_expected(v):v[0]['expected']['level_binary32_hex']='00000000'
    def clamp(v):
        q=next(r for r in v if r['expected']['level_binary32_hex']=='b33bbd2e');q['expected']['level_binary32_hex']='00000000'
    mutations=[lambda v:v.pop(),lambda v:v.__setitem__(1,copy.deepcopy(v[0])),lambda v:v[0]['source'].__setitem__('historical_X2_overlap',True),lambda v:v[0]['source'].__setitem__('pointer','/0'),lambda v:v[0]['input'].__setitem__('curve',6),lambda v:v[0]['input'].__setitem__('position_binary32_hex','00000000'),flip_expected,clamp,lambda v:v[0].__setitem__('comparison_scope','portable-ARM-one-ulp'),lambda v:v[0].__setitem__('application_grade','pass')]
    rejected=0
    for mutate in mutations:
        v=copy.deepcopy(c);mutate(v)
        try:validate(v,source,l,old,new)
        except AssertionError:rejected+=1
        else:raise AssertionError('false adoption accepted')
    for altered in [new.replace('a new mixer', 'a different mixer',1),new.replace('| MV-001 | 001, 003 |','| MV-001 | 014 |',1)]:
        try:validate(c,source,l,old,altered)
        except AssertionError:rejected+=1
        else:raise AssertionError('predecessor change accepted')
    print(json.dumps({'status':'PASS','new_case_projections':252,'per_curve':36,'old_requirements_exact':14,'old_rows_exact':48,'source_observations_reused':301,'negative_controls_rejected':rejected,'pin_count':len(pins),'original_calls':0,'model_or_comparator_runs':0,'scope':'data projection, preservation and document identities only; approved observations/source semantics inherited, no second result review'}))
if __name__=='__main__':main()
