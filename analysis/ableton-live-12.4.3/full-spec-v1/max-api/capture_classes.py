"""Retain publisher-listed LOM documentation; parse HTML only, never run scripts."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
from urllib.request import Request, urlopen

P=Path(__file__).resolve().parent


class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False
        self.link=None
        self.links=[]
        self.text=[]

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='article':
            assert not self.active
            self.active=True
        if self.active and tag=='a' and attrs.get('href','').startswith('/apiref/lom/'):
            assert self.link is None
            self.link=dict(href=attrs['href'],html_line=self.getpos()[0],html_column=self.getpos()[1],text='')

    def handle_data(self,value):
        if self.active:
            self.text.append(value)
        if self.link is not None:
            self.link['text']+=value

    def handle_endtag(self,tag):
        if tag=='a' and self.link is not None:
            self.links.append(self.link)
            self.link=None
        if tag=='article':
            self.active=False


def capture(link):
    url='https://docs.cycling74.com'+link['href']
    assert url.startswith('https://docs.cycling74.com/apiref/lom/')
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
        raw=response.read()
        final=response.url
        content_type=response.headers.get('Content-Type')
    assert final==url and 'text/html' in content_type
    slug=link['href'].strip('/').split('/')[-1]
    return dict(id='C74-LOM-'+slug.upper(),name=link['text'],url=url,final_url=final,capture_utc=datetime.now(timezone.utc).isoformat(),content_type=content_type,file='classes/'+slug+'-2026-10-19.html',bytes=len(raw),sha256=sha256(raw).hexdigest(),version='Index declares Live12.4.5; target12.4.3 applicability U',index_locator=link),raw


if __name__=='__main__':
    original=json.loads((P/'sources-initial.json').read_text())[0]
    raw=(P/original['file']).read_bytes()
    assert len(raw)==original['bytes'] and sha256(raw).hexdigest()==original['sha256']
    parser=Article()
    parser.feed(raw.decode())
    assert 'Ableton Live version 12.4.5' in ' '.join(parser.text)
    assert len(parser.links)==len({r['href'] for r in parser.links})==45
    assert not (P/'classes-sources-r1.json').exists()
    (P/'classes').mkdir(exist_ok=True)
    records=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(capture,row) for row in parser.links]
        for link,future in zip(parser.links,futures):
            try:
                source,data=future.result()
                target=P/source['file']
                assert not target.exists()
                target.write_bytes(data)
                records.append(source)
            except Exception as error:
                records.append(dict(url='https://docs.cycling74.com'+link['href'],error=type(error).__name__+': '+str(error),target_applicability='U'))
    (P/'classes-sources-r1.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(dict(listed_objects=45,retained=sum('file' in r for r in records),errors=[r for r in records if 'error' in r],runtime_execution=False),indent=2))
