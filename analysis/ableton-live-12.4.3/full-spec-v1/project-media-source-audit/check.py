"""Read-only retained Project source reconciliation. No old tools, live app or writes."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json, re, sys
A = Path(__file__).resolve().parent
R = A.parents[3]
O = A.parent / 'project-media'
SECTIONS = {'live-sets', 'live-projects', 'locating-missing-files', 'collecting-external-files', 'finding-unused-files', 'packing-projects-into-packs', 'file-management-faqs'}
def j(p):
    return json.loads(p.read_text())
def dg(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())
def ptr(v, path):
    assert path.startswith('/')
    for key in path.split('/')[1:]:
        if isinstance(v, list):
            assert re.fullmatch(r'0|[1-9][0-9]*', key)
            v = v[int(key)]
        else:
            v = v[key.replace('~1', '/').replace('~0', '~')]
    return v
def primary(inp):
    parser = R / inp['parser']
    assert dg(parser) == inp['files'][inp['parser']]
    assert dg(parser)['sha256'] == '648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
    env = {}
    exec(compile(parser.read_text(), str(parser), 'exec'), env)
    raw = (O / 'manual-files-2026-10-19.html').read_text()
    whole, resources = env['extract'](raw, 'FILES')
    chosen = [b for b in whole if any(h['level'] == 2 and h['anchor'] in SECTIONS for h in b['heading_context'])]
    resources = [q for q in resources if q['raw_start'] >= chosen[0]['raw_start']]
    assert len(whole) == 216 and len(chosen) == 132 and len(resources) == 83
    return chosen, resources
def catalog():
    req, cases = [], []
    for line, text in enumerate((A / 'spec-asof.md').read_text().splitlines(), 1):
        cells = [c.strip() for c in text.strip('|').split('|')]
        if text.startswith('| REQ-PROJECT-MEDIA-'):
            assert len(cells) == 4
            req.append(dict(id=cells[0], preconditions=cells[1], documented_predicate=cells[2], provenance_source=cells[3], source_line=line, markdown=text))
        elif text.startswith('| PMW-'):
            assert len(cells) == 5
            cases.append(dict(id=cells[0], requirements=['REQ-PROJECT-MEDIA-' + cells[1]], kind=cells[2], setup_and_action=cells[3], documentary_comparator=cells[4], source_line=line, markdown=text, actual_expected=None, actual_comparison=None, target='U', executed=False))
    assert len(req) == 22 and len(cases) == 34
    return req, cases
def build(plan, inp):
    blocks, resources = primary(inp)
    req, cases = catalog()
    assessments = []
    for i, block in enumerate(blocks):
        row = plan['judgments'][block['id']]
        rr = [dict(path=str((A / 'audit.json').relative_to(R)), pointer=f'/owner_requirements/{n}', id=r['id'], body_pointer=f'/owner_requirements/{n}/documented_predicate') for n, r in enumerate(req) if r['id'] in row['selected_requirements']]
        cc = [dict(path=str((A / 'audit.json').relative_to(R)), pointer=f'/owner_cases/{n}', id=c['id'], action_pointer=f'/owner_cases/{n}/setup_and_action') for n, c in enumerate(cases) if any(r in row['selected_requirements'] for r in c['requirements'])]
        assert [r['id'] for r in rr] == row['selected_requirements']
        assessments.append(dict(id=f'PMSA-A{i+1:03}', block=block['id'], source_pointer=f'/blocks/{i}', quote=block['text'], quote_sha256=sha256(block['text'].encode()).hexdigest(), scope='Manual WHOLE context, grouped note; not atomic facets or all qualifiers covered.', **{k:row[k] for k in ['assessment', 'disposition', 'proposal_groups']}, requirement_refs=rr, case_refs=cc, documentary_expected=None, documentary_comparison=None, actual_expected=None, actual_comparison=None, target='U', executed=False, complete=False, coverage_credit=0))
    proposals = deepcopy(plan['proposals'])
    for g in proposals:
        g['assessment_ids'] = [q['id'] for q in assessments if g['id'] in q['proposal_groups']]
    return dict(role='Analyst source-only reconciliation; no normative adoption', source=j(O/'source.json'), blocks=blocks, resources=resources, owner_requirements=req, owner_cases=cases, owner_fixtures=j(O/'fixtures.json'), canonical_asof=inp['canonical_asof'], assessments=assessments, proposals=proposals, source_questions=plan['source_questions'], common_future_prerequisites=plan['common_future_prerequisites'], summary=dict(whole_chapter_blocks_FILTERING_ONLY=216, selected_contexts=132, block_kinds=dict(Counter(b['kind'] for b in blocks)), resources=83, resource_kinds=dict(Counter(q['kind'] for q in resources)), requirements=22, cases=34, old_documentary_bounded=30, old_wholly_ungraded=4, actual_null_U=34, proposals=20, questions=8, immutable_pins=8, old_packet_files=6, atomic_facets=False, new_normative_IDs=0, new_cases=0, adoptions=0, coverage_credit=0, complete=False))
GUARDS = {
    'FILES:B094': ['004 actually chooses', '005 actually selects', 'up/down-plus-Enter'],
    'FILES:B100': ['008 actually unfolds', 'Devices icon', 'does not actually drag'],
    'FILES:B105': ['009 actually exports', 'already selected'],
    'FILES:B116': ['013/014/015 actually replace', 'audio-clip-only', 'same-or-longer', 'same-only'],
    'FILES:B118': ['016 genuinely engages Edit', '017 actually changes', 'Sample-only'],
    'FILES:B150': ['022 actually searches', 'independently established criteria', 'not all named actions'],
    'FILES:B172': ['026 genuinely exports', '027 actually chooses', '028 actually Cancel', 'Ask/DontCopy is missing'],
    'FILES:B183': ['029 genuinely inspects', 'project-local unused'],
    'FILES:B195': ['030 actually packs', 'Lossless/up-to50percent', 'no ALP bytes'],
    'FILES:B207': ['onecopy shared samples', 'no hash dedup'],
    'FILES:B215': ['FullyRescanFolders', 'absent from018/022-025']}
def semantic(plan, audit):
    assert len(plan['judgments']) == len(audit['assessments']) == 132
    by = {q['block']:q for q in audit['assessments']}
    for key, phrases in GUARDS.items():
        assert by[key]['assessment'] == plan['judgments'][key]['assessment']
        assert all(p in by[key]['assessment'] for p in phrases), key
    assert len(audit['proposals']) == 20 and len(audit['source_questions']) == 8
    for q in audit['assessments'] + audit['proposals']:
        assert all(q[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
        assert q['target'] == 'U' and not q['complete'] and not q['executed'] and q['coverage_credit'] == 0
    for g in audit['proposals']:
        assert g['new_normative_IDs'] == [] and 'NONEMPTY' in g['proposed_future_positive_baseline'] and g['assessment_ids']
    assert 'BOTH independent' in audit['common_future_prerequisites'] and 'EACH' in audit['common_future_prerequisites']
    assert all(c['actual_expected'] is c['actual_comparison'] is None and c['target'] == 'U' and not c['executed'] for c in audit['owner_cases'])
    assert audit['source']['captured_utc'] == '2026-10-19T20:07:46.423249+00:00'
    return True
def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; unsupported args refused before inputs'
    inp, plan, audit = j(A/'inputs.json'), j(A/'plan.json'), j(A/'audit.json')
    watch = {R/p for p in inp['files']} | {p for p in A.iterdir() if p.is_file()}
    before = {str(p):dg(p) for p in watch}
    for p, row in inp['files'].items():
        assert dg(R/p) == row, p
    for row in inp['canonical_asof'].values():
        assert dg(A/row['provider']) == {k:row[k] for k in ['bytes','sha256']}
    old = j(O/'manifest.json')
    for row in old['files']:
        path = row['path']
        provider = A/inp['canonical_asof'][path]['provider'] if path in inp['canonical_asof'] else R/path
        assert dg(provider) == {k:row[k] for k in ['bytes','sha256']}
    assert audit == build(plan, inp)
    semantic(plan, audit)
    derefs = 0
    for q in audit['assessments']:
        b = ptr(audit, q['source_pointer'])
        assert b['id'] == q['block'] and b['text'] == q['quote']
        for ref in q['requirement_refs'] + q['case_refs']:
            assert (R/ref['path']).resolve() == (A/'audit.json').resolve()
            obj = ptr(audit, ref['pointer'])
            assert obj['id'] == ref['id']
            field = 'body_pointer' if 'body_pointer' in ref else 'action_pointer'
            assert ptr(audit, ref[field]) == obj['documented_predicate' if field == 'body_pointer' else 'setup_and_action']
            derefs += 1
    rejected = []
    for key in GUARDS:
        p, a = deepcopy((plan, audit))
        p['judgments'][key]['assessment'] = next(q for q in a['assessments'] if q['block'] == key)['assessment'] = 'All source gestures already fully tested and pass'
        try:
            semantic(p,a)
        except AssertionError:
            rejected.append(key)
        else:
            raise AssertionError('Unsafe joint judgment accepted ' + key)
    for name, change in [('new-oracle',lambda a:a['proposals'][0].update(actual_expected='pass')), ('no-positive',lambda a:a['proposals'][0].update(proposed_future_positive_baseline='selected flag')), ('target-promoted',lambda a:a['owner_cases'][0].update(actual_expected='pass')), ('wrong-date',lambda a:a['source'].update(captured_utc=None))]:
        a = deepcopy(audit)
        change(a)
        try:
            semantic(plan,a)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Unsafe variant accepted ' + name)
    for path in ['/owner_cases/-1', '/cases/0', '/owner_cases/999']:
        try:
            ptr(audit,path)
        except (AssertionError,KeyError,IndexError):
            rejected.append(path)
        else:
            raise AssertionError('Invalid reference accepted ' + path)
    sealed = (A/'manifest.json').exists()
    if sealed:
        m = j(A/'manifest.json')
        assert set(m['files']) == {p.name for p in A.iterdir() if p.is_file() and p.name != 'manifest.json'}
        for name,row in m['files'].items():
            assert dg(A/name) == row, name
    assert before == {str(p):dg(p) for p in watch}
    print(json.dumps(dict(status='pass',sealed=sealed,contexts=132,resources=83,requirements=22,cases=34,proposals=20,questions=8,actual_null_U=34,source_and_action_refs=derefs,negative_fixtures_rejected=rejected,input_pins=8,old_files_exact=6,watched_unchanged=len(watch),writes=False,adoptions=0,complete=False,independent_review='pending as of author freeze'),indent=2))
if __name__ == '__main__':
    main()
