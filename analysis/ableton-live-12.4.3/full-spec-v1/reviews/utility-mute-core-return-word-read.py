"""One fixed four-byte data read; no decoder, target execution or follow-up."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
OUT = BASE / 'depth-utility-mute-core-return-word'
IMAGE = BASE.parent / 'derived/Live.arm64'
VA = 0x1047bda74


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(name, value):
    with (OUT / name).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


assert 0xd65f03c0 & 0xfffffc1f == 0xd65f0000
assert (0xd65f03c0 >> 5) & 31 == 30
assert 0xd61f03c0 & 0xfffffc1f != 0xd65f0000
assert not OUT.exists(), 'Exclusive fixed data read; no replay'
OUT.mkdir()
selection = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    selector='Root separate four-byte data selection after full6862B prefix peer read',
    question='Is the nominated bit-set destination a RET, and which register?',
    range=[hex(VA), hex(VA + 4)], bytes=4,
    method=identity(Path(__file__).resolve()),
    scope='Header metadata and exactly one word; no decoder, other instructions or original execution')
save('selection.json', selection)
paths = [IMAGE, Path(__file__).resolve(), OUT / 'selection.json',
    BASE / 'depth-utility-mute-core-prefix-instruction-preparation/header-map.json',
    BASE / 'depth-utility-mute-core-prefix-instruction-data/manifest.json',
    BASE / 'reviews/utility-mute-core-prefix-static-actual-review.json']
before = [identity(path) for path in paths]
save('before-map.json', before)
assert (before[0]['bytes'], before[0]['sha256']) == (149711904,
    '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad')
assert before[-1]['sha256'] == '82c06be6e58b10f800015d02a0dfbff455012c2f88ae2318d2bb0c3562e5fbbc'
mapping = json.loads(paths[3].read_text())
segment = mapping['selected_segment']
assert segment == dict(name='__TEXT', vmaddr=0x100000000, vmsize=105873408,
    fileoff=0, filesize=105873408, maxprot=5, initprot=5)
assert segment['vmaddr'] <= VA and VA + 4 <= segment['vmaddr'] + segment['filesize']
offset = VA - segment['vmaddr'] + segment['fileoff']
assert offset == 0x47bda74
with IMAGE.open('rb') as stream:
    header = stream.read(32)
    commands = stream.read(6944)
    assert header.hex() == mapping['header_hex']
    assert hashlib.sha256(commands).hexdigest() == mapping['load_commands_sha256']
    stream.seek(offset)
    raw = stream.read(4)
assert len(raw) == 4
with (OUT / 'word.bin').open('xb') as stream:
    stream.write(raw)
word = struct.unpack('<I', raw)[0]
is_ret = word & 0xfffffc1f == 0xd65f0000
save('result.json', dict(va=hex(VA), file_offset=offset, bytes=raw.hex(),
    word=hex(word), RET_encoding=is_ret, RET_Rn=(word >> 5) & 31 if is_ret else None,
    interpretation='Encoding only; reached valid return/address and path composition remain conditional',
    original_calls=0, decoder_children=0))
after = [identity(path) for path in paths]
save('after-map.json', after)
assert before == after
files = [dict(path=p.name, bytes=p.stat().st_size, sha256=identity(p)['sha256'])
    for p in sorted(OUT.iterdir()) if p.is_file()]
save('manifest.json', dict(files=files, unchanged=True,
    limits='Six fixed inputs only; not a global preservation audit. No retry or extra byte read.'))
print(json.dumps(dict(bytes=raw.hex(), word=hex(word), RET_encoding=is_ret,
    RET_Rn=(word >> 5) & 31 if is_ret else None, unchanged=True)))
