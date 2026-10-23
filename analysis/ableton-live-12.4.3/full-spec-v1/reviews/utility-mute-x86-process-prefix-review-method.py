"""Independent fixed32B data review; no supplied methods, tools or target follow."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

B = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P = B / 'depth-utility-mute-x86-process-prefix-data'
R = B / 'reviews'


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def load(path):
    return json.loads(path.read_text())


def main():
    ep, rp = R / 'utility-mute-x86-process-prefix-review-evidence.json', R / 'utility-mute-x86-process-prefix-review.json'
    assert not ep.exists() and not rp.exists()
    inputs = load(P / 'before-map.json')
    assert len(inputs) == 5 and inputs == load(P / 'after-map.json')
    paths = {Path(row['path']) for row in inputs} | set(P.iterdir()) | {Path(__file__).resolve()}
    before = [identity(path) for path in sorted(paths)]
    for row in inputs:
        assert identity(Path(row['path'])) == row
    manifest, selection = load(P / 'manifest.json'), load(P / 'selection.json')
    assert {row['path'] for row in manifest['files']} == {x.name for x in P.iterdir() if x.name != 'manifest.json'}
    for row in manifest['files']:
        got = identity(P / row['path'])
        assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    assert selection['va'] == '0x104b8c7b0' and selection['file_offset'] == 0x4b8c7b0 and selection['length'] == 32
    assert identity(Path(selection['peer']['path'])) == selection['peer']
    assert selection['peer']['sha256'] == '5cb348cd252efdb4ea4c7fbd364bdb24d47db9a94ff67d532b011cfb2f963bc9'
    assert identity(Path(selection['method']['path'])) == selection['method']
    image, header_provider = Path(inputs[0]['path']), Path(inputs[1]['path'])
    metadata = load(header_provider)
    assert identity(image) == metadata['image']
    with image.open('rb') as stream:
        header = stream.read(32)
        vals = struct.unpack('<IiiIIIII', header)
        assert header.hex() == metadata['header_hex'] and vals[:3] == (0xfeedfacf, 0x1000007, 3) and vals[4:6] == (54, 6832)
        commands = stream.read(6832)
        assert hashlib.sha256(commands).hexdigest() == metadata['load_commands_sha256']
        cursor, segments = 0, []
        for _ in range(54):
            command, size = struct.unpack_from('<II', commands, cursor)
            assert size >= 8 and cursor + size <= len(commands)
            if command == 0x19:
                name, va, vs, fo, fs = struct.unpack_from('<16sQQQQ', commands, cursor + 8)
                assert fo + fs <= metadata['image']['bytes']
                segments.append((name.rstrip(b'\0').decode(), va, fo, fs))
            cursor += size
        assert cursor == len(commands)
        va = int(selection['va'], 16)
        matches = [s for s in segments if s[1] <= va and va + 32 <= s[1] + s[3]]
        assert matches == [('__TEXT', 0x100000000, 0, 111357952)]
        assert va - matches[0][1] + matches[0][2] == selection['file_offset']
        stream.seek(selection['file_offset'])
        raw = stream.read(32)
    assert raw.hex() == '0f57c080bfcf000000000f8577030000554889e58b87c80000004883f8030f87'
    result = load(P / 'result.json')
    assert result['bytes'] == raw.hex() and result['va'] == selection['va'] and result['analysis'] == 'RAW DATA ONLY; no instruction or output claim'
    assert result['original_calls'] == result['decoder_children'] == 0
    fields = [
        (0, 3, '0f57c0', 'XORPS XMM0,XMM0: unprefixed0f57/register ModRMc0'),
        (3, 10, '80bfcf00000000', 'CMP byte[RDI+207],imm8 zero:80 /7,ModRMbf mod2/reg7/rm7,disp32cf000000,imm00'),
        (10, 16, '0f8577030000', 'JNE rel32:0f85, littleendian displacement887'),
        (16, 17, '55', 'PUSH RBP'),
        (17, 20, '4889e5', 'MOV RBP,RSP:REX.W89 ModRMe5 mod3/reg4/rm5'),
        (20, 26, '8b87c8000000', 'MOV EAX,dword[RDI+200]:noREX.W,8b ModRM87 mod2/reg0/rm7'),
        (26, 30, '4883f803', 'CMP RAX,signextended imm8 3:REX.W83 /7 ModRMf8 mod3/reg7/rm0')]
    for lo, hi, code, _ in fields:
        assert raw[lo:hi].hex() == code
    modrm = lambda n: (n >> 6, (n >> 3) & 7, n & 7)
    assert modrm(0xc0) == (3, 0, 0) and modrm(0xbf) == (2, 7, 7)
    assert modrm(0xe5) == (3, 4, 5) and modrm(0x87) == (2, 0, 7) and modrm(0xf8) == (3, 7, 0)
    displacement = int.from_bytes(raw[12:16], 'little', signed=True)
    target = va + 16 + displacement
    assert displacement == 0x377 and target == 0x104b8cb37
    assert raw[30:] == bytes.fromhex('0f87')
    after = [identity(path) for path in sorted(paths)]
    assert before == after
    evidence = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='PASS',
        before=before, after=after, own_watch=len(paths), unchanged=True, input_pairs=5,
        payloads=4, tree=5, raw=raw.hex(), raw_sha256=hashlib.sha256(raw).hexdigest(),
        complete_instructions=[dict(start=hex(va + lo), end_exclusive=hex(va + hi), bytes=code, checked=description) for lo, hi, code, description in fields],
        complete_prefix_bytes=30, incomplete_tail_hex='0f87', signed_rel32=displacement,
        branch_target=hex(target), decoder_or_original_or_supplied_method_runs=0)
    ep.write_text(json.dumps(evidence, indent=2) + '\n')
    report = dict(schema=1, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        disposition='APPROVED PARTIAL FIXED32B DATA AND SEVEN COMPLETE LOCAL ENCODINGS ONLY',
        required_findings=[], author='Root', reviewer='delay_reverb_correction',
        roles='Reviewer authored parentOnMute metadata/preparation and preceding CalcMain actualpeer, not this Root32Bmethod/selection. Prior CalcMain nomination/argument claims are carried as reviewed context, not independently reapproved own prior work. Current fresh proof is this new32B selection only.',
        inputs=dict(manifest=identity(P / 'manifest.json'), method=selection['method'], prior_peer=selection['peer'], evidence=identity(ep), reviewer_method=identity(Path(__file__).resolve())),
        fresh_scope='Full3207B Rootmethod/all4payloads/manifest/fiveinputmaps; same32B/nativefield arithmetic and freshsameimageidentity/header54LC6832/uniqueTEXTmapping. No suppliedmethod/tool/decoder call.',
        verification=dict(payloads=4, tree=5, input_pairs=5, own_watch=len(paths), unchanged=True, selected_bytes=32, complete_prefix_bytes=30, complete_instructions=7, incomplete_tail_bytes=2),
        observations=[
            '0f57c0 is XORPS XMM0,XMM0.80bfcf00000000 is CMP byte[RDI+0xcf],0.0f8577030000 is JNE from next104b8c7c0 plus signed0x377 to104b8cb37. This is target nomination only; no target read.',
            'Linear fallthrough bytes then encode PUSH RBP;MOV RBP,RSP;MOV EAX,dword[RDI+0xc8];CMP RAX,3. These sevencomplete instructions occupy30B, under validmemory/stack/reached nonfaultingpath premises.',
            'Final0f87 is incomplete: required branchdisplacement bytes unread. No completed branch,target or fallthrough beyondthe32B is inferred.'
        ],
        limits=[
            'No actual receiver/state/comparisonoutcome/floatvalue/helperoutput/return/ABI/type/class/nativeextent or publicUtilityMute law inferred. No originalcall, candidategrade or completion; all38application outcomesU/null/unexecuted.',
            'XORPS local selfoperation is not returnedzero/output/silence proof. No branchdestination,remainingbytes/callee/global/CalcMain suffix or extra window/sourcebody read.',
            'Five recorded inputpairs and stated current ownwatch only; no globalpreservation/pretry/catastrophicI/O/runtimeprocess claim.'
        ])
    rp.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(report=identity(rp), evidence=identity(ep), own_watch=len(paths)), indent=2))


if __name__ == '__main__':
    main()
