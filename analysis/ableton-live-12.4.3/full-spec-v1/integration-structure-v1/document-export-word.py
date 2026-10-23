"""Root-selected one8Bdata word only; standard Mach-O header mapping, no target follow."""
from pathlib import Path
import hashlib
import json
import struct

HERE = Path(__file__).resolve().parent
IMAGE = HERE.parents[1] / 'derived/Live.arm64'
START, END = 0x106530bd8, 0x106530be0
EXPECTED = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'

def sha(b):
    return hashlib.sha256(b).hexdigest()

if __name__ == '__main__':
    assert not (HERE / 'document-export-word.json').exists()
    assert not (HERE / 'document-export-word.bin').exists()
    before = sha(IMAGE.read_bytes())
    assert before == EXPECTED and IMAGE.stat().st_size == 149711904
    with IMAGE.open('rb') as f:
        header = f.read(32)
        magic, cpu, subtype, typ, ncmds, sizeofcmds, flags, reserved = struct.unpack('<8I', header)
        assert (magic, cpu, subtype, typ, ncmds, sizeofcmds) == (0xfeedfacf, 0x100000c, 0, 2, 53, 6944)
        commands = f.read(sizeofcmds)
        cursor, segments = 0, []
        for i in range(ncmds):
            cmd, size = struct.unpack_from('<II', commands, cursor)
            assert size >= 8 and cursor + size <= len(commands)
            if cmd == 0x19:
                name = commands[cursor+8:cursor+24].split(b'\0', 1)[0].decode()
                vm, vs, off, fs, maxprot, initprot, ns, sf = struct.unpack_from('<QQQQIIII', commands, cursor+24)
                assert off + fs <= 149711904
                segments.append({'name': name, 'vmaddr': hex(vm), 'vmsize': vs, 'fileoff': off, 'filesize': fs, 'command_index': i})
            cursor += size
        assert cursor == sizeofcmds
        maps = [s for s in segments if int(s['vmaddr'],16) <= START and END <= int(s['vmaddr'],16) + min(s['vmsize'],s['filesize'])]
        assert len(maps) == 1
        fileoff = maps[0]['fileoff'] + START - int(maps[0]['vmaddr'],16)
        f.seek(fileoff)
        raw = f.read(8)
    assert len(raw) == 8 and sha(IMAGE.read_bytes()) == before
    value = hex(struct.unpack('<Q', raw)[0])
    # Explicit byte-order counterexample; this assertion does not execute the target.
    assert struct.unpack('<Q', bytes.fromhex('204f290001000000'))[0] == 0x100294f20
    assert struct.unpack('>Q', bytes.fromhex('204f290001000000'))[0] != 0x100294f20
    result = {'source_export_utc': None, 'selection': {'start': hex(START), 'end_exclusive': hex(END), 'bytes': 8}, 'image': {'path': str(IMAGE), 'bytes': 149711904, 'sha256': before}, 'header': {'raw_hex': header.hex(), 'sha256': sha(header), 'ncmds': ncmds, 'sizeofcmds': sizeofcmds, 'load_commands_sha256': sha(commands)}, 'segments': segments, 'mapping': {'count': len(maps), 'segment': maps[0], 'file_offset': fileoff, 'fully_file_backed': True}, 'word': {'raw_hex': raw.hex(), 'sha256': sha(raw), 'u64_little_endian': value}, 'image_before_after_sha_equal': True, 'limits': ['One physical data word only; no target instruction/string/data/callee follow.', 'Alias/source identity must separately agree; no callability/actual registration/runtime/public behavior inferred from the word alone.'], 'method_sha256': sha(Path(__file__).read_bytes())}
    with (HERE / 'document-export-word.bin').open('xb') as f:
        f.write(raw)
    with (HERE / 'document-export-word.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(result, indent=2))
