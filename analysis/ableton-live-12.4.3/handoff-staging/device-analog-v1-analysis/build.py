"""Package retained numerical captures. Does not execute a device or synthesize audio."""
import csv
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SOURCE=ROOT/'analysis/ableton-live-12.4.3/r2/t12-analog-v1'
PACKAGE=HERE.with_name('device-analog-v1')


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(path,value):path.write_text(json.dumps(value,indent=1,allow_nan=False)+'\n')


def build():
    assert not PACKAGE.exists(), 'candidate already exists'
    manifest=json.loads((SOURCE/'manifest.json').read_text())
    for filename,info in manifest['files'].items():assert sha(SOURCE/filename)==info['sha256'],filename
    records=json.loads((SOURCE/'results/cases.json').read_text())
    table=list(csv.DictReader((ROOT/'analysis/ableton-live-12.4.3/r2/n6-device-tables-v1/out/conversions.tsv').open(),delimiter='\t'))
    rows=[r for r in table if r['device']=='UltraAnalog' and r['index']]
    assert [int(r['index']) for r in rows]==list(range(203))
    names=[]
    for row in rows:
        name=row['stored_name']
        if name.startswith('(second output'):
            parent=int(re.search(r'index (\d+)',name).group(1));name=rows[parent]['stored_name']+'.secondary'
        name=name.replace('/ToggleDummy','/Enabled').replace('DummyPerNotePitchBendRange','PerNotePitchBendRangeComparison')
        names.append(name)
    assert len(set(names))==203
    PACKAGE.mkdir();(PACKAGE/'reference').mkdir();(PACKAGE/'signals').mkdir()
    shutil.copyfile(HERE/'compare_payload.py',PACKAGE/'compare.py')
    spec=importlib.util.spec_from_file_location('metric',HERE/'compare_payload.py');metric=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric)
    excluded={12,33,34,35,36,43,44,46,47}
    ids=[i for i in range(1,46) if i not in excluded]
    cases=[];trace=[];signals={};sources={SOURCE/'manifest.json',SOURCE/'results/cases.json',SOURCE/'results/libm.json',SOURCE/'results/determinism.json',SOURCE/'results/protocol.json',SOURCE/'an.py',SOURCE/'fit.py',ROOT/'analysis/ableton-live-12.4.3/r2/n6-device-tables-v1/out/conversions.tsv',ROOT/'wiki/specs/device-analog.md'}
    steady_numbers=set(range(6,23))-{10,12} | {25,26,27,37,38,41}
    requirements={1:[1,4,6,16],2:[1,4,6,23],3:[1],4:[1,5,17],5:[23],6:[7],7:[7],8:[7],9:[7],10:[6],11:[6],13:[12],14:[12],15:[12],16:[12],17:[12],18:[12],19:[12],20:[12],21:[12],22:[12],23:[13,16],24:[13],25:[14],26:[14],27:[15],28:[16],29:[16],30:[16],31:[17],32:[17],37:[8],38:[8],39:[5],40:[5],41:[11,13],42:[4],45:[1]}
    for number in ids:
        original_ids=[f'DAN-{number:03d}'+suffix for suffix in (['a','b'] if number in [9,45] else ['a','b','c'] if number==11 else [''])]
        evaluations=[]
        for offset,original_id in enumerate(original_ids,1):
            record=records[original_id]
            source_id=record.get('source',original_id);r=records[source_id]
            if 'source' in record:assert record['bit_identical_to_source']
            source_wav=SOURCE/'raw'/f'{source_id}.wav';source_script=SOURCE/'raw'/f'{source_id}.script'
            assert sha(source_wav)==r['wav_sha256']
            rate,mono=wavfile.read(source_wav)
            assert mono.dtype==np.float32 and mono.ndim==1 and rate==r['fs'] and len(mono)==r['frames']
            stereo=np.stack([mono,mono],axis=1).astype('<f4');assert hashlib.sha256(stereo.tobytes()).hexdigest()==r['f32_sha256']
            lines=source_script.read_text().splitlines()
            params=[(int(i),float(v)) for i,v in (re.fullmatch(r'param (\d+) (.+)',line).groups() for line in lines if line.startswith('param '))]
            assert [i for i,v in params]==list(range(203))
            events=[(int(f),int(s,0),int(k),int(v)) for f,s,k,v in (line.split()[1:] for line in lines if line.startswith('event '))]
            assert sorted(events,key=lambda e:e[0])==sorted(map(tuple,r['events']),key=lambda e:e[0])
            identifier=f'ANALOG-AUDIO-{number:03d}-{offset:02d}'
            file=f'reference/{identifier}.f32';(PACKAGE/file).write_bytes(stereo.tobytes())
            frames=len(stereo)
            if frames not in signals:
                signals[frames]=f'signals/silence-{frames}.f32';np.zeros((frames,2),dtype='<f4').tofile(PACKAGE/signals[frames])
            note_ons=[e for e in events if e[1]&240==144 and e[3]>0]
            onset=[];period=rate//1000;block=record['block']
            for frame,status,key,velocity in note_ons:
                point=(frame//period)*period;begin=(frame//block)*block
                if point<begin:point+=period
                start=point+1;onset.append([start,min(start+2048,frames)])
            nonzero=np.flatnonzero(mono!=0);assert len(nonzero) and int(nonzero[0])==r['first_nonzero']
            settings={'first_nonzero':int(nonzero[0]),'last_nonzero':int(nonzero[-1]) if nonzero[-1]<frames-1 else None,'onset_windows':onset,'steady_windows':[]}
            omissions=[]
            if number in steady_numbers:
                assert len(note_ons)==1
                start=note_ons[0][0]+rate//10;stop=frames
                segment=mono[start:stop].astype(float)
                guess=440*2**((note_ons[0][2]-69)/12)
                # Detune/transpose cases have intentionally shifted comparison frequencies.
                if original_id=='DAN-011a':guess=795.770
                elif original_id=='DAN-011b':guess=93.7905
                elif original_id=='DAN-011c':guess=2118.569
                elif number==37:guess/=2
                center=metric.frequency(segment,guess,rate)
                harmonic_count=min(40,int((rate/2)//center))
                amplitudes,dc=metric.harmonic_fit(segment,center,rate,harmonic_count)
                strong=np.flatnonzero(amplitudes>=amplitudes.max()*.01)+1
                assert len(strong)
                minimum=max(.2*rate,25*rate/center)
                if len(segment)>=minimum:
                    settings['steady_windows'].append({'start_frame':start,'stop_frame':stop,'center_hz':center,'harmonic_count':harmonic_count,'graded_harmonics':strong.tolist(),'frequency_graded':center>=100})
                    if center<100:omissions.append('frequency below 100 Hz lies outside the cited pitch calibration; harmonics/DC only')
                else:omissions.append('steady window is shorter than 0.2 s or 25 periods; no frequency/harmonic grade')
            else:omissions.append('no calibrated stationary harmonic window selected; onset/envelope/timing only')
            parameters={names[i]:float(np.float32(v)) for i,v in params}
            public_events=[{'frame':f,'kind':'note_on' if s&240==144 else 'note_off','channel':s&15,'key':k,'velocity':v} for f,s,k,v in events]
            evaluations.append({'id':identifier,'frames':frames,'sample_rate_hz':rate,'block_frames':record['block'],'parameters':parameters,'parameter_order':names,'events':public_events,'signal':signals[frames],'reference':file,'metric':settings})
            trace.append({'evaluation':identifier,'draft_case':original_id,'source_capture':source_id,'source_wav':str(source_wav.relative_to(ROOT)),'source_script':str(source_script.relative_to(ROOT)),'wav_sha256':r['wav_sha256'],'stereo_sample_sha256':r['f32_sha256'],'omissions':omissions,'generated_parameter_names':dict(enumerate(names))})
            sources|={source_wav,source_script}
        cases.append({'id':f'ANALOG-AUDIO-{number:03d}','purpose':records[original_ids[0]]['description'].replace('DAN-004','the three-note chord'),'requirements':[f'REQ-DEVICE-ANALOG-{i:03d}' for i in requirements[number]],'provenance':'original x86_64 device-code output; arm64 correspondence inferred; application not executed','evaluations':evaluations})
    save(PACKAGE/'cases.json',{'schema':'device-audio-cases-v1','status':'staged-unreviewed','release_id':'device-analog-v1','representation':'Independent named comparison-domain vectors and timed note inputs, not an original API or file/Live-chain mapping','sample_format':'little-endian interleaved left/right IEEE-754 binary32, no header','cases':cases})
    save(HERE/'traceability.json',{'source_manifest_sha256':sha(SOURCE/'manifest.json'),'evaluations':trace,'excluded_draft_cases':sorted(excluded)})
    save(HERE/'source-inventory.json',{'files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(sources)]})
    print('groups',len(cases),'evaluations',len(trace),'signals',len(signals),'source_hashes',len(manifest['files']))


if __name__=='__main__':build()
