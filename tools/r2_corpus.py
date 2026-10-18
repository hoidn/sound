#!/usr/bin/env python3
"""Analyst-only verifier for R2BulkDecompile corpora and R2ExportIndexes outputs.

Reads files only; never runs Ghidra or edits evidence. `corpus` recomputes per-state counts
from every committed chunk, checks code hashes and that coverage.json agrees; once every chunk
is committed it also checks the entries against the pinned eligible-list digest. `indexes`
checks each file's line count, byte count and SHA-256 against manifest.json and parses every line.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

STATES = {'exported', 'exported-with-warnings', 'failed'}


class CheckError(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def record_problem(record):
    """Same per-record rules as R2BulkDecompile.recordProblem; None when the record is valid."""
    state, code = record['state'], record['code']
    if state not in STATES:
        return f'unknown state {state}'
    if state.startswith('exported') and (code is None or record['partial_code']):
        return 'exported without complete code'
    if state == 'failed' and record['error'] is None:
        return 'failure without error'
    if code is None:
        return None if record['code_sha256'] is None and record['code_bytes'] is None else 'hash without code'
    data = code.encode('utf-8')
    if len(data) != record['code_bytes']:
        return 'code_bytes mismatch'
    return None if sha(data) == record['code_sha256'] else 'code_sha256 mismatch'


def chunk_records(path, expected):
    data = path.read_bytes()
    if data and not data.endswith(b'\n'):
        raise CheckError(f'{path}: missing final newline')
    records = [json.loads(line) for line in data.split(b'\n')[:-1]]
    if len(records) != expected:
        raise CheckError(f'{path}: {len(records)} records, expected {expected}')
    for number, record in enumerate(records, 1):
        problem = record_problem(record)
        if problem:
            raise CheckError(f'{path} line {number}: {problem}')
    return records


def check_corpus(root):
    run_bytes = (root / 'run.json').read_bytes()
    run = json.loads(run_bytes)
    size, count, eligible = run['chunk_size'], run['chunk_count'], run['eligible']
    names = [f'chunk-{k:05d}.jsonl' for k in range(count)]
    present = {p.name for p in (root / 'chunks').iterdir()}
    temporary = sorted(n for n in present if n.startswith('.') and n.endswith('.tmp'))
    unexpected = present - set(names) - set(temporary)
    if unexpected:
        raise CheckError(f'Unexpected files in chunks/: {sorted(unexpected)}')
    counts, entries = Counter(), []
    for k, name in enumerate(names):
        expected = min(size, eligible - k * size)
        if name not in present:
            counts['pending'] += expected
            continue
        for record in chunk_records(root / 'chunks' / name, expected):
            counts[record['state']] += 1
            entries.append(record['entry'])
    if len(set(entries)) != len(entries):
        raise CheckError('An entry appears in more than one record')
    if sum(counts.values()) != eligible:
        raise CheckError(f'Counts sum to {sum(counts.values())}, eligible {eligible}')
    complete = counts['pending'] == 0
    if complete and sha(''.join(e + '\n' for e in entries).encode()) != run['eligible_keys_sha256']:
        raise CheckError('Committed entries differ from the pinned eligible list')
    coverage = json.loads((root / 'coverage.json').read_bytes())
    if coverage['run_sha256'] != sha(run_bytes):
        raise CheckError('coverage.json belongs to a different run.json')
    if {k: v for k, v in coverage['counts'].items() if v} != dict(counts):
        raise CheckError('coverage.json disagrees with committed chunks; rerun R2BulkDecompile to regenerate it')
    return {'eligible': eligible, 'counts': dict(sorted(counts.items())), 'complete': complete,
            'stale_temporary_files': temporary}


def check_indexes(root):
    manifest = json.loads((root / 'manifest.json').read_bytes())
    result = {}
    for name, expected in sorted(manifest['files'].items()):
        digest, lines, size = hashlib.sha256(), 0, 0
        with (root / name).open('rb') as stream:
            for line in stream:
                digest.update(line)
                lines += line.endswith(b'\n')
                size += len(line)
                json.loads(line)
        actual = {'lines': lines, 'bytes': size, 'sha256': digest.hexdigest()}
        if actual != expected:
            raise CheckError(f'{name}: manifest {expected}, actual {actual}')
        result[name] = lines
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('kind', choices=['corpus', 'indexes'])
    parser.add_argument('root', type=Path)
    args = parser.parse_args(argv)
    try:
        result = check_corpus(args.root) if args.kind == 'corpus' else check_indexes(args.root)
    except (CheckError, OSError, KeyError, ValueError) as failure:
        print(f'FAIL {args.kind} {args.root}: {failure}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
