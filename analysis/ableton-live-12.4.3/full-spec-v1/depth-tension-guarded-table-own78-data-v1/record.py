"""One fixed static 4B+8B read, or owned-data checks. No native/tool/model calls."""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
IMAGE = {'path': '/var/tmp/sound-analysis/helpers/Tension/Tension.arm64',
         'bytes': 449696,
         'sha256': '640700be76a61a782977f8ede5aba32e9b2f287740d7815780b29464e5b424be'}
RANGES = [dict(name='guarded-table', start='0x544be', end_exclusive='0x544c2',
               file_offset=345278, bytes=4),
          dict(name='conditional-own78', start='0x5c138', end_exclusive='0x5c140',
               file_offset=377144, bytes=8)]


def require(value, message):
    if not value:
        raise ValueError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def identity(path):
    h = hashlib.sha256()
    count = 0
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
            count += len(block)
    return dict(path=str(path), bytes=count, sha256=h.hexdigest())


def save(path, value):
    data = value if isinstance(value, bytes) else (json.dumps(value, indent=2) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def geometry(g):
    require(g['image'] == IMAGE and g['ranges'] == RANGES, 'fixed image and two exact ranges')
    require(g['slice_metadata'] == dict(cpu='arm64', slice_offset=524288,
                                        slice_sha256=IMAGE['sha256'], slice_size=449696),
            'retained slice metadata, not an offset addition')
    sections = [dict(addr='0x54180', name='__const', offset=344448, size=5400),
                dict(addr='0x5c0b0', name='__const', offset=377008, size=8544)]
    require([x['metadata'] for x in g['sections']] == sections, 'fixed retained H4 sections')
    for window, section in zip(RANGES, sections):
        start, end, base = int(window['start'], 16), int(window['end_exclusive'], 16), int(section['addr'], 16)
        require(start + window['bytes'] == end and base <= start < end <= base + section['size'],
                'entire selected interval inside section')
        require(section['offset'] + start - base == window['file_offset'] == start
                and start + window['bytes'] <= IMAGE['bytes'], 'standalone mapping only')


def project(table, word):
    require(len(table) == 4 and len(word) == 8, 'exact guarded four bytes and one eight-byte word')
    tags = [dict(tag=tag, table_VA=hex(0x544be + tag), raw_byte_hex=bytes([byte]).hex(),
                 unsigned_byte=byte, branch_base='0x14760', arithmetic_target=hex(0x14760 + 4 * byte),
                 runtime_target=None) for tag, byte in enumerate(table)]
    return dict(tags=tags, table_raw_hex=table.hex(), own78=dict(position='0x5c138',
                raw_le_hex=word.hex(), unsigned_u64_decimal=str(int.from_bytes(word, 'little')),
                unsigned_u64_hex=hex(int.from_bytes(word, 'little')), runtime_target=None),
                interpretation='four guarded tag arithmetic projections and one raw LE integer only')


def watch(pre, raw, digest):
    pins = [{key: value for key, value in pin.items() if key != 'owned_name'} for pin in pre['pins']]
    return [IMAGE, *pins, dict(path=pre['manifest_absolute_path'], bytes=len(raw), sha256=digest)]


def capture(digest):
    require(sys.dont_write_bytecode, 'use python3 -B')
    raw = (HERE / 'pre-call-manifest.json').read_bytes()
    require(sha(raw) == digest, 'exact fixed input manifest')
    pre = json.loads(raw)
    g = load(HERE / 'geometry.json')
    geometry(g)
    require(pre['ranges'] == RANGES and pre['image'] == IMAGE and pre['selected_bytes'] == 12
            and pre['decoder_children'] == 0, 'selected twelve-byte static cut')
    folder = HERE / 'capture'
    folder.mkdir(exist_ok=False)  # No retry after either successful or partial attempt.
    receipt = dict(started_utc=now(), pid=os.getpid(), ppid=os.getppid(), argv=list(sys.argv),
                   sys_executable=sys.executable, proc_self_exe=os.readlink('/proc/self/exe'),
                   pre_call_sha256=digest, before=[], after=[], reads=[], selected_bytes=0,
                   decoder_children=0, original_execution=0, automatic_retry=False, error=None)
    save(folder / 'attempt.json', receipt)
    pins = watch(pre, raw, digest)
    try:
        for pin in pins:
            found = identity(pin['path'])
            receipt['before'].append(found)
            require(found == pin, 'before custody mismatch')
        retained = []
        with Path(IMAGE['path']).open('rb') as image:
            for window in RANGES:
                image.seek(window['file_offset'])
                data = image.read(window['bytes'])
                receipt['selected_bytes'] += len(data)
                receipt['reads'].append(dict(file_offset=window['file_offset'],
                                              requested=window['bytes'], returned=len(data)))
                require(len(data) == window['bytes'], 'short selected read')
                save(folder / (window['name'] + '.bin'), data)
                retained.append(data)
        save(folder / 'projections.json', project(*retained))
        for pin in pins:
            found = identity(pin['path'])
            receipt['after'].append(found)
            require(found == pin, 'after custody mismatch')
        receipt['unchanged'] = receipt['before'] == receipt['after'] == pins
        receipt['status'] = 'complete-fixed-data12'
    except BaseException as error:
        receipt['status'] = 'stopped-partial-no-retry'
        receipt['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        receipt['finished_utc'] = now()
        save(folder / 'receipt.json', receipt)
    return dict(status=receipt['status'], selected_bytes=receipt['selected_bytes'], decoder_children=0)


def check(root):
    raw = (root / 'pre-call-manifest.json').read_bytes()
    pre = json.loads(raw)
    for pin in pre['pins']:
        if pin['owned_name'] is not None:
            data = (root / pin['owned_name']).read_bytes()
            require(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'frozen owned input pin')
    g = load(root / 'geometry.json')
    geometry(g)
    require(pre['ranges'] == RANGES and pre['image'] == IMAGE and pre['selected_bytes'] == 12
            and pre['decoder_children'] == 0, 'whole exact input cut')
    retained = [(root / 'capture' / (window['name'] + '.bin')).read_bytes() for window in RANGES]
    require(load(root / 'capture/projections.json') == project(*retained), 'all four tag projections and one raw word')
    receipt, attempt = load(root / 'capture/receipt.json'), load(root / 'capture/attempt.json')
    require(receipt['pre_call_sha256'] == sha(raw) and receipt['status'] == 'complete-fixed-data12'
            and receipt['error'] is None and receipt['unchanged'], 'completed receipt')
    require(receipt['before'] == receipt['after'] == watch(pre, raw, sha(raw)), 'all recorded custody pairs')
    require(receipt['reads'] == [dict(file_offset=w['file_offset'], requested=w['bytes'], returned=w['bytes'])
                                 for w in RANGES] and receipt['selected_bytes'] == 12, 'two exact reads')
    require(receipt['decoder_children'] == receipt['original_execution'] == 0
            and receipt['automatic_retry'] is False, 'no decoder/runtime/retry')
    require(attempt['pid'] == receipt['pid'] and attempt['started_utc'] == receipt['started_utc']
            and attempt['reads'] == attempt['before'] == attempt['after'] == []
            and attempt['selected_bytes'] == 0, 'one initial attempt')
    require(receipt['argv'] == [pre['script_absolute_path'], '--capture-once', sha(raw)]
            and receipt['started_utc'] <= receipt['finished_utc'], 'literal argv and chronology')
    if (root / 'assessment.json').exists():
        a = load(root / 'assessment.json')
        require(a['required_status'] == 'U/OPEN' and a['runtime_targets'] is None
                and a['new_sites_cases_grades'] == 0 and a['getter_is_producer'] is False
                and a['saved_N_current_child_equivalence'] is None
                and a['formal_return_or_stack_ABI'] is None, 'no runtime/public/ABI/member promotion')
    if (root / 'manifest.json').exists():
        manifest = load(root / 'manifest.json')
        actual = {str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f.name != 'manifest.json'}
        require(actual == {pin['path'] for pin in manifest['files']}, 'exact final tree')
        for pin in manifest['files']:
            data = (root / pin['path']).read_bytes()
            require(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'frozen payload pin')
    return dict(status='PASS-owned-data-only', selected_bytes=12, tags=4, raw_u64_words=1,
                custody_pairs=len(receipt['before']), external_paths_opened=0, children=0)


def controls(root, tamper=False):
    g = load(root / 'geometry.json')
    rejected = []

    def reject(name, fn):
        try:
            fn()
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
            return
        raise ValueError('accepted negative ' + name)

    for name, fn in [('fat offset addition', lambda a: a['ranges'][0].update(file_offset=345278 + 524288)),
                     ('table padding', lambda a: a['ranges'][0].update(bytes=8)),
                     ('wrong own slot', lambda a: a['ranges'][1].update(start='0x5c130')),
                     ('other word', lambda a: a['ranges'].append(copy.deepcopy(a['ranges'][1]))),
                     ('section crossing', lambda a: a['sections'][0]['metadata'].update(size=1)),
                     ('wrong image', lambda a: a['image'].update(bytes=449700))]:
        altered = copy.deepcopy(g)
        fn(altered)
        reject(name, lambda a=altered: geometry(a))
    for name, table, word in [('short table', b'\0' * 3, b'\0' * 8),
                              ('extra table byte', b'\0' * 5, b'\0' * 8),
                              ('short word', b'\0' * 4, b'\0' * 7),
                              ('extra word byte', b'\0' * 4, b'\0' * 9)]:
        reject(name, lambda t=table, w=word: project(t, w))
    test = project(bytes([0, 1, 128, 255]), bytes(range(8)))
    require([x['arithmetic_target'] for x in test['tags']] == ['0x14760', '0x14764', '0x14960', '0x14b5c']
            and test['own78']['unsigned_u64_hex'] == '0x706050403020100'
            and all(x['runtime_target'] is None for x in test['tags']), 'boundary/endianness positive fixture')
    if tamper:
        for case in ['raw table', 'raw word', 'runtime target', 'getter producer', 'saved N equivalence', 'formal ABI']:
            with tempfile.TemporaryDirectory(prefix='tension-data12-check-') as temp:
                target = Path(temp) / 'packet'
                shutil.copytree(root, target)
                for file in target.rglob('*'):
                    if file.is_file():
                        file.chmod(0o644)  # Writable TEMP files only, never the sealed source.
                if case in ['raw table', 'raw word']:
                    name = 'guarded-table.bin' if case == 'raw table' else 'conditional-own78.bin'
                    file = target / 'capture' / name
                    data = file.read_bytes()
                    file.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                elif case == 'runtime target':
                    file = target / 'capture/projections.json'
                    value = load(file)
                    value['tags'][0]['runtime_target'] = value['tags'][0]['arithmetic_target']
                    file.write_text(json.dumps(value))
                else:
                    file = target / 'assessment.json'
                    value = load(file)
                    key = {'getter producer': 'getter_is_producer', 'saved N equivalence': 'saved_N_current_child_equivalence',
                           'formal ABI': 'formal_return_or_stack_ABI'}[case]
                    value[key] = True
                    file.write_text(json.dumps(value))
                reject(case, lambda: check(target))
    return dict(status='PASS-data-only-controls', negative_controls=rejected,
                positive_fixture='all four distinct byte boundaries, raw endian and NULL runtime targets',
                writable_copies='TEMP only', external_paths_opened=0, children=0)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['--self-check']:
        result = controls(HERE)
    elif args == ['--check']:
        result = check(HERE)
    elif args == ['--check-controls']:
        result = controls(HERE, tamper=True)
    elif len(args) == 2 and args[0] == '--capture-once':
        result = capture(args[1])
    else:
        raise ValueError('Only selected --capture-once or owned-data check modes')
    print(json.dumps(result, indent=2))
