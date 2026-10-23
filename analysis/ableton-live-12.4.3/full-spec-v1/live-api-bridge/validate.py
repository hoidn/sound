"""Read-only analyst source/scope integrity; no API/Max/patch/example execution."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import hashlib
import json
import re
import runpy
import subprocess
import sys

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
ORIGIN=P.parent/'max-api'
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows


def load(path):
    return json.loads(path.read_text())


def pin(path, record):
    raw=path.read_bytes()
    assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'],path
    return raw


inventory_pins=load(P/'inventory-pins.json')
assert len(inventory_pins)==5
for record in inventory_pins:
    pin(Path(record['path']),record)
original_manifest=ORIGIN/'manifest-inventory-r1.json'
assert hashlib.sha256(original_manifest.read_bytes()).hexdigest()=='67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73'
inventory=load(original_manifest)
assert len(inventory['files'])==65
for name,record in inventory['files'].items():
    pin(ORIGIN/name,record)
assert inventory['summary']['index_declares_live_version']=='12.4.5'
source_index={r['id']:r for r in load(ORIGIN/'all-sources-r1.json')}
original_blocks=load(ORIGIN/'reference-blocks.json')
sources=load(P/'sources.json')
assert [s['alias'] for s in sources]==['OV','PATH','OBJ','OBS','REM','INIT','JS']
assert len(sources)==len({s['id'] for s in sources})==7
extract=runpy.run_path(str(ORIGIN/'derive_inventory.py'))['extract']
blocks=load(P/'source-blocks.json')
locators={}
for source,count in zip(sources,[126,130,170,141,101,83,142]):
    assert {k:v for k,v in source.items() if k not in ('alias','retained_path')}==source_index[source['id']]
    assert source['retained_path']=='../max-api/'+source['file']
    assert datetime.fromisoformat(source['capture_utc']).utcoffset().total_seconds()==0
    raw=pin(P/source['retained_path'],source)
    assert extract(raw.decode())==original_blocks[source['id']]==blocks[source['alias']]
    assert len(blocks[source['alias']])==count
    for row in blocks[source['alias']]:
        locators[source['alias']+':'+row['block']]=row
assert len(locators)==893
assert (P/'source-blocks.txt').read_text()==''.join(f"{alias}:{r['block']} HTML:{r['html_line']}:{r['html_column']} {r['tag']} {r['text']}".rstrip()+'\n' for alias,rows in blocks.items() for r in rows)
assert locators['PATH:B0062']['text']=='TEXT_HERE'
assert 'Persistent Mapping' in locators['OBJ:B0153']['text']
owner_pins=load(P/'owner-pins.json')
assert len(owner_pins)==17
for record in owner_pins:
    pin(Path(record['path']),record)

rs,cs,counts=[load(P/f'{n}.json') for n in ['requirements','cases','counts']]
reqmap={r['id']:r for r in rs}
assert len(rs)==len(reqmap)==52
assert Counter(r['provenance'] for r in rs)=={'D-current-public':44,'U':8}
assert len(cs)==len({c['id'] for c in cs})==61
assert {rid for c in cs for rid in c['requirements']}==set(reqmap)
for r in rs:
    assert r['target_applicability']=='U' and r['contract']
    assert all(ref in locators for ref in r['source_blocks'])
    assert bool(r['source_blocks'])==(r['provenance']=='D-current-public')
for c in cs:
    assert len(c['requirements'])==1 and c['setup_and_action']
    r=reqmap[c['requirements'][0]]
    assert c['source_blocks']==r['source_blocks']
    assert c['preconditions']==['common','active-positive-guard']
    assert c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
    assert c['source_claim']==(r['contract'] if r['provenance']=='D-current-public' else None)
    if c['kind']=='control':
        assert c['title']=='Persistent Mapping Inspector option'
        assert c['documentary_expected'].startswith('The named Use Persistent Mapping Inspector option is offered')
        assert 'no ID, persistence, message, timing or runtime equivalence oracle' in c['documentary_comparator']
    else:
        assert c['documentary_expected'] is None and c['documentary_comparator'] is None
calculated=dict(requirements=len(rs),requirement_grades=dict(Counter(r['provenance'] for r in rs)),cases=len(cs),case_kinds=dict(Counter(c['kind'] for c in cs)),documentary_oracles=sum(c['documentary_expected'] is not None for c in cs),null_documentary_oracles=sum(c['documentary_expected'] is None for c in cs),retained_sources=7,retained_blocks=893,target_oracles=0)
assert calculated==counts and counts['documentary_oracles']==1 and counts['null_documentary_oracles']==60
assert {'message-role','notification','signal','source-context','persistence','boundary','malformed','negative','sample-rate','automation','undo','cancel','concurrency','source-loss','recovery','teardown'}<={c['kind'] for c in cs}
fixtures=load(P/'fixtures.json')
assert all(name in fixtures for name in ['common','F-PATH','F-OBJECT','F-IDENTITY','F-MUTATE','F-OBSERVE','F-REMOTE','F-AUTO','F-INIT','F-JS','F-PERSIST','active-positive-guard','not_provided'])
assert all(phrase in fixtures['active-positive-guard'] for phrase in ['independently valid owned patch','available initialized Live/Max/API context','nonzero','matched positive baseline','cannot prove no-effect'])

specpath=ROOT/'wiki/specs/live-api-bridge-workflows.md'
researchpath=ROOT/'wiki/research/live-api-bridge-workflows.md'
spec=specpath.read_text()
headings=re.findall(r'^### (REQ-LAPI-BRIDGE-[A-Z0-9-]+) — (.+)$',spec,re.M)
assert len(headings)==52 and {h[0] for h in headings}==set(reqmap)
for r in rs:
    assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
for c in cs:
    assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |" in spec
browser=spec_rows(specpath,spec)
assert len(browser)==52 and {r['id'] for r in browser}==set(reqmap)
assert '12.4.5' in spec and 'REQ013' in spec and 'candidate threading' in spec
assert all(f'Q-LAB-{n:03d}' in researchpath.read_text() for n in range(1,8))


def slug(text):
    return re.sub(r'[^\w\- ]','',re.sub(r'[`*]|<[^>]*>','',text).strip().lower()).replace(' ','-')


links=0
for canonical,snapshot in [(specpath,'spec-r1.md'),(researchpath,'research-r1.md')]:
    assert canonical.read_bytes()==(P/snapshot).read_bytes()
    text=canonical.read_text()
    match=re.match(r'---\n(.*?)\n---\n',text,re.S)
    assert match
    meta=dict(line.split(': ',1) for line in match.group(1).splitlines() if ': ' in line)
    assert {'id','type','status','updated','access','revision','target'}<=meta.keys()
    assert meta['access']=='analysis' and meta['revision']=='1'
    for dest in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',text):
        if re.match(r'[A-Za-z]+:',dest):continue
        name,_,fragment=dest.partition('#')
        path=(canonical.parent/name).resolve() if name else canonical
        if path==P/'manifest-author-r1.json' and not path.exists():continue
        assert path.exists(),(canonical,dest)
        if fragment and path.suffix=='.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$',path.read_text(),re.M)},dest
        links+=1
for path in [specpath,researchpath]+[f for f in P.rglob('*') if f.is_file() and f.suffix in ('.py','.json','.md','.txt')]:
    if path.suffix=='.json':load(path)
    result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True,text=True)
    assert result.returncode in (0,1) and not result.stdout and not result.stderr,(path,result.stdout,result.stderr)
manifest_path=P/'manifest-author-r1.json'
if manifest_path.exists():
    manifest=load(manifest_path)
    assert manifest['counts']==counts
    assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}==set(manifest['files'])|{'manifest-author-r1.json'}
    for name,record in manifest['files'].items():pin(P/name,record)
    assert manifest['canonical_snapshots']=={'spec-r1.md':'wiki/specs/live-api-bridge-workflows.md','research-r1.md':'wiki/research/live-api-bridge-workflows.md'}
print(json.dumps(dict(status='pass',scope='Analyst documentary/source integrity only; no API/Max/runtime',**counts,inventory_R1_payload_pins=65,inventory_identity_pins=5,owner_pins=17,canonical_snapshot_pairs=2,browser_ID_equality=52,local_links_and_anchors=links,sealed_manifest_checked=manifest_path.exists(),all_target_expected_comparison_null_U_unexecuted=True,writes=False,API_or_patch_execution=False,original_execution=False,candidate_execution=False),indent=2))
