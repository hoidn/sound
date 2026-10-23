"""Random parts of Collision: the mallet noise, the noise exciter and the default preset, as seed ensembles.

    python3 -I run_noise.py          # writes raw/*.wav (one member per case), results/noise.json

Collision draws one uniform random number per frame per active voice from rand(), which it seeds once
from the clock while building its engine. Each case is rendered with SEEDS clock values (XDEV_TIME);
member 0 (clock 0) is kept as the reference render. Measures:
- the spectrum: third-octave bands 63 Hz to 16 kHz averaged over the live part of the render, and the
  envelope: 10 ms RMS levels; ensemble power means and their split-half stability (see ensemble()),
  which calibrate the spec's noise metric;
- the noise filter: power spectra (Welch, 4096) of a held Pipe note excited by noise only, divided by
  the spectrum with the Lowpass at Freq 1 (open), sampled at the Pipe's harmonics;
- the envelope: ensemble-mean RMS in 10 ms windows.
Dependencies: numpy, scipy, run_collision.py helpers.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
from scipy.signal import welch  # noqa: E402

import run_collision as rc  # noqa: E402
from col import FS, P, PRESET, note  # noqa: E402

SEEDS = [0, 1760000000, 1760000123, 1234567, 42, 99999, 31337, 2718281]
BANDS = [63 * 2 ** (k / 3) for k in range(25)]          # 63 Hz .. 16 kHz


def band_levels(y, fs=FS, win=1024):
    n = len(y) // win
    f = np.fft.rfftfreq(win, 1 / fs)
    out = np.zeros((2, n, len(BANDS)))
    for ch in range(2):
        seg = y[:n * win, ch].reshape(n, win) * np.hanning(win)
        p = np.abs(np.fft.rfft(seg, axis=1)) ** 2
        for b, fc in enumerate(BANDS):
            m = (f >= fc * 2 ** (-1 / 6)) & (f < fc * 2 ** (1 / 6))
            out[ch, :, b] = 10 * np.log10(p[:, m].sum(1) + 1e-30)
    return out


def ensemble(tag, params, events, frames, keep=True):
    """Render the seed ensemble. Statistics per member against the ensemble (power) mean:
    The ensemble mean is the power mean. Its stability is measured split-half (members 0-3 against
    4-7): spectrum = third-octave levels averaged over the frames whose mean 10 ms level is within 40 dB
    of its peak, max |A - B| over bands within 30 dB of the loudest; envelope = 10 ms RMS levels, median
    and 90th percentile of |A - B| over the windows within 30 dB of the peak."""
    ys = [rc.run(f'{tag}_s{s}', params, events, frames, env={'XDEV_TIME': str(s)}, keep=(keep and i == 0)) for i, s in enumerate(SEEDS)]
    n = frames // 441
    rms = np.array([np.sqrt((y[:n * 441] ** 2).reshape(n, 441, 2).mean(1)) for y in ys])      # member, window, channel
    env = 10 * np.log10((rms ** 2).mean(0) + 1e-60)
    live = env[:, 0] > env[:, 0].max() - 40
    frames_live = np.repeat(live, 441)
    L = np.array([band_levels(y[:n * 441][frames_live[:n * 441]][: (int(frames_live.sum()) // 1024) * 1024]).mean(1) for y in ys])
    pmean = lambda x: 10 * np.log10((10 ** (np.asarray(x) / 10)).mean(0))  # noqa: E731
    mean = pmean(L)
    bands = mean > mean.max() - 30
    A, B = pmean(L[:4]), pmean(L[4:])
    eA = 10 * np.log10((rms[:4] ** 2).mean(0) + 1e-60)
    eB = 10 * np.log10((rms[4:] ** 2).mean(0) + 1e-60)
    win = env > env.max(0) - 30
    d = np.abs(eA - eB)[win]
    return ys, dict(case=tag, live_windows=int(live.sum()),
                    split_half_spectrum_max_db=float(np.abs(A - B)[bands].max()),
                    split_half_envelope_median_db=float(np.median(d)), split_half_envelope_p90_db=float(np.percentile(d, 90)),
                    peak=[float(np.abs(y).max()) for y in ys],
                    spectrum_mean_db=[[round(float(v), 2) for v in mean[ch]] for ch in range(2)],
                    envelope_db_10ms=[[round(float(v), 2) for v in env[:, ch]] for ch in range(2)])


def filt_response(ys, ref):
    f, s = welch(np.concatenate(ys)[:, 0], FS, nperseg=4096)
    _, r = welch(np.concatenate(ref)[:, 0], FS, nperseg=4096)
    return f, s / r


def main():
    rc.xdevpy.build()
    rc.RAW.mkdir(exist_ok=True)
    rc.SCR.mkdir(parents=True, exist_ok=True)
    out = dict(seeds=SEEDS, bands_hz=BANDS)
    hold = note(60, 100, on=0, dur=13230)                  # 0.3 s held
    cases = [('noise_preset', PRESET, note(60, 100, on=0, dur=None), 32768),
             ('noise_mallet_amount1', P(Mallet__NoiseAmount=1), note(60, 100, on=0, dur=None), 32768),
             ('noise_mallet_color0', P(Mallet__NoiseAmount=1, Mallet__NoiseColor=0), note(60, 100, on=0, dur=None), 32768),
             ('noise_exc_default', P(Mallet__OnOff=0, Noise__OnOff=1), hold, 32768),
             ('noise_exc_hp', P(Mallet__OnOff=0, Noise__OnOff=1, Noise__FilterType=1), hold, 32768),
             ('noise_exc_bp', P(Mallet__OnOff=0, Noise__OnOff=1, Noise__FilterType=2, Noise__Q=0.5), hold, 32768),
             ('noise_exc_lphp', P(Mallet__OnOff=0, Noise__OnOff=1, Noise__FilterType=3), hold, 32768),
             ('noise_exc_adsr', P(Mallet__OnOff=0, Noise__OnOff=1, Noise__Attack=0.5, Noise__Decay=0.5, Noise__Sustain=0.5,
                                  Noise__Release=0.5), hold, 44100),
             ('noise_exc_sustain1', P(Mallet__OnOff=0, Noise__OnOff=1, Noise__Sustain=1), hold, 32768)]
    res = {}
    for tag, params, ev, frames in cases:
        _, r = ensemble(tag, params, ev, frames)
        res[tag] = r
        print(tag, 'split spec %.2f env med %.2f p90 %.2f' % (r['split_half_spectrum_max_db'], r['split_half_envelope_median_db'],
                                                              r['split_half_envelope_p90_db']), flush=True)
    out['ensembles'] = res
    # envelope stages: attack, decay, release times from the ensemble mean (resonator decay 0 to keep it short)
    env = {}
    for tag, kw in (('A0', {}), ('A0.25', dict(Noise__Attack=0.25)), ('A0.5', dict(Noise__Attack=0.5)), ('A0.75', dict(Noise__Attack=0.75)),
                    ('D0.5', dict(Noise__Decay=0.5)), ('D0.75', dict(Noise__Decay=0.75)),
                    ('S0.5', dict(Noise__Sustain=0.5)), ('S0.5_R0.5', dict(Noise__Sustain=0.5, Noise__Release=0.5)),
                    ('S0.5_R0.75', dict(Noise__Sustain=0.5, Noise__Release=0.75))):
        _, r = ensemble(f'nenv_{tag}', P(Mallet__OnOff=0, Noise__OnOff=1, Resonator1__Decay=0, **kw), note(60, 100, on=4410, dur=22050),
                        4410 + 22050 + 66150, keep=False)
        e = np.array(r['envelope_db_10ms'][0])
        pk = int(np.argmax(e))
        on, off = 10, 60                                   # note-on at 100 ms, note-off at 600 ms (10 ms windows)
        stage = dict(peak_db=float(e[pk]), peak_ms=10 * (pk - on),
                     ms_to_minus20db_after_peak=next((10 * (k - pk) for k in range(pk, len(e)) if e[k] < e[pk] - 20), None),
                     level_before_off_db=float(e[off - 2] - e[pk]),
                     ms_after_off_to_minus40db=next((10 * (k - off) for k in range(off, len(e)) if e[k] < e[pk] - 40), None),
                     rise_10_to_90pct_ms=None)
        lin = 10 ** (e[on:pk + 1] / 20)
        if pk > on:
            a = np.argmax(lin >= 0.1 * lin.max())
            b = np.argmax(lin >= 0.9 * lin.max())
            stage['rise_10_to_90pct_ms'] = 10 * int(b - a)
        env[tag] = dict(**stage, envelope_db_10ms=r['envelope_db_10ms'][0][:130])
    out['envelope'] = env
    # filter shapes: Pipe at C2, long sustained noise, divided by the open low-pass
    shape = {}
    base = dict(Mallet__OnOff=0, Noise__OnOff=1, Noise__Sustain=1, Resonator1__Type=5, Resonator1__Decay=0.5)
    ev = note(36, 100, on=0, dur=None)
    ref, _ = ensemble('nf_ref', P(**base, Noise__Freq=1), ev, 88200, keep=False)
    harm = 65.4 * np.arange(1, 280)
    for tag, kw in (('lp_0.25', dict(Noise__Freq=0.25)), ('lp_0.5', dict(Noise__Freq=0.5)), ('lp_0.75', dict(Noise__Freq=0.75)),
                    ('lp_0.5_q1', dict(Noise__Freq=0.5, Noise__Q=1)),
                    ('hp_0.5', dict(Noise__FilterType=1, Noise__Freq=0.5)), ('bp_0.5', dict(Noise__FilterType=2, Noise__Freq=0.5)),
                    ('bp_0.5_q1', dict(Noise__FilterType=2, Noise__Freq=0.5, Noise__Q=1)), ('lphp_0.5', dict(Noise__FilterType=3, Noise__Freq=0.5))):
        ys, _ = ensemble(f'nf_{tag}', P(**base, **kw), ev, 88200, keep=False)
        f, g = filt_response(ys, ref)
        gi = np.interp(harm, f, 10 * np.log10(g + 1e-30))
        good = harm < 18000
        shape[tag] = dict(harmonic_hz=[round(float(h), 1) for h in harm[good][::4]], gain_db=[round(float(v), 2) for v in gi[good][::4]],
                          peak_hz=float(harm[good][np.argmax(gi[good])]), peak_db=float(gi[good].max()),
                          minus3db_hz=[float(harm[good][k]) for k in range(1, int(good.sum())) if (gi[k - 1] - gi[good].max() + 3) * (gi[k] - gi[good].max() + 3) <= 0])
    out['filter'] = shape
    # noise exciter volume and velocity: same seed, so gains are exact ratios
    b = rc.run('nv_base', P(Mallet__OnOff=0, Noise__OnOff=1), hold, 16384)[:, 0]
    rows = []
    for kw, vel in ((dict(Noise__Volume=0.25), 100), (dict(Noise__Volume=1), 100), (dict(Noise__VelToVolume=2.5), 127), (dict(Noise__VelToVolume=2.5), 1)):
        g, r = rc.fitg(rc.run('nv', P(Mallet__OnOff=0, Noise__OnOff=1, **kw), note(60, vel, on=0, dur=13230), 16384)[:, 0], b)
        rows.append(dict(**kw, velocity=vel, gain_db=rc.db(g), residual=r))
    out['noise_volume'] = rows
    out['reference_renders'] = rc.KEPT
    (rc.RES / 'noise.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
