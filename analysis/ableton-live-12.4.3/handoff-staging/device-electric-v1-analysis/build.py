"""Stage finite retained Electric outputs; never executes the original device."""
import csv
import hashlib
import importlib.util
import json
import platform
import struct
import sys
from pathlib import Path

import numpy as np
import scipy

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.with_name('device-electric-v1')
SOURCE = HERE.parents[1]/'r2/t12-electric-v1'
NAMES_TABLE = SOURCE.parent/'n5-device-mapping-v1/out/conversions.tsv'
EXCLUDED = {'p04_0': 'too few stable loud envelope windows',
            'p05_1_key36': 'too few stable loud envelope windows',
            'p05_1_key84': 'no stable loud envelope windows'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=1, allow_nan=False)+'\n')


def wav(path):
    data = path.read_bytes()
    assert data[:4] == b'RIFF' and data[8:12] == b'WAVE'
    chunks = {}
    position = 12
    while position < len(data):
        name, count = struct.unpack_from('<4sI', data, position)
        chunks[name] = data[position+8:position+8+count]
        position += 8+count+(count % 2)
    kind, channels, rate, _, align, bits = struct.unpack_from('<HHIIHH', chunks[b'fmt '])
    assert (kind, channels, align, bits) == (3, 1, 4, 32)
    return chunks[b'data'], rate


def band_starts(tag, rate, events):
    if tag.startswith('defaults_c4'):
        return [0, rate//10, int(rate*0.4), rate//2]
    if tag.startswith('preset_') and tag != 'preset_defaults_c4':
        return [int(n*rate/44100) for n in [0, 4410, 17640, 22050, 26460, 39690]]
    if tag == 'poly_2_steal': return [0, 4410, 6615, 13230]
    if tag == 'poly_2_released_first': return [0, 6615, 8820, 13230]
    if tag == 'poly_2_repeat': return [0, 2205, 6615, 13230]
    if tag == 'poly_32_steal': return [0, 4410, 9900, 13230, 30870]
    if tag == 'auto_forcevel': return [2048, 6458, 15278]
    if tag.startswith('auto_'): return [0, 4410, 13230]
    return [0, rate//10, next(e[0] for e in events if e[1] == 128)]


def main():
    original = json.loads((SOURCE/'manifest.json').read_text())
    for name, row in original['files'].items():
        path = SOURCE/name
        assert sha(path) == row['sha256'] and path.stat().st_size == row['bytes'], name
    for row in original['external_inputs'].values():
        assert sha(Path(row['path'])) == row.get('file_sha256', row.get('sha256'))
        if 'x86_64_offset' in row:
            data = Path(row['path']).read_bytes()
            for arch in ['x86_64', 'arm64']:
                section = data[row[arch+'_offset']:row[arch+'_offset']+row[arch+'_size']]
                assert hashlib.sha256(section).hexdigest() == row[arch+'_sha256']
    spec = importlib.util.spec_from_file_location('electric_measurements', PACKAGE/'compare.py')
    comparator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(comparator)
    evidence = json.loads((SOURCE/'results/cases.json').read_text())
    names = {int(r['index']): r['stored_name'] for r in csv.DictReader(NAMES_TABLE.open(), delimiter='\t')
             if r['device'] == 'LoungeLizard' and r['index']}
    names[32] = 'PerNotePitchBendRange'
    order = [names[i] for i in range(33)]
    cases, trace = [], []
    for tag, row in sorted(evidence['cases'].items()):
        if tag in EXCLUDED: continue
        ident = f'ELECTRIC-AUDIO-{len(cases)+1:03}'
        data, rate = wav(SOURCE/row['wav'])
        lines = (SOURCE/'raw'/f'{tag}.script').read_text().splitlines()
        initial = [line.split()[1:] for line in lines if line.startswith('param ')][:33]
        assert [int(v[0]) for v in initial] == list(range(33))
        assert all(float(np.float32(v)) == float(np.float32(row['host'][i])) for i, v in initial)
        captured = [line.split()[1:] for line in lines if line.startswith('event ')]
        warm = 11264 if rate == 44100 else 12288
        assert [[int(f)-warm, int(s,0), int(k), int(v)] for f,s,k,v in captured] == row['events']
        assert sum(int(line.split()[1]) for line in lines if line.startswith('process ')) == warm+row['frames']
        assert rate == row['fs'] and len(data) == 4*row['frames'] and sha(SOURCE/row['wav']) == row['wav_sha256']
        (PACKAGE/'reference'/f'{ident}.f32').write_bytes(data)
        signal = 'signals/zero-'+str(row['frames'])+'.f32'
        (PACKAGE/signal).write_bytes(bytes(len(data)))
        onset = row['measures']['onset']
        metric = {'kind': 'silence' if onset is None else 'electric', 'partials': []}
        if onset is not None:
            event_frame = row['events'][0][0]
            period = rate//1000
            grid = period*(event_frame//period)
            if grid < 512*(event_frame//512): grid += period
            lower = grid+period
            metric.update(band_start_frames=band_starts(tag, rate, row['events']),
                          band_centres_hz=evidence['meta']['band_centres_hz'],
                          graded=row['graded'], tolerances=row['tolerances'],
                          onset_min_frame=lower if 0 <= onset-lower <= 3 else onset,
                          onset_max_frame=lower+3 if 0 <= onset-lower <= 3 else onset)
            assert len(metric['band_start_frames']) == len(row['measures']['bands'])
            if row['f0'] is not None:
                harmonic = sorted({i+1 for k in ['freq', 'amp', 'decay'] for i in row['graded'][k]})
                metric.update(partials=harmonic, fundamental_center_hz=row['f0'],
                              partial_start_frame=onset+int(0.03*rate),
                              partial_stop_frame=next(e[0] for e in row['events'] if e[1] == 128))
        parameters = {names[int(i)]: float(np.float32(v)) for i, v in row['host'].items()}
        events = [{'frame': f, 'type': 'note_on' if status == 144 else 'note_off',
                   'key': key, 'velocity': velocity, 'channel': 1}
                  for f, status, key, velocity in row['events']]
        history = []
        for frame, command in row['extra']:
            _, index, value = command.split()
            history.append({'frame': frame, 'action': 'set_parameter', 'parameter': names[int(index)], 'value': float(np.float32(value))})
        evaluation = dict(id=ident, sample_rate_hz=rate, frames=row['frames'], channels=1,
                          block_frames=512, warm_up_frames=11264 if rate == 44100 else 12288,
                          parameter_order=order, parameters=parameters, events=events,
                          during_processing=history, signal=signal, reference='reference/'+ident+'.f32', metric=metric)
        value = np.frombuffer(data, '<f4').astype(np.float64)
        evaluation['expected_measurements'] = comparator.measure(value, evaluation)
        assert comparator.compare(value, evaluation)['pass']
        req = ['001']
        if tag.startswith('auto_'): req += ['014']
        elif tag.startswith('poly_'): req += ['005']
        elif tag.startswith('key_'): req += ['006']
        elif tag.startswith('vel_'): req += ['007']
        elif tag.startswith('p') and tag[1:3].isdigit():
            index = int(tag[1:3]); req += ['008' if 4 <= index <= 13 else '009' if 14 <= index <= 20 else '010' if 27 <= index <= 29 else '011' if index in [21,22,23,24] else '012' if index in [2,25,26] else '006']
        if rate == 48000: req += ['015']
        cases.append({'id': ident, 'requirements': ['REQ-DEVICE-ELECTRIC-'+r for r in req],
                      'expectation_provenance': 'extracted execution of original x86_64 code with substituted mathematical libraries',
                      'reference_application_execution': 'not-run', 'candidate_execution': 'not-run',
                      'evaluations': [evaluation]})
        trace.append(dict(case=ident, source_case=tag, source_wav=row['wav'], source_wav_sha256=row['wav_sha256'],
                          source_script='raw/'+tag+'.script', source_script_sha256=sha(SOURCE/'raw'/f'{tag}.script'),
                          raw_reference_sha256=sha(PACKAGE/evaluation['reference']),
                          metric_source='results/cases.json/cases/'+tag,
                          metric_narrowing='Frozen stable masks; no random-level or unlisted-output expectation'))
    dump(PACKAGE/'cases.json', {'schema': 'finite-device-audio-v1', 'status': 'staged-unreviewed', 'cases': cases})
    dump(HERE/'traceability.json', {'source_packet': str(SOURCE), 'excluded': EXCLUDED, 'cases': trace})
    dump(HERE/'source-inventory.json', {'original_manifest_sha256': sha(SOURCE/'manifest.json'),
        'manifest_payloads_verified': len(original['files']), 'parameter_names_table_sha256': sha(NAMES_TABLE),
        'identity': original['external_inputs'], 'files': original['files']})
    dump(HERE/'environment.json', {'python': sys.version, 'platform': platform.platform(), 'numpy': np.__version__, 'scipy': scipy.__version__, 'original_code_executed': False})
    print('staged', len(cases), 'finite Electric evaluations; excluded', len(EXCLUDED))


if __name__ == '__main__': main()
