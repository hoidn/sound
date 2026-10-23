"""Read-only finite source audit. No old tool, vendor code or runtime execution."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys

P = Path(__file__).resolve().parent
R = P.parents[3]
F = P.parent
D = F / 'distortion'
NAMES = ['drum-buss', 'dynamic-tube', 'erosion', 'overdrive', 'pedal', 'redux', 'roar', 'saturator', 'vinyl-distortion']
COUNTS = dict(zip(NAMES, [24, 9, 7, 7, 36, 15, 81, 29, 8]))


def load(path):
    return json.loads(path.read_text())


def dg(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=sha256(raw).hexdigest())


def pointer(value, route):
    for key in route.strip('/').split('/') if route else []:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def parser():
    path = F / 'midi-editing-source-audit/source_parser.py'
    assert dg(path)['sha256'] == '648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
    spec = importlib.util.spec_from_file_location('distortion_audit_pure_parser', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.extract


def derive(plan, inputs):
    source = load(D / 'sources.json')[0]
    raw = Path(source['path']).read_text()
    full, resources = parser()(raw, 'AFE')
    blocks = [b for b in full if any(h['level'] == 2 and h['anchor'] in NAMES for h in b['heading_context'])]
    anchors = {h['anchor'] for b in blocks for h in b['heading_context'] if h['level'] >= 2}
    resources = [r for r in resources if r['heading_context_anchor'] in anchors]
    req, cases = load(D / 'requirements.json'), load(D / 'cases.json')
    assessments = []
    counts = Counter()
    null = dict(documentary_expected=None, documentary_comparison=None, actual_expected=None, actual_comparison=None, target='U', executed=False, complete=False, coverage_credit=0)
    for i, b in enumerate(blocks):
        name = next(h['anchor'] for h in b['heading_context'] if h['level'] == 2)
        counts[name] += 1
        local = f'{name}:B{counts[name]:03}'
        row = plan['judgments'][i]
        assert row['profile'] == name and row['local_block'] == local
        rs, cs = [], []
        for n in row['requirement_suffixes']:
            ident = f'REQ-DST-{name.upper()}-{n:03}'
            j = next(j for j, r in enumerate(req) if r['id'] == ident)
            rs.append(dict(id=ident, pointer=f'/owner_requirements/{j}', predicate_pointer=f'/owner_requirements/{j}/contract', role='Only the explicitly assessed source/contract subset; not full-block closure.'))
        for n in row['case_suffixes']:
            ident = f'DST-{name.upper()}-{n:03}'
            j = next(j for j, c in enumerate(cases) if c['id'] == ident)
            cs.append(dict(id=ident, pointer=f'/owner_cases/{j}', action_pointer=f'/owner_cases/{j}/input', role='Only the actual input/action subset explicitly distinguished from enumeration, setup, inspection or documentary expected predicate; no runtime credit.'))
        disposition = 'editorial-or-structural' if b['kind'].startswith('h') else 'represented-subset-with-action-or-prerequisite-gap' if rs and row['proposal_numbers'] else 'represented-subset-or-qualified-source-context' if rs else 'source-only-entry-or-optional-guidance' if row['proposal_numbers'] else 'research-guidance-or-historical-context'
        assessments.append(dict(id=f'DSA-A{i+1:03}', local_block=local, block=b['id'], source_pointer=f'/blocks/{i}/text', quote=b['text'], quote_sha256=sha256(b['text'].encode()).hexdigest(), assessment=row['assessment'], disposition=disposition, represented_requirement_refs=rs, represented_case_refs=cs, open_proposal_groups=[f'DSA-G{n:02}' for n in row['proposal_numbers']], **null))
    proposals = deepcopy(plan['proposals'])
    for g in proposals:
        g['assessment_ids'] = [a['id'] for a in assessments if g['id'] in a['open_proposal_groups']]
        g['source_blocks'] = [a['block'] for a in assessments if g['id'] in a['open_proposal_groups']]
    questions = deepcopy(plan['source_questions'])
    for q in questions:
        q['quotes'] = [dict(local_block=a['local_block'], pointer=a['source_pointer'], quote=a['quote']) for a in assessments if a['local_block'] in q['local_blocks']]
        q.update(null)
    scopes = [dict(id=c['id'], pointer=f'/owner_cases/{i}', action_pointer=f'/owner_cases/{i}/input', legacy_provenance=c['provenance'], legacy_expected_pointer=f'/owner_cases/{i}/expected', legacy_comparison_pointer=f'/owner_cases/{i}/comparison', historical_role='Original D12 documentary proposal, Dpkg file-only assertion or U probe, never a measured application result. Original values unchanged.', actual_expected=None, actual_comparison=None, target='U', executed=False) for i, c in enumerate(cases)]
    return dict(role='Full retained nine-section source-only partial audit, no normative adoption or compatibility credit.', source=dict(**source, captured_utc=None, timestamp_role='Original date-only capture metadata; exact UTC unknown, not invented.'), source_scope='All 216 selected p/li/head contexts and 48 literal resources; 1137 whole-chapter blocks parsed for FILTERING ONLY. No semantic reading claim for other device sections. Whole-context judgments NOT atomic facets or full completion.', blocks=blocks, resources=[dict(r, pixels_or_destination_inspected=False, role='Literal URL/alt/caption/link text read; responsive attributes retained/hash-checked, pixels and destinations uninspected.') for r in resources], owner_requirements=req, owner_cases=cases, owner_fixtures=load(D / 'fixture-signals.json'), owner_contract_scope='Exact corrected R2 immutable as-of providers in inputs, separately approved partial. Historical pending-review prose is preserved as-of only; current disposition shared indexes. No future mutable canonical gates.', case_scope=scopes, assessments=assessments, proposals=proposals, source_questions=questions, common_future_prerequisites=plan['common_future_prerequisites'], summary=dict(selected_blocks=len(blocks), selected_by_profile=dict(counts), block_kinds=dict(Counter(b['kind'] for b in blocks)), selected_table_rows=sum(b['kind'] == 'tr' for b in blocks), selected_table_cells=sum(len(b.get('cells', [])) for b in blocks), whole_chapter_filtering_blocks=len(full), whole_context_judgments=len(assessments), atomic_facets_claimed=False, resources=len(resources), resource_kinds=dict(Counter(r['kind'] for r in resources)), owner_requirements=67, owner_cases=190, legacy_case_provenance=dict(Counter(c['provenance'] for c in cases)), proposals=10, source_questions=6, immutable_pins=len(inputs['files']), asof_providers=2, new_normative_IDs=0, new_cases=0, new_documentary_nonnull=0, actual_nonnull=0, executed=0, adoption=0, coverage_credit=0, complete_topics=0))


def guards(a):
    assert len(a['blocks']) == len(a['assessments']) == 216 and len(a['proposals']) == 10
    assert a['summary']['selected_by_profile'] == COUNTS
    for i, row in enumerate(a['assessments']):
        b = a['blocks'][i]
        assert row['id'] == f'DSA-A{i+1:03}' and row['block'] == b['id'] and row['quote'] == pointer(a, row['source_pointer']) == b['text']
        assert sha256(row['quote'].encode()).hexdigest() == row['quote_sha256']
        for key in ('represented_requirement_refs', 'represented_case_refs'):
            for ref in row[key]:
                assert pointer(a, ref['pointer'])['id'] == ref['id']
    for x in a['assessments'] + a['proposals'] + a['source_questions']:
        assert all(x[k] is None for k in ('documentary_expected', 'documentary_comparison', 'actual_expected', 'actual_comparison'))
        assert x['target'] == 'U' and x['executed'] is x['complete'] is False and x['coverage_credit'] == 0
    for i, g in enumerate(a['proposals'], 1):
        assert g['id'] == f'DSA-G{i:02}' and g['new_normative_IDs'] == []
        assert g['assessment_ids'] == [x['id'] for x in a['assessments'] if g['id'] in x['open_proposal_groups']] and g['assessment_ids']
        assert g['source_blocks'] == [x['block'] for x in a['assessments'] if g['id'] in x['open_proposal_groups']]
    by = {x['local_block']: x for x in a['assessments']}
    ids = lambda local: [r['id'] for r in by[local]['represented_case_refs']]
    assert ids('erosion:B003') == ['DST-EROSION-003', 'DST-EROSION-019']
    assert 'acceptedNoiseBlend100ENABLEDwidthmodY' in by['erosion:B003']['assessment']
    assert '003 enumerates A/B/C' in by['dynamic-tube:B003']['assessment'] and '018 separately tests every model' in by['dynamic-tube:B003']['assessment']
    assert ids('dynamic-tube:B007') == ['DST-DYNAMIC-TUBE-005'] and 'followerPATHONLY' in by['dynamic-tube:B007']['assessment']
    assert 'enumerates five waveforms' in by['roar:B047']['assessment'] and '031 actually tests' in by['roar:B047']['assessment']
    assert 'enumerates five rate modes' in by['roar:B048']['assessment']
    assert ids('roar:B021') == ['DST-ROAR-006', 'DST-ROAR-029'] and ids('roar:B036') == ['DST-ROAR-007', 'DST-ROAR-030']
    assert '007actuallyINSPECTS' in by['roar:B043']['assessment'] and 'operations missing' in by['roar:B043']['assessment']
    assert 'SUSTAININGfeedback' in by['roar:B067']['assessment'] and 'nouniversalinfinite-tailpass' in by['roar:B067']['assessment']
    assert 'BOTHFeedbackModeANDAmount' in by['roar:B080']['assessment']
    assert 'replacement' in by['roar:B081']['assessment'] and 'not a provedidentity' in by['roar:B052']['assessment']
    assert 'enumerates eight Curve Types' in by['saturator:B004']['assessment'] and '021 separately tests' in by['saturator:B004']['assessment']
    assert 'WETgain' in by['roar:B072']['assessment'] and 'nofinalmixedpeakbound' in by['roar:B072']['assessment']
    assert 'PATHonly' in by['saturator:B022']['assessment'] and 'notmainDrive0/devicebypass' in by['saturator:B022']['assessment']
    assert 'TextdoesNOTassign' in by['saturator:B018']['assessment']
    assert 'bothmodelsXY' in by['vinyl-distortion:B004']['assessment']
    g = a['proposals']
    assert 'incoming POST-Drive/distortion' in g[0]['proposed_minimal_delta'] and 'AND Boom resonance' in g[0]['proposed_future_positive_baseline']
    assert 'S1 FIRST second only' in g[1]['proposed_future_positive_baseline']
    assert '006 actual single-track AND return' in g[2]['proposed_minimal_delta'] and 'separately on the return wet output' in g[2]['proposed_future_positive_baseline']
    assert 'Preserve 007 actual Fizzle' in g[3]['proposed_minimal_delta'] and 'optional' in g[3]['proposed_minimal_delta']
    assert 'actual Blend modulation' in g[4]['proposed_minimal_delta'] and 'BOTH stages independently productive' in g[4]['proposed_future_positive_baseline']
    assert '007 inspects' in g[5]['proposed_minimal_delta'] and 'Resampling exception' in g[5]['proposed_minimal_delta'] and 'BOTH filter response AND nonlinear' in g[5]['proposed_future_positive_baseline']
    assert 'Global Mod Amount slider' in g[6]['proposed_minimal_delta'] and 'BOTH LFO and Env independently' in g[6]['proposed_future_positive_baseline']
    assert 'BOTH-controls condition' in g[7]['proposed_future_positive_baseline'] and 'BEFORE accepted MIDI' in g[7]['proposed_minimal_delta']
    assert 'slider operations as alternatives' in g[8]['proposed_minimal_delta'] and 'does not prove exact cancellation' in g[8]['proposed_future_positive_baseline']
    assert 'double-click on the Freq field' in g[9]['proposed_minimal_delta'] and 'BOTH Tracing and Pinch independently productive' in g[9]['proposed_future_positive_baseline']
    assert 'S0 is digital-zero input, NOT proof' in a['common_future_prerequisites']['zero']
    assert a['source']['captured_utc'] is None
    assert a['summary']['selected_table_rows'] == a['summary']['selected_table_cells'] == 0
    assert all(a['summary'][k] == 0 for k in ('new_normative_IDs', 'new_cases', 'actual_nonnull', 'new_documentary_nonnull', 'adoption', 'coverage_credit', 'complete_topics'))


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer, old tool/main, decode or runtime'
    inputs, plan, a = (load(P / n) for n in ('inputs.json', 'plan.json', 'audit.json'))
    watch = {R / x['path'] for x in inputs['files']} | {q for q in P.iterdir() if q.is_file()}
    before = {str(q): dg(q) for q in watch}
    assert len(inputs['files']) == len({x['path'] for x in inputs['files']}) == 89
    for x in inputs['files']:
        assert not x['path'].startswith('wiki/')
        assert dg(R / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}
    assert len([x for x in inputs['files'] if x['path'].startswith(str(D.relative_to(R)) + '/')]) == 83
    assert dg(D / 'manifest-author-r2.json')['sha256'] == '364a6ede14107e4673ee47165ed3aa4a7224f65e183658da7d5f6b1047121312'
    assert dg(D / 'manifest-author-r1.json')['sha256'] == dg(D / 'archive-r1/manifest-author-r1.json')['sha256'] == '5a75e9b74f218fb34b19dc46ad1134b63a7c4546ede9c10b379eea72262e5ade'
    for root, name, count in [(D, 'manifest-author-r2.json', 39), (D / 'archive-r1', 'manifest-author-r1.json', 38)]:
        m = load(root / name)
        assert len(m['payloads']) == count
        for pin in m['payloads']:
            assert dg(root / pin['path']) == {k: pin[k] for k in ('bytes', 'sha256')}
    for provider in inputs['canonical_snapshots']:
        assert dg(R / provider['provider']) == dict(bytes=len(provider['text'].encode()), sha256=sha256(provider['text'].encode()).hexdigest()) == {k: provider[k] for k in ('bytes', 'sha256')}
    assert a == derive(plan, inputs)
    source = Path(a['source']['path'])
    assert dg(source) == dict(bytes=588328, sha256='9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299')
    raw = source.read_text()
    for b in a['blocks']:
        assert raw[b['raw_start']:b['raw_end']] == b['raw_html']
        assert raw.count('\n', 0, b['raw_start']) + 1 == b['html_line']
        assert b['raw_start'] - raw.rfind('\n', 0, b['raw_start']) - 1 == b['html_column']
    for x in a['resources']:
        assert sha256(raw[x['raw_start']:raw.index('>', x['raw_start']) + 1].encode()).hexdigest() == x['starttag_sha256']
        assert x['pixels_or_destination_inspected'] is False
    req, cases = a['owner_requirements'], a['owner_cases']
    assert req == load(D / 'requirements.json') and cases == load(D / 'cases.json') and a['owner_fixtures'] == load(D / 'fixture-signals.json')
    assert len(req) == len({r['id'] for r in req}) == 67 and len(cases) == len({c['id'] for c in cases}) == 190
    assert Counter(r['provenance'] for r in req) == dict(D12=47, Dpkg=9, U=11)
    assert Counter(c['provenance'] for c in cases) == dict(D12=29, Dpkg=18, U=143)
    assert Counter(isinstance(c['input'], str) for c in cases) == {True: 91, False: 99}
    spec = inputs['canonical_snapshots'][0]['text']
    for r in req:
        assert r['contract'] in spec and spec.count('### ' + r['id'] + ' — ') == 1
    for i, c in enumerate(cases):
        assert c['execution'] == 'unexecuted against original and candidate'
        if c['provenance'] == 'U':
            assert c['expected'] is None
        scope = a['case_scope'][i]
        assert pointer(a, scope['pointer']) == c and pointer(a, scope['action_pointer']) == c['input']
        assert scope['actual_expected'] is scope['actual_comparison'] is None and scope['target'] == 'U' and scope['executed'] is False
    for q in a['source_questions']:
        assert len(q['quotes']) == len(q['local_blocks'])
        for quoted in q['quotes']:
            assert pointer(a, quoted['pointer']) == quoted['quote']
    guards(a)
    mutations = [('omit-source', None), ('wrong-pointer', None), ('invent-oracle', None), ('ABC-enumeration-as-selection', None), ('erase-Erosion-enabledcondition', None), ('LFO-enumeration-as-execution', None), ('Saturator-enumeration-as-execution', None), ('filter-inspection-as-operation', None), ('MIDI-Amount-only-correction', None), ('universal-drymixed-peak', None), ('invent-Color-axis', None), ('invent-captureUTC', None)]
    mutations += [(name, (i, key, 'Enabled flags only')) for name, i, key in [('incoming-path-missing', 0, 'proposed_future_positive_baseline'), ('asymmetric-Erosion-source', 1, 'proposed_future_positive_baseline'), ('unproductive-return', 2, 'proposed_future_positive_baseline'), ('Fizzle-all-missing', 3, 'proposed_minimal_delta'), ('one-stage-Blend', 4, 'proposed_future_positive_baseline'), ('filter-only-order', 5, 'proposed_future_positive_baseline'), ('one-modsource-zero', 6, 'proposed_future_positive_baseline'), ('MIDI-no-manual-positive', 7, 'proposed_minimal_delta'), ('Color-exact-inverse', 8, 'proposed_future_positive_baseline'), ('Vinyl-one-model', 9, 'proposed_future_positive_baseline')]]
    rejected = []
    targets = {'ABC-enumeration-as-selection': 'dynamic-tube:B003', 'erase-Erosion-enabledcondition': 'erosion:B003', 'LFO-enumeration-as-execution': 'roar:B047', 'Saturator-enumeration-as-execution': 'saturator:B004', 'filter-inspection-as-operation': 'roar:B043', 'MIDI-Amount-only-correction': 'roar:B080', 'universal-drymixed-peak': 'roar:B072', 'invent-Color-axis': 'saturator:B018'}
    for name, change in mutations:
        t = deepcopy(a)
        if change:
            i, key, value = change; t['proposals'][i][key] = value
        elif name == 'omit-source':
            t['assessments'].pop()
        elif name == 'wrong-pointer':
            t['assessments'][1]['source_pointer'] = '/blocks/2/text'
        elif name == 'invent-oracle':
            t['proposals'][0]['actual_expected'] = 'pass'
        elif name == 'invent-captureUTC':
            t['source']['captured_utc'] = '2026-10-19T00:00:00Z'
        else:
            next(x for x in t['assessments'] if x['local_block'] == targets[name])['assessment'] = 'A named control proves all actual operations and audio laws.'
        try:
            guards(t)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Unsafe mutation accepted: ' + name)
    bs, rs = parser()('<p>Outside</p><div id="chapter_content"><h1 id="r">Root</h1><div><h2 id="roar">Roar</h2><h3 id="route">Route</h3><p>Two stages, unless disabled.</p><ul><li>Positive before zero.</li></ul><table><tr><td>One</td><td>Two</td></tr></table><img alt="" src="unopened"><figcaption>Caption.</figcaption></div></div><p>After</p>', 'TEST')
    assert [b['kind'] for b in bs] == ['h1', 'h2', 'h3', 'p', 'li', 'tr'] and bs[-1]['cells'][1]['text'] == 'Two' and [r['kind'] for r in rs] == ['image', 'caption']
    links = 0
    for url in re.findall(r'\]\(([^)]+)\)', (P / 'README.md').read_text()):
        target = P / url.split('#')[0]
        assert target.exists() or (url == 'manifest.json' and not (P / 'manifest.json').exists()), url
        links += 1
    for q in P.iterdir():
        if q.is_file():
            data = q.read_bytes()
            assert data.endswith(b'\n') and b'\0' not in data and all(line.rstrip(b' \t') == line for line in data.splitlines())
    if (P / 'manifest.json').exists():
        manifest = load(P / 'manifest.json')
        assert set(manifest['files']) == {q.name for q in P.iterdir() if q.is_file()} - {'manifest.json'}
        assert len(manifest['files']) == 5
        for name, pin in manifest['files'].items():
            assert dg(P / name) == pin
    assert before == {str(q): dg(q) for q in watch}
    print(json.dumps(dict(status='pass', sealed=(P / 'manifest.json').exists(), summary=a['summary'], negative_fixtures=rejected, parser_table_boundary_fixture=True, links=links, watched_paths=len(watch), all_unchanged=True, writes=False, old_mains_decodes_runtime=False), indent=2))


if __name__ == '__main__':
    main()
