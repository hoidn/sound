"""Custom selected-capture publication tests; no Ghidra or target execution."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import selected_browser as browser


class SelectedBrowserTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.run = self.base / 'native-live-arm64-targeted-v1'
        self.function = self.run / 'functions/0x1000'
        self.function.mkdir(parents=True)
        (self.run / 'method').mkdir()
        (self.run / 'method/SelectedNativeExport.java').write_text('fixture method')
        method = browser.digest(self.run / 'method/SelectedNativeExport.java')
        seed = {'address': '0x1000', 'window_bytes': 4096, 'label': '<unsafe> symbol', 'source': 'synthetic fixture'}
        self.settings = {'schema': 1, 'target_sha256': browser.TARGET, 'architecture': 'arm64',
                         'profile': browser.PROFILE, 'auto_analysis': False, 'incremental_code_analysis': False,
                         'method_sha256': method, 'ghidra_version': '12.1.4', 'seeds': [seed]}
        self.status = {'executed': True, 'profile': browser.PROFILE, 'exit_code': 0,
                       'cleanup': {'cleaned': True, 'survivors': []},
                       'items': [{'address': '0x1000', 'state': 'exported', 'error': None}]}
        self.metadata = {'schema': 1, 'target_sha256': browser.TARGET, 'provider': 'ghidra-headless-selected-script',
                         'profile': browser.PROFILE, 'method_sha256': method, 'ghidra_version': '12.1.4',
                         'seed': seed, 'address': '0x1000', 'state': 'exported',
                         'body_ranges': [{'start': '0x1000', 'end': '0x1003'}], 'body_bytes': 4, 'instruction_count': 1}
        (self.function / 'pseudocode.c').write_text('void fixture(void) {}')
        (self.function / 'assembly.txt').write_text('0x1000 ret')
        self.write()

    def tearDown(self):
        self.tmp.cleanup()

    def seal(self):
        manifest = {p.relative_to(self.run).as_posix(): browser.digest(p) for p in self.run.rglob('*') if p.is_file() and p.name != 'manifest.json'}
        (self.run / 'manifest.json').write_text(json.dumps(manifest))

    def write(self):
        (self.run / 'run.json').write_text(json.dumps(self.settings))
        (self.run / 'run-status.json').write_text(json.dumps(self.status))
        (self.function / 'metadata.json').write_text(json.dumps(self.metadata))
        self.seal()

    def project(self):
        return browser.project(self.base, str)

    def test_valid_sealed_capture_has_raw_artifact_links(self):
        runs, inputs = self.project()
        self.assertEqual(runs[0]['state'], 'sealed')
        self.assertEqual(runs[0]['successful'], 1)
        self.assertEqual(runs[0]['rows'][0]['label'], '<unsafe> symbol')
        self.assertEqual(len(runs[0]['rows'][0]['links']), 3)
        self.assertTrue(all(Path(url).is_file() for _, url in runs[0]['rows'][0]['links']))
        self.assertIn(self.run / 'manifest.json', inputs)

    def test_tamper_and_unlisted_payload_block_code_publication(self):
        (self.function / 'pseudocode.c').write_text('changed')
        self.assertEqual(self.project()[0][0]['state'], 'invalid')
        self.seal()
        (self.run / 'unexpected.txt').write_text('unsealed')
        run = self.project()[0][0]
        self.assertEqual(run['state'], 'invalid')
        self.assertEqual(run['rows'], [])
        self.assertEqual(run['successful'], 0)

    def test_unsealed_or_unclean_run_never_publishes_code(self):
        (self.run / 'manifest.json').unlink()
        self.assertEqual(self.project()[0][0]['state'], 'unsealed')
        self.status['cleanup'] = {'cleaned': False, 'survivors': [12345]}
        self.write()
        self.assertEqual(self.project()[0][0]['state'], 'invalid')

    def test_failed_partial_artifacts_are_visible_but_not_successful(self):
        self.metadata.update(state='failed', error='bounded export failed')
        self.status['items'][0].update(state='failed', error='bounded export failed')
        self.write()
        run = self.project()[0][0]
        self.assertEqual(run['state'], 'sealed')
        self.assertEqual(run['successful'], 0)
        self.assertEqual(run['counts'], {'failed': 1})
        self.assertEqual(run['rows'][0]['links'][0][0], 'Pseudocode (partial; failed)')

    def test_missing_and_invalid_attempts_have_no_function_links(self):
        self.status['items'][0].update(state='missing', error='not attempted before stop')
        (self.function / 'metadata.json').unlink()
        (self.run / 'run-status.json').write_text(json.dumps(self.status))
        self.seal()
        run = self.project()[0][0]
        self.assertEqual(run['state'], 'sealed')
        self.assertEqual(run['rows'][0]['links'], [])
        self.status['items'][0].update(state='invalid', error='bad output metadata')
        self.write()
        self.assertEqual(self.project()[0][0]['rows'][0]['links'], [])

    def test_identity_and_outcome_mismatch_block_publication(self):
        for field, value in [('target_sha256', 'a' * 64), ('profile', 'different-profile'), ('seed', {})]:
            original = self.metadata[field]
            self.metadata[field] = value
            self.write()
            self.assertEqual(self.project()[0][0]['state'], 'invalid')
            self.metadata[field] = original
        self.status['items'][0]['state'] = 'failed'
        self.write()
        self.assertEqual(self.project()[0][0]['state'], 'invalid')

    def test_unsafe_manifest_path_or_symlink_is_rejected(self):
        outside = self.base / 'outside'
        outside.write_text('untrusted')
        (self.run / 'manifest.json').write_text(json.dumps({'../outside': browser.digest(outside)}))
        self.assertEqual(self.project()[0][0]['state'], 'invalid')
        code = self.function / 'pseudocode.c'
        code.unlink()
        code.symlink_to(outside)
        self.seal()
        self.assertEqual(self.project()[0][0]['state'], 'invalid')

    def test_manifest_symlink_is_rejected(self):
        manifest = self.run / 'manifest.json'
        outside = self.base / 'outside-manifest.json'
        outside.write_bytes(manifest.read_bytes())
        manifest.unlink()
        manifest.symlink_to(outside)
        run = self.project()[0][0]
        self.assertEqual(run['state'], 'invalid')
        self.assertEqual(run['rows'], [])

    def test_success_requires_nonempty_code_and_body(self):
        self.metadata['instruction_count'] = 0
        self.write()
        self.assertEqual(self.project()[0][0]['state'], 'invalid')
        self.metadata['instruction_count'] = 1
        (self.function / 'pseudocode.c').write_text('')
        self.write()
        self.assertEqual(self.project()[0][0]['state'], 'invalid')

    @unittest.skipUnless(shutil.which('node'), 'Node is unavailable')
    def test_selected_search_javascript_with_dom_stub(self):
        prelude = r'''
const assert = require('node:assert/strict');
const input = {value:'', addEventListener(type, handler) {this.handler = handler;}};
const count = {textContent:''};
const rows = [{dataset:{selectedSearch:'v1 0x1000 aloopon exported'}}, {dataset:{selectedSearch:'v2 0x2000 other failed'}}];
global.document = {getElementById(id) {return id==='selected-search'?input:count;}, querySelectorAll() {return rows;}};
'''
        assertions = r'''
assert.equal(count.textContent,'2 of 2 selected outcomes');
input.value='ALOOPON 0x1000'; input.handler();
assert.equal(rows[0].hidden,false); assert.equal(rows[1].hidden,true);
input.value='failed'; input.handler(); assert.equal(rows[1].hidden,false);
input.value='absent'; input.handler(); assert.equal(count.textContent,'0 of 2 selected outcomes');
'''
        result = subprocess.run([shutil.which('node'), '-e', prelude + browser.SCRIPT + assertions], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
