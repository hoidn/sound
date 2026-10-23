"""One current structural check. Stdlib/data only; no comparator, fit, model or device call."""
from pathlib import Path
import copy
import hashlib
import json
import math
import re
import struct
import sys

PRIVATE = Path(__file__).resolve().parent
STAGE = PRIVATE.parent / 'device-corpus-v4'
ROOT = PRIVATE.parents[3]
OLD = ROOT / 'handoff/device-corpus-v3'
FULL = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
B_SHA = 'a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check():
    inputs = json.loads((PRIVATE / 'inputs.json').read_text())
    before = {p: p.read_bytes() for p in STAGE.rglob('*') if p.is_file()}
    for pin in inputs['pins']:
        p = Path(pin['path']); raw = p.read_bytes()
        assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256']
        before[p] = raw
    manifest = json.loads((OLD / 'manifest.json').read_text())
    old_fixtures = []
    for row in manifest['files']:
        source = OLD / row['path']; raw = source.read_bytes(); before[source] = raw
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
        if source.suffix == '.f32':
            assert (STAGE / row['path']).read_bytes() == raw
            old_fixtures.append(row['path'])
    assert len(old_fixtures) == 80
    old = json.loads((OLD / 'cases.json').read_text())
    current = json.loads((STAGE / 'cases.json').read_text())
    script = (FULL / 'depth-corpus-midi-noteoff-decay-zero/gate1-off.script').read_text()
    rows = [s.split() for s in script.splitlines() if s.startswith('param ')]
    assert [int(r[1]) for r in rows] == list(range(38))
    order = old['cases'][24]['evaluations'][0]['parameter_order']
    expected = {name: struct.unpack('<f', struct.pack('<f', float(r[2])))[0] for name, r in zip(order, rows)}

    def validate(data):
        assert data['release_id'] == 'device-corpus-v4'
        assert data['status'] == 'draft-pending-parent-adoption-and-independent-handoff-review'
        assert data['cases'][:25] == old['cases'] and len(data['cases']) == 26
        group = data['cases'][25]
        assert group['id'] == 'CORPUS-AUDIO-026'
        assert group['requirements'] == ['REQ-DEVICE-CORPUS-001', 'REQ-DEVICE-CORPUS-013']
        assert len(group['evaluations']) == 1
        e = group['evaluations'][0]
        assert e['id'] == 'CORPUS-AUDIO-026-01'
        assert e['reference'] == 'reference/CORPUS-AUDIO-026-01.f32'
        assert e['metric'] == {'kind': 'noteoff_decay_zero_waveform'}
        assert e['sample_rate_hz'] == 44100 and e['frames'] == 16384 and e['block_frames'] == 512
        assert e['before_parameters'] == [] and e['after_parameters'] == []
        assert e['signal'] == old['cases'][24]['evaluations'][0]['signal']
        assert e['parameter_order'] == order and len(e['parameters']) == 38
        assert list(e['parameters']) == order
        assert all(struct.pack('<f', e['parameters'][k]) == struct.pack('<f', expected[k]) for k in order)
        assert e['events'] == [dict(frame=1537, kind='note_on', channel=0, key=60, velocity=100),
                               dict(frame=3073, kind='note_off', channel=0, key=60, velocity=64)]
    validate(current)
    rejected = []
    for kind in ('old-object', 'missing-off', 'extra-minus1', 'gate0', 'endpoint1', 'wrong-metric', 'missing-order', 'false-released'):
        data = copy.deepcopy(current); e = data['cases'][25]['evaluations'][0]
        if kind == 'old-object':
            data['cases'][0]['purpose'] += ' changed'
        elif kind == 'missing-off': e['events'].pop()
        elif kind == 'extra-minus1': e['events'][1]['frame'] = 3072
        elif kind == 'gate0': e['parameters']['MidiGate'] = 0.0
        elif kind == 'endpoint1': e['parameters']['DecayOnNoteOff'] = 1.0
        elif kind == 'wrong-metric': e['metric']['kind'] = 'ramp_waveform'
        elif kind == 'missing-order': e['parameter_order'].pop()
        else: data['status'] = 'released'
        try: validate(data)
        except AssertionError: rejected.append(kind)
        else: raise AssertionError(kind)
    assert len(rejected) == 8
    reference = STAGE / 'reference/CORPUS-AUDIO-026-01.f32'
    assert len(reference.read_bytes()) == 131072 and sha(reference.read_bytes()) == B_SHA
    assert (STAGE / 'compare.py').read_bytes() == (PRIVATE / 'comparator-preparation/compare.py').read_bytes()
    assert sha((STAGE / 'compare.py').read_bytes()) == '9964de11da79eb61c0624d34e402d238cd5c466093d15ccc91fd630ac4c54110'
    f32 = [p for p in STAGE.rglob('*.f32')]
    assert len(f32) == 81
    for p in f32:
        raw = p.read_bytes(); assert len(raw) == 131072
        assert all(math.isfinite(v) for row in struct.iter_unpack('<ff', raw) for v in row)
    refs = [e['reference'] for c in current['cases'] for e in c['evaluations']]
    assert len(refs) == 72 and len(set(refs)) == 72
    for c in current['cases']:
        for e in c['evaluations']:
            assert (STAGE / e['signal']).exists() and (STAGE / e['reference']).exists()
    links = []
    for p in STAGE.iterdir():
        if p.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
                assert (p.parent / target).exists(), (p, target)
                links.append(target)
    for p in STAGE.rglob('*'):
        if p.is_file() and p.suffix != '.f32':
            text = p.read_text()
            assert not re.search(r'/home/|/var/tmp|wiki/research|analysis/|0x10[0-9a-fA-F]{6}', text)
            assert all(not line.endswith((' ', '\t')) for line in text.splitlines())
    assert inputs['parent_status'] == 'pending-not-bound'
    assert inputs['parent_R6_pin'] is None
    assert not (STAGE / 'manifest.json').exists()
    assert 'UNSEALED' in (STAGE / 'README.md').read_text()
    for p, raw in before.items():
        assert p.read_bytes() == raw
    prepared = json.loads((PRIVATE / 'comparator-preparation/numeric-results.json').read_text())
    assert prepared['measured_old_plus_new_self'] == 4795 and prepared['pass_']
    return dict(status='UNSEALED draft structural check PASS; parent/source gate pending',
                groups=26, evaluations=72, unchanged_old_groups=25, unchanged_old_evaluations=71,
                preserved_old_F32=80, total_F32=81, candidate_compare_bytes=8830,
                new_reference_sha256=B_SHA, full38parameters_and_events_match=True,
                unsafe_mutations_rejected=rejected, local_links=len(links),
                source_payloads_preserved=len(before), unchanged=True,
                prior_comparator_evidence='Actual4795selfmeasurements carried from frozen preparation; not rerun for relabeling',
                final_parent_binding=False, independent_handoff_review_ready=False,
                original_calls=0, candidate_DSP_calls=0, comparator_calls=0, grade=None)


if __name__ == '__main__':
    if sys.argv[1:] != ['--check']:
        raise SystemExit('Read-only --check only. No release, native or comparator execution.')
    print(json.dumps(check(), indent=2))
