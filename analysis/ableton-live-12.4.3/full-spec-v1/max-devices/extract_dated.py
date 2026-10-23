"""Extract only dated Version12 pages721/730/731, preserving section boundaries."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent
source=json.loads((P/'source-dated-pdf.json').read_text())
assert hashlib.sha256((P/source['file']).read_bytes()).hexdigest()==source['sha256']
records=[]
for file,device,page,section in [('ds-sampler-p721.txt','DS Sampler',721,'30.1.7'),('expression-legacy-p731.txt','Expression Control Legacy',731,'30.3.3'),('expression-context-p730.txt','Expression Control migration context',730,'30.3.2')]:
 text=subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(P/source['file']),'-']).decode()
 target=P/file
 if target.exists():assert target.read_text()==text
 else:target.write_text(text)
 lines=text.splitlines();paragraph=[];start=None;idx=0;active=page!=731
 for i,line in enumerate(lines+[''],1):
  if line.strip():
   if start is None:start=i
   paragraph.append(line)
  elif paragraph:
   text=' '.join(' '.join(paragraph).split());paragraph=[]
   if page==731 and text.startswith('30.3.3 Expression Control Legacy'):active=True
   if active and text and not text.isdigit() and (page!=730 or text.startswith('The previous version')):
    idx+=1;records.append({'locator':f'MX25:{page}:B{idx:03d}','device':device,'source_id':'D12-2025-MAX-GAPS','file':file,'pdf_page_1based':page,'section':section,'line_start':start,'line_end':i-1,'text':text})
   start=None
assert {page:sum(r['pdf_page_1based']==page for r in records) for page in [721,730,731]}=={721:6,730:1,731:8}
assert all(r['line_start']>=16 for r in records if r['pdf_page_1based']==731)
(P/'dated-blocks.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'dated_blocks':len(records),'pages':[721,730,731],'excluded_current_Expression_paragraphs_on_p731':4,'original_execution':False}))
