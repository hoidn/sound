"""Read-only recovery audit; never loads or executes the original device code.

Run from this directory: python3 -I recovery_audit.py > results/recovery-audit.json
The original manifest remains unchanged. Two original payloads were recovered
under recovery/originals/ after an unrelated concurrent edit; current-path
mismatches are reported separately, never accepted as original payloads.
"""
import hashlib
import json
import math
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 't12-device-dsp-v1' / 'harness'
LIB = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library')
ORIGINALS = {'run_collision.py': 'recovery/originals/run_collision.py',
             'results/collision.json': 'recovery/originals/collision.json'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = HERE / 'manifest.json'
    m = json.loads(manifest.read_text())
    mismatches = []
    for name, row in m['files'].items():
        current = HERE / name
        if sha(current) != row['sha256']:
            mismatches.append(dict(path=name, current_sha256=sha(current), original_sha256=row['sha256']))
        path = HERE / ORIGINALS.get(name, name)
        assert path.stat().st_size == row['bytes'], name
        assert sha(path) == row['sha256'], name
    checked = []
    for name, row in m['external_inputs'].items():
        if name == 'previews':
            continue
        path = Path(row.get('path', name))
        assert sha(path) == row.get('file_sha256', row.get('sha256')), name
        checked.append(str(path))
        data = path.read_bytes()
        for arch in ('x86_64', 'arm64'):
            if arch in row:
                part = row[arch]
                section = data[part['offset']:part['offset'] + part['size']]
                assert len(section) == part['size'], arch
                assert hashlib.sha256(section).hexdigest() == part['sha256'], arch
    for name, row in m['external_inputs']['previews'].items():
        for directory, suffix, key in (
            ('Devices/Instruments/Collision', '.adv', 'adv_sha256'),
            ('Ableton Folder Info/Previews/Devices/Instruments/Collision', '.adv.ogg', 'ogg_sha256'),
        ):
            path = LIB / directory / (name + suffix)
            assert sha(path) == row[key], str(path)
            checked.append(str(path))
    assert sha(Path(m['tools']['loader_binary'])) == m['tools']['loader_sha256']
    for path in (HERE / 'harness').iterdir():
        assert sha(path) == sha(BASE / path.name), path.name
    references = []
    for result in ('collision', 'noise'):
        name = 'results/' + result + '.json'
        rows = json.loads((HERE / ORIGINALS.get(name, name)).read_text())['reference_renders']
        for tag, row in rows.items():
            path = HERE / 'raw' / (tag + '.wav')
            assert sha(path) == row['sha256'], tag
            data = path.read_bytes()
            assert data[:4] == b'RIFF' and data[8:12] == b'WAVE', tag
            pos, chunks = 12, {}
            while pos < len(data):
                kind, size = struct.unpack_from('<4sI', data, pos)
                chunks[kind] = data[pos + 8:pos + 8 + size]
                pos += 8 + size + (size % 2)
            fmt, channels, rate, _, align, bits = struct.unpack_from('<HHIIHH', chunks[b'fmt '])
            assert (fmt, channels, rate, align, bits) == (3, 2, row['fs'], 8, 32), tag
            assert len(chunks[b'data']) == row['frames'] * 8, tag
            assert all(math.isfinite(v[0]) for v in struct.iter_unpack('<f', chunks[b'data'])), tag
            lines = (HERE / 'raw' / (tag + '.script')).read_text().splitlines()
            params = [int(line.split()[1]) for line in lines if line.startswith('param ')]
            assert params == list(range(139)), tag
            process = [tuple(map(int, line.split()[1:])) for line in lines if line.startswith('process ')]
            assert [n for n, _ in process] == [row['warm_up_frames'], row['frames']], tag
            calls = sum((n + block - 1) // block for n, block in process)
            references.append(dict(case=tag, frames=row['frames'], fs=row['fs'], calc_calls=calls))
    print(json.dumps(dict(
        id='t12-collision-recovery-audit', date='2026-10-19',
        command='python3 -I recovery_audit.py > results/recovery-audit.json',
        original_manifest_sha256=sha(manifest), manifest_payloads_checked=len(m['files']),
        recovered_original_paths=ORIGINALS, current_payload_mismatches=mismatches,
        external_files_checked=checked, slices_checked=['x86_64', 'arm64'],
        harness_identical=True, loader_hash_matches=True, retained_references=references,
        retained_reference_max_calc_calls=max(r['calc_calls'] for r in references),
        original_code_executed=False,
        limits=[
            'Two current payload paths differ from the original manifest; exact recovered originals are verified instead.',
            'The concurrent extras section has unknown execution provenance and is excluded from the draft.',
            'The historical full run.sh includes 131072-frame low-pitch probes plus warm-up: 278 CalcA calls.',
            'Do not run the historical regeneration command under the current 256-call-per-process limit.',
            'Scratch sweeps, seed members 1-7 and perturbed renders are not retained in the packet.',
            'Hash and shape checks establish integrity, not Live protocol or compatibility.',
        ]), indent=1))


if __name__ == '__main__':
    main()
