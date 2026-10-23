"""Read-only finite evidence checks; no original or earlier analysis code is imported."""
from pathlib import Path
import copy
import hashlib
import json
import struct
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(name):
    return json.loads((BASE / name).read_text())

def resolve(document, pointer):
    value = document
    assert pointer.startswith('/')
    for part in pointer[1:].split('/'):
        if isinstance(value, list):
            assert part.isdecimal() and str(int(part)) == part and int(part) < len(value)
            value = value[int(part)]
        else:
            assert part in value
            value = value[part]
    return value

def validate(records, trace):
    assert trace['A1'] == 'U' and trace['new_application_grades'] == 0
    assert trace['new_requirements'] == trace['new_cases'] == trace['coverage_credit'] == 0
    assert trace['required_outcome_denominator'] is None and trace['candidate_conformance'] is None
    assert trace['original_or_source_execution'] is False and trace['complete'] is False
    assert len(trace['claims']) == 4 and len(trace['predicate']) == len(trace['frontiers']) == 3
    for claim in trace['claims']:
        assert all(claim[k] is None for k in ('expected', 'comparison', 'actual'))
        assert claim['target'] == 'U' and claim['executed'] is False
        for pointer in claim['record_refs']:
            assert resolve(records, pointer)
    assert [r['value'] for r in records['pointer_words']] == ['0x1026f1868', '0x1026f1324', '0x1026f131c']
    by_entry = {r['entry']: r for r in records['function_bytes']}
    def word(address):
        row = next(r for r in by_entry.values() if int(r['entry'], 16) <= address < int(r['entry'], 16) + r['bytes'])
        return struct.unpack_from('<I', bytes.fromhex(row['raw']), address - int(row['entry'], 16))[0]
    def ldr(address, base, target, offset, scalar=False):
        value = word(address)
        assert value & 0xffc00000 == (0xbd400000 if scalar else 0xf9400000)
        assert value >> 5 & 31 == base and value & 31 == target
        assert (value >> 10 & 4095) * (4 if scalar else 8) == offset
    def move(address, source, target):
        value = word(address)
        assert value & 0xfffffc00 == 0x1e204000
        assert value >> 5 & 31 == source and value & 31 == target
    def branch(address, target):
        value = word(address)
        assert value >> 26 == 0b100101
        displacement = value & 0x3ffffff
        if displacement & (1 << 25):
            displacement -= 1 << 26
        assert address + displacement * 4 == target
    ldr(0x1026f131c, 0, 0, 0x230)
    ldr(0x10157486c, 0, 0, 0x80, True)
    ldr(0x101574874, 0, 0, 0x84, True)
    ldr(0x1026f1880, 8, 8, 0x270)
    ldr(0x1026f1894, 8, 8, 0x270)
    branch(0x1026f1888, 0x10157486c)
    branch(0x1026f18a0, 0x101574874)
    move(0x1026f188c, 0, 8)
    move(0x1026f18a4, 0, 1)
    move(0x1026f18a8, 8, 0)
    move(0x1026fa4b4, 1, 0)
    for address in (0x1026f1884, 0x1026f189c, 0x1026fa4b0):
        assert word(address) == 0xd63f0100
    for address, target in ((0x1026fa498, 1), (0x1026fa4ac, 8)):
        ldr(address, 8, target, 0x2e8)
    assert word(0x1026fa49c) == 0xd61f0020
    for entry in ('0x10157486c', '0x101574874'):
        assert by_entry[entry]['bytes'] == 8 and word(int(entry, 16) + 4) == 0xd65f03c0


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('read-only: --check required')
    records, trace = load('records.json'), load('trace.json')
    pins = load('inputs.json')['pins']
    watched = [BASE / name for name in ('records.json', 'trace.json', 'inputs.json', 'README.md', 'check.py')]
    watched += [ROOT / p['path'] for p in pins]
    watched += [ROOT / records['image']['path']]
    seal = BASE / 'manifest.json'
    if seal.exists():
        watched.append(seal)
    before = {str(p): digest(p.read_bytes()) for p in watched}
    for pin in pins + ([load('manifest.json')['image']] if seal.exists() else [records['image']]):
        content = (ROOT / pin['path']).read_bytes()
        assert len(content) == pin['bytes'] and digest(content) == pin['sha256']
    for row in records['fresh_full_functions']:
        raw = Path(row['path']).read_bytes().splitlines()[row['line'] - 1]
        assert digest(raw) == row['raw_sha256'] and json.loads(raw) == row['record']
        body = row['record']['code'].encode()
        assert len(body) == row['record']['code_bytes'] and digest(body) == row['record']['code_sha256']
    for row in records['reused_functions']:
        old = json.loads((ROOT / row['path']).read_text())
        assert resolve(old, row['pointer'])['entry'] == row['entry']
    with (ROOT / records['image']['path']).open('rb') as image:
        assert image.read(32).hex() == records['image']['header']
        for row in records['pointer_words'] + records['function_bytes']:
            address = int(row.get('vmaddr', row.get('entry')), 16)
            raw = bytes.fromhex(row['raw'])
            segment = next(s for s in records['segments'] if s['vmaddr'] <= address and address + len(raw) <= s['vmaddr'] + s['filesize'])
            assert row['fileoff'] == segment['fileoff'] + address - segment['vmaddr']
            image.seek(row['fileoff'])
            assert image.read(len(raw)) == raw
            if 'value' in row:
                assert int(row['base'], 16) + int(row['slot'], 16) == address
                assert int.from_bytes(raw, 'little') == int(row['value'], 16)
    validate(records, trace)
    rejected = 0
    mutations = [('grade', lambda r, t: t.update(new_application_grades=1)),
                 ('accept A1', lambda r, t: t.update(A1='accepted')),
                 ('pointer', lambda r, t: t['claims'][0]['record_refs'].append('/fresh_full_functions/-1')),
                 ('lane', lambda r, t: r['function_bytes'][0].update(raw=r['function_bytes'][0]['raw'].replace('0840201e', '0140201e'))),
                 ('wrong slot', lambda r, t: r['pointer_words'][0].update(value='0x1026f1324'))]
    for label, mutate in mutations:
        r, t = copy.deepcopy(records), copy.deepcopy(trace)
        mutate(r, t)
        try:
            validate(r, t)
        except (AssertionError, KeyError, StopIteration):
            rejected += 1
        else:
            raise AssertionError('fixture accepted: ' + label)
    if seal.exists():
        for pin in load('manifest.json')['files']:
            content = (BASE / pin['path']).read_bytes()
            assert len(content) == pin['bytes'] and digest(content) == pin['sha256']
    assert before == {str(p): digest(p.read_bytes()) for p in watched}
    print(json.dumps(dict(status='pass', sealed=seal.exists(), fresh_bodies=5, reused_functions=3, pointer_words=3, body_ranges=7, body_bytes=164, rejection_fixtures=rejected, watch_unchanged=len(watched), original_execution=False, application_grades=0, writes=False)))

if __name__ == '__main__':
    main()
