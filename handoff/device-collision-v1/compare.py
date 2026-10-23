"""Measure finite Collision outputs. No synthesis; Python standard library only."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent


def audio(path, frames):
    data = Path(path).read_bytes()
    if frames <= 0 or len(data) != frames * 8:
        raise ValueError('expected exactly the declared nonempty stereo binary32 frames')
    values = tuple(x[0] for x in struct.iter_unpack('<f', data))
    if not all(math.isfinite(x) for x in values):
        raise ValueError('nonfinite audio sample')
    return data, values


def measure(candidate, reference, metric):
    if len(candidate) != len(reference) or not candidate:
        raise ValueError('empty or mismatched audio')
    if not all(math.isfinite(x) for x in candidate + reference):
        raise ValueError('nonfinite audio sample')
    if metric['kind'] == 'peak':
        error = max(abs(x) for x in candidate)
    elif metric['kind'] == 'stereo_relative_rms':
        energy = math.fsum(x*x for x in reference)
        if energy <= 0 or not math.isfinite(energy):
            raise ValueError('reference has no finite positive energy')
        error = math.sqrt(math.fsum((x-r)**2 for x, r in zip(candidate, reference))/energy)
    else:
        raise ValueError('unknown comparison metric')
    if not math.isfinite(error):
        raise ValueError('nonfinite comparison result')
    return {'pass': error <= metric['maximum'], 'error': error, 'maximum': metric['maximum']}


def run(directory):
    cases = json.loads((HERE/'cases.json').read_text())['cases']
    if not cases:
        raise ValueError('no cases')
    results = []
    for case in cases:
        try:
            candidate_data, candidate = audio(Path(directory)/(case['id']+'.f32'), case['frames'])
            reference_data, reference = audio(HERE/case['reference'], case['frames'])
            if hashlib.sha256(reference_data).hexdigest() != case['reference_sha256']:
                raise ValueError('reference checksum mismatch')
            result = measure(candidate, reference, case['metric'])
        except (OSError, ValueError, OverflowError) as error:
            result = {'pass': False, 'error': str(error)}
        results.append({'id': case['id'], **result})
    return {'pass': bool(results) and all(x['pass'] for x in results), 'results': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate_directory', type=Path)
    report = run(parser.parse_args().candidate_directory)
    print(json.dumps(report, indent=1, allow_nan=False))
    raise SystemExit(0 if report['pass'] else 1)
