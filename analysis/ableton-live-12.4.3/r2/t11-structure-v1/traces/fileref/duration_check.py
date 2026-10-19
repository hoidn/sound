"""Compare SampleRef DefaultDuration/DefaultSampleRate with the referenced file's own header (read-only; output is data).
Only Core Library files present in the bundle (LivePackName 'Core Library', RelativePathType 5).
WAV: fmt/data chunks (frames = data bytes / block align); AIFF/AIFC: COMM numSampleFrames and 80-bit rate.
usage: python3 -I duration_check.py <App-Resources dir>"""
import collections, gzip, math, os, struct, sys
import xml.etree.ElementTree as ET

def header(p):
    b = open(p, 'rb').read(1 << 20)
    if b[:4] in (b'RIFF', b'RF64') and b[8:12] == b'WAVE':
        o, fmt, frames = 12, None, None
        while o + 8 <= len(b):
            cid, n = b[o:o+4], struct.unpack_from('<I', b, o + 4)[0]
            if cid == b'fmt ': fmt = struct.unpack_from('<HHIIHH', b, o + 8)
            if cid == b'data':
                frames = (n // fmt[4]) if fmt else None; break
            o += 8 + n + (n & 1)
        return ('wav', frames, fmt[2] if fmt else None, fmt[1] if fmt else None)
    if b[:4] == b'FORM' and b[8:12] in (b'AIFF', b'AIFC'):
        o = 12
        while o + 8 <= len(b):
            cid, n = b[o:o+4], struct.unpack_from('>I', b, o + 4)[0]
            if cid == b'COMM':
                ch, frames, bits = struct.unpack_from('>hIh', b, o + 8)
                e, m = struct.unpack_from('>HQ', b, o + 16)
                rate = m * 2.0 ** ((e & 0x7fff) - 16383 - 63)
                return ('aiff', frames, rate, ch)
            o += 8 + n + (n & 1)
    return ('other', None, None, None)

root = sys.argv[1]; res = collections.Counter(); ex = []
seen = set()
for d, _, fs in os.walk(root):
    for f in fs:
        if f.startswith('._') or not f.endswith(('.als', '.alc')): continue
        b = open(os.path.join(d, f), 'rb').read()
        if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
        for sr in ET.fromstring(b).iter('SampleRef'):
            fr = sr.find('FileRef'); v = {ch.tag: ch.get('Value') for ch in fr}
            if v.get('LivePackName') != 'Core Library': continue
            p = os.path.join(root, 'Core Library', v['RelativePath'])
            if not os.path.isfile(p): res['absent'] += 1; continue
            dd, dr = int(sr.find('DefaultDuration').get('Value')), int(sr.find('DefaultSampleRate').get('Value'))
            k = (p, dd, dr)
            if k in seen: continue
            seen.add(k)
            kind, frames, rate, ch = header(p)
            r = f"{kind} frames {'=' if frames == dd else '!='} rate {'=' if rate is not None and int(rate) == dr else '!='}"
            res[r] += 1
            if '!=' in r and len(ex) < 12: ex.append((os.path.relpath(p, root), dd, dr, frames, rate))
for k, n in sorted(res.items()): print(k, n)
for e in ex: print('example', e)
