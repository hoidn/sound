"""Read-only stdlib integrity and negative checks for this bounded family map.

No old script imports, bodies, decoder, provider or original/candidate execution.
"""
import collections
import copy
import csv
import hashlib
import io
import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent
R = P.parents[3]
F = P.parent


def H(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return H(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode())


def load(name):
    return json.loads((P / name).read_text())


def pointer(obj, path):
    for token in path.strip('/').split('/') if path else []:
        token = token.replace('~1', '/').replace('~0', '~')
        obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    return obj


def validate(b, owner):
    errors = []

    def req(ok, msg):
        if not ok:
            errors.append(msg)

    ledger = b['ledger']
    rows = ledger['rows']
    req([x['id'] for x in rows] == [f'RCMAP-{i:03}' for i in range(1, 283)], '282boundedoutcomerows')
    req({x['requirement'] for x in rows} == {f'REQ-RECORDING-COMPING-{i:03}' for i in range(1, 35)},
        'all34requirements')
    req(ledger['owner_revision'] == 4 and ledger['owner_sha256'] == H(owner.encode()), 'currentR4owneridentity')
    for suffix, span in ledger['requirement_spans'].items():
        req(H(owner[span['start']:span['end']].encode()) == span['sha256'], 'ownerclausespan')
    for x in rows:
        s = x['source_span']
        clause = ledger['requirement_spans'][x['owner_clause_span']]
        req(clause['start'] <= s['start'] < s['end'] <= clause['end'], 'outcomeinsideclause')
        req(H(owner[s['start']:s['end']].encode()) == s['sha256'], 'outcomesourcespan')
        req(x['actual_target_status'] == 'U' and not x['original_execution'] and not x['route_is_grade'],
            'allactualUandroutesnotgrades')
        package = x['source_class'] == 'D-package'
        req(x['route_class'] == ('S-route' if package else 'no-established-route'), 'packagerouteonly')
        req(package == x['requirement'].endswith('027'), 'packageowner027only')
        if package:
            req(all(k.startswith('PKG-') for k in x['route_evidence']), 'packageevidenceonly')
        else:
            req(x['missing_join'] in ledger['join_catalog'] and bool(x['missing_join_reason']),
                'concretepublicmissingjoin')
        req(bool(x['case_links']), 'existingcasenavigation')
        for ref in x['source_contexts'] + x['route_evidence']:
            req(ref in b['sources']['records'], 'evidenceresolves')
    req(collections.Counter(x['route_class'] for x in rows) == {'S-route': 8, 'no-established-route': 274},
        'boundedroutecounts')
    req(collections.Counter(x['source_class'] for x in rows) == {'D12-manual': 143, 'U': 131, 'D-package': 8},
        'sourceclasscounts')
    req(all(ledger['counts'][k] == 0 for k in ('new_grades', 'new_original_calls', 'new_indirect_sites')),
        'nonewgradeexecutionsitecredit')
    nav = b['cases']['records']
    req([x['id'] for x in nav] == [f'RC-{i:03}' for i in range(1, 91)], 'all90casepointers')
    req(sum(x['role'] == 'artifact-inventory-only' for x in nav) == 4 and
        all((x['role'] == 'artifact-inventory-only') == (x['id'] in {'RC-061','RC-062','RC-063','RC-064'})
            for x in nav), 'fourartifact86applicationseparate')
    req(all(x['actual_expected'] is None and x['actual_comparison'] is None and
            x['actual_grade'] == 'U' and not x['executed'] for x in nav), '90nullactualU')
    req(sum(x['history'] == 'preserved-old81' for x in nav) == 81 and
        sum(x['history'] == 'new-R4-null-history' for x in nav) == 9, '81old9newhistory')
    req(b['batch']['ready_X_execution_batches'] == [], 'noreadyoriginalexecutionbatch')
    g = b['guards']
    truekeys = ['scene_Off_requires_actual_Off', 'scene_Off_requires_productive_enabled_RC021_first',
                'EACH_NONEMPTY_source_required', 'BOTH_independent_takes_and_maincomp_required',
                'audio_EACH_NONZERO_nonmuted_productive_output_required',
                'matched_highlight_positive_before_mismatch',
                'automatic_and_actual_manual_fade_histories_separate', 'clock_control_host_media_U_preserved']
    falsekeys = ['scene_default_inferred_from_Off', 'UI_only_requires_audio_hardware',
                 'TakeId_or_shared_sample_is_complete_match', 'clip_independence_means_physical_copy',
                 'Capture_heuristic_chosen', 'fourms_is_audio_tolerance',
                 'Q031_color_default_or_random_noncoincidence_chosen', 'posttarget_API_target_parity_claimed',
                 'all_group_complete_or_coverage_credit']
    req(all(g[k] is True for k in truekeys) and all(g[k] is False for k in falsekeys), 'preservedproductiveandQguards')
    req(g['multi_sample_destinations'].startswith('sequential TRACKS only'), 'sequentialTRACKSnotlanes')
    req(g['adoption_groups_unadopted'] == ['G12', 'G13'] and len(g['source_question_ids']) == 6,
        'unadoptedgroupsandsourcequestions')
    req(not b['receipt']['fresh_full_Recording_manual_audit'] and
        b['receipt']['inherited_Comping_audit_blocks'] == 38, 'CompingonlyauditnotfullRecording')
    meta = b['metadata']
    counts = collections.Counter(x['kind'] for x in meta)
    req(counts == {'lexical-owner-data':39,'membership-data':68,'alias-data':68,'RTTI-data':32,
                   'table-data':32,'store-data':75,'call-data':103,'indirect-data':30}, '447fixedmetadatarows')
    tables = [x['record'] for x in meta if x['kind'] == 'table-data']
    aliases = [x['record'] for x in meta if x['kind'] == 'alias-data']
    memberships = [x['record'] for x in meta if x['kind'] == 'membership-data']
    req({x['entry'] for x in aliases} == {x['entry'] for x in memberships} ==
        set(b['census']['alias_entries']), '68aliasmembershipidentity')
    req(len(tables) <= 32 and sum(len(t['slots']) for t in tables) <= 512 and counts['store-data'] <= 128 and
        counts['alias-data'] + counts['membership-data'] <= 512 and
        counts['call-data'] + counts['indirect-data'] <= 512, 'allselectedmetadatacaps')
    for table in tables:
        n = table['exported_prefix_slot_count']
        req(len(table['slots']) == (3 if n > 16 else n), 'largedefinedleading3prefix')
        req(table['native_table_extent'] is None and table['not_complete_render_callback_or_native_extent'],
            'nomethodrenderextentcompleteness')
        typ = table['literal_type_encoding']
        req(typ in {str(len(n))+n for n in b['census']['exact_types']} and table['offset_to_top'] == 0,
            'exact32primarytypes')
    req(sum(len(t['slots']) for t in tables) == 130 and
        sum(t['exported_prefix_slot_count'] for t in tables) == 1577, '130selected1577metadata')
    req(len(b['census']['explicit_scope_exclusions']) == 8 and b['census']['within_caps'] and
        not b['census']['materialized_at_census'], 'declaredexclusionsandpregatehistory')
    req(b['sources']['new_C_selected'] == 0 and not b['chain']['runtime_recording_route'] and
        b['chain']['new_traversals'] == b['chain']['new_indirect_sites'] == 0, 'nonewbodyruntimeortraversal')
    return errors


def main():
    owner = (R / 'wiki/specs/recording-comping.md').read_text()
    b = {'ledger':load('route-ledger.json'),'sources':load('sources.json'),'cases':load('case-navigation.json'),
         'guards':load('prerequisites.json'),'batch':load('batch-inputs.json'),'chain':load('chain-edges.json'),
         'census':load('metadata-census.json'),'receipt':load('read-receipt.json'),
         'metadata':[json.loads(l) for l in (P/'native-data.jsonl').read_text().splitlines()]}
    errors = validate(b, owner)
    pins = load('source-pins.json')['pins']
    for pin in pins:
        data = (R/pin['path']).read_bytes()
        if len(data) != pin['bytes'] or H(data) != pin['sha256']:
            errors.append('pin:'+pin['path'])
    cache = {}

    def fileobj(path):
        if path not in cache:
            cache[path] = json.loads((R/path).read_text())
        return cache[path]

    # Verify exact selected original rows by source line/byte/raw hash.
    # Outside selected lines bytes are counted only, not semantically parsed.
    grouped = collections.defaultdict(dict)
    for row in b['metadata']:
        grouped[row['provider']][row['source_line']] = row
    raw_verified = 0
    for provider, targets in grouped.items():
        off = 0
        with pathlib.Path(provider).open('rb') as f:
            for number, raw in enumerate(f,1):
                if number in targets:
                    row = targets[number]
                    if off != row['source_byte'] or len(raw) != row['raw_bytes'] or H(raw) != row['raw_sha256']:
                        errors.append('originalmetadatalocator')
                    orig = json.loads(raw)
                    if row['kind'] == 'table-data':
                        orig['exported_prefix_slot_count'] = len(orig['slots'])
                        orig['selected_slot_policy'] = ('large-table-header/store + leading3 construction/lifetime prefix only'
                                                       if len(orig['slots'])>16 else 'complete retained small exported prefix')
                        orig['slots'] = orig['slots'][:3] if len(orig['slots'])>16 else orig['slots']
                        orig['not_complete_render_callback_or_native_extent'] = True
                    if orig != row['record']:
                        errors.append('exactmetadataprojection')
                    raw_verified += 1
                off += len(raw)
                if number >= max(targets):
                    break
    if raw_verified != 447:
        errors.append('all447rawsourcechecks')
    actual = json.loads((F/'recording/cases-r4.json').read_text())['records']
    old = json.loads((F/'recording/cases-r3.json').read_text())['records']
    if actual[:81] != old:
        errors.append('old81preservation')
    for i, ref in enumerate(b['cases']['records']):
        c = actual[i]
        if c['id'] != ref['id'] or canonical(c) != ref['record_sha256'] or H(c['action'].encode()) != ref['action_sha256']:
            errors.append('exactcasepointerhash')
        if c['expected'] is not None or c['comparison'] is not None or c['target_grade'] != 'U' or c['executed']:
            errors.append('canonicalactualnullU')
    if not all(k in actual[19]['action'] for k in ('First explicitly enable','RC-021','separate matched history','Off')):
        errors.append('RC020explicitproductivehistory')
    requirements = json.loads((F/'recording/requirements-r4.json').read_text())
    for suffix,s in b['ledger']['requirement_spans'].items():
        if owner[s['start']:s['end']] != requirements[int(suffix)-1]['contract']:
            errors.append('currentownercontractlookup')
    for sid,src in b['sources']['records'].items():
        kind = src['kind']
        if kind == 'retained-current-manual-section':
            html = (R/src['path']).read_text()
            if H(html[src['raw_start']:src['raw_end']].encode()) != src['raw_sha256'] or src['target_parity'] != 'U':
                errors.append('manualsectionorparity')
        elif kind == 'approved-Comping-audit-block':
            block = pointer(fileobj(src['path']),src['pointer'])
            html = (R/src['html_path']).read_text()
            if H(block['raw_html'].encode()) != src['raw_sha256'] or H(block['text'].encode()) != src['text_sha256'] or html[src['raw_start']:src['raw_end']] != block['raw_html']:
                errors.append('Compingexactblock')
        elif kind == 'retained-artifact-inventory':
            for ptr in src['pointers']:
                pointer(fileobj(src['path']),ptr)
        elif kind == 'existing-retained-registry-name-landmarks':
            d = fileobj(src['path'])['record']
            if H(d['code'].encode()) != src['C_code_sha256']:
                errors.append('registrycodeidentity')
            for name in src['landmarks']:
                line = d['code'].splitlines(keepends=True)[name['C_line']-1]
                if H(line.encode()) != name['C_line_sha256'] or '"'+name['name']+'"' not in line or name['native_PC'] is not None:
                    errors.append('registrylandmark')
        elif kind == 'existing-native-string-navigation':
            original = pointer(fileobj(src['path']),src['pointer'])
            if original['line_sha256'] != src['original_raw_sha256'] or original['record']['refs'] != src['references']:
                errors.append('nativestringreference')
    for e in b['chain']['inherited_edges']:
        if canonical(pointer(fileobj(e['path']),e['pointer'])) != e['record_sha256']:
            errors.append('inheritededgeidentity')
    tsv = list(csv.DictReader(io.StringIO((P/'outcomes.tsv').read_text()),delimiter='\t'))
    if len(tsv) != 282:
        errors.append('TSV282rows')
    for r,t in zip(b['ledger']['rows'],tsv):
        if any(str(r[k] if r[k] is not None else '') != t[k] for k in t):
            errors.append('TSVJSONidentity')
    prefix = load('research-prefix.json')
    research = R/prefix['path']
    current = research.read_bytes()
    if H(current[:prefix['bytes']]) != prefix['sha256'] or len(current) <= prefix['bytes']:
        errors.append('fullresearchprefix')
    if b'Pending independent structure review' not in current[prefix['bytes']:]:
        errors.append('pendingreviewappend')
    links = 0
    for page in (P/'structure.md',research):
        for target in re.findall(r'\]\(([^)]+)\)',page.read_text()):
            if target.startswith(('https:','http:','#')):
                continue
            target = target.split('#')[0]
            if target and not (page.parent/target).resolve().exists():
                errors.append('local link:'+target)
            links += 1
    for key in ('id:','type: research','status:','updated:','access: analysis','revision:','target:'):
        if key not in current.decode().split('---',2)[1]:
            errors.append('researchfrontmatter')
    for q in P.iterdir():
        if q.suffix in ('.py','.md') and any(l.rstrip()!=l for l in q.read_text().splitlines()):
            errors.append('ownedtextwhitespace')
    negatives=[]

    def reject(name,change,guard):
        altered=copy.deepcopy(b)
        change(altered)
        rejected=guard in validate(altered,owner)
        negatives.append({'name':name,'rejected':rejected,'matched_guard':guard})
        if not rejected:
            errors.append('negative:'+name)

    reject('omit required predicate',lambda x:x['ledger']['rows'].pop(),'282boundedoutcomerows')
    reject('promote public names to S route',lambda x:x['ledger']['rows'][0].__setitem__('route_class','S-route'),'packagerouteonly')
    reject('invent actual pass',lambda x:x['cases']['records'][0].__setitem__('actual_expected',True),'90nullactualU')
    reject('omit current case',lambda x:x['cases']['records'].pop(),'all90casepointers')
    reject('drop concrete missing join',lambda x:x['ledger']['rows'][0].__setitem__('missing_join',None),'concretepublicmissingjoin')
    reject('corrupt source span',lambda x:x['ledger']['rows'][0]['source_span'].__setitem__('sha256','0'*64),'outcomesourcespan')
    reject('omit selected metadata table',lambda x:x['metadata'].pop(next(i for i,r in enumerate(x['metadata'])if r['kind']=='table-data')),'447fixedmetadatarows')
    reject('expand large table arbitrary fourth slot',lambda x:next(r['record']for r in x['metadata']if r['kind']=='table-data'and r['record']['exported_prefix_slot_count']>16)['slots'].append({'offset':24,'target':'unknown'}),'largedefinedleading3prefix')
    reject('scene Off without enabled positive',lambda x:x['guards'].__setitem__('scene_Off_requires_productive_enabled_RC021_first',False),'preservedproductiveandQguards')
    reject('TakeId proves matching',lambda x:x['guards'].__setitem__('TakeId_or_shared_sample_is_complete_match',True),'preservedproductiveandQguards')
    reject('Capture detector guessed',lambda x:x['guards'].__setitem__('Capture_heuristic_chosen',True),'preservedproductiveandQguards')
    reject('manual fade inferred from automatic',lambda x:x['guards'].__setitem__('automatic_and_actual_manual_fade_histories_separate',False),'preservedproductiveandQguards')
    reject('multi-sample targets take lanes',lambda x:x['guards'].__setitem__('multi_sample_destinations','sequential take lanes'),'sequentialTRACKSnotlanes')
    reject('Q031 default chosen',lambda x:x['guards'].__setitem__('Q031_color_default_or_random_noncoincidence_chosen',True),'preservedproductiveandQguards')
    reject('Comping audit becomes allRecording',lambda x:x['receipt'].__setitem__('fresh_full_Recording_manual_audit',True),'CompingonlyauditnotfullRecording')
    reject('new indirect site credit',lambda x:x['ledger']['counts'].__setitem__('new_indirect_sites',1),'nonewgradeexecutionsitecredit')
    out={'status':'PASS'if not errors else'FAIL','errors':errors,
         'scope':'Selected-data/source/owner integrity and focused docs only; no semantic approval or behavior execution.',
         'rows':282,'routes':{'S_inventory_only':8,'no_established_route':274,'X':0},
         'requirements':34,'case_pointers':90,'artifact_only_cases':4,'application_U_cases':86,
         'all90actualnullU':True,'selected_raw_rows_verified':raw_verified,'pinned_inputs':len(pins),
         'focused_links':links,'negative_controls':negatives,'new_original_calls':0,'new_indirect_sites':0}
    print(json.dumps(out,indent=2))
    raise SystemExit(bool(errors))


if __name__=='__main__':
    main()
