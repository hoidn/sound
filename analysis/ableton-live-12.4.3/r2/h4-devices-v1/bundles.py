"""H4 static: identity and linker-visible interface of the seven device bundles.

Usage: python3 -I bundles.py <Devices/Mac dir> <out dir>
Reads each <X>.bundle/Contents/{Info.plist, MacOS/<exe>, _CodeSignature/CodeResources}; never executes them.
Writes out/bundles.json (identity, slices, load commands, exports, imports, code-signature identity)
and out/bundle_strings.jsonl (every __TEXT,__cstring string of each arm64 slice, with vmaddr).
Depends on: Python stdlib, GNU c++filt (demangling only; mangled names are kept too).
"""
import hashlib, json, os, plistlib, struct, subprocess, sys

CPU = {0x100000C: "arm64", 0x1000007: "x86_64"}
FILETYPE = {6: "MH_DYLIB", 8: "MH_BUNDLE"}
LC_NAMES = {0x19: "LC_SEGMENT_64", 0x2: "LC_SYMTAB", 0xB: "LC_DYSYMTAB", 0xC: "LC_LOAD_DYLIB", 0xD: "LC_ID_DYLIB",
            0x1B: "LC_UUID", 0x32: "LC_BUILD_VERSION", 0x2A: "LC_SOURCE_VERSION", 0x26: "LC_FUNCTION_STARTS",
            0x29: "LC_DATA_IN_CODE", 0x1D: "LC_CODE_SIGNATURE", 0x80000022: "LC_DYLD_INFO_ONLY",
            0x80000033: "LC_DYLD_EXPORTS_TRIE", 0x80000034: "LC_DYLD_CHAINED_FIXUPS", 0x24: "LC_VERSION_MIN_MACOSX",
            0x80000018: "LC_LOAD_WEAK_DYLIB", 0x8000001C: "LC_RPATH"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def uleb(d, i):
    r = s = 0
    while True:
        b = d[i]; i += 1
        r |= (b & 0x7F) << s; s += 7
        if b < 0x80:
            return r, i


def cstr(d, i):
    j = d.index(b"\0", i)
    return d[i:j].decode("utf-8", "replace"), j + 1


def trie(d, base, size):
    out, stack = [], [(0, "")]
    while stack:
        off, prefix = stack.pop()
        i = base + off
        term, i = uleb(d, i)
        if term:
            j = i
            flags, j = uleb(d, j)
            addr, j = uleb(d, j)
            out.append({"name": prefix, "flags": flags, "offset": addr})
            i += term
        n = d[i]; i += 1
        for _ in range(n):
            edge, i = cstr(d, i)
            child, i = uleb(d, i)
            stack.append((child, prefix + edge))
    return sorted(out, key=lambda e: e["name"])


def ver(v):
    return f"{v >> 16}.{(v >> 8) & 0xFF}.{v & 0xFF}"


def codesig(d, off, size):
    blob = d[off:off + size]
    magic, length, count = struct.unpack_from(">3I", blob)
    res = {"superblob_magic": hex(magic), "blobs": []}
    for k in range(count):
        typ, bo = struct.unpack_from(">2I", blob, 12 + 8 * k)
        bm, bl = struct.unpack_from(">2I", blob, bo)
        entry = {"type": typ, "magic": hex(bm), "length": bl}
        if bm == 0xFADE0C02:  # CodeDirectory
            v, flags, hoff, ioff, nspecial, ncode, limit, hsize, htype, plat, pshift = struct.unpack_from(">7I4B", blob, bo + 8)
            entry.update(version=hex(v), flags=hex(flags), identifier=cstr(blob, bo + ioff)[0], hash_type=htype,
                         n_code_slots=ncode, code_limit=limit)
            if v >= 0x20200:
                toff = struct.unpack_from(">I", blob, bo + 48)[0]
                entry["team_id"] = cstr(blob, bo + toff)[0] if toff else None
        res["blobs"].append(entry)
    return res


def macho(d):
    magic, cpu, sub, ft, ncmds, sizeofcmds, flags, _ = struct.unpack_from("<8I", d)
    assert magic == 0xFEEDFACF, hex(magic)
    r = {"cpu": CPU.get(cpu, hex(cpu)), "filetype": FILETYPE.get(ft, ft), "flags": hex(flags), "load_commands": [],
         "dylibs": [], "segments": {}, "exports": [], "symtab_external_defined": [], "imports": []}
    sections, off, symtab = {}, 32, None
    for _ in range(ncmds):
        cmd, cs = struct.unpack_from("<2I", d, off)
        r["load_commands"].append(LC_NAMES.get(cmd, hex(cmd)))
        if cmd == 0x19:
            seg = d[off + 8:off + 24].rstrip(b"\0").decode()
            vmaddr, vmsize, fileoff, filesize, _, _, nsect, _ = struct.unpack_from("<4Q4I", d, off + 24)
            r["segments"][seg] = {"vmaddr": hex(vmaddr), "vmsize": vmsize, "sections": []}
            for k in range(nsect):
                so = off + 72 + 80 * k
                sname = d[so:so + 16].rstrip(b"\0").decode()
                addr, size, foff = struct.unpack_from("<2QI", d, so + 32)
                sections[(seg, sname)] = (addr, size, foff)
                r["segments"][seg]["sections"].append({"name": sname, "addr": hex(addr), "size": size, "offset": foff})
        elif cmd in (0xC, 0xD, 0x80000018):
            so, _, cur, compat = struct.unpack_from("<4I", d, off + 8)
            item = {"name": cstr(d, off + so)[0], "current": ver(cur), "compat": ver(compat)}
            if cmd == 0xD:
                r["id_dylib"] = item
            else:
                r["dylibs"].append(item)
        elif cmd == 0x1B:
            r["uuid"] = d[off + 8:off + 24].hex()
        elif cmd == 0x32:
            plat, minos, sdk, ntools = struct.unpack_from("<4I", d, off + 8)
            r["build_version"] = {"platform": plat, "minos": ver(minos), "sdk": ver(sdk)}
        elif cmd == 0x2A:
            v = struct.unpack_from("<Q", d, off + 8)[0]
            r["source_version"] = ".".join(str(x) for x in (v >> 40, (v >> 30) & 0x3FF, (v >> 20) & 0x3FF, (v >> 10) & 0x3FF, v & 0x3FF))
        elif cmd == 0x2:
            symtab = struct.unpack_from("<4I", d, off + 8)
        elif cmd == 0x80000022:
            eo, es = struct.unpack_from("<2I", d, off + 40)
            r["exports"] = trie(d, eo, es) if es else []
        elif cmd == 0x80000033:
            eo, es = struct.unpack_from("<2I", d, off + 8)
            r["exports"] = trie(d, eo, es) if es else []
        elif cmd == 0x1D:
            so, ss = struct.unpack_from("<2I", d, off + 8)
            r["code_signature"] = codesig(d, so, ss)
        off += cs
    if symtab:
        symoff, nsyms, stroff, _ = symtab
        r["nsyms"] = nsyms
        for k in range(nsyms):
            strx, typ, sect, desc, val = struct.unpack_from("<IBBHQ", d, symoff + 16 * k)
            if typ & 0xE0:
                continue  # debugging stab
            name = cstr(d, stroff + strx)[0]
            if typ & 0x01 and (typ & 0x0E) == 0x0E:
                r["symtab_external_defined"].append({"name": name, "value": hex(val), "private_extern": bool(typ & 0x10)})
            elif (typ & 0x0E) == 0 and typ & 0x01:
                r["imports"].append(name)
    r["imports"].sort()
    cs = sections.get(("__TEXT", "__cstring"))
    strings = []
    if cs:
        addr, size, foff = cs
        blob, i = d[foff:foff + size], 0
        while i < len(blob):
            j = blob.index(b"\0", i)
            if j > i:
                strings.append({"vmaddr": hex(addr + i), "value": blob[i:j].decode("utf-8", "replace")})
            i = j + 1
    return r, strings


def demangle(names):
    if not names:
        return {}
    out = subprocess.run(["c++filt", "-_"], input="\n".join(names), capture_output=True, text=True, check=True).stdout
    return dict(zip(names, out.split("\n")))


def main(root, outdir):
    bundles, strings_out = [], []
    for b in sorted(x for x in os.listdir(root) if x.endswith(".bundle") and not x.startswith("._")):
        c = os.path.join(root, b, "Contents")
        raw_plist = open(os.path.join(c, "Info.plist"), "rb").read()
        try:
            plist = plistlib.loads(raw_plist)
        except Exception as e:  # leading whitespace before DOCTYPE is reported, not hidden
            plist = plistlib.loads(raw_plist.lstrip())
            plist["_parse_note"] = f"strict parse failed ({type(e).__name__}); parsed after stripping leading whitespace"
        exe = os.path.join(c, "MacOS", plist["CFBundleExecutable"])
        data = open(exe, "rb").read()
        cr = os.path.join(c, "_CodeSignature", "CodeResources")
        crp = plistlib.loads(open(cr, "rb").read())
        entry = {"bundle": b, "info_plist": {"sha256": sha(raw_plist), "keys": plist},
                 "code_resources": {"sha256": sha(open(cr, "rb").read()), "files": sorted(crp.get("files", {})),
                                    "files2": sorted(crp.get("files2", {}))},
                 "executable": {"path": os.path.relpath(exe, root), "size": len(data), "sha256": sha(data)}, "slices": []}
        magic = struct.unpack_from(">I", data)[0]
        assert magic == 0xCAFEBABE, (b, hex(magic))
        n = struct.unpack_from(">I", data, 4)[0]
        for k in range(n):
            cpu, _, off, size, align = struct.unpack_from(">5I", data, 8 + 20 * k)
            body = data[off:off + size]
            info, strs = macho(body)
            names = [e["name"] for e in info["exports"]] + [e["name"] for e in info["symtab_external_defined"]]
            dm = demangle(sorted(set(names)))
            for e in info["exports"] + info["symtab_external_defined"]:
                e["demangled"] = dm.get(e["name"], e["name"])
            info.update(slice_offset=off, slice_size=size, slice_sha256=sha(body), string_count=len(strs))
            entry["slices"].append(info)
            if info["cpu"] == "arm64":
                strings_out += [{"bundle": b, **s} for s in strs]
        bundles.append(entry)
    json.dump(bundles, open(os.path.join(outdir, "bundles.json"), "w"), indent=1, sort_keys=True)
    with open(os.path.join(outdir, "bundle_strings.jsonl"), "w") as f:
        for s in strings_out:
            f.write(json.dumps(s, sort_keys=True) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:3])
