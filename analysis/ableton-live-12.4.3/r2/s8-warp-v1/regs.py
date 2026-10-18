"""Extract member registrations (FUN_10147e954 calls) from corpus pseudocode (analyst tool; output is data).
usage: python3 -I regs.py <entry>...   prints offset, name, type (low 32 bits, or the variable holding it) and flags (high 32 bits; 0 when the
decompiler shows no high half) of the last argument.
Depends on corpus_lookup.py (same directory) and the C1 corpus."""
import io, re, sys, contextlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_lookup
for e in sys.argv[1:]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        corpus_lookup.code([e])
    code = re.sub(r'\s+', ' ', buf.getvalue())
    print('//', e)
    for m in re.finditer(r'FUN_10147e954\(([^;]*?)\);', code):
        a = [x.strip() for x in m.group(1).split(',')]
        last, flags, t = a[-1], 0, None
        c = re.fullmatch(r'CONCAT44\((\w+),(\w+)\)', last)
        if c:
            flags, last = int(c.group(1), 0), c.group(2)
        if last.startswith('0x'):
            v = int(last, 16)
            flags, t = v >> 32, ((v & 0xffffffff) ^ 0x80000000) - 0x80000000
        print(f"  off={a[3]:>6} {a[4]:<36} type={t if t is not None else 'from ' + last} flags={flags}")
