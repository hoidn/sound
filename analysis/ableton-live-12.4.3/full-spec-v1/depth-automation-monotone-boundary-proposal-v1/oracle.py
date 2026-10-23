"""Data-only finite selector and proposed local oracles; never launches original code."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
import math
import struct

EPS = F(1, 2**52)
MAX = F.from_float(float.fromhex('0x1.fffffffffffffp+1023'))
OVERFLOW_RN = MAX + F(2**970)
QNAN = 0x7ff8000000000000


def bits(value):
    return f'0x{struct.unpack("<Q", struct.pack("<d", value))[0]:016x}'


def value(raw):
    return struct.unpack('<d', int(raw, 16).to_bytes(8, 'little'))[0]


def token(raw):
    x = value(raw)
    return 'd:' + ('nan' if math.isnan(x) else x.hex())


def sign(x):
    return (x > 0) - (x < 0)


def sqrt_compare(d, t):
    """Exact comparison of nonnegative sqrt(d) with rational t."""
    assert d >= 0
    return 1 if t < 0 else sign(d - t*t)


def exact_owner(x, y):
    """Literal R5 algebra over exact supplied binary64 rationals, guard rounded products."""
    if not (math.isfinite(x) and math.isfinite(y)):
        return {'boolean': False, 'path': 'nonfinite-input'}
    if 0 <= x <= y <= 1:
        return {'boolean': True, 'path': 'ordered-region'}
    x, y = F.from_float(x), F.from_float(y)
    products = [x*x, y*y, x*y]
    if any(abs(p) >= OVERFLOW_RN for p in products):
        return {'boolean': False, 'path': 'individual-product-overflow-RN-proposal'}
    d = products[0] + products[1] - products[2] - x
    if d <= EPS:
        return {'boolean': True, 'path': 'D-at-or-below-tolerance', 'D_compare_epsilon': sign(d-EPS), 'D_sign': sign(d)}
    q, a = 2*(3*x-3*y+1), y-2*x
    if not q:
        return {'boolean': None, 'path': 'undefined-literal-q-zero'}
    # For each root compare with0/1, avoiding numerical square roots entirely.
    c1, c2 = sqrt_compare(d, a), sqrt_compare(d, a+q/2)
    r1gt0, r1lt1 = (c1 > 0, c2 < 0) if q > 0 else (c1 < 0, c2 > 0)
    c3, c4 = sqrt_compare(d, -a), sqrt_compare(d, -a-q/2)
    r2le0, r2ge1 = (c3 >= 0, c4 <= 0) if q > 0 else (c3 <= 0, c4 >= 0)
    yes = False if r1gt0 and r1lt1 else r2le0 or r2ge1
    return {'boolean': yes, 'path': 'r1-interior-reject' if r1gt0 and r1lt1 else 'r2-exterior-accept' if yes else 'r2-other-reject',
            'D_compare_epsilon': 1, 'q_sign': sign(q), 'root_comparisons': {'r1_gt0': r1gt0, 'r1_lt1': r1lt1, 'r2_le0': r2le0, 'r2_ge1': r2ge1},
            'radical_comparison_signs': [c1, c2, c3, c4]}


def binary64_owner(x, y):
    """Declared non-fused, left-associated Python binary64 reading, not target calibration."""
    if not (math.isfinite(x) and math.isfinite(y)):
        return {'boolean': False, 'path': 'nonfinite-input'}
    if 0 <= x <= y <= 1:
        return {'boolean': True, 'path': 'ordered-region'}
    p1, p2, p3 = x*x, y*y, x*y
    if not all(math.isfinite(p) for p in [p1, p2, p3]):
        return {'boolean': False, 'path': 'individual-product-overflow-RN-proposal'}
    d = ((p1+p2)-p3)-x
    detail = {'D_binary64': bits(d)}
    if not math.isfinite(d):
        return {'boolean': None, 'path': 'unresolved-intermediate-D-nonfinite', **detail}
    if d <= float(EPS):
        return {'boolean': True, 'path': 'D-at-or-below-tolerance', 'D_compare_epsilon': sign(d-float(EPS)), 'D_sign': sign(d), **detail}
    q, a = 2*((3*x-3*y)+1), y-2*x
    detail.update(q_binary64=bits(q), a_binary64=bits(a))
    if not math.isfinite(q) or q == 0:
        return {'boolean': None, 'path': 'unresolved-rounded-q-zero-or-nonfinite', **detail}
    root = math.sqrt(d)
    r1, r2 = (2*root-2*a)/q, (-2*root-2*a)/q
    detail.update(r1_binary64=bits(r1), r2_binary64=bits(r2))
    if not (math.isfinite(r1) and math.isfinite(r2)):
        return {'boolean': None, 'path': 'unresolved-nonfinite-root', **detail}
    comparisons = {'r1_gt0': r1 > 0, 'r1_lt1': r1 < 1, 'r2_le0': r2 <= 0, 'r2_ge1': r2 >= 1}
    yes = False if 0 < r1 < 1 else r2 <= 0 or r2 >= 1
    return {'boolean': yes, 'path': 'r1-interior-reject' if 0 < r1 < 1 else 'r2-exterior-accept' if yes else 'r2-other-reject',
            'D_compare_epsilon': 1, 'q_sign': sign(q), 'root_comparisons': comparisons, **detail}


def exact_cubic(x, y):
    """Separate exact derivative nonnegativity, without R5 tolerance/overflow rule."""
    if not (math.isfinite(x) and math.isfinite(y)):
        return {'boolean': None, 'path': 'not-a-finite-real-cubic'}
    x, y = F.from_float(x), F.from_float(y)
    if x < 0 or y > 1:
        return {'boolean': False, 'path': 'negative-endpoint-derivative'}
    a, b = 3*x-3*y+1, 2*(y-2*x)
    if a > 0 and 0 < -b < 2*a:
        v = x - b*b/(4*a)
        return {'boolean': v >= 0, 'path': 'interior-minimum', 'minimum_sign': sign(v)}
    return {'boolean': True, 'path': 'endpoint-minimum-nonnegative'}


def classify(raw1, raw2):
    x, y = value(raw1), value(raw2)
    binary, exact, cubic = binary64_owner(x, y), exact_owner(x, y), exact_cubic(x, y)
    reasons = []
    if binary['boolean'] is None:
        reasons.append(binary['path'])
    if exact['boolean'] is None:
        reasons.append(exact['path'])
    if binary['boolean'] != exact['boolean']:
        reasons.append('binary64-versus-exact-R5-boolean-disagreement')
    if binary['path'] != exact['path']:
        reasons.append('binary64-versus-exact-R5-branch-disagreement')
    if binary.get('root_comparisons') != exact.get('root_comparisons'):
        reasons.append('binary64-versus-exact-R5-root-comparison-disagreement')
    expected = None if reasons else binary['boolean']
    return {'expected_boolean': expected, 'disposition': 'NULL-local-oracle-ungraded-discovery' if reasons else 'predeclared-local-R5-comparison-only',
            'unresolved_reasons': reasons, 'binary64_literal_R5': binary, 'exact_rational_R5': exact, 'exact_cubic_separate': cubic,
            'R5_vs_exact_cubic': None if expected is None or cubic['boolean'] is None else expected != cubic['boolean']}


def neighbors(raw):
    x=value(raw)
    assert math.isfinite(x)
    return [bits(math.nextafter(x,-math.inf)),raw,bits(math.nextafter(x,math.inf))]


def rounded_center(c1, tau, branch, precision):
    with localcontext() as ctx:
        ctx.prec=precision
        x=Decimal.from_float(value(c1))
        t=Decimal(tau.numerator)/Decimal(tau.denominator)
        disc=-3*x*x+4*x+4*t
        assert disc >= 0
        return bits(float((x + branch*disc.sqrt())/2))


def universe():
    """Finite union: whole Cartesian anchor grid + every declared3x3 neighbor family."""
    # Families are selected arithmetically before any original result is available.
    rootmax=bits(float.fromhex('0x1.fffffffffffffp+511'))
    anchors=[-math.inf,math.inf,value(f'0x{QNAN:016x}'),-float(MAX),float(MAX),-1e308,1e308]
    anchors += [value(b) for b in neighbors(rootmax)]
    anchors += [-value(b) for b in neighbors(rootmax)]
    anchors += [-2.,-1.5,-1.,-.5,-2.**-26,-2.**-52,-2.**-1022,-2.**-1074,-0.,0.,2.**-1074,2.**-1022,2.**-52,2.**-26]
    anchors += [.2,.25,1/3,.5,2/3,.75,.8,math.nextafter(.5,-math.inf),math.nextafter(.5,math.inf),math.nextafter(1.,-math.inf),1.,math.nextafter(1.,math.inf),4/3,1.5,2.]
    anchorbits=list(dict.fromkeys(bits(x) for x in anchors))
    members={}
    def add(x,y,family):
        members.setdefault((x,y),set()).add(family)
    for x in anchorbits:
        for y in anchorbits:
            add(x,y,'whole-anchor-Cartesian-grid')
    families=[]
    def neighborhood(x,y,name,detail):
        xs,ys=neighbors(x),neighbors(y)
        families.append({'id':name,'center_binary64':[x,y],'x_neighbors':xs,'y_neighbors':ys,'universe':'whole3x3Cartesian','detail':detail})
        for a in xs:
            for b in ys:
                add(a,b,name)
    # The conic D=tau is solved for c2, using exact supplied c1; retain both roots.
    for x in [0.,.25,.5,.75,1.,1.25,4/3]:
        for tau,label in [(F(0),'zero'),(EPS,'epsilon')]:
            for branch in [-1,1]:
                c1=bits(x);lo=rounded_center(c1,tau,branch,400);hi=rounded_center(c1,tau,branch,800)
                assert lo==hi, 'center rounding unstable; no substitute selection'
                neighborhood(c1,hi,f'D-{label}-c1-{c1}-root-{branch}',{'equation':'c2=(c1 +/- sqrt(-3*c1^2+4*c1+4*tau))/2','tau_fraction':str(tau),'root_sign':branch,'center_rounding':'Decimal400 and800 round to identicalbinary64; rounded center is not claimed exact algebraic root'})
    # q=0 real line c2=c1+1/3: exact binary64 input pairs cannot differ by1/3,
    # but rounded arithmetic can give q=0. Keep all such observations NULL.
    for x in [-2.,-1.,-.5,0.,.25,1/3,.5,1.,1.5,2.]:
        with localcontext() as ctx:
            ctx.prec=800;y=bits(float(Decimal.from_float(x)+Decimal(1)/3))
        neighborhood(bits(x),y,f'q-line-c1-{bits(x)}',{'equation':'c2=c1+1/3; real line rounded to binary64; q-zero remains undefined in literal R5 division'})
    for v in [-2.,-1.,-.5,-2.**-1074,-0.,0.,2.**-1074,.25,.5,.75,1.,1.5,2.]:
        neighborhood(bits(0.),bits(v),f'root0-c2-{bits(v)}',{'equation':'c1=0 endpoint derivative/root condition, with both coordinate nextafter neighbors'})
        neighborhood(bits(v),bits(1.),f'root1-c1-{bits(v)}',{'equation':'c2=1 endpoint derivative/root condition, with both coordinate nextafter neighbors'})
    vectors=[]
    for n,((x,y),membership) in enumerate(sorted(members.items()),1):
        vectors.append({'id':f'MB-{n:04d}','pair_binary64':[x,y],'arguments_binary64':['0x0000000000000000',x,y,'0x3ff0000000000000'],
            'tokens':['call','0x1011f2080','d:0x0.0p+0',token(x),token(y),'d:0x1.0000000000000p+0'],
            'memberships':sorted(membership),**classify(x,y)})
    return anchorbits,families,vectors
