#!/usr/bin/env python3
"""Read-only map integrity. No bytecode import, native calls or value-model execution."""
import sys
if sys.argv[1:] != ['--check']:
    raise SystemExit('read-only: use --check; no writes/replays')
import collections
import copy
import hashlib
import json
import pathlib
D = pathlib.Path(__file__).resolve().parent
R = D.parents[3]
def load(p):
    return json.loads(p.read_text())
def sha(b):
    return hashlib.sha256(b).hexdigest()
def digest(v):
    return sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def need(ok, message):
    if not ok:
        raise AssertionError(message)
def ptr(d, p):
    for k in p.lstrip('/').split('/') if p else []:
        k = k.replace('~1','/').replace('~0','~')
        d = d[int(k)] if isinstance(d,list) else d[k]
    return d
pins = load(D/'pins.json')['providers']
providers = {q['id']:q for q in pins}
l = load(D/'route-ledger.json')
i = load(D/'input-sets.json')
e = load(D/'chain-edges.json')
c = load(D/'control-domains.json')
a = load(D/'canonical-addition.json')
spans = load(D/'source-spans.json')['spans']
basis = load(D/'evidence-locators.json')
def invariants(l,i,e,c):
    rows = l['rows']
    need(len(rows)==94 and len({q['id'] for q in rows})==94, '94 distinct local contexts')
    need(l['denominator'] is None and not l['whole_family_complete'] and l['new_grade_count']==0, 'no denominator/grade')
    need(collections.Counter(q['route'] for q in rows)=={'X':19,'S':31,'no-established-route':44}, 'route counts')
    need(l['counts']==dict(collections.Counter(q['route'] for q in rows)), 'declared counts')
    need({q['requirement'] for q in rows}=={f'REQ-MIDI-USER-{v:03}' for v in range(1,14)}, '13 requirement contexts')
    need(all(q['new_expected'] is None and q['new_actual'] is None and q['new_grade']=='unchanged' for q in rows), 'null new grading')
    need(sum('REQ-MIDI-USER-010' in q['also_requirements'] for q in rows)==2 and sum('REQ-MIDI-USER-012' in q['also_requirements'] for q in rows)==5, 'shared aliases not new outcomes')
    need(len(i['cases'])==161 and [q['id'] for q in i['cases']]==[f'MIDI-CONFIG-{v:03}' for v in range(1,162)], '161 navigation units')
    need(sum(q['value_case'] for q in i['cases'])==52 and i['configuration_only_count']==109, '109 interpretation /52 value')
    need(i['static_derived_objects']==127 and i['extracted_execution_objects']==34, 'provenance split')
    need([q['id'] for q in i['MT_rows']]==[f'MT-{v:02}' for v in range(1,57)], '56 MT rows')
    need(i['MT_counts']=={'S':18,'S-cond':4,'X':34} and dict(collections.Counter(q['current_owner_label'] for q in i['MT_rows']))==i['MT_counts'], 'current MT labels')
    need(i['excluded_MT']==['MT-17','MT-18','MT-43','MT-44'], 'onoff omissions')
    need([q['id'] for q in i['MT_rows'] if q['released_id'] is None]==i['excluded_MT'], 'unreleased onoff')
    need(all(q['current_owner_label']=='S-cond' for q in i['MT_rows'] if q['id'] in i['excluded_MT']), 'onoff stays conditional')
    need(not i['execution_authorized'] and i['fresh_leaf_calls']==0, 'no new execution')
    need(e['edges'][0]['status']=='UNKNOWN' and e['edges'][-2]['status']=='UNKNOWN' and e['edges'][-1]['status']=='UNKNOWN', 'ingress/setter/deferred gaps')
    need(not any(q['runtime_sequence_proved'] for q in e['edges']), 'static is not runtime')
    need(len(c['mode_tokens'])==10 and len(set(c['mode_tokens']))==10 and 'LinearTwoCompliment' in c['mode_tokens'], 'exact ten tokens')
    need(sum(q['count'] for q in c['ordinary_key_families'])==103 and c['per_control_channel_keys']==27, 'key domain counts')
    need(c['precision_scope']['boundary_case_ids']==[149]+list(range(152,162)), 'boundary exceptions')
    need(c['precision_scope']['move_case_ids']==[129,133,137,138,143,144,145,153,155,161], 'move exceptions')
    need(c['precision_scope']['repeated_relative']=='k*tau for k consecutive nonstepped relativemessages', 'relative accumulation')
invariants(l,i,e,c)
# Wiki identities are author-as-of, never future live-file gates.
asof=[]
for q in pins:
    b=(R/q['path']).read_bytes()
    if q['id']=='research-before':
        b=b[:q['bytes']]
    same=len(b)==q['bytes'] and sha(b)==q['sha256']
    if q['kind']=='mutable-asof':
        asof.append({'id':q['id'],'current_equals_author_asof':same})
    else:
        need(same,'immutable pin '+q['id'])
available={providers[q['id']]['path']:q['current_equals_author_asof'] for q in asof}
skipped=[]
spanmap={q['id']:q for q in spans}
for q in spans:
    if not available.get(q['path'],True):
        skipped.append(q['id'])
        continue
    b=(R/q['path']).read_bytes()
    section=b[q['byte_start']:q['byte_end']]
    need(sha(section)==q['sha256'],'span bytehash '+q['id'])
    need(b''.join(b.splitlines(keepends=True)[q['line_start']-1:q['line_end']])==section,'span lines '+q['id'])
for q in basis['json_pointers']:
    v=ptr(load(R/providers[q['provider']]['path']),q['json_pointer'])
    need(digest(v)==q['record_sha256'],'evidence pointer '+q['id'])
known={q['id'] for q in basis['json_pointers']}|{q['id'] for q in basis['source_roles']}
for q in l['rows']:
    need(q['source_span'] in spanmap and set(q['evidence'])<=known,'row source')
    need(set(q['MT_navigation'])<={v['id'] for v in i['MT_rows']},'row MT navigation')
release=load(R/providers['release-cases']['path'])
trace=load(R/providers['traceability']['path'])
release_root=(R/providers['release']['path']).parent
for q in i['cases']:
    old=ptr(release,q['json_pointer'])
    need(digest(old)==q['record_sha256'],'immutable case '+q['id'])
    need(q['requirements']==old['requirements'] and q['expectation_provenance']==old['expectation_provenance'],'case provenance')
    b=(release_root/q['fixture']).read_bytes()
    need(len(b)==q['fixture_bytes'] and sha(b)==q['fixture_sha256'],'fixture bytes '+q['id'])
    need(digest(ptr(trace,q['trace_pointer']))==q['trace_sha256'],'old case trace')
    need(q['new_expected'] is None and q['new_actual'] is None,'no new case oracle')
    if q['value_case']:
        s=old['stimulus']
        need(digest(s['parameter'])==q['parameter_sha256'] and len(s['messages'])==q['message_count'] and s['takeover']==q['takeover'],'value input metadata')
for q in i['MT_rows']:
    s=spanmap[q['source_span']]
    need(s['sha256']==q['row_sha256'],'MT row identity')
    old=ptr(load(R/providers[q['source_provider']]['path']),q['source_json_pointer'])
    need(old['id']==q['id'] and digest(old)==q['source_record_sha256'],'MT source record')
    if q['released_id']:
        need(q['released_id'] in trace['cases'] and any(v['id']==q['released_id'] for v in i['cases']),'MT release navigation')
        tr=trace['cases'][q['released_id']]
        need(q['id'] in (tr.get('x_corroboration','')+' '+tr.get('source','')+' '+tr.get('x_result','')),'actual MT trace association')
need(len({q['released_id'] for q in i['MT_rows'] if q['released_id']})==52,'52 unique value mappings')
canonical=(R/a['path']).read_bytes()
append=a['append_utf8'].encode()
need(sha(append)==a['append_sha256'],'append identity')
canonical_asof=(sha(canonical[:a['before_bytes']])==a['before_sha256'] and canonical[a['before_bytes']:a['after_bytes']]==append)
# Joint semantic mutations: wrong route/grade/precision/source-role promotions.
negatives=[]
def reject(name,mutate):
    state=copy.deepcopy([l,i,e,c])
    mutate(*state)
    try:
        invariants(*state)
    except AssertionError:
        negatives.append(name)
    else:
        raise AssertionError('unsafe fixture accepted '+name)
reject('normative numeric oracle',lambda l,i,e,c:l['rows'][0].update(new_expected=1))
reject('actual candidate pass',lambda l,i,e,c:l['rows'][0].update(new_actual='pass'))
reject('whole family complete',lambda l,i,e,c:l.update(whole_family_complete=True))
reject('case count is denominator',lambda l,i,e,c:l.update(denominator=161))
reject('missing requirement context',lambda l,i,e,c:l['rows'][0].update(requirement='REQ-OTHER'))
reject('duplicate alias outcomes',lambda l,i,e,c:l['rows'][0]['also_requirements'].append('REQ-MIDI-USER-010'))
reject('promote onoff to released',lambda l,i,e,c:i['MT_rows'][16].update(released_id='MIDI-CONFIG-128'))
reject('promote onoff source label',lambda l,i,e,c:i['MT_rows'][16].update(current_owner_label='X'))
reject('generic scheduler proves ingress',lambda l,i,e,c:e['edges'][0].update(status='proved'))
reject('real setter proved',lambda l,i,e,c:e['edges'][-2].update(status='proved'))
reject('source sequence runtime',lambda l,i,e,c:e['edges'][1].update(runtime_sequence_proved=True))
reject('new execution selected',lambda l,i,e,c:i.update(execution_authorized=True))
reject('forget near bound exception scope',lambda l,i,e,c:c['precision_scope']['boundary_case_ids'].append(148))
reject('widen scaling moves',lambda l,i,e,c:c['precision_scope']['move_case_ids'].append(130))
reject('forget accumulated tolerance',lambda l,i,e,c:c['precision_scope'].update(repeated_relative='tau always'))
print(json.dumps({'status':'PASS','rows':94,'routes':l['counts'],'source_spans':len(spans),'evidence_pointers':len(basis['json_pointers']),'providers':len(pins),'case_objects':161,'fixture_byte_identities':161,'MT_rows':56,'MT_labels':i['MT_counts'],'released_value_navigation':52,'negative_fixtures':negatives,'mutable_asof':asof,'skipped_unavailable_asof_spans':skipped,'canonical_prefix_and_append_available':canonical_asof,'scope':'stdlib JSON/text/hash only; no oldmodule import/comparator/model/value calculation/audio/native/provider/decoder/tool/harness run'},indent=2))
