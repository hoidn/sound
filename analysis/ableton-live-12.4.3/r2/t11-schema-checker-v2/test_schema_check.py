"""Run against either checker to retain the failing baseline and corrected result.

python3 -I -B test_schema_check.py <path/to/schema_check.py>
Schemas are read from the locally retained bundle; no Live program is executed.
"""
import gzip
import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
T11 = HERE.parent / 't11-structure-v1'
SCHEMAS = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema')
TARGET = Path(sys.argv.pop(1)).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


subject = load(TARGET, 'subject')
legacy = load(T11 / 'schema_check.py', 'legacy')


def read(path):
    data = path.read_bytes()
    return ET.fromstring(gzip.decompress(data) if data[:2] == b'\x1f\x8b' else data)


def measure(module, root, schema):
    deviations, pointees = module.check(schema, root)
    return deviations, module.rules(root, pointees)


class SchemaCheckTests(unittest.TestCase):
    def old_fixture(self, n=41):
        return read(ROOT / f'handoff/clip-launch-v2/fixtures/CLIP-LAUNCH-{n:03}.xml')

    def test_old_fixtures_count_their_existing_scenes(self):
        schema = subject.load_schema(SCHEMAS / '11.0_405.txt')
        for n in range(41, 46):
            with self.subTest(case=n):
                root = self.old_fixture(n)
                deviations, result = measure(subject, root, schema)
                self.assertEqual(deviations, {})
                self.assertEqual(result['scenes'], 2)
                self.assertTrue(result['scenes_present'])
                self.assertTrue(result['main_slots_equal_scenes'])
                self.assertEqual(result['pointees'], 66)

    def test_old_main_track_sends_are_measured(self):
        root = self.old_fixture()
        ls = root.find('LiveSet')
        holder = ls.find('Tracks/ReturnTrack')
        self.assertIsNotNone(holder)
        sends = ls.find('MasterTrack/DeviceChain/Mixer/Sends')
        self.assertIsNotNone(sends)
        ET.SubElement(sends, 'TrackSendHolder', {'Id': '0'})
        _, result = measure(subject, root, subject.load_schema(SCHEMAS / '11.0_405.txt'))
        self.assertFalse(result['main_prehear_no_sends'])

    def test_old_scene_count_still_detects_a_mismatch(self):
        root = self.old_fixture()
        scenes = root.find('LiveSet/SceneNames')
        scenes.remove(scenes[-1])
        _, result = measure(subject, root, subject.load_schema(SCHEMAS / '11.0_405.txt'))
        self.assertEqual(result['scenes'], 1)
        self.assertFalse(result['main_slots_equal_scenes'])

    def test_input_is_not_renamed_or_modified(self):
        root = self.old_fixture()
        before = ET.tostring(root)
        measure(subject, root, subject.load_schema(SCHEMAS / '11.0_405.txt'))
        self.assertEqual(ET.tostring(root), before)

    def test_current_schema_results_are_unchanged(self):
        schema = subject.load_schema(SCHEMAS / '12.0_12402.txt')
        checked = 0
        for path in sorted((ROOT / 'handoff').glob('*/fixtures/*')):
            if path.suffix not in {'.als', '.xml'}:
                continue
            try:
                root = read(path)
            except (ET.ParseError, OSError, EOFError, ValueError):
                continue
            if root.get('MinorVersion') != '12.0_12402' or root.find('LiveSet') is None:
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                try:
                    expected = measure(legacy, root, schema)
                except (TypeError, ValueError, AttributeError) as error:
                    with self.assertRaises(type(error)):
                        measure(subject, root, schema)
                else:
                    self.assertEqual(measure(subject, root, schema), expected)
                checked += 1
        self.assertGreater(checked, 58)
        print(f'Current-schema comparison: {checked} released Live Sets unchanged')

    def test_cli_matches_legacy_for_current_and_invalid_documents(self):
        current = ROOT / 'handoff/clip-launch-v2/fixtures/CLIP-LAUNCH-001.xml'
        with tempfile.TemporaryDirectory() as tmp:
            invalid = Path(tmp) / 'invalid.xml'
            invalid.write_text('<not-xml')
            args = [str(SCHEMAS / '12.0_12402.txt'), str(current), str(invalid)]
            expected = subprocess.check_output([sys.executable, '-I', '-B',
                                               str(T11 / 'schema_check.py'), *args])
            actual = subprocess.check_output([sys.executable, '-I', '-B', str(TARGET), *args])
            self.assertEqual(actual, expected)

    def test_version_scope_does_not_hide_wrong_old_names_in_current_document(self):
        root = self.old_fixture()
        root.set('MinorVersion', '12.0_12402')
        schema = subject.load_schema(SCHEMAS / '12.0_12402.txt')
        self.assertEqual(measure(subject, root, schema), measure(legacy, root, schema))
        self.assertTrue(measure(subject, root, schema)[0])

    def test_sealed_checker_and_manifest_are_unchanged(self):
        self.assertEqual(hashlib.sha256((T11 / 'schema_check.py').read_bytes()).hexdigest(),
                         'a3892c41d834ad6129df79a55438e747c201091e88190bbbb675629782fd2463')
        self.assertEqual(hashlib.sha256((T11 / 'manifest.json').read_bytes()).hexdigest(),
                         '6981daa7706850fc2ab7c607ac01b39c990b65cd0037a1d073cf01630a49db2e')


if __name__ == '__main__':
    unittest.main(verbosity=2)
