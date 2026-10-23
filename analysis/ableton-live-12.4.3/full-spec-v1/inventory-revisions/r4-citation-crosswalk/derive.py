"""Four-packet exact citation crosswalk; --check is read-only, never product coverage."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[4]
assert sys.argv[1:] in ([], ['--check'])
CHECKING = sys.argv[1:] == ['--check']
if not CHECKING:
    assert not (P / 'manifest.json').exists(), 'Frozen crosswalk: use --check; create another revision for changes'
load = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
inputs = load(P / 'inputs.json')
assert [c['packet'] for c in inputs['cohort']] == [
    'video-workflows', 'synchronization', 'settings-learning', 'stem-separation']
pins = {pin['path']: pin for pin in inputs['pins']}
assert len(pins) == len(inputs['pins']) == 72
for pin in pins.values():
    path = ROOT / pin['path']
    assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], pin['path']
toc = load(ROOT / inputs['toc'])
assert len(toc) == len({t['id'] for t in toc}) == len({t['url'] for t in toc}) == 880
assert sum(t['leaf'] for t in toc) == 708
assert pins[inputs['toc']]['sha256'] == '1ca19a34ad1c0e97a9dd6582d2f7ebf06c5a16ae9d2bd64c26baab5c0eb46e98'
assert pins[inputs['original_toc_source']]['sha256'] == '584d4b61d119c96ecdb7941ef34ac9d4e0282a3e40c8bc474b6cf24892640d80'
original_manifest = load(ROOT / inputs['original_inventory_manifest'])
# Confirm the source/TOC pins also agree with the original inventory manifest.
for name in ('manual-toc.json', 'manual-12-toc-2026-10-19.html'):
    info = original_manifest['files'][name]
    path = (ROOT / inputs['toc']).parent / name
    assert path.stat().st_size == info['bytes'] and sha(path) == info['sha256']

topics = [dict(t, citation_status='no-citation-in-this-four-packet-cohort',
               full_topic_semantic_coverage='unknown', completion_status='unknown',
               target_applicability='U', cohort_citations=[]) for t in toc]
by_url = {t['url']: t for t in topics}
unmatched, unbacked = [], []
all_requirements, all_cases, all_blocks = [], [], []
packet_counts = []


def case_ref(case, path, index):
    assert case['expected'] is None and case['comparison'] is None
    assert case['target_grade'] == 'U' and case['executed'] is False
    return {'case_id': case['id'], 'kind': case['kind'], 'catalog': path,
            'json_pointer': '/' + str(index), 'expected': None, 'comparison': None,
            'target_grade': 'U', 'executed': False,
            'documentary_expected_is_null': case['documentary_expected'] is None,
            'documentary_comparator_is_null': case['documentary_comparator'] is None}


for packet in inputs['cohort']:
    manifest_path = ROOT / packet['manifest']
    manifest, review = load(manifest_path), load(ROOT / packet['review'])
    assert review['reviewed_manifest_sha256'] == sha(manifest_path)
    assert review['id'] == packet['review_id'] and review['disposition'] == packet['review_disposition']
    assert review['disposition'] in ('approved-partial-analyst-draft', 'approved-as-partial-analyst-draft')
    assert not review.get('required_findings') and not review.get('findings')
    assert manifest['id'] == packet['manifest_id'] and manifest['revision'] == 1
    for name, pin in manifest['files'].items():
        path = manifest_path.parent / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256']
        assert str(path.relative_to(ROOT)) in pins
    for pin in manifest.get('external_pins', []):
        path = ROOT / pin['path']
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256']
        assert pin['path'] in pins
    assert (manifest_path.parent / 'spec-r1.md').read_bytes() == (ROOT / packet['canonical_spec']).read_bytes()
    assert (manifest_path.parent / 'research-r1.md').read_bytes() == (ROOT / packet['canonical_research']).read_bytes()
    source = load(ROOT / packet['source'])
    assert manifest['source'] == source and '#' not in source['url']
    source_path = ROOT / packet['source_bytes']
    assert source_path.stat().st_size == source['bytes'] and sha(source_path) == source['sha256']
    assert source_path.name == source['file']
    blocks = load(ROOT / packet['blocks'])
    lookup = {b['id']: b for b in blocks}
    assert len(blocks) == len(lookup)
    requirements, cases = load(ROOT / packet['requirements']), load(ROOT / packet['cases'])
    req_index = {r['id']: r for r in requirements}
    assert len(req_index) == len(requirements) and {rid for c in cases for rid in c['requirements']} == set(req_index)
    assert len({c['id'] for c in cases}) == len(cases)
    assert manifest['requirements'] == len(requirements) and manifest['cases'] == len(cases)
    all_requirements.extend(requirements)
    all_cases.extend(cases)
    all_blocks.extend((packet['packet'], b['id']) for b in blocks)
    packet_counts.append({'packet': packet['packet'], 'requirements': len(requirements),
                          'requirement_strength': dict(Counter(r['strength'] for r in requirements)),
                          'cases': len(cases), 'source_blocks': len(blocks),
                          'review_id': review['id'], 'review_manifest_sha256': sha(manifest_path)})
    for req_number, requirement in enumerate(requirements):
        assert requirement['target_applicability'] == 'U'
        linked = [case_ref(c, packet['cases'], n) for n, c in enumerate(cases) if requirement['id'] in c['requirements']]
        assert linked
        identity = {'packet': packet['packet'], 'requirement_id': requirement['id'],
                    'requirement_strength': requirement['strength'],
                    'requirement_catalog': packet['requirements'],
                    'requirement_json_pointer': '/' + str(req_number),
                    'canonical_spec': packet['canonical_spec'],
                    'canonical_research': packet['canonical_research'],
                    'review': {'path': packet['review'], 'id': review['id'],
                               'sha256': pins[packet['review']]['sha256'],
                               'disposition': review['disposition'],
                               'reviewed_manifest_sha256': sha(manifest_path)},
                    'case_references': linked,
                    'target_applicability': 'U', 'semantic_coverage': 'unknown'}
        if not requirement['evidence']:
            assert requirement['strength'] == 'U'
            unbacked.append(dict(identity, source=None, reason='U requirement has no evidence; no source invented'))
            continue
        assert requirement['strength'] == 'D12'
        assert len({e['block'] for e in requirement['evidence']}) == len(requirement['evidence'])
        for evidence in requirement['evidence']:
            block = lookup[evidence['block']]
            assert evidence['anchor'] == block['anchor'] and evidence['html_line'] == block['html_line']
            exact_url = source['url'] + '#' + evidence['anchor']
            citation = dict(identity, evidence={
                'block': evidence['block'], 'anchor': evidence['anchor'],
                'html_line': evidence['html_line'], 'source_id': source['id'],
                'source_file': packet['source_bytes'], 'source_sha256': source['sha256'],
                'source_capture_utc': source['capture_utc'], 'source_url': source['url'],
                'exact_anchor_url': exact_url, 'block_catalog': packet['blocks'],
                'block_json_pointer': '/' + str(next(n for n, b in enumerate(blocks) if b['id'] == evidence['block']))})
            if exact_url in by_url:
                topic = by_url[exact_url]
                topic['cohort_citations'].append(citation)
                topic['citation_status'] = 'cited-by-partial-reviewed-draft'
            else:
                unmatched.append(dict(citation, reason='Exact source URL plus anchor absent from retained TOC; no title, ancestor or parent inference'))

matched = [c for t in topics for c in t['cohort_citations']]
matched_req_ids = {c['requirement_id'] for c in matched}
unmatched_req_ids = {c['requirement_id'] for c in unmatched}
represented_req_ids = matched_req_ids | unmatched_req_ids | {r['requirement_id'] for r in unbacked}
represented_case_ids = {c['case_id'] for r in [*matched, *unmatched, *unbacked] for c in r['case_references']}
assert len(all_requirements) == len({r['id'] for r in all_requirements}) == 83
assert Counter(r['strength'] for r in all_requirements) == {'D12': 74, 'U': 9}
assert len(all_cases) == len({c['id'] for c in all_cases}) == 123
assert len(all_blocks) == len(set(all_blocks)) == 195
assert represented_req_ids == {r['id'] for r in all_requirements}
assert represented_case_ids == {c['id'] for c in all_cases}
assert len(matched) == 111 and len(unmatched) == 8 and len(unbacked) == 9
assert len(matched_req_ids) == 69 and len(unmatched_req_ids - matched_req_ids) == 5
assert matched_req_ids & unmatched_req_ids == {'REQ-VIDEO-WORKFLOW-013'}
assert [dict((k, t[k]) for k in original) for t, original in zip(topics, toc)] == toc
assert all(not t['complete'] and t['completion_status'] == 'unknown' and t['target_applicability'] == 'U' for t in topics)
summary = {'id': 'FULL-LIVE-MANUAL-CITATION-CROSSWALK-R4-SUMMARY',
           'scope': 'Exactly four reviewed R1 documentary packets, navigation/audit only; not behavioral coverage or applicability proof',
           'cohort': packet_counts, 'input_requirements': 83,
           'input_requirement_strength': {'D12': 74, 'U': 9}, 'input_cases': 123,
           'input_source_blocks': 195, 'source_block_count_scope': 'Only video/synchronization/settings/stem cohort; not the separate engine cohort',
           'manual_topics_preserved': 880, 'manual_leaves_preserved': 708,
           'manual_chapters_preserved': len({t['number'].split('.')[0] for t in toc}),
           'matched_evidence_citations': len(matched), 'unmatched_evidence_citations': len(unmatched),
           'distinct_unmatched_anchor_URLs': len({c['evidence']['exact_anchor_url'] for c in unmatched}),
           'topics_with_cohort_citations': sum(bool(t['cohort_citations']) for t in topics),
           'leaves_with_cohort_citations': sum(t['leaf'] and bool(t['cohort_citations']) for t in topics),
           'nonleaves_with_cohort_citations': sum(not t['leaf'] and bool(t['cohort_citations']) for t in topics),
           'topics_without_cohort_citations': sum(not t['cohort_citations'] for t in topics),
           'requirements_with_exact_TOC_citations': len(matched_req_ids),
           'requirements_with_both_matched_and_unmatched_citations': len(matched_req_ids & unmatched_req_ids),
           'requirements_with_only_unmatched_citations': len(unmatched_req_ids - matched_req_ids),
           'U_requirements_without_evidence': len(unbacked),
           'unique_requirement_references_reconciled': len(represented_req_ids),
           'unique_case_references_reconciled': len(represented_case_ids),
           'external_input_pins': len(pins), 'complete_topics_claimed': 0,
           'full_topic_semantic_coverage': 'unknown', 'target_applicability': 'U',
           'all_case_target_oracles_null_U_unexecuted': True,
           'work_selector': 'wiki/research/full-live-specification-plan.md; existing F01-F10 only',
           'original_runtime_or_candidate_execution': False}
outputs = {'topic-citations.json': topics, 'unmatched-citations.json': unmatched,
           'unbacked-requirements.json': unbacked, 'summary.json': summary}
for name, value in outputs.items():
    raw = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    path = P / name
    if CHECKING:
        assert path.is_file() and path.read_bytes() == raw, name
    else:
        assert not path.exists(), 'Refuse rewriting generated output: ' + name
        path.write_bytes(raw)
if CHECKING:
    for name, pin in load(P / 'manifest.json')['files'].items():
        path = P / name
        assert path.stat().st_size == pin['bytes'] and sha(path) == pin['sha256'], name
    for path in P.iterdir():
        if path.suffix in {'.json', '.py', '.md'}:
            result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True)
            assert result.returncode in (0, 1) and not result.stdout and not result.stderr, path
print(json.dumps(summary, indent=2))
