"""Retain selected existing Ghidra records unchanged; never runs reference code."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORPUS = Path('/var/tmp/sound-analysis/corpus/decomp')
PIN = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
WANTED = '''102fbe25c 102fbe3a0 102fbe580 102fbe650 102fbe73c 102fbe830
102fbe964 102fbebd8 102fbec58 102fbf160 102fbf19c 102fbf220 102fbf340
102fbf38c 102fbf644 102fbf70c 102fbf860 102fbf8c4 102fbf9a0 102fbfb5c
102fbfc78 102fbfce4 102fbfd80 102fbfe54 102fbff98 102fc01ac 102fc0294
102fc04dc 102fc070c 102fc0a38 102fc0e2c 102fcc390 102fccc48 102fcccac
102fccd20 102fccd24 102fccd28 102fccda0 102fccdc0 102fccddc 102fccdf4
102fcce00 102fcce58 101b4456c 101b45c18 101ab4ee4 101a541a4 101ab4558
1011afd78 101df082c 102f999fc'''.split()
wanted = {'0x' + entry for entry in WANTED}
assert len(wanted) == len(WANTED)
run = json.loads((CORPUS / 'run.json').read_bytes())
assert run['executable_sha256'] == PIN
rows, locators = {}, []
for number in [679, 1158, 1181, 1220, 1221, 1371, 2293, 2302, 2303, 2305, 2306]:
    source = CORPUS / 'chunks' / f'chunk-{number:05}.jsonl'
    for line_number, raw in enumerate(source.read_bytes().splitlines(keepends=True), 1):
        record = json.loads(raw)
        if record['entry'] not in wanted:
            continue
        assert record['entry'] not in rows
        assert hashlib.sha256(record['code'].encode()).hexdigest() == record['code_sha256']
        assert not record['partial_code'] and not record['timed_out']
        rows[record['entry']] = raw
        locators.append({'entry': record['entry'], 'source': str(source),
                         'source_line': line_number, 'record_sha256': hashlib.sha256(raw).hexdigest(),
                         'code_sha256': record['code_sha256'], 'warnings': record['warnings']})
assert set(rows) == wanted, sorted(wanted - rows.keys())
ordered = sorted(rows, key=lambda entry: int(entry, 16))
(HERE / 'live-records.jsonl').write_bytes(b''.join(rows[entry] for entry in ordered))
for index, entry in enumerate(ordered, 1):
    next(row for row in locators if row['entry'] == entry)['retained_line'] = index
(HERE / 'record-locators.json').write_text(json.dumps(sorted(locators, key=lambda row: row['retained_line']), indent=2) + '\n')
shutil.copyfile(CORPUS / 'run.json', HERE / 'corpus-run.json')
for label, rel in [('bundle-identities.json', 'r2/h4-devices-v1/out/bundles.json'),
                   ('n5-manifest.json', 'r2/n5-device-mapping-v1/manifest.json')]:
    shutil.copyfile(ROOT / rel, HERE / label)
print(f'Retained {len(rows)} unchanged source records; source/code digests and completeness checked.')
