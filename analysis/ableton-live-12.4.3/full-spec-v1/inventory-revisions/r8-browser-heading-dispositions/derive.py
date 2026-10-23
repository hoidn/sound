"""Finite retained-source diagnosis. Never import/run original inventory capture code."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import hashlib
import json
import re
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[4]
B = P.parents[1]
R6 = B / 'inventory-revisions/r6-citation-crosswalk'
I = B / 'inventory'
BC = B / 'browser-content'
NAMES = ['logging-into-splice', 'searching-for-splice-samples', 'working-with-splice-samples', 'splice-library', 'splice-settings', 'abl-assets', 'chord-banks', 'clips-folder', 'defaults-folder', 'grooves-folder', 'presets-folder', 'samples-folder', 'templates-folder', 'managing-files-in-the-user-library']
BASE_URL = 'https://www.ableton.com/en/live-manual/12/working-with-the-browser/'

def load(path):
    return json.loads(path.read_text())

def pin(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

class Toc(HTMLParser):
    """The original numbered-anchor selection, copied as a bounded parser only."""
    def __init__(self):
        super().__init__(); self.anchor = None; self.rows = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and '/live-manual/12/' in a.get('href', ''):
            self.anchor = [a['href'], '', self.getpos()[0]]
    def handle_data(self, data):
        if self.anchor is not None:
            self.anchor[1] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.anchor is not None:
            href, text, line = self.anchor
            m = re.match(r'^(\d+(?:\.\d+)*)(?:\.)?\s+(.+)$', text.strip())
            if m:
                slug, anchor = href.split('/12/')[1].split('/#')
                self.rows.append(dict(id='SURF-MAN-' + slug.upper() + '--' + anchor.upper(), number=m[1], title=m[2], url='https://www.ableton.com' + href, html_line=line, target_match='version-uncertain', specification='unmapped', complete=False))
            self.anchor = None
    def finish(self):
        for row in self.rows:
            row['leaf'] = not any(other['number'].startswith(row['number'] + '.') for other in self.rows)
        return self.rows

class Headings(HTMLParser):
    """Actual chapter headings, raw tags and outline ancestors; no title matching."""
    def __init__(self, text):
        super().__init__(); self.text = text; self.lines = text.splitlines(keepends=True)
        self.div_depth = 0; self.active = None; self.rows = []; self.outline = []; self.ids = Counter(); self.hrefs = []
    def position_offset(self, pos):
        line, col = pos
        return sum(map(len, self.lines[:line-1])) + col
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids[a['id']] += 1
        if tag == 'a' and 'href' in a: self.hrefs.append(a['href'])
        if tag == 'div':
            if self.div_depth: self.div_depth += 1
            elif a.get('id') == 'chapter_content': self.div_depth = 1
        if self.div_depth and re.fullmatch('h[1-6]', tag):
            assert self.active is None
            self.active = {'tag': tag, 'id': a.get('id'), 'number': a.get('data-number'), 'attrs': attrs, 'html_line': self.getpos()[0], 'html_column': self.getpos()[1], 'raw_start_tag': self.get_starttag_text(), 'text': '', '_start': self.position_offset(self.getpos())}
    def handle_data(self, data):
        if self.active is not None: self.active['text'] += data
    def handle_endtag(self, tag):
        if self.active is not None and tag == self.active['tag']:
            row = self.active; row['text'] = ' '.join(row['text'].split())
            end = self.position_offset(self.getpos()) + len('</' + tag + '>')
            row['raw_heading_html'] = self.text[row.pop('_start'):end]
            while self.outline and int(self.outline[-1]['tag'][1]) >= int(tag[1]): self.outline.pop()
            row['outline_ancestors'] = [{k: x[k] for k in ('tag','id','number','html_line','html_column','text')} for x in self.outline]
            self.rows.append(row); self.outline.append(row); self.active = None
        if tag == 'div' and self.div_depth: self.div_depth -= 1

def parse(text):
    t = Toc(); t.feed(text); h = Headings(text); h.feed(text)
    return t.finish(), h

def selfchecks():
    text = '<div id="chapter_content"><h3 data-number="4.7.3" id="p">Parent</h3><h4 id="x" data-number="4.7.3.1"><span>4.7.3.1</span> Child</h4><a id="not-heading"></a><h4 id="unknown">Unknown</h4></div><a href="/en/live-manual/12/x/#x">4.7.3.1 Child</a>'
    rows, headings = parse(text)
    assert rows[0]['number'] == '4.7.3.1' and rows[0]['leaf']
    assert len(headings.rows) == 3 and headings.rows[1]['outline_ancestors'][-1]['id'] == 'p'
    assert headings.rows[1]['text'] == '4.7.3.1 Child'
    assert 'not-heading' not in [h['id'] for h in headings.rows]
    assert headings.rows[2]['number'] is None
    _, dup = parse('<div id="chapter_content"><h4 id="x">X</h4><h4 id="x">Y</h4></div>')
    assert dup.ids['x'] == 2
    return {'four_part_number_accepted': True, 'numbered_heading_without_link_separate': True, 'inline_title_text': True, 'outline_parent_not_DOM_parent': True, 'nonheading_anchor_not_heading': True, 'missing_number_unresolved': True, 'duplicate_id_detected': True}

def derive():
    toc_text = (I / 'manual-12-toc-2026-10-19.html').read_text()
    browser_text = (BC / 'manual-browser-2026-10-19.html').read_text()
    original = load(I / 'manual-toc.json')
    toc, th = parse(toc_text); browser_toc, bh = parse(browser_text)
    assert toc == original and len(original) == 880 and sum(r['leaf'] for r in original) == 708
    assert [{k:v for k,v in r.items() if k != 'html_line'} for r in toc] == [{k:v for k,v in r.items() if k != 'html_line'} for r in browser_toc]
    unmatched = load(R6 / 'unmatched-citations.json')
    refs = [(n,r) for n,r in enumerate(unmatched) if r['packet'] == 'browser-content']
    assert len(refs) == 46 and {r['evidence']['exact_anchor_url'] for _,r in refs} == {BASE_URL + '#' + n for n in NAMES}
    source = load(BC / 'sources.json')[0]
    assert source['sha256'] == pin(BC / source['file'])['sha256']
    heading_map = {h['id']: h for h in bh.rows}
    blocks = load(BC / 'source-blocks.json')
    rows = []; links = []
    for n, anchor in enumerate(NAMES, 1):
        url = BASE_URL + '#' + anchor; h = heading_map[anchor]
        assert bh.ids[anchor] == 1 and th.ids[anchor] == 0
        assert h['tag'] == 'h4' and len(h['number'].split('.')) == 4
        assert not any(x.split('#')[-1] == anchor for x in bh.hrefs + th.hrefs)
        assert not any(r['url'] == url for r in original)
        parent = h['outline_ancestors'][-1]
        assert parent['tag'] == 'h3' and h['number'].rsplit('.',1)[0] == parent['number']
        parent_row = next(r for r in original if r['url'] == BASE_URL + '#' + parent['id'])
        assert parent_row['leaf'] is True
        identity = 'SRC-BROWSER-HEADING-' + source['sha256'][:12].upper() + '--' + anchor.upper()
        matching_refs = [i for i,r in refs if r['evidence']['exact_anchor_url'] == url]
        rows.append({'id': identity, 'exact_url': url, 'source': source, 'heading': h, 'retained_TOC_id_node_count': 0, 'retained_TOC_link_count': 0, 'retained_Browser_link_count': 0, 'disposition': 'real-numbered-h4-absent-from-retained-toc-links', 'parser_selection_omission': False, 'parser_depth_filter_present': False, 'capture_version_difference_cause': 'not supported by retained navigation; precise publication cause unknown', 'direct_toc_match': False, 'matched_manual_id': None, 'semantic_coverage': 'unknown', 'target_applicability': 'U', 'complete': False, 'r6_reference_count': len(matching_refs), 'source_block_pointers': ['/' + str(i) for i,b in enumerate(blocks) if b['anchor'] == anchor], 'structural_relation': {'type': 'source-heading-outline-child-of', 'subject': identity, 'object_exact_url': parent_row['url'], 'object_baseline_id': parent_row['id'], 'object_source_locator': parent, 'object_original_leaf_unchanged': True, 'meaning': 'ordered heading-level ancestry with agreeing data-number prefix; not DOM containment, direct citation join, behavioral support or coverage'}})
        for i,r in refs:
            if r['evidence']['exact_anchor_url'] == url:
                assert r['evidence']['join_status'] == 'exact-URL-absent-from-TOC' and r['evidence']['matched_manual_id'] is None and r['target_applicability'] == 'U'
                links.append({'source_heading_id': identity, 'r6_catalog': str((R6/'unmatched-citations.json').relative_to(ROOT)), 'r6_json_pointer': '/' + str(i), 'original_record': r})
    assert len(rows) == 14 and len(links) == 46
    return {'heading-dispositions.json': rows, 'r6-reference-pointers.json': sorted(links,key=lambda r:int(r['r6_json_pointer'][1:])), 'summary.json': {'scope': 'finite Q047 source/navigation diagnosis only', 'original_TOC_rows_unchanged': 880, 'original_leaves_unchanged': 708, 'original_chapters_unchanged': 43, 'source_headings': 14, 'outline_child_relations': 14, 'R6_references_preserved_unjoined': 46, 'new_direct_TOC_matches': 0, 'behavioral_coverage_credit': 0, 'completed_topics': 0, 'source_heading_tags': {'h4':14}, 'same_number_title_URL_TOC_sequences_in_both_retained_pages': True, 'capture_version_causality': 'unknown; both retained navigation sequences agree', 'target_applicability': 'U', 'semantic_coverage': 'unknown', 'parser_selfchecks': selfchecks()}}

def main():
    check = sys.argv[1:] == ['--check']
    assert check or sys.argv[1:] == []
    manifest_path = P / 'manifest.json'
    if not check: assert not manifest_path.exists(), 'Frozen packet: successor revision required'
    before = {str(x.relative_to(P)): pin(x) for x in P.rglob('*') if x.is_file()}
    if check:
        for record in load(P/'inputs.json'): assert pin(ROOT / record['path']) == record
    outputs = derive()
    if check:
        for name,data in outputs.items(): assert load(P/name) == data, name
        for path in P.iterdir():
            if path.is_file():
                content = path.read_text()
                assert all(line == line.rstrip() for line in content.splitlines()), path
                assert content.endswith('\n'), path
        for link in re.findall(r'\]\(([^)]+)\)', (P/'README.md').read_text()):
            assert (P / link.split('#')[0]).resolve().exists(), link
        manifest = load(manifest_path)
        for record in manifest['files']: assert pin(ROOT / record['path']) == record
        assert {r['path'] for r in manifest['files']} == {str(x.relative_to(ROOT)) for x in P.iterdir() if x.is_file() and x.name != 'manifest.json'}
        assert {str(x.relative_to(P)): pin(x) for x in P.rglob('*') if x.is_file()} == before
        print(json.dumps({'status':'passed-read-only','summary':outputs['summary.json'],'input_pins':len(load(P/'inputs.json')),'payloads':len(manifest['files']),'manifest_sha256':pin(manifest_path)['sha256']},indent=2))
    else:
        for name,data in outputs.items(): (P/name).write_text(json.dumps(data,indent=2)+'\n')

if __name__ == '__main__': main()
