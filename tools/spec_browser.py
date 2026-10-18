#!/usr/bin/env python3
"""Build one searchable page of every behavioral requirement and candidate requirement in the wiki.

Usage: python3 tools/spec_browser.py [--out DIR]

Sources: `### REQ-…` sections of draft specs in wiki/specs/, and the table rows under any
`## Candidate requirements …` heading in wiki/research/. Each row links back to its source
section; Markdown links inside cells are resolved relative to the output page. Reads Markdown
only and writes a static page (search works with JavaScript; the full table shows without it).
"""
import argparse
import html
import os
from pathlib import Path
import re
import sys

from build_artifact_browser import STYLE

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/ableton-live-12.4.3/browse/specs'
LINK = re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)')


def anchor(heading):
    return re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')


def frontmatter(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    return dict(line.split(': ', 1) for line in m.group(1).splitlines() if ': ' in line) if m else {}


def cells(row):
    return [c.strip() for c in re.split(r'(?<!\\)\|', row.strip().strip('|'))]


def spec_rows(path, text):
    """One row per `### REQ-… — title` section or `| REQ-… |` table row of a draft spec."""
    meta, rows = frontmatter(text), []
    target, status = meta.get('id', path.stem), meta.get('status', '')
    parts = re.split(r'^### ', text, flags=re.M)
    for part in parts[1:]:
        heading, _, body = part.partition('\n')
        m = re.match(r'(REQ-[A-Z0-9-]+)\s*[—-]\s*(.*)', heading)
        if not m:
            continue
        body = body.split('\n## ')[0].split('\n### ')[0].strip()
        rows.append({'id': m.group(1), 'statement': f'{m.group(2)}: ' + ' '.join(body.split())[:600], 'evidence': '',
                     'strength': status, 'target': target, 'kind': 'Draft spec', 'source': (path, anchor(heading))})
    section = ''
    for line in text.splitlines():
        if line.startswith('#'):
            section = anchor(line.lstrip('#'))
        c = cells(line) if line.startswith('|') else []
        if c and re.fullmatch(r'REQ-[A-Z0-9-]+', c[0]):
            rows.append({'id': c[0], 'statement': c[1] if len(c) > 1 else '', 'evidence': c[2] if len(c) > 2 else '',
                         'strength': status, 'target': target, 'kind': 'Draft spec', 'source': (path, section)})
    unique = {}
    for r in rows:
        unique.setdefault(r['id'], r)  # a REQ with both a heading and a table row is listed once
    return list(unique.values())


def candidate_rows(path, text):
    """Table rows under every `## Candidate requirements …` heading of a research page."""
    rows = []
    for m in re.finditer(r'^## (Candidate requirements[^\n]*)\n(.*?)(?=^## |\Z)', text, re.M | re.S):
        heading, body = m.group(1), m.group(2)
        named = re.search(r'SPEC-[A-Z0-9-]+', heading) or re.search(r'for (.*)', heading)
        target = named.group(0) if named else heading
        table = [cells(line) for line in body.splitlines() if line.startswith('|')]
        for c in table[2:]:  # skip header and separator
            if len(c) >= 2 and c[0]:
                rows.append({'id': c[0], 'statement': c[1], 'evidence': c[2] if len(c) > 2 else '',
                             'strength': c[3] if len(c) > 3 else '', 'target': target.replace('for ', ''),
                             'kind': 'Candidate', 'source': (path, anchor(heading))})
    return rows


def render(cell, page_dir, out):
    """Escape a Markdown cell, keeping its links (relative ones re-based to the output page)."""
    pieces, last = [], 0
    for m in LINK.finditer(cell):
        pieces.append(html.escape(cell[last:m.start()]))
        url = m.group(2)
        if not re.match(r'[a-z]+:', url):
            path, _, frag = url.partition('#')
            url = os.path.relpath((page_dir / path).resolve(), out) if path else ''
            url += f'#{frag}' if frag else ''
        pieces.append(f'<a href="{html.escape(url)}">{html.escape(m.group(1))}</a>')
        last = m.end()
    pieces.append(html.escape(cell[last:]))
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', ''.join(pieces))


def collect(root):
    rows = []
    for path in sorted((root / 'wiki/specs').glob('*.md')):
        text = path.read_text()
        if frontmatter(text).get('type') == 'spec':  # plans and indexes cite REQ IDs without defining them
            rows += spec_rows(path, text)
    for path in sorted((root / 'wiki/research').glob('*.md')):
        rows += candidate_rows(path, path.read_text())
    return rows


def build(root, out):
    rows = collect(root)
    out.mkdir(parents=True, exist_ok=True)
    targets = sorted({r['target'] for r in rows})
    body = []
    for r in rows:
        path, frag = r['source']
        link = f'<a href="{html.escape(os.path.relpath(path, out))}#{frag}">{html.escape(path.relative_to(root).as_posix())}</a>'
        search = ' '.join([r['id'], r['statement'], r['evidence'], r['strength'], r['target'], r['kind']]).lower()
        body.append(f'<tr data-search="{html.escape(search)}" data-target="{html.escape(r["target"])}" data-kind="{r["kind"]}">'
                    f'<td><code>{html.escape(r["id"])}</code></td><td>{html.escape(r["target"])}<br><small>{r["kind"]}</small></td>'
                    f'<td>{render(r["statement"], path.parent, out)}</td><td>{render(r["evidence"], path.parent, out)}</td>'
                    f'<td>{render(r["strength"], path.parent, out)}</td><td>{link}</td></tr>')
    options = ''.join(f'<option value="{html.escape(t)}">{html.escape(t)} ({sum(r["target"] == t for r in rows)})</option>' for t in targets)
    (out / 'index.html').write_text(PAGE.format(style=STYLE, total=len(rows), options=options, rows=''.join(body),
                                                index=html.escape(os.path.relpath(root / 'wiki/specs/index.md', out))), encoding='utf-8')
    return rows


PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>Requirements browser</title><style>{style}
td{{font-size:.88rem}}td:first-child{{white-space:nowrap}}</style></head>
<body><main><header><div class="eyebrow">Analyst workspace · Behavioral requirements</div><h1>Requirements and candidates</h1>
<p class="lead">Every requirement in a draft spec and every candidate requirement proposed by a research packet, in one table. <strong>Candidates</strong> are statements a packet found support for in shipped files or decompiled code; they are not yet draft specs and none is released. Released subsets are listed in the handoff index. Each row links to its source section, which owns the evidence and limits.</p>
<p><a href="{index}">Specification index (wiki)</a></p></header>
<section><div class="controls"><div><label for="q">Search</label><input id="q" type="search" placeholder="ID, word or file"></div>
<div><label for="t">Target</label><select id="t"><option value="">All targets</option>{options}</select></div>
<div><label for="k">Kind</label><select id="k"><option value="">All</option><option>Draft spec</option><option>Candidate</option></select></div></div>
<p id="count" role="status" aria-live="polite">{total} rows</p>
<div class="table-wrap"><table><thead><tr><th>ID</th><th>Target</th><th>Statement</th><th>Evidence</th><th>Status or strength</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<p class="muted">Regenerate with <code>python3 tools/spec_browser.py</code>. Static evidence does not establish runtime behavior; see each source page.</p></main>
<script>
(() => {{
  const q = document.getElementById('q'), t = document.getElementById('t'), k = document.getElementById('k');
  const rows = [...document.querySelectorAll('tr[data-search]')];
  const apply = () => {{
    const terms = q.value.toLowerCase().trim().split(/\\s+/).filter(Boolean); let n = 0;
    for (const r of rows) {{ const ok = terms.every(x => r.dataset.search.includes(x)) && (!t.value || r.dataset.target === t.value) && (!k.value || r.dataset.kind === k.value);
      r.hidden = !ok; n += ok; }}
    document.getElementById('count').textContent = `${{n}} of ${{rows.length}} rows`;
  }};
  for (const c of [q, t, k]) c.addEventListener('input', apply);
}})();
</script></body></html>
'''


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', type=Path, default=OUT)
    args = parser.parse_args(argv)
    rows = build(ROOT, args.out.resolve())
    by_target = {}
    for r in rows:
        by_target[r['target']] = by_target.get(r['target'], 0) + 1
    print({'out': str(args.out / 'index.html'), 'rows': len(rows), 'by_target': by_target})
    return 0


if __name__ == '__main__':
    sys.exit(main())
