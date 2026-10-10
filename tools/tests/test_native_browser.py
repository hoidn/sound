"""Navigation projection tests using actual exporter schema, not native tools."""
import importlib.util
import json
from pathlib import Path
import sys
import shutil
import subprocess
from unittest.mock import patch
import fcntl
import tempfile
import unittest
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import native_browser as browser
import export_native_corpus as exporter
import build_artifact_browser as generator
from test_native_export import record, row, TARGET


class BrowserTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'corpus'
        self.root.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def initialize(self):
        source = self.root.parent / 'inventory.json'
        source.write_bytes(exporter.encoded(record('list_procedures', [row(name='<script>alert(1)</script>'), row('0x2000', 'pending')], 1)))
        exporter.initialize(self.root, source, TARGET, 'arm64')

    def test_absent_inventory_is_unknown(self):
        self.assertEqual(browser.project(self.root, str), (None, [], []))

    def test_initial_index_has_only_retained_attempts_and_full_index_is_separate(self):
        rows = [['0x1', ['pending'], 'pending', 0, []],
                ['0x2', ['has code'], 'exported', 1, [['Pseudocode', 'code.c']]],
                ['0x3', ['failed'], 'failed', 1, [['Metadata', 'meta.json']]],
                ['EXTERNAL:0x1', ['external'], 'external', 0, []]]
        scripts = browser.index_scripts(rows)
        initial = json.loads(scripts['native-index.js'][len('window.nativeRows='):-2])
        full = json.loads(scripts['native-inventory.js'][len('window.nativeInventoryRows='):-2])
        self.assertEqual(initial, rows[1:3])
        self.assertEqual(full, rows)
        self.assertNotIn('nativeInventoryRows', scripts['native-index.js'])
        with self.assertRaises(ValueError):
            browser.data_script(rows, 'unsafe;code')

    def test_generator_holds_exporter_lock_through_publication(self):
        def publication():
            with (self.root / 'native-live-arm64-v1/.ingest.lock').open('a') as other:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return {'locked': True}
        with patch.object(generator, 'ARTIFACTS', self.root), patch.object(generator, '_build', publication):
            self.assertEqual(generator.build(), {'locked': True})

    def test_pending_and_export_links_from_actual_schema(self):
        self.initialize()
        source = self.root.parent / 'code.json'
        source.write_bytes(exporter.encoded(record('procedure_pseudo_code', '/* WARNING unresolved */\nvoid f() {}', 2)))
        exporter.ingest(self.root, source)
        summary, rows, inputs = browser.project(self.root, str)
        self.assertEqual(summary['successful'], 1)
        self.assertEqual(rows[0][2], 'exported-with-warnings')
        self.assertEqual(rows[1][2], 'pending')
        self.assertEqual(rows[1][4], [])
        self.assertEqual(len(rows[0][4]), 3)
        self.assertTrue(all(Path(href).is_file() for _, href in rows[0][4]))
        script = browser.data_script(rows)
        self.assertNotIn('<script>', script)
        self.assertNotIn('void f()', script)
        self.assertEqual(json.loads(script[len('window.nativeRows='):-2]), rows)

    def test_failed_partial_never_labeled_success(self):
        self.initialize()
        source = self.root.parent / 'failed.json'
        source.write_bytes(exporter.encoded(record('batch_decompile', {'items': [{'address': '0x1000', 'status': 'error', 'pseudocode': 'partial', 'error': {'message': 'timeout'}}]}, 3)))
        exporter.ingest(self.root, source)
        summary, rows, _ = browser.project(self.root, str)
        self.assertEqual(summary['successful'], 0)
        self.assertEqual(rows[0][2], 'failed')
        self.assertEqual(rows[0][4][0][0], 'Partial code (failed)')

    def test_invalid_paths_and_counts_rejected(self):
        self.initialize()
        path = self.root / 'coverage.json'
        original = json.loads(path.read_text())
        bad = dict(original, unique_functions=999)
        path.write_text(json.dumps(bad))
        with self.assertRaises(ValueError):
            browser.project(self.root, str)
        original['functions'][0]['revisions'] = ['../../elsewhere']
        path.write_text(json.dumps(original))
        with self.assertRaises(ValueError):
            browser.project(self.root, str)

    def test_missing_success_code_rejected(self):
        self.initialize()
        source = self.root.parent / 'code.json'
        source.write_bytes(exporter.encoded(record('procedure_pseudo_code', 'void f() {}', 2)))
        exporter.ingest(self.root, source)
        next((self.root / 'functions').rglob('pseudocode.c')).unlink()
        with self.assertRaises(ValueError):
            browser.project(self.root, str)

    def test_classification_with_failed_attempt_stays_visible(self):
        source = self.root.parent / 'external-inventory.json'
        source.write_bytes(exporter.encoded(record('list_procedures', [row(external=True)], 1)))
        exporter.initialize(self.root, source, TARGET, 'arm64')
        attempt = self.root.parent / 'failed.json'
        attempt.write_bytes(exporter.encoded(record('procedure_pseudo_code', None, 2)))
        exporter.ingest(self.root, attempt)
        summary, rows, _ = browser.project(self.root, str)
        self.assertEqual(rows[0][2], 'external')
        self.assertEqual(len(rows[0][4]), 2)
        self.assertEqual(summary['successful'], 0)

    def test_qualified_external_address_preserves_identity_and_links(self):
        # Ghidra's named EXTERNAL address space is distinct from default memory.
        source = self.root.parent / 'external-space-inventory.json'
        source.write_bytes(exporter.encoded(record('list_procedures', [
            row('0x1', 'memory_one'),
            row('EXTERNAL:0x1', '_malloc', external=True),
            row('EXTERNAL%2Falias:0x1', 'encoded_space_fixture', external=True),
        ], 1)))
        exporter.initialize(self.root, source, TARGET, 'arm64')
        for number, space in enumerate(('EXTERNAL:0x1', 'EXTERNAL%2Falias:0x1'), 2):
            attempt = self.root.parent / f'external-failed-{number}.json'
            failure = record('procedure_pseudo_code', None, number)
            failure['parameters']['procedure'] = space
            attempt.write_bytes(exporter.encoded(failure))
            exporter.ingest(self.root, attempt)
        summary, rows, _ = browser.project(self.root, lambda p: quote(str(p), safe='/.-_'))
        by_address = {row[0]: row for row in rows}
        self.assertEqual(set(by_address), {'0x1', 'EXTERNAL:0x1', 'EXTERNAL%2Falias:0x1'})
        external = by_address['EXTERNAL:0x1']
        self.assertEqual(external[2], 'external')
        self.assertEqual(external[3], 1)
        self.assertIn('/EXTERNAL%3A0x1/', external[4][0][1])
        encoded_link = by_address['EXTERNAL%2Falias:0x1'][4][0][1]
        self.assertIn('/EXTERNAL%252Falias%3A0x1/', encoded_link)
        self.assertTrue(Path(unquote(encoded_link)).is_file())
        self.assertEqual(by_address['0x1'][2], 'pending')
        self.assertEqual(summary['eligible'], 1)
        self.assertEqual(summary['attempted'], 0)

    def test_success_without_revision_and_false_totals_rejected(self):
        self.initialize()
        path = self.root / 'coverage.json'
        original = json.loads(path.read_text())
        for key in ('successful', 'attempted', 'eligible'):
            bad = dict(original)
            bad[key] += 1
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                browser.project(self.root, str)
        original['functions'][0]['state'] = 'exported'
        original['counts'] = {'exported': 1, 'pending': 1}
        original['successful'] = 1
        path.write_text(json.dumps(original))
        with self.assertRaises(ValueError):
            browser.project(self.root, str)

    @unittest.skipUnless(shutil.which('node'), 'Node is unavailable')
    def test_javascript_pagination_and_filters_with_dom_stub(self):
        # Runs the shipped JS; this tests logic, not browser layout or accessibility.
        prelude = r'''
const assert = require('node:assert/strict');
function element() { return { children: [], value: '', textContent: '', handlers: {},
  append(...children) { this.children.push(...children); },
  replaceChildren() { this.children = []; },
  addEventListener(type, callback) { this.handlers[type] = callback; }
}; }
const ids = Object.fromEntries(['native-search','native-status','native-rows','native-count','native-prev','native-next'].map(id => [id, element()]));
global.document = {getElementById(id) { return ids[id]; }, createElement: element};
global.window = {nativeRows: Array.from({length: 205}, (_, i) => ['0x'+(4096+i).toString(16), ['symbol_'+i], i===204?'failed':'pending',0,[]])};
'''
        assertions = r'''
assert.equal(ids['native-rows'].children.length, 100);
ids['native-next'].handlers.click(); assert.equal(ids['native-rows'].children.length, 100);
ids['native-next'].handlers.click(); assert.equal(ids['native-rows'].children.length, 5);
assert.equal(ids['native-next'].disabled, true);
ids['native-status'].value='failed'; ids['native-status'].handlers.input();
assert.equal(ids['native-rows'].children.length, 1);
assert.equal(ids['native-rows'].children[0].children[1].textContent, 'symbol_204');
ids['native-search'].value='absent'; ids['native-search'].handlers.input();
assert.equal(ids['native-rows'].children.length, 0);
assert.match(ids['native-count'].textContent, /page 0 of 0/);
ids['native-status'].value=''; ids['native-search'].value='0X1000 SYMBOL_0'; ids['native-search'].handlers.input();
assert.equal(ids['native-rows'].children.length, 1);
'''
        result = subprocess.run([shutil.which('node'), '-e', prelude + browser.SCRIPT + assertions], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which('node'), 'Node is unavailable')
    def test_lazy_inventory_loading_retry_and_scope_with_dom_stub(self):
        prelude = r'''
const assert = require('node:assert/strict');
function element() { return { children: [], value: '', textContent: '', handlers: {}, dataset: {},
  append(...children) { this.children.push(...children); }, replaceChildren() { this.children = []; },
  remove() { this.removed = true; }, addEventListener(type, callback) { this.handlers[type] = callback; }
}; }
const ids = Object.fromEntries(['native-search','native-status','native-rows','native-count','native-prev','native-next','native-load-inventory','native-load-status','native-scope'].map(id => [id, element()]));
ids['native-load-inventory'].dataset.total='205';
ids['native-load-inventory'].dataset.revision='captured-v1';
const head=element();
global.document={getElementById(id) {return ids[id];},createElement:element,head};
global.window={nativeRows:[['0x1000',['existing code'],'exported',1,[['Pseudocode','code.c']]]]};
const full=Array.from({length:205},(_,i)=>['0x'+(4096+i).toString(16),['symbol_'+i],i===0?'exported':'pending',i===0?1:0,[]]);
'''
        assertions = r'''
assert.equal(head.children.length,0); // No initial full-inventory load.
assert.equal(ids['native-rows'].children.length,1);
const load=ids['native-load-inventory']; load.handlers.click();
assert.equal(load.disabled,true); assert.equal(head.children[0].src,'native-inventory.js');
load.handlers.click(); assert.equal(head.children.length,1); // Duplicate load suppressed.
head.children[0].onerror(); assert.equal(load.disabled,false);
assert.equal(ids['native-rows'].children.length,1); assert.match(ids['native-load-status'].textContent,/retry/);
load.handlers.click(); window.nativeInventoryRows=[]; window.nativeInventoryRevision='captured-v1'; head.children[1].onload();
assert.equal(load.disabled,false); assert.equal(ids['native-rows'].children.length,1); // Wrong count rejected.
load.handlers.click(); window.nativeInventoryRows=full; window.nativeInventoryRevision='changed-v2'; head.children[2].onload();
assert.match(ids['native-load-status'].textContent,/refresh this page/); assert.equal(ids['native-rows'].children.length,1);
const malformed=full.map(row=>row.slice()); malformed[0][4]=null;
load.handlers.click(); window.nativeInventoryRows=malformed; window.nativeInventoryRevision='captured-v1'; head.children[3].onload();
assert.equal(load.disabled,false); assert.equal(ids['native-rows'].children.length,1);
assert.equal(ids['native-rows'].children[0].children[1].textContent,'existing code');
for (const [field,value] of [[4,null],[4,[['broken']]],[4,[['label',null]]],[4,new Array(1)],[1,null],[1,[123]],[1,new Array(1)],[0,123],[2,null],[3,-1],[3,0.5]]) {
  const badTail=full.map(row=>row.slice());badTail[150][field]=value;
  load.handlers.click();window.nativeInventoryRows=badTail;window.nativeInventoryRevision='captured-v1';head.children.at(-1).onload();
  assert.equal(load.disabled,false);assert.equal(ids['native-rows'].children.length,1);
  assert.equal(ids['native-next'].disabled,true); // Tail rows reject before a later page can crash.
}
const sparse=full.slice();delete sparse[150];
load.handlers.click();window.nativeInventoryRows=sparse;window.nativeInventoryRevision='captured-v1';head.children.at(-1).onload();
assert.equal(load.disabled,false);assert.equal(ids['native-rows'].children.length,1);
ids['native-search'].value='existing'; ids['native-search'].handlers.input();
assert.equal(ids['native-rows'].children.length,1); // Filters remain usable after failed render.
ids['native-search'].value='symbol_204'; ids['native-search'].handlers.input();
assert.equal(ids['native-rows'].children.length,0);
load.handlers.click(); window.nativeInventoryRows=full; window.nativeInventoryRevision='captured-v1'; head.children.at(-1).onload();
assert.equal(load.hidden,true); assert.equal(ids['native-rows'].children.length,1);
assert.equal(ids['native-rows'].children[0].children[1].textContent,'symbol_204');
assert.match(ids['native-scope'].textContent,/all 205/);
ids['native-search'].value=''; ids['native-search'].handlers.input();
assert.equal(ids['native-rows'].children.length,100);
ids['native-next'].handlers.click(); ids['native-next'].handlers.click();
assert.equal(ids['native-rows'].children.length,5);
ids['native-status'].value='pending'; ids['native-status'].handlers.input();
assert.match(ids['native-count'].textContent,/204 matching functions/);
'''
        result = subprocess.run([shutil.which('node'), '-e', prelude + browser.SCRIPT + assertions], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
