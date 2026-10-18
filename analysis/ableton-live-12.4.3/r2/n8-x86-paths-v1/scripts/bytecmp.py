# usage: python3 -I bytecmp.py <fileA> <baseA> <vaA> <fileB> <baseB> <vaB> <len>  -> equal-byte ratio and per-16-byte-row equality
import sys
a = open(sys.argv[1], 'rb').read(); b = open(sys.argv[4], 'rb').read()
oa = int(sys.argv[3], 16) - int(sys.argv[2], 16); ob = int(sys.argv[6], 16) - int(sys.argv[5], 16); n = int(sys.argv[7], 16)
x, y = a[oa:oa + n], b[ob:ob + n]
eq = sum(p == q for p, q in zip(x, y))
print(f'equal bytes {eq}/{n} ({eq / n:.3f})')
print('rows identical:', sum(x[i:i + 16] == y[i:i + 16] for i in range(0, n, 16)), 'of', (n + 15) // 16)
