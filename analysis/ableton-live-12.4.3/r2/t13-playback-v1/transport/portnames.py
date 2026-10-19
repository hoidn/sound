"""Decode libc++ short-string port names built byte by byte in decompiled processor SEnable code
(analyst tool; output is data). usage: python3 -I portnames.py <corpus> <entry>..."""
import json, re, subprocess, sys
here = __file__.rsplit('/', 1)[0]
for e in sys.argv[2:]:
    code = subprocess.run([sys.executable, '-I', here + '/../lookup.py', sys.argv[1], 'code', e], capture_output=True, text=True).stdout
    cur, out = {}, []
    for line in code.splitlines():
        m = re.match(r'\s*local_\w+\[(0x[0-9a-f]+|\d+)\] = (0x[0-9a-f]+|\d+);', line)
        if m:
            cur[int(m.group(1), 0)] = int(m.group(2), 0)
            continue
        if cur:
            n = cur.get(0, 0) // 2
            out.append(''.join(chr(cur.get(i, 0)) for i in range(1, n + 1)))
            cur = {}
    print(e, out)
