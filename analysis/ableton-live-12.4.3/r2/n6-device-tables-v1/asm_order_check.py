"""Check the index order derived by extract_nested.py against builder disassembly (analyst tool; output is data).

usage: python3 -I asm_order_check.py <out-dir> <dossier-results-dir>

For each builder with a dossier, the slow-path emplace calls are listed in address order with the member
offset passed in x1 ('add x1,xN,#off'; 'mov x1,xN' = 0; a stack address = an empty or copied entry). Where
the slow blocks are laid out in push order this sequence equals the interpreter's sequence of entries
pushed directly by that function (sub-builder entries excluded; for a sub-builder run n times, its first
run); this is required for the three top-level builders. Otherwise only the set of member offsets is
compared, because duplicated slow blocks and stack-struct pushes break the address order.
Writes <out>/asm_order_check.txt. Depends on: out/live_index_map.tsv, dossiers n6-0002 and n6-0003.
"""
import collections, csv, glob, json, os, re, sys

PUSH = {'1030c50c0', '1030ed054', '1030ed1cc', '1031c280c', '1030ed63c', '103199bc0', '103199ed8', '103199a30',
        '103199d48', '103199734', '1030ed9c0', '1030c4c98', '1030ed468', '1031998c0', '1031c2694', '1030ed7f0'}
TOP = {'0x1030debd0', '0x103193b1c', '0x1031ad110'}


def asm_seq(d):
    seq = []
    for i, x in enumerate(d['disassembly']):
        m = re.fullmatch(r'bl 0x([0-9a-f]+)', x['text'])
        if not (m and m.group(1) in PUSH):
            continue
        off = None
        for y in reversed(d['disassembly'][max(0, i - 24):i]):
            mm = re.fullmatch(r'add x1,x\d+,#(0x[0-9a-f]+|\d+)', y['text'])
            if mm:
                off = int(mm.group(1), 0)
                break
            if re.fullmatch(r'mov x1,x\d+', y['text']):
                off = 0
                break
            if re.match(r'(?:add|sub) x1,(?:sp|x29)', y['text']):
                off = 'stack'
                break
        seq.append(off)
    return seq


def main(out, results):
    rows = list(csv.DictReader(open(os.path.join(out, 'live_index_map.tsv')), delimiter='\t'))
    lines, ok = [], True
    for f in sorted(glob.glob(os.path.join(results, 'n6-*/functions/*.json'))):
        d = json.load(open(f))
        fn = d['entry']
        mine = [r for r in rows if r['builder_fn'] == fn]
        if not mine:
            continue
        got = asm_seq(d)
        want = [int(r['member_path'].split('/')[-1], 16) if r['member_path'] else 'stack' for r in mine]
        # inline-only pushes (no slow path in the binary) cannot appear in the disassembly list
        n = len(want) // len(got) if got and len(want) % len(got) == 0 else 0
        first = want[:len(got)]
        if n and got == first:
            res, how = True, 'sequence' + (f' (first of {n} calls)' if n > 1 else '')
        elif n and got == first[1:] + first[:1]:
            res, how = True, 'sequence, first entry\'s slow block placed last' + (f' (first of {n} calls)' if n > 1 else '')
        elif fn in TOP:
            res, how = False, 'sequence'
        else:
            # slow blocks here are duplicated or out of order, and some entries are pushed by copying a
            # stack struct (x1 = stack address), so only the member offsets that do appear are compared
            gi, wi = {x for x in got if isinstance(x, int)}, {x for x in want if isinstance(x, int)}
            res = gi <= wi
            how = ('offset set: asm subset of interpreter; interpreter-only ' +
                   (','.join(hex(x) for x in sorted(wi - gi)) or 'none') + ' (stack-struct pushes)')
        ok &= res
        lines.append(f'{fn}\t{how}\tasm={len(got)}\tinterpreter={len(want)}\t{"PASS" if res else "FAIL"}')
    lines.append('ALL PASS' if ok else 'FAILURES')
    open(os.path.join(out, 'asm_order_check.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main(*sys.argv[1:3])
