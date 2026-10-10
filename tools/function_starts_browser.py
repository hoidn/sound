"""Validate a sealed linker-starts capture and expose compact navigation only."""
import csv
import json
import re
from selected_browser import TARGET, digest

METHOD = 'index_macho_function_starts.py'


def project(capture, href):
    if not capture.exists():
        return None, []
    try:
        if capture.is_symlink() or (capture / 'manifest.json').is_symlink():
            raise ValueError('Symlinked linker-starts capture or manifest')
        if not (capture / 'manifest.json').is_file():
            return {'state': 'unsealed', 'error': 'No sealed linker-starts manifest.'}, []
        manifest = json.loads((capture / 'manifest.json').read_text())
        allowed = {'summary.json', METHOD, 'addresses.tsv'}
        if not isinstance(manifest, dict) or set(manifest) not in ({'summary.json', METHOD}, allowed):
            raise ValueError('Unexpected linker-starts payload set')
        if {p.name for p in capture.iterdir()} != set(manifest) | {'manifest.json'}:
            raise ValueError('Unsealed or missing linker-starts payload')
        for name, entry in manifest.items():
            path = capture / name
            if path.is_symlink() or not path.is_file():
                raise ValueError('Invalid linker-starts payload path')
            if not isinstance(entry, dict) or set(entry) != {'sha256', 'bytes'}:
                raise ValueError('Invalid linker-starts manifest entry')
            if type(entry['bytes']) is not int or entry['bytes'] < 0 or not isinstance(entry['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', entry['sha256']):
                raise ValueError('Invalid linker-starts payload identity')
            if path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
                raise ValueError('Linker-starts payload digest or size mismatch')
        summary = json.loads((capture / 'summary.json').read_text())
        expected = {'schema': 'macho-linker-function-starts-v1', 'target_sha256': TARGET,
                    'architecture': 'arm64', 'source': 'LC_FUNCTION_STARTS',
                    'method_sha256': manifest[METHOD]['sha256']}
        if any(summary.get(k) != v for k, v in expected.items()):
            raise ValueError('Linker-starts target, schema or method identity mismatch')
        status, count = summary.get('status'), summary.get('declared_start_count')
        if status not in ('present', 'absent') or type(count) is not int or count < 0:
            raise ValueError('Invalid declared-starts status or count')
        if (status == 'present') != ('addresses.tsv' in manifest):
            raise ValueError('Linker-starts status and table availability disagree')
        actual, first, last, previous = 0, None, None, -1
        if status == 'present':
            with (capture / 'addresses.tsv').open(newline='') as stream:
                table = csv.DictReader(stream, delimiter='\t')
                if table.fieldnames != ['address', 'file_offset', 'segment', 'uleb_file_offset']:
                    raise ValueError('Unexpected declared-starts table columns')
                for row in table:
                    entry = row['address']
                    if None in row or any(value is None for value in row.values()) or not re.fullmatch('0x[0-9a-f]+', entry):
                        raise ValueError('Invalid declared-starts row')
                    number = int(entry, 16)
                    if hex(number) != entry or not previous < number < 2**64:
                        raise ValueError('Declared starts are not canonical increasing addresses')
                    actual += 1
                    first = entry if first is None else first
                    last, previous = entry, number
        if (count, summary.get('first_address'), summary.get('last_address')) != (actual, first, last):
            raise ValueError('Declared-starts summary disagrees with table')
        links = ([['Address table (TSV)', href(capture / 'addresses.tsv')]] if status == 'present' else [])
        links += [['Summary and limitations', href(capture / 'summary.json')],
                  ['Provenance manifest', href(capture / 'manifest.json')],
                  ['Captured extraction method', href(capture / METHOD)]]
        return {'state': 'sealed', 'status': status, 'count': count, 'links': links}, [capture / 'manifest.json', *(capture / name for name in manifest)]
    except (ValueError, TypeError, KeyError, AttributeError, OSError, csv.Error) as error:
        return {'state': 'invalid', 'error': str(error)}, []
