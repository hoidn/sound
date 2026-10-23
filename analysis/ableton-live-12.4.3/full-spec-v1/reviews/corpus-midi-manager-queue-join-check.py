"""Selected data/bitfields only. No original function, decoder, tool or instruction runs."""
from pathlib import Path
import copy, hashlib, json, struct, sys
ROOT = Path('/home/ollie/Documents/sound')
Q = ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/queries'
PRIMARY = {
 'corpus-midi-enrollment-argument-frontier-2026-10-20.json':'da39dc9b05a3b83fcffff293f97848d5219b713dd34ba57e67b0ec190675fcac',
 'corpus-midi-module-queue-slots-frontier-2026-10-20.json':'447cc100e7afe1344da014c17171719c9273087b6ea68fa9de5ad0a200ce1d90',
 'corpus-midi-module-enrollment-hooks-frontier-2026-10-20.json':'4e639e202ef7f53f74b8e1d59c55131340fef8f77cda07ee58125d3c9e80c2a0',
 'corpus-midi-render-initialization-frontier-2026-10-20.json':'c75e224ce7cfa6f0e45973219dfba6598c2e0782c9975d0949314a262ac87952',
 'corpus-midi-module-list-membership-frontier-2026-10-20.json':'0bbed110151c0e9b5ff81cc218997a2adb425486b51ec316a60ed13b78f6e206'}

def ident(p):
    b = p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def signed(x, bits): return x - (1 << bits) if x & (1 << (bits-1)) else x

def fields(w, pc, family):
    if family == 'RET':
        assert w & 0xfffffc1f == 0xd65f0000
        return {'Rn':(w>>5)&31}
    if family == 'BLR register':
        assert w & 0xfffffc1f == 0xd63f0000
        return {'Rn':(w>>5)&31}
    if family == 'BL immediate':
        assert w >> 26 == 0x25
        off = signed(w & ((1<<26)-1),26)*4
        return {'signed_byte_offset':off,'target':hex(pc+off)}
    if family == 'compare and branch':
        assert w & 0x7e000000 == 0x34000000
        off = signed((w>>5)&0x7ffff,19)*4
        return {'width':64 if w>>31 else 32,'Rt':w&31,'nonzero':(w>>24)&1,
                'signed_byte_offset':off,'target':hex(pc+off)}
    if family == '64-bit general register pair':
        assert w & 0x3a000000 == 0x28000000 and w>>30 == 2 and not w&(1<<26)
        mode = (w>>23)&3
        return {'load':(w>>22)&1,'Rt':w&31,'Rt2':(w>>10)&31,'Rn':(w>>5)&31,
                'signed_scaled_byte_offset':signed((w>>15)&127,7)*8,
                'address_mode':{1:'post-index',2:'signed offset',3:'pre-index'}[mode]}
    if family == 'load/store unsigned immediate':
        assert w & 0xffc00000 in [0xf9400000,0xf9000000,0xb9400000,0xb9000000]
        size = w>>30
        return {'width':8<<size,'load':(w>>22)&1,'Rt':w&31,'Rn':(w>>5)&31,
                'byte_offset':((w>>10)&4095)*(1<<size)}
    if family == '64-bit load pre-index':
        assert w & 0xffe00c00 == 0xf8400c00
        return {'Rt':w&31,'Rn':(w>>5)&31,'signed_byte_offset':signed((w>>12)&511,9)}
    if family == 'add/sub immediate':
        assert w & 0x1f000000 == 0x11000000 and not w&(1<<29)
        return {'width':64 if w>>31 else 32,'subtract':(w>>30)&1,'Rn':(w>>5)&31,'Rd':w&31,
                'immediate':((w>>10)&4095) << (12 if w&(1<<22) else 0)}
    if family == 'MOV alias of ORR with zero register':
        assert w & 0x7fe0ffe0 == 0x2a0003e0
        return {'width':64 if w>>31 else 32,'Rm':(w>>16)&31,'Rd':w&31}
    if family == 'MOVZ':
        assert w & 0x7f800000 == 0x52800000
        return {'width':64 if w>>31 else 32,'Rd':w&31,'imm16':(w>>5)&65535,'shift':((w>>21)&3)*16}
    if family == 'SXTW alias of signed bitfield move':
        assert w & 0xffc00000 == 0x93400000
        return {'width':64,'Rn':(w>>5)&31,'Rd':w&31,'immr':(w>>16)&63,'imms':(w>>10)&63}
    if family == 'ADD extended register':
        assert w & 0xff200000 == 0x8b200000 and ((w>>13)&7) == 6
        return {'Rn':(w>>5)&31,'Rm':(w>>16)&31,'Rd':w&31,'extend':'SXTW','shift':(w>>10)&7}
    if family == 'ADD shifted register':
        assert w & 0xff200000 == 0x8b000000 and ((w>>22)&3) == 0
        return {'Rn':(w>>5)&31,'Rm':(w>>16)&31,'Rd':w&31,'shift_kind':'LSL','shift':(w>>10)&63}
    raise AssertionError(family)

def main():
    assert sys.argv[1:] == ['--check'], 'Read-only selected-data --check only.'
    docs = {}
    for name, digest in PRIMARY.items():
        assert ident(Q/name)['sha256'] == digest
        docs[name] = json.loads((Q/name).read_text())
    watched = {Q/n for n in PRIMARY} | {Path(__file__)}
    for d in docs.values(): watched |= {Path(r['path']) for r in d['input_pins_asof']}
    before = {str(p):ident(p) for p in sorted(watched)}
    for d in docs.values():
        for r in d['input_pins_asof']: assert ident(Path(r['path'])) == r
    arg = docs['corpus-midi-enrollment-argument-frontier-2026-10-20.json']
    slots = docs['corpus-midi-module-queue-slots-frontier-2026-10-20.json']
    image_record = arg['instruction_data_and_limited_decodes']
    image = Path(image_record['image_path']).read_bytes()
    assert hashlib.sha256(image).hexdigest() == image_record['image_sha256'] and len(image) == 248624
    header = struct.unpack_from('<IiiIIIII',image)
    assert header[0] == 0xfeedfacf and header[1] == 0x100000c and header[3] == 8
    pos, segments = 32, []
    for _ in range(header[4]):
        command,size = struct.unpack_from('<II',image,pos)
        assert size >= 8 and pos+size <= 32+header[5]
        if command == 0x19:
            name,va,vs,fo,fs = struct.unpack_from('<16sQQQQ',image,pos+8)
            segments.append({'name':name.rstrip(b'\0').decode(),'vmaddr':hex(va),'vmsize':vs,'fileoff':fo,'filesize':fs})
        pos += size
    assert pos == 32+header[5] and segments == image_record['segments'] == slots['data_and_target_metadata']['segments']
    assert image[:32].hex() == image_record['header_hex']
    decoded = []
    for span in image_record['spans']:
        va = int(span['start'],16)
        seg = next(s for s in segments if int(s['vmaddr'],16)<=va and va+span['bytes']<=int(s['vmaddr'],16)+s['filesize'])
        off = seg['fileoff']+va-int(seg['vmaddr'],16)
        raw = image[off:off+span['bytes']]
        assert off == span['file_offset'] and raw.hex() == span['raw_hex'] and hashlib.sha256(raw).hexdigest() == span['sha256']
        assert len(raw) == span['bytes'] == int(span['end_inclusive'],16)-va+1
        for i, row in enumerate(span['words']):
            w = struct.unpack_from('<I',raw,i*4)[0]; pc = va+i*4
            assert w == int(row['word'],16) and hex(pc) == row['address'] and raw[i*4:i*4+4].hex() == row['raw_le_hex']
            got = fields(w,pc,row['family'])
            assert got == row['fields']
            decoded.append({'address':hex(pc),'word':hex(w),'family':row['family'],'independent_fields':got})
    assert len(decoded) == 50
    pointers = []
    for row in slots['data_and_target_metadata']['selected_words']:
        va = int(row['virtual_address'],16)
        seg = next(s for s in segments if int(s['vmaddr'],16)<=va< int(s['vmaddr'],16)+s['filesize'])
        off = seg['fileoff']+va-int(seg['vmaddr'],16)
        raw = image[off:off+8]
        assert off == row['file_offset'] and raw.hex() == row['raw_le_hex']
        assert hex(struct.unpack('<Q',raw)[0]) == row['target']
        pointers.append({'virtual_address':hex(va),'file_offset':off,'raw_hex':raw.hex(),'target':row['target']})
    assert [p['target'] for p in pointers] == ['0x1824c','0x18258']
    # Fresh exact source-record equality; no function is imported or executed.
    count, total = 0, 0
    for d in docs.values():
        records = d.get('source_records',[]) + ([d['source_record']] if 'source_record' in d else [])
        for record in records:
            path = Path(record['path']); raw = path.read_bytes().splitlines(keepends=True)[record['line_1based']-1]
            assert hashlib.sha256(raw).hexdigest() == record['raw_record_sha256']
            assert json.loads(raw) == record['record']
            body = record['record']['code'].encode()
            assert len(body) == record['record']['code_bytes'] and hashlib.sha256(body).hexdigest() == record['record']['code_sha256']
            count += 1; total += len(body)
    selected = {r['address']:r['independent_fields'] for r in decoded}
    def carrier_guards(rows):
        assert rows['0x1b820'] == {'load':0,'Rt':21,'Rt2':31,'Rn':31,'signed_scaled_byte_offset':0,'address_mode':'signed offset'}
        assert rows['0x1b824']['imm16'] == 0
        assert rows['0x1b814']['target'] == '0xec40'
        assert rows['0xec88']['Rt2'] == 21 and rows['0xec88']['load'] == 1
        assert rows['0xb768']['immediate'] == 16
        assert rows['0xb76c']['byte_offset'] == rows['0xb778']['immediate'] == 8
        assert rows['0xb774']['byte_offset'] == 64
        assert rows['0xb780']['Rn'] == 9
    carrier_guards(selected)
    rejected = []
    for name, addr, field, value in [('ec40 return used as carrier','0x1b820','Rt',0),
          ('nonzero mode','0x1b824','imm16',1),('wrong ec40 target','0x1b814','target','0xec44'),
          ('missing X21 restore','0xec88','Rt2',20),('cursor points before caller slot','0xb768','immediate',8),
          ('cursor storage mismatch','0xb76c','byte_offset',16),('cursor-address mismatch','0xb778','immediate',16),
          ('wrong receiver slot','0xb774','byte_offset',56),('wrong call register','0xb780','Rn',8)]:
        bad = copy.deepcopy(selected); bad[addr][field] = value
        try: carrier_guards(bad)
        except AssertionError: rejected.append(name)
        else: raise AssertionError(name)
    assert -32+16+16 == 0 and -32+8 == -24
    after = {str(p):ident(p) for p in sorted(watched)}
    assert before == after
    print(json.dumps({'image':ident(Path(image_record['image_path'])),'segments':segments,
          'selected_instruction_bytes':200,'decoded_words':decoded,'selected_data_bytes':16,'pointer_words':pointers,
          'source_record_instances_exact':count,'source_code_instance_bytes':total,'counterexamples_rejected':rejected,
          'stack_equations_entrySP_relative':{'lowerSP':-32,'FP':-16,'initial_cursor_value':0,'cursor_storage_and_X2':-24},
          'scope':'Selected initialization carrier only; no9300render argument proof, actual membership, event representation, Live/x86 or grade.',
          'watch_before':list(before.values()),'watch_after_equal':True,'watched':len(watched),
          'native_instruction_or_source_execution':0,'old_tool_or_decoder_execution':0},indent=2))

if __name__ == '__main__': main()
