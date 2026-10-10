import hashlib
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('starts', Path(__file__).resolve().parents[1] / 'index_macho_function_starts.py')
starts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(starts)


def segment(name, vm, size, fileoff, filesize, protection=5):
    return struct.pack('<II16sQQQQiiII', 0x19, 72, name.encode(), vm, size, fileoff, filesize, protection, protection, 0, 0)


def fixture(payload=b'\x80\x08\x04\x00', extra=(), command=True):
    commands = [segment('__TEXT', 0x100000000, 0x1000, 0, 0x1000),
                segment('__LINKEDIT', 0x100002000, 0x1000, 0x1000, 0x1000, 1), *extra]
    if command:
        commands.append(struct.pack('<IIII', 0x26, 16, 0x1000, len(payload)))
    block = b''.join(commands)
    result = bytearray(struct.pack('<8I', 0xfeedfacf, 0x100000c, 0, 2, len(commands), len(block), 0, 0) + block)
    result.extend(b'\0' * (0x2000 - len(result)))
    result[0x1000:0x1000 + len(payload)] = payload
    return result


class FunctionStartsTests(unittest.TestCase):
    def decode(self, data):
        return list(starts.rows(data, starts.header(data)))

    def test_addresses_are_text_relative_and_file_mapped(self):
        self.assertEqual(self.decode(fixture()), [(0x100000400, 0x400, '__TEXT', 0x1000),
                                                 (0x100000404, 0x404, '__TEXT', 0x1002)])

    def test_nonzero_segment_file_offset_mapping(self):
        data = fixture(b'\x80\x60\x00', extra=[segment('__CODE', 0x100003000, 0x100, 0x1800, 0x100)])
        self.assertEqual(self.decode(data)[0][:3], (0x100003000, 0x1800, '__CODE'))

    def test_architecture_and_header_rejected(self):
        for field, value in ((0, 0xcafebabe), (1, 0x1000007), (2, 2), (3, 6), (7, 1)):
            data = fixture();struct.pack_into('<I', data, field * 4, value)
            with self.subTest(field=field), self.assertRaises(ValueError): starts.header(data)
        with self.assertRaises(ValueError): starts.header(b'\0' * 20)

    def test_load_command_bounds(self):
        for change in ('size', 'count', 'cmdsize', 'sections', 'payload'):
            data = fixture()
            if change == 'size': struct.pack_into('<I', data, 20, 0xffffffff)
            if change == 'count': struct.pack_into('<I', data, 16, 1000)
            if change == 'cmdsize': struct.pack_into('<I', data, 36, 7)
            if change == 'sections': struct.pack_into('<I', data, 32 + 64, 1)
            if change == 'payload': struct.pack_into('<I', data, 32 + 144 + 8, len(data))
            with self.subTest(change=change), self.assertRaises(ValueError): starts.header(data)

    def test_missing_and_duplicate_command(self):
        info = starts.header(fixture(command=False));self.assertEqual(info['status'], 'absent')
        self.assertEqual(list(starts.rows(b'', info)), [])
        duplicate = struct.pack('<IIII', 0x26, 16, 0x1000, 4)
        with self.assertRaisesRegex(ValueError, 'duplicate'): starts.header(fixture(extra=[duplicate]))

    def test_malformed_uleb_and_termination(self):
        for payload in (b'\x80', b'\x80\x00', b'\xff' * 9 + b'\x02', b'\x81' * 11,
                        b'\x04', b'\x04\x00\x01'):
            with self.subTest(payload=payload), self.assertRaises(ValueError): self.decode(fixture(payload))
        self.assertEqual(len(self.decode(fixture(b'\x04\x00\x00\x00'))), 1)

    def test_cumulative_overflow(self):
        with self.assertRaisesRegex(ValueError, 'cumulative'): self.decode(fixture(b'\xff' * 9 + b'\x01\x00'))

    def test_alignment_mapping_and_executable_checks(self):
        for payload in (b'\x01\x00', b'\x80\x40\x00', b'\x80\x20\x00'):
            with self.subTest(payload=payload), self.assertRaises(ValueError): self.decode(fixture(payload))
        overlap = segment('__OTHER', 0x100000400, 0x100, 0x1800, 0x100)
        with self.assertRaisesRegex(ValueError, 'ambiguous'): self.decode(fixture(extra=[overlap]))

    def test_virtual_tail_not_file_backed(self):
        data = fixture();struct.pack_into('<Q', data, 32 + 48, 0x402)
        with self.assertRaisesRegex(ValueError, 'file-backed'): self.decode(data)

    def test_atomic_export_and_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);target = root / 'input';target.write_bytes(fixture());out = root / 'index'
            with self.assertRaisesRegex(ValueError, 'mismatch'): starts.extract(target, out, '0' * 64)
            self.assertFalse(out.exists())
            result = starts.extract(target, out, starts.hash_file(target))
            self.assertEqual(result['declared_start_count'], 2)
            import json
            manifest = json.loads((out / 'manifest.json').read_text())
            self.assertEqual(set(manifest), {'addresses.tsv', 'summary.json', 'index_macho_function_starts.py'})
            for name, record in manifest.items():
                self.assertEqual(record['sha256'], hashlib.sha256((out / name).read_bytes()).hexdigest())
            with self.assertRaisesRegex(ValueError, 'already exists'): starts.extract(target, out, starts.hash_file(target))

    def test_corruption_leaves_no_committed_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);target = root / 'input';target.write_bytes(fixture(b'\x80'));out = root / 'index'
            with self.assertRaises(ValueError): starts.extract(target, out, starts.hash_file(target))
            self.assertFalse(out.exists());self.assertEqual(list(root.iterdir()), [target])

    def test_absence_is_explicit_and_has_no_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);target = root / 'input';target.write_bytes(fixture(command=False));out = root / 'index'
            self.assertEqual(starts.extract(target, out, starts.hash_file(target))['status'], 'absent')
            self.assertFalse((out / 'addresses.tsv').exists())


if __name__ == '__main__':
    unittest.main()
