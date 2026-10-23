"""Independent frozen R5 metadata/source/owned-data preflight only; no export tools."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import struct
import subprocess
import sys

BASE = Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P = BASE / 'depth-corpus-x86-selected-entry-preparation-r5'
OLD = BASE / 'depth-corpus-x86-selected-entry-preparation-r4'
R = BASE / 'reviews'


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def load(path):
    return json.loads(path.read_text())


def replace_exact(text, changes):
    for before, after, count in changes:
        assert text.count(before) == count
        text = text.replace(before, after)
    return text


def main():
    ep = R / 'corpus-x86-selected-entry-r5-code-preflight-review-evidence.json'
    rp = R / 'corpus-x86-selected-entry-r5-code-preflight-review.json'
    assert not ep.exists() and not rp.exists()
    seal = identity(P / 'manifest-preparation.json')
    assert seal['sha256'] == '7a1f153c866e4dbba656594b803d6261dc35d08bb4ec9f0a15ca86f0a0a423f4'
    inputs, manifest, delta = load(P / 'inputs.json'), load(P / 'manifest-preparation.json'), load(P / 'source-delta.json')
    paths = {Path(r['path']) for r in inputs['pins']} | set(P.iterdir()) | {Path(__file__).resolve()}
    before = [identity(p) for p in sorted(paths)]
    for row in inputs['pins']:
        assert identity(Path(row['path'])) == row
    assert len(inputs['pins']) == 95 and len(manifest['files']) == 13
    assert {r['path'] for r in manifest['files']} == {p.name for p in P.iterdir() if p.name != 'manifest-preparation.json'}
    for row in manifest['files']:
        got = identity(P / row['path'])
        assert (got['bytes'], got['sha256']) == (row['bytes'], row['sha256'])
    reconstructed = []
    for row in delta['files']:
        source, target = Path(row['before']['path']), Path(row['after']['path'])
        assert identity(source) == row['before'] and identity(target) == row['after']
        lines = source.read_text().splitlines(keepends=True)
        for edit in reversed(row['edits']):
            lo, hi = edit['old_line_start_zero'], edit['old_line_end_exclusive']
            assert hashlib.sha256(''.join(lines[lo:hi]).encode()).hexdigest() == edit['old_text_sha256']
            lines[lo:hi] = edit['replacement'].splitlines(keepends=True)
        assert ''.join(lines).encode() == target.read_bytes()
        reconstructed.append(target.name)
    assert len(reconstructed) == 9
    java = (P / 'CorpusX86SelectedExport.java').read_text()
    expected_java = replace_exact((OLD / 'CorpusX86SelectedExport.java').read_text(), [
        ('"0x3820"', '"0xd090"', 1), ('0x3820L', '0xd090L', 1),
        ('getAsInt()!=1024', 'getAsInt()!=4096', 1), ('bytes!=1024', 'bytes!=4096', 1),
        ('Only fixed 1024-byte windows', 'Only fixed 4096-byte windows', 1)])
    assert java == expected_java
    driver = (P / 'run-selected.py').read_text()
    expected_driver = replace_exact((OLD / 'run-selected.py').read_text(), [
        ("PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r4'", "PRE=BASE/'depth-corpus-x86-selected-entry-preparation-r5'", 1),
        ("return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r4')", "return BASE/('depth-corpus-x86-selected-entry-'+mode+'-r5')", 1),
        ("('corpus-x86-selected-entry-'+mode+'-r4-selected-execution')", "('corpus-x86-selected-entry-'+mode+'-r5-selected-execution')", 1),
        ("'window_bytes':1024", "'window_bytes':4096", 2), ("'address':'0x3820'", "'address':'0xd090'", 1),
        ("'label':'processing-candidate-0x3820'", "'label':'construction-candidate-0xd090'", 1),
        ('b6d176792b5ce2e12bfeb0546e469e7922e902a9f4d9dff9819a5199e22dad03', '1c514938c8b4b28ee47c0f419acb247e63a65ee988d57b5f195957b3aae4c9de', 1),
        ('bytes=16384', 'bytes=65536', 1)])
    assert driver == expected_driver
    old_tree, tree = ast.parse((OLD / 'run-selected.py').read_text()), ast.parse(driver)
    old_fns = {n.name: n for n in old_tree.body if isinstance(n, ast.FunctionDef)}
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in functions.keys() - {'destination', 'selection_path', 'expected_config'}:
        assert ast.dump(functions[name], include_attributes=False) == ast.dump(old_fns[name], include_attributes=False)
    raw = (P / 'synthetic-corpus-x86.macho').read_bytes()
    expected = bytearray(65536)
    expected[:32] = struct.pack('<8I', 0xfeedfacf, 0x1000007, 3, 8, 1, 152, 0, 0)
    expected[32:104] = struct.pack('<II16sQQQQiiII', 0x19, 152, b'__TEXT', 0, 65536, 0, 65536, 5, 5, 1, 0)
    expected[104:184] = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT', 0x2000, 0xe000, 0x2000, 4, 0, 0, 0x80000400, 0, 0, 0)
    expected[8192:] = b'\xcc' * 57344
    expected[0x23b0:0x23b6] = bytes.fromhex('b82a000000c3')
    expected[0xd090:0xd093] = bytes.fromhex('31c0c3')
    assert raw == expected
    configs = {mode: load(P / (mode + '-config.json')) for mode in ('fixture', 'actual')}
    assert {k for k in configs['fixture'] if configs['fixture'][k] != configs['actual'][k]} == {'target_sha256', 'source'}
    for mode in configs:
        assert [s['address'] for s in configs[mode]['seeds']] == ['0x23b0', '0xd090']
        assert [s['window_bytes'] for s in configs[mode]['seeds']] == [4096, 4096]
        assert not (BASE / ('depth-corpus-x86-selected-entry-' + mode + '-r5')).exists()
    # Fully inspected current preparation check: only pure config AST and stdlib checks.
    checked = subprocess.run([sys.executable, '-B', str(P / 'check.py'), '--check'], capture_output=True, text=True)
    assert checked.returncode == 0 and not checked.stderr
    check_result = json.loads(checked.stdout)
    assert check_result['valid_configs'] == 2 and check_result['valid_commands'] == 1 and len(check_result['unsafe_rejections']) == 17
    assert check_result['pins'] == 95 and check_result['watched'] == 109 and check_result['unchanged'] is True
    refused = subprocess.run([sys.executable, '-B', str(P / 'check.py'), '--write'], capture_output=True, text=True)
    assert refused.returncode == 1 and 'REFUSED' in refused.stderr
    after = [identity(p) for p in sorted(paths)]
    assert before == after
    evidence = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), preparation=seal,
        pins=95, current_tree=14, own_watch=len(paths), before=before, after=after, unchanged=True,
        delta_files_reconstructed=reconstructed, exact_Java_literal_sites=5, exact_driver_literal_sites=9,
        owned_65536_bytes_reconstructed=True, old_nonconfig_function_ASTs_exact=True,
        current_check=dict(exit=checked.returncode, stdout=checked.stdout, stderr=checked.stderr),
        refusal=dict(exit=refused.returncode, stdout=refused.stdout, stderr=refused.stderr),
        supplied_driver_builder_Java_Ghidra_original_executions=0)
    ep.write_text(json.dumps(evidence, indent=2) + '\n')
    report = dict(schema=1, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), reviewer='delay_reverb_correction',
        author='modulation_finish', disposition='APPROVED BOUNDED CODE/PREPARATION READINESS ONLY', required_findings=[],
        preparation=seal, evidence=identity(ep), reviewer_method=identity(Path(__file__).resolve()),
        independence='Current preparation authored Modulation. Reviewer earlier authored Corpus capture preparations and Utility preparation/source metadata and reviewed R1-R3 selected-entry prep/actual history; those are dependencies, not current self-approval. R4 code peer authored Modulation is read as prior context only.',
        fresh_read_scope='Complete13354B Java/17478B driver/10636B checker/1525B builder; full current README/plan/configs/receipt/author-check/manifest/input annotations and all95 pin rows. Full functional source diffs and all9 reconstruction records/hash/ranges verified. Initial serialized inputs/delta display truncated; exact reconstructions and compact complete pin/edit projections were used rather than claiming uninterrupted60563B delta prose reading.',
        checks=[
            'Seal and all13payloads exact;95inputpins/current14tree and110ownwatchedpaths unchanged. Nine source-delta records reconstruct current bytes, all oldR4 prep files/pins retained.',
            'Exactly5Java literal sites change secondentry3820->d090, two1024->4096 windows and diagnostic. Exactly9driver sites change threeR5paths, twoSEEDwindows, secondaddress/label, ownedfixtureSHA/length. Resource1024multipliers, machineidentity/lateoverride2/4Gheap6GRSS3GfloorCPU2/180tool60entry and all nonconfig function ASTs stay exact.',
            'Wholeowned65536B fixture reconstructed independently: TEXT[0,10000),section[2000,10000), CCpadding except known6B/3B twoinstruction pairs23b0/d090; both4096windows fit. Receipt records one ownedbuilder PID404710/exit0/emptyerror, not independent historical execution proof.',
            'Fully read currentreadonly checker ran once:2config positives/1command/17scope rejections, strictguard/env source inequality and9delta reconstructions. --write refused1. No driver/builder/Java/compiler/Ghidra/decoder/original/import run.',
            'CurrentR5 fixture success+independent ACTUAL review and separate Rootactualselection pin gate precede source_bytes; priorR4success cannot satisfy currentprepseal. Two orderedentries/noanalysis/bodycontainment/overlap/controlflow/partialC/noautogrowth preserved.'
        ],
        limits=[
            'Ready only for separately selected current ownfixture, not actualimport. Runtime/tool API behavior and current successful exports untested.',
            'Both4096windows are explicit selected body/output limits, not nativeextents or every-internal-read sandbox; wholethinProgramdata/signatures available. d090 is nomination, not object/receiver/model/coefficient/ABI proof.',
            'Identity-bound group cleanup/sampledRSS/disk/time and pretry/catastrophicI/O/escaped-descendant failures need Rootouterreceipts. Not continuous hardcap or hermetic dependency proof.',
            'All174historicalmodal omissions/twonote72omissions/requirements/cases/application outcomes unchangedU; no originalexecution/newcriterion/candidategrade/completion.'
        ], remaining_gates=['Rootfullpreflight and separate currentfixture selection','Two successful currentfixture exports plus independent actualreview','Separate Rootoriginalimport selection and later independent actualsource review'])
    rp.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(report=identity(rp), evidence=identity(ep), own_watch=len(paths)), indent=2))


if __name__ == '__main__':
    main()
