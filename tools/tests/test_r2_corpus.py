"""R2 corpus/index verifier tests against small synthetic outputs, never Ghidra execution."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('r2_corpus', Path(__file__).resolve().parents[1] / 'r2_corpus.py')
r2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r2)

ENTRIES = ['0x1000', '0x1010', '0x1020']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def record(entry, state='exported', code='void f(void) {}\n'):
    data = None if code is None else code.encode()
    return {'entry': entry, 'name': 'f', 'state': state, 'error': None if state != 'failed' else 'Timed out after 60 s',
            'timed_out': state == 'failed', 'partial_code': False, 'warnings': [], 'ms': 1,
            'code_bytes': None if data is None else len(data), 'code_sha256': None if data is None else sha(data), 'code': code}


class CorpusCheckTests(unittest.TestCase):
    """Three eligible functions in chunks of two: chunk 0 holds two records, chunk 1 one."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'chunks').mkdir()
        run = {'eligible': 3, 'chunk_size': 2, 'chunk_count': 2,
               'eligible_keys_sha256': sha(''.join(e + '\n' for e in ENTRIES).encode())}
        (self.root / 'run.json').write_text(json.dumps(run))

    def tearDown(self):
        self.tmp.cleanup()

    def write_chunk(self, k, records):
        (self.root / 'chunks' / f'chunk-{k:05d}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))

    def write_coverage(self, counts):
        coverage = {'run_sha256': sha((self.root / 'run.json').read_bytes()), 'counts': counts}
        (self.root / 'coverage.json').write_text(json.dumps(coverage))

    def complete(self):
        self.write_chunk(0, [record(ENTRIES[0]), record(ENTRIES[1], 'failed', None)])
        self.write_chunk(1, [record(ENTRIES[2])])
        self.write_coverage({'exported': 2, 'exported-with-warnings': 0, 'failed': 1, 'pending': 0})

    def test_complete_corpus_counts_sum_to_eligible(self):
        self.complete()
        self.assertEqual(r2.check_corpus(self.root)['counts'], {'exported': 2, 'failed': 1})

    def test_missing_chunk_is_pending_not_success(self):
        self.write_chunk(0, [record(ENTRIES[0]), record(ENTRIES[1])])
        self.write_coverage({'exported': 2, 'pending': 1})
        self.assertEqual(r2.check_corpus(self.root)['counts'], {'exported': 2, 'pending': 1})

    def test_changed_code_bytes_are_rejected(self):
        self.complete()
        changed = record(ENTRIES[2])
        changed['code'] = 'void g(void) {}\n'
        self.write_chunk(1, [changed])
        with self.assertRaisesRegex(r2.CheckError, 'code_sha256 mismatch'):
            r2.check_corpus(self.root)

    def test_failure_without_error_is_rejected(self):
        self.complete()
        failed = record(ENTRIES[2], 'failed', None)
        failed['error'] = None
        self.write_chunk(1, [failed])
        with self.assertRaisesRegex(r2.CheckError, 'failure without error'):
            r2.check_corpus(self.root)

    def test_stale_coverage_is_rejected(self):
        self.complete()
        self.write_coverage({'exported': 2, 'pending': 1})
        with self.assertRaisesRegex(r2.CheckError, 'disagrees'):
            r2.check_corpus(self.root)

    def test_entries_differing_from_pinned_list_are_rejected(self):
        self.complete()
        self.write_chunk(1, [record('0x1030')])
        with self.assertRaisesRegex(r2.CheckError, 'pinned eligible list'):
            r2.check_corpus(self.root)

    def test_short_chunk_is_rejected(self):
        self.complete()
        self.write_chunk(0, [record(ENTRIES[0])])
        with self.assertRaisesRegex(r2.CheckError, '1 records, expected 2'):
            r2.check_corpus(self.root)

    def test_unexpected_file_is_rejected(self):
        self.complete()
        (self.root / 'chunks' / 'notes.txt').write_text('x')
        with self.assertRaisesRegex(r2.CheckError, 'Unexpected files'):
            r2.check_corpus(self.root)


class IndexCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        data = b'{"caller":"0x1000"}\n{"caller":"0x1010"}\n'
        (self.root / 'calls.jsonl').write_bytes(data)
        manifest = {'files': {'calls.jsonl': {'lines': 2, 'bytes': len(data), 'sha256': sha(data)}}}
        (self.root / 'manifest.json').write_text(json.dumps(manifest))

    def tearDown(self):
        self.tmp.cleanup()

    def test_matching_manifest_passes(self):
        self.assertEqual(r2.check_indexes(self.root), {'calls.jsonl': 2})

    def test_modified_index_is_rejected(self):
        (self.root / 'calls.jsonl').write_bytes(b'{"caller":"0x1000"}\n{"caller":"0x1011"}\n')
        with self.assertRaisesRegex(r2.CheckError, 'calls.jsonl'):
            r2.check_indexes(self.root)


if __name__ == '__main__':
    unittest.main()
