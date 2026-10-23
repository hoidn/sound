"""Read-only finite owner text/input checks. No comparator or original-code import."""
from pathlib import Path
import copy
import hashlib
import json
import math
import re
import struct
import sys

P = Path(__file__).resolve().parent
REFERENCE_SHA = 'a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829'
BEFORE_SHA = 'aba64f5c420091617c16d28c9f0d2437c0eacf67ed1940bfe27250644038eecf'
KIND = 'noteoff_decay_zero_waveform'


def load(name):
    return json.loads((P / name).read_text())


def identity(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def verify(row):
    got = identity(Path(row['path']))
    assert all(got[k] == row[k] for k in ['bytes', 'sha256']), row['path']


def case_rows(text):
    return re.findall(r'^\| DCO-\d{3} \|.*$', text, re.M)


def requirement_ids(text):
    return re.findall(r'^### (REQ-DEVICE-CORPUS-\d{3}) ', text, re.M)


def requirement_body(text, index):
    start = text.index(f'### REQ-DEVICE-CORPUS-{index:03d} ')
    end = text.index(f'### REQ-DEVICE-CORPUS-{index+1:03d} ', start)
    return text[start:end]


def validate_case(case):
    assert case['id'] == 'DCO-032' and case['kind'] == 'P'
    assert case['requirements'] == ['REQ-DEVICE-CORPUS-001', 'REQ-DEVICE-CORPUS-013']
    assert case['candidate_or_application_grade'] is None
    ev = case['evaluation']
    assert ev['metric'] == {'kind': KIND}
    assert (ev['sample_rate_hz'], ev['frames'], ev['block_frames']) == (44100, 16384, 512)
    assert ev['signal'] == 'reuse exact released signals/input-01.f32'
    assert ev['before_parameters'] == ev['after_parameters'] == []
    original = json.loads((P.parent / 'corpus-owner-r5/cases-additions.json').read_text())[0]
    assert ev['parameter_order'] == original['evaluation']['parameter_order']
    assert len(ev['parameters']) == len(ev['parameter_order']) == 38
    script = (P.parent / 'depth-corpus-midi-noteoff-decay-zero/raw/gate1-off.script').read_text()
    wanted = [line.split() for line in script.splitlines() if line.startswith('param ')]
    assert [int(line[1]) for line in wanted] == list(range(38))
    assert [struct.pack('<f', ev['parameters'][key]) for key in ev['parameter_order']] == [struct.pack('<f', float(line[2])) for line in wanted]
    assert struct.pack('<f', ev['parameters']['DecayOnNoteOff']) == bytes(4)
    assert (ev['parameters']['MidiPitch'], ev['parameters']['MidiGate'], ev['parameters']['LfoOnOff']) == (1., 1., 0.)
    assert ev['events'] == [
        {'frame': 1537, 'kind': 'note_on', 'channel': 0, 'key': 60, 'velocity': 100},
        {'frame': 3073, 'kind': 'note_off', 'channel': 0, 'key': 60, 'velocity': 64}]
    assert [line for line in script.splitlines() if line.startswith('event ')] == ['event 1537 0x90 60 100', 'event 3073 0x80 60 64']
    assert ev['reference'] == {'path': '../depth-corpus-midi-noteoff-decay-zero/raw/gate1-off.f32', 'bytes': 131072, 'sha256': REFERENCE_SHA}
    prefix = case['prefix_scope']
    assert prefix == original['prefix_scope'] and prefix['expected_audio'] is None
    rules = case['metric_rules']
    assert rules['kind'] == KIND and rules['frames_inclusive'] == [4096, 16383]
    assert rules['max_relative_RMS'] == 0.01 and rules['per_channel_independent'] is True
    assert rules['formula'] == 'sqrt(math.fsum((candidate-reference)**2)/math.fsum(reference**2))'
    assert rules['full_file_finite_and_exact_length'] is True
    assert rules['positive_scored_energy_in_each_reference_and_candidate_channel'] is True
    assert rules['reference_identity_required'] is True
    assert rules['alignment_gain_phase_offset_fitting_or_channel_mixing'] is False
    limits = case['scope_limits']
    assert limits == {'finite_prefix_corruption_can_pass': True, 'zero_entire_last8192_can_pass': True,
                      'tail_cutoff_or_silence_grade': False, 'observed_process_flags_expected': None,
                      'host34_stored_or_UI_conversion_proved': False, 'Ramp_sensitivity_or_applicability_transfer': False,
                      'B_specific_uncertainty_or_repeatability_calibration': False, 'new_invariance_claims': False,
                      'source_admission_or_Live_route_proved': False, 'general_gate_or_decay_law': None}
    protocol = copy.deepcopy(original['constant_protocol'])
    protocol.pop('no_noteoff_or_other_events')
    protocol.pop('held_note_scope')
    protocol['no_unlisted_events'] = True
    assert case['constant_protocol'] == protocol
    assert case['format'] == original['format']


def main():
    if sys.argv[1:] not in [['--check'], ['--check-draft']]:
        raise SystemExit('Read-only --check or --check-draft only; no write/seal/capture/comparator mode.')
    inputs = load('inputs.json')
    # All providers are immutable as-of files. No current canonical/wiki equality gate.
    watched = {Path(r['path']) for r in inputs['immutable_pins'] + inputs['historical_consumer_pins']}
    watched.update(q for q in P.iterdir() if q.is_file())
    before_watch = {str(q): identity(q) for q in watched}
    for row in inputs['immutable_pins'] + inputs['historical_consumer_pins']:
        verify(row)
    binding = inputs['criterion_review_binding']
    if sys.argv[1:] == ['--check'] or (P / 'manifest.json').exists():
        assert binding['status'] == 'independently approved finite engineering method only' and binding['pin'] is not None
        verify(binding['pin'])
        review = json.loads(Path(binding['pin']['path']).read_text())
        assert review['required_findings'] == [] and review['disposition'] == binding['disposition']
        assert review['disposition'].startswith('APPROVED finite engineering method')
    if (P / 'manifest.json').exists():
        seal = load('manifest.json')
        assert {q.name for q in P.iterdir() if q.is_file() and q.name != 'manifest.json'} == {r['path'] for r in seal['files']}
        for row in seal['files']:
            got = identity(P / row['path'])
            assert all(got[k] == row[k] for k in ['bytes', 'sha256'])
    before = (P / 'spec-before-r5.md').read_text()
    after = (P / 'spec-r6.md').read_text()
    delta = load('delta.json')
    assert len(before.encode()) == delta['before_bytes'] == 51090
    assert hashlib.sha256(before.encode()).hexdigest() == delta['before_sha256'] == BEFORE_SHA
    reconstructed = before
    for op in delta['replacements']:
        if op['operation'] == 'append':
            reconstructed += op['after']
        else:
            assert reconstructed.count(op['before']) == 1
            reconstructed = reconstructed.replace(op['before'], op['after'])
    assert reconstructed == after and len(after.encode()) == delta['after_bytes']
    assert hashlib.sha256(after.encode()).hexdigest() == delta['after_sha256']
    assert requirement_ids(before) == requirement_ids(after) == [f'REQ-DEVICE-CORPUS-{i:03d}' for i in range(1, 14)]
    for index in range(1, 13):
        assert requirement_body(before, index) == requirement_body(after, index)
    old_rows, new_rows = case_rows(before), case_rows(after)
    assert len(old_rows) == 31 and len(new_rows) == 32 and new_rows[:31] == old_rows
    assert [row.split('|')[3].strip() for row in new_rows].count('U') == 4
    assert new_rows[25] == old_rows[25] and '| DCO-026 | 013 | U |' in new_rows[25]
    assert new_rows[-1].startswith('| DCO-032 | 001, 013 | P |')
    cases = load('cases-additions.json')
    assert len(cases) == 1
    validate_case(cases[0])
    raw = (P / cases[0]['evaluation']['reference']['path']).read_bytes()
    assert len(raw) == 131072 and hashlib.sha256(raw).hexdigest() == REFERENCE_SHA
    frames = list(struct.iter_unpack('<ff', raw))
    assert all(math.isfinite(v) for frame in frames for v in frame)
    assert all(math.fsum(frame[ch]*frame[ch] for frame in frames[4096:]) > 0 for ch in (0, 1))
    # Integrity-only negative fixtures, not numerical comparator/device simulations.
    rejected = []
    def reject(label, mutate):
        bad = copy.deepcopy(cases[0])
        mutate(bad)
        try:
            validate_case(bad)
        except AssertionError:
            rejected.append(label)
            return
        raise AssertionError('Unsafe fixture accepted: ' + label)
    reject('wrong-case-identity', lambda c: c.update(id='DCO-033'))
    reject('old-host34-endpoint', lambda c: c['evaluation']['parameters'].update(DecayOnNoteOff=1.))
    reject('negative-zero-endpoint', lambda c: c['evaluation']['parameters'].update(DecayOnNoteOff=-0.))
    reject('extra-adapter-subtraction', lambda c: c['evaluation']['events'][1].update(frame=3072))
    reject('Ramp-kind-transfer', lambda c: c['evaluation'].update(metric={'kind': 'ramp_waveform'}))
    reject('widened-budget', lambda c: c['metric_rules'].update(max_relative_RMS=0.02))
    reject('tail-exclusion', lambda c: c['metric_rules'].update(frames_inclusive=[4096, 8191]))
    reject('channel-average', lambda c: c['metric_rules'].update(per_channel_independent=False))
    reject('graded-prefix', lambda c: c['prefix_scope'].update(expected_audio='silence'))
    reject('missing-energy-guard', lambda c: c['metric_rules'].update(positive_scored_energy_in_each_reference_and_candidate_channel=False))
    reject('wrong-reference', lambda c: c['evaluation']['reference'].update(sha256='0'*64))
    reject('outputflag-law', lambda c: c['scope_limits'].update(observed_process_flags_expected=0))
    reject('tailzero-limit-erased', lambda c: c['scope_limits'].update(zero_entire_last8192_can_pass=False))
    reject('application-pass', lambda c: c.update(candidate_or_application_grade='pass'))
    criterion_pin = next(r for r in inputs['immutable_pins'] if r['path'].endswith('/depth-corpus-midi-noteoff-decay-zero-criterion-proposal/criterion.json'))
    criterion = json.loads(Path(criterion_pin['path']).read_text())
    assert criterion['metric_kind_proposed'] == KIND and criterion['threshold'] == 0.01 and criterion['reference_sha256'] == REFERENCE_SHA
    assert inputs['candidate_grade'] is None and inputs['new_original_calls'] == 0
    history = load('historical-consumers.json')
    assert history['matched_files'] == 39 and history['immutable_historical_files'] == 38 and history['active_mutable_files'] == 1
    assert len(inputs['historical_consumer_pins']) == 38
    # Check real links in README and the spec snapshot's original canonical context.
    links = 0
    for content, base in [((P/'README.md').read_text(), P), (after, Path(inputs['snapshot_link_base']))]:
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
            if target.startswith(('https:', 'http:', '#')):
                continue
            path = target.split('#', 1)[0]
            assert (base / path).resolve().exists(), target
            links += 1
    for q in P.iterdir():
        if q.is_file() and q.suffix in ['.md', '.json', '.py']:
            text = q.read_text()
            assert text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines()), q
    assert before_watch == {str(q): identity(q) for q in watched}
    print(json.dumps({'status': 'PASS finite owner data integrity only; no numerical comparison or application grade',
                      'sealed': (P/'manifest.json').exists(), 'method_binding': binding['status'],
                      'requirements': 13, 'cases': 32, 'old_case_rows_exact': 31, 'clauses_001_012_literal': True,
                      'finite_proposed': 28, 'U_cases': 4, 'new_cases': 1, 'literal_operations': len(delta['replacements']),
                      'negative_fixtures': rejected, 'links': links, 'watched': len(watched), 'watch_unchanged': True,
                      'new_original_calls': 0, 'comparator_calls': 0, 'application_grade': None}, indent=2))


if __name__ == '__main__':
    main()
