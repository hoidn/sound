"""Select six already retained bytes only; no decoder, original call or follow."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
SOURCE = BASE / 'depth-utility-mute-x86-onmute-entry-instructions/onmute-entry-240.bin'
PEER = BASE / 'reviews/utility-mute-x86-onmute-static-actual-review.json'
OUT = BASE / 'depth-utility-mute-x86-onmute-continuation-data'
VA, OFFSET, LENGTH = 0x10224e797, 55, 6


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def continuation(raw):
    if len(raw) != 6 or raw[:2] != b'\x5d\xe9':
        return dict(pattern='UNKNOWN; stop without expansion')
    displacement = struct.unpack('<i', raw[2:])[0]
    return dict(pattern='POP RBP; JMP rel32', signed_displacement=displacement,
        target=hex(VA + 6 + displacement))


assert continuation(b'\x5d\xe9' + struct.pack('<i', -6))['target'] == hex(VA)
assert continuation(b'\x5b\xe9' + b'\0' * 4)['pattern'].startswith('UNKNOWN')
assert continuation(b'\x5d\xe8' + b'\0' * 4)['pattern'].startswith('UNKNOWN')
assert not OUT.exists(), 'Exclusive fixed selection; no replay'
assert identity(PEER)['sha256'] == 'cadb996edbd08d7aa3a7744d997a509e3f1ba6c5d0d0a94ce5d67c6cf888eee7'
OUT.mkdir()
save('selection.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    selector='Root separate exact six-byte continuation after full6909B prefix peer read',
    source=identity(SOURCE), peer=identity(PEER), method=identity(Path(__file__).resolve()),
    va=hex(VA), source_offset=OFFSET, length=LENGTH,
    scope='Previously opaque retained suffix only. No new image window, decoder or target follow.'))
paths = [SOURCE, PEER, Path(__file__).resolve(), OUT / 'selection.json']
before = [identity(path) for path in paths]
save('before-map.json', before)
assert (before[0]['bytes'], before[0]['sha256']) == (240,
    '95a6a34d9e5d369b2e0e8b5e9a7b67a4c4e0c57b60e9969560ad9924bd5b4a59')
raw = SOURCE.read_bytes()[OFFSET:OFFSET + LENGTH]
assert len(raw) == LENGTH
save('result.json', dict(va=hex(VA), bytes=raw.hex(), analysis=continuation(raw),
    remaining_opaque_selected_suffix_bytes=179, original_calls=0, decoder_children=0,
    limits='Encoding/carrier relationship only, no callee/ABI/public binding or extent proof.'))
after = [identity(path) for path in paths]
save('after-map.json', after)
assert before == after
files = [dict(path=p.name, bytes=p.stat().st_size, sha256=identity(p)['sha256'])
    for p in sorted(OUT.iterdir()) if p.is_file()]
save('manifest.json', dict(files=files, unchanged=True,
    limits='Four fixed inputs only, no global preservation or pretry/I/O guarantee.'))
print(json.dumps(dict(bytes=raw.hex(), analysis=continuation(raw), unchanged=True)))
