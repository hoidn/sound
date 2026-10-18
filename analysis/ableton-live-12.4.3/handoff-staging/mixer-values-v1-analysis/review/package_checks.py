# Reviewer check (analyst-side; not payload): hashes, inventory, links, fixture form and a sanitization
# scan of an exported mixer-values-v1 copy, written independently of build_mv1.py.
# usage: python3 -I package_checks.py <package dir>
import hashlib, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
d = Path(sys.argv[1])
man = json.loads((d / 'manifest.json').read_text())
listed = {f['path']: f for f in man['files']}
actual = sorted(str(p.relative_to(d)) for p in d.rglob('*') if p.is_file() and p.name != 'manifest.json')
print('inventory equal:', sorted(listed) == actual, len(actual), '+ manifest')
print('hash/size mismatches:', [p for p, f in listed.items() if hashlib.sha256((d / p).read_bytes()).hexdigest() != f['sha256'] or (d / p).stat().st_size != f['bytes']])
print('symlinks:', [str(p) for p in d.rglob('*') if p.is_symlink()])
print('manifest:', man['release_status'], man['release_date'], man['review']['status'], man['review']['record'], 'case_count', man['case_count'])
# links
def slug(h): return re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-')
for md in sorted(d.glob('*.md')):
    for t in re.findall(r'\]\(([^)\s]+)\)', md.read_text()):
        path, _, anchor = t.partition('#'); dest = (md.parent / path).resolve() if path else md
        ok = not re.match(r'[a-z]+:', t) and dest.is_file() and d.resolve() in dest.parents
        if ok and anchor: ok = anchor in {slug(h) for h in re.findall(r'^#+ (.+)$', dest.read_text(), re.M)}
        if not ok: print('UNRESOLVED', md.name, t)
print('links checked in', [p.name for p in d.glob('*.md')])
# fixtures
cases = json.loads((d / 'cases.json').read_text())['cases']
raws = [(d / c['input']).read_bytes() for c in cases]
print('fixtures:', len(raws), 'distinct', len(set(raws)), 'ascii/LF/no-tab/final-newline',
      all(r.isascii() and b'\r' not in r and b'\t' not in r and r.endswith(b'\n') for r in raws),
      'well-formed', all(ET.fromstring(r) is not None for r in raws))
print('statuses:', {c['reference_execution'] for c in cases}, {c['candidate_execution'] for c in cases}, {c['expectation_provenance'] for c in cases},
      json.loads((d / 'cases.json').read_text())['status'])
# sanitization: reviewer's own deny-list (internal names, addresses, analyst vocabulary, shipped names, paths)
DENY = r'''0x[0-9a-f]{3,}|\+0x|FUN_|DAT_|PTR_|thunk|vtable|dossier|corpus|Ghidra|pseudocode|disassembl|decompil|symbol|demangl|RTTI|
\bmp[A-Z]\w*|\bm[A-Z][a-z]+[A-Z]\w*|Timeable|Remoteable|TrackDevice|ATrack|LSong|OCrossFade|Processor|Converter|SNewCompound|LomId|
registr|constructor|singleton|formatter|text object|\bslot|log10f|exp10|printf|frinta|fcsel|strtod|libm|
Track Volume|Track Panning|Speaker On|X-Fade|Solo-Cue|Pre-Listen|Preview Volume|Left Split Stereo|Right Split Stereo|Global Groove|
NormalDip|SlightDip|Dipless|ConstantPower|PlayThrough|StereoSplitPan|
Recording Audio|Sample Reference|APC40|Driver Error|Playing Software|8-Track|Podcast|12\.4d1|12\.1d1|\.als\b|\.alc\b|
Live\.arm64|/home/|/var/|/tmp/|analysis/|wiki/|raw/|\.\./|\bPRB-|\bQ-0\d|\bMV-\d|\bMX-\d|\bS9\b|\bD8\b|\bN1\b|\bI[1-6]\b|\bF[1-9]\b|
static-survey|curves\.txt|traceab|build_mv1|derive_curves|\bB0\b|Python|CPython'''.replace('\n', '')
DENY_I = r'vtable|dossier|corpus|ghidra|pseudocode|disassembl|decompil|demangl|registr|constructor|singleton|formatter|text object|\bslot\b|libm|derivation|probe|analyst'
hits = {}
for p in [*sorted(d.rglob('*')), ]:
    if p.is_file():
        t = p.read_text()
        h = sorted(set(m.group(0) for m in re.finditer(DENY, t)) | set(m.group(0) for m in re.finditer(DENY_I, t, re.I)))
        if h: hits[str(p.relative_to(d))] = h
print('deny-list hits:', hits)
