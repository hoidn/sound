"""Root-selected sixteen-byte data read; no decoder or original instruction."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

B = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
OUT = B / 'depth-utility-x86-mode-table-data'
IMAGE = Path('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64')
HEADER = B / 'depth-utility-x86-process-span-preparation/header-map.json'
RAW = B / 'depth-utility-x86-process-span/process-span-904.bin'
PEER = B / 'reviews/utility-x86-process-span-static-actual-review.json'
START = 0x104b8cb38


def identity(p):
    raw = p.read_bytes()
    return dict(path=str(p), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def save(name, value):
    with (OUT / name).open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


assert not OUT.exists()
paths = [IMAGE, HEADER, RAW, PEER, Path(__file__).resolve()]
before = [identity(p) for p in paths]
assert before[0]['sha256'] == '1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0'
assert before[3]['sha256'] == '86bd24a65e14f77aff90ee7a21242e408f8bab4a81b35f4e517b26ed1fb8e4fb'
m = json.loads(HEADER.read_text())
assert m['image'] == before[0]
s = m['selected_segment']
assert s['name'] == '__TEXT' and s['vmaddr'] == 0x100000000 and s['fileoff'] == 0
assert s['vmaddr'] <= START and START + 16 <= s['vmaddr'] + s['filesize']
assert s['initprot'] & 4
# The independently reviewed native LEA/MOVSXD/ADD/JMP nominates only these four words.
assert RAW.read_bytes()[47:63].hex() == '488d0d52030000486304814801c8ffe0'
with IMAGE.open('rb') as f:
    assert f.read(32).hex() == m['header_hex']
    assert f.read(6832).hex() == m['load_commands_hex']
    f.seek(START - s['vmaddr'])
    raw = f.read(16)
assert len(raw) == 16
offsets = struct.unpack('<4i', raw)
OUT.mkdir()
save('before-map.json', before)
with (OUT / 'mode-table-16.bin').open('xb') as f:
    f.write(raw)
save('result.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
     selection='Root separate fixed16B data read after full4757B current actual peer read',
     start=hex(START), end_exclusive=hex(START + 16), file_offset=hex(START - s['vmaddr']),
     raw_hex=raw.hex(), signed_little32_offsets=list(offsets),
     target_expressions=[hex(START + x) for x in offsets],
     limits='Literal four signed32 words and base-plus-offset expressions only; no target read, mode meaning, CFG, ABI, public behavior or original execution. Simple data reader has no standalone child PID/command receipt.'))
after = [identity(p) for p in paths]
assert before == after
save('after-map.json', after)
files = []
for p in sorted(OUT.iterdir()):
    r = identity(p)
    files.append(dict(path=p.name, bytes=r['bytes'], sha256=r['sha256']))
save('manifest.json', dict(files=files, original_instruction_execution=False))
print(json.dumps(dict(manifest=identity(OUT / 'manifest.json'), unchanged=True), indent=2))
