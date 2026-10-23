#!/usr/bin/env python3
"""Readonly Keyboard R5 source/catalog/history checks and bounded rejection fixtures."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=HERE.parent/'keyboard-navigation-source-audit'

def load(path): return json.loads(Path(path).read_text())
def identity(path):
    raw=Path(path).read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def at(data,pointer):
    for key in pointer.strip('/').split('/') if pointer else []:
        key=key.replace('~1','/').replace('~0','~')
        data=data[int(key)] if isinstance(data,list) else data[key]
    return data

def semantic_guards(reqs,cases,bindings):
    r={x['id']:x for x in reqs};c={x['id']:x for x in cases}
    for row in bindings:
        index=int(row['binding']['json_pointer'][1:])
        assert row['explicit_context_blocks']==(['KN2:B350'] if index>=290 else []),'wrong enabled-use prerequisite association'
        assert all(x['block']!='KN2:B351' for x in [{'block':b} for b in row['explicit_context_blocks']]),'general Shift context cannot be a prerequisite'
        assert any(x['block']=='KN2:B351' and 'not a proved' in x['role'] for x in row['related_context_blocks']),'B351 related-only context lost'
    a=c['NAV-088']['action']
    assert 'Use Tab Key to Move Focus OFF' in a and 'prove ordinary Session/Arrangement switching before hold/release' in a,'Tab latching needs productive OFF view-switch baseline'
    assert 'independently enabled functioning Computer MIDI Keyboard' in c['NAV-090']['action'] and 'sounding-note/range-control baseline' in c['NAV-090']['action'],'range-use baseline lost'
    for x in cases:
        assert x['actual_expected'] is None and x['actual_comparison'] is None,'fabricated actual oracle'
        assert x['exact_target']=='U' and x['execution']=='not-run' and x['complete'] is False,'runtime/closure assertion'
        if int(x['id'][4:])>=43 and x['kind'] in {'numeric','reader','timing','signal','analysis','configuration','edit','initial-context','unresolved'}:
            assert x['expected'] is None and x['documentary_comparison'] is None,'unsupported documentary numeric/reader/timing/signal/etc output'
    for x in reqs: assert x['exact_target']=='U' and x['execution']=='not-run' and x['complete'] is False
    q=r['REQ-KEYBOARD-NAV-U-SOURCE']
    assert q['basis']=='U' and 'Q052 stays open' in q['body'] and 'No preferred dispatch' in q['body'],'Q052 wrongly resolved'
    for cid in ['NAV-094','NAV-095']: assert c[cid]['basis']=='U' and c[cid]['expected'] is None
    assert 'no Arrangement-modulation constructor' in r['REQ-KEYBOARD-NAV-032']['body'],'unproved envelope constructor'
    assert 'general single-letter-plus-Shift' in r['REQ-KEYBOARD-NAV-036']['body'] and 'not a proved modifier' in r['REQ-KEYBOARD-NAV-036']['body'],'forced general Shift rule'
    for cid,words in {'NAV-057':['independently available context menu','first'], 'NAV-064':['independently working','accepted copied content baseline'], 'NAV-079':['genuine working','accepted copied-device content'], 'NAV-085':['working reader feedback/control baseline for each'], 'NAV-094':['genuinely working admitted export-menu dialog baseline'], 'NAV-095':['genuine working previous/next']}.items():
        assert all(w in c[cid]['action'] for w in words),'missing admitted productive baseline: '+cid

def fixtures(reqs,cases,bindings):
    tests=[]
    def reject(name,change):
        rr,cc,bb=copy.deepcopy((reqs,cases,bindings));change(rr,cc,bb)
        try: semantic_guards(rr,cc,bb)
        except AssertionError: tests.append({'fixture':name,'result':'rejected'});return
        raise AssertionError('bad mutation accepted: '+name)
    reject('B350 wrongly applied to MIDI Map toggle',lambda r,c,b:b[0].update(explicit_context_blocks=['KN2:B350']))
    reject('B350 wrongly applied to Key Map toggle',lambda r,c,b:b[1].update(explicit_context_blocks=['KN2:B350']))
    reject('B350 wrongly applied to Computer MIDI toggle',lambda r,c,b:b[2].update(explicit_context_blocks=['KN2:B350']))
    reject('B351 wrongly forced onto range row',lambda r,c,b:b[3].update(explicit_context_blocks=['KN2:B350','KN2:B351']))
    reject('enabled context lost for velocity range',lambda r,c,b:b[4].update(explicit_context_blocks=[]))
    reject('Tab latch lacks explicit OFF',lambda r,c,b:c[87].update(action=c[87]['action'].replace('Use Tab Key to Move Focus OFF','unrecorded mode')))
    reject('numeric chance documentary oracle',lambda r,c,b:c[73].update(expected='exact output 50'))
    reject('reader documentary result',lambda r,c,b:c[84].update(expected='reader announces exact value'))
    reject('latch deadline documentary result',lambda r,c,b:c[87].update(expected='returns after exactly500ms'))
    reject('actual oracle seeded',lambda r,c,b:c[59].update(actual_expected='pass'))
    reject('Q052 resolved by preferred dispatch',lambda r,c,b:r[-1].update(basis='D12'))
    reject('clipboard positive baseline lost',lambda r,c,b:c[78].update(action=c[78]['action'].replace('accepted copied-device content','unknown clipboard')))
    semantic_guards(reqs,cases,bindings)
    tests += [{'fixture':'three toggle contexts remain nonconstructor/unknown','result':'accepted'}, {'fixture':'octave and velocity enabled-use prerequisites retained','result':'accepted'}, {'fixture':'Tab OFF positive baseline plus Settings exception retained','result':'accepted'}]
    return tests

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true',required=True);args=parser.parse_args()
    preservation=load(HERE/'preservation-r4-before-r5.json')
    assert len(preservation['packet_files'])==108
    for rel,pin in preservation['packet_files'].items(): assert identity(HERE/rel)==pin,rel
    for canonical,pin in preservation['canonical_before'].items():
        assert identity(HERE/pin['snapshot'])=={'bytes':pin['bytes'],'sha256':pin['sha256']},canonical
    # Historical R4 manifest is verified against its retained bytes, never current canonical R5.
    r4=load(HERE/'manifest.json');assert len(r4['payloads'])==109
    for pin in r4['payloads']:
        path=ROOT/pin['path']
        if pin['path'] in preservation['canonical_before']:path=HERE/preservation['canonical_before'][pin['path']]['snapshot']
        assert identity(path)=={'bytes':pin['bytes'],'sha256':pin['sha256']},pin['path']
    for file in ['inputs-r5.json','consumer-inputs-r5.json']:
        for pin in load(HERE/file): assert identity(ROOT/pin['path'])=={'bytes':pin['bytes'],'sha256':pin['sha256']},pin['path']
    for source in load(HERE/'sources.json'):
        assert identity(ROOT/source['path'])=={'bytes':source['bytes'],'sha256':source['sha256']}
    # Own static author code only; build returns bytes and cannot write or invoke vendor code.
    module_spec=importlib.util.spec_from_file_location('keyboard_r5_static_author',HERE/'author-r5.py')
    author=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(author)
    outputs=author.build()
    for name,raw in outputs.items():assert (HERE/name).read_bytes()==raw,name
    for canonical,snapshot in [('wiki/specs/keyboard-navigation.md','spec-r5.md'),('wiki/research/keyboard-navigation.md','research-r5.md')]:
        assert (ROOT/canonical).read_bytes()==(HERE/snapshot).read_bytes(),canonical
    reqs=load(HERE/'requirements-r5.json');cases=load(HERE/'cases-r5.json');bindings=load(HERE/'binding-context-r5.json')
    assert len(reqs)==40 and len(cases)==96
    assert len({r['id'] for r in reqs})==40 and len({c['id'] for c in cases})==96
    oldreq=load(HERE/'requirements.json');oldcase=load(HERE/'cases.json');data=load(HERE/'adoption-data-r5.json')
    assert [r['id'] for r in reqs[:21]]==[r['id'] for r in oldreq]
    assert [c['id'] for c in cases[:42]]==[c['id'] for c in oldcase]
    assert sum(a['body']!=b['body'] for a,b in zip(oldreq,reqs))==10
    assert sum(a['action']!=b['action'] for a,b in zip(oldcase,cases))==4
    for old,new in zip(oldreq,reqs):
        for key in ['id','title','basis']:assert old[key]==new[key]
        assert new['body']==data['requirement_body_patches'].get(old['id'],old['body'])
    for old,new in zip(oldcase,cases):
        for key in ['id','requirement','kind','expected','unknown','basis','exact_target','execution']:assert old[key]==new[key],(old['id'],key)
        assert new['action']==data['old_case_action_patches'].get(old['id'],old['action'])
    assert len(load(HERE/'shortcut-bindings.json'))==292
    assert bindings==load(AUDIT/'binding-reconciliation-r2.json')[-5:]
    semantic_guards(reqs,cases,bindings)
    fixture_results=fixtures(reqs,cases,bindings)
    assert fixture_results==load(HERE/'focused-fixtures-r5.json')
    block_catalog=load(AUDIT/'source-blocks.json');assert len(block_catalog)==541
    for row in load(HERE/'source-context-r5.json'):
        b=at(block_catalog,row['json_pointer']);assert b['id']==row['block'] and b['text']==row['quote']
        assert row['literal_element_id']==b['attributes'].get('id')
        assert row['raw_html_sha256']==hashlib.sha256(b['raw_html'].encode()).hexdigest()
        raw=(ROOT/row['source']['path']).read_text()
        assert raw[row['raw_start']:row['raw_end']]==b['raw_html'],row['block']
    for x in reqs+cases:
        for e in x['evidence']:
            b=at(block_catalog,e['json_pointer']);assert b['id']==e['block'] and e['block'] in x['source_blocks']
    groups=load(HERE/'reconciliation-r5.json');assert len(groups)==23
    assert {g['audit_group'] for g in groups}=={g['id'] for g in load(AUDIT/'proposed-deltas.json')}
    for g in groups:
        assert at(load(ROOT/g['audit_proposal']['catalog']),g['audit_proposal']['json_pointer'])['id']==g['audit_group']
        for ref in g['requirement_refs']+g['case_refs']:assert at(load(ROOT/ref['catalog']),ref['json_pointer'])['id']==ref['id']
        assert g['target']=='U' and g['complete'] is False
        for path in g['routed_owners']:assert (ROOT/'wiki/specs'/path).is_file(),path
    # Execute only the four inspected pure Markdown parser definitions, never browser build.
    tool=ast.parse((ROOT/'tools/spec_browser.py').read_text())
    selected=[n for n in tool.body if isinstance(n,ast.FunctionDef) and n.name in {'frontmatter','cells','anchor','spec_rows'}]
    assert len(selected)==4
    env={'re':re};exec(compile(ast.Module(body=selected,type_ignores=[]),'spec_browser.py:pure-definitions','exec'),env)
    browser=env['spec_rows'](ROOT/'wiki/specs/keyboard-navigation.md',(ROOT/'wiki/specs/keyboard-navigation.md').read_text())
    assert {r['id'] for r in browser}=={r['id'] for r in reqs} and len(browser)==40
    impact=load(HERE/'historical-consumer-routing-r5.json')
    assert len(impact['records'])==9 and len({r['consumer'] for r in impact['records']})==8
    for item in impact['records']:
        assert at(load(ROOT/item['consumer']),item['json_pointer'])==item['record']
        assert identity(ROOT/item['exact_historical_snapshot'])==item['snapshot_identity']
    # Check local Markdown paths only; figures/remote destinations remain uninspected.
    for name in ['wiki/specs/keyboard-navigation.md','wiki/research/keyboard-navigation.md']:
        page=ROOT/name
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',page.read_text()):
            if not target.startswith(('https:','http:','#')):
                destination=(page.parent/target.split('#')[0]).resolve()
                assert destination.exists(),(name,target)
                if '#' in target and destination.suffix=='.md':
                    fragment=target.split('#',1)[1]
                    headings=[env['anchor'](h.lstrip('#').strip()) for h in destination.read_text().splitlines() if h.startswith('#')]
                    assert fragment in headings,(name,target,'missing heading')
    sealed=HERE/'manifest-author-r5.json'
    if sealed.exists():
        manifest=load(sealed)
        assert manifest['external_pins']==load(HERE/'inputs-r5.json')+load(HERE/'consumer-inputs-r5.json')
        listed={p['path'] for p in manifest['payloads']}
        actual={p.relative_to(ROOT).as_posix() for p in HERE.rglob('*') if p.is_file() and p!=sealed}
        assert listed==actual,'unexpected/dropped packet files'
        for pin in manifest['payloads']:assert identity(ROOT/pin['path'])=={'bytes':pin['bytes'],'sha256':pin['sha256']},pin['path']
        for pin in manifest['canonicals']:assert identity(ROOT/pin['path'])=={'bytes':pin['bytes'],'sha256':pin['sha256']}
    new_paths=[p for p in HERE.rglob('*') if p.is_file() and p.relative_to(HERE).as_posix() not in preservation['packet_files']]
    for path in new_paths+[ROOT/'wiki/specs/keyboard-navigation.md',ROOT/'wiki/research/keyboard-navigation.md']:
        if 'canonical-before-r5' in path.parts:continue
        if path.suffix in {'.md','.json','.py'}:
            raw=path.read_bytes();assert raw.endswith(b'\n') and b'\r\n' not in raw,path
            assert not any(line.rstrip(b' \t')!=line for line in raw.splitlines()),path
    print(json.dumps({'result':'pass','mode':'readonly','sealed':sealed.exists(),'original_files_preserved':108,'input_pins':33,'consumer_pin_files':8,'requirements':40,'cases':96,'source_blocks_used':len(load(HERE/'source-context-r5.json')),'audit_groups':23,'browser_ids':40,'discovery_rows':292,'actual_oracles_nonnull':0,'complete':0,'rejection_fixtures':12,'positive_fixtures':3}))

if __name__=='__main__':main()
