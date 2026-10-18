"""Static reader and disassembler for CPython 3.11 .pyc files (magic a70d0d0a).

Analyst tooling for packet H6. It never imports or executes the code it reads:
marshal data is parsed in pure Python and bytecode is only listed. The opcode
table is rebuilt from the bundle's own lib/opcode.pyc constants.

usage: python3 -I pyc311.py OPCODE_PYC OUT_DIR ROOT [ROOT...]
Writes OUT_DIR/<relpath>.txt per .pyc (AppleDouble ._* skipped).
"""
import os
import struct
import sys

MAGIC = bytes.fromhex('a70d0d0a')


class Code:
    __slots__ = ('argcount', 'posonly', 'kwonly', 'stacksize', 'flags', 'code', 'consts',
                 'names', 'lnames', 'lkinds', 'filename', 'name', 'qualname', 'firstlineno',
                 'linetable', 'exctable')


class Reader:
    def __init__(self, data):
        self.d, self.p, self.refs = data, 0, []

    def take(self, n):
        b = self.d[self.p:self.p + n]
        if len(b) != n:
            raise ValueError(f'truncated marshal at {self.p}')
        self.p += n
        return b

    def i32(self):
        return struct.unpack('<i', self.take(4))[0]

    def obj(self):
        code = self.take(1)[0]
        flag, t = code & 0x80, chr(code & 0x7f)
        slot = None
        if flag:
            slot = len(self.refs)
            self.refs.append(None)
        v = self.value(t)
        if flag:
            self.refs[slot] = v
        return v

    def value(self, t):
        simple = {'0': None, 'N': None, 'F': False, 'T': True, 'S': StopIteration, '.': Ellipsis}
        if t in simple:
            return simple[t]
        if t == 'i':
            return self.i32()
        if t == 'l':
            n = self.i32()
            digits = struct.unpack(f'<{abs(n)}H', self.take(2 * abs(n)))
            v = sum(d << (15 * k) for k, d in enumerate(digits))
            return -v if n < 0 else v
        if t == 'g':
            return struct.unpack('<d', self.take(8))[0]
        if t == 'y':
            return complex(*struct.unpack('<dd', self.take(16)))
        if t == 's':
            return self.take(self.i32())
        if t in 'tuaA':
            raw = self.take(self.i32())
            return raw.decode('utf-8', 'surrogatepass') if t in 'tu' else raw.decode('latin-1')
        if t in 'zZ':
            return self.take(self.take(1)[0]).decode('latin-1')
        if t in ')([<>':
            n = self.take(1)[0] if t == ')' else self.i32()
            items = [self.obj() for _ in range(n)]
            return items if t == '[' else tuple(items)
        if t == '{':
            out = {}
            while True:
                k = self.obj()
                if k is None:
                    return out
                out[k] = self.obj()
        if t == 'r':
            return self.refs[self.i32()]
        if t == 'c':
            c = Code()
            c.argcount, c.posonly, c.kwonly, c.stacksize, c.flags = (self.i32() for _ in range(5))
            for f in ('code', 'consts', 'names', 'lnames', 'lkinds', 'filename', 'name', 'qualname'):
                setattr(c, f, self.obj())
            c.firstlineno = self.i32()
            c.linetable, c.exctable = self.obj(), self.obj()
            return c
        raise ValueError(f'unknown marshal type {t!r} at {self.p - 1}')


def load(path):
    data = open(path, 'rb').read()
    if data[:4] != MAGIC:
        raise ValueError(f'{path}: magic {data[:4].hex()} is not CPython 3.11')
    return Reader(data[16:]).obj()


def opmap_from(opcode_pyc):
    """Pair def_op('NAME', n) constants; deduplicated ints need two fixed values."""
    consts = load(opcode_pyc).consts
    start = consts.index('CACHE')
    ops, pending = {'CACHE': 0, 'STORE_NAME': 90}, None
    for v in consts[start:]:
        if isinstance(v, str) and v.isupper():
            pending = v
        elif isinstance(v, int) and pending:
            ops.setdefault(pending, v)
            pending = None
        elif isinstance(v, tuple):
            break
    check = {'LOAD_CONST': 100, 'LOAD_GLOBAL': 116, 'CALL': 171, 'PRECALL': 166,
             'LOAD_METHOD': 160, 'KW_NAMES': 172, 'RESUME': 151, 'BINARY_OP': 122}
    bad = {k: ops.get(k) for k, v in check.items() if ops.get(k) != v}
    if bad:
        raise ValueError(f'opcode table mismatch: {bad}')
    return {v: k for k, v in ops.items()}


NAME_OPS = {'LOAD_METHOD', 'LOAD_ATTR', 'STORE_ATTR', 'DELETE_ATTR', 'IMPORT_NAME', 'IMPORT_FROM',
            'LOAD_NAME', 'STORE_NAME', 'DELETE_NAME', 'STORE_GLOBAL', 'DELETE_GLOBAL'}
LOCAL_OPS = {'LOAD_FAST', 'STORE_FAST', 'DELETE_FAST', 'LOAD_CLOSURE', 'LOAD_DEREF', 'STORE_DEREF',
             'DELETE_DEREF', 'MAKE_CELL', 'LOAD_CLASSDEREF'}
CMP = ('<', '<=', '==', '!=', '>', '>=')


def short(v):
    if isinstance(v, Code):
        return f'<code {v.qualname}>'
    r = repr(v)
    return r if len(r) <= 300 else r[:300] + '...'


def disasm(c, opname):
    out, ext = [], 0
    b = c.code
    for i in range(0, len(b), 2):
        op, arg = b[i], b[i + 1] | ext
        name = opname.get(op, f'OP{op}')
        if name == 'CACHE':
            continue
        if name == 'EXTENDED_ARG':
            ext = arg << 8
            continue
        ext = 0
        note = ''
        if name in ('LOAD_CONST', 'KW_NAMES'):
            note = short(c.consts[arg])
        elif name == 'LOAD_GLOBAL':
            note = c.names[arg >> 1]
        elif name in NAME_OPS:
            note = c.names[arg]
        elif name in LOCAL_OPS:
            note = c.lnames[arg] if arg < len(c.lnames) else '?'
        elif name == 'COMPARE_OP':
            note = CMP[arg] if arg < len(CMP) else '?'
        out.append(f'  {i:6d} {name:<28} {arg:<5} {note}'.rstrip())
    return out


def walk(c, opname, lines):
    args = c.lnames[:c.argcount + c.kwonly + bool(c.flags & 4) + bool(c.flags & 8)]
    lines.append(f'== {c.qualname} line {c.firstlineno} args {list(args)} flags {c.flags:#x}')
    lines.extend(disasm(c, opname))
    for k in c.consts:
        if isinstance(k, Code):
            walk(k, opname, lines)


def main(argv):
    opname = opmap_from(argv[1])
    out_dir = argv[2]
    for root in argv[3:]:
        base = os.path.dirname(root.rstrip('/'))
        for dirpath, dirs, files in os.walk(root):
            dirs.sort()
            for f in sorted(files):
                if f.startswith('._') or not f.endswith('.pyc'):
                    continue
                src = os.path.join(dirpath, f)
                c = load(src)
                lines = [f'# source {os.path.relpath(src, base)}', f'# co_filename {c.filename}']
                walk(c, opname, lines)
                dst = os.path.join(out_dir, os.path.relpath(src, base)[:-4] + '.txt')
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, 'w') as fh:
                    fh.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main(sys.argv)
