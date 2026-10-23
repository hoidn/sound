"""Independent data/hash/header and sixteen fixed x86 encoding checks only."""
from pathlib import Path
import datetime
import hashlib
import json
import struct

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
A = BASE / 'depth-utility-mute-x86-calcmain-entry-instructions'
O = BASE / 'reviews/utility-mute-x86-calcmain-entry-selected-execution'
P = BASE / 'depth-utility-mute-x86-calcmain-entry-preparation'
R = BASE / 'reviews'


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def load(path):
    return json.loads(path.read_text())


def inventory(directory):
    manifest = load(directory / 'manifest.json')
    assert {row['path'] for row in manifest['files']} == {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file() and p != directory / 'manifest.json'}
    for row in manifest['files']:
        got = identity(directory / row['path'])
        assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    return len(manifest['files'])


def main():
    ep = R / 'utility-mute-x86-calcmain-static-actual-review-evidence.json'
    rp = R / 'utility-mute-x86-calcmain-static-actual-review.json'
    assert not ep.exists() and not rp.exists()
    ab, aa = load(A / 'before-map.json')['files'], load(A / 'after-map.json')['files']
    ob, oa = load(O / 'before-map.json'), load(O / 'after-map.json')
    assert len(ab) == 70 and ab == aa and len(ob) == 3585 and ob == oa
    peers = [R / 'utility-mute-x86-calcmain-code-preflight-review.json', R / 'utility-mute-x86-calcmain-root-actual-assessment.json']
    paths = {Path(row['path']) for row in ob + ab} | set(A.iterdir()) | set(O.iterdir()) | set(P.iterdir()) | set(peers) | {Path(__file__).resolve()}
    before = [identity(p) for p in sorted(paths)]
    for row in ab + ob + load(O / 'pins.json'):
        assert identity(Path(row['path'])) == row
    assert inventory(A) == 12 and inventory(O) == 11
    selection = load(O / 'selection.json')
    assert selection['preparation']['sha256'] == '68b37b95e054245c1cbda56096b310b3e2b5577756d03a462437c9a1439a52b1'
    for k in ['preparation', 'collector', 'root_preflight', 'peer_preflight', 'wrapper', 'wrapper_parent']:
        assert identity(Path(selection[k]['path'])) == selection[k]
    expected_wrapper = Path(selection['wrapper_parent']['path']).read_text()
    for old, new in selection['literal_operations']:
        assert expected_wrapper.count(old) == 1
        expected_wrapper = expected_wrapper.replace(old, new)
    assert expected_wrapper.encode() == (O / 'execute-selected-once.py').read_bytes()
    assert (A / 'collect-once.py').read_bytes() == (P / 'collect-once.py').read_bytes()
    metadata = load(P / 'header-map.json')
    image = Path(metadata['image']['path'])
    assert identity(image) == metadata['image']
    start, length = 0x10224ef20, 240
    with image.open('rb') as stream:
        header = stream.read(32)
        assert header.hex() == metadata['header_hex']
        vals = struct.unpack('<IiiIIIII', header)
        assert vals[:3] == (0xfeedfacf, 0x1000007, 3) and vals[4:6] == (54, 6832)
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
        matches = [s for s in segments if s[1] <= start and start + length <= s[1] + s[3]]
        assert matches == [('__TEXT', 0x100000000, 0, 111357952)]
        offset = matches[0][2] + start - matches[0][1]
        assert offset == 0x224ef20 == metadata['slice_file_offset']
        stream.seek(offset)
        same_window = stream.read(240)
    raw = (A / 'calcmain-entry-240.bin').read_bytes()
    assert raw == same_window and hashlib.sha256(raw).hexdigest() == '6f87d60761066df45732879aa67b7c2e259f1d63f3a817334295c7d36b110bfa'
    # Selected sixteen instruction encodings only; remaining184 bytes stay opaque.
    expected = [
        ('55', 'push rbp'), ('4889e5', 'mov rbp, rsp'), ('53', 'push rbx'), ('50', 'push rax'),
        ('4889fb', 'mov rbx, rdi'), ('4883c748', 'add rdi, 0x48'),
        ('488b4330', 'mov rax, qword [rbx+0x30]'), ('488b4b38', 'mov rcx, qword [rbx+0x38]'),
        ('f30f1000', 'movss xmm0, dword [rax]'), ('f30f1145f0', 'movss dword [rbp-0x10], xmm0'),
        ('f30f1001', 'movss xmm0, dword [rcx]'), ('f30f1145f4', 'movss dword [rbp-0x0c], xmm0'),
        ('488d75f0', 'lea rsi, qword [rbp-0x10]'), ('e860d89302', 'call 0x104b8c7b0'),
        ('0f134340', 'movlps qword [rbx+0x40], xmm0'), ('4883c408', 'add rsp, 0x08')]
    rows = load(A / 'calcmain-entry-240.stdout.json')
    assert len(rows) == 16
    used, verified = 0, []
    for row, (code, opcode) in zip(rows, expected):
        data = bytes.fromhex(code)
        assert type(row['offset']) is int and row['offset'] == start + used
        assert type(row['size']) is int and row['size'] == len(data) and row['bytes'] == code
        assert row['opcode'] == opcode and raw[used:used + len(data)] == data
        verified.append(dict(va=hex(start + used), bytes=code, checked_opcode=opcode))
        used += len(data)
    assert used == 56
    # Explicit ModRM/register/width checks independent of the supplied ESIL strings.
    modrm = lambda n: (n >> 6, (n >> 3) & 7, n & 7)
    assert modrm(0xfb) == (3, 7, 3)             # MOV64 RDI -> RBX
    assert modrm(0x43) == (1, 0, 3)             # RAX <- [RBX+disp8] / MOVLPS [RBX+disp8] <- XMM0
    assert modrm(0x4b) == (1, 1, 3)             # RCX <- [RBX+disp8]
    assert modrm(0x00) == (0, 0, 0) and modrm(0x01) == (0, 0, 1)
    assert modrm(0x45) == (1, 0, 5)             # MOVSS32 [RBP+signed disp8] <- XMM0
    assert int.from_bytes(b'\xf0', 'little', signed=True) == -16 and int.from_bytes(b'\xf4', 'little', signed=True) == -12
    assert modrm(0x75) == (1, 6, 5)             # LEA64 RSI <- [RBP-16]
    displacement = int.from_bytes(bytes.fromhex('60d89302'), 'little', signed=True)
    assert rows[13]['offset'] + 5 + displacement == 0x104b8c7b0
    assert rows[13]['jump'] == 0x104b8c7b0 and rows[13]['fail'] == rows[14]['offset']
    coverage = load(A / 'prefix-coverage.json')
    assert coverage == dict(rows=16, consumed_bytes=56, decoded_prefix_half_open=[hex(start), hex(start + 56)], uninterpreted_selected_bytes=184, selected_bytes=240, body_extent_claim=False)
    inner, outer = load(A / 'status.json'), load(O / 'receipt.json')
    assert inner['attempted_decoder_children'] == inner['returned_pid_children'] == 1 and inner['exit'] == 0 and inner['exception'] is None and inner['providers_unchanged'] is True
    assert outer['attempted_collector_launches'] == 1 and outer['returned_collector_pid'] == 406455 and outer['outer_wrapper_pid'] == 406454
    assert outer['exit'] == 0 and outer['exception'] is None and outer['timeout'] is False and outer['automatic_retry'] is False and outer['unchanged'] is True
    assert load(A / 'returned-pid.json')['pid'] == 406457
    assert load(O / 'collector-pid.json')['pid'] == 406455
    assert (A / 'calcmain-entry-240.stderr').read_bytes() == (O / 'collector.stderr').read_bytes() == b''
    assert load(O / 'collector.stdout.json') == inner
    iv, ov = load(A / 'invocation-before.json'), load(O / 'invocation-before.json')
    assert iv['timeout_seconds'] == 30 and ov['timeout_seconds'] == 55 and iv['core_limit'] == ov['inherited_RLIMIT_CORE'] == [0, 0]
    assert iv['stdin'] == ov['stdin'] == 'DEVNULL' and ov['start_new_session'] is True
    assert iv['environment'] == ov['environment'] == {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}
    assert iv['argv'] == [str(next(Path(r['path']) for r in load(P / 'inputs.json')['pins'] if r.get('role') == 'rizin')), '-NN','-n','-x','-f','-a','x86','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj 16',str(A / 'calcmain-entry-240.bin')]
    assert load(A / 'attempt.json')['argv'] == iv['argv'] and load(O / 'attempt.json')['argv'] == ov['argv']
    assert inner['started_utc'] < load(A / 'attempt.json')['utc'] < load(A / 'returned-pid.json')['utc'] < inner['finished_utc']
    assert selection['selected_utc'] < outer['started_utc'] < outer['finished_utc']
    after = [identity(p) for p in sorted(paths)]
    assert before == after
    evidence = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='PASS',
        before=before, after=after, own_watch=len(paths), unchanged=True, inner_pairs=70, outer_pairs=3585,
        actual_payloads=12, outer_payloads=11, wrapper_literal_inverse=4, same240B_identity=True,
        header_commands=54, loadcommand_bytes=6832, uniqueTEXT_mapping=True, rows=verified,
        occupied_bytes=56, opaque_suffix_bytes=184, call_rel32=displacement, target='0x104b8c7b0',
        original_or_decoder_or_supplied_tool_replays=0)
    ep.write_text(json.dumps(evidence, indent=2) + '\n')
    report = dict(schema=1, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        disposition='APPROVED PARTIAL STATIC SIXTEEN-ROW PREFIX ONLY', required_findings=[], author='Root', reviewer='delay_reverb_correction',
        roles='Current actual Root; current preparation Synthesis/codepeer Modulation. Reviewer authored parentOnMute preparation/metadata and earlier continuation reviews, not current CalcMain actual. Earlier codepeer loose parentOnMute=Synthesis attribution is qualified here: its parent was this reviewer; currentCalcMain author remains Synthesis. No renewal of parent self-approval.',
        inputs=dict(actual_manifest=identity(A / 'manifest.json'), outer_manifest=identity(O / 'manifest.json'),
            preparation=selection['preparation'], codepeer=selection['peer_preflight'], Root_assessment=identity(peers[1]), evidence=identity(ep), reviewer_method=identity(Path(__file__).resolve())),
        fresh_scope='Full5963B outer wrapper/fourliteral changes, copied collector comparison delta against previously fully read parent; all16 row bytes/opcode fields and56occupiedbytes; fullcurrent selection/receipts/invocations/status/coverage/manifests/6918B codepeer/authorassessment. Freshsame240binaryidentity/header54LC6832/uniqueTEXTmap;184suffixbytes opaque. All70inner3585outer recorded identities rechecked current and ownwatch unchanged. No supplied script/main/tool execution.',
        verification=dict(actual_payloads=12, actual_tree=13, outer_payloads=11, outer_tree=12, inner_pairs=70, outer_pairs=3585, own_watch=len(paths), unchanged=True, rows=16, occupied_bytes=56, opaque_suffix_bytes=184, wrapper_inverse=4),
        observations=[
            'PUSH RBP/MOV RBP,RSP/PUSH RBX/PUSH RAX establishes selected localframe; MOV RBX,RDI saves entryreceiver carrier and ADD RDI,0x48 forms an argument carrier.',
            'REX.W MOV loads64-bit pointers from[RBX+0x30]/[RBX+0x38] intoRAX/RCX; MOVSS copies32bits from each pointed address viaXMM0 into adjacent[RBP-0x10]/[RBP-0xc]. LEA RSI,RBP-0x10 addresses this pair.',
            'E8 signedrel32 from10224ef4b with next10224ef50 nominates104b8c7b0; no targetbody read. On normalreturn and preservedRBX/stack/nointerference premises, unprefixed0f13 MOVLPS writes low64XMM0 to[entry+0x40]. ADD RSP,8 follows. No fullreturn appears in this prefix.',
            'Actualonecollector/onedecoder exited0, recordedPIDs406455/406457 underouter406454; core0/DEVNULL/minimalenv/55outer30decoder/noautoretry. Recorded finite pairedmaps unchanged, no timeout/kill indicated.'
        ],
        limits=[
            'Valid entry/pointer/stack memory, reached path, nonfaulting SSE accesses, ordinary normalcallee return/preservedRBX/stack and nointerference are premises, not runtime observations.',
            'No helper output/actualscalarvalue/type/bothzero/nativeextent/class/actualpublicMute/processingroute/ABI/arm64equivalence/audio/default/compatibility grade. All38application outcomesU/null/unexecuted.',
            'No callee, remaining184suffix, other instruction window/global/CalcMain beyond selected prefix or original/decoder/ESIL/model execution. Whole240/hash is identity only for opaque suffix.',
            'Finite recorded preservation/resource/cleanup evidence does not prove absent escapeddescendants or pretry/catastrophicI/O/uncatchable failure retention.'
        ])
    rp.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(report=identity(rp), evidence=identity(ep), own_watch=len(paths)), indent=2))


if __name__ == '__main__':
    main()
