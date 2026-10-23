"""Focused frozen documentary packet checks; no application/audio execution."""
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
assert source['url']=='https://www.ableton.com/en/live-manual/12/clip-view/'
assert source['bytes']==306606 and source['sha256']=='30f156e6d83c8f4caf3fe9dcf55bb2b764dc42ed8cbd3847863a53747851bd80'
assert sha(P/source['file'])==source['sha256']
source_lines=(P/source['file']).read_text().splitlines()
blocks=read('manual-blocks.json')
assert len(blocks)==180 and blocks[0]['section']=='8' and blocks[-1]['heading_context'][-1]['section']=='8.14'
lookup={b['locator']:b for b in blocks}
assert len(lookup)==180
for block in blocks:
    assert 280<=block['html_line']<=844
    assert all(h['section'] and h['anchor'] for h in block['heading_context'])
    # All retained chapter paragraphs start and end on their indicated HTML line.
    actual=' '.join(html.unescape(re.sub('<[^>]*>','',source_lines[block['html_line']-1])).split())
    assert block['text'] in actual,(block['locator'],block['text'][:40])
requirements,cases=read('requirements.json'),read('cases.json')
assert len(requirements)==54 and len(cases)==62
assert len({r['id'] for r in requirements})==54 and len({c['id'] for c in cases})==62
assert Counter(r['provenance'] for r in requirements)=={'D12':46,'U':8}
assert {r['id'] for r in requirements}=={r for c in cases for r in c['requirements']}
assert all(r['target_applicability']=='U' for r in requirements)
assert all(c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
for req in requirements:
    assert all(b in lookup for b in req['source_blocks'])
    linked=[c for c in cases if req['id'] in c['requirements']]
    assert len(linked)==(1 if req['provenance']=='D12' else 2)
    if req['provenance']=='D12':
        assert linked[0]['source_blocks']==req['source_blocks'] and linked[0]['documentary_expected']==req['contract']
for case in cases:
    assert case['fixture']=='fixtures.json#CV-BASE'
    if case['id'].startswith('CV-U-'):
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None and case.get('unknown')
    if case['kind'] in ['signal-obligation','timing-obligation']:
        assert case['documentary_comparator'] is None
required_kinds={'positive','negative','boundary','malformed','cancellation','undo-redo','automation','persistence','source-loss','teardown','sample-rate','midi-output'}
assert required_kinds<={c['kind'] for c in cases}
assert set(read('source-routing.json'))==set(lookup)
assert read('source-routing.json')['CV:B009']['owner']=='session-view-workflows.md'
fixtures=read('fixtures.json')
assert fixtures['id']=='CV-BASE' and fixtures['original_execution'] is False and fixtures['candidate_comparison'] is False
counts=read('counts.json')
assert counts['requirements']==54 and counts['cases']==62 and counts['target_graded']==0
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
        parts=dest.split('#',1);path=(canonical.parent/parts[0])
        assert path.exists(),(canonical,dest)
        if len(parts)>1 and path.suffix=='.json':
            assert json.loads(path.read_text()).get('id')==parts[1]
        links+=1
    assert not any(line.rstrip(' \t')!=line for line in text.splitlines())
for file in P.iterdir():
    if file.suffix in ['.md','.json','.py','.txt']:
        assert not any(line.rstrip(' \t')!=line for line in file.read_text().splitlines()),file
result={'result':'pass','scope':'Frozen source/payload hashes;180 exact source paragraph lines/heading contexts;54 requirement/62 case IDs,provenance,links and null target outcomes;required lifecycle kinds;canonical snapshots/metadata;local files and JSON fixture anchors;untracked-aware whitespace only','payloads':len(manifest['payloads']),'external_pins':len(manifest['external_pins']),'manual_blocks':180,'requirements':54,'cases':62,'target_graded':0,'local_links':links,'original_execution':False,'candidate_comparison':False,'independent_semantic_review':'pending','limitations':['Figures not inspected','No media/MIDI/reference outputs supplied or executed','No audio/time/file codec numerical oracle','Shared indexes/coverage/questions/log integration owned by root']}
(P/'validation-author-r1.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
