#!/usr/bin/env python3
"""Fixed eight-mode recording only. No build, old import, debugger or model construction."""
import copy
import ctypes
from datetime import datetime, timezone
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

HERE = Path(__file__).resolve().parent
INIT = '0x101bc1360'
TARGET = '0x101bb27b0'
MODES = (1, 2, 3, 4, 6, 7, 8, 9)
OLD = {1: (1,), 2: (65, 70), 3: (1, 8), 4: (0, 1, 7),
       6: (1, 64), 7: (0, 64, 65, 127), 8: (1, 65), 9: (1, 64)}
USES = {'__Znwm': 2, '___cxa_atexit': 3, '_pthread_key_create': 1}
HEADER = 'loaded rebases=789951 binds-linux=103 binds-trap=42781 symbols=1882'

def now():
    return datetime.now(timezone.utc).isoformat()

def identity(path):
    p = Path(path)
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return {'path': str(p.resolve()), 'bytes': p.stat().st_size, 'sha256': h.hexdigest()}

def save(path, data):
    with Path(path).open('w') as f:
        json.dump(data, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def oracle(mode, v):
    # Literal REQ005 integer table at the one selected exact dyadic state; no fitted model.
    a = lambda k: (1, 2, 3, 4, 5, 8, 10, 20, 50)[k-1] if 1 <= k <= 9 else 20
    b = lambda k: (1, 2, 3, 4, 5, 8, 20, 50)[k-1] if 1 <= k <= 8 else 50
    if mode == 1: d = a(v) if v <= 64 else -a(v-64)
    elif mode == 2: d = b(v-64) if v >= 64 else -b(64-v)
    elif mode == 3: d = b(v) if v <= 65 else -b(128-v)
    elif mode == 4: d = -b(v) if v <= 64 else b(v-64)
    elif mode == 6: d = v if v <= 64 else -(v-64)
    elif mode == 7: d = v-64
    elif mode == 8: d = v if v <= 64 else v-128
    elif mode == 9: d = -v if v <= 64 else v-64
    else: raise AssertionError('not a selected mode')
    value = .5 + d/256
    assert .25 <= value <= .75
    return d, f'{struct.unpack("<I", struct.pack("<f", value))[0]:08x}'

def tokens(row):
    return ['call', TARGET, 'f:0x1.0000000000000p-1', 'd:0x1.0000000000000p-7',
            'hex:' + row['buffer_le'], 'i:0', 'i:0']

def validate(data):
    assert data['schema'] == 'whole-midi-relative-byte-inputs-v1'
    assert data['counts'] == {'logical': 1024, 'inherited': 18, 'fresh_targets': 1006,
                              'initializers': 8, 'original_calls': 1014, 'children': 8}
    assert data['unit'] == {'current_bits32': '3f000000', 'range_packed_bits64': '3f80000000000000',
                            'prior_bits32': '7f7fffff', 'sensitivity_bits32': '3f800000',
                            'quantized': 0, 'reversed': 0}
    rows = data['rows']
    assert [(r['mode'], r['byte']) for r in rows] == [(m,v) for m in MODES for v in range(128)]
    assert len({r['id'] for r in rows}) == 1024
    for r in rows:
        m,v = r['mode'],r['byte']
        assert r['id'] == f'MR{m:02d}-{v:03d}'
        assert r['buffer_le'] == struct.pack('<fIif', v, 0x7f7fffff, m, 1).hex()
        assert r['oracle_class'] == 'current-REQ005-exact-dyadic-binary32'
        delta,bits = oracle(m,v)
        assert (r['delta_integer'],r['expected_low_xmm0_bits32']) == (delta,bits)
        assert r['provenance'] == ('inherited-X1' if v in OLD[m] else 'fresh-selected')
        assert (r['historical'] is not None) == (v in OLD[m])
    plans = data['plans']
    assert [p['mode'] for p in plans] == list(MODES)
    for p in plans:
        selected = [r for r in rows if r['mode'] == p['mode'] and r['provenance'] == 'fresh-selected']
        assert p['row_ids'] == [r['id'] for r in selected]
        assert p['tokens'] == ['call',INIT] + [t for r in selected for t in tokens(r)]
        assert p['calls'] == 1 + len(selected) <= 128
        assert p['buffers'] == len(selected) <= 127
    return True

def parser_bits():
    # Host libc entry used by the unchanged loader, no original-program execution.
    libc = ctypes.CDLL(None)
    libc.strtod.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    libc.strtod.restype = ctypes.c_double
    out = []
    for token,expected in [('f:0x1.0000000000000p-1','0000003f'),
                           ('d:0x1.0000000000000p-7','000000000000803f')]:
        raw = token[2:].encode()
        buf = ctypes.create_string_buffer(raw)
        end = ctypes.c_void_p()
        value = libc.strtod(buf,ctypes.byref(end))
        temporary = struct.pack('<f',value)
        actual = temporary if token[0] == 'f' else struct.pack('<d',value)
        assert end.value-ctypes.addressof(buf) == len(raw) and actual.hex() == expected
        out.append({'token':token,'strtod_bits64_le':struct.pack('<d',value).hex(),
                    'temporary_float_bits32_le':temporary.hex(),'actual_argument_le':actual.hex()})
    return out

def input_controls(data):
    negatives = [
        ('missing-final-byte',lambda d:d['rows'].pop()),
        ('wrong-mode-set',lambda d:d['rows'][0].update(mode=0)),
        ('duplicate-input',lambda d:d['rows'][1].update(byte=0)),
        ('wrong-endian-record',lambda d:d['rows'][0].update(buffer_le=d['rows'][0]['buffer_le'][::-1])),
        ('wrong-prior',lambda d:d['unit'].update(prior_bits32='00000000')),
        ('new-state-axis',lambda d:d['unit'].update(quantized=1)),
        ('altered-oracle-bit',lambda d:d['rows'][0].update(expected_low_xmm0_bits32='00000000')),
        ('historical-row-replayed',lambda d:d['plans'][0]['row_ids'].append('MR01-001')),
        ('historical-promoted-fresh',lambda d:d['rows'][1].update(provenance='fresh-selected')),
        ('wrong-init-address',lambda d:d['plans'][0]['tokens'].__setitem__(1,'0x0')),
        ('wrong-target-address',lambda d:d['plans'][0]['tokens'].__setitem__(3,'0x0')),
        ('missing-mode-child',lambda d:d['plans'].pop()),
        ('firstN-count',lambda d:d['counts'].update(fresh_targets=6)),
        ('unsafe-buffer-count',lambda d:d['plans'][0].update(buffers=257))]
    passed=[]
    for name,change in negatives:
        d=copy.deepcopy(data);change(d)
        try:validate(d)
        except AssertionError:passed.append(name)
        else:raise AssertionError('negative accepted '+name)
    return passed

def parse_output(text, stderr, rc, plan, row_by_id):
    assert rc == 0 and stderr == ''
    lines=text.splitlines();assert lines[0] == HEADER
    imports=[];calls=[];buffers=[];used={}
    for line in lines[1:]:
        if line.startswith('import '):
            m=re.fullmatch(r'import (linux-data|linux|trap) (\S+) slots=(\d+)',line);assert m
            imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
        elif line.startswith('call '):
            m=re.fullmatch(r'call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)',line);assert m
            calls.append({'index':int(m[1]),'address':m[2],**{k:f'{int(v,16):016x}' for k,v in zip(('rax','rdx','xmm0','xmm1'),m.groups()[2:])}})
        elif line.startswith('out '):
            m=re.fullmatch(r'out b(\d+) (0x[0-9a-f]+) ([0-9a-f]{32})',line);assert m
            buffers.append({'index':int(m[1]),'address':m[2],'bytes_le':m[3]})
        elif line.startswith('used '):
            m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1] not in used
            used[m[1]]=int(m[2])
        else:raise AssertionError('unexpected output '+line)
    assert len(imports)==1882 and len({i['symbol'] for i in imports})==1882
    assert sum(i['kind']=='linux-data' for i in imports)==1
    assert used==USES
    assert len(calls)==plan['calls'] and [c['index'] for c in calls]==list(range(plan['calls']))
    assert calls[0]['address']==INIT and all(c['address']==TARGET for c in calls[1:])
    assert len(buffers)==plan['buffers'] and [b['index'] for b in buffers]==list(range(plan['buffers']))
    assert len({b['address'] for b in buffers})==len(buffers)
    for rid,c,b in zip(plan['row_ids'],calls[1:],buffers):
        r=row_by_id[rid]
        assert b['bytes_le']==r['buffer_le']
        c.update(row_id=rid,low_xmm0_bits32=c['xmm0'][-8:],expected=r['expected_low_xmm0_bits32'])
        c['oracle_agrees']=c['low_xmm0_bits32']==c['expected']
    return {'imports':imports,'calls':calls,'buffers':buffers,'used':used,
            'oracle_mismatches':[c['row_id'] for c in calls[1:] if not c['oracle_agrees']]}

def custody(context):
    result=[]
    freeze=json.loads((HERE/'manifest-before.json').read_text())
    for pin in context['watched'] + freeze['frozen_files']:
        actual=identity(pin['path']);assert actual==pin,pin['path'];result.append(actual)
    return result

def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_CPU,(20,20))
    resource.setrlimit(resource.RLIMIT_FSIZE,(4*1048576,4*1048576))

def main():
    data=json.loads((HERE/'inputs.json').read_text());validate(data)
    negatives=input_controls(data);parsed=parser_bits()
    if sys.argv[1:]==['--check-inputs']:
        print(json.dumps({'status':'PASS','logical':1024,'fresh':1006,'inherited':18,'negative_controls':negatives,
                          'parser_checks':parsed,'original_calls':0,'binary_reads':0}));return
    assert sys.argv[1:]==['--run-once']
    context=json.loads((HERE/'context.json').read_text())
    freeze=json.loads((HERE/'manifest-before.json').read_text())
    for pin in freeze['frozen_files']:
        assert identity(pin['path'])==pin
    attempts=HERE/'attempts';attempts.mkdir(exist_ok=False)
    result={'schema':'midi-relative-bytes-actual-v1','status':'RUNNING','outer_pid':os.getpid(),
            'outer_argv':sys.argv,'utc_start':now(),'children':[],'error':None,
            'input_controls':negatives,'host_parser':parsed,'phases':{'inputs_validated':True,'custody_before':False,
              'calls_started':False,'all_children_completed':False,'custody_after':False}}
    save(HERE/'results.json',result)
    def terminated(signum,frame):
        raise RuntimeError('outer received signal '+str(signum))
    signal.signal(signal.SIGTERM,terminated)
    try:
        result['custody_before']=custody(context);result['phases']['custody_before']=True
        byid={r['id']:r for r in data['rows']}
        for plan in data['plans']:
            directory=attempts/f'mode-{plan["mode"]}';directory.mkdir()
            argv=[context['loader'],context['image'],'--imports']+plan['tokens']
            child={'mode':plan['mode'],'argv':argv,'pid':None,'utc_start':now(),'exit':None,'timeout':False,
                   'cleanup':None,'status':'PREPARED','expected_calls':plan['calls'],'expected_buffers':plan['buffers']}
            result['children'].append(child);save(HERE/'results.json',result)
            p=None;started=time.monotonic()
            try:
                with (directory/'stdout.txt').open('xb') as out,(directory/'stderr.txt').open('xb') as err:
                    p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,cwd=HERE,
                                       env=context['environment'],preexec_fn=limits,start_new_session=True)
                    child['pid']=p.pid;child['status']='RUNNING';result['phases']['calls_started']=True
                    save(HERE/'results.json',result)
                    try:child['exit']=p.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        child['timeout']=True;os.killpg(p.pid,signal.SIGKILL);child['exit']=p.wait(timeout=5)
                        child['cleanup']='selected process group SIGKILL; direct child reaped'
            finally:
                if p is not None and p.poll() is None:
                    os.killpg(p.pid,signal.SIGKILL);child['exit']=p.wait(timeout=5)
                    child['cleanup']='selected group killed and direct child reaped after interruption'
                child.update(utc_end=now(),elapsed_seconds=time.monotonic()-started)
                for name in ('stdout','stderr'):
                    f=directory/(name+'.txt')
                    if f.exists():child[name]=identity(f)
                save(HERE/'results.json',result)
            assert not child['timeout']
            child['parsed']=parse_output((directory/'stdout.txt').read_text(),(directory/'stderr.txt').read_text(),child['exit'],plan,byid)
            child['status']='RECORDED'
            save(HERE/'results.json',result)
            assert not child['parsed']['oracle_mismatches'],'oracle discrepancy: retained; later children stopped'
            child['custody_after']=custody(context)
            assert child['custody_after']==result['custody_before']
            save(HERE/'results.json',result)
            print(f'mode {plan["mode"]}: {plan["calls"]} calls, {plan["buffers"]} target returns, all agree',flush=True)
        result['phases']['all_children_completed']=True
        result['custody_after']=result['children'][-1]['custody_after']
        assert result['custody_before']==result['custody_after']
        result['phases']['custody_after']=True;result['status']='COMPLETE-ONE-ATTEMPT-PER-MODE'
    except BaseException as error:
        result['status']='STOPPED-NO-RETRY';result['error']={'type':type(error).__name__,'message':str(error)}
        try:result['custody_after_failure']=custody(context)
        except BaseException as e:result['custody_after_failure_error']=str(e)
        raise
    finally:
        result['utc_end']=now();save(HERE/'results.json',result)

if __name__=='__main__':main()
