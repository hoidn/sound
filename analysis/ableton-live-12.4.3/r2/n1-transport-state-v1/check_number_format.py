"""Check the statically derived Float/Double text rule against shipped LiveSet documents.

Rule (derived from FUN_101431584 / FUN_101431788 disassembly, see notes.md): for x != 0,
k = ceil(log10|x|) if log10|x| >= 0 else floor(log10|x|); precision = max(0, P - k) with P = 9 (Float,
value first widened to double) or 17 (Double); zero uses precision 8 / 16; format "%.*f", then strip
trailing '0's and a trailing '.' if the text contains '.'. Non-finite values and FLT_MAX/DBL_MAX use
other spellings and are not covered here.
usage: python3 -I check_number_format.py <bundle App-Resources dir>   (reads .als/.alc read-only)
Output: per-field counts of matches; exits 1 on any mismatch.
"""
import gzip, math, os, struct, sys
import xml.etree.ElementTree as ET

def fmt(x, p, pzero):
    if x == 0: prec = pzero
    else:
        e = math.log10(abs(x)); k = math.floor(e) if e < 0 else math.ceil(e); prec = max(0, p - k)
    s = '%.*f' % (prec, x)
    if '.' in s: s = s.rstrip('0').rstrip('.')
    return s

def f32(t): return struct.unpack('<f', struct.pack('<f', float(t)))[0]

FIELDS = {  # path below LiveSet -> (P, zero precision, widen-from-float)
    'Transport/LoopStart': (17, 16, False), 'Transport/LoopLength': (17, 16, False),
    'Transport/CurrentTime': (17, 16, False),
    'MainTrack/DeviceChain/Mixer/Tempo/Manual': (9, 8, True),
}

def main(root):
    stats, bad = {}, []
    for d, _, files in os.walk(root):
        for n in files:
            if n.startswith('._') or not n.endswith(('.als', '.alc')): continue
            p = os.path.join(d, n)
            ls = ET.fromstring(gzip.open(p).read()).find('LiveSet')
            for path, (P, PZ, widen) in FIELDS.items():
                t = ls.find(path).get('Value')
                x = f32(t) if widen else float(t)
                ok = fmt(x, P, PZ) == t
                stats.setdefault(path, [0, 0])[0 if ok else 1] += 1
                if not ok: bad.append((p, path, t, fmt(x, P, PZ)))
            for ev in ls.iter('FloatEvent'):  # automation events are Float in the 12.0_12402 schema
                t = ev.get('Value'); ok = fmt(f32(t), 9, 8) == t
                stats.setdefault('FloatEvent/@Value', [0, 0])[0 if ok else 1] += 1
                if ok and '%.9g' % f32(t) != t:  # values that discriminate this rule from %.9g
                    stats.setdefault('FloatEvent/@Value where %.9g differs', [0, 0])[0] += 1
                if not ok: bad.append((p, 'FloatEvent', t, fmt(f32(t), 9, 8)))
    for k, (ok, ko) in sorted(stats.items()): print(f'{k}: {ok} match, {ko} mismatch')
    for b in bad[:20]: print('MISMATCH', *b)
    # static predictions for values not present in shipped documents
    for x, P, PZ in [(0.1, 9, 8), (0.5, 17, 16), (100.0, 17, 16), (1e20, 17, 16), (-8.0, 17, 16)]:
        print('predict', x, 'P=%d' % P, fmt(f32(x) if P == 9 else x, P, PZ))
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
