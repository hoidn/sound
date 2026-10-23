"""Read-only stdlib packet integrity; no old imports or reference execution."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import sys

P = Path(__file__).resolve().parent
F = P.parent
R = F.parents[2]
D = F / 'delay-reverb'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def j(p):
    return json.loads(p.read_bytes())


def objhash(x):
    return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())


def pin(p):
    b = Path(p['path']).read_bytes()
    need(len(b) == p['bytes'] and sha(b) == p['sha256'], 'changed selected source pin')


def span(s, body):
    b = body[s['byte_start']:s['byte_start']+s['byte_length']]
    need(len(b) == s['byte_length'] and sha(b) == s['sha256'], 'changed owner span')
    need(body[:s['byte_start']].count(b'\n')+1 == s['line_start'], 'owner line locator')


def ledger_check(x, reqs, body):
    rows = x['required_outcomes']
    need(len(rows) == x['required_outcome_rows'] == 562, 'bounded predicate count')
    need(len({r['id'] for r in rows}) == len(rows), 'duplicate outcome id')
    need(len({(r['requirement'],r['device'],r['predicate']) for r in rows}) == len(rows), 'duplicate predicate')
    byid = {r['id']:r for r in reqs}
    need({r['requirement'] for r in rows if r['requirement']} == set(byid), 'missing owner clause')
    units = {}
    for line in (P/'predicate-units.tsv').read_text().splitlines():
        k, v = line.split('\t'); units['REQ-DR-'+k] = v.split('|')
    for requirement, source in byid.items():
        rs = [r for r in rows if r['requirement'] == requirement]
        if requirement in units:
            need([r['predicate'] for r in rs] == units[requirement], 'curated predicate units')
        else:
            need(len(rs) == 17 and source['provenance'] == 'U', 'unresolved observable domains')
        for r in rs:
            span(r['source'], body)
            s = r['source']; text = body[s['byte_start']:s['byte_start']+s['byte_length']].decode()
            need(text == source['text'] and r['source_annotation'] == source['provenance'], 'exact parent body/source label')
    side = [r for r in rows if r['requirement'] is None]
    need(len(side) == 7 and {r['device'] for r in side} == {r['device'] for r in reqs}, 'sidechain contexts not case padding')
    for r in rows:
        span(r['source'], body)
        need(r['route'] == 'no-established-route' and r['actual_status'] == 'U'
             and r['public_binding'] == 'unknown' and not r['grade_changed'], 'no public promotion')
        need(r['missing_join'] and r['enumeration'] and r['related_cases_navigation_only'], 'missing join/enumeration/cases')
        need(not r['id'].startswith('DR-AUX'), 'helper/file outcome padding')
    need(x['route_inventory'] == dict(X_route=0,S_route=0,no_established_route=562), 'route count is inventory only')
    need(collections.Counter(r['source_annotation'] for r in rows) == {'D12':316,'U':246}, 'source annotation accounting')
    need(len(x['auxiliary']) == 7, 'file auxiliary count')
    need(all(not r['required_outcome'] and r['route'] == 'S-route' and not r['raw_reopened'] for r in x['auxiliary']), 'file-only boundary')


def native_row(row):
    with Path(row['provider']).open('rb') as f:
        f.seek(row['source_byte']); raw = f.read(row['raw_bytes'])
    need(sha(raw) == row['raw_sha256'] and raw.endswith(b'\n'), 'native DATA row identity')
    original = json.loads(raw)
    retained = row['record']
    if row['kind'] == 'table-data':
        expected = dict(original)
        expected['exported_prefix_slot_count'] = len(original['slots'])
        expected['selected_slot_policy'] = ('large header/store plus leading3 construction/lifetime prefix only'
                                          if len(original['slots']) > 16 else 'whole small retained exported prefix')
        expected['slots'] = original['slots'][:3] if len(original['slots']) > 16 else original['slots']
        expected['not_complete_native_extent_or_render_callback'] = True
        need(retained == expected, 'whole-small or large leading3 DATA projection')
    else:
        need(retained == original, 'exact DATA record')


def prerequisites(x):
    c = x['common']
    need(all(t in c['signal'] for t in ['NONEMPTY','NONZERO','EACH','BOTH']), 'productive signal prerequisites')
    h = x['devices']['hybrid-reverb']['engines'].lower()
    need(all(t in h for t in ['recognized valid owned nonidentity ir','nonzero convolution','algorithm separately productive','serial algorithm is convolution-fed','g18','saved reference']), 'Hybrid branch/list guards')
    need('remain U' in x['common']['lifecycle'], 'lifecycle remains unknown')


def prefix(x):
    b = Path(x['path']).read_bytes()[:x['bytes']]
    need(len(b) == x['bytes'] and sha(b) == x['sha256'], 'full historical research prefix')


def case_check(n, c, o):
    need(n['record_sha256'] == objhash(c) and n['field_sha256'] == {k:objhash(v) for k,v in c.items()}, 'all full case fields')
    need(c['exact_target_expected'] is None and c['exact_target_applicability'] == 'unknown', 'case target remains null')
    need(o['id'] == c['id'] and o['expected'] is None and o['comparison'] is None and o['target'] == 'U' and not o['executed'], 'actual overlay remains null')


def main():
    need(sys.argv[1:] == [], 'read-only check has no writer/provider modes')
    pins = j(P/'source-pins.json')['files']
    for p in pins:
        pin(p)
    body = (R/'wiki/specs/delay-reverb-devices.md').read_bytes()
    reqs, cases = j(D/'requirements-r3.json'), j(D/'cases-r3.json')
    need(len(reqs) == 93 and len(cases) == 176, 'owner counts')
    need(reqs[:92] == j(D/'requirements.json') and cases[:149] == j(D/'cases.json'), 'old objects exact')
    ledger = j(P/'route-ledger.json'); ledger_check(ledger,reqs,body)
    nav = j(P/'case-navigation.json')['cases']
    need([n['id'] for n in nav] == [c['id'] for c in cases], 'all current case navigation')
    overlays = j(D/'fixtures-r3.json')['current_version_overlay']['actual_oracles']
    for n,c,o in zip(nav,cases,overlays,strict=True):
        case_check(n,c,o)
    need(collections.Counter(c['provenance'] for c in cases) == {'D12':77,'Dpkg':7,'U':92}, 'case grades unchanged')
    native = [json.loads(b) for b in (P/'native-data.jsonl').read_bytes().splitlines()]
    need(len(native) == 690, 'selected DATA row count')
    for n in native:
        native_row(n)
    census = j(P/'metadata-census.json'); counts = census['counts']
    need(census['within_caps'] and [counts[k] for k in ['tables','selected_slots','stores','aliases_plus_memberships','calls_plus_indirect']] == [29,91,43,264,195], 'approved metadata caps')
    ass = j(P/'processor-associations.json')
    need(len(ass) == 7 and sum(len(x['table_rows']) for x in ass.values()) == 29
         and sum(len(x['store_rows']) for x in ass.values()) == 43
         and sum(len(x['aliases']) for x in ass.values()) == 132, 'whole family associations')
    need(len({i for x in ass.values() for i in x['table_rows']}) == 29, 'unique table partition')
    for a in ass.values():
        need(a['new_resolved_indirect_sites'] == 0 and all(v['C_source'] is None and not v['C_body_selected'] for v in a['aliases']), 'no unselected body or site promotion')
    need(all(not b['callable_X_leaves_established'] for b in j(P/'batch-inputs.json').values()), 'no invented callable batch')
    geometry = j(P/'source-geometry.json'); audit = j(F/'delay-reverb-source-audit/audit.json')
    html = Path(geometry['source']['path']).read_text()
    need(len(geometry['blocks']) == len(audit['blocks']) == 207, 'source geometry count')
    for g,b in zip(geometry['blocks'],audit['blocks'],strict=True):
        need(html[g['character_start']:g['character_end']] == b['raw_html'] and sha(b['raw_html'].encode()) == g['raw_utf8_sha256'], 'source raw span geometry')
    prerequisites(j(P/'prerequisites.json')); prefix(j(P/'research-prefix.json'))
    negatives = []
    def reject(name, op):
        try: op()
        except (ValueError,KeyError,IndexError,TypeError): negatives.append(name)
        else: raise ValueError('negative accepted: '+name)
    bad = copy.deepcopy(ledger); bad['required_outcomes'].pop()
    reject('omitted predicate',lambda:ledger_check(bad,reqs,body))
    bad = copy.deepcopy(ledger); bad['required_outcomes'][1]['id'] = bad['required_outcomes'][0]['id']
    reject('duplicate outcome',lambda:ledger_check(bad,reqs,body))
    for field,value,label in [('route','X-route','metadata promoted X'),('route','S-route','D12 promoted public S'),('actual_status','pass','actual U promoted'),('public_binding','established','public receiver fabricated'),('enumeration','','unresolved enumeration omitted')]:
        bad = copy.deepcopy(ledger); bad['required_outcomes'][0][field] = value
        reject(label,lambda bad=bad:ledger_check(bad,reqs,body))
    bad = copy.deepcopy(ledger); bad['required_outcomes'][0]['source']['byte_start'] += 1
    reject('bad source span',lambda:ledger_check(bad,reqs,body))
    bad = copy.deepcopy(ledger); bad['auxiliary'][0]['required_outcome'] = True
    reject('file-only denominator padding',lambda:ledger_check(bad,reqs,body))
    bad = copy.deepcopy(ledger); bad['required_outcomes'][0]['requirement'] = 'REQ-DR-MISSING-999'
    reject('missing owner clause',lambda:ledger_check(bad,reqs,body))
    bad = copy.deepcopy(next(n for n in native if n['kind'] == 'table-data')); bad['record']['slots'][0]['target'] = '0x0'
    reject('arbitrary prefix slot substitution',lambda:native_row(bad))
    bad = copy.deepcopy(native[0]); bad['source_byte'] += 1
    reject('bad retained raw-row locator',lambda:native_row(bad))
    bad = copy.deepcopy(pins[0]); bad['sha256'] = '0'*64
    reject('changed source pin',lambda:pin(bad))
    bad = copy.deepcopy(j(P/'research-prefix.json')); bad['sha256'] = '0'*64
    reject('changed historical research prefix',lambda:prefix(bad))
    bad = copy.deepcopy(j(P/'prerequisites.json')); bad['common']['signal'] = 'Configured controls only'
    reject('vacuous signal baseline',lambda:prerequisites(bad))
    bad = copy.deepcopy(j(P/'prerequisites.json')); bad['devices']['hybrid-reverb']['engines'] = 'Raw Algorithm assumed in Serial'
    reject('Hybrid raw-Algorithm substitution',lambda:prerequisites(bad))
    bad = copy.deepcopy(cases[0]); bad['action'] = 'Role inspection substituted for actual movement'
    reject('changed complete case action',lambda:case_check(nav[0],bad,overlays[0]))
    bad = copy.deepcopy(cases[0]); bad['exact_target_expected'] = 0
    reject('finite target oracle invented',lambda:case_check(nav[0],bad,overlays[0]))
    bad = copy.deepcopy(overlays[0]); bad['expected'] = 0
    reject('actual overlay promoted',lambda:case_check(nav[0],cases[0],bad))
    bad = copy.deepcopy(ledger); bad['required_outcomes'].append(dict(bad['required_outcomes'][0],id='DR-AUX-PAD'))
    reject('helper denominator padding',lambda:ledger_check(bad,reqs,body))
    print(json.dumps(dict(status='PASS-data-only-author-integrity',required_predicates=562,
        routes=dict(X=0,S=0,no_established=562),source_annotations=dict(D12=316,U=246),
        auxiliary_file_S=7,requirements=93,cases=176,old_cases_exact=149,all_actual_U=176,
        selected_DATA_rows=690,tables=29,selected_slots=91,stores=43,source_pins=len(pins),
        geometry_blocks=207,negative_controls=negatives,new_C_bodies=0,new_original_calls=0,
        compatibility_grades=0,closure_gate='OPEN',write_modes=0),indent=2))


if __name__ == '__main__':
    main()
