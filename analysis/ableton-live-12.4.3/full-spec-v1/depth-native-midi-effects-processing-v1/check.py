"""Read-only stdlib check of the approved fixed processing-source batch.

No original code, providers, decoders, old author modules or new source traversal.
Negative controls mutate in-memory projections only.
"""
import copy
import hashlib
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent
R = P.parents[3]
F = P.parent
M = F / 'family-native-midi-effects-routes-v1'
I = F / 'depth-native-midi-effects-initialization-v1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name):
    return json.loads((P / name).read_text())


def fixed_seeds():
    seeds = set()
    for line in (M / 'native-data.jsonl').read_text().splitlines():
        row = json.loads(line)
        d = row['record']
        if row['kind'] == 'selected-alias-data' and any(
                '::' + method + '>' in d['name'] for method in ('OnMidi', 'OnMidiEvent')):
            seeds.add(d.get('thunk_target') or d['entry'])
        if row['kind'] == 'table-prefix-data' and len(d['slots']) == 8:
            seeds.update(s['target'] for s in d['slots'] if s['offset'] in (24, 32, 48))
    return seeds


def validate(b, seeds):
    errors = []

    def req(ok, msg):
        if not ok:
            errors.append(msg)

    census = b['census']
    loc = b['locators']
    by = b['records']
    req(set(by) == seeds and len(by) == 17, 'exact17fixedseeds')
    if set(by) != seeds:
        return errors
    req(set(b['approval']['fixed_entries']) == seeds, 'approvedfixedselection')
    req({x['entry'] for x in loc['records']} == seeds, 'locatorcoverage')
    req({x['entry'] for x in census['records']} == seeds, 'censuscoverage')
    req(len(by) <= 64, 'recordcap')
    req(sum(len(x['code'].encode()) for x in by.values()) <= 196608, 'Cbytecap')
    req(max(len(x['code'].splitlines()) for x in by.values()) <= 1500, 'Clinecap')
    req(census['summary']['total_C_utf8_bytes'] == 50962 and
        census['summary']['total_C_lines'] == 1748 and census['summary']['max_C_lines'] == 327,
        'pinnedmetadatareceipt')
    req(census['new_C_materialized'] is False and census['new_C_bodies_semantically_read'] is False and
        census['approval_required_before_new_C'] is True, 'historicalpregateflags')
    req(loc['new_record_count'] == 3 and loc['inherited_record_count'] == 14 and loc['no_inherited_raw_copy'],
        'newversusinheritedcount')
    req(len(b['new_raw_rows']) == 3 and sha(b''.join(b['new_raw_rows'])) == loc['new_raw_sha256'],
        'only3newrawrows')
    req(sum(x['body_bytes'] for x in by.values()) == 7956, 'nativeextenttotal')
    req(sum(bool(x['thunk']) for x in by.values()) == 0, 'retainedthunkflags')
    req(sum(bool(x['warnings']) for x in by.values()) == 10, 'warningrecordcount')
    for meta in loc['records']:
        d = by[meta['entry']]
        req(len(d['code'].encode()) == meta['C_utf8_bytes'] and sha(d['code'].encode()) == meta['C_sha256'],
            'Cidentity')
        req(len(d['code'].splitlines()) == meta['C_lines'], 'Clines')
        req(d['body_ranges'] == meta['native_body_ranges'] and d['body_bytes'] == meta['native_body_bytes'],
            'nativeextentidentity')
        req(d['state'] == meta['state'] and d['state'] in ('exported', 'exported-with-warnings') and
            d['warnings'] == meta['warnings'] and not d['error'] and not d['timed_out'] and not d['partial_code'],
            'retainedwarningstate')
        inherited = meta['already_retained_and_read_in_initialization']
        req(inherited == ('depth-native-midi-effects-initialization-v1/' in meta['retained_path']),
            'inheritnotcopy')
    expanded = b['projections']['expanded']
    req(b['projections']['warnings'] == [
        {'entry': m['entry'], 'state': m['state'], 'warnings': m['warnings']}
        for m in loc['records'] if m['warnings']], 'allwarningqualifications')
    req({x['entry'] for x in expanded} == {'0x101c1a16c', '0x101f4e438'}, 'twodelegatedprojections')
    for p in expanded:
        req(p['native_bytes'] == by[p['entry']]['body_bytes'] == 4 and not p['record_thunk'] and not p['alias_thunk'],
            'fourbytenativebound')
        req(p['expanded_projection_only'] and not p['independent_native_implementation'] and
            not p['operations_attributed_to_native_entry'], 'expandednotnativeimplementation')
        req(not p['target_record_selected_or_read'] and p['target'] not in by, 'delegatedtargetunread')
    req(len(b['claims']['claims']) == 9, 'nineauxiliaryclaims')
    for c in b['claims']['claims']:
        req(c['entry'] in {'0x101c1a16c', '0x101c286c4', '0x101f4e438'}, 'newclaimselection')
        lines = by[c['entry']]['code'].splitlines(keepends=True)
        req(1 <= c['C_start'] <= c['C_end'] <= len(lines), 'claimrange')
        req(sha(''.join(lines[c['C_start']-1:c['C_end']]).encode()) == c['C_span_sha256'], 'claimspanidentity')
        req(c['expanded_projection_only'] == (c['entry'] != '0x101c286c4'), 'claimprojectionbound')
        req(not c['operations_attributed_to_four_byte_native_body'] and not c['target_body_freshly_inspected'],
            'nodelegatedbodyattribution')
        req(not c['public_outcome_closed'] and not c['X_route_established'] and c['native_PC'] is None,
            'nopublicXorPCpromotion')
        req(not c['total_native_control_flow_or_failure_law'], 'nototalnativefloworfailurelaw')
    whole = b['whole']
    req(len(whole['devices']) == 8 and len({x['device'] for x in whole['devices']}) == 8, 'whole8devices')
    req({e for d in whole['devices'] for e in d['entries']} == seeds, 'whole8entrycoverage')
    req(whole['complete_callable_X_leaves_established'] == whole['new_public_routes'] ==
        whole['new_resolved_indirect_sites'] == 0, 'noestablishedXleafornewcredit')
    req(whole['predecessor_inventory_unchanged'] == {
        'rows_asof': 309, 'documentary_D12': 91, 'U': 218,
        'routes_asof': {'X': 0, 'S': 0, 'no-established-route': 309}, 'new_denominator_derived': False},
        'predecessorasofinventory')
    for device in whole['devices']:
        req(device['X_route'] == 'no-established-route-in-selected-evidence' and
            device['public_delivery_route'] == 'no-established-route' and not device['new_public_outcome_or_grade'],
            'nopublicrouteorgradepromotion')
        req(not device['total_native_control_flow_claimed'], 'qualifiedwarningflow')
        for s in device['scalar_or_value_fragment_candidates']:
            req(not s['callable_standalone_exported_leaf'] and not s['grade_or_expected_value'], 'fragmentnotcallableoracle')
            lines = by[s['entry']]['code'].splitlines(keepends=True)
            req(sha(''.join(lines[s['C_start']-1:s['C_end']]).encode()) == s['C_span_sha256'], 'fragmentspan')
    for front in b['frontiers']['rows']:
        req(not front['followed'] and front['native_PC'] is None and
            front['selected_in_batch'] == (front['target'] in seeds), 'noencounterfollowingorsitecredit')
    return errors


def main():
    loc = load('source-locators.json')
    by = {}
    for m in loc['records']:
        with (R / m['retained_path']).open('rb') as f:
            f.seek(m['retained_byte'])
            raw = f.read(m['raw_bytes'])
        assert sha(raw) == m['raw_sha256']
        by[m['entry']] = json.loads(raw)
    b = {'locators': loc, 'records': by, 'census': load('candidate-census.json'),
         'approval': load('selection-approval.json'), 'projections': load('projection-qualifications.json'),
         'claims': load('source-claims.json'), 'whole': load('whole-set-assessment.json'),
         'frontiers': load('new-call-frontiers.json'),
         'new_raw_rows': (P / 'new-source-records.jsonl').read_bytes().splitlines(keepends=True)}
    seeds = fixed_seeds()
    errors = validate(b, seeds)
    if sha((P / 'candidate-census.json').read_bytes()) != b['approval']['census_sha256']:
        errors.append('approvedcensusidentity')
    pins = load('census-pins.json')['pins']
    for pin in pins + b['census']['approved_C1_chunk_pins']:
        q = pathlib.Path(pin['path'])
        if not q.is_absolute():
            q = R / q
        data = q.read_bytes()
        if len(data) != pin['bytes'] or sha(data) != pin['sha256']:
            errors.append('pin:' + str(q))
    approved = json.loads((F / 'component-resolution-v1/class-inputs.json').read_text())['decomp_chunk_pins']
    for pin in b['census']['approved_C1_chunk_pins']:
        if pin not in approved:
            errors.append('chunknotapproved1a')
    for m in loc['records']:
        data = pathlib.Path(m['source_path']).read_bytes()
        raw = data[m['source_byte']:m['source_byte']+m['raw_bytes']]
        if sha(raw) != m['raw_sha256'] or data[:m['source_byte']].count(b'\n')+1 != m['source_line']:
            errors.append('originalrawlocator')
    oldcalls = [json.loads(l) for l in (M / 'selected-calls.jsonl').read_text().splitlines()]
    for r in load('existing-event-call-frontiers.json')['rows']:
        original = dict(r)
        i = original.pop('retained_line')
        if oldcalls[i-1] != original:
            errors.append('inheritedcallfrontier')
    prefix = load('research-prefix.json')
    research = R / prefix['path']
    current = research.read_bytes()
    if sha(current[:prefix['bytes']]) != prefix['sha256'] or len(current) <= prefix['bytes']:
        errors.append('fullcanonicalprefix')
    if b'Pending independent source review' not in current[prefix['bytes']:]:
        errors.append('pendingreviewappend')
    links = 0
    for page in [P / 'structure.md', P / 'census-rationale.md', research]:
        for target in re.findall(r'\]\(([^)]+)\)', page.read_text()):
            if target.startswith(('http:', 'https:', '#')):
                continue
            target = target.split('#')[0]
            if target and not (page.parent / target).resolve().exists():
                errors.append('local link:' + target)
            links += 1
    frontmatter = current.decode().split('---', 2)[1]
    for key in ('id:', 'type: research', 'status:', 'updated:', 'access: analysis', 'revision:', 'target:'):
        if key not in frontmatter:
            errors.append('researchfrontmatter')
    for q in P.iterdir():
        if q.suffix in ('.md', '.py') and any(l.rstrip() != l for l in q.read_text().splitlines()):
            errors.append('trailingwhitespace:' + q.name)
    negatives = []

    def reject(name, change, guard):
        changed = copy.deepcopy(b)
        change(changed)
        passed = guard in validate(changed, seeds)
        negatives.append({'name': name, 'rejected': passed, 'matched_guard': guard})
        if not passed:
            errors.append('negative:' + name)

    reject('omit fixed record', lambda x: x['records'].pop('0x101c286c4'), 'exact17fixedseeds')
    reject('claim17newbodies', lambda x: x['locators'].__setitem__('new_record_count', 17), 'newversusinheritedcount')
    reject('copy inherited record into newfile', lambda x: x['new_raw_rows'].append(
        (json.dumps(x['records']['0x101c20adc'])+'\n').encode()), 'only3newrawrows')
    reject('altercensusreceipt', lambda x: x['census']['summary'].__setitem__('total_C_utf8_bytes', 196609), 'pinnedmetadatareceipt')
    reject('expandCcap', lambda x: x['records']['0x101c286c4'].__setitem__('code', ' '*196609), 'Cbytecap')
    reject('dropnativeextent', lambda x: x['locators']['records'][0].__setitem__('native_body_bytes', 160), 'nativeextentidentity')
    reject('expandedfourbyteimplementation', lambda x: x['projections']['expanded'][0].__setitem__('operations_attributed_to_native_entry', True), 'expandednotnativeimplementation')
    reject('delegatedtargetfreshlyread', lambda x: x['projections']['expanded'][0].__setitem__('target_record_selected_or_read', True), 'delegatedtargetunread')
    reject('corruptclaimspan', lambda x: x['claims']['claims'][0].__setitem__('C_span_sha256', '0'*64), 'claimspanidentity')
    reject('warningpromotedtototalflow', lambda x: x['claims']['claims'][0].__setitem__('total_native_control_flow_or_failure_law', True), 'nototalnativefloworfailurelaw')
    reject('omitwarningqualification', lambda x: x['projections']['warnings'].pop(), 'allwarningqualifications')
    reject('dropeffect', lambda x: x['whole']['devices'].pop(), 'whole8devices')
    reject('fragmentpromotedtocallable', lambda x: x['whole']['devices'][1]['scalar_or_value_fragment_candidates'][0].__setitem__('callable_standalone_exported_leaf', True), 'fragmentnotcallableoracle')
    reject('publicgradepromotion', lambda x: x['whole']['devices'][0].__setitem__('new_public_outcome_or_grade', True), 'nopublicrouteorgradepromotion')
    reject('rederive309denominator', lambda x: x['whole']['predecessor_inventory_unchanged'].__setitem__('new_denominator_derived', True), 'predecessorasofinventory')
    reject('autofollownewcallee', lambda x: x['frontiers']['rows'][0].__setitem__('followed', True), 'noencounterfollowingorsitecredit')
    result = {'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
              'scope': 'Fixed selected-source/data integrity and focused docs only, not semantic approval or runtime compatibility.',
              'selected_records': 17, 'new_records': 3, 'inherited_records_not_copied': 14,
              'C_utf8_bytes': 50962, 'new_C_utf8_bytes': 6203, 'new_claims_auxiliary_only': 9,
              'whole_devices': 8, 'pinned_inputs': len(pins), 'approved_chunks': 6,
              'focused_links': links, 'negative_controls': negatives,
              'new_native_sites': 0, 'original_native_provider_decoder_calls': 0}
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
