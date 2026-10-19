"""Scan shipped Live Sets and clips for session/arrangement MidiClip loop fields (read-only; output is data).
usage: python3 -I midi/scan_clip_loops.py <App-Resources dir>
Prints counts of MidiClips by LoopOn and whether StartRelative is 0, and examples."""
import gzip, os, sys, xml.etree.ElementTree as ET
root = sys.argv[1]
stats, ex = {}, {}
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith(('.als', '.alc')):
            continue
        p = os.path.join(dp, f)
        try:
            t = ET.fromstring(gzip.open(p).read())
        except Exception as e:
            continue
        for c in t.iter('MidiClip'):
            lp = c.find('Loop')
            if lp is None:
                continue
            v = {k: lp.find(k).get('Value') for k in ('LoopStart', 'LoopEnd', 'StartRelative', 'LoopOn', 'OutMarker', 'HiddenLoopStart', 'HiddenLoopEnd') if lp.find(k) is not None}
            key = (v.get('LoopOn'), float(v.get('StartRelative', '0')) == 0.0)
            stats[key] = stats.get(key, 0) + 1
            ex.setdefault(key, (os.path.relpath(p, root), c.get('Time'), v))
for k in sorted(stats, key=str):
    print('LoopOn=%s StartRelative==0:%s count=%d example=%s' % (k[0], k[1], stats[k], ex[k]))


def iswarped(root):
    """Count shipped MidiClip IsWarped values (second report)."""
    cnt = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(('.als', '.alc')):
                try:
                    t = ET.fromstring(gzip.open(os.path.join(dp, f)).read())
                except Exception:
                    continue
                for c in t.iter('MidiClip'):
                    w = c.find('IsWarped')
                    k = w.get('Value') if w is not None else None
                    cnt[k] = cnt.get(k, 0) + 1
    print('MidiClip IsWarped:', cnt)


iswarped(root)
