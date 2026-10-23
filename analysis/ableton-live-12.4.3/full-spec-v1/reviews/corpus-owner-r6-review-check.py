"""Independent R6 integration checks; only new owner checker may run, no audio comparator."""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import sys

ROOT = Path('/home/ollie/Documents/sound')
BASE = ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1'
P = BASE / 'corpus-owner-r6'


def identity(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def resolve(value, pointer):
    for segment in pointer.lstrip('/').split('/'):
        segment = segment.replace('~1', '/').replace('~0', '~')
        value = value[int(segment)] if isinstance(value, list) else value[segment]
    return value


def main():
    assert sys.argv[1:] == ['--check']
    inputs = json.loads((P/'inputs.json').read_text())
    history = json.loads((P/'historical-consumers.json').read_text())
    seal = json.loads((P/'manifest.json').read_text())
    assert identity(P/'manifest.json') == dict(bytes=1935, sha256='fa001c5d4bffb5568b3a4765ca67a1e193ac5dac7a621ed9ea3a6daf785fb72a')
    assert {q.name for q in P.iterdir()} == {'manifest.json'} | {r['path'] for r in seal['files']}
    pins = inputs['immutable_pins'] + inputs['historical_consumer_pins']
    paths = {Path(r['path']) for r in pins} | set(P.iterdir())
    paths.add(Path(__file__))
    paths.add(ROOT/'wiki/specs/device-corpus.md')
    paths.add(ROOT/'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/inputs/impulse44.f32')
    # Expand only retained file inventories as DATA, never run their checkers.
    for manifest_path in (P.parent/'corpus-owner-r5/manifest.json', ROOT/'handoff/device-corpus-v3/manifest.json'):
        manifest = json.loads(manifest_path.read_text())
        for row in manifest['files']:
            target = manifest_path.parent/row['path']
            assert identity(target) == {k:row[k] for k in ('bytes','sha256')}
            paths.add(target)
    before_watch = {str(q):identity(q) for q in sorted(paths)}
    for row in pins:
        assert identity(Path(row['path'])) == {k:row[k] for k in ('bytes','sha256')}
    for row in seal['files']:
        assert identity(P/row['path']) == {k:row[k] for k in ('bytes','sha256')}
    before = (P/'spec-before-r5.md').read_text()
    after = (P/'spec-r6.md').read_text()
    assert (ROOT/'wiki/specs/device-corpus.md').read_bytes() == before.encode()
    assert (P.parent/'corpus-owner-r5/spec-r5.md').read_bytes() == before.encode()
    delta = json.loads((P/'delta.json').read_text())
    rendered = before
    for op in delta['replacements']:
        if op['operation'] == 'append':
            rendered += op['after']
        else:
            assert op['operation'] == 'replace' and rendered.count(op['before']) == 1
            rendered = rendered.replace(op['before'],op['after'])
    assert len(delta['replacements']) == 18 and rendered == after
    assert identity(P/'spec-r6.md') == dict(bytes=58472,sha256='07a89f25de6b3c987d448e0e049bdd7dfaec52f479532b3aca3faddedcd511cd')
    req = re.compile(r'^### (REQ-DEVICE-CORPUS-\d{3}) ',re.M)
    assert req.findall(before) == req.findall(after) == ['REQ-DEVICE-CORPUS-%03d'%i for i in range(1,14)]
    def bodies(text):
        matches = list(req.finditer(text))
        return [text[a.start():b.start()] for a,b in zip(matches,matches[1:])]
    assert len(bodies(before)) == 12 and bodies(before) == bodies(after)
    rows = lambda text: re.findall(r'^\| DCO-\d{3} \|.*$',text,re.M)
    old, new = rows(before), rows(after)
    assert len(old) == 31 and len(new) == 32 and new[:31] == old
    assert [r.split('|')[1].strip() for r in new] == ['DCO-%03d'%i for i in range(1,33)]
    assert len([r for r in new if r.split('|')[3].strip() == 'U']) == 4
    case, = json.loads((P/'cases-additions.json').read_text())
    ev = case['evaluation']
    assert case['id'] == 'DCO-032' and case['requirements'] == ['REQ-DEVICE-CORPUS-001','REQ-DEVICE-CORPUS-013']
    assert case['candidate_or_application_grade'] is None
    script = (P.parent/'depth-corpus-midi-noteoff-decay-zero/gate1-off.script').read_text()
    params = [line.split() for line in script.splitlines() if line.startswith('param ')]
    assert [int(r[1]) for r in params] == list(range(38))
    assert [struct.pack('<f',ev['parameters'][k]) for k in ev['parameter_order']] == [struct.pack('<f',float(r[2])) for r in params]
    assert struct.pack('<f',ev['parameters']['DecayOnNoteOff']) == bytes(4)
    expected_events = [dict(frame=int(a),kind=('note_on' if int(b,0)==144 else 'note_off'),channel=0,key=int(c),velocity=int(d))
                       for a,b,c,d in re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$',script,re.M)]
    assert ev['events'] == expected_events == [dict(frame=1537,kind='note_on',channel=0,key=60,velocity=100),dict(frame=3073,kind='note_off',channel=0,key=60,velocity=64)]
    assert [line for line in script.splitlines() if not line.startswith(('param ','event '))] == [
        'mxcsr 0x1f80','transport 0 0 120','create','rate 44100','inflag 1',
        'input /home/ollie/Documents/sound/analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/inputs/impulse44.f32','process 16384 512','destroy']
    input_path = Path(next(line[6:] for line in script.splitlines() if line.startswith('input ')))
    assert input_path.read_bytes() == (ROOT/'handoff/device-corpus-v3/signals/input-01.f32').read_bytes()
    assert (ev['sample_rate_hz'],ev['frames'],ev['block_frames']) == (44100,16384,512)
    criterion = json.loads((P.parent/'depth-corpus-midi-noteoff-decay-zero-criterion-proposal/criterion.json').read_text())
    assert ev['metric']['kind'] == case['metric_rules']['kind'] == criterion['metric_kind_proposed']
    assert case['metric_rules']['max_relative_RMS'] == criterion['threshold'] == 0.01
    assert ev['reference']['sha256'] == criterion['reference_sha256']
    assert identity(P/ev['reference']['path']) == {k:ev['reference'][k] for k in ('bytes','sha256')}
    binding = inputs['criterion_review_binding']
    method = json.loads(Path(binding['pin']['path']).read_text())
    assert method['required_findings'] == [] and method['disposition'] == binding['disposition']
    capture = json.loads((BASE/'reviews/corpus-midi-noteoff-decay-zero-capture-review.json').read_text())
    assert capture['required_findings'] == [] and capture['disposition'].startswith('APPROVED bounded actual endpoint')
    assert json.loads((P/'method-review-binding.json').read_text())['current'] == binding
    immutable = {r['path'] for r in inputs['historical_consumer_pins']}
    pointer_count = 0
    for record in history['records']:
        source = record['consumer_identity_asof']
        if source['path'] not in immutable:
            assert record['classification'].startswith('active parallel mutable')
            continue
        content = json.loads(Path(source['path']).read_text())
        for ref in record['references']:
            value = resolve(content,ref['json_pointer'])
            assert value == ref['value'] and value.count(history['R5_sha256']) == ref['literal_occurrences']
            pointer_count += 1
    assert len(immutable) == 38 and len(history['records']) == 39
    # Fully inspected NEW owner checker only: no old checker/comparator/model replay.
    runs = []
    for mode in ('--check','--write','--seal','--capture'):
        done = subprocess.run([sys.executable,'-B',str(P/'check.py'),mode],capture_output=True,timeout=30,check=False)
        assert done.returncode == (0 if mode == '--check' else 1)
        if mode == '--check':
            receipt = json.loads(done.stdout)
            assert len(receipt['negative_fixtures']) == 14 and receipt['old_case_rows_exact'] == 31 and receipt['sealed'] is True
            assert not done.stderr
        else:
            assert not done.stdout and b'Read-only' in done.stderr
        runs.append(dict(mode=mode,exit=done.returncode,stdout_bytes=len(done.stdout),stdout_sha256=hashlib.sha256(done.stdout).hexdigest(),stderr=done.stderr.decode()))
    after_watch = {str(q):identity(q) for q in sorted(paths)}
    assert before_watch == after_watch
    print(json.dumps(dict(status='PASS independent owner integration only',requirements=13,cases=32,old_rows_exact=31,
                          clauses_001_012_exact=True,finite=28,U=4,delta_operations=18,parameter_bits=38,
                          event_count=2,signal_identity=True,immutable_pins=len(inputs['immutable_pins']),
                          historical_pins=38,historical_pointers=pointer_count,active_consumer_asof_only=1,
                          runs=runs,author_receipt=receipt,watched_paths=len(paths),watch_unchanged=True,
                          watch_sha256=hashlib.sha256(json.dumps(before_watch,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                          new_original_calls=0,comparator_calls=0,grade=None),indent=2))


if __name__ == '__main__':
    main()
