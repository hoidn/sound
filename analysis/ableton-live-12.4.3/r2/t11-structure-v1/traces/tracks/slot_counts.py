"""Per-track clip-slot counts (main vs freeze sequencer) against scene count, and track order,
over every non-AppleDouble .als/.alc under the bundle (read-only; output is data).
usage: python3 -I slot_counts.py <App-Resources dir>"""
import collections, gzip, os, sys
import xml.etree.ElementTree as ET
root = sys.argv[1]; c = collections.Counter(); ex = collections.defaultdict(list)
for d, _, fs in os.walk(root):
    for f in sorted(fs):
        if f.startswith('._') or not f.endswith(('.als', '.alc')): continue
        p = os.path.join(d, f); b = open(p, 'rb').read()
        if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
        ls = ET.fromstring(b).find('LiveSet'); kind = f[-3:]
        nsc = len(ls.findall('Scenes/Scene'))
        tr = list(ls.find('Tracks'))
        c[(kind, 'scenes', nsc)] += 1
        tags = [t.tag for t in tr]
        firstret = next((i for i, t in enumerate(tags) if t == 'ReturnTrack'), len(tags))
        c[(kind, 'returns-last', all(t == 'ReturnTrack' for t in tags[firstret:]))] += 1
        c[(kind, 'has-player-track', any(t in ('AudioTrack', 'MidiTrack') for t in tags))] += 1
        nret = tags.count('ReturnTrack')
        c[(kind, 'sendspre==returns', len(ls.findall('SendsPre/SendPreBool')) == nret)] += 1
        for t in tr:
            if t.tag in ('AudioTrack', 'MidiTrack'):
                m = t.findall('DeviceChain/MainSequencer/ClipSlotList/ClipSlot')
                fz = t.find('DeviceChain/FreezeSequencer')
                fzn = None if fz is None else len(fz.findall('ClipSlotList/ClipSlot'))
                c[(kind, t.tag, 'main==scenes', len(m) == nsc)] += 1
                c[(kind, t.tag, 'freeze==main', fzn == len(m))] += 1
                if fzn != len(m) or len(m) != nsc: ex[(kind, t.tag)].append((os.path.relpath(p, root), len(m), fzn, nsc))
            if t.tag == 'GroupTrack':
                c[(kind, 'group-slots==scenes', len(t.findall('Slots/GroupTrackSlot')) == nsc)] += 1
            c[(kind, t.tag, 'TrackGroupId', t.find('TrackGroupId').get('Value'))] += 1
            ids = [x.get('Id') for x in t.findall('DeviceChain/MainSequencer/ClipSlotList/ClipSlot')]
            c[(kind, 'slot-ids-0..n-1', ids == [str(i) for i in range(len(ids))])] += 1
        tids = [t.get('Id') for t in tr]
        c[(kind, 'track-ids-unique', len(set(tids)) == len(tids))] += 1
        sids = [s.get('Id') for s in ls.findall('Scenes/Scene')]
        c[(kind, 'scene-ids-0..n-1', sids == [str(i) for i in range(len(sids))])] += 1
for k, v in sorted(c.items(), key=str): print(k, v)
for k, v in ex.items(): print('EXCEPTIONS', k, len(v), v[:5])
