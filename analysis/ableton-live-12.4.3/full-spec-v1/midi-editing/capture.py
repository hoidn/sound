"""Capture two official manual chapters; produces no original-program execution."""
from pathlib import Path
import hashlib,json,urllib.request
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
sources=[]
for slug in ['editing-midi','midi-tools']:
    url=f'https://www.ableton.com/en/live-manual/12/{slug}/'
    raw=urllib.request.urlopen(url).read()
    html=root/f'manual-12-{slug}-2026-10-19.html'
    if html.exists():
        raise FileExistsError(html)
    html.write_bytes(raw)
    soup=BeautifulSoup(raw,'html.parser')
    article=soup.find('article') or soup.find('main') or soup
    for element in article(['script','style','nav']): element.decompose()
    lines=article.get_text('\n',strip=True).splitlines()
    textpath=root/f'manual-12-{slug}.txt'
    textpath.write_text('\n'.join(f"{i:04d} {line.rstrip() or '[blank]'}" for i,line in enumerate(lines,1))+'\n')
    headings=[{'tag':h.name,'id':h.get('id'),'text':h.get_text(' ',strip=True)} for h in article.find_all(['h1','h2','h3','h4'])]
    sources.append({'id':'SRC-MIDI-EDIT-'+slug.upper(),'url':url,'captured':'2026-10-19','edition':'current Live 12 manual; publication revision unspecified','target':'12.4.3 applicability unknown','html':html.name,'html_sha256':hashlib.sha256(raw).hexdigest(),'derived_text':textpath.name,'headings':headings})
(root/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
