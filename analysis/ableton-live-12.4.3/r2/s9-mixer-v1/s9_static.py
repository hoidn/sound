"""S9 static half: track mixer fields in Live's shipped schemas and LiveSet documents.

Usage: python3 -I s9_static.py <bundle Contents dir> <out.json> <inputs.tsv>
Read-only on inputs. Schema part: evolution of the TrackDevice / MainTrackDevice /
TrackSendHolder classes over every Schema/*.txt (AppleDouble '._*' skipped) and the
mixer holder classes in 12.0_12402. Document part: every non-AppleDouble .als/.alc under
Contents; for each track (AudioTrack, MidiTrack, GroupTrack, ReturnTrack, MainTrack,
PreHearTrack) the Mixer children, Manual values and MidiControllerRange of Volume, Pan,
SplitStereoPanL/R, Send, CrossFade, plus PanMode, CrossFadeState, Speaker, SoloSink,
send holder ids and EnabledByUser, sends-vs-returns counts, and every automation/clip
envelope whose PointeeId is a mixer AutomationTarget or ModulationTarget. Number text
is checked against the N1 writer rule (n1-transport-state-v1/check_number_format.py).
inputs.tsv: sha256, bytes, relative path of every document read.
"""
import collections, gzip, hashlib, json, math, os, re, struct, sys
import xml.etree.ElementTree as ET

SCHEMA_CLASSES = ("TrackDevice", "MainTrackDevice", "MasterTrackDevice", "TrackSendHolder")
TRACKS = ("AudioTrack", "MidiTrack", "GroupTrack", "ReturnTrack")
FLOATS = ("Volume", "Pan", "SplitStereoPanL", "SplitStereoPanR", "CrossFade", "GlobalGrooveAmount")


def fmt(x, p=9, pzero=8):  # N1 writer rule for Float (float32 widened to double)
    if x == 0:
        prec = pzero
    else:
        e = math.log10(abs(x)); k = math.floor(e) if e < 0 else math.ceil(e); prec = max(0, p - k)
    s = '%.*f' % (prec, x)
    return s.rstrip('0').rstrip('.') if '.' in s else s


def f32(t):
    return struct.unpack('<f', struct.pack('<f', float(t)))[0]


def vkey(t):
    return t if t is not None else '<absent>'


def schema_part(sdir):
    files = sorted((f for f in os.listdir(sdir) if f.endswith('.txt') and not f.startswith('._')),
                   key=lambda f: [int(x) for x in re.findall(r'\d+', f)])
    evo = {c: collections.defaultdict(list) for c in SCHEMA_CLASSES}
    present = {c: [] for c in SCHEMA_CLASSES}
    holders, latest = {}, {}
    for f in files:
        root = ET.parse(os.path.join(sdir, f)).getroot()
        v = f[:-4]
        for cls in root:
            if cls.tag in SCHEMA_CLASSES:
                present[cls.tag].append(v)
                for fld in cls:
                    evo[cls.tag][fld.tag].append((v, f"{fld.get('Class')}·{fld.get('Type')}"))
            if f == files[-1]:
                for fld in cls:
                    if fld.tag == 'Mixer':
                        holders[cls.tag] = fld.get('Class')
        if f == files[-1]:
            latest = {c: [[x.tag, x.get('Class'), x.get('Type')] for x in root.find(c)]
                      for c in SCHEMA_CLASSES if root.find(c) is not None}
    segs = {}
    for c, flds in evo.items():
        segs[c] = {}
        for name, occ in flds.items():
            runs = []
            for v, ct in occ:
                if runs and runs[-1][2] == ct and files.index(runs[-1][1] + '.txt') + 1 == files.index(v + '.txt'):
                    runs[-1][1] = v
                else:
                    runs.append([v, v, ct])
            segs[c][name] = {'count': len(occ), 'segments': runs}
    return {'files': len(files), 'latest': files[-1], 'class_present': {c: [len(p), p[:1], p[-1:]] for c, p in present.items()},
            'evolution': segs, 'latest_fields': latest, 'mixer_holders_latest': holders}


def manual(el, sub):
    x = el.find(sub)
    return None if x is None else {
        'manual': (x.find('Manual').get('Value') if x.find('Manual') is not None else None),
        'range': [None if x.find(f'MidiControllerRange/{b}') is None else x.find(f'MidiControllerRange/{b}').get('Value')
                  for b in ('Min', 'Max')],
        'auto': x.find('AutomationTarget').get('Id') if x.find('AutomationTarget') is not None else None,
        'mod': x.find('ModulationTarget').get('Id') if x.find('ModulationTarget') is not None else None}


def doc_part(path, rel, acc):
    raw = open(path, 'rb').read()
    data = gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
    root = ET.fromstring(data)
    ls = root.find('LiveSet')
    if ls is None:
        return None
    meta = (root.get('MinorVersion'), root.get('Creator'))
    acc['docs_by_version'][f'{meta[0]} | {meta[1]}'] += 1
    tracks = [(t.tag, t) for t in (ls.find('Tracks') if ls.find('Tracks') is not None else [])]
    tracks += [(n, ls.find(n)) for n in ('MainTrack', 'PreHearTrack') if ls.find(n) is not None]
    nreturn = sum(1 for k, _ in tracks if k == 'ReturnTrack')
    acc['returns_per_doc'][nreturn] += 1
    for kind, tr in tracks:
        mx = tr.find('DeviceChain/Mixer')
        if mx is None:
            acc['no_mixer'][kind] += 1
            continue
        a = acc['tracks'][kind]
        a['count']['tracks'] += 1
        a['children'][' '.join(c.tag for c in mx)] += 1
        ids = {}
        for name in FLOATS:
            m = manual(mx, name)
            if m is None:
                continue
            a[name + '.manual'][m['manual']] += 1
            a[name + '.range'][' '.join(map(vkey, m['range']))] += 1
            acc['value_docs'][f"{name}.range {' '.join(map(vkey, m['range']))}"].add(rel)
            acc['value_docs'][f"{kind}/{name}.manual {m['manual']}"].add(rel)
            ids[m['auto']] = (name, 'automation'); ids[m['mod']] = (name, 'modulation')
            acc['lexical'][name][fmt(f32(m['manual'])) == m['manual']] += 1
            if name == 'Volume':
                g = f32(m['manual'])
                acc['volume_db'][kind].append(round(20 * math.log10(g), 6) if g > 0 else None)
        for name in ('CrossFadeState', 'Speaker'):
            x = mx.find(name)
            if x is not None:
                a[name + '.manual'][x.find('Manual').get('Value')] += 1
                ids[x.find('AutomationTarget').get('Id')] = (name, 'automation')
        for name in ('PanMode', 'SoloSink'):
            x = mx.find(name)
            a[name][vkey(None if x is None else x.get('Value'))] += 1
        hs = mx.findall('Sends/TrackSendHolder')
        a['sends_minus_returns'][len(hs) - nreturn] += 1
        a['send_holder_ids'][' '.join(h.get('Id') for h in hs)] += 1
        for i, h in enumerate(hs):
            m = manual(h, 'Send')
            a['Send.manual'][m['manual']] += 1
            a['Send.range'][' '.join(map(vkey, m['range']))] += 1
            acc['value_docs'][f"Send.range {' '.join(map(vkey, m['range']))}"].add(rel)
            a['Send.EnabledByUser'][h.find('EnabledByUser').get('Value')] += 1
            acc['lexical']['Send'][fmt(f32(m['manual'])) == m['manual']] += 1
            ids[m['auto']] = (f'Send', 'automation'); ids[m['mod']] = ('Send', 'modulation')
            g = f32(m['manual'])
            acc['send_db'].append(round(20 * math.log10(g), 6) if g > 0 else None)
        ids.pop(None, None)
        for env in list(tr.iter('AutomationEnvelope')) + list(tr.iter('ClipEnvelope')):
            pid = env.find('EnvelopeTarget/PointeeId')
            hit = ids.get(None if pid is None else pid.get('Value'))
            if not hit:
                continue
            key = f'{kind}/{hit[0]}/{hit[1]}/{env.tag}'
            e = acc['envelopes'].setdefault(key, {'envelopes': 0, 'event_tags': collections.Counter(),
                                                  'min': None, 'max': None, 'values': collections.Counter()})
            e['envelopes'] += 1
            for ev in env.findall('Automation/Events/*'):
                e['event_tags'][ev.tag] += 1
                v = ev.get('Value')
                if ev.tag == 'FloatEvent':
                    x = float(v)
                    e['min'] = x if e['min'] is None else min(e['min'], x)
                    e['max'] = x if e['max'] is None else max(e['max'], x)
                    acc['lexical']['FloatEvent(mixer)'][fmt(f32(v)) == v] += 1
                else:
                    e['values'][v] += 1
    return meta


def main(contents, out, tsv):
    sdir = os.path.join(contents, 'App-Resources', 'Schema')
    res = {'schema': schema_part(sdir)}
    C = collections.Counter
    acc = {'docs_by_version': C(), 'returns_per_doc': C(), 'no_mixer': C(),
           'tracks': collections.defaultdict(lambda: collections.defaultdict(C)),
           'lexical': collections.defaultdict(C), 'volume_db': collections.defaultdict(list),
           'send_db': [], 'envelopes': {}, 'value_docs': collections.defaultdict(set)}
    rows, skipped = [], 0
    for d, _, fs in sorted(os.walk(contents)):
        for n in sorted(fs):
            if not n.endswith(('.als', '.alc')):
                continue
            p = os.path.join(d, n)
            if n.startswith('._'):
                assert open(p, 'rb').read(4) == bytes.fromhex('00051607'), p
                skipped += 1
                continue
            raw = open(p, 'rb').read()
            rel = os.path.relpath(p, contents)
            rows.append(f'{hashlib.sha256(raw).hexdigest()}\t{len(raw)}\t{rel}\n')
            doc_part(p, rel, acc)
    open(tsv, 'w').writelines(rows)
    # summarise volume/send dB grids: how many stored gains sit on a 0.01 dB / 0.1 dB / 1 dB grid
    def grid(vals):
        g = C()
        for v in vals:
            if v is None:
                g['nonpositive'] += 1
                continue
            for step in (1, 0.1, 0.01):
                if abs(v / step - round(v / step)) < 1e-3:
                    g[f'on {step} dB grid'] += 1
                    break
            else:
                g['off 0.01 dB grid'] += 1
        return dict(g)
    allvol = [v for vs in acc['volume_db'].values() for v in vs]
    res['documents'] = {
        'files': len(rows), 'appledouble_skipped': skipped,
        'docs_by_version': dict(acc['docs_by_version']), 'returns_per_doc': dict(sorted(acc['returns_per_doc'].items())),
        'tracks_without_mixer': dict(acc['no_mixer']),
        'tracks': {k: {f: (dict(c.most_common()) if isinstance(c, C) else c) for f, c in v.items()} for k, v in acc['tracks'].items()},
        'lexical_rule_match': {k: {'match': c[True], 'mismatch': c[False]} for k, c in acc['lexical'].items()},
        'volume_db_grid': grid(allvol), 'volume_db_range': [min(x for x in allvol if x is not None), max(x for x in allvol if x is not None)],
        'send_db_grid': grid(acc['send_db']),
        'send_db_range': [min(x for x in acc['send_db'] if x is not None), max(x for x in acc['send_db'] if x is not None)],
        'rare_value_docs': {k: sorted(v) for k, v in sorted(acc['value_docs'].items()) if len(v) <= 12},
        'envelopes': {k: {**v, 'event_tags': dict(v['event_tags']), 'values': dict(v['values'])} for k, v in sorted(acc['envelopes'].items())},
    }
    json.dump(res, open(out, 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main(*sys.argv[1:4])
