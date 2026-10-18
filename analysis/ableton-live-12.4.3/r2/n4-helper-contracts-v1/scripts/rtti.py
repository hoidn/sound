# usage: rtti.py <vtable-address-point>... : typeinfo name at vt-8, then slots
import sys, struct, subprocess
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open(__file__.rsplit('/',1)[0]+'/memlib.py').read())
for a in sys.argv[1:]:
    vt=int(a,16)
    ti=rd(vt-8)
    name=''
    if ti:
        o=off(ti+8); nm=struct.unpack_from("<Q",D,o)[0]&0x7fffffffffffffff; name=cstr(nm)
    print(hex(vt),'typeinfo',hex(ti),name)
    for i in range(int(N)):
        print('   +%#x'%(8*i), hex(rd(vt+8*i)))
