"""Check frozen analyst identities/catalogs, never audio or reference conformance."""
from pathlib import Path
from collections import Counter
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
ROOT = P.parents[3]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return json.loads((P / name).read_text())

manifest = read('manifest-author-r2.json')
assert manifest['original_execution'] is False and manifest['candidate_comparison'] is False
assert manifest['status'] == 'author-frozen-partial-draft-awaiting-independent-review'
for record in manifest['payloads']:
    path = P / record['file']
    assert path.is_file() and path.stat().st_size == record['bytes'] and sha(path) == record['sha256'], record
for record in manifest['external_pins']:
    path = P / record['file']
    assert path.is_file() and path.stat().st_size == record['bytes'] and sha(path) == record['sha256'], record
sources = read('sources.json')
assert len(sources) == 7 and len({s['id'] for s in sources}) == 7
for record in sources:
    path = P / record['file']
    assert path.stat().st_size == record['bytes'] and sha(path) == record['sha256'], record['id']
assert sources[0]['sha256'] == '3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a'
assert sources[1]['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
observations = read('preset-observations.json')
assert len(observations) == 5
for obs, record in zip(observations, sources[2:]):
    xml_path = P / record['file'].replace('.adv', '.xml')
    assert gzip.decompress((P / record['file']).read_bytes()) == xml_path.read_bytes()
    root = ET.fromstring(xml_path.read_bytes())
    node = root.find(obs['class'])
    assert root.attrib == record['version'] == obs['creator'] and node is not None
    assert [c.tag for c in node] == obs['top_level_fields']
    assert record['locator'] == obs['preset_locator'] == '/Ableton/' + obs['class']
schema_bytes = (P / sources[1]['file']).read_bytes()
schema = ET.fromstring(schema_bytes)
for cls, record in read('schema-fields.json').items():
    node = schema.find(cls)
    assert node is not None
    assert record['fields'] == [{'name': child.tag, **child.attrib} for child in node]
    assert schema_bytes.decode().splitlines()[record['line'] - 1].strip() == f'<{cls}>'
requirements, cases, locators = read('requirements.json'), read('cases.json'), read('manual-locators.json')
assert len(requirements) == 109 and len(cases) == 154 and len(locators) == 567
assert len({r['id'] for r in requirements}) == len(requirements)
assert len({c['id'] for c in cases}) == len(cases)
assert Counter(r['provenance'] for r in requirements) == {'D12': 104, 'U': 5}
assert all(r['target_applicability'] == 'U' for r in requirements)
assert {r['id'] for r in requirements} == {rid for c in cases for rid in c['requirements']}
assert all(c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False for c in cases)
assert all(c['documentary_expected'] is None and c['documentary_comparator'] is None for c in cases if '-U-' in c['id'])
assert all(c['documentary_comparator'] is None for c in cases if c['kind'] == 'signal-obligation')
manual_lines = (P / sources[0]['file']).read_text().splitlines()
for locator, record in locators.items():
    assert 1 <= record['html_line'] <= len(manual_lines) and record['heading_context']
    block = next(b for b in read(record['file']) if b['locator'] == locator)
    assert block['text'] == record['text'] and block['html_line'] == record['html_line']
for req in requirements:
    assert all(b in locators for b in req['source_blocks'])
    linked = [c for c in cases if req['id'] in c['requirements']]
    assert len(linked) == (10 if req['provenance'] == 'U' else 1)
    if req['provenance'] == 'D12':
        assert linked[0]['source_blocks'] == req['source_blocks'] and linked[0]['documentary_expected'] == req['contract']
lifecycle_kinds = {'boundary','automation','transport','persistence','undo-redo','malformed','cancellation','teardown','sample-rate','tuning-mpe'}
for obs in observations:
    device = obs['device']
    owned = [c for c in cases if c['device'] == device]
    assert {c['kind'] for c in owned if '-U-' in c['id']} == lifecycle_kinds
    count = read('counts.json')[device]
    assert count['cases'] == len(owned) and count['kinds'] == dict(Counter(c['kind'] for c in owned))
assert all(c['preconditions'] == ['common-setup','positive-signal-guard'] for c in cases)
page_records = manifest['canonical_snapshots']
assert len(page_records) == 2
link_count = 0
for record in page_records:
    canonical, snapshot = ROOT / record['canonical'], P / record['snapshot']
    assert canonical.read_bytes() == snapshot.read_bytes() and sha(canonical) == record['sha256']
    text = canonical.read_text()
    assert text.startswith('---\n')
    frontmatter = text.split('---',2)[1]
    for key in ['id','type','status','updated','access']:
        assert re.search(r'^' + key + r': .+', frontmatter, re.M)
    assert 'access: analysis' in frontmatter and '2026-10-19' in frontmatter
    for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', text):
        if '://' in dest or dest.startswith('#'):
            continue
        local = dest.split('#',1)[0]
        assert (canonical.parent / local).exists(), (canonical, dest)
        link_count += 1
for file in P.iterdir():
    if file.suffix in ['.md','.json','.py','.txt','.xml']:
        assert not any(line.rstrip(' \t') != line for line in file.read_text().splitlines()), file
for record in page_records:
    assert not any(line.rstrip(' \t') != line for line in (ROOT / record['canonical']).read_text().splitlines())
result = {'scope': 'Frozen analyst payload/source identity, gzip/XML/schema observations, source-block references, catalogs, null target outcomes, lifecycle coverage, canonical snapshots/frontmatter/relative files and untracked-aware trailing whitespace only', 'result': 'pass', 'payloads': len(manifest['payloads']), 'external_pins':len(manifest['external_pins']), 'sources':len(sources), 'manual_blocks':len(locators), 'requirements':len(requirements), 'cases':len(cases), 'exact_target_graded_cases':0, 'local_links':link_count, 'original_execution':False, 'candidate_comparison':False, 'independent_semantic_review':'pending', 'limitations':['Figures uninspected','No source-link heading anchors used by these pages','Index/coverage/questions/log integration belongs to root','Hash/catalog success is not behavioral conformance', 'Exact34payload r1 and extras preserved; JSON/source byte equality; heading-only delta; browser109of109']}

# This successor checks the exact editorial delta against the immutable prior seal.
response = json.loads((P / 'response-author-r2.json').read_text())
prior_path = P / response['prior_manifest']
assert hashlib.sha256(prior_path.read_bytes()).hexdigest() == response['prior_manifest_sha256']
prior = json.loads(prior_path.read_text())
prior_records = [(record['file'], record) for record in prior['payloads']]
for rel, pin in prior_records:
    archived = prior_path.parent / rel
    raw = archived.read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], rel
    current = P / rel
    if True:
        assert current.read_bytes() == raw, rel
assert (P / 'manifest-author-r1.json').read_bytes() == prior_path.read_bytes()
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
browser_spec = ROOT / 'wiki/specs/synthesis-instruments.md'
browser_rows = spec_browser.spec_rows(browser_spec, browser_spec.read_text())
requirement_ids = {r['id'] for r in json.loads((P / 'requirements.json').read_text())}
assert len(browser_rows) == 109 and {r['id'] for r in browser_rows} == requirement_ids
assert len(spec_browser.spec_rows(browser_spec, (prior_path.parent / 'spec-r1.md').read_text())) == 104

result['browser_rows'] = len(browser_rows)
result['preserved_prior_payloads'] = len(prior_records)
print(json.dumps(result,indent=2))
