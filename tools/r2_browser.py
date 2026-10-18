#!/usr/bin/env python3
"""Build an offline browser for one verified R2BulkDecompile corpus and its R2ExportIndexes.

Usage: python3 tools/r2_browser.py CORPUS INDEXES OUT [--title TEXT]

Reads JSONL only; never opens a Ghidra project or runs a target. CORPUS and INDEXES must pass
r2_corpus.py checks and name the same program, or nothing is written. OUT is replaced as a whole
and must be absent or a previous r2 browser. Chunks are read one at a time and published as
on-demand chunks/chunk-NNNNN.js files; the page loads only functions.js (one row per committed
function) until a function is opened. Output is deterministic for unchanged inputs.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import shutil
import sys

from build_artifact_browser import STYLE, escape
import r2_corpus

SCHEMA = 'r2-corpus-browser-v1'
# ponytail: per-function lists capped at LIST_CAP; raise it if hub functions need full lists.
LIST_CAP = 200


def js_assign(target, value):
    # Data scripts are trusted local code; escape HTML-significant characters as a safeguard.
    text = json.dumps(value, ensure_ascii=True, separators=(',', ':'), sort_keys=True)
    return target + '=' + text.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026') + ';\n'


def lines(path):
    with path.open('rb') as stream:
        for line in stream:
            yield json.loads(line)


def capped(items):
    return {'items': items[:LIST_CAP], 'total': len(items)}


def load_indexes(indexes):
    """Group the C2 index files by function entry; returns per-function relation lists and aliases."""
    rel = defaultdict(lambda: defaultdict(list))
    for c in lines(indexes / 'calls.jsonl'):
        resolved = c['callee_resolved']
        rel[c['caller']]['callees'].append([c['site'], c['callee'], c['callee_name'], c['kind'], c['callee_resolved_name'] or resolved])
        rel[c['callee']]['callers'].append([c['site'], c['caller'], c['caller_name'], c['kind']])
        if resolved and resolved != c['callee']:
            rel[resolved]['callers'].append([c['site'], c['caller'], c['caller_name'], c['kind'] + ' via thunk'])
    for s in lines(indexes / 'strings.jsonl'):
        for r in s['refs']:
            users = [r['function']] if r['function'] else [v['function'] for v in r.get('via', []) if v.get('function')]
            for user in users:
                rel[user]['strings'].append([s['address'], r['from'], s['value'][:300]])
    for i in lines(indexes / 'indirect.jsonl'):
        rel[i['function']]['indirect'].append([i['site'], i['instruction'], i['resolved_targets']])
    # Mangled C++ aliases duplicate the demangled name and would dominate the one-file search index;
    # they remain in aliases.jsonl. ponytail: single functions.js; shard it by entry prefix if a corpus
    # index grows past what a browser loads comfortably (~100 MB).
    aliases = {a['entry']: sorted({s['name'] for s in a['symbols'] if not s['name'].startswith(('_Z', '__Z'))} - {a['name']})
               for a in lines(indexes / 'aliases.jsonl')}
    return rel, aliases


def build(corpus, indexes, out, title):
    summary = r2_corpus.check_corpus(corpus)
    r2_corpus.check_indexes(indexes)
    run_bytes = (corpus / 'run.json').read_bytes()
    run = json.loads(run_bytes)
    index_manifest_bytes = (indexes / 'manifest.json').read_bytes()
    index_manifest = json.loads(index_manifest_bytes)
    if (index_manifest['program'], index_manifest['executable_sha256']) != (run['program'], run['executable_sha256']):
        raise r2_corpus.CheckError('Indexes and corpus describe different programs')
    if out.exists() and not (out / 'manifest.json').is_file():
        raise r2_corpus.CheckError(f'{out} exists and is not an r2 browser; refusing to replace it')
    if out.exists() and json.loads((out / 'manifest.json').read_text()).get('schema') != SCHEMA:
        raise r2_corpus.CheckError(f'{out} is a different kind of output; refusing to replace it')
    rel, aliases = load_indexes(indexes)
    staging = out.with_name(out.name + '.building')
    shutil.rmtree(staging, ignore_errors=True)
    (staging / 'chunks').mkdir(parents=True)
    rows, outputs = [], {}

    def write(name, text):
        data = text.encode('utf-8')
        (staging / name).write_bytes(data)
        outputs[name] = hashlib.sha256(data).hexdigest()

    for k in range(run['chunk_count']):
        path = corpus / 'chunks' / f'chunk-{k:05d}.jsonl'
        if not path.exists():
            continue
        functions = []
        for r in lines(path):
            links = rel.get(r['entry'], {})
            functions.append({**{key: r[key] for key in ('entry', 'name', 'thunk', 'body_bytes', 'body_ranges', 'signature',
                                                          'state', 'error', 'timed_out', 'partial_code', 'warnings', 'ms', 'code')},
                              **{key: capped(links.get(key, [])) for key in ('callers', 'callees', 'strings', 'indirect')}})
            rows.append([r['entry'], r['name'], r['state'], k, len(r['warnings']), aliases.get(r['entry'], [])])
        write(f'chunks/chunk-{k:05d}.js', f'window.r2Chunks=window.r2Chunks||{{}};' + js_assign(f'window.r2Chunks[{k}]', functions))
    write('functions.js', js_assign('window.r2Index', rows))
    counts = summary['counts']
    count_items = ''.join(f'<li>{escape(state)}: {n:,}</li>' for state, n in counts.items())
    states = ''.join(f'<option value="{escape(s)}">{escape(s)}</option>' for s in sorted(counts) if s != 'pending')
    pending = counts.get('pending', 0)
    write('index.html', PAGE.format(
        style=STYLE, title=escape(title), program=escape(run['program']), sha=escape(run['executable_sha256']),
        language=escape(run['language']), ghidra=escape(run['ghidra_version']), eligible=f"{run['eligible']:,}",
        rows=f'{len(rows):,}', counts=count_items, states=states, cap=LIST_CAP,
        pending=f'<p class="notice">{pending:,} eligible functions are in chunks not yet committed; they are not listed.</p>' if pending else '',
        script=SCRIPT))
    manifest = {
        'schema': SCHEMA, 'title': title, 'program': run['program'], 'executable_sha256': run['executable_sha256'],
        'generator': {'path': 'tools/r2_browser.py', 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'inputs': {'run.json': hashlib.sha256(run_bytes).hexdigest(),
                   'coverage.json': hashlib.sha256((corpus / 'coverage.json').read_bytes()).hexdigest(),
                   'indexes/manifest.json': hashlib.sha256(index_manifest_bytes).hexdigest()},
        'counts': counts, 'listed_functions': len(rows), 'list_cap': LIST_CAP, 'outputs': dict(sorted(outputs.items())),
        'scope': 'Navigation view of verified R2 JSONL; no target analysis. Static references do not establish runtime execution.',
    }
    (staging / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    if out.exists():
        shutil.rmtree(out)
    staging.rename(out)
    write_catalog(out.parent)
    return manifest


def write_catalog(parent):
    """List every r2 browser directory beside OUT in r2-index.html."""
    rows = []
    for manifest_path in sorted(parent.glob('*/manifest.json')):
        m = json.loads(manifest_path.read_text())
        if m.get('schema') != SCHEMA:
            continue
        counts = ', '.join(f'{state} {n:,}' for state, n in m['counts'].items())
        rows.append(f'<tr><td><a href="{escape(manifest_path.parent.name)}/index.html">{escape(m["title"])}</a></td>'
                    f'<td><code>{escape(m["program"])}</code></td><td>{m["listed_functions"]:,}</td><td>{escape(counts)}</td></tr>')
    (parent / 'r2-index.html').write_text(CATALOG.format(style=STYLE, rows=''.join(rows)), encoding='utf-8')


CATALOG = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>Revision 2 corpus browsers</title><style>{style}</style></head>
<body><main><header><div class="eyebrow">Analyst workspace · Revision 2</div><h1>Decompiled corpus browsers</h1>
<p class="lead">One offline browser per verified R2BulkDecompile corpus. Regenerate with <code>python3 tools/r2_browser.py CORPUS INDEXES OUT</code>.</p></header>
<section><div class="table-wrap"><table><thead><tr><th>Browser</th><th>Program</th><th>Functions listed</th><th>States</th></tr></thead><tbody>{rows}</tbody></table></div></section></main></body></html>
'''


PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>{title}</title><style>{style}
pre{{background:var(--wash);border:1px solid var(--line);border-radius:6px;padding:14px;overflow:auto;font-size:.85rem;line-height:1.45}}
.rel li{{margin:3px 0;overflow-wrap:anywhere}}#detail h2{{scroll-margin-top:12px}}</style></head>
<body><main>
<header><div class="eyebrow">Analyst workspace · Revision 2 corpus browser</div><h1>{title}</h1>
<p class="lead">Ghidra {ghidra} decompiler output for <code>{program}</code> ({language}), SHA-256 <code>{sha}</code>. Pseudocode approximates compiled behavior; it is not original source. Callers, callees and string references are static references, not observed execution.</p></header>
<section id="coverage"><h2>Coverage</h2><p>{eligible} eligible functions; {rows} listed. Failed attempts stay failures.</p><ul>{counts}</ul>{pending}<p><a href="manifest.json">Generated-view manifest</a> pins the corpus and index inputs.</p></section>
<section id="list"><h2>Functions</h2><noscript><p>This browser needs JavaScript to read its local index files.</p></noscript>
<div class="controls"><div><label for="r2-search">Search entry, name or symbol</label><input id="r2-search" type="search" placeholder="For example: 0x100004bb0 or qt_plugin"></div><div><label for="r2-state">State</label><select id="r2-state"><option value="">All states</option>{states}</select></div></div>
<p id="r2-count" role="status" aria-live="polite"></p><button id="r2-prev" type="button">Previous 100</button> <button id="r2-next" type="button">Next 100</button>
<div class="table-wrap"><table><caption>At most 100 rows shown; open a function to read its code</caption><thead><tr><th>Entry</th><th>Name</th><th>State</th><th>Warnings</th></tr></thead><tbody id="r2-rows"></tbody></table></div></section>
<section id="detail" hidden><p><a href="#list" id="r2-back">Back to the function list</a></p><h2 id="r2-heading" tabindex="-1"></h2><p id="r2-status" role="status" aria-live="polite"></p><div id="r2-body"></div><p class="muted">Lists show at most {cap} items each.</p></section>
</main><script src="functions.js"></script><script>{script}</script></body></html>
'''

SCRIPT = r"""
(() => {
  'use strict';
  const all = window.r2Index || [], byEntry = new Map(all.map((row, i) => [row[0], i]));
  const text = all.map(row => [row[0], row[1], row[2], ...row[5]].join(' ').toLowerCase());
  const $ = id => document.getElementById(id), pageSize = 100, loading = new Map();
  let matches = all.map((_, i) => i), page = 0;
  const el = (tag, content) => { const node = document.createElement(tag); if (content !== undefined) node.textContent = content; return node; };
  const fnLink = (entry, label) => {
    if (!byEntry.has(entry)) return el('span', label);
    const a = el('a', label); a.href = '#f=' + encodeURIComponent(entry); return a;
  };
  function renderList() {
    const body = $('r2-rows'); body.replaceChildren();
    for (const i of matches.slice(page * pageSize, (page + 1) * pageSize)) {
      const row = all[i], tr = el('tr'), first = el('td');
      first.append(fnLink(row[0], row[0]));
      tr.append(first, el('td', row[1]), el('td', row[2]), el('td', String(row[4])));
      body.append(tr);
    }
    $('r2-count').textContent = `${matches.length.toLocaleString('en-US')} matching functions; page ${matches.length ? page + 1 : 0} of ${Math.ceil(matches.length / pageSize)}`;
    $('r2-prev').disabled = page === 0; $('r2-next').disabled = (page + 1) * pageSize >= matches.length;
  }
  function filter() {
    const terms = $('r2-search').value.toLowerCase().trim().split(/\s+/).filter(Boolean), state = $('r2-state').value;
    matches = all.map((_, i) => i).filter(i => terms.every(t => text[i].includes(t)) && (!state || all[i][2] === state));
    page = 0; renderList();
  }
  function chunk(k) {
    if (window.r2Chunks && window.r2Chunks[k]) return Promise.resolve(window.r2Chunks[k]);
    if (!loading.has(k)) loading.set(k, new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = `chunks/chunk-${String(k).padStart(5, '0')}.js`;
      s.onload = () => (window.r2Chunks && window.r2Chunks[k]) ? resolve(window.r2Chunks[k]) : reject(new Error('empty chunk'));
      s.onerror = () => { loading.delete(k); reject(new Error('chunk not found')); };
      document.head.append(s);
    }));
    return loading.get(k);
  }
  function relation(title, list, render) {
    const section = el('div'); section.append(el('h3', `${title} (${list.total.toLocaleString('en-US')})`));
    if (!list.total) { section.append(el('p', 'None recorded.')); return section; }
    const ul = el('ul'); ul.className = 'rel';
    for (const item of list.items) { const li = el('li'); li.append(...render(item)); ul.append(li); }
    section.append(ul);
    if (list.total > list.items.length) section.append(el('p', `${list.total - list.items.length} more not shown.`));
    return section;
  }
  function renderFunction(f) {
    const body = $('r2-body'); body.replaceChildren();
    const facts = el('dl');
    for (const [k, v] of [['State', f.state], ['Signature', f.signature], ['Body bytes', String(f.body_bytes)],
                          ['Body ranges', f.body_ranges.map(r => r.join('–')).join(', ')], ['Thunk', String(f.thunk)],
                          ['Decompile time', f.ms + ' ms'], ['Error', f.error || 'none']]) facts.append(el('dt', k), el('dd', v));
    body.append(facts);
    if (f.warnings.length) { const ul = el('ul'); for (const w of f.warnings) ul.append(el('li', w)); body.append(el('h3', 'Warnings'), ul); }
    body.append(el('h3', f.partial_code ? 'Partial code (failed attempt)' : 'Pseudocode'), el('pre', f.code === null ? 'No code was produced.' : f.code));
    body.append(relation('Callees', f.callees, ([site, to, name, kind, resolved]) => [fnLink(to, name || to), el('span', `${resolved ? ' → ' + resolved : ''} at ${site} (${kind})`)]),
                relation('Callers', f.callers, ([site, from, name, kind]) => [fnLink(from, name || from), el('span', ` at ${site} (${kind})`)]),
                relation('Referenced strings', f.strings, ([addr, from, value]) => [el('code', JSON.stringify(value)), el('span', ` at ${addr}, from ${from}`)]),
                relation('Indirect calls and jumps', f.indirect, ([site, insn, targets]) => [el('code', insn), el('span', ` at ${site}; ${targets.length ? 'resolved: ' + targets.join(', ') : 'unresolved'}`)]));
  }
  function route() {
    const m = /^#f=(.+)$/.exec(location.hash), detail = $('detail');
    if (!m) { detail.hidden = true; return; }
    const entry = decodeURIComponent(m[1]), i = byEntry.get(entry);
    detail.hidden = false; $('r2-body').replaceChildren();
    if (i === undefined) { $('r2-heading').textContent = entry; $('r2-status').textContent = 'This entry is not in the committed corpus.'; return; }
    const row = all[i];
    $('r2-heading').textContent = `${row[1]} · ${row[0]}`; $('r2-heading').focus();
    $('r2-status').textContent = 'Loading code…';
    chunk(row[3]).then(list => {
      if (location.hash !== m[0]) return;
      const f = list.find(x => x.entry === entry);
      if (!f) throw new Error('entry missing from its chunk');
      $('r2-status').textContent = ''; renderFunction(f);
    }).catch(err => { $('r2-status').textContent = `Could not load this function: ${err.message}.`; });
  }
  $('r2-search').addEventListener('input', filter); $('r2-state').addEventListener('input', filter);
  $('r2-prev').addEventListener('click', () => { if (page > 0) { page--; renderList(); } });
  $('r2-next').addEventListener('click', () => { if ((page + 1) * pageSize < matches.length) { page++; renderList(); } });
  window.addEventListener('hashchange', route);
  renderList(); route();
})();
"""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('corpus', type=Path)
    parser.add_argument('indexes', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--title', default=None)
    args = parser.parse_args(argv)
    try:
        title = args.title or json.loads((args.corpus / 'run.json').read_text())['program']
        manifest = build(args.corpus, args.indexes, args.out, title)
    except (r2_corpus.CheckError, OSError, KeyError, ValueError) as failure:
        print(f'FAIL {args.corpus}: {failure}', file=sys.stderr)
        return 1
    print(json.dumps({'out': str(args.out), 'counts': manifest['counts'], 'listed_functions': manifest['listed_functions']}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
