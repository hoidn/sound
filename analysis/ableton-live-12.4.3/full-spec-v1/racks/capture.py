"""Bounded read-only rack/manual evidence capture; no original code execution."""
from pathlib import Path
import datetime, gzip, hashlib, json, urllib.request, xml.etree.ElementTree as ET
from html.parser import HTMLParser

OUT = Path(__file__).resolve().parent
APP = Path('/home/ollie/Ableton Live 12 Suite.app')
SCHEMA = APP / 'Contents/App-Resources/Schema/12.0_12402.txt'
RACKS = ['AudioEffectGroupDevice', 'MidiEffectGroupDevice', 'InstrumentGroupDevice', 'DrumGroupDevice']
def sha(data): return hashlib.sha256(data).hexdigest()
def write(name, obj): (OUT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.on = False; self.depth = 0; self.skip = 0; self.bits = []; self.headings = []; self.heading = None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='h1': self.on=True
        if not self.on: return
        if tag in ['script','style']: self.skip += 1
        if tag in ['p','li','h1','h2','h3','h4','h5']: self.bits.append('\n')
        if tag in ['h1','h2','h3','h4','h5']:
            self.heading={'level':tag,'id':a.get('id'),'html_line':self.getpos()[0],'text':''}
            self.headings.append(self.heading)
    def handle_endtag(self, tag):
        if tag in ['script','style']: self.skip=max(0,self.skip-1)
        if tag in ['h1','h2','h3','h4','h5']: self.heading=None
        if tag in ['p','li','h1','h2','h3','h4','h5']: self.bits.append('\n')
    def handle_data(self, data):
        if self.on and not self.skip:
            self.bits.append(data)
            if self.heading is not None: self.heading['text'] += data
prior_sources=json.loads((OUT/'sources.json').read_text()) if (OUT/'sources.json').exists() else []
sources=[]
for slug,short in [('instrument-drum-and-effect-racks','racks'),('working-with-instruments-and-effects','devices')]:
    url=f'https://www.ableton.com/en/live-manual/12/{slug}/'
    name=f'manual-{short}-2026-10-19.html'
    if (OUT/name).exists():
        data=(OUT/name).read_bytes(); final=url
    else:
        with urllib.request.urlopen(url) as r: data=r.read(); final=r.url
        (OUT/name).write_bytes(data)
    p=Text(); p.feed(data.decode())
    text='\n'.join(' '.join(line.split()) for line in ''.join(p.bits).splitlines() if line.strip())
    # Main article ends before the global manual navigation.
    text=text.split('\nAbleton Reference Manual')[0]
    (OUT/f'manual-{short}.txt').write_text(text+'\n')
    write(f'manual-{short}-headings.json',p.headings)
    prior=next((s for s in prior_sources if s.get('file')==name),None)
    sources.append(prior or {'id':'RACKS-MAN-'+short.upper(),'url':url,'final_url':final,'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':name,'bytes':len(data),'sha256':sha(data),'version':'Live 12, exact 12.4.3 parity unknown'})
schema_bytes=SCHEMA.read_bytes(); schema=ET.fromstring(schema_bytes); lines=schema_bytes.decode().splitlines()
names=RACKS+['AudioEffectBranch','MidiEffectBranch','InstrumentBranch','DrumBranch','ZoneRange','ZoneSettings','DrumZoneSettings','MacroVariations','MacroVariation','MacroSnapshot','MacroSnapshotList','DrumBranchMixerDevice']
rows={}
for node in schema:
    if node.tag in names or node.tag.startswith('Macro'):
        rows[node.tag]={'line':next(i+1 for i,line in enumerate(lines) if line.strip()==f'<{node.tag}>'),'fields':[{'name':c.tag,**c.attrib} for c in node]}
assert set(RACKS+['ZoneRange','MacroVariations']) <= rows.keys()
assert all(len([c for c in rows[t]['fields'] if c['name'].startswith('MacroControls.')])==16 for t in RACKS)
write('schema-fields.json',{'source':str(SCHEMA),'sha256':sha(schema_bytes),'classes':rows})
sources.append({'id':'RACKS-SCHEMA','path':str(SCHEMA),'sha256':sha(schema_bytes),'bytes':len(schema_bytes),'version':'12.0_12402 installed with 12.4.3'})
# One exact shipped Suite demo, retaining relevant rack subtrees as XML evidence.
demo=APP/'Contents/App-Resources/Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als'
data=demo.read_bytes(); root=ET.fromstring(gzip.decompress(data)); records=[]; counts={t:0 for t in RACKS}
for t in RACKS:
    for index,node in enumerate(root.iter(t)):
        counts[t]+=1
        fields={c.tag:c.attrib for c in node if c.tag.startswith(('Macro','ExcludeMacro')) or c.tag in ['NumVisibleMacroControls','ChainSelector','On']}
        branches=[]
        for branch in node.findall('./Branches/*')+node.findall('./ReturnBranches/*'):
            branches.append({'type':branch.tag,'attributes':branch.attrib,'fields':{c.tag:ET.tostring(c,encoding='unicode') for c in branch if c.tag in ['ReceivingNote','SendingNote','ChokeGroup','KeyRange','VelocityRange','BranchSelectorRange','ZoneSettings','BranchInfo','DrumZoneSettings','DeviceChain','MixerDevice']}})
        records.append({'class':t,'ordinal':index,'locator':f'(.//{t})[{index+1}]','attributes':node.attrib,'fields':fields,'branches':branches,'variations':ET.tostring(node.find('MacroVariations'),encoding='unicode') if node.find('MacroVariations') is not None else None})
assert all(counts.values()),counts
write('shipped-racks.json',{'source':str(demo),'sha256':sha(data),'bytes':len(data),'creator':root.attrib,'counts':counts,'racks':records})
sources.append({'id':'RACKS-DEMO','path':str(demo),'sha256':sha(data),'bytes':len(data),'version':root.attrib})
# Retained native export inventory only, no execution or behavioral inference.
strings=Path('/var/tmp/sound-analysis/corpus/indexes/strings.jsonl'); wanted={'ChainSelector','MacroVariations','ChokeGroup','DrumBranch','NumVisibleMacroControls','ExcludeMacroFromRandomization','BranchSelectorRange','ZoneRange'}; found=[]
with strings.open('rb') as f:
    for n,line in enumerate(f,1):
        r=json.loads(line)
        if r.get('value') in wanted: found.append({'line':n,'line_sha256':sha(line),'record':r})
assert found
write('native-strings.json',{'source':str(strings),'sha256':sha(strings.read_bytes()),'rows':found,'limit':'names/references establish presence only'})
sources.append({'id':'RACKS-NATIVE-STRINGS','path':str(strings),'sha256':sha(strings.read_bytes()),'bytes':strings.stat().st_size,'version':'retained 12.4.3 arm64 export'})
# The shipped slicing default was selected by a bounded ADG search for snapshots.
variation=APP/'Contents/App-Resources/Core Library/Defaults/Slicing/Default.adg'
vbytes=variation.read_bytes(); vroot=ET.fromstring(gzip.decompress(vbytes)); snapshots=vroot.findall('.//MacroSnapshot')
assert len(snapshots)==5
if (OUT/'variation-example.adg').exists():
    assert (OUT/'variation-example.adg').read_bytes()==vbytes
else:
    (OUT/'variation-example.adg').write_bytes(vbytes)
write('variation-example.json',{'source':str(variation),'sha256':sha(vbytes),'bytes':len(vbytes),'creator':vroot.attrib,'count':len(snapshots),'snapshots':[ET.tostring(s,encoding='unicode') for s in snapshots]})
sources.append({'id':'RACKS-VARIATION-EXAMPLE','path':str(variation),'sha256':sha(vbytes),'bytes':len(vbytes),'version':vroot.attrib,'retained':'variation-example.adg'})
write('sources.json',sources)
write('summary.json',{'rack_types':len(RACKS),'schema_classes':len(rows),'shipped_racks':counts,'native_strings':len(found),'original_code_executed':False})
print(json.dumps({'counts':counts,'schema_classes':len(rows),'native_strings':len(found)}))
