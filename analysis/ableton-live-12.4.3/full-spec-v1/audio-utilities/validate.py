"""Bounded source/fixture/doc checks; no target application or original code runs."""
from pathlib import Path
import hashlib,json,gzip,re,xml.etree.ElementTree as ET,py_compile
P=Path(__file__).resolve().parent
R=P.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.load(open(P/'sources.json'))
assert len(sources)==24
for s in sources:
 p=P/s['path'];assert p.stat().st_size==s['bytes'];assert sha(p)==s['sha256']
 if 'source_path' in s:assert sha(Path(s['source_path']))==s['sha256']
html=(P/'manual-audio-effects-2026-10-19.html').read_text()
for dev,count in [('utility',14),('tuner',21),('spectrum',11)]:
 blocks=json.load(open(P/f'manual-{dev}-blocks.json'));assert len(blocks)==count
 for i,b in enumerate(blocks,1):
  assert b['locator']==f'{dev}:B{i:02d}'
  assert b['device']==dev and b['html_line']<=len(html.splitlines())
  if b['anchor']:assert f'id="{b["anchor"]}"' in html.splitlines()[b['html_line']-1]
values=json.load(open(P/'package-values.json'));assert len(values)==22
xml={}
for v in values:
 root=ET.fromstring(gzip.decompress((P/v['source']).read_bytes()))
 tag={'Utility':'StereoGain','Tuner':'Tuner','Spectrum':'SpectrumAnalyzer'}[v['device']]
 e=list(root.iter(tag));assert len(e)==1;xml[Path(v['source']).name]=e[0]
 assert root.attrib['Creator']=='Ableton Live 12.4d1'
 assert root.attrib['MinorVersion']=='12.0_12402'
def val(name,path):return xml[name].find(path).attrib['Value']
# These assert the six file-only cases against original retained XML, not case JSON.
assert [val('Bass Mono.adv',x) for x in ['BassMono/Manual','BassMonoFrequency/Manual','Gain/Manual','LegacyMode']]==['true','120','1','false']
assert [val('Phase Invert.adv',x) for x in ['PhaseInvertL/Manual','PhaseInvertR/Manual']]==['true','true']
assert val('Left.adv','ChannelMode/Manual')=='0' and val('Right.adv','ChannelMode/Manual')=='2'
assert [val('Guitar Recording.als',x) for x in ['TuningFreq/Manual','ViewMode','StrobeMode','DisplayPitchInHz','HistogramFollowsPitch','IgnoreTuningSystem']]==['440','0','false','false','true','false']
assert [val('Accurate Fast.adv',x) for x in ['Length','Window','ChannelMode','NumAverages','MinRefreshTime']]==['3','3','2','3','40']
assert [val('Spectrum.adv',x) for x in ['Length','Window','NumAverages','MinRefreshTime','ScaleXMode']]==['2','3','1','100','1']
counts={};case_ids=set();req_ids=set();seen=set()
for dev,nr,nc in [('utility',15,37),('tuner',12,32),('spectrum',14,34)]:
 d=json.load(open(P/f'{dev}-cases.json'));assert len(d['requirements'])==nr and len(d['cases'])==nc
 ids={x['id'] for x in d['requirements']};assert len(ids)==nr;assert not ids&req_ids;req_ids|=ids
 doc=(R/f'wiki/specs/device-{dev}.md').read_text()
 for rid in ids:assert len(re.findall(r'^### '+rid+r' —',doc,re.M))==1
 for c in d['cases']:
  assert c['id'] not in case_ids;case_ids.add(c['id'])
  assert c['requirements'] and set(c['requirements'])<=ids;seen.update(c['requirements'])
  assert c['execution']=='unexecuted' and c['id'] in doc
  assert (c['expected'] is None)==(c['provenance']=='U')
  if c['provenance']=='D12':assert c['target_grade']=='U'
 counts[dev]={k:sum(c['provenance']==k for c in d['cases']) for k in ['D12','Dpkg','U']}
 assert all(any(c['kind']==kind for c in d['cases']) for kind in ['positive','boundary','negative','cancel','undo','persistence','teardown'])
assert seen==req_ids
pages=[R/'wiki/research/device-audio-utilities.md']+[R/f'wiki/specs/device-{x}.md' for x in ['utility','tuner','spectrum']]
for page in pages:
 text=page.read_text()
 for key in ['id','type','status','updated','access']:assert re.search(r'^'+key+r':',text,re.M)
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if target.startswith(('http:','https:','#')):continue
  raw,_,anchor=target.partition('#');dest=(page.parent/raw).resolve();assert dest.exists(),(page,target)
  if anchor:assert anchor=='analysis-only-evidence' and '## Analysis-only evidence' in text,(page,target)
for f in ['capture.py','validate.py']:compile((P/f).read_text(),str(P/f),'exec')
print(json.dumps({'status':'pass','source_hashes':24,'package_xml':22,'file_only_cases':6,'requirements':41,'cases':103,'counts':counts,'runtime_cases_executed':0,'document_links':'resolve','figures_inspected':False,'target_compatibility':'unknown'},indent=2))
