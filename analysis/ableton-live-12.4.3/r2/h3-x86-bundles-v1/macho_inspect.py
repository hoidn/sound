#!/usr/bin/env python3
"""Read-only Mach-O inspector for packet H3 (stdlib only; run with python3 -I).

Usage: macho_inspect.py BINARY OUT.json [STRINGS_DIR]

Writes per-slice identity (SHA-256), header, load commands, linked dylibs,
export-trie entries, symbol-table summary (defined externals and imports with
their dylib), code-signature identifier/team/entitlements, and, if STRINGS_DIR is
given, one <arch>.cstrings.tsv per slice (file offset, vmaddr, section, value) for
every C string in __cstring/__const-like sections. Never executes the input.
"""
import hashlib
import json
import struct
import sys

CPU = {0x01000007: 'x86_64', 0x0100000c: 'arm64', 7: 'i386', 0x12: 'ppc'}
FILETYPE = {1: 'MH_OBJECT', 2: 'MH_EXECUTE', 6: 'MH_DYLIB', 8: 'MH_BUNDLE'}
LC = {0x19: 'LC_SEGMENT_64', 0x1: 'LC_SEGMENT', 0x2: 'LC_SYMTAB', 0xb: 'LC_DYSYMTAB', 0xc: 'LC_LOAD_DYLIB',
      0xd: 'LC_ID_DYLIB', 0x80000018: 'LC_LOAD_WEAK_DYLIB', 0x8000001f: 'LC_REEXPORT_DYLIB',
      0x8000001c: 'LC_RPATH', 0x1b: 'LC_UUID', 0x32: 'LC_BUILD_VERSION', 0x24: 'LC_VERSION_MIN_MACOSX',
      0x80000028: 'LC_MAIN', 0x5: 'LC_UNIXTHREAD', 0x22: 'LC_DYLD_INFO', 0x80000022: 'LC_DYLD_INFO_ONLY',
      0x80000033: 'LC_DYLD_EXPORTS_TRIE', 0x80000034: 'LC_DYLD_CHAINED_FIXUPS', 0x1d: 'LC_CODE_SIGNATURE',
      0x26: 'LC_FUNCTION_STARTS', 0x29: 'LC_DATA_IN_CODE', 0x2a: 'LC_SOURCE_VERSION',
      0x2c: 'LC_ENCRYPTION_INFO_64', 0x2d: 'LC_LINKER_OPTION', 0x1a: 'LC_ROUTINES_64',
      0x12: 'LC_SUB_FRAMEWORK', 0x2b: 'LC_DYLIB_CODE_SIGN_DRS', 0x2e: 'LC_LINKER_OPTIMIZATION_HINT'}
PLATFORM = {1: 'macos', 2: 'ios', 6: 'maccatalyst'}
DYLIB_CMDS = (0xc, 0xd, 0x80000018, 0x8000001f)


def ver(v):
    return f'{v >> 16}.{(v >> 8) & 0xff}.{v & 0xff}'


def cstr(data, off):
    return data[off:data.index(b'\0', off)].decode('utf-8', 'replace')


def uleb(data, off):
    result = shift = 0
    while True:
        b = data[off]
        off += 1
        result |= (b & 0x7f) << shift
        shift += 7
        if b < 0x80:
            return result, off


def export_trie(data, start, size):
    out, stack, seen = [], [(start, '')], set()
    while stack:
        node, prefix = stack.pop()
        if node in seen or not start <= node < start + size:
            raise ValueError(f'bad export-trie node 0x{node:x}')
        seen.add(node)
        tsize, off = uleb(data, node)
        if tsize:
            flags, p = uleb(data, off)
            entry = dict(name=prefix, flags=flags)
            if flags & 8:  # re-export
                entry['reexport_ordinal'], p = uleb(data, p)
            else:
                addr, p = uleb(data, p)
                entry['address'] = f'0x{addr:x}'
            out.append(entry)
        off += tsize
        count = data[off]
        off += 1
        for _ in range(count):
            label = data.index(b'\0', off)
            edge = data[off:label].decode('utf-8', 'replace')
            child, off = uleb(data, label + 1)
            stack.append((start + child, prefix + edge))
    return sorted(out, key=lambda e: e['name'])


def code_signature(data, off, size):
    blob = data[off:off + size]
    magic, length, count = struct.unpack_from('>III', blob)
    info = {'superblob_magic': f'0x{magic:x}', 'blobs': []}
    for i in range(count):
        btype, boff = struct.unpack_from('>II', blob, 12 + 8 * i)
        bmagic, blen = struct.unpack_from('>II', blob, boff)
        info['blobs'].append({'type': f'0x{btype:x}', 'magic': f'0x{bmagic:x}', 'length': blen})
        if bmagic == 0xfade0c02 and 'identifier' not in info:  # CodeDirectory
            cd_ver, flags, _, ident, _, _, _, _, hsize, htype = struct.unpack_from('>IIIIIIIIBB', blob, boff + 8)
            info.update(cd_version=f'0x{cd_ver:x}', cd_flags=f'0x{flags:x}', hash_type=htype,
                        identifier=cstr(blob, boff + ident))
            if cd_ver >= 0x20200:
                team = struct.unpack_from('>I', blob, boff + 48)[0]
                info['team_id'] = cstr(blob, boff + team) if team else None
            if cd_ver >= 0x20400:
                info['runtime_version'] = ver(struct.unpack_from('>I', blob, boff + 88)[0])
        elif bmagic == 0xfade7171:
            info['entitlements_xml'] = blob[boff + 8:boff + blen].decode('utf-8', 'replace')
    return info


def symtab(data, symoff, nsyms, stroff, dylibs, is64):
    defined, imports = [], []
    fmt, width = ('<IBBHQ', 16) if is64 else ('<IBBHI', 12)
    for i in range(nsyms):
        strx, ntype, sect, desc, value = struct.unpack_from(fmt, data, symoff + width * i)
        if ntype & 0xe0:  # stab
            continue
        name = cstr(data, stroff + strx)
        ext, kind = ntype & 1, ntype & 0x0e
        if ext and kind == 0xe:
            defined.append({'name': name, 'value': f'0x{value:x}', 'sect': sect})
        elif ext and kind == 0:
            ordinal = (desc >> 8) & 0xff
            lib = dylibs[ordinal - 1] if 0 < ordinal <= len(dylibs) else {0: 'self', 0xfe: 'executable', 0xff: 'flat'}.get(ordinal, f'ordinal {ordinal}')
            imports.append({'name': name, 'library': lib, 'weak_ref': bool(desc & 0x40)})
    return defined, imports


def slice_info(data, arch, strings_dir):
    magic, cpu, sub, ftype, ncmds, sizeofcmds, flags = struct.unpack_from('<7I', data)
    if magic not in (0xfeedfacf, 0xfeedface):
        raise ValueError(f'{arch}: not a little-endian Mach-O (magic 0x{magic:x})')
    is64 = magic == 0xfeedfacf
    info = {'cputype': CPU.get(cpu, hex(cpu)), 'cpusubtype': f'0x{sub:x}', 'filetype': FILETYPE.get(ftype, ftype),
            'flags': f'0x{flags:x}', 'ncmds': ncmds, 'sizeofcmds': sizeofcmds, 'load_commands': []}
    dylibs, sections, off = [], [], 32 if is64 else 28
    trie = sym = None
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        lc = {'cmd': LC.get(cmd, f'0x{cmd:x}'), 'size': size}
        if cmd in (0x19, 0x1):  # LC_SEGMENT_64 / LC_SEGMENT
            seg_fmt, sec_fmt, hdr, ssz = (('<16sQQQQiiII', '<16s16sQQIIIII', 72, 80) if cmd == 0x19
                                          else ('<16sIIIIiiII', '<16s16sIIIIIII', 56, 68))
            name, vm, vms, fo, fs, maxp, initp, nsects, sflags = struct.unpack_from(seg_fmt, data, off + 8)
            lc.update(segname=name.rstrip(b'\0').decode(), vmaddr=f'0x{vm:x}', vmsize=vms, fileoff=fo,
                      filesize=fs, initprot=initp, sections=[])
            for s in range(nsects):
                sname, segn, addr, ssize, soff, _, _, _, stype = struct.unpack_from(sec_fmt, data, off + hdr + ssz * s)
                sec = {'sectname': sname.rstrip(b'\0').decode(), 'addr': f'0x{addr:x}', 'size': ssize,
                       'offset': soff, 'type': stype & 0xff}
                lc['sections'].append(sec)
                sections.append((lc['segname'], sec, addr))
        elif cmd in DYLIB_CMDS:
            noff, _, cur, compat = struct.unpack_from('<IIII', data, off + 8)
            lc.update(name=cstr(data, off + noff), current=ver(cur), compatibility=ver(compat))
            if cmd != 0xd:
                dylibs.append(lc['name'])
        elif cmd == 0x8000001c:
            lc['path'] = cstr(data, off + struct.unpack_from('<I', data, off + 8)[0])
        elif cmd == 0x1b:
            lc['uuid'] = data[off + 8:off + 24].hex()
        elif cmd == 0x32:
            plat, minos, sdk, ntools = struct.unpack_from('<IIII', data, off + 8)
            lc.update(platform=PLATFORM.get(plat, plat), minos=ver(minos), sdk=ver(sdk),
                      tools=[dict(zip(('tool', 'version'), (t, ver(v)))) for t, v in
                             (struct.unpack_from('<II', data, off + 24 + 8 * i) for i in range(ntools))])
        elif cmd == 0x24:
            v, s = struct.unpack_from('<II', data, off + 8)
            lc.update(minos=ver(v), sdk=ver(s))
        elif cmd == 0x80000028:
            e, st = struct.unpack_from('<QQ', data, off + 8)
            lc.update(entryoff=f'0x{e:x}', stacksize=st)
        elif cmd == 0x2:
            sym = struct.unpack_from('<IIII', data, off + 8)
            lc.update(symoff=sym[0], nsyms=sym[1], stroff=sym[2], strsize=sym[3])
        elif cmd == 0xb:
            f = struct.unpack_from('<6I', data, off + 8)
            lc.update(ilocalsym=f[0], nlocalsym=f[1], iextdefsym=f[2], nextdefsym=f[3], iundefsym=f[4], nundefsym=f[5])
        elif cmd in (0x22, 0x80000022):
            f = struct.unpack_from('<10I', data, off + 8)
            lc.update(export_off=f[8], export_size=f[9])
            if f[9]:
                trie = (f[8], f[9])
        elif cmd in (0x80000033, 0x1d, 0x26, 0x29, 0x80000034, 0x2b, 0x2e):
            lc['dataoff'], lc['datasize'] = struct.unpack_from('<II', data, off + 8)
            if cmd == 0x80000033:
                trie = (lc['dataoff'], lc['datasize'])
            if cmd == 0x1d:
                info['code_signature'] = code_signature(data, lc['dataoff'], lc['datasize'])
        elif cmd == 0x2a:
            v = struct.unpack_from('<Q', data, off + 8)[0]
            lc['version'] = '.'.join(str(x) for x in (v >> 40, (v >> 30) & 0x3ff, (v >> 20) & 0x3ff, (v >> 10) & 0x3ff, v & 0x3ff))
        elif cmd == 0x2d:
            n = struct.unpack_from('<I', data, off + 8)[0]
            lc['strings'] = data[off + 12:off + size].rstrip(b'\0').decode('utf-8', 'replace').split('\0')[:n]
        info['load_commands'].append(lc)
        off += size
    info['linked_dylibs'] = dylibs
    info['exports'] = export_trie(data, *trie) if trie else []
    if sym:
        defined, imports = symtab(data, sym[0], sym[1], sym[2], dylibs, is64)
        info['symtab_defined_external'] = defined
        info['symtab_imports'] = imports
    if strings_dir:
        rows = []
        for seg, sec, addr in sections:
            if sec['type'] == 2 or sec['sectname'] in ('__const', '__cfstring', '__objc_methname', '__objc_classname'):
                if sec['type'] == 2:  # S_CSTRING_LITERALS
                    raw = data[sec['offset']:sec['offset'] + sec['size']]
                    pos = 0
                    for piece in raw.split(b'\0'):
                        if piece:
                            rows.append(f"0x{sec['offset'] + pos:x}\t0x{addr + pos:x}\t{seg},{sec['sectname']}\t"
                                        + piece.decode('utf-8', 'replace').replace('\t', '\\t').replace('\n', '\\n'))
                        pos += len(piece) + 1
        with open(f'{strings_dir}/{arch}.cstrings.tsv', 'w') as fh:
            fh.write('fileoff_in_slice\tvmaddr\tsection\tvalue\n' + '\n'.join(rows) + '\n')
        info['cstring_count'] = len(rows)
    return info


def main(path, out, strings_dir=None):
    data = open(path, 'rb').read()
    result = {'path': path, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'slices': []}
    magic = struct.unpack_from('>I', data)[0]
    if magic == 0xcafebabe:
        n = struct.unpack_from('>I', data, 4)[0]
        archs = [struct.unpack_from('>IIIII', data, 8 + 20 * i) for i in range(n)]
    else:
        archs = [(struct.unpack_from('<I', data, 4)[0], 0, 0, len(data), 0)]
    for cpu, sub, offset, size, align in archs:
        body = data[offset:offset + size]
        arch = CPU.get(cpu, hex(cpu))
        info = {'arch': arch, 'offset': offset, 'size': size, 'sha256': hashlib.sha256(body).hexdigest()}
        info.update(slice_info(body, arch, strings_dir))
        result['slices'].append(info)
    with open(out, 'w') as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write('\n')


if __name__ == '__main__':
    main(*sys.argv[1:])
