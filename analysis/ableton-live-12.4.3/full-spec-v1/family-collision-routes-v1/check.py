#!/usr/bin/env python3
"""Read-only integrity of this author map; stdlib text/JSON/hash only, no audio decode."""
import sys
if sys.argv[1:] != ['--check']:
    raise SystemExit('read-only: use --check; writes/replays unsupported')
import collections
import copy
import hashlib
import json
import pathlib
D = pathlib.Path(__file__).resolve().parent
R = D.parents[3]
P = R / 'analysis/ableton-live-12.4.3/r2/t12-collision-v1'
def sha(b):
    return hashlib.sha256(b).hexdigest()
def load(p):
    return json.loads(p.read_text())
def digest(x):
    return sha(json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())
def require(v, message):
    if not v:
        raise AssertionError(message)
def identity(p, record):
    b = p.read_bytes()
    require(len(b) == record['bytes'] and sha(b) == record['sha256'], 'identity: ' + str(p))
def ptr(d, p):
    for k in p.lstrip('/').split('/') if p else []:
        k = k.replace('~1', '/').replace('~0', '~')
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d
pins = load(D / 'pins.json')
providers = {q['id']: q for q in pins['providers']}
ledger = load(D / 'route-ledger.json')
inputs = load(D / 'input-sets.json')
nav = load(D / 'control-navigation.json')
edges = load(D / 'chain-edges.json')
preservation = load(D / 'preservation.json')
addition = load(D / 'canonical-addition.json')
spans = load(D / 'source-spans.json')['spans']
evidence = load(D / 'evidence-locators.json')
# Invariants target distinct likely semantic promotions, not another owner validator.
def semantic(l, i, n, e, p):
    rows = l['rows']
    require(l['denominator'] is None and not l['whole_family_complete'] and l['new_grade_count'] == 0, 'no denominator/grade')
    require(len(rows) == 84 and len({q['id'] for q in rows}) == 84, 'inventory')
    require(collections.Counter(q['route'] for q in rows) == {'X': 38, 'S': 10, 'no-established-route': 36}, 'route counts')
    require(l['counts'] == dict(collections.Counter(q['route'] for q in rows)), 'declared counts')
    require({q['requirement'] for q in rows} == {f'REQ-DEVICE-COLLISION-{v:03}' for v in range(1, 19)}, '18 context coverage')
    require(all(q['new_expected'] is None and q['new_actual'] is None and q['new_grade'] == 'unchanged' for q in rows), 'null new grading')
    require(len(i['draft_case_navigation']) == 50 and [q['id'] for q in i['draft_case_navigation']] == [f'DCL-{v:03}' for v in range(1, 51)], '50 navigation')
    require(i['retained_fixture_count'] == 41 and len(i['fixtures']) == 41 and i['released_count'] == 2, '41 versus 2')
    require(i['ungraded_retained_fixtures'] == ['DCL-014'] + [f'DCL-{v:03}' for v in range(33, 42)], 'zero-mode/noise omissions')
    require([q['id'] for q in i['released_evaluations']] == ['DEVICE-COLLISION-001', 'DEVICE-COLLISION-002'], 'released membership')
    require(i['released_evaluations'][0]['metric'] == {'kind': 'peak', 'maximum': 1e-18}, 'ctor metric')
    require(i['released_evaluations'][1]['metric'] == {'kind': 'stereo_relative_rms', 'maximum': .003}, 'Pipe-only metric')
    require(n['host_indices'] == list(range(139)) and [q['index'] for q in n['entries']] == list(range(139)), '139 index navigation')
    require(n['models'] == ['Beam','Marimba','String','Membrane','Plate','Pipe','Tube'], 'seven models')
    require(e['edges'][0]['status'] == 'UNKNOWN' and e['edges'][-1]['status'] == 'UNKNOWN', 'generic host/delivery gap')
    require(not any(q['runtime_sequence_proved'] for q in e['edges']), 'not runtime sequence')
    require(p['logical_mapping'] == {'run_collision.py': 'recovery/originals/run_collision.py', 'results/collision.json': 'recovery/originals/collision.json'}, 'exact recovery mapping')
    require(p['original_payload_count'] == 103 and p['all_old_grades_unchanged'] and p['actuals_added'] == 0, 'original history')
    require(p['current_paths_excluded'] == ['run_collision.py','results/collision.json'], 'incident exclusion')
semantic(ledger, inputs, nav, edges, preservation)
# Selected immutable/as-of providers only; wiki later changes are not gates on old evidence.
asof = []
for q in pins['providers']:
    if q['id'] == 'research-before':
        b = (R/q['path']).read_bytes()[:q['bytes']]
        asof.append({'id': q['id'], 'current_equals_author_asof':len(b)==q['bytes'] and sha(b)==q['sha256']})
    elif q['kind'] == 'mutable-asof':
        b = (R/q['path']).read_bytes()
        asof.append({'id': q['id'], 'current_equals_author_asof': len(b) == q['bytes'] and sha(b) == q['sha256']})
    else:
        identity(R/q['path'], q)
# All original103 bytes through explicit recovery map, never current extras as an oracle.
original = load(P/'manifest.json')
recovery = load(P/'recovery-manifest.json')
require(len(original['files']) == 103, 'original103')
require(sha((P/'manifest.json').read_bytes()) == recovery['original_manifest_sha256'], 'original manifest pin')
for name, q in original['files'].items():
    identity(P/recovery['original_path_mapping'].get(name, name), q)
for name, q in recovery['files'].items():
    identity(P/name, q)
excluded_asof = []
for q in preservation['excluded_current_path_identities']:
    b = (R/q['path']).read_bytes()
    excluded_asof.append({'path':q['path'], 'current_equals_author_asof':len(b)==q['bytes'] and sha(b)==q['sha256']})
# Released bytes unchanged; no comparator imported or executed.
release_dir = R/'handoff/device-collision-v1'
release_manifest = load(release_dir/'manifest.json')
for q in release_manifest['files']:
    identity(release_dir/q['path'], q)
require(len(release_manifest['files']) == preservation['released_payload_count'], 'release inventory')
spanmap = {q['id']: q for q in spans}
mutable_availability = {q['path']: next((v['current_equals_author_asof'] for v in asof if v['id']==q['id']), True) for q in pins['providers'] if q['kind']=='mutable-asof'}
skipped_asof_spans = []
for q in spans:
    if not mutable_availability.get(q['path'], True):
        skipped_asof_spans.append(q['id'])
        continue
    b = (R/q['path']).read_bytes()
    portion = b[q['byte_start']:q['byte_end']]
    require(sha(portion) == q['sha256'], 'span bytes: '+q['id'])
    lines = b.splitlines(keepends=True)
    require(b''.join(lines[q['line_start']-1:q['line_end']]) == portion, 'span lines: '+q['id'])
for q in evidence['json_pointers']:
    value = ptr(load(R/providers[q['provider']]['path']), q['json_pointer'])
    require(digest(value) == q['value_sha256'], 'pointer: '+q['id'])
known_evidence = {q['id'] for q in evidence['json_pointers']} | {q['id'] for q in evidence['source_roles']}
for q in ledger['rows']:
    require(q['source_span'] in spanmap and q['evidence'] and set(q['evidence']) <= known_evidence, 'row evidence')
    require(set(q['existing_cases']) <= {v['id'] for v in inputs['draft_case_navigation']}, 'case navigation')
for q in inputs['draft_case_navigation']:
    s = spanmap[q['source_span']]
    require(s['sha256'] == q['row_sha256'], 'draft row byte identity')
    require(q['navigation_only'] and q['ungraded_fixture'] == (q['id'] == 'DCL-014' or 33 <= int(q['id'][-3:]) <= 41), 'draft U scope')
for q in inputs['fixtures']:
    v = ptr(load(R/providers[q['provider']]['path']), q['json_pointer'])
    require(digest(v) == q['record_sha256'] and v['sha256'] == q['wav_sha256'], 'original registry')
    require(sha((R/q['wav_path']).read_bytes()) == q['wav_sha256'], 'WAV byte identity only')
    script = (R/q['script_path']).read_bytes()
    require(sha(script) == q['script_sha256'], 'script identity')
    lines = script.decode().splitlines()
    indices = [int(v.split()[1]) for v in lines if v.startswith('param ')]
    require(indices == list(range(139)) and digest(indices) == q['parameter_index_order_sha256'], 'ordered parameters')
    require([v for v in lines if v.startswith('process ')] == q['process_commands'], 'process metadata')
    require([v for v in lines if v.startswith('event ')] == q['events'], 'event metadata')
for q in inputs['summary_only_sets']:
    v = ptr(load(R/providers[q['provider']]['path']), q['json_pointer'])
    require(digest(v) == q['record_sha256'] and len(v) == q['top_level_items'], 'summary-only set identity')
release_cases = load(release_dir/'cases.json')
for q in inputs['released_evaluations']:
    c = ptr(release_cases, q['json_pointer'])
    require(digest(c) == q['record_sha256'] and len(c['parameter_values']) == 139, 'released object')
    require(c['reference_sha256'] == q['reference_sha256'] and c['metric'] == q['metric'], 'released metric/reference')
table = (R/providers['n6-table']['path']).read_bytes()
for q in nav['entries']:
    b = table[q['source_byte_start']:q['source_byte_start']+q['source_bytes']]
    require(sha(b) == q['source_row_sha256'] and table.splitlines(keepends=True)[q['source_line']-1] == b, 'N6 exact row')
canonical = (R/addition['path']).read_bytes()
append = addition['append_utf8'].encode()
require(sha(append) == addition['append_sha256'], 'append identity')
canonical_asof_available = (sha(canonical[:addition['before_bytes']]) == addition['before_sha256'] and canonical[addition['before_bytes']:addition['after_bytes']] == append)
# Current/as-of availability is reported, never a future gate on a mutable page.
# Independent data mutations must hit the relevant distinct assertions.
negatives = []
def reject(name, mutate):
    state = copy.deepcopy([ledger, inputs, nav, edges, preservation])
    mutate(*state)
    try:
        semantic(*state)
    except AssertionError:
        negatives.append(name)
    else:
        raise AssertionError('unsafe fixture accepted: '+name)
reject('numeric oracle promotion', lambda l,i,n,e,p: l['rows'][0].update(new_expected=1))
reject('actual pass promotion', lambda l,i,n,e,p: l['rows'][0].update(new_actual='pass'))
reject('whole family complete', lambda l,i,n,e,p: l.update(whole_family_complete=True))
reject('drop requirement context', lambda l,i,n,e,p: l['rows'].__setitem__(0,dict(l['rows'][0], requirement='REQ-OTHER')))
reject('count all renders as released', lambda l,i,n,e,p: i.update(released_count=41))
reject('lose zero-mode omission', lambda l,i,n,e,p: i['ungraded_retained_fixtures'].remove('DCL-014'))
reject('lose noise omission', lambda l,i,n,e,p: i['ungraded_retained_fixtures'].remove('DCL-033'))
reject('transfer Pipe budget', lambda l,i,n,e,p: i['released_evaluations'][0].update(metric={'kind':'stereo_relative_rms','maximum':.003}))
reject('generic mixer instance proved', lambda l,i,n,e,p: e['edges'][0].update(status='proved'))
reject('static becomes runtime', lambda l,i,n,e,p: e['edges'][1].update(runtime_sequence_proved=True))
reject('current extras used', lambda l,i,n,e,p: p['logical_mapping'].update({'results/collision.json':'results/collision.json'}))
reject('missing parameter navigation', lambda l,i,n,e,p: n['entries'].pop())
print(json.dumps({'status':'PASS','route_rows':84,'routes':ledger['counts'],'source_spans':len(spans),'JSON_pointers':len(evidence['json_pointers']),'original_payloads':103,'recovery_payloads':len(recovery['files']),'retained_render_script_pairs':41,'summary_only_sets':len(inputs['summary_only_sets']),'released_evaluations':2,'host_indices':139,'negative_fixtures':negatives,'selected_providers':len(pins['providers']),'mutable_asof_comparison':asof,'skipped_unavailable_asof_spans':skipped_asof_spans,'canonical_asof_available':canonical_asof_available,'excluded_current_path_asof':excluded_asof,'scope':'stdlib data/hash/text only; zero audio decode, metrics, old-script imports/replay, original/provider/decoder/harness execution; integrity not semantic completeness'},indent=2))
