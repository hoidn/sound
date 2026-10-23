"""Own draft metadata checks only: no comparator, numerical or original import."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
P = Path(__file__).resolve().parent

def load(n):
    return json.loads((P/n).read_text())

def digest(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def pointer(value, ref):
    for token in ref.lstrip('/').split('/'):
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    return value

def validate(v, sources):
    assert v['required_outcome_denominator'] is None
    assert v['graded_required_outcome_numerator'] is None
    assert v['candidate_conformance'] is None and v['newly_graded_outcomes']==0
    rows=v['outcomes']; ids=[r['id'] for r in rows]
    assert len(ids)==len(set(ids))==96
    assert sum(r['kind']=='fixed-outcome-subset' for r in rows)==5
    assert sum(r['kind']=='unresolved-observation-family' for r in rows)==2
    for r in rows:
        assert r['new_expected'] is r['new_comparison'] is r['candidate_grade'] is None
        assert r['required_scope_grade']==('X-finite' if r['kind']=='fixed-outcome-subset' else 'U')
        assert r['route'] in v['routes'] and r['outcome'] and r['positive_guard']
        for ref in [r['source_ref']]+r.get('cross_owner_refs',[]):
            s=sources[ref['provider']]
            if 'pointer' in ref:s=pointer(json.loads(s),ref['pointer'])
            assert isinstance(s,str)
            assert re.search(r'^### '+re.escape(ref['heading'])+r' — ',s,re.M), ref
    controls=pointer(json.loads(sources['r5_case_inputs']),'/0/evaluation/parameter_order')
    nav=v['control_navigation'];assert len(nav)==38
    assert [(x['host_index'],x['host_name']) for x in nav]==list(enumerate(controls))
    for x in nav:
        assert x['outcome_refs']==[r['id'] for r in rows if x['host_name'] in r['controls'] or 'all38' in r['controls']]
        assert x['outcome_refs']
    assert len(v['open_denominator_obligations'])==6
    assert all(o['required_cardinality'] is None for o in v['open_denominator_obligations'])
    omissions=pointer(json.loads(sources['preflight']),'/omitted_modal_modes')
    assert len(omissions)==14 and sum(o['occurrences'] for o in omissions)==174
    assert v['omission_membership']['historical_occurrences']==174
    assert v['omission_membership']['note72_extra_ungraded']==2
    assert v['next_selection']['outcome']=='CRO-22' and 'model-order' in v['next_selection']['stop_condition']
    assert v['adopted_r6']['application_grade'] is None

def main():
    if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no write, seal, source or numerical execution.')
    p=load('providers.json');paths={Path(r['path']) for r in p['immutable'].values()}
    paths.update(q for q in P.iterdir() if q.is_file())
    before={str(q):digest(q) for q in paths};sources={}
    for k,r in p['immutable'].items():
        q=Path(r['path']);assert digest(q)=={t:r[t] for t in ['bytes','sha256']}
        sources[k]=q.read_text()
    for e in p['policy_asof']:
        assert e['future_live_hash_gate'] is False
        assert hashlib.sha256(e['quote'].encode()).hexdigest()==e['quote_sha256']
    assert p['future_live_hash_gates'] is False
    v=load('outcomes.json');validate(v,sources)
    negatives=[]
    for label,mutation in [
        ('invented-denominator',lambda x:x.update(required_outcome_denominator=96)),
        ('template-promoted-to-X',lambda x:x['outcomes'][5].update(required_scope_grade='X-finite')),
        ('wrong-owner-association',lambda x:x['outcomes'][5]['source_ref'].update(heading='REQ-DEVICE-CORPUS-999')),
        ('old-omission-dropped',lambda x:x['omission_membership'].update(historical_occurrences=173))]:
        bad=copy.deepcopy(v);mutation(bad)
        try:validate(bad,sources)
        except (AssertionError,KeyError,IndexError):negatives.append(label)
        else:raise AssertionError('Unsafe proposal accepted: '+label)
    seal=P/'manifest.json'
    if seal.exists():
        m=load('manifest.json');assert {q.name for q in P.iterdir() if q.is_file() and q!=seal}=={r['path'] for r in m['files']}
        for r in m['files']:assert digest(P/r['path'])=={k:r[k] for k in ['bytes','sha256']}
    for q in P.iterdir():
        if q.is_file():
            t=q.read_text();assert t.endswith('\n') and all(s==s.rstrip() for s in t.splitlines())
    links=0
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(P/'README.md').read_text()):
        assert (P/target).resolve().exists(),target
        links+=1
    assert before=={str(q):digest(q) for q in paths}
    print(json.dumps({'status':'PASS draft navigation/integrity only','sealed':seal.exists(),'proposal_rows':96,'fixed_subsets':5,'open_templates':89,'observation_families':2,'open_continuum_obligations':6,'host_controls_navigation':38,'denominator':None,'newly_graded':0,'candidate_grade':None,'providers':len(p['immutable']),'negative_fixtures':negatives,'readme_links':links,'watched':len(paths),'watch_unchanged':True,'original_calls':0,'numeric_calls':0},indent=2))

if __name__=='__main__':main()
