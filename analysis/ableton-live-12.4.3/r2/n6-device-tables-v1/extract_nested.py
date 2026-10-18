"""Derive the Live-side SetParameterA index tables for Analog, Tension and Collision (analyst tool; output is data).

usage: python3 -I extract_nested.py <out-dir> <h4-out-dir> <Live.arm64>

Extends N5's extract_mapping.py (flat builders only) to the nested builders found at vtable slot +0x5a0.
The builder pushes one 0x38-byte entry per SetParameterA index. Each push has an inline fast path
(capacity available: fields written in place) and an out-of-line slow path (an emplace helper). The
decompiled text interleaves both with gotos, so it is executed symbolically twice: once with every
capacity test true (fast) and once false (slow). Sub-builder calls are followed recursively with the
sub-object. Both runs must give the same member sequence and mode words (asserted). Member names come
from the class registration functions (FUN_10147e954(&class, -1, -1, offset, L"mpName", ...)), stored
ranges from H4 param_table.tsv, bundle kinds and ranges from H4 param_tables.json.
Depends on: C1 Live corpus via ../n1-transport-state-v1/corpus_lookup.py (N1_CACHE), Live.arm64 for
8-byte constants. Limitation: a pattern interpreter for this decompiler output, not a C front end; any
statement it does not recognise and that touches the vector raises an error.
"""
import csv, importlib.util, json, os, re, struct, sys
sys.dont_write_bytecode = True  # do not leave __pycache__ in other packets' directories

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('cl', os.path.join(HERE, '../n1-transport-state-v1/corpus_lookup.py'))
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)
EMAP = cl.entry_map()

# device xml element: (H4 bundle key, top registration fn, builder at +0x5a0)
DEVICES = {
    'UltraAnalog': ('Analog', '0x1031a1c70', '0x1031ad110'),
    'StringStudio': ('Tension', '0x103185630', '0x103193b1c'),
    'Collision': ('Collision', '0x1030db31c', '0x1030debd0'),
}
CLASS_INITS = ['0x1030f1c08', '0x10319bd08', '0x1031c639c']  # static FUN_10147e7c4(&class, L"Name", n, &base, ...)
REGISTRATIONS = ['0x1030ca850', '0x1030cbca8', '0x1030cedc0', '0x1030d0de4', '0x1030d4248', '0x1030db31c',
                 '0x103185630', '0x1031a1c70', '0x1031b1564', '0x1031b5eac', '0x1031b6524', '0x1031b6914']
VALUE_CLASS = {'FUN_1026f01e8': 'TimeableFloat', 'FUN_1026ee86c': 'TimeableEnum',
               'FUN_1026eb790': 'TimeableBool', 'FUN_1026ebbac': 'TimeableBool'}
MODE0 = 0x8000000000000000
# slow-path emplace helpers: name -> how the entry is built from the call arguments (see notes.md)
HELPERS = {
    'FUN_1030c50c0': 'm0', 'FUN_1030ed054': 'm0', 'FUN_1030ed1cc': 'm0', 'FUN_1031c280c': 'm0',
    'FUN_1030ed63c': 'mode', 'FUN_103199bc0': 'mode', 'FUN_103199ed8': 'mode',
    'FUN_103199a30': 'mode2', 'FUN_103199d48': 'mode2', 'FUN_103199734': 'mode5',
    'FUN_1030ed9c0': 'mult', 'FUN_1030c4c98': 'table', 'FUN_1030ed468': 'table',
    'FUN_1031998c0': 'empty', 'FUN_1031c2694': 'ptr', 'FUN_1030ed7f0': 'struct',
}
IGNORED_CALLS = {'FUN_101a24778'}  # operator delete of a temporary table
MODE_NAME = {0: 'IndexedFloat (identity)', 1: 'ModulationPolarizer', 2: 'ToggleMapping', 3: 'FilterType',
             4: 'BoolInverter', 5: 'ToToggleMapping', 6: 'MultiplyOffset', 7: 'IntegerMapping (table)',
             8: 'CollisionScaledMode'}


def code(entry):
    f, off = EMAP[entry]
    with open(f, 'rb') as fh:
        fh.seek(off)
        return json.loads(fh.readline())['code']


class Image:
    def __init__(self, path):
        self.b = open(path, 'rb').read()
        ncmds, off, self.segs = struct.unpack_from('<I', self.b, 16)[0], 32, []
        for _ in range(ncmds):
            cmd, size = struct.unpack_from('<II', self.b, off)
            if cmd == 0x19:
                vm, vs, fo, fs = struct.unpack_from('<QQQQ', self.b, off + 24)
                self.segs.append((vm, fo, fs))
            off += size

    def ptr(self, w):
        return None if w >> 63 else (w & 0xFFFFFFFFF) | 0x100000000  # chained-fixup rebase (as read_ptrs.py)

    def vtable_slot(self, cpp_name, slot):
        """Function at vtable address point + slot for the class whose typeinfo name is <len><cpp_name>."""
        if not hasattr(self, 'rev'):
            self.rev = {}
            for vm, fo, fs in self.segs:
                if vm >= 0x106000000:  # __DATA_CONST / __DATA
                    for o in range(fo, fo + fs - 7, 8):
                        w = struct.unpack_from('<Q', self.b, o)[0]
                        if not w >> 63:
                            self.rev.setdefault(self.ptr(w), []).append(vm + o - fo)
        name = b'\0' + f'{len(cpp_name)}{cpp_name}'.encode() + b'\0'
        o = self.b.find(name)
        assert o > 0 and self.b.find(name, o + 1) < 0, cpp_name
        o += 1
        va = next(vm + o - fo for vm, fo, fs in self.segs if fo <= o < fo + fs)
        out = set()
        for ti in (a - 8 for a in self.rev.get(va, [])):
            for a in self.rev.get(ti, []):
                ap = a + 8
                if self.word(ap - 16) == 0:
                    out.add(self.ptr(self.word(ap + slot)))
        assert len(out) == 1, (cpp_name, out)
        return out.pop()

    def wstr(self, va):
        out = ''
        while (c := self.word(va) & 0xffff):
            out += chr(c)
            va += 2
        return out

    def byte(self, va):
        return self.word(va) & 0xff

    def word(self, va):
        for vm, fo, fs in self.segs:
            if vm <= va < vm + fs:
                return struct.unpack_from('<Q', self.b, fo + va - vm)[0]
        raise ValueError(f'unmapped {va:#x}')


def registrations(img):
    """class descriptor -> {slot offset: (name without 'mp', value class or ('class', descriptor))}, plus
    {class: (C++ name, base class)}. A member's type is the getter assigned to puVar just before its
    FUN_10147e954 call. FUN_10147eacc registers an array member (total bytes, stride): names get '.k'."""
    call = re.compile(r'FUN_10147e(954|acc)\(&(DAT_[0-9a-f]+),(?:(0x[0-9a-f]+|\d+),(0x[0-9a-f]+|\d+),)?'
                      r'0xffffffff,0xffffffff,(0x[0-9a-f]+|\d+),\s*(?:L"mp(\w+)"|&(DAT_[0-9a-f]+))')
    getter = re.compile(r'= \(undefined4 \*\)(FUN_[0-9a-f]+)\((?:&(DAT_[0-9a-f]+))?\);')
    classes, owner, info = {}, {}, {}
    for fn in REGISTRATIONS:
        src, last = code(fn), 0
        for m in call.finditer(src):
            g = getter.findall(src[last:m.start()])
            assert g, (fn, m.group(0))
            fun, sub = g[-1]
            kind = ('class', sub) if sub else VALUE_CLASS.get(fun, 'other:' + fun)
            off = int(m.group(5), 0)
            name = m.group(6) or img.wstr(int(m.group(7)[4:], 16))[2:]  # short names the decompiler left as data
            if m.group(1) == 'acc':
                total, stride = int(m.group(3), 0), int(m.group(4), 0)
                for k in range(total // stride):
                    classes.setdefault(m.group(2), {})[off + k * stride] = (f'{name}.{k}', kind)
            else:
                classes.setdefault(m.group(2), {})[off] = (name, kind)
            owner.setdefault(m.group(2), fn)
            last = m.end()
    for fn in CLASS_INITS:
        for cls, nm, base in re.findall(r'FUN_10147e7c4\(&(DAT_[0-9a-f]+),L"(\w+)",\w+,&(DAT_[0-9a-f]+)', code(fn)):
            info[cls] = (nm, base)
    return classes, owner, info


def statements(src):
    body = src[src.index('\n{\n') + 3:src.rindex('\n}')]
    out, cur = [], ''
    for line in body.split('\n'):
        s = line.strip()
        if not s or s.startswith('/*') or s.startswith('//'):
            continue
        cur = (cur + ' ' + s).strip()
        if (cur.endswith((';', '{', '}')) and not re.fullmatch(r'\} while \(.*', cur[:-1] if cur.endswith('{') else '')) \
                or re.fullmatch(r'LAB_\w+:', cur):
            out.append(cur)
            cur = ''
    assert not cur, cur
    return out


def compile_flat(stmts):
    """Structured if/else and gotos -> flat ops: ('s', text) ('jf', cond, label) ('jt', cond, label) ('j', label) ('L', label)."""
    ops, stack, n = [], [], [0]

    def new():
        n[0] += 1
        return f'_L{n[0]}'
    i = 0
    while i < len(stmts):
        s = stmts[i]
        m = re.fullmatch(r'if \((.*)\) goto (LAB_\w+);', s)
        if m:
            ops.append(('jt', m.group(1), m.group(2)))
        elif re.fullmatch(r'if \((.*)\) \{', s):
            lab = new()
            ops.append(('jf', re.fullmatch(r'if \((.*)\) \{', s).group(1), lab))
            stack.append(('if', lab))
        elif s == '}':
            kind, lab = stack.pop()
            nxt = stmts[i + 1] if i + 1 < len(stmts) else ''
            if kind == 'if' and nxt == 'else {':
                end = new()
                ops += [('j', end), ('L', lab)]
                stack.append(('else', end))
                i += 1
            elif kind == 'if' and re.fullmatch(r'else if \((.*)\) \{', nxt):
                end, lab2 = new(), new()
                ops += [('j', end), ('L', lab)]
                stack.append(('elseif', end))
                ops.append(('jf', re.fullmatch(r'else if \((.*)\) \{', nxt).group(1), lab2))
                stack.append(('if', lab2))
                i += 1
            else:
                ops.append(('L', lab))
                while stack and stack[-1][0] == 'elseif':
                    ops.append(('L', stack.pop()[1]))
        elif s == 'do {':
            stack.append(('do', None))  # body taken once; the back edge is not followed
        elif re.fullmatch(r'\} while \(.*\);', s):
            assert stack.pop()[0] == 'do'
        elif s == 'else {':
            raise ValueError('dangling else')
        elif re.fullmatch(r'goto (LAB_\w+);', s):
            ops.append(('j', s[5:-1]))
        elif re.fullmatch(r'LAB_\w+:', s):
            ops.append(('L', s[:-1]))
        elif s.endswith('{'):
            raise ValueError('unsupported block: ' + s)
        else:
            ops.append(('s', s))
        i += 1
    assert not stack, stack
    return ops


DECL = re.compile(r'(?:undefined\d?|long|ulong|int|uint|double|float|char|bool|code)\s*\**\s*\w+(?:\s*\[\d+\])?;')
NUM = r'(?:0x[0-9a-f]+|\d+)'


class Run:
    def __init__(self, fast, classes, image, trace):
        self.fast, self.classes, self.img, self.trace = fast, classes, image, trace
        self.entries = []

    @staticmethod
    def hi32(env, var):
        v = env.get(var, ('const', 0))
        return v[1] >> 32 if v[0] == 'const' else 0

    def dat(self, name):
        return self.img.word(int(name.split('_')[-1], 16))

    def builder(self, fn, objpath, args):
        """args: {param name: ('obj', path) | ('vec',) | ('const', v)}"""
        src = code(fn)
        sig = re.search(r'\w+ \*?FUN_[0-9a-f]+\(([^)]*)\)', src).group(1)
        ptype = {}
        for p in sig.split(','):
            t, nm = p.strip().rsplit(' ', 1)
            ptype[nm.lstrip('*')] = 8 if ('*' in p and not t.startswith('char')) else 1
        env = dict(args)
        ops = compile_flat([s for s in statements(src) if not DECL.fullmatch(s)])
        labels = {op[1]: k for k, op in enumerate(ops) if op[0] == 'L'}
        pend, pc, steps = None, 0, 0
        while pc < len(ops):
            steps += 1
            assert steps < 100000, fn
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
                    pc = labels[op[2]] if op[2] in labels else len(ops)
                continue
            s = op[1]
            if s == 'return;':
                break
            pend = self.stmt(fn, s, env, ptype, pend)
        assert pend is None, (fn, pend)

    def cond(self, c, env):
        c = c.strip()
        if re.fullmatch(r'\(?\s*(?:\(\w+ \*\*?\))?p[lu]Var\d+ < .*', c):
            return self.fast
        if re.fullmatch(r'.* <= (?:\(\w+ \*\))?p[lu]Var\d+\)?', c):
            return not self.fast
        expr = c.replace('&&', ' and ').replace('||', ' or ').replace("'\\x01'", '1').replace("'\\0'", '0')
        expr = re.sub(r'\((?:int|long|char)\)', '', expr)
        for var in set(re.findall(r'\b(?:local|uStack|param)_\w+\b', expr)):
            val = env.get(var)
            assert val and val[0] == 'const', (c, var, val)
            expr = re.sub(rf'\b{var}\b', str(val[1]), expr)
        return bool(eval(expr, {'__builtins__': {}}))  # expr is only numbers and comparisons here

    def addr(self, e, env, ptype):
        """'BASE + OFF' or 'BASE' -> (objpath, byte offset)."""
        m = re.fullmatch(rf'(\w+)(?: \+ ({NUM}))?', e.strip())
        base = env.get(m.group(1))
        assert base and base[0] in ('obj', 'ref'), (e, base)
        off = int(m.group(2), 0) if m.group(2) else 0
        return base[1], off * ptype.get(m.group(1), 1)

    def load(self, e, env, ptype):
        """Pointer read from a member slot: '*(T *)(BASE + OFF)' or 'BASE[N]' -> member path (slot = off - 8)."""
        e = e.strip()
        m = re.fullmatch(r'\*\((?:\w+) \*+\)\((.+)\)', e) or re.fullmatch(r'\*\((?:\w+) \*+\)(\w+)', e)
        if m:
            path, off = self.addr(m.group(1), env, ptype)
        else:
            m = re.fullmatch(rf'(\w+)\[({NUM})\]', e)
            assert m and env.get(m.group(1), ('',))[0] in ('obj', 'ref'), e
            path, off = env[m.group(1)][1], int(m.group(2), 0) * 8
        return path + (off - 8,)

    def value(self, e, env, ptype):
        e = e.strip()
        e = re.sub(r'^\((?:long|double|ulong|undefined8)\)', '', e)
        m = re.fullmatch(rf'NEON_fmov\(({NUM}),4\)', e)
        if m:  # fmov v.2s, #imm: both 32-bit lanes hold imm
            x = int(m.group(1), 0)
            return ('const', (x << 32) | x)
        m = re.fullmatch(r'-([a-zA-Z_]\w*)', e)
        if m and env.get(m.group(1), ('',))[0] == 'const':  # fneg on a d register flips bit 63 only
            return ('const', env[m.group(1)][1] ^ (1 << 63))
        if re.fullmatch(r"'\\(?:0|x[0-9a-f]{2})'", e):
            return ('const', 0 if e == "'\\0'" else int(e[3:5], 16))
        if re.fullmatch(r'-?' + NUM, e):
            return ('const', int(e, 0) & 0xffffffffffffffff)
        if re.fullmatch(r'_?DAT_[0-9a-f]+', e):
            return ('const', self.dat(e))
        if e in env:
            return env[e]
        m = re.fullmatch(rf'\(\*\*\(code \*\*\)\(\*(\w+) \+ ({NUM})\)\)\(\1\)', e)
        if m:  # parameter returned by a virtual getter of the object; resolved in notes.md
            return ('ref', env[m.group(1)][1] + (f'vcall+{m.group(2)}',))
        m = re.fullmatch(r'CONCAT44\((\w+)\._4_4_,(.+)\)', e)
        if m:
            hi = self.hi32(env, m.group(1))
            return ('const', (hi << 32) | (self.value(m.group(2), env, ptype)[1] & 0xffffffff))
        return ('ref', self.load(e, env, ptype))

    def entry(self, fn, member, second=None, word=MODE0, w3=0x7f7fffff7f7fffff, flag=0, table=None, how=''):
        self.entries.append({'fn': fn, 'member': member, 'second': second, 'word': word, 'w3': w3,
                             'flag': flag, 'table': table, 'how': how})

    def call(self, fn, f, argv, env, ptype):
        vec = [k for k, v in env.items() if v == ('vec',)]
        if f in HELPERS:
            kind = HELPERS[f]
            assert argv[0] in vec, (fn, f, argv)
            loc = lambda a: env.get(a.lstrip('&'), ('const', 0))[1]
            if kind == 'empty':
                return self.entry(fn, None, how=f)
            if kind == 'ptr':
                v = env.get(argv[1].lstrip('&'), ('const', 0))
                return self.entry(fn, v[1] if v[0] == 'ref' else None, how=f)
            if kind == 'struct':
                base = int(argv[1].lstrip('&').split('_')[-1], 16)
                fld = lambda k: next((env[n] for n in env if re.fullmatch(rf'(?:local|[a-z]Stack)_{base - 8 * k:x}', n)), ('const', 0))
                f0, f2, f3 = fld(0), fld(2), fld(3)
                return self.entry(fn, f0[1] if f0[0] == 'ref' else None, word=f2[1], w3=f3[1], how=f)
            path, off = self.addr(argv[1], env, ptype)
            member = path + (off,)
            if kind == 'm0':
                return self.entry(fn, member, how=f)
            if kind == 'mode':
                return self.entry(fn, member, word=(0x80000000 << 32) | (loc(argv[2]) & 0xffffffff), how=f)
            if kind == 'mode2':
                p2, o2 = self.addr(argv[3], env, ptype)
                return self.entry(fn, member, second=p2 + (o2,), word=(0x80000000 << 32) | (loc(argv[2]) & 0xffffffff), how=f)
            if kind == 'mode5':
                return self.entry(fn, member, word=((loc(argv[4]) & 0xffffffff) << 32) | (loc(argv[2]) & 0xffffffff), how=f)
            if kind == 'mult':
                return self.entry(fn, member, word=self.dat('DAT_1055d1ec0'),
                                  w3=((loc(argv[3]) & 0xffffffff) << 32) | (loc(argv[2]) & 0xffffffff), how=f)
            if kind == 'table':
                return self.entry(fn, member, word=self.dat('DAT_1055d1ed0'), table=argv[2], how=f)
        if f in IGNORED_CALLS:
            return None
        if f == 'FUN_1030cb434':
            return self.mod_target(fn, argv, env, ptype)
        objs = [a for a in argv if not a.startswith('&') and a not in vec]
        if any(a in vec for a in argv) and objs:  # sub-builder: (object pointer, vector[, int])
            obj = self.load(objs[0], env, ptype)
            sub = {}
            for k, a in enumerate(argv):
                nm = f'param_{k + 1}'
                if a in vec:
                    sub[nm] = ('vec',)
                elif a == objs[0]:
                    sub[nm] = ('obj', obj)
                else:
                    sub[nm] = self.value(a, env, ptype)
            self.trace.append((f, obj))
            return self.builder('0x' + f[4:], obj, sub)
        raise ValueError(f'unhandled call in {fn}: {f}({argv})')

    def mod_target(self, fn, argv, env, ptype):
        """Hand model of FUN_1030cb434(target object, vector, source), read in full (notes.md): Target slot 0x40 is
        pushed with mode 0 when source is 0, otherwise mode 7 with the table of every k in 0..17 whose byte
        DAT_1068c5398[0x28 * k + source] has bit 0 clear; then Amount slot 0x58 with mode 8."""
        obj = self.load(argv[0], env, ptype)
        src = self.value(argv[2], env, ptype)
        assert src[0] == 'const', argv
        self.trace.append(('FUN_1030cb434', obj))
        if src[1] == 0:
            self.entry('0x1030cb434', obj + (0x40,), how='model')
        else:
            tab = [k for k in range(18) if not self.img.byte(0x1068c5398 + 0x28 * k + src[1]) & 1]
            self.entry('0x1030cb434', obj + (0x40,), word=self.dat('DAT_1055d1ed0'), table=tab, how='model')
        self.entry('0x1030cb434', obj + (0x58,), word=self.dat('DAT_10584d6d0'), how='model')

    def stmt(self, fn, s, env, ptype, pend):
        m = re.fullmatch(r'(?:(\w+(?:\._0_4_)?) = )?(?:\(\w+ \*+\))?(FUN_[0-9a-f]+)\((.*)\);', s)
        if m:
            argv = [a.strip() for a in re.split(r',(?![^()]*\))', m.group(3))] if m.group(3) else []
            self.call(fn, m.group(2), argv, env, ptype)
            return pend
        if pend is not None and re.search(r'\bp[lu]Var\d+ \+ 7\b', s) and not re.fullmatch(r'(?:\*|p[lu]Var\d+\[)', s[:7]):
            self.flush(fn, pend, env, ptype)  # the entry pointer advances past a completed inline entry
            pend = None
        m = re.fullmatch(r'(\w+)\._4_4_ = (.+);', s)
        if m:
            var, val = m.groups()
            if val == f'(undefined4)((ulong){var} >> 0x20)':
                return pend  # keeps the high half
            old = env.get(var, ('const', 0))
            lo = old[1] & 0xffffffff if old[0] == 'const' else 0
            env[var] = ('const', ((self.value(val, env, ptype)[1] & 0xffffffff) << 32) | lo)
            return pend
        m = re.fullmatch(r'(\w+)\._0_4_ = (.+);', s)
        if m:
            var, val = m.groups()
            hi = self.hi32(env, var)
            env[var] = ('const', (hi << 32) | (self.value(val, env, ptype)[1] & 0xffffffff))
            return pend
        for rx, fld in ((r'\*(p[lu]Var\d+) = (.+);', 0), (r'(p[lu]Var\d+)\[(\d+)\] = (.+);', None),
                        (r'\*\(\w+ \*\)\((p[lu]Var\d+) \+ (\d+)\) = (.+);', None),
                        (r'\*\(\w+ \*\)\(\(long\)(p[lu]Var\d+) \+ 0x34\) = (.+);', 'x')):
            m = re.fullmatch(rx, s)
            if m and env.get(m.group(1)) != ('vecalias',):
                if m.group(m.lastindex).startswith('(ulong)'):
                    return pend  # end-pointer update through an alias of the vector header
                field = int(m.group(2)) if fld is None else fld
                pend = pend or {}
                pend[field] = m.group(m.lastindex)
                return pend
            if m:
                return pend
        if re.fullmatch(r'\*\(\w+ \*+\)\(\w+ \+ (?:8|0x10)\) = .*;|\*?param_\d+(?:\[\d\])? = .*;', s):
            return pend  # vector header writes (begin/end/capacity)
        m = re.fullmatch(r'(\w+) = (.+);', s)
        assert m, f'unrecognised statement in {fn}: {s}'
        var, rhs = m.groups()
        if re.fullmatch(r'p[lu]Var\d+', var):
            if re.search(r'\bp[lu]Var\d+ \+ 7\b', rhs) and pend is not None:
                self.flush(fn, pend, env, ptype)
                return None
            if re.fullmatch(r'\w+ \+ [12]', rhs) and rhs.split()[0].startswith('param_'):
                env[var] = ('vecalias',)
            return pend
        if re.search(r'\bp[lu]Var\d+ \+ 7\b', rhs) and pend is not None:
            self.flush(fn, pend, env, ptype)
            pend = None
        if re.fullmatch(r'\(\w+ \*+\)\w+\[\d\]|\*\(\w+ \*+\)\(\w+ \+ (?:8|0x10)\)', rhs) or re.search(r'\bp[lu]Var\d+\b', rhs):
            return pend  # reads of the vector header
        env[var] = self.value(rhs, env, ptype)
        return pend

    def flush(self, fn, pend, env, ptype):
        f0 = pend.get(0, '0')
        v0 = self.value(f0, env, ptype)
        member = v0[1] if v0[0] == 'ref' else None
        assert v0[0] == 'ref' or v0 == ('const', 0), (fn, pend)
        sec = self.value(pend[1], env, ptype) if 1 in pend else ('const', 0)
        word = self.value(pend.get(2, '0'), env, ptype)[1]
        w3 = self.value(pend.get(3, '0x7f7fffff7f7fffff'), env, ptype)
        w3 = w3[1] if w3[0] == 'const' else None
        flag = self.value(pend.get(4, '0'), env, ptype)[1]
        self.entry(fn, member, second=sec[1] if sec[0] == 'ref' else None, word=word, w3=w3, flag=flag, how='inline')


def name_of(path, classes, top, info):
    cls, parts, kind = top, [], None
    for off in path:
        c = cls
        while c is not None and off not in classes.get(c, {}):
            c = info.get(c, (None, None))[1]  # inherited member
        if c is None:
            return None, None
        nm, kind = classes[c][off]
        parts.append(nm)
        cls = kind[1] if isinstance(kind, tuple) else None
    return '/'.join(parts), (kind if isinstance(kind, str) else 'object')


def class_at(path, classes, top, info):
    cls = top
    for off in path:
        c = cls
        while c is not None and off not in classes.get(c, {}):
            c = info.get(c, (None, None))[1]
        cls = classes[c][off][1][1]
    return cls


def f32(w):
    return struct.unpack('<f', struct.pack('<I', w & 0xffffffff))[0]


def main(out_dir, h4, live):
    img = Image(live)
    classes, owner, info = registrations(img)
    table = {(r['device'], r['path']): r for r in csv.DictReader(open(os.path.join(h4, 'param_table.tsv')), delimiter='\t')}
    bundle = json.load(open(os.path.join(h4, 'param_tables.json')))
    rows, summary, vres = [], {}, {d: [] for d in DEVICES}
    for dev, (bkey, reg, bld) in DEVICES.items():
        top = next(c for c, fn in owner.items() if fn == reg)
        runs = {}
        for fast in (True, False):
            trace = []
            r = Run(fast, classes, img, trace)
            r.builder(bld, (), {'param_1': ('vec',), 'param_2': ('obj', ())})
            runs[fast] = (r.entries, trace)
        fast_e, slow_e = runs[True][0], runs[False][0]
        key = lambda e: (e['member'], e['second'], e['word'])
        assert [key(e) for e in fast_e] == [key(e) for e in slow_e], dev
        for fe, se in zip(fast_e, slow_e):  # mode-6 operands: equal where the fast path shows them
            if (fe['word'] & 0xffffffff) == 6:
                assert fe['w3'] in (None, se['w3']), (dev, fe, se)
                fe['w3'] = se['w3']
        for e in fast_e:  # resolve virtual getters: class of the object -> vtable slot -> getter's returned slot
            if e['member'] and isinstance(e['member'][-1], str):
                parent = e['member'][:-1]
                cls = class_at(parent, classes, top, info)
                fn = img.vtable_slot(info[cls][0], int(e['member'][-1].split('+')[1], 16))
                m = re.fullmatch(rf'\s*\w+ FUN_{fn:x}\(long param_1\)\s*\{{\s*return \*\(undefined8 \*\)\(param_1 \+ ({NUM})\);\s*\}}\s*', code(hex(fn)))
                assert m, hex(fn)
                vres[dev].append((e['member'], info[cls][0], hex(fn), int(m.group(1), 0) - 8))
                e['member'] = parent + (int(m.group(1), 0) - 8,)
                e['how'] += f' via virtual getter {fn:#x}'
        brows = {b['index']: b for b in bundle[bkey]['rows']}
        for i, e in enumerate(fast_e):
            name, cls = name_of(e['member'], classes, top, info) if e['member'] else (None, None)
            name2 = name_of(e['second'], classes, top, info)[0] if e['second'] else None
            st = table.get((dev, name))
            b = brows.get(i)
            mode, hi = e['word'] & 0xffffffff, e['word'] >> 32
            extra = ''
            if mode == 6:
                extra = f'mult={f32(e["w3"]):g} off={f32(e["w3"] >> 32):g}'
            elif mode == 5:
                extra = f'param={hi}'
            elif mode == 1:
                extra = f'invert={e["flag"]}'
            elif mode == 7:
                extra = 'table=' + ','.join(map(str, e['table']))
            rows.append({'device': dev, 'index': i, 'name': name or '', 'second': name2 or '', 'value_class': cls or '',
                         'member_path': '/'.join(o if isinstance(o, str) else hex(o) for o in e['member']) if e['member'] else '',
                         'builder_fn': e['fn'], 'mode': mode, 'mode_name': MODE_NAME.get(mode, '?'), 'mode_arg': extra,
                         'stored_range': st['range'] if st else '', 'schema_param': bool(st),
                         'bundle_kind': '' if b is None else b['kind'],
                         'bundle_range': '' if b is None or b['min'] is None else f"{b['min']:g}..{b['max']:g}",
                         'bundle_virtual': '' if b is None else b['virtual']})
        stored = {k[1] for k in table if k[0] == dev}
        in_vec = {r['name'] for r in rows if r['device'] == dev} | {r['second'] for r in rows if r['device'] == dev}
        summary[dev] = {'builder': bld, 'registration': reg, 'class': top, 'entries': len(fast_e),
                        'empty_entries': sum(1 for e in fast_e if e['member'] is None),
                        'modes': {str(m): sum(1 for e in fast_e if (e['word'] & 0xffffffff) == m)
                                  for m in sorted({e['word'] & 0xffffffff for e in fast_e})},
                        'sub_builders': sorted({f for f, _ in runs[True][1]}),
                        'bundle_entries': len(brows), 'bundle_max_index': max(brows),
                        'schema_params': len(stored), 'schema_params_in_vector': len(stored & in_vec),
                        'schema_params_not_in_vector': sorted(stored - in_vec),
                        'vector_names_not_stored': sorted(n for n in in_vec - stored if n),
                        'virtual_getters': [['/'.join(map(str, p)), c, f, hex(o)] for p, c, f, o in vres[dev]]}
    cols = list(rows[0])
    with open(os.path.join(out_dir, 'live_index_map.tsv'), 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(str(r[c]) for c in cols) + '\n')
    json.dump(summary, open(os.path.join(out_dir, 'live_index_summary.json'), 'w'), indent=1, sort_keys=True)
    json.dump({c: {'cpp_name': info.get(c, ('', ''))[0], 'base': info.get(c, ('', ''))[1], 'registration': owner[c],
                   'members': {hex(o): [n, k if isinstance(k, str) else k[1]] for o, (n, k) in sorted(m.items())}}
               for c, m in classes.items()}, open(os.path.join(out_dir, 'registration_classes.json'), 'w'), indent=1)
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == '__main__':
    main(*sys.argv[1:4])
