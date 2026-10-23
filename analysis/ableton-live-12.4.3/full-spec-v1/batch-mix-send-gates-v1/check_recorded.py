"""Packet-only checks and exact output inventory; never launch the original."""
import copy
import datetime
import hashlib
import json
from pathlib import Path
import re
import runpy
import struct
import sys

HERE = Path(__file__).resolve().parent
R = runpy.run_path(str(HERE / 'run_batch.py'), run_name='owned_data_only_import')


def load(name):
    return json.loads((HERE / name).read_text())


def rawcheck(receipt, row, plan, runtime_pins, stdout, stderr, raw):
    assert receipt['id'] == row['id'] and receipt['planned_ordinal'] == row['fresh_ordinal']
    assert receipt['argv'] == [plan['binary']['path'], plan['image']['path'], '--imports', *row['tokens']]
    assert receipt['environment'] == {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}
    assert receipt['exit_status'] == 0 and receipt['error'] is None and receipt['pid'] > 0
    assert not receipt['timed_out'] and not receipt['retry'] and receipt['cleanup'] == []
    assert receipt['stdin'] == 'DEVNULL' and receipt['timeout_seconds'] == 20 and receipt['core_limit'] == 0 and receipt['new_session']
    assert stderr == b'' and len(raw) == 16
    for key, data in [('stdout', stdout), ('stderr', stderr), ('raw_output', raw)]:
        assert receipt[key]['bytes'] == len(data) and receipt[key]['sha256'] == hashlib.sha256(data).hexdigest()
    parsed = R['protocol'](stdout, row)
    assert parsed == receipt['protocol'] and bytes.fromhex(parsed['output_hex']) == raw
    assert receipt['before'] == runtime_pins and receipt['after'] == runtime_pins
    times = [datetime.datetime.fromisoformat(receipt[k]) for k in ('started_utc', 'spawn_started_utc', 'child_finished_utc', 'finished_utc')]
    assert times == sorted(times) and 0 <= receipt['child_wall_seconds'] <= 20
    return parsed


def check():
    catalog, plan, pins = load('catalog.json'), load('execution-plan.json'), load('authority-pins.json')
    R['validate'](catalog)
    checks = {'catalog': R['selfcheck'](catalog), 'synthetic_protocol': R['protocol_selfcheck'](catalog)}
    pre = load('pre-call-manifest.json')
    for p in pre['payloads']:
        assert R['identity'](HERE / p['path']) == dict(p, path=str(HERE / p['path']))
    expected = {p['path']: p for p in pins}
    runtime = [expected[p] for p in plan['runtime_custody_paths']]
    records = [json.loads(s) for s in (HERE / 'results.jsonl').read_text().splitlines()]
    fresh = [r for r in catalog['rows'] if r['disposition'] == 'fresh-planned']
    assert len(records) == len(fresh) == 25
    assert len({r['pid'] for r in records}) == 25
    summary = load('execution-summary.json')
    assert summary['error'] is None and summary['planned_children'] == summary['attempted_children'] == summary['successful_protocols'] == 25
    assert summary['spawned_children'] == summary['returned_direct_calls_with_valid_protocol'] == 25
    assert summary['inherited_not_executed'] == 7 and summary['retries'] == 0 and summary['unattempted_ids'] == []
    assert summary['authority_before'] == summary['authority_after'] == pins
    outputs = {}
    full_imports = None
    fixtures = []
    for receipt, row in zip(records, fresh):
        stdout, stderr, raw = [(HERE / (row['id'] + suffix)).read_bytes() for suffix in ('.stdout', '.stderr', '.raw')]
        parsed = rawcheck(receipt, row, plan, runtime, stdout, stderr, raw)
        if full_imports is None:
            full_imports = parsed['imports_bound_not_invoked']
        assert full_imports == parsed['imports_bound_not_invoked']
        outputs[row['id']] = {'id': row['id'], 'provenance': 'fresh-once-only-original-call', 'fresh_receipt_pointer': '#/' + str(row['fresh_ordinal'] - 1),
                              'output_hex': raw.hex(), 'output_u32_hex': parsed['output_u32_hex'], 'raw_payload': row['id'] + '.raw', 'oracle_prediction': None}
        fixtures.append((receipt, row, stdout, stderr, raw))
    for earlier, later in zip(records, records[1:]):
        assert earlier['finished_utc'] <= later['started_utc']
    inherited = load('inherited-controls.json')['rows']
    assert len(inherited) == 7
    source = next(p for p in pins if p['path'].endswith('/batch-mix-leaves-v1/inputs.json'))
    for i, item in enumerate(inherited):
        row = next(r for r in catalog['rows'] if r['id'] == item['id'])
        assert row['disposition'] == 'inherited-not-executed' and row['inherited_id'] == item['inherited_id']
        assert row['tokens'] == item['tokens'] and item['provider'] == source
        assert item['fresh_receipt'] is None
        assert item['historical_provenance']['recorded_patches'] == []
        assert item['historical_provenance']['recorded_rc'] == 0 and not item['historical_provenance']['recorded_timeout']
        dump = re.findall(r'^dump b2 0x[0-9a-f]+ ([0-9a-f]{32})$', item['historical_stdout'], re.M)
        assert dump == [item['output_hex']]
        assert item['tokens'][3] == 'hex:' + row['input_hex']
        words = struct.unpack('<4I', bytes.fromhex(item['output_hex']))
        assert all((w & 0x7f800000) != 0x7f800000 for w in words)
        outputs[row['id']] = {'id': row['id'], 'provenance': 'inherited-approved-historical-output-not-new-call', 'inherited_projection_pointer': '#/rows/' + str(i),
                              'inherited_id': item['inherited_id'], 'output_hex': item['output_hex'], 'output_u32_hex': [f'{x:08x}' for x in words], 'fresh_receipt': None}
    assert len(outputs) == 32 and len({r['input_hex'] for r in catalog['rows']}) == 32
    receipt, row, stdout, stderr, raw = fixtures[0]
    negatives = []
    for name, change in [('replayed historical id', lambda r: r.__setitem__('id', inherited[0]['id'])),
                         ('invented fresh import use', lambda r: r['protocol']['actual_used_import_counts'].__setitem__('_cos', 1)),
                         ('custody drift', lambda r: r['after'][0].__setitem__('sha256', '0' * 64)),
                         ('wrong argv input', lambda r: r['argv'].__setitem__(-5, 'hex:' + '00' * 52)),
                         ('recorded fault', lambda r: r.__setitem__('exit_status', 87)),
                         ('fabricated timeout success', lambda r: r.__setitem__('timed_out', True)),
                         ('incomplete return lane', lambda r: r['protocol']['return_lanes_u64_hex'].__setitem__('rax', '0'))]:
        bad = copy.deepcopy(receipt)
        change(bad)
        try:
            rawcheck(bad, row, plan, runtime, stdout, stderr, raw)
        except AssertionError:
            negatives.append(name)
        else:
            raise AssertionError('Bad receipt accepted: ' + name)
    for name, s, e, r in [('changed stdout', stdout + b'junk\n', stderr, raw), ('unexpected stderr', stdout, b'error', raw), ('changed raw output', stdout, stderr, bytes([raw[0] ^ 1]) + raw[1:])]:
        try:
            rawcheck(receipt, row, plan, runtime, s, e, r)
        except AssertionError:
            negatives.append(name)
        else:
            raise AssertionError('Bad retained bytes accepted: ' + name)
    checks['retained_packet'] = negatives
    all_outputs = [outputs[r['id']] for r in catalog['rows']]
    checks.update(status='PASS', logical_tuples=32, fresh_children=25, direct_returned_original_entries=25,
                  fresh_output_bytes=400, inherited_joins=7, fresh_inherited_replays=0,
                  all_output_words_finite=True, recorded_runtime_custody_pairs=25 * len(runtime),
                  distinct_import_binding_records=len(full_imports), actual_used_imports_all_children={},
                  data_only_original_calls=0, all_output_inventory=all_outputs)
    return checks


if __name__ == '__main__':
    assert sys.argv[1:] == ['--check']
    result = check()
    print(json.dumps(result, indent=2))
