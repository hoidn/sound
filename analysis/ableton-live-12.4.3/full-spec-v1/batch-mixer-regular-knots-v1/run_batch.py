#!/usr/bin/env python3
"""Fixed seven-helper scalar recording. No build, old imports, patches, objects or oracle fitting."""
import copy
import ctypes
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import struct
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent
FUNCTIONS=('0x101b1a470','0x101b1a550','0x101b1a630','0x101b1a6f0','0x101b1a7b0','0x101b1a880','0x101b1a8e0')
OLD={-64,-60,-48,-32,-16,0,16,32,48,60,64}
HEADER='loaded rebases=789951 binds-linux=103 binds-trap=42781 symbols=1882'
def now():return datetime.now(timezone.utc).isoformat()
def identity(p):
    p=Path(p);h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
def save(p,d):
    with Path(p).open('w') as f:
        json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def validate(d):
    assert d['schema']=='whole-mixer-129-regular-knots-v1'
    assert d['counts']=={'logical':903,'inherited':77,'fresh_targets':826,'children':7,'calls_per_child':118,'buffers':0,'initializers':0}
    rows=d['rows'];assert [(r['curve'],r['k']) for r in rows]==[(c,k) for c in range(7) for k in range(-64,65)]
    assert len({r['id'] for r in rows})==903 and [p['curve'] for p in d['plans']]==list(range(7))
    for r in rows:
        assert r['id']==f'MK{r["curve"]}-{r["k"]+64:03d}' and r['function']==FUNCTIONS[r['curve']]
        value=r['k']/64;bits=f'{struct.unpack("<I",struct.pack("<f",value))[0]:08x}'
        assert r['token']=='f:'+value.hex() and r['input_bits32']==bits
        old=r['k'] in OLD;assert r['provenance']==('inherited-approved' if old else 'fresh-selected')
        assert (r['historical'] is not None)==old
        if old:assert r['expected_bits32']==r['historical']['bits32'] and r['oracle_class']=='inherited-reference-bits'
        else:assert r['expected_bits32'] is None and r['oracle_class']=='NULL-discovery-regular-node'
    for p in d['plans']:
        selected=[r for r in rows if r['curve']==p['curve'] and r['provenance']=='fresh-selected']
        assert len(selected)==118 and p['row_ids']==[r['id'] for r in selected]
        assert p['tokens']==[t for r in selected for t in ('call',r['function'],r['token'])]
def parser_bits(rows):
    libc=ctypes.CDLL(None);libc.strtod.argtypes=[ctypes.c_char_p,ctypes.POINTER(ctypes.c_void_p)];libc.strtod.restype=ctypes.c_double
    out=[]
    for r in rows:
        raw=r['token'][2:].encode();b=ctypes.create_string_buffer(raw);end=ctypes.c_void_p();v=libc.strtod(b,ctypes.byref(end));f=struct.pack('<f',v)
        assert end.value-ctypes.addressof(b)==len(raw) and f[::-1].hex()==r['input_bits32']
        out.append({'id':r['id'],'token':r['token'],'parsed_bits64_le':struct.pack('<d',v).hex(),'argument_bits32_le':f.hex()})
    return out
def input_controls(d):
    changes=[('omit-node',lambda x:x['rows'].pop()),('duplicate-node',lambda x:x['rows'][1].update(k=-64)),('wrong-grid-token',lambda x:x['rows'][1].update(token='f:0.1')),('wrong-endian',lambda x:x['rows'][1].update(input_bits32=x['rows'][1]['input_bits32'][::-1])),('wrong-helper',lambda x:x['rows'][1].update(function='0x0')),('firstN-curve-cut',lambda x:x['plans'].pop()),('historical-replayed',lambda x:x['plans'][0]['row_ids'].append('MK0-064')),('new-oracle-invented',lambda x:x['rows'][1].update(expected_bits32='00000000')),('new-setup-call',lambda x:x['plans'][0]['tokens'].__setitem__(1,'0x101bc1360')),('patch-option',lambda x:x['plans'][0]['tokens'].insert(0,'--patch')),('wrong-count',lambda x:x['counts'].update(fresh_targets=1)),('non-null-control-history',lambda x:x['rows'][0].update(historical=None))]
    passed=[]
    for label,change in changes:
        altered=copy.deepcopy(d);change(altered)
        try:validate(altered)
        except (AssertionError,IndexError,KeyError):passed.append(label)
        else:raise AssertionError('negative accepted '+label)
    return passed
def parse_output(text,stderr,rc,plan,byid):
    assert rc==0 and stderr=='';lines=text.splitlines();assert lines[0]==HEADER
    imports=[];calls=[];used={}
    for line in lines[1:]:
        if line.startswith('import '):
            m=re.fullmatch(r'import (linux-data|linux|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
        elif line.startswith('call '):
            m=re.fullmatch(r'call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)',line);assert m
            calls.append({'index':int(m[1]),'function':m[2],**{k:f'{int(v,16):016x}' for k,v in zip(('rax','rdx','xmm0','xmm1'),m.groups()[2:])}})
        elif line.startswith('used '):
            m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1] not in used;used[m[1]]=int(m[2])
        else:raise AssertionError('Unexpected line '+line)
    assert len(imports)==1882 and len({r['symbol'] for r in imports})==1882
    assert sum(r['kind']=='linux-data' for r in imports)==1
    assert set(used)<={'_cos','_cosf'} and all(v>0 for v in used.values())
    assert len(calls)==118 and [c['index'] for c in calls]==list(range(118))
    for c,rid in zip(calls,plan['row_ids']):
        r=byid[rid];assert c['function']==r['function'];c.update(row_id=rid,low_xmm0_bits32=c['xmm0'][-8:],precall_expected=None)
    return {'imports':imports,'calls':calls,'used':used}
def custody(ctx):
    freeze=json.loads((HERE/'manifest-before.json').read_text());out=[]
    for pin in ctx['watched']+freeze['frozen_files']:
        actual=identity(pin['path']);assert actual==pin,pin['path'];out.append(actual)
    return out
def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(20,20));resource.setrlimit(resource.RLIMIT_FSIZE,(4194304,4194304))
def main():
    d=json.loads((HERE/'inputs.json').read_text());validate(d);controls=input_controls(d);parser=parser_bits(d['rows'])
    if sys.argv[1:]==['--check-inputs']:
        print(json.dumps({'status':'PASS','input_controls':controls,'parser_rows':len(parser),'original_calls':0,'runtime_reads':0}));return
    assert sys.argv[1:]==['--run-once'];ctx=json.loads((HERE/'context.json').read_text());freeze=json.loads((HERE/'manifest-before.json').read_text())
    for pin in freeze['frozen_files']:assert identity(pin['path'])==pin
    attempts=HERE/'attempts';attempts.mkdir(exist_ok=False)
    result={'schema':'mixer-regular-knots-actual-v1','status':'RUNNING','utc_start':now(),'outer_pid':os.getpid(),'outer_argv':sys.argv,'input_controls':controls,'host_parser':parser,'children':[],'error':None,'phases':{'inputs_validated':True,'custody_before':False,'calls_started':False,'all_children_completed':False,'custody_after':False}}
    save(HERE/'results.json',result)
    def terminated(signum,frame):raise RuntimeError('outer received signal '+str(signum))
    signal.signal(signal.SIGTERM,terminated)
    try:
        result['custody_before']=custody(ctx);result['phases']['custody_before']=True;byid={r['id']:r for r in d['rows']}
        for plan in d['plans']:
            directory=attempts/f'curve-{plan["curve"]}';directory.mkdir();argv=[ctx['loader'],ctx['image'],'--imports']+plan['tokens']
            c={'curve':plan['curve'],'argv':argv,'utc_start':now(),'pid':None,'exit':None,'timeout':False,'cleanup':None,'status':'PREPARED'};result['children'].append(c);save(HERE/'results.json',result);p=None;started=time.monotonic()
            try:
                with (directory/'stdout.txt').open('xb') as out,(directory/'stderr.txt').open('xb') as err:
                    p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=HERE,env=ctx['environment'],preexec_fn=limits,start_new_session=True);c['pid']=p.pid;c['status']='RUNNING';result['phases']['calls_started']=True;save(HERE/'results.json',result)
                    try:c['exit']=p.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        c['timeout']=True;os.killpg(p.pid,signal.SIGKILL);c['exit']=p.wait(timeout=5);c['cleanup']='selected process group SIGKILL; direct child reaped'
            finally:
                if p is not None and p.poll() is None:
                    os.killpg(p.pid,signal.SIGKILL);c['exit']=p.wait(timeout=5);c['cleanup']='selected group killed/direct child reaped after interrupted wait'
                c.update(utc_end=now(),elapsed_seconds=time.monotonic()-started)
                for name in ('stdout','stderr'):
                    f=directory/(name+'.txt')
                    if f.exists():c[name]=identity(f)
                save(HERE/'results.json',result)
            assert not c['timeout'];c['parsed']=parse_output((directory/'stdout.txt').read_text(),(directory/'stderr.txt').read_text(),c['exit'],plan,byid);c['status']='RECORDED';save(HERE/'results.json',result)
            c['custody_after']=custody(ctx);assert c['custody_after']==result['custody_before'];save(HERE/'results.json',result)
            print(f'curve {plan["curve"]}:118 returns, used={c["parsed"]["used"]}',flush=True)
        result['phases']['all_children_completed']=True;result['custody_after']=result['children'][-1]['custody_after'];result['phases']['custody_after']=True;result['status']='COMPLETE-ONE-ATTEMPT-PER-CURVE'
    except BaseException as error:
        result['status']='STOPPED-NO-RETRY';result['error']={'type':type(error).__name__,'message':str(error)}
        try:result['custody_after_failure']=custody(ctx)
        except BaseException as e:result['custody_after_failure_error']=str(e)
        raise
    finally:result['utc_end']=now();save(HERE/'results.json',result)
if __name__=='__main__':main()
