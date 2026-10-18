"""Constructor arguments (internal range, user converter, default, display name) for every parameter of
Analog (UltraAnalog), Tension (StringStudio) and Collision (analyst tool; output is data).

usage: python3 -I constructors.py <out-dir> <h4-out-dir> <Live.arm64> <dossier-results-dir>

Walks each device constructor and the sub-object constructors it calls, in decompiled text order (C1 Live
corpus), and records each call to a parameter set-up helper with the member slot it configures. Slots are
named with extract_nested.py's registration classes. Helper semantics (SETUP) were read from the helper
bodies (notes.md). Float arguments of every set-up call in a constructor that has a dossier are re-read
from its disassembly (s0/s1/s2 at the call) and must equal the decompiled value (asserted).
Writes <out>/constructors.tsv (one row per configured slot) and prints a summary.
Depends on: extract_nested.py (same directory), C1 corpus, dossier results n6-0001..n6-0003.
Limitation: straight-line reading; two loops over member arrays in the Analog constructor are expanded
from the stack array they index (LOOP note in notes.md).
"""
import csv, glob, importlib.util, json, os, re, struct, sys
sys.dont_write_bytecode = True  # do not leave __pycache__ in other packets' directories

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('xn', os.path.join(HERE, 'extract_nested.py'))
xn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(xn)

TOP = {'UltraAnalog': '0x1031a3acc', 'StringStudio': '0x103189a7c', 'Collision': '0x1030dc3cc'}
# sub-object constructors: name -> index of the object argument
SUBCTOR = {'FUN_1030cac68': 0, 'FUN_1030ccacc': 0, 'FUN_1030cf96c': 0, 'FUN_1030d1d80': 0, 'FUN_1030d6708': 0,
           'FUN_1031a7d8c': 0, 'FUN_1031b4554': 0}
# AUltraAnalogSignalChain{1,2} vtable +0x1f0, called by 0x1031a7d8c on itself (vtable read in notes.md)
VIRTUAL_SUBCTOR = {('FUN_1031a7d8c', 0x680): 'FUN_1031b625c', ('FUN_1031a7d8c', 0x698): 'FUN_1031b6714'}
# set-up helpers: object argument, default argument, fixed (internal lo, hi), user converter or the argument
# holding it, value class. 'linear01' etc. are the converters the helper builds itself (notes.md).
SETUP = {
    'FUN_103192720': dict(obj=2, dflt=0, rng=(0, 1), conv=('linear', 0, 1), cls='float', name=3),
    'FUN_103197830': dict(obj=2, dflt=0, rng=(0, 1), conv=('linear', 0, 1), conv_arg=7, cls='float', name=3),
    'FUN_103192974': dict(obj=2, dflt=0, rng=(-1, 1), conv=('linear', -1, 1), cls='float', name=3),
    'FUN_103197e1c': dict(obj=2, dflt=0, rng=(-1, 1), conv=('linear', -1, 1), cls='float', name=3),
    'FUN_103192a6c': dict(obj=0, dflt=None, fixed_default=0.5, rng=(-1, 1), conv=('linear', -1, 1), cls='float', name=2),
    'FUN_1030cb214': dict(obj=2, dflt=0, rng=(-5, 5), conv=('linear', -5, 5), cls='float', name=3),
    'FUN_1030cdf18': dict(obj=2, dflt=0, rng=(-2, 2), conv=('linear', -2, 2), cls='float', name=3),
    'FUN_1026f0b58': dict(obj=3, dflt=2, rng=(0, 1), conv_arg=5, cls='float', name=7),
    'FUN_10319285c': dict(obj=0, dflt=2, cls='bool', name=1),
    'FUN_1031980a4': dict(obj=0, dflt=2, cls='bool', name=1),
    'FUN_1026ef060': dict(obj=0, dflt=1, cls='enum', name=3),
    'FUN_1026ef0dc': dict(obj=0, dflt=1, cls='enum', name=4),
    'FUN_101564728': dict(obj=0, dflt=1, cls='bool', name=9),  # plain (non-Timeable) bool value: ToggleDummy
}
CONVERTERS = {'FUN_101575868': 'linear', 'FUN_101577e1c': 'legacyint', 'FUN_101578050': 'quantizing',
              'FUN_101576354': 'log10'}
FLOAT_ARGS = {'FUN_1026f0b58': 3}
INT_DEFAULT_REG = {'FUN_1026ef060': 1, 'FUN_1026ef0dc': 1, 'FUN_10319285c': 2, 'FUN_1031980a4': 2, 'FUN_101564728': 1}  # s0, s1, s2; other float helpers take s0 only
IGNORE_ON_SLOT = {'FUN_10155baa4', 'FUN_1026f96b0', 'FUN_1026f9248', 'FUN_1026efa48', 'FUN_1026fc44c',
                  'FUN_1026f1850', 'FUN_1024dd614', 'FUN_1024dd624', 'FUN_1024dd728', 'FUN_1024874ac',
                  'FUN_102953070', 'FUN_102953514', 'FUN_102953520', 'FUN_102953a9c', 'FUN_10156fa68',
                  'FUN_1025ba00c', 'FUN_10155e028', 'FUN_101567bfc', 'FUN_10150b1cc'}
NUM = r'(?:0x[0-9a-f]+|\d+)'
# Arguments computed at run time, resolved by reading the callees (notes.md): Collision LFO SyncRate uses
# FUN_1020ef18c() = 0x16 rates (internal 0..21, ALegacyQuantingInt(0, 21)) and FUN_1020ee0f4() = 4 as default.
OVERRIDES = {('0x1030ccacc', 'FUN_1026f0b58', 1): dict(internal=(0.0, 21.0), conv=('legacyint', 0.0, 21.0), default=4.0)}
NONPARAM_SETTERS = {'FUN_10156934c': 1, 'FUN_101568960': 0}  # value argument index; set a plain member's value


def f32(bits):
    return struct.unpack('<f', struct.pack('<I', bits & 0xffffffff))[0]


def num(a):
    """Decompiled float/int literal -> (bits, value); floats appear as IEEE bits, ints as small numbers."""
    a = a.strip()
    if re.fullmatch(r'-?' + NUM, a):
        v = int(a, 0) & 0xffffffff
        return v, (f32(v) if v > 0xffff else float(v))
    return None, None


def split_args(s):
    return [x.strip() for x in re.split(r',(?![^()]*\))', s)] if s.strip() else []


class Walk:
    def __init__(self, img, dossiers):
        self.img, self.dossiers, self.rows, self.other, self.fields = img, dossiers, [], [], []

    def ctor(self, fn, path, binds):
        src = xn.code(fn)
        sig = re.search(r'\w+ \*?FUN_[0-9a-f]+\(([^)]*)\)', src).group(1)
        self.scale = {p.strip().rsplit(' ', 1)[1].lstrip('*'): 8 for p in sig.split(',') if p.strip().startswith('long *')}
        ops = xn.compile_flat([s for s in xn.statements(src) if not xn.DECL.fullmatch(s)])
        labels = {op[1]: k for k, op in enumerate(ops) if op[0] == 'L'}
        env, calls, pc, steps = dict(binds), {}, 0, 0
        env['_last_new'] = None
        while pc < len(ops):
            steps += 1
            assert steps < 200000, fn
            op = ops[pc]
            pc += 1
            if op[0] == 'L':
                continue
            if op[0] == 'j':
                pc = labels[op[1]]
                continue
            if op[0] in ('jt', 'jf'):
                v = self.cond(op[1], env)
                if v == (op[0] == 'jt'):
                    pc = labels.get(op[2], len(ops))
                continue
            if op[1] == 'return;':
                break
            self.stmt(fn, op[1], env, calls)

    def cond(self, c, env):
        """Conditions on known integer arguments are evaluated; anything else (static-init guards,
        reference-count tests) is taken as true, which runs guard bodies once."""
        names = set(re.findall(r'\b[a-zA-Z_]\w*\b', c)) - {'int', 'long', 'char'}
        if names and all(env.get(n, ('',))[0] == 'const' for n in names):
            return bool(self.evalc(c, env))
        return True

    def evalc(self, e, env):
        e = re.sub(r'\((?:int|long|char|uint)\)', '', e).replace('&&', ' and ').replace('||', ' or ').replace('!', ' not ').replace(' not =', '!=')
        for n in set(re.findall(r'\b[a-zA-Z_]\w*\b', e)) - {'and', 'or', 'not'}:
            e = re.sub(rf'\b{n}\b', str(env[n][1]), e)
        return eval(e, {'__builtins__': {}})  # only integers and comparisons

    def stmt(self, fn, st, env, calls):
        m = re.fullmatch(r'(\w+) = (?:\(\w+ \*?\))?\*\((?:undefined8|long) \*\)\((\w+) \+ (' + NUM + r')\);', st)
        if m and m.group(2) in env and env[m.group(2)][0] in ('obj', 'addr'):
            env[m.group(1)] = ('obj', self.slot(env[m.group(2)], int(m.group(3), 0) * self.scale.get(m.group(2), 1)))
            return
        m = re.fullmatch(r'(\w+) = (?:\(\w+ \*?\))?(\w+)\[(' + NUM + r')\];', st)
        if m and env.get(m.group(2), ('',))[0] == 'obj':
            env[m.group(1)] = ('obj', self.slot(env[m.group(2)], int(m.group(3), 0) * 8))
            return
        m = re.fullmatch(r'(\w+) = \*\(undefined8 \*\)\(\*\(long \*\)\(\(long\)&local_([0-9a-f]+) \+ lVar\d+\) \+ 8\);', st)
        if m:  # loop over a stack array of member addresses, stride 0x10
            base, slots = int(m.group(2), 16), []
            while env.get(f'local_{base:x}', ('',))[0] == 'addr':
                slots.append(env[f'local_{base:x}'][1])
                base -= 0x10
            env[m.group(1)] = ('slots', slots)
            return
        m = re.fullmatch(r'(\w+) = (\w+) \+ (' + NUM + r');', st)
        if m and env.get(m.group(2), ('',))[0] == 'obj':
            env[m.group(1)] = ('addr', env[m.group(2)][1] + (int(m.group(3), 0) * self.scale.get(m.group(2), 1),))
            return
        m = re.fullmatch(r'(\w+) = (?:\(\w+ \*?\))?FUN_1012d9850\(' + NUM + r'\);', st)
        if m:
            env['_last_new'] = m.group(1)
            env.pop(m.group(1), None)  # a fresh heap object, not a member
            return
        m = re.fullmatch(r'(\w+) = \(int\)(\w+);', st)
        if m and env.get(m.group(2), ('',))[0] == 'const':
            env[m.group(1)] = env[m.group(2)]
            return
        m = re.fullmatch(r'(\w+) = "(.*)";', st)
        if m:
            env[m.group(1)] = ('name', m.group(2))
            return
        m = re.fullmatch(r'(\w+) = (\w+);', st)
        if m and m.group(2) in env:
            env[m.group(1)] = env[m.group(2)]
            return
        for f, args in re.findall(r'(FUN_[0-9a-f]+)\((.*?)\)(?=;|\s*$)', st):
            calls[f] = calls.get(f, 0) + 1
            self.call(fn, f, split_args(args), env, env['_last_new'], calls[f])

    @staticmethod
    def slot(base, off):
        kind, p = base
        return p + (off - 8,) if kind == 'obj' else p[:-1] + (p[-1] + off - 8,)

    def objarg(self, a, env):
        a = a.strip()
        if a in env and env[a][0] in ('obj', 'slots'):
            return [env[a][1]] if env[a][0] == 'obj' else env[a][1]
        m = re.fullmatch(r'\*\(undefined8 \*\)\((\w+) \+ (' + NUM + r')\)', a)
        if m and m.group(1) in env and env[m.group(1)][0] in ('obj', 'addr'):
            return [self.slot(env[m.group(1)], int(m.group(2), 0) * self.scale.get(m.group(1), 1))]
        m = re.fullmatch(r'(\w+)\[(' + NUM + r')\]', a)
        if m and env.get(m.group(1), ('',))[0] == 'obj':
            return [self.slot(env[m.group(1)], int(m.group(2), 0) * 8)]
        return None

    def call(self, fn, f, argv, env, last_new, nth):
        if f in CONVERTERS:
            assert last_new, (fn, f)
            env[last_new] = ('conv', CONVERTERS[f], [num(a)[1] for a in argv if num(a)[0] is not None])
            return
        m = None
        if f == 'FUN_101427680' and len(argv) == 2 and argv[0].startswith('&'):
            env[argv[0][1:]] = ('name', argv[1].strip('"'))
            return
        if f == 'FUN_10142dd4c' and len(argv) == 3 and argv[0].startswith('&'):
            base = env.get(argv[1].lstrip('&'), ('name', '?'))[1]
            env[argv[0][1:]] = ('name', f'{base}{argv[2].strip(chr(34))}')
            return
        if f in SUBCTOR:
            objs = self.objarg(argv[SUBCTOR[f]], env)
            if objs:
                for o in objs:
                    sub = {'param_1': ('obj', o)}
                    for k, a in enumerate(argv):
                        if k != SUBCTOR[f] and num(a)[0] is not None:
                            sub[f'param_{k + 1}'] = ('const', int(a, 0))
                        elif k != SUBCTOR[f] and self.objarg(a, env):
                            sub[f'param_{k + 1}'] = ('obj', self.objarg(a, env)[0])
                    saved = self.scale
                    self.ctor('0x' + f[4:], o, sub)
                    self.scale = saved
                    v = VIRTUAL_SUBCTOR.get((f, o[-1]))
                    if v:
                        self.ctor('0x' + v[4:], o, {'param_1': ('obj', o)})
                        self.scale = saved
                return
        if f in SETUP:
            s = SETUP[f]
            objs = self.objarg(argv[s['obj']], env) if len(argv) > s['obj'] else None
            assert objs, (fn, f, argv)
            conv, rng = s.get('conv'), s.get('rng')
            if f == 'FUN_1026f0b58':
                rng = (num(argv[0])[1], num(argv[1])[1])
            ca = s.get('conv_arg')
            if ca is not None and len(argv) > ca and argv[ca] not in ('0',):
                c = env.get(argv[ca])
                assert c and c[0] == 'conv', (fn, f, argv, c)
                conv = (c[1], *c[2][:2]) if c[1] != 'quantizing' else ('quantizing', rng[0], rng[1])
            if s['dflt'] is None:
                dflt = s['fixed_default']
            else:
                a = argv[s['dflt']] if len(argv) > s['dflt'] else ''
                bits, dflt = num(a)
                if s['cls'] in ('bool', 'enum') and bits is not None:
                    dflt = int(a, 0)
                elif bits is None and a and all(env.get(n, ('',))[0] == 'const' for n in re.findall(r'\b[a-zA-Z_]\w*\b', a) if n not in ('int',)):
                    dflt = int(self.evalc(a, env))
            nm = argv[s['name']] if len(argv) > s['name'] else ''
            nm = nm.strip('"') if nm.startswith('"') else env.get(nm.lstrip('&'), ('name', nm))[1]
            ov = OVERRIDES.get((fn, f, nth))
            if ov:
                rng, conv, dflt = ov['internal'], ov['conv'], ov['default']
            for o in objs:
                self.rows.append({'ctor': fn, 'path': o, 'helper': f, 'nth': nth, 'cls': s['cls'], 'internal': rng,
                                  'conv': conv, 'default': dflt, 'default_arg': argv[s['dflt']] if s['dflt'] is not None else 'fixed',
                                  'display': nm, 'labels_arg': argv[2] if f == 'FUN_1026ef060' else ''})
            return
        objs = [o for a in argv for o in (self.objarg(a, env) or [])]
        if f in NONPARAM_SETTERS and objs:
            a = argv[NONPARAM_SETTERS[f]]
            v = env[a][1] if env.get(a, ('',))[0] == 'const' else a
            self.fields.append((fn, f, objs[0], v))
            return
        if objs and f not in IGNORE_ON_SLOT:
            self.other.append((fn, f, argv))

    def verify_floats(self):
        """Re-read float arguments from dossier disassembly for every set-up call in a dossier-covered ctor."""
        checked, mismatches = 0, []
        for fn in sorted({r['ctor'] for r in self.rows}):
            d = self.dossiers.get(fn)
            if not d:
                continue
            dis = d['disassembly']
            sites = {}
            for i, ins in enumerate(dis):
                m = re.fullmatch(r'bl? 0x([0-9a-f]+)', ins['text'])  # b = tail call
                if m:
                    sites.setdefault('FUN_' + m.group(1), []).append(i)
            for r in [r for r in self.rows if r['ctor'] == fn and r['helper'] in SETUP]:
                s = SETUP[r['helper']]
                if s['cls'] in ('bool', 'enum') and r['helper'] in INT_DEFAULT_REG and num(r['default_arg'])[0] is not None:
                    idx = sites[r['helper']][r['nth'] - 1]
                    got = wreg(dis, idx, INT_DEFAULT_REG[r['helper']])
                    checked += 1
                    if got is None or got != r['default']:
                        mismatches.append((fn, r['helper'], r['nth'], r['display'], got, r['default']))
                    r['asm_checked'] = True
                    continue
                if s['cls'] != 'float' or s['dflt'] is None:
                    continue
                idx = sites[r['helper']][r['nth'] - 1]
                regs = ['s0', 's1', 's2'] if r['helper'] in FLOAT_ARGS else ['s0']
                got = [sreg(dis, idx, reg) for reg in regs]
                want = [r['internal'][0], r['internal'][1], r['default']] if len(regs) == 3 else [r['default']]
                checked += 1
                if (fn, r['helper'], r['nth']) in OVERRIDES:
                    want = [None if g is None else w for g, w in zip(got, want)]  # computed in registers (scvtf)
                if any((g is None) != (w is None) or (g is not None and abs(g - w) > 1e-6 * max(1, abs(w)))
                       for g, w in zip(got, want)):
                    mismatches.append((fn, r['helper'], r['nth'], r['display'], got, want))
                r['asm_checked'] = True
        return checked, mismatches


def sreg(dis, i, reg):
    """Value of float register reg (s0..s15) just before instruction i, by scanning back (straight-line)."""
    n = int(reg[1:])
    for j in range(i - 1, max(i - 400, -1), -1):
        t = dis[j]['text']
        if t.startswith('bl ') and n < 8:
            return None  # clobbered by an earlier call before being set
        m = re.fullmatch(rf'fmov s{n},(0x[0-9a-f]+|#[-0-9.e+]+)', t)
        if m:
            return f32(int(m.group(1), 16)) if m.group(1).startswith('0x') else float(m.group(1)[1:])
        if re.fullmatch(rf'movi [dv]{n},#0x0', t) or re.fullmatch(rf'movi v{n}\.\w+,#0x0', t):
            return 0.0
        m = re.fullmatch(rf'fmov s{n},s(\d+)', t)
        if m:
            return sreg(dis, j, 's' + m.group(1))
        m = re.fullmatch(rf'fmov s{n},w(\d+)', t)
        if m:
            w = wreg(dis, j, int(m.group(1)))
            return None if w is None else f32(w)
        m = re.fullmatch(rf'scvtf s{n},w(\d+)', t)
        if m:
            w = wreg(dis, j, int(m.group(1)))
            return None if w is None else float(w - (1 << 32) if w >> 31 else w)
        if re.match(rf'\w+(\.\w+)? [sdqv]{n}[,.]', t):
            return None  # some other write we do not model
    return None


def wreg(dis, i, n):
    lo = hi = None
    for j in range(i - 1, max(i - 60, -1), -1):
        t = dis[j]['text']
        m = re.fullmatch(rf'movk w{n},#(0x[0-9a-f]+), LSL #16', t)
        if m and hi is None:
            hi = int(m.group(1), 16)
            continue
        m = re.fullmatch(rf'mov w{n},#(0x[0-9a-f]+|\d+)', t)
        if m:
            v = int(m.group(1), 0)
            return (v & 0xffff) | (hi << 16) if hi is not None else v
        if re.match(rf'\w+ [wx]{n},', t) or t.startswith('bl '):
            return None
    return None


def main(out, h4, live, results):
    img = xn.Image(live)
    classes, owner, info = xn.registrations(img)
    dossiers = {}
    for f in glob.glob(os.path.join(results, 'n6-*/functions/*.json')):
        d = json.load(open(f))
        dossiers[d['entry']] = d
    stored = {(r['device'], r['path']): r for r in csv.DictReader(open(os.path.join(h4, 'param_table.tsv')), delimiter='\t')}
    tops = {'UltraAnalog': 'DAT_106e7da00', 'StringStudio': 'DAT_106e7d0a0', 'Collision': 'DAT_106e790a0'}
    allrows, summary, fields = [], {}, []
    for dev, fn in TOP.items():
        w = Walk(img, dossiers)
        w.ctor(fn, (), {'param_1': ('obj', ())})
        checked, mism = w.verify_floats()
        seen = {}
        for r in w.rows:
            name, vcls = xn.name_of(r['path'], classes, tops[dev], info)
            r.update(device=dev, name=name or '', value_class=vcls or '')
            seen.setdefault(name, []).append(r)
        dup = {k: [x['ctor'] for x in v] for k, v in seen.items() if len(v) > 1}
        names = {k[1] for k in stored if k[0] == dev}
        summary[dev] = {'setup_calls': len(w.rows), 'stored_params': len(names),
                        'stored_configured': len(names & set(seen)),
                        'stored_not_configured': sorted(names - set(seen)),
                        'configured_not_stored': sorted(str(n) for n in set(seen) - names),
                        'configured_twice': dup, 'asm_checked_calls': checked, 'asm_mismatches': mism,
                        'other_calls_on_slots': sorted({o[1] for o in w.other})}
        allrows += w.rows
        for ctor, f, path, v in w.fields:
            name = xn.name_of(path, classes, tops[dev], info)[0]
            iv = int(v, 0) if isinstance(v, str) else v
            fields.append((dev, name or '/'.join(map(hex, path)), ctor, f, iv - (1 << 32) if iv >> 31 else iv))
    cols = ['device', 'name', 'value_class', 'cls', 'helper', 'ctor', 'nth', 'internal', 'conv', 'default',
            'default_arg', 'display', 'labels_arg', 'asm_checked']
    with open(os.path.join(out, 'constructors.tsv'), 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for r in allrows:
            f.write('\t'.join(str(r.get(c, '')) for c in cols) + '\n')
    with open(os.path.join(out, 'nonparam_fields.tsv'), 'w') as f:
        f.write('device\tfield\tctor\tsetter\tvalue (signed 32-bit)\n')
        for row in fields:
            f.write('\t'.join(map(str, row)) + '\n')
    json.dump(summary, open(os.path.join(out, 'constructors_summary.json'), 'w'), indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))


if __name__ == '__main__':
    main(*sys.argv[1:5])
