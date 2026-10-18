"""H5 Push 3 helper: regenerate static evidence from the bundle, the helper corpus and indexes.

Reads only. Never executes or imports bundle code. Run with any CPython >= 3.10:
  python3 -I extract.py OUT_DIR
Inputs (fixed paths, see manifest.json):
  BUNDLE   Ableton Live 12 Suite.app (read-only)
  HELPER   /var/tmp/sound-analysis/helpers/Push3 (slice, corpus/decomp/chunks, corpus/indexes)
  LIVE     analysis/ableton-live-12.4.3/derived/Live.arm64 (string offsets only)
  PUSH2    analysis/ableton-live-12.4.3/r2/c-tooling-v1/push2-indexes (comparison only)
Writes: bundle.json, macho.json, imports.json, anchors.json, constants.json, flip-messages.tsv,
  namespaces.json, live-strings.json, push2-comparison.json, functions/<entry>.c, checks.txt.
The asserts at the end are the self-check: they fail if any recorded constant changes.
"""
import base64, collections, glob, hashlib, json, plistlib, re, struct, sys
from pathlib import Path

BUNDLE = Path('/home/ollie/Ableton Live 12 Suite.app/Contents')
APP = BUNDLE / 'Helpers/Push3.app/Contents'
HELPER = Path('/var/tmp/sound-analysis/helpers/Push3')
REPO = Path(__file__).resolve().parents[4]
LIVE = REPO / 'analysis/ableton-live-12.4.3/derived/Live.arm64'
PUSH2 = REPO / 'analysis/ableton-live-12.4.3/r2/c-tooling-v1/push2-indexes'

# Functions whose pseudocode is retained (entry -> role as labelled on the wiki page).
FUNCTIONS = {
    '0x1001bdfa0': 'entry: boost::program_options table, version log',
    '0x10017cfa0': 'application main: hardware search, sockets, ScriptHost, main loop',
    '0x1002867e0': 'CoreMIDI port search by kMIDIPropertyModel',
    '0x10017eabc': 'open Push MIDI output (client port name Ableton Internal Output)',
    '0x1001cbfec': 'RtMidi output open',
    '0x1013e5b58': 'libusb device enumeration, VID/PID/class match, claim interface 0',
    '0x1013ebf50': 'libusb hotplug registration',
    '0x1013eff5c': 'sync bulk OUT endpoint 0x01',
    '0x1013f0008': 'sync bulk IN endpoint 0x81',
    '0x1013f00c8': 'async bulk OUT transfer setup',
    '0x1013f0ae4': 'async bulk IN transfer setup',
    '0x1013ec2f8': 'DisplayUsbCommunication ctor (16-byte header)',
    '0x1013ec734': 'display frame cycle (header then 0x50000-byte payload)',
    '0x1013e70cc': 'USB sysinfo query',
    '0x1013ed848': 'sysinfo request constant',
    '0x1002776a4': 'UsbDisplay::getNextFrameBuffer',
    '0x100277ddc': 'UsbDisplay::transmitFrameBuffer',
    '0x10017f084': 'push-flip-api-ipc-channel socket',
    '0x100180a80': 'ipc:// + temp_directory_path + channel name',
    '0x10031ce0c': 'temp_directory_path',
    '0x100181150': 'nanomsg client open: nn_socket + nn_connect',
    '0x10022142c': 'nanomsg server open: nn_socket + nn_bind',
    '0x100a20064': 'nanomsg connect (create_ep bind=0)',
    '0x100a1fe48': 'nanomsg bind (create_ep bind=1)',
    '0x100180e34': 'nanomsg send wrapper',
    '0x100220998': 'push-to-live-midi-ipc-channel (client)',
    '0x100220f38': 'live-to-push-midi-ipc-channel (server)',
    '0x100220ad0': 'MIDI forwarding thread loop',
    '0x10022cb04': 'MIDI bytes + 8-byte value, send',
    '0x10017f52c': 'ControlledProcessSocket<Watchdog> ctor',
    '0x10017ff30': 'send sync byte to parent',
    '0x1006677a8': 'one-byte message',
    '0x1006678a0': 'Watchdog transition table',
    '0x100668c58': 'Watchdog state names',
    '0x100668d74': 'Watchdog event names',
    '0x100668448': 'Watchdog shutdown reasons',
    '0x100668408': 'Watchdog tick: kLiveStillRunning unless parent pid is gone',
    '0x10066df0c': 'kill(pid, 0) liveness check',
    '0x1013f1be0': 'real-time channel client id',
    '0x1013f1ca4': 'real-time channel shared memory open',
    '0x1001ccc6c': 'Live browser database path',
    '0x10063e970': '{}-files-{}.db',
    '0x1002ad94c': 'service discovery multicast endpoint',
    '0x1002313d8': 'ScriptHost embedded module names',
    '0x100230ab8': 'LiveFlip application root',
    '0x1001b015c': 'update channel names',
}
STRING_RX = re.compile(
    r'(?i)push|ipc|flip|nanomsg: socket|watchdog|shutting down|sync signal|usb|display|firmware|sysinfo|'
    r'hardware|update|224\.76|service discovery|shared memory|client id|Ableton Internal|RtMidi|port search|'
    r'Live Database|-files-|log-file|log-level|parent-process|screenshot|faceless|no-parent|python-log|'
    r'webservice|crashpad|language|LiveFlip|create_instance|BrowserBackend|UsbInterface|WifiConnector|'
    r'SoftwareUpdater|MidiRemoteScript|kLaunched|kWaitFor|kSend|kRunning|kShutdown|kDefunct|kAck|kUsb|'
    r'kProcess|kLive|kReceiver|e3d8be4d07|12\.4\.3|Live\.0\.0')
LIVE_STRINGS = [b'push-flip-api-ipc-channel', b'push-to-live-midi-ipc-channel', b'live-to-push-midi-ipc-channel',
                b'--parent-process-id=', b'--faceless', b'--python-log-filters=', b'--log-level=',
                b'--dont-log-to-console', b'--show-developer-window', b'--emulator-device=ah05',
                b'push-app-launching', b'FlipMessageStreamSocket send error', b'Live.0.0.316', b'--crashpad-fd',
                b'--push2-parent-process-id=', b'--push2-ipc-channel', b'push2ipc-',
                b'Push2/Push2DisplayProcess.app/Contents/MacOS/Push2DisplayProcess']


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def macho(b):
    ncmds = struct.unpack_from('<I', b, 16)[0]; off = 32; segs, cmds = [], []
    for _ in range(ncmds):
        cmd, sz = struct.unpack_from('<II', b, off)
        if cmd == 0x19:
            name = b[off + 8:off + 24].rstrip(b'\0').decode(); va, vs, fo, fs = struct.unpack_from('<QQQQ', b, off + 24)
            segs.append((name, va, vs, fo, fs)); cmds.append(f'SEGMENT_64 {name} vm={va:#x}+{vs:#x} file={fo:#x}+{fs:#x}')
        elif cmd in (0xc, 0x8000001c):
            so = struct.unpack_from('<I', b, off + 8)[0]
            cmds.append(('LOAD_DYLIB ' if cmd == 0xc else 'RPATH ') + b[off + so:off + sz].split(b'\0')[0].decode())
        elif cmd == 0x80000028:
            cmds.append(f'MAIN entryoff={struct.unpack_from("<Q", b, off + 8)[0]:#x}')
        elif cmd == 0x1b:
            cmds.append('UUID ' + b[off + 8:off + 24].hex())
        elif cmd == 0x32:
            p, mn, sdk = struct.unpack_from('<III', b, off + 8); v = lambda x: f'{x >> 16}.{(x >> 8) & 255}.{x & 255}'
            cmds.append(f'BUILD_VERSION platform={p} minos={v(mn)} sdk={v(sdk)}')
        off += sz
    return segs, cmds


def read_va(b, segs, va, n):
    for _, sva, _, fo, fs in segs:
        if sva <= va < sva + fs:
            return b[fo + va - sva:fo + va - sva + n]
    raise ValueError(hex(va))


def cdhashes(path):
    b = Path(path).read_bytes(); out = {}
    n = struct.unpack_from('>I', b, 4)[0]
    for i in range(n):
        cpu, _, off, size, _ = struct.unpack_from('>iiIII', b, 8 + 20 * i); s = b[off:off + size]
        o = 32
        for _ in range(struct.unpack_from('<I', s, 16)[0]):
            cmd, sz = struct.unpack_from('<II', s, o)
            if cmd == 0x1d:
                doff, dsz = struct.unpack_from('<II', s, o + 8); sb = s[doff:doff + dsz]
                for j in range(struct.unpack_from('>I', sb, 8)[0]):
                    typ, bo = struct.unpack_from('>II', sb, 12 + 8 * j)
                    if typ == 0 and struct.unpack_from('>I', sb, bo)[0] == 0xfade0c02:
                        cd = sb[bo:bo + struct.unpack_from('>I', sb, bo + 4)[0]]
                        out[{0x1000007: 'x86_64', 0x100000c: 'arm64'}[cpu]] = base64.b64encode(hashlib.sha256(cd).digest()[:20]).decode()
            o += sz
    return out


def bundle_info():
    files = [p for p in APP.rglob('*') if p.is_file() and not p.name.startswith('._')]
    ext = collections.Counter(p.suffix or p.name for p in files)
    key = ['Info.plist', 'PkgInfo', 'MacOS/Push3', 'Frameworks/libusb-1.0.dylib', '_CodeSignature/CodeResources']
    key += sorted(str(p.relative_to(APP)) for p in (APP / 'Resources/python/Push2/firmware').rglob('*') if p.is_file() and not p.name.startswith('._'))
    outer = (BUNDLE / '_CodeSignature/CodeResources').read_text(errors='replace')
    m = re.search(r'<key>Helpers/Push3.app</key>\s*<dict>\s*<key>cdhash</key>\s*<data>\s*(\S+)\s*</data>\s*<key>requirement</key>\s*<string>([^<]+)', outer)
    helper_py = sorted(p.name for p in (APP / 'Resources/python/Push2').iterdir() if not p.name.startswith('._'))
    live_py = sorted(p.name for p in (BUNDLE / 'App-Resources/MIDI Remote Scripts/Push2').iterdir() if not p.name.startswith('._'))
    p2 = plistlib.loads((BUNDLE / 'Push2/Push2DisplayProcess.app/Contents/Info.plist').read_bytes())
    return {
        'info_plist': plistlib.loads((APP / 'Info.plist').read_bytes()),
        'file_count': len(files), 'by_extension': dict(ext.most_common()),
        'top_dirs': sorted(str(p.relative_to(APP)) for p in APP.glob('*/*') if p.is_dir()),
        'python_packages': sorted(str(p.relative_to(APP)) for p in (APP / 'Resources/python').iterdir() if not p.name.startswith('._')),
        'site_packages': sorted(p.name for p in (APP / 'Resources/python3_dist/site-packages').iterdir() if not p.name.startswith('._')),
        'sha256': {k: sha(APP / k) for k in key}, 'bytes': {k: (APP / k).stat().st_size for k in key},
        'cdhash_slices': cdhashes(APP / 'MacOS/Push3'),
        'outer_code_resources_entry': {'cdhash': m.group(1), 'requirement': m.group(2)} if m else None,
        'push2_package_vs_live_midi_remote_script': {
            'helper_entries': len(helper_py), 'live_entries': len(live_py),
            'common_names': len(set(helper_py) & set(live_py)),
            'common_byte_identical': sum((APP / 'Resources/python/Push2' / n).read_bytes() == (BUNDLE / 'App-Resources/MIDI Remote Scripts/Push2' / n).read_bytes()
                                         for n in set(helper_py) & set(live_py) if n.endswith('.pyc')),
            'only_live': sorted(set(live_py) - set(helper_py))},
        'push2_display_process_info_plist': {k: p2.get(k) for k in ('CFBundleIdentifier', 'CFBundleExecutable', 'LSBackgroundOnly', 'CFBundleShortVersionString')},
        'push2_display_process_qml_files': sum(1 for p in (BUNDLE / 'Push2/Push2DisplayProcess.app').rglob('*.qml') if not p.name.startswith('._')),
    }


def strings_index(path):
    for line in open(path):
        yield json.loads(line)


def main(out):
    out = Path(out); (out / 'functions').mkdir(parents=True, exist_ok=True)
    slice_meta = json.loads((HELPER / 'slice.json').read_text())
    b = (HELPER / 'Push3.arm64').read_bytes()
    assert hashlib.sha256(b).hexdigest() == slice_meta['slice_sha256']
    segs, cmds = macho(b)
    w = lambda name, obj: (out / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + '\n')
    w('bundle.json', bundle_info())
    w('macho.json', {'slice': slice_meta, 'load_commands': cmds})

    idx = HELPER / 'corpus/indexes'
    imports = collections.defaultdict(list)
    for d in strings_index(idx / 'aliases.jsonl'):
        if d['external']:
            imports[d['library'] or '?'].append(d['name'].split('::')[-1])
    p2imports = collections.Counter(d['library'] for d in strings_index(PUSH2 / 'aliases.jsonl') if d['external'])
    w('imports.json', {'push3': {k: sorted(v) for k, v in sorted(imports.items())}, 'push2_display_process_counts': dict(p2imports)})

    anchors, flip, ns = [], {}, collections.Counter()
    for d in strings_index(idx / 'strings.jsonl'):
        v = d['value']
        for m in re.finditer(r'15push_live_model(\d+)', v):
            n = int(m.group(1)); cls = v[m.end():m.end() + n]; m2 = re.match(r'(\d+)Message_', v[m.end() + n:])
            if m2:
                k = int(m2.group(1)); flip.setdefault((cls, v[m.end() + n + len(m2.group(1)):][:k][8:]), d['address'])
        for m in re.finditer(r'7ableton(\d+)', v):
            ns[v[m.end():m.end() + int(m.group(1))]] += 1
        if d['refs'] and STRING_RX.search(v) and not re.match(r'_*Z|N\d|NSt|N5boost|P?F', v) and len(v) < 400:
            anchors.append({'address': d['address'], 'value': v, 'functions': sorted({r.get('function') or r['from'] for r in d['refs']})[:8]})
    w('anchors.json', anchors)
    w('namespaces.json', dict(ns.most_common()))
    (out / 'flip-messages.tsv').write_text('class\tmessage\tstring_address\n' + ''.join(f'{c}\t{m}\t{a}\n' for (c, m), a in sorted(flip.items())))

    rv = lambda va, n: read_va(b, segs, va, n)
    timeouts = struct.unpack('<6I', rv(0x1015c09a0, 24))
    vt = lambda va: {hex(i * 8): hex(struct.unpack_from('<Q', rv(va, 80), i * 8)[0]) for i in range(10)}
    consts = {
        'display_header@0x101809960': rv(0x101809960, 16).hex(' '),
        'sysinfo_request (FUN_1013ed848 returns 0xa1313f8f8, sent as 16 bytes)': struct.pack('<QQ', 0xa1313f8f8, 0).hex(' '),
        'watchdog_timeouts_u32@0x1015c09a0': timeouts,
        'nanomsg_protocol_and_fd@0x101570410': struct.unpack('<Ii', rv(0x101570410, 8)),
        'vtable_client_socket@0x101bcf110': vt(0x101bcf110),
        'vtable_server_socket@0x101bd4098': vt(0x101bd4098),
        'vtable_controlled_process_socket@0x101bcee60': vt(0x101bcee60),
    }
    w('constants.json', consts)

    want, found = set(FUNCTIONS), {}
    for p in sorted(glob.glob(str(HELPER / 'corpus/decomp/chunks/chunk-*.jsonl'))):
        for line in open(p):
            d = json.loads(line)
            if d['entry'] in want:
                found[d['entry']] = d
                (out / 'functions' / f"{d['entry']}.c").write_text(
                    f"// {d['entry']} {d['name']} state={d['state']} role={FUNCTIONS[d['entry']]}\n// source chunk {Path(p).name}; code_sha256={d.get('code_sha256')}\n" + (d['code'] or ''))
    lb = LIVE.read_bytes()
    w('live-strings.json', {'file': str(LIVE.relative_to(REPO)), 'sha256': hashlib.sha256(lb).hexdigest(),
                            'note': 'file offsets in the thin arm64 slice; presence only, no references traced',
                            'offsets': {s.decode(): [hex(m.start()) for m in re.finditer(re.escape(s), lb)][:4] for s in LIVE_STRINGS}})
    p2 = [{'address': d['address'], 'value': d['value']} for d in strings_index(PUSH2 / 'strings.jsonl')
          if d['refs'] and re.search(r'(?i)ipc|push2-|Push2DisplayProcess|qml$|IPC', d['value']) and len(d['value']) < 200 and not re.match(r'_*Z|N\d|NSt', d['value'])]
    w('push2-comparison.json', p2)

    checks = [
        ('slice sha256', slice_meta['slice_sha256'] == '8a2b77c9d5b381ec175d8250b6c0035adc07114e4f13563195a72902c079b7ec'),
        ('display header ff cc aa 88 + 12 zero bytes', rv(0x101809960, 16) == bytes.fromhex('ffccaa88') + bytes(12)),
        ('watchdog timeouts', timeouts == (5000, 20000, 20000, 1000, 2000, 4000)),
        ('nanomsg protocol value 16, fd -1', struct.unpack('<Ii', rv(0x101570410, 8)) == (16, -1)),
        ('client vtable slot 0x38 -> FUN_100181150', consts['vtable_client_socket@0x101bcf110']['0x38'] == '0x100181150'),
        ('server vtable slot 0x38 -> FUN_10022142c', consts['vtable_server_socket@0x101bd4098']['0x38'] == '0x10022142c'),
        ('all retained functions found', want == set(found)),
        ('outer seal cdhash == x86_64 slice cdhash', json.loads((out / 'bundle.json').read_text())['outer_code_resources_entry']['cdhash'] == cdhashes(APP / 'MacOS/Push3')['x86_64']),
        ('VID/PID in device match', all(s in found['0x1013e5b58']['code'] for s in ('0x2982', '0x1967', '0x1969', '_libusb_claim_interface(local_120,0)'))),
        ('hotplug 0x2982/0x1969', '(0,1,0,0x2982,0x1969,0xffffffff' in found['0x1013ebf50']['code']),
        ('bulk endpoints', '_libusb_bulk_transfer(param_1,1,' in found['0x1013eff5c']['code'] and '_libusb_bulk_transfer(param_1,0x81,' in found['0x1013f0008']['code']),
        ('frame payload 0x50000', '(void *)0x50000' in found['0x1013ec734']['code']),
    ]
    (out / 'checks.txt').write_text(''.join(f"{'PASS' if ok else 'FAIL'} {name}\n" for name, ok in checks))
    assert all(ok for _, ok in checks), [n for n, ok in checks if not ok]
    print(f'{len(found)} functions, {len(anchors)} anchors, {len(flip)} flip messages; all checks pass')


if __name__ == '__main__':
    main(sys.argv[1])
