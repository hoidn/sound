"""Finite retained-HTML numbered-heading census. No paragraphs/network/source execution."""
from pathlib import Path
from collections import Counter, defaultdict
from html.parser import HTMLParser
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime

P = Path(__file__).resolve().parent
BASE = P.parents[1]
ROOT = BASE.parents[2]
CHECK = sys.argv[1:] == ['--check']
assert sys.argv[1:] in ([], ['--check'])
if not CHECK:
    assert not (P / 'manifest.json').exists(), 'Sealed census: use --check or a new successor'
read = lambda path: json.loads(path.read_text())
sha = lambda raw: hashlib.sha256(raw).hexdigest()
escape = lambda key: str(key).replace('~', '~0').replace('/', '~1')
NUMBER = re.compile(r'[0-9]+(?:\.[0-9]+)*\Z')


class ChapterHeadings(HTMLParser):
    """Only heading tags, English self links and the exact chapter_content div."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.boundaries = []
        self.closed_boundaries = 0
        self.canonical = []
        self.english = []
        self.title_parts = []
        self.in_title = False
        self.current = None
        self.headings = []
        self.outline = []
        self.ignored_heading_count = 0
        self.issues = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link':
            if a.get('rel') == 'canonical': self.canonical.append(a.get('href'))
            if a.get('rel') == 'alternate' and a.get('hreflang') == 'en': self.english.append(a.get('href'))
        if tag == 'title': self.in_title = True
        if tag == 'div':
            if a.get('id') == 'chapter_content':
                if self.depth: self.issues.append('nested chapter_content boundary')
                self.boundaries.append([tag, list(self.getpos())])
                self.depth += 1
            elif self.depth:
                self.depth += 1
        if self.depth and re.fullmatch('h[1-6]', tag):
            if self.current is not None:
                self.issues.append('nested or unclosed heading')
                return
            self.current = dict(tag=tag, attributes=attrs, id=a.get('id'), number=a.get('data-number'),
                                html_line=self.getpos()[0], html_column=self.getpos()[1], parts=[])

    def handle_data(self, data):
        if self.in_title: self.title_parts.append(data)
        if self.current is not None: self.current['parts'].append(data)

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if self.current is not None and tag == self.current['tag']:
            row = self.current
            self.current = None
            level = int(row['tag'][1])
            self.outline = [h for h in self.outline if h['level'] < level]
            text = ''.join(row.pop('parts'))
            number = row['number']
            if number is None or not NUMBER.fullmatch(number):
                self.ignored_heading_count += 1
                # An unnumbered parent must not silently lend a fabricated numbered ancestor.
                self.outline.append(dict(level=level, index=None, number=None))
            else:
                flags = []
                if not row['id']: flags.append('no-explicit-id-no-literal-URL-join')
                ancestors = [h['index'] for h in self.outline if h['index'] is not None]
                if any(h['index'] is None for h in self.outline): flags.append('unnumbered-ancestor-not-in-numbered-ledger')
                if (self.outline[-1]['level'] if self.outline else 0) + 1 < level: flags.append('heading-level-gap-no-parent-invented')
                if level != len(number.split('.')): flags.append('tag-level-versus-number-depth-differs')
                if self.outline and self.outline[-1]['number'] and not number.startswith(self.outline[-1]['number'] + '.'):
                    flags.append('encountered-outline-number-prefix-differs')
                # Remove only the literal displayed number prefix, never title/URL similarity.
                title = text
                removed = None
                for prefix in [number + '. ', number + ' ']:
                    if text.startswith(prefix):
                        title = text[len(prefix):]
                        removed = prefix
                        break
                row.update(index=len(self.headings), heading_level=level, number_depth=len(number.split('.')),
                           heading_text=text, title=title, removed_literal_number_prefix=removed,
                           preceding_actual_numbered_ancestors=ancestors, flags=flags)
                row['attributes'] = [[k, v] for k, v in row['attributes']]
                self.headings.append(row)
                self.outline.append(dict(level=level, index=row['index'], number=number))
        if tag == 'div' and self.depth:
            self.depth -= 1
            if self.depth == 0:
                self.closed_boundaries += 1
                if self.current is not None: self.issues.append('heading crosses chapter_content boundary')

    def result(self):
        if self.depth: self.issues.append('unclosed chapter_content')
        if self.current is not None: self.issues.append('unclosed heading')
        return dict(canonical=self.canonical, english_alternate_urls=self.english,
                    chapter_boundary=self.boundaries, closed_chapter_boundaries=self.closed_boundaries,
                    document_title=''.join(self.title_parts), headings=self.headings,
                    ignored_non_numeric_or_unnumbered_headings=self.ignored_heading_count,
                    issues=self.issues)


def parse(raw):
    parser = ChapterHeadings()
    parser.feed(raw.decode('utf-8'))
    return parser.result()


def selfchecks():
    sample = b'''<h1 data-number="99" id="outside">outside</h1><script>"<h2 data-number='88'>ignored</h2>"</script><div id="chapter_content"><h1 data-number="4" id="root"><span>4.</span> Root</h1><div><h2 data-number="4.1" id="part">4.1 Part</h2></div><h4 data-number="4.1.1.1" id="deep">4.1.1.1 Deep</h4><h4 data-number="4.x" id="bad">bad</h4><h4 data-number="4.1.1.1" id="deep">same number and ID retained</h4></div><h2 data-number="77" id="after">outside</h2>'''
    got = parse(sample)
    assert [h['id'] for h in got['headings']] == ['root', 'part', 'deep', 'deep']
    assert got['headings'][2]['preceding_actual_numbered_ancestors'] == [0, 1]
    assert 'heading-level-gap-no-parent-invented' in got['headings'][2]['flags']
    assert got['ignored_non_numeric_or_unnumbered_headings'] == 1 and not got['issues']
    assert len(got['chapter_boundary']) == got['closed_chapter_boundaries'] == 1
    assert Counter(h['id'] for h in got['headings'])['deep'] == 2
    assert parse(b'<div id="chapter_content"><h1 data-number="1" id="a">A</h1>')['issues'] == ['unclosed chapter_content']
    two = parse(b'<div id="chapter_content"><h1 data-number="1">A</h1></div><div id="chapter_content"><h1 data-number="2">B</h1></div>')
    assert len(two['chapter_boundary']) == 2 and two['headings'][0]['flags'] == ['no-explicit-id-no-literal-URL-join']
    mismatch = parse(b'<div id="chapter_content"><h1 data-number="1" id="a">A</h1><h3 data-number="1.2" id="b">B</h3></div>')
    assert set(mismatch['headings'][1]['flags']) == {'heading-level-gap-no-parent-invented', 'tag-level-versus-number-depth-differs'}
    assert not parse(b'<article><h1 data-number="1">API is not a chapter</h1></article>')['headings']
    six = parse(b'<div id="chapter_content"><h1 data-number="1">A</h1><h2 data-number="1.1">B</h2><h3 data-number="1.1.1">C</h3><h4 data-number="1.1.1.1">D</h4><h5 data-number="1.1.1.1.1">E</h5><h6 data-number="1.1.1.1.1.1">F</h6><h7 data-number="1.1.1.1.1.1.1">outside allowed tags</h7></div>')
    assert [h['tag'] for h in six['headings']] == ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    assert six['headings'][-1]['preceding_actual_numbered_ancestors'] == [0, 1, 2, 3, 4]
    nbsp = parse(b'<div id="chapter_content"><h1 data-number="1" id="a">1. Speed vs.&nbsp;Quality</h1></div>')
    assert nbsp['headings'][0]['title'] == 'Speed vs.\u00a0Quality'
    # Same-URL distinct hashes never collapse, and identical bytes retain both bindings.
    trial = [('same-url', b'A', 'first'), ('same-url', b'A', 'copy'), ('same-url', b'B', 'variant')]
    grouped = defaultdict(list)
    for url, raw, path in trial: grouped[(url, sha(raw))].append(path)
    assert len(grouped) == 2 and sorted(map(len, grouped.values())) == [1, 2]
    return dict(outside_script_and_after_boundary_ignored=True, nested_div_boundary=True,
                numeric_data_number_required=True, h1_through_h6_only=True,
                depth_gaps_and_mismatches_flagged=True, duplicate_ID_and_number_preserved=True,
                missing_ID_and_multiple_boundaries_visible=True, unclosed_boundary_visible=True,
                decoded_title_whitespace_and_NBSP_preserved=True,
                same_URL_hash_variants_separate=True, identical_bytes_keep_physical_bindings=True)


def pin(path, record):
    raw = path.read_bytes()
    assert len(raw) == record['bytes'] and sha(raw) == record['sha256'], path
    return raw


def at_pointer(value, pointer):
    if pointer == '': return value
    assert pointer.startswith('/')
    for part in pointer[1:].split('/'):
        key = part.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def catalog_records(metadata, hashes, html_paths):
    sources, bindings = [], []
    for item in metadata:
        path = ROOT / item['path']
        data = json.loads(pin(path, item))
        def visit(x, ptr=''):
            if isinstance(x, dict):
                urls = {k: v for k, v in x.items() if k in ['url', 'final_url'] and isinstance(v, str) and v.startswith(('https://', 'http://'))}
                if urls:
                    for field in ['sha256', 'html_sha256', 'article_body_sha256']:
                        if isinstance(x.get(field), str) and x[field] in hashes:
                            sources.append(dict(catalog=item['path'], json_pointer=ptr, digest_pointer=ptr + '/' + field,
                                                source_sha256=x[field], URL_fields=urls, record=x,
                                                basis='explicit URL and retained article-body HTML hash, not full captured response' if field == 'article_body_sha256' else 'explicit URL and exact retained HTML content hash'))
                    if isinstance(x.get('files'), dict):
                        for name, value in x['files'].items():
                            digest = value if isinstance(value, str) else value.get('sha256') if isinstance(value, dict) else None
                            if name.endswith('.html') and digest in hashes:
                                sources.append(dict(catalog=item['path'], json_pointer=ptr,
                                                    digest_pointer=ptr + '/files/' + escape(name) + ('' if isinstance(value, str) else '/sha256'),
                                                    source_sha256=digest, URL_fields=urls, record=x,
                                                    basis='explicit URL with nested named HTML hash'))
                if isinstance(x.get('files'), dict):
                    for name, record in x['files'].items():
                        digest = record if isinstance(record, str) else record.get('sha256') if isinstance(record, dict) else None
                        if not name.endswith('.html') or digest not in hashes: continue
                        target = (path.parent / name).resolve()
                        try: relative = str(target.relative_to(ROOT))
                        except ValueError: continue
                        if relative in html_paths:
                            assert sha(target.read_bytes()) == digest
                            bindings.append(dict(catalog=item['path'], json_pointer=ptr + '/files/' + escape(name),
                                                 declared_file=name, path=relative, sha256=digest, record=record,
                                                 path_resolution='named files entry relative to catalog directory'))
                for k, v in x.items(): visit(v, ptr + '/' + escape(k))
            elif isinstance(x, list):
                for i, v in enumerate(x): visit(v, ptr + '/' + str(i))
        visit(data)
    return sources, bindings


def build():
    tests = selfchecks()
    inputs = read(P / 'html-inputs.json')
    assert len(inputs) == len({r['path'] for r in inputs}) == 134
    assert [r['path'] for r in inputs] == sorted(r['path'] for r in inputs)
    hashes = {r['sha256'] for r in inputs}
    assert len(hashes) == 109
    metadata = read(P / 'metadata-inputs.json')
    assert len(metadata) == len({r['path'] for r in metadata}) == 148
    source_records, manifest_bindings = catalog_records(metadata, hashes, {r['path'] for r in inputs})
    assert source_records == read(P / 'source-records.json') and manifest_bindings == read(P / 'manifest-bindings.json')
    catalogs = {r['path']: read(ROOT / r['path']) for r in metadata}
    for record in source_records:
        assert at_pointer(catalogs[record['catalog']], record['json_pointer']) == record['record']
        assert at_pointer(catalogs[record['catalog']], record['digest_pointer']) == record['source_sha256']
        assert record['URL_fields'] == {k: record['record'][k] for k in record['URL_fields']}
    for record in manifest_bindings:
        assert at_pointer(catalogs[record['catalog']], record['json_pointer']) == record['record']
    baseline = read(P / 'baseline-inputs.json')
    for record in baseline: pin(ROOT / record['path'], record)
    expected_pins = {}
    for group, rows in [('physical-HTML', inputs), ('metadata-catalog', metadata), ('original-baseline', baseline)]:
        for row in rows:
            if row['path'] in expected_pins:
                assert expected_pins[row['path']]['sha256'] == row['sha256'] and expected_pins[row['path']]['bytes'] == row['bytes']
                expected_pins[row['path']]['roles'].append(group)
            else:
                expected_pins[row['path']] = dict(path=row['path'], bytes=row['bytes'], sha256=row['sha256'], roles=[group])
    assert read(P / 'input-pins.json') == [expected_pins[k] for k in sorted(expected_pins)]
    toc = read(BASE / 'inventory/manual-toc.json')
    assert sha((BASE / 'inventory/manual-toc.json').read_bytes()) == '1ca19a34ad1c0e97a9dd6582d2f7ebf06c5a16ae9d2bd64c26baab5c0eb46e98'
    assert sha((BASE / 'inventory/manual-12-toc-2026-10-19.html').read_bytes()) == '584d4b61d119c96ecdb7941ef34ac9d4e0282a3e40c8bc474b6cf24892640d80'
    original_manifest = read(BASE / 'inventory/manifest.json')
    for name in ['manual-toc.json', 'manual-12-toc-2026-10-19.html']:
        pin(BASE / 'inventory' / name, original_manifest['files'][name])
    assert len(toc) == len({r['id'] for r in toc}) == len({r['url'] for r in toc}) == 880
    assert sum(r['leaf'] for r in toc) == 708
    original_chapters = [r for r in toc if '.' not in r['number']]
    assert len(original_chapters) == 43
    by_toc_url = {r['url']: (i, r) for i, r in enumerate(toc)}
    content = {}
    paths = []
    for physical in inputs:
        raw = pin(ROOT / physical['path'], physical)
        parsed = parse(raw)
        assert parsed['canonical'] == physical['canonical']
        assert parsed['chapter_boundary'] == physical['chapter_boundary']
        assert parsed['document_title'] == physical['title']
        digest = physical['sha256']
        refs = [i for i, record in enumerate(source_records) if record['source_sha256'] == digest]
        explicit_urls = sorted({u for i in refs for u in source_records[i]['URL_fields'].values()})
        english = sorted(set(parsed['english_alternate_urls']))
        canonical = sorted(set(parsed['canonical']))
        self_urls = canonical or english
        corroborated = [u for u in self_urls if u in explicit_urls]
        reasons = []
        selected_url = None
        if len(parsed['chapter_boundary']) != 1 or parsed['closed_chapter_boundaries'] != 1:
            reasons.append('not-one-complete-chapter_content-boundary')
        if parsed['issues']: reasons.append('chapter-parser-structural-issues')
        if not parsed['headings']: reasons.append('no-actual-numbered-heading-in-chapter_content')
        if len(self_urls) != 1: reasons.append('missing-or-ambiguous-explicit-HTML-self-URL')
        elif not self_urls[0].startswith('https://www.ableton.com/en/live-manual/12/'):
            reasons.append('explicit-self-URL-not-official-English-Version12-manual')
        elif len(corroborated) != 1:
            reasons.append('Version12-HTML-self-URL-not-corroborated-by-retained-source-catalog-hash')
        else:
            selected_url = corroborated[0]
        selected = not reasons
        excluded_family = None
        if not selected:
            if any(u.startswith('https://www.ableton.com/en/live-manual/11/') for u in self_urls):
                excluded_family = 'official-Version11-manual-not-Version12'
            elif any(u.startswith('https://docs.cycling74.com/') for u in explicit_urls):
                excluded_family = 'public-Max-API-nonmanual-chapter'
            elif any(u.startswith('https://help.ableton.com/') for u in explicit_urls):
                excluded_family = 'Help-article-body-or-response-not-manual-chapter'
            else:
                excluded_family = 'unresolved-nonchapter-HTML-identity'
        source_id = 'HTML-SHA256-' + digest
        path_row = dict(physical, content_id=source_id, selection='selected-Version12-chapter' if selected else 'excluded',
                        exclusion_reasons=reasons, excluded_family=excluded_family, explicit_HTML_self_URLs=self_urls,
                        HTML_self_URL_basis='canonical link' if canonical else 'English alternate link' if english else 'unavailable',
                        matching_source_record_pointers=['/' + str(i) for i in refs],
                        matching_physical_manifest_binding_pointers=['/' + str(i) for i, r in enumerate(manifest_bindings) if r['path'] == physical['path']],
                        chapter_URL=selected_url if selected else None,
                        source_catalog_URLs=explicit_urls, parser_issues=parsed['issues'])
        paths.append(path_row)
        if not selected: continue
        if digest in content:
            assert content[digest]['chapter_URL'] == selected_url and content[digest]['headings'] == parsed['headings']
            content[digest]['physical_paths'].append(physical['path'])
            continue
        matching = [i for i in refs if selected_url in source_records[i]['URL_fields'].values()]
        # Dates remain asserted source-record data. Missing UTC stays unknown; no filesystem dates.
        timestamps, versions = [], []
        for i in matching:
            record = source_records[i]['record']
            for key in ['capture_utc', 'captured_utc', 'capture_date', 'captured', 'date']:
                if key in record:
                    value = record[key]
                    try:
                        dt = datetime.fromisoformat(value)
                        UTC = key in ['capture_utc', 'captured_utc'] and dt.utcoffset() is not None and dt.utcoffset().total_seconds() == 0
                    except (ValueError, TypeError):
                        UTC = False
                    timestamps.append(dict(source_record_pointer='/' + str(i), field=key, value=value,
                                           explicit_UTC_ISO8601=UTC))
            for key in ['version', 'declared_version', 'edition', 'publication_revision', 'applicability']:
                if key in record: versions.append(dict(source_record_pointer='/' + str(i), field=key, value=record[key]))
        content[digest] = dict(id=source_id, sha256=digest, bytes=len(raw), chapter_URL=selected_url,
                               physical_paths=[physical['path']], source_record_pointers=['/' + str(i) for i in matching],
                               source_version_assertions=versions, capture_time_assertions=timestamps,
                               capture_UTC_status='assertions retained individually; no authority or recapture time selected' if any(t['explicit_UTC_ISO8601'] for t in timestamps) else 'unknown: no explicit capture UTC resolved',
                               document_title=parsed['document_title'], chapter_boundary=parsed['chapter_boundary'],
                               ignored_non_numeric_or_unnumbered_headings=parsed['ignored_non_numeric_or_unnumbered_headings'],
                               headings=parsed['headings'], target_applicability='U', semantic_coverage='unknown')
    captures = sorted(content.values(), key=lambda c: (c['chapter_URL'], c['sha256']))
    heading_rows = []
    for capture in captures:
        nonleaves = {i for h in capture['headings'] for i in h['preceding_actual_numbered_ancestors']}
        for h in capture['headings']:
            url = capture['chapter_URL'] + '#' + h['id'] if h['id'] else None
            matched = by_toc_url.get(url)
            heading_rows.append(dict(capture=capture['id'], source_sha256=capture['sha256'],
                                     physical_paths=capture['physical_paths'], chapter_URL=capture['chapter_URL'],
                                     heading=h, numbered_outline_leaf=h['index'] not in nonleaves, exact_heading_URL=url,
                                     original_TOC_pointer='/' + str(matched[0]) if matched else None,
                                     original_TOC_id=matched[1]['id'] if matched else None,
                                     exact_TOC_URL_match=bool(matched),
                                     number_comparison='equal' if matched and matched[1]['number'] == h['number'] else 'different' if matched else 'no-exact-TOC-URL',
                                     title_comparison='equal' if matched and matched[1]['title'] == h['title'] else 'different' if matched else 'no-exact-TOC-URL',
                                     target_applicability='U', semantic_coverage='unknown', complete=False))
    by_url = defaultdict(list)
    for i, h in enumerate(heading_rows):
        if h['exact_heading_URL'] is not None: by_url[h['exact_heading_URL']].append(i)
    topic_rows = [dict(original_topic=r, heading_pointers=['/' + str(i) for i in by_url[r['url']]],
                       captured_heading_status='exact-URL-heading-present' if by_url[r['url']] else 'no-exact-heading-in-frozen-captures',
                       target_applicability='U', semantic_coverage='unknown', complete=False) for r in toc]
    assert [r['original_topic'] for r in topic_rows] == toc
    availability = []
    for chapter in original_chapters:
        url = chapter['url'].partition('#')[0]
        refs = [i for i, c in enumerate(captures) if c['chapter_URL'] == url]
        availability.append(dict(original_chapter=chapter, exact_chapter_URL=url,
                                 capture_pointers=['/' + str(i) for i in refs],
                                 capture_status='retained-selected-chapter-bytes' if refs else 'no-selected-capture-in-this-frozen-input-set',
                                 target_applicability='U', semantic_coverage='unknown', complete=False))
    duplicates = []
    for capture in captures:
        for field in ['id', 'number']:
            values = defaultdict(list)
            for h in capture['headings']: values[h[field]].append(h['index'])
            for value, positions in values.items():
                if value is not None and len(positions) > 1:
                    duplicates.append(dict(capture=capture['id'], field=field, value=value, heading_indices=positions))
    conflicts = []
    for url, positions in sorted(by_url.items()):
        signatures = {(heading_rows[i]['heading']['number'], heading_rows[i]['heading']['tag'], heading_rows[i]['heading']['title']) for i in positions}
        if len(signatures) > 1:
            conflicts.append(dict(exact_URL=url, heading_pointers=['/' + str(i) for i in positions],
                                  status='distinct-retained-observations-no-authority-selected'))
    url_captures = defaultdict(list)
    for i, c in enumerate(captures): url_captures[c['chapter_URL']].append(i)
    variants = [dict(chapter_URL=url, capture_pointers=['/' + str(i) for i in positions],
                     status='distinct-content-hashes-retained-separately-no-latest-selection')
                for url, positions in sorted(url_captures.items()) if len(positions) > 1]
    extras = [dict(heading_pointer='/' + str(i), **h) for i, h in enumerate(heading_rows) if not h['exact_TOC_URL_match']]
    comparison = dict(extra_heading_occurrences=extras,
                      original_topics_with_no_exact_captured_heading=[dict(original_TOC_pointer='/' + str(i), original_topic=r['original_topic']) for i, r in enumerate(topic_rows) if not r['heading_pointers']],
                      matched_URL_number_differences=[dict(heading_pointer='/' + str(i), **h) for i, h in enumerate(heading_rows) if h['number_comparison'] == 'different'],
                      matched_URL_title_differences=[dict(heading_pointer='/' + str(i), **h) for i, h in enumerate(heading_rows) if h['title_comparison'] == 'different'],
                      duplicate_heading_ids_or_numbers_within_capture=duplicates,
                      same_URL_distinct_content_variants=variants, same_heading_URL_conflicting_observations=conflicts,
                      comparison='Literal source chapter URL plus actual heading id only; no aliases, URL normalization, title/number/parent matching or semantic disposition')
    for row in heading_rows:
        if row['original_TOC_pointer']:
            original_row = at_pointer(toc, row['original_TOC_pointer'])
            assert original_row['id'] == row['original_TOC_id'] and original_row['url'] == row['exact_heading_URL']
    for row in availability:
        assert all(at_pointer(captures, pointer)['chapter_URL'] == row['exact_chapter_URL'] for pointer in row['capture_pointers'])
    assert len(paths) == 134 and len(captures) == 44 and len(heading_rows) == 1088 and len(by_url) == 1066
    assert len(extras) == 186 and len(variants) == 1
    summary = dict(scope='Finite captured Version12 actual numbered-heading discovery only; no behavioral or leaf completion',
                   frozen_physical_HTML_inputs=len(inputs), unique_input_HTML_content_hashes=len(hashes),
                   selected_physical_chapter_HTML_paths=sum(r['selection'] == 'selected-Version12-chapter' for r in paths),
                   excluded_physical_HTML_paths=sum(r['selection'] == 'excluded' for r in paths),
                   excluded_physical_HTML_families=dict(Counter(r['excluded_family'] for r in paths if r['excluded_family'])),
                   excluded_reason_occurrences=dict(Counter(reason for r in paths for reason in r['exclusion_reasons'])),
                   selected_unique_content_captures=len(captures), selected_distinct_chapter_URLs=len(url_captures),
                   selected_duplicate_physical_bindings=sum(len(c['physical_paths']) - 1 for c in captures),
                   distinct_content_same_URL_groups=len(variants),
                   actual_numbered_heading_occurrences_across_unique_content_captures=len(heading_rows),
                   distinct_literal_actual_heading_URLs=len(by_url), heading_tags=dict(Counter(h['heading']['tag'] for h in heading_rows)),
                   actual_numbered_outline_leaf_occurrences=sum(h['numbered_outline_leaf'] for h in heading_rows),
                   actual_numbered_outline_nonleaf_occurrences=sum(not h['numbered_outline_leaf'] for h in heading_rows),
                   distinct_actual_numbered_outline_leaf_URLs=len({h['exact_heading_URL'] for h in heading_rows if h['numbered_outline_leaf'] and h['exact_heading_URL']}),
                   original_TOC_leaf_URLs_with_actual_numbered_outline_children=len({h['exact_heading_URL'] for h in heading_rows if h['exact_TOC_URL_match'] and not h['numbered_outline_leaf'] and toc[int(h['original_TOC_pointer'][1:])]['leaf']}),
                   original_TOC_rows_preserved=880, original_TOC_leaves_preserved=708, original_TOC_chapters_preserved=43,
                   original_chapter_URLs_with_selected_capture=sum(bool(r['capture_pointers']) for r in availability),
                   original_chapter_URLs_without_selected_capture=sum(not r['capture_pointers'] for r in availability),
                   original_TOC_topics_with_exact_actual_heading=sum(bool(r['heading_pointers']) for r in topic_rows),
                   original_TOC_topics_without_exact_actual_heading=sum(not r['heading_pointers'] for r in topic_rows),
                   exact_TOC_heading_match_occurrences=sum(h['exact_TOC_URL_match'] for h in heading_rows),
                   extra_actual_heading_occurrences=len(extras), distinct_extra_actual_heading_URLs=len({h['exact_heading_URL'] for h in extras if h['exact_heading_URL']}),
                   matched_URL_number_differences=len(comparison['matched_URL_number_differences']), matched_URL_title_differences=len(comparison['matched_URL_title_differences']),
                   same_heading_URL_conflicting_observations=len(conflicts), within_capture_duplicate_ID_or_number_groups=len(duplicates),
                   heading_context_flag_occurrences=dict(Counter(flag for h in heading_rows for flag in h['heading']['flags'])),
                   selected_captures_without_resolved_capture_UTC=sum(c['capture_UTC_status'].startswith('unknown') for c in captures),
                   selected_ignored_non_numeric_or_unnumbered_headings=sum(c['ignored_non_numeric_or_unnumbered_headings'] for c in captures),
                   metadata_catalog_files=len(metadata), source_URL_hash_records=len(source_records), physical_manifest_bindings=len(manifest_bindings),
                   unique_external_input_pins=len(expected_pins),
                   physical_HTML_paths_with_explicit_manifest_bindings=len({r['path'] for r in manifest_bindings}),
                   physical_HTML_paths_with_source_catalog_content_hash=sum(bool(r['matching_source_record_pointers']) for r in paths),
                   complete_topics_claimed=0, complete_leaves_claimed=0, full_product_denominator='unknown; original TOC is an open discovery baseline',
                   target_applicability='U', all_source_variants_retained=True, paragraphs_read_for_this_census=False,
                   original_API_script_native_runtime_network_candidate_execution=False, parser_selfchecks=tests)
    return {'html-classifications.json': paths, 'captures.json': captures, 'heading-ledger.json': heading_rows,
            'original-TOC-comparison.json': topic_rows, 'chapter-availability.json': availability,
            'differences.json': comparison, 'summary.json': summary}


before = {str(f.relative_to(P)): sha(f.read_bytes()) for f in P.rglob('*') if f.is_file()} if CHECK else None
external_before = {r['path']: sha(pin(ROOT / r['path'], r)) for r in read(P / 'input-pins.json')} if CHECK else None
outputs = build()
for name, value in outputs.items():
    raw = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    if CHECK:
        assert (P / name).read_bytes() == raw, name
    else:
        assert not (P / name).exists(), 'Refuse rewriting generated census output: ' + name
        (P / name).write_bytes(raw)
if CHECK:
    manifest = read(P / 'manifest.json')
    assert set(before) == set(manifest['files']) | {'manifest.json'}
    for name, record in manifest['files'].items(): pin(P / name, record)
    for path in P.iterdir():
        if path.suffix in ['.json', '.py', '.md']:
            result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
            assert result.returncode in (0, 1) and not result.stdout and not result.stderr, path
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', (P / 'README.md').read_text()):
        if re.match(r'[A-Za-z]+:', target): continue
        name, _, fragment = target.partition('#')
        path = (P / name).resolve() if name else P / 'README.md'
        assert path.exists(), target
        if fragment:
            headings = re.findall(r'^#+\s+(.+)$', path.read_text(), re.M)
            assert fragment in {re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-') for h in headings}, target
    assert before == {str(f.relative_to(P)): sha(f.read_bytes()) for f in P.rglob('*') if f.is_file()}
    assert external_before == {r['path']: sha(pin(ROOT / r['path'], r)) for r in read(P / 'input-pins.json')}
print(json.dumps(dict(status='pass', writes=not CHECK, **outputs['summary.json']), indent=2))
