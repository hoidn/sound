"""Which position range does Live pass to Collision? Compare the shipped preset previews (audio Live
rendered for each Collision preset, shipped in the app bundle) with X renders of the same presets under
two hypotheses for the six position parameters (Resonator1/2 HitX, ListeningXL, ListeningXR):

- identity: the stored value 0..1 is passed unchanged (the traced Live-side chain, N5/N6);
- bipolar: the stored value v is passed as 2v - 1 (what the bundle's -2..2 range would suggest).

    python3 -I previews.py           # writes results/previews.json (renders and decoded previews in /var/tmp)

Test 1 (listening positions). For each spectral peak of the preview (a single C4 note), the stereo level
difference R - L in dB depends only on the two pickup positions: excitation, velocity, mallet and hit
cancel because both channels read the same modes. The renders are evaluated at the same frequency bins.
Test 2 (hit position). The within-channel level pattern of the peaks also depends on the hit point, the
mallet and the velocity; the hit hypothesis is varied alone (listening kept as identity), with the best
of velocities 64, 100 and 127 per hypothesis.
Decoding: gst-launch-1.0 (oggdemux, vorbisdec) to binary32. Previews are lossy (Vorbis, about 112 kbit/s).
Dependencies: numpy, scipy, GStreamer with the Vorbis plug-ins, the app bundle.
"""
import concurrent.futures as cf
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
from scipy.signal import find_peaks  # noqa: E402

import xdevpy  # noqa: E402
from col import FS, idx, read_adv, render, script, stored_to_host  # noqa: E402

LIB = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Core Library')
PV = LIB / 'Ableton Folder Info/Previews/Devices/Instruments/Collision'
PR = LIB / 'Devices/Instruments/Collision'
D = Path('/var/tmp/sound-analysis/t12-collision/previews')
LO, N = 2205, 16384                                   # window: 50 ms after the onset, 16384 frames


def decode(ogg):
    out = D / (ogg.name + '.f32')
    if not out.exists():
        subprocess.run(['gst-launch-1.0', '-q', 'filesrc', f'location={ogg}', '!', 'oggdemux', '!', 'vorbisdec', '!',
                        'audioconvert', '!', 'audio/x-raw,format=F32LE,channels=2', '!', 'filesink', f'location={out}'], check=True)
    return np.fromfile(out, np.float32).reshape(-1, 2).astype(float)


def spec(x, lo):
    seg = x[lo:lo + N]
    return np.fft.rfftfreq(1 << 18, 1 / FS), np.abs(np.fft.rfft(seg * np.hanning(len(seg))[:, None], 1 << 18, axis=0))


def peaks(hz, s, top=10):
    m = s.sum(1)
    d = 20 * np.log10(m / m.max() + 1e-30)
    k, _ = find_peaks(d, height=-50, distance=200)
    return sorted(k[np.argsort(-d[k])][:top])


def host(stored, hyp):
    h = stored_to_host(stored, 'bipolar' if hyp == 'bipolar' else 'identity')
    if hyp == 'hit_bipolar':
        for r in (1, 2):
            i = idx(f'Resonator{r}/HitX')
            h[i] = 2 * h[i] - 1
    return h


def one(adv):
    cat, name = adv.parent.name, adv.stem
    ogg = PV / cat / f'{name}.adv.ogg'
    if not ogg.exists():
        return dict(preset=f'{cat}/{name}', skipped='no preview')
    s = read_adv(adv)
    pv = decode(ogg)
    on = int(np.argmax(np.abs(pv).max(1) > 1e-3 * np.abs(pv).max()))
    hz, sp = spec(pv, on + LO)
    ks = peaks(hz, sp)
    lr = lambda S: [float(20 * np.log10(S[k, 1] / S[k, 0])) for k in ks]  # noqa: E731
    lev = lambda S: np.array([20 * np.log10(S[k].sum() / S[ks].sum(1).max()) for k in ks])  # noqa: E731
    out = dict(preset=f'{cat}/{name}', adv_sha256=hashlib.sha256(adv.read_bytes()).hexdigest(),
               ogg_sha256=hashlib.sha256(ogg.read_bytes()).hexdigest(), onset_frame=on,
               peaks_hz=[float(hz[k]) for k in ks], preview_lr_db=lr(sp),
               positions={k: v for k, v in s.items() if k.split('/')[-1] in ('HitX', 'ListeningXL', 'ListeningXR')})
    renders = {}
    for hyp in ('identity', 'bipolar', 'hit_bipolar'):
        best = None
        for vel in ((100,) if hyp == 'bipolar' else (64, 100, 127)):
            y, _ = render(script(host(s, hyp), [(0, 0x90, 60, vel)], frames=LO + N + 4096), D / f'r_{name}_{hyp}_{vel}.f32')
            _, sr = spec(y.astype(float), LO)
            e = float(np.median(np.abs(lev(sr) - lev(sp))))
            if best is None or e < best[0]:
                best = (e, vel, sr)
        renders[hyp] = best
    sr = renders['identity'][2].sum(1)
    near = [k - 40 + int(np.argmax(sr[k - 40:k + 41])) for k in ks]           # render peak within +-40 bins (+-6.7 Hz)
    out['render_minus_preview_cents'] = [float(1200 * np.log2(hz[j] / hz[k])) for j, k in zip(near, ks)]
    out['identity_lr_db'] = lr(renders['identity'][2])
    out['bipolar_lr_db'] = lr(renders['bipolar'][2])
    pv_lr = np.array(out['preview_lr_db'])
    out['lr_median_abs_err_db'] = {h: float(np.median(np.abs(np.array(out[f'{h}_lr_db']) - pv_lr))) for h in ('identity', 'bipolar')}
    out['lr_hypotheses_median_separation_db'] = float(np.median(np.abs(np.array(out['identity_lr_db']) - np.array(out['bipolar_lr_db']))))
    out['level_pattern_median_abs_err_db'] = {h: dict(err=renders[h][0], velocity=renders[h][1]) for h in ('identity', 'hit_bipolar')}
    return out


def main():
    xdevpy.build()
    D.mkdir(parents=True, exist_ok=True)
    advs = sorted(p for p in PR.glob('*/*.adv') if not p.name.startswith('._'))
    with cf.ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(one, advs))
    tested = [r for r in rows if 'lr_median_abs_err_db' in r]
    sep = [r for r in tested if r['lr_hypotheses_median_separation_db'] >= 0.5]
    summary = dict(
        presets=len(rows), with_preview=len(tested),
        listening_separating=len(sep),
        listening_identity_better=sum(r['lr_median_abs_err_db']['identity'] < r['lr_median_abs_err_db']['bipolar'] for r in sep),
        listening_identity_err_max_db=max(r['lr_median_abs_err_db']['identity'] for r in sep),
        listening_identity_err_median_db=float(np.median([r['lr_median_abs_err_db']['identity'] for r in sep])),
        listening_bipolar_err_median_db=float(np.median([r['lr_median_abs_err_db']['bipolar'] for r in sep])),
        peak_cents_median_abs=float(np.median([abs(c) for r in tested for c in r['render_minus_preview_cents']])),
        peak_cents_within_5=sum(abs(c) <= 5 for r in tested for c in r['render_minus_preview_cents']),
        peaks=sum(len(r['render_minus_preview_cents']) for r in tested),
        hit_identity_better=sum(r['level_pattern_median_abs_err_db']['identity']['err'] < r['level_pattern_median_abs_err_db']['hit_bipolar']['err'] - 0.1
                                for r in tested),
        hit_bipolar_better=sum(r['level_pattern_median_abs_err_db']['hit_bipolar']['err'] < r['level_pattern_median_abs_err_db']['identity']['err'] - 0.1
                               for r in tested))
    (HERE / 'results' / 'previews.json').write_text(json.dumps(dict(summary=summary, presets=rows), indent=1) + '\n')
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
