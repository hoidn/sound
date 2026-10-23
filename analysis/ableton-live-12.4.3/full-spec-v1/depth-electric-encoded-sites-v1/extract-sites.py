#!/usr/bin/env python3
"""Data-only classic-pointer site extraction. Never loads or patches an image."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
U64 = (1 << 64) - 1
IMAGE_SIZE = 265920
TARGETS = [0x300c0, 0x300e8, 0x30100, 0x30108, 0x30110, 0x30118]
MODES = ['rebase', 'bind', 'weak_bind', 'lazy_bind']

class Unknown(ValueError):
    pass

def need(ok, reason):
    if not ok:
        raise Unknown(reason)

def add(a, b):
    need(0 <= a <= U64 and 0 <= b <= U64 and a <= U64-b, 'uint64 arithmetic overflow')
    return a+b

def leb(data, pos, signed=False):
    start, value = pos, 0
    for k in range(10):
        need(pos < len(data), 'truncated LEB operand')
        b = data[pos]
        pos += 1
        value |= (b & 127) << (7*k)
        if b < 128:
            if signed and b & 64:
                value -= 1 << (7*(k+1))
            need((-(1 << 63) <= value < (1 << 63)) if signed else (0 <= value <= U64), '64-bit LEB overflow')
            return value, pos, data[start:pos].hex()
    raise Unknown('LEB exceeds ten bytes')

def load_segments(table):
    need(len(table) == 1704, 'fixed approved LC length')
    cursor, segments, commands = 0, [], []
    for i in range(15):
        need(cursor+8 <= len(table), 'LC header crossing')
        cmd, size = struct.unpack_from('<II', table, cursor)
        need(size >= 8 and size % 8 == 0 and cursor+size <= len(table), 'LC size/alignment')
        commands.append(cmd)
        if cmd == 0x19:
            need(size >= 72, 'segment command length')
            name, va, vs, fo, fs, maxp, initp, ns, flags = struct.unpack_from('<16s4Q4I', table, cursor+8)
            need(size == 72+80*ns and fo <= IMAGE_SIZE and fs <= IMAGE_SIZE-fo, 'segment geometry')
            add(va, vs)
            segments.append({'index': len(segments), 'name': name.rstrip(b'\0').decode('ascii'), 'vmaddr': va, 'vmsize': vs, 'fileoff': fo, 'filesize': fs})
        cursor += size
    need(cursor == len(table), 'LC complete coverage')
    need(commands == [25]*4+[0x80000022,2,11,27,50,42,12,12,38,41,29], 'approved LC command sequence')
    need([s['name'] for s in segments] == ['__TEXT','__DATA_CONST','__DATA','__LINKEDIT'], 'segment order')
    return segments

def overlaps(a, b, c, d):
    return max(a, c) < min(b, d)

def associate(runs, segments, targets=TARGETS):
    matches = {hex(t): [] for t in targets}
    for ri, run in enumerate(runs):
        if not run['count']:
            continue
        seg = segments[run['segment_index']]
        base = add(seg['vmaddr'], run['segment_offset'])
        step, count = run['stride'], run['count']
        for target in targets:
            # Each pointer interval intersects [target,target+8) iff its start
            # lies in [target-7,target+7]. At most two candidates when step>=8.
            low = max(0, (target-7-base+step-1)//step)
            high = min(count-1, (target+7-base)//step)
            for j in range(low, high+1):
                va = base+j*step
                off = run['segment_offset']+j*step
                fileoff = seg['fileoff']+off if off+8 <= seg['filesize'] else None
                matches[hex(target)].append({'run': ri, 'iteration': j, 'site_vmaddr': va, 'site_file_offset': fileoff, 'overlap': 'exact' if va == target else 'partial', 'stream_opcode_offset': run['opcode_offset']})
    return matches

def decode(data, mode, segments):
    need(mode in MODES, 'stream mode')
    pos, done, record, trace, runs = 0, False, 0, [], []
    state = {'segment': None, 'offset': 0, 'type': 1 if mode != 'rebase' else None, 'symbol_hex': None, 'flags': None, 'ordinal': None, 'addend': 0}
    implicit_type = mode != 'rebase'
    failure = None
    def operand(signed=False):
        nonlocal pos
        value, pos, raw = leb(data, pos, signed)
        event['operands'].append({'kind': 'SLEB64' if signed else 'ULEB64', 'raw_hex': raw, 'value': value})
        return value
    def emit(count, skip):
        nonlocal state
        need(state['segment'] is not None and state['type'] == 1, 'missing segment/pointer type state')
        need(mode == 'rebase' or state['symbol_hex'] is not None, 'missing symbol state')
        need(state['addend'] is not None, 'ambiguous lazy addend state')
        index, offset = state['segment'], state['offset']
        need(0 <= index < len(segments), 'segment index')
        seg = segments[index]
        stride = add(8, skip)
        need(offset <= seg['vmsize'], 'segment offset range')
        if count:
            need((count-1) <= U64//stride, 'repeat arithmetic overflow')
            last = add(offset, (count-1)*stride)
            need(add(last, 8) <= seg['vmsize'], 'pointer write crosses segment vmsize')
            add(seg['vmaddr'], add(last, 8))
        need(count <= U64//stride, 'repeat final arithmetic overflow')
        final = add(offset, count*stride)
        run = {'opcode_offset': start, 'record': record, 'segment_index': index, 'segment_offset': offset, 'count': count, 'stride': stride, 'write_bytes': 8, 'type': 1, 'type_implicit_local_model': implicit_type, 'final_offset': final}
        if mode != 'rebase':
            run['encoded_binding'] = {k: state[k] for k in ['symbol_hex','flags','ordinal','addend']}
        if count:
            last = offset+(count-1)*stride
            run['file_mapping'] = 'all_file_backed' if last+8 <= seg['filesize'] else ('all_virtual_only' if offset >= seg['filesize'] else 'mixed_or_partial_file_backing')
        else:
            run['file_mapping'] = 'zero_count_no_write'
        runs.append(run)
        state['offset'] = final
    try:
        while pos < len(data):
            start = pos
            byte = data[pos]
            pos += 1
            op, imm = byte & 0xf0, byte & 15
            event = {'offset': start, 'byte': byte, 'record': record, 'operands': []}
            trace.append(event)
            if op == 0:
                need(imm == 0, 'nonzero DONE immediate')
                done = True
                event['kind'] = 'DONE'
                if mode != 'lazy_bind':
                    need(not any(data[pos:]), 'nonzero data after terminal DONE')
                    event['zero_padding_bytes'] = len(data)-pos
                    pos = len(data)
                    break
                record += 1
                # Do not assume Apple reset/inheritance semantics: require each
                # later record to reestablish segment and symbol; addend only
                # remains known when both reset and inherited values would be0.
                state['segment'] = None
                state['symbol_hex'] = None
                state['flags'] = None
                state['ordinal'] = None
                if state['addend'] != 0:
                    state['addend'] = None
                state['type'] = 1
                implicit_type = True
                continue
            done = False
            if mode == 'rebase':
                if op == 0x10:
                    need(imm == 1, 'unsupported rebase type')
                    state['type'], implicit_type = 1, False
                elif op == 0x20:
                    need(imm < len(segments), 'segment index')
                    state['segment'], state['offset'] = imm, operand()
                    need(state['offset'] <= segments[imm]['vmsize'], 'segment offset range')
                elif op == 0x30:
                    need(imm == 0, 'reserved opcode immediate')
                    state['offset'] = add(state['offset'], operand())
                elif op == 0x40:
                    state['offset'] = add(state['offset'], imm*8)
                elif op == 0x50:
                    emit(imm, 0)
                elif op == 0x60:
                    need(imm == 0, 'reserved opcode immediate')
                    emit(operand(), 0)
                elif op == 0x70:
                    need(imm == 0, 'reserved opcode immediate')
                    emit(1, operand())
                elif op == 0x80:
                    need(imm == 0, 'reserved opcode immediate')
                    count, skip = operand(), operand()
                    emit(count, skip)
                else:
                    raise Unknown('unsupported rebase opcode')
            else:
                if op == 0x10:
                    state['ordinal'] = {'encoding': 'immediate', 'raw_immediate': imm}
                elif op == 0x20:
                    need(imm == 0, 'reserved opcode immediate')
                    state['ordinal'] = {'encoding': 'ULEB', 'value': operand()}
                elif op == 0x30:
                    state['ordinal'] = {'encoding': 'special_immediate', 'raw_immediate': imm, 'resolved_ordinal': None}
                elif op == 0x40:
                    need(imm & ~9 == 0, 'unknown symbol flags')
                    end = data.find(b'\0', pos)
                    need(end >= 0, 'unterminated symbol')
                    state['symbol_hex'], state['flags'] = data[pos:end].hex(), imm
                    event['symbol_hex'] = state['symbol_hex']
                    pos = end+1
                elif op == 0x50:
                    need(imm == 1, 'unsupported bind type')
                    state['type'], implicit_type = 1, False
                elif op == 0x60:
                    need(imm == 0, 'reserved opcode immediate')
                    state['addend'] = operand(True)
                elif op == 0x70:
                    need(imm < len(segments), 'segment index')
                    state['segment'], state['offset'] = imm, operand()
                    need(state['offset'] <= segments[imm]['vmsize'], 'segment offset range')
                elif op == 0x80:
                    need(imm == 0, 'reserved opcode immediate')
                    state['offset'] = add(state['offset'], operand())
                elif op in [0x90,0xa0]:
                    need(imm == 0, 'reserved opcode immediate')
                    emit(1, operand() if op == 0xa0 else 0)
                elif op == 0xb0:
                    emit(1, imm*8)
                elif op == 0xc0:
                    need(imm == 0, 'reserved opcode immediate')
                    count, skip = operand(), operand()
                    emit(count, skip)
                else:
                    raise Unknown('unsupported threaded bind opcode' if op == 0xd0 else 'unsupported bind opcode')
            event['end_exclusive'] = pos
        need(done or not data, 'missing terminal DONE')
    except Unknown as e:
        failure = {'opcode_offset': start if trace else 0, 'operand_cursor': pos, 'reason': str(e)}
    result = {'stream': mode, 'input_bytes': len(data), 'classic_pointer_site_decode_complete': failure is None, 'failure': failure, 'consumed_cursor': pos, 'opcode_count': len(trace), 'trace': trace, 'runs': runs, 'encoded_write_count': sum(r['count'] for r in runs), 'matches': associate(runs, segments), 'absence_claim_allowed': failure is None, 'runtime_binding_proved': False}
    return result

def analyze(folder):
    inputs = folder/'inputs'
    segs = load_segments((inputs/'load-commands.bin').read_bytes())
    streams = {mode: decode((inputs/(mode+'.bin')).read_bytes(), mode, segs) for mode in MODES}
    words = []
    for t in TARGETS:
        data = (inputs/('word-'+format(t,'x')+'.bin')).read_bytes()
        need(len(data) == 8, 'selected word length')
        by_stream = {mode: streams[mode]['matches'][hex(t)] for mode in MODES}
        hits = sum(len(x) for x in by_stream.values())
        words.append({'virtual_address': hex(t), 'file_offset': t, 'raw_hex': data.hex(), 'stored_u64': struct.unpack('<Q',data)[0], 'stream_matches': by_stream, 'hit_count': hits, 'duplicate_or_cross_stream': hits > 1, 'partial_overlap': any(h['overlap']=='partial' for hs in by_stream.values() for h in hs), 'all_streams_complete': all(s['classic_pointer_site_decode_complete'] for s in streams.values()), 'runtime_value': None})
    return {'id':'ELECTRIC-ENCODED-CLASSIC-POINTER-SITES-V1','segments':segs,'streams':streams,'six_words':words,'runtime_targets_or_provider_resolution':False,'pointer_patching':False,'method_qualification':'Encoded site association under pinned local classic-pointer transitions; implicit bind POINTER default is local-model context, not Apple runtime proof. Unsupported or incomplete streams cannot prove absence.'}

def pin(path):
    b = path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def put_json(path, value):
    with open(path, 'x') as f:
        json.dump(value,f,indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def main():
    need(len(sys.argv)==2, 'one explicit mode')
    if sys.argv[1] == '--analyze-once':
        frozen = json.loads((HERE/'inputs-manifest.json').read_text())
        before = [pin(HERE/x['relative_path']) for x in frozen['owned_pins']]
        need(before == [x['identity'] for x in frozen['owned_pins']], 'frozen owned identity')
        result = analyze(HERE)
        after = [pin(HERE/x['relative_path']) for x in frozen['owned_pins']]
        need(after == before, 'owned input/source drift')
        put_json(HERE/'result.json',result)
        put_json(HERE/'analysis-receipt.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'sys_argv':sys.argv,'sys_executable_context':sys.executable,'before':before,'after':after,'mode':'owned data only','original_or_decoder_calls':0,'retry':False})
        print(json.dumps({'streams':{n:{'complete':s['classic_pointer_site_decode_complete'],'failure':s['failure'],'runs':len(s['runs']),'writes':s['encoded_write_count']} for n,s in result['streams'].items()},'six_word_hits':[w['hit_count'] for w in result['six_words']]}))
    elif sys.argv[1] == '--check':
        need(analyze(HERE)==json.loads((HERE/'result.json').read_text()), 'owned result projection mismatch')
        print(json.dumps({'status':'PASS','owned_data_only':True}))
    else:
        raise Unknown('unknown mode')

if __name__ == '__main__':
    main()
