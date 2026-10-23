"""Fixed 40-byte static capture once, or owned-data checks; never execute native code."""
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
POSITIONS = [0x5c0f8, 0x5c110, 0x5c118, 0x5c120, 0x5c128]
OFFSETS = [0x38, 0x50, 0x58, 0x60, 0x68]
IMAGE = {'path': '/var/tmp/sound-analysis/helpers/Tension/Tension.arm64',
         'bytes': 449696,
         'sha256': '640700be76a61a782977f8ede5aba32e9b2f287740d7815780b29464e5b424be'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    path = Path(path)
    with path.open('rb') as stream:
        h = hashlib.sha256()
        size = 0
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            h.update(block)
            size += len(block)
    return {'path': str(path), 'bytes': size, 'sha256': h.hexdigest()}


def load(path):
    return json.loads(path.read_bytes())


def save(path, value):
    data = (json.dumps(value, indent=2) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def geometry(authority):
    require(authority['image'] == IMAGE, 'fixed image identity')
    section = authority['mapping']['const_section']
    require(section == {'addr': '0x5c0b0', 'offset': 377008,
                        'size': 8544, 'name': '__const'}, 'fixed retained section')
    words = authority['words']
    require(len(words) == 5, 'whole five, no extra/gap/P+10')
    for word, va, offset in zip(words, POSITIONS, OFFSETS):
        require(word == {'P_nominee': '0x5c0c0', 'offset': hex(offset),
                         'VA': hex(va), 'file_offset': va, 'bytes': 8}, 'exact word')
        require(377008 <= va and va + 8 <= 377008 + 8544 <= IMAGE['bytes'],
                'complete mapped eight-byte interval')
    return words


def project(authority, raw):
    words = geometry(authority)
    require(len(raw) == 40, 'exact forty retained bytes')
    return [{**word, 'retained_byte_offset': i * 8,
             'raw_le_hex': raw[i * 8:i * 8 + 8].hex(),
             'unsigned_u64_decimal': str(int.from_bytes(raw[i * 8:i * 8 + 8], 'little')),
             'unsigned_u64_hex': hex(int.from_bytes(raw[i * 8:i * 8 + 8], 'little')),
             'runtime_target': None} for i, word in enumerate(words)]


def capture(expected_pre_hash):
    pre_raw = (HERE / 'pre-call-manifest.json').read_bytes()
    require(digest(pre_raw) == expected_pre_hash, 'selected frozen input identity')
    pre = json.loads(pre_raw)
    authority = load(HERE / 'authority.json')
    words = geometry(authority)
    require(pre['image'] == IMAGE and pre['words'] == words, 'selected input projection')
    require(pre['decoder_children'] == 0 and pre['selected_bytes'] == 40, 'data-only cut')
    folder = HERE / 'capture'
    folder.mkdir(exist_ok=False)  # The retained attempt directory is never retried.
    receipt = {'started_utc': now(), 'pid': os.getpid(), 'ppid': os.getppid(),
               'argv': list(sys.argv), 'sys_executable': sys.executable,
               'proc_self_exe': os.readlink('/proc/self/exe'),
               'pre_call_sha256': expected_pre_hash, 'selected_bytes_read': 0,
               'read_calls': [], 'decoder_children': 0, 'original_execution': 0,
               'automatic_retry': False, 'before': [], 'after': [], 'error': None}
    save(folder / 'attempt.json', receipt)
    pins = [IMAGE, *[{k: v for k, v in pin.items() if k != 'owned_name'} for pin in pre['pins']],
            {'path': str(HERE / 'pre-call-manifest.json'),
                                'bytes': len(pre_raw), 'sha256': expected_pre_hash}]
    try:
        for pin in pins:
            found = identity(pin['path'])
            receipt['before'].append(found)
            require(found == pin, 'before custody mismatch')
        retained = bytearray()
        with Path(IMAGE['path']).open('rb') as image:
            for word in words:
                image.seek(word['file_offset'])
                data = image.read(8)
                receipt['selected_bytes_read'] += len(data)
                receipt['read_calls'].append({'file_offset': word['file_offset'],
                                               'requested_bytes': 8, 'returned_bytes': len(data)})
                require(len(data) == 8, 'short selected read')
                with (folder / ('word-' + word['VA'][2:] + '.bin')).open('xb') as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                retained.extend(data)
        save(folder / 'words.json', project(authority, retained))
        for pin in pins:
            found = identity(pin['path'])
            receipt['after'].append(found)
            require(found == pin, 'after custody mismatch')
        receipt['unchanged'] = receipt['before'] == receipt['after'] == pins
        receipt['status'] = 'complete-fixed-five-raw-integers'
    except BaseException as error:
        receipt['error'] = type(error).__name__ + ': ' + str(error)
        receipt['status'] = 'stopped-partial-no-retry'
        raise
    finally:
        receipt['finished_utc'] = now()
        save(folder / 'receipt.json', receipt)
    return {'status': receipt['status'], 'selected_bytes_read': 40, 'decoder_children': 0}


def check(root):
    pre_raw = (root / 'pre-call-manifest.json').read_bytes()
    pre = json.loads(pre_raw)
    for pin in pre['pins']:
        if pin['owned_name'] is not None:
            data = (root / pin['owned_name']).read_bytes()
            require(len(data) == pin['bytes'] and digest(data) == pin['sha256'], 'owned frozen input')
    authority = load(root / 'authority.json')
    words = geometry(authority)
    require(pre['image'] == IMAGE and pre['words'] == words and pre['selected_bytes'] == 40
            and pre['decoder_children'] == 0, 'whole precall inputs')
    raw = b''.join((root / 'capture' / ('word-' + word['VA'][2:] + '.bin')).read_bytes()
                   for word in words)
    for word in words:
        require((root / 'capture' / ('word-' + word['VA'][2:] + '.bin')).stat().st_size == 8,
                'individual retained extent')
    require(load(root / 'capture/words.json') == project(authority, raw), 'all five LE projections')
    receipt = load(root / 'capture/receipt.json')
    attempt = load(root / 'capture/attempt.json')
    require(attempt['started_utc'] == receipt['started_utc']
            and attempt['pid'] == receipt['pid'] and attempt['selected_bytes_read'] == 0
            and attempt['read_calls'] == [] and attempt['before'] == []
            and attempt['after'] == [] and attempt['error'] is None, 'one retained initial attempt')
    require(receipt['argv'] == [pre['script_absolute_path'], '--capture-once', digest(pre_raw)]
            and receipt['started_utc'] <= receipt['finished_utc'], 'literal script argv and chronology')
    require(receipt['pre_call_sha256'] == digest(pre_raw) and receipt['error'] is None
            and receipt['status'] == 'complete-fixed-five-raw-integers', 'successful fixed capture')
    pins = [IMAGE, *[{k: v for k, v in pin.items() if k != 'owned_name'} for pin in pre['pins']],
            {'path': pre['manifest_absolute_path'], 'bytes': len(pre_raw), 'sha256': digest(pre_raw)}]
    require(receipt['before'] == receipt['after'] == pins and receipt['unchanged'], 'all recorded custody')
    require(receipt['selected_bytes_read'] == 40 and receipt['decoder_children'] == 0
            and receipt['original_execution'] == 0 and receipt['automatic_retry'] is False, 'no scope expansion')
    require(receipt['read_calls'] == [{'file_offset': va, 'requested_bytes': 8, 'returned_bytes': 8}
                                      for va in POSITIONS], 'five exact reads, excluded gap')
    if (root / 'assessment.json').exists():
        assessment = load(root / 'assessment.json')
        require(assessment['required_status'] == 'U/OPEN' and assessment['runtime_targets'] is None
                and assessment['complete_P_wordset'] is False and assessment['new_sites_cases_grades'] == 0,
                'no runtime/public/completeness promotion')
    if (root / 'manifest.json').exists():
        manifest = load(root / 'manifest.json')
        actual = {str(path.relative_to(root)) for path in root.rglob('*')
                  if path.is_file() and path.name != 'manifest.json'}
        require(actual == {entry['path'] for entry in manifest['files']}, 'exact final tree')
        for entry in manifest['files']:
            data = (root / entry['path']).read_bytes()
            require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'final frozen payload')
    return {'status': 'PASS-owned-data-only', 'selected_bytes': 40, 'words': 5,
            'custody_pairs': len(pins), 'external_paths_opened': 0, 'children': 0}


def controls(root, tamper=False):
    authority = load(root / 'authority.json')
    rejected = []

    def reject(name, function):
        try:
            function()
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
            return
        raise ValueError('accepted negative: ' + name)

    for name, key, value in [('section offset', 'offset', 377016),
                              ('section bound', 'size', 72)]:
        altered = copy.deepcopy(authority)
        altered['mapping']['const_section'][key] = value
        reject(name, lambda a=altered: geometry(a))
    for name, mutate in [('P+10 extra', lambda w: w.append(dict(w[0], offset='0x10', VA='0x5c0d0'))),
                         ('duplicate word', lambda w: w.__setitem__(1, w[0])),
                         ('intervening gap', lambda w: w[1].update(VA='0x5c100', file_offset=0x5c100)),
                         ('wider read', lambda w: w[0].update(bytes=16)),
                         ('wrong nominal offset', lambda w: w[0].update(offset='0x10'))]:
        altered = copy.deepcopy(authority)
        mutate(altered['words'])
        reject(name, lambda a=altered: geometry(a))
    reject('short bytes', lambda: project(authority, bytes(39)))
    reject('extra bytes', lambda: project(authority, bytes(41)))
    fixture = bytes(range(40))
    rows = project(authority, fixture)
    require(rows[0]['unsigned_u64_hex'] == '0x706050403020100'
            and rows[4]['unsigned_u64_hex'] == '0x2726252423222120'
            and all(row['runtime_target'] is None for row in rows), 'synthetic endian/ordering/null projection')
    if tamper:
        for case in ['retained raw', 'runtime promotion', 'complete table promotion', 'new grade']:
            with tempfile.TemporaryDirectory(prefix='tension-five-words-check-') as temp:
                target = Path(temp) / 'packet'
                shutil.copytree(root, target)
                for path in target.rglob('*'):
                    if path.is_file():
                        path.chmod(0o644)  # Writable TEMP files only; sealed originals untouched.
                if case == 'retained raw':
                    path = target / 'capture/word-5c0f8.bin'
                    data = path.read_bytes()
                    path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                else:
                    path = target / 'assessment.json'
                    value = load(path)
                    key, field = {'runtime promotion': ('runtime_targets', []),
                                  'complete table promotion': ('complete_P_wordset', True),
                                  'new grade': ('new_sites_cases_grades', 5)}[case]
                    value[key] = field
                    path.write_text(json.dumps(value))
                reject(case, lambda: check(target))
    return {'status': 'PASS-data-only-controls', 'negative_controls': rejected,
            'positive_fixture': 'all five distinct ordered little-endian words; runtime_target NULL',
            'temp_only_writable': True, 'external_reads_children': 0}


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
        raise ValueError('Only explicit selected capture-once or owned-data check modes')
    print(json.dumps(result, indent=2))
