"""Census of SampleRef/FileRef values in shipped Live Sets and clips (read-only; output is data).
usage: python3 -I fileref_survey.py <bundle App-Resources dir> > fileref-survey.json"""
import collections, gzip, json, os, sys
import xml.etree.ElementTree as ET
root = sys.argv[1]
c = collections.defaultdict(collections.Counter)
docs = 0
for d, _, fs in os.walk(root):
    for f in sorted(fs):
        if f.startswith('._') or not f.endswith(('.als', '.alc')): continue
        p = os.path.join(d, f); docs += 1
        b = open(p, 'rb').read()
        if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
        t = ET.fromstring(b)
        par = {ch: pa for pa in t.iter() for ch in pa}
        for fr in t.iter('FileRef'):
            owner = par.get(fr); owner = owner.tag if owner is not None else None
            gp = par.get(par.get(fr)) if owner else None
            k = f"{owner}<{gp.tag if gp is not None else None}"
            v = {ch.tag: ch.get('Value') for ch in fr}
            c['owner'][k] += 1
            c['RelativePathType'][f"{k}:{v.get('RelativePathType')}"] += 1
            c['Type'][f"{k}:{v.get('Type')}"] += 1
            c['children'][' '.join(ch.tag for ch in fr)] += 1
            c['path_empty'][f"{k}:{v.get('Path') in ('', None)}"] += 1
            c['relpath_prefix'][f"{v.get('RelativePathType')}:{(v.get('RelativePath') or '').split('/')[0][:40]}"] += 1
            c['ext'][os.path.splitext(v.get('Path') or v.get('RelativePath') or '')[1].lower()] += 1
            c['size_crc_nonzero'][f"{v.get('OriginalFileSize') not in ('0', None)}/{v.get('OriginalCrc') not in ('0', None)}"] += 1
            c['livepack'][f"{v.get('RelativePathType')}:{bool(v.get('LivePackName'))}/{bool(v.get('LivePackId'))}"] += 1
            c['path_head'][f"{v.get('RelativePathType')}:{'/'.join((v.get('Path') or '').split('/')[:3])}"] += 1
        for sr in t.iter('SampleRef'):
            v = {ch.tag: ch for ch in sr}
            c['sampleref_children'][' '.join(ch.tag for ch in sr)] += 1
            for n in ('LastModDate', 'DefaultDuration', 'DefaultSampleRate'):
                x = v.get(n); c[n + '_zero'][str(x is not None and x.get('Value') == '0')] += 1
            dsr = v.get('DefaultSampleRate'); c['DefaultSampleRate'][dsr.get('Value') if dsr is not None else None] += 1
            s2 = v.get('SamplesToAutoWarp')
            c['SamplesToAutoWarp'][s2.find('Value').get('Value') if s2 is not None and s2.find('Value') is not None else None] += 1
            suh = v.get('SampleUsageHint')
            c['SampleUsageHint'][suh.find('Value').get('Value') if suh is not None and suh.find('Value') is not None else None] += 1
            sc = v.get('SourceContext')
            c['SourceContext'][' '.join(x.tag for x in sc.iter()) [:120] if sc is not None else None] += 1
out = {'documents': docs}
out.update({k: dict(v.most_common(40)) for k, v in sorted(c.items())})
json.dump(out, sys.stdout, indent=1)
