"""Independent retained-data review only; never imports collector/checker/reader/native code."""
from pathlib import Path
import hashlib
import json
import math
import re
import struct
import sys

ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
P=BASE/'depth-corpus-pickup-step-capture'
E=BASE/'reviews/corpus-pickup-step-root-execution'


def identity(path):
    raw=path.read_bytes();return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    assert sys.argv[1:]==['--check']
    proposal=json.loads((P/'proposal.json').read_text())
    history=json.loads((P/'preservation-inputs.json').read_text())
    paths={Path(r['path']) for r in history+list(proposal['source_pins'].values())}
    paths.update(f for directory in (P,E) for f in directory.rglob('*') if f.is_file())
    paths.update(f for f in (BASE/'depth-corpus-pickup-step-capture-preparation').iterdir() if f.is_file())
    paths.add(BASE/'reviews/corpus-pickup-step-preflight-review.json')
    paths.add(Path(__file__))
    before={str(p):identity(p) for p in sorted(paths)}
    assert identity(P/'manifest.json')['sha256']=='eb26cc30ae0e52cd74b73459532c7e81587fafc6ff2a313f09f7ad8f9cd5e6e2'
    manifest=json.loads((P/'manifest.json').read_text())
    assert len(manifest['files'])==25
    assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}=={'manifest.json'}|{r['path'] for r in manifest['files']}
    for row in manifest['files']:
        assert {k:identity(P/row['path'])[k] for k in ('bytes','sha256')}=={k:row[k] for k in ('bytes','sha256')}
    for row in history+list(proposal['source_pins'].values()):
        assert identity(Path(row['path']))==row
    bundle=Path(proposal['source_pins']['bundle']['path']).read_bytes();segment=proposal['x86_slice']
    assert hashlib.sha256(bundle[segment['offset']:segment['offset']+segment['bytes']]).hexdigest()==segment['sha256']
    preflight=json.loads((P/'manifest-preflight.json').read_text())
    for row in preflight['files']:
        assert (P/row['path']).read_bytes()==(BASE/'depth-corpus-pickup-step-capture-preparation'/row['path']).read_bytes()
    assert (P/'manifest-preflight.json').read_bytes()==(BASE/'depth-corpus-pickup-step-capture-preparation/manifest-preflight.json').read_bytes()
    # Exact durable paired-map reconciliation, not a future equality gate for mutable wiki.
    maps=[]
    for directory,stem,count in [(P,'watch',820),(E,'watch',910),(E,'description-watch',934)]:
        left=json.loads((directory/(stem+'-before.json')).read_text())
        right=json.loads((directory/(stem+'-after.json')).read_text())
        assert left==right['files'] and right['changed']==[] and len(left)==count
        assert len({r['path'] for r in left})==count
        maps.append(dict(scope=stem,directory=directory.name,paths=count,unchanged=True))
    actual=json.loads((P/'results.json').read_text())
    assert (P/'results.json').read_bytes()==(E/'collector.stdout').read_bytes()
    attempt=json.loads((P/'attempt.json').read_text());selection=json.loads((E/'selection.json').read_text());receipt=json.loads((E/'receipt.json').read_text())
    assert receipt['collector_exit']==0 and (E/'collector.stderr').stat().st_size==0
    assert identity(P/'results.json')==receipt['results'] and identity(E/'collector.stdout')==receipt['stdout']
    assert selection['preflight_review']==identity(BASE/'reviews/corpus-pickup-step-preflight-review.json')
    assert selection['argv'][-1]==attempt['preflight_sha256']==identity(P/'manifest-preflight.json')['sha256']
    assert attempt['complete_child_environment']==proposal['child_environment_complete']
    assert set(attempt['complete_child_environment'])=={'PATH','LANG','LC_ALL','LC_CTYPE','XDEV_TIME'}
    assert attempt['complete_child_environment']['XDEV_TIME']=='0'
    assert attempt['child_limits']['RLIMIT_CORE']==[0,0] and attempt['timeout_seconds']==30
    assert [r['name'] for r in actual['runs']]==['control','left-step']
    assert (actual['attempted_launches'],actual['returned_pid_children'],actual['structurally_valid_captures'])==(2,2,2)
    assert actual['grade'] is None and actual['criterion'] is None and actual['new_normative_cases']==0
    vector=json.loads(Path(proposal['source_pins']['released_vector']['path']).read_text())['cases'][5]['evaluations'][0]
    assert vector['id']=='CORPUS-AUDIO-006-01' and proposal['source_vector']=={k:vector[k] for k in ('parameters','parameter_order')}
    arrays={};raw={};logs=[]
    previous=attempt['started_utc']
    for row in actual['runs']:
        name=row['name'];script=(P/(name+'.script')).read_text().splitlines()
        assert script==proposal['scripts'][name] and (P/(name+'.script')).read_bytes()==(P/'raw'/(name+'.script')).read_bytes()
        requested=[line.split()[1:] for line in script if line.startswith('param ')]
        assert [line for line in script if not line.startswith('param ')]==['mxcsr 0x1f80','transport 0 0 120','create','rate 44100','inflag 1','input '+proposal['source_pins']['input']['path'],'process 8192 512','process 8192 512','destroy']
        assert len(requested)==39 and [int(a) for a,b in requested[:38]]==list(range(38))
        assert [struct.pack('<f',float(v)) for k,v in requested[:38]]==[struct.pack('<f',vector['parameters'][k]) for k in vector['parameter_order']]
        assert requested[-1]==['15','0.10000000149011612' if name=='control' else '0.75']
        log=(P/'raw'/(name+'.stdout')).read_text();lines=log.splitlines()
        echoed=[line.split()[1:] for line in lines if line.startswith('param ')]
        assert [a for a,b in echoed]==[a for a,b in requested]
        assert [struct.pack('<f',float(v)) for k,v in echoed]==[struct.pack('<f',float(v)) for k,v in requested]
        commands=[line.split()[0] for line in lines if line.split() and line.split()[0] in {'mxcsr','transport','create','rate','param','inflag','input','process','destroy','event','reset','info'}]
        assert commands==['mxcsr','transport','create','rate']+['param']*38+['inflag','input','process','param','process','destroy']
        assert [line for line in lines if line.startswith('process ')]==['process 8192 512 flags: 16x(ret=0,flag=1) blocks=16']*2==row['process_lines']
        assert not any('TRAP' in s or 'FAULT' in s or s.startswith('xdev:') for s in lines)
        assert lines[-1]=='cxx-failbits 0' and lines.count('create ok')==lines.count('destroy')==1
        assert all(lines.count(s)==1 for s in ['mxcsr 0x1f80','transport 0 0 120','rate 44100 ret=1','inflag 1','input '+proposal['source_pins']['input']['path']])
        assert row['declared_imports']==[s for s in lines if s.startswith('import ')]
        assert row['used_imports']==[s for s in lines if s.startswith('used ')]
        assert row['argv']==[proposal['source_pins']['xdev']['path'],proposal['source_pins']['bundle']['path'],str(P/'raw'/(name+'.script')),str(P/'raw'/(name+'.f32')),'--imports']
        assert row['launch_attempted'] and row['popen_returned_pid'] and isinstance(row['pid'],int)
        assert row['exit_code']==0 and row['signal'] is None and not row['timeout'] and row['exception'] is None
        assert row['valid_capture'] and row['log_valid'] and row['numeric_valid']
        assert selection['selected_utc']<previous<=row['started_utc']<row['finished_utc']<receipt['finished_utc']
        previous=row['finished_utc']
        for suffix,key in [('.stdout','stdout'),('.stderr','stderr'),('.f32','output')]:
            assert identity(P/'raw'/(name+suffix))==row[key]
        assert (P/'raw'/(name+'.stderr')).stat().st_size==0
        assert json.loads((P/(name+'-result.json')).read_text())==row
        raw[name]=(P/'raw'/(name+'.f32')).read_bytes()
        assert len(raw[name])==131072
        arrays[name]=list(struct.iter_unpack('<ff',raw[name]))
        assert all(math.isfinite(v) for frame in arrays[name] for v in frame)
        logs.append(dict(name=name,pid=row['pid'],parameters=39,process_segments=2,CalcA_blocks=32,
                         declared_imports=len(row['declared_imports']),used_imports=len(row['used_imports']),clean=True))
    assert len({r['pid'] for r in actual['runs']})==2
    # Own explicit arithmetic, not execution/import of Root reader.
    description=json.loads((P/'fixed-window-description.json').read_text())
    windows=[(0,4096),(4096,8192),(8192,16384)]+[(i,i+512) for i in range(8192,16384,512)]
    rows=[]
    for start,end in windows:
        for c,label in enumerate(('L','R')):
            a=[arrays['control'][i][c] for i in range(start,end)]
            z=[arrays['left-step'][i][c] for i in range(start,end)]
            changed=[i for i in range(end-start) if a[i]!=z[i]]
            rows.append(dict(start_frame_inclusive=start,end_frame_exclusive=end,channel=label,
                control_energy=math.fsum(v*v for v in a),step_energy=math.fsum(v*v for v in z),
                different_numeric_samples=len(changed),first_different_local_frame=changed[0] if changed else None,
                last_different_local_frame=changed[-1] if changed else None,
                squared_difference_sum=math.fsum((z[i]-a[i])*(z[i]-a[i]) for i in range(end-start)),
                all_channel_sample_bits_equal=all(raw['control'][8*i+4*c:8*i+4*c+4]==raw['left-step'][8*i+4*c:8*i+4*c+4] for i in range(start,end))))
    assert rows==description['rows'] and len(rows)==38
    assert description['criterion'] is None and description['grade'] is None
    dreceipt=json.loads((E/'description-receipt.json').read_text());dselection=json.loads((E/'description-selection.json').read_text())
    assert dselection['selected_reader']==identity(P/'describe-fixed-windows.py')
    assert dreceipt['description']==identity(P/'fixed-window-description.json') and dreceipt['exit']==0
    assert dselection['selected_utc']<dreceipt['finished_utc'] and (E/'description.stderr').stat().st_size==0
    assert json.loads((E/'description.stdout').read_text())==dict(rows=38,main_windows=rows[:6])
    assert before=={str(p):identity(p) for p in sorted(paths)}
    print(json.dumps(dict(status='PASS bounded actual observations only',capture_manifest=identity(P/'manifest.json'),
        payloads=25,source_pins=14,history=811,actual_children=2,counts=[2,2,2],logs=logs,maps=maps,
        main_windows=rows[:6],all38description_rows_exact=True,right_all_bits_equal=all(raw['control'][8*i+4:8*i+8]==raw['left-step'][8*i+4:8*i+8] for i in range(16384)),
        watched=len(paths),watch_unchanged=True,watch_sha256=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),
        collector_or_reader_calls=0,native_calls=0,criterion=None,grade=None),indent=2))


if __name__=='__main__':main()
