"""Sealed declared-starts navigation tests; no binary or native-tool execution."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import function_starts_browser as browser


class FunctionStartsBrowserTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.capture = Path(self.tmp.name) / 'function-starts-v1'
        self.capture.mkdir()
        (self.capture / browser.METHOD).write_text('fixture method')
        (self.capture / 'addresses.tsv').write_text('address\tfile_offset\tsegment\tuleb_file_offset\n0x1000\t0x0\t__TEXT\t0x100\n0x1004\t0x4\t__TEXT\t0x101\n')
        self.summary = {'schema': 'macho-linker-function-starts-v1', 'target_sha256': browser.TARGET,
                        'architecture': 'arm64', 'source': 'LC_FUNCTION_STARTS', 'status': 'present',
                        'method_sha256': browser.digest(self.capture / browser.METHOD), 'declared_start_count': 2,
                        'first_address': '0x1000', 'last_address': '0x1004'}
        self.write()

    def tearDown(self):
        self.tmp.cleanup()

    def seal(self):
        manifest = {p.name: {'sha256': browser.digest(p), 'bytes': p.stat().st_size} for p in self.capture.iterdir() if p.name != 'manifest.json'}
        (self.capture / 'manifest.json').write_text(json.dumps(manifest))

    def write(self):
        (self.capture / 'summary.json').write_text(json.dumps(self.summary))
        self.seal()

    def project(self):
        return browser.project(self.capture, str)

    def test_valid_count_links_and_no_embedded_rows(self):
        view, inputs = self.project()
        self.assertEqual(view['state'], 'sealed')
        self.assertEqual(view['count'], 2)
        self.assertNotIn('rows', view)
        self.assertEqual(len(inputs), 4)
        self.assertTrue(all(Path(url).is_file() for _, url in view['links']))

    def test_absent_command_has_no_table_link(self):
        (self.capture / 'addresses.tsv').unlink()
        self.summary.update(status='absent', declared_start_count=0, first_address=None, last_address=None)
        self.write()
        view, inputs = self.project()
        self.assertEqual(view['state'], 'sealed')
        self.assertEqual(view['count'], 0)
        self.assertEqual(len(inputs), 3)
        self.assertTrue(all('TSV' not in label for label, _ in view['links']))

    def test_tamper_extra_file_and_unsealed_block_publication(self):
        (self.capture / browser.METHOD).write_text('tampered method')
        self.assertEqual(self.project()[0]['state'], 'invalid')
        self.seal()
        (self.capture / 'unexpected').write_text('unsealed')
        self.assertEqual(self.project()[0]['state'], 'invalid')
        (self.capture / 'manifest.json').unlink()
        self.assertEqual(self.project()[0]['state'], 'unsealed')

    def test_summary_identity_count_and_table_order_mismatch(self):
        for key, bad in [('target_sha256', 'a' * 64), ('method_sha256', 'b' * 64), ('declared_start_count', 3), ('first_address', '0x999'), ('status', 'absent')]:
            original = self.summary[key]
            self.summary[key] = bad
            self.write()
            view, inputs = self.project()
            self.assertEqual(view['state'], 'invalid')
            self.assertNotIn('links', view)
            self.assertEqual(inputs, [])
            self.summary[key] = original
        table = self.capture / 'addresses.tsv'
        table.write_text(table.read_text().replace('0x1004', '0x1000'))
        self.write()
        self.assertEqual(self.project()[0]['state'], 'invalid')

    def test_manifest_symlink_and_payload_symlink_rejected(self):
        manifest = self.capture / 'manifest.json'
        outside = self.capture.parent / 'manifest-copy.json'
        outside.write_bytes(manifest.read_bytes())
        manifest.unlink()
        manifest.symlink_to(outside)
        self.assertEqual(self.project()[0]['state'], 'invalid')
        manifest.unlink()
        manifest.write_bytes(outside.read_bytes())
        table = self.capture / 'addresses.tsv'
        copy = self.capture.parent / 'table.tsv'
        copy.write_bytes(table.read_bytes())
        table.unlink()
        table.symlink_to(copy)
        self.assertEqual(self.project()[0]['state'], 'invalid')

    def test_missing_capture_is_optional(self):
        self.assertEqual(browser.project(self.capture / 'not-present', str), (None, []))


if __name__ == '__main__':
    unittest.main()
