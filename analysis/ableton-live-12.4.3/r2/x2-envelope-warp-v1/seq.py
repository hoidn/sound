"""Token-sequence builder and runner for xexec2 (X2 copy of the xexec loader).

A Seq collects one process's command tokens and numbers buffers (bK) and calls (rK) in creation order,
so later tokens can refer to them. Seq.run() executes the sequence in a fresh process via tools/xexec's
Runner with XEXEC_BIN pointing at the X2 loader build. Imports: tools/xexec/xexec.py (unchanged).
"""
import os
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BIN = Path(os.environ.get('X2_BIN', '/var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2'))
os.environ['XEXEC_BIN'] = str(BIN)
sys.path.insert(0, str(ROOT / 'tools' / 'xexec'))
import xexec  # noqa: E402

xexec.BIN = BIN
N_INIT = 3322                       # __mod_init_func entries in the slice


def build():
    """Compile xexec2.c into BIN when missing or older than the source (same flags as tools/xexec)."""
    src = HERE / 'xexec2.c'
    if BIN.exists() and BIN.stat().st_mtime >= src.stat().st_mtime:
        return
    BIN.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['gcc', *xexec.CFLAGS, '-o', str(BIN), str(src), '-ldl', '-lm'], check=True)


build()
xexec.build = lambda: BIN          # never recompile tools/xexec/xexec.c over the X2 copy
R = xexec.Runner()


def d2hex(*xs):
    return struct.pack(f'<{len(xs)}d', *xs).hex()


class Seq:
    def __init__(self, init=True):
        self.tokens, self.nb, self.nc = (['init', '0', str(N_INIT)] if init else []), 0, 0

    def call(self, addr, *args):
        """args: 'buf:N', 'hex:..', 'str:..' (each makes the next bK), or i:/d:/f:/ref: tokens.
        Returns (call index, [buffer indices made by this call])."""
        made = []
        for a in args:
            if a.split(':', 1)[0] in ('buf', 'hex', 'str'):
                made.append(self.nb)
                self.nb += 1
        self.tokens += ['call', hex(addr), *args]
        self.nc += 1
        return self.nc - 1, made

    def mkbuf(self, n):
        self.tokens += ['mkbuf', str(n)]
        self.nb += 1
        return self.nb - 1

    def poke(self, kind, where, value):
        self.tokens += [kind, where, str(value)]

    def dump(self, expr, n):
        self.tokens += ['dump', expr, str(n)]

    def run(self):
        return R.run(self.tokens)


def run_skip(tokens, skip):
    """Run tokens under gdb. Each time execution reaches an address in skip, gdb prints "HIT addr" and leaves
    that function at once with `return`, so its body does not run (void functions only). SIGSEGV and SIGBUS
    pass to the loader, whose init command recovers from faults in static initializers. Same output parsing
    as tools/xexec (Runner.run with skip, which does not pass these signals)."""
    script = ['set pagination off', 'set confirm off', 'handle SIGSEGV nostop noprint pass',
              'handle SIGBUS nostop noprint pass', 'break xcall', 'run', 'delete 1']
    for addr in skip:
        script += [f'break *{addr:#x}', 'commands', 'silent', f'printf "HIT {addr:#x}\\n"', 'return', 'continue',
                   'end']
    script.append('continue')
    gdbx = HERE / '.gdb-script'
    gdbx.write_text('\n'.join(script) + '\n')
    argv = [str(BIN), xexec.SLICE, *map(str, tokens)]
    p = subprocess.run(['gdb', '-q', '-batch', '-nx', '-x', str(gdbx), '--args', *argv], capture_output=True,
                       text=True, timeout=600)
    gdbx.unlink()
    res = xexec.parse(p.returncode, p.stdout, p.stderr)
    res.gdb_script = '\n'.join(script)
    R.log.append((['gdb', *argv[1:]], res))
    return res
