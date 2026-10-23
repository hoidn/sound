"""Read-only stdlib map integrity; no inherited source/helper execution."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def guards(ledger, census, scope):
    assert len(ledger['requirements']) == 23 and len(ledger['case_navigation']) == 34
    assert ledger['required_predicates'] == ledger['application_no_established_route'] == len(ledger['predicates']) == 91
    assert ledger['documentary_annotations_not_extra_outcomes'] == 46
    assert ledger['total_context_records'] == len(ledger['contexts']) == 137
    assert len({x['id'] for x in ledger['predicates']}) == 91
    assert ledger['retained_file_S'] == ledger['X'] == ledger['new_native_site_credit'] == 0
    assert ledger['target_application_outcomes_all_U'] and not ledger['whole_product_denominator']
    assert ledger['helper_only_records_auxiliary'] and ledger['selected_successor'] is None
    predicates = {x['id']: x for x in ledger['predicates']}
    assert set(predicates) == {x for r in ledger['requirements'] for x in r['predicate_ids']}
    ctx = collections.defaultdict(list)
    for row in ledger['contexts']:
        pred = predicates[row['predicate_id']]
        assert row['requirement'] == pred['requirement']
        assert not row['extra_required_predicate']
        assert row['actual'] is row['comparison'] is row['new_grade'] is row['native_PC_basis'] is None
        assert row['missing_joins']
        if row['context'] == 'documentary':
            assert row['route'] == 'no-established-exact-target-route'
            assert row['route_basis'] == 'D12-SOURCE-ONLY' and row['documentary_evidence'] == 'D12'
            assert row['record_kind'] == 'source-evidence-annotation'
        else:
            assert row['context'] == 'target-application' and row['route'] == 'no-established-route'
            assert row['route_basis'] == 'U-APP'
        ctx[pred['id']].append(row['context'])
    for pred in predicates.values():
        assert ctx[pred['id']] == (['documentary', 'target-application'] if pred['predicate_provenance']=='D12' else ['target-application'])
        assert pred['numeric_input_instances_are_context']
    assert census['selected_table_count'] == census['caps']['tables'] == 32
    assert census['selected_slots'] == 150 <= census['caps']['selected_slots'] == 512
    assert census['available_prefix_slots'] == 845 and census['omitted_prefix_slots'] == 695
    assert census['selected_counts'] == {'table-prefix':32, 'store-candidate':63, 'alias':184, 'membership':35}
    assert census['selected_counts']['store-candidate'] <= census['caps']['stores'] == 128
    assert census['combined_alias_membership'] == 219 <= census['caps']['combined_alias_membership'] == 512
    assert census['combined_call_indirect'] == 71 <= census['caps']['call_indirect'] == 512
    assert census['call_rows'] == 61 and census['indirect_rows'] == census['unresolved_indirect_rows'] == 10
    assert not census['actual_encoding_writer_route_established'] and census['no_body_expansion']
    assert census['new_C_bodies_read'] == census['new_native_reads'] == census['new_native_site_credit'] == 0
    assert census['selected_successor'] is None
    assert len(scope['source_sections']) == 6 and scope['source_section_semantics_inherited']
    assert not scope['pixels_or_link_destinations_inspected']
    assert scope['case_results'] == 0 and not scope['source_or_fixture_outputs_are_export_results']
    expected = {'D12_is_exact_target_S':False, 'hardware_object_implies_realtime':False,
        'physical_gap_implies_detected_dropout':False, 'dropout_restart_requires_actual_Live_detection':True,
        'video_requires_Arrangement_video_and_PCM':True, 'EXP023_requires_both_encoder_classes':True,
        'EXP009_toggles_inclusion_with_productive_enabled_effects':True,
        'realtime_cancel_is_general_atomic_cleanup':False, 'metadata_or_header_proves_numeric_DSP':False,
        'ASD_bytes_are_owned_by_this_contract':False, 'Dither32_inherits_sub32_default':False,
        'new_file_output_or_audio_observed':False}
    assert scope['semantic_guards'] == expected


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only; no collector/provider/decoder/source-body/model/write mode.')
    ledger, census, scope, pins = [load(n) for n in ['route-ledger.json','query-census.json','source-scope.json','pins.json']]
    guards(ledger, census, scope)
    providers = {}
    for pin in pins['providers']:
        path = ROOT / pin['path']
        assert path.suffix in {'.json','.md','.html'}
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], pin['id']
        providers[pin['id']] = raw
    manifest = json.loads(providers['owner-manifest'])
    review = json.loads(providers['owner-review'])
    assert review['final_manifest_sha256'] == sha(providers['owner-manifest'])
    assert review['disposition'].startswith('approved as partial documented-domain')
    reviewed = {x['path']:x for x in review['reviewed_payloads']}
    assert reviewed['wiki/specs/audio-video-export.md']['sha256'] == sha(providers['owner'])
    casepath = next(x['path'] for x in pins['providers'] if x['id']=='cases')
    assert reviewed[casepath]['sha256'] == sha(providers['cases'])
    assert manifest['source']['sha256'] == sha(providers['manual'])
    assert sha(providers['manual']) == scope['source_html_sha256']
    source = json.loads(providers['manual-metadata'])
    assert source['captured_utc'] == scope['source_capture_utc']
    assert source['bytes'] == scope['all_chapter_bytes'] == len(providers['manual']) == 320889
    assert '5.4' in providers['ManagingFiles-audit-scope'].decode()
    assert 'sections5.1–5.3 media/export are outside this audit' in providers['ManagingFiles-audit-scope'].decode()
    assert not pins['unreviewed_Recording_dependency']
    owner = providers['owner'].decode()
    lines = owner.splitlines()
    req = {}
    for i, line in enumerate(lines,1):
        if line.startswith('| REQ-EXPORT-'):
            v = [x.strip() for x in line.strip('|').split('|')]
            req[v[0]] = dict(input=v[1],result=v[2],evidence=v[3],line=i,sha256=sha(line.encode()))
    assert len(req) == 23
    clause = load('clause-index.json')
    assert clause['requirements'] == ledger['requirements']
    assert clause['owner_sha256'] == sha(providers['owner'])
    assert {r['id'] for r in ledger['requirements']} == set(req)
    cases = json.loads(providers['cases'])['cases']
    assert len(cases) == 34 and {c['id'] for c in cases} == set(clause['case_ids'])
    for pred in ledger['predicates']:
        r = req[pred['requirement']]
        s = pred['source']
        assert s['owner_row_line'] == r['line'] and s['owner_row_sha256'] == r['sha256']
        a,z = s['text_chars']
        assert r[s['column']][a:z] == s['anchor']
        assert pred['stated_context'] == r['input']
        assert pred['case_navigation'] == [c['id'] for c in cases if c['requirement_suffix']==pred['requirement'][-3:]]
    for nav, case in zip(ledger['case_navigation'],cases):
        assert nav['id'] == case['id']
        assert sha((json.dumps(case,sort_keys=True,separators=(',',':'))+'\n').encode()) == nav['object_sha256']
        assert cases[int(nav['source_pointer'].split('/')[-1])]['id'] == nav['id']
        assert nav['actual'] is nav['new_grade'] is None
        # All34 original case rows remain exact,not merely the case IDs.
        expected = '| ' + ' | '.join([case['id'],case['requirement_suffix'],case['kind'],case['action'],case['comparator_and_limits']]) + ' |'
        assert expected in lines
    bycase = {c['id']:c for c in cases}
    assert 'acknowledged/detected by Live' in bycase['EXP-027']['action']
    assert 'effects enabled' in bycase['EXP-009']['action'] and 'send nonzero' in bycase['EXP-009']['action']
    assert 'configurable and nonconfigurable' in bycase['EXP-023']['action']
    assert '32-bit' in bycase['EXP-018']['action']
    html = providers['manual'].decode()
    for loc in scope['source_sections']:
        part = html[loc['char_start']:loc['char_end']]
        assert sha(part.encode()) == loc['span_sha256']
        assert len(part.encode()) == loc['utf8_bytes']
        assert len(html[:loc['char_start']].encode()) == loc['utf8_byte_start']
        assert html[:loc['char_start']].count('\n')+1 == loc['html_line']
        assert 'id="'+loc['anchor']+'"' in part[:200]
    metadata = [json.loads(x) for x in (HERE/'metadata-rows.jsonl').read_text().splitlines()]
    calls = [json.loads(x) for x in (HERE/'call-rows.jsonl').read_text().splitlines()]
    assert collections.Counter(x['kind'] for x in metadata) == census['selected_counts']
    assert len(calls) == 71 and sum(x['kind']=='indirect' for x in calls) == 10
    auth = {x['path']:x for x in pins['metadata_authority']}
    parent = {x['path']:x for x in json.loads(providers['component'])['files']}
    idx = {x['path']:x for x in json.loads(providers['index-authority'])['retained_indexes_verified']}
    for authority in auth.values():
        original = idx[authority['path']] if authority['path'] in idx else parent[Path(authority['path']).name]
        assert original['bytes'] == authority['bytes'] and original['sha256'] == authority['sha256']
    models = set(census['selected_model_encodings'])
    small = set(census['selected_small_boundary_encodings'])
    table_count = available = slots = model_slots = small_slots = 0
    for item in metadata+calls:
        loc = item['locator']
        assert loc['path'] in auth
        path = Path(loc['path'])
        path = path if path.is_absolute() else ROOT/path
        with path.open('rb') as stream:
            stream.seek(loc['byte_start'])
            raw = stream.read(loc['bytes'])
        assert sha(raw) == loc['raw_sha256']
        original = json.loads(raw)
        if item['kind']=='table-prefix':
            rec = item['record']
            name = original['literal_type_encoding']
            assert name in models|small
            assert rec['slots'] == (original['slots'][:3] if name in models else original['slots'])
            assert rec['available_exported_prefix_slots'] == len(original['slots'])
            assert rec['native_table_extent'] is None
            assert not rec['complete_class_or_processing_interface_established']
            assert not rec['actual_export_instance_established']
            table_count += 1
            available += len(original['slots'])
            slots += len(rec['slots'])
            if name in models:
                model_slots += len(rec['slots'])
            else:
                small_slots += len(rec['slots'])
        else:
            assert item['record'] == original
        if item['kind']=='indirect':
            assert not original['resolved_targets']
    assert (table_count,available,slots,model_slots,small_slots)==(32,845,150,48,102)
    prospective = load('prospective-frontiers.json')
    assert len(prospective['candidates']) == 14
    assert prospective['candidate_original_batch'] is prospective['selected_successor'] is None
    for row in prospective['candidates']:
        assert not row['callable_input_state_abi_established'] and not row['standalone_original_route']
        assert not row['actual_export_instance'] and not row['selected_for_body_or_execution']
    edges = load('chain-edges.json')
    assert edges['metadata_rows'] == len(metadata) == 314 and len(edges['edges'])==12
    assert edges['new_native_site_credit'] == edges['new_public_routes'] == edges['X_export_routes'] == 0
    assert not edges['unreviewed_Recording_dependency'] and edges['selected_successor'] is None
    change = load('research-change.json')
    assert pins['research_change'] == change
    research = (ROOT/change['path']).read_bytes()
    prefix = research[:change['prefix_bytes_after_date_update']]
    assert sha(prefix) == change['prefix_sha256_after_date_update']
    assert sha(prefix.replace(b'updated: 2026-10-20',b'updated: 2026-10-19',1)) == change['original_prefix_sha256']
    start,size = change['append_start_byte'],change['append_bytes']
    assert sha(research[start:start+size]) == change['append_sha256']
    negatives = []

    def reject(name, mutation):
        l,c,s = copy.deepcopy((ledger,census,scope))
        mutation(l,c,s)
        try:
            guards(l,c,s)
        except (AssertionError,KeyError):
            negatives.append(dict(name=name,status='rejected'))
        else:
            raise AssertionError('unsafe mutation accepted: '+name)

    reject('required predicate omitted',lambda l,c,s:l['predicates'].pop())
    reject('numeric format choice counted as extra outcome',lambda l,c,s:l['contexts'].append(l['contexts'][0]))
    reject('D12 annotation promoted to target S',lambda l,c,s:l['contexts'][0].update(route='S'))
    reject('historical header becomes export DSP proof',lambda l,c,s:s['semantic_guards'].update(metadata_or_header_proves_numeric_DSP=True))
    reject('physical gap implies detected dropout',lambda l,c,s:s['semantic_guards'].update(physical_gap_implies_detected_dropout=True))
    reject('single encoder class sufficient for EXP023',lambda l,c,s:s['semantic_guards'].update(EXP023_requires_both_encoder_classes=False))
    reject('general cancel inherits atomic deletion',lambda l,c,s:s['semantic_guards'].update(realtime_cancel_is_general_atomic_cleanup=True))
    reject('32bit inherits sub32 dither default',lambda l,c,s:s['semantic_guards'].update(Dither32_inherits_sub32_default=True))
    reject('model slot window widened arbitrarily',lambda l,c,s:c.update(selected_slots=512))
    reject('alias membership cap exceeded',lambda l,c,s:c.update(combined_alias_membership=513))
    reject('unresolved indirect silently resolved',lambda l,c,s:c.update(unresolved_indirect_rows=0))
    reject('writer name becomes legal original route',lambda l,c,s:c.update(actual_encoding_writer_route_established=True))
    for target in re.findall(r'\]\(([^)]+)\)',(HERE/'structure.md').read_text()):
        assert (HERE/target.split('#')[0]).is_file(),target
    for path in HERE.iterdir():
        if path.suffix in {'.json','.jsonl','.md','.py'}:
            assert not any(line.rstrip()!=line for line in path.read_text().splitlines()),path
    if (HERE/'manifest.json').is_file():
        for f in load('manifest.json')['files']:
            raw = (HERE/f['path']).read_bytes()
            assert len(raw)==f['bytes'] and sha(raw)==f['sha256']
    print(json.dumps(dict(status='PASS-bounded-export-family-data-check',requirements=23,cases=34,
        required_application_predicates=91,application_routes_unestablished=91,
        D12_source_annotations_not_extra_outcomes=46,total_context_records=137,X=0,retained_file_S=0,
        selected_tables=32,available_prefix_slots=845,selected_slots=150,omitted_prefix_slots=695,
        stores=63,aliases=184,memberships=35,boundary_seeds=37,call_rows=61,
        unresolved_indirect_rows=10,selected_provider_pins=len(pins['providers']),
        new_body_native_or_binary_reads=0,new_original_model_comparator_runs=0,new_native_site_credit=0,
        selected_successor=None,research_preserved_except_date_and_append=True,
        negative_controls=negatives,
        checked_scope='All owner/case pointers,selected source section geometry andmetadata exactrows/pins. Original export semantics,1a recovery and1b source/callback associations inherited. ManagingFiles132context audit does not cover export. No old helper/provider/decoder/sourcebody/native/original/model/comparator/fixture or whole old universe replay.'),indent=2))


if __name__=='__main__':
    main()
