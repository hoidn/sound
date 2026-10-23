"""Read-only Settings case successor integrity. No author/original/content execution."""
from pathlib import Path
from collections import Counter
import copy
import hashlib
import json
import re
import runpy
import subprocess
import sys

P=Path(__file__).resolve().parent;R=P.parents[3]
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight']
assert not preflight or not (P/'manifest-author-r2.json').exists()
load=lambda p:json.loads(p.read_text())
info=lambda p:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
inputs=load(P/'inputs-r2.json')
watched=list(p for p in P.rglob('*') if p.is_file())+[R/x['path'] for x in inputs]+[R/'wiki/specs/settings-learning-workflows.md',R/'wiki/research/settings-learning-workflows.md']
before={str(p):info(p) for p in watched}
old=load(P/'manifest-author-r1.json')
assert info(P/'manifest-author-r1.json')['sha256']=='0c4d506425f34a330e7f668563c63824be3746407ff00d358f5bf4df5fc4509c'
assert len(old['files'])==13
for name,pin in old['files'].items():assert info(P/name)==pin and (P/name).read_bytes()==(P/'archive-r1'/name).read_bytes()
assert (P/'manifest-author-r1.json').read_bytes()==(P/'archive-r1/manifest-author-r1.json').read_bytes()
assert {x.name for x in (P/'archive-r1').iterdir()}==set(old['files'])|{'manifest-author-r1.json'}
for x in inputs:assert info(R/x['path'])=={k:x[k] for k in ['bytes','sha256']}
source=load(P/'source.json');assert info(P/source['file'])=={k:source[k] for k in ['bytes','sha256']}
dep=load(P/'dependencies.json')[0];assert info(R/dep['path'])=={k:dep[k] for k in ['bytes','sha256']}
parser=runpy.run_path(str(R/dep['path']))['Chapter']();parser.feed((P/source['file']).read_text())
for i,b in enumerate(parser.rows,1):b['id']=f'SET-B{i:03d}'
assert parser.rows==load(P/'source-blocks.json') and len(parser.rows)==70
requirements=load(P/'requirements.json');oldcases=load(P/'cases.json');cases=load(P/'cases-r2.json')
assert len(requirements)==21 and Counter(r['strength'] for r in requirements)=={'D12':19,'U':2}
assert len(cases)==len({c['id'] for c in cases})==31
assert [c['id'] for c in cases[:30]]==[c['id'] for c in oldcases]
for a,b in zip(oldcases,cases):
    assert set(b)-set(a)<={'finite_contexts','refines_R1_case'}
    for k,v in a.items():
        if k not in {'setup_and_action','fixture'}:assert b[k]==v,(a['id'],k)
    if 'refines_R1_case' in b:assert b['refines_R1_case']==a['id']
req={r['id']:r for r in requirements}


def verify_cases(rows):
    assert len(rows)==len({c['id'] for c in rows})==31
    for c in rows:
        assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
        assert c['fixture']=='fixtures-r2.json#SET-OWNED' and c['setup_and_action']
        assert set(c['requirements'])<=set(req)
        if c['kind']=='timing' or c['id'].startswith('SET-U-'):assert c['documentary_expected'] is c['documentary_comparator'] is None
    assert {q for c in rows for q in c['requirements']}==set(req)
    assert sum(c['documentary_expected'] is not None for c in rows)==18
    assert sum(c['id'].startswith('SET-U-') for c in rows)==12
    cm={c['id']:c for c in rows}
    assert cm['SET-004']['finite_contexts']==['play/pause','progress scrubbing','volume','subtitles','picture-in-picture']
    assert len(cm['SET-002']['finite_contexts'])==4
    assert {'Learn View Home Page return','< Lessons return'}<=set(cm['SET-003']['finite_contexts'])
    assert {'grid opacity','brightness','color intensity','hue'}<=set(cm['SET-015']['finite_contexts'])
    assert len(cm['SET-006']['finite_contexts'])==4 and len(cm['SET-017']['finite_contexts'])==5
    assert cm['SET-U-AVAILABILITY']['requirements']==['REQ-SETTINGS-LEARNING-U-LIFECYCLE']


verify_cases(cases)
for mode in ['graded','duplicate','missing-customization']:
    changed=copy.deepcopy(cases)
    if mode=='graded':changed[-1]['expected']='unsupported default'
    elif mode=='duplicate':changed[-1]['id']=changed[0]['id']
    else:next(c for c in changed if c['id']=='SET-015')['finite_contexts'].remove('hue')
    try:verify_cases(changed)
    except AssertionError:pass
    else:raise AssertionError('Invalid fixture accepted: '+mode)
delta=load(P/'delta-r2.json');assert delta['old_requirements_verbatim']==21 and delta['old_cases_preserved']==30
assert delta['pending_external_owner_group']=='G09'
actual=[dict(id=a['id'],old_pointer=f'/{i}/setup_and_action',new_pointer=f'/{i}/setup_and_action',old_action=a['setup_and_action'],new_action=b['setup_and_action'],finite_contexts=b.get('finite_contexts')) for i,(a,b) in enumerate(zip(oldcases,cases)) if a['setup_and_action']!=b['setup_and_action']]
assert delta['refined_actions']==actual and len(actual)==13
assert delta['adopted_audit_groups']==['G01','G02','G03','G04','G05','G06','G07','G08','G10','G11']
for snap,domain in [('spec-r2.md','specs'),('research-r2.md','research')]:assert (P/snap).read_bytes()==(R/'wiki'/domain/'settings-learning-workflows.md').read_bytes()
spec=(P/'spec-r2.md').read_text();assert 'revision: 2\n' in spec
for r in requirements:assert f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}" in spec
sys.path.insert(0,str(R/'tools'))
from spec_browser import spec_rows
assert {r['id'] for r in spec_rows(R/'wiki/specs/settings-learning-workflows.md',spec)}==set(req)
fixture=load(P/'fixtures-r2.json');assert 'Active input is not active operation' in fixture['positive_guard']
review=load(P.parent/'reviews/settings-source-audit-review.json')
assert review['reviewed_manifest_sha256']=='e443795e09bdeae4f022043fd9a9244305aecaea3459d084506ccf854d248186' and review['findings']==[]
# Exact historical records remain frozen; actual historical replay is a separate tool.
r4=load(P.parent/'inventory-revisions/r4-citation-crosswalk/inputs.json')['pins']
for i,snapshot in [(64,'research-r1.md'),(68,'spec-r1.md')]:assert info(P/snapshot)=={k:r4[i][k] for k in ['bytes','sha256']}
if not preflight:
    manifest=load(P/'manifest-author-r2.json')
    assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(manifest['files'])|{'manifest-author-r2.json'}
    for n,x in manifest['files'].items():assert info(P/n)==x
links=0
for p in [R/'wiki/specs/settings-learning-workflows.md',R/'wiki/research/settings-learning-workflows.md',P/'README-r2.md']:
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',p.read_text()):
        if re.match(r'[a-zA-Z]+:',target):continue
        dest=(p.parent/target.split('#')[0]).resolve() if target.split('#')[0] else p
        if preflight and dest==P/'manifest-author-r2.json':continue
        assert dest.is_file(),(p,target)
        links+=1
for p in [x for x in P.rglob('*') if x.is_file() and x.suffix in {'.md','.py','.json','.txt'}]:
    if p.suffix=='.json':load(p)
    result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True)
    assert not result.stdout and not result.stderr,p
assert before=={str(p):info(p) for p in watched}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',requirements=21,cases=31,old_files_and_archive=14,source_blocks=70,input_pins=len(inputs),exact_browser_IDs=21,refined_actions=13,adopted_local_groups=10,external_group_G09='pending',visible_documentary=18,actual_outcomes='allnull/U/unexecuted',selfchecks=3,local_links=links,writes=False),indent=2))
