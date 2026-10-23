"""Read-only Project R2 source-backed author checks; stdlib and retained data only."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json, re, sys
A = Path(__file__).resolve().parent
R = A.parents[3]
S = A.parent / 'project-media-source-audit'
NULL = ['documentary_expected', 'documentary_comparison', 'actual_expected', 'actual_comparison']
def j(p):
    return json.loads(p.read_text())
def dg(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=sha256(b).hexdigest())
def ptr(v, p):
    assert p.startswith('/')
    for key in p[1:].split('/'):
        if isinstance(v, list):
            assert re.fullmatch(r'0|[1-9][0-9]*', key)
            v = v[int(key)]
        else:
            v = v[key.replace('~1','/').replace('~0','~')]
    return v
# Literal finite safety checks, not general semantic coverage or app tests.
GUARDS = {
    'PMW-035': ['Open Recent', 'double-click', 'press Enter'],
    'PMW-036': ['View menu', 'Up/Down', 'press Enter', 'dimmed'],
    'PMW-037': ['Devices icon', 'whole Group', 'nested Group', 'preview control'],
    'PMW-038': ['dragging', 'Shift', 'Windows Ctrl', 'Mac Option', 'confirm'],
    'PMW-039': ['Set Default Live Set', 'context-menu', 'File-menu', 'create a new Set'],
    'PMW-040': ['HotSwap', 'distinct Y'],
    'PMW-041': ['sample reference', 'non-sample reference', 'without launching'],
    'PMW-042': ['open a known Set', 'title bar', 'other admitted contained Set'],
    'PMW-043': ['content pane', 'drop', 'Current Project label'],
    'PMW-044': ['Status Bar warning', 'Manage Set', 'Locate'],
    'PMW-045': ['Set Folder', 'nested subfolder', 'Search Project', 'Search Library', 'retry', 'HotSwap', 'double-click'],
    'PMW-046': ['Collect All and Save', 'click OK', 'View File Manager', 'Show', 'Collect Into Project', 'Collect and Save'],
    'PMW-047': ['Dont Copy', 'clicking', 'pressing Enter'],
    'PMW-048': ['one clip', 'one preset', 'multiple-track', 'Save Preset button'],
    'PMW-049': ['Manage User Library', 'View File Manager', 'right-click', 'Collect and Save'],
    'PMW-050': ['Manage User Library', 'Unused Files', 'Show', 'preview', 'Delete key', 'context-menu Delete'],
    'PMW-051': ['Create Pack', 'completion notification', 'double-clicking', 'dragging', 'File Install Pack', 'unpack'],
    'PMW-052': ['two admitted Set versions', 'Manage Project', 'Collect Into Project', 'Collect and Save'],
    'PMW-053': ['reorganization', 'Manage Project', 'Locate', 'Fully Rescan Folders', 'click Go', 'after an admitted completed search']}
def semantic(c, ad):
    assert len(c['requirements']) == 23 and len(c['cases']) == 53
    assert [x['id'] for x in c['requirements']] == [f'REQ-PROJECT-MEDIA-{i:03}' for i in range(1,24)]
    assert [x['id'] for x in c['cases']] == [f'PMW-{i:03}' for i in range(1,54)]
    by = {x['id']:x for x in c['cases']}
    for x in c['cases']:
        assert x['actual_expected'] is x['actual_comparison'] is None and x['target'] == 'U' and not x['executed']
    for x in c['cases'][34:]:
        assert all(x[k] is None for k in NULL)
        assert x['provenance'] == 'D12'
        actions = ' '.join(x['setup_and_action'])
        assert all(v in actions for v in GUARDS[x['id']]), x['id']
        assert 'NONEMPTY' in ' '.join(x['prerequisites']) and x['evidence']
        assert all(r in {q['id'] for q in c['requirements']} for r in x['requirements'])
    assert 'actual nonzero delivered' in c['common_future_prerequisites'] and 'EACH' in c['common_future_prerequisites'] and 'BOTH independent' in c['common_future_prerequisites']
    assert 'marker' in ' '.join(by['PMW-040']['prerequisites']) and 'two independently' in ' '.join(by['PMW-040']['prerequisites'])
    assert 'membership' in ' '.join(by['PMW-045']['prerequisites']) and 'not establish membership' in ' '.join(by['PMW-045']['prerequisites'])
    assert 'EACH' in ' '.join(by['PMW-044']['prerequisites']) and 'nonzero' in ' '.join(by['PMW-044']['prerequisites'])
    assert 'EACH preview' in ' '.join(by['PMW-050']['prerequisites']) and 'owned copies only' in ' '.join(by['PMW-050']['prerequisites'])
    assert 'SAME independently established' in ' '.join(by['PMW-052']['prerequisites'])
    assert 'nonzero' in ' '.join(by['PMW-053']['prerequisites']) and 'membership' in ' '.join(by['PMW-053']['prerequisites'])
    assert len(ad['groups']) == 19 and ad['unadopted'][0]['id'] == 'G06' and len(ad['unadopted']) == 1
    for g in ad['groups']:
        assert g['status'] == 'partial-input-history-adopted-not-complete' and not g['complete'] and g['coverage_credit'] == 0
        assert g['source_audit_limits_asof'] and 'Actual target behavior' in g['remaining_U']
        assert [ptr(c,p)['id'] for p in g['case_pointers']] == g['case_ids']
        assert all(by[v]['group'] == g['id'] for v in g['case_ids'])
    n = c['requirements'][-1]
    assert n['provenance_source'] == 'D12/E15' and n['target'] == 'U' and n['actual_expected'] is n['actual_comparison'] is None
    assert 'Manage User Library' in n['documented_predicate'] and 'other Project' in n['preconditions']
    return True
def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Readonly --check only; unsupported arguments refused before inputs'
    inp, c, ad, delta = (j(A/n) for n in ['inputs-r2.json','catalog-r2.json','adoption-r2.json','delta-r2.json'])
    watch = {R/p for p in inp['files']} | {p for p in A.iterdir() if p.is_file()} | {R/p for p in delta['canonicals']}
    before = {str(p):dg(p) for p in watch}
    for path, row in inp['files'].items():
        assert dg(R/path) == row, path
    assert len(inp['old_packet_files']) == 6
    audit = j(S/'audit.json')
    for key, source_key, old_n in [('requirements','owner_requirements',22),('cases','owner_cases',34)]:
        for cur, old in zip(c[key][:old_n],audit[source_key]):
            assert all(cur[k] == v for k,v in old.items()), cur['id']
            o = cur['origin']; raw = (R/o['path']).read_text()
            assert raw[o['character_start']:o['character_end']] == o['raw_line'] == old['markdown']
            assert raw.encode()[o['utf8_start']:o['utf8_end']].decode() == old['markdown']
            assert raw.splitlines()[o['line']-1] == old['markdown']
            assert sha256(o['raw_line'].encode()).hexdigest() == o['raw_line_sha256']
    for path,row in inp['canonical_before'].items():
        assert dg(R/row['provider']) == {k:row[k] for k in ['bytes','sha256']}
    # Resolve only the corrected historical manifest via its immutable providers.
    for row in j(A/'manifest.json')['files']:
        p = R/inp['canonical_before'][row['path']]['provider'] if row['path'] in inp['canonical_before'] else R/row['path']
        assert dg(p) == {k:row[k] for k in ['bytes','sha256']}
    for path,row in delta['canonicals'].items():
        text = (R/row['before']).read_text()
        for e in row['replacements']:
            assert text.count(e['old']) == 1
            text = text.replace(e['old'],e['new'],1)
        assert text + row['append'] == (A/row['current_provider']).read_text() == (R/path).read_text()
    spec = (A/'spec-r2.md').read_text()
    ids = re.findall(r'^\| (REQ-PROJECT-MEDIA-[0-9]+) \|',spec,re.M)
    assert ids == [x['id'] for x in c['requirements']] and len(set(ids)) == 23
    case_ids = re.findall(r'^\| (PMW-[0-9]+) \|',spec,re.M)
    assert case_ids == [x['id'] for x in c['cases']]
    for q in c['requirements'][:22] + c['cases'][:34]:
        assert spec.splitlines().count(q['markdown']) == 1
    assert c['requirements'][-1]['markdown'] in spec.splitlines()
    for x in c['cases'][34:]:
        row = '| '+x['id']+' | '+', '.join(v[-3:] for v in x['requirements'])+' | '+x['title']+' | '+' '.join(x['setup_and_action'])+' | U; documentary and actual expected/comparison null, unexecuted. |'
        assert spec.splitlines().count(row) == 1, x['id']
    assert c['summary'] == dict(requirements=23,old_requirements=22,new_D12_UI_requirements=1,cases=53,old_rows=34,new_U_histories=19,old_bounded_documentary=30,current_documentary_null=23,actual_null_U=53,complete=False)
    semantic(c,ad)
    assert (R/ad['catalog']).resolve() == (A/'catalog-r2.json').resolve()
    e = ad['new_requirement_evidence']
    obj = ptr(c,e['requirement_pointer'])
    assert obj['id'] == e['id'] and ptr(c,e['body_pointer']) == obj['documented_predicate']
    refs = 1
    raw = (A/'manual-files-2026-10-19.html').read_text()
    for x in c['cases'][34:]:
        for e in x['evidence']:
            assert (R/e['path']).resolve() == (S/'audit.json').resolve()
            b = ptr(audit,e['pointer']); assert b['id'] == e['block']
            assert sha256(b['text'].encode()).hexdigest() == e['text_sha256']
            assert raw[b['raw_start']:b['raw_end']] == b['raw_html']; refs += 1
    for g in ad['groups'] + ad['unadopted']:
        e = g['source_proposal']; assert (R/e['path']).resolve() == (S/'audit.json').resolve()
        assert ptr(audit,e['pointer'])['id'] == g['id']; refs += 1
    for e in ad['new_requirement_evidence']['source_blocks']:
        assert (R/e['path']).resolve() == (S/'audit.json').resolve() and ptr(audit,e['pointer'])['id'] == e['block']; refs += 1
    bad = []
    variants = [
        ('operation-to-inspection',lambda x:x['cases'][36].update(setup_and_action=['Inspect available Devices icon, group and preview controls'])),
        ('wrong-template-menu',lambda x:x['cases'][38].update(setup_and_action=[s.replace('Set Default Live Set','Set Default Set') for s in x['cases'][38]['setup_and_action']])),
        ('DontCopy-is-Copy',lambda x:x['cases'][46].update(setup_and_action=[s.replace('Dont Copy','Copy') for s in x['cases'][46]['setup_and_action']])),
        ('shared-sample-no-collection-input',lambda x:x['cases'][51].update(setup_and_action=['Save two admitted Set versions; inspect inventory'])),
        ('new-documentary-oracle',lambda x:x['cases'][34].update(documentary_expected='pass')),
        ('old-actual-promoted',lambda x:x['cases'][0].update(actual_expected='pass')),
        ('flag-only-prerequisite',lambda x:x['cases'][34].update(prerequisites=['selected flag'])),
        ('missing-productive-use',lambda x:x['cases'][43].update(prerequisites=['NONEMPTY file flag'])),
        ('filename-is-matcher',lambda x:x['cases'][44].update(prerequisites=['NONEMPTY filename count'])),
        ('preview-without-output',lambda x:x['cases'][49].update(prerequisites=['NONEMPTY file listing'])),
        ('shared-sample-name-identity',lambda x:x['cases'][51].update(prerequisites=['BOTH NONEMPTY same name'])),
        ('reorganization-no-positive',lambda x:x['cases'][52].update(prerequisites=['NONEMPTY selected folder']))]
    for name, change in variants:
        copy = deepcopy(c); change(copy)
        try: semantic(copy,ad)
        except (AssertionError,KeyError,IndexError): bad.append(name)
        else: raise AssertionError('Unsafe variant accepted '+name)
    for p in ['/cases/-1','/cases/999','/old_case/0']:
        try: ptr(c,p)
        except (AssertionError,KeyError,IndexError): bad.append(p)
        else: raise AssertionError('Bad pointer accepted '+p)
    sealed = (A/'manifest-author-r2.json').exists()
    if sealed:
        m = j(A/'manifest-author-r2.json')
        assert set(m['files']) == {p.name for p in A.iterdir() if p.is_file() and p.name != 'manifest-author-r2.json'}
        for name,row in m['files'].items(): assert dg(A/name) == row, name
    links = 0
    for p, base in [(R/q,(R/q).parent) for q in delta['canonicals']] + [(A/'README-r2.md',A)]:
        for _,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',p.read_text()):
            if '://' in target or target.startswith('#'): continue
            assert (base/target.split('#')[0]).exists(), (p,target)
            links += 1
    own = {p for p in A.iterdir() if p.is_file() and p.suffix in ('.py','.md','.json')} | {R/p for p in delta['canonicals']}
    for p in own:
        assert all(line == line.rstrip() for line in p.read_text().splitlines()), p
    assert before == {str(p):dg(p) for p in watch}
    print(json.dumps(dict(status='pass',sealed=sealed,requirements=23,cases=53,old_requirements_exact=22,old_case_rows_exact=34,new_null_U_histories=19,current_actual_null_U=53,source_proposal_dereferences=refs,negative_fixtures=bad,local_links=links,old_packet_files_exact=6,immutable_pins=len(inp['files']),watch_unchanged=len(watch),writes=False,complete=False,independent_review='pending AS OF AUTHOR FREEZE'),indent=2))
if __name__ == '__main__':
    main()
