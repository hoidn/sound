"""Reviewer's static check of how a user-folder sidecar's entries bind to items (finding RVB-01).

Resolves, in the pinned helper slice, the index object's slot 0x108 and the 0x38 and 0x40
slots of the interface it returns, then prints the queries behind those two slots from the
helper corpus, and the reader's use of each slot for the folder and the pack resource kinds.

Usage: python3 -I binding_check.py HELPER_SLICE CORPUS_CHUNKS_DIR D2_RECORDS.jsonl
"""
import glob, json, os, re, struct, sys


def segs(data):
    _, _, _, _, ncmds, _, _, _ = struct.unpack_from('<IiiIIIII', data, 0)
    off, out = 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        if cmd == 0x19:
            vm, vms, fo, fs = struct.unpack_from('<QQQQ', data, off + 24)
            out.append((vm, fo, fs))
        off += size
    return out


def slot(data, ss, va):
    vm, fo, fs = next(s for s in ss if s[0] <= va < s[0] + s[2])
    w, = struct.unpack_from('<Q', data, fo + va - vm)
    t = w & 0xFFFFFFFFF  # chained-fixup rebase target (as read_ptrs.py in the H2 run)
    return t if t >= 0x100000000 else 0x100000000 + t


def records(chunks, wanted):
    out = {}
    for f in sorted(glob.glob(os.path.join(chunks, '*.jsonl'))):
        for line in open(f):
            r = json.loads(line)
            if r.get('entry') in wanted:
                out[r['entry']] = r['code']
    return out


def main(helper, chunks, d2):
    data = open(helper, 'rb').read()
    ss = segs(data)
    obj_vt, iface_vt = 0x100d92898, 0x100d92fd8  # vtables stored by the index constructor 0x10027d7b4
    s108 = slot(data, ss, obj_vt + 0x108)
    s38, s40 = slot(data, ss, iface_vt + 0x38), slot(data, ss, iface_vt + 0x40)
    print(f'index slot 0x108 -> {s108:#x}; interface slot 0x38 -> {s38:#x}; slot 0x40 -> {s40:#x}')
    code = records(chunks, {hex(s108), hex(s38), hex(s40)})
    print('slot 0x108 returns (object, object + 0x28):', '+ 0x28' in code[hex(s108)])
    for name, fn in (('0x38', s38), ('0x40', s40)):
        inner = re.search(r'(FUN_[0-9a-f]+)\(param_1,lVar3 \+ 0x118', code[hex(fn)]).group(1)
        q = records(chunks, {'0x' + inner[4:]})['0x' + inner[4:]]
        sql = re.search(r'"(SELECT[^"]*)"', q, re.S).group(1)
        print(f'slot {name} -> {inner}: {sql[:200]} ...')
    reader = next(json.loads(l)['code'] for l in open(d2) if json.loads(l)['entry'] == '0x1006d2624')
    print('reader calls slot 0x38 (folder resource branch):', '(*plStack_180 + 0x38)' in reader)
    print('reader calls slot 0x40 (pack resource branch):', '(*local_b0 + 0x40)' in reader)


if __name__ == '__main__':
    main(*sys.argv[1:4])
