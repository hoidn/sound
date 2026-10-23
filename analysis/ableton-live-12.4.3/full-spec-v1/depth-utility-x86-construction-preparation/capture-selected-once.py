"""Three fixed x86_64 physical caps; no instruction execution. --check reads only preparation/source metadata."""
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
SELECTION_SHA = '598ed96b52fea43a73270f0cd6137633a782c02b934dd56032d5a529146930fe'
DEST = PRE.with_name('depth-utility-x86-construction-native-v1')
RANGES = [('0x101ad08a0',112,28117152),('0x1022313c0',64,35853248),('0x102231400',144,35853312)]
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
    ranges = plan['ranges']
    require([(r['entry'],r['bytes'],r['file_offset']) for r in ranges] == RANGES, 'exact three-entry selection')
    previous = None
    for r in ranges:
        start, end = int(r['start'],16), int(r['end_exclusive'],16)
        require(start == int(r['entry'],16) and end-start == r['bytes'] and r['bytes'] > 0, 'exact physical cap')
        require(previous is None or previous <= start, 'nonoverlapping ranges')
        require(r['file_offset'] == start-plan['header']['text']['vmaddr'], 'fixed physical mapping')
        previous = end
    require(sum(r['bytes'] for r in ranges) == plan['selected_physical_bytes'] == 320, 'fixed aggregate bytes')
    require(plan['architecture'] == 'x86_64' and plan['instruction_sizes_bytes'] == [1,15], 'fixed x86 architecture')
    require(plan['future_max_target_decoder_children'] == 3 and plan['future_timeout_seconds_per_child'] == TIMEOUT and plan['future_automatic_retry'] is False, 'fixed child limits')


def metadata(plan):
    for pin in plan['providers']:
        verify_pin(pin)
    retained = json.loads(Path(plan['providers'][1]['path']).read_text())
    require(retained['header'] == plan['header'], 'retained exact header metadata')
    require(retained['physical_bounds_total_bytes'] == 320, 'retained aggregate cap')
    for window, row in zip(plan['ranges'],retained['rows'],strict=True):
        require(row['entry']['address'] == window['entry'] and row['next_start']['address'] == window['end_exclusive'], 'exact adjacent starts')
        require(row['next_start']['index'] == row['entry']['index']+1 and row['physical_bound_bytes'] == window['bytes'], 'immediate next-start cap')
        require(row['entry']['slice_file_offset'] == window['file_offset'], 'retained selected file offset')


def segments(commands, count):
    cursor, result = 0, []
    for _ in range(count):
        require(cursor + 8 <= len(commands), 'load-command header bounds')
        kind, size = struct.unpack_from('<II', commands, cursor)
        require(size >= 8 and cursor + size <= len(commands), 'load-command size bounds')
        if kind == 0x19:
            require(size >= 72, 'segment command size')
            name, va, vs, fo, fs, mp, ip, _, _ = struct.unpack_from('<16sQQQQiiII', commands, cursor+8)
            result.append(dict(name=name.rstrip(b'\0').decode('ascii'),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,initprot=ip))
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
    require(isinstance(rows,list) and rows and len(raw) == window['bytes'], 'nonempty decoder rows and exact raw length')
    cursor, collected = int(window['start'],16), []
    end = int(window['end_exclusive'],16)
    for row in rows:
        require(isinstance(row,dict), 'decoder row object')
        require(type(row.get('offset')) is int and row['offset'] == cursor, 'consecutive exact decoder address')
        size = row.get('size')
        require(type(size) is int and 1 <= size <= 15 and cursor+size <= end, 'bounded x86 instruction size')
        require(isinstance(row.get('type'),str) and row['type'].strip().lower() not in ['', 'ill', 'invalid'], 'valid row type')
        require(isinstance(row.get('opcode'),str) and row['opcode'].strip().lower() not in ['', 'invalid', '(invalid)'], 'valid row opcode')
        encoded = row.get('bytes')
        require(isinstance(encoded,str) and len(encoded) == 2*size and all(c in '0123456789abcdefABCDEF' for c in encoded), 'exact row hex encoding')
        value = bytes.fromhex(encoded)
        collected.append(value)
        cursor += size
    require(cursor == end and b''.join(collected) == raw, 'complete exact raw byte coverage')


def reject_constant(value):
    raise ValueError('nonfinite JSON '+value)


def decoder_argv(plan, window, rawpath):
    return [plan['tool']['path'],'-NN','-n','-x','-f','-a','x86','-b','64','-E','little','-m',window['start'],'-s',window['start'],'-q','-c','pDj '+str(window['bytes']),str(rawpath)]


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
        child = subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=DEST,stdin=subprocess.DEVNULL,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'},start_new_session=True,preexec_fn=child_limits)
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
    state['validated_bytes'] += len(raw)


def capture(plan):
    require(sys.dont_write_bytecode, 'capture requires python3 -B')
    DEST.mkdir()  # Exclusive; any existing failure/success tree refuses reuse.
    state = dict(started_utc=utc(),argv=sys.argv,selection_sha256=SELECTION_SHA,phase='preflight',decoder_attempts=0,decoder_children_started=0,validated_rows=0,validated_bytes=0,selected_bytes_read=0,error=None,original_calls=0,automatic_retry=False)
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
        watched = sorted({Path(plan['image']['path']),Path(plan['tool']['path']),*[Path(x['path']) for x in plan['providers']],*[f for f in PRE.iterdir() if f.is_file()],Path(plan['old_prefix_identity_actual_capture_only']['path'])})
        before = [identity(path) for path in watched]
        save('before-identities.json',before)
        for pin in [plan['image'],plan['tool'],*plan['providers'],{k:plan['old_prefix_identity_actual_capture_only'][k] for k in ['path','bytes','sha256']}]:
            require(next(r for r in before if r['path'] == pin['path']) == pin, 'fresh image/tool/provider identity')
        state['phase'] = 'header-mapping-and-three-extractions'
        with Path(plan['image']['path']).open('rb') as stream:
            header = stream.read(32)
            require(header.hex() == plan['header']['header_hex'], 'fresh pinned image header')
            magic,cpu,_,_,ncmds,sizeofcmds,_,_ = struct.unpack('<IiiIIIII',header)
            require(magic == 0xfeedfacf and cpu == 0x1000007 and ncmds == 54 and sizeofcmds == 6832, 'fixed x86_64 header')
            commands = stream.read(sizeofcmds)
            require(len(commands) == sizeofcmds and sha(commands) == plan['header']['load_commands_sha256'], 'fresh pinned load commands')
            maps = segments(commands,ncmds)
            extracted = []
            for window in plan['ranges']:
                offset = mapped_offset(window,maps,plan['header']['text'],plan['image']['bytes'])
                stream.seek(offset)
                raw = stream.read(window['bytes'])
                require(len(raw) == window['bytes'], 'exact selected extraction length')
                require(offset == window['file_offset'], 'exact selected offset')
                state['selected_bytes_read'] += len(raw)
                save(window['entry'][2:]+'.bin',raw)
                extracted.append((window,raw,offset))
        save('extraction.json',dict(header_hex=header.hex(),load_commands_sha256=sha(commands),segment=plan['header']['text'],ranges=[dict(entry=w['entry'],start=w['start'],end_exclusive=w['end_exclusive'],bytes=len(raw),file_offset=offset,sha256=sha(raw)) for w,raw,offset in extracted],total_bytes=320,branch_global_slot_expansion=False))
        old = Path(plan['old_prefix_identity_actual_capture_only']['path']).read_bytes()
        require(len(old) == 240 and sha(old) == plan['old_prefix_identity_actual_capture_only']['sha256'], 'retained old prefix identity')
        overlap = b''.join(raw for w,raw,_ in extracted if w['entry'] in ['0x1022313c0','0x102231400'])
        require(len(overlap) == 208 and overlap == old[:208], 'exact historical208-byte overlap')
        save('old-prefix-comparison.json',dict(old_selected_bytes=240,old_decoded_bytes=47,old_opaque_bytes=193,new_selected_overlap_bytes=208,overlap_equal=True,potentially_newly_decoded_overlap_bytes=161,old_bytes_outside_selection=32,new_image_bytes=112,scope='Raw byte equality only; future row validation must separately succeed; old packet immutable.'))
        state['phase'] = 'three-static-decoders'
        for window, raw, _ in extracted:
            decode_one(plan,window,raw,state)
        require(state['decoder_children_started'] == 3 and state['decoder_attempts'] == 3 and state['validated_bytes'] == 320 and state['selected_bytes_read'] == 320, 'fixed capture totals')
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
        except (ValueError,KeyError,TypeError,struct.error):
            negatives.append(name)
            return
        raise ValueError('negative accepted: '+name)
    bad_pin = copy.deepcopy(plan['providers'][0]); bad_pin['sha256'] = '0'*64
    rejected('corrupt retained provider pin',lambda:verify_pin(bad_pin))
    for name,key,value in [('wrong start','start','0x101ad08a1'),('range extension','end_exclusive','0x101ad0911'),('wrong file offset','file_offset',28117153),('wrong byte cap','bytes',113)]:
        broken = copy.deepcopy(plan); broken['ranges'][0][key] = value
        rejected(name,lambda broken=broken:validate_ranges(broken))
    broken = copy.deepcopy(plan); broken['ranges'].append(copy.deepcopy(broken['ranges'][0]))
    rejected('fourth range',lambda:validate_ranges(broken))
    broken = copy.deepcopy(plan); broken['ranges'].reverse()
    rejected('range reorder',lambda:validate_ranges(broken))
    window = dict(start='0x101ad08a1',end_exclusive='0x101ad08b4',bytes=19)
    raw = bytes(range(19))
    synthetic = [dict(offset=int(window['start'],16)+offset,size=size,bytes=raw[offset:offset+size].hex(),opcode='synthetic-data',type='synthetic') for offset,size in [(0,1),(1,3),(4,15)]]
    validate_rows(synthetic,raw,window)
    rejected('missing row or tail',lambda:validate_rows(synthetic[:-1],raw,window))
    rejected('empty rows',lambda:validate_rows([],raw,window))
    rejected('nonobject row',lambda:validate_rows([1],raw,window))
    for name,key,value in [('gap','offset',int(window['start'],16)+1),('bool offset','offset',True),('zero size','size',0),('oversized instruction','size',16),('bool size','size',True),('wrong row bytes','bytes','ff'),('hex whitespace','bytes',' 0'),('invalid hex','bytes','zz'),('empty opcode','opcode',''),('invalid opcode','opcode','invalid'),('invalid parenthesized opcode','opcode','(invalid)'),('illegal type','type','ill'),('missing type','type',None)]:
        altered = copy.deepcopy(synthetic); altered[0][key] = value
        rejected(name,lambda altered=altered:validate_rows(altered,raw,window))
    altered = copy.deepcopy(synthetic); altered[1]['offset'] -= 1
    rejected('overlap',lambda:validate_rows(altered,raw,window))
    altered = copy.deepcopy(synthetic); altered[-1]['size'] = 16
    rejected('cross-end row or EOF padding',lambda:validate_rows(altered,raw,window))
    rejected('raw truncation',lambda:validate_rows(synthetic,raw[:-1],window))
    rejected('raw extra byte',lambda:validate_rows(synthetic,raw+b'\x00',window))
    command = struct.pack('<II16sQQQQiiII',0x19,72,b'__TEXT',4294967296,111357952,0,111357952,5,5,0,0)
    maps = segments(command,1)
    selected = plan['ranges'][0]
    expected = plan['header']['text']
    require(mapped_offset(selected,maps,expected,plan['image']['bytes']) == selected['file_offset'],'synthetic mapping')
    rejected('ambiguous mapping',lambda:mapped_offset(selected,maps+maps,expected,plan['image']['bytes']))
    rejected('truncated load command',lambda:segments(command[:-1],1))
    shifted = copy.deepcopy(maps); shifted[0]['fileoff'] = 1
    rejected('changed file mapping',lambda:mapped_offset(selected,shifted,expected,plan['image']['bytes']))
    rejected('image file bound',lambda:mapped_offset(selected,maps,expected,1))
    require(not DEST.exists(), 'no actual destination during preparation check')
    print(json.dumps(dict(status='pass-preparation-data-only',selection_sha256=SELECTION_SHA,ranges=3,selected_bytes=320,instruction_size_range=[1,15],synthetic_positive='odd address and consecutive1/3/15-byte rows cover19 synthetic bytes',provider_pins_checked=len(plan['providers']),synthetic_negative_controls=negatives,image_or_tool_files_read=False,old_prefix_payload_read=False,selected_image_windows_read=0,decoder_children_started=0,original_calls=0,all_six_bridges='U',application_outcomes_U=38,limits='Synthetic validator and retained metadata only; command help is syntax evidence, no target decode/startup/cleanup test or readiness approval.'),indent=2))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        raise SystemExit(check())
    if sys.argv[1:] != ['--capture-selected-once',SELECTION_SHA]:
        raise SystemExit('Use --check, or separately selected --capture-selected-once with the exact frozen selection digest; no retries or overrides.')
    raise SystemExit(capture(selection()))
