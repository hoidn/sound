"""Inventory explicit publisher API declarations; no API or example execution."""
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import sys

P=Path(__file__).resolve().parent


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False
        self.articles=0
        self.current=None
        self.rows=[]
        self.section=None

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='article':
            assert not self.active
            self.active=True
            self.articles+=1
        if self.active and self.current is None and tag in {'h1','h2','h3','h4','p','li','pre','td','th','dt','dd'}:
            if tag=='h2':
                self.section=attrs.get('id')
            self.current=dict(tag=tag,anchor=attrs.get('id'),section=self.section,html_line=self.getpos()[0],html_column=self.getpos()[1],parts=[])

    def handle_data(self,value):
        if self.current is not None:
            self.current['parts'].append(value)

    def handle_endtag(self,tag):
        if self.current is not None and tag==self.current['tag']:
            row=self.current
            self.current=None
            row['text']=' '.join(''.join(row.pop('parts')).split())
            row['block']=f'B{len(self.rows)+1:04d}'
            self.rows.append(row)
        if tag=='article':
            self.active=False


def extract(text):
    parser=Blocks()
    parser.feed(text)
    assert parser.articles==1 and parser.rows and parser.rows[0]['tag']=='h1'
    assert not parser.active and parser.current is None
    return parser.rows


if __name__=='__main__':
    assert sys.argv[1:] in ([],['--check'])
    checking=sys.argv[1:]==['--check']
    test=extract('<p>outside</p><article><h1 id="a">A</h1><h2 id="properties">Properties</h2><h3 id="n">n <code>int</code></h3><p>Access: <b>get</b></p><table><tr><td>x</td></tr></table></article><p>outside</p>')
    assert [r['text'] for r in test]==['A','Properties','n int','Access: get','x']
    assert test[2]['anchor']=='n' and test[2]['section']=='properties'
    initial=json.loads((P/'sources-initial.json').read_text())
    classes=json.loads((P/'classes-sources-r1.json').read_text())
    bridges=json.loads((P/'bridge-sources-r1.json').read_text())
    sources=initial+classes+bridges
    assert len(initial)==2 and len(classes)==45 and len(bridges)==6
    assert len({r['id'] for r in sources})==53
    blocks={}
    for source in sources:
        raw=(P/source['file']).read_bytes()
        assert len(raw)==source['bytes'] and sha256(raw).hexdigest()==source['sha256']
        blocks[source['id']]=extract(raw.decode())
    assert 'Ableton Live version 12.4.5' in ' '.join(r['text'] for r in blocks[initial[0]['id']])
    entries,members=[],[]
    for source in classes:
        rows=blocks[source['id']]
        assert rows[0]['text']==source['name']
        entry_id='SURF-API-LOM-'+source['file'].split('/')[1].removesuffix('-2026-10-19.html').upper()
        entry=dict(id=entry_id,name=source['name'],source_id=source['id'],url=source['url'],source_sha256=source['sha256'],declared_members=[],target_applicability='U',specification='unmapped',complete=False)
        for row in rows:
            if row['tag']=='h3' and row['section'] in {'children','properties','functions'}:
                assert row['anchor'] and row['text']
                mid=entry_id+'--'+row['section'].upper()+'--'+row['anchor']
                members.append(dict(id=mid,reference_entry=entry_id,category=row['section'],heading=row['text'],anchor=row['anchor'],block=row['block'],source_id=source['id'],html_line=row['html_line'],html_column=row['html_column'],url=source['url']+'#'+row['anchor'],target_applicability='U',requirements=[],cases=[],complete=False))
                entry['declared_members'].append(mid)
        entries.append(entry)
    assert len(entries)==45 and len({r['id'] for r in entries})==45
    assert members and len({r['id'] for r in members})==len(members)
    entrypoints=[dict(id='SURF-API-BRIDGE-'+r['id'].removeprefix('C74-'),source_id=r['id'],url=r['url'],source_sha256=r['sha256'],target_applicability='U',member_inventory='pending; generic Max box attributes not automatically Live API surface',complete=False) for r in bridges]
    summary=dict(reference_entries=45,explicit_member_declarations=len(members),by_category=dict(Counter(r['category'] for r in members)),bridge_lifecycle_references=6,retained_sources=53,retained_blocks=sum(len(r) for r in blocks.values()),index_declares_live_version='12.4.5',target='12.4.3; applicability U',complete_entries=0,scope='Explicit headings only; inherited members, aliases/root semantics, bridge signatures/events/grammars, versions and actual outcomes require reconciliation. Counts overlap other product dimensions and are not complete API or behavior coverage.')
    outputs={'all-sources-r1.json':sources,'reference-blocks.json':blocks,'lom-entries.json':entries,'lom-members.json':members,'bridge-entrypoints.json':entrypoints,'summary.json':summary}
    for name,value in outputs.items():
        raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
        file=P/name
        assert not file.exists() or file.read_bytes()==raw,name
        if checking:
            assert file.is_file(),name
        else:
            file.write_bytes(raw)
    if checking:
        for name,pin in json.loads((P/'manifest-inventory-r1.json').read_text())['files'].items():
            raw=(P/name).read_bytes()
            assert len(raw)==pin['bytes'] and sha256(raw).hexdigest()==pin['sha256'],name
    print(json.dumps(summary,indent=2))
