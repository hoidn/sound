"""Driver for the xexec loader: build it, run one call sequence per subprocess, parse the output.

    from xexec import Runner
    r = Runner()                                  # builds xexec.c if needed
    res = r.run(['call', '0x101433f60', 'buf:8', dbl(0.5), 'dump', 'b0*+16', 'b0*+4@'])
    ustr(res.dumps[0][2])                         # -> '25R'

Each run is a fresh process with a timeout, so a fault or trap ends only that run.
run(tokens, skip={addr: [gdb expr, ...]}) runs the same process under gdb: each time execution
reaches addr, the expressions are printed as one "HIT addr v1 v2 ..." line and the function is
left at once with gdb `return` (its body does not run; use it only for void functions).
run(tokens, gdb_script=path) loads an owned GDB script instead of the skip script.
Dependencies: gcc (build), gdb (skip or introspection), the x86_64 slice.
"""
import os
import re
import struct
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICE = os.environ.get('XEXEC_SLICE', '/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64')
BIN = Path(os.environ.get('XEXEC_BIN', '/var/tmp/sound-analysis/xexec/xexec'))
CFLAGS = ['-O1', '-g', '-Wall', '-Wextra', '-no-pie']


def build():
    """Compile xexec.c into BIN when BIN is missing or older than the source."""
    src = HERE / 'xexec.c'
    if BIN.exists() and BIN.stat().st_mtime >= src.stat().st_mtime:
        return BIN
    BIN.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['gcc', *CFLAGS, '-o', str(BIN), str(src), '-ldl', '-lm'], check=True)
    return BIN


@dataclass
class Result:
    rc: int
    stdout: str
    stderr: str
    calls: list = field(default_factory=list)   # dicts: addr, rax, rdx, xmm0, xmm1 (ints)
    outs: dict = field(default_factory=dict)     # buffer index -> bytes after the call that received it
    dumps: list = field(default_factory=list)    # (expr, addr, bytes)
    hits: list = field(default_factory=list)     # (index of the call during which it hit, addr, [values])
    used: dict = field(default_factory=dict)     # Linux-bound import -> number of calls
    trap: str = None
    fault: str = None
    timeout: bool = False
    gdb_script: str = None

    @property
    def ok(self):
        return self.rc == 0 and not self.trap and not self.fault and not self.timeout


def parse(rc, out, err):
    r = Result(rc, out, err)
    for line in out.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == 'call':
            r.calls.append({'addr': int(f[2], 16), **{k: int(v, 16) for k, v in (x.split('=') for x in f[3:])}})
        elif f[0] == 'out':
            r.outs[int(f[1][1:])] = bytes.fromhex(f[3])
        elif f[0] == 'dump':
            r.dumps.append((f[1], int(f[2], 16), bytes.fromhex(f[3]) if len(f) > 3 else b''))
        elif f[0] == 'used':
            r.used[f[1]] = int(f[2])
        elif f[0] == 'HIT':
            r.hits.append((len(r.calls), int(f[1], 16), [int(x, 16) for x in f[2:]]))
    m = re.search(r'^TRAP (.*)$', err, re.M)
    r.trap = m.group(1) if m else None
    m = re.search(r'^FAULT (.*)$', err, re.M)
    r.fault = m.group(1) if m else None
    return r


class Runner:
    def __init__(self, slice_path=SLICE, timeout=20):
        self.bin, self.slice, self.timeout = build(), slice_path, timeout
        self.log = []                                # (argv, Result) for every run, for evidence

    def run(self, tokens, skip=None, gdb_script=None):
        if skip and gdb_script:
            raise ValueError('skip and gdb_script are mutually exclusive')
        argv = [str(self.bin), self.slice, *map(str, tokens)]
        cmd = argv
        if gdb_script:
            cmd = ['gdb', '-q', '-batch', '-nx', '-x', str(gdb_script), '--args', *argv]
        if skip:
            script = ['set pagination off', 'set confirm off', 'break xcall', 'run', 'delete 1']
            for addr, exprs in skip.items():
                fmt = ' '.join(['%lx'] * len(exprs))
                script += [f'break *{addr:#x}', 'commands', 'silent',
                           f'printf "HIT {addr:#x} {fmt}\\n", ' + ', '.join(f'(unsigned long)({e})' for e in exprs),
                           'return', 'continue', 'end']
            script.append('continue')
            gdbx = tempfile.NamedTemporaryFile('w', suffix='.gdb', delete=False)
            gdbx.write('\n'.join(script) + '\n')
            gdbx.close()
            cmd = ['gdb', '-q', '-batch', '-nx', '-x', gdbx.name, '--args', *argv]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
            res = parse(p.returncode, p.stdout, p.stderr)
        except subprocess.TimeoutExpired as e:
            res = Result(-1, (e.stdout or b'').decode(errors='replace') if isinstance(e.stdout, bytes) else (e.stdout or ''),
                         '', timeout=True)
        if skip:
            res.gdb_script = Path(gdbx.name).read_text()
            os.unlink(gdbx.name)
        self.log.append((cmd if skip else argv[1:], res))
        return res


# ---- value encoding and decoding -------------------------------------------------
def f32(x):
    """Round a Python float to binary32 and widen it back."""
    return struct.unpack('<f', struct.pack('<f', x))[0]


def dbl(x):
    """Argument token passing x exactly as binary64 (hex float literal)."""
    return 'd:' + float(x).hex()


def flt(x):
    """Argument token passing binary32(x) in the low lane of the next xmm register."""
    return 'f:' + f32(x).hex()


def as_f64(bits):
    return struct.unpack('<d', struct.pack('<Q', bits))[0]


def as_f32(bits):
    return struct.unpack('<f', struct.pack('<I', bits & 0xffffffff))[0]


def ustr(data):
    """Decode the UTF-16LE text of a Live string block (header +0 refcount, +4 byte size, text at +16)."""
    return data.decode('utf-16-le').rstrip('\0')


def libcxx_string(raw24, heap=None):
    """Decode a libc++ std::string (x86_64, standard layout) from its 24 raw bytes.
    Short mode: byte 0 = size << 1 (bit 0 clear), text at +1.
    Long mode: qword 0 = capacity | 1, qword 1 = size, qword 2 = data pointer; pass heap = bytes at it."""
    if raw24[0] & 1 == 0:
        return raw24[1:1 + (raw24[0] >> 1)].decode('latin-1')
    size = struct.unpack_from('<Q', raw24, 8)[0]
    if heap is None:
        raise ValueError('long-mode string: dump the data pointer (qword at +16) for %d bytes' % size)
    return heap[:size].decode('latin-1')


if __name__ == '__main__':
    assert libcxx_string(bytes([6]) + b'abc' + bytes(20)) == 'abc'
    assert ustr('25R\0'.encode('utf-16-le')) == '25R'
    assert f32(0.33) == 0.33000001311302185
    assert parse(0, 'call 0 0x10 rax=0x1 rdx=0x2 xmm0=0x3ff0000000000000 xmm1=0x0\nout b0 0x20 0a0b\n', '').outs[0] == b'\n\x0b'
    print('xexec.py self-check ok')
