"""Reviewer extracted-execution check (analyst side): does rounding accumulate over a sequence of relative messages?

  python3 -I -B x_relative.py > x_relative.out

Runs the X2 evidence script's chain() (imported unchanged) on long LinearSignedBit and LinearBinaryOffset sequences
for ranges whose step (max - min) x d/256 is not exact in binary32, one gdb process per sequence, at most 202 calls
per process (limit 256). Compares the X values with the exact rule of spec.md (current + (max - min) x d/256,
clamped, from the binary32 range the parameter reports) in units of tau.
"""
import struct
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[4] / 'analysis/ableton-live-12.4.3/r2/x2-midi-v1'))
import run_x2 as x  # noqa: E402


def f32(v):
    return struct.unpack('<f', struct.pack('<f', v))[0]


RUNS = [('LinearSignedBit', 0.0, 5.3, 0.0, 0x01, 200), ('LinearSignedBit', -3.3, 4.9, -3.3, 0x01, 200),
        ('LinearBinaryOffset', 0.0, 100.3, 0.0, 0x41, 200), ('LinearSignedBit', 0.0, 1.0, 0.0, 0x01, 200)]
for mode, mn, mx, start, byte, count in RUNS:
    p = {'kind': 'continuous', 'min': mn, 'max': mx, 'quantized': False, 'value': start}
    r = x.chain([(20, byte)] * count, p, 'none', mode_name=mode)
    lo, hi = F(f32(mn)), F(f32(mx))
    d = (byte if byte <= 64 else -(byte - 64)) if mode == 'LinearSignedBit' else byte - 64
    tau = max(F(1, 10 ** 6), F(1, 2 ** 22) * max(abs(lo), abs(hi)))
    cur, worst, first_over = F(f32(start)), (F(0), None), None
    for k, v in enumerate(r['values'], 1):
        cur = min(max(cur + (hi - lo) * d / 256, lo), hi)
        e = abs(F(v) - cur) / tau
        if e > worst[0]:
            worst = (e, k)
        if first_over is None and e > 1:
            first_over = k
    print(f'{mode} range {mn}..{mx} from {start}, {count} messages of d = {d} ({2 + count} calls): largest '
          f'|X - exact| {float(worst[0]):.2f} tau at message {worst[1]}; first above tau at message {first_over}; '
          f'per message up to {float(worst[0]) / worst[1] if worst[1] else 0:.3f} tau on average')
