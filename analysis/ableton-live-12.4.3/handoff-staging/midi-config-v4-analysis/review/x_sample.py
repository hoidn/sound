"""Reviewer re-run of the midi-config-v4 extracted-execution cases (analyst side; never shipped).

  python3 -I -B x_sample.py > x_sample.out

Feeds each new case's payload stimulus (messages, parameter, takeover choice, map mode) to the X2 evidence
script's own chain() (r2/x2-midi-v1/run_x2.py, imported unchanged; one gdb process per case) and compares the
result with the payload's expected values. Checks the per-process call count against the loader's limit of 256.
"""
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
X2 = ROOT / 'analysis/ableton-live-12.4.3/r2/x2-midi-v1'
STAGE = HERE.parents[1] / 'midi-config-v4'
sys.dont_write_bytecode = True
sys.path.insert(0, str(X2))
import run_x2 as x  # noqa: E402

KIND = {'continuous': 'continuous', 'enumerated': 'enum', 'other': 'other'}
TAKE = {'none': 'none', 'pick-up': 'pickup', 'value-scaling': 'scaling'}


def f32(v):
    return struct.unpack('<f', struct.pack('<f', v))[0]


def main():
    cases = [c for c in json.loads((STAGE / 'cases.json').read_text())['cases'] if int(c['id'][-3:]) >= 128]
    ok, worst_calls = 0, 0
    for c in cases:
        s, p = c['stimulus'], c['stimulus']['parameter']
        a = c['expected']['assignments'][0]
        param = {'kind': KIND[p['kind']], 'min': float(p['min']), 'max': float(p['max']),
                 'quantized': p['stepped'], 'value': p['initial_value']}
        assert f32(p['initial_value']) == p['initial_value'], c['id']        # initial value is a binary32 number
        msgs = [(int(m.split()[1], 16), int(m.split()[2], 16)) for m in s['messages']]
        before = len(x.LOG)
        r = x.chain(msgs, param, TAKE[s['takeover']], avoid=False, mode_name=a['map_mode'])
        calls = 2 + len(msgs)                     # initializer, preference handler, one receiver call per message
        worst_calls = max(worst_calls, calls)
        assert len(x.LOG) == before + 1
        exp = c['expected']['values']
        agree = len(r['values']) == len(exp) and all(abs(u - v) <= 5e-10 for u, v in zip(r['values'], exp))
        ok += agree
        print(c['id'], s['takeover'], a['map_mode'], p['min'], p['max'], p['initial_value'], s['messages'])
        print('   X now  ', [round(v, 9) for v in r['values']], 'agree' if agree else 'DIFFERS', 'calls', calls,
              'stored choice', r['takeover_index_stored'], 'deferred path', r['posting_path'])
    print(f'{ok}/{len(cases)} cases reproduce the payload values within 5e-10; processes {len(cases)}; '
          f'largest call count per process {worst_calls} (limit 256)')


if __name__ == '__main__':
    main()
