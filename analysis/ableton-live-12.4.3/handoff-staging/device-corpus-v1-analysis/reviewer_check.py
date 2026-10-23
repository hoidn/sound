"""Independent Corpus handoff review: source fidelity, numerical probes and export.
No device/program execution or DSP synthesis. Synthetic tones test measurements.
Run: python3 -I -B reviewer_check.py [package directory]
"""
import csv
import hashlib
import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy.signal import firwin, lfilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT / 'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1'
PACKAGE = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.with_name('device-corpus-v1')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location('comparison', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_mode(samples, rate, hz, cutoff):
    length = min(4001, math.floor(3.3*rate/cutoff) | 1)
    impulse = firwin(length, cutoff, fs=rate, window='hamming', scale=True)
    time = np.arange(16384)
    baseband = lfilter(impulse, [1], samples * np.exp(-1j*(2*np.pi*hz/rate)*time))
    selected = baseband[4096+length:]
    time = time[4096+length:] - (length-1)/2
    design = np.column_stack([time-4096, np.ones(len(time))])
    phase = np.linalg.lstsq(design, np.unwrap(np.angle(selected)), rcond=None)[0]
    magnitude = np.linalg.lstsq(design, np.log(np.abs(selected)), rcond=None)[0]
    return hz+phase[0]*rate/(2*np.pi), magnitude[0], 2*np.exp(magnitude[1]+1j*phase[1])


def probes(comparator):
    rate=44100; n=np.arange(16384); reference=np.column_stack([np.sin(2*np.pi*1000*n/rate)]*2)
    outcomes=[]
    def expect(name, candidate, ref, metric, passes):
        try: actual=comparator.compare(candidate, ref, metric, rate)['pass']
        except (ValueError,ZeroDivisionError): actual=False
        assert actual==passes, (name, actual, passes)
        outcomes.append({'probe':name,'expected_pass':passes,'actual_pass':bool(actual)})
    expect('waveform inside RMS bound',reference*1.00005,reference,{'kind':'waveform','start_frame':4096},True)
    expect('waveform outside RMS bound',reference*1.0002,reference,{'kind':'waveform','start_frame':4096},False)
    for db,deg,passes in [(0.005,0.25,True),(0.02,0,False),(0,1,False)]:
        candidate=np.column_stack([10**(db/20)*np.sin(2*np.pi*1000*n/rate+deg*np.pi/180)]*2)
        expect(f'sine {db} dB {deg} degrees',candidate,reference,{'kind':'sine','frequency_hz':1000},passes)
    noise=np.random.default_rng(19).normal(0,.1,(16384,2))
    for db,passes in [(.005,True),(.02,False)]:
        expect(f'noise {db} dB',noise*10**(db/20),noise,{'kind':'noise'},passes)
    base=np.column_stack([np.cos(2*np.pi*261.62*n/rate)]*2)
    for delta,passes in [(.1,True),(.3,False)]:
        candidate=np.column_stack([np.cos(2*np.pi*(261.62+delta)*n/rate)]*2)
        expect(f'LFO frequency shift {delta} Hz',candidate,base,{'kind':'lfo'},passes)
    ramp=np.r_[np.full(100,1e-22),np.arange(1,101)/100,np.ones(16384-200)]
    startup=np.column_stack([ramp,ramp])
    expect('startup tiny floor',startup,startup,{'kind':'startup'},True)
    for name,frame in [('early onset',99),('missing onset',100),('wrong ramp',150)]:
        candidate=startup.copy();candidate[frame,0]=1e-17 if frame==99 else 0
        expect('startup '+name,candidate,startup,{'kind':'startup'},False)
    t=n-4096; hz=440.; rho=-.0001
    def resonance(f,d):return np.where(t>=0,.7*np.exp(d*t)*np.cos(2*np.pi*f*t/rate+.3),0)
    signal=resonance(hz,rho); actual=comparator.mode(signal,hz,rate,50)
    separate=independent_mode(signal,rate,hz,50)
    assert abs(actual[0]-separate[0])<1e-8 and abs(actual[1]-separate[1])<1e-12
    assert abs(actual[2]/separate[2]-1)<1e-9
    assert abs(actual[0]-hz)<1e-6 and abs(actual[1]-rho)<1e-10
    metric={'kind':'modal','modes':[[{'center_hz':hz,'cutoff_hz':50}]]*2}
    ref=np.column_stack([signal,signal])
    bound=hz*4*(3*2**-25/(2*np.pi*hz/rate)**2+2**-23)
    for factor,passes in [(.25,True),(2,False)]:
        candidate=np.column_stack([resonance(hz+factor*bound,rho)]*2)
        expect(f'modal frequency {factor} tolerance',candidate,ref,metric,passes)
    for factor,passes in [(.25,True),(2,False)]:
        candidate=np.column_stack([resonance(hz,rho+factor*8*2**-25)]*2)
        expect(f'modal radius {factor} tolerance',candidate,ref,metric,passes)
    return outcomes


def main():
    comparator=load(PACKAGE/'compare.py')
    cases=json.loads((PACKAGE/'cases.json').read_text())['cases']
    evaluations={e['id']:e for c in cases for e in c['evaluations']}
    assert len(cases)==24 and len(evaluations)==68
    runs=json.loads((SOURCE/'results/corpus_runs.json').read_text())
    modes=json.loads((SOURCE/'results/corpus_model.json').read_text())['modes']
    trace=json.loads((HERE/'traceability.json').read_text())['evaluations']
    names=[row['stored_name'] for row in csv.DictReader((ROOT/'analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/out/conversions.tsv').open(),delimiter='\t') if row['device']=='Corpus']
    graded=omitted=independent=0; max_freq=max_radius=max_amplitude=0
    source_checks=[]
    for row in trace:
        e=evaluations[row['evaluation']]; original=runs['runs'][row['source_run']]; c=original['case']
        assert e['parameter_order']==names and set(e['parameters'])==set(names)
        assert [e['parameters'][name] for name in names]==[float(np.float32(c['params'][str(i)])) for i in range(38)]
        assert e['sample_rate_hz']==c['fs'] and e['frames']==16384
        assert (PACKAGE/e['signal']).read_bytes()==(SOURCE/'inputs'/f"{row['source_input']}.f32").read_bytes()
        assert (PACKAGE/e['reference']).read_bytes()==(SOURCE/'raw/corpus'/f"{row['source_run']}.f32").read_bytes()
        assert sha(PACKAGE/e['reference'])==original['sha256']==row['source_render_sha256']
        if row['protocol_variant']:
            variant=next(v for v in runs['determinism'] if v['case']==row['protocol_variant'])
            change=variant['change']
            if 'block' in change: assert e['block_frames']==change['block'] and not e['before_parameters'] and not e['after_parameters']
            elif 'pre' in change:
                assert e['before_parameters']==[{'action':'set_sample_rate','hz':int(action.split()[1])} for action in change['pre']]
                assert not e['after_parameters']
            else:
                assert change['post']==['inflag 1','input zero','process 1024 512','reset',f"param 0 {int(e['parameters']['ResonanceType'])}.0"]
                assert e['after_parameters']==[{'action':'process_silence','frames':1024,'block_frames':512},{'action':'reset'},{'action':'set_parameter','name':'ResonanceType','value':int(e['parameters']['ResonanceType'])}]
            assert variant['max_abs_diff']<1e-18
        else:
            assert not e['before_parameters'] and not e['after_parameters'] and e['block_frames']==512
        if e['metric']['kind']=='modal':
            signal=np.fromfile(PACKAGE/e['reference'],dtype='<f4').reshape(16384,2).astype(float)
            source=modes[row['source_run']]
            for channel,name in enumerate(['L','R']):
                expected=[]
                for point in source[name]['modes']:
                    if point.get('resolved') and abs(point['render_hz']/point['pole_hz']-1)<1e-4:
                        expected.append({'center_hz':point['pole_hz'],'cutoff_hz':min(100,.4*point['gap_hz'])})
                    else: omitted+=1
                assert expected==e['metric']['modes'][channel] and expected
                graded+=len(expected)
                # A different linear fit parameterization checks every retained reference estimate.
                for point in expected:
                    center=point['center_hz'];cutoff=point['cutoff_hz']
                    fr,radius,amplitude=independent_mode(signal[:,channel],c['fs'],center,cutoff)
                    source_point=next(m for m in source[name]['modes'] if m.get('pole_hz')==center)
                    max_freq=max(max_freq,abs(fr-source_point['render_hz']))
                    max_radius=max(max_radius,abs(radius-source_point['render_log_radius']))
                    assert abs(fr/center-1)<1e-4
                    assert abs(fr-source_point['render_hz'])<1e-6 and abs(radius-source_point['render_log_radius'])<1e-10
                    independent+=1
        source_checks.append({'id':e['id'],'vector_signal_output_history':'matches retained evidence'})
    assert graded==1427 and omitted==174
    source_manifest=json.loads((SOURCE/'manifest.json').read_text())
    for f,entry in source_manifest['files'].items():assert sha(SOURCE/f)==entry['sha256']
    entry=source_manifest['external_inputs']['bundle:Corpus'];bundle=Path(entry['path']).read_bytes()
    assert hashlib.sha256(bundle).hexdigest()==entry['file_sha256']
    assert hashlib.sha256(bundle[entry['x86_64_offset']:entry['x86_64_offset']+entry['x86_64_size']]).hexdigest()==entry['x86_64_sha256']
    inventory=json.loads((HERE/'source-inventory.json').read_text())['files']
    for record in inventory:
        path=ROOT/record.get('retained_copy',record['path'])
        assert sha(path)==record['sha256'] and path.stat().st_size==record['bytes']
    checks=probes(comparator)
    manifest=json.loads((PACKAGE/'manifest.json').read_text());files={str(p.relative_to(PACKAGE)):p for p in PACKAGE.rglob('*') if p.is_file()}
    assert set(files)=={e['path'] for e in manifest['files']}|{'manifest.json'}
    assert not any(p.is_symlink() for p in PACKAGE.rglob('*'))
    for f in manifest['files']:assert sha(files[f['path']])==f['sha256'] and files[f['path']].stat().st_size==f['bytes']
    links=0
    deny=re.compile(r'analysis/|raw/corpus|wiki/|0x[0-9a-fA-F]{5,}|FUN_|DAT_|_ZN|::|/home/|/var/|/tmp/|DCO-\d|CreateInstanceU|SetParameterA|CalcA|xexec|Ghidra|vtable|corpus-dsp-v1')
    for f in files.values():
        if f.suffix not in {'.py','.md','.json'}:continue
        text=f.read_text();assert not deny.search(text),(f.name,deny.search(text).group())
        if f.suffix=='.md':
            for link in re.findall(r'\]\(([^)\s]+)\)',text):
                target,_,anchor=link.partition('#');dest=(f.parent/target).resolve()
                assert PACKAGE.resolve() in dest.parents and dest.is_file(),(f.name,link)
                assert not anchor,('unexpected new anchor',link)
                links+=1
    with tempfile.TemporaryDirectory(prefix='corpus-independent-export-') as tmp:
        exported=Path(tmp)/PACKAGE.name;shutil.copytree(PACKAGE,exported)
        run=subprocess.run([sys.executable,'-I','-B',str(exported/'compare.py'),str(exported/'reference')],capture_output=True,text=True)
        result=json.loads(run.stdout);assert run.returncode==0 and result['pass'] and len(result['results'])==68
        count=sum(len(r['measurements']) for r in result['results']);assert count==4601
        for p in files.values():assert p.read_bytes()==(exported/p.relative_to(PACKAGE)).read_bytes()
    return {'package_manifest_sha256':sha(PACKAGE/'manifest.json'),'case_groups':24,'evaluations':68,'retained_modes':graded,'omitted_mode_occurrences':omitted,'independent_mode_fits':independent,'maximum_frequency_difference_Hz':max_freq,'maximum_log_radius_difference':max_radius,'synthetic_metric_probes':checks,'source_checks':source_checks,'source_manifest_sha256':sha(SOURCE/'manifest.json'),'source_files_verified':len(source_manifest['files']),'source_inventory_entries_verified':len(inventory),'corpus_bundle_sha256':entry['file_sha256'],'corpus_x86_64_sha256':entry['x86_64_sha256'],'payload_files':len(manifest['files']),'markdown_links':links,'isolated_cli_exit':run.returncode,'isolated_self_measurements':count,'original_or_candidate_application_executed':False}


if __name__=='__main__':
    report=main();(HERE/'reviewer-validation.json').write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'synthetic_metric_probes','source_checks'}},indent=1))
