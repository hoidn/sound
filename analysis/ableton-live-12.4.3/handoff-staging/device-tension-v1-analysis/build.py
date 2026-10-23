"""Copy calibrated finite Tension references without running any original code."""
import csv
import hashlib
import json
import platform
import re
import struct
import sys
from pathlib import Path

import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.with_name('device-tension-v1')
SOURCE = HERE.parents[1]/'r2/t12-tension-v1'
TABLE = SOURCE.parent/'n6-device-tables-v1/out/conversions.tsv'
CHAOTIC = {'damper_mass_0', 'exc_bow', 'bow_x1', 'preset_cello'}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data): path.write_text(json.dumps(data, indent=1, allow_nan=False)+'\n')


def wav(path):
    data = path.read_bytes(); chunks = {}; position = 12
    assert data[:4] == b'RIFF' and data[8:12] == b'WAVE'
    while position < len(data):
        name, count = struct.unpack_from('<4sI', data, position)
        chunks[name] = data[position+8:position+8+count]; position += 8+count+(count % 2)
    kind, channels, rate, _, align, bits = struct.unpack_from('<HHIIHH', chunks[b'fmt '])
    assert (kind, channels, align, bits) == (3, 1, 4, 32)
    return chunks[b'data'], rate


def main():
    manifest = json.loads((SOURCE/'manifest.json').read_text())
    for name, row in manifest['files'].items():
        assert sha(SOURCE/name) == row['sha256'] and (SOURCE/name).stat().st_size == row['bytes'], name
    for row in manifest['external_inputs'].values():
        assert sha(Path(row['path'])) == row.get('file_sha256', row.get('sha256'))
        if 'x86_64_offset' in row:
            data = Path(row['path']).read_bytes()
            for arch in ['x86_64', 'arm64']:
                part = data[row[arch+'_offset']:row[arch+'_offset']+row[arch+'_size']]
                assert hashlib.sha256(part).hexdigest() == row[arch+'_sha256']
    runs = json.loads((SOURCE/'results/runs.json').read_text())['runs']
    measures = json.loads((SOURCE/'results/measure.json').read_text())
    sensitivity = json.loads((SOURCE/'results/sensitivity.json').read_text())
    rows = [r for r in csv.DictReader(TABLE.open(), delimiter='\t') if r['device'] == 'StringStudio' and r['index']]
    names = {int(r['index']):r['stored_name'] for r in rows if not r['stored_name'].startswith('(')}
    for row in rows:
        if row['stored_name'].startswith('(second output'):
            index = int(row['index']); parent = int(re.search(r'of index (\d+)', row['stored_name']).group(1))
            names[index] = names[parent]+('.Enabled' if parent == 0 else '.SlopeFlag' if parent == 91 else '.Negative')
    names[121] = 'PerNotePitchBendRange'
    order = [names[i] for i in sorted(names)]
    assert len(order) == len(set(order)) == 129
    cases, trace = [], []
    excluded = {tag: 'chaotic: no statistical comparator released' if tag in CHAOTIC else 'no retained per-setting sensitivity study'
                for tag in runs if tag in CHAOTIC or tag not in sensitivity}
    for tag in [t for t in sensitivity if not t.startswith('_') and t not in CHAOTIC]:
        row, measured = runs[tag], measures[tag]
        ident = f'TENSION-AUDIO-{len(cases)+1:03}'
        data, rate = wav(SOURCE/'raw'/f'{tag}.wav')
        assert len(data) == row['frames']*4 and rate == row['fs'] and sha(SOURCE/'raw'/f'{tag}.wav') == row['wav_sha256']
        (PACKAGE/'reference'/f'{ident}.f32').write_bytes(data)
        signal = 'signals/zero-'+str(row['frames'])+'.f32'; (PACKAGE/signal).write_bytes(bytes(len(data)))
        lines = (SOURCE/'raw'/f'{tag}.script').read_text().splitlines()
        initial = [line.split()[1:] for line in lines if line.startswith('param ')]
        assert [int(i) for i,v in initial] == sorted(names)
        parameters = {names[int(i)]: float(np.float32(v)) for i,v in initial}
        events = [[int(f), int(s,0), int(k), int(v)] for f,s,k,v in [line.split()[1:] for line in lines if line.startswith('event ')]]
        assert events == row['events']
        assert [line for line in lines if line.startswith('process ')] == [f"process {row['frames']} 512"]
        onset = measured['first_nonzero']; off = next(e[0] for e in events if e[1] == 128)
        if tag == 'exc_bounce':
            metric = dict(kind='repeated-strike', onset_frame=onset, waveform_windows=[[onset,row['frames'],0.005,'whole ringing waveform']], partials=[])
        else:
            held = measured['held']; f1 = held['partials'][0]['hz']/held['partials'][0]['k']
            points = [dict(harmonic=p['k'],center_hz=p['hz']) for p in held['partials'] if p['level_db'] >= -60]
            assert points
            metric = dict(kind='stable', onset_frame=onset,
                          waveform_windows=[[onset,off,0.003,'held waveform'],[off,row['frames'],0.01,'release waveform']],
                          partials=points, partial_window=held['window'], partial_cutoff_hz=min(150,0.3*f1),
                          amplitude_normalizer=max(p['amp'] for p in held['partials']))
        evaluation = dict(id=ident, sample_rate_hz=rate, frames=row['frames'], channels=1, block_frames=512,
                          warm_up_frames=0, parameter_order=order, parameters=parameters,
                          events=[dict(frame=f,type='note_on' if s==144 else 'note_off',key=k,velocity=v,channel=1) for f,s,k,v in events],
                          signal=signal, reference='reference/'+ident+'.f32', metric=metric)
        req = ['001']
        if tag.startswith('note_'): req += ['004','005']
        elif tag.startswith('vel'): req += ['007']
        elif tag.startswith(('exc_','plk_','ham_','pos_')): req += ['006']
        elif tag.startswith('str_'): req += ['005']
        elif tag.startswith('damper_'): req += ['008']
        elif tag.startswith('term_'): req += ['009']
        elif tag.startswith('pickup_'): req += ['010']
        elif tag.startswith('body_'): req += ['011']
        elif tag.startswith('filt_'): req += ['012']
        else: req += ['005']
        cases.append(dict(id=ident, requirements=['REQ-DEVICE-TENSION-'+r for r in req],
                          expectation_provenance='extracted execution of original x86_64 code with substituted libraries',
                          reference_application_execution='not-run',candidate_execution='not-run',evaluations=[evaluation]))
        trace.append(dict(case=ident, source_case=tag, source_wav='raw/'+tag+'.wav',source_wav_sha256=row['wav_sha256'],
                          source_script_sha256=sha(SOURCE/'raw'/f'{tag}.script'),raw_reference_sha256=sha(PACKAGE/evaluation['reference']),
                          measurement_source='results/measure.json/'+tag,sensitivity_source='results/sensitivity.json/'+tag,
                          retained_perturbation_maxima=sensitivity[tag]))
    dump(PACKAGE/'cases.json',dict(schema='finite-device-audio-v1',status='staged-unreviewed',cases=cases))
    dump(HERE/'traceability.json',dict(source_packet=str(SOURCE),excluded=excluded,cases=trace))
    dump(HERE/'source-inventory.json',dict(original_manifest_sha256=sha(SOURCE/'manifest.json'),manifest_payloads_verified=len(manifest['files']),
                                        identity=manifest['external_inputs'],files=manifest['files']))
    dump(HERE/'environment.json',dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__,original_code_executed=False))
    print('staged',len(cases),'Tension evaluations; excluded',len(excluded))


if __name__ == '__main__': main()
