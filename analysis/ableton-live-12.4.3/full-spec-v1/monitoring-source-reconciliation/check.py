#!/usr/bin/env python3
"""Finite Monitoring text reconciliation; replay is read-only, no vendor code runs."""
from pathlib import Path
from html.parser import HTMLParser
import copy
import hashlib
import json
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
B = P.parent


def load(p):
    return json.loads(p.read_text())


def identity(p):
    data = p.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = None
        self.parts = []
        self.blocks = []
        self.links = []
        self.images = []
        self.headers = []

    def character_offset(self):
        line, column = self.getpos()
        return sum(len(x) for x in self.rawdata.splitlines(keepends=True)[:line - 1]) + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.active is None and tag in {'h2', 'p', 'li'}:
            self.active, self.start, self.parts = tag, self.character_offset(), []
        if tag == 'h2':
            self.headers.append(attrs)
        if tag == 'a':
            self.links.append(attrs.get('href'))
        if tag in {'img', 'figcaption', 'table'}:
            self.images.append(tag)

    def handle_data(self, value):
        if self.active:
            self.parts.append(value)

    def handle_endtag(self, tag):
        if tag == self.active:
            self.blocks.append({'tag': tag, 'text': ' '.join(''.join(self.parts).split()),
                                'relative_start': self.start,
                                'relative_end_exclusive': self.character_offset() + len('</' + tag + '>')})
            self.active, self.parts = None, []


def pointer(obj, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def reconcile(selected, ledger, owners, proposals):
    original = load(B / 'routing-monitoring/manual-routing-blocks.json')[8:17]
    assert selected['blocks'] == original
    assert selected['compensation_context'] == load(B / 'routing-monitoring/manual-compensation-blocks.json')
    lookup = {x['locator']: x for x in original}
    assert len(ledger) == 24 and [x['id'] for x in ledger] == ['MON-F%02d' % i for i in range(1, 25)]
    keys = {x['key'] for x in owners['references']}
    assert len(keys) == len(owners['references']) == 22
    for ref in owners['references']:
        data = ROOT / ref['catalog']
        if ref.get('format') == 'markdown-section':
            assert data.read_text()[ref['character_start']:ref['character_end_exclusive']] == ref['quoted_scoped_predicate']
            assert ref['quoted_scoped_predicate'].startswith('### REQ-RECORDING-COMPING-002')
        else:
            row = pointer(load(data), ref['pointer'])
            assert row['id'] == ref['id'] and row[ref['quote_field']] == ref['quoted_scoped_predicate']
    for row in ledger:
        assert row['source_quote'] == lookup[row['source_block']]['text']
        assert set(row['owner_references']) <= keys
        assert row['target_applicability'] == 'U' and row['complete'] is False
    assert {x['source_block'] for x in ledger} == {'routing:B%03d' % i for i in range(10, 18)}
    # These distinct source roles prevent adjacent guidance from becoming a new law.
    assert ledger[11]['source_block'] == 'routing:B013' and ledger[11]['disposition'] == 'missing'
    assert ledger[19]['source_block'] == 'routing:B015' and ledger[19]['disposition'] == 'partial_entry'
    assert ledger[20]['disposition'] == 'represented' and 'RML-007' in ledger[20]['owner_references']
    assert ledger[5]['disposition'] == ledger[16]['disposition'] == 'outcome_U'
    assert all(ledger[i]['disposition'] == 'guidance' for i in [1, 9, 13, 14, 15, 18])
    assert len(proposals['groups']) == 2
    for i, row in enumerate(proposals['groups'], 1):
        assert row['id'] == 'MON-P%02d' % i and row['owner'] == 'routing-monitoring-latency'
        assert row['source_claim_only'] is True and row['executed'] is False and row['complete'] is False
        assert row['target_grade'] == 'U'
        assert all(row[k] is None for k in ['expected', 'comparison', 'documentary_expected', 'documentary_comparator'])
        assert row['positive_gate'] == proposals['positive_gate'] and 'genuinely productive' in row['positive_gate']
    assert proposals['groups'][0]['source_facets'] == ['MON-F12']
    assert proposals['groups'][1]['source_facets'] == ['MON-F20']


def run():
    assert sys.argv[1:] in [['--check'], ['--seal']]
    sealing = sys.argv[1:] == ['--seal']
    manifest = P / 'manifest.json'
    assert not manifest.exists() if sealing else manifest.exists(), 'Refuse rewriting a sealed packet'
    pins = load(P / 'input-pins.json')
    assert len(pins) == 15 and len({x['path'] for x in pins}) == 15
    watched = {p: identity(p) for p in P.iterdir() if p.is_file()}
    external = {ROOT / x['path']: {k: x[k] for k in ['bytes', 'sha256']} for x in pins}
    assert all(identity(p) == data for p, data in external.items())
    selected, ledger, owners, proposals = [load(P / name) for name in
        ['selected-source.json', 'ledger.json', 'owner-reconciliation.json', 'proposals.json']]
    reconcile(selected, ledger, owners, proposals)
    context = load(P / 'source-context.json')
    sl = context['raw_selection']
    raw = (ROOT / sl['source_path']).read_text()
    start, end = sl['character_start'], sl['character_end_exclusive']
    assert start == raw.index('<h2 data-number="17.1"')
    assert end == raw.index('<h2 data-number="17.2"', start)
    fragment = raw[start:end]
    assert fragment == (P / sl['file']).read_text()
    assert raw[:start].count('\n') + 1 == sl['html_line_start']
    parsed = Extract()
    parsed.feed(fragment)
    assert [{'kind': x['tag'], 'text': x['text']} for x in parsed.blocks] == [
        {k: x[k] for k in ['kind', 'text']} for x in selected['blocks']]
    assert parsed.headers == [{'data-number': '17.1', 'id': 'monitoring'}]
    assert not parsed.images
    assert parsed.links == ['/en/live-manual/12/recording-new-clips/#recording-new-clips']
    assert len(context['block_locators']) == 9
    for original, block, loc in zip(selected['blocks'], parsed.blocks, context['block_locators']):
        assert loc['source_block'] == original['locator']
        assert loc['character_start'] == start + block['relative_start']
        assert loc['character_end_exclusive'] == start + block['relative_end_exclusive']
        assert loc['html_line'] == raw[:loc['character_start']].count('\n') + 1
        assert loc['html_column_zero_based'] == len(raw[:loc['character_start']].rsplit('\n', 1)[-1])
        assert loc['direct_anchor'] == ('monitoring' if block['tag'] == 'h2' else None)
    fixture = Extract()
    fixture.feed('<h2 id="x">Head</h2><ul><li><p>In <em>blue</em>.</p></li></ul><p>After.</p>')
    assert [(x['tag'], x['text']) for x in fixture.blocks] == [('h2', 'Head'), ('li', 'In blue.'), ('p', 'After.')]
    mutations = []
    d = copy.deepcopy(selected); d['blocks'].pop(); mutations.append((d, ledger, owners, proposals))
    d = copy.deepcopy(ledger); d[11]['source_block'] = 'routing:B017'; mutations.append((selected, d, owners, proposals))
    d = copy.deepcopy(ledger); d[20]['disposition'] = 'missing'; mutations.append((selected, d, owners, proposals))
    d = copy.deepcopy(owners); d['references'][0]['pointer'] = '/999'; mutations.append((selected, ledger, d, proposals))
    d = copy.deepcopy(proposals); d['groups'][0]['comparison'] = 'invented color pass'; mutations.append((selected, ledger, owners, d))
    d = copy.deepcopy(proposals); d['groups'][0]['positive_gate'] = 'accept an inactive path'; mutations.append((selected, ledger, owners, d))
    for args in mutations:
        try:
            reconcile(*args)
        except (AssertionError, IndexError, KeyError):
            continue
        raise AssertionError('mutation accepted')
    if sealing:
        for name, frozen in [('routing-monitoring-latency', B / 'routing-monitoring/spec-r1.md'),
                             ('recording-comping', B / 'recording/spec-r3.md')]:
            assert (ROOT / 'wiki/specs' / (name + '.md')).read_bytes() == frozen.read_bytes()
    for p in P.iterdir():
        if p.is_file() and p.suffix in {'.md', '.py', '.json'}:
            result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(p)], capture_output=True)
            assert result.returncode in (0, 1) and not result.stdout and not result.stderr, p
    if not sealing:
        files = load(manifest)['files']
        assert set(files) == {p.name for p in P.iterdir() if p.is_file() and p != manifest}
        assert all(identity(P / name) == data for name, data in files.items())
    assert all(identity(p) == data for p, data in watched.items())
    assert all(identity(p) == data for p, data in external.items())
    result = {'status': 'pass', 'source_subsection_blocks': 9, 'compensation_context_blocks': 7,
              'bounded_facets': 24, 'selected_owner_references': 22, 'immutable_input_pins': 15,
              'proposed_groups': 2, 'normative_adoptions': 0, 'actual_oracles': 'null/U/unexecuted',
              'images': 0, 'linked_destination_uninspected': 1, 'rejection_fixtures': len(mutations),
              'complete_topics': 0, 'runtime': False, 'writes': sealing}
    if sealing:
        data = {'id': 'MONITORING-SOURCE-RECONCILIATION-R1',
                'status': 'partial source reconciliation awaiting independent review',
                'counts': result, 'files': {p.name: identity(p) for p in sorted(P.iterdir()) if p.is_file()}}
        with manifest.open('x') as out:
            out.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
