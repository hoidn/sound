"""Validate frozen analyst sources/catalogs only; never execute Max, Live or a patch."""
from pathlib import Path
from collections import Counter
import hashlib
import html
import json
import re

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def read(name):return json.loads((P/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=read('manifest-author-r1.json')
for rec in manifest['payloads']+manifest['external_pins']:
    path=P/rec['file']
    assert path.is_file() and path.stat().st_size==rec['bytes'] and sha(path)==rec['sha256'],rec
source=read('source.json')
assert source['url']=='https://www.ableton.com/en/live-manual/12/max-for-live/'
assert source['bytes']==250005 and source['sha256']=='2f771ab26d3e08d4c7df737fbf2a2f95e62cc501739ba65a4531de90d0de69dc'
assert sha(P/source['file'])==source['sha256']
sources=read('sources.json')
assert len(sources)==8 and len({s['id'] for s in sources})==8
for rec in sources:
    path=P/rec['file']
    assert path.stat().st_size==rec['bytes'] and sha(path)==rec['sha256']
source_lines=(P/source['file']).read_text().splitlines()
blocks=read('manual-blocks.json')
assert len(blocks)==42 and blocks[0]['section']=='32' and blocks[-1]['heading_context'][-1]['section']=='32.6'
lookup={b['locator']:b for b in blocks}
assert len(lookup)==42
for block in blocks:
    assert 280<=block['html_line']<=348
    assert all(h['section'] and h['anchor'] for h in block['heading_context'])
    actual=' '.join(html.unescape(re.sub('<[^>]*>','',source_lines[block['html_line']-1])).split())
    assert block['text'] in actual,block['locator']
original_inventory=json.loads((P/'../inventory/devices.json').read_text())
boundary=read('inventory-boundary.json')
assert boundary==[r for r in original_inventory if r['kind'] in ['max-device','max-midi-tool','max-template']]
assert Counter(r['kind'] for r in boundary)=={'max-device':20,'max-midi-tool':2,'max-template':5}
files=read('template-files.json')
assert len(files)==5
for rec in files:
    entry=next(r for r in boundary if r['id']==rec['id'])
    assert entry['kind']=='max-template' and entry['name']==rec['name']
    data=(P/rec['file']).read_bytes()
    assert Path(rec['original_path']).read_bytes()==data
    assert len(data)==entry['source']['bytes']==rec['bytes']
    assert sha(P/rec['file'])==entry['source']['sha256']==rec['sha256']
    assert data[:16].hex()==rec['prefix_hex']
requirements,cases=read('requirements.json'),read('cases.json')
assert len(requirements)==38 and len(cases)==64
assert len({r['id'] for r in requirements})==38 and len({c['id'] for c in cases})==64
assert Counter(r['provenance'] for r in requirements)=={'D12':22,'Dpkg':5,'U':11}
assert Counter(c['provenance'] for c in cases)=={'D12':22,'Dpkg':5,'U':37}
assert {r['id'] for r in requirements}=={r for c in cases for r in c['requirements']}
assert all(r['target_applicability']=='U' for r in requirements)
assert all(c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
for req in requirements:
    assert all(b in lookup for b in req['source_blocks'])
    linked=[c for c in cases if req['id'] in c['requirements']]
    if req['provenance']=='D12':
        assert req['source_id']=='D12-MAX-HOST' and req['source_blocks']
        assert len(linked)==1 and linked[0]['documentary_expected']==req['contract']
    elif req['provenance']=='Dpkg':
        assert req['source_id']==req['template'] and any(f['id']==req['source_id'] for f in files)
        assert len(linked)==1 and linked[0]['kind']=='package'
    else:
        assert len(linked)==(5 if req['template'] else 2)
for case in cases:
    assert case['fixture']=='fixtures.json#MAX-HOST-F0'
    if case['provenance']=='U':
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None
    if case['kind'] in ['signal-obligation','timing-obligation']:
        assert case['documentary_comparator'] is None
for file in files:
    own=[r for r in requirements if r['template']==file['id']]
    assert Counter(r['provenance'] for r in own)=={'D12':1,'Dpkg':1,'U':1}
    own_cases=[c for c in cases if c['template']==file['id']]
    assert len(own_cases)==7
    assert {'signal-obligation','persistence','malformed','cancellation','teardown','package'}<={c['kind'] for c in own_cases}
fixtures=read('fixtures.json')
assert fixtures['id']=='MAX-HOST-F0' and fixtures['original_execution'] is False and fixtures['candidate_comparison'] is False
counts=read('counts.json')
assert counts['requirements']==38 and counts['cases']==64 and counts['target_graded']==0
assert counts['case_kinds']==dict(Counter(c['kind'] for c in cases))
links=0
for rec in manifest['canonical_snapshots']:
    canonical,snapshot=ROOT/rec['canonical'],P/rec['snapshot']
    assert canonical.read_bytes()==snapshot.read_bytes() and sha(canonical)==rec['sha256']
    text=canonical.read_text();frontmatter=text.split('---',2)[1]
    assert text.startswith('---\n')
    for key in ['id','type','status','updated','access']:
        assert re.search(r'^'+key+r': .+',frontmatter,re.M)
    assert 'access: analysis' in frontmatter and 'updated: 2026-10-19' in frontmatter
    for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
        if '://' in dest or dest.startswith('#'):continue
        parts=dest.split('#',1);path=canonical.parent/parts[0]
        assert path.exists(),(canonical,dest)
        if len(parts)>1 and path.suffix=='.json':assert json.loads(path.read_text()).get('id')==parts[1]
        links+=1
    assert not any(line.rstrip(' \t')!=line for line in text.splitlines())
for file in P.iterdir():
    if file.suffix in ['.md','.json','.py','.txt']:
        assert not any(line.rstrip(' \t')!=line for line in file.read_text().splitlines()),file
result={'result':'pass','scope':'Frozen source/payload hashes;42 exact source paragraph lines/heading contexts;5 original/copy unparsed template identities and27 boundary records;38 requirement/64 case IDs,provenance,links and null target outcomes;template-specific and host lifecycle kinds;canonical snapshots/metadata;local files/JSON fixture anchors;untracked-aware whitespace only','payloads':len(manifest['payloads']),'external_pins':len(manifest['external_pins']),'source_pins':8,'manual_blocks':42,'requirements':38,'requirement_provenance':{'D12':22,'Dpkg':5,'U':11},'cases':64,'case_provenance':{'D12':22,'Dpkg':5,'U':37},'target_graded':0,'local_links':links,'original_execution':False,'candidate_comparison':False,'independent_semantic_review':'pending','limits':['Figures not inspected','Template AMXD contents unparsed; no patch code read/executed','No user patches/media/MIDI/reference outputs supplied or executed','Twenty shipped Max devices remain pending;two tools algorithms remain MIDI owner','No arbitrary API/patch/host/DSP compatibility or numerical oracle','Shared indexes/coverage/questions/log integration owned by root']}
(P/'validation-author-r1.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
