"""Read and validate sealed custom selected-entry captures for navigation only."""
from collections import Counter
import hashlib
import json
from pathlib import PurePosixPath
import re

TARGET = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
PROFILE = 'ghidra-selected-entry-noanalysis-v1'
SUCCESS = ('exported', 'exported-with-warnings')


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def sealed(run):
    """Return verified immutable inputs or reject the entire selected run."""
    if (run / 'manifest.json').is_symlink():
        raise ValueError('Sealed manifest is a symlink')
    manifest = json.loads((run / 'manifest.json').read_text())
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError('Empty or invalid sealed manifest')
    paths = []
    for name, expected in manifest.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or str(path) != name or name == 'manifest.json':
            raise ValueError('Unsafe manifest path')
        target = run / name
        cursor = run
        for part in path.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError('Symlink in sealed payload path')
        if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
            raise ValueError('Invalid sealed digest')
        if digest(target) != expected:
            raise ValueError('Sealed payload digest mismatch: ' + name)
        paths.append(target)
    actual = {p.relative_to(run).as_posix() for p in run.rglob('*') if p.is_file() and p != run / 'manifest.json'}
    if actual != set(manifest):
        raise ValueError('Sealed payload set mismatch')
    return manifest, [run / 'manifest.json', *paths]


def verified_run(run, href):
    manifest, inputs = sealed(run)
    for name in ('run.json', 'run-status.json', 'method/SelectedNativeExport.java'):
        if name not in manifest:
            raise ValueError('Required run evidence missing: ' + name)
    settings = json.loads((run / 'run.json').read_text())
    status = json.loads((run / 'run-status.json').read_text())
    if settings.get('schema') != 1 or settings.get('target_sha256') != TARGET or settings.get('architecture') != 'arm64':
        raise ValueError('Selected target identity mismatch')
    if settings.get('profile') != PROFILE or status.get('profile') != PROFILE:
        raise ValueError('Unexpected selected-entry profile')
    if settings.get('auto_analysis') is not False or settings.get('incremental_code_analysis') is not False:
        raise ValueError('Selected profile analysis settings disagree')
    if status.get('executed') is not True or status.get('cleanup', {}).get('cleaned') is not True or status['cleanup'].get('survivors') != []:
        raise ValueError('Selected run execution or cleanup unverified')
    if settings.get('method_sha256') != manifest['method/SelectedNativeExport.java']:
        raise ValueError('Selected method digest mismatch')
    seeds = settings.get('seeds', [])
    entries = {}
    for seed in seeds:
        entry = seed.get('address')
        if not isinstance(entry, str) or not re.fullmatch('0x[0-9a-f]+', entry) or hex(int(entry, 16)) != entry or int(entry, 16) % 4:
            raise ValueError('Invalid selected address')
        if entry in entries:
            raise ValueError('Duplicate selected address')
        if not isinstance(seed.get('label'), str) or not isinstance(seed.get('source'), str):
            raise ValueError('Missing selected seed provenance')
        entries[entry] = seed
    if not entries or len(entries) > 20:
        raise ValueError('Expected one to twenty selected seeds')
    items = status.get('items', [])
    if len(items) != len(entries) or {item.get('address') for item in items} != set(entries):
        raise ValueError('Selected outcomes disagree with seeds')
    rows = []
    for item in items:
        entry, state = item['address'], item.get('state')
        if state not in (*SUCCESS, 'failed', 'missing', 'invalid'):
            raise ValueError('Unknown selected outcome')
        prefix = 'functions/' + entry + '/'
        links = []
        metadata_name = prefix + 'metadata.json'
        if state in (*SUCCESS, 'failed'):
            if metadata_name not in manifest:
                raise ValueError('Selected metadata missing')
            metadata = json.loads((run / metadata_name).read_text())
            expected = {'schema': 1, 'provider': 'ghidra-headless-selected-script', 'profile': PROFILE,
                        'target_sha256': TARGET, 'address': entry, 'method_sha256': settings['method_sha256'],
                        'ghidra_version': settings['ghidra_version'], 'seed': entries[entry], 'state': state}
            if any(metadata.get(key) != value for key, value in expected.items()):
                raise ValueError('Selected function identity or state mismatch')
            if item.get('error') != metadata.get('error'):
                raise ValueError('Selected outcome error mismatch')
            if state in SUCCESS:
                if metadata.get('error') or not metadata.get('body_ranges') or metadata.get('body_bytes', 0) <= 0 or metadata.get('instruction_count', 0) <= 0:
                    raise ValueError('Successful selected output lacks body evidence')
                for name in ('pseudocode.c', 'assembly.txt'):
                    if prefix + name not in manifest or not (run / prefix / name).stat().st_size:
                        raise ValueError('Successful selected output missing code or assembly')
            for name, label in (('pseudocode.c', 'Pseudocode'), ('assembly.txt', 'Assembly')):
                if prefix + name in manifest:
                    links.append([label if state in SUCCESS else label + ' (partial; failed)', href(run / prefix / name)])
            links.append(['Metadata / warnings', href(run / metadata_name)])
        elif state == 'missing' and metadata_name in manifest:
            raise ValueError('Missing outcome has committed metadata')
        # Invalid attempts retain their error and run evidence, not code links.
        rows.append({'address': entry, 'label': entries[entry]['label'], 'state': state,
                     'error': item.get('error'), 'links': links})
    counts = dict(Counter(row['state'] for row in rows))
    return {'name': run.name, 'state': 'sealed', 'profile': PROFILE, 'exit_code': status.get('exit_code'),
            'rows': rows, 'counts': counts, 'successful': sum(counts.get(s, 0) for s in SUCCESS),
            'links': [['Run settings / seed provenance', href(run / 'run.json')],
                      ['Run outcomes', href(run / 'run-status.json')], ['Sealed manifest', href(run / 'manifest.json')]]}, inputs


def project(artifacts, href):
    runs, inputs = [], []
    for run in sorted(artifacts.glob('native-live-arm64-targeted-v*')):
        if not run.is_dir() or not re.fullmatch(r'native-live-arm64-targeted-v\d+', run.name):
            continue
        if not (run / 'manifest.json').is_file():
            runs.append({'name': run.name, 'state': 'unsealed', 'error': 'No sealed manifest; function artifacts are not published.', 'rows': [], 'successful': 0})
            continue
        try:
            if run.is_symlink():
                raise ValueError('Selected capture directory is a symlink')
            result, paths = verified_run(run, href)
            runs.append(result)
            inputs += paths
        except (ValueError, KeyError, TypeError, OSError, AttributeError) as error:
            runs.append({'name': run.name, 'state': 'invalid', 'error': str(error), 'rows': [], 'successful': 0})
    return runs, inputs


SCRIPT = r"""
(() => {
  const search = document.getElementById('selected-search');
  if (!search) return;
  const rows = [...document.querySelectorAll('tr[data-selected-search]')];
  function filter() {
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const row of rows) {
      row.hidden = !terms.every(term => row.dataset.selectedSearch.includes(term));
      if (!row.hidden) count++;
    }
    document.getElementById('selected-count').textContent = `${count} of ${rows.length} selected outcomes`;
  }
  search.addEventListener('input', filter); filter();
})();
"""
