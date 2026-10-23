"""Three fixed call targets: metadata only, never read their instruction bytes."""
from pathlib import Path
import datetime
import hashlib
import json
import struct
import sys

BASE = Path(__file__).resolve().parents[1]
STEM = 'corpus-x86-create-selected-import-metadata-2026-10-20'
OUT = BASE / 'queries' / (STEM + '.json')
IMAGE = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus')
TARGETS = (0x2cc0c, 0x2cccc, 0x2cd20)


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def bounded(offset, size, total):
    assert type(offset) is int and type(size) is int
    assert 0 <= offset <= total and 0 <= size <= total - offset


def main():
    assert sys.argv[1:] == ['--retain-selected'] and not OUT.exists()
    source = BASE / 'depth-apple-macho-format-source'
    metadata_path = BASE / 'queries/corpus-x86-selected-export-metadata-2026-10-20.json'
    actual = BASE / 'depth-corpus-x86-create-entry-instructions/manifest.json'
    assessment = BASE / 'reviews/corpus-x86-create-entry-root-actual-assessment.json'
    providers = sorted({IMAGE, metadata_path, actual, assessment, Path(__file__)} |
                       {p for p in source.iterdir() if p.is_file()})
    before = [pin(p) for p in providers]
    expected = json.loads(metadata_path.read_text())
    fat = IMAGE.read_bytes()
    assert len(fat) == 527152 and hashlib.sha256(fat).hexdigest() == '2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422'
    assert struct.unpack_from('>II', fat) == (0xcafebabe, 2)
    arches = [struct.unpack_from('>IIIII', fat, 8 + 20 * i) for i in range(2)]
    selected = [a for a in arches if a[:2] == (0x1000007, 3)]
    assert len(selected) == 1 and selected[0][2:] == (16384, 250352, 14)
    data = fat[16384:16384 + 250352]
    assert hashlib.sha256(data).hexdigest() == expected['slice']['sha256']
    header = struct.unpack_from('<8I', data)
    assert header[:6] == (0xfeedfacf, 0x1000007, 3, 8, 14, 1696)
    assert data[:32].hex() == expected['slice']['header_hex']
    assert hashlib.sha256(data[32:1728]).hexdigest() == expected['slice']['load_commands_sha256']
    cursor, sections, segments, libraries, symtabs, dysymtabs = 32, [], [], [], [], []
    for index in range(14):
        cmd, size = struct.unpack_from('<II', data, cursor)
        assert size >= 8 and size % 8 == 0
        bounded(cursor, size, 1728)
        if cmd == 0x19:
            name, va, vs, fo, fs, mp, ip, ns, flags = struct.unpack_from('<16sQQQQiiII', data, cursor + 8)
            assert size == 72 + 80 * ns
            bounded(fo, fs, len(data))
            segments.append(dict(name=name.rstrip(b'\0').decode(), va=va, vmsize=vs, fileoff=fo, filesize=fs))
            for j in range(ns):
                pos = cursor + 72 + 80 * j
                sn, sg, addr, count, off, align, reloc, nreloc, flags, r1, r2, r3 = struct.unpack_from('<16s16sQQ8I', data, pos)
                sections.append(dict(name=sn.rstrip(b'\0').decode(), segment=sg.rstrip(b'\0').decode(), address=addr, size=count, fileoff=off, flags=flags, reserved1=r1, reserved2=r2, raw_header_hex=data[pos:pos + 80].hex()))
        elif cmd == 2:
            assert size == 24
            symtabs.append(struct.unpack_from('<6I', data, cursor))
        elif cmd == 0xb:
            assert size == 80
            dysymtabs.append(struct.unpack_from('<20I', data, cursor))
        elif cmd in (0xc, 0x80000018, 0x8000001f, 0x80000023, 0x20):
            assert size >= 24
            libraries.append((cursor, size))
        cursor += size
    assert cursor == 1728 and len(symtabs) == len(dysymtabs) == 1
    _, _, symoff, nsyms, stroff, strsize = symtabs[0]
    indirectoff, indirectcount = dysymtabs[0][14:16]
    bounded(symoff, nsyms * 16, len(data))
    bounded(stroff, strsize, len(data))
    bounded(indirectoff, indirectcount * 4, len(data))
    linkedit = [s for s in segments if s['name'] == '__LINKEDIT']
    assert len(linkedit) == 1
    for off, length in ((symoff, nsyms * 16), (stroff, strsize), (indirectoff, indirectcount * 4)):
        assert linkedit[0]['fileoff'] <= off and off + length <= linkedit[0]['fileoff'] + linkedit[0]['filesize']
    results = []
    for target in TARGETS:
        matches = [s for s in sections if s['flags'] & 0xff == 8 and s['address'] <= target < s['address'] + s['size']]
        assert len(matches) == 1
        section = matches[0]
        width = section['reserved2']
        assert width > 0 and section['size'] % width == 0
        delta = target - section['address']
        assert delta % width == 0
        ordinal = section['reserved1'] + delta // width
        assert ordinal < indirectcount
        off = indirectoff + 4 * ordinal
        symbol_index = struct.unpack_from('<I', data, off)[0]
        assert symbol_index & 0xc0000000 == 0 and symbol_index < nsyms
        pos = symoff + 16 * symbol_index
        sx, typ, sect, desc, value = struct.unpack_from('<IBBHQ', data, pos)
        assert sx < strsize and typ & 0xe0 == 0 and typ & 0xe == 0 and typ & 1 and sect == 0
        end = data.find(b'\0', stroff + sx, stroff + strsize)
        assert end >= stroff + sx
        name = data[stroff + sx:end].decode('ascii')
        library_ordinal = desc >> 8 & 0xff
        assert header[6] & 0x80 and 1 <= library_ordinal <= len(libraries) and library_ordinal <= 0xfd
        lcpos, lcsize = libraries[library_ordinal - 1]
        nameoff = struct.unpack_from('<I', data, lcpos + 8)[0]
        assert 24 <= nameoff < lcsize
        libend = data.find(b'\0', lcpos + nameoff, lcpos + lcsize)
        assert libend >= lcpos + nameoff
        library = data[lcpos + nameoff:libend].decode('ascii')
        results.append(dict(target=hex(target), section=section, stub_index=delta // width, indirect_index=ordinal, indirect_slice_offset=off, indirect_raw_hex=data[off:off + 4].hex(), symbol_index=symbol_index, nlist_slice_offset=pos, nlist_raw_hex=data[pos:pos + 16].hex(), string_slice_offset=stroff + sx, name=name, name_nul_hex=data[stroff + sx:end + 1].hex(), n_type=typ, n_sect=sect, n_desc=desc, n_value=value, library_ordinal=library_ordinal, library=library, library_command_hex=data[lcpos:lcpos + lcsize].hex(), target_instruction_bytes_read=False))
    # Wrong-range and boundary controls exercise the only new shared range check.
    bounded(10, 0, 10)
    for bad in ((-1, 1, 10), (9, 2, 10), (0, -1, 10), (11, 0, 10)):
        try:
            bounded(*bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('Bad metadata bounds accepted')
    after = [pin(p) for p in providers]
    assert before == after
    result = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='PROPOSED_THREE_SELECTED_STUB_IMPORT_METADATA_ONLY_PENDING_INDEPENDENT_REVIEW', selection=[hex(t) for t in TARGETS], image=pin(IMAGE), slice_offset=16384, slice_bytes=len(data), symbol_table=dict(symoff=symoff, nsyms=nsyms, stroff=stroff, strsize=strsize, indirectoff=indirectoff, indirectcount=indirectcount), selected=results, source_format_manifest=pin(source / 'manifest.json'), method=pin(Path(__file__)), preservation=dict(before=before, after=after, unchanged=True), limits=['Exact metadata association only; no stub instructions/global/body decoded or target code executed.', 'Symbol name/library ordinal do not prove current runtime binding, callable ABI, valid arguments, allocation contract, result/object identity or behavior.', 'Only three selected symbol names retained; whole fat/slice bytes hashed opaque outside structural metadata reads.', 'No original/instrumentation/observer/numerical run, case, criterion or grade; all174+2modal omissions U.'], new_REQ_cases_grades=0, complete=False)
    with OUT.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(query=pin(OUT), selected=[dict(target=r['target'], name=r['name'], library=r['library']) for r in results], watched=len(before), unchanged=True)))


if __name__ == '__main__':
    main()
