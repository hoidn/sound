"""Read-only native MIDI R3 analyst-data checks. Never run original code or old tools."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from datetime import datetime, timezone
import ast, copy, json, re, sys
ROOT = Path(__file__).resolve().parents[4]
P = Path(__file__).resolve().parent
A = P.parent / 'native-midi-effects-source-audit'

def load(path):
    return json.loads(path.read_text())

def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}

def pointer(obj, ptr):
    for key in ptr.strip('/').split('/') if ptr else []:
        key = key.replace('~1', '/').replace('~0', '~')
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj

def pure_browser(path):
    tree = ast.parse(path.read_text())
    names = {'anchor', 'frontmatter', 'cells', 'spec_rows'}
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names
    scope = {'re': re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
    return scope['spec_rows']

def contracts(text):
    result = []
    for match in re.finditer(r'^### (REQ-NATIVE-MIDI-\d{3}) — (.*?)\n(.*?)(?=^### REQ-|^## |\Z)', text, re.M | re.S):
        result.append({'id': match[1], 'title': match[2], 'contract': match[3]})
    return result

def validate_data(req, cases, fixtures, adoption, old, audit):
    assert len(req) == 27 and len({r['id'] for r in req}) == 27
    baseline = [{k: r[k] for k in ('id','title','contract')} for r in audit['owner_requirements']]
    assert req[:7] == baseline[:7] and req[8:] == baseline[8:]
    assert adoption['clause_change']['exact_append'] == '**D12 (M 0057).** The LED next to each Shift knob flashes to indicate when its corresponding note is being played. This indicator role is not independent proof of delivered note events.\n\n'
    expected = copy.deepcopy(baseline[7]); expected['contract'] += adoption['clause_change']['exact_append']
    assert req[7] == expected
    assert adoption['clause_change']['source_block'] == 'NME:B043'
    assert 'LED next to each Shift knob' in adoption['clause_change']['exact_append']
    assert 'not independent proof' in adoption['clause_change']['exact_append']
    assert len(cases) == 176 and cases[:146] == old['cases']
    assert len({c['id'] for c in cases}) == 176
    assert Counter(c['grade'] for c in cases) == {'D12':54, 'U':122}
    assert all(c['execution'] == 'unexecuted' and c['exact_build_grade'] == 'U' for c in cases)
    ids = {r['id'] for r in req}
    for i, c in enumerate(cases[146:],67):
        assert c['id'] == f'NME-{i:03}' and c['requirement'] in ids and c['grade'] == 'U'
        assert c['source_claim'] and c['action'] and c['setup']
        assert all(c[k] is None for k in ('documentary_oracle','comparator','documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
        assert c['overlay'] == 'fixtures-r3.json#/current_version_overlay'
        groups = [g for g in adoption['groups'] if g['group'] in c['adoption_groups']]
        assert len(groups) == len(c['adoption_groups'])
        expected_blocks = list(dict.fromkeys(b for g in groups for b in g['source_blocks']))
        assert [r['block_id'] for r in c['source_references']] == expected_blocks
        for r in c['source_references']:
            assert r['path'] == str((A/'audit.json').relative_to(ROOT))
            assert pointer(audit,r['pointer'])['id'] == r['block_id']
    overlay = fixtures['current_version_overlay']
    assert overlay['applies_to'] == [c['id'] for c in cases]
    assert 'UI-only' in overlay['policy'] and 'no event/hardware output' in overlay['policy']
    assert 'NONEMPTY' in overlay['event_positive'] and 'not delivery' in overlay['event_positive']
    assert 'BOTH distinct independent' in overlay['both_events'] and 'without inventing a same-key' in overlay['both_events']
    assert len(fixtures['actual_oracles']) == 176
    for c, o in zip(cases,fixtures['actual_oracles']):
        assert o == dict(id=c['id'],actual_expected=None,actual_comparison=None,target='U',executed=False)
    assert fixtures['questions'] == audit['source_questions']
    assert len(adoption['groups']) == 21
    for i, g in enumerate(adoption['groups']):
        p = audit['proposals'][i]
        assert g['group'] == p['id'] and g['source_blocks'] == p['source_blocks']
        assert g['audit_pointer'] == '/proposals/'+str(i)
        assert g['new_cases'] == [c['id'] for c in cases[146:] if g['group'] in c['adoption_groups']]
        assert not g['complete'] and not g['executed'] and g['target'] == 'U' and g['coverage_credit'] == 0
        assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
        if i in (15,20): assert not g['new_cases'] and g['disposition'] == 'retained-U-no-new-case-or-law'
    by = {c['id']:c for c in cases}
    # Finite semantic guardrails, separate from cryptographic freeze checks.
    required = {
        'NME-070': ('complete productive pattern','do not require the changed-input realization to differ'),
        'NME-073': ('physically held','all-keys-up'),
        'NME-080': ('both genuinely nonempty','same admitted cc','independently received automation','independently received cc control'),
        'NME-086': ('both productive root/generated','not just a device flag'),
        'NME-087': ('latch explicitly off','without forcing a guessed same-key pairing'),
        'NME-089': ('latch off first','genuinely enabled','nme-nl-l01/l05 latch off'),
        'NME-091': ('independently known upper boundary','not inferred from range','both distinct qualifying'),
        'NME-093': ('genuine c-to-d output','mouse click'),
        'NME-094': ('nonzero note on and note off','both separately productive','no raw note on velocity-zero'),
        'NME-095': ('valid nonzero','productive matched clip output','nme-066 raw-zero u'),
        'NME-096': ('shading inspection alone needs no hardware','nme-064 only 60..127 membership')}
    for key, fragments in required.items():
        text = (by[key]['setup']+' '+by[key]['action']).lower()
        assert all(f in text for f in fragments),key
    assert 'double-click' not in (by['NME-093']['action']+by['NME-093']['source_claim'])
    for key in ('NME-NL-L01','NME-NL-L05'):assert 'Latch off' in by[key]['setup']
    for key in ('NME-043','NME-044','NME-045'):assert by[key] == next(c for c in old['cases'] if c['id']==key)
    assert by['NME-064'] == next(c for c in old['cases'] if c['id']=='NME-064')
    return True

def rejection_fixtures(req,cases,fixtures,adoption,old,audit):
    tests=[]
    def add(name,mutate):tests.append((name,mutate))
    add('old-record-mutation',lambda q,c,f,a:c[0].update(action='wrong'))
    add('old-documentary-grade-mutation',lambda q,c,f,a:c[0].update(grade='U'))
    add('new-numeric-documentary-promotion',lambda q,c,f,a:c[146].update(documentary_oracle='numeric law'))
    add('new-actual-promotion',lambda q,c,f,a:c[146].update(actual_expected='pass'))
    add('overlay-actual-promotion',lambda q,c,f,a:f['actual_oracles'][0].update(actual_comparison='value'))
    add('missing-global-positive',lambda q,c,f,a:f['current_version_overlay'].update(event_positive='enabled flag only'))
    add('missing-both-event-reception',lambda q,c,f,a:f['current_version_overlay'].update(both_events='one stream enabled'))
    add('wrong-source-block',lambda q,c,f,a:c[146]['source_references'][0].update(pointer='/blocks/0'))
    add('wrong-adoption-group',lambda q,c,f,a:c[146].update(adoption_groups=['NMA-G21']))
    add('merge-without-two-positives',lambda q,c,f,a:c[159].update(setup='one active flag'))
    add('hold-all-up-borrow',lambda q,c,f,a:c[152].update(setup='all keys released',action='toggle held pattern'))
    add('latch-disabled-automation-borrow',lambda q,c,f,a:c[168].update(setup='Latch on controls disabled'))
    add('pitch-range-unit-borrow',lambda q,c,f,a:c[170].update(setup='Range value computes upper endpoint'))
    add('velocity-zero-borrow',lambda q,c,f,a:c[174].update(setup='raw velocity zero only'))
    add('scale-double-click-invention',lambda q,c,f,a:c[172].update(action=c[172]['action'].replace('mouse click','double-click')))
    add('opaque-alt-resolved',lambda q,c,f,a:a['groups'][15].update(new_cases=['NME-049']))
    for name, mutate in tests:
        q,c,f,a = copy.deepcopy((req,cases,fixtures,adoption));mutate(q,c,f,a)
        try:validate_data(q,c,f,a,old,audit)
        except (AssertionError,KeyError,IndexError):pass
        else:raise AssertionError('unsafe fixture accepted: '+name)
    return [name for name,_ in tests]

PENDING = []

def check_links(path,text):
    count=0
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',text):
        if re.match(r'(https?://|mailto:|#)',target):continue
        target=target.split('#',1)[0]
        if target:
            resolved=(path.parent/target).resolve()
            if not resolved.exists() and not (P/'manifest-author-r3.json').exists() and resolved in {P/'manifest-author-r3.json',P/'validation-r3.json'}:
                PENDING.append(str(resolved.relative_to(ROOT)));continue
            assert resolved.exists(),(path,target)
            count+=1
    return count

def main():
    assert sys.argv[1:] == ['--check'],'Read-only: use --check. No write mode.'
    # Enumerate own packet first. Input metadata is read to enumerate immutable provider watches;
    # every provider is hashed before source parsing and watched until return.
    first={p:identity(p) for p in P.iterdir() if p.is_file()}
    inputs=load(P/'inputs-r3.json')
    wiki=[ROOT/'wiki/specs/native-midi-effects.md',ROOT/'wiki/research/native-midi-effects.md']
    watched=set(first)|{ROOT/x['path'] for x in inputs['files']}|set(wiki)
    before={p:identity(p) for p in watched}
    assert all(before[p]==v for p,v in first.items())
    for row in inputs['files']:assert identity(ROOT/row['path']) == {k:row[k] for k in ('bytes','sha256')},row['path']
    for name,row in inputs['old_packet_files'].items():assert identity(P/name)=={k:row[k] for k in ('bytes','sha256')}
    assert len(inputs['old_packet_files'])==32
    assert identity(P/'manifest-author-r1.json')['sha256']=='95e0785298dddd4e8a4a87f33045e5087f4003ba621a38d9b3cbb97784b792d5'
    assert identity(P/'manifest-author-r2.json')['sha256']=='17d74ef752829a992416eb725bd459c70dd8d4dd61ea2480d6eb17c794c11743'
    assert identity(P/'author-r1-snapshot.tar.gz')['sha256']=='c6967748a7b453dd5d8b4bb336faf42fe417bb3d1bd129e801f5a9e9a0b9864a'
    audit=load(A/'audit.json');old=load(P/'cases.json');req=load(P/'requirements-r3.json')['requirements'];cases=load(P/'cases-r3.json')['cases'];fixtures=load(P/'fixtures-r3.json');adoption=load(P/'adoption-r3.json')
    assert identity(A/'manifest.json')['sha256']=='55a5dba6ea7ac95994e9471387f77834d0c81a8701c0a121223ce6979d1dc3d5'
    # Only the inspected pinned pure analyst HTML parser, no old owner/audit tools.
    parser_path=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/midi-editing-source-audit/source_parser.py'
    assert identity(parser_path)['sha256']=='648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
    scope={};exec(compile(parser_path.read_text(),str(parser_path),'exec'),scope)
    blocks,resources=scope['extract']((P/'manual-12-midi-effects-2026-10-19.html').read_text(),'NME')
    assert blocks==audit['blocks'] and len(blocks)==112 and len(resources)==19
    assert [{k:r[k] for k in x} for x,r in zip(resources,audit['resources'])]==resources
    assert identity(P/'manual-12-midi-effects-2026-10-19.html')['sha256']=='33739cb549d6577624acd91466dafeafe8faaeea03044ac358043233015603a9'
    validate_data(req,cases,fixtures,adoption,old,audit)
    negatives=rejection_fixtures(req,cases,fixtures,adoption,old,audit)
    assert (P/'spec-before-r3.md').read_text()==load(A/'inputs.json')['canonical_snapshots'][0]['text']
    assert (P/'research-before-r3.md').read_text()==load(A/'inputs.json')['canonical_snapshots'][1]['text']
    spec=wiki[0].read_text();research=wiki[1].read_text()
    for snapshot,live in [('spec-r3.md',wiki[0]),('research-r3.md',wiki[1])]:assert (P/snapshot).read_bytes()==live.read_bytes()
    current_contracts=contracts(spec)
    assert len(current_contracts)==27
    assert [{**r,'contract':r['contract'].strip()} for r in current_contracts]==[{**r,'contract':r['contract'].strip()} for r in req]
    browser=pure_browser(ROOT/'tools/spec_browser.py')
    assert [r['id'] for r in browser(wiki[0],spec)]==[r['id'] for r in req]
    consumer=load(P/'consumers-asof-r3.json')
    assert len(consumer['occurrences'])==6 and consumer['paths']==3
    for row in consumer['occurrences']:
        assert pointer(load(ROOT/row['consumer']['path']),row['pointer'])==row['sha256']
        assert identity(ROOT/row['historical_provider'])['sha256']==row['sha256']
    links=check_links(wiki[0],spec)+check_links(wiki[1],research)
    if (P/'README-r3.md').exists():links+=check_links(P/'README-r3.md',(P/'README-r3.md').read_text())
    # Untracked-aware whitespace over authored docs/tools only; immutable HTML/source is hashchecked.
    for name in ['check-r3.py','README-r3.md','spec-r3.md','research-r3.md']:
        if (P/name).exists():assert not any(line.rstrip()!=line for line in (P/name).read_text().splitlines()),name
    for text in [spec,research]:assert not any(line.rstrip()!=line for line in text.splitlines())
    sealed=(P/'manifest-author-r3.json').exists()
    if sealed:
        seal=load(P/'manifest-author-r3.json')
        assert {str(p.relative_to(ROOT)) for p in P.iterdir() if p.is_file()}=={r['path'] for r in seal['payloads']}|{str((P/'manifest-author-r3.json').relative_to(ROOT))}
        for row in seal['payloads']:assert identity(ROOT/row['path'])=={k:row[k] for k in ('bytes','sha256')},row['path']
    assert before=={p:identity(p) for p in watched},'read-only watch changed'
    print(json.dumps(dict(status='pass' if sealed else 'pass-unsealed-preflight',pending_declared_artifacts=sorted(set(PENDING)),utc=datetime.now(timezone.utc).isoformat(),sealed=sealed,requirements=27,browser_IDs=27,cases=176,old_records_exact=146,old_packet_files_exact=32,documentary_D12=54,documentary_U=122,new_documentary_null=30,actual_null_U=176,source_blocks=112,literal_resources=19,input_pins=len(inputs['files']),consumer_occurrences=6,consumer_files=3,links=links,unsafe_fixtures_rejected=negatives,watched_unchanged=len(watched),read_scope='Integrity/current bounded author predicates only, not semantic-independent-review, runtime or coverage.',complete=False),indent=2))

if __name__=='__main__':main()
