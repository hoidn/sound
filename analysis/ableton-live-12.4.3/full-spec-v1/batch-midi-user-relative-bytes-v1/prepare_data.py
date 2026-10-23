#!/usr/bin/env python3
"""One-shot stdlib input/provenance materialization. No original calls or old imports."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('owned_new_recorder',HERE/'run_batch.py')
R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)

def ident(p):return R.identity(p)
def write(n,d):
    assert not (HERE/n).exists(),n
    R.save(HERE/n,d)
def sha(b):return hashlib.sha256(b).hexdigest()

def span(path,first,last):
    p=ROOT/path;b=p.read_bytes();lines=b.splitlines(keepends=True)
    start=sum(map(len,lines[:first-1]));end=sum(map(len,lines[:last]))
    return {'source':ident(p),'lines_inclusive':[first,last],'offset':start,'bytes':end-start,
            'sha256':sha(b[start:end]),'text':b[start:end].decode()}

def main():
    assert sys.argv[1:]==['--prepare-data']
    result_path=ROOT/'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/results/midi.json'
    results=json.loads(result_path.read_text())
    old_cases=json.loads((ROOT/'handoff/midi-config-v3/cases.json').read_text())['cases']
    old_by_id={c['id']:c for c in old_cases}
    names={'AccelSignedBit':1,'AccelBinaryOffset':2,'AccelTwoCompliment':3,'AccelSignedBit2':4,
           'LinearSignedBit':6,'LinearBinaryOffset':7,'LinearTwoCompliment':8,'LinearSignedBit2':9}
    historical={}
    for ci,c in enumerate(results['cases']):
        if c['mode'] not in names:continue
        parameter=old_by_id[c['case']]['stimulus']['parameter']
        if (parameter['min'],parameter['max'],parameter['initial_value'],parameter['stepped'])!=(0,1,.5,False):continue
        current=parameter['initial_value']
        for i,(message,y) in enumerate(zip(c['messages'],c['x'])):
            mode=names[c['mode']];v=int(message.split()[2],16)
            if current==.5 and v in R.OLD[mode] and (mode,v) not in historical:
                historical[(mode,v)]={'path':str(result_path.relative_to(ROOT)),'pointer':f'/cases/{ci}/x/{i}',
                    'case':c['case'],'message_index':i,'message':message,
                    'case_object_sha256':sha(json.dumps(c,sort_keys=True,separators=(',',':')).encode()),
                    'bits32':f'{struct.unpack("<I",struct.pack("<f",y))[0]:08x}'}
            current=y
    assert set(historical)=={(m,v) for m in R.MODES for v in R.OLD[m]}
    rows=[]
    for m in R.MODES:
        for v in range(128):
            delta,bits=R.oracle(m,v)
            old=historical.get((m,v))
            if old:assert bits==old['bits32']
            rows.append({'id':f'MR{m:02d}-{v:03d}','mode':m,'byte':v,
                'buffer_le':struct.pack('<fIif',v,0x7f7fffff,m,1).hex(),
                'delta_integer':delta,'expected_low_xmm0_bits32':bits,
                'oracle_class':'current-REQ005-exact-dyadic-binary32',
                'provenance':'inherited-X1' if old else 'fresh-selected','historical':old})
    plans=[]
    for m in R.MODES:
        fresh=[r for r in rows if r['mode']==m and r['provenance']=='fresh-selected']
        plans.append({'mode':m,'row_ids':[r['id'] for r in fresh],
                      'tokens':['call',R.INIT]+[t for r in fresh for t in R.tokens(r)],
                      'calls':1+len(fresh),'buffers':len(fresh)})
    data={'schema':'whole-midi-relative-byte-inputs-v1','counts':{'logical':1024,'inherited':18,
        'fresh_targets':1006,'initializers':8,'original_calls':1014,'children':8},
        'unit':{'current_bits32':'3f000000','range_packed_bits64':'3f80000000000000',
                'prior_bits32':'7f7fffff','sensitivity_bits32':'3f800000','quantized':0,'reversed':0},
        'rows':rows,'plans':plans}
    R.validate(data);write('inputs.json',data)
    # Copy only the 18 selected exact old raw records; preserve original byte locators and absence of PID/UTC.
    raw_path=ROOT/'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/raw/runs.jsonl'
    selected=bytearray();controls=[];seen=set();offset=0
    with raw_path.open('rb') as f:
        for ordinal,line in enumerate(f,1):
            old=json.loads(line);a=old['argv'];candidate=None
            if len(a)==10 and a[1:5]==['call',R.INIT,'call',R.TARGET] and a[5:7]==['f:0x1.0000000000000p-1','d:0x1.0000000000000p-7'] and a[-2:]==['i:0','i:0']:
                v,prior,m,s=struct.unpack('<fIif',bytes.fromhex(a[7][4:]))
                if v==int(v) and (m,int(v)) in historical and prior==0x7f7fffff and s==1:
                    candidate=(m,int(v))
            if candidate is not None and candidate not in seen:
                seen.add(candidate);m,v=candidate
                controls.append({'mode':m,'byte':v,'original_path':str(raw_path.relative_to(ROOT)),
                    'original_row':ordinal,'original_offset':offset,'raw_bytes':len(line),'raw_sha256':sha(line),
                    'selected_offset':len(selected),'result_locator':historical[candidate],
                    'bits32':historical[candidate]['bits32'],'historical_pid':None,'historical_utc':None})
                selected.extend(line)
            offset+=len(line)
    assert seen==set(historical) and len(controls)==18
    with (HERE/'historical-controls.jsonl').open('xb') as f:f.write(selected);f.flush();os.fsync(f.fileno())
    write('inherited-controls.json',controls)
    # All source below is already retained tooling/contract text, not new original C/native acquisition.
    protocol={'method_spans':[span('analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/run_pilot.py',219,225),
               span('analysis/ableton-live-12.4.3/r2/x2-midi-v1/run_x2.py',507,523),
               span('tools/xexec/xexec.c',271,287),span('tools/xexec/xexec.c',330,385)],
               'owner_span':span('wiki/specs/midi-user-mapping.md',184,211),
               'old_raw_limits':'Original X1 records lack process PID/UTC; none fabricated. No new invocation of them.',
               'review':'handoff/midi-config-v4/REVIEW.md: old case expectations and 52-value scope reviewed; family review by citation, no repeat observation review.'}
    write('protocol-source.json',protocol)
    # Inert exact tooling copies let the peer inspect stubs/FP arguments without an external tooling reopen.
    for old,new in [('tools/xexec/xexec.c','harness-source.c'),('tools/xexec/xexec.py','harness-driver-source.py')]:
        with (HERE/new).open('xb') as f:f.write((ROOT/old).read_bytes());f.flush();os.fsync(f.fileno())
    runtime=[Path('/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64'),
             Path('/var/tmp/sound-analysis/xexec/xexec'),Path(sys.executable),
             Path('/usr/lib/x86_64-linux-gnu/libc.so.6'),Path('/usr/lib/x86_64-linux-gnu/libm.so.6'),
             Path('/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2')]
    runtime_pins=[ident(p) for p in runtime]
    assert runtime_pins[0]['sha256']=='1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0'
    assert runtime_pins[1]['sha256']=='5d236b76351b3a30f56addd37305e8e8935a34ba959fd9be0873cd84886d5385'
    sources=['wiki/specs/midi-user-mapping.md','tools/xexec/xexec.c','tools/xexec/xexec.py',
      'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/manifest.json',
      'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/run_pilot.py',
      'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/results/midi.json',
      'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/raw/runs.jsonl',
      'analysis/ableton-live-12.4.3/r2/x2-midi-v1/manifest.json',
      'analysis/ableton-live-12.4.3/r2/x2-midi-v1/run_x2.py',
      'analysis/ableton-live-12.4.3/full-spec-v1/family-midi-user-routes-v1/manifest.json',
      'analysis/ableton-live-12.4.3/full-spec-v1/family-midi-user-routes-v1/route-ledger.json',
      'analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-midi-user-routes-v1-review.json',
      'handoff/midi-config-v3/cases.json','handoff/midi-config-v4/manifest.json','handoff/midi-config-v4/REVIEW.md']
    context={'schema':'selected-midi-relative-standing-context-v1','image':runtime_pins[0]['path'],
      'loader':runtime_pins[1]['path'],'runtime':runtime_pins,'watched':[ident(ROOT/p) for p in sources]+runtime_pins,
      'environment':{'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'},
      'host':{'utc':R.now(),'python':sys.version,'sys_executable':sys.executable,'sys_flags':str(sys.flags),
              'uname':list(os.uname()),'byteorder':sys.byteorder,'libc':os.confstr('CS_GNU_LIBC_VERSION'),
              'parser':R.parser_bits()},
      'selection':'Root selected exact1024 logical/18inherited/1006fresh+8init, 8children, 20s, no replay/new state axes. Root sole independent peer after finalseal.',
      'expected_used_imports_per_child':R.USES,'expected_loader_header':R.HEADER,
      'policy':{'timeout_seconds':20,'stdin':'DEVNULL','core_limit':[0,0],'cpu_seconds':20,
                'file_size_limit':4194304,'process_group':'new session, SIGKILL/reap selected child on timeout/interruption',
                'attempts_per_mode':1,'retry':False,'stop_remaining_on_anomaly':True,
                'observation_boundary':'Checks occur after each child. Calls already queued within a failing child may have run before detection; all raw retained.',
                'raw_durability':'raw files closed; no explicit fsync on their FDs. JSON bookkeeping fsynced; no power-loss/crash durability proof.'},
      'limits':'Only existing X1/X2 local supplied record/initializer class. No GDB, receiver, actual setter, new original object graph/patch/tool/provider. No current input-register/fenv tracing; no ARM/Apple/public/accumulator/pair/takeover/lifecycle equivalence.'}
    assert sys.byteorder=='little' and os.uname().machine=='x86_64'
    write('context.json',context)
    write('input-checks.json',{'status':'PASS','negative_controls':R.input_controls(data),'parser':R.parser_bits(),
                              'original_calls':0,'binary_custody_only':True})
    print(json.dumps({'logical':1024,'inherited':18,'fresh':1006,'plans':len(plans),'runtime':runtime_pins[:2]}))

if __name__=='__main__':main()
