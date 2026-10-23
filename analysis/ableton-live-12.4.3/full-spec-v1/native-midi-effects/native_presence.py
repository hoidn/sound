"""Bounded existing symbol-index read; names establish no executed lifecycle law."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
src=Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl')
groups={k:[] for k in ['Arpeggiator','CcControl','Chord','NoteLength','Pitcher','Random','Scale','Velocity']}
h=hashlib.sha256()
for lineno,b in enumerate(src.open('rb'),1):
 h.update(b);x=json.loads(b);n=x['name']
 for cls,rows in groups.items():
  if len(rows)<3 and f'OMidi{cls}Processor::' in n and any(f'::{m}' in n for m in ('Reset','Exit','OnOn')):
   rows.append({'source_line':lineno,'line_sha256':hashlib.sha256(b).hexdigest(),'record':x})
result={'source_path':str(src),'source_sha256':h.hexdigest(),'corpus_architecture':'arm64','selection':'at most three aliases per named processor with Reset/Exit/OnOn; no bodies read','grade':'S-presence only; no externally observable behavior established','groups':groups}
(root/'native-presence.json').write_text(json.dumps(result,indent=2)+'\n')
print({k:len(v) for k,v in groups.items()})
