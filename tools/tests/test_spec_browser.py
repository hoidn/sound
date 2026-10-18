"""Requirements browser tests against a small synthetic wiki, never the real pages."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import spec_browser

SPEC = """---
id: SPEC-DEMO
type: spec
status: draft
---
# Demo
## Requirements
### REQ-DEMO-001 — first rule
The device does one thing.
| ID | Statement |
| --- | --- |
| REQ-DEMO-001 | duplicate of the heading |
| REQ-DEMO-002 | second rule from a table |
"""
RESEARCH = """# Packet
## Candidate requirements for SPEC-DEMO
| ID | Statement | Evidence | Strength |
| --- | --- | --- | --- |
| D-C01 | Reads `x` \\| y <script>alert(1)</script> | [data](../../analysis/out.json#k) | Observed |
## Next
| Z-01 | not a candidate | | |
"""


class SpecBrowserTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for d in ('wiki/specs', 'wiki/research', 'analysis'):
            (self.root / d).mkdir(parents=True)
        (self.root / 'wiki/specs/demo.md').write_text(SPEC)
        (self.root / 'wiki/research/packet.md').write_text(RESEARCH)
        (self.root / 'analysis/out.json').write_text('{}')
        self.out = self.root / 'analysis/browse/specs'

    def tearDown(self):
        self.tmp.cleanup()

    def test_rows_from_headings_tables_and_candidate_sections(self):
        rows = spec_browser.collect(self.root)
        self.assertEqual([(r['id'], r['kind']) for r in rows],
                         [('REQ-DEMO-001', 'Draft spec'), ('REQ-DEMO-002', 'Draft spec'), ('D-C01', 'Candidate')])
        self.assertTrue(all(r['target'] == 'SPEC-DEMO' for r in rows))

    def test_page_escapes_text_and_resolves_links(self):
        spec_browser.build(self.root, self.out)
        page = (self.out / 'index.html').read_text()
        self.assertNotIn('<script>alert', page)
        self.assertIn('<code>x</code> \\| y &lt;script&gt;', page)
        self.assertIn('href="../../out.json#k"', page)
        self.assertIn('href="../../../wiki/research/packet.md#candidate-requirements-for-spec-demo"', page)


if __name__ == '__main__':
    unittest.main()
