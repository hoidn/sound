"""Check retained-document consistency only; never grade Live compatibility."""
from pathlib import Path
import gzip, hashlib, html, json, re, xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
SPECS=[ROOT/'wiki/specs/filter-eq-devices.md',ROOT/'wiki/research/filter-eq-devices.md']
def sha(b):return hashlib.sha256(b).hexdigest()
checks={};sources=json.load(open(P/'sources.json'))
old_seal=(P/'manifest-author-r1.json').read_bytes()
assert sha(old_seal)=='0f25052e22eacc205ba7bf5d5a902027c1902051e3174e9c66f1ab22fcc3c49e'
archive=P/'revisions/author-r1'
assert (archive/'manifest-author-r1.json').read_bytes()==old_seal
old=json.loads(old_seal)
for entry in old['files']:
 b=(archive/entry['path']).read_bytes()
 assert len(b)==entry['bytes'] and sha(b)==entry['sha256'],entry['path']
archived_packet=archive/P.relative_to(ROOT)
assert (archived_packet/'sources.json').read_bytes()==(P/'sources.json').read_bytes()
checks['r1_preserved_payloads']=len(old['files'])
for src in sources:
 b=(P/src['path']).read_bytes()
 assert len(b)==src['bytes'] and sha(b)==src['sha256'],src['id']
checks['source_hashes']=len(sources)
manual=(P/'../audio-utilities/manual-audio-effects-2026-10-19.html').read_text().splitlines()
blocks={}
for file in sorted(P.glob('manual-*-blocks.json')):
 rows=json.load(open(file));assert rows and rows[0]['kind']=='h2'
 for i,row in enumerate(rows,1):
  assert row['locator']==row['device']+f':B{i:02d}'
  line=manual[row['html_line']-1]
  # Some paragraph-inline image tags span source lines; strip complete tags.
  window='\n'.join(manual[row['html_line']-1:row['html_line']+100])
  normalized=' '.join(html.unescape(re.sub(r'<[^>]*>','',window)).split())
  assert row['text'] in normalized,(row['locator'],row['html_line'])
  if row['anchor']:assert 'id="'+row['anchor']+'"' in line,row['locator']
  blocks[row['locator']]=row
checks['manual_blocks']=len(blocks)
schema=(P/'../inventory/12.0_12402.txt').read_text().splitlines()
classes=json.load(open(P/'schema-fields.json'))
for cls in classes:
 assert schema[cls['line']-1].strip()=='<'+cls['class']+'>',(cls['class'],schema[cls['line']-1])
 start=cls['line']-1;end=next(i for i in range(start+1,len(schema)) if schema[i].strip()=='</'+cls['class']+'>')
 node=ET.fromstring('\n'.join(schema[start:end+1]))
 assert [{'name':f.tag,**f.attrib} for f in node]==cls['fields'],cls['class']
checks['schema_classes']=len(classes)
observations=json.load(open(P/'package-values.json'))
for o in observations:
 raw=(P/o['source']).read_bytes();xml=gzip.decompress(raw)
 assert xml==(P/(o['source']+'.xml')).read_bytes()
 root=ET.fromstring(xml);assert root.attrib==o['root_attributes']
 assert len(list(root.iter(o['class'])))==1
checks['package_documents']=len(observations)
reqs=json.load(open(P/'requirements.json'));cases=json.load(open(P/'cases.json'))
ids={r['id'] for r in reqs};assert len(ids)==len(reqs)
assert len({c['id'] for c in cases})==len(cases)
assert {r for c in cases for r in c['requirements']}==ids

def evidence(e):
 if e.startswith(('U','PKG-')):return
 device,parts=e.split(':',1)
 for part in parts.split(','):
  span=part.split('–');lo=int(span[0][1:]);hi=int(span[-1][1:])
  for n in range(lo,hi+1):assert device+f':B{n:02d}' in blocks,e
for r in reqs:
 assert re.fullmatch(r'REQ-DEVICE-(AF|CEQ|EQ8|EQ3)-\d{3}',r['id'])
 evidence(r['evidence'])
 assert ('### '+r['id']+' — '+r['title']) in SPECS[0].read_text()
for c in cases:
 assert c['status']=='unexecuted' and set(c['requirements'])<=ids
 assert c['setup_action'] and c['criterion']
 assert (c['expected'] is None)==(c['provenance']=='U'),c['id']
 evidence(c['evidence'])
 row=next(line for line in SPECS[0].read_text().splitlines() if line.startswith('| '+c['id']+' |'))
 assert c['setup_action'].replace('|','\\|') in row,c['id']
 assert (c['expected'] or 'Unknown; no oracle, record without grading.').replace('|','\\|') in row,c['id']
 if 'file_assertions' in c:
  a=c['file_assertions'];root=ET.fromstring(gzip.decompress((P/a['path']).read_bytes()));node=root.find(a['class']);assert node is not None
  for path,expected in a['values'].items():assert node.find(path).get('Value')==expected,(c['id'],path)
for dev in ['AF','CEQ','EQ8','EQ3']:
 owned=[c for c in cases if c['device']==dev]
 kinds='/'.join(c['kind'] for c in owned)
 for kind in ['positive','negative','boundary','automation','malformed','cancel','undo','persistence','teardown','sample-rate']:assert kind in kinds,(dev,kind)
checks['requirements']=len(reqs);checks['cases']=len(cases)
fixtures=json.load(open(P/'fixture-signals.json'))['probe_fixtures']
case_by_id={c['id']:c for c in cases}
for name in ['AF-LFO','AF-ENV']:
 assert fixtures[name]['inherits']=='AF-AUDIO'
 assert fixtures[name]['active_baseline'] and fixtures[name]['mode_preflight']
for c in cases:
 for fixture in c.get('fixtures',[]):assert fixture in fixtures,c['id']
for n in [15,16,17,18,19,20,23,24,25,58,59]:assert 'AF-LFO' in case_by_id[f'AF-C{n:03d}']['fixtures']
for n in [26,27,28,29,36,37,39,40,41]:assert 'AF-ENV' in case_by_id[f'AF-C{n:03d}']['fixtures']
for n in [58,59]:assert case_by_id[f'AF-C{n:03d}']['expected'] is None
for n in [23,24]:assert 'Only UI' in case_by_id[f'AF-C{n:03d}']['expected']
assert 'nonzero gain' in case_by_id['EQ8-C018']['setup_action'] and 'distinct accepted Scale' in case_by_id['EQ8-C018']['setup_action']
for n in [5,6,7]:assert 'stably lit' in case_by_id[f'EQ3-C{n:03d}']['setup_action'] and 'constant' in case_by_id[f'EQ3-C{n:03d}']['setup_action']
checks['review_fixture_checks']='required active-baseline references, separate stochastic U, nonzero Scale inclusion, lit LED preconditions; no runtime proof'
checks['by_device']={dev:{'requirements':sum(r['device']==dev for r in reqs),'cases':{label:sum(c['device']==dev and c['provenance']==label for c in cases) for label in ['D12','Dpkg','U']}} for dev in ['AF','CEQ','EQ8','EQ3']}
for page in SPECS:
 text=page.read_text();assert text.startswith('---\n')
 header=text.split('---',2)[1]
 for key in ['id','type','status','updated','access']:assert re.search(r'^'+key+r': .+',header,re.M),(page,key)
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if link.startswith(('https://','http://','#')):continue
  path=link.split('#',1)[0];target=(page.parent/path).resolve()
  if target in [P/'manifest-author-r2.json',P/'validation-author-r2.json']:continue
  assert target.exists(),(page,link)
checks['canonical_pages']=2

# This successor checks the exact editorial delta against the immutable prior seal.
response = json.loads((P / 'response-author-r3.json').read_text())
prior_path = P / response['prior_manifest']
assert hashlib.sha256(prior_path.read_bytes()).hexdigest() == response['prior_manifest_sha256']
prior = json.loads(prior_path.read_text())
prior_records = [(record['path'], record) for record in prior['files']]
for rel, pin in prior_records:
    archived = prior_path.parent / rel
    raw = archived.read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], rel
    current = ROOT / rel
    if not rel.startswith('wiki/'):
        assert current.read_bytes() == raw, rel
assert (P / 'manifest-author-r2.json').read_bytes() == prior_path.read_bytes()
for extra in response.get('preserved_extras', []):
    assert (P / extra['file']).read_bytes() == (prior_path.parent / extra['file']).read_bytes()
    assert hashlib.sha256((P / extra['file']).read_bytes()).hexdigest() == extra['sha256']
for change in response['page_changes']:
    expected = (P / change['archive_input']).read_text()
    for edit in change['replacements']:
        assert expected.count(edit['before']) == edit['occurrences']
        expected = expected.replace(edit['before'], edit['after'])
    expected += change['append']
    assert (ROOT / change['canonical']).read_text() == expected == (P / change['snapshot']).read_text()
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'tools'))
import spec_browser
browser_spec = ROOT / 'wiki/specs/filter-eq-devices.md'
browser_rows = spec_browser.spec_rows(browser_spec, browser_spec.read_text())
requirement_ids = {r['id'] for r in json.loads((P / 'requirements.json').read_text())}
assert len(browser_rows) == 65 and {r['id'] for r in browser_rows} == requirement_ids
assert len(spec_browser.spec_rows(browser_spec, (prior_path.parent / 'wiki/specs/filter-eq-devices.md').read_text())) == 65
assert '## Auto Filter Legacy' in (ROOT / 'wiki/specs/legacy-native-devices.md').read_text()

current_manifest = json.loads((P / 'manifest-author-r3.json').read_text())
for record in current_manifest['files']:
    raw = (ROOT / record['path']).read_bytes()
    assert len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256']
for record in current_manifest['canonical_snapshots']:
    assert (ROOT / record['canonical']).read_bytes() == (P / record['snapshot']).read_bytes()
for path in SPECS + [f for f in P.rglob('*') if f.is_file() and 'revisions' not in f.relative_to(P).parts and f.suffix in {'.py','.md','.json','.txt'}]:
    if path.suffix == '.json':
        json.loads(path.read_text())
    assert not any(line.rstrip(' \t') != line for line in path.read_text().splitlines()), path
checks['r2_preserved_payloads'] = len(prior_records)
checks['requirements_cases_sources_unchanged'] = True
checks['editorial_delta_only'] = True
checks['browser_rows'] = len(browser_rows)
report={'scope':'Editorial legacy provenance/owner route and retained prior source/document/fixture consistency only; no runtime or semantic scope expansion','checks':checks,'result':'pass','original_execution':False,'candidate_execution':False,'review_limit':'Prior independent semantic reviews retain their original partial scopes; focused editorial review pending'}
print(json.dumps(report,indent=2))
