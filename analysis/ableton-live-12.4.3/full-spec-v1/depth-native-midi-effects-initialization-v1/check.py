"""Read-only, stdlib verification of the fixed retained-data source batch.

Does not import author scripts, execute original code, or traverse new sources.
Negative controls alter in-memory data only. Prints JSON; writes no files.
"""
import collections
import copy
import hashlib
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent
R = P.parents[3]
F = P.parent
M = F / 'family-native-midi-effects-routes-v1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(name):
    return json.loads((P / name).read_text())


def expected_seeds():
    out = set()
    counts = collections.Counter()
    names = {'OMidi' + s + 'Processor' for s in (
        'Arpeggiator', 'CcControl', 'Chord', 'NoteLength', 'Pitcher',
        'Random', 'Scale', 'Velocity')}
    targets = set()
    for line in (M / 'native-data.jsonl').read_text().splitlines():
        row = json.loads(line)
        d = row['record']
        if row['kind'] == 'literal-store-candidate':
            out.add(d['entry'])
            counts['literal_store_rows'] += 1
        if row['kind'] == 'table-prefix-data':
            for slot in d['slots']:
                targets.add(slot['target'])
                out.add(slot['target'])
        if row['kind'] == 'selected-alias-data' and any(
                re.search(re.escape(n) + r'::(?:Init|Exit|Reset|OnOn)(?:>|\()', d['name'])
                for n in names):
            out.add(d.get('thunk_target') or d['entry'])
            counts['lifecycle_wrapper_rows'] += 1
    counts['distinct_prefix_targets'] = len(targets)
    return out, dict(counts)


def validate(bundle, seeds):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    raw_rows = bundle['raw_rows']
    records = [json.loads(raw) for raw in raw_rows]
    by = {x['entry']: x for x in records}
    loc = bundle['locators']
    census = bundle['census']
    require(set(by) == seeds and len(records) == len(seeds) == 74, 'fixed seed identity/uniqueness')
    if set(by) != seeds or len(records) != len(seeds):
        return errors
    require(len(records) <= 96, 'record cap')
    require(sum(len(x['code'].encode()) for x in records) <= 262144, 'C byte cap')
    require(max(len(x['code'].splitlines()) for x in records) <= 1500, 'C line cap')
    require(census['summary']['total_C_utf8_bytes'] == 118189, 'pre-gate byte census')
    require(census['summary']['within_caps'] is True, 'pre-gate census disposition')
    require(census['source_materialized'] is False and census['semantic_bodies_read'] is False,
            'historical pre-gate receipt')
    require({x['entry'] for x in loc['records']} == seeds, 'locator coverage')
    require({x['entry'] for x in census['records']} == seeds, 'census coverage')
    require(loc['retained_raw_sha256'] == digest(b''.join(raw_rows)), 'raw retained identity')
    off = 0
    for i, (raw, meta) in enumerate(zip(raw_rows, loc['records']), 1):
        d = json.loads(raw)
        require(d['entry'] == meta['entry'], 'record order')
        require(meta['retained_line'] == i and meta['retained_byte'] == off, 'retained locator')
        require(len(raw) == meta['raw_bytes'] and digest(raw) == meta['raw_sha256'], 'raw record hash')
        require(len(d['code'].encode()) == meta['code_bytes'] == d['code_bytes'], 'C byte identity')
        require(digest(d['code'].encode()) == meta['code_sha256'] == d['code_sha256'], 'C hash identity')
        require(len(d['code'].splitlines()) == meta['C_lines'], 'C line count')
        require(d['body_ranges'] == meta['native_body_ranges'] and d['body_bytes'] == meta['native_body_bytes'],
                'native extent identity')
        require(d['warnings'] == meta['warnings'] and d['thunk'] == meta['record_thunk'], 'source warnings/thunk')
        require(d['state'] == meta['state'] and d['state'] in ('exported', 'exported-with-warnings') and
                not d['error'] and not d['timed_out'] and not d['partial_code'],
                'complete retained source state')
        off += len(raw)
    require(off == loc['retained_raw_bytes'], 'retained total length')
    require(sum(x['body_bytes'] for x in records) == 14744, 'native extent census')
    require(sum(bool(x['thunk']) for x in records) == 10, 'retained thunk count')
    require(sum(len(x['code'].splitlines()) for x in records) == 4294, 'C total lines')
    require(sum(len(x['code'].encode()) for x in records) == 118189, 'C total bytes')
    pby = {x['entry']: x for x in bundle['projections']['expanded_projections']}
    require(len(pby) == 8, 'expanded projection inventory')
    norm = lambda t: re.sub(r'(?:thunk_)?FUN_[0-9a-f]+(?=\()', 'FUNCTION', t, count=1)
    for entry, p in pby.items():
        require(entry in by and by[entry]['body_bytes'] == p['native_bytes'] == 4, 'projection native bound')
        require(p['independent_native_implementation'] is False, 'projection independence prohibited')
        require(p['native_operations_attributed_to_entry'] is False, 'expanded native attribution prohibited')
        if p.get('same_projection_as'):
            other = p['same_projection_as']
            require(other in by and norm(by[entry]['code']) == norm(by[other]['code']), 'equal constructor projection')
            require(p['target_record_separately_selected'] is True, 'selected projection comparison')
        else:
            require(p['target_record_separately_selected'] is False, 'unselected tail body remains unread')
            require(p['next_target_from_predecessor_call_index'] not in by, 'tail target not expanded')
            require(bool(p.get('tail_reference')), 'tail reference provenance')
    account = bundle['assessments']
    require(account['read_complete'] is True and {x['entry'] for x in account['records']} == seeds,
            'complete selected read accounting')
    for a in account['records']:
        require(a['C_read'] == [1, len(by[a['entry']]['code'].splitlines())], 'complete bounded C read')
        require(a['native_operation_attribution_from_expanded_projection'] is False, 'account projection qualification')
    claims = bundle['claims']
    require(claims['new_resolved_indirect_sites'] == 0 and claims['new_X_routes'] == 0, 'no new site/X credit')
    require(claims['no_public_outcome_closed'] is True and len(claims['claims']) == 28, 'source claim scope')
    for c in claims['claims']:
        require(not c['public_outcome_closed'] and not c['new_X_route'] and not c['inspected_unselected_target_body'],
                'no public closure/unselected inspection')
        for e in c['evidence']:
            entry = e['entry']
            require(entry in by, 'claim inside fixed selection')
            lines = by[entry]['code'].splitlines(keepends=True)
            a, b = e['C_start'], e['C_end']
            require(1 <= a <= b <= len(lines), 'claim C range')
            require(digest(''.join(lines[a-1:b]).encode()) == e['C_span_sha256'], 'claim C span identity')
            require(e['native_PC'] is None and not e['native_operation_attribution_from_expanded_projection'],
                    'no invented native locator/attribution')
            if entry in pby:
                require(e['interpretation'].startswith('expanded-projection-only'), 'claim expanded qualification')
    cont = bundle['continuation']
    require(cont['predecessor_inventory_asof_only'] == {
        'rows': 309, 'documentary_D12': 91, 'U': 218,
        'routes': {'X': 0, 'S': 0, 'no-established-route': 309}, 'new_denominator_derived': False},
        'preserve as-of predecessor inventory')
    require(len(cont['rows']) == 8 and len({x['device'] for x in cont['rows']}) == 8, 'whole eight effects')
    require(cont['public_outcomes_closed'] == cont['new_indirect_site_resolution'] == 0, 'no closure/site credit')
    for row in cont['rows']:
        require(row['public_input_same_device_output_route'] == 'no-established-route' and
                not row['grade_or_owner_change'] and not row['new_X_route'], 'no public route/grade promotion')
    for x in bundle['frontiers']['rows']:
        require(x['source_entry'] in by and not x['followed'] and x['native_call_PC'] is None, 'bounded C frontier')
        require(x['selected_in_fixed_batch'] == (x['target'] in seeds), 'frontier membership')
    return errors


def main():
    bundle = {'raw_rows': (P / 'source-records.jsonl').read_bytes().splitlines(keepends=True),
              'locators': load('source-locators.json'), 'census': load('seed-census.json'),
              'claims': load('source-claims.json'), 'projections': load('projection-qualifications.json'),
              'assessments': load('record-assessments.json'), 'frontiers': load('call-frontiers.json'),
              'continuation': load('route-continuation.json')}
    seeds, selection_counts = expected_seeds()
    errors = validate(bundle, seeds)
    pins = load('source-pins.json')
    for pin in pins['pins'] + pins['approved_C1_chunk_pins']:
        path = pathlib.Path(pin['path'])
        if not path.is_absolute():
            path = R / path
        data = path.read_bytes()
        if len(data) != pin['bytes'] or digest(data) != pin['sha256']:
            errors.append('input pin: ' + str(path))
    approved = json.loads((F / 'component-resolution-v1/class-inputs.json').read_text())['decomp_chunk_pins']
    for pin in pins['approved_C1_chunk_pins']:
        if pin not in approved:
            errors.append('chunk pin not in approved packet 1a')
    for meta in bundle['locators']['records']:
        data = pathlib.Path(meta['source_path']).read_bytes()
        raw = data[meta['source_byte']:meta['source_byte'] + meta['raw_bytes']]
        if digest(raw) != meta['raw_sha256'] or data[:meta['source_byte']].count(b'\n') + 1 != meta['source_line']:
            errors.append('original locator: ' + meta['entry'])
    old_calls = [json.loads(l) for l in (M / 'selected-calls.jsonl').read_text().splitlines()]
    for projection in bundle['projections']['expanded_projections']:
        if projection.get('tail_reference'):
            ref = projection['tail_reference']
            old = old_calls[ref['retained_line'] - 1]
            if old['record']['caller'] != projection['entry'] or old['record']['to'] != ref['target'] or old['record']['site'] != ref['native_PC'] or old['raw_sha256'] != ref['provider_raw_sha256']:
                errors.append('inherited exact tail-reference identity')
    prefix = load('research-prefix.json')
    current = (R / prefix['path']).read_bytes()
    if digest(current[:prefix['bytes']]) != prefix['sha256'] or len(current) <= prefix['bytes']:
        errors.append('canonical full prefix/additive section')
    if b'Pending independent source review' not in current[prefix['bytes']:]:
        errors.append('canonical pending qualification')
    links = 0
    for page in [P / 'structure.md', R / prefix['path']]:
        text = page.read_text()
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', '#')):
                continue
            target = target.split('#')[0]
            if target and not (page.parent / target).resolve().exists():
                errors.append('local link: ' + target)
            links += 1
    fm = current.decode().split('---', 2)[1]
    for key in ['id:', 'type: research', 'status:', 'updated:', 'access: analysis', 'revision:', 'target:']:
        if key not in fm:
            errors.append('research frontmatter: ' + key)
    negatives = []

    def reject(name, mutate, expected_error):
        changed = copy.deepcopy(bundle)
        mutate(changed)
        mutation_errors = validate(changed, seeds)
        rejected = expected_error in mutation_errors
        negatives.append({'name': name, 'rejected': rejected, 'matched_guard': expected_error})
        if not rejected:
            errors.append('negative did not reject: ' + name)

    reject('omit selected record', lambda b: b['raw_rows'].pop(), 'fixed seed identity/uniqueness')
    reject('duplicate selected record', lambda b: b['raw_rows'].append(b['raw_rows'][0]), 'fixed seed identity/uniqueness')
    reject('corrupt pre-gate byte receipt', lambda b: b['census']['summary'].__setitem__('total_C_utf8_bytes', 262145), 'pre-gate byte census')
    reject('corrupt raw-source locator hash', lambda b: b['locators']['records'][0].__setitem__('raw_sha256', '0'*64), 'raw record hash')
    reject('corrupt claim source span', lambda b: b['claims']['claims'][0]['evidence'][0].__setitem__('C_span_sha256', '0'*64), 'claim C span identity')
    reject('invent native extent', lambda b: b['locators']['records'][0].__setitem__('native_body_bytes', 100), 'native extent identity')
    reject('expanded projection independent implementation', lambda b: b['projections']['expanded_projections'][0].__setitem__('independent_native_implementation', True), 'projection independence prohibited')
    reject('false-thunk tail body freshly inspected', lambda b: b['projections']['expanded_projections'][-1].__setitem__('target_record_separately_selected', True), 'unselected tail body remains unread')
    reject('helper promotes public observable', lambda b: b['claims']['claims'][0].__setitem__('public_outcome_closed', True), 'no public closure/unselected inspection')
    reject('partial route promotes grade', lambda b: b['continuation']['rows'][0].__setitem__('grade_or_owner_change', True), 'no public route/grade promotion')
    reject('drop whole-family device', lambda b: b['continuation']['rows'].pop(), 'whole eight effects')
    reject('rederive predecessor denominator', lambda b: b['continuation']['predecessor_inventory_asof_only'].__setitem__('new_denominator_derived', True), 'preserve as-of predecessor inventory')
    reject('autofollow encountered callee', lambda b: b['frontiers']['rows'][0].__setitem__('followed', True), 'bounded C frontier')

    def expand_C(b):
        d = json.loads(b['raw_rows'][0])
        d['code'] = ' ' * 262145
        b['raw_rows'][0] = (json.dumps(d) + '\n').encode()

    reject('C body exceeds byte cap', expand_C, 'C byte cap')
    out = {'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
           'scope': 'Read-only selected data, source integrity, bounded source claims and focused docs only; no semantic approval or execution.',
           'selection_counts': selection_counts, 'selected_records': len(seeds),
           'C_utf8_bytes': 118189, 'source_claims_not_outcomes': 28,
           'pinned_inputs': len(pins['pins']), 'approved_chunks': len(pins['approved_C1_chunk_pins']),
           'focused_links': links, 'negative_controls': negatives,
           'original_native_provider_decoder_calls': 0, 'new_resolved_indirect_sites': 0}
    print(json.dumps(out, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
