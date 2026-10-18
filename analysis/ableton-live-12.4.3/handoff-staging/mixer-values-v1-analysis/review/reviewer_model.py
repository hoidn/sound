# Reviewer check (analyst-side; not payload): an independent restatement of the released clauses of
# mixer-values-v1, written from the reviewer's own reading of the evidence, not from build_mv1.py.
# It reads each fixture, checks its form against the contract's preconditions, derives every value, text
# and name, and compares them with cases.json. It also re-derives the contract's worked examples, the
# boundary distances of every graded gain, and the effect of a log10 result off by up to 3 binary32 steps.
# usage: python3 -I reviewer_model.py <package dir>
import json, re, struct, sys, xml.etree.ElementTree as ET
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
getcontext().prec = 80
PKG = Path(sys.argv[1])

def f32(x):
    """Nearest binary32 to the rational x (ties to even), computed exactly; normal range only."""
    x = Fraction(x)
    if x == 0: return 0.0
    s = -1 if x < 0 else 1; x = abs(x)
    e = x.numerator.bit_length() - x.denominator.bit_length()
    if Fraction(2) ** e > x: e -= 1
    m = x / Fraction(2) ** (e - 23)           # in [2^23, 2^24)
    q, r = divmod(m.numerator, m.denominator); r = Fraction(r, m.denominator)
    if r > Fraction(1, 2) or (r == Fraction(1, 2) and q & 1): q += 1
    return s * float(Fraction(q) * Fraction(2) ** (e - 23))
def step32(v, k):
    if v == 0: return k * 2.0 ** -149
    b = struct.unpack('<i', struct.pack('<f', v))[0]
    return struct.unpack('<f', struct.pack('<i', b + (k if v > 0 else -k)))[0]
def half_gap(t):
    """Distance of decimal text t from the nearest binary32 rounding midpoint, in units of the binary32 step."""
    x = Fraction(t); v = f32(x)
    lo, hi = sorted((v, step32(v, 1) if x >= v else step32(v, -1)))
    mid = (Fraction(lo) + Fraction(hi)) / 2
    return float(abs(x - mid) / (Fraction(hi) - Fraction(lo)))

NUM = re.compile(r'-?[0-9]+(\.[0-9]+)?$')
def number(t):
    assert NUM.match(t), t
    v = f32(Fraction(t))
    assert v == struct.unpack('<f', struct.pack('<f', float(t)))[0], ('double route differs', t)
    return v
def boolean(t):
    assert t in ('true', 'false'), t
    return t == 'true'
def code(t):
    assert re.fullmatch(r'[0-9]+', t), t
    return int(t)

def log10_exact(g): return Fraction(Decimal(Fraction(g).numerator).log10() - Decimal(Fraction(g).denominator).log10())
def db_text(g, k=0):
    L = step32(f32(log10_exact(g)), k) if k else f32(log10_exact(g))
    db = f32(Fraction(L) * 20)
    if db <= -70.0 + 0.3: return '-inf dB'
    t = db * 1000.0
    r = (int(abs(t) + 0.5)) * (1 if t >= 0 else -1)          # round half away from zero
    v = 0.0 if r == 0 else db
    s = '%.3f' % v
    while s.endswith('0') and len(s.split('.')[1]) > 1: s = s[:-1]
    return s + ' dB'
def db_margins(g):
    d = 20 * log10_exact(g)
    near = [abs(d - Fraction(-697, 10)), abs(abs(d) - Fraction(5, 10000))]
    h = (d * 1000 - Fraction(1, 2)); h = abs(h - round(h)) / 1000      # distance to n/1000 + 0.0005
    return float(d), float(min(near)), float(h)
def pan_text(p):
    if -0.01 <= p <= 0.01: return 'C'
    x = abs(p) * 50.0
    assert Fraction(x) == abs(Fraction(p)) * 50 and Fraction(x) % 1 != Fraction(1, 2), p
    return '%.0f' % x + ('L' if p < 0 else 'R')

PANMODE = ['Stereo', 'Split Stereo']; XFADE = ['A', 'None', 'B']
CURVE = ['Dipped', 'Intermediate', 'Constant Power', 'Slow Fade', 'Slow Cut', 'Fast Cut', 'Transition']
LO = f32(Fraction('0.0003162277571')); VHI = f32(Fraction('1.99526238'))
ORDER = ['Sends', 'Speaker', 'SoloSink', 'PanMode', 'Pan', 'SplitStereoPanL', 'SplitStereoPanR', 'Volume', 'CrossFadeState']

def read(path):
    root = ET.parse(path).getroot()
    assert root.tag == 'Ableton' and root.attrib == {'MajorVersion': '5', 'MinorVersion': '12.0_12402', 'SchemaChangeCount': '1'}
    ls = root[0]; assert ls.tag == 'LiveSet' and len(root) == 1
    tracks = ls.find('Tracks')
    assert [t.tag for t in tracks] == ['AudioTrack', 'MidiTrack', 'ReturnTrack']
    mixers = {'audio': tracks[0], 'midi': tracks[1], 'return': tracks[2], 'main': ls.find('MainTrack'), 'cue': ls.find('PreHearTrack')}
    vals, counts, margins = {}, {}, []
    for name, tr in mixers.items():
        mx = tr.find('DeviceChain/Mixer'); assert [c.tag for c in tr] == ['DeviceChain'] and [c.tag for c in tr[0]] == ['Mixer']
        assert [c.tag for c in mx] == ORDER + (['CrossFade'] if name == 'main' else []), name
        holders = list(mx.find('Sends'))
        counts[name] = len(holders)
        assert len(holders) == (0 if name in ('main', 'cue') else 1)
        for h in holders:
            assert h.tag == 'TrackSendHolder' and h.attrib == {'Id': '0'} and [c.tag for c in h] == ['Send', 'EnabledByUser']
            assert h.find('EnabledByUser').get('Value') == ('false' if name == 'return' else 'true')
            g = number(h.find('Send/Manual').get('Value')); assert LO <= g <= 1.0
            margins.append((name + '/Send', g) + db_margins(g))
            vals[name + '/Send'] = {'value': g, 'text': db_text(g)}
        assert mx.find('SoloSink').get('Value') == 'false'
        sp = boolean(mx.find('Speaker/Manual').get('Value')); vals[name + '/Speaker'] = {'value': sp, 'text': 'On' if sp else 'Off'}
        pm = code(mx.find('PanMode').get('Value')); vals[name + '/PanMode'] = {'value': pm, 'name': PANMODE[pm]}
        for el in ('Pan', 'SplitStereoPanL', 'SplitStereoPanR'):
            p = number(mx.find(el + '/Manual').get('Value')); assert -1 <= p <= 1
            vals[name + '/' + el] = {'value': p, 'text': pan_text(p)}
        g = number(mx.find('Volume/Manual').get('Value')); assert LO <= g <= VHI
        margins.append((name + '/Volume', g) + db_margins(g))
        vals[name + '/Volume'] = {'value': g, 'text': db_text(g)}
        xf = code(mx.find('CrossFadeState/Manual').get('Value')); vals[name + '/CrossFadeState'] = {'value': xf, 'name': XFADE[xf]}
        if name == 'main':
            c = number(mx.find('CrossFade/Manual').get('Value')); assert -1 <= c <= 1; vals['main/CrossFade'] = {'value': c}
    cc = code(ls.find('CrossfadeCurve').get('Value')); vals['set/CrossfadeCurve'] = {'value': cc, 'name': CURVE[cc]}
    assert [c.tag for c in ls] == ['Tracks', 'MainTrack', 'PreHearTrack', 'CrossfadeCurve']
    return vals, counts, margins

cases = json.loads((PKG / 'cases.json').read_text())['cases']
base, _, _ = read(PKG / cases[0]['input'])
bad, worst = [], []
for c in cases:
    vals, counts, margins = read(PKG / c['input'])
    exp = c['expected']
    if exp['outcome'] != 'opens': bad.append((c['id'], 'outcome'))
    for k, e in exp['values'].items():
        if vals[k] != e: bad.append((c['id'], k, e, vals[k]))
    if 'send_counts' in exp and any(counts[m] != n for m, n in exp['send_counts'].items()): bad.append((c['id'], 'send_counts'))
    changed = sorted(k for k in vals if vals[k] != base[k])
    if c['id'] != 'MIXER-VALUES-001' and sorted(exp['values']) != changed: bad.append((c['id'], 'listed != changed', changed))
    for key, g, d, near, half in margins:
        if any(k == key for k in exp['values']) and (c['id'] == 'MIXER-VALUES-001' or key in changed):
            stable = all(db_text(g, k) == db_text(g) for k in range(-3, 4))
            worst.append((c['id'], key, g, round(d, 7), db_text(g), round(near, 6), round(half, 6), stable))
print('cases', len(cases), 'mismatches', bad)
print('graded gains: case, key, gain, exact dB, text, distance to -69.7 or +-0.0005, distance to a 3-decimal halfway point, text unchanged for log10 off by -3..+3 steps')
for w in sorted(set(worst), key=lambda w: w[0]): print(' ', w)
print('closest to -69.7 or +-0.0005:', min(w[5] for w in worst), ' closest to a halfway point:', min(w[6] for w in worst),
      ' all stable:', all(w[7] for w in worst))
# fixture number texts: distance from a binary32 rounding midpoint (0.5 means exactly on a binary32 value)
texts = sorted({m.group(1) for c in cases for m in re.finditer(r'Value="(-?[0-9.]+)"', (PKG / c['input']).read_text()) if '.' in m.group(1)})
print('decimal texts in fixtures and their distance from a binary32 midpoint (in steps):', [(t, round(half_gap(t), 4)) for t in texts])
# worked examples of the contract
ex6 = {'1': '0.0 dB', '0.5011872053': '-6.0 dB', '0.5': '-6.021 dB', '0.25': '-12.041 dB', '0.30725': '-10.25 dB',
       '0.7367056608': '-2.654 dB', '1.5': '3.522 dB', '1.99526238': '6.0 dB', '0.99999': '0.0 dB',
       '0.0003311311302': '-69.6 dB', '0.0003235936455': '-inf dB', '0.0003162277571': '-inf dB'}
ex7 = {'-1': '50L', '-0.6': '30L', '-0.5': '25L', '0.2': '10R', '0.5': '25R', '1': '50R', '0.004999999888': 'C',
       '0.01': 'C', '0.0101': '1R', '-0.0101': '1L', '0.33': '17R'}
print('REQ-006 examples wrong:', [(t, db_text(number(t)), e) for t, e in ex6.items() if db_text(number(t)) != e])
print('REQ-007 examples wrong:', [(t, pan_text(number(t)), e) for t, e in ex7.items() if pan_text(number(t)) != e])
p = number('0.33'); print('pan 0.33: binary32', repr(p), 'x50 =', repr(abs(p) * 50.0), '->', pan_text(p), '; decimal 0.33 x50 = 16.5 exactly (a tie)')
# range ends: are they the binary32 numbers nearest to 10^(-70/20) and 10^(6/20)?
for t, dbv in (('0.0003162277571', -70), ('1.99526238', 6)):
    v = number(t); exact = 10 ** (Decimal(dbv) / 20)
    print('range end', t, '=', repr(v), '; nearest binary32 to 10^(%d/20) is' % dbv, repr(f32(Fraction(exact))), '; equal:', v == f32(Fraction(exact)))
