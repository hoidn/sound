"""Read-only bounded R3 owner checks. No historical main/parser/decoder/replay."""
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
A = F / 'modulation-pitch-loop-source-audit'
NEW = ['cases-r3.json', 'actual-overlay-r3.json', 'adoption-r3.json', 'consumer-history-r3.json', 'inputs-r3.json', 'spec-r3.md', 'research-r3.md', 'delta-r3.json', 'check-r3.py', 'README-r3.md']


def load(q):
    return json.loads(q.read_text())


def path(s):
    return Path(s) if Path(s).is_absolute() else R / s


def dg(q):
    b = q.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())


def pointer(v, s):
    for k in s.strip('/').split('/') if s else []:
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def guards(cases, overlay, ledger, audit):
    old = load(D / 'cases.json')
    assert len(cases) == 208 and cases[:186] == old and len({c['id'] for c in cases}) == 208
    assert len(ledger['groups']) == 22 and ledger['requirements_unchanged'] == 106
    assert len(overlay['cases']) == 208
    req = {r['id'] for r in load(D / 'requirements.json')}
    for i, c in enumerate(cases):
        assert set(c['requirements']) <= req and c['expected'] is None and c['target_grade'] == 'U' and c['executed'] is False
        o = overlay['cases'][i]
        assert o['id'] == c['id'] and o['case_pointer'] == f'/cases/{i}' and o['catalog'] == 'cases-r3.json'
        assert o['actual_expected'] is o['actual_comparison'] is None and o['target'] == 'U' and o['executed'] is False
    for i, (g, c, route) in enumerate(zip(audit['proposals'], cases[186:], ledger['groups']), 186):
        assert c['audit_group'] == route['audit_group'] == g['id']
        assert route['case_id'] == c['id'] and route['case_pointer'] == f'/cases/{i}'
        assert c['requirements'] == g['route_to_existing_requirements']
        assert c['source_blocks'] == [audit['local_owner_block_crosswalk'][b] for b in g['source_blocks']]
        assert route['source_blocks'] == g['source_blocks']
        assert c['documentary_expected'] is c['documentary_comparator'] is c['actual_comparison'] is None
        assert c['preconditions'] == ['common-setup', 'positive-signal-guard']
        assert c['setup_and_action'] and c['positive_baseline'] and c['limits']
        for block, loc in zip(route['source_blocks'], route['source_pointers']):
            assert len(route['source_blocks']) == len(route['source_pointers'])
            b = next(b for b in audit['blocks'] if b['id'] == block)
            assert pointer(audit, loc) == b['text']
    by = {c['audit_group']: c for c in cases[186:]}
    def has(group, key, *tokens):
        assert all(t in by[f'MPLA-G{group:02}'][key] for t in tokens), (group, tokens)
    has(1, 'setup_and_action', 'Phase to180', 'Synced/Dotted/Triplet/16th', 'only where admitted, negative Shape')
    has(3, 'setup_and_action', 'first establish productive received-note full-wet processing, then clear latch/release history and remove notes', 'Mono', 'Poly2/4/8')
    has(3, 'positive_baseline', 'BOTH distinguishable notes and EACH tap independently productive')
    has(4, 'setup_and_action', 'four targets and six named', 'isolate other sources', 'Reset On', 'MIDI Off/Quantizer')
    has(5, 'setup_and_action', 'correction-inactive', 'Formant Follow', 'before Amount0')
    has(6, 'setup_and_action', 'Rate with its dial', 'drag vertically in the display', 'Auto versus an offered fixed')
    has(7, 'positive_baseline', 'BOTH independent main LFO and LFO2')
    has(8, 'positive_baseline', 'BEFORE EACH disabled/zero', 'unrelated LFO response is insufficient')
    has(9, 'setup_and_action', 'Internal', 'Coarse AND Fine', 'BEFORE reset to Spread0', 'literal offered Delay free-unit')
    has(9, 'limits', 'Hertz remains unresolved', 'no ms or reciprocal repair')
    has(11, 'positive_baseline', 'Mono overrides shared Poly16', 'cleared histories and dry exclusion')
    has(12, 'setup_and_action', 'negative Stretch', 'Internal', 'MIDI pitch contexts')
    has(13, 'positive_baseline', 'EACH tested voice contribution', 'remain U')
    has(14, 'positive_baseline', 'BOTH devices AND BOTH MIDI paths', 'Empty recognition result')
    has(15, 'positive_baseline', 'Genuine observed nonzero frozen audio BEFORE', 'BOTH old/new captures')
    has(15, 'limits', 'X-Fade ms/percentage stays U', 'no duration equation')
    has(16, 'setup_and_action', 'Frz>Dly and Dly>Frz resets', 'Delay repetitions independently')
    has(17, 'setup_and_action', 'drag X left and Y down', 'select sawtooth', 'each offered pulse')
    has(18, 'setup_and_action', 'BOTH Range sliders and BW', 'click an independently active band', 'change Level and Attack/Release')
    has(19, 'positive_baseline', 'BOTH carrier/modulator and EACH channel independently productive', 'before Solo')
    has(20, 'setup_and_action', 'Repeat Off', 'Chance100 BEFORE Chance0', 'actually disable Repeat', 'before resetting0')
    has(21, 'positive_baseline', 'observed nonzero content BEFORE Clear')
    has(21, 'limits', 'stopped-Overdub choice', 'Link protocol')
    has(22, 'positive_baseline', 'actual NONZERO loop AND productive inserted-effect return')
    has(22, 'setup_and_action', 'BOTH Insert-Looper taps', 'BEFORE the separate Play no-effect', 'enter MIDI Map Mode')
    assert ledger['all_new_documentary_and_actual_oracles_null'] is True and ledger['execution'] is False and ledger['complete_profiles'] == 0


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer, old tools, decode or replay'
    ins = load(D / 'inputs-r3.json')
    own = [q for q in D.rglob('*') if q.is_file()]
    wiki = [R / s['canonical'] for s in ins['canonical_before']]
    watch = {path(x['path']) for x in ins['files']} | set(own) | set(wiki)
    before = {str(q): dg(q) for q in watch}
    assert len(ins['files']) == len({x['path'] for x in ins['files']}) == 130
    assert len(ins['old_owner_files']) == 107
    for x in ins['files']:
        assert not x['path'].startswith('wiki/')
        assert dg(path(x['path'])) == {k: x[k] for k in ('bytes', 'sha256')}, x['path']
    assert dg(A / 'manifest.json')['sha256'] == '4ce18825d70d78d8ad3d5aa1d5a0ae0486b4d3e250403b63719c95e5c149d499'
    assert dg(path(ins['source_audit_review']['path']))['sha256'] == '9a1edc1682a361add55ddf5753059e879741ae1fc2e4b00c64fbbba649a573a2'
    for root, name, count in [(D, 'manifest-author-r2.json', 51), (D / 'archive-r1', 'manifest-author-r1.json', 49)]:
        m = load(root / name)
        assert len(m['files']) == count
        for filename, pin in m['files'].items():
            assert dg(root / filename) == pin
    cases, overlay, ledger = (load(D / name) for name in ['cases-r3.json', 'actual-overlay-r3.json', 'adoption-r3.json'])
    audit = load(A / 'audit.json')
    guards(cases, overlay, ledger, audit)
    raw = path(audit['source']['path']).read_text()
    for g in ledger['groups']:
        for ident, loc in zip(g['source_blocks'], g['source_pointers']):
            b = next(b for b in audit['blocks'] if b['id'] == ident)
            assert pointer(audit, loc) == b['text'] and raw[b['raw_start']:b['raw_end']] == b['raw_html']
    delta = load(D / 'delta-r3.json')
    req = load(D / 'requirements.json')
    links = 0
    for page in delta['pages']:
        previous = (D / page['original_provider']).read_text()
        for edit in page['replacements']:
            assert edit['occurrences'] == previous.count(edit['before']) == 1
            previous = previous.replace(edit['before'], edit['after'], 1)
        current = previous + page['append']
        assert current == (D / page['current_snapshot']).read_text() == (R / page['canonical']).read_text()
        for url in re.findall(r'\]\(([^)]+)\)', current):
            if re.match(r'https?://', url):
                continue
            target = (R / page['canonical']).parent / url.split('#')[0]
            assert target.exists() or (target.name == 'manifest-author-r3.json' and not (D / 'manifest-author-r3.json').exists()), url
            links += 1
    spec = (D / 'spec-r3.md').read_text()
    ids = set(re.findall(r'^\|\s*(REQ-[A-Z0-9-]+)\s*\|', spec, re.M)) | set(re.findall(r'^###\s+(REQ-[A-Z0-9-]+)(?:\s|$)', spec, re.M))
    assert ids == {r['id'] for r in req} and len(ids) == 106
    assert Counter(r['strength'] for r in req) == dict(D12=96, U=10)
    assert all(r['contract'] in spec for r in req if r['strength'] == 'D12')
    history = load(D / 'consumer-history-r3.json')
    assert len(history['occurrences']) == 13 and len({x['path'] for x in history['occurrences']}) == 6
    for x in history['occurrences']:
        assert dg(path(x['path'])) == x['file_pin'] and pointer(load(path(x['path'])), x['json_pointer']) == x['value']
    rejected = []
    trials = [('old-case-mutation', None), ('new-doc-oracle', None), ('actual-overlay-grade', None), ('invent-new-requirement', None), ('wrong-source-pointer', None), ('wrong-case-pointer', None)]
    trials += [(name, (group, key, 'Enabled flag only')) for name, group, key in [('no-received-note-positive', 3, 'positive_baseline'), ('Rate-inspection-not-operation', 6, 'setup_and_action'), ('one-LFO-before-loss', 7, 'positive_baseline'), ('envelope-zero-without-positive', 8, 'positive_baseline'), ('repair-Hertz', 9, 'limits'), ('Poly-default-for-MonoGate', 11, 'positive_baseline'), ('conversion-completed-as-notes', 14, 'positive_baseline'), ('freeze-flag-as-capture', 15, 'positive_baseline'), ('XFade-equation', 15, 'limits'), ('unconditional-order', 16, 'setup_and_action'), ('one-Vocoder-channel', 19, 'positive_baseline'), ('automatic-RepeatOn', 20, 'setup_and_action'), ('clear-empty-flag', 21, 'positive_baseline'), ('insert-tap-name-as-effect', 22, 'positive_baseline')]]
    for name, edit in trials:
        bad, bo, bl = deepcopy(cases), deepcopy(overlay), deepcopy(ledger)
        if edit:
            group, key, value = edit
            bad[185 + group][key] = value
        elif name == 'old-case-mutation':
            bad[0]['setup_and_action'] = 'Different old action'
        elif name == 'new-doc-oracle':
            bad[186]['documentary_expected'] = 'always equal'
        elif name == 'actual-overlay-grade':
            bo['cases'][0]['actual_expected'] = 'pass'
        elif name == 'wrong-source-pointer':
            bl['groups'][0]['source_pointers'][0] = '/blocks/0/text'
        elif name == 'wrong-case-pointer':
            bl['groups'][0]['case_pointer'] = '/cases/0'
        else:
            bad[186]['requirements'] = ['REQ-MPL-NEW-001']
        try:
            guards(bad, bo, bl, audit)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Unsafe mutation accepted: ' + name)
    for name in NEW:
        q = D / name
        data = q.read_bytes()
        assert data.endswith(b'\n') and b'\0' not in data and all(line.rstrip(b' \t') == line for line in data.splitlines()), name
    for url in re.findall(r'\]\(([^)]+)\)', (D / 'README-r3.md').read_text()):
        target = D / url.split('#')[0]
        assert target.exists() or (url == 'manifest-author-r3.json' and not (D / 'manifest-author-r3.json').exists()), url
        links += 1
    seal = D / 'manifest-author-r3.json'
    if seal.exists():
        m = load(seal)
        assert len(m['files']) == 117
        assert set(m['files']) == {str(q.relative_to(D)) for q in D.rglob('*') if q.is_file()} - {seal.name}
        for name, pin in m['files'].items():
            assert dg(D / name) == pin, name
    assert before == {str(q): dg(q) for q in watch}
    print(json.dumps(dict(status='pass', sealed=seal.exists(), old_files_preserved=107, immutable_inputs=130, unchanged_requirements=106, preserved_old_cases=186, new_null_cases=22, current_cases=208, groups_bounded=22, exact_canonical_pages=2, actual_overlay_all_null_U=True, browser_IDs=106, consumer_occurrences=13, external_direct_old_canonical_pins=1, historical_replay=False, negative_fixtures=rejected, links=links, watched_paths=len(watch), all_unchanged=True, writes=False, old_tools_decodes_runtime=False), indent=2))


if __name__ == '__main__':
    main()
