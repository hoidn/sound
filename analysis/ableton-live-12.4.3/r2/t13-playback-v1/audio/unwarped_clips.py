"""List AudioClip elements with IsWarped false in shipped Live Sets (read-only; output is data).

usage: python3 -I unwarped_clips.py <set.als>...    prints one JSON object per unwarped AudioClip:
set path, SHA-256, where the clip sits (session slot or arrangement), and the playback-relevant fields.
"""
import gzip, hashlib, json, sys
import xml.etree.ElementTree as ET

F = ['CurrentStart', 'CurrentEnd', 'IsWarped', 'WarpMode', 'HiQ', 'Fade', 'PitchCoarse', 'PitchFine',
     'SampleVolume', 'LaunchMode', 'LaunchQuantisation', 'Disabled']
L = ['LoopStart', 'LoopEnd', 'StartRelative', 'LoopOn', 'OutMarker', 'HiddenLoopStart', 'HiddenLoopEnd']


def val(el, tag):
    c = el.find(tag)
    if c is None:
        return None
    m = c.find('Manual')
    return (m if m is not None else c).get('Value')


def main():
    for p in sys.argv[1:]:
        try:
            raw = gzip.open(p).read()
        except gzip.BadGzipFile:
            print('skip (not gzip):', p, file=sys.stderr)
            continue
        sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        root = ET.fromstring(raw)
        parent = {c: q for q in root.iter() for c in q}
        for clip in root.iter('AudioClip'):
            if val(clip, 'IsWarped') != 'false':
                continue
            chain, q = [], clip
            while q in parent:
                q = parent[q]
                chain.append(q.tag)
            where = 'session' if 'ClipSlot' in chain else ('arrangement' if 'ArrangerAutomation' in chain else '/'.join(chain[:4]))
            loop = clip.find('Loop')
            sref = clip.find('SampleRef')
            fref = sref.find('FileRef') if sref is not None else None
            rec = {'set': p, 'sha256': sha, 'where': where, 'name': val(clip, 'Name'),
                   **{k: val(clip, k) for k in F}, **({k: val(loop, k) for k in L} if loop is not None else {}),
                   'RelativePath': fref.find('RelativePath').get('Value') if fref is not None else None,
                   'DefaultDuration': val(sref, 'DefaultDuration') if sref is not None else None,
                   'DefaultSampleRate': val(sref, 'DefaultSampleRate') if sref is not None else None,
                   'Fades': {c.tag: c.get('Value') for c in clip.find('Fades')} if clip.find('Fades') is not None else None,
                   'WarpMarkers': [(m.get('SecTime'), m.get('BeatTime')) for m in clip.iter('WarpMarker')]}
            print(json.dumps(rec))


if __name__ == '__main__':
    main()
