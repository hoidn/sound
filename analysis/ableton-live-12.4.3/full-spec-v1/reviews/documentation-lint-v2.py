"""Read-only wiki/released-catalog audit; prints JSON and never repairs evidence."""
from pathlib import Path
from urllib.parse import unquote
import collections
import datetime
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
assert (ROOT / 'wiki/schema.md').is_file()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def slug(text):
    return re.sub(r'[^\w\- ]', '', text.strip().lower()).replace(' ', '-')


def links(text):
    return re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text)


def broken(path, text):
    result = []
    for raw in links(text):
        target = raw.strip().split(' "', 1)[0].strip('<>')
        if re.match(r'[a-zA-Z][\w+.-]*:', target):
            continue
        name, _, fragment = target.partition('#')
        dest = (path.parent / unquote(name)).resolve() if name else path
        if not dest.exists():
            result.append(raw)
        elif fragment and dest.suffix == '.md':
            body = dest.read_text()
            anchors = {slug(x) for x in re.findall(r'^#{1,6} (.+)$', body, re.M)}
            anchors.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', body))
            if unquote(fragment) not in anchors:
                result.append(raw)
    return sorted(set(result))


assert slug('REQ-ONE — visible state') == 'req-one--visible-state'
assert links('[x](some.md#part)') == ['some.md#part']
pages = sorted((ROOT / 'wiki').rglob('*.md')) + [ROOT / 'handoff/index.md']
pages = [p for p in pages if 'templates' not in p.parts]
errors, ids, current_broken = [], [], {}
index_links = set()
for p in pages:
    if p.name == 'index.md':
        for raw in links(p.read_text()):
            target = raw.split('#', 1)[0]
            if not re.match(r'[a-zA-Z][\w+.-]*:', target):
                index_links.add((p.parent / unquote(target)).resolve())
for p in pages:
    text = p.read_text()
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    meta = dict(re.findall(r'^(\w+):\s*(.+)$', match[1], re.M)) if match else {}
    for field in ['id', 'type', 'status', 'updated', 'access']:
        if field not in meta:
            errors.append(f'{p.relative_to(ROOT)} missing {field}')
    if 'id' in meta:
        ids.append(meta['id'])
    try:
        datetime.date.fromisoformat(meta.get('updated', ''))
    except ValueError:
        errors.append(f'{p.relative_to(ROOT)} invalid date')
    if meta.get('access') not in {'neutral', 'analysis', 'implementation', 'handoff'}:
        errors.append(f'{p.relative_to(ROOT)} invalid access')
    if '\x00' in text:
        errors.append(f'{p.relative_to(ROOT)} NUL bytes')
    if p.name != 'index.md' and p not in index_links:
        errors.append(f'{p.relative_to(ROOT)} missing inbound index link')
    bad = broken(p, text)
    if bad:
        current_broken[str(p.relative_to(ROOT))] = bad
errors += [f'duplicate id {k}' for k, n in collections.Counter(ids).items() if n > 1]
baseline = json.loads((Path(__file__).parent / 'documentation-lint-2026-10-19-v1.json').read_text())['existing_broken_links']
new_broken = {p: sorted(set(v) - set(baseline.get(p, []))) for p, v in current_broken.items()}
new_broken = {p: v for p, v in new_broken.items() if v}
payloads, manifests, unlisted = 0, 0, []
for m in sorted((ROOT / 'handoff').glob('*/manifest.json')):
    d = json.loads(m.read_text())
    manifests += 1
    listed = {'manifest.json'}
    for entry in d['files']:
        file = m.parent / entry['path']
        b = file.read_bytes()
        assert len(b) == entry['bytes'] and hashlib.sha256(b).hexdigest() == entry['sha256'], file
        listed.add(entry['path'])
        payloads += 1
    actual = {str(p.relative_to(m.parent)) for p in m.parent.rglob('*') if p.is_file()}
    unlisted.extend(str(m.parent.relative_to(ROOT) / p) for p in actual - listed)
head_paths = [p for p in git('ls-tree', '-r', '--name-only', 'HEAD', 'handoff').decode().splitlines()
              if p != 'handoff/index.md']
for path in head_paths:
    assert (ROOT / path).read_bytes() == git('show', 'HEAD:' + path), path
log_append_only = (ROOT / 'wiki/log.md').read_bytes().startswith(git('show', 'HEAD:wiki/log.md'))
assert log_append_only
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
if diff.returncode:
    errors.append(diff.stdout + diff.stderr)
report = {
    'status': 'pass' if not errors and not new_broken and not unlisted else 'fail',
    'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'wiki_and_catalog_pages': len(pages), 'unique_ids': len(set(ids)),
    'errors': errors, 'new_broken_links': new_broken,
    'existing_broken_link_count': sum(map(len, baseline.values())),
    'release_manifests': manifests, 'payload_hashes_sizes': payloads,
    'immutable_head_payloads_unchanged': len(head_paths),
    'log_append_only': log_append_only, 'unlisted_release_files': unlisted,
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'limits': 'Mechanical audit against retained v1 missing-source baseline; not semantic, runtime or compatibility verification. Untracked authored whitespace is checked separately.'
}
print(json.dumps(report, indent=2, ensure_ascii=False))
raise SystemExit(report['status'] != 'pass')
