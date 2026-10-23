"""Plan x86 GDB coverage from a complete declared contiguous instruction range."""
import re

def plan(rows, begin, end):
    assert rows and rows[0]['addr']==begin and begin<end
    pc=begin
    for row in rows:
        assert row['addr']==pc and row['length']>0
        pc+=row['length']
    assert pc==end
    addresses={r['addr'] for r in rows}
    blocks={begin};calls=[];branches=[];returns=[]
    for row in rows:
        pc=row['addr'];op=row['asm'].split()[0];nxt=pc+row['length']
        if op.startswith('call'):calls.append(pc)
        if op.startswith('ret'):returns.append(pc)
        if op.startswith('j') or op.startswith('loop'):
            branches.append(pc)
            target=re.search(r'\b0x([0-9a-f]+)',row['asm'])
            if target and int(target[1],16) in addresses:blocks.add(int(target[1],16))
        if (op.startswith(('j','loop','call','ret'))) and nxt in addresses:blocks.add(nxt)
    return {'blocks':sorted(blocks),'calls':calls,'branches':branches,'returns':returns,
            'indirects':[r['addr'] for r in rows if r['addr'] in calls+branches and '*' in r['asm']]}

def effective(assembly, regs, read_pointer, pc, length):
    operand=assembly.split(None,1)[1].split('#')[0].strip()
    if not operand.startswith('*'):
        match=re.match(r'0x([0-9a-f]+)',operand)
        return int(match[1],16) if match else None
    operand=operand[1:]
    match=re.fullmatch(r'%([a-z0-9]+)',operand)
    if match:return regs.get(match[1])
    match=re.fullmatch(r'(?:(-?0x[0-9a-f]+))?\(%([a-z0-9]+)\)',operand)
    if match:
        base=pc+length if match[2]=='rip' else regs.get(match[2])
        return None if base is None else read_pointer(base+int(match[1] or '0',16))
    return None  # Indexed/segment/address-size forms stay UNKNOWN.
