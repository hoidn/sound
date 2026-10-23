"""Owned packet-only data checks and bounded synthetic TEMP filesystem controls."""
import argparse,hashlib,json,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent
PLAN='a068ff069a909172d0bce22e62392f92bc00a6ee492b94181d9139ab363b6d2a'
def H(b):return hashlib.sha256(b).hexdigest()
def J(n):return json.loads((P/n).read_bytes())
def need(v,n):
 if not v:raise ValueError(n)
def project(b):
 need(len(b)==4,'wholefourbytes')
 return [{'tag':i,'byte_VA':hex(0x2ac4b+i),'raw_byte':v,'branch_base':'0xd47c','branch_address_nomination':hex(0xd47c+v*4),'runtime_target':None,'destination_content_read':False} for i,v in enumerate(b)]
def valid_projection(r,b):need(r==project(b),'projection')
def exactread(f,n):
 b=f.read(n);need(len(b)==n,'exactsyntheticread');return b
def check():
 pb=(P/'input-plan.json').read_bytes();need(H(pb)==PLAN,'frozeninput');plan=json.loads(pb);bf=J('capture/before-identities.json');af=J('capture/after-identities.json');need(bf==plan['pins']==af['files'] and af['unchanged'] and len(bf)==9,'recordedcustody')
 for x in plan['pins']:
  f=Path(x['path'])
  if f.parent==P:
   b=f.read_bytes();need(len(b)==x['bytes'] and H(b)==x['sha256'],'localinputpin')
 table=(P/'capture/dispatch-bytes.bin').read_bytes();word=(P/'capture/producer-word.bin').read_bytes();need(table.hex()=='00101f2e' and word.hex()=='8c3d000000000000','whole12rawbytes')
 ex=J('capture/extraction.json');need(ex['content_bytes']==12 and ex['code_bytes']==0 and ex['reads_per_range']==1,'exactcontentcounts')
 for x,b in zip(ex['ranges'],[table,word]):need(x['bytes']==len(b) and x['sha256']==H(b),'rawrangepins')
 for addr,n,s in [(0x2ac4b,4,plan['H4']['table_geometry']),(0x30120,8,plan['H4']['word_geometry'])]:
  a=int(s['VA'],16);need(a<=addr and addr+n<=a+s['size'] and s['file_offset']+addr-a==addr,'retainedmapping')
 g=J('guard-inputs.json');expected=['e80240b9','1f0d0071','e8feff54','29bf0e70','1f2003d5','8a000010','2b696838','4a090b8b','40011fd6'];need([(r['pc'],r['bytes']) for r in g['guard_rows']]==[(hex(0xd458+4*i),b) for i,b in enumerate(expected)],'nineguardinputs')
 st=J('capture/status.json');o=J('outer-invocation.json');need(st['error'] is None and st['watch_unchanged'] and st['selected_content_bytes_read']==12 and st['children']==st['original_instruction_execution']==0 and st['attempts']==1 and not st['automatic_retry'],'actualsuccess')
 need(o['pid']==st['pid'] and o['exit_code']==0 and not o['timed_out'] and o['started_utc']<=st['started_utc']<=st['finished_utc']<=o['finished_utc'] and (P/'outer.stderr').stat().st_size==0,'outerstatus')
 rows=project(table);need({r['tag'] for r in rows}==set(range(4)),'wholeguards');need([r['branch_address_nomination'] for r in rows]==['0xd47c','0xd4bc','0xd4f8','0xd534'],'allnominations')
 need(int.from_bytes(word,'little')==0x3d8c,'rawinteger')
 neg=[]
 def reject(n,fn,exceptions=(ValueError,)):
  try:fn()
  except exceptions:neg.append(n)
  else:raise AssertionError('accepted:'+n)
 reject('missingguardtag',lambda:project(table[:-1]));reject('unselectedfifthbyte',lambda:project(table+b'\0'))
 bad=json.loads(json.dumps(rows));bad[0]['raw_byte']=1;reject('wrongrawbyte',lambda:valid_projection(bad,table))
 bad=json.loads(json.dumps(rows));bad[1]['branch_address_nomination']=hex(0xd47c+table[1]);reject('missingscale4',lambda:valid_projection(bad,table))
 bad=json.loads(json.dumps(rows));bad[3]['tag']=4;reject('tag4guardexcluded',lambda:valid_projection(bad,table))
 bad=json.loads(json.dumps(rows));bad[0]['branch_base']='0xd480';reject('wrongbranchbase',lambda:valid_projection(bad,table))
 bad=json.loads(json.dumps(rows));bad[0]['runtime_target']=bad[0]['branch_address_nomination'];reject('runtimepromotion',lambda:valid_projection(bad,table))
 bad=json.loads(json.dumps(rows));bad[0]['destination_content_read']=True;reject('destinationfollowpromotion',lambda:valid_projection(bad,table))
 reject('wrongwordendianness',lambda:need(int.from_bytes(word,'big')==0x3d8c,'wordendian'))
 reject('fourentryfirstN',lambda:valid_projection(rows[:2],table))
 with tempfile.TemporaryDirectory(prefix='electric12-peerlike-author-temp-') as temp:
  q=Path(temp);attempt=q/'attempt';attempt.mkdir();reject('TEMPexclusiveattempt',lambda:attempt.mkdir(),(FileExistsError,))
  f=q/'raw';f.write_bytes(b'ABCD');reject('TEMPnooverwrite',lambda:f.open('xb'),(FileExistsError,))
  with f.open('rb') as s:reject('TEMPshortread',lambda:exactread(s,5))
  with f.open('rb') as s:s.seek(4);reject('TEMPrangeoverrun',lambda:exactread(s,1))
 need(len(neg)==14,'negativecount')
 return {'status':'PASS-currentpacketonly-plus-bounded-syntheticTEMP','raw_data_bytes':12,'recorded_custody_pairs':9,'guard_rows':4,'guard_instruction_input_rows':9,'entries':rows,'word':{'VA':'0x30120','raw_hex':word.hex(),'little_endian_raw_integer':'0x3d8c','runtime_pointer_or_target':None},'negative_controls':neg,'data_negative_controls':10,'TEMP_controls':4,'current_external_image_tool_provider_native_reads':0,'newdecoder_original_model_runtime_calls':0,'limits':'Observedguardwindownotmaximallinkertable;arithmeticnominationsnotruntimeidentity;syntheticTEMPcontrolsnotdurability/adversarialfilesystem/failurepathproof.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true',required=True);ap.parse_args();print(json.dumps(check(),indent=2))
