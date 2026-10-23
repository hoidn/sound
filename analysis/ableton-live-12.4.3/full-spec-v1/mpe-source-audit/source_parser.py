"""Pure retained MPE HTML parser; no source imports, network, application or writes."""
from html.parser import HTMLParser
from hashlib import sha256
import re
class Chapter(HTMLParser):
 def __init__(self,text,source):
  super().__init__();self.raw=text;self.source=source;self.offsets=[0]+[m.end() for m in re.finditer('\n',text)];self.depth=0;self.current=None;self.heading=[];self.blocks=[];self.resources=[];self.openresources={};self.unassigned=[];self.table=0;self.row=0;self.cell=None
 def pos(self):
  line,col=self.getpos();return line,col,self.offsets[line-1]+col
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='div':
   if attrs.get('id')=='chapter_content':self.depth=1
   elif self.depth:self.depth+=1
  if not self.depth:return
  if tag=='table':self.table+=1;self.row=0
  if tag in {'h1','h2','h3','h4','h5','h6'}:
   level=int(tag[1]);self.heading=[h for h in self.heading if h['level']<level]+[dict(level=level,text=None,anchor=attrs.get('id'),section=attrs.get('data-number'),html_line=self.pos()[0])]
  if self.current is None and tag in {'h1','h2','h3','h4','h5','h6','p','li','tr'}:
   line,col,offset=self.pos();self.current=dict(kind=tag,attributes=attrs,html_line=line,html_column=col,raw_start=offset,parts=[],heading_context=[dict(h) for h in self.heading])
   if tag=='tr':self.row+=1;self.current.update(table=self.table,row=self.row,cells=[])
  if tag in {'td','th'} and self.current is not None:self.cell=dict(kind=tag,parts=[])
  if tag in {'a','img','figcaption'}:
   line,col,offset=self.pos();r=dict(kind={'a':'link','img':'image','figcaption':'caption'}[tag],attributes=attrs,html_line=line,html_column=col,raw_start=offset,starttag_sha256=sha256(self.get_starttag_text().encode()).hexdigest(),heading_context_anchor=self.heading[-1]['anchor'] if self.heading else None)
   self.resources.append(r)
   if tag!='img':self.openresources[tag]=(r,[])
 def handle_data(self,text):
  if not self.depth:return
  if self.current is not None:self.current['parts'].append(text)
  if self.cell is not None:self.cell['parts'].append(text)
  for r,parts in self.openresources.values():parts.append(text)
  if text.strip() and self.current is None and 'figcaption' not in self.openresources:self.unassigned.append(dict(html_line=self.pos()[0],text=text))
 def handle_endtag(self,tag):
  if not self.depth:return
  if tag in {'td','th'} and self.cell is not None:
   self.cell['text']=' '.join(' '.join(self.cell.pop('parts')).split());self.current['cells'].append(self.cell);self.cell=None
  if self.current is not None and self.current['kind']==tag:
   r=self.current;self.current=None;r['text']=' '.join(''.join(r.pop('parts')).split());r['raw_end']=self.raw.index('>',self.pos()[2])+1;r['raw_html']=self.raw[r['raw_start']:r['raw_end']]
   if tag.startswith('h'):
    self.heading[-1]['text']=r['text'];r['heading_context']=[dict(h) for h in self.heading]
   if tag=='tr':r['text']=' | '.join(c['text'] for c in r['cells']);r['raw_html_sha256']=sha256(r['raw_html'].encode()).hexdigest()
   r.update(id=f"{self.source}-B{len(self.blocks)+1:03}",source_id=self.source);self.blocks.append(r)
  if tag in self.openresources:
   r,parts=self.openresources.pop(tag);r['text']=' '.join(''.join(parts).split())
  if tag=='div':self.depth-=1

def extract(text,source):
 p=Chapter(text,source);p.feed(text);assert p.blocks and not p.unassigned,p.unassigned;return p.blocks,p.resources
