#!/usr/bin/env python3
"""Build offline analyst navigation from retained evidence; never inspect target code.

Run from any directory: python3 /path/to/sound/tools/build_artifact_browser.py
Generated files are replaceable views. Original evidence is never modified.
"""
from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import os
from collections import Counter
from pathlib import Path
from urllib.parse import quote
import native_browser
import export_native_corpus
import selected_browser
import function_starts_browser
import build_compact_native_browser as compact_browser

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "analysis/ableton-live-12.4.3"
OUT = ARTIFACTS / "browse"
SOURCE_NAMES = (
    "native-targets.json", "native-summary.json", "push2-decompilation-summary.json",
    "evidence/push2-entry-dossier.json",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def href(path: Path) -> str:
    return quote(os.path.relpath(path, OUT).replace(os.sep, "/"), safe="/.-_")


def link(path: Path, label: str) -> str:
    return f'<a href="{href(path)}">{escape(label)}</a>'


def category(path: str) -> str:
    # Navigation groups describe package locations, not recovered subsystem boundaries.
    if path.endswith(".class"):
        return "Java .class candidates"
    for prefix, label in (
        ("Contents/MacOS/", "Live core"),
        ("Contents/App-Resources/Devices/", "Bundled devices"),
        ("Contents/App-Resources/Extensions/", "Extension helpers"),
        ("Contents/App-Resources/Max/", "Max package"),
        ("Contents/Qt/", "Qt libraries and plugins"),
        ("Contents/Frameworks/", "Frameworks"),
        ("Contents/Push2/", "Push 2"),
        ("Contents/Helpers/Push3.app/", "Push 3"),
    ):
        if path.startswith(prefix):
            return label
    return "Other package locations"


def tsv(rows: list[list[object]]) -> str:
    output = io.StringIO(newline="")
    csv.writer(output, delimiter="\t", lineterminator="\n").writerows(rows)
    return output.getvalue()


STYLE = """
:root{color-scheme:light;--ink:#182d3b;--muted:#425c6c;--line:#c9d6df;--accent:#075d85;--paper:#fff;--wash:#edf3f6}
*{box-sizing:border-box}body{margin:0;background:var(--wash);color:var(--ink);font:16px/1.55 system-ui,sans-serif}
main{max-width:1240px;margin:auto;padding:28px 24px 64px}a{color:var(--accent);text-underline-offset:.17em}
a:hover{text-decoration-thickness:2px}h1{font-size:clamp(1.7rem,4vw,2.6rem);line-height:1.18;margin:.5em 0}h2{font-size:1.4rem}h3{font-size:1.1rem}
.eyebrow{text-transform:uppercase;font-size:.78rem;letter-spacing:.09em;color:var(--muted)}.lead{max-width:85ch;color:var(--muted)}
nav{display:flex;flex-wrap:wrap;gap:12px 24px;margin:22px 0}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.card,section{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:20px;margin:20px 0}.card{margin:0}
.card h2{margin-top:8px}.badge{display:inline-block;border:1px solid var(--line);border-radius:4px;padding:2px 7px;font-size:.78rem;background:var(--wash)}
.notice{border-left:4px solid #956009;padding:10px 16px;background:#fff6e2}.muted,small{color:var(--muted)}
code{font-family:ui-monospace,monospace;font-size:.88em;overflow-wrap:anywhere}.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:end;margin:16px 0}
label{display:block;font-weight:600}input,select,button{font:inherit;border:1px solid #7a909d;border-radius:5px;padding:9px;background:white;color:var(--ink);max-width:100%}
input{width:340px}button{cursor:pointer}button:hover{background:var(--wash)}:focus-visible{outline:3px solid #ad6100;outline-offset:3px}
.table-wrap{overflow:auto;max-width:100%}table{border-collapse:collapse;width:100%;font-size:.9rem;text-align:left}caption{text-align:left;padding:10px 0;color:var(--muted)}
th,td{border-bottom:1px solid var(--line);padding:11px 10px;vertical-align:top}th{background:var(--wash)}.group th{background:#dce8ee;padding:9px 10px}.path{min-width:320px;max-width:530px;overflow-wrap:anywhere}.size{white-space:nowrap}.hash{max-width:150px;font-size:.78rem}.flag{color:#83500a;font-weight:600}
#count{font-weight:600}#empty{padding:20px;background:var(--wash)}.modules{columns:2;column-gap:32px}.modules li{break-inside:avoid;margin:6px 0;overflow-wrap:anywhere}
summary{cursor:pointer;font-weight:600;padding:5px 0}.provenance td{overflow-wrap:anywhere}.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:8px;background:white;padding:10px;z-index:1}
[hidden]{display:none!important}@media(max-width:780px){main{padding:18px 14px 40px}.cards{grid-template-columns:1fr}.modules{columns:1}.controls{display:block}.controls>div,button{margin:10px 0}input,select{width:100%}section,.card{padding:16px}}
"""

SCRIPT = """
'use strict';
const search = document.getElementById('search');
const category = document.getElementById('category');
const format = document.getElementById('format');
const rows = [...document.querySelectorAll('tr[data-search]')];
const groups = [...document.querySelectorAll('tbody[data-group]')];
function applyFilters() {
  const terms = search.value.toLocaleLowerCase().trim().split(/\\s+/).filter(Boolean);
  let visible = 0;
  for (const row of rows) {
    const match = terms.every(term => row.dataset.search.includes(term)) &&
      (!category.value || row.dataset.category === category.value) &&
      (!format.value || row.dataset.format === format.value);
    row.hidden = !match;
    if (match) visible++;
  }
  for (const group of groups) {
    const count = [...group.querySelectorAll('tr[data-search]')].filter(row => !row.hidden).length;
    group.hidden = count === 0;
    group.querySelector('.group-count').textContent = String(count);
  }
  document.getElementById('count').textContent = `${visible.toLocaleString('en-US')} of ${rows.length.toLocaleString('en-US')} candidate records`;
  document.getElementById('empty').hidden = visible !== 0;
}
for (const control of [search, category, format]) control.addEventListener('input', applyFilters);
document.getElementById('reset').addEventListener('click', () => {
  search.value = ''; category.value = ''; format.value = ''; applyFilters(); search.focus();
});
const params = new URLSearchParams(location.search);
search.value = params.get('q') || '';
for (const [control, key] of [[category, 'category'], [format, 'format']]) {
  const value = params.get(key);
  if ([...control.options].some(option => option.value === value)) control.value = value;
}
applyFilters();
"""


def build() -> dict:
    # Serialize projection and provenance publication with corpus updates.
    # Otherwise the manifest could hash a newer ledger than the rendered page.
    with export_native_corpus.locked(ARTIFACTS / 'native-live-arm64-v1'):
        return _build()


def _build() -> dict:
    sources = {name: json.loads((ARTIFACTS / name).read_text()) for name in SOURCE_NAMES}
    native = sources["native-targets.json"]
    summary = sources["native-summary.json"]
    push = sources["push2-decompilation-summary.json"]
    dossier = sources["evidence/push2-entry-dossier.json"]["normalized_result"]
    targets = native["targets"]
    modules = sorted((ARTIFACTS / "midi-user-mapping-v1/disassembly").rglob("*.dis.txt"))
    if len(targets) != 1093 or len(modules) != 17:
        raise ValueError("Pinned capture changed: expected 1093 candidates and 17 disassembly files")
    OUT.mkdir(parents=True, exist_ok=True)
    corpus = ARTIFACTS / 'native-live-arm64-v1'
    native_coverage, native_rows, native_inputs = native_browser.project(corpus, href)
    native_scripts = native_browser.index_scripts(native_rows)
    native_inventory_revision = hashlib.sha256(native_scripts['native-inventory.js'].encode('utf-8')).hexdigest()
    native_scripts['native-inventory.js'] += f'window.nativeInventoryRevision="{native_inventory_revision}";\n'
    native_initial_rows = sum(row[3] > 0 for row in native_rows)
    native_inventory_bytes = len(native_scripts['native-inventory.js'].encode('utf-8'))
    selected_runs, selected_inputs = selected_browser.project(ARTIFACTS, href)
    compact_view, compact_inputs = compact_browser.project(ARTIFACTS, corpus, href)
    compact_content = '<p>No compact code viewer is available in this snapshot. The original native revision links remain available above.</p>'
    if compact_view:
        if compact_view['state'] == 'verified':
            compact_counts = compact_view['counts']
            compact_content = f'<p><a href="{escape(compact_view["url"])}">Open the offline native code reader</a>: search {compact_counts["addresses"]:,} mirrored addresses and {compact_counts["revisions"]:,} exact revisions, read code and warnings, and download original UTF-8 code bytes. This mirror adds no decompilation coverage; these are the same retained attempts shown in the corpus ledger.</p><p>All viewer outputs and current archive ZIP bytes were verified for this target, profile and inventory. Reader generation: <code>{escape(compact_view["generation"])}</code>. <a href="{escape(compact_view["manifest_url"])}">Viewer provenance manifest</a>.</p>'
        else:
            compact_content = f'<p class="notice">Compact viewer validation failed: {escape(compact_view["error"])}. Original corpus links remain available.</p>'
    declared_starts, starts_inputs = function_starts_browser.project(ARTIFACTS / 'derived/function-starts-v1', href)
    starts_content = '<p>No sealed linker-declared starts capture is available in this snapshot.</p>'
    if declared_starts:
        if declared_starts['state'] == 'sealed':
            starts_links = ' · '.join(f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in declared_starts['links'])
            starts_content = f'<p><strong>{declared_starts["count"]:,} linker-declared starts</strong> in the pinned arm64 executable. <code>LC_FUNCTION_STARTS</code> status: {escape(declared_starts["status"])}. The sealed payload hashes, target/method identity and table count were checked when building this view.</p><p>{starts_links}</p>'
        else:
            starts_content = f'<p class="notice">{escape(declared_starts["state"])}: {escape(declared_starts["error"])}</p>'
    selected_successful = sum(run['successful'] for run in selected_runs)
    selected_sections = []
    for run in selected_runs:
        if run['state'] != 'sealed':
            selected_sections.append(f'<h3>{escape(run["name"])}</h3><p class="notice">{escape(run["state"])}: {escape(run["error"])}</p>')
            continue
        rows = []
        for row in run['rows']:
            searchable = f'{run["name"]} {row["address"]} {row["label"]} {row["state"]}'.lower()
            links = '<br>'.join(f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in row['links']) or 'No validated function artifacts'
            error = f'<br><small>{escape(row["error"])}</small>' if row['error'] else ''
            rows.append(f'<tr data-selected-search="{escape(searchable)}"><td><code>{escape(row["address"])}</code></td><td>{escape(row["label"])}</td><td>{escape(row["state"])}{error}</td><td>{links}</td></tr>')
        run_links = ' · '.join(f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in run['links'])
        selected_sections.append(f'<h3>{escape(run["name"])}</h3><p>Sealed capture: {run["successful"]} of {len(run["rows"])} selected outcomes have pseudocode. Process exit code: {escape(run["exit_code"])}. Profile: <code>{escape(run["profile"])}</code>. Manifest digests and retained cleanup record verified during this build.</p><p>{run_links}</p><div class="table-wrap"><table><caption>Selected-entry outcomes; names are seed labels, not recovered original source identifiers</caption><thead><tr><th>Address</th><th>Seed label</th><th>Outcome</th><th>Artifacts</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    selected_content = ''.join(selected_sections) or '<p>No selected-entry captures are present in this snapshot.</p>'
    learning = ''.join(f'<li>{link(ROOT / path, label)}</li>' for path, label in (
        ('wiki/research/learning/index.md', 'Start learning: reading route and worked investigations'),
        ('wiki/research/learning/method.md', 'How we reverse engineer: evidence, hypotheses and contracts'),
        ('wiki/research/learning/walkthroughs/first-native-loop-factory.md', 'Read the first main Live function: code, instructions and limits'),
        ('wiki/research/learning/walkthroughs/transport-wrapper-boundary.md', 'Understand a failed transport-wrapper export'),
        ('wiki/research/learning/walkthroughs/artifact-storage-and-recovery.md', 'Understand code archives, storage measurements and analysis recovery'),
        ('wiki/research/program-structure.md', 'Program structure atlas: known relationships and open gaps'),
        ('wiki/research/native-phase-execution.md', 'Current phase: execution ledger and resource limits'),
        ('wiki/research/artifacts/browser-design-and-plan.md', 'Browser design and regeneration policy'),
    ))
    native_badge = 'No corpus inventory retained'
    if native_coverage is None:
        if selected_successful:
            native_badge = f'{selected_successful:,} selected-entry exports · No full inventory'
        native_content = '<p>No frozen main Live function inventory or corpus exports are available in this generated snapshot. The symbol index below remains available. See the execution ledger for current investigation progress; missing inventory is not a function count of zero.</p>'
    else:
        n = native_coverage
        native_badge = f'{n["successful"]:,} functions with pseudocode'
        counts = ''.join(f'<li>{escape(state)}: {count:,}</li>' for state, count in sorted(n['counts'].items()))
        states = ''.join(f'<option value="{escape(state)}">{escape(state)}</option>' for state in sorted(n['counts']))
        native_content = f'''<p>{n['inventory_rows']:,} inventory rows resolve to {n['unique_functions']:,} distinct function addresses; {n['eligible']:,} are eligible for export. {n['attempted']:,} eligible functions have a retained attempt; {n['successful']:,} functions have retained pseudocode. Discovered functions are not all original source.</p><ul>{counts}</ul>
<p>Target SHA-256: <code>{escape(n['target_sha256'])}</code>. Inventory evidence: <code>{escape(n['inventory_evidence_id'])}</code>. {link(corpus / 'coverage.json', 'Full coverage and revision ledger')}.</p>
<p>Search addresses, aliases and status. Each row links a retained revision matching the aggregate status; it need not be the newest attempt. The full ledger records every revision. Warning and failure details remain in revision metadata. Pseudocode approximates compiled behavior; it is not original or guaranteed compilable source.</p>
<noscript><p>JavaScript is disabled. Open the full coverage ledger above to find addresses and revision identities.</p></noscript>
<p id="native-scope">Searching {native_initial_rows:,} functions with retained attempts. Pending and external addresses without attempts become searchable after loading the full inventory.</p>
<button id="native-load-inventory" type="button" data-total="{len(native_rows)}" data-revision="{native_inventory_revision}">Load all {len(native_rows):,} inventoried addresses ({native_inventory_bytes / 1000000:.1f} MB local index)</button><p id="native-load-status" role="status" aria-live="polite"></p>
<div class="controls"><div><label for="native-search">Search native functions</label><input id="native-search" type="search" placeholder="Address, symbol or status"></div><div><label for="native-status">Export status</label><select id="native-status"><option value="">All states</option>{states}</select></div></div>
<p id="native-count" role="status" aria-live="polite"></p><button id="native-prev" type="button">Previous 100</button> <button id="native-next" type="button">Next 100</button>
<div class="table-wrap"><table><caption>Main Live arm64 function corpus · at most 100 rows displayed</caption><thead><tr><th>Address</th><th>Aliases</th><th>Status</th><th>Attempts</th><th>Artifacts</th></tr></thead><tbody id="native-rows"></tbody></table></div>'''
    generated = {
        **native_scripts,
        "push2-entry-assembly.txt": "\n".join(dossier["assembly"]) + "\n",
        "push2-entry-callees.tsv": tsv(
            [["address", "name", "external", "thunk", "classification_provenance"]] +
            [[r.get("address", ""), r.get("name", ""),
              r.get("classification", {}).get("external", ""),
              r.get("classification", {}).get("thunk", ""),
              r.get("classification", {}).get("provenance", "")]
             for r in dossier["callees"]]),
        "push2-entry-strings.tsv": tsv(
            [["address", "source_address", "value"]] +
            [[r.get("address", ""), r.get("source_address", ""), r.get("value", "")]
             for r in dossier["referenced_strings"]]),
    }
    for name, content in generated.items():
        (OUT / name).write_text(content, encoding="utf-8", newline="")
    groups = Counter(category(row["logical_path"]) for row in targets)
    formats = Counter(row["artifact_format"] for row in targets)
    false_positives = groups["Java .class candidates"]
    table = []
    for group in sorted(groups):
        table.append(f'<tbody data-group="{escape(group)}"><tr class="group"><th colspan="4" scope="rowgroup">{escape(group)} · <span class="group-count">{groups[group]}</span></th></tr>')
        for row in sorted((r for r in targets if category(r["logical_path"]) == group), key=lambda r: r["logical_path"]):
            path, fmt, sha = row["logical_path"], row["artifact_format"], row["sha256"]
            flag = '<br><span class="flag">Java .class path: native label unvalidated</span>' if path.endswith('.class') else ''
            searchable = f'{path} {group} {fmt} {sha}'.lower()
            table.append(f'<tr data-search="{escape(searchable)}" data-category="{escape(group)}" data-format="{escape(fmt)}"><td class="path"><code>{escape(path)}</code>{flag}</td><td>{escape(fmt)}</td><td class="size">{row["size"]:,} bytes</td><td class="hash"><code>{escape(sha)}</code><br><small>Hash status: {escape(row["hash_status"])}</small></td></tr>')
        table.append('</tbody>')
    options = lambda counts: ''.join(f'<option value="{escape(k)}">{escape(k)} ({v:,})</option>' for k, v in sorted(counts.items()))
    source_rows = ''.join(f'<tr><td>{link(ARTIFACTS / name, name)}</td><td><code>{digest(ARTIFACTS / name)}</code></td></tr>' for name in SOURCE_NAMES)
    module_links = ''.join(f'<li>{link(p, p.relative_to(ARTIFACTS / "midi-user-mapping-v1/disassembly").as_posix())}</li>' for p in modules)
    version = summary["plist"]["bundle"]["version"]
    addr = push["procedure"]["address"]
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>Ableton 12.4.3 · Artifact browser</title><style>{STYLE}</style></head>
<body><a class="skip" href="#inventory">Skip to package inventory</a><main>
<header><div class="eyebrow">Analyst workspace · Offline artifact browser</div><h1>Ableton: structure and recovered code</h1><p class="lead">Reference build <strong>{escape(version)}</strong>. Open the retained evidence below, or search the package inventory by path, format or SHA-256. This page is a navigation view of existing captures; it makes no new behavioral or compatibility claims.</p>
<nav aria-label="Page navigation">{link(ROOT / 'wiki/research/artifacts/index.md', 'Artifact guide (wiki)')}<a href="#learning">Learn the method and structure</a><a href="#selected-native">Selected main Live pseudocode</a><a href="#native">Default-profile corpus</a><a href="#compact-native">Offline native code reader</a><a href="#declared-starts">Linker-declared starts</a><a href="#inventory">Package inventory</a><a href="#python">Python disassembly</a><a href="#provenance">Provenance</a></nav></header>
<div class="cards">
<article class="card"><span class="badge">{escape(native_badge)}</span><h2>Live core</h2><p>The main executable has x86_64 and arm64 slices. The arm64 symbol index contains {summary['symbol_counts']['exports']:,} merged export/symbol entries; this is not a function count.</p><p><a href="#selected-native">Read selected main Live pseudocode and assembly</a></p><p><a href="#native">Default-profile corpus status and functions</a></p><p>{link(ARTIFACTS / 'live-arm64-symbols.tsv', 'Open symbol index (32 MiB TSV)')}</p><p>{link(ARTIFACTS / 'native-summary.json', 'Native summary and dependencies (JSON)')}</p><p>{link(ARTIFACTS / 'derived/manifest.json', 'Derived arm64 slice manifest')}</p></article>
<article class="card"><span class="badge">One entry procedure · Pseudocode</span><h2>Push 2 display helper</h2><p>Ghidra representation of <code>entry</code> at <code>{escape(addr)}</code>. Warnings and incomplete indirect-call recovery remain; this is not original source.</p><p>{link(ARTIFACTS / 'push2-entry-pseudocode.c', 'Read entry pseudocode (C text)')}</p><p>{link(OUT / 'push2-entry-assembly.txt', f'Assembly ({len(dossier["assembly"]):,} lines)')} · {link(OUT / 'push2-entry-callees.tsv', f'Callees ({len(dossier["callees"]):,})')} · {link(OUT / 'push2-entry-strings.tsv', f'String references ({len(dossier["referenced_strings"]):,})')}</p><p>{link(ARTIFACTS / 'evidence/push2-entry-dossier.json', 'Full entry dossier')} · {link(ARTIFACTS / 'push2-decompilation-summary.json', 'Warnings and summary')}</p></article>
<article class="card"><span class="badge">17 modules · Bytecode disassembly</span><h2>MIDI mapping scripts</h2><p>Readable instruction listings from selected Python 3.11 bytecode. These are static disassemblies, not recovered Python source or runtime observations.</p><p><a href="#python">Browse all 17 module listings</a></p><p>{link(ROOT / 'wiki/research/midi-user-mapping.md', 'Read the mapping findings')} · {link(ROOT / 'wiki/specs/midi-user-mapping.md', 'Draft behavioral contract')}</p></article>
</div>
<section id="learning"><h2>Understand the investigation</h2><p>Follow the method, read worked examples, and explore the application structure as evidence accumulates. These wiki pages separate observations, interpretations and unknowns.</p><ul>{learning}</ul></section>
<section id="selected-native"><h2>Selected main Live functions</h2><p>These bounded captures decompile chosen entries with whole-image auto-analysis disabled. They use a separate custom Ghidra profile, are not REA evidence records, and do not provide a whole-program inventory. Successful entries are available below even when the default-profile corpus is unavailable. Retained attempts across runs can repeat an address; counts describe outcomes, not unique whole-program functions.</p><label for="selected-search">Search selected names, addresses, runs or outcomes</label><input id="selected-search" type="search" placeholder="For example: ALoopOn or 0x10276e5d4"><p id="selected-count" role="status" aria-live="polite"></p><noscript><p>All selected outcomes remain visible; use your browser's Find command.</p></noscript>{selected_content}</section>
<section id="native"><h2>Default-profile main Live corpus</h2>{native_content}</section>
<section id="compact-native"><h2>Offline native code reader</h2>{compact_content}</section>
<section id="declared-starts"><h2>Linker-declared function starts</h2>{starts_content}<p>This address index comes from linker metadata. It is separate from analyzer-discovered functions, recovered bodies and decompiled code. Adjacent addresses do not establish function sizes. Its count is not an export-coverage denominator; open the TSV directly without loading its rows into this page.</p></section>
<section id="inventory"><h2>Package inventory</h2><p class="notice"><strong>{len(targets):,} native-format candidate records, not {len(targets):,} verified native binaries.</strong> The inventory includes {false_positives} paths ending in <code>.class</code>, a Java bytecode extension whose header can collide with the universal Mach-O classifier. Their native-format labels are unvalidated; they remain visible and separately grouped. Other candidate labels have not all been individually validated. Hash verification describes captured bytes, not format correctness.</p><p>Groups are derived from package paths; they do not establish internal subsystem boundaries. Paths identify captured package locations and do not link to a possibly changed installed application.</p>
<noscript><p>JavaScript is disabled. All grouped records and artifact links remain available; use your browser’s Find command to search.</p></noscript>
<div class="controls"><div><label for="search">Search path, format or digest</label><input id="search" type="search" placeholder="For example: Push2, libusb, .class" aria-describedby="search-help"></div><div><label for="category">Package group</label><select id="category"><option value="">All groups</option>{options(groups)}</select></div><div><label for="format">Reported format</label><select id="format"><option value="">All formats</option>{options(formats)}</select></div><button id="reset" type="button">Clear filters</button></div>
<p id="search-help" class="muted">Search is case-insensitive; all space-separated terms must match. Filters combine. For the raw records, {link(ARTIFACTS / 'native-targets.json', 'open native-targets.json')}.</p><p id="count" role="status" aria-live="polite">{len(targets):,} of {len(targets):,} candidate records</p><p id="empty" hidden>No matching records. Try a shorter term or clear filters.</p>
<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable package inventory"><table><caption>Captured package paths, classifier labels, sizes and SHA-256 digests</caption><thead><tr><th scope="col">Path within application bundle</th><th scope="col">Reported format</th><th scope="col">Size</th><th scope="col">SHA-256</th></tr></thead>{''.join(table)}</table></div></section>
<section id="python"><h2>Python module listings</h2><p>All {len(modules)} retained disassemblies in the MIDI mapping investigation. Open a text listing, then search by function name or bytecode offset. Evidence and decoder provenance are in the {link(ROOT / 'wiki/research/sources/midi-user-mapping-12.4.3.md', 'source capture page')}.</p><p>{link(ROOT / 'wiki/research/learning/walkthroughs/midi-integer-parsing.md', 'Worked example: tracing MIDI integer parsing')}</p><ul class="modules">{module_links}</ul></section>
<section id="provenance"><h2>Provenance and regeneration</h2><p>This generated view reads retained records only. It launches no target, performs no decompilation and needs no server, external scripts or network. All links refer to files in this checkout; moving this HTML alone will break them.</p><p>Regenerate from the repository root with <code>python3 tools/build_artifact_browser.py</code>. The output is deterministic for unchanged inputs and generator. {link(OUT / 'manifest.json', 'Generated-view manifest')} records source and output hashes; source artifacts remain untouched.</p><details><summary>Input SHA-256 digests</summary><div class="table-wrap"><table class="provenance"><thead><tr><th scope="col">Retained input</th><th scope="col">SHA-256</th></tr></thead><tbody>{source_rows}</tbody></table></div></details><p class="muted">Analyst material. These raw artifacts are not approved clean-implementation inputs. The linked wiki guide records scope, limitations and handoff boundaries.</p></section>
</main><script src="native-index.js"></script><script>{SCRIPT}\n{native_browser.SCRIPT}\n{selected_browser.SCRIPT}</script></body></html>
'''
    (OUT / 'index.html').write_text(page, encoding='utf-8', newline='')
    input_paths = [ARTIFACTS / name for name in SOURCE_NAMES] + modules + native_inputs + selected_inputs + starts_inputs + compact_inputs
    manifest = {
        "schema": "analyst-artifact-browser-v1",
        "generator": {"path": "tools/build_artifact_browser.py", "sha256": digest(Path(__file__))},
        "helper": {"path": "tools/native_browser.py", "sha256": digest(Path(native_browser.__file__))},
        "selected_helper": {"path": "tools/selected_browser.py", "sha256": digest(Path(selected_browser.__file__))},
        "starts_helper": {"path": "tools/function_starts_browser.py", "sha256": digest(Path(function_starts_browser.__file__))},
        "compact_helper": {"path": "tools/build_compact_native_browser.py", "sha256": digest(Path(compact_browser.__file__))},
        "archive_helper": {"path": "tools/compact_native_corpus.py", "sha256": digest(Path(compact_browser.compact.__file__))},
        "lock_provider": {"path": "tools/export_native_corpus.py", "sha256": digest(Path(export_native_corpus.__file__))},
        "command": "python3 tools/build_artifact_browser.py",
        "scope": "Deterministic navigation and text extraction from retained evidence; no new target analysis.",
        "counts": {"candidate_records": len(targets), "java_class_path_candidates": false_positives,
                   "python_disassembly_files": len(modules), "assembly_lines": len(dossier['assembly']),
                   "callees": len(dossier['callees']), "string_references": len(dossier['referenced_strings'])},
        "native_coverage": native_coverage,
        "native_navigation": {"initial_scope": "functions with retained attempts", "initial_rows": native_initial_rows,
                              "inventory_rows": len(native_rows), "inventory_index_bytes": native_inventory_bytes,
                              "inventory_revision": native_inventory_revision,
                              "inventory_load": "Explicit local script load; no fetch or server"},
        "selected_runs": [{k: v for k, v in run.items() if k not in ('rows', 'links')} for run in selected_runs],
        "linker_declared_starts": {k: v for k, v in declared_starts.items() if k != 'links'} if declared_starts else None,
        "compact_native": {k: v for k, v in compact_view.items() if k not in ('url', 'manifest_url')} if compact_view else None,
        "inputs": [{"path": p.relative_to(ROOT).as_posix(), "sha256": digest(p)} for p in input_paths],
        "outputs": [{"path": (OUT / name).relative_to(ROOT).as_posix(), "sha256": digest(OUT / name)}
                    for name in sorted(["index.html", *generated])],
        "manifest_hash_policy": "This manifest excludes its own digest to avoid a circular hash.",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = build()
    print(json.dumps({"output": str(OUT / "index.html"), "counts": result["counts"]}, indent=2))
