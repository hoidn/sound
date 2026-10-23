"""Owned data-only check; no original/helper execution, external image/tool/provider or old WAV opens."""
from pathlib import Path
import json,hashlib,struct,math,sys,copy
P=Path(__file__).resolve().parent
J=lambda n:json.loads((P/n).read_bytes());H=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def rawok(raw):
 need(len(raw)==352800,'shape');v=struct.unpack('<88200f',raw);need(all(math.isfinite(x)for x in v),'finite-both-channels')
def main():
 plan=J('pre-call-manifest.json');jobs=J('jobs.json');settings=J('settings.json');status=J('actual/status.json');obs=J('observations.json')
 need(len(jobs)==222 and len(settings)==37 and len(obs['settings'])==37,'whole-class')
 need(status['error']is None and status['attempted']==status['completed']==222 and len(status['results'])==222,'complete-once')
 need(J('actual/before-identities.json')==plan['pins']==J('actual/after-identities.json'),'recorded-global-custody')
 for pin in plan['pins']:
  f=Path(pin['path'])
  if f.is_relative_to(P):
   b=f.read_bytes();need(len(b)==pin['bytes'] and H(b)==pin['sha256'],'owned-frozen-input')
 settingsmap={s['name']:s for s in settings}
 for i,j in enumerate(jobs):
  need(j['ordinal']==i and j['variant']==['baseline','libm+1','libm-1','round_down','round_up','round_zero'][i%6],'planned-order')
  b=(P/j['script']).read_bytes();need(len(b)==j['script_bytes']and H(b)==j['script_sha256'],'exact-input')
  ps=[l.split()for l in b.decode().splitlines()if l.startswith('param ')];need([int(l[1])for l in ps]==[n for n in range(130)if n!=2],'129ordered-setters')
  need([{'index':int(l[1]),'token':l[2],'binary32_le':struct.pack('<f',float(l[2])).hex()}for l in ps]==settingsmap[j['name']]['parameter_words'],'full-129words')
  d=P/'actual'/j['key'];r=json.loads((d/'result.json').read_bytes());raw=(d/'output.f32').read_bytes();rawok(raw)
  need(r['error']is None and r['attempt']==1 and not r['timed_out']and r['exit_code']==0 and r['custody_unchanged'],'child-status')
  need(r['protocol']['direct_export_calls']==219 and r['protocol']['CalcA_calls']==87,'bounded-calls')
  need(json.loads((d/'before-identities.json').read_bytes())==json.loads((d/'after-identities.json').read_bytes())==plan['runtime_pins'],'child-custody')
  for n in ['stdout','stderr','output.f32']:
   b=(d/n).read_bytes();ident=r[n.replace('.','_')+'_identity'];need(len(b)==ident['bytes']and H(b)==ident['sha256'],'retained-result-identity')
 for s in obs['settings']:need(len(s['variants'])==5 and len(s['fresh_baseline_vs_old'])==2 and all(len(v['channels'])==2 for v in s['variants']),'complete-metric-representation')
 negatives=[]
 def reject(n,f):
  try:f()
  except ValueError:negatives.append(n);return
  raise AssertionError(n)
 reject('short-output',lambda:rawok(bytes(352796)));bad=bytearray(352800);bad[4:8]=(0x7fc00000).to_bytes(4,'little');reject('right-channel-NaN',lambda:rawok(bytes(bad)));bad[4:8]=bytes(4);bad[0:4]=(0x7f800000).to_bytes(4,'little');reject('left-channel-Infinity',lambda:rawok(bytes(bad)))
 reject('missing-setting',lambda:need(len(settings[:-1])==37,'whole37'));reject('missing-perturbation',lambda:need(len(jobs[:-1])==222,'whole222'));reject('invented-ARM-bound',lambda:need('No new tolerances'not in obs['limits'],'no-ARM-promotion'))
 if(P/'manifest.json').exists():
  m=J('manifest.json');need({str(f.relative_to(P))for f in P.rglob('*')if f.is_file()and f.name!='manifest.json'}=={x['path']for x in m['files']},'exactsealedtree')
  for x in m['files']:
   b=(P/x['path']).read_bytes();need(len(b)==x['bytes']and H(b)==x['sha256'],'sealedpayload')
 print(json.dumps({'status':'PASS-owned-data-only','children':222,'settings':37,'directexports':48618,'CalcA':19314,'raw_bytes':78321600,'both_channels_finite':True,'negative_controls':negatives,'original_or_helper_calls':0,'external_reopens':0},indent=2))
if __name__=='__main__':need(sys.argv[1:]==['--check'],'only-check');main()
