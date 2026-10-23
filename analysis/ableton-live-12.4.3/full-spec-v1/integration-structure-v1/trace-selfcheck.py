"""Owned synthetic checks of the unchanged shared tracer; no original graph run."""
from pathlib import Path
from tempfile import TemporaryDirectory
import copy
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
HELPER = HERE / 'trace.py'
EXPECTED = 'd1fa658bc2e74449034348b34c79eead0e8487f04f118282dd44d8e6a4dc7c24'
RESULT = HERE / 'trace-selfcheck-result.json'


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def put(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def stream(path, records):
    raw = b''.join((json.dumps(r) + '\n').encode() for r in records)
    path.write_bytes(raw)
    return {'lines': len(records), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def rejected(operation):
    try:
        operation()
    except AssertionError:
        return
    raise AssertionError('Expected actual tracer assertion rejection')


def run():
    assert identity(HELPER)['sha256'] == EXPECTED
    watched = [HELPER, HERE / 'hubs.json',
               HERE.parent / 'component-resolution-v1' / 'manifest.json']
    watched += sorted(HERE.glob('transport-*'))
    before = {str(p): identity(p) for p in watched if p.is_file()}
    # A non-main run loads definitions only. Redirect filesystem inputs, not logic.
    namespace = runpy.run_path(str(HELPER), run_name='synthetic_trace_library')
    trace, rows = namespace['trace'], namespace['rows']
    environment = trace.__globals__
    assert rows.__globals__ is environment
    checks = []
    with TemporaryDirectory(prefix='sound-owned-trace-selfcheck-') as temporary:
        root = Path(temporary)
        index, output, previous_dir = root / 'index', root / 'output', root / 'previous'
        for path in (index, output, previous_dir):
            path.mkdir()
        environment.update(INDEX=index, HERE=output, PREVIOUS=previous_dir)
        calls = [
            {'caller': '0x10', 'callee': '0x20', 'site': '0x104', 'kind': 'call'},
            {'caller': '0x20', 'callee': '0x30', 'site': '0x204', 'kind': 'call'},
            {'caller': '0x30', 'callee': '0x40', 'site': '0x304', 'kind': 'call'},
            {'caller': '0x10', 'callee': '0x90', 'site': '0x10c', 'kind': 'call'},
        ]
        indirect = [
            {'function': '0x10', 'site': '0x108', 'kind': 'call', 'resolved_targets': []},
            {'function': '0x20', 'site': '0x208', 'kind': 'jump',
             'resolved_targets': [{'address': '0x2a', 'function': None}]},
            {'function': '0x20', 'site': '0x20c', 'kind': 'call',
             'resolved_targets': [{'address': '0x35', 'function': '0x35'}]},
            {'function': '0x30', 'site': '0x30c', 'kind': 'jump',
             'resolved_targets': [{'address': '0x38', 'function': '0x38'}]},
        ]
        overlay = [{'function': '0x30', 'target': '0x39', 'site': '0x310',
                    'premises': ['SYNTHETIC stable receiver only'],
                    'status': 'new_conditional_static_exact_target'}]
        manifest = {'files': {
            'calls.jsonl': stream(index / 'calls.jsonl', calls),
            'indirect.jsonl': stream(index / 'indirect.jsonl', indirect)}}
        overlay_pin = stream(previous_dir / 'indirect-resolution.jsonl', overlay)
        previous = {'files': [{'path': 'indirect-resolution.jsonl',
                               'bytes': overlay_pin['bytes'], 'sha256': overlay_pin['sha256']}],
                    'additional_conditional_class_slot_sites': 1}
        put(output / 'hubs.json', {'calls_source': manifest['files']['calls.jsonl'],
                                  'hubs': [{'entry': '0x90'}]})
        seeds = output / 'synthetic-seeds.json'
        put(seeds, {'entries': ['0x10'], 'sinks': ['0x40']})
        assert len(list(rows('calls.jsonl', manifest))) == 4
        checks.append('Actual rows() accepts complete correct synthetic stream')
        results = []
        for depth in (1, 2, 3):
            trace(seeds, depth, previous, manifest)
            result = json.loads((output / f'synthetic-trace-depth{depth}.json').read_text())
            assert len(result['waves']) == depth
            results.append(result)
        assert results[0]['waves'] == results[1]['waves'][:1] == results[2]['waves'][:1]
        assert results[1]['waves'] == results[2]['waves'][:2]
        waves = results[2]['waves']
        assert [w['forward']['next_frontier'] for w in waves] == [
            ['0x20'], ['0x30', '0x35'], ['0x38', '0x39', '0x40']]
        assert [w['backward']['next_frontier'] for w in waves] == [
            ['0x30'], ['0x20'], ['0x10']]
        checks.append('Actual trace() depth1/2/3 prefixes and both directional transitions match')
        assert [(e['source'], e['target']) for e in waves[0]['forward']['pruned_hub_edges']] == [
            ('0x10', '0x90')]
        for wave in waves:
            for direction in ('forward', 'backward'):
                assert wave[direction]['edge_budget_omissions'] == 0
                assert wave[direction]['node_budget_omissions'] == []
        assert {e['kind'] for e in waves[1]['forward']['edges']} == {'call', 'indirect-call'}
        assert {e['kind'] for e in waves[2]['forward']['edges']} == {
            'call', 'indirect-jump', 'conditional-class-slot'}
        checks.append('Kinds preserved, hub omission explicit, no unexpected finite-budget omissions')
        unknown = {r['site']: r for r in results[2]['unresolved_indirect_frontiers']}
        assert set(unknown) == {'0x108', '0x208'}
        assert unknown['0x108']['evidence']['record']['resolved_targets'] == []
        assert unknown['0x208']['evidence']['record']['resolved_targets'][0]['function'] is None
        edges = [e for w in waves for d in ('forward', 'backward') for e in w[d]['edges']]
        assert all(e['target'] != '0x2a' and e['site'] != '0x208' for e in edges)
        checks.append('Empty-target and interior-jump unknown retained; interior address not a function edge')
        bad = copy.deepcopy(manifest)
        bad['files']['calls.jsonl']['sha256'] = '0' * 64
        rejected(lambda: list(rows('calls.jsonl', bad)))
        checks.append('Actual rows() rejects deliberately wrong streamed source SHA')
        # Match the hub manifest to bad input so failure must occur in rows(), not hub setup.
        put(output / 'hubs.json', {'calls_source': bad['files']['calls.jsonl'], 'hubs': []})
        bad_seeds = output / 'wrong-hash-seeds.json'
        put(bad_seeds, {'entries': ['0x10'], 'sinks': ['0x40']})
        rejected(lambda: trace(bad_seeds, 1, previous, bad))
        assert not (output / 'wrong-hash-trace-depth1.json').exists()
        checks.append('Actual trace() rejects wrong streamed SHA before output creation')
        summary = [{'level': w['level'], 'forward_frontier': w['forward']['next_frontier'],
                    'backward_frontier': w['backward']['next_frontier']} for w in waves]
    after = {path: identity(Path(path)) for path in before}
    assert before == after
    assert identity(HELPER)['sha256'] == EXPECTED
    with RESULT.open('x') as f:
        json.dump({'status': 'PASS', 'scope': 'Owned synthetic fixtures only; no real graph rerun',
                   'helper': identity(HELPER), 'method': identity(Path(__file__)),
                   'checks': checks, 'synthetic_wave_summary': summary,
                   'watched_file_count': len(before), 'before': before, 'after': after,
                   'watches_unchanged': True,
                   'limits': 'Only module path globals redirected to TemporaryDirectory; actual trace()/rows() logic unchanged. setup()/CLI not invoked. No original, provider, decoder, or runtime execution.'}, f, indent=2)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'checks': len(checks), 'watch': len(before)}))


if __name__ == '__main__':
    run()
