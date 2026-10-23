"""Read-only bounded Distortion owner successor. No old tool/main/parser/decoder/replay."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json
import re
import sys

D = Path(__file__).resolve().parent
F = D.parent
R = F.parents[2]
A = F / 'distortion-source-audit'
NEW = ['research-before-owner-r3.md', 'cases-r3.json', 'actual-overlay-r3.json', 'adoption-r3.json', 'consumer-history-r3.json', 'inputs-r3.json', 'spec-r3.md', 'research-owner-r3.md', 'delta-r3.json', 'check-r3.py', 'README-r3.md']


def load(q):
    return json.loads(q.read_text())


def path(s):
    return Path(s) if Path(s).is_absolute() else R / s


def dg(q):
    b = q.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())


def ptr(v, route):
    for k in route.strip('/').split('/') if route else []:
        k = k.replace('~1', '/').replace('~0', '~')
        try:
            v = v[int(k)] if isinstance(v, list) else v[k]
        except (ValueError, IndexError, KeyError, TypeError):
            raise AssertionError('Invalid actual JSON pointer: ' + route) from None
    return v


def refs(cases, overlay, adoption):
    assert isinstance(cases, list) and len(cases) == 200
    assert len(overlay['cases']) == len({x['id'] for x in overlay['cases']}) == 200
    assert len(adoption['groups']) == len({x['case_id'] for x in adoption['groups']}) == 10
    for x in overlay['cases']:
        assert x['catalog'] == 'cases-r3.json' and ptr(cases, x['case_pointer'])['id'] == x['id']
    for x in adoption['groups']:
        assert x['catalog'] == 'cases-r3.json' and ptr(cases, x['case_pointer'])['id'] == x['case_id']
    assert {x['id'] for x in overlay['cases']} == {c['id'] for c in cases}
    assert {x['case_id'] for x in adoption['groups']} == {c['id'] for c in cases[190:]}


def guards(cases, overlay, adoption, audit):
    assert cases[:190] == load(D / 'cases.json') and len({c['id'] for c in cases}) == 200
    refs(cases, overlay, adoption)
    req = {r['id'] for r in load(D / 'requirements.json')}
    assert len(req) == 67 and adoption['new_normative_IDs'] == [] and adoption['complete_profiles'] == 0
    assert Counter(c['provenance'] for c in cases[:190]) == dict(D12=29, Dpkg=18, U=143)
    for i, c in enumerate(cases):
        assert c['requirement'] in req and c['execution'] == 'unexecuted against original and candidate'
        o = overlay['cases'][i]
        assert o['id'] == c['id'] and o['actual_expected'] is o['actual_comparison'] is None and o['target'] == 'U' and o['executed'] is False
    for i, (c, g) in enumerate(zip(cases[190:], adoption['groups']), 190):
        assert c['audit_group'] == g['audit_group'] == f'DSA-G{i-189:02}'
        assert c['id'] == g['case_id'] and c['requirements'] == g['requirements'] and set(c['requirements']) <= req
        assert c['expected'] is c['comparison'] is c['documentary_expected'] is c['documentary_comparison'] is None
        assert c['provenance'] == 'U' and c['exact_target_applicability'] == 'unknown'
        assert c['input'] and c['positive_baseline'] and c['limits']
        assert len(g['selected_source_blocks']) == len(g['selected_source_pointers']) == len(c['source_blocks'])
        for ident, loc, local in zip(g['selected_source_blocks'], g['selected_source_pointers'], c['source_blocks']):
            b = next(b for b in audit['blocks'] if b['id'] == ident)
            assert ptr(audit, loc) == b['text']
            assert next(x for x in audit['assessments'] if x['block'] == ident)['local_block'] == local
    by = {c['audit_group']: c for c in cases[190:]}
    def has(g, key, *tokens):
        assert all(t in by[f'DSA-G{g:02}'][key] for t in tokens), (g, tokens)
    has(1, 'input', 'Observe the Bass Meter', 'at Boom0', 'at accepted Boom>0')
    has(1, 'positive_baseline', 'Incoming POST-Drive/distortion lows AND resonant contribution independently productive')
    has(2, 'input', 'accepted Blend100/enabled Filter Width BEFORE modifier-Y', 'ONLY S1 first-second segment:1second500Hz peak0.1 identical L/R phase0', 'never its asymmetric/opposite later segments')
    has(2, 'limits', 'inactive gesture remains005U', 'modern/Legacy parity')
    has(3, 'input', 'actually edit', 'slider boxes', 'Preserve006 single-track AND isolated-return')
    has(3, 'positive_baseline', 'separately on the return wet output', 'displayed amount alone is not return efficacy')
    has(4, 'input', 'optional separate reset examples', 'right-most offered position')
    has(4, 'limits', 'Recipes remain optional', 'remain pending')
    has(5, 'input', 'Half Wave Rectifier and Fractal', 'actually modulate Blend', 'rather than merely selecting endpoints')
    has(5, 'positive_baseline', 'BOTH stages independently productive', 'modulation source/route must independently produce response')
    has(6, 'input', 'do NOT actually change gain-stage Filter Frequency', 'explicitly actually edit the gain-stage Filter Frequency control', 'Resonance except Resampling', 'Filter Peak Gain only in Peak', 'Morph only in Morph')
    has(6, 'positive_baseline', 'EACH selected filter/control and nonlinear Shaper independently productive', 'Analysis Frequency and feedback Filter Frequency are separate controls', 'baseline alone is not a Frequency gesture')
    has(7, 'input', 'actually click', 'drag the selected cell vertically', 'Global Modulation Amount')
    has(7, 'positive_baseline', 'BOTH LFO1 AND Env independently produce response', 'NONZERO depth/effect')
    has(8, 'input', 'MIDI sidechain off', 'select Note mode explicitly', 'BOTH Feedback Mode AND Feedback Amount', 'actually receive supported independent notes')
    has(8, 'positive_baseline', 'EACH manual control independently productive', 'genuine NONZERO sustaining feedback first')
    has(9, 'input', 'Amt Lo, Amt Hi, Frequency and Width slider controls', 'Do not invent the unspecified display-axis mapping')
    has(9, 'limits', 'not exact cancellation', 'arbitrary dry mixture')
    has(10, 'input', 'EACH model actually double-click its Freq field and type', 'Retain003 actual X/Y')
    has(10, 'positive_baseline', 'BOTH Tracing and Pinch independently productive', 'actual generator-positive history, not S0 alone')
    old = {c['id']: c for c in cases[:190]}
    assert 'Noise Blend=100%' in old['DST-EROSION-003']['input'] and 'Filter Width is enabled' in old['DST-EROSION-003']['input']
    assert 'only S1 first-second segment' in old['DST-EROSION-006']['input'] and 'Do not use S1 second/third seconds' in old['DST-EROSION-006']['input']
    assert old['DST-ROAR-007']['input'] == 'Select each of nine filters; inspect Resonance, Peak Gain and Morph; toggle Pre.'
    assert 'filter-sensitive and nonlinear baselines' in old['DST-ROAR-030']['input']


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer/old tool/main/replay/decode'
    inputs = load(D / 'inputs-r3.json')
    own = {q for q in D.rglob('*') if q.is_file()}
    wiki = {R / x['canonical'] for x in inputs['canonical_before']}
    watch = {path(x['path']) for x in inputs['files']} | own | wiki
    before = {str(q): dg(q) for q in watch}
    assert len(inputs['files']) == len({x['path'] for x in inputs['files']}) == 103 and len(inputs['old_owner_files']) == 83
    for x in inputs['files']:
        assert not x['path'].startswith('wiki/')
        assert dg(path(x['path'])) == {k: x[k] for k in ('bytes', 'sha256')}, x['path']
    assert dg(path(inputs['corrected_source_review']['path']))['sha256'] == '16b67c516a1ee16ac0ec079d2553734bd798062ed154c68cc3d9aea6b7df9d1c'
    for root, name, count in [(D, 'manifest-author-r2.json', 39), (D / 'archive-r1', 'manifest-author-r1.json', 38)]:
        m = load(root / name); assert len(m['payloads']) == count
        for x in m['payloads']:
            assert dg(root / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}
    assert dg(D / 'research-before-owner-r3.md') == dict(bytes=10548, sha256='fba1f6a0b0d01d48e1760455b3ddad1ad7265cfeedccecbe330d1cebb3de3e1c')
    audit = load(A / 'audit.json')
    correction = load(A / 'response-r2.json')
    assert len(correction['changes']) == 4
    # Explicit current two-field audit view; no old helper/main/parser imports.
    for i, container, key in [(0, audit['assessments'][136], 'assessment'), (2, audit['proposals'][5], 'proposed_minimal_delta')]:
        assert container[key] == correction['changes'][i]['before']
        container[key] = correction['changes'][i]['after']
    assert 'documented-but-unexercised/U' in audit['proposals'][5]['proposed_minimal_delta']
    cases, overlay, adoption = (load(D / n) for n in ['cases-r3.json', 'actual-overlay-r3.json', 'adoption-r3.json'])
    guards(cases, overlay, adoption, audit)
    raw = path(audit['source']['path']).read_text()
    for g in adoption['groups']:
        for ident in g['selected_source_blocks']:
            b = next(b for b in audit['blocks'] if b['id'] == ident)
            assert raw[b['raw_start']:b['raw_end']] == b['raw_html']
    links = 0
    for page in load(D / 'delta-r3.json')['pages']:
        text = (D / page['original_provider']).read_text()
        for e in page['replacements']:
            assert text.count(e['before']) == e['occurrences'] == 1
            text = text.replace(e['before'], e['after'], 1)
        text += page['append']
        assert text == (D / page['current_snapshot']).read_text() == (R / page['canonical']).read_text()
        for url in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'https?://', url): continue
            target = (R / page['canonical']).parent / url.split('#')[0]
            assert target.exists() or (target.name == 'manifest-author-r3.json' and not (D / 'manifest-author-r3.json').exists()), url
            links += 1
    spec = (D / 'spec-r3.md').read_text(); req = load(D / 'requirements.json')
    assert len(req) == 67 and all(r['contract'] in spec for r in req)
    ids = set(re.findall(r'^###\s+(REQ-[A-Z0-9-]+)(?:\s|$)', spec, re.M)) | set(re.findall(r'^\|\s*(REQ-[A-Z0-9-]+)\s*\|', spec, re.M))
    assert ids == {r['id'] for r in req} and len(ids) == 67
    history = load(D / 'consumer-history-r3.json'); assert len(history['occurrences']) == 5
    for x in history['occurrences']:
        assert dg(path(x['path'])) == x['file_pin'] and ptr(load(path(x['path'])), x['json_pointer']) == x['value']
    rejected = []
    # Actual-reference fixtures reject even if overlay/adoption prefixes agree.
    for name in ['joint-cases-prefix', 'wrong-valid-index', 'missing-overlay', 'duplicate-overlay', 'missing-adoption', 'duplicate-adoption', 'out-of-range-overlay', 'out-of-range-adoption']:
        ov, ad = deepcopy(overlay), deepcopy(adoption)
        if name == 'joint-cases-prefix':
            for x in ov['cases'] + ad['groups']: x['case_pointer'] = '/cases' + x['case_pointer']
        elif name == 'wrong-valid-index': ov['cases'][190]['case_pointer'] = '/0'
        elif name == 'missing-overlay': ov['cases'].pop()
        elif name == 'duplicate-overlay': ov['cases'][-1] = deepcopy(ov['cases'][0])
        elif name == 'missing-adoption': ad['groups'].pop()
        elif name == 'duplicate-adoption': ad['groups'][-1] = deepcopy(ad['groups'][0])
        elif name == 'out-of-range-overlay': ov['cases'][0]['case_pointer'] = '/200'
        else: ad['groups'][0]['case_pointer'] = '/200'
        try: refs(cases, ov, ad)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('Invalid references accepted: ' + name)
    variants = [('old-case-mutation', None), ('new-doc-oracle', None), ('actual-file-grade', None), ('wrong-source-pointer', None)]
    variants += [(name, (g, key)) for name, g, key in [('one-low-path', 1, 'positive_baseline'), ('disabled-Erosion-modifier', 2, 'input'), ('asymmetric-Erosion-source', 2, 'input'), ('slider-inspection-only', 3, 'input'), ('unproductive-return', 3, 'positive_baseline'), ('mandatory-recipe', 4, 'limits'), ('Blend-endpoints-only', 5, 'input'), ('one-stage-only', 5, 'positive_baseline'), ('baseline-promoted-to-Frequency', 6, 'input'), ('analysis-Frequency-substitution', 6, 'positive_baseline'), ('Resampling-Resonance-invention', 6, 'input'), ('filter-only-positive', 6, 'positive_baseline'), ('one-modsource-before-zero', 7, 'positive_baseline'), ('feedback-flag-before-absence', 8, 'positive_baseline'), ('repair-MIDI-both-controls', 8, 'input'), ('Color-exact-inverse', 9, 'limits'), ('one-Vinyl-model', 10, 'input'), ('S0-proves-no-generator', 10, 'positive_baseline')]]
    for name, edit in variants:
        cs, ov, ad = deepcopy(cases), deepcopy(overlay), deepcopy(adoption)
        if name == 'analysis-Frequency-substitution':
            cs[195]['input'] = cs[195]['input'].replace('gain-stage Filter Frequency control', 'analysis Frequency control')
        elif name == 'Resampling-Resonance-invention':
            cs[195]['input'] = cs[195]['input'].replace('Resonance except Resampling', 'Resonance including Resampling')
        elif name == 'repair-MIDI-both-controls':
            cs[197]['input'] = cs[197]['input'].replace('BOTH Feedback Mode AND Feedback Amount', 'Feedback Amount only')
        elif name == 'Color-exact-inverse':
            cs[198]['limits'] = cs[198]['limits'].replace('not exact cancellation', 'exact cancellation')
        elif name == 'mandatory-recipe':
            cs[193]['limits'] = cs[193]['limits'].replace('Recipes remain optional', 'Recipes are mandatory for every input')
        elif edit:
            g, key = edit; cs[189 + g][key] = 'Enabled flag or a different source control proves all actions'
        elif name == 'old-case-mutation': cs[0]['input'] = 'Different old action'
        elif name == 'new-doc-oracle': cs[190]['documentary_expected'] = 'equal'
        elif name == 'actual-file-grade': ov['cases'][0]['actual_expected'] = 'source-byte pass'
        else: ad['groups'][0]['selected_source_pointers'][0] = '/blocks/0/text'
        try: guards(cs, ov, ad, audit)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('Unsafe source/action mutation accepted: ' + name)
    for name in NEW:
        data = (D / name).read_bytes()
        assert data.endswith(b'\n') and b'\0' not in data and all(x.rstrip(b' \t') == x for x in data.splitlines()), name
    for url in re.findall(r'\]\(([^)]+)\)', (D / 'README-r3.md').read_text()):
        target = D / url.split('#')[0]
        assert target.exists() or (url == 'manifest-author-r3.json' and not target.exists()), url
        links += 1
    seal = D / 'manifest-author-r3.json'
    if seal.exists():
        m = load(seal); assert len(m['files']) == 94
        assert set(m['files']) == {str(q.relative_to(D)) for q in D.rglob('*') if q.is_file()} - {seal.name}
        for name, pin in m['files'].items(): assert dg(D / name) == pin, name
    assert before == {str(q): dg(q) for q in watch}
    print(json.dumps(dict(status='pass', sealed=seal.exists(), old_files_preserved=83, immutable_inputs=103, unchanged_requirements=67, old_cases_preserved=190, new_null_U_cases=10, current_cases=200, actual_case_refs_dereferenced=200, adoption_refs_dereferenced=10, source_groups_bounded=10, current_actual_all_null_U=True, browser_IDs=67, consumer_occurrences=5, direct_external_old_spec_pins=1, negative_fixtures=rejected, links=links, watched_paths=len(watch), all_unchanged=True, writes=False, old_tools_replays_decodes_runtime=False), indent=2))


if __name__ == '__main__': main()
