#!/usr/bin/env python3
"""One-time input generation; explicit named custody roles, no original calls or old imports."""
import hashlib,json,pathlib,shutil,sys,platform,os
H=pathlib.Path(__file__).resolve().parent;B=H.parent;OLD=B/'batch-corpus-deterministic-free-lfo-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,offset=None,size=None):
 p=pathlib.Path(p).resolve()
 if offset is None:
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
 with p.open('rb') as f:f.seek(offset);b=f.read(size)
 assert len(b)==size;return {'path':str(p),'offset':offset,'bytes':size,'sha256':sha(b),'role':'selected slice hash custody only'}
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert not (H/'inputs.json').exists()
report=B/'reviews/corpus-deterministic-free-lfo-v1-partial-review.json';rp=pin(report);assert rp['bytes']==33471 and rp['sha256']=='009f25f09172e6741c6927711d1ea2adc21194a38fddc942ec04ec0f44778df1';review=json.loads(report.read_text());assert review['disposition']=='APPROVED_ONE_FINITE_SQUARE_OBSERVATION_WITH_FROZEN_BOOKKEEPING_FAILURE_TWO_MEMBERS_UNLAUNCHED'
meta=json.loads((OLD/'manifest.json').read_text());assert pin(OLD/'manifest.json')['sha256']=='91a49deb9b77691d06a45332a42478fa66c909db6c9679cbe6b9b8c686f8f679'
def oldfile(name):
 p=OLD/name;expected=next(x for x in meta['files'] if x['path']==name);actual=pin(p);assert actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256'];return p
old=json.loads(oldfile('inputs.json').read_text());oldctx=json.loads(oldfile('context.json').read_text());d=json.loads(json.dumps(old));d['counts']={'logical':5,'inherited_no_replay':3,'fresh_children':2,'direct_exports':146,'CalcA':64};d['plans']=[p for p in d['plans'] if p['shape'] in (2,4)];(H/'scripts').mkdir();(H/'protocol').mkdir()
shutil.copyfile(oldfile('input.f32'),H/'input.f32')
for p in d['plans']:
 oldscript=oldfile(f'scripts/shape-{p["shape"]}.script');new=H/'scripts'/oldscript.name;shutil.copyfile(oldscript,new);p['script']=str(new)
for r,q in zip(d['catalog'],review['approved_summary']['approved_points']):
 assert r['shape']==q['shape'] and r['parameter_bits32']==q['parameter_bits32']
 if r['shape'] in (0,1,3):
  output=q.get('output') or {'bytes':q['historical']['output_bytes'],'sha256':q['historical']['output_sha256']}
  r['provenance']='inherited-approved-no-replay';r['historical']={'review_sha256':rp['sha256'],'review_pointer':f'/approved_summary/approved_points/{r["shape"]}','approved_point_sha256':sha(json.dumps(q,sort_keys=True,separators=(',',':')).encode()),'output':output,'new_pid':None,'new_receipt':None,'scope':'Approved prior only, no old actual audio/raw/source reopening or retry'}
 else:assert q['disposition']=='NEVER_LAUNCHED_UNRESOLVED' and q['output'] is None;r['historical']=None;r['provenance']='fresh-selected'
save('inputs.json',d);save('approved-prior-summary.json',review['approved_summary']);save('prior-review-pin.json',rp)
for name in ['xdev.h','xdev.c','xdev_bind.c']:shutil.copyfile(oldfile('protocol/'+name),H/'protocol'/name)
# Explicit9 named roles; assertions use role lookup, never list tail position.
roles=[]
for name,item in zip(['loader','universal_bundle','python','libc','libm','libstdcxx','elf_interpreter','selected_x86_slice','source_I1_input'],oldctx['watched']):
 actual=pin(item['path'],item.get('offset'),item['bytes'] if 'offset' in item else None);assert actual==item
 roles.append({'role':name,'identity':actual})
assert len(roles)==9 and len({r['role'] for r in roles})==9
byrole={r['role']:r['identity'] for r in roles}
assert byrole['selected_x86_slice']['sha256']=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
assert byrole['source_I1_input']['sha256']=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6'
ctx={k:v for k,v in oldctx.items() if k!='watched'};ctx['watched_roles']=roles;ctx['host']={'uname':list(platform.uname()),'python':sys.version,'byteorder':sys.byteorder};ctx['continuation']='ONLY prior never-launched2/4; rate return parsedopaque signedinteger, no0/1 semanticoracle. OldSquare NEVERreplayed. Unusedprepare branch removed fromnewrecorder; this generator builds whole9rolecontext inonepass without manualcontext edits.';save('context.json',ctx)
save('authority-pins.json',{'partial_manifest':pin(OLD/'manifest.json'),'partial_review':rp,'unchanged_method_source_pins':json.loads(oldfile('authority-pins.json').read_text()),'input_metadata':pin(OLD/'inputs.json'),'oldcode_context':pin(OLD/'record.py'),'no_old_audio_raw_reads':True})
print(json.dumps({'generated_once':True,'new_shapes':[p['shape'] for p in d['plans']],'roles':[r['role'] for r in roles],'original_calls':0,'old_actual_audio_raw_reads':0}))
