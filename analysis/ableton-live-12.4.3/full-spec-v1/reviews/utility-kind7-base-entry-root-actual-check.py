"""Independent finite data checks; no supplied collector/decoder/native execution."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / 'depth-utility-kind7-base-entry-instruction-data'
OUTER = BASE / 'reviews/utility-kind7-base-entry-selected-execution'
DRAFT = BASE / 'depth-corpus-x86-selected-entry-preparation'


def identity(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
            size += len(block)
    return dict(path=str(path), bytes=size, sha256=h.hexdigest())


def load(path):
    return json.loads(path.read_text())


def adrp(word, pc):
    assert word & 0x9f000000 == 0x90000000
    imm = ((word >> 5 & 0x7ffff) << 2) | (word >> 29 & 3)
    if imm & 0x100000:
        imm -= 0x200000
    return word & 31, (pc & ~0xfff) + imm * 4096


def store(word):
    tag = word & 0xffc00000
    assert tag in (0xf9000000, 0xb9000000)
    width = 8 if tag == 0xf9000000 else 4
    return width, word & 31, word >> 5 & 31, (word >> 10 & 4095) * width


# Small controls distinguish changed native operands from the accepted table.
assert adrp(0x90029ea8, 0x10128ed98) == (8, 0x106662000)
assert adrp(0x90029ec8, 0x10128ed98) != (8, 0x106662000)
assert store(0xf9000008) == (8, 8, 0, 0)
assert store(0xf9000028) != (8, 8, 0, 0)

inner = load(DATA / 'before-map.json')
assert inner == load(DATA / 'after-map.json')['files']
assert inner == [json.loads(line) for line in (DATA / 'before-identities.jsonl').read_text().splitlines()]
outer = load(OUTER / 'before-map.json')
assert outer == load(OUTER / 'after-map.json')
paths = {Path(row['path']) for row in inner + outer}
for directory in (DATA, OUTER):
    paths.update(p for p in directory.iterdir() if p.is_file())
assessment = BASE / 'reviews/utility-kind7-base-entry-author-actual-assessment.json'
paths.update((assessment, Path(__file__).resolve()))
watch = sorted(p for p in paths if not p.is_relative_to(DRAFT))
before = [identity(p) for p in watch]
current = {row['path']: row for row in before}
draft_drift = []
for row in inner + outer + load(OUTER / 'pins.json'):
    path = Path(row['path'])
    actual = identity(path) if path.is_relative_to(DRAFT) else current[str(path)]
    if actual != row:
        assert path.is_relative_to(DRAFT), (row, actual)
        if row not in [x['captured'] for x in draft_drift]:
            draft_drift.append(dict(captured=row, current=actual))
payload_counts = []
for directory in (DATA, OUTER):
    manifest = load(directory / 'manifest.json')
    assert {p.name for p in directory.iterdir()} == {'manifest.json', *[r['path'] for r in manifest['files']]}
    for row in manifest['files']:
        actual = identity(directory / row['path'])
        assert (actual['bytes'], actual['sha256']) == (row['bytes'], row['sha256'])
    payload_counts.append(len(manifest['files']))
selection = load(OUTER / 'selection.json')
text = (OUTER / 'execute-selected-once.py').read_text()
for op in reversed(selection['wrapper_literal_delta']):
    assert text.count(op['new']) == op['count']
    text = text.replace(op['new'], op['old'])
assert text == Path(selection['wrapper_parent']['path']).read_text()
extraction = load(DATA / 'extraction.json')
raw = (DATA / 'base-entry-24.bin').read_bytes()
rows = load(DATA / 'decoder.stdout.json')
assert len(raw) == 24 and len(rows) == 6
assert b''.join(bytes.fromhex(r['bytes']) for r in rows) == raw
assert all(r['offset'] == 0x10128ed98 + i * 4 and r['size'] == 4 and len(bytes.fromhex(r['bytes'])) == 4 for i, r in enumerate(rows))
words = struct.unpack('<6I', raw)
assert words == (0x90029ea8, 0x91354108, 0xf9000008, 0xb900081f, 0xf900081f, 0xd65f03c0)
assert adrp(words[0], 0x10128ed98) == (8, 0x106662000)
assert words[1] & 0xffc00000 == 0x91000000
assert (words[1] & 31, words[1] >> 5 & 31, words[1] >> 10 & 4095) == (8, 8, 0xd50)
assert [store(w) for w in words[2:5]] == [(8, 8, 0, 0), (4, 31, 0, 8), (8, 31, 0, 16)]
assert words[5] == 0xd65f03c0 and words[5] >> 5 & 31 == 30
plan = load(BASE / 'depth-utility-kind7-base-entry-instruction-preparation/plan.json')
with Path(plan['image']['path']).open('rb') as stream:
    header = stream.read(32)
    assert header.hex() == plan['image_header_hex']
    values = struct.unpack('<IiiIIIII', header)
    assert values[0] == 0xfeedfacf and values[1] == 0x100000c and values[4:6] == (53, 6944)
    commands = stream.read(6944)
    assert hashlib.sha256(commands).hexdigest() == plan['load_commands_sha256']
    cursor, matches = 0, []
    for _ in range(53):
        command, length = struct.unpack_from('<II', commands, cursor)
        assert length >= 8 and cursor + length <= len(commands)
        if command == 0x19:
            name, va, vs, fo, fs, mp, ip, ns, sf = struct.unpack_from('<16sQQQQiiII', commands, cursor + 8)
            if va <= 0x10128ed98 and 0x10128edb0 <= va + min(vs, fs):
                matches.append((name.rstrip(b'\0'), fo + 0x10128ed98 - va))
        cursor += length
    assert cursor == len(commands) and matches == [(b'__TEXT', 19459480)]
    stream.seek(19459480)
    assert stream.read(24) == raw
status, receipt = load(DATA / 'status.json'), load(OUTER / 'receipt.json')
assert status['tool_attempts'] == receipt['attempted_collector_launches'] == 1
assert status['tool_exit'] == receipt['exit'] == 0
assert status['exception'] is receipt['exception'] is None
assert receipt['inherited_RLIMIT_CORE'] == [0, 0] and not receipt['timeout'] and not receipt['automatic_retry']
assert (DATA / 'decoder.stderr').stat().st_size == (OUTER / 'collector.stderr').stat().st_size == 0
after = [identity(p) for p in watch]
assert before == after
report = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='PASS_PARTIAL_STATIC_DATA',
              payloads=payload_counts, inner_pairs=len(inner), outer_pairs=len(outer), fresh_watch=len(watch),
              watch_unchanged=True, concurrent_unsealed_draft_drift=draft_drift, fresh_same24=True,
              header_commands=53, native_operand_checks=6, controls=2, supplied_tools_executed=0,
              raw_sha256=hashlib.sha256(raw).hexdigest(), watch_digest=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),
              scope='Current original-image identity/header/same24 only; draft excluded from reviewer watch, exact captured outer pairs retained. No other native or target-data follow.')
with (BASE / 'reviews/utility-kind7-base-entry-root-actual-check-result.json').open('x') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(report, indent=2))
