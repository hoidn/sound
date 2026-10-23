"""Owner wording/mapping/preservation only. No raw/metric/original execution or corpus reads."""
from pathlib import Path
import json,hashlib,re,sys,copy
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
J=lambda n:json.loads((P/n).read_bytes());H=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def block_pins(text):
 out={}
 for m in re.finditer(r'^### (REQ-DEVICE-TENSION-\d{3})[^\n]*\n',text,re.M):
  end=re.search(r'^#{2,3} ',text[m.end():],re.M);b=(text[m.start():m.end()+end.start()]if end else text[m.start():]).encode();out[m.group(1)]={'bytes':len(b),'sha256':H(b)}
 return out
def row_pins(text):
 out={}
 for line in text.splitlines(keepends=True):
  m=re.match(r'\| (DTN-\d{3}) \|',line)
  if m:b=line.encode();out[m.group(1)]={'bytes':len(b),'sha256':H(b)}
 return out
def mapping(a,before):
 rows=a['rows'];need(len(rows)==37 and len({r['setting']for r in rows})==37,'whole37')
 need(len({r['existing_case']for r in rows})==16,'existing16')
 thresholds={'held':0.00075,'release':0.0025,'freq_rel':5e-7,'log_radius_rel':0.00015,'amp_rel':0.000125}
 count=0
 for i,r in enumerate(rows):
  need(r['existing_case']in before['existing_case_rows_including_newline'],'oldcase')
  need(all(q in before['requirement_blocks']for q in r['primary_requirements']),'oldREQ')
  need(r['new_case_id']is None and r['new_accepted_class']is None and r['new_release_criterion']is None,'nopromotion')
  need(r['input_pointer']=='settings.json#/'+str(i)and r['complete_observations_pointer']=='observations.json#/settings/'+str(i),'exactrowpointers')
  relation=r['metric_relations'];need(set(relation)==set(thresholds),'fivequantities')
  for k,q in relation.items():
   need(q['record_count']==10 and q['quarter_of_existing_proposed_tolerance']==thresholds[k],'tenrecords-frozenquarter')
   need(q['within_proposed_margin']==(q['maximum_deviation']<=thresholds[k]),'arithmeticrelation')
   need(q['all_maximum_records']and all(x['value']==q['maximum_deviation']for x in q['all_maximum_records']),'exactmaxima')
  meet=all(q['within_proposed_margin']for q in relation.values());count+=meet
  need(r['owner_mapping_label']==('meets proposed numerical margin for captured class'if meet else'margin not met; eligibility unresolved'),'label-notclass')
 need(count==31 and len(rows)-count==6,'31six')
def main():
 before=J('owner-before.json');a=J('adoption-map.json');delta=J('proposed-delta.json');canonical=(ROOT/'wiki/specs/device-tension.md').read_bytes();text=canonical.decode();append=(P/'annex-append.md').read_text()
 old=delta['edits'][0]['before'];new=delta['edits'][0]['after'];need(old==before['metric_classification_fragment_before'],'oldparagraph')
 if H(canonical)==before['owner']['sha256']:source=text
 elif(P/'preservation-proof.json').exists()and H(canonical)==J('preservation-proof.json')['proposed_owner']['sha256']:
  need(text.endswith(append),'appliedappend');source=text[:-len(append)].replace(new,old,1).replace('revision: 4\n','revision: 3\n',1)
 else:raise ValueError('currentowner differs from retainedbefore/proposed; asofpin only, no claim currentowner is stale or invalid')
 need(H(source.encode())==before['owner']['sha256']and len(source.encode())==before['owner']['bytes'],'beforeidentity')
 need(source.count(old)==1 and source.count('revision: 3\n')==1,'singleedits')
 candidate=source.replace(old,new,1).replace('revision: 3\n','revision: 4\n',1)+append
 need(block_pins(candidate)==before['requirement_blocks']and len(block_pins(candidate))==15,'all15blocksbyteexact')
 need(row_pins(candidate)==before['existing_case_rows_including_newline']and len(row_pins(candidate))==42,'all42rowsbyteexact')
 need(before['tolerance_table']['text']in candidate,'unchangedtolerancetable')
 reverse=candidate[:-len(append)].replace(new,old,1).replace('revision: 4\n','revision: 3\n',1);need(reverse==source,'fullreversiblepreservation')
 mapping(a,before);need(a['upstream_review']['status']=='APPROVED_SOLE_AUTO_ACTUAL_SOURCE_REVIEW','upstreamapproval')
 review=Path(a['upstream_review']['path']);rb=review.read_bytes();need(len(rb)==a['upstream_review']['bytes']and H(rb)==a['upstream_review']['sha256'],'approvedreviewpin')
 manifest=Path(a['upstream_manifest']['path']);mb=manifest.read_bytes();need(len(mb)==a['upstream_manifest']['bytes']and H(mb)==a['upstream_manifest']['sha256'],'upstreammanifestpin')
 peer=J('peer-metric-summary.json');need(len(peer['rows'])==37,'peer37summary')
 for r,s in zip(a['rows'],peer['rows']):
  need(r['setting']==s['setting'],'peersetting')
  for k,q in r['metric_relations'].items():need(q['maximum_deviation']==s['maxima'][k],'peermaxvalue')
 neg=[]
 def reject(n,f):
  try:f()
  except(ValueError,KeyError):neg.append(n);return
  raise AssertionError(n)
 z=copy.deepcopy(a);z['rows']=z['rows'][:-1];reject('omitted-setting',lambda:mapping(z,before))
 z=copy.deepcopy(a);z['rows'][0]['new_case_id']='DTN-043';reject('new-caseID',lambda:mapping(z,before))
 z=copy.deepcopy(a);z['rows'][0]['new_accepted_class']='stable';reject('automatic-stable-class',lambda:mapping(z,before))
 z=copy.deepcopy(a);z['rows'][9]['owner_mapping_label']='chaotic';reject('failed-margin-chaotic-substitute',lambda:mapping(z,before))
 z=copy.deepcopy(a);z['rows'][0]['metric_relations']['held']['quarter_of_existing_proposed_tolerance']=0.003;reject('raised-margin',lambda:mapping(z,before))
 z=copy.deepcopy(a);z['rows'][0]['complete_observations_pointer']='observations.json#/settings/1';reject('crossed-evidence-row',lambda:mapping(z,before))
 proof={'status':'PASS-owner-mapping-wording-preservation-only','before_owner':before['owner'],'proposed_owner':{'bytes':len(candidate.encode()),'sha256':H(candidate.encode())},'all15blocks42rows_exact':True,'tolerance_table_exact':True,'full_original_reconstructed_byteexact':True,'mapping_rows':37,'oldcaseIDs':16,'margin_relations':{'within':31,'unresolved':6},'negative_controls':neg,'canonical_edited':False,'new_original_or_metric_execution_or_raw_reads':0,'upstream_review_inherited_once':True}
 if(P/'manifest.json').exists():
  sealed=J('manifest.json');need({str(f.relative_to(P))for f in P.rglob('*')if f.is_file()and f.name!='manifest.json'}=={x['path']for x in sealed['files']},'sealedtree')
  for x in sealed['files']:
   raw=(P/x['path']).read_bytes();need(len(raw)==x['bytes']and H(raw)==x['sha256'],'sealedpayload')
 print(json.dumps(proof,indent=2))
if __name__=='__main__':need(sys.argv[1:]==['--check'],'onlycheck');main()
