"""H1 plugin-scanner static evidence extractor (analyst-only, read-only).

Usage: python3 -I h1_extract.py <helper-dir> <bundle-Contents> <out-dir>

Inputs (never modified):
  <helper-dir>/Ableton_Plugin_Scanner.arm64        arm64 slice analyzed in Ghidra
  <helper-dir>/corpus/decomp/chunks/*.jsonl        C1 bulk-decompile records
  <bundle>/App-Resources/Extensions/PluginScanner/Ableton Plugin Scanner  (universal)
  <bundle>/MacOS/Live                              (universal; strings only)
  <bundle>/App-Resources/Builtin Lessons/...       (lesson text)
Outputs in <out-dir>: options.json, tables.json, sql.json, functions.tsv,
pseudocode/<entry>.c, live-anchors.json, app-resources.json.
Depends on macho_vtables.py in the same directory for pointer decoding.
"""
import glob, hashlib, json, mmap, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import macho_vtables  # noqa: E402

BASE = 0x100000000
# Function entries read for the H1 page, with the role assigned by this packet (Inferred).
FUNCTIONS = {
    '0x1001308e0': 'main (entry): option parsing, logging setup, VST3 then VST2 scan, final scan message',
    '0x100134348': 'create TRunContext and TControlledProcessIPCChannel "plugin-scanner->live"',
    '0x10013da2c': 'IPC address: "ipc://" + temp_directory_path() + cid (or "inproc://" + cid)',
    '0x10013e06c': 'TRunContext: send "update" {total, current}',
    '0x10013e284': 'TRunContext: send "current-plugin" {name}',
    '0x10013df70': 'TRunContext: channel-alive flag',
    '0x10013df84': 'TRunContext: throttled orphan check',
    '0x1001806e4': 'orphan check: sysctl KERN_PROC_PID, parent pid == 1',
    '0x10013f4fc': 'TLiveProcessWatchDog lambda: clear channel-alive flag',
    '0x100149888': 'helper watchdog shutdown reasons (shared helper code)',
    '0x100148ce0': 'helper watchdog state constructor (constants 0x1009a8ff0)',
    '0x100133aa0': 'VST3 scan driver: TScannerAdapter("VST3", limit) + module load adapter',
    '0x100134018': 'VST2 scan driver: TScannerAdapter("VST2", limit) + module load adapter',
    '0x100133b9c': '--reset matcher: value == "all" or == format name',
    '0x1001332fc': '--vst2/--vst3 value parser: comma list of ID=PATH',
    '0x100137810': 'split once at "="',
    '0x100138504': 'TScannerAdapter run state: 0 continue, 1 stop, 2 limit reached',
    '0x100138578': 'TScannerAdapter: count loaded module',
    '0x100138588': 'TScannerAdapter: report current plugin "<format>: <name>[ [x]]"',
    '0x1005e9fd8': 'SScanVst3PluginPaths (role from mangled-name string, Inferred)',
    '0x1005e8cb4': 'VST3 candidate enumeration: recursive walk, ".vst3", canonical-path dedup',
    '0x1005e91fc': 'VST3 module check and plugin confirmation',
    '0x100145768': 'VST3 subcategory "Instrument" test',
    '0x1005aca28': 'SScanVst2PluginPaths (Inferred)',
    '0x1005aad10': 'VST2 candidate enumeration: breadth-first folder walk, ".vst" bundles, relpath',
    '0x1005aba10': 'VST2 module check and plugin confirmation',
    '0x100145d24': 'VST2 bundle load: code-signature check, main_macho/VSTPluginMain',
    '0x10075325c': 'SecStaticCodeCreateWithPath + SecStaticCodeCheckValidity(flags 9)',
    '0x10014094c': 'VST2 load error-code messages',
    '0x100140cb8': 'VST2 host callback: version 2400, vendor "Ableton", product "Live", shellCategory, language',
    '0x100146ae4': 'VST3 bundle load: bundleEntry/GetPluginFactory/bundleExit',
    '0x1001458a4': 'module fingerprint: hex(size):hex(mtime) of bundle executable',
    '0x100138a34': 'VST3 module load adapter: fingerprint slot (calls 0x1001458a4)',
    '0x1001384a8': 'VST2 module load adapter: fingerprint slot (calls 0x1001458a4)',
    '0x100138340': 'VST2 module load adapter: load slot (calls 0x100145d24)',
    '0x1001387c4': 'VST3 module load adapter: load slot',
    '0x1006c06a0': 'stat st_size',
    '0x1006c0a04': 'stat st_mtimespec.tv_sec',
    '0x1005a4318': 'TPluginScanDatabase::AddModuleCandidate (vtable slot +0x18)',
    '0x1005a55c8': 'TPluginScanDatabase::PrepareModuleForRescan (+0x20)',
    '0x1005a8258': 'TPluginScanDatabase::UpdateUnconfirmedPluginsAndModulesState (+0x48)',
    '0x1005a87f0': 'TPluginScanDatabase::ResetScanData (+0x50)',
    '0x1005a8e20': 'TPluginScanDatabase::ModulesScanData (+0x58)',
    '0x1005a9534': 'TPluginScanDatabase::RemoveModules (+0x60)',
    '0x1005d235c': 'module scan-data row constructor (field layout)',
    '0x1005a2b84': 'default database path: <folder>/Live-plugins-{}.db formatted with 1',
    '0x1005a717c': 'CSV dump of plugin tables to PluginScanDb.txt (no caller found)',
    '0x10059b7a8': 'scan-state name table lookup',
    '0x10059b7d0': 'processor mask to "x86_64"/"arm64"',
    '0x1005aa7cc': 'current processor constant 2',
    '0x10019a9d8': 'parse PluginScanner.txt as a config file',
    '0x10069f714': 'logging options log.level, log.categories',
    '0x100249fac': 'plugin-table schema (oldest CREATE)',
    '0x10024a1b4': 'plugin-table migration: add processor, clear tables',
}
TABLES = {'architecture_names': 0x100b6eb50, 'scan_state_names': 0x100b6eb70}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def nul_strings(buf):
    return [s.decode('latin1') for s in buf.split(b'\0') if s]


def slices(path):
    b = open(path, 'rb').read(8 + 20 * 4)
    n = struct.unpack('>I', b[4:8])[0]
    out = []
    for k in range(n):
        ct, _, off, size, _ = struct.unpack('>iiIII', b[8 + 20 * k:28 + 20 * k])
        out.append({'cputype': hex(ct & 0xffffffff), 'offset': off, 'size': size})
    return out


def options(scanner):
    raw = open(scanner, 'rb').read()
    res = []
    for s in slices(scanner):
        body = raw[s['offset']:s['offset'] + s['size']]
        i = body.find(b'PluginScanner options')
        res.append({'slice': s, 'slice_sha256': hashlib.sha256(body).hexdigest(),
                    'anchor_slice_offset': hex(i),
                    'strings': nul_strings(body[i - 40:i + 640])})
    return res


def tables(arm64):
    b = open(arm64, 'rb').read()
    ptr, cstr, _ = macho_vtables.reader(b)
    out = {name: {'address': hex(va), 'values': [cstr(ptr(va + 8 * i)) for i in range(n)]}
           for (name, va), n in zip(TABLES.items(), (4, 5))}
    o = 0x1009a8ff0 - BASE
    out['watchdog_u32_0x1009a8ff0'] = list(struct.unpack('<6I', b[o:o + 24]))
    o = 0x1009a8748 - BASE
    out['ipc_transport_init_0x1009a8748'] = list(struct.unpack('<2I', b[o:o + 8]))
    return out


def sql(arm64):
    b = open(arm64, 'rb').read()
    pat = re.compile(rb'(?:CREATE|ALTER|INSERT|UPDATE|DELETE|SELECT|DROP)[^\0]{0,1200}?'
                     rb'(?:plugin_modules|plugin_domains|plugins)[^\0]*')
    seen, out = set(), []
    for m in pat.finditer(b):
        s = m.group().decode('latin1')
        if s not in seen and m.start() < 0xb00000:
            seen.add(s)
            out.append({'address': hex(BASE + m.start()), 'sql': re.sub(r'\s+', ' ', s)})
    return out


def functions(helper, outdir):
    rows, pdir = [], os.path.join(outdir, 'pseudocode')
    os.makedirs(pdir, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(helper, 'corpus/decomp/chunks/*.jsonl'))):
        for line in open(f):
            r = json.loads(line)
            if r['entry'] in FUNCTIONS:
                if r.get('code'):
                    open(os.path.join(pdir, r['entry'] + '.c'), 'w').write(r['code'])
                rows.append((r['entry'], r['state'], r.get('code_sha256') or '', os.path.basename(f),
                             FUNCTIONS[r['entry']]))
    rows.sort()
    with open(os.path.join(outdir, 'functions.tsv'), 'w') as fh:
        fh.write('entry\tstate\tcode_sha256\tchunk\trole (Inferred)\n')
        for r in rows:
            fh.write('\t'.join(r) + '\n')
    missing = sorted(set(FUNCTIONS) - {r[0] for r in rows})
    if missing:
        raise SystemExit(f'functions missing from corpus: {missing}')


def live_anchors(live):
    f = open(live, 'rb')
    b = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    sl = slices(live)
    out = []
    for key in [b'--cid\0', b'VstUseSystemFolders\0', b'/Library/Audio/Plug-Ins/VST3\0',
                b'Use VST2 Plug-In System Folders\0']:
        i = -1
        while (i := b.find(key, i + 1)) >= 0:
            s = next(x for x in sl if x['offset'] <= i < x['offset'] + x['size'])
            out.append({'key': key.rstrip(b'\0').decode(), 'file_offset': hex(i), 'slice': s['cputype'],
                        'slice_offset': hex(i - s['offset']),
                        'neighbors': [x for x in nul_strings(b[i - 500:i + 300]) if len(x) > 1]})
    return {'path': live, 'sha256': sha(live), 'slices': sl, 'anchors': out}


def app_resources(contents):
    root = os.path.join(contents, 'App-Resources/Builtin Lessons')
    pat = re.compile(r'plug-?in|VST|Audio Unit', re.I)
    out = []
    for p in sorted(glob.glob(root + '/**/LessonsEN.txt', recursive=True)):
        lines = [(n, l.rstrip('\n')) for n, l in enumerate(open(p, encoding='utf-8', errors='replace'), 1)
                 if pat.search(l)]
        if lines:
            out.append({'file': os.path.relpath(p, contents), 'sha256': sha(p),
                        'lines': [{'line': n, 'text': t} for n, t in lines]})
    return out


def main():
    helper, contents, outdir = sys.argv[1:4]
    arm64 = os.path.join(helper, 'Ableton_Plugin_Scanner.arm64')
    scanner = os.path.join(contents, 'App-Resources/Extensions/PluginScanner/Ableton Plugin Scanner')
    dump = lambda name, obj: json.dump(obj, open(os.path.join(outdir, name), 'w'), indent=1)
    dump('options.json', {'scanner': scanner, 'scanner_sha256': sha(scanner), 'slices': options(scanner)})
    dump('tables.json', {'arm64_slice_sha256': sha(arm64), **tables(arm64)})
    dump('sql.json', sql(arm64))
    functions(helper, outdir)
    dump('live-anchors.json', live_anchors(os.path.join(contents, 'MacOS/Live')))
    dump('app-resources.json', app_resources(contents))


if __name__ == '__main__':
    main()
