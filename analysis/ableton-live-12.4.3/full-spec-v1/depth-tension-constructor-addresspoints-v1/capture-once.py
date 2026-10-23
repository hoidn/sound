"""Fixed 336-byte static capture; no native execution or analysis/emulation."""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DEST = HERE / 'capture'
RANGES = [('0x1c84', '0x1d6c', 7300, 232, 58),
          ('0x15860', '0x158c4', 88160, 100, 25),
          ('0x1e04', '0x1e08', 7684, 4, 1)]
IMAGE = {'path':'/var/tmp/sound-analysis/helpers/Tension/Tension.arm64',
         'bytes':449696,'sha256':'640700be76a61a782977f8ede5aba32e9b2f287740d7815780b29464e5b424be'}
TOOL = {'path':'/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin',
        'bytes':59344432,'sha256':'ab5614cf137608cffc5a3f4f471a91c995cfa7c0c35465bfb73876e5b95561ba'}

def require(value, message):
    if not value:
        raise ValueError(message)

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def identity(path):
    path=Path(path)
    digest=hashlib.sha256(); count=0
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):
            digest.update(block); count+=len(block)
    return {'path':str(path),'bytes':count,'sha256':digest.hexdigest()}

def verify(pin):
    found=identity(pin['path'])
    require(found==pin,'identity mismatch: '+pin['path'])
    return found

def save(name, data):
    if not isinstance(data,bytes):
        data=(json.dumps(data,indent=2,allow_nan=False)+'\n').encode()
    with (DEST/name).open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())

def validate_plan(plan):
    require(plan['image']==IMAGE and plan['tool']==TOOL,'fixed image/tool')
    require(plan['ranges']==[dict(start=s,end_exclusive=e,file_offset=o,bytes=n,words=w)
                            for s,e,o,n,w in RANGES],'exact three ranges')
    require(plan['selected_bytes']==336 and plan['selected_words']==84,'fixed aggregate')
    require(plan['decoder_children_max']==3 and plan['timeout_seconds']==30,'fixed process bounds')
    require(plan['automatic_retry'] is False and plan['native_execution'] is False,'fixed no retry/static policy')
    for r in plan['ranges']:
        require(int(r['end_exclusive'],16)-int(r['start'],16)==r['bytes']==4*r['words'],'word range')
        require(r['file_offset']==int(r['start'],16) and r['file_offset']+r['bytes']<=IMAGE['bytes'],'retained section mapping')

def validate_rows(rows, raw, window):
    require(isinstance(rows,list) and len(rows)==window['words'],'exact row count')
    require(len(raw)==window['bytes'],'exact raw length')
    for i,row in enumerate(rows):
        require(isinstance(row,dict),'row object')
        require(type(row.get('offset')) is int and row['offset']==int(window['start'],16)+4*i,'consecutive address')
        require(type(row.get('size')) is int and row['size']==4,'four-byte word')
        encoded=row.get('bytes')
        require(isinstance(encoded,str) and len(encoded)==8 and all(c in '0123456789abcdefABCDEF' for c in encoded),'four-byte hex')
        require(bytes.fromhex(encoded)==raw[4*i:4*i+4],'raw encoding association')
        require(isinstance(row.get('opcode'),str) and row['opcode'].strip().lower() not in ['', 'invalid', '(invalid)', 'ill'],'valid opcode')
        require(isinstance(row.get('type'),str) and row['type'].strip().lower() not in ['', 'invalid', 'ill'],'valid type')

def argv(window):
    return [TOOL['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little',
            '-m',window['start'],'-s',window['start'],'-q','-c','pdj '+str(window['words']),
            str(DEST/(window['start'][2:]+'.bin'))]

def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def cleanup(child):
    try:
        os.killpg(child.pid,signal.SIGKILL)
        return 'process-group-SIGKILL-sent'
    except ProcessLookupError:
        return 'process-group-already-gone'

def decode(window, raw, state):
    name=window['start'][2:]; child=None; out=b''; err=b''; failure=None
    receipt={'argv':argv(window),'started_utc':utc(),'pid':None,'exit_code':None,
             'timeout_seconds':30,'timed_out':False,'cleanup':None,'error':None,
             'stdin':'DEVNULL','environment':{'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'},
             'core_limit_bytes':0,'new_process_session':True}
    save(name+'.invocation-before.json',receipt)
    try:
        state['attempts']+=1
        child=subprocess.Popen(receipt['argv'],cwd=DEST,stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                               env=receipt['environment'],start_new_session=True,preexec_fn=limits)
        receipt['pid']=child.pid; state['children_started']+=1
        save(name+'.pid.json',{'pid':child.pid,'pgid':child.pid,'spawned_utc':utc(),'argv':receipt['argv']})
        try:
            out,err=child.communicate(timeout=30)
        except subprocess.TimeoutExpired as ex:
            receipt['timed_out']=True; out=ex.output or b''; err=ex.stderr or b''
            raise
    except BaseException as ex:
        failure=ex; receipt['error']=type(ex).__name__+': '+str(ex)
    finally:
        if child is not None:
            receipt['cleanup']=cleanup(child)
            try:
                out,err=child.communicate(timeout=5)
            except subprocess.TimeoutExpired as ex:
                out=ex.output or out; err=ex.stderr or err
                failure=ex; receipt['error']='TimeoutExpired during process/pipe cleanup'
                child.stdout.close(); child.stderr.close()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired as ex:
                    failure=ex; receipt['error']='TimeoutExpired waiting after process-group cleanup'
            receipt['exit_code']=child.returncode
        receipt['finished_utc']=utc()
        save(name+'.stdout.json',out); save(name+'.stderr',err)
        save(name+'.invocation-after.json',receipt)
    if failure is not None:
        raise failure
    require(receipt['exit_code']==0 and not err,'decoder status/stderr')
    rows=json.loads(out,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
    validate_rows(rows,raw,window)
    state['validated_words']+=len(rows)
    state['validated_bytes']+=len(raw)

def capture(digest):
    require(sys.dont_write_bytecode,'use python3 -B')
    data=(HERE/'pre-call-manifest.json').read_bytes()
    require(sha(data)==digest,'exact pre-call manifest digest')
    plan=json.loads(data); validate_plan(plan)
    DEST.mkdir()  # Exclusive attempt tree; success and failure both forbid reuse.
    state={'started_utc':utc(),'outer_pid':os.getpid(),'argv':sys.argv,
           'pre_call_manifest_sha256':digest,'attempts':0,'children_started':0,
           'selected_bytes_read':0,'validated_words':0,'validated_bytes':0,
           'automatic_retry':False,'native_original_instruction_execution':0,
           'phase':'custody-before','error':None}
    save('attempt.json',state)
    watch=[IMAGE,TOOL,*plan['pins'],{'path':str(HERE/'pre-call-manifest.json'),'bytes':len(data),'sha256':digest}]
    before=[]; after=[]
    old_term=signal.getsignal(signal.SIGTERM)
    def interrupted(signum,frame):
        raise RuntimeError('interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted)
    try:
        for pin in watch:
            before.append(verify(pin))
        save('before-identities.json',before)
        state['phase']='exact-three-extractions'
        extracted=[]
        with Path(IMAGE['path']).open('rb') as stream:
            for window in plan['ranges']:
                stream.seek(window['file_offset']); raw=stream.read(window['bytes'])
                require(len(raw)==window['bytes'],'complete selected range')
                save(window['start'][2:]+'.bin',raw)
                state['selected_bytes_read']+=len(raw); extracted.append((window,raw))
        save('extraction.json',{'ranges':[{**w,'sha256':sha(raw)} for w,raw in extracted],
             'total_bytes':336,'mapping':'retained H4 section metadata only; no fresh header/LC reads',
             'whole_image_hash_reads':'custody only, separate from selected content'})
        for window,raw in extracted:
            state['phase']='decoder-'+window['start']
            decode(window,raw,state)
        require(state['attempts']==state['children_started']==3 and state['validated_words']==84
                and state['selected_bytes_read']==state['validated_bytes']==336,'complete fixed capture')
        state['phase']='captured-all84-rows-no-automatic-semantic-conclusion'
    except BaseException as ex:
        state['error']=type(ex).__name__+': '+str(ex)
        save('failure.json',{'utc':utc(),'phase':state['phase'],'error':state['error'],'partial_files_retained':True,'retry':False})
    finally:
        for pin in watch:
            try:
                after.append(identity(pin['path']))
            except Exception as ex:
                after.append({'path':pin['path'],'error':type(ex).__name__+': '+str(ex)})
        state['watch_unchanged']=bool(before) and before==after
        if not state['watch_unchanged'] and state['error'] is None:
            state['error']='custody mismatch/incomplete before-after records'
            save('failure.json',{'utc':utc(),'phase':state['phase'],'error':state['error'],'partial_files_retained':True,'retry':False})
        save('after-identities.json',{'files':after,'unchanged':state['watch_unchanged']})
        state['finished_utc']=utc(); save('status.json',state)
        signal.signal(signal.SIGTERM,old_term)
    print(json.dumps(state,indent=2))
    return 0 if state['error'] is None and state['watch_unchanged'] else 1

def self_check():
    window=dict(start='0x1c84',end_exclusive='0x1d6c',file_offset=7300,bytes=232,words=58)
    raw=bytes(range(232))
    rows=[dict(offset=7300+4*i,size=4,bytes=raw[4*i:4*i+4].hex(),opcode='synthetic',type='synthetic') for i in range(58)]
    validate_rows(rows,raw,window)
    rejected=[]
    def reject(name,action):
        try:
            action()
        except (ValueError,KeyError,TypeError):
            rejected.append(name); return
        raise ValueError('negative control accepted: '+name)
    reject('missing final word',lambda:validate_rows(rows[:-1],raw,window))
    reject('truncated raw',lambda:validate_rows(rows,raw[:-1],window))
    for name,key,value in [('address gap','offset',7304),('bool address','offset',True),
                           ('wrong size','size',8),('bool size','size',True),
                           ('mismatched raw','bytes','ffffffff'),('bad hex','bytes','zzzzzzzz'),
                           ('invalid instruction','opcode','invalid'),('illegal type','type','ill')]:
        bad=copy.deepcopy(rows); bad[0][key]=value
        reject(name,lambda bad=bad:validate_rows(bad,raw,window))
    plan={'image':IMAGE,'tool':TOOL,'ranges':[dict(start=s,end_exclusive=e,file_offset=o,bytes=n,words=w)
                                           for s,e,o,n,w in RANGES],
          'selected_bytes':336,'selected_words':84,'decoder_children_max':3,'timeout_seconds':30,
          'automatic_retry':False,'native_execution':False}
    validate_plan(plan)
    for name,change in [('fourth range',lambda p:p['ranges'].append(copy.deepcopy(p['ranges'][0]))),
                        ('range extension',lambda p:p['ranges'][0].__setitem__('bytes',236)),
                        ('wrong image identity',lambda p:p.__setitem__('image',{})),
                        ('retry prohibited',lambda p:p.__setitem__('automatic_retry',True))]:
        bad=copy.deepcopy(plan); change(bad)
        reject(name,lambda bad=bad:validate_plan(bad))
    require(argv(window)[-2]=='pdj 58','fixed ARM command shape')
    print(json.dumps({'status':'PASS-data-only','synthetic_positive_words':58,'negative_controls':rejected,
                      'image_or_tool_bytes_read':0,'decoder_children':0,'original_calls':0},indent=2))
    return 0

if __name__=='__main__':
    if sys.argv[1:]==['--self-check']:
        raise SystemExit(self_check())
    if len(sys.argv)==3 and sys.argv[1]=='--capture-once':
        raise SystemExit(capture(sys.argv[2]))
    raise SystemExit('Use --self-check or separately selected --capture-once PRE_CALL_SHA; no retries.')
