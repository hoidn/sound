"""R2 corpus browser tests against small synthetic corpora and indexes, never Ghidra execution."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import r2_browser
import r2_corpus

HOSTILE = '</script><img src=x onerror=alert(1)>'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def record(entry, name, code='void f(void) {}\n', state='exported'):
    data = code.encode()
    return {'entry': entry, 'name': name, 'thunk': False, 'body_bytes': 4, 'body_ranges': [[entry, entry]],
            'signature': 'void f(void)', 'state': state, 'error': None, 'timed_out': False, 'partial_code': False,
            'warnings': [], 'ms': 1, 'code_bytes': len(data), 'code_sha256': sha(data), 'code': code}


class BrowserBuildTests(unittest.TestCase):
    """Three eligible functions in chunks of two; 0x1000 calls 0x1010 and references a string."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.corpus, self.indexes, self.out = base / 'corpus', base / 'indexes', base / 'browse'
        self.records = [record('0x1000', 'caller', HOSTILE), record('0x1010', 'callee'), record('0x1020', 'alone')]
        self.write_corpus(self.records, committed=(0, 1))
        self.write_indexes('prog')

    def tearDown(self):
        self.tmp.cleanup()

    def write_corpus(self, records, committed):
        (self.corpus / 'chunks').mkdir(parents=True, exist_ok=True)
        run = {'program': 'prog', 'executable_sha256': 'a' * 64, 'language': 'AARCH64', 'ghidra_version': '12.1.4',
               'eligible': 3, 'chunk_size': 2, 'chunk_count': 2,
               'eligible_keys_sha256': sha(''.join(r['entry'] + '\n' for r in records).encode())}
        run_bytes = json.dumps(run).encode()
        (self.corpus / 'run.json').write_bytes(run_bytes)
        counts = {'exported': 0, 'pending': 0}
        for k in (0, 1):
            chunk = records[2 * k:2 * k + 2]
            if k in committed:
                (self.corpus / 'chunks' / f'chunk-{k:05d}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in chunk))
                counts['exported'] += len(chunk)
            else:
                (self.corpus / 'chunks' / f'chunk-{k:05d}.jsonl').unlink(missing_ok=True)
                counts['pending'] += len(chunk)
        (self.corpus / 'coverage.json').write_text(json.dumps({'run_sha256': sha(run_bytes), 'counts': counts}))

    def write_indexes(self, program):
        self.indexes.mkdir(exist_ok=True)
        content = {
            'calls.jsonl': [{'caller': '0x1000', 'caller_name': 'caller', 'site': '0x1004', 'kind': 'call', 'callee': '0x1010',
                             'callee_name': 'callee', 'callee_resolved': None, 'callee_resolved_name': None}],
            'strings.jsonl': [{'address': '0x9000', 'value': HOSTILE, 'refs': [{'from': '0x1008', 'function': '0x1000'}]}],
            'indirect.jsonl': [{'function': '0x1010', 'site': '0x1014', 'instruction': 'blr x8', 'resolved_targets': []}],
            'vtables.jsonl': [],
            'aliases.jsonl': [{'entry': e, 'name': n, 'symbols': [{'name': n}, {'name': n + '_alias'}]}
                              for e, n in (('0x1000', 'caller'), ('0x1010', 'callee'), ('0x1020', 'alone'))],
        }
        files = {}
        for name, rows in content.items():
            data = ''.join(json.dumps(r) + '\n' for r in rows).encode()
            (self.indexes / name).write_bytes(data)
            files[name] = {'lines': len(rows), 'bytes': len(data), 'sha256': sha(data)}
        (self.indexes / 'manifest.json').write_text(json.dumps({'program': program, 'executable_sha256': 'a' * 64, 'files': files}))

    def build(self):
        return r2_browser.build(self.corpus, self.indexes, self.out, 'Test corpus')

    def chunk(self, k):
        text = (self.out / 'chunks' / f'chunk-{k:05d}.js').read_text()
        return json.loads(text.split('=', 2)[2].rstrip(';\n'))

    def test_relations_land_on_both_ends(self):
        self.build()
        caller, callee = self.chunk(0)
        self.assertEqual(caller['callees']['items'], [['0x1004', '0x1010', 'callee', 'call', None]])
        self.assertEqual(callee['callers']['items'], [['0x1004', '0x1000', 'caller', 'call']])
        self.assertEqual(caller['strings']['items'][0][2], HOSTILE)
        self.assertEqual(callee['indirect']['total'], 1)

    def test_catalog_lists_browser(self):
        self.build()
        catalog = (self.out.parent / 'r2-index.html').read_text()
        self.assertIn('href="browse/index.html">Test corpus</a>', catalog)

    def test_hostile_text_never_appears_raw(self):
        self.build()
        for path in self.out.rglob('*'):
            if path.is_file():
                self.assertNotIn('<img', path.read_text(), path.name)

    def test_tampered_corpus_writes_nothing(self):
        bad = dict(self.records[0], code='changed')
        (self.corpus / 'chunks' / 'chunk-00000.jsonl').write_text(json.dumps(bad) + '\n' + json.dumps(self.records[1]) + '\n')
        with self.assertRaises(r2_corpus.CheckError):
            self.build()
        self.assertFalse(self.out.exists())

    def test_indexes_for_another_program_rejected(self):
        self.write_indexes('other')
        with self.assertRaises(r2_corpus.CheckError):
            self.build()

    def test_refuses_to_replace_unrelated_directory(self):
        self.out.mkdir()
        (self.out / 'notes.txt').write_text('keep')
        with self.assertRaises(r2_corpus.CheckError):
            self.build()
        self.assertEqual((self.out / 'notes.txt').read_text(), 'keep')

    def test_pending_chunk_is_not_listed_and_rebuild_is_identical(self):
        self.write_corpus(self.records, committed=(0,))
        first = self.build()
        rows = json.loads((self.out / 'functions.js').read_text()[len('window.r2Index='):-2])
        self.assertEqual([r[0] for r in rows], ['0x1000', '0x1010'])
        self.assertIn('1 eligible functions are in chunks not yet committed', (self.out / 'index.html').read_text())
        self.assertFalse((self.out / 'chunks' / 'chunk-00001.js').exists())
        self.assertEqual(self.build(), first)


if __name__ == '__main__':
    unittest.main()
