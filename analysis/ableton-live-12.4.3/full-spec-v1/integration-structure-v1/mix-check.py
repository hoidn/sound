"""Validate only mix-owned retained rows and graph receipts; no source program runs."""
from pathlib import Path
import hashlib
import json
import sys

D = Path(__file__).resolve().parent

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    assert sys.argv[1:] == ['--check'], 'Read-only --check only'
    context = json.loads((D / 'mix-seed-explanation.json').read_bytes())
    for pin in context['immutable_source_pins']:
        raw = Path(pin['path']).read_bytes()
        assert (len(raw), sha(raw)) == (pin['bytes'], pin['sha256'])
    # Mutable canonical hashes in the author-time context are deliberately not gates.
    source_rows = json.loads((D / 'mix-seed-sources.json').read_bytes())
    source_rows += [json.loads((D / 'mix-builder-source.json').read_bytes())]
    source_rows += json.loads((D / 'mix-wiring-helper-sources.json').read_bytes())
    source_rows += [json.loads((D / 'mix-connection-core-source.json').read_bytes())]
    complete = {}
    for row in source_rows:
        if 'raw_excerpt_sha256' in row:
            raw = Path(row['provider']).read_bytes().splitlines(keepends=True)[row['line']-1]
            assert sha(raw) == row['raw_excerpt_sha256']
            actual = json.loads(raw)['record']
        else:
            with Path(row['provider']).open('rb') as f:
                f.seek(row['byte_offset'])
                raw = f.readline()
            assert sha(raw) == row['raw_row_sha256']
            actual = json.loads(raw)
        for key, value in row['record'].items():
            assert actual[key] == value, (actual['entry'], key)
        if 'code' in row['record']:
            code = actual['code'].encode()
            assert (len(code), sha(code)) == (actual['code_bytes'], actual['code_sha256'])
            complete[actual['entry']] = len(code)
    assert len(complete) == 10 and sum(complete.values()) == 103736
    expected = [(97,20,501),(18,10,42),(9,9,56)]
    for depth in (1,2,3):
        raw = (D / f'mix-trace-depth{depth}.json').read_bytes()
        trace = json.loads(raw)
        assert trace['script_sha256'] == 'd1fa658bc2e74449034348b34c79eead0e8487f04f118282dd44d8e6a4dc7c24'
        assert trace['seed_sha256'] == sha((D / 'mix-seeds.json').read_bytes())
        review = json.loads((D / f'mix-frontier-depth{depth}-review.json').read_bytes())
        assert review['trace_sha256'] == sha(raw)
        for level, wave in enumerate(trace['waves']):
            q = wave['forward']
            assert (len(q['edges']),len(q['next_frontier']),len(q['pruned_hub_edges'])) == expected[level]
            assert not wave['backward']['edges'] and not wave['frontier_intersection']
            assert q['edge_budget_omissions'] == 0 and not q['node_budget_omissions']
    graph = json.loads((D / 'mix-component-edges.json').read_bytes())
    assert len(graph['edges']) == 9 and graph['runtime_route'] is None and graph['grade'] is None
    assert graph['generic_connection_boundary']['class_slot_resolution'].startswith('NONE')
    print(json.dumps(dict(status='PASS', complete_C_functions=len(complete), complete_C_bytes=sum(complete.values()), waves=3, static_source_edges=9, runtime_route=None, grade=None)))

if __name__ == '__main__':
    main()
