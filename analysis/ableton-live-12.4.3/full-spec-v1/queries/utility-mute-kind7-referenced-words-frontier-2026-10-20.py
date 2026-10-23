"""Retain exactly one selected 16-byte data interval; no target traversal."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import struct
import sys

ROOT = Path('/home/ollie/Documents/sound')
HERE = Path(__file__).resolve().parent
STEM = 'utility-mute-kind7-referenced-words-frontier-2026-10-20'
IMAGE = ROOT / 'analysis/ableton-live-12.4.3/derived/Live.arm64'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
START, END = 0x106793e20, 0x106793e30
PRIOR = HERE / 'utility-mute-kind7-dispatch-block-frontier-2026-10-20.json'
REVIEW = HERE.parent / 'reviews/utility-mute-kind7-dispatch-block-review.json'
PARENT = HERE / 'utility-mute-kind7-preceding-words-frontier-2026-10-20.json'
PARENT_REVIEW = HERE.parent / 'reviews/utility-mute-kind7-preceding-words-review.json'


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    if sys.argv[1:] != ['--retain-selected']:
        raise SystemExit('Only --retain-selected is supported')
    result_path, raw_path = HERE / (STEM + '.json'), HERE / (STEM + '.bin')
    assert not result_path.exists() and not raw_path.exists()
    prior = json.loads(PRIOR.read_text())
    reviewed = json.loads(REVIEW.read_text())
    assert reviewed['disposition'] == 'APPROVED_PARTIAL_LITERAL_DATA_ONLY'
    assert identity(PRIOR)['sha256'] == reviewed['reviewed_query']['sha256']
    assert identity(REVIEW)['sha256'] == '38d3189ba7ef8a6b4c834699796a72c5c55af9a7e215e731a1ddc8e348db04e7'
    parent = json.loads(PARENT.read_text())
    parent_review = json.loads(PARENT_REVIEW.read_text())
    assert identity(PARENT)['sha256'] == 'f86876e575663d5a4fb60f94e5c042d077c5f74cbfa12ae11c1663dc460ebbc9'
    assert identity(PARENT_REVIEW)['sha256'] == 'c178ca4ccfb0f8865adb331036fb3da92da89454508d76467d316a9cd50c4463'
    assert parent_review['reviewed_query']['sha256'] == identity(PARENT)['sha256']
    assert int(parent['block']['words'][1]['u64_little_endian'], 16) == START
    parent_method, parent_raw = Path(parent['method']['path']), Path(parent['retained_raw']['path'])
    for provider in [parent['method'], parent['retained_raw']]:
        actual = identity(Path(provider['path']))
        assert all(actual[key] == provider[key] for key in ['bytes', 'sha256'])
    context = prior['conditional_construction_association']
    source = ROOT / context['provider']['path']
    source_review = ROOT / context['review']['path']
    index_manifest = json.loads((INDEX / 'manifest.json').read_text())
    paths = [IMAGE, PRIOR, REVIEW, source, source_review, Path(__file__),
             INDEX / 'manifest.json', INDEX / 'aliases.jsonl', INDEX / 'vtables.jsonl',
             PARENT, PARENT_REVIEW, parent_method, parent_raw]
    before = [identity(path) for path in paths]
    assert before[0]['bytes'] == 149711904
    assert before[0]['sha256'] == '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
    assert index_manifest['executable_sha256'] == before[0]['sha256']
    for filename in ['aliases.jsonl', 'vtables.jsonl']:
        actual = identity(INDEX / filename)
        assert all(actual[key] == index_manifest['files'][filename][key]
                   for key in ['bytes', 'sha256'])
    for provider in [context['provider'], context['review']]:
        actual = identity(ROOT / provider['path'])
        assert all(actual[key] == provider[key] for key in ['bytes', 'sha256'])
    code = json.loads(source.read_text())['full_selected_record']['record']['code']
    assert code.splitlines(keepends=True)[context['line_1based'] - 1] == context['exact_text']
    assert hashlib.sha256(context['exact_text'].encode()).hexdigest() == context['text_sha256']
    with IMAGE.open('rb') as handle:
        header = handle.read(32)
        magic, cpu, subtype, filetype, count, length, flags, reserved = struct.unpack('<8I', header)
        assert (magic, cpu, subtype, filetype, count, length) == (0xfeedfacf, 0x100000c, 0, 2, 53, 6944)
        commands = handle.read(length)
        assert header.hex() == prior['header']['raw_hex']
        assert hashlib.sha256(commands).hexdigest() == prior['load_commands']['sha256']
        cursor, segments, command_rows = 0, [], []
        for index in range(count):
            command, size = struct.unpack_from('<II', commands, cursor)
            assert size >= 8 and cursor + size <= length
            command_rows.append(dict(index_0based=index, file_offset=32 + cursor,
                                     command=hex(command), cmdsize=size))
            if command == 0x19:
                name = commands[cursor + 8:cursor + 24].split(b'\0', 1)[0].decode()
                vm, vs, offset, size_file, maxprot, initprot, sections, sf = struct.unpack_from('<QQQQIIII', commands, cursor + 24)
                assert offset + size_file <= before[0]['bytes']
                segments.append(dict(command_index_0based=index, command_file_offset=32 + cursor,
                                     name=name, vmaddr=hex(vm), vmsize=vs, fileoff=offset,
                                     filesize=size_file, maxprot=maxprot, initprot=initprot,
                                     nsects=sections, flags=sf))
            cursor += size
        assert cursor == length
        assert segments == prior['load_commands']['segments']
        assert command_rows == prior['load_commands']['command_metadata']
        matched = [segment for segment in segments
                   if int(segment['vmaddr'], 16) <= START
                   and END <= int(segment['vmaddr'], 16) + min(segment['vmsize'], segment['filesize'])]
        assert len(matched) == 1 and matched[0]['name'] == '__DATA_CONST'
        offset = matched[0]['fileoff'] + START - int(matched[0]['vmaddr'], 16)
        assert offset == 108609056 and offset + END - START <= before[0]['bytes']
        handle.seek(offset)
        raw = handle.read(END - START)
    assert len(raw) == 16
    words = []
    for index in range(2):
        piece = raw[index * 8:(index + 1) * 8]
        words.append(dict(physical_index_0based=index, va=hex(START + 8 * index),
                          file_offset=offset + 8 * index, raw_hex=piece.hex(),
                          sha256=hashlib.sha256(piece).hexdigest(),
                          u64_little_endian=hex(struct.unpack('<Q', piece)[0]),
                          role='Unclassified physical unsigned data value.'))
    targets = {int(word['u64_little_endian'], 16) for word in words if int(word['u64_little_endian'], 16)}
    assert len(targets) <= 2
    metadata = []
    for filename, key in [('aliases.jsonl', 'entry'), ('vtables.jsonl', 'address')]:
        matches, total = [], 0
        with (INDEX / filename).open('rb') as handle:
            for total, line in enumerate(handle, 1):
                record = json.loads(line)
                value = record.get(key)
                try:
                    address = int(value, 16) if isinstance(value, str) else None
                except ValueError:
                    address = None
                if address in targets:
                    matches.append(dict(line_1based=total, raw_sha256=hashlib.sha256(line.rstrip(b'\r\n')).hexdigest(),
                                        exact_address=value, metadata={k: record[k] for k in
                                        ['entry', 'address', 'name', 'external', 'thunk', 'thunk_target',
                                         'thunk_target_name', 'library', 'symbols', 'stop'] if k in record}))
        assert total == index_manifest['files'][filename]['lines']
        metadata.append(dict(provider=identity(INDEX / filename), address_field=key,
                             checked_rows=total, matching_rows=len(matches), records=matches))
    after = [identity(path) for path in paths]
    assert before == after
    result = dict(retained_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  status='PARTIAL_LITERAL_DATA_AND_EXACT_METADATA_ONLY_PENDING_ROOT_REVIEW',
                  selection=dict(start_va=hex(START), end_va_exclusive=hex(END), bytes=16,
                                 scope='Exactly two physical words at the value of the retained preceding query second word; no pointer-layout, type or runtime-role inference.'),
                  source_export_utc=None, image=before[0], header=dict(raw_hex=header.hex(), bytes=32,
                  sha256=hashlib.sha256(header).hexdigest(), ncmds=count, sizeofcmds=length),
                  load_commands=dict(bytes=length, sha256=hashlib.sha256(commands).hexdigest(),
                                     command_metadata=command_rows, segments=segments),
                  mapping=dict(segment=matched[0], matching_segment_count=1, file_offset=offset,
                               file_end_exclusive=offset + 16, formula='fileoff + (VA - vmaddr)', fully_file_backed=True),
                  block=dict(raw_hex=raw.hex(), bytes=16, sha256=hashlib.sha256(raw).hexdigest(), words=words),
                  construction_context=context,
                  construction_context_scope='Historical prior64B source context only. The deictic phrase This query in its copied claim refers to that prior query, not this new16B selection.',
                  prior_64byte_query=identity(PRIOR), prior_64byte_review=identity(REVIEW),
                  selected_parent_word=dict(provider=identity(PARENT), pointer='/block/words/1/u64_little_endian',
                                            value=hex(START), review=identity(PARENT_REVIEW), raw=identity(parent_raw)),
                  method_delta=dict(parent=identity(parent_method),
                                    unified_diff=''.join(difflib.unified_diff(parent_method.read_text().splitlines(True),
                                                                           Path(__file__).read_text().splitlines(True),
                                                                           fromfile=parent_method.name, tofile=Path(__file__).name))),
                  metadata_lookup=dict(nonzero_targets=[hex(target) for target in sorted(targets)],
                                       exact_top_level_address_only=True, indexes=metadata,
                                       no_target_data_string_body_read=True),
                  limits=['Physical word value and address selection prove no RTTI/header/offset-to-top/typeinfo/type-name/table-boundary/slot role.',
                          'Previously recovered U firstword literal store is conditional source context, not actual runtime vptr identity.',
                          'Exact index availability/missing rows do not prove runtime absence or type identity; index completeness unknown.',
                          'No further pointer, word, string, target body, instruction, decoder, native, numerical or runtime follow.'],
                  next_frontier='STOP pending Root review and separately explicit selection; no metadata label promoted to object/type/public meaning.',
                  preservation=dict(before=before, after=after, unchanged=True),
                  documentary_expected=None, documentary_comparison=None, actual_expected=None,
                  actual_comparison=None, all38_Utility_application_outcomes='U/unexecuted',
                  new_normative_ids=0, new_cases_or_grades=0, complete=False)
    with raw_path.open('xb') as handle:
        handle.write(raw)
    result['retained_raw'] = identity(raw_path)
    result['method'] = identity(Path(__file__))
    with result_path.open('x') as handle:
        handle.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(query=identity(result_path), raw=identity(raw_path),
                          method=identity(Path(__file__)), values=[word['u64_little_endian'] for word in words],
                          matches=[item['matching_rows'] for item in metadata], watched=len(before))))


if __name__ == '__main__':
    main()
