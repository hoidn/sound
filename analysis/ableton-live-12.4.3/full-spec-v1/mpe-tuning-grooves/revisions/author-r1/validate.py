"""Check this bounded analyst packet, then freeze an author snapshot. No reference tests."""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
docs=[REPO/'wiki/specs/mpe-workflows.md',REPO/'wiki/specs/tuning-systems.md',REPO/'wiki/specs/groove-workflows.md',REPO/'wiki/research/mpe-tuning-grooves.md']
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2)+'\n')

cases=json.loads((ROOT/'cases.json').read_text())
assert len(cases)==83 and len({c['id'] for c in cases})==83
requirements=set()
for doc in docs:
    text=doc.read_text()
    assert text.startswith('---\n')
    front=text.split('---',2)[1]
    for field in ['id','type','status','updated','access']:
        assert re.search(rf'^{field}: .+',front,re.M), (doc,field)
    assert 'updated: 2026-10-19' in front and 'access: analysis' in front
    if '/specs/' in str(doc):
        requirements.update(re.findall(r'^\| (REQ-[A-Z]+-\d{3}) \|',text,re.M))
assert len(requirements)==53
assert {c['requirement'] for c in cases}==requirements
assert all(c['target_build_grade']=='U' and c['execution']=='unexecuted' for c in cases)
assert all(c['setup'] and c['action'] and c['expected'] and c['comparator'] and c['source'] for c in cases)
for prefix in ['MPE','TUN','GRV']:
    kinds={k for c in cases if c['id'].startswith(prefix) for k in c['kinds']}
    assert {'positive','negative','boundary','malformed','cancellation','undo','persistence','teardown'}<=kinds
assert collections.Counter(c['documentary_grade'] for c in cases)=={'D12':52,'U':31}
for source in json.loads((ROOT/'sources.json').read_text()):
    assert sha(ROOT/source['html'])==source['sha256']
    assert (ROOT/source['text']).exists()
for example in json.loads((ROOT/'shipped-examples.json').read_text()):
    assert sha(ROOT/example['retained'])==example['sha256']
    assert sha(Path(example['path']))==example['sha256']
    if 'derived_xml' in example:
        raw=(ROOT/example['retained']).read_bytes()
        xml=gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw
        assert xml==(ROOT/example['derived_xml']).read_bytes()
schema=json.loads((ROOT/'schema-presence.json').read_text())
assert sha(Path(schema['path']))==schema['sha256']
schema_lines=Path(schema['path']).read_text().splitlines()
for block in schema['classes']:
    assert '\n'.join(schema_lines[block['start_line']-1:block['end_line']])==block['text']
assert sha(ROOT/'help-rendered-web-2026-10-19.txt')=='6bf5a4559fab3edcd92c86c796ab65fc8dcb202e40bb37d2ab3bf495fbed8610'

# Generate these two documented outputs before checking their incoming links.
write_json('validation.json',{'scope':'four assigned Markdown pages, cases and pinned packet sources only','date':'2026-10-19','requirements':53,'cases':83,'documentary_grades':{'D12':52,'U':31},'exact_build_grades':{'U':83},'original_or_candidate_execution':False,'checks':['frontmatter','requirement/case identity and category coverage','manual HTML hashes','shipped example original/retained hashes and XML derivation','schema hash and exact line blocks','rendered support capture hash','relative file and heading links','no trailing whitespace in authored pages'],'index_integration':'root-owned, outside this focused check'})
write_json('manifest-author-r1.json',{})
links=0
for doc in docs:
    for line in doc.read_text().splitlines():
        assert line==line.rstrip(),(doc,'trailing whitespace')
    for ref in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
        if ref.startswith(('https://','http://')):
            continue
        file,_,anchor=ref.partition('#')
        path=(doc.parent/file).resolve() if file else doc
        assert path.exists(),(doc,ref)
        if anchor and path.suffix=='.md':
            headings=[]
            for heading in re.findall(r'^#+ (.+)$',path.read_text(),re.M):
                headings.append(re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-'))
            assert anchor in headings,(doc,ref,headings)
        links+=1
snapshots=[]
for doc in docs:
    target=ROOT/(doc.stem+'-author-r1.md')
    target.write_bytes(doc.read_bytes())
    snapshots.append({'canonical':str(doc.relative_to(REPO)),'snapshot':target.name,'sha256':sha(target)})
payloads=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='manifest-author-r1.json']
write_json('manifest-author-r1.json',{'packet':'F-04 MPE/tuning/grooves','author_revision':1,'frozen':'2026-10-19','target':'Live 12 Suite 12.4.3','status':'partial draft for independent review; not released','requirements':53,'cases':83,'source_capture_policy':'three unchanged manual HTML captures; support source raw HTTP403, exact rendered web response retained instead','snapshots':snapshots,'payloads':payloads,'review':'pending separate context','compatibility':'unexecuted; all exact-build case grades U'})
print(json.dumps({'result':'pass','requirements':53,'cases':83,'links_checked':links,'payloads':len(payloads),'runtime_tests':0}))
