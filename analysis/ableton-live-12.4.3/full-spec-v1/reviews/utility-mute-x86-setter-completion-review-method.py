"""Independent five-byte completion: hashes/header/map and explicit encoding fields only."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
REVIEWS = BASE / 'reviews'
PACKET = BASE / 'depth-utility-mute-x86-setter-completion-data'


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def load(path):
    return json.loads(path.read_text())


def classify(prefix, completion):
    if prefix != bytes.fromhex('554889e54088b7cf') or len(completion) != 5 or completion[-2:] != bytes.fromhex('5dc3'):
        return None
    combined = prefix + completion
    rex, opcode, modrm = combined[4:7]
    assert rex == 0x40 and opcode == 0x88
    assert (modrm >> 6, (modrm >> 3) & 7, modrm & 7) == (2, 6, 7)
    displacement = int.from_bytes(combined[7:11], 'little', signed=True)
    return combined, displacement


def main():
    ep = REVIEWS / 'utility-mute-x86-setter-completion-review-evidence.json'
    rp = REVIEWS / 'utility-mute-x86-setter-completion-review.json'
    assert not ep.exists() and not rp.exists()
    selection, manifest = load(PACKET / 'selection.json'), load(PACKET / 'manifest.json')
    inputs = load(PACKET / 'before-map.json')
    assert len(inputs) == 6 and inputs == load(PACKET / 'after-map.json')
    paths = {Path(r['path']) for r in inputs} | set(PACKET.iterdir()) | {Path(__file__).resolve()}
    before = [identity(p) for p in sorted(paths)]
    for row in inputs:
        assert identity(Path(row['path'])) == row
    assert {r['path'] for r in manifest['files']} == {p.name for p in PACKET.iterdir() if p.name != 'manifest.json'}
    for row in manifest['files']:
        got = identity(PACKET / row['path'])
        assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    assert selection['va'] == '0x104b8c768' and selection['file_offset'] == 0x4b8c768 and selection['length'] == 5
    assert selection['peer']['sha256'] == '4ec1e107488946c713b09c02a36428742368e65f27dda5bd67fdef73a2f3d482'
    image, header_provider, peer, previous, method, _ = [Path(r['path']) for r in inputs]
    assert identity(peer) == selection['peer'] and identity(method) == selection['method']
    metadata = load(header_provider)
    assert identity(image) == metadata['image']
    assert metadata['image']['bytes'] == 163716848 and metadata['image']['sha256'] == '1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0'
    with image.open('rb') as stream:
        header = stream.read(32)
        values = struct.unpack('<IiiIIIII', header)
        assert values[:3] == (0xfeedfacf, 0x1000007, 3) and values[4:6] == (54, 6832)
        assert header.hex() == metadata['header_hex']
        commands = stream.read(6832)
        assert hashlib.sha256(commands).hexdigest() == metadata['load_commands_sha256']
        cursor, segments = 0, []
        for _ in range(54):
            cmd, size = struct.unpack_from('<II', commands, cursor)
            assert size >= 8 and cursor + size <= len(commands)
            if cmd == 0x19:
                name, va, vs, fo, fs = struct.unpack_from('<16sQQQQ', commands, cursor + 8)
                assert fo + fs <= metadata['image']['bytes']
                segments.append((name.rstrip(b'\0').decode(), va, fo, fs))
            cursor += size
        assert cursor == len(commands)
        va = int(selection['va'], 16)
        match = [s for s in segments if s[1] <= va and va + 5 <= s[1] + s[3]]
        assert match == [('__TEXT', 0x100000000, 0, 111357952)]
        assert match[0][2] + va - match[0][1] == selection['file_offset']
        stream.seek(selection['file_offset'])
        raw = stream.read(5)
    assert raw.hex() == '0000005dc3'
    prefix = bytes.fromhex(load(previous)['bytes'])
    combined, displacement = classify(prefix, raw)
    assert combined.hex() == '554889e54088b7cf0000005dc3' and displacement == 207
    result = load(PACKET / 'result.json')
    assert result['va'] == selection['va'] and result['bytes'] == raw.hex()
    assert result['analysis'] == dict(pattern='PUSH RBP; MOV RBP,RSP; MOV byte [RDI+disp32],SIL; POP RBP; RET', displacement=207, combined_bytes=combined.hex())
    assert result['original_calls'] == result['decoder_children'] == 0
    assert classify(prefix, raw[:-1] + b'\xc2') is None
    assert classify(prefix, raw[:3] + b'\x5b\xc3') is None
    assert classify(prefix, raw[:-1]) is None
    assert 0x48 + displacement == 0x117
    after = [identity(p) for p in sorted(paths)]
    assert before == after
    evidence = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='PASS',
        payloads=4, tree=5, input_pairs=6, own_watch=len(paths), before=before, after=after,
        unchanged=True, new_raw=raw.hex(), combined_carried_prefix_and_new_completion=combined.hex(),
        modrm=dict(mod=2, reg=6, rm=7), rex='0x40: low byte SIL selected, no extension bits',
        displacement=207, composed_offset='0x117', rejected_literal_controls=3,
        supplied_method_executed=False, decoder_children=0, original_calls=0)
    ep.write_text(json.dumps(evidence, indent=2) + '\n')
    report = dict(schema=1, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        disposition='APPROVED PARTIAL FIVE-BYTE COMPLETION AND CONDITIONAL LOCAL ENCODING ONLY',
        required_findings=[], author='Root', reviewer='delay_reverb_correction',
        roles='Reviewer authored preceding metadata/preparation and reviewed six-byte tail jump; not current completion selector/method author. Prior eight bytes/image facts are carried through the fully read Synthesis4454B peer; current new semantic byte read is five bytes only.',
        inputs=dict(manifest=identity(PACKET / 'manifest.json'), method=selection['method'], peer=selection['peer'], previous_prefix_result=identity(previous), evidence=identity(ep), reviewer_method=identity(Path(__file__).resolve())),
        fresh_scope='Full3966B Root method/all four payloads/manifest/six-input maps and full4454B Synthesis peer. Fresh same mainLive identity/header54LC6832/uniqueTEXTmapping and five selected bytes only. No supplied method/tool executed.',
        verification=dict(payloads=4, tree=5, input_pairs=6, own_watch=len(paths), unchanged=True, controls=3, new_bytes_read=5, decoder_or_original_calls=0),
        observations=[
            'Carried eight-byte554889e54088b7cf plus new0000005dc3 yields13 bytes: PUSH RBP; MOV RBP,RSP; REX40/MOV88/ModRMb7(mod2,reg6,rm7) stores SIL to byte[RDI+signed disp32 cf000000=207]; POP RBP; RET. REX presence makes byte register6 SIL rather than DH.',
            'Under valid reached normal stack/call/return and no-interference premises this is a local store/return encoding; no argument value or actual call occurred.',
            'If the separately reviewed earlier OnMute unequal path reaches its tail jump with K=P+0x48 and its ESI carrier intact, this local store address is K+0xcf=P+0x117. This conditional address algebra establishes no real object identity, application binding, actual float result or setter semantics.'
        ],
        limits=[
            'Prior eight-byte UNKNOWN investigation remains immutable and correct as-of its selection; completion is separately selected new evidence.',
            'No other image bytes, remaining OnMute suffix, global/CalcMain/callee/target/source/runtime execution or native function extent read/inferred.',
            'No actual ABI/callability/class/parameter/value/default/audio/publicMute/arm64 equivalence or compatibility grade. All38Utility outcomes remainU/null/unexecuted.',
            'Six fixed recorded input pairs and stated current own watch only; no global preservation, pretry or catastrophic-I/O guarantee.'
        ])
    rp.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(report=identity(rp), evidence=identity(ep), own_watch=len(paths)), indent=2))


if __name__ == '__main__':
    main()
