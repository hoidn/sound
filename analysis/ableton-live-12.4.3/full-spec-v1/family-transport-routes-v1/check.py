#!/usr/bin/env python3
"""Read-only transport route/data/identity checks. Never imports old tools/code."""
from pathlib import Path
import copy, hashlib, json, re, sys, collections
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def sha(b): return hashlib.sha256(b).hexdigest()
def load(n): return json.loads((P/n).read_text())
def ptr(value,path):
    for key in path.split('/')[1:]:
        key=key.replace('~1','/').replace('~0','~')
        value=value[int(key)] if isinstance(value,list) else value[key]
    return value

def validate(ledger,inputs,locators,providers):
    rows=ledger['outcomes']; assert len(rows)==len({r['id'] for r in rows})
    assert ledger['summary']['new_ids']==ledger['summary']['new_cases']==ledger['summary']['new_grades']==0
    assert ledger['integration_manifest_sha256']=='7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83'
    assert set(r for x in rows for r in x['requirements'])=={'REQ-TRANSPORT-STATE-'+str(i).zfill(3) for i in range(1,13)}
    allowed={'X','S','no-established-route'}
    currentcases=json.loads((ROOT/providers['release-cases']['path']).read_text())['cases']
    ids={r['id'] for r in currentcases}; canonical_unknown={'TS-017','TS-018','TS-019'}
    for r in rows:
        assert r['route'] in allowed and r['new_expected'] is None and r['new_actual'] is None
        assert r['new_grade']=='U / no new grade; owner and case labels unchanged'
        assert r['context_and_premises'] and r['missing_join_or_enumeration_gap']
        assert set(r['existing_cases'])<=ids|canonical_unknown
        assert all(k in inputs['sets'] for k in r['input_sets'])
        assert all(k in locators['locators'] for k in r['evidence_refs'])
        assert {s['requirement'] for s in r['source_spans']}==set(r['requirements'])
        if r['route']=='X': assert r['input_sets'] and all(inputs['sets'][k].get('provider','').startswith('x2-') for k in r['input_sets'])
        for s in r['source_spans']:
            assert s['provider']=='owner'
            data=(ROOT/providers['owner']['path']).read_bytes()[s['byte_start']:s['byte_start']+s['bytes']]
            assert len(data)==s['bytes'] and sha(data)==s['sha256']
            assert s['requirement'].encode() in data
    assert ids<=set(c for r in rows for c in r['existing_cases'])
    assert len(rows)==ledger['summary']['rows']
    assert dict(collections.Counter(r['route'] for r in rows))==ledger['summary']['routes']
    for values in locators['locators'].values():
        for s in values:
            provider=providers[s['provider']]; data=(ROOT/provider['path']).read_bytes()
            if 'pointer' in s: ptr(json.loads(data),s['pointer'])
            else: assert sha(data[s['byte_start']:s['byte_start']+s['bytes']])==s['sha256']
    for s in inputs['sets'].values():
        if 'provider' not in s: continue
        data=json.loads((ROOT/providers[s['provider']]['path']).read_text())
        if 'array_pointer' in s:
            arr=ptr(data,s['array_pointer'])
            indices=s['indices'] if isinstance(s['indices'],list) else list(range(len(arr)))
            assert all(0<=i<len(arr) for i in indices)
            assert len(indices)==s.get('record_count',s.get('count',len(indices)))
            assert all(all(field in arr[i] for field in s.get('input_fields',[])) for i in indices)
            if 'distinct_input_count' in s: assert len({(arr[i]['n'],arr[i]['d']) for i in indices})==s['distinct_input_count']
        elif 'pointer' in s: ptr(data,s['pointer'])
    return len(rows)

def main():
    if sys.argv[1:]!=['--check']: print('read-only: only --check is supported',file=sys.stderr); return 1
    providerlist=load('pins.json')['providers']; providers={r['id']:r for r in providerlist}; assert len(providerlist)==len(providers)
    identities=[]
    for r in providerlist:
        b=(ROOT/r['path']).read_bytes(); equal=len(b)==r['bytes'] and sha(b)==r['sha256']
        if r['kind']=='immutable-predecessor-or-evidence': assert equal,r['id']
        identities.append({'id':r['id'],'current_equals_asof':equal,'kind':r['kind']})
    ledger=load('route-ledger.json');inputs=load('input-sets.json');locators=load('evidence-locators.json')
    count=validate(ledger,inputs,locators,providers)
    for e in load('chain-edges.json')['edges']:
        s=e['evidence']; assert s['provider'] in providers
        if 'pointer' in s: ptr(json.loads((ROOT/providers[s['provider']]['path']).read_text()),s['pointer'])
        elif 'locator_key' in s: assert s['locator_key'] in locators['locators']
        else:
            b=(ROOT/providers[s['provider']]['path']).read_bytes();assert sha(b[s['byte_start']:s['byte_start']+s['bytes']])==s['sha256']
    # Complete current partial release: data hashes only, no validator/replay/import.
    releasepath=ROOT/providers['release']['path']; rel=json.loads(releasepath.read_text()); verified=0
    entries=rel['files'].items() if isinstance(rel['files'],dict) else [(r['path'],r) for r in rel['files']]
    for name,r in entries:
        b=(releasepath.parent/name).read_bytes();assert sha(b)==r['sha256'];assert len(b)==r['bytes'];verified+=1
    addition=load('canonical-addition.json');current=(ROOT/addition['path']).read_bytes()
    assert sha(current[:addition['before_bytes']])==addition['before_sha256']
    assert sha(current[addition['before_bytes']:addition['after_bytes']])==addition['added_sha256']
    # Small joint negative controls: source association, grades, inputs and withdrawn cases.
    failures=[]
    def reject(name,mutate):
        bad=copy.deepcopy(ledger);mutate(bad)
        try: validate(bad,inputs,locators,providers)
        except (AssertionError,KeyError,IndexError,ValueError): failures.append(name);return
        raise AssertionError('unsafe fixture accepted: '+name)
    reject('new expected oracle',lambda d:d['outcomes'][0].update(new_expected='pass'))
    reject('grade promotion',lambda d:d['outcomes'][0].update(new_grade='S pass'))
    reject('broken source association',lambda d:d['outcomes'][0]['source_spans'][0].update(byte_start=0))
    reject('duplicate outcome id',lambda d:d['outcomes'][1].update(id=d['outcomes'][0]['id']))
    reject('unknown predicate promoted to X without input route',lambda d:next(r for r in d['outcomes'] if r['id']=='TSR-007-template').update(route='X'))
    reject('wrong predecessor',lambda d:d.update(integration_manifest_sha256='0'*64))
    reject('withdrawn case used as current evidence',lambda d:d['outcomes'][0]['existing_cases'].append('TS-023'))
    reject('unresolved evidence locator',lambda d:d['outcomes'][0]['evidence_refs'].append('missing#not-a-locator'))
    # Scoped links: this contribution, plus its exact appended research section.
    files=[P/'structure.md'];targets=[]
    append=current[addition['before_bytes']:addition['after_bytes']].decode()
    for f,text in [(files[0],files[0].read_text()),(ROOT/addition['path'],append)]:
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in link:continue
            target=link.split('#')[0];dest=f.parent/target;assert dest.exists(),link;targets.append(link)
    report={'status':'PASS bounded structural/data checks only','rows':count,'routes':ledger['summary']['routes'],'requirements':12,'chain_relationships':len(load('chain-edges.json')['edges']),'negative_controls_rejected':failures,'current_release_payloads_hashed':verified,'provider_identity_results':identities,'canonical_change':'exact before-prefix and appended pending-review bytes verified','local_links_resolve':len(targets),'actual_calls':0,'new_grades':0,'scope_limit':'Not semantic approval, exhaustive enumeration, opcode rederivation or execution of any old tool/model/harness/comparator. Mutablewiki identities are asof, not future hashgates.'}
    print(json.dumps(report,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
