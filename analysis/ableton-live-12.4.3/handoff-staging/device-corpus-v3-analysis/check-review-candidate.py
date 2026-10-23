"""Read-only draft integrity; optional Root-authorized pure measurement tests only."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import math
import re
import struct
import sys
import tempfile

PRIVATE = Path(__file__).resolve().parent
STAGE = PRIVATE.with_name('device-corpus-v3')
ROOT = Path('/home/ollie/Documents/sound')
OLD = ROOT / 'handoff/device-corpus-v2'
METHOD = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-modal-method'


def ident(path):
    data = Path(path).read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def case_texts(text):
    pos = text.index('"cases": [') + len('"cases": [')
    decoder, rows = json.JSONDecoder(), []
    while True:
        while text[pos].isspace() or text[pos] == ',':
            pos += 1
        if text[pos] == ']':
            return rows
        start = pos
        unused, pos = decoder.raw_decode(text, pos)
        rows.append(text[start:pos])


def validate_new(rows, expected):
    assert len(rows) == 2
    for row, want in zip(rows, expected):
        assert row == want, 'new vector/event/metric/reference changed'
        assert len(row['parameters']) == len(row['parameter_order']) == 38
        assert row['before_parameters'] == row['after_parameters'] == []


def main():
    if sys.argv[1:] not in [['--check-draft'], ['--check-numeric']]:
        raise SystemExit('Read-only --check-draft or Root-authorized --check-numeric only.')
    numeric = sys.argv[1] == '--check-numeric'
    provenance = json.loads((PRIVATE / 'author-provenance-review-candidate.json').read_text())
    manifest = json.loads((STAGE / 'manifest.json').read_text())
    oldtext, text = (OLD / 'cases.json').read_text(), (STAGE / 'cases.json').read_text()
    old, current = json.loads(oldtext), json.loads(text)
    fixed = json.loads((PRIVATE / 'expected-new-evaluations.json').read_text())
    watched = set(STAGE.rglob('*')) | {Path(p) for p in provenance['old_release85_watch']}
    watched |= {Path(r['path']) for r in provenance['source_inputs']}
    watched |= {PRIVATE / 'check-review-candidate.py', PRIVATE / 'author-provenance-review-candidate.json',
                PRIVATE / 'expected-new-evaluations.json', PRIVATE / 'parent-r5-author-draft-asof.md'}
    watched = sorted(p for p in watched if p.is_file())
    before = {str(p): ident(p) for p in watched}
    for path, expected in provenance['old_release85_watch'].items():
        assert ident(path) == expected
    for record in provenance['source_inputs']:
        assert ident(record['path']) == {k: record[k] for k in ('bytes', 'sha256')}
    assert ident(METHOD / 'manifest.json') == {k: provenance['frozen_method_manifest'][k]
                                                for k in ('bytes', 'sha256')}
    snap = provenance['proposed_parent_asof']
    assert ident(PRIVATE / snap['snapshot']) == {k: snap[k] for k in ('bytes', 'sha256')}
    # Historical parent input is the private snapshot; never read its changing source path.
    assert len(list(p for p in STAGE.rglob('*') if p.is_file())) == 87
    assert not any(p.is_symlink() for p in STAGE.rglob('*'))
    assert manifest['release_status'].startswith('draft') and manifest['review']['status'] == 'pending'
    assert manifest['specification']['parent_sha256'] == snap['sha256']
    assert manifest['specification']['parent_revision_status'] == 'independently-reviewed-adopted'
    gate = provenance['source_gate']
    receipt = json.loads(Path(gate['adoption_receipt']['path']).read_text())
    assert receipt['canonical']['sha256'] == snap['sha256']
    assert receipt['canonical']['bytes'] == snap['bytes']
    assert receipt['independent_review'] == gate['independent_owner_review']
    assert gate['checked_against_snapshot'] and not gate['future_live_canonical_gate']
    assert not gate['handoff_approved'] and manifest['readiness']['handoff_review'] == 'pending'
    assert len(manifest['files']) == 86
    assert {r['path'] for r in manifest['files']} == {
        str(p.relative_to(STAGE)) for p in STAGE.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    for r in manifest['files']:
        assert ident(STAGE / r['path']) == {k: r[k] for k in ('bytes', 'sha256')}
    assert current['status'].startswith('draft') and current['release_id'] == 'device-corpus-v3'
    assert len(current['cases']) == 25 and current['cases'][:24] == old['cases']
    assert case_texts(text)[:24] == case_texts(oldtext), 'old case objects changed as literal JSON text'
    assert sum(len(c['evaluations']) for c in current['cases']) == 71
    assert current['cases'][-1]['id'] == 'CORPUS-AUDIO-025'
    additions = current['cases'][-1]['evaluations']
    validate_new(additions, fixed)
    old013 = next(e for c in old['cases'] for e in c['evaluations'] if e['id'] == 'CORPUS-AUDIO-013-04')
    decision = json.loads((METHOD / 'selection-decision.json').read_text())
    assert additions[0]['metric'] == old013['metric']
    assert additions[1]['metric'] == decision['selected_note72_metric']
    assert [len(c) for c in additions[0]['metric']['modes']] == [16, 16]
    assert [len(c) for c in additions[1]['metric']['modes']] == [15, 15]
    assert additions[0]['parameters'] == additions[1]['parameters']
    cap = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-pitch/raw'
    for note, row in zip((60, 72), additions):
        lines = (cap / f'note{note}.script').read_text().splitlines()
        pairs = [(int(s.split()[1]), struct.pack('<f', float(s.split()[2])))
                 for s in lines if s.startswith('param ')]
        assert [i for i, value in pairs] == list(range(38))
        assert [value for i, value in pairs] == [struct.pack('<f', row['parameters'][k]) for k in row['parameter_order']]
        assert row['events'] == [{'frame': 1537, 'kind': 'note_on', 'channel': 0, 'key': note, 'velocity': 100}]
        assert f'event 1537 0x90 {note} 100' in lines
        assert (STAGE / row['reference']).read_bytes() == (cap / f'note{note}.f32').read_bytes()
        frames = list(struct.iter_unpack('<ff', (STAGE / row['reference']).read_bytes()))
        assert len(frames) == 16384 and all(math.isfinite(v) for f in frames for v in f)
        assert all(math.fsum(f[c] * f[c] for f in frames[4096:]) > 0 for c in (0, 1))
    fixtures = [p for p in OLD.rglob('*.f32')]
    assert len(fixtures) == 78
    for p in fixtures:
        assert p.read_bytes() == (STAGE / p.relative_to(OLD)).read_bytes()
    assert (STAGE / 'compare.py').read_bytes() == (OLD / 'compare.py').read_bytes()
    assert ident(STAGE / 'compare.py') == {'bytes': 7795, 'sha256': 'f4d660c0c8a798d99f8e560f9505705dea9517174fdc0d5fb8151dc126ad0c83'}
    assert len(list((STAGE / 'reference').glob('*.f32'))) == 71
    assert len({ident(p)['sha256'] for p in (STAGE / 'reference').glob('*.f32')}) == 64
    negatives = []
    for name, mutate in [
        ('wrong event key', lambda x: x[1]['events'][0].update(key=60)),
        ('extra minus-one event shift', lambda x: x[0]['events'][0].update(frame=1536)),
        ('missing ordered parameter', lambda x: x[0]['parameter_order'].pop()),
        ('enabled LFO', lambda x: x[0]['parameters'].update(LfoOnOff=1)),
        ('altered note60 center', lambda x: x[0]['metric']['modes'][0][0].update(center_hz=524)),
        ('restored omitted mode16', lambda x: x[1]['metric']['modes'][0].append({'center_hz': 8371, 'cutoff_hz': 100})),
        ('wrong reference identity', lambda x: x[0].update(reference='reference/CORPUS-AUDIO-013-04.f32')),
    ]:
        changed = copy.deepcopy(additions)
        mutate(changed)
        try:
            validate_new(changed, fixed)
        except AssertionError:
            negatives.append(name)
        else:
            raise AssertionError('unsafe metadata accepted: ' + name)
    links = []
    forbidden = ['/home/', '/tmp/', '/var/tmp/', '../../', 'analysis/', 'wiki/research/',
                 'FUN_0', 'DAT_0', '_CalcA', '_SetParameterA', 'param_1', 'Corpus.bundle']
    for p in STAGE.rglob('*'):
        if p.is_file() and p.suffix in ('.md', '.json', '.py'):
            s = p.read_text()
            assert s.endswith('\n') and all(not line.endswith((' ', '\t')) for line in s.splitlines()), p
            assert not any(token in s for token in forbidden), p
            if p.suffix == '.md':
                for target in re.findall(r'\]\(([^)]+)\)', s):
                    target = target.split('#')[0]
                    if target:
                        destination = (p.parent / target).resolve()
                        assert destination.is_relative_to(STAGE.resolve()) and destination.is_file(), (p, target)
                        links.append([str(p.relative_to(STAGE)), target])
    results = {'mode': 'structural-only' if not numeric else 'structural-and-authorized-new-pure-measurements',
               'old_release_files_unchanged': 85, 'old_case_groups_literal_preserved': 24,
               'old_evaluations_preserved': 69, 'old_fixture_bytes_preserved': 78,
               'groups': 25, 'evaluations': 71, 'stage_files': 87, 'draft_payloads': 86,
               'compare_byte_identical': True, 'links': links,
               'metadata_negative_fixtures': negatives,
               'numeric_scope': 'Not run in this structural check; prior190new measurements retained' if not numeric else 'Two new self comparisons and one wrong-note contrast only; no candidate/original/CLI/run execution.'}
    if numeric:
        assert provenance['method_approval']['sha256'] == ident(provenance['method_approval']['path'])['sha256']
        prior = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = True
            spec = importlib.util.spec_from_file_location('reviewed_v3_measurement_only', STAGE / 'compare.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # No __main__, run(), device synthesis or old private code.
        finally:
            sys.dont_write_bytecode = prior
        references = [module.audio(STAGE / e['reference']) for e in additions]
        selfs = [module.compare(a, a, e['metric'], e['sample_rate_hz']) for a, e in zip(references, additions)]
        assert all(r['pass'] for r in selfs)
        assert [len(r['measurements']) for r in selfs] == [98, 92]
        wrong = module.compare(references[0], references[1], additions[1]['metric'], 44100)
        assert not wrong['pass'] and len(wrong['measurements']) == 92
        assert sum(not r['pass'] for r in wrong['measurements']) == 64
        malformed = []
        with tempfile.TemporaryDirectory(prefix='measurement-fixtures-', dir=PRIVATE) as directory:
            fixture = Path(directory) / 'invalid.f32'
            nominal = (STAGE / additions[0]['reference']).read_bytes()
            for name, data in [('short', nominal[:-8]), ('extra', nominal + b'\0' * 8),
                               ('NaN prefix', struct.pack('<f', math.nan) + nominal[4:]),
                               ('Inf last sample', nominal[:-4] + struct.pack('<f', math.inf))]:
                fixture.write_bytes(data)
                try:
                    module.audio(fixture)
                except ValueError:
                    malformed.append(name)
                else:
                    raise AssertionError('bad format accepted: ' + name)
        for channel in (0, 1):
            silent = references[1].copy()
            silent[:, channel] = 0
            try:
                r = module.compare(silent, references[1], additions[1]['metric'], 44100)
            except ValueError:
                malformed.append(f'silent channel{channel}')
            else:
                assert not r['pass']
                malformed.append(f'silent channel{channel}')
        results.update(new_selfs=selfs, new_self_measurements=190, wrong_note60_vs_note72=wrong,
                       wrong_measurements=92, wrong_failed=64, invalid_audio_fixtures=malformed,
                       environment={'numpy': module.np.__version__, 'scipy': __import__('scipy').__version__},
                       old_4603_measurements='Carried prior v2 approval, not rerun or counted as new current results.')
    after = {str(p): ident(p) for p in watched}
    assert before == after
    results.update(watched_paths=len(watched), watched_unchanged=True, original_calls=0,
                   candidate_calls=0, private_model_calls=0, grade=None, released=False)
    print(json.dumps(results, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
