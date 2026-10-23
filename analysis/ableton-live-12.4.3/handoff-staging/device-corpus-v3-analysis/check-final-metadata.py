"""Finite read-only final metadata checks; no historical tool or numerical execution."""
from pathlib import Path
import copy, hashlib, json, re, sys
P = Path(__file__).resolve().parent
BASE = P.parent
STAGE = BASE / 'device-corpus-v3'
ARCHIVE = P / 'frozen-review-candidate'

def ident(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def check_cases(current, before):
    want = copy.deepcopy(before)
    want['status'] = 'released'
    want['cases'][-1]['provenance'] = want['cases'][-1]['provenance'].replace(
        'finite engineering criteria proposed, application and arm64 not executed',
        'finite engineering criteria independently reviewed, application and arm64 not executed')
    assert current == want

def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no metadata writer, replay, comparator or native call.')
    delta = json.loads((P/'final-metadata-change.json').read_text())
    freeze = json.loads((P/'candidate-freeze.json').read_text())
    prov = json.loads((P/'author-provenance-review-candidate.json').read_text())
    watched = {p for d in [STAGE, P] for p in d.rglob('*') if p.is_file()}
    watched |= {Path(p) for p in prov['old_release85_watch']}
    watched |= {Path(r['path']) for r in prov['source_inputs']}
    before_watch = {str(p): ident(p) for p in sorted(watched)}
    # Explicit snapshot storage verification, not a replay of any historical checker.
    for r in freeze['files']:
        source = Path(r['path'])
        provider = ARCHIVE / source.relative_to('device-corpus-v3') if source.parts[0] == 'device-corpus-v3' else BASE/source
        assert ident(provider) == {k:r[k] for k in ('bytes', 'sha256')}
    for path, expected in prov['old_release85_watch'].items(): assert ident(Path(path)) == expected
    for r in prov['source_inputs']: assert ident(Path(r['path'])) == {k:r[k] for k in ('bytes','sha256')}
    assert ident(Path(delta['review']['path'])) == {k:delta['review'][k] for k in ('bytes','sha256')}
    assert ident(STAGE/'manifest.json') == delta['final_manifest']
    files = sorted(p for p in STAGE.rglob('*') if p.is_file())
    assert len(files) == 87 and not any(p.is_symlink() for p in STAGE.rglob('*'))
    changed = [str(p.relative_to(STAGE)) for p in files if p.read_bytes() != (ARCHIVE/p.relative_to(STAGE)).read_bytes()]
    assert changed == delta['changed_public_paths'] == ['AGENTS.md','README.md','REVIEW.md','cases.json','manifest.json','spec.md']
    for name in ['spec.md', 'README.md', 'AGENTS.md', 'cases.json']:
        text = (ARCHIVE/name).read_text()
        for op in delta['literal_changes']:
            if op['path'] == name:
                assert text.count(op['before_literal']) == 1
                text = text.replace(op['before_literal'], op['after_literal'])
        assert text == (STAGE/name).read_text()
    old = json.loads((ARCHIVE/'cases.json').read_text())
    current = json.loads((STAGE/'cases.json').read_text())
    check_cases(current, old)
    all_evals = lambda x: [e for c in x['cases'] for e in c['evaluations']]
    assert len(all_evals(current)) == 71 and all_evals(current) == all_evals(old)
    assert current['cases'][:24] == old['cases'][:24]
    negatives = []
    for name, mutation in [
        ('event frame changed', lambda x: x['cases'][-1]['evaluations'][0]['events'][0].update(frame=1536)),
        ('omitted mode restored', lambda x: x['cases'][-1]['evaluations'][1]['metric']['modes'][0].append({'center_hz':8371,'cutoff_hz':100})),
        ('stale pending status', lambda x: x.update(status='draft-pending-handoff-review')),
    ]:
        bad = copy.deepcopy(current); mutation(bad)
        try: check_cases(bad, old)
        except AssertionError: negatives.append(name)
        else: raise AssertionError(name)
    m = json.loads((STAGE/'manifest.json').read_text())
    assert m['release_status'] == current['status'] == 'released'
    assert m['release_date'] == m['review']['date'] == '2026-10-20'
    assert m['review']['status'] == 'approved-finite-scope' and m['review']['reviewers'] == ['Codex independent handoff reviewer (synthesis_finish)']
    assert m['specification']['parent_sha256'] == prov['adopted_parent_asof']['sha256']
    assert len(m['files']) == 86 and {r['path'] for r in m['files']} == {str(p.relative_to(STAGE)) for p in files if p.name != 'manifest.json'}
    for r in m['files']: assert ident(STAGE/r['path']) == {k:r[k] for k in ('bytes','sha256')}
    links = []
    for p in files:
        if p.suffix in ['.md','.json','.py']:
            text = p.read_text()
            assert text.endswith('\n') and all(not line.endswith((' ','\t')) for line in text.splitlines())
            assert not any(s in text for s in ['/home/','/tmp/','/var/tmp/','analysis/','wiki/research/','FUN_0','DAT_0','_CalcA','_SetParameterA'])
            if p.suffix == '.md':
                for target in re.findall(r'\]\(([^)]+)\)', text):
                    path = target.split('#')[0]
                    if path:
                        dest = (p.parent/path).resolve()
                        assert dest.is_relative_to(STAGE) and dest.is_file()
                        links.append([p.name,path])
    for name in ['README.md','spec.md','REVIEW.md']:
        text = (STAGE/name).read_text().lower()
        assert not any(s in text for s in ['unreviewed draft','pending independent','await independent approval','proposed parent','draft release'])
    assert before_watch == {str(p):ident(p) for p in sorted(watched)}
    print(json.dumps({'status':'Metadata finalization verified; independent focused final seal still required; not published.',
          'manifest':ident(STAGE/'manifest.json'),'review':ident(STAGE/'REVIEW.md'),'changed_public_paths':changed,
          'all71_evaluations_exact':True,'old24_groups_exact':True,'all80_signal_reference_files_exact':True,
          'comparator_byte_exact':True,'frozen_candidate_108_entries_exact':len(freeze['files']),
          'old_release85_unchanged':True,'negative_fixtures':negatives,'links':links,
          'watched':len(watched),'unchanged':True,'numerical_rerun':False,'original_or_candidate_calls':0},indent=2))

if __name__ == '__main__': main()
