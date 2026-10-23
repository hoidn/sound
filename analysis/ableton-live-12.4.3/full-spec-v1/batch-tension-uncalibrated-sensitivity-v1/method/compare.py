import numpy as np
import measure as M

def compare(name, x, r, meas):
    c = cases.CASES[name]
    on, off, fs = M.onset(r), c['off'], c['fs']
    d = dict(whole=M.rel_rms(x[on:], r[on:]), held=M.rel_rms(x[on:off], r[on:off]), release=M.rel_rms(x[off:], r[off:]),
             first_2048=M.rel_rms(x[on:on + 2048], r[on:on + 2048]))
    d['modal'] = M.modal_compare(x, r, meas['held'], fs) if meas.get('held') else None
    a = on + 2048
    tx, tr = np.array(M.third_octave(x, a, off, fs)), np.array(M.third_octave(r, a, off, fs))
    sel = tr >= tr.max() - 40                                      # bands within 40 dB of the strongest
    d['third_octave_max_db'] = float(np.max(np.abs(tx[sel] - tr[sel])))
    er, ex = M.env_db(r, fs // 20), M.env_db(x, fs // 20)
    sel = er > er.max() - 60
    d['env_50ms_max_db'] = float(np.max(np.abs(ex[sel] - er[sel])))
    d['held_rms_db'] = float(20 * np.log10(np.sqrt(np.mean(x[a:off] ** 2)) / np.sqrt(np.mean(r[a:off] ** 2))))
    d['onset_shift_frames'] = M.onset(x) - on
    d['last_nonzero_shift_frames'] = (M.last(x) or 0) - (M.last(r) or 0)
    return d

