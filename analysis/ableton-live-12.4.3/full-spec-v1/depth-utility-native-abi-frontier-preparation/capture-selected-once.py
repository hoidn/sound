"""Seven fixed ARM64 static windows. --check reads only preparation/source metadata."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import resource
import signal
import struct
import subprocess
import sys

PRE = Path(__file__).resolve().parent
SELECTION_SHA = '6fb6333c80c3c8091c7f45149244eacfb23d37e4260a7930da5e123533f7a9ac'
DEST = PRE.with_name('depth-utility-native-abi-frontier-v1')
RANGES = [('0x101aff380',12),('0x101bc3aa0',64),('0x10214b954',128),('0x10215f2b8',248),('0x10215f3d8',4),('0x1023a1004',488),('0x102f4fadc',52)]
TIMEOUT = 30


def require(value, message):
    if not value:
        raise ValueError(message)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            digest.update(block)
            size += len(block)
    return {'path':str(path),'bytes':size,'sha256':digest.hexdigest()}


def verify_pin(pin):
    actual = identity(Path(pin['path']))
    require(all(actual[k] == pin[k] for k in ['bytes','sha256']), 'provider identity: ' + pin['path'])
    return actual


def save(name, value):
    data = value if isinstance(value, bytes) else (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()
    with (DEST / name).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def selection():
    data = (PRE / 'selection.json').read_bytes()
    require(sha(data) == SELECTION_SHA, 'fixed selection digest')
    plan = json.loads(data)
    validate_ranges(plan)
    require(Path(plan['future_destination']) == DEST, 'fixed exclusive destination')
    return plan


def validate_ranges(plan):
    ranges = plan['fixed_ranges']
    require([(r['entry'],r['bytes']) for r in ranges] == RANGES, 'exact seven-entry selection')
    previous = None
    for r in ranges:
        start, end = int(r['start'],16), int(r['end_exclusive'],16)
        require(start == int(r['entry'],16) and start % 4 == 0 and end - start == r['bytes'] and r['bytes'] % 4 == 0, 'aligned physical range')
        require(r['decoder_rows'] == r['bytes'] // 4, 'row/byte count')
        require(previous is None or previous <= start, 'nonoverlapping ranges')
        previous = end
    require(sum(r['bytes'] for r in ranges) == plan['physical_selected_bytes'] == 996 and sum(r['decoder_rows'] for r in ranges) == plan['decoder_rows'] == 249, 'fixed aggregate units')


def metadata(plan):
    for pin in plan['providers']:
        verify_pin(pin)
    for r in plan['fixed_ranges']:
        path = PRE.parents[3] / r['metadata_source']
        records = json.loads(path.read_text())['records']
        record = next(x['record_metadata'] for x in records if x['entry'] == r['metadata_entry'])
        require(record['entry'] == r['entry'] and record['body_bytes'] == r['bytes'], 'source body extent')
        require(record['body_ranges'] == [[r['start'],hex(int(r['end_exclusive'],16)-1)]], 'single source physical interval')
        require(record['thunk'] is r['metadata_thunk'] and len(record['warnings']) == r['warning_count'] == 0, 'source thunk/warning qualification')
        require(record['state'] == 'exported' and not record['timed_out'] and not record['partial_code'] and record['error'] is None, 'source export status')


def segments(commands, count):
    cursor, result = 0, []
    for _ in range(count):
        require(cursor + 8 <= len(commands), 'load-command header bounds')
        kind, size = struct.unpack_from('<II', commands, cursor)
        require(size >= 8 and cursor + size <= len(commands), 'load-command size bounds')
        if kind == 0x19:
            require(size >= 72, 'segment command size')
            name, va, vs, fo, fs, mp, ip, _, _ = struct.unpack_from('<16sQQQQiiII', commands, cursor+8)
            result.append(dict(name=name.rstrip(b'\0').decode('ascii'),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
        cursor += size
    require(cursor == len(commands), 'exact load-command extent')
    return result


def mapped_offset(window, maps, expected, image_size):
    start, length = int(window['start'],16), window['bytes']
    fits = [s for s in maps if s['vmaddr'] <= start and start+length <= s['vmaddr']+s['filesize']]
    require(len(fits) == 1 and fits[0] == expected, 'unique pinned TEXT mapping')
    offset = fits[0]['fileoff'] + start - fits[0]['vmaddr']
    require(0 <= offset and offset+length <= image_size, 'physical image bounds')
    return offset


def validate_rows(rows, raw, window):
    require(isinstance(rows,list) and len(rows) == window['decoder_rows'] and len(raw) == window['bytes'], 'exact decoder row/byte count')
    collected = []
    for index, row in enumerate(rows):
        require(type(row.get('offset')) is int and row['offset'] == int(window['start'],16)+4*index and row.get('size') == 4, 'exact aligned decoder address/size')
        require(row.get('type') != 'ill' and isinstance(row.get('opcode'),str) and row['opcode'].strip().lower() not in ['', 'invalid'], 'valid decoded instruction row')
        value = bytes.fromhex(row['bytes'])
        require(len(value) == 4, 'four raw bytes per row')
        collected.append(value)
    require(b''.join(collected) == raw, 'raw decoder row bytes exactly equal selected bytes')


def reject_constant(value):
    raise ValueError('nonfinite JSON '+value)


def decoder_argv(plan, window, rawpath):
    return [plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',window['start'],'-s',window['start'],'-q','-c','pdj '+str(window['decoder_rows']),str(rawpath)]


def child_limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0,0))


def cleanup_group(child):
    try:
        os.killpg(child.pid, signal.SIGKILL)
        return 'process-group-SIGKILL-sent'
    except ProcessLookupError:
        return 'process-group-already-gone'


def decode_one(plan, window, raw, state):
    tag = window['entry'][2:]
    state['current_entry'] = window['entry']
    argv = decoder_argv(plan, window, DEST / (tag+'.bin'))
    invocation = dict(argv=argv,started_utc=utc(),timeout_seconds=TIMEOUT,pid=None,exit_code=None,timed_out=False,cleanup=None,core_limit_bytes=0,process_group='new session; inherited descendants killed on completion/failure',error=None)
    save(tag+'.invocation-before.json', invocation)
    stdout, stderr, child = b'', b'', None
    error = None
    try:
        state['decoder_attempts'] += 1
        child = subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=DEST,start_new_session=True,preexec_fn=child_limits)
        invocation['pid'] = child.pid
        state['decoder_children_started'] += 1
        save(tag+'.pid.json',dict(pid=child.pid,pgid=child.pid,spawned_utc=utc(),argv=argv))
        try:
            stdout, stderr = child.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired as failure:
            invocation['timed_out'] = True
            stdout, stderr = failure.output or b'', failure.stderr or b''
            raise
    except BaseException as failure:
        error = failure
        invocation['error'] = type(failure).__name__+': '+str(failure)
    finally:
        if child is not None:
            invocation['cleanup'] = cleanup_group(child)
            try:
                stdout, stderr = child.communicate(timeout=5)
            except subprocess.TimeoutExpired as failure:
                stdout, stderr = failure.output or stdout, failure.stderr or stderr
                if error is None:
                    error = failure
                    invocation['error'] = 'TimeoutExpired during descendant/pipe cleanup'
                # No retry: retain partial output and close an escaped inherited pipe.
                child.stdout.close()
                child.stderr.close()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired as failure:
                    error = failure
                    invocation['error'] = 'TimeoutExpired waiting after process-group cleanup'
            invocation['exit_code'] = child.returncode
        save(tag+'.stdout.json',stdout)
        save(tag+'.stderr',stderr)
        invocation['finished_utc'] = utc()
        save(tag+'.invocation-after.json',invocation)
    if error is not None:
        raise error
    require(child.returncode == 0, 'decoder nonzero exit')
    decoded = json.loads(stdout, parse_constant=reject_constant)
    validate_rows(decoded, raw, window)
    state['validated_rows'] += len(decoded)


def capture(plan):
    require(sys.dont_write_bytecode, 'capture requires python3 -B')
    DEST.mkdir()  # Exclusive; any existing failure/success tree refuses reuse.
    state = dict(started_utc=utc(),argv=sys.argv,selection_sha256=SELECTION_SHA,phase='preflight',decoder_attempts=0,decoder_children_started=0,validated_rows=0,selected_bytes_read=0,error=None,original_calls=0,automatic_retry=False)
    save('attempt.json',state)
    watched, before, after = [], [], []
    old_term = signal.getsignal(signal.SIGTERM)
    def interrupted(signum, frame):
        raise RuntimeError('capture interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM, interrupted)
    try:
        manifest = json.loads((PRE/'manifest-preparation.json').read_text())
        require({r['path'] for r in manifest['files']} == {f.name for f in PRE.iterdir() if f.is_file() and f.name != 'manifest-preparation.json'}, 'exact preparation tree')
        for row in manifest['files']:
            verify_pin(dict(path=str(PRE/row['path']),bytes=row['bytes'],sha256=row['sha256']))
        metadata(plan)
        watched = sorted({Path(plan['image']['path']),Path(plan['tool']['path']),*[Path(x['path']) for x in plan['providers']],*[f for f in PRE.iterdir() if f.is_file()]})
        before = [identity(path) for path in watched]
        save('before-identities.json',before)
        for pin in [plan['image'],plan['tool'],*plan['providers']]:
            require(next(r for r in before if r['path'] == pin['path']) == pin, 'fresh image/tool/provider identity')
        state['phase'] = 'header-mapping-and-seven-extractions'
        with Path(plan['image']['path']).open('rb') as stream:
            header = stream.read(32)
            require(header.hex() == plan['header_hex'], 'fresh pinned image header')
            magic,cpu,_,_,ncmds,sizeofcmds,_,_ = struct.unpack('<IiiIIIII',header)
            require(magic == 0xfeedfacf and cpu == 0x100000c and ncmds == 53 and sizeofcmds == 6944, 'fixed arm64 header')
            commands = stream.read(sizeofcmds)
            require(len(commands) == sizeofcmds and sha(commands) == plan['load_commands_sha256'], 'fresh pinned load commands')
            maps = segments(commands,ncmds)
            extracted = []
            for window in plan['fixed_ranges']:
                offset = mapped_offset(window,maps,plan['expected_segment'],plan['image']['bytes'])
                stream.seek(offset)
                raw = stream.read(window['bytes'])
                require(len(raw) == window['bytes'], 'exact selected extraction length')
                state['selected_bytes_read'] += len(raw)
                save(window['entry'][2:]+'.bin',raw)
                extracted.append((window,raw,offset))
        save('extraction.json',dict(header_hex=header.hex(),load_commands_sha256=sha(commands),segment=plan['expected_segment'],ranges=[dict(entry=w['entry'],start=w['start'],end_exclusive=w['end_exclusive'],bytes=len(raw),file_offset=offset,sha256=sha(raw)) for w,raw,offset in extracted],total_bytes=996,branch_global_slot_expansion=False))
        state['phase'] = 'seven-static-decoders'
        for window, raw, _ in extracted:
            decode_one(plan,window,raw,state)
        require(state['decoder_children_started'] == 7 and state['validated_rows'] == 249 and state['selected_bytes_read'] == 996, 'fixed capture totals')
        state['phase'] = 'captured-byte-exact-static-rows-no-semantic-conclusion'
    except BaseException as error:
        state['error'] = type(error).__name__+': '+str(error)
        save('failure.json',dict(ended_utc=utc(),phase=state['phase'],entry=state.get('current_entry'),error=state['error'],partial_files_retained=True,automatic_retry=False))
    finally:
        for path in watched:
            try:
                after.append(identity(path))
            except Exception as error:
                after.append(dict(path=str(path),error=type(error).__name__+': '+str(error)))
        state['watch_unchanged'] = bool(before) and before == after
        if not state['watch_unchanged'] and state['error'] is None:
            state['error'] = 'Watched image/tool/provider/preparation identity changed or incomplete'
            save('failure.json',dict(ended_utc=utc(),phase=state['phase'],error=state['error'],partial_files_retained=True,automatic_retry=False))
        save('after-identities.json',dict(files=after,unchanged=state['watch_unchanged'],ended_utc=utc()))
        state['finished_utc'] = utc()
        save('status.json',state)
        signal.signal(signal.SIGTERM,old_term)
    print(json.dumps(state,indent=2))
    return 0 if state['error'] is None and state['watch_unchanged'] else 1


def check():
    plan = selection()
    metadata(plan)
    negatives = []
    def rejected(name, action):
        try:
            action()
        except (ValueError, KeyError, struct.error):
            negatives.append(name)
            return
        raise ValueError('negative accepted: '+name)
    bad_pin = copy.deepcopy(plan['providers'][0]); bad_pin['sha256'] = '0'*64; rejected('changed source provider pin',lambda:verify_pin(bad_pin))
    broken = copy.deepcopy(plan); broken['fixed_ranges'].append(copy.deepcopy(broken['fixed_ranges'][0])); rejected('eighth range',lambda:validate_ranges(broken))
    broken = copy.deepcopy(plan); broken['fixed_ranges'][0]['start'] = '0x101aff381'; rejected('unaligned/wrong interval',lambda:validate_ranges(broken))
    broken = copy.deepcopy(plan); broken['fixed_ranges'][0]['end_exclusive'] = '0x101aff390'; rejected('range extension',lambda:validate_ranges(broken))
    broken = copy.deepcopy(plan); broken['fixed_ranges'][0]['decoder_rows'] = 4; rejected('decoder row count',lambda:validate_ranges(broken))
    window = plan['fixed_ranges'][0]
    raw = bytes(range(window['bytes']))
    synthetic = [dict(offset=int(window['start'],16)+i,size=4,bytes=raw[i:i+4].hex(),opcode='synthetic-data',type='synthetic') for i in range(0,len(raw),4)]
    validate_rows(synthetic,raw,window)
    rejected('missing decoder row',lambda:validate_rows(synthetic[:-1],raw,window))
    for name,key,value in [('wrong native address','offset',int(window['start'],16)+4),('wrong instruction size','size',8),('wrong raw row bytes','bytes','ffffffff'),('invalid opcode','opcode','invalid'),('illegal row','type','ill')]:
        altered = copy.deepcopy(synthetic); altered[0][key] = value
        rejected(name,lambda altered=altered:validate_rows(altered,raw,window))
    rejected('raw byte length',lambda:validate_rows(synthetic,raw[:-1],window))
    command = struct.pack('<II16sQQQQiiII',0x19,72,b'__TEXT',0x100000000,105873408,0,105873408,5,5,0,0)
    maps = segments(command,1)
    mapped_offset(window,maps,plan['expected_segment'],plan['image']['bytes'])
    rejected('ambiguous TEXT mapping',lambda:mapped_offset(window,maps+maps,plan['expected_segment'],plan['image']['bytes']))
    rejected('truncated load commands',lambda:segments(command[:-1],1))
    outside = copy.deepcopy(window); outside['start'] = '0x1'; rejected('outside pinned TEXT',lambda:mapped_offset(outside,maps,plan['expected_segment'],plan['image']['bytes']))
    shifted = copy.deepcopy(maps); shifted[0]['fileoff'] = 4; rejected('changed segment file offset',lambda:mapped_offset(window,shifted,plan['expected_segment'],plan['image']['bytes']))
    require(not DEST.exists(), 'no capture destination may exist during preparation check')
    print(json.dumps(dict(status='pass-preparation-data-only',selection_sha256=SELECTION_SHA,ranges=7,selected_bytes=996,decoder_rows=249,provider_pins_checked=len(plan['providers']),synthetic_negative_controls=negatives,image_or_tool_files_read=False,selected_image_windows_read=0,decoder_children_started=0,original_calls=0,all_six_bridges='U',application_outcomes_U=38,limits='Synthetic validator and retained metadata checks only; not capture authorization, native ABI evidence or readiness approval.'),indent=2))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        raise SystemExit(check())
    if sys.argv[1:] != ['--capture-selected-once',SELECTION_SHA]:
        raise SystemExit('Use --check, or separately selected --capture-selected-once with the exact frozen selection digest; no retries or overrides.')
    raise SystemExit(capture(selection()))
