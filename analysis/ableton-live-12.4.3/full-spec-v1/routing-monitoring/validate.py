"""Read-only analyst packet checks; never device, application or hardware tests."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
from html.parser import HTMLParser
import hashlib
import json
import re
import subprocess

P = Path(__file__).resolve().parent
ROOT = P.parents[3]


def read(name):
    return json.loads((P / name).read_text())


def pin(record):
    path = Path(record['path'])
    if not path.is_absolute():
        path = P / path
    data = path.read_bytes()
    assert len(data) == record['bytes'], path
    assert hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


sources = read('sources.json')
assert len(sources) == 5 and len({s['id'] for s in sources}) == 5
src = {s['id']: s for s in sources}
for s in sources:
    pin(s)
for source_id, catalog_id in [('D12-routing-and-i-o', 'RECORDING-CAPTURE-CATALOG'), ('RACKS-MAN-DEVICES', 'RACKS-CAPTURE-CATALOG')]:
    original = next(r for r in json.loads(pin(src[catalog_id])) if r['id'] == source_id)
    assert all(original[k] == src[source_id][k] for k in ['id', 'url', 'captured_utc', 'sha256', 'bytes'])
assert read('mixing-capture.json') == src['D12-MIXING']


class Blocks(HTMLParser):
    def __init__(self, start):
        super().__init__()
        self.start = start
        self.active = False
        self.tag = None
        self.headings = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ['h1', 'h2']:
            if a.get('id') == self.start:
                self.active = True
            elif self.active and not a.get('data-number'):
                self.active = False
        if self.active and self.tag is None and tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li']:
            self.tag = tag
            self.buf = []
            self.meta = {'html_line': self.getpos()[0], 'anchor': a.get('id'), 'section': a.get('data-number')}

    def handle_data(self, text):
        if self.tag:
            self.buf.append(text)

    def handle_endtag(self, tag):
        if tag == self.tag:
            text = ' '.join(''.join(self.buf).split())
            if text:
                if tag.startswith('h'):
                    level = int(tag[1])
                    self.headings = [h for h in self.headings if h['level'] < level]
                    self.headings.append(dict(level=level, text=text, **self.meta))
                self.rows.append(dict(kind=tag, text=text, heading_context=list(self.headings), **self.meta))
            self.tag = None


inputs = [
    ('routing', 'D12-routing-and-i-o', 'routing-and-io', 125, '1a9c9c842c7a2d04b59794ee12d959f7fad15e3b67f41622109ea14e06e4b9b9'),
    ('compensation', 'RACKS-MAN-DEVICES', 'device-delay-compensation', 7, '6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82'),
    ('mixing', 'D12-MIXING', 'mixing', 94, '255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e'),
]
locators = {}
for name, source_id, anchor, count, expected_hash in inputs:
    assert src[source_id]['sha256'] == expected_hash
    parser = Blocks(anchor)
    parser.feed(pin(src[source_id]).decode())
    assert len(parser.rows) == count and parser.rows[0]['anchor'] == anchor
    for i, r in enumerate(parser.rows, 1):
        r['locator'] = f'{name}:B{i:03d}'
        locators[r['locator']] = r
    assert parser.rows == read(f'manual-{name}-blocks.json')
    assert (P / f'manual-{name}.txt').read_text() == '\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in parser.rows) + '\n'
assert len(locators) == 226

requirements, cases, counts = read('requirements.json'), read('cases.json'), read('counts.json')
assert len(requirements) == len({r['id'] for r in requirements}) == 40
assert len(cases) == len({c['id'] for c in cases}) == 69
assert Counter(r['provenance'] for r in requirements) == {'D12': 35, 'U': 5}
assert counts == {'requirements': 40, 'requirement_grades': dict(Counter(r['provenance'] for r in requirements)), 'cases': 69, 'case_kinds': dict(Counter(c['kind'] for c in cases)), 'documentary_oracles': 33, 'null_documentary_oracles': 36, 'target_oracles': 0}
assert sum(c['documentary_expected'] is not None for c in cases) == 33
reqmap = {r['id']: r for r in requirements}
assert set(reqmap) == {rid for c in cases for rid in c['requirements']}
for r in requirements:
    assert r['target_applicability'] == 'U'
    assert r['provenance'] == 'U' or r['source_blocks']
    assert all(b in locators for b in r['source_blocks'])
for c in cases:
    assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
    assert len(c['requirements']) == 1 and c['requirements'][0] in reqmap
    r = reqmap[c['requirements'][0]]
    assert c['source_blocks'] == r['source_blocks']
    assert c['setup_and_action'] and c['preconditions'] == ['F0', 'positive-path-gate']
    if c['kind'] == 'signal' or r['provenance'] == 'U':
        assert c['documentary_expected'] is None and c['documentary_comparator'] is None
    else:
        assert c['documentary_expected'] == r['contract']
        assert 'no audio, MIDI-delivery, meter calibration, latency, timing or private-state oracle' in c['documentary_comparator']
assert {'control', 'state', 'signal', 'boundary', 'sample-rate', 'transport', 'persistence', 'automation', 'undo', 'malformed', 'cancel', 'source-loss', 'teardown', 'recovery'} <= {c['kind'] for c in cases}
fixtures = read('fixtures.json')
assert {'F0', 'F-AUDIO', 'F-MIDI', 'F-PATH', 'F-EXTERNAL', 'F-CUE', 'F-LATENCY', 'positive-path-gate'} <= set(fixtures)
assert 'independent positive source+return baseline' in fixtures['positive-path-gate']
assert 'matching active positive control' in fixtures['positive-path-gate']
assert 'unproven' in fixtures['F-EXTERNAL'] and 'missing capabilities leave the probe U' in fixtures['F0']


def slug(text):
    return re.sub(r'[^\w\- ]', '', re.sub(r'<[^>]+>', '', text).replace('`', '').replace('*', '').lower()).replace(' ', '-')


spec = ROOT / 'wiki/specs/routing-monitoring-latency.md'
research = ROOT / 'wiki/research/routing-monitoring-latency.md'
content = spec.read_text()
assert set(re.findall(r'^### (REQ-RML-(?:\d{3}|U-[A-Z]+))', content, re.M)) == set(reqmap)
for r in requirements:
    assert '**' + r['provenance'] + '/target-U.** ' + r['contract'] in content, r['id']
    for dep in r['dependencies']:
        assert '](' + dep + ')' in content, dep
for c in cases:
    expected = 'visible control/state only' if c['documentary_expected'] is not None else 'U / null'
    assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} | {expected} |" in content
link_count = 0
for page, snapshot in [(spec, 'spec-r1.md'), (research, 'research-r1.md')]:
    text = page.read_text()
    assert (P / snapshot).read_bytes() == page.read_bytes()
    assert text.startswith('---\n') and '\nrevision: 1\n' in text
    frontmatter = text.split('---', 2)[1]
    for field in ['id', 'type', 'status', 'updated', 'access']:
        assert re.search('^' + field + ': .+', frontmatter, re.M)
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if target.startswith(('https://', 'http://')):
            continue
        filename, _, anchor = unquote(target).partition('#')
        dest = (page.parent / filename).resolve() if filename else page
        assert dest.is_file(), (page, target)
        if anchor and dest.suffix == '.md':
            assert anchor in {slug(h) for h in re.findall(r'^#+ (.+)$', dest.read_text(), re.M)}, (page, target)
        link_count += 1
manifest = read('manifest-author-r1.json')
assert manifest['requirements'] == 40 and manifest['cases'] == 69
for name, r in manifest['files'].items():
    pin(dict(path=name, **r))
assert set(manifest['files']) == {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name != 'manifest-author-r1.json'}
for path in [spec, research] + [f for f in P.rglob('*') if f.is_file() and f.suffix in {'.md', '.json', '.txt', '.py'}]:
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], text=True, capture_output=True)
    assert result.returncode in [0, 1] and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)

print(json.dumps({'status': 'pass', 'scope': 'analyst packet/source integrity only', **counts, 'source_records': 5, 'manual_sources': 3, 'original_capture_catalogs': 2, 'retained_blocks': 226, 'all_target_expected_comparison_null_U_unexecuted': True, 'null_documentary_signal_and_unknown_oracles': 36, 'canonical_snapshots': 2, 'local_links_and_anchors': link_count, 'checks': ['source pins and original reused-capture identities', '226 HTML block texts/lines/headings independently reproduced', 'unique IDs, supported evidence routes, case kinds and linked owners', 'case/count tables, all null target oracles, positive-path prerequisites', 'canonical snapshot equality, frontmatter, local links and Markdown anchors', 'manifest hashes and complete payload inventory', 'untracked-aware authored whitespace'], 'limits': ['Author self-check; independent semantic review required', 'No original/extracted-original/candidate/hardware/audio/MIDI execution', 'No numeric latency/DSP/driver/performance or complete routing compatibility proof', 'Future stimuli and qualifying hardware/plugin/latency baselines not retained', 'Figures and linked help/tutorials not inspected; no tooling installed']}, indent=2))
