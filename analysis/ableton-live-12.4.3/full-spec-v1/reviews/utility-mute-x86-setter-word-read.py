"""One fixed eight-byte target read as data, with no decoder or target call."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
IMAGE = Path('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64')
HEADER = BASE / 'depth-utility-mute-x86-onmute-entry-preparation/header-map.json'
PEER = BASE / 'reviews/utility-mute-x86-onmute-continuation-review.json'
OUT = BASE / 'depth-utility-mute-x86-setter-data'
VA, OFFSET, LENGTH = 0x104b8c760, 0x4b8c760, 8


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def pattern(raw):
    if len(raw) != 8 or raw[:3] != b'\x40\x88\xb7' or raw[7:] != b'\xc3':
        return dict(pattern='UNKNOWN; stop without expansion')
    return dict(pattern='MOV byte [RDI+disp32],SIL; RET',
        displacement=struct.unpack('<i', raw[3:7])[0])


assert pattern(bytes.fromhex('4088b7cf000000c3'))['displacement'] == 207
assert pattern(bytes.fromhex('4088b7cf000000c2'))['pattern'].startswith('UNKNOWN')
assert pattern(bytes.fromhex('4889b7cf000000c3'))['pattern'].startswith('UNKNOWN')
assert not OUT.exists(), 'Exclusive fixed read; no replay'
assert identity(PEER)['sha256'] == '0113d8318743e71e87cb300764c657cd66b2b0fa812c36c45d26affc4fbaf11c'
OUT.mkdir()
save('selection.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    selector='Root separate exact eight-byte target selection after full3764B continuation peer read',
    va=hex(VA), file_offset=OFFSET, length=LENGTH, peer=identity(PEER),
    method=identity(Path(__file__).resolve()),
    scope='Header metadata and eight bytes only; no whole function, decoder, other target or original call.'))
paths = [IMAGE, HEADER, PEER, Path(__file__).resolve(), OUT / 'selection.json']
before = [identity(path) for path in paths]
save('before-map.json', before)
assert (before[0]['bytes'], before[0]['sha256']) == (163716848,
    '1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0')
metadata = json.loads(HEADER.read_text())
segment = metadata['selected_segment']
assert segment == dict(name='__TEXT', vmaddr=0x100000000, vmsize=111357952,
    fileoff=0, filesize=111357952, maxprot=5, initprot=5, nsects=13, flags=0)
assert segment['vmaddr'] <= VA and VA + LENGTH <= segment['vmaddr'] + segment['filesize']
assert OFFSET == VA - segment['vmaddr'] + segment['fileoff']
with IMAGE.open('rb') as stream:
    header = stream.read(32)
    commands = stream.read(6832)
    assert header.hex() == metadata['header_hex']
    assert hashlib.sha256(commands).hexdigest() == metadata['load_commands_sha256']
    stream.seek(OFFSET)
    raw = stream.read(LENGTH)
assert len(raw) == LENGTH
save('result.json', dict(va=hex(VA), bytes=raw.hex(), analysis=pattern(raw),
    original_calls=0, decoder_children=0,
    limits='Conditional encoding/store carrier only; no actual argument, public binding or native extent proof.'))
after = [identity(path) for path in paths]
save('after-map.json', after)
assert before == after
files = [dict(path=p.name, bytes=p.stat().st_size, sha256=identity(p)['sha256'])
    for p in sorted(OUT.iterdir()) if p.is_file()]
save('manifest.json', dict(files=files, unchanged=True,
    limits='Five fixed input pairs only; finite pretry/I/O limits, no global preservation claim.'))
print(json.dumps(dict(bytes=raw.hex(), analysis=pattern(raw), unchanged=True)))
