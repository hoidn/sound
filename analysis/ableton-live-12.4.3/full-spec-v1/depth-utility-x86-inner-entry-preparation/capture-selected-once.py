"""One fixed x86_64 physical cap; no instruction execution. --check reads only preparation/source metadata."""
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
SELECTION_SHA = '2d5061a1175eecbae738198c5d8216143735e3e21964ea684c4c614f6126a595'
DEST = PRE.with_name('depth-utility-x86-inner-entry-native-v1')
RANGES = [('0x102247d20',352,35945760)]
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
    require([(r['entry'],r['bytes'],r['file_offset']) for r in ranges] == RANGES, 'exact one-entry selection')
    previous = None
    for r in ranges:
        start, end = int(r['start'],16), int(r['end_exclusive'],16)
        require(start == int(r['entry'],16) and end-start == r['bytes'] and r['bytes'] > 0, 'exact physical cap')
        require(previous is None or previous <= start, 'nonoverlapping ranges')
        require(r['file_offset'] == start-plan['header']['text']['vmaddr'], 'fixed physical mapping')
        previous = end
    require(sum(r['bytes'] for r in ranges) == plan['selected_physical_bytes'] == 352, 'fixed aggregate bytes')
    require(plan['architecture'] == 'x86_64' and plan['instruction_sizes_bytes'] == [1,15], 'fixed x86 architecture')
    require(plan['future_max_target_decoder_children'] == 1 and plan['future_timeout_seconds_per_child'] == TIMEOUT and plan['future_automatic_retry'] is False, 'fixed child limits')


def selected_bound(plan, retained):
    row = retained['rows'][3]['entry']
    window = plan['ranges'][0]
    require(row['previous_address'] == window['entry'] == '0x102247d20' and row['address'] == window['end_exclusive'] == '0x102247e80', 'exact reviewed previous/start pair')
    require(type(row['index']) is int and row['index'] == plan['bounds_basis']['end_ordinal'] == 153130 and row['index']-1 == plan['bounds_basis']['start_ordinal_derived'] == 153129, 'derived immediate previous ordinal')
    encoded = bytes.fromhex(row['uleb_hex'])
    require(encoded == b'\xe0\x02' and (encoded[0]&127)+128*encoded[1] == int(row['address'],16)-int(row['previous_address'],16) == window['bytes'] == 352, 'exact reviewed canonical ULEB delta and cap')
    require(row['slice_file_offset']-352 == window['file_offset'] == 35945760, 'derived selected file offset')
    require(row['uleb_blob_offset'] == 215406 and row['uleb_file_offset'] == retained['header']['function_starts']['dataoff']+215406 == 147771758, 'reviewed source witness locator')
    nomination = plan['target_nomination']
    raw = bytes.fromhex(nomination['raw_hex'])
    require(nomination['PC'] == '0x102247e85' and raw == b'\xe9\x96\xfe\xff\xff' and int(nomination['PC'],16)+5+int.from_bytes(raw[1:],'little',signed=True) == int(window['entry'],16) == int(nomination['raw_signed_target'],16), 'reviewed E9 raw signed target; ESIL excluded')


def metadata(plan):
    for pin in plan['providers']:
        verify_pin(pin)
    retained = json.loads(Path(plan['providers'][1]['path']).read_text())
    require(retained['header'] == plan['header'], 'retained exact header metadata')
    selected_bound(plan,retained)


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
        watched = sorted({Path(plan['image']['path']),Path(plan['tool']['path']),*[Path(x['path']) for x in plan['providers']],*[f for f in PRE.iterdir() if f.is_file()]})
        before = [identity(path) for path in watched]
        save('before-identities.json',before)
        for pin in [plan['image'],plan['tool'],*plan['providers']]:
            require(next(r for r in before if r['path'] == pin['path']) == pin, 'fresh image/tool/provider identity')
        state['phase'] = 'header-mapping-and-one-extraction'
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
        save('extraction.json',dict(header_hex=header.hex(),load_commands_sha256=sha(commands),segment=plan['header']['text'],ranges=[dict(entry=w['entry'],start=w['start'],end_exclusive=w['end_exclusive'],bytes=len(raw),file_offset=offset,sha256=sha(raw)) for w,raw,offset in extracted],total_bytes=352,branch_global_slot_expansion=False))
        state['phase'] = 'one-static-decoder'
        for window, raw, _ in extracted:
            decode_one(plan,window,raw,state)
        require(state['decoder_children_started'] == 1 and state['decoder_attempts'] == 1 and state['validated_bytes'] == 352 and state['selected_bytes_read'] == 352, 'fixed capture totals')
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
    for name,key,value in [('wrong start','start','0x102247d21'),('range extension','end_exclusive','0x102247e81'),('wrong file offset','file_offset',35945761),('wrong byte cap','bytes',353)]:
        broken = copy.deepcopy(plan); broken['ranges'][0][key] = value
        rejected(name,lambda broken=broken:validate_ranges(broken))
    broken = copy.deepcopy(plan); broken['ranges'].append(copy.deepcopy(broken['ranges'][0]))
    rejected('second range',lambda:validate_ranges(broken))
    retained = json.loads(Path(plan['providers'][1]['path']).read_text())
    for name,key,value in [('wrong previous start','previous_address','0x102247d21'),('wrong selected end','address','0x102247e81'),('wrong source ordinal','index',153131),('wrong ULEB cap','uleb_hex','e102'),('wrong derived file offset','slice_file_offset',35946113),('wrong witness locator','uleb_file_offset',147771759)]:
        altered = copy.deepcopy(retained); altered['rows'][3]['entry'][key] = value
        rejected(name,lambda altered=altered:selected_bound(plan,altered))
    altered = copy.deepcopy(plan); altered['target_nomination']['raw_hex'] = 'e995feffff'
    rejected('wrong raw E9 nomination',lambda:selected_bound(altered,retained))
    window = dict(start='0x102247d21',end_exclusive='0x102247d34',bytes=19)
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
    short_window = dict(window,end_exclusive=hex(int(window['end_exclusive'],16)-1),bytes=18)
    rejected('valid-size row crosses selected end',lambda:validate_rows(synthetic,raw[:18],short_window))
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
    print(json.dumps(dict(status='pass-preparation-data-only',selection_sha256=SELECTION_SHA,ranges=1,selected_bytes=352,instruction_size_range=[1,15],synthetic_positive='odd address and consecutive1/3/15-byte rows cover19 synthetic bytes',provider_pins_checked=len(plan['providers']),synthetic_negative_controls=negatives,image_or_tool_files_read=False,prior_code_payload_read=False,selected_image_windows_read=0,decoder_children_started=0,original_calls=0,all_six_bridges='U',application_outcomes_U=38,limits='Synthetic validator and retained metadata only; command help is syntax evidence, no target decode/startup/cleanup test or readiness approval.'),indent=2))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        raise SystemExit(check())
    if sys.argv[1:] != ['--capture-selected-once',SELECTION_SHA]:
        raise SystemExit('Use --check, or separately selected --capture-selected-once with the exact frozen selection digest; no retries or overrides.')
    raise SystemExit(capture(selection()))
