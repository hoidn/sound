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

def load_context(table):
    need(len(table) == 1704, 'fixed approved LC length')
    cursor, segments, commands, dylibs = 0, [], [], 0
    for ordinal in range(15):
        need(cursor+8 <= len(table), 'LC header crossing')
        cmd, size = struct.unpack_from('<II', table, cursor)
        need(size >= 8 and size % 8 == 0 and cursor+size <= len(table), 'LC size/alignment')
        commands.append(cmd)
        if cmd == 0x19:
            need(size >= 72, 'segment command length')
            name, va, vs, fo, fs, maxp, initp, ns, flags = struct.unpack_from('<16s4Q4I', table, cursor+8)
            need(size == 72+80*ns and fo <= IMAGE_SIZE and fs <= IMAGE_SIZE-fo and fs <= vs, 'segment geometry')
            need(maxp & ~7 == 0 and initp & ~7 == 0, 'unknown protection bits')
            add(va, vs)
            segments.append({'index': len(segments), 'name': name.rstrip(b'\0').decode('ascii'), 'vmaddr': va, 'vmsize': vs, 'fileoff': fo, 'filesize': fs, 'maxprot': maxp, 'initprot': initp})
        if cmd == 0xc:
            need(size >= 24, 'dylib declaration size')
            nameoff = struct.unpack_from('<I', table, cursor+8)[0]
            need(24 <= nameoff < size and table.find(b'\0', cursor+nameoff, cursor+size) >= 0, 'dylib name bounds')
            dylibs += 1
        cursor += size
    need(cursor == len(table), 'LC complete coverage')
    need(commands == [25]*4+[0x80000022,2,11,27,50,42,12,12,38,41,29], 'approved LC command sequence')
    need([s['name'] for s in segments] == ['__TEXT','__DATA_CONST','__DATA','__LINKEDIT'], 'segment order')
    need(dylibs == 2, 'approved dylib declaration count')
    return {'segments': segments, 'dylib_count': dylibs, 'linkedit_index': 3, 'permissions_kind': 'encoded initial protections only, not runtime permissions'}

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

def decode(data, mode, context):
    need(mode in MODES, 'stream mode')
    segments = context['segments']
    pos, done, record, trace, runs = 0, False, 0, [], []
    default_type = 1 if mode in ['weak_bind','lazy_bind'] else 0
    origin = 'analyzer_'+mode+'_POINTER_default' if default_type else 'unset'
    state = {'segment': None, 'offset': 0, 'type': default_type, 'symbol_hex': None, 'flags': None, 'ordinal': {'encoding':'weak_lookup_default','value':-3} if mode=='weak_bind' else None, 'addend': 0}
    failure = None
    def operand(signed=False):
        nonlocal pos
        value, pos, raw = leb(data, pos, signed)
        event['operands'].append({'kind': 'SLEB64' if signed else 'ULEB64', 'raw_hex': raw, 'value': value})
        return value
    def emit(count, stride):
        need(stride >= 8 and stride <= U64, 'unsupported repeat stride')
        need(state['segment'] is not None and state['type'] == 1, 'missing segment/explicit POINTER state')
        index, offset = state['segment'], state['offset']
        need(0 <= index < context['linkedit_index'], 'non-LINKEDIT segment index')
        seg = segments[index]
        need(seg['vmsize'] >= 8, 'segment vmsize below pointer width')
        need(seg['initprot'] & 2 and not seg['initprot'] & 4, 'encoded segment permissions unsupported')
        if mode != 'rebase':
            need(state['symbol_hex'] is not None, 'missing symbol state')
            need(state['ordinal'] is not None, 'missing ordinal state')
            need(-3 <= state['ordinal']['value'] <= context['dylib_count'], 'ordinal outside encoded declaration range')
        need(offset <= seg['vmsize'], 'segment offset range')
        if count:
            need(count-1 <= U64//stride, 'repeat arithmetic overflow')
            last = add(offset, (count-1)*stride)
            end = add(last, 8)
            need(end <= seg['vmsize'], 'pointer interval crosses segment vmsize')
            need(end <= seg['filesize'], 'pointer interval not wholly file-backed')
            add(seg['vmaddr'], end)
            need(add(seg['fileoff'], end) <= IMAGE_SIZE, 'pointer file mapping')
        else:
            end = offset
        run = {'opcode_offset':start, 'record':record, 'segment_index':index, 'segment_offset':offset, 'count':count, 'stride':stride, 'write_bytes':8, 'type':1, 'type_origin':origin, 'last_interval_end':end, 'file_mapping':'all_file_backed' if count else 'zero_count_no_write'}
        if mode != 'rebase':
            run['encoded_binding'] = {k:state[k] for k in ['symbol_hex','flags','ordinal','addend']}
        runs.append(run)
    def strict_advance(delta):
        state['offset'] = add(state['offset'], delta)
    def modular_advance(value, pointer_increment):
        # Selected only for ordinary/weak 0x80 or 0xa0, never geometry/LEB/repeats.
        before = state['offset']
        raw_delta = value+pointer_increment
        state['offset'] = (before+raw_delta) & U64
        event['modular_advance'] = {'before':before,'uleb':value,'pointer_increment':pointer_increment,'delta_mod64':raw_delta & U64,'after':state['offset'],'wrapped':before+raw_delta > U64}
    def repeated(count, skip):
        stride = add(8, skip)
        need(count <= U64//stride, 'repeat final arithmetic overflow')
        delta = count*stride
        # Runs are proven monotonically bounded; no modular repeated traversal.
        add(state['offset'], delta)
        emit(count, stride)
        strict_advance(delta)
    try:
        while pos < len(data):
            start = pos
            byte = data[pos]
            pos += 1
            op, imm = byte & 0xf0, byte & 15
            event = {'offset':start,'byte':byte,'record':record,'offset_before':state['offset'],'operands':[]}
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
                # Selected shared whole-stream lazy scan: DONE does not reset.
                continue
            done = False
            if mode == 'rebase':
                if op == 0x10:
                    need(imm == 1, 'unsupported rebase type')
                    state['type'], origin = 1, 'explicit_SET_TYPE_POINTER'
                elif op == 0x20:
                    need(imm < context['linkedit_index'], 'non-LINKEDIT segment index')
                    state['segment'], state['offset'] = imm, operand()
                    need(state['offset'] <= segments[imm]['vmsize'], 'segment offset range')
                elif op == 0x30:
                    need(imm == 0 and state['segment'] is not None, 'reserved immediate/missing segment')
                    strict_advance(operand())
                elif op == 0x40:
                    need(state['segment'] is not None, 'missing segment state')
                    strict_advance(imm*8)
                elif op == 0x50:
                    repeated(imm, 0)
                elif op in [0x60,0x70,0x80]:
                    need(imm == 0, 'reserved opcode immediate')
                    if op == 0x60:
                        repeated(operand(), 0)
                    elif op == 0x70:
                        repeated(1, operand())
                    else:
                        count, skip = operand(), operand()
                        repeated(count, skip)
                else:
                    raise Unknown('unsupported rebase opcode')
            else:
                if mode == 'lazy_bind':
                    need(op in [0x10,0x20,0x30,0x40,0x60,0x70,0x90], 'unsupported shared whole-lazy opcode')
                if mode == 'weak_bind':
                    need(op not in [0x10,0x20,0x30], 'ordinal opcode forbidden in weak stream')
                if op == 0x10:
                    state['ordinal'] = {'encoding':'immediate','value':imm}
                elif op == 0x20:
                    need(imm == 0, 'reserved opcode immediate')
                    value = operand()
                    need(value <= (1 << 31)-1, 'unsupported ordinal integer conversion')
                    state['ordinal'] = {'encoding':'ULEB','value':value}
                elif op == 0x30:
                    state['ordinal'] = {'encoding':'special_immediate','raw_immediate':imm,'value':0 if imm==0 else (imm | 0xf0)-256}
                elif op == 0x40:
                    need(imm & ~9 == 0, 'unknown symbol flags')
                    end = data.find(b'\0',pos)
                    need(end >= 0, 'unterminated symbol')
                    state['symbol_hex'], state['flags'] = data[pos:end].hex(), imm
                    event['symbol_hex'] = state['symbol_hex']
                    event['strong_definition_marker'] = mode == 'weak_bind' and bool(imm & 8)
                    pos = end+1
                elif op == 0x50:
                    need(imm == 1, 'unsupported bind type')
                    state['type'], origin = 1, 'explicit_SET_TYPE_POINTER'
                elif op == 0x60:
                    need(imm == 0, 'reserved opcode immediate')
                    state['addend'] = operand(True)
                elif op == 0x70:
                    need(imm < context['linkedit_index'], 'non-LINKEDIT segment index')
                    state['segment'], state['offset'] = imm, operand()
                    need(state['offset'] <= segments[imm]['vmsize'], 'segment offset range')
                elif op == 0x80:
                    need(imm == 0 and state['segment'] is not None, 'reserved immediate/missing segment')
                    modular_advance(operand(),0)
                elif op == 0x90:
                    need(imm == 0, 'reserved opcode immediate')
                    emit(1,8)
                    strict_advance(8)
                elif op == 0xa0:
                    need(imm == 0, 'reserved opcode immediate')
                    emit(1,8)  # Accepted current emission precedes next operand/advance.
                    modular_advance(operand(),8)
                elif op == 0xb0:
                    emit(1,8)
                    strict_advance(add(8,imm*8))
                elif op == 0xc0:
                    need(imm == 0, 'reserved opcode immediate')
                    count, skip = operand(), operand()
                    repeated(count,skip)
                else:
                    raise Unknown('unsupported threaded bind opcode' if op==0xd0 else 'unsupported bind opcode')
            event['end_exclusive'],event['offset_after'] = pos,state['offset']
        need(done or not data, 'missing terminal DONE')
    except Unknown as error:
        failure = {'opcode_offset':start if trace else 0,'operand_cursor':pos,'reason':str(error)}
    return {'stream':mode,'input_bytes':len(data),'classic_pointer_site_decode_complete':failure is None,'failure':failure,'consumed_cursor':pos,'opcode_count':len(trace),'trace':trace,'runs':runs,'encoded_write_count':sum(r['count'] for r in runs),'matches':associate(runs,segments),'absence_claim_allowed':failure is None,'runtime_binding_proved':False}

def analyze(folder):
    inputs = folder/'inputs'
    context = load_context((inputs/'load-commands.bin').read_bytes())
    seg = context['segments'][1]
    for target in TARGETS:
        need(seg['vmaddr']==seg['fileoff']==0x30000 and target+8 <= seg['vmaddr']+seg['filesize'], 'selected word mapping')
    streams = {mode:decode((inputs/(mode+'.bin')).read_bytes(),mode,context) for mode in MODES}
    words = []
    for target in TARGETS:
        data = (inputs/('word-'+format(target,'x')+'.bin')).read_bytes()
        need(len(data)==8, 'selected word length')
        matches = {mode:streams[mode]['matches'][hex(target)] for mode in MODES}
        hits = sum(len(x) for x in matches.values())
        words.append({'virtual_address':hex(target),'file_offset':target,'raw_hex':data.hex(),'stored_u64':struct.unpack('<Q',data)[0],'stream_matches':matches,'accepted_hit_count':hits,'observed_duplicate_or_cross_stream':hits>1,'observed_partial_overlap':any(h['overlap']=='partial' for hs in matches.values() for h in hs),'all_streams_complete':all(s['classic_pointer_site_decode_complete'] for s in streams.values()),'runtime_value':None})
    return {'id':'ELECTRIC-ENCODED-CLASSIC-POINTER-SITES-V2','method':'Approved dyld-852.2 analyzer ordinary/weak plus shared whole-lazy subset; strict rebase and bounded repeats. Not a runtime loader.','context':context,'streams':streams,'six_words':words,'runtime_targets_or_provider_resolution':False,'pointer_patching':False}

def pin(path):
    data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def put_json(path,value):
    with open(path,'x') as f:
        json.dump(value,f,indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def main():
    need(len(sys.argv)==2,'one explicit mode')
    if sys.argv[1]=='--analyze-once':
        frozen=json.loads((HERE/'inputs-manifest.json').read_text())
        before=[pin(HERE/x['relative_path']) for x in frozen['owned_pins']]
        need(before==[x['identity'] for x in frozen['owned_pins']],'frozen owned identity')
        result=analyze(HERE)
        after=[pin(HERE/x['relative_path']) for x in frozen['owned_pins']]
        need(after==before,'owned input/source drift')
        put_json(HERE/'result.json',result)
        put_json(HERE/'analysis-receipt.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'sys_argv':sys.argv,'sys_executable_context':sys.executable,'before':before,'after':after,'mode':'owned data only','original_or_native_decoder_calls':0,'retry':False})
        print(json.dumps({'streams':{n:{'complete':s['classic_pointer_site_decode_complete'],'failure':s['failure'],'runs':len(s['runs']),'writes':s['encoded_write_count']} for n,s in result['streams'].items()},'six_word_hits':[w['accepted_hit_count'] for w in result['six_words']]}))
    elif sys.argv[1]=='--check':
        need(analyze(HERE)==json.loads((HERE/'result.json').read_text()),'owned result projection mismatch')
        print(json.dumps({'status':'PASS','owned_data_only':True}))
    else:
        raise Unknown('unknown mode')

if __name__=='__main__':
    main()
