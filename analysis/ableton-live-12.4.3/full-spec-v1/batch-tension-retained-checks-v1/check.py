#!/usr/bin/env python3
"""Owned retained-data checks only; never imports or runs historical helpers."""
import copy,hashlib,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((P/n).read_text())
def pointer(j,p):
 for q in p.split('/')[1:]:j=j[q.replace('~1','/').replace('~0','~')]
 return j
def validate(doc,old,selectors,frontiers):
 entries=doc['entries'];names=list(old)
 if doc['sets']!=names or set(selectors)!=set(names):raise ValueError('whole11')
 if len(entries)!=239 or len({e['id'] for e in entries})!=239 or len({e['result_pointer'] for e in entries})!=239:raise ValueError('whole239projection')
 recovered={k:{} for k in names}
 recovered['polyphony']['rule']=doc['polyphony_rule_metadata']
 for e in entries:
  if pointer(old,e['result_pointer'])!=e['retained_report_value']:raise ValueError('literal report join')
  if e['exact_execution_receipt'] is not None or not e['new_exact_input_fixture_admission'].startswith('U where'):raise ValueError('missingreceiptpromotion')
  if e['check_set'] not in names or e['source_anchor']!=selectors[e['check_set']]['source']:raise ValueError('sourcegroup')
  parts=[q.replace('~1','/').replace('~0','~') for q in e['result_pointer'].split('/')[1:]]
  dst=recovered
  for q in parts[:-1]:dst=dst.setdefault(q,{})
  dst[parts[-1]]=e['retained_report_value']
 if recovered!=old:raise ValueError('lossless whole report')
 if len(selectors['timing']['finite_selector']['note_on_groups'][0]['event_frames'])!=140:raise ValueError('whole timing140')
 if len(selectors['timing']['finite_selector']['note_off_groups'][0]['off_frames'])!=100:raise ValueError('whole timing100')
 if len(selectors['quantization']['finite_selector']['position_cases'])!=6 or any(len(x['all_host_values_binary32'])!=129 for x in selectors['quantization']['finite_selector']['position_cases']):raise ValueError('whole position6x129')
 if len(selectors['polyphony']['finite_selector']['whole_capacity_cartesian']['stored_Polyphony'])!=10 or len(selectors['polyphony']['finite_selector']['whole_capacity_cartesian']['later_note_counts'])!=34:raise ValueError('whole capacity10x34')
 if not any(x.get('route')=='TNR-067' and x['disposition'].startswith('U:') for x in frontiers['specific']):raise ValueError('missing ungated frontier')
 return True
def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('only --check; no execution mode')
 pins=load('source-pins.json')['pins']
 for z in pins:
  b=pathlib.Path(z['path']).read_bytes()
  if len(b)!=z['bytes'] or hashlib.sha256(b).hexdigest()!=z['sha256']:raise ValueError('selected retained-source pin mismatch')
 old=json.loads(pathlib.Path(next(z['path'] for z in pins if z['path'].endswith('/results/checks.json'))).read_text())
 doc=load('observations.json');sel=load('input-selectors.json');front=load('open-frontiers.json');validate(doc,old,sel,front)
 negatives=[]
 for n,mut in [('omit-observation',lambda d,s,f:d['entries'].pop()),('duplicate-pointer',lambda d,s,f:d['entries'][-1].update(result_pointer=d['entries'][0]['result_pointer'])),('invent-result',lambda d,s,f:d['entries'][0].update(retained_report_value=False)),('fabricate-receipt',lambda d,s,f:d['entries'][0].update(exact_execution_receipt={'pid':1})),('grade-missingbridge',lambda d,s,f:d['entries'][0].update(new_exact_input_fixture_admission='X complete')),('omit-checkset',lambda d,s,f:d['sets'].pop()),('truncate-positionclass',lambda d,s,f:s['quantization']['finite_selector']['position_cases'][0]['all_host_values_binary32'].pop()),('truncate-polyphony',lambda d,s,f:s['polyphony']['finite_selector']['whole_capacity_cartesian']['later_note_counts'].pop()),('drop-ungated-U',lambda d,s,f:f.update(specific=[x for x in f['specific'] if x.get('route')!='TNR-067']))]:
  d,s,f=copy.deepcopy(doc),copy.deepcopy(sel),copy.deepcopy(front);mut(d,s,f)
  try:validate(d,old,s,f)
  except (ValueError,KeyError):negatives.append(n)
  else:raise AssertionError(n)
 print(json.dumps({'status':'PASS','data_only':True,'sets':11,'projection_entries':239,'lossless_report_reconstruction':True,'negative_controls':negatives,'original_model_helper_audio_comparator_calls':0,'limits':'Retained report/source joins only, no original execution or missing receipt/raw custody validation.'}))
if __name__=='__main__':main()
