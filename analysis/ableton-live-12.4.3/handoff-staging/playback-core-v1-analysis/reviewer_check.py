import copy, json, math, gzip, hashlib, re, struct, wave, sys, subprocess, tempfile, shutil
from fractions import Fraction as Q
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path('/home/ollie/Documents/sound')
P=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'analysis/ableton-live-12.4.3/handoff-staging/playback-core-v1'
D=3843840
f32=lambda x: struct.unpack('<f',struct.pack('<f',float(x)))[0]
def L(x):
 s=-1 if x<0 else 1
 return s*math.floor(abs(x+s*(1/D)/2)*D)/D

def place(b,an,sr,t):
 n,a=an
 b=L(b)
 exact=(Q(round(b*D),D)-Q(a))*sr*60/Q(t)
 n0=math.ceil(exact)
 return [n+n0,n+n0+1] if exact.denominator==1 and (b-a)*((sr/t)*60)>exact else [n+n0]

def value(el,path): return el.find(path).get('Value')
def num(el,path): return float(value(el,path))
def yes(el,path): return value(el,path)=='true'

def calculate(c):
 x=ET.fromstring(gzip.decompress((P/c['input']).read_bytes())).find('LiveSet')
 assert len(x.find('Tracks'))==len(x.find('Scenes'))==1
 tr=x.find('Tracks')[0]
 seq=tr.find('DeviceChain/MainSequencer/ClipSlotList')
 assert len(seq)==len(tr.find('DeviceChain/FreezeSequencer/ClipSlotList'))==1
 clip=seq[0].find('ClipSlot/Value')[0]
 t=f32(num(x,'MainTrack/DeviceChain/Mixer/Tempo/Manual')); sr=c['sample_rate']; spb=(sr/t)*60
 for field,kind in [('Tempo','FloatEvent'),('TimeSignature','EnumEvent')]:
  mix=x.find('MainTrack/DeviceChain/Mixer/'+field)
  key=mix.find('AutomationTarget').get('Id')
  env=next(e for e in x.findall('MainTrack/AutomationEnvelopes/Envelopes/AutomationEnvelope') if value(e,'EnvelopeTarget/PointeeId')==key)
  ev=env.find('Automation/Events'); assert len(ev)==1 and ev[0].tag==kind
  assert ev[0].get('Value')==value(mix,'Manual')
 song_s=num(x,'Transport/LoopStart'); song_e=L(song_s+max(1,num(x,'Transport/LoopLength')))
 loop=yes(x,'Transport/LoopOn'); an=(0,0); held=0; playing=False; jumps=[]; loop_ok=False
 def advance(n):
  nonlocal an
  while loop_ok and place(song_e,an,sr,t)[0]<=n:
   j=place(song_e,an,sr,t); assert len(j)==1
   an=(j[0],song_s); jumps.append(j[0])
 launch=None
 for action in c['script']:
  n=action['at']; advance(n)
  if action['action']=='play':
   an=(n,max(0,L(action['start_beat']))); playing=True; loop_ok=loop and an[1]<song_e
  elif action['action']=='stop': held=an[1]+(n-an[0])*(1/spb); playing=False
  elif action['action']=='continue': an=(n,held); playing=True
  elif action['action']=='launch':
   assert launch is None
   if not playing:
    an=(n,max(0,L(action['start_beat']))); playing=True; loop_ok=loop and an[1]<song_e
   press=L(an[1]+(n-an[0])*(1/spb))
   k=int(num(clip,'LaunchQuantisation'))
   if k==0:
    k=int(num(x,'GlobalQuantisation')); meter=int(num(x,'MainTrack/DeviceChain/Mixer/TimeSignature/Manual'))
    nn,dd={200:(3,4),201:(4,4),202:(5,4),302:(6,8),303:(7,8)}[meter]
   else:
    k-=1; sig=clip.find('TimeSignature/TimeSignatures')[0]; nn=num(sig,'Numerator'); dd=num(sig,'Denominator')
   grids={0:0,1:8*L(4*nn/dd),2:4*L(4*nn/dd),3:2*L(4*nn/dd),4:L(4*nn/dd),5:2,6:4/3,7:1,8:2/3,9:.5,10:1/3,11:.25,12:1/6,13:.125}
   g=grids[k]; B=L(math.ceil(press/g)*g) if g else press
   launch=(B,an,len(jumps))
   assert c['informative']['press_beat']==press,(c['id'],'press')
   if 'grid_beats' in c['informative']: assert c['informative']['grid_beats']==g
   assert c['informative']['launch_boundary_beat']==B
 assert launch is not None
 B,base_an,prior_jumps=launch
 if 'midi' in c['expected']:
  end=c['expected']['midi']['window'][1]
  # Generate in the song-time coordinates at launch, then shift by every intervening jump.
  S=L(num(clip,'Loop/LoopStart')+num(clip,'Loop/StartRelative')); ls=num(clip,'Loop/LoopStart'); le=num(clip,'Loop/LoopEnd'); repeat=yes(clip,'Loop/LoopOn')
  keytrack=clip.find('Notes/KeyTracks')[0]; key=int(num(keytrack,'MidiKey')); notes=keytrack.find('Notes')
  events=[]; passes=0; pstart=B; cstart=S
  def event(b,kind,v):
   a=base_an; shifted=b
   if loop_ok:
    while shifted>=song_e:
     js=place(song_e,a,sr,t); assert len(js)==1
     a=(js[0],song_s); shifted=L(shifted-(song_e-song_s))
   positions=place(shifted,a,sr,t)
   if positions[0]<end:
    assert positions[-1]<end,'window ends inside allowed-sample alternative'
    events.append((b,0 if kind=='note-off' else 2,{'samples':positions,'type':kind,'key':key,'velocity':f32(v)}))
  while place(pstart,base_an,sr,t)[0]<end and passes<100:
   pend=L(pstart+le-cstart)
   for nt in notes:
    ti=float(nt.get('Time')); dur=float(nt.get('Duration'))
    if nt.get('IsEnabled')!='true' or ti<cstart or ti>=le: continue
    on=L(pstart-cstart+ti); off_clip=L(ti+dur)
    if dur==0: off_clip=L(ti+1/D)
    off=L(pstart-cstart+min(off_clip,le))
    event(on,'note-on',float(nt.get('Velocity')))
    event(off,'note-off',64 if off_clip>le else float(nt.get('OffVelocity')))
   if not repeat: break
   pstart=pend; cstart=ls; passes+=1
  result=[e for _,_,e in sorted(events,key=lambda z:(z[0],z[1]))]
  assert result==c['expected']['midi']['events'],(c['id'],'midi mismatch',next(((a,b) for a,b in zip(result,c['expected']['midi']['events']) if a!=b),None),len(result),len(c['expected']['midi']['events']))
  return len(result),0
 path=(P/c['input']).parent/value(clip,'SampleRef/FileRef/RelativePath')
 with wave.open(str(path)) as w:
  assert w.getnchannels()==1 and w.getsampwidth()==2
  rate=w.getframerate(); frames=[v[0]/32768 for v in struct.iter_unpack('<h',w.readframes(w.getnframes()))]
 launchsample=place(B,base_an,sr,t); assert len(launchsample)==1
 incs=json.loads((ROOT/'analysis/ableton-live-12.4.3/r2/t13-playback-v1/audio/results/inc.json').read_text())
 semis=num(clip,'PitchCoarse')
 F=next(v['fixed_32_32'] for v in incs if v['file_rate']==rate and v['engine_rate']==sr and v['semitones']==semis)
 assert F==c['informative']['read_step_fixed_32_32']
 gains=json.loads((ROOT/'analysis/ableton-live-12.4.3/r2/t13-playback-v1/audio/results/gain.json').read_text())['rows']
 gain=next(float(r['engine_gain']) for r in gains if float(r['sample_volume'])==num(clip,'SampleVolume'))
 first=int(rate*num(clip,'Loop/LoopStart')); assert first==c['informative']['first_frame']; assert gain==c['informative']['gain']
 count=0
 for window in c['expected']['audio']['windows']:
  for offset,expected in enumerate(window['values']):
   n=window['from']+offset-launchsample[0]
   pos=first*2**32+n*F; i,r=divmod(pos,2**32)
   if n<0 or i>=len(frames): out=0
   elif F==2**32: out=frames[i]
   else:
    assert i+1<len(frames)
    f=f32(r/2**32); out=f32(f32(f32(1-f)*frames[i])+f32(f*frames[i+1]))
   out=f32(out*gain)
   assert out==expected,(c['id'],'audio value',offset,out,expected)
   count+=1
 return 0,count

def mechanical():
 sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
 manifest=json.loads((P/'manifest.json').read_text())
 files={str(p.relative_to(P)):p for p in P.rglob('*') if p.is_file() and p.name!='manifest.json'}
 assert set(files)=={v['path'] for v in manifest['files']}
 for entry in manifest['files']:
  p=files[entry['path']]; assert sha(p)==entry['sha256'] and p.stat().st_size==entry['bytes']
 assert not any(p.is_symlink() for p in P.rglob('*'))
 links=0; scans=0
 patterns=[r'(?:analysis|raw|wiki)/',r'0x[0-9a-fA-F]{4,}',r'FUN_|_ZN|::',r'/home/|/var/|/tmp/',r'PBC-|CLC-|Q-0|ev_[0-9a-f]',r'disassembl|decompil|pseudocode|Ghidra|vtable|harness|xexec|powf|exp10f|fmadd|fcvtps']
 for p in [*files.values(),P/'manifest.json']:
  if p.suffix=='.wav': continue
  text=gzip.decompress(p.read_bytes()).decode() if p.suffix=='.als' else p.read_text()
  for pat in patterns:
   hits=re.findall(pat,text)
   if p.name=='AGENTS.md': hits=[h for h in hits if h!='decompil']
   assert not hits,(p.name,pat,hits)
  scans+=1
  if p.suffix=='.md':
   for link in re.findall(r'\]\(([^)\s]+)\)',text):
    target,_,anchor=link.partition('#'); dest=(p.parent/target).resolve() if target else p.resolve()
    assert P.resolve() in dest.parents and dest.is_file(),(p.name,link)
    if anchor:
     headings={re.sub(r'[^\w\- ]','',h.strip().lower()).replace(' ','-') for h in re.findall(r'^#+ (.+)$',dest.read_text(),re.M)}
     assert anchor in headings,(p.name,link)
    links+=1
 schema_path=Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Schema/12.0_12402.txt')
 schema={c.tag:{f.tag:(f.get('Class'),f.get('Type')) for f in c} for c in ET.parse(schema_path).getroot()}
 def shape(el,cls):
  assert cls in schema,('unknown class',cls)
  fields=schema[cls]; tags=[c.tag for c in el]; assert len(tags)==len(set(tags)),('duplicate member',cls)
  for child in el:
   assert child.tag in fields,(cls,child.tag)
   target,typ=fields[child.tag]
   if typ=='-4': assert 'Value' in child.attrib,(cls,child.tag,'missing Value')
   elif typ=='0': shape(child,target)
   elif typ=='-1':
    for item in child: shape(item,item.tag)
 for p in (P/'fixtures').glob('*.als'):
  shape(ET.fromstring(gzip.decompress(p.read_bytes())).find('LiveSet'),'LiveSet')
 # The schema walker intentionally treats lists separately; repeated list classes are permitted.
 signals={}
 for name,rate,n,period,seed in [('tone48.wav',48000,480,96,7),('tone44.wav',44100,441,90,11)]:
  p=P/'fixtures/Samples'/name; raw=p.read_bytes(); chunks=[]; off=12
  while off<len(raw):
   size=int.from_bytes(raw[off+4:off+8],'little'); chunks.append(raw[off:off+4].decode()); off+=8+size+(size%2)
  assert chunks==['fmt ','data'] and off==len(raw)
  with wave.open(str(p)) as w:
   assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,rate,n)
   actual=[v[0] for v in struct.iter_unpack('<h',w.readframes(n))]
  expected=[]; state=seed
  for i in range(n):
   state=(1103515245*state+12345)%2**31
   expected.append(max(-32768,min(32767,(i%period)*24000//period-12000+(state>>16)%4001-2000)))
  assert expected==actual; signals[name]={'frames':n,'sha256':sha(p),'chunks':chunks}
 t13=ROOT/'analysis/ableton-live-12.4.3/r2/t13-playback-v1'; sources=json.loads((t13/'manifest.json').read_text())
 for f,h in sources['files'].items(): assert sha(t13/f)==h,('evidence hash',f)
 images={}
 for name,v in sources['slices'].items():
  assert sha(Path(v['path']))==v['sha256']; images[name]=v['sha256']
 x2=ROOT/'analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/results/launch.json'
 assert sha(x2)=='b2ef10311f9c6348cb5c865cf00a9b6b85714b545520a0f48689b2abcdcd621e'
 t11=ROOT/'analysis/ableton-live-12.4.3/r2/t11-structure-v1'
 rows=[json.loads(line) for line in subprocess.check_output([sys.executable,'-I','-B',str(t11/'schema_check.py'),str(schema_path),*map(str,(P/'fixtures').glob('*.als'))],text=True).splitlines()]
 assert len(rows)==58 and not any(r.get('error') or r['deviations'] for r in rows)
 with tempfile.TemporaryDirectory(prefix='playback-review-export-') as tmp:
  export=Path(tmp)/'playback-core-v1'; shutil.copytree(P,export)
  for p in P.rglob('*'):
   if p.is_file(): assert p.read_bytes()==(export/p.relative_to(P)).read_bytes()
  audit=Path(tmp)/'audit.json'
  subprocess.check_call([sys.executable,'-I','-B',str(t11/'fixture_audit.py'),str(schema_path),tmp,str(audit)],stdout=subprocess.DEVNULL)
  summary=json.loads(audit.read_text())['releases'][0]['summary']
  assert summary['refused']==summary['with_unknown_shapes']==0
  assert not summary['cases_contradicted'] and not summary['cases_not_isolating']
  subprocess.check_call([sys.executable,'-I','-B',str(Path(__file__).resolve()),str(export),'expectations-only'],stdout=subprocess.DEVNULL)
 return {'manifest_sha256':sha(P/'manifest.json'),'payload_files':len(files),'markdown_links':links,'files_sanitizer_scanned':scans,'schema_documents':len(rows),'fixture_audit':summary,'independent_shape_check':'58 sets: no repeated member, missing base Value or unknown list class','generated_signals':signals,'t13_artifacts':len(sources['files']),'t13_manifest_sha256':sha(t13/'manifest.json'),'pinned_images':images,'x2_launch_sha256':sha(x2),'schema_sha256':sha(schema_path),'export':'byte-identical temporary copy; all 92 expectations checked again there'}

def main():
 data=json.loads((P/'cases.json').read_text()); n=0; samples=0
 for c in data['cases']:
  a,b=calculate(c); n+=a; samples+=b
 mutations=0
 for c in data['cases']:
  bad=copy.deepcopy(c)
  if 'midi' in bad['expected']: bad['expected']['midi']['events'][0]['velocity']+=1
  else: bad['expected']['audio']['windows'][1]['values'][0]+=1
  try: calculate(bad)
  except AssertionError: mutations+=1
  else: raise AssertionError(('missed mutation',c['id']))
 report=mechanical() if len(sys.argv)<3 else {}
 print(json.dumps({**report,'mutated_expectations_detected':mutations,'cases':len(data['cases']),'midi_cases':sum('midi' in c['expected'] for c in data['cases']),'midi_events':n,'audio_cases':10,'audio_values':samples,'outcome':'all expectations independently recomputed from fixture inputs and contract; audio step/gain taken from retained extracted results'}))
if __name__=='__main__': main()
