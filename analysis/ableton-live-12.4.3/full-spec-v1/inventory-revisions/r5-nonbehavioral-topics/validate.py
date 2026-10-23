"""Read-only checks of proposed manual editorial-topic dispositions."""
from pathlib import Path
import hashlib
import json
import runpy
import subprocess

P=Path(__file__).resolve().parent
ROOT=P.parents[4]
load=lambda path:json.loads(path.read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
pins=load(P/'input-pins.json')
for pin in pins:
    path=ROOT/pin['path']
    assert path.stat().st_size==pin['bytes'] and digest(path)==pin['sha256']
Parser=runpy.run_path(str(ROOT/pins[-1]['path']))['Chapter']
sources=load(P/'sources.json')
assert len(sources)==2 and sources[0]['capture_utc'] is None
assert sources[0]['capture_date']=='2026-10-19'
for source,prefix,name,count in zip(sources,['WELCOME','CRED'],['welcome','credits'],[5,26]):
    path=ROOT/source['path'] if 'path' in source else P/source['file']
    raw=path.read_bytes()
    assert len(raw)==source['bytes'] and hashlib.sha256(raw).hexdigest()==source['sha256']
    parser=Parser()
    parser.feed(raw.decode())
    for i,row in enumerate(parser.rows,1):
        row['id']=f'{prefix}-B{i:03d}'
    assert len(parser.rows)==count and parser.rows==load(P/(name+'-blocks.json'))
original=load(ROOT/pins[0]['path'])
assert len(original)==880 and sum(r['leaf'] for r in original)==708
dispositions=load(P/'dispositions.json')
assert [r['number'] for r in dispositions]==['1','1.1','43']
assert sum(r['leaf'] for r in dispositions)==2
for row in dispositions:
    topic=next(r for r in original if r['id']==row['id'])
    assert {k:row[k] for k in topic}==topic
    assert row['disposition']=='proposed-nonbehavioral-manual-topic'
    assert not row['complete'] and row['target_applicability']=='U'
    assert row['application_requirements']==row['application_cases']==[]
    assert len(row['retained_obligations'])==2 and row['basis']
    blocks=load(P/('credits-blocks.json' if row['number']=='43' else 'welcome-blocks.json'))
    assert row['evidence_blocks']==[r['id'] for r in blocks]
if (P/'manifest.json').exists():
    for name,pin in load(P/'manifest.json')['files'].items():
        file=P/name
        assert file.stat().st_size==pin['bytes'] and digest(file)==pin['sha256'],name
for file in P.iterdir():
    if file.suffix in {'.json','.py','.md'}:
        result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(file)],capture_output=True)
        assert result.returncode in (0,1) and not result.stdout and not result.stderr,file
print(json.dumps(dict(status='pass',scope='proposed documentary disposition integrity only',topics=3,leaves=2,blocks=31,original_heading_leaf_denominator=[880,708],source_pins=2,external_input_pins=4,application_cases=0,complete_topics_claimed=0,target_applicability='U',runtime_execution=False,writes=False),indent=2))
