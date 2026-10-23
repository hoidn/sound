"""Retain official documentation and bounded installed-resource evidence; no Live execution."""
from pathlib import Path
import gzip
import hashlib
import json
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
APP = Path('/home/ollie/Ableton Live 12 Suite.app')
def digest(data):
    return hashlib.sha256(data).hexdigest()
def retain(name, data):
    target = ROOT / name
    if target.exists():
        assert target.read_bytes() == data, f'Immutable capture differs: {target}'
    else:
        target.write_bytes(data)
def write_json(name, value):
    retain(name, (json.dumps(value, indent=2) + '\n').encode())

sources = []
for slug in ('editing-mpe', 'using-tuning-systems', 'using-grooves'):
    url = f'https://www.ableton.com/en/live-manual/12/{slug}/'
    name = f'manual-12-{slug}-2026-10-19.html'
    raw = (ROOT/name).read_bytes() if (ROOT/name).exists() else urllib.request.urlopen(url).read()
    retain(name, raw)
    soup = BeautifulSoup(raw, 'html.parser')
    article = soup.find('article') or soup.find('main') or soup
    for element in article(['script', 'style', 'nav']):
        element.decompose()
    lines = article.get_text('\n', strip=True).splitlines()
    textname = f'manual-12-{slug}.txt'
    retain(textname, ('\n'.join(f'{i:04d} {s}' for i,s in enumerate(lines,1))+'\n').encode())
    sources.append(dict(id='SRC-MTG-'+slug.upper(), url=url, captured='2026-10-19', edition='Version 12; patch revision not supplied', applicability='All detailed 12.4.3 behavior U', html=name, sha256=digest(raw), text=textname, headings=[dict(tag=h.name,id=h.get('id'),text=h.get_text(' ',strip=True)) for h in article.find_all(['h1','h2','h3','h4'])]))
write_json('sources.json',sources)

schema = APP/'Contents/App-Resources/Schema/12.0_12402.txt'
raw = schema.read_bytes()
lines = raw.decode().splitlines()
classes = ['MpeSettings','Groove','GroovePool','ClipGrooveSettings','TuningSystem','TuningRatio','TuningSystemScale','TuningSystemScaleInterval','NoteTuning']
blocks = []
for name in classes:
    start = next(i for i,s in enumerate(lines) if s.strip() == f'<{name}>')
    end = next(i for i in range(start+1,len(lines)) if lines[i].strip() == f'</{name}>')
    blocks.append(dict(name=name,start_line=start+1,end_line=end+1,text='\n'.join(lines[start:end+1])))
write_json('schema-presence.json',dict(path=str(schema),sha256=digest(raw),build='12.4.3',limitation='Declarations establish resource vocabulary only, not editing, units, defaults or execution',classes=blocks))

examples = [
    ('groove-example.agr','Contents/App-Resources/Core Library/Grooves/Utility/Quantize 8.agr'),
    ('tuning-example.ascl','Contents/App-Resources/Core Library/Tunings/EDO/12-TET (EDO).ascl'),
    ('mpe-device-example.adv','Contents/App-Resources/Core Library/Defaults/Instruments/Drift.adv'),
]
records=[]
for dest, rel in examples:
    path=APP/rel
    raw=path.read_bytes()
    retain(dest,raw)
    rec=dict(path=str(path),retained=dest,sha256=digest(raw),size=len(raw))
    if raw[:2] == b'\x1f\x8b' or raw.startswith(b'<?xml'):
        xml=gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
        ET.fromstring(xml)
        retain(dest+'.xml',xml)
        rec['derived_xml']=dest+'.xml'
        rec['root_attributes']=ET.fromstring(xml).attrib
    records.append(rec)
write_json('shipped-examples.json', records)
assert len(sources)==3 and len(blocks)==len(classes) and len(records)==3
