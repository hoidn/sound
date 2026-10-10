"""Project retained native corpus metadata into an offline, paginated browser.

This reads a published coverage ledger; it is not an evidence integrity checker.
"""
import json
import re
from collections import Counter
from export_native_corpus import address


def project(corpus, href):
    coverage = corpus / 'coverage.json'
    if not coverage.exists():
        return None, [], []
    data = json.loads(coverage.read_text())
    if data.get('schema') != 1:
        raise ValueError('Unsupported native coverage schema')
    rows, inputs = [], [coverage]
    functions = data['functions']
    if data['unique_functions'] != len(functions) or dict(Counter(f['state'] for f in functions)) != data['counts']:
        raise ValueError('Native coverage totals disagree with rows')
    expected = {
        'eligible': sum(f['classification'] == 'eligible' for f in functions),
        'attempted': sum(f['classification'] == 'eligible' and f['attempts'] > 0 for f in functions),
        'successful': sum(f['state'] in ('exported', 'exported-with-warnings') for f in functions),
    }
    if any(data[key] != value for key, value in expected.items()):
        raise ValueError('Native coverage summary disagrees with rows')
    for f in functions:
        # Share the exporter's canonical identity grammar, including named
        # spaces such as EXTERNAL:0x1. Never collapse one into default-space 0x1.
        if address(f['address']) != f['address']:
            raise ValueError('Invalid function address')
        if f['attempts'] != len(f['revisions']):
            raise ValueError('Native attempt count disagrees with revisions')
        revisions = []
        for revision in f['revisions']:
            if not re.fullmatch(r'ev_[A-Za-z0-9_-]+-\d+', revision):
                raise ValueError('Invalid revision identifier')
            directory = corpus / 'functions' / f['address'] / revision
            metadata_path = directory / 'metadata.json'
            metadata = json.loads(metadata_path.read_text())
            inputs.append(metadata_path)
            if metadata['address'] != f['address'] or metadata['revision'] != revision:
                raise ValueError('Revision identity disagrees with coverage')
            revisions.append((directory, metadata))
        # Noneligible aggregate states describe inventory classification, not
        # attempt outcome. Preserve the classification and still expose attempts.
        matching = revisions if f['classification'] != 'eligible' else [(p, m) for p, m in revisions if m['state'] == f['state']]
        if (revisions or f['state'] in ('exported', 'exported-with-warnings', 'failed')) and not matching:
            raise ValueError('No revision supports coverage state')
        links = []
        if matching:
            directory, metadata = matching[0]
            source_hash = metadata['source_sha256']
            if not re.fullmatch(r'[0-9a-f]{64}', source_hash):
                raise ValueError('Invalid evidence hash')
            source = corpus / 'evidence' / (source_hash + '.json')
            if not source.is_file():
                raise ValueError('Missing source evidence')
            code = directory / 'pseudocode.c'
            if code.is_file():
                links.append(['Partial code (failed)' if metadata.get('partial_pseudocode') else 'Pseudocode', href(code)])
            elif f['state'] in ('exported', 'exported-with-warnings'):
                raise ValueError('Missing successful pseudocode')
            links += [['Revision / warnings', href(directory / 'metadata.json')], ['Source evidence', href(source)]]
        rows.append([f['address'], f['aliases'], f['state'], f['attempts'], links])
    summary = {key: data[key] for key in ('target_sha256', 'inventory_evidence_id', 'inventory_rows', 'unique_functions', 'eligible', 'counts', 'attempted', 'successful')}
    return summary, rows, inputs


def data_script(rows):
    # External JS, with HTML-significant characters escaped as an extra safeguard.
    return 'window.nativeRows=' + json.dumps(rows, ensure_ascii=True, separators=(',', ':')).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026') + ';\n'


SCRIPT = r"""
(() => {
  'use strict';
  const all = window.nativeRows || [];
  const search = document.getElementById('native-search');
  if (!search) return;
  const status = document.getElementById('native-status');
  const body = document.getElementById('native-rows');
  const searchable = all.map(row => [row[0], ...row[1], row[2]].join(' ').toLowerCase());
  let matches = all.map((_, i) => i), page = 0;
  const pageSize = 100;
  function render() {
    body.replaceChildren();
    for (const i of matches.slice(page * pageSize, (page + 1) * pageSize)) {
      const row = all[i], tr = document.createElement('tr');
      for (const text of [row[0], row[1].join('\n') || '(unnamed)', row[2], String(row[3])]) {
        const td = document.createElement('td'); td.textContent = text; tr.append(td);
      }
      const links = document.createElement('td');
      for (const [label, href] of row[4]) {
        const a = document.createElement('a'); a.textContent = label; a.href = href;
        links.append(a, document.createElement('br'));
      }
      if (!row[4].length) links.textContent = 'No retained attempt';
      tr.append(links); body.append(tr);
    }
    document.getElementById('native-count').textContent = `${matches.length.toLocaleString('en-US')} matching functions; page ${matches.length ? page + 1 : 0} of ${Math.ceil(matches.length / pageSize)}`;
    document.getElementById('native-prev').disabled = page === 0;
    document.getElementById('native-next').disabled = (page + 1) * pageSize >= matches.length;
  }
  function filter() {
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    matches = all.map((_, i) => i).filter(i => terms.every(t => searchable[i].includes(t)) && (!status.value || all[i][2] === status.value));
    page = 0; render();
  }
  search.addEventListener('input', filter); status.addEventListener('input', filter);
  document.getElementById('native-prev').addEventListener('click', () => { if (page > 0) { page--; render(); } });
  document.getElementById('native-next').addEventListener('click', () => { if ((page + 1) * pageSize < matches.length) { page++; render(); } });
  render();
})();
"""
