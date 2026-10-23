"""Read-only, bounded index search. No source program, provider or decoder runs."""
from collections import Counter
from pathlib import Path
import argparse
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
PREVIOUS = HERE.parent / 'component-resolution-v1'
PIN = '392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b'
MAX_NODES, MAX_EDGES = 80, 200


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def node_key(value):
    return (0, int(value, 16)) if value.startswith('0x') else (1, value)


def save(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def setup():
    raw = (PREVIOUS / 'manifest.json').read_bytes()
    assert sha(raw) == PIN
    previous = json.loads(raw)
    raw = (INDEX / 'manifest.json').read_bytes()
    assert sha(raw) == '8451d3023394e6a242793d628ba8e1c29a107757a10da51469bcade8c6e583f5'
    return previous, json.loads(raw)


def rows(name, manifest):
    """Hash the entire stream; callers must consume it fully, including omissions."""
    h, size, count = hashlib.sha256(), 0, 0
    with (INDEX / name).open('rb') as f:
        for raw in f:
            off = size
            h.update(raw)
            size += len(raw)
            count += 1
            yield json.loads(raw), raw, count, off
    p = manifest['files'][name]
    assert (count, size, h.hexdigest()) == (p['lines'], p['bytes'], p['sha256'])


def locator(name, raw, line, off):
    return dict(path=str(INDEX / name), line=line, byte_offset=off,
                raw_bytes=len(raw), raw_sha256=sha(raw))


def overlay_rows(raw):
    records = [json.loads(x) for x in raw.splitlines()]
    for r in records:
        assert all(k in r for k in ('function', 'target', 'site', 'premises', 'status'))
        assert r['status'] == 'new_conditional_static_exact_target'
        assert isinstance(r['premises'], list) and r['premises']
        assert all(isinstance(r[k], str) and r[k].startswith('0x') for k in ('function', 'target', 'site'))
    return records


def select(candidates, hubs, seeds, seen):
    ordered = sorted(candidates, key=lambda e: (node_key(e['source']), node_key(e['target']),
                                               node_key(e['site']), e['kind']))
    pruned, usable = [], []
    for edge in ordered:
        (pruned if edge['next'] in hubs and edge['next'] not in seeds else usable).append(edge)
    chosen = usable[:MAX_EDGES]
    possible = sorted({e['next'] for e in chosen} - seen, key=node_key)
    return dict(edges=chosen, pruned_hub_edges=pruned,
                edge_budget_omissions=len(usable) - len(chosen),
                next_frontier=possible[:MAX_NODES],
                node_budget_omissions=possible[MAX_NODES:])


def selfcheck():
    def edge(target, site='0x10'):
        return dict(source='0x1', target=target, next=target, site=site, kind='test')
    q = select([edge('0x2'), edge('0x3'), edge('0x1')], {'0x2'}, {'0x1'}, {'0x1'})
    assert q['next_frontier'] == ['0x3'] and len(q['pruned_hub_edges']) == 1
    assert len(select([edge('0x2')], {'0x2'}, {'0x2'}, set())['edges']) == 1
    assert select([edge('EXTERNAL:0x523')], set(), set(), set())['next_frontier'] == ['EXTERNAL:0x523']
    assert node_key('0x1') < node_key('EXTERNAL:0x1')
    valid = dict(function='0x1', target='0x2', site='0x3', premises=['stable receiver'], status='new_conditional_static_exact_target')
    assert overlay_rows(json.dumps(valid).encode()) == [valid]
    invalid = dict(valid)
    invalid['implementation_targets'] = [invalid.pop('target')]
    try:
        overlay_rows(json.dumps(invalid).encode())
    except AssertionError:
        pass
    else:
        raise AssertionError('Prototype overlay schema must be rejected before traversal')
    q = select([edge(hex(i + 10), hex(i + 100)) for i in range(300)], set(), set(), set())
    assert len(q['edges']) == 200 and q['edge_budget_omissions'] == 100
    assert len(q['next_frontier']) == 80 and len(q['node_budget_omissions']) == 120


def make_hubs(manifest):
    degree, labels, functions = Counter(), {}, set()
    for r, _, _, _ in rows('calls.jsonl', manifest):
        target = r.get('callee_resolved') or r['callee']
        if target:
            degree[target] += 1
            labels[target] = r.get('callee_resolved_name') or r.get('callee_name')
            functions.add(target)
        functions.add(r['caller'])
    ranked = sorted(degree, key=lambda a: (-degree[a], node_key(a)))[:1000]
    save(HERE / 'hubs.json', dict(rule='Top1000 by incoming row occurrences, resolved-thunk target preferred; numeric VA breaks ties. Explicit seeds exempt from pruning.',
         calls_source=manifest['files']['calls.jsonl'], source_and_target_function_keys=len(functions),
         external_metadata_keys=sum(a.startswith('EXTERNAL:') for a in functions),
         hubs=[dict(entry=a, incoming_rows=degree[a], label=labels[a]) for a in ranked]))


def trace(seed_path, depth, previous, manifest):
    seed_raw = seed_path.read_bytes()
    seed = json.loads(seed_raw)
    assert all(k in seed for k in ('entries', 'sinks'))
    for k in ('entries', 'sinks'):
        assert 0 < len(seed[k]) <= MAX_NODES and len(set(seed[k])) == len(seed[k])
        assert all(isinstance(a, str) and a == hex(int(a, 16)) and 0 <= int(a, 16) < 2**64 for a in seed[k])
    hubraw = (HERE / 'hubs.json').read_bytes()
    hubdata = json.loads(hubraw)
    assert hubdata['calls_source'] == manifest['files']['calls.jsonl']
    hubs = {x['entry'] for x in hubdata['hubs']}
    overlay_raw = (PREVIOUS / 'indirect-resolution.jsonl').read_bytes()
    pin = next(x for x in previous['files'] if x['path'] == 'indirect-resolution.jsonl')
    assert len(overlay_raw) == pin['bytes'] and sha(overlay_raw) == pin['sha256']
    overlay = overlay_rows(overlay_raw)
    assert len(overlay) == previous['additional_conditional_class_slot_sites']
    front = dict(forward=set(seed['entries']), backward=set(seed['sinks']))
    exempt = front['forward'] | front['backward']
    seen = {k: set(v) for k, v in front.items()}
    waves, unknown = [], {}
    for level in range(1, depth + 1):
        candidates = dict(forward=[], backward=[])

        def add(source, target, site, kind, evidence, status):
            for direction in candidates:
                at, other = (source, target) if direction == 'forward' else (target, source)
                if at in front[direction]:
                    candidates[direction].append(dict(source=source, target=target, next=other,
                        site=site, kind=kind, status=status, evidence=evidence))

        for r, raw, line, off in rows('calls.jsonl', manifest):
            target = r.get('callee_resolved') or r['callee']
            if target and (r['caller'] in front['forward'] or target in front['backward']):
                add(r['caller'], target, r['site'], r['kind'],
                    dict(locator=locator('calls.jsonl', raw, line, off), record=r),
                    'observed retained static call reference; runtime unknown')
        considered = seen['forward'] | seen['backward']
        for r, raw, line, off in rows('indirect.jsonl', manifest):
            relevant = r['function'] in front['forward'] or any(t.get('function') in front['backward'] for t in r['resolved_targets'])
            where = None
            if relevant or r['function'] in considered:
                where = locator('indirect.jsonl', raw, line, off)
            if relevant:
                for t in r['resolved_targets']:
                    if t.get('function'):
                        add(r['function'], t['function'], r['site'], 'indirect-' + r['kind'],
                            dict(locator=where, record=r), 'observed analyzer reference; actual target unknown')
            if r['function'] in considered and (not r['resolved_targets'] or any(not t.get('function') for t in r['resolved_targets'])):
                unknown[r['site']] = dict(function=r['function'], site=r['site'], kind=r['kind'],
                    status='unknown cross-function target; not a dead-end assertion', evidence=dict(locator=where, record=r))
        for i, r in enumerate(overlay, 1):
            add(r['function'], r['target'], r['site'], 'conditional-class-slot',
                dict(packet_manifest_sha256=PIN, path='component-resolution-v1/indirect-resolution.jsonl', line=i,
                     premises=r['premises']), 'inferred only under recorded receiver/vptr premises')
        wave = dict(level=level, expanded={k: sorted(v, key=node_key) for k, v in front.items()})
        for direction in front:
            q = select(candidates[direction], hubs, exempt, seen[direction])
            wave[direction] = q
            front[direction] = set(q['next_frontier'])
            seen[direction].update(front[direction])
        wave['external_metadata_frontiers'] = {k: sorted(a for a in v if not a.startswith('0x')) for k, v in front.items()}
        wave['frontier_intersection'] = sorted(seen['forward'] & seen['backward'], key=node_key)
        waves.append(wave)
    save(seed_path.with_name(seed_path.stem.replace('-seeds', '') + '-trace-depth' + str(depth) + '.json'),
         dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), previous_manifest_sha256=PIN,
              script_sha256=sha(Path(__file__).read_bytes()), seed_sha256=sha(seed_raw), hubs_sha256=sha(hubraw),
              seeds=seed, max_nodes_per_direction_level=MAX_NODES, max_edges_per_direction_level=MAX_EDGES,
              max_depth=depth, waves=waves, unresolved_indirect_frontiers=list(unknown.values()),
              limits='Static index search only. Budgets/pruning do not prove absence; intersections are function references, not execution order. Review each frontier before choosing a deeper run. No semantic component or behavior grade.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hubs', action='store_true')
    parser.add_argument('--seeds', type=Path)
    parser.add_argument('--depth', type=int, choices=(1, 2, 3), default=1)
    args = parser.parse_args()
    selfcheck()
    previous, manifest = setup()
    assert args.hubs != bool(args.seeds), 'Choose hubs or seeds.'
    if args.hubs:
        make_hubs(manifest)
    else:
        trace(args.seeds, args.depth, previous, manifest)
