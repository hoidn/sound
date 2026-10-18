"""Corpus demo extractor tests against small synthetic schema and preset files, never the bundle."""
import gzip
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import corpus_demo

SCHEMA = '<?xml version="1.0" encoding="UTF-8"?>\n<AbletonSchema><Corpus><Decay Class="TimeableFloat" Type="0" /><On Class="TimeableBool" Type="0" /></Corpus></AbletonSchema>\n'


def preset(decay, kind, low=0, high=1):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<Ableton><Corpus><On><Manual Value="true" /></On>'
            f'<ResonanceType><Manual Value="{kind}" /><MidiControllerRange><Min Value="0" /><Max Value="6" /></MidiControllerRange></ResonanceType>'
            f'<Decay><Manual Value="{decay}" /><MidiControllerRange><Min Value="{low}" /><Max Value="{high}" /></MidiControllerRange></Decay>'
            f'</Corpus></Ableton>\n').encode()


class ExtractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.res = Path(self.tmp.name)
        (self.res / 'Schema').mkdir()
        (self.res / corpus_demo.SCHEMA).write_text(SCHEMA)
        self.presets = self.res / corpus_demo.PRESETS
        self.presets.mkdir(parents=True)
        (self.presets / 'Pipe Resonator.adv').write_bytes(gzip.compress(preset(0.5, 5)))
        (self.presets / '<b>Tubular<i>.adv').write_bytes(gzip.compress(preset(0.25, 6)))
        (self.presets / '._Pipe Resonator.adv').write_bytes(b'AppleDouble metadata')

    def tearDown(self):
        self.tmp.cleanup()

    def test_values_ranges_and_type_names(self):
        data = corpus_demo.extract(self.res)
        self.assertEqual([f['name'] for f in data['schema']['fields']], ['Decay', 'On'])
        self.assertEqual({p['name']: p['values']['Decay'] for p in data['presets']}, {'<b>Tubular<i>': '0.25', 'Pipe Resonator': '0.5'})
        self.assertEqual(data['ranges'], {'Decay': [0.0, 1.0], 'ResonanceType': [0.0, 6.0]})
        self.assertEqual(data['type_index_from_preset_names'], {'Pipe': [5], 'Tube': [6]})

    def test_inconsistent_range_rejected(self):
        (self.presets / 'Other.adv').write_bytes(gzip.compress(preset(0.5, 1, high=2)))
        with self.assertRaises(ValueError):
            corpus_demo.extract(self.res)

    def test_page_embeds_data_without_raw_markup(self):
        out = self.res / 'out'
        corpus_demo.build(self.res, out)
        page = (out / 'index.html').read_text()
        self.assertNotIn('<b>Tubular', page)
        self.assertIn('\\u003cb\\u003eTubular', page)
        self.assertNotIn('/*CORPUS_DATA*/', page)


if __name__ == '__main__':
    unittest.main()
