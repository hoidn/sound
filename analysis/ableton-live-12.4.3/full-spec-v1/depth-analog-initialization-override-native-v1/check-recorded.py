#!/usr/bin/env python3
"""Owned packet-only assertions. No execution/import of collector, external reads or ESIL."""
import argparse
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
PRE = '6c80c3fee5541ac6cbb571ea05b17fbd27e7d05cfb2d54df454338068921d8c8'
RANGES = [('2c34', 0x2c34, 996), ('17e6c', 0x17e6c, 800)]
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TZ': 'UTC'}

def load(name):
    return json.loads((P / name).read_text())

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def require(ok, label):
    if not ok:
        raise ValueError(label)

def signed(v, width):
    return v - (1 << width) if v & (1 << (width - 1)) else v

def flow(w, pc):
    if w & 0x7c000000 == 0x14000000:
        return {'form': 'BL' if w >> 31 else 'B', 'target': pc + (signed(w & 0x3ffffff, 26) << 2)}
    if w & 0xff000010 == 0x54000000:
        return {'form': 'B.cond', 'target': pc + (signed((w >> 5) & 0x7ffff, 19) << 2)}
    if w & 0x7e000000 == 0x34000000:
        return {'form': 'CB', 'target': pc + (signed((w >> 5) & 0x7ffff, 19) << 2)}
    if w & 0x7e000000 == 0x36000000:
        return {'form': 'TB', 'target': pc + (signed((w >> 5) & 0x3fff, 14) << 2)}
    f = {0xd61f0000: 'BR', 0xd63f0000: 'BLR', 0xd65f0000: 'RET'}.get(w & 0xfffffc1f)
    return {'form': f, 'rn': (w >> 5) & 31} if f else None

def fields(w, pc):
    if w & 0x9f000000 == 0x10000000:
        imm = signed(((w >> 5) & 0x7ffff) << 2 | ((w >> 29) & 3), 21)
        return {'family': 'ADR', 'rd': w & 31, 'address': pc + imm}
    if w & 0x3b000000 == 0x18000000:
        return {'family': 'literal', 'rt': w & 31, 'address': pc + (signed((w >> 5) & 0x7ffff, 19) << 2)}
    if w & 0x3a000000 == 0x28000000:
        return {'family': 'pair', 'rt': w & 31, 'rt2': (w >> 10) & 31,
                'rn': (w >> 5) & 31, 'imm7': signed((w >> 15) & 127, 7),
                'vector': bool(w & (1 << 26)), 'opc': w >> 30,
                'load': bool(w & (1 << 22)), 'mode': (w >> 23) & 3}
    if w & 0x3b000000 == 0x39000000:
        return {'family': 'unsigned-load-store', 'rt': w & 31, 'rn': (w >> 5) & 31,
                'imm12': (w >> 10) & 4095, 'size': w >> 30,
                'vector': bool(w & (1 << 26)), 'opc': (w >> 22) & 3}
    return None

def association(row, raw, pc):
    require(row['offset'] == pc and row['size'] == 4, 'row-position-width')
    require(row['bytes'] == raw.hex(), 'row-byte-association')
    return int.from_bytes(raw, 'little')

def u64_memory(w, load, rt, rn, offset):
    require(w & 0xffc00000 == (0xf9400000 if load else 0xf9000000), 'u64-memory-family')
    require((w & 31, (w >> 5) & 31, ((w >> 10) & 4095) * 8) == (rt, rn, offset), 'u64-memory-operands')

def contract(c):
    require(c == {'actual_runtime_binding': False, 'main_site_credit': 0, 'new_table_bytes': 0,
                  'computed_case_table_read': False, 'E_equals_D': False, 'E_equals_C0': False,
                  'C0_equals_C1': False, 'R_equals_F': False, 'public_behavior_proved': False,
                  'opaque_callee_effects_known': False}, 'unsupported-promotion')

def check():
    pre_raw = (P / 'pre-call-manifest.json').read_bytes()
    require(sha(pre_raw) == PRE, 'exact-precall')
    pre = json.loads(pre_raw)
    for pin in pre['pins']:
        q = Path(pin['path'])
        if q.parent == P:
            b = q.read_bytes()
            require(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'local-precall-pin')
    before, after = load('capture/before-identities.json'), load('capture/after-identities.json')
    require(after['unchanged'] and before == after['files'] and len(before) == 18, 'recorded-custody')
    # Compare recorded custody only. No current external image/tool/source/provider reads.
    require(before[:2] == [pre['image'], pre['tool']], 'recorded-image-tool')
    require(before[2:-1] == pre['pins'] and before[-1]['sha256'] == PRE, 'recorded-watch-membership')
    status = load('capture/status.json')
    require(status['error'] is None and status['watch_unchanged'] and status['children_started'] == 2,
            'capture-success')
    require((status['selected_bytes_read'], status['validated_words'], status['validated_bytes']) == (1796, 449, 1796), 'capture-counts')
    require(not status['automatic_retry'] and status['native_original_instruction_execution'] == 0, 'no-retry-native-execution')
    require(load('capture/data-words.json') == [], 'no-data')
    extraction = load('capture/extraction.json')
    require((extraction['total_code_bytes'], extraction['total_table_bytes']) == (1796, 0), 'extraction-count')
    sources = (P / 'source-context.jsonl').read_bytes().splitlines(keepends=True)
    meta = load('selected-metadata.json')
    require(len(sources) == 2 and (meta['C_bytes'], meta['C_lines'], meta['warnings']) == (9258, 396, 1), 'source-total')
    all_rows, words, associations, branches, bit_fields, children = {}, {}, [], [], [], []
    for i, (name, start, size) in enumerate(RANGES):
        raw = (P / ('capture/' + name + '.bin')).read_bytes()
        rows = load('capture/' + name + '.stdout.json')
        require(len(raw) == size and len(rows) * 4 == size, 'range-size')
        require(sha(raw) == extraction['ranges'][i]['sha256'], 'extraction-hash')
        require(extraction['ranges'][i]['file_offset'] == start, 'retained-H4-identity-map')
        s = json.loads(sources[i]); m = meta['records'][i]
        require(len(sources[i]) == m['raw_bytes'] and sha(sources[i]) == m['raw_sha256'], 'exact-source-record')
        require(s['entry'] == hex(start) and s['body_bytes'] == size and not s['thunk'], 'source-native-extent')
        require(s['error'] is None and not s['timed_out'] and not s['partial_code'], 'source-status')
        cb = s['code'].encode()
        require(len(cb) == m['metadata']['code_bytes'] and sha(cb) == m['metadata']['code_sha256'], 'source-C-pin')
        require(len(s['code'].splitlines()) == m['C_lines'], 'source-lines')
        for j, row in enumerate(rows):
            pc = start + j * 4
            w = association(row, raw[j * 4:j * 4 + 4], pc)
            words[pc], all_rows[pc] = w, row
            associations.append({'pc': hex(pc), 'bytes': row['bytes'], 'bin_offset': j * 4})
            f = flow(w, pc)
            if f:
                if 'target' in f:
                    require(row.get('jump') == f['target'], 'raw-direct-flow-target')
                branches.append({'pc': hex(pc), **f})
            f = fields(w, pc)
            if f:
                bit_fields.append({'pc': hex(pc), **f})
        bef = load('capture/' + name + '.invocation-before.json')
        aft = load('capture/' + name + '.invocation-after.json')
        pid = load('capture/' + name + '.pid.json')
        require(bef['argv'] == aft['argv'] == pid['argv'], 'recorded-child-argv')
        require(aft['exit_code'] == 0 and not aft['timed_out'] and aft['error'] is None, 'child-status')
        require(aft['timeout_seconds'] == 30 and aft['stdin'] == 'DEVNULL' and aft['environment'] == ENV,
                'child-limits-env')
        require(aft['core_limit_bytes'] == 0 and aft['new_process_session'], 'child-core-session')
        require(pid['pid'] == pid['pgid'] == aft['pid'] and pid['pid'] > 0, 'child-PID')
        require((P / ('capture/' + name + '.stderr')).stat().st_size == 0, 'child-stderr')
        require(aft['argv'][-2] == 'pdj ' + str(size // 4), 'exact-pdj-bound')
        require(bef['started_utc'] <= pid['spawned_utc'] <= aft['finished_utc'], 'child-time-order')
        children.append(aft)
    require(len(words) == 449 and set(words) == set(all_rows), 'whole-row-set')
    # Raw register/unsigned-offset checks; no ESIL, tables, runtime reads or decoder.
    critical = [(0x17eac, True, 8, 0, 0), (0x17eb0, True, 8, 8, 0x70),
                (0x17eb8, False, 0, 20, 8), (0x17ffc, True, 23, 20, 8),
                (0x18010, True, 23, 20, 8), (0x1806c, True, 0, 20, 8),
                (0x18088, True, 8, 20, 8), (0x2c9c, True, 0, 19, 8),
                (0x2cbc, True, 0, 19, 8), (0x2cd8, True, 0, 19, 8),
                (0x2cf4, True, 0, 19, 8), (0x2fcc, True, 8, 19, 8)]
    for pc, ld, rt, rn, off in critical:
        u64_memory(words[pc], ld, rt, rn, off)
    require(words[0x17e90] == 0xaa0003f4 and words[0x2c5c] == 0xaa0003f3, 'receiver-carriers')
    expected_indirect = {0x2c98,0x2cb8,0x2cd4,0x2cf0,0x2d0c,0x2d30,0x2dbc,0x2e54,0x2fe8,
                         0x17eb4,0x17ef8,0x1802c,0x18068,0x18084,0x1809c,0x18100}
    require({int(x['pc'],16) for x in branches if x['form'] in ('BR','BLR')} == expected_indirect, 'whole-local-indirect-set')
    require(flow(words[0x17eb4],0x17eb4) == {'form':'BLR','rn':8}, 'producer-slot-call')
    require(words[0x17eb8] == 0xf9000680, 'immediate-call-return-store')
    require(words[0x17ee8] == 0x39014308, 'cast-flag-not-member-store')
    require(flow(words[0x2c98],0x2c98) == {'form':'BR','rn':10} and flow(words[0x2d30],0x2d30) == {'form':'BR','rn':9}, 'unread-computed-tables')
    require(words[0x2d5c] == 0xd2800013 and words[0x2df0] == 0xd2800014 and words[0x2fdc] == 0x52800033, 'register-repurposing')
    c = {'actual_runtime_binding': False, 'main_site_credit': 0, 'new_table_bytes': 0,
         'computed_case_table_read': False, 'E_equals_D': False, 'E_equals_C0': False,
         'C0_equals_C1': False, 'R_equals_F': False, 'public_behavior_proved': False,
         'opaque_callee_effects_known': False}
    contract(c)
    controls = []
    def reject(label, fn):
        try:
            fn()
        except (ValueError, KeyError):
            controls.append(label)
        else:
            raise AssertionError('negative-control-accepted:' + label)
    reject('raw-byte-corruption', lambda: association(all_rows[0x17eb8], bytes(4), 0x17eb8))
    reject('wrong-PC', lambda: association(all_rows[0x17eb8], bytes.fromhex('800600f9'), 0x17ebc))
    reject('producer-base-not-J', lambda: u64_memory(words[0x17eb8],False,0,19,8))
    reject('producer-offset-not-eight', lambda: u64_memory(words[0x17eb8],False,0,20,16))
    reject('producer-register-not-return-X0', lambda: u64_memory(words[0x17eb8],False,1,20,8))
    reject('cast-flag-is-not-u64-member-store', lambda: u64_memory(words[0x17ee8],False,0,20,8))
    for key in c:
        bad = dict(c); bad[key] = 1 if type(c[key]) is int else True
        reject('forbid-' + key, lambda bad=bad: contract(bad))
    require(len(controls) == 16, 'negative-control-count')
    return {'status':'PASS', 'scope':'CURRENT_PACKET_ONLY; recorded external custody, no current external rehash',
            'pre_call_sha256': PRE, 'rows':449, 'code_bytes':1796, 'C_bytes':9258, 'C_lines':396,
            'warnings':1, 'data_bytes':0, 'recorded_custody_pairs':18, 'children':children,
            'all_raw_associations':associations, 'raw_flow_fields':branches, 'raw_selected_field_families':bit_fields,
            'critical_u64_memory_fields':[{'pc':hex(pc),'load':ld,'rt':rt,'rn':rn,'offset':off} for pc,ld,rt,rn,off in critical],
            'local_indirect_operands':16, 'native_site_resolution_credit':0,
            'negative_controls':controls, 'negative_control_count':len(controls),
            'field_decoder_limit':'Checks selected ARM64 field families, not a total ISA/CFG/ABI decoder; all rows separately author-read; ESIL excluded.',
            'runtime_contract':c}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true', required=True); ap.parse_args()
    print(json.dumps(check(), indent=2) + '\n', end='')
