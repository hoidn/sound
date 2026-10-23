"""Read-only retained text/byte identities; never executes decompiled/source code."""
import argparse
import ast
from collections import defaultdict
import copy
import hashlib
import json
import mmap
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def load(path):
    return json.loads(path.read_text())


def digest(path):
    with path.open('rb') as stream:
        return {'bytes': path.stat().st_size, 'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def guards(context, functions, words):
    assert len(functions) == len({r['entry'] for r in functions}) == 16
    assert context['read_scope']['complete_bodies_read'] == 16
    assert context['read_scope']['metadata_only_functions'] == 0
    assert context['source_identity']['source_export_UTC'] is None
    for key in ['UI_kernel_link_established', 'public_grid_bound_established', 'Q053_resolved', 'executed']:
        assert context[key] is False, 'unsupported promoted source/mechanism result'
    for key in ['new_requirements', 'new_cases', 'behavioral_coverage_credit', 'complete_topics']:
        assert context[key] == 0
    assert context['actual_expected'] is context['actual_comparison'] is None and context['target'] == 'U'
    for key in ['class_boundary_established', 'callable_ABI_established', 'actual_dispatch_established']:
        assert words[key] is False
    assert len(words['words']) == 64 and words['words'][50] == '0x10341c29c'
    for item in functions:
        row = item['record']
        assert row['state'] in ['exported', 'exported-with-warnings'] and not row['partial_code']
        code = row['code'].encode()
        assert len(code) == row['code_bytes'] and hashlib.sha256(code).hexdigest() == row['code_sha256']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    pins = load(HERE / 'source-pins.json')
    assert len(pins) == 15
    for pin in pins:
        assert digest(ROOT / pin['path']) == {k: pin[k] for k in ['bytes', 'sha256']}, pin['path']
    context, functions, words = (load(HERE / name) for name in ['context.json', 'functions.json', 'pointer-words.json'])
    guards(context, functions, words)
    indices, calls = load(HERE / 'index-records.json'), load(HERE / 'calls.json')
    assert len(indices) == 73 and sum(r['selected_semantic_context'] for r in indices) == 11
    assert len(calls) == 7
    records = defaultdict(list)
    for row in functions + indices + calls:
        records[row['parent']].append(row)
    lexical_matches = []
    for name, wanted in records.items():
        by_line = {r['line']: r for r in wanted}
        assert len(by_line) == len(wanted)
        found = set()
        with Path(name).open('rb') as stream:
            for number, raw in enumerate(stream, 1):
                if name.endswith(('/aliases.jsonl', '/strings.jsonl')) and b'humaniz' in raw.lower():
                    lexical_matches.append((name, number))
                if number not in by_line:
                    continue
                row = by_line[number]
                hash_key = 'raw_line_sha256' if 'raw_line_sha256' in row else 'raw_record_sha256'
                assert hashlib.sha256(raw).hexdigest() == row[hash_key]
                assert json.loads(raw) == row['record']
                found.add(number)
        assert found == set(by_line)
    assert set(lexical_matches) == {(r['parent'], r['line']) for r in indices}
    for row in calls:
        assert row['record']['caller'] in {f['entry'] for f in functions}
        assert row['record']['callee'] in {f['entry'] for f in functions}
    manifest = next(p for p in pins if p['path'].endswith('/indexes/manifest.json'))
    run = next(p for p in pins if p['path'].endswith('/decomp/run.json'))
    target = context['source_identity']['binary_sha256']
    assert load(ROOT / manifest['path'])['executable_sha256'] == load(ROOT / run['path'])['executable_sha256'] == target == words['sha256']
    # Three inspected pure header functions only; never call the extractor/write path.
    tree = ast.parse((ROOT / 'tools/index_macho_function_starts.py').read_text())
    functions_ast = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'require', 'span', 'header'}]
    assert len(functions_ast) == 3
    env = {'struct': struct, 'U64': (1 << 64) - 1}
    exec(compile(ast.Module(body=functions_ast, type_ignores=[]), 'our-pure-MachO-header', 'exec'), env)
    with (ROOT / words['parent_binary']).open('rb') as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        info = env['header'](data)
        assert info['segments'] == words['segments']
        address = int(words['address'], 16)
        segment = next(s for s in info['segments'] if s['vmaddr'] <= address and address + 512 <= s['vmaddr'] + s['filesize'])
        offset = segment['fileoff'] + address - segment['vmaddr']
        assert offset == int(words['file_offset'], 16)
        raw = data[offset:offset + 512]
        assert raw.hex() == words['raw_hex'] and [hex(x) for x in struct.unpack('<64Q', raw)] == words['words']
    for selected in context['documentary_context']:
        document = load(ROOT / selected['catalog'])
        for pin in document['immutable_inputs']:
            assert digest(ROOT / pin['path']) == {k: pin[k] for k in ['bytes', 'sha256']}
        value = document
        for key in selected['json_pointer'].split('/')[1:]:
            value = value[int(key)] if isinstance(value, list) else value[key]
        assert value == selected['row']
    rejected = []
    for name in ['invent-link', 'resolve-grid', 'invent-UTC', 'infer-table-boundary', 'alter-code']:
        c, f, w = copy.deepcopy((context, functions, words))
        if name == 'invent-link':
            c['UI_kernel_link_established'] = True
        elif name == 'resolve-grid':
            c['Q053_resolved'] = True
        elif name == 'invent-UTC':
            c['source_identity']['source_export_UTC'] = c['queried_utc']
        elif name == 'infer-table-boundary':
            w['class_boundary_established'] = True
        else:
            f[0]['record']['code'] += 'altered'
        try:
            guards(c, f, w)
        except AssertionError:
            rejected.append(name)
            continue
        raise AssertionError('unsafe promotion accepted: ' + name)
    seal = HERE / 'manifest.json'
    if seal.exists():
        mf = load(seal)
        assert {q.name for q in HERE.iterdir() if q.is_file() and q != seal} == {r['file'] for r in mf['payloads']}
        for pin in mf['payloads']:
            assert digest(HERE / pin['file']) == {k: pin[k] for k in ['bytes', 'sha256']}
    for path in HERE.iterdir():
        if path.is_file():
            raw = path.read_bytes()
            assert raw.endswith(b'\n') and not any(line.rstrip(b' \t') != line for line in raw.splitlines()), path
    print(json.dumps({'status': 'pass', 'sealed': seal.exists(), 'mode': 'read-only-static-data', 'functions': 16, 'complete_bodies_read': 16, 'lexical_index_hits': 73, 'selected_relevant_indices': 11, 'direct_call_records': 7, 'literal_pointer_words': 64, 'direct_parent_pins': 15, 'negative_fixtures': rejected, 'Q053_resolved': False, 'new_requirements': 0, 'new_cases': 0, 'coverage_credit': 0, 'actual_nonnull': 0, 'executed': 0, 'complete_topics': 0}))


if __name__ == '__main__':
    main()
