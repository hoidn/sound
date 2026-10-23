#!/usr/bin/env python3
"""Independent stdlib audit of frozen bytes/logs only. No original/collector imports or execution."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import math
import re
import struct

ROOT = Path(__file__).resolve().parents[4]
F = ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
ACT = F/'batch-analog-change-history-v1-actual'
PREP = F/'batch-analog-change-history-v1-preparation'
OUT = F/'reviews'


def read(p):
    return json.loads(p.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(p):
    raw = p.read_bytes()
    try:
        name = str(p.relative_to(ROOT))
    except ValueError:
        name = str(p)
    return dict(path=name, bytes=len(raw), sha256=sha(raw))


def verify(p, pin):
    got = identity(p)
    assert (got['bytes'], got['sha256']) == (pin['bytes'], pin['sha256']), str(p)
    return got


def values(raw, frames):
    assert len(raw) == frames*8, 'size'
    rows = list(struct.iter_unpack('<ff', raw))
    assert all(math.isfinite(x) and math.isfinite(y) for x, y in rows), 'nonfinite'
    return rows


def compare(raw_a, raw_b, frames, boundary):
    a, b = values(raw_a, frames), values(raw_b, frames)
    energy = [math.fsum(row[c]*row[c] for row in a) for c in (0, 1)]
    assert all(math.isfinite(e) and e > 0 for e in energy), 'baseline energy'
    assert raw_a[:8*boundary] == raw_b[:8*boundary], 'prefix bytes'
    assert all(a[k] == b[k] for k in range(boundary)), 'prefix values'
    first = [None, None]
    for n, (left, right) in enumerate(zip(a, b)):
        for c in (0, 1):
            if first[c] is None and left[c] != right[c]:
                first[c] = n
    joint = min((n for n in first if n is not None), default=None)
    return dict(baseline_energy_left=energy[0], baseline_energy_right=energy[1],
                first_numeric_difference=dict(left=first[0], right=first[1], joint=joint),
                first_numeric_difference_from_change={k: None if v is None else v-boundary
                    for k, v in zip(['left', 'right', 'joint'], [*first, joint])},
                prechange_byte_identity=True, prechange_numeric_identity=True,
                baseline_sha256=sha(raw_a), changed_sha256=sha(raw_b),
                full_byte_identity=raw_a == raw_b, all_samples_finite=True)


def fabricated_checks():
    pack = lambda rows: b''.join(struct.pack('<ff', *r) for r in rows)
    base = pack([(1., 2.), (0., 0.), (0., 0.), (1., 2.)])
    signed = pack([(1., 2.), (0., 0.), (-0., 0.), (2., 2.)])
    assert compare(base, signed, 4, 2)['first_numeric_difference'] == dict(left=3, right=None, joint=3)
    other = pack([(1., 2.), (0., 0.), (0., 3.), (2., 2.)])
    assert compare(base, other, 4, 2)['first_numeric_difference'] == dict(left=3, right=2, joint=2)
    assert compare(base, base, 4, 2)['first_numeric_difference'] == dict(left=None, right=None, joint=None)
    rejected = []
    for name, a, b in [
        ('wrong byte length', base, base[:-1]),
        ('NaN anywhere in full capture', base, pack([(1.,2.), (0.,0.), (0.,0.), (math.nan,2.)])),
        ('infinity in full capture', base, pack([(1.,2.), (0.,0.), (0.,0.), (1.,math.inf)])),
        ('one silent baseline channel', pack([(1.,0.)]*4), pack([(1.,0.)]*4)),
        ('preboundary signed-zero byte mutation', base, pack([(1.,2.), (-0.,0.), (0.,0.), (1.,2.)])),
        ('preboundary numeric mutation', base, pack([(2.,2.), (0.,0.), (0.,0.), (1.,2.)])),
    ]:
        try:
            compare(a, b, 4, 2)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('accepted bad fixture '+name)
    return dict(negative_fixtures_rejected=rejected,
                positive_checks=['postboundary signed zero ignored numerically', 'independent left/right first difference order', 'unchanged pair returns None'])


def main():
    manifests = []
    for root, digest in [(ACT, '655b36ebb0f639e0d83522167159efe076fed2867aaa9e246530ba74f601d54a'),
                         (PREP, '8a3398038345a241b72c13a11e356ae0d6bb2136edf6dbc6b09550b2f284f0f2')]:
        pin = identity(root/'manifest.json'); assert pin['sha256'] == digest
        m = read(root/'manifest.json')
        for item in m['files']:
            verify(root/item['path'], item)
        manifests.append(dict(**pin, payloads=len(m['files']), payload_bytes=sum(p['bytes'] for p in m['files'])))
    assert manifests[0]['bytes'] == 5826 and manifests[0]['payloads'] == 34 and manifests[0]['payload_bytes'] == 2943123
    readiness_path = OUT/'analog-change-history-v1-readiness-review.json'
    assert identity(readiness_path)['sha256'] == '2018055b0fcde87a47273f4d544a0ca06b83900eb77b576e75332f3aba27913c'
    ready = read(readiness_path); assert ready['ready_for_root_execution'] is True
    assert ready['disposition'] == 'approved-bounded-analog-change-history-preparation'
    assert ready['reviewed_manifest']['sha256'] == manifests[1]['sha256']
    plan, selection, ids, vector = [read(PREP/n) for n in ['execution-plan.json','selection.json','identities.json','baseline-vector.json']]
    checked = []
    for p in ids['source_pins'] + ids['external_pins']:
        path = Path(p['path']); path = path if path.is_absolute() else ROOT/path
        checked.append(verify(path, p))
        assert str(path.resolve()) == p['resolved_path']
    bundle = ids['original_bundle']; raw = Path(bundle['path']).read_bytes()
    assert sha(raw) == bundle['file_sha256']
    assert sha(raw[bundle['x86_64_offset']:bundle['x86_64_offset']+bundle['x86_64_size']]) == bundle['x86_64_sha256']
    ev = read(ROOT/'handoff/device-analog-v1/cases.json')['cases'][11]['evaluations'][0]
    assert ev['id'] == 'ANALOG-AUDIO-013-01' and len(vector['entries']) == 203
    for index, e in enumerate(vector['entries']):
        assert e['index'] == index and e['label'] == ev['parameter_order'][index]
        assert struct.pack('<f', e['binary32_value']).hex() == e['binary32_little_endian_hex']
        assert struct.pack('<f', e['binary32_value']) == struct.pack('<f', ev['parameters'][e['label']])
    actual = read(ACT/'actual-record.json'); assert actual['original_execution_attempted'] and actual['original_processes_started'] == 16
    assert actual['preparation_manifest_sha256'] == manifests[1]['sha256']
    assert actual['readiness_receipt']['sha256'] == identity(readiness_path)['sha256']
    assert len(actual['runs']) == len(plan['runs']) == 16 and len(actual['pairs']) == len(plan['pairs']) == 8
    assert [r['id'] for r in actual['runs']] == plan['run_order']
    run_data, audits, use_maps = {}, [], []
    bindings = None
    exports = None
    for run, intended in zip(actual['runs'], plan['runs']):
        assert run['argv'] == intended['argv'] and run['environment'] == intended['environment'] == ids['planned_child_environment']
        assert run['limits'] == plan['limits'] and run['attempt'] == 1 and run['returncode'] == 0 and run['status'] == 'captured-UNGRADED'
        script = PREP/intended['script']['path']; verify(script, intended['script'])
        text = script.read_text().splitlines()
        target = next(t for t in selection['targets'] if t['id'] == intended['control_id'])
        expected = ['mxcsr 0x1f80', 'create', 'rate 44100']
        expected += [f"param {e['index']} {e['binary32_value']!r}" for e in vector['entries']]
        update = target['baseline_binary32'] if intended['role'] == 'baseline' else target['target_binary32']
        expected += ['transport 0 0 120', 'event 8192 0x90 48 100', 'inflag 0', 'input zero', 'process 13312 512', f"param {target['index']} {update!r}", 'process 7680 512', 'destroy']
        assert text == expected
        assert 8192 < 13312 and not 8192 < 7680  # queue event belongs only to first local process interval
        lograw = (ACT/run['id']/'loader.log').read_bytes(); log = lograw.decode()
        assert len(lograw) <= 262144 and not re.search(r'^(TRAP\b|FAULT\b|xdev:)', log, re.M)
        assert log.count('create ok\n') == 1 and 'create NULL' not in log
        assert re.findall(r'^cxx-failbits (\d+)$', log, re.M) == ['0']
        assert re.findall(r'^init (\S+)$', log, re.M) == ['0x314d0']
        assert re.findall(r'^slice offset=(\d+) size=(\d+)$', log, re.M) == [('16384','500880')]
        params = re.findall(r'^param (\d+) (\S+)$', log, re.M)
        assert len(params) == 204 and [int(n) for n,_ in params[:203]] == list(range(203))
        for (n,v), entry in zip(params[:203], vector['entries']):
            assert struct.pack('<f', float(v)) == struct.pack('<f', entry['binary32_value'])
        assert int(params[-1][0]) == target['index'] and struct.pack('<f',float(params[-1][1])) == struct.pack('<f',update)
        assert re.findall(r'^event (.*)$',log,re.M) == ['8192 0x90 48 100']
        assert re.findall(r'^rate (.*)$',log,re.M) == ['44100 ret=1'] and re.findall(r'^destroy$',log,re.M) == ['destroy']
        process = re.findall(r'^process (\d+) (\d+) flags:(.*) blocks=(\d+)$',log,re.M)
        assert [(int(n),int(b),int(k)) for n,b,_,k in process] == [(13312,512,26),(7680,512,15)]
        for _,_,states,count in process:
            groups = re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',states)
            assert sum(int(n) for n,_,_ in groups) == int(count) and all(ret == '0' for _,ret,_ in groups)
        ex = re.findall(r'^export (\S+) (\S+)$',log,re.M); assert len(ex) == 7
        if exports is None: exports = ex
        assert ex == exports
        imports = re.findall(r'^import (linux|data|trap) (\S+) slots=(\d+)$',log,re.M)
        if bindings is None: bindings = imports
        assert imports == bindings and len(imports) == 132
        types = collections.Counter(t for t,_,_ in imports); assert types == {'linux':99,'data':7,'trap':26}
        used = {s:int(n) for s,n in re.findall(r'^used (\S+) (\d+)$',log,re.M)}
        assert len(used) == 64 and all(n > 0 for n in used.values())
        assert set(used) <= {s for t,s,_ in imports if t == 'linux'}
        assert (used['_rand'],used['_srand'],used['_time'],used['___cxa_atexit']) == (129,1,1,2)
        use_maps.append(used)
        raw = (ACT/run['id']/'output.f32').read_bytes(); rows = values(raw,20992)
        assert sha(raw) == run['output']['sha256'] and len(raw) == run['output']['bytes'] == 167936
        assert sha(lograw) == run['log_checks']['loader_log_sha256']
        run_data[run['id']] = raw
        audits.append(dict(id=run['id'],returncode=0,attempts=1,frames=20992,bytes=167936,all_finite=True,
                           direct_exports=248,CalcA=41,init_entries=['0x314d0'],import_binding_types=dict(types),
                           used_import_counter_rows=64,used_import_counter_sum=sum(used.values()),
                           used_counter_map_sha256=sha(json.dumps(used,sort_keys=True).encode()),
                           log_bytes=len(lograw),log_sha256=sha(lograw),output_sha256=sha(raw),process_status_rows=[states for _,_,states,_ in process]))
    pairs = []
    for intended, recorded in zip(plan['pairs'],actual['pairs']):
        assert intended['id'] == recorded['id']
        a,b = run_data[intended['baseline_run']], run_data[intended['change_run']]
        got = compare(a,b,20992,13312)
        old = recorded['measurement']
        for field in ['baseline_energy_left','baseline_energy_right','first_numeric_difference','first_numeric_difference_from_change','prechange_byte_identity','prechange_numeric_identity']:
            assert got[field] == old[field], (intended['id'],field)
        assert got['baseline_sha256'] == old['sha256'] and got['changed_sha256'] == old['change_output_sha256']
        assert recorded['expectation'] == 'unknown; no grade'
        target = next(t for t in selection['targets'] if t['id'] == intended['id'])
        pairs.append(dict(control_id=intended['id'],label=target['comparison_label'],index=target['index'],baseline=target['baseline_binary32'],target=target['target_binary32'],**got))
    assert len({p['baseline_sha256'] for p in pairs}) == 1
    assert [p['first_numeric_difference']['joint'] for p in pairs] == [13376,13380,13380,13332,13380,13357,13357,None]
    assert pairs[-1]['full_byte_identity'] is True
    usage = {s:dict(min=min(u[s] for u in use_maps),max=max(u[s] for u in use_maps)) for s in use_maps[0]}
    outer_path = OUT/'batch-analog-change-history-v1-root-execution.json'; outer = read(outer_path)
    assert outer['returncode'] == 0 and outer['status'] == 'collector-returned'
    assert outer['preparation_manifest_sha256'] == manifests[1]['sha256'] and outer['readiness_receipt_sha256'] == identity(readiness_path)['sha256']
    assert outer['argv'][-2:] == ['--execute-after-review', str(readiness_path)]
    assert outer['started_utc'] < outer['ended_utc'] and outer['elapsed_seconds'] > 0
    data = dict(status='PASS-independent-frozen-data-audit-UNGRADED',reviewer='independent analyst /root/mix_routes',
                manifests=manifests,readiness=identity(readiness_path),root_outer_receipt=identity(outer_path),
                selected_source_and_external_pins_checked=checked,baseline_evaluation='ANALOG-AUDIO-013-01:203component payload/order exact',
                runs=audits,pairs=pairs,export_addresses=exports,used_import_counter_ranges=usage,
                totals=dict(original_children_recorded=16,direct_exports=16*248,CalcA=16*41,raw_bytes=16*167936),
                reviewer_byte_checks=fabricated_checks(),
                observations='Seven finite paired first differences; AttackTime unchanged through full20992frames. No general latency, trajectory, smoothing, latching, settling, ARM or Live inference.',
                instrumentation_limits='248 bounds direct exported calls only. One init line per child; nested initializer/original constructor/library entries not counted or capped by256. Import counter sums are intercepted function-call instrumentation, not complete native-call counts; data access counts not instrumented. No per-original-child PID/UTC/elapsed or peak resource consumption.',
                source_execution_by_reviewer=False,collector_or_harness_or_model_or_comparator_run=False)
    (OUT/'batch-analog-change-history-v1-actual-review-data.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],pairs=[dict(id=p['control_id'],first=p['first_numeric_difference'],after=p['first_numeric_difference_from_change']) for p in pairs],baseline_energy=pairs[0]['baseline_energy_left'],direct_exports=3968,CalcA=656)))


if __name__ == '__main__':
    main()
