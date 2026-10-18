# usage: words.py <va> <count> : dump 32-bit instruction words; decode movz wN,#imm and bl targets
import sys, struct
exec(open(__file__.rsplit('/',1)[0]+'/memlib.py').read())
va=int(sys.argv[1],16); n=int(sys.argv[2])
for i in range(n):
    a=va+4*i; w=struct.unpack_from('<I',D,off(a))[0]; d=''
    if (w&0x7f800000)==0x52800000: d='movz %s%d, #%#x'%('x' if w>>31 else 'w', w&31, (w>>5)&0xffff)
    elif (w>>26)==0x25: imm=w&0x3ffffff; imm-= (1<<26) if imm>>25 else 0; d='bl %#x'%(a+4*imm)
    elif (w&0x7fe0ffe0)==0x2a0003e0: d='mov %s%d, %s%d'%('x' if w>>31 else 'w', w&31,'x' if w>>31 else 'w',(w>>16)&31)
    print(hex(a),'%08x'%w,d)
