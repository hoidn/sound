"""Build a finite audio-comparison package from retained evidence; never runs a device."""
import csv
import hashlib
import json
import shutil
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT/'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1'
PACKAGE = HERE.with_name('device-corpus-v1')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=1, allow_nan=False)+'\n')


def build():
    assert not PACKAGE.exists(), 'Refuse to overwrite an existing candidate; remove only this generated candidate explicitly first'
    source_manifest = json.loads((SOURCE/'manifest.json').read_text())
    for file, record in source_manifest['files'].items():
        assert sha(SOURCE/file) == record['sha256'], file
    runs = json.loads((SOURCE/'results/corpus_runs.json').read_text())
    measured = json.loads((SOURCE/'results/corpus_model.json').read_text())
    table = list(csv.DictReader((ROOT/'analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/out/conversions.tsv').open(), delimiter='\t'))
    names = [r['stored_name'] for r in table if r['device']=='Corpus']
    assert len(names)==38 and len(set(names))==38
    groups = [
        ['defaults_44'], ['defaults_48'], ['mode_beam_44'], ['mode_marimba_44'],
        ['mode_string_44'], ['mode_membrane_44'], ['mode_plate_44'], ['mode_beam_48','mode_string_48'],
        ['pitch_0.25','pitch_0.5625','pitch_0.75','pitch_1'], ['detune_0.5'],
        ['decay_0.25','decay_0.5','decay_0.75','decay_0.5_48'],
        ['tone_-1','tone_-0.5','tone_0.5','tone_1'],
        ['hit_-1','hit_-0.5','hit_0','hit_0.5','hit_1'],
        [f'listen{ch}_{v}' for ch in ['L','R'] for v in ['0','0.5','1']],
        ['inharm_-0.5','inharm_0.5','bright_-1','bright_1','ratio_0.2','ratio_0.8','bleed_1'],
        ['sine_261','sine_400','sine_1000','sine_3000','sine_1000_48','drive_0','drive_1','drywet_0.25'],
        ['noise_44'],
        ['wg_pipe_44','wg_pipe_48','wg_tube_44','wg_tube_48','wg_pipe_radius_0','wg_pipe_radius_1','wg_pipe_opening_0.3','wg_tube_radius_0'],
        ['filter_on','filter_200_bw1'], ['lfo_sine'], ['startup_dry'],
        ['defaults_44']*4, ['defaults_48'], ['defaults_44','wg_tube_44']]
    reqs = [[1,4,5,6,7,8],[1,4,5,6,7,8],[5],[5],[5],[5],[5],[5],[6],[6],[7],[7],[8],[8],[5,7],[4],[4,5],[9],[10],[11],[12],[1],[12],[1,12]]
    titles = ['Default Beam at 44.1 kHz','Default Beam at 48 kHz','Beam High','Marimba High','String High','Membrane High','Plate High','Beam and String at 48 kHz','Pitch','Detune','Decay','Material','Strike positions','Pickup positions','Inharmonicity, brightness, ratio and bleed','Steady sine gain and phase','Noise band levels','Pipe and Tube','Band filter','Free-running Sine LFO','Startup gain','Host-block invariance','Sample-rate history','Warm-up and reset']
    for directory in ['signals','reference']:
        (PACKAGE/directory).mkdir(parents=True)
    shutil.copyfile(HERE/'compare_payload.py',PACKAGE/'compare.py')
    inputs = {}
    trace = []
    cases = []
    used = set()
    for number, group in enumerate(groups,1):
        case_id = f'CORPUS-AUDIO-{number:03d}'
        evaluations = []
        for offset, original in enumerate(group,1):
            record = runs['runs'][original]
            c = record['case']
            identifier = f'{case_id}-{offset:02d}'
            input_name = c['input']
            if input_name not in inputs:
                inputs[input_name]=f'signals/input-{len(inputs)+1:02d}.f32'
                assert sha(SOURCE/'inputs'/f'{input_name}.f32') == runs['inputs'][input_name]
                shutil.copyfile(SOURCE/'inputs'/f'{input_name}.f32',PACKAGE/inputs[input_name])
            reference = f'reference/{identifier}.f32'
            assert sha(SOURCE/'raw/corpus'/f'{original}.f32')==record['sha256']
            shutil.copyfile(SOURCE/'raw/corpus'/f'{original}.f32',PACKAGE/reference)
            used.add(original)
            omission = []
            if original in measured['modes']:
                modes = []
                for channel in ['L','R']:
                    eligible=[]
                    for m in measured['modes'][original][channel]['modes']:
                        if m.get('resolved') and abs(m['render_hz']/m['pole_hz']-1)<1e-4:
                            eligible.append({'center_hz':m['pole_hz'],'cutoff_hz':min(100,0.4*m['gap_hz'])})
                        else:
                            omission.append({'channel':channel,'mode':m['k'],'why':m.get('why','reference frequency outside the 1e-4 eligibility band')})
                    assert eligible, (original,channel)
                    modes.append(eligible)
                metric = {'kind':'modal','modes':modes}
            elif original.startswith(('sine_','drive_','drywet_')):
                frequency = 261.62 if input_name.startswith('sine261') else float(input_name.split('_')[0][4:])
                metric = {'kind':'sine','frequency_hz':frequency}
            elif original=='noise_44':
                metric = {'kind':'noise'}
            elif original.startswith('wg_'):
                metric = {'kind':'waveform','start_frame':4096}
            elif original.startswith('filter_'):
                metric = {'kind':'filter','start_frame':8192}
            elif original=='lfo_sine':
                metric = {'kind':'lfo'}
            elif original=='startup_dry':
                metric = {'kind':'startup'}
            else:
                raise AssertionError(original)
            actions=[]
            block=512
            variant=None
            if number==22:
                block=[64,256,333,2048][offset-1]
                variant=f'defaults_44_block{block}'
            elif number==23:
                actions=[{'action':'set_sample_rate','hz':44100},{'action':'set_sample_rate','hz':48000}]
                variant='defaults_48_via_44'
            elif number==24:
                actions=[{'action':'process_silence','frames':1024,'block_frames':512}, {'action':'reset'}, {'action':'set_parameter','name':'ResonanceType','value':0 if offset==1 else 6}]
                variant=original+'_warmup_reset'
            if variant:
                row=next(r for r in runs['determinism'] if r['case']==variant)
                assert row['max_abs_diff']<1e-6
            params = {names[int(k)]:float(np.float32(v)) for k,v in c['params'].items()}
            evaluations.append({'id':identifier,'sample_rate_hz':c['fs'],'frames':16384,'block_frames':block,
                'signal':inputs[input_name],'parameters':params,'parameter_order':names,
                'before_parameters':actions if number==23 else [],'after_parameters':actions if number==24 else [],
                'reference':reference,'metric':metric})
            trace.append({'evaluation':identifier,'draft_case':f'DCO-{number:03d}','source_run':original,'source_input':input_name,
                'source_script':str((SOURCE/'raw/corpus'/f'{original}.script').relative_to(ROOT)),
                'source_render_sha256':record['sha256'],'reference_path':reference,'protocol_variant':variant,
                'ungraded_modes':omission})
        cases.append({'id':case_id,'purpose':titles[number-1], 'requirements':[f'REQ-DEVICE-CORPUS-{i:03d}' for i in reqs[number-1]],
            'provenance':'extracted execution of original x86_64 device code; arm64 correspondence inferred; whole application not executed',
            'evaluations':evaluations})
    write_json(PACKAGE/'cases.json',{'schema':'device-audio-cases-v1','status':'staged-unreviewed','release_id':'device-corpus-v1',
        'representation':'Named comparison-domain values and generated audio; not a claimed application API or required implementation architecture',
        'sample_format':'little-endian IEEE-754 binary32, interleaved left/right, no header','cases':cases})
    write_json(HERE/'traceability.json',{'source_manifest':str((SOURCE/'manifest.json').relative_to(ROOT)),
        'source_manifest_sha256':sha(SOURCE/'manifest.json'),'evaluations':trace})
    write_json(HERE/'source-inventory.json',{'files':[{ 'path':str(f.relative_to(ROOT)), 'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted({SOURCE/'manifest.json',SOURCE/'results/corpus_runs.json',SOURCE/'results/corpus_model.json',SOURCE/'fit.py',SOURCE/'analyze_corpus.py',ROOT/'wiki/specs/device-corpus.md',ROOT/'analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/out/conversions.tsv',*(SOURCE/'inputs'/f'{n}.f32' for n in inputs),*(SOURCE/'raw/corpus'/f'{n}.{ext}' for n in used for ext in ['f32','script','log'])})]})
    print(f'{len(cases)} cases, {sum(len(c["evaluations"]) for c in cases)} evaluations, {len(used)} distinct source renders, {len(inputs)} signals')


if __name__=='__main__':
    build()
