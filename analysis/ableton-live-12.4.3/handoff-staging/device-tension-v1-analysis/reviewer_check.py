"""Independent retained-byte/protocol/calibration review. Does not execute device code."""
import copy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import shutil
import subprocess
import sys
import tempfile

import numpy as np

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PAYLOAD=HERE.with_name('device-tension-v1')
SOURCE=HERE.parents[1]/'r2/t12-tension-v1'


def sha(data):return hashlib.sha256(data).hexdigest()


def main():
    source_manifest=json.loads((SOURCE/'manifest.json').read_text())
    for name,row in source_manifest['files'].items():
        data=(SOURCE/name).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
    assert len(source_manifest['files'])==161
    external_checks=[]
    for name,row in source_manifest['external_inputs'].items():
        data=Path(row['path']).read_bytes();assert sha(data)==row.get('file_sha256',row.get('sha256')),name
        for arch in ('x86_64','arm64'):
            if arch+'_offset' in row:
                part=data[row[arch+'_offset']:row[arch+'_offset']+row[arch+'_size']]
                assert sha(part)==row[arch+'_sha256']
        external_checks.append(name)
    trace=json.loads((HERE/'traceability.json').read_text())['cases']
    runs=json.loads((SOURCE/'results/runs.json').read_text())['runs']
    measurements=json.loads((SOURCE/'results/measure.json').read_text())
    sensitivity=json.loads((SOURCE/'results/sensitivity.json').read_text())
    cases=json.loads((PAYLOAD/'cases.json').read_text())['cases'];assert len(cases)==len(trace)==27
    table=SOURCE.parent/'n6-device-tables-v1/out/conversions.tsv'
    assert sha(table.read_bytes())==json.loads((SOURCE/'results/runs.json').read_text())['n6_conversions_sha256']
    rows=[r for r in csv.DictReader(table.open(),delimiter='\t') if r['device']=='StringStudio' and r['index']]
    labels={int(r['index']):r['stored_name'] for r in rows if not r['stored_name'].startswith('(')}
    for row in rows:
        if row['stored_name'].startswith('(second output'):
            parent=int(re.search(r'of index (\d+)',row['stored_name']).group(1))
            labels[int(row['index'])]=labels[parent]+('.Enabled' if parent==0 else '.SlopeFlag' if parent==91 else '.Negative')
    labels[121]='PerNotePitchBendRange'
    summary={'held':0.0,'release':0.0,'frequency_relative':0.0,'log_radius_relative':0.0,'complex_amplitude':0.0,'repeat_whole':0.0}
    for case,tr in zip(cases,trace):
        e=case['evaluations'][0];tag=tr['source_case'];assert case['id']==tr['case'] and tag in sensitivity
        assert tag not in {'damper_mass_0','exc_bow','bow_x1','preset_cello'}
        row=runs[tag];lines=(SOURCE/f'raw/{tag}.script').read_text().splitlines()
        assert lines[0]=='create' and lines[-1]=='destroy'
        assert [x for x in lines if x.startswith('rate ')]==[f"rate {e['sample_rate_hz']}"]
        assert [x for x in lines if x.startswith('process ')]==[f"process {e['frames']} 512"]
        assert 'input zero' in lines and 'inflag 0' in lines
        entries=[x.split()[1:] for x in lines if x.startswith('param ')]
        assert len(entries)==129 and [int(i) for i,v in entries]==sorted(labels)
        assert e['parameter_order']==[labels[int(i)] for i,v in entries]
        for i,v in entries:
            assert struct.pack('<f',float(v))==struct.pack('<f',e['parameters'][labels[int(i)]])
        events=[[int(x[1]),int(x[2],0),int(x[3]),int(x[4])] for x in map(str.split,lines) if x[0]=='event']
        assert events==row['events']
        assert events==[[v['frame'],144 if v['type']=='note_on' else 128,v['key'],v['velocity']] for v in e['events']]
        assert all(v['channel']==1 for v in e['events'])
        wav=(SOURCE/f'raw/{tag}.wav').read_bytes();assert sha(wav)==row['wav_sha256']
        pos=12;chunks={}
        while pos+8<=len(wav):
            name,size=struct.unpack_from('<4sI',wav,pos);chunks[name]=wav[pos+8:pos+8+size];pos+=8+size+(size%2)
        fmt=struct.unpack_from('<HHIIHH',chunks[b'fmt ']);assert fmt==(3,1,e['sample_rate_hz'],e['sample_rate_hz']*4,4,32)
        data=(PAYLOAD/e['reference']).read_bytes();assert data==chunks[b'data'] and len(data)==e['frames']*4
        # Recover the interleaved original output from the retained identical mono channels.
        values=np.frombuffer(data,dtype='<f4');stereo=np.repeat(values,2).astype('<f4').tobytes()
        assert row['channels_identical'] and sha(stereo)==row['raw_f32_sha256']
        assert (PAYLOAD/e['signal']).read_bytes()==bytes(len(data))
        assert e['warm_up_frames']==0 and e['block_frames']==512
        m=e['metric'];source_measure=measurements[tag]
        assert m['onset_frame']==source_measure['first_nonzero']
        variants=sensitivity[tag];assert set(variants)=={'libm+1','libm-1','round_down','round_up','round_zero'}
        for variant in variants.values():assert variant['onset_shift_frames']==0
        onset=m['onset_frame'];off=next(v[0] for v in events if v[1]==128)
        if tag=='exc_bounce':
            assert m['kind']=='repeated-strike' and m['partials']==[] and m['waveform_windows']==[[onset,e['frames'],0.005,'whole ringing waveform']]
            summary['repeat_whole']=max(v['whole'] for v in variants.values());assert summary['repeat_whole']<0.005
        else:
            assert m['kind']=='stable' and m['waveform_windows']==[[onset,off,0.003,'held waveform'],[off,e['frames'],0.01,'release waveform']]
            held=source_measure['held'];selected=[p for p in held['partials'] if p['level_db']>=-60]
            assert selected and m['partials']==[{'harmonic':p['k'],'center_hz':p['hz']} for p in selected]
            assert m['partial_window']==held['window'] and m['partial_cutoff_hz']==min(150,0.3*held['partials'][0]['hz']/held['partials'][0]['k'])
            assert m['amplitude_normalizer']==max(p['amp'] for p in held['partials'])>0
            for v in variants.values():
                assert v['held']<0.003 and v['release']<0.01 and v['modal']['n']==len(selected)>0
                for key,bound,target in [('freq_rel',2e-6,'frequency_relative'),('log_radius_rel',6e-4,'log_radius_relative'),('amp_rel',5e-4,'complex_amplitude')]:
                    assert np.isfinite(v['modal'][key]) and v['modal'][key]<bound
                    summary[target]=max(summary[target],v['modal'][key])
                summary['held']=max(summary['held'],v['held']);summary['release']=max(summary['release'],v['release'])
    spec=importlib.util.spec_from_file_location('tension_review_measurement',PAYLOAD/'compare.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    first=cases[0]['evaluations'][0];signal=module.audio(PAYLOAD/first['reference'],first['frames'])
    rejects=0
    bad_inputs=[(np.array([]),signal),(signal[:-1],signal),(signal[:,None],signal),(signal+np.nan,signal),(signal,signal+np.inf)]
    for value,reference in bad_inputs:
        try:module.compare(value,reference,first['metric'],first['sample_rate_hz'])
        except ValueError:rejects+=1
        else:raise AssertionError('malformed direct comparison accepted')
    for field,bad in [('partials',[]),('waveform_windows',[]),('waveform_windows',[[100,100,0.003,'empty']])]:
        metric=copy.deepcopy(first['metric']);metric[field]=bad
        try:module.compare(signal,signal,metric,first['sample_rate_hz'])
        except ValueError:rejects+=1
        else:raise AssertionError('missing required measurement accepted')
    with tempfile.TemporaryDirectory() as t:
        empty=Path(t)/'empty.f32';empty.write_bytes(b'')
        try:module.audio(empty,0)
        except ValueError:rejects+=1
        else:raise AssertionError('zero-frame input accepted')
    boundaries=[]
    # Independent generated tones exercise individual numerical boundaries, never device synthesis.
    rate=44100;n=np.arange(24000);center=300.0;radius=-5e-5;origin=1024
    reference=0.7*np.exp(radius*n)*np.cos(2*np.pi*center*n/rate+0.2)
    norm=abs(module.partial(reference,center,40,origin,len(n),rate)[2])
    metric={'kind':'stable','onset_frame':0,'waveform_windows':[[0,len(n),100,'nonrestrictive test window']], 'partials':[{'center_hz':center}],'partial_cutoff_hz':40,'partial_window':[origin,len(n)],'amplitude_normalizer':norm}
    for quantity,bound in [('frequency',2e-6),('log radius',6e-4),('complex amplitude',5e-4)]:
        for factor in [0.9,1.1]:
            if quantity=='frequency':value=0.7*np.exp(radius*n)*np.cos(2*np.pi*center*(1+factor*bound)*n/rate+0.2)
            elif quantity=='log radius':value=0.7*np.exp(radius*(1+factor*bound)*n)*np.cos(2*np.pi*center*n/rate+0.2)
            else:value=reference*(1+factor*bound)
            result=module.compare(value,reference,metric,rate)
            failed=('partial 1 '+quantity) in result['failures']
            assert failed==(factor>1),(quantity,factor,result)
            boundaries.append({'measurement':quantity,'bound_factor':factor,'target_rejected':failed})
    for bound in [0.003,0.01,0.005]:
        metric={'kind':'repeated-strike','onset_frame':0,'waveform_windows':[[0,len(n),bound,'waveform test']],'partials':[]}
        for factor in [0.9,1.1]:
            result=module.compare(reference*(1+factor*bound),reference,metric,rate)
            assert result['pass']==(factor<1)
            boundaries.append({'measurement':'waveform','bound':bound,'bound_factor':factor,'pass':result['pass']})
    manifest=json.loads((PAYLOAD/'manifest.json').read_text())
    actual={str(p.relative_to(PAYLOAD)) for p in PAYLOAD.rglob('*') if p.is_file()}
    assert actual=={r['path'] for r in manifest['files']}|{'manifest.json'}
    assert not any(p.is_symlink() for p in PAYLOAD.rglob('*'))
    restricted=re.compile(r'(?i)(/home/|/var/tmp/|\.bundle|t12-tension|DTN-\d|SetParameterA|CalcA|FUN_[0-9a-f]+|__ZN|0x[0-9a-f]{6,})')
    for row in manifest['files']:
        path=PAYLOAD/row['path'];data=path.read_bytes()
        assert sha(data)==row['sha256'] and len(data)==row['bytes']
        if path.suffix in ('.py','.md','.json'):assert not restricted.search(path.read_text()),path
        if path.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):assert (path.parent/link.split('#')[0]).is_file()
    with tempfile.TemporaryDirectory(prefix='tension-review-export-') as t:
        export=Path(t)/'reviewed';shutil.copytree(PAYLOAD,export)
        process=subprocess.run([sys.executable,'-I',str(export/'compare.py'),str(export/'reference')],capture_output=True,text=True,cwd=t)
        export_report=json.loads(process.stdout);assert process.returncode==0 and export_report['pass'] and len(export_report['results'])==27
        bad=Path(t)/'missing';bad.mkdir()
        missing=subprocess.run([sys.executable,'-I',str(export/'compare.py'),str(bad)],capture_output=True,text=True,cwd=t)
        assert missing.returncode==1 and not json.loads(missing.stdout)['pass']
    report={'status':'pass','reviewer':'independent Tension review context /root/collision_stage','source_payloads_verified':161,'external_identities_verified':external_checks,'evaluations_checked':27,'calibration_variants_checked':135,'calibration_maxima':summary,'mono_and_interleaved_hashes_match':True,'parameters_events_protocol_exact':True,'malformed_direct_measurement_checks':rejects,'boundary_checks':boundaries,'source_code_execution':False,'manifest_sha256':sha((PAYLOAD/'manifest.json').read_bytes()),'inventory_and_export':'pass','source_exclusion':'pass; semantic review accepts public control labels and measurement code only','limitations':'Previously retained perturbation summaries checked; perturbed audio is not retained, no Live/arm64/candidate execution. No application synthesis was performed.'}
    (HERE/'reviewer-validation.json').write_text(json.dumps(report,indent=1,allow_nan=False)+'\n');print(json.dumps(report,indent=1))


if __name__=='__main__':main()
