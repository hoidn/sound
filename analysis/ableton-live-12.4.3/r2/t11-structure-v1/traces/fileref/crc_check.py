"""Check OriginalFileSize/OriginalCrc of shipped SampleRefs against files in the bundle (read-only; output is data).
CRC rule read from arm64 0x101279eac/0x1011b6e88: CRC-16, poly 0x8005, MSB first, init 0, no reflection,
no final xor, over the first min(16384, size) bytes. usage: python3 -I crc_check.py <App-Resources dir>"""
import collections, gzip, os, sys
import xml.etree.ElementTree as ET

def crc16(data):
    c = 0
    for b in data:
        c ^= b << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x8005) if c & 0x8000 else (c << 1)
            c &= 0xffff
    return c

assert crc16(b'123456789') == 0xFEE8  # CRC-16/UMTS check value
root = sys.argv[1]
res = collections.Counter(); seen = {}
for d, _, fs in os.walk(root):
    for f in fs:
        if f.startswith('._') or not f.endswith(('.als', '.alc')): continue
        b = open(os.path.join(d, f), 'rb').read()
        if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
        for fr in ET.fromstring(b).iter('FileRef'):
            v = {ch.tag: ch.get('Value') for ch in fr}
            if v.get('LivePackName') != 'Core Library' or v.get('OriginalFileSize') in (None, '0'): continue
            p = os.path.join(root, 'Core Library', v['RelativePath'])
            if p in seen: continue
            if not os.path.isfile(p): res['file absent'] += 1; seen[p] = None; continue
            data = open(p, 'rb').read()
            ok_size = len(data) == int(v['OriginalFileSize']); ok_crc = crc16(data[:16384]) == int(v['OriginalCrc'])
            seen[p] = (ok_size, ok_crc); res[f'size {ok_size} crc {ok_crc}'] += 1
for k, n in sorted(res.items()): print(k, n)
for p, r in list(seen.items()):
    if r and not all(r): print('mismatch', p, r)
