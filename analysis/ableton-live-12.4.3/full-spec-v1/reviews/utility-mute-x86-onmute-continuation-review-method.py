"""Independent six-retained-byte arithmetic/hash review; no supplied code executed."""
from pathlib import Path
import datetime
import hashlib
import json

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
PACKET = BASE / 'depth-utility-mute-x86-onmute-continuation-data'
REVIEWS = BASE / 'reviews'


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def read_json(path):
    return json.loads(path.read_text())


def local_decode(data, va):
    if len(data) != 6 or data[0] != 0x5d or data[1] != 0xe9:
        return None
    unsigned = sum(data[2 + i] << (8 * i) for i in range(4))
    signed = unsigned - (1 << 32) if unsigned & (1 << 31) else unsigned
    return signed, va + 6 + signed


def main():
    evidence_path = REVIEWS / 'utility-mute-x86-onmute-continuation-review-evidence.json'
    report_path = REVIEWS / 'utility-mute-x86-onmute-continuation-review.json'
    assert not evidence_path.exists() and not report_path.exists()
    selection = read_json(PACKET / 'selection.json')
    manifest = read_json(PACKET / 'manifest.json')
    inputs = read_json(PACKET / 'before-map.json')
    assert inputs == read_json(PACKET / 'after-map.json') and len(inputs) == 4
    prep = BASE / 'depth-utility-mute-x86-onmute-entry-preparation'
    paths = {Path(row['path']) for row in inputs} | set(PACKET.iterdir()) | set(prep.iterdir()) | {Path(__file__).resolve()}
    before = [identity(path) for path in sorted(paths)]
    assert {row['path'] for row in manifest['files']} == {p.name for p in PACKET.iterdir() if p.name != 'manifest.json'}
    for row in manifest['files']:
        got = identity(PACKET / row['path'])
        assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    for row in inputs:
        assert identity(Path(row['path'])) == row
    for role in ('source', 'peer', 'method'):
        assert identity(Path(selection[role]['path'])) == selection[role]
    assert selection['source_offset'] == 55 and selection['length'] == 6 and selection['va'] == '0x10224e797'
    assert selection['peer']['sha256'] == 'cadb996edbd08d7aa3a7744d997a509e3f1ba6c5d0d0a94ce5d67c6cf888eee7'
    assert selection['source']['bytes'] == 240 and selection['source']['sha256'] == '95a6a34d9e5d369b2e0e8b5e9a7b67a4c4e0c57b60e9969560ad9924bd5b4a59'
    # Fresh semantic read is limited to these six bytes of the existing capture.
    with Path(selection['source']['path']).open('rb') as stream:
        stream.seek(55)
        raw = stream.read(6)
    assert raw.hex() == '5de9c3df9302'
    va = int(selection['va'], 16)
    displacement, target = local_decode(raw, va)
    assert displacement == 43245507 and target == 0x104b8c760
    result = read_json(PACKET / 'result.json')
    assert result['bytes'] == raw.hex() and result['va'] == selection['va']
    assert result['analysis'] == dict(pattern='POP RBP; JMP rel32', signed_displacement=displacement, target=hex(target))
    assert result['remaining_opaque_selected_suffix_bytes'] == 240 - 55 - 6 == 179
    assert result['original_calls'] == 0 and result['decoder_children'] == 0
    assert local_decode(bytes.fromhex('5de9faffffff'), va) == (-6, va)
    assert local_decode(bytes.fromhex('5be900000000'), va) is None
    assert local_decode(bytes.fromhex('5de800000000'), va) is None
    assert local_decode(raw[:-1], va) is None
    after = [identity(path) for path in sorted(paths)]
    assert before == after
    evidence = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='PASS',
        input_pairs=4, payloads=4, tree=5, own_watch=len(paths), before=before, after=after,
        unchanged=True, selected_raw_hex=raw.hex(), selected_raw_sha256=hashlib.sha256(raw).hexdigest(),
        signed_displacement=displacement, next_instruction=hex(va + 6), target=hex(target),
        synthetic_controls=dict(negative_displacement_pass=True, wrong_pop_rejected=True,
            wrong_branch_rejected=True, wrong_length_rejected=True), supplied_method_executed=False,
        decoder_children=0, original_calls=0, uninspected_suffix_bytes=179)
    evidence_path.write_text(json.dumps(evidence, indent=2) + '\n')
    report = dict(schema=1, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        disposition='APPROVED PARTIAL SIX-BYTE RETAINED DATA OBSERVATION ONLY', required_findings=[],
        reviewer='delay_reverb_correction', author='Root',
        roles='Reviewer authored preceding metadata/preparation, not current actual continuation selection or method. Earlier 55-byte/image/header observations are carried from the independently read Synthesis peer, not independently reapproved here.',
        inputs=dict(packet_manifest=identity(PACKET / 'manifest.json'), method=selection['method'],
            prefix_peer=selection['peer'], retained_raw=selection['source'],
            reviewer_method=identity(Path(__file__).resolve()), evidence=identity(evidence_path)),
        fresh_scope='Full3020B method and all four payloads/manifest/maps; fresh same six bytes only, manually checked POP RBP opcode and E9 rel32 signed little-endian displacement/next-address arithmetic. Entire6909B preceding peer read; parent preparation hashes retained unchanged.',
        verification=dict(payloads=4, tree=5, recorded_input_pairs=4, own_watch=len(paths), unchanged=True,
            controls=4, supplied_method_run=False, decoder_or_original_calls=0),
        observations=[
            'At VA10224e797, retained5d is POP RBP; E9 at10224e798 consumes signed rel32 c3df9302=43245507. Next address10224e79d plus displacement nominates104b8c760.',
            'Carried prior unequal-comparison path reaches the earlier ADD RDI,0x48 and normalized ESI carrier before this POP/tail jump, conditional on reached path, valid stack/ordinary execution and no intervening fault. This is not a setter-body or actual float-value result.'
        ],
        limits=[
            'No target/callee/global/CalcMain or remaining179 suffix bytes inspected; no new image read/window, decoder, supplied method, original or runtime execution.',
            'No source/class/current receiver, ABI, stack validity, public Utility binding, setter operation, native extent, arm64 equivalence or output grade is established.',
            'Recorded preservation is four fixed input pairs plus the stated current own watch; no global, catastrophic-I/O or pretry guarantee.',
            'All38 Utility application outcomes remain U/null/unexecuted; no normative IDs, cases, compatibility grade or completion.'
        ])
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(report=identity(report_path), evidence=identity(evidence_path), own_watch=len(paths)), indent=2))


if __name__ == '__main__':
    main()
