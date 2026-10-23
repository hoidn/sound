#!/usr/bin/env python3
"""Finite owner R2 integrity checks. Read-only; no old main/decoder/runtime."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

P = Path(__file__).resolve().parent
R = P.parents[3]
A = P.parent / 'audio-utilities-source-audit'


def load(p):
    return json.loads(p.read_text())


def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pins(rows):
    for x in rows:
        assert identity(R / x['path']) == {k: x[k] for k in ('bytes', 'sha256')}, x['path']


def pointer(v, p):
    for k in p.strip('/').split('/') if p else []:
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def safety(cases):
    assert len(cases) == 9
    guards = [
        ['nonzero_active_output','productive_width','productive_midside','positive_before_each_left_right'],
        ['nonzero_active_output','productive_midside','both_intermediate_paths'],
        ['nonzero_active_output','productive_downstream_effect','sustained_nonzero_tail_before_mute','separate_reverb_delay'],
        ['nonzero_active_output','known_low_dc','productive_nonlinear_after_utility','necessary_not_sufficient'],
        ['accepted_monophonic_detection','matched_reference_tuning','both_colors_both_views','actual_classic_arrows','actual_intune_target'],
        ['accepted_monophonic_detection','matched_reference_tuning','positive_before_each_unsupported_input'],
        ['accepted_monophonic_detection','effective_loaded_tuning','independent_ui_route_if_found','no_external_receiver_substitution'],
        ['nonzero_analysis','productive_manual_range','productive_manual_zoom','same_controls_after_auto'],
        ['nonzero_analysis','visible_max_history_before_each','restart_route_if_admitted','max_off_retention_unknown']]
    tokens = [
        ['Before EACH Left and Right','BOTH controls','choose Left','choose Right'],
        ['interior setting between 0 and 100M','interior setting between 0 and 100S'],
        ['sustained NONZERO downstream reverb tail BEFORE','sustained NONZERO tail before Mute','delay-line'],
        ['toggle Utility DC off/on','not assume every qualifying setup changes audibly'],
        ['Classic; actually present','in-tune then out-of-tune','Histogram','BOTH in-tune and out-of-tune','arrows themselves','Target Mode','in-tune history'],
        ['BEFORE each','silence then noise','source removal','may give an error'],
        ['only IF','otherwise retain route/outcome U','do not substitute','TUN-015 external-receiver'],
        ['BOTH minimum and maximum','successful manual zoom','THEN select Auto','same Range sliders AND zoom'],
        ['actually observe retained maximum','Rebuild and observe','if its UI route/event is not established keep that branch U','Max off']]
    # The unsupported-input clause must deny, rather than promise, fallback.
    tokens[5][-1] = 'without assuming inaccurate input must give an error'
    for i, c in enumerate(cases):
        assert c['audit_group'] == f'UAS-G{i+1:02}' if i < 6 else c['audit_group'] == ['UAS-G09','UAS-G07','UAS-G08'][i-6]
        assert set(c['prerequisites']) == set(guards[i])
        for s in tokens[i]:
            assert s in c['actions'], (c['id'], s)
        for k in ('expected','comparison','documentary_expected','documentary_comparison','actual_expected','actual_comparison'):
            assert c[k] is None, (c['id'], k)
        assert c['target_grade'] == 'U' and c['execution'] == 'unexecuted'
        assert c['provenance'] == ('U' if i in (5,6) else 'D12')
    assert 'necessary, not sufficient' in cases[3]['source_claim']
    assert 'as of Live 12.1' in cases[6]['source_claim']
    assert 'not Tuner' in cases[6]['source_claim']


def fixtures(cases):
    rejected = []
    for i, key in [(0,'productive_width'),(0,'productive_midside'),(1,'both_intermediate_paths'),(2,'sustained_nonzero_tail_before_mute'),(3,'known_low_dc'),(3,'productive_nonlinear_after_utility'),(4,'accepted_monophonic_detection'),(5,'positive_before_each_unsupported_input'),(6,'independent_ui_route_if_found'),(7,'productive_manual_range'),(7,'productive_manual_zoom'),(8,'visible_max_history_before_each')]:
        bad = copy.deepcopy(cases)
        bad[i]['prerequisites'].remove(key)
        try:
            safety(bad)
        except AssertionError:
            rejected.append(key)
        else:
            raise AssertionError('guard mutation accepted: '+key)
    for name,i,k,v in [
        ('colors-one-view',4,'actions',cases[4]['actions'].replace('BOTH in-tune and out-of-tune','a generic view toggle')),
        ('ball-instead-of-arrow',4,'actions',cases[4]['actions'].replace('arrows themselves','ball only')),
        ('DC-sufficiency',3,'source_claim',cases[3]['source_claim'].replace('necessary, not sufficient','sufficient')),
        ('TUN015-Tuner-promotion',6,'source_claim',cases[6]['source_claim'].replace('not Tuner','Tuner')),
        ('actual-oracle',8,'actual_expected','reset passes'),
        ('guessed-restart',8,'actions',cases[8]['actions'].replace('if its UI route/event is not established keep that branch U','always stop/start'))]:
        bad = copy.deepcopy(cases);bad[i][k] = v
        try:
            safety(bad)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('semantic mutation accepted: '+name)
    return rejected


def main():
    assert sys.argv[1:] == ['--check'], 'read-only: --check required; writing/old replay refused'
    inputs = load(P/'inputs-r2.json'); prior = load(P/'prior-files-r2.json')
    watched = {x['path'] for x in inputs['files']+prior}
    watched |= {str(p.relative_to(R)) for p in P.rglob('*') if p.is_file()}
    delta = load(P/'delta-r2.json')
    watched |= {x['path'] for x in delta['canonical_pages']}
    watched |= {x['file']['path'] for x in load(P/'consumer-history-r2.json')['external_occurrences']}
    before = {x: identity(R/x) for x in watched}
    pins(inputs['files']);pins(prior)
    # The R1 manifest's four original mutable canonical pins resolve as-of.
    providers = {x['canonical']:x['provider'] for x in inputs['before_snapshots']}
    for x in load(P/'manifest-author-r1.json')['payloads']:
        q = R/providers.get(x['path'],x['path'])
        assert identity(q) == {k:x[k] for k in ('bytes','sha256')}
    for s in load(P/'sources.json'):
        assert identity(P/s['path']) == {k:s[k] for k in ('bytes','sha256')}
    audit = load(A/'audit.json');cat = load(P/'cases-r2.json')['profiles'];req = load(P/'requirements-r2.json')
    assert len(audit['blocks']) == 46 and len(audit['assessments']) == 101
    html = (P/'manual-audio-effects-2026-10-19.html').read_text()
    for b in audit['blocks']:
        assert html[b['raw_start']:b['raw_end']] == b['raw_html']
    new = []
    req_ids = []
    for name, old_count, new_count in [('utility',37,41),('tuner',32,35),('spectrum',34,36)]:
        old = load(P/(name+'-cases.json'))
        assert cat[name]['cases'][:old_count] == old['cases']
        assert len(cat[name]['cases']) == new_count
        assert len(req[name]) == len(old['requirements'])
        assert req[name] == cat[name]['requirements']
        for o,n in zip(old['requirements'],req[name]):
            changes = [d for d in delta['clause_changes'] if d['id'] == o['id']]
            assert n == (changes[0]['after'] if changes else o)
            if changes:
                assert changes[0]['before'] == o
                assert n['contract'].startswith(o['contract']+' ')
        req_ids.extend(x['id'] for x in req[name]);new.extend(cat[name]['cases'][old_count:])
        for c in cat[name]['cases']:
            assert set(c['requirements']) <= {r['id'] for r in req[name]}
            if c['provenance']=='U':assert c['expected'] is None
    assert len(set(req_ids)) == 41
    assert [x['id'] for x in delta['clause_changes']] == ['REQ-DEVICE-UTILITY-005','REQ-DEVICE-UTILITY-013']
    assert 'continuous mono-to-stereo' in delta['clause_changes'][0]['after']['contract']
    assert 'necessary condition, not a promise' in delta['clause_changes'][1]['after']['contract']
    allcases = [c for d in cat.values() for c in d['cases']]
    assert len({c['id'] for c in allcases}) == 112
    assert {g:sum(c['provenance']==g for c in allcases) for g in ['D12','Dpkg','U']} == {'D12':63,'Dpkg':6,'U':43}
    safety(new);rejected=fixtures(new)
    assert delta['source_questions'] == audit['source_questions']
    assert delta['common_future_prerequisites'] == audit['common_future_prerequisites']
    assert len(delta['groups']) == 9
    for g in delta['groups']:
        c = pointer(load(P/'cases-r2.json'),g['case_pointer'])
        assert c['id'] == g['case_id'] and c['audit_group'] == g['audit_group']
        a = pointer(audit,g['audit_pointer']);assert a['id'] == g['audit_group'] and a['limits'] == g['remaining']
    browser = R/'tools/spec_browser.py'
    tree=ast.parse(browser.read_text())
    funcs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ('anchor','frontmatter','cells','spec_rows')]
    assert len(funcs)==4
    ns={'re':re};exec(compile(ast.Module(body=funcs,type_ignores=[]),str(browser),'exec'),ns)
    rows=[];links=0
    for x in delta['canonical_pages']:
        old=(R/x['before_provider']).read_text();current=(R/x['path']).read_text()
        assert identity(R/x['before_provider'])['sha256']==x['before_sha256']
        edits=x['edits'];rebuilt=old
        for e in reversed(edits):
            i,j=e['before_span'];assert old[i:j]==e['before'];rebuilt=rebuilt[:i]+e['after']+rebuilt[j:]
        assert rebuilt==current==(R/x['after_provider']).read_text()
        assert hashlib.sha256(current.encode()).hexdigest()==x['after_sha256']
        if '/specs/' in x['path']:rows+=ns['spec_rows'](R/x['path'],current)
    assert {r['id'] for r in rows}==set(req_ids) and len(rows)==41
    for x in load(P/'consumer-history-r2.json')['external_occurrences']:
        pins([x['file']]);assert pointer(load(R/x['file']['path']),x['json_pointer'])==x['sha256']
        assert identity(R/x['provider'])['sha256']==x['sha256']
    assert len(load(P/'consumer-history-r2.json')['external_occurrences'])==14
    docs=[R/x['path'] for x in delta['canonical_pages']]+[P/'README-r2.md']
    for f in docs:
        t=f.read_text()
        for url in re.findall(r'\]\(([^)\s]+)\)',t):
            if re.match(r'[a-z]+:',url):continue
            path,_,anchor=url.partition('#');q=(f.parent/unquote(path)).resolve() if path else f
            assert q.exists() or (not (P/'manifest-author-r2.json').exists() and q==P/'manifest-author-r2.json'), (str(f),url)
            if anchor and q.exists() and q.suffix=='.md':
                heads=[ns['anchor'](h) for h in re.findall(r'^#+ (.+)$',q.read_text(),re.M)]
                assert anchor in heads,(str(f),url)
            links+=1
    textfiles=[p for p in P.rglob('*') if p.is_file() and p.suffix in ('.json','.md','.py')]
    for f in textfiles+docs:
        t=f.read_text();assert t.endswith('\n') and not any(line.rstrip()!=line for line in t.splitlines()),str(f)
    seal=P/'manifest-author-r2.json'
    if seal.exists():pins(load(seal)['payloads'])
    assert {x:identity(R/x) for x in watched}==before
    print(json.dumps({'status':'pass','sealed':seal.exists(),'requirements':41,'cases':112,'D12':63,'Dpkg_file_only':6,'U':43,'new_doc_actual_nonnull':0,'application_executions':0,'complete_profiles':0,'old_files':len(prior),'immutable_inputs':len(inputs['files']),'browser_ids':len(rows),'links':links,'source_blocks':46,'groups':9,'rejected_mutations':rejected,'watched_unchanged':len(watched),'writes':False},indent=2))


if __name__ == '__main__':
    main()
