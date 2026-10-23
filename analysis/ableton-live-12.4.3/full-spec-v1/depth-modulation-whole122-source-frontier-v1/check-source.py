"""Read-only packet data checks. No original source, indices, binaries, tools, models, or collectors."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys

P = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def j(name):
    return json.loads((P / name).read_bytes())


def span_hash(record, lo, hi):
    lines = record['code'].splitlines(keepends=True)
    assert 1 <= lo <= hi <= len(lines)
    return sha(''.join(lines[lo - 1:hi]).encode())


def lexical(records):
    pats = [
        ('unfollowed-FUN-token', re.compile(r'\b(?:thunk_)?FUN_[0-9a-fA-F]+\b')),
        ('unread-global-token', re.compile(r'\b(?:_?DAT_[0-9a-fA-F]+|PTR_[A-Za-z0-9_]+)\b')),
        ('library-or-builtin-token', re.compile(r'\b(?:_?exp2f|(?:___)?exp10f|_expf|_exp|_fmod|___sincos_stret|___stack_chk_fail|LOAcquire|LORelease|NEON_[A-Za-z0-9_]+)\b')),
    ]
    out = []
    for ordinal, record in enumerate(records, 1):
        for line_no, line in enumerate(record['code'].splitlines(keepends=True), 1):
            for kind, pat in pats:
                for m in pat.finditer(line):
                    out.append((ordinal, record['entry'], line_no, m.start(), kind, m.group(), sha(line.encode())))
            if '(**' in line or '(*(code *)' in line:
                out.append((ordinal, record['entry'], line_no, None, 'unresolved-indirect-expression-line', None, sha(line.encode())))
    return out


def validate(records, raw_lines, census, receipt, gate, assessment, readmap, readreceipt, deps, whole):
    assert len(records) == len(raw_lines) == len(assessment['records']) == len(census['records']) == 122
    entries = [r['entry'] for r in records]
    assert len(set(entries)) == 122 and entries == gate['entries'] == [r['entry'] for r in census['records']]
    assert gate['caps'] == dict(records=122, C_bytes=2097152, C_lines=50000)
    assert census['excluded_UI_group']['count'] == len(census['excluded_UI_group']['entries']) == 11
    assert not set(entries).intersection(census['excluded_UI_group']['entries'])
    assert receipt['raw_range_reads'] == 122 and receipt['source_expansion'] is False and receipt['original_calls'] == 0
    assert receipt['source_selection_sha256'] == '47a667a169e41814599378859b2574adc224763e68b02602b9b7be0637bfd3f9'
    assert receipt['raw_content_bytes'] == 437740 and receipt['retained_sha256'] == sha(b''.join(raw_lines))
    assert len(receipt['records']) == 122
    offset = 0
    warning_occurrences = []
    for i, (r, raw, c, old, a) in enumerate(zip(records, raw_lines, census['records'], receipt['records'], assessment['records']), 1):
        assert sha(raw) == c['raw_sha256'] == old['raw_sha256'] == a['retained_source']['sha256']
        assert len(raw) == c['raw_bytes'] == old['raw_bytes'] == a['retained_source']['bytes']
        assert old['entry'] == r['entry'] == a['entry'] == c['entry']
        assert old['retained_byte'] == a['retained_source']['byte'] == offset
        assert old['original_path'] == c['source_path'] and old['original_byte'] == c['source_byte'] and old['original_line'] == c['source_line']
        assert a['retained_source']['row'] == i and a['retained_source']['path'] == 'selected-records.jsonl'
        offset += len(raw)
        code = r['code'].encode()
        lines = r['code'].splitlines(keepends=True)
        assert len(code) == c['code_utf8_bytes'] == a['C_utf8_bytes'] == r['code_bytes']
        assert sha(code) == c['code_sha256'] == a['C_sha256'] == r['code_sha256']
        assert len(lines) == c['C_lines'] == a['C_lines']
        assert r['name'] == c['export_record_name'] == a['name']
        assert r['body_bytes'] == c['body_bytes'] == a['native_extent_metadata']['body_bytes']
        assert r['body_ranges'] == c['body_ranges'] == a['native_extent_metadata']['body_ranges_inclusive']
        assert not r['thunk'] and not a['native_extent_metadata']['thunk']
        assert a['native_extent_metadata']['instruction_content_read'] is a['native_extent_metadata']['complete_native_implementation_established'] is False
        assert r['warnings'] == c['warnings'] == a['warnings_exact']
        assert r['error'] is c['error'] is a['error'] is None
        assert r['partial_code'] is r['timed_out'] is a['partial_code'] is a['timed_out'] is False
        assert r['state'] == c['state'] == ('exported-with-warnings' if r['warnings'] else 'exported')
        assert a['ordinal'] == i and len(a['observed_source_projection']) >= 80
        assert a['callable_math_X_established'] is a['execution_ready'] is a['public_binding_established'] is False
        assert a['read_method'] == ('lossless-full-base-and-every-change/shared-line' if 89 <= i <= 100 else 'complete-numbered-C-display')
        assert a['full_projection_anchor'] == dict(C_lines_inclusive=[1, len(lines)], span_sha256=sha(code))
        parts = a['semantic_parts']
        assert parts and parts[0]['C_lines_inclusive'][0] == 1 and parts[-1]['C_lines_inclusive'][1] == len(lines)
        assert all(x['C_lines_inclusive'][1] + 1 == y['C_lines_inclusive'][0] for x, y in zip(parts, parts[1:]))
        for part in parts:
            lo, hi = part['C_lines_inclusive']
            assert part['span_sha256'] == span_hash(r, lo, hi)
        for line_no, line in enumerate(lines, 1):
            for m in re.finditer(r'/\* WARNING:.*?\*/', line):
                warning_occurrences.append(dict(ordinal=i, entry=r['entry'], C_line=line_no, warning=m.group(), line_sha256=sha(line.encode())))
        assert collections.Counter(w['warning'] for w in warning_occurrences if w['ordinal'] == i) == collections.Counter(r['warnings'])
    assert assessment['warnings'] == warning_occurrences and len(warning_occurrences) == 31
    assert assessment['summary'] == dict(records=122, C_utf8_bytes=360530, C_lines=9041, warning_records=20, warning_occurrences=31,
        four_byte_extents=47, four_byte_with_more_than_11_C_lines=44, thunk_flags_true=0, established_callable_math_X=0, execution_ready_batches=0, established_public_routes=0)
    assert sum(len(r['code'].encode()) for r in records) == 360530 and sum(len(r['code'].splitlines()) for r in records) == 9041
    assert sum(r['body_bytes'] == 4 for r in records) == 47
    assert sum(r['body_bytes'] == 4 and len(r['code'].splitlines()) > 11 for r in records) == 44
    assert sum(bool(r['warnings']) for r in records) == 20
    assert max(len(r['code'].splitlines()) for r in records) == 609
    assert readmap['fully_reconstructs_each_original_C'] is True and readmap['semantic_read_status'].startswith('COMPLETE:')
    assert [x['ordinal'] for x in readmap['records']] == list(range(89,101))
    assert readmap['explicit_new_or_base_lines'] == 692 and readmap['exact_shared_target_lines'] == 2844
    explicit = shared = 0
    already = set(range(1,89))
    for item in readmap['records']:
        o = item['ordinal']
        r = records[o - 1]
        target = r['code'].splitlines(keepends=True)
        assert item['entry'] == r['entry'] and item['C_lines'] == len(target) and item['code_sha256'] == sha(r['code'].encode())
        if item['mode'] == 'full-base':
            assert o == 89 and item['blocks'] == []
            explicit += len(target)
        else:
            b = item['base_ordinal']
            assert b in already and item['base_entry'] == records[b - 1]['entry']
            base = records[b - 1]['code'].splitlines(keepends=True)
            ti = bi = 0
            reconstructed = []
            assert item['blocks']
            for block in item['blocks']:
                a0, a1 = block['base_zero_based_halfopen']
                b0, b1 = block['target_zero_based_halfopen']
                assert a0 == bi and b0 == ti and a0 <= a1 <= len(base) and b0 <= b1 <= len(target)
                aa, bb = base[a0:a1], target[b0:b1]
                assert block['base_span_sha256'] == sha(''.join(aa).encode())
                assert block['target_span_sha256'] == sha(''.join(bb).encode())
                kind = block['kind']
                assert kind in ['equal', 'replace', 'delete', 'insert']
                if kind == 'equal':
                    assert aa == bb and a1-a0 == b1-b0 and a1>a0
                    reconstructed += aa
                    shared += len(bb)
                else:
                    assert aa != bb
                    if kind == 'delete': assert not bb and aa
                    if kind == 'insert': assert not aa and bb
                    reconstructed += bb
                    explicit += len(bb)
                bi, ti = a1, b1
            assert ti == len(target) and bi == len(base) and reconstructed == target
        already.add(o)
    assert (explicit, shared) == (692,2844)
    assert readreceipt['direct_full_numbered_display_ordinals'] == list(range(1,89)) + list(range(101,123))
    assert readreceipt['lossless_complete_ordinals'] == list(range(89,101))
    assert readreceipt['read_after_truncation']['ordinals'] == [92,93]
    assert readreceipt['complete_projection_records'] == 122 and readreceipt['C_utf8_bytes'] == 360530 and readreceipt['C_lines'] == 9041
    assert readreceipt['all_warning_occurrences_read'] == 31 and readreceipt['warning_records'] == 20
    for key in ['original_calls','new_native_instruction_reads','new_callee_global_slot_provider_follow','new_model_harness_execution','new_site_grade_case_release']:
        assert readreceipt[key] == 0
    assert readreceipt['required_unsupported'] == 'U' and readreceipt['coverage_gate'] == 'OPEN' and readreceipt['successor_selected'] is False
    expected = lexical(records)
    actual = [(x['ordinal'],x['entry'],x['C_line'],x['column_zero_based'],x['kind'],x['token'],x['line_sha256']) for x in deps['occurrences']]
    assert actual == expected and len(actual) == 740
    assert deps['selection_entries'] == entries
    assert deps['kind_counts'] == dict(collections.Counter(x[4] for x in expected)) == {'unfollowed-FUN-token':374,'unread-global-token':169,'library-or-builtin-token':130,'unresolved-indirect-expression-line':67}
    assert not any(x[0] in [55,57,69] for x in expected)
    assert deps['new_bodies_followed'] == deps['native_site_credit'] == 0
    assert whole['whole_set'] == dict(entries=122,C_utf8_bytes=360530,C_lines=9041,original_calls=0,new_source_follow=0,native_reads=0,callable_math_X=0,execution_ready_batches=0,public_routes=0,new_native_sites=0,grade_changes=0)
    assert whole['current_family'] == dict(whole_clause_bundles=106,required_route='no-established-exact-target-route',actual_case_records=208,actual_grades_all='U',D12_annotations_same106=96,unknown_annotations_same106=10,auxiliary_file_S_outside_required=10,changed=False)
    assert [x['id'] for x in whole['claims']] == [f'M122-C{i:02}' for i in range(1,10)]
    assert set(o for cl in whole['claims'] for o in cl['ordinals']) == set(range(1,123))
    for claim in whole['claims']:
        assert claim['observed'] and claim['not_established'] and claim['anchors']
        for a in claim['anchors']:
            assert a['ordinal'] in claim['ordinals']
            span_hash(records[a['ordinal']-1], *a['C_lines_inclusive'])
    assert [x['id'] for x in whole['open_frontiers']] == [f'M122-F{i:02}' for i in range(1,9)]
    assert all(x['status'] == 'UNKNOWN' and x['missing'] for x in whole['open_frontiers'])
    assert len(whole['prospects']) == 6
    for prospect in whole['prospects']:
        assert prospect['callable_X'] is prospect['ready'] is prospect['public_behavior_proof'] is False
        assert prospect['gates'] and prospect['evidence']
        for a in prospect['evidence']: span_hash(records[a['ordinal']-1],*a['C_lines_inclusive'])
    assert whole['required_unsupported'] == 'U' and whole['coverage_gate'] == 'OPEN' and whole['successor_selected'] is False


def main():
    assert sys.argv[1:] == ['--check']
    raw_lines = (P/'selected-records.jsonl').read_bytes().splitlines(keepends=True)
    data = [list(map(json.loads,raw_lines)), raw_lines, j('candidate-census.json'), j('source-retention-receipt.json'), j('selection-source-read.json'), j('source-assessment.json'), j('lossless-vocoder-read-map.json'), j('source-read-receipt.json'), j('source-dependencies.json'), j('whole-set-assessment.json')]
    stage = j('metadata-stage.json')
    # Preservation only: never invoke census.py/retain-sources.py/check-metadata.py or read original files.
    for pin in stage['files']:
        b = (P/pin['path']).read_bytes()
        assert (len(b),sha(b)) == (pin['bytes'],pin['sha256'])
    for pin in j('pins-source.json')['pins']:
        if pin['scope'] == 'owned exact bytes':
            b = (P/pin['path']).read_bytes()
            assert (len(b),sha(b)) == (pin['bytes'],pin['sha256'])
    assert (len((P/'selection-source-read.json').read_bytes()),sha((P/'selection-source-read.json').read_bytes())) == (4802,'47a667a169e41814599378859b2574adc224763e68b02602b9b7be0637bfd3f9')
    validate(*data)
    negatives=[]
    def reject(name, edit):
        bad=copy.deepcopy(data);edit(bad)
        try: validate(*bad)
        except (AssertionError,ValueError,KeyError,IndexError,TypeError):
            negatives.append(dict(name=name,rejected=True));return
        raise AssertionError('negative accepted: '+name)
    reject('drop-one-selected-source',lambda q:q[0].pop())
    reject('duplicate-entry',lambda q:q[0][1].update(entry=q[0][0]['entry']))
    reject('alter-retained-raw-custody',lambda q:q[1].__setitem__(0,q[1][0]+b' '))
    reject('change-C-with-old-hash',lambda q:q[0][0].update(code=q[0][0]['code']+'\n'))
    reject('erase-source-warning',lambda q:q[0][6].update(warnings=[]))
    reject('repair-native-four-byte-extent',lambda q:q[0][6].update(body_bytes=4096))
    reject('repair-false-thunk',lambda q:q[0][6].update(thunk=True))
    reject('accept-partial-C',lambda q:q[0][0].update(partial_code=True))
    reject('invent-second-source-range-pass',lambda q:q[3].update(raw_range_reads=244))
    reject('lose-owned-byte-offset',lambda q:q[5]['records'][1]['retained_source'].update(byte=0))
    reject('misattribute-source-name',lambda q:q[5]['records'][0].update(name='other'))
    reject('wrong-anchor-hash',lambda q:q[5]['records'][0]['semantic_parts'][0].update(span_sha256='0'*64))
    reject('omit-semantic-coverage-part',lambda q:q[5]['records'][56]['semantic_parts'].pop())
    reject('promote-callable-source-projection',lambda q:q[5]['records'][56].update(callable_math_X_established=True))
    reject('promote-public-curve-wrapper',lambda q:q[5]['records'][100].update(public_binding_established=True))
    reject('omit-one-Vocoder-variant',lambda q:q[6]['records'].pop())
    reject('omit-lossless-target-block',lambda q:q[6]['records'][1]['blocks'].pop())
    reject('changed-block-as-byte-identical',lambda q:next(x for x in q[6]['records'][1]['blocks'] if x['kind']=='replace').update(kind='equal'))
    reject('wrong-lossless-base-hash',lambda q:q[6]['records'][1]['blocks'][0].update(base_span_sha256='0'*64))
    reject('circular-lossless-base',lambda q:q[6]['records'][1].update(base_ordinal=90))
    reject('unfinished-semantic-read',lambda q:q[6].update(semantic_read_status='plan'))
    reject('drop-full-direct-read',lambda q:q[7]['direct_full_numbered_display_ordinals'].pop())
    reject('omit-truncation-reread',lambda q:q[7]['read_after_truncation'].update(ordinals=[92]))
    reject('native-read-not-selected',lambda q:q[7].update(new_native_instruction_reads=1))
    reject('erase-lexical-dependency',lambda q:q[8]['occurrences'].pop())
    reject('claim-native-site-from-lexical-token',lambda q:q[8].update(native_site_credit=740))
    reject('drop-whole-set-claim',lambda q:q[9]['claims'].pop())
    reject('close-receiver-frontier',lambda q:q[9]['open_frontiers'][1].update(status='CLOSED'))
    reject('admit-buffer-projection-as-ready',lambda q:q[9]['prospects'][3].update(ready=True))
    reject('pool-documentary-contexts-into-denominator',lambda q:q[9]['current_family'].update(whole_clause_bundles=202))
    reject('regrade-application-case',lambda q:q[9]['current_family'].update(actual_grades_all='S'))
    reject('documentary-coverage-fallback',lambda q:q[9].update(coverage_gate='CLOSED'))
    reject('automatically-select-successor',lambda q:q[9].update(successor_selected=True))
    print(json.dumps(dict(status='PASS',records=122,C_utf8_bytes=360530,C_lines=9041,warning_records=20,warning_occurrences=31,native_four_byte_extents=47,four_byte_more_than11_C_lines=44,lossless_Vocoder_variants=12,explicit_base_or_changed_lines=692,exact_shared_lines=2844,lexical_dependency_occurrences=740,whole_claims=9,open_frontiers=8,source_prospect_classes=6,established_callable_math_X=0,execution_ready_batches=0,established_public_routes=0,original_alias_chunk_native_image_provider_tool_model_harness_reads_or_execution_by_checker=0,metadata8_preserved=True,original_range_custody='122once inherited; checker owneddata only',parent106_208U_unchanged=True,coverage_gate='OPEN',required_unsupported='U',negative_count=len(negatives),negative_controls=negatives),indent=2))


if __name__ == '__main__':
    main()
