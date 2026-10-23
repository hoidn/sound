"""Independent finite fixture/metric audit; no device execution or synthesis."""
import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PACKAGE = HERE.with_name('device-analog-v1')
SOURCE = ROOT/'analysis/ableton-live-12.4.3/r2/t12-analog-v1'
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((SOURCE/'manifest.json').read_text())
    for name, record in manifest['files'].items():
        assert sha(SOURCE/name) == record['sha256'] and (SOURCE/name).stat().st_size == record['bytes']
    external = manifest['external_inputs']
    executable = Path(external['bundle:Analog']['path'])
    assert sha(executable) == external['bundle:Analog']['file_sha256']
    body = executable.read_bytes(); info = external['bundle:Analog']
    assert hashlib.sha256(body[info['x86_64_offset']:info['x86_64_offset']+info['x86_64_size']]).hexdigest() == info['x86_64_sha256']
    info = external['helper-corpus:Analog']['slice']
    assert hashlib.sha256(body[info['slice_offset']:info['slice_offset']+info['slice_size']]).hexdigest() == info['slice_sha256']
    for name, record in external.items():
        if name.startswith('n6-'): assert sha(Path(record['path'])) == record['sha256']
    rows = [r for r in csv.DictReader(Path(external['n6-device-tables-v1/out/conversions.tsv']['path']).open(), delimiter='\t')
            if r['device'] == 'UltraAnalog' and r['index']]
    names = []
    for r in rows:
        name = r['stored_name']
        if name.startswith('('): name = rows[int(re.search(r'index (\d+)', name).group(1))]['stored_name']+'.secondary'
        names.append(name.replace('/ToggleDummy','/Enabled').replace('DummyPerNotePitchBendRange','PerNotePitchBendRangeComparison'))
    captures = json.loads((SOURCE/'results/cases.json').read_text())
    traces = json.loads((HERE/'traceability.json').read_text())['evaluations']
    groups = json.loads((PACKAGE/'cases.json').read_text())['cases']
    evaluations = {e['id']:e for c in groups for e in c['evaluations']}
    original_ids = set(); stationary = frequencies = harmonics = onsets = 0
    for row in traces:
        e = evaluations[row['evaluation']]; original = captures[row['draft_case']]
        record = captures[row['source_capture']]; original_ids.add(row['source_capture'])
        assert e['frames'] == record['frames'] and e['sample_rate_hz'] == record['fs'] and e['block_frames'] == original['block']
        if 'source' in original: assert original['bit_identical_to_source'] and original['source'] == row['source_capture']
        rate, signal = wavfile.read(ROOT/row['source_wav'])
        expanded = np.column_stack((signal, signal)).astype('<f4').tobytes()
        assert expanded == (PACKAGE/e['reference']).read_bytes()
        assert hashlib.sha256(expanded).hexdigest() == record['f32_sha256']
        assert (PACKAGE/e['signal']).read_bytes() == bytes(8*e['frames'])
        lines = (ROOT/row['source_script']).read_text().splitlines()
        parameter_lines = [line.split() for line in lines if line.startswith('param ')]
        assert e['parameter_order'] == names and [int(x[1]) for x in parameter_lines] == list(range(203))
        assert len(e['parameters']) == len(set(names)) == 203
        assert all(np.float32(e['parameters'][name]) == np.float32(x[2]) for name,x in zip(names,parameter_lines))
        for key in ['NoiseToggle','KeyboardError','VibratoToggle','VibratoError','PortamentoToggle','SignalChain1/LFOToggle','SignalChain2/LFOToggle']:
            assert e['parameters'][key] == 0
        for chain in [1,2]: assert e['parameters'][f'SignalChain{chain}/OscillatorWaveShape'] in [0,1,2]
        public_events = [(r['frame'], (144 if r['kind']=='note_on' else 128)+r['channel'],r['key'],r['velocity']) for r in e['events']]
        captured_events = [(int(x[1]),int(x[2],0),int(x[3]),int(x[4])) for x in map(str.split,lines) if x and x[0]=='event']
        assert public_events == captured_events == sorted(map(tuple,record['events']),key=lambda x:x[0])
        assert [line for line in lines if line.startswith('process ')] == [f"process {record['frames']} {record['block']}"]
        assert 'inflag 0' in lines and 'input zero' in lines and not any(line.startswith(('transport ','reset')) for line in lines)
        nz = np.flatnonzero(signal); assert len(nz) and e['metric']['first_nonzero'] == nz[0]
        last = int(nz[-1]) if nz[-1] < len(signal)-1 else None
        assert e['metric']['last_nonzero'] == last
        assert len(e['metric']['onset_windows']) == sum(r['kind']=='note_on' and r['velocity']>0 for r in e['events'])
        for start,stop in e['metric']['onset_windows']: assert 0 <= start < stop <= e['frames'] and stop-start <= 2048
        onsets += len(e['metric']['onset_windows'])
        for point in e['metric']['steady_windows']:
            start,stop,center = point['start_frame'],point['stop_frame'],point['center_hz']
            assert stop-start >= max(.2*rate,25*rate/center)
            assert 0 < point['harmonic_count'] <= 40 and point['harmonic_count']*center <= rate/2
            assert point['graded_harmonics'] and len(point['graded_harmonics']) == len(set(point['graded_harmonics']))
            assert point['frequency_graded'] == (center >= 100)
            # Independent complex-exponential least squares, rather than the payload's real sine/cosine basis.
            sample_time = np.arange(stop-start)/rate
            orders = np.arange(-point['harmonic_count'],point['harmonic_count']+1)
            design = np.exp(2j*np.pi*sample_time[:,None]*center*orders)
            coefficients = np.linalg.lstsq(design,signal[start:stop].astype(float),rcond=None)[0]
            amplitudes = 2*np.abs(coefficients[orders>0])
            eligible = (np.flatnonzero(amplitudes >= .01*amplitudes.max())+1).tolist()
            assert eligible == point['graded_harmonics']
            stationary += 1; frequencies += point['frequency_graded']; harmonics += len(point['graded_harmonics'])
    spec = importlib.util.spec_from_file_location('independent_analog_measurement_audit',PACKAGE/'compare.py')
    tool = importlib.util.module_from_spec(spec); spec.loader.exec_module(tool)
    analytic = []
    for rate, center in [(44100,110.123),(48000,399.987),(44100,1699.25)]:
        n = np.arange(rate)/rate; truth = center+.009
        tone = (.31*np.sin(2*np.pi*truth*n-.71)+.017*np.cos(6*np.pi*truth*n+.2)-.003).astype('<f4').astype(float)
        estimated = tool.frequency(tone,center,rate)
        amplitude, dc = tool.harmonic_fit(tone,truth,rate,12)
        assert abs(estimated-truth)/truth < 1e-7
        assert abs(amplitude[0]-.31) < 1e-8 and abs(amplitude[2]-.017) < 1e-8 and abs(dc+.003) < 1e-8
        assert max(amplitude[[i for i in range(12) if i not in [0,2]]]) < 1e-8
        analytic.append(dict(rate=rate,frequency_hz=truth,relative_frequency_error=abs(estimated-truth)/truth))
    report = dict(status='pass',scope='independent fixture and signal-measurement audit only; no original-code/application execution',
        manifest_sha256=sha(PACKAGE/'manifest.json'),source_manifest_files=len(manifest['files']),case_groups=len(groups),evaluations=len(evaluations),
        unique_captures=len(original_ids),stationary_windows=stationary,frequency_checks_per_channel=frequencies,
        selected_harmonics_per_channel=harmonics,onset_windows_per_channel=onsets,analytic_checks=analytic)
    (HERE/'reviewer-source-metric-check.json').write_text(json.dumps(report,indent=1)+'\n')
    print(json.dumps(report,indent=1))


if __name__ == '__main__': main()
