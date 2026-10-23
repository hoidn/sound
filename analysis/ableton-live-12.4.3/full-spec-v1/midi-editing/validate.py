"""Validate retained documentation packet, never run Live or a candidate."""
from pathlib import Path
import hashlib,json,re,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
repo=root.parents[3]
spec=repo/'wiki/specs/midi-editing-tools.md'
research=repo/'wiki/research/midi-editing-tools.md'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
source_records=json.loads((root/'sources.json').read_text())
for source in source_records:
    assert sha(root/source['html'])==source['html_sha256']
    soup=BeautifulSoup((root/source['html']).read_bytes(),'html.parser')
    for heading in source['headings']:
        if heading['id']: assert soup.find(id=heading['id']) is not None
    lines=(root/source['derived_text']).read_text().splitlines()
    assert all(line.startswith(f'{i:04d} ') for i,line in enumerate(lines,1))
spec_text=spec.read_text()
reqs=re.findall(r'^\| (REQ-MIDI-EDIT-\d{3}) \|',spec_text,re.M)
assert reqs==[f'REQ-MIDI-EDIT-{i:03}' for i in range(1,44)]
cases=json.loads((root/'acceptance-cases.json').read_text())['cases']
assert [c['id'] for c in cases]==[f'MED-{i:03}' for i in range(1,58)]
assert [c['requirement'] for c in cases[:43]]==reqs
assert all(c['target_12_4_3_grade']=='U' and c['execution']=='not-run' for c in cases)
assert [c['documented_domain_grade'] for c in cases]==['D12']*43+['U']*14
inventory=json.loads((root.parent/'inventory/midi-tools.json').read_text())
assert len(inventory)==17
row_titles=[line.split('|')[2].strip() for line in spec_text.splitlines() if line.startswith('| REQ-MIDI-EDIT-')][26:]
assert row_titles==[tool['title']+(' tool' if tool['title'] in ('Chop','LFO','Quantize','Time Warp') else '') for tool in inventory]
survey=json.loads((root/'schema-correlation.json').read_text())
assert sha(repo/survey['source'])==survey['sha256']
assert len(survey['classes'])==23
schema=ET.parse(repo/survey['source']).getroot()
assert sum(not c['class'].endswith('FilterAlgorithm') for c in survey['classes'])==15
for cls in survey['classes']:
    element=schema.find(cls['class'])
    assert element is not None
    assert cls['fields']==[{'name':child.tag,**child.attrib} for child in element]
locators=[]
for source_key,heading_ids,ranges in re.findall(r'^\| ((?:E|T)\d+) \| (.*?) \| (.*?) \|$',spec_text,re.M):
    source=source_records[0 if source_key.startswith('E') else 1]
    body=(root/source['derived_text']).read_text().splitlines()
    html=(root/source['html']).read_text()
    for heading in re.findall(r'`([^`]+)`',heading_ids): assert f'id="{heading}"' in html
    for start,end in re.findall(r'(\d+)–(\d+)',ranges): assert 1<=int(start)<=int(end)<=len(body)
    locators.append(source_key)
assert set(locators)=={f'E{i}' for i in range(1,24)}|{f'T{i}' for i in range(1,20)}
# File existence only here; heading-ID evidence checked above and local section IDs are known owners.
for doc in (spec,research):
    text=doc.read_text()
    assert all(re.search(rf'^{field}: .+',text,re.M) for field in ('id','type','status','updated','access'))
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if '://' in target or target.startswith('#'):continue
        assert (doc.parent/target.split('#')[0]).resolve().exists(),(doc,target)
manifest=json.loads((root/'manifest.json').read_text())
for entry in manifest['files']+manifest['external_dependencies']:
    assert sha(repo/entry['path'])==entry['sha256'],entry['path']
print(json.dumps({'status':'pass','scope':'Packet/document mechanical checks only; no reference/candidate execution, semantic acceptance or full-product closure','requirements':len(reqs),'cases':len(cases),'D12_cases':43,'U_cases':14,'target_U_cases':57,'tools':len(inventory),'schema_classes':len(survey['classes']),'source_locators':len(locators),'manifest_payloads':len(manifest['files'])},indent=2))
