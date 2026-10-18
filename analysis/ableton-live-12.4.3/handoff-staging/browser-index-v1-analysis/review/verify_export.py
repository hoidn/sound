"""Reviewer's independent package check of an exported copy (not the author's verify).

Checks every manifest hash and size, that the inventory equals the directory (manifest
excluded), that no symlink exists, that every relative Markdown link resolves inside the
package, and that every case input and example serialization exists.
Usage: python3 -I verify_export.py PACKAGE_DIR
"""
import hashlib, json, re, sys
from pathlib import Path


def main(d):
    d = Path(d).resolve()
    man = json.loads((d / 'manifest.json').read_text())
    listed = {f['path']: f for f in man['files']}
    on_disk = {str(p.relative_to(d)) for p in d.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    bad = [p for p, f in listed.items() if not (d / p).is_file()
           or hashlib.sha256((d / p).read_bytes()).hexdigest() != f['sha256'] or (d / p).stat().st_size != f['bytes']]
    links = []
    for md in d.glob('*.md'):
        for t in re.findall(r'\]\(([^)\s]+)\)', md.read_text()):
            target = (md.parent / t.split('#')[0]).resolve()
            links.append((md.name, t, target.is_file() and d in target.parents))
    cases = json.loads((d / 'cases.json').read_text())['cases']
    refs = [c['input']['folder'] for c in cases if 'folder' in c['input']]
    refs += [c['expected']['example_serialization'] for c in cases if 'example_serialization' in c['expected']]
    print('listed files:', len(listed), 'hash/size mismatches:', bad)
    print('inventory differences:', sorted(on_disk ^ set(listed)))
    print('symlinks:', [str(p) for p in d.rglob('*') if p.is_symlink()])
    print('links:', len(links), 'unresolved:', [(m, t) for m, t, ok in links if not ok])
    print('case inputs:', len(refs), 'missing:', [r for r in refs if not (d / r).exists()])
    print('cases:', len(cases), 'case_count:', man['case_count'], 'release_status:', man['release_status'],
          'review:', man['review']['status'])
    print('manifest sha256:', hashlib.sha256((d / 'manifest.json').read_bytes()).hexdigest())


if __name__ == '__main__':
    main(sys.argv[1])
