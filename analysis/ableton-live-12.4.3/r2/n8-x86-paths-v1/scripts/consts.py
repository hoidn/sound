# usage: python3 -I consts.py <slice> <image-base> <kind>:<va>[:<count>]...  kind = f32|f64|hex32 (32 raw bytes)
import sys, struct
d = open(sys.argv[1], 'rb').read(); base = int(sys.argv[2], 16)
for spec in sys.argv[3:]:
    p = spec.split(':'); k, va = p[0], int(p[1], 16); n = int(p[2]) if len(p) > 2 else 1; o = va - base
    if k == 'f32': v = [round(x, 6) for x in struct.unpack_from(f'<{n}f', d, o)]
    elif k == 'f64': v = list(struct.unpack_from(f'<{n}d', d, o))
    else: v = d[o:o + 32].hex()
    print(spec, v)
