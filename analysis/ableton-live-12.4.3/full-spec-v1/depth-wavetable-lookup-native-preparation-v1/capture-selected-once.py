"""One fixed164B ARM64 window. --check reads only immutable documents/synthetic data."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import resource
import re
import signal
import struct
import subprocess
import sys

PRE = Path(__file__).resolve().parent
SELECTION_SHA = '60d6d3e421ed4f0cea3e3743697115f868dc0d948af96f9d5ee492b050887cd2'
DEST = PRE.with_name('depth-wavetable-lookup-native-v1')
RANGES = [('0x1047be9c4',40),('0x1047be9ec',124)]
TIMEOUT = 30
OUTPUT_CAP = 131072
ENV = dict(PATH='/usr/bin:/bin',LANG='C',LC_ALL='C',TZ='UTC')


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
    extents = plan['logical_extents']
    require([(r['entry'], r['bytes']) for r in extents] == RANGES, 'exact two logical extents')
    cursor = int(RANGES[0][0], 16)
    for r in extents:
        start, end = int(r['start'],16), int(r['end_exclusive'],16)
        require(start == int(r['entry'],16) == cursor and start % 4 == 0,
                'aligned contiguous logical start')
        require(type(r['bytes']) is int and end-start == r['bytes'] and r['bytes'] % 4 == 0,
                'exact logical byte extent')
        require(type(r['decoder_rows']) is int and r['decoder_rows'] == r['bytes']//4,
                'logical row count')
        require(r['metadata_ranges'] == [[r['start'],hex(end-1)]], 'source range endpoint')
        require(r['warning_count'] == 0, 'no source warning additions')
        cursor = end
    require(plan['physical_window'] == dict(start='0x1047be9c4',end_exclusive='0x1047bea68',
                                           bytes=164,decoder_rows=41), 'exact physical window')
    require(cursor == int(plan['physical_window']['end_exclusive'],16), 'physical/logical end')
    require(sum(x['bytes'] for x in extents) == 164 and sum(x['decoder_rows'] for x in extents) == 41,
            'logical/physical aggregate')
    require(plan['decoder'] == dict(children=1,timeout_seconds=30,cleanup_wait_seconds=5,
        max_stdout_bytes=OUTPUT_CAP,max_stderr_bytes=OUTPUT_CAP,core_limit_bytes=0,
        environment=ENV,stdin='DEVNULL',format='pdj 41 fixed4byteARM64rows; ESIL not a semantic authority'),
        'fixed child/environment/output policy')
    require(plan['required_unsupported'] == 'U' and plan['coverage_gate'] == 'OPEN', 'no closure')
    require(plan['policy'] == dict(automatic_retry=False,original_execution=False,new_tool_install=False,
        decode_only_selected_raw=True,source_preflight_and_independent_readiness_required=True,
        separate_root_actual_selection_required=True,encountered_target_follow=False,
        cast_ABI_or_public_inference=False,new_grade_site_case_release=False), 'fixed separate gates/no expansion')


def metadata(plan):
    require(len(plan['providers']) == 7 and len({x['path'] for x in plan['providers']}) == 7,
            'exact seven immutable providers')
    for pin in plan['providers']:
        require(pin['path'] not in [plan['image']['path'],plan['tool']['path']], 'document providers only')
        verify_pin(pin)
    authority = json.loads(Path(plan['metadata_authority']['path']).read_text())
    for key in ['image','tool','header_hex','load_commands_sha256','expected_segment']:
        require(plan[key] == authority[key], 'inherited authority '+key)
    census = json.loads(Path(plan['source_census']['path']).read_text())
    records = [json.loads(x) for x in Path(plan['source_records']['path']).read_text().splitlines()]
    for r in plan['logical_extents']:
        found = [x for x in census['records'] if x['entry'] == r['entry']]
        raw = [x for x in records if x['entry'] == r['entry']]
        require(len(found) == len(raw) == 1, 'unique selected source metadata')
        c, d = found[0], raw[0]
        require(c['native_body_bytes'] == d['body_bytes'] == r['bytes'], 'source native extent metadata')
        require(c['native_body_ranges'] == d['body_ranges'] == r['metadata_ranges'], 'source interval')
        require(c['code_sha256'] == d['code_sha256'] == r['code_sha256'], 'source C identity')
        require(sha(d['code'].encode()) == r['code_sha256'], 'source retained C hash')
        require(c['record_thunk'] is d['thunk'] is False and c['warnings'] == d['warnings'] == [],
                'source thunk/warning qualifications')
        require(c['state'] == d['state'] == 'exported' and c['error'] is d['error'] is None and
                c['partial_code'] is d['partial_code'] is False and
                c['timed_out'] is d['timed_out'] is False, 'source exported complete metadata')


def segments(commands, count):
    cursor, result = 0, []
    for _ in range(count):
        require(cursor + 8 <= len(commands), 'load-command header bounds')
        kind, size = struct.unpack_from('<II', commands, cursor)
        require(size >= 8 and size % 8 == 0 and cursor + size <= len(commands), 'load-command size bounds')
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
    require(isinstance(rows,list) and len(rows) == window['decoder_rows'] and len(raw) == window['bytes'],
            'exact decoder row/byte count')
    collected = []
    for index, row in enumerate(rows):
        require(type(row) is dict, 'decoder row object')
        require(type(row.get('offset')) is int and row['offset'] == int(window['start'],16)+4*index
                and type(row.get('size')) is int and row['size'] == 4, 'exact aligned decoder address/size')
        require(row.get('type') not in ['ill','invalid'] and isinstance(row.get('opcode'),str)
                and row['opcode'].strip() and not row['opcode'].strip().lower().startswith('invalid'),
                'valid decoded instruction row')
        require(isinstance(row.get('bytes'),str) and re.fullmatch(r'[0-9a-fA-F]{8}',row['bytes']),
                'exact four-byte hex syntax')
        collected.append(bytes.fromhex(row['bytes']))
    require(b''.join(collected) == raw, 'raw decoder row bytes exactly equal selected bytes')


def reject_constant(value):
    raise ValueError('nonfinite JSON '+value)


def decoder_argv(plan, window, rawpath):
    return [plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',window['start'],'-s',window['start'],'-q','-c','pdj '+str(window['decoder_rows']),str(rawpath)]


def child_limits():
    resource.setrlimit(resource.RLIMIT_CORE, (0,0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_CAP,OUTPUT_CAP))


def cleanup_group(child):
    try:
        os.killpg(child.pid, signal.SIGKILL)
        return 'process-group-SIGKILL-sent'
    except ProcessLookupError:
        return 'process-group-already-gone'


def decode_one(plan, window, raw, state):
    tag = window['start'][2:]
    argv = decoder_argv(plan, window, DEST / (tag+'.bin'))
    invocation = dict(argv=argv,environment=ENV,started_utc=utc(),timeout_seconds=TIMEOUT,
        pid=None,exit_code=None,timed_out=False,cleanup=None,core_limit_bytes=0,
        output_limit_bytes_each=OUTPUT_CAP,stdin='DEVNULL',
        process_group='new session; descendants killed after completion/failure',error=None)
    save(tag+'.invocation-before.json', invocation)
    child, error = None, None
    try:
        # Exclusive regular files retain bounded output even after timeout/decoder failure.
        with (DEST/(tag+'.stdout.json')).open('xb') as out, (DEST/(tag+'.stderr')).open('xb') as err:
            state['decoder_attempts'] += 1
            child = subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                cwd=DEST,env=ENV,start_new_session=True,preexec_fn=child_limits)
            invocation['pid'] = child.pid
            state['decoder_children_started'] += 1
            save(tag+'.pid.json',dict(pid=child.pid,pgid=child.pid,spawned_utc=utc(),argv=argv))
            try:
                child.wait(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                invocation['timed_out'] = True
                raise
            finally:
                invocation['cleanup'] = cleanup_group(child)
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    invocation['error'] = 'TimeoutExpired waiting after process-group cleanup'
                    raise
                out.flush()
                err.flush()
                os.fsync(out.fileno())
                os.fsync(err.fileno())
    except BaseException as failure:
        error = failure
        invocation['error'] = type(failure).__name__+': '+str(failure)
    finally:
        # Also cover a failure after Popen but before entering its wait/finally block.
        if child is not None:
            if invocation['cleanup'] is None:
                invocation['cleanup'] = cleanup_group(child)
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired as failure:
                    error = failure
                    invocation['error'] = 'TimeoutExpired in early process-group cleanup'
            invocation['exit_code'] = child.returncode
        invocation['finished_utc'] = utc()
        save(tag+'.invocation-after.json',invocation)
    if error is not None:
        raise error
    require(child.returncode == 0, 'decoder nonzero exit')
    stdout = (DEST/(tag+'.stdout.json')).read_bytes()
    stderr = (DEST/(tag+'.stderr')).read_bytes()
    require(len(stdout) <= OUTPUT_CAP and len(stderr) <= OUTPUT_CAP, 'bounded retained output')
    require(not stderr, 'decoder stderr must be empty; no retries')
    decoded = json.loads(stdout, parse_constant=reject_constant)
    validate_rows(decoded, raw, window)
    # Two logical slices, no second extraction or decoder call.
    logical = []
    offset = 0
    for extent in plan['logical_extents']:
        length = extent['bytes']
        local_raw = raw[offset:offset+length]
        local_rows = decoded[offset//4:(offset+length)//4]
        validate_rows(local_rows,local_raw,extent)
        logical.append(dict(entry=extent['entry'],bytes=length,decoder_rows=len(local_rows),
            physical_byte_offset=offset,sha256=sha(local_raw)))
        offset += length
    save('logical-extents.json',logical)
    state['validated_rows'] = len(decoded)


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
        state['phase'] = 'header-mapping-and-one-extraction'
        with Path(plan['image']['path']).open('rb') as stream:
            header = stream.read(32)
            require(header.hex() == plan['header_hex'], 'fresh pinned image header')
            magic,cpu,_,_,ncmds,sizeofcmds,_,_ = struct.unpack('<IiiIIIII',header)
            require(magic == 0xfeedfacf and cpu == 0x100000c and ncmds == 53 and sizeofcmds == 6944, 'fixed arm64 header')
            commands = stream.read(sizeofcmds)
            require(len(commands) == sizeofcmds and sha(commands) == plan['load_commands_sha256'], 'fresh pinned load commands')
            maps = segments(commands,ncmds)
            window = plan['physical_window']
            offset = mapped_offset(window,maps,plan['expected_segment'],plan['image']['bytes'])
            stream.seek(offset)
            raw = stream.read(window['bytes'])
            require(len(raw) == 164, 'exact selected164byte extraction')
            state['selected_bytes_read'] = len(raw)
            save(window['start'][2:]+'.bin',raw)
        save('extraction.json',dict(header_hex=header.hex(),load_commands_sha256=sha(commands),
            segment=plan['expected_segment'],physical_window=dict(**window,file_offset=offset,sha256=sha(raw)),
            logical_extents=plan['logical_extents'],total_bytes=164,branch_global_slot_expansion=False))
        state['phase'] = 'one-static-decoder'
        decode_one(plan,window,raw,state)
        require(state['decoder_attempts'] == state['decoder_children_started'] == 1 and
                state['validated_rows'] == 41 and state['selected_bytes_read'] == 164, 'fixed capture totals')
        state['phase'] = 'captured-byte-exact-static-rows-no-semantic-conclusion'
    except BaseException as error:
        state['error'] = type(error).__name__+': '+str(error)
        save('failure.json',dict(ended_utc=utc(),phase=state['phase'],entry='0x1047be9c4–0x1047bea68',error=state['error'],partial_files_retained=True,automatic_retry=False))
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
    metadata(plan)  # Only the seven immutable document providers, never image/tool.
    negatives = []
    def rejected(name, action):
        try:
            action()
        except (ValueError, KeyError, TypeError, struct.error, json.JSONDecodeError):
            negatives.append(name)
            return
        raise ValueError('negative accepted: '+name)
    mutations = [
        ('third logical extent',lambda q:q['logical_extents'].append(copy.deepcopy(q['logical_extents'][0]))),
        ('extent order',lambda q:q['logical_extents'].reverse()),
        ('unaligned start',lambda q:q['logical_extents'][0].update(start='0x1047be9c5')),
        ('logical extension',lambda q:q['logical_extents'][0].update(end_exclusive='0x1047be9f0')),
        ('logical rows',lambda q:q['logical_extents'][1].update(decoder_rows=30)),
        ('source endpoint',lambda q:q['logical_extents'][0].update(metadata_ranges=[['0x1047be9c4','0x1047be9ec']])),
        ('warning addition',lambda q:q['logical_extents'][0].update(warning_count=1)),
        ('physical extension',lambda q:q['physical_window'].update(bytes=168)),
        ('physical rows',lambda q:q['physical_window'].update(decoder_rows=42)),
        ('second child',lambda q:q['decoder'].update(children=2)),
        ('environment extension',lambda q:q['decoder']['environment'].update(RZ_TEST='1')),
        ('retry enable',lambda q:q['policy'].update(automatic_retry=True)),
        ('missing readiness gate',lambda q:q['policy'].update(source_preflight_and_independent_readiness_required=False)),
        ('public promotion',lambda q:q['policy'].update(cast_ABI_or_public_inference=True)),
        ('closure promotion',lambda q:q.update(coverage_gate='CLOSED'))]
    for name, mutate in mutations:
        q = copy.deepcopy(plan)
        mutate(q)
        rejected(name,lambda q=q:validate_ranges(q))
    wrong = copy.deepcopy(plan['providers'][0]);wrong['sha256'] = '0'*64
    rejected('changed immutable provider',lambda:verify_pin(wrong))
    w = plan['physical_window']
    raw = bytes(range(164))
    rows = [dict(offset=int(w['start'],16)+i,size=4,bytes=raw[i:i+4].hex(),
                 opcode='synthetic-data',type='synthetic') for i in range(0,164,4)]
    validate_rows(rows,raw,w)
    validate_rows(rows[:10],raw[:40],plan['logical_extents'][0])
    validate_rows(rows[10:],raw[40:],plan['logical_extents'][1])
    rejected('missing row',lambda:validate_rows(rows[:-1],raw,w))
    rejected('raw truncated',lambda:validate_rows(rows,raw[:-1],w))
    for name,key,value in [('wrong address','offset',int(w['start'],16)+4),
        ('boolean address','offset',True),('wrong size','size',8),('boolean size','size',True),
        ('raw mismatch','bytes','ffffffff'),('short rowhex','bytes','000000'),
        ('whitespace rowhex','bytes','00 00 00 00'),('nonhex row','bytes','zzzzzzzz'),
        ('invalid opcode','opcode','invalid'),('invalid opcode prefix','opcode','invalid instruction'),
        ('empty opcode','opcode',' '),('ill type','type','ill')]:
        altered = copy.deepcopy(rows);altered[0][key] = value
        rejected(name,lambda altered=altered:validate_rows(altered,raw,w))
    altered=copy.deepcopy(rows);altered[0]=None
    rejected('nonobject row',lambda:validate_rows(altered,raw,w))
    rejected('nonfinite JSON',lambda:json.loads('[NaN]',parse_constant=reject_constant))
    command = struct.pack('<II16sQQQQiiII',0x19,72,b'__TEXT',0x100000000,105873408,0,105873408,5,5,0,0)
    maps=segments(command,1)
    offset=mapped_offset(w,maps,plan['expected_segment'],plan['image']['bytes'])
    require(offset==0x47be9c4 and offset+164==0x47bea68,'synthetic exact file mapping')
    rejected('ambiguous mapping',lambda:mapped_offset(w,maps+maps,plan['expected_segment'],plan['image']['bytes']))
    rejected('truncated commands',lambda:segments(command[:-1],1))
    rejected('trailing commands',lambda:segments(command+b'12345678',1))
    short=struct.pack('<II',0x19,8)
    rejected('short segment',lambda:segments(short,1))
    zero=struct.pack('<II',1,0)
    rejected('zero command size',lambda:segments(zero,1))
    shifted=copy.deepcopy(maps);shifted[0]['fileoff']=4
    rejected('changed file offset',lambda:mapped_offset(w,shifted,plan['expected_segment'],plan['image']['bytes']))
    rejected('image bounds',lambda:mapped_offset(w,maps,plan['expected_segment'],offset+163))
    outside=copy.deepcopy(w);outside['start']='0x1'
    rejected('outside TEXT',lambda:mapped_offset(outside,maps,plan['expected_segment'],plan['image']['bytes']))
    require(not DEST.exists(),'no capture destination may exist during preparation check')
    print(json.dumps(dict(status='PASS-preparation-data-only',selection_sha256=SELECTION_SHA,
        logical_extents=2,physical_windows=1,selected_bytes=164,decoder_rows=41,
        immutable_document_pins_checked=7,synthetic_negative_controls=negatives,
        negative_count=len(negatives),positive='full41rows and logical10/31rows; exact synthetic mapping',
        image_tool_or_target_bytes_read=0,decoder_children_started=0,original_model_harness_calls=0,
        required_unsupported='U',coverage_gate='OPEN',
        limits='Not source-readiness approval or actual selection. Provider/image/tool identities remain inherited until future actual.'),indent=2))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        raise SystemExit(check())
    if sys.argv[1:] != ['--capture-selected-once',SELECTION_SHA]:
        raise SystemExit('Use --check, or separately Root-selected --capture-selected-once with frozen selection digest; no retries/overrides.')
    raise SystemExit(capture(selection()))
