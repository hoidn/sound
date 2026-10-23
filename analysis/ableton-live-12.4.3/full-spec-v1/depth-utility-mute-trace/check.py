"""Finite static-data proof checks; no original or preflight tool execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json
import re
import struct
import sys

D = Path(__file__).resolve().parent
load = lambda p: json.loads(p.read_text())


def pin(p):
    h = sha256()
    n = 0
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
            n += len(b)
    return dict(bytes=n, sha256=h.hexdigest())


def ptr(v, s):
    assert s.startswith('/')
    for k in s[1:].split('/'):
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def sx(v, bits):
    return v - (1 << bits) if v & (1 << (bits-1)) else v


def branch(w, pc):
    assert w & 0x7c000000 == 0x14000000
    return pc + sx(w & 0x3ffffff, 26) * 4


def adrp(w, pc):
    assert w & 0x9f000000 == 0x90000000
    return (pc & ~4095) + (sx(((w >> 29) & 3) | (((w >> 5) & 0x7ffff) << 2), 21) << 12)


def guards(r, t, old):
    assert len(r['new_full_functions']) == 2
    assert [x['id'] for x in r['new_full_functions']] == ['0x101aa4b94', '0x101aa4c18']
    assert len(r['reused_function_refs']) == 9 and len(r['reused_byte_refs']) == 3
    for q in r['reused_function_refs']:
        assert q['provider'] == str(D.parent/'depth-preflight-utility/records.json')
        assert ptr(old, q['pointer'])['id'] == q['id']
        assert ptr(old, q['pointer'])['read_scope'] == q['scope']
    for q in r['reused_byte_refs']:
        assert q['provider'] == str(D.parent/'depth-preflight-utility/records.json')
        assert ptr(old, q['pointer'])['address'] == q['address']
    assert next(q for q in r['reused_function_refs'] if q['id'] == '0x1021653a8')['scope'] == 'metadata-only-body-not-read'
    for q in r['new_full_functions']:
        b = q['record']['code'].encode()
        assert q['id'] == q['record']['entry'] and len(b) == q['record']['code_bytes'] and sha256(b).hexdigest() == q['record']['code_sha256']
    assert len(r['new_index_records']['aliases']) == 2 and len(r['new_index_records']['calls']) == 1
    assert r['new_index_records']['calls'][0]['record']['callee'] == '0x101a41ce8'
    assert len(t['proof_steps']) == 8 and len(t['case_refs']) == 3
    for s in t['proof_steps']:
        assert s['expected'] is s['comparison'] is s['actual_expected'] is s['actual_comparison'] is None
        assert s['target'] == 'U' and s['executed'] is False and s['normative_credit'] == 0
        for q in s['refs']:
            if q['catalog'] == 'preflight/records.json':
                assert q['provider'] == str(D.parent/'depth-preflight-utility/records.json')
            else:
                assert q['catalog'] == 'records.json'
            assert ptr(old if q['catalog'] == 'preflight/records.json' else r, q['pointer'])['id'] == q['id']
    assert [c['id'] for c in t['case_refs']] == ['DUT-020', 'DUT-021', 'DUT-040']
    for c in t['case_refs']:
        assert c['provider'] == str(D.parent/'depth-preflight-utility/records.json')
        assert ptr(old, c['pointer'])['id'] == c['id']
        assert c['actual_expected'] is c['actual_comparison'] is None and c['target'] == 'U' and c['executed'] is False
    assert t['aliases']['kernel_byte'] == 'K+0xcf=P+0x117'
    assert 0x48 + 0xcf == 0x117 and 0x117 != 0x161
    assert t['aliases']['saved_mute_byte'] == 'P+0x161'
    result = t['proposed_static_result']
    assert result['application_mapping_proved'] is result['scheduler_delivery_proved'] is result['reviewed'] is False
    assert len(result['predicate']) == 6
    for n, words in [(1, ['both P+0x30 and P+0x38', 'valid readable sample pointers']), (2, ['P+0x162==0', '+1.0']), (3, ['No concurrent or intervening write']), (4, ['actually invoked', 'SAME P', 'not scheduler invocation']), (5, ['cached entry', 'untraced changed-cache'])]:
        assert all(w in result['predicate'][n] for w in words)
    assert result['output_bits'] == ['0x00000000', '0x00000000']
    assert 'conditional function-local proposal' in result['consequence']
    assert 'changed-cache' in t['proof_steps'][3]['source_claim'].lower()
    assert 'untraced0x101a41ce8' in t['proof_steps'][3]['source_claim']
    assert 'distinct inactive path' in t['proof_steps'][6]['source_claim']
    assert 'does NOT prove nonzero audio' in t['proof_steps'][7]['source_claim']
    assert t['metrics'] == dict(new_application_outcomes_graded=0, new_owner_requirements=0, new_owner_cases=0, no_route_findings=0, complete_profiles=0, proposed_function_local_predicates=1, source_or_original_execution=False)
    reads = {q['address']: q for q in r['new_byte_reads']}
    assert len(reads) == 6 and sum(q['length'] for q in reads.values()) == 592
    segs = old['byte_reads']['segments']
    for q in reads.values():
        b = bytes.fromhex(q['raw_hex'])
        assert len(b) == q['length'] and sha256(b).hexdigest() == q['sha256']
        assert q['words_le'] == [hex(w) for w in struct.unpack('<'+'I'*(len(b)//4), b)]
        addr = int(q['address'], 16)
        s = next(s for s in segs if int(s['vmaddr'], 16) <= addr and addr+len(b) <= int(s['vmaddr'], 16)+s['filesize'])
        assert q['file_offset'] == s['fileoff'] + addr-int(s['vmaddr'], 16) and q['segment'] == s['name']
    ws = {a: [int(w, 16) for w in q['words_le']] for a, q in reads.items()}
    w = ws['0x10216533c']
    assert w == [0x1e202008,0x1a9f07e8,0x39058408,0x39458808,0x7100051f,0x54000041,0x17ffe823,0x1e202008,0x1a9f07e1,0x91012000,0x149960ff]
    assert (w[2] >> 10) & 4095 == 0x161 and (w[3] >> 10) & 4095 == 0x162
    assert 0x102165350 + sx((w[5] >> 5) & 0x7ffff,19)*4 == 0x102165358
    assert branch(w[6], 0x102165354) == 0x10215f3e0
    assert (w[9] >> 10) & 4095 == 0x48 and branch(w[10],0x102165364) == 0x1047bd760
    w = ws['0x1047bd760'][0]
    assert w == 0x39033c01 and (w & 31, (w >> 5)&31, (w >> 10)&4095) == (1,0,0xcf)
    select = ws['0x10215f3e0']
    at = lambda address: select[(address-0x10215f3e0)//4]
    assert (at(0x10215f3f0)>>10)&4095 == 0x149 and (at(0x10215f3fc)>>10)&4095 == 0x148
    assert (at(0x10215f408)>>10)&4095 == 0x162
    assert at(0x10215f410) == 0x54000221 and 0x10215f410+sx((at(0x10215f410)>>5)&0x7ffff,19)*4 == 0x10215f454
    assert branch(at(0x10215f458),0x10215f458) == 0x101aa4c18
    slot = adrp(at(0x10215f464),0x10215f464) + ((at(0x10215f468)>>10)&4095)*8
    assert slot == 0x106541200 and branch(at(0x10215f474),0x10215f474) == 0x101aa4b94
    # Inactive path passes X1=0 and stores XZR as two adjacent zero output words.
    assert at(0x10215f43c) == 0xd2800001 and at(0x10215f444) == 0xf900227f
    assert branch(at(0x10215f440),0x10215f440) == 0x101aa4b94
    helper = ws['0x101aa4b94']
    assert helper[0] == 0xf9000001
    assert helper[8] == 0x54000300 and 0x101aa4bb4+sx((helper[8]>>5)&0x7ffff,19)*4 == 0x101aa4c14 and helper[-1] == 0xd65f03c0
    assert branch(helper[29],0x101aa4c08) == 0x101a41ce8
    assert ws['0x101aa4c18'] == [0xf9400000,0xd65f03c0]
    assert struct.unpack('<Q', bytes.fromhex(reads['0x1065411b0']['raw_hex']))[0] == 0x1021653a8
    oldbytes = {q['address']: q for q in old['byte_reads']['reads']}
    assert oldbytes['0x106541200']['u64_le'] == ['0x1021658b0']
    kw = [int(w,16) for w in oldbytes['0x1047bd790']['instruction_words_le']]
    assert kw[:4] == [0x39433c08,0x2f00e400,0x2f00e401,0x370016c8]
    assert (kw[0]>>10)&4095 == 0xcf
    target = 0x1047bd79c + sx((kw[3]>>5)&16383,14)*4
    assert target == 0x1047bda74 and kw[(target-0x1047bd790)//4] == 0xd65f03c0
    assert oldbytes['0x1021658b0']['instruction_words_le'][13] == '0x2d080660'


def main():
    assert sys.dont_write_bytecode and sys.argv[1:] == ['--check'], 'Read-only --check only; no writer/original/provider execution'
    i = load(D/'inputs.json')
    watched = {Path(p) for p in i['files']} | set(D.iterdir())
    before = {str(p):pin(p) for p in watched}
    assert len(i['files']) == 10
    for p, expected in i['files'].items(): assert pin(Path(p)) == expected
    pre = Path(i['preflight'])
    pm = load(pre/'manifest.json')
    assert pin(pre/'manifest.json') == i['preflight_manifest']
    for p, expected in pm['payloads'].items(): assert pin(pre/p) == expected
    old = load(pre/'records.json')
    r,t = load(D/'records.json'),load(D/'trace.json')
    guards(r,t,old)
    parents = {}
    for q in r['new_full_functions'] + r['new_index_records']['aliases'] + r['new_index_records']['calls']:
        parents.setdefault(q['parent'],{})[q['line']] = q
    for name, selected in parents.items():
        for n, raw in enumerate(Path(name).open('rb'),1):
            if n in selected:
                q = selected[n]
                assert sha256(raw).hexdigest() == q['raw_line_sha256'] and json.loads(raw) == q['record']
    assert pin(Path(i['source_derived']))['sha256'] == i['target_identity'] == '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
    with Path(i['source_derived']).open('rb') as f:
        for q in r['new_byte_reads']:
            f.seek(q['file_offset']); assert f.read(q['length']).hex() == q['raw_hex']
    rejected=[]
    for kind in ['wrong-state-byte','saved-flag-as-kernel','joint-wrong-function-pointer','wrong-case-index','legacy-promoted','lost-input-validity','lost-no-interference','selection-as-invocation','changed-cache-assumed-safe','inactive-as-mute','unmute-implies-signal','application-grade','new-raw-offset']:
        rr,tt=deepcopy(r),deepcopy(t)
        if kind=='wrong-state-byte': tt['aliases']['kernel_byte']='P+0x161'
        elif kind=='saved-flag-as-kernel':tt['aliases']['saved_mute_byte']='P+0x117'
        elif kind=='joint-wrong-function-pointer':
            tt['proof_steps'][0]['refs'][0]['pointer']='/functions/0'
            next(q for q in rr['reused_function_refs'] if q['id']=='0x10216533c')['pointer']='/functions/0'
        elif kind=='wrong-case-index':tt['case_refs'][0]['pointer']='/owner_profile/cases/0'
        elif kind=='legacy-promoted':next(q for q in rr['reused_function_refs'] if q['id']=='0x1021653a8')['scope']='full-body'
        elif kind=='lost-input-validity':tt['proposed_static_result']['predicate'][1]='Any invalid pointer is safe while muted.'
        elif kind=='lost-no-interference':tt['proposed_static_result']['predicate'][3]='Concurrent writers allowed.'
        elif kind=='selection-as-invocation':tt['proposed_static_result']['scheduler_delivery_proved']=True
        elif kind=='changed-cache-assumed-safe':tt['proof_steps'][3]['source_claim']='All helper returns preserve callback; no remaining calls.'
        elif kind=='inactive-as-mute':tt['proof_steps'][6]['source_claim']='Inactive silence proves Mute.'
        elif kind=='unmute-implies-signal':tt['proof_steps'][7]['source_claim']='Clearing Mute guarantees nonzero signal.'
        elif kind=='application-grade':tt['metrics']['new_application_outcomes_graded']=1
        else:rr['new_byte_reads'][0]['file_offset']+=4
        try:guards(rr,tt,old)
        except (AssertionError,KeyError,IndexError,ValueError,TypeError):rejected.append(kind)
        else:raise AssertionError('Unsafe fixture accepted: '+kind)
    manifest=D/'manifest.json'
    if manifest.exists():
        m=load(manifest);assert m['immutable_inputs']==i['files'] and set(m['payloads'])=={p.name for p in D.iterdir() if p!=manifest}
        for p,expected in m['payloads'].items():assert pin(D/p)==expected
    for p in D.iterdir():
        b=p.read_bytes();assert b.endswith(b'\n') and b'\0' not in b and all(v.rstrip(b' \t')==v for v in b.splitlines())
    for dest in re.findall(r'\]\(([^)]+)\)',(D/'README.md').read_text()):assert (D/dest).exists() or dest=='manifest.json' and not manifest.exists()
    assert before=={str(p):pin(p) for p in watched}
    print(json.dumps(dict(status='pass',sealed=manifest.exists(),pins=10,new_bodies=2,reused_functions=9,new_reads=6,new_bytes=592,proof_steps=8,unchanged_case_refs=3,negative_fixtures=rejected,watch_unchanged=len(watched),writes=False,new_application_grades=0),indent=2))


if __name__=='__main__':main()
